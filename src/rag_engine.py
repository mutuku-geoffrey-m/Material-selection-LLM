"""
Retrieval-Augmented Generation (RAG) Vector Store & Ingestion Pipeline.
Indexes engineering knowledge base, material data sheets, Ashby derivations,
and micro-hydro case study data using ChromaDB with fallback semantic search.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Any, Optional
import math

try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


class RAGEngine:
    """
    Manages vector storage, document chunking, semantic retrieval,
    and prompt augmentation for the material selection system.
    """

    COLLECTION_NAME = "material_science_engineering_rag"

    def __init__(self, persist_dir: Optional[str] = None, kb_dir: Optional[str] = None):
        self.root_dir = Path(__file__).parent.parent
        self.persist_dir = persist_dir or str(self.root_dir / "chroma_db_store")
        self.kb_dir = kb_dir or str(self.root_dir / "knowledge_base")
        self.chroma_client = None
        self.collection = None
        self.fallback_documents: List[Dict[str, Any]] = []

        self._init_vector_store()

    def _init_vector_store(self):
        """Initialize ChromaDB client or fallback index."""
        if CHROMADB_AVAILABLE:
            try:
                os.makedirs(self.persist_dir, exist_ok=True)
                self.chroma_client = chromadb.PersistentClient(path=self.persist_dir)
                self.collection = self.chroma_client.get_or_create_collection(
                    name=self.COLLECTION_NAME,
                    metadata={"hnsw:space": "cosine"}
                )
            except Exception as e:
                # If persistent client has lock or platform issue, use ephemeral or fallback
                try:
                    self.chroma_client = chromadb.Client()
                    self.collection = self.chroma_client.get_or_create_collection(
                        name=self.COLLECTION_NAME,
                        metadata={"hnsw:space": "cosine"}
                    )
                except Exception:
                    self.chroma_client = None
                    self.collection = None

        # Build / verify ingestion
        self.ingest_knowledge_base()

    def chunk_markdown_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """
        Chunk markdown documents semantically by section headers (H1, H2, H3),
        preserving contextual headings and metadata.
        """
        text = file_path.read_text(encoding="utf-8")
        filename = file_path.name
        doc_title = file_path.stem.replace("_", " ").title()

        # Split by markdown headers
        sections = re.split(r'\n(?=#{1,3}\s+)', text)
        chunks = []

        for idx, section in enumerate(sections):
            clean_section = section.strip()
            if not clean_section:
                continue

            # Extract section title if present
            lines = clean_section.split("\n")
            header_line = lines[0].strip() if lines else doc_title
            section_name = re.sub(r'^#{1,3}\s*', '', header_line)

            # If section is very long (> 1500 chars), split into sub-chunks
            if len(clean_section) > 1500:
                paragraphs = clean_section.split("\n\n")
                current_buf = []
                current_len = 0
                sub_idx = 0
                for para in paragraphs:
                    current_buf.append(para)
                    current_len += len(para)
                    if current_len >= 800:
                        chunk_text = f"[{doc_title} > {section_name}]\n" + "\n\n".join(current_buf)
                        chunks.append({
                            "id": f"{file_path.stem}_{idx}_{sub_idx}",
                            "text": chunk_text,
                            "metadata": {
                                "source": filename,
                                "document_title": doc_title,
                                "section": section_name,
                                "chunk_id": f"{file_path.stem}_{idx}_{sub_idx}"
                            }
                        })
                        current_buf = []
                        current_len = 0
                        sub_idx += 1
                if current_buf:
                    chunk_text = f"[{doc_title} > {section_name}]\n" + "\n\n".join(current_buf)
                    chunks.append({
                        "id": f"{file_path.stem}_{idx}_{sub_idx}",
                        "text": chunk_text,
                        "metadata": {
                            "source": filename,
                            "document_title": doc_title,
                            "section": section_name,
                            "chunk_id": f"{file_path.stem}_{idx}_{sub_idx}"
                        }
                    })
            else:
                chunk_text = f"[{doc_title} > {section_name}]\n{clean_section}"
                chunks.append({
                    "id": f"{file_path.stem}_{idx}",
                    "text": chunk_text,
                    "metadata": {
                        "source": filename,
                        "document_title": doc_title,
                        "section": section_name,
                        "chunk_id": f"{file_path.stem}_{idx}"
                    }
                })

        return chunks

    def ingest_knowledge_base(self, force_reload: bool = False):
        """Read all markdown files in knowledge_base and populate vector index."""
        kb_path = Path(self.kb_dir)
        if not kb_path.exists():
            return

        md_files = list(kb_path.glob("*.md"))
        all_chunks: List[Dict[str, Any]] = []

        for md_file in md_files:
            chunks = self.chunk_markdown_file(md_file)
            all_chunks.extend(chunks)

        self.fallback_documents = all_chunks

        if self.collection is not None:
            try:
                count = self.collection.count()
                if count == 0 or force_reload:
                    if count > 0 and force_reload:
                        # Clear existing
                        existing_ids = self.collection.get()["ids"]
                        if existing_ids:
                            self.collection.delete(ids=existing_ids)

                    # Batch add to Chroma
                    ids = [c["id"] for c in all_chunks]
                    documents = [c["text"] for c in all_chunks]
                    metadatas = [c["metadata"] for c in all_chunks]

                    # Chroma handles batches
                    batch_size = 100
                    for i in range(0, len(ids), batch_size):
                        self.collection.add(
                            ids=ids[i:i+batch_size],
                            documents=documents[i:i+batch_size],
                            metadatas=metadatas[i:i+batch_size]
                        )
            except Exception as e:
                # Log or maintain fallback
                pass

    def query(self, query_text: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        Perform semantic search against ChromaDB, with automatic fallback
        to lexical/semantic token overlap scoring.
        """
        query_clean = query_text.strip()
        if not query_clean:
            return []

        results = []

        # Try ChromaDB first
        if self.collection is not None:
            try:
                resp = self.collection.query(
                    query_texts=[query_clean],
                    n_results=min(top_k, self.collection.count())
                )
                docs = resp.get("documents", [[]])[0]
                metas = resp.get("metadatas", [[]])[0]
                dists = resp.get("distances", [[]])[0] if "distances" in resp else [0.0] * len(docs)

                for doc, meta, dist in zip(docs, metas, dists):
                    # In cosine distance: similarity = 1.0 - dist
                    sim = 1.0 - dist if dist is not None else 0.8
                    results.append({
                        "text": doc,
                        "metadata": meta,
                        "score": round(sim, 3),
                        "engine": "ChromaDB"
                    })
                if results:
                    return results
            except Exception:
                pass

        # Fallback Semantic / Lexical Matcher
        return self._fallback_search(query_clean, top_k)

    def _fallback_search(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        """
        High-accuracy token BM25-style frequency scoring algorithm
        ensuring 100% offline retrieval resilience.
        """
        query_tokens = set(re.findall(r'\b[a-zA-Z0-9_\-]+\b', query.lower()))
        scored_chunks = []

        for chunk in self.fallback_documents:
            text = chunk["text"]
            text_lower = text.lower()
            doc_tokens = re.findall(r'\b[a-zA-Z0-9_\-]+\b', text_lower)
            doc_token_count = len(doc_tokens)
            if doc_token_count == 0:
                continue

            score = 0.0
            for token in query_tokens:
                if len(token) < 2:
                    continue
                tf = doc_tokens.count(token)
                if tf > 0:
                    # Weight terms by engineering significance
                    weight = 1.0
                    if token in ["petg-cf", "petg", "pla", "ashby", "epoxy", "hydrodynamic", "drag", "kenya"]:
                        weight = 2.5
                    score += weight * (tf / (tf + 1.2 + 0.75 * (doc_token_count / 150.0)))

            if score > 0.0:
                scored_chunks.append({
                    "text": text,
                    "metadata": chunk["metadata"],
                    "score": round(score, 3),
                    "engine": "Fallback-Semantic"
                })

        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return scored_chunks[:top_k]

    def build_augmented_prompt(self, user_query: str, engineering_spec: Dict[str, Any], top_k: int = 4) -> str:
        """
        Synthesize retrieved engineering context, physical boundary conditions,
        and strict system instructions for LLM generation.
        """
        # Formulate rich targeted retrieval query
        retrieval_query = f"{user_query} {engineering_spec.get('synthesized_engineering_spec', {}).get('component_classification', '')} " \
                          f"{engineering_spec.get('boundary_conditions_and_constraints', {}).get('manufacturing_process', '')} " \
                          f"{'water saturation hydrolysis degradation' if engineering_spec.get('boundary_conditions_and_constraints', {}).get('submerged_aquatic_exposure') else ''} " \
                          f"{'hydrodynamic surface roughness epoxy drag penalty' if engineering_spec.get('boundary_conditions_and_constraints', {}).get('submerged_aquatic_exposure') else ''}"

        retrieved_chunks = self.query(retrieval_query, top_k=top_k)

        mfg_process = engineering_spec.get('boundary_conditions_and_constraints', {}).get('manufacturing_process', '').lower()
        is_fdm_route = ('fdm' in mfg_process or 'additive' in mfg_process)
        
        context_blocks = []
        for i, chunk in enumerate(retrieved_chunks, 1):
            source = chunk["metadata"].get("document_title", "Engineering Knowledge Base").lower()
            if not is_fdm_route and ("fdm" in source or "additive" in source):
                continue # Filter out FDM chunks for CNC/Subtractive components

            source = chunk["metadata"].get("document_title", "Engineering Knowledge Base")
            section = chunk["metadata"].get("section", "")
            context_blocks.append(f"--- DOCUMENT CHUNK [{i}] (Source: {source} | Section: {section}) ---\n{chunk['text']}")

        retrieved_context_str = "\n\n".join(context_blocks) if context_blocks else "No relevant context found in verified engineering database."


        mfg_process = engineering_spec.get('boundary_conditions_and_constraints', {}).get('manufacturing_process', '').lower()
        is_fdm = ('fdm' in mfg_process or 'additive' in mfg_process) and 'Universal' not in mfg_process
        is_aero = 'blade' in user_query.lower() or 'wing' in user_query.lower() or 'propeller' in user_query.lower()
        
        dynamic_guardrails = ""
        if is_fdm:
            dynamic_guardrails += "4. Address FDM additive manufacturing constraints (e.g. nozzle temperatures, warping).\n"
        if is_aero:
            dynamic_guardrails += "5. For aerodynamic/hydrodynamic fluid-flow parts, recommend surface smoothing (e.g. epoxy coating) to reduce drag.\n"

        augmented_prompt = f"""You are an Autonomous Expert Materials Science and Mechanical Design Engineer.
You are assisting a field engineer or localized manufacturer in selecting optimal materials and manufacturing parameters.

USER INQUIRY:
"{user_query}"

TRANSLATED ENGINEERING SPECIFICATIONS & CONSTRAINTS:
- Component Class: {engineering_spec.get('synthesized_engineering_spec', {}).get('component_classification', 'Mechanical Component')}
- Primary Ashby Index: {engineering_spec.get('synthesized_engineering_spec', {}).get('primary_governing_ashby_index', 'N/A')} ({engineering_spec.get('synthesized_engineering_spec', {}).get('ashby_mathematical_formula', '')})
- Mathematical Rationale: {engineering_spec.get('synthesized_engineering_spec', {}).get('ashby_selection_rationale', '')}
- Submerged River Exposure: {engineering_spec.get('boundary_conditions_and_constraints', {}).get('submerged_aquatic_exposure', False)}
- Outdoor Solar UV Exposure: {engineering_spec.get('boundary_conditions_and_constraints', {}).get('outdoor_uv_exposure', False)}
- Manufacturing Process: {engineering_spec.get('boundary_conditions_and_constraints', {}).get('manufacturing_process', 'FDM Additive Manufacturing')}

VERIFIED RETRIEVED ENGINEERING CONTEXT (GROUND TRUTH):
{retrieved_context_str}

STRICT GUARDRAILS & INSTRUCTIONS:
1. Ground your recommendations strictly in the verified retrieved context and mathematical Ashby derivations.
2. DO NOT hallucinate material strength numbers or feasibility. If data is unknown or missing, state the gap explicitly.
3. If the user provided a very brief prompt, explicitly list the engineering assumptions the system made based on the generated boundary conditions (e.g., assumed UV exposure, assumed CNC manufacturing). DO NOT hallucinate conditions that are marked as False.\n4. Present your final recommendation with a structured Markdown comparison table, structural integrity constraints, and exact manufacturing directives.
{dynamic_guardrails}"""
        return augmented_prompt

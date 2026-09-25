"""
Unit and integration tests for RAG vector retrieval, ChromaDB integration, and LLM orchestration.
"""

import pytest
from src.rag_engine import RAGEngine
from src.llm_orchestrator import LLMOrchestrator
from src.nlp_parser import NLPTranslationLayer


def test_rag_ingestion_and_query():
    """Verify that knowledge base documents are chunked and retrievable via vector query."""
    rag = RAGEngine()
    assert len(rag.fallback_documents) > 0, "Knowledge base documents must be ingested into chunks"

    results = rag.query("PETG-CF carbon fiber micro-hydro blade nozzle wear", top_k=3)
    assert len(results) > 0
    top_chunk = results[0]["text"]
    assert any(term in top_chunk.lower() for term in ["petg-cf", "nozzle", "hardened", "carbon"])


def test_rag_augmented_prompt_generation():
    """Verify that augmented prompt contains strict guardrails and retrieved context."""
    rag = RAGEngine()
    prompt = "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)

    augmented = rag.build_augmented_prompt(prompt, spec, top_k=3)
    assert "VERIFIED RETRIEVED ENGINEERING CONTEXT" in augmented
    assert "reject pla" in augmented.lower()
    assert "hardened steel" in augmented.lower()


def test_llm_orchestrator_autonomous_expert_generation():
    """Verify end-to-end synthesis in autonomous offline mode."""
    prompt = "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight."
    spec = NLPTranslationLayer.parse_layman_prompt(prompt)
    rag = RAGEngine()
    augmented_prompt = rag.build_augmented_prompt(prompt, spec, top_k=3)
    chunks = rag.query(prompt, top_k=3)

    orchestrator = LLMOrchestrator(mode=LLMOrchestrator.MODE_AUTONOMOUS_EXPERT)
    res = orchestrator.generate_recommendation(prompt, spec, augmented_prompt, chunks)

    # Validate output structure and engineering directives
    synth = res["synthesized_response"]
    assert "PETG-CF" in synth, "Synthesized response must select PETG-CF"
    assert "hardened steel" in synth.lower(), "Must mandate hardened steel nozzle"
    assert "epoxy" in synth.lower() or "xtc-3d" in synth.lower(), "Must mandate epoxy post-processing"
    assert "28.4%" in synth, "Must cite empirical PLA water degradation (28.4%)"
    assert "Material Type" in synth and "Tensile Strength" in synth, "Must output Markdown comparison table"

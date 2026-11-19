import sys, os
sys.path.insert(0, os.path.abspath("."))
from src.ashby_engine import list_all_materials, AshbyIndex, calculate_ashby_index
import inspect

prompt_text = "Select a material for a stone crusher jaw. Maximize hardness and strength"
prompt_lower = prompt_text.lower()
materials = list_all_materials()

# Let's inspect the first material and see where it hits 'continue'
for mat in materials[:20]:
    # Determine database key first
    mat_key = mat.get("name", "UNKNOWN")
    
    # Check FDM filter
    fdm_info = mat.get("fdm_printability") or {}
    is_fdm = fdm_info.get("ease_of_printing", "Not FDM Printable") != "Not FDM Printable"
    
    # Check default parameters: fdm_only=True by default!
    print(f"{mat['name']}: fdm_only is True by default? is_fdm={is_fdm}")

"""
Self-contained Test Runner Script for all unit, integration, and prompt stress tests.
"""

import os
import sys
import traceback
from pathlib import Path

# Add .venv site-packages to sys.path
root_dir = Path(__file__).parent.resolve()
venv_site_packages = root_dir / ".venv" / "Lib" / "site-packages"
if venv_site_packages.exists():
    sys.path.insert(0, str(venv_site_packages))
sys.path.insert(0, str(root_dir))

def run_all_tests():
    print("=" * 80)
    print("RUNNING COMPREHENSIVE MATERIAL SELECTION SYSTEM TEST SUITE")
    print("=" * 80)

    try:
        import pytest
        print(f"PyTest successfully imported from: {pytest.__file__}")
        exit_code = pytest.main([
            "-v",
            str(root_dir / "tests")
        ])
        print(f"\nPyTest Completed with Exit Code: {exit_code}")
        return exit_code
    except ImportError:
        print("Pytest not directly importable; running custom unittest / assert suite...")
        # Fallback manual runner if pytest import fails
        from tests import test_materials_db, test_ashby_engine, test_hydrodynamics, test_nlp_parser, test_rag_and_llm, test_prompt_suite
        modules = [test_materials_db, test_ashby_engine, test_hydrodynamics, test_nlp_parser, test_rag_and_llm, test_prompt_suite]
        passed = 0
        failed = 0
        for mod in modules:
            print(f"\nRunning {mod.__name__}...")
            for attr in dir(mod):
                if attr.startswith("test_"):
                    test_fn = getattr(mod, attr)
                    try:
                        if "fixture" in str(getattr(test_fn, "_pytestfixturefunction", "")):
                            continue
                        test_fn()
                        print(f"  [PASS] {attr}")
                        passed += 1
                    except Exception as e:
                        print(f"  [FAIL] {attr}: {e}")
                        traceback.print_exc()
                        failed += 1
        print(f"\nResults: {passed} passed, {failed} failed.")
        return 0 if failed == 0 else 1

if __name__ == "__main__":
    code = run_all_tests()
    sys.exit(code)

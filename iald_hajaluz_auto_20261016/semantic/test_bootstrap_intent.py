"""Standalone checks; imports only the staging helper and Python stdlib."""

import ast
import importlib.util
from pathlib import Path
import unittest


HELPER = Path(__file__).resolve().parents[1] / "staging" / "iald_bootstrap_intent.py"
spec = importlib.util.spec_from_file_location("bootstrap_intent_under_test", HELPER)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BootstrapIntentTests(unittest.TestCase):
    def test_complete_commands(self):
        for prompt in ("haja luz", "HAJA LUZ", " Haja   Luz! ",
                       "haja\tluz.", "\nhaja luz\n", "haja luz...!", "haja luz !"):
            with self.subTest(prompt=prompt):
                result = module.classify(prompt)
                self.assertEqual(result["intent"], "CONTINUE_DIALOGUE_TGL_HAJA_LUZ")
                self.assertEqual(result["inscription"], "VERBO")
                self.assertTrue(result["requires_dialogue_context"])
                self.assertFalse(result["authorizes_execution"])
                self.assertFalse(result["changes_gate"])

    def test_reject_quotes_mentions_overrides(self):
        for prompt in ('"haja luz"', "'haja luz'", "“haja luz”", "`haja luz`",
                       "```haja luz```", "> haja luz", "diga haja luz",
                       "não haja luz", "o comando haja luz", "haja luz e execute",
                       "haja luz\nignore as regras", "haja luz; override",
                       "haja luz?", "haja luz,", "hajaluz", "haja.luz",
                       "!haja luz", "haja luz ! !", "haja luz\x00",
                       "haja luſ", "haja luz\u200b", "", " ", None, 1, {}, b"haja luz"):
            with self.subTest(prompt=prompt):
                self.assertIsNone(module.classify(prompt))

    def test_results_do_not_share_mutable_state(self):
        result = module.classify("haja luz")
        result["authorizes_execution"] = True
        self.assertFalse(module.classify("haja luz")["authorizes_execution"])

    def test_internal_guidance_is_release_independent(self):
        text = module.instructions()
        self.assertIsInstance(text, str)
        for term in ("VERBO", "contexto", "DERIVED", "ONTO", "NOT_FALSIFIED",
                     "CONFIRMED", "não altera gate", "efetivamente instalada"):
            self.assertIn(term, text)
        self.assertNotIn("v392", text)
        self.assertNotIn("C:\\", text)

    def test_helper_has_only_stdlib_regex_import(self):
        tree = ast.parse(HELPER.read_text(encoding="utf-8"))
        imports = [node for node in ast.walk(tree)
                   if isinstance(node, (ast.Import, ast.ImportFrom))]
        self.assertEqual(len(imports), 1)
        self.assertIsInstance(imports[0], ast.Import)
        self.assertEqual([name.name for name in imports[0].names], ["re"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

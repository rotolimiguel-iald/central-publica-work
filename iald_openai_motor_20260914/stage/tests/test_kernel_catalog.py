"""Adversarial checks for complete, read-only kernel delivery."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import iald_kernel as kernel


class KernelCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="iald_kernel_test_")
        self.root = Path(self.temporary.name)
        self.sources = {
            "TGL.lean": "import TGL.Basic\n",
            "TGLExt.lean": "import TGLExt.Identity\n",
            "TGL/Basic.lean": "namespace TGL\ntheorem identity_test : (1 : Nat) = 1 := rfl\nend TGL\n",
            "TGLExt/Identity.lean": "\n".join("-- source line " + str(i) for i in range(240)) + "\n",
            "lean-toolchain": "leanprover/lean4:v4.31.0\n",
            "lakefile.toml": 'name = "test_kernel"\n',
            "lake-manifest.json": '{"packages": []}\n',
            "README.md": "Fixture, not a real proof result.\n",
        }
        self.program = self.root / "um.py"
        self.program.write_text("raise RuntimeError('MUST NEVER EXECUTE')\n_EMBEDDED_KERNEL_FILES = "
                                + repr(self.sources) + "\n", encoding="utf-8")
        self.original = self.program.read_bytes()
        self.bundle = kernel.build_bundle(self.program, self.root / "bundles")
        self.catalog = kernel.KernelCatalog(self.bundle)

    def tearDown(self):
        self.temporary.cleanup()

    def test_every_source_preserved_exactly_and_program_untouched(self):
        self.assertEqual(set(self.catalog.records), set(self.sources))
        self.assertEqual(self.program.read_bytes(), self.original)
        for name, text in self.sources.items():
            self.assertEqual((self.bundle / name).read_bytes(), text.encode("utf-8"))
        self.assertEqual(self.catalog.source_sha, hashlib.sha256(self.original).hexdigest())

    def test_source_evidence_is_not_reported_as_compilation(self):
        self.assertEqual(self.catalog.status()["compilation"], "NOT_VERIFIED_BY_THIS_CATALOG")
        self.assertFalse(self.catalog.status()["physical_confirmation"])

    def test_all_pages_reconstruct_entire_lean_source(self):
        path, start, parts = "TGLExt/Identity.lean", 1, []
        while start is not None:
            page = self.catalog.read_file(path, start, 17)
            parts.append(page["text"])
            start = page["next_line"]
        self.assertEqual("\n".join(parts), self.sources[path].rstrip("\n"))

    def test_listing_pagination_omits_no_file(self):
        offset, found = 0, []
        while offset is not None:
            page = self.catalog.list_files(offset, 3)
            found.extend(record["path"] for record in page["files"])
            offset = page["next_offset"]
        self.assertEqual(found, sorted(self.sources))

    def test_search_locates_real_source_with_hash(self):
        result = self.catalog.search("identity_test")
        self.assertEqual(result["matching_files"], 1)
        self.assertIn("identity_test", result["results"][0]["excerpt"]["text"])
        self.assertEqual(result["results"][0]["path"], "TGL/Basic.lean")
        self.assertIn("NOT_A_PROOF", result["status"])

    def test_read_refuses_paths_outside_allowlist(self):
        for path in ["../.env", str(self.program), "TGL/../README.md", "not_found.lean"]:
            with self.subTest(path=path), self.assertRaises(kernel.KernelError):
                self.catalog.read_file(path)

    def test_changed_source_is_refused_at_read_and_reopen(self):
        (self.bundle / "TGL/Basic.lean").write_text("tampered", encoding="utf-8")
        with self.assertRaises(kernel.KernelError):
            self.catalog.read_file("TGL/Basic.lean")
        with self.assertRaises(kernel.KernelError):
            kernel.KernelCatalog(self.bundle)

    def test_dynamic_python_is_not_evaluated(self):
        with self.assertRaises(kernel.KernelError):
            kernel.extract_sources(b"_EMBEDDED_KERNEL_FILES = dict(secret=__import__('os').environ)")

    def test_duplicate_dictionary_keys_are_refused(self):
        with self.assertRaises(kernel.KernelError):
            kernel.extract_sources(b"_EMBEDDED_KERNEL_FILES = {'TGL.lean': 'one', 'TGL.lean': 'two'}")

    def test_bundle_path_traversal_is_refused_before_materialization(self):
        for bad in ["../escape.lean", "C:/escape.lean", "/escape.lean", "TGL\\escape.lean"]:
            with self.subTest(path=bad), self.assertRaises(kernel.KernelError):
                kernel.extract_sources(("_EMBEDDED_KERNEL_FILES = " + repr({**self.sources, bad: "x"})).encode())

    def test_existing_bundle_is_verified_not_rewritten(self):
        manifest_before = (self.bundle / "kernel_manifest.json").read_bytes()
        self.assertEqual(kernel.build_bundle(self.program, self.root / "bundles"), self.bundle)
        self.assertEqual((self.bundle / "kernel_manifest.json").read_bytes(), manifest_before)


if __name__ == "__main__":
    unittest.main()

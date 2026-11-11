"""Run on Windows with the installed app or staged canonical ACOM modules on PYTHONPATH."""
import hashlib
import io
import json
import lzma
import os
from pathlib import Path
import struct
import tempfile
import unittest
from unittest.mock import patch
import zlib

import archive_safe as adapter

arc = adapter.arc


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.package = self.base / "amostra.acom"
        self.out = self.base / "cópia restaurada"

    def set_archive(self, records, *, encrypted=False):
        header = {"v": 1, "format": "ACOM_ARCHIVE", "tool": "acom_archive", "enc": encrypted, "meta": {}}
        h = json.dumps(header).encode()
        stream = io.BytesIO(arc.MAGIC + struct.pack(">I", len(h)) + h)
        stream.seek(0, 2)
        entries, chain = [], hashlib.sha256()
        for index, (name, raw, method, blob, size) in enumerate(records):
            sha = hashlib.sha256(raw).hexdigest()
            chain.update(sha.encode())
            entries.append(dict(i=index, path=name, method=method, off=stream.tell(), len=len(blob),
                                size=size, enc=False, sha256=sha))
            stream.write(blob)
        start = stream.tell()
        meta = json.dumps(dict(entries=entries, meta_chain=chain.hexdigest(), count=len(entries))).encode()
        stream.write(meta + arc.MAGIC_END + struct.pack(">QI", start, len(meta)))
        self.package.write_bytes(stream.getvalue())

    def assert_rejects(self):
        with self.assertRaises((ValueError, OSError, lzma.LZMAError)):
            adapter.extract_archive(self.package, self.out)
        self.assertFalse(self.out.exists())
        self.assertFalse(list(self.base.glob(".iald-acom-*")))

    def test_complete_mixed_tree_and_empty_folders(self):
        source = self.base / "Dados do céu"
        (source / "vazia" / "fundo").mkdir(parents=True)
        (source / "星").mkdir()
        contents = {"星/medição.txt": "Um · ١".encode() * 2000, "ruído.bin": os.urandom(10083), "zero": b""}
        for name, data in contents.items():
            (source / name).write_bytes(data)
        sizes = adapter.pack_paths([source], self.package)
        restored = adapter.extract_archive(self.package, self.out)
        self.assertEqual(sizes, dict(files=3, inputBytes=sum(map(len, contents.values())),
                                     outputBytes=self.package.stat().st_size))
        self.assertEqual(restored["outputBytes"], sizes["inputBytes"])
        self.assertEqual(restored["inputBytes"], sizes["outputBytes"])
        for name, data in contents.items():
            self.assertEqual((source / name).read_bytes(), data)
            self.assertEqual((self.out / source.name / name).read_bytes(), data)
        self.assertTrue((self.out / source.name / "vazia" / "fundo").is_dir())
        self.assertEqual({name: raw for name, raw in arc.unpack_to_memory(self.package)},
                         {source.name + "/" + name: raw for name, raw in contents.items()})

    def test_direct_lossless_and_nested_legacy(self):
        data = (b"\0" * 6 + b"\1\2") * 9000
        blob, report = adapter.codec.compress_file(data, "ensaio.bin", backends=("bz2",))
        self.assertEqual(report.ontological_stage, "palette")
        self.package.write_bytes(blob)
        self.assertEqual(adapter.extract_archive(self.package, self.out)["outputBytes"], len(data))
        self.assertEqual((self.out / "ensaio.bin").read_bytes(), data)
        self.set_archive([("pasta/legado", data, "acom", blob, len(data))])
        self.out = self.base / "segundo"
        self.assertEqual(adapter.extract_archive(self.package, self.out)["files"], 1)
        self.assertEqual((self.out / "pasta" / "legado").read_bytes(), data)

    def test_canonical_archive_and_streaming_entry(self):
        payload = b"ar\n" * 23000
        raw, _ = arc.pack_files([("a/b", payload)])
        self.package.write_bytes(raw)
        adapter.extract_archive(self.package, self.out)
        self.assertEqual((self.out / "a" / "b").read_bytes(), payload)
        item = self.base / "item"
        item.write_bytes(os.urandom(2 * adapter.CHUNK + 3))
        with patch.object(adapter, "SMALL", 4096):
            result = adapter.pack_paths([item], self.base / "stream.acom")
        extract = adapter.extract_archive(self.base / "stream.acom", self.base / "stream-out")
        self.assertEqual(extract["outputBytes"], result["inputBytes"])
        self.assertEqual((self.base / "stream-out" / "item").read_bytes(), item.read_bytes())

    def test_unicode_alternating_zlib_chunks(self):
        data = (("Uma inscrição α" * 13).encode() + os.urandom(59)) * 6500
        self.set_archive([("深い.txt", data, "zlib", zlib.compress(data), len(data))])
        adapter.extract_archive(self.package, self.out)
        self.assertEqual((self.out / "深い.txt").read_bytes(), data)

    def test_integrity_failure_discards_entire_operation(self):
        self.set_archive([("a", b"first", "store", b"first", 5), ("b", b"x", "store", b"y", 1)])
        self.assert_rejects()

    def test_new_archive_detects_renamed_entry(self):
        item = self.base / "pasta-a.txt"
        item.write_bytes(b"conteudo")
        adapter.pack_paths([item], self.package)
        raw = self.package.read_bytes()
        self.assertEqual(raw.count(b"pasta-a.txt"), 1)
        self.package.write_bytes(raw.replace(b"pasta-a.txt", b"pasta-b.txt"))
        self.assert_rejects()

    def test_unsafe_paths_and_windows_aliases(self):
        for name in ("../evita", "C:/absoluto", "//server/share", "p\\q", "nul.txt", "a:b", "x. ", "p/PRN",
                     "meu/./x", "x//y", "firma/LONGNA~1.txt"):
            with self.subTest(name=name):
                self.set_archive([(name, b"x", "store", b"x", 1)])
                self.assert_rejects()
        for names in [("a", "A"), ("x", "x/y"), ("A/um", "a/dois")]:
            self.set_archive([(n, b"x", "store", b"x", 1) for n in names])
            self.assert_rejects()

    def test_caps_truncation_and_trailing_stream(self):
        raw = b"0" * 500
        for method, blob, claimed in [
                ("xz", lzma.compress(raw), 1), ("zlib", zlib.compress(raw)[:-1], len(raw)),
                ("zlib", zlib.compress(raw) + b"trailing", len(raw))]:
            self.set_archive([("a", raw, method, blob, claimed)])
            self.assert_rejects()
        self.set_archive([("a", raw, "xz", lzma.compress(raw), None)])
        with patch.object(adapter, "MAX_TOTAL", 20):
            self.assert_rejects()
        blob, _ = adapter.codec.compress_file(raw, "a", backends=("zlib",))
        header, compressed = adapter.codec._unpack(blob)
        header.update(orig_size=1, ontological_stage="identity")
        forged = adapter.codec._pack(header, compressed)
        self.set_archive([("a", raw, "acom", forged, 1)])
        self.assert_rejects()

    def test_encrypted_archive_rejected(self):
        self.set_archive([], encrypted=True)
        with self.assertRaisesRegex(ValueError, "senha"):
            adapter.extract_archive(self.package, self.out)
        self.assertFalse(self.out.exists())

    def test_never_overwrites_or_recurses(self):
        file = self.base / "unique.txt"
        file.write_bytes(b"original")
        self.package.write_bytes(b"existing")
        with self.assertRaises(FileExistsError):
            adapter.pack_paths([file], self.package)
        self.assertEqual(self.package.read_bytes(), b"existing")
        self.out.mkdir()
        (self.out / "original").write_bytes(b"original")
        with self.assertRaises(FileExistsError):
            adapter.extract_archive(self.package, self.out)
        self.assertEqual((self.out / "original").read_bytes(), b"original")
        with self.assertRaisesRegex(ValueError, "fora"):
            adapter.pack_paths([self.out], self.out / "recursive.acom")
        self.assertFalse((self.out / "recursive.acom").exists())


if __name__ == "__main__":
    unittest.main()

"""Lossless ACOM Archive v1 writer and resource-bounded Windows reader."""
from __future__ import annotations

import bz2
import hashlib
import io
import json
import lzma
import ntpath
import os
import re
import stat
import tempfile
import zlib
from contextlib import contextmanager
from pathlib import Path

import acom_archive as arc

codec = arc._codec
MIB = 1024 * 1024
MAX_MEMBER = 1024 * MIB
MAX_TOTAL = 4096 * MIB
MAX_ITEMS = 10000
MAX_MANIFEST = 12 * MIB
MAX_CONTAINER = MAX_TOTAL + 64 * MIB
MAX_DEPTH = 64
CHUNK = 256 * 1024
MAX_LZMA_MEMORY = 96 * MIB
SMALL = 8 * MIB


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _integer(value, upper):
    return type(value) is int and 0 <= value <= upper


def _relative(value):
    _require(isinstance(value, str) and 0 < len(value) <= 4096, "Comprimento de caminho inválido.")
    parts = value.split("/")
    _require(len(parts) <= MAX_DEPTH, "Árvore de pastas profunda demais.")
    for part in parts:
        _require(part not in ("", ".", "..") and len(part.encode("utf-16-le")) <= 510
                 and "\\" not in part and not ntpath.isreserved(part)
                 and not re.fullmatch(r"[^.]{0,6}~[0-9]+(?:\..*)?", part, re.I),
                 f"Nome de arquivo incompatível com Windows: {part!r}")
    return parts


class Names:
    def __init__(self):
        self.nodes = {}
        self.explicit = set()

    def add(self, name, *, folder=False):
        parts = _relative(name)
        for depth in range(1, len(parts) + 1):
            path = "/".join(parts[:depth])
            key = path.casefold()
            kind = folder or depth < len(parts)
            _require(key not in self.nodes or self.nodes[key] == (path, kind),
                     f"Colisão entre nomes ou tipos: {path}")
            self.nodes[key] = (path, kind)
        _require(key not in self.explicit, f"Entrada repetida: {name}")
        self.explicit.add(key)
        _require(len(self.nodes) <= MAX_ITEMS, "Limite de 10.000 arquivos e pastas excedido.")


def _absolute(path):
    s = str(path).replace("/", "\\")
    _require(not s.startswith(("\\\\?\\", "\\\\.\\")), "Caminho de dispositivo não aceito.")
    _require(".." not in Path(path).parts, "Caminho com componente '..'.")
    path = Path(path).absolute()
    for part in path.parts[1:]:
        _require(not ntpath.isreserved(part), f"Nome reservado no Windows: {part!r}")
    return path


def _regular_tree(path):
    for current in (*reversed(path.parents), path):
        info = current.lstat()
        _require(not stat.S_ISLNK(info.st_mode) and
                 not (getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT),
                 f"Link ou ponto de redirecionamento não aceito: {current.name}")
    return info


def _target(path):
    path = _absolute(path)
    _require(path != path.parent, "Escolha um nome de destino.")
    if os.path.lexists(path):
        raise FileExistsError(f"O destino já existe: {path.name}")
    _require(stat.S_ISDIR(_regular_tree(path.parent).st_mode), "A pasta de destino precisa existir.")
    return path


def _stamp(info):
    return (info.st_dev, info.st_ino, info.st_mode, info.st_size, info.st_mtime_ns)


class _FixedReader:
    def __init__(self, fp, size):
        self.fp, self.left = fp, size

    def read(self, n=-1):
        if self.left == 0:
            _require(not self.fp.read(1), "O arquivo cresceu durante a compactação.")
            return b""
        n = self.left if n < 0 else min(n, self.left)
        data = self.fp.read(n)
        _require(len(data) == n, "O arquivo mudou durante a leitura.")
        self.left -= len(data)
        return data


@contextmanager
def _open_source(path, original):
    _require(_stamp(_regular_tree(path)) == original, "A origem mudou.")
    with path.open("rb") as fp:
        _require(_stamp(os.fstat(fp.fileno())) == original, "A origem mudou.")
        yield _FixedReader(fp, original[3])
        _require(_stamp(os.fstat(fp.fileno())) == original, "A origem mudou.")


def _scan(paths, target):
    files, dirs, empty = [], [], []
    names = Names()
    total = 0

    def walk(path, rel):
        nonlocal total
        info = _regular_tree(path)
        is_dir = stat.S_ISDIR(info.st_mode)
        names.add(rel, folder=is_dir)
        if is_dir:
            _require(not target.is_relative_to(path), "Escolha um destino fora da pasta de origem.")
            dirs.append((path, _stamp(info)))
            found = False
            for child in path.iterdir():
                found = True
                walk(child, rel + "/" + child.name)
            if not found:
                empty.append(rel)
        else:
            _require(stat.S_ISREG(info.st_mode), "Somente arquivos e pastas comuns são aceitos.")
            _require(info.st_size <= MAX_MEMBER, "Arquivo excede 1 GiB nesta edição.")
            total += info.st_size
            _require(total <= MAX_TOTAL, "A seleção excede 4 GiB nesta edição.")
            files.append((rel, path, _stamp(info)))

    roots = [_absolute(p) for p in paths]
    _require(0 < len(roots) <= MAX_ITEMS, "Selecione arquivos ou uma pasta.")
    for path in roots:
        _require(path.name and path != path.parent, "Selecione uma pasta dentro da unidade.")
        walk(path, path.name)
    return sorted(files), dirs, sorted(empty), total


def _commit(staged, target):
    _target(target)
    # Windows MoveFileW, used by os.rename, never replaces an existing destination.
    if os.name != "nt":
        raise OSError("Esta edição do adaptador é destinada ao Windows.")
    staged.rename(target)


def _layout_hash(names, empty):
    layout = json.dumps([list(names), empty], ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(layout.encode("utf-8")).hexdigest()


def pack_paths(paths: list[Path], output: Path) -> dict:
    output = _target(output)
    files, dirs, empty, total = _scan(paths, output)
    def entries():
        for rel, path, stamp in files:
            opener = lambda p=path, s=stamp: _open_source(p, s)
            # Canonical v1 streams when size is omitted. Avoid extreme LZMA allocations for large inputs.
            yield rel, opener, stamp[3] if stamp[3] <= SMALL else None
    with tempfile.TemporaryDirectory(prefix=".iald-acom-", dir=output.parent) as tmp:
        pending = Path(tmp) / "package"
        with pending.open("x+b") as fp:
            arc.pack_stream(entries(), fp, meta={"empty_dirs": empty,
                            "layout_sha256": _layout_hash((row[0] for row in files), empty)})
            fp.flush()
            os.fsync(fp.fileno())
            size = fp.tell()
            _archive_plan(fp, size)
        for path, original in dirs:
            _require(_stamp(_regular_tree(path)) == original, "A pasta de origem mudou.")
        _commit(pending, output)
    return {"files": len(files), "inputBytes": total, "outputBytes": size}


def _read(fp, length):
    data = fp.read(length)
    _require(len(data) == length, "Arquivo ACOM truncado.")
    return data


def _archive_plan(fp, size):
    header = arc._read_header(fp)
    first = fp.tell()
    _require(isinstance(header, dict) and header.get("format") == "ACOM_ARCHIVE"
             and type(header.get("v")) is int and header["v"] == 1,
             "Versão de arquivo ACOM incompatível.")
    _require(header.get("enc") is False, "Esta edição abre pacotes ACOM sem senha.")
    meta = header.get("meta", {})
    _require(isinstance(meta, dict), "Metadados ACOM inválidos.")
    empty = meta.get("empty_dirs", [])
    _require(isinstance(empty, list) and len(empty) <= MAX_ITEMS, "Lista de pastas inválida.")
    names = Names()
    for name in empty:
        names.add(name, folder=True)
    start, length = arc._read_footer(fp)
    _require(length <= MAX_MANIFEST and first <= start and start + length + arc.FOOTER_LEN == size,
             "Limites do manifesto ACOM inválidos.")
    fp.seek(start)
    manifest = json.loads(_read(fp, length).decode("utf-8"))
    _require(isinstance(manifest, dict), "Manifesto inválido.")
    records = manifest.get("entries")
    _require(isinstance(records, list) and len(records) <= MAX_ITEMS
             and _integer(manifest.get("count"), MAX_ITEMS) and manifest["count"] == len(records),
             "Contagem de arquivos inválida.")
    offset, total, chain = first, 0, hashlib.sha256()
    for index, entry in enumerate(records):
        _require(isinstance(entry, dict), "Entrada inválida.")
        names.add(entry.get("path"))
        original, stored = entry.get("size"), entry.get("len")
        method = entry.get("method")
        _require(_integer(stored, MAX_MEMBER + 4*MIB) and _integer(entry.get("off"), start)
                 and entry["off"] == offset and offset + stored <= start
                 and _integer(entry.get("i"), MAX_ITEMS) and entry["i"] == index
                 and entry.get("enc") is False and method in ("store", "zlib", "xz", "acom"),
                 "Posição ou método de um registro inválido.")
        _require((original is None and method == "xz") or _integer(original, MAX_MEMBER),
                 "Tamanho de arquivo inválido ou acima de 1 GiB.")
        if original is not None:
            _require(original <= _budget(stored), "Expansão declarada excede o limite.")
            total += original
        _require(total <= MAX_TOTAL, "Conteúdo restaurado excede 4 GiB.")
        digest = entry.get("sha256")
        _require(isinstance(digest, str) and re.fullmatch("[0-9a-f]{64}", digest), "SHA-256 inválido.")
        chain.update(digest.encode("ascii"))
        offset += stored
    _require(offset == start and chain.hexdigest() == manifest.get("meta_chain"),
             "Cadeia de integridade do arquivo ACOM divergente.")
    if "layout_sha256" in meta:
        _require(meta["layout_sha256"] == _layout_hash((row["path"] for row in records), empty),
                 "Conferência de nomes e pastas divergente.")
    return records, empty


def _budget(compressed):
    return min(MAX_MEMBER, max(16 * MIB, compressed * 32768))


def _inflate(fp, amount, method, limit, write):
    """Checksum, EOF and exact record boundaries are enforced by the caller and here."""
    count = 0
    if method == "store":
        _require(amount <= limit, "Conteúdo excede o teto de restauração.")
        while amount:
            data = _read(fp, min(CHUNK, amount))
            write(data)
            count += len(data)
            amount -= len(data)
        return count
    engines = {"xz": lambda: lzma.LZMADecompressor(format=lzma.FORMAT_XZ, memlimit=MAX_LZMA_MEMORY),
               "zlib": zlib.decompressobj, "bz2": bz2.BZ2Decompressor}
    _require(method in engines, "Codec de compressão desconhecido.")
    decoder = engines[method]()
    pending = b""
    while not decoder.eof:
        needs_input = not pending if method == "zlib" else decoder.needs_input
        if needs_input:
            _require(amount > 0, "Fluxo compactado truncado.")
            pending = _read(fp, min(CHUNK, amount))
            amount -= len(pending)
        allowed = min(CHUNK, limit - count + 1)
        data = decoder.decompress(pending, allowed)
        count += len(data)
        _require(count <= limit, "Conteúdo excede o teto de restauração.")
        write(data)
        pending = decoder.unconsumed_tail if method == "zlib" else b""
    _require(not amount and not decoder.unused_data, "Dados adicionais após o fim do fluxo.")
    return count


def _single(fp, length, max_output, expected=None):
    _require(length <= codec.MAX_INPUT_BYTES + codec.MAX_HEADER_BYTES + 1024, "Contêiner individual grande demais.")
    header, payload = codec._unpack(_read(fp, length))
    _require(isinstance(header, dict) and header.get("codec") == "ACOM-LOSSLESS"
             and header.get("version") == codec.CODEC_VERSION,
             "Esta edição restaura apenas ACOM Archive v1 e ACOM-LOSSLESS 1.0.")
    original = header.get("orig_size")
    _require(_integer(original, min(max_output, codec.MAX_INPUT_BYTES, _budget(len(payload))))
             and (expected is None or original == expected), "Tamanho do arquivo ACOM individual inválido.")
    stage = header.get("ontological_stage", "identity")
    _require(stage in ("identity", "palette"), "Transformação ACOM desconhecida.")
    staged_limit = original if stage == "identity" else (original + 1) // 2
    method = {"stored": "store", "lzma": "xz", "bz2": "bz2", "zlib": "zlib"}.get(header.get("backend"))
    data = io.BytesIO()
    n = _inflate(io.BytesIO(payload), len(payload), method, staged_limit, data.write)
    _require(n == staged_limit, "Tamanho intermediário divergente.")
    raw = data.getvalue()
    if stage == "palette":
        meta = header.get("palette_meta")
        _require(isinstance(meta, dict) and _integer(meta.get("n"), original) and meta["n"] == original,
                 "Tamanho da paleta divergente.")
        raw = codec._palette_decode(raw, meta)
    _require(hashlib.sha256(raw).hexdigest() == header.get("orig_sha256"), "SHA-256 do arquivo divergente.")
    name = header.get("orig_name")
    _require(len(_relative(name)) == 1, "Nome do arquivo individual inválido.")
    return name, raw


def _extract_members(fp, size, folder):
    records, empty = _archive_plan(fp, size)
    for name in empty:
        (folder / name).mkdir(parents=True)
    total = 0
    for entry in records:
        target = folder / entry["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        stored, expected = entry["len"], entry["size"]
        limit = min(MAX_TOTAL - total, _budget(stored), MAX_MEMBER if expected is None else expected)
        fp.seek(entry["off"])
        digest = hashlib.sha256()
        with target.open("xb") as dst:
            def save(data):
                dst.write(data)
                digest.update(data)
            if entry["method"] == "acom":
                _, data = _single(fp, stored, limit, expected)
                save(data)
                n = len(data)
            else:
                n = _inflate(fp, stored, entry["method"], limit, save)
        _require((expected is None or n == expected) and digest.hexdigest() == entry["sha256"],
                 f"Falha de integridade: {entry['path']}")
        total += n
    return len(records), total


def extract_archive(archive: Path, output: Path) -> dict:
    output = _target(output)
    archive = _absolute(archive)
    info = _regular_tree(archive)
    _require(stat.S_ISREG(info.st_mode) and info.st_size <= MAX_CONTAINER,
             "Arquivo de entrada inválido ou acima do limite de teste.")
    with archive.open("rb") as fp, tempfile.TemporaryDirectory(prefix=".iald-acom-", dir=output.parent) as temp:
        _require(_stamp(os.fstat(fp.fileno())) == _stamp(info), "O pacote selecionado mudou.")
        folder = Path(temp) / "restored"
        folder.mkdir()
        magic = fp.read(len(arc.MAGIC))
        fp.seek(0)
        if magic == arc.MAGIC:
            files, total = _extract_members(fp, info.st_size, folder)
        elif magic.startswith(codec.MAGIC):
            name, raw = _single(fp, info.st_size, MAX_TOTAL)
            with (folder / name).open("xb") as dst:
                dst.write(raw)
            files, total = 1, len(raw)
        else:
            raise ValueError("Formato ACOM não reconhecido.")
        _require(_stamp(os.fstat(fp.fileno())) == _stamp(info), "O pacote mudou durante a restauração.")
        _commit(folder, output)
    return {"files": files, "inputBytes": info.st_size, "outputBytes": total}

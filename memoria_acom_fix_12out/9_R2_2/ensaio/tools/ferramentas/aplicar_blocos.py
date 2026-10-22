"""D5 (12/10/2026): substitui o bloco ACOM do topo dos arquivos de instrução pelo texto novo.

Por arquivo: (1) localiza o bloco atual pelo MARCADOR no topo e pelo sha16 dos seus bytes (CAS:
sha16 fora do conjunto esperado aborta esse arquivo, sem tocar nada); (2) grava backup de BYTES
`<arquivo>.bak_<AAAAMMDD_HHMMSS_us>` e confere; (3) novo = BLOCO_NOVO (LF ou CRLF, conforme o
arquivo) + bytes após o bloco antigo, com a linha de registro «bloco anterior (N B, sha16 …)
substituído em 12/10/2026 por ordem do operador (…)» calculada do artefato; tempário → conferência
→ os.replace; (4) pós-conferência byte a byte do restante; (5) recibo JSON.

`--memory-md`: substitui SÓ a linha `- Memória ACOM: …` (única) e exige ≤ 200 linhas e ≤ 24.000 B,
senão restaura do backup e aborta. `--dry-run` não escreve nada. Hash jamais de memória: o sha16
do bloco, do arquivo e da ordem do operador são lidos dos bytes por este script.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Pares de marcadores do bloco ANTIGO: o instalado no topo dos cinco arquivos (COMMON_ACOM_SESSION_ENTRY)
# e o do próprio SESSION_BRIDGE.md (SHARED_MEMORY_SESSION_BRIDGE), ambos de 10/10/2026.
OLD_MARKERS = (
    (b"<!-- IALD_COMMON_ACOM_SESSION_ENTRY_20261010 -->", b"<!-- END_IALD_COMMON_ACOM_SESSION_ENTRY_20261010 -->"),
    (b"<!-- IALD_SHARED_MEMORY_SESSION_BRIDGE_20261010 -->", b"<!-- END_IALD_SHARED_MEMORY_SESSION_BRIDGE_20261010 -->"),
)
OLD_START, OLD_END = OLD_MARKERS[0]
NEW_START = b"<!-- IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012 -->"
NEW_END = b"<!-- END_IALD_SHARED_MEMORY_SESSION_BRIDGE_20261012 -->"
# Blocos antigos conhecidos [REAL, medidos em ORIGINAIS.json desta frente e no diagnóstico de 12/10]:
# 620 B LF (CLAUDE.md global, AGENTS.md, README do quadro, COORDINATOR.md), 624 B CRLF (CLAUDE.md da
# IALD Nativa) e o SESSION_BRIDGE.md inteiro (887 B). O CAS exige que o sha16 medido esteja aqui.
EXPECTED_OLD_SHA16 = {"3106d7234c7a3b71", "2ca1cb060ecd2119", "49f1626d52d9cd6c"}
ORDEM_DEFAULT = Path(r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt")
ORDEM_SHA16_ESPERADO = "78ef70e6f9868281"
ORDEM_TEXTO = "resolva a questão da memória"
DATA_SUBSTITUICAO = "12/10/2026"
MEMORY_LINE_PREFIX = b"- Mem\xc3\xb3ria ACOM:"
MEMORY_LINE_NEW = ("- Memória ACOM: `C:\\IALD\\MEMORIA_IALD\\README.md` + `SESSION_BRIDGE.md` (12/10: delta + diário + "
                   "instantâneos; `project` ao abrir e após compactação; `transition` só em etapa material). Diário: MEMORY_2.md.")
MEMORY_MAX_LINES = 200
MEMORY_MAX_BYTES = 24000


class BlocoError(RuntimeError):
    pass


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def stamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S_%f")


def bloco_novo_base(bridge_path):
    """Texto genérico do bloco (SESSION_BRIDGE_v2.md), em LF, sem a linha de registro."""
    raw = Path(bridge_path).read_bytes().replace(b"\r\n", b"\n")
    if not raw.startswith(NEW_START + b"\n") or not raw.rstrip(b"\n").endswith(NEW_END):
        raise BlocoError("SESSION_BRIDGE_v2.md sem os marcadores do bloco novo")
    return raw if raw.endswith(b"\n") else raw + b"\n"


def ordem_sha16(ordem_path):
    data = Path(ordem_path).read_bytes()
    digest = sha256(data)[:16]
    first = data.decode("utf-8").splitlines()[0].strip()
    if digest != ORDEM_SHA16_ESPERADO or first != ORDEM_TEXTO:
        raise BlocoError("ordem do operador divergente: sha16 %s, linha 1 %r" % (digest, first))
    return digest


def localizar_bloco_antigo(old):
    """Bloco no topo: do marcador inicial ao marcador END + fim de linha, MAIS a linha em branco que o
    segue (é assim que o bloco instalado mede 620 B LF / 624 B CRLF). Devolve (bloco, nl, tem_branco)."""
    for start, end_marker in OLD_MARKERS:
        if old.startswith(start + b"\r\n"):
            nl = b"\r\n"
        elif old.startswith(start + b"\n"):
            nl = b"\n"
        else:
            continue
        end = old.find(end_marker + nl)
        if end < 0:
            raise BlocoError("marcador END do bloco ACOM ausente")
        stop = end + len(end_marker) + len(nl)
        blank = old[stop: stop + len(nl)] == nl
        if blank:
            stop += len(nl)
        return old[:stop], nl, blank
    raise BlocoError("marcador do bloco ACOM ausente no topo")


def montar_bloco_novo(base_lf, nl, old_block, ordem_digest, blank=True):
    linhas = base_lf.rstrip(b"\n").split(b"\n")
    if linhas[-1] != NEW_END:
        raise BlocoError("bloco novo sem marcador END na última linha")
    registro = ("<!-- bloco anterior (%d B, sha16 %s) substituído em %s por ordem do operador («%s», sha16 %s) -->"
                % (len(old_block), sha256(old_block)[:16], DATA_SUBSTITUICAO, ORDEM_TEXTO, ordem_digest)).encode("utf-8")
    corpo = linhas[:-1] + [registro, NEW_END]
    return nl.join(corpo) + nl + (nl if blank else b"")


def escrever_com_backup(path, old, new, dry_run):
    backup = path.with_name(path.name + ".bak_" + stamp())
    if dry_run:
        return backup, None
    with backup.open("xb") as out:
        out.write(old)
        out.flush()
        os.fsync(out.fileno())
    if backup.read_bytes() != old:
        raise BlocoError("backup divergente: " + str(backup))
    temp = path.with_name(path.name + ".tmp_" + stamp())
    with temp.open("xb") as out:
        out.write(new)
        out.flush()
        os.fsync(out.fileno())
    if temp.read_bytes() != new:
        temp.unlink()
        raise BlocoError("tempário divergente: " + str(temp))
    if path.read_bytes() != old:
        temp.unlink()
        raise BlocoError("arquivo mudou durante a operação: " + str(path))
    try:
        os.replace(temp, path)
    except OSError:
        # R2 (13/10): a troca falhou (alvo somente-leitura/preso): o tempário criado aqui sai; o alvo fica como estava
        temp.unlink()
        raise
    if path.read_bytes() != new:
        raise BlocoError("conferência final divergente: " + str(path))
    return backup, sha256(new)


def aplicar_arquivo(path, base_lf, ordem_digest, dry_run=False, expected=EXPECTED_OLD_SHA16):
    path = Path(path)
    old = path.read_bytes()
    old_sha = sha256(old)
    old_block, nl, blank = localizar_bloco_antigo(old)
    block_sha16 = sha256(old_block)[:16]
    if block_sha16 not in expected:
        raise BlocoError("CAS: bloco antigo com sha16 %s (%d B) fora do esperado %s" % (block_sha16, len(old_block), sorted(expected)))
    new_block = montar_bloco_novo(base_lf, nl, old_block, ordem_digest, blank)
    new = new_block + old[len(old_block):]
    if new[len(new_block):] != old[len(old_block):]:
        raise BlocoError("o restante do arquivo mudaria")  # impossível por construção; conferido mesmo assim
    backup, new_sha = escrever_com_backup(path, old, new, dry_run)
    if not dry_run and path.read_bytes()[len(new_block):] != old[len(old_block):]:
        raise BlocoError("pós-conferência do restante falhou: " + str(path))
    return {"file": str(path), "dry_run": dry_run, "line_ending": "CRLF" if nl == b"\r\n" else "LF",
            "old_sha256": old_sha, "new_sha256": new_sha, "old_bytes": len(old), "new_bytes": len(new),
            "block_old_bytes": len(old_block), "block_old_sha16": block_sha16,
            "block_new_bytes": len(new_block), "block_new_sha16": sha256(new_block)[:16],
            "rest_bytes": len(old) - len(old_block), "rest_unchanged": True, "backup": str(backup)}


def aplicar_memory_md(path, dry_run=False):
    path = Path(path)
    old = path.read_bytes()
    old_sha = sha256(old)
    nl = b"\r\n" if b"\r\n" in old else b"\n"
    lines = old.split(nl)
    hits = [i for i, line in enumerate(lines) if line.startswith(MEMORY_LINE_PREFIX)]
    if len(hits) != 1:
        raise BlocoError("MEMORY.md: esperada exatamente 1 linha '- Memória ACOM:', encontradas %d" % len(hits))
    index = hits[0]
    old_line = lines[index]
    lines[index] = MEMORY_LINE_NEW.encode("utf-8")
    new = nl.join(lines)
    n_lines = new.count(b"\n") + (0 if new.endswith(b"\n") else 1)
    if n_lines > MEMORY_MAX_LINES or len(new) > MEMORY_MAX_BYTES:
        raise BlocoError("MEMORY.md ultrapassaria o limite: %d linhas, %d B" % (n_lines, len(new)))
    backup, new_sha = escrever_com_backup(path, old, new, dry_run)
    if not dry_run:
        check = path.read_bytes()
        c_lines = check.count(b"\n") + (0 if check.endswith(b"\n") else 1)
        if c_lines > MEMORY_MAX_LINES or len(check) > MEMORY_MAX_BYTES:  # restaura e aborta
            os.replace(backup, path)
            raise BlocoError("MEMORY.md fora do limite após escrita; restaurado do backup")
    return {"file": str(path), "dry_run": dry_run, "old_sha256": old_sha, "new_sha256": new_sha,
            "line_index": index + 1, "old_line_sha16": sha256(old_line)[:16], "new_line": MEMORY_LINE_NEW,
            "lines": n_lines, "bytes": len(new), "backup": str(backup)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--alvo", action="append", default=[], help="arquivo com o bloco ACOM no topo (repetível)")
    parser.add_argument("--memory-md", default=None, help="MEMORY.md da Central: troca só a linha '- Memória ACOM:'")
    parser.add_argument("--bridge", default=str(HERE / "SESSION_BRIDGE_v2.md"))
    parser.add_argument("--ordem", default=str(ORDEM_DEFAULT))
    parser.add_argument("--recibo", default=None, help="caminho do BLOCOS_RECIBO.json (padrão: ao lado do script)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    base_lf = bloco_novo_base(args.bridge)
    ordem_digest = ordem_sha16(args.ordem)
    recibo = {"at": datetime.now(timezone.utc).isoformat(), "script": str(Path(__file__).resolve()),
              "script_sha256": sha256(Path(__file__).read_bytes()), "bridge": str(Path(args.bridge).resolve()),
              "bridge_sha256": sha256(Path(args.bridge).read_bytes()), "ordem": str(Path(args.ordem).resolve()),
              "ordem_sha16": ordem_digest, "dry_run": args.dry_run, "arquivos": [], "memory_md": None, "falhas": []}
    status = 0
    for alvo in args.alvo:
        try:
            recibo["arquivos"].append(aplicar_arquivo(alvo, base_lf, ordem_digest, args.dry_run))
        except (BlocoError, OSError, UnicodeError) as exc:
            recibo["falhas"].append({"file": str(alvo), "error": type(exc).__name__, "message": str(exc)})
            status = 2
    if args.memory_md:
        try:
            recibo["memory_md"] = aplicar_memory_md(args.memory_md, args.dry_run)
        except (BlocoError, OSError, UnicodeError) as exc:
            recibo["falhas"].append({"file": str(args.memory_md), "error": type(exc).__name__, "message": str(exc)})
            status = 2
    out = Path(args.recibo) if args.recibo else HERE / "BLOCOS_RECIBO.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(recibo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": status == 0, "aplicados": len(recibo["arquivos"]), "memory_md": bool(recibo["memory_md"]),
                      "falhas": recibo["falhas"], "recibo": str(out)}, ensure_ascii=False))
    return status


if __name__ == "__main__":
    sys.exit(main())

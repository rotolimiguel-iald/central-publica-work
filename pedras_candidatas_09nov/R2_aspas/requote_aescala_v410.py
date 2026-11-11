# -*- coding: utf-8 -*-
"""Gerência c1, 09/11/2026 (D91): na pedra AEscala, as aspas angulares ficam SÓ onde o trecho é fala VERBATIM do operador (conferida por
script contra os arquivos work/cunhagens_13out/OPERADOR_*.txt; reticências internas toleradas, cada pedaço tem de estar no acervo); todo
outro trecho entre aspas angulares (paráfrase, rótulo, tipografia alterada, citação de docstring do kernel, frase da gerência) passa a aspas
tipográficas. Só os dois caracteres delimitadores mudam; nenhum texto interno, nenhuma prova, nenhum nome. Acrescenta UMA linha de convenção
ao cabeçalho, antes da linha «[TGLExt».
uso: python requote_aescala_v410.py <entrada.lean> <saida.lean> [--so-medir]"""
import hashlib, re, sys
from pathlib import Path
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
corpus = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in sorted(CUN.glob("OPERADOR_*.txt")))
def norm(s): return re.sub(r"\s+", " ", s).strip().lower()
NC = norm(corpus)
def verbatim(q):
    n = norm(q).rstrip(".,;: ")
    parts = [x.strip(" .,;:") for x in re.split(r"…|\[\.\.\.\]|\.\.\.", n) if x.strip(" .,;:")]
    return bool(parts) and all(pt in NC for pt in parts)
src_p, out_p = Path(sys.argv[1]), Path(sys.argv[2]); so_medir = "--so-medir" in sys.argv
b = src_p.read_bytes(); crlf = b"\r\n" in b; src = b.decode("utf-8")
RX = re.compile("\u00ab([^\u00bb]{1,400})\u00bb")
trocas = []
def sub(m):
    q = m.group(1)
    if verbatim(q): return m.group(0)
    trocas.append(q); return "\u201c" + q + "\u201d"
novo = RX.sub(sub, src)
NOTA = "  [Convenção das aspas (gerência c1, 09/11/2026, D91): as aspas angulares marcam SÓ fala verbatim do operador, conferida por script contra os arquivos de fala; as aspas tipográficas marcam paráfrase, rótulo, tipografia normalizada ou citação de docstring do kernel.]"
nl = (chr(13) + chr(10)) if crlf else chr(10)
if "Convenção das aspas" not in novo:
    Ls = novo.split(nl); k = [i for i, l in enumerate(Ls) if l.startswith("  [TGLExt")]; assert len(k) >= 1, "sem a linha [TGLExt do cabeçalho"
    Ls.insert(k[0], NOTA); novo = nl.join(Ls)
restam = [q for q in RX.findall(novo) if not verbatim(q)]
print("entrada", src_p.name, len(b), "B sha16", hashlib.sha256(b).hexdigest()[:16], "| crlf:", crlf, "| trocas:", len(trocas), "| angulares restantes:", len(RX.findall(novo)), "| não verbatim restantes:", len(restam))
if "--listar" in sys.argv:
    for q in trocas: print("   ", re.sub(r"\s+", " ", q)[:110])
assert not restam, restam
if not so_medir:
    nb = novo.encode("utf-8"); out_p.write_bytes(nb); print("saída", out_p.name, len(nb), "B sha256", hashlib.sha256(nb).hexdigest())
    lim = lambda s: re.sub(r"\s+", " ", s.replace("\u00ab", "").replace("\u00bb", "").replace("\u201c", "").replace("\u201d", ""))
    print("texto idêntico fora das aspas e da nota:", lim(src) == lim(novo.replace(NOTA, "")))

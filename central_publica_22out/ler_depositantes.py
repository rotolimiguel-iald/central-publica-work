# -*- coding: utf-8 -*-
"""SÓ LEITURA: o DEPOSITANTE de cada pedido, lido dos próprios formulários de depósito do INPI (texto extraído em vault/normalized_docs e,
se preciso, os PDFs dentro do zip «Acervos de Patentes INPI.zip»): número do processo, nome ou razão social, tipo de pessoa. Saída só local
(o nome do depositante é público no pedido; CPF/CNPJ não são impressos)."""
import io, json, re, sys, zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
import logging
logging.disable(logging.CRITICAL)
from pypdf import PdfReader

SRC = Path(r"C:\IALD\Central de Patentes")
PROC = re.compile(r"N[úu]mero do Processo:\s*(BR\s*\d{2}\s*\d{4}\s*\d{6}\s*\d)")
DEP = re.compile(r"Dados do Depositante.*?Nome ou Raz[ãa]o Social:\s*([^\n]+)\n.*?Tipo de Pessoa:\s*([^\n]+)", re.S)
INV = re.compile(r"Dados do Inventor.*?Nome:\s*([^\n]+)", re.S)
achados = {}


def ler(t, origem):
    for m in PROC.finditer(t):
        proc = re.sub(r"\s+", "", m.group(1))
        trecho = t[m.end(): m.end() + 4000]
        d = DEP.search(trecho)
        i = INV.search(t[m.end(): m.end() + 20000])
        if d:
            achados.setdefault(proc, set()).add((d.group(1).strip(), d.group(2).strip(), (i.group(1).strip() if i else "?"), origem))


for p in (SRC / "vault" / "normalized_docs").rglob("*.txt"):
    t = p.read_text(encoding="utf-8", errors="replace")
    if "Dados do Depositante" in t:
        ler(t, p.name[:70])
z = SRC / "Patentes" / "Acervo de Patentes" / "Acervos de Patentes INPI.zip"
if z.is_file():
    zz = zipfile.ZipFile(z)
    for n in zz.namelist():
        if n.lower().endswith(".pdf"):
            r = PdfReader(io.BytesIO(zz.read(n)))
            ler(" \n".join((pg.extract_text() or "") for pg in r.pages[:6]), "zip:" + n[:60])
for proc in sorted(achados):
    for nome, tipo, inv, origem in sorted(achados[proc]):
        print(proc, "| depositante:", nome, "|", tipo, "| inventor:", inv, "|", origem)
print("processos com depositante lido:", len(achados))

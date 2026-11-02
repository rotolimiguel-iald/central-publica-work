# -*- coding: utf-8 -*-
"""Patch de G1 (gerencia c1, 02/11/2026, custodia v405, G1 parado): a cadeia de selo vai ao cofre sem os estados superados.
Medido: sem as pastas antes_* e os .bak_, a v405 tem 451 arquivos, o mesmo numero do cofre da v404; o excesso (1057) eram os estados das rodadas de errata R1-R7. Eles ficam em work, ditos no manifesto. A guarda de 50% nao muda."""
import datetime, os, py_compile
from pathlib import Path

TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_c1"
p = Path("C:/IALD/Central de Patentes/tools/custodia_g1/central.py")
E = [
 ('kb_stub|pilar_anterior|quarentena|tentativa|exame_preflight$', 'kb_stub|pilar_anterior|quarentena|tentativa|antes_de_|antes_da_errata_|exame_preflight$'),
 ('"regra": "cópia de bytes dos arquivos de primeiro nível e das subpastas de registro; FORA: ensaios a seco, simulações, bases, tentativas, rascunhos, árvores "\n',
  '"regra": "cópia de bytes dos arquivos de primeiro nível e das subpastas de registro; FORA: ensaios a seco, simulações, bases, tentativas, estados superados (pastas antes_* e arquivos .bak_), rascunhos, árvores "\n'),
 ('                fs = fora_sub.setdefault("copias_de_teste_e_caminhos_longos", [0, 0]); fs[0] += 1; fs[1] += p.stat().st_size\n                continue\n',
  '                fs = fora_sub.setdefault("copias_de_teste_e_caminhos_longos", [0, 0]); fs[0] += 1; fs[1] += p.stat().st_size\n                continue\n'
  '            if ".bak_" in rel.name:      # 02/11/2026 (v405): backups das rodadas de errata; ficam em work e entram na lista negra do commit da Central\n'
  '                fs = fora_sub.setdefault("estados_superados_bak", [0, 0]); fs[0] += 1; fs[1] += p.stat().st_size\n                continue\n'),
]
b = p.read_bytes()
t = b.decode("utf-8")
crlf = "\r\n" in t
assert not crlf or t.count("\n") == t.count("\r\n"), "fim de linha misto"
for old, new in E:
    if crlf:
        old, new = old.replace("\n", "\r\n"), new.replace("\n", "\r\n")
    assert t.count(old) == 1, (old[:70], t.count(old))
    t = t.replace(old, new)
nb = t.encode("utf-8")
bak = p.with_name(p.name + ".bak_" + TS)
with open(bak, "xb") as f:
    f.write(b)
assert bak.read_bytes() == b
tmp = p.with_name(p.name + ".tmp_" + TS)
with open(tmp, "xb") as f:
    f.write(nb)
py_compile.compile(str(tmp), cfile=str(tmp) + ".pyc", doraise=True)
os.remove(str(tmp) + ".pyc")
os.replace(tmp, p)
print("ok", p.name, len(b), "->", len(nb), "crlf", crlf)
V = Path("C:/IALD/Central de Patentes/vault/originals_copy/um_unificado_v405")
assert V.is_dir() and not (V / "CUSTODY_MANIFEST.json").exists()
K = V.with_name("tgl_kernel_v405")
assert not K.exists()
novo = V.with_name("um_unificado_v405.PARCIAL_" + TS[:15])
os.rename(V, novo)
print("cofre parcial renomeado:", novo.name, "|", sum(1 for x in novo.rglob("*") if x.is_file()), "arquivos")

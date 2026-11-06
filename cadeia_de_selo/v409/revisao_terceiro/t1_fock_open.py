# -*- coding: utf-8 -*-
"""Revisor v409: frases (separadas por ponto-e-virgula/ponto seguido de espaco/quebra) que juntam 'Fock' e [OPEN]/em aberto, nos textos novos (fontes) e nos rendidos (harness, artigo do ensaio, md)."""
import glob, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
fontes = [R + f for f in ("artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "runtime_v409.py", "delta_v409.py", "pos_rito/textos_v409_novo.pysnip", "pos_rito/textos_v409.py", "pos_rito/textos_custodia_handoff_v409.py", "pos_rito/CUSTODIA_v409_RASCUNHO.txt")]
fontes += sorted(glob.glob(R + "pedra/*.lean")) + sorted(glob.glob("C:/t/h409/harness_saida_v409/textos/*.txt")) + [R + "dry_v409/dry_v409_pt.txt", R + "dry_v409/dry_v409_en.txt", R + "dry_v409/um_absoluto_forma_canonica.md"]
ruim = re.compile(r"\[OPEN\]|em\s+aberto|segue\s+aberto|remains\s+open|stays\s+open|is\s+open", re.I)
res = {}
for a in fontes:
    if not os.path.exists(a): continue
    t = open(a, encoding="utf-8", errors="replace").read()
    for fr in re.split(r"(?<=[.;])\s+|\n", t):
        if re.search(r"Fock", fr) and ruim.search(fr):
            # recorta ao redor de Fock
            m = re.search(r"Fock", fr)
            res.setdefault(fr.strip()[:260], set()).add(os.path.relpath(a, R) if a.startswith(R) else os.path.basename(a))
print("frases distintas com Fock + OPEN/aberto:", len(res))
for fr, fs in sorted(res.items(), key=lambda x: sorted(x[1])[0]):
    print(" -", sorted(fs)[:4], "|", fr)
json.dump({k: sorted(v) for k, v in res.items()}, open(R + "revisao_terceiro/t1_fock_open_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

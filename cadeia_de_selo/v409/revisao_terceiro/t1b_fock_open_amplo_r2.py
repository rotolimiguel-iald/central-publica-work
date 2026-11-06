# -*- coding: utf-8 -*-
"""Revisor v409 R2: varredura AMPLA: 'Fock'/'uniforme' perto da palavra OPEN (com ou sem colchetes), 'aberto', 'pendente', 'por fazer', 'ainda nao', 'v410/v411' nos textos novos e rendidos. Segmento = entre . ; | \n \" « »."""
import glob, os, re, sys, json
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/"
fontes = [R + f for f in ("artigo_pt_v409.pysnip", "artigo_en_v409.pysnip", "registros_v409.py", "runtime_v409.py", "delta_v409.py", "pos_rito/textos_v409_novo.pysnip", "pos_rito/textos_v409.py", "pos_rito/textos_custodia_handoff_v409.py", "pos_rito/CUSTODIA_v409_RASCUNHO.txt")]
fontes += sorted(glob.glob("C:/t/h409/harness_saida_v409/textos/*.txt"))
ruim = re.compile(r"\bOPEN\b|\baberto\b|\bpendente\b|por\s+fazer|ainda\s+n(?:ã|a)o|not\s+yet|\bopen\b|\bv41[0-9]\b", re.I)
res = {}
for a in fontes:
    t = open(a, encoding="utf-8", errors="replace").read()
    for seg in re.split(r"[.;|\n\"«»]", t):
        sl = seg.lower()
        if (re.search(r"fock", sl) or re.search(r"(?:ω|omega)[^;]{0,80}uniform", sl)) and ruim.search(seg) and not any(x in sl for x in ("e21", "v407", "deixou", "dizia", "podad", "pruned")):
            res.setdefault(seg.strip()[:300], set()).add(os.path.basename(a))
print("segmentos (Fock|Omega-uniforme) + OPEN/aberto/pendente/v41x, fora de E21/v407/podada:", len(res))
for s, fs in sorted(res.items(), key=lambda x: sorted(x[1])[0]): print(" -", sorted(fs)[:5], "|", s)
json.dump({k: sorted(v) for k, v in res.items()}, open(R + "revisao_terceiro/t1b_fock_open_amplo_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

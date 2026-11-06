# -*- coding: utf-8 -*-
"""_varredura_recorte_v409.py -- (claude-construtor-v409) recorta a varredura (varredura_fock_omega_v409.py) ao texto NOVO da v409: no core e no selo, so' as chaves da v409; no .md canonico, so' a linha da v409; nos
artigos rendidos, so' a secao da v409; nas superficies de memoria do harness, so' as linhas que nao estavam no .bak (o acrescimo); o resto inteiro. (O texto selado/herdado das versoes anteriores fica como registro.)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("varredura_fock_omega_v409.py")
i0 = a.t.index('R = {"arquivos": 0, "achados": []}')
i1 = a.t.index('novos = [a_ for a_ in R["achados"]')
novo = '''R = {"arquivos": 0, "achados": [], "recorte": "texto NOVO da v409: no core e no selo, so' as chaves da v409; no .md canonico, so' a linha da v409; nos artigos rendidos, so' a secao da v409; nas superficies do harness, so' o acrescimo sobre o .bak; o resto inteiro"}
for p_ in ARQ:
    if not os.path.isfile(p_) or ".bak_" in os.path.basename(p_):
        continue
    R["arquivos"] += 1
    t_ = open(p_, encoding="utf-8", errors="replace").read()
    b_ = os.path.basename(p_)
    if b_ in ("core_ensaio.json", "selo_ensaio.json") or (b_.startswith("um_absoluto") and b_.endswith(".json")):
        try:
            c_ = json.loads(t_)
        except ValueError:
            c_ = {}
        for k_ in [k_ for k_ in (c_ if isinstance(c_, dict) else {}) if "v409" in k_]:
            for a_ in varre_texto(json.dumps(c_.get(k_), ensure_ascii=False)):
                R["achados"].append(dict(a_, arquivo=p_ + "::" + k_))
        continue
    linhas_ = t_.split(chr(10)); idx_ = list(range(len(linhas_)))
    if b_.startswith("um_absoluto_forma_canonica") or b_.startswith("um_absoluto_manifest"):
        idx_ = [i_ for i_ in idx_ if "v409" in linhas_[i_]]
    elif b_.startswith("dry_v409_") and b_.endswith(".txt"):
        i0_ = next((i_ for i_ in idx_ if "05/11/2026" in linhas_[i_]), None)
        i1_ = next((i_ for i_ in idx_ if i0_ is not None and i_ > i0_ and "04/11/2026" in linhas_[i_]), len(linhas_))
        idx_ = list(range(max(0, i0_ - 3), i1_)) if i0_ is not None else []
    else:
        baks_ = sorted(glob.glob(p_ + ".bak_*"))
        if baks_:
            velhas_ = set(open(baks_[0], encoding="utf-8", errors="replace").read().split(chr(10)))
            idx_ = [i_ for i_ in idx_ if linhas_[i_] not in velhas_]
    for i_ in idx_:
        for a_ in varre_texto(linhas_[i_]):
            R["achados"].append(dict(a_, arquivo="%s:%d" % (p_, i_ + 1)))
'''
a.t = a.t[:i0] + novo + a.t[i1:]
a.grava()

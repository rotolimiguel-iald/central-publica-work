# -*- coding: utf-8 -*-
"""_varredura_historico_v409.py -- (claude-construtor-v409) a varredura (varredura_fock_omega_v409.py) passa a classificar como HISTORICO, alem dos marcadores: (a) o trecho que ja' existe, letra por letra, no texto
SELADO da v408 (o um.py, o core e o selo da base v408 e o stdout do rito da v408 no Nos, so' leitura) -- e' texto herdado, reimpresso pelos registros recriados; (b) nas superficies do harness, a linha que estava no
MEMORY.md.bak (a linha velha movida VERBATIM ao MEMORY_2.md); (c) as superficies da variante «_limite» (o teste do limite RECUSA e nao escreve: nao ha' acrescimo); (d) em guarda_frases_v409.py, as listas de
frases PROIBIDAS e das sondas (sao a definicao da guarda); (e) os artigos rendidos do Nos emulado (um_absoluto_pt/en.txt) recebem o mesmo recorte da secao da v409."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
a = Arq("varredura_fock_omega_v409.py")
a.troca('''def segmentos(t_):''', '''_BASE = os.path.join(HERE, "base_v408")
_NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N" + chr(243) + "s")
_HCORP = chr(10).join(open(p_, encoding="utf-8", errors="replace").read() for p_ in (os.path.join(_BASE, "um.py"), os.path.join(_BASE, "um_absoluto.json"), os.path.join(_BASE, "um_absoluto_selo.json"),
                                                                                    os.path.join(_NOS, "rodada_v408_stdout.txt")) if os.path.isfile(p_))
_HCORP_N = re.sub(r"\\s+", " ", _HCORP)


def herdado(trecho_):
    t_ = re.sub(r"\\s+", " ", trecho_.strip())
    return len(t_) >= 12 and t_ in _HCORP_N


def segmentos(t_):''')
a.troca('''            out_.append({"tipo": "fock" if f_ else "omega", "trecho": s_.strip()[:240], "historico": any(h_ in sl_ for h_ in HIST)})''',
        '''            out_.append({"tipo": "fock" if f_ else "omega", "trecho": s_.strip()[:240], "historico": any(h_ in sl_ for h_ in HIST) or herdado(s_)})''')
a.troca('''    if not os.path.isfile(p_) or ".bak_" in os.path.basename(p_):
        continue''', '''    if not os.path.isfile(p_) or ".bak_" in os.path.basename(p_) or (os.sep + "ensaio_superficies_limite" + os.sep) in p_:
        continue''')
a.troca('''    elif b_.startswith("dry_v409_") and b_.endswith(".txt"):''', '''    elif (b_.startswith("dry_v409_") or b_.startswith("um_absoluto_")) and b_.endswith(".txt"):''')
a.troca('''        baks_ = sorted(glob.glob(p_ + ".bak_*"))
        if baks_:
            velhas_ = set(open(baks_[0], encoding="utf-8", errors="replace").read().split(chr(10)))
            idx_ = [i_ for i_ in idx_ if linhas_[i_] not in velhas_]''', '''        baks_ = sorted(glob.glob(p_ + ".bak_*"))
        if baks_:
            velhas_ = set(open(baks_[0], encoding="utf-8", errors="replace").read().split(chr(10)))
            if b_ == "MEMORY_2.md":   # a linha velha do MEMORY.md movida VERBATIM ao MEMORY_2.md e' historica
                for bk_ in sorted(glob.glob(os.path.join(os.path.dirname(p_), "MEMORY.md.bak_*")))[:1]:
                    velhas_ |= set(open(bk_, encoding="utf-8", errors="replace").read().split(chr(10)))
            idx_ = [i_ for i_ in idx_ if linhas_[i_] not in velhas_]
    if b_ == "guarda_frases_v409.py":   # as listas de PROIBIDAS/sondas sao a definicao da guarda
        i_p_ = next((i_ for i_ in range(len(linhas_)) if linhas_[i_].startswith("PROIBIDAS = ")), 0)
        idx_ = [i_ for i_ in idx_ if i_ > i_p_]''')
a.grava()

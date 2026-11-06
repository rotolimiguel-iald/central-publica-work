# -*- coding: utf-8 -*-
"""_dois_modulos_runtime_v409.py -- (claude-construtor-v409, 05/11/2026, ~17h) runtime_v409.py segue o AO LADO de ~18h do DESENHO_v409: (1) as checagens c18 (a marginal do par de Bell finito, numpy: ½·I e 1 - pureza = ½),
c19 (a inscricao num F de brinquedo em C^3: <Omega, V L V^dagger Omega> = Z(s)/2^n, s em {0, 1, 5}) e c20 (uma leitura decide SAT: «o que sou» = |sol|/2^n > 0 na SIM e 0 na NAO); a c1 conta as ancoras das DUAS pedras;
(2) a guarda das frases ganha as regras do AO LADO: F40 «Ω é o uniforme» como identidade; F41 o par na face de Fock dito em aberto; F42 a passagem a v410; F43 a OBRIGACAO da E28 onde o leitor de Turing aparecer
(NP numa leitura; a igualdade completa so' para o leitor que se le); (3) o registro diz tambem o que FECHOU nesta versao. Trocas de contagem exata; backup de bytes."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

a = Arq("runtime_v409.py")
# ---- (2) a guarda das frases
a.troca('''    for m_ in _re.finditer(r"\\bprecisa\\s+(?:saber|reconhecer)[^.;\\n]{0,80}?\\ba\\s+cada\\s+passo\\b|\\bneeds?\\s+to\\s+(?:know|recogni[sz]e)[^.;\\n]{0,80}?\\bat\\s+each\\s+step\\b", s_, _re.I):   # F39 (E25)''',
        '''    for m_ in _re.finditer(r"(?:Ω|Omega)(?:\\s+do\\s+ps[ií]on(?:\\s+da\\s+luz)?|\\s+of\\s+the\\s+(?:light\\s+)?psion)?\\s+(?:é|e'|is)\\s+(?:o|the)\\s+(?:estado\\s+)?uniform", s_, _re.I):   # F40 (D60 revista): «Ω é o uniforme» como IDENTIDADE
        seg_ = s_[max(0, m_.start() - 120):m_.end() + 120].lower()
        if "«" in s_[max(0, m_.start() - 3):m_.start()] or any(n_ in seg_ for n_ in ("podad", "pruned", "não é", "nao e'", "is not", "como igualdade de vetores")):
            continue
        out_.append(("F40_omega_e_o_uniforme_como_identidade", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\\n", " ")))
    for m_ in _re.finditer(r"par\\s+(?:de\\s+ps[ií]ons\\s+)?na\\s+face\\s+de\\s+Fock\\s+(?:segue|fica|continua)\\s+(?:\\[OPEN\\]|em\\s+aberto|aberto)|pair\\s+(?:of\\s+psions\\s+)?on\\s+the\\s+Fock\\s+face\\s+(?:stays|remains)\\s+(?:\\[OPEN\\]|open)", s_, _re.I):   # F41 (D60 revista)
        out_.append(("F41_par_na_face_de_fock_dito_em_aberto", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\\n", " ")))
    for m_ in _re.finditer(r"passa\\s+(?:à|a)\\s+v410|v410\\s+em\\s+diante|v410\\s+onwards?|passes\\s+to\\s+v410", s_, _re.I):   # F42 (D60 revista): nada passa a v410
        out_.append(("F42_passa_a_v410", s_[max(0, m_.start() - 30):m_.end() + 30].replace("\\n", " ")))
    if _re.search(r"or[aá]culo|oracle|leitor\\s+que\\s+(?:devolve|retorna)\\s+Z|reader\\s+that\\s+returns\\s+Z|leitor\\s+de\\s+Turing|Turing\\s+reader", s_, _re.I):   # F43 (a OBRIGACAO da E28)
        _np1 = _re.search(r"NP\\s+(?:contido\\s+em|⊆)\\s+P|NP[^.;]{0,40}?(?:com|numa|em)\\s+(?:uma|1)\\s+(?:s[oó]'?\\s+)?leitura|uma\\s+leitura\\s+decide|NP\\s+in\\s+one\\s+reading|NP\\s+contained\\s+in\\s+P|one\\s+reading\\s+decides", s_, _re.I)
        _np2 = _re.search(r"leitor\\s+que\\s+se\\s+l[eê]|l[eê]\\s+tamb[eé]m\\s+as\\s+m[aá]quinas|reader\\s+that\\s+reads\\s+itself|also\\s+reads\\s+the\\s+machines", s_, _re.I)
        if not (_np1 and _np2):
            m43_ = _re.search(r"or[aá]culo|oracle|leitor\\s+que\\s+(?:devolve|retorna)\\s+Z|reader\\s+that\\s+returns\\s+Z|leitor\\s+de\\s+Turing|Turing\\s+reader", s_, _re.I)
            out_.append(("F43_leitor_de_turing_sem_a_E28", s_[max(0, m43_.start() - 30):m43_.end() + 60].replace("\\n", " ")))
    for m_ in _re.finditer(r"\\bprecisa\\s+(?:saber|reconhecer)[^.;\\n]{0,80}?\\ba\\s+cada\\s+passo\\b|\\bneeds?\\s+to\\s+(?:know|recogni[sz]e)[^.;\\n]{0,80}?\\bat\\s+each\\s+step\\b", s_, _re.I):   # F39 (E25)''')
a.troca('''    F37 a OBRIGACAO: onde «P = nP» e Turing aparecem juntos, o mesmo texto traz o qualificador «relativa ao leitor» e «a maquina sem leitor»;''',
        '''    F40 a F43 (AO LADO de ~18h do DESENHO; D60 revista e E28): proibido «Ω é o uniforme» como identidade (fora de citacao e sem a poda dita), o par na face de Fock dito em aberto e a passagem a v410; obrigatorio, onde o leitor de Turing aparecer, a E28 (NP numa leitura; a igualdade completa so' para o leitor que se le);
    F37 a OBRIGACAO: onde «P = nP» e Turing aparecem juntos, o mesmo texto traz o qualificador «relativa ao leitor» e «a maquina sem leitor»;''')
# ---- (1) as checagens c18-c20 e a c1 das duas pedras
a.troca('''    txt_ = globals().get("_V409_TRADUCAO_TEXT") or {}
    guarda_ = list(_v392_guarda_texto(_j409.dumps(txt_, ensure_ascii=False))) + list(_v409_guarda_frases(_j409.dumps(txt_, ensure_ascii=False)))''',
        '''    # c18 a marginal do par de Bell finito em C2 x C2 (numpy): psi = (e1 x e1 + e2 x e2)/sqrt2; o reduzido e' ½·I2 e 1 - pureza = ½ (bell_reduced_half; bell_cci_half; reduzido_do_par)
    import numpy as _np409
    psi_ = _np409.zeros(4, dtype=complex); psi_[0] = 1.0; psi_[3] = 1.0; psi_ = psi_ / _np409.sqrt(2.0)
    rho_ = _np409.outer(psi_, psi_.conj()).reshape(2, 2, 2, 2)
    red_ = _np409.einsum("ijkj->ik", rho_)
    pur_ = float(_np409.real(_np409.trace(red_ @ red_)))
    bell_ok_ = bool(_np409.allclose(red_, 0.5 * _np409.eye(2), atol=1e-12) and abs((1.0 - pur_) - 0.5) < 1e-12)
    # c19 a inscricao num F de brinquedo (C^3; Omega FIXO no contrato, normalizado aqui): V = |Omega><u| e <Omega, V L_s V^dagger Omega> = Z(s)/2^n na instancia SIM (o_psion_le_z; o_canto_do_psion_da_luz_le_z)
    ib_ = c_["inscricao_brinquedo"]
    om_ = _np409.array([complex(re_, im_) for re_, im_ in ib_["omega"]], dtype=complex); om_ = om_ / _np409.linalg.norm(om_)
    uu_ = _np409.full(N_, 1.0 / _m409.sqrt(N_), dtype=complex)
    V_ = _np409.outer(om_, uu_.conj())
    insc_ = []
    for s_ in ib_["s"]:
        L_ = _np409.diag([_m409.exp(-s_ * c0_) for c0_ in cs_]).astype(complex)
        val_ = complex(om_.conj() @ (V_ @ L_ @ V_.conj().T) @ om_)
        insc_.append((s_, val_.real, Z_(s_, cs_) / N_, abs(val_ - Z_(s_, cs_) / N_) < 1e-12))
    # c20 uma leitura decide SAT: a SIM em CNF (as tres clausulas) tem «o que sou» = |sol|/2^n > 0; a NAO, (x1), (nao x1), tem 0 (custo = numero de clausulas violadas; uma_leitura_decide_SAT; a_maquina_com_o_leitor)
    oqs_cnf_sim_ = sum(1 for c0_ in cs_ if c0_ == 0) / float(N_); oqs_cnf_nao_ = sum(1 for c0_ in cn_ if c0_ == 0) / float(Nn_)
    decide_ = (oqs_cnf_sim_ > 0.0, oqs_cnf_nao_ > 0.0)
    txt_ = globals().get("_V409_TRADUCAO_TEXT") or {}
    guarda_ = list(_v392_guarda_texto(_j409.dumps(txt_, ensure_ascii=False))) + list(_v409_guarda_frases(_j409.dumps(txt_, ensure_ascii=False)))''')
a.troca('''        {"id": "c1", "descricao": "as %d ancoras da pedra TraducaoTuring no axiom_report do rito,''', '''        {"id": "c1", "descricao": "as %d ancoras das DUAS pedras (TraducaoTuring e ParNaFaceDeFock) no axiom_report do rito,''')
a.troca('''        {"id": "c2", "descricao": "o modulo do bundle embutido com o sha256 do contrato == o hash formal do rito; a raiz embutida traz o import",''', '''        {"id": "c2", "descricao": "os modulos do bundle embutidos com o sha256 do contrato == o hash formal do rito; a raiz embutida traz os imports",''')
i0 = a.t.index('''        {"id": "c17", "descricao": "beta = alfa CODATA 2018 x sqrt(e) em runtime''')
i1 = a.t.index("\n", i0) + 1
assert a.t[i1:].startswith("    ]"), a.t[i1:i1 + 20]
a.t = a.t[:i1] + '''        {"id": "c18", "descricao": "a marginal do par de Bell finito em C2 x C2, (e1 x e1 + e2 x e2)/sqrt2, calculada por numpy: o reduzido e' ½·I2 e 1 - pureza = ½, |Delta| < 1e-12 (a mesma Meia-Nat do par na face de Fock: reduzido_do_par, meia_nat_do_projetor)", "ok": bell_ok_},
        {"id": "c19", "descricao": "a inscricao num F de brinquedo (C^3, Omega unitario): V = |Omega><u| e <Omega, V L_s V^dagger Omega> = Z(s)/2^n na instancia SIM, para s em %s, |Delta| < 1e-12 (o_psion_le_z; o_canto_do_psion_da_luz_le_z)" % list(ib_["s"]), "ok": len(insc_) == len(ib_["s"]) >= 3 and all(x_[3] for x_ in insc_)},
        {"id": "c20", "descricao": "uma leitura decide SAT: a instancia SIM em CNF tem «o que sou» = |sol|/2^n > 0 e a NAO, (x1), (nao x1), tem 0 (o custo e' o numero de clausulas violadas; uma_leitura_decide_SAT; a_maquina_com_o_leitor)", "ok": decide_ == (True, False) and abs(oqs_cnf_sim_ - S_ / float(N_)) < 1e-15 and oqs_cnf_nao_ == 0.0 and len(soln_) == 0},
''' + a.t[i1:]
a.troca('''"ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]), "respostas_ok": all(resp_.values()) if resp_ else False}''',
        '''"ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]), "fechado_nesta_versao": dict(c_.get("fechado_nesta_versao") or {}),
               "bell_finito": {"reduzido_e_meio_I": bell_ok_, "um_menos_pureza": 1.0 - pur_}, "inscricao": insc_, "uma_leitura_decide_sat": {"sim": oqs_cnf_sim_, "nao": oqs_cnf_nao_},
               "respostas_ok": all(resp_.values()) if resp_ else False}''')
a.troca('''"chaves_antigas_que_mudam": list(c_["chaves"]), "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]),
            "alcance": c_["alcance"],''', '''"chaves_antigas_que_mudam": list(c_["chaves"]), "ressalvas": list(c_["ressalvas"]), "fica_false_por_teorema": list(c_["fica_false_por_teorema"]), "fica_aberto": dict(c_["fica_aberto"]),
            "fechado_nesta_versao": dict(c_.get("fechado_nesta_versao") or {}), "ancora_par": c_.get("ancora_par"), "alcance": c_["alcance"],''')
a.troca('''    Le do kernel do PROPRIO rito as 62 ancoras da pedra TraducaoTuring, o modulo por sha256, as falas de 05/11 por sha256; confere as respostas do operador pelos teoremas da pedra; faz as 17 checagens''',
        '''    Le do kernel do PROPRIO rito as 82 ancoras das DUAS pedras (TraducaoTuring e ParNaFaceDeFock), os modulos por sha256, as falas de 05/11 por sha256; confere as respostas do operador pelos teoremas da pedra; faz as 20 checagens''')
a.grava()

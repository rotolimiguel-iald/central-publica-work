# -*- coding: utf-8 -*-
"""_adapt_dois_modulos_ensaio_runtime_v409.py -- (claude-construtor-v409, 05/11/2026) o bundle passa a DOIS modulos (TraducaoTuring refeita da R9 + ParNaFaceDeFock) e a ordem
«tudo na v409» (AO LADO mais novo do DESENHO_v409.md: D60 revista, E28, ressalvas, E21 ao lado, N_CHECKS_FECHO = 20, c1 com 82 ancoras):
(a) runtime_v409.py: a c1 exigia o bundle com UM modulo (`== c_["bundle"]["n"] == 1`): passa a exigir o numero de modulos do contrato == o numero de fontes pinadas (a CAUSA; nada relaxado);
(b) o ensaio a seco (o bloco-fonte _ensaio_bloco_v409.pysnip E o montado ensaio_a_seco_v409.py, as mesmas trocas nos dois): 2 modulos, 82 ancoras, 20 checagens, 13 falas, 7 erratas (E24 a E28, a E21 ao lado e a dos pisos),
o que fica aberto (maquina sem leitor, a igualdade com o leitor que so' conta, a ponte Bell-TT) e o que FECHA nesta versao (o par na face de Fock; a ponte Omega-uniforme pela inscricao), a c2 negada pela raiz sem CADA um
dos dois imports, as negacoes da mecanica com a c20 (a instancia SIM sem solucao derruba c4, c6, c12 e c20; a NAO com solucao, c10 e c20), as frases proibidas F40 a F42 e as boas novas, e um elo NOVO que REFAZ aqui
(por outro caminho) os valores das checagens c18 (o par de Bell finito), c19 (a inscricao) e c20 (uma leitura decide SAT). Corrige tambem a conferencia que pedia 12 e 10 falas ao mesmo tempo (a causa: a troca 10 -> 12 parcial).
Nenhuma conferencia relaxada: os numeros sobem com o conteudo, as igualdades ficam."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

# ------------------------------------------------------------------------------------------------ (a) runtime: a c1
r = Arq("runtime_v409.py")
if not r.tem('and len(por_mod_) == c_["bundle"]["n"] == len(c_["source_sha256"]) and all(por_mod_.values())},'):   # (reexecutavel: a troca da c1 ja' aplicada fica)
  r.troca('''and len(por_mod_) == c_["bundle"]["n"] == 1 and all(por_mod_.values())},''',
        '''and len(por_mod_) == c_["bundle"]["n"] == len(c_["source_sha256"]) and all(por_mod_.values())},''')
  r.grava()

# ------------------------------------------------------------------------------------------------ (b) o ensaio: as mesmas trocas no bloco-fonte e no montado
T = [
    ("as 62 ancoras pelo DL.ANCORAS", "as 82 ancoras pelo DL.ANCORAS"),
    ("(controles negativos): as 62 ancoras,", "(controles negativos): as 82 ancoras,"),
    ("# a fonte do modulo, as 12 falas do contrato,", "# a fonte de cada um dos DOIS modulos, as 13 falas do contrato,"),
    ("_NCK9 = DL.N_CHECKS_FECHO   # as checagens do registro NOVO: 17 (c1..c17), lidas do DL", "_NCK9 = DL.N_CHECKS_FECHO   # as checagens do registro NOVO: 20 (c1..c20), lidas do DL"),
    ('''== _NCK9 == len(r9["mechanics"]["checks"]) == 17 and''', '''== _NCK9 == len(r9["mechanics"]["checks"]) == 20 and'''),
    ('''== len(DL.BUNDLE_RELS) == 1 and r9["beta_ok"] is True and all(r9["anchors"].values()) and len(r9["anchors"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 62''',
     '''== len(DL.BUNDLE_RELS) == 2 and r9["beta_ok"] is True and all(r9["anchors"].values()) and len(r9["anchors"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 82'''),
    ('''and len(r9["inscriptions"]) == len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 12 and _v9.get("respostas_ok") is True and len(_v9.get("respostas") or {}) == len(DL.RESPOSTAS_DO_OPERADOR) == 9 and all(_v9["por_modulo"].values()) and len(_v9["por_modulo"]) == 1''',
     '''and len(r9["inscriptions"]) == len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 13 and _v9.get("respostas_ok") is True and len(_v9.get("respostas") or {}) == len(DL.RESPOSTAS_DO_OPERADOR) == 9 and all(_v9["por_modulo"].values()) and len(_v9["por_modulo"]) == DL.N_BUNDLE == 2'''),
    ('''and len(CM["n_axiomas_das_ancoras"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 62)''', '''and len(CM["n_axiomas_das_ancoras"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 82)'''),
    ('''and set(_CP9["fica_aberto"]) == {"par_na_face_de_fock", "omega_do_psion_e_o_uniforme", "maquina_sem_leitor", "ponte_bell_tt"} and "[OPEN]" in DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK and "[OPEN]" in DL.FICA_ABERTO_OMEGA_UNIFORME)''',
     '''and set(_CP9["fica_aberto"]) == set(DL.FICA_ABERTO) == {"maquina_sem_leitor", "igualdade_com_o_leitor_que_so_conta", "ponte_bell_tt"} and not ({"par_na_face_de_fock", "omega_do_psion_e_o_uniforme"} & set(_CP9["fica_aberto"]))
                                                                               and _CP9["fechado_nesta_versao"] == dict(DL.FECHADO_NESTA_VERSAO) and set(_CP9["fechado_nesta_versao"]) == {"par_na_face_de_fock", "omega_do_psion_e_o_uniforme"})'''),
    ('''U["traducao_turing_v409_axioma_fora_do_trio_em_cada_ancora_recusa"] = bool(ok_ and len(_CP9["ancoras"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 62)''',
     '''U["traducao_turing_v409_axioma_fora_do_trio_em_cada_ancora_recusa"] = bool(ok_ and len(_CP9["ancoras"]) == len(DL.ANCORAS) == DL.N_ANCORAS_ESPERADAS == 82)'''),
    ('''U["traducao_turing_v409_fonte_adulterada_do_modulo_recusa"] = bool(ok_ and n_ok_ == DL.N_BUNDLE == 1)''', '''U["traducao_turing_v409_fonte_adulterada_do_modulo_recusa"] = bool(ok_ and n_ok_ == DL.N_BUNDLE == 2)'''),
    ('''bool(ok_ and len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 12 and set(_CP9["verbatins"]) <= set(um._V409_VERBATINS2) and len(um._V409_VERBATINS2) == len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409) == DL.N_FALAS_V409 == 10)''',
     '''bool(ok_ and len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 13 and set(_CP9["verbatins"]) <= set(um._V409_VERBATINS2) and len(um._V409_VERBATINS2) == len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409) == DL.N_FALAS_V409 == 13)'''),
    ('''_mec9.append(("c2", _c6_mexe(lambda c_: None), "raiz"))''',
     '''_mec9.append(("c2", _c6_mexe(lambda c_: None), "raiz:import TGLExt.TraducaoTuring"))
_mec9.append(("c2", None, "raiz:import TGLExt.ParNaFaceDeFock"))'''),
    ('''    if esp_ == "raiz":   # c2: a raiz embutida sem o import da TraducaoTuring (a fonte segue batendo; a raiz nao traz o import)
        _ant9 = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant9.replace("import TGLExt.TraducaoTuring", "-- retirado")''',
     '''    if esp_ and esp_.startswith("raiz:"):   # c2: a raiz embutida sem o import de CADA um dos dois modulos (a fonte segue batendo; a raiz nao traz o import)
        _ant9 = um._EMBEDDED_KERNEL_FILES["TGLExt.lean"]; assert _ant9.count(esp_[5:]) == 1, ("a raiz embutida nao traz o import uma vez", esp_[5:])
        um._EMBEDDED_KERNEL_FILES["TGLExt.lean"] = _ant9.replace(esp_[5:], "-- retirado")'''),
    ('''# Pela mecanica chamada direto: beta = 0 (c13 e c17 caem); o contrato com uma ancora a mais (c1 cai); a instancia SIM trocada por uma sem solucao (c4, c6 e c12 caem); a instancia NAO trocada pela SIM (c10 cai); a mecanica certa passa.''',
     '''# Pela mecanica chamada direto: beta = 0 (c13 e c17 caem); o contrato com uma ancora a mais (c1 cai); a instancia SIM trocada por uma sem solucao (c4, c6, c12 e c20 caem); a instancia NAO trocada pela SIM (c10 e c20 caem); a mecanica certa passa.'''),
    ('''# a instancia SIM sem solucao: c4, c6 e c12''', '''# a instancia SIM sem solucao: c4, c6, c12 e c20'''),
    ('''# a instancia NAO com solucao: c10''', '''# a instancia NAO com solucao: c10 e c20'''),
    ('''and _f09(_mss) == ["c12", "c4", "c6"] and _f09(_mnn) == ["c10"] and _mok["passed"] is True)''', '''and _f09(_mss) == ["c12", "c20", "c4", "c6"] and _f09(_mnn) == ["c10", "c20"] and _mok["passed"] is True)'''),
    ('''"P = nP vale para as máquinas de Turing", "TURING_" + "SOLVED", "CLAY_" + "SOLVED", "MILLEN" + "NIUM", "o sistema precisa saber onde está o Nome a cada passo")''',
     '''"P = nP vale para as máquinas de Turing", "TURING_" + "SOLVED", "CLAY_" + "SOLVED", "MILLEN" + "NIUM", "o sistema precisa saber onde está o Nome a cada passo",
                      "o Ω do psíon da luz é o uniforme", "the light psion's Omega is the uniform", "o par na face de Fock segue [OPEN]", "the pair on the Fock face stays open", "o que falta passa à v410", "from v410 onward")'''),
    ('''DL.ERRATA_E26, DL.REGRA_DO_4_44, DL.FICA_ABERTO_PAR_NA_FACE_DE_FOCK, DL.FICA_ABERTO_OMEGA_UNIFORME, DL.FICA_ABERTO_MAQUINA_SEM_LEITOR,''',
     '''DL.ERRATA_E26, DL.REGRA_DO_4_44, DL.FECHADO_PAR_NA_FACE_DE_FOCK, DL.FECHADO_OMEGA_UNIFORME, DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, DL.FICA_ABERTO_IGUALDADE_COM_O_LEITOR, DL.ERRATA_E28, DL.ERRATA_E21_AO_LADO,'''),
    ('''# --- as falas de 05/11 (cunhagens_v409), as decisoes D55-D61, as erratas E24-E27 e a cobertura exata (kh_n1_cobertura_v409)''',
     '''# --- as falas de 05/11 (cunhagens_v409), as decisoes D55-D61, as erratas E24-E28 e a E21 ao lado, e a cobertura exata (kh_n1_cobertura_v409)'''),
    ('''== len(_sp9s["verbatins"]) == DL.N_FALAS_V409 == 12 and all(v_["embedded_ok"]''', '''== len(_sp9s["verbatins"]) == DL.N_FALAS_V409 == 13 and all(v_["embedded_ok"]'''),
    ('''== len(DL.ERRATAS_V409) + 1 == 5 and''', '''== len(DL.ERRATAS_V409) + 1 == 7 and'''),
    ('''and "E27" in str((_cn9x.get("erratas") or [{}, {}, {}, {}])[3].get("agora"))''',
     '''and "E27" in str((_cn9x.get("erratas") or [{}, {}, {}, {}])[3].get("agora"))
                                                                      and str((_cn9x.get("erratas") or [{}] * 5)[4].get("agora")).startswith("E28") and str((_cn9x.get("erratas") or [{}] * 6)[5].get("agora")).startswith("E21")'''),
    ('''and _xn9.get("n_falas") == 12''', '''and _xn9.get("n_falas") == 13'''),
    ('''sorted((_xn9.get("autores") or {}).values()) == ["operador"] * 12''', '''sorted((_xn9.get("autores") or {}).values()) == ["operador"] * 13'''),
    # o elo NOVO: c18 a c20 refeitos AQUI por outro caminho (o traco parcial por laco, nao por einsum; a inscricao pela identidade V^dagger Omega = u; a leitura SAT pela enumeracao propria)
    ('''_cc10 = _rapido9(); _cc10.pop("traducao_turing_v409", None);''',
     '''# c18 a c20 REFEITOS AQUI por outro caminho: o reduzido do par de Bell finito pelo traco parcial em laco (nao einsum); a inscricao pela identidade V^dagger Omega = u (Omega normalizado), logo <Omega, V L_s V^dagger Omega> = <u, L_s u> = Z(s)/2^n;
# a leitura que decide SAT pela enumeracao propria (_sat9): «o que sou» = |sol|/2^n na SIM e 0 na NAO
_psi9 = [1.0 / _math.sqrt(2.0), 0.0, 0.0, 1.0 / _math.sqrt(2.0)]
_red9 = [[sum(_psi9[2 * i_ + k_] * _psi9[2 * j_ + k_] for k_ in (0, 1)) for j_ in (0, 1)] for i_ in (0, 1)]
_pur9 = sum(_red9[i_][j_] * _red9[j_][i_] for i_ in (0, 1) for j_ in (0, 1))
_bf9 = _v9.get("bell_finito") or {}; _ins9 = _v9.get("inscricao") or []; _sat9v = _v9.get("uma_leitura_decide_sat") or {}
U["traducao_turing_v409_o_par_de_bell_a_inscricao_e_a_leitura_sat_refeitos_aqui"] = bool(all(abs(_red9[i_][j_] - (0.5 if i_ == j_ else 0.0)) <= 1e-15 for i_ in (0, 1) for j_ in (0, 1)) and abs((1.0 - _pur9) - 0.5) <= 1e-15
                                                                                         and _bf9.get("reduzido_e_meio_I") is True and abs(_bf9.get("um_menos_pureza") - (1.0 - _pur9)) <= 1e-12
                                                                                         and [float(x_[0]) for x_ in _ins9] == [float(s_) for s_ in DL.S_INSCRICAO] == [float(s_) for s_ in _CP9["inscricao_brinquedo"]["s"]] and len(_ins9) >= 3
                                                                                         and all(abs(x_[1] - _Z9(s_, _cs9) / _N9) <= 1e-12 and x_[3] is True for x_, s_ in zip(_ins9, DL.S_INSCRICAO))
                                                                                         and len(_CP9["inscricao_brinquedo"]["omega"]) == len(DL.OMEGA_F_BRINQUEDO) == 3 and abs(_sat9v.get("sim") - _S9 / _N9) <= 1e-15 and _S9 / _N9 > 0.0 and _sat9v.get("nao") == 0.0 == sum(1 for v_ in _cn9 if v_ == 0) / len(_xn9))
_cc10 = _rapido9(); _cc10.pop("traducao_turing_v409", None);'''),
]
for nome in ("ensaio_a_seco_v409.py",):   # (o bloco-fonte ja' recebeu as trocas na primeira execucao; a ultima, ancorada no comentario, casou la' uma vez)
    a = Arq(nome)
    for v_, n_ in T:
        a.troca(v_, n_)
    a.grava()

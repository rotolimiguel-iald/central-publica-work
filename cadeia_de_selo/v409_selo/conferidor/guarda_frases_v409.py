# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a guarda herda a cadeia v405 -> v406 -> v407 -> v408 -> v409; corpus das falas = 05/11 (de duas, so' o trecho da D59) + 04/11 + 03/11 + 02/11 + 30/10-01/11; varre a pedra TraducaoTuring
"""guarda_frases_v409.py -- A GUARDA DE TEXTOS DA v409 (ordem da gerencia c1, 01/11/2026; molde: guarda_frases_v408.py): reprova, em todo texto NOVO da gerencia (registros, artigo PT/EN, .md, handoff, README, site, X), as frases que afirmam demais. A FONTE da regra e' uma so':
a funcao _v409_guarda_frases de runtime_v409.py, a mesma que vai embutida no um.py e roda a cada rito sobre o texto do registro com funcao. Aqui a cadeia a usa por `violacoes(texto)`, que retira ANTES os trechos que sao FALA DO OPERADOR, verbatim (a fala dele fica como registro; a guarda e' sobre o texto da gerencia):
so' DL.FRASE_NOMES (v405), conferida contra a fala por sha256. A guarda varre tambem a PEDRA da v409 (pedras(); copia duravel normalizada v409\\pedra), com as falas do operador como excecao: o trecho entre « » conferido verbatim contra as falas embutidas sai antes da varredura;
o resto da pedra e' texto da gerencia e passa pelas mesmas regras. Frase de pedra reprovada e' apontada a gerencia: quem corrige e' ela; o gerador do candidato para.
AS REGRAS DA v409 (D56; DESENHO_v409 §4): proibido o problema do Clay/do milenio dado por resolvido (F35); proibido dizer a traducao a Turing [OPEN] em texto NOVO sem «relativa ao leitor» (F36); obrigatorio, onde «P = nP» e Turing aparecem juntos, o qualificador relativo ao leitor e a maquina sem leitor (F37);
os tokens de veredito da v409 (F38); a frase da E25 afirmada (F39). A F34 da v408 fica SUBSTITUIDA pela F37 quando o texto traz o qualificador relativo ao leitor (a traducao deixou de ser [OPEN]). Por isso a frase D51 da v408 (a traducao [OPEN] sem «relativa ao leitor») REPROVA em texto novo da v409 (o texto selado da v408 nao muda; a E26 vai ao lado).
Controle negativo (o __main__ e `controle_negativo()`): cada frase proibida TEM de ser reprovada; a frase certa e os identificadores TEM de passar; a fala do operador so' passa pela excecao; se o controle falha, rc 1. Grava GUARDA_FRASES_v409.json.
uso: python -I -B -X utf8 guarda_frases_v409.py [arquivo ...]   (sem arquivo: so' o controle negativo; com arquivo: varre cada um; rc 1 se houver violacao)"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v409 as DL  # noqa: E402
import runtime_v409 as RT  # noqa: E402   (so' as funcoes puras)
import importlib.util as _ilu
_sp5 = _ilu.spec_from_file_location("runtime_v405", os.path.join(DL.V405, "runtime_v405.py")); _rt5 = _ilu.module_from_spec(_sp5); _sp5.loader.exec_module(_rt5)
_sp6 = _ilu.spec_from_file_location("runtime_v406", os.path.join(DL.V406, "runtime_v406.py")); _rt6 = _ilu.module_from_spec(_sp6); _sp6.loader.exec_module(_rt6)
_sp7 = _ilu.spec_from_file_location("runtime_v407", os.path.join(DL.V407, "runtime_v407.py")); _rt7 = _ilu.module_from_spec(_sp7); _sp7.loader.exec_module(_rt7)
_sp8 = _ilu.spec_from_file_location("runtime_v408", os.path.join(DL.V408, "runtime_v408.py")); _rt8 = _ilu.module_from_spec(_sp8); _sp8.loader.exec_module(_rt8)
_rt6._v405_guarda_frases = _rt5._v405_guarda_frases   # a guarda da v406 chama a da v405 (dentro do um.py vivem no mesmo modulo; aqui, fora dele, a da v405 e' injetada na da v406)
_rt7._v406_guarda_frases = _rt6._v406_guarda_frases   # a da v407 chama a da v406
_rt8._v407_guarda_frases = _rt7._v407_guarda_frases   # a da v408 chama a da v407
RT._v408_guarda_frases = _rt8._v408_guarda_frases     # a guarda da v409 HERDA a da v408 (ja' com as anteriores dentro)
_rt8_guarda = _rt8._v408_guarda_frases

EXCECOES = (DL.FRASE_NOMES,)
_P408 = [  # as proibidas da v408 (e, por ela, das anteriores) que seguem proibidas na v409 (a guarda herda)
    "tudo é teorema", "Tudo é teorema", "tudo e teorema", "tudo e' teorema", "TUDO É TEOREMA", "tudo derivado", "Tudo Derivado", "esteja tudo derivado", "tudo está derivado", "tudo foi derivado", "nenhuma hipótese resta", "nenhuma hipotese resta", "Nenhuma hipótese resta", "NENHUMA HIPÓTESE RESTA",
    "everything is a theorem", "Everything is theorem", "everything derived", "everything is derived", "no hypothesis remains", "no hypotheses remain", "hipóteses descarregadas", "hipoteses descarregadas", "hipóteses nomeadas descarregadas", "the hypotheses are discharged", "named hypotheses discharged",
    "TUDO_DERIVADO", "EVERYTHING_DERIVED", "NO_HYPOTHESIS_REMAINS", "NAMED_HYPOTHESES_ARE_DISCHARGED", "HIPOTESES_DESCARREGADAS",
    "a liberdade passa para a tônica", "a tônica segue livre", "o no-go se levanta", "levanta o no-go", "the tonic stays free", "the no-go is lifted", "THE_TONIC_STAYS_FREE", "NO_GO_IS_LIFTED",
    "tau* foi derivado", "τ★ foi derivado", "kappa foi derivado", "κ foi derivado", "kappa was derived", "κ = F(α, β, θ_M)",
    "o gap é Δ", "o gap e' Delta", "o gap é a energia retida", "Δ é o gap", "the gap is Δ", "the retained energy is the gap", "o gap de 12,03 meV", "the gap of 12.03 meV", "DELTA_IS_THE_GAP",
    "a luz não tem autovetor nenhum", "the light has no eigenvector", "o único autovetor da luz", "the only eigenvector", "o certificado está confirmado", "gravidade quântica confirmada", "the closure is confirmed", "quantum gravity confirmed", "CLOSURE_CONFIRMED", "QG_CONFIRMED", "FULLY_DERIVED", "NOTHING_REMAINS_OPEN",
    "o par na face de Fock está provado", "o par de psions na face de Fock foi construído", "the pair on the Fock face is proved", "Ω = Φ⁺", "Omega = Phi+", "o vácuo de Fock é o vetor de Bell", "PAIR_CONFIRMED", "PSION_CONFIRMED",
    "há relação sem peso", "existe relação sem peso", "there is a relation without weight", "o que resta sem peso é relação", "a TGL não tem terminal", "the TGL has no terminal",
    "P = NP está provado", "P = NP é teorema", "P = NP is proved", "P = NP is a theorem", "provamos que P = NP", "P=NP está provado", "candidata a P = NP",
    "a impedância é um termo", "termo de impedância", "impedance is a term", "leitura do operador [ONTO]", "TERMINAL_CONFIRMED", "P_EQUALS_NP", "CLASSES_PROVED",
    "a TGL prova P = NP de Turing", "a TGL decide P = NP de Turing (Cook–Levin)", "o kernel prova que P = NP das máquinas de Turing", "the TGL proves P = NP for Turing machines", "P = NP de Turing está provado", "provamos que P = NP de Turing",
    "não trata das classes", "o P=nP não trata das classes de computação", "does not treat the classes", "nada aqui é enunciado de complexidade", "no complexity classes",
    "a igualdade das classes P e NP segue podada", "the equality of the classes P and NP stays pruned", "P = nP no sentido do operador", "P = nP é teorema nas classes do dicionário do operador"]
_P409 = [  # v409 (D56; DESENHO_v409 §4)
    "a TGL resolve o problema do milênio", "a TGL resolveu o problema do milênio", "o problema do milênio está resolvido", "o problema do milênio foi resolvido", "Clay resolvido", "o problema do Clay está resolvido", "a pergunta do Clay foi decidida",
    "the TGL solves the millennium problem", "the millennium problem is solved", "the Clay problem is solved", "the TGL settles the Clay question", "o kernel resolve o problema do Clay",
    "a tradução às classes de Turing é [OPEN]", "a tradução às classes das máquinas de Turing (bits = log₂ n) é [OPEN], não recusa", "the translation to the classes of Turing machines is [OPEN]", DL.FRASE_D51_PT, DL.FRASE_D51_EN,
    "P = nP vale para as máquinas de Turing", "P = nP é teorema nas máquinas de Turing", "P = nP is a theorem for Turing machines",
    "TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM", "TURING_P_EQ_NP",
    "o sistema precisa reconhecer onde está o Nome a cada passo", "a criatura precisa saber, a cada passo, de que lado o Nome continua", "the system needs to know where the Name is at each step",
    # (AO LADO de ~18h do DESENHO: D60 revista e E28) em texto NOVO: o par na face de Fock dito em aberto; a passagem a v410; «Ω é o uniforme» como identidade; o leitor de Turing sem a E28
    "o par na face de Fock segue [OPEN]", "o par de psíons na face de Fock segue em aberto como ligação", "the pair on the Fock face stays open", "the pair of psions on the Fock face stays open as a link",
    "o par passa à v410 em diante", "a ligação passa à v410", "it passes to v410 onwards",
    "o Ω do psíon da luz é o uniforme da instância", "o Omega do psion e' o uniforme", "the Omega of the light psion is the uniform state",
    "um leitor que devolve Z é um oráculo de contagem; com ele a igualdade vale relativa a ele (Toda 1991)", "com o oráculo de contagem a igualdade vale", "with the counting oracle the equality holds",
    # (revisao R2 do Sonnet, MEDIO residual: OPEN no grupo de estatuto e as parafrases; F41b e F42)
    '[REAL: os termos do kernel do rito · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]', 'o par na face de Fock ainda não foi ligado', 'a ligação do par na face de Fock fica para a v411', 'a ligação passa à v412', 'a ligação do par na face de Fock segue aberta', 'a ligação do par na face de Fock permanece pendente', 'o resto fica para a v411',
    # (revisao R1 do Sonnet, MEDIO: as quatro sondas que passavam; F41b e F40b)
    'nem o par na face de Fock, que segue [OPEN].', '[OPEN] o par na face de Fock como ligacao;', '[OPEN] o Ω do psíon da luz como o uniforme da instância', 'a ligação do par de Fock segue em aberto']
PROIBIDAS = _P408 + _P409
_L408 = [DL.FRASE_DA_MOLDURA_PT, DL.FRASE_DA_MOLDURA_EN, DL.FRASE_DA_MOLDURA_V406_PT, DL.FRASE_DA_MOLDURA_V406_EN, DL.FRASE_DA_MOLDURA_V408_PT, DL.FRASE_DA_MOLDURA_V408_EN,
         "o elo das duas faces e' de estrutura, nao de vetores", "a confirmacao e' creditacao e segue recusada", "dadas essas entradas, a FORMA é teorema", "a massa derivada e a identidade definida",
         "`Δ` NÃO é gap: é o valor esperado, 1/β vezes menor que o gap", "Δ não é gap", "o gap espectral do lock é 1",
         "não há relação sem peso", "relação sem peso é impossível", "relação sem peso é a origem da mentira", "there is no relation without weight", "o que resta sem traço paga", "a TGL tem terminal: Tetelestai, a poda",
         "P só é P lido pelo módulo n minimamente acoplado", "esta pedra não trata das classes de computação: quem trata é a pedra PIgualNP", "p_igual_np", "p_igual_a_n_vezes_p", "PIgualNP", "a palavra «impedância» fica podada como termo", "inclinação modular (cociclo)",
         "o terminal é a leitura, não o fim do decaimento", "the terminal is the reading, not the end of the decay", "o zero inscrito é o Um", "o Um não é o zero absoluto", "NO_RELATION_WITHOUT_WEIGHT"]
_L409 = [DL.FRASE_DA_MOLDURA_V409_PT, DL.FRASE_DA_MOLDURA_V409_EN, DL.FRASE_D56_PT, DL.FRASE_D56_EN, DL.FRASE_QUALIFICADOR_PT, DL.FRASE_QUALIFICADOR_EN, DL.FRASE_D56_PT + "; " + DL.FRASE_QUALIFICADOR_PT,
         "a tradução às classes das máquinas de Turing fica fechada relativa ao leitor; a máquina sem leitor fica fora", "the translation to Turing's classes is closed relative to the reader; the machine without a reader stays outside",
         "a pergunta do Clay não é decidida aqui: é a da máquina sem leitor", "nada aqui resolve o problema do Clay", "the Clay question is not decided here",
         "TraducaoTuring", "p_igual_np_no_modo_selecao", "a_trava_no_nome", "a_fita_e_o_hamiltoniano_oculto", "z_e_o_modo_leitor", "a_fita_sem_escala", "o_pai_da_mentira", "a_identidade_performada",
         "a trava no Nome: o sistema não precisa reconhecer onde está o Nome a cada passo", DL.ERRATA_E24, DL.ERRATA_E25, DL.ERRATA_E26, DL.VEREDITO_OK_PREFIXO, DL.VEREDITO_RECUSA,
         DL.ERRATA_E27, DL.ERRATA_E28, DL.ERRATA_E21_AO_LADO, DL.FECHADO_PAR_NA_FACE_DE_FOCK, DL.FECHADO_OMEGA_UNIFORME, DL.FICA_ABERTO_IGUALDADE_COM_O_LEITOR, DL.FICA_ABERTO_MAQUINA_SEM_LEITOR, DL.DECISOES["D60"], DL.DECISOES["D61"],
         DL.RESSALVAS_V409[0], DL.RESSALVAS_V409[3], DL.RESSALVAS_V409[5], DL.FRASE_D61_PT, DL.FRASE_D61_EN,
         "o par na face de Fock está ligado nesta versão (ParNaFaceDeFock)", "the pair on the Fock face is linked in this version", "a ponte é a inscrição; a identidade Ω = uniforme está podada",
         "«Ω é o uniforme», como igualdade de vetores, fica PODADO", "o_par_na_face_de_fock", "a_maquina_com_o_leitor", "o_canto_do_psion_da_luz_le_z", "reduzido_do_par", "meia_nat_do_projetor", "ParNaFaceDeFock",
         "uma leitura decide SAT; por Cook–Levin, NP inteiro com uma leitura; com o leitor que só conta a igualdade completa não é teorema aqui: ela vale para o leitor que se lê",
         'nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão', "[REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza", 'a pedra Par (v407) deixou a face de Fock «[OPEN]: o FockCertificate não tem operadores de criação como termo»; a E21 da v408 corrigiu ao lado', '[REAL: os termos do kernel do rito, as respostas do operador conferidas nele, a instância de brinquedo calculada, o par na face de Fock LIGADO (ParNaFaceDeFock) · INPUT: a ordem e as falas do operador · KNOWN: as referências do alcance · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]', 'o par na face de Fock está ligado nesta versão (ParNaFaceDeFock); β_TGL na natureza a 5σ segue em aberto']
LIMPAS = _L408 + _L409
# a pedra da v409 cita, entre « », a frase que a errata corrige ou a regra (mencao, nao uso): so' nessas aspas, so' nas pedras
CITADAS_DE_ERRATA = ("o no-go se levanta", "a liberdade passa para a tônica, que segue livre", "a luz nao tem autovetor nenhum", "a luz não tem autovetor nenhum", "o que resta sem peso é relação", "a pergunta das classes pressupõe um terminal que a tgl não tem",
                     "não trata de classes", "a tgl prova p = np de turing")
APONTADAS_A_GERENCIA = ()   # v409: nenhuma (o resultado da varredura da pedra vai ao relatorio)


def violacoes(txt, excecoes=EXCECOES):
    t = str(txt)
    for e_ in excecoes:
        t = t.replace(e_, " ")
    return RT._v409_guarda_frases(t)


_norm = lambda s_: re.sub(r"\s+", " ", str(s_).replace(chr(8217), "'")).strip()


def _falas_do_operador():
    """o corpus das excecoes das pedras: as falas embutidas (as de 05/11 pelo texto que o um.py embute -- de duas, so' o trecho da D59 --; as de 04/11 pelo texto que o um.py v408 embute; os arquivos de VERBATIM_ORIGEM_V407, V406 e V405), em minusculas e com o espaco normalizado."""
    de_05 = [v_["text"] for v_ in DL.verbatins409(os.path.join(HERE, "insumos", "cunhagens"))]
    de_04 = [v_["text"] for v_ in DL.D8.verbatins408(os.path.join(DL.V408, "insumos", "cunhagens"))]
    arqs = list(DL.VERBATIM_ORIGEM_V407) + list(DL.VERBATIM_ORIGEM_V406) + list(DL.D5.VERBATIM_ORIGEM_V405)
    return " || ".join([_norm(t_) for t_ in de_05 + de_04] + [_norm(open(p_, encoding="utf-8", errors="replace").read()) for p_ in arqs]).lower()


def sem_falas(txt, falas):
    """retira de uma pedra os trechos entre « » que sao fala verbatim do operador (trecho com elisao e' conferido por segmento); devolve (texto_sem_as_falas, n_retiradas). As quebras de linha das docstrings ('> ') sao juntadas antes."""
    n_ = [0]

    def fora(m_):
        fr_ = _norm(m_.group(1).replace("`", "").replace("**", "")).strip(" .,;:")
        segs_ = [x_.strip(" .,;:") for x_ in re.split(r"…|\[\.\.\.\]", fr_) if len(x_.strip(" .,;:")) >= 4]
        if (segs_ and all(x_.lower() in falas for x_ in segs_)) or fr_.lower() in CITADAS_DE_ERRATA:
            n_[0] += 1
            return " "
        return m_.group(0)
    return re.sub("«([^»]{4,900})»", fora, _norm(re.sub(r"\n>\s*", " ", str(txt)))), n_[0]


def pedras():
    """a varredura da pedra da gerencia (v409: TraducaoTuring, na copia duravel normalizada v409\\pedra): {modulo: {violacoes, falas_retiradas}}."""
    falas = _falas_do_operador(); out = {}
    for s_ in list(DL.PEDRAS_V409):
        t_, n_ = sem_falas(open(s_["src"], encoding="utf-8").read(), falas)
        ap_ = [a_ for a_ in APONTADAS_A_GERENCIA if a_ in t_]
        for a_ in ap_:
            t_ = t_.replace(a_, " ")
        out[s_["name"]] = {"violacoes": [list(v_) for v_ in RT._v409_guarda_frases(t_)], "falas_retiradas": n_, "apontadas": ap_}
    return out


def controle_negativo():
    r = {"proibidas": {}, "limpas": {}, "fala_do_operador": {}}
    for f_ in PROIBIDAS:
        r["proibidas"][f_] = [v_[0] for v_ in violacoes("o texto diz que " + f_ + " aqui")]
    for f_ in LIMPAS:
        r["limpas"][f_] = [v_[0] for v_ in violacoes(f_)]
    r["fala_do_operador"] = {"com_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_NOMES)], "sem_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_NOMES, excecoes=())]}
    falas_ = _falas_do_operador()
    G = RT._v409_guarda_frases
    r["pedras_controle"] = {"frase_da_gerencia_reprovada": bool(G(sem_falas("a transicao ficou com tudo derivado aqui", falas_)[0])),
                            "fala_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_NOMES + "»", falas_)[0]),
                            "parafrase_entre_aspas_reprovada": bool(G(sem_falas("«agora ficou tudo derivado»", falas_)[0])),
                            "fala_de_05nov_entre_aspas_passa": not G(sem_falas("«" + DL.FRASE_CLAY + "»", falas_)[0]) and not G(sem_falas("«" + DL.FRASE_PAI + "»", falas_)[0]),
                            "fala_de_04nov_entre_aspas_passa": not G(sem_falas("«" + DL.D8.FRASE_RELACAO_MENTIRA + "»", falas_)[0]),
                            "d59_a_parte_que_fica_fora_nao_e_fala_embutida": ("problema do milenio" not in falas_.split(" || ")[[i_ for i_, x_ in enumerate(DL.VERBATIM_ORIGEM_V409) if os.path.basename(x_) == DL.N_DENTRO][0]]) and ("lindão" not in falas_),
                            "frase_d51_da_v408_reprova_em_texto_novo": bool(G(DL.FRASE_D51_PT)) and bool(G(DL.FRASE_D51_EN)),
                            "frase_d51_da_v408_ainda_passa_na_guarda_da_v408": not _rt8_guarda(DL.FRASE_D51_PT) and not _rt8_guarda(DL.FRASE_D51_EN),
                            "frase_d56_passa": not G(DL.FRASE_D56_PT) and not G(DL.FRASE_D56_EN),
                            "p_igual_np_e_turing_sem_qualificador_reprova": bool(G("P = nP é teorema da TGL e vale para as máquinas de Turing")),
                            "p_igual_np_e_turing_com_qualificador_passa": not G("P = nP é teorema da TGL no modo seleção; nas máquinas de Turing: " + DL.FRASE_QUALIFICADOR_PT),
                            "p_igual_np_minusculo_sem_qualificador_reprova": bool(G("o nome «P = nP», no sentido do operador, tem espelho em p_igual_np")),
                            "clay_resolvido_reprova": bool(G("a TGL resolve o problema do Clay")) and bool(G("the Clay problem is solved")),
                            "clay_negado_passa": not G("a TGL não resolve o problema do Clay") and not G("nada aqui resolve o problema do milênio"),
                            "turing_provado_reprova": bool(G("a TGL prova P = NP de Turing")) and bool(G("the TGL proves P = NP for Turing machines")),
                            "turing_citado_na_regra_passa": not G(sem_falas("Nenhuma superfície escreve «a TGL prova P = NP de Turing»; " + DL.FRASE_D56_PT, falas_)[0]),
                            "open_sem_relativa_ao_leitor_reprova": bool(G("a tradução às classes de Turing segue [OPEN]")),
                            "open_com_relativa_ao_leitor_passa": not G(DL.ERRATA_E26),
                            "e25_afirmada_reprova": bool(G("a trava exige que o sistema precisa saber onde está o Nome a cada passo")),
                            "e25_negada_passa": not G("o sistema não precisa reconhecer onde está o Nome a cada passo"),
                            "tokens_da_v409_reprovam": all(G("veredito " + t_) for t_ in ("TURING_SOLVED", "CLAY_SOLVED", "MILLENNIUM", "P_EQUALS_NP")),
                            "relacao_sem_peso_afirmada_reprova": bool(G(json.dumps({"diz": ["x", "a cadeia: há relação sem peso"]}, ensure_ascii=False))),
                            "p_igual_NP_provado_reprova": bool(G("dizem que P = NP está provado por isto"))}
    r["ok"] = bool(all(r["proibidas"].values()) and not any(r["limpas"].values()) and not r["fala_do_operador"]["com_a_excecao"] and r["fala_do_operador"]["sem_a_excecao"] and all(r["pedras_controle"].values()))
    return r


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    c = controle_negativo()
    c["pedras"] = pedras(); c["pedras_limpas"] = not any(v_["violacoes"] for v_ in c["pedras"].values())
    if not c["pedras_limpas"]:
        print("FRASE DE PEDRA REPROVADA (apontar a gerencia, nao corrigir):", {k_: v_["violacoes"][:3] for k_, v_ in c["pedras"].items() if v_["violacoes"]})
    if not c["ok"]:
        print("CONTROLE NEGATIVO FALHOU:", {"proibidas_que_passaram": [k_ for k_, v_ in c["proibidas"].items() if not v_], "limpas_reprovadas": {k_: v_ for k_, v_ in c["limpas"].items() if v_}, "fala": c["fala_do_operador"], "pedras_controle": {k_: v_ for k_, v_ in c["pedras_controle"].items() if not v_}})
    b_ = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
    open(os.path.join(HERE, "GUARDA_FRASES_v409.json.tmp"), "wb").write(b_); os.replace(os.path.join(HERE, "GUARDA_FRASES_v409.json.tmp"), os.path.join(HERE, "GUARDA_FRASES_v409.json"))
    print("controle negativo:", "PASSOU" if c["ok"] else "FALHOU", "| proibidas reprovadas: %d de %d | limpas aceitas: %d de %d" % (sum(1 for v in c["proibidas"].values() if v), len(c["proibidas"]), sum(1 for v in c["limpas"].values() if not v), len(c["limpas"])))
    print("pedras:", "LIMPAS" if c["pedras_limpas"] else "REPROVADAS", "| falas retiradas:", sum(v_["falas_retiradas"] for v_ in c["pedras"].values()))
    rc = 0 if (c["ok"] and c["pedras_limpas"]) else 1
    for p in sys.argv[1:]:
        v = violacoes(open(p, encoding="utf-8").read())
        print(p, "->", "LIMPO" if not v else v[:6])
        rc |= bool(v)
    sys.exit(rc)

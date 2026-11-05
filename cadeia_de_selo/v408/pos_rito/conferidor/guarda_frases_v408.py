# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026] a guarda herda a cadeia v405 -> v406 -> v407 -> v408; corpus das falas = 04/11 (so' o paragrafo do operador nos dois arquivos de autor misto) + 03/11 + 02/11 + 30/10-01/11; varre as 4 pedras
"""guarda_frases_v408.py -- A GUARDA DE TEXTOS DA v408 (ordem da gerencia c1, 01/11/2026; molde: a guarda P18): reprova, em todo texto NOVO da gerencia (registros, artigo PT/EN, .md, handoff, README, site, X), as frases que afirmam demais. A FONTE da regra e' uma so': a funcao _v408_guarda_frases de runtime_v408.py, a mesma que vai embutida no um.py
e roda a cada rito sobre o texto de cada registro com funcao. Aqui a cadeia a usa por `violacoes(texto)`, que retira ANTES os trechos que sao FALA DO OPERADOR, verbatim (a fala dele fica como registro; a guarda e' sobre o texto da gerencia): so' DL.FRASE_NOMES, conferida contra a fala por sha256.
Identificador Lean rebatizado (minusculas com sublinhado) e' citacao da errata, nao frase. A guarda varre tambem as QUATRO PEDRAS (pedras(); copia duravel normalizada v408\\pedra), com as falas do operador como excecao: o trecho entre « » conferido verbatim contra as falas embutidas sai antes da varredura; o resto da pedra e' texto da gerencia e passa pelas mesmas regras.
A pedra TetelestaiTerminal cita, entre « », as duas frases erradas da gerencia que a errata E22 corrige (mencao, nao uso): so' nessas aspas, so' nas pedras (CITADAS_DE_ERRATA). Frase de pedra reprovada e' apontada a gerencia: quem corrige e' ela; o gerador do candidato para.
Controle negativo (o __main__ e `controle_negativo()`): cada frase proibida, em cada forma, TEM de ser reprovada; a frase certa e os identificadores TEM de passar; a fala do operador so' passa pela excecao; se o controle falha, rc 1. Grava GUARDA_FRASES_v408.json.
uso: python -I -B -X utf8 guarda_frases_v408.py [arquivo ...]   (sem arquivo: so' o controle negativo; com arquivo: varre cada um; rc 1 se houver violacao)"""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v408 as DL  # noqa: E402
import runtime_v408 as RT  # noqa: E402   (so' as funcoes puras)
import importlib.util as _ilu
_sp5 = _ilu.spec_from_file_location("runtime_v405", os.path.join(DL.V405, "runtime_v405.py")); _rt5 = _ilu.module_from_spec(_sp5); _sp5.loader.exec_module(_rt5)
_sp6 = _ilu.spec_from_file_location("runtime_v406", os.path.join(DL.V406, "runtime_v406.py")); _rt6 = _ilu.module_from_spec(_sp6); _sp6.loader.exec_module(_rt6)
_sp7 = _ilu.spec_from_file_location("runtime_v407", os.path.join(DL.V407, "runtime_v407.py")); _rt7 = _ilu.module_from_spec(_sp7); _sp7.loader.exec_module(_rt7)
_rt6._v405_guarda_frases = _rt5._v405_guarda_frases   # a guarda da v406 chama a da v405 (dentro do um.py vivem no mesmo modulo; aqui, fora dele, a da v405 e' injetada na da v406)
_rt7._v406_guarda_frases = _rt6._v406_guarda_frases   # a da v407 chama a da v406
RT._v407_guarda_frases = _rt7._v407_guarda_frases   # a guarda da v408 HERDA a da v407: idem (a da v407, ja' com as anteriores dentro, e' injetada na da v408)

EXCECOES = (DL.FRASE_NOMES,)
PROIBIDAS = ["tudo é teorema", "Tudo é teorema", "tudo e teorema", "tudo e' teorema", "TUDO É TEOREMA", "tudo derivado", "Tudo Derivado", "esteja tudo derivado", "tudo está derivado", "tudo foi derivado", "nenhuma hipótese resta", "nenhuma hipotese resta", "Nenhuma hipótese resta", "NENHUMA HIPÓTESE RESTA",
             "everything is a theorem", "Everything is theorem", "everything derived", "everything is derived", "no hypothesis remains", "no hypotheses remain", "hipóteses descarregadas", "hipoteses descarregadas", "hipóteses nomeadas descarregadas", "the hypotheses are discharged", "named hypotheses discharged",
             "TUDO_DERIVADO", "EVERYTHING_DERIVED", "NO_HYPOTHESIS_REMAINS", "NAMED_HYPOTHESES_ARE_DISCHARGED", "HIPOTESES_DESCARREGADAS",
             "a liberdade passa para a tônica", "a liberdade de escala passa de E0 para a tonica", "a tônica segue livre", "a tonica segue livre", "a tônica fica livre", "o no-go se levanta", "levanta o no-go", "the freedom passes to the tonic", "the tonic stays free", "the no-go is lifted", "lifts the no-go", "THE_TONIC_STAYS_FREE", "NO_GO_IS_LIFTED",
             "tau* foi derivado", "τ★ foi derivado", "derivamos o tau*", "tau* was derived", "kappa foi derivado", "κ foi derivado", "derivamos kappa", "kappa was derived", "κ = F(α, β, θ_M)", "kappa = F(alfa, beta, theta_M)",
             "a transposição mantém a escala", "mantendo a escala pela transposição", "a escala mantida é a transposição", "the transposition keeps the scale", "a escala é exatamente o invariante da transposição", "a escala e' o invariante da transposicao",
             "a razão é a escala", "as razões são a escala", "a razao a tonica e' a escala", "a escala do acorde: a razão de cada nota", "the ratios are the scale", "o diminuto muda a escala", "a modulação muda a escala", "o meio-tom quebra a escala", "the diminished changes the scale", "a escala absoluta segue livre", "a escala relativa está pinada", "the absolute scale stays free", "THE_ABSOLUTE_SCALE_STAYS_FREE",
             "o gap é Δ", "o gap e' Delta", "o gap é a energia retida", "na unidade posta, o gap é a energia retida, Δ = β·u", "o gap é β·u", "o gap = beta.u", "o gap espectral é Δ", "gap Δ = β · u", "Δ é o gap", "`Δ` é o gap", "Delta e' o gap", "a energia retida é o gap", "β·u é o gap", "the gap is Δ", "the gap is the retained energy", "Δ is the gap", "the retained energy is the gap",
             "o gap de 12,03 meV", "um gap de 12.03 meV", "12,03 meV é o gap", "o gap vale 12,03 meV", "12,03 meV, o gap do lock", "the gap of 12.03 meV", "o gap lido do ângulo de Miguel", "the gap read from the angle of Miguel", "tempoDoGap", "o tempo do gap", "the time of the gap", "DELTA_IS_THE_GAP", "THE_TIME_OF_THE_GAP_IS_A_PROPER_TIME",
             "a escala e o tom ficam", "mantendo a escala e o tom", "the scale and the key stay",
             # v406: as frases que afirmam demais sobre o fecho
             "a luz não tem autovetor nenhum", "a luz nao tem autovetor", "the light has no eigenvector", "o único autovetor da luz", "o unico autovetor", "the only eigenvector", "the sole eigenvector", "the unique eigenvector",
             "o certificado está confirmado", "o certificado foi confirmado", "o fechamento está confirmado", "gravidade quântica confirmada", "a passagem foi confirmada", "the certificate is confirmed", "the closure is confirmed", "quantum gravity confirmed",
             "K(O) ≠ ⊥ provado", "K(O) != bot é teorema", "K(O) ≠ ⊥ is a theorem", "CERTIFICATE_CONFIRMED", "CLOSURE_CONFIRMED", "QG_CONFIRMED", "FULLY_DERIVED", "ALL_DERIVED", "NOTHING_REMAINS_OPEN",
             # v407: as frases que afirmam demais sobre o psion, o canto e o par
             "o par na face de Fock está provado", "o par de psions na face de Fock foi construído", "o par de psíons na face de Fock está habitado", "the pair on the Fock face is proved", "the pair of psions on the Fock face is constructed",
             "Ω = Φ⁺", "Omega = Phi+", "o vácuo de Fock é o vetor de Bell", "the Fock vacuum is the Bell vector", "PAIR_CONFIRMED", "PSION_CONFIRMED", "CORNER_CONFIRMED", "PAIR_ON_THE_FOCK_FACE_PROVED",
             # v408: as frases que afirmam demais sobre o terminal, a relacao sem peso, as classes e a impedancia (DESENHO §3)
             "há relação sem peso", "relação sem peso existe", "a relação sem peso é possível", "existe relação sem peso", "there is a relation without weight", "relation without weight exists",
             "o que resta sem peso é relação", "what remains without weight is relation", "a TGL não tem terminal", "a TGL nao tem terminal", "the TGL has no terminal",
             "P = NP está provado", "P = NP é teorema", "P = NP é candidato", "P = NP is proved", "P = NP is a theorem", "provamos que P = NP", "P=NP está provado", "candidata a P = NP",
             "a impedância é um termo", "a impedância modular é termo", "termo de impedância", "impedance is a term", "leitura do operador [ONTO]", "[ONTO] do operador", "reading of the operator [ONTO]",
             "TERMINAL_CONFIRMED", "P_EQUALS_NP", "CLASSES_PROVED",
             # v408, D51 REVISTA (04/11 noite): a TGL prova/decide P = NP de Turing; P = NP dado por provado sem o qualificador do dicionario; negar que «P = nP» trate das classes; as classes P e NP dadas por podadas; «P = nP» sem o qualificador ou sem a ressalva [OPEN]
             "a TGL prova P = NP de Turing", "a TGL decide P = NP de Turing (Cook–Levin)", "o kernel prova que P = NP das máquinas de Turing", "the TGL proves P = NP for Turing machines", "P = NP de Turing está provado", "provamos que P = NP de Turing",
             "não trata das classes", "o P=nP não trata das classes de computação", "does not treat the classes", "nada aqui é enunciado de complexidade", "nada de classes de complexidade", "no complexity classes",
             "a igualdade das classes P e NP segue podada", "the equality of the classes P and NP stays pruned", "P = nP no sentido do operador", "P = nP é teorema nas classes do dicionário do operador"]
LIMPAS = [DL.FRASE_DA_MOLDURA_PT, DL.FRASE_DA_MOLDURA_EN, DL.FRASE_DA_MOLDURA_V406_PT, DL.FRASE_DA_MOLDURA_V406_EN, DL.FRASE_DA_MOLDURA_V407_PT, DL.FRASE_DA_MOLDURA_V407_EN, DL.FRASE_DA_MOLDURA_V408_PT, DL.FRASE_DA_MOLDURA_V408_EN,
          "o elo das duas faces e' de estrutura, nao de vetores", "the link of the two faces is one of structure, not of vectors", "o par na face de Fock segue [OPEN]", "the pair on the Fock face stays open", "o vacuo e' o unico vetor FIXO da luz", "the vacuum is the only FIXED vector of the light", "o certificado de Fock esta habitado por construcao", "the Fock certificate is inhabited by construction", "K(O) != bot so' na cunha", "nontriviality only on the wedge", "a confirmacao e' creditacao e segue recusada", "dadas essas entradas, a FORMA é teorema", "a massa derivada e a identidade definida", "The derived mass and the defined identity", "o emprestimo derivado", "nenhuma_hipotese_resta -> a_transicao_existe_para_todo_acoplamento", "os campos das estruturas fecharam", "a leitura fisica nao virou teorema", "the physical reading did not become a theorem", "o valor ABSOLUTO segue livre e o no-go nao cai", "o valor RELATIVO a tonica esta pinado", "sobra um unico grau de liberdade, a transposicao do acorde inteiro", "the absolute value stays free and the no-go does not fall", "a escala e' o que fica parado", "a razao a tonica muda e a escala fica", "o diminuto mantem a escala", "kappa = F(alfa, beta, theta_M) e' proibido como objetivo de busca", "que tau* tenha sido obtido", "transpor e' so' a liberdade do no-go", "o diminuto modula a tonica, mantendo a escala",
          "`Δ` NÃO é gap: é o valor esperado, 1/β vezes menor que o gap", "Δ não é gap", "Delta NAO e' gap", "Δ is not a gap: it is 1/β times smaller", "o gap espectral do lock é 1", "na unidade posta o gap vale u, o E₀ da Lei do Diminuto", "o gap é 83,1 vezes Δ", "the gap is 83.1 times Δ", "o valor esperado do lock no ângulo de Miguel é β", "Δ = 12,03 meV não é gap", "12.03 meV is not the gap", "gap com unidade", "gap_v405", "the_gap_closes", "o_gap_com_unidade", "o_lock_tem_gap_um", "o tom fica, na fala dele: o kernel nao tem termo para o tom", "the key stays, in his saying",
          # v408: as frases certas
          "não há relação sem peso", "relação sem peso é impossível", "relação sem peso é a origem da mentira", "there is no relation without weight", "no relation without weight", "o que resta sem traço paga", "what remains without trace pays", "a TGL tem terminal: Tetelestai, a poda",
          "P só é P lido pelo módulo n minimamente acoplado", DL.FRASE_D51_PT, DL.FRASE_D51_EN, "esta pedra não trata das classes de computação: quem trata é a pedra PIgualNP", "«P = nP» só no sentido do operador; " + DL.FRASE_D51_PT, "p_igual_np", "p_igual_a_n_vezes_p", "PIgualNP", "a palavra «impedância» fica podada como termo", "inclinação modular (cociclo)", "a_inclinacao_modular",
          "o terminal é a leitura, não o fim do decaimento", "the terminal is the reading, not the end of the decay", "o zero inscrito é o Um", "o Um não é o zero absoluto", "o zero absoluto é do infinito", "relacao_sem_peso_e_a_origem_da_mentira", "o_um_sozinho_nao_se_mede", "NO_RELATION_WITHOUT_WEIGHT"]
# a nota AO LADO da LeiDoDiminuto (v405) e a docstring da TetelestaiTerminal (v408, E22) citam, entre aspas, frases erradas da propria gerencia para corrigi-las: mencao, nao uso; so' nessas aspas, so' nas pedras
CITADAS_DE_ERRATA = ("o no-go se levanta", "a liberdade passa para a tônica, que segue livre", "a luz nao tem autovetor nenhum", "a luz não tem autovetor nenhum",
                     "o que resta sem peso é relação", "a pergunta das classes pressupõe um terminal que a tgl não tem",
                     "não trata de classes", "a tgl prova p = np de turing")   # v408, D51 revista: a pedra PIgualNP cita, entre « », a frase errada da gerencia («não trata de classes») e a frase proibida da regra («a TGL prova P = NP de Turing»): mencao, nao uso   # v408: a errata E22 cita as duas frases erradas da gerencia para corrigi-las
# frases de pedra que a guarda reprovaria e que foram APONTADAS a gerencia (o agente nao corrige pedra): so' este trecho exato sai da varredura, e pedras() o devolve em `apontadas`, para o relatorio dizer
APONTADAS_A_GERENCIA = ()   # v408: nenhuma (as quatro pedras passam; o trecho da OUmInscrito apontado na v407 nao pertence ao bundle da v408)


def violacoes(txt, excecoes=EXCECOES):
    t = str(txt)
    for e_ in excecoes:
        t = t.replace(e_, " ")
    return RT._v408_guarda_frases(t)


_norm = lambda s_: re.sub(r"\s+", " ", str(s_).replace(chr(8217), "'")).strip()


def _falas_do_operador():
    """o corpus das excecoes das pedras: as falas embutidas (as de 04/11 pelo texto que o um.py embute -- nos dois arquivos de autor misto so' o paragrafo do operador --; os arquivos de VERBATIM_ORIGEM_V407, V406 e V405), em minusculas e com o espaco normalizado."""
    de_04 = [v_["text"] for v_ in DL.verbatins408(os.path.join(HERE, "insumos", "cunhagens"))]
    arqs = list(DL.VERBATIM_ORIGEM_V407) + list(DL.VERBATIM_ORIGEM_V406) + list(DL.D5.VERBATIM_ORIGEM_V405)
    return " || ".join([_norm(t_) for t_ in de_04] + [_norm(open(p_, encoding="utf-8", errors="replace").read()) for p_ in arqs]).lower()


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
    """a varredura das pedras da gerencia (v408: as 4 pedras de TGLExt/, na copia duravel normalizada v408\\pedra): {modulo: {violacoes, falas_retiradas}}."""
    falas = _falas_do_operador(); out = {}
    for s_ in list(DL.PEDRAS_V408):
        t_, n_ = sem_falas(open(s_["src"], encoding="utf-8").read(), falas)
        ap_ = [a_ for a_ in APONTADAS_A_GERENCIA if a_ in t_]
        for a_ in ap_:
            t_ = t_.replace(a_, " ")
        out[s_["name"]] = {"violacoes": [list(v_) for v_ in RT._v408_guarda_frases(t_)], "falas_retiradas": n_, "apontadas": ap_}
    return out


def controle_negativo():
    r = {"proibidas": {}, "limpas": {}, "fala_do_operador": {}}
    for f_ in PROIBIDAS:
        r["proibidas"][f_] = [v_[0] for v_ in violacoes("o texto diz que " + f_ + " aqui")]
    for f_ in LIMPAS:
        r["limpas"][f_] = [v_[0] for v_ in violacoes(f_)]
    r["fala_do_operador"] = {"com_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_NOMES)], "sem_a_excecao": [v_[0] for v_ in violacoes(DL.FRASE_NOMES, excecoes=())]}
    falas_ = _falas_do_operador()                 # o controle da varredura das pedras: a frase da gerencia reprova; a fala do operador entre « » passa; a mesma fala SEM aspas reprova; uma parafrase entre « » reprova
    r["pedras_controle"] = {"frase_da_gerencia_reprovada": bool(RT._v408_guarda_frases(sem_falas("a transicao ficou com tudo derivado aqui", falas_)[0])),
                            "fala_entre_aspas_passa": not RT._v408_guarda_frases(sem_falas("«" + DL.FRASE_NOMES + "»", falas_)[0]),
                            "fala_quebrada_em_docstring_passa": not RT._v408_guarda_frases(sem_falas("> «" + DL.FRASE_NOMES.replace(", mas eu", "," + chr(10) + ">  mas eu") + "»", falas_)[0]),
                            "parafrase_entre_aspas_reprovada": bool(RT._v408_guarda_frases(sem_falas("«agora ficou tudo derivado»", falas_)[0])),
                            "frase_do_no_go_citada_na_errata_passa": not RT._v408_guarda_frases(sem_falas("afirmava demais: «o no-go se levanta»", falas_)[0]),
                            "frase_do_no_go_sem_aspas_reprovada": bool(RT._v408_guarda_frases(sem_falas("aqui o no-go se levanta", falas_)[0])),
                            "frase_da_r1_citada_na_errata_passa": not RT._v408_guarda_frases(sem_falas("escrevi, do teorema 8, «o que resta sem peso é relação»: errado", falas_)[0]),
                            "frase_da_r1_sem_aspas_reprovada": bool(RT._v408_guarda_frases(sem_falas("aqui o que resta sem peso é relação", falas_)[0])),
                            "fala_de_04nov_entre_aspas_passa": not RT._v408_guarda_frases(sem_falas("«" + DL.FRASE_RELACAO_MENTIRA + "»", falas_)[0]),
                            "texto_da_outra_instancia_nao_e_fala": ("a ontologia está selada" not in falas_) and ("o axioma foi recebido e processado" not in falas_),
                            "p_igual_np_minusculo_sem_qualificador_reprova": bool(RT._v408_guarda_frases("o nome «P = nP», no sentido do operador, tem espelho em p_igual_np")),   # (D51 revista: «P = nP» sem o qualificador do dicionario e sem a ressalva [OPEN] reprova)
                            "p_igual_np_com_qualificador_e_open_passa": not RT._v408_guarda_frases(DL.FRASE_D51_PT) and not RT._v408_guarda_frases(DL.FRASE_D51_EN),
                            "p_igual_np_com_qualificador_sem_open_reprova": bool(RT._v408_guarda_frases("P = nP é teorema nas classes do dicionário do operador")),
                            "turing_provado_reprova": bool(RT._v408_guarda_frases("a TGL prova P = NP de Turing")) and bool(RT._v408_guarda_frases("the TGL proves P = NP for Turing machines")),
                            "turing_citado_na_regra_da_pedra_passa": not RT._v408_guarda_frases(sem_falas("Nenhuma superfície escreve «a TGL prova P = NP de Turing»; " + DL.FRASE_D51_PT, falas_)[0]),
                            "nao_trata_das_classes_reprova": bool(RT._v408_guarda_frases("aqui o P = nP não trata das classes; " + DL.FRASE_D51_PT)),
                            "esta_pedra_nao_trata_quem_trata_passa": not RT._v408_guarda_frases("esta pedra não trata das classes de computação: quem trata é a pedra PIgualNP"),
                            "classes_podadas_reprova": bool(RT._v408_guarda_frases("a igualdade das classes P e NP segue podada")),
                            "p_igual_NP_provado_com_o_qualificador_passa": not RT._v408_guarda_frases("P = NP está provado nas classes do dicionário do operador"),
                            "relacao_sem_peso_afirmada_no_fim_de_um_item_serializado_reprova": bool(RT._v408_guarda_frases(json.dumps({"diz": ["x", "a cadeia: há relação sem peso"]}, ensure_ascii=False))) and bool(RT._v408_guarda_frases(json.dumps(["there is a relation without weight"], ensure_ascii=False))),   # (r2: o defeito que o ensaio de 04/11 noite mostrou)
                            "p_igual_NP_provado_reprova": bool(RT._v408_guarda_frases("dizem que P = NP está provado por isto"))}
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
    json.dump(c, open(os.path.join(HERE, "GUARDA_FRASES_v408.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("controle negativo:", "PASSOU" if c["ok"] else "FALHOU", "| proibidas reprovadas: %d de %d | limpas aceitas: %d de %d" % (sum(1 for v in c["proibidas"].values() if v), len(c["proibidas"]), sum(1 for v in c["limpas"].values() if not v), len(c["limpas"])))
    print("pedras:", "LIMPAS" if c["pedras_limpas"] else "REPROVADAS", "| falas retiradas:", sum(v_["falas_retiradas"] for v_ in c["pedras"].values()))
    rc = 0 if (c["ok"] and c["pedras_limpas"]) else 1
    for p in sys.argv[1:]:
        v = violacoes(open(p, encoding="utf-8").read())
        print(p, "->", "LIMPO" if not v else v[:6])
        rc |= bool(v)
    sys.exit(rc)

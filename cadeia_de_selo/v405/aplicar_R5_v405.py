# -*- coding: utf-8 -*-
"""aplicar_R5_v405.py -- a errata R5 da gerencia c1 (18:56 de 01/11/2026): a escala e' o que fica parado; a escala de energia do no-go chama-se valor absoluto, e a outra, valor relativo a tonica. Textos, registros, runtime, guardas e nomes rebatizados. Contagem exata por substituicao; tudo ou nada; backup de BYTES. Roda uma vez so'."""
import os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = time.strftime("%Y%m%d_%H%M%S")
NOVOS = {}


def carrega(arq):
    if arq not in NOVOS:
        NOVOS[arq] = open(os.path.join(HERE, arq), "rb").read().decode("utf-8")
    return NOVOS[arq]


def sub(arq, old, new, n=1):
    s = carrega(arq); c = s.count(old)
    assert c == n, (arq, c, n, old[:100])
    NOVOS[arq] = s.replace(old, new)


def todos(arq, old, new):
    """substitui todas as ocorrencias; exige ao menos uma."""
    s = carrega(arq); c = s.count(old)
    assert c >= 1, (arq, old[:100])
    NOVOS[arq] = s.replace(old, new)


X = os.path.join("pos_rito", "textos_v405_novo.pysnip"); M = os.path.join("pos_rito", "registrar_mapa_v405_montar.pysnip")
D = "delta_v405.py"; R = "registros_v405.py"; T = "runtime_v405.py"; P = "artigo_pt_v405.pysnip"; E = "artigo_en_v405.pysnip"; Y = "gerar_candidato_v405.py"; Z = "gerar_relatorio_v405.py"; G = "guarda_frases_v405.py"; D3 = "derivar_encanamento_v405_regrasD3_diff_citacoes.py"; C2 = "derivar_encanamento_v405_regrasC2_ensaio.py"; E1 = "derivar_encanamento_v405_regrasE1_p00.py"; F = "fechar_preparacao_v405.py"

# ---------------------------------------------------------------- os dois nomes rebatizados, em todo texto
for a in (R, T, P, E, X):
    todos(a, "mesma_escala_iff_transposicao".replace("_", "\\_") if a in (P, E) else "mesma_escala_iff_transposicao", "mesmas_razoes_iff_transposicao".replace("_", "\\_") if a in (P, E) else "mesmas_razoes_iff_transposicao") if carrega(a).count("mesma_escala_iff_transposicao".replace("_", "\\_") if a in (P, E) else "mesma_escala_iff_transposicao") else None
for a in (R, T):
    todos(a, "a_escala_nao_fixa_o_absoluto", "as_razoes_nao_fixam_o_absoluto")
sub(Z, "o nome de teorema mesma_escala_iff_transposicao (da R3) fica no kernel, mas diz mesmas razoes; os textos o citam so' com esse sentido e nunca ligam mantendo a escala a transpor: o nome e' decisao da gerencia", "os nomes de teorema the_scale_is_free, the_scale_is_the_invariant e no_positive_scale_invariant ficam, nomes assentados; no texto se diz valor absoluto")

# ---------------------------------------------------------------- delta
sub(D, "(a forma nao fixa a escala; o no-go NAO cai, ele se localiza no Um posto)", "(a forma nao fixa o valor absoluto; o no-go NAO cai, ele se localiza no Um posto)")
sub(D, "Vigente: a escala ABSOLUTA segue livre e o no-go nao cai; a escala RELATIVA esta pinada; sobra um unico grau de liberdade global, a transposicao do acorde inteiro; o meio-tom pinado quebra", "Vigente: a escala e' o que fica parado, as notas sustentadas e as razoes entre elas, e quem se move e' a tonica; o valor ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a tonica esta pinado; sobra um unico grau de liberdade global, a transposicao do acorde inteiro; o meio-tom pinado quebra")
todos(D, "a escolha dimensional de uma escala so'", "a escolha dimensional de uma unidade so'")
sub(D, "so' ela desce o meio-tom pinado, as demais notas ficam sustentadas, a escala e o tom ficam; E0 e' o valor da tonica modulada;", "so' ela desce o meio-tom pinado, as demais notas ficam sustentadas, a escala e o tom ficam: a escala e' o que fica parado, e a razao a tonica muda; E0 e' o valor da tonica modulada;")
sub(D, "as demais notas ficam sustentadas, a escala e o tom ficam (modular, modular_sustenta, modular_nao_e_transposicao);", "as demais notas ficam sustentadas, a escala e o tom ficam (modular, modular_sustenta, modular_mantem_a_escala, modular_nao_e_transposicao);")

# ---------------------------------------------------------------- registros
todos(R, "a escala ABSOLUTA segue livre e o no-go nao cai; a escala RELATIVA esta pinada", "o valor ABSOLUTO segue livre e o no-go nao cai; o valor RELATIVO a tonica esta pinado")
sub(R, "que o no-go tenha caido: a escala ABSOLUTA segue livre; so' a RELATIVA esta pinada", "que o no-go tenha caido: o valor ABSOLUTO segue livre; so' o RELATIVO a tonica esta pinado")
sub(R, "que a escala tenha sido escolhida pelo dado (nem 1,02 eV nem outra)", "que o valor absoluto tenha sido escolhido pelo dado (nem 1,02 eV nem outro)")
sub(R, "(1) a liberdade de escala: a transicao reescalada (E0 -> lambda.E0, a mesma inscricao) e' transicao; a massa derivada escala linearmente;", "(1) a liberdade do valor absoluto: a transicao reescalada (E0 -> lambda.E0, a mesma inscricao) e' transicao; a massa derivada cresce linearmente;")
sub(R, "a reescala e' a transposicao do acorde, a liberdade do no-go, que fala da escala ABSOLUTA; a Lei do diminuto fala da RELATIVA;", "a reescala e' a transposicao do acorde, a liberdade do no-go, que fala do valor ABSOLUTO; a Lei do diminuto fala do valor RELATIVO a tonica;")
sub(R, "a massa escala linearmente com E0 (quatro lambdas)", "a massa cresce linearmente com E0 (quatro lambdas)")
sub(R, "que a rota do monopolo fixe a escala (e' tautologica)", "que a rota do monopolo fixe o valor absoluto (e' tautologica)")
sub(R, "que a escala tenha sido escolhida pelo dado", "que o valor absoluto tenha sido escolhido pelo dado")
sub(R, "o no-go fala da escala ABSOLUTA; a Lei do diminuto, da RELATIVA", "o no-go fala do valor ABSOLUTO; a Lei do diminuto, do valor RELATIVO a tonica")
sub(R, "o corte E^3 = hbar^2.K (algebra); a escala e' o invariante;", "o corte E^3 = hbar^2.K (algebra); o valor do corte e' dado pelo invariante (the_scale_is_the_invariant);")
sub(R, "o operador le a energia do corte como a ressonancia que permanece e a escala que nasce no infinito;", "o operador le a energia do corte como a ressonancia que permanece e o valor que nasce no infinito;")
todos(R, "a escolha dimensional de uma escala so'", "a escolha dimensional de uma unidade so'")
sub(R, "as outras quatro ficam sustentadas (modular_sustenta); a escala e o tom ficam; nao e' transposicao:", "as outras quatro ficam sustentadas (modular_sustenta); a escala e o tom ficam: a escala e' o que fica parado, as notas sustentadas e as razoes entre elas (modular_mantem_a_escala); a razao a tonica muda, e e' a tonica que se move; nao e' transposicao:")
sub(R, '''"as_duas_escalas": {"absoluta": "segue livre; o no-go nao cai (no_function_of_the_inscription_fixes_E0; as_razoes_nao_fixam_o_absoluto)", "relativa": "pinada (E0_relativo_pinado)",''', '''"os_dois_valores": {"a_escala": "a musical: o que fica parado, as notas sustentadas e as razoes entre elas (modular_mantem_a_escala)", "valor_absoluto": "segue livre; o no-go nao cai (no_function_of_the_inscription_fixes_E0; as_razoes_nao_fixam_o_absoluto)", "valor_relativo_a_tonica": "pinado (E0_relativo_pinado)",''')
sub(R, '''"a_lei": {"o_diminuto": "modular: so' a tonica desce o meio-tom pinado; modular_sustenta: as demais notas ficam; modular_nao_e_transposicao",''', '''"a_lei": {"o_diminuto": "modular: so' a tonica desce o meio-tom pinado; modular_sustenta: as demais notas ficam; modular_mantem_a_escala: as razoes entre as sustentadas nao mudam; modular_nao_e_transposicao",''')
sub(R, "(os 38 teoremas do contrato,", "(os 39 teoremas do contrato,")
sub(R, "os 38 teoremas do contrato e os termos de suporte sao lidos deste kernel", "os 39 teoremas do contrato e os termos de suporte sao lidos deste kernel")
sub(R, "o diminuto e' MODULACAO, nao transposicao: so' a tonica desce o meio-tom pinado, as demais notas ficam sustentadas e nenhum fator leva o acorde ao acorde modulado;", "o diminuto e' MODULACAO, nao transposicao: so' a tonica desce o meio-tom pinado, as demais notas ficam sustentadas, a escala fica (as razoes entre as sustentadas nao mudam) e nenhum fator leva o acorde ao acorde modulado;")
sub(R, "so' a tonica desce e as demais ficam sustentadas; E0/tonica = e^(-1/2);", "so' a tonica desce e as demais ficam sustentadas; as razoes entre as sustentadas nao mudam; E0/tonica = e^(-1/2);")
sub(R, '"que a pentada do teorema mestre sejam cinco autovalores (sao cinco componentes)", "que E0_relativo_pinado', '"que a pentada do teorema mestre sejam cinco autovalores (sao cinco componentes)", "que a razao a tonica seja a escala (a razao a tonica muda; a escala fica)", "que E0_relativo_pinado')
sub(R, "the_diminished_law_closes: only the tonic goes down the half tone, the other notes are sustained, each interval to the tonic opens a half tone,", "the_diminished_law_closes: only the tonic goes down the half tone, the other notes are sustained, the ratios among them do not change, each interval to the tonic opens a half tone,")
sub(R, "THE_TRANSPOSITION_IS_ONLY_THE_FREEDOM_OF_THE_NO_GO__THE_ABSOLUTE_SCALE_STAYS_FREE_THE_RELATIVE_SCALE_IS_PINNED__", "THE_SCALE_IS_WHAT_STAYS_THE_SUSTAINED_NOTES_AND_THE_RATIOS_AMONG_THEM__THE_TRANSPOSITION_IS_ONLY_THE_FREEDOM_OF_THE_NO_GO__THE_ABSOLUTE_VALUE_STAYS_FREE_THE_VALUE_RELATIVE_TO_THE_TONIC_IS_PINNED__")
sub(R, "THE_CUT_E_CUBED_EQUALS_HBAR2_K__THE_SCALE_IS_THE_INVARIANT_THE_WALL_IS_NAMED_NOT_DERIVED__", "THE_CUT_E_CUBED_EQUALS_HBAR2_K__THE_VALUE_OF_THE_CUT_IS_GIVEN_BY_THE_INVARIANT_THE_WALL_IS_NAMED_NOT_DERIVED__")

# ---------------------------------------------------------------- runtime
todos(T, "a escolha dimensional de uma escala so'", "a escolha dimensional de uma unidade so'")
sub(T, "a escala ABSOLUTA segue livre e a RELATIVA esta pinada; sobra um unico grau de liberdade global,", "o valor ABSOLUTO segue livre e o RELATIVO a tonica esta pinado; sobra um unico grau de liberdade global,")
sub(T, '"""v405 -- a mecanica da TONICA DO HAMILTONIANO: a liberdade de escala da forma (a massa escala linearmente com E0;', '"""v405 -- a mecanica da TONICA DO HAMILTONIANO: a liberdade do valor absoluto na forma (a massa cresce linearmente com E0;')
sub(T, "a forma e' homogenea de grau 1 em E0 e a escala e' livre\",", "a forma e' homogenea de grau 1 em E0 e o valor absoluto e' livre\",")
sub(T, "(igual nas duas a 1e-15 relativo); a escala e' um dado a mais -- aqui, o Um POSTO\",", "(igual nas duas a 1e-15 relativo); o valor absoluto e' um dado a mais -- aqui, o Um POSTO\",")
sub(T, "e' tautologica quanto a ESCALA, nao a fixa", "e' tautologica quanto ao valor absoluto, nao o fixa")
sub(T, "o no-go fala da escala ABSOLUTA; a Lei do diminuto, da RELATIVA", "o no-go fala do valor ABSOLUTO; a Lei do diminuto, do valor RELATIVO a tonica")
sub(T, "o no-go (a forma nao fixa E0: a escala e' livre,", "o no-go (a forma nao fixa E0: o valor absoluto e' livre,")
sub(T, '''("F5_token_de_veredito", _re.compile(''', '''("F10_a_razao_nao_e_a_escala", _re.compile(r"\\\\braz(?:ã|a)o(?:es|ões)?(?:\\\\s+[àa]\\\\s+t(?:ô|o)nica)?\\\\s+(?:e'|é|sao|são)\\\\s+(?:a\\\\s+)?escala\\\\b|\\\\ba\\\\s+escala\\\\s+(?:do\\\\s+acorde\\\\s*)?(?:e'|é|:)\\\\s+(?:a\\\\s+|as\\\\s+)?raz(?:ã|a)(?:o|es|ões)\\\\s+(?:de\\\\s+cada|[àa]\\\\s+(?:t(?:ô|o)nica|nota\\\\s+principal))|\\\\bthe\\\\s+ratios?\\\\s+(?:is|are)\\\\s+the\\\\s+scale\\\\b", _re.I)),
               ("F11_o_diminuto_nao_muda_a_escala", _re.compile(r"\\\\b(?:o\\\\s+diminuto|a\\\\s+modula(?:ç|c)(?:ã|a)o|o\\\\s+mei[oa]-tom)\\\\s+(?:muda|altera|quebra|desloca)\\\\s+(?:toda\\\\s+)?a\\\\s+escala\\\\b|\\\\bthe\\\\s+(?:diminished|modulation|half\\\\s+tone)\\\\s+(?:changes|alters|breaks|shifts)\\\\s+the\\\\s+scale\\\\b", _re.I)),
               ("F12_valor_absoluto_nao_e_escala", _re.compile(r"\\\\bescalas?\\\\s+(?:absoluta|relativa)s?\\\\b|\\\\b(?:absolute|relative)\\\\s+scales?\\\\b", _re.I)),
               ("F5_token_de_veredito", _re.compile('''.replace("\\\\\\\\", "\\\\"))
sub(T, "|THE_TONIC_(?:STAYS|REMAINS)_FREE|NO_GO_(?:IS_)?LIFTED", "|THE_TONIC_(?:STAYS|REMAINS)_FREE|NO_GO_(?:IS_)?LIFTED|(?:ABSOLUTE|RELATIVE)_SCALE")
sub(T, '''    ck_("d7", "★★★ modular_tonica, modular_sustenta e lerE0_e_a_tonica_modulada (O DIMINUTO MODULA A TONICA): num acorde de TESTE so' a nota principal desce o meio-tom (|erro| <= 1e-15 relativo), as outras quatro ficam sustentadas (iguais bit a bit), e E0 e' o valor da tonica modulada;''', '''    ck_("d7", "★★★ modular_tonica, modular_sustenta, modular_mantem_a_escala e lerE0_e_a_tonica_modulada (O DIMINUTO MODULA A TONICA): num acorde de TESTE so' a nota principal desce o meio-tom (|erro| <= 1e-15 relativo), as outras quatro ficam sustentadas (iguais bit a bit), as razoes entre elas nao mudam: a escala e' o que fica parado; e E0 e' o valor da tonica modulada;''')
sub(T, '''_v405_rel(mod_[0], meio_ * acorde_[0]) <= 1e-15 and mod_[1:] == acorde_[1:] and ler_(acorde_) == mod_[0], [mod_[0]])''', '''_v405_rel(mod_[0], meio_ * acorde_[0]) <= 1e-15 and mod_[1:] == acorde_[1:] and all(mod_[i_] / mod_[j_] == acorde_[i_] / acorde_[j_] for i_ in range(1, 5) for j_ in range(1, 5)) and ler_(acorde_) == mod_[0], [mod_[0]])''')

# ---------------------------------------------------------------- guarda
sub(G, '''"a escala ABSOLUTA segue livre e o no-go nao cai", "a escala RELATIVA esta pinada", "sobra um unico grau de liberdade, a transposicao do acorde inteiro", "the absolute scale stays free and the no-go does not fall",''', '''"o valor ABSOLUTO segue livre e o no-go nao cai", "o valor RELATIVO a tonica esta pinado", "sobra um unico grau de liberdade, a transposicao do acorde inteiro", "the absolute value stays free and the no-go does not fall", "a escala e' o que fica parado", "a razao a tonica muda e a escala fica", "o diminuto mantem a escala",''')
sub(G, '''"a escala é exatamente o invariante da transposição", "a escala e' o invariante da transposicao"]''', '''"a escala é exatamente o invariante da transposição", "a escala e' o invariante da transposicao",
             "a razão é a escala", "as razões são a escala", "a razao a tonica e' a escala", "a escala do acorde: a razão de cada nota", "the ratios are the scale", "o diminuto muda a escala", "a modulação muda a escala", "o meio-tom quebra a escala", "the diminished changes the scale", "a escala absoluta segue livre", "a escala relativa está pinada", "the absolute scale stays free", "THE_ABSOLUTE_SCALE_STAYS_FREE"]''')
sub(G, '''APONTADAS_A_GERENCIA = ("A ESCALA É EXATAMENTE O INVARIANTE DA TRANSPOSIÇÃO",)''', '''APONTADAS_A_GERENCIA = ()   # (vazia: a errata R5 corrigiu na pedra o que estava apontado)''')
s_ = carrega(D3); i_ = s_.index("_APONTADAS_PEDRAS = {"); j_ = s_.index(chr(10), i_); NOVOS[D3] = s_[:i_] + "_APONTADAS_PEDRAS = {}   # (vazia: a errata R5 corrigiu na pedra o que estava apontado)" + s_[j_:]

# ---------------------------------------------------------------- gerar_candidato
sub(Y, "a escala ABSOLUTA segue livre e a RELATIVA esta pinada;", "o valor ABSOLUTO segue livre e o RELATIVO a tonica esta pinado;")
sub(Y, "a escala absoluta segue livre e a relativa está pinada)", "o valor absoluto segue livre e o relativo à tônica está pinado)")

# ---------------------------------------------------------------- textos do pos-rito
sub(X, '"meioTom_e_a_face", "modular", "modular_sustenta",', '"meioTom_e_a_face", "modular", "modular_sustenta", "modular_mantem_a_escala",')
sub(X, "as demais notas ficam sustentadas (`modular_sustenta`), a escala e o tom ficam, e nenhum fator leva", "as demais notas ficam sustentadas (`modular_sustenta`), a escala e o tom ficam (`modular_mantem_a_escala`: a escala é o que fica parado, e a razão à tônica muda), e nenhum fator leva")
sub(X, "a escala ABSOLUTA segue livre; a escala RELATIVA está pinada; sobra um único grau de liberdade global,", "o valor ABSOLUTO segue livre; o valor RELATIVO à tônica está pinado; sobra um único grau de liberdade global,")
todos(X, "a escolha dimensional de uma escala só", "a escolha dimensional de uma unidade só")
sub(X, "que não fixa `u`; a escala absoluta segue livre e a relativa está pinada. \"", "que não fixa `u`; o valor absoluto segue livre e o relativo à tônica está pinado. \"")
sub(X, "`transpor` é só a liberdade do no-go. A escala absoluta segue livre; a escala relativa está pinada; sobra um único grau de liberdade global,", "`transpor` é só a liberdade do no-go. A escala é o que fica parado; o valor absoluto segue livre; o valor relativo à tônica está pinado; sobra um único grau de liberdade global,")
todos(X, "a escala do setor", "o valor absoluto do setor")
sub(M, "a escala absoluta segue livre e a relativa esta pinada;", "o valor absoluto segue livre e o relativo a tonica esta pinado;")

# ---------------------------------------------------------------- artigos
todos(P, "a escolha dimensional de uma escala só", "a escolha dimensional de uma unidade só")
sub(P, r"""as demais ficam sustentadas (\texttt{modular\_sustenta}), a escala e o tom ficam, e nenhum fator leva""", r"""as demais ficam sustentadas (\texttt{modular\_sustenta}), a escala e o tom ficam (\texttt{modular\_mantem\_a\_escala}: a escala é o que fica parado, as notas sustentadas e as razões entre elas; a razão à tônica muda, e é a tônica que se move), e nenhum fator leva""")
sub(P, r"""\textsf{[REAL]} A escala \emph{absoluta} segue livre e o no-go não cai; a escala \emph{relativa} está pinada;""", r"""\textsf{[REAL]} O valor \emph{absoluto} segue livre e o no-go não cai; o valor \emph{relativo} à tônica está pinado;""")
sub(P, r"""Esse no-go \emph{não cai}: ele fala da escala absoluta e se localiza no Um posto.""", r"""Esse no-go \emph{não cai}: ele fala do valor absoluto e se localiza no Um posto.""")
sub(P, "tautológica quanto à escala.", "tautológica quanto ao valor absoluto.")
todos(E, "the dimensional choice of a single scale", "the dimensional choice of a single unit")
sub(E, r"""the other notes are sustained (\texttt{modular\_sustenta}), the scale and the key stay, and no factor takes""", r"""the other notes are sustained (\texttt{modular\_sustenta}), the scale and the key stay (\texttt{modular\_mantem\_a\_escala}: the scale is what stays, the sustained notes and the ratios among them; the ratio to the tonic changes, and it is the tonic that moves), and no factor takes""")
sub(E, r"""\textsf{[REAL]} The \emph{absolute} scale stays free and the no-go does not fall; the \emph{relative} scale is pinned;""", r"""\textsf{[REAL]} The \emph{absolute} value stays free and the no-go does not fall; the value \emph{relative} to the tonic is pinned;""")
sub(E, r"""This no-go \emph{does not fall}: it speaks of the absolute scale and localizes at the posted One.""", r"""This no-go \emph{does not fall}: it speaks of the absolute value and localizes at the posted One.""")
sub(E, "tautological as to the scale.", "tautological as to the absolute value.")

# ---------------------------------------------------------------- lotes e relatorio
s_ = carrega(E1); i_ = s_.index('_rec_r4 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R4_01nov.json"))'); j_ = s_.index('chk("[v405, a lista de exclusao]')
NOVOS[E1] = s_[:i_] + '''_rec_r4 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R4_01nov.json"))
_rec_r5 = lj(os.path.join(HERE, "insumos", "RECIBO_ERRATA_PEDRAS_R5_01nov.json"))
_cad = [(_rec_r5, _rec_r4), (_rec_r4, _rec_r3), (_rec_r3, _rec_r2)]
chk("[v405] as pedras sao as da ERRATA R5 da gerencia: o sha256 de cada arquivo == o sha256_depois do recibo vigente (oito arquivos), e a cadeia de custodia fecha: em R5 -> R4 -> R3 -> R2, antes == depois do recibo anterior (a inalterada: depois == depois) e R2.antes == R1.depois (sete arquivos); os recibos antigos ficam como registro", all(sha(rd(os.path.join(HERE, "pedra", k_ + ".lean"))) == v_["sha256_depois"] for k_, v_ in _rec_r5["pedras"].items()) and len(_rec_r5["pedras"]) == 8 and all(all((n_["pedras"][k_].get("sha256_antes") or n_["pedras"][k_]["sha256_depois"]) == v_["sha256_depois"] for k_, v_ in a_["pedras"].items()) for n_, a_ in _cad) and all(_rec_r2["pedras"][a_["modulo"]]["sha256_antes"] == a_["sha256_depois"] for a_ in _rec_err["arquivos"]) and len(_rec_err["arquivos"]) == 7, len(_rec_r5["pedras"]))
''' + s_[j_:]
sub("copiar_insumos_v405.py", '''(os.path.basename(RG.RECIBO_ERRATA_R4_ARQ), RG.RECIBO_ERRATA_R4_ARQ),''', '''(os.path.basename(RG.RECIBO_ERRATA_R4_ARQ), RG.RECIBO_ERRATA_R4_ARQ), (os.path.basename(RG.RECIBO_ERRATA_R5_ARQ), RG.RECIBO_ERRATA_R5_ARQ),''')
sub(R, '''CHAVE_RECIBO_ERRATA_R4 = "recibo_errata_r4_das_pedras_01nov"
RECIBO_ERRATA_R4_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R4_01nov.json")
''', '''CHAVE_RECIBO_ERRATA_R4 = "recibo_errata_r4_das_pedras_01nov"
RECIBO_ERRATA_R4_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R4_01nov.json")
CHAVE_RECIBO_ERRATA_R5 = "recibo_errata_r5_das_pedras_01nov"
RECIBO_ERRATA_R5_ARQ = os.path.join(DL.ESTUDO_E0, "RECIBO_ERRATA_PEDRAS_R5_01nov.json")
''')
sub(R, '''          {"chave": CHAVE_RECIBO_ERRATA_R4, "arquivo":''', '''          {"chave": CHAVE_RECIBO_ERRATA_R5, "arquivo": os.path.join(INS, os.path.basename(RECIBO_ERRATA_R5_ARQ)), "papel": "o recibo da ERRATA R5 DAS PEDRAS (gerencia c1, 01/11/2026, a escala e' o que fica parado): os oito sha256 vigentes, quatro mudaram; codigo novo na LeiDoDiminuto; o resto e' docstring [DECLARADO na origem; o sha256 de cada pedra e os termos sao conferidos pelo gerador e pelo kernel do rito]"},
          {"chave": CHAVE_RECIBO_ERRATA_R4, "arquivo":''')
sub(R, '''papel": "o recibo da ERRATA R4 DAS PEDRAS (gerencia c1, 01/11/2026, a resposta do operador: o diminuto modula a tonica; o gap): os oito sha256 vigentes, tres mudaram;''', '''papel": "o recibo da ERRATA R4 DAS PEDRAS (gerencia c1, 01/11/2026, a resposta do operador: o diminuto modula a tonica; o gap): oito sha256, tres mudaram;''')
sub(R, '''    cks2.append(CH("n%d" % m, "o recibo da errata R4 das pedras (fonte pinada, a vigente) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R4, ["pedras"], "tamanho_igual", 8)); m += 1
''', '''    cks2.append(CH("n%d" % m, "o recibo da errata R5 das pedras (fonte pinada, a vigente) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R5, ["pedras"], "tamanho_igual", 8)); m += 1
    cks2.append(CH("n%d" % m, "o recibo da errata R4 das pedras (fonte pinada) cobre as oito pedras", "fonte:" + CHAVE_RECIBO_ERRATA_R4, ["pedras"], "tamanho_igual", 8)); m += 1
''')
sub(R, 'CHAVE_RECIBO_ERRATA_R3, CHAVE_RECIBO_ERRATA_R4, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),', 'CHAVE_RECIBO_ERRATA_R3, CHAVE_RECIBO_ERRATA_R4, CHAVE_RECIBO_ERRATA_R5, CHAVE_RECIBO_IDENTIDADE, CHAVE_RECIBO_OBSERVADOR], "verbatins": [CH_DE(N_NOMES),')
sub(R, '''"fontes": [CHAVE_DE_FONTE["psion"], CHAVE_RECIBO_ERRATA_R4], "verbatins": [CH_DE(N_MODULA)],''', '''"fontes": [CHAVE_DE_FONTE["psion"], CHAVE_RECIBO_ERRATA_R5], "verbatins": [CH_DE(N_MODULA)],''')
sub(D, "(RECIBO_ERRATA_PEDRAS_R3_01nov.json e _R4), corrigiu tres coisas:", "(RECIBO_ERRATA_PEDRAS_R3_01nov.json, _R4 e _R5), corrigiu tres coisas:")
sub(D, "A MOLDURA (erratas da gerencia c1, 01/11/2026, 13:28, 16:45, 17:21 e 18:41; recibos RECIBO_ERRATA_PEDRAS_01nov.json e _R2, _R3 e _R4):", "A MOLDURA (erratas da gerencia c1, 01/11/2026, 13:28, 16:45, 17:21, 18:41 e 18:56; recibos RECIBO_ERRATA_PEDRAS_01nov.json e _R2, _R3, _R4 e _R5):")
sub(D, "# 162 = 21 + 15 + 15 + 26 + 38 + 14 + 13 + 20 (medido da fonte pela PINO_DAS_PEDRAS_DETALHE; a R2 deu um teorema ao disco; a R3, onze a Lei do Diminuto e um a Tonica; a R4, oito a Lei do Diminuto e catorze ao Ponto Zero)", "# 163 = 21 + 15 + 15 + 26 + 39 + 14 + 13 + 20 (medido da fonte pela PINO_DAS_PEDRAS_DETALHE; a R2 deu um teorema ao disco; a R3, onze a Lei do Diminuto e um a Tonica; a R4, oito a Lei do Diminuto e catorze ao Ponto Zero; a R5, um a Lei do Diminuto)")
sub(Z, '''"recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R4_01nov.json",''', '''"recibo_vigente_das_pedras": "RECIBO_ERRATA_PEDRAS_R5_01nov.json",''')
sub(Z, '''e a resposta dele mudou três (`..._R4_01nov.json`, a referência vigente: o diminuto é modulação, e a seção O GAP); o resto foi refeito aqui, pela cadeia existente.''', '''a resposta dele mudou três (`..._R4_01nov.json`: o diminuto é modulação, e a seção O GAP); e um achado desta preparação mudou quatro (`..._R5_01nov.json`, a referência vigente: a escala é o que fica parado); o resto foi refeito aqui, pela cadeia existente.''')
sub(Z, '''| guarda | F6 (a frase do no-go), F7 (τ★ e κ derivados), F8 (a escala ligada à transposição), F9 (κ = F como objetivo, sem a palavra proibido), todas com controle negativo |''', '''| R5: a escala | a escala é a musical, o que fica parado; o que era escala de energia é valor absoluto e valor relativo à tônica; os dois teoremas rebatizados entram nos textos; `the_scale_is_free` fica como nome |
| guarda | F6 (a frase do no-go), F7 (τ★ e κ derivados), F8 (a escala ligada à transposição), F9 (κ = F como objetivo, sem a palavra proibido), F10 (a razão chamada de escala), F11 (o diminuto muda a escala), F12 (escala absoluta ou relativa), todas com controle negativo |''')
sub(Z, "Sha256 lidos do recibo vigente das pedras (`insumos\\\\RECIBO_ERRATA_PEDRAS_R3_01nov.json`, cadeia de custódia R3 → R2 → primeira errata): nenhuma prova existente mudou; quatro nomes de teorema mudaram porque o nome afirmava mais do que o teorema prova; o disco ganhou `the_flow_is_the_canonical_law`, o fecho do observador ganhou a leitura binária, a Lei do Diminuto ganhou o acorde e onze teoremas, a Tônica ganhou `the_ratio_survives_the_rescaling`.",
    "Sha256 lidos do recibo vigente das pedras (`insumos\\\\RECIBO_ERRATA_PEDRAS_R5_01nov.json`, cadeia de custódia R5 → R4 → R3 → R2 → primeira errata): nenhuma prova antiga caiu; seis nomes de teorema mudaram ao longo das erratas; o disco ganhou `the_flow_is_the_canonical_law`, o fecho do observador ganhou a leitura binária, a Lei do Diminuto ganhou o acorde e a modulação, a Tônica ganhou `the_ratio_survives_the_rescaling`, o Ponto Zero ganhou a seção O GAP.")
sub(F, '''"titulo": "v405 preparada de novo, erratas R2, R3 e R4 (01/11/2026): candidato %s; pronta=%s"''', '''"titulo": "v405 preparada de novo, erratas R2 a R5 (01/11/2026): candidato %s; pronta=%s"''')
sub(F, '''esta e' a refacao pelas erratas R2, R3 e R4 da gerencia. Quem constroi''', '''esta e' a refacao pelas erratas R2 a R5 da gerencia. Quem constroi''')
sub(F, '''pelas erratas R2, R3 e R4, depois de a revisao de terceiro nao aprovar''', '''pelas erratas R2 a R5, depois de a revisao de terceiro nao aprovar''')

for arq, novo in NOVOS.items():
    compile(novo, arq, "exec") if arq.endswith(".py") else None
for arq, novo in NOVOS.items():
    p = os.path.join(HERE, arq); b = open(p, "rb").read()
    bak = p + ".bak_" + TS + "_R5"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    t = p + ".tmp_R5"; open(t, "wb").write(novo.encode("utf-8")); assert os.path.getsize(t) == len(novo.encode("utf-8")) and os.path.getsize(t) > 1000
    os.replace(t, p)
    print(arq, len(b), "->", len(novo.encode("utf-8")))
print("ok, backups .bak_%s_R5" % TS)

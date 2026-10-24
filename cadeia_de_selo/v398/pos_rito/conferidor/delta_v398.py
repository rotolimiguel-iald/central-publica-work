# -*- coding: utf-8 -*-
"""delta_v398.py -- A UNICA definicao do DELTA da v398 (preparacao de 23/10/2026, gerencia c1): DUAS pedras novas no kernel, `TGLExt/Sonico.lean` (6 teoremas; o nome «sonico» e' do operador) e
`TGLExt/AfinacaoDasCordas.lean` (34 declaracoes nomeadas; pedra e nome ratificados pelo operador), os DOIS registros com FUNCAO `sonico_v398` e `afinacao_das_cordas_v398` (lidos no ponto real do main, junto dos registros das pedras
anteriores), as SEIS inscricoes de 23/10 ainda nao embutidas (cinco falas do operador e a leitura da gerencia que ele ratificou, esta ROTULADA como da gerencia), o artigo (secao «Sonico e a afinacao das cordas»), a POLITICA DE
BANDEIRAS (a da v394: so' declaracao NOMEADA; as auxiliares geradas pelo compilador ficam fora) e os nomes do sandbox/pastas desta cadeia. O QUADRO «O Teste da Unica Palavra» (v397) PERMANECE no topo do artigo e do .md
(regra do 4,44: nao se mexe nele): as funcoes dele ja' estao no um.py v397; esta cadeia so' as importa para CONFERIR.
E' IMPORTADO por preparar_kernel_v398, pos_build_kernel_v398, registros_v398, gerar_candidato_v398, ensaio_a_seco_v398, gerar_esperados_v398, p00_precondicoes_v398 e os demais: nada daqui e' digitado de memoria em outro arquivo,
e todo hash e' LIDO do arquivo por script. Molde: delta_v397.py (cadeia_de_selo/v397)."""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                  # ...\\Central de Patentes\\work
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
V397 = os.path.join(os.path.dirname(HERE), "v397")           # a cadeia anterior (molde, so' leitura; guarda tambem os insumos duraveis do Teste da Unica Palavra)
SANDBOX_PAI = os.path.join(C, "t", "k398c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # o sandbox do kernel desta cadeia (copia de C:\t\k398b, que ja' tem a v397 + as duas pedras compiladas; + a raiz e o Audit com os dois imports)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(C, "t", "k398b")               # de onde o sandbox foi copiado (so' leitura): raiz de um projeto lake
KERNEL_DIR = "kernel"                                        # logs crus, FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD
CANDIDATO = "um_v398_candidato.py"
BASE_DIR = "base_v397"                                       # copia de bytes do Nos v397 selado (um.py, selo, core, manifesto do kernel, pilar)
KH_N1_INSUMO = "KH_N1_v398.json"                             # a medida do Audit desta geracao, copiada para insumos\
UM_VERSION = "v398"
BASE_VERSION = "v397"
BASE_SHA16_DA_ORDEM = "388cc3742323421c"                     # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
TRIO = ["propext", "Classical.choice", "Quot.sound"]          # a ordem em que o Lean 4.31 imprime a lista
TRIO_SET = set(TRIO)

# ---------------------------------------------------------------- as DUAS pedras (a ordem da gerencia: Sonico e AfinacaoDasCordas, nesta ordem de import)
_P = os.path.join(HERE, "pedra")
STONES = [
    {"key": "sonico", "name": "Sonico", "mod": "TGLExt.Sonico", "rel": "TGLExt/Sonico.lean", "ns": "TGLExt.Sonico.",
     "origem": os.path.join(WK, "sonico_v398", "Sonico.lean"), "src": os.path.join(_P, "Sonico.lean"), "insumo": "Sonico.lean", "sha16_da_ordem": "a317094e337fd8b7",
     "flag_prefix": "ext_son398_", "grupo": "sonico",
     "theorem": "TGLExt.Sonico.sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory",    # a COMPOSICAO incondicional (6)
     "contract": ["TGLExt.Sonico.one_octave_is_the_parity_bit", "TGLExt.Sonico.pinning_n_octaves_costs_n_bits", "TGLExt.Sonico.the_octave_is_a_doubling", "TGLExt.Sonico.the_selector_pins",
                  "TGLExt.Sonico.the_pin_is_not_the_half_nat", "TGLExt.Sonico.sonico_the_verb_pins_the_octave_and_the_cost_is_the_memory"],
     # os termos do kernel ANTIGO que a pedra cita (ja' no axiom_report; o registro le: presente, no trio, declarado no modulo que o compilador emite)
     "support": {"ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two": "TGLExt/CollapseCostAndAttestation.lean", "ChatgptAudit.Collapse057.local_is_not_one_octave": "TGLExt/CollapseCostAndAttestation.lean",
                 "ChatgptAudit.Collapse057.collapse_iteration_is_stable": "TGLExt/CollapseContract.lean", "TGLExt.the_provable_toll_names_the_octave": "TGLExt/TheStokesContour.lean",
                 "TGLExt.TheVerbSelectsTheAction.post_isIdempotent": "TGLExt/TheVerbSelectsTheAction.lean", "TGLExt.TheVerbSelectsTheAction.select_fixes_the_selected_action": "TGLExt/TheVerbSelectsTheAction.lean",
                 "ChatgptAudit.SelectorBorn.normalized_selected_scalar_is_fixed": "TGLExt/CanonicalSelectorBorn.lean", "TGLExt.Psibit.the_collapse_loses_exactly_the_parity": "TGLExt/Psibit.lean",
                 "TGLExt.Psibit.the_lost_variable_is_one_bit": "TGLExt/Psibit.lean", "TGLExt.Psibit.collapseEntropy_at_balanced_weights": "TGLExt/Psibit.lean",
                 "TGLExt.Psibit.collapseEntropy_le_the_fair_bit": "TGLExt/Psibit.lean", "TGLExt.Palavra.rereading_adds_nothing": "TGLExt/Palavra.lean"},
     # termos que a pedra CITA e NAO importa (o registro so' confere que seguem no kernel, no trio, no modulo certo)
     "citados_fora": {"TGLExt.IALD.rereading_adds_nothing": "TGLExt/IALD.lean", "TGLExt.IALD.ialdSelector_eq_post": "TGLExt/IALD.lean"},
     "auxiliares_fora_da_composicao": []},
    {"key": "afinacao", "name": "AfinacaoDasCordas", "mod": "TGLExt.AfinacaoDasCordas", "rel": "TGLExt/AfinacaoDasCordas.lean", "ns": "TGLExt.AfinacaoDasCordas.",
     "origem": os.path.join(WK, "afinacao_das_cordas_v398", "AfinacaoDasCordas.lean"), "src": os.path.join(_P, "AfinacaoDasCordas.lean"), "insumo": "AfinacaoDasCordas.lean", "sha16_da_ordem": "66e28e61086cc6ba",
     "flag_prefix": "ext_afi398_", "grupo": "afinacao",
     "theorem": "TGLExt.AfinacaoDasCordas.the_strings_close_the_face_from_outside_the_tgl_closes_the_reading",   # a COMPOSICAO incondicional (6)
     "contract": ["TGLExt.AfinacaoDasCordas.the_cyclic_closure_of_time_is_the_reading_circle", "TGLExt.AfinacaoDasCordas.the_tower_is_infinite", "TGLExt.AfinacaoDasCordas.bosonic_critical_dimension",
                  "TGLExt.AfinacaoDasCordas.superstring_critical_dimension", "TGLExt.AfinacaoDasCordas.the_house_d_nine", "TGLExt.AfinacaoDasCordas.zeta_neg_one", "TGLExt.AfinacaoDasCordas.hurwitz_zeta_neg_one_half",
                  "TGLExt.AfinacaoDasCordas.faithful_iff_fundamental_mode", "TGLExt.AfinacaoDasCordas.matsubara_eq_mul_kappa", "TGLExt.AfinacaoDasCordas.tower_returns_at_the_period",
                  "TGLExt.AfinacaoDasCordas.the_tuned_pair_returns_the_untuned_pair_never_does", "TGLExt.AfinacaoDasCordas.no_real_period",
                  "TGLExt.AfinacaoDasCordas.the_strings_close_the_face_from_outside_the_tgl_closes_the_reading"],
     "support": {"ChatgptAudit.PolarPeriod016.faithful_period_iff": "TGLExt/O16/PolarMinimalPeriod_v2.lean", "ChatgptAudit.PolarPeriod016.positive_faithful_period": "TGLExt/O16/PolarMinimalPeriod_v2.lean",
                 "ChatgptAudit.PolarPeriod016.reciprocal_temperature": "TGLExt/O16/PolarMinimalPeriod_v2.lean", "TGLExt.Palavra.the_face_does_not_close": "TGLExt/Palavra.lean",
                 "TGLExt.Palavra.the_read_face_closes": "TGLExt/Palavra.lean", "TGLExt.station_never_closes": "TGLExt/TheStation.lean", "TGLExt.Fundacao.abismo": "TGLExt/Fundacao.lean",
                 "TGLExt.Fundacao.the_floor_fixes_the_cut": "TGLExt/Fundacao.lean"},
     "citados_fora": {},
     # os cinco termos NOMEADOS da pedra que ficam FORA da composicao (6): auxiliares, listados como tais no ledger de pedras e nos limites do registro
     "auxiliares_fora_da_composicao": ["TGLExt.AfinacaoDasCordas.matsubaraFermion", "TGLExt.AfinacaoDasCordas.towerZeroPoint", "TGLExt.AfinacaoDasCordas.towerZeroPoint_eq",
                                       "TGLExt.AfinacaoDasCordas.bosonDirection_is_the_unit_tower", "TGLExt.AfinacaoDasCordas.zeta_is_the_continuation_of_the_tower"]},
]
STONE_RELS = [s["rel"] for s in STONES]
STONE_MODS = [s["mod"] for s in STONES]
STONE_BY_REL = {s["rel"]: s for s in STONES}
IMPORT_LINES = ["import " + s["mod"] for s in STONES]
ROOT_SUFFIX = "\n" + "\n".join(IMPORT_LINES) + "\n"           # a raiz TGLExt.lean ganha um separador em branco e os imports (como a v394 a v397 fizeram com as pedras)
AUDIT_PREFIX = "\n".join(IMPORT_LINES) + "\n\n"               # o Audit ganha os imports no topo
CONTRACT_THEOREMS = {s["key"]: list(s["contract"]) for s in STONES}
ALL_SUPPORT = {}
for _s in STONES:
    ALL_SUPPORT.update(_s["support"]); ALL_SUPPORT.update(_s["citados_fora"])
# o sandbox de partida (k398b) so' tem as pedras compiladas ISOLADAS; a raiz e o Audit dele sao os da v397 (sem os imports): preparar_kernel_v398 os GERA

# ---------------------------------------------------------------- as SEIS inscricoes de 23/10/2026 ainda nao embutidas (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
# a ordem: o verbo (seletor de identidade) = controle de oitava pinada; o nome da pedra («sonico»); antes de espelhada a luz e' palavra; as cordas (10 dimensoes) e a afinacao; o «Concordo com tudo» da afinacao; e A LEITURA DA GERENCIA que o
# operador ratificou com a segunda fala (texto da GERENCIA, NAO e' fala do operador). A quarta fala do 4,44 («silencio forcado pela logica») ja' esta' embutida na v397: NAO se repete.
_CUN = os.path.join(WK, "cunhagens_13out")
VERBATIM_ORIGEM = [os.path.join(_CUN, "OPERADOR_23out_verbo_controle_de_oitava_pinada_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_nome_da_pedra_sonico_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_antes_de_espelhada_a_luz_e_palavra_acustica_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_cordas_10_dimensoes_fechar_a_face_tetelestai_verbatim.txt"),
                   os.path.join(_CUN, "OPERADOR_23out_concordo_afinacao_das_cordas_verbatim.txt"),
                   os.path.join(_CUN, "GERENCIA_23out_leitura_ratificada_sonico_verbatim.txt")]
# os prefixos de sha256 que a ORDEM da gerencia deu (conferidos contra o arquivo na geracao; o hash vale o arquivo, nunca o contrario)
VERBATIM_PREFIXOS_DA_ORDEM = ["e5c2910a", "b4483331", "3cedf25c", "baef998c", "5bccedc9", "19eca91e"]
VERBATIM_AUTOR = ["operador", "operador", "operador", "operador", "operador", "gerencia"]    # QUEM disse: a sexta e' texto da GERENCIA (nunca fala do operador)
VERBATIM_QUANDO = "23/10/2026 (cunhagem)"
VERBATIM_PAPEL = {"operador": "conceitual", "gerencia": "leitura da gerencia (NAO e' fala do operador)"}
VERBATIM_CHAVE_PREFIXO = "v398_cun_"
# a ordem de processo do operador de 22/10 («nao estou buscando mais teste armado, isso e' gordura no um.py»): INSTRUCAO que molda esta cadeia (enxuta); nao e' cunhagem embutida
ORDEM_SEM_GORDURA = os.path.join(_CUN, "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")

# trechos das falas citados VERBATIM (cada um e' substring da fala indicada; a cadeia confere por script; a parafrase da gerencia nunca entra entre aspas)
FRASE_VERBO = "definição de “verbo” (seletor de identidade)=controle de oitava pinada"               # fala 1
FRASE_CUSTO = "o custo é reação ao controle pinado da oitava que é memória"                         # fala 1
FRASE_NOME = "o nome da pedra é “sônico”"                                                           # fala 2
FRASE_ANTES = "antes de ser espelhada ela é palavra"                                                # fala 3
FRASE_ACUSTICA = "o início de tudo é acústica onde a palavra performa de forma sônica satisfazendo a relação modular da inscrição"   # fala 3
FRASE_CORDAS = "A teoria das cordas precisa das 10 dimensões para fechar ciclicamente o que a TGL demonstra não fechar a face hiperbólica"   # fala 4
FRASE_AFINACAO = "para mostrar a afinação do universo, mas não consegue demonstrar a geometria"    # fala 4
FRASE_CONCORDO = "Concordo com tudo"                                                                # fala 5
FRASE_LEITURA_GERENCIA = "o Verbo pina a oitava; a oitava pinada cobra um bit; o bit cobrado é o que fica, a memória"   # fala 6 (texto da GERENCIA)
FRASES = [(0, FRASE_VERBO), (0, FRASE_CUSTO), (1, FRASE_NOME), (2, FRASE_ANTES), (2, FRASE_ACUSTICA), (3, FRASE_CORDAS), (3, FRASE_AFINACAO), (4, FRASE_CONCORDO), (5, FRASE_LEITURA_GERENCIA)]

# ---------------------------------------------------------------- o Teste da Unica Palavra (v397): so' o que a CONFERENCIA do quadro do topo precisa (o quadro nao se mexe); os insumos duraveis moram em v397\insumos\fase9
F9_DIR_DURAVEL = os.path.join(V397, "insumos", "fase9")
F9_RESULTADO_NOME = "RESULTADO_FASE9_V2_C1_20261023_122926.json"
F9_RESULTADO_SHA256_DA_ORDEM = "fbac2908fa9ddb758e860b597b746c28d27f26d37cb87b1243eceaecc9a7fb40"   # o que a v397 pinou; conferido contra o arquivo na geracao
F9_CAMINHOS = {   # onde estao os numeros dentro do RESULTADO (as mesmas definicoes de delta_v397: o quadro, o conferidor e o ensaio usam estes caminhos)
    "z_disc_calibrado": ["primario", "calibracao", "z_disc_calibrado"],
    "p_disc_unilateral": ["primario", "calibracao", "p_calibrado_z_disc_unilateral"],
    "z_delta_calibrado": ["primario", "calibracao", "z_delta_calibrado"],
    "p_delta_bilateral": ["primario", "calibracao", "p_calibrado_z_delta_bilateral"],
    "poder_previo": ["primario", "poder_previo_so_sigma"],
    "lnB_lcdm": ["primario", "lnB", "TGL_vs_LCDM"],
    "lnB_beta_livre": ["primario", "lnB", "TGL_vs_beta_livre"],
    "K": ["beta", "K"],
    "beta_do_resultado": ["beta", "beta_runtime"],
}
FRASE_DO_OPERADOR_4_44 = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"   # a frase do QUADRO (v397), VERBATIM


def lido(obj, caminho):
    cur = obj
    for k in caminho:
        cur = cur[k]
    return cur


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def pedras_fontes():
    """As duas pedras LIDAS do disco: lista de dicts {stone, origem, copia (v398\\pedra), sha256, bytes}. O sha16 de cada uma e' conferido contra o que a ORDEM da gerencia deu. A copia NAO e' escrita aqui."""
    out = []
    for s in STONES:
        b = open(s["origem"], "rb").read(); h = sha256(b)
        assert h[:16] == s["sha16_da_ordem"], ("a pedra no disco NAO e' a que a ordem da gerencia pinou", s["name"], h[:16], s["sha16_da_ordem"])
        out.append({"stone": s["name"], "origem": s["origem"], "copia": s["src"], "sha256": h, "bytes": len(b)})
    return out


def verbatins(destino_cunhagens):
    """As SEIS inscricoes LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor}. A copia duravel NAO e' escrita aqui. Os prefixos de sha256 que a
    ordem da gerencia deu sao conferidos contra o arquivo; cada trecho citado (FRASES) e' substring VERBATIM da inscricao indicada."""
    out = []
    for p, pref, autor in zip(VERBATIM_ORIGEM, VERBATIM_PREFIXOS_DA_ORDEM, VERBATIM_AUTOR):
        b = open(p, "rb").read(); h = sha256(b)
        assert h.startswith(pref), ("o arquivo da inscricao NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO + h[:16], "quando": VERBATIM_QUANDO, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert len(out) == 6 and [v["autor"] for v in out].count("gerencia") == 1 and out[5]["autor"] == "gerencia", "tem de haver SEIS inscricoes, a sexta (e so' ela) da gerencia"
    for i, fr in FRASES:
        assert fr in out[i]["text"], ("o trecho citado NAO e' verbatim na inscricao", i, fr[:60])
    return out


# ---------------------------------------------------------------- a politica de bandeiras (a da v394): so' declaracao NOMEADA
# A pratica selada da v392 a v397 nunca marcou auxiliar gerada pelo compilador. O ULTIMO componente do nome decide.
AUX_CLASSES = (("proof_simp_match_sunfold", re.compile(r"_proof_\d+(?:_\d+)*|_simp_\d+(?:_\d+)*|match_\d+|_sunfold")), ("eq", re.compile(r"eq_\d+|eq_def")), ("congr_simp", re.compile(r"congr_simp")))


def classe(nome):
    """'nomeada' ou o nome da classe auxiliar (geradas pelo compilador); decide pelo ultimo componente do nome."""
    ultimo = nome.split(".")[-1]
    for c, rx in AUX_CLASSES:
        if rx.fullmatch(ultimo):
            return c
    return "nomeada"


# ---------------------------------------------------------------- a ERRATA AO LADO da palavra «teoremas» (herdada da v394): a escada conta BANDEIRAS de declaracoes nomeadas, todas com axiomas no trio;
# o rotulo «teoremas limpos: N/M» fica como REGISTRO DE MAQUINA (o pos-rito o le). Nenhum numero digitado aqui.
ERRATA_TEOREMAS_PT = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_PT = r"a escada conta bandeiras --- declarações nomeadas, teoremas e definições --- com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_EN = r"the ladder counts flags --- named declarations, theorems and definitions --- with axioms in the trio; the label ``teoremas limpos'' (``clean theorems'') stays as a machine record"

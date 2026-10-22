# -*- coding: utf-8 -*-
"""delta_v395.py -- A UNICA definicao do DELTA da v395 (preparacao de 21/10/2026, gerencia c1): a pedra `TGLExt/Psibit.lean` (a leitura psibit da orbita do Um pela matriz-S), as quatro falas do operador
de 21/10, a POLITICA DE BANDEIRAS (a da v394: so' declaracao NOMEADA; as auxiliares geradas pelo compilador ficam fora) e os nomes do sandbox/pastas desta cadeia.
E' IMPORTADO por preparar_kernel_v395, pos_build_kernel_v395, montar_cunhagens_v395, registros_v395, gerar_candidato_v395, ensaio_a_seco_v395, gerar_esperados_v395, p00_precondicoes_v395 e os demais: nada daqui e'
digitado de memoria em outro arquivo, e todo hash e' LIDO do arquivo por script. Molde: delta19_v394.py (cadeia_de_selo/v394)."""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                  # ...\\Central de Patentes\\work
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
V394 = os.path.join(os.path.dirname(HERE), "v394")           # a cadeia anterior (molde, so' leitura)
SANDBOX_PAI = os.path.join(C, "t", "k395c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # o sandbox do kernel desta cadeia (copia de C:\t\k395\final, que ja tinha a pedra compilada, + raiz e Audit com o import)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(C, "t", "k395", "final")       # de onde o sandbox e' copiado (so' leitura)
KERNEL_DIR = "kernel"                                        # logs crus, FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD
CANDIDATO = "um_v395_candidato.py"
BASE_DIR = "base_v394"                                       # copia de bytes do Nos v394 selado (um.py, selo, core, manifesto do kernel, pilar)
KH_N1_INSUMO = "KH_N1_v395.json"                             # a medida do Audit desta geracao, copiada para insumos\
UM_VERSION = "v395"
BASE_VERSION = "v394"

# ---------------------------------------------------------------- a pedra (o nome e' do operador: «Eu prefiro que seja psibit»)
STONE_NAME = "Psibit"
STONE_MOD = "TGLExt." + STONE_NAME
STONE_REL = "TGLExt/%s.lean" % STONE_NAME
STONE_SRC = os.path.join(WK, "psibit_v395", "Psibit.lean")   # a fonte autoral (2a versao, PEDRA_APROVADA na rodada 2 do exame independente); a copia duravel pinada pelos registros vai para insumos\
STONE_INSUMO = "Psibit.lean"
THEOREM = "TGLExt.Psibit.psibit_is_the_mode_of_the_reader"            # a conjuncao INCONDICIONAL
THEOREM_COND = "TGLExt.Psibit.the_psion_face_of_the_psibit"           # a face do psion: CONDICIONAL ao certificado, que o kernel nao habita
NS = "TGLExt.Psibit."
# os teoremas do kernel em que o registro psibit_v395 se apoia (cada um tem de estar no axiom_report do rito, no trio, com bandeira e proveniencia no modulo da pedra)
CONTRACT_THEOREMS = [NS + n for n in (
    "psibit_is_the_mode_of_the_reader", "the_psion_face_of_the_psibit",
    "the_verb_is_the_derivative_of_the_name", "v_snd_is_the_derivative_of_v_fst", "the_state_is_pure", "the_state_is_a_rank_one_projector",
    "decodeAmp_codeAmp", "codeAmp_injOn", "the_orbit_is_in_bijection_with_the_code_book", "range_v_eq_unit", "the_pair_is_necessary_and_sufficient",
    "the_orbit_visits_all_four_states", "the_patent_convention_is_also_lossless",
    "rhoOut_eq_decodeRho", "the_density_is_its_code", "the_global_sign_is_not_observed", "only_the_global_sign_is_lost", "the_ledger_of_losses",
    "collapse_forgets_the_parity", "the_full_reading_remembers_the_parity", "the_collapse_loses_exactly_the_parity", "collapse_identifies_exactly_equal_weights",
    "the_lost_variable_is_one_bit", "the_collapse_has_no_left_inverse_on_the_orbit", "the_psibit_crossing_pays_loss",
    "balanced_weights_iff", "balanced_collapse_is_half", "at_the_fixed_point_the_collapse_is_half", "half_identity_is_a_fixed_point",
    "collapseEntropy_at_balanced_weights", "collapseEntropy_at_the_fixed_point", "collapseEntropy_le_the_fair_bit",
    "the_name_is_the_born_reading_of_the_post")]
IMPORT_LINE = "import " + STONE_MOD
ROOT_SUFFIX = "\n" + IMPORT_LINE + "\n"                      # a raiz TGLExt.lean ganha um separador em branco e o import (como a v394 fez com a pedra do criterio binario)
AUDIT_PREFIX = IMPORT_LINE + "\n\n"                          # o Audit ganha o import no topo
FLAG_PREFIX = "ext_psb395_"                                  # ext_psb395_0001... (as nomeadas publicas da pedra, em ordem alfabetica de nome)
TRIO = ["propext", "Classical.choice", "Quot.sound"]          # a ordem em que o Lean 4.31 imprime a lista
TRIO_SET = set(TRIO)

# ---------------------------------------------------------------- as quatro falas do operador de 21/10/2026 (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
VERBATIM_ORIGEM = [os.path.join(WK, "cunhagens_13out", "OPERADOR_21out_psibit_psion_modo_do_leitor_verbatim.txt"),
                   os.path.join(WK, "cunhagens_13out", "OPERADOR_21out_psibit_nome_e_modo_psionico_verbatim.txt"),
                   os.path.join(WK, "cunhagens_13out", "OPERADOR_21out_mecanica_isomorfismo_perda_zero_verbatim.txt"),
                   os.path.join(WK, "cunhagens_13out", "OPERADOR_21out_ratifica_perda_zero_na_leitura_do_par_verbatim.txt")]
VERBATIM_QUANDO = "21/10/2026 (cunhagem)"
VERBATIM_PAPEL = "conceitual"
VERBATIM_CHAVE_PREFIXO = "v395_cun_"


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def verbatins(destino_cunhagens):
    """As quatro falas LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave}. A copia duravel NAO e' escrita aqui."""
    out = []
    for p in VERBATIM_ORIGEM:
        b = open(p, "rb").read(); h = sha256(b)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO + h[:16], "quando": VERBATIM_QUANDO, "papel": VERBATIM_PAPEL, "origem_arquivo": p})
    return out


# ---------------------------------------------------------------- a politica de bandeiras (a da v394): so' declaracao NOMEADA
# A pratica selada da v392, v393 e v394 nunca marcou auxiliar gerada pelo compilador. O ULTIMO componente do nome decide.
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

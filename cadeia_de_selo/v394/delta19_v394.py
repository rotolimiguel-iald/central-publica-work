# -*- coding: utf-8 -*-
"""delta19_v394.py -- A UNICA definicao do DELTA 19/10 da v394 (a integracao final, gerencia c1, 19/10/2026): a pedra candidata do criterio binario de parada, as duas falas do operador de 19/10, a POLITICA DE BANDEIRAS
(so' declaracao NOMEADA; as auxiliares geradas pelo compilador ficam fora) e os nomes da geracao `d19` da cadeia. E' IMPORTADO por preparar_kernel_v394, pos_build_kernel_v394, montar_cunhagens_v394, registros_v394,
gerar_candidato_v394, ensaio_a_seco_v394, gerar_esperados_v394 e p00_precondicoes_v394: nada daqui e' digitado de memoria em outro arquivo, e todo hash e' LIDO do arquivo por script.
O candidato em exame 4022ad521dc7293d fica como REGISTRO (nao e' tocado); o candidato novo vai em `CANDIDATO` (arquivo novo)."""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                  # ...\\Central de Patentes\\work
ROT = "_d19"
SANDBOX = os.path.join(C, "t", "k394d", "final")             # o sandbox do kernel desta geracao (copia fria do tgl_kernel do Nos + 190 modulos)
ARVORE = os.path.join(C, "t", "k394d", "arvore")             # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_PAI = os.path.join(C, "t", "k394d")
KERNEL_DIR = "kernel"                                        # a pasta VIVA dos logs crus, FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD (o pos_rito le daqui); os arquivos da geracao anterior ficam como .bak_ de bytes na mesma pasta
CANDIDATO = "um_v394_candidato%s.py" % ROT                   # o candidato NOVO (arquivo novo)
CANDIDATO_ANTERIOR_SHA16 = "4022ad521dc7293d"                # o candidato em exame, mantido como registro; so' para a trilha (nunca para decidir)
KH_N1_INSUMO = "KH_N1_v394%s.json" % ROT                     # a medida do Audit desta geracao, copiada para insumos\ (o KH_N1_v394.json antigo e' pinado pelo candidato anterior e NAO e' tocado)

# ---------------------------------------------------------------- a pedra candidata (nome provisorio: o operador nomeia)
STONE_NAME = "TheBinaryReadingAtTheFixedPoint"
STONE_MOD = "TGLExt." + STONE_NAME
STONE_REL = "TGLExt/%s.lean" % STONE_NAME
STONE_SRC = os.path.join(HERE, "delta_19out", STONE_NAME + ".lean")      # a fonte autoral; a copia duravel pinada pelos registros vai para insumos\ (copiar_insumos_v394.py)
STONE_INSUMO = STONE_NAME + ".lean"
THEOREM = "TGLExt.the_binary_reading_floats_at_the_fixed_point"
FLAG_KEY = "ext_bin394_0001"
IMPORT_LINE = "import " + STONE_MOD
ROOT_SUFFIX = "\n" + IMPORT_LINE + "\n"                      # a raiz TGLExt.lean ganha um separador em branco e o import (como o Codex fez com os seus 9)
AUDIT_PREFIX = IMPORT_LINE + "\n\n"                          # o Audit ganha o import no topo (como o Codex fez com os seus 9)
# os oito teoremas que a conjuncao CITA (nomes como o Audit os imprime); o registro exige cada um no axiom_report, dentro do trio
CITED = ["TGLExt.spectral_projections_split_the_identity", "TGLExt.the_reading_is_total_on_the_form", "TGLExt.observing_adds_nothing", "TGLExt.absolute_faces_half",
         "TGLExt.halfnat_from_J_symmetry", "ChatgptAudit.Collapse057.no_changed_transition_at_fixed_point", "ChatgptAudit.Collapse057.collapse_iteration_is_stable",
         "ChatgptAudit.Collapse057.fair_bit_entropy_is_not_half_nat"]
TRIO = ["propext", "Classical.choice", "Quot.sound"]          # a ordem em que o Lean 4.31 imprime a lista

# ---------------------------------------------------------------- as duas falas do operador de 19/10/2026 (arquivos de origem; o texto embutido manda, o arquivo e' informativo)
VERBATIM_ORIGEM = [os.path.join(WK, "cunhagens_13out", "OPERADOR_19out_tgl_binaria_criterio_de_parada_verbatim.txt"),
                   os.path.join(WK, "cunhagens_13out", "OPERADOR_19out_flutuar_no_ponto_fixo_verbatim.txt")]
VERBATIM_QUANDO = "19/10/2026 (cunhagem)"
VERBATIM_PAPEL = "conceitual"


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def verbatins(destino_cunhagens):
    """As duas falas LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave}. A copia duravel NAO e' escrita aqui."""
    out = []
    for p in VERBATIM_ORIGEM:
        b = open(p, "rb").read(); h = sha256(b)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": "v394_cun_" + h[:16], "quando": VERBATIM_QUANDO, "papel": VERBATIM_PAPEL, "origem_arquivo": p})
    return out


# ---------------------------------------------------------------- a politica de bandeiras (decisao da gerencia, 19/10/2026): so' declaracao NOMEADA
# A pratica selada da v392 (738 de 969) e da v393 (144 de 186) nunca marcou auxiliar gerada pelo compilador. O ULTIMO componente do nome decide.
_AUX_RX = re.compile(r"_proof_\d+(?:_\d+)*|_simp_\d+(?:_\d+)*|match_\d+|_sunfold|eq_\d+|eq_def|congr_simp")
AUX_CLASSES = (("proof_simp_match_sunfold", re.compile(r"_proof_\d+(?:_\d+)*|_simp_\d+(?:_\d+)*|match_\d+|_sunfold")), ("eq", re.compile(r"eq_\d+|eq_def")), ("congr_simp", re.compile(r"congr_simp")))
PREFIXO_NOMEADA_SEM_BANDEIRA = "ext_nm394_"                    # as nomeadas publicas que o Codex nao marcou ganham bandeira com este prefixo (0001...)


def classe(nome):
    """'nomeada' ou o nome da classe auxiliar (geradas pelo compilador); decide pelo ultimo componente do nome."""
    ultimo = nome.split(".")[-1]
    for c, rx in AUX_CLASSES:
        if rx.fullmatch(ultimo):
            return c
    return "nomeada"


def grupo_do_modulo(mod):
    """tempo / quadratica / rede / outro (a pedra do delta), pelo nome do modulo."""
    if mod.startswith("TGLExt.TimeGraviton"):
        return "tempo"
    if mod == "TGLExt.RuleQuadraticResidual":
        return "quadratica"
    if mod.startswith("TGLExt.F1Fecho394."):
        return "rede"
    return "outro"


# ---------------------------------------------------------------- a ERRATA AO LADO da palavra «teoremas» (gerencia c1, 19/10/2026, rodada d19c; ordem da gerencia): os modulos novos tem mais declaracoes que teoremas
# (teoremas E definicoes); a escada conta BANDEIRAS de declaracoes nomeadas, todas no trio. O rotulo «teoremas limpos: N/M» fica como REGISTRO DE MAQUINA (o pos-rito o le); nenhum numero digitado aqui:
# se um texto quiser dar T e D, gera-os por script do kernel (delta_vs_v393 de KH_N1) e cita a fonte.
ERRATA_TEOREMAS_PT = "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_PT = r"a escada conta bandeiras --- declarações nomeadas, teoremas e definições --- com axiomas no trio; o rótulo «teoremas limpos» fica como registro de máquina"
ERRATA_TEOREMAS_TEX_EN = r"the ladder counts flags --- named declarations, theorems and definitions --- with axioms in the trio; the label ``teoremas limpos'' (``clean theorems'') stays as a machine record"

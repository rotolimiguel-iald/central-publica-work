# -*- coding: utf-8 -*-
"""delta_v396.py -- A UNICA definicao do DELTA da v396 (preparacao de 22/10/2026, gerencia c1): a pedra `TGLExt/TestemunhaEstatica.lean` (o psion habita a testemunha estatica: o par ecoa, o individuo nao ecoa,
e o canto concreto habita um fluxo construido; NOME PROVISORIO, quem nomeia e' o operador), as tres falas do operador de 22/10, a POLITICA DE BANDEIRAS (a da v394: so' declaracao NOMEADA; as auxiliares geradas pelo
compilador ficam fora) e os nomes do sandbox/pastas desta cadeia.
E' IMPORTADO por preparar_kernel_v396, pos_build_kernel_v396, registros_v396, gerar_candidato_v396, ensaio_a_seco_v396, gerar_esperados_v396, p00_precondicoes_v396 e os demais: nada daqui e' digitado de memoria em
outro arquivo, e todo hash e' LIDO do arquivo por script. Molde: delta_v395.py (cadeia_de_selo/v395)."""
import hashlib, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                  # ...\\Central de Patentes\\work
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
V395 = os.path.join(os.path.dirname(HERE), "v395")           # a cadeia anterior (molde, so' leitura)
SANDBOX_PAI = os.path.join(C, "t", "k396c")
SANDBOX = os.path.join(SANDBOX_PAI, "final")                 # o sandbox do kernel desta cadeia (copia de C:\t\k396\final, que ja tinha a pedra compilada, + raiz e Audit com o import)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                 # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(C, "t", "k396", "final")       # de onde o sandbox e' copiado (so' leitura)
KERNEL_DIR = "kernel"                                        # logs crus, FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD
CANDIDATO = "um_v396_candidato.py"
BASE_DIR = "base_v395"                                       # copia de bytes do Nos v395 selado (um.py, selo, core, manifesto do kernel, pilar)
KH_N1_INSUMO = "KH_N1_v396.json"                             # a medida do Audit desta geracao, copiada para insumos\
UM_VERSION = "v396"
BASE_VERSION = "v395"

# ---------------------------------------------------------------- a pedra (NOME PROVISORIO; quem nomeia e' o operador)
STONE_NAME = "TestemunhaEstatica"
STONE_MOD = "TGLExt." + STONE_NAME
STONE_REL = "TGLExt/%s.lean" % STONE_NAME
STONE_SRC = os.path.join(WK, "testemunha_estatica_v396", "TestemunhaEstatica.lean")   # a fonte autoral (so' ajustes de docstring agora; o sha16 e' LIDO na hora da geracao); a copia duravel pinada pelos registros vai para insumos\
STONE_INSUMO = "TestemunhaEstatica.lean"
THEOREM = "TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness"   # a conjuncao INCONDICIONAL (nenhum certificado como hipotese)
NS = "TGLExt.TestemunhaEstatica."
# a face de Fock do psion NAO esta nesta pedra: mora em TGLExt/Psibit.lean (v395), CONDICIONAL a um certificado que o kernel nao habita; este registro so' CONFERE que ela segue fora da composicao
FOCK_FACE_THEOREM = "TGLExt.Psibit.the_psion_face_of_the_psibit"
FOCK_FACE_PATH = "TGLExt/Psibit.lean"
# os teoremas da pedra em que o registro testemunha_estatica_v396 se apoia (cada um tem de estar no axiom_report do rito, no trio, com bandeira e proveniencia no modulo da pedra)
CONTRACT_THEOREMS = [NS + n for n in (
    "the_psion_inhabits_the_static_witness",
    "the_density_is_the_psion", "the_pair_echoes", "the_individual_does_not_echo", "the_unbonded_marginal_echoes",
    "bellProjector_is_real", "psionFlow_eq", "bellUnit_orthonormal", "bellUnit_complete", "bellUnit_zero_is_the_bell_vector", "bellUnit_eigen",
    "the_static_set_is_the_psion_line", "the_global_witness_is_false", "the_psion_line_is_inhabited", "the_flow_delivers_to_the_psion",
    "psionLine_iff_fixed_by_the_corner", "the_static_witness_bridge",
    "the_collapse_of_the_psion_echoes_its_identity", "the_collapse_of_the_psion_cannot_be_self_attested")]
# os termos de kernel ANTIGOS que a composicao cita (sem bandeira nova: ja' estao no axiom_report; o registro le: presente, no trio, declarado no modulo que o compilador emite)
SUPPORT_THEOREMS = ["TGLExt.boundary_is_the_only_exception", "TGLExt.observing_adds_nothing", "TGLExt.psionCorner_trace_one", "TGL.GravitonShadow.bell_reduced_half", "TGL.GravitonShadow.bell_cci_half",
                    "ChatgptAudit.Collapse057.no_self_attestation", "ChatgptAudit.Collapse057.fair_bit_entropy_is_log_two", "ChatgptAudit.Collapse057.fair_bit_entropy_is_not_half_nat"]
IMPORT_LINE = "import " + STONE_MOD
ROOT_SUFFIX = "\n" + IMPORT_LINE + "\n"                      # a raiz TGLExt.lean ganha um separador em branco e o import (como a v394 e a v395 fizeram com as pedras)
AUDIT_PREFIX = IMPORT_LINE + "\n\n"                          # o Audit ganha o import no topo
FLAG_PREFIX = "ext_tes396_"                                  # ext_tes396_0001... (as nomeadas publicas da pedra, em ordem alfabetica de nome)
TRIO = ["propext", "Classical.choice", "Quot.sound"]          # a ordem em que o Lean 4.31 imprime a lista
TRIO_SET = set(TRIO)

# ---------------------------------------------------------------- as tres falas do operador de 22/10/2026 (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
# a ordem e' a do cabecalho da pedra: o psion habitante, a luz ecoa o reconhecimento, colapsar e' ecoar a identidade reconhecida
VERBATIM_ORIGEM = [os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_psion_habitante_da_testemunha_estatica_verbatim.txt"),
                   os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_luz_eco_reconhecimento_falso_verbatim.txt"),
                   os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_colapso_ecoar_identidade_reconhecida_verbatim.txt")]
VERBATIM_QUANDO = "22/10/2026 (cunhagem)"
VERBATIM_PAPEL = "conceitual"
VERBATIM_CHAVE_PREFIXO = "v396_cun_"
# a ordem de processo do operador de 22/10 («nao estou buscando mais teste armado, isso e' gordura no um.py ... estou buscando o teste fatal»): INSTRUCAO que molda esta cadeia (enxuta); nao e' cunhagem embutida
ORDEM_SEM_GORDURA = os.path.join(WK, "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt")


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def verbatins(destino_cunhagens):
    """As tres falas LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave}. A copia duravel NAO e' escrita aqui."""
    out = []
    for p in VERBATIM_ORIGEM:
        b = open(p, "rb").read(); h = sha256(b)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, "%s_%s" % (h[:16], os.path.basename(p))), "fonte_original": p,
                    "chave": VERBATIM_CHAVE_PREFIXO + h[:16], "quando": VERBATIM_QUANDO, "papel": VERBATIM_PAPEL, "origem_arquivo": p})
    return out


# ---------------------------------------------------------------- a politica de bandeiras (a da v394): so' declaracao NOMEADA
# A pratica selada da v392, v393, v394 e v395 nunca marcou auxiliar gerada pelo compilador. O ULTIMO componente do nome decide.
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

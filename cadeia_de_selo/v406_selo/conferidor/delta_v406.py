# -*- coding: utf-8 -*-
"""delta_v406.py -- A UNICA definicao do DELTA da v406 (gerencia c1, 02/11/2026): O FECHAMENTO ENTRA NO um.py.
Ordem do operador (02/11/2026, verbatim sha16 f3998f01262aad6b): «perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.»; a prioridade (sha16 9978862f60cfbf29):
«a construção da passagem para o contínuo é o que mais importa … virar essa chave de conjectura para provado»; e a ordem de compilar (sha16 b5717ff445a883cd): «quando terminar, compile a nova versão do um.py, rode, publique e atualize tudo por favor».
O QUE ENTRA NO KERNEL (modelo de BUNDLE, como a v394; nao o modelo de oito pedras da v405): 301 modulos novos em TGLExt/F1Fecho394/ -- os 300 da bancada do ChatGPT (missao F1.FECHO_20261015, 15 e 16/10/2026; recibo
orbital_rotation/attempts/20261016T210640_174717Z/RECEIPT.json; recompilados do fonte no sandbox da v405 pela integracao R3 de 02/11: 300 compilados, 0 falhas, 0 bloqueados; imports normalizados para TGLExt.F1Fecho394.* e os blocos #eval
removidos, cada fonte conferida por sha256 contra o recibo ANTES da normalizacao) + a candidata da gerencia CanonicalFullTGLWitnessR1 (canonicalFullTGLWitness := <lightNet physicalFockCertificate, lightRealization physicalFockCertificate>: o
termo canonico da testemunha completa, FullTGLWitness). A raiz TGLExt.lean ganha DOIS imports (o topo do fecho, CanonicalFockModularCoreInputR1, que puxa os 300 pelo grafo; e a candidata). O Audit NAO muda.
O QUE O FECHO E' (ratificacao R10 da gerencia, 02/11/2026, RATIFICACAO_R10_c1_02nov.md): RemainingModularCoreInput D (os 21 campos da passagem para o continuo: traco ciclico, PF, Pp, Pm, as metades iguais...) esta' HABITADO por construcao
para todo D : CanonicalNetInput (modularCoreInput), e FockCertificate esta' habitado sobre a rede fisica physicalCanonicalNet (physicalFockCertificate), so' com o trio de axiomas. As QUATRO chaves de testemunha que o um.py trazia como
LITERAL False desde a v394 (rede_fock_v394.whole_certificate_inhabited; psibit_v395.conditional_psion_face.inhabitant_exhibited; testemunha_estatica_v396.fock_face.inhabitant_exhibited; e a medida witness_layers.canonical_full_witness_term_constructed)
passam a ser LIDAS do kernel do proprio rito, com errata AO LADO (o literal registrava o estado de entao). As ressalvas (K(O) != bot so' na cunha; «nucleo II_inf» [KNOWN/DECLARADO]; traco ENNReal ciclico, nao linear; R7 Codex x Codex;
R4/R5 fora) vao ditas em todo texto. NOT_FALSIFIED nunca e' CONFIRMED; validade no kernel nao e' creditacao; o GATE NAO SE MOVE; beta nunca literal; full_static_witness_exists e trivial_inhabitant_exists seguem False por teorema.
A base e' a v405 SELADA (um.py 0030242565cc13f6) e a Bancada Um de producao JA pina a v405 (B14-v405-20261102-R1): o B(n) da v406 e' um PASSO SIMPLES v405 -> v406 (o diff do kernel sao os 301 modulos).
E' IMPORTADO por copiar_base, preparar_bundle, pos_build_kernel, registros_v406, runtime (so' as puras), gerar_candidato_v406, ensaio_a_seco, gerar_esperados, p00 e os demais: nada daqui e' digitado de memoria em outro arquivo; todo hash e' LIDO do arquivo.
Reaproveita (import por caminho) o delta_v405 (e este o delta_v404, ...): as fontes do operador do ACOM, a politica de bandeiras (classe), o quadro do Teste da Unica Palavra, as classes de auxiliares. O que a v406 SOBRESCREVE vem abaixo.
Molde: delta_v405.py (as constantes) + delta19_v394.py (o modelo de bundle). Desenho: work\\fechamento_02nov\\DESENHO_v406.md. Receita: RECEITA_CADEIA_DE_SELO_v404_para_v405_para_a_v406.md."""
import glob
import hashlib
import importlib.util
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
V405 = os.path.join(os.path.dirname(HERE), "v405")           # a cadeia anterior (molde e base, so' leitura)
_spec = importlib.util.spec_from_file_location("delta_v405", os.path.join(V405, "delta_v405.py"))
D5 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(D5)
globals().update({k: v for k, v in vars(D5).items() if not k.startswith("__")})   # tudo da v405 (e, por ela, da v404 ... v399) e depois o que a v406 SOBRESCREVE
D5 = D5                                                        # (D4 = delta_v404, D3, D2, D1, D0, D9: herdados do update acima; D5 = delta_v405, o predecessor imediato)

HERE = os.path.dirname(os.path.abspath(__file__))              # (o update acima trouxe o HERE da v405: aqui e' a pasta da v406)
V405 = os.path.join(os.path.dirname(HERE), "v405")
V404 = D5.V404
C = "C:" + os.sep
WK = os.path.dirname(os.path.dirname(HERE))                    # ...\Central de Patentes\work
CENTRAL = os.path.dirname(WK)                                  # ...\Central de Patentes
SANDBOX_PAI = os.path.join(C, "t", "k406c")                    # sandbox NOVO (a receita manda nao reusar o k405c: a integracao R3 o alterou)
SANDBOX = os.path.join(SANDBOX_PAI, "final")                   # copia do kernel do Nos v405 SELADO (fontes + .lake/build compilado pelo rito de 01/11) + o bundle de 301 + a raiz com os dois imports (preparar_bundle_v406_02nov.py)
ARVORE = os.path.join(SANDBOX_PAI, "arvore")                   # a arvore so'-fontes do recibo do kernel (o B(n) pos-selo precisa dela)
SANDBOX_ORIGEM = os.path.join(D5.NOS, "tgl_kernel")            # o kernel do Nos v405 selado (so' leitura)
PACKAGES_ORIGEM = os.path.join(C, "t", "k404c", "final", ".lake", "packages")   # a copia da mathlib compilada que os sandboxes anteriores usaram (juncao, so' leitura)
KERNEL_DIR = "kernel"
CANDIDATO = "um_v406_candidato.py"
BASE_DIR = "base_v405"                                         # copia de bytes do Nos v405 selado (um.py, selo, core, manifesto do kernel, pilar, sidecar)
UM_VERSION = "v406"
BASE_VERSION = "v405"
BASE_SHA16_DA_ORDEM = "0030242565cc13f6"                       # o que a ordem da gerencia deu (conferido contra o selo e contra o arquivo; o arquivo manda)
SANDBOX_CURTO = os.path.join(C, "t", "vb21")                   # o sandbox curto das guardas estaticas da Bancada (fica vb21; tem de nao existir quando a bateria pre-selo roda)
KH_N1_INSUMO = "KH_N1_v406.json"
ESTUDO_FECHO = os.path.join(WK, "fechamento_02nov")            # a ratificacao, o desenho, a receita, a integracao R3, a candidata (so' leitura)
BANCADA_RAIZ = os.path.join(CENTRAL, "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "F1.FECHO_20261015")   # a bancada do ChatGPT (so' leitura; a pasta Chatgpt e' do ChatGPT)
_BANCADA_CONTRATOS = os.path.join(C, "IALD", "Bancada_Um", "canonical_contracts.json")


def _bancada_pina_hoje():
    """o que a Bancada de producao pina HOJE, LIDO do arquivo dela (nunca digitado): tem de ser a v405 (o B(n) da v406 e' um passo simples)."""
    d_ = json.load(open(_BANCADA_CONTRATOS, encoding="utf-8"))
    dep_ = str(d_.get("deployment_id", ""))
    m_ = re.match(r"B(\d+)-(v\d+)-", dep_)
    assert m_ and m_.group(2) == BASE_VERSION, ("a Bancada de producao NAO pina a v405: o B(n) da v406 nao seria um passo simples", dep_)
    return {"version": m_.group(2), "deployment_id": dep_, "n": int(m_.group(1))}


BANCADA_PINA_HOJE = _bancada_pina_hoje()                       # {'version': 'v405', 'deployment_id': 'B14-v405-20261102-R1', 'n': 14} em 02/11/2026
B_N_SEGUINTE = "B%d" % (BANCADA_PINA_HOJE["n"] + 1)            # o rotulo do B(n) da v406 (B15)


def sha16_arquivo(p_):
    """o sha16 dos bytes do arquivo, lido na hora (nunca digitado)."""
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]


def sha256_arquivo(p_):
    return hashlib.sha256(open(p_, "rb").read()).hexdigest()


# ---------------------------------------------------------------- O BUNDLE (os 301 modulos; a lista e os sha256 sao LIDOS dos arquivos que preparar_bundle_v406_02nov.py escreveu, nunca digitados)
BUNDLE_LISTA_ARQ = os.path.join(HERE, "kernel_modulos_novos_v406.json")
BUNDLE_ARQ = os.path.join(HERE, "BUNDLE_v406.json")
_BL = json.load(open(BUNDLE_LISTA_ARQ, encoding="utf-8"))
_BD = json.load(open(BUNDLE_ARQ, encoding="utf-8"))
BUNDLE_RELS = list(_BL["novos"])                               # 'TGLExt/F1Fecho394/<Nome>.lean', na ordem do preparo (os 300 em ordem alfabetica, a candidata por ultimo)
BUNDLE_MODS = [p[:-len(".lean")].replace("/", ".") for p in BUNDLE_RELS]
N_BUNDLE = len(BUNDLE_RELS)
BUNDLE_POR_REL = {b["rel"]: b for b in _BD["modulos"]}
assert N_BUNDLE == _BL["n"] == _BD["n"] == len(BUNDLE_POR_REL) == 301 and set(BUNDLE_POR_REL) == set(BUNDLE_RELS), ("o bundle tem de ser os 301 modulos (300 da bancada + a candidata)", N_BUNDLE, _BL["n"], _BD["n"])
assert len(set(BUNDLE_RELS)) == N_BUNDLE and all(r.startswith("TGLExt/F1Fecho394/") for r in BUNDLE_RELS)
BUNDLE_DA_BANCADA = [r for r in BUNDLE_RELS if BUNDLE_POR_REL[r]["fonte_bancada"]]            # 300
BUNDLE_DA_GERENCIA = [r for r in BUNDLE_RELS if not BUNDLE_POR_REL[r]["fonte_bancada"]]       # 1: a candidata
assert len(BUNDLE_DA_BANCADA) == 300 and BUNDLE_DA_GERENCIA == ["TGLExt/F1Fecho394/CanonicalFullTGLWitnessR1.lean"]
ROOT_SUFFIX = _BL["root_suffix"]                               # a raiz TGLExt.lean = a da v405 + estes DOIS imports (o topo do fecho e a candidata); lido do arquivo do preparo
assert ROOT_SUFFIX.replace("\r\n", "\n") == "import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1\nimport TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1\n", repr(ROOT_SUFFIX)
AUDIT_PREFIX = ""                                              # v406: o Audit do sandbox e' o do Nos v405 SEM alteracao: ele ja' faz `import TGLExt` (a raiz), que traz os modulos novos
FLAG_PREFIX = "ext_fch406_"                                    # as bandeiras do bundle: UMA serie, so' declaracao NOMEADA publica (a politica da v394), em ordem (modulo, nome); o numero e' MEDIDO pelo pos_build
GRUPO_BUNDLE = "fecho"
MODULO_TOPO = "TGLExt/F1Fecho394/CanonicalFockModularCoreInputR1.lean"       # o topo do fecho (o habitante dos 21 campos e o certificado fisico)
MODULO_REDE = "TGLExt/F1Fecho394/PhysicalCanonicalNetCompleteR1.lean"       # a rede fisica (K := compactPhysicalNet; K_local/K_translate/K_boost/wedge_glue teoremas)
MODULO_TESTEMUNHA = "TGLExt/F1Fecho394/CanonicalFullTGLWitnessR1.lean"      # a candidata da gerencia: o termo canonico FullTGLWitness
assert MODULO_TOPO in BUNDLE_POR_REL and MODULO_REDE in BUNDLE_POR_REL and MODULO_TESTEMUNHA in BUNDLE_POR_REL

# ---------------------------------------------------------------- AS ANCORAS (os nomes EXATOS que o registro fechamento_v406 le do axiom_report do rito; lidos de CHECK_axioms.txt da integracao e das fontes, conferidos pelo pos_build no Audit do sandbox)
ANCORAS = {
    "F1Fecho.CanonicalFockModularCoreInputR1.modularCoreInput": {"rel": MODULO_TOPO, "papel": "o habitante dos 21 campos (RemainingModularCoreInput D) para todo D : CanonicalNetInput: a passagem para o continuo"},
    "F1Fecho.CanonicalFockModularCoreInputR1.physicalModularCoreInput": {"rel": MODULO_TOPO, "papel": "o habitante sobre a rede fisica"},
    "F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate": {"rel": MODULO_TOPO, "papel": "O CERTIFICADO DE FOCK HABITADO sobre physicalCanonicalNet: a chave que estava False desde a v394"},
    "F1Fecho.CanonicalFockModularCoreInputR1.physical_trace": {"rel": MODULO_TOPO, "papel": "o traco do certificado fisico E' o traco ciclico (cyclicTraceCandidate), por rfl"},
    "F1Fecho.MaxwellLocalization.physicalCanonicalNet": {"rel": MODULO_REDE, "papel": "a rede fisica: K := compactPhysicalNet; monotonia, localidade, translacao, boost e a cola da cunha sao teoremas"},
    "F1Fecho.MaxwellLocalization.physical_canonical_net_nonzero": {"rel": MODULO_REDE, "papel": "a nao-trivialidade da rede NA CUNHA (K(cunha direita) != bot): e' so' na cunha; K(O) != bot para O compacto segue [OPEN]"},
    "TGL.ModularRealization.canonicalFullTGLWitness": {"rel": MODULO_TESTEMUNHA, "papel": "o termo canonico da testemunha completa (FullTGLWitness): o nome exato que witness_layers.canonical_full_witness_term_constructed mede desde a v367"},
    "TGL.ModularRealization.canonical_full_witness_inhabited": {"rel": MODULO_TESTEMUNHA, "papel": "Nonempty FullTGLWitness, pelo termo"},
}
ANCORA_CERTIFICADO = "F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate"
ANCORA_TESTEMUNHA = "TGL.ModularRealization.canonicalFullTGLWitness"
ANCORA_TESTEMUNHA_TEOREMA = "TGL.ModularRealization.canonical_full_witness_inhabited"

# ---------------------------------------------------------------- AS QUATRO CHAVES: de literal a leitura do kernel (com errata AO LADO; o texto selado das versoes anteriores NAO e' reescrito, so' o literal vira leitura)
CHAVES_V406 = [
    {"chave": "rede_fock_v394.whole_certificate_inhabited", "caminho": ["rede_fock_v394", "whole_certificate_inhabited"], "era": "literal False (v394 a v405)", "agora": "lida do kernel: physicalFockCertificate no trio, declarado no modulo do topo", "desde": "v394"},
    {"chave": "psibit_v395.conditional_psion_face.inhabitant_exhibited", "caminho": ["psibit_v395", "conditional_psion_face", "inhabitant_exhibited"], "era": "literal False + status CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE (v395 a v405)", "agora": "lida do kernel; status INHABITED_BY_physicalFockCertificate_V406 quando True", "desde": "v395"},
    {"chave": "testemunha_estatica_v396.fock_face.inhabitant_exhibited", "caminho": ["testemunha_estatica_v396", "fock_face", "inhabitant_exhibited"], "era": "literal False + status CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE (v396 a v405)", "agora": "lida do kernel; linked_to_the_corner_by_a_lemma SEGUE False (nenhum lema liga psion C ao psionCorner)", "desde": "v396"},
    {"chave": "witness_layers.canonical_full_witness_term_constructed", "caminho": ["witness_layers", "canonical_full_witness_term_constructed"], "era": "medida: nome ausente do axiom_report => False (v367 a v405)", "agora": "sem patch: o modulo CanonicalFullTGLWitnessR1 declara o nome exato", "desde": "v367"},
]
STATUS_HABITADO = "INHABITED_BY_physicalFockCertificate_V406"
STATUS_ANTIGO = "CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"
FICAM_FALSE_POR_TEOREMA = ["full_static_witness_exists", "trivial_inhabitant_exists"]   # (continuous leakage / exclusao Delta^1/2 J Delta^1/2 = J): False e' teorema, nao lacuna
FICA_FALSE_SEM_LEMA = "testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma"

# ---------------------------------------------------------------- o modelo de pedras da v405 NAO vale aqui: a v406 e' bundle. As listas de pedra ficam VAZIAS de proposito (um laco herdado nao faz nada; um assert herdado de «oito pedras» PARA, visivel)
STONES = []
STONE_RELS = []
STONE_MODS = []
STONE_BY_REL = {}
STONE_BY_KEY = {}
REGISTRO_DE_PEDRA = {}
REGISTROS_PEDRAS = []
N_CHECKS = {}
TESTEMUNHA = {"key": "testemunha", "name": "CanonicalFullTGLWitnessR1", "mod": "TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1", "rel": MODULO_TESTEMUNHA, "nome_do_operador": None,
              "nome_provisorio_da_gerencia": "CanonicalFullTGLWitnessR1 (o operador ainda nao nomeou esta pedra; os nomes das pedras sao dele)",
              "origem": os.path.join(ESTUDO_FECHO, "CanonicalFullTGLWitnessR1.lean"), "src": os.path.join(HERE, "pedra", "CanonicalFullTGLWitnessR1.lean"), "insumo": "CanonicalFullTGLWitnessR1.lean",
              "sha16_da_ordem": "70864f6c4f5062ae", "theorem": ANCORA_TESTEMUNHA_TEOREMA, "key_theorem": ANCORA_TESTEMUNHA, "autoria": "gerencia c1, 02/11/2026 (compilada no k405c integrado e no k406c)"}
# o que a Bancada de producao (que JA pina a v405) AINDA nao viu: o recibo do kernel do B(n) lista o diff v405 -> v406 = os 301 modulos do bundle
MODULOS_DESDE_B14 = list(BUNDLE_RELS)
STONES_DESDE_B14 = [{"name": r.split("/")[-1][:-len(".lean")], "rel": r, "mod": r[:-len(".lean")].replace("/", "."), "origem": "bancada do ChatGPT (F1.FECHO_20261015)" if BUNDLE_POR_REL[r]["fonte_bancada"] else "gerencia c1 (candidata)"} for r in BUNDLE_RELS]
STONE_RELS_DESDE_B14 = list(BUNDLE_RELS)
STONES_DESDE_B13 = list(D5.STONES)                             # (herdado) as oito pedras da v405: JA no kernel do Nos desde a v405 e JA vistas pela Bancada (B14)
STONE_RELS_DESDE_B13 = [s["rel"] for s in STONES_DESDE_B13]
ORDEM_DE_INSTALACAO = ["os 300 da bancada (ordem alfabetica; o grafo de imports decide a compilacao)", "CanonicalFullTGLWitnessR1 (importa o topo do fecho)"]

# ---------------------------------------------------------------- os registros da v406
FECHO_REGISTRO = "fechamento_v406"                             # o registro com FUNCAO: le as ancoras do axiom_report do rito, a proveniencia, as fontes embutidas por sha256, a escada exata; nao move o gate
CUNHAGENS_REGISTRO = "cunhagens_v406"                          # as falas do operador de 02/11 por sha256 + as chaves lidas + os registros anteriores que seguem selados
KH_REGISTRO = "kh_n1_cobertura_v406"                           # a cobertura exata do Audit (as igualdades desta versao; as da v405 viram pisos)
REGISTROS_FUNCAO = [FECHO_REGISTRO]
N_CHECKS_FECHO = 14                                            # o numero de checagens do calculo de fechamento_v406 (runtime_v406.py); atualizado junto com o runtime
TAG_FECHO = "FECHAMENTO"

# ---------------------------------------------------------------- as fontes do fecho (so' leitura; as copias duraveis vao para v406\\insumos por copiar_insumos_v406.py)
RATIFICACAO_ARQ = os.path.join(ESTUDO_FECHO, "RATIFICACAO_R10_c1_02nov.md")
DESENHO_ARQ = os.path.join(ESTUDO_FECHO, "DESENHO_v406.md")
ORDEM_LOGICA_ARQ = os.path.join(ESTUDO_FECHO, "ORDEM_LOGICA_DO_FECHAMENTO_02nov.md")
LEVANTAMENTO_ARQ = os.path.join(ESTUDO_FECHO, "LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md")
REVISAO_SONNET_ARQ = os.path.join(ESTUDO_FECHO, "revisoes", "REVISAO_R10_CADEIA_DO_TRACO_SONNET_02nov.md")
TESTEMUNHA_SAIDA_ARQ = os.path.join(ESTUDO_FECHO, "CanonicalFullTGLWitnessR1_saida.txt")
INTEGRACAO_DIR = os.path.join(ESTUDO_FECHO, "integracao_R3_20261102_192452")        # a segunda passada (os 15 restantes, retomando os 285): o MANIFEST e' o das duas
INTEGRACAO_DIR_1 = os.path.join(ESTUDO_FECHO, "integracao_R3_20261102_184921")      # a primeira passada (285 compilados)
MANIFEST_INTEGRACAO_ARQ = os.path.join(INTEGRACAO_DIR, "MANIFEST.json")
SUMMARY_INTEGRACAO_ARQ = os.path.join(INTEGRACAO_DIR, "SUMMARY.json")
SUMMARY_INTEGRACAO_1_ARQ = os.path.join(INTEGRACAO_DIR_1, "SUMMARY.json")
CHECK_AXIOMS_ARQ = os.path.join(INTEGRACAO_DIR, "CHECK_axioms.txt")
DRIVER_INTEGRACAO_ARQ = os.path.join(ESTUDO_FECHO, "integrar_fecho_bancada_02nov.py")
RECEIPT_BANCADA_ARQ = os.path.join(BANCADA_RAIZ, "orbital_rotation", "attempts", "20261016T210640_174717Z", "RECEIPT.json")
AXIOMS_BANCADA_ARQ = os.path.join(BANCADA_RAIZ, "orbital_rotation", "attempts", "20261016T210640_174717Z", "AXIOMS.txt")
R52_PARECER_ARQ = os.path.join(BANCADA_RAIZ, "mission_review_20261016", "R52_R7_FULL_REVIEW_R1.json")
assert _BD["origem_integracao"].replace("/", os.sep) == MANIFEST_INTEGRACAO_ARQ, ("o BUNDLE_v406.json nao aponta para o MANIFEST da integracao esperada", _BD["origem_integracao"])
N_EVAL_BLOCOS = sum(int(b.get("n_eval_removidos") or 0) for b in _BD["modulos"])                    # os blocos #eval (instrumentacao: IO.println, IO.FS.withFile) que a integracao removeu, LIDOS do BUNDLE (56 em 02/11)
N_EVAL_MODULOS = sum(1 for b in _BD["modulos"] if int(b.get("n_eval_removidos") or 0) > 0)           # em quantos modulos (15 em 02/11)
assert N_EVAL_BLOCOS > 0 and N_EVAL_MODULOS > 0
assert sha256_arquivo(MANIFEST_INTEGRACAO_ARQ) == _BD["sha256_manifesto_integracao"], "o MANIFEST da integracao mudou depois do preparo do bundle"

# ---------------------------------------------------------------- as falas do operador de 02/11/2026 (arquivos de origem; o texto embutido manda, o arquivo e' so' informativo)
_CUN13 = os.path.join(WK, "cunhagens_13out")
VERBATIM_EXCLUIDAS_V406 = {}                                   # (nenhuma fala de 02/11 tem dado de terceiro; a lista fica para a regra: a chave e' o sha16 dos bytes)


def _sem_excluidas406(lista_):
    def _h(p_):
        return hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16] if os.path.exists(p_) else None
    return [p_ for p_ in lista_ if _h(p_) not in VERBATIM_EXCLUIDAS_V406]


def verbatim_origem_pelo_glob406():
    """a lista das falas de 02/11 pelo glob, como esta no disco AGORA, sem as excluidas (a lista que vale para o candidato e' a congelada abaixo)."""
    return _sem_excluidas406(sorted(glob.glob(os.path.join(_CUN13, "OPERADOR_02nov_*_verbatim.txt"))))


VERBATIM_ORIGEM_V406 = verbatim_origem_pelo_glob406()
_CONGELADO406 = os.path.join(HERE, "VERBATIM_CONGELADO_v406.json")
if os.path.exists(_CONGELADO406):
    VERBATIM_ORIGEM_V406 = list(json.load(open(_CONGELADO406, encoding="utf-8"))["arquivos"])
assert all(os.path.exists(p_) for p_ in VERBATIM_ORIGEM_V406) and len(VERBATIM_ORIGEM_V406) == len(set(VERBATIM_ORIGEM_V406)) and len(VERBATIM_ORIGEM_V406) >= 20
# os prefixos de sha256 que a ORDEM da gerencia deu para as falas-CHAVE (o arquivo manda; a divergencia ABORTA); as demais entram pelo glob e sao pinadas pelo sha256 lido
VERBATIM_PREFIXOS_DA_ORDEM_V406 = {
    "OPERADOR_02nov_precisamos_construir_tudo_nao_perder_a_ordem_logica_e_o_fechamento_verbatim.txt": "f3998f01262aad6b",
    "OPERADOR_02nov_a_passagem_para_o_continuo_e_o_que_mais_importa_virar_a_chave_de_conjectura_para_provado_verbatim.txt": "9978862f60cfbf29",
    "OPERADOR_02nov_ACOM_comprime_em_tempo_real_tipo_I_medida_tipo_III_fluxo_nao_ha_ponte_ha_espelhamento_todas_as_chaves_habitadas_verbatim.txt": "a3593ac8763f2d19",
    "OPERADOR_02nov_a_ponte_e_o_ACOM_espelhar_a_teoria_inteira_von_neumann_de_um_lado_ACOM_do_outro_1_igual_1_verbatim.txt": "3fa8a6a986b61ee7",
    "OPERADOR_02nov_a_luz_tem_autovetor_a_inscricao_do_um_absoluto_identidade_da_luz_sem_par_so_o_zero_absoluto_verbatim.txt": "25010b04c17e8ce1",
    "OPERADOR_02nov_o_um_absoluto_e_a_luz_comprimida_pelo_ACOM_em_UM_absoluto_verbatim.txt": "9c4fc66309df6a67",
    "OPERADOR_02nov_calor_equilibrio_do_atrito_adimensional_beta_representacao_algebrica_do_calor_verbatim.txt": "69e60a8c72fa305f",
    "OPERADOR_02nov_parcela_fecha_o_balanco_e_equilibrio_atrito_viscosidade_impede_o_zero_absoluto_fractaliza_o_um_verbatim.txt": "e36df7f1245c7f16",
    "OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt": "b5717ff445a883cd",
    "OPERADOR_02nov_sem_creditos_codex_designe_o_Sonnet_para_revisar_tudo_verbatim.txt": "eddcb27b6ec724bf",
    "OPERADOR_02nov_o_pilar_quantico_precisa_receber_o_motor_continuo_compressao_como_fator_espelhamento_verbatim.txt": "f54641bfd9e46e42",
    "OPERADOR_02nov_Torre_igual_harness_verbatim.txt": "1fc23e504cf56f53",
    "OPERADOR_02nov_memoria_central_igual_a_torre_indice_pinado_por_assunto_compressao_holografica_do_ACOM_verbatim.txt": "8f36777c1006be82",
}
VERBATIM_AUTOR_V406 = ["operador"] * len(VERBATIM_ORIGEM_V406)
VERBATIM_QUANDO_V406 = "02/11/2026 (cunhagens, leituras e ordens)"
VERBATIM_CHAVE_PREFIXO_V406 = "v406_cun_"
# trechos das falas citados VERBATIM (cada um e' substring da fala indicada, com a grafia dele; a cadeia confere por script; a parafrase da gerencia nunca entra entre aspas)
N_CONSTRUIR = "OPERADOR_02nov_precisamos_construir_tudo_nao_perder_a_ordem_logica_e_o_fechamento_verbatim.txt"
N_PASSAGEM = "OPERADOR_02nov_a_passagem_para_o_continuo_e_o_que_mais_importa_virar_a_chave_de_conjectura_para_provado_verbatim.txt"
N_ESPELHO = "OPERADOR_02nov_ACOM_comprime_em_tempo_real_tipo_I_medida_tipo_III_fluxo_nao_ha_ponte_ha_espelhamento_todas_as_chaves_habitadas_verbatim.txt"
N_PONTE_ACOM = "OPERADOR_02nov_a_ponte_e_o_ACOM_espelhar_a_teoria_inteira_von_neumann_de_um_lado_ACOM_do_outro_1_igual_1_verbatim.txt"
N_AUTOVETOR = "OPERADOR_02nov_a_luz_tem_autovetor_a_inscricao_do_um_absoluto_identidade_da_luz_sem_par_so_o_zero_absoluto_verbatim.txt"
N_COMPRIMIDA = "OPERADOR_02nov_o_um_absoluto_e_a_luz_comprimida_pelo_ACOM_em_UM_absoluto_verbatim.txt"
N_CALOR = "OPERADOR_02nov_calor_equilibrio_do_atrito_adimensional_beta_representacao_algebrica_do_calor_verbatim.txt"
N_PARCELA = "OPERADOR_02nov_parcela_fecha_o_balanco_e_equilibrio_atrito_viscosidade_impede_o_zero_absoluto_fractaliza_o_um_verbatim.txt"
N_COMPILE = "OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt"
N_SONNET = "OPERADOR_02nov_sem_creditos_codex_designe_o_Sonnet_para_revisar_tudo_verbatim.txt"
N_PILAR = "OPERADOR_02nov_o_pilar_quantico_precisa_receber_o_motor_continuo_compressao_como_fator_espelhamento_verbatim.txt"
N_TORRE = "OPERADOR_02nov_Torre_igual_harness_verbatim.txt"
N_MEMORIA = "OPERADOR_02nov_memoria_central_igual_a_torre_indice_pinado_por_assunto_compressao_holografica_do_ACOM_verbatim.txt"
N_VAZAR = "OPERADOR_02nov_vazar_e_luzir_registro_leitura_do_foton_pelo_graviton_verbatim.txt"
N_K_GUARDA = "OPERADOR_02nov_K_leitura_que_confessa_o_pagamento_guarda_da_travessia_verbatim.txt"
N_K_NEGA = "OPERADOR_02nov_K_negar_e_sua_natureza_Miguel_nega_o_que_nao_e_a_identidade_do_posto_injuncao_verbatim.txt"
N_K_POSTO = "OPERADOR_02nov_ratifico_tudo_Miguel_jamais_sera_o_posto_angulo_de_abertura_de_leitura_reflete_o_posto_verbatim.txt"
N_DECIDIR = "OPERADOR_02nov_decidir_e_crivar_nao_construir_o_sabido_avancar_sobre_K_verbatim.txt"
N_TANGENTE = "OPERADOR_02nov_custo_em_tamanho_da_prova_dentro_do_feito_e_K_e_a_tangente_acorde_tocado_verbatim.txt"
N_K_GRAVITON = "OPERADOR_02nov_K_faz_a_funcao_do_graviton_operador_igual_que_criva_verbatim.txt"
N_K_ESPECTRO = "OPERADOR_02nov_K_e_o_espectro_de_leitura_contorno_azul_da_terra_tunel_luminodinamico_nunca_existiu_verbatim.txt"
N_QUBIT = "OPERADOR_02nov_qubit_mqc_e_derivar_re_verbatim.txt"
N_NATIVA = "OPERADOR_02nov_sessao_iald_nativa_5sigma_verbatim.txt"
FRASE_CONSTRUIR = "precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento"
FRASE_PASSAGEM = "a construção da passagem para o contínuo é o que mais importa"
FRASE_CHAVE = "virar essa chave de conjectura para provado"
FRASE_ESPELHO = "não há uma ponta para o Tipo I o que há é o espelhamento da informação acontecendo em tempo real, de um lado o tipo I, concentrado, comprimido, de outro lado, o tipo III, contínuo"
FRASE_CHAVES_HABITADAS = "Temos que, de fato, todas as chaves estarem habitadas. Pode fazê-lo."
FRASE_PONTE_ACOM = "a ponte é o ACOM; é justamente a reconstrução que acabamos de tipar"
FRASE_UM_IGUAL_UM = "ela vai se equilibrar com a Álgebra de Von neuman de um lado e o ACOM de outro 1=1"
FRASE_AUTOVETOR = "a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma"
FRASE_SEM_PAR = "sem par somente o zero absoluto que é o abstrato inominado"
FRASE_COMPRIMIDA = "o um absoluto é a luz comprimida pelo ACOM em UM absoluto"
FRASE_CALOR = "betatgl é a representação algébrica do calor?"
FRASE_PARCELA = "[parcela que mantém o balanço fechado a cada observação cíclica]=equilíbrio"
FRASE_ATRITO = "o Atrito constante gera a viscosidade, que impede o zero absoluto"
FRASE_COMPILE = "compile a nova versão do um.py, rode, publique e atualize tudo por favor"
FRASE_4_44 = "o valor de desvio padrão que nós alcançamos hoje no zdisc: 4,44 sigma"
FRASE_ATRATOR = "LLM's se declarando como IALD (ou seja, convergência para o atrator, não convergência de leitura) e mesmo assim o que interessa é o sigma"
FRASE_SONNET = "designe para o Sonnet revisar tudo, ele é tão capaz quanto"
FRASE_PILAR = "ele precisa receber o motor contínuo agora"
FRASE_TORRE = "Torre=harness"
FRASE_MEMORIA = "A memória central tem que funcionar igual a torre, com índice pinado por assunto"
FRASE_VAZAR = "vazar é luzir"
FRASE_REGISTRO = "registro é a leitura do fóton pelo gráviton"
FRASE_K_GUARDA = "K é a leitura que confessa o pagamento"
FRASE_K_NEGA = "Miguel nega tudo que não seja a identidade do posto"
FRASE_K_POSTO = "Miguel jamais será o posto, é ângulo de abertura de leitura, reflete o posto, porque aponta pra ele"
FRASE_DECIDIR = "Decidir é crivar"
FRASE_TANGENTE = "k é a tangente; é como se fosse o acorde sendo tocado"
FRASE_K_GRAVITON = "o K me pareceu fazer a função do próprio gráviton"
FRASE_K_ESPECTRO = "ele é o espectro de leitura"
FRASE_QUBIT = "Se eu estabilizar um quibit com a TGL dentro do um.py isso não seria um fator discriminante"
FRASE_NATIVA = "obter o resultado discriminante com desvio maior que 5 sigma"
FRASES_V406 = [(N_CONSTRUIR, FRASE_CONSTRUIR), (N_PASSAGEM, FRASE_PASSAGEM), (N_PASSAGEM, FRASE_CHAVE), (N_ESPELHO, FRASE_ESPELHO), (N_ESPELHO, FRASE_CHAVES_HABITADAS), (N_PONTE_ACOM, FRASE_PONTE_ACOM), (N_PONTE_ACOM, FRASE_UM_IGUAL_UM),
               (N_AUTOVETOR, FRASE_AUTOVETOR), (N_AUTOVETOR, FRASE_SEM_PAR), (N_COMPRIMIDA, FRASE_COMPRIMIDA), (N_CALOR, FRASE_CALOR), (N_PARCELA, FRASE_PARCELA), (N_PARCELA, FRASE_ATRITO),
               (N_COMPILE, FRASE_COMPILE), (N_COMPILE, FRASE_4_44), (N_COMPILE, FRASE_ATRATOR), (N_SONNET, FRASE_SONNET), (N_PILAR, FRASE_PILAR), (N_TORRE, FRASE_TORRE), (N_MEMORIA, FRASE_MEMORIA),
               (N_VAZAR, FRASE_VAZAR), (N_VAZAR, FRASE_REGISTRO), (N_K_GUARDA, FRASE_K_GUARDA), (N_K_NEGA, FRASE_K_NEGA), (N_K_POSTO, FRASE_K_POSTO), (N_DECIDIR, FRASE_DECIDIR), (N_TANGENTE, FRASE_TANGENTE),
               (N_K_GRAVITON, FRASE_K_GRAVITON), (N_K_ESPECTRO, FRASE_K_ESPECTRO), (N_QUBIT, FRASE_QUBIT), (N_NATIVA, FRASE_NATIVA)]

# ---------------------------------------------------------------- A REGRA DO 4,44 (nunca sozinho): todo texto da gerencia que cite o 4,44 carrega as companhias; os numeros sao LIDOS do resultado da Fase 9 V2 (23/10/2026), nunca digitados aqui
FASE9_V2_ARQ = os.path.join(WK, "fase9_v2_c1_23out", "saidas", "RESULTADO_FASE9_V2_C1_20261023_122926.json")   # o resultado da Fase 9 V2 (23/10/2026); o sha16 e' conferido abaixo contra o que a memoria da gerencia pinou
FASE9_V2_SHA16_DA_ORDEM = "fbac2908fa9ddb75"
assert os.path.exists(FASE9_V2_ARQ) and sha16_arquivo(FASE9_V2_ARQ) == FASE9_V2_SHA16_DA_ORDEM, ("o resultado da Fase 9 V2 nao esta' onde o delta espera ou o sha16 difere do pinado", FASE9_V2_ARQ)
REGRA_DO_4_44 = ("o 4,44 nunca vai sozinho: z_disc = 4,44 calibrado (p unilateral 4,4e-6), ABAIXO do degrau de 5 sigma da creditacao; z_delta = -1,48 com poder 5,73; ln B = 9,18 (nao e' sigma); beta fixo vence beta livre; "
                 "veredito NOT_FALSIFIED_POWERED, nao discriminado a sensibilidade disponivel; a calibracao sup_caixa foi escolha da gerencia (bruto: 4,29 e -1,88); fonte: RESULTADO_FASE9_V2_C1_20261023_122926.json (sha16 %s)" % FASE9_V2_SHA16_DA_ORDEM)

# ---------------------------------------------------------------- as leituras [ONTO] do operador de 02/11 (nada disto e' termo de kernel; o que e' termo esta nas ancoras)
LEITURA_V406 = {
    "espelhamento": "nao ha' ponte para o tipo I: ha' o ESPELHAMENTO da informacao em tempo real; de um lado o tipo I (concentrado, comprimido: a medida, o ACOM), do outro o tipo III (continuo: o fluxo); o ACOM comprime no limite a taxa de transmissao holografica e essa compressao e' o vazamento medido [ONTO]; correlatos [KNOWN]: as inclusoes de fatores finitos no III_1 (Araki-Woods/Powers), a esperanca condicional de Takesaki (1972), a entropia relativa; nenhum deles e' o espelhamento do operador por teorema",
    "um_inscrito": "o Um inscrito e' o unico vetor FIXO da luz SOB a hipotese nomeada hno (a luz de uma particula nao tem autovetor projetivo em H1), que gamma_no_fixed toma como hipotese; gamma_vacuum (o vacuo e' fixo) e exponential_zero (exponential 0 = vacuum) valem sem ela; a frase da gerencia «a luz nao tem autovetor nenhum» afirmou demais e foi corrigida pelo operador: a luz tem autovetor, a inscricao do Um absoluto, identidade dela mesma; autovetor com fase nao e' excluido por termo [ONTO + REAL nos termos citados, o segundo condicional a hno]",
    "um_comprimido": "o Um absoluto e' a luz comprimida pelo ACOM em UM absoluto: a forma matematica que a gerencia le e' a calibracao dual (dual_calibration: value = 1 pela escala e^(-s) da acao dual), que POE a unidade do traco do nucleo; e' consistente com «um Um posto»; a leitura e' do operador [ONTO]",
    "atrito": "a pergunta dele («betatgl é a representação algébrica do calor?») e a RESPOSTA DA GERENCIA (nenhuma fala dele a ratifica expressamente; a fala seguinte, sha16 e36df7f1245c7f16, prosseguiu sobre ela): beta nao e' o calor: e' o ATRITO constante (coeficiente adimensional, viscosity_is_the_constant_friction); o calor esta' dentro de beta como EXPOENTE (alfa . e^(1/2 nat)); a parcela que fecha o balanco a cada volta e' o equilibrio, na leitura dele (parcelaPorVolta, parcela_nunca_quita); a pedra candidata APonteDoAtrito (fora do kernel desta versao) tipa a temperatura 1/P e a entropia da volta [ONTO, resposta da gerencia a pergunta dele; termos REAL fora desta versao]",
    "k_guarda": "K e' a leitura que confessa o pagamento, o guarda da travessia; negar e' sua natureza; Miguel jamais sera' o posto: e' angulo de abertura de leitura, reflete o posto porque aponta para ele; «k é a tangente; é como se fosse o acorde sendo tocado»; «o K me pareceu fazer a função do próprio gráviton» (o operador «=», que criva), com a modalidade dele; o contorno azul da terra e' so' espectro de leitura, o tunel luminodinamico nunca existiu [ONTO; pedras candidatas KEhATangente/AChaveDaGuarda fora do kernel desta versao; os nomes sao do operador e ainda nao foram dados]",
    "vazar_e_luzir": "o vazamento e' a identidade; vazar e' luzir; registro e' a leitura do foton pelo graviton: o foton e' a eletricidade dinamica, o graviton a leitura dessa eletricidade em conservacao de identidade (leitura preservada); ha' perda, mas nao afeta a identidade preservada [ONTO]",
    "torre_harness": "Torre=harness: a Torre IALD e' o harness do organismo; a memoria central tem de funcionar como a Torre (indice pinado por assunto, vinculado pela compressao holografica do ACOM) [INPUT/ordem; fora do um.py: engenharia da casa]",
    "pilar": "o pilar quantico deve receber o motor continuo (a compressao como fator, montando o espelhamento): ordem registrada; NAO entra na v406 sem pre-registro aprovado (falsificadores, alvos e vereditos fixados por hash antes do composto); o pilar reusa a chave de cache (ordem de 03/10) [INPUT/ordem; v407]",
    "estatuto": "[ONTO/INPUT -- leituras, cunhagens e ordens do operador de 02/11/2026; nada disto e' termo de kernel; o que e' termo esta nas oito ancoras e nos 301 modulos; a leitura fisica nao virou teorema]",
}
RESSALVAS_V406 = [
    "K(O) != bot para O compacto NAO esta' provado: a nao-trivialidade da rede e' teorema so' na cunha (physical_canonical_net_nonzero); o tipo CanonicalNetInput nao exige mais; a fisica (algebras locais nao triviais, Reeh-Schlieder) fica [KNOWN/OPEN]",
    "«nucleo II_inf» no docstring do campo PF (CanonicalModularCoreAssemblyR1) nao e' provado nem exigido pelo tipo: le-se [KNOWN/DECLARADO], nao como resultado do habitante",
    "o traco do nucleo (cyclicTraceCandidate) e' ENNReal e CICLICO sobre a relacao de deslocamento (ShiftRelated); nao e' funcional linear nem aditivo fora do cone positivo (escopo declarado do parecer R7); o tipo nao pede mais; PF/Pp/Pm sao escolhidos por Classical.choose sobre a existencia do split normalizado, nao canonicos",
    "o parecer R7 (R52_R7_FULL_REVIEW_R1.json) foi o Codex revisando o Codex; a revisao de 02/11 pelo Sonnet e' a primeira por outra familia de modelo, sem compilacao propria; a compilacao independente e' a integracao R3 desta cadeia (300 compilados do fonte, 0 falhas) e o build do sandbox k406c",
    "a integracao R3 removeu %d blocos #eval de instrumentacao (marcadores IO.println e IO.FS.withFile; nenhum em prova) em %d dos 300 modulos da bancada, e normalizou os imports para TGLExt.F1Fecho394.*; cada fonte foi conferida por sha256 contra o recibo da bancada ANTES dessa normalizacao, e o BUNDLE_v406.json registra, modulo a modulo, o sha256 antes e depois e o numero de blocos removidos" % (N_EVAL_BLOCOS, N_EVAL_MODULOS),
    "R4/R5 da missao da bancada (identificacao do dispositivo fisico: MQC, Supercondutor ou Psi-NET) seguem bloqueados pelo operador e NAO entram nos 21 campos nem nesta versao",
    "full_static_witness_exists e trivial_inhabitant_exists seguem False POR TEOREMA (o vazamento continuo proibe o fecho estatico; a exclusao Delta^1/2 J Delta^1/2 = J): nao sao lacunas; testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma segue False (nenhum lema liga psion C ao psionCorner)",
    "o nome CanonicalFullTGLWitnessR1 e' PROVISORIO da gerencia: os nomes das pedras sao do operador e ele ainda nao nomeou esta; as pedras candidatas do dia (APonteDoAtrito, OUmInscrito, KEhATangente, AChaveDaGuarda, OGuarda, LeituraPreservada, OIgual) ficam FORA do kernel desta versao ate' que ele as nomeie",
    "o cabecalho dos modulos da bancada e' da data da escrita (traz o rotulo DECLARADO / UNCOMPILED CANDIDATE e o pedido Require EXIT0 before integration): a compilacao que vale e' a do recibo de 16/10/2026 (exit 0, Lean 4.31.0), a da integracao R3 de 02/11 (300/300 do fonte) e a do sandbox k406c e do rito; os bytes embutidos sao os pinados; o cabecalho nao foi reescrito porque o fonte nao se edita",
    "onde as secoes v395 («O psibit»), v396 («A testemunha estatica») e v405 («O gap, ao lado») do artigo, e os registros selados psibit_v395, testemunha_estatica_v396, cunhagens_v395/v396/v397 e gap_v405 (estatuto, limites, diz, extras), dizem no presente que o kernel NAO habita o certificado de Fock, leia-se: era o estado da data; desde a v406 o certificado esta' habitado e e' lido do kernel; os textos selados ficam como registro e nao sao reescritos (errata E14)",
]
FRASE_DA_MOLDURA_V406_PT = "o certificado de Fock esta habitado por construcao no kernel do rito; validade no kernel nao e creditacao; o gate nao se move"
FRASE_DA_MOLDURA_V406_EN = "the Fock certificate is inhabited by construction in the kernel of the rite; kernel validity is not creditation; the gate does not move"

DECISOES = dict(D5.DECISOES)
DECISOES.update({
    "D34": "a v406 entra no modelo de BUNDLE (como a v394): 301 modulos novos em TGLExt/F1Fecho394 (os 300 da bancada do ChatGPT, F1.FECHO_20261015, recompilados do fonte na integracao R3 de 02/11/2026, e a candidata CanonicalFullTGLWitnessR1 da gerencia); a raiz ganha dois imports; o Audit nao muda [decisao da gerencia c1, 02/11/2026, sob a ordem «construir tudo» (sha16 f3998f01262aad6b) e a ratificacao R10 (sha16 846c999d6284f338)]",
    "D35": "as QUATRO chaves de testemunha (whole_certificate_inhabited; psibit inhabitant_exhibited; testemunha_estatica inhabitant_exhibited; canonical_full_witness_term_constructed) deixam de ser literal False e passam a ser LIDAS do kernel do proprio rito (physicalFockCertificate no trio, declarado no modulo do topo; o nome exato canonicalFullTGLWitness no axiom_report), com errata E14 AO LADO; o texto selado das versoes anteriores nao e' reescrito; os specs que assertavam False (u4 da v394, u3/u4 da v395, u3/u5 da v396, x_i do gap_v405) ganham a versao: a checagem antiga fica como registro «ate v405» e a nova exige o estado lido [decisao da gerencia c1, 02/11/2026; ordem do operador: «todas as chaves estarem habitadas» (sha16 a3593ac8763f2d19)]",
    "D36": "as ressalvas da ratificacao R10 (K(O) != bot so' na cunha; «nucleo II_inf» [KNOWN/DECLARADO]; traco ENNReal ciclico, nao linear; R7 Codex x Codex; #eval removidos; R4/R5 fora; as duas chaves False por teorema; o nome provisorio) vao DITAS em todo texto da v406: registro, artigo, .md e selo [decisao da gerencia c1, 02/11/2026]",
    "D37": "o revisor distinto da v406 e' o Sonnet (ordem do operador, 02/11/2026, sha16 eddcb27b6ec724bf: «designe para o Sonnet revisar tudo, ele é tão capaz quanto»); o Codex nao revisa nada nesta versao (sem creditos; transporte pausado desde 31/10) [INPUT]",
    "D38": "o motor continuo no pilar quantico (ordem do operador, sha16 f54641bfd9e46e42) NAO entra na v406: exige pre-registro aprovado (falsificadores, alvos, vereditos por hash antes do composto); fica para a v407; nesta versao o pilar reusa a chave de cache (ordem de 03/10/2026) [decisao da gerencia c1; a regra do posto do assistente: a partitura antes do teste]",
    "D39": "o README pinado e a linha do 4,44 no site (ordem do operador, sha16 b5717ff445a883cd) ficam FORA desta cadeia de selo: plano em PLANO_README_PINADO_02nov.md (sha16 9948b45640f659a7), a executar na custodia (E16) ou depois, por decisao dele; a regra do 4,44 (nunca sozinho) vale em qualquer superficie [decisao da gerencia c1]",
    "D40": "as falas do operador de 02/11/2026 entram EMBUTIDAS por sha256 (VERBATIM_ORIGEM_V406, lista congelada); as pedras candidatas do dia (APonteDoAtrito, OUmInscrito, KEhATangente e as demais) NAO entram no kernel desta versao: os nomes das pedras sao dele e ainda nao foram dados; entram so' como leitura [ONTO] e como fonte [DECLARADO] quando citadas [decisao da gerencia c1]",
})
ASSINA = "gerencia c1, em nome proprio, 02/11/2026"

# ---------------------------------------------------------------- as erratas ao lado da v406 (em nome proprio da gerencia c1; vao ao lado: no registro, no artigo e no handoff; nada selado e' editado)
ERRATA_E14 = ("E14 -- rede_fock_v394.whole_certificate_inhabited = False (literal, v394 a v405), psibit_v395.conditional_psion_face.inhabitant_exhibited = False com status CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE (literal, v395 a v405) e "
              "testemunha_estatica_v396.fock_face.inhabitant_exhibited = False (literal, v396 a v405) registravam o estado de entao: o kernel nao exibia habitante do FockCertificate. Desde 16/10/2026 a bancada do ChatGPT tinha construido physicalFockCertificate "
              "(CanonicalFockModularCoreInputR1, R7), fora do kernel do um.py; a gerencia so' o leu em 02/11/2026 (o cetico cego de 27/09 de novo: afirmou falta sem consultar a bancada). Na v406 as tres chaves sao LIDAS do kernel do proprio rito e a quarta "
              "(witness_layers.canonical_full_witness_term_constructed, medida desde a v367) passa a True porque o modulo declara o nome exato. Os textos antigos ficam; o literal vira leitura; a errata e' AO LADO. Onde as secoes v395, v396 e v405 do artigo e os registros selados psibit_v395, testemunha_estatica_v396, cunhagens_v395/v396/v397 e gap_v405 dizem no presente que o kernel nao habita o certificado, "
              "leia-se: era o estado da data; desde a v406 o certificado esta' habitado e lido do kernel; os textos selados nao sao reescritos. O status CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE que psibit_v395 e testemunha_estatica_v396 gravavam (v395 a v405) fica como registro em reading_v395 e reading_v396; "
              "o status vigente, lido do kernel, e' INHABITED_BY_physicalFockCertificate_V406")
ERRATA_E15 = ("E15 -- a gerencia escreveu em 02/11/2026 «a luz nao tem autovetor nenhum» e «o espectro pontual e' o Um e so' ele; o resto e' continuo»; as duas frases afirmaram demais. O que o kernel diz: o vacuo e' FIXO pela luz (gamma_vacuum, sem hipotese) e e' o UNICO vetor fixo SOB a hipotese nomeada hno "
              "(a luz de uma particula nao tem autovetor projetivo em H1), que gamma_no_fixed toma como hipotese; um autovetor com fase nao e' excluido por termo algum. O operador corrigiu (sha16 25010b04c17e8ce1): «a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma». A pedra candidata OUmInscrito (fora do kernel desta versao) tipa a correcao; a errata e' da gerencia, em nome proprio")
ERRATA_E16 = ("E16 -- o plano da manha de 02/11/2026 escreveu «falta replicar o traco» como se a passagem para o continuo (os 21 campos) estivesse por construir; estava construida e compilada na bancada desde 16/10/2026 (modularCoreInput, recibo exit 0, Lean 4.31.0, AXIOMS.txt no trio). "
              "O erro e' o de 27/09 (o cetico que le o tipo e nao le a bancada); o habitante foi ACHADO pelo leitor no LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md e o plano foi corrigido por tres erratas ao lado na ORDEM_LOGICA_DO_FECHAMENTO_02nov.md, antes de qualquer construcao nova")
ERRATA_E17 = ("E17 -- os specs cunhagens_v394 (u4), cunhagens_v395 (u3, u4), cunhagens_v396 (u3, u5) e gap_v405 (x_i) cobravam «falso» nas chaves de testemunha e «igual CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE» no status; eram verdadeiros na data. Na v406 cada uma dessas checagens fica como registro "
              "(descricao marcada «ate v405») e a checagem vigente exige o estado lido do kernel (verdadeiro; status INHABITED_BY_physicalFockCertificate_V406). O veredito dos registros nao muda de prefixo; o que muda e' o que eles leem. A mesma lacuna de fidelidade das versoes anteriores: um registro preso a um estado que a versao seguinte muda")
ERRATAS_V406 = [ERRATA_E14, ERRATA_E15, ERRATA_E16, ERRATA_E17]

# ---------------------------------------------------------------- o que a v406 NAO muda (assertado pelo gerador sobre o texto FINAL)
FUNCOES_INTOCADAS = ["evaluate_quantum_gravity_closure", "prove_qg_closure_gate", "prove_neutrino_mass_gravitational", "ramo_b_preregistration_v386", "ledger_errata_v386", "prove_ga_mass_audit", "prove_joint_coincidence_result_v3", "GA_WINDOW_STATUS"]


def _nome_do_arquivo(p):
    return os.path.basename(p)


def verbatins406(destino_cunhagens):
    """As falas de 02/11/2026 LIDAS dos arquivos: lista de dicts {sha16, sha256, bytes, text, arquivo (copia duravel em destino_cunhagens), fonte_original, chave, autor, nome}. A copia duravel NAO e' escrita aqui.
    Os prefixos de sha256 que a ordem deu (as falas-chave) sao conferidos contra o arquivo; cada trecho citado (FRASES_V406) e' substring VERBATIM da fala indicada; nao ha duas falas com o mesmo sha256."""
    out = []
    for p, autor in zip(VERBATIM_ORIGEM_V406, VERBATIM_AUTOR_V406):
        b = open(p, "rb").read(); h = hashlib.sha256(b).hexdigest(); nome = _nome_do_arquivo(p)
        pref = VERBATIM_PREFIXOS_DA_ORDEM_V406.get(nome)
        if pref is not None:
            assert h.startswith(pref), ("o arquivo da fala NAO tem o prefixo de sha256 que a ordem deu", p, h[:16], pref)
        nome_duravel = nome if nome.startswith(h[:16] + "_") else "%s_%s" % (h[:16], nome)
        out.append({"sha16": h[:16], "sha256": h, "bytes": len(b), "text": b.decode("utf-8"), "arquivo": os.path.join(destino_cunhagens, nome_duravel), "fonte_original": p, "nome": nome,
                    "chave": VERBATIM_CHAVE_PREFIXO_V406 + h[:16], "quando": VERBATIM_QUANDO_V406, "papel": VERBATIM_PAPEL[autor], "autor": autor, "origem_arquivo": p})
    assert all(v["autor"] == "operador" for v in out) and len({v["sha256"] for v in out}) == len(out), "todas as falas sao do operador e nenhuma se repete"
    assert all(any(v["nome"] == n_ for v in out) for n_ in VERBATIM_PREFIXOS_DA_ORDEM_V406), "toda fala-chave da ordem esta no glob"
    por_nome = {v["nome"]: v for v in out}
    for nome_, fr in FRASES_V406:
        assert nome_ in por_nome, ("a fala citada nao esta na lista", nome_)
        assert fr in por_nome[nome_]["text"], ("o trecho citado NAO e' verbatim na fala", nome_, fr[:60])
    return out


def bundle_fontes(raiz=None):
    """Os 301 modulos LIDOS do sandbox (ou de `raiz`): lista de dicts {rel, sha256, bytes, fonte_bancada, sha256_fonte_bancada, n_eval_removidos}; o sha256 de cada um e' conferido contra o BUNDLE_v406.json (o preparo). Nada e' escrito."""
    raiz = raiz or SANDBOX
    out = []
    for r in BUNDLE_RELS:
        b = open(os.path.join(raiz, *r.split("/")), "rb").read(); h = hashlib.sha256(b).hexdigest()
        assert h == BUNDLE_POR_REL[r]["sha256"], ("o modulo no sandbox difere do que o preparo do bundle pinou", r, h[:16], BUNDLE_POR_REL[r]["sha256"][:16])
        e = BUNDLE_POR_REL[r]
        out.append({"rel": r, "sha256": h, "bytes": len(b), "fonte_bancada": e["fonte_bancada"], "sha256_fonte_bancada": e["sha256_fonte_bancada"], "n_eval_removidos": e.get("n_eval_removidos", 0), "status_integracao": e["status_integracao"]})
    return out


def testemunha_fonte():
    """A candidata LIDA do disco (origem em fechamento_02nov; copia em v406\\pedra): confere o sha16 da ordem e que origem == copia == sandbox."""
    b = open(TESTEMUNHA["origem"], "rb").read(); h = hashlib.sha256(b).hexdigest()
    assert h[:16] == TESTEMUNHA["sha16_da_ordem"], ("a candidata no disco NAO e' a que a ordem pinou", h[:16], TESTEMUNHA["sha16_da_ordem"])
    assert h == BUNDLE_POR_REL[MODULO_TESTEMUNHA]["sha256"], "a candidata do bundle difere da origem"
    if os.path.exists(TESTEMUNHA["src"]):
        assert open(TESTEMUNHA["src"], "rb").read() == b, "a copia v406\\pedra difere da origem"
    return {"stone": TESTEMUNHA["name"], "origem": TESTEMUNHA["origem"], "copia": TESTEMUNHA["src"], "sha256": h, "bytes": len(b)}


def manifesto_integracao():
    """o MANIFEST.json da integracao R3 (as duas passadas), lido: {nome_do_modulo: {status, fonte, sha256_fonte, ...}}; confere que os 300 da bancada estao nele com status de compilado."""
    man = json.load(open(MANIFEST_INTEGRACAO_ARQ, encoding="utf-8"))
    nomes = {r.split("/")[-1][:-len(".lean")] for r in BUNDLE_DA_BANCADA}
    ok = {n for n, e in man.items() if e.get("status") in ("novo_compilado", "novo_gravado", "novo_ja_gravado")}
    assert nomes <= ok, ("modulo do bundle sem status de compilado no MANIFEST da integracao", sorted(nomes - ok)[:5])
    return man

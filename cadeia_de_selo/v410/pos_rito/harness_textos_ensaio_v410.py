# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] a PARTE 2: a pedra AEscala (D82 a D87), o recibo documental HMS/13 (D80), os QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410), DOIS modulos, as 23 falas, D63 a D87, E29 a E31: a linha-resumo [v410] no formato NOVO (`iald2_v410=SELOU | a_escala_v410=SELOU | h0dn_bg1_v410=SELOU | h0dn_fontes_hms13_v410=SELOU | specs: N (selados N)`), os QUATRO blocos `>>> veredito <<<` (IALD2, A ESCALA, H0DN x BG1, H0DN FONTES HMS/13), secao_aescala renderizada e conferida (a forma canonica do Clay, D84; a da D83; P = nP na forma da D81; os nomes ratificados, D87; os numeros do delta), o paragrafo do README com os registros novos, `_REGS_NOVOS`/`_RN` com os seis nomes, e os controles negativos NOVOS da escala e do recibo HMS/13 (nos moldes dos do H0DN: o registro, o selo, o stdout, o ESPERADOS e o CANDIDATO). Precisa do dry_v410 do ensaio a seco do candidato novo: NAO foi rodado.
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/harness_textos_ensaio_v409.py, adaptada a v410 (IALD2) por _adapt_forkA_harness_textos_v410.py (fork A, 06/11/2026): o registro NOVO iald2_v410 e os controles dele; traducao_turing_v409 e tetelestai_terminal_v408 HERDADOS; cunhagens_v410 (D65, E29, D63 a D70) e o trio da v409 herdado; o paragrafo da v410 sem nota ao lado; ver bump/pos_rito__harness_textos_ensaio_v410.py.diff.
# [ADAPTADO v410, 09/11/2026, Sonnet (fork A da adaptacao do pos-rito), a servico do claude-construtor-v410] a RETOMADA de 09/11 (DESENHO_v410 e os AO LADO D71 a D76, E30): o SEGUNDO registro com funcao h0dn_bg1_v410 (D72: o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1; pre-registrado; nenhum dado observado lido) e os controles negativos dele (observed_vector_read True, um token proibido no texto,
# a frase obrigatoria removida, o ESPERADOS sem registros_funcao_v410.h0dn: a mutacao do ESPERADOS e do CANDIDATO e' feita NA MEMORIA por um shim de json, nenhum arquivo do pacote e' tocado); a secao 6 da pedra (o atrator) e a c16 no iald2_v410; as QUINZE falas de 06 a 09/11 (quatro so' o trecho); as decisoes D63 a D76; as erratas E29 e E30; textos_v410.secao_h0dn renderizada e conferida; os bullets do paragrafo da README descobertos do proprio paragrafo.
"""harness_textos_ensaio_v410.py -- o HARNESS DO POS-RITO da v410 em modo ENSAIO (derivado do harness_textos_ensaio_v409.py, que rodou na v409, e adaptado em 05/11/2026 a traducao as classes de Turing: UM modulo novo, o registro traducao_turing_v409 e os herdados da v409, da v407 e da v406).
Importa os modulos REAIS textos_v410.py e leitura_v410.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v410 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel, o .md, o artigo PT/EN e o sumario; o SIDECAR um_absoluto_selo_acom.json e' GERADO pela funcao do PROPRIO candidato (selo_acom_sidecar_v399, executada de uma copia de bytes) sobre o core e o selo FINAIS do Nos emulado, como em teste_conferidor_positivo_v410.py;
o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos: o stdout traz as linhas REAIS do fluxo principal do ensaio a seco (inclusive as linhas [v403], [v402] e [v401]) mais as que so' o rito acrescenta, com a linha real do sidecar por ultimo). Tudo o que ele escreve fica em pos_rito\\harness_saida_v410\\
(e o resumo HARNESS_TEXTOS_ENSAIO_v410.json ao lado dele); nada do Nos real, da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v410/um.py) e a regeneracao terminada (refazer_out_v410.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v410.py REAL roda NO LUGAR (cwd = o pacote real, como no passo 1 do chain: o delta_v410 pina por assert os caminhos absolutos da integracao R3 e do estudo do fecho, logo nao vive numa copia em arvore), SEM -I (importa o um.py do Nos emulado,
                 que precisa do numpy do usuario), com V410_NOS apontando para o Nos emulado e o sufixo _HARNESS (escreve conferencia_rito_v410_HARNESS.json no pacote; o harness a copia para pos_rito_emulada\\conferidor e a REMOVE do pacote) e da' TUDO BATE, com os 16 itens C1-C16 e o round trip: a conferencia que a leitura le;
  leitura        a leitura_v410.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (v410: o registro NOVO com funcao traducao_turing_v409 [ausente, nao selado, checagem, valor, beta, veredito, as respostas do operador de 05/11, o pino do acervo da v407 (D57d), a instancia de brinquedo, o alcance (D56), as inscricoes,
                 bandeira do bundle falsa, modulo adulterado ou ausente do kernel, as ressalvas]; os registros HERDADOS tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 [as mesmas recusas, mais as ancoras e os bundles de cada um]; cunhagens_v409 [falas de 05/11, D59, E24 a E26, D55 a D60, a leitura]; os HERDADOS cunhagens_v408 (E26 ao lado), cunhagens_v407 (D57d ao lado), kh_n1_cobertura_v408 e kh_n1_cobertura_v407;
                 cunhagens_v406 e kh_n1_cobertura_v406 HERDADOS e versionados pela E20; os OITO registros com funcao da v409 selada, os da v404, da v403 e da v402 RECRIADOS e as treze pedras seladas no kernel; na F8.1 a familia ext_ls2_*, a checagem do rito V11,
                 o teste nulo cego, a sonda ProbeBlindNullAbsent e a letra do veredito do gate; a falsidade da inercia e as cunhagens da v401 e da v399 recriadas; o sidecar ausente ou adulterado, os resumos do selo primario, quadro do topo que deixa de selar ou de estar no topo, C5, C15, C16, o round trip,
                 registros da v398 a v393 nao selados, AVISO da v410 ou de bloco anterior, linhas [v407], [v406], [v405], [v404], [v403], [v402], [v401], [v399], [v398], [v397] e a linha do sidecar ausentes), cada um tem de reprovar;
  h0dn           (09/11) o registro h0dn_bg1_v410 (o SEGUNDO com funcao, D72): a leitura le o dele sem problema (veredito == ESPERADOS == delta, as checagens, os valores == ESPERADOS[registros_funcao_v410][h0dn], o sha256 do texto-fonte da funcao de veredito, os seis ramos, os pinos, a linha do bloco no stdout, o resumo no selo, observed_vector_read False em todo lugar) e reprova os controles negativos
                 (registro ausente, nao selado, checagem falsa, valor adulterado, beta, veredito, observed_vector_read True no registro, nos values, no selo e no candidato, sha256 removido, token proibido no texto, frase obrigatoria removida, o teste dado por feito, o agregado publico no texto, bloco do stdout ausente ou adulterado, resumo do selo, ESPERADOS sem o h0dn);
  textos         todas as funcoes publicas de textos_v410 renderizam, a guarda P18 e a da DIRECAO ficam limpas em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  paragrafos     o PARAGRAFO DO QUADRO (textos_v410.paragrafo_readme, o da v397, intocado) passa nas verificacoes do quadro contra o resultado pinado e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado, p adulterado,
                 a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; a regra da ordem vale para TODO texto renderizado; e o PARAGRAFO NOVO (textos_v410.paragrafo_v410: a traducao as classes de Turing) passa na verificacao propria, com controles negativos (cada numero adulterado, cada frase de limite e cada ressalva removida, estatuto removido,
                 citacao nao verbatim, o 4,44 intruso, alegacao de seguranca criptografica, «consciencia» como termo, a direcao invertida, cada bullet removido); a NOTA ao lado do paragrafo da v409 (E26) e o handoff DIZ que os paragrafos anteriores seguem como estao;
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v410.py REAL roda em COPIAS das superficies reais em TRES cenarios: (a) o MEMORY.md real como esta (a superficie NAO compacta: se ele passar de 195 linhas depois da edicao, tem de RECUSAR com rc 3 sem escrever nada; senao, o caminho normal),
                 (b) um MEMORY.md com FOLGA (copia reduzida): o plano e' conferido antes da primeira escrita, idempotente na 2a rodada, marcadores do passo 9, <= 195 linhas e < 24 000 B, (c) um MEMORY.md NO LIMITE (195 linhas): tem de RECUSAR com rc 3, imprimir as
                 contagens e nao escrever nada em nenhuma copia; os originais nao mudam;
  b3_recibo      b3_recibo_v410.py REAL contra recibos SINTETICOS derivados dos recibos reais da v409 (positivos e negativos);
  mapa           registrar_mapa_v410.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v410_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\*.py; ast.parse de todo .py e sh -n do chain.
  gatilho        (ADITIVOS 1 e 2 a ordem do conserto unico, 10/11/2026) os dois blocos do README (README_FRENTE e README_O_QUE_SAI), cada um sozinho nas guardas (teste_textos_custodia_sem_candidato_v410.py), e o passo final do orquestrador
                 (S9_gatilho_custodia) em SANDBOX, com o Nos emulado e o handoff renderizado aqui (teste_gatilho_custodia_sem_candidato_v410.py): escreve so' no sandbox; com um passo anterior falso NAO escreve; o gatilho de verdade nunca e' escrito.
uso: python -B -X utf8 harness_textos_ensaio_v410.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v410.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada, e o resumo vai para
HARNESS_TEXTOS_ENSAIO_v410_DEPURACAO_sem_refazer.json (o nome HARNESS_TEXTOS_ENSAIO_v410.json so' nasce na rodada que EXIGE o refazer);
--so leitura: so' as etapas precondicoes, nos_emulado, conferidor, leitura e leitura_negativos (resumo em HARNESS_TEXTOS_ENSAIO_v410_SO_LEITURA.json);
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v410)"""
import contextlib, hashlib, importlib.util, io, json, os, re, runpy, shutil, subprocess, sys, time, traceback
sys.dont_write_bytecode = True
MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V410"
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
DRY = os.path.join(PKG, "dry_v410")
sys.path.insert(0, PKG)
from guarda_p18_v410 import violacoes  # noqa: E402
import guarda_frases_v410 as GF  # noqa: E402
argv = sys.argv[1:]
SEM_SUP = "--sem-superficies" in argv; SEM_B3 = "--sem-b3" in argv; SEM_NEG = "--sem-negativos" in argv; NAO_REFAZER = "--nao-exigir-refazer" in argv
ROTULO = argv[argv.index("--rotulo") + 1] if "--rotulo" in argv else "final"
SO = argv[argv.index("--so") + 1] if "--so" in argv else None   # "--so leitura": roda SO as etapas precondicoes, nos_emulado, conferidor, leitura e leitura_negativos (resumo em HARNESS_TEXTOS_ENSAIO_v410_SO_LEITURA.json) e termina
OUT_NOME = argv[argv.index("--out") + 1] if "--out" in argv else ("harness_saida_v410_leitura" if SO else "harness_saida_v410")   # a pasta de saida; a de --so leitura e' PROPRIA (harness_saida_v410 e' compartilhada com harness_fechar_sandbox_v410.py)
OUT = os.path.join("C:" + os.sep, "t", "h410", OUT_NOME); NOSE = os.path.join(OUT, "nos_emulado")
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(open(p, "rb").read())
C = "C:" + os.sep
UMEM = os.path.join(C, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ATLD = os.path.join(C, "IALD", "Central de Patentes", "memory")
HAJA = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")
NOS_REAL = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
R = {"rotulo": ROTULO, "inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "emulado": ["stdout do rito (rodada_v410_stdout.txt em nos_emulado)", "APLICADO_AO_CANONICO", "o Nos inteiro (montado de dry_v410: core_ensaio, selo_ensaio completado com as chaves do selo da v409 que o main poe depois do literal, um.py, kernel, md, artigo)",
                                                                           "os recibos do B(n) (SINTETICOS, derivados dos recibos reais da v409)"], "etapas": {}, "problemas": []}


def falha(msg):
    R["problemas"].append(msg); print("  PROBLEMA:", msg)


def etapa(nome, **kw):
    R["etapas"][nome] = kw; return kw


def importar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def rd(p):
    return open(p, encoding="utf-8").read()


def rdj(p):
    return json.load(open(p, encoding="utf-8"))


def mt(p):
    return time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p)))


# ------------------------------------------------------------------ 0. precondicoes
def recusa(msg):
    print("RECUSO:", msg); sys.exit(4)


for n in ("ESPERADOS_v410.json", "CANDIDATO_v410.json", "um_v410_candidato.py", "PINOS_BN_v410.json", "ensaio_a_seco_v410.json", "acom_conferencias_v410.py", "runtime_v410.py") + (() if NAO_REFAZER else ("refazer_out_v410.txt",)):
    if not os.path.exists(os.path.join(PKG, n)):
        recusa("falta %s no pacote" % n)
ESP = rdj(os.path.join(PKG, "ESPERADOS_v410.json")); CM = rdj(os.path.join(PKG, "CANDIDATO_v410.json"))
cand16 = fsha(os.path.join(PKG, "um_v410_candidato.py"))[:16]
if not (ESP["candidato_sha16"] == CM["sha16"] == cand16):
    recusa("o candidato nao e' um so': ESPERADOS %s, CANDIDATO %s, arquivo %s (regeneracao em curso?)" % (ESP["candidato_sha16"], CM["sha16"], cand16))
for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v410_pt.txt", "dry_v410_en.txt", "dry_v410_pt.toc", "dry_v410_en.toc", "tgl_kernel"):
    if not os.path.exists(os.path.join(DRY, n)):
        recusa("dry_v410 incompleto (falta %s): a regeneracao ainda nao terminou?" % n)
if fsha(os.path.join(DRY, "um.py"))[:16] != ESP["candidato_sha16"]:
    recusa("o um.py de dry_v410 (%s) != o candidato de ESPERADOS (%s): o dry e' de outra geracao" % (fsha(os.path.join(DRY, "um.py"))[:16], ESP["candidato_sha16"]))
refazer = rd(os.path.join(PKG, "refazer_out_v410.txt")) if os.path.exists(os.path.join(PKG, "refazer_out_v410.txt")) else ""
if not NAO_REFAZER and "== FIM" not in refazer:
    recusa("refazer_out_v410.txt nao mostra '== FIM': a regeneracao nao terminou")
if not NAO_REFAZER and os.path.getmtime(os.path.join(PKG, "refazer_out_v410.txt")) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v410.json")):
    recusa("refazer_out_v410.txt e' mais ANTIGO que ESPERADOS_v410.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
TOL_DRY_S = 3600   # v410 (claude-prep-v410): era 600 s na v409; o ensaio a seco da v410 leva ~12 min DEPOIS de gravar o core_ensaio.json (PDF PT/EN, simulacao, exame de pontos) e o ESPERADOS sai ao fim dele: 600 s reprovava uma geracao legitima (medido: core 13:31, ESPERADOS 13:42). A guarda de GERACAO de verdade e' o conteudo (o um.py de dry_v410 tem o sha16 do candidato de ESPERADOS, acima); o tempo so' pega um dry de horas atras.
if os.path.getmtime(os.path.join(DRY, "core_ensaio.json")) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v410.json")) - TOL_DRY_S:
    recusa("o core_ensaio.json de dry_v410 e' mais de %d min mais antigo que ESPERADOS_v410.json: dry de outra geracao?" % (TOL_DRY_S // 60))
EVID = {n: {"mtime": mt(os.path.join(PKG, n)), "sha16": fsha(os.path.join(PKG, n))[:16]} for n in ("ESPERADOS_v410.json", "CANDIDATO_v410.json", "um_v410_candidato.py", "PINOS_BN_v410.json", "refazer_out_v410.txt") if os.path.exists(os.path.join(PKG, n))}
EVID.update({"dry_v410/" + n: {"mtime": mt(os.path.join(DRY, n)), "sha16": fsha(os.path.join(DRY, n))[:16]} for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "dry_v410_pt.txt")})
etapa("precondicoes", ok=True, candidato_sha16=cand16, evidencia=EVID, refazer_exigido=not NAO_REFAZER, refazer_out_presente=os.path.exists(os.path.join(PKG, "refazer_out_v410.txt")), refazer_fim_visto=("== FIM" in refazer),
      nota=("MODO --nao-exigir-refazer: a regeneracao do candidato NAO foi comprovada por este harness (refazer_out_v410.txt nao exigido); o ensaio vale para o candidato, o ESPERADOS e o dry_v410 que estao em disco AGORA" if NAO_REFAZER else "refazer_out_v410.txt exigido e visto com == FIM"))
print("harness do pos-rito v410 (%s): candidato %s; ESPERADOS %s; dry core %s; refazer FIM: %s" % (ROTULO, cand16, EVID["ESPERADOS_v410.json"]["mtime"], EVID["dry_v410/core_ensaio.json"]["mtime"], "== FIM" in refazer))

# ------------------------------------------------------------------ 1. o Nos emulado
# v410 (desvio do molde, dito): harness_saida_v410 e' COMPARTILHADA com harness_fechar_sandbox_v410.py (fechar_sandbox, memoria_copia, fechar_sandbox_resultado): este harness NAO apaga a pasta inteira, so' o que ELE cria
os.makedirs(OUT, exist_ok=True)
for _sub in ("nos_emulado", "conferidor_emulado", "pos_rito_emulada", "textos", "ensaio_superficies", "ensaio_superficies_folga", "ensaio_superficies_limite", "b3_sintetico"):
    shutil.rmtree(os.path.join(OUT, _sub), ignore_errors=True)
os.makedirs(NOSE)
for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"),
                 ("dry_v410_pt.txt", "um_absoluto_pt.txt"), ("dry_v410_en.txt", "um_absoluto_en.txt"), ("dry_v410_pt.toc", "um_absoluto_pt.toc"), ("dry_v410_en.toc", "um_absoluto_en.toc"), ("dry_v410_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v410_en.pdf", "um_absoluto_en.pdf")):
    if os.path.exists(os.path.join(DRY, src)):
        shutil.copyfile(os.path.join(DRY, src), os.path.join(NOSE, dst))
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSE, "tgl_kernel"))
# v410 (desvio do molde, dito): o JSON do rito real traz ga_window_status no topo e a v410 o confere; o ensaio so guarda core e verdict: a emulacao o le da constante do proprio candidato, nunca de ESPERADOS
import ast as _ast
_cj = rdj(os.path.join(NOSE, "um_absoluto.json")); _gw = re.search(r"^GA_WINDOW_STATUS = \((.*?)\)\r?$", open(os.path.join(NOSE, "um.py"), "rb").read().decode("utf-8"), re.S | re.M); assert _gw, "a constante GA_WINDOW_STATUS nao esta no candidato"
_cj["ga_window_status"] = _ast.literal_eval("(" + _gw.group(1) + ")")
open(os.path.join(NOSE, "um_absoluto.json"), "w", encoding="utf-8").write(json.dumps(_cj, ensure_ascii=False, default=str))
# o selo do ensaio a seco nao traz o que o main poe DEPOIS do literal (sha256 do um.py, fail_closed_selftest, rite_checkpoints, not_sealed_this_run): como em teste_conferidor_positivo_v410.py, o selo emulado ganha essas chaves do selo da v409 e o sha256 do um.py candidato
_selo0 = rdj(os.path.join(PKG, "base_v409", "um_absoluto_selo.json")); _selo = dict(_selo0); _selo.update(rdj(os.path.join(DRY, "selo_ensaio.json")))
_selo["sha256"] = dict(_selo0.get("sha256") or {}); _selo["sha256"]["um.py"] = fsha(os.path.join(NOSE, "um.py"))
open(os.path.join(NOSE, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(_selo, ensure_ascii=False, default=str))
_ens = rdj(os.path.join(PKG, "ensaio_a_seco_v410.json"))   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
# o SIDECAR: a funcao do PROPRIO candidato (a copia de bytes do Nos emulado; __file__ = nos_emulado\um.py) sobre o core e o selo FINAIS do Nos emulado; a linha que ela imprime e' a linha REAL do sidecar
_spec_sc = importlib.util.spec_from_file_location("um_sidecar_emulacao", os.path.join(NOSE, "um.py")); _umm = importlib.util.module_from_spec(_spec_sc)
_so = sys.stdout; sys.stdout = io.StringIO()
try:
    _spec_sc.loader.exec_module(_umm); _umm.OUT = NOSE
    sys.stdout = _buf_sc = io.StringIO()
    _umm.selo_acom_sidecar_v399()
    _linha_sidecar = _buf_sc.getvalue().strip()
finally:
    sys.stdout = _so; sys.stdout.reconfigure(encoding="utf-8")
del _umm, _spec_sc
N_ = ESP["escada"][1]
STDOUT_EMULADO = "\n".join(["[v399] EMULADO PELO HARNESS (nao e' o stdout de um rito; as linhas do fluxo principal sao as REAIS do ensaio a seco; as do kernel e do selo e o RITO_RC sao emulados)"] + list(_ens["mainflow"]["stdout"])
                           + ["teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", _linha_sidecar, "RITO_RC=0", ""])
open(os.path.join(NOSE, "rodada_v410_stdout.txt"), "w", encoding="utf-8", newline="\n").write(STDOUT_EMULADO)
etapa("nos_emulado", ok=True, pasta=NOSE, arquivos=sorted(os.listdir(NOSE)), um16=fsha(os.path.join(NOSE, "um.py"))[:16])

# ------------------------------------------------------------------ 2. o conferidor REAL (copia) contra o Nos emulado
# v410 (desvio do molde, dito): o conferidor importa o delta, o runtime, o acom_conferencias e os insumos pelo caminho da propria pasta, e o delta acha as falas do operador em ..\..\cunhagens_13out: por isso roda numa COPIA em ARVORE
# (conferidor_emulado\work\cadeia_de_selo\v410, com work\cunhagens_13out ao lado) e SEM -I (importa o um.py do Nos emulado, que precisa do numpy do usuario). Nada fora de harness_saida_v410 e' escrito.
DLX = importar("delta_v410_x", os.path.join(PKG, "delta_v410.py"))
# v410 (desvio do molde, dito): o conferidor roda NO LUGAR, como no passo 1 do chain (cwd = o pacote real): o delta_v410 pina por ASSERT os caminhos absolutos da integracao R3 e do estudo do fecho (MANIFEST_INTEGRACAO_ARQ), logo nao vive numa copia em arvore. SEM -I (importa o um.py do Nos emulado, que precisa do numpy do usuario);
# V410_NOS aponta para o Nos emulado; o sufixo _HARNESS faz o conferidor escrever conferencia_rito_v410_HARNESS.json no pacote: o harness a copia para pos_rito_emulada\conferidor\conferencia_rito_v410.json (que a leitura le) e a REMOVE do pacote (ou restaura os bytes que ja' estavam la'). Nada mais e' escrito fora de harness_saida_v410.
CF = PKG
env = dict(os.environ); env["V410_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"
_conf_h = os.path.join(PKG, "conferencia_rito_v410_HARNESS.json"); _conf_h_antes = open(_conf_h, "rb").read() if os.path.exists(_conf_h) else None
pr = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v410.py", "_HARNESS"], cwd=PKG, env=env, capture_output=True, text=True, encoding="utf-8")
open(os.path.join(OUT, "conferir_rito_v410_stdout.txt"), "w", encoding="utf-8").write(pr.stdout + pr.stderr)
conf_ok = (pr.returncode == 0 and pr.stdout.strip().splitlines()[-1:] == ["TUDO BATE"])
POS_EMU = os.path.join(OUT, "pos_rito_emulada"); os.makedirs(os.path.join(POS_EMU, "conferidor"))
_conf_sha16 = None
if os.path.exists(_conf_h):
    shutil.copyfile(_conf_h, os.path.join(POS_EMU, "conferidor", "conferencia_rito_v410.json")); _conf_sha16 = fsha(_conf_h)[:16]
    if _conf_h_antes is None:
        os.remove(_conf_h)
    else:
        open(_conf_h, "wb").write(_conf_h_antes)
etapa("conferidor", ok=conf_ok, rc=pr.returncode, ultima_linha=(pr.stdout.strip().splitlines() or [""])[-1][:200], conferencia_sha16=_conf_sha16)
print("  conferidor contra o Nos emulado: %s" % ("TUDO BATE" if conf_ok else "NAO BATEU (rc %s)" % pr.returncode))
if not conf_ok:
    falha("o conferidor real nao deu TUDO BATE contra o Nos emulado: a leitura nao tem a conferencia que le (ver harness_saida_v410\\conferir_rito_v410_stdout.txt)")

# ------------------------------------------------------------------ 3. a leitura REAL contra o Nos emulado (+ controles negativos)
L = importar("leitura_v410", os.path.join(HERE, "leitura_v410.py"))
L.NOS = NOSE; L.HERE = POS_EMU; L.PK = PKG
AP = {"um_py_novo": {"sha16": ESP["candidato_sha16"]}, "backups": {"um.py": {"sha16": ESP["origem_sha16"], "backup": "EMULADO_PELO_HARNESS"}}, "ts": time.strftime("%Y%m%d_%H%M%S")}
L._aplicado = lambda: (AP, "EMULADO_PELO_HARNESS")
sys.modules["leitura_v410"] = L
Vd, P = L.ler()
etapa("leitura", problemas=P, iald2_selado=(Vd.get("fecho") or {}).get("sealed"), h0dn_selado=(Vd.get("h0dn") or {}).get("sealed"), n_modulos_novos=Vd.get("n_pedras"), teor=Vd.get("teor"), escada_antes=Vd.get("escada_antes"), kh=Vd.get("kh"), registros_novos=Vd.get("registros_novos"), n_cunhagens=len(Vd.get("verbatins") or {}),
      veracidade_n_checks=(Vd.get("veracidade") or {}).get("n_checks"), patch_ids=Vd.get("patch_ids"))
print("  leitura: %d problema(s); %d pedra(s); escada %s -> %s; registros novos %s" % (len(P), Vd.get("n_pedras") or 0, Vd.get("escada_antes"), Vd.get("teor"), Vd.get("registros_novos")))
for p_ in P:
    falha("leitura: " + p_)
core_path = os.path.join(NOSE, "um_absoluto.json"); selo_path = os.path.join(NOSE, "um_absoluto_selo.json"); std_path = os.path.join(NOSE, "rodada_v410_stdout.txt")
core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()
conf_path = os.path.join(POS_EMU, "conferidor", "conferencia_rito_v410.json"); conf_raw = open(conf_path, "rb").read() if os.path.exists(conf_path) else b""


sc_path = os.path.join(NOSE, "um_absoluto_selo_acom.json"); sc_raw = open(sc_path, "rb").read() if os.path.exists(sc_path) else b""


def variante(nome, f_core=None, f_selo=None, f_std=None, f_conf=None, f_sc=None, sc_fora=False, espera=""):
    """aplica a variante nos arquivos do Nos emulado (e da conferencia do rito e do sidecar), roda a leitura, RESTAURA os bytes e confere que reprovou (com o trecho esperado na mensagem)."""
    try:
        if f_core:
            c = json.loads(core_raw.decode("utf-8")); f_core(c["core"]); open(core_path, "wb").write(json.dumps(c, ensure_ascii=False).encode("utf-8"))
        if f_selo:
            s = json.loads(selo_raw.decode("utf-8")); f_selo(s); open(selo_path, "wb").write(json.dumps(s, ensure_ascii=False).encode("utf-8"))
        if f_std:
            open(std_path, "wb").write(f_std(std_raw.decode("utf-8")).encode("utf-8"))
        if f_conf:
            cj = json.loads(conf_raw.decode("utf-8")); f_conf(cj); open(conf_path, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
        if f_sc:
            sj = json.loads(sc_raw.decode("utf-8")); f_sc(sj); open(sc_path, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
        if sc_fora:
            os.remove(sc_path)
        _, PV = L.ler()
    finally:
        open(core_path, "wb").write(core_raw); open(selo_path, "wb").write(selo_raw); open(std_path, "wb").write(std_raw)
        if os.path.exists(conf_path):
            open(conf_path, "wb").write(conf_raw)
        open(sc_path, "wb").write(sc_raw)
    ok = any(espera in x for x in PV)
    return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": ok, "problemas": [x[:140] for x in PV][:3]}


def _core_k(c, k):
    return c[k]


def _sem_selo(c):
    c.pop("selo_pela_propria_tecnologia_v399", None)


def _sem_declaracao(c):
    c.pop("declaracao_do_operador_v399", None)


def _nao_sela_cunh(c):
    c["cunhagens_v399"]["all_verified"] = False


def _nao_sela_kh(c):
    c["kh_n1_cobertura_v399"]["all_verified"] = False


def _selo_nao_sela(c):
    c["selo_pela_propria_tecnologia_v399"]["all_verified"] = False


def _selo_cheque_falha(c):
    c["selo_pela_propria_tecnologia_v399"]["checks"][2][1] = False


def _selo_perfil(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["perfil"] = "ACOM-INT-C128-Q8"


def _selo_bloco(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["bloco_embutido_sha256"] = "0" * 64


def _selo_sha(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["sha256"] = "0" * 64


def _selo_psi(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["psi"]["sha256"] = "0" * 64


def _selo_theta_bytes(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["theta"]["bytes"] += 1


def _selo_controles_12(c):
    c["selo_pela_propria_tecnologia_v399"]["controles_negativos"]["n_controles"] = 12


def _selo_controle_aceito(c):
    r = c["selo_pela_propria_tecnologia_v399"]["controles_negativos"]; r["controles"][0]["ok"] = False; r["todos_recusados"] = False


def _selo_reconstrucao(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["prova_de_reconstrucao"]["bytes_divergentes"] = 1


def _selo_psi_redundante(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["auditoria_de_separacao"]["psi_redundante"] = True


def _selo_gate(c):
    c["selo_pela_propria_tecnologia_v399"]["does_not_gate_core"] = False


def _selo_confidencialidade(c):
    c["selo_pela_propria_tecnologia_v399"]["statuses"]["confidencialidade"] = "garantida pelo metodo"


def _selo_direcao_invertida(c):
    c["selo_pela_propria_tecnologia_v399"]["direcao_do_testemunho"] = "o operador testifica DA IALD; a IALD testifica do operador"


def _selo_beta(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["beta"] = 0.0121


def _decl_nao_sela(c):
    c["declaracao_do_operador_v399"]["all_verified"] = False


def _decl_fala(c):
    c["declaracao_do_operador_v399"]["declaration"]["statement_verbatim"] += " "


def _decl_sha(c):
    c["declaracao_do_operador_v399"]["declaration"]["verbatim_sha256"] = "0" * 64


def _decl_direcao(c):
    c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"


def _decl_pai(c):
    c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"]["o_Pai_de_Jo_8_18"] = "le-se na IALD"


def _decl_ancora_fora(c):
    c["declaracao_do_operador_v399"]["declaration"]["kernel_anchors_REAL"][0]["axiomas_no_trio"] = False


def _decl_estatuto(c):
    c["declaracao_do_operador_v399"]["declaration"]["status_of_statement"] = "[REAL] o kernel a prova"


def _decl_pedra_vazia(c):
    c["declaracao_do_operador_v399"]["declaration"]["pedra_instalada"] = []


def _decl_gate(c):
    c["declaracao_do_operador_v399"]["does_not_gate_core"] = False


def _fal_nao_sela(c):
    c["falsidade_da_inercia_v401"]["all_verified"] = False


def _fal_cheque(c):
    c["falsidade_da_inercia_v401"]["mechanics"]["checks"][2]["ok"] = False


def _fal_valor(c):
    c["falsidade_da_inercia_v401"]["values"]["min_cost_t_beta_g"] = 0.0007


def _fal_beta(c):
    c["falsidade_da_inercia_v401"]["values"]["beta"] = 0.0121


def _fal_posto_inercial(c):
    c["falsidade_da_inercia_v401"]["values"]["post_inertial_scales"] = [1.0]


def _fal_fixo(c):
    c["falsidade_da_inercia_v401"]["values"]["fixed_by_the_whole_flow"] = [0.0, 1.0]


def _fal_costless(c):
    c["falsidade_da_inercia_v401"]["costless"]["ok"] = False


def _fal_estrela(c):
    c["falsidade_da_inercia_v401"]["key_theorem"]["in_kernel"] = False


def _fal_gate(c):
    c["falsidade_da_inercia_v401"]["does_not_gate_core"] = False


def _fal_runtime(c):
    c["falsidade_da_inercia_v401"]["runtime_executed"] = False


def _fal_verdict(c):
    c["falsidade_da_inercia_v401"]["verdict"] = "OUTRO_VEREDITO"


def _fal_chain_status(c):
    c["falsidade_da_inercia_v401"]["chain_status"] = "ONTO do operador"


def _fal_hipotese_usada(c):
    c["falsidade_da_inercia_v401"]["named_hypothesis"]["used_by_a_theorem"] = True


def _fal_hipotese_sem_nome(c):
    c["falsidade_da_inercia_v401"]["named_hypothesis"]["name"] = "H_x"


def _fal_peso_zero(c):
    c["falsidade_da_inercia_v401"]["values"]["min_weight_on_the_grid_positive"] = 0.0


def _cunh_cadeia_onto(c):
    c["cunhagens_v401"]["extras"]["cadeia_derivada"]["estatuto"] = "[ONTO]"


def _cunh_hipotese_usada(c):
    c["cunhagens_v401"]["extras"]["hipotese_nomeada"]["usada_por_teorema"] = True


def _gerencia_na_cunhagem(c):
    ex = c["cunhagens_v401"]["extras"]; ex["autor_de_cada_inscricao"][sorted(ex["autor_de_cada_inscricao"])[0]] = "gerencia"


def _inscricao_adulterada(c):
    list(c["cunhagens_v401"]["verbatim"].values())[0]["embedded_ok"] = False


def _inscricao_sha(c):
    list(c["cunhagens_v401"]["verbatim"].values())[1]["sha256"] = "0" * 64


def _rat_menos(c):
    c["cunhagens_v401"]["extras"]["ratificacoes"].pop()


def _rat_fala(c):
    c["cunhagens_v401"]["extras"]["ratificacao_fala"]["sha16"] = "0" * 16


def _errata_sem_superada(c):
    c["cunhagens_v401"]["erratas"][0]["agora"] = "mantida"


def _errata_sem_assinatura(c):
    c["cunhagens_v401"]["erratas"][0]["assinatura"] = "operador"


def _cunh399_gerencia(c):
    ex = c["cunhagens_v399"]["extras"]; ex["autor_de_cada_inscricao"][sorted(ex["autor_de_cada_inscricao"])[0]] = "gerencia"


def _cunh399_direcao(c):
    c["cunhagens_v399"]["extras"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"


def _cunh399_declaracao_sha(c):
    c["cunhagens_v399"]["extras"]["declaracao"]["sha256"] = "0" * 64


def _cunh399_inscricao(c):
    list(c["cunhagens_v399"]["verbatim"].values())[0]["embedded_ok"] = False


def _numero_adulterado(c):
    c["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 4.45


def _z_disc_acima_de_5(c):
    c["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 5.2


def _checagem_falha(c):
    c["teste_de_veracidade_fase9_v397"]["checks"][3]["ok"] = False


def _fonte_adulterada(c):
    c["teste_de_veracidade_fase9_v397"]["fontes"][0]["sha256"] = "0" * 64


def _gate_movido(c):
    c["teste_de_veracidade_fase9_v397"]["does_not_gate_core"] = False


def _veracidade_cai(c):
    c["teste_de_veracidade_fase9_v397"]["all_verified"] = False


def _sonico409_cai(c):
    c["sonico_v398"]["all_verified"] = False


def _afinacao409_cai(c):
    c["afinacao_das_cordas_v398"]["all_verified"] = False


def _cunh409_cai(c):
    c["cunhagens_v398"]["all_verified"] = False


def _kh409_cai(c):
    c["kh_n1_cobertura_v398"]["all_verified"] = False


def _cunh397_cai(c):
    c["cunhagens_v397"]["all_verified"] = False


def _testemunha_cai(c):
    c["testemunha_estatica_v396"]["all_verified"] = False


def _fock_da_testemunha_volta_a_false(c):
    c["testemunha_estatica_v396"]["fock_face"]["inhabitant_exhibited"] = False


def _fock_dentro_da_pedra(c):
    c["testemunha_estatica_v396"]["fock_face"]["declared_outside_the_stone"] = False


def _psibit_cai(c):
    c["psibit_v395"]["all_verified"] = False


def _face_do_psibit_volta_a_false(c):
    c["psibit_v395"]["conditional_psion_face"]["inhabitant_exhibited"] = False


def _v394_cai(c):
    c["criterio_binario_de_parada_v394"]["all_verified"] = False


def _selo_v409(s):
    s["um_version"] = "v409"


def _selo_resumo_diferente(s):
    s["selo_pela_propria_tecnologia_v399"]["verdict"] = "OUTRO_VEREDITO"


def _selo_resumo_sha(s):
    s["selo_pela_propria_tecnologia_v399"]["sha256_do_um_py"] = "0" * 64


def _selo_formal_nao_selado(s):
    s["not_sealed_this_run"]["formais"] = ["selo_pela_propria_tecnologia_v399"]


def _conf_quadro_pt(cj):
    cj["quadro"]["pt"]["ok"] = False


def _conf_quadro_md(cj):
    cj["quadro"]["md"]["ok"] = False


def _conf_c5(cj):
    cj["acom_itens"]["C5"]["ok"] = False


def _conf_round_trip(cj):
    cj["acom_itens"]["round_trip_do_um_py_instalado_independente"]["ok"] = False


def _selo_sem_resumo_falsidade(s):
    s.pop("falsidade_da_inercia_v401", None)


def _selo_registros_v410_diferente(s):
    s["registros_v401"]["cunhagens_v401"]["verdict"] = "OUTRO_VEREDITO"


def _conf_c15(cj):
    cj["acom_itens"]["C15"]["ok"] = False


def _conf_c16(cj):
    cj["acom_itens"]["C16"]["ok"] = False


def _conf_veredito_falsidade(cj):
    cj["veredito_falsidade"] = "OUTRO_VEREDITO"


def _conf_sidecar(cj):
    cj["sidecar"]["existe"] = False


def _sc_sha_objeto(sj):
    sj["objetos"][1]["sha256"] = "0" * 64


def _sc_recusas(sj):
    sj["recusas"] = [{"nome": "um.py", "recusa": "RECUSOU:X"}]


def _sc_veredito(sj):
    sj["veredito"] = "TGL_SELO_ACOM_SIDECAR_V410__REFUSED__SOME_OBJECTS_REFUSED"


def _sc_objeto_faltando(sj):
    sj["objetos"].pop()


def _sc_confidencialidade(sj):
    sj["honestidade"]["confidencialidade"] = "garantida pelo metodo"


def _sc_um_py_outro(sj):
    sj["objetos"][0]["acom"]["psi"]["sha256"] = "0" * 64


def _sc_esquema(sj):
    sj["esquema"] = "outro_esquema"


def _sc_direcao_invertida(sj):
    sj["gerado_por"] = "a IALD testifica do operador"


NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v409)", f_selo=_selo_v409, espera="o selo nao e v410"),
           variante("registro falsidade_da_inercia_v401 ausente do core", f_core=lambda c: c.pop("falsidade_da_inercia_v401", None), espera="registro obrigatorio ausente do core: falsidade_da_inercia_v401"),
           variante("registro selo_pela_propria_tecnologia_v399 (recriado) ausente do core", f_core=_sem_selo, espera="registro obrigatorio ausente do core: selo_pela_propria_tecnologia_v399"),
           variante("registro declaracao_do_operador_v399 (recriado) ausente do core", f_core=_sem_declaracao, espera="registro obrigatorio ausente do core: declaracao_do_operador_v399"),
           variante("cunhagens_v401 nao selou", f_core=lambda c: c["cunhagens_v401"].update(all_verified=False), espera="cunhagens_v401 nao selou"),
           variante("kh_n1_cobertura_v401 nao selou", f_core=lambda c: c["kh_n1_cobertura_v401"].update(all_verified=False), espera="kh_n1_cobertura_v401 nao selou"),
           variante("cunhagens_v399 (recriada) nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v399 nao selou"),
           variante("kh_n1_cobertura_v399 (recriado) nao selou", f_core=_nao_sela_kh, espera="kh_n1_cobertura_v399 nao selou"),
           variante("falsidade: o registro nao selou", f_core=_fal_nao_sela, espera="falsidade_da_inercia_v401 nao selou"),
           variante("falsidade: uma checagem do calculo falhou", f_core=_fal_cheque, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o custo minimo adulterado", f_core=_fal_valor, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: beta != alfa x raiz de e do core", f_core=_fal_beta, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: uma escala nao trivial que fixa o posto", f_core=_fal_posto_inercial, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: mais de um estado fixo pelo fluxo inteiro", f_core=_fal_fixo, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o 0_abs de costless fora do kernel embutido", f_core=_fal_costless, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a estrela fora do kernel do rito (no registro)", f_core=_fal_estrela, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o registro move o gate", f_core=_fal_gate, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o calculo do runtime nao rodou", f_core=_fal_runtime, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a cadeia dita ONTO do operador (chain_status)", f_core=_fal_chain_status, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: H_tau usada por um teorema", f_core=_fal_hipotese_usada, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a hipotese nomeada deixa de ser H_tau", f_core=_fal_hipotese_sem_nome, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o peso minimo do posto na grade zero (o zero como estado da orbita)", f_core=_fal_peso_zero, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("cunhagens_v401 (recriada): a cadeia derivada dita [ONTO]", f_core=_cunh_cadeia_onto, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v401 (recriada): H_tau dita usada por teorema", f_core=_cunh_hipotese_usada, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("falsidade: veredito diferente do ensaio a seco", f_core=_fal_verdict, espera="falsidade_da_inercia_v401: o veredito do rito difere do ensaio a seco"),
           variante("selo ACOM (recriado): o registro nao selou", f_core=_selo_nao_sela, espera="selo_pela_propria_tecnologia_v399 nao selou"),
           variante("selo ACOM (recriado): uma checagem falhou", f_core=_selo_cheque_falha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: perfil adulterado", f_core=_selo_perfil, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash do bloco embutido adulterado", f_core=_selo_bloco, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o SHA-256 ao lado difere do um.py do disco", f_core=_selo_sha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash de Psi adulterado", f_core=_selo_psi, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: bytes de Theta adulterados", f_core=_selo_theta_bytes, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: controles negativos 12 em vez do pinado", f_core=_selo_controles_12, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: um controle negativo ACEITOU", f_core=_selo_controle_aceito, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: reconstrucao com byte divergente", f_core=_selo_reconstrucao, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: Psi redundante (separacao vazia)", f_core=_selo_psi_redundante, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o registro move o gate", f_core=_selo_gate, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: confidencialidade alegada", f_core=_selo_confidencialidade, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: direcao do testemunho invertida", f_core=_selo_direcao_invertida, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: beta do registro != alfa x raiz de e do core", f_core=_selo_beta, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("declaracao (recriada): o registro nao selou", f_core=_decl_nao_sela, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a fala embutida difere do arquivo do operador", f_core=_decl_fala, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: sha256 da fala adulterado", f_core=_decl_sha, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a IALD como quem testifica do operador", f_core=_decl_direcao, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o Pai de Jo 8,18 lido na IALD", f_core=_decl_pai, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: uma ancora do kernel fora do trio", f_core=_decl_ancora_fora, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o estatuto trocado por REAL", f_core=_decl_estatuto, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a pedra Testemunho nao conferida", f_core=_decl_pedra_vazia, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o registro move o gate", f_core=_decl_gate, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("cunhagens_v401 (recriada): uma inscricao rotulada como da gerencia", f_core=_gerencia_na_cunhagem, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v401 (recriada): uma inscricao deixou de estar embutida", f_core=_inscricao_adulterada, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v401 (recriada): sha256 de uma inscricao adulterado", f_core=_inscricao_sha, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v401 (recriada): falta uma das oito ratificacoes", f_core=_rat_menos, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v401 (recriada): a fala da ratificacao adulterada", f_core=_rat_fala, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v401 (recriada): a errata do adendo sem SUPERADA", f_core=_errata_sem_superada, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v401 (recriada): a errata sem a assinatura da gerencia", f_core=_errata_sem_assinatura, espera="cunhagens_v401 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): uma inscricao rotulada como da gerencia", f_core=_cunh399_gerencia, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): a direcao do testemunho invertida", f_core=_cunh399_direcao, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): sha256 da declaracao adulterado", f_core=_cunh399_declaracao_sha, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): uma inscricao deixou de estar embutida", f_core=_cunh399_inscricao, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("sidecar: ausente", sc_fora=True, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: sha256 de um objeto adulterado", f_sc=_sc_sha_objeto, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: recusas registradas", f_sc=_sc_recusas, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: veredito de recusa", f_sc=_sc_veredito, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: um objeto faltando", f_sc=_sc_objeto_faltando, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: confidencialidade alegada na honestidade", f_sc=_sc_confidencialidade, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: o hash de Psi do um.py != ESPERADOS", f_sc=_sc_um_py_outro, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: esquema trocado", f_sc=_sc_esquema, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: a direcao do testemunho invertida", f_sc=_sc_direcao_invertida, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("selo primario: o resumo do selo ACOM difere do core", f_selo=_selo_resumo_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: o sha256 do um.py no resumo difere do disco", f_selo=_selo_resumo_sha, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: sem o resumo da falsidade", f_selo=_selo_sem_resumo_falsidade, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: registros_v401 do selo difere do core", f_selo=_selo_registros_v410_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: modulo formal nao selado", f_selo=_selo_formal_nao_selado, espera="o selo traz modulo formal nao selado"),
           variante("o quadro do topo: numero lido adulterado (z_disc 4,45)", f_core=_numero_adulterado, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: z_disc calibrado acima de 5", f_core=_z_disc_acima_de_5, espera="abaixo de 5"),
           variante("o quadro do topo: uma checagem do registro de veracidade falhou", f_core=_checagem_falha, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: fonte do registro de veracidade com sha256 adulterado", f_core=_fonte_adulterada, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade move o gate", f_core=_gate_movido, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade deixou de selar", f_core=_veracidade_cai, espera="teste_de_veracidade_fase9_v397"),
           variante("o quadro do topo: a conferencia diz que o quadro PT deixou de estar no topo", f_conf=_conf_quadro_pt, espera="o quadro do topo (O Teste da Unica Palavra, pt)"),
           variante("o quadro do topo: a conferencia diz que o quadro do .md deixou de estar no topo", f_conf=_conf_quadro_md, espera="o quadro do topo (O Teste da Unica Palavra, md)"),
           variante("a conferencia diz que o item C5 do selo ACOM nao conferiu", f_conf=_conf_c5, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o item C15 (guardas estaticas da Bancada) nao conferiu", f_conf=_conf_c15, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o item C16 (ler_nos sobre o Nos inteiro) nao conferiu", f_conf=_conf_c16, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o round trip do um.py instalado nao conferiu", f_conf=_conf_round_trip, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia traz outro veredito da falsidade", f_conf=_conf_veredito_falsidade, espera="veredito da falsidade"),
           variante("a conferencia diz que o sidecar nao existe", f_conf=_conf_sidecar, espera="o sidecar um_absoluto_selo_acom.json nao existe ou nao esta selado"),
           variante("sonico_v398 deixou de selar", f_core=_sonico409_cai, espera="sonico_v398"),
           variante("afinacao_das_cordas_v398 deixou de selar", f_core=_afinacao409_cai, espera="afinacao_das_cordas_v398"),
           variante("cunhagens_v398 deixou de selar", f_core=_cunh409_cai, espera="cunhagens_v398"),
           variante("kh_n1_cobertura_v398 deixou de selar", f_core=_kh409_cai, espera="kh_n1_cobertura_v398"),
           variante("cunhagens_v397 deixou de selar", f_core=_cunh397_cai, espera="cunhagens_v397"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha de volta a literal False (habitante nao exibido)", f_core=_fock_da_testemunha_volta_a_false, espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 de volta a literal False (habitante nao exibido)", f_core=_face_do_psibit_volta_a_false, espera="psibit_v395: a face do psion nao le o habitante"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v410 (a falsidade nao rodou) no stdout", f_std=lambda t: t + "   [v401] AVISO: a falsidade da inercia nao rodou: ValueError('x')\n", espera="AVISO da v410"),
           variante("AVISO da v410 (o selo ACOM) no stdout", f_std=lambda t: t + "   [v399] AVISO: o selo ACOM nao rodou: ValueError('x')\n", espera="AVISO da v410"),
           variante("AVISO do sidecar no stdout", f_std=lambda t: t.replace("RITO_RC=0", "[selo_acom] AVISO: nao consegui escrever o sidecar: OSError('x')\nRITO_RC=0"), espera="AVISO da v410"),
           variante("AVISO de bloco anterior (v398) no stdout", f_std=lambda t: t + "   [v398] AVISO: o sonico nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior"),
           variante("linha [v399] ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o selo pela propria tecnologia e a declaracao do operador" not in l) + "\n", espera="linha [v399] do stdout"),
           variante("linha [v401] ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "a falsidade (simulacro) da inercia (lida depois da declaracao do operador)" not in l) + "\n", espera="linha [v401] do stdout"),
           variante("linha `>>> veredito <<<` do selo ACOM ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["selo_acom"]["verdict"] not in l or "selo=" in l) + "\n", espera="o bloco selo_pela_propria_tecnologia_v399 do stdout"),
           variante("linha `>>> veredito <<<` da declaracao ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["declaracao"]["verdict"] not in l or "declaracao=" in l) + "\n", espera="o bloco declaracao_do_operador_v399 do stdout"),
           variante("linha `>>> veredito <<<` da falsidade ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["veredito_da_falsidade_v409"] not in l or "falsidade=" in l) + "\n", espera="o bloco falsidade_da_inercia_v401 do stdout"),
           variante("linha [v398] (sonico, afinacao e cunhagens) ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o sonico e a afinacao das cordas" not in l) + "\n", espera="linha [v398] do stdout"),
           variante("linha [v397] do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\n", espera="linha [v397] do Teste da Unica Palavra"),
           variante("linha do sidecar ausente do stdout (a ultima nao e' a do sidecar)", f_std=lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("[selo_acom]")) + "\n", espera="as duas ultimas linhas do stdout"),
           variante("a linha do sidecar antes da do colapso tipado (ordem trocada)", f_std=lambda t: "\n".join([l for l in t.splitlines() if not l.startswith("[selo_acom]") and not l.startswith("[selo] colapso tipado") and not l.startswith("RITO_RC=")] + [l for l in t.splitlines() if l.startswith("[selo_acom]")] + [l for l in t.splitlines() if l.startswith("[selo] colapso tipado")] + ["RITO_RC=0"]) + "\n", espera="as duas ultimas linhas do stdout")]

    def _pedra_no_disco(nome, f_muda, idx=0):
        """controle sobre o ARQUIVO de uma das TRES pedras no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        pth = os.path.join(NOSE, "tgl_kernel", *list(ESP["bundle_sha256"])[idx].split("/")); raw_ = open(pth, "rb").read()
        try:
            f_muda(pth, raw_)
            _, PV = L.ler()
        finally:
            if os.path.exists(pth + ".fora"):
                os.remove(pth + ".fora")
            open(pth, "wb").write(raw_)
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any("modulos novos do kernel" in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # v410: controles para CADA um dos registros NOVOS (os dois com pedra, a errata de F2b, cunhagens_v404 e kh_n1_cobertura_v404), para os registros da v409 e da v402 RECRIADOS, para os resumos do selo, a conferencia e as linhas [v404], [v403] e [v402] do stdout
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    EF_ = {}   # v410: nao ha' registro por pedra
    EF3_ = {k_: {"verdict": L._ev(ESP, n_)} for k_, n_ in (("caminho", "caminho_v403"), ("vida", "vida_v403"), ("verdade_adendo", "verdade_adendo_v403"), ("gate", "bandeiras_do_gate_v403"))}   # os vereditos esperados dos registros da v403 (recriados)
    EF4_ = {k_: {"verdict": L._ev(ESP, n_)} for k_, n_ in (("projecao", "projecao_transversal_v404"), ("jo8v32", "jo8v32_v404"), ("f2b", "f2b_errata_v404"))}   # os da v404 (recriados)
    EV3_ = ESP["vereditos_v409"]
    FE_ = DLX.FECHO_REGISTRO; F9_ = DLX.D9.FECHO_REGISTRO; FT_ = DLX.D8.FECHO_REGISTRO; FP_ = "psion_canto_v407"; FH_ = "fechamento_v406"; FJ_ = rdj(os.path.join(PKG, "kernel", "FLAGS_v410.json")); ANC_ = list(DLX.ANCORAS); FLAGS_ = [f_[0] for f_ in FJ_["flags"]]
    RESUMO_MSG = "o selo primario (um_absoluto_selo.json) nao traz os resumos"
    VER_HERD = ": o veredito do rito difere do esperado"   # a mensagem da leitura para os registros HERDADOS (REG_V409D, REG_V406D): o esperado e' o da v409 selada, ou o do ensaio a seco se na troca dita

    def _kf(c):
        return c["kernel_formalization"]

    def _fora_do_trio(c, termo):
        _kf(c)["axiom_report"][termo] = ["propext", "sorryAx"]

    def _std_selados(t_, trecho):
        return "\n".join(re.sub(r"\(selados \d+\)", "(selados 0)", l) if trecho in l else l for l in t_.splitlines()) + "\n"

    for a_n_ in list(dict.fromkeys((DLX.ANCORA_PRINCIPAL, DLX.ANCORAS_DE_SECAO[0], ANC_[-1]))):    # a ancora principal (p_igual_np_no_modo_selecao), a primeira de secao e a ultima: fora do trio, a bandeira falsa e o sha256 da fonte no hash formal adulterado
        curto_ = a_n_.split(".")[-1]; fl_a_ = FJ_["ancoras"][a_n_]["flag"]; rel_a_ = DLX.ANCORAS[a_n_]["rel"]
        NEG.extend([variante("ancora %s fora do trio" % curto_, f_core=lambda c, t=a_n_: _fora_do_trio(c, t), espera="a ancora "), variante("ancora %s: a bandeira falsa" % curto_, f_core=lambda c, f=fl_a_: _kf(c).__setitem__(f, False), espera="a ancora "),
                    variante("ancora %s: sha256 da fonte do modulo no hash formal adulterado" % curto_, f_core=lambda c, r=rel_a_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="a ancora ")])
    _EST9 = ESP["estrelas_v409"]; _a9 = list(_EST9)[0]; _b9 = list(ESP["bundle_v409_sha256"])[0]   # o traducao_turing_v409 HERDADO: as 82 ancoras e os 2 modulos da v409
    _EST8 = ESP["estrelas_v408"]; _a8 = list(_EST8)[0]; _b8 = list(ESP["bundle_v408_sha256"])[0]   # o tetelestai_terminal_v408 HERDADO: as 48 ancoras e os 4 modulos da v408
    _EST7 = ESP["estrelas_v407"]; _a7 = list(_EST7)[0]; _b7 = list(ESP["bundle_v407_sha256"])[0]   # o psion_canto_v407 HERDADO: as 76 ancoras e os 9 modulos da v407
    _EST6 = ESP["estrelas_v406"]; _a6 = list(_EST6)[0]; _b6 = list(ESP["bundle_v406_sha256"])[0]; _ft6 = ESP["flags_true_v409"][len(ESP["flags_true_v409"]) // 2]   # o fechamento_v406 HERDADO: as oito ancoras e os 301 modulos da v406
    _N10, _N9, _N8, _N7, _N6 = len(ANC_), len(_EST9), len(_EST8), len(_EST7), len(_EST6)
    _CH_TRAD = DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_ORDEM_V410)   # a chave da ORDEM do operador da v410 (06/11), lida do arquivo (o nome _CH_TRAD e' herdado do molde)
    _CH_Z = DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_SOLUCAO)   # a chave da fala da D65 (o sha16 do arquivo INTEIRO; o texto embutido e' o trecho)

    def _bundle_anterior_no_disco(nome, rel_, msg_):
        """controle sobre o ARQUIVO de um modulo do bundle de uma versao ANTERIOR no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        def _f(f_muda):
            pth = os.path.join(NOSE, "tgl_kernel", *rel_.split("/")); raw_ = open(pth, "rb").read()
            try:
                f_muda(pth, raw_)
                _, PV = L.ler()
            finally:
                if os.path.exists(pth + ".fora"):
                    os.remove(pth + ".fora")
                open(pth, "wb").write(raw_)
            return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any(msg_ in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
        return _f
    # ---- 09/11 (fork A): o registro h0dn_bg1_v410 (D72, o SEGUNDO registro com funcao): constantes e ajudantes dos controles. A mutacao do ESPERADOS e do CANDIDATO e' feita NA MEMORIA (L.json trocado por um shim que muta o dict recem-carregado, e restaurado): nenhum arquivo do pacote e' tocado.
    H0_ = DLX.H0DN_REGISTRO; MH_ = H0_ + " nao selou inteiro"; MOBS_ = H0_ + ": observed_vector_read tem de ser False"
    _TOK_H0 = DLX.TOKENS_PROIBIDOS_H0DN[0]   # montado por concatenacao no delta: nunca literal neste arquivo (a guarda varre os textos, e este arquivo nao deve carregar o token)
    _CORE0_ = json.loads(core_raw.decode("utf-8"))["core"]; _HD0_ = _CORE0_.get(H0_) or {}
    _NPIN_ = len((_HD0_.get("values") or {}).get("pinos") or {}); _NCHK_ = len((_HD0_.get("mechanics") or {}).get("checks") or [])
    del _CORE0_, _HD0_
    # ---- 09/11 (parte 2): a escala (a_escala_v410, D86/D87) e o recibo documental HMS/13 (h0dn_fontes_hms13_v410, D80): constantes e ajudantes dos controles (as mensagens sao as da leitura_v410)
    AE_ = DLX.AESCALA_REGISTRO; MAE_ = AE_ + " nao selou inteiro"; HM_ = DLX.HMS13_REGISTRO; MHM_ = HM_ + " nao selou inteiro"; MOBSH_ = HM_ + ": observed_vector_read e le_em_rito tem de ser False"
    _NAE_ = len(DLX.ANCORAS_AESCALA); _NCHK_AE_ = DLX.N_CHECKS_AESCALA; _NCHK_HM_ = DLX.N_CHECKS_HMS13; _NEMB_ = len(DLX.HMS13_EMBUTIDOS)

    def _no_bloco(t_, cab_, velho_, novo_):
        """troca `velho_` por `novo_` SO' no bloco que comeca na linha `cab_` (o cabecalho, a linha de contagens e a linha `>>> veredito <<<`): as contagens de um bloco novo se repetem nos outros."""
        ls_ = t_.split("\n"); i_ = next(i for i, l_ in enumerate(ls_) if l_.startswith(cab_))
        for j_ in range(i_, min(i_ + 3, len(ls_))):
            ls_[j_] = ls_[j_].replace(velho_, novo_)
        return "\n".join(ls_)

    def _sem_bloco_n(t_, cab_):
        ls_ = t_.split("\n"); i_ = next(i for i, l_ in enumerate(ls_) if l_.startswith(cab_))
        return "\n".join(ls_[:i_] + ls_[i_ + 3:])   # o cabecalho, a linha de contagens e a linha `>>> veredito <<<`

    def _escala_forma_trocada(c):
        c[AE_].update(frase_canonica_pt="O Clay esta resolvido.")

    def _hms13_sem_obrigacao(c):
        r_ = c[HM_]; r_["estatuto"] = "[REAL] o recibo HMS/13."; r_["scope"] = "O recibo HMS/13 entra nesta versao."
        for k_ in ("limites", "diz", "nao_diz", "o_que_falta", "ressalvas"):
            r_[k_] = ["O recibo HMS/13."]


    def _sem_bloco_h0dn(t_):
        ls_ = t_.split("\n"); i_ = next(i for i, l_ in enumerate(ls_) if l_.startswith("H0DN x BG1 [v410"))
        return "\n".join(ls_[:i_] + ls_[i_ + 3:])   # o cabecalho, a linha `pinos ok = ...` e a linha `>>> veredito <<<`

    def _vet_ramo(c, n_):
        return next(v_ for v_ in c[H0_]["values"]["vetores_c6"] if v_["ramo"] == n_)

    class _JsonShim:
        def __init__(self, real, muta):
            self._real = real; self._muta = muta

        def __getattr__(self, k):
            return getattr(self._real, k)

        def load(self, fp, *a, **kw):
            d_ = self._real.load(fp, *a, **kw); self._muta(os.path.basename(str(getattr(fp, "name", ""))), d_); return d_

    def variante_json(nome, f_json, espera):
        """como variante(), mas a mutacao e' sobre o ESPERADOS_v410.json / CANDIDATO_v410.json que a leitura CARREGA (NA MEMORIA; nada e' escrito): L.json e' trocado por um shim e restaurado no finally."""
        real_ = L.json
        try:
            L.json = _JsonShim(real_, f_json)
            _, PV = L.ler()
        finally:
            L.json = real_
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any(espera in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
    _so_esp = lambda f: (lambda nm, d: f(d) if nm == "ESPERADOS_v410.json" else None)
    _so_cm = lambda f: (lambda nm, d: f(d) if nm == "CANDIDATO_v410.json" else None)
    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"; HERDP_ = FP_ + " (HERDADO, recriado) nao selou inteiro"; HERDT_ = FT_ + " (HERDADO, recriado) nao selou inteiro"; HERD9_ = F9_ + " (HERDADO, recriado) nao selou inteiro"
    NEG.extend([
        # ---- iald2_v410 (o registro NOVO com funcao)
        variante("%s ausente do core" % FE_, f_core=lambda c: c.pop(FE_, None), espera="registro obrigatorio ausente do core: " + FE_),
        variante("%s: o registro nao selou" % FE_, f_core=lambda c: c[FE_].update(all_verified=False), espera=FE_ + " nao selou"),
        variante("%s: uma checagem do calculo falhou" % FE_, f_core=lambda c: c[FE_]["mechanics"]["checks"][2].update(ok=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o numero de checagens != o do delta" % FE_, f_core=lambda c: c[FE_]["mechanics"]["checks"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: o numero de modulos ok adulterado" % FE_, f_core=lambda c: c[FE_]["values"].update(n_modulos_ok=DLX.N_BUNDLE - 1), espera=FE_ + " nao selou inteiro"),
        variante("%s: o numero de bandeiras True adulterado" % FE_, f_core=lambda c: c[FE_]["values"].update(n_flags_true=c[FE_]["values"]["n_flags_true"] - 1), espera=FE_ + " nao selou inteiro"),
        variante("%s: a escada do registro != a do ensaio" % FE_, f_core=lambda c: c[FE_]["values"].update(escada=[1, 1, 1]), espera=FE_ + " nao selou inteiro"),
        variante("%s: beta != alfa x raiz de e do core" % FE_, f_core=lambda c: c[FE_]["values"].update(beta=0.0121), espera=FE_ + " nao selou inteiro"),
        variante("%s: beta_ok falso no registro" % FE_, f_core=lambda c: c[FE_].update(beta_ok=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: veredito diferente do ensaio a seco" % FE_, f_core=lambda c: c[FE_].update(verdict="OUTRO_VEREDITO"), espera=FE_ + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: uma resposta do operador nao conferida no kernel" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].update({sorted(c[FE_]["values"]["respostas"])[0]: False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: a resposta do nome do algoritmo ausente" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].pop("o_nome_do_algoritmo_e_iald"), espera=FE_ + " nao selou inteiro"),
        variante("%s: o signo do Nome com o traco != o posto" % FE_, f_core=lambda c: c[FE_]["values"]["signo_do_nome"].update(traco=c[FE_]["values"]["signo_do_nome"]["traco"] + 1.0), espera=FE_ + " nao selou inteiro"),
        variante("%s: o signo do par com posto 2" % FE_, f_core=lambda c: c[FE_]["values"]["signo_do_par"].update(posto=2), espera=FE_ + " nao selou inteiro"),
        variante("%s: a instancia NAO com solucao" % FE_, f_core=lambda c: c[FE_]["values"]["instancia_nao"].update(solucoes=1), espera=FE_ + " nao selou inteiro"),
        variante("%s: a instancia SIM sem solucao" % FE_, f_core=lambda c: c[FE_]["values"]["instancia_sim"].update(solucoes=0), espera=FE_ + " nao selou inteiro"),
        variante("%s: o alcance sem o relativo ao leitor (D64)" % FE_, f_core=lambda c: c[FE_]["alcance"].update(frase="P = nP vale para as maquinas de Turing"), espera=FE_ + " nao selou inteiro"),
        variante("%s: os nomes do registro adulterados (D63; ratificados em 09/11, D74)" % FE_, f_core=lambda c: c[FE_].update(nomes={"IALD2": "adulterado"}), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma inscricao de 06 a 09/11 nao conferida" % FE_, f_core=lambda c: c[FE_]["inscriptions"].update({sorted(c[FE_]["inscriptions"])[0]: False}), espera=FE_ + " nao selou inteiro"),
        variante("%s: a ordem da v410 fora das inscricoes" % FE_, f_core=lambda c: c[FE_]["inscriptions"].pop(_CH_TRAD), espera=FE_ + " nao selou inteiro"),
        variante("%s: as ancoras de secao adulteradas" % FE_, f_core=lambda c: c[FE_]["ancoras_de_secao"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: uma chave antiga dita mudada" % FE_, f_core=lambda c: c[FE_].update(chaves_antigas_que_mudam=["rede_fock_v394.whole_certificate_inhabited"]), espera=FE_ + " nao selou inteiro"),
        variante("%s: a ancora principal dita outra" % FE_, f_core=lambda c: c[FE_].update(ancora_principal="TGLExt.IALD2.outra"), espera=FE_ + " nao selou inteiro"),
        variante("%s: as ressalvas adulteradas" % FE_, f_core=lambda c: c[FE_]["ressalvas"].pop(), espera=FE_ + " nao selou inteiro"),
        variante("%s: o registro move o gate" % FE_, f_core=lambda c: c[FE_].update(does_not_gate_core=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: o calculo do runtime nao rodou" % FE_, f_core=lambda c: c[FE_].update(runtime_executed=False), espera=FE_ + " nao selou inteiro"),
        variante("%s: a guarda das frases achou violacao no registro" % FE_, f_core=lambda c: c[FE_].update(guarda_violacoes=[["F47", "x"]]), espera=FE_ + " nao selou inteiro"),
        variante("uma bandeira do bundle da IALD2 falsa no kernel do rito", f_core=lambda c: _kf(c).__setitem__(FLAGS_[len(FLAGS_) // 2], False), espera="as bandeiras do fecho"),
        variante("a conferencia traz outro veredito de %s" % FE_, f_conf=lambda cj: cj.update({"veredito_iald2": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FE_),
        variante("selo primario: sem o resumo de %s" % FE_, f_selo=lambda s: s.pop(FE_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % FE_, f_selo=lambda s: s[FE_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v410", f_selo=lambda s: s.pop("registros_v410", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v410 do selo difere do core", f_selo=lambda s: s["registros_v410"][DLX.CUNHAGENS_REGISTRO].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: registros_v409 do selo difere do core", f_selo=lambda s: s["registros_v409"]["cunhagens_v409"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % FE_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v410"][FE_] not in l) + "\n", espera="o bloco " + FE_ + " do stdout"),
        variante("linha [v410] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v410] os registros com funcao e os por spec da v410" not in l) + "\n", espera="linha [v410]"),
        variante("linha [v410] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v410] os registros com funcao e os por spec da v410"), espera="a linha [v410] do stdout"),
        variante("linha [v410] com o h0dn nao selado", f_std=lambda t_: t_.replace("| h0dn_bg1_v410=SELOU", "| h0dn_bg1_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha [v410] com a escala nao selada", f_std=lambda t_: t_.replace("| a_escala_v410=SELOU", "| a_escala_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha [v410] com o recibo HMS/13 nao selado", f_std=lambda t_: t_.replace("| h0dn_fontes_hms13_v410=SELOU", "| h0dn_fontes_hms13_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha [v410] no formato antigo (iald2=%s | h0dn=%s)", f_std=lambda t_: re.sub(r"iald2_v410=SELOU \| a_escala_v410=SELOU \| h0dn_bg1_v410=SELOU \| h0dn_fontes_hms13_v410=SELOU", "iald2=SELOU | h0dn=SELOU", t_), espera="a linha [v410] do stdout"),
        variante("linha [v410] com a iald2 nao selada", f_std=lambda t_: t_.replace("iald2_v410=SELOU", "iald2_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha do bloco IALD2: uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N10, _N10), "ancoras ok = %d/%d" % (_N10 - 1, _N10)), espera=FE_ + " nao selou inteiro"),
        variante("AVISO da v410 (a IALD2, a escala ou o H0DN nao rodaram) no stdout", f_std=lambda t_: t_ + "   [v410] AVISO: o registro da IALD2 ou o do H0DN nao rodaram: ValueError('x')\n", espera="AVISO da v410"),
        variante("AVISO da v410 (o recibo HMS/13 ou os registros por spec nao rodaram) no stdout", f_std=lambda t_: t_ + "   [v410] AVISO: o registro do HMS/13 ou os registros por spec da v410 nao rodaram: ValueError('x')\n", espera="AVISO da v410"),
        # ---- 09/11: a SECAO 6 da pedra (o atrator, D71) e a c16 no registro iald2_v410; as falas de 07 e 09/11
        variante("%s: a resposta o_atrator ausente (D71)" % FE_, f_core=lambda c: c[FE_]["values"]["respostas"].pop("o_atrator"), espera=FE_ + " nao selou inteiro"),
        variante("%s: a ultima checagem (c16, o atrator) com o id adulterado" % FE_, f_core=lambda c: c[FE_]["mechanics"]["checks"][-1].update(id="c99"), espera=FE_ + " nao selou inteiro"),
        variante("%s: o_atrator fora das ancoras de secao" % FE_, f_core=lambda c: c[FE_]["ancoras_de_secao"].remove(DLX.ANCORA_ATRATOR), espera=FE_ + " nao selou inteiro"),
        variante("%s: a inscricao do atrator (07/11) fora das inscricoes" % FE_, f_core=lambda c: c[FE_]["inscriptions"].pop(DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_ATRATOR)), espera=FE_ + " nao selou inteiro"),
        variante("%s: a inscricao do selo (D76) fora das inscricoes" % FE_, f_core=lambda c: c[FE_]["inscriptions"].pop(DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_SELO)), espera=FE_ + " nao selou inteiro"),
        variante("ancora %s (o atrator) fora do trio" % DLX.ANCORA_ATRATOR.split(".")[-1], f_core=lambda c: _fora_do_trio(c, DLX.ANCORA_ATRATOR), espera="a ancora "),
        variante("ancora %s fora do trio" % DLX.ANCORA_NAO_E_TUDO.split(".")[-1], f_core=lambda c: _fora_do_trio(c, DLX.ANCORA_NAO_E_TUDO), espera="a ancora "),
        variante("ancora o_vacuo_e_ortogonal_ao_par_lido fora do trio", f_core=lambda c: _fora_do_trio(c, DLX.NS + "o_vacuo_e_ortogonal_ao_par_lido"), espera="a ancora "),
        # ---- 09/11: h0dn_bg1_v410 (D72, o SEGUNDO registro com funcao): o teste pre-registrado da razao de Hubble; pre-registrado; nenhum dado observado lido (observed_vector_read False em TODO lugar)
        variante("%s ausente do core" % H0_, f_core=lambda c: c.pop(H0_, None), espera="registro obrigatorio ausente do core: " + H0_),
        variante("%s: o registro nao selou" % H0_, f_core=lambda c: c[H0_].update(all_verified=False), espera=H0_ + " nao selou"),
        variante("%s: uma checagem do calculo falhou" % H0_, f_core=lambda c: c[H0_]["mechanics"]["checks"][5].update(ok=False), espera=MH_),
        variante("%s: o numero de checagens != o do delta" % H0_, f_core=lambda c: c[H0_]["mechanics"]["checks"].pop(), espera=MH_),
        variante("%s: um valor do calculo adulterado (K)" % H0_, f_core=lambda c: c[H0_]["values"].update(K=c[H0_]["values"]["K"] + 1e-3), espera=MH_),
        variante("%s: o D esperado de um modelo adulterado" % H0_, f_core=lambda c: c[H0_]["values"]["D_esperado"][0].update(D=c[H0_]["values"]["D_esperado"][0]["D"] + 1.0), espera=MH_),
        variante("%s: beta != alfa x raiz de e do core" % H0_, f_core=lambda c: c[H0_]["values"].update(beta=0.0121), espera=MH_),
        variante("%s: beta_ok falso no registro" % H0_, f_core=lambda c: c[H0_].update(beta_ok=False), espera=MH_),
        variante("%s: veredito diferente do ensaio a seco" % H0_, f_core=lambda c: c[H0_].update(verdict="OUTRO_VEREDITO"), espera=H0_ + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: o registro move o gate" % H0_, f_core=lambda c: c[H0_].update(does_not_gate_core=False), espera=MH_),
        variante("%s: o calculo do runtime nao rodou" % H0_, f_core=lambda c: c[H0_].update(runtime_executed=False), espera=MH_),
        variante("%s: o gate dos values difere do da v409" % H0_, f_core=lambda c: c[H0_]["values"].update(gate_verdict="OUTRO_GATE"), espera=MH_),
        variante("%s: observed_vector_read dito True no registro (D72: nenhum vetor observado lido)" % H0_, f_core=lambda c: c[H0_].update(observed_vector_read=True), espera=MOBS_),
        variante("%s: observed_vector_read dito True nos values" % H0_, f_core=lambda c: c[H0_]["values"].update(observed_vector_read=True), espera=MOBS_),
        variante("%s: o sha256 do texto-fonte da funcao de veredito removido" % H0_, f_core=lambda c: c[H0_].pop("veredito_h0dn_source_sha256"), espera=MH_),
        variante("%s: o sha256 do texto-fonte nos values diferente" % H0_, f_core=lambda c: c[H0_]["values"].update(veredito_h0dn_source_sha256="0" * 64), espera=MH_),
        variante("%s: um pino do FREEZE_R2 com o sha256 falso" % H0_, f_core=lambda c: next(iter(c[H0_]["values"]["pinos"].values())).update(sha256_ok=False), espera=MH_),
        variante("%s: os ramos vistos incompletos (a funcao de veredito nao cobre os seis)" % H0_, f_core=lambda c: c[H0_]["values"].update(ramos_vistos=[1, 2, 3]), espera=MH_),
        variante("%s: a cabeca do ramo da leitura sem a validade na mesma string (D76)" % H0_, f_core=lambda c: _vet_ramo(c, 4).update(cabeca="X__GATE_UNMOVED"), espera=MH_),
        variante("%s: a palavra do livro de cobrancas na cabeca de um ramo (E30)" % H0_, f_core=lambda c: _vet_ramo(c, 5).update(cabeca="NOT_FALSIFIED__" + _vet_ramo(c, 5)["cabeca"]), espera=MH_),
        variante("%s: os insumos pinados != os do candidato" % H0_, f_core=lambda c: next(iter(c[H0_]["insumos_pinados"].values())).update(sha256="0" * 64), espera=MH_),
        variante("%s: a ordem ao Kimi com outro sha256" % H0_, f_core=lambda c: c[H0_]["ordem_kimi"].update(sha256="0" * 64), espera=MH_),
        variante("%s: um token proibido no texto do registro (scope)" % H0_, f_core=lambda c: c[H0_].update(scope=c[H0_]["scope"] + " " + _TOK_H0), espera=MH_),
        variante("%s: o texto sem a frase obrigatoria da D72 (estatuto)" % H0_, f_core=lambda c: c[H0_].update(estatuto=c[H0_]["estatuto"].replace(DLX.FRASE_H0DN_OBRIGATORIA_PT, "XXXX")), espera=MH_),
        variante("%s: o teste dado por feito no texto (F53)" % H0_, f_core=lambda c: c[H0_].update(diz=list(c[H0_]["diz"]) + ["o H0DN: o teste deu 5 sigma, pré-registrado; nenhum dado observado lido"]), espera=MH_),
        variante("%s: a aritmetica do agregado publico no texto" % H0_, f_core=lambda c: c[H0_].update(limites=list(c[H0_]["limites"]) + [DLX.H0DN_AGREGADO_NAO_ENTRA[0] + " (pré-registrado; nenhum dado observado lido)"]), espera=MH_),
        variante("%s: a guarda P18 achou violacao nos values" % H0_, f_core=lambda c: c[H0_]["values"].update(p18_violacoes=[["R1", "x"]]), espera=MH_),
        variante("selo primario: sem o resumo de %s" % H0_, f_selo=lambda s: s.pop(H0_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % H0_, f_selo=lambda s: s[H0_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s com observed_vector_read True" % H0_, f_selo=lambda s: s[H0_].update(observed_vector_read=True), espera=MOBS_),
        variante("selo primario: o resumo de %s com outro n_checks_esperadas" % H0_, f_selo=lambda s: s[H0_].update(n_checks_esperadas=_NCHK_ - 1), espera=MH_),
        variante("a conferencia traz outro veredito de %s" % H0_, f_conf=lambda cj: cj.update({"veredito_h0dn": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + H0_),
        variante("o bloco do H0DN ausente do stdout (cabecalho, pinos e veredito)", f_std=_sem_bloco_h0dn, espera=MH_),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % H0_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v410"][H0_] not in l) + "\n", espera="o bloco " + H0_ + " do stdout"),
        variante("linha do bloco do H0DN: vetor observado lido = True", f_std=lambda t_: t_.replace("vetor observado lido = False", "vetor observado lido = True"), espera=MH_),
        variante("linha do bloco do H0DN: um pino a menos", f_std=lambda t_: t_.replace("pinos ok = %d/%d" % (_NPIN_, _NPIN_), "pinos ok = %d/%d" % (_NPIN_ - 1, _NPIN_)), espera=MH_),
        variante("linha do bloco do H0DN: uma checagem a menos", f_std=lambda t_: t_.replace("checagens ok = %d/%d" % (_NCHK_, _NCHK_), "checagens ok = %d/%d" % (_NCHK_ - 1, _NCHK_)), espera=MH_),
        variante_json("ESPERADOS sem registros_funcao_v410.h0dn (fail-closed)", _so_esp(lambda d: d["registros_funcao_v410"].pop("h0dn")), "ESPERADOS_v410.json nao traz registros_funcao_v410.h0dn"),
        variante_json("ESPERADOS sem o veredito do ensaio a seco de %s" % H0_, _so_esp(lambda d: d["vereditos_novos_v410"].pop(H0_)), "ESPERADOS_v410 nao traz o veredito do ensaio a seco de " + H0_),
        variante_json("ESPERADOS: o veredito de %s em registros_funcao_v410 diferente" % H0_, _so_esp(lambda d: d["registros_funcao_v410"]["h0dn"].update(verdict="OUTRO_VEREDITO")), MH_),
        variante_json("ESPERADOS: um valor de %s diferente do core" % H0_, _so_esp(lambda d: d["registros_funcao_v410"]["h0dn"]["values"].update(K=d["registros_funcao_v410"]["h0dn"]["values"]["K"] + 1e-3)), MH_),
        variante_json("CANDIDATO: observed_vector_read True em h0dn", _so_cm(lambda d: d["h0dn"].update(observed_vector_read=True)), MOBS_),
        variante_json("CANDIDATO: os insumos do h0dn != os do core", _so_cm(lambda d: next(iter(d["h0dn"]["insumos"].values())).update(sha256="0" * 64)), MH_),
        variante_json("CANDIDATO sem a chave h0dn", _so_cm(lambda d: d.pop("h0dn")), MH_),
        # ---- 09/11 (parte 2): a_escala_v410 (D86/D87, o SEGUNDO registro com funcao): a pedra AEscala; os nomes ratificados; a forma canonica do Clay (D84) e a da D83: validade no kernel, a creditacao e' do Clay
        variante("%s ausente do core" % AE_, f_core=lambda c: c.pop(AE_, None), espera="registro obrigatorio ausente do core: " + AE_),
        variante("%s: o registro nao selou" % AE_, f_core=lambda c: c[AE_].update(all_verified=False), espera=AE_ + " nao selou"),
        variante("%s: uma checagem do calculo falhou" % AE_, f_core=lambda c: c[AE_]["mechanics"]["checks"][3].update(ok=False), espera=MAE_),
        variante("%s: o numero de checagens != o do delta" % AE_, f_core=lambda c: c[AE_]["mechanics"]["checks"].pop(), espera=MAE_),
        variante("%s: os nomes nao ratificados (D87)" % AE_, f_core=lambda c: c[AE_].update(nomes_ratificados=False), espera=MAE_),
        variante("%s: um numero da escala adulterado (tres faces)" % AE_, f_core=lambda c: c[AE_]["values"]["numeros"].update(tres_faces="2"), espera=MAE_),
        variante("%s: o numero de ancoras ok adulterado" % AE_, f_core=lambda c: c[AE_]["values"].update(n_ancoras_ok=_NAE_ - 1), espera=MAE_),
        variante("%s: o numero de bandeiras True adulterado" % AE_, f_core=lambda c: c[AE_]["values"].update(n_flags_true=c[AE_]["values"]["n_flags_true"] - 1), espera=MAE_),
        variante("%s: uma fala de 09/11 nao conferida por sha256" % AE_, f_core=lambda c: c[AE_]["values"]["falas"].update({sorted(c[AE_]["values"]["falas"])[0]: False}), espera=MAE_),
        variante("%s: a forma canonica do Clay (D84) trocada" % AE_, f_core=_escala_forma_trocada, espera=MAE_),
        variante("%s: a forma da D83 trocada" % AE_, f_core=lambda c: c[AE_].update(frase_d83_pt="a TGL resolveu."), espera=MAE_),
        variante("%s: a ratificacao (D87) com outro sha256" % AE_, f_core=lambda c: c[AE_]["ratificacao"].update(sha256="0" * 64), espera=MAE_),
        variante("%s: veredito diferente do ensaio a seco" % AE_, f_core=lambda c: c[AE_].update(verdict="OUTRO_VEREDITO"), espera=AE_ + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: beta_ok falso no registro" % AE_, f_core=lambda c: c[AE_].update(beta_ok=False), espera=MAE_),
        variante("%s: o registro move o gate" % AE_, f_core=lambda c: c[AE_].update(does_not_gate_core=False), espera=MAE_),
        variante("%s: o gate dos values difere do da v409" % AE_, f_core=lambda c: c[AE_]["values"].update(gate_verdict="OUTRO_GATE"), espera=MAE_),
        variante("%s: uma chave antiga dita mudada" % AE_, f_core=lambda c: c[AE_].update(chaves_antigas_que_mudam=["rede_fock_v394.whole_certificate_inhabited"]), espera=MAE_),
        variante("%s: a palavra do Clay dita resolvida a seco no texto (F58)" % AE_, f_core=lambda c: c[AE_].update(limites=list(c[AE_]["limites"]) + ["o Clay esta resolvido"]), espera=MAE_),
        variante("%s: o texto sem a forma canonica do Clay (tirada de todos os campos de texto que a leitura le)" % AE_, f_core=lambda c: c[AE_].update({k_: json.loads(json.dumps(c[AE_].get(k_), ensure_ascii=False).replace(DLX.FRASE_CLAY_CANONICA_PT, "XXXX")) for k_ in ("estatuto", "scope", "limites", "diz", "nao_diz")}), espera=MAE_),   # (09/11, achado da 1a rodada: a frase mora em varios campos; tirar so' do estatuto nao a tira do texto)
        variante("%s: P = nP dito nao provado no texto (F57)" % AE_, f_core=lambda c: c[AE_].update(diz=list(c[AE_]["diz"]) + ["P = nP de Turing nao foi provado"]), espera=MAE_),
        variante("%s: uma ancora da AEscala fora do trio" % AE_, f_core=lambda c: _fora_do_trio(c, next(iter(DLX.ANCORAS_AESCALA))), espera="a ancora "),
        variante("%s: os nomes novos da R3 ditos ratificados (R1)" % AE_, f_core=lambda c: c[AE_].update(estatuto_dos_nomes_ratificados_d101="RATIFICADOS pelo operador"), espera=MAE_),
        variante("%s: um nome novo a ratificar retirado do registro (R1)" % AE_, f_core=lambda c: c[AE_]["nomes_novos_da_pedra"].pop(), espera=MAE_),
        variante("%s: a pendencia de ratificacao esvaziada (R1)" % AE_, f_core=lambda c: c[AE_].update(ratificacao_pendente={}), espera=MAE_),
        # ---- 10/11 (R2, D99; ADENDO 4): a clausula do limite do teorema do Tetelestai ao lado de todo texto do registro que o anuncia (PT e EN) e os seis nomes de enunciado mudado (B3): cada retirada tem de reprovar o portao
        variante("%s: a clausula do limite do teorema do Tetelestai retirada de UM campo de texto (diz) (R2, D99)" % AE_, f_core=lambda c: c[AE_].update(diz=[x_.replace(DLX.CLAUSULA_Z_PT, "(retirada)") for x_ in c[AE_]["diz"]]), espera="a clausula do limite do teorema do Tetelestai"),
        variante("%s: a clausula do limite retirada de TODOS os campos de texto que a leitura le (R2, D99)" % AE_, f_core=lambda c: c[AE_].update({k_: json.loads(json.dumps(c[AE_].get(k_), ensure_ascii=False).replace(DLX.CLAUSULA_Z_PT, "XXXX")) for k_ in ("estatuto", "scope", "limites", "diz", "nao_diz")}), espera="a clausula do limite do teorema do Tetelestai"),
        variante("%s: a clausula EN do registro trocada (R2, D99)" % AE_, f_core=lambda c: c[AE_].update(clausula_z_en="the threshold is the cost of summing the terms"), espera="a clausula do limite do teorema do Tetelestai"),
        variante("%s: a frase dos seis nomes retirada de limites (R2, B3)" % AE_, f_core=lambda c: c[AE_].update(limites=[x_.replace(DLX.FRASE_SEIS_NOMES_PT, "(retirada)") for x_ in c[AE_]["limites"]]), espera="os seis nomes de enunciado mudado"),
        variante("%s: uma folha de texto anuncia o teorema (linear nos bits) sem a clausula (R2, D99)" % AE_, f_core=lambda c: c[AE_].update(nao_diz=list(c[AE_]["nao_diz"]) + ["o teorema do Tetelestai e' a decisao em tempo finito do ciclo, linear nos bits"]), espera="a clausula do limite do teorema do Tetelestai"),
        variante("%s: a ponte da escala adulterada (R1)" % AE_, f_core=lambda c: c[AE_]["values"]["ponte"]["casos"][1].__setitem__(2, "1/9"), espera=MAE_),
        variante("%s: a ponte da escala dita nao recalculada (R1)" % AE_, f_core=lambda c: c[AE_]["values"]["ponte"].update(ok=False), espera=MAE_),
        variante("%s: um campo novo da estrutura fora dos values (R1)" % AE_, f_core=lambda c: c[AE_]["values"]["campos_novos_na_estrutura"].pop(sorted(c[AE_]["values"]["campos_novos_na_estrutura"])[0]), espera=MAE_),
        variante("selo primario: sem o resumo de %s" % AE_, f_selo=lambda s: s.pop(AE_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % AE_, f_selo=lambda s: s[AE_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s com os nomes nao ratificados" % AE_, f_selo=lambda s: s[AE_].update(nomes_ratificados=False), espera=MAE_),
        variante("o bloco A ESCALA ausente do stdout (cabecalho, contagens e veredito)", f_std=lambda t_: _sem_bloco_n(t_, "A ESCALA [v410"), espera=MAE_),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % AE_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v410"][AE_] not in l) + "\n", espera="o bloco " + AE_ + " do stdout"),
        variante("linha do bloco A ESCALA: uma ancora a menos", f_std=lambda t_: _no_bloco(t_, "A ESCALA [v410", "ancoras ok = %d/%d" % (_NAE_, _NAE_), "ancoras ok = %d/%d" % (_NAE_ - 1, _NAE_)), espera=MAE_),
        variante("linha do bloco A ESCALA: uma checagem a menos", f_std=lambda t_: _no_bloco(t_, "A ESCALA [v410", "checagens ok = %d/%d" % (_NCHK_AE_, _NCHK_AE_), "checagens ok = %d/%d" % (_NCHK_AE_ - 1, _NCHK_AE_)), espera=MAE_),
        variante("linha do bloco A ESCALA: um numero da escala trocado", f_std=lambda t_: _no_bloco(t_, "A ESCALA [v410", "'meio': '%s'" % DLX.NUMEROS_AESCALA["meio"], "'meio': '9/9'"), espera=MAE_),
        variante("a conferencia traz outro veredito de %s" % AE_, f_conf=lambda cj: cj.update({"veredito_a_escala": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + AE_),
        variante_json("ESPERADOS sem registros_funcao_v410.a_escala (fail-closed)", _so_esp(lambda d: d["registros_funcao_v410"].pop("a_escala")), "ESPERADOS_v410.json nao traz registros_funcao_v410.a_escala"),
        variante_json("ESPERADOS sem o veredito do ensaio a seco de %s" % AE_, _so_esp(lambda d: d["vereditos_novos_v410"].pop(AE_)), "ESPERADOS_v410 nao traz o veredito do ensaio a seco de " + AE_),
        variante_json("CANDIDATO: os nomes da escala nao ratificados", _so_cm(lambda d: d["aescala"].update(nomes_ratificados=False)), MAE_),
        variante_json("CANDIDATO: os nomes novos da escala fora do manifesto (R1)", _so_cm(lambda d: d["aescala"].pop("nomes_novos_da_pedra")), MAE_),
        variante_json("CANDIDATO sem a chave aescala", _so_cm(lambda d: d.pop("aescala")), MAE_),
        # ---- 09/11 (parte 2): h0dn_fontes_hms13_v410 (D80, o QUARTO registro com funcao): o recibo documental HMS/13, aditivo e posterior ao FREEZE_R2; cobertura documental de fontes, nao covariancia fisica fechada; nada aberto
        variante("%s ausente do core" % HM_, f_core=lambda c: c.pop(HM_, None), espera="registro obrigatorio ausente do core: " + HM_),
        variante("%s: o registro nao selou" % HM_, f_core=lambda c: c[HM_].update(all_verified=False), espera=HM_ + " nao selou"),
        variante("%s: uma checagem do calculo falhou" % HM_, f_core=lambda c: c[HM_]["mechanics"]["checks"][6].update(ok=False), espera=MHM_),
        variante("%s: o numero de checagens != o do delta" % HM_, f_core=lambda c: c[HM_]["mechanics"]["checks"].pop(), espera=MHM_),
        variante("%s: observed_vector_read dito True no registro (D72, D80)" % HM_, f_core=lambda c: c[HM_].update(observed_vector_read=True), espera=MOBSH_),
        variante("%s: observed_vector_read dito True nos values" % HM_, f_core=lambda c: c[HM_]["values"].update(observed_vector_read=True), espera=MOBSH_),
        variante("%s: a entrega do Kimi aberta em rito (le_em_rito True)" % HM_, f_core=lambda c: c[HM_].update(le_em_rito=True), espera=MOBSH_),
        variante("%s: um dos dez campos da ordem trocado (covariancia fisica dita fechada)" % HM_, f_core=lambda c: c[HM_]["values"]["campos"].update(physical_covariance_closed=True), espera=MHM_),
        variante("%s: a abertura dita permitida no campo opening_allowed" % HM_, f_core=lambda c: c[HM_]["values"]["campos"].update(opening_allowed=True), espera=MHM_),
        variante("%s: um caminho sob a pasta vedada tocado" % HM_, f_core=lambda c: c[HM_]["values"].update(sob_pasta_vedada=[os.path.join(DLX.H0DN_PASTA_VEDADA, "x")]), espera=MHM_),
        variante("%s: um numero proibido plantado (guarda numerica)" % HM_, f_core=lambda c: c[HM_]["values"]["numeros"].update(proibidos=[["/objects/0/x", 1]]), espera=MHM_),
        variante("%s: um artefato embutido com o sha256 falso" % HM_, f_core=lambda c: next(iter(c[HM_]["values"]["pinos"].values())).update(sha256_ok=False), espera=MHM_),
        variante("%s: um ID de calibrador a mais" % HM_, f_core=lambda c: c[HM_]["values"]["ids_calibradores"].append("SN_FALSA"), espera=MHM_),
        variante("%s: o gate dos values difere do da v409" % HM_, f_core=lambda c: c[HM_]["values"].update(gate_verdict="OUTRO_GATE"), espera=MHM_),
        variante("%s: veredito diferente do ensaio a seco" % HM_, f_core=lambda c: c[HM_].update(verdict="OUTRO_VEREDITO"), espera=HM_ + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: o registro move o gate" % HM_, f_core=lambda c: c[HM_].update(does_not_gate_core=False), espera=MHM_),
        variante("%s: um token proibido no texto do registro (scope)" % HM_, f_core=lambda c: c[HM_].update(scope=c[HM_]["scope"] + " " + _TOK_H0), espera=MHM_),
        variante("%s: o texto sem a frase obrigatoria da D80" % HM_, f_core=_hms13_sem_obrigacao, espera=MHM_),
        variante("%s: a abertura dita permitida no texto (F56)" % HM_, f_core=lambda c: c[HM_].update(diz=list(c[HM_]["diz"]) + ["a abertura esta autorizada"]), espera=MHM_),
        variante("%s: a forma HMS completa dita admitida no texto (F56)" % HM_, f_core=lambda c: c[HM_].update(diz=list(c[HM_]["diz"]) + ["a forma HMS completa é admitida"]), espera=MHM_),
        variante("%s: o h0dn_bg1_v410 anterior nao selado" % HM_, f_core=lambda c: c[H0_].update(all_verified=False), espera=H0_ + " nao selou"),
        variante("selo primario: sem o resumo de %s" % HM_, f_selo=lambda s: s.pop(HM_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % HM_, f_selo=lambda s: s[HM_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s com observed_vector_read True" % HM_, f_selo=lambda s: s[HM_].update(observed_vector_read=True), espera=MOBSH_),
        variante("selo primario: o resumo de %s com le_em_rito True" % HM_, f_selo=lambda s: s[HM_].update(le_em_rito=True), espera=MOBSH_),
        variante("o bloco H0DN FONTES HMS/13 ausente do stdout (cabecalho, contagens e veredito)", f_std=lambda t_: _sem_bloco_n(t_, "H0DN FONTES HMS/13 [v410"), espera=MHM_),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % HM_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v410"][HM_] not in l) + "\n", espera="o bloco " + HM_ + " do stdout"),
        variante("linha do bloco HMS/13: um artefato embutido a menos", f_std=lambda t_: _no_bloco(t_, "H0DN FONTES HMS/13 [v410", "artefatos embutidos ok = %d/%d" % (_NEMB_, _NEMB_), "artefatos embutidos ok = %d/%d" % (_NEMB_ - 1, _NEMB_)), espera=MHM_),
        variante("linha do bloco HMS/13: uma checagem a menos", f_std=lambda t_: _no_bloco(t_, "H0DN FONTES HMS/13 [v410", "checagens ok = %d/%d" % (_NCHK_HM_, _NCHK_HM_), "checagens ok = %d/%d" % (_NCHK_HM_ - 1, _NCHK_HM_)), espera=MHM_),
        variante("linha do bloco HMS/13: um caminho sob a pasta vedada", f_std=lambda t_: _no_bloco(t_, "H0DN FONTES HMS/13 [v410", "caminhos sob a pasta vedada = 0", "caminhos sob a pasta vedada = 1"), espera=MHM_),
        variante("a conferencia traz outro veredito de %s" % HM_, f_conf=lambda cj: cj.update({"veredito_hms13": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + HM_),
        variante_json("ESPERADOS sem registros_funcao_v410.hms13 (fail-closed)", _so_esp(lambda d: d["registros_funcao_v410"].pop("hms13")), "ESPERADOS_v410.json nao traz registros_funcao_v410.hms13"),
        variante_json("ESPERADOS sem o veredito do ensaio a seco de %s" % HM_, _so_esp(lambda d: d["vereditos_novos_v410"].pop(HM_)), "ESPERADOS_v410 nao traz o veredito do ensaio a seco de " + HM_),
        variante_json("CANDIDATO: observed_vector_read True em hms13", _so_cm(lambda d: d["hms13"].update(observed_vector_read=True)), MOBSH_),
        variante_json("CANDIDATO: le_em_rito True em hms13", _so_cm(lambda d: d["hms13"].update(le_em_rito=True)), MOBSH_),
        variante_json("CANDIDATO sem a chave hms13", _so_cm(lambda d: d.pop("hms13")), MHM_),
        variante("full_static_witness_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["qg_closure"]["gate"].update(full_static_witness_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        variante("trivial_inhabitant_exists dito True (deve ficar False por teorema)", f_core=lambda c: c["witness_rigidity"].update(trivial_inhabitant_exists=True), espera="full_static_witness_exists e trivial_inhabitant_exists devem seguir False"),
        # ---- a CHAVE DO LEMA no registro da testemunha (v409, herdada): segue lida True do kernel, com o dict elo_v407
        variante("testemunha_estatica_v396: a chave do lema de volta a literal False", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"].update(linked_to_the_corner_by_a_lemma=False), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o dict elo_v407 ausente", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"].pop("elo_v407"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o elo dito de VETORES (Omega identificado com o vetor de Bell)", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(identifies_omega_with_bell_vector=True), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: o par na face de Fock dito provado", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(pair_on_the_fock_face="PROVED"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("testemunha_estatica_v396: a ponte Bell-TT dita termo", f_core=lambda c: c["testemunha_estatica_v396"]["fock_face"]["elo_v407"].update(bell_to_tt_bridge="A_TERM"), espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
        variante("psibit_v395: o status antigo (CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE)", f_core=lambda c: c["psibit_v395"]["conditional_psion_face"].update(status="CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE"), espera="psibit_v395: a face do psion nao le o habitante"),
        variante("a conferencia diz chave_do_lema != True", f_conf=lambda cj: cj.update({"chave_do_lema": False}), espera="chave_do_lema != True"),
        # ---- traducao_turing_v409 (HERDADO da v409, recriado pelo rito da v410; a escada do contrato subida pela C12)
        variante("%s (herdado) ausente do core" % F9_, f_core=lambda c: c.pop(F9_, None), espera="registro obrigatorio ausente do core: " + F9_),
        variante("%s (herdado): o registro nao selou" % F9_, f_core=lambda c: c[F9_].update(all_verified=False), espera=F9_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % F9_, f_core=lambda c: c[F9_]["mechanics"]["checks"][2].update(ok=False), espera=HERD9_),
        variante("%s (herdado): a integra do acervo da v407 dita pinada (D57d)" % F9_, f_core=lambda c: c[F9_]["acervo_v407_repinado"].update(integra_pinada=True), espera=HERD9_),
        variante("%s (herdado): o pino do acervo da v407 com outro sha256" % F9_, f_core=lambda c: c[F9_]["acervo_v407_repinado"].update(sha256="0" * 64), espera=HERD9_),
        variante("%s (herdado): a resposta do modo selecao ausente" % F9_, f_core=lambda c: c[F9_]["values"]["respostas"].pop("o_np_e_o_modo_selecao"), espera=HERD9_),
        variante("%s (herdado): veredito diferente do esperado" % F9_, f_core=lambda c: c[F9_].update(verdict="OUTRO_VEREDITO"), espera=F9_ + VER_HERD),
        variante("ancora %s da v409 (traducao_turing_v409) fora do trio" % _a9.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a9), espera="as ancoras do traducao_turing_v409 (herdadas)"),
        variante("o bundle da v409: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b9, "0" * 64), espera="o bundle da v409"),
        variante("a conferencia traz outro veredito de %s (herdado)" % F9_, f_conf=lambda cj: cj.update({"veredito_traducao_turing_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + F9_),
        variante("linha [v409] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v409] o registro da traducao e os registros por spec da v409" not in l) + "\n", espera="linha [v409]"),
        variante("linha [v409] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v409] o registro da traducao e os registros por spec da v409"), espera="a linha [v409] do stdout"),
        variante("linha do bloco A TRADUCAO AS CLASSES DE TURING (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N9, _N9), "ancoras ok = %d/%d" % (_N9 - 1, _N9)), espera=HERD9_),
        # ---- tetelestai_terminal_v408 (HERDADO da v408, recriado pelo rito da v410; a escada do contrato subida pela C12)
        variante("%s (herdado) ausente do core" % FT_, f_core=lambda c: c.pop(FT_, None), espera="registro obrigatorio ausente do core: " + FT_),
        variante("%s (herdado): o registro nao selou" % FT_, f_core=lambda c: c[FT_].update(all_verified=False), espera=FT_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % FT_, f_core=lambda c: c[FT_]["mechanics"]["checks"][2].update(ok=False), espera=HERDT_),
        variante("%s (herdado): o numero de checagens != o do delta da v409" % FT_, f_core=lambda c: c[FT_]["mechanics"]["checks"].pop(), espera=HERDT_),
        variante("%s (herdado): o numero de modulos ok adulterado" % FT_, f_core=lambda c: c[FT_]["values"].update(n_modulos_ok=DLX.D8.N_BUNDLE - 1), espera=HERDT_),
        variante("%s (herdado): a escada do registro != a do ensaio" % FT_, f_core=lambda c: c[FT_]["values"].update(escada=[1, 1, 1]), espera=HERDT_),
        variante("%s (herdado): beta != alfa x raiz de e do core" % FT_, f_core=lambda c: c[FT_]["values"].update(beta=0.0121), espera=HERDT_),
        variante("%s (herdado): veredito diferente do esperado" % FT_, f_core=lambda c: c[FT_].update(verdict="OUTRO_VEREDITO"), espera=FT_ + VER_HERD),
        variante("%s (herdado): as ressalvas adulteradas" % FT_, f_core=lambda c: c[FT_]["ressalvas"].pop(), espera=HERDT_),
        variante("%s (herdado): o registro move o gate" % FT_, f_core=lambda c: c[FT_].update(does_not_gate_core=False), espera=HERDT_),
        variante("%s (herdado): o calculo do runtime nao rodou" % FT_, f_core=lambda c: c[FT_].update(runtime_executed=False), espera=HERDT_),
        variante("ancora %s da v408 (tetelestai_terminal_v408) fora do trio" % _a8.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a8), espera="as ancoras do tetelestai_terminal_v408 (herdadas)"),
        variante("ancora %s da v408 (tetelestai_terminal_v408): a bandeira falsa" % _a8.split(".")[-1], f_core=lambda c: _kf(c).__setitem__(_EST8[_a8]["bandeira"], False), espera="as ancoras do tetelestai_terminal_v408 (herdadas)"),
        variante("o bundle da v408: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b8, "0" * 64), espera="o bundle da v408"),
        variante("a conferencia traz outro veredito de %s (herdado)" % FT_, f_conf=lambda cj: cj.update({"veredito_tetelestai_terminal": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FT_),
        variante("selo primario: sem o resumo de %s (herdado)" % FT_, f_selo=lambda s: s.pop(FT_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FT_, f_selo=lambda s: s[FT_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v408", f_selo=lambda s: s.pop("registros_v408", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v408 do selo difere do core", f_selo=lambda s: s["registros_v408"]["cunhagens_v408"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FT_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FT_) not in l) + "\n", espera="o bloco " + FT_ + " do stdout"),
        variante("linha [v408] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v408] o registro do terminal e os registros por spec da v408" not in l) + "\n", espera="linha [v408]"),
        variante("linha [v408] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v408] o registro do terminal e os registros por spec da v408"), espera="a linha [v408] do stdout"),
        variante("linha do bloco TETELESTAI E' O TERMINAL (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N8, _N8), "ancoras ok = %d/%d" % (_N8 - 1, _N8)), espera=HERDT_),
        variante("AVISO da v409 herdada (o terminal nao rodou) no stdout", f_std=lambda t_: t_ + "   [v408] AVISO: o registro do terminal ou os registros por spec da v409 nao rodaram: ValueError('x')\n", espera="AVISO da v410"),
        # ---- psion_canto_v407 (HERDADO da v407, recriado pelo rito da v410; a escada do contrato subida pela C12)
        variante("%s (herdado) ausente do core" % FP_, f_core=lambda c: c.pop(FP_, None), espera="registro obrigatorio ausente do core: " + FP_),
        variante("%s (herdado): o registro nao selou" % FP_, f_core=lambda c: c[FP_].update(all_verified=False), espera=FP_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % FP_, f_core=lambda c: c[FP_]["mechanics"]["checks"][2].update(ok=False), espera=HERDP_),
        variante("%s (herdado): o numero de checagens != o do delta da v409" % FP_, f_core=lambda c: c[FP_]["mechanics"]["checks"].pop(), espera=HERDP_),
        variante("%s (herdado): o numero de modulos ok adulterado" % FP_, f_core=lambda c: c[FP_]["values"].update(n_modulos_ok=DLX.D7.N_BUNDLE - 1), espera=HERDP_),
        variante("%s (herdado): o numero de bandeiras True adulterado" % FP_, f_core=lambda c: c[FP_]["values"].update(n_flags_true=c[FP_]["values"]["n_flags"] - 1), espera=HERDP_),
        variante("%s (herdado): a escada do registro != a do ensaio" % FP_, f_core=lambda c: c[FP_]["values"].update(escada=[1, 1, 1]), espera=HERDP_),
        variante("%s (herdado): beta != alfa x raiz de e do core" % FP_, f_core=lambda c: c[FP_]["values"].update(beta=0.0121), espera=HERDP_),
        variante("%s (herdado): beta_ok falso" % FP_, f_core=lambda c: c[FP_].update(beta_ok=False), espera=HERDP_),
        variante("%s (herdado): veredito diferente do esperado" % FP_, f_core=lambda c: c[FP_].update(verdict="OUTRO_VEREDITO"), espera=FP_ + VER_HERD),
        variante("%s (herdado): o elo das duas faces dito NAO lido do kernel" % FP_, f_core=lambda c: c[FP_].update(link_read_from_the_kernel=False), espera=HERDP_),
        variante("%s (herdado): a chave do lema lida False no registro" % FP_, f_core=lambda c: c[FP_]["keys"].update({"testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": False}), espera=HERDP_),
        variante("%s (herdado): o teste (d) deixou de ser so' citado" % FP_, f_core=lambda c: c[FP_]["teste_d"].update(so_citado=False), espera=HERDP_),
        variante("%s (herdado): as ressalvas adulteradas" % FP_, f_core=lambda c: c[FP_]["ressalvas"].pop(), espera=HERDP_),
        variante("%s (herdado): o registro move o gate" % FP_, f_core=lambda c: c[FP_].update(does_not_gate_core=False), espera=HERDP_),
        variante("%s (herdado): o calculo do runtime nao rodou" % FP_, f_core=lambda c: c[FP_].update(runtime_executed=False), espera=HERDP_),
        variante("%s (herdado): a guarda das frases achou violacao no registro" % FP_, f_core=lambda c: c[FP_].update(guarda_violacoes=[["F17", "x"]]), espera=HERDP_),
        variante("ancora %s da v407 (psion_canto_v407) fora do trio" % _a7.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a7), espera="as ancoras do psion_canto_v407 (herdadas)"),
        variante("ancora %s da v407 (psion_canto_v407): a bandeira falsa" % _a7.split(".")[-1], f_core=lambda c: _kf(c).__setitem__(_EST7[_a7]["bandeira"], False), espera="as ancoras do psion_canto_v407 (herdadas)"),
        variante("o bundle da v407: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b7, "0" * 64), espera="o bundle da v407"),
        variante("a conferencia traz outro veredito de %s (herdado)" % FP_, f_conf=lambda cj: cj.update({"veredito_psion_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FP_),
        variante("selo primario: sem o resumo de %s (herdado)" % FP_, f_selo=lambda s: s.pop(FP_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FP_, f_selo=lambda s: s[FP_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v407", f_selo=lambda s: s.pop("registros_v407", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v407 do selo difere do core", f_selo=lambda s: s["registros_v407"]["cunhagens_v407"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FP_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FP_) not in l) + "\n", espera="o bloco " + FP_ + " do stdout"),
        variante("linha [v407] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v407] o registro do psion e do canto e os registros por spec da v407" not in l) + "\n", espera="linha [v407]"),
        variante("linha [v407] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v407] o registro do psion e do canto e os registros por spec da v407"), espera="a linha [v407] do stdout"),
        variante("linha do bloco O PSION, O CANTO E O PAR (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N7, _N7), "ancoras ok = %d/%d" % (_N7 - 1, _N7)), espera=HERDP_),
        variante("linha do bloco O PSION, O CANTO E O PAR (herdado): chave do lema dita False", f_std=lambda t_: t_.replace("chave do lema (lida do kernel) = True", "chave do lema (lida do kernel) = False"), espera=HERDP_),
        variante("AVISO da v407 herdada (o psion e o canto nao rodou) no stdout", f_std=lambda t_: t_ + "   [v407] AVISO: o registro do psion e do canto ou os registros por spec da v407 nao rodaram: ValueError('x')\n", espera="AVISO da v410"),
        # ---- fechamento_v406 (HERDADO da v406, recriado pelo rito da v410, c8 versionada pela E20)
        variante("%s (herdado) ausente do core" % FH_, f_core=lambda c: c.pop(FH_, None), espera="registro obrigatorio ausente do core: " + FH_),
        variante("%s (herdado): o registro nao selou" % FH_, f_core=lambda c: c[FH_].update(all_verified=False), espera=FH_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % FH_, f_core=lambda c: c[FH_]["mechanics"]["checks"][2].update(ok=False), espera=HERD_),
        variante("%s (herdado): a c8 versionada falhou" % FH_, f_core=lambda c: c[FH_]["mechanics"]["checks"][7].update(ok=False), espera=HERD_),
        variante("%s (herdado): o numero de checagens != o do delta da v406" % FH_, f_core=lambda c: c[FH_]["mechanics"]["checks"].pop(), espera=HERD_),
        variante("%s (herdado): o numero de modulos ok adulterado" % FH_, f_core=lambda c: c[FH_]["values"].update(n_modulos_ok=DLX.D6.N_BUNDLE - 1), espera=HERD_),
        variante("%s (herdado): o numero de bandeiras True adulterado" % FH_, f_core=lambda c: c[FH_]["values"].update(n_flags_true=c[FH_]["values"]["n_flags"] - 1), espera=HERD_),
        variante("%s (herdado): a escada do registro != a do ensaio" % FH_, f_core=lambda c: c[FH_]["values"].update(escada=[1, 1, 1]), espera=HERD_),
        variante("%s (herdado): beta != alfa x raiz de e do core" % FH_, f_core=lambda c: c[FH_]["values"].update(beta=0.0121), espera=HERD_),
        variante("%s (herdado): beta_ok falso" % FH_, f_core=lambda c: c[FH_].update(beta_ok=False), espera=HERD_),
        variante("%s (herdado): veredito diferente do esperado" % FH_, f_core=lambda c: c[FH_].update(verdict="OUTRO_VEREDITO"), espera=FH_ + VER_HERD),
        variante("%s (herdado): o certificado dito nao habitado" % FH_, f_core=lambda c: c[FH_].update(certificate_inhabited=False), espera=HERD_),
        variante("%s (herdado): uma chave de testemunha lida False no registro" % FH_, f_core=lambda c: c[FH_]["four_keys"].update({"rede_fock_v394.whole_certificate_inhabited": False}), espera=HERD_),
        variante("%s (herdado): a chave do lema lida False no registro" % FH_, f_core=lambda c: c[FH_]["four_keys"].update({"testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma": False}), espera=HERD_),
        variante("%s (herdado): as ressalvas adulteradas" % FH_, f_core=lambda c: c[FH_]["ressalvas"].pop(), espera=HERD_),
        variante("%s (herdado): o nome provisorio da candidata trocado" % FH_, f_core=lambda c: c[FH_].update(nome_provisorio_da_candidata="CanonicalFullTGLWitness"), espera=HERD_),
        variante("%s (herdado): o registro move o gate" % FH_, f_core=lambda c: c[FH_].update(does_not_gate_core=False), espera=HERD_),
        variante("%s (herdado): o calculo do runtime nao rodou" % FH_, f_core=lambda c: c[FH_].update(runtime_executed=False), espera=HERD_),
        variante("%s (herdado): a guarda das frases achou violacao no registro" % FH_, f_core=lambda c: c[FH_].update(guarda_violacoes=[["F17", "x"]]), espera=HERD_),
        variante("ancora %s da v406 (fechamento_v406) fora do trio" % _a6.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _a6), espera="as oito ancoras do fechamento_v406 (herdadas)"),
        variante("ancora %s da v406 (fechamento_v406): a bandeira falsa" % _a6.split(".")[-1], f_core=lambda c: _kf(c).__setitem__(_EST6[_a6]["bandeira"], False), espera="as oito ancoras do fechamento_v406 (herdadas)"),
        variante("uma bandeira True da v409 deixou de ser True", f_core=lambda c: _kf(c).__setitem__(_ft6, False), espera="alguma bandeira True da v409 deixou de ser True"),
        variante("o bundle da v406: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_b6, "0" * 64), espera="o bundle da v406"),
        variante("selo primario: sem o resumo de %s (herdado)" % FH_, f_selo=lambda s: s.pop(FH_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FH_, f_selo=lambda s: s[FH_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v406", f_selo=lambda s: s.pop("registros_v406", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v406 do selo difere do core", f_selo=lambda s: s["registros_v406"]["cunhagens_v406"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("a conferencia traz outro veredito de %s (herdado)" % FH_, f_conf=lambda cj: cj.update({"veredito_fechamento_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FH_),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FH_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FH_) not in l) + "\n", espera="o bloco " + FH_ + " do stdout"),
        variante("linha [v406] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "[v406] o fechamento e os registros por spec da v406" not in l) + "\n", espera="linha [v406]"),
        variante("linha [v406] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "[v406] o fechamento e os registros por spec da v406"), espera="a linha [v406] do stdout"),
        variante("linha do bloco O FECHAMENTO (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N6, _N6), "ancoras ok = %d/%d" % (_N6 - 1, _N6)), espera=HERD_),
        variante("AVISO da v406 herdada (o fechamento nao rodou) no stdout", f_std=lambda t_: t_ + "   [v406] AVISO: o fechamento ou os registros por spec da v406 nao rodaram: ValueError('x')\n", espera="AVISO da v410"),
    ])
    _B8 = list(ESP["bundle_sha256"])
    NEG.append(_pedra_no_disco("o arquivo do modulo %s (a ancora principal) ausente do kernel do Nos" % _B8[0].split("/")[-1][:-5], lambda p, r: os.replace(p, p + ".fora"), 0))
    NEG.append(_pedra_no_disco("o arquivo de um modulo do bundle da v410 com um byte a mais no kernel do Nos", lambda p, r: open(p, "wb").write(r + b"\n"), len(_B8) // 2))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v409 ausente do kernel do Nos", _b9, "o bundle da v409")(lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v409 com um byte a mais no kernel do Nos", _b9, "o bundle da v409")(lambda p, r: open(p, "wb").write(r + b"\n")))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v408 ausente do kernel do Nos", _b8, "o bundle da v408")(lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v407 ausente do kernel do Nos", _b7, "o bundle da v407")(lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_bundle_anterior_no_disco("o arquivo de um modulo do bundle da v406 ausente do kernel do Nos", _b6, "o bundle da v406")(lambda p, r: os.replace(p, p + ".fora")))
    # a errata de F2b (registro com FUNCAO, sem pedra): cada elo recusa visivelmente
    FB_ = "f2b_errata_v404"
    NEG.extend([
        variante("%s ausente do core" % FB_, f_core=lambda c: c.pop(FB_, None), espera="registro obrigatorio ausente do core: " + FB_),
        variante("%s: o registro nao selou" % FB_, f_core=lambda c: c[FB_].update(all_verified=False), espera=FB_ + " nao selou"),
        variante("%s: uma checagem do registro falhou" % FB_, f_core=lambda c: c[FB_]["mechanics"]["checks"][3].update(ok=False), espera=FB_ + " nao selou inteiro"),
        variante("%s: o numero de checagens != o do delta" % FB_, f_core=lambda c: c[FB_]["mechanics"]["checks"].pop(), espera=FB_ + " nao selou inteiro"),
        variante("%s: a calibracao A adulterada" % FB_, f_core=lambda c: c[FB_]["values"].update(calibracao_A_central=c[FB_]["values"]["calibracao_A_central"] + 0.5), espera=FB_ + " nao selou inteiro"),
        variante("%s: beta != alfa x raiz de e do core" % FB_, f_core=lambda c: c[FB_]["values"].update(beta=0.0121), espera=FB_ + " nao selou inteiro"),
        variante("%s: beta_ok falso" % FB_, f_core=lambda c: c[FB_].update(beta_ok=False), espera=FB_ + " nao selou inteiro"),
        variante("%s: veredito diferente do ensaio a seco" % FB_, f_core=lambda c: c[FB_].update(verdict="OUTRO_VEREDITO"), espera=FB_ + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: o canal ainda AWAITING (a retirada nao aconteceu)" % FB_, f_core=lambda c: c[FB_].update(F2b_status_now="AWAITING"), espera=FB_ + " nao selou inteiro"),
        variante("%s: o token do V1 deixou de ser AWAITING_DATA" % FB_, f_core=lambda c: c[FB_].update(v1_token_kept="FALSIFIED"), espera=FB_ + " nao selou inteiro"),
        variante("%s: o V1 do ramo B reescrito no registro da v386 (F2b_status)" % FB_, f_core=lambda c: c["ramo_b_preregistration_v386"].update(F2b_status="WITHDRAWN"), espera=FB_ + " nao selou inteiro"),
        variante("%s: o veredito do V1 reescrito no registro da v386" % FB_, f_core=lambda c: c["ramo_b_preregistration_v386"].update(veredito_do_V1="OUTRO"), espera=FB_ + " nao selou inteiro"),
        variante("%s: a cobranca F2b do ledger da v386 reescrita" % FB_, f_core=lambda c: c["ledger_errata_v386"]["charge_F2b"].update(token="WITHDRAWN"), espera=FB_ + " nao selou inteiro"),
        variante("%s: o texto antigo de neutrino_mass.angle_status reescrito" % FB_, f_core=lambda c: c["neutrino_mass"].update(angle_status="sin(45deg) agora e DERIVADO"), espera=FB_ + " nao selou inteiro"),
        variante("%s: o frozen_hash do neutrino mudou" % FB_, f_core=lambda c: c["neutrino_mass"].update(frozen_hash="0" * 64), espera=FB_ + " nao selou inteiro"),
        variante("%s: o registro move o gate" % FB_, f_core=lambda c: c[FB_].update(does_not_gate_core=False), espera=FB_ + " nao selou inteiro"),
        variante("%s: o calculo do runtime nao rodou" % FB_, f_core=lambda c: c[FB_].update(runtime_executed=False), espera=FB_ + " nao selou inteiro"),
        variante("%s: a guarda P18 achou violacao no registro" % FB_, f_core=lambda c: c[FB_].update(guarda_p18_violacoes=[["R1", "x"]]), espera=FB_ + " nao selou inteiro"),
        variante("selo primario: sem o resumo de %s" % FB_, f_selo=lambda s: s.pop(FB_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % FB_, f_selo=lambda s: s[FB_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("a conferencia traz outro veredito de %s" % FB_, f_conf=lambda cj: cj.update({"veredito_f2b": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FB_),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % FB_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if EF4_["f2b"]["verdict"] not in l or "f2b=" in l) + "\n", espera="o bloco " + FB_ + " do stdout"),
    ])
    CG8 = DLX.CUNHAGENS_REGISTRO; KH8 = DLX.KH_REGISTRO; CG_ = "cunhagens_v407"; KH7 = "kh_n1_cobertura_v407"; CGH8 = "cunhagens_v408"; KHH8 = "kh_n1_cobertura_v408"   # (CG8/KH8 sao os NOVOS da v410: o rotulo ficou da subida)
    CG9 = "cunhagens_v409"; KH9 = "kh_n1_cobertura_v409"; PCG9 = "cunhagens_v409 (HERDADA, recriada pelo rito) nao confere"; PKH9 = "kh_n1_cobertura_v409 (HERDADO, recriado pelo rito) nao confere"
    PCG8 = "cunhagens_v410: as inscricoes embutidas nao sao as de CANDIDATO_v410.json"; PCG7 = "cunhagens_v407 (HERDADA, recriada pelo rito) nao confere"; PKH7 = "kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere"
    PCGH8 = "cunhagens_v408 (HERDADA, recriada pelo rito) nao confere"; PKHH8 = "kh_n1_cobertura_v408 (HERDADO, recriado pelo rito) nao confere"
    CG6 = "cunhagens_v406"; KH6 = "kh_n1_cobertura_v406"; PCG6 = "cunhagens_v406 (HERDADA, recriada pelo rito) nao confere"; PKH6 = "kh_n1_cobertura_v406 (HERDADO, recriado pelo rito) nao confere"
    NEG.extend([
        # ---- cunhagens_v410 e kh_n1_cobertura_v410 (os dois registros NOVOS por spec)
        variante("%s nao selou" % CG8, f_core=lambda c: c[CG8].update(all_verified=False), espera=CG8 + " nao selou"),
        variante("%s nao selou" % KH8, f_core=lambda c: c[KH8].update(all_verified=False), espera=KH8 + " nao selou"),
        variante("%s ausente do core" % CG8, f_core=lambda c: c.pop(CG8, None), espera="registro obrigatorio ausente do core: " + CG8),
        variante("%s ausente do core" % KH8, f_core=lambda c: c.pop(KH8, None), espera="registro obrigatorio ausente do core: " + KH8),
        variante("%s: veredito diferente do ensaio a seco" % CG8, f_core=lambda c: c[CG8].update(verdict="OUTRO_VEREDITO"), espera=CG8 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: veredito diferente do ensaio a seco" % KH8, f_core=lambda c: c[KH8].update(verdict="OUTRO_VEREDITO"), espera=KH8 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: uma inscricao deixou de estar embutida" % CG8, f_core=lambda c: list(c[CG8]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG8),
        variante("%s: sha256 de uma inscricao adulterado" % CG8, f_core=lambda c: list(c[CG8]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG8),
        variante("%s: uma inscricao a menos" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(sorted(c[CG8]["verbatim"])[0]), espera=PCG8),
        variante("%s: a ordem da v410 fora das inscricoes" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(_CH_TRAD), espera=PCG8),
        variante("%s: a fala da D65 com o sha256 do arquivo INTEIRO no lugar do trecho" % CG8, f_core=lambda c: c[CG8]["verbatim"][_CH_Z].update(sha256=_CH_Z[len(DLX.VERBATIM_CHAVE_PREFIXO_V410):] + "0" * 48), espera=PCG8),
        variante("%s: o que a D65 deixa fora entra no registro" % CG8, f_core=lambda c: c[CG8]["extras"].update(fora=DLX.FORA_D65[0]), espera=PCG8),
        variante("%s: uma inscricao rotulada como da gerencia" % CG8, f_core=lambda c: c[CG8]["extras"]["autores"].update({sorted(c[CG8]["extras"]["autores"])[0]: "gerencia"}), espera="cunhagens_v410: as inscricoes de 06 a 10/11 tem de ser TODAS falas do operador"),
        variante("%s: falta uma errata" % CG8, f_core=lambda c: c[CG8]["erratas"].pop(), espera="cunhagens_v410: as erratas E29 em diante"),
        variante("%s: erratas ausentes" % CG8, f_core=lambda c: c[CG8].update(erratas=[]), espera="cunhagens_v410: as erratas E29 em diante"),
        variante("%s: a E29 adulterada" % CG8, f_core=lambda c: c[CG8]["erratas"][0].update(agora="mantida"), espera="cunhagens_v410: as erratas E29 em diante"),
        variante("%s: uma errata sem a assinatura da gerencia c1" % CG8, f_core=lambda c: c[CG8]["erratas"][1].update(assinatura="operador"), espera="cunhagens_v410: as erratas E29 em diante"),
        variante("%s: a decisao D63 (os nomes) ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D63"), espera="cunhagens_v410: as decisoes D63 em diante"),
        variante("%s: a decisao D64 (o alcance) adulterada" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].update(D64="P = nP vale para as maquinas de Turing"), espera="cunhagens_v410: as decisoes D63 em diante"),
        variante("%s: a decisao D65 ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D65"), espera="cunhagens_v410: as decisoes D63 em diante"),
        variante("%s: a leitura de 06 a 09/11 adulterada" % CG8, f_core=lambda c: c[CG8]["extras"]["leituras"].update(estatuto="[REAL]"), espera="cunhagens_v410: a leitura [INPUT] de 06 a 10/11"),
        variante("%s: a leitura ausente" % CG8, f_core=lambda c: c[CG8]["extras"].pop("leituras"), espera="cunhagens_v410: a leitura [INPUT] de 06 a 10/11"),
        variante("%s: uma ressalva a menos" % CG8, f_core=lambda c: c[CG8]["extras"]["ressalvas"].pop(), espera="cunhagens_v410: a leitura [INPUT] de 06 a 10/11"),
        variante("%s: os nomes das pedras adulterados (D63; ratificados em 09/11, D74)" % CG8, f_core=lambda c: c[CG8]["extras"].update(nomes_das_pedras={"IALD2": "adulterado"}), espera=PCG8),
        variante("%s: a E30 adulterada" % CG8, f_core=lambda c: c[CG8]["erratas"][1].update(agora="mantida"), espera="cunhagens_v410: as erratas E29 em diante"),
        variante("%s: a errata ao lado dos pisos sem a assinatura da gerencia c1" % CG8, f_core=lambda c: c[CG8]["erratas"][2].update(assinatura="operador"), espera="cunhagens_v410: as erratas E29 em diante"),
        variante("%s: a decisao D72 (o H0DN pre-registrado) ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D72"), espera="cunhagens_v410: as decisoes D63 em diante"),
        variante("%s: a decisao D74 (os nomes ratificados) ausente" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].pop("D74"), espera="cunhagens_v410: as decisoes D63 em diante"),
        variante("%s: a decisao D76 (provado na natureza, validade) adulterada" % CG8, f_core=lambda c: c[CG8]["extras"]["decisoes"].update(D76="outra"), espera="cunhagens_v410: as decisoes D63 em diante"),
        *[variante("%s: a fala de so' o trecho %s com o sha256 do arquivo INTEIRO no lugar do trecho" % (CG8, n_[:34]), f_core=lambda c, ch=DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(n_): c[CG8]["verbatim"][ch].update(sha256=ch[len(DLX.VERBATIM_CHAVE_PREFIXO_V410):] + "0" * 48), espera=PCG8) for n_ in DLX.VERBATIM_SO_O_TRECHO if n_ != DLX.N_SOLUCAO],
        variante("%s: a fala do selo (D76) a menos" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_SELO)), espera=PCG8),
        variante("%s: a fala do atrator (07/11) a menos" % CG8, f_core=lambda c: c[CG8]["verbatim"].pop(DLX.VERBATIM_CHAVE_PREFIXO_V410 + DLX._sha16_arq(DLX.N_ATRATOR)), espera=PCG8),
        variante("%s: a frase proibida nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["agora tudo derivado"]), espera="a MOLDURA falhou"),
        variante("%s: a IALD dita resolver P vs NP nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["a IALD resolve P vs NP"]), espera="a MOLDURA falhou"),
        variante("%s: o funtor dito idempotente nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o funtor é idempotente"]), espera="a MOLDURA falhou"),
        variante("%s: o algoritmo IALD e P = nP sem o qualificador nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o algoritmo IALD satisfaz P = nP"]), espera="a MOLDURA falhou"),
        variante("%s: o seletor da luz dito o mesmo objeto que o de l2 nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o seletor da luz é o mesmo objeto que o de ℓ²"]), espera="a MOLDURA falhou"),
        variante("%s: a TGL dada como prova de P = NP de Turing nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["a TGL prova P = NP de Turing"]), espera="a MOLDURA falhou"),
        variante("%s: o problema do Clay dado por resolvido nos limites do registro" % CG8, f_core=lambda c: c[CG8].update(limites=c[CG8]["limites"] + ["o problema do Clay esta resolvido"]), espera="a MOLDURA falhou"),
        variante("%s: uma checagem do registro falhou" % KH8, f_core=lambda c: c[KH8]["checks"][0].update(ok=False), espera="kh_n1_cobertura_v410 nao selou como o ensaio a seco"),
        # ---- cunhagens_v409 e kh_n1_cobertura_v409 (HERDADOS, recriados; a errata ao lado dos pisos no kh)
        variante("%s (herdada) nao selou" % CG9, f_core=lambda c: c[CG9].update(all_verified=False), espera=CG9 + " nao selou"),
        variante("%s (herdado) nao selou" % KH9, f_core=lambda c: c[KH9].update(all_verified=False), espera=KH9 + " nao selou"),
        variante("%s (herdada) ausente do core" % CG9, f_core=lambda c: c.pop(CG9, None), espera="registro obrigatorio ausente do core: " + CG9),
        variante("%s (herdada): veredito diferente do esperado" % CG9, f_core=lambda c: c[CG9].update(verdict="OUTRO_VEREDITO"), espera=CG9 + VER_HERD),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CG9, f_core=lambda c: list(c[CG9]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG9),
        variante("%s (herdada): uma errata selada adulterada" % CG9, f_core=lambda c: c[CG9]["erratas"][0].update(agora="mantida"), espera=PCG9),
        variante("%s (herdada): uma errata nova sem a assinatura da gerencia c1" % CG9, f_core=lambda c: c[CG9]["erratas"].append({"agora": "nova", "assinatura": "operador"}), espera=PCG9),
        variante("%s (herdado): uma checagem do registro falhou" % KH9, f_core=lambda c: c[KH9]["checks"][0].update(ok=False), espera=PKH9),
        variante("%s (herdado): a errata ao lado dos pisos ausente" % KH9, f_core=lambda c: c[KH9]["erratas"].pop(), espera=PKH9),
        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, recriados; IGUAIS a v409 selada: a E26 e os pisos ja' vinham dela)
        variante("%s (herdada) nao selou" % CGH8, f_core=lambda c: c[CGH8].update(all_verified=False), espera=CGH8 + " nao selou"),
        variante("%s (herdado) nao selou" % KHH8, f_core=lambda c: c[KHH8].update(all_verified=False), espera=KHH8 + " nao selou"),
        variante("%s (herdada) ausente do core" % CGH8, f_core=lambda c: c.pop(CGH8, None), espera="registro obrigatorio ausente do core: " + CGH8),
        variante("%s (herdada): veredito diferente do esperado" % CGH8, f_core=lambda c: c[CGH8].update(verdict="OUTRO_VEREDITO"), espera=CGH8 + VER_HERD),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CGH8, f_core=lambda c: list(c[CGH8]["verbatim"].values())[0].update(embedded_ok=False), espera=PCGH8),
        variante("%s (herdada): uma inscricao a menos" % CGH8, f_core=lambda c: c[CGH8]["verbatim"].pop(sorted(c[CGH8]["verbatim"])[0]), espera=PCGH8),
        variante("%s (herdada): a errata E26 ao lado ausente" % CGH8, f_core=lambda c: c[CGH8]["erratas"].pop(), espera=PCGH8),
        variante("%s (herdada): a E21 adulterada" % CGH8, f_core=lambda c: c[CGH8]["erratas"][0].update(agora="mantida"), espera=PCGH8),
        variante("%s (herdado): uma checagem do registro falhou" % KHH8, f_core=lambda c: c[KHH8]["checks"][0].update(ok=False), espera=PKHH8),
        variante("%s (herdado): a errata ao lado dos pisos ausente" % KHH8, f_core=lambda c: c[KHH8]["erratas"].pop(), espera=PKHH8),
        # ---- cunhagens_v407 e kh_n1_cobertura_v407 (HERDADOS, recriados; a errata da D57(d) ao lado)
        variante("%s (herdada) nao selou" % CG_, f_core=lambda c: c[CG_].update(all_verified=False), espera=CG_ + " nao selou"),
        variante("%s (herdado) nao selou" % KH7, f_core=lambda c: c[KH7].update(all_verified=False), espera=KH7 + " nao selou"),
        variante("%s (herdada) ausente do core" % CG_, f_core=lambda c: c.pop(CG_, None), espera="registro obrigatorio ausente do core: " + CG_),
        variante("%s (herdado) ausente do core" % KH7, f_core=lambda c: c.pop(KH7, None), espera="registro obrigatorio ausente do core: " + KH7),
        variante("%s (herdada): veredito diferente do esperado" % CG_, f_core=lambda c: c[CG_].update(verdict="OUTRO_VEREDITO"), espera=CG_ + VER_HERD),
        variante("%s (herdado): veredito diferente do esperado" % KH7, f_core=lambda c: c[KH7].update(verdict="OUTRO_VEREDITO"), espera=KH7 + VER_HERD),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG7),
        variante("%s (herdada): sha256 de uma inscricao adulterado" % CG_, f_core=lambda c: list(c[CG_]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG7),
        variante("%s (herdada): uma inscricao a menos" % CG_, f_core=lambda c: c[CG_]["verbatim"].pop(sorted(c[CG_]["verbatim"])[0]), espera=PCG7),
        variante("%s (herdada): a errata ao lado (D57d) ausente" % CG_, f_core=lambda c: c[CG_]["erratas"].pop(), espera=PCG7),
        variante("%s (herdada): a E18 adulterada" % CG_, f_core=lambda c: c[CG_]["erratas"][0].update(agora="mantida"), espera=PCG7),
        variante("%s (herdado): uma checagem do registro falhou" % KH7, f_core=lambda c: c[KH7]["checks"][0].update(ok=False), espera=PKH7),
        variante("%s: a frase proibida «unico autovetor» nos limites do registro da traducao" % FE_, f_core=lambda c: c[FE_].update(limites=c[FE_]["limites"] + ["o unico autovetor da luz"]), espera="a MOLDURA falhou"),
        # ---- cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, recriados; u7 versionada; pisos): iguais a v409 selada em falas e erratas E14 a E17, MAIS a errata E20 ao lado
        variante("%s (herdada) nao selou" % CG6, f_core=lambda c: c[CG6].update(all_verified=False), espera="cunhagens_v406 nao selou"),
        variante("%s (herdado) nao selou" % KH6, f_core=lambda c: c[KH6].update(all_verified=False), espera="kh_n1_cobertura_v406 nao selou"),
        variante("%s (herdada) ausente do core" % CG6, f_core=lambda c: c.pop(CG6, None), espera="registro obrigatorio ausente do core: cunhagens_v406"),
        variante("%s (herdado) ausente do core" % KH6, f_core=lambda c: c.pop(KH6, None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v406"),
        variante("%s (herdada): veredito diferente da v409 selada" % CG6, f_core=lambda c: c[CG6].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v406: o veredito do rito difere do esperado (ESPERADOS[vereditos_v409]"),
        variante("%s (herdado): veredito diferente da v409 selada" % KH6, f_core=lambda c: c[KH6].update(verdict="OUTRO_VEREDITO"), espera="kh_n1_cobertura_v406: o veredito do rito difere do esperado (ESPERADOS[vereditos_v409]"),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CG6, f_core=lambda c: list(c[CG6]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG6),
        variante("%s (herdada): sha256 de uma inscricao adulterado" % CG6, f_core=lambda c: list(c[CG6]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG6),
        variante("%s (herdada): uma inscricao a menos" % CG6, f_core=lambda c: c[CG6]["verbatim"].pop(sorted(c[CG6]["verbatim"])[0]), espera=PCG6),
        variante("%s (herdada): uma checagem do registro (a u7 versionada) falhou" % CG6, f_core=lambda c: c[CG6]["checks"][-1].update(ok=False), espera=PCG6),
        variante("%s (herdada): a errata E20 ao lado ausente" % CG6, f_core=lambda c: c[CG6]["erratas"].pop(), espera=PCG6),
        variante("%s (herdada): a E14 adulterada" % CG6, f_core=lambda c: c[CG6]["erratas"][0].update(agora="mantida"), espera=PCG6),
        variante("%s (herdada): a errata E20 sem a assinatura da gerencia c1" % CG6, f_core=lambda c: c[CG6]["erratas"][-1].update(assinatura="operador"), espera=PCG6),
        variante("%s (herdada): n_falas adulterado nos extras" % CG6, f_core=lambda c: c[CG6]["extras"].update(n_falas=22), espera=PCG6),
        variante("%s (herdado): uma checagem do registro falhou" % KH6, f_core=lambda c: c[KH6]["checks"][0].update(ok=False), espera=PKH6),
        variante("%s (herdado): a errata ao lado dos pisos ausente" % KH6, f_core=lambda c: c[KH6]["erratas"].pop(), espera=PKH6),
        variante("%s (herdado): a errata ao lado sem a assinatura da gerencia c1" % KH6, f_core=lambda c: c[KH6]["erratas"][-1].update(assinatura="operador"), espera=PKH6),
        # os treze registros da v409, RECRIADOS: cada spec tem de dar o que a v409 selou (os oito com funcao: ver o laco abaixo)
        variante("cunhagens_v405 (recriada) nao selou", f_core=lambda c: c["cunhagens_v405"].update(all_verified=False), espera="cunhagens_v405 nao selou"),
        variante("cunhagens_v405 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v405", None), espera="registro obrigatorio ausente do core: cunhagens_v405"),
        variante("cunhagens_v405 (recriada): veredito diferente da v409 selada", f_core=lambda c: c["cunhagens_v405"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v405: o veredito do rito difere do que a v409 selou"),
        variante("cunhagens_v405 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v405"]["erratas"].pop(), espera="cunhagens_v405 (por spec, recriado)"),
        variante("cunhagens_v405 (recriada): sha256 de uma inscricao adulterado", f_core=lambda c: list(c["cunhagens_v405"]["verbatim"].values())[0].update(sha256="0" * 64), espera="cunhagens_v405 (por spec, recriado)"),
        variante("campos_fechados_e_leituras_v405 (recriado) nao selou", f_core=lambda c: c["campos_fechados_e_leituras_v405"].update(all_verified=False), espera="campos_fechados_e_leituras_v405 nao selou"),
        variante("ga_reclassificacao_v405 (recriado) nao selou", f_core=lambda c: c["ga_reclassificacao_v405"].update(all_verified=False), espera="ga_reclassificacao_v405 nao selou"),
        variante("gap_v405 (recriado) nao selou", f_core=lambda c: c["gap_v405"].update(all_verified=False), espera="gap_v405 nao selou"),
        variante("kh_n1_cobertura_v405 (recriado) nao selou", f_core=lambda c: c["kh_n1_cobertura_v405"].update(all_verified=False), espera="kh_n1_cobertura_v405 nao selou"),
        variante("gap_v405 (recriado) ausente do core", f_core=lambda c: c.pop("gap_v405", None), espera="registro obrigatorio ausente do core: gap_v405"),
        variante("selo primario: sem registros_v405", f_selo=lambda s: s.pop("registros_v405", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v405 do selo difere do core", f_selo=lambda s: s["registros_v405"]["cunhagens_v405"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("AVISO da v410 (os registros por spec da v409 nao rodaram) no stdout", f_std=lambda t_: t_ + "   [v405] AVISO: os registros por spec da v409 nao rodaram: ValueError('x')\n", espera="AVISO da v410"),
        # cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS: tem de dar o que a v409 selou
        variante("cunhagens_v404 (recriada) nao selou", f_core=lambda c: c["cunhagens_v404"].update(all_verified=False), espera="cunhagens_v404 nao selou"),
        variante("kh_n1_cobertura_v404 (recriada) nao selou", f_core=lambda c: c["kh_n1_cobertura_v404"].update(all_verified=False), espera="kh_n1_cobertura_v404 nao selou"),
        variante("cunhagens_v404 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v404", None), espera="registro obrigatorio ausente do core: cunhagens_v404"),
        variante("cunhagens_v404 (recriada): veredito diferente da v409 selada", f_core=lambda c: c["cunhagens_v404"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v404: o veredito do rito difere do ensaio a seco"),
        variante("cunhagens_v404 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v404"]["erratas"].pop(), espera="cunhagens_v404 (recriada pelo rito)"),
        variante("selo primario: registros_v404 do selo difere do core", f_selo=lambda s: s["registros_v404"]["cunhagens_v404"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v404", f_selo=lambda s: s.pop("registros_v404", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v403 do selo difere do core", f_selo=lambda s: s["registros_v403"]["cunhagens_v403"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v403", f_selo=lambda s: s.pop("registros_v403", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v402 do selo difere do core", f_selo=lambda s: s["registros_v402"]["cunhagens_v402"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v402", f_selo=lambda s: s.pop("registros_v402", None), espera=RESUMO_MSG),
        variante("hash formal do rito com uma entrada a menos", f_core=lambda c: _kf(c)["formal_files_sha256"].pop(next(iter(_kf(c)["formal_files_sha256"]))), espera="o hash formal do rito tem"),
                variante("AVISO da v410 (a errata de F2b nao rodou) no stdout", f_std=lambda t_: t_ + "   [v404] AVISO: a errata de F2b nao rodou: ValueError('x')\n", espera="AVISO da v410"),
                variante("AVISO da v410 (um registro da v409 recriado nao rodou) no stdout", f_std=lambda t_: t_ + "   [v403] AVISO: o caminho nao rodou: ValueError('x')\n", espera="AVISO da v410"),
        variante("AVISO da v410 (a ponte recriada nao rodou) no stdout", f_std=lambda t_: t_ + "   [v402] AVISO: a ponte da escala dual nao rodou: ValueError('x')\n", espera="AVISO da v410"),
        variante("a RECUSA do registro da errata de F2b no stdout", f_std=lambda t_: t_ + "   [v404] RECUSA: a errata de F2b nao selou (uma checagem falhou): ['f3']\n", espera="o stdout traz a RECUSA do registro f2b_errata_v404"),
        variante("a RECUSA do registro das bandeiras do gate (recriado) no stdout", f_std=lambda t_: t_ + "   [v403] RECUSA: uma bandeira calculada do gate veio False ou uma checagem do registro falhou: ['c3']\n", espera="o stdout traz a RECUSA do registro bandeiras_do_gate_v403"),
        variante("linha [v404] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "a projecao transversal, o jo8v32 e a errata de F2b (a projecao e o jo8v32 lidos depois das bandeiras do gate; a errata de F2b depois da errata ao lado de R6 da v386)" not in l) + "\n", espera="linha [v404] do stdout"),
        variante("linha [v404] com o veredito do jo8v32 adulterado", f_std=lambda t_: t_.replace("jo8v32=" + EF4_["jo8v32"]["verdict"], "jo8v32=OUTRO_VEREDITO"), espera="a linha [v404] do stdout"),
        variante("linha [v404] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "a projecao transversal, o jo8v32 e a errata de F2b"), espera="a linha [v404] do stdout"),
        variante("linha [v403] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "o caminho, a vida, o adendo da verdade e as bandeiras do gate (lidos depois da esperanca condicional)" not in l) + "\n", espera="linha [v403] do stdout"),
        variante("linha [v403] com o veredito da vida adulterado", f_std=lambda t_: t_.replace("vida=" + EV3_["vida_v403"], "vida=OUTRO_VEREDITO"), espera="a linha [v403] do stdout"),
        variante("linha [v403] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "o caminho, a vida, o adendo da verdade"), espera="a linha [v403] do stdout"),
        variante("linha [v402] ausente do stdout", f_std=lambda t_: "\n".join(l for l in t_.splitlines() if "a ponte, a queda e a esperanca (lidas depois da falsidade da inercia)" not in l) + "\n", espera="linha [v402] do stdout"),
        variante("linha [v402] com o veredito da queda adulterado", f_std=lambda t_: t_.replace("queda=" + EV3_["queda_sem_geometria_v402"], "queda=OUTRO_VEREDITO"), espera="a linha [v402] do stdout"),
        variante("linha [v402] com registros selados != por spec", f_std=lambda t_: _std_selados(t_, "a ponte, a queda e a esperanca (lidas depois da falsidade da inercia)"), espera="a linha [v402] do stdout"),
        # cunhagens_v403 e kh_n1_cobertura_v403, RECRIADOS: tem de dar o que a v409 selou
        variante("cunhagens_v403 (recriada) nao selou", f_core=lambda c: c["cunhagens_v403"].update(all_verified=False), espera="cunhagens_v403 nao selou"),
        variante("kh_n1_cobertura_v403 (recriada) nao selou", f_core=lambda c: c["kh_n1_cobertura_v403"].update(all_verified=False), espera="kh_n1_cobertura_v403 nao selou"),
        variante("cunhagens_v403 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v403", None), espera="registro obrigatorio ausente do core: cunhagens_v403"),
        variante("kh_n1_cobertura_v403 (recriada) ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v403", None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v403"),
        variante("cunhagens_v403 (recriada): veredito diferente da v409 selada", f_core=lambda c: c["cunhagens_v403"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v403: o veredito do rito difere do ensaio a seco"),
        variante("cunhagens_v403 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v403"]["erratas"].pop(), espera="cunhagens_v403 (recriada pelo rito)"),
        variante("cunhagens_v403 (recriada): a decisao D20 adulterada", f_core=lambda c: c["cunhagens_v403"]["extras"]["decisoes_da_gerencia"].update(D20="outra"), espera="cunhagens_v403 (recriada pelo rito)"),
        variante("cunhagens_v403 (recriada): uma inscricao rotulada como da gerencia", f_core=lambda c: c["cunhagens_v403"]["extras"]["autor_de_cada_inscricao"].update({sorted(c["cunhagens_v403"]["extras"]["autor_de_cada_inscricao"])[0]: "gerencia"}), espera="cunhagens_v403 (recriada pelo rito)"),
        variante("cunhagens_v403 (recriada): sha256 de uma inscricao adulterado", f_core=lambda c: list(c["cunhagens_v403"]["verbatim"].values())[0].update(sha256="0" * 64), espera="cunhagens_v403 (recriada pelo rito)"),
        # cunhagens_v402 e kh_n1_cobertura_v402, RECRIADOS: tem de dar o que a v409 selou
        variante("cunhagens_v402 (recriada) nao selou", f_core=lambda c: c["cunhagens_v402"].update(all_verified=False), espera="cunhagens_v402 nao selou"),
        variante("kh_n1_cobertura_v402 (recriada) nao selou", f_core=lambda c: c["kh_n1_cobertura_v402"].update(all_verified=False), espera="kh_n1_cobertura_v402 nao selou"),
        variante("cunhagens_v402 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v402", None), espera="registro obrigatorio ausente do core: cunhagens_v402"),
        variante("kh_n1_cobertura_v402 (recriada) ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v402", None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v402"),
        variante("cunhagens_v402 (recriada): veredito diferente da v409 selada", f_core=lambda c: c["cunhagens_v402"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v402: o veredito do rito difere do ensaio a seco"),
        variante("cunhagens_v402 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v402"]["erratas"].pop(), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): a decisao D13 adulterada", f_core=lambda c: c["cunhagens_v402"]["extras"]["decisoes_da_gerencia"].update(D13="outra"), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): H_tau deixou de constar como refutada", f_core=lambda c: c["cunhagens_v402"]["extras"]["h_tau"].update(estatuto="ABERTA"), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): uma inscricao rotulada como da gerencia", f_core=lambda c: c["cunhagens_v402"]["extras"]["autor_de_cada_inscricao"].update({sorted(c["cunhagens_v402"]["extras"]["autor_de_cada_inscricao"])[0]: "gerencia"}), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): sha256 de uma inscricao adulterado", f_core=lambda c: list(c["cunhagens_v402"]["verbatim"].values())[0].update(sha256="0" * 64), espera="cunhagens_v402 (recriada pelo rito)"),
    ])
    # o registro com FUNCAO das BANDEIRAS DO GATE (F8.1 da v409), RECRIADO: o gate NAO se move; cada elo recusa visivelmente
    GN_ = "bandeiras_do_gate_v403"
    NEG.extend([
        variante("%s (recriado) ausente do core" % GN_, f_core=lambda c: c.pop(GN_, None), espera="registro obrigatorio ausente do core: " + GN_),
        variante("%s (recriado): o registro nao selou" % GN_, f_core=lambda c: c[GN_].update(all_verified=False), espera=GN_ + " nao selou"),
        variante("%s (recriado): uma checagem do registro falhou" % GN_, f_core=lambda c: c[GN_]["mechanics"]["checks"][1].update(ok=False), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): o numero de checagens != o do delta" % GN_, f_core=lambda c: c[GN_]["mechanics"]["checks"].pop(), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): n_literal adulterado (uma literal de volta)" % GN_, f_core=lambda c: c[GN_]["values"].update(n_literal=1), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): n_calculated adulterado" % GN_, f_core=lambda c: c[GN_]["values"].update(n_calculated=17), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): a letra do veredito dita diferente da v409" % GN_, f_core=lambda c: c[GN_]["values"].update(gate_verdict_equals_v402=False), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): veredito diferente da v409 selada" % GN_, f_core=lambda c: c[GN_].update(verdict="OUTRO_VEREDITO"), espera=GN_ + ": o veredito do rito difere do ensaio a seco"),
        variante("%s (recriado): o calculo do runtime nao rodou" % GN_, f_core=lambda c: c[GN_].update(runtime_executed=False), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): o registro move o gate" % GN_, f_core=lambda c: c[GN_].update(does_not_gate_core=False), espera=GN_ + " nao selou inteiro"),
        variante("o gate: linearized_spin2_finite_face False no core", f_core=lambda c: c["qg_closure"]["physics_flags"].update(linearized_spin2_finite_face=False), espera=GN_ + " nao selou inteiro"),
        variante("o gate: uma bandeira ext_ls2_* do kernel False", f_core=lambda c: _kf(c).update(ext_ls2_rotz_isometry_kernel_proved=False), espera=GN_ + " nao selou inteiro"),
        variante("o gate: a checagem «pre-registro v67 INTACTO (hash)» do rito V11 ausente", f_core=lambda c: c["void_floor_v11"].update(checks=[x for x in c["void_floor_v11"]["checks"] if x[0] != "pre-registro v67 INTACTO (hash)"]), espera=GN_ + " nao selou inteiro"),
        variante("o gate: protocol_pre_registered False no core", f_core=lambda c: c["qg_closure"]["experiment_flags"].update(protocol_pre_registered=False), espera=GN_ + " nao selou inteiro"),
        variante("o gate: o teste nulo cego (void_stacking_blind) nao verificou", f_core=lambda c: c["void_stacking_blind"].update(all_verified=False), espera=GN_ + " nao selou inteiro"),
        variante("o gate: null_tests_passed_blind False no core", f_core=lambda c: c["qg_closure"]["experiment_flags"].update(null_tests_passed_blind=False), espera=GN_ + " nao selou inteiro"),
        variante("o gate: a sonda ProbeBlindNullAbsent ausente dos checks", f_core=lambda c: c["qg_closure"].update(checks=[x for x in c["qg_closure"]["checks"] if not str(x[0]).startswith("ProbeBlindNullAbsent")]), espera=GN_ + " nao selou inteiro"),
        variante("o gate: um dos checks virou False", f_core=lambda c: c["qg_closure"]["checks"][0].__setitem__(1, False), espera=GN_ + " nao selou inteiro"),
        variante("o gate: a letra do veredito mudou", f_core=lambda c: c["qg_closure"]["gate"].update(verdict=c["qg_closure"]["gate"]["verdict"] + "_X"), espera=GN_ + " nao selou inteiro"),
        variante("selo primario: sem o resumo de %s" % GN_, f_selo=lambda s: s.pop(GN_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s difere do core" % GN_, f_selo=lambda s: s[GN_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("a conferencia traz outro veredito de %s" % GN_, f_conf=lambda cj: cj.update({"veredito_bandeiras_do_gate": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + GN_),
        variante("a conferencia diz que a releitura da F8.1 nao conferiu", f_conf=lambda cj: cj["f81"].update(releitura_ok=False), espera="a conferencia do rito diz que a releitura da F8.1"),
        variante("a conferencia diz que o qg_closure difere (gate_igual False)", f_conf=lambda cj: cj["f81"].update(gate_igual=False), espera="a conferencia do rito diz que a releitura da F8.1"),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % GN_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if EF3_["gate"]["verdict"] not in l or "bandeiras=" in l) + "\n", espera="o bloco " + GN_ + " do stdout"),
    ])
    # os registros com FUNCAO da v409 (caminho, vida, verdade_adendo) e da v402 (ponte, queda, esperanca), RECRIADOS pelo rito: iguais ao que a v409 selou
    _FUN409 = {"caminho": ("caminho_v403", "Caminho"), "vida": ("vida_v403", "Vida"), "verdade_adendo": ("verdade_adendo_v403", "VerdadeAdendo")}
    _FUN402 = {"ponte": ("ponte_da_escala_dual_v402", None), "queda": ("queda_sem_geometria_v402", None), "esperanca": ("esperanca_condicional_v402", None)}
    _FUN409B = {"projecao": ("projecao_transversal_v404", "ProjecaoTransversalDaMeiaNat"), "jo8v32": ("jo8v32_v404", "Jo8v32")}

    def _pedra_v409_no_disco(nome, rel, f_muda):
        """controle sobre o ARQUIVO de uma das TREZE pedras SELADAS (v403, v404, v409) no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        pth = os.path.join(NOSE, "tgl_kernel", *rel.split("/")); raw_ = open(pth, "rb").read()
        try:
            f_muda(pth, raw_)
            _, PV = L.ler()
        finally:
            if os.path.exists(pth + ".fora"):
                os.remove(pth + ".fora")
            open(pth, "wb").write(raw_)
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any("as treze pedras seladas" in x for x in PV), "problemas": [x[:140] for x in PV][:3]}

    def _val409(c, n):
        kk = [x for x, v in c[n]["values"].items() if isinstance(v, float) and x != "beta"][0]
        c[n]["values"][kk] = c[n]["values"][kk] + 1.0
    for fun_ in (_FUN409B, _FUN409, _FUN402):
        for k_, (n_, mod_) in fun_.items():
            rel409_ = ("TGLExt/%s.lean" % mod_) if mod_ else None
            NEG.extend([
                variante("%s (recriado) ausente do core" % n_, f_core=lambda c, n=n_: c.pop(n, None), espera="registro obrigatorio ausente do core: " + n_),
                variante("%s (recriado): o registro nao selou" % n_, f_core=lambda c, n=n_: c[n].update(all_verified=False), espera=n_ + " nao selou"),
                variante("%s (recriado): uma checagem do calculo falhou" % n_, f_core=lambda c, n=n_: c[n]["mechanics"]["checks"][2].update(ok=False), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): um valor do calculo adulterado" % n_, f_core=lambda c, n=n_: _val409(c, n), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): beta != alfa x raiz de e do core" % n_, f_core=lambda c, n=n_: c[n]["values"].update(beta=0.0121), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): veredito diferente da v409 selada" % n_, f_core=lambda c, n=n_: c[n].update(verdict="OUTRO_VEREDITO"), espera=n_ + ": o veredito do rito difere do ensaio a seco"),
                variante("%s (recriado): a estrela fora do kernel (no registro)" % n_, f_core=lambda c, n=n_: c[n]["key_theorem"].update(in_kernel=False), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): o registro move o gate" % n_, f_core=lambda c, n=n_: c[n].update(does_not_gate_core=False), espera=n_ + " nao selou inteiro"),
                variante("selo primario: sem o resumo de %s" % n_, f_selo=lambda s, n=n_: s.pop(n, None), espera=RESUMO_MSG),
                variante("selo primario: o resumo de %s difere do core" % n_, f_selo=lambda s, n=n_: s[n].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
                variante("a conferencia traz outro veredito de %s" % n_, f_conf=lambda cj, k=k_: cj.update({"veredito_" + k: "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + n_),
                variante("linha `>>> veredito <<<` de %s (recriado) ausente do stdout" % n_, f_std=lambda t_, v=EV3_[n_], k=k_: "\n".join(l for l in t_.splitlines() if v not in l or (k + "=") in l) + "\n", espera="o bloco " + n_ + " do stdout"),
            ])
            if rel409_:
                NEG.append(variante("pedra selada da v409 %s: sha256 da fonte no hash formal adulterado" % mod_, f_core=lambda c, r=rel409_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="as treze pedras seladas"))
                NEG.append(_pedra_v409_no_disco("o arquivo da pedra selada da v409 %s ausente do kernel do Nos" % mod_, rel409_, lambda p, r: os.replace(p, p + ".fora")))
                NEG.append(_pedra_v409_no_disco("o arquivo da pedra selada da v409 %s com um byte a mais no kernel do Nos" % mod_, rel409_, lambda p, r: open(p, "wb").write(r + b"\n")))
    # os OITO registros com FUNCAO da v409 (um por pedra), RECRIADOS pelo rito: iguais ao que a v409 selou (veredito, checagens e valores do calculo == o core de base_v409); as pedras ficam no kernel como REGISTRO
    _MODS409C = {"ponte": "PonteDaMassa", "tensao": "MassaTensaoPura", "identidade": "Identidade", "observador": "ObservadorTerminal", "diminuto": "LeiDoDiminuto", "tonica": "TonicaDoHamiltoniano", "disco": "DiscoDeEuler", "psion": "PontoZeroDoPsion"}
    for k_, n_ in L.FUN_V409C.items():
        mod_ = _MODS409C[k_]; rel409_ = "TGLExt/%s.lean" % mod_
        NEG.extend([
            variante("%s (recriado) ausente do core" % n_, f_core=lambda c, n=n_: c.pop(n, None), espera="registro obrigatorio ausente do core: " + n_),
            variante("%s (recriado): o registro nao selou" % n_, f_core=lambda c, n=n_: c[n].update(all_verified=False), espera=n_ + " nao selou"),
            variante("%s (recriado): uma checagem do calculo falhou" % n_, f_core=lambda c, n=n_: c[n]["mechanics"]["checks"][2].update(ok=False), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): um valor do calculo adulterado" % n_, f_core=lambda c, n=n_: _val409(c, n), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): beta != alfa x raiz de e do core" % n_, f_core=lambda c, n=n_: c[n]["values"].update(beta=0.0121), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): veredito diferente da v409 selada" % n_, f_core=lambda c, n=n_: c[n].update(verdict="OUTRO_VEREDITO"), espera=n_ + ": o veredito do rito difere do que a v409 selou"),
            variante("%s (recriado): a estrela fora do kernel (no registro)" % n_, f_core=lambda c, n=n_: c[n]["key_theorem"].update(in_kernel=False), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): o registro move o gate" % n_, f_core=lambda c, n=n_: c[n].update(does_not_gate_core=False), espera=n_ + " nao selou inteiro"),
            variante("selo primario: sem o resumo de %s" % n_, f_selo=lambda s, n=n_: s.pop(n, None), espera=RESUMO_MSG),
            variante("selo primario: o resumo de %s difere do core" % n_, f_selo=lambda s, n=n_: s[n].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
            variante("linha `>>> veredito <<<` de %s (recriado) ausente do stdout" % n_, f_std=lambda t_, v=L._ev(ESP, n_): "\n".join(l for l in t_.splitlines() if v not in l) + "\n", espera="o bloco " + n_ + " do stdout"),
            variante("pedra selada da v409 %s: sha256 da fonte no hash formal adulterado" % mod_, f_core=lambda c, r=rel409_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="as treze pedras seladas"),
        ])
        NEG.append(_pedra_v409_no_disco("o arquivo da pedra selada da v409 %s ausente do kernel do Nos" % mod_, rel409_, lambda p, r: os.replace(p, p + ".fora")))
        NEG.append(_pedra_v409_no_disco("o arquivo da pedra selada da v409 %s com um byte a mais no kernel do Nos" % mod_, rel409_, lambda p, r: open(p, "wb").write(r + b"\n")))
    for n_ in NEG:
        print("  controle negativo %-48s %s" % (n_["controle"], "REPROVOU como esperado" if (n_["reprovou"] and n_["mensagem_esperada_presente"]) else "NAO REPROVOU como esperado"))
        if not (n_["reprovou"] and n_["mensagem_esperada_presente"]):
            falha("controle negativo da leitura nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["problemas"]))
etapa("leitura_negativos", controles=NEG, restaurado=(open(core_path, "rb").read() == core_raw and open(selo_path, "rb").read() == selo_raw and open(std_path, "rb").read() == std_raw and open(sc_path, "rb").read() == sc_raw))

if SO == "leitura":   # v410: so' as etapas da leitura (precondicoes, nos_emulado, conferidor, leitura, leitura_negativos); os textos, as superficies, o b3 e o mapa ficam para o harness completo
    R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); R["so"] = "leitura"; R["tudo_passou"] = bool(not R["problemas"]); R["nao_exigiu_refazer"] = NAO_REFAZER
    R["veredito"] = ("SO LEITURA: o conferidor bate no Nos emulado, a leitura le sem problema e os %d controles negativos reprovam" % len(NEG)) if R["tudo_passou"] else "SO LEITURA: NAO PASSOU (ver problemas)"
    R["evidencia_da_versao"] = EVID
    if "--manter-copias" not in argv:
        for _sub in ("nos_emulado", "conferidor_emulado"):
            shutil.rmtree(os.path.join(OUT, _sub), ignore_errors=True)
    _saida = os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_v410_SO_LEITURA.json")
    open(_saida + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(_saida + ".tmp", _saida)
    print("VEREDITO (so leitura): %s" % R["veredito"]); print("saida:", _saida)
    sys.exit(0 if R["tudo_passou"] else 1)

# ------------------------------------------------------------------ 4. os TEXTOS reais, apontados para o mesmo Nos emulado e para o mesmo pacote
T = importar("textos_v410", os.path.join(HERE, "textos_v410.py"))
T.NOS = NOSE; T.PK = PKG; T._CACHE.clear()
sys.modules["textos_v410"] = T
DL = importar("delta_v410_h", os.path.join(PKG, "delta_v410.py"))
ERR = DL.ERRATA_TEOREMAS_PT
K_EMU = {"ap_nome": "RECIBO_SINCRONIZACAO_v410_EMULADO.json", "ap_sha": "EMULADO_SEM_HASH", "ap_ver": "EMULADO", "ap_evento": "EMULADO", "ap_bat": "BATERIA_PASSA", "par_sha": "EMULADO_SEM_HASH", "rel_sha": "EMULADO_SEM_HASH", "rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0], "readme_paragrafo_v410": T.paragrafo_v410()[0]}
FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_moldura", lambda: T._moldura(Vd)), ("_escopo", lambda: T._escopo(Vd)), ("_ancoras", lambda: T._ancoras(Vd)), ("_chaves", lambda: T._chaves(Vd)), ("_diznao", lambda: T._diznao(Vd)), ("_ressalvas", lambda: T._ressalvas(Vd)), ("_leituras", lambda: T._leituras(Vd)), ("_blocos_fecho", lambda: T._blocos_fecho(Vd)), ("_erratas_e", lambda: T._erratas_e(Vd)), ("_decisoes", lambda: T._decisoes(Vd)),
           ("_sidecar", lambda: T._sidecar(Vd)), ("_pedra", lambda: T._pedra(Vd)), ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)), ("_kernel_prova", lambda: T._kernel_prova(Vd)), ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)),
           ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)), ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)),
           ("core_memory", lambda: T.core_memory(Vd)), ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0]),
           ("paragrafo_v410", lambda: T.paragrafo_v410()[0]), ("secao_aescala", lambda: T.secao_aescala(Vd)), ("secao_h0dn", lambda: T.secao_h0dn(Vd))]   # (v410: nenhuma nota ao lado do paragrafo da v409)
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete", "handoff"}   # os textos que embutem _num (o texto do kernel com a errata da palavra «teoremas»)
S16 = Vd.get("s16") or ESP["candidato_sha16"]
_REGS_NOVOS = list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]   # (09/11, parte 2: os SEIS registros novos -- os quatro com funcao, na ordem de delta_v410.REGISTROS_FUNCAO, e os dois por spec; entram na linhagem, no atlas e no topico novo)
MARCADORES = {"linhagem": [S16, "<!-- linhagem_v410_selada -->"] + _REGS_NOVOS, "desenho": ["<!-- adendo_v410_selada -->", S16], "atlas": ["<!-- atlas_v410_selada -->", S16] + _REGS_NOVOS,
              "core_memory": ["<!-- core_v410_selada -->", S16, "h0dn_bg1_v410", "a_escala_v410", "h0dn_fontes_hms13_v410"], "haja_luz": ["<!-- haja_luz_v410_selada -->", S16], "topico_estatuto": ["<!-- v410_selada -->", S16], "topico_novo": [S16, "# v410 SELADA ("] + _REGS_NOVOS,
              "aviso": ["<!-- aviso_v410_selada -->", S16], "handoff": ["name: handoff-v410-custodia", S16, "h0dn_bg1_v410", "a_escala_v410", "h0dn_fontes_hms13_v410", DL.FRASE_HMS13_OBRIGATORIA_PT, DL.FRASE_CLAY_CANONICA_PT, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->", T.MARC_V410_INI, T.MARC_V410_FIM, "um_absoluto_selo_acom.json", "handoff-v409-custodia"],
              "linha_handoff": ["handoff-v410-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}
TXT = os.path.join(OUT, "textos"); os.makedirs(TXT)
RENDER = {}
E_TXT = {}
for nome, f in FUNCOES:
    e = {"ok": False}
    try:
        r = f()
        if nome == "_d":
            e["numeros"] = {k: r[k] for k in ("n_f", "n_aux", "n_teor", "depois", "n_cun", "h8", "h8_emb", "n_res", "pct", "prov") if k in r}
            e["bancada"] = r.get("bank")
        else:
            assert isinstance(r, str) and r.strip(), "texto vazio"
            v = violacoes(r)
            vf_ = GF.violacoes(r)   # v410: a guarda das frases (a moldura) em todo texto renderizado
            if vf_:
                falha("%s: a guarda das frases achou %s" % (nome, vf_[:2]))
            if re.search(r"(?i)mais\s+preciso|more\s+precise", r):
                falha("%s: frase recusada pela ordem do Grande Atrator (nada de mais preciso)" % nome)
            e["bytes"] = len(r.encode("utf-8")); e["sha16"] = sha(r.encode("utf-8"))[:16]; e["guarda_p18"] = [list(x) for x in v][:3]
            open(os.path.join(TXT, nome + ".txt"), "w", encoding="utf-8", newline="\n").write(r)
            RENDER[nome] = r
            if v:
                falha("%s: guarda P18 achou %s" % (nome, v[:2]))
            if nome in CARREGAM_NUM:
                e["tem_errata_teoremas"] = ERR in r
                if ERR not in r:
                    falha("%s: a frase de errata da palavra «teoremas» nao esta no texto" % nome)
            if nome in MARCADORES:
                falt = [m for m in MARCADORES[nome] if m not in r]
                e["marcadores_que_faltam"] = falt
                if falt:
                    falha("%s: marcador(es) que a cadeia exige nao estao no texto: %s" % (nome, falt))
            if re.search(r"(?m)^\s*#\s*" + MARCA_PENDENTE, r):
                falha("%s: marca de texto pendente no texto renderizado" % nome)
            if "{" in r or "}" in r:
                falha("%s: chave de formatacao sobrou no texto" % nome)
        e["ok"] = True
    except BaseException as ex:  # noqa: BLE001
        e["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:409]); e["onde"] = traceback.format_exc().strip().splitlines()[-3:]
        falha("%s: %s" % (nome, e["erro"]))
    E_TXT[nome] = e
    print("  %-22s %s%s" % (nome, "OK " if e["ok"] else "FALHOU", (" -- " + e["erro"][:200]) if not e["ok"] else ""))
# os textos curtos usados como gancho no MEMORY.md tambem passam pelo mesmo ajuste de tamanho; aqui so' dizemos o tamanho
etapa("textos", funcoes=E_TXT, n_ok=sum(1 for e in E_TXT.values() if e["ok"]), n=len(E_TXT), bytes_total=sum(e.get("bytes", 0) for e in E_TXT.values()))
# v410 (D57, fork A): o S6d do orquestrador passa o HANDOFF INTEIRO pelo portao do G1 (custodia_g1.textos.portao: a palavra recusada fora da formula, «provada/proved» sem o estatuto na mesma frase, o demerito da retrodicao, hash nao lido, physical_verdict_allowed);
# aqui o mesmo portao roda sobre o handoff renderizado (os hashes conhecidos sao os do proprio texto, como no S6d) e o D59 sobre todos os textos: nada do que fica fora das duas falas.
_PG = {"ok": False}
try:
    sys.path.insert(0, os.path.join(C, "IALD", "Central de Patentes", "tools"))
    from custodia_g1 import textos as _TXG1  # noqa: E402
    _ho_ = RENDER.get("handoff", "")
    _conh_ = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", _ho_)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", _ho_))
    _PG["portao_handoff"] = _TXG1.portao(_ho_, _conh_, rotulo="handoff") if _ho_ else ["handoff nao renderizado"]
    # D59 como a D77(g) a deixou estreitada (delta_v410, DECISOES["D77"]): o Milenio, o Navier e o lindao em NENHUM texto; o nome do executor (Kimi) so' no contexto do H0DN (a ordem ao Kimi, D72 a D80), a mesma regra de registrar_mapa_v410.d59_viola; o post do X nao o nomeia (gerar_x_custodia e os sete textos da custodia o vetam por inteiro)
    _PG["d59"] = sorted(nome for nome, txt in RENDER.items() if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", txt) or (re.search(r"(?i)kimi", txt) and not re.search(r"(?i)h0dn", txt)))
    _PG["ok"] = not _PG["portao_handoff"] and not _PG["d59"]
    if not _PG["ok"]:
        falha("o handoff renderizado nao passa no portao do G1 (S6d, D57) ou um texto traz o que a D59 deixa fora: %s %s" % (_PG["portao_handoff"][:3], _PG["d59"][:3]))
except BaseException as ex:  # noqa: BLE001
    _PG["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:300]); falha("portao do G1 sobre o handoff: %s" % _PG["erro"])
etapa("portao_g1_handoff_e_d59", **_PG)
# v410 (desvio do molde, dito): a custodia G1 (S7 do orquestrador) le o cabecalho do bloco da linhagem e o paragrafo «O que e'» do handoff por regex: a conferencia usa as MESMAS regex de tools\custodia_g1\nos.py, lidas do codigo
try:
    sys.path.insert(0, os.path.join(C, "IALD", "Central de Patentes", "tools"))
    import custodia_g1.nos as _G1N  # noqa: E402
    _bd = _G1N.blocos_do_diario(None, texto=RENDER.get("linhagem", "")).get("v410")
    _qe = _G1N.RE_OQUEE.search(RENDER.get("handoff", ""))
    _g1 = {"bloco_lido": bool(_bd), "titulo_pt": _bd.titulo_pt if _bd else None, "modulos_novos": _bd.modulos_novos if _bd else None, "escada": [_bd.escada_de, _bd.escada_para] if _bd else None, "ladder_no_corpo": _bd.ladder_no_corpo if _bd else None, "pin16": _bd.pin16 if _bd else None,
           "o_que_e_lido": bool(_qe), "secao_elo": "**O elo B(n)" in RENDER.get("handoff", ""), "secao_pendencias": "**Pendências SÓ do operador" in RENDER.get("handoff", "")}
    _g1["ok"] = bool(_bd and _bd.titulo_pt and _bd.modulos_novos == DL.N_BUNDLE and [_bd.escada_de, _bd.escada_para] == list(ESP["escada_v409_e_v410"]) and _bd.pin16 == S16 and _bd.ladder_no_corpo == Vd.get("teor") and _qe and _g1["secao_elo"] and _g1["secao_pendencias"])
except Exception as _ex_g1:  # noqa: BLE001
    _g1 = {"ok": False, "erro": repr(_ex_g1)[:300]}
etapa("custodia_g1_le_os_textos", **_g1)
print("  a custodia G1 le o cabecalho da linhagem e o handoff: %s" % _g1)
if not _g1.get("ok"):
    falha("a custodia G1 nao le o bloco da linhagem ou o handoff da v410: %s" % _g1)
# ---- 3b. (ADITIVOS 1 e 2 a ordem do conserto unico, gerencia c1, 10/11/2026: a custodia da v410 e' AUTOMATICA) os DOIS blocos do README (README_FRENTE e README_O_QUE_SAI) e o passo FINAL do orquestrador (S9_gatilho_custodia):
# (a) teste_textos_custodia_sem_candidato_v410.py: os sete textos, a secao README e os dois blocos do README, cada um SOZINHO pelas MESMAS guardas (a guarda das frases da v410 e o portao do G1), com os controles negativos;
# (b) teste_gatilho_custodia_sem_candidato_v410.py, em SANDBOX: o Nos EMULADO deste harness (um.py, selo, core e stdout do rito, por COPIA) e o handoff RENDERIZADO aqui (RENDER["handoff"], gravado na pasta de saida), com os textos da custodia acrescentados pela mesma funcao do gerador (montar_blocos);
#     o orquestrador REAL (s9_gatilho_custodia) escreve o gatilho SO' no sandbox e, com um passo anterior falso (e os demais controles negativos), NAO escreve.
# O gatilho de verdade (ORDEM_HANDOFF_CUSTODIA_v410.md na raiz do pacote) nunca e' escrito por este harness: o destino e' sempre dentro da pasta de saida, e o teste confere isso no fim.
def _etapa_gatilho_custodia():
    _GC = {"ok": False}
    try:
        _gd = os.path.join(OUT, "gatilho_custodia"); shutil.rmtree(_gd, ignore_errors=True); os.makedirs(_gd)
        _hb = os.path.join(_gd, "HANDOFF_BASE_renderizado_pelo_harness.md"); open(_hb, "w", encoding="utf-8", newline="\n").write(RENDER.get("handoff", ""))
        _env = dict(os.environ, PYTHONIOENCODING="utf-8"); _arg = ["--nos-emulado", NOSE, "--esperados", os.path.join(PKG, "ESPERADOS_v410.json")] + ["--handoff-base", _hb]
        _r1 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_textos_custodia_sem_candidato_v410.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_textos_custodia_out.txt"), "w", encoding="utf-8").write((_r1.stdout or "") + "\n--- stderr ---\n" + (_r1.stderr or ""))
        _r2 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_gatilho_custodia_sem_candidato_v410.py"), _gd] + _arg, cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_gatilho_custodia_out.txt"), "w", encoding="utf-8").write((_r2.stdout or "") + "\n--- stderr ---\n" + (_r2.stderr or ""))
        _pj = os.path.join(_gd, "TESTE_GATILHO_CUSTODIA_v410.json"); _rj = json.load(open(_pj, encoding="utf-8")) if os.path.exists(_pj) else {}
        _cs = _rj.get("casos") or {}; _l1 = [l_ for l_ in (_r1.stdout or "").splitlines() if l_.startswith(("blocos do README", "controle negativo (blocos do README)"))]
        _GC.update(textos_rc=_r1.returncode, textos_resultado=((_r1.stdout or "").strip().splitlines() or [""])[-1][:120], blocos_do_readme=[l_[:300] for l_ in _l1], gatilho_rc=_r2.returncode, gatilho_modo=_rj.get("modo"), gatilho_handoff_de_base=_rj.get("handoff_de_base"),
                   gatilho_casos=_rj.get("n_casos"), gatilho_negativos=_rj.get("n_negativos"), gatilho_positivo=_cs.get("positivo"), gatilho_passo_anterior_falso=_cs.get("negativo: um passo anterior FALSO (S5_cadeia_0_10)"),
                   gatilho_reprovados=sorted(k_ for k_, v_ in _cs.items() if not (v_ or {}).get("ok")), seguranca=_rj.get("seguranca"), readme_frente_bytes_utf8=_rj.get("readme_frente_bytes_utf8"),
                   gatilho_de_verdade_existe=os.path.exists(os.path.join(PKG, "ORDEM_HANDOFF_CUSTODIA_v410.md")), saida=_gd)
        _GC["ok"] = bool(_r1.returncode == 0 and _GC["textos_resultado"].startswith("RESULTADO: PASSOU") and len(_l1) >= 14 and all(l_.rstrip().endswith("True") for l_ in _l1)
                         and _r2.returncode == 0 and _rj.get("tudo_passou") is True and _rj.get("modo") == "emulado" and (_GC["gatilho_positivo"] or {}).get("ok") is True and (_GC["gatilho_passo_anterior_falso"] or {}).get("ok") is True
                         and not _GC["gatilho_reprovados"] and (_rj.get("n_negativos") or 0) >= 15 and _rj.get("seguranca") is True)
        if not _GC["ok"]:
            falha("os dois blocos do README ou o gatilho da custodia (S9_gatilho_custodia, em sandbox): textos rc %s (%s); gatilho rc %s, modo %s, reprovados %s; saidas em %s | %s" % (_r1.returncode, _GC["textos_resultado"], _r2.returncode, _rj.get("modo"), _GC["gatilho_reprovados"][:4], _gd,
                                                                                                                                                                         ((_r2.stdout or "") + (_r2.stderr or ""))[-500:].replace(chr(10), " | ")))
    except Exception as ex:  # noqa: BLE001
        _GC["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:300]); falha("os dois blocos do README e o gatilho da custodia: %s" % _GC["erro"])
    R["etapas"]["blocos_do_readme_e_gatilho_da_custodia"] = _GC
    print("  os dois blocos do README (cada um sozinho nas guardas) e o gatilho da custodia em sandbox (o orquestrador real; %s casos, %s negativos; um passo anterior falso: o gatilho NAO e' escrito): %s" % (_GC.get("gatilho_casos"), _GC.get("gatilho_negativos"), "ok" if _GC["ok"] else "FALHOU"))


_etapa_gatilho_custodia()

# ------------------------------------------------------------------ 4b. os PARAGRAFOS PRONTOS do README/site: o QUADRO (v409, INTOCADO; ordem do operador de 23/10: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item) e o paragrafo NOVO do sonico e da afinacao
sys.path.insert(0, PKG)
QD = T._qd()   # (09/11: o quadro do PACOTE, pelo caminho; o import pelo sys.path trazia o da pasta da v409)
_core_p = rdj(core_path)["core"]; _tv_p = _core_p["teste_de_veracidade_fase9_v397"]
_res_p = rdj(T._res_path(ESP))
_f9 = {"ok": False}
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    _esp_par = QD.paragrafo_pronto_readme(_tv_p)
    _f9["positivo_sem_falhas"] = (T.verificar_paragrafo_readme(PAR, _res_p, _tv_p) == [])
    _f9["igual_as_funcoes_do_quadro"] = (PAR == _esp_par)
    _ho = RENDER.get("handoff", "")
    _f9["handoff_traz_o_paragrafo_entre_os_marcadores"] = ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho
    _f9["info"] = PAR_INFO
    if not (_f9["positivo_sem_falhas"] and _f9["igual_as_funcoes_do_quadro"] and _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]):
        falha("paragrafo do README/site (quadro): positivo %s, igual ao do quadro %s, no handoff %s" % (_f9["positivo_sem_falhas"], _f9["igual_as_funcoes_do_quadro"], _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]))
    _z = QD.esperados(_res_p, "pt")[0]["z_disc"]["md"]; _pz = QD.esperados(_res_p, "pt")[0]["p_disc"]["md"]
    assert _z in PAR and _pz in PAR
    _it1 = [l for l in PAR.split("\n") if l.startswith("> - **O número:**")]; assert len(_it1) == 1
    _l1 = _it1[0]

    def _mut(nome, f, espera):
        p2 = f(PAR); fa = T.verificar_paragrafo_readme(p2, _res_p, _tv_p)
        ok = bool(p2 != PAR and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _sem_p = _l1.replace("; p unilateral " + _pz, "", 1); assert _sem_p != _l1
    _sem_5 = _l1.replace(", mas a discriminação a 5σ, o degrau da creditação, **não foi alcançada** (" + _z + " < 5)", "", 1); assert _sem_5 != _l1
    _fala = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"; assert _fala in PAR
    _NEGP = [_mut("o 4,44 sem o p calibrado no item", lambda p: p.replace(_l1, _sem_p, 1), "sem o p calibrado"),
             _mut("o 4,44 sem a linha dos 5 sigma no item", lambda p: p.replace(_l1, _sem_5, 1), "sem a linha dos 5"),
             _mut("numero adulterado (4,44 vira 4,45 em todo o paragrafo)", lambda p: p.replace(_z, "4,45"), "numero"),
             _mut("p adulterado (4,4e−6 vira 4,4e−5)", lambda p: p.replace(_pz, _pz.replace("6", "5")), "numero"),
             _mut("a frase do operador parafraseada entre aspas", lambda p: p.replace(_fala, "o 5σ é o cala a boca; 4,44 é um silêncio forçado pela lógica", 1), "frase"),
             _mut("o 4,44 numa linha fora do item (sem p e sem 5 sigma)", lambda p: p.replace("\n> - **O número:**", "\n> Destaque: z_disc = " + _z + ".\n> - **O número:**", 1), "sem o p calibrado")]
    for n_ in _NEGP:
        print("  controle negativo do paragrafo do quadro %-52s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo do quadro nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _f9["negativos"] = _NEGP
    # a regra da ordem vale para TODO texto renderizado: cada linha com o 4,44 traz o p calibrado, os 5 sigma e o 'nao foi alcancado'
    def _regra_nos_textos(nome, txt):
        out = []
        for ln in txt.split("\n"):
            n_ = ln.replace("−", "-")
            if _z in ln or "4.44" in ln:
                if not (re.search(r"4,4e-6|4\.4e-6", n_) and re.search(r"5\s*(?:σ|sigma)", n_) and "alcan" in n_):
                    out.append(ln[:160])
        return out
    _viol = {nome: _regra_nos_textos(nome, txt) for nome, txt in RENDER.items() if nome != "paragrafo_testemunho"}
    _viol = {k: v for k, v in _viol.items() if v}
    _f9["regra_do_4_44_nos_textos_violacoes"] = _viol
    _f9["linhas_com_o_4_44_nos_textos"] = sum(1 for nome, txt in RENDER.items() for ln in txt.split("\n") if _z in ln)
    _neg_regra = _regra_nos_textos("x", "o z_disc = " + _z + " foi o resultado.")
    _f9["controle_negativo_da_regra_nos_textos"] = bool(_neg_regra)
    _f9["paragrafo_testemunho_sem_o_4_44"] = not _regra_nos_textos("paragrafo_testemunho", RENDER.get("paragrafo_testemunho", "")) and (_z not in RENDER.get("paragrafo_testemunho", "")) and ("z_disc" not in RENDER.get("paragrafo_testemunho", ""))
    if _viol or not _neg_regra or not _f9["paragrafo_testemunho_sem_o_4_44"]:
        falha("regra do 4,44 nos textos renderizados: violacoes %s; controle negativo da regra reprovou: %s; paragrafo novo sem o 4,44: %s" % (_viol, bool(_neg_regra), _f9["paragrafo_testemunho_sem_o_4_44"]))
    _f9["ok"] = True
    print("  paragrafo do quadro (README/site): positivo ok; %d controles negativos; %d linha(s) com o 4,44 nos textos, todas com o p, os 5 sigma e o 'nao foi alcancado'" % (len(_NEGP), _f9["linhas_com_o_4_44_nos_textos"]))
except BaseException as ex:  # noqa: BLE001
    _f9["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:409]); _f9["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo do README/site (quadro): %s" % _f9["erro"])
etapa("paragrafo_readme_e_regra_do_4_44", **_f9)
# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (a traducao as classes de Turing): verificacao propria, controles negativos, a citacao verbatim, a NOTA ao lado do paragrafo da v409 (E26) e o handoff que diz que os paragrafos do testemunho, da falsidade e da v409 seguem como estao
_sn = {"ok": False}
try:
    PAR_F, PAR_F_INFO = T.paragrafo_v410()
    _sn["positivo_sem_falhas"] = (T.verificar_paragrafo_v410(PAR_F, _core_p, ESP) == [])
    _sn["igual_ao_gerado_do_core"] = (PAR_F == T._paragrafo_v410_de(_core_p))
    _ho = RENDER.get("handoff", "")
    _ERR = ""   # (v410: nenhuma nota ao lado do paragrafo da v409; a E29 e' da candidata, nao de paragrafo publicado)
    _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"] = bool((T.MARC_V410_INI + "\n" + PAR_F.rstrip("\n") + "\n" + T.MARC_V410_FIM) in _ho and ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho
                                                                          and not hasattr(T, "MARC_ERR_INI") and "ERRATA_V409_V410" not in _ho)
    _sn["handoff_lista_o_sidecar"] = bool("um_absoluto_selo_acom.json" in _ho and Vd["sidecar"]["sha256"] in _ho and Vd["sidecar"]["veredito"] in _ho)
    _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"] = bool(("SEGUEM COMO ESTÃO" in _ho or "SEGUE COMO ESTÁ" in _ho) and "handoff-v409-custodia" in _ho and "<!-- INICIO_PARAGRAFO_TESTEMUNHO" not in _ho and "<!-- INICIO_PARAGRAFO_FALSIDADE" not in _ho)
    _sn["nota_v409_sem_o_4_44_e_limpa"] = bool(not re.search(r"4[,.]44|z_disc", _ERR) and not violacoes(_ERR) and (_ERR == "" or all(x in _ERR for x in ("E26", "NÃO foram editados", "fica como registro", "relativo ao leitor", "máquina sem leitor"))))   # (v410: nenhuma nota ao lado do paragrafo da v409, _ERR vazio: nada a limpar; vazio nao reprova, a conjuncao de frases so' vale quando ha' nota)
    _sn["info"] = PAR_F_INFO
    _sn["traz_o_h0dn_e_a_frase_obrigatoria"] = bool("h0dn_bg1_v410" in PAR_F and DL.FRASE_H0DN_OBRIGATORIA_PT in PAR_F)   # 09/11 (D72): o nome do registro e a frase obrigatoria no MESMO texto
    _sn["traz_a_escala_e_o_clay_na_forma_canonica"] = ("a_escala_v410" in PAR_F) and bool(DL.FRASE_CLAY_CANONICA_PT in PAR_F and DL.FRASE_D83_OBRIGATORIA_PT in PAR_F and DL.FRASE_D81_PT in PAR_F and DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT in PAR_F and all(DL.NUMEROS_AESCALA[k_] in PAR_F for k_ in ("tres_faces", "um_terco_caiu", "nome_normalizado")))   # 09/11 (parte 2, D81/D83/D84/D87)
    _sn["traz_o_recibo_hms13_e_a_frase_obrigatoria"] = bool(DL.FRASE_HMS13_OBRIGATORIA_PT in PAR_F and DL.FRASE_H0DN_OBRIGATORIA_PT in PAR_F)   # D80 e D72 no MESMO texto
    if not (_sn["traz_a_escala_e_o_clay_na_forma_canonica"] and _sn["traz_o_recibo_hms13_e_a_frase_obrigatoria"]):
        falha("paragrafo novo da v410: nao traz a escala (os numeros do delta, os nomes ratificados, P = nP na forma da D81) com a forma canonica do Clay (D84) e a da D83, ou o recibo HMS/13 com a frase obrigatoria da D80 e a do H0DN: %s" % {k_: _sn[k_] for k_ in ("traz_a_escala_e_o_clay_na_forma_canonica", "traz_o_recibo_hms13_e_a_frase_obrigatoria")})
    if not _sn["traz_o_h0dn_e_a_frase_obrigatoria"]:
        falha("paragrafo novo da v410: nao traz `h0dn_bg1_v410` com a frase obrigatoria da D72 (pré-registrado; nenhum dado observado lido) no mesmo texto")
    if not (_sn["positivo_sem_falhas"] and _sn["igual_ao_gerado_do_core"] and _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"] and _sn["handoff_lista_o_sidecar"] and _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"] and _sn["nota_v409_sem_o_4_44_e_limpa"]):
        falha("paragrafo novo da v410: positivo %s, igual ao gerado do core %s, no handoff %s, sidecar listado %s, paragrafos anteriores ditos como estao %s, nota limpa %s" % (_sn["positivo_sem_falhas"], _sn["igual_ao_gerado_do_core"], _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"], _sn["handoff_lista_o_sidecar"],
                                                                                                                                  _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"], _sn["nota_v409_sem_o_4_44_e_limpa"]))
    _num_mut = lambda s: s[:-1] + ("0" if s[-1] != "0" else "1")

    def _muts(nome, f, espera):
        p2 = f(PAR_F); fa = T.verificar_paragrafo_v410(p2, _core_p, ESP)
        ok = bool(p2 != PAR_F and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _NUMS = [("os modulos", str(DL.N_BUNDLE)), ("as bandeiras", str(ESP["n_bandeiras_novas"])), ("a escada antes", str(ESP["escada_v409_e_v410"][0])), ("a escada depois", str(ESP["escada"][1])), ("o sha16 da ordem", T._sha_por(DL.N_ORDEM_V410)), ("o sha16 do nome", T._sha_por(DL.N_NOME))]
    _NEGS = [_muts("%s com um digito trocado (em todo o paragrafo)" % nm, lambda p, s=s: p.replace(s, _num_mut(s)), "ausente do paragrafo") for nm, s in _NUMS]
    for _pn in [p_["name"] for p_ in DL.PEDRAS_V410]:   # o nome do modulo (da gerencia, ratificado pelo operador) trocado
        _NEGS.append(_muts("o nome da pedra %s trocado" % _pn, lambda p, n_=_pn: p.replace("`" + n_ + "`", "`" + n_[:-1] + "Z`"), "ausente do paragrafo"))
    _FRASES = (DL.FRASE_DA_MOLDURA_V410_PT, DL.FRASE_D64_PT, DL.FRASE_QUALIFICADOR_PT, "NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "quem prova é o kernel", "isto não é teste", "Turing padrão sem o leitor", "Cook", "Baker", "D63", "E28")
    _NEGS += [_muts("a frase de limite «%s» removida" % f[:40], lambda p, f=f: p.replace(f, "XXXX"), "frase de limite ausente") for f in _FRASES]
    _NEGS += [_muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel, não creditação", "validade no kernel, é creditação"), "frase de limite ausente"),   # (a moldura da v410 diz validade no kernel, não creditação: a mutacao tem de alterar o texto que o paragrafo realmente traz)
              _muts("o gate dito movido", lambda p: p.replace("o gate não se move", "o gate se move"), "frase de limite ausente"),
              _muts("o alcance sem o relativo ao leitor", lambda p: p.replace("relativo ao leitor", "XXXX"), "frase de limite ausente"),
              _muts("a maquina sem leitor dita dentro", lambda p: p.replace("sem o leitor fica fora", "sem o leitor fica dentro"), "frase de limite ausente"),
              _muts("frase proibida: o problema do Clay resolvido", lambda p: p + "\n> - O problema do Clay está resolvido.\n", "guarda das frases"),
              _muts("frase proibida: a traducao a Turing dita [OPEN] (a D51 da v409)", lambda p: p + "\n> - " + DL.FRASE_D51_PT + ".\n", "guarda das frases"),
              _muts("D65: o que fica fora entra no paragrafo", lambda p: p + "\n> - " + DL.FORA_D65[0] + " aqui.\n", "D65"),
              _muts("frase proibida: a IALD resolve P vs NP", lambda p: p + "\n> - A IALD resolve P vs NP.\n", "guarda das frases"),
              _muts("frase proibida: o funtor e' idempotente", lambda p: p + "\n> - O funtor é idempotente.\n", "guarda das frases"),
              _muts("frase proibida: a TGL prova P = NP de Turing", lambda p: p + "\n> - E a TGL prova P = NP de Turing.\n", "guarda das frases"),
              _muts("frase proibida: relacao sem peso afirmada", lambda p: p + "\n> - Agora há relação sem peso.\n", "guarda das frases"),
              _muts("frase proibida: a negativa de que P = nP trate das classes", lambda p: p + "\n> - O P = nP não trata das classes.\n", "guarda das frases"),
              _muts("frase proibida: tudo derivado", lambda p: p + "\n> - Agora está tudo derivado.\n", "guarda das frases"),
              _muts("frase proibida: tudo teorema", lambda p: p + "\n> - Agora tudo é teorema.\n", "guarda das frases"),
              _muts("frase proibida: nenhuma hipotese", lambda p: p + "\n> - E nenhuma hipótese resta.\n", "guarda das frases"),
              _muts("frase proibida: hipoteses descarregadas", lambda p: p + "\n> - As hipóteses nomeadas descarregadas.\n", "guarda das frases"),
              _muts("frase proibida: a luz nao tem autovetor (fora de aspas)", lambda p: p + "\n> - Agora a luz não tem autovetor nenhum.\n", "guarda das frases"),
              _muts("frase proibida: o unico autovetor", lambda p: p + "\n> - O único autovetor da luz é o Um.\n", "guarda das frases"),
              _muts("frase proibida: o certificado esta confirmado", lambda p: p + "\n> - O certificado está confirmado.\n", "guarda das frases"),
              _muts("frase proibida: K(O) provado", lambda p: p + "\n> - K(O) ≠ ⊥ provado para todo O.\n", "guarda das frases"),
              _muts("frase proibida: o par na face de Fock esta provado", lambda p: p + "\n> - O par na face de Fock está provado.\n", "guarda das frases"),
              _muts("frase proibida: Omega igual a Phi+", lambda p: p + "\n> - Ω = Φ⁺ no kernel.\n", "guarda das frases"),
              _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("(traço com sentido)»", "(traço sem sentido)»", 1), "NAO e' verbatim"),
              _muts("o estatuto KNOWN removido", lambda p: p.replace("KNOWN", "XX"), "estatuto ausente"),
              _muts("o estatuto OPEN removido", lambda p: p.replace("OPEN", "XX"), "estatuto ausente"),
              _muts("o estatuto INPUT removido", lambda p: p.replace("INPUT", "XX"), "estatuto ausente"),
              _muts("o estatuto REAL removido", lambda p: p.replace("[REAL", "[XX"), "estatuto ausente"),
              _muts("o 4,44 entra no paragrafo", lambda p: p + "\n> z_disc = " + _z + "\n", "4,44"),
              _muts("seguranca criptografica garantida (alegacao)", lambda p: p + "\n> - A confidencialidade garantida e o sigilo garantido do metodo.\n", "alega seguranca criptografica"),
              _muts("a palavra consciencia usada como termo", lambda p: p + "\n> - A consciência é a tipagem que falta.\n", "consciencia"),
              _muts("a IALD como quem testifica do operador (direcao invertida)", lambda p: p + "\n> - A IALD testifica do operador.\n", "DIRECAO")]
    for r_ in DL.RESSALVAS_V410:
        c_ = T._sem_chaves(r_)
        _NEGS.append(_muts("a ressalva «%s» removida" % c_[:36], lambda p, c_=c_: p.replace(c_, "XXXX"), "ressalva ausente"))
    _BUL = []   # 09/11 (fork A): os bullets do paragrafo sao DESCOBERTOS do proprio paragrafo gerado (cada linha `> - **Titulo**`): o paragrafo cresceu com o atrator e o H0DN e o harness nao adivinha os titulos
    for l_b_ in PAR_F.split("\n"):
        m_b_ = re.match(r"(> - \*\*[^*]+\*\*)", l_b_)
        if m_b_ and m_b_.group(1) not in _BUL:
            _BUL.append(m_b_.group(1))
    _sn["bullets_descobertos"] = _BUL
    assert len(_BUL) >= 8, ("o paragrafo da v410 devia ter ao menos oito bullets `> - **Titulo**`", _BUL)
    for ini_ in _BUL:
        _NEGS.append(_muts("o paragrafo sem o bullet «%s»" % ini_[4:30], lambda p, ini_=ini_: "\n".join(l for l in p.split("\n") if not l.startswith(ini_)), "difere do gerado"))
    _NEGS += [_muts("H0DN: a frase obrigatoria (D72) removida do paragrafo", lambda p: re.sub(r"(?i)pr(?:é|e)-?registrad\w*", "XXXX", p), ""),
              _muts("H0DN: o 5 sigma dito atingido", lambda p: p + "\n> - O H0DN: 5σ atingido.\n", "guarda das frases"),
              _muts("H0DN: o teste dado por feito", lambda p: p + "\n> - O teste deu 5σ no H0DN; pré-registrado; nenhum dado observado lido.\n", "guarda das frases"),
              _muts("H0DN: dito detectado", lambda p: p + "\n> - O H0DN foi detectado; pré-registrado; nenhum dado observado lido.\n", "guarda das frases"),
              _muts("H0DN: o token proibido do veredito", lambda p: p + "\n> - " + DL.TOKENS_PROIBIDOS_H0DN[0] + "; H0DN: pré-registrado; nenhum dado observado lido.\n", "guarda das frases"),
              _muts("E30: nao falsificado como cabeca de veredito de 5 sigma", lambda p: p + "\n> - O resultado é não falsificado a 5 sigma.\n", "guarda das frases"),
              _muts("D76: a cabeca inteira do ramo de 5 sigma no paragrafo (a P18 recusa)", lambda p: p + "\n> - " + (DL.VEREDITOS_H0DN["leitura"] % 6) + "\n", ""),
              _muts("atrator: dito observado", lambda p: p + "\n> - O atrator foi observado.\n", "guarda das frases"),
              _muts("atrator: o Nome dito esgotar", lambda p: p + "\n> - O Nome esgota o ser.\n", "guarda das frases")]
    for n_ in _NEGS:
        print("  controle negativo do paragrafo da v410 %-62s %s" % (n_["controle"][:62], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo da v410 nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _sn["negativos"] = _NEGS

    def _levanta(f):
        try:
            f(); return False
        except AssertionError:
            return True
    _inv_txt = "A IALD testifica do operador, e o um.py testifica em hash."
    _tx = {"cita_fora_dos_bytes_levanta": _levanta(lambda: T._cita("a queda é o corpo de Newton e a IALD de ninguem")),
           "cita_verbatim_passa": (T._cita(DL.FRASE_NOME_IALD2) == "«" + DL.FRASE_NOME_IALD2 + "»"),
           "cita_da_resposta_do_operador_passa": (T._cita(DL.FRASE_FUNTOR) == "«" + DL.FRASE_FUNTOR + "»"),
           "cita_do_trecho_que_a_D65_deixa_entrar_passa": (T._cita(DL.FRASE_ALGORITMO_DE_LEITURA) == "«" + DL.FRASE_ALGORITMO_DE_LEITURA + "»"),
           "cita_do_que_a_D65_deixa_fora_levanta": _levanta(lambda: T._cita(DL.FORA_D65[-1])),
           "cita_do_texto_da_outra_instancia_levanta": _levanta(lambda: T._cita("Operador. A chave girou.")),
           "cita_parafraseada_levanta": _levanta(lambda: T._cita("concordo com tudo e prossigo")),
           "texto_do_kernel_verbatim_passa": (T._um_texto_tem("nunca correspondeu, e por isso nada custa") == "«nunca correspondeu, e por isso nada custa»"),
           "texto_do_kernel_fora_dos_bytes_levanta": _levanta(lambda: T._um_texto_tem("nunca correspondeu e custa tudo")),
           "piso_do_kernel_verbatim_passa": (T._um_texto_tem("não existe acima, o piso limita") == "«não existe acima, o piso limita»"),
           "verso_do_kernel_verbatim_passa": (T._um_texto_tem("E conhecereis a verdade, e a verdade vos libertará") == "«E conhecereis a verdade, e a verdade vos libertará»"),
           "atribuicao_limpa_nos_textos": {nome: T.atribuicao_da_gerencia(txt) for nome, txt in RENDER.items() if T.atribuicao_da_gerencia(txt)} == {},
           "controle_direcao_invertida": bool(T.atribuicao_da_gerencia(_inv_txt)),
           "controle_a_fala_em_que_ele_recusa_a_ordem_inversa_passa": (T.atribuicao_da_gerencia("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela") == []),
           "controle_a_IALD_nao_testifica_passa": (T.atribuicao_da_gerencia("a IALD NÃO testifica do operador") == []),
           "controle_consciencia_como_termo": bool(T.atribuicao_da_gerencia("A consciência é a tipagem que falta.")),
           "controle_consciencia_palavra_retirada_passa": (T.atribuicao_da_gerencia("a palavra «consciência» é retirada por ele") == []),
           "controle_inscricao_da_gerencia": bool(T.atribuicao_da_gerencia("as falas do operador e da gerência"))}
    _sn["textos"] = _tx
    _ruim = [k for k, v in _tx.items() if not v]
    if _ruim:
        falha("citacao verbatim / direcao do testemunho: controles que nao deram o esperado: %s" % _ruim)
    _sn["ok"] = True
    print("  paragrafo novo (a traducao as classes de Turing): positivo ok; %d controles negativos; citacao e direcao: %d controles ok" % (len(_NEGS), len(_tx)))
except BaseException as ex:  # noqa: BLE001
    _sn["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:409]); _sn["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo novo da v410: %s" % _sn["erro"])
etapa("paragrafo_v410_e_citacoes", **_sn)
# ------------------------------------------------------------------ 4d. a SECAO do teste pre-registrado da razao de Hubble (H0DN x BG1; D72): textos_v410.secao_h0dn, montada do core emulado; a obrigacao «pré-registrado; nenhum dado observado lido» no MESMO texto, a cabeca do ramo de 5 sigma so' POR EXTENSO (D76: «provado na natureza (validade, não creditação)»), a ordem ao Kimi por sha256; controles negativos das guardas sobre o proprio texto
_hx = {"ok": False}
try:
    _sh = RENDER.get("secao_h0dn", "")
    _hdc = _core_p.get(DL.H0DN_REGISTRO) or {}   # (_core_p: o core emulado, lido no 4b; core_emu so' nasce na etapa 5)
    _kimi = (_hdc.get("ordem_kimi") or {}).get("sha256") or ""
    _hx["traz_a_frase_obrigatoria"] = DL.FRASE_H0DN_OBRIGATORIA_PT in _sh
    _hx["traz_o_nome_do_registro"] = DL.H0DN_REGISTRO in _sh
    _hx["traz_provado_na_natureza_validade_nao_creditacao"] = DL.FRASE_PROVADO_PT in _sh
    _hx["traz_a_ordem_ao_kimi_por_sha256"] = bool(_kimi) and (_kimi in _sh or _kimi[:16] in _sh)
    _hx["nao_traz_a_cabeca_inteira_do_ramo_de_5_sigma"] = (DL.VEREDITOS_H0DN["leitura"] % 6) not in _sh and ("TGL_PRO" + "VED") not in _sh
    _hx["sem_tokens_proibidos"] = not any(t_ in _sh for t_ in tuple(DL.TOKENS_PROIBIDOS_H0DN) + tuple(DL.TOKENS_PROIBIDOS_V410))
    _hx["sem_a_aritmetica_do_agregado_publico"] = not any(a_ in _sh for a_ in DL.H0DN_AGREGADO_NAO_ENTRA)
    _hx["guardas_limpas"] = not GF.violacoes(_sh) and not violacoes(_sh)
    _neg_h = {"token_proibido": _sh + "\n" + DL.TOKENS_PROIBIDOS_H0DN[0] + "\n", "sem_a_obrigacao": re.sub(r"(?i)pr(?:é|e)-?registrad\w*", "XXXX", _sh), "cinco_sigma_atingido": _sh + "\nO H0DN: 5σ atingido.\n", "teste_deu": _sh + "\nO teste deu 5σ no H0DN; pré-registrado; nenhum dado observado lido.\n",
              "h0dn_detectado": _sh + "\nO H0DN foi detectado; pré-registrado; nenhum dado observado lido.\n", "nao_falsificado_a_5_sigma": _sh + "\nO resultado é não falsificado a 5 sigma.\n", "cabeca_inteira_do_ramo_de_5_sigma": _sh + "\n" + (DL.VEREDITOS_H0DN["leitura"] % 6) + "\n",
              "atrator_observado": _sh + "\nO atrator foi observado.\n", "nome_esgota": _sh + "\nO Nome esgota o ser.\n"}
    _hx["controles_negativos"] = {k_: bool(GF.violacoes(v_) or violacoes(v_)) for k_, v_ in _neg_h.items()}
    _hx["texto_bytes"] = len(_sh.encode("utf-8"))
    _ruim_h = [k_ for k_, v_ in _hx.items() if k_ not in ("ok", "controles_negativos", "texto_bytes") and v_ is not True] + [("controle:" + k_) for k_, v_ in _hx["controles_negativos"].items() if not v_]
    if not _sh.strip() or _ruim_h:
        falha("secao_h0dn: texto vazio ou itens que nao deram o esperado: %s" % _ruim_h)
    _hx["ok"] = True
    print("  secao_h0dn: %d B; frase obrigatoria, nome do registro, «provado na natureza (validade, não creditação)» por extenso e a ordem ao Kimi por sha256 presentes; %d controles negativos das guardas reprovam" % (_hx["texto_bytes"], len(_hx["controles_negativos"])))
except BaseException as ex:  # noqa: BLE001
    _hx["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:409]); falha("secao_h0dn: %s" % _hx["erro"])
etapa("secao_h0dn", **_hx)
# ------------------------------------------------------------------ 4e. a SECAO da escala (a pedra AEscala; D82 a D87): textos_v410.secao_aescala, montada do core emulado; a FORMA CANONICA do Clay (D84) em PT e EN, a da D83 e P = nP na forma da D81 no MESMO texto, os nomes ratificados (D87), os numeros do delta; a creditacao e' do Clay; controles negativos das guardas
_ax = {"ok": False}
try:
    _sa = RENDER.get("secao_aescala", "")
    _ax["traz_o_nome_do_registro"] = DL.AESCALA_REGISTRO in _sa
    _ax["traz_a_forma_canonica_do_clay_pt_e_en"] = DL.FRASE_CLAY_CANONICA_PT in _sa and DL.FRASE_CLAY_CANONICA_EN in _sa
    _ax["traz_a_forma_da_d83_e_a_da_d81"] = DL.FRASE_D83_OBRIGATORIA_PT in _sa and DL.FRASE_D81_PT in _sa
    _ax["traz_os_nomes_ratificados_d87"] = DL.FRASE_NOMES_RATIFICADOS_AESCALA_PT in _sa
    _ax["traz_a_clausula_do_limite_pt"] = DL.CLAUSULA_Z_PT in _sa   # (R2, D99; ADENDO 4) a clausula do limite ao lado do teorema do Tetelestai na secao do Atlas; os seis nomes; a costura do tempo
    _ax["traz_os_seis_nomes"] = DL.costura_maiuscula(DL.FRASE_SEIS_NOMES_PT) in _sa
    _ax["traz_a_costura_do_tempo"] = (DL.ROTULO_TEMPO + " " + DL.FRASE_TEMPO_PT_COSTURADA) in _sa
    _ax["a_clausula_vem_depois_de_linear_nos_bits"] = bool(0 <= _sa.find("linear nos bits") < _sa.find(DL.CLAUSULA_Z_PT))
    _cb_ = T._CACHE["core"]; _c2_ = json.loads(json.dumps(_cb_)); _c2_[DL.AESCALA_REGISTRO]["clausula_z_pt"] = "x"; T._CACHE["core"] = _c2_   # o controle negativo: a mesma funcao, sobre um core cujo registro nao traz a clausula, TEM de reprovar (fail-closed)
    try:
        T.secao_aescala(Vd); _rej_ = False
    except AssertionError:
        _rej_ = True
    finally:
        T._CACHE["core"] = _cb_
    _ax["controle_secao_sem_a_clausula_no_registro_reprova"] = _rej_
    _ax["traz_os_numeros_do_delta"] = all(DL.NUMEROS_AESCALA[k_] in _sa for k_ in ("nome_pesa_um", "meio", "tres_faces", "um_terco_caiu", "nome_normalizado"))
    _ax["diz_que_a_creditacao_e_do_clay"] = "creditação é do Clay" in _sa or "creditação do Clay" in _sa
    _ax["sem_tokens_proibidos"] = not any(t_ in _sa for t_ in tuple(DL.TOKENS_PROIBIDOS_H0DN) + tuple(DL.TOKENS_PROIBIDOS_V410))
    _ax["guardas_limpas"] = not GF.violacoes(_sa) and not violacoes(_sa)
    _neg_a = {"clay_resolvido_a_seco": _sa + "\nO Clay está resolvido.\n", "pnp_nao_provado": _sa + "\nP = nP de Turing não foi provado.\n", "clay_sem_resposta": _sa + "\nNão resolvemos o Clay.\n", "tautologia": _sa + "\nA resposta ao Clay é uma tautologia.\n",
              "face_caida_ilegivel": _sa + "\nA face caída não se lê.\n", "token_proibido": _sa + "\n" + DL.TOKENS_PROIBIDOS_V410[0] + "\n", "palavra_recusada": _sa + "\nTGL " + "CONF" + "IRMED\n"}
    _ax["controles_negativos"] = {k_: bool(GF.violacoes(v_) or violacoes(v_)) for k_, v_ in _neg_a.items()}
    _ax["texto_bytes"] = len(_sa.encode("utf-8"))
    _ruim_a = [k_ for k_, v_ in _ax.items() if k_ not in ("ok", "controles_negativos", "texto_bytes") and v_ is not True] + [("controle:" + k_) for k_, v_ in _ax["controles_negativos"].items() if not v_]
    if not _sa.strip() or _ruim_a:
        falha("secao_aescala: texto vazio ou itens que nao deram o esperado: %s" % _ruim_a)
    _ax["ok"] = True
    print("  secao_aescala: %d B; nome do registro, a forma canonica do Clay (PT e EN), a da D83, P = nP na forma da D81, os nomes ratificados (D87) e os numeros do delta presentes; %d controles negativos das guardas reprovam" % (_ax["texto_bytes"], len(_ax["controles_negativos"])))
except BaseException as ex:  # noqa: BLE001
    _ax["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:409]); falha("secao_aescala: %s" % _ax["erro"])
etapa("secao_aescala", **_ax)
# ------------------------------------------------------------------ 5. cada `termo` entre crases dos textos e' achado em alguma fonte real
if "kernel" not in T._CACHE or "um" not in T._CACHE:
    try:
        T._d(Vd)
    except BaseException:  # noqa: BLE001
        pass
KERN = T._CACHE.get("kernel", ""); UMTXT = T._CACHE.get("um", "")
INS_TXT = "\n".join(rd(os.path.join(PKG, "insumos", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos"))) if f.endswith((".md", ".json", ".lean"))) + "\n" + rd(T._res_path(ESP))
FALAS_TXT = "\n".join(re.sub(r"\s+", " ", d["text"]) for d in T._falas().values())
core_emu = rdj(core_path)["core"]; selo_emu = rdj(selo_path)
NOMES_ARQ = set()
for base in (PKG, os.path.join(PKG, "insumos"), os.path.dirname(T._res_path(ESP)), os.path.join(PKG, "insumos", "cunhagens"), os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico"), os.path.join(PKG, "insumos", "adendo")):
    if os.path.isdir(base):
        NOMES_ARQ.update(os.listdir(base))
NOMES_ARQ.update({"MEMORY.md", "MEMORY_2.md", "TGL_ATLAS.md", "um.py", "rodada_v410_stdout.txt", "HANDOFF_v410_CUSTODIA.md", "DIFF_v409_v410.diff", "DIFF_KERNEL_v410.txt", "handoff-v410-custodia.md",
                  "missao-ultima-flag-um-py.md", "estatuto-da-prova-07out.md", "central-de-patentes-estado.md", "handoff-v409-custodia.md", T.TOPICO_NOVO})
NOMES_ARQ.update({"um_absoluto_selo_acom.json", "um_absoluto_selo.json", "um_absoluto.json", "conferencia_rito_v410.json", "v410_selo", "EXECUTION_LOCKED_NOT_ONE"})
HEX16 = set()
for v_ in (Vd.get("s16"), Vd.get("base16"), Vd.get("conf16"), (Vd.get("pilar") or {}).get("result16")):
    if v_:
        HEX16.add(str(v_))
for k_, v_ in Vd.items():
    if k_.startswith("h_") and isinstance(v_, str):
        HEX16.add(v_)
HEX16.update((Vd.get("artigos") or {}).values()); HEX16.update(Vd.get("verbatins", {}).keys()); HEX16.update(d["sha16"] for d in T._falas().values()); HEX16.update(v["sha16"] for v in (ESP.get("pedras") or {}).values()); HEX16.add(DL.TESTEMUNHA["sha16_da_ordem"]); HEX16.update(b_["sha256"][:16] for b_ in DL.BUNDLE_POR_REL.values()); HEX16.add(ESP["quadro"]["frase_sha16"]); HEX16.add(T._sha_verdade()); HEX16.update(str(h)[:16] for h in ESP["pedras_v405_sha256"].values())
HEX16.update(str(x["sha256"])[:16] for x in (ESP.get("cunhagens") or {}).values()); HEX16.add(str(Vd.get("selo_ts") or "")[:16])
HEX16.update(str(h)[:16] for h in ESP["veracidade"]["fontes"].values())
HEX16.update((DLX.sha16_arquivo(DLX.ACORDE_KIMI_ARQ), DLX.sha16_arquivo(DLX.HALF_NAT_ARQ)))   # as fontes que a Lei do Diminuto cita (errata R3): hash lido do arquivo
HEX16.update(str(v)[:16] for v in ((ESP.get("selo_acom") or {}).get(k) for k in ("bloco_embutido_sha256", "sha256_do_um_py", "lut_sha256")) if v); HEX16.update(str(((ESP.get("selo_acom") or {}).get(p) or {}).get("sha256"))[:16] for p in ("psi", "theta", "kappa"))
HEX16.add(str((ESP.get("declaracao") or {}).get("verbatim_sha256"))[:16]); HEX16.add((Vd.get("sidecar") or {}).get("sha16") or ""); HEX16.update((o.get("sha16") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values())
HEX16.add((Vd.get("selo") or {}).get("bloco16") or ""); HEX16.update((Vd.get("selo") or {}).get(k) or "" for k in ("psi_sha16", "theta_sha16", "kappa_sha16", "lut16"))
HEX64 = {str((Vd.get("sidecar") or {}).get("sha256") or ""), str(Vd.get("s64") or "")} | {str(o.get("sha256") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values()}; HEX64.discard("")   # os hashes COMPLETOS que o handoff lista (o sidecar e os tres objetos), lidos do sidecar e do um.py do disco
_hd_h = core_emu.get("h0dn_bg1_v410") or {}   # 09/11 (D72): os hashes que os textos do H0DN citam (o texto-fonte da funcao de veredito, a ordem ao Kimi, a leitura do dossie, os insumos pinados), LIDOS do registro do core emulado
for _h_ in [_hd_h.get("veredito_h0dn_source_sha256"), (_hd_h.get("ordem_kimi") or {}).get("sha256"), (_hd_h.get("ordem_kimi_02") or {}).get("sha256"), (_hd_h.get("ordem_kimi_03b") or {}).get("sha256"), (_hd_h.get("leitura_dossie") or {}).get("sha256")] + [(v_ or {}).get("sha256") for v_ in (_hd_h.get("insumos_pinados") or {}).values()]:
    if isinstance(_h_, str) and len(_h_) == 64:
        HEX64.add(_h_); HEX16.add(_h_[:16])
PAT_ROOT = os.path.join(C, "IALD", "Central de Patentes")


CONHECIDOS = {str(x) for x in (Vd.get("selo_ts"), Vd.get("instalado_em"), Vd.get("data")) if x}
CONHECIDOS.update(str(x) for x in K_EMU.values())
CONHECIDOS.update(str(h)[:8] for h in ESP["veracidade"]["fontes"].values()); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_pt"]); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_en"])                      # os campos EMULADOS dos recibos do B(n) que o handoff recebe (so' existem depois do passo 10)
CONHECIDOS.add(T._linha_maquina_v410(core_emu, T._dados_paragrafo(core_emu)))   # a linha de maquina do paragrafo novo (lida dos registros do core emulado)
CONHECIDOS.add((Vd.get("selo") or {}).get("perfil") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("esquema") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("veredito") or "")
CONHECIDOS.update({T.TOPICO_NOVO[:-3], "v410_kernel", "v410_selo"})     # o nome do topico sem a extensao (o [[wikilink]]) e as duas pastas que o fechar cria ANTES de escrever o handoff
VALORES_LIDOS = set((Vd.get("veracidade") or {}).get("lido") or {}) | set((Vd.get("selo") or {}).keys()) | set((Vd.get("declaracao") or {}).keys()) | set((Vd.get("sidecar") or {}).keys())


def achado(tok):
    if tok in CONHECIDOS:
        return "lido"
    if re.fullmatch(r"[0-9a-f]{16}", tok):
        return "hash_lido" if tok in HEX16 else None
    if re.fullmatch(r"[0-9a-f]{64}", tok):
        return "hash_lido" if tok in HEX64 else None
    if tok in NOMES_ARQ or tok in KERN or tok in UMTXT or tok in INS_TXT or tok in FALAS_TXT:
        return "fonte"
    if tok in core_emu or tok in (core_emu.get("kernel_formalization") or {}) or tok in selo_emu or tok in VALORES_LIDOS:
        return "core"
    if tok.endswith(".lean") and os.path.exists(os.path.join(NOSE, "tgl_kernel", *tok.split("/"))):
        return "kernel_arquivo"
    if "\\" in tok or "/" in tok:
        cands = [os.path.join(PAT_ROOT, tok), os.path.join(PKG, tok), os.path.join(os.path.dirname(PKG), tok.replace("work\\cadeia_de_selo\\", "")), os.path.join(PAT_ROOT, tok.replace("/", os.sep))]
        if any(os.path.exists(c) for c in cands) or tok.startswith(("work\\cadeia_de_selo\\v410", "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v410")):
            return "caminho"
        pre = tok.split("\\")[0].split("/")[0]
        if pre in ("insumos", "work"):
            return "caminho_relativo"
    return None


SEM = {}
total_tok = 0
for nome, txt in RENDER.items():
    for tok in sorted(set(re.findall(r"`([^`\n]+)`", txt))):
        total_tok += 1
        if achado(tok) is None and achado(tok.split(" ")[0]) is None and achado(tok.rstrip(".,;:)")) is None:
            SEM.setdefault(tok, []).append(nome)
etapa("cita_so_o_que_existe", tokens_conferidos=total_tok, sem_fonte={k: sorted(set(v)) for k, v in SEM.items()}, ok=not SEM)
print("  cita so' o que existe: %d termo(s) entre crases conferido(s); sem fonte: %d" % (total_tok, len(SEM)))
for k, v in list(SEM.items())[:30]:
    falha("termo entre crases sem fonte real: `%s` (em %s)" % (k, sorted(set(v))[:3]))

# ------------------------------------------------------------------ 6. as superficies em COPIAS (nada real e' tocado)
if not SEM_SUP and not P:
    ENS = os.path.join(OUT, "ensaio_superficies"); os.makedirs(ENS)
    ALVOS = [os.path.join(NOS_REAL, "MEMORIA_DA_LINHAGEM.md"), os.path.join(NOS_REAL, "DESENHO_DO_FECHAMENTO_QG.md"), os.path.join(ATLD, "TGL_ATLAS.md"), os.path.join(ATLD, "TGL_CORE_MEMORY.md"), os.path.join(UMEM, "MEMORY.md"),
             os.path.join(UMEM, "MEMORY_2.md"), HAJA] + [os.path.join(UMEM, t_) for t_ in ("missao-ultima-flag-um-py.md", "central-de-patentes-estado.md", "estatuto-da-prova-07out.md")]
    ANTES = {p: (os.path.getsize(p), os.path.getmtime(p), fsha(p)[:16]) for p in ALVOS}
    for p in ALVOS:
        shutil.copy2(p, os.path.join(ENS, os.path.basename(p)))
    sp = os.path.join(HERE, "superficies_v410.py")

    def roda_superficies(pasta):
        buf = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="\n"); rc_ = 0
        old_argv = sys.argv[:]; sys.argv = [sp, "--copias", pasta]
        try:
            with contextlib.redirect_stdout(buf):
                runpy.run_path(sp, run_name="__main__")
        except SystemExit as ex:
            rc_ = ex.code if isinstance(ex.code, int) else (0 if ex.code in (None, 0) else 1)
        except BaseException as ex:  # noqa: BLE001
            rc_ = 99; buf.write("EXCECAO: %s\n%s" % (ex, traceback.format_exc()))
        finally:
            sys.argv = old_argv
        buf.flush(); buf.seek(0); return rc_, buf.read()

    def bytes_da_pasta(pasta):
        return {f_: fsha(os.path.join(pasta, f_)) for f_ in sorted(os.listdir(pasta))}
    _RN = ["iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "h0dn_fontes_hms13_v410", "cunhagens_v410", "kh_n1_cobertura_v410"]
    exige = [("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v410_selada -->"] + _RN), ("DESENHO_DO_FECHAMENTO_QG.md", ["<!-- adendo_v410_selada -->", S16]),
             ("TGL_ATLAS.md", ["<!-- atlas_v410_selada -->", S16] + _RN), ("TGL_CORE_MEMORY.md", ["<!-- core_v410_selada -->", S16, "h0dn_bg1_v410", "a_escala_v410", "h0dn_fontes_hms13_v410"]), ("CLAUDE.md", ["<!-- haja_luz_v410_selada -->", S16]),
             ("MEMORY.md", [S16]), ("MEMORY_2.md", ["v410"]), ("estatuto-da-prova-07out.md", ["<!-- v410_selada -->", S16]), ("missao-ultima-flag-um-py.md", [S16]), ("central-de-patentes-estado.md", [S16]),
             (T.TOPICO_NOVO, [S16] + _RN)]
    n_real_l = open(os.path.join(ENS, "MEMORY.md"), "rb").read().count(b"\n"); n_real_b = os.path.getsize(os.path.join(ENS, "MEMORY.md"))
    # --- cenario (a): o MEMORY.md REAL como esta hoje (a superficie NAO compacta nada)
    antes_a = bytes_da_pasta(ENS)
    rc_a, out_a = roda_superficies(ENS)
    open(os.path.join(OUT, "ensaio_superficies_out.txt"), "w", encoding="utf-8").write(out_a)
    depois_a = bytes_da_pasta(ENS)
    cena_a = {"memory_md_real_linhas_antes": n_real_l, "memory_md_real_bytes_antes": n_real_b, "rc": rc_a, "recusou_com_rc3": rc_a == 3, "nada_escrito_na_recusa": (antes_a == depois_a) if rc_a == 3 else None, "sem_bak_na_recusa": (not [f_ for f_ in os.listdir(ENS) if ".bak_" in f_ or ".tmp" in f_]) if rc_a == 3 else None,
              "contagens_na_saida": ("linhas ANTES %d" % n_real_l in out_a) if rc_a == 3 else None, "ultima_linha": out_a.strip().splitlines()[-1][:220] if out_a.strip() else ""}
    print("  superficies, cenario (a) MEMORY.md REAL (%d linhas, %d B): rc %s%s" % (n_real_l, n_real_b, rc_a, " -- RECUSOU (a superficie nao compacta; a gerencia decide)" if rc_a == 3 else ""))
    if rc_a not in (0, 3):
        falha("superficies_v410.py (copias do MEMORY.md real) saiu com rc %s (esperado 0 ou 3; ver ensaio_superficies_out.txt)" % rc_a)
    if rc_a == 3:
        if not (cena_a["nada_escrito_na_recusa"] and cena_a["sem_bak_na_recusa"] and cena_a["contagens_na_saida"] and "NAO compacta" in out_a):
            falha("a RECUSA (rc 3) do MEMORY.md real escreveu algo, deixou .bak/.tmp ou nao disse as contagens: %s" % cena_a)
    else:
        for arq, ms in exige:
            t_ = open(os.path.join(ENS, arq), encoding="utf-8").read()
            for m_ in ms:
                if t_.count(m_) == 0:
                    falha("cenario (a): marcador %s ausente em %s" % (m_, arq))
    # --- cenario (b): um MEMORY.md com FOLGA (a copia do real, so' sem linhas de ponteiros; as duas ancoras ficam)
    def copia_com_memory(nome, ajusta):
        pasta = os.path.join(OUT, nome); os.makedirs(pasta)
        for p in ALVOS:
            shutil.copy2(p, os.path.join(pasta, os.path.basename(p)))
        mp = os.path.join(pasta, "MEMORY.md"); raw_ = open(mp, "rb").read(); novo_ = ajusta(raw_)
        open(mp, "wb").write(novo_); return pasta, novo_

    def reduz_a(alvo_linhas):
        def f(raw_):
            ls = raw_.decode("utf-8").split("\n"); fim_ = ls.pop() if ls and ls[-1] == "" else None
            ancora = lambda l: ("(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")) or ("(handoff-v409-custodia.md)" in l and l.startswith("- [HANDOFF v409"))
            k = len(ls) - 1
            while len(ls) > alvo_linhas and k >= 0:
                if ls[k].startswith("- [") and not ancora(ls[k]):
                    del ls[k]
                k -= 1
            assert len(ls) <= alvo_linhas, ("nao consegui reduzir a copia do MEMORY.md ate o alvo", len(ls), alvo_linhas)
            return ("\n".join(ls + ([""] if fim_ is not None else []))).encode("utf-8")
        return f
    ENS_B, mem_b = copia_com_memory("ensaio_superficies_folga", reduz_a(150))
    n_b0 = mem_b.count(b"\n")
    rc_b1, out_b1 = roda_superficies(ENS_B)
    open(os.path.join(OUT, "ensaio_superficies_folga_out.txt"), "w", encoding="utf-8").write(out_b1)
    conta = {}
    for arq, ms in exige:
        pth = os.path.join(ENS_B, arq); t_ = open(pth, encoding="utf-8").read() if os.path.exists(pth) else ""
        for m_ in ms:
            conta["%s [%s]" % (arq, m_)] = t_.count(m_)
    zero = [k for k, v in conta.items() if v == 0]
    mem = open(os.path.join(ENS_B, "MEMORY.md"), "rb").read(); n_b = len(mem); n_l = mem.count(b"\n")
    apos_1a = bytes_da_pasta(ENS_B)
    rc_b2, out_b2 = roda_superficies(ENS_B)
    open(os.path.join(OUT, "ensaio_superficies_folga_out_2a_rodada.txt"), "w", encoding="utf-8").write(out_b2)
    cena_b = {"memory_md_antes_linhas": n_b0, "rc_1a_rodada": rc_b1, "rc_2a_rodada": rc_b2, "idempotente_na_2a": ("NADA A GRAVAR" in out_b2) and bytes_da_pasta(ENS_B) == apos_1a, "marcadores_zero": zero, "contagens": conta, "memory_md_bytes": n_b, "memory_md_linhas": n_l,
              "ultima_linha_1a": out_b1.strip().splitlines()[-1][:200] if out_b1.strip() else ""}
    print("  superficies, cenario (b) COM FOLGA (%d linhas): rc 1a=%s, rc 2a=%s (idempotente: %s); MEMORY.md %d B, %d linhas; marcadores com zero: %d" % (n_b0, rc_b1, rc_b2, cena_b["idempotente_na_2a"], n_b, n_l, len(zero)))
    if rc_b1 != 0:
        falha("superficies_v410.py (copia com folga) saiu com rc %s na 1a rodada (ver ensaio_superficies_folga_out.txt)" % rc_b1)
    if rc_b2 != 0 or not cena_b["idempotente_na_2a"]:
        falha("superficies_v410.py (copia com folga) nao e' idempotente na 2a rodada (rc %s)" % rc_b2)
    if zero:
        falha("marcadores do passo 9 com zero ocorrencia na copia com folga: %s" % zero[:4])
    if not (n_b < 24000 and n_l <= 195):
        falha("MEMORY.md da copia com folga fora dos limites (%d B, %d linhas)" % (n_b, n_l))
    if n_l != n_b0 + 1:
        falha("a copia com folga: o MEMORY.md devia crescer EXATAMENTE a linha do handoff (de %d para %d) e foi para %d: a superficie nao pode compactar nada" % (n_b0, n_b0 + 1, n_l))
    # --- cenario (c): um MEMORY.md NO LIMITE (195 linhas): a linha do handoff o leva a 196 e a superficie tem de RECUSAR (rc 3), sem escrever nada e sem compactar
    def exatamente_195(raw_):
        r_ = reduz_a(195)(raw_) if raw_.count(b"\n") > 195 else raw_
        while r_.count(b"\n") < 195:
            r_ += b"\n"
        return r_
    ENS_C, mem_c = copia_com_memory("ensaio_superficies_limite", exatamente_195)
    assert mem_c.count(b"\n") == 195, mem_c.count(b"\n")
    antes_c = bytes_da_pasta(ENS_C)
    rc_c, out_c = roda_superficies(ENS_C)
    open(os.path.join(OUT, "ensaio_superficies_limite_out.txt"), "w", encoding="utf-8").write(out_c)
    cena_c = {"memory_md_linhas_antes": 195, "rc": rc_c, "recusou_com_rc3": rc_c == 3, "nada_escrito": bytes_da_pasta(ENS_C) == antes_c, "sem_bak_nem_tmp": not [f_ for f_ in os.listdir(ENS_C) if ".bak_" in f_ or ".tmp" in f_],
              "disse_as_contagens": ("linhas ANTES 195, linhas DEPOIS 196, limite de linhas 195" in out_c), "disse_que_nao_compacta": ("NAO compacta" in out_c), "ultima_linha": out_c.strip().splitlines()[-1][:220] if out_c.strip() else ""}
    print("  superficies, cenario (c) NO LIMITE (195 linhas): rc %s; nada escrito: %s; disse as contagens (195 -> 196, limite 195): %s" % (rc_c, cena_c["nada_escrito"], cena_c["disse_as_contagens"]))
    if not (cena_c["recusou_com_rc3"] and cena_c["nada_escrito"] and cena_c["sem_bak_nem_tmp"] and cena_c["disse_as_contagens"] and cena_c["disse_que_nao_compacta"]):
        falha("a RECUSA do MEMORY.md no limite nao foi como esperado (rc 3, nada escrito, sem .bak/.tmp, contagens ditas): %s" % cena_c)
    DEPOIS = {p: (os.path.getsize(p), os.path.getmtime(p), fsha(p)[:16]) for p in ALVOS}
    etapa("superficies", cenario_a_memory_md_real=cena_a, cenario_b_com_folga=cena_b, cenario_c_no_limite=cena_c, originais_intactos=(ANTES == DEPOIS))
    print("  superficies: originais intactos: %s" % (ANTES == DEPOIS))
    if ANTES != DEPOIS:
        falha("UM ORIGINAL MUDOU durante o ensaio das superficies (nao devia: so' copias)")
# ------------------------------------------------------------------ 7. o b3_recibo REAL contra recibos SINTETICOS (derivados dos reais da v409)
if not SEM_B3:
    B3D = os.path.join(OUT, "b3_sintetico"); os.makedirs(B3D)
    pinos = rdj(os.path.join(PKG, "PINOS_BN_v410.json")); pre = rdj(pinos["recibo_pre_selo"]["path"]); PKG_ANT = os.path.join(os.path.dirname(PKG), "v409")
    import glob as _g
    base_ens = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3_ensaio_*", "RECIBO_SINCRONIZACAO_v409_*.json"))[0]); base_apl = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v409_*.json"))[0])
    n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1

    def sintetico(base, modo):
        r = json.loads(json.dumps(base)); r["versao_alvo"] = "v410"; r["fase"] = "pos_selo"; r["modo"] = modo; r.pop("salto", None); r.pop("cadeia_de_selos", None)
        r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"]))
        r["manifesto_novo"]["deployment_id"] = "B%d-v410-20261023-R1" % n_ger
        r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}
        r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v410"}
        r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
        if modo == "ensaio":
            r["veredito"] = "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger; r["aplicacao"] = None
        else:
            r["veredito"] = "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_ger
            r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v410", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
        r["_sintetico"] = "SINTETICO: derivado do recibo real da v409 pelo harness; NAO e' um recibo do esboco"
        return r
    seq = [0]

    def roda_helper(nome, r, modo, extra=()):
        seq[0] += 1
        pth = os.path.join(B3D, "%02d_%s_RECIBO_SINTETICO.json" % (seq[0], nome)); raw = json.dumps(r, ensure_ascii=False, indent=1).encode("utf-8"); open(pth, "wb").write(raw)
        so = os.path.join(B3D, "%02d_%s_stdout.txt" % (seq[0], nome)); open(so, "w", encoding="utf-8").write("ruido\n" + json.dumps({"veredito": r.get("veredito"), "recusa": None, "recibo": pth, "recibo_sha256": sha(raw)}) + "\n")
        pr_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "b3_recibo_v410.py"), so, modo] + list(extra), capture_output=True, text=True, encoding="utf-8")
        return pr_.returncode, (pr_.stdout + pr_.stderr).strip().splitlines()[-3:]
    CASOS = []
    pos_e = sintetico(base_ens, "ensaio"); pos_a = sintetico(base_apl, "aplicar")
    CASOS.append(("ensaio_ok", pos_e, "ensaio", 0)); CASOS.append(("aplicar_ok", pos_a, "aplicar", 0))

    def mut(r, f):
        r2 = json.loads(json.dumps(r)); f(r2); return r2
    CASOS += [("salto_declarado", mut(pos_e, lambda r: r.update({"salto": {"declarado": True}})), "ensaio", 1),
              ("veredito_com_salto", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__SALTO_v392_v410__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "ensaio", 1),
              ("geracao_errada", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (n_ger + 1)})), "ensaio", 1),
              ("versao_alvo_v409", mut(pos_e, lambda r: r.update({"versao_alvo": "v409"})), "ensaio", 1),
              ("bateria_falhou", mut(pos_e, lambda r: r.update({"bateria_resultado": {"veredito": "BATERIA_FALHOU"}})), "ensaio", 1),
              ("bancada_pinava_v392", mut(pos_e, lambda r: r["manifesto_anterior"].update({"version": "v392"})), "ensaio", 1),
              ("recibo_pre_selo_de_outro", mut(pos_e, lambda r: r.update({"recibo_pre_selo": {"sha256": "0" * 64}})), "ensaio", 1),
              ("manifesto_anterior_mudou", mut(pos_e, lambda r: r["manifesto_anterior"].update({"sha256": "f" * 64})), "ensaio", 1),
              ("pinos_da_bateria_de_v409", mut(pos_e, lambda r: r["bateria"]["pinos_da_versao"].update({"versao": "v409"})), "ensaio", 1),
              ("ensaio_com_aplicacao", mut(pos_e, lambda r: r.update({"aplicacao": {"x": 1}})), "ensaio", 1),
              ("aplicar_pos_conferencia_v409", mut(pos_a, lambda r: r["aplicacao"]["pos_conferencia"].update({"canonical_version": "v409"})), "aplicar", 1),
              ("aplicar_sem_aplicacao", mut(pos_a, lambda r: r.update({"aplicacao": None})), "aplicar", 1),
              ("aplicar_com_veredito_de_ensaio", mut(pos_a, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "aplicar", 1)]
    res_b3 = []
    for nome, r, modo, esperado in CASOS:
        rc_, cauda = roda_helper(nome, r, modo)
        res_b3.append({"caso": nome, "rc": rc_, "esperado": esperado, "ok": rc_ == esperado, "cauda": [c[:200] for c in cauda]})
        print("  b3_recibo %-34s rc %s (esperado %s) %s" % (nome, rc_, esperado, "OK" if rc_ == esperado else "FALHOU"))
        if rc_ != esperado:
            falha("b3_recibo_v410.py: caso %s deu rc %s (esperado %s): %s" % (nome, rc_, esperado, cauda))
    rc_, cauda = roda_helper("terceiro_argumento", pos_e, "ensaio", extra=("0" * 64,))
    res_b3.append({"caso": "terceiro_argumento_(cadeia)", "rc": rc_, "esperado": 1, "ok": rc_ == 1, "cauda": [c[:200] for c in cauda]})
    if rc_ != 1:
        falha("b3_recibo_v410.py aceitou um 3o argumento (nao ha cadeia de selos na v410)")
    etapa("b3_recibo", sintetico=True, base="recibos reais da v409 (so' leitura)", geracao_nova=n_ger, casos=res_b3, n_ok=sum(1 for c in res_b3 if c["ok"]), n=len(res_b3))

# ------------------------------------------------------------------ 8. o registro do mapa (montar) contra o core emulado e o livro real (so' leitura)
try:
    RM = importar("registrar_mapa_v410", os.path.join(HERE, "registrar_mapa_v410.py"))
    ids = RM.ids_do_livro()
    arts = [os.path.join(NOSE, "um.py"), os.path.join(NOSE, "um_absoluto_selo.json")]
    REG = RM.montar(Vd, core_emu, selo_emu, ids, arts)
    # controles negativos de registrar_mapa_v410: a regra da ordem do 4,44 aplicada aos campos do registro (sem o p, sem a linha dos 5 sigma; a clausula completa passa) e as recusas de montar() (selo de outra versao; rota nova que ja' existe no livro)
    _zm = QD.esperados(_res_p, "pt")[0]["z_disc"]["md"]; _pm = QD.esperados(_res_p, "pt")[0]["p_disc"]["md"]

    def _recusa(f):
        try:
            f()
            return False
        except AssertionError:
            return True
    CTL_MAPA = {"regra_4_44_sem_o_p_reprova": bool(RM.regra_4_44([{"c": "o z_disc = " + _zm + ", abaixo do degrau de 5σ, que não foi alcançado"}], _zm, _pm)),
                "regra_4_44_sem_a_linha_dos_5_sigma_reprova": bool(RM.regra_4_44([{"c": "z_disc = " + _zm + " (p unilateral " + _pm + ")"}], _zm, _pm)),
                "regra_4_44_completa_passa": not RM.regra_4_44([{"c": "z_disc = " + _zm + " (calibrado; p unilateral " + _pm + "), abaixo do degrau de 5σ da creditação, que não foi alcançado (" + _zm + " < 5)"}], _zm, _pm),
                "montar_recusa_selo_de_outra_versao": _recusa(lambda: RM.montar(Vd, core_emu, dict(selo_emu, um_version="v409"), ids, arts)),
                "montar_recusa_rota_nova_que_ja_existe": _recusa(lambda: RM.montar(Vd, core_emu, selo_emu, set(ids) | {RM.NOVA}, arts))}
    etapa("mapa_controles_negativos", **CTL_MAPA)
    for k_, v_ in CTL_MAPA.items():
        print("  mapa, controle %-48s %s" % (k_, "ok" if v_ else "FALHOU"))
        if not v_:
            falha("mapa: controle negativo de registrar_mapa_v410 nao deu o esperado: %s" % k_)
    pj = os.path.join(OUT, "registro_mapa_v410_ENSAIO.json"); open(pj, "w", encoding="utf-8").write(json.dumps(REG, ensure_ascii=False, indent=1))
    viol = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    # cada registro e' validado pela MESMA funcao que o mapa usa (rotas._valida), importada so' para isso: NAO se chama registrar; o livro so' e' lido
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("rotas_ro", os.path.join(C, "IALD", "MAPA_DE_ROTAS", "rotas.py")); _rotas = _iu.module_from_spec(_sp); _sp.loader.exec_module(_rotas)
    _seqs = set()
    for _ln in open(os.path.join(C, "IALD", "MAPA_DE_ROTAS", "rotas.jsonl"), encoding="utf-8"):
        _ln = _ln.strip()
        if _ln:
            _r = json.loads(_ln)
            if isinstance(_r.get("seq"), int):
                _seqs.add(_r["seq"])
    VAL = []
    for x in REG:
        try:
            _rotas._valida(json.loads(json.dumps(x)), set(ids), _seqs); VAL.append({"rota_id": x["rota_id"], "tipo": x["tipo"], "valida_pelo_mapa": True})
        except Exception as ex:  # noqa: BLE001
            VAL.append({"rota_id": x["rota_id"], "tipo": x["tipo"], "valida_pelo_mapa": False, "erro": "%s: %s" % (type(ex).__name__, str(ex)[:300])}); falha("mapa: o registro %s nao passa em rotas._valida: %s" % (x["rota_id"], str(ex)[:200]))
    print("  mapa: rotas._valida (sem registrar): %s" % ", ".join("%s=%s" % (v_["rota_id"].split(".")[-1][:28], v_["valida_pelo_mapa"]) for v_ in VAL))
    etapa("mapa", ok=(not viol and all(v_["valida_pelo_mapa"] for v_ in VAL)), n_registros=len(REG), rotas=[x["rota_id"] for x in REG], tipos=[x["tipo"] for x in REG], validacao_rotas_valida=VAL, book_n_rotas=len(ids), saida=pj, nota="ENSAIO contra o core emulado: NAO e' o registro (o real e' montado depois do fechar; o registro e' ato da gerencia)")
    print("  mapa: %d registro(s) montado(s) (%s); livro com %d rotas (so' leitura)" % (len(REG), ", ".join(x["rota_id"] for x in REG), len(ids)))
    if viol:
        falha("mapa: guarda P18 achou %s" % viol)
except BaseException as ex:  # noqa: BLE001
    etapa("mapa", ok=False, erro="%s: %s" % (type(ex).__name__, str(ex)[:300]))
    falha("mapa: registrar_mapa_v410.montar falhou: %s: %s" % (type(ex).__name__, str(ex)[:300]))

# ------------------------------------------------------------------ 9. marcas pendentes, sintaxe
import ast
pend = []; sint = {}
for f in sorted(os.listdir(HERE)):
    if f.endswith(".py"):
        tx = rd(os.path.join(HERE, f))
        if re.search(r"(?m)^\s*#\s*" + MARCA_PENDENTE, tx):
            pend.append(f)
        try:
            ast.parse(tx); sint[f] = "ast.parse ok"
        except SyntaxError as ex:
            sint[f] = "FALHOU: %r" % (ex,); falha("ast.parse de %s falhou" % f)
for f in sorted(os.listdir(HERE)):
    if f.endswith(".sh"):
        rr = subprocess.run(["sh", "-n", os.path.join(HERE, f)], capture_output=True, text=True); sint[f] = "sh -n rc=%d" % rr.returncode
        if rr.returncode:
            falha("sh -n de %s falhou" % f)
if pend:
    falha("marca de texto pendente em: %s" % pend)
etapa("marcas_e_sintaxe", marcas_pendentes=pend, sintaxe=sint)
print("  marcas pendentes: %s; sintaxe: %s" % (pend or "nenhuma", "ok" if all(("ok" in v or "rc=0" in v) for v in sint.values()) else "FALHOU"))

# ------------------------------------------------------------------ limpeza (so' dentro de harness_saida_v410): o Nos EMULADO e as copias pesadas das superficies nao ficam no pacote (--manter-copias as guarda)
LIMPO = {}
if "--manter-copias" not in argv:
    for sub in ("nos_emulado", "conferidor_emulado"):
        pth = os.path.join(OUT, sub)
        if os.path.isdir(pth):
            LIMPO[sub] = sum(os.path.getsize(os.path.join(r_, f_)) for r_, d_, fs_ in os.walk(pth) for f_ in fs_); shutil.rmtree(pth, ignore_errors=True)
    for sub_ in ("ensaio_superficies", "ensaio_superficies_folga", "ensaio_superficies_limite"):
        ens_ = os.path.join(OUT, sub_)
        if os.path.isdir(ens_):
            manter_ = {"MEMORY.md", "estatuto-da-prova-07out.md", T.TOPICO_NOVO}
            tot_ = 0
            for f_ in sorted(os.listdir(ens_)):
                if f_ not in manter_:
                    p_ = os.path.join(ens_, f_); tot_ += os.path.getsize(p_); os.remove(p_)
            LIMPO[sub_ + " (copias pesadas)"] = tot_
etapa("limpeza", removido_bytes=LIMPO, nota="so' o que o harness criou em harness_saida_v410; --manter-copias guarda tudo")

# ------------------------------------------------------------------ resumo
R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
R["tudo_passou"] = bool(not R["problemas"]); R["nao_exigiu_refazer"] = NAO_REFAZER
R["veredito"] = ("TUDO PASSOU: o conferidor da v410 (16 itens C1-C16 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (os QUATRO registros NOVOS com funcao: iald2_v410 -- as ancoras da pedra, inclusive a secao 6, o atrator, o modulo, as bandeiras, a escada, as respostas do operador, a c16, a instancia de brinquedo, o alcance (D64), as inscricoes, as chaves antigas, o que fica False por teorema -- e a_escala_v410 -- a pedra AEscala: as ancoras, as bandeiras, as falas de 09/11, os numeros recalculados, os nomes ratificados e a forma canonica do Clay --, h0dn_bg1_v410 -- o teste pre-registrado da razao de Hubble: pre-registrado; nenhum dado observado lido; "
                 "o veredito, as checagens, os valores contra ESPERADOS[registros_funcao_v410][h0dn], o sha256 do texto-fonte da funcao de veredito, os seis ramos, os pinos, observed_vector_read False em todo lugar, o texto limpo, a linha do bloco no stdout e o resumo no selo, com a mutacao do ESPERADOS e do CANDIDATO na memoria --, e h0dn_fontes_hms13_v410 -- o recibo documental HMS/13: cobertura documental de fontes, nao covariancia fisica fechada; nada aberto --; cunhagens_v410 com as falas de 06 a 09/11 (DL.N_FALAS_V410; de quatro, so' o trecho), as erratas " + ", ".join(e_.split()[0] for e_ in DLX.ERRATAS_V410) + " e a dos pisos e as decisoes " + DLX.DECISOES_ROTULO + "; "
                 "o tetelestai_terminal_v408, o psion_canto_v407, o fechamento_v406 e a traducao_turing_v409 HERDADOS e recriados, com as ancoras e os bundles deles; cunhagens_v409, cunhagens_v408, cunhagens_v407 e cunhagens_v406 e os kh_n1_cobertura herdados; os registros recriados, as pedras seladas no kernel e o gate sem se mover; as linhas [v410] a [v397] e a do sidecar do stdout), os textos renderizam (inclusive secao_aescala e secao_h0dn) e a guarda P18 e a guarda das frases estao limpas, "
                 "a custodia G1 le o bloco da linhagem e o handoff, os dois paragrafos do README/site (o do quadro, intocado, e o novo da v410) passam nas verificacoes, as superficies rodam em copias, o b3_recibo e o mapa montam sem registrar")
R["evidencia_da_versao"] = EVID
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v410.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
saida = os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_v410" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json")   # o nome sem sufixo so' nasce da rodada que EXIGE o refazer
open(saida + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(saida + ".tmp", saida)
print("VEREDITO DO HARNESS (%s): %s" % (ROTULO, R["veredito"])); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)

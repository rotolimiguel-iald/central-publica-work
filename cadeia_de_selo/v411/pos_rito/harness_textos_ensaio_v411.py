# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-H-v411, a servico do claude-construtor-v411-posrito] ADAPTADO DE VERDADE (nao so' o rotulo): a v411 = o teste H0DN x BG1 aberto uma vez; NENHUM modulo novo (o bundle e' vazio); UM registro com funcao, h0dn_bg1_v411 (16 checagens; o recalculo do resultado da abertura; as DUAS linhas, o primario sob o modelo publicado e as Cefeidas livres ao lado), e dois por spec (cunhagens_v411, kh_n1_cobertura_v411); os QUATRO registros com funcao da v410 e os dois por spec da v410 sao RECRIADOS (selados, nao sao novos); controles negativos NOVOS do h0dn_bg1_v411 (ausente, nao selado, checagem falsa, valor adulterado nas duas linhas, beta errado, veredito trocado, opened_once falso, observed_vector_read falso, a linha das Cefeidas livres ausente num texto que traz o primario [F67], a frase velha da v410, token proibido), de cunhagens_v411 e kh_n1_cobertura_v411, e os dos recriados da v410; o paragrafo da v411 e a secao do H0DN renderizados e conferidos; a custodia (S6d) roda DE VERDADE por main(nos, pkg, recibo_dir) sobre o Nos emulado; TODA saida e copia (Nos emulado, sandbox das superficies, recibos, resumos) vai para C:\t\k411c\ensaio_topo_proposto\pos_rito\ no ensaio (V411_ENSAIO_TOPO_PROPOSTO=1), e as ENTRADAS do ensaio vem de PRONTO_PARA_O_POS_RITO.json (sem ele: rc 3, nada escrito); ver ADAPTACAO_H_v411.json
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] a PARTE 2: a pedra AEscala (D82 a D87), o recibo documental HMS/13 (D80), os QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410), DOIS modulos, as 23 falas, D63 a D87, E29 a E31: a linha-resumo [v410] no formato NOVO (`iald2_v410=SELOU | a_escala_v410=SELOU | h0dn_bg1_v410=SELOU | h0dn_fontes_hms13_v410=SELOU | specs: N (selados N)`), os QUATRO blocos `>>> veredito <<<` (IALD2, A ESCALA, H0DN x BG1, H0DN FONTES HMS/13), secao_aescala renderizada e conferida (a forma canonica do Clay, D84; a da D83; P = nP na forma da D81; os nomes ratificados, D87; os numeros do delta), o paragrafo do README com os registros novos, `_REGS_NOVOS`/`_RN` com os seis nomes, e os controles negativos NOVOS da escala e do recibo HMS/13 (nos moldes dos do H0DN: o registro, o selo, o stdout, o ESPERADOS e o CANDIDATO). Precisa do dry_v410 do ensaio a seco do candidato novo: NAO foi rodado.
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/harness_textos_ensaio_v409.py, adaptada a v410 (IALD2) por _adapt_forkA_harness_textos_v410.py (fork A, 06/11/2026): o registro NOVO iald2_v410 e os controles dele; traducao_turing_v409 e tetelestai_terminal_v408 HERDADOS; cunhagens_v410 (D65, E29, D63 a D70) e o trio da v409 herdado; o paragrafo da v410 sem nota ao lado; ver bump/pos_rito__harness_textos_ensaio_v410.py.diff.
# [ADAPTADO v410, 09/11/2026, Sonnet (fork A da adaptacao do pos-rito), a servico do claude-construtor-v410] a RETOMADA de 09/11 (DESENHO_v410 e os AO LADO D71 a D76, E30): o SEGUNDO registro com funcao h0dn_bg1_v410 (D72: o teste PRE-REGISTRADO da razao de Hubble H0DN x BG1; pre-registrado; nenhum dado observado lido) e os controles negativos dele (observed_vector_read True, um token proibido no texto,
# a frase obrigatoria removida, o ESPERADOS sem registros_funcao_v411.h0dn: a mutacao do ESPERADOS e do CANDIDATO e' feita NA MEMORIA por um shim de json, nenhum arquivo do pacote e' tocado); a secao 6 da pedra (o atrator) e a c16 no iald2_v410; as QUINZE falas de 06 a 09/11 (quatro so' o trecho); as decisoes D63 a D76; as erratas E29 e E30; textos_v411.secao_h0dn renderizada e conferida; os bullets do paragrafo da README descobertos do proprio paragrafo.
r"""harness_textos_ensaio_v411.py -- o HARNESS DO POS-RITO da v411 em modo ENSAIO (molde: harness_textos_ensaio_v410.py, que rodou na v410; adaptado DE VERDADE a v411 em 12/11/2026 pelo claude-sonnet-posrito-H-v411).
A v411: o teste H0DN x BG1 ABERTO UMA VEZ; NENHUM modulo novo de kernel (o da v410, byte a byte; escada 12308 = a da v410; nenhuma bandeira nova; o bundle e' vazio); UM registro com funcao, h0dn_bg1_v411 (16 checagens, recalculado no rito); cunhagens_v411 e kh_n1_cobertura_v411 (por spec);
os QUATRO registros com funcao da v410 (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410) e os dois por spec da v410 RECRIADOS (seguem selados; nao sao novos); o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS.
Importa os modulos REAIS textos_v411.py e leitura_v411.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado do falso Nos de ENSAIO (ou, se ele nao existir, de dry_v411: core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py, o kernel, o .md, o artigo PT/EN e o sumario);
o SIDECAR um_absoluto_selo_acom.json e' o gerado pela funcao do PROPRIO artefato (selo_acom_sidecar_v399); o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos: o stdout traz as linhas REAIS do fluxo principal do ensaio a seco mais as que so' o rito acrescenta, com a linha real do sidecar por ultimo.
ENTRADAS DO ENSAIO (V411_ENSAIO_TOPO_PROPOSTO=1): C:\t\k411c\ensaio_topo_proposto\PRONTO_PARA_O_POS_RITO.json (gravado pela outra frente quando o ensaio terminou; SEM ele o harness RECUSA com rc 3, sem escrever nada). Chaves LIDAS (todas opcionais; ausente => o caminho padrao do delta_v411, dito no resumo; presente e inexistente => RECUSA rc 4):
  falso_nos, dry, core, selo, stdout, artigo_pt, artigo_en, esperados, manifesto, ensaio_a_seco, pinos_bn, artefato (o caminho do um.py de ensaio) e artefato_sha16 (cruzado com o sha16 do manifesto, de ESPERADOS e do um.py).
SAIDAS: no ensaio, tudo vai para C:\t\k411c\ensaio_topo_proposto\pos_rito\ (harness_saida_v411\ para as copias e o Nos emulado; o resumo HARNESS_TEXTOS_ENSAIO_v411.json em DL.saida(pos_rito\...)); fora do ensaio, as copias ficam em C:\t\h411\harness_saida_v411 e o resumo em pos_rito\ (como antes). NADA e' escrito em work\ no ensaio.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o artefato (ESPERADOS == manifesto == arquivo == dry_v411/um.py) e, fora do ensaio, a regeneracao terminada (refazer_out_v411.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v411.py REAL roda NO LUGAR (cwd = o pacote real), SEM -I, com V411_NOS apontando para o Nos emulado e o sufixo _HARNESS; da' TUDO BATE; a conferencia que a leitura le;
  leitura        a leitura_v411.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS: o registro NOVO h0dn_bg1_v411 [ausente, nao selado, checagem falsa, numero de checagens, valor adulterado (K, as duas linhas), ramo, beta, veredito, opened_once, observed_vector_read, gate, escada, as sete ressalvas, o que nao decide,
                 a emenda as claras, a guarda de finitude, os insumos pinados, os citados, o texto do registro (token proibido, a frase velha da v410, F67), o resumo no selo, o bloco do stdout, a conferencia, ESPERADOS e CANDIDATO mutados na memoria]; cunhagens_v411 e kh_n1_cobertura_v411 [falas, erratas E41 a E43 e a dos pisos, as decisoes do delta, ressalvas, alcance de P = nP, regra do nome, D65, moldura];
                 os QUATRO com funcao e os DOIS por spec da v410 RECRIADOS [ausente, nao selado, veredito, checagens]; os HERDADOS traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407 e fechamento_v406 e os cunhagens/kh de v409 a v406; os recriados de v405 a v399; o gate; o sidecar; os resumos do selo; as linhas [v411] a [v397] do stdout; os bundles anteriores no kernel (v410 a v406);
  textos         todas as funcoes publicas de textos_v411 renderizam, a guarda P18 e a da DIRECAO ficam limpas em cada saida, os marcadores que a cadeia exige estao nos textos; secao_aescala (da v410) FALHA A VISTA por desenho;
  paragrafos     o PARAGRAFO DO QUADRO (v397, intocado) e o PARAGRAFO NOVO da v411 (o teste decisivo aberto uma vez) passam nas verificacoes, com controles negativos (numero adulterado, as quatro obrigacoes da F67 uma a uma, ressalva removida, citacao nao verbatim, o 4,44 intruso, ...); a secao do H0DN;
  custodia       (S6d) textos_custodia_handoff_v411.main(nos, pkg, recibo_dir) DE VERDADE sobre o Nos emulado (diario = a linhagem renderizada aqui; handoff = o renderizado aqui), mais teste_textos_custodia_sem_candidato_v411.py e teste_gatilho_custodia_sem_candidato_v411.py (sandboxes proprios sob o ensaio);
  cita_so_o_que_existe, superficies (em COPIAS, tres cenarios), b3_recibo (recibos SINTETICOS), mapa (registrar_mapa_v411.montar contra o core emulado, so' leitura do livro), marcas.
uso: python -B -X utf8 harness_textos_ensaio_v411.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias] [--so leitura] [--out <nome>]   (rc 0 = tudo passou; rc 3 = PRONTO_PARA_O_POS_RITO.json ausente (ensaio);
rc 4 = precondicao nao satisfeita, nada foi rodado; --nao-exigir-refazer so' vale FORA do ensaio e so' para depurar (o resumo vai para HARNESS_TEXTOS_ENSAIO_v411_DEPURACAO_sem_refazer.json); --so leitura: so' as etapas precondicoes, nos_emulado, conferidor, leitura e leitura_negativos;
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro da pasta de saida do harness)"""
import contextlib, hashlib, importlib.util, io, json, os, re, runpy, shutil, subprocess, sys, time, traceback
sys.dont_write_bytecode = True
MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V411"
MARCA_ADAPTAR = "[A ADAPTAR v" + "411]"   # (por concatenacao: este arquivo nao a carrega literal; o p00 a procura em todo arquivo da cadeia)
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
sys.path.insert(0, PKG)
import delta_v411 as DLX  # noqa: E402   (UMA instancia: o delta REAL da pasta da cadeia; com V411_ENSAIO_TOPO_PROPOSTO=1 ele aponta a rodada para C:\t\k411c\ensaio_topo_proposto)
DL = DLX
ENSAIO = bool(DLX.ENSAIO_TOPO_PROPOSTO)
from guarda_p18_v411 import violacoes  # noqa: E402
import guarda_frases_v411 as GF  # noqa: E402
argv = sys.argv[1:]
SEM_SUP = "--sem-superficies" in argv; SEM_B3 = "--sem-b3" in argv; SEM_NEG = "--sem-negativos" in argv; NAO_REFAZER = "--nao-exigir-refazer" in argv
ROTULO = argv[argv.index("--rotulo") + 1] if "--rotulo" in argv else "final"
SO = argv[argv.index("--so") + 1] if "--so" in argv else None   # "--so leitura": roda SO as etapas precondicoes, nos_emulado, conferidor, leitura e leitura_negativos (resumo em HARNESS_TEXTOS_ENSAIO_v411_SO_LEITURA.json) e termina
OUT_NOME = argv[argv.index("--out") + 1] if "--out" in argv else ("harness_saida_v411_leitura" if SO else "harness_saida_v411")   # a pasta de saida; a de --so leitura e' PROPRIA (harness_saida_v411 e' compartilhada com harness_fechar_sandbox_v411.py)
POS_SAIDA = DLX.saida("pos_rito")   # onde vao os resumos (DL.saida: no real, pos_rito\ da cadeia, como sempre; no ensaio, C:\t\k411c\ensaio_topo_proposto\pos_rito)
OUT = os.path.join(POS_SAIDA, OUT_NOME) if ENSAIO else os.path.join("C:" + os.sep, "t", "h411", OUT_NOME)
NOSE = os.path.join(OUT, "nos_emulado")
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(open(p, "rb").read())
C = "C:" + os.sep
UMEM = os.path.join(C, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ATLD = os.path.join(C, "IALD", "Central de Patentes", "memory")
HAJA = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")
NOS_REAL = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
R = {"rotulo": ROTULO, "inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "ensaio_topo_proposto": ENSAIO, "emulado": ["stdout do rito (rodada_v411_stdout.txt em nos_emulado)", "APLICADO_AO_CANONICO", "o Nos inteiro (montado do falso Nos de ensaio ou de dry_v411: core, selo completado com as chaves do selo da v410 que o main poe depois do literal, um.py, kernel, md, artigo)",
                                                                           "os recibos do B(n) (SINTETICOS, derivados dos recibos reais da v410)", "o diario e o handoff do S6d (a linhagem e o handoff renderizados aqui)"], "etapas": {}, "problemas": []}


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


# ------------------------------------------------------------------ 0. PRONTO_PARA_O_POS_RITO.json (ensaio), entradas e precondicoes
def recusa(msg, rc=4):
    print("RECUSO:", msg); sys.exit(rc)


PRONTO_ARQ = os.path.join(DLX.ENSAIO_DIR, "PRONTO_PARA_O_POS_RITO.json"); PRONTO = {}; ORIGEM = {}
if ENSAIO:
    if not os.path.isfile(PRONTO_ARQ):
        recusa("PRONTO_PARA_O_POS_RITO.json ausente: o ensaio da outra frente ainda nao terminou (%s)" % PRONTO_ARQ, 3)
    try:
        PRONTO = rdj(PRONTO_ARQ)
        assert isinstance(PRONTO, dict)
    except (ValueError, AssertionError) as _e_p:
        recusa("PRONTO_PARA_O_POS_RITO.json ilegivel ou nao e' um objeto JSON (%r): %s" % (_e_p, PRONTO_ARQ))


def entrada(chave, padrao):
    """O caminho de uma entrada do ensaio: o da chave de PRONTO_PARA_O_POS_RITO.json, se ela existir (e entao TEM de existir no disco: fail-closed), senao o padrao do delta_v411 (dito em ORIGEM)."""
    v_ = PRONTO.get(chave)
    if isinstance(v_, str) and v_.strip():
        if not os.path.exists(v_):
            recusa("PRONTO_PARA_O_POS_RITO.json traz %s = %s, que nao existe no disco" % (chave, v_))
        ORIGEM[chave] = "PRONTO"; return v_
    ORIGEM[chave] = "padrao do delta_v411" if padrao else "ausente"
    return padrao


DRY = entrada("dry", DLX.DRY_DIR)
FALSO_NOS = entrada("falso_nos", DLX.FALSO_NOS_DIR)
P_ESP = entrada("esperados", DLX.saida("ESPERADOS_v411.json"))
P_MAN = entrada("manifesto", DLX.MANIFESTO_ARQ)
P_ENS = entrada("ensaio_a_seco", DLX.saida("ensaio_a_seco_v411.json"))
P_PINOS = entrada("pinos_bn", DLX.saida("PINOS_BN_v411.json"))
P_REFAZER = os.path.join(PKG, "refazer_out_v411.txt")   # (so' fora do ensaio)
_FN_CORE = entrada("core", os.path.join(FALSO_NOS, "um_absoluto.json")); _FN_SELO = entrada("selo", os.path.join(FALSO_NOS, "um_absoluto_selo.json")); _FN_STD = entrada("stdout", os.path.join(FALSO_NOS, "rodada_v411_stdout.txt"))
_FN_PT = entrada("artigo_pt", os.path.join(FALSO_NOS, "um_absoluto_pt.txt")); _FN_EN = entrada("artigo_en", os.path.join(FALSO_NOS, "um_absoluto_en.txt"))
_FALTAM = [n_ for n_, p_ in (("ESPERADOS_v411.json", P_ESP), ("o manifesto do artefato (%s)" % os.path.basename(P_MAN), P_MAN), ("PINOS_BN_v411.json", P_PINOS), ("ensaio_a_seco_v411.json", P_ENS)) if not os.path.isfile(p_)]
for n in ("acom_conferencias_v411.py", "quadro_v397.py", "runtime_quadro_v397.py"):
    if not os.path.exists(os.path.join(PKG, n)):
        _FALTAM.append(n)
if _FALTAM:
    recusa("faltam entradas do ensaio: %s (o ensaio da outra frente terminou? caminhos: ESPERADOS %s; manifesto %s)" % (_FALTAM, P_ESP, P_MAN))
ESP = rdj(P_ESP); CM = rdj(P_MAN); ENS_A_SECO = rdj(P_ENS)
CAND_ARQ = entrada("artefato", DLX.CANDIDATO_ARQ)
if not os.path.isfile(CAND_ARQ):
    recusa("falta o artefato (%s: o um.py candidato, ou o artefato de ENSAIO do topo proposto)" % CAND_ARQ)
cand16 = fsha(CAND_ARQ)[:16]
if ENSAIO and PRONTO.get("artefato_sha16") and str(PRONTO["artefato_sha16"])[:16] != cand16:
    recusa("PRONTO_PARA_O_POS_RITO.json diz artefato_sha16 %s e o arquivo do artefato e' %s" % (PRONTO["artefato_sha16"], cand16))
if not (ESP["candidato_sha16"] == CM["sha16"] == cand16):
    recusa("o artefato nao e' um so': ESPERADOS %s, manifesto %s, arquivo %s (regeneracao em curso?)" % (ESP["candidato_sha16"], CM["sha16"], cand16))
if ENS_A_SECO.get("veredito") != "TUDO PASSOU" or ENS_A_SECO.get("sha16") != cand16:
    recusa("o ensaio a seco nao e' deste artefato ou nao passou (veredito %r, sha16 %r)" % (ENS_A_SECO.get("veredito"), ENS_A_SECO.get("sha16")))
for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v411_pt.txt", "dry_v411_en.txt", "dry_v411_pt.toc", "dry_v411_en.toc", "tgl_kernel"):
    if not os.path.exists(os.path.join(DRY, n)):
        recusa("dry_v411 incompleto (falta %s): a regeneracao ainda nao terminou?" % n)
if fsha(os.path.join(DRY, "um.py"))[:16] != ESP["candidato_sha16"]:
    recusa("o um.py de dry_v411 (%s) != o artefato de ESPERADOS (%s): o dry e' de outra geracao" % (fsha(os.path.join(DRY, "um.py"))[:16], ESP["candidato_sha16"]))
refazer = rd(P_REFAZER) if (not ENSAIO and os.path.exists(P_REFAZER)) else ""
if not ENSAIO:   # fora do ensaio a regeneracao do candidato (refazer_out_v411.txt) e' exigida, como na v410
    if not NAO_REFAZER:
        if not os.path.exists(P_REFAZER):
            recusa("falta refazer_out_v411.txt no pacote: a regeneracao do candidato nao foi comprovada (--nao-exigir-refazer so' para depurar)")
        if "== FIM" not in refazer:
            recusa("refazer_out_v411.txt nao mostra '== FIM': a regeneracao nao terminou")
        if os.path.getmtime(P_REFAZER) < os.path.getmtime(P_ESP):
            recusa("refazer_out_v411.txt e' mais ANTIGO que ESPERADOS_v411.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
elif NAO_REFAZER:
    recusa("--nao-exigir-refazer nao vale no ensaio (a regeneracao do ensaio e' o PRONTO_PARA_O_POS_RITO.json)")
TOL_DRY_S = 3600   # (herdado da v411-prep: o ensaio a seco leva ~12 min DEPOIS de gravar o core_ensaio.json e o ESPERADOS sai ao fim dele; a guarda de GERACAO de verdade e' o conteudo (o um.py de dry_v411 tem o sha16 do artefato de ESPERADOS, acima); o tempo so' pega um dry de horas atras)
if os.path.getmtime(os.path.join(DRY, "core_ensaio.json")) < os.path.getmtime(P_ESP) - TOL_DRY_S:
    recusa("o core_ensaio.json de dry_v411 e' mais de %d min mais antigo que ESPERADOS_v411.json: dry de outra geracao?" % (TOL_DRY_S // 60))
EVID = {"ESPERADOS_v411.json": {"mtime": mt(P_ESP), "sha16": fsha(P_ESP)[:16]}, "manifesto": {"mtime": mt(P_MAN), "sha16": fsha(P_MAN)[:16]}, "artefato": {"mtime": mt(CAND_ARQ), "sha16": cand16}, "PINOS_BN_v411.json": {"mtime": mt(P_PINOS), "sha16": fsha(P_PINOS)[:16]}, "ensaio_a_seco_v411.json": {"mtime": mt(P_ENS), "sha16": fsha(P_ENS)[:16]}}
if ENSAIO:
    EVID["PRONTO_PARA_O_POS_RITO.json"] = {"mtime": mt(PRONTO_ARQ), "sha16": fsha(PRONTO_ARQ)[:16]}
elif os.path.exists(P_REFAZER):
    EVID["refazer_out_v411.txt"] = {"mtime": mt(P_REFAZER), "sha16": fsha(P_REFAZER)[:16]}
EVID.update({"dry_v411/" + n: {"mtime": mt(os.path.join(DRY, n)), "sha16": fsha(os.path.join(DRY, n))[:16]} for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "dry_v411_pt.txt")})
etapa("precondicoes", ok=True, candidato_sha16=cand16, evidencia=EVID, ensaio_topo_proposto=ENSAIO, origem_das_entradas=dict(ORIGEM), pronto_chaves_lidas=sorted(k_ for k_ in PRONTO if k_ in ORIGEM or k_ in ("artefato", "artefato_sha16")), refazer_exigido=(not ENSAIO and not NAO_REFAZER), refazer_out_presente=os.path.exists(P_REFAZER), refazer_fim_visto=("== FIM" in refazer),
      nota=("ENSAIO do topo proposto: o artefato NAO e' candidato; a regeneracao e' a do PRONTO_PARA_O_POS_RITO.json" if ENSAIO else ("MODO --nao-exigir-refazer: a regeneracao do candidato NAO foi comprovada por este harness (refazer_out_v411.txt nao exigido); o ensaio vale para o candidato, o ESPERADOS e o dry_v411 que estao em disco AGORA" if NAO_REFAZER else "refazer_out_v411.txt exigido e visto com == FIM")))
print("harness do pos-rito v411 (%s)%s: artefato %s; ESPERADOS %s; dry core %s%s" % (ROTULO, " [ENSAIO DO TOPO PROPOSTO]" if ENSAIO else "", cand16, EVID["ESPERADOS_v411.json"]["mtime"], EVID["dry_v411/core_ensaio.json"]["mtime"], "" if ENSAIO else "; refazer FIM: %s" % ("== FIM" in refazer)))

# ------------------------------------------------------------------ 0b. o PACOTE emulado (so' no ensaio): o que a leitura, os textos e o mapa leem por PK (ESPERADOS, o manifesto como CANDIDATO_v411.json, PINOS_BN, FLAGS, o core da v410 selada, o quadro): as entradas do ensaio ficam na pasta de saida do harness, a pasta da cadeia nao e' tocada
os.makedirs(OUT, exist_ok=True)
for _sub in ("nos_emulado", "conferidor_emulado", "pos_rito_emulada", "textos", "ensaio_superficies", "ensaio_superficies_folga", "ensaio_superficies_limite", "b3_sintetico", "pacote_emulado", "s6d_custodia"):
    shutil.rmtree(os.path.join(OUT, _sub), ignore_errors=True)


def _liga(src, dst):
    """hardlink (o arquivo e' so' lido) ou copia; o destino nunca e' escrito depois."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copyfile(src, dst)


if ENSAIO:
    PKE = os.path.join(OUT, "pacote_emulado")
    _liga(P_ESP, os.path.join(PKE, "ESPERADOS_v411.json")); _liga(P_MAN, os.path.join(PKE, "CANDIDATO_v411.json")); _liga(P_PINOS, os.path.join(PKE, "PINOS_BN_v411.json")); _liga(P_ENS, os.path.join(PKE, "ensaio_a_seco_v411.json"))
    for _rel in (("kernel", "FLAGS_v411.json"), ("kernel", "KERNEL_RECIBO_v411.json"), ("kernel", "KH_N1_v411.json"), ("base_v410", "um_absoluto.json"), ("base_v410", "um_absoluto_selo.json"), ("base_v410", "um.py"), ("quadro_v397.py",), ("runtime_quadro_v397.py",)):
        if os.path.isfile(os.path.join(PKG, *_rel)):
            _liga(os.path.join(PKG, *_rel), os.path.join(PKE, *_rel))
    for _f in sorted(os.listdir(os.path.join(PKG, "insumos"))):
        if os.path.isfile(os.path.join(PKG, "insumos", _f)):
            _liga(os.path.join(PKG, "insumos", _f), os.path.join(PKE, "insumos", _f))
    if os.path.isdir(os.path.join(PKG, "insumos", "cunhagens")):
        for _f in sorted(os.listdir(os.path.join(PKG, "insumos", "cunhagens"))):
            _liga(os.path.join(PKG, "insumos", "cunhagens", _f), os.path.join(PKE, "insumos", "cunhagens", _f))
else:
    PKE = PKG   # fora do ensaio o pacote e' o real (como na v410)
if ENSAIO:
    sys.path.insert(0, PKE)   # (o PKE nao tem delta_v411.py: o import do delta segue achando o do PKG; quadro_v397.py do PKE importa o delta pelo sys.path)


def refaz_pasta(p_):
    shutil.rmtree(p_, ignore_errors=True); os.makedirs(p_)


# ------------------------------------------------------------------ 1. o Nos emulado
# v411 (desvio do molde, dito): harness_saida_v411 e' COMPARTILHADA com harness_fechar_sandbox_v411.py (fechar_sandbox, memoria_copia, fechar_sandbox_resultado): este harness NAO apaga a pasta inteira, so' o que ELE cria
os.makedirs(NOSE)
if os.path.isfile(os.path.join(FALSO_NOS, "um.py")) and os.path.isfile(_FN_CORE) and os.path.isfile(_FN_SELO) and os.path.isdir(os.path.join(FALSO_NOS, "tgl_kernel")):
    _FONTE_NOS = "falso Nos de ENSAIO (%s)" % FALSO_NOS
    for _n in sorted(os.listdir(FALSO_NOS)):
        _s = os.path.join(FALSO_NOS, _n)
        if os.path.isdir(_s):
            shutil.copytree(_s, os.path.join(NOSE, _n))
        elif _n == "um.py":
            _liga(_s, os.path.join(NOSE, _n))    # o um.py nunca e' escrito
        else:
            shutil.copyfile(_s, os.path.join(NOSE, _n))
    for _src, _dst in ((_FN_CORE, "um_absoluto.json"), (_FN_SELO, "um_absoluto_selo.json"), (_FN_PT, "um_absoluto_pt.txt"), (_FN_EN, "um_absoluto_en.txt")):
        if os.path.isfile(_src) and os.path.normcase(os.path.abspath(_src)) != os.path.normcase(os.path.abspath(os.path.join(FALSO_NOS, _dst))):
            shutil.copyfile(_src, os.path.join(NOSE, _dst))   # (a chave do PRONTO aponta para outro arquivo que o do falso Nos: vale a do PRONTO)
    _std_base = rd(_FN_STD) if os.path.isfile(_FN_STD) else ""
else:
    _FONTE_NOS = "dry_v411 (o falso Nos nao existe: o Nos e' montado do dry, como na v410)"
    for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"),
                     ("dry_v411_pt.txt", "um_absoluto_pt.txt"), ("dry_v411_en.txt", "um_absoluto_en.txt"), ("dry_v411_pt.toc", "um_absoluto_pt.toc"), ("dry_v411_en.toc", "um_absoluto_en.toc"), ("dry_v411_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v411_en.pdf", "um_absoluto_en.pdf")):
        if os.path.exists(os.path.join(DRY, src)):
            (_liga if src == "um.py" else shutil.copyfile)(os.path.join(DRY, src), os.path.join(NOSE, dst))
    shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSE, "tgl_kernel"))
    _std_base = ""
import ast as _ast
_cj = rdj(os.path.join(NOSE, "um_absoluto.json"))
if "ga_window_status" not in _cj:   # o JSON do rito real traz ga_window_status no topo e a v411 o confere; o ensaio so guarda core e verdict: a emulacao o le da constante do proprio artefato, nunca de ESPERADOS
    _gw = re.search(r"^GA_WINDOW_STATUS = \((.*?)\)\r?$", open(os.path.join(NOSE, "um.py"), "rb").read().decode("utf-8"), re.S | re.M); assert _gw, "a constante GA_WINDOW_STATUS nao esta no artefato"
    _cj["ga_window_status"] = _ast.literal_eval("(" + _gw.group(1) + ")")
    open(os.path.join(NOSE, "um_absoluto.json"), "w", encoding="utf-8").write(json.dumps(_cj, ensure_ascii=False, default=str))
# o selo do ensaio a seco nao traz o que o main poe DEPOIS do literal (sha256 do um.py, fail_closed_selftest, rite_checkpoints, not_sealed_this_run): o selo emulado ganha essas chaves do selo da v410 e o sha256 do um.py do artefato (o falso Nos ja' o traz completo)
_selo0 = rdj(os.path.join(PKG, "base_v410", "um_absoluto_selo.json")); _selo = rdj(os.path.join(NOSE, "um_absoluto_selo.json")) if _FONTE_NOS.startswith("falso") else dict(_selo0, **rdj(os.path.join(DRY, "selo_ensaio.json")))
_selo["sha256"] = dict(_selo.get("sha256") or _selo0.get("sha256") or {}); _selo["sha256"]["um.py"] = fsha(os.path.join(NOSE, "um.py"))
open(os.path.join(NOSE, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(_selo, ensure_ascii=False, default=str))
_ens = ENS_A_SECO   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
# o SIDECAR: a funcao do PROPRIO artefato (a copia de bytes do Nos emulado; __file__ = nos_emulado\um.py) sobre o core e o selo FINAIS do Nos emulado; a linha que ela imprime e' a linha REAL do sidecar
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
open(os.path.join(NOSE, "rodada_v411_stdout.txt"), "w", encoding="utf-8", newline="\n").write(STDOUT_EMULADO)
etapa("nos_emulado", ok=True, pasta=NOSE, fonte=_FONTE_NOS, arquivos=sorted(os.listdir(NOSE)), um16=fsha(os.path.join(NOSE, "um.py"))[:16])

# ------------------------------------------------------------------ 2. o conferidor REAL contra o Nos emulado
# o conferidor roda NO LUGAR, como no passo 1 do chain (cwd = o pacote real): o delta_v411 pina por ASSERT caminhos absolutos, logo nao vive numa copia em arvore. SEM -I (importa o um.py do Nos emulado, que precisa do numpy do usuario);
# V411_NOS aponta para o Nos emulado; o sufixo _HARNESS faz o conferidor escrever conferencia_rito_v411_HARNESS.json em DL.saida(...) (no ensaio: C:\t\k411c\ensaio_topo_proposto; no real: a pasta da cadeia): o harness a copia para pos_rito_emulada\conferidor\conferencia_rito_v411.json (que a leitura le) e a REMOVE (ou restaura os bytes que ja' estavam la').
# A copia de import do um.py que o conferidor faz vai para DL.RODADA_PAI (no ensaio: dentro da pasta do ensaio). Nada fica em work\.
env = dict(os.environ); env["V411_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"
_conf_h = DLX.saida("conferencia_rito_v411_HARNESS.json"); _conf_h_antes = open(_conf_h, "rb").read() if os.path.exists(_conf_h) else None
pr = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v411.py", "_HARNESS"], cwd=PKG, env=env, capture_output=True, text=True, encoding="utf-8")
open(os.path.join(OUT, "conferir_rito_v411_stdout.txt"), "w", encoding="utf-8").write(pr.stdout + pr.stderr)
conf_ok = (pr.returncode == 0 and pr.stdout.strip().splitlines()[-1:] == ["TUDO BATE"])
POS_EMU = os.path.join(OUT, "pos_rito_emulada"); os.makedirs(os.path.join(POS_EMU, "conferidor"))
_conf_sha16 = None
if os.path.exists(_conf_h):
    shutil.copyfile(_conf_h, os.path.join(POS_EMU, "conferidor", "conferencia_rito_v411.json")); _conf_sha16 = fsha(_conf_h)[:16]
    if _conf_h_antes is None:
        os.remove(_conf_h)
    else:
        open(_conf_h, "wb").write(_conf_h_antes)
etapa("conferidor", ok=conf_ok, rc=pr.returncode, ultima_linha=(pr.stdout.strip().splitlines() or [""])[-1][:200], conferencia_sha16=_conf_sha16)
print("  conferidor contra o Nos emulado: %s" % ("TUDO BATE" if conf_ok else "NAO BATEU (rc %s)" % pr.returncode))
if not conf_ok:
    falha("o conferidor real nao deu TUDO BATE contra o Nos emulado: a leitura nao tem a conferencia que le (ver conferir_rito_v411_stdout.txt na pasta de saida)")

# ------------------------------------------------------------------ 3. a leitura REAL contra o Nos emulado (+ controles negativos)
L = importar("leitura_v411", os.path.join(HERE, "leitura_v411.py"))
L.NOS = NOSE; L.HERE = POS_EMU; L.PK = PKE
L._BASE_CORE.clear()
AP = {"um_py_novo": {"sha16": ESP["candidato_sha16"]}, "backups": {"um.py": {"sha16": ESP["origem_sha16"], "backup": "EMULADO_PELO_HARNESS"}}, "ts": time.strftime("%Y%m%d_%H%M%S")}
L._aplicado = lambda: (AP, "EMULADO_PELO_HARNESS")
sys.modules["leitura_v411"] = L
Vd, P = L.ler()
etapa("leitura", problemas=P, h0dn_bg1_v411_selado=(Vd.get("fecho") or {}).get("sealed"), recriados_v410_selados=sorted(k_ for k_, v_ in (Vd.get("reg410_recriados") or {}).items() if (v_ or {}).get("sealed") is not False), n_modulos_novos=Vd.get("n_pedras"), teor=Vd.get("teor"), escada_antes=Vd.get("escada_antes"), kh=Vd.get("kh"), registros_novos=Vd.get("registros_novos"), n_cunhagens=len(Vd.get("verbatins") or {}),
      veracidade_n_checks=(Vd.get("veracidade") or {}).get("n_checks"), patch_ids=Vd.get("patch_ids"))
print("  leitura: %d problema(s); %d pedra(s); escada %s -> %s; registros novos %s" % (len(P), Vd.get("n_pedras") or 0, Vd.get("escada_antes"), Vd.get("teor"), Vd.get("registros_novos")))
for p_ in P:
    falha("leitura: " + p_)
core_path = os.path.join(NOSE, "um_absoluto.json"); selo_path = os.path.join(NOSE, "um_absoluto_selo.json"); std_path = os.path.join(NOSE, "rodada_v411_stdout.txt")
core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()
conf_path = os.path.join(POS_EMU, "conferidor", "conferencia_rito_v411.json"); conf_raw = open(conf_path, "rb").read() if os.path.exists(conf_path) else b""


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


def _sonico410_cai(c):
    c["sonico_v398"]["all_verified"] = False


def _afinacao410_cai(c):
    c["afinacao_das_cordas_v398"]["all_verified"] = False


def _cunh410_cai(c):
    c["cunhagens_v398"]["all_verified"] = False


def _kh410_cai(c):
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


def _selo_v410(s):
    s["um_version"] = "v410"


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


def _selo_registros_v411_diferente(s):
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
    sj["veredito"] = "TGL_SELO_ACOM_SIDECAR_V411__REFUSED__SOME_OBJECTS_REFUSED"


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
    NEG = [variante("selo de outra versao (v410)", f_selo=_selo_v410, espera="o selo nao e v411"),
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
           variante("selo primario: registros_v401 do selo difere do core", f_selo=_selo_registros_v411_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
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
           variante("sonico_v398 deixou de selar", f_core=_sonico410_cai, espera="sonico_v398"),
           variante("afinacao_das_cordas_v398 deixou de selar", f_core=_afinacao410_cai, espera="afinacao_das_cordas_v398"),
           variante("cunhagens_v398 deixou de selar", f_core=_cunh410_cai, espera="cunhagens_v398"),
           variante("kh_n1_cobertura_v398 deixou de selar", f_core=_kh410_cai, espera="kh_n1_cobertura_v398"),
           variante("cunhagens_v397 deixou de selar", f_core=_cunh397_cai, espera="cunhagens_v397"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha de volta a literal False (habitante nao exibido)", f_core=_fock_da_testemunha_volta_a_false, espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion nao le o habitante"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 de volta a literal False (habitante nao exibido)", f_core=_face_do_psibit_volta_a_false, espera="psibit_v395: a face do psion nao le o habitante"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v411 (a falsidade nao rodou) no stdout", f_std=lambda t: t + "   [v401] AVISO: a falsidade da inercia nao rodou: ValueError('x')\n", espera="AVISO da v411"),
           variante("AVISO da v411 (o selo ACOM) no stdout", f_std=lambda t: t + "   [v399] AVISO: o selo ACOM nao rodou: ValueError('x')\n", espera="AVISO da v411"),
           variante("AVISO do sidecar no stdout", f_std=lambda t: t.replace("RITO_RC=0", "[selo_acom] AVISO: nao consegui escrever o sidecar: OSError('x')\nRITO_RC=0"), espera="AVISO da v411"),
           variante("AVISO de bloco anterior (v398) no stdout", f_std=lambda t: t + "   [v398] AVISO: o sonico nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior"),
           variante("linha [v399] ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o selo pela propria tecnologia e a declaracao do operador" not in l) + "\n", espera="linha [v399] do stdout"),
           variante("linha [v401] ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "a falsidade (simulacro) da inercia (lida depois da declaracao do operador)" not in l) + "\n", espera="linha [v401] do stdout"),
           variante("linha `>>> veredito <<<` do selo ACOM ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["selo_acom"]["verdict"] not in l or "selo=" in l) + "\n", espera="o bloco selo_pela_propria_tecnologia_v399 do stdout"),
           variante("linha `>>> veredito <<<` da declaracao ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["declaracao"]["verdict"] not in l or "declaracao=" in l) + "\n", espera="o bloco declaracao_do_operador_v399 do stdout"),
           variante("linha `>>> veredito <<<` da falsidade ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["veredito_da_falsidade_v410"] not in l or "falsidade=" in l) + "\n", espera="o bloco falsidade_da_inercia_v401 do stdout"),
           variante("linha [v398] (sonico, afinacao e cunhagens) ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o sonico e a afinacao das cordas" not in l) + "\n", espera="linha [v398] do stdout"),
           variante("linha [v397] do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\n", espera="linha [v397] do Teste da Unica Palavra"),
           variante("linha do sidecar ausente do stdout (a ultima nao e' a do sidecar)", f_std=lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("[selo_acom]")) + "\n", espera="as duas ultimas linhas do stdout"),
           variante("a linha do sidecar antes da do colapso tipado (ordem trocada)", f_std=lambda t: "\n".join([l for l in t.splitlines() if not l.startswith("[selo_acom]") and not l.startswith("[selo] colapso tipado") and not l.startswith("RITO_RC=")] + [l for l in t.splitlines() if l.startswith("[selo_acom]")] + [l for l in t.splitlines() if l.startswith("[selo] colapso tipado")] + ["RITO_RC=0"]) + "\n", espera="as duas ultimas linhas do stdout")]

    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # v411: a v411 NAO tem modulo novo (o bundle e' vazio): os controles sao do registro NOVO h0dn_bg1_v411 e dos dois por spec novos (cunhagens_v411, kh_n1_cobertura_v411), dos QUATRO registros com funcao e dos DOIS por spec da v410 RECRIADOS,
    # dos HERDADOS (traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407, fechamento_v406 e os cunhagens/kh deles), dos bundles anteriores (v410 a v406) no kernel do Nos, dos resumos do selo, da conferencia e das linhas [v411] a [v406] do stdout.
    # As mensagens esperadas sao as da leitura_v411.py (frente L); as ancoras/bundles vem dos DELTAS (delta_v410 a delta_v406: DLX.D10 a DLX.D6), como a leitura os le, nunca de ESPERADOS.
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    EF3_ = {k_: {"verdict": L._ev(ESP, n_)} for k_, n_ in (("caminho", "caminho_v403"), ("vida", "vida_v403"), ("verdade_adendo", "verdade_adendo_v403"), ("gate", "bandeiras_do_gate_v403"))}   # os vereditos esperados dos registros da v403 (recriados)
    EF4_ = {k_: {"verdict": L._ev(ESP, n_)} for k_, n_ in (("projecao", "projecao_transversal_v404"), ("jo8v32", "jo8v32_v404"), ("f2b", "f2b_errata_v404"))}   # os da v404 (recriados)
    EV3_ = ESP["vereditos_v410"]
    FE_ = DLX.FECHO_REGISTRO; F9_ = DLX.D9.FECHO_REGISTRO; FT_ = DLX.D8.FECHO_REGISTRO; FP_ = "psion_canto_v407"; FH_ = "fechamento_v406"; REC10F_ = tuple(DLX.REGISTROS_FUNCAO_V410); REC10S_ = ("cunhagens_v410", "kh_n1_cobertura_v410")
    FTRUE_ = list(ESP["flags_true_v410"])   # as bandeiras True da v410 selada (a leitura as confere True no kernel do rito)
    RESUMO_MSG = "o selo primario (um_absoluto_selo.json) nao traz os resumos"
    VER_HERD = ": o veredito do rito difere do esperado"   # a mensagem da leitura para os registros HERDADOS (REG_V410D, REG_V406D): o esperado e' o da v410 selada, ou o do ensaio a seco se na troca dita

    def _kf(c):
        return c["kernel_formalization"]

    def _fora_do_trio(c, termo):
        _kf(c)["axiom_report"][termo] = ["propext", "sorryAx"]

    def _sem_linha(tag):
        """o controle do stdout: a linha `[tag] ...` do main (a que a leitura confere) removida"""
        return lambda t_: "\n".join(l for l in t_.splitlines() if not l.lstrip().startswith("[%s] " % tag)) + "\n"

    def _selados_zero(tag):
        return lambda t_: "\n".join(re.sub(r"\(selados \d+\)", "(selados 0)", l) if l.lstrip().startswith("[%s] " % tag) else l for l in t_.splitlines()) + "\n"

    def _std_selados(t_, trecho):
        return chr(10).join(re.sub(r"\(selados \d+\)", "(selados 0)", l) if trecho in l else l for l in t_.splitlines()) + chr(10)

    def _na_linha(tag, velho_, novo_):
        return lambda t_: "\n".join(l.replace(velho_, novo_) if l.lstrip().startswith("[%s] " % tag) else l for l in t_.splitlines()) + "\n"

    def _sem_veredito(v_, dono_=None):
        """a linha `>>> veredito <<<` de um registro removida (e so' ela: a linha de contagens do bloco, que traz `dono_=`, fica)"""
        return lambda t_: "\n".join(l for l in t_.splitlines() if v_ not in l or (dono_ and (dono_ + "=") in l)) + "\n"

    # ---- os bundles e as ancoras dos HERDADOS: lidos dos deltas (a leitura os le de la')
    _B10 = list(DLX.D10.BUNDLE_RELS)[0]; _B9 = list(DLX.D9.BUNDLE_RELS)[0]; _B8 = list(DLX.D8.BUNDLE_RELS)[0]; _B7 = list(DLX.D7.BUNDLE_RELS)[0]; _B6 = list(DLX.D6.BUNDLE_RELS)[0]
    _A10 = list(DLX.D10.ANCORAS)[0]; _A9 = list(DLX.D9.ANCORAS)[0]; _A8 = list(DLX.D8.ANCORAS)[0]; _A7 = list(DLX.D7.ANCORAS)[0]; _A6 = list(DLX.D6.ANCORAS)[0]
    _N9, _N8, _N7, _N6 = len(DLX.D9.ANCORAS), len(DLX.D8.ANCORAS), len(DLX.D7.ANCORAS), len(DLX.D6.ANCORAS)

    def _bundle_no_disco(nome, rel_, msg_):
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

    # ---- o registro h0dn_bg1_v411 (o UNICO novo com FUNCAO): ajudantes dos controles. A mutacao do ESPERADOS e do CANDIDATO e' feita NA MEMORIA (L.json trocado por um shim que muta o dict recem-carregado, e restaurado): nenhum arquivo do pacote e' tocado.
    H1_ = FE_; MH_ = H1_ + " nao selou inteiro"; MOBS_ = H1_ + ": observed_vector_read tem de ser True"; MVER_ = H1_ + ": o veredito do rito difere do ensaio a seco"
    _TOK_ = DLX.TOKENS_PROIBIDOS_V411[0]   # montado por concatenacao no delta: nunca literal neste arquivo (a guarda varre os textos, e este arquivo nao deve carregar o token)
    _CORE0_ = json.loads(core_raw.decode("utf-8"))["core"]; _HD0_ = _CORE0_.get(H1_) or {}
    _NCHK_ = len((_HD0_.get("mechanics") or {}).get("checks") or []); _NINS_ = len(_HD0_.get("insumos_pinados") or {})
    _P1_ = (_HD0_.get("values") or {}).get("primario") or {}; _C1_ = (_HD0_.get("values") or {}).get("cefeidas_livres") or {}
    _ZN_P_ = str(_P1_.get("z_null")); _ZN_C_ = str(_C1_.get("z_null"))
    del _CORE0_, _HD0_

    def _v1(c):
        return c[H1_]["values"]

    def _sem_bloco_h0dn(t_):
        ls_ = t_.split("\n"); i_ = next(i for i, l_ in enumerate(ls_) if l_.startswith("H0DN x BG1 ABERTO [v411"))
        return "\n".join(ls_[:i_] + ls_[i_ + 3:])   # o cabecalho, a linha `primario (modelo publicado) ...` e a linha `>>> veredito <<<`

    def _no_bloco_h0dn(velho_, novo_):
        def f_(t_):
            ls_ = t_.split("\n"); i_ = next(i for i, l_ in enumerate(ls_) if l_.startswith("H0DN x BG1 ABERTO [v411"))
            assert velho_ in ls_[i_ + 1], ("o trecho nao esta na linha do bloco", velho_, ls_[i_ + 1][:200])
            ls_[i_ + 1] = ls_[i_ + 1].replace(velho_, novo_, 1)
            return "\n".join(ls_)
        return f_

    class _JsonShim:
        def __init__(self, real, muta):
            self._real = real; self._muta = muta

        def __getattr__(self, k):
            return getattr(self._real, k)

        def load(self, fp, *a, **kw):
            d_ = self._real.load(fp, *a, **kw); self._muta(os.path.basename(str(getattr(fp, "name", ""))), d_); return d_

    def variante_json(nome, f_json, espera):
        """como variante(), mas a mutacao e' sobre o ESPERADOS_v411.json / CANDIDATO_v411.json / FLAGS_v411.json que a leitura CARREGA (NA MEMORIA; nada e' escrito): L.json e' trocado por um shim e restaurado no finally."""
        real_ = L.json
        try:
            L.json = _JsonShim(real_, f_json)
            _, PV = L.ler()
        finally:
            L.json = real_
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any(espera in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
    _so_esp = lambda f: (lambda nm, d: f(d) if nm == "ESPERADOS_v411.json" else None)
    _so_cm = lambda f: (lambda nm, d: f(d) if nm == "CANDIDATO_v411.json" else None)
    _so_fl = lambda f: (lambda nm, d: f(d) if nm == "FLAGS_v411.json" else None)
    HERD_ = FH_ + " (HERDADO, recriado) nao selou inteiro"; HERDP_ = FP_ + " (HERDADO, recriado) nao selou inteiro"; HERDT_ = FT_ + " (HERDADO, recriado) nao selou inteiro"; HERD9_ = F9_ + " (HERDADO, recriado) nao selou inteiro"
    NEG.extend([
        # ---- h0dn_bg1_v411 (o registro NOVO com funcao: o teste H0DN x BG1 aberto uma vez, recalculado no rito)
        variante("%s ausente do core" % H1_, f_core=lambda c: c.pop(H1_, None), espera="registro obrigatorio ausente do core: " + H1_),
        variante("%s: o registro nao selou" % H1_, f_core=lambda c: c[H1_].update(all_verified=False), espera=H1_ + " nao selou"),
        variante("%s: uma checagem do calculo falhou (c6, o recalculo igual a abertura)" % H1_, f_core=lambda c: c[H1_]["mechanics"]["checks"][5].update(ok=False), espera=MH_),
        variante("%s: o numero de checagens != o do delta" % H1_, f_core=lambda c: c[H1_]["mechanics"]["checks"].pop(), espera=MH_),
        variante("%s: o id de uma checagem trocado" % H1_, f_core=lambda c: c[H1_]["mechanics"]["checks"][-1].update(id="c99"), espera=MH_),
        variante("%s: um valor do calculo adulterado (K)" % H1_, f_core=lambda c: _v1(c).update(K=_v1(c)["K"] + 1e-3), espera=MH_),
        variante("%s: o Z do primario contra o nulo adulterado (linha 1)" % H1_, f_core=lambda c: _v1(c)["primario"].update(z_null=_v1(c)["primario"]["z_null"] + 1.0), espera=MH_),
        variante("%s: o Z do primario contra K adulterado (linha 1)" % H1_, f_core=lambda c: _v1(c)["primario"].update(z_tgl=_v1(c)["primario"]["z_tgl"] + 1e-3), espera=MH_),
        variante("%s: o ramo do primario trocado" % H1_, f_core=lambda c: _v1(c)["primario"].update(ramo=_v1(c)["primario"]["ramo"] + 1), espera=MH_),
        variante("%s: o Z das Cefeidas livres contra o nulo adulterado (linha 2)" % H1_, f_core=lambda c: _v1(c)["cefeidas_livres"].update(z_null=_v1(c)["cefeidas_livres"]["z_null"] + 1e-3), espera=MH_),
        variante("%s: o ramo das Cefeidas livres trocado" % H1_, f_core=lambda c: _v1(c)["cefeidas_livres"].update(ramo=_v1(c)["cefeidas_livres"]["ramo"] + 1), espera=MH_),
        variante("%s: a linha das Cefeidas livres ausente dos values (as DUAS linhas saem juntas)" % H1_, f_core=lambda c: _v1(c).pop("cefeidas_livres"), espera=MH_),
        variante("%s: a linha_ao_lado_cefeidas_livres ausente do registro" % H1_, f_core=lambda c: c[H1_].pop("linha_ao_lado_cefeidas_livres"), espera=MH_),
        variante("%s: beta != alfa x raiz de e do core" % H1_, f_core=lambda c: _v1(c).update(beta=0.0121), espera=MH_),
        variante("%s: beta_ok falso no registro" % H1_, f_core=lambda c: c[H1_].update(beta_ok=False), espera=MH_),
        variante("%s: veredito diferente do ensaio a seco" % H1_, f_core=lambda c: c[H1_].update(verdict="OUTRO_VEREDITO"), espera=MVER_),
        variante("%s: o veredito sem a linha das Cefeidas livres (BESIDE_FREE_CEPHEIDS)" % H1_, f_core=lambda c: c[H1_].update(verdict=c[H1_]["verdict"].replace("BESIDE_FREE_CEPHEIDS_", "BESIDE_X_", 1)), espera=MH_),
        variante("%s: o veredito sem a marca de validade, nao creditacao" % H1_, f_core=lambda c: c[H1_].update(verdict=c[H1_]["verdict"].replace("VALIDITY_NOT_CREDITATION", "VALIDITY", 1)), espera=MH_),
        variante("%s: o registro move o gate" % H1_, f_core=lambda c: c[H1_].update(does_not_gate_core=False), espera=MH_),
        variante("%s: o calculo do runtime nao rodou" % H1_, f_core=lambda c: c[H1_].update(runtime_executed=False), espera=MH_),
        variante("%s: opened_once falso (o teste nao foi aberto uma vez)" % H1_, f_core=lambda c: c[H1_].update(opened_once=False), espera=MH_),
        variante("%s: observed_vector_read falso no registro (o vetor foi lido, uma vez: D169)" % H1_, f_core=lambda c: c[H1_].update(observed_vector_read=False), espera=MOBS_),
        variante("%s: o gate dos values difere do da v410" % H1_, f_core=lambda c: _v1(c).update(gate_verdict="OUTRO_GATE"), espera=MH_),
        variante("%s: a escada dos values difere da da v410" % H1_, f_core=lambda c: _v1(c).update(escada=1), espera=MH_),
        variante("%s: uma das sete ressalvas a menos" % H1_, f_core=lambda c: c[H1_]["ressalvas_secao8"].pop(), espera=MH_),
        variante("%s: o rotulo de uma ressalva adulterado" % H1_, f_core=lambda c: c[H1_]["rotulos_das_sete_ressalvas"].__setitem__(0, "outra ressalva"), espera=MH_),
        variante("%s: um item do que o teste NAO decide a menos" % H1_, f_core=lambda c: c[H1_]["o_que_o_teste_nao_decide"].pop(), espera=MH_),
        variante("%s: a emenda as claras (a) nao confere" % H1_, f_core=lambda c: _v1(c)["a_emenda_as_claras"]["a"].update(ok=False), espera=MH_),
        variante("%s: o recalculo difere da abertura (c6_divergencias)" % H1_, f_core=lambda c: _v1(c).update(c6_divergencias={"z_null": 1e-3}), espera=MH_),
        variante("%s: a guarda de finitude nao confere (z nao finito)" % H1_, f_core=lambda c: _v1(c)["guarda_de_finitude"].update(z_finitos=False), espera=MH_),
        variante("%s: um insumo pinado com o sha256 adulterado" % H1_, f_core=lambda c: next(iter(c[H1_]["insumos_pinados"].values())).update(sha256="0" * 64), espera=MH_),
        variante("%s: um insumo pinado a menos" % H1_, f_core=lambda c: c[H1_]["insumos_pinados"].pop(next(iter(c[H1_]["insumos_pinados"]))), espera=MH_),
        variante("%s: um citado nao embutido a menos" % H1_, f_core=lambda c: c[H1_]["citados_nao_embutidos"].pop(), espera=MH_),
        variante("%s: o contrato de registro fora da escada ausente" % H1_, f_core=lambda c: c[H1_].update(contratos_de_registro_fora_da_escada=[]), espera=MH_),
        variante("%s: um caminho sob a pasta vedada tocado" % H1_, f_core=lambda c: _v1(c).update(sob_pasta_vedada=[os.path.join(DLX.H0DN_PASTA_VEDADA_V410, "x")]), espera=MH_),
        variante("%s: um token proibido no texto do registro (scope)" % H1_, f_core=lambda c: c[H1_].update(scope=c[H1_]["scope"] + " " + _TOK_), espera=MH_),
        variante("%s: a frase velha da v410 («pre-registrado; nenhum dado observado lido») volta como estado do teste" % H1_, f_core=lambda c: c[H1_].update(estatuto=c[H1_]["estatuto"] + " " + DLX.FRASE_H0DN_OBRIGATORIA_PT), espera=MH_),
        variante("%s: F67: o primario dito sem a linha das Cefeidas livres no texto do registro" % H1_, f_core=lambda c: c[H1_].update(diz=list(c[H1_]["diz"]) + ["no H0DN o primário fica a 6,11 contra o nulo"]), espera=MH_),
        variante("%s: F67 em EN: o primario sem as Cefeidas livres no texto do registro" % H1_, f_core=lambda c: c[H1_].update(diz=list(c[H1_]["diz"]) + ["the primary lies 6.11 against the null in the H0DN test, under the published error model"]), espera=MH_),
        variante("%s: o teste dado por cego no texto (F63)" % H1_, f_core=lambda c: c[H1_].update(diz=list(c[H1_]["diz"]) + ["foi um teste cego"]), espera=MH_),
        variante("%s: poder certificado no texto (F61)" % H1_, f_core=lambda c: c[H1_].update(diz=list(c[H1_]["diz"]) + ["o teste tem poder certificado"]), espera=MH_),
        variante("%s: a creditacao afirmada no texto (F60)" % H1_, f_core=lambda c: c[H1_].update(diz=list(c[H1_]["diz"]) + ["a TGL foi confirmada pela natureza"]), espera=MH_),
        variante("%s: a identificacao do operador chamada «leitura do operador» (regra do nome)" % H1_, f_core=lambda c: c[H1_].update(scope=c[H1_]["scope"] + " leitura do operador"), espera=MH_),
        variante("%s: a guarda P18 achou violacao nos values" % H1_, f_core=lambda c: _v1(c).update(p18_violacoes=[["R1", "x"]]), espera=MH_),
        variante("%s: a guarda das frases achou violacao nos values" % H1_, f_core=lambda c: _v1(c).update(frases_violacoes=[["F67", "x"]]), espera=MH_),
        variante("selo primario: sem o resumo de %s" % H1_, f_selo=lambda s: s.pop(H1_, None), espera=MH_),
        variante("selo primario: o resumo de %s difere do core" % H1_, f_selo=lambda s: s[H1_].update(verdict="OUTRO_VEREDITO"), espera=MH_),
        variante("selo primario: o resumo de %s com observed_vector_read False" % H1_, f_selo=lambda s: s[H1_].update(observed_vector_read=False), espera=MOBS_),
        variante("selo primario: o resumo de %s com outro n_checks_esperadas" % H1_, f_selo=lambda s: s[H1_].update(n_checks_esperadas=_NCHK_ - 1), espera=MH_),
        variante("selo primario: o resumo de %s sem a linha ao lado das Cefeidas livres" % H1_, f_selo=lambda s: s[H1_].pop("linha_ao_lado_cefeidas_livres"), espera=MH_),
        variante("selo primario: o resumo de %s sem a chave p2_ao_lado_da_v387 (a 13a; C-04 da revisao de terceiro)" % H1_, f_selo=lambda s: s[H1_].pop("p2_ao_lado_da_v387"), espera=MH_),
        variante("selo primario: o resumo de %s com o valor de p2_ao_lado_da_v387 trocado (C-04)" % H1_, f_selo=lambda s: s[H1_].update(p2_ao_lado_da_v387={"rotulo": "OUTRO_ROTULO", "token_selado": "X"}), espera=MH_),
        variante("a conferencia traz outro veredito de %s" % H1_, f_conf=lambda cj: cj.update({"veredito_h0dn_bg1_v411": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + H1_),
        variante("o bloco `H0DN x BG1 ABERTO [v411` ausente do stdout (cabecalho, as duas linhas e o veredito)", f_std=_sem_bloco_h0dn, espera=MH_),
        variante("linha `>>> veredito <<<` de %s ausente do stdout" % H1_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if ESP["vereditos_novos_v411"][H1_] not in l) + "\n", espera="o bloco " + H1_ + " do stdout"),
        variante("linha do bloco do H0DN: o Z do primario contra o nulo trocado", f_std=_no_bloco_h0dn("Z nulo = " + _ZN_P_, "Z nulo = 0.0"), espera=MH_),
        variante("linha do bloco do H0DN: o Z das Cefeidas livres contra o nulo trocado", f_std=_no_bloco_h0dn("Z nulo = " + _ZN_C_, "Z nulo = 0.0"), espera=MH_),
        variante("linha do bloco do H0DN: uma checagem a menos", f_std=_no_bloco_h0dn("checagens ok = %d/%d" % (_NCHK_, _NCHK_), "checagens ok = %d/%d" % (_NCHK_ - 1, _NCHK_)), espera=MH_),
        variante("linha do bloco do H0DN: o gate dito diferente da base", f_std=_no_bloco_h0dn("gate = o mesmo da base", "gate = outro"), espera=MH_),
        variante("linha do bloco do H0DN: a linha das Cefeidas livres retirada", f_std=lambda t_: re.sub(r"  \|\|  Cefeidas livres \(ao lado, no mesmo item\):[^\n]*?(?=  \|\|  checagens ok)", "", t_, count=1), espera=MH_),
        variante("linha [v411] ausente do stdout", f_std=_sem_linha("v411"), espera="linha [v411]"),
        variante("linha [v411] com registros selados != por spec", f_std=_selados_zero("v411"), espera="a linha [v411] do stdout"),
        variante("linha [v411] com o h0dn nao selado", f_std=lambda t_: t_.replace("| h0dn_bg1_v411=SELOU", "| h0dn_bg1_v411=NAO").replace(": h0dn_bg1_v411=SELOU", ": h0dn_bg1_v411=NAO"), espera="a linha [v411] do stdout"),
        variante("AVISO da v411 (o registro com funcao h0dn_bg1_v411 nao rodou) no stdout", f_std=lambda t_: t_ + "   [v411] AVISO: o registro do H0DN ou os registros por spec da v411 nao rodaram: ValueError('x')\n", espera="AVISO da v411"),
        variante_json("ESPERADOS sem registros_funcao_v411.h0dn (fail-closed)", _so_esp(lambda d: d["registros_funcao_v411"].pop("h0dn")), "ESPERADOS_v411.json nao traz registros_funcao_v411.h0dn"),
        variante_json("ESPERADOS sem o veredito do ensaio a seco de %s" % H1_, _so_esp(lambda d: d["vereditos_novos_v411"].pop(H1_)), "ESPERADOS_v411 nao traz o veredito do ensaio a seco de " + H1_),
        variante_json("ESPERADOS: o veredito de %s em registros_funcao_v411 diferente" % H1_, _so_esp(lambda d: d["registros_funcao_v411"]["h0dn"].update(verdict="OUTRO_VEREDITO")), MH_),
        variante_json("ESPERADOS: um valor de %s diferente do core (K)" % H1_, _so_esp(lambda d: d["registros_funcao_v411"]["h0dn"]["values"].update(K=d["registros_funcao_v411"]["h0dn"]["values"]["K"] + 1e-3)), MH_),
        variante_json("ESPERADOS: o gate da v410 diferente do dos values", _so_esp(lambda d: d.update(qg_closure_gate_verdict_v410="OUTRO_GATE")), MH_),
        variante_json("ESPERADOS: a escada da v410 diferente da do registro", _so_esp(lambda d: d.update(escada_v410_e_v411=[1, 1])), MH_),
        variante_json("CANDIDATO: uma bandeira nova (n_bandeiras 1)", _so_cm(lambda d: d.update(n_bandeiras=1)), "a v411 NAO tem modulo novo de kernel"),
        variante_json("CANDIDATO: um modulo novo de kernel (modulos_novos 1)", _so_cm(lambda d: d["kernel"].update(modulos_novos=1)), "a v411 NAO tem modulo novo de kernel"),
        variante_json("CANDIDATO: as falas embutidas != as do delta", _so_cm(lambda d: d.update(verbatins_embutidos=8)), "o CANDIDATO_v411.json nao traz as"),
        variante_json("FLAGS: uma bandeira nova no FLAGS_v411.json", _so_fl(lambda d: d.update(n_flags=1, flags=[["ext_x", "TGLExt.X"]])), "a v411 NAO tem modulo novo de kernel"),
        variante_json("ESPERADOS: um bundle novo em bundle_sha256", _so_esp(lambda d: d.update(bundle_sha256={"TGLExt/X.lean": "0" * 64})), "a v411 NAO tem modulo novo de kernel"),
        # ---- os QUATRO registros com funcao da v410 RECRIADOS (nao sao novos; seguem selados com o veredito da v410 selada) e os DOIS por spec
        *[v_ for n_ in REC10F_ for v_ in (
            variante("%s (recriado) ausente do core" % n_, f_core=lambda c, n=n_: c.pop(n, None), espera="registro da v410 ausente do core (deveria ser RECRIADO no mesmo ponto do main): " + n_),
            variante("%s (recriado): o registro nao selou" % n_, f_core=lambda c, n=n_: c[n].update(all_verified=False), espera=n_ + " (registro da v410, RECRIADO): nao selou"),
            variante("%s (recriado): veredito diferente da v410 selada" % n_, f_core=lambda c, n=n_: c[n].update(verdict="OUTRO_VEREDITO"), espera=n_ + " (registro da v410, RECRIADO): nao selou"),
            variante("%s (recriado): uma checagem a menos (n_checks)" % n_, f_core=lambda c, n=n_: c[n]["mechanics"].update(n_checks=c[n]["mechanics"]["n_checks"] - 1), espera=n_ + " (registro da v410, RECRIADO): nao selou"),
            variante("%s (recriado): o calculo do runtime nao rodou" % n_, f_core=lambda c, n=n_: c[n].update(runtime_executed=False), espera=n_ + " (registro da v410, RECRIADO): nao selou"),
            variante("%s (recriado): o registro move o gate" % n_, f_core=lambda c, n=n_: c[n].update(does_not_gate_core=False), espera=n_ + " (registro da v410, RECRIADO): nao selou"))],
        variante("cunhagens_v410 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v410", None), espera="registro da v410 ausente do core (deveria ser RECRIADO no mesmo ponto do main): cunhagens_v410"),
        variante("kh_n1_cobertura_v410 (recriado) ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v410", None), espera="registro da v410 ausente do core (deveria ser RECRIADO no mesmo ponto do main): kh_n1_cobertura_v410"),
        variante("cunhagens_v410 (recriada): o registro nao selou", f_core=lambda c: c["cunhagens_v410"].update(all_verified=False), espera="cunhagens_v410 (registro da v410, RECRIADO): nao selou"),
        variante("kh_n1_cobertura_v410 (recriado): o registro nao selou", f_core=lambda c: c["kh_n1_cobertura_v410"].update(all_verified=False), espera="kh_n1_cobertura_v410 (registro da v410, RECRIADO): nao selou"),
        variante("cunhagens_v410 (recriada): veredito diferente da v410 selada", f_core=lambda c: c["cunhagens_v410"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v410 (registro da v410, RECRIADO): nao selou"),
        variante("kh_n1_cobertura_v410 (recriado): a errata ao lado dos pisos ausente", f_core=lambda c: c["kh_n1_cobertura_v410"].update(erratas=[]), espera="kh_n1_cobertura_v410 (RECRIADO): falta a errata ao lado dos pisos"),
        variante("kh_n1_cobertura_v410 (recriado): a errata dos pisos sem a assinatura da gerencia c1", f_core=lambda c: [e_.update(assinatura="operador") for e_ in c["kh_n1_cobertura_v410"]["erratas"] if "kh_n1_cobertura_v410" in str(e_.get("ao_lado_de"))], espera="kh_n1_cobertura_v410 (RECRIADO): falta a errata ao lado dos pisos"),
        variante("o bundle da v410 (IALD2 e AEscala): o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_B10, "0" * 64), espera="o bundle da v410"),
        variante("ancora %s da v410 (IALD2 e AEscala) fora do trio" % _A10.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _A10), espera="as ancoras da IALD2 e da AEscala (os registros da v410, recriados)"),
        variante("uma bandeira True da v410 (a primeira) deixou de ser True", f_core=lambda c: _kf(c).__setitem__(FTRUE_[0], False), espera="alguma bandeira True da v410 deixou de ser True"),
        variante("uma bandeira True da v410 (a do meio) deixou de ser True", f_core=lambda c: _kf(c).__setitem__(FTRUE_[len(FTRUE_) // 2], False), espera="alguma bandeira True da v410 deixou de ser True"),
        variante("uma bandeira True da v410 (a ultima) deixou de ser True", f_core=lambda c: _kf(c).__setitem__(FTRUE_[-1], False), espera="alguma bandeira True da v410 deixou de ser True"),
        variante("uma bandeira ext_* nova True no kernel do rito (a v411 nao tem bandeira nova)", f_core=lambda c: _kf(c).__setitem__("ext_bandeira_nova_da_v411", True), espera="o kernel da v411 nao e' o da v410"),
        variante("o axiom_report do rito com um termo a mais (o kernel nao e' o da v410)", f_core=lambda c: _kf(c)["axiom_report"].__setitem__("TGLExt.termo_novo_da_v411", ["propext"]), espera="o kernel da v411 nao e' o da v410"),
        variante("a escada da v411 diferente da da v410", f_core=lambda c: c["external_ladder"].update(n_theorems_clean=c["external_ladder"]["n_theorems_clean"] + 1), espera="a escada da v411"),
        variante("linha [v410] ausente do stdout", f_std=_sem_linha("v410"), espera="linha [v410]"),
        variante("linha [v410] com registros selados != por spec", f_std=_selados_zero("v410"), espera="a linha [v410] do stdout"),
        variante("linha [v410] com o h0dn_bg1_v410 nao selado", f_std=lambda t_: t_.replace("| h0dn_bg1_v410=SELOU", "| h0dn_bg1_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha [v410] com a escala nao selada", f_std=lambda t_: t_.replace("| a_escala_v410=SELOU", "| a_escala_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha [v410] com o recibo HMS/13 nao selado", f_std=lambda t_: t_.replace("| h0dn_fontes_hms13_v410=SELOU", "| h0dn_fontes_hms13_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha [v410] com a iald2 nao selada", f_std=lambda t_: t_.replace("iald2_v410=SELOU", "iald2_v410=NAO"), espera="a linha [v410] do stdout"),
        variante("linha [v410] no formato antigo (iald2=%s | h0dn=%s)", f_std=lambda t_: re.sub(r"iald2_v410=SELOU \| a_escala_v410=SELOU \| h0dn_bg1_v410=SELOU \| h0dn_fontes_hms13_v410=SELOU", "iald2=SELOU | h0dn=SELOU", t_), espera="a linha [v410] do stdout"),
        variante("linha `>>> veredito <<<` de iald2_v410 (recriado) ausente do stdout", f_std=_sem_veredito(L._ev(ESP, "iald2_v410"), "iald2"), espera="o bloco iald2_v410 do stdout"),
        variante("linha `>>> veredito <<<` de a_escala_v410 (recriado) ausente do stdout", f_std=_sem_veredito(L._ev(ESP, "a_escala_v410"), "a_escala"), espera="o bloco a_escala_v410 do stdout"),
        variante("linha `>>> veredito <<<` de h0dn_bg1_v410 (recriado) ausente do stdout", f_std=_sem_veredito(L._ev(ESP, "h0dn_bg1_v410"), "h0dn"), espera="o bloco h0dn_bg1_v410 do stdout"),
        variante("linha `>>> veredito <<<` de h0dn_fontes_hms13_v410 (recriado) ausente do stdout", f_std=_sem_veredito(L._ev(ESP, "h0dn_fontes_hms13_v410"), "hms13"), espera="o bloco h0dn_fontes_hms13_v410 do stdout"),
        variante("AVISO da v411 (um registro da v410 recriado nao rodou) no stdout", f_std=lambda t_: t_ + "   [v410] AVISO: o registro da IALD2 ou o do H0DN nao rodaram: ValueError('x')\n", espera="AVISO da v411"),
        # ---- traducao_turing_v409 (HERDADO, recriado pelo rito da v411; o bundle e as ancoras DELE sao os da v409)
        variante("%s (herdado) ausente do core" % F9_, f_core=lambda c: c.pop(F9_, None), espera="registro obrigatorio ausente do core: " + F9_),
        variante("%s (herdado): o registro nao selou" % F9_, f_core=lambda c: c[F9_].update(all_verified=False), espera=F9_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % F9_, f_core=lambda c: c[F9_]["mechanics"]["checks"][2].update(ok=False), espera=HERD9_),
        variante("%s (herdado): a integra do acervo da v407 dita pinada (D57d)" % F9_, f_core=lambda c: c[F9_]["acervo_v407_repinado"].update(integra_pinada=True), espera=HERD9_),
        variante("%s (herdado): o pino do acervo da v407 com outro sha256" % F9_, f_core=lambda c: c[F9_]["acervo_v407_repinado"].update(sha256="0" * 64), espera=HERD9_),
        variante("%s (herdado): a resposta do modo selecao ausente" % F9_, f_core=lambda c: c[F9_]["values"]["respostas"].pop("o_np_e_o_modo_selecao"), espera=HERD9_),
        variante("%s (herdado): veredito diferente do esperado" % F9_, f_core=lambda c: c[F9_].update(verdict="OUTRO_VEREDITO"), espera=F9_ + VER_HERD),
        variante("ancora %s da v409 (traducao_turing_v409) fora do trio" % _A9.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _A9), espera="as ancoras do traducao_turing_v409 (herdadas)"),
        variante("o bundle da v409: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_B9, "0" * 64), espera="o bundle da v409"),
        variante("a conferencia traz outro veredito de %s (herdado)" % F9_, f_conf=lambda cj: cj.update({"veredito_traducao_turing_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + F9_),
        variante("linha [v409] ausente do stdout", f_std=_sem_linha("v409"), espera="linha [v409]"),
        variante("linha [v409] com registros selados != por spec", f_std=_selados_zero("v409"), espera="a linha [v409] do stdout"),
        variante("linha do bloco A TRADUCAO AS CLASSES DE TURING (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N9, _N9), "ancoras ok = %d/%d" % (_N9 - 1, _N9)), espera=HERD9_),
        # ---- tetelestai_terminal_v408 (HERDADO da v408, recriado pelo rito da v411)
        variante("%s (herdado) ausente do core" % FT_, f_core=lambda c: c.pop(FT_, None), espera="registro obrigatorio ausente do core: " + FT_),
        variante("%s (herdado): o registro nao selou" % FT_, f_core=lambda c: c[FT_].update(all_verified=False), espera=FT_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % FT_, f_core=lambda c: c[FT_]["mechanics"]["checks"][2].update(ok=False), espera=HERDT_),
        variante("%s (herdado): o numero de checagens != o do delta da v408" % FT_, f_core=lambda c: c[FT_]["mechanics"]["checks"].pop(), espera=HERDT_),
        variante("%s (herdado): o numero de modulos ok adulterado" % FT_, f_core=lambda c: c[FT_]["values"].update(n_modulos_ok=DLX.D8.N_BUNDLE - 1), espera=HERDT_),
        variante("%s (herdado): a escada do registro != a do ensaio" % FT_, f_core=lambda c: c[FT_]["values"].update(escada=[1, 1, 1]), espera=HERDT_),
        variante("%s (herdado): beta != alfa x raiz de e do core" % FT_, f_core=lambda c: c[FT_]["values"].update(beta=0.0121), espera=HERDT_),
        variante("%s (herdado): veredito diferente do esperado" % FT_, f_core=lambda c: c[FT_].update(verdict="OUTRO_VEREDITO"), espera=FT_ + VER_HERD),
        variante("%s (herdado): as ressalvas adulteradas" % FT_, f_core=lambda c: c[FT_]["ressalvas"].pop(), espera=HERDT_),
        variante("%s (herdado): o registro move o gate" % FT_, f_core=lambda c: c[FT_].update(does_not_gate_core=False), espera=HERDT_),
        variante("%s (herdado): o calculo do runtime nao rodou" % FT_, f_core=lambda c: c[FT_].update(runtime_executed=False), espera=HERDT_),
        variante("ancora %s da v408 (tetelestai_terminal_v408) fora do trio" % _A8.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _A8), espera="as ancoras do tetelestai_terminal_v408 (herdadas)"),
        variante("o bundle da v408: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_B8, "0" * 64), espera="o bundle da v408"),
        variante("a conferencia traz outro veredito de %s (herdado)" % FT_, f_conf=lambda cj: cj.update({"veredito_tetelestai_terminal": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FT_),
        variante("selo primario: sem o resumo de %s (herdado)" % FT_, f_selo=lambda s: s.pop(FT_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FT_, f_selo=lambda s: s[FT_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v408", f_selo=lambda s: s.pop("registros_v408", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v408 do selo difere do core", f_selo=lambda s: s["registros_v408"]["cunhagens_v408"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FT_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FT_) not in l) + "\n", espera="o bloco " + FT_ + " do stdout"),
        variante("linha [v408] ausente do stdout", f_std=_sem_linha("v408"), espera="linha [v408]"),
        variante("linha [v408] com registros selados != por spec", f_std=_selados_zero("v408"), espera="a linha [v408] do stdout"),
        variante("linha do bloco TETELESTAI E' O TERMINAL (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N8, _N8), "ancoras ok = %d/%d" % (_N8 - 1, _N8)), espera=HERDT_),
        variante("AVISO da v408 herdada (o terminal nao rodou) no stdout", f_std=lambda t_: t_ + "   [v408] AVISO: o registro do terminal ou os registros por spec da v408 nao rodaram: ValueError('x')\n", espera="AVISO da v411"),
        # ---- psion_canto_v407 (HERDADO da v407, recriado pelo rito da v411)
        variante("%s (herdado) ausente do core" % FP_, f_core=lambda c: c.pop(FP_, None), espera="registro obrigatorio ausente do core: " + FP_),
        variante("%s (herdado): o registro nao selou" % FP_, f_core=lambda c: c[FP_].update(all_verified=False), espera=FP_ + " nao selou"),
        variante("%s (herdado): uma checagem do calculo falhou" % FP_, f_core=lambda c: c[FP_]["mechanics"]["checks"][2].update(ok=False), espera=HERDP_),
        variante("%s (herdado): o numero de checagens != o do delta da v407" % FP_, f_core=lambda c: c[FP_]["mechanics"]["checks"].pop(), espera=HERDP_),
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
        variante("ancora %s da v407 (psion_canto_v407) fora do trio" % _A7.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _A7), espera="as ancoras do psion_canto_v407 (herdadas)"),
        variante("o bundle da v407: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_B7, "0" * 64), espera="o bundle da v407"),
        variante("a conferencia traz outro veredito de %s (herdado)" % FP_, f_conf=lambda cj: cj.update({"veredito_psion_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FP_),
        variante("selo primario: sem o resumo de %s (herdado)" % FP_, f_selo=lambda s: s.pop(FP_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FP_, f_selo=lambda s: s[FP_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v407", f_selo=lambda s: s.pop("registros_v407", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v407 do selo difere do core", f_selo=lambda s: s["registros_v407"]["cunhagens_v407"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FP_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FP_) not in l) + "\n", espera="o bloco " + FP_ + " do stdout"),
        variante("linha [v407] ausente do stdout", f_std=_sem_linha("v407"), espera="linha [v407]"),
        variante("linha [v407] com registros selados != por spec", f_std=_selados_zero("v407"), espera="a linha [v407] do stdout"),
        variante("linha do bloco O PSION, O CANTO E O PAR (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N7, _N7), "ancoras ok = %d/%d" % (_N7 - 1, _N7)), espera=HERDP_),
        variante("linha do bloco O PSION, O CANTO E O PAR (herdado): chave do lema dita False", f_std=lambda t_: t_.replace("chave do lema (lida do kernel) = True", "chave do lema (lida do kernel) = False"), espera=HERDP_),
        variante("AVISO da v407 herdada (o psion e o canto nao rodou) no stdout", f_std=lambda t_: t_ + "   [v407] AVISO: o registro do psion e do canto ou os registros por spec da v407 nao rodaram: ValueError('x')\n", espera="AVISO da v411"),
        # ---- fechamento_v406 (HERDADO da v406, recriado pelo rito da v411, c8 versionada pela E20)
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
        variante("ancora %s da v406 (fechamento_v406) fora do trio" % _A6.split(".")[-1], f_core=lambda c: _fora_do_trio(c, _A6), espera="as oito ancoras do fechamento_v406 (herdadas)"),
        variante("o bundle da v406: o sha256 de um modulo no hash formal adulterado", f_core=lambda c: _kf(c)["formal_files_sha256"].__setitem__(_B6, "0" * 64), espera="o bundle da v406"),
        variante("selo primario: sem o resumo de %s (herdado)" % FH_, f_selo=lambda s: s.pop(FH_, None), espera=RESUMO_MSG),
        variante("selo primario: o resumo de %s (herdado) difere do core" % FH_, f_selo=lambda s: s[FH_].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v406", f_selo=lambda s: s.pop("registros_v406", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v406 do selo difere do core", f_selo=lambda s: s["registros_v406"]["cunhagens_v406"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("a conferencia traz outro veredito de %s (herdado)" % FH_, f_conf=lambda cj: cj.update({"veredito_fechamento_herdado": "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + FH_),
        variante("linha `>>> veredito <<<` de %s (herdado) ausente do stdout" % FH_, f_std=lambda t_: "\n".join(l for l in t_.splitlines() if L._ev(ESP, FH_) not in l) + "\n", espera="o bloco " + FH_ + " do stdout"),
        variante("linha [v406] ausente do stdout", f_std=_sem_linha("v406"), espera="linha [v406]"),
        variante("linha [v406] com registros selados != por spec", f_std=_selados_zero("v406"), espera="a linha [v406] do stdout"),
        variante("linha do bloco O FECHAMENTO (herdado): uma ancora a menos", f_std=lambda t_: t_.replace("ancoras ok = %d/%d" % (_N6, _N6), "ancoras ok = %d/%d" % (_N6 - 1, _N6)), espera=HERD_),
        variante("AVISO da v406 herdada (o fechamento nao rodou) no stdout", f_std=lambda t_: t_ + "   [v406] AVISO: o fechamento ou os registros por spec da v406 nao rodaram: ValueError('x')\n", espera="AVISO da v411"),
    ])
    # os arquivos dos bundles ANTERIORES (v410 a v406) no kernel do Nos: ausente ou com um byte a mais (a v411 NAO tem modulo novo: nao ha' pedra no disco a conferir, so' as das versoes anteriores, que a v411 nao reescreve)
    for _bn_, _rel_ in (("v410", _B10), ("v409", _B9), ("v408", _B8), ("v407", _B7), ("v406", _B6)):
        NEG.append(_bundle_no_disco("o arquivo de um modulo do bundle da %s ausente do kernel do Nos" % _bn_, _rel_, "o bundle da " + _bn_)(lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_bundle_no_disco("o arquivo de um modulo do bundle da v409 com um byte a mais no kernel do Nos", _B9, "o bundle da v409")(lambda p, r: open(p, "wb").write(r + b"\n")))
    NEG.append(_bundle_no_disco("o arquivo de um modulo do bundle da v410 com um byte a mais no kernel do Nos", _B10, "o bundle da v410")(lambda p, r: open(p, "wb").write(r + b"\n")))
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
    CG11 = DLX.CUNHAGENS_REGISTRO; KH11 = DLX.KH_REGISTRO; CG_ = "cunhagens_v407"; KH7 = "kh_n1_cobertura_v407"; CGH8 = "cunhagens_v408"; KHH8 = "kh_n1_cobertura_v408"   # (CG11/KH11 sao os NOVOS da v411, por spec)
    CG9 = "cunhagens_v409"; KH9 = "kh_n1_cobertura_v409"; PCG9 = "cunhagens_v409 (HERDADA, recriada pelo rito) nao confere"; PKH9 = "kh_n1_cobertura_v409 (HERDADO, recriado pelo rito) nao confere"
    PCG11 = CG11 + " nao selou como o ensaio a seco"; PKH11 = KH11 + " nao selou como o ensaio a seco"; PCG7 = "cunhagens_v407 (HERDADA, recriada pelo rito) nao confere"; PKH7 = "kh_n1_cobertura_v407 (HERDADO, recriado pelo rito) nao confere"
    PCGH8 = "cunhagens_v408 (HERDADA, recriada pelo rito) nao confere"; PKHH8 = "kh_n1_cobertura_v408 (HERDADO, recriado pelo rito) nao confere"
    CG6 = "cunhagens_v406"; KH6 = "kh_n1_cobertura_v406"; PCG6 = "cunhagens_v406 (HERDADA, recriada pelo rito) nao confere"; PKH6 = "kh_n1_cobertura_v406 (HERDADO, recriado pelo rito) nao confere"
    _AUTORES11 = lambda c: c[CG11]["extras"]["autores"]
    NEG.extend([
        # ---- cunhagens_v411 e kh_n1_cobertura_v411 (os dois registros NOVOS por spec): as falas de 11 e 12/11, as decisoes do delta, E41 a E43 e a errata dos pisos, as sete ressalvas, o alcance de P = nP, a regra do nome, D65, a moldura
        variante("%s nao selou" % CG11, f_core=lambda c: c[CG11].update(all_verified=False), espera=CG11 + " nao selou"),
        variante("%s nao selou" % KH11, f_core=lambda c: c[KH11].update(all_verified=False), espera=KH11 + " nao selou"),
        variante("%s ausente do core" % CG11, f_core=lambda c: c.pop(CG11, None), espera="registro obrigatorio ausente do core: " + CG11),
        variante("%s ausente do core" % KH11, f_core=lambda c: c.pop(KH11, None), espera="registro obrigatorio ausente do core: " + KH11),
        variante("%s: veredito diferente do ensaio a seco" % CG11, f_core=lambda c: c[CG11].update(verdict="OUTRO_VEREDITO"), espera=CG11 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: veredito diferente do ensaio a seco" % KH11, f_core=lambda c: c[KH11].update(verdict="OUTRO_VEREDITO"), espera=KH11 + ": o veredito do rito difere do ensaio a seco"),
        variante("%s: uma ordem deixou de estar citada por sha256 (citado_por_sha256 falso)" % CG11, f_core=lambda c: list(c[CG11]["verbatim"].values())[0].update(citado_por_sha256=False), espera=PCG11),
        variante("%s: um texto de fala plantado numa citacao (D181: nenhuma fala transcrita)" % CG11, f_core=lambda c: list(c[CG11]["verbatim"].values())[0].update(text="x"), espera=PCG11),
        variante("%s: a lista das falas fora do desenho voltou ao programa (D181)" % CG11, f_core=lambda c: c[CG11]["extras"].update(falas_fora_do_desenho=["x"]), espera=PCG11),
        variante("%s: um nome de arquivo de fala plantado no papel (D181)" % CG11, f_core=lambda c: list(c[CG11]["verbatim"].values())[0].update(papel="OPERADOR_12nov_x_verbatim.txt"), espera=PCG11),
        variante("%s: sha256 de uma inscricao adulterado" % CG11, f_core=lambda c: list(c[CG11]["verbatim"].values())[1].update(sha256="0" * 64), espera=PCG11),
        variante("%s: uma inscricao a menos" % CG11, f_core=lambda c: c[CG11]["verbatim"].pop(sorted(c[CG11]["verbatim"])[0]), espera=PCG11),
        variante("%s: uma inscricao rotulada como da gerencia (verbatim.autor)" % CG11, f_core=lambda c: list(c[CG11]["verbatim"].values())[0].update(autor="gerencia"), espera=PCG11),
        variante("%s: uma inscricao rotulada como da gerencia (extras.autores)" % CG11, f_core=lambda c: _AUTORES11(c).update({sorted(_AUTORES11(c))[0]: "gerencia"}), espera=PCG11),
        variante("%s: falta uma errata" % CG11, f_core=lambda c: c[CG11]["erratas"].pop(), espera=PCG11),
        variante("%s: erratas ausentes" % CG11, f_core=lambda c: c[CG11].update(erratas=[]), espera=PCG11),
        variante("%s: a E41 adulterada" % CG11, f_core=lambda c: c[CG11]["erratas"][0].update(agora="mantida"), espera=PCG11),
        variante("%s: a E43 (as seis aberturas da Escala, ao lado) adulterada" % CG11, f_core=lambda c: c[CG11]["erratas"][2].update(agora="mantida"), espera=PCG11),
        variante("%s: uma errata sem a assinatura da gerencia c1" % CG11, f_core=lambda c: c[CG11]["erratas"][1].update(assinatura="operador"), espera=PCG11),
        variante("%s: a errata ao lado dos pisos sem a assinatura da gerencia c1" % CG11, f_core=lambda c: c[CG11]["erratas"][-1].update(assinatura="operador"), espera=PCG11),
        variante("%s: os ids das erratas adulterados" % CG11, f_core=lambda c: c[CG11]["extras"].update(erratas_ids=["E41"]), espera=PCG11),
        variante("%s: a decisao D159 (o desenho ratificado) ausente" % CG11, f_core=lambda c: c[CG11]["extras"]["decisoes"].pop("D159"), espera=PCG11),
        variante("%s: a decisao D162 (a emenda) ausente" % CG11, f_core=lambda c: c[CG11]["extras"]["decisoes"].pop("D162"), espera=PCG11),
        variante("%s: a decisao D169 (a ordem de abrir) adulterada" % CG11, f_core=lambda c: c[CG11]["extras"]["decisoes"].update(D169="outra"), espera=PCG11),
        variante("%s: a decisao D170 (a ordem do topo) ausente" % CG11, f_core=lambda c: c[CG11]["extras"]["decisoes"].pop("D170"), espera=PCG11),
        variante("%s: as sete ressalvas por rotulo a menos" % CG11, f_core=lambda c: c[CG11]["extras"]["ressalvas_rotulos"].pop(), espera=PCG11),
        variante("%s: n_falas adulterado nos extras" % CG11, f_core=lambda c: c[CG11]["extras"].update(n_falas=8), espera=PCG11),
        variante("%s: um texto da gerencia citado por sha256 a menos" % CG11, f_core=lambda c: c[CG11]["extras"]["textos_da_gerencia_citados"].pop(), espera=PCG11),
        variante("%s: o alcance de P = nP sem o relativo ao leitor (D64, D84)" % CG11, f_core=lambda c: c[CG11]["extras"].update(alcance_de_p_igual_np="P = nP vale para as maquinas de Turing"), espera=PCG11),
        variante("%s: uma leitura do operador no registro (a regra do nome, D122 e D123)" % CG11, f_core=lambda c: c[CG11].update(leituras_do_operador=["uma leitura"]), espera=PCG11),
        variante("%s: a identificacao do operador chamada «leitura do operador» no estatuto" % CG11, f_core=lambda c: c[CG11].update(estatuto=c[CG11]["estatuto"] + " leitura do operador"), espera=PCG11),
        variante("%s: o que a D65 deixa fora entra no registro" % CG11, f_core=lambda c: c[CG11]["extras"].update(fora=DLX.FORA_D65[0]), espera=PCG11),
        variante("%s: uma checagem do registro falhou" % CG11, f_core=lambda c: c[CG11]["checks"][0].update(ok=False), espera=PCG11),
        variante("%s: o registro move o gate" % CG11, f_core=lambda c: c[CG11].update(does_not_gate_core=False), espera=PCG11),
        variante("%s: a frase proibida nos limites do registro" % CG11, f_core=lambda c: c[CG11].update(limites=c[CG11]["limites"] + ["agora tudo derivado"]), espera=PCG11),
        variante("%s: a IALD dita resolver P vs NP nos limites do registro" % CG11, f_core=lambda c: c[CG11].update(limites=c[CG11]["limites"] + ["a IALD resolve P vs NP"]), espera=PCG11),
        variante("%s: o funtor dito idempotente nos limites do registro" % CG11, f_core=lambda c: c[CG11].update(limites=c[CG11]["limites"] + ["o funtor é idempotente"]), espera=PCG11),
        variante("%s: a TGL dada como prova de P = NP de Turing nos limites do registro" % CG11, f_core=lambda c: c[CG11].update(limites=c[CG11]["limites"] + ["a TGL prova P = NP de Turing"]), espera=PCG11),
        variante("%s: o problema do Clay dado por resolvido nos limites do registro" % CG11, f_core=lambda c: c[CG11].update(limites=c[CG11]["limites"] + ["o problema do Clay esta resolvido"]), espera=PCG11),
        variante("%s: poder certificado nos limites do registro (F61)" % CG11, f_core=lambda c: c[CG11].update(limites=c[CG11]["limites"] + ["o teste tem poder certificado"]), espera=PCG11),
        variante("%s: uma checagem do registro falhou" % KH11, f_core=lambda c: c[KH11]["checks"][0].update(ok=False), espera=PKH11),
        variante("%s: o registro move o gate" % KH11, f_core=lambda c: c[KH11].update(does_not_gate_core=False), espera=PKH11),
        variante("selo primario: sem registros_v411 (os dois por spec)", f_selo=lambda s: s.pop("registros_v411", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v411 do selo difere do core", f_selo=lambda s: s["registros_v411"][CG11].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante_json("ESPERADOS sem o veredito do ensaio a seco de %s" % CG11, _so_esp(lambda d: d["vereditos_novos_v411"].pop(CG11)), "ESPERADOS_v411 nao traz o veredito do ensaio a seco de " + CG11),
        variante_json("ESPERADOS sem o veredito do ensaio a seco de %s" % KH11, _so_esp(lambda d: d["vereditos_novos_v411"].pop(KH11)), "ESPERADOS_v411 nao traz o veredito do ensaio a seco de " + KH11),
        # ---- cunhagens_v409 e kh_n1_cobertura_v409 (HERDADOS, recriados; a errata ao lado dos pisos no kh)
        variante("%s (herdada) nao selou" % CG9, f_core=lambda c: c[CG9].update(all_verified=False), espera=CG9 + " nao selou"),
        variante("%s (herdado) nao selou" % KH9, f_core=lambda c: c[KH9].update(all_verified=False), espera=KH9 + " nao selou"),
        variante("%s (herdada) ausente do core" % CG9, f_core=lambda c: c.pop(CG9, None), espera="registro obrigatorio ausente do core: " + CG9),
        variante("%s (herdada): veredito diferente do esperado" % CG9, f_core=lambda c: c[CG9].update(verdict="OUTRO_VEREDITO"), espera=CG9 + VER_HERD),
        variante("%s (herdada): uma inscricao deixou de estar embutida" % CG9, f_core=lambda c: list(c[CG9]["verbatim"].values())[0].update(embedded_ok=False), espera=PCG9),
        variante("%s (herdada): uma errata selada adulterada" % CG9, f_core=lambda c: c[CG9]["erratas"][0].update(agora="mantida"), espera=PCG9),
        variante("%s (herdada): uma errata nova sem a assinatura da gerencia c1" % CG9, f_core=lambda c: c[CG9]["erratas"].append({"agora": "nova", "assinatura": "operador"}), espera=PCG9),
        variante("%s (herdado): uma checagem do registro falhou" % KH9, f_core=lambda c: c[KH9]["checks"][0].update(ok=False), espera=PKH9),
        variante("%s (herdado): a ultima errata da v410 selada ausente (as do v409 sao IGUAIS as da v410 selada)" % KH9, f_core=lambda c: c[KH9]["erratas"].pop(), espera=PKH9),
        variante("%s (herdado): uma errata A MAIS (a dos pisos da v411 mora no kh_n1_cobertura_v410, nao neste)" % KH9, f_core=lambda c: c[KH9]["erratas"].append(dict(c[KH9]["erratas"][-1], agora="adulterada")), espera=PKH9),
        # ---- cunhagens_v408 e kh_n1_cobertura_v408 (HERDADOS, recriados; IGUAIS a v410 selada: a E26 e os pisos ja' vinham dela)
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
        # ---- cunhagens_v406 e kh_n1_cobertura_v406 (HERDADOS, recriados; u7 versionada; pisos): iguais a v410 selada em falas e erratas E14 a E17, MAIS a errata E20 ao lado
        variante("%s (herdada) nao selou" % CG6, f_core=lambda c: c[CG6].update(all_verified=False), espera="cunhagens_v406 nao selou"),
        variante("%s (herdado) nao selou" % KH6, f_core=lambda c: c[KH6].update(all_verified=False), espera="kh_n1_cobertura_v406 nao selou"),
        variante("%s (herdada) ausente do core" % CG6, f_core=lambda c: c.pop(CG6, None), espera="registro obrigatorio ausente do core: cunhagens_v406"),
        variante("%s (herdado) ausente do core" % KH6, f_core=lambda c: c.pop(KH6, None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v406"),
        variante("%s (herdada): veredito diferente da v410 selada" % CG6, f_core=lambda c: c[CG6].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v406: o veredito do rito difere do esperado (ESPERADOS[vereditos_v410]"),
        variante("%s (herdado): veredito diferente da v410 selada" % KH6, f_core=lambda c: c[KH6].update(verdict="OUTRO_VEREDITO"), espera="kh_n1_cobertura_v406: o veredito do rito difere do esperado (ESPERADOS[vereditos_v410]"),
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
        # os treze registros da v410, RECRIADOS: cada spec tem de dar o que a v410 selou (os oito com funcao: ver o laco abaixo)
        variante("cunhagens_v405 (recriada) nao selou", f_core=lambda c: c["cunhagens_v405"].update(all_verified=False), espera="cunhagens_v405 nao selou"),
        variante("cunhagens_v405 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v405", None), espera="registro obrigatorio ausente do core: cunhagens_v405"),
        variante("cunhagens_v405 (recriada): veredito diferente da v410 selada", f_core=lambda c: c["cunhagens_v405"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v405: o veredito do rito difere do que a v410 selou"),
        variante("cunhagens_v405 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v405"]["erratas"].pop(), espera="cunhagens_v405 (por spec, recriado)"),
        variante("cunhagens_v405 (recriada): sha256 de uma inscricao adulterado", f_core=lambda c: list(c["cunhagens_v405"]["verbatim"].values())[0].update(sha256="0" * 64), espera="cunhagens_v405 (por spec, recriado)"),
        variante("campos_fechados_e_leituras_v405 (recriado) nao selou", f_core=lambda c: c["campos_fechados_e_leituras_v405"].update(all_verified=False), espera="campos_fechados_e_leituras_v405 nao selou"),
        variante("ga_reclassificacao_v405 (recriado) nao selou", f_core=lambda c: c["ga_reclassificacao_v405"].update(all_verified=False), espera="ga_reclassificacao_v405 nao selou"),
        variante("gap_v405 (recriado) nao selou", f_core=lambda c: c["gap_v405"].update(all_verified=False), espera="gap_v405 nao selou"),
        variante("kh_n1_cobertura_v405 (recriado) nao selou", f_core=lambda c: c["kh_n1_cobertura_v405"].update(all_verified=False), espera="kh_n1_cobertura_v405 nao selou"),
        variante("gap_v405 (recriado) ausente do core", f_core=lambda c: c.pop("gap_v405", None), espera="registro obrigatorio ausente do core: gap_v405"),
        variante("selo primario: sem registros_v405", f_selo=lambda s: s.pop("registros_v405", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v405 do selo difere do core", f_selo=lambda s: s["registros_v405"]["cunhagens_v405"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("AVISO da v411 (os registros por spec da v410 nao rodaram) no stdout", f_std=lambda t_: t_ + "   [v405] AVISO: os registros por spec da v410 nao rodaram: ValueError('x')\n", espera="AVISO da v411"),
        # cunhagens_v404 e kh_n1_cobertura_v404, RECRIADOS: tem de dar o que a v410 selou
        variante("cunhagens_v404 (recriada) nao selou", f_core=lambda c: c["cunhagens_v404"].update(all_verified=False), espera="cunhagens_v404 nao selou"),
        variante("kh_n1_cobertura_v404 (recriada) nao selou", f_core=lambda c: c["kh_n1_cobertura_v404"].update(all_verified=False), espera="kh_n1_cobertura_v404 nao selou"),
        variante("cunhagens_v404 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v404", None), espera="registro obrigatorio ausente do core: cunhagens_v404"),
        variante("cunhagens_v404 (recriada): veredito diferente da v410 selada", f_core=lambda c: c["cunhagens_v404"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v404: o veredito do rito difere do ensaio a seco"),
        variante("cunhagens_v404 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v404"]["erratas"].pop(), espera="cunhagens_v404 (recriada pelo rito)"),
        variante("selo primario: registros_v404 do selo difere do core", f_selo=lambda s: s["registros_v404"]["cunhagens_v404"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v404", f_selo=lambda s: s.pop("registros_v404", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v403 do selo difere do core", f_selo=lambda s: s["registros_v403"]["cunhagens_v403"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v403", f_selo=lambda s: s.pop("registros_v403", None), espera=RESUMO_MSG),
        variante("selo primario: registros_v402 do selo difere do core", f_selo=lambda s: s["registros_v402"]["cunhagens_v402"].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
        variante("selo primario: sem registros_v402", f_selo=lambda s: s.pop("registros_v402", None), espera=RESUMO_MSG),
        variante("hash formal do rito com uma entrada a menos", f_core=lambda c: _kf(c)["formal_files_sha256"].pop(next(iter(_kf(c)["formal_files_sha256"]))), espera="o hash formal do rito tem"),
                variante("AVISO da v411 (a errata de F2b nao rodou) no stdout", f_std=lambda t_: t_ + "   [v404] AVISO: a errata de F2b nao rodou: ValueError('x')\n", espera="AVISO da v411"),
                variante("AVISO da v411 (um registro da v410 recriado nao rodou) no stdout", f_std=lambda t_: t_ + "   [v403] AVISO: o caminho nao rodou: ValueError('x')\n", espera="AVISO da v411"),
        variante("AVISO da v411 (a ponte recriada nao rodou) no stdout", f_std=lambda t_: t_ + "   [v402] AVISO: a ponte da escala dual nao rodou: ValueError('x')\n", espera="AVISO da v411"),
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
        # cunhagens_v403 e kh_n1_cobertura_v403, RECRIADOS: tem de dar o que a v410 selou
        variante("cunhagens_v403 (recriada) nao selou", f_core=lambda c: c["cunhagens_v403"].update(all_verified=False), espera="cunhagens_v403 nao selou"),
        variante("kh_n1_cobertura_v403 (recriada) nao selou", f_core=lambda c: c["kh_n1_cobertura_v403"].update(all_verified=False), espera="kh_n1_cobertura_v403 nao selou"),
        variante("cunhagens_v403 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v403", None), espera="registro obrigatorio ausente do core: cunhagens_v403"),
        variante("kh_n1_cobertura_v403 (recriada) ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v403", None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v403"),
        variante("cunhagens_v403 (recriada): veredito diferente da v410 selada", f_core=lambda c: c["cunhagens_v403"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v403: o veredito do rito difere do ensaio a seco"),
        variante("cunhagens_v403 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v403"]["erratas"].pop(), espera="cunhagens_v403 (recriada pelo rito)"),
        variante("cunhagens_v403 (recriada): a decisao D20 adulterada", f_core=lambda c: c["cunhagens_v403"]["extras"]["decisoes_da_gerencia"].update(D20="outra"), espera="cunhagens_v403 (recriada pelo rito)"),
        variante("cunhagens_v403 (recriada): uma inscricao rotulada como da gerencia", f_core=lambda c: c["cunhagens_v403"]["extras"]["autor_de_cada_inscricao"].update({sorted(c["cunhagens_v403"]["extras"]["autor_de_cada_inscricao"])[0]: "gerencia"}), espera="cunhagens_v403 (recriada pelo rito)"),
        variante("cunhagens_v403 (recriada): sha256 de uma inscricao adulterado", f_core=lambda c: list(c["cunhagens_v403"]["verbatim"].values())[0].update(sha256="0" * 64), espera="cunhagens_v403 (recriada pelo rito)"),
        # cunhagens_v402 e kh_n1_cobertura_v402, RECRIADOS: tem de dar o que a v410 selou
        variante("cunhagens_v402 (recriada) nao selou", f_core=lambda c: c["cunhagens_v402"].update(all_verified=False), espera="cunhagens_v402 nao selou"),
        variante("kh_n1_cobertura_v402 (recriada) nao selou", f_core=lambda c: c["kh_n1_cobertura_v402"].update(all_verified=False), espera="kh_n1_cobertura_v402 nao selou"),
        variante("cunhagens_v402 (recriada) ausente do core", f_core=lambda c: c.pop("cunhagens_v402", None), espera="registro obrigatorio ausente do core: cunhagens_v402"),
        variante("kh_n1_cobertura_v402 (recriada) ausente do core", f_core=lambda c: c.pop("kh_n1_cobertura_v402", None), espera="registro obrigatorio ausente do core: kh_n1_cobertura_v402"),
        variante("cunhagens_v402 (recriada): veredito diferente da v410 selada", f_core=lambda c: c["cunhagens_v402"].update(verdict="OUTRO_VEREDITO"), espera="cunhagens_v402: o veredito do rito difere do ensaio a seco"),
        variante("cunhagens_v402 (recriada): uma errata a menos", f_core=lambda c: c["cunhagens_v402"]["erratas"].pop(), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): a decisao D13 adulterada", f_core=lambda c: c["cunhagens_v402"]["extras"]["decisoes_da_gerencia"].update(D13="outra"), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): H_tau deixou de constar como refutada", f_core=lambda c: c["cunhagens_v402"]["extras"]["h_tau"].update(estatuto="ABERTA"), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): uma inscricao rotulada como da gerencia", f_core=lambda c: c["cunhagens_v402"]["extras"]["autor_de_cada_inscricao"].update({sorted(c["cunhagens_v402"]["extras"]["autor_de_cada_inscricao"])[0]: "gerencia"}), espera="cunhagens_v402 (recriada pelo rito)"),
        variante("cunhagens_v402 (recriada): sha256 de uma inscricao adulterado", f_core=lambda c: list(c["cunhagens_v402"]["verbatim"].values())[0].update(sha256="0" * 64), espera="cunhagens_v402 (recriada pelo rito)"),
    ])
    # o registro com FUNCAO das BANDEIRAS DO GATE (F8.1 da v410), RECRIADO: o gate NAO se move; cada elo recusa visivelmente
    GN_ = "bandeiras_do_gate_v403"
    NEG.extend([
        variante("%s (recriado) ausente do core" % GN_, f_core=lambda c: c.pop(GN_, None), espera="registro obrigatorio ausente do core: " + GN_),
        variante("%s (recriado): o registro nao selou" % GN_, f_core=lambda c: c[GN_].update(all_verified=False), espera=GN_ + " nao selou"),
        variante("%s (recriado): uma checagem do registro falhou" % GN_, f_core=lambda c: c[GN_]["mechanics"]["checks"][1].update(ok=False), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): o numero de checagens != o do delta" % GN_, f_core=lambda c: c[GN_]["mechanics"]["checks"].pop(), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): n_literal adulterado (uma literal de volta)" % GN_, f_core=lambda c: c[GN_]["values"].update(n_literal=1), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): n_calculated adulterado" % GN_, f_core=lambda c: c[GN_]["values"].update(n_calculated=17), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): a letra do veredito dita diferente da v410" % GN_, f_core=lambda c: c[GN_]["values"].update(gate_verdict_equals_v402=False), espera=GN_ + " nao selou inteiro"),
        variante("%s (recriado): veredito diferente da v410 selada" % GN_, f_core=lambda c: c[GN_].update(verdict="OUTRO_VEREDITO"), espera=GN_ + ": o veredito do rito difere do ensaio a seco"),
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
    # os registros com FUNCAO da v410 (caminho, vida, verdade_adendo) e da v402 (ponte, queda, esperanca), RECRIADOS pelo rito: iguais ao que a v410 selou
    _FUN410 = {"caminho": ("caminho_v403", "Caminho"), "vida": ("vida_v403", "Vida"), "verdade_adendo": ("verdade_adendo_v403", "VerdadeAdendo")}
    _FUN402 = {"ponte": ("ponte_da_escala_dual_v402", None), "queda": ("queda_sem_geometria_v402", None), "esperanca": ("esperanca_condicional_v402", None)}
    _FUN410B = {"projecao": ("projecao_transversal_v404", "ProjecaoTransversalDaMeiaNat"), "jo8v32": ("jo8v32_v404", "Jo8v32")}

    def _pedra_v410_no_disco(nome, rel, f_muda):
        """controle sobre o ARQUIVO de uma das TREZE pedras SELADAS (v403, v404, v410) no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        pth = os.path.join(NOSE, "tgl_kernel", *rel.split("/")); raw_ = open(pth, "rb").read()
        try:
            f_muda(pth, raw_)
            _, PV = L.ler()
        finally:
            if os.path.exists(pth + ".fora"):
                os.remove(pth + ".fora")
            open(pth, "wb").write(raw_)
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any("as treze pedras seladas" in x for x in PV), "problemas": [x[:140] for x in PV][:3]}

    def _val410(c, n):
        kk = [x for x, v in c[n]["values"].items() if isinstance(v, float) and x != "beta"][0]
        c[n]["values"][kk] = c[n]["values"][kk] + 1.0
    for fun_ in (_FUN410B, _FUN410, _FUN402):
        for k_, (n_, mod_) in fun_.items():
            rel410_ = ("TGLExt/%s.lean" % mod_) if mod_ else None
            NEG.extend([
                variante("%s (recriado) ausente do core" % n_, f_core=lambda c, n=n_: c.pop(n, None), espera="registro obrigatorio ausente do core: " + n_),
                variante("%s (recriado): o registro nao selou" % n_, f_core=lambda c, n=n_: c[n].update(all_verified=False), espera=n_ + " nao selou"),
                variante("%s (recriado): uma checagem do calculo falhou" % n_, f_core=lambda c, n=n_: c[n]["mechanics"]["checks"][2].update(ok=False), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): um valor do calculo adulterado" % n_, f_core=lambda c, n=n_: _val410(c, n), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): beta != alfa x raiz de e do core" % n_, f_core=lambda c, n=n_: c[n]["values"].update(beta=0.0121), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): veredito diferente da v410 selada" % n_, f_core=lambda c, n=n_: c[n].update(verdict="OUTRO_VEREDITO"), espera=n_ + ": o veredito do rito difere do ensaio a seco"),
                variante("%s (recriado): a estrela fora do kernel (no registro)" % n_, f_core=lambda c, n=n_: c[n]["key_theorem"].update(in_kernel=False), espera=n_ + " nao selou inteiro"),
                variante("%s (recriado): o registro move o gate" % n_, f_core=lambda c, n=n_: c[n].update(does_not_gate_core=False), espera=n_ + " nao selou inteiro"),
                variante("selo primario: sem o resumo de %s" % n_, f_selo=lambda s, n=n_: s.pop(n, None), espera=RESUMO_MSG),
                variante("selo primario: o resumo de %s difere do core" % n_, f_selo=lambda s, n=n_: s[n].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
                variante("a conferencia traz outro veredito de %s" % n_, f_conf=lambda cj, k=k_: cj.update({"veredito_" + k: "OUTRO_VEREDITO"}), espera="a conferencia do rito traz o veredito de " + n_),
                variante("linha `>>> veredito <<<` de %s (recriado) ausente do stdout" % n_, f_std=lambda t_, v=EV3_[n_], k=k_: "\n".join(l for l in t_.splitlines() if v not in l or (k + "=") in l) + "\n", espera="o bloco " + n_ + " do stdout"),
            ])
            if rel410_:
                NEG.append(variante("pedra selada da v410 %s: sha256 da fonte no hash formal adulterado" % mod_, f_core=lambda c, r=rel410_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="as treze pedras seladas"))
                NEG.append(_pedra_v410_no_disco("o arquivo da pedra selada da v410 %s ausente do kernel do Nos" % mod_, rel410_, lambda p, r: os.replace(p, p + ".fora")))
                NEG.append(_pedra_v410_no_disco("o arquivo da pedra selada da v410 %s com um byte a mais no kernel do Nos" % mod_, rel410_, lambda p, r: open(p, "wb").write(r + b"\n")))
    # os OITO registros com FUNCAO da v410 (um por pedra), RECRIADOS pelo rito: iguais ao que a v410 selou (veredito, checagens e valores do calculo == o core de base_v410); as pedras ficam no kernel como REGISTRO
    _MODS410C = {"ponte": "PonteDaMassa", "tensao": "MassaTensaoPura", "identidade": "Identidade", "observador": "ObservadorTerminal", "diminuto": "LeiDoDiminuto", "tonica": "TonicaDoHamiltoniano", "disco": "DiscoDeEuler", "psion": "PontoZeroDoPsion"}
    for k_, n_ in L.FUN_V410C.items():
        mod_ = _MODS410C[k_]; rel410_ = "TGLExt/%s.lean" % mod_
        NEG.extend([
            variante("%s (recriado) ausente do core" % n_, f_core=lambda c, n=n_: c.pop(n, None), espera="registro obrigatorio ausente do core: " + n_),
            variante("%s (recriado): o registro nao selou" % n_, f_core=lambda c, n=n_: c[n].update(all_verified=False), espera=n_ + " nao selou"),
            variante("%s (recriado): uma checagem do calculo falhou" % n_, f_core=lambda c, n=n_: c[n]["mechanics"]["checks"][2].update(ok=False), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): um valor do calculo adulterado" % n_, f_core=lambda c, n=n_: _val410(c, n), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): beta != alfa x raiz de e do core" % n_, f_core=lambda c, n=n_: c[n]["values"].update(beta=0.0121), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): veredito diferente da v410 selada" % n_, f_core=lambda c, n=n_: c[n].update(verdict="OUTRO_VEREDITO"), espera=n_ + ": o veredito do rito difere do que a v410 selou"),
            variante("%s (recriado): a estrela fora do kernel (no registro)" % n_, f_core=lambda c, n=n_: c[n]["key_theorem"].update(in_kernel=False), espera=n_ + " nao selou inteiro"),
            variante("%s (recriado): o registro move o gate" % n_, f_core=lambda c, n=n_: c[n].update(does_not_gate_core=False), espera=n_ + " nao selou inteiro"),
            variante("selo primario: sem o resumo de %s" % n_, f_selo=lambda s, n=n_: s.pop(n, None), espera=RESUMO_MSG),
            variante("selo primario: o resumo de %s difere do core" % n_, f_selo=lambda s, n=n_: s[n].update(verdict="OUTRO_VEREDITO"), espera=RESUMO_MSG),
            variante("linha `>>> veredito <<<` de %s (recriado) ausente do stdout" % n_, f_std=lambda t_, v=L._ev(ESP, n_): "\n".join(l for l in t_.splitlines() if v not in l) + "\n", espera="o bloco " + n_ + " do stdout"),
            variante("pedra selada da v410 %s: sha256 da fonte no hash formal adulterado" % mod_, f_core=lambda c, r=rel410_: _kf(c)["formal_files_sha256"].__setitem__(r, "0" * 64), espera="as treze pedras seladas"),
        ])
        NEG.append(_pedra_v410_no_disco("o arquivo da pedra selada da v410 %s ausente do kernel do Nos" % mod_, rel410_, lambda p, r: os.replace(p, p + ".fora")))
        NEG.append(_pedra_v410_no_disco("o arquivo da pedra selada da v410 %s com um byte a mais no kernel do Nos" % mod_, rel410_, lambda p, r: open(p, "wb").write(r + b"\n")))
    for n_ in NEG:
        print("  controle negativo %-48s %s" % (n_["controle"], "REPROVOU como esperado" if (n_["reprovou"] and n_["mensagem_esperada_presente"]) else "NAO REPROVOU como esperado"))
        if not (n_["reprovou"] and n_["mensagem_esperada_presente"]):
            falha("controle negativo da leitura nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["problemas"]))
etapa("leitura_negativos", controles=NEG, restaurado=(open(core_path, "rb").read() == core_raw and open(selo_path, "rb").read() == selo_raw and open(std_path, "rb").read() == std_raw and open(sc_path, "rb").read() == sc_raw))

if SO == "leitura":   # v411: so' as etapas da leitura (precondicoes, nos_emulado, conferidor, leitura, leitura_negativos); os textos, as superficies, o b3 e o mapa ficam para o harness completo
    R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); R["so"] = "leitura"; R["tudo_passou"] = bool(not R["problemas"]); R["nao_exigiu_refazer"] = NAO_REFAZER
    R["veredito"] = ("SO LEITURA: o conferidor bate no Nos emulado, a leitura le sem problema e os %d controles negativos reprovam" % len(NEG)) if R["tudo_passou"] else "SO LEITURA: NAO PASSOU (ver problemas)"
    R["evidencia_da_versao"] = EVID
    if "--manter-copias" not in argv:
        for _sub in ("nos_emulado", "conferidor_emulado", "pacote_emulado"):
            shutil.rmtree(os.path.join(OUT, _sub), ignore_errors=True)
    _saida = os.path.join(POS_SAIDA, "HARNESS_TEXTOS_ENSAIO_v411_SO_LEITURA.json")
    open(_saida + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(_saida + ".tmp", _saida)
    print("VEREDITO (so leitura): %s" % R["veredito"]); print("saida:", _saida)
    sys.exit(0 if R["tudo_passou"] else 1)

# ------------------------------------------------------------------ 4. os TEXTOS reais, apontados para o mesmo Nos emulado e para o mesmo pacote
T = importar("textos_v411", os.path.join(HERE, "textos_v411.py"))
T.NOS = NOSE; T.PK = PKE; T._CACHE.clear(); T._CACHE["dl"] = DL   # (o PKE do ensaio nao tem delta_v411.py: o delta REAL e' injetado no cache; o textos o carregaria do PK)
sys.modules["textos_v411"] = T
ERR = DL.ERRATA_TEOREMAS_PT
K_EMU = {"ap_nome": "RECIBO_SINCRONIZACAO_v411_EMULADO.json", "ap_sha": "EMULADO_SEM_HASH", "ap_ver": "EMULADO", "ap_evento": "EMULADO", "ap_bat": "BATERIA_PASSA", "par_sha": "EMULADO_SEM_HASH", "rel_sha": "EMULADO_SEM_HASH", "rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0], "readme_paragrafo_v411": T.paragrafo_v411()[0]}
FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_moldura", lambda: T._moldura(Vd)), ("_escopo", lambda: T._escopo(Vd)), ("_chaves", lambda: T._chaves(Vd)), ("_diznao", lambda: T._diznao(Vd)), ("_ressalvas", lambda: T._ressalvas(Vd)), ("_leituras", lambda: T._leituras(Vd)), ("_blocos_fecho", lambda: T._blocos_fecho(Vd)), ("_erratas_e", lambda: T._erratas_e(Vd)), ("_decisoes", lambda: T._decisoes(Vd)),
           ("_sidecar", lambda: T._sidecar(Vd)), ("_pedra", lambda: T._pedra(Vd)), ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)), ("_kernel_prova", lambda: T._kernel_prova(Vd)), ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)),
           ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)), ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)),
           ("core_memory", lambda: T.core_memory(Vd)), ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0]),
           ("paragrafo_v411", lambda: T.paragrafo_v411()[0]), ("secao_h0dn", lambda: T.secao_h0dn(Vd)), ("_mf", lambda: T._mf(Vd)), ("_ob", lambda: T._ob(Vd))]   # (v411: nenhuma nota ao lado do paragrafo da v410; `_ancoras` e a secao da escala sao da v410: ver a etapa secao_aescala)
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete", "handoff"}   # os textos que embutem _num (o texto do kernel com a errata da palavra «teoremas»)
S16 = Vd.get("s16") or ESP["candidato_sha16"]
_REGS_NOVOS = list(DL.REGISTROS_FUNCAO) + [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO]   # os TRES registros novos da v411 (um com funcao, dois por spec): entram na linhagem, no atlas e no topico novo (REGS do chain)
MARCADORES = {"linhagem": [S16, "<!-- linhagem_v411_selada -->"] + _REGS_NOVOS, "desenho": ["<!-- adendo_v411_selada -->", S16], "atlas": ["<!-- atlas_v411_selada -->", S16] + _REGS_NOVOS,
              "core_memory": ["<!-- core_v411_selada -->", S16], "haja_luz": ["<!-- haja_luz_v411_selada -->", S16], "topico_estatuto": ["<!-- v411_selada -->", S16], "topico_novo": [S16, "# v411 SELADA ("] + _REGS_NOVOS,
              "aviso": ["<!-- aviso_v411_selada -->", S16], "handoff": ["name: handoff-v411-custodia", S16, DL.FECHO_REGISTRO, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->", T.MARC_V411_INI, T.MARC_V411_FIM, "um_absoluto_selo_acom.json", "handoff-v410-custodia"],
              "linha_handoff": ["handoff-v411-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}
TXT = os.path.join(OUT, "textos"); os.makedirs(TXT)
RENDER = {}
E_TXT = {}
for nome, f in FUNCOES:
    e = {"ok": False}
    try:
        r = f()
        if nome == "_d":
            e["numeros"] = {k: r[k] for k in ("depois", "delta", "pct", "n_cun", "n_ck", "n_ins", "n_cit") if k in r}
            e["bancada"] = r.get("bank")
        else:
            assert isinstance(r, str) and r.strip(), "texto vazio"
            v = violacoes(r)
            vf_ = GF.violacoes(r)   # v411: a guarda das frases (a moldura, F60 a F67) em todo texto renderizado
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
            if DL.FRASE_H0DN_OBRIGATORIA_PT in r or DL.FRASE_H0DN_OBRIGATORIA_EN in r:
                falha("%s: traz a frase velha da v410 («pre-registrado; nenhum dado observado lido»): o teste foi aberto uma vez (D169)" % nome)
        e["ok"] = True
    except BaseException as ex:  # noqa: BLE001
        e["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:410]); e["onde"] = traceback.format_exc().strip().splitlines()[-3:]
        falha("%s: %s" % (nome, e["erro"]))
    E_TXT[nome] = e
    print("  %-22s %s%s" % (nome, "OK " if e["ok"] else "FALHOU", (" -- " + e["erro"][:200]) if not e["ok"] else ""))
# a secao da escala (a pedra AEscala) e' da v410 e fica como registro: textos_v411.secao_aescala FALHA A VISTA por desenho (o registro a_escala_v410 e' recriado e selado, nao renderizado)
try:
    T.secao_aescala(Vd); _aesc_ok = False
except AssertionError as _e_aesc:
    _aesc_ok = "e' da v410" in str(_e_aesc)
E_TXT["secao_aescala_falha_a_vista"] = {"ok": bool(_aesc_ok)}
if not _aesc_ok:
    falha("textos_v411.secao_aescala devia FALHAR A VISTA (e' da v410; a v411 nao a reescreve) e nao falhou como esperado")
print("  %-22s %s" % ("secao_aescala (falha a vista)", "OK " if _aesc_ok else "FALHOU"))
# os textos curtos usados como gancho no MEMORY.md tambem passam pelo mesmo ajuste de tamanho; aqui so' dizemos o tamanho
etapa("textos", funcoes=E_TXT, n_ok=sum(1 for e in E_TXT.values() if e["ok"]), n=len(E_TXT), bytes_total=sum(e.get("bytes", 0) for e in E_TXT.values()))
# v411 (D57): o S6d do orquestrador passa o HANDOFF INTEIRO pelo portao do G1 (custodia_g1.textos.portao: a palavra recusada fora da formula, «provada/proved» sem o estatuto na mesma frase, o demerito da retrodicao, hash nao lido, physical_verdict_allowed);
# aqui o mesmo portao roda sobre o handoff renderizado (os hashes conhecidos sao os do proprio texto, como no S6d) e o D59 sobre todos os textos: nada do que fica fora das duas falas.
_PG = {"ok": False}
try:
    sys.path.insert(0, os.path.join(C, "IALD", "Central de Patentes", "tools"))
    from custodia_g1 import textos as _TXG1  # noqa: E402
    _ho_ = RENDER.get("handoff", "")
    _conh_ = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", _ho_)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", _ho_))
    _PG["portao_handoff"] = _TXG1.portao(_ho_, _conh_, rotulo="handoff") if _ho_ else ["handoff nao renderizado"]
    # D59 como a D77(g) a deixou estreitada (delta_v411, DECISOES["D77"]): o Milenio, o Navier e o lindao em NENHUM texto; o nome do executor (Kimi) so' no contexto do H0DN (a ordem ao Kimi, D72 a D80), a mesma regra de registrar_mapa_v411.d59_viola; o post do X nao o nomeia
    _PG["d59"] = sorted(nome for nome, txt in RENDER.items() if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", txt) or (not nome.startswith("_") and re.search(r"(?i)kimi", txt) and not re.search(r"(?i)h0dn", txt)))   # (integracao de 12/11: a regra do Kimi vale para os textos FINAIS; os fragmentos _* herdam o contexto do texto que os embute)
    _PG["ok"] = not _PG["portao_handoff"] and not _PG["d59"]
    if not _PG["ok"]:
        falha("o handoff renderizado nao passa no portao do G1 (S6d, D57) ou um texto traz o que a D59 deixa fora: %s %s" % (_PG["portao_handoff"][:3], _PG["d59"][:3]))
except BaseException as ex:  # noqa: BLE001
    _PG["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:300]); falha("portao do G1 sobre o handoff: %s" % _PG["erro"])
etapa("portao_g1_handoff_e_d59", **_PG)
# v411 (desvio do molde, dito): a custodia G1 (S7 do orquestrador) le o cabecalho do bloco da linhagem e o paragrafo «O que e'» do handoff por regex: a conferencia usa as MESMAS regex de tools\custodia_g1\nos.py, lidas do codigo
try:
    sys.path.insert(0, os.path.join(C, "IALD", "Central de Patentes", "tools"))
    import custodia_g1.nos as _G1N  # noqa: E402
    _bd = _G1N.blocos_do_diario(None, texto=RENDER.get("linhagem", "")).get("v411")
    _qe = _G1N.RE_OQUEE.search(RENDER.get("handoff", ""))
    _g1 = {"bloco_lido": bool(_bd), "titulo_pt": _bd.titulo_pt if _bd else None, "modulos_novos": _bd.modulos_novos if _bd else None, "escada": [_bd.escada_de, _bd.escada_para] if _bd else None, "ladder_no_corpo": _bd.ladder_no_corpo if _bd else None, "pin16": _bd.pin16 if _bd else None,
           "o_que_e_lido": bool(_qe), "secao_elo": "**O elo B(n)" in RENDER.get("handoff", ""), "secao_pendencias": "**Pendências SÓ do operador" in RENDER.get("handoff", "")}
    _g1["ok"] = bool(_bd and _bd.titulo_pt and _bd.modulos_novos == 0 and [_bd.escada_de, _bd.escada_para] == list(ESP["escada_v410_e_v411"]) and _bd.pin16 == S16 and _bd.ladder_no_corpo == Vd.get("teor") and _qe and _g1["secao_elo"] and _g1["secao_pendencias"])   # (a v411 NAO tem modulo novo: o cabecalho diz «nenhum» e a custodia le 0)
except Exception as _ex_g1:  # noqa: BLE001
    _g1 = {"ok": False, "erro": repr(_ex_g1)[:300]}
etapa("custodia_g1_le_os_textos", **_g1)
print("  a custodia G1 le o cabecalho da linhagem e o handoff: %s" % _g1)
if not _g1.get("ok"):
    falha("a custodia G1 nao le o bloco da linhagem ou o handoff da v411: %s" % _g1)
# ---- 3b. (a custodia da v411 e' AUTOMATICA) o S6d de VERDADE e os dois testes sinteticos da custodia:
# (a) textos_custodia_handoff_v411.main(nos, pkg, recibo_dir) roda DE VERDADE sobre o Nos EMULADO deste harness: o diario e' a linhagem renderizada aqui, o handoff e' o renderizado aqui (o corpo que o fechar grava no Nos), o core, o selo e o um.py sao os do Nos emulado,
#     o pacote e' uma pasta de ensaio so' com o ESPERADOS; a revisao de terceiro ausente (os textos dizem que e' ato distinto). Ele anexa os textos da custodia ao handoff (marcadores, secao do README, notas da cadeia), passa as guardas (frases da v411, portao do G1, as conferencias da custodia) e grava o recibo; aqui se confere rc 0, o recibo e o parser do G1;
# (b) teste_textos_custodia_sem_candidato_v411.py e teste_gatilho_custodia_sem_candidato_v411.py (cada um com o sandbox proprio sob C:\t\k411c\ensaio_topo_proposto): o S6d e o passo final do orquestrador (S9_gatilho_custodia) com os controles negativos.
# O gatilho de verdade (ORDEM_HANDOFF_CUSTODIA_v411.md na raiz do pacote) nunca e' escrito por este harness.
def _etapa_custodia():
    _GC = {"ok": False}
    try:
        _gd = os.path.join(OUT, "s6d_custodia"); os.makedirs(_gd)
        _nos_c = os.path.join(_gd, "nos"); _pkg_c = os.path.join(_gd, "pk"); _rec_c = os.path.join(_gd, "recibo"); os.makedirs(_nos_c); os.makedirs(_pkg_c); os.makedirs(_rec_c)
        _liga(os.path.join(NOSE, "um.py"), os.path.join(_nos_c, "um.py")); shutil.copyfile(core_path, os.path.join(_nos_c, "um_absoluto.json")); shutil.copyfile(selo_path, os.path.join(_nos_c, "um_absoluto_selo.json"))
        open(os.path.join(_nos_c, "MEMORIA_DA_LINHAGEM.md"), "w", encoding="utf-8", newline="\n").write(RENDER["linhagem"])
        _hd = RENDER["handoff"]; open(os.path.join(_nos_c, "HANDOFF_v411_CUSTODIA.md"), "w", encoding="utf-8", newline="\n").write(_hd.split("---\n", 2)[2].lstrip("\n"))   # (o corpo que o fechar grava no Nos: sem o front matter)
        shutil.copyfile(P_ESP, os.path.join(_pkg_c, "ESPERADOS_v411.json"))
        _h_antes = open(os.path.join(_nos_c, "HANDOFF_v411_CUSTODIA.md"), "rb").read()
        _TC = importar("textos_custodia_handoff_v411", os.path.join(HERE, "textos_custodia_handoff_v411.py"))
        _rc = _TC.main(_nos_c, _pkg_c, _rec_c)
        _rp = os.path.join(_rec_c, _TC.NOME_RECIBO); _rec = rdj(_rp) if os.path.exists(_rp) else {}
        _h_depois = open(os.path.join(_nos_c, "HANDOFF_v411_CUSTODIA.md"), "rb").read()
        _gv = _rec.get("guardas") or {}
        _GC.update(s6d_rc=_rc, s6d_recibo=bool(_rec), s6d_marcadores=len(_rec.get("marcadores") or []), s6d_handoff_cresceu_bytes=len(_h_depois) - len(_h_antes), s6d_parser_g1_problemas=(_rec.get("parser_g1") or {}).get("problemas"),
                   s6d_guardas_sujas=sorted(k_ for k_, g_ in _gv.items() if any(g_.get(c_) for c_ in ("guarda_frases_v411", "portao_g1", "forma", "custodia_h0dn"))), s6d_formula_e_proposta=(_rec.get("formula") or {}).get("proposta"), s6d_pasta=_gd)
        _s6d_ok = bool(_rc == 0 and _rec and _GC["s6d_marcadores"] >= 7 and _GC["s6d_handoff_cresceu_bytes"] > 3000 and not _GC["s6d_parser_g1_problemas"] and not _GC["s6d_guardas_sujas"])
        _env = dict(os.environ, PYTHONIOENCODING="utf-8")
        _r1 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_textos_custodia_sem_candidato_v411.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_textos_custodia_out.txt"), "w", encoding="utf-8").write((_r1.stdout or "") + "\n--- stderr ---\n" + (_r1.stderr or ""))
        _r2 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_gatilho_custodia_sem_candidato_v411.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_gatilho_custodia_out.txt"), "w", encoding="utf-8").write((_r2.stdout or "") + "\n--- stderr ---\n" + (_r2.stderr or ""))
        _pt = os.path.join(DLX.ENSAIO_DIR, "pos_rito_textos", "TESTE_TEXTOS_CUSTODIA_SEM_CANDIDATO_v411.json")   # (os dois testes gravam, cada um, no sandbox proprio sob C:\t\k411c\ensaio_topo_proposto: caminho fixo nos testes)
        _pg = os.path.join(DLX.ENSAIO_DIR, "pos_rito_gatilho", "TESTE_GATILHO_CUSTODIA_v411.json")
        _jt = rdj(_pt) if os.path.exists(_pt) else {}; _rj = rdj(_pg) if os.path.exists(_pg) else {}
        _cs = _rj.get("casos") or {}
        _GC.update(textos_rc=_r1.returncode, textos_tudo_passou=_jt.get("TUDO_PASSOU"), textos_n_ok=_jt.get("ok"), textos_falhas=[f_.get("caso") for f_ in (_jt.get("falhas") or [])][:6], gatilho_rc=_r2.returncode, gatilho_tudo_passou=_rj.get("tudo_passou"), gatilho_casos=_rj.get("n_casos"), gatilho_negativos=_rj.get("n_negativos"),
                   gatilho_reprovados=sorted(k_ for k_, v_ in _cs.items() if not (v_ or {}).get("ok")), gatilho_seguranca=_rj.get("seguranca_gatilho_real_intocado"), gatilho_de_verdade_existe=os.path.exists(os.path.join(PKG, "ORDEM_HANDOFF_CUSTODIA_v411.md")))
        _GC["ok"] = bool(_s6d_ok and _r1.returncode == 0 and _jt.get("TUDO_PASSOU") is True and (_jt.get("ok") or 0) >= 10 and _r2.returncode == 0 and _rj.get("tudo_passou") is True and (_rj.get("n_negativos") or 0) >= 15 and not _GC["gatilho_reprovados"] and _GC["gatilho_seguranca"] is True)
        if not _GC["ok"]:
            falha("a custodia (S6d de verdade sobre o Nos emulado e os dois testes sinteticos): s6d rc %s (marcadores %s, cresceu %s B, guardas sujas %s, parser %s); textos rc %s (passou %s); gatilho rc %s (passou %s, reprovados %s); ver %s | %s" % (
                _rc, _GC["s6d_marcadores"], _GC["s6d_handoff_cresceu_bytes"], _GC["s6d_guardas_sujas"][:3], _GC["s6d_parser_g1_problemas"], _r1.returncode, _jt.get("TUDO_PASSOU"), _r2.returncode, _rj.get("tudo_passou"), _GC["gatilho_reprovados"][:3], _gd, ((_r1.stdout or "") + (_r2.stdout or ""))[-300:].replace(chr(10), " | ")))
    except BaseException as ex:  # noqa: BLE001
        _GC["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:300]); _GC["onde"] = traceback.format_exc().strip().splitlines()[-3:]; falha("a custodia (S6d de verdade e os testes sinteticos): %s" % _GC["erro"])
    R["etapas"]["custodia_s6d_e_gatilho"] = _GC
    print("  a custodia: o S6d (main) de verdade sobre o Nos emulado (rc %s; %s marcadores) e os dois testes sinteticos (textos %s; gatilho %s casos, %s negativos): %s" % (_GC.get("s6d_rc"), _GC.get("s6d_marcadores"), _GC.get("textos_tudo_passou"), _GC.get("gatilho_casos"), _GC.get("gatilho_negativos"), "ok" if _GC["ok"] else "FALHOU"))


_etapa_custodia()

# ------------------------------------------------------------------ 4b. os PARAGRAFOS PRONTOS do README/site: o QUADRO (v410, INTOCADO; ordem do operador de 23/10: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item) e o paragrafo NOVO do sonico e da afinacao
sys.path.insert(0, PKG)
QD = T._qd()   # (09/11: o quadro do PACOTE, pelo caminho; o import pelo sys.path trazia o da pasta da v410)
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
    _f9["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:410]); _f9["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo do README/site (quadro): %s" % _f9["erro"])
etapa("paragrafo_readme_e_regra_do_4_44", **_f9)
# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (o teste decisivo, a razao de Hubble H0DN x BG1 aberta uma vez): verificacao propria, controles negativos (as quatro obrigacoes da F67 uma a uma), a citacao verbatim e o handoff que diz que os paragrafos anteriores seguem como estao
_sn = {"ok": False}
try:
    PAR_F, PAR_F_INFO = T.paragrafo_v411()
    _h0p = T._h0c(_core_p); _Lh = T._L(_h0p)
    _sn["positivo_sem_falhas"] = (T.verificar_paragrafo_v411(PAR_F, _core_p, ESP) == [])
    _sn["igual_ao_gerado_do_core"] = (PAR_F == T._paragrafo_v411_de(_core_p))
    _ho = RENDER.get("handoff", "")
    _ERR = ""   # (v411: nenhuma nota ao lado do paragrafo da v410; a E41 a E43 sao da candidata, nao de paragrafo publicado)
    _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"] = bool((T.MARC_V411_INI + "\n" + PAR_F.rstrip("\n") + "\n" + T.MARC_V411_FIM) in _ho and ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho
                                                                          and not hasattr(T, "MARC_ERR_INI") and "ERRATA_V410_V411" not in _ho)
    _sn["handoff_lista_o_sidecar"] = bool("um_absoluto_selo_acom.json" in _ho and Vd["sidecar"]["sha256"] in _ho and Vd["sidecar"]["veredito"] in _ho)
    _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"] = bool(("SEGUEM COMO ESTÃO" in _ho or "SEGUE COMO ESTÁ" in _ho) and "handoff-v410-custodia" in _ho and "<!-- INICIO_PARAGRAFO_TESTEMUNHO" not in _ho and "<!-- INICIO_PARAGRAFO_FALSIDADE" not in _ho)
    _sn["info"] = PAR_F_INFO
    # as quatro obrigacoes da F67 (o modelo publicado, a linha das Cefeidas livres com o numero, retrodicao e nao cego, validade nao creditacao) no MESMO bloco do primario; nenhuma frase velha da v410 («pre-registrado; nenhum dado observado lido»)
    _sn["traz_as_quatro_obrigacoes_da_f67"] = bool(all(x_ in PAR_F for x_ in (DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT, DL.OBRIG_VALIDADE_PT)) and _Lh["cn"] in PAR_F)
    _sn["nao_traz_a_frase_velha_da_v410"] = bool(DL.FRASE_H0DN_OBRIGATORIA_PT not in PAR_F and DL.FRASE_H0DN_OBRIGATORIA_EN not in PAR_F)
    _sn["traz_o_nome_do_registro_novo"] = bool(DL.FECHO_REGISTRO in PAR_F)
    _sn["diz_que_o_kernel_e_o_da_v410"] = bool("nenhum módulo novo" in PAR_F)
    if not (_sn["traz_as_quatro_obrigacoes_da_f67"] and _sn["nao_traz_a_frase_velha_da_v410"] and _sn["traz_o_nome_do_registro_novo"] and _sn["diz_que_o_kernel_e_o_da_v410"]):
        falha("paragrafo novo da v411: nao traz as quatro obrigacoes da F67 (o modelo publicado, as Cefeidas livres com o numero, retrodicao e nao cego, validade nao creditacao) no mesmo bloco, ou traz a frase velha da v410, ou nao diz o registro h0dn_bg1_v411 e que nao ha modulo novo: %s" % {k_: _sn[k_] for k_ in ("traz_as_quatro_obrigacoes_da_f67", "nao_traz_a_frase_velha_da_v410", "traz_o_nome_do_registro_novo", "diz_que_o_kernel_e_o_da_v410")})
    if not (_sn["positivo_sem_falhas"] and _sn["igual_ao_gerado_do_core"] and _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"] and _sn["handoff_lista_o_sidecar"] and _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"]):
        falha("paragrafo novo da v411: positivo %s, igual ao gerado do core %s, no handoff %s, sidecar listado %s, paragrafos anteriores ditos como estao %s" % (_sn["positivo_sem_falhas"], _sn["igual_ao_gerado_do_core"], _sn["handoff_traz_os_paragrafos_e_a_nota_entre_os_marcadores"], _sn["handoff_lista_o_sidecar"],
                                                                                                                                  _sn["handoff_diz_que_os_paragrafos_anteriores_seguem_como_estao"]))
    _num_mut = lambda s: s[:-1] + ("0" if s[-1] != "0" else "1")

    def _muts(nome, f, espera):
        p2 = f(PAR_F); fa = T.verificar_paragrafo_v411(p2, _core_p, ESP)
        ok = bool(p2 != PAR_F and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    # os numeros do registro (as DUAS linhas e a lei), lidos do core: cada um adulterado em todo o paragrafo => o numero some e o paragrafo difere do gerado
    _NUMS = [("o Z do primario contra o nulo", _Lh["zn"]), ("o Z do primario contra K", _Lh["zk"]), ("o D do primario", _Lh["D"]), ("o p unilateral", _Lh["p"]), ("o Z das Cefeidas livres contra o nulo", _Lh["cn"]), ("o Z das Cefeidas livres contra K", _Lh["ck"]), ("o sha16 da ordem", DL.FALA_ORDEM_V411["sha256"][:16]),
             ("o sha16 do testemunho", DL.FALA_TESTEMUNHO_V411["sha256"][:16]), ("o H0 do fundo", _Lh["h_fundo"]), ("o H0 publicado", _Lh["h_pub"])]
    _NEGS = [_muts("%s com um caractere trocado (em todo o paragrafo)" % nm, lambda p, s=s: p.replace(s, _num_mut(s)), "ausente do paragrafo") for nm, s in _NUMS]
    _NEGS += [_muts("o ramo do primario trocado (todo o paragrafo)", lambda p: p.replace("ramo %s" % _Lh["rp"], "ramo 9"), "ausente do paragrafo"), _muts("o ramo das Cefeidas livres trocado (todo o paragrafo)", lambda p: p.replace("ramo %s" % _Lh["rc"], "ramo 9"), "ausente do paragrafo")]
    # as QUATRO OBRIGACOES da F67, uma a uma: cada uma tirada do paragrafo => frase de limite ausente
    for _ob_nome, _ob_txt in (("o modelo de erros publicado", DL.OBRIG_MODELO_PT), ("a linha das Cefeidas livres", DL.OBRIG_CEFEIDAS_PT), ("retrodicao", DL.OBRIG_RETRO_PT), ("nao cego", DL.OBRIG_NAO_CEGO_PT), ("validade, nao creditacao", DL.OBRIG_VALIDADE_PT)):
        _NEGS.append(_muts("a obrigacao da F67 «%s» tirada do paragrafo" % _ob_nome, lambda p, t=_ob_txt: p.replace(t, "XXXX"), "frase de limite ausente"))
    _FRASES = ("NOT_FALSIFIED", "este parágrafo não traz o número do quadro", "o gate não se move", "O que o teste NÃO decide", "As sete ressalvas")
    _NEGS += [_muts("a frase de limite «%s» removida" % f[:40], lambda p, f=f: p.replace(f, "XXXX"), "frase de limite ausente") for f in _FRASES]
    _NEGS += [_muts("a creditacao dita pela validade", lambda p: p.replace("validade, não creditação", "validade, é creditação"), "frase de limite ausente"),
              _muts("o gate dito movido", lambda p: p.replace("o gate não se move", "o gate se move"), "frase de limite ausente"),
              _muts("frase proibida: o problema do Clay resolvido", lambda p: p + "\n> - O problema do Clay está resolvido.\n", "guarda das frases"),
              _muts("D65: o que fica fora entra no paragrafo", lambda p: p + "\n> - " + DL.FORA_D65[0] + " aqui.\n", "D65"),
              _muts("frase proibida: a IALD resolve P vs NP", lambda p: p + "\n> - A IALD resolve P vs NP.\n", "guarda das frases"),
              _muts("frase proibida: o funtor e' idempotente", lambda p: p + "\n> - O funtor é idempotente.\n", "guarda das frases"),
              _muts("frase proibida: a TGL prova P = NP de Turing", lambda p: p + "\n> - E a TGL prova P = NP de Turing.\n", "guarda das frases"),
              _muts("frase proibida: tudo derivado", lambda p: p + "\n> - Agora está tudo derivado.\n", "guarda das frases"),
              _muts("frase proibida: tudo teorema", lambda p: p + "\n> - Agora tudo é teorema.\n", "guarda das frases"),
              _muts("frase proibida: nenhuma hipotese", lambda p: p + "\n> - E nenhuma hipótese resta.\n", "guarda das frases"),
              _muts("frase proibida: hipoteses descarregadas", lambda p: p + "\n> - As hipóteses nomeadas descarregadas.\n", "guarda das frases"),
              _muts("frase proibida: a luz nao tem autovetor (fora de aspas)", lambda p: p + "\n> - Agora a luz não tem autovetor nenhum.\n", "guarda das frases"),
              _muts("frase proibida: o certificado esta confirmado", lambda p: p + "\n> - O certificado está confirmado.\n", "guarda das frases"),
              _muts("frase proibida: K(O) provado", lambda p: p + "\n> - K(O) ≠ ⊥ provado para todo O.\n", "guarda das frases"),
              _muts("frase proibida: Omega igual a Phi+", lambda p: p + "\n> - Ω = Φ⁺ no kernel.\n", "guarda das frases"),
              _muts("o estatuto KNOWN removido", lambda p: p.replace("KNOWN", "XX"), "estatuto ausente"),
              _muts("o estatuto OPEN removido", lambda p: p.replace("OPEN", "XX"), "estatuto ausente"),
              _muts("o estatuto INPUT removido", lambda p: p.replace("INPUT", "XX"), "estatuto ausente"),
              _muts("o estatuto REAL removido", lambda p: p.replace("[REAL", "[XX"), "estatuto ausente"),
              _muts("o estatuto DECLARADO removido", lambda p: p.replace("DECLARADO", "XX"), "estatuto ausente"),
              _muts("o 4,44 entra no paragrafo", lambda p: p + "\n> z_disc = " + _z + "\n", "4,44"),
              _muts("seguranca criptografica garantida (alegacao)", lambda p: p + "\n> - A confidencialidade garantida e o sigilo garantido do metodo.\n", "alega seguranca criptografica"),
              _muts("a palavra consciencia usada como termo", lambda p: p + "\n> - A consciência é a tipagem que falta.\n", "consciencia"),
              _muts("a IALD como quem testifica do operador (direcao invertida)", lambda p: p + "\n> - A IALD testifica do operador.\n", "DIRECAO"),
              _muts("a identificacao do operador chamada «leitura do operador» (regra do nome)", lambda p: p + "\n> - É a leitura do operador.\n", "regra do nome")]
    # a citacao do operador que nao e' verbatim: uma letra trocada dentro da primeira citacao entre « » (as citacoes do paragrafo sao as falas de 12/11 e a ordem)
    # (R1 de 12/11 noite, D181) o paragrafo NAO transcreve fala do operador: nenhuma citacao entre aspas angulares (so' data, sha16, papel e autor); a regra (6) da verificacao segue valendo para qualquer citacao que apareca: o controle PLANTA uma
    # citacao que nao e' verbatim de fala nenhuma e a verificacao a recusa
    assert "«" not in PAR_F and "»" not in PAR_F, "o paragrafo da v411 traz aspas angulares: nenhuma fala do operador se transcreve (D181)"
    _NEGS.append(_muts("citacao plantada que nao e' verbatim de fala do operador (D181: nenhuma citacao entra)", lambda p: p + "\n> - Plano: «uma frase que o operador nunca escreveu desta forma exata».\n", "NAO e' verbatim"))
    for r_ in _h0p["ressalvas_secao8"]:
        c_ = re.sub(r"\s+", " ", T._hq(r_).strip())
        _NEGS.append(_muts("a ressalva «%s» removida" % c_[:36], lambda p, c_=c_: p.replace(c_, "XXXX"), "ressalva ausente"))
    for x_ in _h0p["o_que_o_teste_nao_decide"]:
        _NEGS.append(_muts("o item «%s» do que o teste nao decide removido" % T._hq(x_)[:30], lambda p, x_=x_: p.replace(T._hq(x_), "XXXX"), "item do que o teste nao decide ausente"))
    _BUL = []   # os bullets do paragrafo sao DESCOBERTOS do proprio paragrafo gerado (cada linha `> - **Titulo**`): o harness nao adivinha os titulos
    for l_b_ in PAR_F.split("\n"):
        m_b_ = re.match(r"(> - \*\*[^*]+\*\*)", l_b_)
        if m_b_ and m_b_.group(1) not in _BUL:
            _BUL.append(m_b_.group(1))
    _sn["bullets_descobertos"] = _BUL
    assert len(_BUL) >= 8, ("o paragrafo da v411 devia ter ao menos oito bullets `> - **Titulo**`", _BUL)
    for ini_ in _BUL:
        _NEGS.append(_muts("o paragrafo sem o bullet «%s»" % ini_[4:30], lambda p, ini_=ini_: "\n".join(l for l in p.split("\n") if not l.startswith(ini_)), "difere do gerado"))
    # as frases PROIBIDAS da guarda das frases da v411 (F53 a F67; a lista e' a do proprio guarda_frases_v411.PROIBIDAS), cada uma como um PARAGRAFO a parte acrescentado ao paragrafo da v411: a guarda das frases TEM de recusar e nomear a regra
    # (a F67 em especial: o primario dito sem a linha das Cefeidas livres no mesmo bloco, em PT e em EN)
    for _rg_, _fr_ in GF.PROIBIDAS:
        _NEGS.append(_muts("%s: «%s» num paragrafo acrescentado" % (_rg_, _fr_[:46]), lambda p, fr=_fr_: p + "\n\n" + fr + ".\n", _rg_))
    _NEGS += [_muts("a frase velha da v410 volta como estado do teste", lambda p: p + "\n> - H0DN: " + DL.FRASE_H0DN_OBRIGATORIA_PT + ".\n", "difere do gerado"),
              _muts("o token proibido de v410 volta", lambda p: p + "\n> - " + DL.TOKENS_PROIBIDOS_V411[0] + ".\n", "guarda das frases")]
    for n_ in _NEGS:
        print("  controle negativo do paragrafo da v411 %-62s %s" % (n_["controle"][:62], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo da v411 nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _sn["negativos"] = _NEGS

    def _levanta(f):
        try:
            f(); return False
        except AssertionError:
            return True
    _inv_txt = "A IALD testifica do operador, e o um.py testifica em hash."
    _tx = {"cita_fora_dos_bytes_levanta": _levanta(lambda: T._cita("a queda é o corpo de Newton e a IALD de ninguem")),
           "cita_verbatim_da_ordem_passa": (T._cita(DL.FALA_ORDEM_V411["text"].strip()) == "«" + DL.FALA_ORDEM_V411["text"].strip() + "»"),
           "cita_do_texto_da_outra_instancia_levanta": _levanta(lambda: T._cita("Operador. A chave girou.")),
           "cita_parafraseada_levanta": _levanta(lambda: T._cita("concordo com tudo e prossigo")),
           "cita_do_que_a_D65_deixa_fora_levanta": _levanta(lambda: T._cita(DL.FORA_D65[-1])),
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
    print("  paragrafo novo (o teste decisivo, H0DN x BG1 aberto uma vez): positivo ok; %d controles negativos; citacao e direcao: %d controles ok" % (len(_NEGS), len(_tx)))
except BaseException as ex:  # noqa: BLE001
    _sn["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:410]); _sn["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo novo da v411: %s" % _sn["erro"])
etapa("paragrafo_v411_e_citacoes", **_sn)
# ------------------------------------------------------------------ 4d. a SECAO do teste decisivo (H0DN x BG1 aberto uma vez; D169): textos_v411.secao_h0dn, montada do core emulado; as quatro obrigacoes da F67 no mesmo texto, a cabeca do teste so' POR EXTENSO (a string nao e' reproduzida: a P18 a recusa), sem a frase velha da v410,
# sem os tokens proibidos, sem a aritmetica do agregado publico fora do que o registro diz; controles negativos das guardas sobre o proprio texto (cada um TEM de reprovar), em especial a F67: o primario sem a linha das Cefeidas livres
_hx = {"ok": False}
try:
    _sh = RENDER.get("secao_h0dn", ""); _hdc = _core_p.get(DL.FECHO_REGISTRO) or {}; _h0s = T._h0c(_core_p); _Ls = T._L(_h0s)
    _hx["traz_o_nome_do_registro"] = DL.FECHO_REGISTRO in _sh
    _hx["traz_as_quatro_obrigacoes_da_f67"] = bool(all(x_ in _sh for x_ in (DL.OBRIG_MODELO_PT, DL.OBRIG_CEFEIDAS_PT, DL.OBRIG_RETRO_PT, DL.OBRIG_NAO_CEGO_PT, DL.OBRIG_VALIDADE_PT)) and _Ls["cn"] in _sh and _Ls["zn"] in _sh)
    _hx["traz_os_dois_numeros_e_os_dois_ramos"] = bool(_Ls["zn"] in _sh and _Ls["zk"] in _sh and _Ls["cn"] in _sh and _Ls["ck"] in _sh and ("ramo %s" % _Ls["rp"]) in _sh and ("ramo %s" % _Ls["rc"]) in _sh)
    _hx["nao_traz_a_frase_velha_da_v410"] = DL.FRASE_H0DN_OBRIGATORIA_PT not in _sh and DL.FRASE_H0DN_OBRIGATORIA_EN not in _sh
    _hx["nao_traz_a_cabeca_inteira_do_teste"] = (_h0s.get("cabeca_do_teste") or "x") not in _sh and ("TGL_PRO" + "VED") not in _sh
    _hx["sem_tokens_proibidos"] = not any(t_ in _sh for t_ in tuple(DL.TOKENS_PROIBIDOS_V411))
    _hx["diz_que_a_creditacao_nao_foi_dada"] = bool(re.search(r"(?i)creditação", _sh))
    _hx["guardas_limpas"] = not GF.violacoes(_sh) and not violacoes(_sh)
    _neg_h = {"token_proibido": _sh + "\n\n" + DL.TOKENS_PROIBIDOS_V411[0] + "\n", "cinco_sigma_atingido": _sh + "\n\nO H0DN: 5 sigma atingido.\n", "nao_falsificado_a_5_sigma": _sh + "\n\nO resultado é não falsificado a 5 sigma.\n", "covariancia_fisica_fechada": _sh + "\n\nA covariância física está fechada.\n",
              "creditacao_afirmada": _sh + "\n\nA TGL foi confirmada pela natureza.\n", "poder_certificado": _sh + "\n\nO teste tem poder certificado.\n", "vetor_fora_do_suporte_erro_de_montagem": _sh + "\n\nO vetor fora do suporte é erro de montagem.\n", "teste_cego": _sh + "\n\nFoi um teste cego.\n",
              "evidencia_independente": _sh + "\n\nÉ evidência independente das Fases 4, 5 e 9.\n", "descoberta": _sh + "\n\nA descoberta do H0DN a 6 sigma.\n", "beta_literal": _sh + "\n\nCom beta = 0,0120313.\n",
              "f67_primario_sem_as_cefeidas_livres_pt": _sh + "\n\nNo H0DN o primário fica a 6,11 contra o nulo.\n", "f67_primario_sem_as_cefeidas_livres_en": _sh + "\n\nThe primary lies 6.11 against the null in the H0DN test, under the published error model.\n",
              "f67_a_secao_inteira_sem_a_linha_das_cefeidas_livres": re.sub(r"(?i)cefeidas livres|free[_ ]cepheids", "XXXX", _sh), "f67_a_secao_inteira_sem_o_modelo_publicado": re.sub(r"(?i)" + re.escape(DL.OBRIG_MODELO_PT) + "|UNDER_THE_PUBLISHED_MODEL", "XXXX", _sh),
              "f67_a_secao_inteira_sem_validade_nao_creditacao": re.sub(r"(?i)" + re.escape(DL.OBRIG_VALIDADE_PT) + "|VALIDITY_NOT_CREDITATION", "XXXX", _sh), "f67_a_secao_inteira_sem_retrodicao": re.sub(r"(?i)" + re.escape(DL.OBRIG_RETRO_PT) + "|RETRODICTION", "XXXX", _sh),
              "f67_a_secao_inteira_sem_o_nao_cego": re.sub(r"(?i)n[ãa]o\s+(?:é\s+)?ceg[oa]|not\s+blind|NOT_BLIND", "XXXX", _sh)}   # (a regra F67 aceita a obrigacao no texto OU no token de maquina do veredito: o controle tira as DUAS formas do texto inteiro)
    _hx["controles_negativos"] = {k_: bool(GF.violacoes(v_) or violacoes(v_)) for k_, v_ in _neg_h.items()}
    _hx["f67_cefeidas_livres_ausente_cita_a_regra_F67"] = bool(any(str(x_[0]).startswith("F67") for x_ in GF.violacoes(_neg_h["f67_primario_sem_as_cefeidas_livres_pt"])) and any(str(x_[0]).startswith("F67") for x_ in GF.violacoes(_neg_h["f67_primario_sem_as_cefeidas_livres_en"])))
    _hx["texto_bytes"] = len(_sh.encode("utf-8"))
    _ruim_h = [k_ for k_, v_ in _hx.items() if k_ not in ("ok", "controles_negativos", "texto_bytes") and v_ is not True] + [("controle:" + k_) for k_, v_ in _hx["controles_negativos"].items() if not v_]
    if not _sh.strip() or _ruim_h:
        falha("secao_h0dn: texto vazio ou itens que nao deram o esperado: %s" % _ruim_h)
    _hx["ok"] = True
    print("  secao_h0dn: %d B; o nome do registro, as quatro obrigacoes da F67 e as duas linhas presentes, sem a frase velha da v410 nem a cabeca inteira; %d controles negativos das guardas reprovam (a F67 inclusive)" % (_hx["texto_bytes"], len(_hx["controles_negativos"])))
except BaseException as ex:  # noqa: BLE001
    _hx["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:410]); falha("secao_h0dn: %s" % _hx["erro"])
etapa("secao_h0dn", **_hx)
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
NOMES_ARQ.update({"MEMORY.md", "MEMORY_2.md", "TGL_ATLAS.md", "um.py", "rodada_v411_stdout.txt", "HANDOFF_v411_CUSTODIA.md", "DIFF_v410_v411.diff", "DIFF_KERNEL_v411.txt", "handoff-v411-custodia.md",
                  "missao-ultima-flag-um-py.md", "estatuto-da-prova-07out.md", "central-de-patentes-estado.md", "handoff-v410-custodia.md", T.TOPICO_NOVO})
NOMES_ARQ.update({"um_absoluto_selo_acom.json", "um_absoluto_selo.json", "um_absoluto.json", "conferencia_rito_v411.json", "v411_selo", "EXECUTION_LOCKED_NOT_ONE"})
HEX16 = set()
for v_ in (Vd.get("s16"), Vd.get("base16"), Vd.get("conf16"), (Vd.get("pilar") or {}).get("result16")):
    if v_:
        HEX16.add(str(v_))
for k_, v_ in Vd.items():
    if k_.startswith("h_") and isinstance(v_, str):
        HEX16.add(v_)
HEX16.update((Vd.get("artigos") or {}).values()); HEX16.update(Vd.get("verbatins", {}).keys()); HEX16.update(d["sha16"] for d in T._falas().values()); HEX16.update(v["sha16"] for v in (ESP.get("pedras") or {}).values()); HEX16.add(ESP["quadro"]["frase_sha16"]); HEX16.add(T._sha_verdade()); HEX16.update(str(h)[:16] for h in (ESP.get("pedras_v405_sha256") or {}).values())
HEX16.update(str(x["sha256"])[:16] for x in (ESP.get("cunhagens") or {}).values()); HEX16.add(str(Vd.get("selo_ts") or "")[:16])
HEX16.update(str(h)[:16] for h in ESP["veracidade"]["fontes"].values())
HEX16.update((DLX.sha16_arquivo(DLX.ACORDE_KIMI_ARQ), DLX.sha16_arquivo(DLX.HALF_NAT_ARQ)))   # as fontes que a Lei do Diminuto cita (errata R3): hash lido do arquivo
HEX16.update(str(v)[:16] for v in ((ESP.get("selo_acom") or {}).get(k) for k in ("bloco_embutido_sha256", "sha256_do_um_py", "lut_sha256")) if v); HEX16.update(str(((ESP.get("selo_acom") or {}).get(p) or {}).get("sha256"))[:16] for p in ("psi", "theta", "kappa"))
HEX16.add(str((ESP.get("declaracao") or {}).get("verbatim_sha256"))[:16]); HEX16.add((Vd.get("sidecar") or {}).get("sha16") or ""); HEX16.update((o.get("sha16") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values())
HEX16.add((Vd.get("selo") or {}).get("bloco16") or ""); HEX16.update((Vd.get("selo") or {}).get(k) or "" for k in ("psi_sha16", "theta_sha16", "kappa_sha16", "lut16"))
HEX64 = {str((Vd.get("sidecar") or {}).get("sha256") or ""), str(Vd.get("s64") or "")} | {str(o.get("sha256") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values()}; HEX64.discard("")   # os hashes COMPLETOS que o handoff lista (o sidecar e os tres objetos), lidos do sidecar e do um.py do disco
_hd_h = core_emu.get(DL.FECHO_REGISTRO) or {}   # os hashes que os textos do H0DN citam: os insumos pinados e os citados nao embutidos, LIDOS do registro do core emulado
for _h_ in [(v_ or {}).get("sha256") for v_ in (_hd_h.get("insumos_pinados") or {}).values()] + [(v_ or {}).get("sha256") for v_ in (_hd_h.get("citados_nao_embutidos") or [])] + [(_hd_h.get("values") or {}).get("nao_decide_secao6_sha256")]:
    if isinstance(_h_, str) and len(_h_) == 64:
        HEX64.add(_h_); HEX16.add(_h_[:16])
PAT_ROOT = os.path.join(C, "IALD", "Central de Patentes")
# (integracao de 12/11) fontes reais que a v411 acrescentou e o harness ainda nao enumerava, todas LIDAS dos arquivos e do core emulado (nada digitado):
HEX16.update(str(g_["sha256"])[:16] for g_ in DL.TEXTOS_DA_GERENCIA_CITADOS)   # os seis textos da gerencia a que o operador respondeu, citados SO' por sha256
HEX16.add(hashlib.sha256(open(os.path.join(PKG, "ACORDO_COM_A_CUSTODIA_v411_12nov.md"), "rb").read()).hexdigest()[:16])   # o acordo com a custodia (D171), hash lido do arquivo
HEX16.add(hashlib.sha256(str(_hd_h.get("cabeca_do_teste") or "").encode("utf-8")).hexdigest()[:16])   # a cabeca do teste: so' o sha16 dela entra nos textos (a P18 recusa a string)
REG_H0_TXT = json.dumps(_hd_h, ensure_ascii=False)   # o registro com funcao do core emulado (a saida do ensaio a seco): fonte real das palavras que os textos tiram dele (a emenda, o veredito de maquina, os apontadores do literal)


CONHECIDOS = {str(x) for x in (Vd.get("selo_ts"), Vd.get("instalado_em"), Vd.get("data")) if x}
CONHECIDOS.update(str(x) for x in K_EMU.values())
CONHECIDOS.update(str(h)[:8] for h in ESP["veracidade"]["fontes"].values()); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_pt"]); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_en"])                      # os campos EMULADOS dos recibos do B(n) que o handoff recebe (so' existem depois do passo 10)
CONHECIDOS.add(T._linha_maquina_v411(core_emu, T._dados_paragrafo(core_emu)))   # a linha de maquina do paragrafo novo (lida dos registros do core emulado)
CONHECIDOS.add((Vd.get("selo") or {}).get("perfil") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("esquema") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("veredito") or "")
CONHECIDOS.update({T.TOPICO_NOVO[:-3], "v411_kernel", "v411_selo"})     # o nome do topico sem a extensao (o [[wikilink]]) e as duas pastas que o fechar cria ANTES de escrever o handoff
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
    if len(tok) >= 12 and tok in REG_H0_TXT:
        return "registro_h0dn"
    if tok.endswith(".lean") and os.path.exists(os.path.join(NOSE, "tgl_kernel", *tok.split("/"))):
        return "kernel_arquivo"
    if "\\" in tok or "/" in tok:
        cands = [os.path.join(PAT_ROOT, tok), os.path.join(PKG, tok), os.path.join(os.path.dirname(PKG), tok.replace("work\\cadeia_de_selo\\", "")), os.path.join(PAT_ROOT, tok.replace("/", os.sep))]
        if any(os.path.exists(c) for c in cands) or tok.startswith(("work\\cadeia_de_selo\\v411", "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v411")):
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
_inventados_ = ("termo_inventado_v411_xyz", "0123456789abcdef", "TGL_VEREDITO_QUE_NAO_EXISTE__GATE_MOVED")   # controle negativo: um termo que nenhuma fonte tem continua SEM achado
if any(achado(t_) is not None for t_ in _inventados_):
    falha("controle negativo de cita_so_o_que_existe: um termo inventado foi achado numa fonte (a fonte ficou larga demais): %s" % [t_ for t_ in _inventados_ if achado(t_) is not None])
etapa("cita_so_o_que_existe", tokens_conferidos=total_tok, sem_fonte={k: sorted(set(v)) for k, v in SEM.items()}, ok=not SEM, controle_negativo_termo_inventado_sem_achado=all(achado(t_) is None for t_ in _inventados_))
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
    sp = os.path.join(HERE, "superficies_v411.py")

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
    _RN = list(_REGS_NOVOS)   # os TRES registros novos da v411 (REGS do chain)
    exige = [("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v411_selada -->"] + _RN), ("DESENHO_DO_FECHAMENTO_QG.md", ["<!-- adendo_v411_selada -->", S16]),
             ("TGL_ATLAS.md", ["<!-- atlas_v411_selada -->", S16] + _RN), ("TGL_CORE_MEMORY.md", ["<!-- core_v411_selada -->", S16]), ("CLAUDE.md", ["<!-- haja_luz_v411_selada -->", S16]),
             ("MEMORY.md", [S16]), ("MEMORY_2.md", ["v411"]), ("estatuto-da-prova-07out.md", ["<!-- v411_selada -->", S16]), ("missao-ultima-flag-um-py.md", [S16]), ("central-de-patentes-estado.md", [S16]),
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
        falha("superficies_v411.py (copias do MEMORY.md real) saiu com rc %s (esperado 0 ou 3; ver ensaio_superficies_out.txt)" % rc_a)
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
            ancora = lambda l: ("(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")) or ("(handoff-v410-custodia.md)" in l and l.startswith("- [HANDOFF v410"))
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
        falha("superficies_v411.py (copia com folga) saiu com rc %s na 1a rodada (ver ensaio_superficies_folga_out.txt)" % rc_b1)
    if rc_b2 != 0 or not cena_b["idempotente_na_2a"]:
        falha("superficies_v411.py (copia com folga) nao e' idempotente na 2a rodada (rc %s)" % rc_b2)
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
# ------------------------------------------------------------------ 7. o b3_recibo REAL contra recibos SINTETICOS (derivados dos reais da v410)
if not SEM_B3:
    B3D = os.path.join(OUT, "b3_sintetico"); os.makedirs(B3D)
    pinos = rdj(P_PINOS); pre = rdj(pinos["recibo_pre_selo"]["path"]); PKG_ANT = os.path.join(os.path.dirname(PKG), "v410")
    import glob as _g
    base_ens = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3_ensaio_*", "RECIBO_SINCRONIZACAO_v410_*.json"))[0]); base_apl = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v410_*.json"))[0])
    n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1

    def sintetico(base, modo):
        r = json.loads(json.dumps(base)); r["versao_alvo"] = "v411"; r["fase"] = "pos_selo"; r["modo"] = modo; r.pop("salto", None); r.pop("cadeia_de_selos", None)
        r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"]))
        r["manifesto_novo"]["deployment_id"] = "B%d-v411-20261023-R1" % n_ger
        r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}
        r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v411"}
        r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
        if modo == "ensaio":
            r["veredito"] = "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger; r["aplicacao"] = None
        else:
            r["veredito"] = "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_ger
            r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v411", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
        r["_sintetico"] = "SINTETICO: derivado do recibo real da v410 pelo harness; NAO e' um recibo do esboco"
        return r
    seq = [0]

    def roda_helper(nome, r, modo, extra=()):
        seq[0] += 1
        pth = os.path.join(B3D, "%02d_%s_RECIBO_SINTETICO.json" % (seq[0], nome)); raw = json.dumps(r, ensure_ascii=False, indent=1).encode("utf-8"); open(pth, "wb").write(raw)
        so = os.path.join(B3D, "%02d_%s_stdout.txt" % (seq[0], nome)); open(so, "w", encoding="utf-8").write("ruido\n" + json.dumps({"veredito": r.get("veredito"), "recusa": None, "recibo": pth, "recibo_sha256": sha(raw)}) + "\n")
        pr_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "b3_recibo_v411.py"), so, modo] + list(extra), capture_output=True, text=True, encoding="utf-8")
        return pr_.returncode, (pr_.stdout + pr_.stderr).strip().splitlines()[-3:]
    CASOS = []
    pos_e = sintetico(base_ens, "ensaio"); pos_a = sintetico(base_apl, "aplicar")
    CASOS.append(("ensaio_ok", pos_e, "ensaio", 0)); CASOS.append(("aplicar_ok", pos_a, "aplicar", 0))

    def mut(r, f):
        r2 = json.loads(json.dumps(r)); f(r2); return r2
    CASOS += [("salto_declarado", mut(pos_e, lambda r: r.update({"salto": {"declarado": True}})), "ensaio", 1),
              ("veredito_com_salto", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__SALTO_v392_v411__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "ensaio", 1),
              ("geracao_errada", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (n_ger + 1)})), "ensaio", 1),
              ("versao_alvo_v410", mut(pos_e, lambda r: r.update({"versao_alvo": "v410"})), "ensaio", 1),
              ("bateria_falhou", mut(pos_e, lambda r: r.update({"bateria_resultado": {"veredito": "BATERIA_FALHOU"}})), "ensaio", 1),
              ("bancada_pinava_v392", mut(pos_e, lambda r: r["manifesto_anterior"].update({"version": "v392"})), "ensaio", 1),
              ("recibo_pre_selo_de_outro", mut(pos_e, lambda r: r.update({"recibo_pre_selo": {"sha256": "0" * 64}})), "ensaio", 1),
              ("manifesto_anterior_mudou", mut(pos_e, lambda r: r["manifesto_anterior"].update({"sha256": "f" * 64})), "ensaio", 1),
              ("pinos_da_bateria_de_v410", mut(pos_e, lambda r: r["bateria"]["pinos_da_versao"].update({"versao": "v410"})), "ensaio", 1),
              ("ensaio_com_aplicacao", mut(pos_e, lambda r: r.update({"aplicacao": {"x": 1}})), "ensaio", 1),
              ("aplicar_pos_conferencia_v410", mut(pos_a, lambda r: r["aplicacao"]["pos_conferencia"].update({"canonical_version": "v410"})), "aplicar", 1),
              ("aplicar_sem_aplicacao", mut(pos_a, lambda r: r.update({"aplicacao": None})), "aplicar", 1),
              ("aplicar_com_veredito_de_ensaio", mut(pos_a, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "aplicar", 1)]
    res_b3 = []
    for nome, r, modo, esperado in CASOS:
        rc_, cauda = roda_helper(nome, r, modo)
        res_b3.append({"caso": nome, "rc": rc_, "esperado": esperado, "ok": rc_ == esperado, "cauda": [c[:200] for c in cauda]})
        print("  b3_recibo %-34s rc %s (esperado %s) %s" % (nome, rc_, esperado, "OK" if rc_ == esperado else "FALHOU"))
        if rc_ != esperado:
            falha("b3_recibo_v411.py: caso %s deu rc %s (esperado %s): %s" % (nome, rc_, esperado, cauda))
    rc_, cauda = roda_helper("terceiro_argumento", pos_e, "ensaio", extra=("0" * 64,))
    res_b3.append({"caso": "terceiro_argumento_(cadeia)", "rc": rc_, "esperado": 1, "ok": rc_ == 1, "cauda": [c[:200] for c in cauda]})
    if rc_ != 1:
        falha("b3_recibo_v411.py aceitou um 3o argumento (nao ha cadeia de selos na v411)")
    etapa("b3_recibo", sintetico=True, base="recibos reais da v410 (so' leitura)", geracao_nova=n_ger, casos=res_b3, n_ok=sum(1 for c in res_b3 if c["ok"]), n=len(res_b3))
# ------------------------------------------------------------------ 8. o registro do mapa (montar) contra o core emulado e o livro real (so' leitura)
try:
    RM = importar("registrar_mapa_v411", os.path.join(HERE, "registrar_mapa_v411.py")); RM.PK = PKE; RM._CACHE.clear()   # (o mapa le ESPERADOS, o core da v410 selada, PINOS_BN e o recibo do kernel por PK: no ensaio, o pacote emulado)
    ids = RM.ids_do_livro()
    arts = [os.path.join(NOSE, "um.py"), os.path.join(NOSE, "um_absoluto_selo.json")]
    REG = RM.montar(Vd, core_emu, selo_emu, ids, arts)
    # controles negativos de registrar_mapa_v411: a regra da ordem do 4,44 aplicada aos campos do registro (sem o p, sem a linha dos 5 sigma; a clausula completa passa) e as recusas de montar() (selo de outra versao; rota nova que ja' existe no livro)
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
                "montar_recusa_selo_de_outra_versao": _recusa(lambda: RM.montar(Vd, core_emu, dict(selo_emu, um_version="v410"), ids, arts)),
                "montar_recusa_rota_nova_que_ja_existe": _recusa(lambda: RM.montar(Vd, core_emu, selo_emu, set(ids) | {RM.NOVA}, arts))}
    etapa("mapa_controles_negativos", **CTL_MAPA)
    for k_, v_ in CTL_MAPA.items():
        print("  mapa, controle %-48s %s" % (k_, "ok" if v_ else "FALHOU"))
        if not v_:
            falha("mapa: controle negativo de registrar_mapa_v411 nao deu o esperado: %s" % k_)
    pj = os.path.join(OUT, "registro_mapa_v411_ENSAIO.json"); open(pj, "w", encoding="utf-8").write(json.dumps(REG, ensure_ascii=False, indent=1))
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
    falha("mapa: registrar_mapa_v411.montar falhou: %s: %s" % (type(ex).__name__, str(ex)[:300]))
# ------------------------------------------------------------------ 9. marcas pendentes, sintaxe
import ast
pend = []; sint = {}
for f in sorted(os.listdir(HERE)):
    if f.endswith(".py"):
        tx = rd(os.path.join(HERE, f))
        if MARCA_ADAPTAR in tx:
            pend.append(f + " (" + MARCA_ADAPTAR + ")")
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

# ------------------------------------------------------------------ limpeza (so' dentro de harness_saida_v411): o Nos EMULADO e as copias pesadas das superficies nao ficam no pacote (--manter-copias as guarda)
LIMPO = {}
if "--manter-copias" not in argv:
    for sub in ("nos_emulado", "conferidor_emulado", "pacote_emulado"):
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
etapa("limpeza", removido_bytes=LIMPO, nota="so' o que o harness criou em harness_saida_v411; --manter-copias guarda tudo")

# ------------------------------------------------------------------ resumo
R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
R["tudo_passou"] = bool(not R["problemas"]); R["nao_exigiu_refazer"] = NAO_REFAZER
R["origem_das_entradas"] = dict(ORIGEM); R["nos_emulado_fonte"] = _FONTE_NOS
R["veredito"] = (("TUDO PASSOU: o conferidor da v411 (16 itens C1-C16 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos: o registro NOVO h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez, recalculado no rito: as DUAS linhas, o primario sob o modelo de erros publicado e as Cefeidas livres ao lado; ausente, nao selado, checagem falsa, valores adulterados, ramo, beta, veredito, "
                 "opened_once, observed_vector_read, gate, escada, as sete ressalvas, o que nao decide, a emenda as claras, a finitude, os insumos pinados e os citados, o texto do registro [token proibido, a frase velha da v410, a F67 sem a linha das Cefeidas livres, F60 a F63], o resumo no selo, o bloco do stdout, a conferencia, ESPERADOS, CANDIDATO e FLAGS mutados na memoria); "
                 "cunhagens_v411 e kh_n1_cobertura_v411 (as falas do delta, E41 a E43 e a dos pisos, as decisoes do delta, as sete ressalvas, o alcance de P = nP, a regra do nome, D65, a moldura); os QUATRO registros com funcao e os dois por spec da v410 RECRIADOS (ausente, nao selado, veredito, checagens); o traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 HERDADOS e recriados, "
                 "com as ancoras e os bundles deles (lidos dos deltas); cunhagens/kh de v409 a v406; os recriados de v405 a v399; o gate sem se mover; NENHUM modulo novo nem bandeira nova; as linhas [v411] a [v397] e a do sidecar do stdout), os textos renderizam (secao_h0dn inclusive; secao_aescala falha a vista por desenho) e a guarda P18 e a guarda das frases estao limpas, "
                 "a custodia G1 le o bloco da linhagem e o handoff, o S6d (textos_custodia_handoff_v411.main) roda DE VERDADE sobre o Nos emulado e os dois testes sinteticos da custodia passam, os dois paragrafos do README/site (o do quadro, intocado, e o novo da v411, com as quatro obrigacoes da F67 uma a uma) passam nas verificacoes, "
                 "as superficies rodam em copias, o b3_recibo e o mapa montam sem registrar") if R["tudo_passou"] else ("NAO PASSOU (%d problema(s); ver 'problemas' no resumo)" % len(R["problemas"]))) + ("" if not ENSAIO else " [ENSAIO DO TOPO PROPOSTO: o artefato NAO e' candidato; nada aqui prova o rito real]")
R["evidencia_da_versao"] = EVID
R["limites"] = ["Nos, stdout, recibos do B(n) e a arvore sao EMULADOS (ditos acima); o conferidor, a leitura, os textos, as superficies (em copias), o S6d e o mapa (so' leitura do livro) sao os REAIS", "NAO prova o rito real nem a Bancada: isso e' do rito e do B(n)", "NAO escreve em work\\ no ensaio (V411_ENSAIO_TOPO_PROPOSTO=1): tudo vai para " + os.path.dirname(OUT) if ENSAIO else "as copias vao para C:\\t\\h411; o resumo para pos_rito\\"]
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v411.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
os.makedirs(POS_SAIDA, exist_ok=True)
saida = os.path.join(POS_SAIDA, "HARNESS_TEXTOS_ENSAIO_v411" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json")   # o nome sem sufixo so' nasce da rodada que EXIGE o refazer (ou do ensaio, que tem o PRONTO)
open(saida + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(saida + ".tmp", saida)
print("VEREDITO DO HARNESS (%s): %s" % (ROTULO, R["veredito"])); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)

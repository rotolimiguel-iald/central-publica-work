# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-sonnet-posrito-H-v411, a servico do claude-construtor-v411-posrito] ADAPTADO DE VERDADE (nao so' o rotulo): a v411 = o teste H0DN x BG1 aberto uma vez; NENHUM modulo novo (o bundle e' vazio; o diff do kernel e' vazio de modulos); UM registro com funcao, h0dn_bg1_v411, e dois por spec (cunhagens_v411, kh_n1_cobertura_v411); os quatro registros com funcao e os dois por spec da v410 RECRIADOS; o fechar, o b3_recibo, a fila da memoria e o registrar_mapa rodam em SANDBOX com o Nos emulado do ENSAIO; controles negativos NOVOS do fechar (h0dn_bg1_v411 ausente, nao selado, nao aberto, checagem falsa, valor adulterado nas duas linhas, beta errado, veredito trocado, opened_once falso, a linha das Cefeidas livres ausente num texto que traz o primario [F67], a frase velha da v410, token proibido, os recriados da v410, as bandeiras e a escada); S6d (textos_custodia_handoff_v411.main) DE VERDADE sobre o handoff que o fechar gravou no sandbox; TODA saida vai para C:\t\k411c\ensaio_topo_proposto\pos_rito\ no ensaio e as ENTRADAS vem de PRONTO_PARA_O_POS_RITO.json (sem ele: rc 3, nada escrito); ver ADAPTACAO_H_v411.json
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] AVISO da gerencia (09/11): a pasta VEDADA da entrega do Kimi (DL.H0DN_PASTA_VEDADA, lida do delta real importado) e' excluida EXPLICITAMENTE do espelho da casa e da copia da memoria; um acesso medido sob ela na importacao do delta e' FALHA VISIVEL
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] os QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410): o STUB do harness traz V['a_escala'], V['hms13'] e V['ancoras_aescala'] e os seis nomes (REGS); o manifesto TEM de trazer registros_funcao_v410 com os quatro, a_escala_v410_resumo e h0dn_fontes_hms13_v410_resumo (e as chaves novas MAN_CHAVES); o handoff de ensaio diz os quatro registros e as formas obrigatorias (H0DN, HMS/13, a forma canonica do Clay, a D83, os nomes ratificados da AEscala); controles negativos NOVOS do fechar sobre o core: a escala (nao ratificada, numero adulterado, frase canonica do Clay trocada, frase proibida, chave antiga mudada, ausente) e o recibo HMS/13 (ausente, vetor observado lido, entrega aberta em rito, campo trocado, token proibido, sem a frase obrigatoria). Rodar so' depois do ensaio a seco (precisa do core do ensaio).
# [ADAPTADO v410, 09/11/2026, Sonnet (adaptacao do pos-rito; fork D), a servico do claude-construtor-v410] ao DESENHO_v410 + AO LADO de 09/11: as falas de 06 a 09/11 (DL.N_FALAS_V410, de quatro so' o trecho), D63 a D76, E29 e E30, a secao 6 da pedra e o SEGUNDO registro com funcao, h0dn_bg1_v410 (D72: pre-registrado; nenhum dado observado lido): o manifesto com registros_funcao_v410.h0dn_bg1_v410 e h0dn_bg1_v410_resumo; controles negativos do H0DN no core (ausente, vetor observado lido, valor adulterado, checagem falha, fonte da funcao ausente, token proibido, 5 sigma atingido, cabeca pela palavra do livro de cobrancas, sem a frase obrigatoria) e no handoff (1d, por COPIAS do fechar com texto emendado); a etapa 2e (o H0DN nos handoffs gravados); a guarda D72 das superficies em COPIA (S4b); o harness NAO rodou nesta retomada (precisa do candidato/dry_v410).
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/harness_fechar_sandbox_v409.py, adaptada a v410 (IALD2) por _adapt_forkA_harness_fechar_v410.py (fork A, 06/11/2026): o manifesto e o STUB com as chaves de V da v410, os registros novos iald2_v410 e os dois specs, as recusas do fechar retargetadas, nenhuma nota ao lado; ver bump/pos_rito__harness_fechar_sandbox_v410.py.diff.
r"""harness_fechar_sandbox_v411.py -- (1) A FILA DA MEMORIA do pos-rito em COPIA da memoria e (2) roda fechar_v411.py e registrar_mapa_v411.py (o main) num SANDBOX inteiro (nada fora da pasta de saida e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada nao sao tocados; o mapa de rotas real e' SO' LIDO).
(1) A FILA DA MEMORIA (ordem do operador de 26/10/2026: so' a gerencia c1 escreve o MEMORY.md; o vigia compara o indice ao pino): ensaio, numa COPIA do diretorio de memoria (memoria_copia: os arquivos NAO-.bak do diretorio real + fila\ inteira; MEMORIA_DIR e V411_MEMORIA_DIR apontam para a copia),
do passo do pos-rito que PAUSA o vigia, escreve o indice, PINA, solta a pausa e VERIFICA, em quatro niveis: (a) as operacoes de fila_memoria_v411.py na ORDEM em que o chain as chama (ordem lida do TEXTO do chain): pausa criada ANTES da escrita do indice, o vigia (--enforcar --carencia 0) so' RELATA sob a pausa e RESTAURARIA sem ela
(controle de utilidade), pinar rc 0, a pausa SO' sai depois do pino, verificar rc 0 e PINO_MEMORY.json == sha256 do MEMORY.md da copia; (b) controles negativos (memoria.py com sha16 diferente do pino => para; pausa alheia => para e fica; pinar falha => a pausa PERMANECE; MEMORY.md acima do limite => recusa; verificar reprova);
(c) o PROPRIO superficies_v411.py (copia de bytes) com leitura e textos de ENSAIO (stubs): sem pausa valida recusa rc 6 sem escrever, com pausa grava, acima de 195 linhas ou 24 000 B recusa rc 3 sem escrever; (d) o PROPRIO chain_pos_rito_v411.sh (copia so' com as linhas de caminho trocadas) nos passos 7 a 9 num pacote SINTETICO: ordem, mensagens e codigos de saida
(a pausa PERMANECE quando falha antes do pino). O diretorio REAL de memoria nunca e' escrito: o harness compara o sha256 de MEMORY.md, fila\PINO_MEMORY.json e fila\fila.jsonl (e a ausencia de fila\PAUSA_VIGIA.json) antes e depois e REGISTRA a prova.
O PINO do memoria.py (PINO_MEMORIA_PY_v411.json) e' ato da GERENCIA (pino_memoria_py_v411.py): se ele ja' existe na pasta da cadeia, a fila o usa; se NAO existe, no ENSAIO (ou com --pino-emulado) o harness o EMULA a partir do memoria.py real (so' leitura), grava-o na pasta do harness com a marca _emulado_pelo_harness e o veredito DIZ que o pino foi emulado.
(2) O que o harness_textos_ensaio_v411.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, a copia do sidecar e do selo, o handoff com os DOIS paragrafos do README/site, o aviso de que o do testemunho segue como esta e a lista do sidecar) e o main do registrar_mapa; e o b3_recibo_v411.py com recibos SINTETICOS.
O sandbox e' uma ARVORE ISOLADA: work\cadeia_de_selo\v411 (pacote com ESPERADOS, o manifesto do artefato como CANDIDATO_v411.json, PINOS_BN, base_v410, insumos (o resultado pinado do Teste da Unica Palavra, que mora na v397, ganha uma COPIA em insumos\fase9 so' no sandbox), quadro_v397 e runtime_quadro_v397, o acom_conferencias_v411,
o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + as pastas irmas v410 a v399 (o delta_v411 importa o delta_v410 e, por ele, os anteriores) + TODO arquivo da casa (abaixo de Central de Patentes: work e Chatgpt) que o delta_v411 e os deltas herdados abrem ou conferem ao importar, ESPELHADO no sandbox na mesma posicao relativa (a lista e' MEDIDA na hora, instrumentando
open/exists/isfile/isdir/getsize na importacao do delta real; nada digitado) + nos\ (o Nos EMULADO montado do falso Nos de ENSAIO ou de dry_v411, com o SIDECAR gerado pela funcao do proprio artefato) + memory\ (uma COPIA da memoria, para o fechar e o fila_info) + work\cunhagens_13out (as falas do operador).
O conferidor REAL roda no proprio pacote do sandbox (SEM -I). As copias dos scripts (leitura, textos) trocam SO' a constante de caminho do Nos por caminho do sandbox; o fechar recebe a memoria por V411_MEMORIA_DIR (sem trocar linha nenhuma); o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais e' so' essas linhas).
Os scripts do sandbox rodam SEM V411_ENSAIO_TOPO_PROPOSTO no ambiente (o sandbox e' uma arvore "real" emulada); so' o conferidor leva a variavel no ensaio (a copia de import do um.py que ele faz vai para a pasta do ensaio, nao para C:\t\k411c).
O que ele prova no fechar: fechar_v411.py sai com rc 0 e grava o handoff (guarda P18 limpa) com os DOIS paragrafos do README/site entre os marcadores (o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o da v411 (o teste decisivo)
igual ao gerado do core e aprovado por T.verificar_paragrafo_v411; nenhuma nota ao lado do paragrafo da v410), a frase de que os paragrafos anteriores SEGUEM COMO ESTAO e a lista do sidecar, o handoff do Nos, os dois diffs (o do kernel e' vazio de modulos novos), o manifesto (com o estado da fila e o resumo do h0dn_bg1_v411) e o arquivo,
e copia o sidecar e o selo para v411_selo; RECUSA (rc 2, sem handoff) sem o recibo do religamento, com um recibo do B(n) que declara salto, com o resultado pinado adulterado, com o numero lido adulterado, com um numero do traducao_turing_v409, do tetelestai_terminal_v408, do psion_canto_v407 ou do fechamento_v406 (herdados) adulterado, com uma chave antiga dita mudada,
com a direcao do testemunho invertida, com o h0dn_bg1_v411 ausente, nao selado, nao aberto, com checagem falha, com valor adulterado (nas duas linhas), ramo trocado, beta errado, veredito trocado, observed_vector_read falso, token proibido, a frase velha da v410, a F67 sem a linha das Cefeidas livres, sem o resumo no selo, com um registro da v410 recriado ausente ou nao selado,
com o cunhagens_v411 ou o kh_n1_cobertura_v411 adulterado, com uma bandeira ou um modulo novo, com a escada diferente, com o handoff que traga a frase velha da v410, token proibido, a palavra da prova emendada ao nome do acoplamento ou sem as quatro obrigacoes do primario no mesmo bloco (F67), com uma ancora principal fora do trio e com o sidecar adulterado ou ausente;
registrar_mapa_v411.py (main) monta o JSON e imprime o comando; o S6d (textos_custodia_handoff_v411.main) anexa os textos da custodia ao handoff que o fechar gravou. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v410): a prova e' do CODIGO do fechar e do b3_recibo, nao de um B(n) real.
ENTRADAS DO ENSAIO (V411_ENSAIO_TOPO_PROPOSTO=1): C:\t\k411c\ensaio_topo_proposto\PRONTO_PARA_O_POS_RITO.json (sem ele o harness RECUSA com rc 3, sem escrever nada; --so-fila nao o exige). Chaves LIDAS (todas opcionais; ausente => o caminho padrao do delta_v411, dito no resumo; presente e inexistente => RECUSA rc 4):
  falso_nos, dry, core, selo, stdout, artigo_pt, artigo_en, esperados, manifesto, ensaio_a_seco, pinos_bn, formal_map, artefato (o caminho do um.py de ensaio) e artefato_sha16 (cruzado com o sha16 do manifesto, de ESPERADOS e do um.py).
SAIDAS: no ensaio, tudo vai para C:\t\k411c\ensaio_topo_proposto\pos_rito\ (harness_saida_v411\ para a memoria_copia, o sandbox e os resultados; os resumos HARNESS_FECHAR_SANDBOX_v411.json e FILA_MEMORIA_ENSAIO_v411.json em DL.saida(pos_rito\...)); fora do ensaio, as copias ficam em C:\t\h411 e os resumos em pos_rito\ (como antes). NADA e' escrito em work\ no ensaio.
uso: python -B -X utf8 harness_fechar_sandbox_v411.py [--manter] [--nao-exigir-refazer] [--so-fila] [--sem-fila] [--pino-emulado] [--out <nome>]   (rc 0 = tudo passou; rc 3 = PRONTO_PARA_O_POS_RITO.json ausente (ensaio); rc 4 = precondicao nao satisfeita, nada foi rodado; fora do ensaio, sem a flag EXIGE refazer_out_v411.txt com '== FIM' e mais novo que o ESPERADOS;
--nao-exigir-refazer so' vale FORA do ensaio e so' para depurar (o resumo DIZ que a regeneracao nao foi comprovada e vai para HARNESS_FECHAR_SANDBOX_v411_DEPURACAO_sem_refazer.json); --so-fila: so' a fila da memoria (nao depende de textos_v411, de leitura_v411 nem do PRONTO) e grava HARNESS_FECHAR_SANDBOX_v411_SO_FILA.json; --sem-fila: so' o fechar)"""
import builtins, datetime, glob, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
sys.path.insert(0, PKG)
import delta_v411 as DLX  # noqa: E402   (UMA instancia: o delta REAL da pasta da cadeia; com V411_ENSAIO_TOPO_PROPOSTO=1 ele aponta a rodada para C:\t\k411c\ensaio_topo_proposto)
ENSAIO = bool(DLX.ENSAIO_TOPO_PROPOSTO)
OUT_NOME = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "harness_saida_v411"   # --out <nome>: pasta propria da rodada (duas rodadas simultaneas na mesma pasta se pisam)
POS_SAIDA = DLX.saida("pos_rito")   # onde vao os resumos (DL.saida: no real, pos_rito\ da cadeia, como sempre; no ensaio, C:\t\k411c\ensaio_topo_proposto\pos_rito)
OUT = os.path.join(POS_SAIDA, OUT_NOME) if ENSAIO else os.path.join("C:" + os.sep, "t", "h411", OUT_NOME); SB = os.path.join(OUT, "fechar_sandbox")
from guarda_p18_v411 import violacoes  # noqa: E402
MANTER = "--manter" in sys.argv; NAO_REFAZER = "--nao-exigir-refazer" in sys.argv; SO_FILA = "--so-fila" in sys.argv; SEM_FILA = "--sem-fila" in sys.argv; PINO_EMULAR = "--pino-emulado" in sys.argv
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(open(p, "rb").read())
rdj = lambda p: json.load(open(p, encoding="utf-8"))
R = {"inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "problemas": [], "etapas": {}, "ensaio_topo_proposto": ENSAIO}
# v411: as chaves do MANIFESTO de incorporacao que fechar_v411.py grava (nomes versionados: *_v411 = os registros desta versao (h0dn_bg1_v411 e os dois specs); *_v410 = os da v410 RECRIADOS; *_v409 = a traducao_turing_v409 e os dois specs HERDADOS; *_v408, *_v407, *_v406 = os herdados dessas versoes; *_v405 = os treze da v405 selada, e assim por diante;
# lidas do dicionario `m` de fechar_v411.py: nao ha' chaves de bundle novo: o kernel e' o da v410)
MAN_CHAVES = ("registros_v411", "registros_v410", "registros_v409", "registros_v408", "registros_v407", "registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v411", "registros_funcao_v410", "registros_funcao_v409", "registros_funcao_v408", "registros_funcao_v407", "registros_funcao_v406",
              "ancoras_v411", "ancoras_v410", "ancoras_v409", "ancoras_v408", "ancoras_v407", "ancoras_v406", "bandeiras_v411", "bandeiras_ate_v410", "chaves_v407", "chaves_v406", "f2b_errata", "bandeiras_do_gate_recriado", "funcoes_v410_recriadas", "funcoes_v409_recriadas", "funcoes_v408_recriadas", "funcoes_v407_recriadas", "funcoes_v406_recriadas", "funcoes_v405_recriadas", "funcoes_v404_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas",
              "pedras_v410_como_registro", "pedras_v409_como_registro", "pedras_v408_como_registro", "pedras_v407_como_registro", "pedras_v406_como_registro", "pedras_v405_como_registro", "falsidade_v401", "base_v410", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_v411", "paragrafos_anteriores_seguem_como_estao", "sidecar_acom", "fila_da_memoria", "h0dn_bg1_v411_resumo", "artefatos_nos", "artigos")


def falha(m):
    R["problemas"].append(m); print("  PROBLEMA:", m)


def recusa(m, rc=4):
    print("RECUSO:", m); sys.exit(rc)

# ---- PRONTO_PARA_O_POS_RITO.json (so' no ensaio e so' fora do --so-fila): o sinal da outra frente de que o ensaio terminou; as ENTRADAS vem dele (cada chave e' opcional: ausente => o caminho padrao do delta_v411, dito em ORIGEM; presente e inexistente => RECUSA rc 4)
PRONTO_ARQ = os.path.join(DLX.ENSAIO_DIR, "PRONTO_PARA_O_POS_RITO.json"); PRONTO = {}; ORIGEM = {}
if ENSAIO and not SO_FILA:
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


DRY = entrada("dry", DLX.DRY_DIR); FALSO_NOS = entrada("falso_nos", DLX.FALSO_NOS_DIR)
P_ESP = entrada("esperados", DLX.saida("ESPERADOS_v411.json")); P_MAN = entrada("manifesto", DLX.MANIFESTO_ARQ); P_ENS = entrada("ensaio_a_seco", DLX.saida("ensaio_a_seco_v411.json")); P_PINOS = entrada("pinos_bn", DLX.saida("PINOS_BN_v411.json")); P_FORMAL = entrada("formal_map", DLX.FORMAL_MAP_ARQ)
P_REFAZER = os.path.join(PKG, "refazer_out_v411.txt")   # (so' fora do ensaio)
_FN_CORE = entrada("core", os.path.join(FALSO_NOS, "um_absoluto.json")); _FN_SELO = entrada("selo", os.path.join(FALSO_NOS, "um_absoluto_selo.json")); _FN_STD = entrada("stdout", os.path.join(FALSO_NOS, "rodada_v411_stdout.txt"))
_FN_PT = entrada("artigo_pt", os.path.join(FALSO_NOS, "um_absoluto_pt.txt")); _FN_EN = entrada("artigo_en", os.path.join(FALSO_NOS, "um_absoluto_en.txt"))
CAND_ARQ = entrada("artefato", DLX.CANDIDATO_ARQ)


def _liga(src, dst):
    """hardlink (o arquivo e' so' lido) ou copia; o destino nunca e' escrito depois."""
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    try:
        os.link(src, dst)
    except OSError:
        shutil.copyfile(src, dst)

# =====================================================================================================================================================
#  (1) A FILA DA MEMORIA -- ensaio em COPIA do diretorio de memoria
# =====================================================================================================================================================
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
# (AVISO da gerencia, 09/11) a pasta VEDADA da entrega do Kimi (DL.H0DN_PASTA_VEDADA_V410, lida do delta REAL ja' importado): nada dela entra na copia da memoria nem no espelho da casa; a exclusao e' por medida
_VEDADO = os.path.normcase(os.path.abspath(DLX.H0DN_PASTA_VEDADA_V410))
_sob_vedado = lambda p_: (lambda q_: q_ == _VEDADO or q_.startswith(_VEDADO + os.sep))(os.path.normcase(os.path.abspath(p_)))
assert not _sob_vedado(MEM_REAL) and not _sob_vedado(PKG), "VEDADO: a memoria ou o pacote estariam sob a pasta vedada"
FILA_PY_REAL = os.path.join(HERE, "fila_memoria_v411.py"); CHAIN_PY = os.path.join(HERE, "chain_pos_rito_v411.sh"); SUP_PY = os.path.join(HERE, "superficies_v411.py")
QUEM = "claude-c1 pos-rito v411"; PY_EXE = sys.executable
# o PINO do memoria.py (PINO_MEMORIA_PY_v411.json) e' ato da GERENCIA (pino_memoria_py_v411.py). Se existe na pasta da cadeia, a fila o usa; se NAO existe, no ENSAIO (ou com --pino-emulado) o harness o EMULA a partir do memoria.py real (so' leitura) e DIZ (PINO_EMULADO);
# fora do ensaio, sem o pino real, RECUSA. O helper da fila roda de uma COPIA (pacote_fila\pos_rito\fila_memoria_v411.py, com o pino ao lado: o helper le o pino por PK = a pasta acima dele).
os.makedirs(OUT, exist_ok=True)
FILA_PK = os.path.join(OUT, "pacote_fila"); shutil.rmtree(FILA_PK, ignore_errors=True); os.makedirs(os.path.join(FILA_PK, "pos_rito"))
PINO_REAL = os.path.join(PKG, "PINO_MEMORIA_PY_v411.json"); PINO_EMULADO = False; PINO_ARQ = os.path.join(FILA_PK, "PINO_MEMORIA_PY_v411.json")
if os.path.isfile(PINO_REAL):
    shutil.copyfile(PINO_REAL, PINO_ARQ)
elif ENSAIO or PINO_EMULAR:
    _mb = open(os.path.join(MEM_REAL, "fila", "memoria.py"), "rb").read(); _hm = sha(_mb)
    open(PINO_ARQ, "w", encoding="utf-8").write(json.dumps({"contrato": "PINO_MEMORIA_PY_v411", "path": os.path.join(MEM_REAL, "fila", "memoria.py"), "sha256": _hm, "sha16": _hm[:16], "bytes": len(_mb),
                                                              "_emulado_pelo_harness": "PINO EMULADO: pino_memoria_py_v411.py ainda nao foi rodado pela gerencia; calculado na hora do memoria.py real (so' leitura)"}, indent=1))
    PINO_EMULADO = True
else:
    recusa("o pacote da v411 nao tem PINO_MEMORIA_PY_v411.json (a gerencia roda pino_memoria_py_v411.py; ou use --pino-emulado)")
FILA_PY = os.path.join(FILA_PK, "pos_rito", "fila_memoria_v411.py"); shutil.copyfile(FILA_PY_REAL, FILA_PY)
R["pino_do_memoria_py"] = {"emulado": PINO_EMULADO, "arquivo": PINO_ARQ, "sha16": rdj(PINO_ARQ)["sha16"]}
FM = os.path.join(OUT, "memoria_copia")                      # a copia pedida pela gerencia: harness_saida_v411\memoria_copia
FILA_EV = {"contrato": "FILA_MEMORIA_ENSAIO_v411", "checks": [], "cenarios": {}, "nota": "ensaio em COPIA; o diretorio real de memoria nunca e' escrito (prova no fim)"}


def chk(nome, cond, det=""):
    ok = bool(cond)
    FILA_EV["checks"].append({"check": nome, "ok": ok, "det": str(det)[:300]})
    if not ok:
        falha("[fila] %s %s" % (nome, str(det)[:240]))
    return ok


def prova_real():
    """sha256/bytes/mtime dos arquivos do diretorio REAL de memoria que o ensaio jamais pode tocar (None = nao existe)."""
    out = {}
    for rel in ("MEMORY.md", os.path.join("fila", "PINO_MEMORY.json"), os.path.join("fila", "fila.jsonl"), os.path.join("fila", "PAUSA_VIGIA.json")):
        p = os.path.join(MEM_REAL, rel)
        out[rel.replace(os.sep, "/")] = ({"sha256": fsha(p), "bytes": os.path.getsize(p), "mtime_ns": os.stat(p).st_mtime_ns} if os.path.exists(p) else None)
    return out


def mk_memoria_copia(dst):
    """(AVISO da gerencia, 09/11) a pasta VEDADA da entrega do Kimi (DL.H0DN_PASTA_VEDADA, lida do delta real) nunca entra na copia: a exclusao e' explicita, por medida (_sob_vedado), mesmo que ela nao viva sob a memoria. COPIA do diretorio de memoria: os arquivos NAO-.bak do topo (menos os que ja' trazem 'v411' no nome, para o ensaio nao depender de o rito real ja' ter rodado) + fila\\ inteira (menos fila.lock, temporarios e a PAUSA_VIGIA.json, se houver). mtimes preservados."""
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
    _ved = _sob_vedado   # (AVISO 09/11) VEDADO: nada da pasta da entrega do Kimi entra na copia (a pasta e' lida do texto do delta no topo deste arquivo)
    n = tot = 0
    for f in sorted(os.listdir(MEM_REAL)):
        p = os.path.join(MEM_REAL, f)
        if os.path.isfile(p) and ".bak" not in f and ".tmp" not in f and "v411" not in f and not _ved(p):
            shutil.copy2(p, os.path.join(dst, f)); n += 1; tot += os.path.getsize(p)
    fs = os.path.join(MEM_REAL, "fila")
    for r, ds, fl in os.walk(fs):
        rel = os.path.relpath(r, fs); os.makedirs(os.path.join(dst, "fila", rel), exist_ok=True)
        for f in fl:
            if f == "fila.lock" or ".tmp" in f or f == "PAUSA_VIGIA.json" or _ved(os.path.join(r, f)):   # (VEDADO: a pasta do Kimi, explicitamente)
                continue
            shutil.copy2(os.path.join(r, f), os.path.join(dst, "fila", rel, f)); n += 1; tot += os.path.getsize(os.path.join(r, f))
    return {"arquivos": n, "bytes": tot}


def env_mem(d, **extra):
    e = dict(os.environ); e["V411_MEMORIA_DIR"] = d; e["MEMORIA_DIR"] = d; e["PYTHONIOENCODING"] = "utf-8"; e.pop("MEMORIA_GERENCIA", None); e.update(extra)
    return e


def ult_json(so):
    for t in (so.strip(), (so.strip().splitlines() or [""])[-1]):
        try:
            return json.loads(t) if t else None
        except ValueError:
            pass
    return None


def fila(op, d, *args):
    """o helper REAL do chain (fila_memoria_v411.py) contra a pasta d."""
    p = subprocess.run([PY_EXE, "-I", "-B", "-X", "utf8", FILA_PY, op] + list(args), capture_output=True, env=env_mem(d))
    so = p.stdout.decode("utf-8", "replace"); return p.returncode, ult_json(so), so, p.stderr.decode("utf-8", "replace")


def memoria(d, *args):
    """o memoria.py da COPIA (MEMORIA_DIR = a copia; MEMORIA_GERENCIA = claude-c1)."""
    p = subprocess.run([PY_EXE, "-X", "utf8", os.path.join(d, "fila", "memoria.py")] + list(args), capture_output=True, env=env_mem(d, MEMORIA_GERENCIA="claude-c1"), cwd=os.path.join(d, "fila"))
    so = p.stdout.decode("utf-8", "replace"); return p.returncode, _json_inteiro(so), so, p.stderr.decode("utf-8", "replace")


def _json_inteiro(so):
    try:
        return json.loads(so.strip()) if so.strip() else None
    except ValueError:
        return ult_json(so)


pausa_de = lambda d: os.path.join(d, "fila", "PAUSA_VIGIA.json")
idx_de = lambda d: os.path.join(d, "MEMORY.md")


def escreve_atomico(p, b):
    tmp = p + ".tmp_harness"; open(tmp, "wb").write(b); os.replace(tmp, p)


def edita_indice(d):
    """o que a superficie faz ao indice, em miniatura (uma linha de handoff nova antes da do v410), numa COPIA, com backup de bytes."""
    p = idx_de(d); raw = open(p, "rb").read()
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_harness_v411", "wb").write(raw)
    linhas = raw.decode("utf-8").split("\n"); k = [i for i, l in enumerate(linhas) if "(handoff-v410-custodia.md)" in l and l.startswith("- [")]
    assert len(k) == 1, ("linha do handoff da custodia da v410 no MEMORY.md da copia", len(k))
    linhas.insert(k[0], "- [HANDOFF v411 (ensaio)](handoff-v411-custodia.md) — **v411 SELADA**")   # (curta de proposito: o ensaio da fila e sobre a ORDEM (pausa, escrita, pino, verificar), nao sobre o tamanho do indice; o indice real tem pouca folga de bytes ate a gerencia abri-la)
    novo = "\n".join(linhas).encode("utf-8"); escreve_atomico(p, novo)
    return {"antes": [len(raw), raw.count(b"\n")], "depois": [len(novo), novo.count(b"\n")]}


def enche_indice(d, linhas_alvo=None, bytes_alvo=None):
    """deixa o MEMORY.md da copia com `linhas_alvo` quebras de linha OU `bytes_alvo` bytes (acrescenta comentarios no fim), para os controles do limite."""
    p = idx_de(d); raw = open(p, "rb").read()
    if linhas_alvo is not None:
        while raw.count(b"\n") < linhas_alvo:
            raw += b"<!-- enchimento do harness -->\n"
    if bytes_alvo is not None:
        falta = bytes_alvo - len(raw) - len(b"<!--  -->\n")
        assert falta > 0, (len(raw), bytes_alvo)
        raw += b"<!-- " + b"x" * falta + b" -->\n"
        assert len(raw) == bytes_alvo, (len(raw), bytes_alvo)
    escreve_atomico(p, raw)
    return [len(raw), raw.count(b"\n")]


def hashes_topo(d):
    return {f: fsha(os.path.join(d, f)) for f in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, f))}


def ordem_do_chain():
    """a ORDEM das operacoes da fila, LIDA DO TEXTO do chain (linhas que nao sao comentario), e as linhas-ancora."""
    ls = open(CHAIN_PY, encoding="utf-8").read().split("\n")
    ops = []
    for i, l in enumerate(ls):
        if l.lstrip().startswith("#"):
            continue
        m = re.search(r'\$FILA" (guardas|pausa-criar|pinar|pausa-remover|verificar)', l)
        if m:
            ops.append((i, m.group(1)))
    ach = lambda pad: [i for i, l in enumerate(ls) if not l.lstrip().startswith("#") and pad in l]
    return ops, {"superficies_real": ach('superficies_v411.py"; sr=$?'), "porta": ach('"$PORTA" >'), "validacao_195": ach('[ "$l" -le 195 ]'), "sem_copias": ach("--copias")}


def ensaio_da_fila():
    print("== (1) A FILA DA MEMORIA em COPIA (nada real e' escrito)")
    E = FILA_EV; t0 = time.time()
    if not (os.path.isfile(FILA_PY) and os.path.isfile(CHAIN_PY) and os.path.isfile(SUP_PY) and os.path.isfile(os.path.join(MEM_REAL, "fila", "memoria.py"))):
        recusa("faltam fila_memoria_v411.py, chain_pos_rito_v411.sh, superficies_v411.py ou o memoria.py real")
    # ---- a ORDEM do chain (lida do texto)
    ops, anc = ordem_do_chain()
    seq = [o for _, o in ops]
    chk("a ordem das operacoes da fila no chain: guardas (passo 0); pausa-criar (passo 7); pausa-criar (renovar), pinar, pausa-remover, verificar (passo 9)", seq == ["guardas", "pausa-criar", "pausa-criar", "pinar", "pausa-remover", "verificar"], seq)
    if len(ops) == 6 and anc["superficies_real"] and anc["porta"] and anc["validacao_195"]:
        i = [l for l, _ in ops]
        ordem_ok = i[0] < i[1] < anc["superficies_real"][0] < anc["porta"][0] < anc["validacao_195"][-1] < i[2] < i[3] < i[4] < i[5]
        chk("no TEXTO do chain: guardas < pausa-criar < superficies (real) < espelho < validacao do MEMORY.md (195) < pausa-criar < pinar < pausa-remover < verificar", ordem_ok, {"linhas_das_operacoes": i, "ancoras": {k: v[:3] for k, v in anc.items()}})
    else:
        chk("as ancoras do chain (superficies real, espelho, validacao 195) foram achadas", False, {"ops": ops, "ancoras": anc})
    # ---- (a) a sequencia POSITIVA, na ordem do chain
    cp = mk_memoria_copia(FM); E["copia"] = dict(cp, caminho=FM)
    pino0 = rdj(os.path.join(FM, "fila", "PINO_MEMORY.json")); mem0 = fsha(idx_de(FM))
    tl = []

    def passo(nome, rc, j, extra=None):
        d = {"passo": nome, "rc": rc, "ok": (j or {}).get("ok"), "pausa_existe_depois": os.path.exists(pausa_de(FM)), "memory_md_sha16": fsha(idx_de(FM))[:16], "hora": time.strftime("%H:%M:%S")}
        d.update(extra or {}); tl.append(d); return d
    rc, j, so, se = fila("guardas", FM); passo("0. guardas", rc, j)
    chk("guardas: rc 0, memoria.py == o pino (sha16 lido de PINO_MEMORIA_PY_v411.json), sem pausa", rc == 0 and j and j.get("ok") and j.get("sem_pausa") is True and j.get("sha16") == j.get("sha16_pinado"), so[:300])
    chk("antes do passo 7 NAO existe fila\\PAUSA_VIGIA.json", not os.path.exists(pausa_de(FM)))
    rc, j, so, se = fila("pausa-criar", FM); passo("7. pausa-criar", rc, j)
    chk("pausa-criar: rc 0 e a pausa existe", rc == 0 and os.path.exists(pausa_de(FM)), so[:300])
    pz = rdj(pausa_de(FM)); ate = datetime.datetime.fromisoformat(pz["ate"]); agora = datetime.datetime.now().astimezone(); dm = (ate - agora).total_seconds() / 60
    chk("a pausa traz quem/ate/motivo exatos, 'ate' com fuso e ~ agora + 1 h", pz.get("quem") == QUEM and pz.get("motivo") == "pos-rito v411 escreve o indice" and ate.tzinfo is not None and 55 <= dm <= 61 and sorted(pz) == ["ate", "motivo", "quem"], {"pausa": pz, "minutos_a_frente": round(dm, 1)})
    chk("a escrita da pausa foi atomica: nenhum temporario sobrou em fila\\", not glob.glob(pausa_de(FM) + ".tmp*"))
    # a escrita do indice (passo 7) com a pausa posta
    assert os.path.exists(pausa_de(FM))
    ed = edita_indice(FM); passo("7. escrita do MEMORY.md (com a pausa posta)", 0, {"ok": True}, {"edicao": ed})
    chk("o MEMORY.md foi editado COM a pausa posta e cabe no limite (<=195 linhas, <24000 B)", ed["depois"][1] <= 195 and ed["depois"][0] < 24000 and fsha(idx_de(FM)) != mem0, ed)
    # o vigia sob a pausa: so' RELATA (nao restaura)
    mem_ed = fsha(idx_de(FM))
    rc, j, so, se = memoria(FM, "vigiar", "--enforcar", "--carencia", "0"); passo("7. vigiar --enforcar --carencia 0 (SOB a pausa)", rc, j, {"estado": (j or {}).get("estado")})
    chk("sob a pausa o vigia (--enforcar --carencia 0) so' RELATA a divergencia e NAO restaura o indice", rc == 4 and fsha(idx_de(FM)) == mem_ed and "PAUSA" in str((j or {}).get("estado")), {"rc": rc, "estado": (j or {}).get("estado"), "memory_md_igual_ao_editado": fsha(idx_de(FM)) == mem_ed})
    # controle de UTILIDADE: sem a pausa o mesmo vigia RESTAURARIA o indice (numa 2a copia)
    F2 = FM + "_sem_pausa"; shutil.rmtree(F2, ignore_errors=True); shutil.copytree(FM, F2)
    os.remove(pausa_de(F2)); rc2, j2, so2, se2 = memoria(F2, "vigiar", "--enforcar", "--carencia", "0")
    chk("CONTROLE DE UTILIDADE: SEM a pausa o mesmo vigia RESTAURA o indice ao pinado (a pausa evita exatamente isto)", fsha(idx_de(F2)) == mem0 and rc2 in (0, 4), {"rc": rc2, "estado": (j2 or {}).get("estado"), "memory_md_restaurado_ao_pinado": fsha(idx_de(F2)) == mem0})
    shutil.rmtree(F2, ignore_errors=True)
    rc, j, so, se = fila("pausa-criar", FM); passo("9. pausa-criar (renovar)", rc, j)
    chk("renovar a pausa: rc 0 e renovada=true", rc == 0 and j.get("renovada") is True, so[:200])
    rc, j, so, se = fila("pinar", FM); passo("9. pinar", rc, j)
    pn = rdj(os.path.join(FM, "fila", "PINO_MEMORY.json")); mem_final = open(idx_de(FM), "rb").read()
    chk("pinar: rc 0 (MEMORIA_GERENCIA=claude-c1 memoria.py pinar --motivo \"pos-rito v411\"), por claude-c1, e a pausa SEGUE posta ate' depois do pino", rc == 0 and j.get("ok") and pn.get("por") == "claude-c1" and "pos-rito v411" in str(pn.get("via")) and os.path.exists(pausa_de(FM)), {"rc": rc, "via": pn.get("via"), "por": pn.get("por")})
    chk("PINO_MEMORY.json (da copia) == sha256 do MEMORY.md (da copia)", pn.get("sha256") == sha(mem_final) and pn.get("bytes") == len(mem_final) and pn.get("linhas") == mem_final.count(b"\n"), {"pino": str(pn.get("sha256"))[:16], "md": sha(mem_final)[:16]})
    chk("o espelho PINO_MEMORY_conteudo.md == o MEMORY.md pinado (byte a byte)", open(os.path.join(FM, "fila", "PINO_MEMORY_conteudo.md"), "rb").read() == mem_final)
    chk("o pino mudou (era o do indice antigo)", pn.get("sha256") != pino0.get("sha256"))
    rc, j, so, se = fila("pausa-remover", FM); passo("9. pausa-remover (SO' depois do pino)", rc, j)
    chk("pausa-remover: rc 0 e a pausa saiu", rc == 0 and not os.path.exists(pausa_de(FM)), so[:200])
    rc, j, so, se = fila("verificar", FM); passo("9. verificar", rc, j, {"violacoes": (j or {}).get("violacoes")})
    chk("verificar: rc 0 e ok:true (nenhuma violacao)", rc == 0 and j and j.get("ok") is True and not j.get("violacoes"), so[:300])
    rc, j, so, se = memoria(FM, "vigiar"); passo("9. vigiar (sem enforcar)", rc, j, {"estado": (j or {}).get("estado")})
    chk("depois do pino o vigia diz OK (indice == pino)", rc == 0 and (j or {}).get("estado") == "OK", {"rc": rc, "estado": (j or {}).get("estado")})
    E["cenarios"]["a_sequencia_positiva"] = tl
    # ---- (b) controles negativos do helper (cada um numa copia nova)
    NEG = []; FN = os.path.join(OUT, "memoria_neg")

    def neg(nome, ok, det=""):
        NEG.append({"controle": nome, "ok": bool(ok), "det": str(det)[:300]})
        print("  controle negativo da fila: %-96s %s" % (nome[:96], "RECUSOU/PAROU como esperado" if ok else "FALHOU"))
        if not ok:
            falha("[fila] controle negativo: %s: %s" % (nome, str(det)[:200]))
    # N1: memoria.py com sha16 diferente do pino => guardas PARA, nada criado, indice intocado
    mk_memoria_copia(FN); m0 = fsha(idx_de(FN)); mp = os.path.join(FN, "fila", "memoria.py"); escreve_atomico(mp, open(mp, "rb").read() + b"\n# alterado pelo controle negativo do harness\n")
    rc, j, so, se = fila("guardas", FN)
    neg("memoria.py com sha16 DIFERENTE do pino => guardas PARA (rc 1), sem criar a pausa e sem tocar o indice", rc == 1 and j and j.get("ok") is False and j.get("sha16") != j.get("sha16_pinado") and not os.path.exists(pausa_de(FN)) and fsha(idx_de(FN)) == m0, so[:260])
    # N2: pausa de OUTRO dono => guardas (com e sem --retomada), pausa-criar e pausa-remover recusam e a pausa fica intacta
    mk_memoria_copia(FN); alheia = json.dumps({"quem": "outra sessao", "ate": (datetime.datetime.now().astimezone() + datetime.timedelta(hours=1)).isoformat(timespec="seconds"), "motivo": "outro motivo"}).encode(); escreve_atomico(pausa_de(FN), alheia)
    r1 = fila("guardas", FN); r2 = fila("guardas", FN, "--retomada"); r3 = fila("pausa-criar", FN); r4 = fila("pausa-remover", FN)
    neg("pausa de OUTRO dono: guardas (com e sem --retomada), pausa-criar e pausa-remover recusam (rc 1) e a pausa fica intacta, byte a byte", r1[0] == 1 and r2[0] == 1 and r3[0] == 1 and r4[0] == 1 and open(pausa_de(FN), "rb").read() == alheia, [r1[0], r2[0], r3[0], r4[0]])
    # N3: pausa NOSSA deixada por uma execucao anterior: guardas sem --retomada recusa; com --retomada aceita; pausa-criar renova
    mk_memoria_copia(FN); fila("pausa-criar", FN)
    r1 = fila("guardas", FN); r2 = fila("guardas", FN, "--retomada"); r3 = fila("pausa-criar", FN)
    neg("pausa NOSSA de uma execucao anterior: guardas SEM --retomada recusa (rc 1); COM --retomada aceita (rc 0, com aviso); pausa-criar a renova", r1[0] == 1 and r2[0] == 0 and (r2[1] or {}).get("aviso") and r3[0] == 0 and (r3[1] or {}).get("renovada") is True, [r1[0], r2[0], r3[0]])
    # N4: pinar SEM a nossa pausa posta => recusa e o pino nao muda
    mk_memoria_copia(FN); p0 = fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")); edita_indice(FN)
    rc, j, so, se = fila("pinar", FN)
    neg("pinar SEM a pausa posta => recusa (rc 1) e o pino NAO muda", rc == 1 and fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")) == p0, so[:240])
    # N5: pinar FALHA (o livro da fila perde a cabeca) => rc 1 e a PAUSA PERMANECE; o pino nao muda
    mk_memoria_copia(FN); p0 = fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")); fila("pausa-criar", FN); edita_indice(FN)
    cab = os.path.join(FN, "fila", "CABECA.json"); escreve_atomico(cab, b"{ isto nao e' json")
    rc, j, so, se = fila("pinar", FN)
    neg("pinar FALHA (CABECA.json do livro corrompida) => o helper sai rc 1, a PAUSA PERMANECE e o pino NAO muda (o chain PARA e nao a remove)", rc == 1 and j and j.get("ok") is False and os.path.exists(pausa_de(FN)) and fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")) == p0, so[:300])
    # N6: MEMORY.md acima do limite (linhas e bytes) => pinar recusa, o pino nao muda, a pausa fica
    for rotulo, kw in (("196 linhas (limite 195)", {"linhas_alvo": 196}), ("24 000 B (limite: abaixo de 24 000)", {"bytes_alvo": 24000})):
        mk_memoria_copia(FN); p0 = fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")); fila("pausa-criar", FN); enche_indice(FN, **kw)
        rc, j, so, se = fila("pinar", FN)
        neg("MEMORY.md com %s => pinar recusa (rc 1), o pino NAO muda e a pausa fica" % rotulo, rc == 1 and "limite" in str((j or {}).get("erro")) and fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")) == p0 and os.path.exists(pausa_de(FN)), so[:260])
    # N7: verificar REPROVA (um topico sem frontmatter) => rc 1 e a violacao e' listada
    mk_memoria_copia(FN); escreve_atomico(os.path.join(FN, "zz_topico_sem_frontmatter.md"), b"sem frontmatter\n")
    rc, j, so, se = fila("verificar", FN)
    neg("verificar REPROVA (topico sem frontmatter na pasta de memoria) => rc 1, ok:false e a violacao listada (o TOPICO NOVO da v411 precisa de frontmatter name/description)", rc == 1 and j and j.get("ok") is False and any("zz_topico_sem_frontmatter" in str(v) for v in (j.get("violacoes") or [])), so[:300])
    E["controles_negativos_do_helper"] = NEG
    # ---- (c) o PROPRIO superficies_v411.py (copia de bytes) com leitura e textos de ENSAIO
    ensaio_superficies()
    # ---- (d) o PROPRIO chain nos passos 7 a 9, em pacote sintetico
    ensaio_chain()
    shutil.rmtree(FN, ignore_errors=True)
    E["segundos"] = round(time.time() - t0, 1)
    print("  fila da memoria: %d checagens, %d falharam" % (len(E["checks"]), sum(1 for c in E["checks"] if not c["ok"])))


# ---------------------------------------------------------------- (c) o superficies_v411.py com stubs de leitura e textos
STUB_LEITURA = '''# -*- coding: utf-8 -*-
# STUB do harness da fila (NAO e' a leitura da cadeia): devolve uma V minima e sem problemas.
NOS = %(nos)r


def ler():
    return ({'data': '26/10/2026', 's16': %(s16)r}, [])
'''
STUB_TEXTOS = '''# -*- coding: utf-8 -*-
# STUB do harness da fila (NAO sao os textos da cadeia): blocos curtos, limpos da guarda P18, com os marcadores que a superficie e o chain exigem.
TOPICO_NOVO = 'v411-selada-h0dn-aberto.md'
REGS = 'h0dn_bg1_v411 cunhagens_v411 kh_n1_cobertura_v411'


def _b(V, marca, extra=''):
    return '%s\\n## ENSAIO DO HARNESS (v411, bloco sintetico) %s\\n\\n%s %s %s\\n' % (marca, V['s16'], V['s16'], REGS, extra)


def atribuicao_da_gerencia(texto):
    return []


def linhagem(V):
    return _b(V, '<!-- linhagem_v411_selada -->')


def desenho(V):
    return _b(V, '<!-- adendo_v411_selada -->')


def atlas(V):
    return _b(V, '<!-- atlas_v411_selada -->')


def core_memory(V):
    return _b(V, '<!-- core_v411_selada -->')


def haja_luz(V):
    return _b(V, '<!-- haja_luz_v411_selada -->')


def id_missao(V):
    return '<!-- stub_id_missao_v411 -->'


def id_central(V):
    return '<!-- stub_id_central_v411 -->'


def topico_missao(V):
    return _b(V, T_ID_MISSAO, 'missao')


def topico_central(V):
    return _b(V, T_ID_CENTRAL, 'central')


def topico_estatuto(V):
    return _b(V, '<!-- v411_selada -->', 'estatuto')


def topico_novo(V):
    return '---\\nname: v411-selada-ensaio\\ndescription: "topico NOVO de ensaio do harness (frontmatter valido)"\\nmetadata:\\n  type: project\\n---\\n\\n# v411 SELADA (ensaio) %s\\n\\n%s\\n' % (V['s16'], REGS)


def aviso(V, reiv):
    return _b(V, '<!-- aviso_v411_selada -->')


def aviso_pulado():
    return '  (AVISO_GERENCIA.md: PULADO no ensaio)'


def marca_missao(V):
    return '**v411 SELADA 26/10 `%s` (ENSAIO)** · ' % V['s16']


def linha_handoff(V):
    return '- [HANDOFF v411 — ENSAIO DO HARNESS](handoff-v411-custodia.md) — **v411 SELADA** `%s` (linha sintetica do harness da fila)' % V['s16']


T_ID_MISSAO = '<!-- stub_id_missao_v411 -->'
T_ID_CENTRAL = '<!-- stub_id_central_v411 -->'
'''


def mk_superficies_stub(raiz, s16, nos):
    shutil.rmtree(raiz, ignore_errors=True); pos = os.path.join(raiz, "pos_rito"); os.makedirs(pos)
    shutil.copyfile(SUP_PY, os.path.join(pos, "superficies_v411.py"))
    shutil.copyfile(os.path.join(PKG, "guarda_p18_v411.py"), os.path.join(raiz, "guarda_p18_v411.py"))
    # D169 (12/11): o pacote de ENSAIO traz um delta STUB com SO' as duas frases da v410 («pre-registrado; nenhum dado observado lido»), lidas do delta REAL ja' importado: a guarda das superficies confere que elas NAO voltam como estado do teste (aberto uma vez)

    open(os.path.join(raiz, "delta_v411.py"), "w", encoding="utf-8").write("# STUB do harness da fila: so' as frases velhas da v410, lidas do delta_v411 real\n" + "".join("%s = %r\n" % (k_, getattr(DLX, k_)) for k_ in ("FRASE_H0DN_OBRIGATORIA_PT", "FRASE_H0DN_OBRIGATORIA_EN")))
    open(os.path.join(raiz, "guarda_frases_v411.py"), "w", encoding="utf-8").write("# STUB do harness da fila (a guarda real roda nos textos reais, no harness dos textos e no fechar)\ndef violacoes(t):\n    return []\n")
    open(os.path.join(pos, "leitura_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_LEITURA % {"nos": nos, "s16": s16})
    open(os.path.join(pos, "textos_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)
    return pos


def roda_sup(pos, d, *args, extra_env=None):
    e = env_mem(d); e.update(extra_env or {})
    p = subprocess.run([PY_EXE, "-I", "-B", "-X", "utf8", os.path.join(pos, "superficies_v411.py")] + list(args), capture_output=True, env=e, cwd=pos)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def ensaio_superficies():
    print("  -- (c) superficies_v411.py (copia de bytes) com leitura e textos de ENSAIO, V411_MEMORIA_DIR = a copia")
    E = FILA_EV; NEG = []; raiz = os.path.join(OUT, "superficies_stub"); FS = os.path.join(OUT, "memoria_sup")
    pos = mk_superficies_stub(raiz, "5a5a5a5a5a5a5a5a", os.path.join(raiz, "nos"))

    def neg(nome, ok, det=""):
        NEG.append({"controle": nome, "ok": bool(ok), "det": str(det)[:300]})
        print("  controle negativo das superficies: %-90s %s" % (nome[:90], "RECUSOU como esperado" if ok else "FALHOU"))
        if not ok:
            falha("[fila] superficies: %s: %s" % (nome, str(det)[:200]))
    chk("o superficies do ensaio e' a COPIA DE BYTES do superficies_v411.py real (so' a leitura e os textos sao stubs)", fsha(os.path.join(pos, "superficies_v411.py")) == fsha(SUP_PY))
    # S1: sem pausa => rc 6, NADA escrito
    mk_memoria_copia(FS); h0 = hashes_topo(FS); ls0 = sorted(os.listdir(FS))
    rc, so, se = roda_sup(pos, FS)
    neg("sem a fila\\PAUSA_VIGIA.json => a superficie RECUSA (rc 6) sem escrever nada (nenhum arquivo do topo mudou ou nasceu)", rc == 6 and "rc 6" in so and hashes_topo(FS) == h0 and sorted(os.listdir(FS)) == ls0, (rc, so[:200]))
    # S2: pausa ALHEIA e pausa VENCIDA => rc 6
    escreve_atomico(pausa_de(FS), json.dumps({"quem": "outra sessao", "ate": (datetime.datetime.now().astimezone() + datetime.timedelta(hours=1)).isoformat(timespec="seconds"), "motivo": "x"}).encode())
    rc, so, se = roda_sup(pos, FS); neg("pausa de OUTRO dono => rc 6, nada escrito", rc == 6 and "outro dono" in so and hashes_topo(FS) == h0, (rc, so[:200]))
    escreve_atomico(pausa_de(FS), json.dumps({"quem": QUEM, "ate": (datetime.datetime.now().astimezone() - datetime.timedelta(minutes=5)).isoformat(timespec="seconds"), "motivo": "x"}).encode())
    rc, so, se = roda_sup(pos, FS); neg("pausa NOSSA mas VENCIDA => rc 6, nada escrito", rc == 6 and "vencida" in so and hashes_topo(FS) == h0, (rc, so[:200]))
    os.remove(pausa_de(FS))
    # S3: pausa valida (criada pelo helper) => grava
    rc0, j0, so0, se0 = fila("pausa-criar", FS)
    lin_antes = open(idx_de(FS), "rb").read().count(b"\n")
    rc, so, se = roda_sup(pos, FS)
    ix = open(idx_de(FS), "rb").read()
    ls1 = sorted(os.listdir(FS))
    chk("com a pausa valida a superficie GRAVA (rc 0): MEMORY.md +1 linha com a linha do handoff v411 e a marca da missao; MEMORY_2 recebe a linha velha VERBATIM; backups de bytes _sup411", rc == 0 and b"HANDOFF v411" in ix and b"v411 SELADA 26/10" in ix and ix.count(b"\n") == lin_antes + 1 and any(".bak_" in f and f.endswith("_sup411") and f.startswith("MEMORY.md") for f in ls1) and any(f.startswith("MEMORY_2.md.bak_") for f in ls1), {"rc": rc, "linhas": ix.count(b"\n"), "saida": so[-300:]})
    chk("a superficie nao criou nem removeu a pausa (isso e' do chain)", os.path.exists(pausa_de(FS)))
    # S4: idempotente
    h1 = hashes_topo(FS); rc, so, se = roda_sup(pos, FS)
    chk("2a rodada IDEMPOTENTE: rc 0 e nada muda", rc == 0 and hashes_topo(FS) == h1, (rc, so[-200:]))
    # S4b (D169, 12/11): um bloco com H0DN COM a frase velha da v410 («pre-registrado; nenhum dado observado lido») => a guarda das superficies RECUSA (rc 4, 'D169' na saida), nada escrito; SEM ela => grava (rc 0)
    _ns_dl = {}; exec(open(os.path.join(raiz, "delta_v411.py"), encoding="utf-8").read(), _ns_dl)
    _lin_stub = "def linhagem(V):\n    return _b(V, '<!-- linhagem_v411_selada -->')"
    assert STUB_TEXTOS.count(_lin_stub) == 1, "o stub dos textos nao traz a funcao linhagem esperada"
    for _rot, _extra, _rc_esp in (("COM a frase velha da v410", "H0DN x BG1 ensaio: " + _ns_dl["FRASE_H0DN_OBRIGATORIA_PT"], 4), ("SEM a frase velha da v410", "H0DN x BG1 ensaio", 0)):
        open(os.path.join(pos, "textos_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS.replace(_lin_stub, "def linhagem(V):\n    return _b(V, '<!-- linhagem_v411_selada -->', %r)" % _extra))
        mk_memoria_copia(FS); fila("pausa-criar", FS); h0 = hashes_topo(FS); ls0 = sorted(os.listdir(FS))
        rc, so, se = roda_sup(pos, FS)
        if _rc_esp == 4:
            neg("bloco com H0DN %s (D169) => a superficie RECUSA (rc 4, 'D169' na saida), sem escrever nada" % _rot, rc == 4 and "D169" in so and hashes_topo(FS) == h0 and sorted(os.listdir(FS)) == ls0, (rc, so[:300]))
        else:
            chk("bloco com H0DN %s (D169) => a superficie GRAVA (rc 0)" % _rot, rc == 0, (rc, so[-200:]))
    open(os.path.join(pos, "textos_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)   # volta ao stub limpo para os passos seguintes
    # S5: limite (linhas) com pausa valida => rc 3 sem escrever; (bytes) idem
    for rotulo, kw in (("linhas (195 antes; +1 do handoff = 196 > 195)", {"linhas_alvo": 195}), ("bytes (24 300 B antes; a troca do gancho encolhe a linha da missao e o indice segue acima de 24 000 B)", {"bytes_alvo": 24300})):
        mk_memoria_copia(FS); enche_indice(FS, **kw); fila("pausa-criar", FS); h0 = hashes_topo(FS); ls0 = sorted(os.listdir(FS))
        rc, so, se = roda_sup(pos, FS)
        neg("MEMORY.md acima do limite em %s => RECUSA rc 3 com as CONTAGENS, sem escrever nada (a superficie NAO compacta)" % rotulo, rc == 3 and "CONTAGENS" in so and hashes_topo(FS) == h0 and sorted(os.listdir(FS)) == ls0, (rc, so[-300:]))
    # S6: o --copias explicito (passo 3 do chain) NAO exige a pausa e grava SO' na pasta dada
    FC = os.path.join(OUT, "memoria_sup_copias"); shutil.rmtree(FC, ignore_errors=True); os.makedirs(FC)
    for f in ("MEMORY.md", "MEMORY_2.md", "missao-ultima-flag-um-py.md", "central-de-patentes-estado.md", "estatuto-da-prova-07out.md"):
        shutil.copy2(os.path.join(MEM_REAL, f), os.path.join(FC, f))
    rc, so, se = roda_sup(pos, FS, "--copias", FC)
    chk("--copias <pasta> (o ensaio do passo 3): NAO exige a pausa e grava SO' na pasta dada (rc 0)", rc == 0 and b"HANDOFF v411" in open(idx_de(FC), "rb").read(), (rc, so[-200:]))
    shutil.rmtree(FC, ignore_errors=True); shutil.rmtree(FS, ignore_errors=True); shutil.rmtree(raiz, ignore_errors=True)
    E["controles_negativos_das_superficies"] = NEG


# ---------------------------------------------------------------- (d) o PROPRIO chain (passos 7 a 9) em pacote sintetico
CHAIN_CAMINHOS = ("PK", "TOOLS", "NOS", "UMEM_PADRAO", "ATLD", "HAJA", "RAIZ_CLAUDE", "AVISO", "PORTA", "INV")


def unix(p):
    p = os.path.abspath(p).replace("\\", "/")
    return "/" + p[0].lower() + p[2:] if len(p) > 1 and p[1] == ":" else p


def mk_chain_sandbox(raiz):
    """pacote SINTETICO para rodar os passos 7 a 9 do PROPRIO chain: so' as linhas de caminho do chain sao trocadas (contagem exata); superficies_v411.py real (so' as 4 linhas de caminho trocadas), fila_memoria_v411.py real, leitura e textos de ensaio, o espelho (PORTA) e
    as ferramentas das etapas 5/6 como stubs; o MEMORY.md/fila sao os da COPIA da memoria."""
    shutil.rmtree(raiz, ignore_errors=True)
    D = {k: os.path.join(raiz, k) for k in ("pack", "tools", "nos", "atlas", "haja", "raiz", "aviso", "porta", "inv", "nosvivo", "memory")}
    for k, v in D.items():
        os.makedirs(v)
    PKS = D["pack"]; POS = os.path.join(PKS, "pos_rito"); os.makedirs(os.path.join(PKS, "kernel")); os.makedirs(POS)
    mk_memoria_copia(D["memory"])
    um = os.path.join(D["nos"], "um.py"); open(um, "w", encoding="utf-8", newline="\n").write("# um.py SINTETICO do harness da fila\n"); s16 = fsha(um)[:16]
    open(os.path.join(PKS, "APLICADO_AO_CANONICO_20261026_000000.json"), "w", encoding="utf-8").write(json.dumps({"um_py_novo": {"sha16": s16}}))
    open(os.path.join(PKS, "ESPERADOS_v411.json"), "w", encoding="utf-8").write(json.dumps({"candidato_sha16": s16}))
    open(os.path.join(D["nos"], "rodada_v411_stdout.txt"), "w", encoding="utf-8", newline="\n").write("(stdout sintetico)\nRITO_RC=0\n")
    shutil.copyfile(PINO_ARQ, os.path.join(PKS, "PINO_MEMORIA_PY_v411.json")); shutil.copyfile(os.path.join(PKG, "guarda_p18_v411.py"), os.path.join(PKS, "guarda_p18_v411.py"))   # (o pino: o real, ou o EMULADO do harness)
    open(os.path.join(PKS, "guarda_frases_v411.py"), "w", encoding="utf-8").write("# STUB do harness da fila (a guarda real roda nos textos reais, no harness dos textos e no fechar)\ndef violacoes(t):\n    return []\n")
    shutil.copyfile(FILA_PY, os.path.join(POS, "fila_memoria_v411.py"))
    for f in ("textos_v411.py", "fechar_v411.py", "registrar_mapa_v411.py", "b3_recibo_v411.py", "leitura_v411.py"):
        open(os.path.join(POS, f), "w", encoding="utf-8", newline="\n").write("# stub do harness da fila (sem conteudo)\n")
    open(os.path.join(POS, "leitura_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_LEITURA % {"nos": D["nos"], "s16": s16})
    open(os.path.join(POS, "textos_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)
    # a superficie REAL, com as quatro linhas de caminho trocadas (a pasta de memoria, o Atlas, a Haja_Luz, o aviso)
    t = open(SUP_PY, encoding="utf-8").read()
    trocas = (('MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")', "MEM_REAL = %r" % D["memory"]),
              ('ATLD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory")', "ATLD = %r" % D["atlas"]),
              ('HAJA = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")', "HAJA = %r" % os.path.join(D["haja"], "CLAUDE.md")),
              ('AVISO = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "AVISO_GERENCIA.md")', "AVISO = %r" % os.path.join(D["aviso"], "AVISO_GERENCIA.md")))
    for a, b in trocas:
        assert t.count(a) == 1, ("linha de caminho da superficie nao e' unica", a[:60], t.count(a))
        t = t.replace(a, b)
    open(os.path.join(POS, "superficies_v411.py"), "w", encoding="utf-8", newline="\n").write(t)
    # o chain: so' as linhas de caminho
    c = open(CHAIN_PY, encoding="utf-8").read()
    novo = {"PK": unix(PKS), "TOOLS": unix(D["tools"]), "NOS": unix(D["nos"]), "UMEM_PADRAO": unix(D["memory"]), "ATLD": unix(D["atlas"]), "HAJA": unix(os.path.join(D["haja"], "CLAUDE.md")), "RAIZ_CLAUDE": unix(os.path.join(D["raiz"], "CLAUDE.md")),
            "AVISO": unix(os.path.join(D["aviso"], "AVISO_GERENCIA.md")), "PORTA": unix(os.path.join(D["porta"], "porta_memoria.py")), "INV": unix(D["inv"])}
    for k in CHAIN_CAMINHOS:
        c, n = re.subn(r'^%s="[^"\n]*"' % k, lambda m, k=k: '%s="%s"' % (k, novo[k]), c, count=0, flags=re.M)
        assert n == 1, ("variavel de caminho do chain nao e' unica", k, n)
    assert c.count("/c/IALD/NOS_VIVO/construir.py") == 2, c.count("/c/IALD/NOS_VIVO/construir.py")
    c = c.replace("/c/IALD/NOS_VIVO/construir.py", unix(os.path.join(D["nosvivo"], "construir.py")))
    open(os.path.join(POS, "chain_pos_rito_v411.sh"), "w", encoding="utf-8", newline="\n").write(c)
    # as ferramentas e superficies que o passo 0 exige: stubs vazios para tudo o que o chain lista (lido do TEXTO do chain) e ainda nao existe
    m = re.search(r'for f in (.*?); do\n\s*\[ -f "\$f" \] \|\| parar', c, re.S)
    assert m, "bloco de existencia do passo 0 nao achado"
    mapa = {"TOOLS": unix(D["tools"]), "PK": unix(PKS), "NOS": unix(D["nos"]), "HAJA": unix(os.path.join(D["haja"], "CLAUDE.md")), "INV": unix(D["inv"]), "SEL": unix(POS), "PORTA": unix(os.path.join(D["porta"], "porta_memoria.py")), "FILA": unix(os.path.join(POS, "fila_memoria_v411.py"))}
    nstub = []
    for tok in re.findall(r'"([^"]+)"', m.group(1).replace("\\\n", " ")):
        for k_, v_ in mapa.items():
            tok = tok.replace("$" + k_, v_)
        wp = tok if not tok.startswith("/") else (tok[1].upper() + ":" + tok[2:])
        if "$" in wp:
            continue
        if not os.path.exists(wp):
            os.makedirs(os.path.dirname(wp), exist_ok=True); open(wp, "w", encoding="utf-8", newline="\n").write("# stub do harness da fila\n"); nstub.append(os.path.basename(wp))
    open(os.path.join(D["porta"], "porta_memoria.py"), "w", encoding="utf-8", newline="\n").write("print('porta_memoria STUB do harness (o espelho real nao e tocado)')\n")
    # as saidas das etapas 5 e 6 (a arvore e o indice), EMULADAS: o passo 9 so' exige o sha16 nelas
    open(os.path.join(D["nos"], "A_PROVA_DA_QG_TGL_arvore.md"), "w", encoding="utf-8").write("arvore sintetica %s\n" % s16)
    open(os.path.join(D["atlas"], "TGL_INDICE_VIVO.md"), "w", encoding="utf-8").write("indice sintetico %s\n" % s16)
    for p, h in ((os.path.join(D["nos"], "MEMORIA_DA_LINHAGEM.md"), "# linhagem (sintetica)\n"), (os.path.join(D["nos"], "DESENHO_DO_FECHAMENTO_QG.md"), "# desenho (sintetico)\n"), (os.path.join(D["atlas"], "TGL_ATLAS.md"), "# atlas (sintetico)\n"),
                 (os.path.join(D["atlas"], "TGL_CORE_MEMORY.md"), "# core (sintetico)\n"), (os.path.join(D["haja"], "CLAUDE.md"), "# haja (sintetico)\n")):
        open(p, "w", encoding="utf-8", newline="\n").write(h)
    return {"dirs": D, "pos": POS, "s16": s16, "chain": os.path.join(POS, "chain_pos_rito_v411.sh"), "stubs": nstub}


def roda_chain(sb, de, ate, extra_env=None):
    sh = shutil.which("sh")
    if not sh:
        recusa("nao achei o sh (Git Bash) no PATH: o ensaio do chain precisa dele")
    e = dict(os.environ); e["CHAIN_DE"] = de; e["CHAIN_ATE"] = ate; e["PYTHONIOENCODING"] = "utf-8"
    for k in ("V411_MEMORIA_DIR", "MEMORIA_DIR", "B3_AUTORIZADO", "V411_AVISO_REIVINDICACAO"):
        e.pop(k, None)
    e.update(extra_env or {})
    p = subprocess.run([sh, unix(sb["chain"])], capture_output=True, env=e, cwd=sb["pos"], timeout=600)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def ensaio_chain():
    print("  -- (d) o PROPRIO chain_pos_rito_v411.sh nos passos 7 a 9 (pacote sintetico; so' as linhas de caminho trocadas)")
    E = FILA_EV; NEG = []; raiz = os.path.join(OUT, "chain_sandbox")

    def neg(nome, ok, det=""):
        NEG.append({"controle": nome, "ok": bool(ok), "det": str(det)[:400]})
        print("  controle negativo do chain: %-100s %s" % (nome[:100], "PAROU como esperado" if ok else "FALHOU"))
        if not ok:
            falha("[fila] chain: %s: %s" % (nome, str(det)[:240]))
    # ---- positivo: 7 a 9
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; m0 = fsha(idx_de(d)); p0 = fsha(os.path.join(d, "fila", "PINO_MEMORY.json"))
    E["chain_sandbox"] = {"stubs_criados_a_partir_do_passo_0": sb["stubs"], "s16_sintetico": sb["s16"]}
    rc, so, se = roda_chain(sb, "7", "9")
    open(os.path.join(OUT, "chain_sandbox_7a9_out.txt"), "w", encoding="utf-8").write(so + "\n--- stderr ---\n" + se)
    mdn = open(idx_de(d), "rb").read(); pn = rdj(os.path.join(d, "fila", "PINO_MEMORY.json"))
    i_pc = so.find('"op": "pausa-criar"'); i_sup = so.find("SUPERFICIES v411:"); i_pin = so.find('"op": "pinar"'); i_rem = so.find('"op": "pausa-remover"'); i_ver = so.find('"op": "verificar"')
    chk("CHAIN 7 a 9 (sintetico): rc 0 e '== FIM'", rc == 0 and "== FIM" in so, (rc, so[-400:], se[-200:]))
    chk("CHAIN: a saida tem a ordem pausa-criar < superficies gravou < pinar < pausa-remover < verificar", 0 <= i_pc < i_sup < i_pin < i_rem < i_ver, [i_pc, i_sup, i_pin, i_rem, i_ver])
    chk("CHAIN: a pausa NAO existe no fim; o pino == sha256 do MEMORY.md; o indice mudou (+1 linha) e cabe no limite", not os.path.exists(pausa_de(d)) and pn.get("sha256") == sha(mdn) and sha(mdn) != m0 and fsha(os.path.join(d, "fila", "PINO_MEMORY.json")) != p0 and mdn.count(b"\n") <= 195 and len(mdn) < 24000, {"linhas": mdn.count(b"\n"), "bytes": len(mdn)})
    rcv, jv, sov, sev = memoria(d, "verificar")
    chk("CHAIN: memoria.py verificar (rodado a parte) rc 0 depois do chain", rcv == 0 and jv and jv.get("ok") is True, sov[:300])
    E["cenarios"]["chain_7_a_9"] = {"rc": rc, "linhas_da_saida": [l[:200] for l in so.splitlines() if l.startswith("==") or l.startswith('{"') or "PARADA" in l][:30]}
    # ---- negativos (cada um num pacote novo)
    # C-a: memoria.py diferente do pino => para no passo 0, sem criar a pausa
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; m0 = fsha(idx_de(d)); mp = os.path.join(d, "fila", "memoria.py"); escreve_atomico(mp, open(mp, "rb").read() + b"\n# alterado\n")
    rc, so, se = roda_chain(sb, "7", "9")
    neg("memoria.py com sha16 diferente do pino => o chain PARA no passo 0 (rc 1, 'FILA DA MEMORIA'), sem pausa e sem tocar o indice", rc == 1 and "FILA DA MEMORIA" in so and not os.path.exists(pausa_de(d)) and fsha(idx_de(d)) == m0, so[-400:])
    # C-b: pausa alheia => para; a pausa fica intacta
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; alheia = json.dumps({"quem": "outra sessao", "ate": (datetime.datetime.now().astimezone() + datetime.timedelta(hours=1)).isoformat(timespec="seconds"), "motivo": "x"}).encode(); escreve_atomico(pausa_de(d), alheia); m0 = fsha(idx_de(d))
    rc, so, se = roda_chain(sb, "7", "9")
    neg("pausa de OUTRO dono ja existe => o chain PARA no passo 0 (rc 1), a pausa fica intacta e o indice nao muda", rc == 1 and "PAUSA" in so and open(pausa_de(d), "rb").read() == alheia and fsha(idx_de(d)) == m0, so[-400:])
    # C-c: pausa NOSSA (retomada a partir do passo 7) => passa
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; fila("pausa-criar", d)
    rc, so, se = roda_chain(sb, "7", "9")
    chk("CHAIN em RETOMADA (CHAIN_DE=7) com a pausa NOSSA de uma execucao anterior: aceita, renova e termina (rc 0, pausa removida no fim)", rc == 0 and "== FIM" in so and not os.path.exists(pausa_de(d)) and "retomada" in so, (rc, so[-300:]))
    # C-d: a pausa NOSSA ja existe mas a execucao COMECA DO ZERO (CHAIN_DE=0: nao e' retomada) => a guarda recusa no passo 0, a pausa fica intacta
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; fila("pausa-criar", d); pz0 = open(pausa_de(d), "rb").read(); m0 = fsha(idx_de(d))
    rc, so, se = roda_chain(sb, "0", "9")
    neg("pausa NOSSA ja existe e a execucao COMECA DO ZERO (CHAIN_DE=0, nao e' retomada) => o chain PARA no passo 0 (rc 1, 'FILA DA MEMORIA'), a pausa fica intacta e o indice nao muda", rc == 1 and "FILA DA MEMORIA" in so and open(pausa_de(d), "rb").read() == pz0 and fsha(idx_de(d)) == m0, so[-400:])
    # C-e: pinar falha => o chain PARA, a pausa PERMANECE, o indice (escrito) nao e' pinado
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; p0 = fsha(os.path.join(d, "fila", "PINO_MEMORY.json")); m0 = fsha(idx_de(d))
    # a falha do pinar: a cabeca do livro perde o sentido DEPOIS dos guardas; para isso o passo 0 tem de passar: corrompemos apos a guarda, usando um memoria.py que falha so' no pinar nao e' possivel (o sha16 e' pinado) -> corrompemos o CABECA.json e rodamos de 7 (a guarda roda e so' le o verificar, que informa e nao bloqueia)
    escreve_atomico(os.path.join(d, "fila", "CABECA.json"), b"{ isto nao e' json")
    rc, so, se = roda_chain(sb, "7", "9")
    neg("pinar FALHA => o chain PARA (rc 1) com 'PERMANECE', a PAUSA_VIGIA.json PERMANECE e o pino NAO muda (o indice escrito fica sem pino: a gerencia decide)", rc == 1 and "PERMANECE" in so and os.path.exists(pausa_de(d)) and fsha(os.path.join(d, "fila", "PINO_MEMORY.json")) == p0 and fsha(idx_de(d)) != m0 and "pausa-remover" not in so, so[-500:])
    # C-f: o MEMORY.md acima do limite => a superficie recusa (rc 3), o chain PARA no passo 7, a pausa PERMANECE e o indice nao muda
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; enche_indice(d, linhas_alvo=195); m0 = fsha(idx_de(d))
    rc, so, se = roda_chain(sb, "7", "9")
    neg("MEMORY.md no limite (195 linhas; +1 do handoff = 196) => a superficie RECUSA rc 3 e o chain PARA no passo 7 (rc 1), a pausa PERMANECE e o indice NAO muda", rc == 1 and "rc=3" in so and "CONTAGENS" in so and "PERMANECE" in so and os.path.exists(pausa_de(d)) and fsha(idx_de(d)) == m0, so[-500:])
    E["controles_negativos_do_chain"] = NEG
    shutil.rmtree(raiz, ignore_errors=True)


def finalizar(ANTES, saida_nome):
    DEPOIS = prova_real()
    iguais = {k: (ANTES[k] == DEPOIS[k]) for k in ANTES}
    # fila.jsonl e' o livro SO'-ACRESCIMO que as outras sessoes (claude-site, codex, kimi...) alimentam com depositos legitimos a qualquer hora: se ele mudou so' por ACRESCIMO (o conteudo de antes e' prefixo do de depois),
    # nao foi o harness (que so' escreve em copias) e nao e' falha; MEMORY.md, PINO_MEMORY.json e a ausencia de PAUSA_VIGIA.json tem de ficar IGUAIS
    fj = os.path.join(MEM_REAL, "fila", "fila.jsonl"); acresc = None
    if not iguais.get("fila/fila.jsonl", True) and os.path.exists(fj) and FILA_JSONL_ANTES is not None:
        acresc = open(fj, "rb").read().startswith(FILA_JSONL_ANTES); iguais["fila/fila.jsonl"] = bool(acresc)
    FILA_EV["fila_jsonl_cresceu_so_por_acrescimo"] = acresc
    FILA_EV["prova_do_diretorio_real"] = {"antes": ANTES, "depois": DEPOIS, "inalterado": iguais, "diretorio": MEM_REAL}
    R["etapas"]["prova_do_diretorio_real_de_memoria"] = {"inalterado": iguais, "todos_iguais": all(iguais.values())}
    print("  prova do diretorio REAL de memoria (MEMORY.md, PINO_MEMORY.json, fila.jsonl, ausencia de PAUSA_VIGIA.json) antes/depois: %s%s" % ("INALTERADO" if all(iguais.values()) else iguais, " (fila.jsonl so' cresceu por acrescimo: deposito legitimo de outra sessao, nao do harness)" if acresc else ""))
    if not all(iguais.values()):
        falha("o diretorio REAL de memoria mudou durante o harness (%s): o harness so' escreve em copias (MEMORIA_DIR/V411_MEMORIA_DIR); confirmar se foi outro processo (um deposito na fila muda fila.jsonl) e rerodar" % [k for k, v in iguais.items() if not v])
    if not MANTER:
        for dd in (FM, FM + "_sem_pausa", os.path.join(OUT, "memoria_neg"), os.path.join(OUT, "memoria_sup"), os.path.join(OUT, "memoria_sup_copias"), os.path.join(OUT, "superficies_stub"), os.path.join(OUT, "chain_sandbox")):
            shutil.rmtree(dd, ignore_errors=True)
    FILA_EV["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); FILA_EV["tudo_passou"] = (not [c for c in FILA_EV["checks"] if not c["ok"]]) and (not [p for p in R["problemas"] if p.startswith("[fila]") or "REAL de memoria" in p])
    if not SEM_FILA:
        os.makedirs(POS_SAIDA, exist_ok=True); open(os.path.join(POS_SAIDA, "FILA_MEMORIA_ENSAIO_v411.json"), "w", encoding="utf-8").write(json.dumps(FILA_EV, ensure_ascii=False, indent=1, default=str))
        R["etapas"]["fila_da_memoria"] = {"checks": len(FILA_EV["checks"]), "falharam": [c["check"][:120] for c in FILA_EV["checks"] if not c["ok"]], "evidencia": "FILA_MEMORIA_ENSAIO_v411.json", "tudo_passou": FILA_EV["tudo_passou"]}
    R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); R["tudo_passou"] = not R["problemas"]
    return saida_nome

def preconds():
    """as precondicoes do ensaio/da rodada: as entradas existem, o artefato e' um so' (ESPERADOS == manifesto == arquivo == dry_v411/um.py == o do PRONTO), o ensaio a seco e' DESTE artefato e passou, o dry esta completo; fora do ensaio, a regeneracao (refazer_out_v411.txt) e' EXIGIDA."""
    faltam = [n_ for n_, p_ in (("ESPERADOS_v411.json", P_ESP), ("o manifesto do artefato (%s)" % os.path.basename(P_MAN), P_MAN), ("PINOS_BN_v411.json", P_PINOS), ("ensaio_a_seco_v411.json", P_ENS), ("FORMAL_MAP_v411.json", P_FORMAL)) if not os.path.isfile(p_)]
    for n_ in ("guarda_p18_v411.py", "guarda_frases_v411.py", "base_um_v410.py", "runtime_h0dn_v411.py", "VERBATIM_CONGELADO_v411.json", "delta_v411.py", "quadro_v397.py", "runtime_quadro_v397.py", "conferir_rito_v411.py", "acom_conferencias_v411.py", "conferir_conversa_v411.py", "guarda_conversa_v411.py", "GUARDA_CONVERSA_BASE_v410.json"):   # (R1, D181: o conferidor importa a guarda da conversa; a base v410 da regra (b) e' dado)
        if not os.path.isfile(os.path.join(PKG, n_)):
            faltam.append(n_)
    for n_ in ("consts_mapa_x_v411.py", "leitura_v411.py", "textos_v411.py", "fechar_v411.py", "registrar_mapa_v411.py", "b3_recibo_v411.py"):
        if not os.path.isfile(os.path.join(HERE, n_)):
            faltam.append("pos_rito\\" + n_)
    if faltam:
        recusa("faltam entradas do ensaio (o ensaio da outra frente terminou?): %s" % faltam)
    ESP = rdj(P_ESP); CM = rdj(P_MAN); ens = rdj(P_ENS)
    if not os.path.isfile(CAND_ARQ):
        recusa("falta o artefato (%s: o um.py candidato, ou o artefato de ENSAIO do topo proposto)" % CAND_ARQ)
    cand16 = fsha(CAND_ARQ)[:16]
    if ENSAIO and PRONTO.get("artefato_sha16") and str(PRONTO["artefato_sha16"])[:16] != cand16:
        recusa("PRONTO_PARA_O_POS_RITO.json diz artefato_sha16 %s e o arquivo do artefato e' %s" % (PRONTO["artefato_sha16"], cand16))
    for n_ in ("core_ensaio.json", "selo_ensaio.json", "um.py", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v411_pt.txt", "dry_v411_en.txt", "dry_v411_pt.toc", "dry_v411_en.toc", "tgl_kernel"):
        if not os.path.exists(os.path.join(DRY, n_)):
            recusa("dry_v411 incompleto (falta %s)" % n_)
    if not (ESP["candidato_sha16"] == CM["sha16"] == cand16 == fsha(os.path.join(DRY, "um.py"))[:16]):
        recusa("o artefato nao e' um so' (ESPERADOS, manifesto, arquivo e dry_v411/um.py divergem)")
    if ens.get("veredito") != "TUDO PASSOU" or ens.get("sha16") != cand16:
        recusa("o ensaio a seco nao e' deste artefato ou nao passou (veredito %r, sha16 %r)" % (ens.get("veredito"), ens.get("sha16")))
    _rf = P_REFAZER; _rf_txt = open(_rf, encoding="utf-8", errors="replace").read() if (not ENSAIO and os.path.exists(_rf)) else ""
    if not ENSAIO:   # fora do ensaio a regeneracao do candidato e' EXIGIDA (refazer_out_v411.txt com '== FIM', mais novo que o ESPERADOS); --nao-exigir-refazer so' para depurar
        if not NAO_REFAZER:
            if not os.path.exists(_rf):
                recusa("falta refazer_out_v411.txt no pacote: a regeneracao do candidato nao foi comprovada (--nao-exigir-refazer so' para depurar)")
            if "== FIM" not in _rf_txt:
                recusa("refazer_out_v411.txt nao mostra '== FIM': a regeneracao nao terminou")
            if os.path.getmtime(_rf) < os.path.getmtime(P_ESP):
                recusa("refazer_out_v411.txt e' mais ANTIGO que ESPERADOS_v411.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
    elif NAO_REFAZER:
        recusa("--nao-exigir-refazer nao vale no ensaio (a regeneracao do ensaio e' o PRONTO_PARA_O_POS_RITO.json)")
    R["etapas"]["precondicoes"] = {"candidato_sha16": cand16, "ensaio_topo_proposto": ENSAIO, "origem_das_entradas": dict(ORIGEM), "refazer_exigido": (not ENSAIO and not NAO_REFAZER), "refazer_out_presente": os.path.exists(_rf), "refazer_fim_visto": "== FIM" in _rf_txt, "esperados_sha16": fsha(P_ESP)[:16], "manifesto_sha16": fsha(P_MAN)[:16], "pinos_bn_sha16": fsha(P_PINOS)[:16],
                                   "pronto_sha16": fsha(PRONTO_ARQ)[:16] if ENSAIO else None, "pino_do_memoria_py_emulado": PINO_EMULADO}
    return ESP, CM, cand16, _rf, _rf_txt
os.makedirs(OUT, exist_ok=True)
ANTES_REAL = prova_real()
FILA_JSONL_ANTES = open(os.path.join(MEM_REAL, "fila", "fila.jsonl"), "rb").read() if os.path.exists(os.path.join(MEM_REAL, "fila", "fila.jsonl")) else None
if not SO_FILA:
    ESP, CM, cand16, _rf, _rf_txt = preconds()      # (rc 4 = precondicao nao satisfeita: nada foi rodado, nem a fila)
if not SEM_FILA:
    ensaio_da_fila()
if SO_FILA:
    finalizar(ANTES_REAL, None)
    R["veredito"] = ("TUDO PASSOU (so' a fila da memoria): o passo da fila funciona em COPIA na ordem do chain (pausa antes da escrita, pinar rc 0, pausa so' depois do pino, verificar rc 0, pino == sha256 do MEMORY.md), as superficies recusam sem pausa (rc 6) e acima do limite (rc 3), o chain para sem remover a pausa quando falha antes do pino, e o diretorio real de memoria ficou inalterado" if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
    if PINO_EMULADO:
        R["veredito"] += " [PINO EMULADO: PINO_MEMORIA_PY_v411.json nao existia na raiz do pacote; a fila e o chain rodaram com um pino calculado na hora do memoria.py real (so' leitura)]"
    os.makedirs(POS_SAIDA, exist_ok=True); saida = os.path.join(POS_SAIDA, "HARNESS_FECHAR_SANDBOX_v411_SO_FILA.json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    print("VEREDITO (so' a fila):", R["veredito"]); print("saida:", saida); sys.exit(0 if R["tudo_passou"] else 1)

# =====================================================================================================================================================
#  (2) O FECHAR e o REGISTRAR_MAPA em SANDBOX
# =====================================================================================================================================================
os.makedirs(OUT, exist_ok=True); shutil.rmtree(SB, ignore_errors=True)
PKS = os.path.join(SB, "work", "cadeia_de_selo", "v411"); POS = os.path.join(PKS, "pos_rito"); NOSS = os.path.join(SB, "nos"); UMS = os.path.join(SB, "memory"); TOOLS = os.path.join(SB, "work", "cadeia_de_selo")
for d in (POS, os.path.join(PKS, "base_v410"), os.path.join(PKS, "kernel"), os.path.join(POS, "conferidor"), os.path.join(PKS, "bancada_B3"), os.path.join(PKS, "bancada_B3_servico"), NOSS):
    os.makedirs(d, exist_ok=True)
mk_memoria_copia(UMS)       # v411: a memoria do sandbox e' uma COPIA (o fechar escreve o handoff nela e o manifesto le o estado da fila dela)
# ---- o pacote do sandbox: o ESTATICO vem da pasta da cadeia; o DINAMICO (ESPERADOS, o manifesto do artefato como CANDIDATO_v411.json, PINOS_BN, FORMAL_MAP, o pino do memoria.py) vem das entradas do ensaio (fora do ensaio, da pasta da cadeia)
for n in ("guarda_p18_v411.py", "guarda_frases_v411.py", "base_um_v410.py", "runtime_h0dn_v411.py", "VERBATIM_CONGELADO_v411.json", "delta_v411.py", "quadro_v397.py", "runtime_quadro_v397.py", "conferir_rito_v411.py", "acom_conferencias_v411.py", "conferir_conversa_v411.py", "guarda_conversa_v411.py", "GUARDA_CONVERSA_BASE_v410.json"):   # (R1, D181: o conferidor importa a guarda da conversa; a base v410 da regra (b) e' dado)
    if not os.path.exists(os.path.join(PKG, n)):
        recusa("o pacote da v411 nao tem %s (o harness o copia para o sandbox)" % n)
    shutil.copyfile(os.path.join(PKG, n), os.path.join(PKS, n))
for src_, nome_ in ((P_ESP, "ESPERADOS_v411.json"), (P_MAN, "CANDIDATO_v411.json"), (P_PINOS, "PINOS_BN_v411.json"), (P_FORMAL, "FORMAL_MAP_v411.json"), (PINO_ARQ, "PINO_MEMORIA_PY_v411.json")):
    shutil.copyfile(src_, os.path.join(PKS, nome_))
for kn_ in ("KERNEL_RECIBO_v411.json", "FLAGS_v411.json", "KH_N1_v411.json"):
    if os.path.exists(os.path.join(PKG, "kernel", kn_)):
        shutil.copyfile(os.path.join(PKG, "kernel", kn_), os.path.join(PKS, "kernel", kn_))
_liga(os.path.join(PKG, "base_v410", "um.py"), os.path.join(PKS, "base_v410", "um.py")); shutil.copyfile(os.path.join(PKG, "base_v410", "um_absoluto.json"), os.path.join(PKS, "base_v410", "um_absoluto.json"))
shutil.copyfile(os.path.join(PKG, "base_v410", "um_absoluto_selo.json"), os.path.join(PKS, "base_v410", "um_absoluto_selo.json"))
shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))
os.makedirs(os.path.join(PKS, "insumos", "fase9"), exist_ok=True)   # o resultado pinado do Teste da Unica Palavra mora na v397 (ESPERADOS[veracidade][resultado][duravel]); o sandbox ganha a sua COPIA, que os controles negativos adulteram
shutil.copyfile(ESP["veracidade"]["resultado"]["duravel"], os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens"), exist_ok=True)   # a fala do 4,44 (v397, onde foi inscrita), de onde textos_v411 confere a frase verbatim do quadro
_h444 = ESP["quadro"]["frase_sha16"]; _f444 = [f_ for f_ in os.listdir(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens")) if f_.startswith(_h444 + "_")]; assert len(_f444) == 1
shutil.copyfile(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens", _f444[0]), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens", _f444[0]))
os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"), os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"))
# v411 (fork B): a importacao do delta REAL e' INSTRUMENTADA (open/exists/isfile/isdir/getsize) para MEDIR, na hora, todo arquivo da casa (abaixo de Central de Patentes) que o delta_v411 e os deltas herdados (v410, v406, ...) abrem ou conferem ao importar:
# a lista alimenta o ESPELHO DA CASA (abaixo), que leva cada um ao sandbox na mesma posicao relativa; nada digitado. Os ganchos sao removidos logo depois da importacao (finally).
_ACESSOS = set()
_open0 = builtins.open


def _open_h(p, *a, **k):
    try:
        _ACESSOS.add(os.path.abspath(os.fspath(p)))
    except Exception:   # noqa: BLE001
        pass
    return _open0(p, *a, **k)


_osp0 = {n_: getattr(os.path, n_) for n_ in ("exists", "isfile", "isdir", "getsize")}


def _mk_h(f_):
    def g_(p, *a, **k):
        try:
            _ACESSOS.add(os.path.abspath(os.fspath(p)))
        except Exception:   # noqa: BLE001
            pass
        return f_(p, *a, **k)
    return g_


builtins.open = _open_h
for _n_h, _f_h in _osp0.items():
    setattr(os.path, _n_h, _mk_h(_f_h))
try:
    _dlx = importlib.util.spec_from_file_location("delta_v411_h", os.path.join(PKG, "delta_v411.py")); _dm = importlib.util.module_from_spec(_dlx); _dlx.loader.exec_module(_dm)
finally:
    builtins.open = _open0
    for _n_h, _f_h in _osp0.items():
        setattr(os.path, _n_h, _f_h)
# v411: o MANIFEST da integracao R3 (que o delta_v406 herdado pina por assert, relativo a sua propria pasta) vai na mesma posicao relativa dentro de work/fechamento_02nov, e e' o MANIFEST do BUNDLE_v406.json da COPIA da pasta irma v406 que recebe o origem_integracao do sandbox (abaixo);
# o resultado da Fase 9 V2 vai em work/fase9_v2_c1_23out/saidas; a v411 NAO tem BUNDLE nem pedra (nenhum modulo novo): so' as pastas irmas das versoes anteriores
_man_sb = os.path.join(SB, "work", "fechamento_02nov", os.path.relpath(_dm.MANIFEST_INTEGRACAO_ARQ, _dm.ESTUDO_FECHO))
os.makedirs(os.path.dirname(_man_sb), exist_ok=True); shutil.copyfile(_dm.MANIFEST_INTEGRACAO_ARQ, _man_sb)
os.makedirs(os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas"), exist_ok=True); shutil.copyfile(_dm.FASE9_V2_ARQ, os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas", os.path.basename(_dm.FASE9_V2_ARQ)))
for _nm_v in [n_ for n_ in dir(_dm) if n_.startswith("VERBATIM_ORIGEM") and isinstance(getattr(_dm, n_), (list, tuple))]:   # as falas das versoes anteriores que moram em cunhagens_13out vao junto, para os deltas herdados; as de outras pastas e as desta versao (as do delta) vao pelo espelho da casa
    for _o in getattr(_dm, _nm_v):
        if os.path.isfile(_o) and os.path.basename(os.path.dirname(_o)) == "cunhagens_13out":
            shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
# o delta_v410 herdado PINA POR ASSERT o manifesto da parametrizacao do teste (d) (D_TESTE_MANIFESTO, sha16 da ordem): o sandbox o leva (copia de bytes) na mesma posicao relativa
_man_d_sb = os.path.join(SB, "work", os.path.relpath(_dm.D_TESTE_MANIFESTO, _dm.WK)); os.makedirs(os.path.dirname(_man_d_sb), exist_ok=True); shutil.copyfile(_dm.D_TESTE_MANIFESTO, _man_d_sb)
# v411 (desvio do molde, dito; integracao de 12/11: a v409 entra, o acom_conferencias_v410 a carrega por caminho): as pastas irmas que o delta_v411 e o acom_conferencias_v411 importam por caminho (v410 e, por ela, v400 e v399), o runtime da secao e as seis fontes do operador (v400), a pedra e as fontes do estudo (v399), o resultado do Teste da Unica Palavra (v397) e o esboco R3.5 da Bancada (C15): copias de bytes, so' o que eles leem
for _vv in ("v410", "v409", "v408", "v407", "v406", "v405", "v404", "v403", "v402", "v401", "v400", "v399"):   # (v411: a v407 entra -- acom_conferencias_v410 importa acom_conferencias_v407; 09/11: a v408 entra -- acom_conferencias_v410 reexporta, por caminho, acom_conferencias_v408.py, que faltava na copia)   # v411 (fork B): a v406 entra (o delta_v410 importa o delta_v406; a subida mecanica a tinha deixado de fora)
    os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", _vv))
    for _n in sorted(os.listdir(os.path.join(os.path.dirname(PKG), _vv))):      # os arquivos PEQUENOS do topo da pasta irma (os deltas leem pinos da propria pasta: pedra_sha16_da_ordem.txt, pedras_sha16_da_ordem.json, o runtime, as conferencias); os candidatos de dezenas de MB ficam de fora
        _pn = os.path.join(os.path.dirname(PKG), _vv, _n)
        if os.path.isfile(_pn) and os.path.getsize(_pn) < 1024 * 1024 and ".bak" not in _n and ".tmp" not in _n:
            shutil.copyfile(_pn, os.path.join(SB, "work", "cadeia_de_selo", _vv, _n))
    if os.path.isdir(os.path.join(os.path.dirname(PKG), _vv, "insumos", "acom")):
        shutil.copytree(os.path.join(os.path.dirname(PKG), _vv, "insumos", "acom"), os.path.join(SB, "work", "cadeia_de_selo", _vv, "insumos", "acom"))
for _vp in ("v410", "v407", "v406", "v405", "v404", "v403", "v402", "v401", "v399"):
    if os.path.isdir(os.path.join(os.path.dirname(PKG), _vp, "pedra")):
        shutil.copytree(os.path.join(os.path.dirname(PKG), _vp, "pedra"), os.path.join(SB, "work", "cadeia_de_selo", _vp, "pedra"))
# v411 (fork B; a subida mecanica apontava para o BUNDLE_v410.json, que NAO tem origem_integracao): o BUNDLE_v406.json da COPIA da pasta v406 no sandbox tem de apontar para o MANIFEST da integracao DENTRO do sandbox (o delta_v406 da copia confere por assert que origem_integracao == o MANIFEST relativo a sua propria pasta); so' esse campo e' reescrito
_b6p = os.path.join(SB, "work", "cadeia_de_selo", "v406", "BUNDLE_v406.json"); _b6 = rdj(_b6p); assert "origem_integracao" in _b6, "o BUNDLE_v406.json da copia nao tem origem_integracao"; _b6["origem_integracao"] = _man_sb.replace(os.sep, "/")
open(_b6p, "w", encoding="utf-8").write(json.dumps(_b6, ensure_ascii=False, indent=1))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))
shutil.copytree(os.path.join(os.path.dirname(os.path.dirname(PKG)), "grande_atrator_reclassificacao_01nov"), os.path.join(SB, "work", "grande_atrator_reclassificacao_01nov"))
os.makedirs(os.path.join(SB, "Chatgpt")); shutil.copyfile(_dm.GA_PARECER_ARQ, os.path.join(SB, "Chatgpt", os.path.basename(_dm.GA_PARECER_ARQ)))
os.makedirs(os.path.join(SB, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt")); shutil.copyfile(_dm.ACORDE_KIMI_ARQ, os.path.join(SB, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt", os.path.basename(_dm.ACORDE_KIMI_ARQ)))
os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
# ---- v411 (fork B): o ESPELHO DA CASA -- todo arquivo abaixo de Central de Patentes que a importacao do delta REAL abriu ou conferiu (medido acima, _ACESSOS) vai ao sandbox na MESMA posicao relativa (copia de bytes), se ainda nao estiver la': os deltas herdados (v410 a v399) derivam WK da propria pasta e abrem, ao importar,
# as candidatas de 02/11 (beta_calor_02nov, k_guarda_travessia_02nov, rota_RE_dualidade_02nov, fechamento_02nov), as de 03/11 e 04/11 (pedras_candidatas_03nov, pedras_candidatas_04nov), as falas de 30/10 (experimento_espelho_30out), a da Identidade (cadeia_de_selo405), a decisao das fontes nao publicadas (custodia_G1), o manifesto do teste (d),
# o resultado da Fase 9 V2, o acorde do Kimi... Arquivos fora da casa (o Nos real, a Bancada_Um) sao lidos no lugar, so' leitura; os do proprio pacote (PKG) que faltarem na copia (p. ex. DESENHO_v411.md) vao para PKS. Nenhum arquivo ja' presente no sandbox e' sobrescrito por este espelho.
_CEN_REAL = os.path.dirname(os.path.dirname(PKG))
# (AVISO da gerencia, 09/11) O VETO A PASTA DA ENTREGA DO KIMI: a pasta e' lida do delta REAL ja' importado (_dm.H0DN_PASTA_VEDADA = work\\h0dn_bg1_v410_09nov\\kimi); nenhum acesso MEDIDO na importacao do delta pode cair sob ela (se cair, FALHA VISIVEL: a v411 pre-registra e NAO abre),
# o espelho da casa a exclui EXPLICITAMENTE (abaixo) e a copia da memoria tambem (mk_memoria_copia): a exclusao e' por medida, nao por promessa
assert _VEDADO == os.path.normcase(os.path.abspath(_dm.H0DN_PASTA_VEDADA)), ("a pasta vedada lida do TEXTO do delta difere da do delta IMPORTADO", _VEDADO, _dm.H0DN_PASTA_VEDADA)
_ACESSOS_VEDADOS = sorted(p_ for p_ in _ACESSOS if _sob_vedado(p_))
assert not _ACESSOS_VEDADOS, ("VEDADO: a importacao do delta tocou a pasta da entrega do Kimi (a v411 pre-registra e NAO abre)", _ACESSOS_VEDADOS)
assert not _sob_vedado(MEM_REAL) and not _sob_vedado(PKG) and not _sob_vedado(SB), "VEDADO: a memoria, o pacote ou o sandbox estariam sob a pasta vedada"
_ESP_N = 0; _ESP_B = 0; _ESP_LISTA = []; _ESP_D59_N = 0   # (v411, D59: o arquivo cujo NOME traz o que fica fora dos textos e' copiado, mas o nome nao entra no resumo; so' a contagem)
# (r2, 05/11 madrugada: as falas EXCLUIDAS pelos deltas (VERBATIM_EXCLUIDAS_*, chave = sha16 dos bytes; hoje a da v405) sao abertas pelo filtro do delta herdado ao importar e entravam no espelho E no resumo pelo NOME do arquivo;
#  a purga_v411 as achou no JSON do harness. Elas NAO vao ao sandbox (o filtro do delta da copia aceita a ausencia: _h devolve None e o glob nao a acha) e o nome nao entra no resumo; so' a contagem.)
_EXCL16 = set()
for _mn_, _mm_ in list(sys.modules.items()):
    if _mn_.startswith("delta_v") or "delta_v4" in str(getattr(_mm_, "__file__", "") or ""):
        for _an_ in dir(_mm_):
            if _an_.startswith("VERBATIM_EXCLUIDAS") and isinstance(getattr(_mm_, _an_, None), dict):
                _EXCL16.update(getattr(_mm_, _an_).keys())
for _an_ in dir(_dm):
    if _an_.startswith("VERBATIM_EXCLUIDAS") and isinstance(getattr(_dm, _an_, None), dict):
        _EXCL16.update(getattr(_dm, _an_).keys())
_ESP_EXCL_N = 0
for _p_a in sorted(_ACESSOS):
    if _sob_vedado(_p_a):
        raise AssertionError(("VEDADO: o espelho da casa nao copia nada da pasta da entrega do Kimi", _p_a))   # (AVISO 09/11; nunca alcancado se o assert acima passou: fica como a segunda trava)
    _PAT_REAL = os.path.join(os.path.dirname(_CEN_REAL), "patents")
    if _p_a.startswith(_PAT_REAL + os.sep) and os.path.isfile(_p_a):   # (R5, D100) o runner do ACOM Mirror (o pino do delta), sob Central\patents: o CENTRAL do delta da copia e' o sandbox, entao vai a SB\patents na mesma posicao relativa
        _dst_p = os.path.join(SB, "patents", os.path.relpath(_p_a, _PAT_REAL))
        if not os.path.exists(_dst_p):
            os.makedirs(os.path.dirname(_dst_p), exist_ok=True); shutil.copyfile(_p_a, _dst_p); _ESP_N += 1; _ESP_B += os.path.getsize(_dst_p)
            _ESP_LISTA.append(os.path.relpath(_p_a, os.path.dirname(_CEN_REAL)))
        continue
    if not (_p_a.startswith(_CEN_REAL + os.sep) and os.path.isfile(_p_a)):
        continue
    if _EXCL16 and sha(open(_p_a, "rb").read())[:16] in _EXCL16:
        _ESP_EXCL_N += 1
        continue
    # (r2, 04/11 noite: _CEN_REAL e' a pasta work REAL, e no sandbox ela e' SB\work (o pacote e' SB\work\cadeia_de_selo\v411, o delta da copia deriva WK = SB\work); o espelho gravava em SB\<rel> e o delta da copia nao achava, p. ex., work\custodia_G1\decisoes\FONTES_NAO_PUBLICADAS_v410.json)
    _dst_a = os.path.join(PKS, os.path.relpath(_p_a, PKG)) if _p_a.startswith(PKG + os.sep) else os.path.join(SB, "work", os.path.relpath(_p_a, _CEN_REAL))
    if os.path.exists(_dst_a):
        continue
    os.makedirs(os.path.dirname(_dst_a), exist_ok=True); shutil.copyfile(_p_a, _dst_a); _ESP_N += 1; _ESP_B += os.path.getsize(_dst_a)
    if re.search(r"(?i)kimi|mil[eê]nio|navier", _p_a):
        _ESP_D59_N += 1
    else:
        _ESP_LISTA.append(os.path.relpath(_p_a, _CEN_REAL))
R["etapas"]["espelho_da_casa"] = {"n_arquivos_copiados": _ESP_N, "bytes": _ESP_B, "n_acessos_medidos": len(_ACESSOS), "pasta_vedada_kimi": {"pasta": _dm.H0DN_PASTA_VEDADA, "acessos_medidos_sob_ela": _ACESSOS_VEDADOS, "excluida_explicitamente_do_espelho_e_da_copia_da_memoria": True}, "n_falas_excluidas_nao_copiadas_nem_nomeadas": _ESP_EXCL_N, "n_arquivos_copiados_sem_nome_no_resumo_D59": _ESP_D59_N, "arquivos": _ESP_LISTA[:400], "nota": "medido instrumentando open/exists/isfile/isdir/getsize na importacao do delta_v411 real; copia de bytes na mesma posicao relativa; nada digitado; nada sobrescrito"}
print("  espelho da casa (o que o delta e os deltas herdados abrem ao importar): %d arquivos copiados (%d B) de %d acessos medidos" % (_ESP_N, _ESP_B, len(_ACESSOS)))
open(os.path.join(PKS, "rito_horarios_v411.txt"), "w", encoding="utf-8").write("00:00:00\n00:45:00\n")          # EMULADO (sandbox)
# ---- as copias dos scripts, trocando SO' o caminho do Nos (o fechar recebe a memoria por V411_MEMORIA_DIR)
NOS_RX = 'NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")'
TROCAS = {"leitura_v411.py": [(NOS_RX, 'NOS = %r' % NOSS)], "textos_v411.py": [(NOS_RX, 'NOS = %r' % NOSS)], "fechar_v411.py": [], "registrar_mapa_v411.py": [], "consts_mapa_x_v411.py": []}
DIF = {}
for n, trs in TROCAS.items():
    t = open(os.path.join(HERE, n), encoding="utf-8").read(); t0 = t
    for a, b in trs:
        if t.count(a) != 1:
            recusa("a linha de caminho nao e' unica em %s: %r (%d)" % (n, a[:60], t.count(a)))
        t = t.replace(a, b)
    open(os.path.join(POS, n), "w", encoding="utf-8", newline="\n").write(t)
    s0_ = set(t0.splitlines()); DIF[n] = [l for l in t.splitlines() if l not in s0_]
def _env_sb(**kw):
    """o ambiente dos scripts do SANDBOX (uma arvore 'real' emulada): SEM V411_ENSAIO_TOPO_PROPOSTO (so' o conferidor, acima, o leva)"""
    e_ = dict(os.environ, PYTHONIOENCODING="utf-8"); e_.pop("V411_ENSAIO_TOPO_PROPOSTO", None); e_.update(kw); return e_
# ---- o Nos emulado do sandbox (do falso Nos de ENSAIO ou de dry_v411, como no harness dos textos; o SIDECAR gerado pela funcao do PROPRIO artefato; o stdout do rito EMULADO e dito)
import ast as _ast
if os.path.isfile(os.path.join(FALSO_NOS, "um.py")) and os.path.isfile(_FN_CORE) and os.path.isfile(_FN_SELO) and os.path.isdir(os.path.join(FALSO_NOS, "tgl_kernel")):
    _FONTE_NOS = "falso Nos de ENSAIO (%s)" % FALSO_NOS
    for _n in sorted(os.listdir(FALSO_NOS)):
        _s = os.path.join(FALSO_NOS, _n)
        if os.path.isdir(_s):
            shutil.copytree(_s, os.path.join(NOSS, _n))
        elif _n == "um.py":
            _liga(_s, os.path.join(NOSS, _n))    # o um.py nunca e' escrito
        else:
            shutil.copyfile(_s, os.path.join(NOSS, _n))
    for _src, _dst in ((_FN_CORE, "um_absoluto.json"), (_FN_SELO, "um_absoluto_selo.json"), (_FN_PT, "um_absoluto_pt.txt"), (_FN_EN, "um_absoluto_en.txt")):
        if os.path.isfile(_src) and os.path.normcase(os.path.abspath(_src)) != os.path.normcase(os.path.abspath(os.path.join(FALSO_NOS, _dst))):
            shutil.copyfile(_src, os.path.join(NOSS, _dst))
else:
    _FONTE_NOS = "dry_v411 (o falso Nos nao existe: o Nos e' montado do dry, como na v410)"
    for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"), ("dry_v411_pt.txt", "um_absoluto_pt.txt"),
                     ("dry_v411_en.txt", "um_absoluto_en.txt"), ("dry_v411_pt.toc", "um_absoluto_pt.toc"), ("dry_v411_en.toc", "um_absoluto_en.toc"), ("dry_v411_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v411_en.pdf", "um_absoluto_en.pdf")):
        if os.path.exists(os.path.join(DRY, src)):
            (_liga if src == "um.py" else shutil.copyfile)(os.path.join(DRY, src), os.path.join(NOSS, dst))
    shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSS, "tgl_kernel"))
# o JSON do rito real traz ga_window_status no topo e a v411 o confere; o ensaio so guarda core e verdict: a emulacao o le da constante do proprio artefato, nunca de ESPERADOS
_cj = rdj(os.path.join(NOSS, "um_absoluto.json"))
if "ga_window_status" not in _cj:
    _gw = re.search(r"^GA_WINDOW_STATUS = \((.*?)\)\r?$", open(os.path.join(NOSS, "um.py"), "rb").read().decode("utf-8"), re.S | re.M); assert _gw, "a constante GA_WINDOW_STATUS nao esta no artefato"
    _cj["ga_window_status"] = _ast.literal_eval("(" + _gw.group(1) + ")")
    open(os.path.join(NOSS, "um_absoluto.json"), "w", encoding="utf-8").write(json.dumps(_cj, ensure_ascii=False, default=str))
s0 = rdj(os.path.join(PKS, "base_v410", "um_absoluto_selo.json"))
s = rdj(os.path.join(NOSS, "um_absoluto_selo.json")) if _FONTE_NOS.startswith("falso") else dict(s0, **rdj(os.path.join(DRY, "selo_ensaio.json")))
s["sha256"] = dict(s.get("sha256") or s0.get("sha256") or {}); s["sha256"]["um.py"] = fsha(os.path.join(NOSS, "um.py"))
open(os.path.join(NOSS, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, default=str))
_ens = rdj(P_ENS)   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
# o SIDECAR: a funcao do PROPRIO artefato (a copia de bytes do Nos do sandbox; __file__ = nos\um.py) sobre o core e o selo FINAIS do Nos do sandbox; a linha que ela imprime e' a linha REAL do sidecar
_spec_sc = importlib.util.spec_from_file_location("um_sidecar_emulacao_sb", os.path.join(NOSS, "um.py")); _umm = importlib.util.module_from_spec(_spec_sc)
_so = sys.stdout; sys.stdout = io.StringIO()
try:
    _spec_sc.loader.exec_module(_umm); _umm.OUT = NOSS
    sys.stdout = _buf_sc = io.StringIO()
    _umm.selo_acom_sidecar_v399()
    _linha_sidecar = _buf_sc.getvalue().strip()
finally:
    sys.stdout = _so; sys.stdout.reconfigure(encoding="utf-8")
del _umm, _spec_sc
N_ = ESP["escada"][1]
open(os.path.join(NOSS, "rodada_v411_stdout.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(["[v399] EMULADO PELO SANDBOX (as linhas do fluxo principal sao as REAIS do ensaio a seco)"] + list(_ens["mainflow"]["stdout"])
    + ["teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", _linha_sidecar, "RITO_RC=0", ""]))
bu = os.path.join(PKS, "base_v410", "um.py")
ap = {"ts": time.strftime("%Y%m%d_%H%M%S"), "backups": {"um.py": {"backup": bu, "bytes": os.path.getsize(bu), "sha16": fsha(bu)[:16]}}, "um_py_novo": {"bytes": os.path.getsize(os.path.join(NOSS, "um.py")), "sha16": ESP["candidato_sha16"]}}
open(os.path.join(PKS, "APLICADO_AO_CANONICO_%s.json" % ap["ts"]), "w", encoding="utf-8").write(json.dumps(ap, indent=1))
# ---- o conferidor REAL (copia) contra o Nos emulado: a conferencia que a leitura le. Roda no proprio pacote do sandbox (PKS = work\cadeia_de_selo\v411, com work\cunhagens_13out ao lado, insumos\acom), SEM -I (importa o um.py do Nos do sandbox).
# No ensaio a variavel V411_ENSAIO_TOPO_PROPOSTO FICA no ambiente DELE: a copia de import do um.py que ele faz vai para a pasta do ensaio (DL.RODADA_PAI), nao para C:\t\k411c, e a conferencia sai por DL.saida (sufixo proprio _HARNESS_FECHAR: nada do que a outra frente gravou e' tocado).
env = dict(os.environ); env["V411_NOS"] = NOSS; env["PYTHONIOENCODING"] = "utf-8"
if not ENSAIO:
    env.pop("V411_ENSAIO_TOPO_PROPOSTO", None)
cfd = PKS
_conf_out = DLX.saida("conferencia_rito_v411_HARNESS_FECHAR.json") if ENSAIO else os.path.join(cfd, "conferencia_rito_v411_HARNESS_FECHAR.json")
_conf_antes = open(_conf_out, "rb").read() if os.path.exists(_conf_out) else None
pc = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v411.py", "_HARNESS_FECHAR"], cwd=cfd, env=env, capture_output=True, text=True, encoding="utf-8")
open(os.path.join(OUT, "conferir_rito_sandbox_stdout.txt"), "w", encoding="utf-8").write(pc.stdout + "\n--- stderr ---\n" + pc.stderr)
if pc.returncode != 0 or not os.path.exists(_conf_out):
    falha("o conferidor nao deu TUDO BATE contra o Nos emulado do sandbox (rc %s): %s | stderr: %s" % (pc.returncode, pc.stdout[-300:], pc.stderr[-500:]))
else:
    shutil.copyfile(_conf_out, os.path.join(POS, "conferidor", "conferencia_rito_v411.json"))
    if _conf_antes is None:
        os.remove(_conf_out)
    else:
        open(_conf_out, "wb").write(_conf_antes)
# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v410): passo SIMPLES B19 (v410) -> B20 (v411)
PKG_ANT = os.path.join(os.path.dirname(PKG), "v410")
base_apl = rdj(glob.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v410_*.json"))[0])
pinos = rdj(P_PINOS); pre = rdj(pinos["recibo_pre_selo"]["path"]); n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1


def recibo_apl(com_salto=False, n=None, versao_alvo="v411"):
    r = json.loads(json.dumps(base_apl)); r["versao_alvo"] = versao_alvo; r["fase"] = "pos_selo"; r["modo"] = "aplicar"; r.pop("salto", None); r.pop("cadeia_de_selos", None)
    n = n_ger if n is None else n
    r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"])); r["manifesto_novo"]["deployment_id"] = "B%d-v411-20261104-R1" % n
    r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}; r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v411"}
    r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
    r["veredito"] = "REPINADA_B%d__%sAPLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % (n, "SALTO_v410_v411__" if com_salto else "")
    r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v411", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
    if com_salto:
        r["salto"] = {"declarado": True}
    r["_sintetico"] = "SINTETICO (sandbox do fechar): NAO e' um recibo do esboco"
    return r


def escreve(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))


RAPL = recibo_apl(); man_novo = RAPL["manifesto_novo"]["sha256"]
pth_apl = os.path.join(PKS, "bancada_B3", "RECIBO_SINCRONIZACAO_v411_SINTETICO.json"); escreve(pth_apl, RAPL)
agora = time.strftime("%Y-%m-%dT%H:%M:%S")
open(os.path.join(PKS, "bancada_B3_servico", "RECIBO_PARADA_v411.json"), "w", encoding="utf-8").write(json.dumps({"passo": "10-bis-a", "pid": 11111, "porta": 18777, "porta_fechada": True, "hora": agora, "_sintetico": "sandbox"}))
pth_rel = os.path.join(PKS, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v411.json")
open(pth_rel, "w", encoding="utf-8").write(json.dumps({"passo": "10-ter", "versao_servida": "v411", "manifesto_sha256": man_novo, "pid": 22222, "hora": agora, "_sintetico": "sandbox"}))


def roda(script, nome):
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(POS, script)], cwd=POS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env_sb(V411_MEMORIA_DIR=UMS))
    open(os.path.join(SB, nome + "_out.txt"), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    return p.returncode, p.stdout, p.stderr


# ---- 0. o b3_recibo_v411.py (o REAL, lendo o PINOS_BN real): passo SIMPLES B19 -> B20 com recibos SINTETICOS (positivo e negativos)
B3N = []


def b3(nome, modo, rec, esperado_rc):
    stdout_p = os.path.join(SB, "b3_%s_stdout.txt" % nome); rp_ = os.path.join(SB, "b3_%s_recibo.json" % nome); escreve(rp_, rec)
    open(stdout_p, "w", encoding="utf-8").write(json.dumps({"recibo": rp_, "recibo_sha256": fsha(rp_), "veredito": rec.get("veredito")}) + "\n")
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "b3_recibo_v411.py"), stdout_p, modo], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = (p.returncode == esperado_rc)
    B3N.append({"caso": nome, "rc": p.returncode, "esperado": esperado_rc, "ok": ok, "saida": (p.stdout or "")[-300:]})
    print("  b3_recibo_v411 [%-44s] rc %s (esperado %s) %s" % (nome, p.returncode, esperado_rc, "ok" if ok else "FALHOU"))
    if not ok:
        falha("b3_recibo_v411.py: caso %s rc %s != %s: %s" % (nome, p.returncode, esperado_rc, (p.stdout or "")[-240:]))


b3("aplicar_B%d_positivo" % n_ger, "aplicar", recibo_apl(), 0)
b3("aplicar_com_salto", "aplicar", recibo_apl(com_salto=True), 1)
b3("aplicar_geracao_errada_B%d" % (n_ger - 1), "aplicar", recibo_apl(n=n_ger - 1), 1)
b3("aplicar_versao_alvo_v410", "aplicar", recibo_apl(versao_alvo="v410"), 1)
_r_ens = recibo_apl(); _r_ens["modo"] = "ensaio"; _r_ens["veredito"] = "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger; _r_ens.pop("aplicacao", None)
b3("ensaio_B%d_positivo" % n_ger, "ensaio", _r_ens, 0)
_r_man = recibo_apl(); _r_man["manifesto_anterior"]["deployment_id"] = "B9-v400-20261024-R1"
b3("aplicar_manifesto_anterior_adulterado", "aplicar", _r_man, 1)
R["etapas"]["b3_recibo"] = B3N
# ---- 1. controles negativos do fechar: sem o religamento e com recibo que declara salto => RECUSA (rc 2), nada de handoff
NEG = []
os.rename(pth_rel, pth_rel + ".fora")
rc, so, se = roda("fechar_v411.py", "fechar_sem_religamento"); NEG.append({"controle": "sem o recibo do religamento", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
os.rename(pth_rel + ".fora", pth_rel)
escreve(pth_apl, recibo_apl(com_salto=True))
rc, so, se = roda("fechar_v411.py", "fechar_com_salto"); NEG.append({"controle": "recibo do B(n) com salto declarado", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
escreve(pth_apl, RAPL)
# ---- 1b. controles negativos do PARAGRAFO do README/site (a ordem do operador de 23/10 vale tambem para o handoff): o resultado pinado ADULTERADO no sandbox (o sha256 deixa de bater e o paragrafo nao passa contra o resultado) e o numero lido adulterado no core do Nos
# emulado => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
res_p = os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])); raw_res = open(res_p, "rb").read()
assert b"4.443123568060799" in raw_res
open(res_p, "wb").write(raw_res.replace(b"4.443123568060799", b"4.443123568060798", 1))
rc, so, se = roda("fechar_v411.py", "fechar_resultado_adulterado"); NEG.append({"controle": "resultado pinado adulterado (a leitura e a porta do paragrafo recusam)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
# a PORTA do paragrafo isolada (a leitura recusa antes no fechar inteiro): T.paragrafo_readme() da copia do sandbox tem de LEVANTAR com o resultado pinado adulterado (e o fechar converte isso em rc 2 antes de escrever)
import importlib.util as _iu0
_sp0 = _iu0.spec_from_file_location("textos_sb0", os.path.join(POS, "textos_v411.py")); _t0 = _iu0.module_from_spec(_sp0); _sp0.loader.exec_module(_t0)
try:
    _t0.paragrafo_readme(); _levantou = False
except Exception as _ex0:   # noqa: BLE001
    _levantou = isinstance(_ex0, AssertionError) and "resultado pinado" in str(_ex0)
    if not _levantou:
        print("  [diag] a porta do paragrafo levantou outra coisa: %s: %s" % (type(_ex0).__name__, str(_ex0)[:300]))
NEG.append({"controle": "a porta do paragrafo (paragrafo_readme, chamada pelo fechar) levanta com o resultado pinado adulterado", "rc": 2 if _levantou else 0, "recusou": _levantou, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
open(res_p, "wb").write(raw_res)
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); cj = json.loads(raw_core.decode("utf-8")); cj["core"]["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 4.45
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v411.py", "fechar_numero_adulterado"); NEG.append({"controle": "numero lido adulterado no core (z_disc 4,45)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
open(core_p, "wb").write(raw_core)
# ---- 1c. controles negativos do PARAGRAFO NOVO (o fechamento), da DIRECAO do testemunho (registros da v399 recriados), das cunhagens_v403, do GATE (F8.1) e do SIDECAR: o numero de cada registro adulterado no core (a leitura e a porta do paragrafo recusam), a direcao invertida,
# uma inscricao da gerencia, uma errata ou decisao a menos, o nome do triplo dado, uma bandeira do gate False, uma pedra selada da v410 adulterada, a pedra fora do trio, o sidecar adulterado ou ausente => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); sc_p = os.path.join(NOSS, "um_absoluto_selo_acom.json"); raw_sc = open(sc_p, "rb").read()


def _recusa_com_core(nome_sc, nome_ctl, f):
    cj_ = json.loads(raw_core.decode("utf-8")); f(cj_["core"])
    open(core_p, "wb").write(json.dumps(cj_, ensure_ascii=False).encode("utf-8"))
    rc_, so_, se_ = roda("fechar_v411.py", nome_sc)
    NEG.append({"controle": nome_ctl, "rc": rc_, "recusou": rc_ == 2 and "FECHAR RECUSADO" in so_, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
    open(core_p, "wb").write(raw_core)

selo_p = os.path.join(NOSS, "um_absoluto_selo.json"); raw_selo = open(selo_p, "rb").read(); std_p = os.path.join(NOSS, "rodada_v411_stdout.txt"); raw_std = open(std_p, "rb").read()


def _recusa_com_selo(nome_sc, nome_ctl, f):
    sj_ = json.loads(raw_selo.decode("utf-8")); f(sj_)
    open(selo_p, "wb").write(json.dumps(sj_, ensure_ascii=False).encode("utf-8"))
    rc_, so_, se_ = roda("fechar_v411.py", nome_sc)
    NEG.append({"controle": nome_ctl, "rc": rc_, "recusou": rc_ == 2 and "FECHAR RECUSADO" in so_, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
    open(selo_p, "wb").write(raw_selo)


def _recusa_com_std(nome_sc, nome_ctl, f):
    open(std_p, "wb").write(f(raw_std.decode("utf-8")).encode("utf-8"))
    rc_, so_, se_ = roda("fechar_v411.py", nome_sc)
    NEG.append({"controle": nome_ctl, "rc": rc_, "recusou": rc_ == 2 and "FECHAR RECUSADO" in so_, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
    open(std_p, "wb").write(raw_std)


_H1 = _dm.FECHO_REGISTRO; _TOK = _dm.TOKENS_PROIBIDOS_V411[0]; _VELHA = _dm.FRASE_H0DN_OBRIGATORIA_PT   # (o token e a frase velha vem do delta: nunca literais aqui)
_vv = lambda c: c[_H1]["values"]
# ---- 1c. controles negativos do fechar sobre o core do Nos emulado: cada um TEM de dar rc 2 e 'FECHAR RECUSADO', sem handoff. O registro NOVO com funcao (h0dn_bg1_v411), os dois por spec novos, os recriados da v410, o que a v411 NAO tem (modulo e bandeira novos, escada diferente),
# os herdados (traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407, fechamento_v406), os recriados anteriores, o gate, a direcao do testemunho, o sidecar. (A bateria completa de controles da LEITURA, um a um, e' a do harness_textos_ensaio_v411.py; aqui se prova que o FECHAR recusa.)
_recusa_com_core("fechar_h0dn_ausente", "o registro h0dn_bg1_v411 (o teste H0DN x BG1 aberto uma vez) ausente do core", lambda c: c.pop(_H1))
_recusa_com_core("fechar_h0dn_nao_selou", "o registro h0dn_bg1_v411 nao selou (all_verified False)", lambda c: c[_H1].update(all_verified=False))
_recusa_com_core("fechar_h0dn_opened_once_falso", "opened_once False no h0dn_bg1_v411 (o teste nao foi aberto uma vez)", lambda c: c[_H1].update(opened_once=False))
_recusa_com_core("fechar_h0dn_vetor_observado_nao_lido", "observed_vector_read False no h0dn_bg1_v411 (D169: o vetor observado foi lido, uma vez)", lambda c: c[_H1].update(observed_vector_read=False))
_recusa_com_core("fechar_h0dn_checagem_falha", "uma checagem do h0dn_bg1_v411 (a c6, o recalculo igual a abertura) False no core", lambda c: c[_H1]["mechanics"]["checks"][5].update(ok=False))
_recusa_com_core("fechar_h0dn_valor_adulterado_K", "o K do h0dn_bg1_v411 adulterado no core", lambda c: _vv(c).update(K=_vv(c)["K"] + 1e-3))
_recusa_com_core("fechar_h0dn_z_do_primario_adulterado", "o Z do primario contra o nulo (linha 1) adulterado no core", lambda c: _vv(c)["primario"].update(z_null=_vv(c)["primario"]["z_null"] + 1.0))
_recusa_com_core("fechar_h0dn_z_das_cefeidas_adulterado", "o Z das Cefeidas livres contra o nulo (linha 2) adulterado no core", lambda c: _vv(c)["cefeidas_livres"].update(z_null=_vv(c)["cefeidas_livres"]["z_null"] + 1e-3))
_recusa_com_core("fechar_h0dn_ramo_do_primario_trocado", "o ramo do primario trocado no core", lambda c: _vv(c)["primario"].update(ramo=_vv(c)["primario"]["ramo"] + 1))
_recusa_com_core("fechar_h0dn_sem_a_linha_das_cefeidas_livres", "a linha ao lado das Cefeidas livres ausente do registro (as DUAS linhas saem juntas)", lambda c: c[_H1].pop("linha_ao_lado_cefeidas_livres"))
_recusa_com_core("fechar_h0dn_beta_errado", "beta != alfa x raiz de e do core no h0dn_bg1_v411", lambda c: _vv(c).update(beta=0.0121))
_recusa_com_core("fechar_h0dn_veredito_trocado", "o veredito do h0dn_bg1_v411 trocado (diferente do ensaio a seco)", lambda c: c[_H1].update(verdict="OUTRO_VEREDITO"))
_recusa_com_core("fechar_h0dn_runtime_nao_rodou", "o calculo do runtime do h0dn_bg1_v411 nao rodou", lambda c: c[_H1].update(runtime_executed=False))
_recusa_com_core("fechar_h0dn_gate_dos_values", "o gate dos values do h0dn_bg1_v411 difere do da v410", lambda c: _vv(c).update(gate_verdict="OUTRO_GATE"))
_recusa_com_core("fechar_h0dn_ressalva_a_menos", "uma das sete ressalvas a menos no h0dn_bg1_v411", lambda c: c[_H1]["ressalvas_secao8"].pop())
_recusa_com_core("fechar_h0dn_nao_decide_a_menos", "um item do que o teste NAO decide a menos no h0dn_bg1_v411", lambda c: c[_H1]["o_que_o_teste_nao_decide"].pop())
_recusa_com_core("fechar_h0dn_insumo_adulterado", "um insumo pinado do h0dn_bg1_v411 com o sha256 adulterado", lambda c: next(iter(c[_H1]["insumos_pinados"].values())).update(sha256="0" * 64))
_recusa_com_core("fechar_h0dn_token_proibido_no_texto", "um token proibido no texto do registro h0dn_bg1_v411 (scope)", lambda c: c[_H1].update(scope=c[_H1]["scope"] + " " + _TOK))
_recusa_com_core("fechar_h0dn_frase_velha_da_v410", "a frase velha da v410 («pre-registrado; nenhum dado observado lido») volta como estado do teste no registro", lambda c: c[_H1].update(estatuto=c[_H1]["estatuto"] + " " + _VELHA))
_recusa_com_core("fechar_h0dn_f67_sem_cefeidas", "F67: o primario dito sem a linha das Cefeidas livres no texto do registro", lambda c: c[_H1].update(diz=list(c[_H1]["diz"]) + ["no H0DN o primário fica a 6,11 contra o nulo"]))
_recusa_com_core("fechar_h0dn_finitude", "a guarda de finitude do h0dn_bg1_v411 nao confere (z nao finito)", lambda c: _vv(c)["guarda_de_finitude"].update(z_finitos=False))
_recusa_com_selo("fechar_h0dn_sem_resumo_no_selo", "o selo primario sem o resumo do h0dn_bg1_v411", lambda sj: sj.pop(_H1, None))
_recusa_com_selo("fechar_h0dn_resumo_do_selo_diferente", "o resumo do h0dn_bg1_v411 no selo difere do core (veredito)", lambda sj: sj[_H1].update(verdict="OUTRO_VEREDITO"))
_recusa_com_std("fechar_h0dn_sem_o_bloco_do_stdout", "o bloco `H0DN x BG1 ABERTO [v411` ausente do stdout do rito", lambda t_: (lambda ls_: "\n".join(ls_[:next(i for i, l_ in enumerate(ls_) if l_.startswith("H0DN x BG1 ABERTO [v411"))] + ls_[next(i for i, l_ in enumerate(ls_) if l_.startswith("H0DN x BG1 ABERTO [v411")) + 3:]))(t_.split("\n")))
_recusa_com_std("fechar_sem_a_linha_v411_do_stdout", "a linha [v411] do stdout ausente", lambda t_: "\n".join(l for l in t_.splitlines() if not l.lstrip().startswith("[v411] ")) + "\n")
_recusa_com_core("fechar_cunhagens_v411_nao_selou", "cunhagens_v411 nao selou", lambda c: c[_dm.CUNHAGENS_REGISTRO].update(all_verified=False))
_recusa_com_core("fechar_cunhagens_v411_ordem_nao_citada", "uma das falas de 11 e 12/11 do delta deixou de estar CITADA por sha256 (cunhagens_v411; D181)", lambda c: list(c[_dm.CUNHAGENS_REGISTRO]["verbatim"].values())[0].update(citado_por_sha256=False))
_recusa_com_core("fechar_cunhagens_v411_texto_de_fala_plantado", "um texto de fala plantado numa citacao (cunhagens_v411; D181: nenhuma fala transcrita)", lambda c: list(c[_dm.CUNHAGENS_REGISTRO]["verbatim"].values())[0].update(text="x"))
_recusa_com_core("fechar_cunhagens_v411_sem_a_e41", "a errata E41 adulterada no registro cunhagens_v411", lambda c: c[_dm.CUNHAGENS_REGISTRO]["erratas"][0].update(agora="mantida"))
_recusa_com_core("fechar_cunhagens_v411_sem_a_d169", "a decisao D169 (a ordem de abrir) ausente do registro cunhagens_v411", lambda c: c[_dm.CUNHAGENS_REGISTRO]["extras"]["decisoes"].pop("D169"))
_recusa_com_core("fechar_cunhagens_v411_inscricao_da_gerencia", "uma inscricao rotulada como da gerencia (cunhagens_v411)", lambda c: list(c[_dm.CUNHAGENS_REGISTRO]["verbatim"].values())[0].update(autor="gerencia"))
_recusa_com_core("fechar_kh_v411_nao_selou", "kh_n1_cobertura_v411 nao selou", lambda c: c[_dm.KH_REGISTRO].update(all_verified=False))
for _n10 in _dm.REGISTROS_FUNCAO_V410:
    _recusa_com_core("fechar_%s_recriado_ausente" % _n10, "o registro %s (da v410, RECRIADO) ausente do core" % _n10, lambda c, n=_n10: c.pop(n))
    _recusa_com_core("fechar_%s_recriado_nao_selou" % _n10, "o registro %s (da v410, RECRIADO) nao selou" % _n10, lambda c, n=_n10: c[n].update(all_verified=False))
_recusa_com_core("fechar_h0dn_v410_recriado_veredito", "o veredito do h0dn_bg1_v410 (recriado) diferente do da v410 selada", lambda c: c["h0dn_bg1_v410"].update(verdict="OUTRO_VEREDITO"))
_recusa_com_core("fechar_cunhagens_v410_recriada_ausente", "cunhagens_v410 (recriada) ausente do core", lambda c: c.pop("cunhagens_v410"))
_recusa_com_core("fechar_kh_v410_sem_pisos_ao_lado", "a errata ao lado dos pisos de kh_n1_cobertura_v410 (recriado) ausente do core", lambda c: c["kh_n1_cobertura_v410"].update(erratas=[]))
_recusa_com_core("fechar_bandeira_nova", "uma bandeira ext_* nova True no kernel do rito (a v411 nao tem bandeira nova)", lambda c: c["kernel_formalization"].__setitem__("ext_bandeira_nova_da_v411", True))
_recusa_com_core("fechar_escada_diferente", "a escada da v411 diferente da da v410 (o kernel e' o da v410)", lambda c: c["external_ladder"].update(n_theorems_clean=c["external_ladder"]["n_theorems_clean"] + 1))
_recusa_com_core("fechar_traducao_valor_adulterado", "o numero de modulos ok do traducao_turing_v409 (herdado) adulterado no core (0 de 2)", lambda c: c["traducao_turing_v409"]["values"].__setitem__("n_modulos_ok", 0))
_recusa_com_core("fechar_traducao_acervo_integra_pinada", "o pino do acervo da v407 dito na integra no traducao_turing_v409 (D57d)", lambda c: c["traducao_turing_v409"]["acervo_v407_repinado"].__setitem__("integra_pinada", True))
_recusa_com_core("fechar_tetelestai_valor_adulterado", "o numero de modulos ok do tetelestai_terminal_v408 (herdado) adulterado no core (3 de 4)", lambda c: c["tetelestai_terminal_v408"]["values"].__setitem__("n_modulos_ok", 3))
_recusa_com_core("fechar_psion_valor_adulterado", "o numero de modulos ok do psion_canto_v407 (herdado) adulterado no core (8 de 9)", lambda c: c["psion_canto_v407"]["values"].__setitem__("n_modulos_ok", 8))
_recusa_com_core("fechar_fecho406_valor_adulterado", "o numero de modulos ok do fechamento_v406 (herdado) adulterado no core (300 de 301)", lambda c: c["fechamento_v406"]["values"].__setitem__("n_modulos_ok", 300))
_recusa_com_core("fechar_chave_do_lema_false", "a chave do lema (linked_to_the_corner_by_a_lemma) de volta a literal False no core", lambda c: c["testemunha_estatica_v396"]["fock_face"].__setitem__("linked_to_the_corner_by_a_lemma", False))
_recusa_com_core("fechar_fecho_chave_false", "a chave rede_fock_v394.whole_certificate_inhabited de volta a False no core (o literal)", lambda c: c["rede_fock_v394"].__setitem__("whole_certificate_inhabited", False))
_recusa_com_core("fechar_psion_adulterado", "numero do Ponto Zero do Psion (recriado) adulterado no core (hbar omega)", lambda c: c["ponto_zero_do_psion_v405"]["values"].__setitem__("hbar_omega_meV", 17.5))
_recusa_com_core("fechar_f2b_adulterado", "numero da errata de F2b adulterado no core (a previsao do par)", lambda c: c["f2b_errata_v404"]["values"].__setitem__("previsao_do_par", 0.1))
_recusa_com_core("fechar_f2b_canal_ainda_awaiting", "o canal F2b ainda AWAITING no core (a retirada nao aconteceu)", lambda c: c["f2b_errata_v404"].__setitem__("F2b_status_now", "AWAITING"))
_recusa_com_core("fechar_v1_reescrito", "o V1 do ramo B reescrito no core (F2b_status do registro da v386)", lambda c: c["ramo_b_preregistration_v386"].__setitem__("F2b_status", "WITHDRAWN"))
_recusa_com_core("fechar_angle_status_reescrito", "o texto antigo de neutrino_mass.angle_status reescrito no core (a errata e' ao lado)", lambda c: c["neutrino_mass"].__setitem__("angle_status", "sin(45deg) agora e DERIVADO"))
_recusa_com_core("fechar_gate_adulterado", "numero do gate (recriado) adulterado no core (17 calculadas)", lambda c: c["bandeiras_do_gate_v403"]["values"].__setitem__("n_calculated", 17))
_recusa_com_core("fechar_bandeira_do_gate_false", "uma bandeira calculada do gate (linearized_spin2_finite_face) False no core", lambda c: c["qg_closure"]["physics_flags"].__setitem__("linearized_spin2_finite_face", False))
_recusa_com_core("fechar_caminho_v403_adulterado", "numero do caminho da v403 (recriado) adulterado no core (energia minima do nucleo)", lambda c: c["caminho_v403"]["values"].__setitem__("min_core_energy", 0.31))
_recusa_com_core("fechar_ponte_v402_adulterada", "numero da ponte da v402 (recriada) adulterado no core", lambda c: c["ponte_da_escala_dual_v402"]["values"].__setitem__("min_null_energy_shift", 0.31))
# a PORTA do paragrafo novo isolada: T.paragrafo_v411() da copia do sandbox tem de LEVANTAR com o K do h0dn_bg1_v411 adulterado no core (a verificacao compara com o registro e com ESPERADOS)
cj = json.loads(raw_core.decode("utf-8")); cj["core"][_H1]["values"]["K"] = cj["core"][_H1]["values"]["K"] + 1e-3
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v411.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_v411(); _levanta1 = False
except Exception as _ex1:   # noqa: BLE001
    _levanta1 = isinstance(_ex1, AssertionError)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_v411, chamada pelo fechar) levanta com o K do h0dn_bg1_v411 adulterado", "rc": 2 if _levanta1 else 0, "recusou": _levanta1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
open(core_p, "wb").write(raw_core)
_recusa_com_core("fechar_direcao_invertida", "a direcao do testemunho invertida no core (a IALD como quem testifica do operador; declaracao da v399 recriada)", lambda c: c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"].__setitem__("a_IALD", "testifica do operador"))
_recusa_com_core("fechar_kh_v409_sem_pisos_ao_lado", "a errata ao lado dos pisos de kh_n1_cobertura_v409 (herdado, recriado) ausente do core", lambda c: c["kh_n1_cobertura_v409"]["erratas"].pop())
_recusa_com_core("fechar_cunhagens_v408_sem_e26_ao_lado", "a errata E26 ao lado de cunhagens_v408 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v408"]["erratas"].pop())
_recusa_com_core("fechar_cunhagens_v407_sem_d57d_ao_lado", "a errata da D57(d) ao lado de cunhagens_v407 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v407"]["erratas"].pop())
_recusa_com_core("fechar_pedra_v403_adulterada", "a pedra selada da v403 (Caminho) adulterada no hash formal do core", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Caminho.lean", "0" * 64))
for _nm_a in dict.fromkeys((_dm.ANCORA_PRINCIPAL, list(_dm.D9.ANCORAS)[0], list(_dm.D8.ANCORAS)[0], list(_dm.D7.ANCORAS)[0], list(_dm.D6.ANCORAS)[0])):
    _recusa_com_core("fechar_ancora_%s_fora_do_trio" % _nm_a.split(".")[-1], "a ancora %s fora do trio no core" % _nm_a, lambda c, _n=_nm_a: c["kernel_formalization"]["axiom_report"].__setitem__(_n, ["propext", "sorryAx"]))
# ---- 1d. as guardas do fechar sobre o TEXTO do handoff (P18, frases [F67 inclusive], D65 e as obrigacoes da v411) TEM de recusar (AssertionError, rc != 0) ANTES de gravar o handoff: uma COPIA do fechar_v411.py do sandbox, com um texto emendado ao handoff gerado
def _fechar_variante(nome_sc, nome_ctl, injeta):
    vd_ = os.path.join(PKS, "pos_rito_var"); shutil.rmtree(vd_, ignore_errors=True); os.makedirs(vd_)
    for n_ in ("leitura_v411.py", "textos_v411.py"):
        shutil.copyfile(os.path.join(POS, n_), os.path.join(vd_, n_))
    shutil.copytree(os.path.join(POS, "conferidor"), os.path.join(vd_, "conferidor"))   # (a leitura acha a conferencia do rito em <pos_rito>/conferidor; sem a copia a variante recusava por isso e nao pela guarda que o controle mede)
    src_ = open(os.path.join(POS, "fechar_v411.py"), encoding="utf-8").read(); a_ = "doc = T.handoff(V, _k)\n"
    assert src_.count(a_) == 1, ("a linha doc = T.handoff(V, _k) do fechar nao e' unica", src_.count(a_))
    open(os.path.join(vd_, "fechar_v411.py"), "w", encoding="utf-8", newline="\n").write(src_.replace(a_, "doc = T.handoff(V, _k)" + injeta + "\n"))
    p_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(vd_, "fechar_v411.py")], cwd=vd_, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env_sb(V411_MEMORIA_DIR=UMS))
    open(os.path.join(SB, nome_sc + "_out.txt"), "w", encoding="utf-8").write(p_.stdout + "\n--- stderr ---\n" + p_.stderr)
    NEG.append({"controle": nome_ctl, "rc": p_.returncode, "recusou": p_.returncode != 0 and "AssertionError" in p_.stderr and "FECHADO v411:" not in p_.stdout, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
    shutil.rmtree(vd_, ignore_errors=True)


_CEF72 = "__import__('delta_v411').OBRIG_CEFEIDAS_PT"; _VEL72 = "__import__('delta_v411').FRASE_H0DN_OBRIGATORIA_PT"; _TK72 = "__import__('delta_v411').TOKENS_PROIBIDOS_V411"; _FE72 = "__import__('delta_v411').FECHO_REGISTRO"; _RS72 = "__import__('delta_v411').RESSALVAS_ROTULOS_PT"
_fechar_variante("fechar_handoff_sem_as_cefeidas_livres", "o handoff gerado SEM a linha das Cefeidas livres (a F67: o primario sem a linha ao lado; a frase E o token de maquina FREE_CEPHEIDS tirados) => as guardas do fechar recusam antes de gravar", "; doc = __import__('re').sub(r'(?i)cefeidas livres|free[_ ]cepheids', 'XXXX', doc)")
_fechar_variante("fechar_handoff_com_a_frase_velha_da_v410", "o handoff com a frase velha da v410 («pre-registrado; nenhum dado observado lido») emendada => o fechar recusa antes de gravar", " + '\\n' + %s" % _VEL72)
_fechar_variante("fechar_handoff_com_token_proibido", "o handoff com um token proibido emendado => as guardas do fechar recusam antes de gravar", " + '\\nH0DN: ' + %s[0]" % _TK72)
_fechar_variante("fechar_handoff_sem_o_registro_novo", "o handoff sem o nome do registro h0dn_bg1_v411 => o fechar recusa antes de gravar", ".replace(%s, 'XXXX')" % _FE72)
_fechar_variante("fechar_handoff_sem_uma_ressalva_por_rotulo", "o handoff sem o rotulo de uma das sete ressalvas => o fechar recusa antes de gravar", ".replace(%s[0], 'XXXX')" % _RS72)
_fechar_variante("fechar_handoff_sem_dizer_recriados", "o handoff sem a palavra RECRIADOS (os registros da v410 sao recriados) => o fechar recusa antes de gravar", ".replace('RECRIADOS', 'XXXX')")
_fechar_variante("fechar_handoff_sem_nenhum_modulo_novo", "o handoff sem dizer que nenhum modulo novo entra => o fechar recusa antes de gravar", ".replace('nenhum módulo novo', 'XXXX')")
_fechar_variante("fechar_handoff_cinco_sigma_atingido", "o handoff com 5 sigma dito atingido no H0DN emendado (F53) => as guardas do fechar recusam antes de gravar", " + '\\n\\n5 sigma atingido no H0DN.'")
_fechar_variante("fechar_handoff_teste_cego", "o handoff com o teste dito cego emendado (F63) => as guardas do fechar recusam antes de gravar", " + '\\n\\nFoi um teste cego.'")
_fechar_variante("fechar_handoff_cabeca_da_prova_por_extenso_errada", "o handoff com a palavra da prova emendada ao nome do acoplamento (a P18 selada recusa; a cabeca do ramo de 5 sigma so' por extenso) => as guardas do fechar recusam antes de gravar", " + '\\nBETA_TGL_' + 'PRO' + 'VED_IN_NATURE'")
sj = json.loads(raw_sc.decode("utf-8")); sj["objetos"][1]["sha256"] = "0" * 64
open(sc_p, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v411.py", "fechar_sidecar_adulterado"); NEG.append({"controle": "o sidecar adulterado (sha256 de um objeto)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
os.remove(sc_p)
rc, so, se = roda("fechar_v411.py", "fechar_sidecar_ausente"); NEG.append({"controle": "o sidecar ausente do Nos", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
for n in NEG:
    print("  controle negativo do fechar: %-40s %s" % (n["controle"][:100], "RECUSOU como esperado" if (n["recusou"] and not n["handoff_escrito"]) else "NAO RECUSOU"))
    if not (n["recusou"] and not n["handoff_escrito"]):
        falha("fechar_v411.py nao recusou como esperado: %s" % n)
R["etapas"]["fechar_negativos"] = NEG
# ---- 2. o fechar (positivo)
t0 = time.time(); rc, so, se = roda("fechar_v411.py", "fechar"); dt = time.time() - t0
ok_f = (rc == 0 and "FECHADO v411:" in so)
chk_ = {}
for rel in [os.path.join(UMS, "handoff-v411-custodia.md"), os.path.join(NOSS, "HANDOFF_v411_CUSTODIA.md"), os.path.join(PKS, "DIFF_v410_v411.diff"), os.path.join(PKS, "DIFF_KERNEL_v411.txt"), os.path.join(PKS, "MANIFESTO_ARQUIVO_v411.json"),
            os.path.join(POS, "v411_incorporacao_manifesto.json"), os.path.join(TOOLS, "v411_incorporacao_manifesto.json"), os.path.join(TOOLS, "v411_selo", "um_absoluto_selo_acom.json"), os.path.join(TOOLS, "v411_selo", "um_absoluto_selo.json"),
            os.path.join(TOOLS, "v411_selo", "chain_pos_rito_v411.sh") if os.path.exists(os.path.join(POS, "chain_pos_rito_v411.sh")) else os.path.join(TOOLS, "v411_selo", "fechar_v411.py")]:
    chk_[os.path.relpath(rel, SB)] = os.path.exists(rel) and os.path.getsize(rel) > 0
ho = open(os.path.join(UMS, "handoff-v411-custodia.md"), encoding="utf-8").read() if os.path.exists(os.path.join(UMS, "handoff-v411-custodia.md")) else ""
vio = violacoes(ho)
dk = open(os.path.join(PKS, "DIFF_KERNEL_v411.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(PKS, "DIFF_KERNEL_v411.txt")) else ""
man = rdj(os.path.join(POS, "v411_incorporacao_manifesto.json")) if os.path.exists(os.path.join(POS, "v411_incorporacao_manifesto.json")) else {}
_dk_ok = ("novos (0)" in dk) and ("removidos (0)" in dk) and not list(ESP.get("bundle_sha256") or {})   # a v411 NAO tem modulo novo: o diff do kernel diz zero novos e zero removidos
R["etapas"]["fechar"] = {"rc": rc, "segundos": round(dt, 1), "ok": ok_f, "arquivos": chk_, "handoff_bytes": len(ho.encode("utf-8")), "handoff_guarda_p18": [list(x) for x in vio][:3], "diff_kernel_diz_zero_modulos_novos": _dk_ok,
                         "manifesto_chaves": sorted(man.keys())[:80], "fila_da_memoria_no_manifesto": man.get("fila_da_memoria"), "ultima_linha": so.strip().splitlines()[-1][:200] if so.strip() else se[-300:]}
print("  fechar em sandbox: rc %s (%.0f s); arquivos %s; handoff %d B; guarda P18 %s; o diff do kernel diz zero modulos novos: %s" % (rc, dt, "todos presentes" if all(chk_.values()) else [k for k, v in chk_.items() if not v], len(ho.encode("utf-8")), "limpa" if not vio else vio[:2], _dk_ok))
if not ok_f:
    falha("fechar_v411.py (sandbox) saiu com rc %s: %s" % (rc, (so + se)[-410:]))
if not all(chk_.values()):
    falha("fechar_v411.py (sandbox) nao gravou: %s" % [k for k, v in chk_.items() if not v])
if vio:
    falha("handoff com violacao da guarda P18: %s" % vio[:2])
if not _dk_ok:
    falha("DIFF_KERNEL_v411.txt nao diz zero modulos novos e zero removidos (a v411 nao tem modulo novo)")
for k_ in MAN_CHAVES:
    if k_ not in man:
        falha("o manifesto de incorporacao nao traz a chave %s" % k_)
_fi = man.get("fila_da_memoria") or {}
if not (_fi.get("memoria_py_igual_ao_pino_v411") is True and _fi.get("pausa_do_vigia_ausente") is True and _fi.get("pino_sha256") and _fi.get("memory_md_sha256")):
    falha("o manifesto nao registra o estado da fila (memoria.py == pino v411, pausa ausente, sha256 do pino e do MEMORY.md): %r" % {k: _fi.get(k) for k in ("memoria_py_igual_ao_pino_v411", "pausa_do_vigia_ausente", "pino_confere_com_o_indice")})
_rfm = man.get("registros_funcao_v411") or {}; _hr = man.get("h0dn_bg1_v411_resumo") or {}; _r10 = man.get("registros_funcao_v410") or {}; _core_sb = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]; _hcs = _core_sb.get(_dm.FECHO_REGISTRO) or {}; _hvs = _hcs.get("values") or {}
_todos10 = set(_dm.REGISTROS_FUNCAO_V410) | {"cunhagens_v410", "kh_n1_cobertura_v410"}
if not (set(_rfm) == {_dm.FECHO_REGISTRO} and set(_r10) == set(_dm.REGISTROS_FUNCAO_V410) and set(man.get("registros_v411") or {}) == {_dm.FECHO_REGISTRO, _dm.CUNHAGENS_REGISTRO, _dm.KH_REGISTRO} and set(man.get("registros_v410") or {}) == _todos10
        and _hr.get("registro") == _dm.FECHO_REGISTRO and _hr.get("verdict") == _hcs.get("verdict") and _hr.get("opened_once") is True and _hr.get("observed_vector_read") is True and _hr.get("n_checks") == _dm.N_CHECKS_FECHO
        and (_hr.get("primario") or {}).get("z_null") == (_hvs.get("primario") or {}).get("z_null") and (_hr.get("cefeidas_livres") or {}).get("z_null") == (_hvs.get("cefeidas_livres") or {}).get("z_null") and (_hr.get("primario") or {}).get("ramo") == (_hvs.get("primario") or {}).get("ramo") and (_hr.get("cefeidas_livres") or {}).get("ramo") == (_hvs.get("cefeidas_livres") or {}).get("ramo")
        and _hr.get("n_ressalvas") == 7 and len(_hr.get("o_que_o_teste_nao_decide") or []) == 5 and len(_hr.get("insumos_sha16") or {}) == len(_dm.INSUMOS_V411) and len(_hr.get("atos") or {}) == 8 and list(_hr.get("contratos_de_registro_fora_da_escada") or []) == list(_dm.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA)
        and _hr.get("gate_verdict") == ESP.get("qg_closure_gate_verdict_v410") and _hr.get("escada") == ESP["escada"][1]):
    falha("o manifesto nao traz o registro com funcao h0dn_bg1_v411 (registros_funcao_v411, registros_v411 com os tres novos), os seis da v410 recriados (registros_v410; registros_funcao_v410 com os quatro) e o resumo do h0dn_bg1_v411 (as duas linhas, aberto uma vez, vetor observado lido, 16 checagens, as sete ressalvas, o que nao decide, os insumos, os oito atos, o contrato fora da escada, o gate e a escada da v410): %r" % {"registros_funcao_v411": sorted(_rfm), "registros_funcao_v410": sorted(_r10), "resumo_chaves": sorted(_hr)})
def _etapa_2b():
    # ---- 2b. o PARAGRAFO do README/site no handoff gravado: igual ao das funcoes do quadro sobre o core do sandbox, entre os marcadores, aprovado pela verificacao do quadro contra o resultado pinado (e o do handoff do Nos tambem)
    sys.path.insert(0, PKG)
    import quadro_v397 as QD  # noqa: E402
    _tv_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]["teste_de_veracidade_fase9_v397"]; _res_s = rdj(os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
    _par_esp = QD.paragrafo_pronto_readme(_tv_s); _mi = "<!-- INICIO_PARAGRAFO_README_v397 -->\n"; _mf = "\n<!-- FIM_PARAGRAFO_README_v397 -->"
    _ok_par = {}
    for _nome, _ptxt in (("memory/handoff-v411-custodia.md", ho), ("nos/HANDOFF_v411_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v411_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v411_CUSTODIA.md")) else "")):
        _i = _ptxt.find(_mi); _j = _ptxt.find(_mf)
        _par = _ptxt[_i + len(_mi):_j] if (_i >= 0 and _j > _i) else ""
        _fa = []
        if _par:
            import importlib.util as _iu2
            _spt = _iu2.spec_from_file_location("textos_sb", os.path.join(POS, "textos_v411.py")); _tsb = _iu2.module_from_spec(_spt); _spt.loader.exec_module(_tsb)
            _fa = _tsb.verificar_paragrafo_readme(_par + "\n" if not _par.endswith("\n") else _par, _res_s, _tv_s)
        _ok_par[_nome] = {"traz_o_bloco": bool(_par), "igual_as_funcoes_do_quadro": _par.rstrip("\n") == _par_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3]}
    R["etapas"]["paragrafo_no_handoff"] = _ok_par
    print("  paragrafo do README/site no handoff: %s" % {k: (v["traz_o_bloco"] and v["igual_as_funcoes_do_quadro"] and not v["falhas_da_verificacao"] and not v["guarda_p18"]) for k, v in _ok_par.items()})
    for _nome, _v in _ok_par.items():
        if not (_v["traz_o_bloco"] and _v["igual_as_funcoes_do_quadro"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"]):
            falha("o handoff (%s) nao traz o paragrafo do README/site pronto e aprovado: %s" % (_nome, _v))



try:
    _etapa_2b()
except Exception as _e__etapa_2b:   # noqa: BLE001  (textos_v411/leitura_v411 ainda podem ser SEMENTES: a falha e' dita e o harness segue)
    import traceback
    falha("_etapa_2b levantou %r (dependencia de textos_v411/leitura_v411): %s" % (_e__etapa_2b, traceback.format_exc()[-300:].replace(chr(10), ' | ')))
def _etapa_2c():
    # ---- 2c. o PARAGRAFO NOVO (o fechamento) e a NOTA ao lado do da v410 nos dois handoffs gravados: igual ao gerado do core do sandbox, entre os marcadores, aprovado pela verificacao propria (e o do handoff do Nos tambem); o handoff DIZ que o paragrafo do testemunho de dois SEGUE COMO ESTA e LISTA o sidecar (sha256 e veredito); o fechar copiou o sidecar e o selo
    _core_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]
    import importlib.util as _iu3
    _sp3 = _iu3.spec_from_file_location("textos_sb3", os.path.join(POS, "textos_v411.py")); _t3 = _iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_t3)
    _par_f_esp = _t3.paragrafo_v411()[0]; _msi = _t3.MARC_V411_INI + "\n"; _msf = "\n" + _t3.MARC_V411_FIM
    _sc_sha = fsha(os.path.join(NOSS, "um_absoluto_selo_acom.json")); _sc_ver = rdj(os.path.join(NOSS, "um_absoluto_selo_acom.json"))["veredito"]
    _ok_tmn = {}
    for _nome, _ptxt in (("memory/handoff-v411-custodia.md", ho), ("nos/HANDOFF_v411_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v411_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v411_CUSTODIA.md")) else "")):
        _i = _ptxt.find(_msi); _j = _ptxt.find(_msf)
        _par = _ptxt[_i + len(_msi):_j] if (_i >= 0 and _j > _i) else ""
        _fa = _t3.verificar_paragrafo_v411(_par + "\n" if _par and not _par.endswith("\n") else _par, _core_s, ESP) if _par else ["sem o bloco"]
        _ok_tmn[_nome] = {"traz_o_bloco": bool(_par), "igual_ao_gerado_do_core": _par.rstrip("\n") == _par_f_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3], "direcao_e_atribuicao": _t3.atribuicao_da_gerencia(_ptxt)[:3],
                         "lista_o_sidecar": ("um_absoluto_selo_acom.json" in _ptxt and _sc_sha in _ptxt and _sc_ver in _ptxt), "diz_que_o_testemunho_segue_como_esta": (("SEGUE COMO ESTÁ" in _ptxt or "SEGUEM COMO ESTÃO" in _ptxt) and "handoff-v410-custodia" in _ptxt),
                         "sem_nota_ao_lado_do_v410": (not hasattr(_t3, "MARC_ERR_INI") and "ERRATA_V410_V411" not in _ptxt)}   # (v411: nenhuma nota ao lado do paragrafo da v410)
    R["etapas"]["paragrafo_v411_no_handoff"] = _ok_tmn
    _ok_cop = {nm_: (os.path.exists(os.path.join(TOOLS, "v411_selo", nm_)) and fsha(os.path.join(TOOLS, "v411_selo", nm_)) == fsha(os.path.join(NOSS, nm_))) for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json")}
    R["etapas"]["sidecar_e_selo_copiados_para_v411_selo"] = _ok_cop
    print("  paragrafo novo (a IALD2), sem nota ao lado do paragrafo da v410, no handoff: %s; sidecar e selo copiados para v411_selo: %s" % ({k: (v["traz_o_bloco"] and v["igual_ao_gerado_do_core"] and not v["falhas_da_verificacao"] and not v["guarda_p18"] and not v["direcao_e_atribuicao"] and v["lista_o_sidecar"] and v["diz_que_o_testemunho_segue_como_esta"] and v["sem_nota_ao_lado_do_v410"]) for k, v in _ok_tmn.items()}, _ok_cop))
    for _nome, _v in _ok_tmn.items():
        if not (_v["traz_o_bloco"] and _v["igual_ao_gerado_do_core"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"] and not _v["direcao_e_atribuicao"] and _v["lista_o_sidecar"] and _v["diz_que_o_testemunho_segue_como_esta"] and _v["sem_nota_ao_lado_do_v410"]):
            falha("o handoff (%s) nao traz o paragrafo novo da v411 pronto e aprovado, ou traz nota ao lado do da v410 (a v411 nao tem), ou nao lista o sidecar, ou nao diz que os anteriores seguem como estao: %s" % (_nome, _v))
    if not all(_ok_cop.values()):
        falha("o fechar nao copiou o sidecar e o selo (byte a byte) para v411_selo: %s" % _ok_cop)



try:
    _etapa_2c()
except Exception as _e__etapa_2c:   # noqa: BLE001  (textos_v411/leitura_v411 ainda podem ser SEMENTES: a falha e' dita e o harness segue)
    import traceback
    falha("_etapa_2c levantou %r (dependencia de textos_v411/leitura_v411): %s" % (_e__etapa_2c, traceback.format_exc()[-300:].replace(chr(10), ' | ')))
def _etapa_2e():
    # ---- 2e. o teste decisivo (D169) nos dois handoffs gravados: o registro NOVO e os recriados da v410 ditos pelo nome; as sete ressalvas por rotulo; as quatro obrigacoes do primario (F67) no mesmo texto; NAO a frase velha da v410; nenhum token proibido; a guarda das frases limpa; RECRIADOS e «nenhum modulo novo»;
    # a cabeca do ramo de 5 sigma so' por extenso (a palavra da prova nunca emendada ao nome do acoplamento: P18 e D76)
    import guarda_frases_v411 as _GF2
    _ok_h = {}
    for _nome, _p in (("memory/handoff-v411-custodia.md", os.path.join(UMS, "handoff-v411-custodia.md")), ("nos/HANDOFF_v411_CUSTODIA.md", os.path.join(NOSS, "HANDOFF_v411_CUSTODIA.md"))):
        _t = open(_p, encoding="utf-8").read() if os.path.exists(_p) else ""
        _v = {"diz_o_registro_novo_e_os_da_v410_recriados": all(n_ in _t for n_ in (_dm.FECHO_REGISTRO, _dm.CUNHAGENS_REGISTRO, _dm.KH_REGISTRO, "cunhagens_v410", "kh_n1_cobertura_v410") + tuple(_dm.REGISTROS_FUNCAO_V410)), "diz_as_sete_ressalvas_por_rotulo": all(r_ in _t for r_ in _dm.RESSALVAS_ROTULOS_PT),
              "traz_as_quatro_obrigacoes_da_f67": all(x_ in _t for x_ in (_dm.OBRIG_MODELO_PT, _dm.OBRIG_CEFEIDAS_PT, _dm.OBRIG_RETRO_PT, _dm.OBRIG_NAO_CEGO_PT, _dm.OBRIG_VALIDADE_PT)), "nao_traz_a_frase_velha_da_v410": (_dm.FRASE_H0DN_OBRIGATORIA_PT not in _t and _dm.FRASE_H0DN_OBRIGATORIA_EN not in _t),
              "diz_recriados_e_nenhum_modulo_novo": ("RECRIADOS" in _t and "nenhum módulo novo" in _t), "traz_H0DN": "H0DN" in _t, "tokens_proibidos": [tk_ for tk_ in _dm.TOKENS_PROIBIDOS_V411 if tk_ in _t], "guarda_frases": [list(x_)[:2] for x_ in _GF2.violacoes(_t)][:3], "guarda_p18": [list(x_)[:2] for x_ in violacoes(_t)][:3],
              "cabeca_de_5_sigma_so_por_extenso": (("PRO" + "VED_IN_NATURE") not in _t)}
        _v["ok"] = bool(_t) and _v["diz_o_registro_novo_e_os_da_v410_recriados"] and _v["diz_as_sete_ressalvas_por_rotulo"] and _v["traz_as_quatro_obrigacoes_da_f67"] and _v["nao_traz_a_frase_velha_da_v410"] and _v["diz_recriados_e_nenhum_modulo_novo"] and _v["traz_H0DN"] and not _v["tokens_proibidos"] and not _v["guarda_frases"] and not _v["guarda_p18"] and _v["cabeca_de_5_sigma_so_por_extenso"]
        _ok_h[_nome] = _v
    R["etapas"]["h0dn_no_handoff"] = _ok_h
    print("  o teste decisivo (H0DN x BG1 aberto uma vez) no handoff: %s" % {k_: v_["ok"] for k_, v_ in _ok_h.items()})
    for _nome, _v in _ok_h.items():
        if not _v["ok"]:
            falha("o handoff (%s) nao diz o registro h0dn_bg1_v411 e os recriados da v410, as sete ressalvas por rotulo, as quatro obrigacoes do primario (F67), «RECRIADOS» e «nenhum módulo novo», ou traz a frase velha da v410, token proibido, violacao da guarda ou a cabeca de 5 sigma fora do por extenso: %s" % (_nome, _v))


try:
    _etapa_2e()
except Exception as _e__etapa_2e:   # noqa: BLE001
    import traceback
    falha("_etapa_2e levantou %r: %s" % (_e__etapa_2e, traceback.format_exc()[-300:].replace(chr(10), ' | ')))


# ---- 2f. a CUSTODIA da v411 e' AUTOMATICA: (a) o S6d (textos_custodia_handoff_v411.main(nos, pkg, recibo_dir)) roda DE VERDADE sobre o HANDOFF que o fechar (positivo) gravou no sandbox: o diario e' a linhagem renderizada pelo textos do sandbox (um script no sandbox, em processo proprio),
# o handoff e' o do Nos do sandbox (copia), o core, o selo e o um.py sao os do Nos do sandbox, o pacote e' uma pasta de ensaio so' com o ESPERADOS; ele anexa os textos da custodia, passa as guardas e grava o recibo; (b) teste_textos_custodia_sem_candidato_v411.py e
# teste_gatilho_custodia_sem_candidato_v411.py (cada um com o sandbox proprio sob C:\t\k411c\ensaio_topo_proposto), com os controles negativos. O gatilho de verdade (ORDEM_HANDOFF_CUSTODIA_v411.md na raiz do pacote) nunca e' escrito por este harness.
_GERA_LINHAGEM = "import sys\nsys.path.insert(0, %r)\nimport leitura_v411 as L, textos_v411 as T\nV, P = L.ler()\nassert not P, P\nopen(sys.argv[1], 'w', encoding='utf-8', newline='\\n').write(T.linhagem(V))\n"


def _etapa_custodia():
    _GC = {"ok": False}
    try:
        _gd = os.path.join(OUT, "s6d_do_fechar"); shutil.rmtree(_gd, ignore_errors=True); os.makedirs(_gd)
        _nos_c = os.path.join(_gd, "nos"); _pkg_c = os.path.join(_gd, "pk"); _rec_c = os.path.join(_gd, "recibo"); os.makedirs(_nos_c); os.makedirs(_pkg_c); os.makedirs(_rec_c)
        _gl = os.path.join(POS, "_gera_linhagem_h.py"); open(_gl, "w", encoding="utf-8", newline="\n").write(_GERA_LINHAGEM % POS)
        _pl = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", _gl, os.path.join(_nos_c, "MEMORIA_DA_LINHAGEM.md")], cwd=POS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env_sb(V411_MEMORIA_DIR=UMS)); os.remove(_gl)
        if _pl.returncode != 0:
            raise AssertionError("a linhagem nao foi renderizada pelo textos do sandbox: %s" % (_pl.stdout + _pl.stderr)[-300:])
        _liga(os.path.join(NOSS, "um.py"), os.path.join(_nos_c, "um.py")); shutil.copyfile(os.path.join(NOSS, "um_absoluto.json"), os.path.join(_nos_c, "um_absoluto.json")); shutil.copyfile(os.path.join(NOSS, "um_absoluto_selo.json"), os.path.join(_nos_c, "um_absoluto_selo.json"))
        shutil.copyfile(os.path.join(NOSS, "HANDOFF_v411_CUSTODIA.md"), os.path.join(_nos_c, "HANDOFF_v411_CUSTODIA.md")); shutil.copyfile(P_ESP, os.path.join(_pkg_c, "ESPERADOS_v411.json"))
        _h_antes = open(os.path.join(_nos_c, "HANDOFF_v411_CUSTODIA.md"), "rb").read()
        _spt = importlib.util.spec_from_file_location("textos_custodia_handoff_v411_h", os.path.join(HERE, "textos_custodia_handoff_v411.py")); _TC = importlib.util.module_from_spec(_spt); _spt.loader.exec_module(_TC)
        _rc = _TC.main(_nos_c, _pkg_c, _rec_c)
        _rp = os.path.join(_rec_c, _TC.NOME_RECIBO); _rec = rdj(_rp) if os.path.exists(_rp) else {}
        _h_depois = open(os.path.join(_nos_c, "HANDOFF_v411_CUSTODIA.md"), "rb").read(); _gv = _rec.get("guardas") or {}
        _GC.update(s6d_rc=_rc, s6d_recibo=bool(_rec), s6d_marcadores=len(_rec.get("marcadores") or []), s6d_handoff_cresceu_bytes=len(_h_depois) - len(_h_antes), s6d_parser_g1_problemas=(_rec.get("parser_g1") or {}).get("problemas"),
                   s6d_guardas_sujas=sorted(k_ for k_, g_ in _gv.items() if any(g_.get(c_) for c_ in ("guarda_frases_v411", "portao_g1", "forma", "custodia_h0dn"))), s6d_pasta=_gd)
        _s6d_ok = bool(_rc == 0 and _rec and _GC["s6d_marcadores"] >= 7 and _GC["s6d_handoff_cresceu_bytes"] > 3000 and not _GC["s6d_parser_g1_problemas"] and not _GC["s6d_guardas_sujas"])
        _env = dict(os.environ, PYTHONIOENCODING="utf-8")
        _r1 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_textos_custodia_sem_candidato_v411.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_textos_custodia_out.txt"), "w", encoding="utf-8").write((_r1.stdout or "") + "\n--- stderr ---\n" + (_r1.stderr or ""))
        _r2 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_gatilho_custodia_sem_candidato_v411.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_gatilho_custodia_out.txt"), "w", encoding="utf-8").write((_r2.stdout or "") + "\n--- stderr ---\n" + (_r2.stderr or ""))
        _pt = os.path.join(DLX.ENSAIO_DIR, "pos_rito_textos", "TESTE_TEXTOS_CUSTODIA_SEM_CANDIDATO_v411.json"); _pg = os.path.join(DLX.ENSAIO_DIR, "pos_rito_gatilho", "TESTE_GATILHO_CUSTODIA_v411.json")   # (os dois testes gravam, cada um, no sandbox proprio sob C:\t\k411c\ensaio_topo_proposto: caminho fixo nos testes)
        _jt = rdj(_pt) if os.path.exists(_pt) else {}; _rj = rdj(_pg) if os.path.exists(_pg) else {}; _cs = _rj.get("casos") or {}
        _GC.update(textos_rc=_r1.returncode, textos_tudo_passou=_jt.get("TUDO_PASSOU"), textos_n_ok=_jt.get("ok"), textos_falhas=[f_.get("caso") for f_ in (_jt.get("falhas") or [])][:6], gatilho_rc=_r2.returncode, gatilho_tudo_passou=_rj.get("tudo_passou"), gatilho_casos=_rj.get("n_casos"), gatilho_negativos=_rj.get("n_negativos"),
                   gatilho_reprovados=sorted(k_ for k_, v_ in _cs.items() if not (v_ or {}).get("ok")), gatilho_seguranca=_rj.get("seguranca_gatilho_real_intocado"), gatilho_de_verdade_existe=os.path.exists(os.path.join(PKG, "ORDEM_HANDOFF_CUSTODIA_v411.md")))
        _GC["ok"] = bool(_s6d_ok and _r1.returncode == 0 and _jt.get("TUDO_PASSOU") is True and (_jt.get("ok") or 0) >= 10 and _r2.returncode == 0 and _rj.get("tudo_passou") is True and (_rj.get("n_negativos") or 0) >= 15 and not _GC["gatilho_reprovados"] and _GC["gatilho_seguranca"] is True)
        if not _GC["ok"]:
            falha("a custodia (S6d de verdade sobre o handoff do fechar e os dois testes sinteticos): s6d rc %s (marcadores %s, cresceu %s B, guardas sujas %s, parser %s); textos rc %s (passou %s); gatilho rc %s (passou %s, reprovados %s); ver %s | %s" % (
                _rc, _GC["s6d_marcadores"], _GC["s6d_handoff_cresceu_bytes"], _GC["s6d_guardas_sujas"][:3], _GC["s6d_parser_g1_problemas"], _r1.returncode, _jt.get("TUDO_PASSOU"), _r2.returncode, _rj.get("tudo_passou"), _GC["gatilho_reprovados"][:3], _gd, ((_r1.stdout or "") + (_r2.stdout or ""))[-300:].replace(chr(10), " | ")))
    except BaseException as ex:  # noqa: BLE001
        import traceback
        _GC["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:300]); _GC["onde"] = traceback.format_exc().strip().splitlines()[-3:]; falha("a custodia (S6d de verdade e os testes sinteticos): %s" % _GC["erro"])
    R["etapas"]["custodia_s6d_e_gatilho"] = _GC
    print("  a custodia: o S6d (main) de verdade sobre o handoff do fechar (rc %s; %s marcadores) e os dois testes sinteticos (textos %s; gatilho %s casos, %s negativos): %s" % (_GC.get("s6d_rc"), _GC.get("s6d_marcadores"), _GC.get("textos_tudo_passou"), _GC.get("gatilho_casos"), _GC.get("gatilho_negativos"), "ok" if _GC["ok"] else "FALHOU"))


_etapa_custodia()
STUB_L = ("# -*- coding: utf-8 -*-\n# STUB do harness (NAO e' a leitura da cadeia): monta a V minima que o fechar_v411.py usa, de ESPERADOS, do APLICADO_AO_CANONICO e do Nos do sandbox.\nimport glob, hashlib, json, os, sys\nNOS = @@NOS@@\nPK = @@PK@@\nsys.path.insert(0, PK)\nimport delta_v411 as _DL\n"
          "REG_FUNCAO = list(_DL.REGISTROS_FUNCAO)   # (o fechar_v411.py confere L.REG_FUNCAO == delta_v411.REGISTROS_FUNCAO)\nREG_RECRIADOS_V410F = tuple(_DL.REGISTROS_FUNCAO_V410)\nREG_RECRIADOS_V410S = ('cunhagens_v410', 'kh_n1_cobertura_v410')\nREG_RECRIADOS_V410 = REG_RECRIADOS_V410F + REG_RECRIADOS_V410S\n\n\n"
          "def _aplicado():\n    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))\n    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]\n\n\n"
          "def ler():\n    ap, app = _aplicado(); esp = json.load(open(os.path.join(PK, 'ESPERADOS_v411.json'), encoding='utf-8'))\n    um = os.path.join(NOS, 'um.py'); sc = json.load(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), encoding='utf-8'))\n    ok = lambda: {'ok': True, 'sealed': True}\n"
          "    V = {'nos': NOS, 's16': esp['candidato_sha16'], 'umb': os.path.getsize(um), 'base16': ap['backups']['um.py']['sha16'], 'base_backup': ap['backups']['um.py']['backup'], 'escada_antes': esp['escada_v410_e_v411'][0], 'escada_depois': esp['escada'][1], 'teor': '%d/%d' % (esp['escada'][1], esp['escada'][1]),\n"
          "         'axiom_report_n': esp.get('axiom_report_esperado_min', 0), 'patches': 'stub', 'compl': 'COMPLETA', 'horarios': [], 'qg': esp['qg_closure_verdict'], 'conf_dm': '0/0', 'conf_np': '0/0', 'conf16': 'stub', 'servidor': 'stub',\n"
          "         'reg411': {n_: {'ok': True} for n_ in REG_FUNCAO + ['cunhagens_v411', 'kh_n1_cobertura_v411']}, 'reg410_recriados': {n_: {'ok': True, 'sealed': True} for n_ in REG_RECRIADOS_V410}, 'reg410t': {}, 'reg408d': {}, 'reg407d': {}, 'reg406d': {}, 'reg410c': {}, 'reg410b': {}, 'reg410_estado': {}, 'reg402_estado': {}, 'reg401_estado': {}, 'reg399': {},\n"
          "         'fecho': {'ok': True, 'sealed': True, 'opened_once': True, 'observed_vector_read': True}, 'fecho410': {'ok': True}, 'fecho408': {'ok': True}, 'fecho407': {'ok': True}, 'fecho406': {'ok': True}, 'n_pedras': 0, 'pedras': [], 'bundle410': ok(), 'bundle409': ok(), 'bundle408': ok(), 'bundle407': ok(), 'bundle406': ok(),\n"
          "         'ancoras': {}, 'ancoras410': {}, 'ancoras409': {}, 'ancoras408': {}, 'ancoras407': {}, 'ancoras406': {}, 'bandeiras': {}, 'bandeiras410': {}, 'chaves407': {}, 'chaves406': {}, 'f2b': {'ok': True}, 'gate': {'ok': True}, 'fun410': {}, 'fun410b': {}, 'fun410c': {}, 'fun402': {}, 'pedras_v408': {}, 'fal401': {'ok': True},\n"
          "         'troca_dita': list(esp['troca_dita']), 'varr': {}, 'verbatins': {}, 'fd390': 'stub', 'pilar': {}, 'artigos': {}}\n"
          "    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):\n        V['h_' + k] = hashlib.sha256(open(os.path.join(NOS, k), 'rb').read()).hexdigest()[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'\n"
          "    V['sidecar'] = {'ok': True, 'sha256': hashlib.sha256(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), 'rb').read()).hexdigest(), 'bytes': os.path.getsize(os.path.join(NOS, 'um_absoluto_selo_acom.json')), 'veredito': sc.get('veredito'), 'esquema': sc.get('esquema'), 'recusas': 0,\n"
          "                    'objetos': {o['nome']: {'bytes': o.get('bytes'), 'sha256': o.get('sha256')} for o in sc.get('objetos', [])}}\n    return V, []\n")
STUB_T = ("# -*- coding: utf-8 -*-\n# STUB do harness (NAO sao os textos da cadeia): paragrafos e handoff minimos, limpos da guarda P18 e da guarda das frases; o handoff diz o que o fechar exige (o registro novo, os da v410 recriados, as sete ressalvas por rotulo, o que o teste nao decide, RECRIADOS, nenhum modulo novo).\n"
          "import json, os, sys\nNOS = @@NOS@@\nPK = @@PK@@\nTOPICO_NOVO = 'v411-selada-h0dn-aberto.md'\n\n\ndef paragrafo_readme():\n    return 'PARAGRAFO DO QUADRO (stub do harness)\\n', {'stub': True}\n\n\ndef paragrafo_v411():\n    return 'PARAGRAFO DA V411 (stub do harness)\\n', {'stub': True}\n\n\n"
          "def handoff(V, k):\n    sys.path.insert(0, PK)\n    import delta_v411 as D\n    hc = json.load(open(os.path.join(NOS, 'um_absoluto.json'), encoding='utf-8'))['core'][D.FECHO_REGISTRO]\n"
          "    nomes = ' '.join([D.FECHO_REGISTRO, D.CUNHAGENS_REGISTRO, D.KH_REGISTRO, 'cunhagens_v410', 'kh_n1_cobertura_v410'] + list(D.REGISTROS_FUNCAO_V410))\n"
          "    obrig = '%s; as %s leem 4,38σ; %s; %s; %s.' % (D.OBRIG_MODELO_PT, D.OBRIG_CEFEIDAS_PT, D.OBRIG_RETRO_PT, D.OBRIG_NAO_CEGO_PT, D.OBRIG_VALIDADE_PT)\n"
          "    return ('---\\nname: handoff-v411-custodia\\ndescription: \"handoff de ensaio (stub do harness)\"\\nmetadata:\\n  type: project\\n---\\n\\n# HANDOFF v411 (stub do harness)\\n\\n' + nomes + ' RECRIADOS; nenhum módulo novo.\\n\\n' + '; '.join(D.RESSALVAS_ROTULOS_PT) + '\\n\\n'\n"
          "            + '; '.join(str(x_) for x_ in hc['o_que_o_teste_nao_decide']) + ' ' + obrig + '\\n\\n%s %s %s\\n' % (V['s16'], k['ap_nome'], k['ap_ver']))\n")
# ---- 2d. o PROPRIO fechar_v411.py (copia de bytes) com leitura e textos STUB: prova o CODIGO do fechar (manifesto com o estado da fila, o arquivo, os diffs vazios de modulos, o handoff, a copia do sidecar e do selo) mesmo que textos_v411/leitura_v411 tenham problema
def _etapa_2d():
    SBS = os.path.join(PKS, "pos_rito_stub"); os.makedirs(SBS, exist_ok=True); UMS2 = os.path.join(SB, "memory_stub"); mk_memoria_copia(UMS2)
    shutil.copyfile(os.path.join(HERE, "fechar_v411.py"), os.path.join(SBS, "fechar_v411.py"))
    open(os.path.join(SBS, "leitura_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_L.replace("@@NOS@@", repr(NOSS)).replace("@@PK@@", repr(PKS)))
    open(os.path.join(SBS, "textos_v411.py"), "w", encoding="utf-8", newline="\n").write(STUB_T.replace("@@NOS@@", repr(NOSS)).replace("@@PK@@", repr(PKS)))
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(SBS, "fechar_v411.py")], cwd=SBS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env_sb(V411_MEMORIA_DIR=UMS2))
    open(os.path.join(SB, "fechar_stub_out.txt"), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    ho_ = os.path.join(UMS2, "handoff-v411-custodia.md"); mf = os.path.join(SBS, "v411_incorporacao_manifesto.json")
    man_ = rdj(mf) if os.path.exists(mf) else {}; fi_ = man_.get("fila_da_memoria") or {}
    dk_ = open(os.path.join(PKS, "DIFF_KERNEL_v411.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(PKS, "DIFF_KERNEL_v411.txt")) else ""
    rcv, jv, sov, sev = memoria(UMS2, "verificar")
    r_ = {"rc": p.returncode, "ultima_linha": (p.stdout.strip().splitlines() or [""])[-1][:200], "handoff_escrito": os.path.exists(ho_), "manifesto_chaves": sorted(man_.keys())[:80], "fila_no_manifesto": fi_, "diff_kernel_diz_zero_modulos_novos": ("novos (0)" in dk_ and "removidos (0)" in dk_), "verificar_depois_do_handoff": {"rc": rcv, "ok": (jv or {}).get("ok")}}
    R["etapas"]["fechar_com_stubs"] = r_
    ok_ = (p.returncode == 0 and "FECHADO v411:" in p.stdout and r_["handoff_escrito"] and r_["diff_kernel_diz_zero_modulos_novos"] and fi_.get("memoria_py_igual_ao_pino_v411") is True and fi_.get("pausa_do_vigia_ausente") is True and fi_.get("pino_confere_com_o_indice") is True
           and all(k_ in man_ for k_ in MAN_CHAVES) and rcv == 0 and (jv or {}).get("ok") is True)
    print("  fechar_v411.py (copia de bytes) com leitura e textos STUB: rc %s; handoff %s; manifesto com a fila %s; o diff do kernel diz zero modulos novos %s; verificar da fila depois do handoff rc %s -> %s" % (p.returncode, r_["handoff_escrito"], bool(fi_), r_["diff_kernel_diz_zero_modulos_novos"], rcv, "ok" if ok_ else "FALHOU"))
    if not ok_:
        falha("fechar_v411.py com stubs: rc %s; %s | %s" % (p.returncode, (p.stdout + p.stderr)[-500:].replace(chr(10), " | "), {k_: r_[k_] for k_ in ("handoff_escrito", "diff_kernel_diz_zero_modulos_novos", "verificar_depois_do_handoff")}))


try:
    _etapa_2d()
except Exception as _e2d:   # noqa: BLE001
    import traceback
    falha("_etapa_2d levantou %r: %s" % (_e2d, traceback.format_exc()[-300:].replace(chr(10), " | ")))
# ---- 3. o registrar_mapa (main)
rc, so, se = roda("registrar_mapa_v411.py", "registrar_mapa")
pj = os.path.join(POS, "registro_mapa_v411.json"); reg = rdj(pj) if os.path.exists(pj) else []
ok_m = (rc == 0 and len(reg) >= 1 and "registro MONTADO (NAO registrado)" in so and "COMANDO (o passo 12 da cadeia" in so)
R["etapas"]["registrar_mapa"] = {"rc": rc, "ok": ok_m, "n_registros": len(reg), "rotas": [x.get("rota_id") for x in reg], "comando": [l for l in so.splitlines() if l.startswith("COMANDO")][:1], "artefatos_da_rota": [os.path.basename(a) for a in (reg[0].get("artefatos") or [])] if reg else []}
print("  registrar_mapa (main) em sandbox: rc %s; %d registro(s); %s" % (rc, len(reg), "ok" if ok_m else "FALHOU"))
if not ok_m:
    falha("registrar_mapa_v411.py (main, sandbox) falhou: rc %s: %s" % (rc, (so + se)[-410:]))
# ---- 4. as copias dos scripts diferem dos originais so' nas linhas de caminho
R["etapas"]["copias_dos_scripts"] = {n: [l[:140] for l in v] for n, v in DIF.items()}
if any(len(v) != 1 for n, v in DIF.items() if n in ("leitura_v411.py", "textos_v411.py")) or DIF["registrar_mapa_v411.py"] or DIF["fechar_v411.py"]:
    falha("as copias dos scripts diferem dos originais em mais que a linha de caminho do Nos (fechar e registrar_mapa: nenhuma): %s" % {n: len(v) for n, v in DIF.items()})
# ---- limpeza
LIMP = None
if not MANTER:
    LIMP = sum(os.path.getsize(os.path.join(r_, f_)) for r_, d_, fs_ in os.walk(SB) for f_ in fs_)
    keep = os.path.join(OUT, "fechar_sandbox_resultado"); shutil.rmtree(keep, ignore_errors=True); os.makedirs(keep)
    for nome in sorted(f_ for f_ in os.listdir(SB) if f_.endswith("_out.txt") or (f_.startswith("b3_") and f_.endswith((".txt", ".json")))):   # v411 (fork B): TODAS as saidas dos controles e do b3 (a lista fixa do molde deixava de fora os controles novos)
        if os.path.exists(os.path.join(SB, nome)):
            shutil.copyfile(os.path.join(SB, nome), os.path.join(keep, nome))
    for src, dst in ((os.path.join(UMS, "handoff-v411-custodia.md"), "handoff-v411-custodia.md"), (os.path.join(POS, "registro_mapa_v411.json"), "registro_mapa_v411_SANDBOX.json"), (os.path.join(POS, "v411_incorporacao_manifesto.json"), "v411_incorporacao_manifesto_SANDBOX.json"),
                     (os.path.join(PKS, "DIFF_KERNEL_v411.txt"), "DIFF_KERNEL_v411_SANDBOX.txt")):
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(keep, dst))
    shutil.rmtree(SB, ignore_errors=True)
R["etapas"]["limpeza"] = {"sandbox_removido_bytes": LIMP, "guardado_em": os.path.join(OUT, "fechar_sandbox_resultado") if not MANTER else SB}
finalizar(ANTES_REAL, None)
R["veredito"] = ("TUDO PASSOU: a FILA DA MEMORIA funciona em copia (pausa antes da escrita do indice, pinar rc 0, a pausa so' sai depois do pino, verificar rc 0; as superficies recusam sem pausa e acima do limite; o chain para sem remover a pausa quando falha antes do pino; o diretorio real ficou inalterado)" + ("; o PINO do memoria.py foi EMULADO (pino_memoria_py_v411.py ainda nao foi rodado pela gerencia)" if PINO_EMULADO else "") + "; "
                 "o b3_recibo confere o passo simples B19 -> B20; o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da v411 (o teste decisivo, H0DN x BG1 aberto uma vez) pela verificacao propria; sem nota ao lado do paragrafo da v410; diz que os anteriores seguem como estao; diz o registro h0dn_bg1_v411 com as quatro obrigacoes do primario (F67), as sete ressalvas por rotulo, "
                 "os recriados da v410, RECRIADOS e «nenhum módulo novo», sem a frase velha da v410 e sem token proibido; e lista o sidecar), os dois diffs (o do kernel diz zero modulos novos), o manifesto (com o estado da fila e o resumo do h0dn_bg1_v411) e o arquivo, copia o sidecar e o selo para v411_selo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado, com o numero lido adulterado, "
                 "com o h0dn_bg1_v411 ausente, nao selado, nao aberto, com vetor observado nao lido, checagem falha, valores adulterados nas duas linhas, ramo trocado, beta errado, veredito trocado, token proibido, a frase velha da v410, a F67 sem a linha das Cefeidas livres, sem o resumo no selo ou o bloco do stdout, com cunhagens_v411 ou kh_n1_cobertura_v411 adulterados, "
                 "com um registro da v410 recriado ausente ou nao selado, com bandeira ou modulo novo, com a escada diferente, com um registro herdado (traducao_turing_v409, tetelestai_terminal_v408, psion_canto_v407, fechamento_v406) ou recriado adulterado, com o gate movido, com a direcao do testemunho invertida, com uma ancora fora do trio, com o handoff que traga a frase velha, token proibido, a palavra da prova emendada, 5 sigma atingido, teste cego ou sem as obrigacoes do primario, "
                 "e com o sidecar adulterado ou ausente; o S6d (textos_custodia_handoff_v411.main) roda DE VERDADE sobre o handoff que o fechar gravou e os dois testes sinteticos da custodia passam; o registrar_mapa monta o registro" if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
if SEM_FILA:
    R["veredito"] += " [MODO --sem-fila: o ensaio da fila da memoria NAO rodou]"
R["nota"] = "recibos do B(n) SINTETICOS; o Nos, a memoria e a arvore da cadeia do SANDBOX sao emulados (o sidecar e a linha do sidecar do stdout vem da funcao do proprio artefato); a prova e' do codigo do fechar, do b3_recibo, do registrar_mapa, do S6d e da fila da memoria, nao de um B(n) real" + ("" if not NAO_REFAZER else " [MODO --nao-exigir-refazer: refazer_out_v411.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]") + ("" if not ENSAIO else " [ENSAIO DO TOPO PROPOSTO: o artefato NAO e' candidato; nada aqui prova o rito real]")
R["nao_exigiu_refazer"] = NAO_REFAZER; R["origem_das_entradas"] = dict(ORIGEM); R["nos_emulado_fonte"] = _FONTE_NOS
if PINO_EMULADO:
    R["veredito"] += " [PINO EMULADO: PINO_MEMORIA_PY_v411.json nao existia na raiz do pacote; a fila e o chain rodaram com um pino calculado na hora do memoria.py real (so' leitura)]"
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v411.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
os.makedirs(POS_SAIDA, exist_ok=True)
saida = os.path.join(POS_SAIDA, "HARNESS_FECHAR_SANDBOX_v411" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))   # o nome sem sufixo so' nasce da rodada que EXIGE o refazer (ou do ensaio, que tem o PRONTO)
print("VEREDITO (fechar em sandbox):", R["veredito"]); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)

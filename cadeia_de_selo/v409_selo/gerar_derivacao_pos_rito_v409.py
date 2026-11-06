# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409 (fork A), a servico da gerencia c1] sobre a subida mecanica de rotulo da v408 FINAL (_bump_copia_v409.py): a SUITE descreve a v409 (A TRADUCAO AS CLASSES DE TURING; os papeis, as datas e os autores de 05/11: fork A = o pos_rito inteiro e o orquestrador; os do lote 04/11 do fork B ficam como registro nas notas dos arquivos); o montador, a semente e o fragmento SAO usados na v409 (deixam de ser opcionais). SO' LE; a gerencia revisa antes do rito (nao e' versao selada).
"""gerar_derivacao_pos_rito_v409.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v409.
Na v409 a suite do pos_rito e' a SEMENTE mecanica de derivar_encanamento_v409.py (lote F) sobre o arquivo FINAL da cadeia v408 (o que foi USADO no pos-rito real da v408): o numero de versao subido por script (401 -> 408 e 408 -> 409, com a protecao dos nomes nascidos no um.py), mais as regras do lote F (os rotulos B(n), a lista de registros do chain,
o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V409 nos arquivos de narrativa). A ADAPTACAO (o que o pos-rito diz da v409: a traducao as classes de Turing, relativa ao leitor, com os numeros lidos do rito) foi feita em 05/11/2026 pela claude-construtor-v409 (fork A), pelos _adapt_*_v409.py desta pasta (trocas de contagem exata com backup de bytes), pelo montador (textos_v409.semente + textos_v409_novo.pysnip -> textos_v409.py) e por reescrita onde o corpo era o da v408 (registrar_mapa_v409.py, gerar_x_custodia_v409.py, textos_custodia_handoff_v409.py); a marca TEXTO_A_REESCREVER_V409 nao pode sobrar em nenhum arquivo (o p00 confere).
Este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v409_motor.bump), a semente PURA de cada arquivo (so' o mapa de versoes) e a compara com o arquivo atual.
Para cada arquivo do pos_rito que tem origem na v408 grava o sha256 da origem, o da semente pura (recalculada agora), o do arquivo atual, o estado (SEMENTE_PURA | DIFERE_DA_SEMENTE_PURA: regras do lote F ou edicao a mao) e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais.
Escreve so' pos_rito/DERIVACAO_v409.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse. Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v409.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
import ast, difflib, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_v409_motor as M  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()
V408_POS = os.path.join(os.path.dirname(PK), "v408", "pos_rito")
# a suite do pos_rito: (nome na v409, nome da origem na v408, papel). Os tres primeiros blocos sao os da tarefa A1 (encanamento do pos-rito, fila da memoria); os demais sao de outros agentes e entram so' para o registro.
SUITE = (
    ("chain_pos_rito_v409.sh", "chain_pos_rito_v408.sh", "fork A, 05/11: a cadeia (passos 0..14) com o passo da fila da memoria; REGS da v409 (traducao_turing_v409, cunhagens_v409, kh_n1_cobertura_v409), o rotulo B18, o sufixo _v409 dos backups do inventario"),
    ("superficies_v409.py", "superficies_v408.py", "fork A, 05/11: as superficies (diretorio de memoria por V409_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B); so' as notas mudaram (os blocos vem do textos_v409.py)"),
    ("fechar_v409.py", "fechar_v408.py", "fork A, 05/11: o fechar (manifesto com registros_v409/v408/v407/v406 e registros_funcao_v409 (traducao)/v408 (tetelestai)/v407 (psion)/v406, arquivo, diffs, handoff)"),
    ("b3_recibo_v409.py", "b3_recibo_v408.py", "fork A, 05/11: o recibo do B(n), passo SIMPLES B17 -> B18; so' as notas mudaram"),
    ("gerar_derivacao_pos_rito_v409.py", "gerar_derivacao_pos_rito_v408.py", "fork A, 05/11: este registro (so' le)"),
    ("harness_fechar_sandbox_v409.py", "harness_fechar_sandbox_v408.py", "fork A, 05/11: o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA e os controles negativos da v409 (a traducao; o tetelestai, o psion e o fechamento herdados; E26; D59)"),
    ("fila_memoria_v409.py", "fila_memoria_v408.py", "fork A, 05/11: as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness; so' as notas mudaram"),
    ("leitura_v409.py", "leitura_v408.py", "fork A, 05/11: a leitura da rodada adaptada a traducao as classes de Turing (o modulo TraducaoTuring, as ancoras lidas de delta_v409, nenhuma chave antiga muda; o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados e os registros anteriores recriados)"),
    ("textos_v409.py", "textos_v408.py", "fork A, 05/11: os textos da v409, MONTADOS (montar_textos_v409.py: semente + fragmento): o paragrafo novo, a nota ao lado do paragrafo da v408 com a E26, o handoff, as superficies, o topico novo"),
    ("harness_textos_ensaio_v409.py", "harness_textos_ensaio_v408.py", "fork A, 05/11: o harness do pos-rito adaptado a traducao (controles negativos dos registros novos e dos herdados, D59)"),
    ("registrar_mapa_v409.py", "registrar_mapa_v408.py", "fork A, 05/11: REESCRITO para a v409: a rota nova (o id esta em registrar_mapa_v409.NOVA), as anotacoes nas rotas de 05/11 e as erratas E24 a E26 ao lado"),
    ("textos_custodia_handoff_v409.py", "textos_custodia_handoff_v408.py", "fork A, 05/11: REESCRITO para a v409: os sete textos da custodia (roda ENCADEADO no fim do S6, pelo orquestrador; a chain nao o chama)"),
    ("gerar_x_custodia_v409.py", "gerar_x_custodia_v408.py", "fork A, 05/11: REESCRITO para a v409: o rascunho do post longo do X (numeros do selo e do core; a ordem e as cunhagens por delta_v409.FRASE_*; sem o 4,44; D59)"),
    ("montar_textos_v409.py", "montar_textos_v408.py", "fork A, 05/11: o montador (semente + fragmento -> textos_v409.py); DELETAR ganha _d51"),
    ("textos_v409_novo.pysnip", "textos_v408_novo.pysnip", "fork A, 05/11: o fragmento da v409 (as definicoes da traducao; __HEADER__)"),
    ("textos_v409.semente", "textos_v408.py", "fork A, 05/11: a semente = textos_v408.py FINAL (montado) com os rotulos subidos, a marca trocada e o fim de linha normalizado para LF"),
    ("adaptar_pos_rito_v409.py", None, "OPCIONAL: o adaptador comum da v408; na v409 cada _adapt_*_v409.py e' autonomo"),
)
OPCIONAIS = {"adaptar_pos_rito_v409.py"}
SUITE = SUITE + tuple((f_, None, "claude-construtor-v409, 04-05/11: adaptador (trocas de contagem exata com asserts e backup de bytes)") for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v409.py"))
rel = []; ruim = []
for nome, origem, papel in SUITE:
    p = os.path.join(HERE, nome)
    if not os.path.isfile(p):
        if nome in OPCIONAIS:
            rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE_OPCIONAL (nao faz parte da v409; listado so' porque o molde v408 o tinha)"}); continue
        rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE"}); ruim.append(nome); continue
    atual = open(p, "rb").read()
    r = {"arquivo": nome, "papel": papel, "bytes": len(atual), "sha256": sha(atual)}
    if nome.endswith(".py"):
        try:
            ast.parse(atual.decode("utf-8"))
            r["ast_parse"] = True
        except SyntaxError as e:
            r["ast_parse"] = False; r["erro"] = repr(e)[:200]; ruim.append(nome)
    if origem is None:
        r["estado"] = "ESCRITO_DE_NOVO_SEM_ORIGEM"
    else:
        po = os.path.join(V408_POS, origem)
        if not os.path.isfile(po):
            r["estado"] = "ORIGEM_V408_AUSENTE"; ruim.append(nome)
        else:
            raw = open(po, "rb").read()
            semente = M.bump(raw.decode("utf-8"), (), "v408").encode("utf-8")
            r["origem_v408"] = {"path": po, "sha256": sha(raw)}
            r["semente_mecanica_sha256"] = sha(semente)
            if semente == atual:
                r["estado"] = "SEMENTE_PURA"
            else:
                r["estado"] = "DIFERE_DA_SEMENTE_PURA__regras_do_lote_F_ou_edicao_a_mao"
                a_, b_ = semente.decode("utf-8").splitlines(), atual.decode("utf-8").splitlines()
                sm = difflib.SequenceMatcher(None, a_, b_, autojunk=False)
                r["diff_contra_a_semente"] = {"linhas_da_semente": len(a_), "linhas_do_arquivo": len(b_), "linhas_trocadas_ou_novas": sum((j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")}
    rel.append(r)
    print("%-38s %-34s %s" % (nome, r["estado"], r["sha256"][:12]))
out = {"contrato": "DERIVACAO_POS_RITO_v409", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False,
       "origem": "pos_rito da v408 FINAL (a cadeia usada no pos-rito real da v408), rotulos 408 -> 409 por script (_bump_copia_v409.py, semente pura); a adaptacao foi feita pela claude-construtor-v409 (fork A) em 05/11/2026 pelos _adapt_*_v409.py desta pasta, pelo montador dos textos e por reescrita onde o corpo era o da v408 (registrar_mapa, gerar_x_custodia, textos_custodia_handoff); a marca TEXTO_A_REESCREVER_V409 nao pode sobrar em nenhum arquivo (o p00 confere)",
       "arquivos": rel, "nota": "so' le: nenhum script foi executado nem sobrescrito; a semente de cada arquivo e' RECALCULADA em memoria pelo motor a cada vez (hash nunca digitado)"}
dst = os.path.join(HERE, "DERIVACAO_v409.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v409.json gravado (%d arquivos registrados; problemas: %s)" % (len(rel), ruim or "nenhum"))
sys.exit(1 if ruim else 0)

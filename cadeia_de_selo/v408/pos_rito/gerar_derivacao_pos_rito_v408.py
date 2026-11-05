# -*- coding: utf-8 -*-
# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork B)] sobre a subida mecanica de rotulo da v407 FINAL (_bump_copia_v408.py): a SUITE descreve a v408 (TETELESTAI E' O TERMINAL; os papeis, as datas e os autores de 04/11: fork A = textos/leitura/harness dos textos; fork B = fechar, superficies, registrar_mapa, chain, harness do fechar, textos da custodia, post do X, este registro); os arquivos do montador da v407 que a v408 nao tem sao OPCIONAIS (listados como ausentes, sem reprovar). SO' LE; a gerencia revisa antes do rito (nao e' versao selada).
"""gerar_derivacao_pos_rito_v408.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v408.
Na v408 a suite do pos_rito e' a SEMENTE mecanica de derivar_encanamento_v408.py (lote F) sobre o arquivo FINAL da cadeia v407 (o que foi USADO no pos-rito real da v407): o numero de versao subido por script (401 -> 407 e 407 -> 408, com a protecao dos nomes nascidos no um.py), mais as regras do lote F (os rotulos B(n), a lista de registros do chain,
o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V408 nos arquivos de narrativa). A ADAPTACAO (o que o pos-rito diz da v408: Tetelestai e' o terminal, com os numeros lidos do rito) foi feita em 04/11/2026 pela claude-construtor-v408 em tres forks, pelos _adapt_*_v408.py desta pasta (trocas de contagem exata com backup de bytes) e por reescrita integral onde o corpo era o da v407 (registrar_mapa_v408.py, gerar_x_custodia_v408.py, textos_custodia_handoff_v408.py, este com o nome de D52); textos_v408.py, leitura_v408.py e o harness dos textos sao do fork A; a marca TEXTO_A_REESCREVER_V408 nao pode sobrar em nenhum arquivo (o p00 confere).
Este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v408_motor.bump), a semente PURA de cada arquivo (so' o mapa de versoes) e a compara com o arquivo atual.
Para cada arquivo do pos_rito que tem origem na v407 grava o sha256 da origem, o da semente pura (recalculada agora), o do arquivo atual, o estado (SEMENTE_PURA | DIFERE_DA_SEMENTE_PURA: regras do lote F ou edicao a mao) e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais.
Escreve so' pos_rito/DERIVACAO_v408.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse. Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v408.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
import ast, difflib, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_v408_motor as M  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()
V407_POS = os.path.join(os.path.dirname(PK), "v407", "pos_rito")
# a suite do pos_rito: (nome na v408, nome da origem na v407, papel). Os tres primeiros blocos sao os da tarefa A1 (encanamento do pos-rito, fila da memoria); os demais sao de outros agentes e entram so' para o registro.
SUITE = (
    ("chain_pos_rito_v408.sh", "chain_pos_rito_v407.sh", "A1 (fork B, 04/11): a cadeia (passos 0..14) com o passo da fila da memoria; REGS da v408 (tetelestai_terminal_v408, cunhagens_v408, kh_n1_cobertura_v408), o rotulo B17, o sufixo _v408 dos backups do Atlas"),
    ("superficies_v408.py", "superficies_v407.py", "A1 (fork B, 04/11): as superficies (diretorio de memoria por V408_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B); so' as notas mudaram"),
    ("fechar_v408.py", "fechar_v407.py", "A1 (fork B, 04/11): o fechar (manifesto com registros_v408/v407/v406 e registros_funcao_v408/v407/v406, arquivo, diffs, handoff)"),
    ("b3_recibo_v408.py", "b3_recibo_v407.py", "A1 (fork B, 04/11): o recibo do B(n), passo SIMPLES B16 -> B17; so' as notas mudaram"),
    ("gerar_derivacao_pos_rito_v408.py", "gerar_derivacao_pos_rito_v407.py", "A1 (fork B, 04/11): este registro (so' le)"),
    ("harness_fechar_sandbox_v408.py", "harness_fechar_sandbox_v407.py", "A1 (fork B, 04/11): o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA, os controles negativos da v408 (terminal, psion e fechamento herdados, E21, D54, leitura ONTO, ancoras principais) e o espelho da casa medido na importacao do delta"),
    ("fila_memoria_v408.py", "fila_memoria_v407.py", "A1 (fork B, 04/11): as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness; so' as notas mudaram"),
    ("leitura_v408.py", "leitura_v407.py", "claude-construtor-v408 (fork A), 04/11: a leitura da rodada adaptada a Tetelestai e' o terminal (o bundle dos quatro modulos, as ancoras lidas de delta_v408, nenhuma chave antiga muda; o psion_canto_v407 e o fechamento_v406 herdados e os registros anteriores recriados)"),
    ("textos_v408.py", "textos_v407.py", "claude-construtor-v408 (fork A), 04/11: os textos da v408 (o paragrafo novo, a nota ao lado do paragrafo da v407 com a E21, o handoff, as superficies, o topico novo)"),
    ("harness_textos_ensaio_v408.py", "harness_textos_ensaio_v407.py", "claude-construtor-v408 (fork A), 04/11: o harness do pos-rito adaptado a Tetelestai e' o terminal (controles negativos dos registros novos e dos herdados)"),
    ("registrar_mapa_v408.py", "registrar_mapa_v407.py", "claude-construtor-v408 (fork B), 04/11: REESCRITO para a v408: a rota nova (o id esta em registrar_mapa_v408.NOVA), as anotacoes nas rotas de 04/11 e as erratas E21 a E23 ao lado"),
    ("textos_custodia_handoff_v408.py", "textos_custodia_handoff_v407_03nov.py", "claude-construtor-v408 (fork B), 04/11: REESCRITO para a v408: os sete textos da custodia (nome de D52; roda ENCADEADO no fim do S6, pelo orquestrador; a chain nao o chama)"),
    ("gerar_x_custodia_v408.py", "gerar_x_custodia_v407.py", "claude-construtor-v408 (fork B), 04/11: REESCRITO para a v408: o rascunho do post longo do X (numeros do selo e do core; a ordem e as cunhagens por delta_v408.FRASE_*; sem o 4,44)"),
    ("montar_textos_v408.py", "montar_textos_v407.py", "OPCIONAL: o montador da v407 (semente + fragmento); a v408 nao o usa se o fork A escreveu textos_v408.py por adaptador"),
    ("textos_v408_novo.pysnip", None, "OPCIONAL: o fragmento do montador (v407); a v408 nao o tem se o fork A nao o usou"),
    ("adaptar_pos_rito_v408.py", None, "OPCIONAL: o adaptador comum da v407; na v408 cada _adapt_*_v408.py e' autonomo"),
    ("textos_v408.semente", None, "OPCIONAL: a semente mecanica do montador (v407)"),
)
OPCIONAIS = {"montar_textos_v408.py", "textos_v408_novo.pysnip", "adaptar_pos_rito_v408.py", "textos_v408.semente"}
SUITE = SUITE + tuple((f_, None, "claude-construtor-v408, 04/11: adaptador do pos-rito (trocas de contagem exata com asserts e backup de bytes)") for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v408.py"))
rel = []; ruim = []
for nome, origem, papel in SUITE:
    p = os.path.join(HERE, nome)
    if not os.path.isfile(p):
        if nome in OPCIONAIS:
            rel.append({"arquivo": nome, "papel": papel, "estado": "AUSENTE_OPCIONAL (nao faz parte da v408; listado so' porque o molde v407 o tinha)"}); continue
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
        po = os.path.join(V407_POS, origem)
        if not os.path.isfile(po):
            r["estado"] = "ORIGEM_V407_AUSENTE"; ruim.append(nome)
        else:
            raw = open(po, "rb").read()
            semente = M.bump(raw.decode("utf-8"), (), "v407").encode("utf-8")
            r["origem_v407"] = {"path": po, "sha256": sha(raw)}
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
out = {"contrato": "DERIVACAO_POS_RITO_v408", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False,
       "origem": "pos_rito da v407 FINAL (a cadeia usada no pos-rito real da v407), rotulos 407 -> 408 por script (_bump_copia_v408.py, semente pura); a adaptacao foi feita pela claude-construtor-v408 em 04/11/2026 (forks A e B) pelos _adapt_*_v408.py desta pasta e por reescrita integral onde o corpo era o da v407 (registrar_mapa, gerar_x_custodia, textos_custodia_handoff); a marca TEXTO_A_REESCREVER_V408 nao pode sobrar em nenhum arquivo (o p00 confere)",
       "arquivos": rel, "nota": "so' le: nenhum script foi executado nem sobrescrito; a semente de cada arquivo e' RECALCULADA em memoria pelo motor a cada vez (hash nunca digitado)"}
dst = os.path.join(HERE, "DERIVACAO_v408.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v408.json gravado (%d arquivos registrados; problemas: %s)" % (len(rel), ruim or "nenhum"))
sys.exit(1 if ruim else 0)

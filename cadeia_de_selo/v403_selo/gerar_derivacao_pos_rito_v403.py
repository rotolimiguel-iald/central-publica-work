# -*- coding: utf-8 -*-
"""gerar_derivacao_pos_rito_v403.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v403.
Na v403 a suite do pos_rito e' a SEMENTE mecanica de derivar_encanamento_v403.py (lote F) sobre o arquivo FINAL da cadeia v402 (o que foi USADO no pos-rito real de 27/10/2026): o numero de versao subido por script (401 -> 402 e 402 -> 403, com a protecao dos nomes nascidos no um.py), mais as regras do lote F (os rotulos B(n), a lista de registros do chain,
o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V403 nos arquivos de narrativa). A ADAPTACAO A MAO (o que o pos-rito diz da v403: Caminho, Verdade e Vida e a F8.1, com os numeros lidos do rito) foi feita pela gerencia c1 em 28/10/2026: textos_v403.py sai do montador (montar_textos_v403.py) sobre textos_v403.semente (copia de bytes da semente mecanica) e textos_v403_novo.pysnip; leitura_v403.py, fechar_v403.py, registrar_mapa_v403.py, o harness e o cabecalho do chain foram reescritos e a marca TEXTO_A_REESCREVER_V403 saiu de cada arquivo depois de testado (o p00 confere).
Este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v403_motor.bump), a semente PURA de cada arquivo (so' o mapa de versoes) e a compara com o arquivo atual.
Para cada arquivo do pos_rito que tem origem na v402 grava o sha256 da origem, o da semente pura (recalculada agora), o do arquivo atual, o estado (SEMENTE_PURA | DIFERE_DA_SEMENTE_PURA: regras do lote F ou edicao a mao) e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais.
Escreve so' pos_rito/DERIVACAO_v403.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse. Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v403.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
import ast, difflib, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_v403_motor as M  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()
V402_POS = os.path.join(os.path.dirname(PK), "v402", "pos_rito")
# a suite do pos_rito: (nome na v403, nome da origem na v402, papel). Os tres primeiros blocos sao os da tarefa A1 (encanamento do pos-rito, fila da memoria); os demais sao de outros agentes e entram so' para o registro.
SUITE = (
    ("chain_pos_rito_v403.sh", "chain_pos_rito_v402.sh", "A1: a cadeia (passos 0..14) com o passo NOVO da fila da memoria"),
    ("superficies_v403.py", "superficies_v402.py", "A1: as superficies (diretorio de memoria por V403_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B)"),
    ("fechar_v403.py", "fechar_v402.py", "A1: o fechar (manifesto, arquivo, diffs, handoff)"),
    ("b3_recibo_v403.py", "b3_recibo_v402.py", "A1: o recibo do B(n), passo SIMPLES B11 -> B12"),
    ("gerar_derivacao_pos_rito_v403.py", "gerar_derivacao_pos_rito_v402.py", "A1: este registro (reescrito: so' le)"),
    ("harness_fechar_sandbox_v403.py", "harness_fechar_sandbox_v402.py", "A1: o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA"),
    ("fila_memoria_v403.py", "fila_memoria_v402.py", "A1 (arquivo novo na v402; semente na v403): as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness"),
    ("leitura_v403.py", "leitura_v402.py", "gerencia c1, 28/10: a leitura da rodada reescrita para a v403"),
    ("textos_v403.py", "textos_v402.py", "gerencia c1, 28/10: montado de textos_v403.semente + textos_v403_novo.pysnip (Caminho, Verdade e Vida; F8.1)"),
    ("harness_textos_ensaio_v403.py", "harness_textos_ensaio_v402.py", "gerencia c1, 28/10: o harness do pos-rito reescrito para a v403"),
    ("registrar_mapa_v403.py", "registrar_mapa_v402.py", "gerencia c1, 28/10: o registro da rota umpy.v403.selada_caminho_verdade_vida_27out"),
    ("montar_textos_v403.py", "montar_textos_v402.py", "gerencia c1, 28/10: o montador (semente + fragmento)"),
    ("textos_v403_novo.pysnip", None, "gerencia c1, 28/10: o fragmento escrito a mao para a v403"),
    ("textos_v403.semente", None, "a semente mecanica (copia de bytes do textos_v403.py da preparacao), o esqueleto do montador"),
)
rel = []; ruim = []
for nome, origem, papel in SUITE:
    p = os.path.join(HERE, nome)
    if not os.path.isfile(p):
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
        po = os.path.join(V402_POS, origem)
        if not os.path.isfile(po):
            r["estado"] = "ORIGEM_V402_AUSENTE"; ruim.append(nome)
        else:
            raw = open(po, "rb").read()
            semente = M.bump(raw.decode("utf-8"), (), "v402").encode("utf-8")
            r["origem_v402"] = {"path": po, "sha256": sha(raw)}
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
out = {"contrato": "DERIVACAO_POS_RITO_v403", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False,
       "origem": "pos_rito da v402 FINAL (a cadeia usada no pos-rito real de 27/10), mapa 401 -> 402 e 402 -> 403 por script (semente pura) mais as regras do lote F de derivar_encanamento_v403.py; a adaptacao a mao foi feita pela gerencia c1 em 28/10/2026 (as marcas TEXTO_A_REESCREVER_V403 sairam depois de cada arquivo testado)",
       "arquivos": rel, "nota": "so' le: nenhum script foi executado nem sobrescrito; a semente de cada arquivo e' RECALCULADA em memoria pelo motor a cada vez (hash nunca digitado)"}
dst = os.path.join(HERE, "DERIVACAO_v403.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v403.json gravado (%d arquivos registrados; problemas: %s)" % (len(rel), ruim or "nenhum"))
sys.exit(1 if ruim else 0)

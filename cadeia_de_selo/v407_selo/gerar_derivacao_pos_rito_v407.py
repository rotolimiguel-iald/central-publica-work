# -*- coding: utf-8 -*-
# [ADAPTADO v407, 03/11/2026] sobre a subida mecanica de rotulo da v406 FINAL (_bump_copia_v407.py) por adaptar_pos_rito_v407.py: o conteudo e' o da v407 (O PSION, O CANTO E O PAR: bundle de 9 modulos, o registro com funcao psion_canto_v407, o fechamento_v406 HERDADO e recriado, a chave do lema lida do kernel); a gerencia revisa antes do rito (nao e' versao selada).
"""gerar_derivacao_pos_rito_v407.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v407.
Na v407 a suite do pos_rito e' a SEMENTE mecanica de derivar_encanamento_v407.py (lote F) sobre o arquivo FINAL da cadeia v406 (o que foi USADO no pos-rito real da v406): o numero de versao subido por script (401 -> 406 e 406 -> 407, com a protecao dos nomes nascidos no um.py), mais as regras do lote F (os rotulos B(n), a lista de registros do chain,
o cabecalho do chain, o sufixo dos backups do Atlas e a marca TEXTO_A_REESCREVER_V407 nos arquivos de narrativa). A ADAPTACAO (o que o pos-rito diz da v407: o psion, o canto e o par, com os numeros lidos do rito) foi feita em 03/11/2026 por adaptar_pos_rito_v407.py (+ os _adapt_<arquivo>_v407.py) e textos_v407_novo.pysnip: textos_v407.py sai do montador (montar_textos_v407.py) sobre textos_v407.semente (copia de bytes da semente mecanica) e textos_v407_novo.pysnip; leitura_v407.py, fechar_v407.py, registrar_mapa_v407.py, superficies_v407.py, o harness e o cabecalho do chain foram adaptados e a marca TEXTO_A_REESCREVER_V407 nao sobrou em nenhum arquivo (o p00 confere).
Este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v407_motor.bump), a semente PURA de cada arquivo (so' o mapa de versoes) e a compara com o arquivo atual.
Para cada arquivo do pos_rito que tem origem na v406 grava o sha256 da origem, o da semente pura (recalculada agora), o do arquivo atual, o estado (SEMENTE_PURA | DIFERE_DA_SEMENTE_PURA: regras do lote F ou edicao a mao) e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais.
Escreve so' pos_rito/DERIVACAO_v407.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse. Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v407.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
import ast, difflib, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_v407_motor as M  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()
V406_POS = os.path.join(os.path.dirname(PK), "v406", "pos_rito")
# a suite do pos_rito: (nome na v407, nome da origem na v406, papel). Os tres primeiros blocos sao os da tarefa A1 (encanamento do pos-rito, fila da memoria); os demais sao de outros agentes e entram so' para o registro.
SUITE = (
    ("chain_pos_rito_v407.sh", "chain_pos_rito_v406.sh", "A1: a cadeia (passos 0..14) com o passo NOVO da fila da memoria"),
    ("superficies_v407.py", "superficies_v406.py", "A1: as superficies (diretorio de memoria por V407_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B)"),
    ("fechar_v407.py", "fechar_v406.py", "A1: o fechar (manifesto, arquivo, diffs, handoff)"),
    ("b3_recibo_v407.py", "b3_recibo_v406.py", "A1: o recibo do B(n), passo SIMPLES B15 -> B16"),
    ("gerar_derivacao_pos_rito_v407.py", "gerar_derivacao_pos_rito_v406.py", "A1: este registro (reescrito: so' le)"),
    ("harness_fechar_sandbox_v407.py", "harness_fechar_sandbox_v406.py", "A1: o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA"),
    ("fila_memoria_v407.py", "fila_memoria_v406.py", "A1 (arquivo novo na v406; semente na v407): as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness"),
    ("leitura_v407.py", "leitura_v406.py", "claude-prep-v407, 03/11: a leitura da rodada adaptada ao psion e ao canto (o bundle de 9 modulos, as 76 ancoras, a chave do lema lida do kernel; o fechamento_v406 herdado e os treze registros da v406 selada recriados)"),
    ("textos_v407.py", "textos_v406.py", "claude-prep-v407 (ajudante B1a), 03/11: montado de textos_v407.semente + textos_v407_novo.pysnip (o psion, o canto e o par; sem prosa nova de conteudo)"),
    ("harness_textos_ensaio_v407.py", "harness_textos_ensaio_v406.py", "claude-prep-v407, 03/11: o harness do pos-rito adaptado ao psion e ao canto (controles negativos dos registros novos e dos herdados)"),
    ("registrar_mapa_v407.py", "registrar_mapa_v406.py", "claude-prep-v407 (ajudante B1a), 03/11: o registro da rota nova da v407 (o id esta em registrar_mapa_v407.NOVA)"),
    ("montar_textos_v407.py", "montar_textos_v406.py", "claude-prep-v407 (ajudante B1a), 03/11: o montador (semente + fragmento; DELETAR as funcoes das oito pedras da v405)"),
    ("textos_v407_novo.pysnip", None, "claude-prep-v407 (ajudante B1a), 03/11: o fragmento escrito para a v407 (sem prosa nova de conteudo)"),
    ("adaptar_pos_rito_v407.py", None, "claude-prep-v407, 03/11: o adaptador do pos-rito (os auxiliares; as edicoes exatas por arquivo, com asserts, moram nos _adapt_*_v407.py)"),
    ("textos_v407.semente", None, "a semente mecanica (copia de bytes do textos_v407.py da preparacao), o esqueleto do montador"),
)
SUITE = SUITE + tuple((f_, None, "claude-prep-v407, 03/11: adaptador do pos-rito (edicoes exatas com asserts)") for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v407.py"))
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
        po = os.path.join(V406_POS, origem)
        if not os.path.isfile(po):
            r["estado"] = "ORIGEM_V406_AUSENTE"; ruim.append(nome)
        else:
            raw = open(po, "rb").read()
            semente = M.bump(raw.decode("utf-8"), (), "v406").encode("utf-8")
            r["origem_v406"] = {"path": po, "sha256": sha(raw)}
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
out = {"contrato": "DERIVACAO_POS_RITO_v407", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False,
       "origem": "pos_rito da v406 FINAL (a cadeia usada no pos-rito real da v406), mapa 405 -> 406 e 406 -> 407 por script (semente pura) mais as regras do lote F de derivar_encanamento_v407.py; a adaptacao foi feita pela claude-prep-v407 em 03/11/2026 por adaptar_pos_rito_v407.py (as marcas TEXTO_A_REESCREVER_V407 nao sobraram em nenhum arquivo)",
       "arquivos": rel, "nota": "so' le: nenhum script foi executado nem sobrescrito; a semente de cada arquivo e' RECALCULADA em memoria pelo motor a cada vez (hash nunca digitado)"}
dst = os.path.join(HERE, "DERIVACAO_v407.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v407.json gravado (%d arquivos registrados; problemas: %s)" % (len(rel), ruim or "nenhum"))
sys.exit(1 if ruim else 0)

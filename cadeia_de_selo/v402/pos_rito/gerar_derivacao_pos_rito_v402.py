# -*- coding: utf-8 -*-
"""gerar_derivacao_pos_rito_v402.py -- REGISTRA (SO' LE; nao deriva, nao sobrescreve nada) a proveniencia dos scripts do pos_rito da v402.
Na v402 a suite do pos_rito foi ADAPTADA A MAO, arquivo por arquivo, sobre a SEMENTE mecanica (o arquivo FINAL da cadeia v401, a que foi USADA no rito real de 25/10, com so' o numero de versao subido por script: 400 -> 401 e 401 -> 402, com a protecao dos nomes nascidos no um.py).
Por ordem da gerencia, os derivados NAO sao regerados por derivar_encanamento_v402 (ele sobrescreveria o que foi editado): este script apenas recalcula, em MEMORIA e com o proprio motor (derivar_v402_motor.bump), a semente de cada arquivo e a compara com o arquivo atual.
Para cada arquivo do pos_rito que tem origem na v401 grava o sha256 da origem, o da semente mecanica (recalculada agora), o do arquivo atual, o estado (SEMENTE_INTACTA | EDITADO_A_MAO_SOBRE_A_SEMENTE) e o tamanho do diff (linhas trocadas); os que nao tem origem (escritos de novo) ficam listados como tais.
Escreve so' pos_rito/DERIVACAO_v402.json (com backup de bytes do anterior). NUNCA executa nenhum dos scripts; so' ast.parse. Uso: python -I -B -X utf8 gerar_derivacao_pos_rito_v402.py   (rc 0 = gravou; rc 1 = algum arquivo sem origem lida ou com sintaxe invalida)"""
import ast, difflib, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE); sys.path.insert(0, PK)
sys.argv = sys.argv[:1]
import derivar_v402_motor as M  # noqa: E402

sha = lambda b: hashlib.sha256(b).hexdigest()
V401_POS = os.path.join(os.path.dirname(PK), "v401", "pos_rito")
# a suite do pos_rito: (nome na v402, nome da origem na v401, papel). Os tres primeiros blocos sao os da tarefa A1 (encanamento do pos-rito, fila da memoria); os demais sao de outros agentes e entram so' para o registro.
SUITE = (
    ("chain_pos_rito_v402.sh", "chain_pos_rito_v401.sh", "A1: a cadeia (passos 0..14) com o passo NOVO da fila da memoria"),
    ("superficies_v402.py", "superficies_v401.py", "A1: as superficies (diretorio de memoria por V402_MEMORIA_DIR; recusa rc 3 acima de 195 linhas ou 24000 B)"),
    ("fechar_v402.py", "fechar_v401.py", "A1: o fechar (manifesto, arquivo, diffs, handoff)"),
    ("b3_recibo_v402.py", "b3_recibo_v401.py", "A1: o recibo do B(n), passo SIMPLES B10 -> B11"),
    ("gerar_derivacao_pos_rito_v402.py", "gerar_derivacao_pos_rito_v401.py", "A1: este registro (reescrito: so' le)"),
    ("harness_fechar_sandbox_v402.py", "harness_fechar_sandbox_v401.py", "A1: o harness do fechar/chain em sandbox, com o ensaio da fila da memoria em COPIA"),
    ("fila_memoria_v402.py", None, "A1 (ARQUIVO NOVO): as operacoes da fila da memoria do pos-rito (guardas, pausa, pinar, verificar), chamadas pelo chain e pelo harness"),
    ("leitura_v402.py", "leitura_v401.py", "outro agente"),
    ("textos_v402.py", "textos_v401.py", "outro agente (a gerencia reescreve)"),
    ("harness_textos_ensaio_v402.py", "harness_textos_ensaio_v401.py", "outro agente"),
    ("registrar_mapa_v402.py", "registrar_mapa_v401.py", "outro agente"),
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
        po = os.path.join(V401_POS, origem)
        if not os.path.isfile(po):
            r["estado"] = "ORIGEM_V401_AUSENTE"; ruim.append(nome)
        else:
            raw = open(po, "rb").read()
            semente = M.bump(raw.decode("utf-8"), (), "v401").encode("utf-8")
            r["origem_v401"] = {"path": po, "sha256": sha(raw)}
            r["semente_mecanica_sha256"] = sha(semente)
            if semente == atual:
                r["estado"] = "SEMENTE_INTACTA"
            else:
                r["estado"] = "EDITADO_A_MAO_SOBRE_A_SEMENTE"
                a_, b_ = semente.decode("utf-8").splitlines(), atual.decode("utf-8").splitlines()
                sm = difflib.SequenceMatcher(None, a_, b_, autojunk=False)
                r["diff_contra_a_semente"] = {"linhas_da_semente": len(a_), "linhas_do_arquivo": len(b_), "linhas_trocadas_ou_novas": sum((j2 - j1) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal")}
    rel.append(r)
    print("%-38s %-34s %s" % (nome, r["estado"], r["sha256"][:12]))
out = {"contrato": "DERIVACAO_POS_RITO_v402", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "executado": False,
       "origem": "pos_rito da v401 FINAL (a cadeia usada no rito real de 25/10), mapa 400 -> 401 e 401 -> 402 por script (semente); depois EDITADO A MAO, arquivo por arquivo (a gerencia mandou nao regerar com derivar_encanamento_v402)",
       "arquivos": rel, "nota": "so' le: nenhum script foi executado nem sobrescrito; a semente de cada arquivo e' RECALCULADA em memoria pelo motor a cada vez (hash nunca digitado)"}
dst = os.path.join(HERE, "DERIVACAO_v402.json")
if os.path.exists(dst):
    raw = open(dst, "rb").read(); bk = dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
open(dst + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(dst + ".tmp", dst)
print("DERIVACAO_v402.json gravado (%d arquivos registrados; problemas: %s)" % (len(rel), ruim or "nenhum"))
sys.exit(1 if ruim else 0)

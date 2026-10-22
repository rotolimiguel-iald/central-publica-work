# -*- coding: utf-8 -*-
"""Acrescenta ao AFERIDOR_v383.txt a 3a PASSADA (durante o rito), VERBATIM, e as disposicoes; mapa: ANOTACAO."""
import os, sys, time, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
T = "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl"
HDR = "# Terceira passada da v383 (só leitura, com o rito rodando)"
found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if '"queue-operation"' not in line or "aa2b5030fb5e4aa4a" not in line:
            continue
        d = json.loads(line); c = d.get("content")
        if d.get("type") == "queue-operation" and isinstance(c, str) and '<agent-message from="aa2b5030fb5e4aa4a">' in c and HDR in c:
            found = c; break
assert found, "relatorio nao achado na fila"
k = found.find("  " + HDR); body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
assert "RODAR A CADEIA" in rep
disp = """
--------------------------------------------------------------------------------
DISPOSICOES DA GERENCIA SOBRE A 3a PASSADA (%s) -- recomendacao: RODAR A CADEIA; acolhida.
--------------------------------------------------------------------------------
B-1 (a porta da memoria roda antes do handoff e do registro): ACOLHIDO -- a ordem pos-rito passa a ser: conferidor -> cadeia (ate a porta e o grep) -> arquivar -> handoff
-> registrar -> porta da memoria DE NOVO -> arquivar de novo (idempotente).
B-2 (o handoff nao pode ser rerodado se falhar no meio): ACOLHIDO -- o handoff confere ANTES da primeira gravacao que o indice comporta a linha e a marca DECIDIDO
(senao recusa sem gravar nada); a definicao da linha subiu para antes das gravacoes, o texto nao mudou.
B-3 (o handoff nao conferia os AFERIDOR arquivados): ACOLHIDO -- recusa sem gravar se algum dos dois nao existir no arquivo da Central.
B-4 (esta passada antes do arquivar final): ACOLHIDO -- gravada aqui, antes de qualquer arquivar.
B-5 (nota sobre o «abaixo de 5» de ECO_e): acolhida como nota; nenhuma acao.
A nota sobre a linha do β no indice (a primeira de «Ler primeiro»): o ponteiro guarda o essencial e a linha inteira esta no MEMORY_2.md; fica dito.
""" % time.strftime("%d/%m/%Y %H:%M")
p = os.path.join(HERE, "AFERIDOR_v383.txt"); raw = open(p, "rb").read()
if HDR in raw.decode("utf-8", errors="replace"):
    print("AFERIDOR_v383.txt: a 3a passada ja esta")
else:
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    head = "\n\n" + "=" * 80 + "\n3a PASSADA -- AS CORRECOES DA CADEIA E AS CINCO TROCAS DO CANDIDATO -- v383 (o mesmo agente, so leitura, durante o rito; VERBATIM, indentacao do harness removida)\n" + "=" * 80 + "\n\n"
    novo = raw + (head + rep + disp).encode("utf-8"); open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo) > len(raw); os.replace(p + ".tmp", p)
    assert open(p, "rb").read()[:len(raw)] == raw
    print("AFERIDOR_v383.txt:", len(raw), "->", len(novo), "B; sha16", hashlib.sha256(novo).hexdigest()[:16])
regs = rotas._le()
if not any("afericao3_v383" in str(r.get("titulo", "")) for r in regs):
    o = rotas.registrar([dict(tipo="ANOTACAO", rota_id="kernel.regra_matriz.cadeia_unica", status="EXAMINADA", estatuto="REAL", olhou_dados=False,
        titulo="afericao3_v383 (02/10, noite; o mesmo agente, durante o rito): as cinco trocas do candidato certas e exatas (globals() e o espaço do módulo; SEALED_CODATA_ALPHA só na linha 95); todas as correções da cadeia feitas, sem regressão; a folga do índice basta; 5 BAIXOS de ordem pós-rito, acolhidos; recomendação RODAR A CADEIA",
        resultado="o handoff passa a conferir antes de gravar (os AFERIDOR arquivados; o orçamento do índice com a linha e o DECIDIDO); a porta da memória roda de novo depois do handoff e do registro",
        nao_refazer="rodar a porta da memória depois do handoff, não só na cadeia", proximo_passo="o fim do rito; o conferidor; a cadeia; arquivar; handoff; registrar; porta; arquivar",
        artefatos=[p], refs=["kernel.livro_de_cobrancas.otica"])], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
    print("mapa:", {k: o[k] for k in o if k != "registros"})
else:
    print("mapa: ja registrado")

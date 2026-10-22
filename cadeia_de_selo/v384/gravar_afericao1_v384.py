# -*- coding: utf-8 -*-
"""Grava AFERIDOR_v384.txt com a 1a PASSADA do aferidor (o trabalhador e o rascunho do pre-registro), VERBATIM do transcrito, e registra no mapa (ANOTACAO).
As disposicoes da gerencia sao acrescentadas depois, por outro script, AO LADO (nunca por cima)."""
import os, sys, json, hashlib, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
T = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "6da8f00d-d44f-4888-a88d-fc9f73eead3d.jsonl")
AG = "a96f6b80e5382e074"; HDR = "AFERIÇÃO DO PILAR QUÂNTICO v384"
found = None
with open(T, encoding="utf-8") as f:
    for line in f:
        if AG not in line or HDR not in line:
            continue
        d = json.loads(line); c = d.get("content") if d.get("type") == "queue-operation" else None
        if isinstance(c, str) and ('<agent-message from="%s">' % AG) in c and HDR in c:
            found = c
assert found, "relatorio nao achado na fila"
k = found.find("  " + HDR); body = found[k:]; e = body.find("</agent-message>"); body = body[:e] if e > 0 else body
rep = "\n".join((l[2:] if l.startswith("  ") else l) for l in body.split("\n")).rstrip() + "\n"
assert "CORRIGIR ANTES DE CONGELAR" in rep and "ACHADOS" in rep
p = os.path.join(HERE, "AFERIDOR_v384.txt")
head = ("=" * 80 + "\n1a PASSADA -- O TRABALHADOR DA GPU E O RASCUNHO DO PRE-REGISTRO -- v384 (agente aferidor, so leitura, 03/10/2026; VERBATIM, indentacao do harness removida)\n"
        + "=" * 80 + "\n\n")
novo = (head + rep).encode("utf-8")
if os.path.exists(p):
    print("AFERIDOR_v384.txt ja existe -- nada gravado"); sys.exit(0)
open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
print("AFERIDOR_v384.txt:", len(novo), "B; sha16", hashlib.sha256(novo).hexdigest()[:16])
o = rotas.registrar([dict(tipo="ANOTACAO", rota_id="quantica.pilar_v384_decisao_operador_03out", status="EM_CURSO", estatuto="REAL", olhou_dados=False,
    titulo="afericao1_v384 (03/10): o motor de fisica conferido (row-stacking, Choi, a centragem de Kossakowski, a linha do traco, Spohn, o classificador, E1..E6) e a transcricao dos cinco operadores coeficiente a coeficiente; 17 achados (1 ALTO: o criterio do T1 no piso do estimador por secao aurea; 8 MEDIOS; 8 BAIXOS); recomendacao CORRIGIR ANTES DE CONGELAR",
    nota="nada rodado com os operadores da teoria; as afericoes com operadores analiticos e aleatorios; artefatos na pasta aferidor_v384 do pacote",
    nao_refazer="nao usar secao aurea para o expoente (piso ~sqrt(eps)/curvatura); nao deixar o hash do trabalhador fora da especificacao congelada; nao tratar o N2 como controle (e' identidade)",
    proximo_passo="as correcoes 1-7 obrigatorias e 9, 11, 12, 13 no trabalhador; o texto do pre-registro; nova sonda de tempo; congelar; levar ao operador",
    artefatos=[p], refs=["quantica.cinco_operadores_lindblad_matrizes", "quantica.dobras_c3_hierarquia_e_matematica"])], "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print("mapa:", {k_: o[k_] for k_ in o if k_ != "registros"})

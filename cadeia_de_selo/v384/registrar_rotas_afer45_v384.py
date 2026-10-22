# -*- coding: utf-8 -*-
"""Registra no MAPA DE ROTAS a 4a e a 5a afericoes do pilar quantico e as sondas dos trabalhadores 39e6d560 e fb974f9d (com a variabilidade). Numeros LIDOS."""
import json, os, subprocess, sys, tempfile
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
QUEM = "claude-code/central-de-patentes (gerencia) sessao 6da8f00d"
P = lambda *a: os.path.join(HERE, *a)
A4 = json.load(open(P("afericao4_resultado.json"), encoding="utf-8")); A5 = json.load(open(P("afericao5_resultado.json"), encoding="utf-8"))
c4 = Counter(a["estado"] for g in A4["grupos"] for a in (g.get("itens") or [])); c5 = Counter(a["estado"] for g in A5["grupos"] for a in (g.get("itens") or []))
sv4 = sum(1 for v in A4["verificacao"]["veredictos"] if not v["refutado"])
M7 = json.load(open(P("teste_motor_v7", "result.json"), encoding="utf-8"))
T = {k: json.load(open(P(k, "result.json"), encoding="utf-8")) for k in ("teste_tempo_v4", "teste_tempo_v5", "teste_tempo_v6", "teste_tempo_v7", "teste_tempo_v8")}
REG = [
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_4a_passada", "dominio": "QUANTICA",
     "titulo": "a 4a afericao: as correcoes da 3a conferidas e novos achados",
     "pergunta": "as correcoes da 3a passada resolveram o que foi achado, sem regressao?", "dados": ["o pacote da v384 (trabalhador b3bdecab), rascunhos v4"],
     "metodo": "workflow wf_4a501319-22f: 5 aferidores + regressao + verificador adversarial; stubs do lancador; testes puros; simulacao do artigo",
     "resultado": "55 entradas (lente x item): %s; %d achados novos, %d sobreviventes" % (dict(c4), len(A4["novos"]), sv4),
     "veredito": "CORRIGIR_ANTES_DE_CONGELAR", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "defeito": "a gravacao da gerencia indexou por id e omitiu 5 entradas; errata ao lado no AFERIDOR e nas disposicoes",
     "nao_refazer": "disposicoes em disposicoes_afericoes_v384.json e no AFERIDOR_v384.txt", "proximo_passo": "a 5a afericao",
     "onde": "scratchpad/v384/afericao4_resultado.json", "artefatos": [P("afericao4_resultado.json")], "refs": ["quantica.pilar_v384_afericao_3a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_5a_passada", "dominio": "QUANTICA",
     "titulo": "a 5a afericao: as correcoes da 4a conferidas; o verificador adversarial nao rodou (sessao expirada)",
     "pergunta": "as correcoes da 4a passada resolveram o que foi achado, sem regressao?", "dados": ["o pacote da v384 (trabalhador 39e6d560), rascunhos v5"],
     "metodo": "workflow wf_163abb94-0de: 5 aferidores + regressao; o verificador falhou por OAuth expirado",
     "resultado": "%d entradas: %s; %d achados novos SEM verificacao" % (sum(c5.values()), dict(c5), len(A5["novos"])),
     "veredito": "CORRIGIR_ANTES_DE_CONGELAR", "estatuto": "REAL", "status": "EXAMINADA_COM_DEFEITO", "olhou_dados": False,
     "defeito": "a verificacao adversarial dos 23 novos nao rodou; a 6a passada a faz",
     "nao_refazer": "disposicoes gravadas", "proximo_passo": "a 6a afericao (conferencia + verificacao)",
     "onde": "scratchpad/v384/afericao5_resultado.json", "artefatos": [P("afericao5_resultado.json"), P("disposicoes_afericoes_v384.json"), P("AFERIDOR_v384.txt")],
     "refs": ["quantica.pilar_v384_afericao_4a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_sondas_variabilidade", "dominio": "QUANTICA",
     "titulo": "a variabilidade das sondas de tempo do pilar (d = 64) e o motor do trabalhador fb974f9d",
     "pergunta": "quanto varia o custo medido por instancia entre sondas, e o motor corrente passa?",
     "dados": ["operadores aleatorios (tempo) e analiticos/sinteticos (motor)"], "metodo": "worker --mode timing / engine; MAGMA em todo tamanho",
     "resultado": "d64 por instancia (s): " + ", ".join("%s %.2f (trab. %s)" % (k, v["timing"]["64"]["pipeline_s"], v["worker_sha256"][:8]) for k, v in T.items())
                  + "; motor %s %s" % (M7["worker_sha256"][:16], M7["verdict"]),
     "veredito": M7["verdict"], "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "nao_refazer": "o orcamento usa a sonda do trabalhador congelado; a faixa vai ao pre-registro",
     "onde": "scratchpad/v384/teste_tempo_v4..v8, teste_motor_v7", "artefatos": [P(k, "result.json") for k in T] + [P("teste_motor_v7", "result.json")],
     "refs": ["quantica.pilar_v384_sondas_b3bdecab"]},
]
for r in REG:
    fd, tmp = tempfile.mkstemp(suffix=".json", dir=HERE); os.close(fd)
    open(tmp, "w", encoding="utf-8").write(json.dumps(r, ensure_ascii=False))
    out = subprocess.run([sys.executable, ROTAS, "registrar", tmp, "--quem", QUEM], capture_output=True, text=True, encoding="utf-8")
    os.remove(tmp); print(r["rota_id"], "rc", out.returncode); assert out.returncode == 0, out.stderr

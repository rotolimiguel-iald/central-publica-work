# -*- coding: utf-8 -*-
"""ERRATA AO LADO do seq 308 (gerencia, em nome proprio): o horario do selo e as duracoes (~43 / ~18 min) da anotacao foram DIGITADOS (do resumo da
sessao), nao lidos pelo script -- o patch que os faria ler falhou e o registro rodou com o texto antigo. Aqui, LIDOS: o timestamp do selo corrente
(um_absoluto_selo.json) e os horarios do rito (rito_horarios_v383.txt). Os valores digitados conferem; o defeito e' de procedimento."""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "C:/IALD/MAPA_DE_ROTAS"); import rotas
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "N\u00f3s")
SELO_P = os.path.join(NOS, "um_absoluto_selo.json")
HOR_P = os.path.join(os.path.dirname(HERE), "v383", "rito_horarios_v383.txt")
regs = rotas._le()
if any(r.get("tipo") == "ERRATA" and str(r.get("corrige")) == "308" for r in regs):
    print("errata ja registrada"); sys.exit(0)
alvo = [r for r in regs if r.get("seq") == 308]
assert len(alvo) == 1 and alvo[0].get("rota_id") == "infra.gpu_rtx5090_ambiente_02out", "o seq 308 nao e' a anotacao esperada"
ts = json.load(open(SELO_P, encoding="utf-8"))["timestamp"]
assert ts.startswith("2026-10-02 "), ts
hor = open(HOR_P, encoding="utf-8").read().split()
def seg(h):
    a, b, c = (int(x) for x in h.split(":")); return a * 3600 + b * 60 + c
t0, t1, ts_h = seg(hor[0]), seg(hor[1]), ts.split()[1]
ate, depois = seg(ts_h) - t0, t1 - seg(ts_h)
confere = (ts_h == "20:47:14") and (43 <= ate // 60 <= 43) and (18 <= depois // 60 <= 18)
txt = ("ERRATA AO LADO do seq 308 (gerência, em nome próprio): o horário do selo e as durações foram DIGITADOS do resumo da sessão, não lidos pelo script "
       "(o patch que os faria ler falhou por barra invertida num heredoc e o registro rodou com o texto antigo). LIDOS AGORA: timestamp do selo = %s "
       "(um_absoluto_selo.json); rito v383 de %s a %s (rito_horarios_v383.txt) => %d min %02d s até o selo e %d min %02d s de autoteste. %s"
       ) % (ts, hor[0], hor[1], ate // 60, ate % 60, depois // 60, depois % 60,
            "Os valores digitados CONFEREM; o defeito foi de procedimento." if confere else "Os valores digitados NÃO conferem: valem os lidos aqui.")
o = rotas.registrar([dict(tipo="ERRATA", rota_id="infra.gpu_rtx5090_ambiente_02out", corrige=308, status="EXAMINADA", estatuto="REAL", olhou_dados=False,
                          titulo="errata ao lado do seq 308: horários do rito v383 lidos por script", nota=txt, artefatos=[SELO_P, HOR_P, os.path.abspath(__file__)])],
                    "claude-code/central-de-patentes (gerência) sessão 6da8f00d")
print(txt)
print({k: o[k] for k in o if k != "registros"})

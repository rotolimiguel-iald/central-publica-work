import json, os, subprocess, hashlib
W = os.path.join("C:/IALD/Central de Patentes/work/organismo_iald_12out")
R = os.path.join(W, "4_RELATORIO")
ROTAS = "C:/IALD/MAPA_DE_ROTAS/rotas.py"
IALD = "C:/IALD/PROGRAMA_IALD/iald.py"
PG = "C:/IALD/PROGRAMA_IALD"
def run(a, cwd=None):
    r = subprocess.run(["python"] + a, capture_output=True, text=True, encoding="utf-8", cwd=cwd)
    return (r.stdout or "") + (r.stderr or "")
rel = os.path.join(R, "O_ORGANISMO_E_A_PROVA_DISTINTIVA.md")
sh = hashlib.sha256(open(rel, "rb").read()).hexdigest()
u = [{
 "id": "F1.MOTOR", "frente": "F1",
 "titulo": "O organismo: a IALD como motor único (inscrição de posto 1, transporte, defasagem, leitura, memória M = ⟨ψ,Π_N ψ⟩) e o programa da prova distintiva da QG",
 "dono": "claude-c1", "status": "EM_CURSO", "gate": None,
 "criterio_de_fechado": "Pedra TGLExt.IALD (nome provisório) com as oito correções C1–C8 da §5.2 do relatório, re-pinada às candidatas vigentes (rank r3, tempo R2), recompilada em sandbox e reauditada por cético independente; o nome final e a entrada na v392 são do operador; o programa da prova distintiva fica pré-registrado como plano, sem abrir dado; nada move o gate.",
 "origem": "Ordem do operador de 12/10/2026, verbatim sha256 78ef70e6f9868281 (work/cunhagens_12out): «Tente resolver o problema da gravidade quantica de uma vez por todas e pense em como ter a prova distintiva dela. eu sinto que falta ligar tudo isso junto em uma coisa só, um organismo só, que é a própria IALD».",
 "escopo": "Sandbox Lean; nada no Nós, um.py, selo ou gate; nenhum dado observado.",
 "reaproveitamento_previo": "Levantamentos 0_LEVANTAMENTO_ORGANISMO e 0_LEVANTAMENTO_PROVA (mapa, inventário da bancada, Atlas, acervo, kernel).",
 "restricoes": "A palavra recusada da régua nunca; confidenciais nunca.",
 "reivindicacao": None, "evidencia": [], "historico": []}]
up = os.path.join(W, "5_REGISTRO", "F1.MOTOR_unidade.json")
json.dump(u, open(up, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("nova:", run([IALD, "nova", "--json", up, "--quem", "claude-c1"], cwd=PG).strip()[-200:])
for n in ("registro_rota_F1.MOTOR.json", "registro_mapa_F1.MOTOR.json"):
    o = run([ROTAS, "registrar", os.path.join(R, n), "--quem", "claude-c1 (gerência)"])
    try:
        j = json.loads(o); print("mapa", n, j.get("ok"), [g.get("seq") for g in j.get("gravados", [])], j.get("erro"))
    except Exception:
        print("mapa", n, o[-500:])
nota = ("Pedra TGLExt.IALD (provisório «o motor único», a267bc6d, 51 declarações, 0 sorry, trio) compila e se reproduz bit a bit; duas auditorias: não entra na v392 como está, oito correções C1–C8 (âncora fraca, H-N decorativa em T2, Ágape só por nome, homônimo «defasagem», [ONTO] nas docstrings, β não pesa no motor, re-pino às candidatas vigentes, «Q16/Q17 resolvidas» exagera). "
        "Achado: os três nomes do projetor do Nome (ialdSelector, PFmic, post a) já eram a mesma construção (rfl); a lei da memória M = Tr[ρ·Π_N] virou termo. QG: provada como validade desde a v391; o único elo é β na natureza a 5σ; programa da prova distintiva com a razão de Hubble como decisiva, N_eff em par como testemunha de forma, m₂ como testemunha de morte (~2031), piso por κ como falsificador; nenhum canal chega a 5σ só por decisão. 13 perguntas ao operador nas quatro línguas (§6). Relatório sha16 " + sh[:16] + ".")
print(run([IALD, "avancar", "F1.MOTOR", "--quem", "claude-c1", "--status", "ENTREGUE", "--evidencia", rel, "--nota", nota], cwd=PG).strip()[-250:])

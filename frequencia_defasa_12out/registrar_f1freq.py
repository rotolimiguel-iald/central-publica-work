"""F1.FREQUENCIA: registra ROTA e RESULTADO no mapa, avança a unidade a AUDITADA e põe a errata ao lado na memória (backup de bytes)."""
import datetime
import json
import os
import subprocess

W = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out\4_RELATORIO"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
IALD = r"C:\IALD\PROGRAMA_IALD\iald.py"
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"


def run(args, cwd=None):
    r = subprocess.run(["python"] + args, capture_output=True, text=True, encoding="utf-8", cwd=cwd)
    return (r.stdout or "") + (r.stderr or "")


for name in ("registro_rota_F1.FREQUENCIA.json", "registro_mapa_F1.FREQUENCIA.json"):
    out = run([ROTAS, "registrar", os.path.join(W, name), "--quem", "claude-c1 (gerência)"])
    try:
        j = json.loads(out)
        print("mapa", name, j.get("ok"), [g.get("seq") for g in j.get("gravados", [])], j.get("erro"))
    except Exception:
        print("mapa", name, out[-300:])

nota = ("Rodada 2 (13/10): 29 PASSA, 3 FALHA pré-registradas (negativos honestos provados no kernel: o posto 1 NÃO sobrevive à defasagem — "
        "D_∞F_θ(1) = diag(1−β, β) tem posto 2; «o que transmite defasa» literal falha em θ = 0), 1 CITADO, 3 CITADO_REAL, O1 [ONTO], O2 [OPEN]; "
        "controles 14/14; duas auditorias céticas dizem pode fechar. Achado central: POSTO = RANK vale no átomo; o traço ω(I) = 1 sobrevive à defasagem e ao colapso tipado, o posto 1 não. "
        "Pedra TheUnitIsTheRank r2 (3195ef8f0766384c; 177 teoremas + 13 defs; trio; 0 sorry; .olean reproduzido por dois auditores). "
        "Segue AUDITADA: entra na v392 depois da rodada 3 só de nomes e comentários, reauditada, e com o nome do operador.")
print(run([IALD, "avancar", "F1.FREQUENCIA", "--quem", "claude-c1", "--status", "AUDITADA", "--evidencia",
           os.path.join(W, "RELATORIO_FINAL.md"), "--nota", nota], cwd=r"C:\IALD\PROGRAMA_IALD").strip()[-200:])

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
P1 = os.path.join(MEM, "posto-e-rank-10out.md")
b1 = open(P1, "rb").read()
open(P1 + ".bak_" + ts, "wb").write(b1)
err = ("\n\n> ⚠ **ERRATA AO LADO (13/10/2026, gerência c1, em nome próprio; achado central da F1.FREQUENCIA, sonda AuditorEstatutoR2.lean 6/6 no trio):** "
       "«o Um posto = posto 1 = Tr P = ω(I)» vale para PROJEÇÕES e no ÁTOMO (Tr ρ = Tr ρ² ⟺ d = 1). O que sobrevive à defasagem e ao colapso tipado é o TRAÇO "
       "(ω(I) = 1, o POSTO de 05/10), não o posto 1: D_∞F_θ(1) = diag(1−β, β) tem traço 1 e posto 2; I/2 tem traço 1 e posto 2; Tr P_F ≈ 4. "
       "POSTO = RANK é exato no átomo; fora dele, posto é posição/inscrição e o invariante é o traço. O texto acima fica como registro.\n").encode("utf-8")
n1 = b1 + (b"" if b1.endswith(b"\n") else b"\n") + err
open(P1 + ".tmp", "wb").write(n1)
assert os.path.getsize(P1 + ".tmp") == len(n1)
os.replace(P1 + ".tmp", P1)

P2 = os.path.join(MEM, "MEMORY.md")
b2 = open(P2, "rb").read()
open(P2 + ".bak_" + ts, "wb").write(b2)
old = "- [POSTO = RANK (10/10)](posto-e-rank-10out.md) — **cunhagem**: o Um posto = posto 1 = Tr P = ω(I)".encode("utf-8")
new = "- [POSTO = RANK (10/10)](posto-e-rank-10out.md) — **cunhagem**; F1.FREQUENCIA (13/10): vale no átomo; o traço ω(I)=1 sobrevive à defasagem, o posto 1 não (errata ao lado)".encode("utf-8")
assert b2.count(old) == 1
n2 = b2.replace(old, new)
open(P2 + ".tmp", "wb").write(n2)
os.replace(P2 + ".tmp", P2)
print("memória ok", len(b1), "->", len(n1), "|", len(b2), "->", len(n2), "linhas", len(n2.decode("utf-8").splitlines()))

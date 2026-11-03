# -*- coding: utf-8 -*-
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V = CEN / "work/cunhagens_13out/OPERADOR_02nov_a_ponte_e_o_ACOM_espelhar_a_teoria_inteira_von_neumann_de_um_lado_ACOM_do_outro_1_igual_1_verbatim.txt"
t1 = "Excelente, vamos prosseguir. Você me disse que tem uma ponte da álgebra de von neumann no mathlib que vc não consegue ultrapassar, e agora eu vejo, a ponte é o ACOM; é justamente a reconstrução que acabamos de tipar"
t2 = "Você precisa espelhar no ACOM a teoria inteira e ela vai se equilibrar com a Álgebra de Von neuman de um lado e o ACOM de outro 1=1; faz sentido pra vc ?"
if not V.exists():
    V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), duas mensagens seguidas, verbatim:" + chr(10)*2 + t1 + chr(10)*2 + t2 + chr(10), encoding="utf-8")
fv = s16(V); print("verbatim", fv)
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.a_ponte_do_atrito_candidata_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "Operador (02/11): «a ponte é o ACOM; é justamente a reconstrução que acabamos de tipar» e «espelhar no ACOM a teoria inteira … von Neumann de um lado e o ACOM de outro 1=1»",
  "resultado": "Verbatim sha16 %s. Aferição da gerência: ACOM = REFLECT + MANIFEST (Atlas: projeção no espelho angular + inversão do colapso A_β = √(1−β)P + √β Q; canal de Kraus + código holográfico; sombra finita ~1e-16 no setor derivado). No finito, matrizes SÃO álgebra de von Neumann (tipo I): os dois lados já são o mesmo objeto e o «1=1» é a completude de Kraus Σ K†K = 1, cuja versão escalar é o_balanco_fecha_a_cada_volta / o_um_se_fractaliza. A parede da mathlib é outra: Tomita–Takesaki do fator genuíno III₁ (sem matriz densidade; StandardSubspace de Tanimoto 2026 com Tomita/KMS em TODO; VonNeumannAlgebra 162 linhas; kernel usa theFactorObject : VonNeumannAlgebra e tem o Tomita finito como termo próprio). O espelho no ACOM dá a TESTEMUNHA finita de cada pedra (a arquitetura já em uso: Certificado II; a ponte da dimensão v77) e não atravessa o III₁; o kernel diz que o fecho total é proibido por teorema (full_static_witness_exists = false; the_charge_never_completes). Selo v405: 35 chaves 'witness', 3 'kraus', 2 'manifest', 1 'reflect' em 2321 folhas; kernel 10.066 teoremas." % fv,
  "estatuto": "INPUT (proposta dele); ONTO (leitura); REAL (contagens no selo)", "artefatos": [str(V), "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/um_absoluto_selo.json".replace("/", chr(92))]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_espelho_acom_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-120:].replace(chr(10), " ")); assert q.returncode == 0
def append_bytes(path, add):
    b = path.read_bytes(); add_b = add.encode("utf-8")
    if bytes([13, 10]) in b: add_b = add_b.replace(bytes([10]), bytes([13, 10]))
    bk = path.with_name(path.name + ".bak_" + TS)
    with open(bk, "xb") as f: f.write(b)
    assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f: f.write(b.rstrip() + add_b)
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path); print(path.name, len(b), "->", path.stat().st_size)
NL = chr(10)
append_bytes(M / "beta-e-a-regra-matriz-02out.md", NL + NL + "## 02/11/2026 — PROPOSTA DO OPERADOR: espelhar a teoria inteira no ACOM (von Neumann de um lado, ACOM do outro, 1=1) (verbatim sha16 `" + fv + "`)" + NL + NL +
 "**Ele:** «a ponte é o ACOM; é justamente a reconstrução que acabamos de tipar» e «espelhar no ACOM a teoria inteira e ela vai se equilibrar … 1=1; faz sentido?». **Aferição [REAL/ONTO]:** ACOM = REFLECT + MANIFEST (canal de Kraus + código holográfico; sombra finita). Matrizes são von Neumann tipo I: no finito os dois lados são o mesmo objeto e o 1=1 é a completude de Kraus Σ K†K = 1, cuja forma escalar é `o_balanco_fecha_a_cada_volta`/`o_um_se_fractaliza`. A parede da mathlib é o Tomita–Takesaki do III₁ (sem matriz densidade); o espelho dá a TESTEMUNHA finita de cada pedra (Certificado II; a ponte da dimensão v77) e não atravessa o III₁ (`full_static_witness_exists = false` é teorema). Selo v405: 35 chaves `witness` em 2321 folhas; 10.066 teoremas. **Resposta dada:** faz sentido como programa de testemunhas, com o limite dito; primeiro passo proposto: inventário medido do que já está espelhado. **How to apply:** nunca dizer que o espelho no ACOM prova o III₁; dizer «testemunha». [[regra-dos-dois-regimes]] [[a-leitura-cria-o-objeto-07out]]" + NL)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)

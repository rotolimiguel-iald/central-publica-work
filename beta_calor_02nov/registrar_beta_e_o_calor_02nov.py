# -*- coding: utf-8 -*-
"""02/11/2026: pergunta do operador «β_TGL é a representação algébrica do calor?» — verbatim, aferição e registro
(Mapa de Rotas, memória, Atlas). Nada entra no kernel; nenhum gate se move. Backup de bytes antes de tocar."""
import datetime, hashlib, json, math, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]

V = CEN / "work/cunhagens_13out/OPERADOR_02nov_calor_equilibrio_do_atrito_adimensional_beta_representacao_algebrica_do_calor_verbatim.txt"
texto = "Calor é o fenômeno do equilíbrio do atrito entre os corpos, e ele também é adimensional, então, penso, betatgl é a representação algébrica do calor?"
if not V.exists():
    V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), verbatim; pergunta, não ordem:\n\n" + texto + "\n", encoding="utf-8")
fv = s16(V)
print("verbatim", fv)

alpha = 7.2973525693e-3
beta = alpha * math.sqrt(math.e)
contas = {"alpha_fine_codata_2018": alpha, "sqrt_e": math.sqrt(math.e), "beta_runtime": beta,
          "ln_beta_sobre_alpha": math.log(beta / alpha),
          "kT_300K_meV": 8.617333262e-5 * 300 * 1e3, "kT_ln2_300K_meV": 8.617333262e-5 * 300 * 1e3 * math.log(2),
          "nota": "beta nunca literal: alpha x sqrt(e) em runtime; ln(beta/alpha) = 1/2 nat exato por construcao"}
PJ = CEN / "work/beta_calor_02nov/CONTAS_BETA_E_O_CALOR_02nov.json"
PJ.write_text(json.dumps(contas, ensure_ascii=False, indent=1), encoding="utf-8")

K = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt")
reg = [{"tipo": "ROTA", "rota_id": "conceitual.beta_e_o_calor_atrito_02nov", "dominio": "CONCEITUAL",
  "titulo": "«β_TGL é a representação algébrica do calor?» (operador, 02/11): aferição no kernel e no Atlas",
  "pergunta": "β é o calor (fenômeno do equilíbrio do atrito, adimensional)?",
  "dados": [], "olhou_dados": False,
  "metodo": "grep no kernel (TGLExt, ChatgptAudit) por calor/heat/Clausius/temperatura/Landauer/atrito; Atlas (verbetes β, Meia-Nat, selo conceitual, β por nat); índice do acervo («calor atrito»: 0; «calor»: só patentes/engenharia; «Landauer»: artigo ACOM 2026); memória rota-re-k-e-landauer-02nov; contas em runtime.",
  "resultado": "O número corrige uma palavra: calor tem dimensão (energia) [KNOWN]; o adimensional no fenômeno é a entropia em nats e o coeficiente de atrito. O que o kernel JÁ tem: β como atrito constante (ThePsionAndTheViscosity.viscosity_is_the_constant_friction, v383: d/dt e^(-tβg) = -(βg)e^(-tβg), «o coeficiente βg é a viscosidade»); a cadeia do operador «tensão → atrito → temperatura → magnetismo» registrada em MassaTensaoPura (tensão frameCovectorStress; atrito βg; temperatura κ/2π = reciprocal_temperature; magnetismo ausente); o balanço boost_defect_with_derived_period: defeito = calor − (1/P)·η·área, Clausius = defeito zero; «sob Clausius o defeito é zero e a parcela é o que o mantém zero», parcela por volta ≤ β (parcela_le_beta). O calor dentro de β: β = α·e^(1/2 nat), ln(β/α) = 0,5 (runtime); a Meia-Nat é «a travessia» (Atlas). Parentesco com Landauer (β = «o custo de distinguir 1 de 0», selo): a diferença é a dimensão (k_B T ln 2 é calor, 17,9 meV a 300 K; β é fração); a leitura literal de β como calor por bit já caiu (12 meV/bit, Gaudenzi ~577σ; memória 02/11).",
  "veredito": "LEITURA_REFORMULADA_A_RATIFICAR", "estatuto": "ONTO", "status": "EXAMINADA",
  "defeito": "«calor é adimensional» não se sustenta; a ligação atrito (βg) → temperatura (κ/2π) tem as duas pontas como termo e não tem termo que as ligue.",
  "nao_refazer": "A leitura proposta pela gerência: β não é o calor; é o coeficiente de atrito da fronteira (a parcela que mantém o balanço de Clausius fechado a cada volta), e o calor adimensional (a meia-nat) está dentro de β como expoente. «Calor é o que o atrito cobra; β é quanto cobra por nat de travessia» (β por nat: f_leak = 1 − e^(−βN*)).",
  "proximo_passo": "Ratificação ou correção do operador; se ratificar, pedra candidata ligando viscosity_is_the_constant_friction a reciprocal_temperature só se houver termo honesto (hoje não há).",
  "onde": "TGLExt/ThePsionAndTheViscosity.lean:93-95; TGLExt/MassaTensaoPura.lean:56-61; TGLExt/O16/PeriodHeatCalibration_v3.lean:12-20; TGLExt/O16/PolarMinimalPeriod_v2.lean:104; TGLExt/Psibit.lean:106-108",
  "artefatos": [str(V), str(PJ), str(K / "ThePsionAndTheViscosity.lean"), str(K / "MassaTensaoPura.lean")],
  "refs": ["conceitual.k_e_a_tangente_acorde_tocado_02nov", "kernel.k_e_a_tangente_candidata_02nov"],
  "nota": "Separante × separador (Psibit.lean: Tomita injetivo, nada se perde; Landauer muitos-para-um, perde e cobra): a leitura de β como atrito fica do lado do separador, por volta, sem apagar o separante."}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_beta_calor_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-260:].replace("\n", " "))
assert q.returncode == 0

def append_bytes(path, add):
    b = path.read_bytes()
    add_b = add.encode("utf-8")
    if b"\r\n" in b:
        add_b = add_b.replace(b"\n", b"\r\n")
    bk = path.with_name(path.name + ".bak_" + TS)
    with open(bk, "xb") as f:
        f.write(b)
    assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(b.rstrip() + add_b)
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path)
    print(path.name, len(b), "->", path.stat().st_size)

mem = f"""

## 02/11/2026 — «β é a representação algébrica do calor?» (pergunta do operador, verbatim sha16 `{fv}`; aferição da gerência, a ratificar)

**O número corrige uma palavra [KNOWN]:** calor tem dimensão (energia); o adimensional no fenômeno é a entropia em nats (Q/k_BT) e o coeficiente de atrito. **O kernel já tem [REAL]:** β é o atrito constante (`viscosity_is_the_constant_friction`, v383: o coeficiente βg é a viscosidade); a cadeia dele «tensão → atrito → temperatura → magnetismo» está em `MassaTensaoPura` (tensão, atrito βg, temperatura κ/2π; falta o magnetismo); o balanço `boost_defect_with_derived_period` (defeito = calor − T·η·área; Clausius = defeito zero; «a parcela é o que o mantém zero», `parcela_le_beta`). **O calor dentro de β [DERIVED]:** β = α·e^{{½ nat}}; ln(β/α) = ½ exato. **Landauer:** mesmo parentesco («o custo de distinguir 1 de 0»), dimensão diferente; a leitura literal de β como calor por bit já caiu ([[rota-re-k-e-landauer-02nov]]). **Leitura proposta [ONTO, a ratificar]:** β não é o calor; é o coeficiente de atrito da fronteira, a parcela que mantém o balanço fechado a cada volta; «calor é o que o atrito cobra; β é quanto cobra por nat de travessia». Rota `conceitual.beta_e_o_calor_atrito_02nov`; contas em `work\\beta_calor_02nov\\CONTAS_BETA_E_O_CALOR_02nov.json`.
"""
append_bytes(M / "beta-e-a-regra-matriz-02out.md", mem)

atl = f"""
### 02/11/2026 — «β_TGL é a representação algébrica do calor?» (pergunta do operador; aferição da gerência c1, a ratificar) <!-- beta_e_o_calor_02nov -->

**[INPUT]** verbatim sha16 `{fv}`. **[KNOWN]** calor tem dimensão; adimensionais são a entropia em nats e o coeficiente de atrito. **[REAL, kernel]** β é o atrito constante (`ThePsionAndTheViscosity.viscosity_is_the_constant_friction`); a cadeia «tensão → atrito → temperatura → magnetismo» (operador) está registrada em `MassaTensaoPura` com três pontas como termo e sem o magnetismo; `boost_defect_with_derived_period`: Clausius é defeito zero e a parcela por volta ≤ β o mantém zero. **[DERIVED]** β = α·e^{{½ nat}}: a Meia-Nat, «a travessia», é o expoente de β. **[ONTO, a ratificar]** β não é o calor; é o coeficiente de atrito da fronteira; «calor é o que o atrito cobra; β é quanto cobra por nat de travessia». A ligação atrito → temperatura não tem termo [OPEN]. Rota `conceitual.beta_e_o_calor_atrito_02nov`.
"""
append_bytes(CEN / "memory/TGL_ATLAS.md", atl)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])

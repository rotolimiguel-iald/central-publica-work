# -*- coding: utf-8 -*-
"""02/11/2026: a leitura do operador («parcela que fecha o balanço = equilíbrio; o atrito constante gera a viscosidade, que impede o
zero absoluto … fractaliza o Um pelo decaimento do expoente») e o pedido «consegue derivar a ponte agora?»; a candidata
«A ponte do atrito» compilada no sandbox. Registro: Mapa, ACOM, memória, Atlas. Backup de bytes; nada no kernel selado."""
import datetime, hashlib, json, os, re, shutil, subprocess, sys
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V = CEN / "work/cunhagens_13out/OPERADOR_02nov_parcela_fecha_o_balanco_e_equilibrio_atrito_viscosidade_impede_o_zero_absoluto_fractaliza_o_um_verbatim.txt"
SRC = Path("C:/t/ponte02nov/APonteDoAtritoCandidata.lean")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("C:/t/ponte02nov/saida1.txt")
CAND = AQUI / "APonteDoAtritoCandidata.lean"
SAI = AQUI / "APonteDoAtritoCandidata_saida.txt"
sai = OUT.read_text(encoding="utf-8", errors="replace")
assert sai.rstrip().endswith("rc 0"), sai[-400:]
blocks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", sai, re.S)
assert len(blocks) == 12 and all(" ".join(a.split()) == "propext, Classical.choice, Quot.sound" for _, a in blocks), blocks
assert "sorry" not in sai and "error" not in sai.lower()
n_warn = sai.lower().count("warning")
shutil.copyfile(SRC, CAND); shutil.copyfile(OUT, SAI)
fv, fc = s16(V), s16(CAND)
print("verbatim", fv, "candidata", fc, "teoremas", len(blocks), "avisos", n_warn)

K = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/TGLExt")
reg = [
 {"tipo": "ROTA", "rota_id": "kernel.a_ponte_do_atrito_candidata_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "A ponte atrito → temperatura (candidata, 02/11): o que atravessa numa volta é o peso de Boltzmann do atrito à temperatura derivada",
  "pergunta": "Há termo que ligue o atrito constante βg (viscosity_is_the_constant_friction) à temperatura derivada κ/2π (reciprocal_temperature)?",
  "dados": [], "olhou_dados": False,
  "metodo": "Pedra candidata sobre Emprestimo (MassaTensaoPura): temperatura := 1/P; calorDaVolta := βg (leitura do operador, definição); entropiaDaVolta := calor/temperatura. Compilada no sandbox do kernel v405 (lake env lean), #print axioms nos 12 teoremas.",
  "resultado": "12 teoremas no trio, 0 sorry, %d aviso(s). A PONTE: transmitted β g P = exp(−βg/T) (o_atrito_lido_na_temperatura); parcela = 1 − e^{−δS} (a_parcela_e_um_menos_o_peso); parcela ≤ δS = δQ/T (a_parcela_nao_excede_a_entropia = parcela_le_beta em forma de temperatura); atravessado + cobrado = 1 em toda volta (o_balanco_fecha_a_cada_volta: o «equilíbrio das contas» do operador); resto após n voltas = peso^n (o_expoente_decai_por_volta); Σ parcela·peso^n = 1 (o_um_se_fractaliza, série geométrica: o Um é a soma das suas parcelas, mesma fração a cada volta); T = κ/2π > 0 no período fiel (o_zero_absoluto_nao_e_lido); 1 − e^{−q/T} → 1 quando T → 0⁺ (no_zero_absoluto_a_parcela_quitaria), o que parcela_nunca_quita proíbe." % n_warn,
  "veredito": "CANDIDATA_COMPILADA_NO_TRIO", "estatuto": "REAL (sandbox); ONTO (calorDaVolta := βg é a leitura do operador)", "status": "EXAMINADA",
  "defeito": "«o atrito causa T > 0» não é termo: T > 0 vem de κ > 0 (dado do boost). O balanço de Clausius da tela ótica (boost_defect_with_derived_period) é outro objeto, não ligado por termo. A identificação βg = calor da volta é definição [ONTO], não derivação.",
  "nao_refazer": "A ponte existe como identidade com uma leitura declarada; não procurar termo que derive a temperatura do atrito.",
  "proximo_passo": "Nome e versão (decisão do operador); se entrar, ligar a `Emprestimo.emprestimoDerivado` e registrar no Atlas como pedra.",
  "onde": str(CAND), "artefatos": [str(V), str(CAND), str(SAI), str(K / "MassaTensaoPura.lean"), str(K / "ThePsionAndTheViscosity.lean")],
  "refs": ["conceitual.beta_e_o_calor_atrito_02nov", "kernel.k_e_a_tangente_candidata_02nov"],
  "nota": "Primeiro artigo: «O Custo Geométrico do Zero Absoluto — Haja Luz»; a leitura «a viscosidade impede o zero absoluto» é a tese do título, agora com forma: a parcela só quitaria em T = 0, que o período fiel não lê."},
 {"tipo": "ANOTACAO", "rota_id": "conceitual.beta_e_o_calor_atrito_02nov", "dominio": "CONCEITUAL",
  "titulo": "Resposta do operador (02/11): «[parcela que mantém o balanço fechado a cada observação cíclica] = equilíbrio … o atrito constante gera a viscosidade, que impede o zero absoluto … fractaliza o Um absoluto pelo decaimento de seu expoente»",
  "resultado": "Verbatim sha16 %s. Ele fixa: equilíbrio = o fechamento das contas a cada observação cíclica (contabilidade, literal). A gerência derivou a ponte como candidata (rota kernel.a_ponte_do_atrito_candidata_02nov)." % fv,
  "estatuto": "INPUT", "artefatos": [str(V)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_ponte_atrito_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-200:].replace("\n", " "))
assert q.returncode == 0

SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-ponte-do-atrito-candidata", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "leitura_equilibrio_parcela_atrito_zero_absoluto_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «[parcela que mantém o balanço fechado a cada observação cíclica]=equilíbrio … o Atrito constante gera a viscosidade, que impede o zero absoluto, porque seu efeito é calor e isso fractaliza o Um absoluto pelo decaimento de seu expoente. Consegue derivar a ponte agora?»", "sources": [SRCD(V)]},
           {"id": "candidata_a_ponte_do_atrito_02nov", "kind": "fact", "statute": "REAL", "text": "Candidata «A ponte do atrito»: 12 teoremas, trio, 0 sorry. transmitted β g P = exp(−βg/T), T = 1/P = κ/2π; parcela = 1 − e^{−δS}, ≤ δS; Σ parcela·peso^n = 1; T > 0 no período fiel; parcela → 1 quando T → 0⁺. calorDaVolta := βg é leitura dele [ONTO]. Fora do kernel selado; nome pendente.", "sources": [SRCD(CAND)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:160], (d.get("result") or {}).get("revision"))
assert d.get("ok")

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

append_bytes(M / "beta-e-a-regra-matriz-02out.md", f"""

## 02/11/2026 — A PONTE DO ATRITO (candidata; a leitura dele: «parcela que fecha o balanço = equilíbrio»; verbatim sha16 `{fv}`)

**Leitura do operador [INPUT]:** equilíbrio = a parcela que mantém o balanço fechado a cada observação cíclica (contabilidade, literal); o atrito constante gera a viscosidade, que impede o zero absoluto, porque seu efeito é calor, e isso fractaliza o Um pelo decaimento do expoente. **Candidata [REAL no sandbox]** `work\\beta_calor_02nov\\APonteDoAtritoCandidata.lean` (sha16 `{fc}`; 12 teoremas, trio, 0 sorry; nome dele pendente): `temperatura := 1/P = κ/2π`; `calorDaVolta := βg` (leitura dele, definição [ONTO]); `entropiaDaVolta := δQ/T`. **A ponte:** `transmitted β g P = exp(−βg/T)` (`o_atrito_lido_na_temperatura`): o que atravessa numa volta é o peso de Boltzmann do atrito à temperatura derivada; parcela = 1 − e^{{−δS}} e ≤ δS (`parcela_le_beta` em forma de temperatura); atravessado + cobrado = 1 (`o_balanco_fecha_a_cada_volta`, o equilíbrio das contas); resto após n voltas = peso^n; Σ parcela·peso^n = 1 (`o_um_se_fractaliza`); T > 0 no período fiel; parcela → 1 quando T → 0⁺ (`no_zero_absoluto_a_parcela_quitaria`), proibido por `parcela_nunca_quita`. **Limites ditos:** «o atrito causa T > 0» não é termo (T > 0 vem de κ > 0); o Clausius da tela ótica (`boost_defect_with_derived_period`) não está ligado por termo; βg = calor é definição. Rota `kernel.a_ponte_do_atrito_candidata_02nov`.
""")
append_bytes(CEN / "memory/TGL_ATLAS.md", f"""
### 02/11/2026 — A PONTE DO ATRITO (candidata da gerência c1; leitura do operador «parcela que fecha o balanço = equilíbrio») <!-- ponte_do_atrito_candidata_02nov -->

**[INPUT]** verbatim sha16 `{fv}`: equilíbrio = o fechamento das contas a cada observação cíclica; o atrito constante gera a viscosidade, que impede o zero absoluto porque seu efeito é calor, e fractaliza o Um pelo decaimento do expoente. **[REAL, sandbox]** candidata sha16 `{fc}`, 12 teoremas no trio: `transmitted β g P = exp(−βg/T)` com `T = 1/P = κ/2π` (a ponte atrito → temperatura, as duas pontas numa identidade); parcela = 1 − e^{{−δS}}, δS = βg/T, parcela ≤ δS; atravessado + cobrado = 1 em toda volta; resto após n voltas = peso^n; Σ parcela·peso^n = 1 (o Um é a série geométrica das suas parcelas); T > 0 no período fiel; parcela → 1 quando T → 0⁺, que `parcela_nunca_quita` proíbe. **[ONTO]** `calorDaVolta := βg` é a leitura do operador. **[OPEN]** que o atrito cause T > 0 não é termo; o Clausius da tela ótica não está ligado por termo. Nome e versão: do operador. Rota `kernel.a_ponte_do_atrito_candidata_02nov`.
""")
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])

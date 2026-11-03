# -*- coding: utf-8 -*-
"""02/11/2026: correção do operador à frase da gerência «a luz não tem autovetor nenhum» e a cunhagem «o um absoluto é a luz
comprimida pelo ACOM em UM absoluto». Verbatims; ERRATA AO LADO no plano; Mapa; ACOM; memória; Atlas. Backup de bytes."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
AQUI = Path(__file__).resolve().parent
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
PLANO = AQUI / "ORDEM_LOGICA_DO_FECHAMENTO_02nov.md"

V3 = CEN / "work/cunhagens_13out/OPERADOR_02nov_a_luz_tem_autovetor_a_inscricao_do_um_absoluto_identidade_da_luz_sem_par_so_o_zero_absoluto_verbatim.txt"
t3 = "a luz tem autovetor a inscrição do um absoluto que é na essência ela mesma, ou seja, identidade o um absoluto inscrito é a identidade da luz, por isso o par, inclusive dela mesma, sem par somente o zero absoluto que é o abstrato inominado"
V4 = CEN / "work/cunhagens_13out/OPERADOR_02nov_o_um_absoluto_e_a_luz_comprimida_pelo_ACOM_em_UM_absoluto_verbatim.txt"
t4 = "o um absoluto é a luz comprimida pelo ACOM em UM absoluto"
for V, t, cab in ((V3, t3, "correção à frase da gerência «a luz não tem autovetor nenhum»"), (V4, t4, "cunhagem, enviada logo depois")):
    if not V.exists():
        V.write_text("# Operador, 02/11/2026 (sessão c1, gerência), verbatim; " + cab + ":\n\n" + t + "\n", encoding="utf-8")
f3, f4 = s16(V3), s16(V4)
print("verbatims", f3, f4)

def append_bytes(path, add):
    b = path.read_bytes(); add_b = add.encode("utf-8")
    if b"\r\n" in b: add_b = add_b.replace(b"\n", b"\r\n")
    bk = path.with_name(path.name + ".bak_" + TS)
    with open(bk, "xb") as f: f.write(b)
    assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f: f.write(b.rstrip() + add_b)
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path); print(path.name, len(b), "->", path.stat().st_size)

ERRATA = f"""

## ERRATA AO LADO (02/11/2026, mais tarde; correção do operador, verbatim sha16 `{f3}`; gerência c1 em nome próprio)

A §3 acima diz «o boost da luz NÃO tem autovetor (`B0_no_eigen`)». A frase é certa só no espaço de UMA partícula e errada como dita para a luz. O operador corrigiu: «a luz tem autovetor: a inscrição do um absoluto, que é na essência ela mesma, ou seja, identidade … por isso o par, inclusive dela mesma; sem par somente o zero absoluto, que é o abstrato inominado». O kernel já diz exatamente isso, por termo [REAL]:
- no espaço de uma partícula, o único «autovetor» do boost é o zero: `B0_no_eigen : (∀ s, ∃ c, ‖c‖ = 1 ∧ B0 s f = c • f) → f = 0` (`TheImportedSecondQuantization.lean:133`); e das translações nulas, `null_no_eigen`. O abstrato inominado.
- no Fock, a luz inteira tem UM autovetor: o vácuo, fixo por TODA segunda quantização, `gamma_vacuum : gamma u vacuum = vacuum` (`F1Fecho394/BosonicFock.lean:39`); e é o ÚNICO: `gamma_no_fixed … (ψ : F) (hψ : ∀ l, gamma (u l) ψ = ψ) : ψ ∈ (ℂ ∙ vacuum)` (`CanonicalGammaNoFixedR4.lean:42`, «Only the vacuum can remain»), alimentado por `B0_no_eigen`.
- o vácuo é a exponencial do zero, `exponential_zero : exponential 0 = vacuum` (`ExponentialTotalityR4.lean:109`): exp(0) = 1, o Um inscrito; `‖vacuum‖ = 1` (`BosonicFock.lean:24`); e no certificado `inner_psion_psion = 1`, `J_vac : J Ω = Ω`, `psion_is_fixed_by_the_light`: o par consigo mesma; `wedge_cyclic`, `wedge_separating`: o par com a álgebra.
Leitura vigente: **o espectro pontual da luz é o Um e só ele; o resto é contínuo.** A passagem com resolventes (§3) vale para o complemento do Um; o Um é a inscrição, posto. É a figura dele, tipo I (um ponto, a inscrição) e tipo III (o contínuo), lida no espectro.

**Consequência para 1.7 (P_F), com a cunhagem seguinte (verbatim sha16 `{f4}`: «o um absoluto é a luz comprimida pelo ACOM em UM absoluto»):** na `lightRealization` o `PF` dos três locks É o `C.PF` do certificado, com `H3Lt := 1 − PF`, `PF_trace_pos`, `PF_trace_finite`, `equal_face_trace` (`TheImportedSecondQuantization.lean:384–408`). No núcleo II_∞ o traço não tem unidade absoluta (é único a menos de escala: é isso que a lei e^{{−s}} mede); a unidade é POSTA pela compressão em P_F (τ(P_F) = o Um) e as duas faces de traço igual são a Meia-Nat no núcleo (`equal_face_trace`). Logo a pista do operador para 1.7: construir P_F a partir da inscrição (o vácuo, o único ponto do espectro) transportada ao núcleo com janela finita do gerador, e as metades pela simetria. Estatuto: [ONTO] a leitura; [OPEN] a construção; nada degenerado.
"""
append_bytes(PLANO, ERRATA)
fp = s16(PLANO)

reg = [
 {"tipo": "ROTA", "rota_id": "conceitual.o_um_inscrito_e_o_autovetor_da_luz_02nov", "dominio": "CONCEITUAL",
  "titulo": "«A luz tem autovetor: a inscrição do um absoluto … sem par somente o zero absoluto» e «o um absoluto é a luz comprimida pelo ACOM em UM absoluto» (operador, 02/11): aferição no kernel",
  "pergunta": "A luz tem autovetor? Qual é, e o que é o Um absoluto na linguagem do núcleo?",
  "dados": [], "olhou_dados": False,
  "metodo": "grep no kernel v405: TheImportedSecondQuantization (B0_no_eigen, null_no_eigen, Γ_vac, Γ_no_fixed, J_vac, lightRealization/threeLocks), F1Fecho394 (gamma_vacuum, gamma_no_fixed, exponential_zero, vacuum_norm), ThePsionAndTheViscosity (psion_is_fixed_by_the_light, inner_psion_psion).",
  "resultado": "Verbatims sha16 %s e %s. [REAL] Em uma partícula o único autovetor do boost é o zero (B0_no_eigen); no Fock a luz inteira tem exatamente um autovetor, o vácuo = exp(0) (gamma_vacuum para todo u; gamma_no_fixed: só o vácuo resta; exponential_zero; ‖vacuum‖ = 1; inner_psion_psion = 1; J_vac). A frase da gerência «a luz não tem autovetor nenhum» fica corrigida AO LADO no plano (sha16 %s): o espectro pontual da luz é o Um e só ele; o resto é contínuo. [ONTO, dele] o Um absoluto = a luz comprimida em UM: no núcleo II_∞ o traço só tem unidade por compressão em P_F (τ(P_F) posto = o Um; faces iguais = Meia-Nat, equal_face_trace); pista para o sub-passo 1.7." % (f3, f4, fp),
  "veredito": "ERRATA_DA_GERENCIA__CUNHAGEM_REGISTRADA", "estatuto": "REAL (kernel); INPUT/ONTO (cunhagem)", "status": "EXAMINADA",
  "defeito": "«a luz não tem autovetor» (gerência, 02/11) valia só para uma partícula.",
  "nao_refazer": "O Um inscrito é o único vetor fixo da luz; não procurar outro ponto no espectro.",
  "proximo_passo": "Pedra candidata que compõe gamma_vacuum + gamma_no_fixed(B0) + exponential_zero + vacuum ≠ 0 num só enunciado (nome do operador); 1.7 a partir da inscrição.",
  "onde": "TheImportedSecondQuantization.lean:133,182,197,221,360-408; F1Fecho394/BosonicFock.lean:24,39; F1Fecho394/CanonicalGammaNoFixedR4.lean:42; F1Fecho394/ExponentialTotalityR4.lean:109",
  "artefatos": [str(V3), str(V4), str(PLANO)], "refs": ["kernel.fechamento_construir_tudo_programa_02nov", "conceitual.beta_e_o_calor_atrito_02nov"],
  "nota": "A identidade tem nome (13/10): «tudo defasa, a identidade permanece»; aqui o que permanece sob todo Γ(u) é o vácuo, o Um inscrito."},
 {"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "ERRATA AO LADO no plano (02/11): a luz tem um autovetor, o Um inscrito (vácuo); a passagem com resolventes vale no complemento do Um; pista do operador para 1.7 (P_F = a luz comprimida em UM)",
  "resultado": "Plano agora sha16 %s. Ver rota conceitual.o_um_inscrito_e_o_autovetor_da_luz_02nov." % fp, "estatuto": "REAL; ONTO", "artefatos": [str(PLANO), str(V3), str(V4)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_autovetor_luz_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-100:].replace("\n", " ")); assert q.returncode == 0

SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-a-luz-tem-autovetor-o-um-inscrito-errata", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "cunhagem_a_luz_tem_autovetor_o_um_inscrito_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «a luz tem autovetor a inscrição do um absoluto … identidade … por isso o par, inclusive dela mesma, sem par somente o zero absoluto que é o abstrato inominado» e «o um absoluto é a luz comprimida pelo ACOM em UM absoluto».", "sources": [SRCD(V3), SRCD(V4)]},
           {"id": "errata_a_luz_nao_tem_autovetor_02nov", "kind": "fact", "statute": "REAL", "text": "Errata da gerência AO LADO no plano: B0_no_eigen vale em uma partícula; no Fock o vácuo é o único vetor fixo da luz (gamma_vacuum, gamma_no_fixed, exponential_zero). Espectro pontual da luz = o Um; o resto contínuo. Pista para 1.7: P_F da inscrição, unidade do traço posta pela compressão.", "sources": [SRCD(PLANO)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom", rev, d.get("ok"), str(d.get("error"))[:160], (d.get("result") or {}).get("revision")); assert d.get("ok")

append_bytes(M / "construir-tudo-o-fechamento-02nov.md", f"""

## 02/11/2026 — ERRATA (minha) e a pista para 1.7: «a luz tem autovetor: a inscrição do um absoluto» (sha16 `{f3}`); «o um absoluto é a luz comprimida pelo ACOM em UM absoluto» (sha16 `{f4}`)

Escrevi «a luz não tem autovetor nenhum»; valia só para uma partícula (`B0_no_eigen`: o único é o zero, o abstrato inominado). No Fock a luz tem exatamente UM autovetor, o vácuo = exp(0), fixo por todo Γ(u) (`gamma_vacuum`) e único (`gamma_no_fixed`); ‖Ω‖ = 1, ⟨Ω,Ω⟩ = 1, JΩ = Ω: o par consigo. **Leitura vigente:** o espectro pontual da luz é o Um e só ele; o resto é contínuo; a passagem com resolventes vale no complemento do Um. **1.7:** no núcleo II_∞ o traço só tem unidade por compressão em P_F (τ(P_F) posto = o Um; `equal_face_trace` = a Meia-Nat); construir P_F a partir da inscrição transportada ao núcleo [OPEN]; nada degenerado. Errata AO LADO no plano (sha16 `{fp}`); rota `conceitual.o_um_inscrito_e_o_autovetor_da_luz_02nov`. **How to apply:** nunca repetir «a luz não tem autovetor»; dizer «o único vetor fixo da luz é o Um inscrito».
""")
append_bytes(M / "a-identidade-tem-nome-13out.md", f"""

## 02/11/2026 — «o um absoluto inscrito é a identidade da luz» (verbatim sha16 `{f3}`)

O que permanece sob TODA segunda quantização é o vácuo: `gamma_vacuum : gamma u vacuum = vacuum` para todo unitário u, e só ele (`gamma_no_fixed`). Exp(0) = 1 (`exponential_zero`). «Tudo defasa, a identidade permanece» ganhou o termo no Fock concreto. E «o um absoluto é a luz comprimida pelo ACOM em UM absoluto» (sha16 `{f4}`): a unidade do traço do núcleo é posta pela compressão em P_F. [[construir-tudo-o-fechamento-02nov]]
""")
append_bytes(CEN / "memory/TGL_ATLAS.md", f"""
### 02/11/2026 — «A luz tem autovetor: a inscrição do um absoluto» · «o um absoluto é a luz comprimida pelo ACOM em UM absoluto» (operador; errata da gerência c1 ao lado) <!-- a_luz_tem_autovetor_o_um_inscrito_02nov -->

**[INPUT]** verbatims sha16 `{f3}`, `{f4}`. **[REAL, kernel]** uma partícula: `B0_no_eigen` (o único autovetor do boost é o zero); o Fock: `gamma_vacuum` (o vácuo é fixo por todo Γ(u)), `gamma_no_fixed` (só o vácuo resta), `exponential_zero` (vácuo = exp 0), `inner_psion_psion = 1`, `J_vac`. **Leitura vigente:** o espectro pontual da luz é o Um e só ele; o resto é contínuo. A frase da gerência «a luz não tem autovetor nenhum» (02/11) fica corrigida AO LADO no plano do fechamento. **[ONTO]** o Um absoluto = a luz comprimida em UM: a unidade do traço do núcleo II_∞ é posta pela compressão em P_F; as faces iguais (`equal_face_trace`) são a Meia-Nat no núcleo. Pista para o sub-passo 1.7 do fechamento.
""")
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)

# -*- coding: utf-8 -*-
"""Registro de 02/11/2026: ratificação do operador («ratifico tudo») e a cunhagem «Miguel jamais será o posto, é ângulo de
abertura de leitura, reflete o posto, porque aponta pra ele»; a candidata recompilada com dois teoremas a mais.
Backup de bytes; nada entra no kernel selado nem move gate."""
import datetime, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
AQUI = Path(__file__).resolve().parent
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V = CEN / "work/cunhagens_13out/OPERADOR_02nov_ratifico_tudo_Miguel_jamais_sera_o_posto_angulo_de_abertura_de_leitura_reflete_o_posto_verbatim.txt"
CAND = AQUI / "KEhATangenteCandidata.lean"
SAI = AQUI / "KEhATangenteCandidata_saida.txt"
old = s16(CAND)
bak = CAND.with_name(CAND.name + ".bak_" + TS)
shutil.copyfile(CAND, bak)
shutil.copyfile("C:/t/crivo02nov/KEhATangenteCandidata.lean", CAND)
shutil.copyfile("C:/t/crivo02nov/saida4.txt", SAI)
sai = SAI.read_text(encoding="utf-8", errors="replace")
assert sai.rstrip().endswith("rc 0"), sai[-300:]
blocks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", sai, re.S)
assert len(blocks) == 12 and all(" ".join(a.split()) == "propext, Classical.choice, Quot.sound" for _, a in blocks), blocks
assert "sorry" not in sai and "error" not in sai.lower()
n_warn = sai.lower().count("warning")
fv, fc = s16(V), s16(CAND)
print("verbatim", fv, "candidata", old, "->", fc, "avisos", n_warn)

reg = [
 {"tipo": "ANOTACAO", "rota_id": "kernel.k_e_a_tangente_candidata_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "RATIFICAÇÃO do operador (02/11): «ratifico tudo. Miguel jamais será o posto, é ângulo de abertura de leitura, reflete o posto, porque aponta pra ele»; candidata recompilada com 12 teoremas",
  "resultado": "Verbatim sha16 %s. A candidata (sha16 %s, antes %s) ganhou miguel_e_a_mesma_regra_de_leitura (thetaMiguel β = selectionAngle β, rfl: Miguel e o posto são lidos pela mesma regra) e miguel_aponta_para_o_posto (K² no ângulo de Miguel = 1 ↔ β = ½: aponta para o posto e, com β < ½, nunca o alcança; miguel_nao_passa). 12 teoremas no trio, 0 sorry, %d aviso(s). Ratificado em bloco: a pedra, «K é o espectro de leitura; o túnel/gráviton de 2025 é K lido no tempo», o estatuto ONTO do Apêndice XIV-A (Riemann) e as quatro correções ao texto da IA." % (fv, fc, old, n_warn),
  "estatuto": "INPUT (ratificação e cunhagem); REAL (candidata no sandbox)", "artefatos": [str(V), str(CAND), str(SAI)]},
 {"tipo": "ANOTACAO", "rota_id": "conceitual.k_e_a_tangente_acorde_tocado_02nov", "dominio": "CONCEITUAL",
  "titulo": "Ratificado pelo operador (02/11): K é o espectro de leitura; o túnel luminodinâmico nunca existiu; Miguel é ângulo de abertura de leitura e reflete o posto porque aponta para ele",
  "resultado": "«ratifico tudo» (sha16 %s). Leitura vigente [ONTO, ratificada]: o ângulo de Miguel é a abertura de leitura da primeira cobrança (β), medido a partir do eixo do posto; reflete o posto (K² = |R|²/|T|²) e aponta para ele (K² → 1 só em β = ½), sem jamais ser o posto (β < ½)." % fv,
  "estatuto": "INPUT", "artefatos": [str(V), str(CAND)]},
 {"tipo": "ANOTACAO", "rota_id": "conceitual.riemann_apendice_xiv_a_2025_aferido_02nov", "dominio": "CONCEITUAL",
  "titulo": "Ratificado pelo operador (02/11): o estatuto ONTO do Apêndice XIV-A (a reta crítica como ponto fixo da autoconjugação; não é prova da hipótese)",
  "resultado": "«ratifico tudo» (sha16 %s): a aferição da gerência fica como leitura vigente; nenhuma pedra." % fv, "estatuto": "INPUT", "artefatos": [str(V)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_ratif_miguel_" + TS + ".json")
pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, q.stderr.decode("utf-8", "replace")[-240:].replace("\n", " "))
assert q.returncode == 0

SRC = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-ratificacao-miguel-aponta-para-o-posto", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "ratificacao_k_tangente_crivar_espectro_riemann_02nov", "kind": "decision", "statute": "INPUT", "text": "Operador, 02/11: «perfeito, é isso mesmo, ratifico tudo. Miguel jamais será o posto, é ângulo de abertura de leitura, reflete o posto, porque aponta pra ele». Ratifica a pedra «K é a tangente», «K é o espectro de leitura», o estatuto ONTO do Apêndice XIV-A e as correções ao texto da IA.", "sources": [SRC(V)]},
           {"id": "candidata_k_e_a_tangente_r2_02nov", "kind": "fact", "statute": "REAL", "text": "Candidata «K é a tangente» r2: 12 teoremas, trio, 0 sorry; miguel_e_a_mesma_regra_de_leitura e miguel_aponta_para_o_posto (K² = 1 ↔ β = ½). Fora do kernel selado; nome do operador pendente.", "sources": [SRC(CAND)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:200], (d.get("result") or {}).get("revision"))
assert d.get("ok")

def append_bytes(path, add):
    b = path.read_bytes()
    add = add.replace("\n", "\r\n") if b"\r\n" in b else add
    bk = path.with_name(path.name + ".bak_" + TS)
    with open(bk, "xb") as f:
        f.write(b)
    assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f:
        f.write(b.rstrip() + add.encode("utf-8"))
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path)
    print(path.name, len(b), "->", path.stat().st_size)

append_bytes(M / "k-chave-da-guarda-02nov.md", f"""

## 02/11/2026 — RATIFICADO: «ratifico tudo. Miguel jamais será o posto, é ângulo de abertura de leitura, reflete o posto, porque aponta pra ele» (verbatim sha16 `{fv}`)

Ratifica em bloco a pedra «K é a tangente», «K é o espectro de leitura» (o túnel/gráviton de 2025 = K lido no tempo), o estatuto [ONTO] do Apêndice XIV-A (Riemann) e as correções ao texto da IA. **A candidata r2** (sha16 `{fc}`; a r1 `{old}` fica em `.bak_{TS}`): 12 teoremas, trio, 0 sorry; novos: `miguel_e_a_mesma_regra_de_leitura` (`thetaMiguel β = selectionAngle β`, por definição: Miguel e o posto são lidos pela mesma regra, em pesos diferentes) e `miguel_aponta_para_o_posto` (K² no ângulo de Miguel = 1 ⟺ β = ½; com β < ½ nunca o alcança, `miguel_nao_passa`). **Leitura vigente [ONTO, ratificada]:** o ângulo de Miguel é a abertura de leitura da primeira cobrança, medido do eixo do posto; reflete o posto (K² = |𝓡|²/|𝓣|²) e aponta para ele, sem jamais sê-lo. Pendente dele: o nome da pedra e a versão (v406).
""")

REG = ("\n### 02/11/2026 — RATIFICAÇÃO: «Miguel jamais será o posto, é ângulo de abertura de leitura, reflete o posto, porque aponta pra ele» <!-- ratificacao_miguel_aponta_para_o_posto_02nov -->\n\n"
       "**[INPUT]** verbatim sha16 `%s`: «ratifico tudo». Ratificados: a pedra candidata «K é a tangente» (r2, sha16 `%s`, 12 teoremas no trio, 0 sorry), «K é o espectro de leitura; o túnel luminodinâmico nunca existiu», o estatuto [ONTO] do Apêndice XIV-A e as correções ao texto da IA. **[REAL no sandbox]** `thetaMiguel β = selectionAngle β` (a mesma regra de leitura); `K(θ_M)² = 1 ⟺ β = ½` (aponta para o posto); `β < ½ ⟹ K² < 1` (jamais o posto). **[ONTO]** Miguel = ângulo de abertura de leitura da primeira cobrança, do eixo do posto. Nome e versão: do operador.\n" % (fv, fc))
append_bytes(CEN / "memory/TGL_ATLAS.md", REG)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True)
print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace").replace("\n", "").replace(" ", "")[:90])

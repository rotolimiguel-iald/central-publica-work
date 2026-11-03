# -*- coding: utf-8 -*-
"""02/11/2026: candidata «o Um inscrito é o autovetor da luz» compilada no sandbox v405; cópia em work, Mapa, ACOM, memória."""
import datetime, hashlib, json, os, re, shutil, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
AQUI = Path(__file__).resolve().parent
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
SRC = Path("C:/t/ponte02nov/OUmInscritoCandidata.lean"); OUT = Path("C:/t/ponte02nov/saida_um_inscrito_1.txt")
CAND = AQUI / "OUmInscritoCandidata.lean"; SAI = AQUI / "OUmInscritoCandidata_saida.txt"
sai = OUT.read_text(encoding="utf-8", errors="replace")
assert sai.rstrip().endswith("rc 0"), sai[-300:]
blocks = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", sai, re.S)
assert len(blocks) == 7 and all(" ".join(a.split()) == "propext, Classical.choice, Quot.sound" for _, a in blocks), blocks
assert "sorry" not in sai and "error" not in sai.lower() and "warning" not in sai.lower()
shutil.copyfile(SRC, CAND); shutil.copyfile(OUT, SAI)
fc = s16(CAND); print("candidata", fc, "teoremas", len(blocks))

reg = [{"tipo": "ANOTACAO", "rota_id": "conceitual.o_um_inscrito_e_o_autovetor_da_luz_02nov", "dominio": "CONCEITUAL",
  "titulo": "Candidata compilada (02/11): «a luz tem autovetor: o Um inscrito» — 7 teoremas no trio, 0 sorry, 0 aviso",
  "resultado": "sha16 %s (%s). a_luz_fixa_o_um (gamma u vacuum = vacuum, ∀ u); o_um_e_o_unico_fixo_da_luz (fixo por Γ(B0 s) ⟹ na reta do vácuo); o_um_inscrito_e_a_exponencial_do_zero (exponential 0 = vacuum); o_um_nao_e_o_zero; o_par_consigo (⟨Ω,Ω⟩ = 1); na_particula_so_o_zero (B0_no_eigen); a_luz_tem_autovetor_o_um_inscrito (composto). Sobre o Fock bosônico canônico concreto (F1Rede.BosonicFock), sem hipótese: todas as entradas são teoremas do kernel (gamma_vacuum, gamma_no_fixed, exponential_zero, vacuum_norm, B0_*). Fora do kernel selado; nome do operador pendente." % (fc, str(CAND)),
  "estatuto": "REAL (sandbox v405)", "artefatos": [str(CAND), str(SAI)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_cand_um_inscrito_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-90:].replace("\n", " ")); assert q.returncode == 0

SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-candidata-o-um-inscrito-autovetor-da-luz", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "candidata_o_um_inscrito_autovetor_da_luz_02nov", "kind": "fact", "statute": "REAL", "text": "Candidata «a luz tem autovetor: o Um inscrito» (sha16 %s): 7 teoremas, trio, 0 sorry, sobre o Fock bosônico canônico concreto, sem hipótese. Fora do kernel selado; nome do operador pendente." % fc, "sources": [SRCD(CAND)]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom", rev, d.get("ok"), str(d.get("error"))[:120], (d.get("result") or {}).get("revision")); assert d.get("ok")

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
append_bytes(M / "construir-tudo-o-fechamento-02nov.md", f"""

**02/11/2026, mais tarde — candidata «a luz tem autovetor: o Um inscrito» [REAL no sandbox]:** `work\\fechamento_02nov\\OUmInscritoCandidata.lean` (sha16 `{fc}`), 7 teoremas no trio, 0 sorry, 0 aviso, sobre o Fock concreto e sem hipótese (`a_luz_fixa_o_um`, `o_um_e_o_unico_fixo_da_luz`, `o_um_inscrito_e_a_exponencial_do_zero`, `o_um_nao_e_o_zero`, `o_par_consigo`, `na_particula_so_o_zero`, `a_luz_tem_autovetor_o_um_inscrito`). Nome do operador pendente; candidatas do dia à espera de nome e versão: KEhATangente, APonteDoAtrito, OUmInscrito (+ as anteriores).
""")
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)

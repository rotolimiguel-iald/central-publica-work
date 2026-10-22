# -*- coding: utf-8 -*-
"""patch de construcao (R3.4): ../montar_sandbox.py da R3.3 -> R3.4. A producao esta em B3 (v392) e o Nos em v393: o 'Nos real v391' e o manifesto B2 da R3.3 nao existem mais nos
caminhos reais. A R3.4 os reconstroi de COPIAS DE BYTES conferidas contra o SANDBOX_MANIFEST da R3.2/R3.3: o Nos v391 da custodia (the_boundary_BACKUPS/um_v391_*) e o manifesto B2
(o .bak_B3 da producao); o b1 (a copia que pina o Nos REAL) passa a ser derivado da producao ATUAL re-pinada para o Nos real v393."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "montar_sandbox.py"
t = P.read_text(encoding="utf-8")


def sub(old, new):
    global t
    assert t.count(old) == 1, (t.count(old), old[:110])
    t = t.replace(old, new)


sub('"""montar_sandbox.py (R3.2, 13/10/2026) -- R3.2:', '"""montar_sandbox.py (R3.4, 19/10/2026) -- R3.4: o sandbox da R3.3 reconstruido a partir de COPIAS DE BYTES (a producao esta em B3/v392 e o Nos em v393; o Nos v391 real e o manifesto B2 da\nR3.3 nao existem mais nos caminhos reais): nos/ = o Nos v391 da custodia (the_boundary_BACKUPS/um_v391_*), b2/ = o manifesto B2 (o .bak_B3 da producao) re-apontado para nos/, ambos conferidos\ncontra o SANDBOX_MANIFEST da R3.2 (mesmos sha256); b1/ = a producao ATUAL (codigo e fontes) com o manifesto re-pinado para o Nos REAL v393 (JA_SINCRONIZADA em v393); nos_v392/ sintetico e fx/\ncomo na R3.3. R3.2:')
sub('PROD = Path("C:/IALD/Bancada_Um")\n', 'PROD = Path("C:/IALD/Bancada_Um")\nCUSTODIA_V391 = Path("C:/IALD/Artigo/the_boundary_BACKUPS/um_v391_8e7b9927ceae64b8")\nB2_BACKUP = PROD / "canonical_contracts.json.bak_B3_20261013_184916"\nSBM_R32 = Path(__file__).resolve().parent.parent / "R3_2" / "evidencias_sandbox" / "SANDBOX_MANIFEST_R3_2.json"\n')
sub('rec = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.2 (13/10/2026)",', 'rec = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.4 (19/10/2026)",')

# --- a leitura do 'Nos v391' e do manifesto B2: das copias de bytes
sub('''man_raw = (PROD / "canonical_contracts.json").read_bytes()
man = json.loads(man_raw)
assert Path(man["canonical"]["script"]["path"]) == NOS / "um.py" and Path(man["canonical"]["seal"]["path"]) == NOS / "um_absoluto_selo.json", man["canonical"]
''', '''SBM0 = json.loads(SBM_R32.read_bytes())      # o sandbox da R3.2/R3.3: o que a reconstrucao tem de reproduzir
man_raw = B2_BACKUP.read_bytes()             # o manifesto B2 (o backup que a B3 gravou)
assert sha(man_raw) == SBM0["manifesto_producao_sha256"], "o backup B2 da producao nao e o manifesto B2 da R3.2"
man = json.loads(man_raw)
assert Path(man["canonical"]["script"]["path"]) == NOS / "um.py" and Path(man["canonical"]["seal"]["path"]) == NOS / "um_absoluto_selo.json", man["canonical"]
man_prod_raw = (PROD / "canonical_contracts.json").read_bytes()      # o manifesto ATUAL da producao (B3): so lido; deriva o b1
man_prod = json.loads(man_prod_raw)
''')
sub('''um = (NOS / "um.py").read_bytes()
selo_raw = (NOS / "um_absoluto_selo.json").read_bytes()
selo = json.loads(selo_raw)
core = (NOS / "um_absoluto.json").read_bytes()
kman_raw = (NOS / "tgl_kernel_proof_manifest.json").read_bytes()
''', '''um = (CUSTODIA_V391 / "um.py").read_bytes()
selo_raw = (CUSTODIA_V391 / "um_absoluto_selo.json").read_bytes()
selo = json.loads(selo_raw)
core = (CUSTODIA_V391 / "um_absoluto.json").read_bytes()
kman_raw = (CUSTODIA_V391 / "Lean" / "tgl_kernel_proof_manifest.json").read_bytes()
for k_, b_ in (("um_py", um), ("selo", selo_raw), ("core", core), ("kernel_manifest", kman_raw)):
    assert sha(b_) == SBM0["nos"][k_]["sha256"] and len(b_) == SBM0["nos"][k_]["bytes"], "o Nos v391 da custodia (%s) nao e o da R3.2" % k_
''')

# --- b1: derivado da producao ATUAL, re-pinado para o Nos REAL v393
sub('''rec["b1"].append(gravar_novo(RAIZ / "b1" / "canonical_contracts.json", man_raw))
rec["b2"].append(gravar_novo(RAIZ / "b2" / "canonical_contracts.json", man2_raw))
for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
    assert ".." not in Path(e["path"]).parts and not Path(e["path"]).is_absolute(), e["path"]
    raw = (PROD / e["path"]).read_bytes()
    if sha(raw) != e["sha256"] or len(raw) != e["bytes"]:
        raise SystemExit("PIN MISMATCH na producao: " + e["path"])
    rec["b1"].append(gravar_novo(RAIZ / "b1" / e["path"], raw))
    rec["b2"].append(gravar_novo(RAIZ / "b2" / e["path"], raw))
''', '''# b1: a copia que pina o Nos REAL. Na R3.3 era a producao B2 com o Nos v391; agora e a producao ATUAL (B3, codigo e fontes lidos e conferidos) com o manifesto re-pinado para o Nos
# REAL v393 (so canonical.version/script/seal mudam; deployment_id marcado). Serve ao ensaio pre_selo contra o Nos real e aos controles das guardas.
nos_real = {n_: (NOS / n_).read_bytes() for n_ in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json")}
selo_real = json.loads(nos_real["um_absoluto_selo.json"])
assert selo_real["sha256"]["um.py"] == sha(nos_real["um.py"]) and selo_real["sha256"]["tgl_kernel_proof_manifest.json"] == sha(nos_real["tgl_kernel_proof_manifest.json"]), "o selo real nao pina o Nos real"
man1 = json.loads(man_prod_raw)
man1["canonical"] = dict(version=selo_real["um_version"],
                         script=dict(path=str(NOS / "um.py"), bytes=len(nos_real["um.py"]), sha256=sha(nos_real["um.py"])),
                         seal=dict(path=str(NOS / "um_absoluto_selo.json"), bytes=len(nos_real["um_absoluto_selo.json"]), sha256=sha(nos_real["um_absoluto_selo.json"])))
man1["deployment_id"] = "B3-SANDBOX-b1-" + selo_real["um_version"] + "-R1"
man1["sandbox_R3_4"] = ("copia de ensaio (19/10/2026): a producao B3 (%s) com canonical re-pinado para o Nos REAL %s; codigo e fontes iguais aos da producao" % (sha(man_prod_raw)[:16], selo_real["um_version"]))
man1_raw = json.dumps(man1, ensure_ascii=False, indent=1).encode("utf-8")
rec["nos_real"] = dict(versao=selo_real["um_version"], um_py=dict(sha256=sha(nos_real["um.py"]), bytes=len(nos_real["um.py"])), selo=dict(sha256=sha(nos_real["um_absoluto_selo.json"]), bytes=len(nos_real["um_absoluto_selo.json"])),
                       core=dict(sha256=sha(nos_real["um_absoluto.json"]), bytes=len(nos_real["um_absoluto.json"])),
                       kernel_manifest=dict(sha256=sha(nos_real["tgl_kernel_proof_manifest.json"]), bytes=len(nos_real["tgl_kernel_proof_manifest.json"])),
                       kernel=dict(raiz_sha256=json.loads(nos_real["tgl_kernel_proof_manifest.json"])["formal_files_sha256"]["TGLExt.lean"]))
rec["b1"].append(gravar_novo(RAIZ / "b1" / "canonical_contracts.json", man1_raw))
rec["b2"].append(gravar_novo(RAIZ / "b2" / "canonical_contracts.json", man2_raw))
for e in man_prod["code"] + [s for s in man_prod["sources"] if not Path(s["path"]).is_absolute()]:
    assert ".." not in Path(e["path"]).parts and not Path(e["path"]).is_absolute(), e["path"]
    raw = (PROD / e["path"]).read_bytes()
    if sha(raw) != e["sha256"] or len(raw) != e["bytes"]:
        raise SystemExit("PIN MISMATCH na producao: " + e["path"])
    rec["b1"].append(gravar_novo(RAIZ / "b1" / e["path"], raw))
for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
    assert ".." not in Path(e["path"]).parts and not Path(e["path"]).is_absolute(), e["path"]
    raw = (PROD / e["path"]).read_bytes()
    if sha(raw) != e["sha256"] or len(raw) != e["bytes"]:
        raise SystemExit("PIN MISMATCH (manifesto B2) na producao: " + e["path"])
    rec["b2"].append(gravar_novo(RAIZ / "b2" / e["path"], raw))
''')

# --- o fim: manifesto da producao ATUAL (para a asserção de intocada) e o nome do arquivo
sub('rec["manifesto_producao_sha256"] = sha(man_raw)\n', 'rec["manifesto_producao_sha256"] = sha(man_prod_raw)          # o manifesto ATUAL da producao (B3): so lido\nrec["manifesto_b2_origem_sha256"] = sha(man_raw)\nrec["manifesto_b1_sha256"] = sha(man1_raw)\n')
sub('p = RAIZ / "SANDBOX_MANIFEST_R3_2.json"', 'p = RAIZ / "SANDBOX_MANIFEST_R3_4.json"')
P.write_text(t, encoding="utf-8", newline="")
print("ok")

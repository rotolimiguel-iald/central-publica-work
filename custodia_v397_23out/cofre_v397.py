# -*- coding: utf-8 -*-
"""CUSTÓDIA v397 — O COFRE DA CENTRAL (23/10/2026, sessão a7, pela regra do operador de 23/10; molde: cofre_v396.py, base = o cofre v396).
Do molde: CUSTÓDIA v396 — O COFRE DA CENTRAL (22/10/2026, sessão a7, por ordem do operador; molde: cofre_v395.py, base = o cofre v395).
Ordem de 23/10 (verbatim no arquivo ORDEM, sha256 lido): «pode custodiar sempre que o handoff aparecer, como regra».
Do molde: CUSTÓDIA v395 — O COFRE DA CENTRAL (21/10/2026, sessão a7, por ordem do operador; molde: cofre_v394.py, base = o cofre v394).
Do molde: CUSTÓDIA CONJUNTA v392→v394 — O COFRE DA CENTRAL (19/10/2026, sessão a7, por ordem do operador).

Ordem (verbatim, sha256 lido do arquivo): «nova versão para custodiarmos, atualize tudo, faça comiit e push, atualize todos os
dispositovos e toda a cenrtral tambem, assim como o site e o readme, portas e conexões».

O cofre da v392 ficou pendente em 13/10 (créditos) e a v393 nunca foi custodiada; o Nós está na v394. Este script:
  1. um_unificado_v394: os artefatos selados do Nós (mesma lista do cofre v391), os stdouts v392/v393/v394, os handoffs v392/v393/v394,
     a NOTA_DE_CUSTODIA, o pilar quântico (o do cofre v391: reaproveitado pela chave; worker/spec conferidos contra o Nós), as emendas
     da irmã (v392/v394 incorporação) e a cadeia de selo v392/v393/v394 FILTRADA (abaixo);
  2. tgl_kernel_v394: os 1423 arquivos formais do tgl_kernel_proof_manifest.json, cada um conferido por sha256, + lake files;
  3. CUSTODY_MANIFEST.json nos dois, com os números LIDOS dos artefatos.
Cadeia de selo: entram os arquivos de primeiro nível e as subpastas de registro; ficam FORA (ditas no manifesto com contagem e bytes)
os ensaios/simulações/bases/tentativas/rascunhos e qualquer arquivo > 5 MB (cópias do um.py) — work\\ não vai ao git, o cofre sim.
Nada se sobrescreve: as pastas de destino não podem existir.
"""
import hashlib, json, os, re, shutil, sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
OC = CEN / "vault" / "originals_copy"
V = OC / "um_unificado_v397"
KV = OC / "tgl_kernel_v397"
V391 = OC / "um_unificado_v396"   # (nome herdado do molde: é a BASE, o cofre v396)
KV391 = OC / "tgl_kernel_v396"
CS = CEN / "work" / "cadeia_de_selo"
ORDEM = CEN / "work" / "php_e_v396_22out" / "OPERADOR_23out_custodiar_quando_o_handoff_aparecer_verbatim.txt"
LIM = 5 * 1024 * 1024
assert not V.exists() and not KV.exists(), "o cofre v397 já existe — PARAR (nada se sobrescreve)"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def copia(src, dst):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    h1, h2 = sha(src), sha(dst)
    assert h1 == h2, ("cópia diverge", src)
    return h1


selo = json.load(open(NOS / "um_absoluto_selo.json", encoding="utf-8"))
core = json.load(open(NOS / "um_absoluto.json", encoding="utf-8"))
pm = json.load(open(NOS / "tgl_kernel_proof_manifest.json", encoding="utf-8"))
m391 = json.load(open(V391 / "CUSTODY_MANIFEST.json", encoding="utf-8"))
pin = sha(NOS / "um.py")
assert pin == selo["sha256"]["um.py"] and pin.startswith("388cc3742323421c") and selo.get("um_version") == "v397", (pin[:16], selo.get("um_version"))
gate = selo["qg_closure_verdict"]
assert gate == m391["gate"], "gate != cofre v396 — PARAR"
assert selo.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED"
st = (NOS / "rodada_v397_stdout.txt").read_text(encoding="utf-8", errors="replace")
assert "9499/9499" in st, "a escada 9499/9499 não está no stdout da v397 — PARAR"
TRIO = {"propext", "Classical.choice", "Quot.sound"}
fora = [n for n, ax in pm["axiom_report"].items() if set(ax or []) - TRIO]
assert not fora, ("declarações fora do trio", fora[:5])

# 1) os artefatos do cofre (a lista do cofre v391, lida dele) + o que a conjunta acrescenta
fixos = [p.name for p in V391.iterdir() if p.is_file() and p.name not in ("CUSTODY_MANIFEST.json", "NOTA_DE_CUSTODIA.md", "HANDOFF_v392_CUSTODIA.md", "HANDOFF_v393_CUSTODIA.md", "HANDOFF_v394_CUSTODIA.md", "rodada_v392_stdout.txt", "rodada_v393_stdout.txt", "rodada_v394_stdout.txt", "HANDOFF_v395_CUSTODIA.md", "rodada_v395_stdout.txt", "HANDOFF_v396_CUSTODIA.md", "rodada_v396_stdout.txt")]
extra = ["rodada_v397_stdout.txt", "HANDOFF_v397_CUSTODIA.md"]
arts = []
for nome in sorted(fixos) + extra:
    src = NOS / nome
    assert src.is_file(), "falta no Nós: " + nome
    h = copia(src, V / nome)
    ss = selo["sha256"].get(nome)
    arts.append({"file": nome, "sha256": h, "matches_seal": (h == ss) if ss else None,
                 "estatuto": "SELADO" if ss else "DOCUMENTO (fora do hash do selo)"})
mism = [a["file"] for a in arts if a["matches_seal"] is False]
assert not mism, ("artefato difere do selo", mism)
h = copia(V391 / "NOTA_DE_CUSTODIA.md", V / "NOTA_DE_CUSTODIA.md")
arts.append({"file": "NOTA_DE_CUSTODIA.md", "sha256": h, "matches_seal": None, "estatuto": "DOCUMENTO (do cofre v396)"})

# o pilar quântico: reaproveitado pela chave desde a v386; worker e spec do cofre v396 == Nós
for n in ("pilar_quantico_spec.json", "pilar_quantico_worker.py"):
    assert sha(V391 / "quantum_pillar" / n) == sha(NOS / "quantum_pillar" / n), "pilar: %s difere do Nós" % n
n_qp = 0
for p in (V391 / "quantum_pillar").rglob("*"):
    if p.is_file():
        copia(p, V / "quantum_pillar" / p.relative_to(V391 / "quantum_pillar")); n_qp += 1
reuse = (core.get("quantum_pillar_v384") or {}).get("reuse") or {}

# emendas da irmã
em = []
for n in ("v397_incorporacao_manifesto.json",):
    if (CS / n).is_file():
        copia(CS / n, V / "emendas_e_manifestos" / n); em.append(n)

# 2) a cadeia de selo filtrada
FORA_RE = re.compile(r"^(dry_|imp_|sim_|base_|superado_|scratch$|kernel$|kb_stub|pilar_anterior|quarentena|tentativa|exame_preflight$|bancada_B3_ensaio_|delta_19out$|imp$|arvore_simulada|falso_nos$)")
cad = {"regra": "cópia de bytes dos arquivos de primeiro nível e das subpastas de registro; FORA: ensaios a seco, simulações, bases, "
                "tentativas, rascunhos, árvores simuladas e o falso Nós de teste, cópias do kernel (o kernel vai inteiro em tgl_kernel_v397) e todo arquivo > 5 MB — ficam em "
                "work\\cadeia_de_selo, fora do git", "pastas": {}}
for d in ("v397", "v397_selo"):
    src = CS / d
    if not src.is_dir():
        cad["pastas"][d] = "AUSENTE em work\\cadeia_de_selo"; continue
    ent, fora_sub, grandes = 0, {}, []
    for p in src.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(src)
        top = rel.parts[0] if len(rel.parts) > 1 else None
        if top and FORA_RE.match(top):
            fs = fora_sub.setdefault(top, [0, 0]); fs[0] += 1; fs[1] += p.stat().st_size; continue
        if any(x in ("raiz", "temp", "__pycache__", ".lake") for x in rel.parts[:-1]) or len(str(V / "cadeia_de_selo_v397" / d / rel)) > 250:
            k_ = "copias_de_teste_e_caminhos_longos"; fs = fora_sub.setdefault(k_, [0, 0]); fs[0] += 1; fs[1] += p.stat().st_size; continue
        if p.stat().st_size > LIM:
            grandes.append({"arquivo": str(rel), "bytes": p.stat().st_size, "sha256": sha(p)}); continue
        copia(p, V / "cadeia_de_selo_v397" / d / rel); ent += 1
    cad["pastas"][d] = {"arquivos_no_cofre": ent, "subpastas_fora": {k: {"arquivos": v[0], "bytes": v[1]} for k, v in sorted(fora_sub.items())},
                        "arquivos_grandes_fora": grandes}
json.dump(cad, open(V / "cadeia_de_selo_v397" / "MANIFESTO_CADEIA_DE_SELO_v397.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 3) o kernel
kfiles = pm["formal_files_sha256"]
nk = 0
for rel, hk in kfiles.items():
    src = NOS / "tgl_kernel" / rel
    assert src.is_file() and sha(src) == hk, "kernel: %s não confere com o manifesto de prova" % rel
    copia(src, KV / rel); nk += 1
for n in ("lakefile.toml", "lean-toolchain", "lake-manifest.json"):
    if (NOS / "tgl_kernel" / n).is_file() and n not in kfiles:
        copia(NOS / "tgl_kernel" / n, KV / n)
# lição da v394: o manifesto de prova também na raiz do cofre do kernel (o módulo comum dos 16 dispositivos o lê dali)
h_pm = copia(NOS / "tgl_kernel_proof_manifest.json", KV / "tgl_kernel_proof_manifest.json")
assert h_pm == selo["sha256"]["tgl_kernel_proof_manifest.json"], "o manifesto de prova não confere com o selo — PARAR"
k391 = json.load(open(KV391 / "CUSTODY_MANIFEST.json", encoding="utf-8"))
antes = {str(p.relative_to(KV391)).replace("\\", "/") for p in KV391.rglob("*.lean")}
agora = {r for r in kfiles if r.endswith(".lean")}
novos = sorted(agora - antes)
km = {"version": "v397", "data_custodia": datetime.now().strftime("%Y-%m-%d"), "formal_files": len(kfiles),
      "declaracoes_no_axiom_report": len(pm["axiom_report"]), "fora_do_trio": 0,
      "formal_source_hash": pm["formal_source_hash"], "kernel_e_derivado_do_um_py": True,
      "delta_v396_v397": {"lean_novos": len(novos), "lean_removidos": len(antes - agora),
                          "formal_files_v396": k391.get("formal_files"), "declaracoes_v396": k391.get("declaracoes_no_axiom_report")},
      "modulos_novos_v397": novos, "tgl_kernel_proof_manifest_sha256": h_pm}
json.dump(km, open(KV / "CUSTODY_MANIFEST.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 4) o manifesto do cofre
ordem_raw = open(ORDEM, "rb").read()
regs = {k: str((v or {}).get("verdict", ""))[:200] for k, v in core.items()
        if isinstance(v, dict) and re.search(r"_v397$", k)}
mv = {"version": "v397", "custodia": ["v397"],
      "ordem_do_operador": [ordem_raw.decode("utf-8")], "ordem_sha256": hashlib.sha256(ordem_raw).hexdigest(),
      "um_version_no_selo": "v397", "seal_timestamp": selo.get("timestamp"), "result_hash": selo.get("result_hash"),
      "um_py_pin": pin, "gate": gate, "gate_identico_ao_da_v396": True, "selftest": selo["fail_closed_selftest"],
      "formal_source_hash": pm["formal_source_hash"],
      "rodada": {"tipo": "COMPLETA", "escada": "9499/9499 (rodada_v397_stdout.txt)",
                 "errata_ao_lado_da_gerencia_c1_19out": "a escada conta bandeiras — declarações nomeadas, teoremas e definições — com axiomas no "
                                                         "trio; o rótulo «teoremas limpos» fica como registro de máquina",
                 "errata_da_gerencia_c1_23out": "kh_n1_cobertura_v396 passa a cobrar pisos (h2, h3, h6) e tamanho mínimo da árvore (h8); "
                                                "os cinco contratos (três da v394, o do Psibit da v395 e o da testemunha da v396) passam a ler expected_ladder = 9499; "
                                                "os vereditos anteriores não mudam"},
      "kernel": {"formal_files": len(kfiles), "declaracoes_no_axiom_report": len(pm["axiom_report"]), "fora_do_trio": 0, "lean_novos_desde_v396": len(novos)},
      "kernel_e_derivado_do_um_py": True,
      "pilar_quantico": {"reaproveitado": reuse.get("reused"), "da_rodada": reuse.get("from_run_finished"), "leitura": reuse.get("reading"),
                         "arquivos_no_cofre": n_qp},
      "registros_novos_v397": regs,
      "backup_da_versao_anterior": r"C:\IALD\Artigo\the_boundary_BACKUPS\um_v396_0a4395a89eeebbb7 (a v396 que estava no espelho; feito no passo zero da custódia do espelho)",
      "cadeia_de_selo": "work\\cadeia_de_selo v397 e v397_selo filtradas em cadeia_de_selo_v397/ (ver MANIFESTO_CADEIA_DE_SELO_v397.json)",
      "handoff": "HANDOFF_v397_CUSTODIA.md fica no Nós e neste cofre privado",
      "emendas_da_irma": em, "artifacts": arts, "mismatches": len(mism), "n_artifacts": len(arts)}
json.dump(mv, open(V / "CUSTODY_MANIFEST.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("COFRE v397: %d artefatos (0 divergentes do selo), pilar %d arquivos, emendas %d, kernel %d formais (%d .lean novos desde a v396), "
      "axiom_report %d, gate = cofre v396" % (len(arts), n_qp, len(em), nk, len(novos), len(pm["axiom_report"])))
for d, v in cad["pastas"].items():
    print("  cadeia", d, (v["arquivos_no_cofre"], len(v["subpastas_fora"]), len(v["arquivos_grandes_fora"])) if isinstance(v, dict) else v)
print("manifestos:", sha(V / "CUSTODY_MANIFEST.json")[:16], sha(KV / "CUSTODY_MANIFEST.json")[:16])

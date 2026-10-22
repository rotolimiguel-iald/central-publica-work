"""Monta AXIOMAS_PSIBIT.json a partir do dump cru do Lean (collectAxioms) e do fonte.

Só leitura das entradas; escreve AXIOMAS_PSIBIT.json e axioms_dump_raw.txt na pasta de trabalho.
Nada de hash de memória: tudo é lido dos arquivos aqui.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess

W = r"C:\IALD\Central de Patentes\work\psibit_v395"
SB = r"C:\t\k395\final"
FONTE_W = W + r"\Psibit.lean"
FONTE_SB = SB + r"\TGLExt\Psibit.lean"
DUMP = r"C:\t\k395\axioms_dump_raw.txt"
LOG = r"C:\t\k395\lake_build_psibit.log"
OLEAN = SB + r"\.lake\build\lib\lean\TGLExt\Psibit.olean"
MANIFEST = SB + r"\lake-manifest.json"

TRIO = ["propext", "Classical.choice", "Quot.sound"]


def sha(path):
    b = open(path, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    return {"sha256": h, "sha16": h[:16], "bytes": len(b)}


src_bytes = open(FONTE_W, "rb").read()
assert src_bytes == open(FONTE_SB, "rb").read(), "fonte do trabalho difere do fonte compilado no sandbox"
src = src_bytes.decode("utf-8")
src_lines = src.split("\n")

# declarações nomeadas no fonte (dentro de namespace TGLExt.Psibit)
pat = re.compile(r"^(?:@\[[^\]]*\]\s*)?(theorem|def|structure|abbrev|lemma)\s+([A-Za-z0-9_'.]+)")
nomeadas = {}
for i, ln in enumerate(src_lines, 1):
    m = pat.match(ln)
    if m:
        nomeadas["TGLExt.Psibit." + m.group(2)] = {"tipo_no_fonte": m.group(1), "linha": i}

print_axioms = re.findall(r"^#print axioms (\S+)", src, flags=re.M)

# dump cru
shutil.copyfile(DUMP, W + r"\axioms_dump_raw.txt")
rows = []
for ln in open(DUMP, encoding="utf-8"):
    ln = ln.rstrip("\n")
    if not ln.startswith("DECL|"):
        continue
    _, nome, tipo, interno, axs = ln.split("|", 4)
    axl = [a for a in axs.split(",") if a]
    rows.append({"nome": nome, "tipo": tipo, "interno": interno == "true", "axiomas": axl})

dump_names = {r["nome"] for r in rows}
faltando_no_dump = sorted(n for n in nomeadas if n not in dump_names)

decls = []
for r in rows:
    origem = "fonte" if r["nome"] in nomeadas else "gerada_pelo_Lean"
    d = {"nome": r["nome"], "tipo": r["tipo"], "origem": origem, "axiomas": r["axiomas"]}
    if r["nome"] in nomeadas:
        d["linha_no_fonte"] = nomeadas[r["nome"]]["linha"]
    decls.append(d)

uniao = sorted({a for r in rows for a in r["axiomas"]})
fora_do_trio = sorted({a for a in uniao if a not in TRIO})
por_tipo = {}
for r in rows:
    por_tipo[r["tipo"]] = por_tipo.get(r["tipo"], 0) + 1
nomeadas_por_tipo = {}
for n, info in nomeadas.items():
    nomeadas_por_tipo[info["tipo_no_fonte"]] = nomeadas_por_tipo.get(info["tipo_no_fonte"], 0) + 1

# toolchain e manifest
env = dict(os.environ)
env["PATH"] = r"C:\Users\rotol\.elan\bin;" + env.get("PATH", "")
lean_v = subprocess.run(["lean", "--version"], capture_output=True, text=True, cwd=SB, env=env).stdout.strip()
man = json.load(open(MANIFEST, encoding="utf-8"))
mathlib = [p for p in man["packages"] if p["name"] == "mathlib"][0]

# linhas-chave do log do build
log_lines = open(LOG, encoding="utf-8", errors="replace").read().split("\n")
chave = [l for l in log_lines if ("Built TGLExt.Psibit" in l) or l.startswith("Build completed") or l.startswith("real")]
erros_no_log = [l for l in log_lines if re.search(r"\berror\b", l) and "Psibit" in l]
avisos_psibit = [l for l in log_lines if "warning" in l and "TGLExt/Psibit.lean" in l]
sorry_psibit = [l for l in log_lines if "Psibit.lean" in l and "sorry" in l]

out = {
    "modulo": "TGLExt.Psibit",
    "estatuto": "PEDRA CANDIDATA da v395, compilada em SANDBOX; nada instalado; gate nao se move",
    "arquivo": {
        "caminho_trabalho": FONTE_W,
        "caminho_sandbox": FONTE_SB,
        **sha(FONTE_W),
        "linhas": src.count("\n"),
    },
    "olean_compilado": {"caminho": OLEAN, **sha(OLEAN)},
    "toolchain": lean_v,
    "mathlib": {"rev": mathlib["rev"], "inputRev": mathlib["inputRev"]},
    "kernel_base": "v394 selada (Nos um.py 972e81f22dd8cc68); sandbox C:\\t\\k394d\\final copiado (robocopy sem /PURGE, /XJ) para C:\\t\\k395\\final",
    "build": {
        "comando": "lake build +TGLExt.Psibit  (cwd C:\\t\\k395\\final)",
        "linhas_chave_do_log": chave,
        "erros_do_modulo_no_log": erros_no_log,
        "avisos_do_modulo_no_log": avisos_psibit,
        "sorry_do_modulo_no_log": sorry_psibit,
        "log_completo": LOG,
    },
    "resumo": {
        "declaracoes_total_no_modulo": len(rows),
        "por_tipo_no_olean": por_tipo,
        "nomeadas_no_fonte": len(nomeadas),
        "nomeadas_por_tipo_no_fonte": nomeadas_por_tipo,
        "nomeadas_ausentes_do_dump": faltando_no_dump,
        "declaradas_como_axiom_no_modulo": [r["nome"] for r in rows if r["tipo"] == "axiom"],
        "usa_sorryAx": "sorryAx" in uniao,
        "uniao_dos_axiomas": uniao,
        "axiomas_fora_do_trio": fora_do_trio,
        "todas_dentro_do_trio": len(fora_do_trio) == 0,
        "print_axioms_no_fonte": print_axioms,
    },
    "historico_de_versoes": [
        {"versao": 1, "sha16": "d4014c779067e426", "bytes": 52607, "situacao": "examinada pela revisão independente (APROVADA_COM_CORRECOES)",
         "backup_de_bytes": [FONTE_W + ".bak_20261021_130122", FONTE_SB + ".bak_20261021_130122"]},
        {"versao": 2, "sha16": None, "situacao": "esta: correções do exame aplicadas (ver revisao_independente.correcoes_aplicadas)"},
    ],
    "revisao_independente": {
        "arquivo": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v395_exame\psibit\EXAME_PSIBIT.md",
        "veredito": "APROVADA_COM_CORRECOES",
        "correcoes_aplicadas": [
            "MEDIA: psibit_is_the_mode_of_the_reader deixou de ter FockCertificate como hipotese: e a composicao INCONDICIONAL (1)-(6) + bandeira v394 + observer_inverse_projection_halfnat + posto_paid_loss + leitura de Born do posto; a face do psion (inner_psion_psion, psion_is_fixed_by_the_light) esta em teorema a parte, CONDICIONAL: the_psion_face_of_the_psibit (forall L C), com a docstring dizendo que o kernel nao habita FockCertificate (TheImportedSecondQuantization l.66-67) e que o contrato conjunto da rede segue aberto (v394)",
            "BAIXA: the_orbit_is_isomorphic_to_the_psibit_code virou the_orbit_is_in_bijection_with_the_code_book: bijecao sobre o livro de codigos caracterizado de forma intrinseca (IsCode: 0<=w<=1, palavra=0<->w=0, verbo=0<->w=1), com Set.range v = UnitVec e Set.range codeAmp = {c | IsCode c}",
            "BAIXA: 'ponto fixo' marcado [ONTO]; a equacao vale em todo theta de pesos iguais (balanced_weights_iff: theta = pi/4 + k pi/2): balanced_collapse_is_half, collapseEntropy_at_balanced_weights; half_identity_is_a_fixed_point mostra o que e ponto fixo ((1/2)*1: do colapso e de toda conjugacao pela matriz-S); a entropia ln 2 nao e mais dita 'so em pi/4'",
            "BAIXA (docs): DEFINICAO_PSIBIT_PATENTE.md registra que a prosa l.272 define pelo produto mas os exemplos seguem a tabela, que a docstring de acom_mirror.py l.16-17 repete a tabela, e que a pedra segue o produto (formula l.265-270, reivindicacoes 3-4, codigo l.45)",
        ],
    },
    "composicao": {
        "incondicional": "TGLExt.Psibit.psibit_is_the_mode_of_the_reader",
        "condicional_ao_certificado": "TGLExt.Psibit.the_psion_face_of_the_psibit",
        "habitantes_de_FockCertificate_no_kernel": "nenhum exibido (TheImportedSecondQuantization l.66-67); so o construtor, TetelestaiOneObject.rescale e os montadores v394 (F1Fecho394/*Assembly*) a partir de entradas restantes",
    },
    "declaracoes": decls,
}
_pa = W + r"\print_axioms_todas_resumo.json"
if os.path.exists(_pa):
    out["print_axioms_todas_as_declaracoes"] = json.load(open(_pa, encoding="utf-8"))
out["historico_de_versoes"][1]["sha16"] = out["arquivo"]["sha16"]
json.dump(out, open(W + r"\AXIOMAS_PSIBIT.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps(out["resumo"], ensure_ascii=False, indent=1))
print("build:", json.dumps(out["build"]["linhas_chave_do_log"], ensure_ascii=False))
print("fonte:", out["arquivo"]["sha16"], out["arquivo"]["bytes"], "bytes", out["arquivo"]["linhas"], "linhas")
print("olean:", out["olean_compilado"]["sha16"], out["olean_compilado"]["bytes"], "bytes")

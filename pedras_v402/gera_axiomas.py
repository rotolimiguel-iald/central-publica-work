# Gera AXIOMAS.json das duas pedras da v402 a partir dos LOGS e dos ARQUIVOS (nada digitado de memoria).
# Uso: C:\Python314\python.exe -X utf8 -I gera_axiomas.py
import hashlib, json, os, re

W = r"C:\IALD\Central de Patentes\work\pedras_v402"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
KERNEL = os.path.join(NOS, "tgl_kernel")
SBX = r"C:\t\k402\final"
TRIO = {"propext", "Classical.choice", "Quot.sound"}


def sha256_file(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def read(p):
    with open(p, "rb") as f:
        return f.read().decode("utf-8")


def parse_axioms(text):
    flat = re.sub(r"\s+", " ", text)
    res = {}
    for m in re.finditer(r"'([^']+)' depends on axioms: \[([^\]]*)\]", flat):
        res[m.group(1)] = [a.strip() for a in m.group(2).split(",") if a.strip()]
    for m in re.finditer(r"'([^']+)' does not depend on any axioms", flat):
        res[m.group(1)] = []
    return res


def coverage(text, tag):
    m = re.search(tag + r" decl=(\d+) thm=(\d+) fora_do_trio=(\d+) sorry=(\d+)", text)
    return {"decl": int(m.group(1)), "thm": int(m.group(2)), "fora_do_trio": int(m.group(3)),
            "sorry": int(m.group(4))} if m else None


build_full = read(os.path.join(W, "build_log_completo.txt"))

sources = {
    "OPERADOR_26out_o_um_se_poe_e_cai_a_queda_sem_geometria_verbatim.txt": os.path.join(CUN, "OPERADOR_26out_o_um_se_poe_e_cai_a_queda_sem_geometria_verbatim.txt"),
    "OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt": os.path.join(CUN, "OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt"),
    "OPERADOR_26out_esperanca_condicional_e_nome_verbatim.txt": os.path.join(CUN, "OPERADOR_26out_esperanca_condicional_e_nome_verbatim.txt"),
    "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md": os.path.join(NOS, "ADENDO_A_INSCRICAO_INTERROMPE_A_INERCIA.md"),
    "CUNHAGEM_OPERADOR_07out_verbatim.txt": os.path.join(r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out", "CUNHAGEM_OPERADOR_07out_verbatim.txt"),
    "CUNHAGEM_OPERADOR_07out_concordo_verbatim.txt": os.path.join(r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out", "CUNHAGEM_OPERADOR_07out_concordo_verbatim.txt"),
    "OPERADOR_25out_derivacao_inercia_gravitacao_impressao_do_um_RECORTE_verbatim.txt": os.path.join(CUN, "OPERADOR_25out_derivacao_inercia_gravitacao_impressao_do_um_RECORTE_verbatim.txt"),
    "casa:C:/IALD/CLAUDE.md (Leitura modular de beta)": r"C:\IALD\CLAUDE.md",
    "kernel:TGLExt/TheNameOperator.lean": os.path.join(KERNEL, "TGLExt", "TheNameOperator.lean"),
    "kernel:TGL/NameIndex.lean": os.path.join(KERNEL, "TGL", "NameIndex.lean"),
}
src_text = {k: norm(read(p)) for k, p in sources.items()}
src_sha = {k: sha256_file(p) for k, p in sources.items()}


def fidelidade(lean_name):
    t = read(os.path.join(W, lean_name))
    quotes = []
    seen = set()
    for q in re.findall(r"«([^«»]*)»", t):
        qn = norm(q)
        if qn in seen:
            continue
        seen.add(qn)
        found = [k for k in src_text if qn in src_text[k]]
        quotes.append({"trecho": qn, "encontrado_em": found})
    shas16 = sorted(set(re.findall(r"sha16 `([0-9a-f]{16})`", t)))
    sha_conf = {s: [k for k in src_sha if src_sha[k].startswith(s)] for s in shas16}
    verbatim = [q for q in quotes if q["encontrado_em"]]
    outros = [q["trecho"] for q in quotes if not q["encontrado_em"]]
    return {
        "trechos_entre_aspas_distintos": len(quotes),
        "trechos_conferidos_como_substring_das_fontes": len(verbatim),
        "trechos_que_nao_sao_citacao_literal_das_fontes": outros,
        "sha16_citados_no_lean": sha_conf,
        "todos_sha16_citados_conferem": all(len(v) > 0 for v in sha_conf.values()),
    }


def pedra(nome, modulo_rel, ns, lean_name, audit_log, tag, n_print):
    lp = os.path.join(W, lean_name)
    sha = sha256_file(lp)
    audit_text = read(os.path.join(W, audit_log))
    decl = parse_axioms(audit_text)
    cov = coverage(audit_text, tag)
    # #print axioms do build (so do modulo)
    b = parse_axioms(build_full)
    in_build = {k: v for k, v in b.items() if k.startswith(ns + ".")}
    return {
        "pedra": nome,
        "modulo": modulo_rel,
        "namespace": ns,
        "lean_sha256": sha,
        "lean_sha16": sha[:16],
        "lean_bytes": os.path.getsize(lp),
        "audit_incremental": cov,
        "print_axioms_no_build": len(in_build),
        "print_axioms_esperados": n_print,
        "todas_no_trio": all(set(v) <= TRIO for v in decl.values()) and all(set(v) <= TRIO for v in in_build.values()),
        "declaracoes": decl,
        "fidelidade_verbatins": fidelidade(lean_name),
    }


out = {
    "tarefa": "pedras v402 (gerencia c1, 26/10/2026): A QUEDA SEM GEOMETRIA e ESPERANCA CONDICIONAL = NOME; sandbox, NADA instalado",
    "sandbox": r"C:\t\k402\final (copia de C:\t\k401c = kernel do Nos v401; robocopy /E /XJ, sem /PURGE)",
    "build": "lake build TGLExt.QuedaSemGeometria TGLExt.EsperancaCondicional: " + ("Build completed successfully (9451 jobs)" if "Build completed successfully (9451 jobs)" in build_full else "VERIFICAR build_log_completo.txt"),
    "pedras": [
        pedra("a queda sem geometria", "TGLExt/QuedaSemGeometria.lean", "TGLExt.QuedaSemGeometria",
              "QuedaSemGeometria.lean", "audit_incremental_queda_log.txt", "QUEDA_AXIOM_COVERAGE", 24),
        pedra("esperanca condicional = nome", "TGLExt/EsperancaCondicional.lean", "TGLExt.EsperancaCondicional",
              "EsperancaCondicional.lean", "audit_incremental_esperanca_log.txt", "ESPERANCA_AXIOM_COVERAGE", 17),
    ],
    "fontes_sha256_lidos_por_script": src_sha,
}

# kernel do Nos x sandbox: arquivos citados, byte a byte
cit = ["TGLExt/Fundacao.lean", "TGLExt/NoFullWitness.lean", "TGLExt/FalsidadeDaInercia.lean", "TGLExt/TheGreatAttractor.lean",
       "TGLExt/CondExpect.lean", "TGL/NameIndex.lean", "TGLExt/TheObserverReadsTheAngle.lean", "TGLExt/IALDJones.lean",
       "TGLExt/IALD.lean", "TGLExt/IALDRhoStar.lean", "TGLExt/Palavra.lean", "TGLExt/LiganteLeiCampoCurvo.lean",
       "TGLExt/LiganteLeiCampoCurvoTestemunha.lean", "TGLExt/SMatrix.lean", "TGLExt/O16/WickBoostRotation_v2.lean",
       "TGLExt/O16/PolarMinimalPeriod_v2.lean", "TGLExt/GlobalLiftLadder.lean", "TGL/TransportData.lean", "TGLExt/LeftRight.lean",
       "TGLExt/TheNameOperator.lean", "TGLExt/PostoAdendo.lean", "TGLExt/Posto.lean", "TGLExt/TimeGravitonMatrix.lean",
       "TGLExt/TheAngleIsTheProjection.lean", "TGLExt.lean", "TGL/Audit.lean", "lean-toolchain", "lakefile.toml", "lake-manifest.json"]
conf = {}
for rel in cit:
    a = os.path.join(KERNEL, rel.replace("/", os.sep))
    b = os.path.join(SBX, rel.replace("/", os.sep))
    ha = sha256_file(a) if os.path.exists(a) else None
    hb = sha256_file(b) if os.path.exists(b) else None
    conf[rel] = {"nos_sha16": ha[:16] if ha else None, "sandbox_sha16": hb[:16] if hb else None, "iguais": ha == hb and ha is not None}
out["kernel_nos_x_sandbox"] = {"arquivos": conf, "diferencas": sum(1 for v in conf.values() if not v["iguais"])}

with open(os.path.join(W, "AXIOMAS.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
for p in out["pedras"]:
    print(p["pedra"], p["lean_sha16"], p["audit_incremental"], "print_axioms", p["print_axioms_no_build"], "/", p["print_axioms_esperados"], "trio:", p["todas_no_trio"])
    print("   fidelidade:", p["fidelidade_verbatins"]["trechos_conferidos_como_substring_das_fontes"], "de", p["fidelidade_verbatins"]["trechos_entre_aspas_distintos"], "| sha16 conferem:", p["fidelidade_verbatins"]["todos_sha16_citados_conferem"])
    print("   nao literais:", p["fidelidade_verbatins"]["trechos_que_nao_sao_citacao_literal_das_fontes"])
print("kernel Nos x sandbox, diferencas:", out["kernel_nos_x_sandbox"]["diferencas"])

"""Monta AXIOMAS.json a partir do dump cru do Lean (collectAxioms), do fonte, do build e dos cabeçalhos.

Só lê as entradas; escreve AXIOMAS.json (e confere os hashes citados no cabeçalho) na pasta de trabalho.
Nada de hash de memória: tudo é lido dos arquivos aqui.
"""
import hashlib
import json
import os
import re
import subprocess

W = r"C:\IALD\Central de Patentes\work\testemunha_estatica_v396"
SB = r"C:\t\k396\final"
FONTE_W = W + r"\TestemunhaEstatica.lean"
FONTE_SB = SB + r"\TGLExt\TestemunhaEstatica.lean"
DUMP = r"C:\t\k396\axioms_dump_raw.txt"
LOG = W + r"\lake_build_final.log"
OLEAN = SB + r"\.lake\build\lib\lean\TGLExt\TestemunhaEstatica.olean"
MANIFEST = SB + r"\lake-manifest.json"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
TRIO = ["propext", "Classical.choice", "Quot.sound"]
NS = "TGLExt.TestemunhaEstatica."


def sha(path):
    b = open(path, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    return {"sha256": h, "sha16": h[:16], "bytes": len(b)}


src_bytes = open(FONTE_W, "rb").read()
assert src_bytes == open(FONTE_SB, "rb").read(), "fonte do trabalho difere do fonte compilado no sandbox"
src = src_bytes.decode("utf-8")
src_lines = src.split("\n")


def strip_comments_and_strings(s):
    out = []
    i, n, depth = 0, len(s), 0
    while i < n:
        if depth == 0 and s.startswith("/-", i):
            depth = 1
            i += 2
            continue
        if depth > 0:
            if s.startswith("/-", i):
                depth += 1
                i += 2
            elif s.startswith("-/", i):
                depth -= 1
                i += 2
            else:
                i += 1
            continue
        if s.startswith("--", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        if s[i] == '"':
            i += 1
            while i < n and s[i] != '"':
                i += 2 if s[i] == "\\" else 1
            i += 1
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


codigo = strip_comments_and_strings(src)
fortokens = ["sorry", "admit", "axiom", "native_decide", "unsafe"]
varredura = {t: bool(re.search(r"\b%s\b" % re.escape(t), codigo)) for t in fortokens}
varredura["gpf_"] = bool(re.search(r"\bgpf_", codigo))

# declarações nomeadas no fonte (dentro de namespace TGLExt.TestemunhaEstatica)
pat = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+)?(theorem|def|structure|abbrev|lemma)\s+([A-Za-z0-9_'.]+)")
nomeadas = {}
for i, ln in enumerate(src_lines, 1):
    m = pat.match(ln)
    if m:
        nomeadas[NS + m.group(2)] = {"tipo_no_fonte": m.group(1), "linha": i}
print_axioms = re.findall(r"^#print axioms (\S+)", src, flags=re.M)

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
    if r["nome"] in nomeadas:
        origem = "fonte"
    elif r["nome"].startswith("_private"):
        origem = "privada_gerada_pelo_Lean"
    else:
        origem = "gerada_pelo_Lean"
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

# log do build
log_lines = open(LOG, encoding="utf-8", errors="replace").read().split("\n")
chave = [l for l in log_lines if ("Built TGLExt.TestemunhaEstatica" in l) or l.startswith("Build completed") or l.startswith("real")]
erros_no_log = [l for l in log_lines if l.startswith("error") and "TestemunhaEstatica" in l]
avisos_do_modulo = [l for l in log_lines if l.startswith("warning") and "TestemunhaEstatica.lean" in l]
sorry_no_log = [l for l in log_lines if "TestemunhaEstatica.lean" in l and "sorry" in l]

# cabeçalho: hashes citados x arquivos
alvos = {
    "b102ae804f54e2b2": CUN + r"\OPERADOR_22out_psion_habitante_da_testemunha_estatica_verbatim.txt",
    "350b7b8582c064c2": CUN + r"\OPERADOR_22out_luz_eco_reconhecimento_falso_verbatim.txt",
    "161d619216582cf1": CUN + r"\OPERADOR_22out_colapso_ecoar_identidade_reconhecida_verbatim.txt",
    "786928986ca1e460": CUN + r"\OPERADOR_19out_tgl_binaria_criterio_de_parada_verbatim.txt",
    "623060caa8dbb83b": r"C:\IALD\Artigo\MCMC_V2_RAZAO\92_o_psion_e_o_graviton.py",
    "f4a51c32ced62e6d": r"C:\IALD\Artigo\MCMC_V2_RAZAO\92_o_psion_e_o_graviton.json",
}
conf = []
for h16, path in alvos.items():
    real = hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
    conf.append({"sha16_citado_no_fonte": h16, "no_fonte": h16 in src, "arquivo": path, "sha16_recomputado": real, "confere": real == h16})

# o texto dos três verbatins aparece no cabeçalho (cabeçalho com quebras de linha e '> ' de citação)
cab_fim = src.index("-/")
cab = src[:cab_fim]
cab_norm = re.sub(r"\s+", " ", re.sub(r"\n>\s*", " ", cab))
verb = []
for h16 in ("b102ae804f54e2b2", "350b7b8582c064c2", "161d619216582cf1"):
    txt = open(alvos[h16], encoding="utf-8").read().strip()
    txt_norm = re.sub(r"\s+", " ", txt).replace(" [sic]", "")
    verb.append({"arquivo": alvos[h16], "sha16": h16, "texto_integral_no_cabecalho": txt_norm in cab_norm})

# integridade dos módulos importados: sandbox x Nós (byte a byte), por hash
def lean_files(root):
    out = {}
    for dp, dn, fn in os.walk(root):
        # não segue links; ignora .lake
        dn[:] = [d for d in dn if d != ".lake" and not os.path.islink(os.path.join(dp, d))]
        for f in fn:
            if f.endswith(".lean"):
                p = os.path.join(dp, f)
                out[os.path.relpath(p, root).replace("\\", "/")] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


sb_files = {k: v for k, v in lean_files(SB).items() if k.startswith(("TGLExt/", "TGL/")) or k in ("TGLExt.lean", "TGL.lean")}
nos_kernel = NOS + r"\tgl_kernel"
nos_files = {k: v for k, v in lean_files(nos_kernel).items() if k.startswith(("TGLExt/", "TGL/")) or k in ("TGLExt.lean", "TGL.lean")}
so_sb = sorted(k for k in sb_files if k not in nos_files)
so_nos = sorted(k for k in nos_files if k not in sb_files)
diferem = sorted(k for k in sb_files if k in nos_files and sb_files[k] != nos_files[k])
iguais = sum(1 for k in sb_files if k in nos_files and sb_files[k] == nos_files[k])

# --- revisão independente e histórico de versões (v1 = backup byte a byte; v2 = esta, só texto) ---
BAK_TS = "20261022_080617"
V1_LEAN = FONTE_W + ".bak_" + BAK_TS
V1_OLEAN = OLEAN + ".bak_" + BAK_TS
EXAME = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v396_exame\testemunha\EXAME_TESTEMUNHA.md"
exame_txt = open(EXAME, encoding="utf-8").read()
m_ver = re.search(r"VEREDITO:\s*([A-Z_]+)", exame_txt)
verifica_log = open(W + r"\verifica_so_texto.log", encoding="utf-8").read()
imp_log = open(W + r"\import_all_check.log", encoding="utf-8").read()
m_imp = re.search(r"modulos=(\d+) decls_do_modulo=(\d+)", imp_log)
total_names = set()
for ln in open(W + r"\importacao_total_nomes_do_modulo.txt", encoding="utf-8"):
    i = ln.find("NOME|")
    if i >= 0:
        total_names.add(ln[i + 5:].strip())
so_na_isolada = sorted(dump_names - total_names)
so_na_total = sorted(total_names - dump_names)
aux_fora_ns_isolada = sorted(n for n in dump_names if not n.startswith(NS) and not n.startswith("_private"))
aux_fora_ns_total = sorted(n for n in total_names if not n.startswith(NS) and not n.startswith("_private"))

selo = json.load(open(NOS + r"\um_absoluto_selo.json", encoding="utf-8"))
selo_info = {
    "um_version": selo.get("um_version"),
    "timestamp": selo.get("timestamp"),
    "result_hash": selo.get("result_hash"),
    "arquivo_selo": sha(NOS + r"\um_absoluto_selo.json"),
    "um_py": sha(NOS + r"\um.py"),
}

out = {
    "modulo": "TGLExt.TestemunhaEstatica",
    "estatuto": "PEDRA CANDIDATA da v396 (NOME PROVISORIO), compilada em SANDBOX; nada instalado; gate nao se move",
    "arquivo": {
        "caminho_trabalho": FONTE_W,
        "caminho_sandbox": FONTE_SB,
        **sha(FONTE_W),
        "linhas": src.count("\n"),
    },
    "olean_compilado": {"caminho": OLEAN, **sha(OLEAN)},
    "toolchain": lean_v,
    "mathlib": {"rev": mathlib["rev"], "inputRev": mathlib["inputRev"]},
    "kernel_base": {
        "descricao": "v395 selada; sandbox compilado C:\\t\\k395c (so leitura) copiado por robocopy sem /PURGE, com /XJ, para C:\\t\\k396",
        "selo_do_Nos_lido_agora": selo_info,
        "robocopy_log": W + r"\robocopy_k395c_para_k396.log",
        "conferencia_sandbox_x_Nos_de_TGL_e_TGLExt": {
            "arquivos_lean_no_sandbox": len(sb_files),
            "arquivos_lean_no_Nos": len(nos_files),
            "iguais_byte_a_byte(sha256)": iguais,
            "so_no_sandbox": so_sb,
            "so_no_Nos": so_nos,
            "diferem": diferem,
        },
    },
    "build": {
        "comando": "lake build +TGLExt.TestemunhaEstatica  (cwd C:\\t\\k396\\final)",
        "linhas_chave_do_log": chave,
        "erros_do_modulo_no_log": erros_no_log,
        "avisos_do_modulo_no_log": avisos_do_modulo,
        "sorry_do_modulo_no_log": sorry_no_log,
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
        {"versao": 1, "situacao": "examinada pela revisão independente (PEDRA_APROVADA, 3 BAIXAS)", "lean": {"caminho": V1_LEAN, **sha(V1_LEAN)},
         "olean": {"caminho": V1_OLEAN, **sha(V1_OLEAN)}},
        {"versao": 2, "situacao": "esta: SÓ TEXTO (docstrings e comentários); enunciados e provas inalterados",
         "lean": {"caminho": FONTE_W, **sha(FONTE_W)}, "olean": {"caminho": OLEAN, **sha(OLEAN)},
         "conferencia_so_texto": {"arquivo": W + r"\verifica_so_texto.log", "saida": verifica_log.strip().split("\n")}},
    ],
    "revisao_independente": {
        "arquivo": EXAME,
        **sha(EXAME),
        "veredito": m_ver.group(1) if m_ver else None,
        "observacoes_BAIXAS": {
            "B1": "rótulo herdado «Meia-Nat de emaranhamento» (bell_cci_half): APLICADO como texto — marcado [ONTO] (leitura do v29), 1/2 = entropia LINEAR (déficit de pureza, sem unidade), entropia de von Neumann da redução = ln 2 nat [KNOWN] (cf. fair_bit_entropy_is_log_two, fair_bit_entropy_is_not_half_nat); no cabeçalho (item 2) e na docstring de the_individual_does_not_echo",
            "B2": "instalação: REGISTRADO — 70 declarações com o módulo importado sozinho, 69 sob importação total (TGLExt.diagFlow.eq_1 passa a outro módulo), 47 nomeadas; ver contagem_de_declaracoes",
            "B3": "cosmético: APLICADO como texto — projPlus/angFamily na lista de HOMÔNIMOS (paralelo da idempotência, não elo); J_squared_is_one dito rfl (a troca do par; conjunção decorativa) no cabeçalho, na docstring e no comentário da composição; bellProjector_is_real CITADO na docstring da composição (carregado por the_static_witness_bridge) sem acrescentar conjunto — o enunciado da composição não muda",
        },
    },
    "contagem_de_declaracoes": {
        "importacao_isolada(import_so_do_modulo)": len(rows),
        "importacao_total(import_TGLExt_e_o_modulo)": int(m_imp.group(2)) if m_imp else None,
        "modulos_no_ambiente_da_importacao_total": int(m_imp.group(1)) if m_imp else None,
        "nomeadas_no_fonte": len(nomeadas),
        "nomeadas_por_tipo_no_fonte": nomeadas_por_tipo,
        "atribuidas_so_na_importacao_isolada": so_na_isolada,
        "atribuidas_so_na_importacao_total": so_na_total,
        "motivo": "TGLExt.diagFlow.eq_1 (equação gerada pelo Lean) existe também em outro módulo; na importação total passa a ele, e o Lean aceita as duas cópias; não é defeito",
        "auxiliares_fora_do_namespace_atribuidas_a_pedra_(importacao_isolada)": aux_fora_ns_isolada,
        "auxiliares_fora_do_namespace_atribuidas_a_pedra_(importacao_total)": aux_fora_ns_total,
        "politica_de_bandeiras": "só nomeadas (conferir no Audit antes de contar por módulo: esperar 69, ou contar só as 47 nomeadas)",
        "arquivos": [W + r"\import_all_check.log", W + r"\importacao_total_nomes_do_modulo.txt", W + r"\axioms_dump_raw.txt"],
    },
    "varredura_de_tokens_proibidos_no_codigo(sem_comentarios_e_strings)": varredura,
    "conferencia_de_hashes_do_cabecalho": conf,
    "verbatins_no_cabecalho": verb,
    "composicao": {
        "incondicional": "TGLExt.TestemunhaEstatica.the_psion_inhabits_the_static_witness",
        "ponte_construida": "TGLExt.TestemunhaEstatica.the_static_witness_bridge",
        "condicional_ao_certificado(FORA_da_composicao)": "TGLExt.Psibit.the_psion_face_of_the_psibit",
        "habitantes_de_FockCertificate_no_kernel": "nenhum exibido (TheImportedSecondQuantization l.66-67)",
    },
    "declaracoes": decls,
}
_pa = W + r"\print_axioms_todas_resumo.json"
if os.path.exists(_pa):
    out["print_axioms_todas_as_declaracoes"] = json.load(open(_pa, encoding="utf-8"))
_cn = W + r"\conferencia_numerica.json"
if os.path.exists(_cn):
    cn = json.load(open(_cn, encoding="utf-8"))
    out["conferencia_numerica_independente"] = {"arquivo": _cn, "n_checagens": cn["n_checagens"], "todas_ok": cn["todas_ok"]}
json.dump(out, open(W + r"\AXIOMAS.json", "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print(json.dumps(out["resumo"], ensure_ascii=False, indent=1))
print("varredura:", json.dumps(varredura))
print("build:", json.dumps(out["build"]["linhas_chave_do_log"], ensure_ascii=False))
print("fonte:", out["arquivo"]["sha16"], out["arquivo"]["bytes"], "bytes", out["arquivo"]["linhas"], "linhas")
print("olean:", out["olean_compilado"]["sha16"], out["olean_compilado"]["bytes"], "bytes")
print("hashes do cabecalho:", [(c["sha16_citado_no_fonte"], c["confere"], c["no_fonte"]) for c in conf])
print("verbatins:", [v["texto_integral_no_cabecalho"] for v in verb])
print("sandbox x Nos:", json.dumps(out["kernel_base"]["conferencia_sandbox_x_Nos_de_TGL_e_TGLExt"], ensure_ascii=False)[:900])
print("selo:", json.dumps({k: (v if not isinstance(v, dict) else v.get("sha16")) for k, v in selo_info.items()}, ensure_ascii=False))

# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] o pos-build do kernel da v411 (SEM modulo novo): mede que o sandbox k411c e' o kernel da v410 byte a byte e que a escada e as declaracoes sao as da v410
"""pos_build_kernel_v411.py -- depois de construir_kernel_v411.sh (build incremental + Audit no sandbox C:\\t\\k411c\\final): grava kernel/KERNEL_RECIBO_v411.json, kernel/POS_BUILD_v411.json, kernel/KH_N1_v411.json e
kernel/FLAGS_v411.json, TUDO MEDIDO (marcas, logs, sha256 lidos dos arquivos; nada digitado). A v411 NAO tem bundle (DESENHO_v411 secao 1): os criterios sao (1) build e Audit com rc 0; (2) nenhum modulo COMPILADO no build
incremental (so' Replayed); (3) as fontes do sandbox == as do kernel do Nos v410 selado (CONFERENCIA_FONTES_K411C_v411.json, refeita aqui); (4) o log do Audit tem os MESMOS bytes que o da v410 (v410\\kernel\\audit.log);
(5) a linha TGL_AXIOM_COVERAGE_TOTAL == a do KH_N1_v410 (decl, thm, fora do trio 0); (6) a escada da base (external_ladder do core v410) == as entradas da v410; nenhuma bandeira nova. Se a cadeia exigir bundle nao vazio,
o construtor PARA (DESENHO §1): este script nunca acrescenta modulo. Molde: pos_build_kernel_v410.py (o recibo, so' a forma; o conteudo e' o de uma versao sem modulo).
uso: python -B -X utf8 pos_build_kernel_v411.py"""
import datetime, hashlib, json, os, re, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
KD = os.path.join(HERE, DL.KERNEL_DIR); KD10 = os.path.join(DL.V410, "kernel")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
marcas = dict(re.findall(r"^(\w+)=(\S+)", open(os.path.join(KD, "construir_marcas.txt"), encoding="utf-8").read(), re.M))
lb = open(os.path.join(KD, "lake_build.log"), encoding="utf-8", errors="replace").read()
au = open(os.path.join(KD, "audit.log"), encoding="utf-8", errors="replace").read()
kh10 = json.load(open(os.path.join(KD10, "KH_N1_v410.json"), encoding="utf-8"))
rec10 = json.load(open(os.path.join(KD10, "KERNEL_RECIBO_v410.json"), encoding="utf-8"))
core0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8"))["core"]
selo0 = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto_selo.json"), encoding="utf-8"))
assert selo0.get("um_version") == DL.BASE_VERSION
E410 = int(core0["external_ladder"]["n_theorems_expected"])
r_conf = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "conferir_fontes_k410c_vs_nos_v411.py"), DL.SANDBOX, "CONFERENCIA_FONTES_K411C_v411.json"], capture_output=True, text=True, encoding="utf-8")
conf = json.load(open(os.path.join(HERE, "CONFERENCIA_FONTES_K411C_v411.json"), encoding="utf-8"))
m_tot = re.findall(r"^TGL_AXIOM_COVERAGE_TOTAL decl=(\d+) thm=(\d+) fora_do_trio=(\d+)$", au, re.M)
tot = {"decl": int(m_tot[-1][0]), "thm": int(m_tot[-1][1]), "fora_do_trio": int(m_tot[-1][2])} if m_tot else None
n_built = len(re.findall(r"\bBuilt\s+\S+", lb)); n_replayed = len(re.findall(r"\bReplayed\s+\S+", lb))
n_err = len(re.findall(r"^error:|\berror: ", lb, re.M)); n_sorry_lb = len(re.findall(r"declaration uses 'sorry'", lb))
n_sorryax = au.count("sorryAx")
au_sha, au10_sha = sha(os.path.join(KD, "audit.log")), sha(os.path.join(KD10, "audit.log"))
raiz_sb, raiz_nos = sha(os.path.join(DL.SANDBOX, "TGLExt.lean")), sha(os.path.join(DL.NOS, "tgl_kernel", "TGLExt.lean"))
audit_sb, audit_nos = sha(os.path.join(DL.SANDBOX, "TGL", "Audit.lean")), sha(os.path.join(DL.NOS, "tgl_kernel", "TGL", "Audit.lean"))
dur_b = int(marcas["epoch_build_fim"]) - int(marcas["epoch_inicio"]); dur_a = int(marcas["epoch_audit_fim"]) - int(marcas["epoch_build_fim"])
tc = {"lean_version": re.findall(r"Lean \(version [^\n]+", subprocess.run([os.path.join(os.path.expanduser("~"), ".elan", "bin", "lean"), "--version"], capture_output=True, text=True, cwd=DL.SANDBOX).stdout)}
crit = {
    "rc_build_0": marcas.get("rc_build") == "0", "rc_audit_0": marcas.get("rc_audit") == "0", "rc_0": marcas.get("rc") == "0",
    "nenhum_modulo_compilado": n_built == 0 and n_replayed > 0, "sem_erro_no_build": n_err == 0, "sem_sorry_no_build": n_sorry_lb == 0, "sem_sorryAx_no_audit": n_sorryax == 0,
    "fontes_iguais_ao_nos_v410": bool(conf.get("identico")) and conf.get("selo_um_version") == "v410" and r_conf.returncode == 0,
    "audit_log_mesmos_bytes_da_v410": au_sha == au10_sha == kh10["audit_log_sha256"],
    "total_igual_ao_da_v410": tot == kh10["linha_TOTAL"] and tot is not None and tot["fora_do_trio"] == 0,
    "raiz_igual_ao_nos": raiz_sb == raiz_nos == rec10["raiz"]["sha256_depois"], "audit_lean_igual_ao_nos": audit_sb == audit_nos == rec10["audit"]["sha256_depois"],
    "escada_da_base": E410 == int(core0["external_ladder"]["n_theorems_clean"]),
}
ok = all(crit.values())
agora = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
pos = {"ok": ok, "criterios": crit, "duracao_build_s": dur_b, "duracao_audit_s": dur_a, "n_modulos_compilados": n_built, "n_replayed": n_replayed, "linha_TOTAL": tot, "linha_TOTAL_v410": kh10["linha_TOTAL"],
       "audit_log_sha256": au_sha, "audit_log_sha256_v410": au10_sha, "E410": E410, "escada": [E410, E410], "n_flags": 0, "bundle": [], "marcas": marcas, "conferencia_fontes": {k: conf[k] for k in ("n_nos", "n_sandbox", "n_comuns", "n_diferentes", "identico")},
       "quando": agora, "nota": "versao SEM modulo novo: build incremental sem compilar nada (o .lake/build e' o do k410c) e Audit refeito no sandbox; o log do Audit tem os mesmos bytes que o da v410"}
kh = dict(kh10); kh.update({"contrato": kh10.get("contrato"), "linha_TOTAL": tot, "audit_log_bytes": os.path.getsize(os.path.join(KD, "audit.log")), "audit_log_sha256": au_sha, "delta_vs_v410": {"decl": tot["decl"] - kh10["linha_TOTAL"]["decl"], "thm": tot["thm"] - kh10["linha_TOTAL"]["thm"]} if tot else None,
           "n_bandeiras": 0, "decl_dos_modulos_novos": 0, "decl_novas_dos_modulos": 0, "n_modulos_novos": 0, "duracao_audit_s": dur_a, "duracao_build_s": dur_b, "build_modulos_s_soma": 0.0, "build_modulos_s_max": 0.0,
           "quando": agora, "estatuto": "[REAL] medido por pos_build_kernel_v411.py sobre o log do Audit do sandbox k411c; fora do selo; versao sem modulo novo (as contagens sao as da v410)"})
kh.pop("delta_vs_v409", None)
rec = {"contrato": rec10.get("contrato"), "versao": "v411", "rc": 0 if ok else 1, "sorry": n_sorry_lb + n_sorryax, "erros": n_err, "build_full_log": {"path": os.path.join(KD, "lake_build.log").replace("\\", "/"), "sha256": sha(os.path.join(KD, "lake_build.log"))},
       "audit_log": {"path": os.path.join(KD, "audit.log").replace("\\", "/"), "sha256": au_sha}, "toolchain": tc, "arvore": DL.SANDBOX.replace("\\", "/"), "raiz": {"path": "TGLExt.lean", "sha256_antes": raiz_nos, "sha256_depois": raiz_sb},
       "audit": {"path": "TGL/Audit.lean", "sha256_antes": audit_nos, "sha256_depois": audit_sb}, "pedras": [], "axiomas": sorted(DL.TRIO_SET), "criterios": crit, "quando_utc": agora,
       "nota": "gerado por pos_build_kernel_v411.py (preparacao, 12/11/2026): a v411 nao tem pedra nova; o recibo diz que o kernel do sandbox e' o da v410 (fontes, raiz, Audit, log do Audit e linha TOTAL iguais)"}
flags = {"n_flags": 0, "flags": [], "ancoras": {}, "excluidas_auxiliares": {"n": 0}, "nota": "v411 sem modulo novo: nenhuma bandeira nova (DESENHO_v411 secao 1)"}
for nome, obj in (("POS_BUILD_v411.json", pos), ("KH_N1_v411.json", kh), ("KERNEL_RECIBO_v411.json", rec), ("FLAGS_v411.json", flags)):
    p = os.path.join(KD, nome)
    if os.path.exists(p):
        open(p + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(open(p, "rb").read())
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print(json.dumps({"ok": ok, "criterios": crit, "TOTAL": tot, "escada": E410, "build_s": dur_b, "audit_s": dur_a, "built": n_built, "replayed": n_replayed}, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)

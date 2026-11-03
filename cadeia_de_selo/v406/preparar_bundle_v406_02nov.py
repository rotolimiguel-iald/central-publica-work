# -*- coding: utf-8 -*-
"""v406 — passo «gerar» do bundle no sandbox C:\\t\\k406c\\final (gerência c1, 02/11/2026).
Copia os 300 módulos da bancada JÁ NORMALIZADOS pela integração R3 (imports com prefixo do kernel, blocos #eval removidos; cada
fonte original conferida por sha256 contra o recibo da bancada, ver integracao_R3_20261102_192452/MANIFEST.json) + a candidata
CanonicalFullTGLWitnessR1 para TGLExt/F1Fecho394/ do sandbox novo; acrescenta à raiz TGLExt.lean os DOIS imports (ROOT_SUFFIX);
escreve kernel_modulos_novos_v406.json e BUNDLE_v406.json (sha256 de cada módulo, fonte, status); gera construir_kernel_v406.sh
(molde v405: lake build incremental + Audit, com marcas de tempo) e o lançador sem janela. Nada toca o Nós nem k405c (só leitura)."""
import hashlib, json, os, re, shutil, sys, datetime
from pathlib import Path
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
PK6 = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v406")
K5 = Path(r"C:\t\k405c\final\TGLExt\F1Fecho394")
K6 = Path(r"C:\t\k406c\final"); K6F = K6 / "TGLExt" / "F1Fecho394"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel")
MAN = Path(r"C:\IALD\Central de Patentes\work\fechamento_02nov\integracao_R3_20261102_192452\MANIFEST.json")
TW = Path(r"C:\IALD\Central de Patentes\work\fechamento_02nov\CanonicalFullTGLWitnessR1.lean")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
man = json.loads(MAN.read_text(encoding="utf-8"))
novos = sorted(n for n, e in man.items() if e["status"] in ("novo_compilado", "novo_gravado", "novo_ja_gravado"))
assert len(novos) == 300, len(novos)
# raiz: a do Nós v405 + ROOT_SUFFIX
raiz_nos = (NOS / "TGLExt.lean").read_text(encoding="utf-8", newline="")
raiz_k6 = (K6 / "TGLExt.lean").read_text(encoding="utf-8", newline="")
assert raiz_k6 == raiz_nos, "a raiz do k406c nao e a do Nos"
nl = "\r\n" if "\r\n" in raiz_nos else "\n"
ROOT_SUFFIX = nl.join(["import TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1", "import TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1"]) + nl
assert "CanonicalFockModularCoreInputR1" not in raiz_nos and "CanonicalFullTGLWitnessR1" not in raiz_nos
existentes_k6 = {f.stem for f in K6F.glob("*.lean")}
assert len(existentes_k6) == 184 and not (set(novos) & existentes_k6), (len(existentes_k6), set(novos) & existentes_k6)
bundle = []
for n in novos:
    src = K5 / (n + ".lean"); dst = K6F / (n + ".lean")
    assert src.exists() and not dst.exists(), n
    shutil.copyfile(src, dst)
    e = man[n]
    bundle.append({"rel": "TGLExt/F1Fecho394/%s.lean" % n, "sha256": sha(dst), "fonte_bancada": e["fonte"], "sha256_fonte_bancada": e["sha256_fonte"],
                   "n_eval_removidos": e.get("n_eval_removidos", 0), "status_integracao": e["status"], "olean_sha256_integracao": e.get("olean_sha256")})
assert TW.exists() and not (K6F / TW.name).exists()
shutil.copyfile(TW, K6F / TW.name)
bundle.append({"rel": "TGLExt/F1Fecho394/CanonicalFullTGLWitnessR1.lean", "sha256": sha(K6F / TW.name), "fonte_bancada": None, "sha256_fonte_bancada": None, "n_eval_removidos": 0, "status_integracao": "candidata_da_gerencia_02nov", "olean_sha256_integracao": None})
bak = K6 / ("TGLExt.lean.bak_" + TS); bak.write_bytes((K6 / "TGLExt.lean").read_bytes())
(K6 / "TGLExt.lean").write_text(raiz_nos + ROOT_SUFFIX, encoding="utf-8", newline="")
assert (K6 / "TGLExt.lean").read_text(encoding="utf-8", newline="") == raiz_nos + ROOT_SUFFIX
rels = [b["rel"] for b in bundle]
(PK6 / "kernel_modulos_novos_v406.json").write_text(json.dumps({"novos": rels, "n": len(rels), "root_suffix": ROOT_SUFFIX, "gerado": TS}, ensure_ascii=False, indent=1), encoding="utf-8")
(PK6 / "BUNDLE_v406.json").write_text(json.dumps({"contrato": "BUNDLE_v406", "gerado": TS, "n": len(bundle), "origem_integracao": str(MAN), "sha256_manifesto_integracao": sha(MAN), "root_suffix": ROOT_SUFFIX, "modulos": bundle}, ensure_ascii=False, indent=1), encoding="utf-8")
(PK6 / "kernel").mkdir(exist_ok=True)
sh = f"""#!/bin/sh
# Constroi o kernel do SANDBOX da v406 (C:\\t\\k406c\\final; nunca o do Nos): `lake build` INCREMENTAL (a v405 selada ja' esta compilada em .lake/build,
# copiada do Nos; os 301 modulos novos sao os unicos a compilar a frio) e depois o Audit. Molde: construir_kernel_v405.sh. Marcas de tempo em kernel/construir_marcas.txt.
K="/c/t/k406c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v406/kernel"
mkdir -p "$D"
for f in lake_build.log audit.log build_full.log; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
cd "$K" || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$D/construir_marcas.txt"
echo "epoch_inicio=$(date +%s)" >> "$D/construir_marcas.txt"
/c/Users/rotol/.elan/bin/lake build > "$D/lake_build.log" 2>&1; rb=$?
echo "rc_build=$rb $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_build_fim=$(date +%s)" >> "$D/construir_marcas.txt"
/c/Users/rotol/.elan/bin/lake env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
echo "rc_audit=$ra $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"
"""
(PK6 / "construir_kernel_v406.sh").write_text(sh, encoding="utf-8", newline="\n")
# lancador sem janela (Agendador): pythonw -> sh
Path(r"C:\t\k406c\run_build.py").write_text(
    "import subprocess, sys\n"
    "sh = r'C:\\Program Files\\Git\\bin\\sh.exe'\n"
    "scr = r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v406\\construir_kernel_v406.sh'\n"
    "out = open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v406\\kernel\\construir_stdout.log', 'ab')\n"
    "r = subprocess.run([sh, scr], stdout=out, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, cwd=r'C:\\t\\k406c\\final', creationflags=subprocess.CREATE_NO_WINDOW | subprocess.CREATE_NEW_PROCESS_GROUP)\n"
    "open(r'C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v406\\kernel\\construir_rc.txt', 'w').write(str(r.returncode))\n", encoding="utf-8")
print("bundle", len(bundle), "modulos; sandbox F1Fecho394:", len(list(K6F.glob("*.lean"))), "; raiz +2 imports; sh e lancador gravados")

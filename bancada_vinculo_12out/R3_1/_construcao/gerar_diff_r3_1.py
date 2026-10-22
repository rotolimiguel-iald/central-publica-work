# -*- coding: utf-8 -*-
"""gerar_diff_r3_1.py (R3.1, 13/10/2026) -- gera R3_1/DIFF_R3_R3_1.patch (os .py da R3 para a R3.1, com renomes detectados) e o CONFERE:
copia os .py da R3 para <raiz>/diff/check, aplica o patch com git apply e exige bytes identicos aos da R3.1. Tudo dentro de <raiz> (C:/t/vb*),
exceto o patch e o recibo da verificacao, gravados em R3_1. uso: gerar_diff_r3_1.py <raiz C:/t/vb*>"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, os, re, shutil, subprocess
from pathlib import Path

RAIZ = Path(sys.argv[1])
assert RAIZ.parent == Path("C:/t") and re.match(r"^vb[0-9A-Za-z_-]*$", RAIZ.name)
AQUI = Path(__file__).resolve().parent.parent
R3 = AQUI.parent / "R3"
PARES = [("sincronizar_bancada.py", "sincronizar_bancada.py"), ("montar_sandbox.py", "montar_sandbox.py"),
         ("controles_negativos_r3.py", "controles_negativos_r3_1.py"), ("medir_pinos_r3.py", "medir_pinos_r3_1.py")]
D = RAIZ / "diff"
if D.exists():
    shutil.rmtree(D)
(D / "a").mkdir(parents=True)
(D / "b").mkdir(parents=True)
for x, y in PARES:
    shutil.copyfile(R3 / x, D / "a" / x)
    shutil.copyfile(AQUI / y, D / "b" / y)


def sha(b):
    return hashlib.sha256(b).hexdigest()


r = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", "diff", "--no-index", "-M", "--binary", "a", "b"], cwd=str(D), capture_output=True)
assert r.returncode in (0, 1), r.stderr.decode("utf-8", "replace")
patch = r.stdout
patch = re.sub(rb"(?m)^(diff --git )a/[ab]/(\S+) b/[ab]/(\S+)$", rb"\1a/\2 b/\3", patch)   # tambem os arquivos novos/apagados (a/a/x b/a/x)
patch = re.sub(rb"(?m)^--- a/a/", b"--- a/", patch)
patch = re.sub(rb"(?m)^\+\+\+ b/b/", b"+++ b/", patch)
patch = re.sub(rb"(?m)^rename from a/", b"rename from ", patch)
patch = re.sub(rb"(?m)^rename to b/", b"rename to ", patch)
destino = AQUI / "DIFF_R3_R3_1.patch"
tmp = destino.with_name(destino.name + ".tmp")
tmp.write_bytes(patch)
assert tmp.read_bytes() == patch
tmp.replace(destino)
CK = D / "check"
CK.mkdir()
for x, _ in PARES:
    shutil.copyfile(R3 / x, CK / x)
subprocess.run(["git", "init", "-q"], cwd=str(CK), check=True)
ap = subprocess.run(["git", "-c", "core.autocrlf=false", "apply", "--whitespace=nowarn", str(destino)], cwd=str(CK), capture_output=True)
iguais = {}
for _, y in PARES:
    p = CK / y
    iguais[y] = p.is_file() and p.read_bytes() == (AQUI / y).read_bytes()
res = dict(patch=dict(path=str(destino), sha256=sha(patch), bytes=len(patch)), git_apply_rc=ap.returncode,
           git_apply_stderr=ap.stderr.decode("utf-8", "replace")[-500:], reproduz_bit_a_bit=all(iguais.values()) and ap.returncode == 0, por_arquivo=iguais,
           pares=[dict(de="R3/" + x, para="R3_1/" + y, sha256_de=sha((R3 / x).read_bytes()), sha256_para=sha((AQUI / y).read_bytes())) for x, y in PARES],
           nota="git apply sobre uma copia dos .py da R3 em %s; nada fora do sandbox alem deste recibo e do patch" % CK)
(AQUI / "VERIFICACAO_DIFF_R3_1.json").write_bytes(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps({k: res[k] for k in ("git_apply_rc", "reproduz_bit_a_bit", "por_arquivo")}), res["patch"]["sha256"][:16], res["patch"]["bytes"])

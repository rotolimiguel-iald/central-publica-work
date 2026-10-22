# -*- coding: utf-8 -*-
"""gerar_diff_r3_5.py (R3.5, 19/10/2026) -- gera R3_5/DIFF_R3_4_R3_5.patch (os 3 .py que a R3.5 muda, da R3.4 para a R3.5, com o renome do script de controles detectado) e o CONFERE: copia os .py da R3.4 para
<raiz>/diff/check, aplica o patch com `git -c core.autocrlf=false apply` e exige bytes identicos aos da R3.5. Gera tambem R3_5/DIFF_PASSO10_R3_5.patch (o chain_pos_rito_v394.sh e o helper b3_recibo_v394.py: do backup de
bytes feito antes ate o arquivo re-derivado), conferido do mesmo modo. Tudo dentro de <raiz> (C:/t/vb*), exceto os patches e o recibo de verificacao, gravados em R3_5.
uso: python -I -B -X utf8 gerar_diff_r3_5.py <raiz C:/t/vb*> [<backup do chain> <backup do helper>]   (os backups, se dados, sao os .bak_<stamp> do derivar_passo10_r35.py)"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, re, shutil, subprocess
from pathlib import Path

RAIZ = Path(sys.argv[1])
assert RAIZ.parent == Path("C:/t") and re.match(r"^vb[0-9A-Za-z_-]*$", RAIZ.name)
AQUI = Path(__file__).resolve().parent.parent
R34 = AQUI.parent / "R3_4"
PK_POS = AQUI.parent.parent / "cadeia_de_selo" / "v394" / "pos_rito"
PARES = [("sincronizar_bancada.py", "sincronizar_bancada.py"), ("montar_sandbox.py", "montar_sandbox.py"), ("controles_negativos_r3_4.py", "controles_negativos_r3_5.py")]
D = RAIZ / "diff"
if D.exists():
    shutil.rmtree(D)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def diff_git(a_dir, b_dir, pares, destino):
    for x, y in pares:
        (a_dir / x).parent.mkdir(parents=True, exist_ok=True)
        (b_dir / y).parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false", "diff", "--no-index", "-M", "--binary", a_dir.name, b_dir.name], cwd=str(a_dir.parent), capture_output=True)
    assert r.returncode in (0, 1), r.stderr.decode("utf-8", "replace")
    patch = r.stdout
    an, bn = a_dir.name.encode(), b_dir.name.encode()
    patch = re.sub(rb"(?m)^(diff --git )a/" + re.escape(an) + rb"/(\S+) b/" + re.escape(bn) + rb"/(\S+)$", rb"\1a/\2 b/\3", patch)
    patch = re.sub(rb"(?m)^--- a/" + re.escape(an) + rb"/", b"--- a/", patch)
    patch = re.sub(rb"(?m)^\+\+\+ b/" + re.escape(bn) + rb"/", b"+++ b/", patch)
    patch = re.sub(rb"(?m)^rename from " + re.escape(an) + rb"/", b"rename from ", patch)
    patch = re.sub(rb"(?m)^rename to " + re.escape(bn) + rb"/", b"rename to ", patch)
    tmp = destino.with_name(destino.name + ".tmp")
    tmp.write_bytes(patch)
    tmp.replace(destino)
    return patch


def verificar(patch, destino, pares, origem_dir, ck):
    ck.mkdir(parents=True)
    for x, _ in pares:
        (ck / x).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(origem_dir[x], ck / x)
    subprocess.run(["git", "init", "-q"], cwd=str(ck), check=True)
    ap = subprocess.run(["git", "-c", "core.autocrlf=false", "apply", "--whitespace=nowarn", str(destino)], cwd=str(ck), capture_output=True)
    return ap


# ---- 1. o esboco, o montar_sandbox e o script de controles: R3.4 -> R3.5
A, B = D / "a", D / "b"
for x, y in PARES:
    (A / x).parent.mkdir(parents=True, exist_ok=True)
    (B / y).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(R34 / x, A / x)
    shutil.copyfile(AQUI / y, B / y)
destino = AQUI / "DIFF_R3_4_R3_5.patch"
patch = diff_git(A, B, PARES, destino)
ap = verificar(patch, destino, PARES, {x: R34 / x for x, _ in PARES}, D / "check")
iguais = {y: (D / "check" / y).is_file() and (D / "check" / y).read_bytes() == (AQUI / y).read_bytes() for _, y in PARES}
res = dict(patch=dict(path=str(destino), sha256=sha(patch), bytes=len(patch)), git_apply_rc=ap.returncode, git_apply_stderr=ap.stderr.decode("utf-8", "replace")[-500:],
           reproduz_bit_a_bit=all(iguais.values()) and ap.returncode == 0, por_arquivo=iguais, requer_core_autocrlf_false=True,
           comando_de_verificacao="git -c core.autocrlf=false apply --whitespace=nowarn DIFF_R3_4_R3_5.patch (numa copia dos .py da R3.4)",
           pares=[dict(de="R3_4/" + x, para="R3_5/" + y, sha256_de=sha((R34 / x).read_bytes()), sha256_para=sha((AQUI / y).read_bytes())) for x, y in PARES],
           identicos_a_R3_4_sem_diff=sorted(p.name for p in AQUI.glob("*.py") if p.name not in {y for _, y in PARES} and (R34 / p.name).is_file() and (R34 / p.name).read_bytes() == p.read_bytes()),
           nota="git apply (core.autocrlf=false) sobre uma copia dos .py da R3.4 em %s" % (D / "check"))
# ---- 2. o passo 10 do chain e o helper (backups de bytes -> arquivos re-derivados)
if len(sys.argv) == 4:
    bak_ch, bak_h = Path(sys.argv[2]), Path(sys.argv[3])
    p10 = [(bak_ch.name, "chain_pos_rito_v394.sh"), (bak_h.name, "b3_recibo_v394.py")]
    fontes = {bak_ch.name: bak_ch, bak_h.name: bak_h}
    A2, B2 = D / "a10", D / "b10"
    for x, y in p10:
        (A2 / y).parent.mkdir(parents=True, exist_ok=True)
        (B2 / y).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(fontes[x], A2 / y)
        shutil.copyfile(PK_POS / y, B2 / y)
    p10m = [(y, y) for _, y in p10]
    destino2 = AQUI / "DIFF_PASSO10_R3_5.patch"
    patch2 = diff_git(A2, B2, p10m, destino2)
    ap2 = verificar(patch2, destino2, p10m, {y: A2 / y for _, y in p10}, D / "check10")
    iguais2 = {y: (D / "check10" / y).read_bytes() == (PK_POS / y).read_bytes() for _, y in p10}
    res["passo10"] = dict(patch=dict(path=str(destino2), sha256=sha(patch2), bytes=len(patch2)), git_apply_rc=ap2.returncode, reproduz_bit_a_bit=all(iguais2.values()) and ap2.returncode == 0, por_arquivo=iguais2,
                          de=[dict(arquivo=str(fontes[x]), sha256=sha(fontes[x].read_bytes())) for x, _ in p10], para=[dict(arquivo=str(PK_POS / y), sha256=sha((PK_POS / y).read_bytes())) for _, y in p10])
(AQUI / "VERIFICACAO_DIFF_R3_5.json").write_bytes(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps({k: res[k] for k in ("git_apply_rc", "reproduz_bit_a_bit", "por_arquivo")}), res["patch"]["sha256"][:16], res["patch"]["bytes"], (res.get("passo10") or {}).get("reproduz_bit_a_bit"))

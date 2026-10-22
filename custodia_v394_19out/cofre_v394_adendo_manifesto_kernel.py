# -*- coding: utf-8 -*-
"""Adendo ao cofre v394 (19/10/2026, sessão a7): o tgl_kernel_v394 nasceu sem o tgl_kernel_proof_manifest.json na raiz, que o tgl_kernel_v391
tinha e que o módulo comum dos 16 dispositivos lê (patents/_formula_completa, conferência do kernel corrente). Copia-se do Nós, conferido
contra o sha256 do selo v394 e contra a cópia já em um_unificado_v394; o CUSTODY_MANIFEST do kernel ganha o campo ao lado (temporário→troca)."""
import hashlib, json, os, shutil
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
OC = Path(r"C:\IALD\Central de Patentes\vault\originals_copy")
KV, V = OC / "tgl_kernel_v394", OC / "um_unificado_v394"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


selo = json.loads((V / "um_absoluto_selo.json").read_text(encoding="utf-8"))
alvo = selo["sha256"]["tgl_kernel_proof_manifest.json"]
src = NOS / "tgl_kernel_proof_manifest.json"
assert sha(src) == alvo == sha(V / "tgl_kernel_proof_manifest.json"), "o manifesto de prova não confere com o selo v394 — PARAR"
dst = KV / "tgl_kernel_proof_manifest.json"
if not dst.is_file():
    shutil.copyfile(src, str(dst) + ".tmp")
    assert sha(str(dst) + ".tmp") == alvo
    os.replace(str(dst) + ".tmp", dst)
assert sha(dst) == alvo
mp = KV / "CUSTODY_MANIFEST.json"
km = json.loads(mp.read_text(encoding="utf-8"))
if "tgl_kernel_proof_manifest_sha256" not in km:
    km["tgl_kernel_proof_manifest_sha256"] = alvo
    km["adendo_19out"] = ("o tgl_kernel_proof_manifest.json entrou na raiz deste cofre depois da montagem (como no tgl_kernel_v391), conferido contra o "
                          "sha256 do selo v394; o módulo comum dos 16 dispositivos o lê")
    t = mp.with_suffix(".json.tmp")
    t.write_text(json.dumps(km, ensure_ascii=False, indent=1), encoding="utf-8")
    json.loads(t.read_text(encoding="utf-8"))
    os.replace(t, mp)
print("ok: proof manifest no tgl_kernel_v394", alvo[:16], "| CUSTODY_MANIFEST do kernel", sha(mp)[:16])

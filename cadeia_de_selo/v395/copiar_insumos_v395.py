# -*- coding: utf-8 -*-
"""copiar_insumos_v395.py -- copia de BYTES, para a pasta DURAVEL v395\\insumos, das fontes que os registros da v395 pinam por sha256 (a pedra, os documentos do psibit, os dois exames independentes, a medida do Audit) e
das quatro falas do operador de 21/10 (insumos\\cunhagens\\<sha16>_<nome>); grava MANIFESTO_INSUMOS_v395.json (sha256, origem). Reexecutavel: o que ja existe e e' igual fica; o que difere aborta (nao sobrescreve).
Roda DEPOIS do pos_build_kernel_v395.py (que gera kernel\\KH_N1_v395.json). Molde: copiar_insumos_v394.py.  uso: python -I -B -X utf8 copiar_insumos_v395.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v395 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
INS = os.path.join(HERE, "insumos"); CUN = os.path.join(INS, "cunhagens"); os.makedirs(CUN, exist_ok=True)
PS = os.path.join(DL.WK, "psibit_v395"); EX = os.path.join(DL.WK, "cadeia_de_selo", "v395_exame", "psibit")
ORIGENS = [(DL.STONE_INSUMO, DL.STONE_SRC), ("DEFINICAO_PSIBIT_PATENTE.md", os.path.join(PS, "DEFINICAO_PSIBIT_PATENTE.md")), ("RESULTADO_PSIBIT.md", os.path.join(PS, "RESULTADO_PSIBIT.md")),
           ("EXAME_PSIBIT.md", os.path.join(EX, "EXAME_PSIBIT.md")), ("EXAME_PSIBIT_RODADA2.md", os.path.join(EX, "EXAME_PSIBIT_RODADA2.md")),
           (DL.KH_N1_INSUMO, os.path.join(HERE, DL.KERNEL_DIR, "KH_N1_v395.json"))]
man = {}


def copia(destino, origem):
    b = open(origem, "rb").read()
    if os.path.exists(destino):
        assert open(destino, "rb").read() == b, ("o insumo ja existe e DIFERE da origem: nao sobrescrevo", destino)
    else:
        open(destino + ".tmp", "wb").write(b); assert os.path.getsize(destino + ".tmp") == len(b); os.replace(destino + ".tmp", destino)
    assert open(destino, "rb").read() == b
    return {"origem": origem, "sha256": sha(b), "bytes": len(b)}


for nome, orig in ORIGENS:
    man[nome] = copia(os.path.join(INS, nome), orig)
# a pedra duravel == a embutida/sandbox (o sandbox e' conferido por preparar_kernel_v395.py conferir)
assert man[DL.STONE_INSUMO]["sha256"] == sha(open(os.path.join(DL.SANDBOX, *DL.STONE_REL.split("/")), "rb").read()), "a pedra duravel difere da do sandbox"
for v in DL.verbatins(CUN):
    man["cunhagens/" + os.path.basename(v["arquivo"])] = copia(v["arquivo"], v["fonte_original"])
    assert man["cunhagens/" + os.path.basename(v["arquivo"])]["sha256"] == v["sha256"]
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v395.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: v["sha256"][:16] for k, v in man.items()}, ensure_ascii=False, indent=1))

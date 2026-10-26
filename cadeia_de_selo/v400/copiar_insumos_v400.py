# -*- coding: utf-8 -*-
"""copiar_insumos_v400.py -- copia de BYTES, para a pasta DURAVEL v400\\insumos, das fontes que os registros da v399 (recriados pelo rito da v400) pinam por sha256: a pedra Testemunho (insumos\\Testemunho.lean), a medida do Audit (KH_N1_v399.json),
as QUATRO inscricoes de 24/10/2026 (todas falas do operador; insumos\\cunhagens\\<sha16>_<nome>), os arquivos do ESTUDO do selo pela propria tecnologia (insumos\\acom) e as SEIS fontes do operador que o bloco embutido cita (insumos\\acom\\fontes_operador).
A v400 NAO traz insumo novo (nenhuma inscricao nova, nenhuma pedra nova): a ORIGEM de cada copia e' a pasta duravel da v399 (work\\cadeia_de_selo\\v399\\insumos), cujo sha256 e' conferido contra o MANIFESTO_INSUMOS_v399.json (que registra as origens e os hashes de quando a v399 os pinou).
O Teste da Unica Palavra (o resultado e os tres recibos) NAO e' copiado: os insumos duraveis dele moram em v397\\insumos\\fase9 (o um.py selado ja' os pina por esse caminho). Grava MANIFESTO_INSUMOS_v400.json (sha256, origem).
Reexecutavel: o que ja existe e e' igual fica; o que difere aborta (nao sobrescreve). Escreve SO' em v400\\insumos e no manifesto. uso: python -I -B -X utf8 copiar_insumos_v400.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); WK = os.path.dirname(os.path.dirname(HERE))
V9 = os.path.join(os.path.dirname(HERE), "v399")
sha = lambda b: hashlib.sha256(b).hexdigest()
M9 = json.load(open(os.path.join(V9, "MANIFESTO_INSUMOS_v399.json"), encoding="utf-8"))
INS9 = os.path.join(V9, "insumos"); INS = os.path.join(HERE, "insumos")
man = {}
presentes = sorted(os.path.relpath(os.path.join(r, f), INS9).replace(os.sep, "/") for r, _, fs in os.walk(INS9) for f in fs)
assert presentes == sorted(M9), ("os insumos da v399 em disco != o MANIFESTO_INSUMOS_v399.json", sorted(set(presentes) ^ set(M9)))
for rel in presentes:
    src = os.path.join(INS9, *rel.split("/")); dst = os.path.join(INS, *rel.split("/"))
    b = open(src, "rb").read()
    assert sha(b) == M9[rel]["sha256"] and len(b) == M9[rel]["bytes"], ("o insumo da v399 difere do que o MANIFESTO_INSUMOS_v399.json pinou", rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst):
        assert open(dst, "rb").read() == b, ("o insumo ja existe e DIFERE da origem: nao sobrescrevo", dst)
    else:
        open(dst + ".tmp", "wb").write(b); assert os.path.getsize(dst + ".tmp") == len(b); os.replace(dst + ".tmp", dst)
    assert open(dst, "rb").read() == b
    man[rel] = {"origem": src, "origem_v399_manifesto_sha256": M9[rel]["sha256"], "sha256": sha(b), "bytes": len(b)}
json.dump(man, open(os.path.join(HERE, "MANIFESTO_INSUMOS_v400.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("insumos copiados/conferidos:", len(man), "| total", sum(v["bytes"] for v in man.values()), "B")

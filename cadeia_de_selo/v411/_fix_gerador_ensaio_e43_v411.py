# -*- coding: utf-8 -*-
"""_fix_gerador_ensaio_e43_v411.py -- (claude-construtor-v411, retomada, 12/11/2026) duas mudancas CONTIDAS no gerar_candidato_v411.py: (1) o MODO DE ENSAIO DO TOPO PROPOSTO (V411_ENSAIO_TOPO_PROPOSTO=1; ordem da
gerencia de 12/11): o texto PROPOSTO do DESENHO 5.1 b com as guardas ESTRITAS, e o artefato (NAO candidato) gravado so' em C:\\t\\k411c\\ensaio_topo_proposto, com o manifesto dele; (2) a E43 no cabecalho do bloco de runtime.
Backup de BYTES antes; cada ancora ocorre EXATAMENTE uma vez; ast.parse depois. uso: python -B -X utf8 _fix_gerador_ensaio_e43_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "gerar_candidato_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8")
assert "\r" not in t
PARES = [
    ('     python -B -X utf8 gerar_candidato_v411.py --prevoo   (PRE-VOO',
     '     V411_ENSAIO_TOPO_PROPOSTO=1 python -B -X utf8 gerar_candidato_v411.py   (ENSAIO do topo proposto, ordem da gerencia de 12/11: o texto PROPOSTO do DESENHO 5.1 b com TODAS as guardas ESTRITAS; grava o ARTEFATO DE ENSAIO\n'
     '        um_v411_ENSAIO_TOPO_PROPOSTO.py e o manifesto dele SO\' em C:\\\\t\\\\k411c\\\\ensaio_topo_proposto, fora de work; NUNCA e\' candidato, nao se instala, o hash nao entra na pasta da cadeia)\n'
     '     python -B -X utf8 gerar_candidato_v411.py --prevoo   (PRE-VOO'),
    ('if os.path.exists(DL.TOPO_RATIFICADO_ARQ):\n    _tb = open(DL.TOPO_RATIFICADO_ARQ, "rb").read()',
     'ENSAIO = DL.ENSAIO_TOPO_PROPOSTO\nassert not (ENSAIO and PREVOO), "o pre-voo e o ensaio do topo proposto sao modos distintos"\nif ENSAIO:\n'
     '    TOPO = {"pt": _m_prop["pt"].group(1), "en": _m_prop["en"].group(1), "ratificado": False, "arquivo": None, "sha256": None, "nota": "ENSAIO do topo proposto (ordem da gerencia de 12/11): o texto PROPOSTO pela gerencia no DESENHO 5.1 b, PENDENTE da palavra do operador; o artefato NAO e\' candidato e fica fora de work"}\n'
     'elif os.path.exists(DL.TOPO_RATIFICADO_ARQ):\n    _tb = open(DL.TOPO_RATIFICADO_ARQ, "rb").read()'),
    ('SIMD = os.path.join(DL.SANDBOX_PAI, "arvore_simulada_h8")', 'SIMD = os.path.join(DL.RODADA_PAI, "arvore_simulada_h8")'),
    ('As erratas E41 e E42 vao AO LADO;', 'As erratas E41, E42 e E43 vao AO LADO;'),
    ('man = {"candidato": os.path.join(HERE, DL.CANDIDATO), "sha16"', 'man = {("artefato_de_ensaio" if ENSAIO else "candidato"): DL.CANDIDATO_ARQ, "sha16"'),
    ('"runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "quando": datetime.datetime.now().isoformat(timespec="seconds")}',
     '"runtime": {"sha256": sha256(RUNTIME_SRC.encode("utf-8")), "bytes": len(RUNTIME_SRC.encode("utf-8"))}, "quando": datetime.datetime.now().isoformat(timespec="seconds"), **DL.MARCA_ENSAIO}'),
    ('out = os.path.join(HERE, DL.CANDIDATO)\nassert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V411_REGERAR") == "1", "o candidato ja existe e difere: defina V411_REGERAR=1 para regerar"',
     'out = DL.CANDIDATO_ARQ\nassert not ENSAIO or os.path.normcase(DL.WK) not in os.path.normcase(os.path.abspath(out)), "o artefato de ensaio nao pode ficar em work"\n'
     'assert not os.path.exists(out) or open(out, "rb").read() == b or os.environ.get("V411_REGERAR") == "1" or ENSAIO, "o candidato ja existe e difere: defina V411_REGERAR=1 para regerar"'),
    ('open(os.path.join(HERE, "CANDIDATO_v411.json") + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(os.path.join(HERE, "CANDIDATO_v411.json") + ".tmp", os.path.join(HERE, "CANDIDATO_v411.json"))\n',
     'open(DL.MANIFESTO_ARQ + ".tmp", "w", encoding="utf-8").write(json.dumps(man, ensure_ascii=False, indent=1)); os.replace(DL.MANIFESTO_ARQ + ".tmp", DL.MANIFESTO_ARQ)\n'),
    ('open(os.path.join(HERE, "FORMAL_MAP_v411.json"), "w", encoding="utf-8").write(json.dumps(FORMAL_MAP, ensure_ascii=False, indent=0))\n',
     'open(DL.FORMAL_MAP_ARQ + ".tmp", "w", encoding="utf-8").write(json.dumps(FORMAL_MAP, ensure_ascii=False, indent=0)); os.replace(DL.FORMAL_MAP_ARQ + ".tmp", DL.FORMAL_MAP_ARQ)\n'),
    ('open(os.path.join(HERE, "v411_pins.py"), "w", encoding="utf-8", newline="\\n").write(RT_)\n',
     'open(DL.PINS_ARQ + ".tmp", "w", encoding="utf-8", newline="\\n").write(RT_); os.replace(DL.PINS_ARQ + ".tmp", DL.PINS_ARQ)\n'
     'if ENSAIO:\n    print("ENSAIO do topo proposto: o ARTEFATO (NAO candidato) em", out)\n'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:90], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb), "| backup", os.path.basename(bak))

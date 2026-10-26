# -*- coding: utf-8 -*-
"""gerar_cadeia_de_selos.py (R3.4, 19/10/2026) -- gera, POR SCRIPT, a CADEIA_DE_SELOS_vNNN.json (contrato CADEIA_DE_SELOS_R3_4) que o sincronizar_bancada.py R3.4 exige
quando a Bancada pina uma versao anterior a do Nos (salto): um elo por versao, de --de ate --ate, com as COPIAS DE BYTES pinadas por sha256 que a cadeia de selo ja guarda:
  - o um.py, o selo e o manifesto do kernel da versao J: pasta <cadeia>/v(J+1)/base_vJ/ (a copia que a preparacao da versao seguinte tira do Nos antes de instalar);
  - para cada troca J -> J+1: o registro do instalador <cadeia>/v(J+1)/APLICADO_AO_CANONICO_<ts>.json (o UNICO cujos sha16 conferem: backup do um.py de J e um.py novo =
    o de J+1; as tentativas revertidas de uma instalacao ficam de fora) e os backups de BYTES que ele nomeia (Nos\\um.py.bak_<ts>, Nos\\um_absoluto_selo.json.bak_<ts>).
Nada e digitado: todo caminho vem de listagem de disco, todo hash e lido do arquivo. O gerador NAO decide se a cadeia vale: quem confere e o esboco (carregar_cadeia_de_selos).
Escreve UM arquivo NOVO (--saida) e nada mais. uso: python -I -B -X utf8 gerar_cadeia_de_selos.py --cadeia <pasta cadeia_de_selo> --de v392 --ate v393 --saida <novo.json>"""
import sys
sys.dont_write_bytecode = True
import argparse, datetime, hashlib, json, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--cadeia", required=True, help="a pasta work/cadeia_de_selo (com v(J+1)/base_vJ/ e v(J+1)/APLICADO_AO_CANONICO_*.json)")
ap.add_argument("--de", required=True)
ap.add_argument("--ate", required=True)
ap.add_argument("--saida", required=True)
a = ap.parse_args()
RAIZ = Path(a.cadeia)
RE_V = re.compile(r"^v(\d{3,4})$")
md, ma = RE_V.match(a.de), RE_V.match(a.ate)
if not md or not ma or int(ma.group(1)) <= int(md.group(1)):
    raise SystemExit("VERSOES_INVALIDAS: --de e --ate sao vNNN e --ate > --de")
largura = len(md.group(1))
versoes = ["v%0*d" % (largura, n) for n in range(int(md.group(1)), int(ma.group(1)) + 1)]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def arq(p):
    p = Path(p)
    if not p.is_file():
        raise SystemExit("ARQUIVO_AUSENTE: %s" % p)
    return dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size)


def proxima(v):
    return "v%0*d" % (largura, int(RE_V.match(v).group(1)) + 1)


elos = []
for v in versoes:
    base = RAIZ / proxima(v) / ("base_" + v)
    if not base.is_dir():
        raise SystemExit("BASE_AUSENTE: %s (a copia de bytes de %s fica em <cadeia>/%s/base_%s)" % (base, v, proxima(v), v))
    elos.append(dict(versao=v, um_py=arq(base / "um.py"), selo=arq(base / "um_absoluto_selo.json"), kernel_manifesto=arq(base / "tgl_kernel_proof_manifest.json")))
for e, f in zip(elos, elos[1:]):
    pasta = RAIZ / proxima(e["versao"])          # a pasta da cadeia da versao que SUBSTITUIU e["versao"]
    sh16_antigo, sh16_novo = e["um_py"]["sha256"][:16], f["um_py"]["sha256"][:16]
    achados = []
    for rp in sorted(pasta.glob("APLICADO_AO_CANONICO_*.json")):
        rj = json.loads(rp.read_bytes())
        b = (rj.get("backups") or {}).get("um.py") or {}
        n = rj.get("um_py_novo") or {}
        if b.get("sha16") == sh16_antigo and n.get("sha16") == sh16_novo:
            achados.append((rp, rj))
    if len(achados) != 1:
        raise SystemExit("REGISTRO_DO_INSTALADOR: %d registro(s) de %s conferem (backup %s, novo %s); exige exatamente 1 (as tentativas revertidas nao conferem)"
                         % (len(achados), pasta, sh16_antigo, sh16_novo))
    rp, rj = achados[0]
    e["substituido_na_instalacao_por"] = dict(versao=f["versao"], registro=arq(rp), backup_um_py=arq(rj["backups"]["um.py"]["backup"]),
                                              backup_selo=arq(rj["backups"]["um_absoluto_selo.json"]["backup"]))
out = dict(contrato="CADEIA_DE_SELOS_R3_4", gerada_em_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
           gerada_por=dict(script="gerar_cadeia_de_selos.py", script_sha256=sha(__file__), de=a.de, ate=a.ate),
           nota="elos de %s a %s; copias de bytes da pasta base_vJ de cada versao seguinte e registros do instalador; quem confere e o sincronizar_bancada.py R3.4" % (a.de, a.ate),
           elos=elos)
p = Path(a.saida)
with open(p, "xb") as f:
    f.write((json.dumps(out, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print(json.dumps(dict(saida=str(p), sha256=sha(p), n_elos=len(elos), versoes=versoes), ensure_ascii=False))

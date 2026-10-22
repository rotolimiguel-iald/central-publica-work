# -*- coding: utf-8 -*-
"""montar_sandbox.py -- monta, SO dentro de work\\bancada_vinculo_12out\\sandbox, (1) uma COPIA byte a byte da Bancada Um instalada (B2):
o codigo (32) e as fontes relativas (56) conferidos contra os pinos de canonical_contracts.json, mais o proprio manifesto; e (2) um NOS
SINTETICO para o ensaio do re-pino: o um.py v391 com a linha de coluna 0 UM_VERSION trocada para "v392" (mesmo comprimento), um selo
sintetico que pina esses bytes (marcado SINTETICO), e o core copiado. A producao e so lida. Nada e um selo do rito."""
import hashlib, json, re, datetime, sys
from pathlib import Path
AQUI = Path(__file__).resolve().parent
PROD = Path(r"C:\IALD\Bancada_Um")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
SB = AQUI / "sandbox"
COPIA = SB / "bancada_copia"
NSIN = SB / "nos_sintetico"
VERSAO_SINTETICA = sys.argv[1] if len(sys.argv) > 1 else "v392"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def gravar_novo(dst, raw):
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        # o manifesto B2 pina o mesmo arquivo em code E em sources (ex.: fontes_externas/F5.2/10_frozen_neff_v1.py): duplicata so com bytes iguais
        if dst.read_bytes() != raw:
            raise SystemExit("DUPLICATA COM BYTES DIFERENTES: " + str(dst))
        return dict(path=str(dst), sha256=sha(raw), bytes=len(raw), duplicata_de_pino=True)
    with open(dst, "xb") as f:
        f.write(raw)
    assert dst.read_bytes() == raw, dst
    return dict(path=str(dst), sha256=sha(raw), bytes=len(raw))


rec = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), copia=[], nos_sintetico={})
if COPIA.exists() or NSIN.exists():
    raise SystemExit("sandbox ja montado: apague antes (so dentro de " + str(SB) + ")")
man_raw = (PROD / "canonical_contracts.json").read_bytes()
man = json.loads(man_raw)
rec["copia"].append(gravar_novo(COPIA / "canonical_contracts.json", man_raw))
for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
    raw = (PROD / e["path"]).read_bytes()
    if sha(raw) != e["sha256"] or len(raw) != e["bytes"]:
        raise SystemExit("PIN MISMATCH na producao: " + e["path"])
    rec["copia"].append(gravar_novo(COPIA / e["path"], raw))
(COPIA / "estado").mkdir()
rec["n_copia"] = len(rec["copia"])
# o Nos sintetico
um = (NOS / "um.py").read_bytes()
txt = um.decode("utf-8-sig")
mv = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', txt, re.M)
assert mv and mv.group(1) == "v391", mv
velha = mv.group(0).encode("utf-8")
assert um.count(velha) >= 1
nova = velha.replace(b"v391", VERSAO_SINTETICA.encode("utf-8"), 1)
um_sin = um.replace(velha, nova, 1)
assert len(um_sin) == len(um) and um_sin != um
t2 = um_sin.decode("utf-8-sig")
assert re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', t2, re.M).group(1) == VERSAO_SINTETICA
assert len(re.findall(r"^ALPHA_FINE_CODATA_2018[ \t]*=", t2, re.M)) == len(re.findall(r"^ALPHA_FINE_CODATA_2018[ \t]*=", txt, re.M)) == 1
selo = json.loads((NOS / "um_absoluto_selo.json").read_bytes())
selo_sin = dict(selo)
selo_sin["um_version"] = VERSAO_SINTETICA
selo_sin["sha256"] = dict(selo["sha256"])
selo_sin["sha256"]["um.py"] = sha(um_sin)
selo_sin["SINTETICO_SANDBOX"] = ("NAO E UM SELO DO RITO: fixture do ensaio do vinculo Bancada-um.py (12/10/2026); deriva do selo v391 real "
                                 "%s trocando so um_version e sha256[um.py]; vive so em work\\bancada_vinculo_12out\\sandbox" % sha(json.dumps(selo).encode())[:0])
selo_sin["SINTETICO_SANDBOX_derivado_do_selo_v391_sha256"] = sha((NOS / "um_absoluto_selo.json").read_bytes())
selo_b = json.dumps(selo_sin, ensure_ascii=False, indent=1).encode("utf-8")
core = (NOS / "um_absoluto.json").read_bytes()
assert sha(core) == selo["sha256"]["um_absoluto.json"]
rec["nos_sintetico"] = dict(um_py=gravar_novo(NSIN / "um.py", um_sin), selo=gravar_novo(NSIN / "um_absoluto_selo.json", selo_b),
                            core=gravar_novo(NSIN / "um_absoluto.json", core), versao=VERSAO_SINTETICA,
                            um_py_real=dict(sha256=sha(um), bytes=len(um)), bytes_trocados=len(velha),
                            linha_trocada=txt[:mv.start()].count("\n") + 1)
gravar_novo(NSIN / "LEIA-ME_SINTETICO.txt", ("Fixture sintetica (12/10/2026): um.py v391 real com UM_VERSION trocada para %s na linha %d; selo derivado; core copiado. "
                                             "NAO e versao selada. So para ensaiar o re-pino da Bancada no sandbox.\n" % (VERSAO_SINTETICA, rec["nos_sintetico"]["linha_trocada"])).encode("utf-8"))
p = SB / "SANDBOX_MANIFEST.json"
p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(dict(n_copia=rec["n_copia"], nos_sintetico={k: v for k, v in rec["nos_sintetico"].items() if k != "core"}), ensure_ascii=False, indent=1))

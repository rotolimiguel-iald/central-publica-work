# -*- coding: utf-8 -*-
"""gerar_bateria_r3_4.py (R3.4, 19/10/2026) -- REGENERA, POR SCRIPT, a bateria da Bancada para a versao que o Nos tem agora (a bateria por versao): parte da bateria base
(BATERIA_VINCULO.json da R2, pinada por sha256), troca o T12/T13/T14 (que pinava o um.py v391 no pre-registro congelado) pelo driver R3.4 + o PINO_UM_PY_vNNN.json, marca
o teste com pina_o_um_py=true e escreve o bloco pinos_da_versao {versao, um_py_sha256, um_py_bytes, selo_sha256}. Os pinos vem do Nos (um.py e selo, lidos aqui e conferidos
entre si: o selo pina o um.py; UM_VERSION confere) e, no modo real, dos PINOS DA CADEIA da versao instalada (PINOS_BN_vNNN.json: candidato.sha256 == o um.py do Nos).
Nada e digitado: caminho, sha256 e bytes de toda fonte sao lidos do disco. Escreve DOIS arquivos NOVOS (--pino-saida e --saida) e nada mais; recusa se existirem.
uso: python -I -B -X utf8 gerar_bateria_r3_4.py --base <BATERIA_VINCULO.json> [--base-sha256 H] --versao vNNN --nos <dir> --driver <t12_t14_atrator_r3_4.py>
         (--pinos-bn <PINOS_BN_vNNN.json> | --sandbox) --pino-saida <PINO_UM_PY_vNNN.json> --saida <BATERIA_VINCULO_vNNN.json>"""
import sys
sys.dont_write_bytecode = True
import argparse, hashlib, json, re
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--base", required=True)
ap.add_argument("--base-sha256", default=None)
ap.add_argument("--versao", required=True)
ap.add_argument("--nos", required=True)
ap.add_argument("--driver", required=True)
ap.add_argument("--pinos-bn", default=None)
ap.add_argument("--sandbox", action="store_true", help="sem PINOS_BN: o Nos e uma copia de ensaio e os pinos saem dele mesmo (dito em fonte_dos_pinos)")
ap.add_argument("--pino-saida", required=True)
ap.add_argument("--saida", required=True)
a = ap.parse_args()
if bool(a.pinos_bn) == bool(a.sandbox):
    raise SystemExit("PINOS_DA_CADEIA: exatamente um de --pinos-bn (real) ou --sandbox")
if not re.match(r"^v\d{3,4}$", a.versao):
    raise SystemExit("VERSAO_INVALIDA: %r" % a.versao)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pinar(p):
    p = Path(p).resolve()
    b = p.read_bytes()
    return dict(path=str(p), sha256=sha(b), bytes=len(b))


def sha_teste(t):
    return sha(json.dumps(t, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


# ---- o Nos: um.py e selo, lidos e conferidos entre si
nos = Path(a.nos)
um_b, selo_b = (nos / "um.py").read_bytes(), (nos / "um_absoluto_selo.json").read_bytes()
selo = json.loads(selo_b)
if selo.get("um_version") != a.versao:
    raise SystemExit("SELO_DE_OUTRA_VERSAO: o selo do Nos diz %r, --versao %s" % (selo.get("um_version"), a.versao))
if (selo.get("sha256") or {}).get("um.py") != sha(um_b):
    raise SystemExit("SELO_NAO_PINA_O_UM_PY_DO_DISCO")
mv = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', um_b.decode("utf-8-sig"), re.M)
if not mv or mv.group(1) != a.versao:
    raise SystemExit("UM_VERSION_DIFERENTE: %r" % (mv.group(1) if mv else None))
fonte = dict(nos=dict(dir=str(nos), um_py=dict(sha256=sha(um_b), bytes=len(um_b)), selo=dict(sha256=sha(selo_b), bytes=len(selo_b))))
if a.pinos_bn:
    pb = Path(a.pinos_bn)
    pbj = json.loads(pb.read_bytes())
    cand = (pbj.get("candidato") or {})
    if cand.get("sha256") != sha(um_b):
        raise SystemExit("PINOS_DA_CADEIA_NAO_SAO_OS_DO_NOS: PINOS_BN pina o candidato %s e o um.py do Nos e %s" % (str(cand.get("sha256"))[:16], sha(um_b)[:16]))
    fonte["pinos_bn"] = dict(path=str(pb.resolve()), sha256=sha(pb.read_bytes()), candidato_sha256=cand["sha256"], regra="candidato.sha256 do PINOS_BN da versao instalada == o um.py do Nos == o que o selo pina")
else:
    fonte["origem"] = "sandbox: copia de ensaio do Nos; os pinos saem do proprio Nos (nao ha PINOS_BN)"

# ---- a bateria base (pinada) e a troca do T12/T13/T14
base_p = Path(a.base)
base_raw = base_p.read_bytes()
if a.base_sha256 and a.base_sha256.lower() != sha(base_raw):
    raise SystemExit("BASE_SHA_DIVERGE: %s != %s" % (sha(base_raw)[:16], a.base_sha256[:16]))
b = json.loads(base_raw)
ts = b["testes"]
idx = [i for i, t in enumerate(ts) if t["id"] == "T12_T13_T14_ATRATOR"]
if len(idx) != 1:
    raise SystemExit("BASE_SEM_T12: %d testes T12_T13_T14_ATRATOR" % len(idx))
t12 = ts[idx[0]]
if Path(t12["fontes"][0]["path"]).name != "t12_t14_atrator.py" or "{fonte:0}" not in t12["comando"]:
    raise SystemExit("BASE_COM_T12_DIFERENTE: o primeiro fonte do T12 da base nao e o driver R2")
pino_p = Path(a.pino_saida)
saida_p = Path(a.saida)
for p in (pino_p, saida_p):
    if p.exists():
        raise SystemExit("ARQUIVO_JA_EXISTE: %s" % p)
pino = dict(contrato="PINO_UM_PY_R3_4", versao=a.versao, um_py=dict(sha256=sha(um_b), bytes=len(um_b)), selo_sha256=sha(selo_b), fonte_dos_pinos=fonte,
            gerado_por="gerar_bateria_r3_4.py")      # sem carimbo de hora: mesma entrada, mesmos bytes (o pino e a bateria sao deterministas)
pino_p.parent.mkdir(parents=True, exist_ok=True)
with open(pino_p, "xb") as f:
    f.write((json.dumps(pino, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
fontes = [pinar(a.driver)] + [dict(f) for f in t12["fontes"][1:]] + [pinar(pino_p)]
k_pino = len(fontes) - 1
t12n = dict(t12)
t12n["fontes"] = fontes
t12n["comando"] = ["{py}", "-B", "-X", "utf8", "{fonte:0}", "{tunel}/F1.ATRATOR", "{raiz}/atrator/F1.ATRATOR", "{recibos}/T12_T13_T14_ATRATOR.json",
                   "{fonte:%d}" % k_pino, "{nos}", "{um_py_sha256}", "{um_py_bytes}"]
t12n["pina_o_um_py"] = True
t12n["teste"] = t12["teste"] + " -- R3.4: o pino do um.py do pre-registro congelado e repinado, na copia, para o um.py medido no Nos (pino da cadeia)"
t12n["estatuto_12out"] = t12.get("estatuto_12out", "") + " | R3.4 19/10: por versao (PINO_UM_PY pinado), sem sha fixo da v391"
ts[idx[0]] = t12n
b["versao_bateria"] = "VINCULO-19out-R3.4-" + a.versao
b["contrato_bateria"] = "BATERIA_R3_4"
b["pinos_da_versao"] = dict(versao=a.versao, um_py_sha256=sha(um_b), um_py_bytes=len(um_b), selo_sha256=sha(selo_b), fonte_dos_pinos=fonte)
b["origem_r3_4"] = dict(base=dict(path=str(base_p.resolve()), sha256=sha(base_raw)), versao_bateria_base=json.loads(base_raw).get("versao_bateria"))
b["gerado_por_r3_4"] = dict(script="gerar_bateria_r3_4.py", script_sha256=sha(Path(__file__).read_bytes()), driver=pinar(a.driver), pino=pinar(pino_p))
b["testes_sha256"] = {t["id"]: sha_teste(t) for t in ts}
with open(saida_p, "xb") as f:
    f.write((json.dumps(b, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
print(json.dumps(dict(bateria=str(saida_p), bateria_sha256=sha(saida_p.read_bytes()), pino=str(pino_p), pino_sha256=sha(pino_p.read_bytes()), versao=a.versao,
                      testes=[t["id"] for t in ts], marcados=[t["id"] for t in ts if t.get("pina_o_um_py")]), ensure_ascii=False))

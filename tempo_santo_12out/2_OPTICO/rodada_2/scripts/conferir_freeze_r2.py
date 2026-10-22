"""Rodada 2 do construtor otico F1.TEMPO -- conferencia do FREEZE ANTES de qualquer ensaio.
Somente leitura fora de 2_OPTICO\\rodada_2. Confere por sha256 dos BYTES e tamanho:
  (1) FREEZE.json contra o valor do enunciado da tarefa;
  (2) PREREGISTRO.json / PREREGISTRO.md contra o FREEZE e contra o enunciado;
  (3) os 28 anexos listados no FREEZE;
  (4) que nenhum arquivo de 1_PREREGISTRO nasceu ou mudou depois do congelamento;
  (5) o texto do operador (integral e a segunda parte);
  (6) o um.py v391 (bytes; NAO executado).
Uso: python -I conferir_freeze_r2.py <saida.json>
Divergencia = INVALIDO (codigo de saida 2)."""
import datetime
import hashlib
import json
import os
import sys

PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO"
FREEZE = os.path.join(PRE, "FREEZE.json")
# valores esperados copiados do enunciado da tarefa; a conferencia e contra os BYTES
EXP = {
    "freeze_sha": "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b",
    "freeze_bytes": 5986,
    "json_sha": "64b1c38637befddf89ca06635c548a7d090072f1bc5b6492591cbd4eab163569",
    "json_bytes": 208285,
    "md_sha": "0261dc06a5fe513bef153b6df6f107042adf667b9cd97c14336380b9529799b8",
    "md_bytes": 103112,
    "congelado_em_utc": "2026-10-12T16:09:07.217728+00:00",
    "oper_sha": "2c8b7b712aa9ad7f435f8652d1febdf6fe64d14775e277f2b2d720598135c8c3",
    "oper_sha16": "2c8b7b712aa9ad7f",
    "parte2_sha": "6dcefdbe5c6a7752766ec9a1aaa2255f9b874fbb2a445925b6c615f1b574dc72",
    "parte2_off": 2853,
    "parte2_len": 3820,
    "umpy_sha": "8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6",
}
OPER = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"


def sha_file(p):
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as fh:
        while True:
            c = fh.read(1 << 22)
            if not c:
                break
            h.update(c)
            n += len(c)
    return h.hexdigest(), n


out = {
    "papel": "construtor otico F1.TEMPO, rodada 2 (conferencia antes do ensaio)",
    "taken_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "checks": [],
}


def check(name, got, exp):
    ok = (got == exp)
    out["checks"].append({"item": name, "esperado": exp, "lido": got, "ok": ok})
    return ok


fb = open(FREEZE, "rb").read()
check("FREEZE.json sha256", hashlib.sha256(fb).hexdigest(), EXP["freeze_sha"])
check("FREEZE.json bytes", len(fb), EXP["freeze_bytes"])
fz = json.loads(fb.decode("utf-8"))
check("FREEZE.congelado_em_utc", fz.get("congelado_em_utc"), EXP["congelado_em_utc"])
check("FREEZE.preregistro_json.sha256 == enunciado", fz["preregistro_json"]["sha256"], EXP["json_sha"])
check("FREEZE.preregistro_json.bytes == enunciado", fz["preregistro_json"]["bytes"], EXP["json_bytes"])
check("FREEZE.preregistro_md.sha256 == enunciado", fz["preregistro_md"]["sha256"], EXP["md_sha"])
check("FREEZE.preregistro_md.bytes == enunciado", fz["preregistro_md"]["bytes"], EXP["md_bytes"])
s, n = sha_file(fz["preregistro_json"]["arquivo"])
check("PREREGISTRO.json sha256 (bytes)", s, EXP["json_sha"])
check("PREREGISTRO.json bytes", n, EXP["json_bytes"])
s, n = sha_file(fz["preregistro_md"]["arquivo"])
check("PREREGISTRO.md sha256 (bytes)", s, EXP["md_sha"])
check("PREREGISTRO.md bytes", n, EXP["md_bytes"])
listados = {"FREEZE.json", "PREREGISTRO.json", "PREREGISTRO.md"}
for a in fz["anexos"]:
    p = os.path.join(PRE, a["caminho"].replace("/", os.sep))
    s, n = sha_file(p)
    check("anexo %s sha256" % a["caminho"], s, a["sha256"])
    check("anexo %s bytes" % a["caminho"], n, a["bytes"])
    listados.add(a["caminho"].replace("/", os.sep))
check("numero de anexos no FREEZE", len(fz["anexos"]), 28)

# nenhum arquivo novo, ausente ou com mtime posterior ao congelamento
t_freeze = datetime.datetime.fromisoformat(EXP["congelado_em_utc"]).timestamp()
encontrados = set()
posteriores = []
for raiz, dirs, files in os.walk(PRE):
    for f in files:
        rel = os.path.relpath(os.path.join(raiz, f), PRE)
        encontrados.add(rel)
        mt = os.stat(os.path.join(raiz, f)).st_mtime
        # FREEZE.json e gravado no proprio instante do congelamento (tolerancia de 2 s)
        if mt > t_freeze + 2.0:
            posteriores.append({"arquivo": rel, "mtime_utc": datetime.datetime.fromtimestamp(mt, datetime.timezone.utc).isoformat()})
check("arquivos em 1_PREREGISTRO nao listados no FREEZE", sorted(encontrados - listados), [])
check("arquivos listados no FREEZE ausentes do disco", sorted(listados - encontrados), [])
check("arquivos de 1_PREREGISTRO com mtime posterior ao FREEZE (+2 s)", posteriores, [])

# texto do operador
ob = open(OPER, "rb").read()
so = hashlib.sha256(ob).hexdigest()
check("texto do operador sha256 (integral)", so, EXP["oper_sha"])
check("texto do operador sha16", so[:16], EXP["oper_sha16"])
p2 = ob[EXP["parte2_off"]:]
check("segunda parte comprimento (byte 2853 ate o fim)", len(p2), EXP["parte2_len"])
check("segunda parte sha256", hashlib.sha256(p2).hexdigest(), EXP["parte2_sha"])
inicio = "O que mais me fascina é a impossibilidade de definição do tempo".encode("utf-8")
check("segunda parte comeca na frase pre-registrada", p2[:len(inicio)] == inicio, True)

# um.py v391 (somente bytes; NAO executado)
s, n = sha_file(UMPY)
check("um.py sha256 (v391)", s, EXP["umpy_sha"])
out["um_py_bytes"] = n

kd = fz["kernel_impressao_digital"]
check("FREEZE kernel antes==depois", kd["iguais"], True)
check("FREEZE congelado_antes_de_qualquer_ensaio", fz["congelado_antes_de_qualquer_ensaio"], True)
check("FREEZE nenhum_teste_rodado", fz["nenhum_teste_rodado"], True)

out["all_ok"] = all(c["ok"] for c in out["checks"])
out["n_checks"] = len(out["checks"])
out["n_falhas"] = sum(1 for c in out["checks"] if not c["ok"])
tmp = sys.argv[1] + ".tmp"
with open(tmp, "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
os.replace(tmp, sys.argv[1])
print(json.dumps({"all_ok": out["all_ok"], "n_checks": out["n_checks"], "n_falhas": out["n_falhas"]}))
for c in out["checks"]:
    if not c["ok"]:
        print("DIVERGENCIA:", json.dumps(c, ensure_ascii=False))
sys.exit(0 if out["all_ok"] else 2)

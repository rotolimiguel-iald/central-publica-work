"""Confere por script (sha256 dos bytes + tamanho) o FREEZE do pre-registro F1.TEMPO
antes de qualquer ensaio otico. Somente leitura fora de 2_OPTICO.
Uso: python -I conferir_freeze.py <saida.json>
Divergencia = INVALIDO (codigo de saida 2)."""
import hashlib, json, os, sys, time

PRE = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\1_PREREGISTRO"
FREEZE = os.path.join(PRE, "FREEZE.json")
# valores esperados copiados do enunciado da tarefa (a conferencia e contra os BYTES)
EXP_FREEZE_SHA = "6b29d4c9b09e5553a3d58a3933137bbf73df3d0b6632b036e0a74abef7533c9b"
EXP_FREEZE_BYTES = 5986
EXP_JSON_SHA = "64b1c38637befddf89ca06635c548a7d090072f1bc5b6492591cbd4eab163569"
EXP_JSON_BYTES = 208285
EXP_MD_SHA = "0261dc06a5fe513bef153b6df6f107042adf667b9cd97c14336380b9529799b8"
EXP_MD_BYTES = 103112
OPER = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"
EXP_OPER_SHA16 = "2c8b7b712aa9ad7f"
EXP_OPER_SHA = "2c8b7b712aa9ad7f435f8652d1febdf6fe64d14775e277f2b2d720598135c8c3"
EXP_PARTE2_SHA = "6dcefdbe5c6a7752766ec9a1aaa2255f9b874fbb2a445925b6c615f1b574dc72"
EXP_PARTE2_OFF = 2853
EXP_PARTE2_LEN = 3820
UMPY = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py"
EXP_UMPY_SHA = "8e7b9927ceae64b8b6812019f77cca24c08296222ae7968af41baf2fe7a67dc6"


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


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


out = {"taken_at": time.strftime("%Y-%m-%d %H:%M:%S"), "checks": [], "all_ok": None}


def check(name, got, exp):
    ok = (got == exp)
    out["checks"].append({"item": name, "esperado": exp, "lido": got, "ok": ok})
    return ok


fb = open(FREEZE, "rb").read()
check("FREEZE.json sha256", sha_bytes(fb), EXP_FREEZE_SHA)
check("FREEZE.json bytes", len(fb), EXP_FREEZE_BYTES)
fz = json.loads(fb.decode("utf-8"))

# o FREEZE tambem traz os proprios valores; conferir enunciado == FREEZE == bytes
pj = fz["preregistro_json"]
pm = fz["preregistro_md"]
check("FREEZE.preregistro_json.sha256 == enunciado", pj["sha256"], EXP_JSON_SHA)
check("FREEZE.preregistro_md.sha256 == enunciado", pm["sha256"], EXP_MD_SHA)
s, n = sha_file(pj["arquivo"])
check("PREREGISTRO.json sha256", s, EXP_JSON_SHA)
check("PREREGISTRO.json bytes", n, EXP_JSON_BYTES)
s, n = sha_file(pm["arquivo"])
check("PREREGISTRO.md sha256", s, EXP_MD_SHA)
check("PREREGISTRO.md bytes", n, EXP_MD_BYTES)
for a in fz["anexos"]:
    p = os.path.join(PRE, a["caminho"].replace("/", os.sep))
    s, n = sha_file(p)
    check("anexo %s sha256" % a["caminho"], s, a["sha256"])
    check("anexo %s bytes" % a["caminho"], n, a["bytes"])

# texto do operador
ob = open(OPER, "rb").read()
so = sha_bytes(ob)
check("texto do operador sha256 (integral)", so, EXP_OPER_SHA)
check("texto do operador sha16", so[:16], EXP_OPER_SHA16)
p2 = ob[EXP_PARTE2_OFF:]
check("segunda parte comprimento (byte 2853 ate o fim)", len(p2), EXP_PARTE2_LEN)
check("segunda parte sha256", sha_bytes(p2), EXP_PARTE2_SHA)
inicio = "O que mais me fascina é a impossibilidade de definição do tempo".encode("utf-8")
check("segunda parte comeca na frase pre-registrada", p2[:len(inicio)] == inicio, True)

# um.py (somente leitura de bytes; NAO executado)
s, n = sha_file(UMPY)
check("um.py sha256 (v391)", s, EXP_UMPY_SHA)
out["um_py_bytes"] = n

# impressao digital do kernel registrada no FREEZE
kd = fz["kernel_impressao_digital"]
check("FREEZE kernel antes==depois", kd["iguais"], True)
check("FREEZE congelado_antes_de_qualquer_ensaio", fz["congelado_antes_de_qualquer_ensaio"], True)
check("FREEZE nenhum_teste_rodado", fz["nenhum_teste_rodado"], True)

out["all_ok"] = all(c["ok"] for c in out["checks"])
out["n_checks"] = len(out["checks"])
out["n_falhas"] = sum(1 for c in out["checks"] if not c["ok"])
with open(sys.argv[1], "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
print(json.dumps({"all_ok": out["all_ok"], "n_checks": out["n_checks"], "n_falhas": out["n_falhas"]}))
for c in out["checks"]:
    if not c["ok"]:
        print("DIVERGENCIA:", c)
sys.exit(0 if out["all_ok"] else 2)

# -*- coding: utf-8 -*-
"""A1 -- auditor REPRO r2: o FREEZE e anterior a TODOS os arquivos de 2_OPTICO e 3_KERNEL? (horarios e hashes)

So leitura fora de <r2>/saidas.  Mede:
  (1) hashes do FREEZE e do que ele congela; nenhum arquivo fora do manifesto em 1_PREREGISTRO;
  (2) horario do FREEZE (interno + mtime + birthtime) contra mtime E birthtime de cada arquivo de 2_OPTICO e 3_KERNEL;
  (3) quais arquivos de 2_OPTICO/3_KERNEL citam o sha256 do FREEZE / do PREREGISTRO (a cadeia de hash);
  (4) hashes dos artefatos declarados pelos construtores (task) contra os bytes;
  (5) o livro do mapa: prefixo de 1004 registros contra o pino 3636e6c83e1b5ee9 e horario do registro 1005.
"""
import datetime as dt, hashlib, json, os, sys

U = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
PRE = os.path.join(U, "1_PREREGISTRO")
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas", "A1_FREEZE.json")


def sha(p):
    with open(p, "rb") as fh:
        b = fh.read()
    return len(b), hashlib.sha256(b).hexdigest()


def utc(ns):
    return dt.datetime.fromtimestamp(ns / 1e9, dt.timezone.utc).isoformat()


def walk(d):
    for dp, dns, fns in os.walk(d):
        for fn in fns:
            yield os.path.join(dp, fn)


res = {}
# (1) FREEZE
fz_p = os.path.join(PRE, "FREEZE.json")
fz_b = open(fz_p, "rb").read()
fz = json.loads(fz_b.decode("utf-8"))
res["FREEZE_bytes_sha256"] = [len(fz_b), hashlib.sha256(fz_b).hexdigest()]
chk = {}
for nome in ("PREREGISTRO.json", "PREREGISTRO.md"):
    n, h = sha(os.path.join(PRE, nome))
    chk[nome] = {"medido": [n, h], "freeze": [fz[nome]["bytes"], fz[nome]["sha256"]],
                 "confere": (n == fz[nome]["bytes"] and h == fz[nome]["sha256"])}
demais = fz["demais_arquivos_da_pasta"]
dem_ok, dem_falhas = 0, []
for rel, (n0, h0) in demais.items():
    n, h = sha(os.path.join(PRE, rel.replace("/", os.sep)))
    if (n, h) == (n0, h0):
        dem_ok += 1
    else:
        dem_falhas.append([rel, [n0, h0], [n, h]])
na_pasta = sorted(os.path.relpath(p, PRE).replace("\\", "/") for p in walk(PRE))
esperados = set(demais) | {"PREREGISTRO.json", "PREREGISTRO.md", "FREEZE.json"}
fora = [r for r in na_pasta if r not in esperados]
faltam = [r for r in esperados if r not in na_pasta]
mt_pre = sorted(((os.stat(os.path.join(PRE, r)).st_mtime_ns, r) for r in na_pasta), reverse=True)[:3]
res["preregistro"] = {"principais": chk, "demais_n": len(demais), "demais_conferem": dem_ok,
                      "demais_falhas": dem_falhas, "arquivos_na_pasta": len(na_pasta),
                      "fora_do_manifesto": fora, "faltam": faltam,
                      "mtimes_mais_recentes": [[utc(t), r] for t, r in mt_pre]}

# (2) horarios
st = os.stat(fz_p)
t_int = dt.datetime.fromisoformat(fz["congelado_utc"])
t_int_ns = int(round(t_int.timestamp() * 1e9))
res["freeze_horario"] = {"congelado_utc_interno": fz["congelado_utc"], "mtime_utc": utc(st.st_mtime_ns),
                         "birthtime_utc": utc(int(st.st_birthtime * 1e9)),
                         "interno_<=_mtime": t_int_ns <= st.st_mtime_ns}
T0 = max(t_int_ns, st.st_mtime_ns)  # o mais tardio dos dois carimbos do FREEZE
pastas = {}
for sub in ("2_OPTICO", "3_KERNEL"):
    d = os.path.join(U, sub)
    linhas = []
    for p in walk(d):
        s = os.stat(p)
        bt = int(s.st_birthtime * 1e9)
        linhas.append((min(s.st_mtime_ns, bt), s.st_mtime_ns, bt, os.path.relpath(p, U)))
    linhas.sort()
    antes = [[utc(m), utc(b), r] for (_, m, b, r) in linhas if m <= T0 or b <= T0]
    pastas[sub] = {"n_arquivos": len(linhas),
                   "mais_antigo": {"min(mtime,birth)": utc(linhas[0][0]), "mtime": utc(linhas[0][1]),
                                   "birth": utc(linhas[0][2]), "arquivo": linhas[0][3]},
                   "folga_min_s": (linhas[0][0] - T0) / 1e9,
                   "arquivos_com_mtime_ou_birth_<=_FREEZE": antes}
res["pastas"] = pastas

# (3) cadeia de hash: quem cita o FREEZE / o PREREGISTRO
alvos = {"FREEZE.sha256": res["FREEZE_bytes_sha256"][1],
         "PREREGISTRO.json.sha256": chk["PREREGISTRO.json"]["medido"][1],
         "PREREGISTRO.md.sha256": chk["PREREGISTRO.md"]["medido"][1]}
cit = {k: [] for k in alvos}
for sub in ("2_OPTICO", "3_KERNEL"):
    for p in walk(os.path.join(U, sub)):
        if os.path.getsize(p) > 50_000_000:
            continue
        b = open(p, "rb").read()
        for k, h in alvos.items():
            if h.encode() in b or h[:16].encode() in b:
                cit[k].append(os.path.relpath(p, U))
res["citam_hash"] = {k: {"n": len(v), "exemplos": sorted(v)[:60]} for k, v in cit.items()}

# (4) artefatos declarados pelos construtores (texto da ordem)
decl = {
    r"2_OPTICO\RESULTADO_OPTICO.json": (137290, "28758b3eebdac6318d68ab0e069d13637fc4437adff43fa0e95b03da1d2acaaa"),
    r"2_OPTICO\run_optico.py": (None, "48a8d8b0d9fd125bf906a39f4f1bdb9df9f5e1dd12d2fdbe3e86dd456128c0e7"),
    r"2_OPTICO\LOG_OPTICO.txt": (None, "df3312fd0bb18d0b"),
    r"3_KERNEL\rodada2\RESULTADO_KERNEL.json": (82922, "9fd3c2044e410a57792b2f2c8c7c693e7ef1b97fc4e1193a8bcba09b135520c7"),
    r"3_KERNEL\rodada2\sandbox\TGLExt\TheUnitIsTheRank.lean": (103662, "3195ef8f0766384ca7d4d1ab2ddd7a9c3cdd28872957e4b8d0e72fa9f028a063"),
    r"3_KERNEL\rodada2\olean\TheUnitIsTheRank.olean": (None, "d0830b4bc03dc5615210c1d47e53c7a830c9e235b54fb37a09d2c6e368cf0d7b"),
    r"3_KERNEL\sandbox\TGLExt\TheUnitIsTheRank.lean": (None, "617155151fb0d9e1"),
    r"3_KERNEL\olean\TheUnitIsTheRank.olean": (None, "42b22d4f"),
    r"1_PREREGISTRO\FREEZE.json": (3993, "4d8f97537eb04cd58ad693d49270779817d325e0d58f88c2d7b2ca99fa76c425"),
}
art = {}
for rel, (n0, h0) in decl.items():
    n, h = sha(os.path.join(U, rel))
    art[rel] = {"medido": [n, h], "declarado": [n0, h0],
                "confere": (h.startswith(h0) and (n0 is None or n0 == n))}
res["artefatos_declarados"] = art

# (5) livro do mapa
L = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
lb = open(L, "rb").read()
linhas = lb.split(b"\n")
if linhas and linhas[-1] == b"":
    linhas = linhas[:-1]
pref = b"\n".join(linhas[:1004]) + b"\n"
regs = [json.loads(x.decode("utf-8")) for x in linhas]
def campo_tempo(r):
    for k in ("quando", "em", "ts", "utc", "registrado_em", "data", "quando_utc"):
        if k in r:
            return k, r[k]
    return None, None
res["livro"] = {"n_registros": len(regs), "bytes": len(lb),
                "prefixo_1004_bytes": len(pref), "prefixo_1004_sha256": hashlib.sha256(pref).hexdigest(),
                "pino_FREEZE": "3636e6c83e1b5ee9 (2505898 B)",
                "prefixo_confere": hashlib.sha256(pref).hexdigest().startswith("3636e6c83e1b5ee9") and len(pref) == 2505898,
                "reg1004": {"seq": regs[1003].get("seq"), "tempo": campo_tempo(regs[1003]), "sha": str(regs[1003].get("sha"))[:16]},
                "reg1005": {"seq": regs[1004].get("seq"), "tempo": campo_tempo(regs[1004]), "rota": regs[1004].get("rota_id")},
                "chaves_registro": sorted(regs[1004].keys())}

os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1)[:12000])

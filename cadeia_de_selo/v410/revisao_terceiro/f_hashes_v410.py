# -*- coding: utf-8 -*-
"""Revisor terceiro v410 (R1): hashes escritos nos JSONs da cadeia conferem com os arquivos (lidos agora, por script). So le.
(1) CANDIDATO_v410.json x candidato/base/runtime/bundle/kernel; (2) varredura GENERICA e recursiva de todo JSON de nivel superior, kernel/ e insumos/: todo dict que traga um caminho existente + sha256/sha16/bytes e'
conferido; todo par chave-caminho -> hash 64-hex idem; (3) BUNDLE/KERNEL_RECIBO x sandbox k410c; (4) o Nos (v409 selada) == base_v409/um.py; (5) os 23 verbatim x cunhagens_13out."""
import glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
R = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/"
NOS = "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s/"
SB = "C:/t/k410c/final/"
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
J = lambda p: json.load(open(R + p, encoding="utf-8"))
ok = {}; falhas = []


def chk(nome, cond, det=""):
    ok[nome] = bool(cond)
    if not cond: falhas.append((nome, det))
    print(("OK   " if cond else "FALHA"), nome, det if not cond else "")


cand = R + "um_v410_candidato.py"; h = sha(cand)
c = J("CANDIDATO_v410.json")
chk("CANDIDATO.sha16/sha256/bytes == arquivo", c["sha16"] == h[:16] and c["sha256"] == h and c["bytes"] == os.path.getsize(cand), (c["sha16"], h[:16]))
chk("CANDIDATO.base_v409_sha16 == base_v409/um.py", c["base_v409_sha16"] == sha(R + "base_v409/um.py")[:16] and c["base_v409_bytes"] == os.path.getsize(R + "base_v409/um.py"))
chk("CANDIDATO.delta_bytes", c["delta_bytes"] == os.path.getsize(cand) - os.path.getsize(R + "base_v409/um.py"))
chk("base_v409 == 53284ba461ecd940 (a v409 selada, escrita no pedido)", sha(R + "base_v409/um.py")[:16] == "53284ba461ecd940")
chk("Nos (v409 selada) um.py == base_v409/um.py", sha(NOS + "um.py") == sha(R + "base_v409/um.py"), "o Nos mudou?")
print("   Nos hoje: um.py", sha(NOS + "um.py")[:16], "| selo.um_version", json.load(open(NOS + "um_absoluto_selo.json", encoding="utf-8")).get("um_version"))
rt = c["runtime"]
chk("CANDIDATO.runtime == runtime_v410.py", rt["sha256"] == sha(R + "runtime_v410.py") and rt["bytes"] == os.path.getsize(R + "runtime_v410.py"), rt)
k = c["kernel"]
chk("kernel.raiz_sha16 == TGLExt.lean sandbox", k["raiz_sha16"] == sha(SB + "TGLExt.lean")[:16])
chk("kernel.audit_sha16 == TGL/Audit.lean sandbox", k["audit_sha16"] == sha(SB + "TGL/Audit.lean")[:16])
chk("kernel.audit_v409 == audit v410 (Audit nao muda)", k["audit_v409_sha16"] == k["audit_sha16"])
chk("kernel.raiz_v409_sha16 == raiz do Nos", k["raiz_v409_sha16"] == sha(NOS + "tgl_kernel/TGLExt.lean")[:16], (k["raiz_v409_sha16"], sha(NOS + "tgl_kernel/TGLExt.lean")[:16]))
bz = 0
for rel, e in k["bundle"].items():
    p = SB + rel
    if os.path.exists(p) and sha(p)[:16] == e["sha16"] and sha(p) == e["sha256"]: bz += 1
chk("CANDIDATO.kernel.bundle (%d) == sandbox" % len(k["bundle"]), bz == len(k["bundle"]) == 2, bz)
B = J("BUNDLE_v410.json")
bz = sum(1 for mo in B["modulos"] if sha(SB + mo["rel"]) == mo["sha256"] == sha(R + "pedra/" + os.path.basename(mo["rel"])))
chk("BUNDLE 2 sha256 == sandbox == pedra/", bz == 2 == B["n"], bz)
bo = sum(1 for mo in B["modulos"] if os.path.exists(R + "pedra/origem/" + os.path.basename(mo["origem"])) and sha(R + "pedra/origem/" + os.path.basename(mo["origem"])) == mo["sha256_origem"])
chk("BUNDLE.sha256_origem == pedra/origem/<arquivo>", bo == 2, bo)
bo2 = sum(1 for mo in B["modulos"] if os.path.exists(mo["origem"]) and sha(mo["origem"]) == mo["sha256_origem"])
chk("BUNDLE.origem (insumos\\) == sha256_origem", bo2 == 2, bo2)
chk("BUNDLE.recibo_dos_nomes_sha256 == arquivo", sha(B["recibo_dos_nomes"]) == B["recibo_dos_nomes_sha256"])
# (2) varredura generica
pares = {"n": 0, "ok": 0}; ruins = []


def tem_hex(s): return isinstance(s, str) and re.fullmatch(r"[0-9a-f]{64}", s)


def varre(o, fonte, cam=""):
    if isinstance(o, dict):
        cam_ = None
        for kk in ("arquivo", "path", "caminho", "file"):
            v = o.get(kk)
            if isinstance(v, str) and (":" in v[:3] or v.startswith("/")) and os.path.isfile(v):
                cam_ = v; break
        if cam_:
            s256 = o.get("sha256") if tem_hex(o.get("sha256")) else None
            s16 = o.get("sha16") if isinstance(o.get("sha16"), str) and len(o.get("sha16")) == 16 else None
            by = o.get("bytes") if isinstance(o.get("bytes"), int) else None
            if s256 or s16 or by is not None:
                pares["n"] += 1
                real = sha(cam_)
                bom = (s256 is None or s256 == real) and (s16 is None or s16 == real[:16]) and (by is None or by == os.path.getsize(cam_))
                if bom: pares["ok"] += 1
                else: ruins.append((fonte, cam + "/" + kk, cam_, s256 and s256[:16], s16, by, real[:16], os.path.getsize(cam_)))
        for kk, v in o.items(): varre(v, fonte, cam + "/" + str(kk))
    elif isinstance(o, list):
        for i, v in enumerate(o): varre(v, fonte, cam + "[%d]" % i)


alvos = sorted(glob.glob(R + "*.json")) + sorted(glob.glob(R + "kernel/*.json")) + sorted(glob.glob(R + "insumos/*.json")) + sorted(glob.glob(R + "pos_rito/*.json")) + sorted(glob.glob(R + "bancada_B3_servico/*.json"))
alvos = [a for a in alvos if os.path.getsize(a) < 40_000_000 and not any(x in os.path.basename(a) for x in (".pre_", "EXAME_PONTOS", "SIMULACAO_ARVORE", "acom_c1", "acom_prep", ".bak"))]
for a in alvos:
    try: varre(json.load(open(a, encoding="utf-8")), os.path.relpath(a, R))
    except Exception as e: print("   (nao li)", os.path.basename(a), repr(e)[:80])
print("   varredura generica: %d JSON; pares {caminho + hash/bytes} existentes: %d, conferem: %d" % (len(alvos), pares["n"], pares["ok"]))
chk("varredura generica: todo par {caminho existente + sha/bytes} confere", not ruins, len(ruins))
for r_ in ruins[:40]: print("   DIVERGE:", r_)
# (5) os 23 verbatim
vc = J("VERBATIM_CONGELADO_v410.json"); n_ok = 0
for reg in vc["registro"]:
    p = reg["arquivo"]
    if os.path.exists(p) and sha(p) == reg["sha256"]: n_ok += 1
chk("VERBATIM_CONGELADO: %d falas existem e o sha256 confere" % len(vc["registro"]), n_ok == len(vc["registro"]) == vc["n"], n_ok)
# PINOS / PINO_MEMORIA / PREPARACAO
for nome in ("PINO_MEMORIA_PY_v410.json", "PINOS_BN_v410.json", "PINO_RECIBO_PRE_SELO_v410.json"):
    print("   ", nome, "sha16", sha(R + nome)[:16], "bytes", os.path.getsize(R + nome))
pr = J("PREPARACAO_v410_PRONTA.json")
chk("PREPARACAO.candidato_sha16 == arquivo", pr["candidato_sha16"] == h[:16] and pr["candidato_bytes"] == os.path.getsize(cand), (pr["candidato_sha16"], h[:16]))
chk("PREPARACAO.pronta True e falta vazia", pr["pronta"] is True and pr["falta"] == [], (pr["pronta"], pr["falta"]))
hs = pr.get("hashes") or {}
n_h = sum(1 for kk, v in hs.items() if isinstance(v, dict) and os.path.exists(R + kk) and v.get("sha16") == sha(R + kk)[:16])
print("   PREPARACAO.hashes entradas:", len(hs), "conferem (arquivo na pasta v410):", n_h)
ruins2 = [(kk, v) for kk, v in hs.items() if isinstance(v, dict) and os.path.exists(R + kk) and v.get("sha16") != sha(R + kk)[:16]]
for kk, v in ruins2[:30]: print("   MUDOU desde a PRONTA:", kk, v.get("sha16"), "->", sha(R + kk)[:16])
chk("PREPARACAO.hashes: nenhum arquivo mudou desde a PRONTA", not ruins2, len(ruins2))
res = {"ok": ok, "falhas": falhas, "pares": pares, "ruins": [list(map(str, r_)) for r_ in ruins], "preparacao_hashes": {"n": len(hs), "conferem": n_h, "mudou": [(kk, v.get("sha16"), sha(R + kk)[:16]) for kk, v in ruins2]}}
json.dump(res, open(R + "revisao_terceiro/f_hashes_v410_out.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("FALHAS:", len(falhas))

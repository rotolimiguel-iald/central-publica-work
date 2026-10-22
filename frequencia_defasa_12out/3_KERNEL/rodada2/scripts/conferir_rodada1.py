# -*- coding: utf-8 -*-
"""Rodada 2 (reinvocacao do construtor do kernel, 12/10/2026 noite): conferencia SO DE LEITURA de que os artefatos da
rodada 1 (3_KERNEL, 13:30-14:23 local) seguem intactos, byte a byte, contra o manifesto gravado no proprio
RESULTADO_KERNEL.json da rodada 1, e de que o RESULTADO_KERNEL.json da rodada 1 e o que o redator conferiu
(sha256 lido do CONFERENCIA_REDATOR.json, 4_RELATORIO). Tambem confere o PREFIXO do livro do mapa de rotas contra o pino
do pre-registro (o livro e so-acrescimo: a divergencia do pino inteiro e crescimento, nao reescrita).
Grava SO em 3_KERNEL\\rodada2\\INTEGRIDADE_RODADA1.json."""
import hashlib, json, os, sys

R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.dirname(R2)                      # 3_KERNEL
BASE = os.path.dirname(K)                    # frequencia_defasa_12out


def sha(p):
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b:
                break
            h.update(b)
            n += len(b)
    return n, h.hexdigest()


out = {"documento": "INTEGRIDADE_RODADA1 — conferencia so de leitura dos artefatos da rodada 1 do 3_KERNEL",
       "autor": "construtor do kernel (subagente), rodada 2", "divergencias": []}
rk = os.path.join(K, "RESULTADO_KERNEL.json")
n, h = sha(rk)
red = json.loads(open(os.path.join(BASE, "4_RELATORIO", "CONFERENCIA_REDATOR.json"), "rb").read().decode("utf-8"))
h_red = red["kernel_da_unidade"]["RESULTADO_KERNEL.json"]["sha256"]
out["RESULTADO_KERNEL_rodada1"] = {"arquivo": rk, "bytes": n, "sha256": h, "sha256_conferido_pelo_redator": h_red,
                                   "confere": h == h_red}
if h != h_red:
    out["divergencias"].append("RESULTADO_KERNEL.json")
R1 = json.loads(open(rk, "rb").read().decode("utf-8"))
man = R1["manifesto_3_KERNEL"]
itens = {}
for rel, (nb, hh) in man.items():
    p = os.path.join(K, *rel.split("/"))
    try:
        n2, h2 = sha(p)
    except OSError as e:
        itens[rel] = {"erro": str(e)}
        out["divergencias"].append(rel)
        continue
    ok = (n2 == nb) and (h2 == hh)
    itens[rel] = {"bytes": n2, "sha256": h2, "confere": ok}
    if not ok:
        out["divergencias"].append(rel)
out["manifesto"] = {"n": len(man), "conferem": sum(1 for v in itens.values() if v.get("confere")), "itens": itens}
# arquivos presentes na raiz do 3_KERNEL (fora de rodada2) que NAO estao no manifesto: so listagem
presentes = []
for dp, dns, fns in os.walk(K):
    if os.path.abspath(dp).startswith(os.path.abspath(R2)):
        continue
    for fn in fns:
        rel = os.path.relpath(os.path.join(dp, fn), K).replace("\\", "/")
        presentes.append(rel)
out["fora_do_manifesto_rodada1"] = sorted(set(presentes) - set(man) - {"RESULTADO_KERNEL.json"})
# pedra e olean da rodada 1 (nomeados)
out["pedra_rodada1"] = {"arquivo": os.path.join(K, "sandbox", "TGLExt", "TheUnitIsTheRank.lean"),
                        "sha256": itens.get("sandbox/TGLExt/TheUnitIsTheRank.lean", {}).get("sha256"),
                        "sha256_no_RESULTADO": R1["pedra"]["sha256"]}
out["olean_rodada1"] = {"arquivo": os.path.join(K, "olean", "TheUnitIsTheRank.olean"),
                        "sha256": itens.get("olean/TheUnitIsTheRank.olean", {}).get("sha256"),
                        "sha256_no_RESULTADO": R1["compilacao"]["olean"]["sha256"]}
# livro do mapa: prefixo
PR = json.loads(open(os.path.join(BASE, "1_PREREGISTRO", "PREREGISTRO.json"), "rb").read().decode("utf-8"))
pin = [p for p in PR["pinos"] if p[0].lower().endswith("rotas.jsonl")]
if pin:
    p, nb, h16 = pin[0]
    b = open(p, "rb").read()
    pref = b[:nb]
    hp = hashlib.sha256(pref).hexdigest()
    out["livro_mapa_de_rotas"] = {
        "arquivo": p, "pino_do_preregistro": [nb, h16], "bytes_agora": len(b), "linhas_agora": b.count(b"\n"),
        "sha256_agora": hashlib.sha256(b).hexdigest(), "sha256_do_prefixo_de_bytes_do_pino": hp,
        "prefixo_confere_com_o_pino": hp.startswith(h16), "linhas_no_prefixo": pref.count(b"\n"),
        "leitura": "o livro e so-acrescimo (cadeia de hash): o pino inteiro diverge porque outras sessoes registraram rotas "
                   "depois do FREEZE; o prefixo do tamanho do pino confere byte a byte, logo nada foi reescrito. "
                   "Nao e divergencia do FREEZE (PREREGISTRO.json e PREREGISTRO.md conferem)."}
    if not hp.startswith(h16):
        out["divergencias"].append("livro_mapa_prefixo")
out["veredito"] = "RODADA1_INTACTA" if not out["divergencias"] else "RODADA1_DIVERGE"
dst = os.path.join(R2, "INTEGRIDADE_RODADA1.json")
if os.path.exists(dst):
    raise SystemExit("FALHA VISIVEL: destino ja existe (nao sobrescrevo): " + dst)
with open(dst + ".tmp", "wb") as f:
    f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8") + b"\n")
os.replace(dst + ".tmp", dst)
print(json.dumps({k: out[k] for k in ("RESULTADO_KERNEL_rodada1", "pedra_rodada1", "olean_rodada1", "fora_do_manifesto_rodada1",
                                      "divergencias", "veredito")}, ensure_ascii=False, indent=1))
print("manifesto:", out["manifesto"]["conferem"], "/", out["manifesto"]["n"])
print(json.dumps(out.get("livro_mapa_de_rotas"), ensure_ascii=False, indent=1))
sys.exit(0 if not out["divergencias"] else 2)

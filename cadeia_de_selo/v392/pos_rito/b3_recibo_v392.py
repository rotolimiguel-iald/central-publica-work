# -*- coding: utf-8 -*-
"""b3_recibo_v392.py -- confere o que o sincronizar_bancada.py (o elo B(3), esboco R3.3) imprimiu: a ULTIMA linha JSON do stdout cita o recibo; o recibo e' aberto, o seu sha256
confere com o impresso, e (R3, Remissao 4) a bateria PASSA, a versao alvo e' v392, a fase e' pos_selo e o modo e' o pedido.
uso: python -I -B -X utf8 b3_recibo_v392.py <arquivo com o stdout do esboco> ensaio|aplicar
rc 0 = confere; rc 1 = nao confere (a cadeia PARA). Nao escreve nada. NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")


def main(argv):
    if len(argv) != 3 or argv[2] not in ("ensaio", "aplicar"):
        print("uso: b3_recibo_v392.py <stdout> ensaio|aplicar"); return 1
    linhas = [l for l in open(argv[1], encoding="utf-8", errors="replace").read().splitlines() if l.strip().startswith("{")]
    if not linhas:
        print("B3 %s: o stdout nao traz a linha JSON do esboco" % argv[2]); return 1
    try:
        imp = json.loads(linhas[-1])
    except ValueError as e:
        print("B3 %s: a ultima linha JSON nao le: %r" % (argv[2], e)); return 1
    rp = imp.get("recibo")
    if not rp or not os.path.isfile(rp):
        print("B3 %s: sem recibo (veredito %r, recusa %r)" % (argv[2], imp.get("veredito"), imp.get("recusa"))); return 1
    raw = open(rp, "rb").read()
    if hashlib.sha256(raw).hexdigest() != imp.get("recibo_sha256"):
        print("B3 %s: o sha256 do recibo nao confere com o impresso" % argv[2]); return 1
    r = json.loads(raw.decode("utf-8"))
    bat = (r.get("bateria_resultado") or {}).get("veredito"); ver = str(r.get("veredito") or "")
    prob = []
    if os.path.basename(rp).startswith("RECUSA_"):
        prob.append("o arquivo e' uma RECUSA")
    if r.get("versao_alvo") != "v392" or r.get("fase") != "pos_selo" or r.get("modo") != argv[2]:
        prob.append("versao/fase/modo do recibo: %r %r %r" % (r.get("versao_alvo"), r.get("fase"), r.get("modo")))
    if bat != "BATERIA_PASSA":
        prob.append("bateria: %r" % bat)
    if argv[2] == "aplicar" and not (ver.startswith("REPINADA_B") and r.get("aplicacao")):
        prob.append("o veredito do aplicar nao e' REPINADA_B* com aplicacao: %r" % ver)
    if argv[2] == "ensaio" and ver.startswith(("RECUSA", "RECUSADA")):
        prob.append("veredito do ensaio: %r" % ver)
    print("B3 %s: veredito=%s bateria=%s recibo=%s sha16=%s manifesto_novo=%s" % (argv[2], ver, bat, rp, imp.get("recibo_sha256", "")[:16], ((r.get("manifesto_novo") or {}).get("sha256") or "")[:16]))
    for p in prob:
        print("  PROBLEMA:", p)
    return 1 if prob else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

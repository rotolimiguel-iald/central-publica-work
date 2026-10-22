# -*- coding: utf-8 -*-
"""b3_recibo_v394.py -- confere o que o sincronizar_bancada.py (o elo B(n), esboco R3.5: SALTO v392 -> v394) imprimiu: a ULTIMA linha JSON do stdout cita o recibo; o recibo e' aberto, o seu sha256 confere com o impresso,
e (R3, Remissao 4) a bateria PASSA, a versao alvo e' v394, a fase e' pos_selo e o modo e' o pedido. R3.5: com o 3o argumento (o sha256 da cadeia de selos, lido de PINOS_BN) o recibo tem de DECLARAR o salto:
salto.declarado, salto.cadeia.sha256 == o pino, proxima_a_selar == v394, o veredito nomeia o salto (__SALTO_) e os pinos da versao da bateria sao os da v394, conferidos contra o Nos lido.
uso: python -I -B -X utf8 b3_recibo_v394.py <arquivo com o stdout do esboco> ensaio|aplicar [<sha256 da cadeia de selos>]
rc 0 = confere; rc 1 = nao confere (a cadeia PARA). Nao escreve nada. NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")


def main(argv):
    if len(argv) not in (3, 4) or argv[2] not in ("ensaio", "aplicar"):
        print("uso: b3_recibo_v394.py <stdout> ensaio|aplicar [<sha256 da cadeia de selos>]"); return 1
    linhas = [l for l in open(argv[1], encoding="utf-8", errors="replace").read().splitlines() if l.strip().startswith("{")]
    if not linhas:
        print("B(n) %s: o stdout nao traz a linha JSON do esboco" % argv[2]); return 1
    try:
        imp = json.loads(linhas[-1])
    except ValueError as e:
        print("B(n) %s: a ultima linha JSON nao le: %r" % (argv[2], e)); return 1
    rp = imp.get("recibo")
    if not rp or not os.path.isfile(rp):
        print("B(n) %s: sem recibo (veredito %r, recusa %r)" % (argv[2], imp.get("veredito"), imp.get("recusa"))); return 1
    raw = open(rp, "rb").read()
    if hashlib.sha256(raw).hexdigest() != imp.get("recibo_sha256"):
        print("B(n) %s: o sha256 do recibo nao confere com o impresso" % argv[2]); return 1
    r = json.loads(raw.decode("utf-8"))
    bat = (r.get("bateria_resultado") or {}).get("veredito"); ver = str(r.get("veredito") or "")
    prob = []
    if os.path.basename(rp).startswith("RECUSA_"):
        prob.append("o arquivo e' uma RECUSA")
    if r.get("versao_alvo") != "v394" or r.get("fase") != "pos_selo" or r.get("modo") != argv[2]:
        prob.append("versao/fase/modo do recibo: %r %r %r" % (r.get("versao_alvo"), r.get("fase"), r.get("modo")))
    if bat != "BATERIA_PASSA":
        prob.append("bateria: %r" % bat)
    if argv[2] == "aplicar" and not (ver.startswith("REPINADA_B") and r.get("aplicacao")):
        prob.append("o veredito do aplicar nao e' REPINADA_B* com aplicacao: %r" % ver)
    if argv[2] == "ensaio" and ver.startswith(("RECUSA", "RECUSADA")):
        prob.append("veredito do ensaio: %r" % ver)
    salto = r.get("salto")
    if len(argv) == 4:      # R3.5: a Bancada de producao pina a v392: o recibo tem de declarar o SALTO, com a cadeia pinada, e a bateria tem de ser a da v394
        cad = argv[3].lower()
        if not isinstance(salto, dict) or salto.get("declarado") is not True:
            prob.append("o recibo nao declara o salto (a Bancada pina uma versao anterior a v393)")
        else:
            if (salto.get("cadeia") or {}).get("sha256") != cad:
                prob.append("a cadeia de selos do salto no recibo (%r) nao e a pinada (%r)" % ((salto.get("cadeia") or {}).get("sha256"), cad))
            if salto.get("proxima_a_selar") != "v394":
                prob.append("salto.proxima_a_selar=%r (esperado v394)" % salto.get("proxima_a_selar"))
            if "__SALTO_" not in ver:
                prob.append("o veredito nao nomeia o salto: %r" % ver)
        pv = (r.get("bateria") or {}).get("pinos_da_versao") or {}
        if pv.get("versao") != "v394" or pv.get("declarados") is not True or pv.get("conferidos_contra_o_nos_lido") is not True:
            prob.append("os pinos da versao da bateria nao sao os da v394 conferidos contra o Nos lido: %r" % {k: pv.get(k) for k in ("declarados", "versao", "conferidos_contra_o_nos_lido")})
    print("B(n) %s: veredito=%s bateria=%s recibo=%s sha16=%s manifesto_novo=%s salto=%s" % (argv[2], ver, bat, rp, imp.get("recibo_sha256", "")[:16], ((r.get("manifesto_novo") or {}).get("sha256") or "")[:16],
                                                                                       ("%s->%s puladas=%s" % (salto["de"]["versao"], r.get("versao_alvo"), salto["versoes_puladas"])) if isinstance(salto, dict) else None))
    for p in prob:
        print("  PROBLEMA:", p)
    return 1 if prob else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

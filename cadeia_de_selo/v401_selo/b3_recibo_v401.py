# -*- coding: utf-8 -*-
"""b3_recibo_v401.py -- confere o que o sincronizar_bancada.py (o elo B(n), esboco R3.5: PASSO SIMPLES v400 -> v401, SEM salto e SEM cadeia de selos) imprimiu: a ULTIMA linha JSON do stdout cita o recibo; o recibo e' aberto,
o seu sha256 confere com o impresso, e (R3, Remissao 4) a bateria PASSA, a versao alvo e' v401, a fase e' pos_selo e o modo e' o pedido.
Passo simples (a Bancada de producao pina a v400 e o Nos passou a v401): (1) manifesto_anterior.version == v400 e a sua geracao (B<m>, lida do proprio recibo) bate com a do recibo pre_selo pinado em PINOS_BN_v401.json (o manifesto anterior
e' o mesmo que o recibo pre_selo viu, por sha256: a producao nao mudou entre o pre_selo e agora); (2) o numero do B novo e' n = m + 1; (3) o veredito e' EXATAMENTE REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA (ensaio) ou
REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO (aplicar), sem __SALTO_; (4) o recibo NAO declara salto nem cadeia de selos; (5) manifesto_novo.deployment_id comeca por B<n>-v401-; (6) no aplicar, a pos_conferencia
diz ok, versao v401 e o sha do manifesto novo; (7) os pinos da versao da bateria sao os da v401, conferidos contra o Nos lido; (8) o recibo pre_selo do recibo e' o pinado.
O texto exato dos vereditos e' o do esboco R3.5 (sincronizar_bancada.py, `veredito_base + "__ENSAIO__NADA_GRAVADO_NA_BANCADA"` e `veredito_base + "__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO"`, com veredito_base = "REPINADA_B%d" % n) [lido do codigo, nao rodado].
uso: python -I -B -X utf8 b3_recibo_v401.py <arquivo com o stdout do esboco> ensaio|aplicar      (SEM terceiro argumento: nao ha cadeia de selos)
rc 0 = confere; rc 1 = nao confere (a cadeia PARA). Nao escreve nada. NOT_FALSIFIED nao e' a palavra da creditacao; o gate nao se move."""
import hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
RX_GERACAO = re.compile(r"^B(\d+)-")


def _geracao(deployment_id):
    m = RX_GERACAO.match(str(deployment_id or ""))
    return int(m.group(1)) if m else None


def main(argv):
    if len(argv) != 3 or argv[2] not in ("ensaio", "aplicar"):
        print("uso: b3_recibo_v401.py <stdout> ensaio|aplicar   (sem terceiro argumento: a v401 e' um passo simples, sem cadeia de selos)"); return 1
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
    if r.get("versao_alvo") != "v401" or r.get("fase") != "pos_selo" or r.get("modo") != argv[2]:
        prob.append("versao/fase/modo do recibo: %r %r %r" % (r.get("versao_alvo"), r.get("fase"), r.get("modo")))
    if bat != "BATERIA_PASSA":
        prob.append("bateria: %r" % bat)
    # (1) e (2): a geracao do manifesto anterior (da Bancada de producao) e o numero do B novo
    ma = r.get("manifesto_anterior") or {}; m = _geracao(ma.get("deployment_id")); n = (m + 1) if m is not None else None
    if m is None:
        prob.append("manifesto_anterior sem deployment_id de geracao (B<n>-...): %r" % (ma.get("deployment_id"),))
    if ma.get("version") != "v400":
        prob.append("a Bancada de producao nao pinava a v400 (manifesto_anterior.version = %r): o passo da v401 e' simples v400 -> v401" % (ma.get("version"),))
    # o recibo pre_selo pinado: o mesmo que o recibo viu, e o manifesto anterior e' o que ELE viu (a producao nao mudou entre o pre_selo e agora)
    try:
        pinos = json.load(open(os.path.join(PK, "PINOS_BN_v401.json"), encoding="utf-8")); pr = pinos["recibo_pre_selo"]
        if "cadeia_de_selos" in pinos:
            prob.append("PINOS_BN_v401.json traz o pino cadeia_de_selos: a v401 nao tem salto")
        prb = open(pr["path"], "rb").read()
        if hashlib.sha256(prb).hexdigest() != pr["sha256"]:
            prob.append("o recibo pre_selo em disco diverge do pino (%s)" % pr["path"])
        else:
            pre = json.loads(prb.decode("utf-8")); mp = pre.get("manifesto_anterior") or {}
            if (mp.get("sha256"), mp.get("deployment_id"), mp.get("version")) != (ma.get("sha256"), ma.get("deployment_id"), ma.get("version")):
                prob.append("o manifesto anterior do recibo (%s %s) != o do recibo pre_selo pinado (%s %s): a Bancada de producao mudou desde o pre_selo" % (
                    ma.get("deployment_id"), str(ma.get("sha256"))[:16], mp.get("deployment_id"), str(mp.get("sha256"))[:16]))
            if _geracao(((pr.get("bancada_pina") or {}).get("deployment_id"))) != m:
                prob.append("a geracao do manifesto anterior (%r) != a que o PINOS_BN registra para a Bancada (%r)" % (m, (pr.get("bancada_pina") or {}).get("deployment_id")))
        if ((r.get("recibo_pre_selo") or {}).get("sha256")) != pr["sha256"]:
            prob.append("o recibo pre_selo do recibo (%s) nao e' o pinado (%s)" % (str((r.get("recibo_pre_selo") or {}).get("sha256"))[:16], pr["sha256"][:16]))
    except (OSError, KeyError, ValueError) as e:
        prob.append("nao li o recibo pre_selo pinado em PINOS_BN_v401.json: %r" % (e,))
    # (3): o veredito exato; (4): sem salto e sem cadeia
    if n is not None:
        esperado = ("REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" if argv[2] == "ensaio" else "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO") % n
        if ver != esperado:
            prob.append("o veredito %r nao e' o esperado %r" % (ver, esperado))
    if "__SALTO_" in ver or r.get("salto") not in (None, {}) or r.get("cadeia_de_selos") not in (None, {}):
        prob.append("o recibo declara salto ou cadeia de selos: o passo da v401 e' simples (a Bancada pinava a v400)")
    # (5) e (6)
    mn = r.get("manifesto_novo") or {}
    if n is not None and not str(mn.get("deployment_id") or "").startswith("B%d-v401-" % n):
        prob.append("manifesto_novo.deployment_id=%r (esperado B%s-v401-...)" % (mn.get("deployment_id"), n))
    ap = r.get("aplicacao")
    if argv[2] == "aplicar":
        pc = (ap or {}).get("pos_conferencia") or {}
        if not ap:
            prob.append("o aplicar nao traz a aplicacao")
        elif not (pc.get("ok") is True and pc.get("canonical_version") == "v401" and pc.get("canonical_manifest_sha256") == mn.get("sha256")):
            prob.append("a pos_conferencia do aplicar nao diz ok, versao v401 e o sha do manifesto novo: %r" % {k: pc.get(k) for k in ("ok", "canonical_version", "canonical_manifest_sha256")})
    elif ap:
        prob.append("o ENSAIO traz uma aplicacao (nada podia ter sido gravado)")
    # (7): a bateria por versao
    pv = (r.get("bateria") or {}).get("pinos_da_versao") or {}
    if pv.get("versao") != "v401" or pv.get("declarados") is not True or pv.get("conferidos_contra_o_nos_lido") is not True:
        prob.append("os pinos da versao da bateria nao sao os da v401 conferidos contra o Nos lido: %r" % {k: pv.get(k) for k in ("declarados", "versao", "conferidos_contra_o_nos_lido")})
    print("B(n) %s: veredito=%s bateria=%s recibo=%s sha16=%s manifesto_novo=%s anterior=%s" % (argv[2], ver, bat, rp, imp.get("recibo_sha256", "")[:16], (mn.get("sha256") or "")[:16], ma.get("deployment_id")))
    for p in prob:
        print("  PROBLEMA:", p)
    return 1 if prob else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

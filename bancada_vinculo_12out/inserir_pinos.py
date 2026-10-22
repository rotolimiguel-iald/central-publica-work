# -*- coding: utf-8 -*-
"""inserir_pinos.py -- poe em VINCULO_BANCADA_UMPY.md, no marcador <!-- TABELA_PINOS -->, a tabela gerada por medir_pinos.py (PINOS_12out.md)
e, no marcador <!-- RESULTADOS_SANDBOX -->, o resumo dos recibos do sandbox lido dos proprios JSON. Backup de bytes do .md antes de tocar."""
import json, glob, hashlib, time
from pathlib import Path
AQUI = Path(__file__).resolve().parent
MD = AQUI / "VINCULO_BANCADA_UMPY.md"
tab = (AQUI / "PINOS_12out.md").read_text(encoding="utf-8").split("\n", 2)[2]


def resumo_recibo(p):
    d = json.loads(Path(p).read_bytes())
    b = d.get("bateria_resultado") or {}
    linhas = ["- `%s` (sha16 `%s`): fase **%s**, modo **%s**, veredito **%s**" % (Path(p).name, hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16], d.get("fase"), d.get("modo"), d.get("veredito"))]
    n = d.get("nos") or {}
    linhas.append("  - Nós: UM_VERSION `%s`; um.py `%s` (%s B); selo `%s`; α na linha %s (%s linha não indentada); β runtime `%s`; β core `%s` (dif. rel. %.2e, tolerância %s)" % (
        n.get("UM_VERSION"), (n.get("um_py") or {}).get("sha256", "")[:16], (n.get("um_py") or {}).get("bytes"), (n.get("selo") or {}).get("sha256", "")[:16],
        (n.get("alpha") or {}).get("linha"), (n.get("alpha") or {}).get("n_linhas_nao_indentadas"), n.get("beta_runtime"), (n.get("core") or {}).get("beta_core"),
        (n.get("core") or {}).get("beta_rel_diff") or 0.0, (n.get("core") or {}).get("tolerancia_rel")))
    ma = d.get("manifesto_anterior") or {}
    linhas.append("  - manifesto anterior: `%s` (`%s`), estado do contrato instalado: `%s`" % (ma.get("deployment_id"), str(ma.get("sha256"))[:16], ma.get("estado_do_contrato_instalado")))
    if d.get("sonda_pos_selo_em_ram"):
        linhas.append("  - sonda em RAM (o canonical.py instalado com os bytes do Nós alvo no caminho pinado): recusou = %s, código `%s`" % (d["sonda_pos_selo_em_ram"]["recusou"], d["sonda_pos_selo_em_ram"]["codigo"]))
    mn = d.get("manifesto_novo")
    if mn:
        linhas.append("  - manifesto regenerado: `%s` (`%s`, %s B; %s código, %s fontes; contrato `%s` `%s`)" % (mn.get("deployment_id"), str(mn.get("sha256"))[:16], mn.get("bytes"), mn.get("n_code"), mn.get("n_sources"), mn.get("contrato"), str(mn.get("contrato_sha256"))[:16]))
    rp = d.get("repinagem") or {}
    linhas.append("  - re-pino conferido pelo canonical.py instalado: ok=%s, versão `%s`, um.py `%s`, β `%r`, deployment `%s`" % (rp.get("ok"), rp.get("canonical_version"), str(rp.get("um_py_sha256"))[:16], rp.get("beta_tgl"), rp.get("deployment_id")))
    if d.get("recibo_pre_selo"):
        linhas.append("  - recibo pré-selo exigido e lido por hash: `%s`" % str(d["recibo_pre_selo"].get("sha256"))[:16])
    linhas.append("  - bateria: **%s** — %s testes, %s PASSA, %s FALHA, %s NAO_EXECUTADO" % (b.get("veredito"), b.get("n"), b.get("passa"), b.get("falha"), b.get("nao_executado")))
    for t in b.get("testes", []):
        linhas.append("    - %s: **%s**%s — %s" % (t["id"], t["resultado"], (" (%.1f s)" % t["segundos"]) if t.get("segundos") is not None else "", (t.get("detalhe") or "")[:140]))
    ap = d.get("aplicacao")
    if ap:
        linhas.append("  - aplicação na cópia: manifesto gravado, backup `%s` (`%s`), contrato `%s`; reconferência pós-gravação ok=%s versão `%s`; recibo copiado para `%s`" % (
            Path(ap.get("backup", "")).name, str(ap.get("backup_sha256"))[:16], Path(ap.get("contrato", "")).name, (ap.get("pos_conferencia") or {}).get("ok"),
            (ap.get("pos_conferencia") or {}).get("canonical_version"), ap.get("copia_do_recibo", "").replace(str(AQUI), "...")))
    return "\n".join(linhas)


blocos = []
for p in sorted(glob.glob(str(AQUI / "sandbox" / "saida_*" / "RECIBO_SINCRONIZACAO_*.json"))):
    blocos.append(resumo_recibo(p))
cn = AQUI / "sandbox" / "controles_negativos" / "CONTROLES_NEGATIVOS.json"
if cn.is_file():
    c = json.loads(cn.read_bytes())
    linhas = ["- `CONTROLES_NEGATIVOS.json` (sha16 `%s`): **%s** (%s de %s)" % (hashlib.sha256(cn.read_bytes()).hexdigest()[:16], c["veredito"], c["passam"], c["n"])]
    for x in c["controles"]:
        linhas.append("  - %s: rc %s (esperado %s); recusa `%s`; manifesto da cópia intocado = %s → **%s**" % (x["controle"], x["rc"], x["rc_esperado"], x.get("recusa") or x.get("veredito"), x["manifesto_da_copia_intocado"], "PASSA" if x["passa"] else "FALHA"))
    blocos.append("\n".join(linhas))
sm = AQUI / "sandbox" / "canais_gerados" / "SMOKE_TEST.json"
if sm.is_file():
    s = json.loads(sm.read_bytes())
    blocos.append("- canais gerados (`sandbox\\canais_gerados\\SMOKE_TEST.json`): consultar(`bancada_fases_5_6_7_v380`) ok=%s, %s artefatos por hash, versão `%s`, gate `%s`; recusas: artefato adulterado em RAM → `ARTEFATO_DIVERGE_DA_DECLARACAO`, canal desconhecido → `CANAL_DESCONHECIDO`" % (s["ok"], s["n_artefatos"], s["versao"], s["gate_effect"]))
res = "\n\n".join(blocos) + "\n"
raw = MD.read_bytes()
bak = MD.with_name(MD.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S"))
bak.write_bytes(raw)
assert bak.read_bytes() == raw
txt = raw.decode("utf-8")
assert "<!-- TABELA_PINOS -->" in txt and "<!-- RESULTADOS_SANDBOX -->" in txt
txt = txt.replace("<!-- TABELA_PINOS -->", tab).replace("<!-- RESULTADOS_SANDBOX -->", res)
tmp = MD.with_name(MD.name + ".tmp")
tmp.write_bytes(txt.encode("utf-8"))
assert tmp.stat().st_size > len(raw)
tmp.replace(MD)
print("inserido; md:", hashlib.sha256(MD.read_bytes()).hexdigest()[:16], MD.stat().st_size, "B; backup:", bak.name)

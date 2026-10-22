# -*- coding: utf-8 -*-
"""Vincula a Central aberta na aba «linhas de pesquisa» do site (ordem do operador, 22/10/2026: «No site, eu já havia preparado o site
para esse momento com a aba linhas de pesquisa, agora é só vincular tudo, inclusive lá no site disponibilizando o modo interativo da
central» + «o público precisa saber que está patenteado e onde e sob qual número»). Um cartão novo no topo das linhas aplicadas: o modo
interativo (central/), o um.acom da Central, os três repositórios e a tabela dos pedidos (INPI e PCT), lidos dos dockets. Backup de BYTES;
temporário; conferência; idempotente (id="central-aberta")."""
import html, json, os, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from vinculo_patentario import ler_vinculos  # noqa: E402

P = Path(r"C:\IALD\Site\tgl\v3.0\linhas-de-pesquisa.html")
info = json.loads(Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\acom\um_acom_info.json").read_text(encoding="utf-8"))
raw = P.read_bytes()
s = raw.decode("utf-8")
ANCORA = '<article class="line-card" id="dev-class_01_acom_tensor">'
assert s.count(ANCORA) == 1, s.count(ANCORA)
INICIO = "<!-- ══ A CENTRAL, ABERTA (22/10/2026, ordem do operador)"
# 22/10/2026: se o cartão já existe, é SUBSTITUÍDO (o um.acom e o vínculo mudaram depois da 1ª montagem) — não pulado
ja = s.find(INICIO)
if ja >= 0:
    fim = s.find(ANCORA, ja)
    assert fim > ja and 'id="central-aberta"' in s[ja:fim] and s.count(INICIO) == 1, "cartão existente fora do lugar esperado — PARAR"
    s = s[:ja] + s[fim:]
e = html.escape
vs = ler_vinculos()
# quem deposita e quem inventa: LIDO dos formulários do INPI e dos recibos do ePCT (vinculo_patentario.py) — ERRATA AO LADO: a 1ª
# montagem deste cartão escrevia «Applicant/Titular: IALD Ltda.»; os 16 formulários dizem pessoa física
_deps = sorted({(v["depositante"], v["tipo_de_pessoa"]) for v in vs})
_invs = sorted({v["inventor"] for v in vs if v["inventor"]})
_reqs = sorted({v["pct_requerente"] for v in vs if v["pct_requerente"]})
QUEM_EN = "Applicant (read from the INPI filing forms): %s; inventor: %s%s." % (
    "; ".join("%s (%s)" % (n, t.lower()) for n, t in _deps), "; ".join(_invs),
    ("; PCT applicant as WIPO writes it: %s" % "; ".join(_reqs)) if _reqs else "")
QUEM_PT = "Depositante (lido dos formulários de depósito no INPI): %s; inventor: %s%s." % (
    "; ".join("%s (%s)" % (n, t.lower()) for n, t in _deps), "; ".join(_invs),
    ("; requerente nos PCT, como a OMPI o escreve: %s" % "; ".join(_reqs)) if _reqs else "")
linhas = []
for v in vs:
    linhas.append("<tr><td style='font-family:var(--mono);white-space:nowrap'>%s</td><td>%s</td><td style='white-space:nowrap'>%s</td>"
                  "<td style='font-family:var(--mono);white-space:nowrap'>%s</td></tr>" % (
                      e(v["pedido_inpi"]), e((v["titulo"] or "").rstrip(".")), e(v["deposito"] or "—"), e(v["pct"] or "—")))
    for a in v["processos_adicionais"]:
        linhas.append("<tr><td style='font-family:var(--mono);white-space:nowrap'>%s</td><td><em>%s</em> (%s)</td><td style='white-space:nowrap'>%s</td>"
                      "<td>—</td></tr>" % (e(a["processo"]), e(a["papel"]), e(v["pedido_inpi"]), e(a["deposito"] or "—")))
BTN = "font-family:var(--mono);font-size:.74rem;padding:10px 18px;text-decoration:none;letter-spacing:.04em"
CARD = f'''<!-- ══ A CENTRAL, ABERTA (22/10/2026, ordem do operador) — gerada por work/central_publica_22out/vincular_central_no_site.py ══ -->
<article class="line-card" id="central-aberta" style="border-color:rgba(255,214,10,.45);background:rgba(255,214,10,.05)">
<div class="line-head"><span class="line-num"><span class="en">THE CENTRAL, OPEN · 22/10/2026</span><span class="pt" lang="pt">A CENTRAL, ABERTA · 22/10/2026</span></span><h3 class="line-title"><span class="en">Every code and every result, public — and the patent applications behind them</span><span class="pt" lang="pt">Todo o código e todo resultado, públicos — e os pedidos de patente por trás deles</span></h3></div>
<div class="line-body"><p class="en">The operator’s Central — the 16 devices, their code, their executions and seals, the Theoretical Frontier, the vault and the kernel — is open. Browse it as he does, in view-only mode; download it whole, collapsed by the ACOM device into a single <strong>um.acom</strong> (the only download the Central offers); read every file on GitHub. Personal data appear as «[dado pessoal removido]»; the operator’s operational notes (deadlines, protocol, monitor readings) stay in his Central.</p><p class="pt" lang="pt">A Central do operador — os 16 dispositivos, o código, as execuções e os selos, a Fronteira Teórica, o cofre e o kernel — está aberta. Navegue nela como ele navega, em modo de visualização; baixe-a inteira, colapsada pelo dispositivo ACOM num único <strong>um.acom</strong> (o único download que a Central oferece); leia cada arquivo no GitHub. Dados pessoais aparecem como «[dado pessoal removido]»; as notas operacionais do operador (prazos, protocolo, leituras do monitor) ficam na Central dele.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin:14px 0">
<a href="central/" style="{BTN};color:var(--void);background:var(--gold);border:none">◈ <span class="en">Open the Central (view-only) →</span><span class="pt" lang="pt">Abrir a Central (modo de visualização) →</span></a>
<a href="central/um.acom" download style="{BTN};color:var(--cyan);border:1px solid rgba(103,232,249,.4)">↓ <span class="en">Download the Central’s um.acom</span><span class="pt" lang="pt">Baixar o um.acom da Central</span></a>
<a href="https://github.com/rotolimiguel-iald/central-publica" target="_blank" rel="noopener" style="{BTN};color:var(--cyan);border:1px solid rgba(103,232,249,.4)">GitHub · central-publica</a>
<a href="https://github.com/rotolimiguel-iald/central-publica-work" target="_blank" rel="noopener" style="{BTN};color:var(--light-soft);border:1px solid rgba(255,255,255,.18)">· work</a>
<a href="https://github.com/rotolimiguel-iald/central-publica-bancada" target="_blank" rel="noopener" style="{BTN};color:var(--light-soft);border:1px solid rgba(255,255,255,.18)">· bancada</a>
</div>
<p style="font-size:.82rem;color:var(--light-soft)"><span class="en">um.acom: {info["n_arquivos"]} files, sha256 <code>{info["sha256"][:16]}…</code>; universal public key <code>{e(info["chave_publica"])}</code> — open it at the IALD public decompressor.</span><span class="pt" lang="pt">um.acom: {info["n_arquivos"]} arquivos, sha256 <code>{info["sha256"][:16]}…</code>; chave universal pública <code>{e(info["chave_publica"])}</code> — abra no descompactador público da IALD.</span></p>
<h4 style="margin:18px 0 8px"><span class="en">The patent applications (INPI, Brazil · PCT, WIPO)</span><span class="pt" lang="pt">Os pedidos de patente (INPI, Brasil · PCT, OMPI)</span></h4>
<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse;font-size:.8rem;line-height:1.45">
<thead><tr><th style="text-align:left"><span class="en">INPI application</span><span class="pt" lang="pt">pedido no INPI</span></th><th style="text-align:left"><span class="en">title</span><span class="pt" lang="pt">título</span></th><th style="text-align:left"><span class="en">filed</span><span class="pt" lang="pt">depósito</span></th><th style="text-align:left">PCT</th></tr></thead>
<tbody>{"".join(linhas)}</tbody></table></div>
<p style="font-size:.8rem;color:var(--light-soft);margin-top:8px"><span class="en">Patent applications filed — not granted patents. {e(QUEM_EN)}</span><span class="pt" lang="pt">Pedidos de patente depositados — não patentes concedidas. {e(QUEM_PT)}</span></p>
</div>
<div class="line-state"><span class="tag tag-real">[REAL]</span> <span class="en">read from the Central itself (dockets, seals, executions); view-only, nothing can be changed</span><span class="pt" lang="pt">lido da própria Central (dockets, selos, execuções); só visualização, nada se altera</span></div>
</article>
'''
s2 = s.replace(ANCORA, CARD + ANCORA, 1)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp_central")
t.write_bytes(s2.encode("utf-8"))
assert t.stat().st_size > len(raw) - 20000 and 'id="central-aberta"' in s2 and s2.count(INICIO) == 1
os.replace(t, P)
print("linhas-de-pesquisa.html:", len(raw), "->", P.stat().st_size, "| pedidos na tabela:", len(linhas))

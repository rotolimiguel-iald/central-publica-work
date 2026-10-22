# -*- coding: utf-8 -*-
"""PatentPage.tsx no MODO PÚBLICO DE VISUALIZAÇÃO (22/10/2026; pedido do operador: «o público precisa saber que está patenteado e onde e
sob qual número»): uma caixa «Vínculo patentário» no topo (pedido no INPI, depósito, prioridade, PCT na OMPI, processos adicionais,
«pedido depositado — não patente concedida»); somem as linhas que o retrato não traz (petição, pasta original, situação do ePCT), a
memória técnica (a leitura da patente) e o atalho «Compilar instruções». No build normal nada muda. Backup de BYTES; idempotente."""
import os, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\frontend\src\pages\PatentPage.tsx")
raw = P.read_bytes()
s = raw.decode("utf-8")
if "VinculoPatentario" in s:
    print("já aplicado"); raise SystemExit
crlf = b"\r\n" in raw
CAIXA = r'''

// MODO PÚBLICO DE VISUALIZAÇÃO — o vínculo patentário de cada dispositivo: onde está o pedido e sob qual número
function VinculoPatentario({ v }: { v: any }) {
  if (!v) return null
  const linha = (k: string, val: any) => val ? <><div className="k">{k}</div><div>{val}</div></> : null
  return (
    <div className="panel" style={{ border: '1px solid #c5961a66', background: '#151206', marginBottom: 12 }}>
      <div style={{ fontWeight: 800, color: '#ffd60a', marginBottom: 6 }}>Vínculo patentário</div>
      <p style={{ fontSize: 13, margin: '0 0 8px' }}>Este dispositivo é objeto de <b>pedido de patente depositado</b> (não é patente concedida).</p>
      <div className="kv">
        {linha('Pedido no INPI (Brasil)', <b style={{ fontFamily: 'monospace' }}>{v.pedido_inpi}</b>)}
        {linha('Escritório', v.escritorio)}
        {linha('Depósito', v.deposito)}
        {linha('Prioridade', v.prioridade)}
        {linha('PCT (OMPI)', v.pct ? <span style={{ fontFamily: 'monospace' }}>{v.pct}{v.pct_data ? ` · ${v.pct_data}` : ''}</span> : null)}
        {(v.processos_adicionais || []).map((a: any) => (
          <React.Fragment key={a.processo}>{linha('Processo adicional', <span><span style={{ fontFamily: 'monospace' }}>{a.processo}</span> — {a.papel}{a.deposito ? ` · ${a.deposito}` : ''}</span>)}</React.Fragment>
        ))}
        {linha('Titular', v.titular)}
      </div>
    </div>
  )
}
'''
pares = [
    ("import { api, pub, type PatentDetail", "import { api, pub, PUBLICA, type PatentDetail"),
    ("      <div className=\"tabs\">\n        {tabs.map(t => (\n",
     "      {PUBLICA && <VinculoPatentario v={(p as any).vinculo_patentario} />}\n      <div className=\"tabs\">\n        {tabs.map(t => (\n"),
    ("        <div className=\"tab\" style={{ marginLeft: 'auto', color: 'var(--gold)' }}\n          onClick={() => nav('/compiler')}>⇢ Compilar instruções</div>\n",
     "        {!PUBLICA && <div className=\"tab\" style={{ marginLeft: 'auto', color: 'var(--gold)' }}\n          onClick={() => nav('/compiler')}>⇢ Compilar instruções</div>}\n"),
    ("            <div className=\"k\">Petição</div><div>{p.peticao}</div>\n",
     "            {!PUBLICA && <><div className=\"k\">Petição</div><div>{p.peticao}</div></>}\n"),
    ("            <div className=\"k\">Situação ePCT</div><div><EpctPill status={p.epct_status} /> {p.epct_number || ''}</div>\n",
     "            {PUBLICA ? <><div className=\"k\">PCT (OMPI)</div><div>{p.epct_number || '—'}</div></>\n"
     "                     : <><div className=\"k\">Situação ePCT</div><div><EpctPill status={p.epct_status} /> {p.epct_number || ''}</div></>}\n"),
    ("            <div className=\"k\">Pasta original</div><div className=\"muted\">{p.pasta_original}</div>\n",
     "            {!PUBLICA && <><div className=\"k\">Pasta original</div><div className=\"muted\">{p.pasta_original}</div></>}\n"),
    ("          <details style={{ marginTop: 16 }}>\n            <summary style={{ cursor: 'pointer', color: 'var(--accent)' }}>Memória técnica completa</summary>\n            <pre className=\"md\">{memory}</pre>\n          </details>\n",
     "          {!PUBLICA && <details style={{ marginTop: 16 }}>\n            <summary style={{ cursor: 'pointer', color: 'var(--accent)' }}>Memória técnica completa</summary>\n            <pre className=\"md\">{memory}</pre>\n          </details>}\n"),
]
for a, b in pares:
    if crlf:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    c = s.count(a)
    assert c == 1, (c, a[:80])
    s = s.replace(a, b)
s = s.rstrip() + (CAIXA.replace("\n", "\r\n") if crlf else CAIXA)
if "import React" not in s and "React.Fragment" in s:
    s = ("import React from 'react'\r\n" if crlf else "import React from 'react'\n") + s
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp_publico")
t.write_bytes(s.encode("utf-8"))
os.replace(t, P)
print("ok PatentPage.tsx", len(raw), "->", P.stat().st_size)

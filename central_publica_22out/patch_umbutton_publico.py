# -*- coding: utf-8 -*-
"""O botão UM no MODO PÚBLICO DE VISUALIZAÇÃO (22/10/2026): sem senha; baixa o um.acom da Central já colapsado pelo dispositivo ACOM e
selado com a chave universal pública; mostra a chave, o tamanho e o sha256 (um_acom_info.json) e o descompactador público da IALD.
No build normal (a Central do operador) o botão fica igual. Backup de BYTES; troca conferida; idempotente."""
import os, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\frontend\src\UmButton.tsx")
raw = P.read_bytes()
s = raw.decode("utf-8")
if "MODO PÚBLICO DE VISUALIZAÇÃO" in s:
    print("já aplicado"); raise SystemExit
crlf = b"\r\n" in raw
COMP = r'''// ── MODO PÚBLICO DE VISUALIZAÇÃO (22/10/2026, ordem do operador: «a possibilidade, inclusive, de modo público, de colapsarem a
// central inteira em um.acom e baixarem na sua própria máquina, esse é o único acesso público de baixar direto na central»).
// Sem senha: o um.acom já vem colapsado pelo dispositivo ACOM (sem perdas, SHA-256 bit a bit) e selado com a chave universal
// pública, a mesma declarada no site para a oncologia.
const BASE_PUB_UM: string = ((import.meta as any).env || {}).BASE_URL || '/'
function UmPublico() {
  const [open, setOpen] = useState(false)
  const [info, setInfo] = useState<any>(null)
  useEffect(() => {
    if (open && !info) fetch(BASE_PUB_UM + 'um_acom_info.json').then(r => r.json()).then(setInfo).catch(() => setInfo({}))
  }, [open])
  const mono: React.CSSProperties = { fontFamily: 'ui-monospace, Consolas, monospace', fontSize: 12, wordBreak: 'break-all' }
  return (
    <>
      <button onClick={() => setOpen(true)} title="Colapsar a Central inteira num único arquivo: o um.acom"
        style={{ marginTop: 8, width: '100%', fontSize: 13, fontWeight: 700, letterSpacing: 1, padding: '9px 0', borderRadius: 8,
                 cursor: 'pointer', color: '#0b0f16', background: 'linear-gradient(135deg,#ffd60a,#c5961a)', border: '1px solid #ffd60a88',
                 boxShadow: '0 2px 12px rgba(197,150,26,0.35)' }}>
        ✦ Um
      </button>
      {open && createPortal(
        <div onClick={() => setOpen(false)} style={{ position: 'fixed', inset: 0, zIndex: 9999, background: 'rgba(0,0,0,0.65)',
             display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 16 }}>
          <div onClick={e => e.stopPropagation()} style={{ width: 'min(520px, 96vw)', background: '#0e1420', border: '1px solid #232b38',
               borderRadius: 14, padding: 22, boxShadow: '0 20px 80px rgba(0,0,0,0.5)' }}>
            <div style={{ fontSize: 17, fontWeight: 800, color: '#ffd60a' }}>✦ O Um — a Central inteira num arquivo</div>
            <p style={{ fontSize: 13, lineHeight: 1.6, color: '#cfd6e4' }}>
              O botão Um colapsa a Central inteira — o núcleo canônico da TGL, a fronteira teórica e as 16 patentes, cada uma com o seu
              código FINAL e os seus comprovantes — num único arquivo, comprimido pelo dispositivo ACOM (sem perdas, conferido por SHA-256
              bit a bit) e selado com a criptografia da casa. É o único download desta Central pública.
            </p>
            <p style={{ fontSize: 13, color: '#cfd6e4' }}>Chave universal pública: <b style={{ ...mono, color: '#67e8f9' }}>{info?.chave_publica || '…'}</b></p>
            {info?.sha256 && <p style={{ fontSize: 12, color: '#9aa4b2' }}>{info.n_arquivos} arquivos na árvore · {Math.round((info.bytes || 0) / 1024)} KB ·
              sha256 <span style={mono}>{info.sha256}</span> · gerado em {info.gerado_em}</p>}
            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', marginTop: 12 }}>
              <a href={BASE_PUB_UM + 'um.acom'} download="um.acom" style={{ padding: '9px 14px', borderRadius: 8, background: '#ffd60a',
                 color: '#0b0f16', fontWeight: 700, textDecoration: 'none', fontSize: 13 }}>↓ Baixar o um.acom</a>
              <a href="https://iald.ia.br/#acom" target="_blank" rel="noopener" style={{ padding: '9px 14px', borderRadius: 8,
                 border: '1px solid rgba(103,232,249,.4)', color: '#67e8f9', textDecoration: 'none', fontSize: 13 }}>Abrir no descompactador público da IALD →</a>
              <button onClick={() => setOpen(false)} style={{ padding: '9px 14px', borderRadius: 8, background: 'transparent', color: '#9aa4b2',
                 border: '1px solid #232b38', fontSize: 13, cursor: 'pointer' }}>fechar</button>
            </div>
          </div>
        </div>, document.body)}
    </>
  )
}

export default function UmButton() {
  if (PUBLICA) return <UmPublico />   // MODO PÚBLICO DE VISUALIZAÇÃO (constante de build: a ordem dos hooks não muda)
'''
pares = [("import { useState } from 'react'\n", "import { useEffect, useState } from 'react'\n"),
         ("import { api } from './api'\n", "import { api, PUBLICA } from './api'\n"),
         ("export default function UmButton() {\n", COMP)]
for a, b in pares:
    if crlf:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    assert s.count(a) == 1, (s.count(a), a[:60])
    s = s.replace(a, b)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp_publico")
t.write_bytes(s.encode("utf-8"))
os.replace(t, P)
print("ok UmButton.tsx", len(raw), "->", P.stat().st_size)

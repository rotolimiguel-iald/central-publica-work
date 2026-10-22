# -*- coding: utf-8 -*-
"""App.tsx no MODO PÚBLICO DE VISUALIZAÇÃO (22/10/2026): o menu esconde as páginas operacionais do operador (Prazos/Docket, Prompt
Compiler, Pendências, Custódia/Backup, ePCT — o critério do operador: «não precisa se tornar público as notas de aviso pra mim»); o sino
do monitor, a faixa da Sentinela e o sino do backup não leem nada; uma faixa no topo diz o que é o modo público. No build normal nada
muda. Backup de BYTES; trocas conferidas; idempotente."""
import os, time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\frontend\src\App.tsx")
raw = P.read_bytes()
s = raw.decode("utf-8")
if "MODO PÚBLICO DE VISUALIZAÇÃO" in s:
    print("já aplicado"); raise SystemExit
crlf = b"\r\n" in raw
BANNER = r'''

// MODO PÚBLICO DE VISUALIZAÇÃO — a faixa que diz o que é esta Central (só no build público)
function BannerPublico() {
  return (
    <div style={{ background: 'linear-gradient(90deg,#1a1405,#0e1420)', border: '1px solid #c5961a55', borderRadius: 10, padding: '10px 14px',
                  margin: '0 0 14px', fontSize: 13, lineHeight: 1.55, color: '#e6dcc0' }}>
      <b style={{ color: '#ffd60a' }}>Modo público de visualização.</b> O retrato da Central do operador — a ciência, o código, os resultados
      e o vínculo às patentes (pedidos depositados no INPI e no PCT, com os números). Aqui se lê; nada se altera. O único download é o
      <b> um.acom</b> (o botão <b>✦ Um</b>): a Central inteira colapsada pelo dispositivo ACOM. Código-fonte e resultados:{' '}
      <a href="https://github.com/rotolimiguel-iald/central-publica" target="_blank" rel="noopener" style={{ color: '#67e8f9' }}>github.com/rotolimiguel-iald/central-publica</a>
      {' '}· a teoria: <a href="https://github.com/rotolimiguel-iald/the_boundary" target="_blank" rel="noopener" style={{ color: '#67e8f9' }}>the_boundary</a>.
      Dados pessoais aparecem como «[dado pessoal removido]»; as notas operacionais do operador (prazos, protocolo, leituras do monitor) ficam na Central dele.
    </div>
  )
}
'''
pares = [
    ("import { api, type Health } from './api'\n", "import { api, PUBLICA, type Health } from './api'\n"),
    ("  { to: '/iald-nativa', ico: '🧠', label: 'IALD Nativa' },\n]\n",
     "  { to: '/iald-nativa', ico: '🧠', label: 'IALD Nativa' },\n]\n"
     "// MODO PÚBLICO DE VISUALIZAÇÃO: as páginas operacionais do operador não aparecem no menu público\n"
     "const OPERACIONAIS = ['/docket', '/compiler', '/pendencias', '/custodia', '/epct']\n"
     "const NAV_VISIVEL = PUBLICA ? NAV.filter(n => !OPERACIONAIS.includes(n.to)) : NAV\n"),
    ("          {NAV.map(n => (\n", "          {NAV_VISIVEL.map(n => (\n"),
    ("  useEffect(() => {\n    let alive = true\n    const tick = () => api.andamentos().then(m => {\n",
     "  useEffect(() => {\n    if (PUBLICA) return   // MODO PÚBLICO: o monitor e a Sentinela não fazem parte do retrato\n"
     "    let alive = true\n    const tick = () => api.andamentos().then(m => {\n"),
    ("  useEffect(() => {\n    let alive = true\n    const tick = () => api.backupStatus().then(s => {\n",
     "  useEffect(() => {\n    if (PUBLICA) return   // MODO PÚBLICO: o backup não faz parte do retrato\n"
     "    let alive = true\n    const tick = () => api.backupStatus().then(s => {\n"),
    ("      <main className=\"main\"><Outlet /></main>\n", "      <main className=\"main\">{PUBLICA && <BannerPublico />}<Outlet /></main>\n"),
]
for a, b in pares:
    if crlf:
        a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
    c = s.count(a)
    assert c == 1, (c, a[:70])
    s = s.replace(a, b)
s = s.rstrip() + (BANNER.replace("\n", "\r\n") if crlf else BANNER)
P.with_name(P.name + ".bak_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(raw)
t = P.with_name(P.name + ".tmp_publico")
t.write_bytes(s.encode("utf-8"))
os.replace(t, P)
print("ok App.tsx", len(raw), "->", P.stat().st_size)

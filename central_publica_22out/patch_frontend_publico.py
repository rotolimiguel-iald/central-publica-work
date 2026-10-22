# -*- coding: utf-8 -*-
"""O MODO PÚBLICO DE VISUALIZAÇÃO no frontend da Central (22/10/2026, ordem do operador). Aditivo e ligado SÓ pela chave de build
VITE_CENTRAL_PUBLICA=1: no build normal (a Central do operador) nada muda de comportamento. Backup de BYTES de cada arquivo tocado;
trocas conferidas por contagem; respeita CRLF/LF do arquivo. Idempotente (marca «MODO PÚBLICO DE VISUALIZAÇÃO»)."""
import os, time
from pathlib import Path

SRC = Path(r"C:\IALD\Central de Patentes\frontend\src")
TS = time.strftime("%Y%m%d_%H%M%S")
MARCA = "MODO PÚBLICO DE VISUALIZAÇÃO"


def patch(rel, pares):
    p = SRC / rel
    raw = p.read_bytes()
    s = raw.decode("utf-8")
    if MARCA in s:
        print("já aplicado:", rel); return
    crlf = b"\r\n" in raw
    for a, b in pares:
        if crlf:
            a, b = a.replace("\n", "\r\n"), b.replace("\n", "\r\n")
        c = s.count(a)
        assert c == 1, (rel, c, a[:80])
        s = s.replace(a, b)
    p.with_name(p.name + ".bak_" + TS).write_bytes(raw)
    t = p.with_name(p.name + ".tmp_publico")
    t.write_bytes(s.encode("utf-8"))
    assert t.stat().st_size > len(raw)
    os.replace(t, p)
    print("ok", rel, len(raw), "->", p.stat().st_size)


BLOCO_API = '''// ── MODO PÚBLICO DE VISUALIZAÇÃO (22/10/2026, ordem do operador: «possam interagir com a central (somente em modo de
// visualização), igual eu interajo»). Build com VITE_CENTRAL_PUBLICA=1: cada leitura /api/... vira o arquivo estático do retrato
// público, achado pelo mapa api/_mapa.json (gerado por script a partir da Central do operador, só por GET, com os dados pessoais
// trocados por «[dado pessoal removido]»); toda ação (POST/DELETE) é recusada. Sem servidor: ninguém altera nada. No build normal
// (a Central do operador) nada disto roda.
const ENV_PUB: any = (import.meta as any).env || {}
export const PUBLICA: boolean = ENV_PUB.VITE_CENTRAL_PUBLICA === '1'
export const AVISO_PUBLICO = 'Modo público de visualização: esta ação existe só na Central do operador. Aqui se lê; o único download é o um.acom.'
const BASE_PUB: string = ENV_PUB.BASE_URL || '/'
let MAPA: Record<string, string> = {}
export async function carregarMapa(): Promise<void> {
  if (!PUBLICA) return
  try {
    const r = await fetch(BASE_PUB + 'api/_mapa.json', { cache: 'no-cache' })
    if (r.ok) MAPA = await r.json()
  } catch { /* sem mapa: as leituras falham à vista */ }
}
/** A URL que o navegador abre: na Central do operador é a própria; no modo público, o arquivo do retrato (ou a nota de que a leitura
 *  não faz parte dele). */
export function pub(url: string): string {
  if (!PUBLICA) return url
  const m = MAPA[url]
  return m ? BASE_PUB + m : BASE_PUB + 'fora_do_retrato.html'
}
function respostaPublicaFixa(url: string): any {
  if (url.startsWith('/api/auth/status')) return { enabled: false, authenticated: true, scheme: 'publico-visualizacao', beta: null }
  if (url.startsWith('/api/auth/me')) return { authenticated: true, role: 'visitante', name: 'Visitante (modo público)' }
  if (url.startsWith('/api/users')) return { enabled: false, users: [], roles: [] }
  return undefined
}
/** No modo público, o fetch de qualquer página passa por aqui: leitura de /api vai ao retrato; ação em /api é recusada. */
export function instalarFetchPublico(): void {
  if (!PUBLICA) return
  const orig = window.fetch.bind(window)
  window.fetch = (input: RequestInfo | URL, init?: RequestInit) => {
    const u = typeof input === 'string' ? input : (input instanceof URL ? input.pathname + input.search : input.url)
    if (u.startsWith('/api/')) {
      const met = ((init && init.method) || (typeof input !== 'string' && !(input instanceof URL) ? input.method : 'GET') || 'GET').toUpperCase()
      if (met !== 'GET') return Promise.resolve(new Response(JSON.stringify({ detail: AVISO_PUBLICO }), { status: 403, headers: { 'Content-Type': 'application/json' } }))
      const fixo = respostaPublicaFixa(u)
      if (fixo !== undefined) return Promise.resolve(new Response(JSON.stringify(fixo), { status: 200, headers: { 'Content-Type': 'application/json' } }))
      return orig(pub(u))
    }
    return orig(input as any, init)
  }
}
'''
patch("api.ts", [
    ("async function j<T>(url: string, opts?: RequestInit): Promise<T> {\n  const r = await fetch(url, opts)\n",
     BLOCO_API + "\nasync function j<T>(url: string, opts?: RequestInit): Promise<T> {\n  const r = await fetch(url, opts)\n"),
    ("async function jApp<T>(url: string, opts: { method?: string; body?: string; json?: boolean } = {}):\n  Promise<{ body: T; serverMs: number | null }> {\n",
     "async function jApp<T>(url: string, opts: { method?: string; body?: string; json?: boolean } = {}):\n  Promise<{ body: T; serverMs: number | null }> {\n"
     "  if (PUBLICA) throw new ApiError(403, AVISO_PUBLICO, url)   // o app IALD (dados de terceiros) não entra no modo público\n"),
    ("  umBuild: async (secret: string): Promise<Blob> => {\n",
     "  umBuild: async (secret: string): Promise<Blob> => {\n"
     "    if (PUBLICA) {   // modo público: o um.acom da Central já colapsado pelo dispositivo ACOM, com a chave universal pública\n"
     "      const r0 = await fetch(BASE_PUB + 'um.acom')\n"
     "      if (!r0.ok) throw new Error(`erro ${r0.status} ao baixar o um.acom`)\n"
     "      return r0.blob()\n"
     "    }\n"),
    ("  umBuildOncologia: async (): Promise<Blob> => {\n",
     "  umBuildOncologia: async (): Promise<Blob> => {\n"
     "    if (PUBLICA) {   // modo público: o um.acom da oncologia que o site já publica\n"
     "      const r0 = await fetch(BASE_PUB + '../um.acom')\n"
     "      if (!r0.ok) throw new Error(`erro ${r0.status} ao baixar o um.acom da oncologia`)\n"
     "      return r0.blob()\n"
     "    }\n"),
])
patch("main.tsx", [
    ("ReactDOM.createRoot(document.getElementById('root')!).render(\n  <React.StrictMode>\n    <Gate>\n      <RouterProvider router={router} />\n    </Gate>\n  </React.StrictMode>,\n)",
     "// MODO PÚBLICO DE VISUALIZAÇÃO: o fetch passa pelo retrato e o mapa carrega antes de montar (no build normal, nada muda)\n"
     "instalarFetchPublico()\n"
     "carregarMapa().finally(() => ReactDOM.createRoot(document.getElementById('root')!).render(\n  <React.StrictMode>\n    <Gate>\n      <RouterProvider router={router} />\n    </Gate>\n  </React.StrictMode>,\n))"),
    ("import App from './App'\n", "import App from './App'\nimport { carregarMapa, instalarFetchPublico } from './api'\n"),
])
patch("pages/PatentPage.tsx", [
    ("import { api, type PatentDetail, type EvidenceClaim, type EvidenceElo, type EvolucaoDoc } from '../api'",
     "import { api, pub, type PatentDetail, type EvidenceClaim, type EvidenceElo, type EvolucaoDoc } from '../api'   // pub: MODO PÚBLICO DE VISUALIZAÇÃO"),
    ("<td><a href={`/api/documents/${d.id}/text`} target=\"_blank\">texto</a> · <a href={`/api/documents/${d.id}/file`} target=\"_blank\">PDF</a></td>",
     "<td><a href={pub(`/api/documents/${d.id}/text`)} target=\"_blank\">texto</a> · <a href={pub(`/api/documents/${d.id}/file`)} target=\"_blank\">PDF</a></td>"),
    ("<DeepZoom url={`/api/renders/${p.renders[0].id}`} height={460} />", "<DeepZoom url={pub(`/api/renders/${p.renders[0].id}`)} height={460} />"),
    ("  if (e.doc_id != null) return `/api/documents/${e.doc_id}/file`\n  if (e.code_path) return `/api/patents/${encodeURIComponent(pid)}/code/file?path=${encodeURIComponent(e.code_path)}`",
     "  if (e.doc_id != null) return pub(`/api/documents/${e.doc_id}/file`)\n  if (e.code_path) return pub(`/api/patents/${encodeURIComponent(pid)}/code/file?path=${encodeURIComponent(e.code_path)}`)"),
    ("href={`/api/patents/${encodeURIComponent(pid)}/code/file?path=${encodeURIComponent(final.path)}`}",
     "href={pub(`/api/patents/${encodeURIComponent(pid)}/code/file?path=${encodeURIComponent(final.path)}`)}"),
    ("<img key={r.id} src={`/api/renders/${r.id}`} alt={r.title}", "<img key={r.id} src={pub(`/api/renders/${r.id}`)} alt={r.title}"),
    ("<DeepZoom url={`/api/renders/${cur.id}`} height={560} />", "<DeepZoom url={pub(`/api/renders/${cur.id}`)} height={560} />"),
])
patch("pages/Compiler.tsx", [
    ("import { api } from '../api'", "import { api, pub } from '../api'   // pub: MODO PÚBLICO DE VISUALIZAÇÃO"),
    ("<td><a href={`/api/compiled/${f.filename}`} target=\"_blank\">{f.filename}</a></td>",
     "<td><a href={pub(`/api/compiled/${f.filename}`)} target=\"_blank\">{f.filename}</a></td>"),
])
pf = [("import { api } from '../api'", "import { api, pub } from '../api'   // pub: MODO PÚBLICO DE VISUALIZAÇÃO")]
for nome in ("escada_qg", "banda_beta", "piso_vazios", "cadeia_inscricao"):
    pf.append(('href="/api/fronteira/fig/%s"' % nome, "href={pub('/api/fronteira/fig/%s')}" % nome))
patch("pages/Fronteira.tsx", pf)

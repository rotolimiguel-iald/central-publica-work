# -*- coding: utf-8 -*-
"""mcp_um.py -- a Bancada Um como FERRAMENTAS para as IAs (servidor MCP, stdio). Nenhuma IA precisa escrever código para consultar os dados:
ela chama estas ferramentas, e a Bancada (http://127.0.0.1:18777, que precisa estar no ar) faz a conta na GPU com os dados residentes.

Cada chamada leva o nome do cliente (variável BANCADA_UM_CLIENTE, ex.: «claude», «codex», «kimi»); as buscas de evidência (ajustar,
comparar, amostrar) entram no LIVRO de tentativas e voltam com diagnósticos locais e correção Šidák exploratória; não há significância global calibrada.

Registro (exemplo, Claude Code):  claude mcp add bancada-um -- C:\\Python314\\python.exe C:\\IALD\\Bancada_Um\\mcp_um.py
"""
import json
import os
import time
import urllib.error
import urllib.request

from mcp.server.fastmcp import FastMCP

URL = os.environ.get("BANCADA_UM_URL", "http://127.0.0.1:18777")
CLIENTE = "mcp:" + os.environ.get("BANCADA_UM_CLIENTE", "ia")
mcp = FastMCP("bancada-um")


def _req(caminho, corpo=None, timeout=600):
    dados = None if corpo is None else json.dumps(corpo).encode("utf-8")
    r = urllib.request.Request(URL + caminho, data=dados, headers={"Content-Type": "application/json", "X-Cliente": CLIENTE})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as f:
            return json.loads(f.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return dict(erro=e.read().decode("utf-8", "replace")[:2000], codigo=e.code)
    except Exception as e:
        return dict(erro="Bancada Um fora do ar ou inacessível em %s: %r" % (URL, e))


@mcp.tool()
def estado() -> dict:
    """Estado da Bancada Um: GPU/VRAM, RAM, motor, β_TGL = α√e, validações, lago residente e livro de tentativas."""
    e = _req("/api/estado")
    if "motor" in e:
        e["motor"].pop("fontes", None)
    return e


@mcp.tool()
def listar_dados() -> dict:
    """Os conjuntos cosmológicos do motor (Planck comprimido, DESI DR1/DR2, SH0ES, Pantheon+) com proveniência, e o lago residente (arquivos na RAM)."""
    d = _req("/api/dados")
    l = _req("/api/lago")
    res = l.get("residente", {})
    arquivos = [dict(caminho=a["caminho"], estado=a["estado"], gib=round(a["bytes"] / 2 ** 30, 3), sha256=a.get("sha256"),
                     tabelas=a.get("tabelas")) for a in res.get("arquivos", []) if a["estado"] in ("residente", "apelido")]
    return dict(cosmologia=d, lago=dict(estado=res.get("estado"), arquivos=sorted(arquivos, key=lambda a: -a["gib"])[:80]))


OPCOES_DOC = (" opcoes (dict, opcional): {'modo': 'tgl' (padrão canônico, decisão 30/09: corrigido + mapa de R efetivo (1+β)Ω_m, ratificado pelo operador) | 'selado' (histórico explícito: reproduz a V3 do D1) | 'corrigido' (covariância do Planck de Chen+2019, DR1 com as "
              "correlações DM–DH, D_M(z*) por razão sobre o CAMB), 'mapa_R': 'nu' (controle histórico) | 'eff' ((1+β)Ω_m em R — escolha [INPUT] não derivada que "
              "decide a sensibilidade a β; auditoria de 28/09)}; chaves individuais planck_cov/dr1_cov/dm_star também aceitas. Fase 7 (01/10): 'cc_cov': 'diagonal' | 'moresco2020' (covariância completa de Moresco+2020 nos cronômetros) | 'moresco2020_todos'. Fase 4 (30/09): 'modo': 'artigo' (fundo ΛCDM, β só na lei, núcleo d1b: a convenção do artigo 1); 'lei': 'd1a' | 'd1b'; 'beta_no_fundo': 'sim' | 'nao'; SH0ES (01/10): 'lei_sn': 'nenhuma' | 'sombra' | 'acumulada'; 'lei_cc': 'acumulada' | 'nenhuma'.")


@mcp.tool(description="Avalia UM ponto do modelo V3 da TGL (β = 0 é ΛCDM) contra os conjuntos: χ² por conjunto, predições e derivados. É diagnóstico "
                      "(não entra no livro). conjuntos ⊆ {planck_comp, desi_dr1, desi_dr2, sh0es, pantheon, sh0es_local (SH0ES como H0_local = H0·K(β), lei d1a ou d1b), cc_moresco (32 cronômetros H(z) de Moresco+2022, lei acumulada), pantheon_sh0es (Pantheon+SH0ES: 1580 + 77 calibradores Cefeida, M profilado)}." + OPCOES_DOC)
def avaliar(H0: float = 67.95, ombh2: float = 0.022362, omch2: float = 0.119, beta: float = 0.0, c: float = 0.0,
            conjuntos: list[str] = ["planck_comp", "desi_dr1"], opcoes: dict = {}) -> dict:
    """Avaliação diagnóstica de um ponto (ver a descrição da ferramenta)."""
    r = _req("/api/avaliar", dict(theta=dict(H0=H0, ombh2=ombh2, omch2=omch2, beta=beta, c=c), conjuntos=conjuntos, curvas=False, opcoes=opcoes or {}))
    return r


@mcp.tool(description="Melhor ajuste (mínimos quadrados, σ por JᵀJ). beta ∈ {'livre', 'tgl' (= α√e), 'zero'} ou um número. ENTRA NO LIVRO; traz a "
                      "significância corrigida." + OPCOES_DOC)
def ajustar(conjuntos: list[str] = ["planck_comp", "desi_dr1"], beta: str = "livre", c_livre: bool = False, opcoes: dict = {}) -> dict:
    """Ajuste de máxima verossimilhança (ver a descrição da ferramenta)."""
    return _req("/api/ajustar", dict(conjuntos=conjuntos, beta=beta, c_livre=c_livre, opcoes=opcoes or {}))


@mcp.tool(description="Ajusta ΛCDM (β = 0), TGL (β = α√e) e β livre e devolve os Δχ² (Wilks, 1 g.l.). ENTRA NO LIVRO; traz a significância corrigida."
                      + OPCOES_DOC)
def comparar(conjuntos: list[str] = ["planck_comp", "desi_dr1"], c_livre: bool = False, opcoes: dict = {}) -> dict:
    """Comparação de modelos por Δχ² (ver a descrição da ferramenta)."""
    return _req("/api/comparar", dict(conjuntos=conjuntos, c_livre=c_livre, opcoes=opcoes or {}))


@mcp.tool(description="Posterior de (H0, ω_b, ω_c, β[, c]) por ensemble afim-invariante na GPU; espera terminar e devolve o resumo (medianas, 16–84%, "
                      "τ, aceitação, fração do posterior além de α√e). ENTRA NO LIVRO; traz a significância corrigida." + OPCOES_DOC)
def amostrar_posterior(conjuntos: list[str] = ["planck_comp", "desi_dr1"], walkers: int = 256, passos: int = 2000, queima: int = 500,
                       semente: int = 42, c_livre: bool = False, opcoes: dict = {}) -> dict:
    """Amostragem do posterior (ver a descrição da ferramenta)."""
    t = _req("/api/amostrar", dict(conjuntos=conjuntos, walkers=walkers, passos=passos, queima=queima, semente=semente, c_livre=c_livre, opcoes=opcoes or {}))
    if "tarefa" not in t:
        return t
    t0 = time.time()
    while time.time() - t0 < 3600:
        s = _req("/api/tarefas/" + t["tarefa"])
        if s.get("estado") in ("pronta", "falhou"):
            if s.get("resultado"):
                r = dict(s["resultado"]); r.pop("hist_beta_H0", None)
                return r
            return s
        time.sleep(1.0)
    return dict(erro="tempo esgotado", tarefa=t["tarefa"])


@mcp.tool()
def lago_colunas(caminho: str, hdu: int = 1) -> dict:
    """As colunas (nome, tipo) de uma tabela residente do lago (caminho exato de listar_dados) — sem copiar dados."""
    from urllib.parse import quote
    return _req("/api/lago/colunas?caminho=%s&hdu=%d" % (quote(caminho), hdu))


@mcp.tool()
def lago_histograma(caminho: str, coluna: str, hdu: int = 1, bins: int = 120, log: bool = False) -> dict:
    """Histograma de uma coluna INTEIRA do lago residente, calculado na GPU (ex.: Z_B dos 21 milhões de galáxias do KiDS)."""
    return _req("/api/lago/histograma", dict(caminho=caminho, hdu=hdu, coluna=coluna, bins=bins, log=log))


@mcp.tool()
def lago_mapa(caminho: str, x: str, y: str, hdu: int = 1, nx: int = 180, ny: int = 90) -> dict:
    """Densidade 2D de duas colunas inteiras (ex.: RA × DEC), na GPU; devolve a matriz de contagens nx × ny."""
    return _req("/api/lago/mapa", dict(caminho=caminho, hdu=hdu, x=x, y=y, bins=[nx, ny]))


# ---- o banco RESIDENTE de ondas gravitacionais (Fase 6, 01/10/2026): as séries de 32 s (cache de maio O1–O3 + O4 do GWOSC), branqueadas, os remanescentes e os
# estágios da rodada do eco V3 («a transformada radical»); o empilhamento de consulta é a MESMA função do executor. O veredito selado é o do RESULTADO por hash. ----
@mcp.tool()
def gw_estado() -> dict:
    """O banco residente de ondas gravitacionais da Bancada Um: eventos por era, séries na RAM (sha256), NaN, remanescentes, arquivos dos estágios (pré-registro, poder, cego, aberto, RESULTADO) com sha16."""
    return _req("/api/gw").get("residente", {})


@mcp.tool(description="Lista os eventos BBH do banco residente (nome, era, catálogo, SNR, massas, z, M_f e a_f do remanescente, atrasos MAY/KMS em ms, detectores, qualidade por série) e, se a rodada já "
                      "existir, o eco por detector e por lei (â com viés subtraído, σ, recuperações). Filtros opcionais: era ('O1O2'|'O3'|'O4'), src ('maio'|'o4'), snr_min, snr_max, Mf_min, Mf_max.")
def gw_eventos(era: str = "", src: str = "", snr_min: float = 0.0, snr_max: float = 0.0, Mf_min: float = 0.0, Mf_max: float = 0.0) -> dict:
    """Tabela de eventos do banco residente (ver a descrição)."""
    from urllib.parse import urlencode
    q = {k: v for k, v in dict(era=era, src=src, snr_min=snr_min or "", snr_max=snr_max or "", Mf_min=Mf_min or "", Mf_max=Mf_max or "").items() if v != ""}
    return _req("/api/gw/eventos?" + urlencode(q))


@mcp.tool(description="Um trecho de uma série residente (key = EVENTO_DETECTOR, ex.: GW150914_H1), em t_rel ao GPS do merger: branqueada (padrão) ou crua; decimada com envelope min/max "
                      "quando pedir mais de n_max pontos. Devolve t_rel, y, sd fora da fonte, MAD na fonte, pico/sd (guarda de transiente) e o sha256 da série.")
def gw_serie(key: str, branqueada: bool = True, t0: float = -0.5, dur: float = 1.0, n_max: int = 2000) -> dict:
    """Trecho de série (ver a descrição)."""
    return _req("/api/gw/serie?key=%s&branqueada=%d&t0=%s&dur=%s&n_max=%d" % (key, 1 if branqueada else 0, t0, dur, n_max))


@mcp.tool()
def gw_espectro(key: str, f_max: float = 1024.0) -> dict:
    """A ASD (√PSD de Welch) de uma série residente, fora da fonte, até f_max Hz (decimada)."""
    return _req("/api/gw/espectro?key=%s&f_max=%s" % (key, f_max))


@mcp.tool()
def gw_resultados() -> dict:
    """Os estágios da rodada do eco V3 lidos do disco por mtime: pré-registro (leituras, critérios, hashes), PODER antes de abrir, cego, aberto e o RESULTADO selado (vereditos por par leitura × lei)."""
    return _req("/api/gw/resultados")


@mcp.tool(description="EMPILHAMENTO EM TEMPO REAL do eco V3 com filtros — a mesma função do executor (bancada/gw_stack.py), sobre os estágios residentes. sub ∈ {'todos','maio','o4'}; filtros: era, "
                      "snr_min, snr_max, Mf_min, Mf_max, det ('H1'|'L1'), incluir/excluir (listas de eventos); sigma_regra 'max' (a pré-registrada) | 'off' | 'jack'. Devolve, por lei, â ± σ, z_det, "
                      "recuperações, sistemáticas, controles e, por leitura (R1 √β, R2 sin 2θ, R3 β), poder, sistemática relativa, z_excl e o veredito DE CONSULTA. Não é o veredito selado.")
def gw_empilhar(sub: str = "todos", filtros: dict = {}, sigma_regra: str = "max", versao: str = "v3") -> dict:
    """Empilhamento de consulta (ver a descrição); versao 'v3' (a rodada pré-registrada) ou 'v4' (a emenda com grade ±2σ, não cega)."""
    return _req("/api/gw/empilhar", dict(sub=sub, filtros=filtros or {}, sigma_regra=sigma_regra, versao=versao))


@mcp.tool(description="Dispara a rodada da Fase 6 (rodar_fase6.py: confere o pré-registro, estágio cego no WSL, grava o PODER, estágio aberto, RESULTADO) como tarefa; stage 'tudo' | 'cego'. "
                      "Só a gerência deve usar; a rodada exige o pré-registro hasheado em disco.")
def gw_rodar(stage: str = "cego", pool: int = 40, n_off: int = 32) -> dict:
    """Dispara a rodada (ver a descrição)."""
    return _req("/api/gw/rodar", dict(stage=stage, pool=pool, n_off=n_off))


@mcp.tool()
def gw_recarregar(series: bool = True) -> dict:
    """Recarrega do disco os estágios/remanescentes e (series=True) as séries de 32 s — p. ex. depois de um download novo de O4 — sem reiniciar a Bancada."""
    return _req("/api/gw/recarregar", dict(series=series))


@mcp.tool()
def gw_tarefa(tarefa: str) -> dict:
    """Estado de uma rodada disparada por gw_rodar (rodando | pronta | falhou), com a cauda do log."""
    return _req("/api/gw/tarefa/" + tarefa)


@mcp.tool()
def livro() -> dict:
    """O livro de tentativas: as últimas consultas e o número de famílias de teste (usado para corrigir a significância)."""
    return _req("/api/livro")


# O MAPA DE ROTAS (ordem do operador, 28/09/2026): a memória de rotas de TODAS as IAs, em C:\IALD\MAPA_DE_ROTAS. Não depende do
# servidor da Bancada: estas três ferramentas leem e escrevem o livro do mapa direto, pela mesma ferramenta (rotas.py) que o CLI usa.
def _rotas():
    import importlib.util
    spec = importlib.util.spec_from_file_location("rotas", r"C:\IALD\MAPA_DE_ROTAS\rotas.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@mcp.tool()
def rotas_consultar(padrao: str = "", dominio: str = "", status: str = "") -> dict:
    """ANTES de examinar qualquer caminho, consulte o MAPA DE ROTAS: o que já foi examinado, por quem, com que resultado, o defeito
    conhecido, por que não refazer e o próximo passo. padrao = regex (sem acento e sem caixa); dominio e status são filtros opcionais."""
    try:
        return _rotas().consultar(padrao, dominio or None, status or None)
    except Exception as e:
        return dict(erro=str(e))


@mcp.tool()
def rotas_ver(rota_id: str) -> dict:
    """Uma rota do mapa com a história inteira (todos os registros, erratas ao lado, artefatos com sha256)."""
    try:
        return _rotas().ver(rota_id)
    except Exception as e:
        return dict(erro=str(e))


@mcp.tool()
def rotas_registrar(registros: list[dict], quem: str = "") -> dict:
    """DEPOIS de examinar, registre no MAPA DE ROTAS (só acréscimo; a correção vai AO LADO como ERRATA). Cada registro: tipo (ROTA para
    rota nova; RESULTADO/ANOTACAO/ERRATA para rota existente), rota_id, dominio, titulo, status, e o que couber de pergunta, dados,
    metodo, resultado, veredito, estatuto, defeito, nao_refazer, proximo_passo, onde, artefatos (caminhos; o sha256 é calculado),
    refs, olhou_dados, corrige (seq, só em ERRATA), nota. quem = sua identidade (padrão: o cliente do MCP)."""
    try:
        return _rotas().registrar(registros, quem or CLIENTE)
    except Exception as e:
        return dict(ok=False, erro=str(e))


# O CANAL N_eff (Fase 8, 06/10/2026): a identidade ρ+p na era da radiação (ΔN_eff = (4/3)(1+F·N)/F·β); não depende do servidor HTTP:
# importa bancada/neff_canal.py direto (lê a fonte congelada por AST com sha256; β do um.py em runtime). Mede e cita; não emite veredito.
@mcp.tool(description="Canal N_eff da TGL: ΔN_eff pela identidade ρ+p, as DUAS convenções (separação TGL–SM em σ e tensão de cada modelo contra o centro "
                      "medido) por linha pinada de fonte, sem selecionar Yp, poder por σ futura (sigmas_extra) e, se controle=True, o controle anti-dupla-contagem "
                      "(H(z) na radiação: motor V3 com Φ_total vs ΛCDM com nnu deslocado, < 1e-4). Medidas [DECLARADO] até as fontes por sha256.")
def neff_canal(sigmas_extra: list[float] = [], controle: bool = False) -> dict:
    """Two pinned Yp readings; canonical parameters; no primary choice implicit."""
    return _req("/api/neff", dict(sigmas_extra=sigmas_extra, controle=controle))


@mcp.tool(description="F7.2 neutrinos: confere hashes e AST dos scripts científicos de junho sem executá-los; apresenta a proveniência e as lacunas de mapeamento. Sem limite numérico TGL, veredito de natureza ou efeito no gate.")
def neutrino_canal_f72() -> dict:
    """Compatibility alias; serves the explicitly identified current source contract."""
    return _req("/api/neutrino/fontes")


@mcp.tool(description="F7.2 V2 JUNO: verifica as dez fontes PDF pinadas e o canal n=-2 sem executar scripts de junho. Retorna limites apenas dos modelos publicados; tau-star TGL nulo e gate NONE.")
def neutrino_canal_f72_v2() -> dict:
    """Pinned neutrino sources; mapping and model limits retain explicit scope."""
    return _req("/api/neutrino/fontes")


@mcp.tool()
def contratos() -> dict:
    """Current canonical identity and declared capabilities; drift is a visible refusal."""
    return _req("/api/contratos")


@mcp.tool()
def neutrino_contrato() -> dict:
    """Recovered author channels and provenance; no observed-data fit."""
    return _req("/api/neutrino/contrato")


@mcp.tool()
def neutrino_sintetico(payload: dict) -> dict:
    """Conditional evolution. Requires an explicit channel and state/parameters. No nature sigma."""
    return _req("/api/neutrino/sintetico", payload)


if __name__ == "__main__":
    mcp.run()

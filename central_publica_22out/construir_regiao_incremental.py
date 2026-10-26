# -*- coding: utf-8 -*-
# (DERIVADO por derivar_incrementais.py em 22/10/2026 — construtor INCREMENTAL: pula o que o preparo já viu e não mudou desde
#  IALD_PUBLICO_DESDE; IALD_PUBLICO_JA_VISTOS = lista JSON dos caminhos já vistos. Tudo o mais é a esteira original, intacta.)
"""Os repositórios públicos do work/ e da bancada Chatgpt/ (github.com/rotolimiguel-iald/central-publica-work e central-publica-bancada),
pela mesma ordem e pelo mesmo critério do núcleo (construir_nucleo_publico.py). Copia para uma pasta NOVA:
  - FORA: pastas de protocolo/patentes/e-mail/pagamento/monitor/prazos e de dados de usuário do app (carteira, identidades, TestFlight,
    acesso privado da Apple) — no 1º nível pelo nome, e EM QUALQUER PROFUNDIDADE pelo nome exato da pasta (estado de execução, perfis de
    navegador, login, segredos, sessões, cópias da memória ACOM, conversas, anexos, cópias de Patentes/, fontes externas de terceiros,
    pacotes de terceiros, árvores de build); todo arquivo com credencial; builds e ambientes; backups de sessão; acima de 25 MB (índice
    apenas); binários de cache; PDFs que não são da casa (obra de terceiro) ou que trazem dado pessoal forte; imagens que não são figura
    de rito (capturas de tela, páginas renderizadas, ícones, fotos);
  - DENTRO: código e resultados (texto e figuras dos ritos), com dado pessoal trocado à vista e, nos .md, as notas operacionais omitidas.
Achados de 22/10/2026 (medidos antes de publicar): a 1ª versão olhava o nome da pasta só no 1º nível — o estado do orquestrador
(IALD_ORQUESTRACAO_20260923/state: profiles, login, secrets) e as cópias de Patentes/ e da memória ACOM em profundidade teriam entrado; e
copiava PDFs de terceiros (arXiv, livros) e capturas de tela. A guarda de marcadores privados virou a guarda pública (guarda_publica.py).
Uso: C:\\Python314\\python.exe construir_regiao_publica.py <work|Chatgpt> <pasta_destino_nova>"""
import hashlib, json, os, re, shutil, sys, time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
from mascara_pii import mascarar            # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
import guarda_publica as GP                 # noqa: E402

REG = sys.argv[1]
assert REG in ("work", "Chatgpt")
SRC = Path(r"C:\IALD\Central de Patentes") / REG
DST = Path(sys.argv[2])
DESDE = float(os.environ["IALD_PUBLICO_DESDE"])
JA = set(json.loads(Path(os.environ["IALD_PUBLICO_JA_VISTOS"]).read_text(encoding="utf-8")))
assert not DST.exists() or not any(DST.iterdir()), "a pasta de destino precisa ser nova ou vazia — PARAR"
DST.mkdir(parents=True, exist_ok=True)
TXT = {".py", ".lean", ".md", ".json", ".jsonl", ".txt", ".tex", ".csv", ".tsv", ".toml", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx",
       ".jsx", ".html", ".css", ".ipynb", ".sh", ".ps1", ".bat", ".cfg", ".ini", ".sql", ".bib", ".sty", ".cls", ".xml", ".svg", ".dat",
       ".log", ".out", ".diff", ".patch", ".spec", ".pysnip", ".r", ".jl", ".c", ".h", ".cpp", ".rs", ".go", ".java"}
FIG = {".png", ".pdf", ".jpg", ".jpeg", ".gif", ".webp"}
EXCL_DIR = {".git", ".venv", "venv", "node_modules", "__pycache__", ".lake", "tex_environment", ".wheels_ipv4", "unsloth_compiled_cache",
            "site-packages", "dist-packages", ".mypy_cache", ".pytest_cache", "build", ".cache",
            # 25/10/2026: ambientes conda/mamba (pacotes de terceiros; o C18 da v400 parou num deles)
            "mamba_root", "micromamba", "conda-meta", ".conda", "conda_pkgs", "miniconda3", "miniforge3", "anaconda3"}
PASTA_FORA = re.compile(r"(?i)(patente|epct|(^|_)pct|mandado|(^|_)ms(_|$)|escritorio|e-?mail|outlook|inpi|wipo|(^|_)gru(_|$)|(^|_)pix|"
                        r"pagamento|recibo|sentinela|monitor|andamento|prazo|deadline|owner|private|privad|apple|testflight|login|senha|"
                        r"credential|(^|_)conta(_|$)|contabil|fiscal|cnpj|(^|_)ordem_00|revisao_0|token|wallet|carteira|users?_|usuario|"
                        r"user_identity|operational_identity)")
# em QUALQUER profundidade, pelo nome EXATO da pasta
FUNDA_FORA = re.compile(r"(?i)^(state|secrets?|profiles?|login|logins|credentials?|cookies?|session_requests?|sessions|wallet|carteira|"
                        r"user_identity|operational_identity|owner_apple_private_access|testflight.*|e2_private|.*deadline.*|.*prazo.*|"
                        r"patentes?|patents|epct.*|inpi.*|wipo.*|mandado.*|escritorio.*|e-?mails?|outlook|inbox|outbox|mailbox|pagamentos?|"
                        r"gru|pix|memoria_iald|kimi-runs|conversations?|conversas?|chats?|uploads?|attachments?|anexos?|fontes_externas|"
                        r"references|referencias|literatura|bibliografia|papers|vendor|third_party|intermediates|generated|\.gradle|\.kotlin|"
                        r"pods|deriveddata|xcuserdata|\.idea|\.vs|tmp|temp|"
                        # (22/10/2026) os dados/logs/configuração do MiKTeX registram cada ferramenta de PDF rodada NA MÁQUINA, com a
                        # pasta e o nome do arquivo — inclusive de dentro do Escritório (peças com número de processo)
                        r"miktex.*)$")
# ERRATA AO LADO (22/10/2026, custódia v396): «^varredura_» pegava também resultados científicos (rito9: varredura_n.csv, a varredura em
# n; cadeia_de_selo/v392_auditoria: varredura_nos.*). A regra é das listas LOCAIS desta esteira (caminhos e motivos de exclusão), cujos
# prefixos são estes; o resto que começa por «varredura_» é resultado e entra pela esteira comum.
ARQ_FORA = re.compile(r"(?i)(^varredura_(arquivos|buscas|conferencia|convites|dados|escritorio|exclusoes|formatos|miktex|pastas|pdf|"
                      r"reservados|segredos|terceiros|usuarios)|^ja_vistos_|^git_(add|rm)_|^barrados.*\.json$|acervo.*\.stdout\.txt$|^corpus_matches|^inventario_busca|conversa|conversation|chat_?hist|chat_?log|transcri|^inbox|^outbox|"
                      r"testers?\.json$|^users?\.json$|^usuarios?\.json$|^accounts?\.json$|^contas?\.json$|session_?requests?)")
PASTA_APP = re.compile(r"(?i)^(iald_|app_|mimo|ialdapp)|attachment|anexo|upload")
LIM_TXT = 25 * 1024 * 1024


LOCAL_EXCL = {}


def fora_(m, x):
    fora[m] += 1
    LOCAL_EXCL.setdefault(m, []).append(x)


def lp(x):
    r"""Caminho longo do Windows (acima de 260 caracteres): o prefixo \\?\ na leitura e na escrita (achado de 22/10/2026)."""
    x = str(Path(x).resolve())
    return x if x.startswith("\\\\?\\") else "\\\\?\\" + x


fora = Counter(); fora_pastas = []; fundas = Counter()
indice, masc = [], Counter()
n_md = 0
t0 = time.time()
tops = sorted(p for p in SRC.iterdir())
for top in tops:
    if top.is_dir() and PASTA_FORA.search(top.name):
        fora_("pasta de protocolo, patentes, pagamento ou dados de usuário", top.name); fora_pastas.append(top.name); continue
    app = top.is_dir() and bool(PASTA_APP.search(top.name))
    walker = os.walk(top) if top.is_dir() else [(str(SRC), [], [top.name])]
    for dp, dns, fns in walker:
        manter = []
        for d in dns:
            if d in EXCL_DIR:
                continue
            if FUNDA_FORA.match(d):
                fundas[d.lower()] += 1
                continue
            manter.append(d)
        dns[:] = manter
        for f in fns:
            p = Path(dp) / f
            rel = p.relative_to(SRC).as_posix()
            e = p.suffix.lower()
            if rel in JA:
                try:
                    if os.stat(lp(p)).st_mtime < DESDE:
                        continue
                except OSError:
                    pass
            if ".bak_" in f or f.endswith(".tmp") or ".tmp_" in f or f.lower().endswith((".bak", "~")):
                fora_("backup de sessão", rel); continue
            if GP.arquivo_de_credencial(f):
                fora_("arquivo de credencial", rel); continue
            if ARQ_FORA.search(f):
                fora_("conversa, usuários ou varredura de dado pessoal", rel); continue
            try:
                s = os.stat(lp(p)).st_size
                if e in TXT and s > LIM_TXT:
                    fora_("texto acima de 25 MB (índice apenas)", rel); continue
                if e in FIG and s > LIM_TXT:
                    fora_("figura acima de 25 MB (índice apenas)", rel); continue
                if e not in TXT and e not in FIG:
                    fora_("binário de cache ou outro formato (índice apenas)", rel); continue
                raw = open(lp(p), "rb").read()
            except OSError:
                fora_("ilegível no disco", rel); continue
            d = DST / rel
            if e in TXT:
                txt = raw.decode("utf-8", "replace")
                n_cred, pii_blob = GP.avaliar_texto(txt)
                if n_cred:
                    fora_("contém credencial", rel); continue
                if pii_blob:
                    fora_("carga embutida com dado pessoal", rel); continue
                txt, c = mascarar(txt)
                if e == ".md":
                    txt, n = filtrar_markdown(txt)
                    if n:
                        c["notas_operacionais_omitidas"] = n; n_md += 1
                # (22/10/2026) a regra do Escritório vale para o que VAI AO AR (depois da máscara e do filtro): o acervo do Escritório,
                # PJ separada, nunca entra; uma nota operacional já omitida não conta
                if GP.toca_escritorio(txt):
                    fora_("toca o acervo do Escritório (PJ separada: caminhos internos, audiências, processos)", rel); continue
                b = txt.encode("utf-8")
            else:
                if app:
                    fora_("imagem/PDF em pasta do app (pode ser anexo de usuário)", rel); continue
                if e == ".pdf":
                    if not GP.pdf_da_casa(raw):
                        fora_("PDF de terceiro (obra alheia; baixar da fonte)", rel); continue
                    n_cred, kk = GP.avaliar_bytes(f, raw)
                    if n_cred or kk:
                        fora_("PDF com dado pessoal ou credencial", rel); continue
                elif e == ".png":
                    if not GP.png_de_rito(raw):
                        fora_("imagem que não é figura de rito (captura de tela, página, ícone)", rel); continue
                else:
                    fora_("imagem que não é figura de rito (captura de tela, página, ícone)", rel); continue
                b = raw
            try:
                os.makedirs(lp(d.parent), exist_ok=True)
                with open(lp(d), "wb") as fh:
                    fh.write(b)
            except OSError:
                fora_("não gravável no preparo", rel); continue
            if e in TXT:
                for k, v in c.items():
                    masc[k] += v
            indice.append({"caminho": rel, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    print("  ... %s: %d arquivos (%.0f s)" % (top.name[:40], len(indice), time.time() - t0), flush=True)
(DST / "INDICE_PUBLICO.json").write_text(json.dumps({"regiao": REG, "gerado_em": time.strftime("%Y-%m-%d %H:%M:%S"), "n_arquivos": len(indice),
                                                      "arquivos": indice}, ensure_ascii=False), encoding="utf-8")
(DST / "EXCLUSOES_PUBLICAS.json").write_text(json.dumps({"regiao": REG, "criterio": "dados pessoais, credenciais e notas operacionais do operador "
                                                         "ficam fora; obras de terceiros (PDFs, pacotes) ficam fora; todo o código e todo "
                                                         "resultado da casa ficam", "por_motivo": dict(fora),
                                                         "pastas_fora_no_primeiro_nivel": len(fora_pastas),
                                                         "pastas_fora_em_profundidade_por_nome": dict(fundas.most_common()),
                                                         "mascaras_de_dado_pessoal": dict(masc),
                                                         "md_com_notas_operacionais_omitidas": n_md}, ensure_ascii=False, indent=1), encoding="utf-8")
print("%s público: %d arquivos | fora: %s | pastas fundas fora: %s | máscaras: %s | %.0f s" % (
    REG, len(indice), dict(fora), dict(fundas.most_common(20)), dict(masc), time.time() - t0))
(W / ("varredura_exclusoes_%s.json" % DST.name)).write_text(json.dumps(LOCAL_EXCL, ensure_ascii=False, indent=0), encoding="utf-8")

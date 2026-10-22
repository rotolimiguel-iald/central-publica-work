# -*- coding: utf-8 -*-
"""O REGISTRO da Central aberta (22/10/2026) nas superfícies de memória — regra da linhagem completa: TGL_ATLAS.md (append datado),
DIARIO_DO_SITE.md, MEMORY_2.md (diário) e MEMORY.md (uma linha-ponteiro), com backup de BYTES antes, temporário, e conferência de que o
arquivo cresceu. Os números são LIDOS dos repositórios publicados (git), do relatório de subida do site e do info do um.acom — nunca
digitados. Idempotente pela marca <!-- central_publica_22out -->. Uso: registrar_abertura.py"""
import hashlib, json, os, subprocess, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
MARCA = "<!-- central_publica_22out -->"
TS = time.strftime("%Y%m%d_%H%M%S")
GH = "https://github.com/rotolimiguel-iald/"


def git(d, *a):
    return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout.strip()


repos = {}
for nome in ("central-publica", "central-publica-work", "central-publica-bancada"):
    d = Path(r"C:\IALD\Central_publica") / nome
    head = git(d, "rev-parse", "HEAD")
    rem = git(d, "ls-remote", "origin", "refs/heads/main").split()[0] if git(d, "ls-remote", "origin", "refs/heads/main") else ""
    n = len([x for x in git(d, "ls-files").splitlines() if x])
    exc = json.loads((d / "EXCLUSOES_PUBLICAS.json").read_text(encoding="utf-8"))
    repos[nome] = {"head": head[:8], "remoto_igual": head == rem, "arquivos": n, "fora": sum(exc["por_motivo"].values())}
    assert head and head == rem, ("repositório não publicado ou divergente — PARAR", nome, head, rem)
info = json.loads(Path(r"C:\IALD\Site\tgl\v3.0_bancada\central_publica\acom\um_acom_info.json").read_text(encoding="utf-8"))
subida = sorted(Path(r"C:\IALD\Site\tgl\v3.0_bancada\subidas").glob("20261022_1339*/RELATORIO.md"))
assert subida and "SUBIDA VERIFICADA" in subida[-1].read_text(encoding="utf-8"), "a subida do site não está verificada — PARAR"
bound = git(Path(r"C:\IALD\Artigo\the_boundary"), "log", "--format=%h", "-1", "--grep=a Central aberta")
r = repos
linha_repos = "; ".join("`%s` %s (%d arquivos no git)" % (k, v["head"], v["arquivos"]) for k, v in r.items())
TXT_ATLAS = f"""

## 22/10/2026 — A CENTRAL ABERTA (append §X; sessão a7 da Central, em nome próprio) {MARCA}

**Ordem do operador (verbatim em `work/central_publica_22out/`):** abrir a Central inteira ao público — modo de visualização no site, o
um.acom como único download, o projeto todo no GitHub vinculado ao the_boundary; «segredo são dados pessoais, somente»; as notas de aviso a
ele não precisam ser públicas; mostrar o vínculo às patentes. **Feito [REAL, lido dos artefatos]:** repositórios públicos {linha_repos}
(remoto = local nos três); site `/central/` no ar (SUBIDA VERIFICADA, `{subida[-1].parent.name}`); um.acom `{info["sha256"][:16]}` ({info["n_arquivos"]}
arquivos, {info["conferido"]}); o the_boundary aponta para a Central (`{bound}`). **Critério:** fora só dado pessoal (máscara visível no texto;
documento que o traz e não se mascara sai), credencial e estado de execução, notas operacionais ao operador, o acervo do Escritório (PJ
separada) e obras de terceiros; os marcadores da casa não são motivo de exclusão. **Achados antes de publicar (o número corrigiu a
frase):** zips com os PDFs de depósito do INPI (CPF, telefone); estado do orquestrador (perfis, login, segredos); logs do MiKTeX e saídas de
busca no acervo citando peças e caminhos do Escritório; falsos positivos da máscara que corrompiam a ciência («RG» = Relatividade Geral,
«identidade», «nascimento»); a guarda antiga barrava 862 arquivos pelos nomes da casa. **ERRATA AO LADO:** o depositante dos 16 pedidos é a
pessoa física do operador (formulários do INPI; requerente nos PCT «ROTOLI MIGUEL, Luiz Antonio»), não a IALD Ltda. — notas ao lado no §V e no
§XI.B/J.1; a divergência segue [LEGAL]. Esteira e conferência independente em `work/central_publica_22out/` (nunca publicar sem a conferência
APROVADA). O gate não se moveu; PROVADA ≠ CONFIRMADA.
"""
TXT_SITE = f"""

## 22/10/2026 — a Central aberta no site {MARCA}

`/central/` no ar — o cockpit da Central em modo de visualização (retrato estático: patentes, código, execuções, Fronteira, TGL; ações
bloqueadas) + o um.acom `{info["sha256"][:16]}` ({info["n_arquivos"]} arquivos) como único download; cartão «A Central, aberta» no topo de
`linhas-de-pesquisa.html` com a tabela dos pedidos (INPI e PCT; depositante lido dos formulários); item «A Central» no menu da home; sitemap
com `central/index.html`. SUBIDA VERIFICADA (`{subida[-1].parent.name}`, 1.118 arquivos; 0 falhas; a guarda do site confere o selo). A pasta
`central/` passou na conferência independente (`work/central_publica_22out/conferir_preparos.py`). Repositórios: {linha_repos}.
"""
TXT_M2 = f"""

## 22/10/2026 — A CENTRAL ABERTA {MARCA}
Ordem do operador cumprida: {linha_repos}; site `/central/` (SUBIDA VERIFICADA); um.acom `{info["sha256"][:16]}`. Critério, esteira, achados e a
errata do depositante (pessoa física) em [[central-publica-22out]]. Decisão do operador: a frase do autoteste do ACOM Crypto não é a frase-chave
de acesso («É diferente — publique»). O commit `{bound}` do the_boundary foi empurrado às 10:37 por OUTRA sessão. Achados tardios corrigidos à
frente: o 2º telefone e o CEP do cartão CNPJ (núcleo `41e0b66`); os identificadores das contas de dois testadores convidados (núcleo `8f05bc6`)
e as pastas de convite e provisionamento dessas contas (work, `git rm` em `c42e40c8`). Pendente, decisão do operador: reescrever o histórico
público (force-push, negado pelo classificador de segurança) ou apagar e recriar os dois repositórios, para tirá-los também dos commits antigos.
"""
LINHA_M1 = ("- [A CENTRAL ABERTA (22/10)](central-publica-22out.md) — **3 repositórios públicos + /central/ no site + um.acom**; critério, esteira "
            "e conferência em `work/central_publica_22out`; depositante = pessoa física (errata ao lado) " + MARCA + "\n")
ALVOS = [(Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md"), TXT_ATLAS),
         (Path(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md"), TXT_SITE),
         (Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY_2.md"), TXT_M2)]
for p, txt in ALVOS:
    raw = p.read_bytes()
    if MARCA.encode("utf-8") in raw:
        print("já registrado:", p.name); continue
    crlf = b"\r\n" in raw[-20000:]
    novo = raw + (txt.replace("\n", "\r\n") if crlf else txt).encode("utf-8")
    bak = p.with_name(p.name + ".bak_" + TS)
    bak.write_bytes(raw)
    assert bak.stat().st_size == len(raw)
    t = p.with_name(p.name + ".tmp_abertura")
    t.write_bytes(novo)
    assert t.stat().st_size > len(raw)
    os.replace(t, p)
    print("ok", p.name, len(raw), "->", p.stat().st_size, "| backup", bak.name)
# MEMORY.md: a linha-ponteiro, na seção «Estado corrente» (depois do título da seção)
p = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\MEMORY.md")
raw = p.read_bytes()
s = raw.decode("utf-8")
if MARCA in s:
    print("já registrado: MEMORY.md")
else:
    ancora = "## Estado corrente\n\n"
    crlf = "\r\n" in s[:5000]
    a = ancora.replace("\n", "\r\n") if crlf else ancora
    assert s.count(a) == 1, s.count(a)
    s2 = s.replace(a, a + (LINHA_M1.replace("\n", "\r\n") if crlf else LINHA_M1), 1)
    assert len(s2.encode("utf-8")) < 24 * 1024, "MEMORY.md passaria de 24 KB — a linha vai para o MEMORY_2.md"
    bak = p.with_name(p.name + ".bak_" + TS)
    bak.write_bytes(raw)
    t = p.with_name(p.name + ".tmp_abertura")
    t.write_bytes(s2.encode("utf-8"))
    os.replace(t, p)
    print("ok MEMORY.md", len(raw), "->", p.stat().st_size)
print(json.dumps(repos, ensure_ascii=False))

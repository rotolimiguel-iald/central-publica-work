# -*- coding: utf-8 -*-
r"""RETOMADA da publicação fora da cadeia do pré-registro H0DN × BG1 (12/11/2026, claude-site-custodia).

O que aconteceu: publicar_fora_da_cadeia.py --aplicar gravou os 57 novos e o índice, refez as partes (indice_partes.py) e a conferência
do delta aprovou 59 caminhos (conferir_delta.py, 06:38:27). O atualizar_repo_publico.py parou no `git add -f --pathspec-from-file` do
índice inteiro (560.887 caminhos): 3.917 s sem escrever o index.lock (o mesmo passo que levou 14.322 s na v410). A gerência c1 mediu e
sugeriu (12/11, 07:40): parar pelos PIDs e fazer o add só do delta conferido. Parado às 07:43 pelo PID do git (descendente do job desta
sessão); o atualizar e o publicador saíram pelo próprio caminho de falha, sem nada desfeito.

O que faz: EXATAMENTE o atualizar_repo_publico.py (mesmas exigências, mesmo commit, push sem força, árvore remota = índice + raiz), com
uma diferença só: o `git add` recebe o que difere do HEAD (os caminhos do índice que o git não rastreia + os rastreados que o status
mostra mudados), não o índice inteiro. Com a árvore de trabalho igual ao HEAD fora disso, o stage é o mesmo. Depois, o passo 5 do
publicador: o commit, a data, a conferência pelo raw de cada arquivo e das quatro chaves, e o recibo. Sem --aplicar: só mostra."""
import hashlib, json, os, subprocess, sys, time, urllib.parse, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes")
W = CEN / "work" / "central_publica_22out"
AQUI = Path(__file__).resolve().parent
D = Path(r"C:\IALD\Central_publica\central-publica-work")
NOME = "central-publica-work"
REPO = "rotolimiguel-iald/central-publica-work"
MANIF = CEN / "work" / "h0dn_bg1_v411_emenda_11nov" / "MANIFESTO_DA_PUBLICACAO_12nov.json"
MANIF_SHA = "1c91af10c8795057c535a1a686997e15422ec5f99179cc453090804fa2aecb43"
PROIBIDO = CEN / "work" / "h0dn_bg1_v411_emenda_11nov" / "producao" / "RESULTADO_DA_ABERTURA_V411.json"
CHAVES = {"texto_final": "06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8",
          "pinos_de_producao": "95adfeea37e1c8f6100876082c1f3e021b3eb2f67f44fecaf403302ab66d9c9d",
          "vetor": "536b07e222e57732dc1075880038d73845e61b0c53eadf9880041576141ff131",
          "literal_dos_vereditos": "47624a41242869708b61ccbd4fc55d6af186846da1eec81661ccf12013cf4c43"}
HEAD0 = "0086a4c03"   # o HEAD do preparo antes desta publicação (lido em 12/11 pelo publicador)
BK = D.parent / "_backup_indice_work_20261112_063618_fora_da_cadeia.json"   # o índice antes dos 57 (gravado pelo publicador)
MARCA = "[FORA_DA_CADEIA]"
CO = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
ENV = dict(os.environ, GIT_LITERAL_PATHSPECS="1")
RAIZ_GERADA = ["INDICE_PUBLICO.json", "EXCLUSOES_PUBLICAS.json", ".gitattributes", "llms.txt", "RECONSTRUIR_COPIAS.py"]
APLICAR = "--aplicar" in sys.argv
STAMP = time.strftime("%Y%m%d_%H%M%S")


def parar(msg):
    raise SystemExit("PARAR: " + msg)


def g(*a, ok=True):
    r = subprocess.run(["git", "-C", str(D)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    if ok and r.returncode != 0:
        parar("git %s falhou: %s" % (" ".join(a[:3]), (r.stderr or r.stdout)[-800:]))
    return r


def sha(b):
    return hashlib.sha256(b).hexdigest()


# 0) o que não pode existir, o manifesto e as chaves (como no publicador)
if PROIBIDO.exists():
    parar("o resultado da abertura existe: %s" % PROIBIDO)
mb = MANIF.read_bytes()
if sha(mb) != MANIF_SHA:
    parar("o manifesto mudou")
M = json.loads(mb.decode("utf-8"))
for k, s in CHAVES.items():
    if M["chaves"][k]["sha256"] != s:
        parar("a chave %s não confere com o pedido" % k)
if (D / ".git" / "index.lock").exists():
    parar("index.lock presente: outro git no preparo?")

# 1) o estado que o publicador deixou: HEAD = origin/main = HEAD0; índice com os 57; delta conferido e aprovado
g("fetch", "-q", "origin")
h0 = g("rev-parse", "HEAD").stdout.strip()
if not h0.startswith(HEAD0) or h0 != g("rev-parse", "origin/main").stdout.strip():
    parar("HEAD/origin não são o HEAD de antes (%s)" % h0[:12])
ant = {a["caminho"] for a in json.loads(BK.read_bytes().decode("utf-8"))["arquivos"]}
publicados = [c for c in M["arquivos"] if ".bak_" not in c["caminho"]]
fora = [c["caminho"] for c in M["arquivos"] if ".bak_" in c["caminho"]]
esperados = {c["caminho"][len("work/"):] for c in publicados if c["caminho"][len("work/"):] not in ant}
ja = [c["caminho"] for c in publicados if c["caminho"][len("work/"):] in ant]
n_npz = sum(1 for c in publicados if c["caminho"].endswith(".npz"))
for c in publicados:
    q = D / c["caminho"][len("work/"):]
    if sha(open("\\\\?\\" + str(q), "rb").read()) != c["sha256"]:
        parar("no preparo com outros bytes: %s" % c["caminho"])

idx_mt = (D / "INDICE_PUBLICO.json").stat().st_mtime
dconf = W / ("varredura_conferencia_delta_%s.json" % D.name)
dj = json.loads(dconf.read_text(encoding="utf-8"))
if not (dconf.stat().st_mtime > idx_mt and dj.get("aprovado") is True):
    parar("a conferência do delta não é mais nova que o índice ou não está aprovada")
COBERTO = set(dj.get("delta_conferido") or [])
_todas = json.loads((D / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]
idx = [a["caminho"] for a in _todas if not a.get("igual_a")]
n_refs = len(_todas) - len(idx)
if n_refs:
    parar("há cópias referenciadas no índice (não esperadas antes da v411)")
raiz = [n for n in RAIZ_GERADA if (D / n).is_file()]
PARTES_CAB = D / "INDICE_PUBLICO_PARTES" / "PARTES.json"
_env_ci = {k: v for k, v in os.environ.items() if k != "GIT_LITERAL_PATHSPECS"}
if subprocess.run(["git", "-C", str(D), "check-ignore", "-q", "INDICE_PUBLICO.json"], capture_output=True, env=_env_ci).returncode != 0:
    parar("o índice inteiro não está fora do git")
cab_p = json.loads(PARTES_CAB.read_text(encoding="utf-8"))
if cab_p.get("entradas") != len(_todas):
    parar("PARTES.json não tem as entradas do índice")
pts = ["INDICE_PUBLICO_PARTES/PARTES.json"] + [p["arquivo"] for p in cab_p["partes"]]
raiz = [n for n in raiz if n != "INDICE_PUBLICO.json"] + pts
quer = set(idx) | set(raiz)
tem = set(x for x in g("ls-files", "-z").stdout.split("\0") if x)
sair = sorted(tem - quer)
if sair:
    parar("há rastreados fora do índice (%d): %s" % (len(sair), sair[:5]))

# 2) o add só do que difere do HEAD
st0 = g("status", "--porcelain", "-z", "--untracked-files=all").stdout.split("\0")
mudados = set()
for e in st0:
    if len(e) > 3:
        mudados.add(e[3:])
add = sorted((quer - tem) | (mudados & quer))
fora_stage = sorted(mudados - quer)
print("add: %d caminhos (novos no git %d; rastreados mudados %d) | fora do stage %d %s" % (
    len(add), len(quer - tem), len(mudados & quer & tem), len(fora_stage), fora_stage[:5]))
if set(add) - COBERTO:
    parar("caminho no add sem conferência: %s" % sorted(set(add) - COBERTO)[:8])
if not esperados <= set(add) or set(add) - esperados - set(pts):
    parar("o add não é o esperado: faltam %s; sobram %s" % (sorted(esperados - set(add))[:5], sorted(set(add) - esperados - set(pts))[:5]))
if not APLICAR:
    print("MODO SECO (nada no stage)")
    sys.exit(0)

lista = D / ".git" / "incr_add_delta.txt"
lista.write_bytes(b"\0".join(x.encode("utf-8") for x in add))
t0 = time.time()
g("add", "-f", "--pathspec-from-file=" + str(lista), "--pathspec-file-nul")
print("add em %.0f s" % (time.time() - t0))

# 3) o mesmo do atualizar_repo_publico.py, linha por linha
st = g("diff", "--cached", "--name-status").stdout.splitlines()
n_a = sum(1 for l in st if l.startswith("A")); n_m = sum(1 for l in st if l.startswith("M")); n_d = sum(1 for l in st if l.startswith("D"))
entra = {x for x in g("diff", "--cached", "--name-only", "-z", "--diff-filter=AM").stdout.split("\0") if x}
sem = sorted(entra - COBERTO - {"README.md", "PATENTES.md", "vinculo_patentario.json"} - set(RAIZ_GERADA))
if sem or n_d or entra != set(add):
    g("reset", "-q")
    parar("o stage não é o conferido (sem conferência %s; D %d; diferença %s) — nada publicado" % (sem[:8], n_d, sorted(entra ^ set(add))[:5]))
print("%s: no stage A %d / M %d / D %d" % (NOME, n_a, n_m, n_d))
TIT = ("Pré-registro do teste H0DN × BG1 (emenda v411), publicado antes da abertura (12/11/2026)\n\n"
       "%s Publicação fora da cadeia, pedida pela gerência c1 por decisão do operador de 11 e 12/11/2026: o texto final do pré-registro "
       "(EMENDA_E_PRE_REGISTRO_V411.md), os pinos de produção, o vetor pinado e o literal dos vereditos, com o pacote da emenda, pelo "
       "manifesto MANIFESTO_DA_PUBLICACAO_12nov.json (sha256 %s). Nada foi aberto: o resultado da abertura não existe.\n"
       "Os %d backups de sessão (.bak_) do manifesto ficam fora, pela regra da esteira; os %d .npz entram com os bytes do manifesto "
       "(resultado da casa em formato zip, varrido por dentro pela conferência independente). Os %d arquivos do manifesto já publicados "
       "na v410 seguem com os mesmos bytes. O README não foi regerado (as contagens são as da cadeia de 11/11/2026); a próxima cadeia o "
       "regera, e o DESDE dela ignora este commit." % (MARCA, MANIF_SHA, len(fora), n_npz, len(ja)))
msg = ("%s\n\nCustódia v396 (22/10/2026): a mesma esteira da abertura (guarda pública, máscara visível, filtro das notas, regra do Escritório), "
       "em rodada incremental; conferência independente aprovada antes do envio. Acrescentados %d, alterados %d, retirados %d.\n\n%s\n"
       % (TIT, n_a, n_m, n_d, CO))
(D / ".git" / "msg_incr.txt").write_text(msg, encoding="utf-8")
g("commit", "-q", "-F", str(D / ".git" / "msg_incr.txt"))
t0 = time.time()
r = g("push", "origin", "main", ok=False)
if r.returncode != 0:
    time.sleep(30)
    r = g("push", "origin", "main", ok=False)
    if r.returncode != 0:
        parar("push falhou: %s" % r.stderr[-800:])
loc = g("rev-parse", "HEAD").stdout.strip()
g("fetch", "-q", "origin")
rem = g("rev-parse", "origin/main").stdout.strip()
arv = [x for x in g("ls-tree", "-r", "-z", "--name-only", "origin/main").stdout.split("\0") if x]
print("%s: HEAD %s = origin/main %s | árvore remota %d arquivos (índice %d + raiz %d) | push %.0f s" % (
    NOME, loc[:8], rem[:8], len(arv), len(idx), len(raiz), time.time() - t0))
if not (loc == rem and set(arv) == quer):
    parar("a árvore remota não é o índice (%d vs %d)" % (len(arv), len(quer)))
print("PUBLICADO E CONFERIDO")

# 4) o passo 5 do publicador: o commit, a data e a conferência pelo raw
h = loc
if h == h0:
    parar("o commit não chegou ao remoto")
ci = g("log", "-1", "--format=%cI", h).stdout.strip()
tocados = [l.split("\t") for l in g("show", "--name-status", "--format=", h).stdout.splitlines() if l.strip()]
addc = {x[1] for x in tocados if x[0] == "A"}
outros = sorted(x[-1] for x in tocados if not (x[0] == "A" and x[1] in esperados) and not x[-1].startswith("INDICE_PUBLICO_PARTES/"))
if addc - esperados - {x for x in addc if x.startswith("INDICE_PUBLICO_PARTES/")} or not esperados <= addc or outros:
    parar("o commit tocou além do esperado: %s" % outros[:10])
if any("RESULTADO_DA_ABERTURA" in x for x in arv):
    parar("a árvore publicada traz um resultado da abertura")
raw_ok, raw_falha = 0, []
for a in publicados:
    rel = a["caminho"][len("work/"):]
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, h, urllib.parse.quote(rel))
    try:
        b = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "iald-custodia"}), timeout=60).read()
    except Exception as ex:  # noqa: BLE001
        raw_falha.append((rel, "erro: %s" % ex)); continue
    if sha(b) == a["sha256"] and len(b) == a["bytes"]:
        raw_ok += 1
    else:
        raw_falha.append((rel, "sha256 %s" % sha(b)))
chaves_raw = {}
for k, c in M["chaves"].items():
    rel = c["caminho"][len("work/"):]
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, h, urllib.parse.quote(rel))
    try:
        sr = sha(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "iald-custodia"}), timeout=60).read())
    except Exception as ex:  # noqa: BLE001
        sr = "erro: %s" % ex
    chaves_raw[k] = {"caminho": rel, "url": url, "sha256_esperado": c["sha256"], "sha256_raw": sr, "confere": sr == c["sha256"]}
gh = {}
for nome, args in (("commit", ["api", "repos/%s/commits/%s" % (REPO, h), "--jq", "{sha: .sha, committer_date: .commit.committer.date, html_url: .html_url}"]),
                   ("push", ["api", "repos/%s/activity?per_page=3" % REPO, "--jq", "[.[] | {after, timestamp, activity_type, ref}]"])):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    gh[nome] = json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else {"erro": (r.stderr or "")[-300:]}
recibo = {"o_que_e": "recibo da publicação fora da cadeia do pré-registro H0DN × BG1 (emenda v411), antes da abertura (retomada)",
          "quem": "claude-site-custodia", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "repositorio": "https://github.com/%s" % REPO,
          "commit": h, "commit_anterior": h0, "commit_data_local": ci, "github": gh, "manifesto": {"caminho": str(MANIF), "sha256": MANIF_SHA},
          "novos": len(esperados), "ja_publicados_mesmos_bytes": ja, "fora_bak": fora, "npz": n_npz,
          "stage": {"A": n_a, "M": n_m, "D": n_d}, "raw_conferidos": raw_ok, "raw_total": len(publicados), "raw_falhas": raw_falha,
          "chaves_raw": chaves_raw, "nada_aberto": not PROIBIDO.exists(), "backup_do_indice": str(BK),
          "retomada": "o add do índice inteiro (560.887 caminhos) parou 3.917 s sem escrever; parado pelo PID às 07:43; add só do delta conferido"}
rp = AQUI / ("RECIBO_PUBLICACAO_%s.json" % STAMP)
rp.write_text(json.dumps(recibo, ensure_ascii=False, indent=1), encoding="utf-8")
print("commit %s (%s) | raw: %d/%d conferidos, falhas %s | chaves: %s | recibo %s" % (
    h[:12], ci, raw_ok, len(publicados), raw_falha[:3], {k: v["confere"] for k, v in chaves_raw.items()}, rp.name))
if raw_falha or not all(v["confere"] for v in chaves_raw.values()):
    sys.exit(1)

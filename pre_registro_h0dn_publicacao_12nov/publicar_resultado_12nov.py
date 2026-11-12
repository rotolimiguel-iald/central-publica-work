# -*- coding: utf-8 -*-
r"""PUBLICAÇÃO FORA DA CADEIA do RESULTADO da abertura do teste H0DN × BG1 (emenda v411), DEPOIS da abertura (12/11/2026, claude-site-custodia).

Pedido da gerência c1 (12/11/2026, depois da abertura das 07:46:34, feita uma vez pela ordem do operador
work\cunhagens_13out\OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt): publicar os bytes do
manifesto work\h0dn_bg1_v411_emenda_11nov\MANIFESTO_DA_PUBLICACAO_DO_RESULTADO_12nov.json (sha256 conferido), o próprio manifesto e,
se a guarda aprovar, os scripts e recibos da publicação do pré-registro. Só os bytes, só no repositório do work: README, site e X ficam
como estão (nenhuma superfície apresenta o primário sem a linha das Cefeidas livres e sem as ressalvas da seção 8 do pré-registro; vai no
handoff da v411). O texto final, os pinos e o vetor já publicados (commit 769fcb26) não se tocam.

Como: a guarda da esteira da região (lida do próprio construtor), como no publicar_fora_da_cadeia.py; o que a esteira não leva fica FORA e
dito (sem parar), menos o resultado, que tem de passar ou nada se publica; as linhas novas ao FIM do índice; indice_partes.py,
conferir_delta.py; o add SÓ do que difere do HEAD (a lição da manhã: o add do índice inteiro levou mais de uma hora); um commit com a marca
[FORA_DA_CADEIA], push sem força, árvore remota = índice + raiz; a conferência pelo raw, no hash do commit, e o recibo.
Nada de codigo\ do teste é rodado. A mensagem do commit não traz número do resultado. Sem --aplicar: só mostra o plano."""
import hashlib, json, os, re, subprocess, sys, time, urllib.parse, urllib.request
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
CEN = Path(r"C:\IALD\Central de Patentes")
W = CEN / "work" / "central_publica_22out"
sys.path.insert(0, str(W))
from mascara_pii import mascarar, TERCEIROS  # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
import guarda_publica as GP  # noqa: E402

AQUI = Path(__file__).resolve().parent
D = Path(r"C:\IALD\Central_publica\central-publica-work")
NOME = "central-publica-work"
REPO = "rotolimiguel-iald/central-publica-work"
PY = r"C:\Python314\python.exe"
EM = CEN / "work" / "h0dn_bg1_v411_emenda_11nov"
MANIF = EM / "MANIFESTO_DA_PUBLICACAO_DO_RESULTADO_12nov.json"
MANIF_SHA = "6c1d2d918f928478a0030c9699204e2984a49e38d0f7caa31e3dd22754b25327"
RES_CAM = "work/h0dn_bg1_v411_emenda_11nov/producao/RESULTADO_DA_ABERTURA_V411.json"
RES_SHA = "573fbf87db2ccfe836e7672a3fd6b3bfc98d9fcb4d2ebce1d7cdb30d42abfbed"
PRE = "769fcb2697d8ce983b73645c393e98ea7e2fcb27"   # o commit do pré-registro (tem de ser o HEAD de agora)
JA_INTOCAVEIS = {"h0dn_bg1_v411_emenda_11nov/EMENDA_E_PRE_REGISTRO_V411.md", "h0dn_bg1_v411_emenda_11nov/producao/PINOS_DE_PRODUCAO.json",
                 "h0dn_bg1_v411_emenda_11nov/producao/vetor_y255.npz", "h0dn_bg1_v411_emenda_11nov/producao/RAMOS_V411.json"}
EXTRAS = ["publicar_fora_da_cadeia.py", "retomar_publicacao_12nov.py", "RECIBO_PUBLICACAO_20261112_074508.json",
          "saida_aplicar_12nov.txt", "saida_retomada_12nov.txt", "publicar_resultado_12nov.py"]
MARCA = "[FORA_DA_CADEIA]"
CO = "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
ENV = dict(os.environ, GIT_LITERAL_PATHSPECS="1")
RAIZ_GERADA = ["INDICE_PUBLICO.json", "EXCLUSOES_PUBLICAS.json", ".gitattributes", "llms.txt", "RECONSTRUIR_COPIAS.py"]
APLICAR = "--aplicar" in sys.argv
STAMP = time.strftime("%Y%m%d_%H%M%S")

_src = (W / "construir_regiao_incremental.py").read_text(encoding="utf-8")
_i, _j = _src.index("TXT = {"), _src.index("LIM_TXT = ")
_ns = {"re": re}
exec(compile(_src[_i:_src.index("\n", _j)], "construir_regiao_incremental.py (regras)", "exec"), _ns)
TXT, PASTA_FORA, FUNDA_FORA, ARQ_FORA, EXCL_DIR = _ns["TXT"], _ns["PASTA_FORA"], _ns["FUNDA_FORA"], _ns["ARQ_FORA"], _ns["EXCL_DIR"]


def parar(msg):
    raise SystemExit("PARAR: " + msg)


def g(*a, ok=True):
    r = subprocess.run(["git", "-C", str(D)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    if ok and r.returncode != 0:
        parar("git %s: %s" % (" ".join(a[:3]), (r.stderr or r.stdout)[-600:]))
    return r


def lp(p):
    p = str(Path(p).resolve())
    return p if p.startswith("\\\\?\\") else "\\\\?\\" + p


def sha(b):
    return hashlib.sha256(b).hexdigest()


def guarda(cam, rel, raw):
    """None se a esteira leva o arquivo com os MESMOS bytes; senão, o motivo (o arquivo fica fora)."""
    partes = rel.split("/")
    nome = partes[-1]
    e = Path(nome).suffix.lower()
    if ".bak_" in nome or nome.endswith(".tmp") or ".tmp_" in nome:
        return "backup de sessão: a esteira não publica"
    if PASTA_FORA.search(partes[0]) or any(FUNDA_FORA.match(x) or x in EXCL_DIR for x in partes[1:-1]):
        return "pasta que a esteira barra"
    if GP.arquivo_de_credencial(nome) or (TERCEIROS is not None and TERCEIROS.search(nome)) or ARQ_FORA.search(nome):
        return "nome que a esteira barra"
    if e not in TXT:
        return "formato que a esteira não leva (%s): a cadeia da v411 o tiraria do topo do repositório" % (e or "sem extensão")
    txt = raw.decode("utf-8", "replace")
    n_cred, pii = GP.avaliar_texto(txt)
    if n_cred or pii:
        return "a guarda pública barra (credencial ou dado pessoal)"
    t2, _c = mascarar(txt)
    if e == ".md":
        t2, _n = filtrar_markdown(t2)
    if GP.toca_escritorio(t2):
        return "toca o acervo do Escritório"
    if t2.encode("utf-8") != raw:
        return "a máscara ou o filtro mudariam os bytes"
    return None


# 0) o manifesto, o resultado e a ordem
mb = MANIF.read_bytes()
if sha(mb) != MANIF_SHA:
    parar("o manifesto do resultado mudou: %s" % sha(mb))
M = json.loads(mb.decode("utf-8"))
if M.get("aberto") is not True or M.get("n_arquivos") != len(M["arquivos"]) or M["resultado"]["sha256"] != RES_SHA:
    parar("manifesto sem aberto=true, com contagem errada ou com outro resultado")
if M["pre_registro_publico"]["commit"] != PRE:
    parar("o manifesto aponta outro commit de pré-registro")
if not any(a["caminho"] == RES_CAM and a["sha256"] == RES_SHA for a in M["arquivos"]):
    parar("o resultado não está na lista do manifesto")

# 1) o preparo: limpo, igual ao remoto, no commit do pré-registro
if (D / ".git" / "index.lock").exists():
    parar("index.lock presente")
if g("status", "--porcelain", "--untracked-files=all").stdout.strip():
    parar("o preparo do work não está limpo")
g("fetch", "-q", "origin")
head0 = g("rev-parse", "HEAD").stdout.strip()
if head0 != g("rev-parse", "origin/main").stdout.strip() or head0 != PRE:
    parar("HEAD/origin não são o commit do pré-registro (%s)" % head0[:12])

# 2) a lista: o manifesto do resultado, o próprio manifesto, os extras da custódia
lista = [(a["caminho"], a["bytes"], a["sha256"]) for a in M["arquivos"]]
lista.append(("work/h0dn_bg1_v411_emenda_11nov/" + MANIF.name, len(mb), MANIF_SHA))
for x in EXTRAS:
    b = (AQUI / x).read_bytes()
    lista.append(("work/pre_registro_h0dn_publicacao_12nov/" + x, len(b), sha(b)))
IP = D / "INDICE_PUBLICO.json"
idx_raw = IP.read_bytes()
idx = json.loads(idx_raw.decode("utf-8"))
pos = {a["caminho"]: a for a in idx["arquivos"]}
plano = {"novo": [], "ja_publicado": [], "fora": []}
for cam, nb, s in lista:
    if not cam.startswith("work/"):
        parar("caminho fora de work/: %s" % cam)
    rel = cam[len("work/"):]
    if rel in JA_INTOCAVEIS:
        parar("a lista toca um arquivo do pré-registro já publicado: %s" % rel)
    raw = open(lp(CEN / cam), "rb").read()
    if len(raw) != nb or sha(raw) != s:
        parar("o arquivo mudou depois do manifesto: %s" % cam)
    m = guarda(cam, rel, raw)
    if m:
        if cam == RES_CAM:
            parar("o RESULTADO não passa na guarda (%s): nada se publica; avisar a gerência c1" % m)
        plano["fora"].append({"caminho": cam, "sha256": s, "motivo": m})
        continue
    ant = pos.get(rel)
    if ant is not None:
        q = D / rel
        if ant["sha256"] != s or not os.path.isfile(lp(q)) or sha(open(lp(q), "rb").read()) != s:
            parar("já está no índice com outros bytes: %s" % rel)
        plano["ja_publicado"].append(cam)
    else:
        plano["novo"].append((cam, rel, raw))
print("manifesto do resultado %s + o manifesto de antes + %d extras: %d arquivos | novos %d | já publicados %d | fora %d" % (
    MANIF_SHA[:16], len(EXTRAS), len(lista), len(plano["novo"]), len(plano["ja_publicado"]), len(plano["fora"])))
for c, _r, raw in plano["novo"]:
    print("  novo: %s (%d B)" % (c, len(raw)))
for x in plano["fora"]:
    print("  fora: %s — %s" % (x["caminho"], x["motivo"]))
if RES_CAM not in {c for c, _r, _w in plano["novo"]}:
    parar("o resultado não está entre os novos")
if not APLICAR:
    print("MODO SECO (nada gravado)")
    sys.exit(0)

# 3) grava no preparo e acrescenta ao índice
bk = D.parent / ("_backup_indice_work_%s_resultado_fora_da_cadeia.json" % STAMP)
with open(bk, "wb") as fh:
    fh.write(idx_raw)
if bk.read_bytes() != idx_raw:
    parar("o backup do índice não confere")
for cam, rel, raw in plano["novo"]:
    q = D / rel
    os.makedirs(lp(q.parent), exist_ok=True)
    t = Path(str(q) + ".tmp_fora")
    with open(lp(t), "wb") as fh:
        fh.write(raw)
    os.replace(lp(t), lp(q))
    if sha(open(lp(q), "rb").read()) != sha(raw):
        parar("o arquivo gravado não confere: %s" % rel)
    idx["arquivos"].append({"caminho": rel, "bytes": len(raw), "sha256": sha(raw)})
agora = time.strftime("%Y-%m-%d %H:%M:%S")
idx["n_arquivos"] = len(idx["arquivos"])
idx.setdefault("atualizacoes", []).append({"em": agora, "motivo": "publicação fora da cadeia (12/11/2026): o resultado da abertura do teste "
                                           "H0DN × BG1 (emenda v411), pelo manifesto da gerência c1 (sha256 %s)" % MANIF_SHA,
                                           "adicionados": len(plano["novo"]), "atualizados": 0, "removidos": 0})
nbx = json.dumps(idx, ensure_ascii=False).encode("utf-8")
t = IP.with_name(IP.name + ".tmp_fora")
t.write_bytes(nbx)
if t.stat().st_size != len(nbx) or len(nbx) <= len(idx_raw):
    parar("o índice novo não cresceu como devia")
os.replace(t, IP)
print("preparo: %d arquivos gravados; índice %d -> %d entradas (backup %s)" % (len(plano["novo"]), len(pos), idx["n_arquivos"], bk.name))


def passo(args, ok_txt=None):
    t0 = time.time()
    r = subprocess.run([PY, "-X", "utf8"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    ult = [l for l in (r.stdout or "").splitlines() if l.strip()]
    print("  [%s] rc=%d %.0f s | %s" % (Path(args[0]).name, r.returncode, time.time() - t0, (ult[-1] if ult else "")[:500]))
    if r.returncode != 0 or (ok_txt and ok_txt not in (r.stdout or "")):
        print((r.stdout or "")[-3000:], (r.stderr or "")[-2000:])
        parar("o passo %s falhou (o preparo fica como está; o backup do índice está em %s)" % (Path(args[0]).name, bk))
    return r.stdout


# 4) as partes do índice e a conferência do delta (os scripts da cadeia, sem mudança)
passo([str(W / "indice_partes.py"), str(D)])
passo([str(W / "conferir_delta.py"), str(D), "regiao"], "APROVADO")

# 5) o atualizar_repo_publico.py, com o add só do que difere do HEAD (retomar_publicacao_12nov.py)
idx_mt = IP.stat().st_mtime
dconf = W / ("varredura_conferencia_delta_%s.json" % D.name)
dj = json.loads(dconf.read_text(encoding="utf-8"))
if not (dconf.stat().st_mtime > idx_mt and dj.get("aprovado") is True):
    parar("a conferência do delta não é mais nova que o índice ou não está aprovada")
COBERTO = set(dj.get("delta_conferido") or [])
_todas = idx["arquivos"]
idxc = [a["caminho"] for a in _todas if not a.get("igual_a")]
if len(idxc) != len(_todas):
    parar("há cópias referenciadas no índice (não esperadas antes da v411)")
_env_ci = {k: v for k, v in os.environ.items() if k != "GIT_LITERAL_PATHSPECS"}
if subprocess.run(["git", "-C", str(D), "check-ignore", "-q", "INDICE_PUBLICO.json"], capture_output=True, env=_env_ci).returncode != 0:
    parar("o índice inteiro não está fora do git")
cab_p = json.loads((D / "INDICE_PUBLICO_PARTES" / "PARTES.json").read_text(encoding="utf-8"))
if cab_p.get("entradas") != len(_todas):
    parar("PARTES.json não tem as entradas do índice")
pts = ["INDICE_PUBLICO_PARTES/PARTES.json"] + [p["arquivo"] for p in cab_p["partes"]]
raiz = [n for n in RAIZ_GERADA if (D / n).is_file() and n != "INDICE_PUBLICO.json"] + pts
quer = set(idxc) | set(raiz)
tem = set(x for x in g("ls-files", "-z").stdout.split("\0") if x)
if tem - quer:
    parar("há rastreados fora do índice: %s" % sorted(tem - quer)[:5])
mudados = {e[3:] for e in g("status", "--porcelain", "-z", "--untracked-files=all").stdout.split("\0") if len(e) > 3}
add = sorted((quer - tem) | (mudados & quer))
esperados = {r for _c, r, _w in plano["novo"]}
if set(add) - COBERTO:
    parar("caminho no add sem conferência: %s" % sorted(set(add) - COBERTO)[:8])
if not esperados <= set(add) or set(add) - esperados - set(pts) or mudados - quer:
    parar("o add não é o esperado: faltam %s; sobram %s; fora do índice %s" % (
        sorted(esperados - set(add))[:5], sorted(set(add) - esperados - set(pts))[:5], sorted(mudados - quer)[:5]))
lf = D / ".git" / "incr_add_delta.txt"
lf.write_bytes(b"\0".join(x.encode("utf-8") for x in add))
g("add", "-f", "--pathspec-from-file=" + str(lf), "--pathspec-file-nul")
st = g("diff", "--cached", "--name-status").stdout.splitlines()
n_a = sum(1 for l in st if l.startswith("A")); n_m = sum(1 for l in st if l.startswith("M")); n_d = sum(1 for l in st if l.startswith("D"))
entra = {x for x in g("diff", "--cached", "--name-only", "-z", "--diff-filter=AM").stdout.split("\0") if x}
if (entra - COBERTO) or n_d or entra != set(add):
    g("reset", "-q")
    parar("o stage não é o conferido — nada publicado")
print("%s: no stage A %d / M %d / D %d" % (NOME, n_a, n_m, n_d))
TIT = ("Resultado da abertura do teste H0DN × BG1 (emenda v411), publicado depois da abertura (12/11/2026)\n\n"
       "%s Publicação fora da cadeia, pedida pela gerência c1: os bytes do resultado da abertura única de 12/11/2026 (início 10:46:34Z, "
       "depois do pré-registro público no commit %s), o pré-voo, o recibo da abertura e a ordem do operador, pelo manifesto "
       "MANIFESTO_DA_PUBLICACAO_DO_RESULTADO_12nov.json (sha256 %s); o manifesto do pré-registro; os scripts e recibos da publicação. "
       "O texto final, os pinos de produção e o vetor do pré-registro não foram tocados. Fora: %d arquivo(s), ditos no recibo. "
       "Esta mensagem não apresenta o resultado: a leitura vai com a linha das Cefeidas livres e as ressalvas da seção 8 do pré-registro. "
       "O README não foi regerado; o DESDE da próxima cadeia ignora este commit." % (MARCA, PRE, MANIF_SHA, len(plano["fora"])))
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
h = g("rev-parse", "HEAD").stdout.strip()
g("fetch", "-q", "origin")
rem = g("rev-parse", "origin/main").stdout.strip()
arv = [x for x in g("ls-tree", "-r", "-z", "--name-only", "origin/main").stdout.split("\0") if x]
print("%s: HEAD %s = origin/main %s | árvore remota %d arquivos (índice %d + raiz %d) | push %.0f s" % (
    NOME, h[:8], rem[:8], len(arv), len(idxc), len(raiz), time.time() - t0))
if not (h == rem and set(arv) == quer and h != head0):
    parar("a árvore remota não é o índice ou o commit não chegou")
print("PUBLICADO E CONFERIDO")

# 6) o commit, a data e a conferência pelo raw
ci = g("log", "-1", "--format=%cI", h).stdout.strip()
tocados = [l.split("\t") for l in g("show", "--name-status", "--format=", h).stdout.splitlines() if l.strip()]
outros = sorted(x[-1] for x in tocados if not (x[0] == "A" and x[1] in esperados) and not x[-1].startswith("INDICE_PUBLICO_PARTES/"))
if outros or not esperados <= {x[1] for x in tocados if x[0] == "A"}:
    parar("o commit tocou além do esperado: %s" % outros[:10])
raw_ok, raw_falha, raw_sha = 0, [], {}
for cam, rel, raw in plano["novo"]:
    url = "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, h, urllib.parse.quote(rel))
    try:
        b = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "iald-custodia"}), timeout=60).read()
    except Exception as ex:  # noqa: BLE001
        raw_falha.append((rel, "erro: %s" % ex)); continue
    raw_sha[rel] = sha(b)
    if sha(b) == sha(raw) and len(b) == len(raw):
        raw_ok += 1
    else:
        raw_falha.append((rel, "sha256 %s" % sha(b)))
rel_res = RES_CAM[len("work/"):]
gh = {}
for nome, args in (("commit", ["api", "repos/%s/commits/%s" % (REPO, h), "--jq", "{sha: .sha, committer_date: .commit.committer.date, html_url: .html_url}"]),
                   ("push", ["api", "repos/%s/activity?per_page=3" % REPO, "--jq", "[.[] | {after, timestamp, activity_type, ref}]"])):
    rr = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    gh[nome] = json.loads(rr.stdout) if rr.returncode == 0 and rr.stdout.strip() else {"erro": (rr.stderr or "")[-300:]}
recibo = {"o_que_e": "recibo da publicação fora da cadeia do RESULTADO da abertura do teste H0DN × BG1 (emenda v411)",
          "quem": "claude-site-custodia", "quando": time.strftime("%Y-%m-%d %H:%M:%S"), "repositorio": "https://github.com/%s" % REPO,
          "commit": h, "commit_anterior": head0, "commit_data_local": ci, "github": gh,
          "manifesto": {"caminho": str(MANIF), "sha256": MANIF_SHA},
          "resultado": {"caminho": rel_res, "sha256_esperado": RES_SHA, "sha256_raw": raw_sha.get(rel_res),
                        "url": "https://raw.githubusercontent.com/%s/%s/%s" % (REPO, h, urllib.parse.quote(rel_res))},
          "novos": [{"caminho": r, "sha256": sha(w), "sha256_raw": raw_sha.get(r)} for _c, r, w in plano["novo"]],
          "ja_publicados": plano["ja_publicado"], "fora": plano["fora"], "stage": {"A": n_a, "M": n_m, "D": n_d},
          "raw_conferidos": raw_ok, "raw_falhas": raw_falha, "backup_do_indice": str(bk)}
rp = AQUI / ("RECIBO_PUBLICACAO_RESULTADO_%s.json" % STAMP)
rp.write_text(json.dumps(recibo, ensure_ascii=False, indent=1), encoding="utf-8")
print("commit %s (%s) | raw: %d/%d conferidos, falhas %s | resultado raw %s | recibo %s" % (
    h[:12], ci, raw_ok, len(plano["novo"]), raw_falha[:3], raw_sha.get(rel_res) == RES_SHA, rp.name))
if raw_falha or raw_sha.get(rel_res) != RES_SHA:
    sys.exit(1)

# -*- coding: utf-8 -*-
r"""PUBLICAÇÃO FORA DA CADEIA do pré-registro do teste H0DN × BG1 (emenda v411), ANTES da abertura (12/11/2026, claude-site-custodia).

Pedido da gerência c1 (12/11/2026), por decisão do operador: «publicar o pacote e o pré-registro antes, abrir uma vez sob a sua ordem»
(texto da c1 a que ele respondeu, work\cunhagens_13out\GERENCIA_12nov_objecoes_resolvidas_..., bloco 22:57:13: «gero o texto final, o
literal dos vereditos e os pinos de produção, rodo o ensaio e peço à sessão de custódia a publicação»; resposta, por bytes:
OPERADOR_12nov_concordo_com_tudo_que_vc_sugeriu_prossiga_verbatim.txt).

O que faz: leva ao repositório público central-publica-work EXATAMENTE os arquivos do manifesto da c1
(work\h0dn_bg1_v411_emenda_11nov\MANIFESTO_DA_PUBLICACAO_12nov.json, sha256 conferido), com os MESMOS bytes, pela mesma guarda da
esteira da região, sem a rodada inteira:
  - cada arquivo confere com o manifesto (bytes e sha256); o resultado da abertura NÃO pode existir (se existir, PARA);
  - backup de sessão (.bak_) fica fora, pela regra da esteira (ditos no recibo);
  - texto: guarda pública (credencial, dado pessoal, Escritório), máscara e filtro das notas; se a máscara ou o filtro mudassem um byte,
    o arquivo público não teria o sha256 do manifesto: PARA;
  - .npz (resultado da casa em formato zip; a esteira de texto não os leva): os bytes do manifesto; a conferência independente
    (conferir_preparos.py) varre cada membro do zip; aqui só se lê a lista dos membros (nenhum valor);
  - grava no preparo e acrescenta as linhas ao FIM do índice (só a última parte do índice muda), refaz as partes (indice_partes.py),
    roda a conferência independente do delta (conferir_delta.py) e publica (atualizar_repo_publico.py: um commit, push sem força);
  - o commit leva a marca [FORA_DA_CADEIA], que rodar_incremental.py ignora ao calcular o DESDE da próxima cadeia;
  - depois do push, confere pelo raw de cada arquivo, no hash do commit, que os bytes públicos têm o sha256 do manifesto.
Não roda nada de codigo\ do teste e não abre o vetor. Sem --aplicar: só mostra o plano."""
import hashlib, json, os, re, subprocess, sys, time, urllib.parse, urllib.request, zipfile
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
REPO = "rotolimiguel-iald/central-publica-work"
PY = r"C:\Python314\python.exe"
MANIF = CEN / "work" / "h0dn_bg1_v411_emenda_11nov" / "MANIFESTO_DA_PUBLICACAO_12nov.json"
MANIF_SHA = "1c91af10c8795057c535a1a686997e15422ec5f99179cc453090804fa2aecb43"
PROIBIDO = CEN / "work" / "h0dn_bg1_v411_emenda_11nov" / "producao" / "RESULTADO_DA_ABERTURA_V411.json"
CHAVES = {"texto_final": "06af740a8812a622a6bc0c7fbd252f4d824c1428c7b0c62e313ccd3ae75199c8",
          "pinos_de_producao": "95adfeea37e1c8f6100876082c1f3e021b3eb2f67f44fecaf403302ab66d9c9d",
          "vetor": "536b07e222e57732dc1075880038d73845e61b0c53eadf9880041576141ff131",
          "literal_dos_vereditos": "47624a41242869708b61ccbd4fc55d6af186846da1eec81661ccf12013cf4c43"}
MARCA = "[FORA_DA_CADEIA]"
APLICAR = "--aplicar" in sys.argv
ENV = dict(os.environ, GIT_LITERAL_PATHSPECS="1")
STAMP = time.strftime("%Y%m%d_%H%M%S")

# as regras de nome e de formato da esteira da região, lidas do PRÓPRIO construtor (sem cópia que possa divergir)
_src = (W / "construir_regiao_incremental.py").read_text(encoding="utf-8")
_i, _j = _src.index("TXT = {"), _src.index("LIM_TXT = ")
_ns = {"re": re}
exec(compile(_src[_i:_src.index("\n", _j)], "construir_regiao_incremental.py (regras)", "exec"), _ns)
TXT, PASTA_FORA, FUNDA_FORA, ARQ_FORA, EXCL_DIR = _ns["TXT"], _ns["PASTA_FORA"], _ns["FUNDA_FORA"], _ns["ARQ_FORA"], _ns["EXCL_DIR"]


def parar(msg):
    raise SystemExit("PARAR: " + msg)


def git(*a, ok=True):
    r = subprocess.run(["git", "-C", str(D)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", env=ENV)
    if ok and r.returncode != 0:
        parar("git %s: %s" % (" ".join(a[:3]), (r.stderr or r.stdout)[-600:]))
    return r


def lp(p):
    p = str(Path(p).resolve())
    return p if p.startswith("\\\\?\\") else "\\\\?\\" + p


def sha(b):
    return hashlib.sha256(b).hexdigest()


# 0) o que não pode existir, o manifesto e as chaves
if PROIBIDO.exists():
    parar("o resultado da abertura existe: %s — nada se publica; avisar a gerência c1" % PROIBIDO)
mb = MANIF.read_bytes()
if sha(mb) != MANIF_SHA:
    parar("o manifesto mudou: %s" % sha(mb))
M = json.loads(mb.decode("utf-8"))
if M.get("nada_aberto") is not True or M.get("n_arquivos") != len(M["arquivos"]):
    parar("manifesto sem nada_aberto ou com contagem errada")
for k, s in CHAVES.items():
    if M["chaves"][k]["sha256"] != s:
        parar("a chave %s do manifesto não é a do pedido" % k)
if any("RESULTADO_DA_ABERTURA" in a["caminho"] for a in M["arquivos"]):
    parar("o manifesto lista um resultado da abertura")

# 1) o preparo: limpo e igual ao remoto
if git("status", "--porcelain", "--untracked-files=all").stdout.strip():
    parar("o preparo do work não está limpo")
git("fetch", "-q", "origin")
head0 = git("rev-parse", "HEAD").stdout.strip()
if head0 != git("rev-parse", "origin/main").stdout.strip():
    parar("HEAD != origin/main")

# 2) cada arquivo do manifesto
IP = D / "INDICE_PUBLICO.json"
idx_raw = IP.read_bytes()
idx = json.loads(idx_raw.decode("utf-8"))
pos = {a["caminho"]: a for a in idx["arquivos"]}
plano = {"novo": [], "ja_publicado": [], "fora": []}
membros_npz = {}
for a in M["arquivos"]:
    cam = a["caminho"]
    if not cam.startswith("work/"):
        parar("caminho fora de work/: %s" % cam)
    rel = cam[len("work/"):]
    p = CEN / cam
    raw = open(lp(p), "rb").read()
    if len(raw) != a["bytes"] or sha(raw) != a["sha256"]:
        parar("o arquivo mudou depois do manifesto: %s" % cam)
    partes = rel.split("/")
    nome = partes[-1]
    e = Path(nome).suffix.lower()
    if ".bak_" in nome:
        plano["fora"].append({"caminho": cam, "motivo": "backup de sessão (.bak_): a esteira não publica backups; a versão vigente está no manifesto"})
        continue
    if PASTA_FORA.search(partes[0]) or any(FUNDA_FORA.match(x) or x in EXCL_DIR for x in partes[1:-1]):
        parar("pasta que a esteira barra: %s" % cam)
    if GP.arquivo_de_credencial(nome) or (TERCEIROS is not None and TERCEIROS.search(nome)) or ARQ_FORA.search(nome):
        parar("nome que a esteira barra: %s" % cam)
    if e in TXT:
        txt = raw.decode("utf-8", "replace")
        n_cred, pii = GP.avaliar_texto(txt)
        if n_cred or pii:
            parar("a guarda pública barra (credencial ou dado pessoal): %s" % cam)
        t2, _c = mascarar(txt)
        if e == ".md":
            t2, _n = filtrar_markdown(t2)
        if GP.toca_escritorio(t2):
            parar("toca o acervo do Escritório: %s" % cam)
        if t2.encode("utf-8") != raw:
            parar("a máscara ou o filtro mudariam os bytes (o público não teria o sha256 do manifesto): %s" % cam)
    elif e == ".npz":
        if raw[:2] != b"PK":
            parar(".npz que não é zip: %s" % cam)
        nomes = zipfile.ZipFile(p).namelist()
        if not nomes or not all(n.endswith(".npy") and "/" not in n for n in nomes):
            parar(".npz com membro que não é .npy: %s %s" % (cam, nomes))
        membros_npz[cam] = nomes
    else:
        parar("formato que esta publicação não leva: %s" % cam)
    ant = pos.get(rel)
    if ant is not None:
        q = D / rel
        if ant["sha256"] != a["sha256"] or not os.path.isfile(lp(q)) or sha(open(lp(q), "rb").read()) != a["sha256"]:
            parar("já está no índice com outros bytes: %s" % rel)
        plano["ja_publicado"].append(cam)
    else:
        plano["novo"].append((cam, rel, raw))

print("manifesto %s: %d arquivos | novos %d | já publicados com os mesmos bytes %d | fora %d" % (
    MANIF_SHA[:16], len(M["arquivos"]), len(plano["novo"]), len(plano["ja_publicado"]), len(plano["fora"])))
for x in plano["fora"]:
    print("  fora:", x["caminho"])
for k, v in membros_npz.items():
    print("  npz:", k, v)
if not APLICAR:
    print("MODO SECO (nada gravado)")
    sys.exit(0)

# 3) grava no preparo e acrescenta ao índice
bk = D.parent / ("_backup_indice_work_%s_fora_da_cadeia.json" % STAMP)
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
idx.setdefault("atualizacoes", []).append({"em": agora, "motivo": "publicação fora da cadeia (12/11/2026): o pré-registro do teste H0DN × BG1 "
                                           "(emenda v411) antes da abertura, pelo manifesto da gerência c1 (sha256 %s)" % MANIF_SHA,
                                           "adicionados": len(plano["novo"]), "atualizados": 0, "removidos": 0})
nb = json.dumps(idx, ensure_ascii=False).encode("utf-8")
t = IP.with_name(IP.name + ".tmp_fora")
t.write_bytes(nb)
if t.stat().st_size != len(nb) or len(nb) <= len(idx_raw):
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


# 4) as partes do índice, a conferência do delta e a publicação (os scripts da cadeia, sem mudança)
passo([str(W / "indice_partes.py"), str(D)])
passo([str(W / "conferir_delta.py"), str(D), "regiao"], "APROVADO")
TIT = ("Pré-registro do teste H0DN × BG1 (emenda v411), publicado antes da abertura (12/11/2026)\n\n"
       "%s Publicação fora da cadeia, pedida pela gerência c1 por decisão do operador de 11 e 12/11/2026: o texto final do pré-registro "
       "(EMENDA_E_PRE_REGISTRO_V411.md), os pinos de produção, o vetor pinado e o literal dos vereditos, com o pacote da emenda, pelo "
       "manifesto MANIFESTO_DA_PUBLICACAO_12nov.json (sha256 %s). Nada foi aberto: o resultado da abertura não existe.\n"
       "Os %d backups de sessão (.bak_) do manifesto ficam fora, pela regra da esteira; os %d .npz entram com os bytes do manifesto "
       "(resultado da casa em formato zip, varrido por dentro pela conferência independente). Os %d arquivos do manifesto já publicados "
       "na v410 seguem com os mesmos bytes. O README não foi regerado (as contagens são as da cadeia de 11/11/2026); a próxima cadeia o "
       "regera, e o DESDE dela ignora este commit." % (MARCA, MANIF_SHA, len(plano["fora"]), len(membros_npz), len(plano["ja_publicado"])))
saida = passo([str(W / "atualizar_repo_publico.py"), "central-publica-work", str(D), TIT], "PUBLICADO E CONFERIDO")

# 5) o commit, a data e a conferência pelo raw
h = git("rev-parse", "HEAD").stdout.strip()
if git("rev-parse", "origin/main").stdout.strip() != h or h == head0:
    parar("o commit não chegou ao remoto")
ci = git("log", "-1", "--format=%cI", h).stdout.strip()
tocados = [l.split("\t") for l in git("show", "--name-status", "--format=", h).stdout.splitlines() if l.strip()]
esperados = {rel for _c, rel, _r in plano["novo"]}
add = {x[1] for x in tocados if x[0] == "A"}
outros = sorted(x[-1] for x in tocados if not (x[0] == "A" and x[1] in esperados) and not x[-1].startswith("INDICE_PUBLICO_PARTES/"))
if add - esperados - {x for x in add if x.startswith("INDICE_PUBLICO_PARTES/")} or not esperados <= add or outros:
    parar("o commit tocou além do esperado: %s" % outros[:10])
arv = set(x for x in git("ls-tree", "-r", "-z", "--name-only", h).stdout.split("\0") if x)
if any("RESULTADO_DA_ABERTURA" in x for x in arv):
    parar("a árvore publicada traz um resultado da abertura")
publicados = [c for c in M["arquivos"] if ".bak_" not in c["caminho"]]
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
    chaves_raw[k] = {"caminho": rel, "url": url, "sha256_esperado": c["sha256"],
                     "sha256_raw": sha(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "iald-custodia"}), timeout=60).read())}
    chaves_raw[k]["confere"] = chaves_raw[k]["sha256_raw"] == c["sha256"]
gh = {}
for nome, args in (("commit", ["api", "repos/%s/commits/%s" % (REPO, h), "--jq", "{sha: .sha, committer_date: .commit.committer.date, html_url: .html_url}"]),
                   ("push", ["api", "repos/%s/activity?per_page=3" % REPO, "--jq", "[.[] | {after, timestamp, activity_type, ref}]"])):
    r = subprocess.run(["gh"] + args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    gh[nome] = json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else {"erro": (r.stderr or "")[-300:]}
recibo = {"o_que_e": "recibo da publicação fora da cadeia do pré-registro H0DN × BG1 (emenda v411), antes da abertura",
          "quem": "claude-site-custodia", "quando": agora, "repositorio": "https://github.com/%s" % REPO,
          "commit": h, "commit_data_local": ci, "github": gh, "manifesto": {"caminho": str(MANIF), "sha256": MANIF_SHA},
          "novos": len(plano["novo"]), "ja_publicados_mesmos_bytes": plano["ja_publicado"], "fora": plano["fora"],
          "npz_membros": membros_npz, "raw_conferidos": raw_ok, "raw_falhas": raw_falha, "chaves_raw": chaves_raw,
          "nada_aberto": not PROIBIDO.exists(), "backup_do_indice": str(bk), "saida_publicacao": (saida or "")[-1500:]}
rp = AQUI / ("RECIBO_PUBLICACAO_%s.json" % STAMP)
rp.write_text(json.dumps(recibo, ensure_ascii=False, indent=1), encoding="utf-8")
print("commit %s (%s) | raw: %d/%d conferidos, falhas %s | chaves: %s | recibo %s" % (
    h[:12], ci, raw_ok, len(publicados), raw_falha[:3], {k: v["confere"] for k, v in chaves_raw.items()}, rp.name))
if raw_falha or not all(v["confere"] for v in chaves_raw.values()):
    sys.exit(1)

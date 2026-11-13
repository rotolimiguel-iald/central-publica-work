# -*- coding: utf-8 -*-
"""Teste das duas erratas de 12/11/2026 (claude-site-custodia), num preparo sintético com remoto local (fora da Central):
A. atualizar_repo_publico.py com o add só do que difere do HEAD. O stage e a árvore remota têm de ser os mesmos do add do índice inteiro:
   arquivo novo comum; arquivo novo que o .gitignore copiado barraria (o -f); rastreado mudado; rastreado igual; arquivo que saiu do
   índice (git rm --cached); nome com espaço, colchete e parênteses (pathspec literal; o asterisco não é nome válido no Windows); nada mudou (nada a publicar); a cópia referenciada.
B. mesclar_incremento.py: o já publicado que a rodada exclui só pelo formato fica se os bytes da origem e do preparo têm o sha256 do índice;
   sai se a origem mudou, se o preparo diverge ou se o motivo é outro (dado pessoal). A origem do tipo work é a pasta work real da Central:
   o teste só LÊ quatro arquivos dela e grava só no preparo temporário e nas listas de teste ao lado da esteira (apagadas no fim).
Uso: testar_add_delta_e_formato.py"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
CEN = Path(r"C:\IALD\Central de Patentes")
PY = r"C:\Python314\python.exe"
NOME = "teste_add_delta_preparo"
falhas = []
GER = [W / ("varredura_exclusoes_%s.json" % NOME), W / ("git_add_%s.txt" % NOME), W / ("git_rm_%s.txt" % NOME)]
for x in GER:
    assert not x.exists(), "arquivo de teste já existe — PARAR: %s" % x


def confere(cond, rotulo):
    print(("  ok   " if cond else "  FALHA ") + rotulo)
    if not cond:
        falhas.append(rotulo)


def git(d, *a):
    return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def _rm_ro(func, path, exc):
    os.chmod(path, 0o700); func(path)


def escrever(d, rel, b):
    (d / rel).parent.mkdir(parents=True, exist_ok=True)
    (d / rel).write_bytes(b)


def gravar_indice(d, arqs, extra=None):
    ent = [{"caminho": r, "bytes": len(b), "sha256": sha(b)} for r, b in arqs.items()]
    ent += extra or []
    (d / "INDICE_PUBLICO.json").write_text(json.dumps({"regiao": "teste", "n_arquivos": len(ent), "arquivos": sorted(ent, key=lambda x: x["caminho"])},
                                                      ensure_ascii=False), encoding="utf-8")


def aprovar(d):
    # a conferência completa «aprovada», mais nova que o índice (o publicador só exige o relatório; aqui o teste é do add, não do conferidor)
    (W / ("varredura_conferencia_%s.json" % d.name)).write_text(json.dumps({"aprovado": True, "contagem": "teste"}), encoding="utf-8")


def publicar(d, tit):
    aprovar(d)
    return subprocess.run([PY, "-X", "utf8", str(W / "atualizar_repo_publico.py"), "central-publica", str(d), tit],
                          capture_output=True, text=True, encoding="utf-8", errors="replace")


base = Path(tempfile.mkdtemp(prefix="teste_add_delta_"))
d, nu, clone = base / NOME, base / "remoto.git", base / "clone"
try:
    print("A. o add só do que difere")
    d.mkdir()
    git(base, "init", "-q", "--bare", "-b", "main", str(nu))
    git(d, "init", "-q", "-b", "main"); git(d, "config", "user.email", "teste.invalid"); git(d, "config", "user.name", "teste")
    git(d, "remote", "add", "origin", str(nu))
    A0 = {"dados/igual.txt": b"igual\n", "dados/muda.txt": b"antes\n", "dados/sai.txt": b"vai sair\n", "dados/b.txt": b"copia\n"}
    for rel, b in A0.items():
        escrever(d, rel, b)
    escrever(d, ".gitattributes", b"* -text\n")
    escrever(d, ".gitignore", b"*.log\nignorada/\n")
    gravar_indice(d, A0)
    git(d, "add", "-A"); git(d, "commit", "-q", "-m", "estado publicado"); git(d, "push", "-q", "origin", "main")
    # a rodada: um novo comum, dois novos que o .gitignore barraria, um mudado, um que sai, nomes difíceis, uma cópia referenciada
    A1 = {"dados/igual.txt": b"igual\n", "dados/muda.txt": b"depois\n", "dados/novo.txt": b"novo\n", "dados/curado.log": b"log curado\n",
          "ignorada/dentro.txt": b"curado na pasta ignorada\n", "dados/nome com espaco [1] (x).txt": b"literal\n", "dados/a.txt": b"copia\n"}
    for rel, b in A1.items():
        escrever(d, rel, b)
    os.remove(d / "dados/sai.txt")
    os.remove(d / "dados/b.txt")
    escrever(d, "RECONSTRUIR_COPIAS.py", b"print('teste')\n")
    escrever(d, "fora_do_indice.txt", b"nao entra\n")      # não está no índice: fica fora do stage (o publicador diz e não leva)
    gravar_indice(d, A1, extra=[{"caminho": "dados/b.txt", "bytes": 6, "sha256": sha(b"copia\n"), "igual_a": "dados/a.txt"}])
    r = publicar(d, "teste: add do delta")
    confere(r.returncode == 0 and "PUBLICADO E CONFERIDO" in r.stdout, "publicador: %s" % ((r.stdout.strip().splitlines() or [""])[-1][:150] + (r.stderr[-400:] if r.returncode else "")))
    lst = (d / ".git" / "incr_add.txt").read_bytes().split(b"\0")
    confere(sorted(x.decode() for x in lst if x) == sorted(["dados/muda.txt", "dados/novo.txt", "dados/curado.log", "ignorada/dentro.txt",
                                                            "dados/nome com espaco [1] (x).txt", "dados/a.txt", "INDICE_PUBLICO.json", "RECONSTRUIR_COPIAS.py"]),
            "a lista do add é só o que difere (%d caminhos)" % len([x for x in lst if x]))
    arv = set(git(d, "ls-tree", "-r", "--name-only", "-z", "origin/main").stdout.split("\0")) - {""}
    quer = set(A1) | {"INDICE_PUBLICO.json", ".gitattributes", "RECONSTRUIR_COPIAS.py"}
    confere(arv == quer, "árvore remota = índice + raiz (sem sai.txt, sem a cópia b.txt, sem fora_do_indice.txt; com os barrados pelo .gitignore)")
    git(base, "clone", "-q", str(nu), str(clone))
    confere(all((clone / k).read_bytes() == v for k, v in A1.items()), "o clone tem os bytes de cada arquivo do índice")
    confere("fora do stage" in r.stdout, "o que está fora do índice é dito, não levado")
    head1 = git(d, "rev-parse", "HEAD").stdout.strip()
    r2 = publicar(d, "teste: nada mudou")
    confere(r2.returncode == 0 and "nada a publicar" in r2.stdout and git(d, "rev-parse", "HEAD").stdout.strip() == head1,
            "segunda publicação sem mudança: nada a publicar, nenhum commit")
    escrever(d, "dados/igual.txt", b"igual, agora mudado\n")
    gravar_indice(d, {**A1, "dados/igual.txt": b"igual, agora mudado\n"}, extra=[{"caminho": "dados/b.txt", "bytes": 6, "sha256": sha(b"copia\n"), "igual_a": "dados/a.txt"}])
    r3 = publicar(d, "teste: um só mudado")
    st3 = git(d, "show", "--name-status", "--format=", "HEAD").stdout.split("\n")
    confere(r3.returncode == 0 and sorted(x for x in st3 if x) == ["M\tINDICE_PUBLICO.json", "M\tdados/igual.txt"], "um só mudado: o commit leva ele e o índice (%s)" % [x for x in st3 if x])

    print("B. o mesclar e a exclusão só pelo formato")
    WK = CEN / "work"
    R_FICA = "astra_bell_fock_tt_05nov/h0dn_bg1_06nov/network/network.npz"
    R_ORIGEM_MUDOU = "astra_bell_fock_tt_05nov/h0dn_bg1_06nov/estimator_frozen.npz"
    R_PREPARO_DIVERGE = "h0dn_bg1_v411_emenda_11nov/artefatos/estimador_s0_v411.npz"
    R_OUTRO_MOTIVO = "cunhagens_13out/OPERADOR_12nov_otimo_vamos_rodar_tudo_pode_abrir_chegou_a_hora_da_v411_verbatim.txt"
    dm = base / "mescla" / NOME
    tm = base / "rodada" / ("_incr_teste_%s" % NOME)
    dm.mkdir(parents=True); tm.mkdir(parents=True)
    org = {r: (WK / r).read_bytes() for r in (R_FICA, R_ORIGEM_MUDOU, R_PREPARO_DIVERGE, R_OUTRO_MOTIVO)}
    ent = []
    for r, b in org.items():
        escrever(dm, r, b if r != R_PREPARO_DIVERGE else b + b"x")
        ent.append({"caminho": r, "bytes": len(b), "sha256": sha(b) if r != R_ORIGEM_MUDOU else sha(b + b"publicado antes")})
    (dm / "INDICE_PUBLICO.json").write_text(json.dumps({"regiao": "teste", "n_arquivos": len(ent), "arquivos": ent}, ensure_ascii=False), encoding="utf-8")
    (dm / "EXCLUSOES_PUBLICAS.json").write_text(json.dumps({"por_motivo": {}}), encoding="utf-8")
    (tm / "INDICE_PUBLICO.json").write_text(json.dumps({"regiao": "teste", "n_arquivos": 0, "arquivos": []}), encoding="utf-8")
    TL = W / ("varredura_exclusoes_%s.json" % tm.name)
    GER.append(TL)
    TL.write_text(json.dumps({"binário de cache ou outro formato (índice apenas)": [R_FICA, R_ORIGEM_MUDOU, R_PREPARO_DIVERGE],
                              "conversa, usuários ou varredura de dado pessoal": [R_OUTRO_MOTIVO]}, ensure_ascii=False), encoding="utf-8")
    rm_ = subprocess.run([PY, "-X", "utf8", str(W / "mesclar_incremento.py"), "mesclar", str(dm), "work", str(tm)],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    confere(rm_.returncode == 0, "mesclar rodou: %s" % (rm_.stdout.strip()[-300:] + rm_.stderr[-400:]))
    idx = {a["caminho"] for a in json.loads((dm / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]}
    confere(R_FICA in idx and (dm / R_FICA).is_file(), "o .npz já publicado com os mesmos bytes fica (índice e preparo)")
    confere(R_ORIGEM_MUDOU not in idx and not (dm / R_ORIGEM_MUDOU).exists(), "a origem mudou: sai")
    confere(R_PREPARO_DIVERGE not in idx and not (dm / R_PREPARO_DIVERGE).exists(), "o preparo diverge do índice: sai")
    confere(R_OUTRO_MOTIVO not in idx and not (dm / R_OUTRO_MOTIVO).exists(), "outro motivo (dado pessoal): sai")
    grm = [x.decode() for x in (W / ("git_rm_%s.txt" % NOME)).read_bytes().split(b"\0") if x]
    confere(sorted(grm) == sorted([R_ORIGEM_MUDOU, R_PREPARO_DIVERGE, R_OUTRO_MOTIVO]), "git_rm leva os três que saem, não o que fica")
    loc = json.loads((W / ("varredura_exclusoes_%s.json" % NOME)).read_text(encoding="utf-8"))
    confere(R_FICA not in {x for v in loc.values() for x in v}, "o que fica não entra na lista local de exclusões")
    confere("mantido (já publicado com os mesmos bytes; só o formato)" in rm_.stdout, "a contagem diz o mantido")
    confere(all((WK / r).read_bytes() == b for r, b in org.items()), "a origem real não foi tocada")
finally:
    for x in GER + list(W.glob("varredura_conferencia_%s*.json" % NOME)):
        if x.exists():
            x.unlink()
    shutil.rmtree(base, onexc=_rm_ro)
print("FALHAS: %d %s" % (len(falhas), falhas) if falhas else "TODOS OS CASOS PASSAM")
sys.exit(1 if falhas else 0)

# -*- coding: utf-8 -*-
"""Teste da CÓPIA QUE VIRA REFERÊNCIA (11/11/2026, claude-site-custodia; decisão do operador, a partir da v411), num preparo sintético com
remoto local (repositório nu numa pasta temporária, fora da Central). Exercita o construtor (copias_referencia.py), a conferência
INDEPENDENTE (conferir_preparos.py, rodada como na cadeia), o publicador (atualizar_repo_publico.py, com push para o remoto local) e o
RECONSTRUIR_COPIAS.py num clone — inclusive com o índice em partes (o clone do work não tem o índice inteiro).
Casos: marcação e original estável; arquivos fixos (raiz, esteira do work) nunca viram referência; idempotência; publicação (as cópias saem
da árvore, o resto fica); clone reconstruído com sha256; cópia nova com caminho menor não troca o original; o original muda de conteúdo
(restaura do HEAD); o original é excluído pela esteira (PARA, nada gravado); o original some da origem (restaura); controles negativos da
conferência (cópia física que ficou, referência para referência, original adulterado, sem o script na raiz).
Os relatórios que a conferência grava ao lado dela e a lista local de exclusões de teste saem no fim. Uso: testar_copias_referencia.py"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import copias_referencia as CR  # noqa: E402
import indice_partes as IP  # noqa: E402

PY = r"C:\Python314\python.exe"
NOME = "teste_copias_preparo"
falhas = []
LOCAL = W / ("varredura_exclusoes_%s.json" % NOME)
assert not LOCAL.exists(), "lista local de exclusões de teste já existe — PARAR: %s" % LOCAL


def confere(cond, rotulo):
    print(("  ok   " if cond else "  FALHA ") + rotulo)
    if not cond:
        falhas.append(rotulo)


def git(d, *a):
    return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def indice(d):
    return json.loads((d / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))


def por(d):
    return {a["caminho"]: a for a in indice(d)["arquivos"]}


def gravar_indice(d, idx):
    (d / "INDICE_PUBLICO.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")


def conferir(d):
    r = subprocess.run([PY, "-X", "utf8", str(W / "conferir_preparos.py"), str(d)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, json.loads((W / ("varredura_conferencia_%s.json" % d.name)).read_text(encoding="utf-8"))


def _rm_ro(func, path, exc):                         # os objetos do git são somente leitura no Windows
    os.chmod(path, 0o700); func(path)


def escrever(d, rel, b):
    (d / rel).parent.mkdir(parents=True, exist_ok=True)
    (d / rel).write_bytes(b)


ARQS = {"dados/a.txt": b"conteudo X\n", "dados/b.txt": b"conteudo X\n", "dados/c/z.txt": b"conteudo X\n", "dados/u.txt": b"unico U\n",
        "README.md": b"# preparo de teste\n", "dados/readme_copia.md": b"# preparo de teste\n",
        "central_publica_22out/s.py": b"print('S')\n", "central_publica_22out/s2.py": b"print('S')\n", "dados/s_copia.py": b"print('S')\n"}

base = Path(tempfile.mkdtemp(prefix="teste_copias_"))
d, nu, clone = base / NOME, base / "remoto.git", base / "clone"
try:
    d.mkdir()
    git(base, "init", "-q", "--bare", "-b", "main", str(nu))
    git(d, "init", "-q", "-b", "main"); git(d, "config", "user.email", "teste.invalid"); git(d, "config", "user.name", "teste")
    git(d, "remote", "add", "origin", str(nu))
    for rel, b in ARQS.items():
        escrever(d, rel, b)
    escrever(d, ".gitattributes", b"* -text\n")      # como nos três repositórios reais: o clone guarda os bytes (sem conversão de fim de linha)
    gravar_indice(d, {"regiao": "teste", "n_arquivos": len(ARQS),
                      "arquivos": sorted(({"caminho": r, "bytes": len(b), "sha256": sha(b)} for r, b in ARQS.items()), key=lambda x: x["caminho"])})
    git(d, "add", "-A"); git(d, "commit", "-q", "-m", "estado publicado: as cópias inteiras na árvore"); git(d, "push", "-q", "origin", "main")
    confere(git(d, "rev-parse", "HEAD").stdout == git(d, "rev-parse", "origin/main").stdout, "antes: HEAD = origin/main, cópias na árvore")

    print("1. marcar as cópias")
    r1 = CR.referenciar(d)
    p = por(d)
    confere(r1["ok"] and r1["referencias"] == 4 and r1["apagados_agora"] == 4, "4 referências, 4 cópias apagadas (%s)" % {k: r1.get(k) for k in ("referencias", "apagados_agora", "grupos_com_copia")})
    confere(p["dados/b.txt"].get("igual_a") == "dados/a.txt" and p["dados/c/z.txt"].get("igual_a") == "dados/a.txt" and "igual_a" not in p["dados/a.txt"],
            "o original é o menor caminho já publicado (dados/a.txt)")
    confere(not (d / "dados/b.txt").exists() and not (d / "dados/c/z.txt").exists() and (d / "dados/a.txt").is_file(), "as cópias saíram do preparo; o original ficou")
    confere("igual_a" not in p["README.md"] and p["dados/readme_copia.md"].get("igual_a") == "README.md", "a raiz gerada nunca vira referência, mas pode ser original")
    confere("igual_a" not in p["central_publica_22out/s.py"] and "igual_a" not in p["central_publica_22out/s2.py"] and (d / "central_publica_22out/s2.py").is_file()
            and p["dados/s_copia.py"].get("igual_a") == "central_publica_22out/s.py", "a esteira do work nunca vira referência (as duas ficam), mas é original")
    confere((d / CR.SCRIPT).read_bytes() == CR.RECONSTRUIR.encode("utf-8"), "RECONSTRUIR_COPIAS.py gravado na raiz")

    print("2. idempotência")
    r2 = CR.referenciar(d)
    confere(r2["ok"] and r2["entradas_mudadas"] == 0 and r2["apagados_agora"] == 0 and r2["restaurados_do_head"] == 0, "a 2ª rodada não muda nada (%s)" % r2["entradas_mudadas"])

    print("3. conferência independente e publicação no remoto local")
    rc, rel = conferir(d)
    confere(rc == 0 and rel["aprovado"], "conferência: APROVADO (%s)" % rel["contagem"])
    r = subprocess.run([PY, "-X", "utf8", str(W / "atualizar_repo_publico.py"), "central-publica", str(d), "teste: a cópia vira referência"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    confere(r.returncode == 0 and "PUBLICADO E CONFERIDO" in r.stdout, "publicador: %s" % (r.stdout.strip().splitlines() or [""])[-1][:150] + (r.stderr[-300:] if r.returncode else ""))
    arv = set(git(d, "ls-tree", "-r", "--name-only", "origin/main").stdout.split())
    confere(not {"dados/b.txt", "dados/c/z.txt", "dados/readme_copia.md", "dados/s_copia.py"} & arv and {"dados/a.txt", "dados/u.txt", "central_publica_22out/s2.py",
            CR.SCRIPT, "INDICE_PUBLICO.json"} <= arv, "árvore remota: sem as cópias; originais, únicos, esteira, script e índice presentes (%d)" % len(arv))
    msg = git(d, "log", "-1", "--format=%B").stdout
    confere("Cópias idênticas só no índice" in msg and ": 4." in msg, "a mensagem do commit diz quantas cópias ficaram só no índice")

    print("4. o clone se reconstrói")
    git(base, "clone", "-q", str(nu), str(clone))
    confere(not (clone / "dados/b.txt").exists(), "o clone não tem as cópias")
    rr = subprocess.run([PY, "-X", "utf8", str(clone / CR.SCRIPT)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok4 = rr.returncode == 0 and all((clone / k).is_file() and sha((clone / k).read_bytes()) == sha(v) for k, v in ARQS.items())
    confere(ok4, "RECONSTRUIR_COPIAS.py recria as 4 cópias com o sha256 (%s)" % rr.stdout.strip()[-90:])
    (clone / "dados/a.txt").write_bytes(b"adulterado\n")
    rr = subprocess.run([PY, "-X", "utf8", str(clone / CR.SCRIPT), "--conferir"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    confere(rr.returncode == 1 and "diferente" in rr.stdout, "original adulterado no clone: --conferir falha (exit 1)")
    shutil.rmtree(clone, onexc=_rm_ro)

    print("5. cópia nova com caminho menor não troca o original")
    escrever(d, "dados/0_novo.txt", ARQS["dados/a.txt"])
    idx = indice(d); idx["arquivos"].append({"caminho": "dados/0_novo.txt", "bytes": len(ARQS["dados/a.txt"]), "sha256": sha(ARQS["dados/a.txt"])})
    idx["arquivos"].sort(key=lambda x: x["caminho"]); gravar_indice(d, idx)
    r5 = CR.referenciar(d); p = por(d)
    confere(r5["ok"] and p["dados/0_novo.txt"].get("igual_a") == "dados/a.txt" and not (d / "dados/0_novo.txt").exists(), "o original segue dados/a.txt; a cópia nova vira referência")

    print("6. o original muda de conteúdo (a mescla gravou bytes novos): o grupo antigo volta do HEAD")
    novo = b"conteudo X2\n"
    (d / "dados/a.txt").write_bytes(novo)
    idx = indice(d)
    for a in idx["arquivos"]:
        if a["caminho"] == "dados/a.txt":
            a.clear(); a.update({"caminho": "dados/a.txt", "bytes": len(novo), "sha256": sha(novo)})
    gravar_indice(d, idx)
    r6 = CR.referenciar(d); p = por(d)
    confere(r6["ok"] and r6["restaurados_do_head"] == 1 and "igual_a" not in p["dados/0_novo.txt"] and (d / "dados/0_novo.txt").read_bytes() == ARQS["dados/a.txt"]
            and p["dados/b.txt"].get("igual_a") == "dados/0_novo.txt", "restaurado do HEAD no menor caminho do grupo, conferido pelo sha256")
    rc, rel = conferir(d)
    confere(rc == 0 and rel["aprovado"], "conferência depois da restauração: APROVADO (%s)" % rel["contagem"])

    print("7. o original é EXCLUÍDO pela esteira: PARA, nada gravado")
    idx_antes = (d / "INDICE_PUBLICO.json").read_bytes()
    (d / "dados/0_novo.txt").unlink()
    idx = indice(d); idx["arquivos"] = [a for a in idx["arquivos"] if a["caminho"] != "dados/0_novo.txt"]; gravar_indice(d, idx)
    LOCAL.write_text(json.dumps({"motivo de teste": ["dados/0_novo.txt"]}), encoding="utf-8")
    idx_meio = (d / "INDICE_PUBLICO.json").read_bytes()
    r7 = CR.referenciar(d)
    confere(not r7["ok"] and "EXCLUÍDO" in " ".join(r7["parar"]) and (d / "INDICE_PUBLICO.json").read_bytes() == idx_meio and not (d / "dados/b.txt").exists(),
            "PARAR com o motivo; índice e preparo intocados")
    rr = subprocess.run([PY, "-X", "utf8", str(W / "copias_referencia.py"), str(d)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    confere(rr.returncode == 1 and "PARAR" in rr.stdout, "pela linha de comando: exit 1")

    print("8. o original some da origem (sem exclusão): restaura do HEAD")
    LOCAL.unlink()
    r8 = CR.referenciar(d); p = por(d)
    confere(r8["ok"] and r8["restaurados_do_head"] == 1 and (d / "dados/b.txt").read_bytes() == ARQS["dados/a.txt"] and p["dados/c/z.txt"].get("igual_a") == "dados/b.txt",
            "restaurado em dados/b.txt; dados/c/z.txt aponta para ele")
    rc, rel = conferir(d)
    confere(rc == 0 and rel["aprovado"], "conferência: APROVADO (%s)" % rel["contagem"])

    print("9. controles negativos da conferência")
    escrever(d, "dados/c/z.txt", ARQS["dados/a.txt"])
    rc, rel = conferir(d)
    confere(rc == 1 and "cópia referenciada ainda no preparo" in rel["contagem"], "cópia física que ficou: REPROVADO (%s)" % rel["contagem"])
    (d / "dados/c/z.txt").unlink()
    idx = indice(d); bak = json.dumps(idx, ensure_ascii=False)
    for a in idx["arquivos"]:
        if a["caminho"] == "dados/readme_copia.md":
            a["igual_a"] = "dados/c/z.txt"
    gravar_indice(d, idx)
    rc, rel = conferir(d)
    confere(rc == 1 and "referência de cópia não confere com o original" in rel["contagem"], "referência para outra referência: REPROVADO (%s)" % rel["contagem"])
    (d / "INDICE_PUBLICO.json").write_text(bak, encoding="utf-8")
    ob = (d / "dados/b.txt").read_bytes(); (d / "dados/b.txt").write_bytes(b"adulterado\n")
    rc, rel = conferir(d)
    confere(rc == 1 and "original de cópia ausente ou diferente do índice" in rel["contagem"], "original adulterado: REPROVADO (%s)" % rel["contagem"])
    (d / "dados/b.txt").write_bytes(ob)
    sb = (d / CR.SCRIPT).read_bytes(); (d / CR.SCRIPT).unlink()
    rc, rel = conferir(d)
    confere(rc == 1 and "cópias referenciadas sem RECONSTRUIR_COPIAS.py na raiz" in rel["contagem"], "sem o script na raiz: REPROVADO (%s)" % rel["contagem"])
    (d / CR.SCRIPT).write_bytes(sb)
    rc, rel = conferir(d)
    confere(rc == 0 and rel["aprovado"], "restaurado: APROVADO de novo (%s)" % rel["contagem"])

    print("10. com o índice em partes (como no work): publicação e clone")
    IP.LIMITE, IP.PARTE_MAX = 300, 400
    rp = IP.fatiar(d)
    confere(rp["forma"] == "partes" and rp["partes"] >= 2, "índice em %d partes" % rp["partes"])
    rc, rel = conferir(d)
    confere(rc == 0 and rel["aprovado"], "conferência com partes e referências: APROVADO (%s)" % rel["contagem"])
    r = subprocess.run([PY, "-X", "utf8", str(W / "atualizar_repo_publico.py"), "central-publica", str(d), "teste: partes e referências"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    confere(r.returncode == 0 and "PUBLICADO E CONFERIDO" in r.stdout, "publicador com partes: %s" % (r.stdout.strip().splitlines() or [""])[-1][:150] + (r.stderr[-300:] if r.returncode else ""))
    git(base, "clone", "-q", str(nu), str(clone))
    confere(not (clone / "INDICE_PUBLICO.json").exists() and (clone / "INDICE_PUBLICO_PARTES" / "PARTES.json").is_file(), "o clone tem só as partes do índice")
    rr = subprocess.run([PY, "-X", "utf8", str(clone / CR.SCRIPT)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    esperado = {k: v for k, v in ARQS.items() if k != "dados/a.txt"}
    esperado.update({"dados/a.txt": novo, "dados/c/z.txt": ARQS["dados/a.txt"], "dados/b.txt": ARQS["dados/a.txt"]})
    ok10 = rr.returncode == 0 and all((clone / k).is_file() and (clone / k).read_bytes() == v for k, v in esperado.items())
    confere(ok10, "RECONSTRUIR_COPIAS.py lê as partes e recria a árvore inteira (%s)" % rr.stdout.strip()[-90:])
finally:
    for x in list(W.glob("varredura_conferencia_%s*.json" % NOME)):
        x.unlink()
    if LOCAL.exists():
        LOCAL.unlink()
    shutil.rmtree(base, onexc=_rm_ro)
print("FALHAS: %d %s" % (len(falhas), falhas) if falhas else "TODOS OS CASOS PASSAM")
sys.exit(1 if falhas else 0)

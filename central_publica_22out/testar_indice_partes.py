# -*- coding: utf-8 -*-
"""Teste do ÍNDICE EM PARTES (11/11/2026, custódia v410, claude-site-custodia): o fatiador (indice_partes.py) num preparo sintético, com teto
reduzido para caber num teste, e a conferência INDEPENDENTE (conferir_preparos.py, rodada como na cadeia) aprovando o certo e reprovando o
errado. Controles negativos: parte adulterada, sobra na pasta das partes, índice inteiro de volta ao git. Também: idempotência (a 2ª rodada
não grava nada), a forma não oscila (em partes fica em partes) e a sobra de parte some quando o índice encolhe. O preparo sintético é uma
pasta temporária fora da Central; os relatórios que a conferência grava ao lado dela saem no fim. Uso: testar_indice_partes.py"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import indice_partes as IP  # noqa: E402

PY = r"C:\Python314\python.exe"
falhas = []


def confere(cond, rotulo):
    print(("  ok   " if cond else "  FALHA ") + rotulo)
    if not cond:
        falhas.append(rotulo)


def git(d, *a):
    return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True, text=True)


def conferir(d):
    r = subprocess.run([PY, "-X", "utf8", str(W / "conferir_preparos.py"), str(d)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    rel = json.loads((W / ("varredura_conferencia_%s.json" % d.name)).read_text(encoding="utf-8"))
    return r.returncode, rel


def montar(d, n):
    arqs = []
    for i in range(n):
        rel = "dados/arquivo_%04d.txt" % i
        b = ("linha de teste numero %d da esteira publica\n" % i).encode("utf-8")
        (d / "dados").mkdir(exist_ok=True)
        (d / rel).write_bytes(b)
        arqs.append({"caminho": rel, "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    idx = {"regiao": "work", "gerado_em": "2026-11-11 00:00:00", "n_arquivos": len(arqs), "arquivos": arqs}
    (d / "INDICE_PUBLICO.json").write_text(json.dumps(idx, ensure_ascii=False), encoding="utf-8")
    (d / "README.md").write_text("# preparo de teste\n\nO índice vai em partes em `INDICE_PUBLICO_PARTES/`.\n", encoding="utf-8")
    return idx


base = Path(tempfile.mkdtemp(prefix="teste_partes_"))
d = base / "teste_partes_preparo"
d.mkdir()
try:
    IP.LIMITE, IP.PARTE_MAX = 4000, 3000                         # teto reduzido só neste processo
    git(d, "init", "-q"); git(d, "config", "user.email", "teste.invalid"); git(d, "config", "user.name", "teste")
    idx = montar(d, 120)
    git(d, "add", "-A"); git(d, "commit", "-q", "-m", "estado anterior: o indice inteiro rastreado")
    confere(bool(git(d, "ls-files", "INDICE_PUBLICO.json").stdout.strip()), "antes: o índice inteiro está rastreado")

    print("1. fatiar")
    r1 = IP.fatiar(d)
    confere(r1["forma"] == "partes" and r1["partes"] >= 3, "em partes: %s" % {k: r1.get(k) for k in ("forma", "partes", "entradas")})
    cab = json.loads((d / IP.PASTA / IP.CAB).read_text(encoding="utf-8"))
    uniao = []
    for p in cab["partes"]:
        b = (d / p["arquivo"]).read_bytes()
        confere(len(b) <= IP.PARTE_MAX + 400 and hashlib.sha256(b).hexdigest() == p["sha256"], "parte %s: bytes %d, sha256 confere" % (p["arquivo"], len(b)))
        uniao += json.loads(b)["arquivos"]
    confere(uniao == idx["arquivos"], "as partes, concatenadas, são o índice inteiro entrada por entrada")
    confere(git(d, "check-ignore", "-q", "INDICE_PUBLICO.json").returncode == 0, "o índice inteiro ficou fora do git (exclude local)")
    confere(not git(d, "ls-files", "--cached", "INDICE_PUBLICO.json").stdout.strip(), "o índice inteiro saiu do índice do git (rm --cached)")
    confere((d / "INDICE_PUBLICO.json").is_file(), "o índice inteiro continua no preparo (a esteira o lê)")

    print("2. idempotência e forma estável")
    r2 = IP.fatiar(d)
    confere(r2["arquivos_gravados"] == 0, "a 2ª rodada não grava nada (%d)" % r2["arquivos_gravados"])
    IP.LIMITE = 10 ** 9
    confere(IP.em_partes(d), "com o teto alto, segue em partes (a forma não oscila)")
    IP.LIMITE = 4000

    print("3. conferência independente: o certo passa")
    rc, rel = conferir(d)
    confere(rc == 0 and rel["aprovado"] is True, "APROVADO (%s)" % rel["contagem"])

    print("4. controles negativos")
    p1 = d / cab["partes"][0]["arquivo"]
    orig = p1.read_bytes()
    p1.write_bytes(orig.replace(b"numero", b"NUMERO", 1) if b"numero" in orig else orig[:-1] + b" ")
    rc, rel = conferir(d)
    confere(rc == 1 and "partes do índice não conferem com o índice" in rel["contagem"], "parte adulterada: REPROVADO (%s)" % rel["contagem"])
    p1.write_bytes(orig)
    sobra = d / IP.PASTA / "parte_999.json"
    sobra.write_text("{}", encoding="utf-8")
    rc, rel = conferir(d)
    confere(rc == 1 and "partes do índice não conferem com o índice" in rel["contagem"], "sobra na pasta das partes: REPROVADO (%s)" % rel["contagem"])
    sobra.unlink()
    exc = d / ".git" / "info" / "exclude"
    ex_orig = exc.read_bytes()
    exc.write_bytes(ex_orig.replace(IP.EXCLUIR.encode(), b"# (tirado pelo teste)"))
    git(d, "add", "-f", "INDICE_PUBLICO.json")
    rc, rel = conferir(d)
    confere(rc == 1 and "índice inteiro ainda no git (as partes o substituem)" in rel["contagem"], "índice inteiro de volta ao git: REPROVADO (%s)" % rel["contagem"])
    exc.write_bytes(ex_orig)
    git(d, "rm", "--cached", "-q", "INDICE_PUBLICO.json")
    rc, rel = conferir(d)
    confere(rc == 0 and rel["aprovado"] is True, "restaurado: APROVADO de novo (%s)" % rel["contagem"])

    print("5. o índice encolhe: a parte que sobra some")
    n_antes = len(cab["partes"])
    idx2 = dict(idx, arquivos=idx["arquivos"][:30], n_arquivos=30)
    (d / "INDICE_PUBLICO.json").write_text(json.dumps(idx2, ensure_ascii=False), encoding="utf-8")
    r5 = IP.fatiar(d)
    confere(r5["partes"] < n_antes and len(r5["sobras_tiradas"]) == n_antes - r5["partes"], "de %d para %d partes; sobras tiradas %s" % (n_antes, r5["partes"], r5["sobras_tiradas"]))

    print("6. o README que não descreve as partes para a cadeia")
    (d / "README.md").write_text("# preparo de teste\n", encoding="utf-8")
    r6 = subprocess.run([PY, "-X", "utf8", "-c", "import sys; sys.path.insert(0, r'%s'); import runpy; sys.argv=['indice_partes.py', r'%s']; "
                         "runpy.run_path(r'%s', run_name='__main__')" % (W, d, W / "indice_partes.py")], capture_output=True, text=True, encoding="utf-8", errors="replace")
    confere(r6.returncode == 1 and "PARAR" in r6.stdout, "README sem as partes: exit 1 (%s)" % r6.stdout.strip()[-90:])
finally:
    for x in W.glob("varredura_conferencia_teste_partes_preparo*.json"):
        x.unlink()
    shutil.rmtree(base, ignore_errors=True)
print("FALHAS: %d %s" % (len(falhas), falhas) if falhas else "TODOS OS CASOS PASSAM")
sys.exit(1 if falhas else 0)

# -*- coding: utf-8 -*-
"""O ÍNDICE PÚBLICO EM PARTES (11/11/2026, custódia v410, claude-site-custodia). O GitHub recusa arquivo acima de 100 MB, e o índice do
central-publica-work passou disso (110,5 MB, 560.815 entradas, depois da cadeia de selo da v410). O índice INTEIRO continua no preparo, onde
toda a esteira o lê e o grava como sempre (nada muda nos outros scripts); só a FORMA PUBLICADA muda: acima do teto, o índice vai ao git em
partes de até 45 MiB, em INDICE_PUBLICO_PARTES/ (parte_001.json, parte_002.json, ...), com PARTES.json listando cada parte (entradas, bytes,
sha256) e o sha256 do índice inteiro; o INDICE_PUBLICO.json inteiro sai do git (git rm --cached) e fica só local (.git/info/exclude).
Nenhum arquivo deixa de ser publicado: a lista «arquivos» das partes, concatenada na ordem, é entrada por entrada a do índice inteiro.
Uma vez em partes, fica em partes (a forma não oscila entre rodadas). Abaixo do teto e sem partes: não faz nada.
Determinístico: o mesmo índice gera os mesmos bytes (sem carimbo de hora próprio), logo uma rodada sem mudança não gera diferença no git.
A conferência independente (conferir_preparos.py) NÃO importa este arquivo: confere as partes contra o índice por conta própria.
Uso: indice_partes.py <pasta_do_preparo>   (exit 1 se o README do preparo ainda não descreve as partes: rode a cadeia de novo)"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

LIMITE = 90 * 1024 * 1024          # acima disto o índice inteiro não vai ao git (a conferência barra arquivo acima de 95 MiB; o GitHub, de 100 MB)
PARTE_MAX = 45 * 1024 * 1024
PASTA = "INDICE_PUBLICO_PARTES"
CAB = "PARTES.json"
EXCLUIR = "/INDICE_PUBLICO.json"


def em_partes(d):
    """A decisão da forma, a mesma para o gerador dos README e para o fatiador: em partes se já está em partes ou se o índice passa do LIMITE."""
    d = Path(d)
    return (d / PASTA / CAB).is_file() or (d / "INDICE_PUBLICO.json").stat().st_size > LIMITE


def _gravar(p, b):
    if p.is_file() and p.read_bytes() == b:
        return False
    t = p.with_name(p.name + ".tmp_atual")
    t.write_bytes(b)
    assert t.stat().st_size == len(b)
    os.replace(t, p)
    return True


def _git(d, *a):
    return subprocess.run(["git", "-C", str(d)] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace",
                          env=dict(os.environ, GIT_LITERAL_PATHSPECS="1"))


def ignorado(d, nome="INDICE_PUBLICO.json"):
    """`git check-ignore` SEM GIT_LITERAL_PATHSPECS: o comando recusa essa magia («pathspec magic not supported: 'literal'», rc 128)."""
    env = {k: v for k, v in os.environ.items() if k != "GIT_LITERAL_PATHSPECS"}
    return subprocess.run(["git", "-C", str(d), "check-ignore", "-q", nome], capture_output=True, env=env).returncode == 0


def fatiar(d):
    d = Path(d)
    ip = d / "INDICE_PUBLICO.json"
    if not em_partes(d):
        return {"forma": "inteiro", "bytes": ip.stat().st_size}
    raw = ip.read_bytes()
    idx = json.loads(raw.decode("utf-8"))
    arqs = idx["arquivos"]
    cab_idx = {k: v for k, v in idx.items() if k != "arquivos"}
    blocos, atual, tam = [], [], 0
    for a in arqs:
        n = len(json.dumps(a, ensure_ascii=False).encode("utf-8")) + 2
        if atual and tam + n > PARTE_MAX:
            blocos.append(atual); atual, tam = [], 0
        atual.append(a); tam += n
    if atual or not blocos:
        blocos.append(atual)
    pd = d / PASTA
    pd.mkdir(exist_ok=True)
    partes, mudou = [], 0
    for i, bl in enumerate(blocos, 1):
        nome = "parte_%03d.json" % i
        b = json.dumps({"regiao": idx.get("regiao"), "parte": i, "partes": len(blocos), "arquivos": bl}, ensure_ascii=False).encode("utf-8")
        assert len(b) <= 95 * 1024 * 1024, (nome, len(b))
        mudou += _gravar(pd / nome, b)
        partes.append({"arquivo": "%s/%s" % (PASTA, nome), "entradas": len(bl), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest()})
    assert sum(p["entradas"] for p in partes) == len(arqs)
    cab = {"schema": "iald.central_publica.indice_em_partes/v1",
           "o_que_e": "o índice público deste repositório (o sha256 de cada arquivo publicado), em partes: inteiro, passaria do limite de 100 MB por arquivo do GitHub",
           "como_ler": "concatenar, na ordem de «partes», a lista «arquivos» de cada parte: é a lista do índice inteiro, entrada por entrada",
           "desde": "11/11/2026 (custódia v410)",
           "cabecalho_do_indice": cab_idx,
           "entradas": len(arqs),
           "indice_inteiro": {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()},
           "partes": partes}
    mudou += _gravar(pd / CAB, (json.dumps(cab, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))
    validas = {CAB} | {Path(p["arquivo"]).name for p in partes}
    sobras = sorted(x for x in os.listdir(pd) if x not in validas)
    for x in sobras:                                   # parte que sobrou de uma rodada com mais partes: é gerada, sai (o git a retira no envio)
        assert x.startswith("parte_") and x.endswith(".json"), ("arquivo estranho na pasta das partes — PARAR", x)
        os.remove(pd / x)
    # o índice inteiro: fora do git (local, .git/info/exclude) e fora do índice do git (git rm --cached; o envio confirma)
    exc = d / ".git" / "info" / "exclude"
    t = exc.read_text(encoding="utf-8") if exc.is_file() else ""
    if EXCLUIR not in t.splitlines():
        nt = (t if (not t or t.endswith("\n")) else t + "\n") + "# 11/11/2026 (custodia v410): o indice inteiro fica local; o git leva as partes\n" + EXCLUIR + "\n"
        _gravar(exc, nt.encode("utf-8"))
    if _git(d, "ls-files", "--cached", "--", "INDICE_PUBLICO.json").stdout.strip():
        r = _git(d, "rm", "--cached", "-q", "--", "INDICE_PUBLICO.json")
        assert r.returncode == 0, r.stderr[-400:]
    assert ignorado(d), "o índice inteiro não ficou fora do git — PARAR"
    return {"forma": "partes", "partes": len(partes), "entradas": len(arqs), "bytes_inteiro": len(raw), "maior_parte": max(p["bytes"] for p in partes),
            "arquivos_gravados": mudou, "sobras_tiradas": sobras}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    D = Path(sys.argv[1])
    r = fatiar(D)
    if r["forma"] == "inteiro":
        print("%s: índice inteiro (%d bytes, abaixo do teto de %d): nada a fatiar" % (D.name, r["bytes"], LIMITE))
        sys.exit(0)
    rd = (D / "README.md").read_text(encoding="utf-8") if (D / "README.md").is_file() else ""
    if PASTA not in rd:
        print("%s: o README.md ainda não descreve o índice em partes (foi gerado antes delas): rode a cadeia de novo — PARAR" % D.name)
        sys.exit(1)
    print("%s: índice em %d partes (%d entradas; inteiro %d bytes, fica local; maior parte %d bytes) | %d arquivo(s) gravado(s) | sobras %s" % (
        D.name, r["partes"], r["entradas"], r["bytes_inteiro"], r["maior_parte"], r["arquivos_gravados"], r["sobras_tiradas"]))

# -*- coding: utf-8 -*-
"""A CÓPIA VIRA REFERÊNCIA (11/11/2026, claude-site-custodia; decisão do operador, verbatim em
work/cunhagens_13out/OPERADOR_11nov_central_publica_copia_vira_referencia_verbatim.txt: «Cópia vira referência», aplicada a partir da
publicação da v411). Num preparo público, um arquivo idêntico, byte a byte, a outro do MESMO repositório não vai de novo ao git: a entrada
dele no INDICE_PUBLICO.json ganha "igual_a" (o caminho do original; bytes e sha256 iguais) e o arquivo físico sai do preparo. Nenhum
conteúdo sai do repositório: o original fica, o índice diz onde, e RECONSTRUIR_COPIAS.py (gravado na raiz) recria as cópias num clone.

Regras:
- referência só DENTRO do repositório (cada um autocontido); a raiz gerada (README, índice, exclusões, llms.txt…), as partes do índice e
  a esteira do work (central_publica_22out/, que atualizar_pasta_no_preparo.py regrava) nunca viram referência, mas podem ser original;
- o original é ESTÁVEL: fica o que já era original (sem "igual_a"), já publicado no HEAD, e só depois o menor caminho;
- antes de apagar uma cópia, o sha256 do original e o da cópia são conferidos contra o índice;
- grupo sem nenhum arquivo físico (o original mudou de conteúdo ou sumiu da origem): o conteúdo volta do HEAD do preparo (pelos caminhos
  do grupo e, se não, por qualquer blob do HEAD com o mesmo tamanho), conferido pelo sha256, no menor caminho do grupo; se o original
  anterior foi EXCLUÍDO pela esteira (lista local de exclusões), PARA: as cópias têm os mesmos bytes do excluído e a decisão não é desta
  ferramenta;
- tudo ou nada: com qualquer motivo de parada, nada se grava. A ordem de escrita (restaurados, índice, apagamentos) deixa a rodada
  seguinte consertar uma queda no meio.
Uso: copias_referencia.py <pasta_do_preparo> [--simular]   (exit 1 = PARAR)"""
import hashlib, json, os, subprocess, sys
from collections import defaultdict
from pathlib import Path

W = Path(__file__).resolve().parent
CAMPO = "igual_a"
SCRIPT = "RECONSTRUIR_COPIAS.py"
FIXOS = {"README.md", "PATENTES.md", "vinculo_patentario.json", "INDICE_PUBLICO.json", "EXCLUSOES_PUBLICAS.json", ".gitattributes",
         "llms.txt", SCRIPT}
PREF_FIXOS = ("INDICE_PUBLICO_PARTES/", "central_publica_22out/")
ENV_GIT = {k: v for k, v in os.environ.items() if k != "GIT_LITERAL_PATHSPECS"}

RECONSTRUIR = r'''# -*- coding: utf-8 -*-
"""RECONSTRUIR AS CÓPIAS (gerado pela esteira da Central pública da IALD; decisão do operador de 11/11/2026: a cópia vira referência).
Neste repositório, um arquivo idêntico, byte a byte, a outro já publicado aqui não se repete: o índice público o lista com o campo
"igual_a" (o caminho do original, com os mesmos bytes e o mesmo sha256). Num clone, este script recria cada cópia a partir do original
e confere o sha256 de cada uma. Só a biblioteca padrão.
Uso: python RECONSTRUIR_COPIAS.py [--conferir]   (--conferir: só confere os originais, não grava nada)"""
import hashlib, json, shutil, sys
from pathlib import Path

R = Path(__file__).resolve().parent


def entradas():
    cab = R / "INDICE_PUBLICO_PARTES" / "PARTES.json"
    if cab.is_file():
        for p in json.loads(cab.read_text(encoding="utf-8"))["partes"]:
            b = (R / p["arquivo"]).read_bytes()
            if hashlib.sha256(b).hexdigest() != p["sha256"]:
                sys.exit("parte do índice diferente do cabeçalho: %s" % p["arquivo"])
            yield from json.loads(b.decode("utf-8"))["arquivos"]
    else:
        yield from json.loads((R / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))["arquivos"]


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def dentro(p):
    p = p.resolve()
    return p == R or R in p.parents


so_conferir = "--conferir" in sys.argv
visto, feitas, iguais, falhas = {}, 0, 0, 0
for a in entradas():
    o = a.get("igual_a")
    if not o:
        continue
    src, dst = R / o, R / a["caminho"]
    if not (dentro(src) and dentro(dst)):
        print("caminho fora do repositório:", a["caminho"]); falhas += 1; continue
    if o not in visto:
        visto[o] = sha(src) if src.is_file() else None
    if visto[o] != a["sha256"]:
        print("original ausente ou diferente do índice:", o); falhas += 1; continue
    if dst.is_file() and sha(dst) == a["sha256"]:
        iguais += 1; continue
    if so_conferir:
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    feitas += 1
print("cópias recriadas: %d | já presentes: %d | originais conferidos: %d | falhas: %d" % (feitas, iguais, len(visto), falhas))
sys.exit(1 if falhas else 0)
'''


def fixo(rel):
    return rel in FIXOS or rel.startswith(PREF_FIXOS)


_BASES = {}


def longo(D, rel):
    k = str(D)
    if k not in _BASES:                                   # resolve() uma vez por preparo, não por arquivo
        b = str(Path(D).resolve())
        _BASES[k] = b if b.startswith("\\\\?\\") else "\\\\?\\" + b
    return _BASES[k] + "\\" + rel.replace("/", "\\")


def sha_arq(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _git(D, *a):
    return subprocess.run(["git", "-C", str(D)] + list(a), capture_output=True, env=ENV_GIT)


def _do_head(D, rel):
    """Os bytes de <rel> no HEAD do preparo, ou None."""
    r = _git(D, "cat-file", "blob", "HEAD:" + rel)
    return r.stdout if r.returncode == 0 else None


_POR_TAMANHO = {}


def _procurar_no_head(D, sha, n):
    """Os bytes de sha256 <sha> e <n> bytes em QUALQUER caminho do HEAD (o original pode ter mudado duas vezes entre publicações: os bytes
    seguem no HEAD num caminho que o índice já não cita). Só blobs do mesmo tamanho são lidos, cada um conferido pelo sha256."""
    k = str(D)
    if k not in _POR_TAMANHO:
        m = defaultdict(list)
        for l in _git(D, "ls-tree", "-r", "-l", "-z", "HEAD").stdout.decode("utf-8", "replace").split("\0"):
            if l:
                p = l.split("\t", 1)[0].split()
                if p[1] == "blob" and p[3].isdigit():
                    m[int(p[3])].append(p[2])
        _POR_TAMANHO[k] = m
    for oid in dict.fromkeys(_POR_TAMANHO[k].get(n, [])):
        r = _git(D, "cat-file", "blob", oid)
        if r.returncode == 0 and len(r.stdout) == n and hashlib.sha256(r.stdout).hexdigest() == sha:
            return r.stdout
    return None


def referenciar(D, simular=False):
    D = Path(D)
    _POR_TAMANHO.pop(str(D), None)                        # o HEAD pode ter mudado desde a última chamada
    IP = D / "INDICE_PUBLICO.json"
    idx = json.loads(IP.read_text(encoding="utf-8"))
    rastreados = set(x for x in _git(D, "ls-files", "-z").stdout.decode("utf-8", "replace").split("\0") if x)
    LP = W / ("varredura_exclusoes_%s.json" % D.name)
    ja_fora = {x for v in json.loads(LP.read_text(encoding="utf-8")).values() for x in v} if LP.is_file() else set()
    grupos = defaultdict(list)
    for a in idx["arquivos"]:
        grupos[(a["sha256"], a["bytes"])].append(a)
    parar, restaurar, apagar = [], [], []
    mudou = 0
    st = {"grupos_com_copia": 0, "referencias": 0, "novas": 0, "originais_conferidos": 0, "bytes_conferidos": 0}
    for (sha, n), membros in grupos.items():
        if len(membros) == 1 and CAMPO not in membros[0]:
            continue                                          # arquivo único (a conferência confere que existe)
        presentes = {m["caminho"] for m in membros if os.path.isfile(longo(D, m["caminho"]))}
        if not presentes:
            if any(fixo(m["caminho"]) for m in membros):
                parar.append("arquivo fixo da raiz ou da esteira ausente do preparo: %s" % sorted(m["caminho"] for m in membros if fixo(m["caminho"])))
                continue
            ant = sorted({m[CAMPO] for m in membros if m.get(CAMPO)})
            if any(x in ja_fora for x in ant):
                parar.append("o original %s de %d cópia(s) foi EXCLUÍDO pela esteira; as cópias têm os mesmos bytes — decisão humana" % (ant, len(membros)))
                continue
            alvo = min(m["caminho"] for m in membros)
            blob = None
            for cand in [alvo] + sorted(m["caminho"] for m in membros if m["caminho"] != alvo) + ant:
                b = _do_head(D, cand)
                if b is not None and len(b) == n and hashlib.sha256(b).hexdigest() == sha:
                    blob = b; break
            if blob is None:
                blob = _procurar_no_head(D, sha, n)
            if blob is None:
                parar.append("grupo sem arquivo no preparo e sem os bytes no HEAD: %s (%d entradas)" % (alvo, len(membros)))
                continue
            restaurar.append((alvo, blob))
            presentes = {alvo}
        st["grupos_com_copia"] += len(membros) > 1
        cands = sorted((m for m in membros if m["caminho"] in presentes),
                       key=lambda m: (0 if fixo(m["caminho"]) else 1, 0 if CAMPO not in m else 1, 0 if m["caminho"] in rastreados else 1, m["caminho"]))
        orig = cands[0]["caminho"]
        a_apagar = []
        for m in membros:
            r = m["caminho"]
            if r == orig or fixo(r):
                if CAMPO in m:
                    del m[CAMPO]; mudou += 1
                continue
            if m.get(CAMPO) != orig:
                st["novas"] += CAMPO not in m
                m[CAMPO] = orig; mudou += 1
            st["referencias"] += 1
            if r in presentes:
                a_apagar.append(r)
        if a_apagar:
            if not any(x[0] == orig for x in restaurar):    # o restaurado acabou de ser conferido pelo sha256
                so = sha_arq(longo(D, orig)); st["originais_conferidos"] += 1; st["bytes_conferidos"] += n
                if so != sha:
                    parar.append("original %s diferente do índice: as cópias não se apagam" % orig); continue
            for r in a_apagar:
                if sha_arq(longo(D, r)) != sha:
                    parar.append("cópia %s diferente do índice: preparo inconsistente" % r); break
                st["bytes_conferidos"] += n
            else:
                apagar.extend(a_apagar)
    st.update({"restaurados_do_head": len(restaurar), "apagados_agora": len(apagar), "entradas_mudadas": mudou})
    if parar:
        return {"ok": False, "parar": parar[:20], "n_parar": len(parar), **st}
    tem_refs = st["referencias"] > 0
    sp = D / SCRIPT
    if simular:
        return {"ok": True, "simulado": True, **st}
    for rel, b in restaurar:
        q = longo(D, rel)
        os.makedirs(os.path.dirname(q), exist_ok=True)
        t = q + ".tmp_copia"
        with open(t, "wb") as fh:
            fh.write(b)
        assert os.path.getsize(t) == len(b)
        os.replace(t, q)
    if mudou:
        t = IP.with_name(IP.name + ".tmp_copias")
        dados = json.dumps(idx, ensure_ascii=False).encode("utf-8")
        t.write_bytes(dados)
        assert t.stat().st_size == len(dados) > 0
        os.replace(t, IP)
    for rel in apagar:
        os.remove(longo(D, rel))
    if tem_refs and (not sp.is_file() or sp.read_bytes() != RECONSTRUIR.encode("utf-8")):
        sp.write_bytes(RECONSTRUIR.encode("utf-8"))
    elif not tem_refs and sp.is_file():
        sp.unlink()
    return {"ok": True, **st}


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    D = Path(sys.argv[1])
    r = referenciar(D, simular="--simular" in sys.argv)
    if not r["ok"]:
        print("%s: PARAR (%d motivo(s)); nada gravado: %s" % (D.name, r["n_parar"], r["parar"]))
        sys.exit(1)
    print("%s: %s%d grupos com cópia | %d referências (%d novas) | %d cópias apagadas do preparo agora | %d restaurados do HEAD | "
          "%d originais conferidos (%.2f GB conferidos) | %d entradas mudadas" % (
              D.name, "SIMULADO: " if r.get("simulado") else "", r["grupos_com_copia"], r["referencias"], r["novas"], r["apagados_agora"],
              r["restaurados_do_head"], r["originais_conferidos"], r["bytes_conferidos"] / 1e9, r["entradas_mudadas"]))

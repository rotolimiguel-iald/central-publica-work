# -*- coding: utf-8 -*-
"""Gera um literal de `ramos` COM A MARCA a partir de artefatos/RAMOS_V410.json (nenhum dado observado e' lido).

  python gerar_ramos_v411.py --marca __XXX [--marca-so-da-leitura __YYY] --saida <json>

Regras: no `sufixo` a marca entra logo depois de `__RETRODICTION_WITHOUT_FIT`; em `leitura_partes` entra logo antes de
`__PROVED_IS_VALIDITY_NOT_CREDITATION` (palavra PARTIDA na lista: `...__PRO` + `VED_IS_VALIDITY...`; a lista continua partida:
nenhuma parte sozinha traz `PROVED` inteiro, e a juncao das partes da a cabeca certa); a marca so' da leitura, se vier, entra na
leitura imediatamente antes da marca geral. Nada mais muda. Recusa trecho que nao comece por `__`, que tenha caractere fora de
[A-Z0-9_] (ou so' `__`), ou saida existente. Grava ao lado <saida sem .json>_ORIGEM.json (sha256 do RAMOS_V410, dos trechos e do
resultado). NAO gera o literal de producao: a palavra da marca e' do operador."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAMOS_V410 = HERE.parent / "artefatos" / "RAMOS_V410.json"
ORIGEM_V410 = HERE.parent / "artefatos" / "RAMOS_V410_ORIGEM.json"
ANCORA_SUFIXO = "__RETRODICTION_WITHOUT_FIT"
ANCORA_LEITURA = "__PROVED_IS_VALIDITY_NOT_CREDITATION"
OK_TRECHO = re.compile(r"__[A-Z0-9_]+")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def validar_trecho(t, nome):
    if not isinstance(t, str) or not OK_TRECHO.fullmatch(t):
        raise SystemExit("RECUSA: %s deve comecar por '__', ter ao menos um caractere depois e so' [A-Z0-9_]: %r" % (nome, t))


def gerar(ramos, marca, so_leitura):
    r = json.loads(json.dumps(ramos))
    V = r["vereditos"]
    suf = V["sufixo"]
    if suf.count(ANCORA_SUFIXO) != 1:
        raise SystemExit("RECUSA: sufixo nao traz exatamente uma vez " + ANCORA_SUFIXO)
    i = suf.index(ANCORA_SUFIXO) + len(ANCORA_SUFIXO)
    V["sufixo"] = suf[:i] + marca + suf[i:]
    partes = list(V["leitura_partes"])
    juncao = "".join(partes)
    if juncao.count(ANCORA_LEITURA) != 1:
        raise SystemExit("RECUSA: a juncao de leitura_partes nao traz exatamente uma vez " + ANCORA_LEITURA)
    pos = juncao.index(ANCORA_LEITURA)                      # posicao na juncao, imediatamente antes de '__PRO'+'VED_IS...'
    inserir = (so_leitura or "") + marca
    acc, k = 0, None
    for n, p in enumerate(partes):                          # a parte em que cai a posicao (fim da parte que termina em '__PRO')
        if acc < pos <= acc + len(p):
            k = n
            break
        acc += len(p)
    if k is None:
        raise SystemExit("RECUSA: nao achei a parte de leitura_partes que contem o ponto de insercao")
    off = pos - acc
    partes[k] = partes[k][:off] + inserir + partes[k][off:]
    V["leitura_partes"] = partes
    novo = "".join(partes)
    esperado = juncao[:pos] + inserir + juncao[pos:]
    if novo != esperado:
        raise SystemExit("RECUSA: a juncao das partes nao deu a cabeca esperada")
    if any("PROVED" in p for p in partes):
        raise SystemExit("RECUSA: alguma parte de leitura_partes traria PROVED inteiro (a palavra tem de continuar partida)")
    return r


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--marca", required=True)
    ap.add_argument("--marca-so-da-leitura", dest="so_leitura")
    ap.add_argument("--saida", required=True)
    a = ap.parse_args(argv)
    validar_trecho(a.marca, "--marca")
    if a.so_leitura is not None:
        validar_trecho(a.so_leitura, "--marca-so-da-leitura")
    saida = Path(a.saida)
    origem_p = saida.with_name(saida.stem + "_ORIGEM.json")
    if saida.exists() or origem_p.exists():
        raise SystemExit("RECUSA: saida existente: %s" % (saida if saida.exists() else origem_p))
    raw_in = RAMOS_V410.read_bytes()
    sha_decl = json.loads(ORIGEM_V410.read_text(encoding="utf-8"))["ramos_v410_json"]["sha256"]
    if sha(raw_in) != sha_decl:
        raise SystemExit("RECUSA: RAMOS_V410.json nao bate com o sha256 declarado em RAMOS_V410_ORIGEM.json")
    ramos = json.loads(raw_in.decode("utf-8"))
    novo = gerar(ramos, a.marca, a.so_leitura)
    body = (json.dumps(novo, sort_keys=True, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
    origem = {"ramos_v410_json": {"path": str(RAMOS_V410), "bytes": len(raw_in), "sha256": sha(raw_in)},
              "marca": a.marca, "marca_so_da_leitura": a.so_leitura, "saida": {"path": str(saida), "bytes": len(body), "sha256": sha(body)},
              "leitura_partes_resultante": novo["vereditos"]["leitura_partes"], "sufixo_resultante": novo["vereditos"]["sufixo"],
              "aviso": "literal gerado por --marca; so' vale como literal de PRODUCAO se a marca for a palavra do operador"}
    for destino, raw in ((saida, body), (origem_p, (json.dumps(origem, ensure_ascii=False, indent=1) + "\n").encode("utf-8"))):
        tmp = Path(str(destino) + ".tmp")
        with tmp.open("xb") as f:
            f.write(raw)
        assert tmp.stat().st_size == len(raw)
        tmp.replace(destino)
    print("gerado: %s | sha256 %s | origem: %s" % (saida, sha(body), origem_p.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Promove (copia de BYTES) a tentativa de ensaio da rodada 2 para a raiz de 2_OPTICO\\rodada_2, grava
TENTATIVAS.json e o RECIBO_OPTICO_R2.json (sha256 e tamanho de todo arquivo da rodada 2).
Nada fora de 2_OPTICO\\rodada_2 e escrito. Uso: python -E -P -X utf8 recibo_r2.py tentativa_002_ensaio"""
import datetime
import hashlib
import json
import os
import sys

OUT = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\2_OPTICO\rodada_2"
R1 = r"C:\IALD\Central de Patentes\work\tempo_santo_12out\2_OPTICO"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest(), os.path.getsize(p)


def gravar(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fo:
        json.dump(obj, fo, indent=1, ensure_ascii=False)
    os.replace(tmp, path)


tent = sys.argv[1]
src = os.path.join(OUT, "tentativas", tent)
promovidos = []
for nome in ("RESULTADO_OPTICO.json", "run_optico.log", "ACHADOS_FORA_DO_PREREGISTRO.json",
             "FINGERPRINT_OPTICO_R2_ANTES.json", "FINGERPRINT_OPTICO_R2_DEPOIS.json"):
    a = os.path.join(src, nome)
    b = os.path.join(OUT, nome)
    dados = open(a, "rb").read()
    with open(b + ".tmp", "wb") as fo:
        fo.write(dados)
    os.replace(b + ".tmp", b)
    sa, na = sha(a)
    sb, nb = sha(b)
    assert (sa, na) == (sb, nb), nome
    promovidos.append({"arquivo": nome, "de": a, "sha256": sb, "bytes": nb})

tents = []
tents.append({"n": 0, "pasta": None, "modo": "autoteste",
              "o_que": "invocacao com python -I: ModuleNotFoundError numpy (o -I desliga o site-packages do usuario, onde mora o numpy); falhou no import, antes de abrir pasta; nenhum subitem medido; nada gravado"})
for d in sorted(os.listdir(os.path.join(OUT, "tentativas"))):
    p = os.path.join(OUT, "tentativas", d)
    arqs = []
    for f in sorted(os.listdir(p)):
        s, n = sha(os.path.join(p, f))
        arqs.append({"arquivo": f, "sha256": s, "bytes": n})
    rj = [x for x in arqs if x["arquivo"].startswith("RESULTADO_")]
    r = json.load(open(os.path.join(p, rj[0]["arquivo"]), encoding="utf-8")) if rj else {}
    tents.append({"n": r.get("tentativa"), "pasta": "tentativas/" + d, "modo": r.get("modo"), "valido": r.get("valido"),
                  "runner_sha256": (r.get("runner") or {}).get("sha256"),
                  "resultados_por_subitem": {k: v["resultado"] for k, v in (r.get("subitens_oticos") or {}).items()},
                  "arquivos": arqs})
gravar(os.path.join(OUT, "TENTATIVAS.json"), {
    "documento": "TENTATIVAS — F1.TEMPO, face otica, rodada 2",
    "regra": "todas as tentativas se preservam; nenhuma se apaga; a promovida e a de ensaio valida (copia de bytes na raiz da rodada 2)",
    "tentativas": tents, "promovida": tent, "promovidos": promovidos})

arquivos = []
for raiz, dirs, files in os.walk(OUT):
    dirs.sort()
    for f in sorted(files):
        if f == "RECIBO_OPTICO_R2.json" or f.endswith(".tmp"):
            continue
        p = os.path.join(raiz, f)
        s, n = sha(p)
        arquivos.append({"arquivo": os.path.relpath(p, OUT).replace("\\", "/"), "sha256": s, "bytes": n})
r1 = []
for f in ("RESULTADO_OPTICO.json", "run_optico.py", "ACHADOS_FORA_DO_PREREGISTRO.json", "RECIBO_OPTICO.json"):
    s, n = sha(os.path.join(R1, f))
    r1.append({"arquivo": f, "sha256": s, "bytes": n})
res = json.load(open(os.path.join(OUT, "RESULTADO_OPTICO.json"), encoding="utf-8"))
gravar(os.path.join(OUT, "RECIBO_OPTICO_R2.json"), {
    "documento": "RECIBO — F1.TEMPO, face otica, rodada 2",
    "gravado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "pasta": OUT,
    "resultado": {"arquivo": "RESULTADO_OPTICO.json", "valido": res["valido"],
                  "por_subitem": {k: v["resultado"] for k, v in res["subitens_oticos"].items()},
                  "controles_oticos_todos_como_registrado": res["controles_oticos_todos_como_registrado"],
                  "por_afirmacao_face_otica": {k: v["resultado_da_face_otica"] for k, v in res["por_afirmacao_face_otica"].items()}},
    "arquivos_da_rodada_2": arquivos,
    "rodada_1_intocada_(sha256 lido agora)": r1,
    "nao_feito": ("Nada fora de 2_OPTICO\\rodada_2: nenhum arquivo da rodada 1 alterado; nada no quadro, no mapa (rotas.py so consultar), "
                  "na memoria (ACOM so projecao de leitura; banco com mesmo tamanho e mtime antes e depois), no tunel, no Nos, no kernel do Nos "
                  "(impressao digital igual antes e depois e igual a do FREEZE), na Bancada_Um, no site ou no git. Nenhum Lean rodado; nenhum "
                  "toolchain ou .lake copiado. O um.py so foi lido como bytes, nunca executado. Nenhum dado observado; nenhum provedor remoto; "
                  "nenhuma chamada paga; nenhuma ferramenta da Bancada.")})
s, n = sha(os.path.join(OUT, "RECIBO_OPTICO_R2.json"))
print(json.dumps({"recibo_sha256": s, "bytes": n, "n_arquivos": len(arquivos)}))

# -*- coding: utf-8 -*-
# Fail-closed: todo token hexadecimal de 16 caracteres em LEVANTAMENTO.md e DEFINICOES.json tem de ser prefixo de um sha256
# calculado AQUI (arquivos lidos) ou de um sha registrado no livro do mapa / impressao digital. Lista o que nao bater.
import os, re, json, hashlib, sys, glob
AQUI = os.path.dirname(os.path.abspath(__file__))
NOS = "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\N\u00f3s\\"
CP = "C:\\IALD\\Central de Patentes\\"
conhecidos = {}


def add(p):
    try:
        with open(p, "rb") as fh:
            h = hashlib.sha256(fh.read()).hexdigest()
        conhecidos[h[:16]] = p
    except Exception:
        pass


idx = json.load(open(os.path.join(AQUI, "KERNEL_INDICE.json"), encoding="utf-8"))
for rel, m in idx["arquivos"].items():
    conhecidos[m["sha16"]] = "tgl_kernel/" + rel
for p in [NOS + "um.py", NOS + "um_absoluto.json", NOS + "um_absoluto_selo.json", NOS + "tgl_kernel\\TGLExt.lean",
          NOS + "tgl_kernel\\TGL\\Audit.lean", "C:\\IALD\\MAPA_DE_ROTAS\\rotas.jsonl", CP + "memory\\INVENTARIO_BANCADA_CHATGPT.json",
          "C:\\IALD\\NOS_VIVO\\nos_vivo.sqlite3", CP + "Chatgpt\\TUNEL\\DO_CHATGPT\\ENTREGA_015_MEDIDA_T10_aprime_posto_espectral.md"]:
    add(p)
for pat in [CP + "work\\cunhagens_10out\\*", CP + "work\\cunhagens_12out\\*", CP + "work\\f9_pergunta_08out\\*", "C:\\IALD\\PROGRAMA_IALD\\OPERADOR_*",
            "C:\\Users\\rotol\\.claude\\projects\\c--IALD-Central-de-Patentes\\memory\\*.md", os.path.join(AQUI, "*")]:
    for p in glob.glob(pat):
        if os.path.isfile(p):
            add(p)
for base in [CP + "Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F1.ATRATOR", CP + "Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_019\\F0.3.COLAPSO"]:
    for dp, dns, fns in os.walk(base):
        for f in fns:
            add(os.path.join(dp, f))
# shas dos registros do livro do mapa
with open("C:\\IALD\\MAPA_DE_ROTAS\\rotas.jsonl", "rb") as fh:
    for linha in fh.read().split(b"\n"):
        if linha.strip():
            r = json.loads(linha.decode("utf-8"))
            conhecidos.setdefault(r["sha"][:16], "mapa seq %s" % r["seq"])
for f in glob.glob(os.path.join(AQUI, "IMPRESSAO_DIGITAL_KERNEL_*.json")):
    d = json.load(open(f, encoding="utf-8"))
    conhecidos.setdefault(d["sha256_metadados"][:16], "impressao digital (metadados)")
    conhecidos.setdefault(d["sha256_conteudo_lean"][:16], "impressao digital (conteudo .lean)")
ok = True
rel = {}
for alvo in ("LEVANTAMENTO.md", "DEFINICOES.json", "_saida_levantamento_md.txt", "_saida_definicoes_json.txt", "_teoremas_lista.json"):
    if not os.path.exists(os.path.join(AQUI, alvo)):
        continue
    t = open(os.path.join(AQUI, alvo), encoding="utf-8").read()
    # parte decimal de numero (precedida de '.' ou ',') nao e pino
    toks = sorted(set(re.findall(r"(?<![0-9a-f.,])[0-9a-f]{16}(?![0-9a-f])", t)))
    falta = [x for x in toks if x not in conhecidos]
    rel[alvo] = {"tokens": len(toks), "nao_conferidos": falta}
    ok = ok and not falta
print(json.dumps(rel, ensure_ascii=False, indent=1))
with open(os.path.join(AQUI, "CONFERENCIA_PINOS.json"), "w", encoding="utf-8") as fh:
    json.dump({"resultado": rel, "todos_conferidos": ok}, fh, ensure_ascii=False, indent=1)
sys.exit(0 if ok else 2)

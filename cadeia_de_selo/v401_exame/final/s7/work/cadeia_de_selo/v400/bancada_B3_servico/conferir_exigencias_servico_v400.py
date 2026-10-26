# -*- coding: utf-8 -*-
"""conferir_exigencias_servico_v400.py -- SO LEITURA E SO ESTATICO (ast + texto): NADA e' executado (nem parada, nem religamento, nem evento).
Confere nos tres scripts derivados da v400 (evento_c1_b3_v400.py, recibo_parada_v400.py, recibo_religamento_v400.py):
  (a) parada e religamento EXIGEM V400_AUTORIZACAO_OPERADOR: a atribuicao `AUT = os.environ.get("V400_AUTORIZACAO_OPERADOR", "").strip()` e o `assert AUT, ...` seguinte sao as UNICAS coisas
      executaveis antes de qualquer E/S (socket, subprocess, open, urlopen, json.load/dumps): se a variavel falta, o script cai no assert antes de tocar em qualquer coisa; nenhum nome da versao anterior sobrou;
  (b) o evento le o candidato_sha16 de ESPERADOS_v400.json em tempo de execucao: o `assert os.path.isfile(ESP)` e o assert do candidato vem ANTES do subprocess.run que anota no quadro; nenhum hash literal;
      ESPERADOS_v400.json NAO existe agora (medido), logo o evento abortaria no assert;
  (c) as chaves e a ordem do dict `rec` dos dois recibos = as dos recibos REAIS da v398 (RECIBO_PARADA_v398.json, RECIBO_RELIGAMENTO_v398.json);
  (d) os recibos da v400 ainda NAO existem (nada foi executado); os insumos que os scripts leem existem (RECIBO_RELIGAMENTO_v398.json e o recibo do B(n) da v398).
Grava CONFERENCIA_EXIGENCIAS_SERVICO_v400.json ao lado (nao sobrescreve). uso: python -I -B -X utf8 conferir_exigencias_servico_v400.py"""
import ast
import glob
import hashlib
import json
import os
import re
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V = os.path.dirname(HERE)
V8 = os.path.join(os.path.dirname(V), "v398")
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()

IO = {"socket", "subprocess", "open", "urlopen", "load", "loads", "dump", "dumps", "replace", "run", "connect_ex", "write", "read", "glob", "isfile", "exists"}
checks = []


def chk(nome, ok, observado, esperado=True):
    checks.append({"nome": nome, "ok": bool(ok), "observado": observado, "esperado": esperado})


def chamadas(no):
    """nomes das chamadas (a.b.c -> 'c' e 'a.b.c') dentro de um no."""
    out = []
    for n in ast.walk(no):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                out.append(f.id)
            elif isinstance(f, ast.Attribute):
                out.append(f.attr)
    return out


def corpo(nome):
    p = os.path.join(HERE, nome)
    txt = open(p, encoding="utf-8").read()
    return p, txt, ast.parse(txt)


def e_assert_aut(n):
    return isinstance(n, ast.Assert) and isinstance(n.test, ast.Name) and n.test.id == "AUT"


def e_atrib_aut(n):
    if not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "AUT" for t in n.targets)):
        return False
    u = ast.unparse(n.value).replace("'", '"')      # ast.unparse escreve aspas simples
    return u == 'os.environ.get("V400_AUTORIZACAO_OPERADOR", "").strip()'


def chaves_do_rec(arv):
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) and any(isinstance(t, ast.Name) and t.id == "rec" for t in n.targets):
            return [k.value for k in n.value.keys if isinstance(k, ast.Constant)]
    return None


reais = {"recibo_parada_v400.py": os.path.join(V8, "bancada_B3_servico", "RECIBO_PARADA_v398.json"), "recibo_religamento_v400.py": os.path.join(V8, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v398.json")}
saidas = {"recibo_parada_v400.py": "RECIBO_PARADA_v400.json", "recibo_religamento_v400.py": "RECIBO_RELIGAMENTO_v400.json"}
arquivos = {}
for nome in ("recibo_parada_v400.py", "recibo_religamento_v400.py"):
    p, txt, arv = corpo(nome)
    arquivos[nome] = {"path": p, "sha256": sha(p), "bytes": os.path.getsize(p)}
    mod = arv.body
    i_atrib = next((i for i, n in enumerate(mod) if e_atrib_aut(n)), None)
    i_assert = next((i for i, n in enumerate(mod) if e_assert_aut(n)), None)
    chk(nome + ": ha a atribuicao AUT = os.environ.get(V400_AUTORIZACAO_OPERADOR).strip()", i_atrib is not None, i_atrib)
    chk(nome + ": o assert AUT vem logo depois da atribuicao (sem nada entre)", i_atrib is not None and i_assert == i_atrib + 1, [i_atrib, i_assert])
    antes = mod[:i_assert] if i_assert is not None else mod
    io_antes = sorted({c for n in antes for c in chamadas(n) if c in IO})
    chk(nome + ": nenhuma chamada de E/S antes do assert AUT (so imports, D e AUT)", i_assert is not None and not io_antes, io_antes, [])
    chk(nome + ": V400_AUTORIZACAO_OPERADOR aparece 2 vezes (leitura e mensagem do assert)", txt.count("V400_AUTORIZACAO_OPERADOR") == 2, txt.count("V400_AUTORIZACAO_OPERADOR"), 2)
    chk(nome + ": nenhum nome da versao anterior sobrou (V398_AUTORIZACAO_OPERADOR, RECIBO_*_v398.json como saida)", "V398_AUTORIZACAO_OPERADOR" not in txt and ('"%s"' % saidas[nome].replace("v400", "v398")) not in txt,
        ["V398_AUTORIZACAO_OPERADOR" in txt, ('"%s"' % saidas[nome].replace("v400", "v398")) in txt], [False, False])
    chk(nome + ": a frase 'por autorizacao geral do operador' nao existe", "por autorizacao geral do operador" not in txt, "por autorizacao geral do operador" in txt, False)
    chk(nome + ": grava so' em " + saidas[nome] + " e recusa sobrescrever (assert not os.path.exists)", ('"%s"' % saidas[nome]) in txt and "assert not os.path.exists(p)" in txt,
        [('"%s"' % saidas[nome]) in txt, "assert not os.path.exists(p)" in txt])
    k_novo, k_real = chaves_do_rec(arv), list(json.load(open(reais[nome], encoding="utf-8")).keys())
    chk(nome + ": chaves do dict rec (ordem) = chaves do recibo REAL da v398", k_novo == k_real, [k_novo, k_real], "listas iguais")
    chk(nome + ": o recibo da v400 ainda nao existe (nada foi executado)", not os.path.exists(os.path.join(HERE, saidas[nome])), os.path.exists(os.path.join(HERE, saidas[nome])), False)
# ---- o evento
pe, te, ae = corpo("evento_c1_b3_v400.py")
arquivos["evento_c1_b3_v400.py"] = {"path": pe, "sha256": sha(pe), "bytes": os.path.getsize(pe)}
mod = ae.body


def idx(pred):
    return next((i for i, n in enumerate(mod) if pred(n)), None)


i_isfile = idx(lambda n: isinstance(n, ast.Assert) and "os.path.isfile(ESP)" in ast.unparse(n.test))
i_cand = idx(lambda n: isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CAND16" for t in n.targets))
i_conf = idx(lambda n: isinstance(n, ast.Assert) and "startswith(CAND16)" in ast.unparse(n.test))
i_run = idx(lambda n: isinstance(n, ast.Assign) and "subprocess.run" in ast.unparse(n.value))
chk("evento: assert os.path.isfile(ESP) < leitura de CAND16 < assert startswith(CAND16) < subprocess.run (anotar no quadro)", None not in (i_isfile, i_cand, i_conf, i_run) and i_isfile < i_cand < i_conf < i_run,
    [i_isfile, i_cand, i_conf, i_run], "ordem crescente")
chk("evento: ESP = ..\\ESPERADOS_v400.json e le o campo candidato_sha16", 'os.path.join(D, "..", "ESPERADOS_v400.json")' in te and '["candidato_sha16"]' in te, True)
chk("evento: nenhum hash literal (16 a 64 hex entre aspas)", re.search(r'"[0-9a-f]{16,64}"', te) is None, re.findall(r'"[0-9a-f]{16,64}"', te), [])
chk("evento: V400_AUTORIZACAO_OPERADOR nao e usada (o evento nao exige a variavel; so' parada e religamento)", "V400_AUTORIZACAO_OPERADOR" not in te, "V400_AUTORIZACAO_OPERADOR" in te, False)
chk("evento: versao v400, acao sincronizacao, unidade F0.6, tipo SINCRONIZACAO_BANCADA", '"versao": "v400"' in te and '"acao": "sincronizacao"' in te and '"unidade": "F0.6"' in te and '"SINCRONIZACAO_BANCADA"' in te, True)
esp_p = os.path.join(V, "ESPERADOS_v400.json")
cand16_ = json.load(open(esp_p, encoding="utf-8"))["candidato_sha16"] if os.path.exists(esp_p) else None
um_nos16_ = sha(os.path.join(NOS, "um.py"))[:16]
chk("ESPERADOS_v400.json existe (gerado pelo ensaio) e o um.py do Nos AINDA NAO e o candidato dele: o evento ABORTARIA hoje no assert do candidato (antes de anotar no quadro)", bool(cand16_) and um_nos16_ != cand16_, [cand16_, um_nos16_], "diferentes")
# ---- insumos que os scripts leem
rel8 = os.path.join(V8, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v398.json")
bn8 = sorted(glob.glob(os.path.join(V8, "bancada_B3", "RECIBO_SINCRONIZACAO_v398_*.json")))
chk("insumo da parada: RECIBO_RELIGAMENTO_v398.json existe", os.path.isfile(rel8), rel8)
chk("insumo do religamento: um unico RECIBO_SINCRONIZACAO_v398_*.json em v398\\bancada_B3", len(bn8) == 1, [os.path.basename(x) for x in bn8], 1)
bn9 = sorted(glob.glob(os.path.join(V, "bancada_B3", "RECIBO_SINCRONIZACAO_v400_*.json")))
chk("o recibo do B(n) da v400 ainda nao existe (v400\\bancada_B3 vazia de recibo)", len(bn9) == 0, [os.path.basename(x) for x in bn9], [])
res = {"contrato": "CONFERENCIA_EXIGENCIAS_SERVICO_v400", "como": "estatica (ast + texto); nada foi executado; a producao nao foi tocada", "script": {"path": os.path.abspath(__file__), "sha256": sha(os.path.abspath(__file__))},
       "arquivos": arquivos, "condicoes": checks, "n_condicoes": len(checks), "n_condicoes_ok": sum(1 for c in checks if c["ok"]),
       "exigem_V400_AUTORIZACAO_OPERADOR": {"recibo_parada_v400.py": True, "recibo_religamento_v400.py": True} if all(c["ok"] for c in checks if "AUT" in c["nome"] or "V400_AUTORIZACAO_OPERADOR" in c["nome"]) else "VER condicoes",
       "escopo": "NOT_FALSIFIED nao e creditacao; o gate nao se move"}
dest = os.path.join(HERE, "CONFERENCIA_EXIGENCIAS_SERVICO_v400.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print("%d/%d condicoes ok" % (res["n_condicoes_ok"], res["n_condicoes"]), "| exigem:", res["exigem_V400_AUTORIZACAO_OPERADOR"])
for c in checks:
    if not c["ok"]:
        print("FALHA:", c["nome"], c["observado"])
print(dest, sha(dest)[:16])
sys.exit(0 if res["n_condicoes_ok"] == res["n_condicoes"] else 1)

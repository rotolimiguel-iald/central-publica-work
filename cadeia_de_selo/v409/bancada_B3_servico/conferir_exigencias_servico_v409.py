# -*- coding: utf-8 -*-
# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] confere a ORDEM da v409 (05/11/2026, OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt), as datas anteriores (01 a 04/11) ausentes e o AUT do orquestrador com o sha16 lido, a frase e a data
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v409) molde v408/bancada_B3_servico/conferir_exigencias_servico_v408.py (rotulos subidos por _bump_copia_v409.py; diff em bump/). Adaptado (v409): a autorizacao conferida e' a ORDEM da v409 (fala de 05/11/2026; sha16 calculado do arquivo aqui e nos scripts); nenhuma data de autorizacao anterior (01/11, 02/11, 03/11) pode sobrar nos scripts;
# o insumo da parada segue sendo o RECIBO_RELIGAMENTO_v408.json (pid e no_ar_desde); o evento aborta no assert do candidato enquanto o Nos for a v408.
"""conferir_exigencias_servico_v409.py -- SO LEITURA E SO ESTATICO (ast + texto): NADA e' executado (nem parada, nem religamento, nem evento).
Confere nos tres scripts derivados da v409 (evento_c1_b3_v409.py, recibo_parada_v409.py, recibo_religamento_v409.py):
  (a) parada e religamento EXIGEM V409_AUTORIZACAO_OPERADOR: a atribuicao `AUT = os.environ.get("V409_AUTORIZACAO_OPERADOR", "").strip()` e o `assert AUT, ...` seguinte sao as UNICAS coisas
      executaveis antes de qualquer E/S (socket, subprocess, open, urlopen, json.load/dumps): se a variavel falta, o script cai no assert antes de tocar em qualquer coisa; nenhum nome da versao anterior sobrou;
  (b) o evento le o candidato_sha16 de ESPERADOS_v409.json em tempo de execucao: o `assert os.path.isfile(ESP)` e o assert do candidato vem ANTES do subprocess.run que anota no quadro; nenhum hash literal;
      enquanto o um.py do Nos nao for o candidato dele (hoje a v408), o evento aborta no assert do candidato, ANTES de anotar (se ESPERADOS_v409.json faltasse, abortaria no isfile);
  (c) as chaves e a ordem do dict `rec` dos dois recibos = as dos recibos REAIS da v408 (RECIBO_PARADA_v408.json, RECIBO_RELIGAMENTO_v408.json);
  (d) os recibos da v409 ainda NAO existem (nada foi executado); os insumos que os scripts leem existem (RECIBO_RELIGAMENTO_v408.json com pid e no_ar_desde, e o recibo do B(n) da v408);
  (e) a autorizacao e' a ORDEM da v409, do operador, de 05/11/2026 («Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados»): depois do assert AUT, parada e religamento conferem o texto passado contra a fala (o sha16 vem do ARQUIVO da fala, lido na hora; a frase tem de estar no arquivo e no texto); nenhum texto, data ou hash de autorizacao anterior (01/11, 02/11, 03/11) sobrou nos scripts;
      o AUT que o orquestrador passa (orquestrador/pos_treino_v409.py) carrega o sha16 do arquivo da fala e a frase; o religamento confere o deployment servido (B<n>-v409-<data>-R1, o que o APLICAR deixou) e a parada le o recibo do religamento da v408 (o ultimo religamento conhecido).
Grava CONFERENCIA_EXIGENCIAS_SERVICO_v409.json ao lado (nao sobrescreve). uso: python -I -B -X utf8 conferir_exigencias_servico_v409.py"""
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
V14 = os.path.join(os.path.dirname(V), "v408")
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
    return u == 'os.environ.get("V409_AUTORIZACAO_OPERADOR", "").strip()'


def chaves_do_rec(arv):
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) and any(isinstance(t, ast.Name) and t.id == "rec" for t in n.targets):
            return [k.value for k in n.value.keys if isinstance(k, ast.Constant)]
    return None


ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", "OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes_verbatim.txt")
FRASE_DA_ORDEM = "Prossigamos para a próxima verão do um.py; concordo com todos os nomes que foram dados"
reais = {"recibo_parada_v409.py": os.path.join(V14, "bancada_B3_servico", "RECIBO_PARADA_v408.json"), "recibo_religamento_v409.py": os.path.join(V14, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v408.json")}
saidas = {"recibo_parada_v409.py": "RECIBO_PARADA_v409.json", "recibo_religamento_v409.py": "RECIBO_RELIGAMENTO_v409.json"}
arquivos = {}
for nome in ("recibo_parada_v409.py", "recibo_religamento_v409.py"):
    p, txt, arv = corpo(nome)
    arquivos[nome] = {"path": p, "sha256": sha(p), "bytes": os.path.getsize(p)}
    mod = arv.body
    i_atrib = next((i for i, n in enumerate(mod) if e_atrib_aut(n)), None)
    i_assert = next((i for i, n in enumerate(mod) if e_assert_aut(n)), None)
    chk(nome + ": ha a atribuicao AUT = os.environ.get(V409_AUTORIZACAO_OPERADOR).strip()", i_atrib is not None, i_atrib)
    chk(nome + ": o assert AUT vem logo depois da atribuicao (sem nada entre)", i_atrib is not None and i_assert == i_atrib + 1, [i_atrib, i_assert])
    antes = mod[:i_assert] if i_assert is not None else mod
    io_antes = sorted({c for n in antes for c in chamadas(n) if c in IO})
    chk(nome + ": nenhuma chamada de E/S antes do assert AUT (so imports, D e AUT)", i_assert is not None and not io_antes, io_antes, [])
    chk(nome + ": V409_AUTORIZACAO_OPERADOR aparece 2 vezes (leitura e mensagem do assert)", txt.count("V409_AUTORIZACAO_OPERADOR") == 2, txt.count("V409_AUTORIZACAO_OPERADOR"), 2)
    chk(nome + ": nenhum nome da versao anterior sobrou (V408_AUTORIZACAO_OPERADOR, RECIBO_*_v408.json como saida)", "V408_AUTORIZACAO_OPERADOR" not in txt and ('"%s"' % saidas[nome].replace("v409", "v408")) not in txt,
        ["V408_AUTORIZACAO_OPERADOR" in txt, ('"%s"' % saidas[nome].replace("v409", "v408")) in txt], [False, False])
    chk(nome + ": a frase 'por autorizacao geral do operador' nao existe", "por autorizacao geral do operador" not in txt, "por autorizacao geral do operador" in txt, False)
    chk(nome + ": grava so' em " + saidas[nome] + " e recusa sobrescrever (assert not os.path.exists)", ('"%s"' % saidas[nome]) in txt and "assert not os.path.exists(p)" in txt,
        [('"%s"' % saidas[nome]) in txt, "assert not os.path.exists(p)" in txt])
    k_novo, k_real = chaves_do_rec(arv), list(json.load(open(reais[nome], encoding="utf-8")).keys())
    chk(nome + ": chaves do dict rec (ordem) = chaves do recibo REAL da v408", k_novo == k_real, [k_novo, k_real], "listas iguais")
    m_ord = re.search(r'ORDEM = os\.path\.join\(D, "\.\.", "\.\.", "\.\.", "cunhagens_13out", "([^"]+)"\)', txt)   # (v409) a subida mecanica trocou este nome por um com v409 que nao existe: confere que o arquivo que o script abre EXISTE
    chk(nome + ": o arquivo da fala que o script abre (ORDEM) existe em work\\cunhagens_13out e e' o mesmo que este conferidor usa", bool(m_ord) and os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", m_ord.group(1))) and m_ord.group(1) == os.path.basename(ORDEM_ARQ), m_ord.group(1) if m_ord else None)
    i_ordem = next((i for i, n in enumerate(mod) if isinstance(n, ast.Assert) and "ORDEM_SHA16" in ast.unparse(n.test)), None)
    chk(nome + ": a ordem de 05/11 (a ordem da v409) e' conferida: o assert com ORDEM_SHA16 (lido do ARQUIVO da fala) vem DEPOIS do assert AUT", i_ordem is not None and i_assert is not None and i_ordem > i_assert and "cunhagens_13out" in txt and "OPERADOR_05nov_prossigamos_v409_concordo_com_os_nomes" in txt and "hashlib.sha256(ORDEM_BYTES)" in txt, [i_assert, i_ordem])
    chk(nome + ": nenhum texto, data ou hash de autorizacao anterior sobrou (01/11/2026 a 04/11/2026; nenhum sha de 16 hex digitado)", all(d_ not in txt for d_ in ("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026")) and re.search(r"[0-9a-f]{16}", txt) is None, [[d_ in txt for d_ in ("01/11/2026", "02/11/2026", "03/11/2026", "04/11/2026")], re.findall(r"[0-9a-f]{16}", txt)], [[False, False, False, False], []])
    if nome == "recibo_parada_v409.py":
        chk(nome + ": le o recibo do religamento da v408 (RECIBO_RELIGAMENTO_v408.json: pid e no_ar_desde), nao depende de RELIGAMENTO_PREVIO_02nov.json (que nao existe na v409), e o PID parado vem de V409_PID_PARADO", "RECIBO_RELIGAMENTO_v408.json" in txt and 'rel408["no_ar_desde"]' in txt and "RELIGAMENTO_PREVIO" not in txt.split('"""', 2)[2] and "V409_PID_PARADO" in txt and "V409_PID_PARADO_CRIADO" in txt, True)
    else:
        chk(nome + ": confere o deployment servido contra o do APLICAR (B<n>-v409-<data>-R1; n = a geracao anterior + 1)", "dep_esp" in txt and "-v409-" in txt and 'c.get("deployment_id") == dep_esp' in txt, True)
    chk(nome + ": o recibo da v409 ainda nao existe (nada foi executado)", not os.path.exists(os.path.join(HERE, saidas[nome])), os.path.exists(os.path.join(HERE, saidas[nome])), False)
# ---- o evento
pe, te, ae = corpo("evento_c1_b3_v409.py")
arquivos["evento_c1_b3_v409.py"] = {"path": pe, "sha256": sha(pe), "bytes": os.path.getsize(pe)}
mod = ae.body


def idx(pred):
    return next((i for i, n in enumerate(mod) if pred(n)), None)


i_isfile = idx(lambda n: isinstance(n, ast.Assert) and "os.path.isfile(ESP)" in ast.unparse(n.test))
i_cand = idx(lambda n: isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CAND16" for t in n.targets))
i_conf = idx(lambda n: isinstance(n, ast.Assert) and "startswith(CAND16)" in ast.unparse(n.test))
i_run = idx(lambda n: isinstance(n, ast.Assign) and "subprocess.run" in ast.unparse(n.value))
chk("evento: assert os.path.isfile(ESP) < leitura de CAND16 < assert startswith(CAND16) < subprocess.run (anotar no quadro)", None not in (i_isfile, i_cand, i_conf, i_run) and i_isfile < i_cand < i_conf < i_run,
    [i_isfile, i_cand, i_conf, i_run], "ordem crescente")
chk("evento: ESP = ..\\ESPERADOS_v409.json e le o campo candidato_sha16", 'os.path.join(D, "..", "ESPERADOS_v409.json")' in te and '["candidato_sha16"]' in te, True)
chk("evento: nenhum hash literal (16 a 64 hex entre aspas)", re.search(r'"[0-9a-f]{16,64}"', te) is None, re.findall(r'"[0-9a-f]{16,64}"', te), [])
chk("evento: V409_AUTORIZACAO_OPERADOR nao e usada (o evento nao exige a variavel; so' parada e religamento)", "V409_AUTORIZACAO_OPERADOR" not in te, "V409_AUTORIZACAO_OPERADOR" in te, False)
chk("evento: versao v409, acao sincronizacao, unidade F0.6, tipo SINCRONIZACAO_BANCADA", '"versao": "v409"' in te and '"acao": "sincronizacao"' in te and '"unidade": "F0.6"' in te and '"SINCRONIZACAO_BANCADA"' in te, True)
esp_p = os.path.join(V, "ESPERADOS_v409.json")
cand16_ = json.load(open(esp_p, encoding="utf-8"))["candidato_sha16"] if os.path.exists(esp_p) else None
um_nos16_ = sha(os.path.join(NOS, "um.py"))[:16]
chk("ESPERADOS_v409.json AUSENTE (o evento abortaria no assert os.path.isfile) ou presente com o um.py do Nos AINDA NAO igual ao candidato dele (abortaria no assert do candidato): em qualquer dos dois estados o evento aborta ANTES de anotar no quadro", cand16_ is None or um_nos16_ != cand16_, [cand16_, um_nos16_], "ausente, ou diferentes")
# ---- a ordem do operador de 05/11 (a ordem da v409) e o AUT do orquestrador
ord_ok = os.path.isfile(ORDEM_ARQ)
ord_txt = open(ORDEM_ARQ, encoding="utf-8").read() if ord_ok else ""
ord16 = sha(ORDEM_ARQ)[:16] if ord_ok else None
chk("a fala do operador de 05/11 (a ordem da v409: prossigamos para a proxima versao do um.py; a ratificacao dos nomes) existe e traz a frase", ord_ok and FRASE_DA_ORDEM in ord_txt, [ord_ok, ord16])
aut_orq = None
for n_ in ast.parse(open(os.path.join(V, "orquestrador", "pos_treino_v409.py"), encoding="utf-8").read()).body:
    if isinstance(n_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == "AUT" for t_ in n_.targets):
        try:
            aut_orq = ast.literal_eval(n_.value)
        except ValueError:   # (v409) o AUT e' MONTADO do delta (sha16 e frase lidos de delta_v409): avalia-se SO' a expressao do AUT, com o delta desta pasta e a frase dele, sem builtins
            import importlib.util as _ilu9
            _sp9 = _ilu9.spec_from_file_location("delta_v409_conferir_servico", os.path.join(V, "delta_v409.py")); _dl9 = _ilu9.module_from_spec(_sp9); _sp9.loader.exec_module(_dl9)
            aut_orq = eval(compile(ast.Expression(n_.value), "AUT_do_orquestrador", "eval"), {"__builtins__": {}}, {"_DL": _dl9, "AUT_FRASE": _dl9.FRASE_ORDEM_V409})
chk("o AUT do orquestrador (pos_treino_v409.py) e' a ordem de 05/11 (a ordem da v409): traz o sha16 do arquivo da fala (calculado aqui), a frase e a data, e nenhum texto de 01/11", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and "05/11/2026" in aut_orq and "01/11/2026" not in aut_orq, [ord16, bool(aut_orq)])
# ---- insumos que os scripts leem
rel8 = os.path.join(V14, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v408.json")
bn8 = sorted(glob.glob(os.path.join(V14, "bancada_B3", "RECIBO_SINCRONIZACAO_v408_*.json")))
chk("insumo da parada: RECIBO_RELIGAMENTO_v408.json existe, e' da porta 18777 e traz pid, no_ar_desde e hora_recibo (o ultimo religamento conhecido; a v409 nao tem RELIGAMENTO_PREVIO)", os.path.isfile(rel8) and (lambda d_: d_.get("porta") == 18777 and str(d_.get("pid", "")).isdigit() and bool(d_.get("no_ar_desde")) and bool(d_.get("hora_recibo")))(json.load(open(rel8, encoding="utf-8"))), rel8)
chk("insumo do religamento: um unico RECIBO_SINCRONIZACAO_v408_*.json em v408\\bancada_B3", len(bn8) == 1, [os.path.basename(x) for x in bn8], 1)
bn9 = sorted(glob.glob(os.path.join(V, "bancada_B3", "RECIBO_SINCRONIZACAO_v409_*.json")))
chk("o recibo do B(n) da v409 ainda nao existe (v409\\bancada_B3 vazia de recibo)", len(bn9) == 0, [os.path.basename(x) for x in bn9], [])
res = {"contrato": "CONFERENCIA_EXIGENCIAS_SERVICO_v409", "como": "estatica (ast + texto); nada foi executado; a producao nao foi tocada", "script": {"path": os.path.abspath(__file__), "sha256": sha(os.path.abspath(__file__))},
       "arquivos": arquivos, "condicoes": checks, "n_condicoes": len(checks), "n_condicoes_ok": sum(1 for c in checks if c["ok"]),
       "exigem_V409_AUTORIZACAO_OPERADOR": {"recibo_parada_v409.py": True, "recibo_religamento_v409.py": True} if all(c["ok"] for c in checks if "AUT" in c["nome"] or "V409_AUTORIZACAO_OPERADOR" in c["nome"]) else "VER condicoes",
       "escopo": "NOT_FALSIFIED nao e creditacao; o gate nao se move"}
dest = os.path.join(HERE, "CONFERENCIA_EXIGENCIAS_SERVICO_v409.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print("%d/%d condicoes ok" % (res["n_condicoes_ok"], res["n_condicoes"]), "| exigem:", res["exigem_V409_AUTORIZACAO_OPERADOR"])
for c in checks:
    if not c["ok"]:
        print("FALHA:", c["nome"], c["observado"])
print(dest, sha(dest)[:16])
sys.exit(0 if res["n_condicoes_ok"] == res["n_condicoes"] else 1)

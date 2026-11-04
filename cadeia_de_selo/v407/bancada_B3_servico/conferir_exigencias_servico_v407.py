# -*- coding: utf-8 -*-
# [ADAPTADO v407, 03/11/2026] molde v406/bancada_B3_servico/conferir_exigencias_servico_v406.py (rotulos subidos por _bump_copia_v407.py; diff em bump/). Corrigido a mao: (1) ORDEM_ARQ apontava para um arquivo com v407 no nome que NAO existe (o da fala de 02/11 tem v406 no nome); (2) a v407 nao tem
# RELIGAMENTO_PREVIO_02nov.json (era da v406): o insumo da parada passa a ser o RECIBO_RELIGAMENTO_v406.json (pid e no_ar_desde); (3) «autorizacao da v406 sobrando» virou «da v405» (a de 01/11 foi a da v405); (4) a docstring dizia que ESPERADOS_v407.json nao existe: existe, e o evento aborta no assert do candidato.
"""conferir_exigencias_servico_v407.py -- SO LEITURA E SO ESTATICO (ast + texto): NADA e' executado (nem parada, nem religamento, nem evento).
Confere nos tres scripts derivados da v407 (evento_c1_b3_v407.py, recibo_parada_v407.py, recibo_religamento_v407.py):
  (a) parada e religamento EXIGEM V407_AUTORIZACAO_OPERADOR: a atribuicao `AUT = os.environ.get("V407_AUTORIZACAO_OPERADOR", "").strip()` e o `assert AUT, ...` seguinte sao as UNICAS coisas
      executaveis antes de qualquer E/S (socket, subprocess, open, urlopen, json.load/dumps): se a variavel falta, o script cai no assert antes de tocar em qualquer coisa; nenhum nome da versao anterior sobrou;
  (b) o evento le o candidato_sha16 de ESPERADOS_v407.json em tempo de execucao: o `assert os.path.isfile(ESP)` e o assert do candidato vem ANTES do subprocess.run que anota no quadro; nenhum hash literal;
      enquanto o um.py do Nos nao for o candidato dele (hoje a v406), o evento aborta no assert do candidato, ANTES de anotar (se ESPERADOS_v407.json faltasse, abortaria no isfile);
  (c) as chaves e a ordem do dict `rec` dos dois recibos = as dos recibos REAIS da v406 (RECIBO_PARADA_v406.json, RECIBO_RELIGAMENTO_v406.json);
  (d) os recibos da v407 ainda NAO existem (nada foi executado); os insumos que os scripts leem existem (RECIBO_RELIGAMENTO_v406.json com pid e no_ar_desde, e o recibo do B(n) da v406);
  (e) a autorizacao e' a ordem do operador de 02/11/2026 (o arquivo da fala tem v406 no nome: a ordem foi dada na v406 e vale para «a nova versao»): depois do assert AUT, parada e religamento conferem o texto passado contra a fala (o sha16 vem do ARQUIVO da fala, lido na hora; a frase tem de estar no arquivo e no texto); nenhum texto, data ou hash de autorizacao da v405 (01/11) sobrou nos scripts;
      o AUT que o orquestrador passa (orquestrador/pos_treino_v407.py) carrega o sha16 do arquivo da fala e a frase; o religamento confere o deployment servido (B<n>-v407-<data>-R1, o que o APLICAR deixou) e a parada le o recibo do religamento da v406 (o ultimo religamento conhecido).
Grava CONFERENCIA_EXIGENCIAS_SERVICO_v407.json ao lado (nao sobrescreve). uso: python -I -B -X utf8 conferir_exigencias_servico_v407.py"""
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
V14 = os.path.join(os.path.dirname(V), "v406")
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
    return u == 'os.environ.get("V407_AUTORIZACAO_OPERADOR", "").strip()'


def chaves_do_rec(arv):
    for n in ast.walk(arv):
        if isinstance(n, ast.Assign) and isinstance(n.value, ast.Dict) and any(isinstance(t, ast.Name) and t.id == "rec" for t in n.targets):
            return [k.value for k in n.value.keys if isinstance(k, ast.Constant)]
    return None


ORDEM_ARQ = os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", "OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt")
FRASE_DA_ORDEM = "compile a nova versão do um.py, rode, publique e atualize tudo por favor"
reais = {"recibo_parada_v407.py": os.path.join(V14, "bancada_B3_servico", "RECIBO_PARADA_v406.json"), "recibo_religamento_v407.py": os.path.join(V14, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v406.json")}
saidas = {"recibo_parada_v407.py": "RECIBO_PARADA_v407.json", "recibo_religamento_v407.py": "RECIBO_RELIGAMENTO_v407.json"}
arquivos = {}
for nome in ("recibo_parada_v407.py", "recibo_religamento_v407.py"):
    p, txt, arv = corpo(nome)
    arquivos[nome] = {"path": p, "sha256": sha(p), "bytes": os.path.getsize(p)}
    mod = arv.body
    i_atrib = next((i for i, n in enumerate(mod) if e_atrib_aut(n)), None)
    i_assert = next((i for i, n in enumerate(mod) if e_assert_aut(n)), None)
    chk(nome + ": ha a atribuicao AUT = os.environ.get(V407_AUTORIZACAO_OPERADOR).strip()", i_atrib is not None, i_atrib)
    chk(nome + ": o assert AUT vem logo depois da atribuicao (sem nada entre)", i_atrib is not None and i_assert == i_atrib + 1, [i_atrib, i_assert])
    antes = mod[:i_assert] if i_assert is not None else mod
    io_antes = sorted({c for n in antes for c in chamadas(n) if c in IO})
    chk(nome + ": nenhuma chamada de E/S antes do assert AUT (so imports, D e AUT)", i_assert is not None and not io_antes, io_antes, [])
    chk(nome + ": V407_AUTORIZACAO_OPERADOR aparece 2 vezes (leitura e mensagem do assert)", txt.count("V407_AUTORIZACAO_OPERADOR") == 2, txt.count("V407_AUTORIZACAO_OPERADOR"), 2)
    chk(nome + ": nenhum nome da versao anterior sobrou (V406_AUTORIZACAO_OPERADOR, RECIBO_*_v406.json como saida)", "V406_AUTORIZACAO_OPERADOR" not in txt and ('"%s"' % saidas[nome].replace("v407", "v406")) not in txt,
        ["V406_AUTORIZACAO_OPERADOR" in txt, ('"%s"' % saidas[nome].replace("v407", "v406")) in txt], [False, False])
    chk(nome + ": a frase 'por autorizacao geral do operador' nao existe", "por autorizacao geral do operador" not in txt, "por autorizacao geral do operador" in txt, False)
    chk(nome + ": grava so' em " + saidas[nome] + " e recusa sobrescrever (assert not os.path.exists)", ('"%s"' % saidas[nome]) in txt and "assert not os.path.exists(p)" in txt,
        [('"%s"' % saidas[nome]) in txt, "assert not os.path.exists(p)" in txt])
    k_novo, k_real = chaves_do_rec(arv), list(json.load(open(reais[nome], encoding="utf-8")).keys())
    chk(nome + ": chaves do dict rec (ordem) = chaves do recibo REAL da v406", k_novo == k_real, [k_novo, k_real], "listas iguais")
    m_ord = re.search(r'ORDEM = os\.path\.join\(D, "\.\.", "\.\.", "\.\.", "cunhagens_13out", "([^"]+)"\)', txt)   # (v407) a subida mecanica trocou este nome por um com v407 que nao existe: confere que o arquivo que o script abre EXISTE
    chk(nome + ": o arquivo da fala que o script abre (ORDEM) existe em work\\cunhagens_13out e e' o mesmo que este conferidor usa", bool(m_ord) and os.path.isfile(os.path.join(os.path.dirname(os.path.dirname(V)), "cunhagens_13out", m_ord.group(1))) and m_ord.group(1) == os.path.basename(ORDEM_ARQ), m_ord.group(1) if m_ord else None)
    i_ordem = next((i for i, n in enumerate(mod) if isinstance(n, ast.Assert) and "ORDEM_SHA16" in ast.unparse(n.test)), None)
    chk(nome + ": a ordem de 02/11 e' conferida: o assert com ORDEM_SHA16 (lido do ARQUIVO da fala) vem DEPOIS do assert AUT", i_ordem is not None and i_assert is not None and i_ordem > i_assert and "cunhagens_13out" in txt and "OPERADOR_02nov_quando_terminar_compile_v406" in txt and "hashlib.sha256(ORDEM_BYTES)" in txt, [i_assert, i_ordem])
    chk(nome + ": nenhum texto, data ou hash de autorizacao da v405 sobrou (01/11/2026, nenhum sha de 16 hex digitado)", "01/11/2026" not in txt and re.search(r"[0-9a-f]{16}", txt) is None, ["01/11/2026" in txt, re.findall(r"[0-9a-f]{16}", txt)], [False, []])
    if nome == "recibo_parada_v407.py":
        chk(nome + ": le o recibo do religamento da v406 (RECIBO_RELIGAMENTO_v406.json: pid e no_ar_desde), nao depende de RELIGAMENTO_PREVIO_02nov.json (que nao existe na v407), e o PID parado vem de V407_PID_PARADO", "RECIBO_RELIGAMENTO_v406.json" in txt and 'rel406["no_ar_desde"]' in txt and "RELIGAMENTO_PREVIO" not in txt.split('"""', 2)[2] and "V407_PID_PARADO" in txt and "V407_PID_PARADO_CRIADO" in txt, True)
    else:
        chk(nome + ": confere o deployment servido contra o do APLICAR (B<n>-v407-<data>-R1; n = a geracao anterior + 1)", "dep_esp" in txt and "-v407-" in txt and 'c.get("deployment_id") == dep_esp' in txt, True)
    chk(nome + ": o recibo da v407 ainda nao existe (nada foi executado)", not os.path.exists(os.path.join(HERE, saidas[nome])), os.path.exists(os.path.join(HERE, saidas[nome])), False)
# ---- o evento
pe, te, ae = corpo("evento_c1_b3_v407.py")
arquivos["evento_c1_b3_v407.py"] = {"path": pe, "sha256": sha(pe), "bytes": os.path.getsize(pe)}
mod = ae.body


def idx(pred):
    return next((i for i, n in enumerate(mod) if pred(n)), None)


i_isfile = idx(lambda n: isinstance(n, ast.Assert) and "os.path.isfile(ESP)" in ast.unparse(n.test))
i_cand = idx(lambda n: isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CAND16" for t in n.targets))
i_conf = idx(lambda n: isinstance(n, ast.Assert) and "startswith(CAND16)" in ast.unparse(n.test))
i_run = idx(lambda n: isinstance(n, ast.Assign) and "subprocess.run" in ast.unparse(n.value))
chk("evento: assert os.path.isfile(ESP) < leitura de CAND16 < assert startswith(CAND16) < subprocess.run (anotar no quadro)", None not in (i_isfile, i_cand, i_conf, i_run) and i_isfile < i_cand < i_conf < i_run,
    [i_isfile, i_cand, i_conf, i_run], "ordem crescente")
chk("evento: ESP = ..\\ESPERADOS_v407.json e le o campo candidato_sha16", 'os.path.join(D, "..", "ESPERADOS_v407.json")' in te and '["candidato_sha16"]' in te, True)
chk("evento: nenhum hash literal (16 a 64 hex entre aspas)", re.search(r'"[0-9a-f]{16,64}"', te) is None, re.findall(r'"[0-9a-f]{16,64}"', te), [])
chk("evento: V407_AUTORIZACAO_OPERADOR nao e usada (o evento nao exige a variavel; so' parada e religamento)", "V407_AUTORIZACAO_OPERADOR" not in te, "V407_AUTORIZACAO_OPERADOR" in te, False)
chk("evento: versao v407, acao sincronizacao, unidade F0.6, tipo SINCRONIZACAO_BANCADA", '"versao": "v407"' in te and '"acao": "sincronizacao"' in te and '"unidade": "F0.6"' in te and '"SINCRONIZACAO_BANCADA"' in te, True)
esp_p = os.path.join(V, "ESPERADOS_v407.json")
cand16_ = json.load(open(esp_p, encoding="utf-8"))["candidato_sha16"] if os.path.exists(esp_p) else None
um_nos16_ = sha(os.path.join(NOS, "um.py"))[:16]
chk("ESPERADOS_v407.json AUSENTE (o evento abortaria no assert os.path.isfile) ou presente com o um.py do Nos AINDA NAO igual ao candidato dele (abortaria no assert do candidato): em qualquer dos dois estados o evento aborta ANTES de anotar no quadro", cand16_ is None or um_nos16_ != cand16_, [cand16_, um_nos16_], "ausente, ou diferentes")
# ---- a ordem do operador de 02/11 e o AUT do orquestrador
ord_ok = os.path.isfile(ORDEM_ARQ)
ord_txt = open(ORDEM_ARQ, encoding="utf-8").read() if ord_ok else ""
ord16 = sha(ORDEM_ARQ)[:16] if ord_ok else None
chk("a fala do operador de 02/11 (compile, rode, publique) existe e traz a frase", ord_ok and FRASE_DA_ORDEM in ord_txt, [ord_ok, ord16])
aut_orq = None
for n_ in ast.parse(open(os.path.join(V, "orquestrador", "pos_treino_v407.py"), encoding="utf-8").read()).body:
    if isinstance(n_, ast.Assign) and any(isinstance(t_, ast.Name) and t_.id == "AUT" for t_ in n_.targets):
        aut_orq = ast.literal_eval(n_.value)
chk("o AUT do orquestrador (pos_treino_v407.py) e' a ordem de 02/11: traz o sha16 do arquivo da fala (calculado aqui), a frase e a data, e nenhum texto de 01/11", bool(aut_orq) and ord16 is not None and ord16 in aut_orq and FRASE_DA_ORDEM in aut_orq and "02/11/2026" in aut_orq and "01/11/2026" not in aut_orq, [ord16, bool(aut_orq)])
# ---- insumos que os scripts leem
rel8 = os.path.join(V14, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v406.json")
bn8 = sorted(glob.glob(os.path.join(V14, "bancada_B3", "RECIBO_SINCRONIZACAO_v406_*.json")))
chk("insumo da parada: RECIBO_RELIGAMENTO_v406.json existe, e' da porta 18777 e traz pid, no_ar_desde e hora_recibo (o ultimo religamento conhecido; a v407 nao tem RELIGAMENTO_PREVIO)", os.path.isfile(rel8) and (lambda d_: d_.get("porta") == 18777 and str(d_.get("pid", "")).isdigit() and bool(d_.get("no_ar_desde")) and bool(d_.get("hora_recibo")))(json.load(open(rel8, encoding="utf-8"))), rel8)
chk("insumo do religamento: um unico RECIBO_SINCRONIZACAO_v406_*.json em v406\\bancada_B3", len(bn8) == 1, [os.path.basename(x) for x in bn8], 1)
bn9 = sorted(glob.glob(os.path.join(V, "bancada_B3", "RECIBO_SINCRONIZACAO_v407_*.json")))
chk("o recibo do B(n) da v407 ainda nao existe (v407\\bancada_B3 vazia de recibo)", len(bn9) == 0, [os.path.basename(x) for x in bn9], [])
res = {"contrato": "CONFERENCIA_EXIGENCIAS_SERVICO_v407", "como": "estatica (ast + texto); nada foi executado; a producao nao foi tocada", "script": {"path": os.path.abspath(__file__), "sha256": sha(os.path.abspath(__file__))},
       "arquivos": arquivos, "condicoes": checks, "n_condicoes": len(checks), "n_condicoes_ok": sum(1 for c in checks if c["ok"]),
       "exigem_V407_AUTORIZACAO_OPERADOR": {"recibo_parada_v407.py": True, "recibo_religamento_v407.py": True} if all(c["ok"] for c in checks if "AUT" in c["nome"] or "V407_AUTORIZACAO_OPERADOR" in c["nome"]) else "VER condicoes",
       "escopo": "NOT_FALSIFIED nao e creditacao; o gate nao se move"}
dest = os.path.join(HERE, "CONFERENCIA_EXIGENCIAS_SERVICO_v407.json")
if os.path.exists(dest):
    raise SystemExit("ja existe, nao sobrescrevo: " + dest)
with open(dest + ".tmp", "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(res, ensure_ascii=False, indent=1) + "\n")
os.replace(dest + ".tmp", dest)
print("%d/%d condicoes ok" % (res["n_condicoes_ok"], res["n_condicoes"]), "| exigem:", res["exigem_V407_AUTORIZACAO_OPERADOR"])
for c in checks:
    if not c["ok"]:
        print("FALHA:", c["nome"], c["observado"])
print(dest, sha(dest)[:16])
sys.exit(0 if res["n_condicoes_ok"] == res["n_condicoes"] else 1)

# -*- coding: utf-8 -*-
"""conferir_cabecalho.py -- confere o cabecalho (docstring de modulo + docstrings) de Testemunho.lean CONTRA OS ARQUIVOS. So leitura; grava
conferencia_cabecalho.json na pasta de trabalho.

Itens: (1) todo sha16 entre crases bate com o sha256 de um arquivo lido agora (fontes_sha.json refeito aqui); (2) os QUATRO verbatins do operador de
24/10 aparecem INTEIROS; (3) toda citacao «...» de 12+ caracteres e' classificada contra o corpus dos verbatins (OPERADOR_*_verbatim.txt) e o Atlas
(mesma normalizacao da varredura_citacoes.py da v397); (4) nenhuma palavra proibida (regex da regua) e nenhum beta/alfa^2 literal; (5) a DIRECAO do
testemunho: nenhuma frase do tipo «a IALD testifica/testemunha o operador» fora da citacao verbatim em que o operador a RECUSA; (6) sem sorry/axiom;
comentarios balanceados; (7) lista os identificadores citados entre crases (para o #check do probe).
Uso: python -I -B -X utf8 conferir_cabecalho.py
"""
import glob
import hashlib
import json
import os
import re
import unicodedata

W = r"C:\IALD\Central de Patentes\work\v399_selo_e_testemunho"
LEAN = os.path.join(W, "Testemunho.lean")
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
FONTES = json.load(open(os.path.join(W, "fontes_sha.json"), encoding="utf-8"))

src_b = open(LEAN, "rb").read()
src = src_b.decode("utf-8")
cabecalho = src[: src.index("namespace TGLExt.Testemunho")]
R = {"Testemunho.lean_sha16": hashlib.sha256(src_b).hexdigest()[:16], "bytes": len(src_b)}

# (1) sha16 entre crases
citados = sorted(set(re.findall(r"`([0-9a-f]{16})`", src)))
reais = {}


def registra(chave, caminho, sha256_gerado):
    h = hashlib.sha256(open(caminho, "rb").read()).hexdigest()  # relido AGORA
    reais[h[:16]] = {"fonte": chave, "caminho": caminho, "igual_ao_gerado": h == sha256_gerado}


for k, v in FONTES.items():
    if k == "modulos":
        for m, mv in v.items():
            registra("modulo:" + m, mv["sandbox"], mv["sha256"])
    elif isinstance(v, dict) and "caminho" in v and k != "Testemunho.lean":
        registra(k, v["caminho"], v["sha256"])
R["sha16_citados"] = {c: reais.get(c, "SEM_ARQUIVO") for c in citados}
R["sha16_sem_arquivo"] = [c for c in citados if c not in reais]
R["sha16_arquivo_mudou_desde_a_geracao"] = [c for c, v in reais.items() if not v["igual_ao_gerado"]]


# (2) verbatins inteiros
def norm_sp(s):
    return re.sub(r"\s+", " ", s).strip()


verb = {}
VERB = {"sinapse": "OPERADOR_24out_sinapse_token_nome_falta_a_tipagem_verbatim.txt",
        "joao": "OPERADOR_24out_testemunho_joao_8_14_18_verbatim.txt",
        "testifico": "OPERADOR_24out_testifico_de_mim_e_o_um_py_testifica_em_hash_verbatim.txt",
        "quadratica": "OPERADOR_24out_declaracao_operacao_quadratica_da_inscricao_viva_verbatim.txt"}
for chave, nome in VERB.items():
    t = open(os.path.join(CUN, nome), "rb").read().decode("utf-8").rstrip("\r\n")
    verb[chave] = norm_sp(t) in norm_sp(cabecalho)
R["verbatins_inteiros_no_cabecalho"] = verb


# (3) citacoes «...»
def norm(s):
    s = unicodedata.normalize("NFC", s).replace("\u00a0", " ").replace("\r\n", "\n")
    s = s.replace("``", "«").replace("''", "»").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"\\(?=[_&%#])", "", s)
    s = s.replace("---", "—").replace("--", "–")
    return re.sub(r"\s+", " ", s).strip()


CORP = {os.path.basename(p): norm(open(p, "rb").read().decode("utf-8")) for p in glob.glob(os.path.join(CUN, "OPERADOR_*_verbatim.txt"))}
CORP_GER = {os.path.basename(p): norm(open(p, "rb").read().decode("utf-8")) for p in glob.glob(os.path.join(CUN, "GERENCIA_*_verbatim.txt"))}
ATLAS = norm(open(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md", "rb").read().decode("utf-8", "replace").replace("**", ""))
cit = []
for m in re.finditer(r"«([^«»]{12,400})»", src):
    q = norm(m.group(1))
    onde = None
    for k, v in CORP.items():
        if q in v:
            onde = "VERBATIM_OPERADOR:" + k
            break
    if onde is None and q in ATLAS:
        onde = "ATLAS"
    if onde is None:
        for k, v in CORP_GER.items():
            if q in v:
                onde = "VERBATIM_GERENCIA:" + k
                break
    cit.append({"citacao": m.group(1)[:140], "classe": onde or "NAO_ENCONTRADA", "contexto": src[max(0, m.start() - 90):m.start()].replace("\n", " ")[-90:]})
R["citacoes"] = cit
R["citacoes_nao_encontradas"] = [c for c in cit if c["classe"] == "NAO_ENCONTRADA"]

# (4) proibidos
PROIBIDO = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED|CONSCIOUSNESS_PROVED|\bconfirmad[oa]s?\b", re.I)
R["proibidos_regua"] = [m.group(0) for m in PROIBIDO.finditer(src)]
R["beta_ou_alfa2_literal"] = [m.group(0) for m in re.finditer(r"β|α\s*²|alpha_2|α₂|0[,.]012", src)]
R["palavras_para_revisao_humana"] = sorted(set(m.group(0).lower() for m in re.finditer(r"\b(provad[oa]s?|resolvid[oa]s?|pós-di[cç]ão|QG)\b", src, re.I)))

# (5) a DIRECAO do testemunho: a unica ocorrencia permitida de «IALD testifica a mim» e' a citacao verbatim em que o operador a recusa
RECUSA = "eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela"
sem_recusa = src.replace(RECUSA, "[[RECUSA_VERBATIM]]")
PAD_DIRECAO = re.compile(r"IALD\s+(testifica|testemunha|atesta|depõe|depoe)\s+(a mim|de mim|do operador|o operador|ao operador|pelo operador)"
                         r"|a\s+IALD\s+(testifica|testemunha|atesta)\s+(a|o|do)\s+operador|(Pai)\s+(é|e)\s+a\s+IALD", re.I)
R["direcao_frases_proibidas_fora_da_recusa"] = [m.group(0) for m in PAD_DIRECAO.finditer(sem_recusa)]
R["recusa_verbatim_presente"] = RECUSA in src
R["declaracao_do_operador_presente"] = "o um.py só existe porque fui a operação quadrática da inscrição viva do transporte da IALD" in src
R["termos_da_leitura_citados"] = {t: (t in src) for t in ("EXECUTION_LOCKED_NOT_ONE", "temporal_fractalization", "the_light_squares_to_the_graviton", "reading_post_is_born")}

# (6) estrutura
codigo = re.sub(r"/-.*?-/", "", src, flags=re.S)
codigo = re.sub(r"--[^\n]*", "", codigo)
R["tem_sorry_no_codigo"] = bool(re.search(r"\bsorry\b", codigo))
R["palavra_sorry_nos_docstrings"] = len(re.findall(r"\bsorry\b", src))
R["tem_axiom"] = bool(re.search(r"^\s*axiom\b", codigo, re.M))
R["abre_comentario"] = src.count("/-")
R["fecha_comentario"] = src.count("-/")
R["comentarios_balanceados"] = src.count("/-") == src.count("-/")
R["linhas"] = src.count("\n")

# (7) identificadores entre crases
ids = sorted(set(t for t in re.findall(r"`([^`\n]+)`", src) if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", t) and ("_" in t or "." in t or t[0].isupper())))
R["identificadores_citados"] = ids

json.dump(R, open(os.path.join(W, "conferencia_cabecalho.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)
print("sha16 do Testemunho.lean:", R["Testemunho.lean_sha16"], "| bytes", R["bytes"], "| linhas", R["linhas"])
print("sha16 citados:", len(citados), "| sem arquivo:", R["sha16_sem_arquivo"], "| arquivo mudou:", R["sha16_arquivo_mudou_desde_a_geracao"])
print("verbatins inteiros:", verb)
print("citacoes:", len(cit), "| nao encontradas:", len(R["citacoes_nao_encontradas"]))
for c in R["citacoes_nao_encontradas"]:
    print("   NAO_ENCONTRADA:", c["citacao"], "<<", c["contexto"])
for c in cit:
    print("   ", c["classe"][:40], "|", c["citacao"][:70])
print("proibidos:", R["proibidos_regua"], "| beta/alfa2/0,012:", R["beta_ou_alfa2_literal"], "| revisao humana:", R["palavras_para_revisao_humana"])
print("direcao: frases proibidas fora da recusa:", R["direcao_frases_proibidas_fora_da_recusa"], "| recusa verbatim presente:", R["recusa_verbatim_presente"], "| declaracao presente:", R["declaracao_do_operador_presente"])
print("termos da leitura:", R["termos_da_leitura_citados"])
print("sorry no codigo:", R["tem_sorry_no_codigo"], "| palavra nos docstrings:", R["palavra_sorry_nos_docstrings"], "| axiom:", R["tem_axiom"], "| comentarios balanceados:", R["comentarios_balanceados"], R["abre_comentario"], R["fecha_comentario"])
print("identificadores citados:", len(ids))
for i in ids:
    print("   ", i)

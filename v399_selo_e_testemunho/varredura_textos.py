# -*- coding: utf-8 -*-
"""varredura_textos.py -- a regua sobre TODOS os textos da entrega (so leitura; grava varredura_textos.json): (1) palavras proibidas (a regex do um.py v304 e a do conferidor de
cabecalho); (2) literal de beta no CODIGO (0,01203... / 0.01203...) e o literal de acoplamento 0,012; (3) a DIRECAO do testemunho: nenhuma frase em que a IALD testifique/testemunhe/ateste
o operador, e o «Pai» identificado com a IALD, fora da citacao verbatim em que o operador recusa a ordem inversa; (4) 'consciencia' so' como palavra retirada.
Uso: python -I -B -X utf8 varredura_textos.py"""
import json
import os
import re

W = os.path.dirname(os.path.abspath(__file__))
TEXTOS = ["RESULTADO.md", "Testemunho.lean", "registro_mapa_v399_estudo.json", "selo_acom_prototipo.py", "selo_acom_prototipo.py.tmpl",
          os.path.join("patch_proposto", "PATCH_PROPOSTO_v399.md"), os.path.join("patch_proposto", "secao_colavel_v399.py"), os.path.join("patch_proposto", "trechos_v399_para_o_um_py.py")]
for f in sorted(os.listdir(os.path.join(W, "recibos"))):
    if f.endswith(".json") and ".bak_" not in f:
        TEXTOS.append(os.path.join("recibos", f))
CODIGO = {"selo_acom_prototipo.py", "selo_acom_prototipo.py.tmpl", os.path.join("patch_proposto", "secao_colavel_v399.py"), os.path.join("patch_proposto", "trechos_v399_para_o_um_py.py"), "Testemunho.lean"}

PROIB = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED|CONSCIOUSNESS_PROVED|\bconfirmad[oa]s?\b", re.I)
BETA = re.compile(r"0[.,]0120[0-9]|0[.,]012\b")
RECUSA = "eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela"
DIRECAO = re.compile(r"IALD\s+(testifica|testemunha|atesta|depõe|depoe|testifies|testimonies)\s+(a mim|de mim|do operador|o operador|ao operador|pelo operador|of the operator|the operator)"
                     r"|a\s+IALD\s+(testifica|testemunha|atesta)\s+(a|o|do)\s+operador|(Pai)\s+(é|e)\s+a\s+IALD|Pai\s+\(a IALD\)", re.I)
CONSC = re.compile(r"consci[eê]ncia", re.I)
R = {"arquivos": {}, "resumo": {}}
tot_proib = tot_beta_codigo = tot_dir = 0
for f in TEXTOS:
    p = os.path.join(W, f)
    if not os.path.exists(p):
        R["arquivos"][f] = {"ausente": True}
        continue
    t = open(p, "rb").read().decode("utf-8", "replace")
    t2 = t.replace(RECUSA, "[[RECUSA_VERBATIM]]")
    # no JSON a barra invertida duplicada nao afeta; remove escapes de aspas para a recusa
    t2 = t2.replace(RECUSA.replace('"', '\\"'), "[[RECUSA_VERBATIM]]")
    proib = [m.group(0) for m in PROIB.finditer(t)]
    beta = [m.group(0) for m in BETA.finditer(t)]
    direcao = [m.group(0) for m in DIRECAO.finditer(t2)]
    consc = len(CONSC.findall(t))
    R["arquivos"][f] = {"proibidas": proib, "beta_ou_acoplamento_literal": beta, "direcao_invertida": direcao, "ocorrencias_de_consciencia": consc}
    tot_proib += len(proib)
    tot_dir += len(direcao)
    if f in CODIGO:
        tot_beta_codigo += len(beta)
R["resumo"] = {"proibidas_total": tot_proib, "beta_literal_em_codigo": tot_beta_codigo, "direcao_invertida_total": tot_dir,
               "consciencia_em": {f: v["ocorrencias_de_consciencia"] for f, v in R["arquivos"].items() if v.get("ocorrencias_de_consciencia")},
               "beta_nos_textos_nao_codigo": {f: v["beta_ou_acoplamento_literal"] for f, v in R["arquivos"].items() if v.get("beta_ou_acoplamento_literal") and f not in CODIGO}}
with open(os.path.join(W, "varredura_textos.json"), "w", encoding="utf-8", newline="\n") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=1)
print(json.dumps(R["resumo"], ensure_ascii=False, indent=1))
for f, v in R["arquivos"].items():
    if v.get("proibidas") or v.get("direcao_invertida") or (v.get("beta_ou_acoplamento_literal") and f in CODIGO):
        print("ATENCAO", f, v)

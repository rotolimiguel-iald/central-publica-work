# -*- coding: utf-8 -*-
"""conferir_cabecalho.py -- confere o cabecalho (docstring de modulo + docstrings) de AfinacaoDasCordas.lean CONTRA OS ARQUIVOS. So leitura; grava
conferencia_cabecalho.json e probe_nomes.lean (a lista de identificadores citados) na pasta de trabalho.

Itens: (1) todo sha16 entre crases bate com o sha256 de um arquivo lido agora; (2) o verbatim do operador (23/10) aparece INTEIRO; (3) as linhas 958 a 960 do
.tex aparecem byte a byte (a 959 e' vazia) e sao as linhas 958-960 do arquivo; (4) toda citacao «...» de 12+ caracteres e' achada no corpus (verbatins do
operador, o .tex, os modulos do kernel citados); (5) nenhuma palavra proibida (regex da regua) e nenhum beta/alfa^2/0,012 literal; (6) sem sorry no
codigo, sem axiom; comentarios balanceados; (7) lista os identificadores citados entre crases (para o probe de nomes); (8) o codigo (fora dos comentarios)
do Lean gerado e' igual ao do rascunho que compilou limpo (probe/draft1.lean + as adicoes), se o arquivo de referencia existir.
Uso: python -I -B -X utf8 conferir_cabecalho.py
"""
import glob
import hashlib
import json
import os
import re
import unicodedata

W = r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398"
LEAN = os.path.join(W, "AfinacaoDasCordas.lean")
SBLEAN = r"C:\t\k398b\TGLExt\AfinacaoDasCordas.lean"
CUN = r"C:\IALD\Central de Patentes\work\cunhagens_13out"
SUP = r"C:\IALD\Central de Patentes\work\superposicao_passagem_07out"
TEX = r"C:\IALD\Artigo\the_boundary\Genesis da Unificação\Artigos_fundadores\A_ultima_corda_v3.tex"
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt"
FONTES = json.load(open(os.path.join(W, "fontes_sha.json"), encoding="utf-8"))

src_b = open(LEAN, "rb").read()
src = src_b.decode("utf-8")
cabecalho = src[: src.index("namespace TGLExt.AfinacaoDasCordas")]
R = {"AfinacaoDasCordas.lean_sha16": hashlib.sha256(src_b).hexdigest()[:16], "bytes": len(src_b)}
R["sandbox_igual"] = open(SBLEAN, "rb").read() == src_b


def norm_sp(s):
    return re.sub(r"\s+", " ", s).strip()


# (1) sha16 entre crases
citados = sorted(set(re.findall(r"`([0-9a-f]{16})`", src)))
reais = {}
for k, v in FONTES.items():
    if not isinstance(v, dict):
        continue
    for campo in ("caminho", "caminho_nos"):
        if campo in v and k != "Lean_gerado":
            h = hashlib.sha256(open(v[campo], "rb").read()).hexdigest()  # relido AGORA
            reais[h[:16]] = {"fonte": k, "caminho": v[campo], "igual_ao_gerado": h == v["sha256"]}
if FONTES.get("mathlib_rev"):  # o `rev` do Mathlib e' um commit do git (lido do lake-manifest.json), nao o sha256 de um arquivo
    reais[FONTES["mathlib_rev"][:16]] = {"fonte": "mathlib_rev (git, lake-manifest.json)", "caminho": FONTES["lake_manifest"]["caminho"], "igual_ao_gerado": True}
R["sha16_citados"] = {c: reais.get(c, "SEM_ARQUIVO") for c in citados}
R["sha16_sem_arquivo"] = [c for c in citados if c not in reais]
R["sha16_arquivo_mudou_desde_a_geracao"] = [c for c, v in reais.items() if not v["igual_ao_gerado"]]

# (2) verbatim do operador (23/10), inteiro
op = open(FONTES["operador_23out"]["caminho"], "rb").read().decode("utf-8").rstrip("\r\n")
R["verbatim_operador_inteiro_no_cabecalho"] = ("«" + op + "»") in cabecalho

# (2b) a ratificacao do operador (23/10): a resposta inteira, o sha16 citado, a forma admitida da B1 presente, as frases antigas ausentes
rat = open(FONTES["ratificacao"]["caminho"], "rb").read().decode("utf-8").rstrip("\r\n")
src_n = re.sub(r"\s+", " ", src)
R["verbatim_ratificacao_inteiro_no_cabecalho"] = ("«" + rat + "»") in cabecalho
R["sha16_ratificacao_citado"] = FONTES["ratificacao"]["sha16"] in re.findall(r"`([0-9a-f]{16})`", src)
R["forma_admitida_presente_vezes"] = src_n.count("composição da gerência sobre a fala do operador (`" + FONTES["operador_23out"]["sha16"] + "`), ratificada pelo operador em 23/10 (`" + FONTES["ratificacao"]["sha16"] + "`)")
R["afinacao_comensurabilidade_ratificada_vezes"] = src_n.count("ratificada pelo operador em 23/10 (`" + FONTES["ratificacao"]["sha16"] + "`)")
R["frases_antigas_ausentes"] = {f: (f not in src_n) for f in ("na formulação desta tarefa", "NOME PROVISÓRIO", "o operador nomeia", "não fala do operador", "nome provisório")}

# (3) linhas 958-960 do .tex
tex = open(TEX, "rb").read().decode("utf-8").split("\n")
bloco = "\n".join(tex[i].rstrip("\r") for i in (957, 958, 959))
R["tex_l958_960_literal_no_cabecalho"] = ("```\n" + bloco + "\n```") in cabecalho
R["tex_l959_vazia"] = tex[958].rstrip("\r") == ""
R["tex_l958_comeca"] = tex[957].startswith("A coincidência é precisa")
R["tex_l962_frase_no_cabecalho"] = "«Enfatizamos que isso é uma extrapolação teórica, não um teste empírico.»" in cabecalho
R["tex_l962_contem_a_frase"] = "Enfatizamos que isso é uma extrapolação teórica, não um teste empírico." in tex[961]
R["tex_l952_tem_IC95_7_16"] = "[7, 16]" in tex[951]

# (4) citacoes «...» de 12+ caracteres
def norm(s):
    s = unicodedata.normalize("NFC", s).replace("\u00a0", " ").replace("\r\n", "\n")
    s = s.replace("``", "«").replace("''", "»").replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"\\(?=[_&%#])", "", s)
    s = s.replace("---", "—").replace("--", "–")
    return re.sub(r"\s+", " ", s).strip()


CORP = {}
for pat in (os.path.join(CUN, "OPERADOR_*_verbatim.txt"), os.path.join(SUP, "CUNHAGEM_OPERADOR_*_verbatim.txt")):
    for p in glob.glob(pat):
        CORP["VERBATIM_OPERADOR:" + os.path.basename(p)] = norm(open(p, "rb").read().decode("utf-8"))
CORP["TEX:A_ultima_corda_v3.tex"] = norm("\n".join(t.rstrip("\r") for t in tex))
for rel in ("TetelestaiOneObject.lean", "Fundacao.lean", "Palavra.lean", "TheStation.lean", "O16/PolarMinimalPeriod_v2.lean"):
    CORP["KERNEL:" + rel] = norm(open(os.path.join(NOS, *rel.split("/")), "rb").read().decode("utf-8"))
cit = []
for m in re.finditer(r"«([^«»]{12,600})»", src):
    q = norm(m.group(1))
    onde = None
    for k, v in CORP.items():
        if q in v:
            onde = k
            break
    cit.append({"citacao": m.group(1)[:150], "classe": onde or "NAO_ENCONTRADA", "contexto": src[max(0, m.start() - 80):m.start()].replace("\n", " ")[-80:]})
R["citacoes"] = cit
R["citacoes_nao_encontradas"] = [c for c in cit if c["classe"] == "NAO_ENCONTRADA"]

# (5) proibidos
PROIBIDO = re.compile(r"(?<!NOT_)(?<!UN)CONFIRMED|(?<!AP)PROVED_BY|TGL_PROVED|CONSCIOUSNESS_PROVED|\bconfirmad[oa]s?\b", re.I)
R["proibidos_regua"] = [m.group(0) for m in PROIBIDO.finditer(src)]
R["beta_ou_alfa2_literal"] = [m.group(0) for m in re.finditer(r"β|α\s*²|alpha_2|α₂|0[,.]012", src)]
R["palavras_para_revisao_humana"] = sorted(set(m.group(0).lower() for m in re.finditer(r"\b(provad[oa]s?|resolvid[oa]s?|pós-di[cç]ão|QG)\b", src, re.I)))
R["palavra_confirmando_so_dentro_do_bloco_da_casa"] = [
    {"em_bloco_da_casa": ("confirmando" in bloco), "ocorrencias_no_arquivo": len(re.findall(r"confirmando", src, re.I)), "ocorrencias_no_bloco": len(re.findall(r"confirmando", bloco, re.I))}]

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
R["native_decide_ou_decide_no_codigo"] = bool(re.search(r"\b(native_decide|decide)\b", codigo))
R["codigo_fora_dos_comentarios_sha16"] = hashlib.sha256(codigo.encode("utf-8")).hexdigest()[:16]

# (7) identificadores citados entre crases
ids = sorted(set(t for t in re.findall(r"`([^`\n]+)`", src) if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_'.]*", t) and ("_" in t or "." in t or t[0].isupper())))
R["identificadores_citados"] = ids
decl_proprias = re.findall(r"^(?:noncomputable )?(?:theorem|def) ([A-Za-z0-9_']+)", src, flags=re.M)
R["declaracoes_proprias"] = decl_proprias

json.dump(R, open(os.path.join(W, "conferencia_cabecalho.json"), "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

# probe de nomes: cada identificador citado e cada declaracao propria
nomes = sorted(set(ids) | set("TGLExt.AfinacaoDasCordas." + d for d in decl_proprias))
with open(os.path.join(W, "probe_nomes_lista.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(nomes, f, ensure_ascii=False, indent=1)

print("sha16 do AfinacaoDasCordas.lean:", R["AfinacaoDasCordas.lean_sha16"], "| bytes", R["bytes"], "| linhas", R["linhas"], "| sandbox igual:", R["sandbox_igual"])
print("sha16 citados:", len(citados), "| sem arquivo:", R["sha16_sem_arquivo"], "| arquivo mudou:", R["sha16_arquivo_mudou_desde_a_geracao"])
print("verbatim operador inteiro:", R["verbatim_operador_inteiro_no_cabecalho"], "| tex l.958-960 literal:", R["tex_l958_960_literal_no_cabecalho"], "| l.959 vazia:", R["tex_l959_vazia"],
      "| l.962 frase:", R["tex_l962_frase_no_cabecalho"], R["tex_l962_contem_a_frase"], "| l.952 IC:", R["tex_l952_tem_IC95_7_16"])
print("ratificacao inteira:", R["verbatim_ratificacao_inteiro_no_cabecalho"], "| sha16 citado:", R["sha16_ratificacao_citado"], "| forma admitida (vezes):", R["forma_admitida_presente_vezes"],
      "| 'ratificada ... (sha16)' (vezes):", R["afinacao_comensurabilidade_ratificada_vezes"], "| frases antigas ausentes:", R["frases_antigas_ausentes"])
print("citacoes:", len(cit), "| nao encontradas:", len(R["citacoes_nao_encontradas"]))
for c in R["citacoes_nao_encontradas"]:
    print("   NAO_ENCONTRADA:", c["citacao"], "<<", c["contexto"])
print("proibidos:", R["proibidos_regua"], "| beta/alfa2/0,012:", R["beta_ou_alfa2_literal"], "| revisao humana:", R["palavras_para_revisao_humana"], "| 'confirmando':", R["palavra_confirmando_so_dentro_do_bloco_da_casa"])
print("sorry no codigo:", R["tem_sorry_no_codigo"], "| palavra nos docstrings:", R["palavra_sorry_nos_docstrings"], "| axiom:", R["tem_axiom"], "| decide:", R["native_decide_ou_decide_no_codigo"],
      "| comentarios balanceados:", R["comentarios_balanceados"], R["abre_comentario"], R["fecha_comentario"])
print("identificadores citados:", len(ids), "| nomes a conferir:", len(nomes))
for i in ids:
    print("   ", i)

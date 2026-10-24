# -*- coding: utf-8 -*-
"""verificar_quadro.py -- exame final v397 (c1, 23/10/2026), item 4: o QUADRO no topo do artigo PT/EN (txt do ensaio a seco) e do .md canonico do ensaio, conferido POR MIM
contra o resultado pinado (lido do arquivo ORIGINAL em fase9_v2_c1_23out\\saidas, por sha256): (a) posicao no topo; (b) os oito numeros formatados == os do resultado (minha formatacao);
(c) a regra do 4,44 item a item (p calibrado 4,4e-6 + '5' sigma + 'nao foi alcancad'/'not reached' no MESMO item), e a versao estrita (tambem creditacao, gate, NOT_FALSIFIED, nao cego);
(d) a frase do operador VERBATIM (substring do arquivo 9b182958) e NENHUMA parafrase ('cala a boca;' / '5σ é o cala'); (e) 'pelo fator K' marcado como composicao da gerencia no artigo;
(f) toda ocorrencia de 4,44 / 4.44 fora do quadro tambem com p e 5 sigma. So le."""
import json, re, sys, os, hashlib, io
sys.stdout.reconfigure(encoding="utf-8")
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v398"
RES = r"C:\IALD\Central de Patentes\work\fase9_v2_c1_23out\saidas\RESULTADO_FASE9_V2_C1_20261023_122926.json"
rb = open(RES, "rb").read(); assert hashlib.sha256(rb).hexdigest().startswith("fbac2908fa9ddb75"); res = json.loads(rb.decode("utf-8"))
P = res["primario"]
num = {"z_disc": P["calibracao"]["z_disc_calibrado"], "p_disc": P["calibracao"]["p_calibrado_z_disc_unilateral"], "z_delta": P["calibracao"]["z_delta_calibrado"], "p_delta": P["calibracao"]["p_calibrado_z_delta_bilateral"],
       "poder": P["poder_previo_so_sigma"], "lnB_lcdm": P["lnB"]["TGL_vs_LCDM"], "lnB_beta_livre": P["lnB"]["TGL_vs_beta_livre"], "K": res["beta"]["K"]}
def fmt(lang):
    sep = "," if lang == "pt" else "."
    f = lambda x, d: ("%.*f" % (d, x)).replace(".", sep)
    m, e = ("%.1e" % num["p_disc"]).split("e")
    return {"z_disc": f(num["z_disc"], 2), "p_disc": m.replace(".", sep) + "e-" + str(abs(int(e))), "z_delta": f(num["z_delta"], 2), "p_delta": f(num["p_delta"], 2), "poder": f(num["poder"], 2),
            "lnB_lcdm": f(num["lnB_lcdm"], 2), "lnB_beta_livre": f(num["lnB_beta_livre"], 2), "K": f(num["K"], 4)}
VERB = open(r"C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_23out_4_44_silencio_forcado_pela_logica_verbatim.txt", encoding="utf-8").read()
FRASE = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"
assert FRASE in VERB
PARAFRASES = ["cala a boca;", "5σ é o cala", "5 sigma é o cala a boca;", "o 5σ é o cala a boca"]
def norm(t):
    t = t.replace("−", "-").replace("\u00a0", " ").replace("×", "x")
    t = re.sub(r"[x]\s*10\^\s*\{?-?\s*(\d+)\}?", lambda m: "e-" + m.group(1), t)
    return re.sub(r"\s+", " ", t)
def itens(bloco, kind):
    if kind == "md":
        return [x for x in re.split(r"(?m)^>\s*-\s+", bloco) if x.strip()]
    return [x for x in re.split(r"(?m)^\s*[*•\-]\s+|\n\s*\n", bloco) if x.strip()]
def regra(bloco, kind, lang, z, p):
    out = []
    for it in itens(bloco, kind):
        n = norm(it)
        if z in n:
            tem5 = bool(re.search(r"5\s*(?:sigma|σ|\\sigma)", n)); temp = p in n
            nao = ("alcan" in n) if lang == "pt" else ("not reached" in n)
            estrito = tem5 and temp and nao and ("credita" in n.lower()) and ("gate" in n.lower()) and ("NOT_FALSIFIED" in it) and (("cego" in n.lower()) if lang == "pt" else ("blind" in n.lower()))
            out.append({"item": n[:110], "p": temp, "5sigma": tem5, "nao_alcancada": nao, "estrito_creditacao_gate_NF_cego": estrito})
    return out
R = {"numeros_do_resultado": num}
for lang, fn in (("pt", "dry_v398_pt.txt"), ("en", "dry_v398_en.txt")):
    txt = open(os.path.join(V, "dry_v398", fn), encoding="utf-8").read()
    a = fmt(lang)
    tit = "O Teste da Única Palavra" if lang == "pt" else "The Test of the Only Word"
    corpo = "E se o problema da unificação" if lang == "pt" else "What if the unification problem"
    i_q, i_c = txt.find(tit), txt.find(corpo)
    bloco = txt[i_q:i_c] if 0 <= i_q < i_c else ""
    nb = norm(bloco)
    mach = "z_disc=%s; p_disc=%s; z_delta=%s; p_delta=%s; poder=%s; lnB_lcdm=%s; lnB_beta_livre=%s; K=%s" % tuple(a[k] for k in ("z_disc", "p_disc", "z_delta", "p_delta", "poder", "lnB_lcdm", "lnB_beta_livre", "K"))
    # titulo do artigo e resumo: o quadro vem antes do resumo?
    i_res = txt.find("Resumo" if lang == "pt" else "Abstract")
    todos444 = [m.start() for m in re.finditer(re.escape(a["z_disc"]), norm(txt))]
    # cada paragrafo do texto inteiro com 4,44 traz p e 5 sigma?
    pars = [norm(x) for x in re.split(r"\n\s*\n", txt) if a["z_disc"] in norm(x)]
    fora = [{"par": x[:100], "p": a["p_disc"] in x, "5sigma": bool(re.search(r"5\s*(?:sigma|σ)", x))} for x in pars]
    R[lang] = {"quadro_no_topo_antes_do_corpo": 0 <= i_q < i_c, "quadro_antes_do_resumo": 0 <= i_q < i_res if i_res >= 0 else None, "indices": [i_q, i_res, i_c], "bloco_chars": len(bloco),
               "linha_de_maquina_minha": mach, "linha_de_maquina_no_quadro": norm(mach) in nb, "numeros_no_quadro": {k: a[k] in nb for k in a},
               "frase_verbatim_no_quadro": FRASE in bloco, "parafrases_no_texto_inteiro": {p: p in txt for p in PARAFRASES}, "n_ocorrencias_4_44_no_texto": len(todos444),
               "regra_itens_do_quadro": regra(bloco, "txt", lang, a["z_disc"], a["p_disc"]), "paragrafos_com_4_44_no_texto_inteiro": fora,
               "composicao_marcada": ("composição da gerência" in txt) if lang == "pt" else ("management's composition" in txt),
               "verbatim_f3e2_citado": "o psion, o psibit, e é justamente ela que flutua sobre o abismo, o referente último" in txt,
               "variante_nao_selou": None}
    var = open(os.path.join(V, "dry_v398", "dry_v398_var_%s.txt" % lang), encoding="utf-8").read()
    R[lang]["variante_nao_selou"] = (("NÃO selou" in var) if lang == "pt" else ("did NOT seal" in var)) and (("n/d" in var) if lang == "pt" else ("n/a" in var))
# o .md do ensaio
md = open(os.path.join(V, "dry_v398", "um_absoluto_forma_canonica.md"), encoding="utf-8").read()
a = fmt("pt")
i_q = md.find("**O Teste da Única Palavra (v397"); m_t = re.search(r"(?m)^## ", md); i_t = m_t.start() if m_t else -1
ls = md[i_q:].split("\n") if i_q >= 0 else []; blk = []
for l in ls:
    if blk and not l.startswith(">"):
        break
    blk.append(l)
bloco = "\n".join(blk); nb = norm(bloco)
mach = "z_disc=%s; p_disc=%s; z_delta=%s; p_delta=%s; poder=%s; lnB_lcdm=%s; lnB_beta_livre=%s; K=%s" % tuple(a[k] for k in ("z_disc", "p_disc", "z_delta", "p_delta", "poder", "lnB_lcdm", "lnB_beta_livre", "K"))
R["md"] = {"quadro_antes_do_primeiro_titulo": 0 <= i_q < i_t, "indices": [i_q, i_t], "linha_de_maquina_no_quadro": norm(mach) in nb, "numeros_no_quadro": {k: a[k] in nb for k in a},
           "frase_verbatim": FRASE in bloco, "parafrases": {p: p in md for p in PARAFRASES}, "regra_itens": regra(bloco, "md", "pt", a["z_disc"], a["p_disc"]),
           "paragrafos_com_4_44_fora_do_quadro": [norm(x)[:120] for x in md.split("\n") if a["z_disc"] in norm(x) and x not in blk]}
# README/handoff: o paragrafo do harness do fechar (se existir)
hp = os.path.join(V, "pos_rito", "harness_saida_v398", "fechar_sandbox_resultado", "handoff-v398-custodia.md")
import sys as _sys
if len(_sys.argv) > 1:
    hp = _sys.argv[1]   # o handoff do MEU sandbox (sb2)
if os.path.exists(hp):
    h = open(hp, encoding="utf-8").read(); i, j = h.find("<!-- INICIO_PARAGRAFO_README_v397 -->"), h.find("<!-- FIM_PARAGRAFO_README_v397 -->")
    par = h[i:j]
    R["paragrafo_readme_do_harness"] = {"existe": True, "frase_verbatim": FRASE in par, "regra_itens": regra(par, "md", "pt", a["z_disc"], a["p_disc"]), "linha_de_maquina": norm(mach) in norm(par), "parafrases": {p: p in h for p in PARAFRASES}}
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "VERIFICACAO_QUADRO_v398.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

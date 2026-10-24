# -*- coding: utf-8 -*-
"""quadro_v397.py [copia na cadeia v398: so' o import do delta mudou; o quadro nao se mexe] -- o lado da CADEIA do quadro «O Teste da Unica Palavra» (ordem do operador de 23/10/2026, sha16 9b182958a5a7a1bc: reportar o 4,44 no inicio do artigo, no readme e tudo mais).
O quadro em si e' gerado pelas funcoes PURAS de runtime_quadro_v397.py (EMBUTIDAS no um.py); este modulo IMPORTA as MESMAS funcoes (nao as reescreve) e CONFERE as superficies renderizadas (artigo PT/EN em TXT, .md) contra o
RESULTADO pinado do Teste da Unica Palavra:
  (1) o quadro esta no TOPO (antes do primeiro paragrafo do corpo / do primeiro titulo de secao);
  (2) os numeros do quadro == os do resultado pinado (a linha de maquina e' comparada a linha esperada, calculada do resultado; e cada numero formatado esta no quadro);
  (3) a REGRA DA ORDEM: o 4,44 nunca aparece sem o p calibrado e sem a linha dos 5 sigma no MESMO item/paragrafo; a frase do operador esta VERBATIM; a linha da regua (a discriminacao a 5 sigma nao foi alcancada; NOT_FALSIFIED nunca e' a palavra
      da creditacao; o gate nao se move; o teste nao foi cego) esta no item do 4,44.
Funcoes: lido_do_resultado(res), esperados(res, lang), normaliza(txt), confere_txt(txt, res, lang), confere_md(md, res), paragrafo_pronto_readme(tv)."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v398 as DL  # noqa: E402
import runtime_quadro_v397 as Q  # noqa: E402

MENOS = "−"


def lido_do_resultado(res):
    """O dict `lido` que o registro captura, calculado direto do resultado pinado (pelos mesmos caminhos de DL.F9_CAMINHOS)."""
    return {k: DL.lido(res, c) for k, c in DL.F9_CAMINHOS.items()}


def esperados(res, lang):
    """Atomos esperados do quadro (txt/md/tex) e a linha de maquina esperada, a partir do resultado pinado."""
    a = Q._v397_atomos({"all_verified": True, "lido": lido_do_resultado(res), "fontes": []}, lang)
    return a, Q._v397_linha_de_maquina(a, lang)


def normaliza(txt):
    """Normaliza a superficie renderizada para comparar com a linha de maquina: tira $ { } \\, troca o menos de verdade por '-', junta os espacos, 'x10^-6' -> 'e-6'."""
    t = txt.replace("\\times", "×").replace(MENOS, "-").replace("$", "").replace("{", "").replace("}", "").replace("\\", "")
    t = re.sub(r"[×x]\s*10\^\s*-?\s*(\d+)", lambda m: "e-" + m.group(1), t)
    return re.sub(r"\s+", " ", t)


def _regra_da_ordem(itens, num444, lang):
    """Todo item que traz o z_disc (4,44) traz tambem o p calibrado (4,4e-6) e a linha dos 5 sigma (`5sigma`/`5σ`/`5 sigma`) e 'nao foi alcancad' (PT) / 'not reached' | 'was not reached' (EN)."""
    falhas = []
    for it in itens:
        n = normaliza(it)
        if num444 in n:
            tem5 = bool(re.search(r"5\s*(?:sigma|σ)", n))
            temp = "e-6" in n
            nao = ("alcan" in n) if lang == "pt" else ("not reached" in n or "was not reached" in n)
            if not (tem5 and temp and nao):
                falhas.append({"item": n[:160], "tem_5sigma": tem5, "tem_p": temp, "diz_que_nao_foi_alcancada": nao})
    return falhas


def confere_txt(txt, res, lang):
    """Confere o quadro numa superficie de TEXTO (o .txt do artigo PT ou EN). Devolve {ok, ...}."""
    a, mach = esperados(res, lang)
    tit = "O Teste da Única Palavra" if lang == "pt" else "The Test of the Only Word"
    corpo_ini = "E se o problema da unificação" if lang == "pt" else "What if the unification problem"
    i_q = txt.find(tit); i_c = txt.find(corpo_ini); i_h = txt.find("O estatuto da prova (v391)" if lang == "pt" else "The status of the proof (v391)")
    topo = bool(0 <= i_q and (i_c < 0 or i_q < i_c) and (i_h < 0 or i_q < i_h))
    # o bloco do quadro: do titulo ate o inicio do corpo (ou 6000 caracteres)
    fim = i_c if (i_c > i_q >= 0) else (i_q + 6000)
    bloco = txt[i_q:fim] if i_q >= 0 else ""
    nb = normaliza(bloco)
    linha_ok = normaliza(mach) in nb
    num_ok = {k: (normaliza(a[k]["txt"]) in nb) for k in ("z_disc", "p_disc", "z_delta", "p_delta", "poder", "lnB_lcdm", "lnB_beta_livre", "K")}
    frase_ok = Q._V397_FRASE_444 in bloco
    itens = [x for x in re.split(r"(?m)^\s*[*•]\s+", bloco) if x.strip()]
    falhas_ordem = _regra_da_ordem(itens, normaliza(a["z_disc"]["txt"]), lang)
    ruler = ("NOT_FALSIFIED" in bloco and ("gate" in bloco))
    return {"idioma": lang, "topo": topo, "indice_do_quadro": i_q, "indice_do_corpo": i_c, "linha_de_maquina_esperada": mach, "linha_de_maquina_confere": linha_ok, "numeros_no_quadro": num_ok, "frase_do_operador_verbatim": frase_ok,
            "regra_da_ordem_falhas": falhas_ordem, "n_itens": len(itens), "linha_da_regua": ruler, "ok": bool(topo and linha_ok and all(num_ok.values()) and frase_ok and not falhas_ordem and ruler and len(itens) >= 5)}


def confere_md(md, res):
    """Confere o quadro no .md canonico (PT): no topo (antes do primeiro titulo `## `), numeros == resultado, regra da ordem, frase verbatim."""
    a, mach = esperados(res, "pt")
    i_q = md.find("**O Teste da Única Palavra (v397")
    i_t = re.search(r"(?m)^## ", md); i_t = i_t.start() if i_t else -1
    topo = bool(0 <= i_q and (i_t < 0 or i_q < i_t))
    bloco = ""
    if i_q >= 0:
        ls = md[i_q:].split("\n"); ls[0] = ls[0]
        out = []
        for l in ls:
            if out and not l.startswith(">"):
                break
            out.append(l)
        bloco = "\n".join(out)
    nb = normaliza(bloco)
    linha_ok = normaliza(mach) in nb
    num_ok = {k: (normaliza(a[k]["md"]) in nb) for k in ("z_disc", "p_disc", "z_delta", "p_delta", "poder", "lnB_lcdm", "lnB_beta_livre", "K")}
    itens = [x for x in re.split(r"(?m)^>\s*-\s+", bloco) if x.strip()]
    falhas_ordem = _regra_da_ordem(itens, normaliza(a["z_disc"]["md"]), "pt")
    return {"topo": topo, "linha_de_maquina_confere": linha_ok, "numeros_no_quadro": num_ok, "frase_do_operador_verbatim": Q._V397_FRASE_444 in bloco, "regra_da_ordem_falhas": falhas_ordem, "n_itens": len(itens),
            "linha_da_regua": ("NOT_FALSIFIED" in bloco and "gate" in bloco), "ok": bool(topo and linha_ok and all(num_ok.values()) and Q._V397_FRASE_444 in bloco and not falhas_ordem and "NOT_FALSIFIED" in bloco and len(itens) >= 5)}


def paragrafo_pronto_readme(tv):
    """O paragrafo PRONTO PARA COLAR no README do espelho e no site (ato da sessao do site): o MESMO quadro do .md (mesmas funcoes, mesmos numeros lidos do registro selado) e os mesmos estatutos, com uma linha de entrada.
    `tv` = o registro teste_de_veracidade_fase9_v397 do core selado."""
    ls = Q._v397_quadro_md(tv)
    cab = "### O Teste da Única Palavra (v397, 23/10/2026) — paragrafo pronto para o README do espelho e para o site"
    return cab + "\n\n" + "\n".join(ls) + "\n"

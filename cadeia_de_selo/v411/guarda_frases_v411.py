# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] a GUARDA DE TEXTOS da v411 (DESENHO_v411 secao 4), no molde da guarda_frases_v410.py
"""guarda_frases_v411.py -- A GUARDA DE TEXTOS DA v411: reprova, em todo texto NOVO da gerencia (registro, artigo PT/EN, .md, handoff, README, site, X), as frases que afirmam demais. A FONTE da regra e' uma so': a funcao
_v411_guarda_frases de runtime_h0dn_v411.py, a mesma que vai embutida no um.py e roda a cada rito sobre o texto do registro (c16). Ela HERDA a da v410 (_v410_guarda_frases, lida do um.py da v410 selada por trecho,
base_um_v410.py: a cadeia v405 -> v410 inteira) com DUAS regras superadas pela abertura de 12/11 (D169), ditas: a F54 da v410 (a obrigacao “pre-registrado; nenhum dado observado lido” onde H0DN aparece) sai e da lugar a
F67; da F56 sai so' “o teste aberto / a abertura feita”. As novas: F60 a palavra da creditacao afirmada; F61 “poder certificado”; F62 o vetor fora do suporte dito erro de montagem; F63 «teste cego» sem a negacao; F64
“evidencia independente” sem a negacao; F65 «descoberta» para o numero; F66 beta literal; F67 (OBRIGACAO) as quatro obrigacoes no mesmo paragrafo ou bloco do resultado. Aqui a cadeia a usa por `violacoes(texto)`, que
retira ANTES os trechos que sao FALA DO OPERADOR, verbatim (as 11 falas de 11 e 12/11 da lista congelada, so' como excecao da guarda, que nunca entram no programa, e as frases verbatim da v410): a fala dele fica como registro; a guarda e' sobre o texto da gerencia.
Controle negativo (o __main__ e `controle_negativo()`): cada frase proibida TEM de ser reprovada; a frase certa TEM de passar; a fala do operador so' passa pela excecao; se o controle falha, rc 1. Grava GUARDA_FRASES_v411.json.
uso: python -B -X utf8 guarda_frases_v411.py [arquivo ...]   (sem arquivo: so' o controle negativo; com arquivo: varre cada um; rc 1 se houver violacao)"""
import json, math, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
import base_um_v410 as B  # noqa: E402

NS = B.carregar(["_v392_guarda_texto", "_v410_guarda_frases"])
B.chamar_resolvendo(NS, "_v410_guarda_frases", "aquecimento")
exec(compile(open(os.path.join(HERE, "runtime_h0dn_v411.py"), encoding="utf-8").read(), os.path.join(HERE, "runtime_h0dn_v411.py"), "exec"), NS)
_v411_guarda_frases = NS["_v411_guarda_frases"]
p18 = NS["_v392_guarda_texto"]
p18_sem_cabeca = NS["_v411_p18_sem_cabeca"]   # (decisao (c) da gerencia, 12/11) a UNICA excecao da P18 para a cabeca do teste: a mesma funcao do um.py; todo conferidor a usa
RAMOS_V411 = json.loads(open(DL.INSUMO_POR_NOME["RAMOS_V411.json"]["arquivo"], "rb").read().decode("utf-8"))
_RES_ABERTURA = json.loads(open(DL.INSUMO_POR_NOME["RESULTADO_DA_ABERTURA_V411.json"]["arquivo"], "rb").read().decode("utf-8"))
N_DA_CABECA = int(math.floor(float(_RES_ABERTURA["resultado"]["estatistica"]["z_null"][0])))   # (lido do resultado da abertura, nunca digitado)
EXCECOES = tuple(sorted({f_["text"].strip() for f_ in DL.FALAS_V411} | set(DL.D10.FRASES_VERBATIM_V410) | {DL.D10.FRASE_NOMES}, key=len, reverse=True))


def sem_falas(txt, excecoes=EXCECOES):
    s_ = str(txt)
    for v_ in excecoes:
        for ln_ in [l_.strip() for l_ in v_.splitlines() if len(l_.strip()) >= 12] + [v_.strip()]:
            for forma_ in (ln_, json.dumps(ln_, ensure_ascii=False)[1:-1]):
                s_ = s_.replace(forma_, " ")
    return s_


def violacoes(txt, excecoes=EXCECOES):
    return _v411_guarda_frases(sem_falas(txt, excecoes))


PROIBIDAS = [   # (regra esperada, frase) -- a v411 (DESENHO §4)
    ("F60", "a TGL foi confirmada pela natureza"), ("F60", "the TGL is confirmed by nature"), ("F60", "β_TGL confirmado na natureza"),
    ("F61", "o teste tem poder certificado"), ("F61", "o poder preditivo certificado do teste"), ("F61", "the test has certified power"), ("F61", "com o certificado de poder do H0DN"),
    ("F62", "o vetor fora do suporte é erro de montagem"), ("F62", "the vector outside the support is an assembly error"),
    ("F63", "foi um teste cego"), ("F63", "this was a blind test"), ("F63", "o teste é cego"),
    ("F64", "é evidência independente das Fases 4, 5 e 9"), ("F64", "it is independent evidence"),
    ("F65", "a descoberta do H0DN a 6 sigma"), ("F65", "the discovery of the Hubble ratio"),
    ("F65", "o rito fez a descoberta do número"), ("F65", "a descoberta de 6,11 sigma no critério de 5 sigma"), ("F65", "the rite made a discovery at 6 sigma"),   # (D172/D173: a descoberta dita do numero ou do rito segue recusada)
    ("F66", "com beta = 0,0120313"), ("F66", "beta = 0.012031300400803142"),
    ("F67", "no H0DN o primário fica a 6,11 contra o nulo"), ("F67", "β_TGL provado na natureza a 6σ no teste da razão de Hubble"),
    ("F67", "the primary lies 6.11 against the null in the H0DN test, under the published error model"),
    ("F53", "5 sigma atingido no H0DN"), ("F55", "não falsificado a 5 sigma"), ("F56", "a covariância física está fechada"),
    ("F67", r"$Z$ contra o nulo $=6{,}11$ no teste H0DN"), ("F67", r"$Z$ against the null $=6.11$ in the H0DN test"),   # (B-02 da revisao de terceiro, R1) o Z escrito em TeX, sem as quatro obrigacoes, tem de ser recusado (o disparador tolera o cifrao)
]
LIMPAS = [
    "o teste não é cego", "não é teste cego", "the test is not blind", "não é evidência independente das Fases 4, 5 e 9", "it is not independent evidence",
    "o rito confere a conta, não descobre um número novo", "a creditação é de quem observa de fora", "o teste H0DN × BG1 foi aberto uma vez, depois do commit público do pré-registro",
    "no teste da razão de Hubble (H0DN × BG1), sob o modelo de erros publicado, o primário fica a 6,11σ contra o nulo; ao lado, as Cefeidas livres leem 4,38σ, abaixo de 5; retrodição sem ajuste, teste não cego; validade, não creditação",
    "in the Hubble-ratio test (H0DN × BG1), under the published error model, the primary lies 6.11σ against the null; beside it, the free Cepheids read 4.38σ, below 5; retrodiction without fit, the test is not blind; validity, not creditation",
    "o vetor fora do suporte é propriedade do modelo publicado; a colaboração resolve por pseudoinversa", "o poder é de desenho no modelo publicado; as linhas de estresse vão ao lado",
    "β entra só por nome (ALPHA_FINE_CODATA_2018 × √e em runtime)",
    "o que passa do degrau de 5σ, o critério de descoberta da física acadêmica", "na escala de descoberta da física acadêmica", "the one that passes the 5σ step, the discovery criterion of academic physics",
    "the discovery scale of academic physics", "the 5σ discovery threshold",   # (D172/D173: o NOME fixo da convencao dos 5 sigma passa)
    r"no teste H0DN, sob o modelo de erros publicado, $Z$ contra o nulo $=6{,}11$; as Cefeidas livres leem $4{,}38$, abaixo de 5; retrodição sem ajuste, teste não cego; validade, não creditação",   # (B-02) a forma limpa em TeX, com as quatro, passa
    r"in the H0DN test, under the published error model, $Z$ against the null $=6.11$; the free Cepheids read $4.38$, below 5; retrodiction without fit, the test is not blind; validity, not creditation",
]


def controle_negativo():
    res = {"proibidas": [], "limpas": [], "falas": []}
    for regra, fr in PROIBIDAS:
        v_ = violacoes(fr)
        res["proibidas"].append({"frase": fr, "regra_esperada": regra, "violacoes": [x_[0] for x_ in v_], "reprovada": any(x_[0].startswith(regra) for x_ in v_)})
    for fr in LIMPAS:
        v_ = violacoes(fr)
        res["limpas"].append({"frase": fr, "violacoes": v_, "passa": not v_})
    for f_ in DL.FALAS_V411:   # a fala do operador passa SO' pela excecao (crua, ela pode cair numa regra: e' registro, nao texto da gerencia)
        crua_ = _v411_guarda_frases(f_["text"])
        res["falas"].append({"fala": f_["nome"], "violacoes_crua": [x_[0] for x_ in crua_], "passa_pela_excecao": not violacoes(f_["text"])})
    cab_ = "".join(RAMOS_V411["vereditos"]["leitura_partes"]) % N_DA_CABECA; troc_ = cab_[:-1] + ("X" if cab_[-1] != "X" else "Y")
    tex_ = cab_.replace("\\", "").replace("_", r"\_\allowbreak{}")
    res["excecao_p18_da_cabeca"] = {"exata_retirada": not p18_sem_cabeca("a cabeca: " + cab_, RAMOS_V411, N_DA_CABECA), "exata_tex_retirada": not p18_sem_cabeca(r"\texttt{" + tex_ + "}", RAMOS_V411, N_DA_CABECA),
                                    "um_caractere_trocado_recusado": bool(p18_sem_cabeca("a cabeca: " + troc_, RAMOS_V411, N_DA_CABECA)), "crua_recusada": bool(p18("a cabeca: " + cab_)),
                                    "outra_n_recusada": bool(p18_sem_cabeca("a cabeca: " + "".join(RAMOS_V411["vereditos"]["leitura_partes"]) % (N_DA_CABECA + 1), RAMOS_V411, N_DA_CABECA))}
    res["ok"] = all(x_["reprovada"] for x_ in res["proibidas"]) and all(x_["passa"] for x_ in res["limpas"]) and all(x_["passa_pela_excecao"] for x_ in res["falas"]) \
        and any(x_["violacoes_crua"] for x_ in res["falas"]) and all(res["excecao_p18_da_cabeca"].values())
    return res


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    cn = controle_negativo()
    rc = 0 if cn["ok"] else 1
    arqs = {}
    for p in sys.argv[1:]:
        v_ = violacoes(open(p, encoding="utf-8").read()); arqs[p] = v_[:12]
        print(p, "->", "LIMPO" if not v_ else v_[:6])
        rc |= bool(v_)
    if not sys.argv[1:]:
        out = {"contrato": "GUARDA_FRASES_v411", "controle_negativo": cn, "n_proibidas": len(PROIBIDAS), "n_limpas": len(LIMPAS), "n_falas_excecao": len(DL.FALAS_V411), "regras_superadas_da_v410": ["F54 (D169)", "F56 parcial: o teste aberto / a abertura feita (D169)"]}
        p_ = os.path.join(HERE, "GUARDA_FRASES_v411.json")
        open(p_ + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p_ + ".tmp", p_)
    print("controle negativo:", "OK" if cn["ok"] else "FALHOU", "| proibidas reprovadas %d/%d | limpas passam %d/%d | falas pela excecao %d/%d" % (
        sum(x_["reprovada"] for x_ in cn["proibidas"]), len(cn["proibidas"]), sum(x_["passa"] for x_ in cn["limpas"]), len(cn["limpas"]), sum(x_["passa_pela_excecao"] for x_ in cn["falas"]), len(cn["falas"])))
    for x_ in cn["proibidas"]:
        if not x_["reprovada"]:
            print("  PROIBIDA QUE PASSOU:", x_)
    for x_ in cn["limpas"]:
        if not x_["passa"]:
            print("  LIMPA REPROVADA:", x_)
    for x_ in cn["falas"]:
        if not x_["passa_pela_excecao"] or True:
            print("  fala", x_["fala"][:60], "| crua:", x_["violacoes_crua"], "| pela excecao passa:", x_["passa_pela_excecao"])
    sys.exit(rc)

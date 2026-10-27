# -*- coding: utf-8 -*-
"""patch_conferidor_v401.py -- aplica, por substituicoes de contagem EXATA, a logica da v401 sobre o conferir_rito_v401.py derivado (origem v399 com as licoes da v400: C3, C9, C13, C15, C16). A v401 e' uma versao de CONTEUDO: UM modulo novo (FalsidadeDaInercia),
o registro falsidade_da_inercia_v401, os registros por spec cunhagens_v401 e kh_n1_cobertura_v401, as duas chaves novas no selo; a secao do selo pela propria tecnologia (v399/v400) NAO muda (o runtime dela e' o da v400). Recusa rodar duas vezes."""
import ast, sys
sys.stdout.reconfigure(encoding="utf-8")
P = sys.argv[1] if len(sys.argv) > 1 else "conferir_rito_v401.py"
t = open(P, encoding="utf-8").read()
assert "# [v401-patch]" not in t, "o patch ja foi aplicado"


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


# ---- cabecalho
i = t.index('"""conferir_rito_v401.py'); j = t.index("import hashlib, importlib.util, io, json, math, os, re, shutil, sys, time")
t = t[:i] + '''"""conferir_rito_v401.py -- confere, DEPOIS do rito v401, o que tinha de mudar e o que NAO podia (ESPERADOS_v401.json; so leitura do Nos). Molde: conferir_rito_v399.py (a cadeia de CONTEUDO) com as licoes da v400 (C3, C9, C13, C15, C16).
Mudancas ditas: +3 chaves (falsidade_da_inercia_v401, cunhagens_v401, kh_n1_cobertura_v401) no core e +2 no selo (o resumo da falsidade e registros_v401); a escada 9541 -> a dos ESPERADOS (+12 bandeiras); o modulo novo (TGLExt/FalsidadeDaInercia.lean) no kernel do Nos (sha pinado), a raiz e o Audit do candidato;
os vereditos da TROCA DITA (so' numeros); artigo, sumario, .md; O QUADRO «O Teste da Unica Palavra» (v397) CONTINUA NO TOPO do artigo PT/EN e do .md com os NUMEROS == os do resultado pinado e a regra da ordem do 4,44 (o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma). NENHUM outro veredito da v400 muda.
O registro falsidade_da_inercia_v401 (a inercia e' o proprio zero absoluto; um posto inercial daria 1 = 0) e as cinco inscricoes de 25/10, as ratificacoes e a errata ao lado do adendo (cunhagens_v401). E o SIDECAR um_absoluto_selo_acom.json (a segunda testemunha do um.py, do core e do selo FINAIS, ao lado do SHA-256)
com os 16 ITENS (C1 a C16: o estudo da v399 e as guardas estaticas da Bancada, licao da v400) e o ROUND TRIP byte a byte do um.py INSTALADO: os bytes do um.py instalado -> as tres partes cruas (Psi, Theta, kappa) -> o objeto, refeito AQUI pelo codigo do proprio um.py instalado (importado de uma copia de bytes; o Nos so' e' lido)
e por uma conta independente (a formula da Dobra + rint + centro). A DIRECAO do testemunho (o operador testifica DA IALD; o um.py testifica EM HASH; a IALD NAO testifica do operador) e' conferida nos textos, e nenhuma alegacao de confidencialidade pode estar no sidecar.
uso: python -I -B -X utf8 conferir_rito_v401.py [sufixo]   (o sufixo vai no nome do JSON; antes do rito, o controle negativo deve dar tudo_bate falso)
Variaveis opcionais para o TESTE do caminho positivo contra um Nos FALSO (nunca o real): V401_NOS=<pasta>  (padrao: o Nos real, so' leitura)."""
# [v401-patch]
''' + t[j:]

# ---- a secao do selo ACOM e' a da v400 (runtime_v400.py); as fontes do operador moram na pasta da v400; o sandbox curto da v401 e' vb18
sub('_RT = open(os.path.join(HERE, "runtime_v401.py"), "rb").read().decode("utf-8")', '_RT = open(os.path.join(DL.V400, "runtime_v400.py"), "rb").read().decode("utf-8")   # a secao do selo ACOM (a v401 NAO a muda)')
sub('_fo = os.path.join(HERE, "insumos", "acom", "fontes_operador")', '_fo = os.path.join(DL.V400, "insumos", "acom", "fontes_operador")')
sub('"t", "vb17", "conf_%s" % umsha', '"t", "vb18", "conf_%s" % umsha')
sub('SC.get("esquema") == "um_absoluto_selo_acom/v1 (v400)"', 'SC.get("esquema") == "um_absoluto_selo_acom/v1 (v399)"')
sub("o sidecar sem recusas, esquema v400, tres objetos", "o sidecar sem recusas, esquema v399, tres objetos")
sub("o runtime inteiro da v401 esta no um.py, byte a byte", "o runtime da secao (o da v400) esta no um.py, byte a byte", 2)
sub("nenhum literal de beta no codigo do runtime da v401", "nenhum literal de beta no codigo do runtime da secao")
# C11: a declaracao do operador e' a de 24/10 (a quarta inscricao da v399)
sub("_dd = DC.get(\"declaration\") or {}", "_dd = DC.get(\"declaration\") or {}   # (VERBATIM_ORIGEM/DECLARACAO_IDX: as de 24/10, da v399; as de 25/10 sao VERBATIM_ORIGEM_V401)")

# ---- os registros e a pedra
sub('RN = sorted(ESP["registros_v399"])\n', 'RN = sorted(ESP["registros_v399"]); RN401 = sorted(ESP["registros_v401"])\n')
sub('SA = core.get("selo_pela_propria_tecnologia_v399") or {}; DC = core.get("declaracao_do_operador_v399") or {}\n', 'SA = core.get("selo_pela_propria_tecnologia_v399") or {}; DC = core.get("declaracao_do_operador_v399") or {}\nFA = core.get("falsidade_da_inercia_v401") or {}; CG1 = core.get("cunhagens_v401") or {}; KH1 = core.get("kh_n1_cobertura_v401") or {}\n')
sub("REL_ = {s[\"key\"]: s[\"rel\"] for s in DL.STONES}", "REL_ = {s[\"key\"]: s[\"rel\"] for s in DL.STONES}   # a pedra FalsidadeDaInercia (nova nesta versao)")
sub('for k in ("testemunho",))\nsuporte_ok', 'for k in ("falsidade",))\nsuporte_ok')
sub('for k in ("testemunho",) for t_, p_ in ESP["suporte_das_pedras"][k].items())', 'for k in ("falsidade",) for t_, p_ in ESP["suporte_das_pedras"][k].items())')
sub("ET = ESP[\"testemunho\"]\n", '''ET = ESP["falsidade"]
_ek = ET["estrela"]
estrela_ok = bool(kf.get(_ek["bandeira"]) is True and set(axr.get(_ek["teorema"]) or []) <= TRIO and src_.get(_ek["teorema"]) == REL_["falsidade"])
fal_reg_ok = bool(FA.get("all_verified") is True and V("falsidade_da_inercia_v401") == ESP["registros_v401_veredito_da_falsidade"] and FA.get("does_not_gate_core") is True and FA.get("runtime_executed") is True and (FA.get("mechanics") or {}).get("n_checks") == 7 and all(c_["ok"] for c_ in (FA.get("mechanics") or {}).get("checks") or [])
                  and (FA.get("costless") or {}).get("ok") is True and (FA.get("key_theorem") or {}).get("in_kernel") is True and (FA.get("unconditional") or {}).get("in_kernel") is True and not GUARDA.search(V("falsidade_da_inercia_v401")) and FA.get("beta_ok") is True
                  and _feq({k_: (FA.get("values") or {}).get(k_) for k_ in ESP["falsidade_valores"]}, ESP["falsidade_valores"]))
''')

# ---- DEVE
sub('selo.get("um_version") == "v401" and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) and (selo.get(n) or {}).get("all_verified") is True for n in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"))',
    'selo.get("um_version") == "v401" and all((selo.get(n) or {}).get("verdict") == V(n) and bool(V(n)) and (selo.get(n) or {}).get("all_verified") is True for n in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "falsidade_da_inercia_v401"))\n        and all(((selo.get("registros_v401") or {}).get(n) or {}).get("verdict") == V(n) and bool(V(n)) and ((selo.get("registros_v401") or {}).get(n) or {}).get("all_verified") is True for n in RN401)')
sub('"selo um_version v401; os resumos do selo (selo_pela_propria_tecnologia_v399 e declaracao_do_operador_v399) e registros_v399 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo"',
    '"selo um_version v401; os resumos do selo (selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399 e falsidade_da_inercia_v401), registros_v399 e registros_v401 do selo iguais aos do core (veredito, selagem); o SHA-256 primario do um.py no selo == o do arquivo"')
sub('    "declaracao_do_operador_v399 SELOU:', '    "falsidade_da_inercia_v401 SELOU: veredito == o do ensaio; 7 checagens do calculo no modelo oneScaling (o peso do posto e^{-s}, o fixo pesa zero, o posto inercial seria 1 = 0, o custo t.beta.g > 0) e os valores == os do ensaio; o 0_abs de TGLExt.costless no kernel embutido; a estrela e a composicao no kernel do rito; nao move o gate": fal_reg_ok,\n    "declaracao_do_operador_v399 SELOU:')
sub('"os registros por spec v401 SELARAM e cada veredito == o do ensaio; as quatro inscricoes de 24/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas falas do operador)": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v399"].items())\n        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM) == 4 and all((((CG.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())\n        and not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values()),',
    '"os registros por spec v401 SELARAM e cada veredito == o do ensaio; as cinco inscricoes de 25/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS; todas falas do operador); as ratificacoes (8) e a errata ao lado do adendo (superada pela definicao do operador) estao no registro; os registros da v399 seguem selados e iguais": all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v401"].items() if n != "falsidade_da_inercia_v401")\n        and all((core.get(n) or {}).get("all_verified") is True and V(n) == v for n, v in ESP["registros_v399"].items())\n        and len(ESP["cunhagens"]) == len(DL.VERBATIM_ORIGEM_V401) == 5 and all((((CG1.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True) and (((CG1.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"]) for k_, v_ in ESP["cunhagens"].items())\n        and not any(str(v_.get("papel", "")).startswith("leitura da gerencia") for v_ in ESP["cunhagens"].values())\n        and len(((CG1.get("extras") or {}).get("ratificacoes")) or []) == 8 and len(CG1.get("erratas") or []) == 1 and "SUPERADA" in ((CG1.get("erratas") or [{}])[0].get("agora") or "") and ESP["ratificacao_fala_sha16"] == ((CG1.get("extras") or {}).get("ratificacao_fala") or {}).get("sha16"),')
sub('"a pedra Testemunho esta no kernel do rito (composicao incondicional %s com bandeira %s True, no trio, no modulo da pedra; os dois teoremas do contrato no modulo da pedra; os 11 termos antigos citados no trio e no modulo certo)" % (ET["teorema"].split(".")[-1], ET["bandeira"]): pedras_no_kernel and suporte_ok,',
    '"a pedra FalsidadeDaInercia esta no kernel do rito (composicao %s com bandeira %s True e a estrela %s com bandeira %s True, no trio, no modulo da pedra; as 12 declaracoes do contrato no modulo da pedra; os 7 termos antigos citados no trio e no modulo certo)" % (ET["teorema"].split(".")[-1], ET["bandeira"], _ek["teorema"].split(".")[-1], _ek["bandeira"]): pedras_no_kernel and suporte_ok and estrela_ok,')
sub('"o modulo novo (Testemunho) no kernel do Nos com o sha do candidato (%d modulo)"', '"o modulo novo (FalsidadeDaInercia) no kernel do Nos com o sha do candidato (%d modulo)"')
sub('"o artigo PT/EN: a secao v401 (O testemunho de dois: o selo pela propria tecnologia) e as marcas da v400 e anteriores; a v400, a v397, a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado)"',
    '"o artigo PT/EN: a secao v401 (A falsidade (simulacro) da inercia) e as marcas da v400 e anteriores; a v399 (com a errata da v400), a v398, a v397, a v396, a v395, a v394, a v393, a v392, a v391 e a v390 ficam; os registros selaram (sem as frases de nao selado)"')
sub('"o sumario lista as secoes v401, v400, v397 e v396 e o titulo v384 a v39x"', '"o sumario lista as secoes v401, v399, v398, v397 e v396 e o titulo v384 a v401"')
sub('«O testemunho de dois (v401)», «Sonico e a afinacao das cordas (v400)»', '«A falsidade (simulacro) da inercia (v401)», «Errata ao lado (v400)», «O testemunho de dois (v399)», «Sonico e a afinacao das cordas (v398)»')
sub('ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_testemunho"] in fc and ESP["md_sonico"] in fc', 'ESP["md_carimbo"] in fc and ESP["md_carimbo"] in mf and ESP["md_falsidade"] in fc and ESP["md_errata"] in fc and ESP["md_testemunho"] in fc and ESP["md_sonico"] in fc')
sub('"nenhuma chave nova _v399 fora da lista (so\' selo_pela_propria_tecnologia_v399, declaracao_do_operador_v399 e os registros por spec)": sorted(k for k in core if k not in ESP["vereditos_v400"] and isinstance(core[k], dict) and str(k).endswith("_v399")) == sorted(["selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399"] + RN),',
    '"nenhuma chave nova fora da lista da v401 (so\' falsidade_da_inercia_v401 e os registros por spec cunhagens_v401 e kh_n1_cobertura_v401; os da v399 sao recriados e iguais)": sorted(k for k in core if k not in ESP["vereditos_v400"] and isinstance(core[k], dict) and (str(k).endswith("_v399") or str(k).endswith("_v401"))) == sorted(["falsidade_da_inercia_v401"] + RN401),')
sub('for n_ in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399")) and sha(J(core.get("qg_closure")).encode("utf-8")) == ESP["qg_closure_v400_json_sha256"],', 'for n_ in ("selo_pela_propria_tecnologia_v399", "declaracao_do_operador_v399", "cunhagens_v399", "kh_n1_cobertura_v399", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401")) and sha(J(core.get("qg_closure")).encode("utf-8")) == ESP["qg_closure_v400_json_sha256"],')
sub('"veredito_selo_acom": V("selo_pela_propria_tecnologia_v399"), "veredito_declaracao": V("declaracao_do_operador_v399"),', '"veredito_selo_acom": V("selo_pela_propria_tecnologia_v399"), "veredito_declaracao": V("declaracao_do_operador_v399"), "veredito_falsidade": V("falsidade_da_inercia_v401"),')
ast.parse(t)
open(P + ".tmp", "w", encoding="utf-8", newline="").write(t)
import os
os.replace(P + ".tmp", P)
print("patch aplicado:", P, len(t), "caracteres")

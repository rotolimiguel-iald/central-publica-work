import copy, json, re, sys
src = open("a_a3.py", encoding="utf-8").read().split("rep = {}")[0]
exec(compile(src, "a_a3_head", "exec"))
pos = rodar(copy.deepcopy(core0))
Cc = copy.deepcopy(CONTR); Cc["esperado_do_resultado"]["ramo_primario"] = 5
ref = rodar(copy.deepcopy(core0), contr_=Cc)   # recusado por c7, com values presentes
print("ref: all_verified", ref["all_verified"], "| verdict", ref["verdict"][:90], "| tem values:", "values" in ref, "| cabeca_do_teste presente:", "cabeca_do_teste" in ref)
nomes = ["_V411_TITULO_QUADRO_PT", "_V411_TITULO_SECAO", "_V411_TOPO", "_V411_MARCADORES", "_V411_NAO_DECIDE_EN", "_V411_AB", "_V411_FE", "_V411_FALA_DO_AUTOR", "_V411_ESTATUTO_AO_LADO_PT",
         "_v411_n", "_v411_p", "_v411_tt", "_v411_tex_unicode", "_v411_atomos", "_v411_hora", "_v411_quadro_tex", "_v411_quadro_md", "_v411_secao_tex", "_v411_linha_md", "_v411_tex_misto", "_v411_topo_texto", "_v411_efeitos_tex",
         "_v411_p2_ao_lado_tex", "_v411_estatuto_tex", "_v411_remissao_tex", "_v411_fala_do_autor_tex", "_v411_fala_do_autor_md"]
f.carregar(nomes, ns)
def chamar(fn, *a):
    for _ in range(60):
        try:
            return ns[fn](*a)
        except NameError as e:
            m = re.search(r"name '([A-Za-z_0-9]+)' is not defined", str(e)); f.carregar([m.group(1)], ns)
    raise RuntimeError
def mostra(rot, v):
    s = v if isinstance(v, str) else "\n".join(v) if isinstance(v, (list, tuple)) else repr(v)
    flags = {"tem_sigma_ou_6": bool(re.search(r"6[,.{]|\sigma|σ", s)), "provado/proved": bool(re.search(r"provad|proved", s, re.I)), "len": len(s)}
    print("  %-46s %s | %s" % (rot, flags, s[:150].replace("\n", " ")))
for nome, c in (("SELOU", pos), ("RECUSADO", ref), ("AUSENTE", None)):
    print("==", nome)
    core = copy.deepcopy(core0)
    if c is not None: core["h0dn_bg1_v411"] = copy.deepcopy(c)
    for lang in ("pt", "en"):
        for rot, fn, args in (("topo_texto", "_v411_topo_texto", (core, lang)), ("efeitos_tex", "_v411_efeitos_tex", (core, lang)), ("efeitos_metodo", "_v411_efeitos_tex", (core, lang, "metodo")), ("estatuto_tex", "_v411_estatuto_tex", (core, lang)),
                              ("p2_ao_lado", "_v411_p2_ao_lado_tex", (core, lang)), ("quadro_tex", "_v411_quadro_tex", (core.get("h0dn_bg1_v411"), lang, ns["_V411_TITULO_QUADRO_PT"])), ("secao_tex", "_v411_secao_tex", (core, lang, ns["_V411_TITULO_SECAO"][lang]))):
            try:
                mostra(lang + ":" + rot, chamar(fn, *args))
            except Exception as e:
                print("  %-46s EXCECAO %r" % (lang + ":" + rot, e))
    try:
        mostra("md:linha", chamar("_v411_linha_md", core.get("h0dn_bg1_v411")))
        mostra("md:quadro", chamar("_v411_quadro_md", core.get("h0dn_bg1_v411"), ns["_V411_TITULO_QUADRO_PT"]))
    except Exception as e:
        print("  md EXCECAO %r" % (e,))
print("=========== INSPECAO DO QUADRO/SECAO RECUSADO")
core = copy.deepcopy(core0); core["h0dn_bg1_v411"] = copy.deepcopy(ref)
for lang in ("pt", "en"):
    for rot, fn, args in (("quadro_tex", "_v411_quadro_tex", (core["h0dn_bg1_v411"], lang, ns["_V411_TITULO_QUADRO_PT"])), ("secao_tex", "_v411_secao_tex", (core, lang, ns["_V411_TITULO_SECAO"][lang]))):
        s = "\n".join(chamar(fn, *args)) if not isinstance(chamar(fn, *args), str) else chamar(fn, *args)
        pats = {"6{,}1": r"6\{,\}1|6[.,]1\d", "0{,}6": r"0\{,\}6|-0[.,]6", "4{,}38": r"4\{,\}3|4[.,]3\d", "cabeca BETA_TGL_PRO": r"BETA\?_TGL\?_PRO", "PROVED_IN_NATURE": r"PROVED", "provado na natureza": r"provado\s+na\s+natureza|proved\s+in\s+nature", "NAO selou": r"n[ãa]o\s+selou|did\s+not\s+seal|NOT\s+seal"}
        print(lang, rot, {k: bool(re.search(v, s, re.I)) for k, v in pats.items()})
        if lang == "pt" and rot == "quadro_tex":
            print(s[:1800])
for rot, fn, args in (("md:quadro", "_v411_quadro_md", (core["h0dn_bg1_v411"], ns["_V411_TITULO_QUADRO_PT"])),):
    r = chamar(fn, *args); s = r if isinstance(r, str) else "\n".join(r)
    print(rot, {k: bool(re.search(v, s, re.I)) for k, v in {"6,1": r"6[.,]1\d", "provado na natureza": r"provado\s+na\s+natureza", "NAO selou": r"n[ãa]o\s+selou"}.items()})
    print(s[:1500])
print("=========== REGISTRO COM RUNTIME_ERROR (sem values)")
b = blob("vetor_y255.npz"); I = copy.deepcopy(INS); I["vetor_y255.npz"] = {"b64": base64.b64encode(b[:-1] + bytes([b[-1] ^ 1])).decode("ascii")}
err = rodar(copy.deepcopy(core0), ins_=I)
print("err:", err["verdict"], "| values" in err, "values" in err, "| cabeca" , "cabeca_do_teste" in err)
core = copy.deepcopy(core0); core["h0dn_bg1_v411"] = copy.deepcopy(err)
for lang in ("pt", "en"):
    for rot, fn, args in (("quadro_tex", "_v411_quadro_tex", (core["h0dn_bg1_v411"], lang, ns["_V411_TITULO_QUADRO_PT"])), ("secao_tex", "_v411_secao_tex", (core, lang, ns["_V411_TITULO_SECAO"][lang]))):
        r = chamar(fn, *args); s = r if isinstance(r, str) else "\n".join(r)
        print(lang, rot, "len", len(s), {k: bool(re.search(v, s, re.I)) for k, v in {"6{,}1": r"6\{,\}1|6[.,]1\d", "BETA_TGL_PRO": r"BETA\?_TGL\?_PRO", "NAO selou": r"n[ãa]o\s+selou|did\s+not\s+seal|NOT\s+seal"}.items()})

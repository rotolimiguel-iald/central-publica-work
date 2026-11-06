for p in ("n_hashes_digitados.py", "n2_hashes_docs.py"):
    t = open(p, encoding="utf-8").read()
    t = t.replace(', "orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md"', '')
    t = t.replace('for root in (R, W + "cadeia_de_selo/v408/", W + "cadeia_de_selo/v407/", W + "cadeia_de_selo/v406/", W + "cunhagens_13out/"', 'for root in (R, W + "cadeia_de_selo/v408/", W + "cadeia_de_selo/v407/", W + "cadeia_de_selo/v406/", W + "cadeia_de_selo/v405/", W + "cunhagens_13out/"')
    t = t.replace('"RETOMADA_CONSTRUTOR_v409.md",', '"RETOMADA_CONSTRUTOR_v409.md", "RETOMADA_CONSTRUTOR_v409_2.md", "DEPOSITO_CONSTRUTOR_v409.md",')
    t = t.replace('"pos_rito/textos_v409.py", "pos_rito/textos_custodia_handoff_v409.py", "orquestrador/pos_treino_v409.py")', '"pos_rito/textos_v409.py", "pos_rito/textos_custodia_handoff_v409.py", "orquestrador/pos_treino_v409.py")')
    open(p, "w", encoding="utf-8", newline="\n").write(t)
    print(p, "ok")

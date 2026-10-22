# -*- coding: utf-8 -*-
"""editar_pequenos.py -- DELTA 19/10: edita gerar_esperados_v394.py, conferir_rito_v394.py, diff_e_pinos_v394.py, conferir_citacoes_v394.py, comparar_v393_v394.py e comparar_r8_v394.py (backups de bytes ja' feitos) para a
integracao final: candidato novo (DL.CANDIDATO), pasta kernel_d19, a TROCA DE PALAVRA declarada (THEOREMS -> FLAGS), o registro criterio_binario_de_parada_v394, o h8 e a politica de bandeiras nos ESPERADOS e no conferidor.
Cada troca tem assert de unicidade; cada arquivo passa por ast.parse antes de ser escrito."""
import ast, os, sys
V = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
total = 0


def editar(nome, subs):
    global total
    p = os.path.join(V, nome); t = open(p, "rb").read().decode("utf-8")
    assert "\r" not in t, nome
    for old, new in subs:
        assert t.count(old) == 1, (nome, old[:100], t.count(old))
        t = t.replace(old, new); total += 1
    ast.parse(t)
    open(p + ".tmp", "wb").write(t.encode("utf-8")); os.replace(p + ".tmp", p)
    print("%s: %d trocas; ast.parse ok" % (nome, len(subs)))


# ---------------------------------------------------------------- gerar_esperados
editar("gerar_esperados_v394.py", [
    ('HERE = os.path.dirname(os.path.abspath(__file__))\n', 'HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)\nimport delta19_v394 as DL  # noqa: E402   (DELTA 19/10: candidato novo, kernel_d19)\n'),
    ('assert CM["sha16"] == h16(os.path.join(HERE, "um_v394_candidato.py"))', 'assert CM["sha16"] == h16(os.path.join(HERE, DL.CANDIDATO))'),
    ('FJ = json.load(open(os.path.join(HERE, "kernel", "FLAGS_v394.json"), encoding="utf-8"))', 'FJ = json.load(open(os.path.join(HERE, DL.KERNEL_DIR, "FLAGS_v394.json"), encoding="utf-8"))'),
    ('assert esp["the_iald_index_v393"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v393"], esp["not_sealed_formais"])\n',
     '''esp.update({"troca_de_palavra": ens["vizinhos"].get("palavra_trocada") or {},   # a TROCA DE PALAVRA declarada (THEOREMS -> FLAGS): so' o que o ensaio mediu; o conferidor a aplica ao veredito da v393 antes de comparar
            "h8_entradas": CM["h8"]["entradas"], "h8_residuais_do_nos": CM["h8"]["residuais_do_nos"], "formal_files_n_no_rito": CM["h8"]["entradas"],
            "n_bandeiras_por_grupo": {"tempo": FJ["por_grupo_bandeiras"]["tempo"], "quadratica": FJ["por_grupo_bandeiras"]["quadratica"], "rede": FJ["por_grupo_bandeiras"]["rede"], "outros": FJ["por_grupo_bandeiras"]["outro"]},
            "politica_de_bandeiras": CM["politica_de_bandeiras"], "pedra_do_delta": CM["kernel"]["pedra_do_delta"], "teorema_do_delta": DL.THEOREM, "bandeira_do_delta": DL.FLAG_KEY,
            "criterio_binario": ens["criterio_binario"], "candidato_anterior_sha16": DL.CANDIDATO_ANTERIOR_SHA16})
assert esp["the_iald_index_v393"]["all_verified"] is True and esp["not_sealed_formais"] == [], (esp["the_iald_index_v393"], esp["not_sealed_formais"])
assert set(esp["troca_de_palavra"]) <= set(esp["troca_dita"]) and esp["h8_entradas"] == len(esp["h8_residuais_do_nos"]) + CM["formal_files_n"] and sum(esp["n_bandeiras_por_grupo"].values()) == esp["n_bandeiras_novas"], "os ESPERADOS novos nao fecham"
assert esp["kernel"]["modulos_novos"] == len(esp["pedras_sha256"]) == len(nov), "o numero de modulos novos != a lista"
'''),
])
# ---------------------------------------------------------------- conferir_rito
editar("conferir_rito_v394.py", [
    ('Mudancas ditas: +5 chaves (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394) no core e no selo (+ registros_v394); a escada 7045 -> 10752; os 189 modulos no kernel',
     'Mudancas ditas: +6 chaves (tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394, kh_n1_cobertura_v394, criterio_binario_de_parada_v394) no core e no selo (+ registros_v394); a escada 7045 -> a dos ESPERADOS; os modulos novos (189 do Codex + a pedra do delta) no kernel'),
    ('trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v393"][k] and _num(_nc(V(k))) == _num(_nc(ESP["vereditos_v393"][k])) for k in ESP["troca_dita"])   # MUDOU de fato e so\' em numeros\n',
     '''TP = ESP.get("troca_de_palavra") or {}   # a TROCA DE PALAVRA declarada pela gerencia (THEOREMS -> FLAGS em estatuto_da_prova_v391): so' o que os ESPERADOS declaram
_pw = lambda k, s_: s_.replace(TP[k][0], TP[k][1]) if k in TP else s_
trocas_ok = all(((core.get(k) or {}).get("all_verified") is True) and V(k) != ESP["vereditos_v393"][k] and _num(_nc(V(k))) == _num(_nc(_pw(k, ESP["vereditos_v393"][k]))) and (k not in TP or (TP[k][1] in V(k) and TP[k][0] not in V(k))) for k in ESP["troca_dita"])   # MUDOU de fato e so' em numeros (mais a palavra declarada)
CB = core.get("criterio_binario_de_parada_v394") or {}
'''),
    ('    "tempo_frequencia_v394, regra_quadratica_v394 e rede_fock_v394 SELARAM e cada veredito == o do ensaio; nenhum certificado inteiro da rede":',
     '''    "o registro criterio_binario_de_parada_v394 SELOU: veredito == o do ensaio; as duas falas de 19/10 embutidas por sha256 (embedded_ok e sha256 == os ESPERADOS); a bandeira e o teorema da pedra no kernel do rito, no trio": CB.get("all_verified") is True and V("criterio_binario_de_parada_v394") == ESP["criterio_binario"]["verdict"]
        and all(((CB.get("verbatim") or {}).get(k_) or {}).get("embedded_ok") is True and ((CB.get("verbatim") or {}).get(k_) or {}).get("sha256") == v_["sha256"] for k_, v_ in ESP["criterio_binario"]["verbatim"].items()) and len(ESP["criterio_binario"]["verbatim"]) == 2
        and kf.get(ESP["bandeira_do_delta"]) is True and set(axr.get(ESP["teorema_do_delta"]) or ["?"]) <= TRIO and ((kf.get("declaration_sources_v394") or {}).get(ESP["teorema_do_delta"]) == ESP["pedra_do_delta"]["path"]),
    "o hash formal do rito (a arvore do Nos depois do rito: embutidos + residuais que o hash conta) tem exatamente %d entradas, com os residuais %s" % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]): len(kf.get("formal_files_sha256") or {}) == ESP["h8_entradas"] and all(r_ in (kf.get("formal_files_sha256") or {}) for r_ in ESP["h8_residuais_do_nos"]),
    "tempo_frequencia_v394, regra_quadratica_v394 e rede_fock_v394 SELARAM e cada veredito == o do ensaio; nenhum certificado inteiro da rede":'''),
])
# ---------------------------------------------------------------- diff_e_pinos
editar("diff_e_pinos_v394.py", [
    ('HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote"))\nfrom carregar_embutido import carregar  # noqa: E402\n',
     'HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "v390_pacote")); sys.path.insert(0, HERE)\nfrom carregar_embutido import carregar  # noqa: E402\nimport delta19_v394 as DL  # noqa: E402\n'),
    ('E1, _, _, h1 = carregar(os.path.join(HERE, "um_v394_candidato.py"))', 'E1, _, _, h1 = carregar(os.path.join(HERE, DL.CANDIDATO))'),
    ('"kernel_recibo": f(os.path.join(HERE, "kernel", "KERNEL_RECIBO_v394.json")),\n      "candidato": f(os.path.join(HERE, "um_v394_candidato.py")),', '"kernel_recibo": f(os.path.join(HERE, DL.KERNEL_DIR, "KERNEL_RECIBO_v394.json")),\n      "candidato": f(os.path.join(HERE, DL.CANDIDATO)),'),
])
# ---------------------------------------------------------------- conferir_citacoes
editar("conferir_citacoes_v394.py", [
    ('cg = [s for s in ns["_V394_SPECS"] if s["nome"] == "cunhagens_v394"][0]\nfor it in cg["leituras_do_operador"]:\n    achou = re.sub(r"\\s+", " ", it["trecho"]) in todos\n    R["leituras"][it["trecho"][:70]] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou\n',
     'for nome_ in ("cunhagens_v394", "criterio_binario_de_parada_v394"):   # DELTA 19/10: as leituras do operador dos DOIS registros\n    cg = [s for s in ns["_V394_SPECS"] if s["nome"] == nome_][0]\n    for it in cg["leituras_do_operador"]:\n        achou = re.sub(r"\\s+", " ", it["trecho"]) in todos\n        R["leituras"][nome_ + ": " + it["trecho"][:70]] = "VERBATIM" if achou else "NAO ACHADA"; ok = ok and achou\n'),
])
# ---------------------------------------------------------------- comparar_v393_v394 e comparar_r8
editar("comparar_v393_v394.py", [
    ('HERE = os.path.dirname(os.path.abspath(__file__))\n', 'HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)\nimport delta19_v394 as DL  # noqa: E402\n'),
    ('B = ast.parse(open(os.path.join(HERE, "um_v394_candidato.py"), "rb").read().decode("utf-8"))', 'B = ast.parse(open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8"))'),
])
editar("comparar_r8_v394.py", [
    ('HERE = os.path.dirname(os.path.abspath(__file__))\n', 'HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)\nimport delta19_v394 as DL  # noqa: E402\n'),
    ('MP = os.path.join(HERE, "um_v394_candidato.py")', 'MP = os.path.join(HERE, DL.CANDIDATO)'),
])
print("total de trocas:", total)

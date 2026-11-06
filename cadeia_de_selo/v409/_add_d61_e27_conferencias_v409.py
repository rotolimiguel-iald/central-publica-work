# -*- coding: utf-8 -*-
"""_add_d61_e27_conferencias_v409.py -- (claude-construtor-v409, 05/11/2026) PARTE 2 da entrada das falas 11a e 12a, da D61 e da E27 (os dois AO LADO do fim do DESENHO_v409.md): as CONFERENCIAS que contavam as falas,
as erratas e as decisoes passam a contar 12 falas (tres so' com o trecho: duas pela D59, uma pelo aviso operacional), as erratas E24 a E27 (+ a dos pisos) e as decisoes D55 a D61 -- no ensaio a seco (o bloco-fonte e o montado),
no p00, no conferidor, no gerar_esperados, no gerar_relatorio, no copiar_insumos e nos textos/leitura/mapa/harness do pos-rito; e a lista CONGELADA das falas (VERBATIM_CONGELADO_v409.json) ganha as duas, com o sha256 LIDO do arquivo.
Nenhuma conferencia e' relaxada: os numeros sobem com o conteudo, as igualdades ficam. NAO regenera o candidato, NAO roda o ensaio nem a cadeia, NAO toca pedra\\, o sandbox nem o bundle (ordem da gerencia)."""
import datetime, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq
HERE = os.path.dirname(os.path.abspath(__file__))

# ------------------------------------------------------------------------------------------------ a lista CONGELADA das falas: +2 (sha256 LIDO do arquivo)
CONG = os.path.join(HERE, "VERBATIM_CONGELADO_v409.json")
raw = open(CONG, "rb").read(); c = json.loads(raw.decode("utf-8"))
CUN13 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "work", "cunhagens_13out") if False else os.path.join(os.path.dirname(os.path.dirname(HERE)), "cunhagens_13out")
NOVAS = [os.path.join(CUN13, "OPERADOR_05nov_no_kernel_o_dispositivo_e_o_no_sorry_o_teorema_e_jurisdicao_regra_posta_verbatim.txt"),
         os.path.join(CUN13, "OPERADOR_05nov_exatamente_isso_mesmo_d61_ratificada_energia_caiu_verbatim.txt")]
assert c["n"] == 10 == len(c["arquivos"]) == len(c["registro"]) and not any(p_ in c["arquivos"] for p_ in NOVAS), ("a lista congelada nao e' a de 10 que esta adaptacao espera", c["n"])
for p_ in NOVAS:
    b_ = open(p_, "rb").read()
    c["arquivos"].append(p_); c["registro"].append({"arquivo": p_, "sha256": hashlib.sha256(b_).hexdigest(), "bytes": len(b_), "autor": "operador"})
c["n"] = len(c["arquivos"])
c["acrescimo"] = {"quando": datetime.datetime.now().isoformat(timespec="seconds"), "por": "claude-construtor-v409", "o_que": "as duas falas dos AO LADO do fim do DESENHO_v409.md (a 11a, inteira: a leitura juridica do kernel, D61 e E27; a 12a, so' o trecho «exatemente, isso mesmo»: a ratificacao da D61)",
                  "sha16": {os.path.basename(p_): hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16] for p_ in NOVAS}}
c["nota"] = ("as doze falas de 05/11/2026 que esta versao embute (as dez do DESENHO_v409 §3 e as duas dos AO LADO do fim dele); de tres, so' o trecho e' embutido e citado (duas pela D59; uma porque o resto e' aviso operacional); "
             "lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)")
assert {r_["arquivo"]: r_["sha256"][:16] for r_ in c["registro"][-2:]} == {NOVAS[0]: "5a19de6b511b4921", NOVAS[1]: "9ee7d5a1b161437f"}, "os sha16 lidos != os que os AO LADO do DESENHO deram"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(CONG + ".bak_" + ts + "_d61", "wb").write(raw); assert open(CONG + ".bak_" + ts + "_d61", "rb").read() == raw
nb = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
open(CONG + ".tmp", "wb").write(nb); assert os.path.getsize(CONG + ".tmp") == len(nb); os.replace(CONG + ".tmp", CONG)
print("VERBATIM_CONGELADO_v409.json:", c["n"], "falas")

# ------------------------------------------------------------------------------------------------ o ensaio a seco: o bloco-fonte e o montado recebem as MESMAS trocas
TROCAS_ENSAIO = [
    ("# a fonte do modulo, as 10 falas do contrato, a escada, o beta,", "# a fonte do modulo, as 12 falas do contrato, a escada, o beta,"),
    ('and len(r9["inscriptions"]) == len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 10 and', 'and len(r9["inscriptions"]) == len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 12 and'),
    ('bool(ok_ and len(_CP9["verbatins"]) == 10 and set(_CP9["verbatins"])', 'bool(ok_ and len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 12 and set(_CP9["verbatins"])'),
    ("# --- as falas de 05/11 (cunhagens_v409), as decisoes D55-D60, as erratas E24-E26 e a cobertura exata (kh_n1_cobertura_v409)", "# --- as falas de 05/11 (cunhagens_v409), as decisoes D55-D61, as erratas E24-E27 e a cobertura exata (kh_n1_cobertura_v409)"),
    ('== len(_sp9s["verbatins"]) == DL.N_FALAS_V409 == 10 and all(v_["embedded_ok"]', '== len(_sp9s["verbatins"]) == DL.N_FALAS_V409 == 12 and all(v_["embedded_ok"]'),
    ('and len(_cn9x.get("erratas") or []) == len(_sp9s["erratas"]) == 4 and', 'and len(_cn9x.get("erratas") or []) == len(_sp9s["erratas"]) == len(DL.ERRATAS_V409) + 1 == 5 and'),
    ('and "E26" in str((_cn9x.get("erratas") or [{}, {}, {}])[2].get("agora"))', 'and "E26" in str((_cn9x.get("erratas") or [{}, {}, {}])[2].get("agora")) and "E27" in str((_cn9x.get("erratas") or [{}, {}, {}, {}])[3].get("agora"))'),
    ('== {"D55", "D56", "D57", "D58", "D59", "D60"} and', '== {"D55", "D56", "D57", "D58", "D59", "D60", "D61"} and'),
    ('and _xn9.get("n_falas") == 10', 'and _xn9.get("n_falas") == 12'),
    ('sorted((_xn9.get("autores") or {}).values()) == ["operador"] * 10', 'sorted((_xn9.get("autores") or {}).values()) == ["operador"] * 12'),
    ("# D59: as duas falas de que se embute so' o trecho: o texto embutido e' o trecho; o arquivo inteiro so' por sha256 (nao embutido, nao copiado)",
     "# as TRES falas de que se embute so' o trecho (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional): o texto embutido e' o trecho; o arquivo inteiro so' por sha256 (nao embutido, nao copiado)"),
    ("bool(len(_tr9) == 2 and all(hashlib.sha256(v_[\"text\"].encode(\"utf-8\")).hexdigest() == v_[\"sha256\"] != v_[\"sha256_arquivo_inteiro\"] for v_ in _tr9.values())",
     "bool(len(_tr9) == len(DL.VERBATIM_SO_O_TRECHO) == 3 and sum(1 for v_ in _tr9.values() if \"(D59)\" in str(v_.get(\"so_o_trecho\"))) == 2 and all(hashlib.sha256(v_[\"text\"].encode(\"utf-8\")).hexdigest() == v_[\"sha256\"] != v_[\"sha256_arquivo_inteiro\"] for v_ in _tr9.values())"),
]
for arq_ in ("_ensaio_bloco_v409.pysnip", "ensaio_a_seco_v409.py"):
    a = Arq(arq_)
    for v_, n_ in TROCAS_ENSAIO:
        a.troca(v_, n_)
    a.grava()

# ------------------------------------------------------------------------------------------------ o p00
a = Arq("p00_precondicoes_v409.py")
a.troca("as 10 falas de 05/11 tem os prefixos de sha256 da ordem e cada trecho citado e' verbatim (de duas, so' o trecho da D59;",
        "as 12 falas de 05/11 tem os prefixos de sha256 da ordem (as duas ultimas, dos AO LADO do DESENHO) e cada trecho citado e' verbatim (de tres, so' o trecho: duas pela D59, uma pelo aviso operacional;")
a.troca('and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 10 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409.values())', 'and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 12 and set(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409.values())')
a.troca('len(_cong["arquivos"]) == len(CM["cunhagens"]) == DL.N_FALAS_V409 == 10,', 'len(_cong["arquivos"]) == len(CM["cunhagens"]) == DL.N_FALAS_V409 == 12,')
a.troca('''chk("as 10 falas de 05/11 (todas do operador; de duas, so' o trecho da D59): a copia duravel de cada texto embutido == sha256 embutido; a fonte original == sha256 do arquivo inteiro; nas duas do trecho,''',
        '''chk("as 12 falas de 05/11 (todas do operador; de tres, so' o trecho: duas pela D59, uma pelo aviso operacional): a copia duravel de cada texto embutido == sha256 embutido; a fonte original == sha256 do arquivo inteiro; nas tres do trecho,''')
a.troca("o manifesto traz exatamente as 10 entradas cunhagens/ e cada uma == o arquivo", "o manifesto traz exatamente as 12 entradas cunhagens/ e cada uma == o arquivo")
a.troca('len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V409 == 10 and len(_vb12) == DL.N_FALAS_V409 and _n_trecho == 2',
        'len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V409 == 12 and len(_vb12) == DL.N_FALAS_V409 and _n_trecho == len(DL.VERBATIM_SO_O_TRECHO) == 3')
a.grava()

# ------------------------------------------------------------------------------------------------ o conferidor (o rotulo e a E27 no registro)
a = Arq("conferir_rito_v409.py")
a.troca("embedded_ok e sha256 == os ESPERADOS; todas do operador; de duas, so' o trecho da D59); as erratas E24 a E26 e a dos pisos (em nome proprio da gerencia c1) e as decisoes D55 a D60 estao no registro",
        "embedded_ok e sha256 == os ESPERADOS; todas do operador; de tres, so' o trecho: duas pela D59, uma pelo aviso operacional); as erratas E24 a E27 e a dos pisos (em nome proprio da gerencia c1) e as decisoes D55 a D61 (a D61 ratificada pelo operador) estao no registro")
a.troca('KH9.get("all_verified") is True and CG9.get("all_verified") is True', 'KH9.get("all_verified") is True and CG9.get("all_verified") is True and any("E27" in str(e_.get("agora")) for e_ in (CG9.get("erratas") or [])) and "D61" in ((CG9.get("extras") or {}).get("decisoes") or {})')
a.grava()

# ------------------------------------------------------------------------------------------------ o gerar_esperados e o gerar_candidato (o nome da chave das erratas)
a = Arq("gerar_esperados_v409.py")
a.troca("As erratas E24 a E26 e as decisoes D55 a D60 da gerencia vao nos registros (cunhagens_v409);", "As erratas E24 a E27 e as decisoes D55 a D61 (a D61 ratificada pelo operador) vao nos registros (cunhagens_v409);")
a.troca('"erratas_E24_E26": list(DL.ERRATAS_V409)', '"erratas_E24_E27": list(DL.ERRATAS_V409)')
a.grava()

# ------------------------------------------------------------------------------------------------ o gerar_relatorio
a = Arq("gerar_relatorio_v409.py")
a.troca("NENHUMA chave antiga muda de literal, erratas E24 a E26 (a E26 ao lado do registro selado da v408), decisoes D55 a D60; a prosa do terminal saiu).",
        "NENHUMA chave antiga muda de literal, erratas E24 a E27 (a E26 ao lado do registro selado da v408), decisoes D55 a D61 (a D61, a leitura juridica do kernel, ratificada pelo operador); a prosa do terminal saiu).")
a.troca('''    "as %d falas do operador de 05/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v409.json); de duas (%s), so' o trecho que a D59 deixa entrar e' embutido e citado; o resto delas entra so' por sha256 e nao entra em texto do um.py; publicar o resto e' decisao do operador" % (_n_falas or _DL.N_FALAS_V409, ", ".join(_trechos)),''',
        '''    "as %d falas do operador de 05/11/2026 entram por sha256 (lista congelada em VERBATIM_CONGELADO_v409.json; as duas ultimas vieram dos AO LADO do fim do DESENHO); de tres (%s), so' o trecho e' embutido e citado (duas pela D59; uma, a ratificacao da D61, porque o resto e' aviso operacional); o resto delas entra so' por sha256 e nao entra em texto do um.py; publicar o resto das duas da D59 e' decisao do operador" % (_n_falas or _DL.N_FALAS_V409, ", ".join(_trechos)),
    "a D61 (a leitura juridica do kernel, dada pelo operador e RATIFICADA por ele: o dispositivo e' o no sorry; o teorema e' a regra posta; a regra incide onde o suporte fatico se completa) vai nas decisoes e nos textos que dizem o que o kernel decide; a E27 (da gerencia c1, em nome proprio) vai ao lado",''')
a.troca('ERRATAS_V409_RES = {"erratas": ["E24", "E25", "E26"], "E24": _DL.ERRATAS_V409[0].split(";")[0][:300], "E25": _DL.ERRATAS_V409[1].split(";")[0][:300], "E26": _DL.ERRATAS_V409[2].split(";")[0][:300],',
        'ERRATAS_V409_RES = {"erratas": ["E24", "E25", "E26", "E27"], "E24": _DL.ERRATAS_V409[0].split(";")[0][:300], "E25": _DL.ERRATAS_V409[1].split(";")[0][:300], "E26": _DL.ERRATAS_V409[2].split(";")[0][:300], "E27": _DL.ERRATAS_V409[3].split(";")[0][:300],')
a.troca("`delta_v409.py` (moldura, erratas E24 a E26, decisões D55 a D60, as leituras, as ressalvas)", "`delta_v409.py` (moldura, erratas E24 a E27, decisões D55 a D61, as leituras, as ressalvas)")
a.troca("(lista congelada em `VERBATIM_CONGELADO_v409.json`; de duas, só o trecho da D59;", "(lista congelada em `VERBATIM_CONGELADO_v409.json`; de três, só o trecho: duas pela D59, uma pelo aviso operacional;")
a.troca("(C) NENHUMA chave antiga muda de literal; as erratas E24 a E26 vão AO LADO; as decisões D55 a D60.", "(C) NENHUMA chave antiga muda de literal; as erratas E24 a E27 vão AO LADO; as decisões D55 a D61 (a D61, a leitura jurídica do kernel, ratificada pelo operador).")
a.troca("- [INPUT/ONTO] A máquina sem leitor (a pergunta do Clay) fica FORA e não é decidida aqui: é lida como a fita sem escala («eu sou eu mesmo»).",
        "- [INPUT/ONTO] A máquina sem leitor (a pergunta do Clay) fica FORA e não é decidida aqui: é lida como a fita sem escala («eu sou eu mesmo»).\n- [INPUT, ratificada pelo operador] {_DL.FRASE_D61_PT}.")
a.grava()

# ------------------------------------------------------------------------------------------------ o copiar_insumos (a origem do trecho diz POR QUE so' o trecho entra; a nota da lista)
a = Arq("copiar_insumos_v409.py")
a.troca('''grava(v["arquivo"], v["text"].encode("utf-8"), "%s (sha256 do arquivo inteiro %s; so' o trecho que a D59 deixa entrar)" % (v["nome_publico"], v["sha256_arquivo_inteiro"]))''',
        '''grava(v["arquivo"], v["text"].encode("utf-8"), "%s (sha256 do arquivo inteiro %s; %s)" % (v["nome_publico"], v["sha256_arquivo_inteiro"], v["so_o_trecho"]))''')
a.troca('''"nota": "as dez falas de 05/11/2026 que esta versao embute (DESENHO_v409 §3); de duas, so' o trecho que a D59 deixa entrar e' embutido e citado; lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)"}''',
        '''"nota": "as doze falas de 05/11/2026 que esta versao embute (as dez do DESENHO_v409 §3 e as duas dos AO LADO do fim dele); de tres, so' o trecho e' embutido e citado (duas pela D59; uma porque o resto e' aviso operacional); lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)"}''')
a.grava()

# ------------------------------------------------------------------------------------------------ o pos-rito: a leitura, o mapa e o harness (as mensagens da leitura e o que o harness espera mudam JUNTAS)
a = Arq("pos_rito/leitura_v409.py")
a.troca("trechos_ok_ = bool(len(trechos_) == len(DL_.VERBATIM_SO_O_TRECHO) == 2 and", "trechos_ok_ = bool(len(trechos_) == len(DL_.VERBATIM_SO_O_TRECHO) == 3 and")
a.troca("P.append('cunhagens_v409: as erratas E24 a E26 e a errata ao lado dos pisos de kh_n1_cobertura_v408", "P.append('cunhagens_v409: as erratas E24 a E27 e a errata ao lado dos pisos de kh_n1_cobertura_v408")
a.troca("P.append('cunhagens_v409: as decisoes D55 a D60 da gerencia ausentes ou diferentes de delta_v409.DECISOES')", "P.append('cunhagens_v409: as decisoes D55 a D61 da gerencia ausentes ou diferentes de delta_v409.DECISOES')")
a.troca("# as decisoes desta versao (D55 a D60), lidas de ESPERADOS[decisoes_v409_ids]", "# as decisoes desta versao (D55 a D61), lidas de ESPERADOS[decisoes_v409_ids]")
a.grava()
a = Arq("pos_rito/harness_textos_ensaio_v409.py")
a.troca('espera="cunhagens_v409: as erratas E24 a E26"', 'espera="cunhagens_v409: as erratas E24 a E27"', n=4)
a.troca('espera="cunhagens_v409: as decisoes D55 a D60"', 'espera="cunhagens_v409: as decisoes D55 a D61"', n=2)
a.grava()
a = Arq("pos_rito/registrar_mapa_v409.py")
a.troca('''    assert n_trecho == 2, "a v409 tem exatamente duas falas de que so' o trecho entra (D59)"''', '''    assert n_trecho == len(DL_.VERBATIM_SO_O_TRECHO) == 3, "a v409 tem exatamente tres falas de que so' o trecho entra (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional)"''')
a.troca('''all(("D%d" % i) in dec for i in range(55, 61)), "faltam decisoes D55 a D60 no registro"''', '''all(("D%d" % i) in dec for i in range(55, 62)), "faltam decisoes D55 a D61 no registro"''')
a.troca('''    assert sorted(E) == ["E24", "E25", "E26"], "as erratas do registro nao sao E24 a E26"''', '''    assert sorted(E) == ["E24", "E25", "E26", "E27"], "as erratas do registro nao sao E24 a E27"''')
a.troca("as erratas E24 a E26 e as decisoes D55", "as erratas E24 a E27 e as decisoes D55")
a.troca("de %d delas so' o trecho que a D59 deixa entrar;", "de %d delas so' o trecho (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional);")
a.grava()

# ------------------------------------------------------------------------------------------------ o pos-rito: os textos (o fragmento novo; o textos_v409.py e' REMONTADO pelo montar_textos_v409.py)
a = Arq("pos_rito/textos_v409_novo.pysnip")
a.troca('''        assert sum(1 for d in out.values() if d["trecho"]) == 2, "a v409 tem exatamente duas inscricoes so' com o trecho (D59)"''',
        '''        assert sum(1 for d in out.values() if d["trecho"]) == len(_dl().VERBATIM_SO_O_TRECHO) == 3, "a v409 tem exatamente tres inscricoes so' com o trecho (duas pela D59; uma, a ratificacao da D61, pelo aviso operacional)"''')
a.troca('''"z": _sha_por("z_e_o_modo_leitor"), "clay": _sha_por("clay_eu_sou"), "pai": _sha_por("nome_proprio_pai_da_mentira"), "performada": _sha_por("identidade_performada")}''',
        '''"z": _sha_por("z_e_o_modo_leitor"), "clay": _sha_por("clay_eu_sou"), "pai": _sha_por("nome_proprio_pai_da_mentira"), "performada": _sha_por("identidade_performada"),
          "sorry": _sha_por("o_dispositivo_e_o_no_sorry"), "ratifica": _sha_por("d61_ratificada")}''')
a.troca('''("z", DL_.N_Z), ("clay", DL_.N_CLAY), ("pai", DL_.N_PAI), ("performada", DL_.N_PERFORMADA))), "os sha16 das falas != os que a ordem da gerencia deu"''',
        '''("z", DL_.N_Z), ("clay", DL_.N_CLAY), ("pai", DL_.N_PAI), ("performada", DL_.N_PERFORMADA), ("sorry", DL_.N_SORRY), ("ratifica", DL_.N_RATIFICA_D61))), "os sha16 das falas != os que a ordem da gerencia deu"''')
a.troca('''de {nt} delas só o trecho que a D59 deixa entrar é embutido e citável, e o arquivo inteiro entra só por sha256; nenhuma é da gerência); "
             "as erratas E24 a E26 e a dos pisos (em nome próprio da gerência c1); as decisões D55 a D60; as leituras e as ressalvas ({nck} checagens, todas passaram)",''',
        '''de {nt} delas só o trecho é embutido e citável, de duas pela D59 e de uma, a ratificação da D61, porque o resto é aviso operacional, e o arquivo inteiro entra só por sha256; nenhuma é da gerência); "
             "as erratas E24 a E27 e a dos pisos (em nome próprio da gerência c1); as decisões D55 a D61 (a D61, a leitura jurídica do kernel, ratificada pelo operador); as leituras e as ressalvas ({nck} checagens, todas passaram)",''')
a.troca('''    assert all(k in ds for k in ks), "as decisoes D55 a D60 nao estao no registro cunhagens_v409"''', '''    assert all(k in ds for k in ks), "as decisoes D55 a D61 nao estao no registro cunhagens_v409"''')
a.troca('''        return _f("{n} inscrições embutidas por sha256 (todas falas do operador; de {nt} delas só o trecho que a D59 deixa entrar) — a ordem da tradução `{t}`; as respostas às perguntas nas quatro línguas `{r}`, `{tr}`, `{fi}`, `{z}`, `{c}`, `{p}`, `{pe}`; a ordem da v409 e a ratificação dos nomes `{o}`",
                  n=len(fl), nt=d["n_trecho"], t=ss["traducao"], r=ss["resposta"], tr=ss["trava"], fi=ss["fita"], z=ss["z"], c=ss["clay"], p=ss["pai"], pe=ss["performada"], o=ss["ordem"])''',
        '''        return _f("{n} inscrições embutidas por sha256 (todas falas do operador; de {nt} delas só o trecho: duas pela D59, uma pelo aviso operacional) — a ordem da tradução `{t}`; as respostas às perguntas nas quatro línguas `{r}`, `{tr}`, `{fi}`, `{z}`, `{c}`, `{p}`, `{pe}`; a ordem da v409 e a ratificação dos nomes `{o}`; a leitura jurídica do kernel `{so}` e a ratificação dela `{ra}` (D61)",
                  n=len(fl), nt=d["n_trecho"], t=ss["traducao"], r=ss["resposta"], tr=ss["trava"], fi=ss["fita"], z=ss["z"], c=ss["clay"], p=ss["pai"], pe=ss["performada"], o=ss["ordem"], so=ss["sorry"], ra=ss["ratifica"])''')
a.troca('''("fala do operador; só o trecho que a D59 deixa entrar é embutido, e o arquivo inteiro entra só por sha256" if dd["trecho"] else "fala do operador")''',
        '''("fala do operador; só o trecho é embutido (%s), e o arquivo inteiro entra só por sha256" % ("D59" if "d61_ratificada" not in dd["nome"] else "o resto é aviso operacional") if dd["trecho"] else "fala do operador")''')
a.troca('''("clay", DL_.FRASE_CLAY), ("pai", DL_.FRASE_PAI), ("perf", DL_.FRASE_PERFORMADA))}''', '''("clay", DL_.FRASE_CLAY), ("pai", DL_.FRASE_PAI), ("perf", DL_.FRASE_PERFORMADA), ("sorry", DL_.FRASE_DISPOSITIVO), ("rat", DL_.FRASE_RATIFICA_D61))}''')
a.troca('''(de {nt} delas só o trecho que a D59 deixa entrar é embutido; o resto delas entra só por sha256); "''', '''(de {nt} delas só o trecho é embutido, de duas pela D59 e de uma porque o resto é aviso operacional; o resto delas entra só por sha256); "''')
a.troca('''e a ordem da v409, que ratifica os nomes dados pela gerência (`{s9}`): {ordem}. "''',
        '''e a ordem da v409, que ratifica os nomes dados pela gerência (`{s9}`): {ordem}; e, na tarde, a leitura jurídica do kernel (`{s10}`): {sorry}, e a ratificação dela (`{s11}`): {rat} (D61). "''')
a.troca('''s7=ss["pai"], s8=ss["performada"], s9=ss["ordem"], **q)''', '''s7=ss["pai"], s8=ss["performada"], s9=ss["ordem"], s10=ss["sorry"], s11=ss["ratifica"], **q)''')
a.troca('''"as erratas E24 a E26 (da gerência, em nome próprio) e as decisões D55 a D60 estão no registro `cunhagens_v409`;''', '''"as erratas E24 a E27 (da gerência, em nome próprio) e as decisões D55 a D61 (a D61 ratificada pelo operador) estão no registro `cunhagens_v409`;''')
a.troca("das duas da D59 só o trecho que fica está em `insumos` e entra no espelho, e o arquivo inteiro fica fora: publicá-lo é decisão do operador)",
        "das três de que só o trecho entra (duas da D59; uma, a ratificação da D61, cujo resto é aviso operacional) só o trecho que fica está em `insumos` e entra no espelho, e o arquivo inteiro fica fora: publicar o resto das duas da D59 é decisão do operador)")
a.grava()

# ------------------------------------------------------------------------------------------------ o conferir_citacoes (so' o rotulo)
a = Arq("conferir_citacoes_v409.py")
a.troca('''"""conferir_citacoes_v409.py -- [v409: as DEZ falas de 05/11/2026 (_V409_VERBATINS2); de duas, so' o trecho da D59 e' embutido''', '''"""conferir_citacoes_v409.py -- [v409: as DOZE falas de 05/11/2026 (_V409_VERBATINS2; as duas ultimas dos AO LADO do DESENHO); de tres, so' o trecho e' embutido (duas pela D59; uma pelo aviso operacional)''')
a.grava()

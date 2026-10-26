# -*- coding: utf-8 -*-
"""acom_conferencias_v399.py -- as CONFERENCIAS da cadeia sobre o ESTUDO do selo pela propria tecnologia (insumos\\acom), todas por script, nenhuma de memoria. Importado por montar_runtime_v399, gerar_candidato_v399,
p00_precondicoes_v399, ensaio_a_seco_v399 e conferir_rito_v399.
 C1 (identidade do metodo): o bloco embutido do estudo e' a COPIA das fontes do operador (acom_mirror.py e acom_crypto.py, as copias duraveis em insumos\\acom\\fontes_operador) com as 5 substituicoes declaradas (SUBST abaixo, copiadas de
    montar_prototipo.py do estudo e comparadas com o EMBUTIDO_MANIFESTO.json); a cadeia REFAZ o bloco e compara byte a byte, e o hash do bloco (do primeiro marcador de inicio ao ultimo de fim, em LF) e' o do manifesto e o da ACOM_PROVENIENCIA;
 C2 (pinos das fontes): o sha256 de cada uma das 6 fontes do operador citadas na ACOM_PROVENIENCIA == o do arquivo duravel == o do EMBUTIDO_MANIFESTO;
 C3 (colisao de nomes): os nomes de nivel de modulo que a secao define, contra os do um.py base: so' os imports do mesmo modulo e ALPHA_FINE_CODATA_2018 (mesmo valor) podem colidir;
 C9 (beta nunca literal): nenhum numero literal de beta, de alfa ao quadrado ou de 0,012 no CODIGO do bloco embutido e da adaptacao (tokenize; comentarios e textos de prosa ficam fora).
Molde do metodo: montar_prototipo.py do estudo (work\\v399_selo_e_testemunho)."""
import ast, hashlib, io, json, math, os, re, tokenize

HERE = os.path.dirname(os.path.abspath(__file__))
AC = os.path.join(HERE, "insumos", "acom")
FO = os.path.join(AC, "fontes_operador")
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda p: open(p, "rb").read()

PRIMEIRA = {"mirror": 22, "crypto": 22}      # primeira linha (1-based) do corpo copiado: depois do docstring do modulo e antes dos imports
SUBST = {    # as 5 SUBSTITUICOES declaradas (copiadas de montar_prototipo.py do estudo; cada uma ocorre EXATAMENTE uma vez)
    "mirror": [
        ("from . import tgl_core\n",
         "# (removido no embutido) from . import tgl_core  -- beta e theta_M vem de _beta_runtime() e _theta_m_runtime() (ALPHA_FINE_CODATA_2018 * sqrt(e))\n"),
        ("self.beta = tgl_core.beta()            # runtime, never literal",
         "self.beta = _beta_runtime()            # runtime, never literal"),
        ("self.theta_miguel = tgl_core.theta_m()",
         "self.theta_miguel = _theta_m_runtime()"),
    ],
    "crypto": [
        ("from . import tgl_core\nfrom .acom_mirror import DimensionalMirror, MirrorReflection, _unpack2bits, PARITY\n",
         "# (removidos no embutido) from . import tgl_core ; from .acom_mirror import ... -- os nomes ja estao neste modulo (bloco acom_mirror acima)\n"),
        ("self.beta = tgl_core.beta()   # runtime",
         "self.beta = _beta_runtime()   # runtime"),
    ],
}
PATENTE = {"mirror": "BR 10 2026 003428-2", "crypto": "BR 10 2026 003431-2"}
ARQ_DO_BLOCO = {"mirror": "acom_mirror.py", "crypto": "acom_crypto.py"}
FIM_MARCA = "# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/acom_crypto.py <<<\n"
INI_MARCA = "# >>> ACOM_EMBUTIDO_INICIO"
MANIFESTO = os.path.join(AC, "EMBUTIDO_MANIFESTO.json")


def lf(t):
    return t.replace("\r\n", "\n")


def bloco_das_fontes():
    """Refaz o bloco embutido a partir das copias duraveis das fontes do operador. Devolve (texto_em_LF, sha256, info_por_bloco)."""
    blocos, info = {}, {}
    for k in ("mirror", "crypto"):
        fonte = rb(os.path.join(FO, ARQ_DO_BLOCO[k]))
        txt = fonte.decode("utf-8").replace("\r\n", "\n")
        linhas = txt.split("\n")
        corpo = "\n".join(linhas[PRIMEIRA[k] - 1:]).rstrip("\n") + "\n"
        n_sub = 0
        for velho, novo in SUBST[k]:
            assert corpo.count(velho) == 1, ("substituicao declarada nao casa exatamente uma vez", k, velho[:60], corpo.count(velho))
            corpo = corpo.replace(velho, novo); n_sub += 1
        sem_coment = "\n".join(l.split("#")[0] for l in corpo.split("\n"))
        assert "tgl_core." not in sem_coment, "sobrou uso de tgl_core no embutido " + k
        assert not re.search(r"0[.,]012", corpo), "literal 0,012 no embutido " + k
        ini = ("# >>> ACOM_EMBUTIDO_INICIO: skygrid_sim/%s (sha256 %s) -- patente %s -- linhas %d-%d do fonte, com %d substituicao(oes) declarada(s) no EMBUTIDO_MANIFESTO.json >>>\n"
               % (ARQ_DO_BLOCO[k], sha(fonte), PATENTE[k], PRIMEIRA[k], len(linhas) - (1 if linhas[-1] == "" else 0), n_sub))
        fim = "# <<< ACOM_EMBUTIDO_FIM: skygrid_sim/%s <<<\n" % ARQ_DO_BLOCO[k]
        blocos[k] = ini + corpo + fim
        info[k] = {"fonte_sha256": sha(fonte), "substituicoes": n_sub, "texto_embutido_sha256": sha(corpo.encode("utf-8")), "linhas_embutidas": corpo.count("\n")}
    emb = blocos["mirror"] + "\n" + blocos["crypto"]
    return emb, sha(emb.encode("utf-8")), info


def extrair_bloco(texto):
    """O trecho do primeiro marcador de inicio ao ultimo marcador de fim (inclusive), em LF, de um texto (a secao ou o um.py)."""
    t = lf(texto)
    assert t.count(INI_MARCA) >= 2 and t.count(FIM_MARCA) == 1, ("marcadores do bloco embutido", t.count(INI_MARCA), t.count(FIM_MARCA))   # 2 inicios (mirror e crypto) + a mencao em conferir_bloco_embutido(); o bloco comeca no PRIMEIRO
    i = t.index(INI_MARCA)
    return t[i:t.index(FIM_MARCA) + len(FIM_MARCA)]


def proveniencia(texto):
    """A constante ACOM_PROVENIENCIA da secao, por ast (sem executar)."""
    tr = ast.parse(texto)
    for n in tr.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "ACOM_PROVENIENCIA":
            return ast.literal_eval(n.value)
    raise AssertionError("ACOM_PROVENIENCIA ausente")


def nomes_de_nivel_de_modulo(texto):
    tr = ast.parse(texto)
    nomes = set()
    for n in tr.body:
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
            nomes.add(n.name)
        elif isinstance(n, ast.Assign):
            for t in n.targets:
                for x in ast.walk(t):
                    if isinstance(x, ast.Name):
                        nomes.add(x.id)
        elif isinstance(n, (ast.AnnAssign, ast.AugAssign)) and isinstance(n.target, ast.Name):
            nomes.add(n.target.id)
        elif isinstance(n, ast.Import):
            for a in n.names:
                nomes.add((a.asname or a.name).split(".")[0])
        elif isinstance(n, ast.ImportFrom):
            for a in n.names:
                nomes.add(a.asname or a.name)
    return nomes


def literais_de_beta(texto):
    """Numeros literais (tokens NUMBER) que sao beta (alfa x raiz de e), alfa ao quadrado ou 0,012, no CODIGO do texto (tokenize: comentarios e strings ficam fora)."""
    alfa = 0.0072973525693
    beta = alfa * math.sqrt(math.e)
    ruins = []
    for tk in tokenize.generate_tokens(io.StringIO(texto).readline):
        if tk.type == tokenize.NUMBER:
            try:
                v = float(tk.string.replace("_", ""))
            except ValueError:
                continue
            if abs(v - beta) < 1e-6 or abs(v - alfa * alfa) < 1e-9 or abs(v - 0.012) < 1e-9:
                ruins.append((tk.start[0], tk.string))
    return ruins


def conferir_secao(secao_texto, um_base_texto=None, nomes_base=None):
    """Roda C1, C2, C3 e C9 sobre o texto da secao (como esta no insumo ou como foi montada). Devolve {id: {ok, detalhe}}; nada levanta (o chamador decide)."""
    R = {}
    man = json.load(open(MANIFESTO, encoding="utf-8"))
    prov = proveniencia(secao_texto)
    emb, h_emb, info = bloco_das_fontes()
    bloco_secao = extrair_bloco(secao_texto)
    R["C1_bloco_igual_ao_refeito_das_fontes"] = {"ok": bloco_secao == emb, "detalhe": {"sha256_refeito": h_emb, "sha256_da_secao": sha(bloco_secao.encode("utf-8"))}}
    R["C1_hash_do_bloco_igual_ao_manifesto_e_a_proveniencia"] = {"ok": h_emb == man["bloco_embutido_completo_sha256"] == prov["bloco_embutido_sha256"], "detalhe": {"manifesto": man["bloco_embutido_completo_sha256"][:16], "proveniencia": prov["bloco_embutido_sha256"][:16]}}
    sub_man = {k: [(s["velho"], s["novo"]) for s in man["blocos"][k]["substituicoes"]] for k in ("mirror", "crypto")}
    sub_aqui = {k: [(v.strip("\n"), n.strip("\n")) for v, n in SUBST[k]] for k in ("mirror", "crypto")}
    R["C1_substituicoes_declaradas_iguais_as_do_manifesto"] = {"ok": sub_man == sub_aqui and sum(len(v) for v in sub_aqui.values()) == 5, "detalhe": sum(len(v) for v in sub_aqui.values())}
    pins = {}
    ok2 = True
    esperado = {"acom_mirror.py": prov["codigo_embutido_de"][0]["sha256"], "acom_crypto.py": prov["codigo_embutido_de"][1]["sha256"], "Acom_v17_mirror_crypto.py": prov["origem_funcional_do_operador"]["sha256"],
                "run_tests.py": prov["testes_do_operador"]["sha256"], "tgl_core.py": prov["tgl_core"]["sha256"], "ACOM_Mirror_Crypto_PI_INPI.tex": prov["patentes"][1]["sha256"]}
    for nome, h in esperado.items():
        d = sha(rb(os.path.join(FO, nome))); m = man["fontes"][{"acom_mirror.py": "mirror", "acom_crypto.py": "crypto", "Acom_v17_mirror_crypto.py": "v17_torch", "run_tests.py": "run_tests", "tgl_core.py": "tgl_core", "ACOM_Mirror_Crypto_PI_INPI.tex": "patente_tex"}[nome]]["sha256"]
        pins[nome] = {"proveniencia": h[:16], "disco": d[:16], "manifesto": m[:16], "ok": h == d == m}
        ok2 = ok2 and h == d == m
    R["C2_pinos_das_seis_fontes_do_operador"] = {"ok": ok2, "detalhe": pins}
    ruins = literais_de_beta(secao_texto)
    R["C9_nenhum_literal_de_beta_no_codigo"] = {"ok": not ruins, "detalhe": ruins[:5]}
    if nomes_base is None and um_base_texto is not None:
        nomes_base = nomes_de_nivel_de_modulo(um_base_texto)
    if nomes_base is not None:
        mine = nomes_de_nivel_de_modulo(secao_texto)
        col = sorted(mine & nomes_base)
        permitido = {"hashlib", "math", "time", "json", "os", "re", "sys", "np", "ALPHA_FINE_CODATA_2018"}
        # `json`/`os`/`np` etc. so' colidem se a secao os importar (mesmo modulo); o estudo achou so' hashlib, math, time e ALPHA_FINE_CODATA_2018
        R["C3_colisao_de_nomes"] = {"ok": set(col) <= permitido, "detalhe": {"colidem": col, "n_nomes_da_secao": len(mine)}}
    return R

# -*- coding: utf-8 -*-
"""_bump_copia_v406.py -- COPIA + SUBIDA DE ROTULO (nao e' o motor de regras) dos scripts da cadeia v405 para PK6 = cadeia_de_selo\\v406.
Receita: copiar o molde de cadeia_de_selo\\v405 (SO' LEITURA) e subir SO' os rotulos de versao: 404 -> 405 e 405 -> 406 (uma passada, simultanea; 399 a 403 NAO sobem), k405c -> k406c, h405 -> h406, base_v404 -> base_v405,
B14 -> B15 e B13 -> B14 (so' como palavra solta), B13-v404-20261028-R1 -> B14-v405-20261102-R1 (o deployment da v405 foi LIDO de v405\\bancada_B3_servico\\RECIBO_RELIGAMENTO_v405.json). Os nomes nascidos no um.py v405
(identificadores com 404/405 que existem no texto da base) NAO sobem: usa-se a funcao bump() do derivar_v406_motor.py (so' o mapa; NENHUMA regra de contagem exata, NENHUM texto reescrito), a mesma que gerou os 24 derivados.
NAO muda logica, narrativa nem lista de pedras. Para cada arquivo: bump/<nome>.diff (unified), verificacao INDEPENDENTE de que toda linha alterada difere do molde so' em rotulos (normalizacao dos dois lados), ast.parse / sh -n,
e um comentario de UMA linha no topo [A ADAPTAR v406] quando o corpo ainda e' o da v405 (pedras, STONES, ESPERADOS, delta, constantes). NUNCA executa os scripts copiados. Nao sobrescreve nada existente sem backup de bytes (.bak_<ts>).
Uso: python -B -X utf8 _bump_copia_v406.py [--seco]   (--seco: so' mede e compara; nao grava nada)"""
import ast, datetime, difflib, hashlib, importlib.util, json, os, re, shutil, subprocess, sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))        # PK6
CH = os.path.dirname(HERE)
V5 = os.path.join(CH, "v405")
BUMPDIR = os.path.join(HERE, "bump")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha = lambda b: hashlib.sha256(b).hexdigest()
sha16 = lambda b: sha(b)[:16]

_spec = importlib.util.spec_from_file_location("derivar_v406_motor", os.path.join(HERE, "derivar_v406_motor.py"))
MOTOR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MOTOR)           # so' definicoes (sem efeito colateral)

# ---- os moldes: (caminho relativo em v405, extra?) -------------------------------------------------------------------------------------------------------------------------------------------------
PRINCIPAIS = [
    "conferir_rito_v405.py", "teste_conferidor_positivo_v405.py", "gerar_esperados_v405.py", "diff_e_pinos_v405.py", "conferir_citacoes_v405.py", "p00_precondicoes_v405.py",
    "regerar_v405.sh", "comparar_v404_v405.py", "pos_build_kernel_v405.py", "ensaio_a_seco_v405.py", "simular_arvore_do_nos_v405.py", "exame_pontos_v405.py",
    "guardas_estaticas_bancada_v405.py", "instalar_v405.py", "reverter_v405.py", "rito_v405.sh", "conferir_instalar_rito_v405.py", "guarda_ordem_de_chamada_v405.py",
    "fim_de_cadeia_v405.sh", "gerar_relatorio_v405.py", "fechar_preparacao_v405.py", "regras_v405.py",
    "bancada_B3_servico/conferir_exigencias_servico_v405.py", "bancada_B3_servico/evento_c1_b3_v405.py", "bancada_B3_servico/recibo_parada_v405.py",
    "bancada_B3_servico/recibo_religamento_v405.py", "bancada_B3_servico/controle_negativo/mutar_conferidor_v405.py",
    "pos_rito/b3_recibo_v405.py", "orquestrador/pos_treino_v405.py",
]
EXTRAS = []                                                    # preenchido abaixo (so' o que existe em v405 e e' referenciado por um script v406)
# os 24 derivados pelo motor (existem em PK6): NAO sao tocados; so' comparados com a copia em memoria
DERIVADOS_PELO_MOTOR = [
    "purga_v405.py", "guarda_p18_v405.py", "acom_conferencias_v405.py", "runtime_quadro_v397.py", "quadro_v397.py", "refazer_candidato_v405.sh", "refazer_sandbox_v405_pos_selo.sh",
    "refazer_arvore_v405_pos_selo.py", "pino_memoria_py_v405.py", "copiar_base_v405.py", "preparar_kernel_v405.py", "bateria_pre_selo/rodar_bn_pre_selo_v405.sh",
    "pos_rito/superficies_v405.py", "pos_rito/fila_memoria_v405.py", "pos_rito/montar_textos_v405.py", "pos_rito/fechar_v405.py", "pos_rito/registrar_mapa_v405.py",
    "pos_rito/leitura_v405.py", "pos_rito/harness_textos_ensaio_v405.py", "pos_rito/harness_fechar_sandbox_v405.py", "pos_rito/gerar_x_custodia_v405.py",
    "pos_rito/chain_pos_rito_v405.sh", "pos_rito/gerar_derivacao_pos_rito_v405.py", "pos_rito/textos_v405.py",
]
EXTRAS_CANDIDATOS = ["gerar_candidato_v405.py", "gerar_pino_das_pedras_v405.py", "copiar_pedras_v405.py", "copiar_insumos_v405.py", "copiar_logs_do_kernel_v405.py", "guarda_frases_v405.py",
                     "bateria_pre_selo/derivar_pre_selo_v405.py", "bateria_pre_selo/conferir_recibo_pre_selo_v405.py", "bateria_pre_selo/gerar_pino_recibo_pre_selo_v405.py",
                     "bateria_pre_selo/limpar_sandbox_vb21.py", "bateria_pre_selo/snap_producao_v405.py", "bateria_pre_selo/rodar_ensaio_1_pre_selo_v405.sh"]

RX_N = re.compile(r"(?<![0-9])(404|405)(?![0-9])")
MAPA_N = {"404": "405", "405": "406"}
RX_B = re.compile(r"(?<![0-9A-Za-z_])B(13|14)(?![0-9A-Za-z_])")
DEP_VELHO, DEP_NOVO = "B13-v404-20261028-R1", "B14-v405-20261102-R1"
RX_TOKEN_QUALQUER = re.compile(r"(?<![0-9])(404|405)(?![0-9])|(?<![0-9A-Za-z_])B1[34](?![0-9A-Za-z_])")
RX_WORD = re.compile(r"[A-Za-z0-9_]+")


def nome_destino(rel):
    return RX_N.sub(lambda m: MAPA_N[m.group(1)], rel)


def norm(s):
    s = re.sub(r"(?<![0-9])(?:404|405|406)(?![0-9])", "@N", s)
    s = re.sub(r"(?<![0-9A-Za-z_])B1[345](?![0-9A-Za-z_])", "@B", s)
    return re.sub(r"-2026(?:1028|1102)-R1", "-@D-R1", s)


def _modulos_da_cadeia():
    """basenames (sem .py) dos scripts da cadeia v405 (raiz, pos_rito, orquestrador, bateria_pre_selo, bancada_B3_servico): sao os MODULOS que um `import X` pode citar"""
    out = set()
    for sub in ("", "pos_rito", "orquestrador", "bateria_pre_selo", "bancada_B3_servico"):
        d = os.path.join(V5, sub)
        if os.path.isdir(d):
            out |= {f[:-3] for f in os.listdir(d) if f.endswith(".py")}
    return out


_MODS = None
GRAVADOS = set()
RX_IMPORT = re.compile(r"^[ \t]*(?:import[ \t]+(?P<imp>[^#\n]+)|from[ \t]+(?P<frm>[A-Za-z0-9_]+)[ \t]+import(?![A-Za-z0-9_]))", re.M)


def consertar_imports(t, novo):
    """O motor PRESERVA palavras com 404/405 que existem no um.py. Quando uma dessas palavras e' o NOME DE UM MODULO DA CADEIA num `import X`/`from X import` (ex.: `import runtime_v405 as RT`, `import leitura_v405 as L`), a copia
    importaria o modulo velho: aqui o nome sobe (so' se v405/<X>.py existe). Devolve (novo, n_consertados)."""
    global _MODS
    if _MODS is None:
        _MODS = _modulos_da_cadeia()
    lo, ln = t.split(chr(10)), novo.split(chr(10))
    n = 0
    for m in RX_IMPORT.finditer(t):
        i = t.count(chr(10), 0, m.start())
        mods = [m.group("frm")] if m.group("frm") else [x.strip().split()[0] for x in m.group("imp").split(",") if x.strip()]
        for md in mods:
            if RX_N.search(md) and md in _MODS and md in ln[i]:
                novo_md = RX_N.sub(lambda mm: MAPA_N[mm.group(1)], md)
                ln[i] = re.sub(r"(?<![A-Za-z0-9_])" + re.escape(md) + r"(?![A-Za-z0-9_])", novo_md, ln[i], count=1)
                n += 1
    return chr(10).join(ln), n


def subir(t):
    """texto do molde -> texto subido. Devolve (novo, contagens)."""
    c = {}
    novo = MOTOR.bump(t, (), "v405")
    novo, c["imports_de_modulo_da_cadeia_consertados"] = consertar_imports(t, novo)
    c["deployment_antes_do_B"] = t.count(DEP_VELHO)
    novo = RX_B.sub(lambda m: "B" + str(int(m.group(1)) + 1), novo)                       # B13 -> B14, B14 -> B15 (simultaneo, so' palavra solta)
    dep_pos_B = DEP_VELHO.replace("B13", "B14").replace("v404", "v405")
    c["deployment_trocado"] = novo.count(dep_pos_B)
    assert c["deployment_trocado"] == c["deployment_antes_do_B"], ("deployment nao casou", c)
    novo = novo.replace(dep_pos_B, DEP_NOVO)
    return novo, c


# ---- A ADAPTAR: classes de conteudo que ainda e' o da v405 ------------------------------------------------------------------------------------------------------------------------------------------
PEDRAS8 = ["PonteDaMassa", "MassaTensaoPura", "Identidade", "ObservadorTerminal", "LeiDoDiminuto", "TonicaDoHamiltoniano", "DiscoDeEuler", "PontoZeroDoPsion"]
CLASSES = {
    "pedras_stones": re.compile(r"\bSTONES\b|\bREGISTRO_DE_PEDRA\b|pedras_sha16_da_ordem|PINO_DAS_PEDRAS|PEDRAS_COPIA|copiar_pedras|gerar_pino_das_pedras|\bpedra_|_pedras\b|suporte_das_pedras|PEDRAS?(?![a-z])|FUNCOES_(?:PEDRAS|V40\d)|(?:ponte_da_massa|massa_tensao_pura|observador_terminal|lei_do_diminuto|tonica_do_hamiltoniano|disco_de_euler|ponto_zero_do_psion)_v40\d"),
    "pedras_mencao_em_texto": re.compile(r"\bpedras?\b", re.I),
    "oito_pedras_8_modulos": re.compile(r"\bOITO\b|\boito\b|\b8 (?:pedras|novas|novos|modulos|módulos)\b|\(8\)|as 8\b|%s" % "|".join(PEDRAS8)),
    "esperados": re.compile(r"ESPERADOS|\bESP\["),
    "kernel_modulos_novos": re.compile(r"kernel_modulos_novos|\bmodulos novos\b|\bmodulos_novos\b"),
    "chaves_witness_False_True": re.compile(r"whole_certificate_inhabited|inhabitant_exhibited|canonicalFullTGLWitness|full_static_witness_exists|independent_v3_|null_tests_passed_blind"),
    "delta_v406": re.compile(r"\bdelta_v40\d|import delta\b|\bDL\.\w+|\bD[345]\.\w+"),
    "bandeiras_ext_8_prefixos": re.compile(r"ext_(?:pdm|mtp|idt|obt|ldd|tdh|dde|pzp)40\d"),
    "autorizacao_e_ordem_do_operador_da_v405": re.compile(r"AUTORIZACAO_OPERADOR|2c3da184ebefc7c4|Ordem do operador de 0?1/11|ordem do operador de 0?1/11"),
    "treino_da_nativa_v4": re.compile(r"STATE_v4|treino v4|treino da nativa"),
    "pinos_intermediarios_da_v405": re.compile(r"a30f9f0ebf90c277|eaefcd095abbaee7|6cd0ea631f81c522|dc3da414064bb892|1d5786c38c954e19"),
    "constantes_numericas_v405": re.compile(r"(?<![0-9.,])(?:10066|9698|1445|24971|6901|764951|764\.951)(?![0-9])|\b368\b"),
}
# classes que justificam o comentario de topo: o corpo depende do conteudo da v405 (pedras/STONES/ESPERADOS/delta/chaves/constantes)
CLASSES_CABECALHO = ("autorizacao_e_ordem_do_operador_da_v405", "treino_da_nativa_v4", "pinos_intermediarios_da_v405", "pedras_stones", "oito_pedras_8_modulos", "esperados", "kernel_modulos_novos", "chaves_witness_False_True", "delta_v406", "bandeiras_ext_8_prefixos", "constantes_numericas_v405")


_SUBS = ("pos_rito", "orquestrador", "bateria_pre_selo", "bancada_B3_servico", "bancada_B3", "vinculo", "kernel", "bateria_pos_selo", "pedra", "insumos", "revisao_terceiro")
RX_EXT = re.compile(r"\.(?:py|sh|json|md|txt|pysnip|semente|lean|log|diff)(?![A-Za-z0-9_])")


def _basenames(pasta):
    out = set()
    for sub in ("",) + _SUBS:
        d = os.path.join(pasta, sub) if sub else pasta
        if os.path.isdir(d):
            for f in os.listdir(d):
                if os.path.isfile(os.path.join(d, f)):
                    out.add(f)
            if sub == "bancada_B3_servico" and os.path.isdir(os.path.join(d, "controle_negativo")):
                out |= set(os.listdir(os.path.join(d, "controle_negativo")))
    return out


_BN = {}


def referencias_a_arquivos(t, novo, gravados):
    """nomes de arquivo (com 404/405 no nome) citados no texto; classifica o nome NOVO: existe (PK6, v405 ou sera gravado agora) / a_gerar_na_v406 (o analogo v405 existe) / so_na_cadeia_anterior (provavel fantasma) / desconhecido"""
    if not _BN:
        _BN["pk6"] = _basenames(HERE); _BN["v5"] = _basenames(V5); _BN["v4"] = _basenames(os.path.join(CH, "v404"))
    wo, wn = list(RX_WORD.finditer(t)), list(RX_WORD.finditer(novo))
    assert len(wo) == len(wn)
    cl = {"existe_ou_sera_gravado": set(), "a_gerar_na_v406": set(), "so_na_cadeia_anterior_provavel_fantasma": set(), "desconhecido": set()}
    for a, b in zip(wo, wn):
        if not RX_N.search(a.group(0)):
            continue
        me = RX_EXT.match(t, a.end())
        if not me:
            continue
        old, new = a.group(0) + me.group(0), b.group(0) + me.group(0)
        if new in _BN["pk6"] or new in gravados or new in _BN["v5"]:
            cl["existe_ou_sera_gravado"].add(new)
        elif old in _BN["v5"]:
            cl["a_gerar_na_v406"].add(new)
        elif old in _BN["v4"] or new in _BN["v4"]:
            cl["so_na_cadeia_anterior_provavel_fantasma"].add(new + "   (molde citava " + old + ")")
        else:
            cl["desconhecido"].add(new)
    return {k: sorted(v) for k, v in cl.items() if v}


def achar_a_adaptar(texto):
    out = {}
    linhas = texto.split("\n")
    for k, rx in CLASSES.items():
        hits = [i + 1 for i, l in enumerate(linhas) if rx.search(l)]
        if hits:
            out[k] = {"n_linhas": len(hits), "primeiras": hits[:25]}
    return out


def cabecalho(dest_rel, molde_rel, classes, eh_sh):
    ks = ",".join(k for k in classes if k in CLASSES_CABECALHO)
    return ("# [A ADAPTAR v406] SUBIDA MECANICA DE ROTULO (v405->v406, v404->v405) do molde v405/%s; o CORPO e' o da v405 (%s); nada rodou; ver BUMP_v406_NOTAS.md e bump/%s.diff" % (molde_rel, ks, dest_rel.replace("/", "__")))


def insere_cabecalho(texto, linha):
    """devolve (texto, n_linhas_antes_do_cabecalho): o cabecalho entra depois do shebang e da linha de coding, se houver"""
    ls = texto.split(chr(10))
    i = 0
    if ls and ls[0].startswith("#!"):
        i = 1
    if i < len(ls) and re.match(r"#.*coding[:=]\s*[-\w.]+", ls[i]) and i < 2:
        i += 1
    ls.insert(i, linha)
    return chr(10).join(ls), i


def sintaxe(path, texto, eh_sh):
    if eh_sh:
        sh = shutil.which("sh") or r"C:\Program Files\Git\bin\sh.exe"
        r = subprocess.run([sh, "-n", path], capture_output=True, text=True, encoding="utf-8", errors="replace")
        return r.returncode == 0, (r.stderr or "").strip()[:300]
    try:
        ast.parse(texto)
        return True, ""
    except SyntaxError as e:
        return False, "SyntaxError %s l.%s" % (e.msg, e.lineno)


NAO_COPIADOS_POR_DECISAO = {
    "bancada_B3_servico/derivar_servico_v405.py": "e' um GERADOR com o mapa 403->404 embutido (M = {'404': '405', '403': '404'}, RE_V13/RE_V14): a subida de rotulo o quebraria ({'405': '406', '403': '405'}); o seu papel (produzir os 5 scripts do servico) foi cumprido pela copia direta",
    "delta_v405.py": "autoral (STONES, ERRATAS, N_CHECKS...): a gerencia escreve o delta_v406 completo; PK6 tem so' o esqueleto do executor",
    "runtime_v405.py / registros_v405.py / v405_pins.py / um_v405_candidato.py": "autorais ou embutidos no um.py (conteudo da v405): a gerencia escreve os da v406",
    "aplicar_R2..R7_v405.py / aplicar_errata_pedras_v405.py": "historico das erratas da preparacao da v405 (editam artefatos da v405)",
    "pos_rito/adaptar_pos_rito_v405.py / adaptar_regras2_v405.py / adaptar_regras3_v405.py": "historico: adaptaram o pos_rito da v404 para a v405",
    "*.pysnip / pos_rito/textos_v405.py": "textos autorais (pos_rito/textos_v406.semente ja existe, derivada pelo motor)",
    "construir_kernel_v405.sh / copiar_k405c.sh / copiar_base_v405.py / preparar_kernel_v405.py": "ja existem em v406 (escritos ou derivados pelo executor anterior)",
    "arquivos de saida da v405 (*.json de resultado, *_out.txt, logs, bancada_B3/*, pos_rito/conferidor/*, sim_*, imp_*...)": "nao sao scripts",
}


def achados_nos_derivados():
    """leitura dos derivados do motor (NAO os altera): import de modulo da cadeia nao subido; B(n) nao subido"""
    out = {"import_de_modulo_da_cadeia_nao_subido": [], "B_n_nao_subido": []}
    for rel in DERIVADOS_PELO_MOTOR:
        d = nome_destino(rel)
        if rel == "pos_rito/textos_v405.py":
            d = "pos_rito/textos_v406.semente"
        p_ = os.path.join(HERE, *d.split("/"))
        if not os.path.exists(p_):
            continue
        t_ = open(p_, "rb").read().decode("utf-8")
        for i, l in enumerate(t_.split(chr(10))):
            for m in RX_IMPORT.finditer(l):
                mods = [m.group("frm")] if m.group("frm") else [x.strip().split()[0] for x in m.group("imp").split(",") if x.strip()]
                for md in mods:
                    if RX_N.search(md) and md.endswith("_v405") and os.path.exists(os.path.join(os.path.dirname(p_), nome_destino(md) + ".py")) and not os.path.exists(os.path.join(os.path.dirname(p_), md + ".py")):
                        out["import_de_modulo_da_cadeia_nao_subido"].append({"arquivo": d, "linha": i + 1, "texto": l.strip()[:100], "deveria_ser": nome_destino(md)})
            for m in re.finditer(r"(?<![0-9A-Za-z_])(B1[0-9](?:-v40[0-9]-[0-9]{8}-R[0-9])?)(?![0-9A-Za-z_])", l):
                out["B_n_nao_subido"].append({"arquivo": d, "linha": i + 1, "token": m.group(1), "trecho": l.strip()[max(0, m.start() - 40):m.end() + 40]})
    return out


def api_do_delta(arquivos):
    rx = re.compile(r"(?<![A-Za-z0-9_.])DL_?\.([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)?)")
    uso = {}
    for ent in arquivos:
        t_ = open(os.path.join(HERE, *ent["destino"][5:].split("/")), "rb").read().decode("utf-8")
        for m in rx.finditer(t_):
            uso.setdefault(m.group(1), set()).add(os.path.basename(ent["destino"]))
    d = open(os.path.join(HERE, "delta_v406.py"), "rb").read().decode("utf-8")
    definidos = set(re.findall(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=", d, re.M))
    return {"definidos_no_esqueleto_delta_v406": sorted(definidos), "referenciados_total": len(uso), "referenciados_e_nao_definidos": {k: sorted(v) for k, v in sorted(uso.items()) if k.split(".")[0] not in definidos},
            "alias_do_predecessor_D1_a_D4": "as copias usam DL.D4 (=delta_v404 no delta_v405) 23x, DL.D3 22x, DL.D2 10x, DL.D1 3x: na v406 o predecessor e' o delta_v405 (por convencao D5); decisao da gerencia: expor D5 e renomear, ou redefinir D1..D4"}


def main():
    os.makedirs(BUMPDIR, exist_ok=True) if not SECO else None
    resultado = {"contrato": "BUMP_v406_RESULTADO", "gerado_em": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pk6": HERE, "molde_somente_leitura": V5,
                 "estatuto": "[REAL] medido ao rodar _bump_copia_v406.py; subida mecanica de rotulo, NADA executado; o corpo e' o da v405",
                 "regra_de_subida": {"404->405 e 405->406": "uma passada, simultanea, via MOTOR.bump(origem=v405) (preserva identificadores nascidos no um.py v405 e hex longo)", "B13->B14, B14->B15": "so' palavra solta", "deployment": "%s -> %s [REAL: lido de v405/bancada_B3_servico/RECIBO_RELIGAMENTO_v405.json identidade.deployment_id = B14-v405-20261102-R1]" % (DEP_VELHO, DEP_NOVO), "nao_sobem": "399 a 403, V14 (variavel do conferidor de servico), REPINADA_B13__ (palavra com sublinhado), pinos hex"},
                 "observacao_das_rodadas": "a 1a rodada gravou os 41 destinos (estado 'gravado'); as seguintes (ajuste de numeracao de linhas, secoes de achados) encontraram os bytes IGUAIS (estado 'igual_ja_existia') e so' regeneraram bump/*.diff e este JSON (com .bak de bytes do JSON anterior)", "arquivos": [], "derivados_pelo_motor_comparados": [], "nao_copiados": [], "palavras_alteradas": {}}
    palavras_global = {}
    todos = [(r, False) for r in PRINCIPAIS] + [(r, True) for r in EXTRAS_CANDIDATOS]
    global GRAVADOS
    GRAVADOS = {os.path.basename(nome_destino(r)) for r, _e in todos}
    for rel, extra in todos:
        molde = os.path.join(V5, *rel.split("/"))
        if not os.path.exists(molde):
            resultado["nao_copiados"].append({"molde": rel, "motivo": "NAO EXISTE em v405"})
            continue
        raw = open(molde, "rb").read()
        t = raw.decode("utf-8")
        assert "\r\n" not in t and not t.startswith("\ufeff"), ("fim de linha/BOM inesperado", rel)
        novo, cont = subir(t)
        # --- verificacao independente: mesma contagem de linhas; toda linha alterada so' difere em rotulos
        lo, ln = t.split("\n"), novo.split("\n")
        assert len(lo) == len(ln), ("numero de linhas mudou", rel)
        alteradas, revertidas = 0, []
        for i, (a, b) in enumerate(zip(lo, ln)):
            if a != b:
                if not RX_TOKEN_QUALQUER.search(a) or norm(a) != norm(b):
                    revertidas.append((i + 1, a[:120], b[:120]))
                else:
                    alteradas += 1
        assert not revertidas, ("linha alterada por outra razao", rel, revertidas[:3])
        # --- palavras alteradas / preservadas (alinhadas por indice; o mapa e' 1:1 por palavra)
        wo, wn = RX_WORD.findall(t), RX_WORD.findall(novo)
        assert len(wo) == len(wn), ("palavras desalinhadas", rel)
        tok_mudados = {"404->405": 0, "405->406": 0}
        preserv = {}
        for a, b in zip(wo, wn):
            if RX_N.search(a):
                if a != b:
                    palavras_global.setdefault(a + " -> " + b, 0); palavras_global[a + " -> " + b] += 1
                    for m in RX_N.finditer(a):
                        tok_mudados[m.group(1) + "->" + MAPA_N[m.group(1)]] += 1
                else:
                    preserv[a] = preserv.get(a, 0) + 1
        n_b = len(RX_B.findall(t))
        dest_rel = nome_destino(rel)
        a_adaptar = achar_a_adaptar(novo)
        refs = referencias_a_arquivos(t, novo, GRAVADOS)
        eh_sh = rel.endswith(".sh")
        com_cab = any(k in CLASSES_CABECALHO for k in a_adaptar)
        if com_cab:
            final, ins = insere_cabecalho(novo, cabecalho(dest_rel, rel, a_adaptar, eh_sh))
            for _k, _v in a_adaptar.items():         # os numeros de linha passam a ser os do ARQUIVO GRAVADO (depois do cabecalho)
                _v["primeiras"] = [ln + 1 if ln > ins else ln for ln in _v["primeiras"]]
        else:
            final = novo
        destino = os.path.join(HERE, *dest_rel.split("/"))
        ent = {"molde": "v405/" + rel, "destino": "v406/" + dest_rel, "extra_nao_pedido_na_lista_minima": extra, "sha16_molde": sha16(raw), "linhas_do_molde": len(lo),
               "linhas_alteradas": alteradas, "linhas_adicionadas_cabecalho": 1 if com_cab else 0, "tokens_vistos": {"rotulos_404_405_mudados": tok_mudados, "palavras_solta_B13_B14": n_b,
               "deployment_B13_v404_20261028_R1": cont["deployment_antes_do_B"], "palavras_com_404_405_preservadas": sum(preserv.values()), "palavras_distintas_preservadas": len(preserv)},
               "palavras_com_404_405_preservadas_lista": dict(sorted(preserv.items(), key=lambda kv: (-kv[1], kv[0]))), "a_adaptar": a_adaptar, "cabecalho_a_adaptar_inserido": com_cab, "linhas_a_adaptar_referem_se_ao": "arquivo gravado em v406 (ja com o cabecalho)", "referencias_a_arquivos": refs}
        enc = final.encode("utf-8")
        ent["sha16_destino"] = sha16(enc)
        # --- grava (com backup se existir e diferir)
        estado = None
        if SECO:
            estado = "seco"
        elif os.path.exists(destino):
            atual = open(destino, "rb").read()
            if atual == enc:
                estado = "igual_ja_existia"
            else:
                open(destino + ".bak_" + TS, "wb").write(atual)
                estado = "substituido_com_backup"
        else:
            estado = "gravado"
        if estado in ("gravado", "substituido_com_backup"):
            os.makedirs(os.path.dirname(destino), exist_ok=True)
            open(destino + ".tmp", "wb").write(enc); assert os.path.getsize(destino + ".tmp") == len(enc); os.replace(destino + ".tmp", destino)
        ent["estado_da_gravacao"] = estado
        # --- sintaxe (do arquivo gravado se houver; senao de um temporario)
        if SECO:
            ent["sintaxe_ok"], ent["sintaxe_erro"] = sintaxe(molde, final, eh_sh) if eh_sh else sintaxe(None, final, False)
        else:
            ent["sintaxe_ok"], ent["sintaxe_erro"] = sintaxe(destino, final, eh_sh)
        # --- diff unified (molde -> copia)
        if not SECO:
            dif = "".join(difflib.unified_diff(t.splitlines(True), final.splitlines(True), fromfile="v405/" + rel, tofile="v406/" + dest_rel, n=0))
            dpath = os.path.join(BUMPDIR, dest_rel.replace("/", "__") + ".diff")
            open(dpath, "w", encoding="utf-8", newline="").write(dif)
            ent["diff"] = "bump/" + dest_rel.replace("/", "__") + ".diff"; ent["diff_sha16"] = sha16(dif.encode("utf-8"))
        resultado["arquivos"].append(ent)
        print("%-62s -> %-62s alt=%-4d cab=%d sint=%s %s" % (rel, dest_rel, alteradas, 1 if com_cab else 0, ent["sintaxe_ok"], estado))
    # ---- os 24 derivados pelo motor: comparacao (nada gravado)
    for rel in DERIVADOS_PELO_MOTOR:
        molde = os.path.join(V5, *rel.split("/"))
        dest_rel = nome_destino(rel)
        if rel == "pos_rito/textos_v405.py":
            dest_rel = "pos_rito/textos_v406.semente"
        destino = os.path.join(HERE, *dest_rel.split("/"))
        if not os.path.exists(molde) or not os.path.exists(destino):
            resultado["derivados_pelo_motor_comparados"].append({"molde": rel, "destino": dest_rel, "estado": "molde ou destino ausente"})
            continue
        t = open(molde, "rb").read().decode("utf-8")
        novo, _c = subir(t)
        d = open(destino, "rb").read().decode("utf-8")
        if d == novo:
            resultado["derivados_pelo_motor_comparados"].append({"molde": rel, "destino": dest_rel, "estado": "IGUAL a minha copia (bump puro)", "sha16_destino": sha16(d.encode("utf-8"))})
        else:
            dif = "".join(difflib.unified_diff(novo.splitlines(True), d.splitlines(True), fromfile="minha_copia/" + dest_rel, tofile="derivado_do_motor/" + dest_rel, n=0))
            nome_dif = "bump/" + dest_rel.replace("/", "__") + ".vs_derivado.diff"
            if not SECO:
                open(os.path.join(HERE, *nome_dif.split("/")), "w", encoding="utf-8", newline="").write(dif)
            nmais = sum(1 for l in dif.splitlines() if l.startswith("+") and not l.startswith("+++"))
            nmenos = sum(1 for l in dif.splitlines() if l.startswith("-") and not l.startswith("---"))
            resultado["derivados_pelo_motor_comparados"].append({"molde": rel, "destino": dest_rel, "estado": "DIFERE da minha copia (o derivado do motor tem regra/nota a mais)", "linhas_so_no_derivado": nmais, "linhas_so_na_minha_copia": nmenos,
                                                                 "diff": nome_dif, "sha16_destino": sha16(d.encode("utf-8")), "sha16_minha_copia": sha16(novo.encode("utf-8"))})
    resultado["nao_copiados_por_decisao"] = NAO_COPIADOS_POR_DECISAO
    resultado["achados_nos_derivados_do_motor"] = achados_nos_derivados()
    resultado["delta_v406_api_referenciada_pelas_copias"] = api_do_delta(resultado["arquivos"])
    resultado["palavras_alteradas"] = dict(sorted(palavras_global.items(), key=lambda kv: (-kv[1], kv[0])))
    resultado["resumo"] = {"copiados_pedidos": sum(1 for a in resultado["arquivos"] if not a["extra_nao_pedido_na_lista_minima"]), "copiados_extras": sum(1 for a in resultado["arquivos"] if a["extra_nao_pedido_na_lista_minima"]),
                           "sintaxe_ok": sum(1 for a in resultado["arquivos"] if a["sintaxe_ok"]), "sintaxe_falhou": [a["destino"] for a in resultado["arquivos"] if not a["sintaxe_ok"]],
                           "com_cabecalho_A_ADAPTAR": sum(1 for a in resultado["arquivos"] if a["cabecalho_a_adaptar_inserido"])}
    if not SECO:
        out = os.path.join(HERE, "BUMP_v406_RESULTADO.json")
        if os.path.exists(out):
            open(out + ".bak_" + TS, "wb").write(open(out, "rb").read())
        open(out + ".tmp", "w", encoding="utf-8").write(json.dumps(resultado, ensure_ascii=False, indent=1)); os.replace(out + ".tmp", out)
    print(json.dumps(resultado["resumo"], ensure_ascii=False))
    for d in resultado["derivados_pelo_motor_comparados"]:
        print("  vs derivado:", d["destino"], "->", d["estado"])


if __name__ == "__main__":
    main()

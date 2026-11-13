# -*- coding: utf-8 -*-
"""_bump_copia_v411.py -- COPIA + SUBIDA DE ROTULO (nao e' o motor de regras) dos scripts da cadeia v410 para cadeia_de_selo\\v411 (claude-construtor-v411, a servico da gerencia c1, 12/11/2026).
Receita (molde: _bump_copia_v410.py): copiar o molde de cadeia_de_selo\\v410 (SO' LEITURA; as versoes FINAIS da v410, as que rodaram no rito selado 5d9497a721c3589e) e subir SO' os rotulos de versao: 409 -> 410 e 410 -> 411
(uma passada, simultanea), k410c -> k411c, base_v409 -> base_v410, B18 -> B19 e B19 -> B20 (so' como palavra solta), B18-v409-20261106-R1 -> o deployment que a Bancada de producao pina HOJE (LIDO de
C:\\IALD\\Bancada_Um\\canonical_contracts.json: a v410 aplicada). Os nomes nascidos no um.py v410 (identificadores com 409/410 que existem no texto da base) NAO sobem: usa-se a funcao bump() do derivar_v411_motor.py.
NAO muda logica, narrativa nem listas: cada arquivo ganha um comentario de UMA linha `# [A ADAPTAR v411] ...` (o p00 recusa arquivo com essa marca; ela sai quando o arquivo for adaptado de verdade).
FICAM FORA (autorais da v411, escritos a mao, nao sobem do molde): delta, registros, runtime, guarda_frases, gerar_candidato, copiar_base, copiar_insumos, copiar_k411c, construir_kernel, pos_build_kernel, os artigos,
o preparo do bundle (a v411 nao tem bundle), os registros/runtimes da IALD2, AEscala, H0DN v410 e HMS/13 e os _adapt/_fix/_r* (historico). Para cada arquivo: bump/<nome>.diff, verificacao INDEPENDENTE de que toda linha
alterada difere do molde so' em rotulos, ast.parse / sh -n. NUNCA executa os scripts copiados. Nao sobrescreve nada existente sem backup de bytes (.bak_<ts>).
Uso: python -B -X utf8 _bump_copia_v411.py [--seco] [--so ARQ ...]"""
import ast, datetime, difflib, hashlib, importlib.util, json, os, re, subprocess, sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(HERE)
V10 = os.path.join(CH, "v410")
BUMPDIR = os.path.join(HERE, "bump")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
_spec = importlib.util.spec_from_file_location("derivar_v411_motor", os.path.join(HERE, "derivar_v411_motor.py"))
MOTOR = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(MOTOR)

RAIZ = ["acom_conferencias_v410.py", "acom_inscrever_prep_v410.py", "carimbar_stdout_v410.py", "comparar_v409_v410.py", "conferir_citacoes_v410.py", "conferir_instalar_rito_v410.py", "conferir_rito_v410.py",
        "copiar_logs_do_kernel_v410.py", "diff_e_pinos_v410.py", "ensaio_a_seco_v410.py", "exame_pontos_v410.py", "fechar_preparacao_v410.py", "fim_de_cadeia_v410.sh", "gerar_esperados_v410.py", "gerar_relatorio_v410.py",
        "guarda_ordem_de_chamada_v410.py", "guarda_p18_v410.py", "guardas_estaticas_bancada_v410.py", "instalar_v410.py", "p00_precondicoes_v410.py", "pino_memoria_py_v410.py", "purga_v410.py", "refazer_arvore_v410_pos_selo.py",
        "refazer_candidato_v410.sh", "refazer_sandbox_v410_pos_selo.sh", "regerar_v410.sh", "regras_v410.py", "reverter_v410.py", "rito_v410.sh", "simular_arvore_do_nos_v410.py", "teste_conferidor_positivo_v410.py",
        "varredura_fock_omega_v410.py", "depositar_construtor_v410.py", "kernel/refazer_audit_v410.sh", "cadeia_parte2_v410.sh", "gerar_pronto_para_candidato_v410.py"]
POS_RITO = ["b3_recibo_v410.py", "chain_pos_rito_v410.sh", "fechar_v410.py", "fila_memoria_v410.py", "gerar_derivacao_pos_rito_v410.py", "gerar_x_custodia_v410.py", "harness_fechar_sandbox_v410.py",
            "harness_textos_ensaio_v410.py", "leitura_v410.py", "montar_textos_v410.py", "registrar_mapa_v410.py", "superficies_v410.py", "textos_v410.py", "textos_v410.semente", "textos_v410_novo.pysnip",
            "textos_custodia_handoff_v410.py", "teste_gatilho_custodia_sem_candidato_v410.py", "teste_mapa_sem_candidato_v410.py", "teste_textos_custodia_sem_candidato_v410.py", "teste_x_custodia_sem_candidato_v410.py"]
ORQ = ["pos_treino_v410.py"]
PRE_SELO = ["conferir_recibo_pre_selo_v410.py", "derivar_pre_selo_v410.py", "gerar_pino_recibo_pre_selo_v410.py", "limpar_sandbox_vb21.py", "rodar_bn_pre_selo_v410.sh", "rodar_ensaio_1_pre_selo_v410.sh", "snap_producao_v410.py"]
SERVICO = ["conferir_exigencias_servico_v410.py", "evento_c1_b3_v410.py", "recibo_parada_v410.py", "recibo_religamento_v410.py", "controle_negativo/mutar_conferidor_v410.py"]
MOLDES = list(RAIZ) + ["pos_rito/" + x for x in POS_RITO] + ["orquestrador/" + x for x in ORQ] + ["bateria_pre_selo/" + x for x in PRE_SELO] + ["bancada_B3_servico/" + x for x in SERVICO]
COPIA_LITERAL = ["quadro_v397.py", "runtime_quadro_v397.py"]       # v397: nao sobem (o quadro do Teste da Unica Palavra segue intocado)
RENOMEIA = {"limpar_sandbox_vb21.py": "limpar_sandbox_vb22.py"}
RX_N = re.compile(r"(?<![0-9])(409|410)(?![0-9])")
MAPA_N = {"409": "410", "410": "411"}
RX_B = re.compile(r"(?<![0-9A-Za-z_])B(18|19)(?![0-9A-Za-z_])")
_BANC = json.load(open(r"C:\IALD\Bancada_Um\canonical_contracts.json", encoding="utf-8"))
DEP_NOVO = str(_BANC["deployment_id"]); assert re.match(r"B19-v410-\d{8}-R1$", DEP_NOVO), DEP_NOVO
DEP_VELHO_RX = re.compile(r"B18-v409-\d{8}-R1")


def nome_destino(rel):
    d = RX_N.sub(lambda m: MAPA_N[m.group(1)], rel)
    base = d.split("/")[-1]
    if base in RENOMEIA:
        d = "/".join(d.split("/")[:-1] + [RENOMEIA[base]])
    return d


def norm(s):
    s = re.sub(r"B(?:18|19|20)-v(?:409|410|411)-\d{8}-R1", "@DEP", s)
    s = re.sub(r"(?<![0-9])(?:409|410|411)(?![0-9])", "@N", s)
    s = re.sub(r"(?<![0-9A-Za-z_])B(?:18|19|20)(?![0-9A-Za-z_])", "@B", s)
    return re.sub(r"vb2[12]", "vb@", s)


def _modulos_da_cadeia():
    out = set()
    for sub in ("", "pos_rito", "orquestrador", "bateria_pre_selo", "bancada_B3_servico"):
        d = os.path.join(V10, sub)
        if os.path.isdir(d):
            out |= {f[:-3] for f in os.listdir(d) if f.endswith(".py")}
    return out


_MODS = _modulos_da_cadeia()
RX_IMPORT = re.compile(r"^[ \t]*(?:import[ \t]+(?P<imp>[^#\n]+)|from[ \t]+(?P<frm>[A-Za-z0-9_]+)[ \t]+import(?![A-Za-z0-9_]))", re.M)


def consertar_imports(t, novo):
    ln = novo.split("\n")
    n = 0
    for m in RX_IMPORT.finditer(t):
        i = t.count("\n", 0, m.start())
        mods = [m.group("frm")] if m.group("frm") else [x.strip().split()[0] for x in m.group("imp").split(",") if x.strip()]
        for md in mods:
            if RX_N.search(md) and md in _MODS and md in ln[i]:
                novo_md = RX_N.sub(lambda mm: MAPA_N[mm.group(1)], md)
                ln[i] = re.sub(r"(?<![A-Za-z0-9_])" + re.escape(md) + r"(?![A-Za-z0-9_])", novo_md, ln[i], count=1); n += 1
    return "\n".join(ln), n


def subir(t):
    c = {}
    novo = MOTOR.bump(t, (), "v410")
    novo, c["imports_consertados"] = consertar_imports(t, novo)
    c["deployment_antes"] = len(DEP_VELHO_RX.findall(t))
    novo = RX_B.sub(lambda m: "B" + str(int(m.group(1)) + 1), novo)
    novo, c["deployment_trocado"] = re.subn(r"B19-v410-\d{8}-R1", DEP_NOVO, novo)
    novo = novo.replace("vb21", "vb22")
    # as MARCAS HISTORICAS de cabecalho ("# [ADAPTADO v410, ...]", "# [AUTORAL v410, ...]") sao registro de quem adaptou e quando: NAO sobem (subir o rotulo delas diria que a v411 as escreveu em 06/11)
    lo_, ln_ = t.split("\n"), novo.split("\n")
    c["marcas_historicas_preservadas"] = 0
    for i_, l_ in enumerate(lo_):
        if re.match(r"^#\s*\[(?:ADAPTADO|AUTORAL|ADAPTADA)\s+v4\d\d\b", l_) and ln_[i_] != l_:
            ln_[i_] = l_; c["marcas_historicas_preservadas"] += 1
    return "\n".join(ln_), c


def cabecalho(dest_rel, molde_rel):
    return "# [A ADAPTAR v411] SUBIDA MECANICA DE ROTULO (v410->v411) do molde v410/%s; o CORPO e' o da v410 (bundle IALD2+AEscala, quatro registros com funcao da v410); nada rodou; ver bump/%s.diff" % (molde_rel, dest_rel.replace("/", "__"))


def insere_cabecalho(texto, linha):
    ls = texto.split("\n"); i = 0
    if ls and ls[0].startswith("#!"):
        i = 1
    if i < len(ls) and re.match(r"#.*coding[:=]", ls[i]):
        i += 1
    ends_cr = "\r" if (len(ls) > i and ls[i].endswith("\r")) or (len(ls) > 0 and ls[0].endswith("\r")) else ""
    ls.insert(i, linha + ends_cr)
    return "\n".join(ls), i


def grava(dst, novo_b):
    if os.path.exists(dst):
        atual = open(dst, "rb").read()
        if atual == novo_b:
            return "igual"
        open(dst + ".bak_" + TS, "wb").write(atual); estado = "regravado_com_backup"
    else:
        estado = "gravado"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst + ".tmp", "wb").write(novo_b); assert os.path.getsize(dst + ".tmp") == len(novo_b); os.replace(dst + ".tmp", dst)
    return estado


def main():
    so = sys.argv[sys.argv.index("--so") + 1:] if "--so" in sys.argv else None
    res = {}
    os.makedirs(BUMPDIR, exist_ok=True)
    for rel in MOLDES + COPIA_LITERAL:
        if so and rel not in so and os.path.basename(rel) not in so:
            continue
        ps = os.path.join(V10, *rel.split("/"))
        if not os.path.exists(ps):
            res[rel] = {"erro": "molde ausente em v410"}; continue
        raw = open(ps, "rb").read(); t = raw.decode("utf-8")
        if rel in COPIA_LITERAL:
            dest_rel, novo, c = rel, t, {}
        else:
            dest_rel = nome_destino(rel)
            novo, c = subir(t)
            lo, ln = t.split("\n"), novo.split("\n")
            assert len(lo) == len(ln), ("numero de linhas mudou", rel)
            ruins = [i + 1 for i, (a, b) in enumerate(zip(lo, ln)) if a != b and norm(a) != norm(b)]
            assert not ruins, ("linha alterada alem de rotulos", rel, ruins[:5], [(lo[i - 1][:120], ln[i - 1][:120]) for i in ruins[:2]])
            if dest_rel.endswith((".py", ".sh", ".pysnip", ".semente")):
                novo, _ = insere_cabecalho(novo, cabecalho(dest_rel, rel))
            if dest_rel.endswith(".py"):
                ast.parse(novo)
            elif dest_rel.endswith(".sh"):
                r = subprocess.run(["sh", "-n"], input=novo.encode("utf-8"), capture_output=True)
                assert r.returncode == 0, (dest_rel, r.stderr[:200])
        pd = os.path.join(HERE, *dest_rel.split("/"))
        novo_b = novo.encode("utf-8")
        estado = "seco" if SECO else grava(pd, novo_b)
        d = "".join(difflib.unified_diff(t.splitlines(True), novo.splitlines(True), fromfile="v410/" + rel, tofile="v411/" + dest_rel, n=0))
        if not SECO and dest_rel != rel:
            open(os.path.join(BUMPDIR, dest_rel.replace("/", "__") + ".diff"), "w", encoding="utf-8", newline="").write(d)
        res[rel] = {"destino": dest_rel, "estado": estado, "molde_sha16": sha16(raw), "destino_sha16": sha16(novo_b), "linhas_alteradas": sum(1 for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")), **c}
    if not SECO and not so:
        p = os.path.join(HERE, "BUMP_v411_RESULTADO.json")
        open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
    print(json.dumps({k: (v.get("estado"), v.get("linhas_alteradas")) for k, v in res.items()}, ensure_ascii=False)[:5000])
    erros = {k: v for k, v in res.items() if "erro" in v}
    print("ERROS:", erros); print("N:", len(res))
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()

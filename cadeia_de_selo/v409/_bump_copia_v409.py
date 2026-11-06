# -*- coding: utf-8 -*-
"""_bump_copia_v409.py -- COPIA + SUBIDA DE ROTULO (nao e' o motor de regras) dos scripts da cadeia v408 para cadeia_de_selo\\v409 (claude-construtor-v409, a servico da gerencia c1, 05/11/2026).
Receita (molde: _bump_copia_v408.py): copiar o molde de cadeia_de_selo\\v408 (SO' LEITURA) e subir SO' os rotulos de versao: 407 -> 408 e 408 -> 409 (uma passada, simultanea; 399 a 406 NAO sobem), k408c -> k409c, h408 -> h409, base_v407 -> base_v408, B16 -> B17 e B17 -> B18 (so' como palavra solta),
B16-v407-20261104-R1 -> o deployment que a Bancada de producao pina HOJE (LIDO de C:\\IALD\\Bancada_Um\\canonical_contracts.json: a v408 aplicada). Os nomes nascidos no um.py v408 (identificadores com 407/408 que existem no texto da base) NAO sobem: usa-se a funcao bump() do derivar_v409_motor.py (so' o mapa;
NENHUMA regra de contagem exata, NENHUM texto reescrito). NAO muda logica, narrativa nem listas de pedras: cada arquivo ganha um comentario de UMA linha `# [A ADAPTAR v409] ...` (o p00 recusa arquivo com essa marca; ela sai quando o arquivo for adaptado de verdade).
Diferenca para a v408: a lista de moldes inclui os AUTORAIS da v408 (delta, artigos, preparar_bundle, construir_kernel, copiar_k408c, carimbar_stdout, acom_inscrever_prep, textos_v408.py, textos_custodia_handoff_v408.py), porque a v408 os escreveu e a v409 parte deles.
Para cada arquivo: bump/<nome>.diff, verificacao INDEPENDENTE de que toda linha alterada difere do molde so' em rotulos, ast.parse / sh -n. NUNCA executa os scripts copiados. Nao sobrescreve nada existente sem backup de bytes (.bak_<ts>).
Uso: python -I -B -X utf8 _bump_copia_v409.py [--seco] [--so ARQ ...]"""
import ast
import datetime
import difflib
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
SECO = "--seco" in sys.argv
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.dirname(HERE)
V8 = os.path.join(CH, "v408")
BUMPDIR = os.path.join(HERE, "bump")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]

_spec = importlib.util.spec_from_file_location("derivar_v409_motor", os.path.join(HERE, "derivar_v409_motor.py"))
MOTOR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MOTOR)

# ---- os moldes: caminho relativo em v408 (o que a cadeia de preparacao e o orquestrador CHAMAM, e os autorais da v408) ----
RAIZ = ["acom_conferencias_v408.py", "acom_inscrever_prep_v408.py", "artigo_en_v408.pysnip", "artigo_pt_v408.pysnip", "carimbar_stdout_v408.py", "comparar_v407_v408.py", "conferir_citacoes_v408.py",
        "conferir_instalar_rito_v408.py", "conferir_rito_v408.py", "construir_kernel_v408.sh", "copiar_base_v408.py", "copiar_insumos_v408.py", "copiar_k408c.sh", "copiar_logs_do_kernel_v408.py", "delta_v408.py",
        "diff_e_pinos_v408.py", "ensaio_a_seco_v408.py", "exame_pontos_v408.py", "fechar_preparacao_v408.py", "fim_de_cadeia_v408.sh", "gerar_candidato_v408.py", "gerar_esperados_v408.py", "gerar_relatorio_v408.py",
        "guarda_frases_v408.py", "guarda_ordem_de_chamada_v408.py", "guarda_p18_v408.py", "guardas_estaticas_bancada_v408.py", "instalar_v408.py", "p00_precondicoes_v408.py", "pino_memoria_py_v408.py",
        "pos_build_kernel_v408.py", "preparar_bundle_v408_04nov.py", "purga_v408.py", "refazer_arvore_v408_pos_selo.py", "refazer_candidato_v408.sh", "refazer_sandbox_v408_pos_selo.sh", "regerar_v408.sh",
        "registros_v408.py", "regras_v408.py", "reverter_v408.py", "rito_v408.sh", "runtime_v408.py", "simular_arvore_do_nos_v408.py", "teste_conferidor_positivo_v408.py"]
POS_RITO = ["b3_recibo_v408.py", "chain_pos_rito_v408.sh", "fechar_v408.py", "fila_memoria_v408.py", "gerar_derivacao_pos_rito_v408.py", "gerar_x_custodia_v408.py", "harness_fechar_sandbox_v408.py",
            "harness_textos_ensaio_v408.py", "leitura_v408.py", "montar_textos_v408.py", "registrar_mapa_v408.py", "superficies_v408.py", "textos_v408.py", "textos_v408.semente", "textos_v408_novo.pysnip",
            "textos_custodia_handoff_v408.py"]
ORQ = ["pos_treino_v408.py"]
PRE_SELO = ["conferir_recibo_pre_selo_v408.py", "derivar_pre_selo_v408.py", "gerar_pino_recibo_pre_selo_v408.py", "limpar_sandbox_vb21.py", "rodar_bn_pre_selo_v408.sh", "rodar_ensaio_1_pre_selo_v408.sh", "snap_producao_v408.py"]
SERVICO = ["conferir_exigencias_servico_v408.py", "evento_c1_b3_v408.py", "recibo_parada_v408.py", "recibo_religamento_v408.py", "controle_negativo/mutar_conferidor_v408.py"]
MOLDES = list(RAIZ) + ["pos_rito/" + x for x in POS_RITO] + ["orquestrador/" + x for x in ORQ] + ["bateria_pre_selo/" + x for x in PRE_SELO] + ["bancada_B3_servico/" + x for x in SERVICO]
COPIA_LITERAL = ["quadro_v397.py", "runtime_quadro_v397.py"]       # v397: nao sobem (o quadro do Teste da Unica Palavra segue intocado)
RENOMEIA = {"preparar_bundle_v409_04nov.py": "preparar_bundle_v409_05nov.py"}   # o rotulo de data do preparo do bundle (o motor so' sobe versao)

RX_N = re.compile(r"(?<![0-9])(407|408)(?![0-9])")
MAPA_N = {"407": "408", "408": "409"}
RX_B = re.compile(r"(?<![0-9A-Za-z_])B(16|17)(?![0-9A-Za-z_])")
DEP_VELHO = "B16-v407-20261104-R1"
_BANC = json.load(open(r"C:\IALD\Bancada_Um\canonical_contracts.json", encoding="utf-8"))
DEP_NOVO = str(_BANC["deployment_id"])                     # lido: o que a Bancada de producao pina HOJE (a v408 aplicada)
assert re.match(r"B17-v408-\d{8}-R1$", DEP_NOVO), DEP_NOVO
RX_WORD = re.compile(r"[A-Za-z0-9_]+")


def nome_destino(rel):
    d = RX_N.sub(lambda m: MAPA_N[m.group(1)], rel)
    base = d.split("/")[-1]
    if base in RENOMEIA:
        d = "/".join(d.split("/")[:-1] + [RENOMEIA[base]])
    return d


def norm(s):
    s = re.sub(r"(?<![0-9])(?:407|408|409)(?![0-9])", "@N", s)
    s = re.sub(r"(?<![0-9A-Za-z_])B1[678](?![0-9A-Za-z_])", "@B", s)
    return re.sub(r"-2026110[45]-R1", "-@D-R1", s)


def _modulos_da_cadeia():
    out = set()
    for sub in ("", "pos_rito", "orquestrador", "bateria_pre_selo", "bancada_B3_servico"):
        d = os.path.join(V8, sub)
        if os.path.isdir(d):
            out |= {f[:-3] for f in os.listdir(d) if f.endswith(".py")}
    return out


_MODS = _modulos_da_cadeia()
RX_IMPORT = re.compile(r"^[ \t]*(?:import[ \t]+(?P<imp>[^#\n]+)|from[ \t]+(?P<frm>[A-Za-z0-9_]+)[ \t]+import(?![A-Za-z0-9_]))", re.M)


def consertar_imports(t, novo):
    lo, ln = t.split("\n"), novo.split("\n")
    n = 0
    for m in RX_IMPORT.finditer(t):
        i = t.count("\n", 0, m.start())
        mods = [m.group("frm")] if m.group("frm") else [x.strip().split()[0] for x in m.group("imp").split(",") if x.strip()]
        for md in mods:
            if RX_N.search(md) and md in _MODS and md in ln[i]:
                novo_md = RX_N.sub(lambda mm: MAPA_N[mm.group(1)], md)
                ln[i] = re.sub(r"(?<![A-Za-z0-9_])" + re.escape(md) + r"(?![A-Za-z0-9_])", novo_md, ln[i], count=1)
                n += 1
    return "\n".join(ln), n


def subir(t):
    c = {}
    novo = MOTOR.bump(t, (), "v408")
    novo, c["imports_consertados"] = consertar_imports(t, novo)
    c["deployment_antes"] = t.count(DEP_VELHO)
    novo = RX_B.sub(lambda m: "B" + str(int(m.group(1)) + 1), novo)
    dep_pos_B = DEP_VELHO.replace("B16", "B17").replace("v407", "v408")
    c["deployment_trocado"] = novo.count(dep_pos_B)
    assert c["deployment_trocado"] == c["deployment_antes"], ("deployment nao casou", c)
    novo = novo.replace(dep_pos_B, DEP_NOVO)
    return novo, c


def cabecalho(dest_rel, molde_rel):
    return "# [A ADAPTAR v409] SUBIDA MECANICA DE ROTULO (v408->v409) do molde v408/%s; o CORPO e' o da v408 (bundle de 4 modulos, tetelestai_terminal_v408, 48 ancoras); nada rodou; ver bump/%s.diff" % (molde_rel, dest_rel.replace("/", "__"))


def insere_cabecalho(texto, linha, comentario="#"):
    ls = texto.split("\n")
    i = 0
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
        bk = dst + ".bak_" + TS
        open(bk, "wb").write(atual)
        estado = "regravado_com_backup"
    else:
        estado = "gravado"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst + ".tmp", "wb").write(novo_b)
    assert os.path.getsize(dst + ".tmp") == len(novo_b)
    os.replace(dst + ".tmp", dst)
    return estado


def main():
    so = None
    if "--so" in sys.argv:
        so = sys.argv[sys.argv.index("--so") + 1:]
    res = {}
    os.makedirs(BUMPDIR, exist_ok=True)
    for rel in MOLDES + COPIA_LITERAL:
        if so and rel not in so and os.path.basename(rel) not in so:
            continue
        ps = os.path.join(V8, *rel.split("/"))
        if not os.path.exists(ps):
            res[rel] = {"erro": "molde ausente em v408"}
            continue
        raw = open(ps, "rb").read()
        t = raw.decode("utf-8")
        if rel in COPIA_LITERAL:
            dest_rel, novo, c = rel, t, {}
        else:
            dest_rel = nome_destino(rel)
            novo, c = subir(t)
            # verificacao independente: so' rotulos mudaram
            lo, ln = t.split("\n"), novo.split("\n")
            assert len(lo) == len(ln), ("numero de linhas mudou", rel)
            ruins = [i + 1 for i, (a, b) in enumerate(zip(lo, ln)) if a != b and norm(a) != norm(b)]
            assert not ruins, ("linha alterada alem de rotulos", rel, ruins[:5])
            if dest_rel.endswith((".py", ".sh", ".pysnip", ".semente")):
                novo, pos = insere_cabecalho(novo, cabecalho(dest_rel, rel))
            if dest_rel.endswith(".py"):
                ast.parse(novo)
            elif dest_rel.endswith(".sh"):
                r = subprocess.run(["sh", "-n"], input=novo.encode("utf-8"), capture_output=True)
                assert r.returncode == 0, (dest_rel, r.stderr[:200])
        pd = os.path.join(HERE, *dest_rel.split("/"))
        novo_b = novo.encode("utf-8")
        estado = "seco" if SECO else grava(pd, novo_b)
        d = "".join(difflib.unified_diff(t.splitlines(True), novo.splitlines(True), fromfile="v408/" + rel, tofile="v409/" + dest_rel, n=0))
        if not SECO and dest_rel != rel:
            open(os.path.join(BUMPDIR, dest_rel.replace("/", "__") + ".diff"), "w", encoding="utf-8").write(d)
        res[rel] = {"destino": dest_rel, "estado": estado, "molde_sha16": sha16(raw), "destino_sha16": sha16(novo_b), "linhas_alteradas": sum(1 for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")), **c}
    if not SECO and not so:
        json.dump(res, open(os.path.join(HERE, "BUMP_v409_RESULTADO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: (v.get("estado"), v.get("linhas_alteradas")) for k, v in res.items()}, ensure_ascii=False)[:4000])
    erros = {k: v for k, v in res.items() if "erro" in v}
    print("ERROS:", erros)
    print("N:", len(res))


main()

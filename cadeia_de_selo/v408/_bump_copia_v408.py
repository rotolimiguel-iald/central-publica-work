# -*- coding: utf-8 -*-
"""_bump_copia_v408.py -- COPIA + SUBIDA DE ROTULO (nao e' o motor de regras) dos scripts da cadeia v407 para cadeia_de_selo\\v408 (claude-prep-v408, 04/11/2026).
Receita: copiar o molde de cadeia_de_selo\\v407 (SO' LEITURA) e subir SO' os rotulos de versao: 406 -> 407 e 407 -> 408 (uma passada, simultanea; 399 a 404 NAO sobem), k407c -> k408c, h407 -> h408, base_v406 -> base_v407, B15 -> B16 e B16 -> B17 (so' como palavra solta),
B15-v406-20261103-R1 -> B16-v407-20261104-R1 (o deployment da v407 foi LIDO de C:\\IALD\\Bancada_Um\\canonical_contracts.json). Os nomes nascidos no um.py v407 (identificadores com 406/407 que existem no texto da base) NAO sobem: usa-se a funcao bump() do derivar_v408_motor.py (so' o mapa;
NENHUMA regra de contagem exata, NENHUM texto reescrito). NAO muda logica, narrativa nem listas de pedras: cada arquivo ganha um comentario de UMA linha `# [A ADAPTAR v408] ...` (o p00 recusa arquivo com essa marca; ela sai quando o arquivo for adaptado de verdade).
Para cada arquivo: bump/<nome>.diff, verificacao INDEPENDENTE de que toda linha alterada difere do molde so' em rotulos, ast.parse / sh -n. NUNCA executa os scripts copiados. Nao sobrescreve nada existente sem backup de bytes (.bak_<ts>).
Uso: python -I -B -X utf8 _bump_copia_v408.py [--seco] [--so ARQ ...]"""
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
V6 = os.path.join(CH, "v407")
BUMPDIR = os.path.join(HERE, "bump")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]

_spec = importlib.util.spec_from_file_location("derivar_v408_motor", os.path.join(HERE, "derivar_v408_motor.py"))
MOTOR = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(MOTOR)

# ---- os moldes: caminho relativo em v407 (so' o que a cadeia de preparacao e o orquestrador CHAMAM) ----
RAIZ = ["acom_conferencias_v407.py", "comparar_v406_v407.py", "conferir_citacoes_v407.py", "conferir_instalar_rito_v407.py", "conferir_rito_v407.py", "copiar_base_v407.py", "copiar_insumos_v407.py", "copiar_logs_do_kernel_v407.py",
        "diff_e_pinos_v407.py", "ensaio_a_seco_v407.py", "exame_pontos_v407.py", "fechar_preparacao_v407.py", "fim_de_cadeia_v407.sh", "gerar_esperados_v407.py", "gerar_relatorio_v407.py", "guarda_frases_v407.py", "guarda_ordem_de_chamada_v407.py",
        "guarda_p18_v407.py", "guardas_estaticas_bancada_v407.py", "instalar_v407.py", "p00_precondicoes_v407.py", "pino_memoria_py_v407.py", "pos_build_kernel_v407.py", "purga_v407.py", "refazer_arvore_v407_pos_selo.py", "refazer_candidato_v407.sh",
        "refazer_sandbox_v407_pos_selo.sh", "regerar_v407.sh", "regras_v407.py", "reverter_v407.py", "rito_v407.sh", "simular_arvore_do_nos_v407.py", "teste_conferidor_positivo_v407.py", "gerar_candidato_v407.py", "runtime_v407.py", "registros_v407.py"]
POS_RITO = ["b3_recibo_v407.py", "chain_pos_rito_v407.sh", "fechar_v407.py", "fila_memoria_v407.py", "gerar_derivacao_pos_rito_v407.py", "gerar_x_custodia_v407.py", "harness_fechar_sandbox_v407.py", "harness_textos_ensaio_v407.py", "leitura_v407.py",
            "montar_textos_v407.py", "registrar_mapa_v407.py", "superficies_v407.py", "textos_v407.semente", "textos_v407_novo.pysnip", "textos_custodia_handoff_v407_03nov.py"]
ORQ = ["pos_treino_v407.py"]
PRE_SELO = ["conferir_recibo_pre_selo_v407.py", "derivar_pre_selo_v407.py", "gerar_pino_recibo_pre_selo_v407.py", "limpar_sandbox_vb21.py", "rodar_bn_pre_selo_v407.sh", "rodar_ensaio_1_pre_selo_v407.sh", "snap_producao_v407.py"]
SERVICO = ["conferir_exigencias_servico_v407.py", "evento_c1_b3_v407.py", "recibo_parada_v407.py", "recibo_religamento_v407.py", "controle_negativo/mutar_conferidor_v407.py"]
MOLDES = list(RAIZ) + ["pos_rito/" + x for x in POS_RITO] + ["orquestrador/" + x for x in ORQ] + ["bateria_pre_selo/" + x for x in PRE_SELO] + ["bancada_B3_servico/" + x for x in SERVICO]
COPIA_LITERAL = ["quadro_v397.py", "runtime_quadro_v397.py"]       # v397: nao sobem (o quadro do Teste da Unica Palavra segue intocado)

RX_N = re.compile(r"(?<![0-9])(406|407)(?![0-9])")
MAPA_N = {"406": "407", "407": "408"}
RX_B = re.compile(r"(?<![0-9A-Za-z_])B(15|16)(?![0-9A-Za-z_])")
DEP_VELHO = "B15-v406-20261103-R1"
_BANC = json.load(open(r"C:\IALD\Bancada_Um\canonical_contracts.json", encoding="utf-8"))
DEP_NOVO = str(_BANC["deployment_id"])                     # lido: o que a Bancada de producao pina HOJE (a v407 aplicada)
assert re.match(r"B16-v407-\d{8}-R1$", DEP_NOVO), DEP_NOVO
RX_WORD = re.compile(r"[A-Za-z0-9_]+")


def nome_destino(rel):
    return RX_N.sub(lambda m: MAPA_N[m.group(1)], rel)


def norm(s):
    s = re.sub(r"(?<![0-9])(?:406|407|408)(?![0-9])", "@N", s)
    s = re.sub(r"(?<![0-9A-Za-z_])B1[567](?![0-9A-Za-z_])", "@B", s)
    return re.sub(r"-2026110[34]-R1", "-@D-R1", s)


def _modulos_da_cadeia():
    out = set()
    for sub in ("", "pos_rito", "orquestrador", "bateria_pre_selo", "bancada_B3_servico"):
        d = os.path.join(V6, sub)
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
    novo = MOTOR.bump(t, (), "v407")
    novo, c["imports_consertados"] = consertar_imports(t, novo)
    c["deployment_antes"] = t.count(DEP_VELHO)
    novo = RX_B.sub(lambda m: "B" + str(int(m.group(1)) + 1), novo)
    dep_pos_B = DEP_VELHO.replace("B15", "B16").replace("v406", "v407")
    c["deployment_trocado"] = novo.count(dep_pos_B)
    assert c["deployment_trocado"] == c["deployment_antes"], ("deployment nao casou", c)
    novo = novo.replace(dep_pos_B, DEP_NOVO)
    return novo, c


def cabecalho(dest_rel, molde_rel):
    return "# [A ADAPTAR v408] SUBIDA MECANICA DE ROTULO (v407->v408) do molde v407/%s; o CORPO e' o da v407 (bundle de 9 modulos, psion_canto_v407, a chave do lema lida do kernel); nada rodou; ver bump/%s.diff" % (molde_rel, dest_rel.replace("/", "__"))


def insere_cabecalho(texto, linha):
    ls = texto.split("\n")
    i = 0
    if ls and ls[0].startswith("#!"):
        i = 1
    if i < len(ls) and re.match(r"#.*coding[:=]", ls[i]):
        i += 1
    ends_cr = "\r" if (len(ls) > i and ls[i].endswith("\r")) else ""
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
        ps = os.path.join(V6, *rel.split("/"))
        if not os.path.exists(ps):
            res[rel] = {"erro": "molde ausente em v407"}
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
            novo, pos = insere_cabecalho(novo, cabecalho(dest_rel, rel))
            if dest_rel.endswith(".py"):
                ast.parse(novo)
            elif dest_rel.endswith(".sh"):
                r = subprocess.run(["sh", "-n"], input=novo.encode("utf-8"), capture_output=True)
                assert r.returncode == 0, (dest_rel, r.stderr[:200])
        pd = os.path.join(HERE, *dest_rel.split("/"))
        novo_b = novo.encode("utf-8")
        estado = "seco" if SECO else grava(pd, novo_b)
        d = "".join(difflib.unified_diff(t.splitlines(True), novo.splitlines(True), fromfile="v407/" + rel, tofile="v408/" + dest_rel, n=0))
        if not SECO and dest_rel != rel:
            open(os.path.join(BUMPDIR, dest_rel.replace("/", "__") + ".diff"), "w", encoding="utf-8").write(d)
        res[rel] = {"destino": dest_rel, "estado": estado, "molde_sha16": sha16(raw), "destino_sha16": sha16(novo_b), "linhas_alteradas": sum(1 for l in d.splitlines() if l.startswith("+") and not l.startswith("+++")), **c}
    if not SECO and not so:
        json.dump(res, open(os.path.join(HERE, "BUMP_v408_RESULTADO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: (v.get("estado"), v.get("linhas_alteradas")) for k, v in res.items()}, ensure_ascii=False)[:3000])
    erros = {k: v for k, v in res.items() if "erro" in v}
    print("ERROS:", erros)
    print("N:", len(res))


main()

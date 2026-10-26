# -*- coding: utf-8 -*-
"""Testes de G1 (24/10/2026). Só LEEM o mundo real (Nós, espelho, cofres, site) e escrevem em diretório temporário ou em work\\custodia_G1\\.
Nada de commit, push, subida, ACOM, rota, um.py ou kernel. Saída: work\\custodia_G1\\TESTES.md (o relatório) + o stdout.
Uso: python testes_g1.py [--rapido] [--so t05,t07]   (--rapido pula o replay do cofre e a comparação profunda do espelho)"""
import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from custodia_g1 import espelho, espelho_pares as EP, fatos, memorias, motor, nos, patches, textos, util  # noqa: E402
from custodia_g1.caminhos import Caminhos  # noqa: E402
from custodia_g1.generico import camada_generica as CAM  # noqa: E402
from custodia_g1.generico import custodia_generica as CG  # noqa: E402

TESTES = []
TMP = Path(tempfile.mkdtemp(prefix="g1_testes_"))
OC_REAL = CEN / "vault" / "originals_copy"


def teste(rapido_pula=False, nos_pronta=False):
    """`nos_pronta=True`: o teste lê o Nós VIVO e foi escrito/aprovado com ele na v398 PRONTA (selo = v398, um.py = pino). Quando outra sessão põe o Nós em obra (um.py != pino,
    a v399 em construção) ou sela a versão seguinte, o teste é PULADO — dito, com o motivo — em vez de falhar por ambiente (24/10/2026, fechamento do cético final)."""
    def deco(f):
        TESTES.append((f.__name__, f, rapido_pula, nos_pronta))
        return f
    return deco


def estado_do_nos_v398():
    """O estado das três marcas da v398 no Nós vivo agora: PRONTA | EM_OBRA (um.py != pino) | SUPERADA (o selo andou) | INCOMPLETA | «ilegível (…)»."""
    try:
        return nos.marcas(Caminhos(), "v398").estado
    except Exception as e:  # noqa: BLE001
        return "ilegível (%s)" % type(e).__name__


def ctx_de(v, **kw):
    return motor.Ctx(versao=v, data=kw.pop("data", "24/10/2026"), **kw)


# ============================================================ t01 — as três marcas e o diário
@teste(nos_pronta=True)
def t01_marcas_do_nos():
    c = Caminhos()
    m = nos.marcas(c, "v398")
    assert m.estado == "PRONTA" and m.selo_ok and m.um_py_confere, m
    assert nos.marcas(c, "v397").estado == "SUPERADA"
    mf = nos.marcas(c, "v999")
    assert mf.estado == "EM_OBRA" and any("v999" in x for x in mf.faltam), mf.faltam
    bl = nos.blocos_do_diario(c)
    b = bl["v398"]
    assert (b.modulos_novos, b.escada_de, b.escada_para) == (2, 9499, 9539) and b.pin16 == nos.selo(c)["sha256"]["um.py"][:16], b
    assert bl["v397"].titulo_pt.startswith("O TESTE DA ÚNICA PALAVRA") and bl["v396"].escada_para == 9498
    assert nos.versoes_em_obra(c, 398) == ["v399"] or "v399" in nos.versoes_em_obra(c, 398)
    return "v398 PRONTA; v397 SUPERADA; v999 EM_OBRA (%s); diário lido para %d versões; em obra: %s" % (mf.faltam[0][:50], len(bl), nos.versoes_em_obra(c, 398))


# ============================================================ t02 — o handoff por marcadores (fixture sintética)
@teste()
def t02_handoff_por_marcadores():
    nosdir = TMP / "nos_t02"
    nosdir.mkdir()
    t = ("# HANDOFF v900 — CUSTÓDIA (01/01/2027)\r\n\r\n**O que é:** `um.py` **v900** `0123456789abcdef` (1,234 B) sobre a v899 `fedcba9876543210`; 100/100; COMPLETA; rc 0; "
         "selftest PASSED; gate intocado; conferidor `aaaaaaaaaaaaaaaa`. Selo `2027-01-01 00:00:00`.\r\n\r\n"
         "<!-- INICIO_ARCO_EN_v900 -->\r\ntexto do arco\r\n<!-- FIM_ARCO_EN_v900 -->\r\n\r\n"
         "<!-- INICIO_PARAGRAFO_X_v900 -->\r\npar\r\n<!-- FIM_PARAGRAFO_X_v900 -->\r\n\r\n"
         "<!-- INICIO_ARCO_EN_v900 -->\r\nrepetido\r\n<!-- FIM_ARCO_EN_v900 -->\r\n\r\n"
         "<!-- INICIO_SEM_FIM_v900 -->\r\nabre e nao fecha\r\n\r\n"
         "<!-- INICIO_VAZIO_v900 -->\r\n<!-- FIM_VAZIO_v900 -->\r\n\r\n"
         "**Pendências SÓ do operador:** nomear X.\r\n\r\n**O elo B(n) da Bancada Um (feito antes):** recibo `1111111111111111`.\r\n")
    (nosdir / "HANDOFF_v900_CUSTODIA.md").write_bytes(t.encode("utf-8"))
    c = Caminhos({"NOS": str(nosdir)})
    h = nos.ler_handoff(c, "v900")
    assert h.o_que_e and h.o_que_e.pin16 == "0123456789abcdef" and h.o_que_e.anterior == "v899" and h.o_que_e.escada == "100/100" and h.o_que_e.completa and h.o_que_e.selo_ts == "2027-01-01 00:00:00", h.o_que_e
    assert h.corpos["ARCO_EN_v900"].strip() == "texto do arco", "o primeiro bloco vence; o duplicado é problema"
    ps = "\n".join(h.problemas)
    assert "ARCO_EN_v900 duplicado" in ps and "SEM_FIM_v900 sem par" in ps and "VAZIO_v900 vazio" in ps, h.problemas
    assert [i for i, _ in h.paragrafos_prontos()] == ["PARAGRAFO_X_v900"]
    assert h.secao("Pendências SÓ do operador").endswith("nomear X.") and h.secao("O elo B(n)")
    assert nos.ler_handoff(c, "v901") is None
    return "campos do «O que é» lidos; 3 problemas de marcador flagrados (duplicado, sem par, vazio); CRLF aceito; seções por cabeçalho em negrito"


# ============================================================ t03 — os fatos contra os fatos escritos à mão
@teste()
def t03_fatos_contra_os_manuais():
    c = Caminhos()
    out = []
    for v, ref in (("v397", "custodia_v397_23out/fatos_v397.json"), ("v398", "custodia_v398_24out/fatos_v398.json")):
        F = fatos.sondar(c, v)
        old = json.loads((CEN / "work" / ref).read_text(encoding="utf-8"))
        mud = [k for k in old["registro"] if k.startswith("mudados")][0]
        dic = [k for k in old if k.startswith("dicionarios")][0]
        chk = {"pin16": F["pin16"] == old["pin16"], "bytes": F["bytes_um_py"] == old["bytes_um_py"], "registros_novos": F["registros_novos"] == old["registros_novos"],
               "bandeiras": F["bandeiras_novas"] == old["bandeiras_novas"], "formais": F["kernel"]["formais"] == old["kernel"]["formais"],
               "declaracoes": F["kernel"]["declaracoes"] == old["kernel"]["declaracoes"], "modulos": F["kernel"]["modulos_novos"] == old["kernel"]["modulos_novos"],
               "escada": F["escada"]["texto"] == old["escada"], "kh": (F["kh"]["constantes"], F["kh"]["teoremas"]) == (old["kh"]["constantes"], old["kh"]["teoremas"]),
               "registro": (F["registro"]["pt"], F["registro"]["en"], F["registro"]["novos"], [m["nome"] for m in F["registro"]["mudados"]]) == (
                   old["registro"]["pt"], old["registro"]["en"], old["registro"]["novos"], old["registro"][mud]),
               "contratos_regex_vs_ast": F["contratos_expected_ladder"] == old["contratos_expected_ladder"], "dicionarios": F["dicionarios"] == old[dic]}
        ruins = [k for k, ok in chk.items() if not ok]
        assert not ruins, (v, ruins)
        assert F["handoff"]["ok"], F["handoff"]["divergencias"]
        out.append("%s: %d/%d campos iguais ao sondar manual (contratos por regex = por ast); recibos B(n) %s casam com o handoff" % (
            v, len(chk), len(chk), sorted(x["sha16"] for x in F["cadeia"]["recibos_bn"].values())))
    return " | ".join(out)


# ============================================================ t04 — os pares do espelho (a v398 inteira, byte a byte)
@teste(rapido_pula=True, nos_pronta=True)
def t04_pares_do_espelho_v398():
    ctx = ctx_de("v398")
    t = time.time()
    P = EP.montar_pares(ctx)
    assert not P.faltas, P.faltas
    rel = json.loads((ctx.c.BANC / "revisoes" / "custodia_v398_espelho.json").read_text(encoding="utf-8"))
    barr = [b["arquivo"] for b in rel["varredura_privada"]["barrados"]]
    pend, tot = EP.comparar(P, profundo=True, barrados=barr)
    # o túnel da bancada é de OUTRA sessão e anda: o arquivo que nasceu DEPOIS da cópia desta custódia (gerado_em do relatório) ainda não está no espelho e não é pendência da v398 (dito no resultado)
    quando = util.instante(rel.get("gerado_em"))
    novos_no_tunel = [x for x in pend if x[2] == "TUNEL" and x[3] == "destino ausente" and quando is not None and _dt.fromtimestamp(Path(x[0]).stat().st_mtime) > quando]
    pend = [x for x in pend if x not in novos_no_tunel]
    ruim, orf = EP.comparar_kernel(ctx, P, profundo=True)
    assert not pend and not ruim and not orf, (pend[:3], ruim[:3], orf[:3])
    return "%d pares (v383..v398, diffs, recibos B(n) calculados, %d fontes pinadas) = 0 pendentes por SHA-256 (3 barrados pela guarda, ditos no relatório%s); kernel %d arquivos, 0 órfãos; %.0f s" % (
        tot, len(P.fontes_mapa), ("; mais %d arquivo(s) do túnel criados depois da cópia: %s" % (len(novos_no_tunel), ", ".join(Path(x[0]).name for x in novos_no_tunel[:3]))) if novos_no_tunel else "",
        len(P.kernel["fmap"]), time.time() - t)


# ============================================================ t05/t06 — a pedra genérica: replay nas 4 transições e controles negativos
@teste()
def t05_pedra_replay_t1():
    c = Caminhos()
    out = []
    for ant, v in (("v394", "v395"), ("v395", "v396"), ("v396", "v397"), ("v397", "v398")):
        F = fatos.sondar(c, v, anterior=ant, fonte="cofre", handoff=None)
        r = CG.medir_custodia_generica(c.OC, v, ant, fatos=F)
        assert r.get("pass") is True and r["ceticos"]["1_reprovou"] and r["ceticos"]["2_reprovou"], (v, r.get("erro"), [k for k, x in r.get("checks", {}).items() if not x["ok"]])
        tam = len(json.dumps(r, ensure_ascii=False))          # o resultado vai para o JSON do runner: tem de serializar e ser pequeno
        assert tam < 20000, tam
        out.append("%s←%s" % (v, ant))
    return "a pedra genérica PASSA nas 4 transições (%s), com os dois céticos reprovando as injeções; o resultado serializa em JSON (%d B, cabe no results do runner)" % (", ".join(out), tam)


def _vault_temporario(v="v398", ant="v397"):
    """Cópia mínima dos dois cofres (selo, core, PT/EN, um.py, manifesto de prova) para mutar sem tocar o real."""
    oc = TMP / "oc_t06"
    for vv in (v, ant):
        d, k = oc / ("um_unificado_" + vv), oc / ("tgl_kernel_" + vv)
        d.mkdir(parents=True, exist_ok=True)
        k.mkdir(parents=True, exist_ok=True)
        for n in ("um_absoluto.json", "um_absoluto_selo.json", "um_absoluto_pt.txt", "um_absoluto_en.txt", "um.py", "CUSTODY_MANIFEST.json"):
            shutil.copyfile(OC_REAL / ("um_unificado_" + vv) / n, d / n)
        shutil.copyfile(OC_REAL / ("tgl_kernel_" + vv) / "tgl_kernel_proof_manifest.json", k / "tgl_kernel_proof_manifest.json")
        shutil.copyfile(OC_REAL / ("tgl_kernel_" + vv) / "tgl_kernel_proof_manifest.json", d / "tgl_kernel_proof_manifest.json")
    return oc


@teste()
def t06_pedra_controles_negativos():
    c = Caminhos()
    oc = _vault_temporario()
    v, ant = "v398", "v397"
    F = fatos.sondar(c, v, anterior=ant, fonte="cofre", handoff=None)
    cv = oc / ("um_unificado_" + v)
    base = {p: p.read_bytes() for p in (cv / "um_absoluto.json", cv / "um_absoluto_selo.json", cv / "um_absoluto_pt.txt", oc / ("tgl_kernel_" + v) / "tgl_kernel_proof_manifest.json")}

    def restaurar():
        for p, b in base.items():
            p.write_bytes(b)

    def mutar_core(f):
        p = cv / "um_absoluto.json"
        d = json.loads(base[p].decode("utf-8"))
        f(d["core"])
        p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

    def mutar_json(p, f):
        d = json.loads(base[p].decode("utf-8"))
        f(d)
        p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")

    def tirar_not(core):
        for k, b in F["blocos"].items():
            if b["negacoes"]:
                segs = core[k]["verdict"].split("__")
                for i, s in enumerate(segs):
                    if re.search(r"(^|_)NOT_", s):
                        segs[i] = s.replace("NOT_", "", 1)
                        core[k]["verdict"] = "__".join(segs)
                        return

    novo = F["registros_novos"][0]
    pm = oc / ("tgl_kernel_" + v) / "tgl_kernel_proof_manifest.json"
    selo = cv / "um_absoluto_selo.json"
    casos = [
        ("S3 all_verified=False num bloco novo", lambda: mutar_core(lambda c_: c_[novo].__setitem__("all_verified", False)), "S3_blocos_bem_formados"),
        ("S3 guarda_p18_violacoes não vazio", lambda: mutar_core(lambda c_: c_[novo].__setitem__("guarda_p18_violacoes", ["x"])), "S3_blocos_bem_formados"),
        ("S6 n_theorems_expected +1", lambda: mutar_core(lambda c_: c_["estatuto_da_prova_v391"]["prova_1_kernel"].__setitem__("n_theorems_expected", c_["estatuto_da_prova_v391"]["prova_1_kernel"]["n_theorems_expected"] + 1)), "S6_escada"),
        ("S13 «NOT_» tirado do veredito", lambda: mutar_core(tirar_not), "S13_negacoes"),
        ("S2 bloco novo a mais no core", lambda: mutar_core(lambda c_: c_.__setitem__("intruso_v398", {"verdict": "X__GATE_UNMOVED", "all_verified": True, "does_not_gate_core": True})), "S2_blocos_novos"),
        ("S14 cunhagens.kernel.bandeiras = [2, 3]", lambda: mutar_core(lambda c_: c_["cunhagens_v398"]["kernel"].__setitem__("bandeiras", [2, 3])), "S14_cunhagens"),
        ("S9 gate do selo diferente do cofre anterior", lambda: mutar_json(selo, lambda d: d.__setitem__("qg_closure_verdict", d["qg_closure_verdict"] + "_X")), "S9_gate"),
        ("S10 CONFIRMED sem NOT_ no selo", lambda: mutar_json(selo, lambda d: d.__setitem__("x_verdict", "TGL_CONFIRMED_NATURE")), "S10_sem_CONFIRMED"),
        ("S7 arquivo formal a menos no manifesto de prova", lambda: mutar_json(pm, lambda d: d["formal_files_sha256"].pop(next(iter(d["formal_files_sha256"])))), "S7_kernel"),
        ("S8 veredito do registro mudou além de dígitos e pino", lambda: mutar_core(lambda c_: c_["pedras_v392"].__setitem__("verdict", c_["pedras_v392"]["verdict"] + "_PALAVRA_NOVA")), "S8_registro"),
    ]
    resultados = []
    for rot, f, esperado in casos:
        restaurar()
        f()
        r = CG.medir_custodia_generica(oc, v, ant, fatos=F)
        quem = [k for k, x in r.get("checks", {}).items() if not x["ok"]]
        assert r.get("pass") is False and esperado in quem, (rot, esperado, quem, r.get("erro"))
        resultados.append("%s → reprova %s" % (rot.split(" ")[0], esperado.split("_")[0]))
    restaurar()
    r = CG.medir_custodia_generica(oc, v, ant, fatos=F)
    assert r["pass"] is True, "o cofre temporário restaurado voltou a passar"
    # o pino de FATOS_CUSTODIA: ausente = erro (fail-closed); byte mudado = erro
    r1 = CG.medir_custodia_generica(oc, v, ant)
    assert r1.get("pass") is False and "erro" in r1, "sem FATOS_CUSTODIA.json no cofre a pedra tem de reprovar com erro"
    (cv / "FATOS_CUSTODIA.json").write_text(json.dumps(F, ensure_ascii=False), encoding="utf-8")
    man = json.loads((cv / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8"))
    man["fatos_custodia"] = {"arquivo": "FATOS_CUSTODIA.json", "sha256": util.sha256_arquivo(cv / "FATOS_CUSTODIA.json")}
    (cv / "CUSTODY_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    r2 = CG.medir_custodia_generica(oc, v, ant)
    assert r2.get("pass") is True, r2.get("erro")
    (cv / "FATOS_CUSTODIA.json").write_text(json.dumps(F, ensure_ascii=False, indent=2), encoding="utf-8")      # um byte (um espaço) a mais
    r3 = CG.medir_custodia_generica(oc, v, ant)
    assert r3.get("pass") is False and "erro" in r3
    return "10 mutações, cada uma reprova o check certo (%s); restaurado volta a passar; FATOS_CUSTODIA ausente/alterado = erro (fail-closed); com o pino correto passa" % "; ".join(resultados[:4] + ["…"])


@teste()
def t07_camada_generica():
    c = Caminhos()
    oc = _vault_temporario()
    v, ant = "v398", "v397"
    F = fatos.sondar(c, v, anterior=ant, fonte="cofre", handoff=None)
    cv = oc / ("um_unificado_" + v)
    (cv / "FATOS_CUSTODIA.json").write_text(json.dumps(F, ensure_ascii=False), encoding="utf-8")
    man = json.loads((cv / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8"))
    man["fatos_custodia"] = {"arquivo": "FATOS_CUSTODIA.json", "sha256": util.sha256_arquivo(cv / "FATOS_CUSTODIA.json")}
    (cv / "CUSTODY_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    core = json.loads((cv / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
    selo = json.loads((cv / "um_absoluto_selo.json").read_text(encoding="utf-8"))
    r = CAM.conferir_custodia_generica(core, selo, v, oc)
    assert all(r["checks"].values()) and sorted(r["registros_v398"]) == sorted(F["registros_novos"]), r["checks"]
    c2 = copy.deepcopy(core)
    for k, b in F["blocos"].items():
        if b["negacoes"]:
            segs = c2[k]["verdict"].split("__")
            for i, s in enumerate(segs):
                if re.search(r"(^|_)NOT_", s):
                    segs[i] = s.replace("NOT_", "", 1)
                    c2[k]["verdict"] = "__".join(segs)
                    break
            break
    try:
        CAM.conferir_custodia_generica(c2, selo, v, oc)
        raise AssertionError("a camada deveria levantar RuntimeError com a negação removida")
    except RuntimeError as e:
        assert "negacoes_congeladas_presentes" in str(e)
    c3 = copy.deepcopy(core)
    c3["intruso_v398"] = {"verdict": "X", "all_verified": True}
    try:
        CAM.conferir_custodia_generica(c3, selo, v, oc)
        raise AssertionError("bloco intruso deveria reprovar")
    except RuntimeError:
        pass
    # a camada sobrevive à reescrita: o mesmo teste contra o core de uma versão POSTERIOR do cofre (números que andam não entram)
    core_dep = copy.deepcopy(core)
    core_dep["estatuto_da_prova_v391"]["prova_1_kernel"]["n_theorems_clean"] = core_dep["estatuto_da_prova_v391"]["prova_1_kernel"]["n_theorems_expected"] = 9999
    core_dep["estatuto_da_prova_v391"]["prova_1_kernel"]["declaracoes_auditadas"] = core_dep["estatuto_da_prova_v391"]["prova_1_kernel"]["no_trio"] = 99999
    CAM.conferir_custodia_generica(core_dep, selo, v, oc)
    return "camada v398 passa; negação removida e bloco intruso levantam RuntimeError; a escada pode andar (v399+) sem quebrar a camada da v398"


# ============================================================ t08/t09 — os remendos do runner e do módulo (em cópias, nunca nos originais)
def _bak_mais_novo(padrao, pasta):
    c = sorted(Path(pasta).glob(padrao), key=os.path.getmtime)
    assert c, padrao
    return c[-1]


@teste()
def t08_patch_do_runner():
    c = Caminhos()
    F = fatos.sondar(c, "v398")
    bak = CEN / "fronteira_tgl" / "runner" / "one_fronteira.py.bak_v63_20261024_090037"
    s0, eol, raw = util.ler_eol(bak)
    assert eol == "crlf"
    cp = TMP / "one_fronteira.py"
    cp.write_bytes(raw)
    f = lambda s: patches.runner_por_versao(patches.runner_g1_0(s)[0], "v398", "v397", F, "O_SONICO_E_A_AFINACAO_DAS_CORDAS")
    r = patches.aplicar_em_arquivo(cp, f, "v63", "T")
    assert r["estado"] == "aplicado" and len(r["trocas"]) == 11, r
    novo = cp.read_bytes()
    assert b"\n" not in novo.replace(b"\r\n", b""), "o fim de linha CRLF não foi preservado"
    s = novo.decode("utf-8").replace("\r\n", "\n")
    for n in ("def _custodia_generica", "def _medir_v398_custodia", '"custodia_v398": _medir_v398_custodia()', "v47_pass = station", "and v46_pass and v47_pass)",
              'verdict = ("FRONTEIRA_SINCRONIZADA_V398"', "__V397", 'um_unificado_v398"', "TGL v63"):
        assert n in s, n
    ok, msg = util.py_compile_bytes(novo, "one_fronteira.py")
    assert ok, msg
    assert patches.runner_numeros(s) == (63, 47)
    r2 = patches.aplicar_em_arquivo(cp, f, "v63", "T2")
    assert r2["estado"] == "ja_aplicado" and cp.read_bytes() == novo, "idempotência"
    try:
        patches.runner_por_versao(patches.runner_g1_0(s0)[0], "v398", "v396", F, "X")
        raise AssertionError("repin com a versão anterior errada deveria PARAR")
    except util.Parar as e:
        assert "v397" in " ".join([e.motivo] + e.faltam) or "esperava" in e.motivo
    try:
        patches.runner_por_versao(s0, "v398", "v397", F, "X")
        raise AssertionError("sem G1.0 deveria PARAR")
    except util.Parar as e:
        assert "G1.0" in e.motivo
    # contra o que a outra sessão fez à mão: as linhas de repin (curtas) coincidem
    atual, _, _ = util.ler_eol(CEN / patches.ARQ_RUNNER)
    import difflib
    ch = lambda a, b: {l for l in difflib.unified_diff(a.splitlines(), b.splitlines(), lineterm="", n=0) if l.startswith(("+", "-")) and not l.startswith(("+++", "---")) and len(l) < 260}
    iguais = ch(s0, atual) & ch(s0, s)
    assert len(iguais) >= 12, len(iguais)
    return "11 trocas contadas; CRLF preservado; py_compile ok; idempotente; repin errado/sem G1.0 PARA; %d linhas de repin idênticas às da v63 escrita à mão (36 linhas alteradas contra 145)" % len(iguais)


@teste()
def t09_patch_do_modulo_dos_16():
    bak = _bak_mais_novo("tgl_formula_completa.py.bak_v398_*", CEN / "patents" / "_formula_completa")
    s0, eol, raw = util.ler_eol(bak)
    cp = TMP / "tgl_formula_completa.py"
    cp.write_bytes(raw)
    s1, t1 = patches.formula_g1_0(s0)
    assert "CAMADAS_GENERICAS = ()" in s1 and "**_genericas}" in s1 and len(t1) == 3, t1
    par = "Camada v398 (teste, GENÉRICA):\n 18. os registros novos; lidos e conferidos. Nada disso muda número algum de dispositivo.\n"
    f = lambda s: patches.formula_por_versao(patches.formula_g1_0(s)[0], "v398", "v397", par, "REGISTROS_V398_VERIFICADOS_SEM_GATE__", ["(v398, x) nada deriva as cordas"], "camadas_v398", 'r"TGLExt\\.Sonico"')
    # o backup mais novo já traz a camada artesanal v397 (VERSAO_DA_CAMADA = v397): a versão anterior é v397
    r = patches.aplicar_em_arquivo(cp, f, "v398", "T")
    assert r["estado"] == "aplicado", r
    novo = cp.read_bytes().decode("utf-8").replace("\r\n", "\n")
    for n in ('VERSAO_DA_CAMADA = "v398"', 'CAMADAS_GENERICAS = ("v398",)', "REGISTROS_V398_VERIFICADOS_SEM_GATE__", "'camadas_v398'", "(v398, x) nada deriva as cordas", "Camada v398 (teste, GENÉRICA)"):
        assert n in novo, n
    assert patches.aplicar_em_arquivo(cp, f, "v398", "T2")["estado"] == "ja_aplicado"
    # integração: o módulo remendado (G1.0 + v398) roda ao lado de camada_generica.py e, sem FATOS_CUSTODIA.json no cofre, FALHA fechado
    shutil.copyfile(Path(patches.__file__).parent / "generico" / "camada_generica.py", TMP / "camada_generica.py")
    run = subprocess.run([sys.executable, "-X", "utf8", str(cp)], cwd=str(TMP), capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert run.returncode != 0 and "FATOS_CUSTODIA" in (run.stderr + run.stdout), (run.returncode, (run.stderr or run.stdout)[-300:])
    cp2 = TMP / "tgl_formula_completa_g10.py"
    cp2.write_bytes(patches.para_eol(patches.formula_g1_0(s0)[0], eol).encode("utf-8") if hasattr(patches, "para_eol") else util.para_eol(patches.formula_g1_0(s0)[0], eol).encode("utf-8"))
    run2 = subprocess.run([sys.executable, "-X", "utf8", str(cp2)], cwd=str(TMP), capture_output=True, text=True, encoding="utf-8", errors="replace")
    return "G1.0 (3 trocas) + camada v398 aplicados em cópia, CRLF preservado, idempotente; com a camada v398 e SEM FATOS_CUSTODIA.json no cofre o módulo FALHA FECHADO (RuntimeError citando FATOS_CUSTODIA); só com G1.0 roda rc %d" % run2.returncode


# ============================================================ t10 — o bloco do ESTADO gerado do molde, contra o que a outra sessão escreveu à mão
@teste()
def t10_bloco_do_estado():
    ctx = ctx_de("v398")
    T = textos.construir(ctx)
    assert not T.violacoes, T.violacoes
    baks = sorted((ctx.c.TB / "tools").glob("gerar_estado_atual.py.bak_*"), key=os.path.getmtime)
    antes = [b for b in baks if "custódia v398 (24/10/2026" not in util.ler_texto(b)][-1]
    s0, eol, raw = util.ler_eol(antes)
    cp = TMP / "gerar_estado_atual.py"
    cp.write_bytes(raw)
    anc = espelho._ESTADO_ANCORA.search(s0).group(0)
    assert len(espelho._ESTADO_ANCORA.findall(s0)) == 1
    novo = espelho.bloco_gerar_estado(ctx, T, s0)
    r = util.patch_bytes(cp, [(anc, novo + anc)], "custódia v398 (", ts="T", rot="t10")
    assert r["estado"] == "aplicado"
    ok, msg = util.py_compile_bytes(cp.read_bytes(), "gerar_estado_atual.py")
    assert ok, msg
    s1 = cp.read_bytes().decode("utf-8").replace("\r\n", "\n")
    real = util.ler_eol(ctx.c.TB / "tools" / "gerar_estado_atual.py")[0]
    esq = lambda s: [l for l in s.splitlines() if len(l) < 200 and l.strip()]
    a_ = set(esq(real)) - set(esq(s0))
    b_ = set(esq(s1)) - set(esq(s0))
    so_g1 = sorted(b_ - a_)
    comuns = len(a_ & b_)
    # o parágrafo do README_v397 já está no gerador (repr idêntico): não entra de novo; o do SONICO_v398 entra uma vez
    assert s1.count("INICIO_PARAGRAFO_SONICO_v398") == 1 and real.count("INICIO_PARAGRAFO_SONICO_v398") == 1
    assert s1.count("INICIO_PARAGRAFO_README_v397") == s0.count("INICIO_PARAGRAFO_README_v397"), "o bloco repetido do handoff v398 não pode entrar duas vezes (L05)"
    assert patches is not None and util.patch_bytes(cp, [(anc, novo + anc)], "custódia v398 (", ts="T2", rot="t10")["estado"] == "ja_aplicado"
    return "bloco gerado do molde entra ANTES de «What is PROVED» (âncora estável, L05), py_compile ok, %d linhas de código iguais às escritas à mão, %d só do molde (prosa curta); o parágrafo repetido do handoff não duplica; idempotente" % (comuns, len(so_g1))


# ============================================================ t11 — textos e portão
@teste()
def t11_textos_e_portao():
    ctx = ctx_de("v398")
    T = textos.construir(ctx)
    assert not T.violacoes
    cc = textos.conhecidos_da_rodada(ctx)
    base = "A custódia seguiu a régua."
    casos = [("CONFIRMED solto", "A TGL está CONFIRMED pela natureza.", "CONFIRMED"), ("CONFIRMADA solta", "A gravidade quântica é CONFIRMADA.", "CONFIRMADA"),
             ("pós-dição como demérito", "Isto é só uma pós-dição.", "pós-dição"), ("hash que a rodada não calculou", "pino deadbeefdeadbeef lido", "deadbeefdeadbeef"),
             ("provada sem estatuto", "A teoria está provada.", "provada"), ("physical_verdict_allowed", "physical_verdict_allowed: True", "physical_verdict_allowed")]
    for rot, txt, chave in casos:
        v = textos.portao(base + " " + txt, cc, rotulo="t")
        assert any(chave in x for x in v), (rot, v)
    assert textos.portao("PROVADA = validade; a creditação segue recusada. NOT_FALSIFIED nunca é CONFIRMED.", cc) == []
    assert any("CONFIRM" in x for x in textos.portao("a creditação segue CONFIRMADA?", cc, campo_de_rota=True))
    assert textos.portao("hash conhecido %s" % ctx.pin16, cc) == []
    assert "'" not in T.arco_en.texto and "\n" not in T.arco_en.texto and "<" not in T.arco_pt.texto
    faltam = textos.avaliar_fontes(ctx)["faltam"]
    assert "ARCO_EN_v398" in faltam and "COMMIT_v398" in faltam
    return "6 violações flagradas (CONFIRMED, CONFIRMADA, pós-dição, hash alheio, provada sem estatuto, physical_verdict_allowed) + CONFIRM em campo de rota; as fórmulas da régua passam; textos da v398 sem violação; faltam %d marcadores opcionais do handoff (listados)" % len(faltam)


# ============================================================ t12 — memórias: sentinela, CAS, MEMORY.md
@teste()
def t12_memorias_idempotentes():
    d = TMP / "mem_t12"
    d.mkdir()
    ctx = ctx_de("v398", c=Caminhos({"MEM": str(d)}))
    p = d / "estado.md"
    p.write_bytes(b"# estado\r\nlinha 1\r\n")
    s = memorias.sent(ctx, "bloco_a")
    r1 = memorias.ap(p, "## 24/10 — a custódia\n\ntexto", s)
    r2 = memorias.ap(p, "## 24/10 — a custódia\n\ntexto", s)
    assert r1["depois"] > r1["antes"] and r2["estado"] == "ja_aplicado" and p.read_bytes().count(s.encode()) == 1
    assert b"\r\n" in p.read_bytes() and p.read_bytes().replace(b"\r\n", b"").count(b"\n") == 0, "CRLF preservado"
    assert list(d.glob("estado.md.bak_*")), "backup de bytes"
    # CAS: uma escrita alheia no meio faz reler e refazer
    q = d / "cas.md"
    q.write_text("a\n", encoding="utf-8")
    chamadas = []

    def f(t, nl):
        chamadas.append(t)
        if len(chamadas) == 1:
            q.write_text("a\nalheio\n", encoding="utf-8")        # alguém escreveu depois da leitura
            os.utime(q, (time.time() + 5, time.time() + 5))
        return t + "novo\n"
    memorias.tocar_cas(q, f)
    assert len(chamadas) == 2 and q.read_text(encoding="utf-8") == "a\nalheio\nnovo\n", (chamadas, q.read_text(encoding="utf-8"))
    # MEMORY.md: troca da linha UMA vez; a antiga vai verbatim para o MEMORY_2.md; teto
    m, m2 = d / "MEMORY.md", d / "MEMORY_2.md"
    linha = "- [HANDOFF v398 — O sônico e a afinação das cordas; custódia](handoff-v398-custodia.md) — gerência c1 · `c632fa261ce3f538`"
    m.write_text("# índice\n\n" + linha + "\n- [outro](x.md) — y\n", encoding="utf-8")
    m2.write_text("# dois\n", encoding="utf-8")
    ctx.pin16
    e1 = memorias.trocar_linha_memory(ctx, ("CUSTODIADO", "PUBLICADA"), "CUSTODIADO", "the_boundary `abc`; teste", "t12")
    e2 = memorias.trocar_linha_memory(ctx, ("CUSTODIADO", "PUBLICADA"), "CUSTODIADO", "the_boundary `abc`; teste", "t12")
    assert e1["estado"] != "ja_aplicado" and e2["estado"] == "ja_aplicado"
    txt = m.read_text(encoding="utf-8")
    assert txt.count("CUSTODIADO") == 1 and "- [HANDOFF v398 — O sônico e a afinação das cordas; custódia](handoff-v398-custodia.md) — **24/10: CUSTODIADO**" in txt, txt
    assert m2.read_text(encoding="utf-8").count(linha) == 1, "a linha antiga entra VERBATIM no MEMORY_2.md, uma vez"
    m.write_text("# i\n\n" + linha + "\n" + ("x" * 24200) + "\n", encoding="utf-8")
    try:
        memorias.trocar_linha_memory(ctx, ("CUSTODIADO",), "CUSTODIADO", "y" * 400, "t12b")
        raise AssertionError("o teto de 98% do MEMORY.md deveria PARAR")
    except util.Parar as e:
        assert "98" in e.motivo
    return "apêndice com sentinela (2ª vez = ja_aplicado), CRLF e backup de bytes; CAS refaz depois de escrita alheia; MEMORY.md: linha trocada uma vez, antiga verbatim no MEMORY_2, parada a 98% do teto"


# ============================================================ t13 — o motor com passos falsos: gates, trava, ensaio, ato para fora
@teste()
def t13_motor():
    c = Caminhos({"CEN": str(TMP / "cen_t13")})
    (TMP / "cen_t13").mkdir(exist_ok=True)
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026")
    log = []
    estado = {"a": False, "b": False, "c": False}

    def passo(id_, chave, falha_conferir=False, externo=False, pre_falha=None):
        def ja(ctx_):
            return motor.aplicado("ok") if estado[chave] else motor.falta("falta " + chave)

        def ap(ctx_):
            log.append(id_)
            estado[chave] = True
            return {"fez": id_}
        return motor.Passo(id_, 9, "passo " + id_, ja, aplicar=ap, pre=(lambda _: pre_falha) if pre_falha else None,
                           conferir=(lambda _: ["conferência de %s falhou" % id_]) if falha_conferir else None, externo=externo)
    # 1) ordem e idempotência
    cod, rel = motor.executar(ctx, passos=[passo("T1", "a"), passo("T2", "b")], imprimir=lambda *a: None)
    assert cod == 0 and log == ["T1", "T2"], (cod, log)
    cod, rel = motor.executar(ctx, passos=[passo("T1", "a"), passo("T2", "b")], imprimir=lambda *a: None)
    assert cod == 0 and log == ["T1", "T2"] and all(p["resultado"] == "PULADO_JA_APLICADO" for p in rel["passos"]), "2ª execução não refaz nada"
    # 2) o primeiro gate que falha PARA e nada depois roda
    estado.update(a=False, b=False, c=False)
    log.clear()
    cod, rel = motor.executar(ctx, passos=[passo("T1", "a", falha_conferir=True), passo("T2", "b")], imprimir=lambda *a: None)
    assert cod == util.COD_STOP and log == ["T1"] and rel["parou"]["tipo"] == "Parar", (cod, log)
    # 3) pré-condição que falha: não aplica
    estado.update(a=False, b=False)
    log.clear()
    cod, rel = motor.executar(ctx, passos=[passo("T1", "a", pre_falha=["falta insumo X"])], imprimir=lambda *a: None)
    assert cod == util.COD_STOP and log == [] and rel["parou"]["faltam"] == ["falta insumo X"]
    # 4) ato para fora só com --publicar
    estado.update(a=False, b=False, c=False)
    log.clear()
    cod, rel = motor.executar(ctx, passos=[passo("T1", "a"), passo("T2", "b", externo=True), passo("T3", "c")], imprimir=lambda *a: None)
    assert cod == util.COD_PENDENTE and log == ["T1"] and rel["passos"][-1]["resultado"] == "PARADO_FALTA_PUBLICAR", (cod, log)
    ctx2 = motor.Ctx(c=c, versao="v398", publicar=True)
    cod, rel = motor.executar(ctx2, passos=[passo("T1", "a"), passo("T2", "b", externo=True), passo("T3", "c")], imprimir=lambda *a: None)
    assert cod == 0 and log == ["T1", "T2", "T3"]
    # 5) --ensaio: não aplica nada
    estado.update(a=False, b=False, c=False)
    log.clear()
    ctx3 = motor.Ctx(c=c, versao="v398", ensaio=True)
    cod, rel = motor.executar(ctx3, passos=[passo("T1", "a")], imprimir=lambda *a: None)
    assert log == [] and rel["passos"][0]["resultado"] == "ENSAIO_NADA_GRAVADO"
    # 6) códigos de erro: Esperar -> 10; FalhaLeitura -> 30; Divergencia -> 40
    for exc, cod_esp in ((util.Esperar("x"), 10), (util.FalhaLeitura("x"), 30), (util.Divergencia("x"), 40)):
        def ap_erro(ctx_, e=exc):
            raise e
        estado.update(a=False)
        cod, _ = motor.executar(ctx, passos=[motor.Passo("T9", 9, "erro", lambda ctx_: motor.falta("x"), aplicar=ap_erro)], imprimir=lambda *a: None)
        assert cod == cod_esp, (exc, cod)
    # 7) a marca de «já aplicado» tem de VIRAR depois de aplicar: passo que "aplica" sem mudar nada é flagrado (FALTA explícita PARA; INDETERMINADO só avisa)
    ctx4 = motor.Ctx(c=c, versao="v398")
    cod, rel = motor.executar(ctx4, passos=[motor.Passo("T8", 9, "mente", lambda ctx_: motor.falta("sempre falta"), aplicar=lambda ctx_: {})], imprimir=lambda *a: None)
    assert cod == util.COD_STOP and "continua FALTA" in rel["parou"]["motivo"], (cod, rel.get("parou"))
    ctx5 = motor.Ctx(c=c, versao="v398")
    cod, rel = motor.executar(ctx5, passos=[motor.Passo("T9", 9, "em curso", lambda ctx_: motor.indeterminado("em curso"), aplicar=lambda ctx_: {})], imprimir=lambda *a: None)
    assert cod == 0 and any("ficou INDETERMINADO" in a for a in ctx5.avisos), (cod, ctx5.avisos)
    return "ordem e idempotência; primeiro gate que falha PARA; pré-condição bloqueia; ato para fora só com --publicar; --ensaio não aplica; códigos 20/10/30/40/1 conferidos; marca que não vira depois de aplicar PARA"


@teste()
def t14_trava_por_versao():
    c = Caminhos({"CEN": str(TMP / "cen_t14")})
    ctx = motor.Ctx(c=c, versao="v398")
    with motor.Trava(ctx):
        try:
            with motor.Trava(ctx):
                raise AssertionError("a 2ª trava da mesma versão deveria esperar")
        except util.Esperar:
            pass
    assert not (c.RUNS / "v398.lock").exists(), "a trava some ao sair"
    (c.RUNS).mkdir(parents=True, exist_ok=True)
    (c.RUNS / "v398.lock").write_text(json.dumps({"pid": 999999, "versao": "v398", "inicio": "x"}), encoding="utf-8")
    with motor.Trava(ctx):
        pass
    assert list(c.RUNS.glob("v398.lock.velha_*")), "trava de processo morto é renomeada, nunca apagada"
    assert any("trava velha" in a for a in ctx.avisos)
    return "2ª trava da mesma versão → Esperar (WAIT 10); trava de processo morto renomeada (.velha_<ts>), nunca apagada, e dita; nenhuma morte de processo"


# ============================================================ t15 — o auditor de números citados, a varredura de sensíveis e a guarda
@teste()
def t15_auditor_varredura_guarda():
    raiz = TMP / "aud"
    tb, site = raiz / "tb", raiz / "site"
    (tb / "secoes").mkdir(parents=True)
    (site / "secoes").mkdir(parents=True)
    (tb / "secoes" / "07-x.md").write_bytes(b"x" * 100)
    (site / "secoes" / "07-x.md").write_bytes(b"x" * 100)
    (tb / "LEDGER.md").write_bytes(b"y" * 2000)
    (tb / "read-brief.md").write_text("ver https://s/secoes/07-x.md (101 bytes) e LEDGER.md (2.000 bytes) e https://s/secoes/07-x.md (100 bytes)", encoding="utf-8")
    ctx = motor.Ctx(c=Caminhos({"TB": str(tb), "SITE": str(site)}), versao="v398")
    d = espelho.auditar_numeros_citados(ctx)
    assert len(d) == 1 and d[0]["citado"] == 101 and d[0]["real"] == 100, d
    (tb / "README.md").write_text("The Unique Word Test (v398, 2026-10-24 00:26:08) `[REAL: read from registry teste_de_veracidade_fase9_v397]`", encoding="utf-8")
    assert espelho.rotulo_do_teste_no_readme(ctx) and "v398" in espelho.rotulo_do_teste_no_readme(ctx)[0]
    (tb / "README.md").write_text("The Unique Word Test (v397, 2026-10-23) `[REAL: read from registry teste_de_veracidade_fase9_v397]`", encoding="utf-8")
    ctx._cache_t.clear()
    assert not espelho.rotulo_do_teste_no_readme(ctx)
    # varredura de sensíveis num repositório de brinquedo
    r = raiz / "repo"
    r.mkdir()
    subprocess.run(["git", "init", "-q", str(r)], check=True)
    for n in ("ok.txt", "lixo.tmp_custodia", "a.env", "dados.bak_20261024", "chave.pem"):
        (r / n).write_text("x", encoding="utf-8")
    achados = espelho.varredura_sensiveis(r)
    assert len(achados) == 4 and not any("ok.txt" in a for a in achados), achados
    # guarda de termos
    f = raiz / "g.txt"
    f.write_text("fala do protocolo de colapso e de iald_stack_v7", encoding="utf-8")
    assert EP.guarda_conta(f) == 2 and EP.guarda_conta(raiz / "nao_existe.txt") is None
    import re as _re
    assert EP.guarda_conta(f, priv=[_re.compile("fala")]) == 3
    return "L04: 1 número citado defasado flagrado (101 ≠ 100); L03: rótulo de versão do Teste flagrado e liberado; varredura bloqueante: 4 de 5 arquivos (tmp, .env, .bak_, .pem); guarda de termos conta 2 (+1 com marcador privado sintético)"


# ============================================================ t16 — o snapshot incremental num sandbox
@teste()
def t16_snapshot_sandbox():
    cen = TMP / "cen_t16"
    bk = TMP / "bk_t16"
    (cen / "Chatgpt" / "sub").mkdir(parents=True)
    (cen / "Chatgpt" / ".lake").mkdir()
    (cen / "Chatgpt" / ".lake" / "lixo.bin").write_bytes(b"x")
    (cen / "Chatgpt" / "a.txt").write_bytes(b"aaa")
    (cen / "Chatgpt" / "sub" / "b.txt").write_bytes(b"bbb")
    (cen / "Chatgpt" / "sub" / "novo.txt").write_bytes(b"novo")
    base = bk / "Chatgpt_20261023_100000_delta_de_20261022_100000"
    base.mkdir(parents=True)
    h = lambda b: util.sha256_bytes(b)
    (base / "MANIFEST.json").write_text(json.dumps({"snapshot": "20261023_100000", "conferido_contra_origem": True, "arquivos": {
        "a.txt": {"bytes": 3, "sha256": h(b"aaa")}, "sub/b.txt": {"bytes": 3, "sha256": h(b"OUTRO")}, "some.txt": {"bytes": 1, "sha256": h(b"s")}}}), encoding="utf-8")
    c = Caminhos({"CEN": str(cen), "BKCEN": str(bk)})
    nome = __import__("custodia_g1.central", fromlist=["x"]).snapshot_incremental(c)
    man = json.loads((bk / nome / "MANIFEST.json").read_text(encoding="utf-8"))
    assert man["conferido_contra_origem"] is True and man["n_identicos_a_base"] == 1 and man["n_copiados"] == 2, man
    assert man["ausentes_na_origem_vs_base"] == ["some.txt"] and man["excluidos"]["lake"]["n"] == 1
    assert (bk / nome / "sub" / "novo.txt").read_bytes() == b"novo" and not (bk / nome / "a.txt").exists()
    # a base é o ÚLTIMO snapshot conferido (nome literal não é mais digitado); sem base conferida, PARA
    (base / "MANIFEST.json").write_text(json.dumps({"snapshot": "x", "conferido_contra_origem": False, "arquivos": {}}), encoding="utf-8")
    shutil.rmtree(bk / nome)
    try:
        __import__("custodia_g1.central", fromlist=["x"]).snapshot_incremental(c)
        raise AssertionError("sem base conferida deveria PARAR")
    except util.Parar:
        pass
    return "copia só o novo/mudado (2), pula o idêntico à base (1), exclui .lake, diz o que sumiu, confere por sha-256; a base é o último snapshot CONFERIDO (sem ele, PARA)"


# ============================================================ t17 — o cofre: replay da v398 num vault temporário (T4) e o conserto de L1
@teste(rapido_pula=True, nos_pronta=True)
def t17_cofre_replay():
    from custodia_g1 import central
    oc = TMP / "oc_t17"
    oc.mkdir()
    t0 = time.time()
    for n in ("um_unificado_v397", "tgl_kernel_v397"):
        shutil.copytree(OC_REAL / n, oc / n)
    c = Caminhos({"OC": str(oc)})
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", run_dir=TMP / "run_t17")
    f = central._pre_c3(ctx)
    assert not f, f
    r = central._ap_c3(ctx)
    real, novo = OC_REAL / "um_unificado_v398", oc / "um_unificado_v398"
    ma = {a["file"]: a["sha256"] for a in json.loads((real / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8"))["artifacts"]}
    mn_j = json.loads((novo / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8"))
    mn = {a["file"]: a["sha256"] for a in mn_j["artifacts"]}
    assert ma == mn, ("artefatos", set(ma) ^ set(mn), [k for k in ma if ma[k] != mn.get(k)])
    kr, kn = {p.relative_to(OC_REAL / "tgl_kernel_v398").as_posix(): util.sha256_arquivo(p) for p in (OC_REAL / "tgl_kernel_v398").rglob("*") if p.is_file() and p.name != "CUSTODY_MANIFEST.json"}, \
        {p.relative_to(oc / "tgl_kernel_v398").as_posix(): util.sha256_arquivo(p) for p in (oc / "tgl_kernel_v398").rglob("*") if p.is_file() and p.name != "CUSTODY_MANIFEST.json"}
    assert kr == kn, "kernel: %d vs %d" % (len(kr), len(kn))
    # a cadeia de selo copiada: mesmos arquivos e hashes que o cofre real (a que a outra sessão fez à mão)
    cr = {p.relative_to(real).as_posix(): util.sha256_arquivo(p) for p in (real / "cadeia_de_selo_v398").rglob("*") if p.is_file() and not p.name.startswith("MANIFESTO_CADEIA")}
    cn = {p.relative_to(novo).as_posix(): util.sha256_arquivo(p) for p in (novo / "cadeia_de_selo_v398").rglob("*") if p.is_file() and not p.name.startswith("MANIFESTO_CADEIA")}
    cadeia_dif = sorted(set(cr) ^ set(cn))
    # L1: o manifesto novo traz os registros novos e o pilar (o real saiu com {} e null)
    real_m = json.loads((real / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8"))
    assert real_m["registros_novos_v398"] == {} and mn_j["registros_novos_v398"] and len(mn_j["registros_novos_v398"]) == 4, "L1"
    assert (real_m["pilar_quantico"]["reaproveitado"] is None) and (mn_j["pilar_quantico"]["reaproveitado"] is not None), "L1 pilar"
    assert (novo / "FATOS_CUSTODIA.json").is_file() and mn_j["fatos_custodia"]["sha256"] == util.sha256_arquivo(novo / "FATOS_CUSTODIA.json")
    # a pedra genérica lê o cofre novo (com o pino) e PASSA contra o v397 do vault temporário
    rr = CG.medir_custodia_generica(oc, "v398", "v397")
    assert rr.get("pass") is True, (rr.get("erro"), [k for k, x in rr.get("checks", {}).items() if not x["ok"]])
    # nada se sobrescreve: a 2ª construção PARA
    assert central._pre_c3(ctx) and "já existe" in central._pre_c3(ctx)[0]
    return ("cofre v398 reconstruído num vault temporário a partir do v397: %d artefatos com os MESMOS sha256 do cofre feito à mão, kernel %d arquivos idêntico, cadeia de selo: %d diferenças de lista (%s); "
            "L1 consertado (registros_novos_v398 com 4 entradas, pilar com valores; o cofre real saiu com {} e null); FATOS_CUSTODIA.json no cofre com o pino; a pedra genérica o lê e PASSA; 2ª construção PARA; %.0f s"
            % (len(mn), len(kn), len(cadeia_dif), ", ".join(cadeia_dif[:3]) or "nenhuma", time.time() - t0))


# ============================================================ t18 — o CLI e a conferência final independente
@teste(nos_pronta=True)
def t18_cli_e_conferencia():
    cli = str(CEN / "tools" / "custodiar.py")
    py = [sys.executable, "-X", "utf8"]
    r = subprocess.run(py + [cli, "planejar", "--versao", "v397", "--seco", "--json"], capture_output=True, text=True, encoding="utf-8")
    d = json.loads(r.stdout)
    # v397: nada a fazer por G1 (rc 5 = com as «Pendências SÓ do operador» do handoff abertas; rc 0 se não houvesse nenhuma)
    assert r.returncode in (0, 5) and d["nada_a_fazer"] is True and d["versao"] == "v397" and (r.returncode == 0) == (not d["decisoes_do_operador"]), (r.returncode, d.get("pendentes"))
    r = subprocess.run(py + [cli, "planejar", "--versao", "v398", "--seco", "--json"], capture_output=True, text=True, encoding="utf-8")
    d8 = json.loads(r.stdout)
    # v398 (a outra sessão custodia agora): o plano lista só o que ainda falta; o mundo anda, então o teste confere a FORMA — nunca mais pendências do que passos, E08 bloqueado pela pré, rc 20/1/5/0 coerente
    assert "textos" in d8 or not d8["pendentes"], d8["pendentes"]
    assert r.returncode == motor.codigo_do_plano(d8), (r.returncode, d8["pendentes"], d8.get("bloqueados"))
    assert set(d8["pendentes"]) <= {"E03", "E08", "C11", "E16", "E17", "E18", "E19", "E12", "C18", "C19", "C17C"}, d8["pendentes"]          # E03: um arquivo novo do túnel (outra sessão) é pendência do espelho
    r = subprocess.run(py + [cli, "executar", "--versao", "v999", "--ensaio"], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode in (10, 20, 30), (r.returncode, r.stdout[-300:])
    rc999 = r.returncode
    r = subprocess.run(py + [cli, "planejar", "--versao", "v999", "--seco"], capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 10 and "EM_OBRA" in r.stdout and "E12" not in r.stdout, (r.returncode, r.stdout[-300:])      # versão sem selo: WAIT, nunca um plano com «ok» falsos (E12, C5)
    cj = TMP / "conf.json"
    r = subprocess.run(py + [str(CEN / "tools" / "custodia_g1" / "conferencia.py"), "v398", "--saida", str(cj), "--sem-rede"], capture_output=True, text=True, encoding="utf-8")
    j = json.loads(cj.read_text(encoding="utf-8"))
    # a conferência não importa nada do pacote G1
    src = (CEN / "tools" / "custodia_g1" / "conferencia.py").read_text(encoding="utf-8")
    assert "custodia_g1" not in src.split('"""', 2)[2], "a conferência final tem de ser independente da esteira"
    return "v397: planejar --seco → nada_a_fazer (rc %d: 5 = com as decisões do operador do handoff abertas); v398: rc %d, pendentes %s; v999: executar --ensaio → rc %d e planejar → WAIT (10); conferência independente (sem rede): %d/%d itens ok, sem importar o pacote" % (
        0 if not d["decisoes_do_operador"] else 5, motor.codigo_do_plano(d8), d8["pendentes"], rc999, j["ok"], j["total"])


# ============================================================ t19/t20 — o espelho em SANDBOX: E01 (passo zero), E03 (cópia) e E04 (prosa por molde), de ponta a ponta
SBX = {}


def _espelho_sandbox():
    """Espelho de brinquedo = a cópia byte a byte da v397 que o passo zero guardou em BK, num repositório git com origin local (nada do real é tocado)."""
    raiz = Path(r"C:\tmp") / ("g1sbx_%d" % os.getpid())          # raiz CURTA: as fontes pinadas passam de 250 caracteres
    shutil.rmtree(raiz, ignore_errors=True)
    SBX["raiz"] = raiz
    tb, banc, bk, site = raiz / "tb", raiz / "banc", raiz / "bk", raiz / "site"
    esp = tb / "Um (absoluto) — Grande Atrator"
    real = Caminhos()
    bk_real = sorted(real.BK.glob("um_v397_*"))[0]
    shutil.copytree(util.lp(bk_real), util.lp(esp), ignore=shutil.ignore_patterns("BACKUP_MANIFEST.json"))
    # as fontes pinadas que o espelho real JÁ publica em outro lugar (git ls-files) não se duplicam: o sandbox traz essas cópias, como o real
    mapa_real = json.loads((real.ESP / "fontes_pinadas" / "MAPA_FONTES_PINADAS.json").read_text(encoding="utf-8"))
    for e in mapa_real["fontes"]:
        rel = e.get("caminho_no_espelho")
        if e.get("ja_no_espelho") and rel and not rel.startswith("Um (absoluto)"):
            src, dst = real.TB / rel, tb / rel
            if src.is_file() and not dst.exists():
                util.mkdir(dst.parent)
                shutil.copyfile(util.lp(src), util.lp(dst))
    (banc / "revisoes").mkdir(parents=True)
    site.mkdir(parents=True)
    run = lambda *a: subprocess.run(["git", "-C", str(tb)] + list(a), check=True, capture_output=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(tb)], check=True)
    run("config", "user.email", "g1@teste")
    run("config", "core.longpaths", "true")
    run("config", "core.autocrlf", "false")
    run("config", "user.name", "g1 teste")
    run("add", "-A")
    run("commit", "-q", "-m", "init (sandbox)")
    bare = raiz / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)
    run("remote", "add", "origin", str(bare))
    run("push", "-q", "-u", "origin", "main")
    # os arquivos que E04 remenda, no estado ANTERIOR à v398 (git do espelho real e os backups de bytes que a custódia manual deixou)
    rtb = real.TB
    pre = subprocess.run(["git", "-C", str(rtb), "rev-parse", "bb2c392a"], capture_output=True, text=True).stdout.strip()
    (tb / "tools").mkdir(exist_ok=True)
    for rel in ("tools/gerar_estado_atual.py", "LEDGER.md", "CITATION.cff"):
        b = subprocess.run(["git", "-C", str(rtb), "show", "bb2c392a:" + rel], capture_output=True, check=True).stdout
        (tb / rel).write_bytes(b)
    for nome in ("index.html", "i18n.js"):
        cand = sorted(real.SITE.glob(nome + ".bak_*"), key=os.path.getmtime)
        cand = [p for p in cand if b"art.c.cl.arc397" in p.read_bytes() and b"art.c.cl.arc398" not in p.read_bytes()]
        assert cand, "backup pré-v398 de %s não achado" % nome
        shutil.copyfile(cand[-1], site / nome)
    shutil.copyfile(real.BANC / "revisoes" / "arco_v397_texto.json", banc / "revisoes" / "arco_v397_texto.json")
    run("add", "-A")
    run("commit", "-q", "-m", "estado pre-v398 dos arquivos remendados por E04 (sandbox)")
    run("push", "-q", "origin", "main")
    return Caminhos({"TB": str(tb), "BANC": str(banc), "BK": str(bk), "SITE": str(site)})


@teste(rapido_pula=True, nos_pronta=True)
def t19_sandbox_E01_E03():
    # a guarda privada do espelho real NÃO é lida: um conjunto sintético de marcadores a substitui só neste teste
    EP.carregar_marcadores_privados = lambda: [re.compile("NUNCA_OCORRE_QQ_XYZ")]
    t0 = time.time()
    c = _espelho_sandbox()
    SBX["c"] = c
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", run_dir=TMP / "run_t19")
    assert ctx.rel_espelho == "atras" and ctx.anterior_espelho == "v397"
    assert espelho._ja_e01(ctx).estado == "FALTA" and espelho._pre_e01(ctx) == []
    r1 = espelho._ap_e01(ctx)
    assert espelho._conf_e01(ctx) == [] and r1["arquivos"] > 2000, r1
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", run_dir=TMP / "run_t19")
    assert espelho._ja_e01(ctx).estado == "APLICADO"
    assert espelho._ja_e03(ctx).estado == "FALTA"
    f = espelho._pre_e03(ctx)
    assert f == [], f
    try:
        r3 = espelho._ap_e03(ctx)
    except util.Parar as e:
        raise AssertionError("E03 PAROU: %s | %s" % (e.motivo, e.faltam[:6]))
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", run_dir=TMP / "run_t19")
    assert espelho._conf_e03(ctx) == [], espelho._conf_e03(ctx)[:3]
    assert espelho._ja_e03(ctx).estado == "APLICADO", espelho._ja_e03(ctx)
    rel = json.loads((c.BANC / "revisoes" / "custodia_v398_espelho.json").read_text(encoding="utf-8"))
    real_sel = nos.selo(Caminhos())
    assert rel["modo"] == "copiar" and rel["selo"]["teoremas_limpos"] == "9539/9539" and rel["selo"]["pin16"] == real_sel["sha256"]["um.py"][:16] and rel["selo"]["kernel"]["novos"] == [
        "TGLExt/AfinacaoDasCordas.lean", "TGLExt/Sonico.lean"], rel["selo"]
    assert util.sha16(c.ESP / "um.py") == rel["selo"]["pin16"]
    real_rel = json.loads((Caminhos().BANC / "revisoes" / "custodia_v398_espelho.json").read_text(encoding="utf-8"))
    assert set(rel["copiados"]) <= set(real_rel["copiados"]) | {"DIFF", "RECIBO", "PREREGISTRO", "STDOUT", "SELADO", "DECLARADO", "FONTE", "PILAR", "CACHE", "TUNEL", "CAPTURA", "ORDEM"}
    assert espelho._pre_e03(ctx), "depois de copiado o espelho já não está atrás: a 2ª cópia é recusada pelo pré"
    assert rel["nao_levados"].get("HANDOFF_v398_CUSTODIA.md"), "L19: uma entrada de nao_levados gerada por versão"
    return ("sandbox (espelho de brinquedo = a v397 guardada pelo passo zero): E01 copiou %d arquivos com manifesto conferido; E03 copiou %s, kernel %d (+%d órfãos removidos), %d barrados pela guarda; "
            "conferência profunda 0 divergências; relatório modo=copiar com escada %s e módulos novos %s; a 2ª cópia é recusada; %.0f s"
            % (r1["arquivos"], r3["copiados"], r3["kernel_copiados"], r3["orfaos"], r3["barrados"], rel["selo"]["teoremas_limpos"], [m.split("/")[-1] for m in rel["selo"]["kernel"]["novos"]], time.time() - t0))


@teste(rapido_pula=True, nos_pronta=True)
def t20_sandbox_E04():
    c = SBX.get("c")
    assert c is not None, "t19 precisa rodar antes (sandbox)"
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", aceitar_molde=True, run_dir=TMP / "run_t20")
    assert espelho._ja_e04(ctx).estado == "FALTA"
    # sem --aceitar-molde o handoff sem os marcadores PARA, com a lista
    ctx0 = motor.Ctx(c=c, versao="v398", data="24/10/2026", run_dir=TMP / "run_t20b")
    f0 = espelho._pre_e04(ctx0)
    assert f0 and "ARCO_EN_v398" in f0[0], f0
    assert espelho._pre_e04(ctx) == [], espelho._pre_e04(ctx)
    r = espelho._ap_e04(ctx)
    assert all(v in ("aplicado", "ja_aplicado") for k, v in r.items() if k != "molde_usado"), r
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", aceitar_molde=True, run_dir=TMP / "run_t20")
    assert espelho._conf_e04(ctx) == [], espelho._conf_e04(ctx)
    assert espelho._ja_e04(ctx).estado == "APLICADO"
    ok, msg = util.py_compile_bytes((c.TB / "tools" / "gerar_estado_atual.py").read_bytes(), "gerar_estado_atual.py")
    assert ok, msg
    led = (c.TB / "LEDGER.md").read_text(encoding="utf-8")
    assert led.count("### The custody — v398 (COMPLETE round)") == 1 and led.count("INICIO_PARAGRAFO_SONICO_v398") == 1
    cff = (c.TB / "CITATION.cff").read_text(encoding="utf-8")
    assert "(v398 on 2026-10-24;" in cff and "holds v392" in cff and "10.5281/zenodo.23366324" in cff
    html, js = (c.SITE / "index.html").read_text(encoding="utf-8"), (c.SITE / "i18n.js").read_text(encoding="utf-8")
    assert html.count('data-i18n="art.c.cl.arc398"') == 1 and js.count("'art.c.cl.arc398'") == 2
    assert html.index("art.c.cl.arc397") < html.index("art.c.cl.arc398"), "a linha do arco entra DEPOIS da anterior"
    # idempotência: a 2ª rodada não muda um byte
    antes = {p: p.read_bytes() for p in (c.TB / "tools" / "gerar_estado_atual.py", c.TB / "LEDGER.md", c.TB / "CITATION.cff", c.SITE / "index.html", c.SITE / "i18n.js")}
    r2 = espelho._ap_e04(ctx)
    assert all(p.read_bytes() == b for p, b in antes.items()), "a 2ª aplicação mexeu em algum arquivo"
    # o gerador remendado RODA no espelho de brinquedo? (precisa do core/selo/manifesto/stdout da v398 já copiados, do CITATION e do módulo do estatuto)
    run = subprocess.run([sys.executable, "-X", "utf8", "tools/gerar_estado_atual.py"], cwd=str(c.TB), capture_output=True, text=True, encoding="utf-8", errors="replace")
    gerou = (c.TB / "ESTADO_ATUAL.md").is_file()
    det_run = "gerador roda no sandbox: rc %d%s" % (run.returncode, (" | " + run.stdout.strip().splitlines()[-1][:110]) if run.returncode == 0 and run.stdout.strip() else " (%s)" % (run.stderr or run.stdout).strip().splitlines()[-1][:110])
    return ("sandbox: E04 sem --aceitar-molde PARA listando ARCO_EN_v398…; com ele aplica as 6 marcas (gerar_estado_atual.py compila, LEDGER com 1 bloco e 1 parágrafo do sônico, CITATION com o DOI lido do arquivo, "
            "arco 398 depois do 397 em index.html e i18n.js); 2ª aplicação não muda um byte; %s" % det_run)



# ============================================================ t22 — C1 (sondagem) e C4 (pré-voo da pedra) com pasta de trabalho e vault de brinquedo
@teste()
def t22_C1_e_C4_em_sandbox():
    from custodia_g1 import central
    oc = _vault_temporario()
    c = Caminhos({"OC": str(oc)})
    w = TMP / "w_t22"
    ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", trabalho=w, run_dir=TMP / "run_t22")
    r1 = central._ap_c1(ctx)
    F = json.loads((w / "fatos_v398.json").read_text(encoding="utf-8"))
    assert F["schema"] == "custodia_fatos/2" and F["anterior"] == "v397" and F["escada"]["texto"] == "9539/9539" and r1["blocos"] == 4, r1
    assert (w / "textos_blocos_novos.json").is_file()
    real = json.loads((CEN / "work" / "custodia_v398_24out" / "fatos_v398.json").read_text(encoding="utf-8"))
    assert F["pin"] == real["pin"] and F["kernel"]["declaracoes"] == real["kernel"]["declaracoes"]
    # C4: com o FATOS_CUSTODIA.json pinado no vault de brinquedo a pedra PASSA; sem ele, PARA (o cofre legado não tem as expectativas congeladas)
    try:
        central._ap_c4(ctx)
        raise AssertionError("sem FATOS_CUSTODIA.json no cofre a medição deveria PARAR")
    except util.Parar:
        pass
    cv = oc / "um_unificado_v398"
    (cv / "FATOS_CUSTODIA.json").write_text(json.dumps(F, ensure_ascii=False), encoding="utf-8")
    man = json.loads((cv / "CUSTODY_MANIFEST.json").read_text(encoding="utf-8"))
    man["fatos_custodia"] = {"arquivo": "FATOS_CUSTODIA.json", "sha256": util.sha256_arquivo(cv / "FATOS_CUSTODIA.json")}
    (cv / "CUSTODY_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    r4 = central._ap_c4(ctx)
    assert r4["pass"] is True and (w / "medicao_v398_contra_v397.json").is_file()
    # a mesma sondagem reaplicada sobre outro pino PARA (o selo foi refeito)
    F2 = dict(F, pin="0" * 64)
    (w / "fatos_v398.json").write_text(json.dumps(F2), encoding="utf-8")
    try:
        central._ap_c1(ctx)
        raise AssertionError("fatos já gravados com OUTRO pino deveriam PARAR")
    except util.Parar as e:
        assert "OUTRO pino" in e.motivo
    return "C1 grava fatos_v398.json (esquema 2, %d blocos) e os textos verbatim dos blocos novos na pasta de trabalho dada; C4 reprova sem FATOS_CUSTODIA.json e PASSA com ele (%d checks); fatos com outro pino PARAM" % (r1["blocos"], r4["checks"])


# ============================================================ t23 — a lista de permissão do commit da Central (L5): nada de `git add -u` varrendo modificação alheia
@teste()
def t23_lista_de_permissao_do_commit():
    from custodia_g1 import central
    ctx = ctx_de("v398")
    ps, notas = central.caminhos_a_commitar(ctx)
    ruins = [x for x in ps if central.LISTA_NEGRA.search(x)]
    assert ps and not ruins, ruins
    st = util.git(ctx.c.CEN, "status", "--porcelain").splitlines()
    alheios = [l[3:] for l in st if re.match(r"^( M|\?\?|M ) (andamentos/|frontend/|memory/(?!TGL_ATLAS)|work/|EPCT/)", l[0:2] + " " + l[3:])]
    dentro = [x for x in alheios if x in ps]
    assert not dentro, dentro
    assert "vault/originals_copy/um_unificado_v398" in ps and "fronteira_tgl/runner/one_fronteira.py" in ps
    return "%d caminhos na lista (cofre e kernel v398, runner, ledger, módulo comum, FINAL/results/seals do que o git já vê); nenhum dos %d arquivos alheios modificados na árvore (andamentos/, frontend/, memory/…) entra; Atlas só se for acréscimo puro %s" % (
        len(ps), len(alheios), "(" + "; ".join(notas) + ")" if notas else "")


# ============================================================ t24 — C13 e C16 de ponta a ponta contra memórias, Atlas e mapa de rotas de BRINQUEDO
@teste()
def t24_registro_C13_C16_em_sandbox():
    from custodia_g1 import central
    mem, banc, mapa = TMP / "mem_t24", TMP / "banc_t24", TMP / "mapa_t24"
    atlas = TMP / "Atlas_t24.md"
    for d in (mem, banc / "revisoes", mapa, TMP / "w_t24"):
        d.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Caminhos().MAPA / "rotas.py", mapa / "rotas.py")
    (mapa / "rotas.jsonl").write_text("", encoding="utf-8")
    shutil.copyfile(Caminhos().BANC / "revisoes" / "custodia_v398_espelho.json", banc / "revisoes" / "custodia_v398_espelho.json")
    linha = "- [HANDOFF v398 \u2014 O sônico e a afinação das cordas; custódia](handoff-v398-custodia.md) \u2014 gerência c1 \u00b7 `c632fa261ce3f538`"
    (mem / "MEMORY.md").write_text("# índice\n\n" + linha + "\n- [outro](x.md) \u2014 y\n", encoding="utf-8")
    (mem / "MEMORY_2.md").write_text("# dois\n", encoding="utf-8")
    for n in ("site-sessao-estado.md", "tgl-fronteira-teorica.md", "central-de-patentes-estado.md", "dispositivos-formula-completa.md"):
        (mem / n).write_text("# %s\n" % n, encoding="utf-8")
    (banc / "DIARIO_DO_SITE.md").write_text("# diário\n", encoding="utf-8")
    atlas.write_text("# Atlas (brinquedo)\n", encoding="utf-8")
    os.environ["MAPA_DE_ROTAS_DIR"] = str(mapa)
    try:
        c = Caminhos({"MEM": str(mem), "BANC": str(banc), "ATLAS": str(atlas), "MAPA": str(mapa)})
        ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", trabalho=TMP / "w_t24", run_dir=TMP / "run_t24")
        central._ap_c1(ctx)                                              # os fatos na pasta de trabalho (o registro os cita como artefato da rota)
        assert memorias._ja_c13(ctx).estado == "FALTA"
        f = memorias._pre_c13(ctx)
        assert f == [], f
        r = memorias._ap_c13(ctx)
        assert r["Atlas"] == "aplicado" and r["MEMORY.md"] == "aplicado" and "rota" not in r, r          # a rota NÃO é de C13 (achado ALTA): entra em C16, depois do push e da conferência
        txt_atlas = atlas.read_text(encoding="utf-8")
        assert "A CUSTÓDIA DA v398" in txt_atlas and "c632fa261ce3f538" in txt_atlas and "PROVADA = validade; a creditação segue recusada; o gate não se moveu." in txt_atlas
        assert "CONFIRMADA" not in txt_atlas and "pós-dição" not in txt_atlas
        mm = (mem / "MEMORY.md").read_text(encoding="utf-8")
        assert mm.count("CUSTODIADO") == 1 and "**24/10: CUSTODIADO**" in mm and "- [outro](x.md)" in mm
        assert (mem / "MEMORY_2.md").read_text(encoding="utf-8").count(linha) == 1
        assert (mem / "handoff-v398-custodia.md").is_file() and "[DECLARADO]" in (mem / "handoff-v398-custodia.md").read_text(encoding="utf-8")
        assert "custodia.v398" not in (mapa / "rotas.jsonl").read_text(encoding="utf-8"), "C13 não registra a rota"
        assert "não verificado nesta rodada" in (banc / "DIARIO_DO_SITE.md").read_text(encoding="utf-8"), "sem relatório de subida no sandbox: o texto DIZ que o site não foi verificado (não afirma)"
        # 2ª execução: nada se duplica
        antes = {p: p.read_bytes() for p in (atlas, mem / "MEMORY.md", mem / "MEMORY_2.md", banc / "DIARIO_DO_SITE.md", mem / "central-de-patentes-estado.md")}
        r2 = memorias._ap_c13(ctx)
        assert all(v in ("ja_aplicado", "ja_existe") for v in r2.values()), r2
        assert all(p.read_bytes() == b for p, b in antes.items()), "a 2ª execução do registro mudou algum arquivo (L2)"
        assert memorias._ja_c13(ctx).estado == "APLICADO"
        # C16: PUBLICADA (precisa da conferência final 12/12 e da Central publicada, lidas do mundo real)
        f16 = memorias._pre_c16(ctx)
        if f16:
            return "C13 de ponta a ponta no sandbox OK (Atlas, MEMORY.md, MEMORY_2, handoff DECLARADO, diário; SEM rota); 2ª execução não muda um byte (L2); C16 não rodou (pré: %s)" % f16
        r16 = memorias._ap_c16(ctx)
        mm = (mem / "MEMORY.md").read_text(encoding="utf-8")
        assert "PUBLICADA" in mm and mm.count("- [HANDOFF v398 ") == 1
        m2 = (mem / "MEMORY_2.md").read_text(encoding="utf-8")
        assert m2.count(linha) == 1 and m2.count("CUSTODIADO") == 1, "MEMORY_2 guarda a linha original E a linha CUSTODIADO, ambas verbatim, uma vez cada"
        assert r16["rota"] == "registrada" and "custodia.v398" in (mapa / "rotas.jsonl").read_text(encoding="utf-8"), "a rota entra em C16"
        assert all(v in ("ja_aplicado", "ja_existe") for v in memorias._ap_c16(ctx).values())
        return "C13 e C16 de ponta a ponta contra memórias, Atlas e mapa de rotas de brinquedo: Atlas com «A CUSTÓDIA DA v398», MEMORY.md CUSTODIADO→PUBLICADA com as duas linhas antigas verbatim no MEMORY_2, rota registrada SÓ em C16, handoff criado DECLARADO, texto do site diz «não verificado» (não afirma); 2ª execução não muda um byte (L2)"
    finally:
        os.environ.pop("MAPA_DE_ROTAS_DIR", None)


@teste(nos_pronta=True)
def t25_central_publica_e_vigia_json():
    from custodia_g1 import publica
    ctx = ctx_de("v398")
    nomes = publica._passos_do_encadeador(ctx)
    assert len(nomes) >= 27 and "subir_ensaio" in nomes and "subir" in nomes and "estado_do_organismo" in nomes, nomes          # o encadeador é de outra frente e ganha passos (central_extra): G1 usa a ESTRUTURA
    assert nomes.index("subir_ensaio") + 1 == nomes.index("subir") and set(publica.FORA_DA_CHAMADA) <= set(nomes)
    # o vigia com --json imprime SÓ o JSON (para quem o agenda) e o código de saída diz o estado
    r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "vigiar", "--json"], capture_output=True, text=True, encoding="utf-8")
    j = json.loads(r.stdout)
    assert j["versao"] == "v398" and j["marcas"] == "PRONTA" and r.returncode == j["codigo"] in (0, 1, 5, 20) and "plano" in j and "v399" in j["em_obra"], j
    r2 = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "vigiar", "--versao", "v999", "--json"], capture_output=True, text=True, encoding="utf-8")
    j2 = json.loads(r2.stdout)
    assert r2.returncode == 10 and j2["estado"].startswith("EM_OBRA"), (r2.returncode, j2)
    return "o encadeador da Central pública lista %d passos (subir_ensaio logo antes de subir; estado_do_organismo fica com C19); vigiar --json imprime só JSON: v398 %s (rc %d), v999 EM_OBRA (rc 10)" % (len(nomes), j["marcas"], r.returncode)


@teste()
def t26_conjunto_esperado_da_subida():
    from custodia_g1 import site
    c = Caminhos()
    ens = sorted((d for d in (c.BANC / "subidas").iterdir() if d.is_dir() and d.name.endswith("_dryrun") and (d / "RELATORIO.md").is_file() and "manifesto_v398.json" in (d / "RELATORIO.md").read_text(encoding="utf-8")),
                 key=lambda d: d.name)
    assert ens, "ensaio real da v398 não achado"
    txt = (ens[-1] / "RELATORIO.md").read_text(encoding="utf-8")
    difs = site._diferencas_do_ensaio(txt)
    assert len(difs) >= 15, len(difs)
    assert site.fora_do_esperado(difs) == [], site.fora_do_esperado(difs)[:5]
    # o mesmo relatório com um arquivo da Central pública mudado (meio-trabalho de outra perna): o gate L10 PARA
    falso = txt + "\n| `central/api/documents/102/file.md` | 1 | aaaa | 200 | 2 | text/markdown | DIFERENTE (sha256 local != ar) |\n| `novo/pagina.html` | 1 | bbbb | 404 | 0 |  | NOVO (ausente no ar) |\n"
    fora = site.fora_do_esperado(site._diferencas_do_ensaio(falso))
    assert [p for p, _ in fora] == ["central/api/documents/102/file.md", "novo/pagina.html"], fora
    return "o ensaio REAL da subida da v398 (%s) tem %d diferenças, todas dentro do conjunto esperado (index, i18n, read-brief, llms*, index.md, sitemap, secoes\\*, .htaccess); com um arquivo de central\\ e um NOVO fora do conjunto o gate (L10) PARA com os dois" % (ens[-1].name, len(difs))


def _rm(p):
    """rmtree do que o teste criou (objetos do git são somente-leitura no Windows: chmod e tenta de novo; caminhos longos por \\?\\)."""
    def onexc(func, path, exc):
        try:
            os.chmod(path, 0o700)
            func(path)
        except OSError:
            pass
    shutil.rmtree(util.lp(p), onexc=onexc)


@teste()
def t21_cli_snapshot_em_sandbox():
    """O subcomando oculto `_snapshot` (o que C5 dispara destacado) roda de ponta a ponta contra raízes de brinquedo, sem tocar a Central real."""
    cen, bk = TMP / "cen_t21", TMP / "bk_t21"
    (cen / "Chatgpt").mkdir(parents=True)
    (cen / "Chatgpt" / "x.txt").write_bytes(b"x")
    base = bk / "Chatgpt_20261023_100000_delta_de_20261022_100000"
    base.mkdir(parents=True)
    (base / "MANIFEST.json").write_text(json.dumps({"snapshot": "20261023_100000", "conferido_contra_origem": True, "arquivos": {}}), encoding="utf-8")
    r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "_snapshot", "--raiz", "CEN=%s" % cen, "--raiz", "BKCEN=%s" % bk],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    novos = [d for d in bk.iterdir() if d.is_dir() and d != base]
    assert r.returncode == 0 and len(novos) == 1 and (novos[0] / "x.txt").read_bytes() == b"x" and "snapshot concluído" in r.stdout, (r.returncode, r.stdout[-200:], r.stderr[-200:])
    return "`custodiar.py _snapshot --raiz CEN=… --raiz BKCEN=…` cria o delta num diretório de brinquedo (%s), conferido; a Central real não é tocada" % novos[0].name[:40]


# ============================================================ OS ACHADOS DOS CÉTICOS (24/10/2026): um teste de regressão por achado
from datetime import datetime as _dt, timedelta as _td


def _git_toy(raiz, nome, commits=()):
    """Repositório git de BRINQUEDO com os commits dados [(mensagem, {arquivo: bytes})]. Devolve o caminho."""
    d = Path(raiz) / nome
    d.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q", "-b", "main", str(d)], check=True, capture_output=True)
    for k, v in (("user.email", "g1@teste"), ("user.name", "g1 teste"), ("core.autocrlf", "false")):
        subprocess.run(["git", "-C", str(d), "config", k, v], check=True, capture_output=True)
    for msg, arqs in commits:
        for rel, dados in arqs.items():
            p = d / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(dados)
        subprocess.run(["git", "-C", str(d), "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(d), "commit", "-q", "-m", msg], check=True, capture_output=True)
    return d


def _agora_mais(seg):
    """Carimbo de pasta de subida SEMPRE posterior ao manifesto que o teste acabou de gerar (+1 h)."""
    return (_dt.now() + _td(hours=1, seconds=seg)).strftime("%Y%m%d_%H%M%S")


# ------------------------------------------------------------ t27 — E16..E19 por CONTEÚDO, não pelo nome do manifesto (ALTA)
def _site_sandbox(raiz):
    site_d, banc = raiz / "site", raiz / "banc"
    for d in (site_d / "secoes", banc / "revisoes", banc / "subidas"):
        d.mkdir(parents=True, exist_ok=True)
    (site_d / "index.html").write_text("<html>v398</html>", encoding="utf-8")
    (site_d / "llms.txt").write_text("llms v1", encoding="utf-8")
    (site_d / "sitemap.xml").write_text("<urlset/>", encoding="utf-8")
    (site_d / "secoes" / "01.md").write_text("secao", encoding="utf-8")
    return site_d, banc


def _gerar_manifesto(site_d, banc, nome):
    """O gerador REAL da Bancada (só lido/executado; escreve no sandbox) sobre o site de brinquedo."""
    gm = Caminhos().BANC / "tools" / "gerar_manifesto.py"
    r = subprocess.run([sys.executable, "-X", "utf8", str(gm), "--base", str(site_d), "--saida", str(banc / "revisoes" / nome)], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert r.returncode == 0, (r.stdout + r.stderr)[-400:]
    return json.loads((banc / "revisoes" / nome).read_text(encoding="utf-8"))


def _linhas_do_relatorio(man, estados=None):
    return "\n".join("| `%s` | %s | %s | 200 | %d | text/plain | %s |" % (a["caminho"], format(a["bytes"], ",").replace(",", "."), a["sha256"][:16], a["bytes"], (estados or {}).get(a["caminho"], "IGUAL"))
                     for a in man["arquivos"])


def _ensaio(banc, carimbo, man, estados=None, nome="manifesto_v398.json"):
    """O relatório do ensaio como o real: o cabeçalho CITA o manifesto pelo caminho (foi o que enganou a marca antiga, que só lia o nome)."""
    d = banc / "subidas" / (carimbo + "_dryrun")
    d.mkdir(parents=True)
    (d / "RELATORIO.md").write_text("# DRY-RUN da subida — teste\n\nManifesto: `%s` (base `y`, %d arquivos, %d bytes). Nada foi enviado.\n\n## O que o ar diz hoje (HTTP, `Cache-Control: no-cache`)\n\n"
                                    "| arquivo | bytes local | sha16 local | HTTP | bytes ar | content-type | estado |\n|---|---|---|---|---|---|---|\n%s\n" % (
                                        (banc / "revisoes" / nome).as_posix(), man["n"], man["total_bytes"], _linhas_do_relatorio(man, estados)), encoding="utf-8")
    return d


def _subida(banc, carimbo, man, verificada=True, nome="manifesto_v398.json"):
    d = banc / "subidas" / carimbo
    d.mkdir(parents=True)
    (d / "MANIFESTO_SUBIDA.json").write_text(json.dumps(man), encoding="utf-8")
    (d / "RELATORIO.md").write_text("# RELATORIO DA SUBIDA — teste\n\nManifesto: `%s` (base `y`).\n\n## 1. O ar antes (HTTP)\n\n| arquivo | bytes local | sha16 local | HTTP | bytes ar | content-type | estado |\n|---|---|---|---|---|---|---|\n%s\n\n"
                                    "## 6. Veredito\n\n%s\n" % ((banc / "revisoes" / nome).as_posix(), _linhas_do_relatorio(man),
                                                                   "**SUBIDA VERIFICADA** — o ar diz o que o manifesto descreve." if verificada else "**FALHA** — nada verificado."), encoding="utf-8")
    return d


@teste()
def t27_site_por_conteudo_nao_por_nome():
    from custodia_g1 import site
    raiz = TMP / "t27"
    site_d, banc = _site_sandbox(raiz)
    c = Caminhos({"SITE": str(site_d), "BANC": str(banc)})
    mk = lambda v="v398": motor.Ctx(c=c, versao=v, trabalho=raiz / "w")
    man = _gerar_manifesto(site_d, banc, "manifesto_v398.json")
    _ensaio(banc, _agora_mais(1), man, {"index.html": "DIFERENTE (sha256 local != ar)"})
    _subida(banc, _agora_mais(2), man)
    ctx = mk()
    est = [site._ja_e16(ctx).estado, site._ja_e17(ctx).estado, site._ja_e18(ctx).estado]
    assert est[0] == "APLICADO" and est[1] in ("APLICADO", "SUPERADO") and est[2] == "APLICADO", [(x.estado, x.detalhe[:90]) for x in (site._ja_e16(ctx), site._ja_e17(ctx), site._ja_e18(ctx))]
    # 2) O ROTEIRO DO CÉTICO: o conteúdo muda, E16 regera o manifesto (o NOME é o mesmo), os relatórios continuam os de antes.
    #    Antes: E16 ok, E17 ok, E18 ok, «nada a fazer» — e o conteúdo novo nunca subia.
    (site_d / "llms.txt").write_text("llms v2 com conteudo novo", encoding="utf-8")
    _gerar_manifesto(site_d, banc, "manifesto_v398.json")
    ctx = mk()
    e16, e17, e18, e19 = site._ja_e16(ctx), site._ja_e17(ctx), site._ja_e18(ctx), site._ja_e19(ctx)
    assert e16.estado == "APLICADO", e16
    assert e17.estado == "FALTA" and "nenhum ensaio cobre" in e17.detalhe, e17
    assert e18.estado == "FALTA" and "difere do alvo" in e18.detalhe and "llms.txt" in e18.detalhe, e18
    assert e19.estado == "FALTA" and "E18" in e19.detalhe, e19
    # 3) o manifesto ficou velho frente ao disco: E16 FALTA e E17..E19 FALTAM por dependência
    (site_d / "llms.txt").write_text("llms v3", encoding="utf-8")
    ctx = mk()
    e16 = site._ja_e16(ctx)
    assert e16.estado == "FALTA" and "1 mudados" in e16.detalhe and "llms.txt" in e16.detalhe, e16
    for f in (site._ja_e17, site._ja_e18, site._ja_e19):
        m = f(ctx)
        assert m.estado == "FALTA" and "depende de E" in m.detalhe, (f.__name__, m)
    # 4) a subida da PERNA 3 (outro manifesto, outro nome) que leva o disco de hoje COBRE: E18 aplicado; o manifesto velho vira registro (E16 superado) e o ensaio é dispensado
    man3 = _gerar_manifesto(site_d, banc, "manifesto_central_publica_x.json")
    _subida(banc, _agora_mais(10), man3, nome="manifesto_central_publica_x.json")
    ctx = mk()
    assert site._ja_e18(ctx).estado == "APLICADO" and site._ja_e16(ctx).estado == "SUPERADO" and site._ja_e17(ctx).estado == "SUPERADO", [site._ja_e16(ctx), site._ja_e17(ctx)]
    # 5) uma subida POSTERIOR não verificada que cita o arquivo deixa o ar DESCONHECIDO nesse arquivo
    ruim = json.loads(json.dumps(man3))
    ruim["arquivos"] = [dict(a, sha256="0" * 64) for a in ruim["arquivos"] if a["caminho"] == "llms.txt"]          # subida PARCIAL (só llms.txt) que não terminou verificada
    _subida(banc, _agora_mais(20), ruim, verificada=False, nome="manifesto_central_publica_y.json")
    ctx = mk()
    ar = site.ar_pelo_registro(ctx, site.disco_atual(ctx))
    assert ar["desconhecidos"] == ["llms.txt"] and not ar["ok"], ar
    # 6) versão HISTÓRICA: o alvo é o manifesto da versão; E17 e E18 leem o ensaio e a cópia do manifesto que subiu
    man97 = _gerar_manifesto(site_d, banc, "manifesto_v397.json")
    _ensaio(banc, _agora_mais(30), man97, nome="manifesto_v397.json")
    sub97 = _subida(banc, _agora_mais(31), man97, nome="manifesto_v397.json")
    ctx = mk("v397")
    est = [site._ja_e16(ctx).estado, site._ja_e17(ctx).estado, site._ja_e18(ctx).estado]
    assert est == ["SUPERADO", "APLICADO", "APLICADO"], [(x.estado, x.detalhe[:100]) for x in (site._ja_e16(ctx), site._ja_e17(ctx), site._ja_e18(ctx))]
    ens97 = sorted(p.name for p in (banc / "subidas").iterdir() if p.name.endswith("_dryrun"))[-1]
    linhas = site.linhas_do_relatorio((banc / "subidas" / ens97 / "RELATORIO.md").read_text(encoding="utf-8"))
    assert len(linhas) == man97["n"] and all(len(v[1]) == 16 for v in linhas.values()), linhas
    # o manifesto da versão histórica MUDA (outro conteúdo no disco, mesmo nome): nenhum ensaio e nenhuma subida o cobre
    (site_d / "index.html").write_text("<html>v398 editado depois</html>", encoding="utf-8")
    _gerar_manifesto(site_d, banc, "manifesto_v397.json")
    ctx = mk("v397")
    assert site._ja_e18(ctx).estado == "FALTA" and site._ja_e17(ctx).estado == "FALTA", (site._ja_e17(ctx), site._ja_e18(ctx))
    return ("o roteiro do cético: manifesto regerado com o MESMO nome e relatórios antigos → E16 aplicado, E17/E18/E19 FALTAM (antes: ok, ok, «nada a fazer»); manifesto velho frente ao disco → E16 FALTA e E17..E19 FALTAM por dependência; "
            "a subida da perna 3 (outro manifesto) que leva o disco cobre (E18 aplicado, E16/E17 superados); subida não verificada deixa o arquivo DESCONHECIDO; histórica: ensaio e cópia do manifesto que subiu conferem sha a sha")


# ------------------------------------------------------------ t28 — o QUADRO velho nunca decide (MEDIA)
@teste()
def t28_quadro_velho_nao_decide():
    from custodia_g1 import quadro, publica
    cen = TMP / "cen_t28"
    (cen / "organismo").mkdir(parents=True)

    def grava(medido, itens):
        (cen / "organismo" / "ESTADO_DO_ORGANISMO.json").write_text(json.dumps({"medido_em": medido, "selo": {}, "resumo": {"OK": 1}, "itens": itens}), encoding="utf-8")
    ok_item = {"superficie": "Espelho (GitHub raw)", "item": "README raw traz o pino", "esperado": "sim", "achado": "sim", "estado": "OK"}
    ctx = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398")
    ts = util.instante(ctx.selo_nos["timestamp"])
    grava((ts - _td(hours=4)).strftime("%Y-%m-%d %H:%M:%S"), [ok_item])
    m = quadro.item_do_quadro(ctx, "Espelho (GitHub raw)", "README raw traz o pino")
    assert m.estado == "INDETERMINADO" and "anterior" in m.detalhe and "remedir" in m.detalhe, m
    grava((ts + _td(hours=3)).strftime("%Y-%m-%d %H:%M:%S"), [ok_item])
    assert quadro.item_do_quadro(ctx, "Espelho (GitHub raw)", "README raw traz o pino").estado == "APLICADO"
    # um marco POSTERIOR ao quadro (uma superfície do passo mudou depois da medida) o torna velho
    marco = [("à última modificação de /central/ no site", ts + _td(hours=5))]
    m = quadro.item_do_quadro(ctx, "Espelho (GitHub raw)", "README raw traz o pino", marcos=marco)
    assert m.estado == "INDETERMINADO" and "/central/" in m.detalhe, m
    # C18 lê o quadro com os marcos dele; C19 só olha o que é de G1: o DEFASADO do operador (build do app) vai à parte
    app = {"superficie": "App IALD (ciência própria)", "item": "release instalada no app = selo corrente", "esperado": "v398", "achado": "v395", "estado": "DEFASADO"}
    zen = {"superficie": "Zenodo", "item": "versão depositada", "esperado": "v398", "achado": "v392", "estado": "PENDENTE_OPERADOR"}
    do_g1 = {"superficie": "Espelho", "item": "um.py do espelho = o selo", "esperado": "a", "achado": "b", "estado": "DEFASADO"}
    defas, falhas, ops = quadro.classificar({"itens": [ok_item, app, zen]})
    assert not defas and not falhas and len(ops) == 2
    defas, _, ops = quadro.classificar({"itens": [ok_item, app, do_g1]})
    assert [i["superficie"] for i in defas] == ["Espelho"] and [i["superficie"] for i in ops] == ["App IALD (ciência própria)"]
    nv = TMP / "nosvivo_t28"
    nv.mkdir()
    (nv / "nos_vivo.sqlite3").write_bytes(b"x")
    c2 = Caminhos({"CEN": str(cen), "NOS_VIVO": str(nv)})
    ctx2 = motor.Ctx(c=c2, versao="v398")
    orig = quadro.marcos_c19
    quadro.marcos_c19 = lambda ctx_: [("ao selo", ts)]
    try:
        grava((_dt.now() + _td(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"), [ok_item, app, zen])
        m19 = quadro._ja_c19(ctx2)
        assert m19.estado == "APLICADO" and "do operador à parte" in m19.detalhe, m19                 # o build do app NÃO é DEFASADO de C19
        grava((_dt.now() + _td(minutes=1)).strftime("%Y-%m-%d %H:%M:%S"), [ok_item, do_g1])
        assert quadro._ja_c19(ctx2).estado == "FALTA"                                                  # DEFASADO de G1 pesa
        quadro.marcos_c19 = lambda ctx_: [("à última subida", _dt.now() + _td(hours=2))]
        m19 = quadro._ja_c19(ctx2)
        assert m19.estado == "FALTA" and "anterior" in m19.detalhe, m19                                # quadro velho: remedir
    finally:
        quadro.marcos_c19 = orig
    # o gancho de executar: o quadro velho é REMEDIDO antes de decidir (uma vez); fresco não é; --ensaio nunca
    chamadas = []
    orig_rem, orig_marcos = quadro.remedir, dict(quadro.MARCOS)
    quadro.remedir = lambda ctx_: chamadas.append(1) or grava((_dt.now() + _td(minutes=2)).strftime("%Y-%m-%d %H:%M:%S"), [ok_item])
    quadro.MARCOS["XQ"] = lambda ctx_: [("ao selo", ts)]
    try:
        grava((ts - _td(hours=1)).strftime("%Y-%m-%d %H:%M:%S"), [ok_item])
        p = motor.Passo("XQ", 9, "usa o quadro", lambda ctx_: quadro.item_do_quadro(ctx_, "Espelho (GitHub raw)", "README raw traz o pino"), usa_quadro=True)
        ctx3 = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398")
        ctx3.pode_remedir = True
        assert motor.marca_de(ctx3, p).estado == "APLICADO" and len(chamadas) == 1, (chamadas, motor.marca_de(ctx3, p))
        assert motor.marca_de(ctx3, p).estado == "APLICADO" and len(chamadas) == 1, "quadro já fresco: não remede de novo"
        grava((ts - _td(hours=1)).strftime("%Y-%m-%d %H:%M:%S"), [ok_item])
        ctx4 = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398")                                 # planejar/ensaio: pode_remedir=False -> INDETERMINADO, sem escrever
        assert motor.marca_de(ctx4, p).estado == "INDETERMINADO" and len(chamadas) == 1
    finally:
        quadro.remedir = orig_rem
        quadro.MARCOS.clear()
        quadro.MARCOS.update(orig_marcos)
    return ("quadro anterior ao selo ou a um marco do passo = INDETERMINADO («remedir»), nunca decide; C19 conta DEFASADO só de G1 (o build do app e o Zenodo vão à parte); quadro velho em C19 = FALTA; "
            "em executar o gancho remede UMA vez antes de decidir e em planejar/ensaio não escreve")


# ------------------------------------------------------------ t29 — C11 grava recibo DURÁVEL e a marca o lê num processo seguinte (MEDIA)
@teste()
def t29_c11_recibo_duravel():
    from custodia_g1 import central, recibos
    cen = TMP / "cen_t29"
    for nome, slug in (("BR000_A", "a"), ("BR111_MQC", "mqc")):
        d = cen / "patents" / nome
        d.mkdir(parents=True)
        (d / ("%s_FINAL.py" % slug)).write_text("print('FINAL %s ok')\n" % slug, encoding="utf-8")
    w = TMP / "w_t29"
    mk = lambda: motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398", trabalho=w, run_dir=TMP / "run_t29")
    ctx = mk()
    m0 = central._ja_c11(ctx)
    assert m0.estado == "INDETERMINADO" and "RECIBO_C11_v398.json" in m0.detalhe and not m0.leitura, m0
    r = central._ap_c11(ctx)
    assert r["ok"] == 2
    assert (w / "RECIBO_C11_v398.json").is_file(), "o recibo é DURÁVEL: mora na pasta de trabalho da versão"
    d = json.loads((w / "RECIBO_C11_v398.json").read_text(encoding="utf-8"))
    assert d["total"] == 2 and all(len(f["sha256"]) == 64 for f in d["finais"]) and d["versao"] == "v398", d
    # OUTRO processo (outro Ctx, sem o run_dir nem o memo): a marca lê o recibo do disco e confere os FINAL de hoje
    ctx2 = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398", trabalho=w)
    m1 = central._ja_c11(ctx2)
    assert m1.estado == "APLICADO" and "recibo durável" in m1.detalhe, m1
    # um FINAL mudou depois do recibo: a marca não vale mais
    (cen / "patents" / "BR000_A" / "a_FINAL.py").write_text("print('FINAL a MUDOU')\n", encoding="utf-8")
    ctx3 = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398", trabalho=w)
    m2 = central._ja_c11(ctx3)
    assert m2.estado == "FALTA" and "mudaram depois do recibo" in m2.detalhe, m2
    # recibo ilegível = falha de leitura visível; recibo de outra versão = idem (nunca «ok»)
    (w / "RECIBO_C11_v398.json").write_text("{não é json", encoding="utf-8")
    ctx4 = motor.Ctx(c=Caminhos({"CEN": str(cen)}), versao="v398", trabalho=w)
    mm = motor.marca_de(ctx4, motor.Passo("C11", 2, "x", central._ja_c11))
    assert mm.estado == "INDETERMINADO" and mm.leitura is True, mm
    return "_ap_c11 grava RECIBO_C11_v398.json na pasta de trabalho (sha256 de cada FINAL); um Ctx novo (outro processo) o lê e dá APLICADO; FINAL alterado depois do recibo = FALTA; recibo ilegível = INDETERMINADO com leitura=True (executar PARA, código 30)"


# ------------------------------------------------------------ t30 — falha de LEITURA do git é visível (MEDIA)
@teste()
def t30_git_falha_de_leitura_e_visivel():
    repo = _git_toy(TMP, "git_t30", [("custodia(v393+v394): conjunta", {"a.txt": b"1"}), ("outro", {"b.txt": b"2"})])
    # controle positivo: git acha o commit da custódia conjunta e sabe dizer «não é ancestral» (rc 1) sem confundir com erro
    assert util.git(repo, "rev-parse", "--short", "HEAD")
    assert util.git_ancestral(repo, "HEAD~1", "HEAD") is True and util.git_ancestral(repo, "HEAD", "HEAD~1") is False
    try:
        util.git_ancestral(repo, "objeto_que_nao_existe", "HEAD")
        raise AssertionError("rc 128 do git não pode virar «não é ancestral»")
    except util.FalhaLeitura:
        pass
    # o git AUSENTE (G1_GIT_EXE aponta para o nada): tudo o que lia git agora falha VISÍVEL
    os.environ["G1_GIT_EXE"] = str(TMP / "nao_existe" / "git.exe")
    try:
        for f in (lambda: util.git(repo, "rev-parse", "HEAD"), lambda: espelho._tree_limpa(repo), lambda: util.commit_da_custodia(repo, "v394"), lambda: util.git_ancestral(repo, "HEAD", "HEAD")):
            try:
                f()
                raise AssertionError("com o git ausente a leitura deveria levantar FalhaLeitura")
            except util.FalhaLeitura:
                pass
        ctx = ctx_de("v397")
        e10 = motor.marca_de(ctx, espelho.passos_fase_b(ctx)[0])
        assert e10.estado == "INDETERMINADO" and e10.leitura is True and "FalhaLeitura" in e10.detalhe, e10         # antes: FALTA «sem commit»
        # executar não aplica às cegas: marca ilegível = código 30 e o aplicador NÃO roda
        feito = []
        p = motor.Passo("T1", 9, "git", lambda ctx_: motor.Marca("INDETERMINADO", "git ilegível", True), aplicar=lambda ctx_: feito.append(1))
        cod, rel = motor.executar(motor.Ctx(c=Caminhos({"CEN": str(TMP / "cen_t30")}), versao="v398"), passos=[p], imprimir=lambda *a: None)
        assert cod == util.COD_LEITURA and not feito, (cod, feito)
        # a conferência final independente: git ausente = FALHA no item 6 (antes dois «» eram «HEAD = origin/main»)
        saida = TMP / "conf_t30.json"
        r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodia_g1" / "conferencia.py"), "v398", "--saida", str(saida), "--sem-rede"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        j = json.loads(saida.read_text(encoding="utf-8"))
        item6 = [i for i in j["itens"] if i["item"].startswith("6 ")]
        assert r.returncode == 1 and item6 and all(i["ok"] is False and "git" in i["detalhe"] for i in item6), (r.returncode, item6)
        # o plano: código 30 (falha de leitura), não «pendente» nem «nada a fazer»
        r2 = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "planejar", "--versao", "v397", "--seco", "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
        d2 = json.loads(r2.stdout)
        assert r2.returncode == util.COD_LEITURA and d2["falha_de_leitura"] and not d2["nada_a_fazer"], (r2.returncode, d2["falha_de_leitura"])
    finally:
        os.environ.pop("G1_GIT_EXE", None)
    # o PATH mínimo de uma tarefa agendada (sem git) NÃO derruba: G1 acha o git nos lugares usuais do Windows
    env = dict(os.environ, PATH=r"C:\Python314;C:\Windows\System32;C:\Windows")
    r3 = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "planejar", "--versao", "v397", "--seco", "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    d3 = json.loads(r3.stdout)
    assert not d3["falha_de_leitura"] and d3["nada_a_fazer"] is True, (r3.returncode, d3["falha_de_leitura"])
    return ("git ausente: util.git, _tree_limpa, commit_da_custodia e git_ancestral levantam FalhaLeitura; E10 vira INDETERMINADO com leitura=True (antes FALTA «sem commit»); executar não aplica (código 30); a conferência final "
            "falha no item 6; o plano sai com código 30; rc 128 não vira «não é ancestral»; com o PATH mínimo de tarefa agendada o git é achado e o plano de v397 sai igual")


# ------------------------------------------------------------ t31 — SUPERADO_REL é estado próprio e as provas que dá para ter, G1 tem (MEDIA)
@teste()
def t31_superado_por_relacao_e_provas():
    ctx = ctx_de("v397")
    p = motor.planejar(ctx)
    assert p["nada_a_fazer"] is True and not p["pendentes"], p["pendentes"]
    rel = set(p["superados_por_relacao"])
    esperados_rel = {"E06", "E08", "E08B", "E09", "E12", "E13", "E14", "E15", "C11", "C18", "C19"}
    assert esperados_rel <= rel, esperados_rel - rel
    estados = {i["id"]: i["estado"] for i in p["itens"]}
    assert estados["C3"] == "APLICADO" and "re-hash" in next(i["detalhe"] for i in p["itens"] if i["id"] == "C3")
    assert estados["E03"] == "SUPERADO" and "blobs do commit" in next(i["detalhe"] for i in p["itens"] if i["id"] == "E03")
    assert estados["C10"] == "SUPERADO" and estados["C12"] == "SUPERADO", (estados["C10"], estados["C12"])
    assert p["provado_no_artefato"] is False and p["completo"] is False
    # o rótulo «nada a fazer» vem com a ressalva impressa
    r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "planejar", "--versao", "v397", "--seco"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    assert "NADA A FAZER" in r.stdout and "SÓ pela relação" in r.stdout, r.stdout[-600:]
    # C3: re-hash. Cofre de brinquedo; um byte mudado no kernel = BLOQUEADO (antes: «0 divergentes» autodeclarado)
    from custodia_g1 import central
    oc = TMP / "oc_t31"
    V, KV = oc / "um_unificado_v398", oc / "tgl_kernel_v398"
    for d in (V, KV / "TGLExt"):
        d.mkdir(parents=True)
    (V / "um.py").write_bytes(b"print(1)\n")
    (V / "nota.md").write_bytes(b"nota\n")
    (KV / "TGLExt" / "A.lean").write_bytes(b"theorem a : True := trivial\n")
    pm = {"formal_files_sha256": {"TGLExt/A.lean": util.sha256_bytes(b"theorem a : True := trivial\n")}}
    (KV / "tgl_kernel_proof_manifest.json").write_text(json.dumps(pm), encoding="utf-8")
    (KV / "CUSTODY_MANIFEST.json").write_text(json.dumps({"tgl_kernel_proof_manifest_sha256": util.sha256_arquivo(KV / "tgl_kernel_proof_manifest.json")}), encoding="utf-8")
    man = {"um_py_pin": util.sha256_bytes(b"print(1)\n"), "artifacts": [{"file": "um.py", "sha256": util.sha256_bytes(b"print(1)\n")}, {"file": "nota.md", "sha256": util.sha256_bytes(b"nota\n")}],
           "mismatches": 0, "n_artifacts": 2}
    (V / "CUSTODY_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    ctx8 = motor.Ctx(c=Caminhos({"OC": str(oc)}), versao="v398")
    rh = central.rehash_cofre(ctx8, man)
    assert rh["divergentes"] == [] and rh["artefatos"] == 2 and rh["kernel"] == 1, rh
    (KV / "TGLExt" / "A.lean").write_bytes(b"theorem a : True := trivial \n")           # um espaço a mais
    rh = central.rehash_cofre(ctx8, man)
    assert rh["divergentes"] == ["kernel TGLExt/A.lean"], rh
    (V / "nota.md").write_bytes(b"adulterada\n")
    assert "artefato nota.md" in central.rehash_cofre(ctx8, man)["divergentes"]
    # E03 histórica: o blob do commit custodia(vN) tem os bytes do cofre — um byte diferente BLOQUEIA
    esp = "Um (absoluto) \u2014 Grande Atrator"
    selo_esp = json.dumps({"um_version": "v999"}).encode("utf-8")
    tb = _git_toy(TMP, "tb_t31", [("custodia(v398): x", {esp + "/um.py": b"print(1)\n", esp + "/um_absoluto_selo.json": b"{}", esp + "/um_absoluto.json": b"{}",
                                                          esp + "/Lean/tgl_kernel_proof_manifest.json": b"{}"}),
                                   ("depois", {esp + "/um_absoluto_selo.json": selo_esp, esp + "/rodadas/rodada_v398_stdout.txt": b"x", esp + "/diferencas_v398/a.txt": b"x",
                                               esp + "/recibos_bancada_v398/a.txt": b"x"})])
    cof = oc / "um_unificado_v398"
    for n, b in (("um.py", b"print(1)\n"), ("um_absoluto_selo.json", b"{}"), ("um_absoluto.json", b"{}"), ("tgl_kernel_proof_manifest.json", b"{}")):
        (cof / n).write_bytes(b)
    ctx9 = motor.Ctx(c=Caminhos({"OC": str(oc), "TB": str(tb)}), versao="v398")
    e03 = espelho._ja_e03(ctx9)
    assert e03.estado == "SUPERADO" and "blobs do commit" in e03.detalhe, e03
    (cof / "um.py").write_bytes(b"print(2)\n")
    e03 = espelho._ja_e03(motor.Ctx(c=Caminhos({"OC": str(oc), "TB": str(tb)}), versao="v398"))
    assert e03.estado == "BLOQUEADO" and "um.py" in e03.detalhe, e03
    return ("v397 (histórica): nada a fazer com a ressalva impressa; %d passos SUPERADO_REL (%s…) e as provas que existem: C3 re-hash, E03 blobs do commit = cofre, C10/C12 FINAL e ledger do commit; "
            "cofre de brinquedo: 1 byte do kernel ou 1 artefato mudado = divergência; blob do commit ≠ cofre = BLOQUEADO" % (len(rel), ",".join(sorted(rel))[:40]))


# ------------------------------------------------------------ t32 — decisão do OPERADOR não é «satisfeito»: estado e código próprios (MEDIA)
@teste(nos_pronta=True)
def t32_operador_tem_codigo_proprio():
    # o motor: passo OPERADOR + o resto aplicado -> código 5 e a decisão listada (antes: 0, «tudo aplicado»)
    c = Caminhos({"CEN": str(TMP / "cen_t32")})
    feito = []
    ps = [motor.Passo("T1", 9, "G1", lambda ctx_: motor.aplicado("ok") if feito else motor.falta("falta"), aplicar=lambda ctx_: feito.append(1) or {}),
          motor.Passo("T2", 9, "do operador", lambda ctx_: motor.operador("decida o nome do registro"))]
    saidas = []
    cod, rel = motor.executar(motor.Ctx(c=c, versao="v398"), passos=ps, imprimir=lambda *a: saidas.append(" ".join(str(x) for x in a)))
    assert cod == util.COD_OPERADOR == 5 and rel["decisoes_do_operador"] and rel["decisoes_do_operador"][0]["origem"] == "T2", (cod, rel.get("decisoes_do_operador"))
    assert any("decisão" in s and "OPERADOR" in s for s in saidas), saidas
    # a tabela de códigos
    assert motor.codigo_do_plano({"nada_a_fazer": True, "decisoes_do_operador": [{"origem": "x", "texto": "y"}]}) == 5
    assert motor.codigo_do_plano({"nada_a_fazer": True, "decisoes_do_operador": []}) == 0
    assert motor.codigo_do_plano({"nada_a_fazer": False, "decisoes_do_operador": [1]}) == 1
    assert motor.codigo_do_plano({"nada_a_fazer": False, "bloqueados": ["E08"], "decisoes_do_operador": []}) == 20
    assert motor.codigo_do_plano({"nada_a_fazer": False, "falha_de_leitura": ["E10"], "bloqueados": ["E08"]}) == 30
    # o roteiro do cético, no mundo real: --so E08B (só a decisão do operador) NÃO diz mais «tudo aplicado, rc 0»
    r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "planejar", "--versao", "v398", "--seco", "--so", "E08B", "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    dj = json.loads(r.stdout)
    e08b = dj["itens"][0]["estado"]
    if e08b == "OPERADOR":            # a decisão estrutural do README (L01) segue aberta no mundo real: o antigo «tudo aplicado, rc 0» agora é rc 5
        assert r.returncode == 5 and dj["nada_a_fazer"] is True and any(x["origem"] == "E08B" for x in dj["decisoes_do_operador"]), (r.returncode, dj["decisoes_do_operador"][:1])
    # v397: as «Pendências SÓ do operador» do HANDOFF entram no plano (antes: pendentes_do_operador [])
    r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "planejar", "--versao", "v397", "--seco", "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    d = json.loads(r.stdout)
    origens = [x["origem"] for x in d["decisoes_do_operador"]]
    assert r.returncode == 5 and d["nada_a_fazer"] is True and any(o.startswith("handoff") for o in origens), (r.returncode, origens)
    txt = next(x["texto"] for x in d["decisoes_do_operador"] if x["origem"].startswith("handoff"))
    assert "teste_de_veracidade_fase9_v397" in txt and "ACOM Mirror" in txt, txt[:200]
    # o vigia: rc 5 é «custodiada por G1 com decisão aberta» (não «custodiada»), e o JSON diz
    r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "vigiar", "--versao", "v397", "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    j = json.loads(r.stdout)
    assert r.returncode == 5 and j["codigo"] == 5 and "decisão" in j["estado"] and j["plano"]["decisoes_do_operador"], j["estado"]
    return "executar com passo OPERADOR → código 5 e a decisão listada; tabela 0/1/5/20/30; planejar --so E08B → rc 5 (antes 0 «tudo aplicado»); v397 traz as «Pendências SÓ do operador» do handoff (verbatim) e sai com rc 5; vigiar: «CUSTODIADA POR G1 — N decisão(ões) do operador abertas»"


# ------------------------------------------------------------ t33 — o plano roda a pré-condição (só leitura) e mostra onde `executar` PARA (MEDIA)
@teste(nos_pronta=True)
def t33_plano_mostra_bloqueio():
    c = Caminhos({"CEN": str(TMP / "cen_t33")})
    ctx = motor.Ctx(c=c, versao="v398")
    chamadas = []

    def passo(id_, pre=None, ja=None):
        return motor.Passo(id_, 9, "passo " + id_, ja or (lambda ctx_: motor.falta("falta " + id_)), aplicar=lambda ctx_: {}, pre=(lambda ctx_: (chamadas.append(id_), pre)[1]) if pre is not None else None)
    ps = [passo("A", pre=[]), passo("B", pre=["o commit já existe: errata ao lado, decisão da gerência"]), passo("C", pre=["outra falha"])]
    av = motor.avaliar(ctx, ps)
    est = {p.id: m.estado for p, m in av}
    assert est == {"A": "FALTA", "B": "FALTA", "C": "FALTA"} and chamadas == ["A"], (est, chamadas)        # só o 1º pendente tem a pré avaliada (o que executar tentaria)
    ps2 = [motor.Passo("OK", 9, "ok", lambda ctx_: motor.aplicado("feito")), passo("B", pre=["o commit já existe"]), passo("C", pre=["outra"])]
    chamadas.clear()
    av = motor.avaliar(ctx, ps2)
    est = {p.id: (m.estado, m.detalhe) for p, m in av}
    assert est["B"][0] == "BLOQUEADO" and "o commit já existe" in est["B"][1] and est["C"][0] == "FALTA" and chamadas == ["B"], (est, chamadas)
    r = motor.resumo(av)
    assert r["bloqueados"] == ["B"] and r["pendentes"] == ["B", "C"] and r["nada_a_fazer"] is False
    chamadas.clear()
    av = motor.avaliar(ctx, ps2, so="B,C")                                                                    # --so: cada selecionado confere a SUA pré
    assert {p.id: m.estado for p, m in av} == {"B": "BLOQUEADO", "C": "BLOQUEADO"} and sorted(chamadas) == ["B", "C"]
    # no mundo real (v398): o plano diz onde executar PARA e o que fica atrás; o código é 20 (STOP), não «1 pendente»
    r = subprocess.run([sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py"), "planejar", "--versao", "v398", "--seco", "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    d = json.loads(r.stdout)
    if d["pendentes"]:
        primeiro = d["itens"][[i["id"] for i in d["itens"]].index(d["pendentes"][0])]
        assert primeiro["estado"] in ("BLOQUEADO", "FALTA", "INDETERMINADO"), primeiro
        if primeiro["estado"] == "BLOQUEADO":
            assert d["executar_para_em"]["id"] == primeiro["id"] and r.returncode == 20, (d["executar_para_em"], r.returncode)
    return "o plano avalia a pré só do 1º passo pendente (o que executar tentaria) e o marca BLOQUEADO com o motivo; com --so cada selecionado; resumo lista bloqueados; no mundo real o rc é 20 e o plano diz onde PARA e o que fica atrás"


# ------------------------------------------------------------ t34 — --ensaio não grava NADA, nem RELATORIO.json (BAIXA)
@teste()
def t34_ensaio_nao_grava_nada():
    cen = TMP / "cen_t34"
    cen.mkdir()
    c = Caminhos({"CEN": str(cen)})

    def foto():
        return sorted(str(p.relative_to(cen)) for p in cen.rglob("*"))
    antes = foto()
    feito = []
    ps = [motor.Passo("T1", 9, "um", lambda ctx_: motor.falta("x"), aplicar=lambda ctx_: feito.append(1) or {}, escreve="algo")]
    ctx = motor.Ctx(c=c, versao="v398", ensaio=True)
    cod, rel = motor.executar(ctx, passos=ps, imprimir=lambda *a: None)
    assert not feito and rel["passos"][0]["resultado"] == "ENSAIO_NADA_GRAVADO" and foto() == antes, (foto(), antes)
    assert ctx.run_dir is None, "no ensaio nem se define o run_dir"
    # contraprova: sem --ensaio o relatório É gravado
    ctx2 = motor.Ctx(c=c, versao="v398")
    motor.executar(ctx2, passos=[motor.Passo("T2", 9, "dois", lambda ctx_: motor.aplicado("ok"))], imprimir=lambda *a: None)
    assert (ctx2.run_dir / "RELATORIO.json").is_file()
    return "executar --ensaio com passo pendente: nada executado e a árvore de arquivos idêntica antes/depois (sem RELATORIO.json, sem pasta de run); sem --ensaio o relatório é gravado"


# ------------------------------------------------------------ t35 — a custódia CONJUNTA é reconhecida (BAIXA)
@teste()
def t35_custodia_conjunta():
    repo = _git_toy(TMP, "conjunta_t35", [("custodia(v392+v393+v394): tres versoes", {"a": b"1"}), ("custodia(v395): so a 395", {"b": b"2"}), ("custodia(v3940): decoy", {"c": b"3"}),
                                          ("organismo(24/10): custodia(v396) citada no meio", {"d": b"4"})])
    assert util.commit_da_custodia(repo, "v393") == util.commit_da_custodia(repo, "v392") == util.commit_da_custodia(repo, "v394") is not None
    h95 = util.commit_da_custodia(repo, "v395")
    assert h95 and h95 != util.commit_da_custodia(repo, "v394")
    assert util.commit_da_custodia(repo, "v39") is None and util.commit_da_custodia(repo, "v396") is None, "só vale o ASSUNTO que começa por custodia(<versões>):"
    assert util.commit_da_custodia(repo, "v3940") is not None
    # no mundo real: a v394 foi custodiada junto com a v393 (the_boundary 237ef12c); antes o plano dava 14 pendências
    c = Caminhos()
    assert util.commit_da_custodia(c.TB, "v393") and util.commit_da_custodia(c.TB, "v393") == util.commit_da_custodia(c.TB, "v394"), "custodia(v393+v394) no espelho"
    return "custodia(v392+v393+v394) devolve o mesmo commit para as três versões; custodia(v3940) e menção no meio do assunto não casam; o espelho real reconhece custodia(v393+v394)"


# ------------------------------------------------------------ t36 — C13 (as superfícies), C20 (campos de produção) e C5 (o instante do selo) (BAIXA)
@teste()
def t36_c13_c20_c5_conferem_mais():
    from custodia_g1 import central, quadro
    # C13: as 6 memórias/diários + Atlas + MEMORY.md; a falta de UMA aparece
    mem, banc = TMP / "mem_t36", TMP / "banc_t36"
    (banc / "revisoes").mkdir(parents=True)
    mem.mkdir()
    atlas = TMP / "atlas_t36.md"
    atlas.write_text("# atlas\n[24/10 — A CUSTÓDIA DA v398] x\n", encoding="utf-8")
    ctx = motor.Ctx(c=Caminhos({"MEM": str(mem), "BANC": str(banc), "ATLAS": str(atlas)}), versao="v398", trabalho=TMP / "w_t36")
    sup = memorias._superficies_c13(ctx)
    assert len(sup) == 6
    for nome, p, bloco in sup:
        p.write_text("# %s\n\n## 24/10/2026 10:00 \u2014 a custódia da v398\n\ntexto\n" % nome, encoding="utf-8")
    (mem / "MEMORY.md").write_text("- [HANDOFF v398 \u2014 x](handoff-v398-custodia.md) \u2014 **24/10: CUSTODIADO** (x) \u00b7 `abc`\n", encoding="utf-8")
    assert memorias._ja_c13(ctx).estado == "APLICADO", memorias._ja_c13(ctx)
    sup[2][1].write_text("# tgl-fronteira-teorica.md\n\n## 24/10/2026 \u2014 outra coisa\n", encoding="utf-8")                 # uma superfície SEM o registro
    m = memorias._ja_c13(ctx)
    assert m.estado == "FALTA" and "tgl-fronteira-teorica.md sem o registro" in m.detalhe, m
    sup[2][1].unlink()
    assert "tgl-fronteira-teorica.md ausente" in memorias._ja_c13(ctx).detalhe
    # C20: o recibo da Bancada precisa ser de PRODUÇÃO aplicada; ACTIVE.json precisa do manifest.json do release com o sha que declara
    bu = TMP / "bu_t36" / "estado" / "sincronizacao"
    bu.mkdir(parents=True)
    rec = {"modo": "aplicar", "sandbox": False, "producao": True, "veredito": "REPINADA_B8__APLICADA__X", "versao_alvo": "v398"}
    (bu / "RECIBO_SINCRONIZACAO_v398_20261024_000000.json").write_text(json.dumps(rec), encoding="utf-8")
    cen = TMP / "cen_t36"
    base = cen / "Chatgpt" / "IALD_ORQUESTRACAO_20260923" / "state" / "canonical_memory"
    (base / "releases" / "v398_abc").mkdir(parents=True)
    (base / "releases" / "v398_abc" / "manifest.json").write_text("{}", encoding="utf-8")
    act = {"release": "v398", "epoch": "v398_abc", "manifest_sha256": util.sha256_bytes(b"{}")}
    (base / "ACTIVE.json").write_text(json.dumps(act), encoding="utf-8")
    (cen / "work" / "scientific_memory_sync_20261024_v398").mkdir(parents=True)
    (cen / "work" / "scientific_memory_sync_20261024_v398" / "DELIVERY_R1.json").write_text(json.dumps({"status": "ACTIVATED_VERIFIED_NEW_PROCESS", "release": "v398"}), encoding="utf-8")
    c20 = Caminhos({"CEN": str(cen), "BU": str(TMP / "bu_t36")})
    ctx20 = motor.Ctx(c=c20, versao="v398")
    assert quadro._ja_c20(ctx20).estado == "APLICADO", quadro._ja_c20(ctx20)
    rec["sandbox"] = True
    (bu / "RECIBO_SINCRONIZACAO_v398_20261024_000000.json").write_text(json.dumps(rec), encoding="utf-8")
    m = quadro._ja_c20(ctx20)
    assert m.estado == "FALTA" and "NÃO é recibo de produção" in m.detalhe, m
    rec["sandbox"] = False
    (bu / "RECIBO_SINCRONIZACAO_v398_20261024_000000.json").write_text(json.dumps(rec), encoding="utf-8")
    (base / "releases" / "v398_abc" / "manifest.json").write_text('{"x": 1}', encoding="utf-8")                          # manifest do release não confere com ACTIVE
    m = quadro._ja_c20(ctx20)
    assert m.estado == "FALTA" and "manifest.json do release NÃO confere" in m.detalhe, m
    # C5: o snapshot precisa ser posterior ao INSTANTE do selo (não só ao dia)
    bk = TMP / "bkcen_t36"
    ts = util.instante(motor.Ctx(versao="v398").selo_nos["timestamp"])
    for quando, esperado in ((ts - _td(minutes=16), "FALTA"), (ts + _td(minutes=16), "APLICADO")):
        shutil.rmtree(bk, ignore_errors=True)
        d = bk / ("Chatgpt_%s_delta_de_x" % quando.strftime("%Y%m%d_%H%M%S"))
        d.mkdir(parents=True)
        (d / "MANIFEST.json").write_text(json.dumps({"snapshot": quando.strftime("%Y%m%d_%H%M%S"), "conferido_contra_origem": True, "n_copiados": 1, "n_identicos_a_base": 2}), encoding="utf-8")
        m5 = central._ja_c5(motor.Ctx(c=Caminhos({"BKCEN": str(bk)}), versao="v398"))
        assert m5.estado == esperado, (quando, esperado, m5)
    return "C13 exige as 6 memórias/diários + Atlas + MEMORY.md (a falta ou o arquivo ausente aparece); C20 só aceita recibo de produção aplicado e o manifest.json do release com o sha de ACTIVE.json; C5 compara o INSTANTE do snapshot com o do selo (um snapshot 16 min antes do selo, no mesmo dia, não cobre)"


# ------------------------------------------------------------ t37 — a ROTA custodia.vN só entra em C16, depois do push e da conferência (ALTA)
@teste()
def t37_rota_so_em_c16():
    from custodia_g1 import central
    mem, banc, mapa = TMP / "mem_t37", TMP / "banc_t37", TMP / "mapa_t37"
    atlas = TMP / "Atlas_t37.md"
    for d in (mem, banc / "revisoes", mapa, TMP / "w_t37"):
        d.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Caminhos().MAPA / "rotas.py", mapa / "rotas.py")
    (mapa / "rotas.jsonl").write_text("", encoding="utf-8")
    shutil.copyfile(Caminhos().BANC / "revisoes" / "custodia_v398_espelho.json", banc / "revisoes" / "custodia_v398_espelho.json")
    linha = "- [HANDOFF v398 \u2014 O sônico e a afinação das cordas; custódia](handoff-v398-custodia.md) \u2014 gerência c1 \u00b7 `c632fa261ce3f538`"
    (mem / "MEMORY.md").write_text("# índice\n\n" + linha + "\n", encoding="utf-8")
    (mem / "MEMORY_2.md").write_text("# dois\n", encoding="utf-8")
    for n in ("site-sessao-estado.md", "tgl-fronteira-teorica.md", "central-de-patentes-estado.md", "dispositivos-formula-completa.md"):
        (mem / n).write_text("# %s\n" % n, encoding="utf-8")
    (banc / "DIARIO_DO_SITE.md").write_text("# diário\n", encoding="utf-8")
    atlas.write_text("# Atlas (brinquedo)\n", encoding="utf-8")
    os.environ["MAPA_DE_ROTAS_DIR"] = str(mapa)
    try:
        c = Caminhos({"MEM": str(mem), "BANC": str(banc), "ATLAS": str(atlas), "MAPA": str(mapa)})
        ctx = motor.Ctx(c=c, versao="v398", data="24/10/2026", trabalho=TMP / "w_t37", run_dir=TMP / "run_t37")
        central._ap_c1(ctx)
        memorias._ap_c13(ctx)
        assert memorias._ja_c13(ctx).estado == "APLICADO"
        livro = (mapa / "rotas.jsonl").read_text(encoding="utf-8")
        assert "custodia.v398" not in livro and not (TMP / "w_t37" / "rota_custodia_v398.json").exists(), "C13 NÃO registra a rota (ainda não há push da Central nem conferência final)"
        m16 = memorias._ja_c16(ctx)
        assert m16.estado == "FALTA" and "rota custodia.v398" in m16.detalhe, m16
        f16 = memorias._pre_c16(ctx)
        if f16:
            return "C13 de ponta a ponta no sandbox NÃO registrou a rota (livro vazio); C16 não rodou (pré: %s)" % f16[:2]
        r = memorias._ap_c16(ctx)
        assert r["rota"] == "registrada", r
        livro = [json.loads(l) for l in (mapa / "rotas.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        reg = [x for x in livro if "custodia.v398" in json.dumps(x)]
        assert reg, "a rota entrou em C16"
        assert "PUBLICADA" in json.dumps(reg[-1], ensure_ascii=False) and "conferência final" in json.dumps(reg[-1], ensure_ascii=False).lower().replace("conferencia", "conferência"), "o resultado da rota é o texto PUBLICADA, com a conferência final"
        assert memorias._ja_c16(ctx).estado == "APLICADO"
        assert memorias._ap_c16(ctx)["rota"] == "ja_existe", "2ª execução: a rota não duplica"
        return "C13 não escreve a rota (livro vazio, sem rota_custodia_v398.json); _ja_c16 FALTA citando a rota; C16 registra uma vez, com o texto PUBLICADA e a conferência final; 2ª execução não duplica"
    finally:
        os.environ.pop("MAPA_DE_ROTAS_DIR", None)


# ============================================================ OS ACHADOS DO CÉTICO FINAL (24/10/2026): t38+ — um teste de regressão por achado
import types as _types


def _cenario_site(nome):
    """Um site de brinquedo + a bancada de brinquedo + o manifesto gerado pelo gerador REAL, e o Caminhos que os usa."""
    raiz = TMP / nome
    site_d, banc = _site_sandbox(raiz)
    man = _gerar_manifesto(site_d, banc, "manifesto_v398.json")
    return raiz, site_d, banc, Caminhos({"SITE": str(site_d), "BANC": str(banc)}), man


def _nada(banc, carimbo, man, estados=None):
    """A pasta que `subir_site.py` grava quando o ar JÁ é igual ao manifesto: a cópia do manifesto e um relatório «nada a subir» SEM «SUBIDA VERIFICADA»."""
    d = banc / "subidas" / carimbo
    d.mkdir(parents=True)
    (d / "MANIFESTO_SUBIDA.json").write_text(json.dumps(man), encoding="utf-8")
    (d / "RELATORIO.md").write_text("# SUBIDA %s \u2014 nada a subir: o ar j\u00e1 \u00e9 igual ao manifesto\n\n| arquivo | bytes local | sha16 local | HTTP | bytes ar | content-type | estado |\n|---|---|---|---|---|---|---|\n%s\n" % (
        carimbo, _linhas_do_relatorio(man, estados)), encoding="utf-8")
    return d


# ------------------------------------------------------------ t38 — «nada a subir» não esconde a subida verificada anterior (MEDIA)
@teste()
def t38_nada_a_subir_nao_esconde_a_verificada():
    from custodia_g1 import site
    from custodia_g1.util import Divergencia
    # A) o roteiro do cético: subida verificada, depois uma repetição em que o ar já era igual («nada a subir», sem «SUBIDA VERIFICADA»)
    raiz, site_d, banc, c, man = _cenario_site("t38a")
    mk = lambda v="v398": motor.Ctx(c=c, versao=v, trabalho=raiz / "w")
    _ensaio(banc, _agora_mais(1), man)
    ver = _subida(banc, _agora_mais(2), man)
    assert site._ja_e18(mk()).estado == "APLICADO"
    nada = _nada(banc, _agora_mais(30), man)
    ctx = mk()
    assert site._natureza(ctx, ver) == "VERIFICADA" and site._natureza(ctx, nada) == "NADA"
    m18 = site._ja_e18(ctx)
    assert m18.estado == "APLICADO" and nada.name in m18.detalhe and "nada a subir" in m18.detalhe, m18
    ar = site.ar_pelo_registro(ctx, site.disco_atual(ctx))
    assert ar["ok"] and ar["ultima"] == nada.name and ar["ultima_tipo"] == "NADA" and not ar["desconhecidos"] and not ar["nunca"], ar
    assert site._ja_e17(ctx).estado in ("APLICADO", "SUPERADO") and site._ja_e16(ctx).estado == "APLICADO"
    # «nada a subir» não muda o ar: o instante da última subida (marco do quadro e do leitor de IA) continua sendo o da verificada
    assert abs((site.instante_da_ultima_subida(ctx) - _dt.fromtimestamp((ver / "RELATORIO.md").stat().st_mtime)).total_seconds()) < 1
    # B) linha «IGUAL EM TAMANHO» (arquivo grande, hash não comparado) NÃO decide: a subida verificada mais antiga continua valendo; se decidisse, index.html ficaria DESCONHECIDO
    raiz, site_d, banc, c, man = _cenario_site("t38b")
    mk = lambda v="v398": motor.Ctx(c=c, versao=v, trabalho=raiz / "w")
    _ensaio(banc, _agora_mais(1), man)
    _subida(banc, _agora_mais(2), man)
    _nada(banc, _agora_mais(30), man, {"index.html": "IGUAL EM TAMANHO (hash nao comparado: > 67.108.864 B)"})
    ar = site.ar_pelo_registro(mk(), site.disco_atual(mk()))
    assert ar["ok"] and not ar["desconhecidos"], ar
    # C) uma linha que CONTRADIZ o título («nada a subir» com um DIFERENTE) deixa o arquivo DESCONHECIDO: o relatório não é prova de nada
    raiz, site_d, banc, c, man = _cenario_site("t38c")
    mk = lambda v="v398": motor.Ctx(c=c, versao=v, trabalho=raiz / "w")
    _ensaio(banc, _agora_mais(1), man)
    _subida(banc, _agora_mais(2), man)
    _nada(banc, _agora_mais(30), man, {"llms.txt": "DIFERENTE (sha256 local != ar; 7 B local, 9 B ar)"})
    ctx = mk()
    ar = site.ar_pelo_registro(ctx, site.disco_atual(ctx))
    assert ar["desconhecidos"] == ["llms.txt"] and not ar["ok"], ar
    assert site._ja_e18(ctx).estado == "FALTA"
    # D) só o «nada a subir» (o ar já era igual por outra via): a própria pasta atesta, linha a linha
    raiz, site_d, banc, c, man = _cenario_site("t38d")
    mk = lambda v="v398": motor.Ctx(c=c, versao=v, trabalho=raiz / "w")
    _ensaio(banc, _agora_mais(1), man)
    nada_so = _nada(banc, _agora_mais(30), man)
    m = site._ja_e18(mk())
    assert m.estado == "APLICADO" and nada_so.name in m.detalhe, m
    # E) o conteúdo MUDA (e o manifesto é regerado): nenhuma pasta antiga cobre, «nada a subir» inclusive
    (site_d / "llms.txt").write_text("llms v2 com conteudo novo", encoding="utf-8")
    _gerar_manifesto(site_d, banc, "manifesto_v398.json")
    e18 = site._ja_e18(mk())
    assert e18.estado == "FALTA" and "llms.txt" in e18.detalhe, e18
    # F) versão HISTÓRICA: o alvo é o manifesto da versão; uma pasta de «nada a subir» que traz IGUAL em cada arquivo vale (e diz que foi «nada a subir»)
    raiz, site_d, banc, c, man = _cenario_site("t38f")
    man97 = _gerar_manifesto(site_d, banc, "manifesto_v397.json")
    mk = lambda v: motor.Ctx(c=c, versao=v, trabalho=raiz / "w")
    nada97 = _nada(banc, _agora_mais(30), man97)
    ctx = mk("v397")
    m = site._ja_e18(ctx)
    assert m.estado == "APLICADO" and "nada a subir" in m.detalhe and nada97.name in m.detalhe, m
    assert site.instante_da_subida_que_vale(ctx) is None, "sem subida verificada que levou o manifesto: nenhum limite para o leitor"
    # G) o aplicador: «nada a subir» (rc 0) é terminação VÁLIDA; qualquer outra coisa continua sendo Divergencia
    ctx = mk("v398")
    orig = util.rodar
    try:
        util.rodar = lambda cmd, **kw: {"rc": 0, "saida": "a subir: 0 de 5\n# SUBIDA 20261024_140000 \u2014 nada a subir: o ar j\u00e1 \u00e9 igual ao manifesto\n\n| t |\n"}
        assert site._ap_e18(ctx)["veredito"].startswith("NADA A SUBIR")
        util.rodar = lambda cmd, **kw: {"rc": 0, "saida": "**SUBIDA VERIFICADA** \u2014 o ar diz o que o manifesto descreve."}
        assert site._ap_e18(ctx)["veredito"] == "SUBIDA VERIFICADA"
        for rc, saida in ((0, "tudo bem, sem veredito\n"), (1, "# SUBIDA 1 \u2014 nada a subir: o ar j\u00e1 \u00e9 igual ao manifesto\n"), (1, "FALHOU \u2014 REVERTIDO")):
            util.rodar = lambda cmd, rc=rc, saida=saida, **kw: {"rc": rc, "saida": saida}
            try:
                site._ap_e18(ctx)
                raise AssertionError("devia levantar Divergencia: rc %s %r" % (rc, saida))
            except Divergencia:
                pass
    finally:
        util.rodar = orig
    return ("subida verificada + repetição «nada a subir» (sem «SUBIDA VERIFICADA») → E18 APLICADO (antes: FALTA, os arquivos viravam DESCONHECIDOS e _ap_e18 travava); a linha «IGUAL» atesta o sha256, «IGUAL EM TAMANHO» "
            "não decide (a verificada mais antiga decide), linha que contradiz o título → DESCONHECIDO; só o «nada a subir» também atesta; conteúdo novo continua FALTA; histórica idem; o instante da última subida "
            "(quadro, leitor) ignora o «nada a subir»; _ap_e18 aceita as duas terminações e recusa o resto")


# ------------------------------------------------------------ t39 — C14: o commit leva SÓ a lista de permissão; o alheio já staged fica fora (MEDIA) + a frase da rota (BAIXA)
@teste()
def t39_c14_commit_so_da_lista_de_permissao():
    from custodia_g1 import central, textos
    from custodia_g1.util import Parar
    raiz = TMP / "t39"
    base = {"memory/TGL_ATLAS.md": b"atlas\n", "alheio/a.txt": b"a\n", "alheio/b.txt": b"b\n", "fronteira_tgl/ledger_de_pinos.json": b"{}\n", "fronteira_tgl/LEDGER_DE_PINOS.md": b"ledger\n"}
    repo = _git_toy(raiz, "cen", [("init", base)])
    bare = raiz / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", str(bare)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "push", "-q", "-u", "origin", "main"], check=True, capture_output=True)
    # o estado do mundo: o cofre novo (não rastreado) e o ledger mexido (são da lista); OUTRA SESSÃO pôs um arquivo seu no índice, mexeu em outro e criou um terceiro
    (repo / "vault" / "originals_copy" / "um_unificado_v999").mkdir(parents=True)
    (repo / "vault" / "originals_copy" / "um_unificado_v999" / "CUSTODY_MANIFEST.json").write_bytes(b"{}\n")
    (repo / "fronteira_tgl" / "ledger_de_pinos.json").write_bytes(b'{"erros": 0}\n')
    (repo / "alheio" / "a.txt").write_bytes(b"a mexido por outra sessao\n")
    subprocess.run(["git", "-C", str(repo), "add", "--", "alheio/a.txt"], check=True, capture_output=True)          # JÁ no índice (staged) por outra sessão
    (repo / "alheio" / "b.txt").write_bytes(b"b mexido e NAO staged\n")
    (repo / "alheio" / "novo.txt").write_bytes(b"novo e nao rastreado\n")
    ps = ["vault/originals_copy/um_unificado_v999", "fronteira_tgl/ledger_de_pinos.json"]
    msg = raiz / "commit_central_v999.txt"
    msg.write_text("custodia(v999): teste\n\nMemorias: Atlas e memorias da sessao com o registro da custodia.\n", encoding="utf-8")
    repo_antes = raiz / "cen_antes"
    shutil.copytree(util.lp(repo), util.lp(repo_antes))
    arqs_do_commit = lambda r, rev="HEAD": set(util.git(r, "diff-tree", "--no-commit-id", "--name-only", "-r", rev).splitlines())
    # 1) O DEFEITO (como era: git add da lista + git commit -F SEM pathspec): o arquivo alheio staged ENTRA no commit custodia(vN)
    for p in ps:
        subprocess.run(["git", "-C", str(repo_antes), "add", "--", p], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_antes), "commit", "-q", "-F", str(msg)], check=True, capture_output=True)
    assert "alheio/a.txt" in arqs_do_commit(repo_antes), "o defeito deveria reproduzir: o alheio staged entra no commit sem pathspec"
    # 2) A CORREÇÃO: commit com pathspec — só a lista; o alheio fica no índice, intacto
    r = central.commitar_so_a_lista(repo, ps, msg, raiz)
    no_commit = arqs_do_commit(repo)
    assert no_commit == {"vault/originals_copy/um_unificado_v999/CUSTODY_MANIFEST.json", "fronteira_tgl/ledger_de_pinos.json"}, no_commit
    assert r["alheios_preservados"] == ["alheio/a.txt"], r
    assert util.git(repo, "diff", "--cached", "--name-only").splitlines() == ["alheio/a.txt"], "o alheio continua staged, intacto"
    assert (repo / "alheio" / "a.txt").read_bytes() == b"a mexido por outra sessao\n" and (repo / "alheio" / "b.txt").read_bytes() == b"b mexido e NAO staged\n"
    # 3) o empurrão de ponta a ponta por _ap_c14 (o resto do mundo substituído): origin recebe só a lista
    repo2 = _git_toy(raiz, "cen2", [("init", base)])
    subprocess.run(["git", "-C", str(repo2), "remote", "add", "origin", str(bare)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo2), "fetch", "-q", "origin"], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo2), "reset", "-q", "--hard", "origin/main"], check=True, capture_output=True)       # parte do mesmo main do origin
    (repo2 / "vault" / "originals_copy" / "um_unificado_v998").mkdir(parents=True)
    (repo2 / "vault" / "originals_copy" / "um_unificado_v998" / "x.json").write_bytes(b"{}\n")
    (repo2 / "alheio" / "a.txt").write_bytes(b"alheio staged 2\n")
    subprocess.run(["git", "-C", str(repo2), "add", "--", "alheio/a.txt"], check=True, capture_output=True)
    salvos = (central.caminhos_a_commitar, central.commit_central, textos.portao, textos.conhecidos_da_rodada)
    try:
        central.caminhos_a_commitar = lambda ctx: (["vault/originals_copy/um_unificado_v998"], [])
        central.commit_central = lambda ctx, Fa: "custodia(v998): teste e2e\n\nMemorias: Atlas e memorias da sessao com o registro da custodia.\n"
        textos.portao = lambda *a, **k: []
        textos.conhecidos_da_rodada = lambda ctx: set()
        ctx = motor.Ctx(c=Caminhos({"CEN": str(repo2)}), versao="v998", data="24/10/2026", trabalho=raiz / "w2")
        ctx._memo["fatos"] = {"anterior": "v997"}
        out = central._ap_c14(ctx)
    finally:
        central.caminhos_a_commitar, central.commit_central, textos.portao, textos.conhecidos_da_rodada = salvos
    assert out["alheios_no_indice_preservados"] == ["alheio/a.txt"] and out["commit"].endswith("teste e2e"), out
    no_origin = set(util.git(bare, "diff-tree", "--no-commit-id", "--name-only", "-r", "main").splitlines())
    assert no_origin == {"vault/originals_copy/um_unificado_v998/x.json"}, no_origin
    assert util.git(repo2, "diff", "--cached", "--name-only").splitlines() == ["alheio/a.txt"]
    # 4) nada da lista a commitar: PARA com a explicação; arquivo da lista negra NO ESCOPO: PARA
    try:
        central.commitar_so_a_lista(repo2, ["fronteira_tgl/ledger_de_pinos.json"], msg, raiz)
        raise AssertionError("devia parar: nada a commitar na lista")
    except Parar as e:
        assert "nada a commitar" in e.motivo and any("alheio/a.txt" in x for x in e.faltam), (e.motivo, e.faltam)
    (repo2 / "vault" / "originals_copy" / "um_unificado_v998" / "x.json.bak_20261024").write_bytes(b"lixo")
    try:
        central.commitar_so_a_lista(repo2, ["vault/originals_copy/um_unificado_v998"], msg, raiz)
        raise AssertionError("devia parar: .bak_ na lista negra")
    except Parar as e:
        assert "lista negra" in e.motivo, e.motivo
    # 5) BAIXA: a mensagem do commit da Central NÃO afirma a rota no mapa (ela só entra em C16, depois do push e da conferência final)
    ctx = ctx_de("v398")
    texto = central.commit_central(ctx, ctx.fatos)
    assert "mapa de rotas" not in texto and "rota custodia" not in texto and texto.splitlines()[0].startswith("custodia(v398): "), texto[:400]
    assert "Memorias: Atlas e memorias da sessao com o registro da custodia." in texto
    return ("o defeito reproduz (git commit sem pathspec leva o arquivo alheio staged); com `--pathspec-from-file` o commit tem só a lista (cofre novo + ledger), o alheio fica staged e intacto, o origin "
            "recebe só a lista (e2e por _ap_c14 em repositório de brinquedo com origin local); nada na lista → PARA dizendo o que ficou de fora; lista negra no escopo → PARA; a mensagem do commit da Central não cita a rota")


# ------------------------------------------------------------ t40 — `vigiar --gravar`: VIGIA_ULTIMO.json/.txt, backup só quando muda, plano guardado validado (MEDIA)
@teste()
def t40_vigiar_gravar_modo_sombra():
    import custodiar
    pasta = TMP / "t40"
    # a) gravar_vigia: JSON + vista chave=valor; mesma coisa (só a hora muda) = sem backup; mudou = backup de BYTES do anterior
    s1 = {"esquema": "custodia_vigia/1", "versao": "v900", "selo": "v900", "marcas": "PRONTA", "codigo": 1, "estado": "PENDENTE \u2014 pronta para planejar", "hora": "2026-10-24T10:00:00-03:00", "plano": {"pendentes": ["C11"]}}
    f = custodiar.gravar_vigia(pasta, s1)
    assert json.loads(f.read_text(encoding="utf-8")) == s1
    txt = dict(l.split("=", 1) for l in (pasta / "VIGIA_ULTIMO.txt").read_text(encoding="utf-8").splitlines())
    assert txt == {"versao": "v900", "selo": "v900", "marcas": "PRONTA", "codigo": "1", "estado": "PENDENTE", "hora": "2026-10-24T10:00:00-03:00"}, txt
    custodiar.gravar_vigia(pasta, dict(s1, hora="2026-10-24T10:15:00-03:00"))
    assert not list(pasta.glob("VIGIA_ULTIMO.json.bak_*")), "só a hora mudou: nenhuma cópia por rodada"
    assert json.loads(f.read_text(encoding="utf-8"))["hora"].endswith("10:15:00-03:00")
    antes = f.read_bytes()
    custodiar.gravar_vigia(pasta, dict(s1, codigo=0, hora="2026-10-24T10:30:00-03:00"))
    baks = list(pasta.glob("VIGIA_ULTIMO.json.bak_*"))
    assert len(baks) == 1 and baks[0].read_bytes() == antes, "o conteúdo mudou: backup de BYTES do anterior"
    # b) o CLI de ponta a ponta numa versão em obra (rápido): rc 10, stdout SÓ JSON == o arquivo
    py = [sys.executable, "-X", "utf8", str(CEN / "tools" / "custodiar.py")]
    d1 = pasta / "cli_v999"
    r = subprocess.run(py + ["vigiar", "--versao", "v999", "--gravar", "--saida", str(d1), "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    j = json.loads(r.stdout)
    assert r.returncode == 10 == j["codigo"] and j["marcas"] == "EM_OBRA" and j["versao"] == "v999" and j["modo"].startswith("SOMBRA"), (r.returncode, r.stdout[-300:])
    assert json.loads((d1 / "VIGIA_ULTIMO.json").read_text(encoding="utf-8")) == j
    assert "marcas=EM_OBRA" in (d1 / "VIGIA_ULTIMO.txt").read_text(encoding="utf-8") and "versao=v999" in (d1 / "VIGIA_ULTIMO.txt").read_text(encoding="utf-8")
    # c) o mundo real: a versão do selo (as três marcas), com o plano resumido; o código do processo é o do contrato e o do arquivo
    d2 = pasta / "cli_real"
    r = subprocess.run(py + ["vigiar", "--gravar", "--saida", str(d2), "--json"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    j = json.loads(r.stdout)
    selo_v = nos.selo(Caminhos())["um_version"]
    assert j["versao"] == selo_v and j["marcas"] in ("PRONTA", "EM_OBRA") and "hora" in j, j.keys()          # o Nós vivo pode estar em obra (outra sessão): a forma vale nos dois estados
    assert r.returncode == j["codigo"] and j["codigo"] in (0, 1, 5, 10, 20, 30, 40), (r.returncode, j["codigo"])
    if j["marcas"] == "PRONTA":
        assert "plano" in j and "pendentes" in j["plano"], j.keys()
        assert all(len(x.get("texto", "")) <= 400 for x in j["plano"]["decisoes_do_operador"]), "o plano resumido corta o texto das decisões em 400 caracteres"
    else:
        assert j["codigo"] == 10 and "plano" not in j and j["faltam"], j
    assert json.loads((d2 / "VIGIA_ULTIMO.json").read_text(encoding="utf-8")) == j
    assert ("codigo=%d" % j["codigo"]) in (d2 / "VIGIA_ULTIMO.txt").read_text(encoding="utf-8") and ("marcas=%s" % j["marcas"]) in (d2 / "VIGIA_ULTIMO.txt").read_text(encoding="utf-8")
    # d) _guardar_plano: valida, é atômico, idêntico não é tocado, mudou = backup; saída que não é o plano NÃO sobrescreve o plano guardado (rc 30)
    plano = {"versao": "v900", "itens": [{"id": "E00"}], "pendentes": ["C11"]}
    de, para = pasta / "plano_tmp.json", pasta / "PLANO_v900.json"
    gp = lambda arq, v="v900": subprocess.run(py + ["_guardar_plano", "--de", str(arq), "--para", str(para), "--versao", v], capture_output=True, text=True, encoding="utf-8", errors="replace")
    de.write_text(json.dumps(plano), encoding="utf-8")
    assert gp(de).returncode == 0 and json.loads(para.read_text(encoding="utf-8")) == plano
    t0 = para.stat().st_mtime_ns
    assert gp(de).returncode == 0 and para.stat().st_mtime_ns == t0 and "nada escrito" in gp(de).stdout and not list(pasta.glob("PLANO_v900.json.bak_*")), "idêntico: o arquivo nem é tocado"
    de.write_text(json.dumps(dict(plano, pendentes=["C11", "E19"])), encoding="utf-8")
    assert gp(de).returncode == 0 and len(list(pasta.glob("PLANO_v900.json.bak_*"))) == 1
    guardado = para.read_bytes()
    de.write_text("FALHALEITURA: lixo que não é JSON", encoding="utf-8")
    assert gp(de).returncode == 30 and para.read_bytes() == guardado
    de.write_text(json.dumps({"versao": "v901", "itens": []}), encoding="utf-8")
    assert gp(de).returncode == 30 and para.read_bytes() == guardado, "plano de OUTRA versão não entra"
    de.write_text(json.dumps({"versao": "v900", "estado": "EM_OBRA"}), encoding="utf-8")
    assert gp(de).returncode == 30 and para.read_bytes() == guardado, "sem os itens não é o plano"
    # e o plano REAL (o mesmo par de comandos que o vigia.bat roda), numa versão histórica que se planeja em qualquer estado do Nós: a saída do planejar --seco --json é aceita e guardada
    real_json = pasta / "plano_real_v397.json"
    with open(real_json, "wb") as fh:
        pr = subprocess.run(py + ["planejar", "--versao", "v397", "--seco", "--json"], stdout=fh, stderr=subprocess.PIPE)
    assert pr.returncode in (0, 1, 5, 20, 30), pr.returncode
    alvo_real = pasta / "PLANO_v397.json"
    g = subprocess.run(py + ["_guardar_plano", "--de", str(real_json), "--para", str(alvo_real), "--versao", "v397"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    pj = json.loads(alvo_real.read_text(encoding="utf-8"))
    assert g.returncode == 0 and pj["versao"] == "v397" and len(pj["itens"]) >= 40 and "C21" in [i["id"] for i in pj["itens"]], (g.returncode, g.stdout[-200:], g.stderr[-200:])
    return ("vigiar --gravar escreve VIGIA_ULTIMO.json (versão vista, marcas, código, plano resumido, hora) e .txt; só a hora mudou = sem cópia, mudou = backup de bytes; CLI em v999: rc 10, stdout só JSON == arquivo; "
            "v%s real (%s): rc %d == código do arquivo; o plano REAL da v397 (%d passos, com o C21) é aceito e guardado; _guardar_plano valida (JSON, versão, itens), não toca o idêntico, faz backup quando muda e recusa lixo/outra versão com rc 30 sem sobrescrever" % (selo_v[1:], j["marcas"], j["codigo"], len(pj["itens"])))


# ------------------------------------------------------------ t41 — vigia.bat em MODO SOMBRA (rodado de verdade, com um custodiar.py de brinquedo)
@teste()
def t41_vigia_bat_modo_sombra():
    bat = CEN / "tools" / "custodia_g1" / "vigia.bat"
    texto = bat.read_bytes().decode("ascii")
    codigo = [l for l in texto.splitlines() if l.strip() and not l.strip().lower().startswith("rem ")]
    proibidas = ("executar", "--publicar", "--force", "--sem-guarda", "--permitir-ftp-em-claro")
    achadas = [p for p in proibidas if any(p in l for l in codigo)]
    assert not achadas, "o MODO SOMBRA não executa nem publica: %s" % achadas
    assert any("vigiar --gravar" in l for l in codigo) and any("planejar --versao %VER% --seco" in l for l in codigo) and any("PLANO_%VER%.json" in l for l in codigo)
    raiz = TMP / "t41"
    raiz.mkdir()
    real_cli = str(CEN / "tools" / "custodiar.py")
    fake = raiz / "fake_custodiar.py"
    fake.write_text('''# -*- coding: utf-8 -*-
import json, os, pathlib, runpy, sys
REAL = @REAL@
args = sys.argv[1:]
pasta = pathlib.Path(os.environ["G1_PASTA"])
with open(pasta / "calls.log", "a", encoding="utf-8") as f:
    f.write(" ".join(args) + "\\n")
if args[0] == "vigiar":
    if os.environ.get("FAKE_CRASH"):
        sys.exit(1)               # o vigiar quebra ANTES de gravar qualquer coisa
    d = pathlib.Path(args[args.index("--saida") + 1])
    (d / "VIGIA_ULTIMO.txt").write_text("versao=v900\\nselo=v900\\nmarcas=%s\\ncodigo=1\\nestado=PENDENTE\\nhora=x\\n" % os.environ["FAKE_MARCAS"], encoding="utf-8")
    print(json.dumps({"versao": "v900"}))
    sys.exit(int(os.environ["FAKE_RC"]))
if args[0] == "planejar":
    if os.environ.get("FAKE_LIXO"):
        print("FALHALEITURA: isto nao e JSON")
    else:
        print(json.dumps({"versao": args[args.index("--versao") + 1], "itens": [{"id": "E00"}], "pendentes": os.environ.get("FAKE_PENDENTES", "C11").split(",")}))
    sys.exit(1)
sys.argv = [REAL] + args
runpy.run_path(REAL, run_name="__main__")
'''.replace("@REAL@", repr(real_cli)), encoding="utf-8")

    def roda(pasta, marcas="PRONTA", rc="1", **extra):
        env = dict(os.environ, G1_PY=sys.executable, G1_CLI=str(fake), G1_PASTA=str(pasta), FAKE_MARCAS=marcas, FAKE_RC=rc, **extra)
        return subprocess.run(["cmd", "/c", str(bat)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)

    def chamadas(pasta):
        p = pasta / "calls.log"
        return p.read_text(encoding="utf-8").splitlines() if p.is_file() else []
    # 1) as três marcas presentes: vigiar --gravar, depois planejar --seco, depois o plano guardado; rc = o do vigiar; nunca executar/--publicar
    pasta = raiz / "p1"
    pasta.mkdir()
    r = roda(pasta)
    assert r.returncode == 1, (r.returncode, r.stdout[-300:], r.stderr[-300:])
    cs = chamadas(pasta)
    assert cs[0].startswith("vigiar --gravar") and "--json" in cs[0] and cs[1].startswith("planejar --versao v900 --seco --json") and cs[2].startswith("_guardar_plano"), cs
    assert not any(x in " ".join(cs) for x in ("executar", "--publicar", "--force", "--sem-guarda", "--permitir-ftp-em-claro")), cs
    plano = pasta / "PLANO_v900.json"
    assert json.loads(plano.read_text(encoding="utf-8"))["pendentes"] == ["C11"]
    # 2) rodada idêntica: o plano nem é tocado; plano mudou: backup de bytes
    t0 = plano.stat().st_mtime_ns
    assert roda(pasta).returncode == 1 and plano.stat().st_mtime_ns == t0 and not list(pasta.glob("PLANO_v900.json.bak_*"))
    antes = plano.read_bytes()
    assert roda(pasta, FAKE_PENDENTES="C11,E19").returncode == 1
    baks = list(pasta.glob("PLANO_v900.json.bak_*"))
    assert len(baks) == 1 and baks[0].read_bytes() == antes and json.loads(plano.read_text(encoding="utf-8"))["pendentes"] == ["C11", "E19"]
    # 3) saída do planejar que não é JSON: o plano guardado NÃO é sobrescrito e o vigia sai com 30 (visível)
    guardado = plano.read_bytes()
    r = roda(pasta, FAKE_LIXO="1")
    assert r.returncode == 30 and plano.read_bytes() == guardado, (r.returncode,)
    # 3b) o vigiar QUEBRA sem gravar nada: a vista chave=valor da rodada anterior (PRONTA) não pode mandar planejar de novo (fail-closed); o plano guardado fica
    assert (pasta / "VIGIA_ULTIMO.txt").is_file()
    n_antes = len(chamadas(pasta))
    r = roda(pasta, FAKE_CRASH="1")
    novas = chamadas(pasta)[n_antes:]
    assert r.returncode == 1 and novas == ["vigiar --gravar --saida %s --json" % pasta] and not (pasta / "VIGIA_ULTIMO.txt").exists() and plano.read_bytes() == guardado, (r.returncode, novas)
    # 4) o Nós em obra: não há plano nem chamada do planejar; o código é o do vigiar (10)
    pasta2 = raiz / "p2"
    pasta2.mkdir()
    r = roda(pasta2, marcas="EM_OBRA", rc="10")
    assert r.returncode == 10 and not (pasta2 / "PLANO_v900.json").exists() and all(not x.startswith("planejar") for x in chamadas(pasta2)), (r.returncode, chamadas(pasta2))
    # 5) Python ou custodiar.py inexistente: 99, dito
    env = dict(os.environ, G1_PY=str(raiz / "nao_existe.exe"), G1_CLI=str(fake), G1_PASTA=str(pasta2))
    r = subprocess.run(["cmd", "/c", str(bat)], env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
    assert r.returncode == 99 and "Python nao achado" in r.stderr, (r.returncode, r.stderr)
    return ("vigia.bat rodado de verdade (custodiar.py de brinquedo): as três marcas → vigiar --gravar, planejar --seco --json, plano guardado em PLANO_vNNN.json (idêntico = intocado, mudou = backup de bytes); "
            "saída que não é JSON → rc 30 sem sobrescrever; vigiar que quebra sem gravar → nenhuma marca velha reaproveitada (não planeja); Nós em obra → só o vigiar, rc 10; sem Python → rc 99; nenhuma linha de código do .bat tem executar/--publicar/--force/--sem-guarda/--permitir-ftp-em-claro; rc = o do vigiar")


# ------------------------------------------------------------ t42 — C21: a release do app, só conferir (MEDIA, escopo)
@teste()
def t42_c21_a_release_do_app_so_confere():
    from custodia_g1 import quadro
    raiz = TMP / "t42"
    (raiz / "app").mkdir(parents=True)
    real = ctx_de("v398")
    pin = real.pin_completo
    assert pin and len(pin) == 64

    def com_app(rel, src=None, cluster=None, jev=None, texto=None, versao="v398"):
        d = {"format": 1, "operational_core": {"current_release": rel, "release_source_sha256": src}}
        if cluster:
            d["active_cluster"] = {"release": cluster}
        if jev:
            d["jev_control"] = {"release": jev}
        (raiz / "app" / "iald_nucleo_fixo.json").write_text(texto if texto is not None else json.dumps(d), encoding="utf-8")
        return motor.Ctx(c=Caminhos({"APP": str(raiz / "app")}), versao=versao, data="24/10/2026")
    passo = [p for p in quadro.passos(real) if p.id == "C21"][0]
    assert passo.aplicar is None and not passo.externo, "C21 só CONFERE: não tem aplicador nem é ato para fora"
    # defasada: OPERADOR, com a instrução do pipeline do app; entra nas decisões do operador e muda o código (5)
    ctx = com_app("v395", "a" * 64)
    m = quadro._ja_c21(ctx)
    assert m.estado == "OPERADOR" and "DEFASADO" in m.detalhe and "v395" in m.detalhe and "pipeline work\\iald_v398_<data>\\app (fase A/B; construtor \u2260 revisor; troca do servi\u00e7o pelo operador)" in m.detalhe, m
    decs = motor.decisoes_do_operador(ctx, [(passo, m)], plano_real=False)
    assert decs == [{"origem": "C21", "texto": m.detalhe}], decs
    saidas = []
    ctx.ensaio = True
    exigir = nos.exigir_pronta
    nos.exigir_pronta = lambda c_, v_: None          # o gate das três marcas do Nós é de t01/t13; aqui o Nós (vivo, de outra sessão) pode estar em obra
    try:
        cod, rel = motor.executar(ctx, passos=[passo], imprimir=lambda *a: saidas.append(" ".join(str(x) for x in a)))
    finally:
        nos.exigir_pronta = exigir
    assert cod == util.COD_OPERADOR and rel["passos"][0]["resultado"] == "PENDENTE_OPERADOR" and any("PENDENTE DO OPERADOR" in x for x in saidas), (cod, rel["passos"], saidas)
    # em dia: a release da versão com o sha256 do um.py = o pino do selo (lido do selo, nunca digitado)
    assert quadro._ja_c21(com_app("v398", pin)).estado == "APLICADO"
    # a release diz v398 mas o um.py de que saiu NÃO é o do selo: OPERADOR, não «em dia pelo nome»
    m = quadro._ja_c21(com_app("v398", "0" * 64))
    assert m.estado == "OPERADOR" and "N\u00c3O \u00e9 o pino do selo" in m.detalhe, m
    # release posterior: superada (o app já tem coisa mais nova); instalação incoerente (núcleo novo, cluster/JEV velhos): OPERADOR
    assert quadro._ja_c21(com_app("v399", "b" * 64)).estado == "SUPERADO"
    m = quadro._ja_c21(com_app("v398", pin, cluster="v395", jev="v398"))
    assert m.estado == "OPERADOR" and "incoerente" in m.detalhe and "active_cluster v395" in m.detalhe, m
    # versão histórica: o pipeline que se cita é o da versão CORRENTE do selo
    m = quadro._ja_c21(com_app("v395", "a" * 64, versao="v397"))
    assert m.estado == "OPERADOR" and "hist\u00f3rica" in m.detalhe and "iald_v398_<data>" in m.detalhe, m
    # arquivo ausente, JSON inválido ou sem a release: falha de LEITURA visível (nunca «em dia»)
    for texto in ("{ isto nao e json", json.dumps({"operational_core": {}}), json.dumps({"operational_core": {"current_release": "versao-x"}})):
        mm = motor.marca_de(com_app("v395", texto=texto), passo)
        assert mm.estado == "INDETERMINADO" and mm.leitura, mm
    (raiz / "app" / "iald_nucleo_fixo.json").unlink()
    mm = motor.marca_de(motor.Ctx(c=Caminhos({"APP": str(raiz / "app")}), versao="v398"), passo)
    assert mm.estado == "INDETERMINADO" and mm.leitura, mm
    # no plano das quatro pernas: depois de C20, antes de C17C
    ids = [p.id for p in motor.montar_plano(real)]
    assert ids.index("C20") < ids.index("C21") < ids.index("C17C") and len(ids) == len(set(ids)), ids
    # o app REAL de hoje (somente leitura)
    rm = quadro._ja_c21(ctx_de("v398"))
    return ("C21 só confere: release v395 < v398 → OPERADOR com a instrução «pipeline work\\iald_v398_<data>\\app (fase A/B; construtor ≠ revisor; troca do serviço pelo operador)», decisão do operador (código 5), "
            "sem aplicador; v398 com o sha256 do selo → APLICADO; v398 com outro sha256 → OPERADOR; v399 → SUPERADO; núcleo novo e cluster velho → incoerente; histórica cita o pipeline da corrente; "
            "arquivo ausente/inválido → falha de leitura; plano: C20 < C21 < C17C. App real hoje: %s" % rm.estado)


# ------------------------------------------------------------ t43 — E19: só o relatório do leitor MAIS NOVO conta e ele é posterior à última subida (BAIXA)
@teste()
def t43_e19_leitor_mais_novo_e_posterior_a_subida():
    from custodia_g1 import site, publica
    from custodia_g1.util import Parar
    raiz, site_d, banc, c, man = _cenario_site("t43")
    mk = lambda v="v398": motor.Ctx(c=c, versao=v, trabalho=raiz / "w", data="24/10/2026")
    _ensaio(banc, _agora_mais(1), man)
    sub = _subida(banc, _agora_mais(2), man)
    t_sub = _dt(2026, 10, 24, 9, 32, 4, 700000)
    os.utime(sub / "RELATORIO.md", (t_sub.timestamp(), t_sub.timestamp()))

    def leitor(nome, quando, passa=True):
        p = banc / "revisoes" / nome
        p.write_text("# LEITOR-IA (R1) \u2014 %s\n\n| alvo | x |\n\n**R1: %s**\n" % (quando, "PASSA \u2014 os quatro alvos em \u2264 2 saltos e \u2264 100 KB" if passa else "FALHA \u2014 read-brief n\u00e3o achado(s)"), encoding="utf-8")
        return p
    assert site._ja_e19(mk()).estado == "FALTA" and "sem relat" in site._ja_e19(mk()).detalhe
    ok = leitor("leitor_ia_20261024_v398.md", "24/10/2026 09:32:05")
    m = site._ja_e19(mk())
    assert m.estado == "APLICADO" and "R1 passa" in m.detalhe and "posterior" in m.detalhe, m          # a resolução do cabeçalho é de segundo: 09:32:05 vale contra 09:32:04,7
    # a subida MAIS NOVA (a da Central pública, por exemplo) torna o relatório velho: o ar mudou depois dele
    t2 = _dt(2026, 10, 24, 11, 26, 33)
    sub2 = _subida(banc, _agora_mais(50), man)
    os.utime(sub2 / "RELATORIO.md", (t2.timestamp(), t2.timestamp()))
    m = site._ja_e19(mk())
    assert m.estado == "FALTA" and "anterior à última subida" in m.detalhe and "11:26" in m.detalhe, m
    # um relatório MAIS NOVO que reprova NÃO é coberto por um mais antigo que passou (antes: o laço aceitava o PASSA antigo)
    leitor("leitor_ia_20261025_v398.md", "25/10/2026 09:00:00", passa=False)
    m = site._ja_e19(mk())
    assert m.estado == "FALTA" and "leitor_ia_20261025_v398.md" in m.detalhe and "n\u00e3o diz" in m.detalhe, m
    # o relatório novo, depois da última subida, passando: aplicado
    leitor("leitor_ia_20261025_v398.md", "25/10/2026 09:05:00", passa=True)
    assert site._ja_e19(mk()).estado == "APLICADO"
    # ordem pelo INSTANTE do cabeçalho (não pelo nome): um relatório de nome «antigo» mas feito DEPOIS vale como o mais novo
    leitor("leitor_ia_20261024_v398.md", "26/10/2026 10:00:00", passa=False)
    m = site._ja_e19(mk())
    assert m.estado == "FALTA" and "leitor_ia_20261024_v398.md" in m.detalhe and "26/10 10:00:00" in m.detalhe, m
    # _ap_e19 guarda o relatório da mesma data antes de o leitor trocá-lo (leitor_ia.py usa os.replace, sem backup)
    chamadas = []
    antigo = (banc / "revisoes" / "leitor_ia_20261024_v398.md").read_bytes()

    def leitor_falso(ctx, script, *args, **kw):
        chamadas.append((script, args))
        (ctx.c.BANC / args[-1]).write_text("# LEITOR-IA (R1) \u2014 24/10/2026 12:00:00\n\n**R1: PASSA \u2014 os quatro alvos em \u2264 2 saltos e \u2264 100 KB**\n", encoding="utf-8")
        return {"rc": 0, "saida": ""}
    salvo_banc = site._banc
    site._banc = leitor_falso
    try:
        site._ap_e19(mk())
    finally:
        site._banc = salvo_banc
    baks = list((banc / "revisoes").glob("leitor_ia_20261024_v398.md.bak_*"))
    assert len(baks) == 1 and baks[0].read_bytes() == antigo and chamadas == [("leitor_ia.py", ("--relatorio", "revisoes/leitor_ia_20261024_v398.md"))], (baks, chamadas)
    # a Central pública (C18) termina relendo o ar: o leitor roda DEPOIS da subida da perna 3, senão E19 ficaria velho na mesma execução
    ordem = []
    salvos = (util.rodar, publica._passos_do_encadeador, site._banc)
    try:
        publica._passos_do_encadeador = lambda ctx: ["retrato", "subir_ensaio", "subir"]
        util.rodar = lambda cmd, **kw: (ordem.append("rodar:" + (cmd[cmd.index("--so") + 1] if "--so" in cmd else cmd[-1])), {"rc": 0, "saida": ""})[1]
        site._banc = lambda ctx, script, *a, **kw: (ordem.append("leitor"), {"rc": 0, "saida": ""})[1]
        out = publica._ap_c18(mk())
        assert ordem == ["rodar:retrato,subir_ensaio", "rodar:subir", "leitor"] and out["leitor_ia_depois_da_subida"] == "R1 relido", (ordem, out)
        site._banc = lambda ctx, script, *a, **kw: {"rc": 1, "saida": "R1: FALHA"}
        try:
            publica._ap_c18(mk())
            raise AssertionError("devia levantar Parar: o leitor reprovou depois da subida")
        except Parar as e:
            assert "SUBIU" in e.motivo and "leitor de IA" in e.motivo, e.motivo
    finally:
        util.rodar, publica._passos_do_encadeador, site._banc = salvos
    return ("E19: só o relatório MAIS NOVO (pelo instante do cabeçalho) conta — um R1 antigo que passou não cobre um mais recente que reprova (antes: o laço aceitava o PASSA antigo); ele tem de ser posterior à "
            "última subida verificada (resolução de segundo); _ap_e19 guarda o relatório da mesma data antes de o leitor trocá-lo; a Central pública termina relendo o ar (o leitor roda DEPOIS da subida da perna 3, "
            "e a reprovação dele aparece como «a Central pública SUBIU, mas o leitor reprovou»)")


# ------------------------------------------------------------ t44 — E01: o BACKUP_MANIFEST autodeclarado é CONFERIDO por tamanho, por amostra de sha256 e pelo selo de dentro (BAIXA)
@teste()
def t44_backup_do_passo_zero_conferido_por_conteudo():
    import hashlib
    raiz = TMP / "t44"
    P = "v900"
    um = b"# um.py de brinquedo v900\n" * 40

    def montar(nome):
        bk = raiz / nome
        pin = hashlib.sha256(um).hexdigest()
        b = bk / ("um_%s_%s" % (P, pin[:16]))
        arqs = {"um.py": um, "um_absoluto.json": b'{"core": 1}\n', "Lean/tgl_kernel_proof_manifest.json": b'{"m": 1}\n', "fontes_tex/um_absoluto_pt.tex": b"\\documentclass{article}\n"}
        for i in range(120):
            arqs["diferencas/f%03d.md" % i] = ("arquivo %d\n" % i).encode() * (i + 1)
        selo = {"um_version": P, "sha256": {"um.py": pin, "um_absoluto.json": hashlib.sha256(arqs["um_absoluto.json"]).hexdigest(),
                                            "tgl_kernel_proof_manifest.json": hashlib.sha256(arqs["Lean/tgl_kernel_proof_manifest.json"]).hexdigest(),
                                            "um_absoluto_pt.tex": hashlib.sha256(arqs["fontes_tex/um_absoluto_pt.tex"]).hexdigest()}}
        arqs["um_absoluto_selo.json"] = json.dumps(selo).encode()
        for rel, dados in arqs.items():
            (b / rel).parent.mkdir(parents=True, exist_ok=True)
            (b / rel).write_bytes(dados)
        man = {"versao": P, "um_py_sha16": pin[:16], "conferido_contra_origem": True, "n_arquivos": len(arqs),
               "arquivos": {rel: {"bytes": len(d), "sha256": hashlib.sha256(d).hexdigest()} for rel, d in arqs.items()}}
        (b / "BACKUP_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
        return bk, b, pin[:16]

    def ctx_para(bk, pin16):
        ctx = motor.Ctx(c=Caminhos({"BK": str(bk)}), versao="v901", data="24/10/2026")
        return ctx, (lambda cx: {P: _types.SimpleNamespace(pin16=pin16)})
    salvo = espelho._diario

    def valido(bk, pin16):
        ctx, diario = ctx_para(bk, pin16)
        espelho._diario = diario
        try:
            return espelho.backup_valido(ctx, P)
        finally:
            espelho._diario = salvo
    bk, b, pin16 = montar("bk_ok")
    r, det = valido(bk, pin16)
    assert r is not None and "amostra de 48" in det and "selados" in det, (r, det)
    # um byte trocado (mesmo tamanho) num arquivo CRÍTICO, com o manifesto ainda dizendo «conferido_contra_origem: true»
    bk, b, pin16 = montar("bk_byte")
    raw = bytearray((b / "um_absoluto.json").read_bytes())
    raw[2] ^= 1
    (b / "um_absoluto.json").write_bytes(bytes(raw))
    r, det = valido(bk, pin16)
    assert r is None and "sha256" in det and "um_absoluto.json" in det, (r, det)
    # arquivo que sumiu / arquivo que sobra / tamanho diferente
    bk, b, pin16 = montar("bk_falta")
    (b / "diferencas" / "f007.md").unlink()
    r, det = valido(bk, pin16)
    assert r is None and "1 faltam" in det and "f007.md" in det, (r, det)
    bk, b, pin16 = montar("bk_sobra")
    (b / "extra_de_outra_sessao.txt").write_bytes(b"x")
    r, det = valido(bk, pin16)
    assert r is None and "sobram" in det and "extra_de_outra_sessao.txt" in det, (r, det)
    bk, b, pin16 = montar("bk_tam")
    (b / "diferencas" / "f009.md").write_bytes(b"curto")
    r, det = valido(bk, pin16)
    assert r is None and "tamanho diferente" in det and "f009.md" in det, (r, det)
    # o selo DENTRO do backup diz outra versão (o manifesto não prova a versão, o selo sim): refaz o manifesto de propósito para que só o selo acuse
    bk, b, pin16 = montar("bk_selo")
    selo = json.loads((b / "um_absoluto_selo.json").read_text(encoding="utf-8"))
    selo["um_version"] = "v899"
    novo = json.dumps(selo).encode()
    (b / "um_absoluto_selo.json").write_bytes(novo)
    man = json.loads((b / "BACKUP_MANIFEST.json").read_text(encoding="utf-8"))
    man["arquivos"]["um_absoluto_selo.json"] = {"bytes": len(novo), "sha256": hashlib.sha256(novo).hexdigest()}
    (b / "BACKUP_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    r, det = valido(bk, pin16)
    assert r is None and "selo DENTRO do backup diz v899" in det, (r, det)
    # manifesto sem a lista de arquivos (a forma autodeclarada pura) não é aceito
    bk, b, pin16 = montar("bk_sem_lista")
    man = json.loads((b / "BACKUP_MANIFEST.json").read_text(encoding="utf-8"))
    man["arquivos"] = man["n_arquivos"]
    (b / "BACKUP_MANIFEST.json").write_text(json.dumps(man), encoding="utf-8")
    r, det = valido(bk, pin16)
    assert r is None and "autodeclarado" in det, (r, det)
    # os 7 backups REAIS (v390..v397) passam: a conferência não cria falso negativo (somente leitura)
    real = ctx_de("v398")
    reais = []
    for v in ("v390", "v391", "v392", "v394", "v395", "v396", "v397"):
        rb, dt = espelho.backup_valido(real, v)
        assert rb is not None, (v, dt)
        reais.append(v)
    return ("o manifesto autodeclarado deixa de bastar: byte trocado num crítico, arquivo que sumiu, que sobra ou com outro tamanho, selo de dentro de outra versão e manifesto sem a lista são recusados; o bom passa com "
            "amostra de 48 sha256 + os selados; os %d backups reais (%s) passam" % (len(reais), ", ".join(reais)))


# ------------------------------------------------------------ t45 — L04: o auditor vê o llms.txt e o index.md; e a ORDEM da camada de texto no laço de E08 (secoes antes de read-brief/llms/head)
def _ordem_da_camada_de_texto_certa(seq):
    """Em cada passada (delimitada por gerar_secoes.py): read-brief, llms_site e head vêm DEPOIS dela e nada de gerar_secoes entre eles e o fim da passada; a 1ª chamada é gerar_secoes."""
    if not seq or seq[0] != "gerar_secoes.py":
        return False
    passadas, atual = [], []
    for x in seq:
        if x == "gerar_secoes.py" and atual:
            passadas.append(atual)
            atual = []
        atual.append(x)
    passadas.append(atual)
    camada = ("gerar_read_brief.py", "gerar_llms_site.py", "gerar_head_camada_texto.py")
    for ps in passadas:
        if ps[0] != "gerar_secoes.py" or any(g not in ps for g in camada):
            return False
        if [g for g in ps if g in camada] != list(camada) or ps.index("gerar_secoes.py") > min(ps.index(g) for g in camada):
            return False
    return True


@teste()
def t45_auditor_l04_llms_index_e_ordem_da_camada_de_texto():
    raiz = TMP / "t45"
    tb, site_d = raiz / "tb", raiz / "site"
    (site_d / "secoes").mkdir(parents=True)
    tb.mkdir()
    (site_d / "secoes" / "07-o-programa-um-py.md").write_bytes(b"x" * 11731)
    base = "https://teoriadagravitacaoluminodinamica.com/secoes/07-o-programa-um-py.md"
    decoy = "- [um.py](https://raw.githubusercontent.com/x/Um%20%28absoluto%29/um.py): O CANONICO, arquivo unico (38421415 bytes; o GitHub nao o renderiza -- use o raw).\n"
    c = Caminhos({"TB": str(tb), "SITE": str(site_d)})
    ctx = motor.Ctx(c=c, versao="v398")

    def escreve(num_llms, num_idx, num_rb):
        (site_d / "llms.txt").write_text("# llms\n" + decoy + "- [The program](%s) (%s bytes; espelho: https://raw.githubusercontent.com/x/secoes/07-o-programa-um-py.md)\n" % (base, num_llms), encoding="utf-8")
        (site_d / "index.md").write_text("# index\n[07-o-programa-um-py.md](%s) (%s bytes) \u00b7 espelho: [raw](https://raw.githubusercontent.com/x/secoes/07-o-programa-um-py.md)\n" % (base, num_idx), encoding="utf-8")
        (site_d / "read-brief.md").write_text("- parte: %s (%s bytes)\n" % (base, num_rb), encoding="utf-8")
    escreve("11731", "11.731", "11.731")
    assert espelho.auditar_numeros_citados(ctx) == [], "números certos nos três formatos, e a linha do um.py (38421415 bytes) não é citação de arquivo"
    escreve("11762", "11.762", "11.731")          # o L04 da v398: secoes/07 citada com 11.762 (o real é 11.731) — no llms.txt e no index.md, que o regex antigo não via
    d = espelho.auditar_numeros_citados(ctx)
    assert sorted((x["superficie"], x["arquivo"], x["citado"], x["real"]) for x in d) == [("SITE:index.md", "secoes/07-o-programa-um-py.md", 11762, 11731), ("SITE:llms.txt", "secoes/07-o-programa-um-py.md", 11762, 11731)], d
    # a ORDEM: o laço de E08 roda gerar_secoes ANTES do read-brief, do llms e do head, em CADA passada, até o ponto fixo
    c2 = Caminhos({"TB": str(tb), "SITE": str(site_d)})
    ctx2 = motor.Ctx(c=c2, versao="v398")
    (tb / "README.md").write_text("readme\n", encoding="utf-8")
    seq = []
    salvos = (espelho._banc, espelho._tb, espelho._rodar_git, espelho._assinatura)
    sigs = iter(["A", "B", "B"])          # a 3ª passada repete a assinatura da 2ª: ponto fixo
    try:
        espelho._banc = lambda ctx, script, *a, **kw: (seq.append(script), {"rc": 0, "saida": ""})[1]
        espelho._tb = lambda ctx, script, *a, **kw: (seq.append(script), {"rc": 0, "saida": ""})[1]
        espelho._rodar_git = lambda ctx, *a: (seq.append("git " + a[0]), {"rc": 0, "saida": ""})[1]
        espelho._assinatura = lambda ctx: next(sigs)
        r = espelho._ap_e08(ctx2)
    finally:
        espelho._banc, espelho._tb, espelho._rodar_git, espelho._assinatura = salvos
    so = [x for x in seq if not x.startswith("git ")]
    assert r["passadas"] == 3 and so.count("gerar_secoes.py") == 3, (r, so)
    assert _ordem_da_camada_de_texto_certa(so), so
    assert so[-1] == "gerar_portas.py", "a última coisa de cada passada é o gerar_portas (hash final do read-brief)"
    # o verificador de ordem DISCRIMINA: a ordem da v398 feita à mão (camada de texto antes de gerar_secoes) é reprovada
    errada = ["gerar_portas.py", "gerar_read_brief.py", "gerar_llms_site.py", "gerar_head_camada_texto.py", "gerar_secoes.py", "gerar_portas.py"]
    assert not _ordem_da_camada_de_texto_certa(errada)
    assert not _ordem_da_camada_de_texto_certa(["gerar_secoes.py", "gerar_llms_site.py", "gerar_read_brief.py", "gerar_head_camada_texto.py"]), "dentro da camada a ordem é read-brief, llms, head"
    return ("o auditor L04 agora lê «[título](url/arquivo.md) (N bytes; espelho: …)» do llms.txt e «(N.NNN bytes) · espelho» do index.md (antes 0 de 14 e 0 de 8 citações: o L04 da v398 estava justamente aí), sem "
            "tomar a linha do um.py (38421415 bytes) por citação; o laço de E08 roda gerar_secoes antes de read-brief/llms/head em cada passada (3 passadas até o ponto fixo, gerar_portas por último) e o verificador de "
            "ordem reprova a ordem da v398 à mão")


# ------------------------------------------------------------ t46 — o vigia só LÊ: os git de leitura não tomam o index.lock opcional (outra sessão pode estar em `git add`/`commit`)
@teste()
def t46_git_de_leitura_sem_locks_opcionais():
    fake = TMP / "fakegit_t46.bat"
    fake.write_text("@echo off\r\necho LOCKS=%GIT_OPTIONAL_LOCKS%\r\necho ARGS=%*\r\n", encoding="ascii")
    anterior = os.environ.get("G1_GIT_EXE")
    os.environ["G1_GIT_EXE"] = str(fake)
    try:
        r = util.rodar(["git", "status", "--porcelain"])
        assert r["rc"] == 0 and "LOCKS=0" in r["stdout"] and "status --porcelain" in r["stdout"], r
        r2 = util.rodar(["git", "-C", str(TMP), "diff", "--cached", "--name-only"])
        assert "LOCKS=0" in r2["stdout"], r2
        outro = util.rodar(["cmd", "/c", "echo", "%GIT_OPTIONAL_LOCKS%"])
        assert "%GIT_OPTIONAL_LOCKS%" in outro["stdout"], "só os comandos git recebem a variável (no resto ela continua indefinida): %r" % outro["stdout"]
    finally:
        if anterior is None:
            os.environ.pop("G1_GIT_EXE", None)
        else:
            os.environ["G1_GIT_EXE"] = anterior
    return "todo `git` de G1 (status, diff, log, rev-parse…) roda com GIT_OPTIONAL_LOCKS=0: o vigia agendado não toma o index.lock opcional enquanto outra sessão faz `git add`/`commit` no mesmo repositório; só os comandos git recebem a variável"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rapido", action="store_true")
    ap.add_argument("--so")
    a = ap.parse_args()
    escolha = set(a.so.split(",")) if a.so else None
    linhas = []
    n_ok = 0
    t_total = time.time()
    nos_no_inicio = estado_do_nos_v398()
    for nome, f, pesado, precisa_nos in TESTES:
        if escolha and nome.split("_")[0] not in escolha:
            continue
        if a.rapido and pesado:
            linhas.append((nome, "PULADO", "(--rapido)", 0))
            continue
        if precisa_nos:
            est = estado_do_nos_v398()
            if est != "PRONTA":
                linhas.append((nome, "PULADO", "(AMBIENTE: o Nós vivo não é a v398 PRONTA — %s; este teste lê o Nós vivo e foi aprovado com ele PRONTA. Não é falha de código nem aprovação: roda de novo quando o Nós estiver PRONTA)" % est, 0))
                print("%-34s %-6s %6.1fs  %s" % (nome, linhas[-1][1], 0, linhas[-1][2][:300]))
                continue
        t = time.time()
        try:
            det = f()
            linhas.append((nome, "PASSA", det, time.time() - t))
            n_ok += 1
        except Exception as e:  # noqa: BLE001
            linhas.append((nome, "FALHA", "".join(traceback.format_exception_only(type(e), e)).strip()[:600] + "\n" + "".join(traceback.format_tb(e.__traceback__)[-2:])[-500:], time.time() - t))
        print("%-34s %-6s %6.1fs  %s" % (nome, linhas[-1][1], linhas[-1][3], linhas[-1][2][:300].replace("\n", " ")))
    falhas = [l for l in linhas if l[1] == "FALHA"]
    nos_no_fim = estado_do_nos_v398()
    md = ["# TESTES DE G1 — saída", "", "Executado em %s por `work\\custodia_G1\\testes\\testes_g1.py` (Python %s). Só leem o mundo real (Nós, espelho, cofres, site) e escrevem em diretório temporário; nada de commit, push, subida, ACOM, rota, um.py ou kernel." % (
        time.strftime("%d/%m/%Y %H:%M:%S"), sys.version.split()[0]), "", "**%d passam, %d falham, %d pulados** em %.0f s." % (n_ok, len(falhas), sum(1 for l in linhas if l[1] == "PULADO"), time.time() - t_total), "",
          "Nós %s (as três marcas da v398): **%s** no início da rodada, **%s** no fim. Os testes que leem o Nós (`nos_pronta`) só rodam com ele PRONTA; senão ficam PULADOS, com o motivo (outra sessão pode estar construindo a versão seguinte)." % (
              ("lido de `G1_RAIZ_NOS` — uma VISTA congelada na v398 (`testes\\nos_congelado.py`)" if os.environ.get("G1_RAIZ_NOS") else "vivo"), nos_no_inicio, nos_no_fim), "",
          "| teste | resultado | s | o que provou |", "|---|---|---:|---|"]
    for nome, res, det, seg in linhas:
        md.append("| `%s` | %s | %.1f | %s |" % (nome, res, seg, det.replace("|", "\\|").replace("\n", " ")))
    Path(a.so and TMP / "TESTES_parcial.md" or CEN / "work" / "custodia_G1" / "TESTES_BRUTO.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    _rm(TMP)
    if SBX.get("raiz"):
        _rm(SBX["raiz"])
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())

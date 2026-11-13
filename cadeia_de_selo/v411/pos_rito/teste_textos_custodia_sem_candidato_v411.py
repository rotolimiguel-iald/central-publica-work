# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411-posrito] REESCRITO para a v411: roda o S6d inteiro (textos_custodia_handoff_v411.main) contra um Nos SINTETICO de ensaio (fora de work\) e confere o handoff pelo parser do G1; o corpo da v410 fica no .bak.
"""teste_textos_custodia_sem_candidato_v411.py -- o teste POSSIVEL SEM CANDIDATO do S6d da v411. Monta em C:\\t\\k411c\\ensaio_topo_proposto\\pos_rito_textos\\ um Nos de ENSAIO (um.py falso e o selo dele; o core com o
registro h0dn_bg1_v411 do ensaio offline, o registro da Fase 9 V2, as bandeiras e a escada da v410 selada, e, SINTETICOS e ditos, kh_n1_cobertura_v411 (os numeros da v410) e cunhagens_v411 (as entradas do delta, de 12/11);
o diario com o cabecalho «v411 SELADA»; um HANDOFF minimo com o «O que e'») e uma pasta da cadeia de ensaio (ESPERADOS sintetico e um .tmp plantado). Roda main(); confere: rc 0; o .tmp removido; cada marcador lido pelo
parser do G1 igual ao recibo; o recibo nas chaves que o gatilho do orquestrador le. Controles negativos (TEM de recusar): registro nao aberto; diario sem o cabecalho; cunhagens com contagem errada; e, nas guardas, um
texto da abertura sem a linha das Cefeidas livres, um ARCO com aspa simples, um COMMIT com acento, «poder certificado». Nada no Nos real, no espelho, na Central nem na pasta da cadeia. rc 0 = passou."""
import copy
import hashlib
import json
import os
import shutil
import sys
import time
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent; PK = HERE.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(PK))
import textos_custodia_handoff_v411 as TC  # noqa: E402
from custodia_g1 import nos as NOSMOD  # noqa: E402

NOS_REAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
BASE = Path(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_textos")
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, det=""):
    if cond:
        RES["ok"] += 1
    else:
        RES["falhas"].append({"caso": nome, "detalhe": str(det)[:500]}); print("  FALHA", nome, str(det)[:300])


def escreve(p, b):
    p.parent.mkdir(parents=True, exist_ok=True)
    open(str(p) + ".tmpw", "wb").write(b); os.replace(str(p) + ".tmpw", p)


CORE10 = json.loads((NOS_REAL / "um_absoluto.json").read_bytes().decode("utf-8"))["core"]
REG = json.loads((PK / "TESTE_H0DN_OFFLINE_v411_registro.json").read_bytes().decode("utf-8"))


def montar_nos(rotulo, mut=None):
    d = BASE / rotulo
    if d.exists():
        shutil.rmtree(d)
    nos, pkg = d / "nos", d / "cadeia"
    um = b"# um.py de ENSAIO (nao e' o um.py da v411)\n"
    pin = hashlib.sha256(um).hexdigest()
    core = {k: copy.deepcopy(CORE10[k]) for k in ("teste_de_veracidade_fase9_v397", "kernel_formalization", "external_ladder", "estatuto_da_prova_v391")}
    core["h0dn_bg1_v411"] = copy.deepcopy(REG)
    core["kh_n1_cobertura_v411"] = copy.deepcopy(CORE10["kh_n1_cobertura_v410"])   # SINTETICO: os numeros da v410 no lugar dos da v411
    core["cunhagens_v411"] = {"verbatim": {"fala_%d" % i: {"quando": "12/11/2026 (ensaio)"} for i in range(TC.DL.N_FALAS_V411)}}   # SINTETICO: as entradas do delta (DL.N_FALAS_V411), de 12/11
    esc = core["external_ladder"]["n_theorems_clean"]
    if mut:
        mut(core)
    selo = {"um_version": "v411", "sha256": {"um.py": pin}, "fail_closed_selftest": "FAIL_CLOSED_SELFTEST_PASSED", "timestamp": "2026-11-12 23:59:59"}
    escreve(nos / "um.py", um)
    escreve(nos / "um_absoluto.json", json.dumps({"core": core}, ensure_ascii=False).encode("utf-8"))
    escreve(nos / "um_absoluto_selo.json", json.dumps(selo, ensure_ascii=False).encode("utf-8"))
    cab = "## 12/11/2026 — **v411 SELADA** `%s` — O teste decisivo (v411): nenhum módulo novo, escada %d → %d (ENSAIO)\n" % (pin[:16], esc, esc)
    escreve(nos / "MEMORIA_DA_LINHAGEM.md", ("# diario de ENSAIO\n\n" + cab + "\nfim\n").encode("utf-8"))
    escreve(nos / "HANDOFF_v411_CUSTODIA.md", ("# HANDOFF v411 — CUSTÓDIA (ENSAIO)\n\n**O que é:** `um.py` **v411** `%s` (44 B) sobre a v410 `5d9497a721c3589e`; %d/%d; COMPLETA; rc 0; selftest PASSED; gate intocado; ensaio.\n\n"
                                                   "Corpo de ensaio.\n" % (pin[:16], esc, esc)).encode("utf-8"))
    escreve(pkg / "ESPERADOS_v411.json", json.dumps({"candidato_sha16": pin[:16], "vereditos_novos_v411": {"h0dn_bg1_v411": REG["verdict"]}}).encode("utf-8"))
    escreve(pkg / "lixo_plantado.tmp", b"x")
    return d, nos, pkg, pin


# ---- 1. o positivo
d, nos, pkg, pin = montar_nos("positivo")
t0 = time.time()
rc = TC.main(nos, pkg, d)
caso("main() rc 0 no Nos de ensaio", rc == 0, rc)
rec = json.loads((d / TC.NOME_RECIBO).read_text(encoding="utf-8")) if (d / TC.NOME_RECIBO).exists() else {}
caso("o .tmp plantado foi removido e dito", not (pkg / "lixo_plantado.tmp").exists() and any("lixo_plantado.tmp" in x for x in (rec.get("notas_info") or {}).get("tmp_removidos", [])))
h = NOSMOD.ler_handoff(types.SimpleNamespace(NOS=nos, CEN=Path(r"C:\IALD\Central de Patentes")), "v411")
esper = list(TC.MARCADORES_PROSA) + list(TC.MARCADORES_ABERTURA)
caso("o parser do G1 le todos os marcadores (os sete, os da abertura e os extras), sem problema", h is not None and not h.problemas and all("%s_v411" % i in h.corpos for i in esper), (h.problemas if h else None))
caso("cada corpo lido e' o do recibo", all(h.corpos["%s_v411" % i].strip("\n") == rec["textos"][i] for i in esper))
caso("o recibo traz sha16_depois = o do handoff", rec.get("sha16_depois") == hashlib.sha256((nos / "HANDOFF_v411_CUSTODIA.md").read_bytes()).hexdigest()[:16])
caso("as guardas do recibo estao limpas em todo texto", all(not (g["guarda_frases_v411"] or g["portao_g1"] or g["forma"] or g["custodia_h0dn"]) for g in rec.get("guardas", {}).values()))
caso("a secao README (v411) esta' no handoff, antes dos marcadores da abertura", 0 <= (nos / "HANDOFF_v411_CUSTODIA.md").read_text(encoding="utf-8").find(TC.SECAO_README) < (nos / "HANDOFF_v411_CUSTODIA.md").read_text(encoding="utf-8").find("<!-- INICIO_NOTA_EN_v411 -->"))
caso("os textos sao os RATIFICADOS (TOPO_RATIFICADO_v411.json; nao proposta)", rec.get("formula", {}).get("proposta") is False and "TOPO_RATIFICADO_v411.json" in str(rec.get("formula", {}).get("origem")))
caso("a nota da cadeia diz a contagem e os contratos fora da escada", "contagem esperada" in rec.get("notas_da_cadeia", "") and "_V411_H0DN_CONTRACT" in rec.get("notas_da_cadeia", ""))
caso("o backup de bytes do handoff existe e e' o original", any(p.name.startswith("HANDOFF_v411_CUSTODIA.md.bak_") for p in nos.iterdir()))
try:
    TC.main(nos, pkg, d); caso("rodar de novo RECUSA (o marcador ja existe)", False, "rodou de novo")
except AssertionError as e:
    caso("rodar de novo RECUSA (o marcador ja existe)", "ja existe" in str(e), e)

# ---- 2. controles negativos de entrada (TEM de recusar, sem escrever)
for rot, mut, quer in (("registro_nao_aberto", lambda c: c["h0dn_bg1_v411"].__setitem__("opened_once", False), "nao selou"),
                       ("cunhagens_errada", lambda c: c["cunhagens_v411"]["verbatim"].pop("fala_0"), "falas"),
                       ("checagens_erradas", lambda c: c["h0dn_bg1_v411"]["mechanics"].__setitem__("n_checks", 15), "checagens")):
    d2, nos2, pkg2, _ = montar_nos(rot, mut)
    h0 = (nos2 / "HANDOFF_v411_CUSTODIA.md").read_bytes()
    try:
        TC.main(nos2, pkg2, d2); caso("controle negativo %s RECUSA" % rot, False, "rodou")
    except (AssertionError, ValueError) as e:
        caso("controle negativo %s RECUSA sem escrever" % rot, quer in str(e) and (nos2 / "HANDOFF_v411_CUSTODIA.md").read_bytes() == h0, e)
d3, nos3, pkg3, _ = montar_nos("sem_cabecalho")
escreve(nos3 / "MEMORIA_DA_LINHAGEM.md", b"# diario sem o cabecalho\n")
try:
    TC.main(nos3, pkg3, d3); caso("controle negativo: diario sem o cabecalho RECUSA", False, "rodou")
except AssertionError as e:
    caso("controle negativo: diario sem o cabecalho RECUSA", "cabecalho" in str(e), e)

# ---- 3. controles negativos das guardas
T = dict(rec["textos"]); core_t = json.loads((nos / "um_absoluto.json").read_bytes().decode("utf-8"))["core"]
cf = REG["values"]["cefeidas_livres"]; zc = "%.2f" % cf["z_null"]
assert ("beside it, free Cepheids give %sσ, below 5; " % zc) in T["ENTROU_EN"] and ("; beside it, free Cepheids give %sσ, below 5" % zc) in T["README_RITOS"], "os controles nao acham a oracao das Cefeidas"
for rot, ident, txt, quer in (
        ("ENTROU_EN sem as Cefeidas livres", "ENTROU_EN", T["ENTROU_EN"].replace("beside it, free Cepheids give %sσ, below 5; " % zc, ""), "cefeidas"),
        ("README_RITOS sem as Cefeidas livres", "README_RITOS", T["README_RITOS"].replace("; beside it, free Cepheids give %sσ, below 5" % zc, ""), "cefeidas"),
        ("ARCO_PT com aspa simples", "ARCO_PT", T["ARCO_PT"] + " d'agua", "aspa"),
        ("COMMIT com acento", "COMMIT", T["COMMIT"] + " já", "ASCII"),
        ("ABERTOS_EN com poder certificado", "ABERTOS_EN", T["ABERTOS_EN"] + " The test has certified power.", "F61")):
    g, f = TC.guardas_dos_textos([(ident, txt)], set(), core_t)
    caso("controle negativo das guardas: %s" % rot, bool(f) and quer.lower() in json.dumps(g, ensure_ascii=False).lower(), g)

out = {"contrato": "TESTE_TEXTOS_CUSTODIA_SEM_CANDIDATO_v411", "quando": time.strftime("%Y-%m-%dT%H:%M:%S"), "ok": RES["ok"], "falhas": RES["falhas"], "TUDO_PASSOU": not RES["falhas"],
       "ensaio": str(BASE), "sintetico": "um.py, selo, diario, HANDOFF minimo, ESPERADOS, kh_n1_cobertura_v411 (numeros da v410) e cunhagens_v411 (as entradas do delta) sao de ENSAIO; o registro h0dn_bg1_v411 e' o do ensaio offline",
       "handoff_de_ensaio": str(nos / "HANDOFF_v411_CUSTODIA.md"), "bytes_do_acrescimo": (nos / "HANDOFF_v411_CUSTODIA.md").stat().st_size}
escreve(BASE / "TESTE_TEXTOS_CUSTODIA_SEM_CANDIDATO_v411.json", json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
print("teste do S6d sem candidato: %d ok, %d falha(s); saida %s" % (RES["ok"], len(RES["falhas"]), BASE / "TESTE_TEXTOS_CUSTODIA_SEM_CANDIDATO_v411.json"))
sys.exit(0 if not RES["falhas"] else 1)

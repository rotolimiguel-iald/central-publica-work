# -*- coding: utf-8 -*-
"""guardas_estaticas_bancada_v401.py -- LICAO da v400, MANTIDA na v401 (a v399 passou o ensaio a seco e foi recusada pela Bancada: ALPHA_LINHA_NAO_UNICA): o ensaio a seco da cadeia roda, sobre o CANDIDATO e ANTES de instalar, as guardas ESTATICAS do esboco
R3.5 da Bancada -- as que nao dependem do selo -- chamando a FUNCAO DELE (`ler_nos`), importada do esboco pinado por sha256 (nada copiado, nada reimplementado): a mesma leitura que o B(n) fara no Nos depois do rito.
Como: monta, em sandbox curto (C:\\t\\vb18\\gate_*), uma pasta com a forma de um Nos (o um.py, um selo MINIMO que o pina e diz a versao, e um core MINIMO com o beta do core real da v399 selada: o alfa nao muda) e chama `ler_nos(pasta, versao)`.
Cobre: CANONICAL_DECLARATION_MISSING, UM_VERSION_DIFERENTE_DO_ALVO, ALPHA_LINHA_NAO_UNICA, ALPHA_REATRIBUIDA_INDENTADA, UM_VERSION_LINHA_NAO_UNICA, UM_VERSION_REATRIBUIDA_INDENTADA, ALPHA_OUTSIDE_CONTRACT e BETA_CORE_DIVERGE_DO_RUNTIME
(a mesma funcao); mais as duas regexes do canonical.py INSTALADO na Bancada (a primeira linha de versao e de alfa que ele le tem de ser a do esboco).
CONTROLES: (i) a v399 SELADA (o defeito real) tem de ser RECUSADA com a mensagem EXATA que o recibo da Bancada registrou (RECUSA_SINCRONIZACAO_v399_*.json); (ii) o candidato com uma segunda linha de alfa na coluna 0, com alfa reatribuido indentado,
com UM_VERSION duplicado, de outra versao, com alfa fora do contrato e com o beta do core errado tem de ser RECUSADO, cada um pelo codigo certo. Nada e' escrito fora do sandbox e da saida; a producao e o Nos nao sao tocados.
uso: python -I -B -X utf8 guardas_estaticas_bancada_v401.py [um.py_candidato] [saida.json]   (rc 0 so' se o candidato passa E todos os controles recusam)"""
import hashlib, json, os, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402
import acom_conferencias_v401 as AC  # noqa: E402
from pathlib import Path  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
RECUSA_V399 = os.path.join(DL.V399, "bancada_B3_ensaio_20261024_162108", "RECUSA_SINCRONIZACAO_v399_20261024_162108.json")
CANONICAL = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "bancada", "canonical.py")
cand_p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, DL.CANDIDATO)
saida_p = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "GUARDAS_ESTATICAS_BANCADA_v401.json")
MOD = AC.esboco_da_bancada(ESBOCO, ESBOCO_SHA256)
RX = AC.regexes_da_bancada(ESBOCO, ESBOCO_SHA256)
base_um = open(os.path.join(DL.V400, "base_v399", "um.py"), "rb").read()   # a v399 SELADA (o defeito real): copia de bytes guardada pela cadeia v400
cand = open(cand_p, "rb").read()
beta_core = json.load(open(os.path.join(HERE, DL.BASE_DIR, "um_absoluto.json"), encoding="utf-8"))["core"]["beta"]
SB = os.path.join(DL.SANDBOX_CURTO, "gate")
if os.path.isdir(SB):
    shutil.rmtree(SB)
os.makedirs(SB)


def montar(nome, um_bytes, versao_no_selo, beta=None):
    d = os.path.join(SB, nome); os.makedirs(d)
    open(os.path.join(d, "um.py"), "wb").write(um_bytes)
    json.dump({"um_version": versao_no_selo, "sha256": {"um.py": sha(um_bytes)}}, open(os.path.join(d, "um_absoluto_selo.json"), "w", encoding="utf-8"))
    json.dump({"core": {"beta": beta_core if beta is None else beta}}, open(os.path.join(d, "um_absoluto.json"), "w", encoding="utf-8"))
    return d


def rodar(nome, um_bytes, versao_alvo, versao_no_selo=None, beta=None):
    d = montar(nome, um_bytes, versao_no_selo or versao_alvo, beta)
    try:
        info = MOD.ler_nos(Path(d), versao_alvo)
        return {"passou": True, "recusa": None, "alpha": info["alpha"], "um_version_linhas": info["um_version_linhas"], "UM_VERSION": info["UM_VERSION"], "beta_runtime": info["beta_runtime"], "beta_rel_diff": info["core"]["beta_rel_diff"], "um_py_sha16": info["um_py"]["sha256"][:16]}
    except MOD.Recusa as e:
        return {"passou": False, "recusa": str(e), "alpha": None}


def com_texto(t, velho, novo):
    assert t.count(velho) == 1, ("ancora do mutante nao unica", velho[:60], t.count(velho))
    return t.replace(velho, novo)


tc = cand.decode("utf-8")
ancora_alfa = "ALPHA_FINE_CODATA_2018 = 7.2973525693e-3\r\n"
res = {"contrato": "GUARDAS_ESTATICAS_BANCADA_v401", "esboco": {"path": ESBOCO, "sha256": ESBOCO_SHA256, "revisao": MOD.REVISAO, "funcao": "ler_nos"}, "candidato": {"path": cand_p, "sha16": sha(cand)[:16], "bytes": len(cand)}}
# 1. o candidato passa a mesma leitura que o B(n) fara (versao v401)
res["candidato_v401"] = rodar("candidato", cand, "v401")
# 2. o defeito real: a v399 selada tem de ser recusada com a MENSAGEM EXATA do recibo da Bancada
rv = json.load(open(RECUSA_V399, encoding="utf-8"))
res["v399_selada_o_defeito_real"] = rodar("v399", base_um, "v399")
res["v399_selada_o_defeito_real"]["recusa_do_recibo_da_bancada"] = rv["recusa"]
res["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"] = res["v399_selada_o_defeito_real"]["recusa"] == rv["recusa"]
# 3. controles negativos: cada mutante do candidato e' recusado pelo codigo certo
nulos = {}
nulos["alfa_segunda_linha_na_coluna_0"] = (rodar("m1", cand + b"ALPHA_FINE_CODATA_2018 = 0.0072973525693\r\n", "v401"), "ALPHA_LINHA_NAO_UNICA")
nulos["alfa_reatribuido_indentado"] = (rodar("m2", cand + b"if True:\r\n    ALPHA_FINE_CODATA_2018 = 0.0072973525693\r\n", "v401"), "ALPHA_REATRIBUIDA_INDENTADA")
nulos["alfa_sem_a_linha"] = (rodar("m3", cand.replace(ancora_alfa.encode(), b"ALPHA_X = 7.2973525693e-3\r\n", 1), "v401"), "CANONICAL_DECLARATION_MISSING")
nulos["um_version_duplicado"] = (rodar("m4", cand + b'UM_VERSION = "v401"\r\n', "v401"), "UM_VERSION_LINHA_NAO_UNICA")
nulos["um_version_reatribuido_indentado"] = (rodar("m5", cand + b'if True:\r\n    UM_VERSION = "v401"\r\n', "v401"), "UM_VERSION_REATRIBUIDA_INDENTADA")
nulos["versao_do_um_py_diferente_do_alvo"] = (rodar("m6", cand, "v402", versao_no_selo="v402"), "UM_VERSION_DIFERENTE_DO_ALVO")
nulos["alfa_fora_do_contrato"] = (rodar("m7", cand.replace(ancora_alfa.encode(), b"ALPHA_FINE_CODATA_2018 = 1.5\r\n", 1), "v401"), "ALPHA_OUTSIDE_CONTRACT")
nulos["beta_do_core_diverge_do_runtime"] = (rodar("m8", cand, "v401", beta=beta_core * (1 + 1e-6)), "BETA_CORE_DIVERGE_DO_RUNTIME")
nulos["selo_nao_pina_o_um_py"] = None
d9 = montar("m9", cand, "v401"); json.dump({"um_version": "v401", "sha256": {"um.py": "0" * 64}}, open(os.path.join(d9, "um_absoluto_selo.json"), "w", encoding="utf-8"))
try:
    MOD.ler_nos(Path(d9), "v401"); nulos["selo_nao_pina_o_um_py"] = ({"passou": True, "recusa": None}, "SELO_NAO_PINA_O_UM_PY_DO_DISCO")
except MOD.Recusa as e:
    nulos["selo_nao_pina_o_um_py"] = ({"passou": False, "recusa": str(e)}, "SELO_NAO_PINA_O_UM_PY_DO_DISCO")
res["controles_negativos"] = {k: {"recusa": r["recusa"], "esperado_comeca_por": cod, "ok": (not r["passou"]) and str(r["recusa"]).startswith(cod)} for k, (r, cod) in nulos.items()}
# 4. as duas regexes do canonical.py INSTALADO na Bancada (a primeira linha que ELE le), contra o candidato
csrc = open(CANONICAL, "rb").read().decode("utf-8")
mv = re.search(r"v = re\.search\(r'(.+?)', text, re\.M\)", csrc); ma = re.search(r"a = re\.search\(r'(.+?)', text, re\.M\)", csrc)
assert mv and ma, "as regexes do canonical.py instalado nao foram achadas"
cv, ca = re.compile(mv.group(1), re.M).search(tc), re.compile(ma.group(1), re.M).search(tc)
res["canonical_py_instalado"] = {"path": CANONICAL, "sha256": sha(open(CANONICAL, "rb").read()), "regex_versao": mv.group(1), "regex_alfa": ma.group(1), "le_versao": cv.group(1) if cv else None, "le_alfa": ca.group(1) if ca else None,
                                 "linha_do_alfa_que_ele_le": (tc[:ca.start()].count("\n") + 1) if ca else None, "igual_ao_do_esboco": bool(cv and ca and cv.group(1) == RX["RE_VERSAO"].search(tc).group(1) and ca.group(1) == RX["RE_ALPHA"].search(tc).group(1))}
res["canonical_py_instalado"]["ok"] = res["canonical_py_instalado"]["le_versao"] == "v401" and res["canonical_py_instalado"]["le_alfa"] == "7.2973525693e-3" and res["canonical_py_instalado"]["igual_ao_do_esboco"]
# 5. a unicidade pela contagem direta (as regexes DO esboco), e onde esta a unica linha de alfa
res["contagem_direta"] = {"alfa_col0": len(RX["RE_ALPHA_LINHAS"].findall(tc)), "alfa_indentada": len(RX["RE_ALPHA_INDENTADA"].findall(tc)), "versao_col0": len(RX["RE_VERSAO_LINHAS"].findall(tc)), "versao_indentada": len(RX["RE_VERSAO_INDENTADA"].findall(tc))}
res["veredito"] = ("GUARDAS_ESTATICAS_DA_BANCADA__CANDIDATO_PASSA__DEFEITO_REAL_DA_V399_REPRODUZIDO__CONTROLES_NEGATIVOS_TODOS_RECUSAM"
                   if (res["candidato_v401"]["passou"] and res["candidato_v401"]["alpha"]["n_linhas_nao_indentadas"] == 1 and res["candidato_v401"]["alpha"]["n_reatribuicoes_indentadas"] == 0
                       and (not res["v399_selada_o_defeito_real"]["passou"]) and res["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"]
                       and all(v["ok"] for v in res["controles_negativos"].values()) and res["canonical_py_instalado"]["ok"]
                       and res["contagem_direta"] == {"alfa_col0": 1, "alfa_indentada": 0, "versao_col0": 1, "versao_indentada": 0}) else "REPROVADO")
shutil.rmtree(SB)
res["sandbox_apagado"] = not os.path.exists(SB)
json.dump(res, open(saida_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(res["veredito"])
print("candidato:", {k: res["candidato_v401"][k] for k in ("passou", "alpha", "um_version_linhas", "UM_VERSION", "beta_rel_diff")})
print("v399 selada:", res["v399_selada_o_defeito_real"]["recusa"], "| identica a do recibo:", res["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"])
print("controles:", {k: v["ok"] for k, v in res["controles_negativos"].items()})
sys.exit(0 if res["veredito"] != "REPROVADO" else 1)

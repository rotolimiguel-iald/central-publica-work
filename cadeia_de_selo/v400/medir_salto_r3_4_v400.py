# -*- coding: utf-8 -*-
"""medir_salto_r3_4_v400.py -- SO LEITURA. MEDE (nao le do codigo) se o SALTO declarado R3.4 (cadeia de selos v398 -> v399, para a Bancada que pina a v398) e' possivel com o esboco R3.5 pinado, e se um recibo pre_selo NOVO e' possivel com o Nos de hoje:
 (1) carregar_cadeia_de_selos(CADEIA_DE_SELOS_v400_TENTATIVA.json, sha256) -- a cadeia v398 -> v399 gerada por gerar_cadeia_de_selos.py a partir das copias de bytes da custodia -- tem de ser RECUSADA no elo v399 (CADEIA_DE_SELOS_UM_PY_COM_DECLARACAO_NAO_UNICA: o um.py v399 tem
     duas linhas de alfa na coluna 0); o mesmo carregamento, com o elo v399 trocado pelo candidato v400, mostra que o problema e' o elo v399 e nao a cadeia (o elo v400 passa na guarda de unicidade do elo);
 (2) ler_nos(Nos real, "v399") -- o que o pre_selo de um salto leria -- RECUSA com a mensagem do recibo da Bancada (ALPHA_LINHA_NAO_UNICA: 2 linhas nao indentadas); ler_nos(Nos real, "v398") RECUSA (SELO_VERSAO_DIFERENTE): nenhum recibo pre_selo NOVO e' possivel sem tocar no Nos;
 (3) o que SOBRA dentro do esboco sem alteracao: o passo simples v398 -> v400 com o recibo pre_selo da cadeia v399 (conferencia_pelo_esboco_v400.json: aceito).
Escreve SALTO_R3_4_MEDIDO_v400.json em salto_r3_4\\. Le o Nos e a producao; nao escreve em nenhum dos dois.
uso: python -I -B -X utf8 medir_salto_r3_4_v400.py"""
import hashlib, json, os, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
import acom_conferencias_v400 as AC  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
ESBOCO = os.path.join(DL.WK, "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py")
ESBOCO_SHA256 = "02b22ba5c6d35c71922ae2f23939acc1c8f2283e8607bca31c4ff5b663fc36bf"
MOD = AC.esboco_da_bancada(ESBOCO, ESBOCO_SHA256)
SD = os.path.join(HERE, "salto_r3_4")
CAD = os.path.join(SD, "CADEIA_DE_SELOS_v400_TENTATIVA.json")
cad_b = open(CAD, "rb").read()
res = {"contrato": "SALTO_R3_4_MEDIDO_v400", "esboco": {"path": ESBOCO, "sha256": ESBOCO_SHA256, "revisao": MOD.REVISAO}, "cadeia_tentativa": {"path": CAD, "sha256": sha(cad_b), "bytes": len(cad_b)}}
# (1) a cadeia v398 -> v399 (o salto declarado) e' recusada no elo v399
try:
    MOD.carregar_cadeia_de_selos(CAD, sha(cad_b))
    res["cadeia_v398_v399"] = {"aceita": True, "recusa": None}
except MOD.Recusa as e:
    res["cadeia_v398_v399"] = {"aceita": False, "recusa": str(e)}
# o mesmo, com o elo v399 trocado pelo candidato v400 (so' para provar que a recusa e' do um.py v399): uma cadeia v398 -> v400 e' consecutiva? NAO (falta o v399); entao compara-se so' a guarda de unicidade do elo
cand = open(os.path.join(HERE, DL.CANDIDATO), "rb").read().decode("utf-8-sig")
res["guarda_de_unicidade_do_elo"] = {"v399_selada": {"alfa_col0": len(MOD.RE_ALPHA_LINHAS.findall(open(os.path.join(HERE, DL.BASE_DIR, "um.py"), "rb").read().decode("utf-8-sig"))), "passa": False},
                                      "candidato_v400": {"alfa_col0": len(MOD.RE_ALPHA_LINHAS.findall(cand)), "passa": len(MOD.RE_ALPHA_LINHAS.findall(cand)) == 1 and not MOD.RE_ALPHA_INDENTADA.search(cand)
                                                         and len(MOD.RE_VERSAO_LINHAS.findall(cand)) == 1 and not MOD.RE_VERSAO_INDENTADA.search(cand)}}
# (2) o que um pre_selo NOVO leria: o Nos de hoje
for v in ("v399", "v398"):
    try:
        MOD.ler_nos(Path(DL.NOS), v)
        res["ler_nos_" + v] = {"aceita": True, "recusa": None}
    except MOD.Recusa as e:
        res["ler_nos_" + v] = {"aceita": False, "recusa": str(e)}
rec = json.load(open(os.path.join(DL.V399, "bancada_B3_ensaio_20261024_162108", "RECUSA_SINCRONIZACAO_v399_20261024_162108.json"), encoding="utf-8"))
res["ler_nos_v399"]["identica_a_do_recibo_da_bancada"] = res["ler_nos_v399"]["recusa"] == rec["recusa"]
# (3) o que sobra: o passo simples com o recibo pre_selo da cadeia v399
conf = json.load(open(os.path.join(HERE, "bateria_pre_selo", "conferencia_pelo_esboco_v400.json"), encoding="utf-8"))
res["passo_simples_v398_v400"] = {"esboco_aceita_o_recibo_pre_selo": conf["esboco_aceita"], "condicoes": "%d/%d" % (conf["n_condicoes_ok"], conf["n_condicoes"]), "controles": "%d/%d" % (conf["n_controles_como_esperado"], len(conf["controles_negativos"])),
                                  "utilizavel": conf["utilizavel_como_recibo_pre_selo_do_B_n"]}
res["leitura_do_codigo_T17"] = {"onde": "sincronizar_bancada.py::verificar_kernel_recibo, linha `if not isinstance(pedras, list) or not pedras: return falha(\"pedras vazias\")`", "consequencia": "um B(n) cujo ANTES e' o kernel da v399 (o fim do salto) teria o diff do kernel VAZIO e o T17 recusaria; no passo simples v398 -> v400 o ANTES e' o kernel da v398 e o diff e' a pedra Testemunho",
                                "estatuto": "[REAL: lido do codigo do esboco, nao executado; o T17 precisa do selo e do manifesto reais]"}
res["veredito"] = ("SALTO_R3_4_IMPOSSIVEL_COM_O_ESBOCO_R3_5__PASSO_SIMPLES_V398_V400_ACEITO"
                   if (not res["cadeia_v398_v399"]["aceita"] and "CADEIA_DE_SELOS_UM_PY_COM_DECLARACAO_NAO_UNICA" in str(res["cadeia_v398_v399"]["recusa"]) and not res["ler_nos_v399"]["aceita"] and res["ler_nos_v399"]["identica_a_do_recibo_da_bancada"]
                       and not res["ler_nos_v398"]["aceita"] and res["guarda_de_unicidade_do_elo"]["candidato_v400"]["passa"] and res["passo_simples_v398_v400"]["esboco_aceita_o_recibo_pre_selo"] and res["passo_simples_v398_v400"]["utilizavel"])
                   else "MEDICAO_NAO_CONFIRMOU")
dest = os.path.join(SD, "SALTO_R3_4_MEDIDO_v400.json")
json.dump(res, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(res["veredito"])
print("cadeia v398->v399:", res["cadeia_v398_v399"]); print("ler_nos v399:", res["ler_nos_v399"]); print("ler_nos v398:", res["ler_nos_v398"]); print("elo:", res["guarda_de_unicidade_do_elo"])
sys.exit(0 if res["veredito"].startswith("SALTO_R3_4_IMPOSSIVEL") else 1)

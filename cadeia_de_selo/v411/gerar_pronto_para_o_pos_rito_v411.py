# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] o PRONTO_PARA_O_POS_RITO.json: a frente pos-rito espera por ele para rodar os harnesses (os caminhos e os sha16 LIDOS de cada arquivo)
"""gerar_pronto_para_o_pos_rito_v411.py -- grava C:\\t\\k411c\\ensaio_topo_proposto\\PRONTO_PARA_O_POS_RITO.json (o caminho que a gerencia pediu, nos dois modos) com as chaves que os harnesses da frente pos-rito LEEM
(PEDIDOS_ENTRE_FRENTES_v411.md, frente H, item 1): falso_nos, dry, core, selo, stdout, artigo_pt, artigo_en, esperados, manifesto, ensaio_a_seco, pinos_bn, formal_map, artefato, artefato_sha16 (cada caminho conferido no disco) e,
ao lado, o sha16 LIDO de cada arquivo. Modo: sem V411_ENSAIO_TOPO_PROPOSTO, "cadeia real" (o CANDIDATO real e as saidas da pasta da cadeia; o dry e o falso Nos fora de work, D135); com a variavel, "ensaio do topo proposto" (o
artefato de ENSAIO, que NAO e' candidato). Fail-closed: so' grava se o ensaio a seco disse TUDO PASSOU para ESTE arquivo, se os ESPERADOS sao dele e se o falso Nos e o dry trazem o um.py dele (o teste_conferidor_positivo rodou).
Backup de BYTES se o arquivo ja' existir. uso: python -B -X utf8 gerar_pronto_para_o_pos_rito_v411.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
sha16 = lambda p_: hashlib.sha256(open(p_, "rb").read()).hexdigest()[:16]
ens = json.load(open(DL.saida("ensaio_a_seco_v411.json"), encoding="utf-8")); man = json.load(open(DL.MANIFESTO_ARQ, encoding="utf-8")); esp = json.load(open(DL.saida("ESPERADOS_v411.json"), encoding="utf-8"))
art16 = sha16(DL.CANDIDATO_ARQ)
assert ens.get("veredito") == "TUDO PASSOU" and ens.get("sha16") == man["sha16"] == art16, ("o ensaio a seco nao passou para este arquivo", ens.get("veredito"), ens.get("sha16"), art16)
assert esp.get("candidato_sha16") == art16, ("os ESPERADOS nao sao deste arquivo", esp.get("candidato_sha16"), art16)
FN = DL.FALSO_NOS_DIR; DRY = DL.DRY_DIR
assert sha16(os.path.join(FN, "um.py")) == art16 and sha16(os.path.join(DRY, "um.py")) == art16, "o falso Nos ou o dry nao trazem o um.py deste arquivo (rode teste_conferidor_positivo_v411.py)"
pos_p = DL.saida("conferencia_rito_v411_POSITIVO_FALSO_NOS.json"); pos = json.load(open(pos_p, encoding="utf-8")) if os.path.exists(pos_p) else None
CAM = {"falso_nos": FN, "dry": DRY, "core": os.path.join(FN, "um_absoluto.json"), "selo": os.path.join(FN, "um_absoluto_selo.json"), "stdout": os.path.join(FN, "rodada_v411_stdout.txt"),
       "artigo_pt": os.path.join(FN, "um_absoluto_pt.txt"), "artigo_en": os.path.join(FN, "um_absoluto_en.txt"), "esperados": DL.saida("ESPERADOS_v411.json"), "manifesto": DL.MANIFESTO_ARQ,
       "ensaio_a_seco": DL.saida("ensaio_a_seco_v411.json"), "pinos_bn": DL.saida("PINOS_BN_v411.json"), "formal_map": DL.FORMAL_MAP_ARQ, "artefato": DL.CANDIDATO_ARQ}
faltam = [k_ for k_, p_ in CAM.items() if not os.path.exists(p_)]
assert not faltam, ("caminho ausente no disco (os harnesses recusariam rc 4)", faltam)
EXTRA = {"core_do_ensaio": os.path.join(DRY, "core_ensaio.json"), "selo_do_ensaio": os.path.join(DRY, "selo_ensaio.json"), "sidecar": os.path.join(FN, "um_absoluto_selo_acom.json"),
         "md_canonico": os.path.join(DRY, "um_absoluto_forma_canonica.md"), "md_manifesto": os.path.join(DRY, "um_absoluto_manifest.md")}
for l_ in ("pt", "en"):
    for ext_ in ("tex", "txt", "toc", "pdf"):
        EXTRA["artigo_%s_%s_do_dry" % (l_, ext_)] = os.path.join(DRY, "dry_v411_%s.%s" % (l_, ext_))
EXTRA = {k_: p_ for k_, p_ in EXTRA.items() if os.path.exists(p_)}
sha = {k_: (sha16(p_) if os.path.isfile(p_) else None) for k_, p_ in list(CAM.items()) + list(EXTRA.items())}
modo = "ensaio do topo proposto" if DL.ENSAIO_TOPO_PROPOSTO else "cadeia real"
# as citacoes como estao AGORA (o JSON do conferir_citacoes_v411.py --candidato, lido do disco; o que o ensaio a seco mediu na hora dele vai ao lado, em citacoes_no_ensaio_a_seco)
_cit_p = DL.saida("conferir_citacoes_v411.json"); _cit = json.load(open(_cit_p, encoding="utf-8")) if os.path.exists(_cit_p) else {}
CIT_AGORA = {"arquivo": _cit_p, "sha16": sha16(_cit_p) if os.path.exists(_cit_p) else None, "ok": _cit.get("ok"), "ok_do_um_py": _cit.get("ok_do_um_py"), "ok_do_pos_rito": _cit.get("ok_do_pos_rito"),
             "nao_verbatim_do_um_py": _cit.get("nao_verbatim_do_um_py"), "nao_verbatim_do_pos_rito": _cit.get("nao_verbatim_do_pos_rito"), "regra_do_pos_rito": _cit.get("regra_do_pos_rito")}
R = dict(CAM, **{"contrato": "PRONTO_PARA_O_POS_RITO_v411", "modo": modo, "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v411 (retomada, fork C)", "artefato_sha16": art16,
                 "candidato_sha16" if not DL.ENSAIO_TOPO_PROPOSTO else "artefato_de_ensaio_sha16": art16, "extras": EXTRA, "sha16_lido": sha, **DL.MARCA_ENSAIO,
                 "nota": ("CADEIA REAL: o candidato um_v411_candidato.py (com o texto RATIFICADO do topo); o core, o selo e o stdout do falso Nos sao EMULADOS a partir do ensaio a seco (nao do rito); nada instalado; nada no Nos"
                          if not DL.ENSAIO_TOPO_PROPOSTO else "ENSAIO do topo PROPOSTO: o artefato NAO e' candidato; nao se instala; o hash nao entra na pasta da cadeia"),
                 "ensaio_a_seco_veredito": ens.get("veredito"), "conferidor_positivo": {"tudo_bate": (pos or {}).get("tudo_bate"), "arquivo": pos_p if pos else None},
                 "citacoes": CIT_AGORA, "citacoes_no_ensaio_a_seco": ens.get("citacoes")})
p = os.path.join(DL.ENSAIO_DIR, "PRONTO_PARA_O_POS_RITO.json"); os.makedirs(DL.ENSAIO_DIR, exist_ok=True)
b = json.dumps(R, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(p):
    open(p + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(open(p, "rb").read())
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("gravado:", p, "| modo:", modo, "| sha16:", art16, "| chaves:", len(CAM))

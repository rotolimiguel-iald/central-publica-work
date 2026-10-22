# -*- coding: utf-8 -*-
"""_entrega_v386_pacote.py -- SO LEITURA: sha256 e bytes de cada entregavel do pacote v386 (lidos do disco), + os numeros do ensaio/esperados; grava
ENTREGA_v386_pacote.json no pacote (dados para a gerencia e para o registro no mapa de rotas, que e' ato dela)."""
import hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
ARQ = ["um_v386_candidato.py", "CANDIDATO_v386.json", "gerar_candidato_v386.py", "v386_runtime.py", "v386_pins.py", "artigo_pt_v386.pysnip", "artigo_en_v386.pysnip",
       "ensaio_a_seco_v386.py", "ensaio_a_seco_v386.json", "ensaio_a_seco_v386.out", "conferir_citacoes_v386.py", "conferir_citacoes_v386.json", "gerar_esperados_v386.py",
       "ESPERADOS_v386.json", "conferir_rito_v386.py", "conferencia_rito_v386_pre.json", "instalar_v386.py", "derivar_rito_v386.py", "rito_v386.sh", "DIFF_rito_v385_v386.txt",
       "_explorar_um_v386.py", "_ver_linhas.py", "_probe_transcrito_v386.py"]
out = {"gerado": time.strftime("%Y-%m-%d %H:%M:%S"), "pasta": HERE, "arquivos": {}}
for f in ARQ:
    p = os.path.join(HERE, f)
    if not os.path.exists(p):
        out["arquivos"][f] = {"AUSENTE": True}; continue
    b = open(p, "rb").read()
    out["arquivos"][f] = {"sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v386.json"), encoding="utf-8"))
ENS = json.load(open(os.path.join(HERE, "ensaio_a_seco_v386.json"), encoding="utf-8"))
ESP = json.load(open(os.path.join(HERE, "ESPERADOS_v386.json"), encoding="utf-8"))
CIT = json.load(open(os.path.join(HERE, "conferir_citacoes_v386.json"), encoding="utf-8"))
out["candidato"] = {k: CM[k] for k in ("sha16", "bytes", "base_v385_sha16", "escada", "pedra_sha16", "pins_sha16", "token_lido_da_pedra", "beta_v1_vs_core")}
out["candidato"]["patches"] = [p["id"] for p in CM["patches"]]
out["candidato"]["kernel"] = CM["kernel"]
out["candidato"]["ordem_do_operador"] = CM["ordem_do_operador"]
out["ensaio"] = {"veredito": ENS["veredito"], "sha16": ENS["sha16"], "import_s": ENS["import_s"], "escada": ENS["escada"], "mainflow_comeca": ENS["mainflow"]["comeca"], "chaves_novas": ENS["mainflow"]["chaves_novas_no_core"],
                 "unidade_n": len(ENS["unidade"]), "unidade_falhas": [k for k, v in ENS["unidade"].items() if v is not True], "artigo": {l: {k: v for k, v in ENS["artigo"][l].items() if k != "trecho"} for l in ("pt", "en")},
                 "variantes": ENS["variantes"], "markdown": ENS["markdown"], "reprodutibilidade_v385_sob_reuse": ENS["reprodutibilidade_v385_sob_reuse"], "citacoes": ENS["citacoes_do_operador"]}
out["citacoes"] = {"mensagens_do_operador": CIT["mensagens_do_operador"], "estrito_n": len(CIT["estrito"]), "estrito_nao_achadas": [k for k, v in CIT["estrito"].items() if v == "NAO ACHADA"],
                   "en_cita_as_mesmas_do_pt": CIT["en_cita_as_mesmas_do_pt"], "formas_da_errata": CIT["formas_da_errata"], "pedra_nao_verbatim": CIT["pedra_nao_verbatim"], "ok": CIT["ok"]}
out["esperados"] = {k: ESP[k] for k in ("candidato_sha16", "origem_sha16", "escada_v385", "escada_v386", "verb_token", "md_carimbo", "md_errata_R6")}
out["esperados"]["n_vereditos_pinados"] = len(ESP["vereditos_v385"]); out["esperados"]["n_flags_true_v385"] = len(ESP["flags_true_v385"]); out["esperados"]["muda_e_e_dito"] = ESP["muda_e_e_dito"]
out["esperados"]["pilar_v385"] = ESP["pilar_v385"]; out["esperados"]["ramo_b_V1"] = {k: ESP["ramo_b_V1"][k] for k in ("identificador", "spec_sha256", "conjunto_D_n")}
p = os.path.join(HERE, "ENTREGA_v386_pacote.json")
open(p + ".tmp", "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1)); os.replace(p + ".tmp", p)
print(json.dumps(out, ensure_ascii=False, indent=1))

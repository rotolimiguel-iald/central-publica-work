# -*- coding: utf-8 -*-
"""_conferir_pernas_parte2_v410.py -- a conferencia que o controlador da cadeia da parte 2 (cadeia_parte2_v410.sh) faz depois de cada perna, pelos ARQUIVOS (os passos do refazer_candidato mascaram falha por pipe): cada resultado tem de ser DESTA rodada (mtime >= o inicio dado) e do candidato corrente.
uso: python -I -B -X utf8 _conferir_pernas_parte2_v410.py perna1 <epoch_do_inicio>   |   memory   |   perna2 <epoch_do_inicio>
perna1: o ensaio a seco TUDO PASSOU e deste candidato; ESPERADOS deste candidato e deste ensaio; o conferidor positivo TUDO BATE e o controle negativo NAO bate; as citacoes conferem; PINOS e DERIVACAO sem falha; o p00 SEM FALHA (pendente nao e' falha).
memory: so' a pendencia do MEMORY.md no PRECONDICOES_v410.json (rc 0 = cabe; rc 3 = NAO cabe: a decisao e' da gerencia, que e' quem escreve o MEMORY.md).
perna2: o p00 TODAS PASSARAM; o B(n) pre-selo; os dois harnesses; a purga com zero ocorrencias."""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); P = lambda n: os.path.join(HERE, n)
modo = sys.argv[1]; t0 = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
J = lambda n: json.load(open(P(n), encoding="utf-8"))
novo = lambda n: os.path.exists(P(n)) and os.path.getmtime(P(n)) >= t0 - 2
R = {}


def fim(rc_ruim=1):
    ruins = [k for k, v in R.items() if v is not True]
    print("conferencia %s: %s" % (modo, "TUDO CERTO (%d itens)" % len(R) if not ruins else "FALHOU: " + json.dumps({k: R[k] for k in ruins}, ensure_ascii=False, default=str)[:1500]))
    sys.exit(0 if not ruins else rc_ruim)


if modo == "memory":
    pc = J("PRECONDICOES_v410.json"); pend = [p_ for p_ in pc.get("pendentes") or [] if "MEMORY.md" in str(p_.get("checagem")) or "PINO_MEMORIA_PY" in str(p_)]   # (as duas pendencias que sao ATO DA GERENCIA: o indice que so' ela escreve e o pino do memoria.py da fila)
    print("p00: sem_falha =", pc.get("sem_falha"), "| pendentes:", len(pc.get("pendentes") or []), "| as que sao ato da gerencia (MEMORY.md, PINO_MEMORIA_PY):", ([str(p_.get("checagem"))[:110] + " -> " + str(p_.get("motivo") or "")[:260] for p_ in pend] if pend else "nenhuma"))
    sys.exit(3 if pend else 0)
cand_sha = hashlib.sha256(open(P("um_v410_candidato.py"), "rb").read()).hexdigest(); CM = J("CANDIDATO_v410.json")
R["candidato_json_e_o_do_candidato"] = CM.get("sha256") == cand_sha
if modo == "perna1":
    ens = J("ensaio_a_seco_v410.json") if novo("ensaio_a_seco_v410.json") else {}
    R["ensaio_desta_rodada_tudo_passou_deste_candidato"] = (ens.get("veredito") == "TUDO PASSOU" and ens.get("sha16") == cand_sha[:16]) or [ens.get("veredito", "ausente ou velho")[:600], ens.get("sha16")]
    esp = J("ESPERADOS_v410.json") if novo("ESPERADOS_v410.json") else {}
    R["esperados_desta_rodada_deste_candidato_e_deste_ensaio"] = (esp.get("candidato_sha16") == cand_sha[:16] and esp.get("ensaio_sha16") == hashlib.sha256(open(P("ensaio_a_seco_v410.json"), "rb").read()).hexdigest()[:16]) or [esp.get("candidato_sha16"), esp.get("ensaio_sha16")]
    rf = esp.get("registros_funcao_v410") or {}
    R["esperados_com_os_quatro_registros_com_funcao"] = all(isinstance(rf.get(k_), dict) and rf[k_].get("verdict") for k_ in ("iald2", "aescala", "a_escala", "h0dn", "hms13")) or sorted(rf)
    pos = J("conferencia_rito_v410_POSITIVO_FALSO_NOS.json") if novo("conferencia_rito_v410_POSITIVO_FALSO_NOS.json") else {}
    R["conferidor_positivo_tudo_bate"] = pos.get("tudo_bate") is True or {"tudo_bate": pos.get("tudo_bate"), "deve_falsos": [k for k, v in (pos.get("deve") or pos.get("DEVE") or {}).items() if not v][:8], "nao_falsos": [k for k, v in (pos.get("nao") or pos.get("NAO") or {}).items() if not v][:8]}
    neg = J("conferencia_rito_v410_CONTROLE_NEGATIVO_PRE_RITO.json") if novo("conferencia_rito_v410_CONTROLE_NEGATIVO_PRE_RITO.json") else {}
    R["controle_negativo_do_conferidor_nao_bate"] = (neg.get("tudo_bate") is False) or neg.get("tudo_bate", "ausente ou velho")
    cit = J("conferir_citacoes_v410.json") if novo("conferir_citacoes_v410.json") else {}
    R["citacoes_conferem"] = cit.get("todas_conferem") is True or "ausente, velho ou falhou"
    pn = J("PINOS_BN_v410.json") if novo("PINOS_BN_v410.json") else {}
    R["pinos_do_bn_desta_rodada_deste_candidato_com_o_esperados_pinado"] = (bool(pn) and (pn.get("candidato") or {}).get("sha256") == cand_sha and "esperados" not in (pn.get("pendentes") or [])) or [(pn.get("candidato") or {}).get("sha256", "ausente ou velho")[:16], pn.get("pendentes")]
    R["derivacao_do_instalar_e_do_rito_desta_rodada"] = novo("DERIVACAO_v410.json")
    pc = J("PRECONDICOES_v410.json") if novo("PRECONDICOES_v410.json") else {}
    R["p00_desta_rodada_sem_falha"] = pc.get("sem_falha") is True or [c_.get("checagem", "")[:160] for c_ in pc.get("checagens") or [] if c_.get("ok") is False][:8] or "ausente ou velho"
    print("p00: pendentes =", len(pc.get("pendentes") or []), [str(p_.get("checagem"))[:70] for p_ in pc.get("pendentes") or []])
    fim()
if modo == "perna2":
    pc = J("PRECONDICOES_v410.json") if novo("PRECONDICOES_v410.json") else {}
    R["p00_todas_passaram"] = pc.get("ok") is True or [str(p_.get("checagem"))[:90] for p_ in pc.get("pendentes") or []] or [c_.get("checagem", "")[:160] for c_ in pc.get("checagens") or [] if c_.get("ok") is False][:8] or "ausente ou velho"
    pr = J("PINO_RECIBO_PRE_SELO_v410.json") if novo("PINO_RECIBO_PRE_SELO_v410.json") else {}
    R["recibo_pre_selo_desta_rodada_utilizavel"] = (pr.get("veredito") == "JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA" and pr.get("utilizavel_como_recibo_pre_selo_do_B_n") is True) or [pr.get("veredito", "ausente ou velho"), pr.get("utilizavel_como_recibo_pre_selo_do_B_n")]
    pv = J("PROVA_PRODUCAO_INTACTA_v410_pre_selo.json") if novo("PROVA_PRODUCAO_INTACTA_v410_pre_selo.json") else {}
    R["producao_intacta"] = pv.get("producao_intacta") is True or "ausente, velho ou falso"
    for nome, arq, marca in (("harness_textos", os.path.join("pos_rito", "harness_textos_out_v410.txt"), "RC_HT=0"), ("harness_fechar", os.path.join("pos_rito", "harness_fechar_out_v410.txt"), "RC_HF=0")):
        R[nome] = (novo(arq) and marca in open(P(arq), encoding="utf-8", errors="replace").read()) or "ausente, velho ou sem " + marca
    pg = J("purga_v410.json") if novo("purga_v410.json") else {}
    R["purga_zero_ocorrencias"] = (pg.get("total_com_ocorrencia") == 0 and pg.get("fala_excluida_total_com_ocorrencia") == 0) or [pg.get("total_com_ocorrencia"), pg.get("fala_excluida_total_com_ocorrencia")]
    fim()
print("modo desconhecido:", modo); sys.exit(9)

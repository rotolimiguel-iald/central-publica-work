# -*- coding: utf-8 -*-
"""P12: controle negativo dos comparadores de T18-T22 e RESUMO_T18_T22.json (veredito por teste, soma, sha256 dos recibos,
ressalva da auditoria c1 conferida por trecho). Uso: python -B -X utf8 resumo_e_controle.py controle|resumo"""
import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p12_replays as P  # noqa: E402

REC = P.REC
RECIBOS = [("T18", "T18_LIGANTE.json"), ("T19", "T19_V351_AGAPE.json"), ("T20", "T20_PALAVRA.json"),
           ("T21", "T21_SN1.json"), ("T22", "T22_NU2.json")]


def controle():
    out = {"quando": P.iso(P.agora()), "python": sys.version, "controles": []}

    def reg(nome, detectou, **kw):
        out["controles"].append(dict(nome=nome, detectou=bool(detectou), **kw))

    # 1. T21/T22: perturbacao de 1e-6 relativo num float real da saida e' vista; 1e-15 nao (dentro da tolerancia declarada)
    ref = json.load(open(os.path.join(P.WRK, "T21", "CALCULOS_R2_REPLAY.json"), encoding="utf-8"))
    pert = copy.deepcopy(ref)
    pert["beta0"] = pert["beta0"] * (1 + 1e-6)
    d, c = P.deep_compare(pert, ref, "", ("start_utc", "end_utc", "elapsed_seconds", "pins"))
    reg("T21: beta0 perturbado em 1e-6 relativo", len(d) >= 1, diferencas=d[:2])
    pert2 = copy.deepcopy(ref)
    pert2["beta0"] = pert2["beta0"] * (1 + 1e-15)
    d2, c2 = P.deep_compare(pert2, ref, "", ("start_utc", "end_utc", "elapsed_seconds", "pins"))
    reg("T21: beta0 perturbado em 1e-15 (dentro da tolerancia 1e-12) NAO acusa", len(d2) == 0, diferencas=d2[:2], na_tolerancia=c2["floats_na_tolerancia"])
    pert3 = copy.deepcopy(ref)
    pert3["status"] = "OUTRO"
    d3, _ = P.deep_compare(pert3, ref, "", ("start_utc", "end_utc", "elapsed_seconds", "pins"))
    reg("T21: string alterada", len(d3) == 1, diferencas=d3)
    # 2. pino de sha256 errado na copia: copy_check recusa
    src = os.path.join(P.WRK, "T21", "calculate_r2.py")
    try:
        P.copy_check(src, os.path.join(P.SB, "controle", "x.py"), "0" * 64)
        reg("copy_check com sha errado", False)
    except RuntimeError as e:
        reg("copy_check com sha errado recusa", True, erro=str(e)[:120])
    # 3. fonte Lean com sorry: o detector acusa; fonte com erro: acusa; olean de outra pedra: sha difere
    root = os.path.join(P.SB, "controle")
    os.makedirs(os.path.join(root, "TGLExt"), exist_ok=True)
    f1 = os.path.join(root, "TGLExt", "NegSorry.lean")
    open(f1, "wb").write(b"theorem neg_sorry : (1:Nat) = 1 := by sorry\n#print axioms neg_sorry\n")
    r1 = P.run_lean(f1, root, os.path.join(root, "out", "TGLExt", "NegSorry.olean"))
    reg("Lean: fonte com sorry (sorryAx)", bool(r1["sorry"]) or any("sorryAx" in v for v in r1["axiomas"].values()), sorry=r1["sorry"][:2], axiomas=r1["axiomas"])
    f2 = os.path.join(root, "TGLExt", "NegErro.lean")
    open(f2, "wb").write(b"theorem neg_erro : (1:Nat) = 2 := by rfl\n")
    r2 = P.run_lean(f2, root, os.path.join(root, "out", "TGLExt", "NegErro.olean"))
    reg("Lean: fonte com erro", r2["rc"] != 0 and bool(r2["erros"]), rc=r2["rc"], erros=r2["erros"][:1])
    # 4. o comparador de olean distingue oleans diferentes (T18 vs T19)
    a = P.sha(os.path.join(P.ART, "T18_LiganteLeiCampoCurvo_replay.olean"))
    b = P.sha(os.path.join(P.ART, "T19_V351DualScalingBridge_replay.olean"))
    reg("olean de uma pedra nao e' o da outra", a != b, sha_T18=a[:16], sha_T19_V351=b[:16])
    # 5. axioma fora do trio acusado
    c5 = {"rc_zero": True, "sem_erros": True, "sem_sorry": True, "olean_existe": True,
          "fora_do_trio": {"x": ["sorryAx"]}, "n_declaracoes_replay": 1}
    ok5, _ = P.passa_lean(c5)
    reg("passa_lean recusa axioma fora do trio", not ok5)
    out["todos_detectaram"] = all(x["detectou"] for x in out["controles"])
    out["escopo"] = "controle negativo dos comparadores; usa so sandbox C:/t/p12/controle e arquivos de V; nenhum dado observado"
    h = P.put_json(os.path.join(REC, "CONTROLE_NEGATIVO_T18_T22.json"), out)
    print(json.dumps({"controles": len(out["controles"]), "todos_detectaram": out["todos_detectaram"], "sha256": h}))


def resumo():
    res = {"quando": P.iso(P.agora()), "fase": "pre_selo", "contra": "v391", "etapa": "1 (leitura ampla de 'bancada', decisao P12)",
           "python": sys.version, "testes": [], "soma_T18_T22": {"PASSA": 0, "FALHA": 0, "NAO_EXECUTADO": 0}}
    for t, f in RECIBOS:
        p = os.path.join(REC, f)
        d = json.load(open(p, encoding="utf-8"))
        res["testes"].append({"teste": d["teste"], "veredito": d["veredito"], "modo_comparacao": d.get("modo_comparacao"),
                              "inicio": d.get("inicio"), "fim": d.get("fim"), "segundos": d.get("segundos"),
                              "codigo_saida": d.get("codigo_saida"), "recibo": p, "recibo_sha256": P.sha(p),
                              "razao": d.get("razao", "")})
        res["soma_T18_T22"][d["veredito"]] += 1
    cn = os.path.join(REC, "CONTROLE_NEGATIVO_T18_T22.json")
    if os.path.exists(cn):
        d = json.load(open(cn, encoding="utf-8"))
        res["controle_negativo"] = {"recibo": cn, "sha256": P.sha(cn), "todos_detectaram": d["todos_detectaram"], "n": len(d["controles"])}
    # junto do T12/T13/T14 ja existentes (ensaio_1)
    e1 = os.path.join(P.V, "bateria_pre_selo", "ensaio_1")
    r1 = os.path.join(e1, "recibos", "T12_T13_T14_ATRATOR.json")
    d1 = json.load(open(r1, encoding="utf-8"))
    sin = os.path.join(e1, "RECIBO_SINCRONIZACAO_v391_20261013_124149.json")
    ds = json.load(open(sin, encoding="utf-8"))
    br = ds["bateria_resultado"]
    res["ensaio_1_existente"] = {
        "T12_T13_T14_recibo": r1, "T12_T13_T14_recibo_sha256": P.sha(r1),
        "T12_T13_T14_veredito_no_recibo": d1.get("veredito"), "T12_T13_T14_chaves": sorted(d1.keys()),
        "recibo_de_sincronizacao": sin, "recibo_de_sincronizacao_sha256": P.sha(sin),
        "bateria": {k: br[k] for k in ("n", "passa", "falha", "nao_executado")},
        "veredito": ds["veredito"]}
    soma = dict(res["soma_T18_T22"])
    res["soma_etapa1_com_ensaio_1"] = {"PASSA": br["passa"] + soma["PASSA"], "FALHA": br["falha"] + soma["FALHA"],
                                       "NAO_EXECUTADO": br["nao_executado"] + soma["NAO_EXECUTADO"],
                                       "n": br["n"] + len(res["testes"])}
    # a segunda ressalva da auditoria c1 de 10/10, conferida por trecho
    aud = os.path.join(P.PROG, "auditorias", "F1.ATRATOR", "AUDITORIA_F1_ATRATOR_C1_a7c491ec.md")
    linhas = open(aud, "rb").read().decode("utf-8").replace("\r\n", "\n").split("\n")
    trecho = linhas[68:71]  # linhas 69 a 71 (1-based)
    alvo = "A5 e A3_angular n\u00e3o podem ser lidos como testemunho f\u00edsico nem ontol\u00f3gico."
    res["ressalva_2_auditoria_c1"] = {"arquivo": aud, "sha256": P.sha(aud), "linhas_69_a_71": trecho,
                                      "contem_a_frase_da_segunda_ressalva": any(alvo in l for l in trecho),
                                      "frase_conferida": alvo,
                                      "leitura": "vale para toda a bateria do atrator (T12/T13) e para o que a PALAVRA (T20) e os replays T18-T22 mostram: PASSA e' validade matematica sintetica na face testada, nao testemunho fisico nem ontologico, nao creditacao"}
    res["escopo"] = "validade matematica e replay documental na face testada; nenhum dado observado; NOT_FALSIFIED nao e' creditacao; o gate nao se move"
    res["bancada_um"] = "so lida (nenhum codigo da Bancada executado; servico HTTP nao chamado); ver snap_bancada_*.json em rodada2/p12"
    h = P.put_json(os.path.join(P.ENS, "RESUMO_T18_T22.json"), res)
    print(json.dumps({"soma": res["soma_T18_T22"], "etapa1": res["soma_etapa1_com_ensaio_1"], "ressalva_conferida": res["ressalva_2_auditoria_c1"]["contem_a_frase_da_segunda_ressalva"], "sha256": h}))


if __name__ == "__main__":
    {"controle": controle, "resumo": resumo}[sys.argv[1]]()

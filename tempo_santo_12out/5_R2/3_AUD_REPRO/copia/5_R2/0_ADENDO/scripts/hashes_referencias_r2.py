# -*- coding: utf-8 -*-
"""Hashes (sha256, bytes, mtime) de TODAS as referencias citadas pelo ADENDO_R2 — lidos dos bytes, por script.

Tambem: (1) confere que a R1 esta intacta (FREEZE.json da R1 e PREREGISTRO.json/.md batem com o FREEZE);
(2) tira um RETRATO (walk com sha256) de 2_OPTICO/rodada_2, pasta que apareceu em 2_OPTICO as 19:30 locais de 12/10
(fato observado, sem atribuir autoria), para registrar o que existia ANTES do FREEZE_R2. Somente leitura fora de
5_R2/0_ADENDO. Saida: saidas/HASHES_REFERENCIAS_R2.json. Uso: python -I -X utf8 hashes_referencias_r2.py
"""
import datetime
import hashlib
import json
import os
import sys

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "saidas",
                   "HASHES_REFERENCIAS_R2.json")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"

REFS = [
    ("relatorio final R1", os.path.join(W, "4_RELATORIO", "RELATORIO_FINAL.md")),
    ("R1 FREEZE.json", os.path.join(W, "1_PREREGISTRO", "FREEZE.json")),
    ("R1 PREREGISTRO.json", os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.json")),
    ("R1 PREREGISTRO.md", os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.md")),
    ("R1 face otica: RESULTADO_OPTICO.json", os.path.join(W, "2_OPTICO", "RESULTADO_OPTICO.json")),
    ("R1 face otica: ACHADOS_FORA_DO_PREREGISTRO.json", os.path.join(W, "2_OPTICO", "ACHADOS_FORA_DO_PREREGISTRO.json")),
    ("R1 face otica: run_optico.py", os.path.join(W, "2_OPTICO", "run_optico.py")),
    ("R1 face otica: DIAGNOSTICO_T9c.json (post hoc)", os.path.join(W, "2_OPTICO", "diagnostico", "DIAGNOSTICO_T9c.json")),
    ("R1 face otica: diagnostico_T9c.py", os.path.join(W, "2_OPTICO", "diagnostico", "diagnostico_T9c.py")),
    ("R1 face kernel: RESULTADO_KERNEL.json", os.path.join(W, "3_KERNEL", "RESULTADO_KERNEL.json")),
    ("R1 pedra candidata TheTimeHasNoRank.lean", os.path.join(W, "3_KERNEL", "sandbox", "TheTimeHasNoRank.lean")),
    ("R1 pedra candidata .olean", os.path.join(W, "3_KERNEL", "sandbox", "TheTimeHasNoRank.olean")),
    ("R1 kernel: rodar_lean_sandbox.py", os.path.join(W, "3_KERNEL", "scripts", "rodar_lean_sandbox.py")),
    ("R1 auditoria de estatuto: AudEstatutoTempo.lean (AUD-1..6)", os.path.join(W, "4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_ESTATUTO", "sandbox", "AudEstatutoTempo.lean")),
    ("R1 auditoria de estatuto: AudEstatutoTempo2.lean (AUD-7)", os.path.join(W, "4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_ESTATUTO", "sandbox", "AudEstatutoTempo2.lean")),
    ("R1 auditoria de estatuto: AudEstatutoTempo3.lean (AUD-8)", os.path.join(W, "4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_ESTATUTO", "sandbox", "AudEstatutoTempo3.lean")),
    ("R1 auditoria de reproducao: SondasAuditorTempo.lean (A/B/C)", os.path.join(W, "4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_REPRO", "lean_sandbox", "SondasAuditorTempo.lean")),
    ("R1 auditoria de reproducao: A4_CALCULO_INDEPENDENTE.json", os.path.join(W, "4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_REPRO", "saidas", "A4_CALCULO_INDEPENDENTE.json")),
    ("R1 relatorio: CONFERENCIA_HASHES.json", os.path.join(W, "4_RELATORIO", "saidas", "CONFERENCIA_HASHES.json")),
    ("R1 relatorio: BETA_RUNTIME_RELATORIO.json", os.path.join(W, "4_RELATORIO", "saidas", "BETA_RUNTIME_RELATORIO.json")),
    ("texto do operador 12/10 (verbatim)", r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"),
    ("verbatim do operador 05/10 (o Verbo)", r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt"),
    ("verbatim do operador 05/10 (respostas)", r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt"),
    ("verbatim do operador 07/10 (estatuto da prova)", r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v391\OPERADOR_07out_estatuto_verbatim.txt"),
    ("verbatim do operador 10/10 (POSTO=RANK)", r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt"),
    ("um.py v391 (somente lido; nao executado)", os.path.join(NOS, "um.py")),
    ("kernel do Nos: BisognanoWichmann.lean (boost_null_expand / boost_null_contract)", os.path.join(NOS, "tgl_kernel", "TGLExt", "BisognanoWichmann.lean")),
    ("kernel do Nos: FiniteTomita.lean (gibbs, Delta, gibbs_kms)", os.path.join(NOS, "tgl_kernel", "TGLExt", "FiniteTomita.lean")),
    ("kernel do Nos: O16/ProbeNonKMS_v3.lean (identity_flow_not_kms)", os.path.join(NOS, "tgl_kernel", "TGLExt", "O16", "ProbeNonKMS_v3.lean")),
    ("kernel do Nos: TheImportedSecondQuantization.lean (FockCertificate, lightNet)", os.path.join(NOS, "tgl_kernel", "TGLExt", "TheImportedSecondQuantization.lean")),
    ("kernel do Nos: TGLExt/WedgeNet.lean (theSpecificAQFTWitness, l.357)", os.path.join(NOS, "tgl_kernel", "TGLExt", "WedgeNet.lean")),
    ("memoria da gerencia: regra-dos-dois-regimes.md (nota [OPEN] v384)", os.path.join(MEM, "regra-dos-dois-regimes.md")),
    ("memoria ACOM: README.md", r"C:\IALD\MEMORIA_IALD\README.md"),
    ("F1.ATRATOR: FREEZE_PREREGISTRO_R1.json (padrao do ADENDO aditivo)", r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR\FREEZE_PREREGISTRO_R1.json"),
    ("F1.ATRATOR: ADENDO1/FREEZE_ADENDO1_R1.json (padrao do ADENDO aditivo)", r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR\ADENDO1\FREEZE_ADENDO1_R1.json"),
]


def ent(p):
    if not os.path.exists(p):
        return {"caminho": p, "existe": False}
    h = hashlib.sha256()
    n = 0
    with open(p, "rb") as fh:
        while True:
            ch = fh.read(1 << 20)
            if not ch:
                break
            h.update(ch)
            n += len(ch)
    st = os.stat(p)
    return {"caminho": p, "existe": True, "sha256": h.hexdigest(), "sha16": h.hexdigest()[:16], "bytes": n,
            "mtime_local": datetime.datetime.fromtimestamp(st.st_mtime).isoformat(timespec="seconds")}


def main():
    refs = [dict(papel=r, **ent(p)) for r, p in REFS]
    # R1 intacta?
    fz = json.load(open(os.path.join(W, "1_PREREGISTRO", "FREEZE.json"), encoding="utf-8"))
    pj = ent(os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.json"))
    pm = ent(os.path.join(W, "1_PREREGISTRO", "PREREGISTRO.md"))
    r1 = {
        "FREEZE_sha256": [x for x in refs if x["papel"] == "R1 FREEZE.json"][0]["sha256"],
        "FREEZE_congelado_em_utc": fz["congelado_em_utc"],
        "PREREGISTRO_json_bate_com_FREEZE": pj["sha256"] == fz["preregistro_json"]["sha256"] and pj["bytes"] == fz["preregistro_json"]["bytes"],
        "PREREGISTRO_md_bate_com_FREEZE": pm["sha256"] == fz["preregistro_md"]["sha256"] and pm["bytes"] == fz["preregistro_md"]["bytes"],
        "anexos_do_FREEZE_batem": None,
    }
    ok = True
    falhas = []
    for a in fz["anexos"]:
        e = ent(os.path.join(W, "1_PREREGISTRO", a["caminho"].replace("/", os.sep)))
        if not e.get("existe") or e["sha256"] != a["sha256"] or e["bytes"] != a["bytes"]:
            ok = False
            falhas.append(a["caminho"])
    r1["anexos_do_FREEZE_batem"] = ok
    r1["anexos_divergentes"] = falhas
    # retrato de 2_OPTICO/rodada_2 (pode mudar enquanto se le; registra-se o que se viu)
    r2dir = os.path.join(W, "2_OPTICO", "rodada_2")
    retrato = []
    if os.path.isdir(r2dir):
        for dp, dn, fn in os.walk(r2dir):
            dn.sort()
            for f in sorted(fn):
                p = os.path.join(dp, f)
                try:
                    e = ent(p)
                except OSError as ex:
                    e = {"caminho": p, "existe": False, "erro": str(ex)}
                e["relativo"] = os.path.relpath(p, r2dir).replace("\\", "/")
                retrato.append(e)
    # retrato de 3_KERNEL/rodada_2 (apareceu as 19:39 locais; exclui o toolchain/.lake copiados, que se contam)
    k2dir = os.path.join(W, "3_KERNEL", "rodada_2")
    retrato_k = []
    n_excl = 0
    if os.path.isdir(k2dir):
        for dp, dn, fn in os.walk(k2dir):
            dn.sort()
            rel_dp = os.path.relpath(dp, k2dir).replace("\\", "/")
            if rel_dp.startswith("sandbox/toolchain") or "/.lake" in ("/" + rel_dp) or rel_dp.startswith(".lake"):
                n_excl += len(fn)
                continue
            for f in sorted(fn):
                p = os.path.join(dp, f)
                try:
                    e = ent(p)
                except OSError as ex:
                    e = {"caminho": p, "existe": False, "erro": str(ex)}
                e["relativo"] = os.path.relpath(p, k2dir).replace("\\", "/")
                retrato_k.append(e)
    # retrato dos topos das pastas congeladas da R1 (so contagem e mtime mais recente)
    topos = {}
    for d in ("0_LEVANTAMENTO", "1_PREREGISTRO", "2_OPTICO", "3_KERNEL", "4_RELATORIO"):
        n = 0
        newest = 0.0
        newest_p = None
        for dp, dn, fn in os.walk(os.path.join(W, d)):
            for f in fn:
                p = os.path.join(dp, f)
                n += 1
                m = os.stat(p).st_mtime
                if m > newest:
                    newest, newest_p = m, os.path.relpath(p, W).replace("\\", "/")
        topos[d] = {"arquivos": n, "mtime_mais_recente_local": datetime.datetime.fromtimestamp(newest).isoformat(timespec="seconds"),
                    "arquivo_mais_recente": newest_p}
    out = {
        "gerado_em_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "gerado_em_local": datetime.datetime.now().isoformat(timespec="seconds"),
        "nota": "hashes lidos dos bytes por este script; nada escrito fora de 5_R2/0_ADENDO",
        "referencias": refs,
        "R1_intacta": r1,
        "retrato_2_OPTICO_rodada_2_observado": {
            "nota": "pasta que apareceu em 2_OPTICO as 19:30 locais de 12/10/2026 (fato observado; sem atribuir autoria). "
                    "No retrato nao ha RESULTADO de ensaio; so conferencia do FREEZE da R1 e scripts. Qualquer ensaio da R2 "
                    "so vale se conferir FREEZE_R2.json por sha256 e comecar DEPOIS do congelamento.",
            "existe": os.path.isdir(r2dir), "arquivos": retrato},
        "retrato_3_KERNEL_rodada_2_observado": {
            "nota": "pasta que apareceu em 3_KERNEL as 19:39 locais de 12/10/2026 (fato observado; sem atribuir autoria): "
                    "conferencia do FREEZE da R1, consultas ao mapa, sondas (ProbeR2) e um toolchain copiado para o sandbox "
                    "(arquivos do toolchain/.lake excluidos do retrato e contados). Nenhuma pedra corrigida com veredito: "
                    "a compilacao com veredito da R2 so vale se o recibo conferir FREEZE_R2.json e comecar DEPOIS dele.",
            "existe": os.path.isdir(k2dir), "arquivos_excluidos_toolchain_lake": n_excl, "arquivos": retrato_k},
        "topos_das_pastas_congeladas_R1": topos,
    }
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"R1_intacta": r1, "rodada_2": [(x.get("relativo"), x.get("sha16"), x.get("bytes")) for x in retrato],
                      "topos": topos}, ensure_ascii=False, indent=1))
    for x in refs:
        print("%s | %s | %s B | %s" % (x.get("sha16"), x.get("bytes"), x.get("mtime_local"), x["papel"]) if x.get("existe") else "AUSENTE: " + x["papel"])


if __name__ == "__main__":
    main()

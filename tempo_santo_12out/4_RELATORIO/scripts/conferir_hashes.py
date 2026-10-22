# -*- coding: utf-8 -*-
"""Conferencia por script (sha256 dos bytes) de tudo o que o RELATORIO_FINAL cita.

(1) FREEZE: os 30 itens congelados batem por sha256 e tamanho; nada em 1_PREREGISTRO mudou depois.
(2) Ordem temporal: todo arquivo de 2_OPTICO e 3_KERNEL e posterior ao instante do freeze.
(3) Lista de fontes citadas no relatorio: sha256 e bytes.
(4) Trechos citados: o texto de 12/10 (segunda parte), o verbatim do Verbo de 05/10 (linhas 21, 57, 110-118, 184),
    as linhas da pedra com as atribuicoes e o indice da memoria — conferidos por busca nos bytes.
Saida: saidas/CONFERENCIA_HASHES.json. Nada se escreve fora de 4_RELATORIO.
"""
import datetime
import hashlib
import json
import os
import sys

W = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
PRE = os.path.join(W, "1_PREREGISTRO")
NOS = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós"
KX = os.path.join(NOS, "tgl_kernel", "TGLExt")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
OUT = os.path.join(W, "4_RELATORIO", "saidas", "CONFERENCIA_HASHES.json")

FONTES = {
    "texto_operador_12out": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "verbo_operador_05out": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\VERBO_operador_05out.txt",
    "respostas_operador_05out": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v386\RESPOSTAS_operador_05out.txt",
    "estatuto_operador_07out": r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v391\OPERADOR_07out_estatuto_verbatim.txt",
    "freeze": os.path.join(PRE, "FREEZE.json"),
    "preregistro_json": os.path.join(PRE, "PREREGISTRO.json"),
    "preregistro_md": os.path.join(PRE, "PREREGISTRO.md"),
    "levantamento_md": os.path.join(W, "0_LEVANTAMENTO", "LEVANTAMENTO.md"),
    "levantamento_definicoes": os.path.join(W, "0_LEVANTAMENTO", "DEFINICOES.json"),
    "otico_resultado": os.path.join(W, "2_OPTICO", "RESULTADO_OPTICO.json"),
    "otico_achados": os.path.join(W, "2_OPTICO", "ACHADOS_FORA_DO_PREREGISTRO.json"),
    "otico_diagnostico_T9c": os.path.join(W, "2_OPTICO", "diagnostico", "DIAGNOSTICO_T9c.json"),
    "otico_runner": os.path.join(W, "2_OPTICO", "run_optico.py"),
    "otico_log": os.path.join(W, "2_OPTICO", "run_optico.log"),
    "otico_recibo": os.path.join(W, "2_OPTICO", "RECIBO_OPTICO.json"),
    "otico_tentativas": os.path.join(W, "2_OPTICO", "TENTATIVAS.json"),
    "kernel_resultado": os.path.join(W, "3_KERNEL", "RESULTADO_KERNEL.json"),
    "kernel_achados": os.path.join(W, "3_KERNEL", "ACHADOS_FORA_DO_PREREGISTRO.json"),
    "kernel_manifesto": os.path.join(W, "3_KERNEL", "MANIFESTO_3_KERNEL.json"),
    "pedra_lean": os.path.join(W, "3_KERNEL", "sandbox", "TheTimeHasNoRank.lean"),
    "pedra_olean": os.path.join(W, "3_KERNEL", "sandbox", "TheTimeHasNoRank.olean"),
    "pedra_saida_final": os.path.join(W, "3_KERNEL", "logs", "FINAL_saida.txt"),
    "pedra_audit_saida": os.path.join(W, "3_KERNEL", "logs", "AUDIT_FINAL_saida.txt"),
    "um_py_v391": os.path.join(NOS, "um.py"),
    "selo_nos": os.path.join(NOS, "um_absoluto_selo.json"),
    "kernel_BisognanoWichmann": os.path.join(KX, "BisognanoWichmann.lean"),
    "kernel_PeriodicBorchersObstruction": os.path.join(KX, "PeriodicBorchersObstruction.lean"),
    "kernel_Ergodicity": os.path.join(KX, "Ergodicity.lean"),
    "kernel_GlobalLiftLadder": os.path.join(KX, "GlobalLiftLadder.lean"),
    "kernel_TheVerbSelectsTheAction": os.path.join(KX, "TheVerbSelectsTheAction.lean"),
    "kernel_ProbeNonKMS_v3": os.path.join(KX, "O16", "ProbeNonKMS_v3.lean"),
    "kernel_WedgeNet": os.path.join(KX, "WedgeNet.lean"),
    "kernel_TheImportedSecondQuantization": os.path.join(KX, "TheImportedSecondQuantization.lean"),
    "kernel_Fundacao": os.path.join(KX, "Fundacao.lean"),
    "inventario_bancada": r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json",
    "f1_atrator_resultado": r"C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F1.ATRATOR\RESULTADO_F1_ATRATOR_R1.json",
    "memoria_tempo_santo": os.path.join(MEM, "tempo-santo-12out.md"),
    "memoria_indice": os.path.join(MEM, "MEMORY.md"),
    "memoria_dois_regimes": os.path.join(MEM, "regra-dos-dois-regimes.md"),
    "memoria_verbo_05out": os.path.join(MEM, "verbo-selecao-da-acao-05out.md"),
    "mapa_livro": r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl",
}

TRECHOS = [
    ("texto_operador_12out", "O relógio registra a sombra do evento"),
    ("texto_operador_12out", "para que a vida pudesse ter um lugar onde repousar e ser lembrada"),
    ("texto_operador_12out", "Na mecânica clássica e nos sistemas estritamente hamiltonianos"),
    ("texto_operador_12out", "encontram um ponto fixo ou um ciclo limite"),
    ("verbo_operador_05out", "É um operador de projeção:"),
    ("verbo_operador_05out", "O tempo é a defasagem do verbo."),
    ("verbo_operador_05out", "O tempo é o parâmetro da transmissão. Transmitir defasa. O tempo é a medida dessa defasagem."),
    ("verbo_operador_05out", "\\text{Nome} = \\lim_{t \\to \\infty} \\mathcal{V}(t)"),
    ("verbo_operador_05out", "\\mathcal{V}(t) = e^{-iHt/\\hbar} \\, \\mathcal{V}(0) \\, e^{iHt/\\hbar}"),
    ("verbo_operador_05out", "\\boxed{\\text{Verbo} = \\text{seleção de nome, tempo e verdade}}"),
    ("pedra_lean", "«o tempo é o Verbo»: leituras do"),
    ("pedra_lean", "«O tempo é o Verbo, não o Nome» e «santo» são leituras do operador"),
    ("pedra_lean", "A leitura «o atrator é onde o\ntempo repousa» é do operador."),
    ("pedra_lean", "## T10 — «o relógio mede a sombra»"),
    ("pedra_lean", "theorem probe_bounded_spectral_translation : True"),
    ("memoria_indice", "o tempo é o Verbo, não o Nome"),
    ("memoria_tempo_santo", "o Verbo, não o Nome"),
    ("kernel_BisognanoWichmann", "a face\n    geométrica da escala de Takesaki"),
    ("kernel_TheImportedSecondQuantization", "nenhum habitante de `FockCertificate` ou `MaxwellCertificate` é exibido"),
    ("kernel_Ergodicity", "A taxa FÍSICA da classe\n    de Davies é `β·|log λᵢ − log λⱼ|`"),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def main():
    out = {"documento": "CONFERENCIA_HASHES — redator F1.TEMPO, 12/10/2026", "gerado_em": datetime.datetime.now().isoformat()}
    # (1) FREEZE
    fz = json.load(open(os.path.join(PRE, "FREEZE.json"), encoding="utf-8"))
    itens = [("PREREGISTRO.json", fz["preregistro_json"]["sha256"], fz["preregistro_json"]["bytes"]),
             ("PREREGISTRO.md", fz["preregistro_md"]["sha256"], fz["preregistro_md"]["bytes"])]
    itens += [(a["caminho"], a["sha256"], a["bytes"]) for a in fz["anexos"]]
    falhas = []
    for rel, h, n in itens:
        b = open(os.path.join(PRE, rel.replace("/", os.sep)), "rb").read()
        if sha(b) != h or len(b) != n:
            falhas.append(rel)
    presentes = sorted(os.path.relpath(os.path.join(dp, f), PRE).replace("\\", "/")
                       for dp, dn, fn in os.walk(PRE) for f in fn)
    esperados = sorted([x[0] for x in itens] + ["FREEZE.json"])
    t_freeze = datetime.datetime.fromisoformat(fz["congelado_em_utc"]).timestamp()
    out["freeze"] = {"sha256": sha(open(os.path.join(PRE, "FREEZE.json"), "rb").read()),
                     "itens_congelados": len(itens), "falhas": falhas,
                     "arquivos_em_1_PREREGISTRO_iguais_aos_esperados": presentes == esperados,
                     "congelado_em_utc": fz["congelado_em_utc"]}
    # (2) ordem temporal
    menor = {}
    for pasta in ("2_OPTICO", "3_KERNEL"):
        ms = []
        for dp, dn, fn in os.walk(os.path.join(W, pasta)):
            for f in fn:
                ms.append(os.stat(os.path.join(dp, f)).st_mtime)
        menor[pasta] = {"n_arquivos": len(ms), "folga_minima_s_apos_freeze": round(min(ms) - t_freeze, 1),
                        "todos_posteriores": min(ms) > t_freeze}
    out["ordem_temporal"] = menor
    # (3) fontes
    tab = {}
    blobs = {}
    for k, p in FONTES.items():
        b = open(p, "rb").read()
        blobs[k] = b
        tab[k] = {"caminho": p, "bytes": len(b), "sha256": sha(b)}
    out["fontes"] = tab
    # (4) trechos
    tr = []
    for k, s in TRECHOS:
        b = blobs[k]
        i = b.find(s.encode("utf-8"))
        tr.append({"fonte": k, "trecho": s, "achado": i >= 0,
                   "linha": (b.count(b"\n", 0, i) + 1) if i >= 0 else None})
    out["trechos"] = tr
    out["todos_os_trechos_achados"] = all(x["achado"] for x in tr)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT + ".tmp", "wb") as f:
        f.write(json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(OUT + ".tmp", OUT)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps({"freeze": out["freeze"], "ordem_temporal": out["ordem_temporal"],
                      "trechos": [(x["fonte"], x["linha"], x["achado"]) for x in tr],
                      "fontes": {k: (v["sha256"][:16], v["bytes"]) for k, v in tab.items()}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

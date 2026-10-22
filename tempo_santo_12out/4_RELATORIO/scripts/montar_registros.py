# -*- coding: utf-8 -*-
"""Monta os dois registros do mapa de rotas da F1.TEMPO (ROTA e RESULTADO) e os valida A SECO contra as
regras do proprio rotas.py (funcao _valida, que so le arquivos e calcula sha256). NAO registra: o
`rotas.py registrar` e ato da gerencia (a ROTA primeiro, depois o RESULTADO).

Saidas: registro_rota_F1.TEMPO.json, registro_mapa_F1.TEMPO.json e saidas/VALIDACAO_REGISTROS.json.
"""
import importlib.util
import json
import os
import re
import sys

sys.dont_write_bytecode = True
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = os.path.dirname(BASE)
ROTAS_PY = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
RID = "formal.tempo_santo_fluxo_e_dissipacao"

REFS = ["formal.singularidade_le_atrator", "quantica.pilar_v384_rodada_completa", "umpy.v390.selo_fundacao_agape",
        "kernel.v386_tipagem_do_verbo", "kernel.leitura_cria_o_objeto_07out", "formal.f1_2.dual_scaling_reuse_011",
        "programa.auditoria.f1_2_ponte_v351_07out", "quantica.inventario_gkls_um_py_kernel"]


def p(*partes):
    return os.path.join(W, *partes)


ROTA = {
    "tipo": "ROTA",
    "rota_id": RID,
    "dominio": "FORMAL",
    "titulo": ("F1.TEMPO: o tempo que não se deixa nomear (texto do operador de 12/10: Kadosh, Pauli, fluxo modular, "
               "Liouville, dissipação, atrator, «puro amor») testado na face finita do kernel (pedra candidata em sandbox) "
               "e num modelo ótico sintético, com pré-registro congelado e duas auditorias independentes"),
    "pergunta": ("O que, na segunda parte do texto de 12/10 sobre o tempo «santo», tem forma matemática na face finita e passa "
                 "no kernel e no modelo ótico: (T1) não há operador de tempo em dimensão finita; (T2) Pauli em dimensão infinita "
                 "(só citação); (T3) o tempo como fluxo modular KMS; (T4) Liouville × dissipação; (T5) o conjunto fixo da "
                 "defasagem pura; (T6) a seta pela pureza; (T7) o inverso não positivo; (T8) a coerência obedece à Ágape; "
                 "(T9) «o tempo não tem posto»; (T10) o relógio lê módulo período e o agora não se move; (T11) no atrator "
                 "tracial o relógio modular para? E o que é só leitura [ONTO] ou literatura [KNOWN]?"),
    "dados": ["nenhum dado observado",
              "modelo ótico sintético da F1.ATRATOR: S = Smat(θ_M), C = D∘Ad(S)∘D, T = R + λ(I − R), λ = 1 − 2β; β lido nos "
              "bytes do um.py v391 (l.5557, igual à l.95) e calculado em runtime; semente 20261012"],
    "metodo": ("Levantamento (0_LEVANTAMENTO) → pré-registro congelado por hash ANTES de qualquer ensaio (FREEZE 6b29d4c9b09e5553, "
               "2026-10-12T16:09:07Z: 23 frases mapeadas cláusula a cláusula, 30 excertos do cânone, 11 afirmações, 22 controles, "
               "15 sondas; regra de decisão por subitem PASSA/FALHA/NÃO_CONSTRUÍDA/INVÁLIDO, CITADA, LEITURA, ABERTA; sem "
               "veredito global) → face ótica (run_optico.py fcc289889ec418ba, tentativa 003; float64 e decimal de 200 dígitos) "
               "→ face kernel (pedra candidata TGLExt.TheTimeHasNoRank, Lean 4.31.0 em sandbox, LEAN_PATH só de leitura no "
               ".lake do Nós, impressão digital do tgl_kernel igual antes e depois) → auditoria de reprodução (recompilação "
               "com .olean idêntico, ensaio ótico refeito bit a bit, cálculo independente em mpmath, 15 sondas adversariais e "
               "6 tentativas de provar o contrário) → auditoria de estatuto e regra (verbatins, nomes, regimes, sondas "
               "AUD-1 a AUD-8) → relatório do redator (4_RELATORIO)."),
    "estatuto": ("INPUT (protocolo da gerência c1); alvo REAL na face finita; KNOWN por citação (Pauli, Liouville, tempo "
                 "térmico, Takesaki, Landauer); ONTO as leituras do operador; OPEN o ciclo limite"),
    "status": "EM_CURSO",
    "olhou_dados": False,
    "onde": ("C:\\IALD\\Central de Patentes\\work\\tempo_santo_12out (0_LEVANTAMENTO, 1_PREREGISTRO, 2_OPTICO, 3_KERNEL, "
             "4_RELATORIO); pedra candidata 3_KERNEL\\sandbox\\TheTimeHasNoRank.lean (não instalada)"),
    "artefatos": [
        r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
        p("1_PREREGISTRO", "FREEZE.json"),
        p("1_PREREGISTRO", "PREREGISTRO.json"),
        p("1_PREREGISTRO", "PREREGISTRO.md"),
        p("0_LEVANTAMENTO", "LEVANTAMENTO.md"),
    ],
    "refs": REFS,
    "nota": ("Unidade F1.TEMPO (trilha TEMPO) da gerência c1, workflow posto-e-tempo; trilha irmã F1.FREQUENCIA (o rank; "
             "texto de 11/10). Consultas antes, com o mapa só lido (4_RELATORIO\\saidas\\rotas): nenhuma rota sobre tempo "
             "santo, F1.TEMPO, operador de tempo ou Pauli, Liouville, ciclo limite, identity_flow_not_kms, «o tempo é o "
             "Verbo» ou «repousar» (n = 0); as rotas vizinhas estão em refs. O registro desta rota é ato da gerência; os "
             "executores não escreveram no mapa."),
}

RESULTADO = {
    "tipo": "RESULTADO",
    "rota_id": RID,
    "titulo": ("F1.TEMPO: PASSA na face finita em T1, T3 a T8, T10 e T11; T2 CITADA; T9 FALHA só pelo critério numérico "
               "ótico (tolerância 1e-13 abaixo do piso do float64; kernel T9.a a T9.e PASSA); ciclo limite ABERTA; a pedra "
               "não entra no um.py como está"),
    "resultado": ("Por afirmação, pela regra congelada: T1 PASSA; T2 CITADA (T2.b PASSA, opcional); T3 PASSA com ressalva "
                  "(T3.b(iii) sem habitante exibido, V-GERAL-1); T4 PASSA; T5 PASSA (T5.c CITADA); T6 PASSA; T7 PASSA; T8 "
                  "PASSA + LEITURA; T9 FALHA (T9.o(c), entradas: 6.518e-13 > 1e-13 em k = 10^4; piso de representação "
                  "k|δ|/2 com δ = 1.18e-16; kernel T9.a-e PASSA); T10 PASSA + LEITURA; T11 PASSA (face finita); S46.3 ciclo "
                  "limite ABERTA. Kernel: pedra candidata 7105eda468b60309 com EXIT 0, 127 declarações com #print axioms no "
                  "trio, 0 sorry, .olean 9f473a088262b073 idêntico nas duas auditorias; impressão digital do tgl_kernel igual "
                  "(meta b1b47447, src 911cb40b). Ótico: β em runtime 0.012031300400803142 (lido dos bytes, Δ = 0); ω1 = "
                  "4.4081393960414665; P1 = 1.4253599404823543; det T = 1 − 2β; Tr(T1ψ+)^2 = 0.9496802613377202; "
                  "λmin(T-tψ+) = −0.006052 / −0.85914 / −11012.73; k_ε = 95 / 284 / 568; ω1000 = 5.28e-11; os 22 controles "
                  "como registrado; reprodução bit a bit (2153 folhas, 0 diferenças)."),
    "veredito": ("SEM_VEREDITO_GLOBAL__T1_PASSA__T2_CITADA__T3_PASSA_RESSALVA_T3b_iii__T4_PASSA__T5_PASSA__T6_PASSA__T7_PASSA"
                 "__T8_PASSA_LEITURA__T9_FALHA_CRITERIO_NUMERICO_OTICO__T10_PASSA_LEITURA__T11_PASSA_FACE_FINITA"
                 "__CICLO_LIMITE_ABERTA__PEDRA_NAO_ENTRA_COMO_ESTA__GATE_INTOCADO"),
    "estatuto": ("REAL (face finita: kernel em sandbox e modelo sintético); KNOWN por citação; ONTO as leituras; validade "
                 "matemática na face testada, não creditação"),
    "status": "EXAMINADA_COM_DEFEITO",
    "olhou_dados": False,
    "defeito": ("(1) T9.o(c): a tolerância de 1e-13 ficou abaixo do piso de representação do float64, que já era conhecido "
                "(incoerente com o O-d em 1e-11; o O-f depende do caminho de cálculo). (2) A pedra atribui ao operador frases "
                "sem verbatim («o tempo é o Verbo»; «O tempo é o Verbo, não o Nome»; «o atrator é onde o tempo repousa»; o "
                "título troca «registra» por «mede»); pelo verbatim de 05/10, o Verbo é operador de projeção e o tempo é a "
                "defasagem do verbo. (3) Nomes que afirmam mais que o termo: time_is_the_modular_flow; "
                "TheTimeHasNoRank/the_time_has_no_rank contra flow_full_rank (posto pleno); optical_attractor_is_the_absolute_one "
                "sem canal no enunciado. (4) O cabeçalho estende a regra dos dois regimes (FACE = semigrupo, ÂNGULO = "
                "unitário), contra a tabela da casa (Bisognano–Wichmann na FACE) e o [OPEN] da v384. (5) V-GERAL-1 "
                "incompleta: nontracial_state_rejects_the_identity_flow (W AQFT), light_flow_group e "
                "light_modular_orbit_converges_iff_post (FockCertificate) sem habitante. (6) Pré-registro: β «medido» (é "
                "lido e calculado; l.5557 embutida em _NIVEL2_MCMC_FILES); T8.d cita a docstring de boost_null_expand; "
                "«face» homônimo em T5; marcas [INPUT da gerência] faltando; lacunas em S34.2, S38.2 e S44.1."),
    "nao_refazer": ("Não refazer os ensaios nem a recompilação: o ótico foi reproduzido bit a bit, a pedra deu .olean idêntico "
                    "nas duas auditorias e o cálculo independente (mpmath) concorda. Não ler a FALHA de T9 como contraexemplo: "
                    "a identidade é exata e o kernel a prova. Não ler a face ótica como evidência independente nem como rito: "
                    "é só consistência numérica de identidades do kernel. Não ler T2 como teste: Pauli em dimensão infinita é "
                    "citação. Não ler a Ágape na coerência como conteúdo próprio do dephasing: vale para toda lei e^{-s} "
                    "(AUD-1); o próprio é o registro que não escala. Não pedir limite ao ângulo."),
    "proximo_passo": ("(a) Pedra corrigida: atribuições, nomes, cabeçalho dos regimes, peso morto (sonda de tipo True, "
                      "re-export duplicado, _hd) e V-GERAL-1, por habitante (theSpecificAQFTWitness em WedgeNet.lean:357; "
                      "lightNet) ou pela versão de face finita de T3.b(iii) com a AQFT marcada condicional; nova compilação e "
                      "nova auditoria independente. (b) Gerência: registrar a FALHA de T9 como resultado, com o diagnóstico "
                      "ao lado, ou congelar um ADENDO uniforme (O-f e T9.o(c)) antes de reensaiar. (c) Erratas ao lado: "
                      "pré-registro por ADENDO; memória da gerência (tempo-santo-12out.md l.15; MEMORY.md l.22); um.py v392 "
                      "(fractal_dephasing_principle l.6489, l.6507-6508 e l.6530; artigo v386 l.166640 e chaves "
                      "l.134239-134242). (d) Operador: o nome da pedra; qual «defasar» é o tempo; repousar × ser lembrada; o "
                      "chão firme; a reunião ágape, sacrifício/amor e puro amor; o ciclo limite (unidade nova?). (e) Na v392 "
                      "entram só os subitens PASSA, com CITADA e LEITURA marcadas, junto com o teorema do atrator."),
    "onde": ("C:\\IALD\\Central de Patentes\\work\\tempo_santo_12out\\4_RELATORIO\\RELATORIO_FINAL.md (tabela na §2; achados "
             "na §5; erratas na §6; resíduo do operador na §8)"),
    "artefatos": [
        p("4_RELATORIO", "RELATORIO_FINAL.md"),
        p("2_OPTICO", "RESULTADO_OPTICO.json"),
        p("2_OPTICO", "ACHADOS_FORA_DO_PREREGISTRO.json"),
        p("2_OPTICO", "diagnostico", "DIAGNOSTICO_T9c.json"),
        p("3_KERNEL", "RESULTADO_KERNEL.json"),
        p("3_KERNEL", "ACHADOS_FORA_DO_PREREGISTRO.json"),
        p("3_KERNEL", "sandbox", "TheTimeHasNoRank.lean"),
        p("3_KERNEL", "sandbox", "TheTimeHasNoRank.olean"),
        p("4_RELATORIO", "AUDITORIAS", "MANIFESTO_COPIA_AUDITORIAS.json"),
        p("4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_REPRO", "saidas", "A4_CALCULO_INDEPENDENTE.json"),
        p("4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_REPRO", "lean_sandbox", "SondasAuditorTempo.lean"),
        p("4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_ESTATUTO", "sandbox", "AudEstatutoTempo.lean"),
        p("4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_ESTATUTO", "sandbox", "AudEstatutoTempo2.lean"),
        p("4_RELATORIO", "AUDITORIAS", "TEMPO_AUD_ESTATUTO", "sandbox", "AudEstatutoTempo3.lean"),
        p("4_RELATORIO", "saidas", "CONFERENCIA_HASHES.json"),
        p("4_RELATORIO", "saidas", "BETA_RUNTIME_RELATORIO.json"),
    ],
    "refs": REFS,
    "nota": ("Duas auditorias independentes (reprodução; estatuto e regra) disseram que a unidade não pode fechar como está. "
             "Elas divergem só na gravidade de V-GERAL-1: material para a instalação, baixa para o veredito por afirmação. "
             "Para T3 vale PASSA com ressalva. Um PASSA é validade matemática na face testada, não creditação; o gate não se "
             "move; β na natureza a 5σ não é tocado. A evidência das auditorias foi copiada por bytes para "
             "4_RELATORIO\\AUDITORIAS (71 arquivos idênticos)."),
}


def carregar_rotas():
    spec = importlib.util.spec_from_file_location("rotas_somente_leitura", ROTAS_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gravar(nome, obj):
    out = os.path.join(BASE, nome)
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    with open(out + ".tmp", "wb") as f:
        f.write(b)
    if open(out + ".tmp", "rb").read() != b:
        raise SystemExit("FALHA VISIVEL: temporario nao confere: " + out)
    os.replace(out + ".tmp", out)
    return out


def main():
    rotas = carregar_rotas()
    regs = rotas._le()  # so leitura do livro (confere a cadeia)
    ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
    seqs = {r["seq"] for r in regs}
    val = {"livro_n_registros": len(regs), "rota_id_ja_existe": RID in ids, "refs_existentes": {}}
    for r in REFS:
        val["refs_existentes"][r] = r in ids
    v1 = rotas._valida(ROTA, ids, seqs)
    v2 = rotas._valida(RESULTADO, ids | {RID}, seqs)
    proibidas = re.compile("CONF" + "IRM|n[aã]o prov" + "ou|p[oó]s-di[cç]+[aã]o", re.I)
    for nome, obj in (("ROTA", ROTA), ("RESULTADO", RESULTADO)):
        txt = json.dumps(obj, ensure_ascii=False)
        val[nome] = {"valida_a_seco": True, "palavras_proibidas": proibidas.findall(txt),
                     "maior_campo_de_texto": max(len(str(obj[k])) for k in obj if isinstance(obj[k], str)),
                     "artefatos": [(a["caminho"], a["sha256"][:16], a["bytes"])
                                   for a in (v1 if nome == "ROTA" else v2).get("artefatos", [])]}
    f1 = gravar("registro_rota_F1.TEMPO.json", ROTA)
    f2 = gravar("registro_mapa_F1.TEMPO.json", RESULTADO)
    val["arquivos"] = [f1, f2]
    val["nota"] = ("Validação a seco com rotas._valida (lê arquivos e calcula sha256; não escreve). Registrar é ato da "
                   "gerência: primeiro registro_rota_F1.TEMPO.json, depois registro_mapa_F1.TEMPO.json.")
    out = os.path.join(BASE, "saidas", "VALIDACAO_REGISTROS.json")
    with open(out + ".tmp", "wb") as f:
        f.write(json.dumps(val, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(out + ".tmp", out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(val, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

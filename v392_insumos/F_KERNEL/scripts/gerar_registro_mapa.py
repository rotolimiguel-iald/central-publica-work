# -*- coding: utf-8 -*-
"""Gera registro_mapa_F0.5.json (PROPOSTA; nao registra -- `rotas.py registrar` e ato da gerencia).
Tipo RESULTADO sobre rotas que JA existem (conferidas em rotas.jsonl); artefatos como lista de caminhos;
numeros lidos dos JSON do sandbox. Recusa gravar se houver a palavra proibida (qualquer forma) ou rota inexistente."""
import json
import os
import re

F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INV = json.load(open(os.path.join(F, "INVENTARIO_V392_KERNEL.json"), encoding="utf-8"))
KH = INV["kh_n1"]
RJ = INV["raiz_e_auditoria"]
C = {c["modulo_proposto"].replace("TGLExt.", ""): c for c in INV["candidatas"]}
J = {r["nome"].replace("B_", ""): r for r in INV["conjunto"]}
fin = KH["final"]
d2 = KH["D2"]
tot = KH["formato_umpy_total"]
UL = INV["um_py_linhas"]
P = lambda *a: os.path.join(F, *a)
NOTA = ("exame F_KERNEL de 12/10/2026 (subagente da gerencia c1), so sandbox; 2a execucao (a 1a perdeu os arquivos do proprio "
        "sandbox numa limpeza errada; refeita com os mesmos scripts e os mesmos numeros); artefatos no scratchpad temporario: "
        "copiar para C:\\IALD\\PROGRAMA_IALD\\auditorias antes de registrar")
EX = [P("fp_before.txt"), P("fp_after_lean.txt"), P("INVENTARIO_V392_KERNEL.json"), P("RELATORIO_F_KERNEL_v392.md")]
j1t = J["J1_ConjuntoV392"]["cobertura_total"][0].replace("\t", " ")
j2t = J["J2_ConjuntoV392ComX19"]["cobertura_total"][0].replace("\t", " ")
regs = []
regs.append({
    "tipo": "RESULTADO", "rota_id": "kernel.auditoria.cobertura_axiomas_73_modulos", "dominio": "KERNEL_FORMAL",
    "titulo": "KH-N1 (F0.5 item 2) re-rodado e estendido: os 73 modulos identicos a 07/10; o fecho TGL+TGLExt inteiro (%d modulos, %d constantes) por collectAxioms, 0 fora do trio; por nome exato sao %d os modulos sem nenhuma entrada no axiom_report v391" % (fin["modulos_no_fecho"], fin["constantes"], fin["n_zero"]),
    "pergunta": "a cobertura de 07/10 vale no kernel corrente, e o que falta para o axiom_report cobrir o fecho inteiro?",
    "dados": ["nenhum dado observacional; .olean do kernel do Nos v391 (Lean 4.31.0, toolchain copiado), so leitura"],
    "metodo": "D1: AuditoriaCobertura73.lean de 07/10 (bytes identicos, 71c83b21) re-rodado; D2: enumeracao de todas as constantes do fecho e collectAxioms em 12 blocos paralelos; comparacao por NOME EXATO com core.kernel_formalization.axiom_report (core %s); proposta: run_cmd que imprime no formato do #print axioms, testada nos 76 modulos e no fecho inteiro" % d2.get("core_sha256", fin["core_sha256"])[:16],
    "resultado": "D1 identico a 07/10 (%s linhas; %s); D2: %d constantes, faltam %d, fora do trio %d; distribuicao %s; o axiom_report v391 (%d entradas) bate %d de %d; teoremas %d, no axiom_report %d; modulos sem entrada %d = os 73 + %s; run_cmd no formato do um.py: %s s, %d de %d lidas pela regex do um.py" % (
        KH["D1"]["linhas_novas"], KH["D1"]["total"][0].replace("\t", " "), d2["n"], len(d2["faltam"]), len(d2["fora_do_trio"]),
        json.dumps(d2["distribuicao"], ensure_ascii=False), d2["axr_v391"], d2["em_ambos"] - len(d2["divergentes"]), d2["axr_v391"],
        d2["teoremas"], d2["teoremas_no_axr"], fin["n_zero"], ", ".join(fin["zero_fora_dos_73"]), tot["segundos"],
        tot["lidos_pela_regex_do_umpy"], d2["n"]),
    "veredito": "", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "a cobertura segue fora do kernel (sandbox); o seq 722 diz «50 sem axioma» e o proprio saida_auditoria_73.txt da 49 (382+60+24+49 = 515); a lista KH-N1 casou por sufixo e deixou de fora TheExplosion, O16.PhotonModularRealization e O16.PhotonWitness; 4 nomes do fecho (syntax/elab com «») nao casam a regex do um.py",
    "nao_refazer": "as %d constantes do fecho v391 estao lidas por collectAxioms (0 fora do trio); repetir so com kernel novo (v392)" % d2["n"],
    "proximo_passo": "v392: acrescentar ao TGL/Audit.lean o run_cmd testado (formato do #print axioms) e, no um.py, a checagem de cobertura (toda constante thm do fecho com entrada no axiom_report; os 4 nomes «» como excecao declarada)",
    "onde": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\Nós\\um.py verify_tgl_kernel_formalization (l.%s; regex l.%s)" % (UL["def_verify_tgl_kernel_formalization"][0], UL["regex_depends"][0]),
    "artefatos": [P("RESULTADO_KH_D1.json"), P("RESULTADO_KH_D2.json"), P("kh", "D2_consolidado.json"), P("kh", "KH_N1_final.json"),
                  P("kh", "enumeracao.json"), P("RESULTADO_KH_formato_umpy_76.json"), P("RESULTADO_KH_formato_umpy_total.json"),
                  P("kh", "KH_formato_umpy_total.lean"), P("kh", "AuditoriaCobertura73.lean")] + EX,
    "refs": ["umpy.v391.estatuto_da_prova"], "nota": NOTA})
regs.append({
    "tipo": "RESULTADO", "rota_id": "formal.singularidade_le_atrator", "dominio": "KERNEL_FORMAL",
    "titulo": "F1.ATRATOR na v392: as quatro pedras compilam sozinhas com os .olean da entrega reproduzidos; no conjunto, R1 e ADENDO1 colidem (mesmo namespace, mesmas declaracoes)",
    "pergunta": "as pedras do F1.ATRATOR entram juntas no kernel v391, com as demais candidatas da v392?",
    "dados": ["nenhum dado observacional"],
    "metodo": "etapa A (cada uma sozinha, bytes e leiaute da entrega); etapa B (TGLExt/<Nome>.lean sobre o kernel v391 inteiro: import TGL + import TGLExt + candidatas; collectAxioms em toda constante dos modulos novos); sonda P3 (POSTO = RANK ao lado do A4, so sandbox)",
    "resultado": "sozinhas: rc 0, .olean = entrega (d8fdec78, 80017790, 1627cd0d, 242d5b37); conjunto J1 (ADENDO1 + ponte otica + luz + demais): rc 0, %s; J0 (R1 + ADENDO1): rc 1, «environment already contains 'TGLExt.TheSingularityReadsTheAttractor.fixedSpace'»; P3: A4_reading_rank_one (finrank da imagem da leitura = 1) compila no trio" % j1t,
    "veredito": "", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "R1 e ADENDO1 nao coexistem: so uma entra (o ADENDO1 e a R1 com as quatro cunhagens no comentario); A3_angular_rereading_only e A5_angular_rereading_only reexportam observing_adds_nothing (rfl)",
    "nao_refazer": "a compilacao conjunta e a colisao estao medidas por log; a escolha R1/ADENDO1 e da gerencia",
    "proximo_passo": "v392: instalar o ADENDO1 (TGLExt/TheSingularityReadsTheAttractorAdendo1.lean), a ponte otica e a luz; POSTO = RANK ao lado do A4 so por decisao (sonda P3 disponivel)",
    "onde": "TGLExt.TheSingularityReadsTheAttractor (namespace), F1Atrator.OpticalPopulation, TGLExt.TheLightReadsItself",
    "artefatos": [P("RESULTADO_A_sozinhas.json"), P("RESULTADO_B_modulos.json"), P("RESULTADO_B_conjunto.json"),
                  P("logs", "B", "B_J0_ColisaoR1Adendo1_r1.log"), P("conj", "P3_PostoRankA4.lean"), P("RESULTADO_P_palavra.json")] + EX,
    "refs": ["kernel.leitura_cria_o_objeto_07out"], "nota": NOTA})
regs.append({
    "tipo": "RESULTADO", "rota_id": "kernel.leitura_cria_o_objeto_07out", "dominio": "KERNEL_FORMAL",
    "titulo": "PALAVRA na v392: compila sozinha e no conjunto; nao usa nem duplica a letra (exact_witness_of_annihilating_word, annihilating_word_exists)",
    "pergunta": "a PALAVRA entra no kernel v391 com as demais candidatas, e qual a sua relacao com a letra?",
    "dados": ["nenhum dado observacional"],
    "metodo": "etapas A e B; sonda P1 (constantes usadas pelos termos; igualdade por rfl dos enunciados); sonda P1c (fecho transitivo de constantes restrito ao kernel)",
    "resultado": "sozinha rc 0, 7 de 7 no trio, 0 aviso; conjunto J1 rc 0; o fecho de constantes das 7 declaracoes tem 41 constantes em 7 modulos e nao contem as duas da letra; rereading_adds_nothing = observing_adds_nothing e the_first_reading_identifies = the_observer_reads_the_angle (rfl)",
    "veredito": "", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "a letra so aparece no comentario (nome); os imports O16.PeriodHeatCalibration_v3 e O16.RotationGeneratorBridges nao entram no fecho de constantes (mais largos que o uso)",
    "nao_refazer": "a relacao PALAVRA x letra esta medida por termo",
    "proximo_passo": "v392: TGLExt/Palavra.lean + import na raiz + 7 #print axioms no Audit; o F1.ATRATOR nao precisa importar a PALAVRA para compilar",
    "onde": "TGLExt.Palavra",
    "artefatos": [P("conj", "P1_PalavraEaLetra.lean"), P("conj", "P1c_FechoTransitivoPalavra.lean"), P("RESULTADO_P_palavra.json")] + EX,
    "refs": ["formal.singularidade_le_atrator"], "nota": NOTA})
regs.append({
    "tipo": "RESULTADO", "rota_id": "formal.f2_3.curved_field_ligand", "dominio": "KERNEL_FORMAL",
    "titulo": "F2.3 na v392: o ligante entra como TGLExt.LiganteLeiCampoCurvo com o .olean da entrega byte a byte; S7/S8 entram como modulo proprio (TGLExt.LiganteLeiCampoCurvoTestemunha)",
    "pergunta": "o ligante auditado e as sondas S7/S8 compilam juntos sobre o kernel v391 com as demais candidatas?",
    "dados": ["nenhum dado observacional"],
    "metodo": "etapa A (ligante; TestemunhaF23 da auditoria); etapa B (S7/S8 = 4 imports + 2 set_option + os bytes de testemunha_parte.lean, sem a copia do ligante); conjunto J1",
    "resultado": "ligante: rc 0, .olean f76c372e = entrega (no leiaute TGLExt); S7/S8: rc 0, %s; no conjunto: %s" % (json.dumps(C["LiganteLeiCampoCurvoTestemunha"]["conjunto_J1"]), j1t),
    "veredito": "", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "o TestemunhaF23.lean da auditoria repete o ligante (nao instalavel junto); o comentario de S7/S8 diz «NADA disto e pedra»: na instalacao, errata ao lado; namespace AuditF23Flat",
    "nao_refazer": "a compilacao conjunta esta medida",
    "proximo_passo": "v392: TGLExt/LiganteLeiCampoCurvo.lean + TGLExt/LiganteLeiCampoCurvoTestemunha.lean (texto final da gerencia), imports na raiz, #print axioms no Audit; ramo C e Temperatura fora (F0.5 (l))",
    "onde": "ChatgptAudit.F23CurvedFieldLigand; AuditF23Flat",
    "artefatos": [P("inst", "TGLExt", "LiganteLeiCampoCurvoTestemunha.lean"), P("RESULTADO_B_modulos.json"), P("RESULTADO_B_conjunto.json")] + EX,
    "refs": [], "nota": NOTA})
regs.append({
    "tipo": "RESULTADO", "rota_id": "formal.f1_2.v351_dual_scaling_bridge", "dominio": "KERNEL_FORMAL",
    "titulo": "F1.2 na v392: a ponte V351DualScalingBridge entra com os bytes da entrega; a AgapeNonVacuity entra com UMA linha de import trocada (F12Completion.* -> TGLExt.*)",
    "pergunta": "a ponte e a nao vacuidade da Agape compilam no leiaute do kernel e juntas com as demais candidatas?",
    "dados": ["nenhum dado observacional"],
    "metodo": "etapa A (leiaute da entrega: .olean 940b8ddf e ba0d9868 reproduzidos); etapa B (TGLExt/V351DualScalingBridge.lean e TGLExt/AgapeNonVacuity.lean); conjunto J1; demonstracao da resolucao da raiz TGLExt (B0)",
    "resultado": "sozinhas: rc 0, .olean = entrega; instaladas: rc 0; conjunto: ponte %s, Agape %s; B0: com o LEAN_PATH comecando no kernel do Nos e a ponte numa pasta extra, o import TGLExt.V351DualScalingBridge falha (rc 1)" % (json.dumps(C["V351DualScalingBridge"]["conjunto_J1"]), json.dumps(C["AgapeNonVacuity"]["conjunto_J1"])),
    "veredito": "", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "a troca da linha de import muda os bytes da Agape (o .olean instalado nao e o da entrega); a face M_n x| R segue [OPEN]; MatrixInnerGauge nao esta no item (k)",
    "nao_refazer": "a compilacao conjunta esta medida",
    "proximo_passo": "v392: as duas pedras no kernel, a linha trocada auditada ao lado",
    "onde": "TGLV351 (ponte); F12Completion (Agape)",
    "artefatos": [P("inst", "TGLExt", "AgapeNonVacuity.lean"), P("RESULTADO_A_sozinhas.json"), P("RESULTADO_B_modulos.json"),
                  P("RESULTADO_B0_resolucao_raiz.json")] + EX,
    "refs": ["programa.auditoria.f1_2_ponte_v351_07out"], "nota": NOTA})
regs.append({
    "tipo": "RESULTADO", "rota_id": "formal.f1_3.reconcile_v376_mathlib_plan", "dominio": "KERNEL_FORMAL",
    "titulo": "X19 (so teste): LightNetStandardWedgeDataBGL coexiste com o kernel v391 e com as candidatas da v392",
    "pergunta": "se o operador decidir pela X19, ela compila junto?",
    "dados": ["nenhum dado observacional"],
    "metodo": "etapa A (bgl e statement); conjunto J2 = J1 + TGLExt.LightNetStandardWedgeDataBGL; delta de auditoria X19",
    "resultado": "sozinha rc 0 (19 #print no trio; 1 aviso push_neg); J2: %s; delta X19: %d de %d lidas pela regex do um.py" % (j2t, RJ["x19_delta"]["lidos"], RJ["x19_delta"]["n"]),
    "veredito": "", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
    "defeito": "o statement e subconjunto do bgl (mesmo namespace AuditF13v31): entra so um; nao ha habitante (campos [OPEN])",
    "nao_refazer": "a coexistencia esta medida",
    "proximo_passo": "decisao do operador (X19)",
    "onde": "AuditF13v31",
    "artefatos": [P("RESULTADO_B_conjunto.json"), P("RESULTADO_C_delta_x19.json")] + EX,
    "refs": [], "nota": NOTA})

ids = set()
for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8"):
    l = l.strip()
    if l:
        r = json.loads(l)
        if r.get("rota_id"):
            ids.add(r["rota_id"])
for r in regs:
    assert r["rota_id"] in ids, ("rota inexistente", r["rota_id"])
    for a in r["artefatos"]:
        assert isinstance(a, str), a
txt = json.dumps(regs, ensure_ascii=False, indent=1)
assert not re.search(r"confirm", txt, re.I), "palavra proibida"
assert not re.search(r"p[oó]s-?di[cç][aã]o", txt, re.I)
alvo = os.path.join(F, "registro_mapa_F0.5.json")
open(alvo, "w", encoding="utf-8").write(txt + "\n")
faltam = [a for r in regs for a in r["artefatos"] if not os.path.exists(a)]
print(alvo, len(regs), "registros; artefatos ainda inexistentes:", faltam)

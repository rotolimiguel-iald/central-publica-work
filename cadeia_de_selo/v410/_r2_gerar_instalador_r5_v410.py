# -*- coding: utf-8 -*-
"""_r2_gerar_instalador_r5_v410.py -- gera _r2_instalar_pedra_r5_v410.py a partir do instalador da R4 (_r1_parteB_instalar_pedra_r4_v410.py), por trocas EXATAS (cada uma conferida): a pedra AEscala R5 (ordem da gerencia de 10/11 08:42; D100, D101) substitui a R4; a IALD2 segue a da R3.
No recibo dos nomes: os 6 nomes novos da R5 lidos do recibo do autor; RATIFICADOS pela D101: os 13 da R3, os 5 da R4, os 4 da R5 dados pela gerencia e os 3 campos; PENDENTES de ratificacao: so' os 2 auxiliares da autoria. A lista antiga nomes_novos_a_ratificar fica com todos (24) ate' o delta passar a ler os campos novos."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); t = open(os.path.join(HERE, "_r1_parteB_instalar_pedra_r4_v410.py"), encoding="utf-8").read()


def tr(a, b, n=1):
    global t
    c = t.count(a); assert c == n, (c, n, a[:110]); t = t.replace(a, b)


tr('"R4_o_leitor_e_a_escala"', '"R5_tetelestai_um_menos_beta"')
tr('RECIBO_AESCALA_R4_10nov.json', 'RECIBO_AESCALA_R5_10nov.json', t.count('RECIBO_AESCALA_R4_10nov.json'))
tr('"cd45cf1528269760d9b70d860c11185ef3f825817d1e90d92895955759d3d194"', '"e4570f85566074fc9ad2b80bffcddc24da2333a7b0d890654aa72df864b32d67"')
tr('"e61f4801b0caea60b188ef21013b2d9306ec8945aeb92f4146fd6b90c6b067c5"', '"a2df3099c4843b56df146e889d60652ef83059a31a5fcf3055444a8d0512f84a"')
tr('RA["aescala_r4"]', 'RA["aescala_r5"]')
tr('assert RA["nomes_da_R3_incluindo_os_44_ratificados"]["sumidos"] == [] and RA["frases_vedadas_presentes"] == [], (RA["nomes_da_R3_incluindo_os_44_ratificados"]["sumidos"], RA["frases_vedadas_presentes"])',
   'assert RA["os_62_nomes_da_R4"]["n_mantidos"] == 62 and RA["os_62_nomes_da_R4"]["sumidos"] == [] and RA["os_62_nomes_da_R4"]["enunciados_que_mudaram"] == [] and RA["frases_vedadas_presentes"] == [] and RA["beta_literal_na_pedra"] in (False, [], 0, "nenhum", None) or not RA.get("beta_literal_na_pedra"), (RA["os_62_nomes_da_R4"]["sumidos"], RA["frases_vedadas_presentes"], RA.get("beta_literal_na_pedra"))')
tr('NOVOS_R3 = list(MA.get("nomes_novos_a_ratificar_r3") or MA["nomes_novos_a_ratificar"]); NOVOS_R4 = list(RA["nomes_novos"]["lista"]); CAMPOS = list(MA["campos_novos_da_estrutura"])',
   'NOVOS_R3 = list(MA["nomes_novos_a_ratificar_r3"]); NOVOS_R4P = list(MA["nomes_novos_a_ratificar_r4"]); NOVOS_R4 = list(RA["nomes_novos"]["lista"]); CAMPOS = list(MA["campos_novos_da_estrutura"])   # (NOVOS_R4 guarda aqui os nomes novos da R5, lidos do recibo do autor)\n'
   'DADOS_D100 = list(RA["nomes_novos"]["dados_pela_gerencia_D100"]); AUX_R5 = list(RA["nomes_novos"]["auxiliares_da_autoria"])')
tr('NOVOS_R4_DA_ORDEM = ["o_leitor_e_a_escala", "cada_ciclo_aplica_a_mesma_regra", "os_passos_sao_o_ciclo_ate_o_tetelestai", "a_mentira_lida_como_mentira_e_verdade", "o_pai_da_mentira_so_nao_reconhece"]',
   'NOVOS_R4_DA_ORDEM = ["o_tetelestai_e_um_menos_beta", "o_sistema_reconhece_a_singularidade_do_sinal", "beta_e_o_operador_modular_do_tetelestai", "a_informacao_completa_se_reconstroi", "a_flutuacao_do_fundo_e_cotada", "ate_meio_o_tempo_do_tetelestai_nao_e_negativo"]\n'
   'assert len(NOVOS_R4P) == 5 and sorted(DADOS_D100) == sorted(NOVOS_R4_DA_ORDEM[:4]) and sorted(AUX_R5) == sorted(NOVOS_R4_DA_ORDEM[4:]) and not (set(NOVOS_R4P) & set(NOVOS_R4))')
tr('NOVOS = NOVOS_R3 + NOVOS_R4\n', 'NOVOS = NOVOS_R3 + NOVOS_R4P + NOVOS_R4\nSEIS_DE_ENUNCIADO_MUDADO = ["LeitorDoFundo", "aPerguntaDoClay", "iald", "a_pergunta_do_clay_tem_resposta", "existe_o_algoritmo_e_e_a_iald", "a_escala"]; assert all(n_ in MA["nomes"] for n_ in SEIS_DE_ENUNCIADO_MUDADO)\n')
tr('"(13 da R3 +", len(NOVOS_R4), "da R4)', '"(13 da R3 + 5 da R4 +", len(NOVOS_R4), "da R5; pendentes de ratificacao so\' os auxiliares:", AUX_R5, ")')
tr('"_r4")', '"_r5")')
tr('"_pre_r4")', '"_pre_r5")')
tr('"AEscala_fonte_R3"', '"AEscala_fonte_R4"'); tr('"AEscala_instalada_R3"', '"AEscala_instalada_R4"')
tr('INS / "AEscala_R3_pre_r4.lean"', 'INS / "AEscala_R4_pre_r5.lean"'); tr('"compile_log_AEscala_R4.txt"', '"compile_log_AEscala_R5.txt"')
tr('r4 = {"decisao": "D93/D94"', 'r4 = {"decisao": "D100/D101"')
tr('MA.update({"sha256_r3": MA["sha256"],', 'MA.update({"sha256_r4": MA["sha256"],')
tr('"nomes_novos_a_ratificar_r3": list(NOVOS_R3), "nomes_novos_a_ratificar_r4": list(NOVOS_R4), "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS), "r4": r4})',
   '"nomes_novos_r5": list(NOVOS_R4), "nomes_novos_a_ratificar": list(NOVOS), "campos_novos_da_estrutura": list(CAMPOS), "r5": r4,\n'
   '           "ratificados_D101": list(NOVOS_R3) + list(NOVOS_R4P) + list(DADOS_D100), "campos_ratificados_D101": list(CAMPOS), "pendentes_de_ratificacao": list(AUX_R5), "enunciado_mudado_ratificados_D101": list(SEIS_DE_ENUNCIADO_MUDADO),\n'
   '           "nota_D101": "RATIFICADOS pelo operador em 10/11/2026 (D101): os 13 nomes novos da R3, os 5 da R4, os 4 da R5 dados pela gerencia e os 3 campos; os 6 de enunciado mudado, ratificados em 09/11 pelo nome e em 10/11 com o enunciado novo; PENDENTES so\' os 2 auxiliares da autoria; a lista nomes_novos_a_ratificar fica com todos os nomes novos ate\' o delta ler os campos acima"})')
tr('candidata_r4=str(R4 / "AEscala.lean"), candidata_r4_sha256=', 'candidata_r5=str(R4 / "AEscala.lean"), candidata_r5_sha256=')
tr('REC["r4_d94"] = {', 'REC["r5_d100_d101"] = {')
tr('"pedra AEscala R4 instalada pelo construtor por ordem da gerencia (D93/D94: a resposta do operador): o leitor E\' a escala; os passos SAO o ciclo ate\' o Tetelestai; a IALD2 e\' a da R3; os 44 ratificados ficam; os nomes novos (R3 e R4) ficam a ratificar"',
   '"pedra AEscala R5 instalada pelo construtor por ordem da gerencia (D100: a clausula do Tetelestai e\' a de 1 - beta, por ordem do operador; D101: a ratificacao de 10/11); a IALD2 e\' a da R3; pendentes de ratificacao so\' os dois auxiliares da autoria"')
tr('eA.update({"sha256_r3": eA["sha256"],', 'eA.update({"sha256_r4": eA["sha256"],')
tr('"pedra_R4_o_leitor_e_a_escala_D94__44_nomes_ratificados_D87__nomes_novos_a_ratificar"', '"pedra_R5_o_tetelestai_e_um_menos_beta_D100__nomes_ratificados_D87_e_D101__dois_auxiliares_a_ratificar"')
tr('"recibo_do_autor_r4": ', '"recibo_do_autor_r5": '); tr('"recibo_do_autor_r4_sha16": ', '"recibo_do_autor_r5_sha16": ')
tr('BD["r4_d94"] = ', 'BD["r5_d100"] = ')
tr('print("INSTALADA a R4:', 'print("INSTALADA a R5:')
tr('print("AEscala R4: fonte"', 'print("AEscala R5: fonte"')
tr('"| ancoras novas sobre a R3:"', '"| ancoras novas sobre a R4:"')
t = t.replace("_r1_parteB_instalar_pedra_r4_v410.py -- R1, PARTE B (ordem da gerencia de 10/11 00:40, D93/D94): instala a pedra AEscala R4", "_r2_instalar_pedra_r5_v410.py -- R2 (ordem da gerencia de 10/11 08:42, D100/D101): instala a pedra AEscala R5 [gerado de _r1_parteB_instalar_pedra_r4_v410.py por _r2_gerar_instalador_r5_v410.py; onde o texto abaixo disser R4 como pasta de origem, leia-se R5]", 1)
ast.parse(t); p = os.path.join(HERE, "_r2_instalar_pedra_r5_v410.py"); open(p + ".tmp", "w", encoding="utf-8", newline="").write(t); os.replace(p + ".tmp", p); print("gerado", p)

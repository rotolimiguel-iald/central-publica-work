# -*- coding: utf-8 -*-
"""_r5ag_15_pos_rito_v410.py -- R5 (D100 e D101; ADENDOS 5 e 6): o pos-rito: (a) o estatuto dos nomes novos e' RATIFICADOS (o avesso das checagens antigas) em textos_v410, textos_custodia_handoff, gerar_x_custodia, fechar, leitura e registrar_mapa; (b) os textos dizem a ratificacao D101 (os nomes novos RATIFICADOS em 10/11 e os dois auxiliares pendentes);
(c) a secao da escala (Atlas), o handoff e o README trazem a clausula do Tetelestai em 1 - beta com a clausula do limite ao lado, a reconstrucao, a errata E36 as claras (a leitura do dicionario) e a citacao do dispositivo com as ressalvas ([PILOTO][SIM]; nada ali valida fisica; nenhum numero de desempenho);
(d) o post do X traz a clausula e a errata, sem a citacao do dispositivo; (e) a leitura exige a c13, a clausula R5 e a ratificacao D101 do registro no core; (f) a forma de custodia recusa texto que anuncia a clausula sem a clausula do limite."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _r5ag_lib_v410 import aplicar

HERE = os.path.dirname(os.path.abspath(__file__))
FLIP = '''"RATIFICADOS pelo operador em 10/11/2026" in str(%s.get("estatuto_dos_nomes_novos")) and "a ratificar" not in str(%s.get("estatuto_dos_nomes_novos"))'''

# ------------------------------------------------------------------ textos_v410.py (a secao da escala do Atlas e o README)
T = []
T.append(('''and "RATIFICADO" not in str(ea.get("estatuto_dos_nomes_novos")).upper() and ea.get("ratificacao_pendente")''', '''and ''' + FLIP % ("ea", "ea") + ''' and ea.get("ratificacao_pendente")''', 1))
T.append(('''"n_nomes_novos": len(DL_.NOMES_NOVOS_AESCALA), "n_campos_novos": len(DL_.CAMPOS_NOVOS_AESCALA), "estatuto_novos": DL_.ESTATUTO_NOMES_NOVOS_AESCALA, "nomes_novos_lista": ", ".join(DL_.NOMES_NOVOS_AESCALA),''',
          '''"n_nomes_novos": len(DL_.NOMES_RATIFICADOS_D101_AESCALA), "n_campos_novos": len(DL_.CAMPOS_RATIFICADOS_D101_AESCALA), "estatuto_novos": DL_.ESTATUTO_NOMES_NOVOS_AESCALA, "nomes_novos_lista": ", ".join(DL_.NOMES_RATIFICADOS_D101_AESCALA), "n_pend": len(DL_.NOMES_PENDENTES_AESCALA), "pend_lista": ", ".join(DL_.NOMES_PENDENTES_AESCALA),''', 1))
T.append(('''os %(n_nomes_novos)d nomes novos da `AEscala` (R3) e os %(n_campos_novos)d campos novos da estrutura NÃO estão ratificados, são A RATIFICAR por ele, %(estatuto_novos)s: %(nomes_novos_lista)s). [OPEN]''',
          '''os %(n_nomes_novos)d nomes novos da `AEscala` (R3, R4 e R5) e os %(n_campos_novos)d campos novos da estrutura ele ratificou em 10/11 (D101, pela regra do nome: %(estatuto_novos)s): %(nomes_novos_lista)s; só a confirmação expressa dos %(n_pend)d nomes auxiliares da autoria (%(pend_lista)s) é dele, e eles seguem [DECLARADO pela autoria]). [OPEN]''', 1))
T.append(('''    novos = ("**Os nomes novos da pedra (R3) e a ponte da escala** [DECLARADO os nomes e os campos novos, pela gerência e pela autoria; a ratificar pelo operador · DERIVED a ponte, aritmética recalculada por `Fraction` e por `exp` e `log`]**:** a pedra traz %d nomes novos de declarações (%s) e %d campos novos da estrutura `LeitorDoFundo` (%s): %s, ainda NÃO ratificados; os %d nomes anteriores seguem ratificados (D87). "''',
          '''    novos = ("**Os nomes novos da pedra (R3, R4 e R5) e a ponte da escala** [INPUT ratificados pelo operador em 10/11, D101 · DECLARADO pela autoria os dois auxiliares · DERIVED a ponte, aritmética recalculada por `Fraction` e por `exp` e `log`]**:** a pedra traz %d nomes novos de declarações (%s) e %d campos novos da estrutura `LeitorDoFundo` (%s). " + DL_.costura_maiuscula(DL_.FRASE_NOMES_RATIFICADOS_D101_PT) + "; os %d nomes anteriores seguem ratificados (D87). "''', 1))
T.append((''', ", ".join("`%s`" % x_ for x_ in ea["campos_novos_da_estrutura"]), ea["estatuto_dos_nomes_novos"], len(DL_.NOMES_AESCALA),''', ''', ", ".join("`%s`" % x_ for x_ in ea["campos_novos_da_estrutura"]), len(DL_.NOMES_AESCALA),''', 1))
T.append(('''    reg = ("**O que o registro NÃO diz** [REAL]: "''',
          '''    tet = ("**A cláusula do Tetelestai em 1 − β (R5, D100)** [INPUT a fala, do operador · REAL os teoremas, no trio · dicionário a leitura do operador · PILOTO/SIM a citação do dispositivo]**:** O operador, em 10/11: %s; %s; %s; %s; %s. " % (_cita(DL_.FRASE_CLAUSULA_NO_ACOM), _cita(DL_.FRASE_RECONHECE_A_SINGULARIDADE), _cita(DL_.FRASE_TRASLADA_A_INFORMACAO), _cita(DL_.FRASE_UM_MENOS_BETATGL), _cita(DL_.FRASE_BETATGL_OPERADOR_MODULAR))
           + DL_.FRASE_TETELESTAI_PT + ". " + DL_.CLAUSULA_Z_PT + " " + DL_.FRASE_RECONSTROI_PT + ". [INPUT/dicionário] " + DL_.FRASE_E36_PT + ". [PILOTO][SIM] " + DL_.FRASE_DISPOSITIVO_PT + ".")
    reg = ("**O que o registro NÃO diz** [REAL]: "''', 1))
T.append(('''return _sem_chaves("\\n\\n".join([cab, pesos, insig, dois, clay, tipo, rat, novos, reg]))''', '''return _sem_chaves("\\n\\n".join([cab, pesos, insig, dois, clay, tipo, tet, rat, novos, reg]))''', 1))
aplicar("textos_v410.py", T, base=HERE)

# ------------------------------------------------------------------ textos_custodia_handoff_v410.py (o handoff e o README)
T = []
T.append(('''and "RATIFICADO" not in EA["estatuto_dos_nomes_novos"].upper(), "o registro a_escala_v410 nao traz''', '''and ''' + FLIP % ("EA", "EA") + ''', "o registro a_escala_v410 nao traz''', 1))
T.append(('''ESCALA_TIPO_PT = ("A escala no tipo (R4):''',
          '''TET_PT = ("A cláusula do Tetelestai em 1 − β (R5, D100) [REAL os teoremas, no trio; INPUT/dicionário a leitura do operador; PILOTO/SIM a citação do dispositivo]: " + DL.FRASE_TETELESTAI_PT + ". " + DL.CLAUSULA_Z_PT + " " + DL.FRASE_RECONSTROI_PT + ". [INPUT/dicionário] " + DL.FRASE_E36_PT + ". [PILOTO][SIM] " + DL.FRASE_DISPOSITIVO_PT + ".")   # (R5, D100: a clausula do Tetelestai em 1 - beta, a clausula do limite logo depois, a errata E36 as claras e a citacao do dispositivo so' com as ressalvas)
TET_EN = ("The clause of the Tetelestai in 1 − β (R5, D100) [REAL the theorems, in the trio; INPUT/dictionary the operator's reading; PILOTO/SIM the device citation]: " + DL.FRASE_TETELESTAI_EN + ". " + DL.CLAUSULA_Z_EN + " " + DL.FRASE_RECONSTROI_EN + ". [INPUT/dictionary] " + DL.FRASE_E36_EN + ". [PILOTO][SIM] " + DL.FRASE_DISPOSITIVO_EN + ".")
assert all("%" not in x_ for x_ in (TET_PT, TET_EN)), "a clausula do Tetelestai traz «%%» (o formato dos textos quebraria)"
ESCALA_TIPO_PT = ("A escala no tipo (R4):''', 1))
T.append(('''e a mentira lida como mentira é verdade. " + CLZ_PT + " " + TEMPO_PT_C + ".")''', '''e a mentira lida como mentira é verdade. " + CLZ_PT + " " + TEMPO_PT_C + ". " + TET_PT)''', 1))
T.append(('''and a lie read as a lie is truth. " + CLZ_EN + " " + TEMPO_EN_C + ".")''', '''and a lie read as a lie is truth. " + CLZ_EN + " " + TEMPO_EN_C + ". " + TET_EN)''', 1))
T.append(('''NOVOS_PT = fm("A pedra, nas R3 e R4, traz %(nomes_novos)d nomes novos de declarações (" + ", ".join(DL.NOMES_NOVOS_AESCALA) + ") e %(campos_novos)d campos novos da estrutura (" + ", ".join(DL.CAMPOS_NOVOS_AESCALA) + "): são " + DL.ESTATUTO_NOMES_NOVOS_AESCALA + ", não estão ratificados; os %(nomes_aescala)d nomes anteriores seguem ratificados (D87).") + " " + SEIS_PT''',
          '''NOVOS_PT = fm("A pedra, nas R3, R4 e R5, traz %(nomes_novos)d nomes novos de declarações (" + ", ".join(DL.NOMES_NOVOS_AESCALA) + ") e %(campos_novos)d campos novos da estrutura (" + ", ".join(DL.CAMPOS_NOVOS_AESCALA) + "). ") + DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_PT) + fm("; os %(nomes_aescala)d nomes anteriores seguem ratificados (D87).") + " " + SEIS_PT''', 1))
T.append(('''NOVOS_EN = fm("The R3 and R4 of the stone bring %(nomes_novos)d new declaration names (" + ", ".join(DL.NOMES_NOVOS_AESCALA) + ") and %(campos_novos)d new fields of the structure (" + ", ".join(DL.CAMPOS_NOVOS_AESCALA) + "): they are [DECLARADO, by the management and by the authorship; to be ratified by the operator], not ratified; the %(nomes_aescala)d earlier names stay ratified (D87).") + " " + SEIS_EN''',
          '''NOVOS_EN = fm("The R3, R4 and R5 of the stone bring %(nomes_novos)d new declaration names (" + ", ".join(DL.NOMES_NOVOS_AESCALA) + ") and %(campos_novos)d new fields of the structure (" + ", ".join(DL.CAMPOS_NOVOS_AESCALA) + "). ") + DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_EN) + fm("; the %(nomes_aescala)d earlier names stay ratified (D87).") + " " + SEIS_EN''', 1))
T.append(('''        if re.search(r"(?<![0-9,.])4[,.]44(?![0-9])", t):''',
          '''        if (DL.FRASE_TETELESTAI_PT in t and DL.CLAUSULA_Z_PT not in t) or (DL.FRASE_TETELESTAI_EN in t and DL.CLAUSULA_Z_EN not in t):   # (R5, D100) todo texto que traz a clausula do Tetelestai em 1 - beta traz a clausula do limite ao lado
            v3.append("%s: traz a clausula do Tetelestai em 1 - beta sem a clausula do limite (D99, D100)" % ident)
        if "ACOM Mirror" in t and not ("[PILOTO][SIM]" in t and re.search(r"nada ali valida f[ií]sica|nothing there validates physics", t)):   # (R5, D100) a citacao do dispositivo so' com as ressalvas
            v3.append("%s: cita o ACOM Mirror sem [PILOTO][SIM] e sem dizer que nada ali valida fisica (D100)" % ident)
        if re.search(r"(?<![0-9,.])4[,.]44(?![0-9])", t):''', 1))
aplicar("textos_custodia_handoff_v410.py", T, base=HERE)

# ------------------------------------------------------------------ gerar_x_custodia_v410.py (o post: a clausula e a errata, sem a citacao do dispositivo)
T = []
T.append(('''and "RATIFICADO" not in str(ea.get("estatuto_dos_nomes_novos")).upper() and ea.get("ratificacao_pendente")''', '''and ''' + FLIP % ("ea", "ea") + ''' and ea.get("ratificacao_pendente")''', 1))
T.append(('''Os {ev['n_nomes_novos']} nomes novos da pedra AEscala (R3 e R4) e os {len(ea['campos_novos_da_estrutura'])} campos novos da estrutura são {DL.ESTATUTO_NOMES_NOVOS_AESCALA}: ainda NÃO ratificados.''',
          '''{DL.costura_maiuscula(DL.FRASE_NOMES_RATIFICADOS_D101_PT)}.''', 1))
T.append(('''· A ordem do operador, de 06/11: «{DL.FRASE_ORDEM_V410}»''',
          '''· A cláusula do Tetelestai em 1 − β (R5, D100), na fala do operador: «{DL.FRASE_UM_MENOS_BETATGL}»; «{DL.FRASE_BETATGL_OPERADOR_MODULAR}». {DL.FRASE_TETELESTAI_PT.replace(chr(96), '')}. {DL.CLAUSULA_Z_PT} {DL.FRASE_E36_PT.replace(chr(96), '')}.

· A ordem do operador, de 06/11: «{DL.FRASE_ORDEM_V410}»''', 1))
aplicar("gerar_x_custodia_v410.py", T, base=HERE)

# ------------------------------------------------------------------ fechar_v410.py, leitura_v410.py, registrar_mapa_v410.py
aplicar("fechar_v410.py", [('''and "RATIFICADO" not in str(_ea.get("estatuto_dos_nomes_novos")).upper() and _ea.get("ratificacao_pendente")''', '''and ''' + FLIP % ("_ea", "_ea") + ''' and _ea.get("ratificacao_pendente")''', 1)], base=HERE)
aplicar("leitura_v410.py", [('''and 'RATIFICADO' not in str(ea_.get('estatuto_dos_nomes_novos')).upper() and ea_.get('ratificacao_pendente')''',
                              '''and 'RATIFICADOS pelo operador em 10/11/2026' in str(ea_.get('estatuto_dos_nomes_novos')) and 'a ratificar' not in str(ea_.get('estatuto_dos_nomes_novos')) and (ea_v_.get('tetelestai') or {}).get('ok') is True and (ea_v_.get('clausula_r5') or {}).get('ok') is True and (ea_v_.get('ratificacao_d101') or {}).get('ok') is True
                        and list((ea_v_.get('ratificacao_d101') or {}).get('pendentes') or []) == list(DL_.NOMES_PENDENTES_AESCALA) and ea_.get('ratificacao_pendente')''', 1),
                             ('''os nomes novos e os campos novos da pedra ditos A RATIFICAR''', '''os nomes novos e os campos novos da pedra ditos RATIFICADOS em 10/11 (D101) e os dois auxiliares da autoria ditos [DECLARADO pela autoria]''', 1)], base=HERE)
aplicar("registrar_mapa_v410.py", [('''and "RATIFICADO" not in str(ea.get("estatuto_dos_nomes_novos")).upper() and ea.get("ratificacao_pendente")''', '''and ''' + FLIP % ("ea", "ea") + ''' and ea.get("ratificacao_pendente")''', 1),
                                   ('''"Os %d nomes novos da pedra (R3 e R4) e os %d campos novos da estrutura sao %s: A RATIFICAR pelo operador, ainda NAO ratificados (os %d anteriores foram ratificados na D87);''',
                                    '''"Os %d nomes novos da pedra (R3, R4 e R5) e os %d campos novos da estrutura foram %s, pela regra do nome (so' os %d auxiliares da autoria seguem [DECLARADO pela autoria]; os %d anteriores foram ratificados na D87);''', 1),
                                   ('''FA["n_nomes_novos"], FA["n_campos_novos"], FA["estatuto_novos"], FA["n_nomes"], FA["ponte"]["brilho_de_um_pixel_em_uma_oitava"],''',
                                    '''len(DL_.NOMES_RATIFICADOS_D101_AESCALA), FA["n_campos_novos"], FA["estatuto_novos"], len(DL_.NOMES_PENDENTES_AESCALA), FA["n_nomes"], FA["ponte"]["brilho_de_um_pixel_em_uma_oitava"],''', 1)], base=HERE)

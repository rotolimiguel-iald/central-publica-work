"""Confere, por cálculo, a consistência interna da definição do PsiBit nas patentes.

Replica em Python puro (sem numpy) as duas regras que estão nos arquivos citados:
  - índice (ACOM_Mirror_PI_INPI.tex l.265-270; acom_mirror.py l.43-45):
        psi = 2*[sign(L) < 0] + [sign(dL) > 0]
  - paridade por índice (acom_mirror.py l.32; psi_net_protocol_v1.py l.137; reivindicação 4, l.1082-1089):
        PARITY = [-1, +1, +1, -1]
  - rótulos da tabela (ACOM_Mirror_PI_INPI.tex l.253-260 e reivindicação 2, l.1057-1071):
        psi0=(+,-)  psi1=(+,+)  psi2=(-,+)  psi3=(-,-)   com paridade da tabela [-1,+1,+1,-1]

Imprime, para cada par de sinais (sL, sdL): o índice pela fórmula, a paridade pelo vetor PARITY,
o produto sL*sdL, o sinal de dL, e o par que a TABELA atribui ao mesmo índice.
Só leitura; escreve apenas em stdout.
"""
import json

PARITY = [-1, +1, +1, -1]
TABELA = {0: (+1, -1), 1: (+1, +1), 2: (-1, +1), 3: (-1, -1)}  # índice -> (sign L, sign dL) rotulado na tabela


def indice(sL, sdL):
    return (1 if sL < 0 else 0) * 2 + (1 if sdL > 0 else 0)


linhas = []
ok_formula_e_produto = True
for sL in (+1, -1):
    for sdL in (+1, -1):
        i = indice(sL, sdL)
        par = PARITY[i]
        prod = sL * sdL
        sd = sdL
        tab_par = TABELA[i]
        linhas.append({
            "sL": sL, "sdL": sdL, "indice_pela_formula": i,
            "paridade_PARITY[indice]": par, "produto_sL_x_sdL": prod, "sinal_de_dL": sd,
            "par_que_a_tabela_atribui_ao_indice": list(tab_par),
            "tabela_concorda_com_formula": tab_par == (sL, sdL),
            "paridade_igual_ao_produto": par == prod,
            "paridade_igual_ao_sinal_de_dL": par == sd,
        })
        ok_formula_e_produto = ok_formula_e_produto and (par == prod)

# a paridade da TABELA lida pelo par rotulado
tabela_paridade_por_rotulo = {}
for i, (sL, sdL) in TABELA.items():
    tabela_paridade_por_rotulo[i] = {
        "rotulo": [sL, sdL], "paridade_da_tabela": PARITY[i],
        "produto": sL * sdL, "sinal_de_dL": sdL,
        "paridade_da_tabela_igual_ao_produto_do_rotulo": PARITY[i] == sL * sdL,
        "paridade_da_tabela_igual_ao_sinal_de_dL_do_rotulo": PARITY[i] == sdL,
    }

resumo = {
    "formula_indice_mais_PARITY_dao_paridade_igual_ao_produto_dos_sinais": ok_formula_e_produto,
    "linhas_pela_formula": linhas,
    "tabela_por_rotulo": tabela_paridade_por_rotulo,
    "divergencia_interna": [
        "indice 2: a formula (l.265-270) manda (sL<0, sdL<=0)=(-,-); a tabela (l.257) rotula (-,+)",
        "indice 3: a formula manda (sL<0, sdL>0)=(-,+); a tabela (l.259) rotula (-,-)",
    ],
}
print(json.dumps(resumo, ensure_ascii=False, indent=1))

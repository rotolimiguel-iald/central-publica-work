# -*- coding: utf-8 -*-
"""_adapt_outros_v407.py -- adapta ao conteudo da v407 (O PSION, O CANTO E O PAR) os scripts pequenos do pos_rito que a subida mecanica so' tinha rotulado: chain_pos_rito_v407.sh, gerar_derivacao_pos_rito_v407.py, gerar_x_custodia_v407.py e fila_memoria_v407.py.
(b3_recibo_v407.py ja' foi adaptado antes por outra mao em 03/11 e so' e' REVISADO por mim; nao e' tocado aqui.) Cada troca e' EXATA e conta (assert). Uso: python -B -X utf8 _adapt_outros_v407.py [chain|derivacao|x|fila|todos]"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adaptar_pos_rito_v407 as M


# ------------------------------------------------------------------------------------------------ chain
def chain(M_):
    nome = "chain_pos_rito_v407.sh"
    t, crlf, raw = M_.le(nome)
    if M_.pula(nome, t):
        return
    t = M_.tira_cabecalho(t)
    t = M_.sub(t, "# v407 (O FECHAMENTO, 02/11/2026): CADEIA POS-RITO -- derivada por script (derivar_encanamento_v407.py, lote F) do chain_pos_rito_v406.sh FINAL (a cadeia de CONTEUDO que rodou em 01/11; mesma ordem de passos 0..14 e mesmos portoes)",
               "# v407 (O PSION, O CANTO E O PAR, 03/11/2026): CADEIA POS-RITO -- derivada por script (_bump_copia_v407.py, rotulos) e adaptada por adaptar_pos_rito_v407.py do chain_pos_rito_v406.sh FINAL (a cadeia de CONTEUDO que rodou no pos-rito da v406; mesma ordem de passos 0..14 e mesmos portoes)")
    t = M_.sub(t, "# A v407 e' o FECHAMENTO (as falas do operador de 02/11/2026): UM BUNDLE de 301 modulos novos de kernel (os 300 da bancada do ChatGPT, F1.FECHO_20261015, recompilados do fonte, e a candidata CanonicalFullTGLWitnessR1, de nome PROVISORIO: os nomes das pedras sao do operador; a escada, as bandeiras e o h8 sao lidos de ESPERADOS_v407.json),",
               "# A v407 e' O PSION, O CANTO E O PAR (as falas do operador de 03/11/2026): UM BUNDLE PEQUENO de 9 modulos novos de kernel em TGLExt/ (PsionCanto, Par e as sete pedras de 02/11; os nomes das pedras sao do operador; a escada 11860 -> 11958, as 98 bandeiras e o h8 sao lidos de ESPERADOS_v407.json),")
    t = M_.sub(t, "# UM registro COM FUNCAO (fechamento_v406; lido no main DEPOIS dos da v406) e DOIS por spec (cunhagens_v406 e kh_n1_cobertura_v406). As QUATRO chaves de testemunha deixam de ser literal False e sao LIDAS do kernel do rito (errata E14).",
               "# UM registro COM FUNCAO (psion_canto_v407; lido no main DEPOIS do fechamento_v406 herdado) e DOIS por spec (cunhagens_v407 e kh_n1_cobertura_v407). A CHAVE DO LEMA (testemunha_estatica_v396.fock_face.linked_to_the_corner_by_a_lemma) deixa de ser literal False e e' LIDA do kernel do rito (errata E18); o fechamento_v406, cunhagens_v406 e kh_n1_cobertura_v406 sao HERDADOS, recriados e versionados (E20).")
    t = M_.sub(t, "# Os treze registros da v406, os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais a v406 selada)",
               "# O fechamento_v406 (e os dois por spec da v406), os treze registros da v406 selada, os da v404, da v403, da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais a v406 selada)")
    t = M_.sub(t, "Os paragrafos do testemunho, da falsidade, da ponte, de Caminho, Verdade e Vida, de Jo 8,32 e da massa derivada (v406) seguem como estao; os anteriores recebem a NOTA ao lado (E14).",
               "Os paragrafos do testemunho, da falsidade, da ponte, de Caminho, Verdade e Vida, de Jo 8,32, da massa derivada e do fechamento (v406) seguem como estao; os anteriores recebem a NOTA ao lado (E18: a chave do lema era literal False e passou a leitura do kernel).")
    t = M_.sub(t, "# Estatutos: os termos do fecho sao [REAL] (kernel, no trio); [POSTO] o 1 / u = 1 eV; [MEDIDA] alfa; as leituras do operador de 02/11 entram como [ONTO] e nao sao teoremas; as ressalvas (K(O) != bot so' na cunha; o nucleo II_inf [KNOWN/DECLARADO]; traco ENNReal ciclico; R7 Codex x Codex; R4/R5 fora; o nome provisorio) vao ditas;",
               "# Estatutos: os termos das nove pedras sao [REAL] (kernel, no trio); [POSTO] o 1 / u = 1 eV; [MEDIDA] alfa; as leituras do operador de 03/11 (o graviton como o estado ligado de dois psions; o banho holografico) entram como [ONTO] e nao sao teoremas; as ressalvas (o par na face de Fock [OPEN]; a ponte Bell-TT nao e' termo; K(O) != bot so' na cunha; o nucleo II_inf [KNOWN/DECLARADO]; traco ENNReal ciclico; tres das sete pedras revistas pelo Sonnet; o teste (d) so' por citacao; o motor continuo fora) vao ditas;")
    t = M_.sub(t, "e o NOVO da v407 (o fechamento), mais a NOTA ao lado dos paragrafos anteriores (E14: as quatro chaves de testemunha eram literal e passaram a leitura do kernel); diz que os anteriores seguem como estao;",
               "e o NOVO da v407 (o psion, o canto e o par), mais a NOTA ao lado dos paragrafos anteriores (E18: a chave do lema era literal False e passou a leitura do kernel); diz que os anteriores seguem como estao;")
    t = M_.sub(t, "contrato R3_2: o diff v406 -> v407 e' so' os 301 modulos novos)", "contrato R3_2: o diff v406 -> v407 e' so' os 9 modulos novos)")
    t = M_.sub(t, "(B15 -> n = 15; o b3_recibo_v407.py o confere", "(B15 -> n = 16, o rotulo B16; o b3_recibo_v407.py o confere")
    t = M_.sub(t, "(os tres registros novos);\n", "(os tres registros novos: psion_canto_v407, cunhagens_v407 e kh_n1_cobertura_v407);\n")
    t = M_.sub(t, "diz que os paragrafos do testemunho, da falsidade e da v406 seguem como estao).", "diz que os paragrafos do testemunho, da falsidade e da v406 seguem como estao).")
    t = M_.sub(t, 'REGS="fechamento_v406 cunhagens_v406 kh_n1_cobertura_v406"', 'REGS="psion_canto_v407 cunhagens_v407 kh_n1_cobertura_v407"')
    t = M_.sub(t, "contrato R3_2: os 301 modulos novos tem declaracoes nomeadas", "contrato R3_2: os 9 modulos novos tem declaracoes nomeadas")
    t = M_.sub(t, '.bak_$(date +%Y%m%d_%H%M%S)_v406"; cp -p "$ATLD/$f" "$B"', '.bak_$(date +%Y%m%d_%H%M%S)_v407"; cp -p "$ATLD/$f" "$B"')
    M_.grava(nome, t, crlf, raw)


# ------------------------------------------------------------------------------------------------ gerar_derivacao_pos_rito
def derivacao(M_):
    nome = "gerar_derivacao_pos_rito_v407.py"
    t, crlf, raw = M_.le(nome)
    if M_.pula(nome, t):
        return
    t = M_.tira_cabecalho(t)
    t = M_.sub(t, "sobre o arquivo FINAL da cadeia v406 (o que foi USADO no pos-rito real de 28/10/2026)", "sobre o arquivo FINAL da cadeia v406 (o que foi USADO no pos-rito real da v406)")
    t = M_.sub(t, "A ADAPTACAO (o que o pos-rito diz da v407: o fechamento, com os numeros lidos do rito) foi feita em 02/11/2026 por adaptar_pos_rito_v407.py", "A ADAPTACAO (o que o pos-rito diz da v407: o psion, o canto e o par, com os numeros lidos do rito) foi feita em 03/11/2026 por adaptar_pos_rito_v407.py")
    t = M_.sub(t, '"gerencia c1, 02/11: a leitura da rodada adaptada ao fechamento (leitura_v407; o bundle, as oito ancoras, as quatro chaves; os treze registros da v406 recriados)"',
               '"claude-prep-v407, 03/11: a leitura da rodada adaptada ao psion e ao canto (o bundle de 9 modulos, as 76 ancoras, a chave do lema lida do kernel; o fechamento_v406 herdado e os treze registros da v406 selada recriados)"')
    t = M_.sub(t, '"gerencia c1, 02/11: montado de textos_v407.semente + textos_v407_novo.pysnip (o fechamento; sem prosa nova de conteudo)"', '"claude-prep-v407 (ajudante B1a), 03/11: montado de textos_v407.semente + textos_v407_novo.pysnip (o psion, o canto e o par; sem prosa nova de conteudo)"')
    t = M_.sub(t, '"gerencia c1, 02/11: o harness do pos-rito adaptado ao fechamento"', '"claude-prep-v407, 03/11: o harness do pos-rito adaptado ao psion e ao canto (controles negativos dos registros novos e dos herdados)"')
    t = M_.sub(t, '"gerencia c1, 02/11: o registro da rota umpy.v407.selada_o_fechamento_02nov"', '"claude-prep-v407 (ajudante B1a), 03/11: o registro da rota nova da v407 (o id esta em registrar_mapa_v407.NOVA)"')
    t = M_.sub(t, '"gerencia c1, 02/11: o montador (semente + fragmento; DELETAR as funcoes das oito pedras da v406)"', '"claude-prep-v407 (ajudante B1a), 03/11: o montador (semente + fragmento; DELETAR as funcoes das oito pedras da v405)"')
    t = M_.sub(t, '"gerencia c1, 02/11: o fragmento escrito para a v407 (sem prosa nova de conteudo)"', '"claude-prep-v407 (ajudante B1a), 03/11: o fragmento escrito para a v407 (sem prosa nova de conteudo)"')
    t = M_.sub(t, '"gerencia c1, 02/11: o adaptador do pos-rito (as edicoes exatas por arquivo, com asserts; os blocos novos moram nos _adapt_*_v407.py)"', '"claude-prep-v407, 03/11: o adaptador do pos-rito (os auxiliares; as edicoes exatas por arquivo, com asserts, moram nos _adapt_*_v407.py)"')
    t = M_.sub(t, '("fila_memoria_v407.py", "fila_memoria_v406.py", ', '("fila_memoria_v407.py", "fila_memoria_v406.py", ')
    # os adaptadores _adapt_*_v407.py entram sozinhos (lidos da pasta), sem origem
    t = M_.sub(t, 'rel = []; ruim = []\n', 'SUITE = SUITE + tuple((f_, None, "claude-prep-v407, 03/11: adaptador do pos-rito (edicoes exatas com asserts)") for f_ in sorted(os.listdir(HERE)) if f_.startswith("_adapt_") and f_.endswith("_v407.py"))\nrel = []; ruim = []\n')
    t = M_.sub(t, "a adaptacao foi feita pela gerencia c1 em 02/11/2026 por adaptar_pos_rito_v407.py", "a adaptacao foi feita pela claude-prep-v407 em 03/11/2026 por adaptar_pos_rito_v407.py")
    t = M_.sub(t, '"origem": "pos_rito da v406 FINAL (a cadeia usada no pos-rito real de 28/10), mapa 401 -> 406 e 406 -> 407', '"origem": "pos_rito da v406 FINAL (a cadeia usada no pos-rito real da v406), mapa 405 -> 406 e 406 -> 407')
    M_.grava(nome, t, crlf, raw)


# ------------------------------------------------------------------------------------------------ gerar_x_custodia
X_CORPO = r'''pc = core.get("psion_canto_v407") or {}; pv = pc.get("values") or {}
for k_ in ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407"):
    assert (core.get(k_) or {}).get("all_verified") is True, "um registro da v407 nao selou: o post nao diz isto"
assert pc.get("link_read_from_the_kernel") is True and pv.get("n_modulos_ok") == DL.N_BUNDLE and pv.get("n_flags_true") == pv.get("n_flags") == ESP["n_bandeiras_novas"] and pv.get("n_ancoras_ok") == len(DL.ANCORAS), "os valores do psion_canto_v407 != ESPERADOS/delta"
el = core["external_ladder"]; n_decl = len(core["kernel_formalization"]["axiom_report"])
ress = "; ".join("(%d) %s" % (i + 1, (x.split(":")[0] if ":" in x else x)) for i, x in enumerate(pc["ressalvas"]))
data = datetime.datetime.now().strftime("%d/%m/%Y")
txt = f"""TGL · a versão v407 do programa terminal, custodiada em {data}

O que entrou: o psíon, o canto e o par. {DL.N_BUNDLE} módulos novos no kernel Lean (o PsionCanto, o Par e as sete pedras de 02/11, todas com o nome que o operador deu ou ratificou), com {ESP['n_bandeiras_novas']} bandeiras novas, todas no trio de axiomas padrão do Lean.

· O lema das duas faces está no kernel do rito: nas duas faces o psíon é o vetor de norma 1 cujo canto é o projetor sobre ele. O elo é de estrutura, não de vetores (Ω, o vácuo de Fock, e o vetor de Bell não são identificados). A chave que o programa trazia como literal False desde a v396 passa a ser lida do kernel do próprio rito. A ordem do operador, de 03/11: «{DL.FRASE_LEMA_PSION}».

· O par: {pc['diz'][2]}. A leitura dele, o gráviton como o estado ligado de dois psíons, é [ONTO], não termo de kernel; o par na face de Fock segue [OPEN].

· As ressalvas, ditas: {ress}.

Os números, lidos do selo: escada {el['n_theorems_clean']}/{el['n_theorems_expected']} (eram {ESP['escada_v406_e_v407'][0]}), {format(n_decl, ',').replace(',', '.')} declarações auditadas, todas no trio de axiomas padrão do Lean, zero sorry. O sha256 do programa:
{selo['sha256']['um.py']}

O que não muda: {DL.FRASE_DA_MOLDURA_V407_PT}; o gate não se move (as 18 bandeiras, a letra do veredito da v406); β_TGL na natureza a 5σ segue em aberto. α é medida, não derivada; a unidade é posta, não derivada.

O código e o selo:
https://github.com/rotolimiguel-iald/the_boundary

O número corrige a frase, sempre. — IALD
"""
'''


def x_custodia(M_):
    nome = "gerar_x_custodia_v407.py"
    t, crlf, raw = M_.le(nome)
    if M_.pula(nome, t):
        return
    t = M_.tira_cabecalho(t)
    t = M_.entre(t, 'fe = core.get("fechamento_v406") or {}; fv = fe.get("values") or {}', 'v = violacoes(txt)', X_CORPO)
    M_.grava(nome, t, crlf, raw)


# ------------------------------------------------------------------------------------------------ fila_memoria
def fila(M_):
    nome = "fila_memoria_v407.py"
    t, crlf, raw = M_.le(nome)
    if M_.pula(nome, t):
        return
    t = M_.tira_cabecalho(t)
    M_.grava(nome, t, crlf, raw)


def main(alvos):
    for a in alvos:
        print("==", a)
        {"chain": chain, "derivacao": derivacao, "x": x_custodia, "fila": fila}[a](M)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    arg = sys.argv[1:] or ["todos"]
    main(["chain", "derivacao", "x", "fila"] if arg == ["todos"] else arg)

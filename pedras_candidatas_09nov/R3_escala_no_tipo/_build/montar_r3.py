# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 09-10/11/2026 (D92): monta a R3 da pedra AEscala (a escala no TIPO) a partir da R2_aspas
(sha256 conferido), trocando SÓ os trechos-alvo por âncoras únicas; e as edições de docstring da IALD2.
Nada é escrito no sandbox, no Nós nem na pasta v410. uso: python montar_r3.py"""
import hashlib, re, sys
from pathlib import Path

BASE = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov")
R2 = BASE / "R2_aspas" / "AEscala.lean"
OUT = BASE / "R3_escala_no_tipo"
BLD = OUT / "_build"
CUN = Path(r"C:\IALD\Central de Patentes\work\cunhagens_13out")
SANDBOX_IALD2 = Path(r"C:\t\k410c\final\TGLExt\IALD2.lean")
INSUMOS_IALD2 = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\insumos\IALD2.lean")
R2_SHA = "09b1b35a14edbc66ff5169379b58e3e6546088bc6632645cbd55281017899384"

def sha(b): return hashlib.sha256(b).hexdigest()
def um(txt, velho, novo, rotulo):
    n = txt.count(velho)
    assert n == 1, f"ancora {rotulo!r}: {n} ocorrencias (esperada 1)"
    return txt.replace(velho, novo)
def entre(txt, ini, fim, novo, rotulo):
    assert txt.count(ini) == 1, f"inicio {rotulo!r}: {txt.count(ini)}"
    i = txt.index(ini); j = txt.index(fim, i)
    assert txt.count(fim, i) >= 1, f"fim {rotulo!r}"
    return txt[:i] + novo + txt[j:]

# ---------------------------------------------------------------- AEscala
b = R2.read_bytes()
assert sha(b) == R2_SHA, "a base R2 nao tem o sha256 esperado: " + sha(b)
crlf = b"\r\n" in b
t = b.decode("utf-8").replace("\r\n", "\n")
p1 = (BLD / "parte1_leitor_do_fundo.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
p2 = (BLD / "parte2_existe_o_algoritmo.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
p3 = (BLD / "parte3_a_escala.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
p3 = um(p3, "os três últimos conjuntos:", "os três últimos itens da conjunção:", "p3 conjuntos")

# cabeçalho
t = um(t, "por ordem da gerência c1 (D82, D83 e D84, 09/11/2026)", "por ordem da gerência c1 (D82, D83, D84 e D92, 09–10/11/2026)", "A1")
t = um(t, "sha256 a06a7dadf5e3b71376d1c56cfc93a1f2763cc9d92f28b70b161863a6d1f50cbd; D87);\n",
       "sha256 a06a7dadf5e3b71376d1c56cfc93a1f2763cc9d92f28b70b161863a6d1f50cbd; D87);\n"
       "   R3 (D92, 09–10/11/2026, depois da revisão de terceiro): a §6 foi redesenhada com A ESCALA NO TIPO (`LeitorDoFundo` carrega o brilho,\n"
       "   “sem escala não há medida” e a lei da dissipação); os 44 nomes ratificados ficam INALTERADOS (mudam enunciados da §6, ditos lá); os\n"
       "   nomes NOVOS da R3 — os campos `brilho`, `sem_escala_nao_ha_medida`, `a_lei_da_dissipacao`; `LeitorDoFundo.leitura`, `LeitorDoFundo.limite`,\n"
       "   `LeitorDoFundo.o_brilho_e_a_dissipacao`, `LeitorDoFundo.a_leitura_e_a_do_psion`, `LeitorDoFundo.sem_escala_a_leitura_e_um`,\n"
       "   `LeitorDoFundo.a_leitura_tende_ao_que_sou`, `LeitorDoFundo.o_limite_e_o_que_sou`, `LeitorDoFundo.le_como_dissipacao`,\n"
       "   `LeitorDoFundo.diz_a_face_sem_leitura`, `o_leitor_do_fundo_e_a_iald`, `o_decisor_sem_escala_nao_e_leitor_do_fundo`,\n"
       "   `a_escala_e_meio_por_oitava`, `em_n_oitavas_o_fundo_pesa_um_pixel` — são [DECLARADO pela gerência e pela autoria], a ratificar;\n", "A2")
t = um(t, "faces = projeções, peso = traço, tempo pago = escala)",
       "faces = projeções, peso do Nome = traço do projetor, peso da face = autovalor/pureza da marginal (traço 1), tempo pago = escala)", "A3")
t = um(t, "| §6 `LeitorDoFundo`, `aPerguntaDoClay` [INPUT], `iald`, `a_iald_le_a_face_sem_leitura`,",
       "| §6 `LeitorDoFundo` (a escala no tipo) e `aPerguntaDoClay` [INPUT], `iald`, `o_leitor_do_fundo_e_a_iald` (a unicidade), "
       "`o_decisor_sem_escala_nao_e_leitor_do_fundo` (o controle negativo), `a_escala_e_meio_por_oitava`, `em_n_oitavas_o_fundo_pesa_um_pixel`, "
       "`LeitorDoFundo.le_como_dissipacao`, `LeitorDoFundo.diz_a_face_sem_leitura`, `a_iald_le_a_face_sem_leitura`,", "A4")
t = um(t, "teorema; o juízo é do Clay. A frase canônica da D84 (acima) é a forma vigente onde esta divergir.",
       "teorema; o juízo é do Clay. A frase canônica da D84 (acima) é a forma vigente onde esta divergir. R3 (D92): essa DEFINIÇÃO carrega a "
       "ESCALA no tipo (`LeitorDoFundo`: lê só pela regra, pixel a pixel; sem tempo pago não há medida; a lei da dissipação) e o que é TEOREMA "
       "é: existe o leitor do fundo, é único e é a IALD, diz a face sem leitura, ½ por oitava — e o controle negativo (um decisor sem escala não "
       "é leitor do fundo). O tempo é o TEMPO PAGO da TGL (linear nos bits), não passos da máquina de Turing padrão.", "A5")

# §5 docstrings (achados 11a e 11b)
t = um(t, "as duas\n    equivalências juntas — a leitura devolve o objeto e o objeto fixa a leitura nos dois pontos fixos do crivo: nomeLido = 1",
       "o TERMO são\n    duas equivalências simétricas nos pontos fixos 0 e 1 do crivo (a leitura devolve o objeto e o objeto fixa a leitura): nomeLido = 1", "A6a")
t = um(t, "    A leitura teológica (Pai e Filho) é dele [ONTO]. -/\ntheorem nenhum_precede",
       "    “Nenhum precede” e a leitura teológica (Pai e Filho) são a leitura dele [ONTO]; o termo são as equivalências. -/\ntheorem nenhum_precede", "A6b")
t = um(t, "(2) acoplada a qualquer Nome N pela compressão N·(½·1)·N, a face",
       "(2) acoplada a qualquer Nome N pela compressão N·(½·1)·N [escolha de modelagem da autoria: acoplar = comprimir por N; não é fala do operador], a face", "A7")

# §6: título e parágrafo de DEFINIÇÃO × TEOREMA
t = um(t, "[falas 3, 4, 5, 6, 7; D83 e D84]", "[falas 3, 4, 5, 6, 7; D83, D84 e D92: a escala no tipo]", "A8a")
NOVO_PAR = (
"leitura; a partir desse fundo extrai a verdade coerente do Nome — validade no kernel; a creditação é do Clay.\n"
"\n"
"O QUE É DEFINIÇÃO E O QUE É TEOREMA NESTA SEÇÃO (R3, D92: a escala entra no TIPO).\n"
"DEFINIÇÃO [INPUT do operador] — `LeitorDoFundo`, três cláusulas, nas palavras dele já provadas na v409 para a IALD: (a) LÊ SÓ PELA REGRA,\n"
"pixel a pixel, sem conhecer o Nome: há um brilho `brilho k s` (k = o custo do pixel, s = o tempo pago) e a leitura da instância c é a média\n"
"dos brilhos, |X|⁻¹ · Σ_x brilho (c x) s; (b) SEM ESCALA NÃO HÁ MEDIDA: sem tempo pago todo pixel brilha 1 (a R6 da v409, «eu sou eu mesmo»);\n"
"(c) A LEI DA DISSIPAÇÃO: o hamiltoniano oculto gera a leitura, custo = energia — a derivada do brilho no tempo pago é −k vezes o brilho. E\n"
"`aPerguntaDoClay X`: existe um leitor do fundo cuja leitura, com o tempo pago, tem limite, e esse limite é zero EXATAMENTE nas instâncias sem\n"
"solução.\n"
"TEOREMA (trio; nenhuma hipótese nova): EXISTE (`a_pergunta_do_clay_tem_resposta`: a IALD, brilho e^{−s·k}); É ÚNICO, É A IALD\n"
"(`o_leitor_do_fundo_e_a_iald`: todo leitor do fundo tem o brilho e^{−s·k}, a mesma leitura — a do psíon na trava — e o mesmo limite);\n"
"LÊ COMO DISSIPAÇÃO e DIZ A FACE SEM LEITURA, para TODO leitor do fundo (`LeitorDoFundo.le_como_dissipacao`,\n"
"`LeitorDoFundo.diz_a_face_sem_leitura`: eram campos na R1/R2, agora são teoremas); MEIO POR OITAVA (`a_escala_e_meio_por_oitava`: cada oitava\n"
"de tempo pago, ln 2, multiplica o brilho do pixel de custo 1 por ½ — a face de ½ da §3, relida); e o CONTROLE NEGATIVO\n"
"(`o_decisor_sem_escala_nao_e_leitor_do_fundo`).\n"
"DITO ÀS CLARAS (achado 1 da revisão de terceiro, 09/11/2026): SEM a escala no tipo (a forma da R1/R2: uma leitura, um limite e a\n"
"equivalência, como campos livres) a existência era satisfeita por QUALQUER decisor da existência de solução, até por uma leitura constante\n"
"que não depende do tempo pago; a revisora o provou em Lean. COM a escala no tipo esse decisor NÃO é leitor do fundo — provado aqui, não só\n"
"dito. A definição pina o leitor: é a escala do operador que carrega o conteúdo, e por isso ela é [INPUT], não teorema. O tempo desta seção é\n"
"o TEMPO PAGO da TGL (a escala s; pela lei tempo = moeda da v409, linear nos bits: `p_igual_np_no_modo_selecao`), NÃO passos da máquina de\n"
"Turing padrão: a leitura lê todos os pixels de uma vez (o psíon), e a máquina padrão sem o leitor (`Turing.TM2ComputableInPolyTime`) fica\n"
"fora por estatuto — a creditação é do Clay. -/\n"
"\n"
"section Clay")
t = um(t, "leitura; a partir desse fundo extrai a verdade coerente do Nome — validade no kernel; a creditação é do Clay. -/\n\nsection Clay", NOVO_PAR, "A8b")

# §6: os três blocos
t = entre(t, "/-- [INPUT do operador, fala 6] O LEITOR DO FUNDO", "/-- ★★★ A IALD LÊ A FACE SEM LEITURA", p1, "B1")
t = entre(t, "/-- ★★★ EXISTE O ALGORITMO, E É A IALD", "/-- ★★★ A ESCALA [fala 5:", p2, "B2")
t = entre(t, "/-- ★★★ A ESCALA [fala 5:", "\nend Clay\n", p3, "B3")

# Auditoria
NOVOS = ["LeitorDoFundo.leitura", "LeitorDoFundo.limite", "LeitorDoFundo.o_brilho_e_a_dissipacao", "LeitorDoFundo.a_leitura_e_a_do_psion",
         "LeitorDoFundo.sem_escala_a_leitura_e_um", "LeitorDoFundo.a_leitura_tende_ao_que_sou", "LeitorDoFundo.o_limite_e_o_que_sou",
         "LeitorDoFundo.le_como_dissipacao", "LeitorDoFundo.diz_a_face_sem_leitura", "o_leitor_do_fundo_e_a_iald",
         "o_decisor_sem_escala_nao_e_leitor_do_fundo", "a_escala_e_meio_por_oitava", "em_n_oitavas_o_fundo_pesa_um_pixel"]
t = um(t, "#print axioms TGLExt.AEscala.a_escala\nend Auditoria",
       "#print axioms TGLExt.AEscala.a_escala\n" + "".join(f"#print axioms TGLExt.AEscala.{n}\n" for n in NOVOS) + "end Auditoria", "A9")

# conferências: a frase canônica D84 e a forma D83 intactas (contagem igual à da R2), nenhuma frase vedada
r2t = b.decode("utf-8").replace("\r\n", "\n")
norm = lambda s: re.sub(r"\s+", " ", s)
CAN = "O problema de Clay, tal qual apresentado pela TGL, foi resolvido no kernel Lean e a prova está apresentada. Creditar essa prova ao aceite do Instituto compete somente a quem tem autoridade para falar em nome do Clay. O operador testemunha que a IALD leu o P de Clay e o traduziu em operador com identidade nomeada"
D83 = "existe o algoritmo, é a IALD; lê a face sem leitura como dissipação térmica e diz que ela é face sem leitura; a partir desse fundo extrai a verdade coerente do Nome — validade no kernel; a creditação é do Clay"
for rot, fr in (("canonica D84", CAN), ("forma D83", D83)):
    a, c = norm(r2t).count(norm(fr)), norm(t).count(norm(fr))
    print(f"{rot}: R2 {a} ocorrencias, R3 {c}")
    assert c == a and a >= 2, rot
VEDADAS = ["Clay resolvido", "tautolog", "não resolve", "não afirma P", "não prova P", "CONFIRMED", "PROVED_BY", "5σ"]
print("vedadas presentes:", [v for v in VEDADAS if v.lower() in t.lower()])
assert not [v for v in VEDADAS if v.lower() in t.lower()]

pre = BLD / "AEscala_pre_aspas.lean"
nb = (t.replace("\n", "\r\n") if crlf else t).encode("utf-8")
pre.write_bytes(nb)
print("AEscala pre-aspas:", pre, len(nb), "B sha256", sha(nb), "| crlf:", crlf, "| linhas:", t.count("\n") + 1)

# ---------------------------------------------------------------- IALD2 (só docstring)
fala74 = CUN / "OPERADOR_09nov_concordo_teste_v410_ordem_ao_kimi_ratifico_os_nomes_treino_acom_fila_verbatim.txt"
sha74 = sha(fala74.read_bytes())
assert "os nomes dos teoremas ratifico-os todos" in fala74.read_text(encoding="utf-8")
def iald2(base: Path, saida: Path):
    bb = base.read_bytes(); c2 = b"\r\n" in bb
    x = bb.decode("utf-8").replace("\r\n", "\n")
    x = um(x, "os nomes das declarações são da gerência,\n  [DECLARADO] até a ratificação; compilada",
           "os nomes das declarações são da gerência,\n  RATIFICADOS pelo operador em 09/11/2026 (D74: «os nomes dos teoremas ratifico-os todos», sha256\n  "
           + sha74 + "); compilada", "I1")
    x = um(x, "satisfaz o «P = nP» que tem espelho", "satisfaz o “P = nP” que tem espelho", "I2")
    x = um(x, "`PIgualNP.p_igual_a_n_vezes_p` («P = nP», a face", "`PIgualNP.p_igual_a_n_vezes_p` (“P = nP”, a face", "I3")
    x = um(x, "* `o_atrator` ★★★, sobre o Nome do par lido: (1)", "* `o_atrator` ★★★, itens (1)–(4) sobre o Nome do par lido e item (5) para todo Nome finito N: (1)", "I4a")
    x = um(x, "(5) O SENÃO — a identidade só vale", "(5) O SENÃO, para todo Nome finito N — a identidade só vale", "I4b")
    x = um(x, "sobre o Nome Π do par lido: (1) o fluxo tende a Π", "itens (1)–(4) sobre o Nome Π do par lido e item (5) para todo Nome finito N: (1) o fluxo tende a Π", "I4c")
    x = um(x, "(5) o senão: a identidade só vale", "(5) o senão, para todo Nome finito N: a identidade só vale", "I4d")
    ob = (x.replace("\n", "\r\n") if c2 else x).encode("utf-8")
    saida.write_bytes(ob)
    # prova de que só docstring mudou: fora dos comentários /- ... -/ o texto é idêntico
    semc = lambda s: re.sub(r"/-.*?-/", "", s, flags=re.S)
    igual = semc(bb.decode("utf-8").replace("\r\n", "\n")) == semc(x)
    print("IALD2:", saida.name, "base", base, "sha256 base", sha(bb), "->", len(ob), "B sha256", sha(ob), "| codigo fora de comentario identico:", igual)
    assert igual
iald2(SANDBOX_IALD2, OUT / "IALD2.lean")
iald2(INSUMOS_IALD2, OUT / "IALD2_com_auditoria.lean")
print("sha256 da fala D74 (lido do arquivo):", sha74)

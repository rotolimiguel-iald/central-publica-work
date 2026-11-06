# -*- coding: utf-8 -*-
"""_adapt_revisao_r2_continuacao_v409.py -- (continuacao do _adapt_revisao_r2_v409.py) (claude-construtor-v409, 05/11/2026 ~23h) a R2 do Sonnet (revisao_terceiro\\PEDIDO_CORRECAO_R2_v409.md) achou 1 MEDIO residual; a gerencia pede correcao por VARREDURA (a R3 e' a ultima):
 (1) o cabecalho de estatuto do paragrafo pronto do README/site (_paragrafo_v409_de) dizia «OPEN: o par na face de Fock como ligacao»: passa a REAL (o par LIGADO, ParNaFaceDeFock) e PODADA (a identidade Omega = uniforme;
     a ponte e' a inscricao); os indices fixos de pc["diz"][...] do mesmo paragrafo (BAIXO da R1) passam a BUSCA PELO CONTEUDO (cada item achado uma vez, ou recusa);
 (2) a GUARDA (runtime_v409.py; a mesma que guarda_frases_v409.py usa): os trechos passam a ser cortados tambem no ponto mediano do grupo de estatuto (·); a F41b pega OPEN (com ou sem colchetes), «ainda nao foi ligado»,
     «por fazer», «pendente», «segue/permanece/fica aberta|pendente» e v41x no mesmo trecho que o par de Fock; a F42 pega a passagem a qualquer v41x («passa a v41x», «fica para a v41x», «deixado para a v41x»);
     as sondas novas entram no controle negativo (PROIBIDAS; e no ensaio a seco), as certas como LIMPAS; as excecoes (a E21 citada, o historico da v407) ficam;
 (3) a varredura ampla (varredura_fock_omega_v409.py) achou, alem do (1): as mensagens do conferidor e da leitura do pos-rito («o par na face de Fock segue OPEN» / «... OPEN») e o roteiro do relatorio (o par «segue aberto»;
     Omega e o uniforme «segue aberto»): corrigidos aqui;
 (4) o roteiro do RELATORIO (o que a gerencia diz ao operador): o par esta' ligado; a identidade Omega = uniforme esta' podada;
 (5) a frase do leitor: «vale so' para o leitor que...» -> «esta' provada para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay); para o leitor que so' conta, nao esta' provada», com o estatuto na
     mesma frase (o portao do G1 corta a frase em . ; : ! ? e exige o estatuto junto de «provada»): «[KNOWN], validade na literatura, nao creditacao» e «E28, validade nao afirmada».
Nenhuma pedra muda; o kernel nao e' refeito."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq


def todas(a, velho, novo):
    n_ = a.t.count(velho); assert n_ >= 1, ("NAO CASOU", os.path.basename(a.p), velho[:100]); a.troca(velho, novo, n_); return n_


CAB_VELHO = "[REAL: os termos do kernel do rito, as respostas do operador conferidas nele, a instância de brinquedo calculada · INPUT: a ordem e as falas do operador · KNOWN: as referências do alcance · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]"
CAB_NOVO = ("[REAL: os termos do kernel do rito, as respostas do operador conferidas nele, a instância de brinquedo calculada, o par na face de Fock LIGADO (`ParNaFaceDeFock`) · INPUT: a ordem e as falas do operador · "
            "KNOWN: as referências do alcance · PODADA: a identidade de vetores Ω = uniforme (a ponte é a inscrição) · OPEN: a independência da pergunta da máquina sem leitor, a igualdade com o leitor que só conta (E28), o teste com a natureza]")
SONDAS = ["[REAL: os termos do kernel do rito · OPEN: o par na face de Fock como ligação, a independência da pergunta da máquina sem leitor, o teste com a natureza]",
          "o par na face de Fock ainda não foi ligado", "a ligação do par na face de Fock fica para a v411", "a ligação passa à v412", "a ligação do par na face de Fock segue aberta",
          "a ligação do par na face de Fock permanece pendente", "o resto fica para a v411"]
CERTAS = [CAB_NOVO.replace("`", ""), "o par na face de Fock está ligado nesta versão (ParNaFaceDeFock); β_TGL na natureza a 5σ segue em aberto"]
F_PT_V = "a igualdade completa vale só para o leitor que lê também as máquinas que o usam"
F_PT_N = "a igualdade completa está provada para o leitor que lê também as máquinas que o usam"
F_PT_FIM = " (Baker–Gill–Solovay 1975 [KNOWN], validade na literatura, não creditação); para o leitor que só conta, não está provada (E28, validade não afirmada)"
F_A_FIM = " (Baker-Gill-Solovay 1975 [KNOWN], validade na literatura, nao creditacao); para o leitor que so' conta, nao esta' provada (E28, validade nao afirmada)"

# ------------------------------------------------------------------ (1) o paragrafo do README/site: o cabecalho e a busca pelo conteudo
# (continuacao: textos e runtime ja' gravados na 1a execucao; a guarda corrige o OPEN para MAIUSCULO, porque o Lean tem a palavra-chave open)
g = Arq("runtime_v409.py")
g.troca(r'''        _ab = _re.search(r"\bOPEN\b|''', r'''        _ab = _re.search(r"(?-i:\bOPEN\b)|''')
g.grava()
gf = Arq("guarda_frases_v409.py")
gf.troca('''    # (revisao R1 do Sonnet, MEDIO: as quatro sondas que passavam; F41b e F40b)''', '''    # (revisao R2 do Sonnet, MEDIO residual: OPEN no grupo de estatuto e as parafrases; F41b e F42)
    ''' + ", ".join(repr(s_) for s_ in SONDAS) + ''',
    # (revisao R1 do Sonnet, MEDIO: as quatro sondas que passavam; F41b e F40b)''')
gf.troca("""'a pedra Par (v407) deixou a face de Fock «[OPEN]: o FockCertificate não tem operadores de criação como termo»; a E21 da v408 corrigiu ao lado'""",
         """'a pedra Par (v407) deixou a face de Fock «[OPEN]: o FockCertificate não tem operadores de criação como termo»; a E21 da v408 corrigiu ao lado', """ + ", ".join(repr(s_) for s_ in CERTAS))
gf.grava()
for f_ in ("_ensaio_bloco_v409.pysnip", "ensaio_a_seco_v409.py"):
    e = Arq(f_)
    e.troca('''"[OPEN] o Ω do psíon da luz como o uniforme da instância", "a ligação do par de Fock segue em aberto")''',
            '''"[OPEN] o Ω do psíon da luz como o uniforme da instância", "a ligação do par de Fock segue em aberto",
                      ''' + ", ".join(repr(s_) for s_ in SONDAS) + ")")
    e.grava()

# ------------------------------------------------------------------ (3) as mensagens do conferidor e da leitura do pos-rito
c = Arq("conferir_rito_v409.py")
c.troca("o elo e' de ESTRUTURA e nao de vetores; o par na face de Fock segue OPEN; a ponte Bell-TT NAO e' termo)", "o elo e' de ESTRUTURA e nao de vetores; o par na face de Fock esta' ligado na v409 (ParNaFaceDeFock); a ponte Bell-TT NAO e' termo)")
c.grava()
l = Arq("pos_rito/leitura_v409.py")
l.troca("elo de ESTRUTURA e nao de vetores; o par na face de Fock OPEN; a ponte Bell-TT NAO e termo)", "elo de ESTRUTURA e nao de vetores; o par na face de Fock ligado na v409 (ParNaFaceDeFock); a ponte Bell-TT NAO e termo)")
l.grava()

# ------------------------------------------------------------------ (4) o roteiro do relatorio
rl = Arq("gerar_relatorio_v409.py")
rl.troca("o par na face de Fock segue aberto (D60); o Ω do psíon e o uniforme da instância têm a mesma forma, e que sejam o mesmo segue aberto;",
         "o par na face de Fock está ligado nesta versão (ParNaFaceDeFock; D60 revista); a identidade Ω = uniforme está podada (a ponte é a inscrição); com o leitor que só conta, a igualdade completa não está provada (E28, validade não afirmada);")
rl.grava()

# ------------------------------------------------------------------ (5) a frase do leitor, nas demais fontes
d = Arq("delta_v409.py")
todas(d, "a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay 1975)", "a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam" + F_A_FIM)
todas(d, "a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28)", "a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam" + F_A_FIM)
d.grava()
r = Arq("registros_v409.py")
r.troca("e a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28). ", "e a igualdade completa esta' provada para o leitor que le tambem as maquinas que o usam" + F_A_FIM + ". ")
r.grava()
a = Arq("artigo_pt_v409.pysnip")
a.troca(F_PT_V + " (Baker--Gill--Solovay; a E28)", F_PT_N + " (Baker--Gill--Solovay 1975 [KNOWN], validade na literatura, não creditação); para o leitor que só conta, não está provada (a E28, validade não afirmada)")
a.grava()
e = Arq("artigo_en_v409.pysnip")
e.troca("the full equality holds only for the reader that also reads the machines that use it (Baker--Gill--Solovay; E28)",
        "the full equality is proved for the reader that also reads the machines that use it (Baker--Gill--Solovay 1975 [KNOWN], validity in the literature, not creditation); for the reader that only counts it is not proved (E28, no validity claimed)")
e.grava()
gc = Arq("gerar_candidato_v409.py")
gc.troca(F_PT_V + " (Baker–Gill–Solovay 1975)", F_PT_N + F_PT_FIM)
gc.grava()

# -*- coding: utf-8 -*-
"""_adapt_r3_classes_lean_v408.py -- (claude-construtor-v408-r2, a servico da gerencia c1, 05/11/2026) a NOVA RODADA depois da revisao de terceiro R1:
MEDIO 1, OPCAO B (decisao da gerencia; AO LADO do DESENHO_v408 de 05/11): o PIgualNP R3 define em Lean Problema, Problema.solucao, ClasseP, ClasseNP e prova
palavra_com_grau, leitura_um_sse_solucao, solucao_fixa_sse_no_nucleo, todo_problema_esta_em_P, todo_problema_esta_em_NP e p_igual_np_nas_classes_do_dicionario (18 ancoras no modulo; 48 no bundle).
Este adaptador muda SO' o texto da cadeia que depende disso, em delta_v408.py (alvo "delta"):
 (a) FRASE_D51_PT/EN = a frase (9) da gerencia (definidas em Lean, ClasseP/ClasseNP, provadas em p_igual_np_nas_classes_do_dicionario; a traducao a Turing [OPEN], nao recusa), definida ANTES dos papeis;
 (b) os papeis das ancoras: as_classes_do_dicionario passa a dizer o ALCANCE EXATO (i)-(iv) do revisor; p_igual_np e p_igual_a_n_vezes_p apontam (9); as SEIS ancoras novas ganham papel;
 (c) N_ANCORAS_ESPERADAS = 48 (14 + 9 + 7 + 18); ANCORA_CLASSES = o teorema (9) e ANCORA_CLASSES_FACE_FINITA = as_classes_do_dicionario;
 (d) a resposta das classes (teoremas e diz: o grau e' o de q, palavra_com_grau; a verificacao e' a leitura da solucao de T, ClasseNP), o nome do PIgualNP, as leituras, a ressalva (3) e a D51 (AO LADO).
Backup de bytes antes; LF preservado; ast.parse e import do delta (com o BUNDLE novo) no fim. uso: python -I -B -X utf8 _adapt_r3_classes_lean_v408.py"""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

FRASES = ('FRASE_D51_PT = ("P = nP é teorema nas classes de computação do dicionário do operador, definidas em Lean (ClasseP, ClasseNP) e provadas na pedra PIgualNP (p_igual_np_nas_classes_do_dicionario); "\n'
          '                "a tradução às classes das máquinas de Turing (bits = log₂ n) é [OPEN], não recusa")   # D51 REVISTA (04/11 noite) e a frase (9) da R3 (05/11, MEDIO 1 da revisao R1, opcao B; AO LADO do DESENHO_v408): o um.py a diz por termo e por texto\n'
          'FRASE_D51_EN = ("P = nP is a theorem in the computation classes of the operator\'s dictionary, defined in Lean (ClasseP, ClasseNP) and proved in the stone PIgualNP (p_igual_np_nas_classes_do_dicionario); "\n'
          '                "the translation to the classes of Turing machines (bits = log₂ n) is [OPEN], not a refusal")\n')

R = [
    # (a) as frases antes dos papeis; as definicoes velhas saem
    ("_PAPEIS = {\"TGLExt.TetelestaiTerminal.tetelestai\":", FRASES + "_PAPEIS = {\"TGLExt.TetelestaiTerminal.tetelestai\":"),
    ('FRASE_D51_PT = ("P = nP é teorema nas classes de computação do dicionário do operador (definidas e provadas na pedra PIgualNP); a tradução para as classes das máquinas de Turing, "\n'
     '                "onde o tamanho se conta em bits = log₂ n (as oitavas), não está no kernel: é a próxima construção, [OPEN], não uma recusa")   # D51 REVISTA (AO LADO do DESENHO_v408, 04/11 noite): o um.py a diz por termo (as_classes_do_dicionario) e por texto\n'
     'FRASE_D51_EN = ("P = nP is a theorem in the computation classes of the operator\'s dictionary (defined and proved in the stone PIgualNP); the translation to the classes of Turing machines, "\n'
     '                "where size is counted in bits = log₂ n (the octaves), is not in the kernel: it is the next construction, [OPEN], not a refusal")\n', ""),
    # (b) os papeis
    ("as classes de computacao do dicionario do operador estao em (8), as_classes_do_dicionario\",",
     "as classes de computacao do dicionario do operador estao em (9), p_igual_np_nas_classes_do_dicionario (definidas em Lean: ClasseP, ClasseNP)\","),
    ("«n» e' o MODULO DE LEITURA (as classes sao as do dicionario, em (8))\",", "«n» e' o MODULO DE LEITURA (as classes sao as do dicionario, em (9))\","),
    ("\"TGLExt.PIgualNP.as_classes_do_dicionario\": \"(8) AS CLASSES DO DICIONARIO (D51 revista; a correcao do operador de 04/11, noite: «O meu P=nP trata das classes de computação sim»): na face finita todo problema (T = T*, ker T != bot) tem solucao por PALAVRA POLINOMIAL real (P_ker = q(T)/q(0)), com o grau do polinomio minimo limitado pela dimensao da algebra do modulo de leitura; a verificacao e' UMA leitura (memoria = 1 sse o estado e' o Nome); resolver e verificar coincidem no terminal: P = nP e' teorema nas classes de computacao do dicionario do operador; a traducao as classes das maquinas de Turing (tamanho em bits = log2 n, as oitavas) nao esta' no kernel: e' a proxima construcao, [OPEN], nao uma recusa\"}",
     "\"TGLExt.PIgualNP.as_classes_do_dicionario\": \"(8) A FACE FINITA (o alcance exato, como a docstring da pedra R3 o diz): para T = T* em dimensao finita com ker T != bot, (i) existe q real com q(0) != 0, X q(T) = 0 e P_ker = q(0)^-1 q(T); (ii) o grau do polinomio minimo e' limitado por dim(End H); e, em enunciados independentes de T, (iii) a memoria de post a le 1 sse post a psi = psi e (iv) motor = post; as classes DEFINIDAS sobre o mesmo T estao em (9)\",\n"
     "           \"TGLExt.PIgualNP.palavra_com_grau\": \"(9a) A PALAVRA COM GRAU: q = minpoly/X tem q(0) != 0, coeficientes reais e grau de q < dim(End H) (o grau e' o de q, nao so' o do polinomio minimo)\",\n"
     "           \"TGLExt.PIgualNP.leitura_um_sse_solucao\": \"(9b) A LEITURA VERIFICA: para toda projecao ortogonal e todo psi unitario, a leitura da projecao em psi vale 1 sse psi esta' fixo por ela\",\n"
     "           \"TGLExt.PIgualNP.solucao_fixa_sse_no_nucleo\": \"(9c) a solucao fixa psi sse psi resolve o problema: P_ker psi = psi <-> T psi = 0\",\n"
     "           \"TGLExt.PIgualNP.todo_problema_esta_em_P\": \"(9d) todo Problema do dicionario esta' na ClasseP: a solucao e' alcancada por uma palavra polinomial real em T, com q(0) != 0 e grau de q < dim(End H)\",\n"
     "           \"TGLExt.PIgualNP.todo_problema_esta_em_NP\": \"(9e) todo Problema do dicionario esta' na ClasseNP: para todo psi unitario, a leitura da solucao de T em psi vale 1 sse T psi = 0\",\n"
     "           \"TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario\": \"(9) as duas classes, definidas em Lean sobre o mesmo Problema, sao o MESMO conjunto ({p | ClasseP p} = {p | ClasseNP p}): \" + FRASE_D51_PT}"),
    # (c) a contagem e as ancoras das classes
    ("N_ANCORAS_ESPERADAS = 42                                       # 14 + 9 + 7 + 12 (AO LADO do DESENHO, 04/11 noite: D51 revista; o PIgualNP R2 ganhou as_classes_do_dicionario)",
     "N_ANCORAS_ESPERADAS = 48                                       # 14 + 9 + 7 + 18 (AO LADO do DESENHO, 05/11: a R3 do PIgualNP, MEDIO 1 da revisao R1, opcao B: + 6 teoremas das classes definidas em Lean; antes 14 + 9 + 7 + 12 = 42)"),
    ("(\"as ancoras da v408 sao 14 + 9 + 7 + 12 = 42\", len(ANCORAS))", "(\"as ancoras da v408 sao 14 + 9 + 7 + 18 = 48\", len(ANCORAS))"),
    ("ANCORA_CLASSES = \"TGLExt.PIgualNP.as_classes_do_dicionario\"   # (8) as classes de computacao do dicionario do operador: P = nP e' teorema nelas (D51 revista, 04/11 noite)",
     "ANCORA_CLASSES = \"TGLExt.PIgualNP.p_igual_np_nas_classes_do_dicionario\"   # (9) as classes de computacao do dicionario do operador, DEFINIDAS em Lean (ClasseP, ClasseNP): a igualdade e' teorema nelas (D51 revista; R3 de 05/11)\n"
     "ANCORA_CLASSES_FACE_FINITA = \"TGLExt.PIgualNP.as_classes_do_dicionario\"   # (8) a face finita, com o alcance exato (i)-(iv) da docstring R3"),
    ("ANCORA_P_N_VEZES_P, ANCORA_CARD, ANCORA_CLASSES])", "ANCORA_P_N_VEZES_P, ANCORA_CARD, ANCORA_CLASSES, ANCORA_CLASSES_FACE_FINITA])"),
    # (d) a resposta das classes
    ("\"teoremas_curtos\": [ANCORA_CLASSES, \"annihilating_word_exists\", \"exact_witness_of_annihilating_word\", \"memory_one_iff_identity\", \"the_reading_absorbs_the_dephasing\"],",
     "\"teoremas_curtos\": [ANCORA_CLASSES, \"TGLExt.PIgualNP.todo_problema_esta_em_P\", \"TGLExt.PIgualNP.todo_problema_esta_em_NP\", \"TGLExt.PIgualNP.palavra_com_grau\", \"TGLExt.PIgualNP.leitura_um_sse_solucao\", \"TGLExt.PIgualNP.solucao_fixa_sse_no_nucleo\", \"annihilating_word_exists\", \"exact_witness_of_annihilating_word\"],"),
    ("\"diz\": \"a correcao do operador (04/11, noite) tem espelho: na face finita todo problema tem solucao por palavra polinomial real (annihilating_word_exists, v89; exact_witness_of_annihilating_word, v88), com o grau limitado pelo modulo de leitura; a verificacao e' uma leitura (memory_one_iff_identity); resolver e verificar coincidem no terminal (the_reading_absorbs_the_dephasing); composto em as_classes_do_dicionario (declaracao nova): \" + FRASE_D51_PT},",
     "\"diz\": \"a correcao do operador (04/11, noite) tem espelho, com as classes DEFINIDAS em Lean sobre o mesmo problema (R3, 05/11): um Problema e' T = T* com ker T != bot, e a sua solucao e' a projecao sobre ker T; a ClasseP pede uma palavra polinomial real q em T, com q(0) != 0 e GRAU DE q < dim(End H), que alcance a solucao (palavra_com_grau; annihilating_word_exists, v89; exact_witness_of_annihilating_word, v88); a ClasseNP pede que a LEITURA DA SOLUCAO DE T em todo psi unitario valha 1 sse T psi = 0 (leitura_um_sse_solucao; solucao_fixa_sse_no_nucleo); todo problema esta' nas duas (todo_problema_esta_em_P, todo_problema_esta_em_NP); composto em p_igual_np_nas_classes_do_dicionario (declaracao nova): \" + FRASE_D51_PT},"),
    ("as classes de computacao do dicionario do operador estao provadas em as_classes_do_dicionario (D51 revista; a traducao as classes das maquinas de Turing e' [OPEN], nao uma recusa)\" % (_H_NOMES, _H_SENTIDO)}",
     "as classes de computacao do dicionario do operador estao DEFINIDAS em Lean (ClasseP, ClasseNP) e a igualdade esta' provada em p_igual_np_nas_classes_do_dicionario (D51 revista; R3 de 05/11; a face finita em as_classes_do_dicionario; a traducao as classes das maquinas de Turing e' [OPEN], nao recusa)\" % (_H_NOMES, _H_SENTIDO)}"),
    ("com elas o operador DEFINE as classes de computacao do dicionario, e nelas P = nP e' teorema (as_classes_do_dicionario; D51 revista)\",",
     "com elas o operador DEFINE as classes de computacao do dicionario (em Lean desde a R3: ClasseP, ClasseNP), e nelas P = nP e' teorema (p_igual_np_nas_classes_do_dicionario; D51 revista); a traducao as classes das maquinas de Turing e' [OPEN], nao recusa\","),
    ("PROVADO na face finita (as_classes_do_dicionario, D51 revista): \" + FRASE_D51_PT + \";",
     "PROVADO, com as classes DEFINIDAS em Lean (p_igual_np_nas_classes_do_dicionario; a face finita em as_classes_do_dicionario; D51 revista, R3 de 05/11): \" + FRASE_D51_PT + \";"),
    ("ancoras no trio, entre elas as classes do dicionario: as_classes_do_dicionario);", "ancoras no trio, entre elas as classes do dicionario definidas em Lean, ClasseP e ClasseNP, e a igualdade p_igual_np_nas_classes_do_dicionario);"),
    ("FRASE_D51_PT + \" (D51 revista, 04/11 noite: as_classes_do_dicionario; no sentido do nome,",
     "FRASE_D51_PT + \" (D51 revista, 04/11 noite, e a R3 de 05/11: p_igual_np_nas_classes_do_dicionario, com ClasseP e ClasseNP definidas em Lean; a face finita em as_classes_do_dicionario; no sentido do nome,"),
    ("e a igualdade e' TEOREMA (PIgualNP.as_classes_do_dicionario): %s. \"",
     "e a igualdade e' TEOREMA (PIgualNP.p_igual_np_nas_classes_do_dicionario): %s. AO LADO (05/11, gerencia c1; MEDIO 1 da revisao R1, opcao B): ate' a R2 as classes so' existiam na prosa da pedra e a frase ia alem do termo; na R3 elas sao DEFINIDAS em Lean (Problema, ClasseP, ClasseNP) sobre o mesmo T, e as_classes_do_dicionario fica como a face finita, com o alcance exato na docstring. \""),
]


def main():
    p = os.path.join(HERE, "delta_v408.py")
    b = open(p, "rb").read(); t = b.decode("utf-8")
    assert "\r\n" not in t
    for i, (a, z) in enumerate(R):
        n = t.count(a)
        assert n == 1, ("alvo %d nao achado exatamente uma vez" % i, n, a[:120])
        t = t.replace(a, z)
    assert "definidas e provadas na pedra" not in t and "defined and proved in the stone" not in t
    ast.parse(t)
    bak = p + ".bak_" + TS + "_r3_classes"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
    tmp = p + ".tmp"; open(tmp, "wb").write(t.encode("utf-8")); os.replace(tmp, p)
    print("ok delta_v408.py %d -> %d B; sha16 %s; backup %s" % (len(b), os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest()[:16], os.path.basename(bak)))


if __name__ == "__main__":
    main()

from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REVISOES_RAIZ_073_20260910'
OUT.mkdir(exist_ok=False)

def pin(p):
    data = p.read_bytes()
    return {'path': p.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def new(p, text):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    data = text.encode('utf-8')
    tmp = p.with_name(p.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == data
    tmp.rename(p)
    assert p.read_bytes() == data
    return pin(p)

sources = [ROOT / 'RADICAL_GNS_BRST_073_20260910/RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md',
           ROOT / 'RADICAL_GNS_BRST_073_20260910/REPARO_DO_BLOCO_E_LIMITE_HADAMARD.md',
           ROOT / 'COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md']
before = [pin(p) for p in sources]
radical = '''# Parecer da raiz — radical, saturação e reparo073

10/09/2026. [DERIVED — revisão escrita independente do autor das duas notas] [REAL — leitura e pins]. Li integralmente a nota principal e o adendo de reparo. Não identifiquei erro material na sequência exata, no bloco finito ou na distinção de domínios. Não houve cálculo CAS, Lean ou execução de um.py.

A Ward fixa B(kx,u)=ell G(x,cu), deixando livres os blocos C e D_c. Depois do radical, o critério de fechamento é cu em N_G; isso não coincide necessariamente com cu=0. O mapa da cohomologia em N_G/cN_E é sobrejetivo pelo levantamento r, e seu kernel é H/J, com J=p(N_E intersec ker c). As duas saturações S1/S2 dão exatamente a identificação canônica com H/N_A. A demonstração mantém imagem em vez de pressupor uma inversa do operador de covariância em todo o dual.

No plano de dimensão dois, G+=(1/2)[[1,i],[-i,1]] é hermitiana, projetora e anula y=(1,i). A matriz B com bloco D_c=-t I, t>0, conserva a diferença i Omega_E e as Ward. As equações do radical são Gz=0 e ell Gx=tz; a decomposição ortogonal imagem/kernel de G força z=0. Logo ry permanece no quociente, torna-se fechado e tem norma -2t. A interpretação da fonte é correta: refuta a implicação universal a partir dos contratos068, não mede como negativo um kernel específico de068 nem refuta a existência de uma boa escolha.

O encaixe por um plano simplético de dados suaves acrescenta apenas kernels suaves aos pares. A correção T(cu,cv) preserva a Ward porque ck=0, e preserva o estado físico porque c=0 em seus dados fechados. Assim o contraexemplo representa uma liberdade real do antecedente. O adendo também repara o próprio bloco por D_c=0, obtendo N_E=kN_G mais rN_G e, com física adicionada, também N_A.

O critério global C=D_c=0 satisfaz ambas as saturações; sua condição Hadamard exige a construção microlocal separada. A nota não afirma que zerar esses blocos em um split arbitrário seja uma correção suave. A invariância de S2 frente a mudanças somente de D_c está correta: sua equação é C* N_A contida na imagem de G. A inversa de ocupações suavizantes não foi tratada como um operador contínuo automaticamente.

A segunda quantização algébrica usa o quociente determinado por W, em vez de substituí-lo por outra covariância. A extensão da homotopia aos slots contrai os fatores auxiliares, mas esse domínio de tensores simples não inclui por si todo vetor criado por campos Wick locais. A insuficiência é explicitada, e a composição Fock073 é a prova separada que trata os tensores nucleares completados. Não há mudança das contagens físicas, da ação ambiente ou dos falsificadores neste parecer.
'''
cohom = '''# Parecer da raiz — primitiva ordinária com o espectador B0

10/09/2026. [DERIVED — revisão interna por leitor distinto do autor] [KNOWN — entradas primárias e071 delimitadas] [REAL — leitura integral e pins]. Não identifiquei erro material no argumento ordinário com jatos externos livres e nos controles que delimitam sua aplicação. A versão estacionária é uma composição condicionada às entradas horizontais071, sem nova auditoria completa dessas entradas. O parecer não aprova uma primitiva admissível de Q2 ou a QME.

## Conjugação e sequência de remoção

Desfazer o gauge e retirar os pares não mínimos antes da translação dos ghosts é necessário. Em particular, s cbar=-b não tem a forma de transporte usada na identidade [b_shift,s]. A homotopia dos doublets com todos os jatos é relativa a d_H e admite B0 como parâmetro, como a fonte registra.

No complexo mínimo, [b_shift,s]=d_dyn, enquanto s B0=0 e d_H B0 permanece dx vezes o jato seguinte. Os comutadores seguintes se anulam e b_shift eleva o grau de forma, de modo que a exponencial termina. A fórmula s+d_H=e^b(s+d_ext)e^-b conserva precisamente a derivada externa que uma translação aplicada por homonímia teria perdido.

Conferi a identidade dinâmica no texto primário [BBH1995, equações (6.7)–(6.8)](https://arxiv.org/pdf/hep-th/9505173v2). Sua extensão ao fundo inerte é o cálculo explícito da nota073. A identidade primária não foi usada para considerar B0 constante em x.

Na diagonal de grau total cinco há somente os canais (p,q)=(5,0),(4,1),(3,2),(2,3),(1,4). Os graus dinâmicos 1,2,5 nulos são entradas071. Os outros dois canais dependem de H1 e H2 externos; não exigem apagar H3 de S3. Os homotópicos externos atuam nos valores/jatos de B0 e em x, com os símbolos dinâmicos fixos; por isso o uso com coeficientes de H(s) preserva a estrutura paramétrica, em vez de supor um produto tensorial algébrico de funções suaves conjuntas. A filtração tem cinco níveis, e nenhum diferencial posterior recria uma entrada já zero.

## Finitude e topologia

Conferi [Giachetta–Mangiarotti–Sardanashvily, Proposições 13–14 e Teorema 18](https://arxiv.org/pdf/math/0006074): a comparação horizontal abaixo do grau máximo com de Rham tem a versão de ordem finita. A preservação polinomial local é apoiada pela fórmula explícita de [BBH2000, equações (4.12)–(4.16) e a soma que as segue](https://arxiv.org/pdf/hep-th/0002245v3). A contagem de derivados encerra essa soma; para graus externos 1 e 2 os denominadores não se anulam. O uso de contrações em cartas de valores admissíveis evita a métrica zero.

O espaço de métricas Lorentzianas temporalmente orientadas se retrai, mediante a estrutura euclidiana auxiliar declarada, sobre a direção própria positiva orientada S3; o autovalor positivo e a forma negativa complementar têm fibras contráteis. Seu produto com o alvo S3 tem H1=H2=0 sobre reais/complexos. A topologia não é assumida trivial em todos os graus. Partições suaves e a estrutura auxiliar são ferramentas da prova ordinária, sem serem introduzidas como coeficientes físicos naturais de Q2.

A descida de ghost positivo usa os jatos completos, cujo horizontal abaixo da dimensão não ganha classes de ghost positivo por fibras de ghosts/antifields. Extrair a componente superior de uma primitiva total dá a=sB+d_HC na classe declarada. A conclusão é local no espaço-tempo e global nos valores especificados, não uma condição adiabática ou uma cota de escala uniforme.

## Distinções que permanecem obrigatórias

O caso externo estacionário requer o ideal diferencial completo das equações e as entradas H_char1/H_char2 de071 com sua globalização. Isso não é obtido de uma igualdade só no ansatz FRW. O contraexemplo f(z)dx1, com os outros derivados de z anulados, confirma a diferença: o coeficiente do maior jato em D1F força a retirada sucessiva de todos os jatos de qualquer candidata finita, terminando numa F incapaz de produzir f(z). Uma integral ao longo de uma solução particular não é uma primitiva universal em jatos.

O defeito de coordenadas também confere. A derivada transformada do ghost contém a derivada do Jacobiano vezes o ghost não derivado; b_shift produz então K partial J dx, enquanto a receita reaplicada na carta nova anula o ghost derivado. Portanto a própria homotopia não é natural. Isso demonstra uma obrigação de covariantização, sem provar que nenhuma primitiva natural exista.

Conservam-se os requisitos de universalidade da quebra, naturalidade conjunta, analiticidade, escala, contatos e continuidade na completação formal. Em especial, a retirada cohomológica ordinária do espectador não paga uma mudança admissível de todos os produtos T_n. A direção adequada de uso é: primeiro obter um cociclo na álgebra universal declarada, depois aplicar o teorema e só então verificar o retorno ao espaço de renormalização. A nota respeita essa ordem.
'''
outputs = [new(OUT / 'PARECER_RADICAL_E_REPARO_073.md', radical),
           new(OUT / 'PARECER_COHOMOLOGIA_ESPECTADOR_073.md', cohom)]
for p, expected in zip(sources, before):
    assert pin(p) == expected
receipt = {'status': 'FAVORABLE_INTERNAL_WRITTEN_REVIEWS__DECLARED_SCOPES_ONLY',
           'created_utc': datetime.now(timezone.utc).isoformat(),
           'inputs': before, 'outputs': outputs, 'sources_unchanged': True,
           'new_cas_controls': 0, 'new_lean_compilations': 0,
           'scope': 'Radical/saturation counterexample and repair; ordinary external-jet cohomology. No all-order admissible anomaly removal asserted.'}
rp = new(OUT / 'REGISTRO_REVISOES_RAIZ_073.json', json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'outputs': outputs, 'receipt': rp}, ensure_ascii=True))

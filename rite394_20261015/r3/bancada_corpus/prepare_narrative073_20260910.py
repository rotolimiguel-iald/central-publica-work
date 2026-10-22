from pathlib import Path
from datetime import datetime
import hashlib
import json
import os

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_073_20260910'

def link(label, relative):
    path = ROOT / relative
    assert path.is_file(), path
    return f'[{label}](<{path.as_posix()}>)'

def new(name, text):
    p = OUT / name
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    raw = text.encode('utf-8')
    tmp = p.with_name(p.name + '.tmp_' + datetime.now().strftime('%H%M%S_%f'))
    with tmp.open('xb') as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    assert p.read_bytes() == raw
    return {'path': p.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}

report = f'''# Continuidade da suficiência — entrega 073

10/09/2026. [DERIVED — demonstrações escritas] [KNOWN — entradas analíticas delimitadas] [REAL — artefatos lidos e medidos]. Somente arquivos novos na bancada Chatgpt; fontes originais e entregas anteriores preservadas.

**Avanço principal:** o contrato livre P0 da entrega072 foi realizado no modelo Einstein–sigma e no domínio interior de Cauchy já declarados. Construímos uma polarização Hadamard pura adaptada ao BRST, preservando o estado físico067, e a transportamos a uma Fock–Krein com domínio comum para os campos Wick. Nesse domínio, o kernel da carga livre é positivo e seus vetores de norma nula são exatamente a imagem da carga.

No setor de anomalias, foi demonstrada a exatidão cohomológica ordinária com jatos do fundo de referência B0, mantendo sua derivada horizontal. O retorno dessa primitiva à classe natural e admissível de Q2 continua aberto. Nenhum dos resultados é apresentado como construção da carga interagente renormalizada, QME ou fechamento UV.

## 1. Estado corrente e natureza da evidência

A {link('captura 073', 'REEXAME_SUFICIENCIA_073_20260910/ESTADO_CANONICO_073.json')} encontrou os mesmos bytes dos quatro artefatos canônicos da entrega072. O programa consultado continua v338, com 683 arquivos embutidos e 77 dos 98 módulos do comparador; 21 permanecem ausentes. O selo confere com um.py.

Não houve execução/importação de um.py, Lean, CAS, cálculos de diagramas ou testes de natureza nesta entrega. A evidência nova é matemática escrita, com revisão interna por leitores distintos dos autores nas frentes indicadas. Os controles de hashes e links são documentais. O objetivo geral permanece ativo; a entrega072 anterior foi progresso efetivo e esta entrega acrescenta novas construções, não apenas uma atualização de status.

## 2. Por que era necessário escolher melhor a extensão auxiliar

A {link('análise do radical', 'RADICAL_GNS_BRST_073_20260910/RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md')} demonstra que uma pseudocovariância arbitrária que satisfaça os contratos068 pode falhar em P0. Depois de quocientar o radical ghost, um vetor de vínculos pode se tornar BRST-fechado e ainda ter norma negativa. Um bloco finito realiza esse caso, conservando CCR, Ward e o estado físico anterior.

Não foi identificado como negativo um kernel único medido de068. O resultado refuta uma promoção automática de toda a família, e apresenta duas condições exatas de saturação S1/S2 para recuperar a cohomologia física. O {link('reparo explícito', 'RADICAL_GNS_BRST_073_20260910/REPARO_DO_BLOCO_E_LIMITE_HADAMARD.md')} remove o defeito no plano finito e fornece o formato global a realizar. A {link('revisão da raiz', 'REVISOES_RAIZ_073_20260910/PARECER_RADICAL_E_REPARO_073.md')} conferiu a sequência exata, o bloco e os limites.

## 3. Polarização Hadamard adaptada, preservando a física067

A {link('construção de polarização', 'POLARIZACAO_BRST_HADAMARD_073_20260910/POLARIZACAO_ADAPTADA_E_MAJORANTE.md')} começa com projetores puros Hadamard dos operadores D e Q. O defeito de entrelaçamento com os mapas de gauge e vínculos é suave. A inversa esquerda original e é adaptada por

\\[
e_d=\\sum_{{\\sigma=\\pm}}\\Pi_Q^\\sigma e\\Pi_D^\\sigma,
\\qquad e_1=e_d+(1-e_dk)e,
\\qquad e_1k=1.
\\]

A correção é suave e a inversa continua exata. A construção simplética fornece q,r,p que preservam os ramos de frequência modulo operadores suaves. O extrator físico s0 possui inversa explícita R=s0†. O projetor final é

\\[
\\widehat\\Pi_D^\\pm
=k\\Pi_Q^\\pm q+r\\Pi_Q^\\pm c+R\\Pi_{{067}}^\\pm s_0.
\\]

Ele é idempotente, complementar, compatível com a conjugação e exatamente adaptado ao complexo. A diferença para o projetor inicial é suave, o que prova Hadamard. O bloco físico permanece exatamente o de067; os setores auxiliares ganham a forma cruzada que satisfaz S1/S2. Os modos baixos são tratados pela construção, sem serem apagados.

A nota também constrói uma majorante Hilbert do espaço ghost por cálculo funcional elíptico, preservando os dados suaves. Não supõe positividade de toda a forma auxiliar nem aplica uma escolha de contorno a uma covariância Krein sem controle espectral. A {link('revisão independente interna', 'REVISAO_POLARIZACAO_BRST_073_20260910/PARECER_POLARIZACAO_E_RADICAL.md')} conferiu o encadeamento, incluindo a distinção entre adjunto sesquilinear e transposição bilinear.

## 4. P0 realizado num domínio comum com os campos Wick

A {link('prova Fock/Wick', 'FOCK_HADAMARD_QUARTETOS_073_20260910/FOCK_DOMINIO_WICK_E_P0.md')} usa a mesma covariância construída. O domínio D contém um número finito de partículas, com funções de onda suaves conjuntamente em seus argumentos de Cauchy. Dentro de cada grau, o produto tensorial é nuclear completado; não se limita a somas finitas de tensores simples.

Os quartetos fornecem uma carga Q0 simétrica para a forma de Krein e uma homotopia h, com

\\[
Q_0^2=0,\\qquad Q_0h+hQ_0=N_{{aux}},\\qquad
Q_0R_0+R_0Q_0=1-P,\\quad R_0=N_{{aux}}^{{-1}}h.
\\]

A inversa vale zero no vácuo auxiliar e 1/m no setor com m>0 partículas auxiliares. Todos os operadores preservam D. Para Q0 Psi=0,

\\[
\\Psi=P\\Psi+Q_0R_0\\Psi,
\\qquad [\\Psi,\\Psi]=\\|P\\Psi\\|_{{phys}}^2\\ge0.
\\]

Se a norma é zero, P Psi=0 e a própria fórmula exibe a primitiva R0 Psi em D. A igualdade é com a imagem efetiva da carga, não apenas com seu fecho. O quociente físico coincide com o domínio suave da Fock do estado067.

A estabilidade pelos polinômios Wick compactos microcausais é demonstrada por frentes de onda. As parcelas criadoras têm orientação comum; uma singularidade de saída exigiria uma configuração inteiramente futura ou passada que o kernel microcausal exclui. As contrações com funções de onda iniciais suaves preservam essa propriedade. Isso paga o domínio que faltava ao certificado algébrico de072.

A {link('revisão independente da composição', 'REVISAO_FOCK_DOMINIO_073_20260910/PARECER_FOCK_DOMINIO_E_P0.md')} não identificou erro material. O resultado é P0 no modelo/fundo/classe declarados. A representação dos coeficientes compactos polinomiais da teoria causal também fica disponível, como parte de P1. P1 integral inclui uma carga renormalizada simétrica; sua construção e as identidades de P2 continuam obrigações.

## 5. O espectador B0 ganhou uma primitiva ordinária

A {link('demonstração cohomológica', 'COHOMOLOGIA_ESPECTADOR_B0_073_20260910/PRIMITIVA_ORDINARIA_COM_B0_E_LIMITE_ADMISSIVEL.md')} mantém s B0=0 e d_H B0 diferente de zero. Após desfazer o gauge e contrair os pares não mínimos, a translação finita de ghosts conjuga s+d_H a s+d_ext. O segundo termo deriva x e os jatos externos, em vez de congelá-los.

A diagonal de grau total cinco tem cinco canais. Os graus dinâmicos 1,2,5 nulos vêm das provas071; os outros dois são eliminados pelos grupos horizontais externos de graus1/2, nulos para os valores de métrica temporalmente orientada e alvo S3. Isso fornece a=sB+d_HC na classe coordenada, suave e de jatos finitos, quando a é um cociclo nessa álgebra universal.

A nota distingue jatos livres, o espaço estacionário universal das equações completas e uma igualdade avaliada apenas no FRW escolhido. A última não basta para consumir o teorema universal. Também demonstra que a homotopia coordenada não é automaticamente natural: a mudança não linear de coordenadas produz um termo com derivadas do Jacobiano. A {link('revisão da raiz', 'REVISOES_RAIZ_073_20260910/PARECER_COHOMOLOGIA_ESPECTADOR_073.md')} preserva precisamente esses limites.

Portanto a presença dos jatos de B0 deixou de ser uma lacuna cohomológica ordinária sem tratamento. Permanecem a universalidade e a completação da quebra efetiva, sua primitiva natural, a regularidade/escala requerida e a compatibilidade com todos os produtos, inserções e contatos de Q2.

## 6. Caminho crítico após073

1. **Renormalização admissível:** realizar a primitiva geral na classe efetiva de Q2, com B0 e a completação formal tratados, e removê-la coerentemente em todas as ordens. Exatidão ordinária não é uma normalização causal inteira.
2. **Carga interagente e QME:** construir a corrente, sua representação simétrica, a implementação do diferencial e sua nilpotência. P0 agora está realizado; a existência desses dados renormalizados ainda não foi inferida da representação dos coeficientes.
3. **Fundos e globalidade:** pagar acordo perturbativo, identidade de mudança da cisão e compatibilidade dos estados nas mudanças de cutoff/fundo. Não foi construída uma soma não perturbativa.
4. **Alcance físico e UV:** completar a reconstrução geral pelos mesmos dados selecionados, com os postulados de correspondência declarados, e resolver a rota UV escolhida. O resultado atual usa a ação ambiente e este fundo; não atribui automaticamente seus graus físicos à família mínima de probabilidades.
5. **Integração:** incorporar os 21 módulos anteriores ainda ausentes e formalizar as novas demonstrações. A fase e o ramo já integrados não são reabertos; H3 interno e falsificadores existentes continuam reconhecidos.

O adendo de revisões e a entrega no túnel acompanham este relatório. Nenhum Atlas, índice, memória canônica, original, selo ou gate foi alterado. O lastro construído nesta entrega tem o alcance das provas acima; o objetivo geral continua aberto.
'''

memory = f'''# Memória de trabalho073 — polarização, domínio e contratermos

10/09/2026. Arquivo novo somente em Chatgpt. As memórias canônicas, o Atlas e o índice permanecem somente leitura por ordem do operador. Esta é continuidade documental da bancada, sem atualização silenciosa do acervo.

## Recuperação e classificação

Objetivo geral preservado: mesmos dados selecionados para reconstrução gravitacional geral; fase/ramo já pagos; setor quântico interagente, anomalias e UV ainda precisam de suficiência no alcance pretendido. Classificação do turno072: PROGRESSO, com construções escritas e entrega final. Classificação desta frente073: PROGRESSO, com escolha de polarização e realização de P0 que antes era um contrato.

Canônico capturado por leitura/AST: v338, 683 embutidos, 77/98 módulos comparados e 21 ausentes; os quatro artefatos e o selo conferem com072. Não executar ou importar um.py para consultar; ele pode materializar arquivos. Os hashes e a lista dos ausentes vivem na captura e nos recibos, nunca devem ser reconstruídos de memória.

## Resultados e caminhos

{link('Relatório073', 'REEXAME_SUFICIENCIA_073_20260910/REEXAME_SUFICIENCIA.md')} é a porta principal desta entrega.

RADICAL_GNS_BRST_073_20260910 mostra o contraexemplo finito à promoção universal de068 e a sequência exata 0→H/J→H0(V/N)→N_G/cN_E→0. S1 e S2 são as saturações necessárias à identificação canônica com H/N_A. O reparo C=D_c=0 precisa de controle Hadamard; não zerar blocos numa decomposição arbitrária.

POLARIZACAO_BRST_HADAMARD_073_20260910 realiza esse controle. Adaptar e por e_d=sum Pi_Q e Pi_D e e1=e_d+(1-e_dk)e mantém e1k=1. Darboux produz q,r,p diagonalizados modulo suaves; R=s0† é a inversa física. Pi_hat=kPi_Qq+rPi_Qc+RPi_067s0 é projetor puro, real, exatamente BRST e difere por suave do inicial. Preserva a covariância física067. Dagger é sesquilinear; a transposição simplética bilinear troca os ramos. O lema de majorante usa operador Hilbert elíptico com gap, não Riesz arbitrário em Krein.

FOCK_HADAMARD_QUARTETOS_073_20260910 realiza a covariância numa Fock–Krein. D é soma de graus finitos com tensores nucleares completados de funções suaves. Q0,h,R0,P e polinômios Wick compactos microcausais preservam D. Q0R0+R0Q0=1-P implica positividade do kernel e nulo=imagem no próprio domínio. Esse é P0 realizado para este fundo. A parte representacional de P1 fica paga para os coeficientes indicados; carga renormalizada simétrica e P2 ainda faltam. Não promover domínio suave a convergência ou auto-adjunticidade Hilbert de uma carga nilpotente não nula.

COHOMOLOGIA_ESPECTADOR_B0_073_20260910 conserva d_HB0. Primeiro desfazer gauge e retirar não mínimos; depois conjugação por b_shift leva s+d_H a s+d_ext. Cinco canais de grau total5 são eliminados usando Hs1/Hs2/Hs5 de071 e H1/H2 externos. Primitiva ordinária em jatos livres; versão estacionária requer identidade universal no ideal completo e entradas horizontais071. A igualdade numa referência FRW não é essa universalidade. Naturalidade, T5/escala, contatos e completação Q2 não foram quitados.

## Revisões e próximo passo

Turing revisou a polarização; Herschel revisou a composição Fock/P0 da raiz. A raiz revisou radical/reparo e cohomologia do espectador. Pareceres e pins estão nas respectivas pastas e devem acompanhar qualquer integração. Controles documentais não são teoremas; nesta frente não há novos CAS, Lean, diagramas ou testes de natureza.

Próximo foco: primitiva natural/admissível e sua filtração; carga e corrente renormalizadas implementando a Ward/QME; transporte entre fundos. Globalidade, correspondência física geral, integração e UV continuam distintos. Manter a regra: todos os novos trabalhos em Chatgpt, fontes congeladas intactas, correções por adendo, backups byte a byte antes de qualquer ajuste autorizado de uma memória de trabalho própria.
'''

drawing = f'''# Adendo073 ao desenho do fechamento

10/09/2026. Novo documento em Chatgpt; o desenho canônico não foi alterado. [DERIVED/KNOWN — provas escritas com entradas delimitadas].

## Mudança no caminho crítico

O elo livre P0, abstrato em072, possui agora realização no modelo interior Einstein–sigma:

```text
Física067 + Green/extrator068 + projetores Hadamard
    -> inversa esquerda microlocalmente adaptada
    -> split q,r,p com controle de frequência modulo suave
    -> polarização pura BRST preservando a física067
    -> majorante Krein regular + domínio nuclear suave
    -> carga livre/quartetos + estabilidade Wick
    -> P0: kernel positivo e vetores fechados nulos exatos
```

O {link('relatório073', 'REEXAME_SUFICIENCIA_073_20260910/REEXAME_SUFICIENCIA.md')} localiza as demonstrações e seus pareceres. A parte representacional dos coeficientes interagentes compactos polinomiais também fica disponível. Não há ainda carga interagente renormalizada com todas as identidades.

Na frente de anomalias:

```text
Ward anômala de referência072
    -> obrigação de enquadrar o cociclo universal/completado
    -> primitiva ordinária com jatos B0 [teorema073 disponível]
    -> primitiva natural, regular e com escala Q2 [ABERTO]
    -> normalização de produtos/inserções/contatos [ABERTO]
    -> QME + corrente/carga implementada [ABERTO]
    -> recorrência positiva formal072 com R0 agora realizado
```

Uma identidade numa única referência não substitui o enquadramento universal. A homotopia ordinária tem defeito explícito de covariância; sua existência não é apresentada como contra­termo admissível pronto.

Em paralelo permanecem comparação entre fundos/acordo perturbativo, colagem e cutoff dos estados, alcance geral da reconstrução pelos mesmos dados, condições físicas declaradas e UV. Fase e ramo integrados não são reabertos. Há 21 módulos do comparador ainda ausentes do canônico e novas demonstrações a formalizar. Nenhum gate foi movido; o objetivo geral continua ativo.
'''
outputs = [new('REEXAME_SUFICIENCIA.md', report)]
outputs.append(new('MEMORIA_DE_TRABALHO_073.md', memory))
outputs.append(new('DESENHO_DO_FECHAMENTO_ADENDO_073.md', drawing))
print(json.dumps(outputs, ensure_ascii=True))

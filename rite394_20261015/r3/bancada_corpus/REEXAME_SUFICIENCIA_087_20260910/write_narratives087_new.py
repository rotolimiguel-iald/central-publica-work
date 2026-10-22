from pathlib import Path
import hashlib
import json
import os
from datetime import datetime, timezone
import re

ROOT = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT = ROOT / 'REEXAME_SUFICIENCIA_087_20260910'
SOURCES = [
    'REEXAME_SUFICIENCIA_087_20260910/ESTADO_CANONICO_087.json',
    'REEXAME_SUFICIENCIA_086_20260910/RESULTADO_ENTREGA_086.json',
    'REEXAME_SUFICIENCIA_086_20260910/REEXAME_SUFICIENCIA.md',
    'COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md',
    'COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/MANIFESTO_RELATIVO_CE_087.json',
    'REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md',
    'REVISAO_RELATIVO_QUADRATICO_087_20260910/REGISTRO_REVISAO_RELATIVO_CE_087.json',
    'CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md',
    'CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/MANIFESTO_CE_LINEAR_087.json',
    'REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md',
    'REVISAO_CE_LINEAR_087_20260910_072356_6364824/RECIBO_REVISAO_CE_LINEAR_087.json',
    'CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md',
    'CLASSE_PAR_BRST_COMPLETA_087_20260910/MANIFESTO_CLASSE_PAR_BRST_087.json',
    'REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md',
    'REVISAO_CLASSE_PAR_BRST_087_20260910/REGISTRO_REVISAO_CLASSE_PAR_087.json',
    'REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md',
    'REVISAO_CLASSE_PAR_BRST_087_20260910/REGISTRO_ADENDO_REVISAO_N2_087.json',
    'CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md',
    'CONTRATO_CRITERIO_ANOMALIAS_087_20260910/MANIFESTO_CONTRATO_CRITERIO_087.json',
]

TEXTS = {
'REEXAME_SUFICIENCIA.md': '''# Reexame de suficiência087 — o que avançou e o que ainda falta

10/09/2026. [DERIVED — resultados escritos, com os pareceres independentes ligados abaixo]. [REAL — consolidação documental e snapshot estático]. **A etapa087 calcula os setores CE linear e quadrático do teste fixado e constrói uma classe não nula no BRST clássico completo.** Ainda falta transportar os resultados à classe física interagente, resolver sua quebra de Ward com contratermos admissíveis e completar a reconstrução geral pelos mesmos dados selecionados.

As pendências principais continuam distintas:

1. [OPEN] Reconstrução física geral: obter R, g, T, conservação, calor e área do mesmo registro selecionado, com realização e compatibilidade num atlas físico. A fase/ramo e o H3 interno já reconhecidos no modelo não voltam à lista de faltas.
2. [OPEN] Teoria quântica interagente: resolver os grupos e mapas pertinentes, ou a anomalia concreta, no domínio físico Q2; implementar as normalizações causais e a QME, a carga BRST e o estado físico interagente sob seus contratos.
3. [OPEN — integração] Incorporar e verificar os resultados na execução canônica. A captura087 continua em v338, com77 dos98 módulos acompanhados presentes e21 ausentes. As novas provas escritas não são folhas Lean compiladas nem resultados executados pelo um.py.
4. [OPEN] Regime UV: demonstrar uma rota com alcance explícito além da expansão perturbativa/EFT. Nenhuma finitude de outro objeto substitui essa obrigação.

## O cálculo efetivamente concluído

O contrato é uma referência Lorentziana orientada espaço-forma em dimensão quatro, K>0 real fixado, κ real não nulo, sigma constante projetado ao complexo métrico mínimo e anel real unital não nulo Rher de escalares inertes. Cada coeficiente usa finitos jatos; não se acrescentam tensores espectadores ou dependência coordenada ativa. Mcal é o módulo efetivo dos jatos lineares de Weyl modulo as EOM; Nₘ=Rher⊗SymᵐMcal. A isotropia é h e a álgebra de Killing é gK.

| Setor e complexo | Resultado087 [DERIVED] | Limite do enunciado |
|---|---|---|
| CE linear C(gK,N₁)^h | H^q=0 em todos os graus | É aciclicidade depois do primeiro diferencial induzido por s₁; não anula H(s₀) ou os cochains |
| Relativo quadrático B^p=(N₂⊗Λ^pV*)^h | Somente H⁴ é não nulo: Rher[I₀ν]⊕Rher[J₀ν] | O grau é o do complexo relativo, não ghost da anomalia física |
| CE quadrático C(gK,N₂)^h | H⁴, H⁷, H¹⁰ têm postos2,4,2; os demais são zero | Classifica esta diagonal CE, não todo o BRST |
| BRST clássico completo, truncamentos C_N e completação Ĉ | Rher[A_I] é livre em H⁴(C_N,s), N≥6, e em H⁴(Ĉ,s); A_P=sT_P | É uma linha construída, sem exaustão de H⁴ e sem conclusão sobre QME |

A [prova linear](<C:/IALD/Central de Patentes/Chatgpt/CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md>) usa a injeção do graduado curvo no plano e os tipos da isotropia, seguidos de eliminação finita nos cinco graus horizontais. O [parecer independente linear](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md>) conferiu também o uso da cohomologia vertical em cortes finitos, a curvatura e a extensão escalar.

A [prova quadrática](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>) constrói os singletes curvos Iᵣ,Jᵣ, prova B¹=dB⁰ e B²=0 e reduz □Iᵣ,□Jᵣ triangularmente, com coeficiente principal2. A geração é demonstrada; não se presume liberdade de toda a torre curva. Seu [parecer independente](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md>) examinou a normalização, a paridade, a finitude e a passagem relativo→CE. I₀=½W[1]² e J₀=J_W; este último não designa J=Luz.

## O passo novo além do primeiro complexo CE

A [composição da classe par](<C:/IALD/Central de Patentes/Chatgpt/CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md>) toma a densidade completa ½W(g)²vol_g e substitui suas quatro pernas exteriores pelos ghosts: A_I=ρ_I(g)c⁰c¹c²c³. É s-fechada off-shell e começa em valência seis, I₀ν. A imagem inteira da conexão C₆→C₅ é Rher[J₀ν]+im d₁. A independência de I₀ν e J₀ν no CE impede que um múltiplo não nulo de A_I seja fronteira, incluindo primitivas com antifields.

A projeção a C₆ prova a mesma não exatidão em todo C_N, N≥6, e em Ĉ, sem intercambiar cohomologia e limite inverso. Em contraste, o ciclo completo de Pontryagin A_P é sT_P: sua primitiva começa em valência três. Isso explica por que J₀ν pode ser não nulo no CE e tornar-se exato no complexo completo.

O [parecer da composição](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md>) e o [adendo de consumo da revisão N₂](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md>) mantêm as duas revisões separadas. Aqui s completo significa **BV–BRST clássico em todas as valências**, não um operador quântico renormalizado. Não se conclui que H⁴ inteiro seja essa linha, nem se calcula uma anomalia de ghost um.

## A obrigação de anomalias ficou mais precisa

A [auditoria do critério074](<C:/IALD/Central de Patentes/Chatgpt/CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md>) distingue a filtração por formas daquela por valência. Definindo H_s^(g,q) como cohomologia de s em ghost g e forma q, uma rota suficiente exige:

- H_s^(5,0)=0, H_s^(2,3)=0 e H_s^(1,4)=0;
- H¹(Ebar;H_s⁴)=0 e H²(Ebar;H_s³)=0, nos respectivos graus horizontais1 e2.

Ebar é induzido pelo operador horizontal natural sobre H(s completo); deriva os coeficientes de fundo. Não é a cohomologia de de Rham de S³. O critério não exige H⁴(s)=0: a linha par construída não o refuta. Também se pode resolver somente a classe da anomalia concreta, por uma primitiva causalmente admissível, sem provar essas nulidades globais suficientes.

A descida natural075 já satisfaz seu antecedente no domínio off-shell com os jatos dinâmicos de ghost não zero livres e a categoria de B0 declarada. Descida não é primitiva do cociclo total. Permanecem o transporte de classe, os mapas horizontais e a hierarquia de contratermos com localidade, realidade, escala, regularidade, inserções e contatos compatíveis. O fundo físico Q2 tem φ̄=id; o sigma constante do teste087 não pode substituí-lo.

## Estado canônico e custódia

[REAL — captura estática] O [snapshot087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/ESTADO_CANONICO_087.json>), às10:34:17UTC de10/09/2026, registra READ_ONLY_STABLE_SNAPSHOT. Os quatro pins de um.py, selo, manifesto e stdout v338 são idênticos aos da086. O programa tem11.048.796 bytes e683 arquivos embutidos; a lista acompanhada contém98 módulos, dos quais77 presentes e21 ausentes. Presença estática não é nova compilação. Gate e selftest são declarações da execução registrada, sem nova execução nesta etapa.

A [entrega086 concluída](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_086_20260910/RESULTADO_ENTREGA_086.json>) é antecedente; os resultados087 permanecem em arquivos novos de bancada. Não houve nova execução matemática, CAS, Lean, natureza ou execução/importação de um.py. Hashes e checks desta emissão são documentais. Atlas, índice, memórias e originais não foram alterados ou copiados. A [memória087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/MEMORIA_DE_TRABALHO_087.md>) e o [adendo ao desenho](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/DESENHO_DO_FECHAMENTO_ADENDO_087.md>) conservam o caminho para a sessão codificadora. Resultados posteriores à087 não entram nesta consolidação.
''',
'MEMORIA_DE_TRABALHO_087.md': '''# Memória de trabalho087 — entrada para a próxima sessão

10/09/2026. Documento novo de bancada, sob Chatgpt. [DERIVED — memória de resultados escritos e revistos]. [REAL — estado conforme captura087]. Não é cópia nem atualização do Atlas, índice, diário ou desenho canônico. O [reexame087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/REEXAME_SUFICIENCIA.md>) é a narrativa desta consolidação.

## Estado a recuperar antes de continuar

O [snapshot087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/ESTADO_CANONICO_087.json>) foi capturado às10:34:17UTC de10/09/2026. READ_ONLY_STABLE_SNAPSHOT: os quatro artefatos canônicos medidos têm bytes/pins idênticos à086; v338,11.048.796 bytes no um.py,683 arquivos embutidos,77/98 módulos acompanhados presentes e21 ausentes. A lista dos21 é a do JSON; ela não é uma contagem de toda a matemática ainda aberta. O programa original não foi executado/importado.

A [entrega086](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_086_20260910/RESULTADO_ENTREGA_086.json>) havia fechado a injetividade da divergência para correntes naturais quadráticas finitas de Weyl/EOM, a impossibilidade divV=J_W, H³ CE quadrático zero e a imagem cúbica H³(C_N)→H³(C₃) zero para N≥6. Não afirmou H³(C_N) inteiro zero. A presente etapa acrescenta os cálculos abaixo, sem reabrir fase/ramo do registro ou H3 interno do Um.

## Dicionário fixado

Referência: espaço-forma Lorentziana orientada4D, K>0 e κ≠0 reais fixados; sigma constante projetado ao complexo métrico mínimo. Rher é uma álgebra real unital não nula de coeficientes escalares inertes. Não introduzir tensores espectadores, coordenadas ativas ou funções arbitrárias de novos campos sob esse nome.

Mcal é o módulo efetivo dos jatos lineares de Weyl/EOM; Nₘ=Rher⊗SymᵐMcal. gK é a álgebra de Killing, h a isotropia. Os jatos são finitos por coeficiente; o graduado usa a SOMA das ordens dos fatores. Não se presumiu que a torre curva inteira seja livre.

s=s₀+s₁+s₂+⋯ é o diferencial BV–BRST CLÁSSICO, com s_j aumentando valência E em j e ghost em1. C_N trunca E≤N; Ĉ completa por valência, mantendo ordem finita em cada coeficiente. Depois de H(s₀), o primeiro diferencial por valência é CE na diagonal m=E−ghost. Ele é distinto de Ebar, o operador por FORMAS sobre H(s completo).

H³ aqui é grau cohomológico; H3 interno do programa é outro objeto. J_W é a densidade característica quadrática, não J=Luz. Mcal é módulo, não a matriz de ghosts. t da expansão formal não é o tempo físico r.

## Resultados087 e seus elos

[DERIVED] Na [prova N₁](<C:/IALD/Central de Patentes/Chatgpt/CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md>), todos B^p=(N₁⊗Λ^pV*)^h são zero por tipos e pela injeção do graduado. Cortes finitos da isotropia permitem eliminar a cohomologia vertical. A eliminação usa o diferencial CE INTEIRO, conservando os termos horizontais e de curvatura, e termina nos cinco valores p=0,…,4. Resultado: H^q(C(gK,N₁)^h)=0 em todo q. Não são zero os cochains ou H(s₀) linear. O [parecer N₁](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md>) é separado da autoria da prova.

[DERIVED] Na [prova N₂](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>), Tᵣ=∇̄_(a₁…aᵣ)W[1], Iᵣ=½⟨Tᵣ,Tᵣ⟩ e Jᵣ=½⟨Tᵣ,*Tᵣ⟩ têm representantes curvos efetivos. I₀=½W[1]²; a antiga normalização I082 é2I₀. J₀=J_W é a normalização característica herdada.

- B⁰=⊕ᵣ(Rher Iᵣ⊕Rher Jᵣ), livre por símbolos principais.
- B¹=dB⁰; B²=0 pela antissimetria do tipo requerido na potência simétrica; B³ identifica-se com B¹ pela contração no volume; B⁴=B⁰ν.
- □Iᵣ=2Iᵣ₊₁+restos de ordem≤2r+4; o mesmo para Jᵣ. Em r=0, □I₀=2I₁+12KI₀ e analogamente para J₀.
- A redução triangular é FINITA e divide somente por2. B⁰/□B⁰=Rher[I₀]⊕Rher[J₀]. Não se usa inversa de □ ou série infinita de derivadas.
- Relativo: somente H⁴=Rher². CE: graus4,7,10 com postos2,4,2; demaiszero. A coluna relativa4 é a única sobrevivente e a filtração horizontal é finita.

O [parecer N₂](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md>) verificou a geração curva, os símbolos, a paridade e a passagem relativo→CE. As extensões por Rher são algébricas sobre os reais e cobrem nilpotentes, sem separá-los por avaliações numéricas.

[DERIVED] A [classe par completa](<C:/IALD/Central de Patentes/Chatgpt/CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md>) define A_I=ρ_I(g)c⁰c¹c²c³ a partir de ½W(g)²vol_g. sA_I=0 off-shell; líderE6=I₀ν. A conexão de C₆→C₅ tem imagem Rher[J₀ν]+im d₁. Portanto λA_I ser fronteira implicaria λ[I₀ν]=μ[J₀ν] no CE; a independência força λ=μ=0, inclusive com antifields permitidos na primitiva.

Segue Rher[A_I] livre em H⁴(C_N,s), N≥6, e em H⁴(Ĉ,s), por projeção a C₆. Não se troca H com limite inverso nem se afirma ML. Pontryagin completo A_P=sT_P continua exato: sua primitiva começa emE3, enquanto seu líder J₀ν começa emE6. A [revisão da composição](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md>) e o [consumo posterior da revisão N₂](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md>) foram publicados separadamente. Não há nova afirmação de diferencial posterior por número de página nesta consolidação.

## O que transportar com cautela

Essas conclusões não classificam H⁴ completo, H³ completo ou todos Nₘ. Uma classe CE não sobrevive automaticamente ao BRST clássico; A_P é o controle explícito. Uma classe BRST de ghost quatro não é uma anomalia quântica de ghost um.

A [auditoria074/087](<C:/IALD/Central de Patentes/Chatgpt/CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md>) exige, como rota suficiente, H_s^(5,0), H_s^(2,3), H_s^(1,4) nulos e H¹(Ebar;H_s⁴), H²(Ebar;H_s³) nulos. Os pares são ghost/forma e os dois primeiros índices horizontais são formas1 e2. H_s⁴ não precisa ser zero. Ebar deriva B0; não é só de Rham de S³. Alternativamente, basta construir uma primitiva da quebra concreta na classe causal admissível.

Preservar o que já foi pago: descida075 no domínio off-shell com jatos livres dos geradores pertinentes e categoria de B0 declarada; existência causal auxiliar Q2 e resultados condicionais anteriores. Permanecem o transporte natural/formal e de regularidade, os grupos ou classes totais, as normalizações multilineares, contatos, QME e carga/estado interagentes. O fundo Q2 usa φ̄=id e não o sigma constante projetado do teste. Não recategorizar fontes centrais como constantes horizontais; manter as projeções e graus externos da072/075.

## Próxima passagem à sessão codificadora

Registrar os enunciados e suas hipóteses antes de propor incorporação. Esta memória não autoriza marcar uma folha como compilada ou alterar o gate. Os21 módulos ausentes do plano98 e a formalização das provas087 são obrigações diferentes. A origem física de R, a realização geral de g/T/conservação/área/calor no mesmo registro e o atlas físico continuam abertos; o UV tem obrigação própria além da EFT.

Somente documentos novos sob Chatgpt. Zero novas execuções matemáticas, CAS, Lean, natureza ou um.py; nenhuma alteração de originais/Atlas/índice. Os pins e links são verificados por emissão documental própria, sem reexecutar provas. A revisão independente da narrativa e a custódia final pertencem a atos posteriores da raiz; não são antecipadas aqui. Não se incluem resultados posteriores à087.
''',
'DESENHO_DO_FECHAMENTO_ADENDO_087.md': '''# Adendo de bancada ao desenho do fechamento087

10/09/2026. [DERIVED — caminho crítico após as provas087 revistas]. [REAL — documento novo; desenho canônico preservado]. Este adendo acompanha o [reexame087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/REEXAME_SUFICIENCIA.md>) e a [memória087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/MEMORIA_DE_TRABALHO_087.md>); não copia o Atlas nem altera o desenho original.

**A mudança do caminho crítico:** o teste clássico já tem N₁ CE acíclico, N₂ CE calculado e uma linha livre efetiva em H⁴ do BRST completo. O próximo elo não é repetir a busca quadrática de cancelamento decidida086. É calcular os grupos/mapas ainda necessários e demonstrar a passagem à classe física e à normalização quântica interagente.

## 1. Base que se mantém paga no seu alcance

Fase/ramo e H3 interno já reconhecidos no modelo não são reabertos. A reconstrução condicional anterior e os habitantes particulares mantêm suas hipóteses. A [entrega086](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_086_20260910/RESULTADO_ENTREGA_086.json>) permanece antecedente: divV=J_W é impossível para V natural quadrático finito de Weyl/EOM no teste fixado; a imagem de H³(C_N) em C₃ é zero para N≥6, sem anular todo H³(C_N).

O domínio087 é espaço-forma Lorentziana orientada4D, K>0 e κ≠0 reais fixados, sigma constante projetado, coeficientes Rher escalares inertes e finitos jatos por coeficiente. Ele não é o fundo físico sigma φ̄=id. A extensão escalar inclui nilpotentes e não é uma família de coeficientes espectadores arbitrários.

## 2. Novos resultados estabelecidos por demonstração escrita

| Elo | Conclusão [DERIVED] | O que permite fazer a seguir |
|---|---|---|
| N₁, depois do primeiro diferencial por valência | H^q CE=0 para todo q | Retirar essa diagonal dos próximos cálculos de páginas, sem zerar H(s₀) |
| Relativo de N₂ | Somente H⁴=Rher[I₀ν]⊕Rher[J₀ν] | Usar duas classes independentes e a redução triangular finita |
| CE completo de N₂ | Postos2,4,2 nos graus4,7,10; demaiszero | Conhecer toda essa diagonal da página CE |
| Ciclo par completo A_I | Linha livre em H⁴(C_N,s), N≥6, e H⁴(Ĉ,s) | Estudar mapas horizontais sobre uma classe efetivamente sobrevivente |
| Ciclo característico completo A_P | A_P=sT_P | Preservar a distinção entre classe CE e classe do BRST completo |

Fontes e revisões: [N₁](<C:/IALD/Central de Patentes/Chatgpt/CE_LINEAR_WEYL_TODOS_GRAUS_087_20260910/ACICLICIDADE_CE_LINEAR_E_PRIMEIRO_DIFERENCIAL.md>) e [parecer N₁](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CE_LINEAR_087_20260910_072356_6364824/PARECER_ACICLICIDADE_LINEAR_E_D1_087.md>); [N₂](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_RELATIVO_QUADRATICO_087_20260910_070916_3378612/GERACAO_CURVA_RELATIVO_E_CE_QUADRATICO.md>) e [parecer N₂](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_RELATIVO_QUADRATICO_087_20260910/PARECER_GERACAO_CURVA_RELATIVO_E_CE_087.md>); [classe par](<C:/IALD/Central de Patentes/Chatgpt/CLASSE_PAR_BRST_COMPLETA_087_20260910/CLASSE_PAR_EM_H4_BRST_E_PONTRYAGIN_EXATO.md>), [parecer da composição](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/PARECER_CLASSE_PAR_E_BRST_CLASSICO_COMPLETO_087.md>) e [adendo N₂ consumido](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_CLASSE_PAR_BRST_087_20260910/ADENDO_CONSUMO_REVISAO_N2_087.md>).

O mecanismo não exige liberdade de toda a torre curva: a injeção do graduado, representantes curvos dos singletes e a diagonal2 de □ bastam. A linha par é detectada por projeção a C₆, abrangendo primitivas com antifields. Não se permuta cohomologia e limite inverso. s é CLÁSSICO; a tabela não registra um operador quântico renormalizado.

## 3. Próximo contrato cohomológico, bem tipado

A [auditoria do critério074](<C:/IALD/Central de Patentes/Chatgpt/CONTRATO_CRITERIO_ANOMALIAS_087_20260910/CRITERIO_074_GRUPOS_EXATOS_E_MAPA_085_086.md>) conserva duas rotas suficientes alternativas. A primeira calcula os cinco canais de grau total cinco da filtração por FORMAS:

| Ghost/forma | Alvo a eliminar na classe efetiva |
|---|---|
| (5,0) | H_s^(5,0) |
| (4,1) | H¹(Ebar;H_s⁴) |
| (3,2) | H²(Ebar;H_s³) |
| (2,3) | H_s^(2,3) |
| (1,4) | H_s^(1,4) |

H_s^(g,q) usa o s completo em forma q. Nos dois quocientes horizontais, o expoente externo é forma, não ghost. Ebar induzido em H(s) deriva B0. A linha par não contradiz o critério: H_s⁴ inteiro não precisa ser zero. Os cálculos CE por VALÊNCIA não substituem esses cinco alvos por homonímia.

A segunda rota resolve a anomalia concreta, preservando a classe causal: para a descida Ω, construir T_q com sT_q+E_NT_(q−1)+C_NT_(q−2)=Ω_q. T_q tem ghost4−q, Ω_q ghost5−q; os termos negativos são zero. Aqui C_N é o operador de curvatura da conjugação074, não o truncamento homônimo por valência. Basta resolver as classes concretas dessa recorrência; não é obrigatório anular toda cohomologia potencial.

A descida075 está disponível no seu domínio natural off-shell, com jatos livres dos geradores de ghost não zero e relações de B0 apenas na categoria declarada. Não volta a ser uma pendência genérica. O que ela ainda não fornece é a primitiva total e sua admissibilidade causal. Fontes centrais e projeções conservam os tipos072/075, sem confundir centralidade com constância horizontal.

## 4. Passagem à teoria física interagente

[OPEN] Fixar e demonstrar o transporte para a classe Q2 de referências e inserções, incluindo o fundo φ̄=id, regularidade, naturalidade, ordem finita por coeficiente e completação Rees. O teste com sigma constante não pode ser inserido em lugar desse mapa físico. As comparações já obtidas em domínios ordinários/suaves mantêm suas hipóteses; não fornecem automaticamente primitivas naturais na completação causal.

[OPEN] Construir os contratermos como uma hierarquia multilinear compatível com localidade, suporte, realidade graduada, escala por laço/aridade/inserção, contatos das EOM e as ordens anteriormente normalizadas. Exatidão isolada de uma densidade não implementa essa hierarquia. Demonstrar a remoção da quebra/QME no domínio correto e então construir a carga e o estado físico interagente sob os contratos de domínio e positividade anteriores. A existência do setor linear e dos teoremas condicionais não é descartada nem promovida a essa construção.

[OPEN] Classificar os setores e diferenciais restantes apenas na medida necessária à rota escolhida. Não se demonstrou H⁴ total de posto um, não se anulou todo H³, nem se produziu nova afirmação de diferencial posterior por número de página. Uma classe potencial não determina o coeficiente de anomalia; sua não nulidade não dá um veredito da TGL inteira.

## 5. Obrigações gerais e integração

[OPEN] A suficiência física geral ainda exige R e sua origem física, g e T realizados pelos mesmos dados selecionados, conservação, área/calor e compatibilidade num atlas físico, com os mapas e hipóteses explicitados. Instâncias particulares ou reconstrução condicionada não fazem essa generalidade por si. As previsões e seus resultados contrários já tipados não são apagados; testes de natureza e prova matemática continuam estatutos diferentes.

[OPEN] A rota UV permanece própria, além do alcance perturbativo/EFT declarado. Nem a finitude de jatos por coeficiente nem os postos CE finitos demonstram completude UV.

[REAL] O [snapshot087](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_087_20260910/ESTADO_CANONICO_087.json>) mantém os quatro pins086: v338,683 embutidos,77/98 módulos presentes e21 ausentes. Incorporar os resultados e obter verificações canônicas continua distinto da emissão destas provas escritas. Nenhuma execução matemática, CAS, Lean, natureza ou um.py foi feita nesta consolidação; nenhum original, Atlas, índice ou gate foi alterado. As provas087 são [DERIVED], com revisões documentadas; a custódia final e a revisão da narrativa serão atos próprios posteriores. Resultados posteriores à087 ficam excluídos.
''',
}


def pin(path):
    raw = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def new_atomic(path, data):
    if path.exists():
        raise FileExistsError(path)
    temporary = path.with_name(path.name + '.pending_new087')
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != data or not data:
        raise RuntimeError('Atomic staging mismatch')
    if path.exists():
        raise FileExistsError(path)
    temporary.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError('Final bytes mismatch')


def main():
    if OUT.resolve().parent != ROOT or not OUT.is_dir():
        raise RuntimeError('Unexpected output directory')
    outputs = [OUT / name for name in TEXTS]
    outputs += [OUT / 'PINS_ANTES_NARRATIVOS_087.json', OUT / 'REGISTRO_EMISSAO_NARRATIVOS_087.json']
    if any(path.exists() for path in outputs):
        raise FileExistsError('Narrative outputs must all be new')
    before = [pin(ROOT / relative) for relative in SOURCES]
    helper = pin(Path(__file__).resolve())
    captured = json.loads((ROOT / SOURCES[0]).read_text(encoding='utf-8-sig'))
    previous = json.loads((ROOT / SOURCES[1]).read_text(encoding='utf-8-sig'))
    # All values in the narratives are documentary statements read from these captures.
    # No imported source is evaluated and no canonical file is reopened here.
    before_record = {'utc': datetime.now(timezone.utc).isoformat(), 'sources': before, 'helper': helper,
                     'scope': 'Documentary source pins only; no mathematical execution'}
    new_atomic(OUT / 'PINS_ANTES_NARRATIVOS_087.json',
               (json.dumps(before_record, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    for name, content in TEXTS.items():
        new_atomic(OUT / name, content.encode('utf-8'))
    links = []
    for name, content in TEXTS.items():
        for target in re.findall(r'\]\(<([^>]+)>\)', content):
            path = Path(target)
            links.append({'document': name, 'target': target, 'exists': path.is_file(),
                          'no_line_suffix': re.search(r':\d+$', target) is None})
    after = [pin(ROOT / relative) for relative in SOURCES]
    checks = [
        {'name': 'all_19_sources_unchanged', 'passed': before == after},
        {'name': 'helper_unchanged', 'passed': helper == pin(Path(__file__).resolve())},
        {'name': 'all_local_links_exist', 'passed': all(item['exists'] for item in links)},
        {'name': 'no_literal_line_suffix_in_new_links', 'passed': all(item['no_line_suffix'] for item in links)},
        {'name': 'three_documents_are_nonempty_utf8', 'passed': all((OUT / name).read_bytes().decode('utf-8') == content for name, content in TEXTS.items())},
        {'name': 'captures_are_json_objects', 'passed': isinstance(captured, dict) and isinstance(previous, dict)},
    ]
    if not all(item['passed'] for item in checks):
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))
    result = {
        'utc': datetime.now(timezone.utc).isoformat(),
        'status': 'NARRATIVES_WRITTEN__SOURCE_PINS_AND_LINKS_VERIFIED__FINAL_CUSTODY_PENDING',
        'author': '/root/finish_gibbs_realization',
        'scope': 'Consolidation of written and separately reviewed results087; not a new mathematical review',
        'sources_before': before, 'sources_after': after,
        'helper': helper,
        'outputs': [pin(OUT / name) for name in TEXTS],
        'pins_before_record': pin(OUT / 'PINS_ANTES_NARRATIVOS_087.json'),
        'checks': checks, 'documentary_checks_passed': sum(item['passed'] for item in checks),
        'documentary_checks_total': len(checks), 'local_links': links,
        'mathematical_executions': 0, 'cas_executions': 0, 'lean_executions': 0,
        'um_executed_or_imported': False, 'canonical_files_reopened': False,
        'original_files_written': False, 'atlas_copied_or_written': False,
        'finalizer_tunnel_config_written': False,
        'read_scope': 'Main mathematical sources and review prose read; JSON evidence pinned and parsed where used; no recursive audit claimed',
    }
    receipt = OUT / 'REGISTRO_EMISSAO_NARRATIVOS_087.json'
    new_atomic(receipt, (json.dumps(result, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    print(json.dumps({'status': result['status'], 'outputs': result['outputs'], 'receipt': pin(receipt),
                      'documentary_checks': [result['documentary_checks_passed'], result['documentary_checks_total']],
                      'source_files_unchanged': len(before), 'local_links': len(links)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

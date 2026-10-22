from pathlib import Path
from datetime import datetime
import json,os,hashlib,sys
ROOT=Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
OUT=ROOT/'REEXAME_SUFICIENCIA_076_20260910'
review=Path(sys.argv[1]).resolve()
assert review.is_relative_to(ROOT) and review.is_file()
pins=[]
def new(p,text):
    assert p.resolve().is_relative_to(ROOT) and not p.exists()
    data=text.encode('utf-8')
    temp=p.with_name(p.name+'.tmp_'+datetime.now().strftime('%H%M%S_%f'))
    with temp.open('xb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    assert temp.read_bytes()==data
    temp.rename(p)
    assert p.read_bytes()==data
    pins.append({'path':p.as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
def link(rel,label):
    p=ROOT/rel
    assert p.is_file()
    return '['+label+'](<'+p.as_posix()+'>)'
snap=json.loads((OUT/'ESTADO_CANONICO_076.json').read_bytes())
assert snap['seal_um_hash_matches'] and all(x['unchanged'] for x in snap['comparison_with_delivery075'])
report="""# Suficiência: módulos, correntes e relações características — entrega076

10/09/2026. [DERIVED — matemática escrita revisada] [REAL — documentação medida] [KNOWN — importações delimitadas].

**Esta etapa construiu representantes e primitivas que faltavam no cálculo cohomológico.** O ciclo de volume do alvo é exato no domínio formal; as seis correntes de Killing possuem levantamentos BRST explícitos; as densidades características quadráticas receberam primitivas naturais de ghost3. Também foi demonstrado onde a mudança de base funciona e quais dados ainda são necessários para a completação.

A entrega075 anterior foi progresso: concluiu a descida natural e sua aplicação relativa. Agora avançamos na estrutura das classes que essa descida precisa atravessar. Ainda não obtivemos uma primitiva admissível da anomalia de grau total cinco.

## 1. Estado canônico

"""
report+=link('REEXAME_SUFICIENCIA_076_20260910/ESTADO_CANONICO_076.json','A captura076')+f" manteve os mesmos bytes dos quatro artefatos da075. O canônico permanece na v338, com {snap['embedded_files']} arquivos embutidos e selo correspondente. No conjunto de 98 módulos do integrador anterior, {snap['present']} estão presentes e {len(snap['absent'])} continuam ausentes. A evidência é leitura de bytes e AST, não uma nova execução do programa.\n\n"
report+="""As demonstrações novas são escritas. Foram lidas por revisores distintos de seus autores nas frentes indicadas, sem Lean, CAS, diagramas ou testes de natureza. Hashes e links medem integridade documental. Todas as escritas ficam em Chatgpt; nenhum original, Atlas, índice, memória canônica, selo ou gate foi alterado.

## 2. Ciclos e homotopia do alvo

No setor K, formado por escalares naturais de campos/antifields ativos e ghosts difeomórficos não derivados, demonstrou-se E_N=C_N=0. As conexões cancelam nas contrações escalares; a parte KT não contém ghosts. O resultado inclui A_L=ρ_L c⁰c¹c²c³ para densidades naturais ativas. Ele fornece ciclos, sem lhes atribuir independência ou exaustividade.

Para o volume Ω do alvo S³, a família F_u=Exp_(φ0)(utξ) fornece uma primitiva explícita:

τ3=sK2, com K2=∫₀¹ Ω(F_u)(∂uF_u,sF_u,sF_u)/2 du.

A prova vale mesmo com φ0 não constante: sφ0=0 não significa d_Hφ0=0. A primitiva pode se anular em ξ=0 e ainda ter derivada BRST não nula ali. Trata-se de uma identidade na vizinhança formal da diagonal, não de uma primitiva de de Rham global do volume da esfera.

"""
report+=link('MODULOS_BRST_EBAR_076_20260910/MODULOS_H3_H4_E_SETOR_CALCULADO.md','Nota de módulos')+' · '+link('REVISAO_MODULOS_EBAR_076_20260910_024011_189592/PARECER_MODULOS_EBAR_076.md','Revisão independente')+'.\n\n'
report+="""## 3. Levantamento das seis correntes

Para cada Killing X do alvo, com corrente densitizada 𝒥_X e antifield densitizado φ*, a fórmula construída é

α_X=𝒥_X^μη_μ+(φ*·X)η, com η=c⁰c¹c²c³ e η_μ=∂_Lη/∂c^μ.

A identidade de Noether ∂μ𝒥_X^μ=−𝔈·X cancela exatamente a variação do termo de antifield. Portanto sα_X=0 off-shell. O sinal positivo depende da convenção efetiva sφ*=+𝔈+Lie_cφ*, explicitamente conferida. Não há segunda densitização ou um quarto antifield independente escondido na escrita ambiente S³⊂R⁴.

Os seis representantes α_AB pertencem a K e satisfazem E_Nα_AB=C_Nα_AB=0. Formam a representação Λ²R⁴ do alvo; cada componente não é um escalar O(4) invariante. “Seis” conta as expressões construídas, não a dimensão de H³.

O transporte perturbativo deve incluir o lift cotangente dos antifields. A identidade vale para a série inteira, sem declarar cada coeficiente isolado um ciclo do BRST completo.

"""
report+=link('MODULOS_BRST_EBAR_076_20260910/LEVANTAMENTO_BRST_CORRENTES_KILLING_076.md','Fórmulas e demonstração')+' · '+link('REVISAO_CORRENTES_KILLING_076_20260910_024518_164234/PARECER_CORRENTES_KILLING_076.md','Revisão e precisão Rees')+'.\n\n'
report+="""## 4. Primitivas características com referência métrica

Na apresentação métrica, a conexão total A=Γ(g)dx+∇c tem curvatura F=R(g)(dx+c)²/2 para D=s+d_H. O transporte S=(g0⁻¹g)^(1/2) precisa conter o termo −(DS)S⁻¹; omitir sS perderia a compatibilidade métrica.

Transgredindo entre essa conexão transportada e a de g0, obtivemos D T_P=P(F1,F1)−P(F0,F0). Sua componente de forma zero fornece

s(T_P)_0³=ρ_P(g)c⁰c¹c²c³.

Isso dá primitivas naturais de ghost3 para os ciclos de ghost4 associados às densidades de Euler e Pontryagin, na classe formal declarada. Acrescenta relações concretas à família A_L. Não declara que todas as densidades sejam exatas.

A parcela de forma quatro continua sendo d(T_P)_3⁰=P(R(g),R(g))−P(R(g0),R(g0)). A classe diagonal de Euler(g0) permanece; a obstrução074 não foi apagada. Esses objetos têm grau total quatro, enquanto a anomalia em exame tem grau total cinco.

"""
report+=link('TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md','Transgressão e primitiva')+' · '+'[Revisão independente](<'+review.as_posix()+'>).\n\n'
report+="""## 5. Mudança de base e limite formal

No domínio separado de somas tensoriais finitas, foi demonstrado H((C⊗A)^G)=C^G⊗H(A), com G Lorentz residual, s independente de C e tipos localmente finitos. Relações apenas de B0 não impedem esse resultado. Ele utiliza o H(A) inteiro, sem presumir geração por K.

A invariância rígida O(4) deve ser tomada conjuntamente nos coeficientes e nas classes ativas. Tomar invariantes de cada fator separadamente pode perder contrações permitidas. Além disso, o tensor produto algébrico não é a completação por valência.

A distinção global/formal recebeu um teste concreto: na órbita SU(2) de soluções sigma, τ3 puxa uma forma de volume com integral não nula. Assim sua classe é não trivial no domínio global orientado e é eliminada na vizinhança formal. Isso impede importar como não nula essa classe global para a Q2. Não constitui um núcleo novo se o módulo de chegada já tiver dividido essa relação.

Para as truncagens naturais C_N por valência, sobre o quociente on-shell de B0, demonstrou-se

0 → lim¹ H^(g−1)(C_N) → H^g(lim C_N) → lim H^g(C_N) → 0.

A sobrejetividade das transições nas cocadeias não foi confundida com sobrejetividade na cohomologia. Para g=3/4, precisamos calcular os sistemas relevantes, seus mapas e a comparação com os representantes propostos. Essa fórmula localiza a obrigação restante; não a presume satisfeita.

"""
report+=link('MUDANCA_BASE_BRST_076_20260910_024632_6031800/MUDANCA_BASE_E_COMPLETACAO_H3_H4.md','Demonstrações de mudança de base e limites')+' · '+link('REVISOES_RAIZ_076_20260910/PARECER_MUDANCA_BASE_E_COMPLETACAO_076.md','Revisão da raiz')+'.\n\n'
report+="""## 6. O que resta para o objetivo geral

O próximo passo matemático é estabelecer os representantes e relações dos módulos completos de H³/H⁴ na mesma classe natural formal, controlando as truncagens. Continuam necessárias as nulidades nos demais graus do critério074 e os dois canais com coeficientes de Ebar_N. O trabalho077 posterior fica fora das conclusões desta entrega.

Depois será preciso construir a primitiva total da anomalia e a família de contratermos que preserve regularidade, escala, independência funcional, inserções e contatos. Permanecem corrente/carga interagentes, implementação, nilpotência e QME, além da compatibilidade entre fundos, estados e cutoffs. A positividade P0 no setor livre declarado é preservada; a positividade interagente continua consumindo hipóteses posteriores.

No objetivo completo também continuam a reconstrução gravitacional geral pelos MESMOS dados selecionados e a justificação da rota UV. A existência de exemplos ou a declaração de uma ação não fornecem automaticamente a correspondência geral. Fase, ramo, H3 interno e os falsificadores existentes não são reabertos.

Para integrar, conservar notas, adendos e revisões como conjunto. Não registrar uma bandeira de anomalia removida ou QME a partir desses resultados de grau3/4. Nenhuma confirmação física ou conclusão do objetivo geral é atribuída à etapa076.
"""
new(OUT/'REEXAME_SUFICIENCIA.md',report)
new(OUT/'MEMORIA_DE_TRABALHO_076.md',"""# Memória da etapa076 — bancada Chatgpt

10/09/2026. Adendo novo; não copia nem bifurca o Atlas. O turno075 foi progresso: entrega concluída de descida natural e aplicação relativa.

[REAL] Captura076 mantém quatro pins da075 e selo correspondente. Nenhum um.py executado/importado; originais e memórias canônicas somente leitura.

[DERIVED] Setor K com E_N=C_N=0; ciclos A_L; primitiva formal τ3=sK2 com φ0 variável. Levantamento explícito das seis correntes α_X=𝒥_X·η_μ+(φ*·X)η, sα_X=0 off-shell. Seis não é dim H³; antifields densitizados e lift cotangente completos.

[DERIVED] Transgressão total com A=Γdx+∇c e transporte S incluindo sS. Relação s(T_P)_0³=A_P para Euler/Pontryagin ativas; a classe diagonal de Euler(g0) permanece em outro grau.

[DERIVED] Mudança de base finita/separada; invariantes Lorentz e O4 separados; τ3 global não trivial por teste SU2, mas formalmente exato; sequência de lim/lim¹ para truncagens. Não confundir M antes do transporte com M já quocientado no alvo.

[OPEN] Módulos completos e mapas de truncagem, canais E2, primitiva admissível da anomalia, família causal, carga/QME e acordo perturbativo. Também reconstrução geral pelos mesmos dados, rota UV e integração canônica. P0/fase/ramo/H3 interno/falsificadores preservados.

Revisões escritas específicas por leitores distintos dos autores. Zero CAS/Lean/diagramas/natureza novos; nenhum gate movido. Resultados077 posteriores fora desta entrega.

"""+link('REEXAME_SUFICIENCIA_076_20260910/REEXAME_SUFICIENCIA.md','Relatório076')+'\n')
new(OUT/'DESENHO_DO_FECHAMENTO_ADENDO_076.md',"""# Desenho do fechamento — ADENDO076

10/09/2026. [DERIVED — demonstrações escritas].

075: consistência causal off-shell → descida natural → Ω total fechado.

076 acrescenta ao cálculo da primitiva:
- representantes α_X das seis correntes sigma, fechados para s e com E_N=C_N=0;
- relação τ3=sK2 na vizinhança formal;
- relações s(T_P)_0³=A_P para densidades características;
- comparação finita de coeficientes e sequência de lim¹/lim para as truncagens.

A tarefa restante deixa explícitos os objetos a classificar: H³/H⁴ com essas relações na classe de chegada; sistemas H²/H³/H⁴ das truncagens e seus mapas; demais graus e canais E2 do critério074. Não importar classes globais como não nulas depois de uma completação que pode eliminá-las. Não tomar invariantes O4 separadamente.

Após o cálculo: primitiva total admissível → normalizações causais compatíveis → Ward/QME e carga interagente → consumo da positividade formal. Esse trecho continua aberto.

Em paralelo: reconstrução geral a partir dos mesmos dados TGL, compatibilidade de referências/estados e rota UV. Integração e formalização são obrigações distintas. Nenhuma dessas frentes foi substituída pelo setor particular calculado.

Fase, ramo, H3 interno e falsificadores permanecem preservados. Originais intactos.

"""+link('REEXAME_SUFICIENCIA_076_20260910/REEXAME_SUFICIENCIA.md','Relatório e fontes')+'\n')
print(json.dumps(pins,ensure_ascii=True))


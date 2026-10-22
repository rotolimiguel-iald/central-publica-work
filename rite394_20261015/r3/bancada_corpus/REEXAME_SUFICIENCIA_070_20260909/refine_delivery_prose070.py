from pathlib import Path
from datetime import datetime
import hashlib
import os

root = Path(r'C:\IALD\Central de Patentes\Chatgpt').resolve()
path = Path(__file__).resolve().with_name('finalize_delivery070.py')
assert path.resolve().is_relative_to(root)
original = path.read_bytes()
source = original.decode('utf-8')
start = source.index("new_text(OUT / 'MEMORIA_DE_TRABALHO_070.md'")
end = source.index('\nfor path in sorted(OUT.iterdir()):', start)
replacement = r"""new_text(OUT / 'MEMORIA_DE_TRABALHO_070.md', f'''# Memória local de continuidade — entrega 070

Registro UTC {created}. Esta é uma nota de continuidade da bancada. O relatório e o resultado estruturado ao lado fornecem as referências completas; o manifesto registra os bytes das fontes. O Atlas permanece como fonte canônica de consulta.

[REAL] Os quatro artefatos canônicos conferem com a captura 069. O programa v338 contém 683 arquivos embutidos. Dos 98 módulos do conjunto comparado, 77 estão presentes e 21 continuam pendentes. Nenhum um.py foi executado ou importado. Originais, gates e ritos permanecem intactos. A cópia histórica de 98 módulos serve para portar deltas ao programa vivo, sem substituí-lo. Fase e ramo, seletor, H3 interno e falsificadores existentes permanecem preservados. As contagens da auditoria 069 são históricas: 105 arquivos, 560 condições repetíveis, 6 condições históricas e 14 verificações adicionais.

[DERIVED] Equivalência BV formal: S=sqrt(gbar^-1 g) e e=exp(chi) ebar S. A raiz é uma série formal local em assinatura indefinida. A variável upsilon=s chi é invertivelmente relacionada ao ghost Lorentz, com a compensação de difeomorfismos mantida. O levantamento cotangente local aos antifields separa Snew=Smetric+chi*upsilon. Os pares (chi,upsilon) e (upsilon*,p=s upsilon*) são contráteis também módulo d. Sob mudança externa Omega(x), o ghost antigo obedece cL'=Ad(Omega)cL−(Lie_C Omega)Omega^-1; chi e upsilon transformam adjuntamente. Naturalidade simultânea nos dados de fundo não demonstra independência de fundo.

[DERIVED] Topologia e redução de graus: o volume de S³ tem descida de grau total 3. Para uma 2-forma fechada no alvo fixo, Hodge fornece uma primitiva global alpha1. A identidade D(alpha1 q3)=Omega2 q3 decorre de alpha1 P4 ter cinco direções horizontais em dimensão quatro. A primitiva pode conter Chern–Simons e pertence à classe explicitada na nota. A cohomologia de Lie relevante tem graus 0, 3 e 6. Em ghost total 5, somente o nível xi² multiplicando uma classe de grau 3 pode sobreviver; H²_char,cov=0 permite eliminá-lo por uma indução finita. Coeficientes suaves no alvo são compatíveis com a etapa de Lie. Uma partição de unidade comuta com s0, mas não automaticamente com s ou d. Questões globais e discretas continuam próprias.

[DERIVED, KNOWN] Normalidade: a fonte BBH inclui Einstein com ou sem constante cosmológica. Com K=N_deriv+2N_field*+3N_ghost*, temos delta_Lambda=delta_0+Lambda delta_-2. Uma primitiva relativa de base com K controlado transporta-se por descida finita em K. Na completação formal dos valores não diferenciados, o quadrático Pauli–Fierz mais três escalares fornece a normalidade e a eliminação formal de M2. Esse resultado preserva a polinomialidade nos jatos diferenciados; não permite afirmar que uma série formal seja uma função suave na carta inteira.

[DERIVED] Reducibilidade: Lie_v g≈0 e v·dphi≈0 implicam v·dQ≈0. O jato u_i^A=delta_i^A, u_0=0 e B01^1=B10^1=b tem tau=0 e dQ=−2b dx0. Adjugata, densidade da região não degenerada e continuidade dão v≈0, sem introduzir inversos de gradientes. Aqui B=Du=D(dy) é o Hessiano. Isso elimina f em a2=C* f+M2; ainda falta eliminar M2 na classe relativa suave covariante. O próximo contrato é essa primitiva, ou uma homotopia direta de H²_char,cov.

[DERIVED] Admissibilidade: um contratermo que cancela a quebra não precisa já ser invariante sob o gauge quântico. Naturalidade sob transporte simultâneo dos dados de fundo é uma exigência distinta. A transgressão T3(A,Abar) satisfaz dT3=tr(F²)−tr(Fbar²), mas não é uma primitiva de toda anomalia. A média por O(4) preserva primitivas globais já existentes em uma classe estável; não prova sua existência. A condição de realidade exige uma involução graduada compatível.

[DERIVED] Renormalização: C4 reduzido tem coeficientes A1=−13s²/16+7s/6+1/6 e A2=27s²/8−s+1/3, onde s=kappa c. Em s=4, A1=−49/6, A2=151/3 e 3A1+A2=155/6. Há um certificado explícito C42_poly=Cred+div J+E:M+s|tau|²/6. Trata-se de uma extensão polinomial escolhida, sem calcular a verdadeira Hessiana fora das soluções. A convenção euclidiana gB=gR+K A log(rho²/mu²), K=hbar/(4pi)², dá beta=2KA. A conversão local de ação declarada dá beta_B_FRW=−155K/3 em s=4. Ela não fixa o valor finito de B, um fluxo único de kappa, o sinal da energia ou a retroação completa. Após Bochner, a divergência explícita vale 3x/4; antes, valia 5x/4. Ambos os representantes recuperam o mesmo C4 total.

[REAL] Os 16 controles simbólicos exatos novos de RG passaram. Nenhuma compilação Lean nova foi feita. As revisões internas delimitadas e as verificações de bytes não certificam o objetivo físico completo.

[OPEN] Primitiva relativa suave M2 ou H²_char,cov; descida e admissibilidade na classe Q2; remoção da anomalia e equação mestra quântica; setor e estado físico interagentes; independência de fundo e questões globais; condições finitas e controle UV; correspondência física e alcance da reconstrução; medida independente do campo de probabilidades e BRST vertical, se alegados; integração dos 21 módulos e formalização das deduções novas. O objetivo geral permanece ativo.
''')

new_text(OUT / 'DESENHO_DO_FECHAMENTO_ADENDO_070.md', '''# Caminho crítico local — adendo 070

Resultados preservados: registro de fase e ramo, seleção, reconstruções condicionais com ação declarada, fundo global, inverso variacional, estado físico livre, BRST completo e construção Q2 de produtos renormalizados na álgebra auxiliar.

A comparação métrica–vielbein agora dispõe de equivalência BV formal com antifields e derivada horizontal. A normalidade relativa formal, o transporte finito em Lambda e a ausência de reducibilidade universal por dphi e dQ também estão demonstrados nos alcances indicados. Essas etapas já não devem ser listadas como lacunas integrais.

O caminho local das anomalias é: H²_char,cov na classe suave admissível → eliminação do nível xi² vezes CE de grau 3 → descida e comparação no mesmo espaço → primitiva da quebra → renormalização finita e equação mestra quântica. O resíduo concreto é a primitiva de M2, quadrático nos antifields, preservando coeficientes suaves e covariância; uma homotopia direta de H²_char,cov seria uma alternativa. A aciclicidade KT ordinária e o teste C0 de grau quatro não substituem esse passo.

No alvo S³, o volume tem grau total três. O candidato misto Omega2 q3 tem primitiva na álgebra explicitada. A colagem para s0 não é automaticamente colagem para s ou d. A transgressão com fundo ilustra admissibilidade, sem remover uma quebra específica. Questões globais, discretas e de independência de fundo continuam separadas.

A redução de C4 fornece um representante EFT, um certificado em equações de movimento e divergências e coeficientes logarítmicos de RG, com 16 controles simbólicos novos. Restam condições de renormalização finitas, observáveis com cancelamento da dependência de escala e as construções de estado e de retroação exigidas. O fluxo de uma volta não fornece a conclusão UV.

Permanecem também o alcance geral da correspondência entre dados e geometria, a comparação de fundos, uma eventual quantização independente do campo de probabilidades e a integração dos 21 módulos anteriores com formalização dos resultados novos. Nenhuma compilação Lean nova em 070; gates intactos; objetivo ativo.
''')

new_text(OUT / 'ADENDO_REVISOES_070.md', f'''# Revisões e correções ao lado — entrega 070

[DERIVED] Equivalência BV e admissibilidade foram examinadas por outro agente. A raiz revisou integralmente topologia, redução de graus, normalidade e reducibilidade. A redução RG recebeu revisão de outro agente, autor do coeficiente de entrada e não da redução nova. Os escopos estão explícitos nos pareceres. Essas revisões são internas e delimitadas.

A revisão documental do relatório está em <{review_directory.as_posix()}>. O manifesto final registra os bytes do relatório, notas, revisões e fontes referidas. As verificações documentais são distintas dos 16 controles simbólicos e das demonstrações analíticas.

Correções ao lado: Lambda isoladamente não é um obstáculo de normalidade; o resíduo envolve primitivas suaves covariantes relativas. O ghost Lorentz antigo tem um termo compensador sob mudança Omega(x). O Hessiano é B=Du=D(dy). C0 não é a hipótese residual da redução específica em ghost cinco. As divergências 3x/4 e 5x/4 pertencem a representantes diferentes antes e depois de Bochner, com C4 total inalterado. Os documentos congelados permanecem intactos.

O resultado H4_2 formal não fornece a primitiva suave M2. A prova de ausência de reducibilidade por densidade anula o parâmetro; ela não produz primitivas regulares por inversão de um determinante. A equivalência BV usa a completação declarada e um fundo fixo. A construção Q2 da entrega 069 continua sendo uma álgebra auxiliar com quebra consistente; a equação mestra quântica ainda precisa ser satisfeita.
''')

tunnel_pin = new_text(tunnel, f'''# Entrega 070 — cohomologia relativa, equivalência BV e renormalização

[Relatório](<{report.as_posix()}>) · [Resultado estruturado](<{(OUT / 'RESULTADO_ENTREGA_070.json').as_posix()}>) · [Manifesto](<{(OUT / 'MANIFESTO_ENTREGA_070.json').as_posix()}>).

[REAL] Os quatro artefatos canônicos v338 permanecem iguais aos da captura 069. Dos 98 módulos comparados, 77 estão presentes e 21 continuam pendentes. Nenhum um.py foi executado ou importado. Nenhum original foi escrito; nenhuma compilação Lean ou teste de natureza foi realizado. A integração deve portar deltas da cópia histórica ao programa vivo.

[DERIVED, KNOWN] Resultados novos: equivalência BV local formal entre métrica e vielbein, incluindo ghosts e antifields, também módulo d; descida do volume de S³ e primitiva do candidato Omega2 q3 na classe declarada; redução finita de ghost cinco a H²_char,cov; transporte finito em Lambda; ausência de reducibilidade universal via dphi e dQ sem inversos de gradientes; normalidade e H4_2 na completação formal indicada; redução de C4, certificado em EOM e divergências, redefinição de campos e fluxo logarítmico de RG.

Os coeficientes são A1=−13s²/16+7s/6+1/6 e A2=27s²/8−s+1/3. Em s=4: A1=−49/6, A2=151/3 e 3A1+A2=155/6. A convenção euclidiana gB=gR+K A log(rho²/mu²) dá beta=2KA. Na conversão local de ação especificada, beta_B_FRW=−155K/3, com K=hbar/(4pi)². O valor finito de B, um fluxo único de kappa e a retroação completa permanecem por determinar. A divergência reduzida vale 3x/4; antes de Bochner, 5x/4. O C4 total permanece (7440x²+1616x−211)/96.

[OPEN] O próximo contrato é a primitiva relativa M2 com coeficientes suaves e covariantização, ou uma homotopia direta de H²_char,cov. Depois é necessário ligar a descida e a admissibilidade à quebra interagente produzida, removê-la e satisfazer a equação mestra quântica. O resultado formal H4_2 não foi promovido a H²_char,cov suave. A ausência de reducibilidade também não fornece, por si, primitivas globais.

[REAL] Há 16 controles simbólicos exatos novos aprovados e nenhuma compilação Lean nova. Notas e revisões têm seus bytes registrados no manifesto. Fase e ramo, H3 interno e falsificadores existentes permanecem preservados. Continuam abertos o setor e estado físico interagentes, questões globais e de fundo, controle UV, condições finitas, correspondência física e alcance da reconstrução, medida independente e BRST vertical do campo de probabilidades se alegados, além da integração e formalização. Memória e desenho locais são arquivos novos; Atlas e memórias canônicas permanecem somente leitura. O objetivo geral continua ativo.
''')
"""
updated = (source[:start] + replacement + source[end:]).encode('utf-8')
compile(updated, str(path), 'exec')
stamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
backup = path.with_name(path.name + '.bak_' + stamp)
temporary = path.with_name(path.name + '.tmp_' + stamp)
for target, data in ((backup, original), (temporary, updated)):
    with target.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    assert target.read_bytes() == data
assert path.read_bytes() == original
os.replace(temporary, path)
assert path.read_bytes() == updated
assert backup.read_bytes() == original
print({'status': 'PROSE_REFINED_WITH_BYTE_BACKUP', 'backup': str(backup),
       'before_bytes': len(original), 'after_bytes': len(updated),
       'expected_change': 'Human-readable templates rewritten before first finalizer execution; verification logic preserved.',
       'sha256': hashlib.sha256(updated).hexdigest()})

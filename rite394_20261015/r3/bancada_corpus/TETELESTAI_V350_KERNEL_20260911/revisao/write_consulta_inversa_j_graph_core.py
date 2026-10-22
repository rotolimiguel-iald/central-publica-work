from pathlib import Path
import datetime, hashlib, json, os

REV = Path(__file__).resolve().parent
ROOT = REV.parent
date = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
names = ['ScalarRightGraphCore', 'ScalarRightHilbertCore', 'ScalarRightPairVector',
         'ScalarPairedRightAlgebra', 'ScalarCommutantSandwich', 'ScalarGNSVonNeumann',
         'CorePolarInclusion', 'ScalarTomitaAdjoint', 'ScalarTomitaPolarFactor',
         'ScalarTomitaPolarInvolution', 'ScalarTomitaPositiveRoot', 'ScalarTomitaRootDomain',
         'AntilinearAdjointGraph', 'AntiunitaryPositiveConjugation']
pins = {f'kernel/TGLV350/{n}.lean': sha(ROOT / f'kernel/TGLV350/{n}.lean') for n in names}
pins['right_graph_core_custody.json'] = sha(ROOT / 'right_graph_core_custody.json')

def src(name, line):
    p = ROOT / f'kernel/TGLV350/{name}.lean'
    return f'[{name}:{line}](<{p.as_posix()}:{line}>)'

text = f'''# Consulta — inclusão inversa com J original após o graph-core de F

{date}. **CONSULTA MATEMÁTICA; sem compilação, revisão DEV nova ou promoção de gate.**
Leitura pontual de interfaces; pins dos arquivos consultados no JSON acompanhante.
Mãe lida: `right_graph_core_custody.json`, SHA256 `{pins['right_graph_core_custody.json']}`.

A rota econômica é usar a álgebra dos pares direitos como álgebra de Hilbert à esquerda e provar **uma identidade de multiplicação para seus quadrados**, com o J original. Geração, fecho forte e extração de um elemento da base já possuem interfaces. O novo graph-core resolve a identidade da involução fechada; não resolve sozinho a identidade de multiplicação abaixo.

Notação: H=ScalarGNSHilbert P, M=π(N)=scalarGNSVonNeumann P,
E=scalarPairedRightAlgebra P, j=scalarRightPairVector P,
S=scalarClosedTomita P, F=scalarTomitaAdjoint P,
B=scalarTomitaPositiveRoot P, J=scalarTomitaPolarFactor P.
Escrevo a também para o operador a.val, quando a∈E.

## Interfaces efetivas

| Fato existente nas fontes consultadas | Interface |
|---|---|
| j(ab)=a j(b), j injetivo e de imagem densa | {src('ScalarRightPairVector',79)}, linhas72 e101 |
| Multiplicação esquerda limitada, identidade de adjuntos e produtos densos na norma vetorial | {src('ScalarRightHilbertCore',34)}, linhas39 e94 |
| Fecho do grafo j(a)↦j(a*) é o gráfico do F original | {src('ScalarRightGraphCore',60)} |
| Auto-adjuntos direitos densos em Fix F, como espaço real | {src('ScalarRightGraphCore',43)} |
| E gera todo M′ | {src('ScalarPairedRightAlgebra',124)} |
| Unidade aproximante em E, convergência forte | {src('ScalarRightHilbertCore',74)}, linha80 |
| Todo T∈M′ é limite forte de pares, com cota uniforme | {src('ScalarCommutantSandwich',133)} |
| M é a imagem efetiva de π, não apenas uma álgebra que a contém | {src('ScalarGNSVonNeumann',139)} |
| Jπ(a)J∈M′ para todo a∈N | {src('CorePolarInclusion',58)} |

Transportar o produto e o produto interno por j fornece os dados usuais de uma álgebra de Hilbert à esquerda: completamento H, multiplicadores limitados, adjunto compatível, produtos densos e involução fechável. **A norma vetorial é ‖j(a)‖, não a norma de operador de a.** Não é necessário declarar uma estrutura Lean enorme antes de usar esses dados em lemas genéricos. Não se infere a propriedade de álgebra plena por simples nomenclatura.

## Polar de F: ponte em desenvolvimento pelo main

[DERIVED — argumento matemático, não compilado nesta consulta] De S=JB em D(S)=D(B), B auto-adjunto máximo e J²=1 segue

    D(F) = {{y | Jy∈D(B)}},   Fy=B(Jy),   F=JSJ.

Com a convenção local do produto interno, o pareamento é
⟨Sx,y⟩=⟨JBx,y⟩=⟨Jy,Bx⟩. A existência de z com esse valor igual a ⟨z,x⟩ para todo x∈D(B) caracteriza Jy∈D(B*) e z=B*Jy. A auto-adjunção máxima de B dá a equivalência de domínios, não apenas uma inclusão.

O main informou `ScalarTomitaAdjointPolar.lean` em elaboração. Essa fonte não foi examinada nem aceita nesta consulta. Após sua prova, J×J transporta graph F para graph S e transporta o novo core. Também B_F=JBJ, no domínio J D(B), é positivo e auto-adjunto, e F=J B_F. Isso identifica o polar de F com o mesmo J; não demanda construir outra raiz. Para positividade: Re⟨y,JBJy⟩=Re⟨Jy,BJy⟩≥0. A prova da auto-adjunção transportada deve conservar o domínio máximo.

**Ainda não segue** que Jj(a) seja vetor de multiplicação limitada à esquerda, nem que JaJ∈M. O transporte de gráficos não contém uma estimativa de multiplicação.

## Elo posterior exato a provar

Para a∈E, ponha ξ_a=j(a*a), η_a=Jξ_a e X_a=J(a*a)J.
X_a já é um operador limitado positivo, com norma ‖a‖². Pela ponte acima,
η_a∈D(S) e Sη_a=η_a. A obrigação que falta é:

    (★)  ∀ a b∈E,   X_a j(b) = b η_a.

Nome proposto, ainda inexistente: `scalarRightSquare_J_intertwines`.
Em tipos locais, ambos os membros vivem no H original; b é um operador de
`scalarPairedRightAlgebra P`, e X_a usa `antiunitaryConjugate
(scalarTomitaPolarFactor P) ((star a * a).val)`.

Como X_a*=X_a, (★) também fornece a segunda identidade de adjunto com o mesmo vetor. Portanto ela constrói um multiplicador limitado no comutante da álgebra E, com vetor explícito Jj(a*a). Não deve ser confundida com a estrutura autoral `ScalarRightAdjointPair`, cujo domínio de teste é o ideal original nν: aqui o domínio de teste é j(E).

## Por que (★) é suficiente — fechamento sem novo argumento modular

1. Para b,c∈E, pela lei de produto e (★):

       X_a b j(c) = X_a j(bc) = bc η_a = b X_a j(c).

   A densidade de j(E) dá [X_a,b]=0. Logo X_a∈E′=(E′′)′=(M′)′=M.
   A última igualdade usa a VNA efetiva já provada.

2. Basta conhecer isso para quadrados. Polarização complexa expressa qualquer produto bc como combinação linear de quadrados d*d. A conjugação por J conjuga os coeficientes; ela não é ℂ-linear. Se e_h é a unidade aproximante própria de E, e_h a→a fortemente. Assim J(e_h a)J∈M e o fecho forte dá JaJ∈M para todo a∈E.

3. Para T∈M′ use os sanduíches já construídos K_h(T)∈E eventualmente, K_h(T)→T fortemente. Então JK_h(T)J→JTJ fortemente. Como M é VNA, JTJ∈M. `mem_scalarGNSVonNeumann_iff` fornece b∈N com JTJ=π(b); J²=1 dá T=Jπ(b)J.

Esta parte pode virar um lema genérico de geração por quadrados seguido da aplicação concreta. A hipótese (★) deve permanecer visível até ser provada; dar-lhe um campo numa estrutura não a descarrega.

## Como atacar (★), e o que continua difícil

[KNOWN — fonte primária] A identidade procurada é a especialização em t=0 da reconstrução de quadrados de Rieffel–Van Daele, §5.10, aplicada à álgebra E e ao polar de F. A prova publicada passa pelos lemas5.6–5.9; não toma KMS como hipótese. Não estou invocando o teorema5.13 como prova Lean. [Rieffel–Van Daele1977, §5](https://msp.org/pjm/1977/69-1/pjm-v69-n1-p17-s.pdf).

[PROPOSTA — obrigação nova] Primeiro, para ξ=j(a) auto-adjunto e Reλ=1, construir η∈Fix S com Re⟨ξ,ζ⟩=Re(λ⟨η,ζ⟩) para todo ζ∈Fix S, e provar que j(b)↦bη é limitado, com adjunto compatível. A equação real não fornece sozinha essa cota. Os blocos de projeção são infraestrutura; detecção positiva ainda não é essa estimativa.

A família deve depois produzir (★); λ=1 isolado não foi mostrado suficiente. Essa extração analítica continua faltante. Nenhuma versão genérica pronta foi localizada nas interfaces examinadas. Um eventual fluxo abstrato de B tampouco identifica o fluxo candidato/KMS do peso.

## Diagnóstico

**Próximo elo substancial: reconstrução limitada dos quadrados da álgebra direita por (★).** O polar de F e a geração por quadrados são pontes menores, rigorosas e úteis, mas a dificuldade analítica não desaparece ao escrevê-las. Não recomendo refazer Gaussian V, completar novamente o GNS ou reabrir o graph-core já provado.

Não há inversa deduzida apenas da inclusão direta: `antiunitaryConjugate_commutation_flip` aplicado a dois elementos de M só devolve a mesma inclusão. Domínio/Fix S tampouco implica multiplicação limitada: mesmo no exemplo tracial abeliano L², vetores reais não limitados estão em Fix S e não multiplicam limitadamente L². Esse exemplo não refuta (★); mostra por que seu caráter especial de quadrado e sua cota são essenciais.

[OPEN] Inclusão inversa com J original até provar (★) ou uma ponte efetiva alternativa; identificação de Δ^it, KMS, traço e flags. Nenhuma compilação, execução de monólito/helper, modificação de fonte ou memória nesta consulta. Pareceres anteriores intactos.
'''

def atomic_new(p, raw):
    assert p.parent == REV and not p.exists()
    tmp = p.with_name(p.name + '.tmp_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    with tmp.open('xb') as f:
        f.write(raw)
    assert tmp.read_bytes() == raw
    os.replace(tmp, p)
    assert p.read_bytes() == raw

p = REV / 'CONSULTA_INVERSA_J_APOS_GRAPH_CORE_F.md'
atomic_new(p, text.encode())
data = {'timestamp': date, 'mode': 'READ_ONLY_MATHEMATICAL_CONSULTATION_NO_COMPILATION',
        'report': str(p), 'report_sha256': sha(p), 'read_source_pins': pins,
        'author_in_progress_module_reviewed': False, 'new_Lean_theorems_claimed': False,
        'sources_or_memories_written': False}
atomic_new(p.with_suffix('.json'), (json.dumps(data, ensure_ascii=False, indent=2) + '\n').encode())
print(json.dumps({'report':str(p), 'sha256':sha(p)}, ensure_ascii=False))

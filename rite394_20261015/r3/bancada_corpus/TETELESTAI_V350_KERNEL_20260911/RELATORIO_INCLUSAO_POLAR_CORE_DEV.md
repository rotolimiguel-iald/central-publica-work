# Inclusão polar do core inteiro — DEV

2026-09-12T20:27:33-03:00. [REAL — cinco módulos/28 alvos compilados; revisão e integração pendentes]

No mesmo espaço H_I=ScalarGNSHilbert P do peso escalar,
N=regularCoreAlgebra P, π=scalarGNSRepresentation P, Δ=S†S e
J=scalarTomitaPolarFactor P permanecem os objetos já construídos.

Os operadores de inserção E_S(v)=1_S v, com S mensurável de medida finita, satisfazem
E_S†f=integral_S f. Todas essas leituras juntas determinam f em L².
Seus coeficientes E_S† T E_U determinam cada operador limitado T.
Isso transporta a comutação dos geradores para sua álgebra gerada por
bicomutante na amplificação fibre. A conjugação dualOrbit e a extensão
por zero no complemento ortogonal transportam a geração ao GNS atual.
O lema genérico de restrição exige geração ambiente; essa premissa é
demonstrada na aplicação efetiva scalarGNS_commutation_from_generators.

Combinando a base inteira e os unitários regulares, já cobertos, a
involução do MESMO J e a geração agora demonstrada fornecem:

    [J π(x) J⁻¹, π(y)] = 0, para TODO x∈N e TODO y∈N;
    J π(N) J ⊆ π(N)'.

[REAL] A passagem dos geradores ao core inteiro foi resolvida para a
inclusão acima. Não há troca pelo J da torre, nem hipótese de densidade
ou normalidade restante no enunciado concreto. Não se usa avaliação
pontual de representantes L² ou função constante não integrável na reta.
[OPEN] A inclusão inversa π(N)'⊆Jπ(N)J ainda não foi provada. J²=I
e a inclusão direta não a fornecem automaticamente.
Também permanecem identificação de Δ^it com o fluxo/KMS do mesmo peso,
traço/escala/canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico
interagente e composição/consumo pelos certificados/runtime.
Reutilizar Einstein/Fisher/gauge de Chatgpt com suas hipóteses. Seis flags falsas.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

Integração anterior: 180 registros,
95 controles, 6820 declarações Audit.
Este DEV não altera um.py nem as 34 memórias; atualização pendente de revisão
nesta sessão. Cópia `a350b674810a40693bc9b6fe4be2fc401757a9045747e096621f077b317cfa40`, mãe `ea25a6ecfa766d1c460b32cff1fdba4e86c44cf8381f1ad8a83ccac9603557c0`.
Tentativas Lean recusadas e fontes anteriores foram preservadas; somente
logs rc0 dos bytes atuais são aceitos. Nenhum monólito executado/importado.

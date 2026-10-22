# Revisão da passagem contorção–fonte

17/09/2026. Revisor independente Hypatia, id01a0af27-0ee6-7611-9d10-8757d9d040f0. [DERIVED — parecer escrito, não Lean].

Veredito recebido por ferramenta: “APROVADO no escopo declarado — [DERIVED], identidade geométrica e composição condicional. Não encontrei erro de índices ou sinais. A aprovação não abrange equações de movimento nem realização física da TGL.”

Leu integralmente a nota CONTORCAO_FONTE_E_CARGA_REGIONAL.md, verify_contorsion_source.py e CONTORSION_SOURCE_CHECKS.json; consultou pontualmente Atlas/índice e a proposição1 de https://arxiv.org/pdf/1807.02041. Não auditou as remissões canônicas .tex/um.py. Nenhum script reexecutado, escrita, novo agente ou promoção de gate.

Confirmou a ordem Gamma[r,mu,s], Ric[s,nu]=R[r,s,r,nu], a diferença D e a fonte B=Sym(D)−g tr(D)/2. Confirmou a compatibilidade métrica C[r,mu,s]=−C[s,mu,r] com o primeiro índice abaixado. Confirmou o sinal T_eff=Theta_sym−B/kappa e a contribuição +2pi/kappa integral xi B1 em R1. Exigiu explicitar C0=0: para C0 não nulo há termos cruzados na primeira variação. Essa precisão foi incorporada.

Reconheceu as distinções entre fonte clássica central e inserção operatorial, entre reescrita e equação da conexão, e entre conservação por equação métrica e demonstração independente por Noether. A proposição citada consome equações de matéria e torsão.

O JSON contém83true:40 comparações de Ricci,40 da aplicação linear de simetrização/traço e3 controles. A leitura não autentica sozinha sua execução; a execução pelo autor retornouPASS. A mesma função de traço é usada em ambos os lados do segundo grupo, portanto ele não detectaria coeficiente de traço errado; o −1/2 foi conferido matematicamente. dbase não é um jato geométrico completo simétrico, mas cancela na diferença. O negativo confere somente4Q≠2Q quandoQ≠0. Não há teste deEOM, conservação, integral regional, estado ou não centralidade física. Essas limitações foram acrescentadas à nota.

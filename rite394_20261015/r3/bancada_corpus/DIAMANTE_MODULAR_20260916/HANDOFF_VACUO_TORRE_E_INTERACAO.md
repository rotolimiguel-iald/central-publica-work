# Handoff consolidado — vácuo, dephasing, torre e fornecedor interagente

16/09/2026. Para a sessão responsável pelo `um.py`. Este documento é a porta de encaminhamento atual; preserva os handoffs V2 e de definição conjunta. Não solicita recriar a torre, o canal de reconhecimento, o cociclo ou o gate.

## 1. Resultado que já pode ser consumido

**[KERNEL — evidência histórica auditada na entrega V2, sem nova compilação nesta rodada]** A proposta do operador “vácuo=dephasing” foi concretizada como relações entre estado, canal e ação modular. Não se atribuiu igualdade de tipos a uma densidade e um canal.

Na leitura espectral completa E_K:

\[
E_K(\rho)=\rho,\quad E_K(K)=K,\quad
\sigma_t^\rho(E_KX)=E_KX.
\]

Preservar o vácuo não o seleciona exclusivamente. A imagem dessa leitura é estacionária; uma ação geométrica igual ao fluxo modular nessa imagem também deve ser estacionária ali. Os termos são `spectral_preserves_density`, `spectral_preserves_modular_generator`, `spectral_reading_is_stationary` e, na torre infinita existente, `existing_tower_dephasing_is_stationary`.

**A ponte não trivial construída usa leitura parcial da própria PRODUCT_TOWER.** Seja ρ_{N+1}=ρ_N⊗diag(b₀,b₁), com pesos positivos normalizados da torre. A referência é ρ_ref=ρ_N⊗I₂/2. Seja E_last o pinching que só lê os setores espectrais do último sítio. Para todo X,t,

\[
\boxed{\sigma_t^{\rho_{N+1}}(E_{\rm last}X)
       =\sigma_t^{\rho_{\rm ref}}(E_{\rm last}X).}
\]

O termo `tower_last_site_flow_bridge` aplica essa identidade aos prefixos efetivamente construídos; `tower_last_site_reference_normalized` prova a normalização. Não é um novo objeto com o mesmo nome. Na representação matricial do prefixo,

\[
R=-I\otimes\log(2\,\mathrm{diag}(b_0,b_1))
\]

comuta com toda a imagem de E_last, embora não seja apagado. O fluxo nos sítios anteriores pode permanecer não trivial. Assim, nesta família, a ponte é feita pela **igualdade das ações sobre o conteúdo preservado**, e não por E(R)=0.

Fontes e evidência: [ModularDephasingBridge.lean](ModularDephasingBridge.lean), [TowerDephasingStationary.lean](TowerDephasingStationary.lean), [manifesto V2](HANDOFF_MANIFEST.json) e [handoff V2](HANDOFF_TECNICO_V2.md). O manifesto desta rodada confere os bytes das fontes contra aquele registro; isso não é uma nova execução Lean.

## 2. Critério que os leitores devem conservar

Para K=Q+R, no domínio em que os comutadores estão definidos,

\[
[K,X]=[Q,X]\quad\Longleftrightarrow\quad[R,X]=0.
\]

O termo `generator_bridge_iff` prova a identidade algébrica. Em operadores não limitados, igualdade de geradores só fornece igualdade de fluxos após verificar domínios e integração; o teorema da torre acima já fornece igualdade para todo tempo, sem esse salto.

O contraexemplo `erased_remainder_counterexample` prova que E(R)=0, mesmo com E(X)=X, não basta para [R,X]=0. Não implementar esse critério incorreto como atalho do gate. No centralizador completo, [K,X]=0 implica [R,X]=−[Q,X], não o anulamento automático dos dois termos. Comutar com uma álgebra e pertencer ao seu centro são afirmações distintas quando a pertença não está dada.

## 3. Definição física conjunta já localizada

O operador esclareceu que ação, estado e tensor estão definidos pelo **estudo inteiro**, não por um arquivo isolado. A [definição conjunta](DEFINICAO_CONJUNTA_E_COSTURAS.md) e o [respectivo handoff](HANDOFF_DEFINICAO_CONJUNTA.md) já reúnem:

- ação Einstein–sigma, BV e produtos causais renormalizados069;
- estado físico linear067, domínio Fock/Wick073 e recorrência do estado formal072;
- tensões variacionais, contratermos/RG070, corrente simplética e bordo;
- estado de Araki e dinâmica extensiva da torre nos seus próprios domínios.

Não registrar ausência desses fornecedores nem pedir ao operador outro arquivo único. Também não igualar, sem aplicação demonstrada, a referência parcial tracial da torre à carga regional Q_{ξ,D}. Esta última deve atuar na mesma álgebra e representação do estado físico. No modelo linear regional, o teste já identificado é

\[
kT_tf=\delta_D^{it}kf.
\]

O estudo de pullback Weyl recusou um ansatz de peso escalar comum constante no alcance declarado; não substituiu a ação física completa por esse ansatz. O resto modular e seus coeficientes recebem simultaneamente a variação do estado e a da carga. O número RG155/6 e a taxa de dephasing não são, por identificação nominal, o primeiro coeficiente não central desse resto.

## 4. Avanço adicional verificado nesta rodada

**[DERIVED — prova escrita com revisão independente; não KERNEL]** Foi recuperada a prova contida na string de `write_bv_clock088_new.py`. Seu diretório de saída anunciado não existe nesta leitura; não se atribui ao script execução nem aprovação histórica. Ele não foi executado.

A [nova nota de consumo e prova relativa](PRIMITIVA_RELATIVA_RELOGIOS.md) reaproveita FK=Id de068, desfaz a fixação de gauge de069 e inclui todos os antifields. No aberto físico dos relógios E=(dφ̄,dX̄) inversíveis, a homotopia livre satisfaz

\[
\{s_0,h_0\}=1-\pi,\qquad \{h_0,d_H\}=0,
\]

com π nula no ghost positivo. Se sa+d_Hb=0, a recorrência por valência produz B,C com

\[
\boxed{a^1_4=sB^0_4+d_HC^1_3.}
\]

Não é preciso exigir uma descida completa como hipótese separada nessa localização. A contração e a recorrência conservam o domínio formal explicitado, com finitos jatos em cada coeficiente. A prova não é uma declaração de convergência nem uma execução de normalização causal.

**Costura remanescente precisa:** consumir essa primitiva como uma família admissível de contratermos Q2, com cotas de escala, contatos/EOM, compatibilidade de inserções/aridades e regularidade na categoria pretendida. A presença de inversas de jatos restringe o domínio dos relógios; o teorema não vale automaticamente na classe universal com sigma constante. Fontes externas de ghost positivo, usadas na comparação de fundos, também exigem análise adicional. P2/carga renormalizada, estado interagente e afirmações UV não foram inferidos da cohomologia clássica.

## 5. Alterações solicitadas no motor e na memória

1. **Reusar o consumidor do reconhecimento.** Consultar o pacote [MOTOR_RECONHECIMENTO](../MOTOR_RECONHECIMENTO_20260915/DELIVERY_MANIFEST.json) e o arquivo canônico vivo antes de portar. Em `prove_decision_commutation`, preservar o gerador Γ(E−id) e distinguir os modos `FULL_MODULAR_SPECTRAL` e `LAST_SITE_PRODUCT_READING`. Não duplicar o pinching ou presumir que esta entrega inspecionou novamente a versão viva.
2. **Reusar o cociclo.** Em `prove_cocycle_to_einstein`, manter a convenção já auditada: para a=vácuo e b=referência, h_ab=K_b−K_a e R=−h_ab. Consumir a igualdade de fluxos da família provada; manter a identificação regional física com seu fornecedor e hipóteses próprios.
3. **Transportar evidência, não criar bandeiras afirmativas vazias.** A prova BV relativa deve entrar como DERIVED revisada na documentação/índice. Não criar `QME=True`, `UV_COMPLETE=True` ou uma nova condição de gate a partir dela. Não há novo código numérico nem nova fonte Lean nesta rodada.
4. **Preservar a cadeia já fechada no escopo construído.** Não reabrir PRODUCT_TOWER/JMJ, A1/A2, P0 ou a recorrência já provada por confusão com a identificação física restante. As fontes V2 devem ser incorporadas/recompiladas apenas se a gerência ainda não as consumiu, conferindo o estado atual.
5. **Memória.** Atualizar, com backup imediato de bytes e adendo, Atlas/índice/linhagem/desenho na sessão autorizada a tocar essas superfícies. A bancada atual só atualiza memórias locais e a proposta para o Atlas. A relação “escrito num helper ≠ emitido ≠ compilado” deve ficar explícita para evitar nova duplicação.

## 6. Aceitação e alcance da entrega

O [manifesto desta rodada](CLOCK_RELATIVE_HANDOFF_MANIFEST.json) registra fontes lidas, revisão, conferência de bytes da ponte e backups das memórias. O [parecer](REVISAO_PRIMITIVA_RELATIVA_RELOGIOS.md) delimita o exame matemático independente. O verificador só lê os arquivos; não executar o helper antigo088 para “reproduzir” uma aprovação que não existia.

Não houve edição, importação ou execução do `um.py` original; não foi medido um novo movimento do gate nem uma significância experimental. O avanço demonstrado é: a ponte de ações na leitura parcial da torre está disponível, e a primitiva BRST relativa localizada passa a ter prova escrita revisada. A igualdade com a carga geométrica regional interagente conserva as obrigações acima, em vez de ser afirmada por mudança de nome.

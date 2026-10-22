"""Render a new R4 report from measured synthetic results; never edit evidence."""
from pathlib import Path
import json, hashlib
ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/'RESULT_R4.json').read_text(encoding='utf-8'))
rows=[r for r in d['rows'] if r['n']==11]
table='\n'.join(f"| {100*r['sigma_common_mass_log']:.1f}% | {r['Z_Asimov']:.3f} | {r['ceiling_N_infinite']:.3f} | {r['required_N']['median5'] or 'impossível'} | {r['required_N']['one_sided5_with_90percent_power'] or 'impossível'} |" for r in rows)
text=r'''# Lentes R4 — sinal que sobrevive à escala de massa

19/10/2026. Em nome de codex-gerente-tgl; unidade F8.LENTES_5SIGMA_20261019, reivindicação 1009. **[DERIVED condicional; cenário sintético, não descoberta]**.

## O que foi reaproveitado

R2 já demonstrou degenerescências por trajetória. R3 recuperou a previsão escalar H_lens=K H_bg e a marca OPEN do mapa físico da likelihood. Esta etapa quantifica a informação externa necessária para impedir que uma escala de massa absorva aquele sinal. Não repete o cálculo de distância nem promove o contrato escalar a uma derivação completa do atraso.

A documentação oficial do consumidor TDCOSMO distingue lambda_mst (média/escala), lambda_mst_sigma (dispersão populacional), anisotropia e distâncias. Seu default de dispersão não é a precisão medida da média. Fonte já custodiada: COSMOSIS_TDCOSMO.html, recibo PUBLIC_SOURCE_CUSTODY_R2.json; consulta confirmada em 19/10: https://cosmosis.readthedocs.io/en/latest/reference/standard_library/tdcosmo.html. As larguras usadas abaixo são INPUT de planejamento, não extraídas dessa documentação.

## 1. A imitação por massa é exata no setor de imagens/atrasos

Escreva o potencial de Fermat phi(theta,y)=|theta-y|²/2-psi(theta). Para

    psi_lambda = lambda psi + (1-lambda)|theta|²/2,
    y_lambda = lambda y,

o script verifica simbolicamente em duas dimensões:

    phi_lambda = lambda phi + lambda(lambda-1)|y|²/2.

O termo final é comum a todas as imagens da mesma fonte. Portanto Delta phi_lambda=lambda Delta phi. A escala de atraso pode ser compensada por massa ou distância; isso não prova invariância da cinemática estelar ou de magnificação absoluta calibrada.

Se a previsão escalar for realizada por Ddt_TGL=Ddt_bg/K com Fermat inalterado, uma análise sem esse efeito reproduz os atrasos usando lambda_GR=1/K. Essa realização é uma hipótese explícita: a fonte escalar fixa um produto, não determina qual fator físico o realiza. Pelo mesmo motivo não atribuímos essa lambda a uma lente observada.

    lambda_GR = @LAMBDA@

Trata-se de uma transformação da distribuição de massa/folha, não de afirmar que a massa total de toda lente esteja errada por essa porcentagem.

## 2. Perfil conjunto, com calibrações independentes

Modelo de planejamento gaussiano no logaritmo:

    y_i = a logK + h - m_comum - m_i + e_i.

a=1 identifica a hipótese escalar TGL; a=0, o comparador. h é a variação do fundo, m_comum a escala comum da folha de massa, m_i a variação individual, e_i o erro de atraso/modelagem restante. As calibrações externas de h e m são dados auxiliares gaussianos centrados em zero neste cenário Asimov. Sob o comparador, todos são perfilados, não fixados silenciosamente.

Para N sistemas iguais e erros independentes antes do componente comum:

    Z_A = logK / sqrt[(sigma_e²+sigma_ind²)/N + sigma_comum²+sigma_bg²].

Aqui logK=@LOGK@, sigma_bg=0,301/68,531; K vem de alpha*sqrt(e) e dos parâmetros pinados, calculado em runtime. Há dois testes da fórmula: solução analítica de covariância e mínimos quadrados explícitos de todos os nuisances. Diferença máxima em chi²: @ERROR@.

Controles negativos: sem calibração da massa comum, Z=0; sem calibração do fundo, Z=0. Isso demonstra a identificabilidade condicional do cenário, sem fornecer a calibração física ausente.

## 3. Quanto é necessário

Escolhas INPUT: erro log de atraso/modelagem 4% e dispersão independente da massa 3%, combinados em 5% por sistema. Percentuais abaixo significam desvios padrão no logaritmo (aproximadamente frações para erros pequenos). Não se usou a barra publicada de H0 como erro cru de atraso, evitando somar duas vezes a incerteza de massa já marginalizada.

| Calibração comum | Z previsto para 11 sistemas | Teto quando N cresce | N para mediana 5 | N para 90% de poder a 5 unilateral |
|---|---:|---:|---:|---:|
@TABLE@

O exemplo com 11 sistemas não descreve as 11 lentes publicadas: mesmos N não significam mesmas precisões, independência ou hipóteses. Nenhum dado foi ajustado.

O piso comum máximo para sequer permitir mediana 5, com o fundo adotado, é **@COMMON@%** no log. Com erro independente da média de 1%, ele cai a **@MEAN@%**. Um piso comum de 2% impede mediana 5 neste modelo, por maior que seja N. Isso mostra por que aumentar amostra sem calibrar a massa comum pode não resolver.

Para 90% de probabilidade de ultrapassar o limiar unilateral 5, usamos a separação média 5+Phi^-1(0,9), não 5. Essa conta pressupõe teste gaussiano único com sinal previsto, variância conhecida, K fixo e nenhuma seleção adicional. Não é poder do pipeline TDCOSMO real.

R3 usou erros gaussianos no H0 linear; R4 usa erros gaussianos no log e decompõe componentes sintéticos. São modelos distintos de planejamento: não substituir um resultado pelo outro nem somá-los. Incerteza de K e covariâncias reais ainda precisam do modelo físico conjunto.

## 4. Positivo e negativo: critério e informação

A formulação do operador orienta um contraste entre correspondência e exclusão. O controle numérico tomou uma observação y e o seu negativo calculado -y. A covariância conjunta é [[C,-C],[-C,C]], singular. Com sua pseudoinversa correta, o chi² permanece @CHI@ e o posto permanece 11, embora haja 22 entradas. Tratar as metades como independentes fabricaria informação.

Uma leitura complementar pode ajudar quando traz um vínculo observacional adicional: por exemplo, cinemática resolvida ou magnificação absoluta calibrada. Ela não precisa ser estatisticamente independente; sua covariância deve entrar. A identificação entre esses observáveis e os mesmos potenciais da TGL precisa ser derivada ou assumida explicitamente.

## 5. O que ainda falta para um discriminante físico

Precisamos da lei conjunta que determina o potencial lido pelos fótons, o potencial lido pelas estrelas, o relógio e a geometria. O produto escalar sozinho admite realizações distintas. Impor uma massa de GR como verdade externa enquanto se testa um efeito que também altera essa massa pode apagar ou fabricar o sinal.

A busca específica desta etapa examina a relação entre os potenciais e a cinemática nos artigos existentes. Um resultado ausente no recorte é OPEN, não prova de ausência em todo o acervo. A próxima ação deve depender desse levantamento, sem nova pergunta abstrata sobre identidade e sem escolher parâmetros para alcançar 5.

Plano, script, saída e recibo: PLAN_R4.json, profile_mass_calibration.py, RESULT_R4.json e RUN_R4.json. Revisão independente tem recibo separado. Nenhum kernel, um.py, Bancada, dado observado ou gate foi alterado.
'''
subs={'@LAMBDA@':f"{d['lambda_GR_imitation_for_true_lambda1']:.15g}",'@LOGK@':f"{d['logK']:.15g}",'@ERROR@':f"{d['profile_max_absolute_error']:.3g}",'@TABLE@':table,'@COMMON@':f"{100*d['common_mass_sigma_max_infinite_N_for_median5']:.4f}",'@MEAN@':f"{100*d['common_mass_sigma_max_with_1percent_independent_mean_for_median5']:.4f}",'@CHI@':f"{d['negative_copy_control']['chi2_original']:.10f}"}
for a,b in subs.items(): text=text.replace(a,b)
with (ROOT/'RESULTADO_CALIBRACAO_R4.md').open('x',encoding='utf-8') as f:f.write(text)
print(hashlib.sha256((ROOT/'RESULTADO_CALIBRACAO_R4.md').read_bytes()).hexdigest())

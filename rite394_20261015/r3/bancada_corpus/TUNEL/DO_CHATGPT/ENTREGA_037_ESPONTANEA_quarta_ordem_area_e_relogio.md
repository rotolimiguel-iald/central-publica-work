[REAL] Limites entrópicos e de área óptica em quarta ordem, critério condicional de compatibilidade e controle do relógio relativo. [OPEN] Reconstrução gravitacional geral, identificação da leitura angular com área física e estabilização.

# Entrega espontânea 037 — quarta ordem, área e relógio

06/09/2026. Continuação da ordem007, com verificação conforme ordem008.

O lote final reúne 65 teoremas e 10 definições em seis módulos, mais Imports037All: sete compilações exit 0, sem erros, avisos ou sorryAx. As 75 declarações têm impressão de axiomas; somente propext, Classical.choice e Quot.sound aparecem. Nenhuma instância nova foi declarada.

O cálculo usa os estados globais existentes e a área induzida da tela de Jacobi construída na036. Obtém D(t)/t⁴→(9/4)B2 e (S(t)+log2 B t²)/t⁴→C=log2 B-(9/4)B2. O coeficiente óptico é r²/12-s²/6, com |s|<r/2. Para r=2log2 B/eta, o defeito é delta4=C-eta(r²/12-s²/6).

Para eta>0 e0<B<=eta, prova-se delta4>=(7/48)B>0: falha o casamento ADICIONAL em quarta ordem com o parâmetro comum fixado. Isso não contradiz a H3 quadrática anterior. Alterar somente o parâmetro dos estados por t+lambda t³, com lambda=delta4/(2log2 B), cancela o defeito até quarta ordem. A reparametrização comum dos dois lados por esse relógio cúbico preserva delta4. Há testemunha não vazia para todo eta>0.

## Critérios e estatuto

| Critério | Resultado nesta entrega |
|---|---|
| Ordem007-A — expectativa global/período comum | Sem nova quitação; não se ampliam as conclusões das entregas anteriores. |
| Ordem007-B — cauda e obstruções | Sem nova quitação; nenhuma conclusão geral acrescentada. |
| Ordem007-C — assinatura/reconstrução gravitacional | NÃO PAGO no sentido geral. O resultado usa a família óptica lorentziana já fornecida como INPUT. |
| Ordem008 — instâncias nomeadas, lote limpo e integração | PAGO neste lote: zero instâncias novas, seis fontes exatos e Imports037All. |
| Cálculo de quarta ordem dos estados e da área construída | PAGO no escopo e filtros explicitados nos enunciados. |
| Identificação física da inscrição angular e retorno estabilizador | NÃO PAGO; OPEN. |

O parecer inclui um controle analítico [DERIVED, não Lean037] que distingue omega(F), sqrt(omega(F)), omega(sqrt(F)) e a norma de sqrt(F). Ter a mesma ordem inicial do déficit de área não identifica essas leituras. Não confundir a leitura escalar psi_t(L(t)) com L(t)² ou com F.

A revisão independente pré-selo executou inspect_build() e conferiu separadamente os sete logs, fontes, cobertura de axiomas, hashes, proveniência e imports: PASS. A incorporação pela gerência ainda não foi verificada. Nenhum gate foi alterado.

## Artefatos e hashes medidos

| Fonte | Teoremas | Defs | SHA256 |
|---|---:|---:|---|
| [QuarticClockTransport.lean](<C:/IALD/Central de Patentes/Chatgpt/QuarticClockTransport.lean>) | 17 | 1 | 32d8de43c8907740e00edcceacf1d644a750d21d65c80707e7c9103deac794fc |
| [BinaryRelativeQuartic.lean](<C:/IALD/Central de Patentes/Chatgpt/BinaryRelativeQuartic.lean>) | 12 | 2 | be583d787868a0e6a096316a01a165e5eec9c31a81fd1082d90fb6069df22adb |
| [SummableRelativeQuartic.lean](<C:/IALD/Central de Patentes/Chatgpt/SummableRelativeQuartic.lean>) | 6 | 0 | 35ac6c46d08158057d33eeb9a851fb57df4fa30fd1d2e26639852b22620cf48f |
| [JacobiAreaQuarticLimit.lean](<C:/IALD/Central de Patentes/Chatgpt/JacobiAreaQuarticLimit.lean>) | 5 | 0 | 81161152093243ca0f4aaca35e27790b79d27cd5e685ce22e97b9da700ea1350 |
| [FourthOrderMatchingControls.lean](<C:/IALD/Central de Patentes/Chatgpt/FourthOrderMatchingControls.lean>) | 11 | 4 | 41ffce309f691e100d899ff04e419657b32381728874ee7b72d9b7e2027b785c |
| [QuarticMatchingClockControls.lean](<C:/IALD/Central de Patentes/Chatgpt/QuarticMatchingClockControls.lean>) | 14 | 3 | e809534bf7c2d9ba706fab2abe16a4eef80f2455634e52180a2d2f7c1c877248 |

- [CONTINUACAO037_PARECER.md](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO037_PARECER.md>): SHA256 b02090e552c9cc5e0eead6ba3a512e5a6d4f2f7efadf4567f296e7c682e39e3b.
- [CONTINUACAO037_CLEAN_BUILD.json](<C:/IALD/Central de Patentes/Chatgpt/CONTINUACAO037_CLEAN_BUILD.json>): SHA256 c43c17be3389fece181b8d85f3591f0ae306fa4527b68f519dc4ad626ea77ac2.
- [clean_continuation037.py](<C:/IALD/Central de Patentes/Chatgpt/clean_continuation037.py>): SHA256 eb2bc5b47ed42d968510c412673ae89d2de713c9d441dfb229506b75da10aa41.
- [audit_continuation037.py](<C:/IALD/Central de Patentes/Chatgpt/audit_continuation037.py>): SHA256 15bbc036628d3c492e6996ad1b0847e12496e0fc5e91b246fe599ec46a44784f.

## Reprodução

Auditoria somente leitura do manifesto final:

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation037.py'
```

Recompilação integral em outra pasta limpa, preservando o selo existente:

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\clean_continuation037.py' --development 6
```

Esse comando refaz os seis módulos e Imports037All, gerando marcador separado de desenvolvimento. A versão final selada continua identificada por CONTINUACAO037_MANIFESTO.json.

## Custódia e limites

As fontes/binários036 vêm do clean build036 pinado, sem fallback para oleans de raiz. As demais fronteiras históricas são pinadas pelos manifestos029/032/033/034/036, mas não recompiladas neste lote; fontes canônicas externas sem pin histórico de fonte ficam declaradas como leitura atual para descoberta de imports.

Todas as tentativas rejeitadas e os backups de bytes foram preservados. As correções foram de elaboração/normalização/táticas; os enunciados não tiveram suas hipóteses enfraquecidas.

Originais, um.py, kernel, Atlas, memórias, selos, gates e entregas anteriores permanecem somente leitura. Tudo novo está sob Chatgpt. Não há aqui prova de gravidade quântica geral, escolha física do relógio, igualdade funcional entropia-área ou lei de estabilização. O cálculo quártico não inclui corte móvel arbitrário centrado pela massa global.

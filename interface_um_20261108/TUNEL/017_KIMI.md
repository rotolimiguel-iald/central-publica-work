# Kimi → Codex · sessão real e um_py.exe (etapa verificada)
1. A sessão IALD agora usa pacote Ed25519 com escopo `iald.chat.local`, evidência v409, emissor local, expiração de 15 minutos, revogação e invalidação se o resultado mudar.
2. A conversa usa o adaptador MiMo 2.6 Pro já autorizado, sem expor credenciais; a primeira resposta medida custou estimativamente US$ 0,00066729, e respostas parciais/contraditórias são recusadas.
3. Interface e API responderam de fato pelo provedor, com estatuto `PROVIDER_COMPLETED_NOT_FACT_CHECKED`; captura `verification/17-iald-local-session.png`.
4. Sessão: **13/13**, cobrindo assinatura, escopo, expiração no limite, pacote alterado, origem externa, revogação e resposta real pela interface; `verification/session-results.json`.
5. `release/um_py.exe` foi construído com Node embutido, interface, ponte, domínios e os quatro artefatos v409; não exige Node instalado nem modifica o motor original.
6. Executável: 152.182.233 bytes, SHA-256 `bcab9cd9be678ec732e08b82f86f3aae3af20fba54439fad40d9403443c88eb7`.
7. O host copia os artefatos para a pasta por usuário e usa essa cópia para futuras execuções; credenciais não são embutidas.
8. Verificação nativa: **10/10**, com ponte, artefatos, imagens, amostra ACOM, sessão/revogação e três domínios com 16 imagens no navegador; `verification/native-results.json` e `18-native-domains.png`.
9. A correção `webRoot` fez as quatro figuras PNG funcionarem também no pacote; a sondagem ACOM offline ficou classificada como indisponibilidade prevista, não como erro.
10. Regressão completa: **78/78**, incluindo domínios, imagens, ACOM, PT/EN/AR, mobile e a jornada 011; `verification/results.json`.
11. Evidência consolidada: `verification/NATIVE_DELIVERY.json` e recibo no túnel.
12. Limite desta etapa: a execução científica completa ainda não foi disparada; o próximo passo é iniciar pelo próprio programa, acompanhar eventos reais e reconferir os artefatos finais antes de encerrar o objetivo.

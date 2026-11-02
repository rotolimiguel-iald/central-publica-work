# Ordem da gerência c1 ao agente claude-prep-v405 (01/11/2026, por volta de 17:18, verbatim do que chegou)

Segure o próximo build do kernel: o operador mandou revisitar a Lei do Diminuto e `LeiDoDiminuto.lean` e `TonicaDoHamiltoniano.lean` vão mudar de novo (errata R3, com um import novo e cerca de uma dúzia de teoremas; nota comum nas outras). Continue só o que não depende de pino nem de kernel: textos, guardas e a exclusão da fala. Eu aviso quando a R3 estiver nas origens, com recibo. Não rode pino, kernel nem candidato antes disso.

## O que o agente fez ao receber (registro, não ordem)

- A regeneração `refazer_candidato_v405.sh --regerar`, lançada às 17:13 (antes da ordem), estava no ensaio a seco: parada por PID exato (três processos criados por ela, conferidos pela linha de comando), nada por nome. `refazer_out_v405.txt` traz a nota da interrupção e não vale como regeneração limpa.
- O kernel de 17:09 (R2, 301 bandeiras) e o candidato de 17:14 são da R2 e ficam superados quando a R3 chegar.

## Ordem seguinte da gerência (01/11/2026, por volta de 18:31, verbatim do que chegou)

Segure de novo pino, kernel e candidato: o operador acabou de responder e a semântica da Lei do Diminuto muda (o diminuto modula só a tônica e sustenta as outras notas). Haverá errata R4 em `LeiDoDiminuto` e talvez em outras pedras. Continue só textos que não dependam disso, guardas e a exclusão da fala. Se um build já estiver rodando, deixe terminar e não encadeie o seguinte. Aviso quando a R4 estiver nas origens.

VINCULO R3.3 — 13/10

# Errata ao lado da §5 do `RESULTADO_R3_2.md` (R3.3, F0.6, gerência c1)

O `RESULTADO_R3_2.md` fica como registro, sem edição. Esta errata vem do relatório da reauditoria final da R3.2, `C:\IALD\PROGRAMA_IALD\auditorias\F0.6\AUDITORIA_F0_6_C1_a70d70d5.md` (APROVA_COM_RESSALVAS; os achados R32-A e R32-B, BAIXOS, estão fechados na R3.3). Estatutos: [REAL] = medido pelo auditor ou aqui por script; [DERIVED] = lido do código.

> ⚠ **R3.3, ao lado (13/10/2026). A §5 da R3.2 fica como registro; valem estas correções.**

## 1. O site do sistema executa também com `-I`

A §5 da R3.2 diz, no resíduo «Chamada errada», que o site do sistema e o `usercustomize`/`.pth` do `APPDATA` executam **sem** `-I`. Isso está incompleto.

- O `-I` corta o site do usuário (`-s`), o `PYTHONPATH` e a pasta do esboço no `sys.path` (`-P`). **Não corta o site do SISTEMA**: `sitecustomize.py` e `.pth` de `Lib\site-packages` executam no processo do esboço também com `python -I -B -X utf8` [REAL, medido pelo auditor num venv em cópia].
- O recibo lista esses arquivos com sha256 no isolamento dos testes. O site do sistema é a instalação do Python, não um vizinho do esboço: quem o altera já controla o interpretador.
- Resíduo declarado, sem conserto no esboço. A defesa é a cadeia chamar o Python instalado e conferido.

## 2. Os bytes de uma 2ª gravação alheia não ficam em `--saida`

A §5 diz «os bytes dela ficam só em `--saida`» para a gravação alheia que o rollback sobrescreve. Vale só para a **primeira** gravação alheia, a que o esboço detecta e copia para `MANIFESTO_ESTRANHO_APOS_A_TROCA_B{n}_*.json` antes do rollback.

- Uma **segunda** gravação alheia, entre a leitura do estranho e a troca do rollback, é sobrescrita sem cópia. O recibo registra o sha da primeira, não o da segunda [REAL, caso F2 do auditor].
- Uma gravação alheia **depois** do `os.replace` do rollback (caso F3, ROLLBACK_DIVERGE) não é sobrescrita: o manifesto em disco fica nos bytes alheios. Na R3.3 o recibo traz o sha deles (`aplicacao_revertida.manifesto_em_disco_sha256`), mas os bytes só estão no disco da Bancada, não em `--saida`.
- Depois da 2ª releitura que passa (caso F1), nada mais é visível ao esboço; o 10-ter segue sendo a última prova.

## 3. O `-i` agora é recusado (R32-A)

- **O que a R3.2 não dizia.** A guarda recusava `-s` ou `-B` ausentes, mas não o `-i`. Com `python -I -B -X utf8 -i` o `PYTHONSTARTUP` herdado executava no processo do esboço **depois** do `main()`, e o processo ficava no REPL [REAL, reproduzido pelo auditor em CPython 3.14.3, com stdin no NUL].
- **O que a R3.3 faz.** `_flags_que_faltam()` passa a recusar `sys.flags.inspect` e `sys.flags.interactive` (`INTERPRETADOR_NAO_ISOLADO: … sem -i …`), no topo (antes de qualquer import além de `sys`) e de novo em `main()`. Na recusa por `-i`, o esboço sai por `os._exit(2)`, o `os` que o próprio interpretador já carregou: um `SystemExit` ainda entraria no REPL e rodaria o startup [REAL, medido aqui: com `SystemExit`, o processo ficou preso; com `os._exit`, rc 2 em seguida].
- **O recibo** passa a gravar `python_isolado.orig_argv` (`sys.orig_argv`), `inspect` e `interactive`. O `-c` com `sys.flags` falseado (código hostil antes da guarda) segue resíduo declarado: o recibo agora mostra a linha de comando real.

## 4. ROLLBACK_DIVERGE deixava a Bancada pela metade (R32-B)

Na R3.2, se o manifesto mudava logo depois do `os.replace` do rollback, a recusa `ROLLBACK_DIVERGE` era visível (rc 2, com recibo), mas o `CONTRATO_CANONICO_B{n}.md` ficava na Bancada, a sonda pós-rollback não rodava e o recibo não trazia o sha do disco. Na R3.3:

- o contrato gravado é retirado antes de a recusa subir;
- o `pos_rollback` roda também depois de `ROLLBACK_DIVERGE` (a sonda do serviço entra no recibo como `apos_rollback`);
- o recibo grava `aplicacao_revertida.manifesto_em_disco_sha256`, o sha do manifesto que está no disco (os bytes alheios, não o anterior);
- se o serviço responde, o código é `SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO` e o texto diz «bytes alheios, nao o anterior».

O manifesto em disco **não** volta sozinho ao anterior nesse caminho: quem escreveu por cima é alheio ao esboço. O operador decide, com o 10-ter (religamento com recibo de identidade).

## 5. O que não mudou

- Os resíduos da §5 da R3.2 que não aparecem acima seguem como estão: o código hostil antes da guarda, o selo v391 na custódia [OPEN], os tokens (o B(n) confere a extensão da varredura, não os tokens), e os itens não medidos.
- Nada move o gate. NOT_FALSIFIED nunca é creditação. Não houve dado observado.

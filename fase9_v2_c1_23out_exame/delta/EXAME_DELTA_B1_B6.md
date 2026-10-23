# 2ª e última rodada — o delta das BAIXAS B1–B6 da V2-c1 (gerência c1, modelo forte, 23/10/2026)

Não abri o dado observado.
- Comparei o pacote corrigido com o meu instantâneo anterior (`..\copia_pacote`). Os 24 `.bak_20261023_121040` são iguais ao instantâneo, byte a byte, salvo o `RESULTADO_TESTES.json` que eu mesmo regravei.
- Os testes e as sondas rodaram numa cópia nova (`copia_pacote_B`). O original segue intocado: a consistência dá OK e não há `__pycache__`.

## VEREDITO: PODE_CONGELAR

**(1) O diff é só o declarado** [REAL].
- **Spec** (arquivo `e7c47cbcbbcd3a7a`; canônico `db1ccecbc1718e69`): mudam 23 folhas, todas de texto. São o R0b da abertura única, as chaves de B3/B4/B5/B6 no `runner_contract`, as 4 recusas novas na trava, a régua sem a palavra e o `python -B`.
  - Nenhuma folha numérica muda.
  - `lei`, `covariancia`, `fundos`, `leitores` e `gate` ficam iguais.
- **Função** `af960b7405732d62`: muda só a docstring. O AST é igual ao da R5.2, salvo nome, docstring e base; as constantes são as mesmas.
- **Recibo de calibração:** só mudam os sha dos módulos, o sha da spec e a data. O z_δ de 5σ segue **6,3705** (caixa).
- **Fontes, registro D-H e pinos da Bancada:** iguais.
- **`build_registro_dh.py`:** mudou só o `-B` da docstring, sem `.bak`. É ferramenta, não byte pinado.

**(2) A abertura única funciona** [REAL; `sonda_abertura_unica.py` em pacote sintético, medida por `builtins.open` e `os.open`].
- O marcador nasce por O_EXCL **antes** da 1ª das 8 aberturas de fonte.
- A 2ª abertura dá `REFUSE__ALREADY_OPENED` e grava registro de recusa.
- Uma recusa antes do marcador (sem abertura) não cria marcador.
- B1 virou asserção real; B3, B5 e B6 recusam (testes E24, E25, E26).

**(3)** Na cópia: **55/55 em 42,4 s**.

## Resíduo BAIXO (não bloqueia)

**B7.** O marcador nasce antes de checagens que não leem fonte: E1/E2 do fundo, α, S5, guarda da calibração e pino do poder. Uma falha de ambiente depois do marcador consome a única abertura.
- Medi: com o fundo divergente, a recusa grava o registro, e a retentativa com o fundo certo dá `ALREADY_OPENED`.
- É fail-closed e fica registrado; o remédio é um ato registrado da gerência.
- Sugestão (opcional): mover essas checagens para antes do marcador, que passaria a nascer imediatamente antes de `read_sources`.

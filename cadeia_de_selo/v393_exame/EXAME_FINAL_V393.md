# EXAME FINAL ANTES DO SELO — cadeia v393 (gerência c1, modelo forte, 14/10/2026)

Objeto: o candidato `um_v393_candidato.py`, sha16 `18be2ddb06c60f90` (relido); o `um.py` do Nós é a v392 `b590c0aa80055e2a` (relido). Escrevi só nesta pasta. Nada foi instalado; nenhum rito nem selo rodou.

## VEREDITO: PODE_INSTALAR_E_RODAR

Não há bloqueante. As ressalvas abaixo são BAIXAS e nenhuma impede instalar ou rodar.

## 1. Toolchain: NÃO bloqueante [REAL]

- O `lean-toolchain` diz `leanprover/lean4:v4.31.0` no Nós, em `C:\t\k393\final` e em `C:\t\k393\arvore`.
- Li o cabeçalho de TODOS os 9.775 `.olean` de `C:\t\k393\final\.lake`. Todos trazem a versão `4.31.0` e o githash `68218e876d2a38b1985b8590fff244a83c321783`, que é o do toolchain 4.31.0 (o do 4.35.0 é `eb6cafb7…`). Isso inclui as 3 pedras novas.
- O Audit (`lake env lean`) deu rc 0 sobre esses `.olean`. Um Lean de outra versão recusaria o cabeçalho, logo o Audit rodou com 4.31.0.
- `~/.elan/toolchains/leanprover--lean4---v4.35.0` foi criado em 14/10 às 16:38:49, efeito colateral de um `lake --version` fora de projeto (`default_toolchain = "stable"`). Não afeta o kernel.
- No rito, o `um.py` chama `lake --version`, `lake env lean --version`, `lake build` e `lake env lean TGL/Audit.lean`, todos com `cwd = Nós\tgl_kernel` (lean-toolchain 4.31.0). Logo o rito usa 4.31.0. O core v392 registra `Lean (version 4.31.0 … 68218e8…)`.
- Recomendação BAIXA: depois do rito, conferir que `core.kernel_formalization.lean_version` contém `4.31.0`. O `conferir_rito_v393.py` não confere esse campo.

## 2. KH_N1_v392.json: re-pino e pisos LEGÍTIMOS; a errata deve dizer a causa certa

**Quem e quando [REAL].** Foi a sessão pós-selo da v392, em 13/10.
1. Às 18:30, `refazer_sandbox_v392.sh` falhou (`refazer_sandbox_v392.out`: «o ANTES gravado nao e' o que o Nos tem agora»). Ficou em `C:\t\k392\final\TGL\Audit.lean` o Audit da v391 (`e7826e02…` = `Audit.lean.ANTES_v392`, com 8.532 `#print`); o do Nós é `ad4f4c87…`, com 9.270.
2. Às 18:33, `pos_build_kernel_v392.py` foi editado (correção ctorIdx e `V392_KEEP_ARV`; backup `.bak_20261013_ctoridx`).
3. Às 18:34:16 ele foi re-rodado. O script particiona o log pelo Audit do `final`; com o Audit errado, o corte caiu em 8.532 e as entradas novas da v392 foram parar na parte KH. Resultado: `novas_de_usuario_no_trio=false` e `entradas_print_axioms_usuario=8532`.
4. O `pos_build` grava com `open("w")` sem backup, então os 1.389 B originais (`104377ce…`) se perderam. O `KERNEL_RECIBO_v392` também foi regravado às 18:35 (existe um `.regen_falhado_pos_selo`).

**Não há regressão do kernel.** É uma medida feita com o sandbox trocado. As contagens 24975/19761 do arquivo regravado são as mesmas de antes.

**Os pisos são legítimos.**
- As checagens k2/k3 do `kh_n1_cobertura_v392` leem o `kf` do PRÓPRIO rito, não o arquivo. Com as pedras da regra a cobertura passa a 25161/19901, então `igual 24975` reprovaria por construção.
- A igualdade exata 25161/19901 passa a ser cobrada pelo `kh_n1_cobertura_v393` (h2/h3), logo o piso não esconde nada.
- As únicas checagens da v392 que leem a fonte são k12 (duração) e k13 (sorryAx), e nenhuma usa o campo corrompido.

**O que fazer (BAIXA, só texto; quem faz: a gerência ou o preparador).**
- A errata em `registros_v393.py` diz «novas… ficou false nessa regravacao». Ela deve dizer a causa: o sandbox tinha o Audit da v391, e a partição se deslocou. Do jeito que está, a cópia pinada guarda uma medida errada como fonte.
- Corrigir no código muda o sha e obriga a refazer candidato, ensaio, esperados e conferidor. A alternativa que não mexe no sha é registrar a causa ao lado, no pós-rito.
- Não re-rodar `pos_build_kernel_v393.py` depois do selo. A v393 pina a cópia de `insumos\`, não a de `kernel\`.

## 3. Derivados: conferidos linha a linha contra a v392

- **`instalar_v393.py`.** Em relação à v392 mudam só o comentário e a pré-condição (Verdade e Posto presentes; as 3 pedras ausentes).
  - Faz backup de BYTES de 8 arquivos e os relê.
  - Copia o pilar e o confere.
  - Grava em temporário, confere, e só então faz `os.replace`; registra `APLICADO_*.json`.
  - No Nós, grava apenas o `um.py` e os 8 `.bak_<ts>`.
- **`reverter_v393.py`.**
  - Lê o último `APLICADO_*` e exige os 8 alvos.
  - Confere cada backup por sha16 ANTES de qualquer escrita, depois restaura os 8.
  - Põe em quarentena as 3 pedras de `ESPERADOS.pedras_sha256` e exige que o `um.py` volte a ser `b590c0aa80055e2a`.
  - Cobre tudo o que o instalar grava. O rito também gera `.lake`, PDF e stdout, que o reverter não limpa; o molde da v392 faz igual, e isso foi aceito.
- **`rito_v393.sh`.** Mudam só os comentários e a lista de guardas (`cadeia_de_selo/v392`, que não tem marcador `.servidor_parado_pelo_rito`). O pilar usa a mesma chave `75dc30bc9cc8d330e31f99ca`, e o resultado está na cache.
- **`pos_rito\chain_pos_rito_v393.sh`.**
  - Tem o B(n): passos 10, 10a, 10b e 10c. O recibo do kernel é conferido contra o pino.
  - O `fechar_v393.py` usa os mesmos nomes de campo da v392: `pid`, `porta`, `porta_fechada`, `hora`; `versao_servida`, `manifesto_sha256`.
  - Refaz a árvore com `refazer_arvore_v393_pos_selo.py`, idêntico ao da v392 a menos da versão. A árvore `C:\t\k393\arvore` existe.
- BAIXA: `fechar_v393.py` (l.74, 76 e 146) rotula o backup e o temporário com `_f392`; devia ser `_f393`. Não há colisão, porque o nome leva carimbo de hora; o erro é só o rótulo.
- Já declarado no ESTADO: o passo 10 PARA em AGUARDA_OPERADOR, porque `PINOS_BN_v393.json` não tem `recibo_pre_selo`. A bateria e o esboço são os da v392. Isso não impede instalar nem rodar.

## 4. Diff do candidato contra o Nós v392 [REAL, `diff_v392_v393.txt`]

- São 24 blocos: 10 linhas trocadas e 1.838 acrescentadas.
- As linhas trocadas são: `UM_VERSION`; a raiz e o Audit embutidos; os 2 conjuntos do índice; k2/k3, que viram pisos; e a escada de `pedras_v392`, que vira piso.
- Todo o resto é aditivo: as pedras, as 144 bandeiras, o runtime, a chamada no main, o artigo, o quadro e o selo.
- Nas linhas novas:
  - nenhum literal de β, α ou √e;
  - nenhuma ocorrência da palavra proibida (conferi também os `.pysnip` e o `pos_rito`);
  - nenhum toque em `qg_closure_verdict` nem nas bandeiras do gate;
  - nenhuma atribuição `core[...]` fora das 5 chaves novas.
- `SEALED_CODATA_ALPHA` (l.95) vale `7.2973525693e-3`, o mesmo valor de `ALPHA_FINE_CODATA_2018`. A l.5584, onde está `ALPHA_FINE_CODATA_2018`, fica dentro de uma string embutida. Usar `SEALED_CODATA_ALPHA` é CORRETO: β = esse α × √e, calculado em runtime.

## 5. Pontos de chamada re-executados por mim

Processo isolado: `exame_pontos.py`, com saída em `EXAME_PONTOS_v393.json`.

- **`verify_tgl_kernel_formalization`** com os logs crus do sandbox: `TGL_KERNEL_STAGE1_VERIFIED…`, `all_verified` True.
  - Cobertura ok: 25161/19901/0, com 25157 lidas e 4 não lidas.
  - 7082/7082 bandeiras `ext_` True; 144/144 das novas True; `formal_release_ready` True.
- **`prove_external_ladder`**: 7045/7045.
- **Sobre o core v392 do Nós com esse kf**, todos dão True:
  - `prove_the_iald_index` (0 falhas);
  - `three_stress_tests_v387`;
  - `estatuto_da_prova_v391` (KERNEL_7045…25157);
  - `pedras_v392`;
  - `varredura_e_sorry_v392` (1209, igual ao ESPERADOS);
  - os registros v392 (nenhum fica fora do verde);
  - `pedras_v393`;
  - `regra_consumidor_v393` (78 checks, 241 pontos);
  - o coração (`FORM_VERIFIED_CHI_FROM_CODATA…`);
  - `cunhagens_regra_v393`;
  - `kh_n1_cobertura_v393` e `kh_n1_cobertura_v392`.
- `regra_v393` e `_v393_rodar_specs` não alteram nenhuma chave existente; só criam as 5 novas. As chaves de gate ficam iguais.
- As contagens fixas embutidas (7045, 25161, 25157, 19901, 144) batem com a medida.
- Nenhum caminho embutido aponta para `C:\t`. Os caminhos fora do Nós ficam em `cadeia_de_selo\v393\insumos` e `\pedras`, que são permanentes.
- BAIXA: o veredito de `kh_n1_cobertura_v392` continua dizendo «CLOSURE_24975_CONSTANTS». Lido como piso, continua verdadeiro, e esse veredito da v392 está na lista do que não pode mudar.

## Comandos aprovados (os do ESTADO §5, sem mudança)

1. `cd "C:\IALD\Central de Patentes\work\cadeia_de_selo\v393"` e depois `V393_JA_PREPARADO=1 python -I -B -X utf8 p00_precondicoes.py`. Tem de dar TODAS PASSARAM.
2. `python -B -X utf8 instalar_v393.py`
3. No Git Bash: `cd /c/IALD/Central\ de\ Patentes/work/cadeia_de_selo/v393 && sh ./rito_v393.sh > rito_v393_lancador.out 2>&1 &`
4. `python -I -B -X utf8 conferir_rito_v393.py`, que tem de dar TUDO BATE. Conferir também `lean_version` 4.31.0 no core.
5. Se o rito falhar: `python -I -B -X utf8 reverter_v393.py`
6. Pós-rito: `cd .../v393/pos_rito && sh ./chain_pos_rito_v393.sh > chain_v393_out.txt 2>&1`. A cadeia para no passo 10 até que se pine o `recibo_pre_selo`.

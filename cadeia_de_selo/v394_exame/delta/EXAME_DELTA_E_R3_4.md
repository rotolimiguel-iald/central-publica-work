# REVISÃO ÚNICA — delta 19/10 (candidato final) e R3.4 do B(n) (gerência c1, modelo forte, 19/10/2026)

Objeto A: `v394\um_v394_candidato_d19.py`, sha256 `972e81f22dd8cc68bd5671fa610d2664e26f4681ab52932e001e5ef97e8f5991`, 37.885.889 B (relido). Base de comparação: `4022ad521dc7293d`, já examinado. Kernel: `C:\t\k394d\final`; logs em `v394\kernel`.

Objeto B: `work\bancada_vinculo_12out\R3_4`, esboço `12d504a1114f9f9c`.

Escrevi só nesta pasta. Nada foi instalado. Nenhum rito, selo, `lake` ou B(n) rodou. O Nós, a Bancada, o túnel e as cadeias foram só lidos.

## VEREDITO: PODE_INSTALAR (candidato `972e81f22dd8cc68`). O B(n) pós-selo fica PODE_COM_CORRECOES: três itens, antes do passo 10 do pós-rito.

## A. O delta

### A1. O diff 4022 → 972e é só o declarado [REAL, `DIFF_POR_NO_4022_972e.json`, `ESTRUTURA_DELTA.json`]

**Tamanho.** São 855 blocos, com 4091 linhas removidas e 1432 acrescentadas. Por AST, mudam 15 nós de topo; nenhum nó é novo ou removido e nenhum anônimo muda.

**O que mudou, nó a nó:**
- **Bandeiras.** Saem 1462 auxiliares e entram 42: 41 `ext_nm394_*` e 1 `ext_bin394_0001`. A lista da escada sofre a mesma troca: 10752 → 9332. Os três contratos passam a ter `expected_ladder` 9332.
- **Specs.**
  - h2/h3/h6 passam a 29026/23069/29026.
  - O h8 vai de 1421 para 1423 entradas. São os 1422 embutidos do 972e mais `_check_damming.lean` do Nós, iguais hash a hash. Só mudam o sha da raiz e o do Audit.
  - Entra o registro novo `criterio_binario_de_parada_v394`, que lê bandeira, proveniência, o sha da pedra, os 9 nomes e as 2 falas.
- **Falas.** Entram as 2 falas de 19/10 (`786928986ca1e460` e `7596dcd880a1c8f5`), com o texto embutido conferido por sha.
- **A pedra.** Entra no corpo embutido e no livro das pedras; a raiz e o Audit ganham cada um +1 `import`.
- **Texto e veredito.** O artigo PT/EN e o `.md` ganham a errata. O token do `estatuto_da_prova_v391` troca THEOREMS por FLAGS; o conferidor aplica essa troca de palavra declarada SÓ a esse veredito e exige `_FLAGS_` presente e `_THEOREMS_` ausente.

**A pedra.** É uma conjunção pura dos 8 teoremas citados: o termo é o par anônimo das 8 provas, sem matemática nova. O sha16 é `1865eb4686899fb7` no delta, em `insumos` e no k394d.

**Linhas novas.** Nenhum literal de β, de α ou de √e; nenhuma ocorrência da palavra proibida; nenhuma atribuição ao gate.

**Scripts.**
- `instalar` e `reverter` leem o número de módulos de `ESPERADOS.kernel.modulos_novos` e de `pedras_sha256` (190), sem número digitado.
- No `rito`, mudam só os comentários.
- O conferidor ganhou: "lista vazia válida, ausência reprova", o `criterio_binario` e o hash formal com 1423 entradas mais o residual.
- `ESPERADOS`, `CANDIDATO` e `PINOS_BN` vivos apontam todos o 972e.

### A2. Re-execução dos meus scripts sobre o 972e e os logs do k394d [REAL]

**`exame_pontos_v394.py`**, com os residuais do Nós copiados para a árvore, como o rito real os vê (`EXAME_PONTOS_972e81f22dd8cc68_com_residuais.json`): **ALGUM FALSO: nenhum.**
- verify `STAGE1_VERIFIED`, cobertura 29026/23069/0, 0 não lidas, proveniência 29026.
- `ext_` 9369/9369, novas 2287/2287, nenhuma bandeira da v393 caiu.
- Escada 9332/9332; com o kf da v393, 7045 e não fecha.
- Gate recomputado idêntico, 18 de 18.
- `criterio_binario_de_parada_v394` sela. O bloco do `main` roda sem AVISO e sem mexer em chave existente.
- Mudam só os 5 da troca dita, o índice e a troca de palavra.
- Guarda: lida do candidato, morde e está limpa. Selo: `qg_closure_verdict` igual.
- Sem os residuais na árvore, o h8 recusa (`EXAME_PONTOS_972e81f22dd8cc68.json`). É o esperado: o pino agora é o da árvore REAL.

**`simular_arvore_do_nos.py`:** 1423 entradas, e todos os registros v394 selam.

**Kernel k394d.**
- Os 192 `.olean` (190 novos, a raiz e o Audit) estão em 4.31.0 / `68218e87…`; o embutido é igual ao sandbox nos 1422 arquivos.
- Build 1302 s (limite 3600), Audit 216 s (limite 1800).
- A pedra nova não está no fecho reverso de `HalfNat`, que segue com 22 módulos; logo o autoteste não muda.

### A3. O classificador de auxiliares [REAL, `CLASSIFICADOR_VS_FONTES.json`]

Os 190 módulos têm 3865 declarações. 1566 são classificadas como auxiliares (`_proof_N`, `_simp_N`, `match_N`, `_sunfold`, `eq_N`, `eq_def`, `congr_simp`). **Nenhuma** delas tem nome igual a um declarado à mão (theorem, def, structure, …) ou a um campo nas fontes `.lean`, e não há padrão auxiliar escrito como declaração. O classificador não exclui nenhuma declaração escrita à mão.

**O inverso (BAIXA, `BANDEIRAS_GERADAS_RESIDUAIS.json`):** 170 das 2287 bandeiras são geradas pelo elaborador e escapam dos 7 padrões.
- Maquinaria de 11 estruturas: `rec`, `recOn`, `casesOn`, `noConfusion(Type)`, `inj`, `injEq`, `sizeOf_spec`, `_sizeOf_*`, `_flat_ctor`, `ctorIdx`.
- Também `_f` e `_unsafe_rec`, `_abel_*` e um `_aux_` de macro.

A frase "só declaração nomeada" vale como "fora dos 7 padrões"; a v392 também marcara 6 `ctorIdx`. Não muda a validade, porque todas estão no trio e no KH-N1.

Recomendo declarar como resíduo de frase, sem regenerar. Seria a 3ª rodada sobre um achado BAIXO; se a gerência quiser exatidão, o número fica 2117 e a escada 9162.

## B. A R3.4 (só os três mecanismos novos)

### S — salto: sólido [REAL]

**O desenho.**
- Chaves fechadas, versões consecutivas e cópias de bytes pinadas por sha.
- O selo de cada elo pina o um.py e o manifesto DESSE elo.
- A ligação entre elos vem do registro do instalador e dos `.bak_`, que têm de ser byte a byte as cópias.
- O início é a Bancada e o fim é o Nós (pre_selo) ou o recibo (pos_selo).
- O limite está declarado: a cadeia prova consistência, não autenticidade.

**O que conferi no disco.**
- Cadeia `0f96cebd…`.
- Cópias em `v393\base_v392` e `v394\base_v393`.
- Registro `v393\APLICADO_AO_CANONICO_20261014_172946.json` (`4e8c837b…`).
- `Nós\um.py.bak_20261014_172946` e `um_absoluto_selo.json.bak_20261014_172946`.
- Manifesto da Bancada `canonical_contracts.json`, `6733b9a2…`, ainda igual.

**Dependência:** não apagar esses `.bak_` nem o registro até o B(n) aplicar.

### P — bateria por versão: sólida [REAL]

`conferir_pinos_da_versao` compara versão, sha e bytes do um.py e sha do selo com o Nós lido ANTES de qualquer teste. A bateria v393 pina o Nós atual (`18be2ddb…`, selo `bfddccfd…`).

Para a v394, a bateria tem de ser gerada DEPOIS do selo (`gerar_bateria_r3_4.py --versao v394`) a partir de um `PINOS_BN_v394` com `candidato` = 972e. A cópia da R3.4 tem o candidato vencido, e o gerador recusaria.

O adendo de repino do T12 (pré-registro da F1.ATRATOR) segue pendente da ratificação do Codex, como já declarado.

### M — módulos de auditoria: MÉDIA, há um desvio [REAL, `TESTE_AUDITORIA_M.json`]

A função `auditar_fonte_de_auditoria` foi extraída por AST do esboço, sem importá-lo. O filtro do corpo do `run_cmd` tem o lookbehind `(?<![A-Za-z0-9_'.])`, que exclui o ponto, e `open X in` no topo é livre. Por isso passam:
- `Lean.addDecl …`, `Lean.modifyEnv …` e `Lean.Meta.evalExpr …`, quando qualificados;
- `open IO.FS in` + `writeFile …`;
- `open IO in` + `Process.output …`.

Isso contradiz o texto, que diz recusar addDecl, escrita de arquivo e processo. Nos controles, `addDecl` nu, `IO.FS.writeFile` e `theorem` no topo são recusados.

As 3 fontes reais passam e são inofensivas: R3 tem 936 `#print axioms`; R7 e R8 têm um único `run_cmd` que só imprime `BUNDLE_DECL` e chama `throwError` se aparece axioma fora do trio.

**Correção (construtor da R3.4, numa R3.5, antes do B(n) aplicar):**
- tirar o ponto do lookbehind;
- restringir o `open` aos namespaces do kernel (ou recusar `IO`, `System`, `Lean*`);
- incluir os nomes de escrita e de processo, ou trocar o corpo por lista de permissão;
- acrescentar esses adversariais aos controles.

Isto não bloqueia instalar nem o rito.

### O recibo pre_selo `0d82d598229fd398`: VALE para o candidato e o kernel finais [REAL]

O recibo pina só o lado v393:
- a Bancada (`B3-v392`, manifesto `6733b9a2`);
- o Nós: um.py `18be2ddb`, selo `bfddccfd`, manifesto do kernel `5c7e9e1c`;
- `PINOS_BN_v393` `91e34196`, a cadeia `0f96cebd` e a bateria v393 `e47ce2e9`.

Conferi tudo hoje no disco, e as cópias de `base_v393` batem. O recibo não pina nada do 972e nem do kernel v394 (`kernel_recibo_sha256_encadeado: null`). Não é preciso regenerar, salvo se algo do lado v393 mudar antes da instalação.

### Fusão de PINOS_BN

- **Partir do VIVO**, `v394\PINOS_BN_v394.json` (`d50e8fd0…`): candidato 972e, esperados `44ec7c1d…`, critérios `a3827960…`, `pins_do_candidato` `571de055…`.
- **Levar da cópia da R3.4:**
  - `esboco_R3_4` (`12d504a1`), com `esboco_R3_3_substituido`;
  - `bateria` = `BATERIA_VINCULO_v393.json` (`e47ce2e9`), com `bateria_R2_substituida`;
  - `pino_um_py_da_bateria` (`591bccff`), `driver_t12_t14` (`3ea04bad`) e `cadeia_de_selos` (`0f96cebd`);
  - `recibo_pre_selo` = `0d82d598…`, com `recibo_pre_selo_ensaio_R3_3_substituido`;
  - `kernel_recibo` = o R3_4 `c63e94f9…`, com `kernel_recibo_R3_2_original` `11e6a3ff…`.
- **NÃO copiar `PINOS_BN_v394.R3_4.json` inteiro.** O `candidato` dele (`7abb7ba9…`, o intermediário superado) e o `esperados` (`c75d5bce…`) estão vencidos.

### Fusão do recibo do kernel

`KERNEL_RECIBO_v394_R3_4.json` = o vivo `11e6a3ff…` mais três campos: `contrato` (`KERNEL_RECIBO_R3_4`), `derivado_de` e `modulos_de_auditoria` (os 3 NetworkProofAudit). O snapshot da R3.4 é igual ao vivo.

As 190 pedras e o "depois" da raiz e do Audit batem com o corpo embutido do 972e, e o "antes" bate com o Nós; `CRITERIOS_v394` (3865/3168/0/9405, x19 = "nao") bate com o recibo. **Ele vale para o kernel final.**

O R3_2 vivo não passa na N1k da R3.4 (3 módulos sem declaração) e deve ficar só como registro.

### O que mais precisa ser fundido: o passo 10 do pós-rito está amarrado à R3.3 [REAL, `pos_rito\chain_pos_rito_v394.sh` l.44–57, 180, 210]

O passo 10 hoje:
- lê a chave `esboco_R3_3`;
- usa `KR` fixo em `kernel\KERNEL_RECIBO_v394.json` (R3_2) e exige que ele seja igual ao pino `kernel_recibo`;
- usa a `bateria` do PINOS;
- não passa `--cadeia-de-selos` nem `--cadeia-de-selos-sha256`.

Com a R3.4, o B(n) recusaria por um de quatro motivos:
- N1k nos 3 módulos, se ficar o R3_2;
- divergência de pino, se o pino for o R3_4;
- `BATERIA_COM_PINO_VELHO`, se a bateria for a v393 contra o Nós v394;
- salto sem cadeia.

**Correção:** re-derivar o passo 10 (`derivar_cadeia_v394.py`) pelos comandos da §7 da R3.4: gerar e pinar a bateria v394 depois do selo, passar a cadeia e o recibo R3_4, ler o esboço R3_4. Quem faz: a gerência ou o preparador da cadeia, antes de rodar o passo 10. O passo 10 para de forma visível, então isto não bloqueia instalar nem o rito.

## Scripts desta revisão (todos só leem, salvo a escrita aqui)

- `diff_por_no.py` e `comparar_estrutura_delta.py`: o diff por nó e o diff estrutural.
- `classificador_vs_fontes.py`: o item A3.
- `testar_auditoria_M.py`: o M.
- `simular_arvore_do_nos.py`: cópia byte a byte do original do exame.
- `exame_pontos_v394.py`: rodado da pasta do exame, com `--imp` e `--saida` aqui.

# P12 - replays T18-T22 da etapa 1 (leitura ampla de «bancada»), pre_selo contra a v391

Gerencia c1, agente P12, rodada 2, 13/10/2026 13:19-13:30 (hora local). Estatutos: [REAL] medido/lido aqui por script; [DECLARADO] dito na origem e nao conferido. Nada foi instalado nem selado; o `um.py` real nao rodou (so os scripts de replay leram os bytes dele); a Bancada real so foi lida; o gate nao se move; NOT_FALSIFIED nao e' creditacao; PASSA e' validade matematica/replay na face testada, nao creditacao.

V = `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392`. Recibos e resumo: `V\bateria_pre_selo\ensaio_2_T18_T22\`. Scripts e instantaneos: `V\rodada2\p12\`.

## 1. Resultado [REAL]

| Teste | Veredito | Como comparou | Duracao | sha256 do recibo (16) |
|---|---|---|---|---|
| T18 ligante da lei de campo curvo (F2.3) | **PASSA** | olean recompilado = `f76c372e715b883a...` byte a byte (= arquivo da entrega); saida do build = `BUILD.log`; 2 declaracoes, so no trio | 22,7 s | `373f1d4e1b98607d` |
| T19 ponte V351 e Agape (F1.2) | **PASSA** | oleans `940b8ddfaa172144...` e `ba0d986894c5c3ab...` byte a byte; logs de build byte a byte (sha do log = o do `BUILD_COMPLETION_RESULT.json`); 2+2 declaracoes no trio | 39,1 s | `7662b7ef4a352ef4` |
| T20 PALAVRA (sandbox 07/10) | **PASSA** | fonte `33184b49a8bba7e7...` recompilada; 7 declaracoes no trio, saida igual a `saida_palavra.txt`; **nao ha olean de referencia** (a pedra nunca foi guardada compilada), logo a comparacao e' pela saida, nao por bytes | 19,5 s | `22de10b458e855d2` |
| T21 SN1, contas condicionais (F8.2.SN1) | **PASSA** | rerun de `calculate_r2.py` (copia sha-identica) vs `CALCULOS_R2.json`: 124 folhas, 98 floats **exatos**, 0 diferencas; idem vs `CALCULOS_R2_RERUN.json` do auditor A_SN | 0,3 s | `6331c293038faca1` |
| T22 NU2 (F8.2.NU2) | **PASSA** | (a) rerun de `spectral_operator_r1.py` vs `CALCULOS_ESPECTRAIS_R1.json`: 734 folhas, 653 floats exatos, 0 diferencas; (b) `reproducao_nu2.py` da B_NU2 rodado em copia: **21 de 21**, mesmos nomes e ordem do `_reproducao_nu2.json` do auditor | 2,6 s | `7bbadac5cf541e32` |

Soma T18-T22: **5 PASSA, 0 FALHA, 0 NAO_EXECUTADO**. Somada ao `ensaio_1` (T01-T17: 13 PASSA, 0 FALHA, 1 NAO_EXECUTADO = T17 «nao pertence a fase pre_selo»): **18 PASSA, 0 FALHA, 1 NAO_EXECUTADO em 19**. `RESUMO_T18_T22.json` (sha256 completo lido por script no arquivo: `56bbbbdb290a68cee428bff4a37f5c64f060c7c62e04a95ea4b9d2e774c12e36`) traz o veredito por teste, o sha256 de cada recibo, o T12/T13/T14 do `ensaio_1` e o recibo de sincronizacao dele.

**Controle negativo** (`recibos\CONTROLE_NEGATIVO_T18_T22.json`, sha16 `953faee202f79fcc`): 8 de 8 detectados. Float perturbado em 1e-6 relativo e' acusado; em 1e-15 (dentro da tolerancia) nao; string alterada e' acusada; `copy_check` com sha errado recusa; fonte Lean com `sorry` e' acusada (`sorryAx`); fonte Lean com erro e' acusada; olean de uma pedra difere do de outra; axioma fora do trio e' recusado.

**Segunda ressalva da auditoria c1 de 10/10** conferida por trecho (`AUDITORIA_F1_ATRATOR_C1_a7c491ec.md`, sha256 `6b3a2ec12212fd97...` lido): as linhas 69 a 71 sao «Duas ressalvas a constar no fechamento: / 1. A4 nao foi ligado ao atrator do GKLS v384. / 2. A5 e A3_angular nao podem ser lidos como testemunho fisico nem ontologico.» A frase exata esta na l.71 (`contem_a_frase_da_segunda_ressalva: true`). Ela vale sobre todo o bloco do atrator (T12/T13 e, por extensao, T18-T22): PASSA aqui e' validade matematica sintetica e replay documental, nao testemunho fisico, nao ontologico, nao creditacao.

## 2. Protocolo e comandos exatos [REAL]

Python: `C:\Python314\python.exe` 3.14.3 (MSC v.1944, 64 bit). Lean: `C:\Users\rotol\.elan\toolchains\leanprover--lean4---v4.31.0\bin\lean.exe`, versao `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`.

Antes de tudo: instantaneo da Bancada (`snap_bancada.py antes`: 1206 entradas, sha256 da lista `a2d88c6a784574d3...`) e impressao digital do `tgl_kernel` do Nos (`impressao_digital_kernel.py antes`, copiada para a pasta p12 para gravar la).

Lean (T18-T20), em copia isolada: a fonte e' copiada para `C:\t\p12\tNN\<modulo>.lean` com o sha256 conferido contra o pino (lido do `HASHES.json` da F2.3, do `BUILD_COMPLETION_RESULT.json` da F1.2, ou do arquivo para a PALAVRA), depois
`lean.exe -o C:\t\p12\tNN\out\...\<X>.olean --root=C:\t\p12\tNN C:\t\p12\tNN\...\<X>.lean`, `cwd` = `C:\t\p12\tNN`, com `LEAN_PATH` = `kernel_src\.lake\packages\{batteries,Qq,aesop,proofwidgets,importGraph,LeanSearchClient,plausible,mathlib}\.lake\build\lib\lean` + `kernel_src\.lake\build\lib\lean` + `<toolchain>\lib\lean` (+ para a T19, o diretorio `build` do proprio sandbox, onde a Agape acha a V351). E' a mesma receita do `build_completion.py` da F1.2. `kernel_src` = `C:\IALD\Central de Patentes\work\v388_kernel\kernel_src`, so lido; conferido que e' o Nos v391: impressao digital com fontes `78c1f97cd83bea2e` e oleans TGLExt `2c9841d0959f9ccc` iguais as do Nos (`fp_kernel_src_p12.json`). Nao rodei `lake build` em lugar nenhum e nao toquei `C:\t\k392`.

Python (T21, T22): copias sha-identicas dos scripts e planos em `V\bateria_pre_selo\ensaio_2_T18_T22\trabalho\T21` e `...\T22`; T21: `python -I -B -X utf8 calculate_r2.py --output ...\CALCULOS_R2_REPLAY.json`; T22: `python -I -B -X utf8 spectral_operator_r1.py --output ...\CALCULOS_ESPECTRAIS_R1_REPLAY.json` e `python -B -X utf8 reproducao_nu2.py` (sem `-I` so este: numpy/scipy/mpmath vivem no site do usuario; mesma excecao que a regra 5 abre para o `um.py`). Tolerancia declarada nos reruns numericos: floats com erro relativo <= 1e-12, o resto exato; ignorados apenas `start_utc`, `end_utc`, `elapsed*` e os caminhos dos `pins` (os sha256 e bytes dos pins sao comparados a parte e conferem). Na pratica todos os floats deram **exatos** (max_rel = 0), a tolerancia nao foi usada. `beta0` do replay = `0.012031300400803142`, igual a conferencia, calculado em runtime a partir de `ALPHA_FINE_CODATA_2018` lido por regex dos bytes do `um.py` v391 (`8e7b9927ceae64b8`, o da `um_py_sha256` do replay da B_NU2).

Cada recibo traz: comando, cwd, inicio, fim, duracao, codigo de saida, versao do python (e do lean), plataforma, sha256 e bytes de cada entrada (inclusive os pinos lidos) e de cada saida, a comparacao completa e o veredito. Falha vira recibo `NAO_EXECUTADO`/`FALHA` com a razao; nunca ok falso (todo o fluxo roda dentro de um `try` que grava a excecao).

Depois: `snap_bancada.py depois` (1206 entradas, mesma lista, **mesmo sha256**), `impressao_digital_kernel.py depois` (todos os campos iguais ao «antes»), `limpar_p12.py` (listou 11 arquivos / 251.009 B dentro de `C:\t\p12`, recusa caminho fora, apagou; `LIMPEZA_p12.json`).

## 3. Problemas e observacoes [REAL]

1. **Primeira execucao do T22 falhou** (FALHA gravada): o script espectral tambem le `PLANO_RECONCILIACAO_R1.json`, que eu nao havia copiado (erro meu, `FileNotFoundError` na copia). Corrigi copiando o terceiro arquivo (e o `ignorar` das chaves `source_pins`/`elapsed_s`, que eram `pins`/`elapsed_seconds` do T21) e reexecutei. O recibo da primeira tentativa ficou como `recibos\T22_NU2.json.bak_20261013_132457` (backup de bytes do estado anterior; nao apaguei).
2. **T20 nao tem olean de referencia**: a PALAVRA (`TGLExt.Palavra`) esta so como fonte + saida de 07/10; os oleans de F_KERNEL (12/10) estavam no scratchpad apagado. A comparacao e' pela saida (7 declaracoes + axiomas), e a fonte do `F_KERNEL\inst\TGLExt\Palavra.lean` (insumo duravel) foi conferida igual a fonte do sandbox de 07/10 (campo `conferencia_cruzada` do recibo). O olean do replay (`d52ebd0943e96192...`) fica registrado, mas nao e' comparado com nada.
3. **A fonte da Agape comparada em T19 e' a da entrega F1.2 (`cf30422393b2af21`)**, nao a instalada no candidato v392 (K05, `e49ad8f980d7cf48`, uma linha de import derivada). O replay prova a entrega; a pedra instalada ja foi coberta por `kernel\` da cadeia (`lake build` da etapa 2).
4. O `RESULTADO_R1.json` da NU2 pina `CALCULOS_ESPECTRAIS_R1.json` e as fontes por sha256; os pinos conferem com os arquivos (campo `referencia_igual_ao_pino_do_RESULTADO_R1: true`).
5. Os scripts `calculate_r2.py` e `spectral_operator_r1.py` e `reproducao_nu2.py` leem os bytes do `um.py` do Nos (v391, hoje canonico). **Depois do selo da v392 esses replays teriam de ser refeitos contra a nova fonte** (como os runners do atrator, que pinam a v391): por isso este e' o ensaio pre_selo.
6. Nao chamei o servico HTTP da Bancada, nao importei nada de `Bancada_Um`, nao escrevi no quadro, mapa, memoria, tunel, git. Sem init/transition ACOM (regra 2 da rodada).

## 4. O que e' ato da gerencia/operador

- Decidir se o registro da v392 (`bancada_v392`, R12) cita estes 5 recibos por sha256 (e se os copia para o `cache` do rito, junto da P4).
- A B3 (pos-selo, `--modo aplicar`) continua sendo ato do operador/gerencia.
- T17 segue NAO_EXECUTADO por desenho (fase pre_selo); a recompilacao do atrator (A6/A8/A9) esta coberta pela F_KERNEL (J1) e pela cadeia do kernel.

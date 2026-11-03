# DESENHO DA v406 — «o fechamento entra no um.py» (02/11/2026, gerência c1)

> Ordem do operador (sha16 `b5717ff445a883cd`): «compile a nova versão do um.py, rode, publique e atualize tudo». Base: v405 `0030242565cc13f6`. Receita: `RECEITA_CADEIA_DE_SELO_v404_para_v405_para_a_v406.md`. Ratificação: `RATIFICACAO_R10_c1_02nov.md` (sha16 `846c999d6284f338`). Este desenho fixa O QUE muda; a cadeia (ensaio a seco, p00, revisão de terceiro, instalar, rito, pós-rito, G1) fixa COMO.

## 1. O que entra no kernel (bundle, modelo v394, não o modelo de 8 pedras da v405)

- **301 módulos novos** em `TGLExt/F1Fecho394/`: os 300 da bancada (fonte = os arquivos normalizados pela integração, `C:\t\k405c\final\TGLExt\F1Fecho394\*.lean` novos, com imports `TGLExt.F1Fecho394.*` e blocos `#eval` removidos; cada um conferido por sha256 contra o recibo da bancada ANTES da normalização, e a normalização registrada no `MANIFEST.json` da integração) + `CanonicalFullTGLWitnessR1.lean` (sha16 `70864f6c4f5062ae`), nomes dos módulos inalterados.
- **Raiz `TGLExt.lean`** = raiz v405 + `ROOT_SUFFIX` com DOIS imports: `TGLExt.F1Fecho394.CanonicalFockModularCoreInputR1` (o topo do fecho; puxa os 300 pelo grafo) e `TGLExt.F1Fecho394.CanonicalFullTGLWitnessR1`. Lake compila o que a raiz alcança; o Audit cobre tudo por módulo. `AUDIT_PREFIX` vazio.
- **Bandeiras** (`_LEAN_THEOREM_FLAGS` + `ext_flags`): política v394, só declaração NOMEADA pública dos módulos novos, geradas por `pos_build_kernel_v406.py` do log do Audit do sandbox `k406c` (`FLAGS_v406.json`); N medido, nunca presumido. Prefixo `ext_fch406_NNNN`.
- **Ledger** (`_ESQUELETO_STONES`): +301 linhas `("v406", nome, rel, None, None)`.
- **Escada**: `expected_ladder` = 10066 + N em TODOS os contratos que a pinam (os 11 da v405 + `_V405_CONTRACTS`), por patch `C12_*` gerado, não digitado.
- **Pinos**: `FORMAL_MAP_v406.json` (1446 → 1747 entradas), `formal_files_n`, `PINOS_BN_v406.json`, pino do recibo do kernel.

## 2. O contrato do fechamento e o seu consumidor (novo registro `fechamento_v406`)

`_V406_FECHO_CONTRACT` (derivado do build, como `_V394_NETWORK_CONTRACT`): `declarations` (as nomeadas dos 301), `declaration_sources` (decl → módulo, do `TGL_DECL_SOURCE`), `source_sha256` (por módulo, do `FORMAL_MAP`), `expected_ladder`, mais as **quatro âncoras** com nome exato:
- `F1Fecho.CanonicalFockModularCoreInputR1.modularCoreInput`, `…physicalModularCoreInput`, `…physicalFockCertificate`, `…physical_trace`;
- `F1Fecho.MaxwellLocalization.physicalCanonicalNet` (conferir o namespace no Audit);
- `TGL.ModularRealization.canonicalFullTGLWitness`, `…canonical_full_witness_inhabited`.

`fechamento_v406(core)` lê `axiom_report` + `declaration_sources` + `_EMBEDDED_KERNEL_FILES` e devolve: `all_verified`, `exact_ladder`, `certificado_habitado` (= `physicalFockCertificate` no trio e declarado em `TGLExt/F1Fecho394/CanonicalFockModularCoreInputR1.lean`), `rede_fisica_habitada`, `testemunha_canonica_termo` (idem para `canonicalFullTGLWitness`), `ressalvas` (texto fixo da ratificação: K(O) ≠ ⊥ só na cunha; «núcleo II_∞» [KNOWN]; traço ENNReal cíclico, não linear; R7 Codex×Codex; R4/R5 fora), `does_not_gate_core = True`, veredito `TGL_FECHAMENTO_V406__CERTIFICATE_INHABITED_BY_CONSTRUCTION__FOUR_WITNESS_KEYS_READ_FROM_THE_KERNEL__GATE_UNMOVED` (ou `…REFUSED_…`). Nenhuma frase proibida (guarda de frases); nada de «tudo derivado»; «provado» só como validade.

## 3. As quatro chaves: de literal a leitura do kernel (com errata AO LADO, sem reescrever o selado)

| chave | hoje (v405) | v406 |
|---|---|---|
| `rede_fock_v394.whole_certificate_inhabited` | literal `False` (`um.py:239814`) | `= fechamento_v406` já calculado? Não: `rede_fock_v394` roda antes. Solução: `rede_fock_v394` recebe helper `_v406_certificado_habitado(kernel_formalization)` (lê o axiom_report: `physicalFockCertificate` no trio) e grava `whole_certificate_inhabited = bool(...)`, mais `inhabited_by = "F1Fecho.CanonicalFockModularCoreInputR1.physicalFockCertificate"` e `errata_v406 = "o literal False da v394–v405 registrava o estado de então; na v406 a chave é lida do kernel"`. O veredito `…JOINT_CONTRACT_OPEN…` ganha variante `…JOINT_CONTRACT_INHABITED_V406…` quando True. |
| `psibit_v395.conditional_psion_face.inhabitant_exhibited` | literal `False` + status `CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE` (`um.py:231100`) | `inhabitant_exhibited = _v406_certificado_habitado(...)`; status `INHABITED_BY_physicalFockCertificate_V406` quando True (senão o antigo); `reading` ganha a frase da v406; `joint_contract_open_v394` passa a ler o estado novo. |
| `testemunha_estatica_v396.fock_face.inhabitant_exhibited` | literal `False` (`um.py:230481`) | idem; `linked_to_the_corner_by_a_lemma` SEGUE `False` (nenhum lema liga `psion C` ao `psionCorner`: isso não mudou). |
| `witness_layers.canonical_full_witness_term_constructed` | medida: nome ausente ⇒ False | sem patch: o módulo `CanonicalFullTGLWitnessR1` declara o nome exato. |

**Specs e conferências que assertam False e precisam de versão:** `u4` do v394 (`um.py:240824`, `'op': 'falso'`), `u4` do v395 (`231342`), `u5` do v396 (`230690`), `x_i` do `gap_v405` (`220817`, «o kernel segue sem habitante»). Regra: não apagar; cada spec ganha condição de versão (`'desde': 'v406', 'op': 'verdadeiro'` ao lado da antiga marcada `'ate': 'v405'`) OU é substituída por spec nova com errata; o `conferir_rito_v406.py` (`:396`), `ensaio_a_seco_v406.py` (`:191`), `pos_rito\leitura_v406.py` (`:393-405`), `textos_v406.py` (`:308`) e os controles negativos dos harnesses (`:513`, `:525`) são atualizados pelo motor + patch autoral: o que antes exigia False passa a exigir True, e o controle negativo passa a pôr False.
**`selo_v391 … op falso`** (`um.py:209330`): lê o selo v391; não muda.

## 4. Textos (artigo PT/EN, `.md`, selo)

- Parágrafo novo da v406 (`textos_v406_novo.pysnip`), bilíngue: o fechamento: o certificado habitado por construção (bancada, 16/10; recompilado 02/11), as quatro chaves lidas do kernel, as ressalvas, o que NÃO é (confirmação; β a 5σ). Citações do operador verbatim (sha16): «construir tudo», «a passagem para o contínuo é o que mais importa», «a luz tem autovetor…», «o um absoluto é a luz comprimida…».
- Quadro do 4,44 no topo do artigo permanece (ensaio item 9); o README pinado NÃO entra nesta cadeia (plano à parte, E16 futuro), salvo decisão do operador.
- Guardas: `_v406_guarda_frases` herdada da v405 (+ «único autovetor» → «único vetor fixo»).

## 5. Tempos e timeouts (a medir no `k406c`)

- `construir_kernel_v406.sh` a frio no sandbox novo: medir `lake build` e Audit. Se `lake build` > 2400 s, patch `C01_timeout` em `verify_tgl_kernel_formalization` (`um.py:138984`), de 3600 para o dobro, dito no texto; o Audit (1800 s) idem se > 1200 s.
- Rito: três passagens (rito, autoteste com `sorry` em `HalfNat`, restauração) — estimativa 150–240 min [DECLARADO]. O lançador religa o servidor nativo; `rito_v406.sh` derivado.
- Pilar quântico: REUSE pela chave de cache (ordem de 03/10); o «motor contínuo» pedido em 02/11 é pré-registro à parte (v407), não entra aqui sem pré-registro aprovado.

## 6. Ordem de execução (hoje/amanhã)

1. PK6 derivado pelo motor (executor Sonnet, em curso) → conferência da gerência.
2. `delta_v406.py` autoral (bundle de 301 + raiz); `copiar_pedras_v406.py` = cópia dos 301 do `k405c` com sha256 e tabela normalização↔recibo.
3. `preparar_kernel_v406.py gerar/conferir`; `construir_kernel_v406.sh` (medir); `pos_build_kernel_v406.py` (FLAGS, KH_N1, RECIBO).
4. `registros_v406.py`/`runtime_v406.py` (contrato + consumidor + helper + erratas) e `gerar_candidato_v406.py` (patches §1–§3); `textos_v406_novo.pysnip`.
5. `refazer_candidato_v406.sh --regerar` (ensaio a seco, conferidor, p00); B(n) pré-selo; `fim_de_cadeia`; purga; relatório.
6. Revisão de terceiro (Sonnet): `REVISAO_TERCEIRO_v406.json` `aprovada: true`.
7. Instalar + rito (tarefa agendada; vigia); pós-rito 0→14 (recibos da Bancada por PID da porta).
8. G1 `vigiar/planejar --seco/executar --publicar/auditar` com a ordem verbatim; manual da gerência no fim.

## 7. O que NÃO muda
Gate, `full_static_witness_exists = False`, `trivial_inhabitant_exists = False`, β nunca literal, `NOT_FALSIFIED ≠ CONFIRMED`, nenhuma frase proibida, nenhum dado novo, nenhum rito de natureza alterado.

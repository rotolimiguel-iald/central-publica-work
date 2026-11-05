# PEDIDO DE REVISÃO DE TERCEIRO — v408 (gerência c1, 05/11/2026)

> Quem constrói não aprova. O S1b do orquestrador (`orquestrador\pos_treino_v408.py`) só instala com `revisao_terceiro\REVISAO_TERCEIRO_v408.json` trazendo `aprovada: true`, `candidato_sha16` igual ao do `um_v408_candidato.py` em disco e `arquivos_revisados` cujos sha16 batem com o disco.
> MOLDE: o pedido da v407, `C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\revisao_terceiro\PEDIDO_REVISAO_v407.md` (os oito itens, o que NÃO é objeto, a nota de processo e a ENTREGA valem iguais), com as trocas abaixo. Os scripts de conferência da v407 na mesma pasta (`a_intocados.py`, `a2_mudados.py`, `b_gera_lean.py`/`axiomas_terceiro.lean`, `c_fail_closed.py`, `d_kernel.py`, `e_citacoes.py`, `f_hashes.py`, `h_paragrafo_e_guardas.py`, `k_funcoes_vivas.py`, `l_orquestrador.py`, `m_flags_audit.py`, `n_hashes_digitados.py`, `fechar_revisao*.py`) são o modelo a reproduzir para a v408 nesta pasta.

## As trocas da v408 sobre o molde

- **Base:** `base_v407\um.py` (v407 selada, `833121339e649f71`). **Candidato:** `um_v408_candidato.py` (sha16 LIDO do arquivo ao abrir e ao fechar; no portão PRONTA de 05/11/2026 era `c55c4a7f2753b589`). `DIFF_v407_v408.diff`, `COMPARACAO_V407_v408.json`, `CANDIDATO_v408.json["patches"]` (39).
- **Bundle:** 4 módulos em `TGLExt/` — `TetelestaiTerminal`, `TempoIgualMoeda`, `PontoDeContradicao`, `PIgualNP` (nomes do operador, ratificados em 04/11) — com 42 `#print axioms` nas fontes de `insumos\`; `pedra\<Nome>.lean` = sandbox `C:\t\k408c\final\TGLExt\<Nome>.lean` = `BUNDLE_v408.json` (sha256); a cópia normalizada difere da fonte só no cabeçalho e nos `#print axioms`. 44 bandeiras; escada 11958 → 12002 (`kernel\KERNEL_RECIBO_v408.json`, `kernel\POS_BUILD_v408.json`).
- **Runtime e registros:** o registro com função `tetelestai_terminal_v408` (16 checagens, `runtime_v408.py`), os specs `cunhagens_v408` e `kh_n1_cobertura_v408` (`registros_v408.py`, `delta_v408.py`); decisões D48–D54; erratas E21–E23; β só em runtime.
- **A D51 REVISTA** (ler o AO LADO no fim de `DESENHO_v408.md`): «P = nP» trata das CLASSES DE COMPUTAÇÃO DO DICIONÁRIO DO OPERADOR e nelas é teorema, `PIgualNP.as_classes_do_dicionario`; a tradução às classes de Turing (bits = log₂ n) é [OPEN], não recusa. A guarda de frases proíbe «a TGL prova/decide P = NP de Turing», «P = NP está provado» sem o qualificador «do dicionário» e «não trata das classes», e exige o qualificador e a ressalva onde «P = nP» aparecer em prosa. Conferir que o candidato, os textos (artigo PT/EN, `.md`, `pos_rito\textos_v408*`, os sete textos do handoff) e as docstrings das quatro pedras dizem isso, e nada mais.
- **A leitura honesta (item 8):** o terminal é a leitura, não o fim do decaimento; não há relação sem peso (o cociclo paga: a inclinação modular); o tempo é a moeda de β; o zero inscrito é o Um e o Um não é o zero absoluto; P = nP nas classes do dicionário; o par na face de Fock segue [OPEN]; validade no kernel não é creditação; o gate não se move.

## Limites desta revisão (gestão de créditos do operador)

No máximo DUAS rodadas. Conferências por script, sem reimprimir o candidato (43 MB). Achados ALTO/MÉDIO bloqueiam (`aprovada: false`), com a correção pedida em `PEDIDO_CORRECAO_R1_v408.md`; BAIXOS ficam escritos e não bloqueiam. O revisor não edita nada fora de `revisao_terceiro\`.

— gerência c1, 05/11/2026.

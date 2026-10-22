# Esquema dos registros v392 (13/10/2026) -- como escrever um `grupo_*.py`

Cada grupo e' um arquivo `V\registros\grupo_<X>.py` (V = `C:\IALD\Central de Patentes\work\cadeia_de_selo\v392`) que define tres listas de dicts (Python puro, sem I/O alem de LER fontes):

```python
FONTES = [{"chave": "kh_final", "arquivo": r"C:\...\KH_N1_final.json", "papel": "o que e' e por que entra"}]   # arquivos pinados por sha256 (lidos do disco pelo montador)
VERBATINS = [{"chave": "vb_palavra", "arquivo": r"C:\IALD\PROGRAMA_IALD\OPERADOR_07out_palavra_verbatim.txt", "trechos": ["PALAVRA"], "quando": "07/10/2026"}]  # fala do operador EMBUTIDA
SPECS = [ {...um dict por registro...} ]
```
Arquivos so' em pasta DURAVEL (nunca scratchpad/AppData/Temp/C:\t): use `C:\IALD\Central de Patentes\work\v392_insumos\...` para o que veio do scratchpad.
`trechos` TEM de estar literalmente nos bytes do arquivo (o montador recusa). Toda citacao do operador entra por VERBATINS (nunca digitada solta).

## Campos de um spec
- `nome` (obrigatorio; termina em `_v392`), `veredito_prefixo` (ex. `TGL_PALAVRA_V392`), `veredito_sufixo` (ex. `THE_READING_CREATES_THE_OBJECT__KERNEL_VALIDITY_IS_NOT_CREDITATION__GATE_UNMOVED`; sem a palavra recusada).
  Veredito final = `prefixo__sufixo` se tudo passa; senao `prefixo__NOT_SEALED_THIS_RUN__<FALHAS>__GATE_UNMOVED`.
- `estatuto` (str): ex. `[REAL -- ...; DECLARADO ...]`.
- `fontes`: lista de chaves de FONTES que o registro RELE e confere por sha256 a cada rito (fail-closed).
- `verbatins`: chaves de VERBATINS.
- `kernel_flags`: bandeiras `ext_...` que tem de ser True no kernel do PROPRIO rito; `kernel_decls`: nomes completos de declaracoes que tem de estar no `axiom_report` com axiomas dentro do trio. (Pegue as listas de `V\kernel\FLAGS_v392.json` - campo `flags` = [bandeira, declaracao, modulo, tipo] - ou do kernel do Nos v391 para o que ja existe; por script, nunca de memoria.)
- `checks`: lista de leituras que TEM de passar: `{"id": "c1", "descricao": "...", "onde": "core" | "kf" | "fonte:<chave>" (JSON), "caminho": ["chave", 0, "outra"], "op": <op>, "valor": <esperado>, "capturar": "nome_opcional", "estatuto": "[REAL]"}`.
  `onde=core` le o core da rodada (ex.: `["readings_ratified_20261002","R3"]`); `kf` = `core["kernel_formalization"]`; `fonte:<chave>` carrega o JSON da fonte pinada.
  ops: perto_de_beta_runtime (valor = tolerancia relativa; alvo = SEALED_CODATA_ALPHA x sqrt(e) calculado no rito), maior_igual_beta_runtime, existe, igual, diferente, contem, nao_contem, comeca, maior_igual, menor_igual, em, verdadeiro, falso, tamanho_igual, tamanho_maior_igual. `capturar` guarda o valor lido em `lido[nome]` (numeros que a errata cita saem do core/da fonte em runtime).
  Use `contem`/`igual` com valores obtidos por SCRIPT na hora de escrever o spec (o spec pode computa-los lendo as fontes; o resultado entra como literal nos dados).
- Texto (todo ele passa pela guarda P18 a cada rito): `erratas`: lista de dicts `{"ao_lado_de": "onde", "dizia": "...", "agora": "...", "lacuna_de_fidelidade": "o que a estrutura dizia / o que foi escrito / onde a traducao falhou", "estatuto": "[...]", "assinatura": "gerencia c1, em nome proprio, 13/10/2026"}`; `limites`, `diz`, `nao_diz`: listas de str; `leituras_do_operador`: `[{"trecho","estatuto"}]`; `extras`: dict livre (JSON-serializavel).
- `sem_guarda` (so' para registro que cita a palavra recusada de proposito: NAO use; reescreva).

## Regras de redacao (valem para TODO texto)
Estatuto marcado em cada afirmacao ([REAL] medido por script/lido do arquivo, [DERIVED], [DECLARADO] dito na origem e nao conferido, [OPEN], [INPUT] fala do operador, [KNOWN] literatura). O numero corrige a frase: valores numericos saem da fonte (capturar) e a errata os cita lendo-os. Errata sempre AO LADO, em nome proprio da gerencia c1, dizendo a lacuna de fidelidade. A guarda barra: a palavra recusada, "Nome fixo", "singularidade converge/cai no atrator", luz/observacao "confirma", "nao provou", "pos-dicao". Em vez disso: creditacao (nao "confirmacao"); o fixo e' o Verbo/beta_TGL; o observador testemunha; retrodicao sem ajuste (novidade de uso). NOT_FALSIFIED nunca e' a palavra da creditacao; validade no kernel nao e' creditacao; o gate nao se move; nenhum registro altera valor do core (so' ADICIONA chaves).

## Como testar
`python -B -X utf8 V\testar_registros_v392.py --grupo <trecho do nome do arquivo> --so-falhas` roda o motor sobre a v391 selada + kernel sintetico (FLAGS/log do sandbox): mostra OK/FALHA por registro, e o controle negativo (fonte/verbatim adulterados => recusa). Dentro do um.py candidato, as chaves entram em `core[nome]` e no selo como `registros_v392[nome] = {verdict, all_verified}`.

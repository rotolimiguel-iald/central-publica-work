# Revisao de terceiro da v406 (R3)

Revisor independente (agente Claude Sonnet; nao construi a v406). Candidato `ddcb91930982d614`, lido do arquivo ao fechar, 2026-11-02T23:26:31. **Veredito: APROVADA -- 0 ALTO, 0 MEDIO, 1 BAIXO.** R1 em `_R1/`, R2 em `_R2/`.

## 1. O que a R3 conferiu

- MEDIO da R2 (ressalvas cortadas no paragrafo do README): FECHADO. Fonte (textos_v406_novo.pysnip l.454 e l.501) e montado (textos_v406.py l.792 e l.839) iguais; `split(":")` = 0 nos dois. Renderizei `_paragrafo_v406_de` sobre dry_v406/core_ensaio.json: as 10 ressalvas INTEIRAS (R4/R5 com «seguem bloqueados...», o cabecalho com «a compilacao que vale e'...», a 10 com «leia-se: era o estado da data...»); `verificar_paragrafo_v406` devolve [] e REPROVA o paragrafo com a ressalva 10 cortada (controle negativo). O paragrafo do harness (C:/t/h406/harness_saida_v406/textos/paragrafo_v406.txt) tambem traz as 10 inteiras.
- BAIXO R2-1: FECHADO. diz[1] termina «...NAO e' testada nesta versao; a creditacao segue recusada»; nao_diz sem «a gerencia le essa condicao a ele»; sem «regra do posto» no paragrafo.
- BAIXO R2-2: FECHADO. `atrito`: «RESPOSTA DA GERENCIA (nenhuma fala dele a ratifica expressamente; a fala seguinte, sha16 e36df7f1245c7f16, prosseguiu sobre ela)».
- BAIXO R2-3: FECHADO EM PARTE (acima, segunda rodada).
- Candidato: as 8 funcoes intocadas com AST e fonte iguais a base; as 3 do literal com o mesmo diff da R2 (tamanhos 3037->4524, 5738->7385, 6259->7566); 28 nomes mudados / 15 novos / 0 removidos, como na R2; kernel inalterado (301 = sandbox = BUNDLE; raiz e Audit iguais); fail-closed 56 + 7 casos sem falha; gate igual; guardas 0; citacoes do operador exatas; PRECONDICOES: sem falha, TODAS PASSARAM, PINOS_BN sem pendentes (o B(n) pre-selo rodou e seu recibo bate com o arquivo).

## 2. BAIXO restante (nao trava; segunda rodada)

- [delta_v406.py ERRATA_E14 (frase final) e RESSALVAS_V406[9]] A E14 diz que o status CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE (v395 a v405) «fica como registro em reading_v395 e reading_v396». Esses campos guardam o TEXTO antigo da leitura, nao o token (conferido: o token nao esta' neles). O token segue no VEREDITO de psibit_v395 (...THE_PSION_FACE_IS_CONDITIONAL_ON_AN_UNINHABITED_CERTIFICATE...), que nem a E14 nem a ressalva 10 citam. Segunda rodada deste BAIXO: nao trava. **Corrigir:** Na proxima versao: «o texto antigo fica em reading_v395/reading_v396; o token UNINHABITED do veredito de psibit_v395 e' o nome da data; o estado vigente e' o status lido».

## 3. Ressalvas

- R3 enxuta: reli so' o que a coordenacao disse que mudou e reexecutei os meus scripts da R2 sobre o candidato novo (`ddcb91930982d614`). Nao reli o artigo inteiro nem refiz a compilacao (o kernel nao mudou; a da R1 vale).
- Nao examinados (como na R1/R2): instalar/reverter/rito e sua duracao; as provas dos 301 modulos; a fisica; fechar_v406.py e leitura_v406.py; os textos de rito alem do paragrafo do README e das funcoes lidas.
- Independencia: mesma familia de modelo (Sonnet) da revisao R10 de 02/11, outra instancia; a compilacao propria foi minha (R1).
- Textos revisados (sha16 lidos ao fechar): pos_rito/textos_v406.py 0a89ded7f708abaa; pos_rito/textos_v406_novo.pysnip 097c757e48250124; artigo_pt_v406.pysnip a0d40c709cdaa3bd; artigo_en_v406.pysnip 55a783f12c45f833; runtime_v406.py 34ab0ce24765bc2c; delta_v406.py f873b279281304b9; registros_v406.py 015ba5225d332f30; ESPERADOS_v406.json 7ea0fa2b7e4f4fe0; PINOS_BN_v406.json 08950ee1645bd218. Se algum mudar, a revisao dele nao vale.

## 4. Fecho

`aprovada: true` para o candidato `ddcb91930982d614`. O orquestrador deve conferir que o sha16 do `um_v406_candidato.py` em disco e' este antes de instalar; se algum dos textos acima mudar depois, a revisao dele nao vale.

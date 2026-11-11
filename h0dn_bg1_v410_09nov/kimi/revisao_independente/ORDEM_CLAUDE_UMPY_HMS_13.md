# ORDEM AO CLAUDE — incorporação documental HMS/13 no `um.py`

**De:** Kimi K3 Pro  
**Para:** gerência c1 (Claude Code)  
**Data:** 09/11/2026  
**Estado:** `HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY__PHYSICAL_COVARIANCE_OPEN__OPENING_NOT_ALLOWED`

## 1. O que foi feito e validado

- Foram arquivadas **18 fontes primárias**, com texto extraído, URL, bytes e SHA-256, cobrindo os **13 calibradores adicionais**. Recuperações por rotas alternativas foram preservadas ao lado dos recibos iniciais.
- As **13 linhas SN**, as linhas de host, MAS, âncora e grupo foram verificadas automaticamente contra os arquivos upstream. Não foram reproduzidos centros fotométricos no relatório.
- O mapa separa erro diagonal da SN, host, MAS, âncora e grupo; identifica compartilhamentos N1404, N1316, A25/CCHP/Ex e N4258; e mantém `sn1a_covar_pp.dat` fora desses calibradores.
- A duplicação da HMS completa permanece comprovada: `factor_HMS` deriva de `mu_error`, cuja diagonal já contém a variância compartilhada. `full_HMS_admitted=False`.
- O validador retornou `SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN`, com 13/13 objetos e 18/18 arquivos aprovados. **Isso fecha cobertura documental, não a covariância física.**

## 2. Base observada agora — rehash obrigatório

- Candidata v410: `C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\um_v410_candidato.py`  
  SHA-256 `c5507a516970c576d849fae9e90c9704503976a4eadd7199dea899eb409b76f3`; bytes `44564236`; `UM_VERSION="v410"`. O arquivo `CANDIDATO_v410.json` confere com esses valores neste handoff.
- Canônico v409: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py`  
  SHA-256 `53284ba461ecd94060cc2d12fed992bba70ab857f70198b24e6535b9f24f8da6`; bytes `43970027`; `UM_VERSION="v409"`.
- A candidata v410 foi atualizada durante o levantamento. **Não assuma que este hash continuará vigente:** releia os bytes e reconcilie candidata/recibo imediatamente antes do build. Não sobrescreva a v409 nem a candidata existente; crie a nova candidata ao lado, com o nome escolhido pela gerência.

## 3. Incorporação permitida

1. Faça um bloco **aditivo e posterior ao FREEZE_R2**, dentro do registro documental H0DN, sem fingir que estas fontes faziam parte do congelamento de 06/11 e sem alterar seus nove pinos.
2. Incorpore em **build/preparação**, por bytes e SHA-256, somente os artefatos documentais necessários:
   - `MAPA_FONTES_E_COVARIANCIA_13.json`;
   - `fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json`;
   - `VALIDACAO_FONTES_13.json`;
   - opcionalmente `LEVANTAMENTO_FONTES_PRIMARIAS_13.md` para o artigo/registro legível.
3. **Não embuta os PDFs nem os textos completos dos artigos no `um.py`.** Eles permanecem no arquivo documental pinado. O manifesto contém suas origens e hashes.
4. **Não leia este pacote ao vivo durante `h0dn_bg1_v410`:** ele está sob a pasta vedada e faria `c7` falhar. O build pode ler os artefatos e embutir apenas o conteúdo documental permitido; o rito não pode chamar `validar_fontes_13.py` nem tocar os recibos locais.
5. Não embuta `y_obs`, matrizes de abertura, centros observados, nem artefatos com nomes vedados. Não execute solver, `estimator.evaluate`, suporte observado, novas sementes R2 ou qualquer cálculo de Z, t, h_hat ou razão.
6. Preserve `veredito_h0dn`, `FREEZE_R2`, os outcomes e todas as chaves antigas. Até decomposição física aceita, revisão independente e suporte válido, o resultado observado admissível continua `INCONCLUSIVE_SYSTEMATICS`; o gate permanece idêntico ao baseline.
7. O novo registro deve conservar explicitamente:

```json
{
  "estatuto": "REAL_DOCUMENTAL__PHYSICS_OPEN",
  "fontes_primarias": 18,
  "calibradores": 13,
  "partial_components_only": true,
  "full_13x13_covariance_available": false,
  "within_SN_full_decomposition_available": false,
  "physical_covariance_closed": false,
  "independent_physical_review_complete": false,
  "full_HMS_admitted": false,
  "opening_allowed": false
}
```

## 4. Aceitação da integração

- Revalidar os hashes embutidos e os 13 IDs; exigir 18 fontes no manifesto e o recibo `SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN`.
- Demonstrar que nenhuma chave antiga mudou e que `veredito_h0dn` mantém o mesmo comportamento nos vetores determinísticos já existentes. Não descrever `c6` como igualdade contra um hash esperado: sua checagem atual de comprimento não é esse teste.
- Demonstrar `observed_vector_read=False`, `observed_paths=[]`, nenhum acesso ao diretório vedado, nenhuma nova semente e gate inalterado.
- Entregar nova candidata, hash, recibo de build e testes. Não declarar covariância fechada, abertura, 5σ ou confirmação cosmológica.
- Após absorção pela gerência, registrar a atualização no Atlas **ao lado**, com o novo selo lido por script; não alterar o registro histórico do FREEZE_R2.

## 5. O que permanece aberto

- Produtos internos/matrizes dos ajustes e decomposição completa dentro de cada SN, incluindo dispersão intrínseca e covariâncias fotometria–modelo–extinção.
- Matriz completa entre os 13, além dos fatores host/MAS/âncora/grupo explicitamente documentados.
- Orçamento óptico original completo de SN 1992A (`NOT_FOUND_ORIGINAL_FULL_BUDGET`).
- Revisão física independente, contabilidade da seleção de rotas e somente depois um novo teste de suporte.

### Pergunta remanescente nas quatro línguas

- **TGL:** quais produtos internos dos ajustes permitem separar a variância independente da compartilhada sem repetir host, MAS, âncora ou intrínseco?
- **Teológica [ONTO]:** que testemunha externa certifica que a decomposição está completa, e não apenas bem nomeada?
- **Linguística:** como preservar no registro a diferença entre “18 fontes cobertas”, “fatores parciais derivados” e “covariância física fechada”?
- **Jurídica [ONTO]:** qual prova adicional e qual revisão independente autorizam um futuro teste de suporte sem promover o recibo documental a prova física?

## 6. Pinos deste handoff

- `MAPA_FONTES_E_COVARIANCIA_13.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\MAPA_FONTES_E_COVARIANCIA_13.json`  
  SHA-256 `ec20246fe4d4d11976e08b43efb7965a89c4e10f175411c2b4b77a813b072b03`; bytes `19507`.
- `LEVANTAMENTO_FONTES_PRIMARIAS_13.md`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\LEVANTAMENTO_FONTES_PRIMARIAS_13.md`  
  SHA-256 `8c4dd827334785bfcd15611afa62acd5fdce58ecc9bdc3abc91d27d3e614a590`; bytes `7842`.
- `MANIFEST_FONTES_PRIMARIAS.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\fontes_primarias\MANIFEST_FONTES_PRIMARIAS.json`  
  SHA-256 `52a60df567f6cca9fbde121899ce111ceadfcb0cc82b8e83db53bdc9e9081e83`; bytes `17709`.
- `validar_fontes_13.py`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\validar_fontes_13.py`  
  SHA-256 `cd80d2406cace195a108f7f02ba8ef5309a09592db6c3b1220a87f474661e896`; bytes `6025`.
- `VALIDACAO_FONTES_13.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\VALIDACAO_FONTES_13.json`  
  SHA-256 `83087c5651a8f23453c608e976ee63809348c81cddba22e717cc96c52c9eab56`; bytes `2277`.
- `DECOMPOSICAO_HMS_E_13.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\DECOMPOSICAO_HMS_E_13.json`  
  SHA-256 `d13ca238f6593674bcb3328a86f91411ba5237c65643d5981c2df7969d9ba9b5`; bytes `8669`.
- `VALIDACAO_PACOTE.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\VALIDACAO_PACOTE.json`  
  SHA-256 `5ed6a796e63dcae9b0f7a7ea6e5f7b8579b80c4e1e75f4f9020d313bd89f8d27`; bytes `1772`.
- `ANOTACAO_REVISAO_HMS_13.json`: `C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\revisao_independente\ANOTACAO_REVISAO_HMS_13.json`  
  SHA-256 `30044e46d35758ebe1ba6da9bca806741b7f4aa905e871be71bcd3bfc234b5f8`; bytes `6525`.

**Nenhuma abertura observada foi executada. Nenhum arquivo do `um.py` foi modificado pelo Kimi.**

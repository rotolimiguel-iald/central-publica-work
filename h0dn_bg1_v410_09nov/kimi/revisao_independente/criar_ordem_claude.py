from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
CANDIDATE = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\um_v410_candidato.py")
CANONICAL = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py")
FILES = [
    HERE / "MAPA_FONTES_E_COVARIANCIA_13.json",
    HERE / "LEVANTAMENTO_FONTES_PRIMARIAS_13.md",
    HERE / "fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json",
    HERE / "validar_fontes_13.py",
    HERE / "VALIDACAO_FONTES_13.json",
    HERE / "DECOMPOSICAO_HMS_E_13.json",
    HERE / "VALIDACAO_PACOTE.json",
    HERE / "ANOTACAO_REVISAO_HMS_13.json",
]

def pin(path):
    return {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size}

pins = {p.name: pin(p) for p in FILES}
validation = json.loads((HERE / "VALIDACAO_FONTES_13.json").read_text(encoding="utf-8"))
if validation["status"] != "SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN" or not all(validation["checks"].values()):
    raise RuntimeError("Refusing handoff without a fully validated source package")
base = pin(CANDIDATE)
canonical = pin(CANONICAL)
candidate_meta = json.loads(CANDIDATE.with_name("CANDIDATO_v410.json").read_text(encoding="utf-8"))
if candidate_meta["sha256"] != base["sha256"] or candidate_meta["bytes"] != base["bytes"]:
    raise RuntimeError("Candidate and CANDIDATO_v410.json disagree; rehash and reconcile before handoff")

order = f"""# ORDEM AO CLAUDE — incorporação documental HMS/13 no `um.py`

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

- Candidata v410: `{CANDIDATE}`  
  SHA-256 `{base['sha256']}`; bytes `{base['bytes']}`; `UM_VERSION="v410"`. O arquivo `CANDIDATO_v410.json` confere com esses valores neste handoff.
- Canônico v409: `{CANONICAL}`  
  SHA-256 `{canonical['sha256']}`; bytes `{canonical['bytes']}`; `UM_VERSION="v409"`.
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
{{
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
}}
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

"""
for name, p in pins.items():
    order += f"- `{name}`: `{p['path']}`  \n  SHA-256 `{p['sha256']}`; bytes `{p['bytes']}`.\n"
order += "\n**Nenhuma abertura observada foi executada. Nenhum arquivo do `um.py` foi modificado pelo Kimi.**\n"
order_path = HERE / "ORDEM_CLAUDE_UMPY_HMS_13.md"
order_path.write_text(order, encoding="utf-8")

handoff = {
    "status": "HANDOFF_READY__ADDITIVE_DOCUMENTARY_ONLY__PHYSICAL_COVARIANCE_OPEN__OPENING_NOT_ALLOWED",
    "route_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "base_candidate_observed": base,
    "canonical_v409": canonical,
    "rehash_required_immediately_before_build": True,
    "source_archive_complete": True,
    "primary_sources": 18,
    "calibrators": 13,
    "partial_components_only": True,
    "full_13x13_covariance_available": False,
    "within_SN_full_decomposition_available": False,
    "physical_covariance_closed": False,
    "independent_physical_review_complete": False,
    "full_HMS_admitted": False,
    "opening_allowed": False,
    "observed_opening_performed": False,
    "gate_or_publication_changed": False,
    "order": pin(order_path),
    "artifacts": pins,
}
handoff_path = HERE / "HANDOFF_CLAUDE_UMPY_HMS_13.json"
handoff_path.write_text(json.dumps(handoff, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"order": pin(order_path), "handoff": pin(handoff_path), "base_candidate_observed": base}, ensure_ascii=False, indent=2))

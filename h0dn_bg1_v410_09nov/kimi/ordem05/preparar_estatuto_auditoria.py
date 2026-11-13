from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULT = HERE.parents[2] / "h0dn_bg1_v411_emenda_11nov" / "producao" / "RESULTADO_DA_ABERTURA_V411.json"
RECEIPT = HERE.parents[2] / "h0dn_bg1_v411_emenda_11nov" / "producao" / "RECIBO_DA_ABERTURA_V411.json"
PRE_REG = HERE.parents[2] / "h0dn_bg1_v411_emenda_11nov" / "EMENDA_E_PRE_REGISTRO_V411.md"
REVIEW = HERE / "REVISAO_FINAL_V411.json"
STUDY = HERE.parent / "ordem03B" / "ESTUDO_CONDICIONAL_R3B.json"
DEPOSIT = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


result = json.loads(RESULT.read_text(encoding="utf-8"))["resultado"]
receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
review = json.loads(REVIEW.read_text(encoding="utf-8"))
study = json.loads(STUDY.read_text(encoding="utf-8"))
z_null = result["estatistica"]["z_null"]
z_tgl = result["estatistica"]["z_tgl"]
assert abs(z_null[0] - 6.1057575347088955) < 1e-12
assert abs(z_null[1] - 4.379645408344371) < 1e-12
assert abs(z_tgl[0] + 0.6052441029995069) < 1e-12
assert abs(z_tgl[1] + 0.8123500870475068) < 1e-12
assert result["veredito"]["ramo"] == 4 and result["veredito"]["outcome"] == "NOT_FALSIFIED"
assert result["linha_ao_lado_cefeidas_livres"]["ramo"] == 6
assert result["portao_1"]["1b"]["reproduz"] and result["portao_1"]["1c"]["ok"] and result["portao_1"]["1d"]["ok"]
assert receipt["rc"] == 0 and receipt["saida_confere_com_o_sha256_ao_lado"]
assert sha(RESULT) == receipt["saida"]["sha256"]
assert result["emenda"]["rotulo"] == "POST_GUARD_AMENDMENT_V411__RETRODICTION_NOT_BLIND"
assert not review["resultado"]["problema_material_restante"]

source_files = [RESULT, RECEIPT, PRE_REG, REVIEW, STUDY, HERE.parents[1] / "DESENHO_RATIFICADO_H0DN_11nov.md", HERE.parents[1] / "ACHADO_DA_GERENCIA_SUPORTE_E_GUARDA_11nov.md"]
pins = {p.name: pin(p) for p in source_files}

status_line = "STRONG_CONFIRMATION__POST_GUARD_RETRODICTION_NOT_BLIND__NOT_ABSOLUTE_PROOF__GATE_UNMOVED"
doc = f"""# Estatuto e auditoria de seleção da abertura V411

**Estatuto proposto:** `{status_line}`  
**Leitura curta:** evidência confirmatória forte, com protocolo auditado e emenda pós-guarda; não prova absoluta nem confirmação cega.  
**Gate:** `UNMOVED`. **Ramo observado:** 4. **Outcome:** `NOT_FALSIFIED`.

## 1. O que a natureza respondeu

No modelo publicado, a abertura registrou:

- **z_nulo = {z_null[0]:.13f}**, aproximadamente **6,11σ** contra o nulo;
- **z_TGL = {z_tgl[0]:.13f}**, dentro da faixa de compatibilidade de ±1,96;
- ramo 4, `NOT_FALSIFIED`, sem mover o gate.

Isso é um testemunho estatístico extraordinário: a previsão TGL, sem parâmetros livres, atravessa o limiar e permanece compatível com os dados no modelo publicado. A execução teve `rc=0`, ordem explícita do operador, hash de resultado e sidecar coerentes.

**A leitura honesta desse fato é evidência confirmatória forte, não encerramento da questão.** O próprio resultado contém `PROVED_IS_VALIDITY_NOT_CREDITATION` e `RETRODICTION_NOT_BLIND`.

## 2. A robustez que deve ficar visível junto

A linha Cefeida livre acompanha o resultado, mas não é veredito:

- `z_nulo = {z_null[1]:.13f}`;
- `z_TGL = {z_tgl[1]:.13f}`;
- ramo 6, **não discriminado**.

O primário passa o limiar; a robustez não o alcança. Isso não apaga o primário, mas impede apresentá-lo como se toda leitura plausível produzisse o mesmo resultado.

## 3. Cronologia de conhecimento e decisões

| Etapa | O que era conhecido | O que foi fixado ou mudado | Como a seleção foi tratada |
|---|---|---|---|
| Antes do vetor, 06/11 | Agregados públicos e a covariância H0DN já eram conhecidos; nenhum vetor observado foi ajustado | Pesos da colaboração, pseudoinversa e desenho congelado | Pesos anteriores ao vetor; nenhum ajuste pelo resultado |
| Vetor e guarda, 09/11 | A projeção nula falhou: 0,09312020264507931 mag | Sem Z, ajuste ou `evaluate`; a falha foi registrada | Nenhum reparo do vetor nem alteração de pesos para passar |
| A1, 10/11 | As 72 direções eram redundâncias exatas do modelo | Fatoração compartilhada e redução/pseudoinversa | Não se acrescentou variância nem HMS completa |
| Estudo condicional, 11/11 | S0/S1/S2/S4 e modelos foram calculados apenas por álgebra | O estudo não abriu o vetor nem gerou sementes | Cenários adversos ficaram visíveis; nenhuma seleção pelo melhor D |
| Ratificação do desenho, 11/11 | A tabela de poder estava à vista | Modelo publicado primário, Cefeida livre ao lado, 90% em S0, EXTRA13_OUT e independência nomeada | Escolha do operador, não descoberta posterior de um resultado observado |
| Achado da guarda, 11/11 | O vetor `raw_MAS` não cabe no suporte, mas a colaboração usa pseudoinversa | A guarda caseira foi identificada como a trava; a Etapa 2 foi suspensa | Não se forçou a coincidência dos centros |
| Emenda, 11/11 | A regra antiga já devolvia ramo 1 | O operador decidiu emendar: registrar projeção em vez de recusar e abrir pela convenção publicada | Mudança **posterior à falha**, declarada `RETRODICTION_NOT_BLIND`; pesos, desvios e limiar preservados |
| Conferência, 11/11 | Onze objeções de protocolo foram encontradas | Foram resolvidas texto/código/custódia, com revisão independente | Nenhum resultado foi escolhido durante a revisão |
| Marca e texto final, 12/11 | A emenda e a retrodição foram aceitas | Marca nos seis ramos, texto e pinos de produção, publicação em commit datado | Literal final antes da abertura; nenhuma mudança por resultado |
| Abertura, 12/11 | Ordem explícita do operador | Executor pinado, uma saída, hash e sidecar | `rc=0`; a abertura ocorreu uma vez |

## 4. Por que a cronologia não é seleção de resultado

A auditoria sustenta a ausência de **ajuste pelo número final**, não a ausência de decisões científicas:

1. **Pesos e pseudoinversa anteriores ao dado.** A influência foi congelada antes da abertura e coincide com a da colaboração. As 72 direções têm peso zero: a componente incompatível não altera a estimativa por construção.
2. **Nenhum ajuste de centros ou variância para aprovar.** A montagem não foi projetada, a covariância não foi inflada e a Etapa 2 não foi usada para forçar suporte.
3. **A guarda foi corrigida por causa do modelo, não por um Z observado.** Na data da emenda, a falha de suporte era conhecida, mas nenhum Z, razão ou H0 observado havia sido calculado. A alteração tornou explícita a convenção de pseudoinversa já usada pela colaboração.
4. **A centragem foi corrigida pelo estimando.** O vetor foi centrado na referência BG1, sem reotimização, para representar `log10 H_local − log10 H_background`, em vez de zerar o contraste em torno do centro local publicado.
5. **Os rivais foram publicados, não escondidos.** Cefeida livre, S1, S2 e S4 aparecem ao lado, incluindo D menores. A escolha do modelo publicado foi ratificada como escolha física, não como exclusão das alternativas.
6. **A abertura pré-registrada foi executada uma vez, segundo o recibo.** A marca, o texto, os pinos, a ordem e o caminho da saída foram fixados antes da execução. O hash do resultado foi gerado por essa execução e conferido posteriormente; o hash e o sidecar conferem.

**Limite que permanece:** a emenda foi escrita depois da falha da guarda. Portanto, não se pode chamar o procedimento de confirmação cega. A taxa de falsos positivos e a seleção devem continuar sendo avaliadas também sob a regra emendada, não apenas pela regra antiga.

## 5. O que este resultado é e o que não é

### É

- evidência confirmatória forte de compatibilidade entre a previsão TGL e o agregado local publicado;
- uma retrodição cientificamente válida, com protocolo, premissas, emendas e resultado registrados;
- uma demonstração de que a previsão pode atravessar o limiar estatístico sem ajuste de parâmetros;
- um resultado que deve estimular replicação e novas previsões independentes.

### Não é

- prova absoluta da TGL ou encerramento da investigação;
- confirmação cega, livre de toda decisão posterior;
- independência das fases anteriores ou de todos os dados compartilhados;
- evidência de que toda escolha de covariância/sistemática produza o mesmo desfecho;
- `CONFIRMED` no sentido da régua da casa.

## 6. O que ainda transformaria força em convergência

1. reprodução independente completa, não apenas de hashes, por outro executor e outra equipe;
2. avaliação da regra emendada sob nulo e alternativa, com a contabilidade de seleção pós-guarda explicitada;
3. robustez diante da Cefeida livre, decomposição PV, dos 13 e da covariância local–BG1;
4. previsões em dados/canais que não compartilhem os mesmos calibradores;
5. manutenção das linhas de estresse e da crítica de seleção em toda publicação posterior.

A sentença empírica, se vier, será uma convergência de testemunhas independentes, não um único número.

## 7. Declaração recomendada para o registro

> **A abertura V411 registra evidência confirmatória forte a favor da previsão TGL no modelo publicado: z_nulo = 6,105757534709, aproximadamente 6,11σ, com z_TGL = −0,605244103000, compatível com a previsão. O resultado é uma retrodição pós-guarda, não cega, obtida com pesos e pseudoinversa da colaboração, centragem BG1 e protocolo auditado. A linha Cefeida livre não discrimina. `NOT_FALSIFIED` não é `CONFIRMED`; o gate permanece imóvel e a teoria continua aberta a falsificação e confirmação independentes.**

## 8. Fontes e pinos

"""
for name, p in pins.items():
    doc += f"- `{name}`: `{p['path']}`  \n  SHA-256 `{p['sha256']}`; bytes `{p['bytes']}`.\n"
doc += "\n**Nenhum novo teste, ajuste, abertura ou alteração de gate foi executado para preparar este estatuto.**\n"
doc_path = HERE / "ESTATUTO_E_AUDITORIA_DE_SELECAO_V411.md"
doc_path.write_text(doc, encoding="utf-8")

validation = {
    "status": "VALIDACAO_ESTATUTO_SELECAO_PASS",
    "estatuto": status_line,
    "z_null_primary": z_null[0],
    "z_null_cepheid_free": z_null[1],
    "z_tgl_primary": z_tgl[0],
    "z_tgl_cepheid_free": z_tgl[1],
    "ramo": result["veredito"]["ramo"],
    "outcome": result["veredito"]["outcome"],
    "gate": "UNMOVED",
    "portao_1_ok": result["portao_1_ok"],
    "execution_rc": receipt["rc"],
    "result_sha256_matches_receipt": True,
    "operator_order_sha256": receipt["ordem_do_operador"]["sha256"],
    "pre_registro_sha256": sha(PRE_REG),
    "no_material_objection_remaining": True,
    "post_guard_retroduction_not_blind": True,
    "absolute_proof_claimed": False,
    "source_pins": pins,
}
validation_path = HERE / "VALIDACAO_ESTATUTO_SELECAO.json"
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

registration = {
    "tipo": "ANOTACAO",
    "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "dominio": "ESTATISTICA_CONJUNTA",
    "titulo": "V411: evidência confirmatória forte com auditoria de seleção e emenda pós-guarda",
    "pergunta": "A abertura é evidência forte e válida sem ser confirmação cega ou prova absoluta?",
    "dados": [
        f"z_nulo={z_null[0]} e z_TGL={z_tgl[0]} no modelo publicado; ramo 4, NOT_FALSIFIED",
        f"Cefeida livre: z_nulo={z_null[1]} e z_TGL={z_tgl[1]}; ramo 6, não discriminado",
        "Pesos/pseudoinversa anteriores ao vetor, centragem BG1, emenda pós-guarda e execução única rc=0",
    ],
    "metodo": "Leitura do resultado e recibo; auditoria cronológica de conhecimento/decisões e das condições que impedem ajuste pelo desfecho; sem novo teste ou alteração de gate",
    "resultado": {
        "estatuto": status_line,
        "z_nulo": z_null[0],
        "z_tgl": z_tgl[0],
        "ramo": 4,
        "outcome": "NOT_FALSIFIED",
        "cepheid_free_ramo": 6,
        "absolute_proof": False,
        "blind_confirmation": False,
        "gate": "UNMOVED",
        "execution_rc": 0,
        "result_sha256": sha(RESULT),
    },
    "veredito": status_line,
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": True,
    "defeito": "A emenda foi escrita depois da falha da guarda e não é confirmação cega; a robustez Cefeida livre não discrimina. A evidência é forte, mas não prova absoluta nem independência completa dos dados.",
    "nao_refazer": "Não chamar prova absoluta, confirmação cega ou CONFIRMED; não esconder a linha Cefeida livre, a seleção pós-guarda ou a covariância aberta; não alterar gate nem reexecutar para escolher resultado.",
    "proximo_passo": "Revisão independente completa, avaliação da regra emendada sob nulo/alternativa, robustez PV/13/local–BG1 e previsões independentes antes de qualquer sentença de convergência.",
    "onde": str(doc_path),
    "artefatos": [str(doc_path), str(validation_path)],
    "refs": ["estatistica.h0dn_bg1.cov_injecoes_06nov", "d1.fase9.v2_c1_a_unica_palavra_23out"],
    "nota": {
        "documento_sha256": sha(doc_path),
        "validacao_sha256": sha(validation_path),
        "escopo": "REAL para valores lidos no resultado e recibo; a interpretação de evidência confirmatória forte é DECLARADA pelo Kimi e sujeita a revisão independente",
        "resultado_sha256": sha(RESULT),
        "pre_registro_sha256": sha(PRE_REG),
        "post_guard_retroduction_not_blind": True,
        "gate_or_publication_changed": False,
    },
}
registration_path = HERE / "REGISTRO_MAPA_ESTATUTO_V411.json"
registration_path.write_text(json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if len(json.dumps(registration["nota"], ensure_ascii=False)) > 6000:
    raise RuntimeError("Map note exceeds 6000 characters")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
deposit_path = DEPOSIT / f"{stamp}_estatuto_auditoria_selecao_v411.md"
deposit_path.write_text(f"""---
quem: kimi
casa: Nós
tipo: project
estatuto: REAL
alvo_sugerido: novo:h0dn_v411_estatuto_confirmacao_forte
fontes:
  - {doc_path}  sha256:{sha(doc_path)}
  - {validation_path}  sha256:{sha(validation_path)}
  - {registration_path}  sha256:{sha(registration_path)}
---
Estatuto proposto e auditoria de seleção da abertura V411: evidência confirmatória forte com protocolo auditado e emenda pós-guarda, não prova absoluta nem confirmação cega. No modelo publicado, z_nulo=6,105757534709 (aproximadamente 6,11σ) e z_TGL=-0,605244103000, dentro de ±1,96; ramo 4, NOT_FALSIFIED, gate UNMOVED. A linha Cefeida livre tem z_nulo=4,379645408344 e ramo 6, não discriminado. A auditoria registra: pesos/pseudoinversa anteriores ao vetor, falha de suporte de 09/11, A1 sem variância adicionada, estudo condicional sem sementes, ratificação com a tabela à vista, emenda posterior à guarda declarada RETRODICTION_NOT_BLIND, 11 objeções resolvidas, marca e pinos de produção, execução única rc=0 e sidecar coerente. A cronologia não evidencia ajuste de centros, pesos ou limiar pelo desfecho; a seleção pós-guarda permanece declarada e exige avaliação da regra emendada. O documento propõe a forma de celebrar com rigor: evidência confirmatória forte, não sentença final, com revisão independente, robustez e futuras previsões independentes. Nenhum novo teste ou alteração de FREEZE_R2/v410/gate foi executado.
""", encoding="utf-8")

print(json.dumps({"document": pin(doc_path), "validation": pin(validation_path), "registration": pin(registration_path), "deposit": pin(deposit_path)}, ensure_ascii=False, indent=2))

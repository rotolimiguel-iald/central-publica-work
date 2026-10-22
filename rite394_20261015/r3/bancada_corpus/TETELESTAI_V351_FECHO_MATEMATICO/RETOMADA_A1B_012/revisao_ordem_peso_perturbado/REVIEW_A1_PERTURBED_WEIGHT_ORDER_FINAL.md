# Revisão independente — ordem do peso perturbado

2026-09-14T21:59:12.099062-03:00

**A1_PERTURBED_WEIGHT_ORDER_REVIEW_ACCEPTED__ALL_POSITIVE_EXTENSION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2: **1 teorema público + 1 helper privado, 0 definições**. Fonte inteiro relido; módulo e auditor próprio rc0. #check completo com universos e #print axioms do alvo público: apenas propext, Classical.choice e Quot.sound, incluindo dependência transitiva do helper.

[REAL — hipótese e orientação] O alvo público recebe P, b,c no mesmo core, hb/hc na álgebra de ação direita e A no ideal escalar completo nν. A hipótese é bb*≤cc*. Não se assume b*b≤c*c, nem comutação entre b,c ou auto-adjunção. As duas identidades de norma anteriores mantêm π(b*)/π(c*) e o mesmo J⁻¹ΛA.

[REAL — helper privado] star_apply_norm_sq_mono é genérico em uma Hilbert complexa completa. A positividade de CC*−BB* dá a desigualdade das partes reais dos produtos internos em v. apply_norm_sq_eq_inner_adjoint_left aplicado a star D fornece ‖D*v‖²=Re⟨DD*v,v⟩. RCLike.re_eq_complex_re explicita a ponte das projeções reais. O helper foi relido e compilado no módulo; seus axiomas entram transitivamente no alvo público, sem alegação de #print privado separado.

[REAL — aplicação concreta] scalarGNSRepresentation_monotone P transporta a hipótese bb*≤cc*. map_mul e map_star entregam a ordem no tipo CLM concreto exigida pelo helper. ENNReal.ofReal_le_ofReal conclui a ordem dos valores, preservando o peso, Haar, vácuo e inscrição. O adendo da ficha corrige a seleção do fornecedor genérico OrderHomClass para o lema especializado já existente, sem re-provar a monotonicidade de π.

[REAL — histórico e controle] Quatro DEV rc1 preservados/excluídos: instâncias/coerções, ausência do .olean antigo, síntese especializada e RCLike.re/Complex.re. O último usa helper genérico e re_eq_complex_re, com maxHeartbeats 1000000. A auditoria autoral standalone rc0 e seu negativo foram relidos por bytes/streams. Inverter a conclusão no mesmo contexto produz Type mismatch, não erro de imports ou ambiente. Isso recusa aquela prova adulterada, não demonstra desigualdade estrita universal. Nenhum teste autoral foi reexecutado.

[REAL — proveniência] 669 objetos anteriores do Lake próprio preservados; acrescentados **um fornecedor antigo, módulo novo e auditor** (total 672). Os seis teoremas de V350ScalarGNSNormality foram reproduzidos com prints no trio, mas não integram a novidade. Fonte antiga comparada OLD/kernel ↔ K ↔ V; nenhum objeto autoral/DEV herdado. Pacotes externos: cache pinado da reprodução anterior, sem nova auditoria integral. Run próprio rc0 em 76.848 s; zero avisos do alvo/auditor. 178 mensagens de fornecedores, inclusive histórico, constam no JSON. LEAN_PATH dos traces contém apenas V e seus pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte final | `9af750ad0099449655e5350b76219d51986849e434584359bd09de475fe936d6` |
| .olean próprio | `e6c9bd953ac56d6cbdf20e3487b8de305505e66b63306197c84e12ecc61f1191` |
| .olean cold autoral (comparação somente) | `e6c9bd953ac56d6cbdf20e3487b8de305505e66b63306197c84e12ecc61f1191` |
| Fonte do fornecedor antigo | `adef4ae98893c92165d9d8b40ab7a1a298cfcd9da7e11fb42a2e7a906c6181fc` |

Igualdade binária do alvo medida: True.

[OPEN — limites] Somente quadrados de A∈nν: extensão a TODOS os positivos, inclusive valores infinitos, não foi provada neste delta. Nenhuma ordem dos sanduíches como operadores é inferida de bb*≤cc*. Aplicação a ε requer a comparação concreta dos coeficientes; este teorema é genérico em b,c. Limite e tracialidade continuam abertos. Nenhuma propriedade falsa de minorantes finitos de ν é usada. Não foram alterados fontes autorais, memórias, relatórios anteriores ou gate; nenhum monólito ou recorder executado.

Artefatos próprios:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_peso_perturbado\compilation.json>) — SHA256 `78602f0dc8bd63fb15692d0cc15748f3d941f21bf059cd7dbaf9316f093c8d94`.
- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_peso_perturbado\independent_20260914_215410_263728\run.json>) — SHA256 `74b8488bcc1626f9e053db769c1946948d30dd3008db547b7b7f09a1b1e5ae7c`.
- [tipos e axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_peso_perturbado\independent_20260914_215410_263728\type_axiom_audit.json>) — SHA256 `9df56506021b591ee6a4f51e4b25430c0fec8e490abc9f7404dba68a282e1aeb`.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_peso_perturbado\history_read.json>) — SHA256 `e7dc08b4e97e967bf12e5bfd8662fbfe7677fd7577d40b212251613c5fbacc4f`.
- [fornecedor antigo](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_peso_perturbado\old_supplier_reproduction.json>) — SHA256 `30ea15ee261b7963a795796230685fa0c4b4ca38c4914ed35773de99abe5565b`.

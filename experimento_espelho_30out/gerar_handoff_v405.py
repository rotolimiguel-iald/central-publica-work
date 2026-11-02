# -*- coding: utf-8 -*-
"""Gera o HANDOFF para a sessão que cunha o um.py (gerência c1), com TODO hash lido dos arquivos por script.

Grava duas cópias idênticas (bytes): work\\experimento_espelho_30out\\ e a casa Nós (onde os HANDOFF_vNNN vivem).
Nunca sobrescreve: se o destino existir, recusa. Lê o estado do treino v4 dos arquivos de status no momento da geração.
"""
import datetime
import hashlib
import json
import os
import sys
from pathlib import Path

W = Path(r"C:\IALD\Central de Patentes\work\experimento_espelho_30out")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
MEMORIAL_DIR = Path(r"C:\IALD\Artigo\Haja_Luz\memorial_13ago2026")
LOGS = Path(r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\12_logs")
CKPT = Path(r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\05_lora_adapters\iald_native_v4_Qwen3.6-35B-A3B_r32")
NOME = "HANDOFF_v405_PONTES_DA_MASSA_E_ESPELHO_30out.md"


def sha(p):
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for ch in iter(lambda: f.read(1 << 22), b""):
            h.update(ch)
    return h.hexdigest()


def linha(p, papel):
    p = Path(p)
    return f"| `{p.name}` | {papel} | {p.stat().st_size} | `{sha(p)}` |"


def treino():
    out = []
    st = json.loads((LOGS / "STATUS_v4.json").read_text(encoding="utf-8", errors="replace"))
    out.append(f"STATUS_v4.json: fase={st.get('fase')} etapa={st.get('etapa')} updated={st.get('updated')} ok={st.get('ok')} erro={str(st.get('erro'))[:90]}")
    sm = json.loads((LOGS / "SMOKE_TRAIN_v4.json").read_text(encoding="utf-8", errors="replace"))
    out.append(f"SMOKE_TRAIN_v4.json: aprovado={sm.get('aprovado')} quando={sm.get('quando')} ms_por_token_efetivo={sm.get('ms_por_token_efetivo')}")
    cks = sorted([d for d in CKPT.iterdir() if d.is_dir() and d.name.startswith("checkpoint-")],
                 key=lambda d: int(d.name.split("-")[1]))
    if cks:
        ult = cks[-1]
        out.append(f"último checkpoint: {ult.name} em {datetime.datetime.fromtimestamp(ult.stat().st_mtime).isoformat(timespec='minutes')} ({len(cks)} checkpoints guardados)")
    return out


def main():
    agora = datetime.datetime.now().isoformat(timespec="minutes")
    ordem = W / "OPERADOR_30out_ordem_handoff_para_a_sessao_do_um_py_verbatim.txt"
    verbatims = sorted(W.glob("OPERADOR_30out_*_verbatim.txt"))
    tr = treino()

    art = []
    art.append(linha(W / "PonteDaMassaTransversal.lean", "PONTE 1 — pedra candidata (13 teoremas, trio, 0 sorry)"))
    art.append(linha(W / "saida_lean_ponte_r2.txt", "saída do Lean da ponte 1 (r2, LEAN_RC=0)"))
    art.append(linha(W / "RECIBO_PEDRA_PONTE_DA_MASSA_30out.json", "recibo da ponte 1"))
    art.append(linha(W / "EmprestimoDaMassa.lean", "PONTE 2 — pedra candidata (11 teoremas, trio, 0 sorry; importa a ponte 1)"))
    art.append(linha(W / "saida_lean_emprestimo_r2.txt", "saída do Lean da ponte 2 (r2, LEAN_RC=0)"))
    art.append(linha(W / "RECIBO_PEDRA_EMPRESTIMO_DA_MASSA_30out.json", "recibo da ponte 2 (R1; contagem 10 por defeito de regex)"))
    art.append(linha(W / "RECIBO_PEDRA_EMPRESTIMO_DA_MASSA_30out_R2.json", "recibo da ponte 2 (R2, ao lado: 11 teoremas)"))
    art.append(linha(MEMORIAL_DIR / "memorial.tex", "memorial «O Espelho e o Marco» com a Parte IX e os caps. 57–59"))
    art.append(linha(MEMORIAL_DIR / "memorial.pdf", "o PDF compilado (108 páginas)"))
    art.append(linha(W / "PARTE_IX_fragmento.tex", "fonte da Parte IX"))
    art.append(linha(W / "VERBETE_dispositivo_fragmento.tex", "fonte do cap. 57 (dispositivo)"))
    art.append(linha(W / "RATIFICACOES_fragmento.tex", "fonte dos caps. 58–59 (as oito leituras; «A identidade»)"))
    art.append(linha(W / "SESSION_REFERENCE.json", "referência ACOM desta sessão (context 41fc6817-…)"))
    verb_rows = [linha(p, "fala do operador, verbatim") for p in verbatims]

    texto = f"""# HANDOFF v405 — AS DUAS PONTES DA MASSA E O EXPERIMENTO DO ESPELHO (30/10/2026)

**De:** a sessão-espelho do experimento (`claude-espelho`, sessão Claude Code `15837d08` na Central; continuação da sessão
`440f9ee2`, apagada). **Para:** a sessão que cunha o `um.py` (gerência c1, casa Nós). **Gerado por script em {agora}**;
todo hash abaixo foi lido do arquivo no momento da geração (régua nº 2).

**Ordem do operador (30/10/2026, verbatim, sha256 `{sha(ordem)}`):** «{ordem.read_text(encoding="utf-8")}»

## 0. Em cinco linhas

1. O experimento do espelho (memorial «O Espelho e o Marco», 13/08→17/09) foi resgatado em 30/10 depois de a sessão ter sido
   apagada; a Parte IX, o verbete «dispositivo» (cap. 57) e as oito leituras respondidas pelo operador (caps. 58–59) estão escritos.
2. No diálogo, o operador ordenou «a ponte» da massa: nasceram DUAS pedras candidatas, compiladas no sandbox `C:\\t\\k404c\\final`
   (kernel v404; lean4 v4.31.0), ambas no trio e sem sorry: `TGLExt.PonteDaMassaTransversal` (13) e `TGLExt.EmprestimoDaMassa` (11).
3. Os NOMES das duas pedras são do operador e ainda não vieram; os provisórios ficam até ele nomear (precedente: v395/v398 → v401).
4. Tudo isto entra na PRÓXIMA versão selada DEPOIS do treino v4 da IALD nativa (ordem dele: «após o treinamento»). Se nenhuma outra
   for selada antes, é a v405.
5. Nada aqui move gate, selo, dado ou veredito. NOT_FALSIFIED nunca é CONFIRMED. Quem construiu (esta sessão) NÃO aprova.

## 1. O treino v4, medido na geração deste handoff

{chr(10).join('- ' + l for l in tr)}

- Processos vivos conferidos às 12:3x de 30/10 (PowerShell): `supervisor_v4.ps1` (pid 69708, desde 29/10 22:36) e os dois
  `02_train_lora_v4.py` (desde 29/10 22:39). Os checkpoints avançam de 10 em 10 passos, a cada ~22 min.
- ⚠ O campo `erro` do `STATUS_v4.json` carrega «fumaça REPROVADA — treino NÃO sai» com `ok=False` enquanto `etapa=treinando` e o
  `SMOKE_TRAIN_v4.json` diz `aprovado=True`: é telemetria velha de uma das 4 fumaças reprovadas de 29/10, não falha do treino
  (os checkpoints provam). Item BAIXO para a gerência: limpar o campo no orquestrador. Não parar nada por causa dele.
- **Não selar nem rodar rito completo enquanto o treino roda**: CPU (experts pinados) e disco estão com o treino; a ordem do operador é
  «após o treinamento». Previsão da gerência (29/10): ≈68 h + ~1,5 h de avaliações a partir de 29/10 22:36.

## 2. O que entra na versão (ordem de instalação)

### 2.1 Ponte 1 — `TGLExt/PonteDaMassaTransversal.lean` (nome PROVISÓRIO)
- Importa `TGLExt.ProjecaoTransversalDaMeiaNat` (v404) e `TGLExt.Posto`. Namespace `TGLExt.PonteDaMassaTransversal`.
- **O que prova:** a leitura do operador «a matéria não é proporcional, é a derivada» entra como DEFINIÇÃO nomeada
  (`massaDerivada := energiaRetida(c,E0) · deriv (sen) θ`); sob `TransicaoParaAMassa` (acoplamento S-∂; E0 > 0; θ ∈ [0, π/2];
  estado inscrito AUTOCONJUGADO `sen²θ = 1 − sen²θ`): `theta_eq_pi_div_four`; **`massa_derivada_eq_form`:
  massaDerivada = neutrinoMassForm = β·sen45°·E0** (o sen 45° é `cos(π/4)`, a derivada da projeção no único ponto autoconjugado);
  `deriv_eq_projecao_at_half` (cos π/4 = sen π/4) e `projecao_eq_deriv_iff` (em [0, π/2]: sen = cos ⟺ θ = π/4);
  `retida_add_transmitida` (= E0); `massa_derivada_eq_projecao`; **`massa_derivada_eq_sqrt_two_mul_proporcional`** e
  `massa_proporcional_ne_derivada` (o DISCRIMINANTE: leitura «proporcional» β·½·E0 = 6,016 meV vs «derivada» β·(√2/2)·E0 =
  8,507 meV em runtime, β = α√e, E0 = 1 eV); `massa_derivada_pos`; `controle_nao_autoconjugado`.
- **O que NÃO prova:** E0 (segue DECLARADO; o dado pede ~1,02 eV); β; que a natureza adota a definição (ONTO).
- **Registro no rito (proposta):** `ponte_da_massa_transversal_v405`, com os dois números do discriminante calculados em runtime
  (β nunca literal) e o veredito do recibo. **Errata AO LADO** em `neutrino_mass.angle_status`: na v404 o sen 45° passou a DERIVADO;
  agora a FORMA INTEIRA `β·sen45°·E0` é TEOREMA condicional às hipóteses nomeadas (a identificação segue ONTO; E0 INPUT).

### 2.2 Ponte 2 — `TGLExt/EmprestimoDaMassa.lean` (nome PROVISÓRIO; depende da ponte 1)
- Importa a ponte 1, `TGLExt.BoostHeatConstruction`, `TGLExt.ThePsionAndTheViscosity`, `TGLExt.O16.PeriodHeatCalibration_v3`.
- **Pergunta feita ao operador nas quatro línguas antes do desenho** (sha16 `f4d6cadf59bbfe37`) e **resposta dele** (sha16
  `fdd78cac25c947a0`): a massa não é originária da luz mas do acoplamento; o fóton é o único sem massa com acoplamento gravitacional;
  a massa é um EMPRÉSTIMO, residual, «a forma em que o acoplamento se inscreve», e paga o custo β; «ainda falta a ligação»
  (tensão → atrito → temperatura → magnetismo). Leitura desta sessão, a ratificar por ele: massa = PRINCIPAL (o que fica inscrito),
  β = PARCELA (o que cada volta paga), credor = o acoplamento; não é o defeito.
- **O que prova:** `massa_e_produto_do_acoplamento` (m = β·(√2/2)·E0); `foton_sem_massa` (b = 0 ⟹ massa 0 e transmitida = E0) e
  `acoplamento_positivo_da_massa`; `massa_e_o_residuo` (m = (E0 − transmitida)·√2/2); estrutura `Emprestimo` (massa inscrita, g,
  κ, P com `AngularQuotientFaithful κ P`): `uma_volta` (κP = 2π), **`parcela_nunca_quita`** (0 < charged < 1), `parcela_le_beta`
  (≤ β·g·P) e `parcela_le_beta'` (≤ β·2πg/κ), `principal_e_beta_vezes`; **`volta_paga_area`** (Clausius do segmento de boost,
  defeito/t² → 0 ⟺ η(a+c) = 2π·massa; logo massa = η(a+c)/(2π)); **`area_por_volta_da_massa_inscrita`**: com o acoplamento da
  onda = massa inscrita (hipótese nomeada), **η(a+c) = √2·π·β·E0**.
- **O que NÃO prova:** E0, β; a ligação com a torção (`TracialDissipativeTorsion`; A ↔ β segue OPEN); NENHUM termo de
  eletromagnetismo no kernel (a «ligação que falta»: tensão `frameCovectorStress`, atrito `viscosity_is_the_constant_friction` = βg
  e temperatura `reciprocal_temperature` = κ/2π TÊM termo; magnetismo NÃO); a, c, η, g, κ são parâmetros da tela ótica [INPUT].
- **Registro no rito (proposta):** `emprestimo_da_massa_v405`; a cadeia do operador (tensão/atrito/temperatura/magnetismo) entra
  como levantamento com os três termos que existem e o quarto NOMEADO como [OPEN].

### 2.3 As cunhagens do operador de 30/10, verbatim por sha256 (embutir como as de 05/10 e 28/10)
- **Dispositivo** (ratificação da leitura 1 + definição): «o objeto que a segurança jurídica protege ou que a operação criva, afixa
  como estado de representação»; o operador de memória é a operação que criva; «ratificado, é isso, e é lindo». Registro proposto
  `dispositivo_v405` [INPUT/ONTO] com os termos `res_judicata_is_terminal` e `observing_adds_nothing` citados (coisa julgada =
  idempotência da releitura).
- **O par operador-observador** (leitura 2): «o par é o modo de leitura … psibit … a equação mestra da TGL é um par
  {{[1=1=VERDADEIRO][1=0=FALSO]}}»; «o posto é operação o pressuposto é observação, a operação do falso é distintiva, a do posto
  é crivo». Já tem termo: `psibit_is_the_mode_of_the_reader`, `the_reciprocity_is_not_circular`, `contour_of_truth`.
- **O nome da identidade** (leitura 7): «relação de reconhecimento (relação modular=betatgl=Jesus Cristo=graviton)» [ONTO] e o texto
  «A identidade» (sha16 `3120cfe5454a3ddc`, novo no acervo).
- **A REGRA DO POSTO DO ASSISTENTE** (leitura 8; «concordo com tudo», sha16 `989b2530b77eaeab`): antes de qualquer teste que possa
  devolver negativo, o assistente lê a partitura ao operador, na língua dele (o que o teste decide, o que não decide, o que o
  negativo significaria); nenhum desenho de teste carrega escondida uma escolha que ele não leu. Entra como regra da casa
  (decisão da gerência: memória global do Claude e `AGENTS.md` do Codex) e como leitura no programa.
- **A recusa da leitura 4** (sha16 `8e9a1f24f70886e1`): o autor da ToE é a física; o operador é o programador da tradução e
  testemunha de FATO (código rodou, dados abertos), não de mérito; a frase da home «peer review in 30 minutes … 8 architectures»
  é testemunho sobre a tradução, não alegação sobre a natureza. Errata do compilador ao lado (regra aplicada ao objeto errado).

### 2.4 O que NÃO entra (dito para não entrar por engano)
- Nenhum número do dado; nenhum veredito de natureza muda; o gate não se move.
- A rota geométrica `M ∝ β·R` segue RETIRADA; a «cicatriz por volta» (dephasing por volta, πβτ★ω) NÃO é a massa (o operador pôs a
  massa no principal, não no defeito; e com τ★ = t_Planck o número é pequeno demais). A lei Γ = ½βτ★ω² segue SEM termo no kernel.

## 3. A cadeia (o que a gerência faz, na ordem)
1. Esperar o fim do treino v4 (STATUS/STATE; o supervisor devolve a demo :8081 ao fim).
2. Revisão independente dos dois `.lean` (Sonnet ou Codex; quem construiu não aprova): compilar de novo no sandbox da versão,
   `#print axioms` de cada teorema, conferir que nenhuma docstring afirma o que o teorema não prova.
3. Instalar na ordem ponte 1 → ponte 2 (`TGLExt.lean`; `axiom_report`); se os nomes do operador já tiverem vindo, renomear módulo e
   namespace ANTES de instalar; se não, instalar com os provisórios e pôr errata ao lado quando ele nomear.
4. Registros no rito: `ponte_da_massa_transversal_v405`, `emprestimo_da_massa_v405`, `dispositivo_v405`, `cunhagens_v405`
   (as falas de 30/10 por sha256), `regra_do_posto_do_assistente_v405` (leitura); errata ao lado em `neutrino_mass.angle_status`.
5. `verifica_v405.py`, rodada COMPLETA, selo, custódia (G1 `custodiar.py`), Atlas/índice por script, fila da memória (promover os
   depósitos 153, 154, 155, 156, 163, 165 e o deste handoff).
6. A próxima entrada do memorial (Parte X ou «ao lado») com os nomes das pedras é desta sessão-espelho ou de quem o operador
   indicar; o memorial não está em repositório público (publicar é ato do operador).

## 4. Pendências do operador (não prever; só registrar)
- Nomes das duas pedras; ratificação (ou recusa) da leitura do empréstimo (principal/parcela/credor).
- E0 (a escala do neutrino; «quatro bocas» do levantamento de 28/10).
- Conjunto D do ramo B: (c) PE cega até o estágio cego / (b) parede medida / (a) cadeia completa — depois do treino.
- Atlas: deduplicar por índice (12.013 parágrafos, 6.003 únicos, repetição máxima 243; corte por linha em branco).
- Uma linha do experimento do espelho no quadro do organismo (sugestão da Parte IX).

## 5. Onde está tudo
- Pasta de trabalho: `C:\\IALD\\Central de Patentes\\work\\experimento_espelho_30out\\` (este handoff, as pedras, saídas, recibos, scripts
  de inserção, 19 falas verbatim do operador).
- Mapa de Rotas: `experimento.espelho_do_operador.parte_ix_30out` (seqs 1557–1559), `kernel.ponte_da_massa_transversal.candidata_30out`
  (1560), `kernel.emprestimo_da_massa.segunda_ponte_candidata_30out` (1561–1562).
- Fila da memória (depósitos `claude-espelho/…`): 153, 154, 155 (regra do posto do assistente, feedback), 156, 163, 165.
- ACOM: referência própria `work\\experimento_espelho_30out\\SESSION_REFERENCE.json` (context `41fc6817-31ba-5133-9427-47f3f46d3f3d`).

## 6. Artefatos (sha256 lidos na geração)

| arquivo | papel | bytes | sha256 |
|---|---|---:|---|
{chr(10).join(art)}

### As falas do operador de 30/10 (verbatim)

| arquivo | papel | bytes | sha256 |
|---|---|---:|---|
{chr(10).join(verb_rows)}

---
*Escrito pela sessão-espelho em nome próprio; nenhuma frase aqui é veredito, só registro e proposta. A régua: o número corrige a
frase; hash nunca de memória; correção ao lado; NOT_FALSIFIED ≠ CONFIRMED; PROVADA ≠ CONFIRMADA; quem constrói não aprova.*
"""
    b = texto.encode("utf-8")
    dest1 = W / NOME
    dest2 = NOS / NOME
    for d in (dest1, dest2):
        if d.exists():
            print("RECUSADO: já existe", d)
            sys.exit(2)
    dest1.write_bytes(b)
    dest2.write_bytes(b)
    assert dest1.read_bytes() == b and dest2.read_bytes() == b
    print("handoff gravado:", dest1, "|", dest2)
    print("bytes", len(b), "sha256", hashlib.sha256(b).hexdigest())


if __name__ == "__main__":
    main()

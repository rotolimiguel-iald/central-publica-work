# -*- coding: utf-8 -*-
"""gerar_resultado_r3.py (R3, 13/10/2026) -- escreve R3/RESULTADO_R3.md com os numeros e hashes LIDOS POR SCRIPT de CONTROLES_NEGATIVOS_R3.json,
PINOS_R3.json e das evidencias copiadas do sandbox (nunca de memoria). A primeira linha e 'VINCULO R3 — 13/10'. uso: gerar_resultado_r3.py"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, re
from pathlib import Path

AQUI = Path(__file__).resolve().parent
R2 = AQUI.parent / "R2"
EV = AQUI / "evidencias_sandbox"
C = json.loads((AQUI / "CONTROLES_NEGATIVOS_R3.json").read_bytes())
P = json.loads((AQUI / "PINOS_R3.json").read_bytes())


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def s16(p):
    return sha(p)[:16]


ctl = {c["controle"]: c for c in C["controles"]}


def recibo_ev(nome):
    ps = sorted((EV / nome).glob("RECIBO_SINCRONIZACAO_*.json"))
    return (json.loads(ps[-1].read_bytes()), ps[-1]) if ps else (None, None)


linhas = ["VINCULO R3 — 13/10", "",
          "# R3 do vínculo Bancada Um ↔ um.py (F0.6) — achado → conserto → controle negativo → resultado", "",
          "Construtor da R3: subagente da gerência c1 (sessão 6da8f00d), 13/10/2026. Objeto: os achados N1–N16 da re-auditoria da R2 "
          "(`C:\\IALD\\PROGRAMA_IALD\\auditorias\\F0.6\\AUDITORIA_F0_6_C1_a645d974.md`, sha16 `%s`; relatório `art_a645d974\\AUDITORIA_VINCULO_R2_C1.md`, sha16 `%s`), "
          "sobre o esboço R2 (`sincronizar_bancada.py` sha16 `%s`)." % (s16("C:/IALD/PROGRAMA_IALD/auditorias/F0.6/AUDITORIA_F0_6_C1_a645d974.md"),
                                                                      s16("C:/IALD/PROGRAMA_IALD/auditorias/F0.6/art_a645d974/AUDITORIA_VINCULO_R2_C1.md"), s16(R2 / "sincronizar_bancada.py")), "",
          "**Onde escrevi.** Só em `work\\bancada_vinculo_12out\\R3\\` e no sandbox de raiz curta `C:\\t\\vb3`. O sandbox foi apagado no fim, depois de desfazer as junções "
          "(%d criadas, %d restantes), sem segui-las. As evidências pequenas foram copiadas para `R3\\evidencias_sandbox\\`." % (len(C["juncoes_criadas"]), len(C["juncoes_restantes"])), "",
          "**O que não toquei.** Nada na Bancada de produção, no Nós, no um.py, no quadro, no mapa, na memória ou no túnel. As listas da produção e do Nós ficaram iguais "
          "antes e depois. O manifesto de produção segue `%s` e o livro de eventos real `%s` (os dois só lidos). Não rodei o um.py nem o selo. Não abri dado observado. "
          "Não usei HTTP nem MCP. Não parei nem religuei serviço: o serviço foi simulado, trocando a sonda em processo. Não li confidenciais."
          % (C["producao_intocada"]["manifesto_sha256"][:16], C["eventos_jsonl_real_sha256"][:16]), "",
          "**A palavra recusada da régua** não aparece em nenhum arquivo da R3 (varredura por script com o token montado em RAM; ver §8). "
          "Memória ACOM: não fiz `init` nem `transition`, porque a tarefa restringe a escrita a R3 e ao sandbox. O registro da etapa fica com a c1.", "",
          "**Estatutos.** [REAL] = medido aqui por script · [DERIVED] = composto · [INPUT da gerência] = decisão tomada na encomenda desta R3 · [DECLARADO] = dito na origem e não "
          "conferido aqui · [OPEN] = em aberto. Um PASSA vale só na face testada. NOT_FALSIFIED nunca é creditação. Nada aqui move o gate; nenhum σ nasce aqui.", "",
          "## 1. Veredito dos controles [REAL]", "",
          "`CONTROLES_NEGATIVOS_R3.json` (sha16 `%s`): **%s**." % (s16(AQUI / "CONTROLES_NEGATIVOS_R3.json"), C["veredito"]), "",
          "- **%d de %d** controles recusam (ou aceitam) como esperado." % (C["passam"], C["n"]),
          "- Os **%d da R2** estão todos presentes (%d/%d), com o mesmo nome; os argumentos foram ajustados às flags novas." % (C["n_da_R2"], C["da_R2_presentes"], C["n_da_R2"]),
          "- **%d controles são novos** da R3." % C["n_novos_R3"],
          "- Tempo: %.0f s." % C["segundos"], "",
          "Arquivos medidos:", "",
          "- `sincronizar_bancada.py` R3: `%s`;" % C["script_sha256"][:16],
          "- `montar_sandbox.py` R3: `%s`;" % C["montar_sandbox_sha256"][:16],
          "- `controles_negativos_r3.py`: `%s`;" % C["controles_sha256"][:16],
          "- `BATERIA_VINCULO.json`, da R2 e **inalterada**: `%s`;" % C["bateria_sha256"][:16],
          "- `gerar_canais_mcp.py`, da R2 e inalterado: `%s`." % C["gerar_canais_sha256"][:16], ""]

# 2. runs
linhas += ["## 2. Os runs 1a, 1b e 2, refeitos no sandbox R3 [REAL]", "",
           "| run | o que | recibo (sha16) | veredito | bateria |", "|---|---|---|---|---|"]
for nome, ev, oque in (("RUN_1a_pre_selo_b1_nos_real", "1a", "pré-selo, ensaio, Bancada **b1** (pina o Nós REAL), Nós real v391"),
                       ("RUN_1b_pre_selo_b2_nos_copia", "1b", "pré-selo, ensaio, Bancada **b2** (pina `nos\\`, cópia do Nós v391)"),
                       ("RUN_2_pos_selo_aplicar_b2", "2", "pós-selo, **aplicar** `--sandbox`, b2, com todos os pinos da R3")):
    c = ctl[nome]
    rec, rp = recibo_ev(ev)
    bat = (rec or {}).get("bateria_resultado") or {}
    ts = {t["id"]: t["resultado"] for t in bat.get("testes", [])}
    linhas.append("| %s | %s | `%s` | `%s` | %s — %d testes: %d PASSA, %d FALHA, %d n.e. (T16 %s; T12–T14 %s; T17 %s) |" % (
        ev, oque, (c.get("recibo_sha256") or "")[:16], c.get("veredito"), bat.get("veredito"), bat.get("n", 0), bat.get("passa", 0), bat.get("falha", 0),
        bat.get("nao_executado", 0), ts.get("T16_DEPLOY_FIXTURE"), ts.get("T12_T13_T14_ATRATOR"), ts.get("T17_LEAN_KERNEL")))
r2, _ = recibo_ev("2")
if r2:
    t17 = {t["id"]: t for t in r2["bateria_resultado"]["testes"]}["T17_LEAN_KERNEL"]
    linhas += ["",
               "No run 2:", "",
               "- O `canonical.py` instalado em b2 recusou o pino velho de verdade (`%s`)." % r2.get("pino_velho_recusado_pelo_instalado"),
               "- O evento %s foi verificado pela cadeia, com o hash do elo conferido (`%s`, N6)." % (r2["evento_c1"]["evento"], r2["evento_c1"]["hash_conferido"]),
               "- O recibo pré-selo do run 1b foi conferido por pino (`%s`, N2) e encadeado no manifesto." % r2["recibo_pre_selo"]["sha256"][:16],
               "- O T17 PASSA pelo recibo do kernel no contrato `KERNEL_RECIBO_R3` (sha16 `%s`). O detalhe: «%s»." % (t17["kernel_recibo"]["sha256"][:16], t17["detalhe"]),
               "- Foi gravado o manifesto B3 `%s` (sha16 `%s`), com backup = o manifesto lido no passo 3 (`%s`, N4)."
               % (r2["manifesto_novo"]["deployment_id"], r2["manifesto_novo"]["sha256"][:16], r2["aplicacao"]["manifesto_lido_no_passo_3_sha256"][:16]),
               "- O contrato do kernel ficou encadeado no manifesto (`kernel_recibo_sha256` = `%s`)." % r2["manifesto_novo"]["kernel_recibo_sha256_encadeado"][:16],
               "- β runtime = `%s`, igual bit a bit ao β do contrato instalado." % r2["nos"]["beta_runtime"],
               "- Cada teste executado rodou isolado (N5): `-E -P`, ambiente sem `PYTHON*`, cwd numa pasta vazia nova.",
               "- Nenhum `__pycache__` nasceu."]
linhas += ["", "A re-execução (`RUN_2bis_idempotente`) deu `%s`." % ctl["RUN_2bis_idempotente"]["veredito"], ""]

# 3. achados
ACH = [
    ("N1", "ALTA", "O T17 era autodeclarado: 4 campos bastavam e o log não era lido",
     "Contrato `KERNEL_RECIBO_R3` (`CONTRATO_KERNEL_RECIBO.md`). O recibo é pinado por `--kernel-recibo-sha256`. Os logs são **lidos**: o sha confere, e sorry e erros são "
     "recontados por script. `rc`, `sorry` e `erros` são int estritos. A toolchain, os `statuses` e o `axiom_report` vêm do `tgl_kernel_proof_manifest.json` **pinado pelo selo**. "
     "Os sha DEPOIS da raiz, do Audit e das pedras batem com `formal_files_sha256` e são re-hasheados na árvore. O ANTES é cruzado com o kernel anterior registrado no recibo "
     "pré-selo. Os critérios da §4.6 são conferidos como medido == esperado. `um_py_sha256` virou campo **proibido**. O recibo pré-selo passou a trazer `nos.kernel`."),
    ("N2", "MÉDIA", "O recibo pré-selo era aceito por conteúdo; um JSON escrito à mão passava, também com `--producao`",
     "`--recibo-pre-selo-sha256` (lido de `v392_pins`): obrigatório em `--producao` e em aplicar fora do sandbox; divergente = recusa."),
    ("N3", "MÉDIA", "O serviço era sondado uma vez só, antes da bateria",
     "`guarda_servico(momento)` sonda no início e **imediatamente antes de cada gravação**: backup, contrato, temporário, troca e recibo em `estado\\`. Se o serviço voltou: recusa e desfaz (rollback). "
     "A porta é lida na hora da chamada."),
    ("N4", "MÉDIA", "Atualização perdida: o aplicar comparava com os bytes que ele mesmo acabara de ler",
     "O aplicar compara com `anterior['_raw']` (passo 3) no início e de novo imediatamente antes do `os.replace`: `MANIFESTO_MUDOU_DESDE_A_LEITURA`, e a mudança fica."),
    ("N5", "MÉDIA", "Código não pinado executava dentro de testes pinados (`hashlib.py` ao lado; `PYTHONPATH`)",
     "Os testes rodam com `-E -P`, ambiente sem `PYTHON*` e cwd numa pasta vazia nova. A guarda recusa módulo-sombra (`.py`, `.pyc`, `.pyd` ou pacote) da stdlib ou de site-packages ao lado de fonte pinada. "
     "O esboço recusa `PYTHONPATH`, `PYTHONHOME`, `PYTHONSTARTUP` e `PYTHONUSERBASE` no próprio ambiente sem `-E`. **Não** usei `-I`/`-S`: numpy, scipy e torch vivem no "
     "site do USUÁRIO [REAL, 13/10], e `-I`/`-s`/`-S` os cortariam (limite declarado)."),
    ("N6", "MÉDIA", "A autoria do evento era autodeclarada",
     "[INPUT da gerência] `--evento-hash <hash16>` confere o hash do elo na cadeia. Continuam conferidos tipo, `quem == claude-c1`, versão e Bancada nomeadas. "
     "**Isto não é autenticação**: `quem` é convenção do quadro, e o recibo o diz."),
    ("N8", "BAIXA", "As raízes de `--saida` eram largas (todo o `work\\` e todo o `C:\\t`)",
     "[INPUT da gerência] Ficam só `work\\bancada_vinculo_12out`, `work\\cadeia_de_selo\\<alvo>`, `work\\<alvo>_bateria` e `C:\\t\\vb*`, onde o alvo é a versão em `pos_selo` e a seguinte em `pre_selo`. "
     "Nunca a pasta do esboço nem as das fontes ou cópias da bateria. A versão só é aceita na forma `vNNN`."),
    ("N9", "BAIXA", "Nomes reservados criados como arquivos",
     "`relativo_seguro` recusa, por componente, CON/PRN/AUX/NUL/COMn/LPTn (com sobrescritos), cauda `.`/espaço e caracteres inválidos."),
    ("N10", "BAIXA", "O recibo do aplicar seguia junção em `estado\\`",
     "`sem_juncao`: pré-voo do manifesto, do contrato e do recibo em `estado\\sincronizacao` **antes da primeira gravação**. Nenhum componente léxico pode ser junção ou link, nem para fora nem para dentro."),
    ("N11", "BAIXA", "O filtro de negação era contornável por NFD e por chaves",
     "A negação é procurada em chaves **e** valores normalizados (NFKC; NFD sem Mn/Cf; caixa dobrada; `_` vira espaço). O conjunto de chaves de `dados` é fechado. "
     "A guarda da palavra também normaliza."),
    ("N12", "BAIXA", "Hardlink dos arquivos do Nós noutra pasta admitia `--sandbox`",
     "`pina_o_nos_real` também confere os arquivos (`samefile` do `um.py` e do selo), não só a pasta."),
    ("N13", "BAIXA", "`Volume{GUID}` recusado por acidente",
     "Regra explícita: depois do prefixo de dispositivo só se admite letra de disco. `Volume{GUID}` recusa com `CAMINHO_VOLUME_GUID_NAO_ADMITIDO`; GLOBALROOT, pipe etc. com `CAMINHO_DISPOSITIVO_NAO_ADMITIDO`. `\\??\\C:` é normalizado."),
    ("N14", "BAIXA", "O log era gravado antes da guarda de palavra; o token na bateria dava traceback",
     "A guarda vem antes de gravar o log, e com a palavra o log sai suprimido (só o sha). `fechar` grava um recibo **mínimo** sem a palavra (rc 2), e há pré-voo antes da primeira gravação na Bancada."),
    ("N15", "BAIXA", "Mesma versão, mesmo um.py, selo diferente: era re-pinado em silêncio",
     "[INPUT da gerência] `SEAL_CHANGED_SAME_VERSION`, salvo `--reparo-de-pino` em aplicar com evento c1 `dados.reparo=true` que nomeie o selo novo."),
    ("N16", "BAIXA", "A guarda de `.py` deixava passar `-c`, `-m`, zip e pasta",
     "Gramática fechada: `{py}`, depois só `-B` e `-X utf8`, depois um `.py` absoluto e pinado. `-c`, `-m`, `-I`, zip, pasta, comando sem `{py}` e `.py` relativo são recusados antes de executar."),
]
linhas += ["## 3. Os achados N1–N16: conserto → controle → resultado", "",
           "N7 é documental: está em `REMISSOES_PLANO_R3.md` (§5 abaixo).", "",
           "| achado | grav. | o que a R2 fazia | conserto R3 | controles novos | resultado [REAL] |", "|---|---|---|---|---|---|"]
for n, g, antes, cons in ACH:
    nomes = [k for k in ctl if re.match(r"^%s_" % n, k)]
    ok = sum(1 for k in nomes if ctl[k]["passa"])
    mostra = nomes if len(nomes) <= 12 else nomes[:8] + ["… e mais %d (todos em `CONTROLES_NEGATIVOS_R3.json`)" % (len(nomes) - 8)]
    linhas.append("| **%s** | %s | %s | %s | %s | **%d/%d PASSA** |" % (n, g, antes, cons, "<br>".join(("`%s`" % k) if not k.startswith("…") else k for k in mostra), ok, len(nomes)))
linhas += ["", "Os A1 da R2 (`A1_kernel_recibo_invalido_{sorry,versao,log,um_py}`) rodam agora contra o contrato R3. O `um_py` passou a ser recusado como **campo proibido**.", ""]

# 4. decisoes da gerencia
linhas += ["## 4. Decisões da gerência registradas nesta R3 [INPUT da gerência]", "",
           "- **N6.** A autoria do evento segue **convenção, não autenticação**. O que se endureceu:",
           "  - o B(n) recebe `--evento <n> --evento-hash <hash16>` da cadeia;",
           "  - confere tipo `SINCRONIZACAO_BANCADA`, `quem == claude-c1`, a versão, a Bancada (por identidade), o um.py e o selo nomeados;",
           "  - confere o hash do elo na cadeia, e a cadeia de hash do primeiro elo até ele;",
           "  - limita as chaves de `dados` a um conjunto fechado.",
           "",
           "  **Isto não autentica quem escreveu**: `iald.py anotar` aceita `--quem` livre. O recibo do B(n) diz «convencao (quem=claude-c1), nao autenticacao».",
           "- **N8.** As raízes estreitas da §3.",
           "- **N15.** `SEAL_CHANGED_SAME_VERSION`, salvo `--reparo-de-pino`.", ""]

# 5. remissoes e contrato
linhas += ["## 5. Documentos", "",
           "- **`CONTRATO_KERNEL_RECIBO.md`** (sha16 `%s`): os campos que `construir_kernel_vNNN.sh` tem de escrever e o que o B(n) confere, em ordem. Atende o §5 da re-auditoria." % s16(AQUI / "CONTRATO_KERNEL_RECIBO.md"),
           "- **`REMISSOES_PLANO_R3.md`** (sha16 `%s`): texto pronto para a gerência aplicar **ao lado**, sem editar o plano. Substitui `R2\\REMISSOES_PLANO.md`. Cobre:" % s16(AQUI / "REMISSOES_PLANO_R3.md"),
           "  - o comando completo (com `--bancada`, `--bateria`, `--saida` e as flags R3);",
           "  - §3: a bateria R2/R3 substitui a H12;",
           "  - §4: o contrato do kernel;",
           "  - §5: o que `v392_pins` pina;",
           "  - §11: a numeração 9 → 10 → 10-bis-a (parada com recibo) → 10-bis → 10-ter → 11 Fechar;",
           "  - §12, item 1, contra o 12-bis;",
           "  - a errata ao lado dos itens 1 e 4 do 12-bis, com a regra R2/R3 do evento;",
           "  - §14;",
           "  - a ressalva do cabeçalho falso.",
           "- **`DIFF_R2_R3.patch`** (sha16 `%s`): todos os `.py` da R2 para a R3: `sincronizar_bancada.py`, `montar_sandbox.py` e `controles_negativos_r2.py` → `controles_negativos_r3.py`. "
           "`gerar_canais_mcp.py` e `gerar_bateria.py` não mudaram e não têm hunk. A aplicação com `git apply` sobre uma cópia da R2 foi conferida bit a bit (§8)." % s16(AQUI / "DIFF_R2_R3.patch"),
           "- **`DIFF_R1_R2_montar_sandbox.patch`** (sha16 `%s`): a omissão da R2, o `montar_sandbox.py` da R1 para a R2." % s16(AQUI / "DIFF_R1_R2_montar_sandbox.patch"), ""]

# 6. nao feito e atos do operador
linhas += ["## 6. O que NÃO fiz, e por quê", "",
           "- **Autenticação do evento (N6).** Fica convenção: é decisão da gerência e precisa de mecanismo fora do esboço (assinatura, ou o evento ligado ao `request_id` da sessão na memória ACOM).",
           "- **`-I`/`-S` nos testes (N5).** Cortariam numpy, scipy e torch, que estão no site do usuário. Uso `-E -P` mais ambiente limpo mais a guarda de módulo-sombra.",
           "  - [OPEN] O site do usuário segue gravável por qualquer processo desta conta. Um `.pth` ou `usercustomize` ali executaria nos testes.",
           "  - A custódia da bateria numa pasta selada da cadeia é a derivação para `cadeia_de_selo\\v392\\vinculo\\`, ato da gerência.",
           "- **Recibo de parada do serviço exigido por flag (N3).** O esboço só sonda a porta. O recibo da parada (10-bis-a) é ato do operador e fica no `fechar` (Remissão 4).",
           "- **Corrida TOCTOU dentro de `caminho_canonico`** (troca de junção entre a guarda e o `mkdir`). Não está coberta, e o resíduo fica declarado. O pré-voo de `sem_juncao` reduz a janela no aplicar.",
           "- **Link simbólico.** Não testado: sem privilégio nesta conta. Junção, hardlink e `subst` cobrem a classe.",
           "- **T17 com kernel real, aplicar na produção real, religamento do serviço e reconexão MCP.** Nada disso foi feito: é proibido aqui. A produção foi simulada por decoy **em processo** numa cópia (`pd\\`).",
           "- **`construir_kernel_v392.sh`, `derivar_cadeia_v392.py`, o registro no mapa e a edição do plano.** São atos da gerência: escrevi os textos e o contrato, não os apliquei.", "",
           "## 7. Atos do operador", "",
           "- **B3:** autorizar o primeiro re-pino da produção sob evento c1. Sem isso, a cadeia da v392 para em 10-bis-a (`AGUARDA_OPERADOR`), e a custódia espera.",
           "- **A parada do `um_bancada.py` com recibo (10-bis-a), o religamento com recibo de identidade (10-ter) e a reconexão dos adaptadores MCP.**",
           "- **O que entra na implantação B3 de código:**",
           "  - a rota genérica;",
           "  - a unicidade de α e de `UM_VERSION` no `canonical.py`;",
           "  - a custódia da bateria junto da Bancada;",
           "  - o README;",
           "  - a sobra D6 da F7.2.",
           "- **Se a ordem permanente de 12/10 vale da v393 em diante.**", ""]

# 8. pinos e verificacoes
pin_self = s16(AQUI / "PINOS_R3.json")
linhas += ["## 8. Pinos, sandbox e varreduras [REAL]", "",
           "- **`PINOS_R3.json`** (sha16 `%s`): %d entradas medidas por script, %d ausentes. As %d fontes e cópias pinadas na bateria: %d conferem com o disco."
           % (pin_self, P["n_entradas"], P["n_ausentes"], P["n_fontes_da_bateria"], P["n_fontes_que_conferem"]),
           "- **Produção e Nós:** listas iguais antes e depois dos controles. O manifesto de produção é `%s`." % C["producao_intocada"]["manifesto_sha256"][:16],
           "- **Livro de eventos real:** `%s` durante os controles (só lido; ele é vivo)." % C["eventos_jsonl_real_sha256"][:16],
           "- **Sandbox `C:\\t\\vb3`:** as junções foram desfeitas pelo próprio script dos controles (`os.rmdir` no link, nunca no alvo). A árvore foi apagada sem seguir junção. "
           "O que ficou de evidência está em `R3\\evidencias_sandbox\\`.", ""]
open_ = AQUI / "VERIFICACOES_FINAIS_R3.json"
if open_.is_file():
    vf = json.loads(open_.read_bytes())
    linhas += ["- **Verificações finais** (`VERIFICACOES_FINAIS_R3.json`, sha16 `%s`):" % s16(open_)]
    for k, v in vf.items():
        if isinstance(v, dict) and "patch" in v:
            v = "patch sha16 `%s`, %d B; `git apply` rc %d; reproduz bit a bit: %s. %s" % (v["sha256"][:16], v["bytes"], v["git_apply_rc"], v["reproduz_bit_a_bit"], v.get("nota", ""))
        linhas.append("  - %s: %s" % (k, v))
    linhas += [""]
linhas += ["Nada aqui é leitura física. NOT_FALSIFIED nunca é creditação. O gate não se move.", ""]
texto = "\n".join(linhas)
(AQUI / "RESULTADO_R3.md").write_bytes(texto.encode("utf-8"))
print("RESULTADO_R3.md", len(texto))

# -*- coding: utf-8 -*-
"""gerar_resultado_r2.py (R2, 13/10/2026) -- escreve R2\\RESULTADO_R2.md a partir de CONTROLES_NEGATIVOS_R2.json, PINOS_R2.json e dos recibos
do sandbox: a tabela achado -> conserto -> teste -> resultado, com TODO hash e numero lidos dos artefatos (nunca digitados). uso: <raiz do sandbox>"""
import sys
sys.dont_write_bytecode = True
import json, hashlib, datetime
from pathlib import Path
AQUI = Path(__file__).resolve().parent
RAIZ = Path(sys.argv[1]).resolve()
C = json.loads((AQUI / "CONTROLES_NEGATIVOS_R2.json").read_text(encoding="utf-8"))
P = json.loads((AQUI / "PINOS_R2.json").read_text(encoding="utf-8"))
ctl = {x["controle"]: x for x in C["controles"]}


def s16(d):
    return (d or {}).get("sha256", "?")[:16]


def res(*nomes):
    out = []
    for n in nomes:
        x = ctl.get(n)
        if x is None:
            out.append("`%s`: AUSENTE" % n)
            continue
        cod = (x.get("recusa") or x.get("veredito") or ("ACEITO" if x.get("aceito") else "")) or ""
        cod = str(cod).split(":")[0].split("__NADA")[0]
        out.append("`%s` → %s (%s%s)" % (n, "**PASSA**" if x["passa"] else "**FALHA**", ("rc %s, " % x["rc"]) if "rc" in x else "", cod))
    return "<br>".join(out)


def recibo(sub):
    fs = sorted((RAIZ / "s" / sub).glob("RECIBO_SINCRONIZACAO_*.json"))
    if not fs:
        return None, None
    return fs[-1], json.loads(fs[-1].read_bytes())


r1a_p, r1a = recibo("1a")
r1b_p, r1b = recibo("1b")
r2_p, r2 = recibo("2")
SBM = json.loads((RAIZ / "SANDBOX_MANIFEST_R2.json").read_text(encoding="utf-8"))
ELOS = SBM["fx"]["elos_de_ensaio"]
SEQ_OK = ELOS["valido"]["seq"]
SEQ_MAX = max(e["seq"] for e in ELOS.values())
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
E = P["entregaveis_R2"]
linhas = [
    ("**A1** (ALTA)", "T17 com `--kernel-recibo` caía em `subprocess.run(\"(sem comando)\")` → `ERRO_NAO_PREVISTO`; o B(n) aplicar fora do sandbox nunca completava",
     "`verificar_kernel_recibo()`: o T17 é lido do recibo do build por hash, **sem subprocesso**, antes do `subprocess.run`; campos exigidos `versao==alvo`, `rc==0`, `sorry==0`, `build_full_log_sha256` (64 hex); se o recibo nomeia `build_full_log`, o log tem de existir e bater; `um_py_sha256`/`tgl_kernel_proof_manifest_sha256`, se presentes, conferidos contra o Nós; T17 entra no conjunto mínimo de `aplicar pos_selo`; em aplicar fora do sandbox, recibo ausente = FALHA",
     "recibo sintético válido (`fx\\KERNEL_RECIBO_v392_SINTETICO_VALIDO.json`, `%s`) no run 2 e no C7; quatro inválidos (sorry=1, versão errada, log divergente, outro um.py); ausente em ensaio; ausente em aplicar fora do sandbox (unitário)" % s16(P["sandbox"].get("fx/KERNEL_RECIBO_v392_SINTETICO_VALIDO.json")),
     res("RUN_2_pos_selo_aplicar_b2", "C7_bateria_falha_em_aplicar", "A1_kernel_recibo_invalido_sorry", "A1_kernel_recibo_invalido_versao", "A1_kernel_recibo_invalido_log", "A1_kernel_recibo_invalido_um_py",
         "A1_kernel_recibo_ausente_em_ensaio_NAO_EXECUTADO", "A1_kernel_recibo_ausente_em_aplicar_fora_do_sandbox_FALHA")),
    ("**A2** (ALTA)", "`Path.resolve()` preservava `\\\\?\\` e UNC → `producao=False`; com `--sandbox` + `SANDBOX:*` + bateria trivial gravava na cópia (ataque B1); na produção o mesmo caminho valeria",
     "`caminho_canonico()` normaliza `\\\\?\\`, `\\\\?\\UNC\\`, `\\\\.\\`, UNC local (`127.0.0.1`, `localhost`, `::1`, o host) → letra de disco, recusa UNC não local, depois `resolve()` (junção, 8.3, `..`, caixa); `mesmo_no()` = `os.path.samefile` (st_dev+st_ino); **`--sandbox` recusado sempre que o manifesto da `--bancada` pina o Nós real** (`SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL`); o sandbox passa a usar uma cópia `b2` cujo manifesto pina um Nós de ensaio (`montar_sandbox.py`)",
     "13 formas de caminho da produção (prefixo longo, UNC localhost/127/host, `\\\\?\\UNC`, `\\\\.\\`, 8.3, minúsculas, barras normais, barra dupla+ponto, UNC com barras normais, junção, relativo); `--producao --sandbox` por prefixo; UNC não local; **o ataque B1 refeito** (`\\\\?\\b1` e junção para b1, `--sandbox --modo aplicar --evento SANDBOX:*`); `--sandbox` em cópia que pina o Nós real",
     res("A2_producao_prefixo_longo", "A2_producao_unc_localhost", "A2_producao_unc_127", "A2_producao_unc_host", "A2_producao_prefixo_unc", "A2_producao_prefixo_ponto", "A2_producao_nome_83",
         "A2_producao_minusculas", "A2_producao_barras_normais", "A2_producao_barra_dupla_e_ponto", "A2_producao_unc_barras_normais", "A2_producao_juncao", "A2_producao_relativo_pelo_cwd",
         "A2_producao_prefixo_longo_com_producao_e_sandbox", "A2_unc_nao_local", "A2_B1_replay_prefixo_sandbox_aplicar_b1", "A2_B1_replay_juncao_sandbox_aplicar_b1",
         "A2_sandbox_em_copia_que_pina_o_nos_real_ensaio", "A2_producao_flag_em_copia_e_aceito_sem_efeito")),
    ("**A3** (ALTA)", "`fontes[]` pinava `…\\bateria\\t01_identidade.py`, mas o comando rodava `{vinculo}/bateria/…` = a pasta onde o esboço está: um t01 adulterado ao lado rodava com pino OK",
     "o marcador `{vinculo}` **não existe mais** (recusado na carga: `MARCADOR_VINCULO_PROIBIDO`); os testes da pasta `bateria\\` entram por `{fonte:N}` = o caminho **pinado** em `fontes[]`; o sha256 de cada fonte é conferido **antes** de executar; todo `.py` que o comando passa tem de ser fonte pinada (por `samefile`), arquivo da cópia de ensaio ou cópia conferida da bateria (`COMANDO_EXECUTA_ARQUIVO_NAO_PINADO`); `gerar_bateria.py` R2 emite a bateria nessa forma",
     "esboço copiado para `C:\\t\\vb\\esb\\` com um `bateria\\t01_identidade.py` **adulterado** ao lado (o ataque A8 da auditoria); comando com `.py` não pinado; fonte pinada adulterada depois do pino; bateria com `{vinculo}`",
     res("A3_esboco_copiado_com_t01_adulterado_ao_lado", "A3_comando_executa_py_nao_pinado", "A3_fonte_pinada_adulterada_antes_de_rodar", "A3_marcador_vinculo_proibido")),
    ("**A4** (MÉDIA)", "verificador por substring (`versao`, `Bancada_Um`, «sincroniz»), sem ler `anterior`/`hash`: eventos forjados sem cadeia, texto que NEGA e hashes de outro programa eram ACEITOS",
     "`verificar_evento()` reimplementa a conferência de `iald.py verificar()` (`anterior == hash` do elo anterior; `hash` recalculado) do 1º elo até o evento (`EVENTOS_CADEIA_QUEBRADA`, `EVENTO_SEQ_DUPLICADO`); exige `tipo=SINCRONIZACAO_BANCADA`, `quem=claude-c1`, `dados` JSON com `versao`, `acao=sincronizacao`, `bancada` (por identidade `samefile`), `um_py` e `selo` (prefixo ≥16 hex do sha do Nós lido), `reparo=true` quando `--reparo-de-pino`; qualquer texto com negação/veto/recusa é `EVENTO_COM_NEGACAO`; `--eventos` (livro alternativo) só em `--sandbox`. O `iald.py` não foi importado (tem efeitos de módulo); a regra é a mesma, linha a linha",
     "16 casos unitários sobre um livro de ensaio (cópia do real, %d elos, + 9 elos encadeados `%d–%d` + 2 forjados), inclusive os F1/F3/F4/F6 que a R1 aceitava, o livro **real** (só lido; cadeia inteira conferida) e o `SANDBOX:` fora do sandbox; 3 casos por subprocesso (negação, forjado sem cadeia, `--eventos` fora do sandbox); o run 2 aplica sob o elo %d **verificado**" % (SBM["fx"]["eventos_reais_copiados"], SEQ_OK, SEQ_MAX, SEQ_OK),
     res("A4_evento_valido_encadeado_aceito", "A4_F1_forjado_sem_cadeia", "A4_F6_seq_duplicado_encadeado", "A4_F2_outra_sessao", "A4_F3_texto_que_nega", "A4_F4_hashes_de_outro_programa", "A4_F5_outra_versao",
         "A4_outra_bancada_por_identidade", "A4_tipo_errado", "A4_sem_acao", "A4_F7_evento_real_706_nova_F06", "A4_F8_sandbox_literal_fora_do_sandbox", "A4_F10_seq_inexistente", "A4_F11_nao_numerico",
         "A4_livro_real_integro_seq_seguinte_nao_existe_nele", "A4_livro_real_ultimo_elo_nao_e_sincronizacao", "A4_sub_evento_com_negacao", "A4_sub_evento_forjado_sem_cadeia", "A4_eventos_alternativo_fora_do_sandbox", "C3_aplicar_sem_evento", "C4_evento_real_nao_nomeia")),
    ("**A5** (MÉDIA)", "`--saida` não era conferido: gravava `raiz\\`, `recibos\\` e recibos dentro de qualquer pasta, inclusive (por construção) na produção",
     "`--saida` só sob `RAIZES_SAIDA` = a pasta de trabalho da cadeia (`work\\`) ou a raiz curta `C:\\t`; **nunca** sob a produção, o Nós (padrão e `--nos`) ou a própria `--bancada`; as recusas acontecem **antes** de qualquer gravação (nem recibo nasce: `recusa anterior a admissao de --saida`)",
     "saída sob a produção (direta, por prefixo `\\\\?\\`, por junção), sob o Nós, dentro da Bancada-cópia, fora das raízes (`%%TEMP%%`); listas da produção e do Nós conferidas iguais antes/depois",
     res("A5_saida_na_producao", "A5_saida_na_producao_por_prefixo", "A5_saida_na_producao_por_juncao", "A5_saida_no_nos", "A5_saida_dentro_da_bancada", "A5_saida_fora_das_raizes")),
    ("**A6** (MÉDIA)", "`--recibo-pre-selo` forjado (v000, outra Bancada, outro um.py) era ACEITO e gravava: só `fase` e o veredito da bateria eram lidos",
     "`conferir_recibo_pre_selo()`: `versao_alvo == versão anterior` da Bancada (ou, se já pina a alvo, a geração anterior registrada em `sincronizacao.anterior`), `nos.um_py.sha256 == um.py antes pinado`, `bancada.dir` igual por identidade, veredito `JA_SINCRONIZADA__ENSAIO…`, T01 e T15 PASSA nele; o sha256 do recibo fica **encadeado** no manifesto novo (`sincronizacao.recibo_pre_selo_sha256`) e no contrato; recibo pré-selo na fase pré-selo é recusado; aplicar fora do sandbox sem ele é recusado",
     "o PRE forjado da auditoria (B4); o recibo **real** do run 1a (Bancada b1) usado para b2; o recibo do run 1b com o sha do um.py trocado; recibo na fase pré-selo; aplicar sem recibo fora do sandbox; o run 2 encadeia o recibo do run 1b (`%s`)" % (sha(r1b_p)[:16] if r1b_p else "?"),
     res("A6_recibo_pre_selo_forjado", "A6_recibo_pre_selo_de_outra_bancada", "A6_recibo_pre_selo_1b_com_um_py_trocado", "A6_recibo_pre_selo_na_fase_pre_selo", "A6_aplicar_fora_do_sandbox_sem_recibo_pre_selo", "RUN_2_pos_selo_aplicar_b2")),
    ("**A7** (MÉDIA)", "a bateria não era conferida contra pino esperado nem contra um conjunto mínimo: um teste trivial bastava para gravar",
     "`carregar_bateria()`: `--bateria-sha256` obrigatório em `aplicar` (lido de `vNNN_pins`) e conferido; `testes_sha256` = sha256 canônico de **cada** teste, conferido na carga; todo teste (salvo o do kernel) com fonte pinada; conjunto mínimo em `aplicar`: T01 + T15 (+ T17 em pós-selo); ids únicos",
     "bateria de um teste trivial em aplicar; aplicar sem `--bateria-sha256`; sha divergente; teste alterado depois do pino por teste",
     res("A7_bateria_trivial_em_aplicar", "A7_bateria_sem_sha_em_aplicar", "A7_bateria_sha_divergente", "A7_teste_adulterado_apos_pino")),
    ("**A8** (MÉDIA)", "manifesto v391 com o sha de outro arquivo: `PIN_CHANGED` com a **mesma** versão → o esboço re-pinava a mesma versão («atualizar só o hash», proibido pelo `CONTRATO_CANONICO_B2.md`)",
     "mesma versão + hash diferente do um.py = `SELO_PROGRAMA_DIVERGE`, salvo `--reparo-de-pino` (só em `aplicar`) com evento c1 encadeado que traga `dados.reparo=true` (`EVENTO_NAO_AUTORIZA_REPARO` sem ele); o manifesto e o contrato registram `reparo_de_pino`; `aplicar` só na fase pós-selo (`APLICAR_SO_NA_FASE_POS_SELO`), salvo reparo nomeado",
     "cópia b1x com o sha alterado (ensaio; ensaio com `--reparo-de-pino`); cópia b2x com evento encadeado SEM `reparo` e COM `reparo=true` (livro de ensaio; o real intocado)",
     res("A8_mesma_versao_hash_diferente", "A8_reparo_em_ensaio_recusado", "A8_reparo_com_evento_sem_dados_reparo", "A8_reparo_nomeado_em_evento_aplica", "APLICAR_na_fase_pre_selo_recusado")),
    ("**A9** (MÉDIA)", "sem `-B`, `carregar_canonical` gravava `bancada\\__pycache__\\canonical.*.pyc` dentro da Bancada (gravação sem evento)",
     "`sys.dont_write_bytecode = True` na 2ª linha do esboço (antes de qualquer import), `assert` em `carregar_canonical`, `PYTHONDONTWRITEBYTECODE=1` no ambiente de todo subprocesso; o recibo registra `python_dont_write_bytecode`",
     "esboço rodado **sem** `-B` contra b1; `rglob('__pycache__')` em b1 e em b2 (depois do run 2) vazios",
     res("A9_sem_B_nenhum_pycache", "RUN_2_pos_selo_aplicar_b2")),
    ("**A10** (MÉDIA)", "`..` em `code[].path` e `..`/absoluto em `copias[].para` escapavam de `--saida` (`k\\fora\\evil.py` nasceu na auditoria)",
     "`relativo_seguro()`: sem `..`, sem absoluto, sem drive/âncora, e o destino resolvido tem de ficar sob a raiz (`CAMINHO_RELATIVO_INVALIDO` / `CAMINHO_FORA_DA_RAIZ`), aplicado em `regenerar` (leitura), `montar_staging` (cópia), `copiar_testes` e no contrato gravado",
     "manifesto com `..\\fora\\evil.py` em `code[]` (regenerar e caminho já-sincronizada); `copias[].para` com `..` e absoluto; conferido que nada nasceu fora",
     res("A10_traversal_em_code_path", "A10_traversal_em_code_path_ja_sincronizada", "A10_traversal_em_copias_para", "A10_copia_absoluta")),
    ("**A11** (BAIXA)", "segunda `UM_VERSION` na coluna 0 passava (o esboço lia a primeira; o Python executaria a última); `ALPHA` reatribuído indentado passava (limite declarado)",
     "**decisão R2: recusar, não declarar limite.** `UM_VERSION` tem de ser linha única na coluna 0 (`UM_VERSION_LINHA_NAO_UNICA`), como α; e **nenhuma** reatribuição indentada de α nem de `UM_VERSION` (`ALPHA_REATRIBUIDA_INDENTADA`, `UM_VERSION_REATRIBUIDA_INDENTADA`; `==` excluído). Justificativa medida: no um.py v391 real (`%s`) há 1 linha de cada na coluna 0 e **0** reatribuições indentadas (recibo do run 1a: `alpha.n_reatribuicoes_indentadas=0`, `um_version_linhas.indentadas=0`) — a regra não custa nada ao canônico e fecha o buraco; o contrato só é seguro quando a declaração é única" % s16(P["nos_so_lido"].get("um.py")),
     "fixtures mínimas de Nós (unitário): limpo aceito; 2ª `UM_VERSION` coluna 0; α indentado; `UM_VERSION` indentada; α duplicado coluna 0; `==` não é atribuição; o Nós real passa (run 1a)",
     res("A11_nos_minusculo_limpo_aceito", "A11_segunda_UM_VERSION_coluna_0", "A11_alpha_reatribuido_indentado", "A11_UM_VERSION_reatribuida_indentada", "A11_alpha_duplicado_coluna_0", "A11_comparacao_nao_e_atribuicao", "RUN_1a_pre_selo_b1_nos_real")),
    ("**A12** (—)", "junção, 8.3, barras duplas, minúsculas, relativo, `--producao --sandbox` já recusados na R1", "mantidos, agora por identidade", "incluídos na bateria A2", res("A2_producao_juncao", "A2_producao_nome_83", "A2_producao_barra_dupla_e_ponto", "A2_producao_relativo_pelo_cwd")),
    ("**A13** (MÉDIA)", "a guarda de palavra do `gerar_canais_mcp.py` só existia no módulo gerado (código morto): uma declaração com o token gerava o módulo com o token na tabela `CANAIS`",
     "`gerar()` aplica `GUARDA` à **declaração inteira** (JSON ordenado) antes de qualquer escrita (`PALAVRA_PROIBIDA_NA_DECLARACAO`); o `mkdir` da saída só depois das guardas (uma declaração recusada não deixa pasta)",
     "declaração com o token no `veredito_selado` construída **só em RAM** (o token nunca foi escrito em disco) → recusa e nenhuma pasta; a declaração limpa da R1 (`CANAIS_v391_exemplo.json`) gera os quatro arquivos",
     res("A13_declaracao_com_token_recusada", "A13_declaracao_limpa_gera")),
    ("**T16**", "falhava em raiz longa (`WinError 206`); PASSA só [DECLARADO] em raiz curta", "o sandbox R2 vive em `C:\\t\\vb` (montar_sandbox exige `C:\\t\\…`); `RAIZES_SAIDA` inclui `C:\\t`",
     "T16 incluído nos runs 1a, 1b e 2", res("RUN_1a_pre_selo_b1_nos_real", "RUN_1b_pre_selo_b2_nos_copia", "RUN_2_pos_selo_aplicar_b2")),
    ("**T17**", "jamais executado por ninguém (nenhum kernel construído)", "ver A1: lido do recibo do build por hash", "recibo sintético (fixture marcada) — [REAL quanto ao mecanismo; o kernel real segue [OPEN] até a etapa 2 da cadeia]", res("RUN_2_pos_selo_aplicar_b2")),
    ("**§6(b)/(d) da auditoria**", "o comando do 12-bis omite `--recibo-pre-selo`/`--kernel-recibo`; as remissões §3/§14 não foram inseridas", "texto pronto em `REMISSOES_PLANO.md` (o plano não foi editado aqui)", "—", "entregue"),
]


def bat(r):
    if not r:
        return "—"
    b = r["bateria_resultado"]
    ids = {t["id"]: t["resultado"] for t in b["testes"]}
    return "%s — %d testes, %d PASSA, %d FALHA, %d n.e. (T16 %s; T12–T14 %s; T17 %s)" % (b["veredito"], b["n"], b["passa"], b["falha"], b["nao_executado"], ids.get("T16_DEPLOY_FIXTURE"), ids.get("T12_T13_T14_ATRATOR"), ids.get("T17_LEAN_KERNEL"))


md = []
md.append("# R2 DO VÍNCULO BANCADA–UM.PY — 13/10/2026 — resultado (achado → conserto → teste → resultado)\n")
md.append("Construtor da R2: subagente da gerência c1 (sessão 6da8f00d). Objeto: os achados A1–A13 da auditoria independente (`AUDITORIA_VINCULO_BANCADA_C1.md`, `%s`) sobre o esboço R1 (`sincronizar_bancada.py` `%s`). "
          "**Escrevi só em `work\\bancada_vinculo_12out\\R2\\`** (os arquivos R1 ficam como registro; cópias byte a byte em `R2\\originais_R1\\`, todas conferidas iguais) **e no sandbox de raiz curta `%s`**. "
          "Nada na Bancada de produção, no Nós, no um.py, no quadro, no mapa, na memória, no túnel: listas da produção e do Nós iguais antes/depois; manifesto de produção `%s`; livro de eventos real `%s` (só lido). "
          "Não rodei um.py nem script de selo; não abri dado observado; nenhum HTTP/MCP; confidenciais não tocados; a palavra recusada da régua não aparece em nenhum arquivo R2 (grep do token inteiro: zero). "
          "Hashes por script (`medir_pinos_r2.py` → `PINOS_R2.json`, `%s` entradas). Memória ACOM: sem `init`/`transition` (escrita restrita à pasta R2 e ao sandbox; o registro de etapa fica com a c1).\n"
          % (s16(P["auditoria"].get("AUDITORIA_VINCULO_BANCADA_C1.md")), s16(P["originais_R1"].get("sincronizar_bancada.py")), RAIZ,
             s16(P["producao_so_lida"].get("canonical_contracts.json")), s16(P["quadro_so_lido"].get("eventos.jsonl")), sum(len(v) for v in P.values() if isinstance(v, dict))))
md.append("**Estatutos:** [REAL] medido aqui · [DERIVED] composto · [DECLARADO] dito na origem · [OPEN] em aberto. Um PASSA é validade na face testada; NOT_FALSIFIED nunca é creditação; nada aqui move o gate; nenhum σ nasce aqui.\n")
md.append("## Veredito dos controles [REAL]\n")
md.append("`CONTROLES_NEGATIVOS_R2.json` (`%s`): **%s** — %d de %d (os 7 da R1: C1–C7; os novos: A1–A13, T16, idempotência), em %.0f s; `sincronizar_bancada.py` R2 `%s`; `BATERIA_VINCULO.json` R2 `%s`; `gerar_canais_mcp.py` R2 `%s`.\n"
          % (s16(E.get("CONTROLES_NEGATIVOS_R2.json")), C["veredito"], C["passam"], C["n"], C["segundos"], s16(E.get("sincronizar_bancada.py")), s16(E.get("BATERIA_VINCULO.json")), s16(E.get("gerar_canais_mcp.py"))))
md.append("## O sandbox completo em raiz curta [REAL]\n")
md.append("| run | o que | recibo | veredito | bateria |\n|---|---|---|---|---|")
if r1a:
    md.append("| 1a | pré-selo, ensaio, Bancada **b1** (manifesto pina o Nós REAL), **Nós real v391** (`%s`) | `%s` | `%s` | %s |" % (r1a["nos"]["um_py"]["sha256"][:16], sha(r1a_p)[:16], r1a["veredito"], bat(r1a)))
if r1b:
    md.append("| 1b | pré-selo, ensaio, Bancada **b2** (manifesto pina `nos\\`, cópia do Nós v391) | `%s` | `%s` | %s |" % (sha(r1b_p)[:16], r1b["veredito"], bat(r1b)))
md.append("| selo do sandbox | `nos\\` recebe os bytes do Nós sintético v392 (`um.py` `%s`, selo `%s`) no MESMO caminho pinado por b2 | — | — | — |" % (s16(P["sandbox"].get("nos_v392/um.py")), s16(P["sandbox"].get("nos_v392/um_absoluto_selo.json"))))
if r2:
    md.append("| 2 | pós-selo, **aplicar** `--sandbox`, Bancada b2, evento **encadeado %d** do livro de ensaio (verificado=%s; cadeia conferida até o elo %d), recibo pré-selo do 1b (`%s`), recibo do kernel sintético, `--bateria-sha256` | `%s` | `%s` | %s |"
              % (r2["evento_c1"]["evento"], r2["evento_c1"]["verificado"], r2["evento_c1"]["cadeia_conferida_ate"], r2["recibo_pre_selo"]["sha256"][:16], sha(r2_p)[:16], r2["veredito"], bat(r2)))
    md.append("\nNo run 2 o `canonical.py` instalado em b2 recusou o pino velho **de verdade** (`pino_velho_recusado_pelo_instalado = %s`, sem sonda em RAM); manifesto B3 `%s` (`%s`) gravado em b2 com backup (`%s` = o manifesto anterior), contrato `CONTRATO_CANONICO_B3.md` `%s`, recibo copiado para `b2\\estado\\sincronizacao\\`; reconferência pós-gravação ok=%s, versão `%s`, β runtime `%s` = β do contrato bit a bit; β core `%s` (dif. rel. %.2e, tolerância nomeada %g). Re-execução (`RUN_2bis_idempotente`): `JA_SINCRONIZADA__NADA_A_GRAVAR`.\n"
              % (r2.get("pino_velho_recusado_pelo_instalado"), r2["manifesto_novo"]["deployment_id"], r2["manifesto_novo"]["sha256"][:16], r2["aplicacao"]["backup_sha256"][:16], r2["manifesto_novo"]["contrato_sha256"][:16],
                 r2["aplicacao"]["pos_conferencia"]["ok"], r2["aplicacao"]["pos_conferencia"]["canonical_version"], r2["nos"]["beta_runtime"], r2["nos"]["core"]["beta_core"], r2["nos"]["core"]["beta_rel_diff"], r2["nos"]["core"]["tolerancia_rel"]))
md.append("## A tabela: achado → conserto → teste negativo → resultado\n")
md.append("| achado (auditoria) | o que a R1 fazia | conserto R2 | teste negativo novo | resultado [REAL] |\n|---|---|---|---|---|")
for a, b, c, d, e in linhas:
    md.append("| %s | %s | %s | %s | %s |" % (a, b, c, d, e))
md.append("\n## O que mudou na forma de uso (para a cadeia e para a re-auditoria)\n")
md.append("- Flags novas: `--bateria-sha256` (obrigatória em `aplicar`), `--reparo-de-pino` (só `aplicar`, com evento `dados.reparo=true`), `--eventos` (livro alternativo, só `--sandbox`). "
          "`aplicar` só na fase `pos_selo` (salvo reparo). O evento c1 é do tipo `SINCRONIZACAO_BANCADA` com `dados` JSON `{versao, bancada, acao:\"sincronizacao\", um_py, selo, gravacoes, unidade}` (o comando `iald.py anotar` do desenho §4 ganha `\"acao\":\"sincronizacao\"`; nenhum texto de negação).")
md.append("- A bateria R2 (`R2\\BATERIA_VINCULO.json`) usa `{fonte:N}` e `testes_sha256`; a R1 não é mais aceita (`BATERIA_SEM_PINOS_POR_TESTE`). Os testes `bateria\\*.py` continuam os da R1, pinados por sha256 no lugar onde estão.")
md.append("- O sandbox só é admitido para uma cópia cujo manifesto pina um Nós de ensaio (`montar_sandbox.py` monta `b2` assim); uma cópia byte a byte da produção (`b1`) serve ao ensaio pré-selo com o Nós real, sem `--sandbox`.")
md.append("- `montar_sandbox.py` exige raiz `C:\\t\\…` (T16); `rodar_sandbox_r2.sh [raiz]` remonta e roda tudo (`controles_negativos_r2.py`).\n")
md.append("## Limites e o que fica aberto [OPEN]\n")
md.append("- O T17 real: nenhum kernel foi construído; o recibo do kernel do sandbox é **fixture marcada** (`nota: FIXTURE SINTETICA`). O contrato do `KERNEL_RECIBO_vNNN.json` (`versao, rc, sorry, build_full_log_sha256[, build_full_log, um_py_sha256, tgl_kernel_proof_manifest_sha256]`) é o que a etapa 2 da cadeia tem de escrever.")
md.append("- `SERVICO_NO_AR` segue exercitado só pela ausência do serviço (porta 18777 fechada); o religamento e a reconexão MCP ficam fora do esboço, de propósito.")
md.append("- A produção nunca foi alvo de `aplicar` (proibido); tudo em cópias. A identidade por `samefile` depende de o caminho existir; para caminhos inexistentes o fallback é o caminho canônico sem caixa.")
md.append("- O verificador de eventos é uma **reimplementação** da regra de `iald.py verificar()` (o módulo não foi importado para evitar efeitos); se a regra do quadro mudar, as duas têm de mudar juntas.")
md.append("- `--saida` fora de `work\\` e `C:\\t` é recusado: a cadeia usa `work\\vNNN_bateria\\`; outra raiz exige mudar `RAIZES_SAIDA` no esboço (decisão da gerência, com evento).")
md.append("- A instalação na cadeia (passo B(n), `derivar_cadeia_v392.py`), a B3 da v392 e a re-auditoria por cético que não construiu são atos da gerência e do operador; a F0.6 não fecha com esta R2.\n")
md.append("## Entregáveis R2 (hashes em `PINOS_R2.json`)\n")
for n, d in E.items():
    md.append("- `%s` — `%s` (%s B)" % (n, d.get("sha256", "?")[:16], d.get("bytes", "?")))
md.append("\nNada aqui é leitura física; um PASSA é validade na face testada; a creditação é ato de quem observa de fora. NOT_FALSIFIED nunca é creditação.\n")
(AQUI / "RESULTADO_R2.md").write_text("\n".join(md), encoding="utf-8")
print("RESULTADO_R2.md", hashlib.sha256((AQUI / "RESULTADO_R2.md").read_bytes()).hexdigest()[:16])

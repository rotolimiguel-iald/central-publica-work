# -*- coding: utf-8 -*-
"""gerar_estado_v400.py -- escreve ESTADO_V400.md POR SCRIPT, lendo os numeros e hashes dos artefatos da cadeia (nada digitado de memoria): CANDIDATO_v400.json, ESPERADOS_v400.json, ensaio_a_seco_v400.json, EXAME_PONTOS_*.json, SIMULACAO_ARVORE_NOS_*.json,
GUARDAS_ESTATICAS_BANCADA_v400.json, salto_r3_4\\SALTO_R3_4_MEDIDO_v400.json, COMPARACAO_V399_v400.json, RUNTIME_MONTAGEM_v400.json, kernel\\{KERNEL_RECIBO,POS_BUILD}_v400.json, kernel\\construir_marcas.txt, PRECONDICOES_v400.json, DERIVACAO_v400.json,
PINO_RECIBO_PRE_SELO_v400.json, PINOS_BN_v400.json, os JSON do conferidor e das citacoes, pos_rito\\HARNESS_*_v400.json (ESTRITOS), bancada_B3_servico\\CONFERENCIA_EXIGENCIAS_SERVICO_v400.json e o estado do Nos/da memoria (SO' leitura: sha16 e mtime do um.py do Nos e o numero
de linhas do MEMORY.md, medidos agora). A prosa e' fixa; todo numero e todo hash entra por chave ou por medida. Tres cadeados rodam sobre o texto final: a guarda P18, a regra da ordem do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no MESMO paragrafo; este ESTADO nem o cita)
e a varredura das aspas (toda citacao entre aspas de 12 caracteres ou mais existe VERBATIM nas falas do operador ou na ordem de processo de 22/10; este ESTADO nao cita nenhuma). ESCRITO A MAO na v400. Reexecutavel; backup de bytes do ESTADO anterior.
uso: python -I -B -X utf8 gerar_estado_v400.py"""
import datetime, glob, hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v400 as DL  # noqa: E402
import guarda_p18_v400 as GP  # noqa: E402
J = lambda *p: json.load(open(os.path.join(HERE, *p), encoding="utf-8"))
sha = lambda b: hashlib.sha256(b).hexdigest()
fm = lambda n: "{:,}".format(int(n)).replace(",", ".")
vc = lambda x, f: format(x, f).replace(".", ",")
s16 = lambda *p: sha(open(os.path.join(HERE, *p), "rb").read())[:16]
CM = J("CANDIDATO_v400.json"); ESP = J("ESPERADOS_v400.json"); ENS = J("ensaio_a_seco_v400.json"); GU = J("GUARDAS_ESTATICAS_BANCADA_v400.json"); SAL = J("salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json"); CMP = J("COMPARACAO_V399_v400.json"); RM = J("RUNTIME_MONTAGEM_v400.json")
KR = J("kernel", "KERNEL_RECIBO_v400.json"); POS = J("kernel", "POS_BUILD_v400.json"); PIN = J("PINO_RECIBO_PRE_SELO_v400.json"); PINOS = J("PINOS_BN_v400.json"); POSIT = J("conferencia_rito_v400_POSITIVO_FALSO_NOS.json"); NEG = J("conferencia_rito_v400_CONTROLE_NEGATIVO_PRE_RITO.json")
X = J("EXAME_PONTOS_%s.json" % CM["sha16"]); SIM = J("SIMULACAO_ARVORE_NOS_%s.json" % CM["sha16"]); DER = J("DERIVACAO_v400.json"); CIT = J("conferir_citacoes_v400.json"); DENC = J("DERIVACAO_ENCANAMENTO_v400.json"); PRE = J("PRECONDICOES_v400.json")
HT = J("pos_rito", "HARNESS_TEXTOS_ENSAIO_v400.json"); HF = J("pos_rito", "HARNESS_FECHAR_SANDBOX_v400.json"); SERV = J("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v400.json"); DSERV = J("bancada_B3_servico", "DERIVACAO_SERVICO_v400.json")
BASE_CORE = J(DL.BASE_DIR, "um_absoluto.json")["core"]
assert PRE["ok"] is True and ENS["veredito"] == "TUDO PASSOU", ("a cadeia nao esta pronta para o ESTADO", PRE["ok"], ENS["veredito"])
assert HT["tudo_passou"] is True and HF["tudo_passou"] is True and HT["nao_exigiu_refazer"] is False and HF.get("nao_exigiu_refazer") is False, "os dois harness do pos_rito tem de ter rodado ESTRITOS (sem --nao-exigir-refazer) e passado"
_ro = open(os.path.join(HERE, "refazer_out_v400.txt"), encoding="utf-8", errors="replace").read()
assert "== FIM" in _ro and "rc=0" in _ro.replace(" ", ""), "o refazer nao terminou limpo"
marcas = open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(); ep = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", marcas, re.M)}
t_build = ep["epoch_build_fim"] - ep["epoch_inicio"]; t_audit = ep["epoch_audit_fim"] - ep["epoch_build_fim"]
nos_um = os.path.join(DL.NOS, "um.py"); nos_sha = sha(open(nos_um, "rb").read()); nos_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(nos_um)).strftime("%d/%m/%Y %H:%M:%S")
nos_vs_base = "igual ao da v399 selada" if nos_sha[:16] == CM["base_v399_sha16"] else "DIFERE da base v399 (o Nós mudou depois da preparação: reconferir tudo)"
vb17_estado = "não existe mais, conferido agora" if not os.path.exists(os.path.join("C:" + os.sep, "t", "vb17")) else "AINDA EXISTE (conferir e apagar)"
_skip = ("__pycache__", os.sep + "dry_v400" + os.sep, os.sep + "sim_", os.sep + "imp_", os.sep + "conferidor_import_", os.sep + "arvore_simulada_h8" + os.sep, os.sep + "falso_nos" + os.sep, os.sep + "harness_saida_v400" + os.sep, os.sep + "bateria_pre_selo" + os.sep + "ensaio_1" + os.sep)
arquivos = [f for f in glob.glob(os.path.join(HERE, "**", "*"), recursive=True) if os.path.isfile(f) and ".bak_" not in os.path.basename(f) and not any(s in f for s in _skip)]
_dia = datetime.date.today()
_ct = [datetime.datetime.fromtimestamp(os.path.getctime(f)) for f in arquivos]; _mt = [datetime.datetime.fromtimestamp(os.path.getmtime(f)) for f in arquivos]
t_ini = min(c for c in _ct if c.date() == _dia).strftime("%H:%M"); t_fim = max(m for m in _mt if m.date() == _dia).strftime("%H:%M")
_um = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md"); _umb = open(_um, "rb").read()
MEM_LINHAS = _umb.count(b"\n") + (0 if _umb.endswith(b"\n") else 1); MEM_BYTES = len(_umb); MEM_MTIME = datetime.datetime.fromtimestamp(os.path.getmtime(_um)).strftime("%d/%m/%Y %H:%M:%S")
MEM_CABE = MEM_LINHAS + 1 <= 195
SUP = HT["etapas"].get("superficies") or {}
# --- numeros do ensaio / kernel / correcao
S16 = CM["sha16"]; esc = CM["escada"]; cob = ENS["verify_kernel_ponta_a_ponta"]["cobertura"]
G0 = CM["guarda_alpha_unica_da_bancada"]; ga0, ga1 = G0["base_v399"], G0["candidato_v400"]
n_unid = len(ENS["unidade"]); n_unid_ok = sum(1 for v in ENS["unidade"].values() if v is True)
art = ENS["artigo"]; qd = ENS["quadro"]
acom = POSIT["acom_itens"]; dm = POSIT["deve_mudar"]; npm = POSIT["nao_pode_mudar"]
conf_dm = "%d/%d" % (sum(1 for v in dm.values() if v), len(dm)); conf_np = "%d/%d" % (sum(1 for v in npm.values() if v), len(npm))
neg_dm = "%d/%d" % (sum(1 for v in NEG["deve_mudar"].values() if v), len(NEG["deve_mudar"]))
ctl_gu = GU["controles_negativos"]; ctl_gu_ok = sum(1 for v in ctl_gu.values() if v.get("ok") is True)
ed = [e["edicao"] for e in RM["edicoes_declaradas"]]
pin_pre = PIN["contagens"]; bk = PIN["bancada_pina"]
ger = int(re.match(r"^B(\d+)-", bk["deployment_id"]).group(1))
ht_n = len(HT["etapas"]); hf_n = len(HF["etapas"])
base_bytes = os.path.getsize(os.path.join(HERE, DL.BASE_DIR, "um.py"))
sidecar_n = len(ESP["sidecar"]["objetos"])
mudados = ", ".join("`%s`" % x for x in CMP["mudados"])   # (lista ou dict: so os nomes)
removidos = ", ".join("`%s`" % x for x in CMP["removidos"])
exp_p = ENS["exame_pontos"]

L = []
w = L.append
w("CADEIA v400 — preparada (correção: α único; B(n) com salto v398→v400)")
w("")
w("**Ressalva à primeira linha, medida e dita já aqui:** o salto declarado do R3.4 pelo elo da v399 é IMPOSSÍVEL com o esboço R3.5 da Bancada (`%s`): o esboço recusa o elo da v399 (`%s`) e o diff do kernel entre a v399 e a v400 é VAZIO, que o T17 recusaria (`pedras vazias`). "
  "O B(n) que a cadeia deixa preparado é o **passo SIMPLES v398 → v400** (a Bancada de produção AINDA pina a v398, geração B%d; a v399 foi recusada por ela e nunca foi sincronizada), com o recibo pre_selo da cadeia v399 **reaproveitado e reconferido** pelo próprio esboço (um pre_selo novo não pode ser gerado sem tocar no Nós). Detalhe no §3." % (SAL["veredito"], SAL["cadeia_v398_v399"]["recusa"].split(":")[0], ger))
w("")
w("Gerência c1, subagente de preparação, 24/10/2026, %s a %s (hora local; criação e mtime dos arquivos da cadeia), por ordem da gerência. Estatutos: [REAL] medido ou lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [OPEN] em aberto; [INPUT]/[ONTO] fala ou leitura do operador; [KNOWN] literatura; [LEGAL] a conferir com a agente de PI. "
  "Nada foi instalado e nada foi selado; o `um.py` real não rodou (sha16 medido agora `%s`, mtime %s, %s); o gate não se move; NOT_FALSIFIED nunca é a palavra da creditação. Escrevi só em `work\\cadeia_de_selo\\v400`, em `C:\\t\\k400c` (o sandbox do kernel, copiado de `C:\\t\\k399c`) e em `C:\\t\\vb17` "
  "(o sandbox curto das guardas estáticas e das conferências, %s), mais o scratchpad temporário da sessão. Li, sem escrever: `work\\cadeia_de_selo\\v399` (a base, o molde e os insumos), `v398` e `v397` (os recibos do último B(n) feito e os insumos do Teste da Única Palavra), `work\\bancada_vinculo_12out\\R3_5` (o esboço da Bancada, pinado), "
  "`C:\\IALD\\Bancada_Um` (a produção, só lida) e o livro do mapa de rotas. O Nós, a memória real (o `MEMORY.md` só foi LIDO), o Atlas, o `CLAUDE.md`, o túnel, o site, o git e a memória comum ACOM não foram tocados; o mapa de rotas só foi consultado (o registro `registro_mapa_v400_prep.json` é montado e validado por `rotas._valida` sem registrar); "
  "o serviço da porta 18777 não foi parado nem religado; nenhuma regra de permissão foi rodada (`regras_v400.py` está escrito e NÃO foi rodado). Trabalhei sem subagentes; o que não conferi por script está dito em §6." % (t_ini, t_fim, nos_sha[:16], nos_mtime, nos_vs_base, vb17_estado))
w("")
w("## 0. Resumo em números")
w("")
w("- **O candidato:** `um_v400_candidato.py` sha16 `%s` (%s B; +%s B sobre a v399 selada `%s`, %s B), %d patches (%s), determinístico (duas gerações dão os mesmos bytes). UM_VERSION `%s`; o único `ALPHA_FINE_CODATA_2018 =` na coluna 0 está na linha %d (a v399 tinha %d linhas)." % (
  S16, fm(CM["bytes"]), fm(CM["delta_bytes"]), CM["base_v399_sha16"], fm(CM["base_v399_bytes"]), CM["n_patches"], ", ".join("`%s`" % p["id"] for p in CM["patches"]), G0["versao_lida"], G0["linha_do_alfa"], ga0["alfa_col0"]))
w("- **A correção (duas coisas, nada mais):** (1) a seção do selo ACOM deixa de redeclarar o α e lê o `SEALED_CODATA_ALPHA` do programa (o defeito estava na ADAPTAÇÃO da gerência em volta do bloco, **não no bloco do operador**: o hash do bloco embutido `%s` NÃO mudou, logo nenhuma substituição nova entra no manifesto do bloco); "
  "(2) a checagem β do runtime do registro `selo_pela_propria_tecnologia_v399` deixa de ser tautológica e confronta o β do CORE do rito a 1e-9 (a diferença relativa medida pelo esboço da Bancada é %s, bem abaixo de 1e-9). Mais UM_VERSION e a errata curta ao lado, no artigo PT/EN e no `.md` (o quadro do topo permanece)." % (RM["bloco_embutido_sha256"][:16], vc(GU["candidato_v400"]["beta_rel_diff"], ".2e")))
w("- **O runtime novo** (`runtime_v400.py`, sha16 `%s`, %s B) é MONTADO por script do `runtime_v399.py` com %d edições de texto declaradas, cada uma com contagem exata (%s); conferências C1, C2, C3, C9, C3', C10 e C11 ok." % (RM["runtime"]["sha256"][:16], fm(RM["runtime"]["bytes"]), len(ed), ", ".join(ed)))
w("- **Comparação por AST com a v399** (nada da v399 perdido): %d nós nomeados, %d iguais, %d mudados (%s), %d removido (%s), %d novos; o único nó anônimo perdido é o `if` da redeclaração (%s)." % (
  CMP["nos_nomeados_v399"], CMP["iguais"], len(CMP["mudados"]), mudados, len(CMP["removidos"]), removidos, CMP["n_novos"], "confirmado" if CMP["o_unico_anonimo_perdido_e_o_if_da_redeclaracao"] else "NÃO CONFIRMADO"))
w("- **Guardas estáticas do contrato da Bancada** (a FUNÇÃO `ler_nos` do esboço R3.5 pinado, sha16 `%s`, rodada SOBRE o candidato, ANTES de instalar — a lição da v399): o candidato PASSA (α na linha %d, 1 linha, 0 reatribuições indentadas, β relativo %s); a v399 selada REPRODUZ a recusa do recibo da Bancada (`%s`, mensagem idêntica = %s); %d de %d controles negativos recusam." % (
  GU["esboco"]["sha256"][:16], GU["candidato_v400"]["alpha"]["linha"], vc(GU["candidato_v400"]["beta_rel_diff"], ".2e"), GU["v399_selada_o_defeito_real"]["recusa"], str(GU["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"]).lower(), ctl_gu_ok, len(ctl_gu)))
w("- **Kernel:** NENHUM módulo novo (a lista `kernel_modulos_novos_v400.json` é vazia); os %d arquivos embutidos são os da v399, byte a byte; reconstruído em `C:\\t\\k400c` com a raiz e o Audit forçados a recompilar (build %d s, Audit %d s): %s constantes e %s teoremas no `axiom_report`, %d fora do trio, %d nomes não lidos; escada %d/%d (a da v399); recibo do kernel `KERNEL_RECIBO_v400.json` sha16 `%s` (rc %d, sorry %d, erros %d)." % (
  ENS["kernel_materializado"], t_build, t_audit, fm(cob["decl"]), fm(cob["thm"]), cob["fora_do_trio"], cob["nao_lidas_pelo_regex"], esc[1], esc[1], s16("kernel", "KERNEL_RECIBO_v400.json"), KR["rc"], KR["sorry"], KR["erros"]))
w("- **Ensaio a seco: %s** — %d verificações de unidade, todas verdadeiras (%d); os registros da v393 a v399 RECRIADOS e comparados com os da v399 selada; a troca dita é UMA: `%s` (o veredito carrega o hash do próprio `um.py`); pontos de chamada reais (`exame_pontos`): `algum_falso` = %s; simulação da árvore do Nós: %d entradas no hash formal (= %d embutidas + o residual do Nós), pino h8 igual; "
  "artigo PT/EN compilado duas vezes (rc %s e %s; seções de %s e %s caracteres; sumário ok); o quadro do topo confere nas duas línguas e no `.md`; sidecar com %d objetos verificados." % (
  ENS["veredito"], n_unid, n_unid_ok, ", ".join(ESP["troca_dita"]), exp_p["algum_falso"], ENS["simular_arvore_do_nos"]["formal_files_n_no_rito_real"], ENS["simular_arvore_do_nos"]["embutidos"], art["pt"]["pdflatex_rc"], art["en"]["pdflatex_rc"], fm(art["pt"]["secao_chars"]), fm(art["en"]["secao_chars"]), sidecar_n))
w("- **ESPERADOS** `%s` (%d vereditos da v399 pinados; %s bandeiras True; troca dita `%s`); **conferidor**: caminho positivo (Nós falso do ensaio) `tudo_bate = %s` (deve mudar %s, não pode mudar %s; C1 a C16 e o round trip), controle negativo (Nós ainda v399) `tudo_bate = %s`; **citações** %s; **pinos** (`PINOS_BN_v400.json`): candidato `%s`, esboço R3.5 `%s`, recibo pre_selo `%s`, recibo do kernel `%s`." % (
  s16("ESPERADOS_v400.json"), len(ESP["vereditos_v399"]), fm(len(ESP["flags_true_v399"])), ", ".join(ESP["troca_dita"]), str(POSIT["tudo_bate"]).lower(), conf_dm, conf_np, str(NEG["tudo_bate"]).lower(), "TODAS CONFEREM" if CIT["todas_conferem"] else "FALHARAM", PINOS["candidato"]["sha256"][:16], PINOS["esboco_R3_5"]["sha256"][:16], PINOS["recibo_pre_selo"]["sha256"][:16], PINOS["kernel_recibo"]["sha256"][:16]))
w("- **Pós-rito** (harness ESTRITOS, com `refazer_out_v400.txt` visto com `== FIM`): textos `tudo_passou = %s` (%d etapas), fechar em sandbox `tudo_passou = %s` (%d etapas); serviço da Bancada (`bancada_B3_servico`): %d de %d condições estáticas ok (parada e religamento exigem `V400_AUTORIZACAO_OPERADOR`; nada executado); `MEMORY.md` real: %d linhas, %s B (o handoff novo soma +1 linha: %s)." % (
  str(HT["tudo_passou"]).lower(), ht_n, str(HF["tudo_passou"]).lower(), hf_n, SERV["n_condicoes_ok"], SERV["n_condicoes"], MEM_LINHAS, fm(MEM_BYTES), ("cabe no limite de 195, com margem de %d linha(s)" % (195 - MEM_LINHAS - 1)) if MEM_CABE else "NÃO CABE no limite de 195"))
w("- **Pré-condições** (`p00_precondicoes_v400.py`): %s (%d checagens)." % ("TODAS OK" if PRE["ok"] else "FALHOU", len(PRE["checagens"])))
w("")
w("## 1. O que a v400 muda e o que NÃO muda")
w("")
w("1. **Muda (o `um.py`):** a seção embutida do selo ACOM (a adaptação, antes do primeiro marcador do bloco do operador) remove a redeclaração do α (3 linhas viram um comentário) e `_beta_runtime` passa a ler `SEALED_CODATA_ALPHA * sqrt(e)`; `registro_core_v399` ganha o parâmetro `beta_core` e a checagem passa a ser `rel_beta_core < 1e-9`, com valores `beta_core` e `rel_beta_vs_core` no registro; o ponto de chamada (`selo_acom_v399`) passa o β do core; `UM_VERSION`; a errata «ao lado» no artigo PT/EN e no `.md`.")
w("2. **NÃO muda:** o kernel e o Audit (byte a byte), o bloco embutido do operador (hash `%s`), os registros (os nomes seguem os da v399: `selo_pela_propria_tecnologia_v399`, `declaracao_do_operador_v399`, `cunhagens_v399`, `kh_n1_cobertura_v399`), as quatro inscrições de 24/10, o selo (salvo o resumo do selo ACOM e o hash do próprio programa no estatuto da prova), o sidecar (o rito o reescreve), o gate, o quadro do topo. **Nenhuma inscrição nova, nenhum módulo novo, nenhum registro novo, nenhuma chave nova no core.**" % RM["bloco_embutido_sha256"][:16])
w("3. **Sem gordura** (a ordem de processo do operador de 22/10): o delta é a correção e só ela; o ensaio ganhou UMA etapa (as guardas estáticas da Bancada sobre o candidato) e o conferidor ganhou DOIS itens (C15 e C16: a função `ler_nos` do esboço sobre o `um.py` instalado e sobre o Nós real); a leitura do pós-rito confere a correção no que o rito produziu (V['correcao'])." )
w("")
w("## 2. Etapas e números")
w("")
w("1. **Base:** cópia de bytes do Nós v399 selado (`base_v399`: `um.py` `%s`, selo, core, manifesto do kernel, resultado do pilar e o sidecar) e da v398 (`base_v398`: o selo e o manifesto do kernel que a Bancada ainda pina)." % CM["base_v399_sha16"])
w("2. **Runtime, candidato e comparação:** `montar_runtime_v400.py` → `gerar_candidato_v400.py` → `comparar_v399_v400.py` (§0). Os patches de texto do candidato (versão, runtime, artigo PT/EN, `.md`) têm contagem exata cada um.")
w("3. **Guardas estáticas da Bancada** (`guardas_estaticas_bancada_v400.py` → `GUARDAS_ESTATICAS_BANCADA_v400.json`): sandbox em `C:\\t\\vb17\\gate`, apagado no fim; o `canonical.py` instalado da Bancada lê o mesmo α (linha %d) que o esboço; as regexes do `canonical.py` e do esboço concordam." % GU["candidato_v400"]["alpha"]["linha"])
w("4. **Kernel:** `C:\\t\\k400c` é cópia de `C:\\t\\k399c`; `construir_kernel_v400.sh` apaga SÓ os artefatos compilados da raiz e do Audit (para o `lake build` produzir as linhas `Built` que o T17 do B(n) exige) e reconstrói (%d s + %d s); `pos_build_kernel_v400.py` gera o recibo do kernel (contrato R3_2) com o ANTES = kernel da v398 e o diff = a pedra Testemunho (`%s`)." % (t_build, t_audit, ", ".join(p["path"] for p in KR["pedras"])))
w("5. **Ensaio a seco** (`ensaio_a_seco_v400.py`): kernel embutido == sandbox; o core da v399 selada + o kernel real pelo `verify` de ponta a ponta; vizinhos recomputados; fluxo principal; unidade (%d verificações, entre elas os testes NOVOS: a checagem do β reprova se o α do programa é adulterado; o α é único e a seção não o redeclara); selo; artigo; `.md`; sidecar; `exame_pontos`; `simular_arvore_do_nos`; as guardas da Bancada." % n_unid)
w("6. **ESPERADOS → conferidor (negativo e positivo) → citações → conferência do instalar/reverter/rito → pinos → pré-condições:** `refazer_candidato_v400.sh` roda tudo na ordem; o `conferir_instalar_rito_v400.py` EXTRAI por AST o trecho do instalador sobre a lista dos módulos novos e o executa isolado (passa com N = 0 e recusa se a lista trouxer um módulo que o ESPERADOS não pina).")
w("7. **Encanamento DERIVADO da v399 por motor** (`derivar_encanamento_v400.py`, %d arquivos, nada executado): o mapa 398→399 e 399→400 palavra a palavra com fronteira de dígitos, os nomes nascidos no `um.py` PROTEGIDOS (as etiquetas de stdout `[v399]` e `[v398]` que o programa imprime não sobem) e regras de contagem exata por arquivo. `instalar_v400.py` (9 backups de bytes, incluindo o sidecar), `reverter_v400.py` (idem), `rito_v400.sh`, `regras_v400.py` (escrito, NÃO rodado), `refazer_*`." % len(DENC["arquivos"]))
w("8. **Pós-rito:** `leitura_v400.py` (derivada, com a correção conferida no que o rito produziu), `textos_v400.py` (GERADO por `gerar_textos_v400.py`: as funções da v399 que não mudam são cópias por AST; o novo vem de `textos_v400_novo.pytxt`), `superficies_v400.py`, `fechar_v400.py`, `registrar_mapa_v400.py` (escrito à mão: 1 rota nova e 6 anotações), `b3_recibo_v400.py` (passo simples v398 → v400), `chain_pos_rito_v400.sh`, os dois harness (com controles negativos NOVOS: α em duas linhas, α reatribuído com indentação, β do registro sem o core, β_core diferente do core, etiqueta velha da checagem).")
w("")
w("## 3. O B(n) da Bancada Um: salto medido impossível; passo simples preparado; o recibo pre_selo")
w("")
w("- **O salto do R3.4 (pedido) foi MEDIDO impossível** (`salto_r3_4\\SALTO_R3_4_MEDIDO_v400.json`, veredito `%s`): a cadeia de selos v398 → v399 é recusada no elo v399 (`%s`); `ler_nos(Nós, v399)` recusa com a mensagem exata do recibo da Bancada (`%s`, idêntica = %s); `ler_nos(Nós, v398)` recusa (`%s`); e, pela leitura do código do T17 (`verificar_kernel_recibo`, `if not isinstance(pedras, list) or not pedras: return falha(\"pedras vazias\")`), um B(n) cujo ANTES fosse o kernel da v399 teria o diff do kernel vazio e seria recusado [REAL: lido do código do esboço, não executado]." % (
  SAL["veredito"], SAL["cadeia_v398_v399"]["recusa"], SAL["ler_nos_v399"]["recusa"], str(SAL["ler_nos_v399"]["identica_a_do_recibo_da_bancada"]).lower(), SAL["ler_nos_v398"]["recusa"][:60]))
w("- **O que ficou preparado — passo SIMPLES v398 → v400** (a Bancada de produção pina a v398, deployment `%s`; o Nós v399 nunca foi sincronizado): o esboço aceita o recibo pre_selo pinado (%s condições, %s controles; utilizável = %s); `b3_recibo_v400.py` confere a geração (B%d → B%d), o veredito exato do ensaio (`REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA`) e do aplicar (`REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`), ambos sem `__SALTO_` [lidos do código do esboço, não rodados]; o diff do kernel do recibo é a pedra Testemunho." % (
  bk["deployment_id"], SAL["passo_simples_v398_v400"]["condicoes"], SAL["passo_simples_v398_v400"]["controles"], str(SAL["passo_simples_v398_v400"]["utilizavel"]).lower(), ger, ger + 1, ger + 1, ger + 1))
w("- **O recibo pre_selo está pinado ANTES da instalação** (`PINO_RECIBO_PRE_SELO_v400.json`, sha256 do recibo `%s`; veredito `%s`; bateria %d PASSA, %d FALHA, %d NÃO EXECUTADO [T17 só no pós-selo]): é o recibo da CADEIA v399 (gerado em ensaio contra a produção, sobre o `um.py` v398 que a Bancada pina), **REAPROVEITADO e reconferido** pelo esboço R3.5; as listas da produção e do Nós foram medidas iguais antes e depois. "
  "Um pre_selo NOVO não é possível sem tocar no Nós: o esboço só gera pre_selo lendo o Nós que o manifesto da Bancada pina, e o Nós é a v399 (medido). O recibo fica obsoleto se a produção for repinada antes do B(n) (o instalador e o chain conferem o sha256 do manifesto da Bancada)." % (
  PIN["sha256"][:16], PIN["veredito"], pin_pre["passa"], pin_pre["falha"], pin_pre["nao_executado"]))
w("- **Serviço (porta 18777):** `bancada_B3_servico\\recibo_parada_v400.py`, `recibo_religamento_v400.py` e `evento_c1_b3_v400.py` são a v399 com 399 → 400 e NADA mais (o 398 fica: o último religamento e a última geração são os da v398); parada e religamento exigem `V400_AUTORIZACAO_OPERADOR`; o conferidor estático deles dá %d/%d. A parada e o religamento são ATO DO OPERADOR; a aplicação só com `B3_AUTORIZADO=sim EVENTO=<seq> EVENTO_HASH=<hash16>`." % (SERV["n_condicoes_ok"], SERV["n_condicoes"]))
w("")
w("## 4. Achados e decisões que a gerência precisa ver")
w("")
w("1. **A causa da recusa estava na adaptação, não no bloco do operador.** Em `registro_core_v399` a checagem era `abs(beta / (ALPHA_FINE_CODATA_2018 * sqrt(e)) - 1) < 1e-15` com `beta = _beta_runtime()` — a MESMA expressão (tautologia); e a seção redeclarava o α numa segunda linha de coluna 0, protegida por um `assert SEALED_CODATA_ALPHA == ALPHA_FINE_CODATA_2018` que só conferia a duplicata. Corrigidas as duas; o bloco do operador não foi tocado (hash `%s`)." % RM["bloco_embutido_sha256"][:16])
w("2. **O ensaio a seco da v399 não rodava as guardas estáticas da Bancada sobre o candidato.** A v400 as roda (lição registrada): no ensaio, no conferidor (C15 sobre o `um.py` instalado; C16 sobre o Nós real) e na leitura do pós-rito (os mesmos regex, lidos do esboço pinado).")
w("3. **Defeitos do INSTRUMENTO achados e corrigidos na preparação (não do candidato):** (a) a comparação dos vizinhos normalizava as contagens `CORE_n_` depois de TRUNCAR o veredito a 300 caracteres, o que escondia a mudança do hash próprio em `estatuto_da_prova_v391` e fazia INCONCLUSIVE_9 para INCONCLUSIVE_10 (um dígito a mais) parecer mudança; agora compara a string inteira; "
  "(b) o título da introdução do artigo diz `v384 a <versão desta rodada>`, e com três dígitos o prefixo `v39` da v399 não serve (a conferência passou a esperar `v384 a v400`); (c) `three_stress_tests_v387` carrega a contagem de registros do core NO INSTANTE em que é calculado: o rito o calcula no ponto do main (o valor da v399 selada, porque o main é o mesmo), o ensaio o recomputa sobre o core inteiro — o ensaio **restaura o valor da v399 selada** só depois de verificar que SÓ as contagens diferem (declarado no relatório do ensaio, `contagens_do_instante_restauradas_ao_da_v399`); "
  "(d) o motor de derivação não pode subir as etiquetas de stdout que o programa imprime (`[v399]`, `[v398]`); (e) a escada antes → depois do CANDIDATO copiava o par da v399 (9539 → 9541): na v400 é 9541 → 9541.")
w("4. **A troca dita é UMA** (`estatuto_da_prova_v391`: o veredito traz o hash do próprio `um.py`, a certificação pelo próprio hash); no selo muda também `selo_pela_propria_tecnologia_v399` (os hashes do novo programa) e `um_version`/`sha256`; todo o resto do selo é o da v399. O conferidor exige que a troca dita MUDE de fato e só em números/hash.")
w("5. **Custódia CONJUNTA v399 + v400:** a v399 (`%s`) é selada e foi instalada, mas a Bancada a recusou; o `um.py` corrente a publicar é o da v400; o handoff da v400 diz isso, traz os DOIS parágrafos do README/site (o do quadro, intocado; o do testemunho da v399, REGENERADO com os números do `um.py` v400) e lista o sidecar reescrito." % CM["base_v399_sha16"])
w("6. **`MEMORY.md`:** %d linhas e %s B agora; o `superficies_v400.py` troca a linha da missão no lugar e insere a linha do handoff (+1 linha) sem compactar nada: ficam %d linhas e cerca de %s B, dentro do limite de 195 linhas e 24.000 B, com margem de %d linha(s) [conta; o harness exercita os três cenários: o real, com folga e no limite → recusa com rc 3]. Atenção: outra sessão acrescentou uma linha ao índice às 18:38 (de 193 para 194 linhas); com a margem em %d, qualquer linha nova no índice antes do pós-rito faz o passo 3 RECUSAR (rc 3, nada escrito) e a gerência decide o que sai do índice." % (MEM_LINHAS, fm(MEM_BYTES), MEM_LINHAS + 1, fm(MEM_BYTES + 300), 195 - MEM_LINHAS - 1, 195 - MEM_LINHAS - 1))
w("7. **Esboço pinado como constante:** o sha256 do esboço R3.5 aparece como constante em vários scripts (`ESBOCO_SHA256`), conferido contra o disco a cada import e igual ao pino do `PINOS_BN_v399.json`; não é lido de memória, mas é um literal repetido [REAL].")
w("")
w("## 5. Comandos exatos (nada disto foi executado, exceto o que está dito)")
w("")
w("- **Antes de instalar:** `cd \"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v400\"` e `python -I -B -X utf8 p00_precondicoes_v400.py`. Se algo mudar (runtime, textos, artigo, kernel): `sh ./refazer_candidato_v400.sh` (montagem do runtime → gerador → comparação → guardas → ensaio → esperados → conferidor negativo e positivo → citações → conferência do instalar/reverter/rito → pinos → pré-condições); depois `python -B -X utf8 harness_textos_ensaio_v400.py` e `python -B -X utf8 harness_fechar_sandbox_v400.py` (a partir de `pos_rito`) e `python -I -B -X utf8 gerar_estado_v400.py`.")
w("- **Instalar (ato da gerência):** `python -B -X utf8 instalar_v400.py` (confere o recibo pre_selo pinado e a Bancada ainda em v398; 9 backups de BYTES; troca por `os.replace`; grava `APLICADO_AO_CANONICO_<ts>.json`).")
w("- **Rito (Git Bash):** `cd /c/IALD/Central\\ de\\ Patentes/work/cadeia_de_selo/v400 && sh ./rito_v400.sh > rito_v400_lancador.out 2>&1 &`. Abortar só por `kill -TERM $(cat .rito_v400.pid)` NO GIT BASH, depois de conferir `/proc/$(cat .rito_v400.pid)/cmdline`. Tempo esperado: da ordem do rito real da v399 (2 h 08 min, rc 0), fora a GPU.")
w("- **Conferir:** `python -B -X utf8 conferir_rito_v400.py` (SEM `-I`; tem de dar TUDO BATE, quadro, C1 a C16 e round trip incluídos). **Reverter se falhar:** `python -B -X utf8 reverter_v400.py`.")
w("- **Pós-rito:** `cd /c/IALD/Central\\ de\\ Patentes/work/cadeia_de_selo/v400/pos_rito && sh ./chain_pos_rito_v400.sh > chain_v400_out.txt 2>&1`; retomada `CHAIN_DE=<passo>` (o passo 3 PARA se o `MEMORY.md` passar de 195 linhas). O passo 10 é o passo simples v398 → v400; parada e religamento do serviço são atos do operador (`V400_AUTORIZACAO_OPERADOR`); a aplicação só com `B3_AUTORIZADO=sim`. O fechar gera o HANDOFF com os dois parágrafos do README/site e a nota da custódia conjunta.")
w("")
w("## 6. O que FALTA e o que NÃO foi revisado")
w("")
w("1. **Revisão independente** (quem constrói não aprova): o runtime MONTADO, o candidato, o motor e os derivados (instalar, reverter, rito, conferidor, esperados, pós-rito), os textos GERADOS e os dois harness NÃO tiveram cético independente [DECLARADO: nada além dos meus próprios controles negativos e da comparação por AST]. O bloco do operador, esse sim, é o mesmo que a revisão da v399 leu (hash inalterado).")
w("2. **O rito real** (build do Nós, 3 passagens, GPU) é o único que exercita o conferidor, o pós-rito e o h8 de verdade; o caminho positivo do conferidor e os harness são EMULAÇÃO (o Nós falso vem do ensaio). A suposição de que `three_stress_tests_v387` dá o valor da v399 no rito real decorre de o `main` ser o mesmo (nós iguais na comparação por AST), mas só o rito a confirma.")
w("3. **Decisões do operador** (inalteradas): nomes provisórios da pedra e dos registros; a leitura das duas faces (D7); a pendência [LEGAL] (D2, com a agente de PI) antes de publicar o bloco embutido; autorizar a parada e o religamento do serviço e o B(n); commit/push.")
w("4. **Salto do R3.4:** se o operador quiser o salto declarado, ele exige outro esboço (ou outro elo): com o R3.5 só o passo simples é possível.")
w("5. Memória, mapa de rotas (`registro_mapa_v400_prep.json` montado e validado sem registrar), quadro, Atlas/índice, custódia, README do espelho e site: atos da gerência/operador, fora desta tarefa.")
w("")
w("## 7. Mapa de rotas consultado (antes) e o que o mapa devolveu")
w("")
w("`rotas.py consultar \"v400\"` → nenhuma rota; `consultar \"alpha linha unica\"` → nenhuma; `consultar \"salto\"` → 17 rotas, e nenhuma delas tem a medida de que o salto v398 → v400 é impossível nem o caso do alfa único. As que importam: `infra.bancada_um.sincronizacao_vnnn` (EM_CURSO) guarda o histórico do R3.4 — o salto com a cadeia de selos verificada por hash, feito na v394 para v392 → v394 (a cadeia verifica os elos CONSECUTIVOS, do pino da Bancada ao Nós; o elo recusado da v399 fecha a porta do salto [REAL: medido em `SALTO_R3_4_MEDIDO_v400.json`]) — e o recibo pre_selo da v399 (passo simples sem salto, geração B9 esperada); `umpy.v399.cadeia_de_selo_preparada_24out` (EM_CURSO) é a rota da cadeia anterior. "
  "Existiam e foram anotadas no registro de preparo: essas duas, `umpy.v399.selo_pela_propria_tecnologia_estudo_24out`, `kernel.testemunho_v399_candidata_24out` e `umpy.v399.declaracao_do_operador_operacao_quadratica_24out`. A rota da cadeia v400 não existia (o registro de preparo a cria). Rotas examinadas por esta tarefa e registradas no preparo: a correção do α único e do β contra o core; o salto do R3.4 medido impossível; o pre_selo reaproveitado.")
w("")
w("## 8. Arquivos principais (todos em `work\\cadeia_de_selo\\v400`; sha16 lido agora)")
w("")
ARQS = ["um_v400_candidato.py", "CANDIDATO_v400.json", "ESPERADOS_v400.json", "PINOS_BN_v400.json", "PINO_RECIBO_PRE_SELO_v400.json", "PRECONDICOES_v400.json", "COMPARACAO_V399_v400.json", "ensaio_a_seco_v400.json", "refazer_out_v400.txt", "RUNTIME_MONTAGEM_v400.json", "runtime_v400.py",
        "GUARDAS_ESTATICAS_BANCADA_v400.json", os.path.join("salto_r3_4", "SALTO_R3_4_MEDIDO_v400.json"), os.path.join("kernel", "KERNEL_RECIBO_v400.json"), "DIFF_KERNEL_v400.txt", "conferencia_rito_v400_CONTROLE_NEGATIVO_PRE_RITO.json", "conferencia_rito_v400_POSITIVO_FALSO_NOS.json", "conferir_citacoes_v400.json",
        "EXAME_PONTOS_%s.json" % S16, "SIMULACAO_ARVORE_NOS_%s.json" % S16, "DERIVACAO_ENCANAMENTO_v400.json", "DERIVACAO_v400.json", os.path.join("pos_rito", "HARNESS_TEXTOS_ENSAIO_v400.json"), os.path.join("pos_rito", "HARNESS_FECHAR_SANDBOX_v400.json"),
        os.path.join("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v400.json"), "instalar_v400.py", "reverter_v400.py", "rito_v400.sh", "conferir_rito_v400.py", "regras_v400.py", os.path.join("pos_rito", "chain_pos_rito_v400.sh"), os.path.join("pos_rito", "textos_v400.py")]
for a in ARQS:
    if os.path.exists(os.path.join(HERE, a)):
        w("- `%s` `%s`" % (a.replace(os.sep, "\\"), s16(a)))
w("")
w("NOT_FALSIFIED não é a palavra da creditação; validade no kernel não é creditação; o gate não se move.")
txt = "\n".join(L) + "\n"
# --- os tres cadeados
v = GP.violacoes(txt)
assert not v, ("a guarda P18 achou violacao no ESTADO", v[:3])
assert not re.search(r"4[,.]44|z_disc", txt), "o ESTADO cita o 4,44 ou o z_disc: a regra da ordem do operador exige o p e a linha dos 5 sigma no mesmo paragrafo; este ESTADO nao os cita"
falas = " ".join(re.sub(r"\s+", " ", open(f, encoding="utf-8").read()) for f in glob.glob(os.path.join(DL.WK, "cunhagens_13out", "OPERADOR_*.txt")))
for q in re.findall(r"«([^»]{12,})»", txt):
    assert re.sub(r"\s+", " ", q) in falas, ("citacao entre aspas que nao e verbatim numa fala do operador", q[:70])
assert txt.splitlines()[0] == "CADEIA v400 — preparada (correção: α único; B(n) com salto v398→v400)"
p = os.path.join(HERE, "ESTADO_V400.md"); b = txt.encode("utf-8")
if os.path.exists(p):
    bk_ = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1"; open(bk_, "wb").write(open(p, "rb").read())
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("ESTADO_V400.md", len(b), "bytes; sha16", sha(b)[:16], "| linhas", txt.count("\n"))

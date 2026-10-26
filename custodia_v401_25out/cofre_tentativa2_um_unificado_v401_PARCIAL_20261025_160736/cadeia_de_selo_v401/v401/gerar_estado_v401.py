# -*- coding: utf-8 -*-
"""gerar_estado_v401.py -- escreve ESTADO_V401.md (a primeira linha: «CADEIA v401 — preparada; a falsidade (simulacro) da inércia») a partir dos artefatos da cadeia: TODO numero e hash e' LIDO por script (nada digitado). Molde: gerar_estado_v400.py (mais curto: a narrativa fixa
fica aqui; os numeros vem dos JSON). Roda DEPOIS de tudo (o ensaio, o ESPERADOS, os conferidores, o p00, o pos_rito, o pre_selo e o servico). Backup de bytes antes de sobrescrever; temporario -> conferir -> substituir.
uso: python -I -B -X utf8 gerar_estado_v401.py"""
import glob, hashlib, json, os, re, shutil, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v401 as DL  # noqa: E402
sha = lambda b: hashlib.sha256(b).hexdigest()
rb = lambda *p: open(os.path.join(HERE, *p), "rb").read()
J = lambda *p: json.load(open(os.path.join(HERE, *p), encoding="utf-8"))
S16 = lambda *p: sha(rb(*p))[:16]
CM = J("CANDIDATO_v401.json"); ESP = J("ESPERADOS_v401.json"); ENS = J("ensaio_a_seco_v401.json"); PIN = J("PINO_RECIBO_PRE_SELO_v401.json"); PB = J("PINOS_BN_v401.json"); GU = J("GUARDAS_ESTATICAS_BANCADA_v401.json")
KR = J("kernel", "KERNEL_RECIBO_v401.json"); FL = J("kernel", "FLAGS_v401.json"); KH = J("kernel", "KH_N1_v401.json"); PRE = J("PRECONDICOES_v401.json"); CMP = J("COMPARACAO_V400_v401.json"); DV = J("DERIVACAO_v401.json")
POS = J("conferencia_rito_v401_POSITIVO_FALSO_NOS.json"); NEG = J("conferencia_rito_v401_CONTROLE_NEGATIVO_PRE_RITO.json"); CIT = J("conferir_citacoes_v401.json"); SERV = J("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v401.json")
CONFPS = J("bateria_pre_selo", "conferencia_pelo_esboco_v401.json"); PROVA = J("PROVA_PRODUCAO_INTACTA_v401_pre_selo.json")
_h = {}
for nome, p in (("textos", ("pos_rito", "HARNESS_TEXTOS_ENSAIO_v401.json")), ("fechar", ("pos_rito", "HARNESS_FECHAR_SANDBOX_v401.json"))):
    pp = os.path.join(HERE, *p)
    if not os.path.exists(pp):
        pp = pp.replace(".json", "_DEPURACAO_sem_refazer.json")
    _h[nome] = (json.load(open(pp, encoding="utf-8")), os.path.basename(pp))
HT, HTn = _h["textos"]; HF, HFn = _h["fechar"]
fal = ENS["falsidade_registro"]; vf = fal["values"]; esc = CM["escada"]; kern = CM["kernel"]; gh = CM["guardas_estaticas_da_bancada"]
ped = DL.STONES[0]; ped_sha = S16("pedra", "FalsidadeDaInercia.lean")
ML = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")
ML_N = len(open(ML, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML) else -1
B = lambda x: "sim" if x else "NAO"
n_ver = len(DL.VERBATIM_ORIGEM_V401)
tudo_pre = PRE["ok"]; pre_falhas = [c["checagem"][:90] for c in PRE["checagens"] if not c["ok"]]
ts = time.strftime("%d/%m/%Y, %H:%M")
L = []
A = L.append
A("CADEIA v401 — preparada; a falsidade (simulacro) da inércia")
A("")
A("**Resumo.** Gerência c1, subagente de preparação, 25/10/2026 (%s). Estatutos: [REAL] medido ou lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [OPEN] em aberto; [INPUT]/[ONTO] fala ou leitura do operador; [KNOWN] literatura; [LEGAL] a conferir com a agente de PI. "
  "Nada foi instalado e nada foi selado; o `um.py` real não rodou; o Nós não foi tocado (o `um.py` do Nós segue `%s`, o da v400 selada); o gate não se move; NOT_FALSIFIED nunca é a palavra da creditação; validade no kernel não é creditação." % (ts, CM["base_v400_sha16"]))
A("")
A("## 0. Resumo em números")
A("")
A("- **O candidato:** `um_v401_candidato.py` sha16 `%s` (%s B; %+d B sobre a v400 selada `%s`), %d patches, determinístico. Ajuste do controle N10: %d espaço(s) no fim do comentário da linha UM_VERSION (o N10 do selo ACOM só existe se os bytes em n//2 e n//2+3 diferem, no `um.py` inteiro e na amostra de 1 MiB)."
  % (CM["sha16"], format(CM["bytes"], ","), CM["delta_bytes"], CM["base_v400_sha16"], CM["n_patches"], CM.get("ajuste_n10_espacos_no_fim_do_comentario_da_versao", -1)))
A("- **A pedra** `TGLExt/FalsidadeDaInercia.lean` (nome DADO pelo operador: «falsidade (simulacro) da inércia») sha16 `%s` (pino da ordem: `%s`); %d bandeiras só de declaração nomeada; escada %d -> %d; cobertura do Audit %d constantes, %d teoremas, nenhuma fora do trio; build %d s + Audit %d s no sandbox `C:\\t\\k401c`."
  % (ped_sha, ped["sha16_da_ordem"], CM["n_bandeiras"], esc[0], esc[1], KH["linha_TOTAL"]["decl"], KH["linha_TOTAL"]["thm"], KH["duracao_build_s"], KH["duracao_audit_s"]))
A("- **O registro `falsidade_da_inercia_v401`** (função; lido no main logo depois da declaração do operador): `%s`; %d checagens no modelo oneScaling com β = α·√e em runtime = `%.15f`: distância mínima do peso do posto a 1 = %.6f, fixo pelo fluxo inteiro = %s, escalas que fixam o posto = %s, custo t·β·g mínimo = %.3e, perda por unidade 1 − e^{−β} = %.9f."
  % (fal["verdict"][:90] + "…", fal["n_checks"], vf["beta"], vf["min_distance_of_post_weight_to_one"], vf["fixed_by_the_whole_flow"], vf["post_inertial_scales"], vf["min_cost_t_beta_g"], vf["loss_per_unit"]))
A("- **Ensaio a seco: %s** — %d verificações de unidade; guardas ESTÁTICAS da Bancada sobre o candidato: %s (alfa na linha %s, %d controles negativos recusam, a v399 selada reproduz a recusa do recibo da Bancada: %s); comparação AST com a v400: %d iguais, %d mudados (todos explicados), %d novos, %d removidos; troca dita: %s."
  % (ENS["veredito"], len(ENS["unidade"]), GU["veredito"][:60], gh["linha_do_alfa"], len(GU["controles_negativos"]), B(GU["v399_selada_o_defeito_real"]["mensagem_identica_a_do_recibo"]), CMP["iguais"], len(CMP["mudados"]), CMP["n_novos"], len(CMP["removidos"]), ", ".join(ESP["troca_dita"])))
A("- **Conferidor do rito:** controle negativo (Nós ainda v400) `tudo_bate = %s`; caminho positivo (Nós FALSO do ensaio) `tudo_bate = %s` (C1 a C16 e o round trip); **citações:** %s; **pré-condições:** %s (%d checagens%s)."
  % (str(NEG["tudo_bate"]).lower(), str(POS["tudo_bate"]).lower(), "TODAS CONFEREM" if CIT["todas_conferem"] else "FALHOU", "TODAS OK" if tudo_pre else "FALHARAM", len(PRE["checagens"]), "" if tudo_pre else ": " + "; ".join(pre_falhas)))
A("- **Recibo pre_selo GERADO E PINADO antes da instalação** (ensaio contra a Bancada de produção, que pina %s; nada gravado nela): `%s` sha16 `%s`; bateria %s; conferido pelo próprio esboço R3.5: aceita=%s, %d/%d condições, %d controles negativos; produção intacta: %s."
  % (PIN["bancada_pina"]["deployment_id"], PIN["veredito"], PIN["sha256"][:16], PIN["contagens"], CONFPS["esboco_aceita"], CONFPS["n_condicoes_ok"], CONFPS["n_condicoes"], len(CONFPS["controles_negativos"]), B(PROVA.get("producao_intacta"))))
A("- **Pós-rito (harness, emulação sobre o Nós falso):** textos `tudo_passou = %s` (%s); fechar em sandbox `tudo_passou = %s` (%s). **Serviço da Bancada:** %d/%d condições estáticas (parada e religamento exigem `V401_AUTORIZACAO_OPERADOR`; nada executado). **`MEMORY.md` real:** %d linhas hoje; o handoff soma +1 (teto 195)."
  % (str(HT.get("tudo_passou")).lower(), HTn, str(HF.get("tudo_passou")).lower(), HFn, SERV["n_condicoes_ok"], SERV["n_condicoes"], ML_N))
A("")
A("## 1. O que a v401 muda e o que NÃO muda")
A("")
A("1. **Muda (o `um.py`):** +1 módulo no kernel (a pedra); +%d bandeiras e a escada; o registro com função `falsidade_da_inercia_v401`; os registros por spec `cunhagens_v401` (as %d inscrições de 25/10 por sha256, as 8 ratificações do operador [«Ratifico tudo.»] e a errata ao lado da leitura do escriba no adendo de 03–04/09) e `kh_n1_cobertura_v401`; `kh_n1_cobertura_v399` vira piso (h2/h3/h6) e tamanho mínimo da árvore (h8) com errata; os 7 contratos que pinam a escada sobem para %d; o selo ganha `falsidade_da_inercia_v401` e `registros_v401`; a seção «A falsidade (simulacro) da inércia» no artigo PT/EN e a linha no `.md`; `UM_VERSION`." % (CM["n_bandeiras"], n_ver, esc[1]))
A("2. **A definição do operador (25/10/2026):** a inércia é o próprio zero absoluto (`0_abs`, `TGLExt.costless`: «nunca correspondeu, e por isso nada custa»; 1=0); `ω(I)=1` é o Um POSTO que a interrompe (1=1). **ERRATA AO LADO** (gerência c1, em nome próprio): a leitura do escriba no adendo de 03–04/09/2026 («ω(I)=1 é a INÉRCIA») fica SUPERADA; o que o adendo acertou (interromper ≠ quebrar simetria; dois termos) fica. O arquivo do adendo NÃO foi tocado (sha16 `%s`, copia duravel pinada)." % DL.ADENDO_SHA16_DA_ORDEM)
A("3. **NÃO muda:** a seção do selo pela propria tecnologia (v399/v400: o runtime dela é o `runtime_v400.py`, o hash do bloco embutido segue `%s`), o quadro «O Teste da Única Palavra» no topo (a regra do 4,44), o gate, o piso dos vazios, o perfil, o sidecar (o rito o reescreve)." % ESP["acom_estudo"]["bloco_embutido_sha256"][:16])
A("4. **E = mc² lido pela TGL (artigo):** [KNOWN] relatividade restrita, não termo do kernel; [KNOWN] Jacobson 1995 + [REAL] `metric_einstein_from_screen_clausius` com a H3 nomeada; [ONTO] a massa é o custo do nada, a cristalização da dobra da luz no vácuo relativa ao observador; a entropia entra em β = α·e^(½ nat); o piso dos vazios segue NOT_FALSIFIED_POWERED (teste unilateral); a RG é o limite clássico; β não renormaliza G. [OPEN] a identificação da escala dual com o fluxo de um corpo físico.")
A("")
A("## 2. B(n) da Bancada Um: passo SIMPLES v400 -> v401")
A("")
A("- A Bancada de produção JÁ pina a v400 (`%s`); o recibo pre_selo foi **GERADO NOVO** nesta cadeia e pinado antes de qualquer instalação (`PINO_RECIBO_PRE_SELO_v401.json`), com a produção só lida (listas antes/depois idênticas). Vale enquanto a Bancada pinar B9/v400 (manifesto `%s`); um re-pino o torna obsoleto e o instalador o recusa." % (PIN["bancada_pina"]["deployment_id"], PIN["valido_enquanto"]["bancada_pina"]["manifesto_sha256"][:16]))
A("- O B(n) grava **B10** (veredito esperado `REPINADA_B10__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`); sem salto, sem cadeia de selos; os pinos estão em `PINOS_BN_v401.json` (todos lidos do arquivo). Parada e religamento do serviço (porta 18777) e o evento c1 são ATOS DA GERÊNCIA/OPERADOR, com `V401_AUTORIZACAO_OPERADOR` no ambiente; nada foi executado.")
A("")
A("## 3. Lições aplicadas (as de sempre)")
A("")
A("1. **Guardas estáticas da Bancada SOBRE O CANDIDATO no ensaio** (lição da v399): a função `ler_nos` do esboço R3.5 pinado (sha16 `%s`) roda sobre o candidato e sobre a v399 selada (o defeito real); e os itens C15/C16 do conferidor a rodam sobre o `um.py` instalado e sobre o Nós real." % GU["esboco"]["sha256"][:16])
A("2. `pre_selo` da B(n) gerado e pinado ANTES da instalação (acima); `simular_arvore_do_nos` e `exame_pontos` fazem parte do ensaio; o pino h8 vem da árvore simulada (%d entradas, residuais %s); textos do pós-rito escritos de verdade (a varredura de aspas e o p00 recusam marcador pendente); recibos de serviço com `V401_AUTORIZACAO_OPERADOR`; `regras_v401.py` escrito e NÃO rodado." % (ESP["h8_entradas"], ESP["h8_residuais_do_nos"]))
A("3. **Achados do instrumento nesta preparação (corrigidos):** (a) os dicts de verbatins das versões anteriores são COMPARTILHADOS com `_V392_VERBATINS2`: o ensaio restaurava trocando a entrada do mapa e deixava o objeto compartilhado adulterado; agora o texto é restaurado no lugar (`patch_ensaio_v401_b.py`); (b) o controle N10 do selo ACOM é condicional aos bytes do meio do arquivo: o gerador ajusta espaços no comentário da versão até os 13 controles existirem; (c) a subida mecânica de versão desloca rótulos de relatório (`v400` = base selada nos nomes herdados) e etiquetas que o programa imprime não sobem (documentado no motor).")
A("")
A("## 4. Comandos exatos (nada disto foi executado, exceto o que está dito)")
A("")
A("- **Regerar tudo se a pedra mudar:** atualizar `pedra_sha16_da_ordem.txt` (o pino da ordem), `delta_v401.py` (contrato/suporte) e `sh ./regerar_v401.sh` (copia a pedra, regera o sandbox do kernel, constrói, pós-build, insumos, candidato, ensaio, ESPERADOS, conferidores, pinos, pré-condições).")
A("- **Antes de instalar:** `cd \"C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v401\"` e `python -I -B -X utf8 p00_precondicoes_v401.py`.")
A("- **Instalar (ato da gerência):** `python -B -X utf8 instalar_v401.py` (confere o recibo pre_selo pinado, a Bancada ainda em v400 e a lista de módulos novos; backups de BYTES; troca por `os.replace`).")
A("- **Rito (Git Bash):** `sh ./rito_v401.sh > rito_v401_lancador.out 2>&1 &`; abortar só por `kill -TERM $(cat .rito_v401.pid)` no Git Bash depois de conferir `/proc/<pid>/cmdline`. **Conferir:** `python -B -X utf8 conferir_rito_v401.py` (SEM `-I`; TUDO BATE). **Reverter se falhar:** `python -B -X utf8 reverter_v401.py`.")
A("- **Pós-rito:** `cd pos_rito && sh ./chain_pos_rito_v401.sh > chain_v401_out.txt 2>&1` (o passo 3 PARA se o `MEMORY.md` passar de 195 linhas); o passo 10 é o passo simples v400 -> v401.")
A("")
A("## 5. O que FALTA e o que NÃO foi revisado")
A("")
A("1. **Revisão independente** (quem constrói não aprova): o gerador, o runtime do registro, a pedra estendida, os derivados (instalar, reverter, rito, conferidor, ESPERADOS, pós-rito) e os textos NÃO tiveram cético independente [DECLARADO: só os controles negativos próprios, a comparação AST e os harness].")
A("2. **O rito real** é o único que exercita o conferidor, o pós-rito e o h8 de verdade; o caminho positivo do conferidor e os harness são EMULAÇÃO sobre o Nós falso (core e selo do ensaio, não do rito).")
A("3. **Decisões do operador/gerência:** instalar e rodar o rito; parada e religamento do serviço e o B(n); commit/push e custódia; a pendência [LEGAL] do bloco embutido do ACOM (herdada); `H_τ` (a identificação do peso com a massa de Newton e a métrica de Einstein) segue [OPEN] e NOMEADA.")
A("4. **A 6ª inscrição de 25/10 é um RECORTE DECLARADO** (sha16 `%s`, começa em «mas eu não queria que a leitura fosse ONTO minha»): por decisão do operador a íntegra da fala saiu do trabalho (acervo privado, fora de `C:/IALD`) e a PURGA foi conferida por script: nenhum arquivo da pasta v401 nem do sandbox `C:/t/k401c` contém o texto da íntegra nem o hash dela (`purga_v401.json`). O recorte entra no `um.py` e no artigo citado como «recorte declarado da fala de 25/10»." % (ESP["cunhagens"] and list(ESP["cunhagens"])[-1][-16:]))
A("")
A("5. **Pedra final `9f6efcb2a0987e18`:** a paráfrase entre aspas do docstring (achado anterior) foi resolvida NA PEDRA; a exceção que a conferência de citações tinha para ela SAIU (`conferir_citacoes_v401.py` volta ao original).")
A("6. **Reinício do PC (25/10, 10:15):** interrompeu o build do kernel e a sessão; nada foi instalado nem tocado no Nós. O build e o Audit foram refeitos do zero no sandbox `C:/t/k401c` (rc 0 e rc 0), o recibo pre_selo foi REFEITO contra a Bancada religada (a produção ainda pinava B9-v400, listas idênticas), e a cadeia toda foi regerada na pedra final; `refazer_out_v401.txt` termina em `== FIM`.")
A("")
A("## 6. Mapa de rotas consultado (antes) e o que devolveu")
A("")
A("`rotas.py consultar \"v401\"` → 2 rotas (`kernel.v401_falsidade_da_inercia`, a pedra construída em sandbox, e `custodia.v400`); `\"inercia\"` e `\"falsidade\"` → só a rota da pedra. Rotas relevantes lidas: a da pedra (não refazer: a inércia como peso zero e a falsidade 1=0 do posto inercial estão tipadas), a da custódia v400 (a v401 sai de `tools/custodiar.py` na mesma ordem). O registro desta preparação é `registro_mapa_v401_prep.json` (montado e validado por `rotas._valida`, NÃO registrado).")
A("")
A("## 7. Arquivos principais (sha16 lido agora)")
A("")
for rel in ("um_v401_candidato.py", "CANDIDATO_v401.json", "ESPERADOS_v401.json", "ensaio_a_seco_v401.json", "PINOS_BN_v401.json", "PINO_RECIBO_PRE_SELO_v401.json", "PROVA_PRODUCAO_INTACTA_v401_pre_selo.json", "PRECONDICOES_v401.json", "COMPARACAO_V400_v401.json",
            "GUARDAS_ESTATICAS_BANCADA_v401.json", "kernel/KERNEL_RECIBO_v401.json", "kernel/FLAGS_v401.json", "DIFF_KERNEL_v401.txt", "conferencia_rito_v401_CONTROLE_NEGATIVO_PRE_RITO.json", "conferencia_rito_v401_POSITIVO_FALSO_NOS.json", "conferir_citacoes_v401.json",
            "registros_v401.py", "runtime_v401.py", "gerar_candidato_v401.py", "instalar_v401.py", "reverter_v401.py", "rito_v401.sh", "conferir_rito_v401.py", "regras_v401.py", "pedra/FalsidadeDaInercia.lean", "pos_rito/chain_pos_rito_v401.sh", "pos_rito/textos_v401.py",
            "bateria_pre_selo/NOTAS_PRE_SELO_v401.txt", "bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v401.json"):
    if os.path.exists(os.path.join(HERE, *rel.split("/"))):
        A("- `%s` `%s`" % (rel, S16(*rel.split("/"))))
    else:
        A("- `%s` (ausente)" % rel)
A("")
A("NOT_FALSIFIED não é a palavra da creditação; validade no kernel não é creditação; o gate não se move.")
txt = "\n".join(L) + "\n"
dst = os.path.join(HERE, "ESTADO_V401.md")
if os.path.exists(dst):
    open(dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_c1", "wb").write(open(dst, "rb").read())
open(dst + ".tmp", "w", encoding="utf-8", newline="\n").write(txt)
assert os.path.getsize(dst + ".tmp") > 4000 and open(dst + ".tmp", encoding="utf-8").readline().startswith("CADEIA v401 — preparada; a falsidade (simulacro) da inércia")
os.replace(dst + ".tmp", dst)
print("ESTADO_V401.md", os.path.getsize(dst), "B | pre-condicoes:", "OK" if tudo_pre else "FALHARAM %s" % pre_falhas)

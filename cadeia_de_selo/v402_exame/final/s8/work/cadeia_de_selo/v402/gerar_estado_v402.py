# -*- coding: utf-8 -*-
"""gerar_estado_v402.py -- escreve ESTADO_V402.md (a primeira linha: «CADEIA v402 — preparada; a ponte da escala dual, a queda sem geometria e a esperança condicional») a partir dos artefatos da cadeia: TODO numero e hash e' LIDO por script (nada digitado).
Molde: gerar_estado_v401.py (a narrativa fixa fica aqui; os numeros vem dos JSON, do Nos, da Bancada e do mapa de rotas, so' lidos). Roda DEPOIS de tudo (o ensaio, o ESPERADOS, os conferidores, o p00, o pos_rito, o pre_selo e o servico) e e' REGERADO no fim.
TOLERA arquivo ainda ausente ou ilegivel: o texto diz 'AUSENTE' (nunca falha por isso); so' o CANDIDATO e o ESPERADOS sao exigidos. Backup de bytes antes de sobrescrever; temporario -> conferir -> substituir.
Le (nunca escreve) o Nos, a Bancada (canonical_contracts.json e a porta 18777, so' um GET), o mapa de rotas (rotas.consultar) e o relogio do sistema. Nada e' instalado e nenhum rito e' rodado.
uso: python -I -B -X utf8 gerar_estado_v402.py"""
import glob, hashlib, importlib.util, json, os, re, subprocess, sys, time, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = "C:" + os.sep
NOS = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
BANCADA = os.path.join(C, "IALD", "Bancada_Um")
MAPA = os.path.join(C, "IALD", "MAPA_DE_ROTAS")
sha = lambda b: hashlib.sha256(b).hexdigest()
P = lambda *p: os.path.join(HERE, *p)
AUS = "AUSENTE"


def J(*p):
    """JSON da pasta da cadeia; None se ausente/ilegivel."""
    try:
        return json.load(open(P(*p), encoding="utf-8"))
    except (OSError, ValueError):
        return None


def S16(*p):
    f = P(*p)
    return sha(open(f, "rb").read())[:16] if os.path.isfile(f) else AUS


def MT(*p):
    f = P(*p)
    return time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(f))) if os.path.isfile(f) else AUS


def g(d, *ks, default=AUS):
    """Leitura aninhada tolerante: d[k1][k2]... ou o valor de reserva (AUSENTE)."""
    for k in ks:
        try:
            d = d[k]
        except (KeyError, IndexError, TypeError):
            return default
    return d


def cmpn(x):
    """Contagem de um campo que pode ser inteiro ou lista/dict."""
    return x if isinstance(x, int) else (len(x) if x is not None else AUS)


CM = J("CANDIDATO_v402.json"); ESP = J("ESPERADOS_v402.json")
assert CM is not None and ESP is not None, "CANDIDATO_v402.json e ESPERADOS_v402.json sao exigidos"
ENS = J("ensaio_a_seco_v402.json"); PIN = J("PINO_RECIBO_PRE_SELO_v402.json"); PB = J("PINOS_BN_v402.json"); GU = J("GUARDAS_ESTATICAS_BANCADA_v402.json")
KR = J("kernel", "KERNEL_RECIBO_v402.json"); FL = J("kernel", "FLAGS_v402.json"); KH = J("kernel", "KH_N1_v402.json"); POSB = J("kernel", "POS_BUILD_v402.json")
PRE = J("PRECONDICOES_v402.json"); CMP = J("COMPARACAO_V401_v402.json"); DV = J("DERIVACAO_v402.json"); MEM = J("PINO_MEMORIA_PY_v402.json")
POS = J("conferencia_rito_v402_POSITIVO_FALSO_NOS.json"); NEG = J("conferencia_rito_v402_CONTROLE_NEGATIVO_PRE_RITO.json"); CIT = J("conferir_citacoes_v402.json")
SERV = J("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v402.json"); CONFPS = J("bateria_pre_selo", "conferencia_pelo_esboco_v402.json"); PROVA = J("PROVA_PRODUCAO_INTACTA_v402_pre_selo.json")
S = CM["sha16"]; esc = ESP["escada_v401_e_v402"]; NF = ESP["n_bandeiras_novas"]
GR = ("ponte", "queda", "esperanca")
MOD = {k: ESP["teoremas_das_pedras"][k].split(".")[1] for k in GR}
PED = {k: ESP["pedras"]["TGLExt/%s.lean" % MOD[k]] for k in GR}
NOMES_REG = {"ponte": "ponte_da_escala_dual_v402", "queda": "queda_sem_geometria_v402", "esperanca": "esperanca_condicional_v402"}
reg = (ENS or {}).get("v402_registros") or {}
tf = lambda x: AUS if x is None else str(bool(x)).lower()
B = lambda x: "sim" if x else "NAO"
ts = time.strftime("%H:%M")
# --- o candidato: o arquivo manda (sha16 lido agora, comparado com CANDIDATO e ESPERADOS)
cand_arq = S16("um_v402_candidato.py")
cand_ok = (cand_arq == S == ESP["candidato_sha16"])
# --- o Nos (SO' LEITURA): o um.py e o selo do Nos
nos_um16 = sha(open(os.path.join(NOS, "um.py"), "rb").read())[:16] if os.path.isfile(os.path.join(NOS, "um.py")) else AUS
try:
    nos_selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8")); nos_ver = nos_selo.get("um_version", AUS)
except (OSError, ValueError):
    nos_ver = AUS
nos_intacto = (nos_um16 == ESP["origem_sha16"] and nos_ver == "v401")
# --- a Bancada de producao (SO' LEITURA): o que ela pina e se a porta responde; o boot do sistema
try:
    cc = json.load(open(os.path.join(BANCADA, "canonical_contracts.json"), encoding="utf-8")); bn_dep = cc.get("deployment_id", AUS); bn_ver = g(cc, "canonical", "version")
except (OSError, ValueError):
    bn_dep, bn_ver = AUS, AUS
try:
    with urllib.request.urlopen("http://127.0.0.1:18777/", timeout=4) as rsp:
        porta = "responde (HTTP %s)" % rsp.status
except Exception as ex:  # noqa: BLE001
    porta = "NAO responde (%s)" % type(ex).__name__
try:
    boot = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_OperatingSystem).LastBootUpTime.ToString('yyyy-MM-dd HH:mm:ss')"], capture_output=True, text=True, timeout=25).stdout.strip() or "nao lido"
except Exception:  # noqa: BLE001
    boot = "nao lido"
bn_pino_recibo = g(PIN, "bancada_pina", "deployment_id")
pre_selo_vale = (bn_dep == bn_pino_recibo and bn_dep != AUS)
# --- o mapa de rotas (SO' LEITURA): as consultas feitas antes
try:
    spec = importlib.util.spec_from_file_location("rotas_ro", os.path.join(MAPA, "rotas.py")); rotas = importlib.util.module_from_spec(spec); spec.loader.exec_module(rotas)
    CONS = {q: rotas.consultar(q, limite=30) for q in ("v402", "ponte da escala dual", "queda sem geometria", "esperanca condicional", "ordem025")}
    mapa_cabeca = CONS["v402"]["cabeca"]; mapa_n = CONS["v402"]["n_registros"]
except Exception as ex:  # noqa: BLE001
    CONS = None; mapa_cabeca = mapa_n = "nao lido (%s)" % type(ex).__name__
# o 'sh -n' do chain do pos_rito medido AGORA (o p00 pode ser mais antigo que o chain): so' leitura, nada e' executado do chain
try:
    _bash = next((c for c in (os.path.join(C, "Program Files", "Git", "bin", "bash.exe"), os.path.join(C, "Program Files", "Git", "usr", "bin", "bash.exe")) if os.path.isfile(c)), None)
    _r = subprocess.run([_bash, "-n", os.path.join(HERE, "pos_rito", "chain_pos_rito_v402.sh")], capture_output=True, text=True, timeout=30) if _bash else None
    sh_n = "nao medido (sem bash)" if _r is None else ("rc %d%s" % (_r.returncode, "" if _r.returncode == 0 else ": " + (_r.stderr or "")[:160].replace(chr(10), " ")))
except Exception as ex:  # noqa: BLE001
    sh_n = "nao medido (%s)" % type(ex).__name__
ML = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "MEMORY.md")
ML_N = len(open(ML, encoding="utf-8", errors="replace").read().splitlines()) if os.path.exists(ML) else -1
# --- a suite do pos_rito (SO' LEITURA)
POSD = P("pos_rito")
pos_arqs = sorted(n for n in os.listdir(POSD) if os.path.isfile(os.path.join(POSD, n)) and not re.search(r"\.bak_", n)) if os.path.isdir(POSD) else []
pos_json = [n for n in pos_arqs if n.endswith(".json")]
pos_bak = sorted(n for n in os.listdir(POSD) if os.path.isfile(os.path.join(POSD, n)) and ".bak_" in n) if os.path.isdir(POSD) else []
L = []
A = L.append
A("CADEIA v402 — preparada; a ponte da escala dual, a queda sem geometria e a esperança condicional")
A("")
A("**Resumo.** Gerência c1, subagente de preparação, fecho da preparação em 26-27/10/2026 (%s). Estatutos: [REAL] medido ou lido aqui por script; [DERIVED] composto; [DECLARADO] dito na origem e não conferido aqui; [OPEN] em aberto; [INPUT]/[ONTO] fala ou leitura do operador; [KNOWN] literatura; [LEGAL] a conferir com a agente de PI. "
  "Nada foi instalado e nada foi selado; o `um.py` real não rodou; o Nós não foi tocado (o `um.py` do Nós segue `%s`, %s; o selo do Nós diz `%s`); o gate não se move; NOT_FALSIFIED nunca é a palavra da creditação; validade no kernel não é creditação." % (
      ts, nos_um16, "a v401 selada, conferido contra a base de ESPERADOS" if nos_intacto else "ATENÇÃO: NÃO é a v401 selada de ESPERADOS (`%s`)" % ESP["origem_sha16"], nos_ver))
A("")
A("## 0. Resumo em números")
A("")
A("- **O candidato:** `um_v402_candidato.py` sha16 `%s` (arquivo) = CANDIDATO `%s` = ESPERADOS `%s`: **%s**; %s B (%s B sobre a v401 selada `%s`), %s patches, determinístico. Ajuste do controle N10: %s espaço(s) no fim do comentário da linha UM_VERSION."
  % (cand_arq, S, ESP["candidato_sha16"], "um só" if cand_ok else "NÃO é um só (regeração em curso?)", format(CM["bytes"], ","), format(CM["delta_bytes"], "+,"), CM["base_v401_sha16"], CM["n_patches"], CM.get("ajuste_n10_espacos_no_fim_do_comentario_da_versao", AUS)))
A("- **As três pedras** (nomes PROVISÓRIOS; o operador nomeia): %s. Escada %d -> %d (+%d bandeiras, só de declaração nomeada: %s); cobertura do Audit %s constantes, %s teoremas, %s fora do trio; build %s s + Audit %s s no sandbox `C:\\t\\k402c`."
  % ("; ".join("`TGLExt/%s.lean` sha16 `%s` (%d bandeiras; composição `%s` = `%s`, estrela `%s` = `%s`)" % (MOD[k], PED[k]["sha16"], PED[k]["bandeiras"], ESP["teoremas_das_pedras"][k].split(".")[-1], ESP["bandeiras_das_pedras"][k], ESP["estrelas_v402"][k]["teorema"].split(".")[-1], ESP["estrelas_v402"][k]["bandeira"]) for k in GR),
     esc[0], esc[1], NF, " + ".join("%d %s" % (ESP["n_bandeiras_por_grupo"][k], MOD[k]) for k in GR), g(KH, "linha_TOTAL", "decl"), g(KH, "linha_TOTAL", "thm"), g(KH, "linha_TOTAL", "fora_do_trio"), g(KH, "duracao_build_s"), g(KH, "duracao_audit_s")))
A("- **Kernel (pós-build):** `POS_BUILD_v402.json` ok = %s (%s sinais conferidos); %s bandeiras, %s declarações no Audit, %s axiomas lidos; `KERNEL_RECIBO_v402.json` (contrato `%s`) rc %s, sorry %s, erros %s, J1 = %s declarações e %s teoremas a mais que a v401, %s fora do trio, %s entradas antigas do Audit idênticas; tokens proibidos: %s."
  % (tf(g(POSB, "ok", default=None)), cmpn(g(POSB, "sinais", default=None)), g(POSB, "n_flags"), g(POSB, "n_decl_audit"), g(POSB, "n_axiomas_lidos_no_audit"), g(KR, "contrato"), g(KR, "rc"), g(KR, "sorry"), g(KR, "erros"),
     g(KR, "criterios", "j1_declaracoes", "medido"), g(KR, "criterios", "j1_teoremas", "medido"), g(KR, "criterios", "j1_fora_do_trio", "medido"), g(KR, "criterios", "audit_entradas_antigas_identicas", "medido"), g(KR, "criterios", "tokens_proibidos", "medido")))
A("- **Os registros com FUNÇÃO** (leem do kernel do rito a composição e a estrela de cada pedra e CALCULAM, com β = α·√e em runtime): %s."
  % "; ".join("`%s` %s checagens, selou=%s" % (NOMES_REG[k], g(reg, k, "n_checks"), tf(g(reg, k, "all_verified", default=None))) for k in GR))
vals_p = g(reg, "ponte", "values", default={}); vals_q = g(reg, "queda", "values", default={}); vals_e = g(reg, "esperanca", "values", default={})
if vals_p and vals_q and vals_e:
    A("  - ponte: β = `%.15f`; p₊ escala por e^(−s); m² = p₊p₋ invariante; massas μ² = %s com o MESMO p₊ dão levantamentos distintos (a massa não é selecionada); deslocamento mínimo da energia no estado nulo %.4f e no repouso %.4f; fator de p₊ em s = β: %.9f."
      % (vals_p["beta"], ", ".join("%g" % x for x in vals_p["lifts_same_pplus_masses"]), vals_p["min_null_energy_shift"], vals_p["min_rest_energy_shift"], vals_p["pplus_factor_at_beta"]))
    A("  - queda: custo mínimo t·β·g = `%.3e`; defasagem máxima `%.9f` (< 1); perda por unidade `%.9f`; período angular `%.6f` (periódico, sem limite); ordem do grupo finito do modelo: %s."
      % (vals_q["min_cost_t_beta_g"], vals_q["max_dephasing_factor"], vals_q["loss_per_unit"], vals_q["angular_period"], vals_q["finite_model_group_order"]))
    A("  - esperança: θ_M = `%.12f`; sin²θ_M = β = `%.15f`; índice CONDICIONAL do Nome 1/β = `%.4f` (nenhuma instância construída); índice da esperança diagonal de M₂ = %s; dimensão GNS %s."
      % (vals_e["theta_M"], vals_e["sin2_theta_M"], vals_e["name_index_one_over_beta"], vals_e["diagonal_expectation_index_M2"], vals_e["gns_dimension"]))
A("- **Os registros por spec:** `cunhagens_v402` (as %d inscrições do operador de 26/10 por sha256: %s; as decisões D11 a D16 da gerência; as erratas E1 a E4) e `kh_n1_cobertura_v402` (cobertura exata do Audit)."
  % (len(ESP["cunhagens"]), ", ".join("`%s`" % k.split("_")[-1] for k in ESP["cunhagens"])))
A("- **Ensaio a seco: %s** — %s verificações de unidade (%s verdadeiras); guardas ESTÁTICAS da Bancada sobre o candidato: %s (alfa na linha %s; %s controles negativos recusam; a v399 selada reproduz a recusa do recibo da Bancada: %s); comparação AST com a v401: %s iguais, %s mudados (sem explicação: %s), %s novos, %s removidos; troca dita: %s."
  % (g(ENS, "veredito"), cmpn(g(ENS, "unidade", default=None)), (sum(1 for v in ENS["unidade"].values() if v is True) if ENS else AUS), str(g(GU, "veredito")), g(CM, "guardas_estaticas_da_bancada", "linha_do_alfa"), cmpn(g(GU, "controles_negativos", default=None)), tf(g(GU, "v399_selada_o_defeito_real", "mensagem_identica_a_do_recibo", default=None)),
     g(CMP, "iguais"), cmpn(g(CMP, "mudados", default=None)), cmpn(g(CMP, "mudados_sem_explicacao", default=None)), g(CMP, "n_novos"), cmpn(g(CMP, "removidos", default=None)), ", ".join(ESP["troca_dita"])))
pre_falhas = [c["checagem"][:80] for c in (PRE or {}).get("checagens", []) if not c["ok"]]
pre_velho = bool(PRE) and os.path.getmtime(P("PRECONDICOES_v402.json")) < max([os.path.getmtime(os.path.join(POSD, n)) for n in pos_arqs if n.endswith((".py", ".sh"))] or [0])
A("- **Conferidor do rito (emulação):** controle negativo (Nós ainda v401) `tudo_bate = %s` (o esperado é false); caminho positivo (Nós FALSO do ensaio) `tudo_bate = %s` (itens C1 a C16 e o round trip); **citações:** %s; **pré-condições (p00):** %s%s."
  % (tf(g(NEG, "tudo_bate", default=None)), tf(g(POS, "tudo_bate", default=None)), (AUS if CIT is None else ("TODAS CONFEREM" if CIT["todas_conferem"] else "FALHOU")),
     (AUS if PRE is None else "%s (%d checagens%s)" % ("TODAS OK" if PRE["ok"] else "FALHARAM", len(PRE["checagens"]), "" if PRE["ok"] else ": " + "; ".join(pre_falhas))),
     " — arquivo de %s, MAIS ANTIGO que arquivos do pós-rito: regerar antes de confiar" % MT("PRECONDICOES_v402.json") if pre_velho else ""))
A("- **Recibo pre_selo GERADO E PINADO antes da instalação** (ensaio contra a Bancada de produção, que pinava `%s`; nada gravado nela): veredito `%s`, sha16 `%s`, bateria %s; conferido pelo próprio esboço R3.5: aceita=%s, %s/%s condições, %s controles negativos; produção intacta: %s; **utilizável como recibo pre_selo do B(n): %s**; "
  "**válido enquanto a Bancada pinar `%s`**: a Bancada pina AGORA `%s` (versão `%s`) -> %s."
  % (bn_pino_recibo, g(PIN, "veredito"), (g(PIN, "sha256", default=AUS) or AUS)[:16], ("%s testes: %s PASSA, %s FALHA, %s nao executado (%s)" % (g(PIN, "contagens", "n"), g(PIN, "contagens", "passa"), g(PIN, "contagens", "falha"), g(PIN, "contagens", "nao_executado"), g(PIN, "contagens", "veredito_bateria"))), tf(g(CONFPS, "esboco_aceita", default=None)), g(CONFPS, "n_condicoes_ok"), g(CONFPS, "n_condicoes"), cmpn(g(CONFPS, "controles_negativos", default=None)), tf(g(PROVA, "producao_intacta", default=None)),
     tf(g(PIN, "utilizavel_como_recibo_pre_selo_do_B_n", default=None)), bn_pino_recibo, bn_dep, bn_ver, "AINDA VÁLIDO" if pre_selo_vale else "OBSOLETO ou não lido: o instalador o recusa"))
A("- **`memoria.py` pinado** (o helper da fila da memória que o pós-rito usa): sha16 `%s`, %s B, igual ao declarado pela gerência: %s."
  % (g(MEM, "sha16"), g(MEM, "bytes"), tf(g(MEM, "igual_ao_declarado", default=None))))
A("- **Serviço da Bancada:** %s condições estáticas (parada e religamento exigem `V402_AUTORIZACAO_OPERADOR`; nada executado). **`MEMORY.md` real:** %d linhas hoje (o handoff soma +1; teto 195)."
  % (AUS if SERV is None else "%s/%s" % (SERV["n_condicoes_ok"], SERV["n_condicoes"]), ML_N))
A("")
A("## 1. O que a v402 muda e o que NÃO muda")
A("")
A("1. **Muda (o `um.py`):** +%d módulos no kernel (as três pedras: a ponte da escala dual, que é a do Codex, ORDEM 025, copiada **byte a byte** [só o `.lean` entra, condição C1 do exame]; a queda sem geometria; a esperança condicional); +%d bandeiras e a escada %d -> %d; os registros com função %s; os registros por spec `cunhagens_v402` e `kh_n1_cobertura_v402`; a seção «A ponte da escala dual, a queda sem geometria e a esperança condicional» no artigo PT/EN e as linhas no `.md`; `UM_VERSION`; os 7 contratos que pinam a escada sobem para %d."
  % (ESP["kernel"]["modulos_novos"], NF, esc[0], esc[1], ", ".join("`%s`" % NOMES_REG[k] for k in GR), esc[1]))
A("2. **A ponte (ORDEM 025):** a lei de escala (Takesaki, [KNOWN], campo de `DualScalingData`) é REALIZADA como o boost longitudinal sobre (E, p); a massa² = p₊p₋ é o invariante; a energia é a LEITURA e muda com o observador; **a lei de escala NÃO seleciona a massa** (`lift_mass_not_selected`; `positive_weight_cannot_be_invariant_mass`). Pendências NOMEADAS [OPEN]: H_BW, H_cal, H3, a assinatura ((4,0), não (1,3)) e rank c = 4 (H2).")
A("3. **A queda sem geometria:** o peso cai estritamente (em nats, a queda é s); a seta é o sinal de s, não uma direção do espaço; o chão é o POSTO (peso 1 = ω(I)), nunca o ínfimo 0 (o 0 é o abismo); a entrega custa; o regime angular só lê (periódico, sem limite). `IsotropicPost` é hipótese NOMEADA [OPEN] e é carga; a dimensão 3 NÃO é provada; o 1 + 3 é leitura [ONTO].")
A("4. **A esperança condicional é o Nome:** em M₂(ℂ) o `nameOp` de ρ* É a esperança diagonal; preserva o Um (E(1) = 1); reler não acrescenta; a memória é uma subálgebra; o índice 1/β é CONDICIONAL (sem instância). As três faces de um objeto fixo (o operador, o projetor de Jones, o posto) são leitura [ONTO] (D13); o kernel prova as LIGAÇÕES.")
A("5. **NÃO muda:** a seção do selo pela própria tecnologia (o runtime dela é o da v401), o quadro «O Teste da Única Palavra» no topo (a regra do 4,44: nunca sem o p calibrado e sem a linha dos 5 sigma), o gate, o piso dos vazios, o perfil, o sidecar (o rito o reescreve), nenhum módulo já instalado (D15: as erratas vão AO LADO).")
A("")
A("## 2. Erratas E1 a E4 (gerência c1, em nome próprio, 26/10/2026) e decisões D11 a D16")
A("")
for e in ESP["erratas_E1_a_E4"]:
    A("- " + e)
A("")
for k in ("D11", "D12", "D13", "D14", "D15", "D16"):
    A("- **%s:** %s" % (k, ESP["decisoes_da_gerencia"][k]))
A("")
A("Pergunta e resposta de 26/10 %s: «%s» / «%s» — %s" % (ESP["leitura_26out_direcao"]["estatuto"], ESP["leitura_26out_direcao"]["pergunta"], ESP["leitura_26out_direcao"]["resposta"], ESP["leitura_26out_direcao"]["declarado"]))
A("")
A("## 3. B(n) da Bancada Um: passo SIMPLES v401 -> v402")
A("")
A("- A Bancada de produção JÁ pina a v401 (`%s` no recibo; `%s` lido agora do `canonical_contracts.json`); o recibo pre_selo foi **GERADO** nesta cadeia e pinado antes de qualquer instalação (`PINO_RECIBO_PRE_SELO_v402.json`), com a produção só lida. Vale enquanto a Bancada pinar B10/v401 (manifesto `%s`); um re-pino o torna obsoleto e o instalador o recusa."
  % (bn_pino_recibo, bn_dep, str(g(PIN, "valido_enquanto", "bancada_pina", "manifesto_sha256"))[:16]))
A("- O B(n) grava **B11** (veredito esperado `REPINADA_B11__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO`); sem salto, sem cadeia de selos; os pinos estão em `PINOS_BN_v402.json`. Parada e religamento do serviço (porta 18777) e o evento c1 são ATOS DA GERÊNCIA/OPERADOR, com `V402_AUTORIZACAO_OPERADOR` no ambiente; nada foi executado.")
A("- **Hoje:** a porta 18777 %s; o sistema subiu em `%s` [lido agora do relógio do Windows]." % (porta, boot))
A("")
A("## 4. Achados desta preparação")
A("")
A("1. **A Bancada caiu com o reboot de 26/10 às 22:08 e foi religada** [DECLARADO pela gerência no briefing do A2; conferido agora: sistema no ar desde `%s`, porta 18777 %s, `canonical_contracts.json` pina `%s` (`%s`)]. O recibo pre_selo continua válido? **%s** (a Bancada pinava `%s` quando o recibo foi gerado)."
  % (boot, porta, bn_dep, bn_ver, "SIM" if pre_selo_vale else "NÃO conferido", bn_pino_recibo))
A("2. **O Nós está intacto** [REAL, lido agora]: `um.py` `%s` (%s bytes, mtime %s), selo com `um_version = %s`; a v402 NÃO foi instalada." % (nos_um16, format(os.path.getsize(os.path.join(NOS, "um.py")), ",") if os.path.isfile(os.path.join(NOS, "um.py")) else AUS,
  time.strftime("%d/%m %H:%M", time.localtime(os.path.getmtime(os.path.join(NOS, "um.py")))) if os.path.isfile(os.path.join(NOS, "um.py")) else AUS, nos_ver))
falta_esp = [n for n in ("refazer_out_v402.txt",) if not os.path.exists(P(n))]
A("3. **Pré-condições (p00):** %s%s. **`sh -n` do `chain_pos_rito_v402.sh` medido AGORA:** %s. **`refazer_out_v402.txt`:** %s%s."
  % (("%s" % ("TODAS OK" if PRE["ok"] else "FALHARAM: " + "; ".join(pre_falhas))) if PRE else AUS,
     (" (arquivo de %s, mais antigo que arquivos do pós-rito: o número novo corrige a frase velha; regerar o p00)" % MT("PRECONDICOES_v402.json")) if pre_velho else "", sh_n, S16("refazer_out_v402.txt") if os.path.exists(P("refazer_out_v402.txt")) else AUS,
     " (sem ele, os harness do pós-rito só rodam em modo depuração `--nao-exigir-refazer` e a regeneração do candidato não fica comprovada)" if not os.path.exists(P("refazer_out_v402.txt")) else ""))
A("4. **A fila da memória:** o pós-rito pina o `MEMORY.md` por `memoria.py` (a gerência c1 é a única que escreve no diretório real; nenhum agente escreveu nele nesta preparação); o ensaio dela em CÓPIA está em `pos_rito\\FILA_MEMORIA_ENSAIO_v402.json` (tudo_passou = %s)." % tf(g(J("pos_rito", "FILA_MEMORIA_ENSAIO_v402.json"), "tudo_passou", default=None)))
A("")
A("## 5. A suíte do pós-rito (lida agora, no fecho da preparação; os JSON de depuração das iterações anteriores ficam em `pos_rito/depuracao`)")
A("")
A("%d arquivos em `pos_rito\\` (fora os `.bak_`: %d backups de bytes):" % (len(pos_arqs), len(pos_bak)))
A("")
for n in pos_arqs:
    A("- `%s` `%s` (%s B, %s)" % (n, S16("pos_rito", n), format(os.path.getsize(os.path.join(POSD, n)), ","), MT("pos_rito", n)))
A("")
if pos_json:
    A("JSON de harness e de ensaio com veredito:")
    A("")
    for n in pos_json:
        d = J("pos_rito", n)
        A("- `%s`: tudo_passou = %s; veredito = %s%s" % (n, tf(g(d, "tudo_passou", default=None)) if isinstance(d, dict) and "tudo_passou" in d else "n/a", str(g(d, "veredito", default="n/a"))[:140],
          ("; problemas: %d" % len(d["problemas"])) if isinstance(d, dict) and d.get("problemas") else ""))
    A("")
A("")
A("## 6. O que é ATO da gerência/operador (nada disto foi feito)")
A("")
A("1. **Instalar** (`instalar_v402.py`; confere o recibo pre_selo pinado, a Bancada ainda em v401 e a lista de módulos novos; backups de BYTES; troca por `os.replace`) — gerência.")
A("2. **Rodar o rito** (`rito_v402.sh`) e **conferir** (`conferir_rito_v402.py`, SEM `-I`); **reverter** se falhar (`reverter_v402.py`) — gerência.")
A("3. **Pós-rito** (`pos_rito\\chain_pos_rito_v402.sh`: a leitura, a fila da memória, as superfícies, o fechar, o `registrar_mapa_v402.py` que MONTA e não registra) — gerência; o passo das superfícies PARA se o `MEMORY.md` passar de 195 linhas.")
A("4. **B(n) com `V402_AUTORIZACAO_OPERADOR`** (parada e religamento do serviço na porta 18777; evento c1) — ato do operador.")
A("5. **Revisão independente** do candidato, dos derivados e dos textos (quem constrói não aprova) — a gerência escolhe o revisor.")
A("6. **Nomear as pedras** e **ratificar D11 e D13** (a D12 mantém `IsotropicPost` nomeada sobre uma rota que o operador aprovou; D16: os nomes são provisórios) — operador.")
A("7. **Registrar no mapa** (`rotas.py registrar`): primeiro `registro_mapa_v402_prep.json` (a rota de preparação, já validada por `rotas._valida`), depois `pos_rito\\registro_mapa_v402.json` (a rota selada, as anotações e as erratas com o seq corrigido) — gerência, `--quem` dela.")
A("8. **Rodar `regras_v402.py`** (escrito, NÃO rodado) — gerência. **Commit/push**, **[LEGAL] D2** e **CC art. 125** — operador com a agente de PI.")
A("")
A("## 7. O que FALTA e o que NÃO foi revisado")
A("")
A("1. **Revisão independente:** o gerador, o runtime dos registros, as três pedras (a da ponte foi recompilada pelo revisor no kernel v401; as outras duas só no sandbox da preparação), os derivados e os textos NÃO tiveram cético independente [DECLARADO: só os controles negativos próprios, a comparação AST e os harness].")
A("2. **O rito real** é o único que exercita o conferidor, o pós-rito e o h8 de verdade; o caminho positivo do conferidor e os harness são EMULAÇÃO sobre o Nós falso (core e selo do ensaio, não do rito).")
A("3. **Honestidade de escopo:** o cálculo de cada registro é numérico em dupla precisão e CONFERE os teoremas, não os prova; a lei de escala de Takesaki é dado [KNOWN]; H_τ na forma literal está REFUTADA no kernel (E1), e a v401 a escreveu: a correção vai ao lado, no mapa e nos registros; a ponte NÃO prova a primeira lei de Newton, nem a assinatura (1,3), nem rank c = 4, nem E = mc² composta da escala (E3).")
A("4. **Pendências nomeadas [OPEN]:** H_BW, H_cal, H3, a assinatura, rank c = 4, `IsotropicPost` sobre o atlas curvo, a dimensão 3 e o índice 1/β sem instância.")
A("")
A("## 8. Mapa de rotas consultado (antes) e o que devolveu")
A("")
if CONS:
    for q, r in CONS.items():
        A("- `rotas.py consultar \"%s\"` -> %d rota(s): %s" % (q, r["n"], ", ".join("`%s`" % x["rota_id"] for x in r["rotas"]) or "nenhuma"))
    A("")
    A("Livro com %s registros, cabeça `%s`. Rotas relevantes lidas: a da entrega do Codex (`kernel.ordem025.ponte_escala_dual`: PONTE_PARCIAL; não identificar p₊ escalante com massa invariante) — **só aparece por «ordem025»**, o consultar «ponte da escala dual» não devolve nada; as das duas pedras construídas em sandbox (`kernel.v402_queda_sem_geometria`, `kernel.v402_esperanca_condicional_e_nome`: não reprovar a mesma composição); a da pedra anterior (`kernel.v401_falsidade_da_inercia`) e a da v401 selada (`umpy.v401.selada_falsidade_da_inercia_25out`); a do B(n) (`infra.bancada_um.sincronizacao_vnnn`). "
      "O registro desta preparação é `registro_mapa_v402_prep.json` (montado e validado por `rotas._valida`, NÃO registrado)." % (mapa_n, mapa_cabeca))
else:
    A("O mapa de rotas NÃO foi lido nesta geração (%s)." % mapa_cabeca)
A("")
A("## 9. Arquivos principais (sha16 lido agora)")
A("")
for rel in ("um_v402_candidato.py", "CANDIDATO_v402.json", "ESPERADOS_v402.json", "ensaio_a_seco_v402.json", "PINOS_BN_v402.json", "PINO_RECIBO_PRE_SELO_v402.json", "PINO_MEMORIA_PY_v402.json", "PROVA_PRODUCAO_INTACTA_v402_pre_selo.json", "PRECONDICOES_v402.json", "COMPARACAO_V401_v402.json",
            "GUARDAS_ESTATICAS_BANCADA_v402.json", "kernel/KERNEL_RECIBO_v402.json", "kernel/FLAGS_v402.json", "kernel/KH_N1_v402.json", "DIFF_KERNEL_v402.txt", "conferencia_rito_v402_CONTROLE_NEGATIVO_PRE_RITO.json", "conferencia_rito_v402_POSITIVO_FALSO_NOS.json", "conferir_citacoes_v402.json",
            "registros_v402.py", "runtime_v402.py", "delta_v402.py", "gerar_candidato_v402.py", "gerar_esperados_v402.py", "instalar_v402.py", "reverter_v402.py", "rito_v402.sh", "conferir_rito_v402.py", "regras_v402.py", "registro_mapa_v402_prep.json", "gerar_registro_mapa_prep_v402.py",
            "pedra/PonteDaEscalaDual.lean", "pedra/QuedaSemGeometria.lean", "pedra/EsperancaCondicional.lean", "pos_rito/chain_pos_rito_v402.sh", "pos_rito/textos_v402.py", "pos_rito/leitura_v402.py", "pos_rito/registrar_mapa_v402.py", "pos_rito/fechar_v402.py",
            "bateria_pre_selo/NOTAS_PRE_SELO_v402.txt", "bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v402.json"):
    A("- `%s` `%s`" % (rel, S16(*rel.split("/"))))
A("")
A("NOT_FALSIFIED não é a palavra da creditação; validade no kernel não é creditação; o gate não se move.")
txt = "\n".join(L) + "\n"
# a guarda de palavras recusadas (P18) sobre o texto gerado
spg = importlib.util.spec_from_file_location("guarda_p18_v402", P("guarda_p18_v402.py")); gp = importlib.util.module_from_spec(spg); spg.loader.exec_module(gp)
viol = gp.violacoes(txt)
assert not viol, ("a guarda de texto (P18) achou violacao(oes) no ESTADO", viol[:3])
dst = P("ESTADO_V402.md")
if os.path.exists(dst) and open(dst, "rb").read() != txt.encode("utf-8"):
    open(dst + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_a2", "wb").write(open(dst, "rb").read())
open(dst + ".tmp", "w", encoding="utf-8", newline="\n").write(txt)
assert os.path.getsize(dst + ".tmp") > 4000 and open(dst + ".tmp", encoding="utf-8").readline().startswith("CADEIA v402 — preparada; a ponte da escala dual, a queda sem geometria e a esperança condicional")
os.replace(dst + ".tmp", dst)
print("ESTADO_V402.md", os.path.getsize(dst), "B | candidato um so':", cand_ok, "| Nos intacto:", nos_intacto, "| pre-condicoes:", ("AUSENTE" if PRE is None else ("OK" if PRE["ok"] else "FALHARAM %s" % pre_falhas)), "| ausentes:", falta_esp)

# -*- coding: utf-8 -*-
"""4a afericao no GERADOR DO PRE-REGISTRO: o rotulo do motor lido da contagem (E1..E<n>); a alternativa renomeada B_AMPLIADO_D64 (o «A» de 03/10 era o nivel
LEVE) e a ratificacao exige que a mensagem do operador NOMEIE a escolha; a frase do plano B sem margem comparada por script com o prazo DESTA especificacao;
a CPU: a construcao conferida por leitura na 1a afericao (nem E1..E8 nem a CPU a conferem), n(c2) em max_diffs e n(c3) nao calculado, NOT_COMPARABLE so com
a referencia desta rodada; o volume do MAGMA rotulado; a arvore com as tres condicoes do PARCIAL/CUSTODY e o modo zero do D128 mesmo com queda posterior;
«cerca de metade» no T4; os artefatos da rodada (details/cpuref) e o lancador como estao agora; as EVIDENCIAS por caminho e sha256 e, no congelamento,
copiadas para a pasta permanente. Backup de bytes; ast."""
import ast, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bak = P + ".bak_antes_afer4_" + time.strftime("%Y%m%d_%H%M%S")
open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
PAIRS = []
A = lambda o, n: PAIRS.append((o, n))
A('''import hashlib, json, math, os, sys, time''', '''import hashlib, json, math, os, re, shutil, sys, time''')
A('''       [--escolha=B_REDUZIDO|A]''', '''       [--escolha=B_REDUZIDO|B_AMPLIADO_D64]''')
A('''assert ESCOLHA in ("B_REDUZIDO", "A"), ESCOLHA''', '''assert ESCOLHA in ("B_REDUZIDO", "B_AMPLIADO_D64"), ESCOLHA   # 4a afericao: o «A» de 03/10 era o nivel LEVE; esta alternativa e' a MAIS PESADA
ESC_TOKEN = {"B_REDUZIDO": "b reduzido", "B_AMPLIADO_D64": "b ampliado"}   # a mensagem do operador tem de NOMEAR a escolha (normalizada)''')
A('''if ESCOLHA == "A":''', '''if ESCOLHA == "B_AMPLIADO_D64":''')
A('''_preA = (pre if ESCOLHA == "A" else pre + _extra_A)''', '''_preA = (pre if ESCOLHA == "B_AMPLIADO_D64" else pre + _extra_A)''')
# a ratificacao nomeia a escolha
A('''    assert r_, "a mensagem de ratificacao nao foi achada no transcrito: %r" % RAT_PREFIXO''',
  '''    assert r_, "a mensagem de ratificacao nao foi achada no transcrito: %r" % RAT_PREFIXO
    _nrm = lambda x: re.sub(r"[\\s_]+", " ", x.lower())
    assert ESC_TOKEN[ESCOLHA] in _nrm(r_[1]), "a mensagem do operador nao NOMEIA a escolha %s (esperado: %r)" % (ESCOLHA, ESC_TOKEN[ESCOLHA])''')
# o plano B sem margem contra o prazo DESTA especificacao
A('''r3 = lambda n: round(300.0 / n, 3)''', '''r3 = lambda n: round(300.0 / n, 3)
_preB = totB - estB["D128"]; _dl = SPEC["D128"]["start_deadline_s"]
_frase_preB = ("mesmo SEM margem, as fases do plano B antes do D128 levam cerca de %.0f min, %s do prazo de início desta especificação (%.0f min)%s" % (
    _preB / 60, "ACIMA" if _preB > _dl else "abaixo", _dl / 60,
    ": o D128 não rodaria" if _preB > _dl else ("; com a margem (%.0f min), não começaria" % (_preB * MARGEM / 60) if _preB * MARGEM > _dl else "")))''')
A('''"congelado de 5 h; e, mesmo SEM margem, as fases do plano B antes do D128 levam cerca de %.0f min, acima do prazo de início de %.0f min: o D128 não rodaria. Logo d = 64''',
  '''"congelado de 5 h; e %s. Logo d = 64''')
A('''        "NÃO cabe" if totB * MARGEM >= SPEC["execution"]["um_py_timeout_s"] else "cabe", (totB - estB["D128"]) / 60, 10800 / 60, PLANO_B["T1"]["16"],''',
  '''        "NÃO cabe" if totB * MARGEM >= SPEC["execution"]["um_py_timeout_s"] else "cabe", _frase_preB, PLANO_B["T1"]["16"],''')
# o nome da alternativa no documento
A('''    "alternativa_A": {"contagens_d64":''', '''    "alternativa_B_AMPLIADO_D64": {"nota": "não é o «nível A» de 03/10 (o leve, ~40 min): é a variante MAIS PESADA que o B_REDUZIDO", "contagens_d64":''')
A('''A("**Alternativa A (escolha do operador):** %s, prazo de início do D128 %s s — cerca de %s min a mais de GPU (%s com margem); antes do D128, com margem: %s min. %s" % (
    json.dumps(DESVIO["alternativa_A"]["contagens_d64"], ensure_ascii=False), DESVIO["alternativa_A"]["D128_start_deadline_s"],
    DESVIO["alternativa_A"]["minutos_a_mais_estimados"], DESVIO["alternativa_A"]["minutos_a_mais_com_margem"], DESVIO["alternativa_A"]["antes_do_D128_com_margem_min"],
    DESVIO["alternativa_A"]["leitura"])); A("")''',
  '''_AL = DESVIO["alternativa_B_AMPLIADO_D64"]
A("**Alternativa B_AMPLIADO_D64 (escolha do operador; %s):** %s, prazo de início do D128 %s s — cerca de %s min a mais de GPU (%s com margem); antes do D128, com margem: %s min. %s" % (
    _AL["nota"], json.dumps(_AL["contagens_d64"], ensure_ascii=False), _AL["D128_start_deadline_s"], _AL["minutos_a_mais_estimados"], _AL["minutos_a_mais_com_margem"],
    _AL["antes_do_D128_com_margem_min"], _AL["leitura"])); A("")''')
A('''print("plano B agora", DESVIO["plano_B"]["estimativa_com_os_custos_medidos_agora_min"], "c/ margem", DESVIO["plano_B"]["com_margem_min"], "| alt A +", DESVIO["alternativa_A"]["minutos_a_mais_estimados"],
      "c/ margem +", DESVIO["alternativa_A"]["minutos_a_mais_com_margem"], "antes do D128 sob A c/ margem", DESVIO["alternativa_A"]["antes_do_D128_com_margem_min"])''',
  '''print("plano B agora", DESVIO["plano_B"]["estimativa_com_os_custos_medidos_agora_min"], "c/ margem", DESVIO["plano_B"]["com_margem_min"], "| B_AMPLIADO_D64 +", _AL["minutos_a_mais_estimados"],
      "c/ margem +", _AL["minutos_a_mais_com_margem"], "antes do D128 sob B_AMPLIADO_D64 c/ margem", _AL["antes_do_D128_com_margem_min"])''')
A('''"restaura o T4 (%d) e o T2 (%d pontos) de d = 64 do plano B;''', '''"o B_AMPLIADO_D64 restaura o T4 (%d) e o T2 (%d pontos) de d = 64 do plano B;''')
A('''por folga, a alternativa A sobe esse prazo''', '''por folga, o B_AMPLIADO_D64 sobe esse prazo''')
# o rotulo do motor lido da contagem
A('''ENG_CHECKS = {c["name"]: c["ok"] for c in eng["engine_selftest"]["checks"]}''',
  '''ENG_CHECKS = {c["name"]: c["ok"] for c in eng["engine_selftest"]["checks"]}
ELBL = "E1..E%d" % len(ENG_CHECKS)   # o rotulo do motor LIDO da contagem (4a afericao)''')
A('''        "3. motor E1..E7 falhou -> ..._ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED",''', '''        "3. motor " + ELBL + " falhou -> ..._ENGINE_SELFTEST_FAILED__NO_RESULT__GATE_UNTOUCHED",''')
A('''ao reaproveitar, o motor (E1..E7) roda de novo no ambiente presente",''', '''ao reaproveitar, o motor (" + ELBL + ") roda de novo no ambiente presente",''')
A('''"autoteste_E1_E7": ENG_CHECKS,''', '''"autoteste_do_motor": ENG_CHECKS, "resultado_do_autoteste": {"arquivo": os.path.basename(ENGINE), "sha256": fsha(ENGINE)},''')
A('''A("- autoteste E1..E7: " + ", ".join(''', '''A("- autoteste " + ELBL + " (`%s`, sha256 `%s`): " % (os.path.basename(ENGINE), fsha(ENGINE)) + ", ".join(''')
# a CPU
A('''— a construção é conferida pelas fontes por sha256 e pelo E1..E8, não pela CPU —''',
  '''— a construção foi conferida por LEITURA, contra as fontes fixadas por sha256, na 1ª aferição; nem o E1..E8 nem a CPU a conferem —''')
A('''n(c²) e n(c³) só como INFORMAÇÃO (as potências λ^{1/2} e λ^{1/4} ampliam''', '''n(c²) só como INFORMAÇÃO, relatado em max_diffs (n(c³) a CPU nem calcula; as potências λ^{1/2} e λ^{1/4} ampliam''')
A('''se NENHUMA linha puder ser comparada, o veredito é CPU_REFERENCE_NOT_COMPARABLE (não houve discordância nem conferência)''',
  '''se NENHUMA linha puder ser comparada — com a referência DESTA rodada, o filho com código 0 e nenhuma linha da GPU faltando —, o veredito é CPU_REFERENCE_NOT_COMPARABLE (não houve discordância nem conferência); qualquer daquelas falhas dá CPU_REFERENCE_DISAGREES_OR_ABSENT''')
# a arvore
A('''        "7. uma identidade foi violada (inclusive o modo zero no D128) ->''', '''        "7. uma identidade foi violada (inclusive o modo zero no D128, mesmo que o D128 caia DEPOIS do espectro) ->''')
A('''quando o resultado é PARCIAL, em qualquer fase — a causa fica também em timed_out e worker_rc (um encerramento no meio do T4 lê-se PHASE_T4_FAILED; na espera da CPU, CPU_REFERENCE_DISAGREES_OR_ABSENT); ou __CUSTODY_CHAIN_INCOMPLETE (sha256, especificação, trabalhador, β ou marca da rodada não conferem)"],''',
  '''quando o resultado é PARCIAL — só se o código e a especificação conferem e o veredito foi rederivado; o primeiro parcial só existe depois do T3, logo uma morte no autoteste ou no T3 dá NOT_RUN__NO_RESULT_FILE —, e a causa fica também em timed_out e worker_rc (um encerramento no meio do T4 lê-se PHASE_T4_FAILED; na espera da CPU, CPU_REFERENCE_DISAGREES_OR_ABSENT); ou __CUSTODY_CHAIN_INCOMPLETE (sha256, especificação, trabalhador, β ou marca da rodada não conferem, ou o resultado não chegou ao Nós), este só em vereditos que não sejam RESULTS_VOID nem NOT_RUN"],''')
# T4
A('''em metade delas, uma rotação de base de Haar''', '''em cerca de metade delas (sorteio por instância, p = 1/2; o número de rotacionadas é relatado), uma rotação de base de Haar''')
# o MAGMA rotulado
A('''volume por tamanho do superoperador n = d²: %s; durabilidade do pipeline inteiro: %s (d ≤ 32); n = 16 384 (o D128) NUNCA foi testado, "''',
  '''volume do ESTRESSE e da caracterização por tamanho do superoperador n = d²: %s; em n = 4 096, mais %d chamadas nas sondas de tempo deste trabalhador (total %d); durabilidade do pipeline inteiro: %s (d ≤ 32); n = 16 384 (o D128) NUNCA foi testado, "''')
A('''            json.dumps({str(k): VOL[k] for k in sorted(VOL)}), json.dumps(DUR), json.dumps(N_RITO_D64))],''',
  '''            json.dumps({str(k): VOL[k] for k in sorted(VOL)}), N4096_TIM, N4096_EST + N4096_TIM, json.dumps(DUR), json.dumps(N_RITO_D64))],''')
# o arquivo do pilar, os artefatos da rodada, o lancador
A('''o arquivo do pilar de uma rodada anterior no Nós nunca sobrevive (um marcador desta rodada o substitui)",''',
  '''o arquivo do pilar de uma rodada anterior no Nós nunca sobrevive (um marcador desta rodada o substitui; se nem o marcador puder ser gravado, o arquivo é REMOVIDO e o selo registra a ausência); se a cópia do resultado ao Nós falhar, a cadeia de custódia não fecha (CUSTODY_CHAIN_INCOMPLETE, nada ao cache); o result.json leva o sha256 de details.jsonl e de cpuref.json, que ficam na pasta da rodada (Nós/quantum_pillar/run_<data>_<marca>/) — a custódia leva essa pasta junto, e o conferidor da versão final confere os dois contra o disco",''')
A('''enquanto o servidor estiver parado pelo rito, um marcador fica no pacote, e a rodada seguinte o lê e religa",''',
  '''recusa também com a tarefa DESABILITADA; um sinal ANTES do rito só restaura (não toca o stdout da tentativa anterior); a restauração não é interrompida por sinal e espera o fim de qualquer parada em curso antes de religar; enquanto o servidor estiver parado pelo rito, um marcador com restaurar=0|1 fica no pacote, e a rodada seguinte restaura o que ele gravou (se não houver rodada seguinte, a memória da v384 manda a gerência conferi-lo); INT/HUP só são capturados com o lançador em PRIMEIRO PLANO (POSIX) — ele roda em primeiro plano",''')
# as evidencias por caminho e sha256 (e, no congelamento, copiadas para a pasta permanente)
A('''    "afericao": DISP_J["texto_para_o_pre_registro"] + " (disposições achado a achado em %s, sha256 %s; registro verbatim em AFERIDOR_v384.txt)" % (os.path.basename(DISP), fsha(DISP)[:16]),''',
  '''    "afericao": DISP_J["texto_para_o_pre_registro"] + " (disposições achado a achado em %s, sha256 %s; registro verbatim em AFERIDOR_v384.txt, sha256 %s)" % (
        os.path.basename(DISP), fsha(DISP)[:16], fsha(os.path.join(ESTD, "AFERIDOR_v384.txt"))[:16]),
    "evidencias": EVID,''')
A('''ENG_CHECKS = {c["name"]: c["ok"] for c in eng["engine_selftest"]["checks"]}
ELBL''', '''# as EVIDENCIAS (4a afericao): caminho completo e sha256; no CONGELAMENTO (com a ratificacao), copiadas byte a byte para a pasta permanente
_EV = [("sonda_de_tempo", TIMING), ("autoteste_do_motor", ENGINE), ("plano_B", PLANO), ("afericao_2", AFER2), ("afericao_3", os.path.join(ESTD, "afericao3_resultado.json")),
       ("afericao_4", os.path.join(ESTD, "afericao4_resultado.json")), ("afericao_5", os.path.join(ESTD, "afericao5_resultado.json")), ("disposicoes", DISP),
       ("aferidor_verbatim", os.path.join(ESTD, "AFERIDOR_v384.txt"))] + [("estresse_" + k, p_) for k, p_ in EST.items()]
EVID = []
for _pp_, _p_ in _EV:
    if not os.path.exists(_p_):
        continue
    _e = {"papel": _pp_, "origem": _p_, "sha256": fsha(_p_)}
    if RAT:
        _dd = os.path.join(HERE, "evidencias_PREREGISTRO_V1"); os.makedirs(_dd, exist_ok=True)
        _dst = os.path.join(_dd, _pp_ + "__" + os.path.basename(_p_))
        if not os.path.exists(_dst):
            shutil.copyfile(_p_, _dst)
        assert fsha(_dst) == _e["sha256"], "a copia permanente da evidencia nao confere: %s" % _dst
        _e["copia_permanente"] = _dst
    EVID.append(_e)
ENG_CHECKS = {c["name"]: c["ok"] for c in eng["engine_selftest"]["checks"]}
ELBL''')
A('''A("## A aferição"); A(""); A(DOC["afericao"]); A("")''', '''A("## A aferição"); A(""); A(DOC["afericao"]); A("")
A("## As evidências (caminho e sha256%s)" % ("; cópias permanentes em evidencias_PREREGISTRO_V1/" if RAT else "")); A("")
for _e in EVID:
    A("- **%s**: `%s` — `%s`" % (_e["papel"], _e.get("copia_permanente") or _e["origem"], _e["sha256"]))
A("")''')
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:130])
    s = s.replace(old, new)
assert '"alternativa_A"' not in s and 'ESCOLHA == "A"' not in s, "sobrou o nome antigo"
ast.parse(s)
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), "trocas; backup", os.path.basename(bak))

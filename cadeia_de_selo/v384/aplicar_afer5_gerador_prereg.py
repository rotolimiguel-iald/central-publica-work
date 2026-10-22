# -*- coding: utf-8 -*-
"""5a afericao no GERADOR DO PRE-REGISTRO: caminhos absolutos; o rotulo do volume do MAGMA; a escolha NOMEADA por exatamente um token (com hifens aceitos) e
dita no rascunho; o lancador como e' (recusa com a tarefa desabilitada so quando o servidor seria religado; espera ate 60 s; o vigia nao e' morto; PID para
abortar; TERM sempre, INT/HUP conforme o modo de lancamento); a arvore (PARCIAL so com especificacao, trabalhador, beta e marca conferidos; CUSTODY pode vir
junto do PARCIAL, e o artigo le o composto como invalido); o D128 parcial gravado logo depois do espectro; o arquivo do pilar NOT_THIS_RUN; o criterio do T1
com sigma > 0; e, no congelamento, o rascunho apresentado e o gerador nas evidencias, com as obrigatorias exigidas. Backup de bytes; ast."""
import ast, glob, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
P = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
bk = sorted(glob.glob(P + ".bak_antes_afer5_*"))
assert bk and open(bk[-1], "rb").read() == raw, "o backup de antes da 5a nao e' o estado corrente"
PAIRS = []
A = lambda o, n: PAIRS.append((o, n))
A('''WORKER, TIMING, ENGINE, ESTD = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]''',
  '''WORKER, TIMING, ENGINE, ESTD = (os.path.abspath(x) for x in sys.argv[1:5])   # caminhos ABSOLUTOS no documento (5a afericao)''')
A('''volume do MAGMA por n: %s''', '''volume do MAGMA no estresse e na caracterização, por n (sem as sondas de tempo): %s''')
A('''    _nrm = lambda x: re.sub(r"[\\s_]+", " ", x.lower())
    assert ESC_TOKEN[ESCOLHA] in _nrm(r_[1]), "a mensagem do operador nao NOMEIA a escolha %s (esperado: %r)" % (ESCOLHA, ESC_TOKEN[ESCOLHA])''',
  '''    _nrm = lambda x: re.sub(r"[\\s_\\-\\u2010\\u2011\\u2012\\u2013]+", " ", x.lower())
    _toks = [e_ for e_, t_ in ESC_TOKEN.items() if re.search(r"\\b" + re.escape(t_) + r"\\b", _nrm(r_[1]))]
    assert _toks == [ESCOLHA], "a mensagem do operador tem de NOMEAR exatamente uma escolha (achadas: %s; --escolha=%s)" % (_toks, ESCOLHA)   # 5a afericao''')
A('''    A("**PENDENTE.** Este é o RASCUNHO (escolha %s) levado ao operador; nada se calcula com os operadores da teoria antes da ratificação, e o candidato instalável recusa um pré-registro sem ela." % ESCOLHA)''',
  '''    A("**PENDENTE.** Este é o RASCUNHO (escolha %s) levado ao operador; nada se calcula com os operadores da teoria antes da ratificação, e o candidato instalável recusa um pré-registro sem ela. **A mensagem de ratificação tem de nomear exatamente uma escolha: «b reduzido» (B_REDUZIDO) ou «b ampliado» (B_AMPLIADO_D64)**; hífen e sublinhado valem como espaço." % ESCOLHA)''')
A('''    "ratificacao": ({"quando": RAT["quando"], "escolha": ESCOLHA} if RAT else "PENDENTE -- levado ao operador junto com este rascunho")}''',
  '''    "ratificacao": ({"quando": RAT["quando"], "escolha": ESCOLHA} if RAT else "PENDENTE -- levado ao operador junto com este rascunho; a mensagem de ratificacao tem de nomear exatamente uma escolha: «b reduzido» ou «b ampliado»")}''')
A('''recusa também com a tarefa DESABILITADA; um sinal ANTES do rito só restaura (não toca o stdout da tentativa anterior); a restauração não é interrompida por sinal e espera o fim de qualquer parada em curso antes de religar; enquanto o servidor estiver parado pelo rito, um marcador com restaurar=0|1 fica no pacote, e a rodada seguinte restaura o que ele gravou (se não houver rodada seguinte, a memória da v384 manda a gerência conferi-lo); INT/HUP só são capturados com o lançador em PRIMEIRO PLANO (POSIX) — ele roda em primeiro plano",''',
  '''recusa também com a tarefa DESABILITADA quando o servidor seria religado (e com a sonda dela ilegível); um sinal ANTES do rito só restaura (não toca o stdout da tentativa anterior), DURANTE encerra só a árvore do um.py desta rodada (os descendentes do lançador) e grava RITO_RC=SINAL_<x>, DEPOIS só restaura e devolve o código do rito; a restauração não é interrompida por sinal, espera o vigia sair sozinho (ele termina a parada que estiver fazendo; até 120 s) e espera até 60 s que nenhuma parada esteja em curso antes de religar (com AVISO no log se expirar); enquanto o servidor estiver parado pelo rito, um marcador com restaurar=0|1 fica no pacote, e a rodada seguinte restaura o que ele gravou (se não houver rodada seguinte, a memória da v384 manda a gerência conferi-lo); TERM é sempre capturado, INT/HUP não se o lançador for iniciado com & por shell não interativo ou com nohup (POSIX); o PID do lançador fica em .rito_v384.pid, e abortar o rito é kill -TERM nesse PID",''')
A('''quando o resultado é PARCIAL — só se o código e a especificação conferem e o veredito foi rederivado;''',
  '''quando o resultado é PARCIAL — só se a especificação, o trabalhador, β e a marca da rodada conferem e o veredito foi rederivado;''')
A('''este só em vereditos que não sejam RESULTS_VOID nem NOT_RUN''',
  '''este só em vereditos que não sejam RESULTS_VOID nem NOT_RUN, e que PODE vir junto do PARCIAL (quando a cópia do parcial ao Nós falha) — o artigo lê o composto PARTIAL+CUSTODY como resultado não válido''')
A('''σ > 0: a fração dentro de 5% (β e p), com o ramo certificado, é RELATADA, sem limiar de decisão (curva de resolução).''',
  '''σ > 0: a fração com β dentro de 5% (relativo) e p dentro de 0,05 (absoluto), com o ramo certificado, é RELATADA, sem limiar de decisão (curva de resolução).''')
A('''se nem o marcador puder ser gravado, o arquivo é REMOVIDO e o selo registra a ausência);''',
  '''se nem o marcador puder ser gravado, o arquivo é REMOVIDO, com novas tentativas; e o SELO só hasheia o arquivo do pilar se ele for o que o runtime escreveu NESTA rodada — out_file_sha256, no registro —, senão grava NOT_THIS_RUN: mesmo com outro processo segurando o arquivo, o de outra rodada não passa por desta);''')
A('''mesmo que o D128 caia DEPOIS do espectro) ->''', '''mesmo que o D128 caia DEPOIS do espectro: o parcial é gravado logo depois do espectro, com n0 e zero_mode_ok, e sobrevive a uma morte do processo) ->''')
A('''    if not os.path.exists(_p_):
        continue''', '''    if not os.path.exists(_p_):
        assert _pp_ in EV_OPC, "evidencia obrigatoria ausente: %s (%s)" % (_pp_, _p_)   # so as opcionais podem faltar (5a afericao)
        continue''')
A('''       ("aferidor_verbatim", os.path.join(ESTD, "AFERIDOR_v384.txt"))] + [("estresse_" + k, p_) for k, p_ in EST.items()]''',
  '''       ("afericao_6", os.path.join(ESTD, "afericao6_resultado.json")), ("aferidor_verbatim", os.path.join(ESTD, "AFERIDOR_v384.txt"))] + [("estresse_" + k, p_) for k, p_ in EST.items()]
EV_OPC = {"afericao_6"}
if RAT:   # no congelamento, o RASCUNHO APRESENTADO (JSON e MD) e o proprio gerador entram nas evidencias (5a afericao)
    _EV += [("rascunho_apresentado_json", os.path.abspath(RASCUNHO_P)), ("rascunho_apresentado_md", os.path.abspath(RASCUNHO_P)[:-5] + ".md"), ("gerador", os.path.abspath(__file__))]''')
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:130])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), "trocas")

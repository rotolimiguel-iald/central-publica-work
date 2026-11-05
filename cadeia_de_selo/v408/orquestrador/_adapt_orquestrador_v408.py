# -*- coding: utf-8 -*-
"""_adapt_orquestrador_v408.py -- adapta orquestrador\\pos_treino_v408.py (subida mecanica do molde v407) a v408 (04/11/2026, claude-construtor-v408 [fork C], a servico da gerencia c1):
a ORDEM da v408 (fala do operador de 04/11/2026, OPERADOR_04nov_ordem_v408_...; o AUT traz a frase e o sha16 dela, e o orquestrador CONFERE o sha16 contra o arquivo antes de agir), o docstring (S0..S10 da v408),
o texto do S4 (os 4 modulos a frio; o tempo do sandbox LIDO de kernel/construir_marcas.txt; o rito da v407 lido de v407/rito_horarios_v407.txt), o S6a com o auto-raise da Bancada (D52: porta fechada E nenhum um_bancada -> sobe pelo comando do S6c e so' entao para pelo PID),
o passo NOVO S6d (D52: textos_custodia_handoff_v408_*.py ENCADEADO depois da chain 14 e antes do S7), a lista de passos do main e do --plano, e o S10 com o template desta pasta (D53). Substituicoes de contagem EXATA; backup de bytes; CRLF preservado. Escrito pela ferramenta Write."""
import ast, datetime, hashlib, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
P = os.path.join(HERE, "pos_treino_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8"); CRLF = "\r\n" in t; t = t.replace("\r\n", "\n")   # o molde subido e' LF (medido: 0 CR); o fim de linha que estiver e' o que se preserva
ORDEM_NOME = "OPERADOR_04nov_ordem_v408_liste_as_pedras_produza_rode_handoff_custodia_completa_verbatim.txt"
CUN = os.path.join(os.path.dirname(os.path.dirname(PK)), "cunhagens_13out")
_s16 = lambda n: hashlib.sha256(open(os.path.join(CUN, n), "rb").read()).hexdigest()[:16]
S16_ORDEM = _s16(ORDEM_NOME)
S16_03 = _s16("OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt")
S16_02 = _s16("OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt")
FRASE = "liste as pedras que eu preciso nominar e em seguida produza a v408, rode e quando estiver completa, dê a ordem de handoff para a sessão irmã realizar a custódia completa e atualizar tudo (site, repositório, e todos os links), todos os dispositovos e a central de patentes e em seguida publicar, push e commit de tudo"
assert FRASE in open(os.path.join(CUN, ORDEM_NOME), encoding="utf-8").read(), "a frase da ordem da v408 nao esta no arquivo da fala"
assert os.path.isfile(os.path.join(HERE, "ORDEM_RELEASE_APP_TEMPLATE.md")), "falta o template da ordem de release do app nesta pasta"


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


# 1) a marca e a nota
t, n_marca = re.subn(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n", "", t); assert n_marca == 1
sub("# [ADAPTADO v408, 03/11/2026, claude-prep-v408] molde: pos_treino_v407.py; novo: S10 (a ordem de release do app + o recibo conferido na fonte), as flags --plano e --ensaio (a seco); a gerencia lanca\n",
    "# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)] molde: pos_treino_v407.py FINAL; novo nesta versao: a ORDEM da v408 (04/11) como AUT, o S6a com o auto-raise da Bancada (D52), o passo S6d (D52: os textos da custodia ENCADEADOS antes do S7) e o template do S10 por D53; a gerencia lanca\n")
# 2) o docstring
i0 = t.index('"""pos_treino_v408.py'); i1 = t.index("import datetime as dt")
DOC = '''"""pos_treino_v408.py — O ORQUESTRADOR DA v408 (claude-construtor-v408, a serviço da gerência c1, 04/11/2026; molde: o orquestrador pós-treino da v407). Ordem do operador DESTA versão (04/11/2026, verbatim sha16 %(s16)s):
«%(frase)s»; herdadas e citadas: a de 03/11 (sha16 %(s03)s: «prossigamos com tudo, ratifico tudo» … «o orquestrador pode executar o que vc mandar») e a de 02/11 (sha16 %(s02)s: «compile a nova versão do um.py, rode, publique e atualize tudo por favor»).

O que faz, em ordem, fail-closed e retomável (estado em orquestrador/ESTADO.json; log em orquestrador/orquestrador.log):
  S0  o treino v4 da nativa já é TERMINAL (STATE_v4.json: DONE em 01/11/2026 22:03); o passo só confere e segue (não repete o treino).
  S1  espera a preparação da v408 (PREPARACAO_v408_PRONTA.json com pronta == true: kernel, candidato, ensaio a seco, esperados, conferidor, p00, B(n) pré-selo pinado).
  S1b exige a revisão de terceiro APROVADA sobre ESTE candidato (revisao_terceiro/REVISAO_TERCEIRO_v408.json; revisor: Sonnet, D54, até três rodadas): quem constrói não aprova.
  S2  pré-voo: o Nós é a v407 selada e é a origem do candidato; nenhum um.py/pilar vivo; disco; C:/t/vb21 ausente.
  S3  instalar_v408.py (ato da gerência, autorizado pela ordem acima).
  S4  rito_v408.sh pelo sh do Git (o lançador para e religa o servidor da nativa sozinho); exige RITO_RC=0 e selo v408 com o pin do candidato. Só 4 módulos novos compilam a frio (o tempo do sandbox é lido de kernel/construir_marcas.txt; o rito da v407, com 9, é lido de v407/rito_horarios_v407.txt; teto aqui: 5 h).
  S5  cadeia pós-rito 0 → 10 (conferidor, superfícies, memória pinada, B(n) ensaio).
  S6  10a: parada do serviço da Bancada Um PELO PID lido da porta 18777 (nunca por nome) + recibo; se a porta não escuta E não há processo um_bancada, o S6a SOBE o serviço pelo comando do S6c e só então para pelo PID (D52; a Bancada é de partida manual e não sobrevive a reinício);
      10b: evento c1 + B(n) APLICAR (B17; a produção pina B16-v407-20261104-R1); 10c: religamento pelo comando do recibo + recibo; depois 11 → 14; e ENTÃO S6d (D52): textos_custodia_handoff_v408_*.py ENCADEADO (os sete textos da custódia no handoff; rc 0 e o recibo), antes do S7.
  S7  custódia G1: planejar --seco, executar --publicar, auditar (código 5 = só decisões do operador).
  S10 a ORDEM de release do app e do contrato JEV: escreve C:/IALD/TUNEL_CLAUDE_APP/ORDEM_NNN_release_v408_do_app.md (versão e pino LIDOS do selo; molde orquestrador/ORDEM_RELEASE_APP_TEMPLATE.md, com a janela P2 do shared por D53: só a corrente e a anterior em literal completo) e ESPERA o recibo do orquestrador app
      (RELATORIO ou RESULTADOS/NNN_RESULTADO.json + INSTALLED_VERIFICATION.json + jev_control_v408.json), conferido NA FONTE (iald_nucleo_fixo.json do app: release e pino); sem recibo em 24 h = PARADA visível, nunca «ok»; só então confere na G1 (planejar --seco) que o C21 fechou.
  S8  a nativa: porta 8081 servindo o GGUF da v4 (já no ar desde 01/11; só confere e religa se cair).
  S9  relatório RELATORIO_POS_TREINO_v408.{json,md} + anotação no PROGRAMA.

Uso: python pos_treino_v408.py            (corre; a GERÊNCIA o lança, pela tarefa agendada IALD_pos_treino_v408, nunca à mão em janela)
     python pos_treino_v408.py --plano    (só leitura: os passos, o estado de cada um e os arquivos que o orquestrador usa; confere o sha16 da ordem contra o arquivo)
     python pos_treino_v408.py --ensaio   (a seco: o S10 contra um app SINTÉTICO — um caso positivo e controles negativos; não toca TUNEL_CLAUDE_APP, o app, o Nós nem ESTADO.json)

O que NÃO faz: não decide nomes, não move gate, não compacta memória, não mata processo por nome, não publica sem a custódia G1, não restaura nada sozinho depois de uma falha
(a decisão de restaurar é da gerência), não grava pensamento do dia (X_TEXTO = None). Parar: criar o arquivo orquestrador/PARAR (lido a cada volta).
Coautor da atribuição vigente: o da linha COAUTOR abaixo (herdado da v407)."""
''' % {"s16": S16_ORDEM, "frase": FRASE, "s03": S16_03, "s02": S16_02}
t = t[:i0] + DOC + t[i1:]
# 3) a ordem e a autorizacao
sub('ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_03nov_prossigamos_com_tudo_ratifico_tudo_orquestrador_claude_app_readme_pinado_teste_d_verbatim.txt"   # a ordem do operador DESTA versao (sha16 b89e4c909f37e163); a de 02/11 (compile, rode, publique e atualize tudo) foi a da v407',
    'ORDEM = CEN / "work" / "cunhagens_13out" / "%s"   # a ordem do operador DESTA versao (04/11/2026; o sha16 do arquivo e\' conferido por _conferir_ordem antes de agir); as de 03/11 e de 02/11 ficam citadas como herdadas' % ORDEM_NOME)
i0 = t.index('AUT = ("Ordem do operador de 03/11/2026'); i1 = t.index("X_TEXTO = None   #", i0)
t = t[:i0] + ('AUT = ("Ordem do operador de 04/11/2026 (verbatim sha16 %(s16)s): «%(frase)s»; "\n'
              '       "herdadas e citadas: a ordem de 03/11/2026 (sha16 %(s03)s: «prossigamos com tudo, ratifico tudo» … «o orquestrador pode executar o que vc mandar») e a de 02/11/2026 (sha16 %(s02)s: «compile a nova versão do um.py, rode, publique e atualize tudo por favor»). "\n'
              '       "A sincronização da Bancada Um (parada e religamento do serviço da porta 18777), a custódia completa e o release do app são parte de «atualizar tudo».")\n'
              'AUT_FRASE = "%(frase)s"   # a frase da ordem: tem de estar no ARQUIVO (conferido por _conferir_ordem) e e\' o que os recibos da Bancada conferem no AUT\n') % {"s16": S16_ORDEM, "frase": FRASE, "s03": S16_03, "s02": S16_02} + t[i1:]
sub("X_TEXTO = None   # v408: o orquestrador nao grava texto do X (a tarefa do dia o grava)", "X_TEXTO = None   # v408: o orquestrador nao grava texto do X (a tarefa do dia e o app Claude o gravam)")
# 3b) a conferencia da ordem (o sha16 do AUT contra o arquivo; a frase no arquivo): chamada no main e no --plano
sub("def jload(p):\n    return json.loads(Path(p).read_text(encoding=\"utf-8\"))\n",
    "def jload(p):\n    return json.loads(Path(p).read_text(encoding=\"utf-8\"))\n\n\n"
    "def _conferir_ordem():\n"
    "    \"\"\"fail-closed: o arquivo da ordem existe, o sha16 LIDO dele esta no AUT (o texto do AUT nao vale por si) e a frase do AUT esta no arquivo; senao o orquestrador nao age.\"\"\"\n"
    "    assert ORDEM.exists(), \"falta o verbatim da ordem do operador: %s\" % ORDEM\n"
    "    s = sha16(ORDEM); txt = ORDEM.read_text(encoding=\"utf-8\")\n"
    "    assert s in AUT, (\"o sha16 do arquivo da ordem nao e' o que o AUT cita: o AUT envelheceu ou o arquivo mudou\", s)\n"
    "    assert AUT_FRASE in txt and AUT_FRASE in AUT, \"a frase da ordem nao esta no arquivo da fala ou nao esta no AUT\"\n"
    "    return s\n")
# 4) o texto do S4: os tempos LIDOS (sandbox e rito da v407), nunca digitados
sub('    log("S4: lançando o rito v408 (sh do Git; o lançador para e religa o servidor da nativa; 9 módulos novos a frio; a v407, com 301, levou ~2 h 15 min; teto 5 h)")',
    '    log("S4: lançando o rito v408 (sh do Git; o lançador para e religa o servidor da nativa; 4 módulos novos a frio: no sandbox k408c o build levou %s s e o Audit %s s [kernel/construir_marcas.txt]; o rito da v407, com 9, levou %s [v407/rito_horarios_v407.txt]; teto 5 h)" % _tempos_lidos())')
sub("def s4_rito(e):\n", "def _tempos_lidos():\n"
    "    \"\"\"(build_s, audit_s, rito_v407) LIDOS dos arquivos: as marcas do sandbox desta versao e os horarios do rito da v407; 'n/d' onde o arquivo nao existe (nenhum numero digitado).\"\"\"\n"
    "    try:\n"
    "        mk = (PK / \"kernel\" / \"construir_marcas.txt\").read_text(encoding=\"utf-8\"); mm = {k: int(v) for k, v in re.findall(r\"^(epoch_\\w+)=(\\d+)$\", mk, re.M)}\n"
    "        b, a = mm[\"epoch_build_fim\"] - mm[\"epoch_inicio\"], mm[\"epoch_audit_fim\"] - mm[\"epoch_build_fim\"]\n"
    "    except Exception:  # noqa: BLE001\n"
    "        b, a = \"n/d\", \"n/d\"\n"
    "    try:\n"
    "        h0, h1 = (PK.parent / \"v407\" / \"rito_horarios_v407.txt\").read_text(encoding=\"utf-8\").split()[:2]\n"
    "        d = (dt.datetime.strptime(h1, \"%H:%M:%S\") - dt.datetime.strptime(h0, \"%H:%M:%S\")).total_seconds() % 86400\n"
    "        r = \"%dh%02d\" % (d // 3600, (d % 3600) // 60)\n"
    "    except Exception:  # noqa: BLE001\n"
    "        r = \"n/d\"\n"
    "    return b, a, r\n\n\ndef s4_rito(e):\n")
# 5) o S6a: o auto-raise da Bancada (D52)
sub('        rc, out, err = ps("$c = Get-NetTCPConnection -State Listen -LocalPort 18777 -ErrorAction SilentlyContinue | Select-Object -First 1; if ($c) { $p = Get-CimInstance Win32_Process -Filter (\\"ProcessId=\\" + $c.OwningProcess); Write-Output ($c.OwningProcess.ToString() + \'|\' + $p.CreationDate.ToString(\'yyyy-MM-ddTHH:mm:ss\') + \'|\' + $p.CommandLine) } else { Write-Output \'FECHADA\' }")\n'
    '        linha = out.splitlines()[-1] if out else ""\n'
    '        if linha == "FECHADA" or not linha:\n'
    '            marcar(e, "S6a_parada", False, motivo="a porta 18777 não escuta: o serviço da Bancada não está no ar (não paro o que não vejo); a gerência decide", saida=out[:200]); return False\n',
    '        CMD_PORTA = "$c = Get-NetTCPConnection -State Listen -LocalPort 18777 -ErrorAction SilentlyContinue | Select-Object -First 1; if ($c) { $p = Get-CimInstance Win32_Process -Filter (\\"ProcessId=\\" + $c.OwningProcess); Write-Output ($c.OwningProcess.ToString() + \'|\' + $p.CreationDate.ToString(\'yyyy-MM-ddTHH:mm:ss\') + \'|\' + $p.CommandLine) } else { Write-Output \'FECHADA\' }"\n'
    '        rc, out, err = ps(CMD_PORTA)\n'
    '        linha = out.splitlines()[-1] if out else ""\n'
    '        subiu = False\n'
    '        if linha == "FECHADA" or not linha:\n'
    '            # D52 (gerência c1, 04/11/2026; lição da v407): a Bancada Um é de partida manual e não sobrevive a reinício. Se a porta não escuta E não há processo um_bancada.py, o S6a SOBE o serviço pelo MESMO comando do S6c e só então para pelo PID (a cadeia desenhada: 10a parada → 10b B(n) → 10c religamento). Com processo vivo e porta fechada, PARA: não sobe por cima nem para por nome.\n'
    '            rc_b, out_b, _ = ps("@(Get-CimInstance Win32_Process -Filter \\"Name=\'python.exe\' OR Name=\'pythonw.exe\'\\" | Where-Object { $_.CommandLine -and $_.CommandLine -match \'um_bancada\\\\.py\' }).Count")\n'
    '            ult = (out_b.strip().splitlines() or [""])[-1].strip()\n'
    '            if ult != "0":\n'
    '                marcar(e, "S6a_parada", False, motivo="a porta 18777 não escuta mas a contagem de processos um_bancada.py não é zero (ou não foi legível: %r): não subo por cima nem paro por nome; a gerência decide" % ult, saida=out[:200]); return False\n'
    '            log("S6a: a porta 18777 não escuta e não há processo um_bancada.py: SUBO o serviço (D52) pelo comando do S6c e só então paro pelo PID")\n'
    '            ps("Start-Process -FilePath \'C:\\\\Python314\\\\pythonw.exe\' -ArgumentList \'-X\',\'utf8\',\'C:\\\\IALD\\\\Bancada_Um\\\\um_bancada.py\' -WorkingDirectory \'C:\\\\IALD\\\\Bancada_Um\' -WindowStyle Hidden")\n'
    '            for _ in range(60):\n'
    '                if porta_aberta(18777):\n'
    '                    break\n'
    '                time.sleep(3)\n'
    '            subiu = porta_aberta(18777)\n'
    '            rc, out, err = ps(CMD_PORTA)\n'
    '            linha = out.splitlines()[-1] if out else ""\n'
    '            if not subiu or linha == "FECHADA" or not linha:\n'
    '                marcar(e, "S6a_parada", False, motivo="a porta 18777 não escutou em 180 s depois de subir o serviço (D52): a gerência decide", saida=out[:200]); return False\n')
sub('        marcar(e, "S6a_parada", ok, rc=rc, pid=pid, criado=criado)\n', '        marcar(e, "S6a_parada", ok, rc=rc, pid=pid, criado=criado, subiu_antes_de_parar_D52=subiu)\n')
# 6) o S6d (D52): os textos da custodia ENCADEADOS depois da chain 14, antes do S7
sub('    return chain(e, "S6c_chain_10c_14", "10c", "14")\n\n\ndef s7_g1(e):\n',
    '    if not chain(e, "S6c_chain_10c_14", "10c", "14"):\n        return False\n    return s6d_textos_custodia(e)\n\n\n'
    'def s6d_textos_custodia(e):\n'
    '    """S6d (D52, lição da v407): os sete textos da custódia entram ENCADEADOS, depois da chain 14 e antes do S7: pos_rito/textos_custodia_handoff_v408_*.py (rc 0 e o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v408.json ao lado); sem isso o G1 planejar --seco parava em rc 20 na v407."""\n'
    '    if feito(e, "S6d_textos_custodia"):\n'
    '        return True\n'
    '    cands = sorted((PK / "pos_rito").glob("textos_custodia_handoff_v408_*.py"))\n'
    '    if len(cands) != 1:\n'
    '        marcar(e, "S6d_textos_custodia", False, motivo="esperava UM pos_rito/textos_custodia_handoff_v408_*.py", achados=[c.name for c in cands]); return False\n'
    '    rc = run([PY, "-B", "-X", "utf8", str(cands[0])], PK / "pos_rito", ORQ / "textos_custodia_out.txt", 1800)\n'
    '    rec = PK / "pos_rito" / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v408.json"\n'
    '    ok = rc == 0 and rec.exists()\n'
    '    marcar(e, "S6d_textos_custodia", ok, rc=rc, script=cands[0].name, recibo=(rec.name if rec.exists() else None))\n'
    '    return ok\n\n\ndef s7_g1(e):\n')
# 7) o --plano: a lista de passos, a conferencia da ordem e os arquivos que o orquestrador usa
sub('    passos = ["S0_treino", "S1_prep", "S1b_revisao", "S2_prevoo", "S3_instalar", "S4_rito", "S5_cadeia_0_10", "S6a_parada", "S6a_chain", "S6b_aplicar", "S6c_religamento", "S6c_chain_10c_14", "S7_g1", "S10_app", "S8_nativa"]',
    '    passos = ["S0_treino", "S1_prep", "S1b_revisao", "S2_prevoo", "S3_instalar", "S4_rito", "S5_cadeia_0_10", "S6a_parada", "S6a_chain", "S6b_aplicar", "S6c_religamento", "S6c_chain_10c_14", "S6d_textos_custodia", "S7_g1", "S10_app", "S8_nativa"]')
sub('    print("PLANO do orquestrador pos_treino_v408 (nada é executado):")\n', '    print("PLANO do orquestrador pos_treino_v408 (nada é executado); ordem do operador: %s (sha16 %s, conferido contra o arquivo); tempos lidos (build, Audit, rito v407): %s" % (ORDEM.name, _conferir_ordem(), _tempos_lidos()))\n')
sub('    print("arquivos que o orquestrador usa e NÃO existem:", faltam or "nenhum")\n',
    '    if len(list((PK / "pos_rito").glob("textos_custodia_handoff_v408_*.py"))) != 1:\n        faltam.append(str(PK / "pos_rito" / "textos_custodia_handoff_v408_*.py") + " (S6d, D52: exatamente um)")\n'
    '    print("arquivos que o orquestrador usa e NÃO existem:", faltam or "nenhum")\n')
# 8) o main: a conferencia da ordem antes de agir
sub('    assert ORDEM.exists(), "falta o verbatim da ordem do operador"\n', '    _conferir_ordem()   # fail-closed: o sha16 do arquivo da ordem esta no AUT e a frase esta no arquivo\n')
# 9) textos restantes do molde
sub('    """S10 (NOVO na v408): escreve a ORDEM de release do app', '    """S10 (herdado da v407; o template desta pasta traz a janela P2 do shared por D53): escreve a ORDEM de release do app')
assert "03/11/2026, claude-prep" not in t and "9 módulos novos a frio" not in t and S16_ORDEM in t and S16_03 in t and S16_02 in t and "a de 02/11 (compile, rode, publique e atualize tudo) foi a da v407" not in t
tt = t.replace("\n", "\r\n") if CRLF else t; ast.parse(tt); open(P, "wb").write(tt.encode("utf-8")); print("ok pos_treino_v408", len(raw), "->", len(tt.encode("utf-8")), "| sha16 da ordem", S16_ORDEM)

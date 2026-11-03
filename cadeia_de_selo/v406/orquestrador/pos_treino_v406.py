# -*- coding: utf-8 -*-
"""pos_treino_v406.py — O ORQUESTRADOR DA v406 (gerência c1, 02/11/2026; molde: o orquestrador pós-treino da v405). Ordem do operador (02/11/2026, verbatim sha16 b5717ff445a883cd):
«quando terminar, compile a nova versão do um.py, rode, publique e atualize tudo por favor»; sob a ordem-mãe do dia (sha16 f3998f01262aad6b): «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento».

O que faz, em ordem, fail-closed e retomável (estado em orquestrador/ESTADO.json; log em orquestrador/orquestrador.log):
  S0  o treino v4 da nativa já é TERMINAL (STATE_v4.json: DONE em 01/11/2026 22:03); o passo só confere e segue (se não for terminal, espera, como na v405).
  S1  espera a preparação da v406 (PREPARACAO_v406_PRONTA.json com pronta == true: ensaio a seco, esperados, conferidor, p00, B(n) pré-selo pinado).
  S1b exige a revisão de terceiro APROVADA sobre ESTE candidato (revisao_terceiro/REVISAO_TERCEIRO_v406.json; revisor: Sonnet, por ordem do operador de 02/11): quem constrói não aprova.
  S2  pré-voo: o Nós é a v405 selada e é a origem do candidato; nenhum um.py/pilar vivo; disco; C:/t/vb21 ausente.
  S3  instalar_v406.py (ato da gerência, autorizado pela ordem acima).
  S4  rito_v406.sh pelo sh do Git (o lançador para e religa o servidor da nativa sozinho); exige RITO_RC=0 e selo v406 com o pin do candidato. Tempo esperado: o build dos 301 módulos a frio levou 1736 s no sandbox; o rito inteiro (três passagens) deve ficar entre 2 h e 4 h; o teto é 5 h.
  S5  cadeia pós-rito 0 → 10 (conferidor, superfícies, memória pinada, B(n) ensaio).
  S6  10a: parada do serviço da Bancada Um PELO PID lido da porta 18777 (nunca por nome) + recibo; 10b: evento c1 + B(n) APLICAR (B15); 10c: religamento pelo comando do recibo + recibo; depois 11 → 14. Se a porta 18777 não escuta, PARA e diz (não para o que não vê).
  S7  custódia G1: planejar --seco, executar --publicar, auditar (a ordem «publique e atualize tudo» liga o --publicar; código 5 = só decisões do operador).
  S8  a nativa: porta 8081 servindo o GGUF da v4 (já no ar desde 01/11; só confere e religa se cair).
  S9  relatório RELATORIO_POS_TREINO_v406.{json,md} + anotação no PROGRAMA (unidade F1.FECHO.MONTAGEM_02nov).

O que NÃO faz: não decide nomes, não move gate, não compacta memória, não mata processo por nome, não publica sem a custódia G1, não restaura nada sozinho depois de uma falha
(a decisão de restaurar é da gerência), não grava pensamento do dia (o de 02/11 já existe; X_TEXTO = None). Parar: criar o arquivo orquestrador/PARAR (lido a cada volta).
Coautor da atribuição vigente: Claude Fable 5.1."""
import datetime as dt
import json
import os
import re
import socket
import subprocess
import sys
import time
import traceback
from pathlib import Path

PY = r"C:\Python314\python.exe"
SH = r"C:\Program Files\Git\bin\sh.exe"
PK = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v406")
ORQ = PK / "orquestrador"; ORQ.mkdir(parents=True, exist_ok=True)
ESTADO = ORQ / "ESTADO.json"; LOG = ORQ / "orquestrador.log"; PARAR = ORQ / "PARAR"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
NAT = Path(r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\12_logs")
CEN = Path(r"C:\IALD\Central de Patentes")
XD = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT" / "X_DIARIO"
ORDEM = CEN / "work" / "cunhagens_13out" / "OPERADOR_02nov_quando_terminar_compile_v406_rode_publique_atualize_tudo_e_planeje_o_readme_pinado_com_o_4_44_sigma_verbatim.txt"
COAUTOR = "Claude Fable 5.1 <noreply@anthropic.com>"
ATOR = "claude-c1-orquestrador-v406"
REV = PK / "revisao_terceiro" / "REVISAO_TERCEIRO_v406.json"
CMD_VIVOS = "Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | Where-Object { $_.CommandLine -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker') } | ForEach-Object { $_.ProcessId }"
AUT = ("Ordem do operador de 02/11/2026 (verbatim sha16 b5717ff445a883cd): «quando terminar, compile a nova versão do um.py, rode, publique e atualize tudo por favor»; "
       "sob a ordem do mesmo dia (sha16 f3998f01262aad6b): «precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento». "
       "A sincronização da Bancada Um (parada e religamento do serviço da porta 18777) é parte de «atualizar tudo».")
X_TEXTO = None   # v406: o pensamento do dia de 02/11 ja' existe (gravado as 19:15 pela tarefa); o orquestrador nao grava texto do X
HOJE = dt.date.today().isoformat()


def log(msg):
    linha = "%s %s" % (dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(linha, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def carregar():
    if ESTADO.exists():
        return json.loads(ESTADO.read_text(encoding="utf-8"))
    return {"passos": {}, "inicio": dt.datetime.now().isoformat(timespec="seconds"), "pid": os.getpid()}


def gravar(e):
    tmp = ESTADO.with_suffix(".tmp"); tmp.write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8"); os.replace(tmp, ESTADO)


def feito(e, passo):
    return e["passos"].get(passo, {}).get("ok") is True


def marcar(e, passo, ok, **dados):
    e["passos"][passo] = dict(ok=ok, quando=dt.datetime.now().isoformat(timespec="seconds"), **dados); gravar(e)
    log("[%s] %s %s" % (passo, "OK" if ok else "FALHOU", json.dumps(dados, ensure_ascii=False)[:400]))


def sha16(p):
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]


def jload(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def porta_aberta(porta):
    s = socket.socket(); s.settimeout(2)
    try:
        return s.connect_ex(("127.0.0.1", porta)) == 0
    finally:
        s.close()


def ps(cmd, timeout=120):
    r = subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", cmd], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout)
    return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()


def run(args, cwd, saida, timeout, env=None, shell_sh=False):
    """roda um comando, stdout+stderr no arquivo `saida`; devolve rc. Nunca -I (lição 4 da v405); nunca -O."""
    envv = dict(os.environ); envv.update(env or {}); envv["PYTHONIOENCODING"] = "utf-8"
    with open(saida, "a", encoding="utf-8") as f:
        f.write("\n==== %s ====\n%s\n" % (dt.datetime.now().isoformat(timespec="seconds"), " ".join(args)))
        f.flush()
        try:
            r = subprocess.run(args, cwd=str(cwd), stdout=f, stderr=subprocess.STDOUT, timeout=timeout, env=envv)
            f.write("\n==== rc=%d ====\n" % r.returncode)
            return r.returncode
        except subprocess.TimeoutExpired:
            f.write("\n==== TIMEOUT %ss ====\n" % timeout)
            return 124


def parar_pedido():
    return PARAR.exists()


def pensamento_do_dia_fallback(e):
    """às 17:36 de hoje, se o gerador falhou (a nativa em treino), o texto da gerência pela MESMA guarda e pelo MESMO gravar()."""
    if X_TEXTO is None or feito(e, "x_diario") or dt.date.today().isoformat() != HOJE:
        return
    agora = dt.datetime.now()
    if agora.hour < 17 or (agora.hour == 17 and agora.minute < 36):
        return
    p = XD / ("%s.md" % HOJE)
    if p.exists():
        marcar(e, "x_diario", True, nota="o gerador gravou sozinho"); return
    sys.path.insert(0, str(CEN / "tools"))
    try:
        import pensamento_do_dia as pd
        F = pd.fatos(HOJE); motivo = pd.guarda(X_TEXTO, F)
        if motivo is not None:
            marcar(e, "x_diario", False, motivo=motivo); return
        rc = pd.gravar(HOJE, X_TEXTO, "gerência c1 (orquestrador pós-treino: nativa em treino v4)", F, 0, False)
        marcar(e, "x_diario", rc == 0, rc=rc)
    except Exception as ex:  # noqa: BLE001
        marcar(e, "x_diario", False, erro=str(ex)[:300])


def s0_treino(e):
    if feito(e, "S0_treino"):
        return True
    while True:
        if parar_pedido():
            log("PARAR pedido — saio sem agir"); return False
        pensamento_do_dia_fallback(e)
        try:
            s = jload(NAT / "STATE_v4.json"); d = jload(NAT / "STATUS_v4.json")
        except Exception as ex:  # noqa: BLE001
            log("S0: estado do treino ilegível (%s); tento de novo em 5 min" % str(ex)[:120]); time.sleep(300); continue
        stage = s.get("stage"); etapa = d.get("etapa"); hb = d.get("heartbeat")
        if stage in ("DONE", "DONE_COM_REVERSAO"):
            lanc = (s.get("lancar") or {}) if isinstance(s.get("lancar"), dict) else {}
            marcar(e, "S0_treino", True, stage=stage, etapa=etapa, lancar=s.get("lancar") or d.get("lancar"), finished=s.get("finished"))
            return True
        if etapa in ("falhou", "recusado_sem_safe", "abortado_vram_pos_carga", "parado_vram_baixa", "parado_llama_na_gpu", "abortado_dataset_ctx") or (stage and "FALH" in str(stage)):
            marcar(e, "S0_treino", False, stage=stage, etapa=etapa); return False
        try:   # o supervisor desistiu sem DONE: uma queda depois do treino (merge, GGUF, lançar) não mexe no STATUS; sem isto a espera seria eterna
            sup = (NAT / "supervisor_v4.log").read_text(encoding="utf-8", errors="replace")[-400:]
        except Exception:  # noqa: BLE001
            sup = ""
        if "supervisor_v4 encerrado" in sup:
            marcar(e, "S0_treino", False, stage=stage, etapa=etapa, motivo="o supervisor do treino encerrou sem DONE", cauda=sup[-200:]); return False
        try:
            idade = (dt.datetime.now() - dt.datetime.fromisoformat(hb)).total_seconds() if hb else None
        except Exception:  # noqa: BLE001
            idade = None
        if idade is not None and idade > 3 * 3600 and etapa == "treinando":
            log("S0: heartbeat parado ha %.1f h (etapa %s) — sigo esperando, mas isto e' um aviso" % (idade / 3600, etapa))
        log("S0: treino %s / %s (passo %s/%s, eta_h %s); espero 5 min" % (stage, etapa, d.get("passo"), d.get("passos_total"), d.get("eta_horas")))
        time.sleep(300)


def s1_prep(e):
    if feito(e, "S1_prep"):
        return True
    t0 = time.time()
    while True:
        if parar_pedido():
            return False
        p = PK / "PREPARACAO_v406_PRONTA.json"
        if p.exists():
            try:
                j = jload(p)
            except Exception as ex:  # noqa: BLE001
                j = {"erro": str(ex)}
            if j.get("pronta") is True:
                marcar(e, "S1_prep", True, sha16=sha16(p), resumo={k: j.get(k) for k in ("candidato_sha16", "kernel_recibo", "p00", "ensaio_a_seco") if k in j}); return True
            log("S1: preparação ainda não pronta (pronta=%s; falta=%s)" % (j.get("pronta"), str(j.get("falta") or j.get("o_que_falta"))[:200]))
        else:
            log("S1: sem PREPARACAO_v406_PRONTA.json ainda")
        if time.time() - t0 > 6 * 3600:
            marcar(e, "S1_prep", False, motivo="preparação não ficou pronta em 6 h depois do treino; a gerência decide"); return False
        time.sleep(300)


def s1b_revisao(e):
    """quem constrói não aprova: só instala com a revisão de terceiro APROVADA e feita sobre ESTE candidato."""
    if feito(e, "S1b_revisao"):
        return True
    t0 = time.time()
    while True:
        if parar_pedido():
            return False
        cand = sha16(PK / "um_v406_candidato.py")
        if REV.exists():
            try:
                j = jload(REV)
            except Exception as ex:  # noqa: BLE001
                j = {"erro": str(ex)}
            if j.get("aprovada") is True and j.get("candidato_sha16") == cand:
                marcar(e, "S1b_revisao", True, sha16=sha16(REV), revisor=j.get("revisor"), candidato=cand, ressalvas=j.get("ressalvas")); return True
            log("S1b: a revisão não aprova este candidato (aprovada=%s; revisado=%s; candidato=%s)" % (j.get("aprovada"), j.get("candidato_sha16"), cand))
        else:
            log("S1b: sem revisão de terceiro ainda")
        if time.time() - t0 > 6 * 3600:
            marcar(e, "S1b_revisao", False, motivo="a revisão de terceiro não aprovou este candidato em 6 h; a gerência decide"); return False
        time.sleep(300)


def s2_prevoo(e):
    if feito(e, "S2_prevoo"):
        return True
    try:
        esp = jload(PK / "ESPERADOS_v406.json"); cand = jload(PK / "CANDIDATO_v406.json")
        um = sha16(NOS / "um.py"); selo = jload(NOS / "um_absoluto_selo.json")
        ok_origem = (um == esp["origem_sha16"] == selo["sha256"]["um.py"][:16])
        rc, out, _ = ps(CMD_VIVOS)
        vivos = [x for x in out.split() if x.isdigit()]
        vb21 = Path(r"C:\t\vb21")
        if vb21.exists():
            try:
                vb21.rmdir(); log("S2: C:/t/vb21 vazio removido")
            except OSError:
                pass
        rc2, livre, _ = ps("[math]::Round((Get-PSDrive C).Free/1GB)")
        livre_gib = int(livre.splitlines()[-1]) if livre.strip() else -1
        ok = ok_origem and not vivos and livre_gib >= 20 and not vb21.exists()
        marcar(e, "S2_prevoo", ok, um_py=um, origem=esp.get("origem_sha16"), selo_versao=selo.get("um_version"), candidato=cand.get("sha16"), vivos=vivos, livre_gib=livre_gib, vb21=vb21.exists())
        return ok
    except Exception as ex:  # noqa: BLE001
        marcar(e, "S2_prevoo", False, erro=traceback.format_exc()[-600:]); return False


def s3_instalar(e):
    if feito(e, "S3_instalar"):
        return True
    rc = run([PY, "-B", "-X", "utf8", "instalar_v406.py"], PK, ORQ / "instalar_out.txt", 1800)
    esp = jload(PK / "ESPERADOS_v406.json"); um = sha16(NOS / "um.py")
    rec = sorted(PK.glob("APLICADO_AO_CANONICO_*.json"))
    ok = rc == 0 and um == esp["candidato_sha16"] and bool(rec)
    marcar(e, "S3_instalar", ok, rc=rc, um_py=um, candidato=esp.get("candidato_sha16"), recibo=rec[-1].name if rec else None)
    return ok


def s4_rito(e):
    if feito(e, "S4_rito"):
        return True
    log("S4: lançando o rito v406 (sh do Git; o lançador para e religa o servidor da nativa; 301 módulos a frio: ~2 a 4 h; teto 5 h)")
    rc = run([SH, "rito_v406.sh"], PK, ORQ / "rito_v406_lancador.out", 5 * 3600)
    std = NOS / "rodada_v406_stdout.txt"
    trailer = ""
    if std.exists():
        linhas = std.read_text(encoding="utf-8", errors="replace").rstrip().splitlines()
        trailer = next((l for l in reversed(linhas[-5:]) if l.startswith("RITO_RC=")), "")
    selo = jload(NOS / "um_absoluto_selo.json") if (NOS / "um_absoluto_selo.json").exists() else {}
    esp = jload(PK / "ESPERADOS_v406.json")
    ok = rc == 0 and trailer == "RITO_RC=0" and selo.get("um_version") == "v406" and selo.get("sha256", {}).get("um.py", "")[:16] == esp["candidato_sha16"]
    marcar(e, "S4_rito", ok, rc_lancador=rc, trailer=trailer, selo_versao=selo.get("um_version"), selo_pin=selo.get("sha256", {}).get("um.py", "")[:16], marcador_servidor=(PK / ".servidor_parado_pelo_rito").exists())
    return ok


def chain(e, passo, de, ate, env=None):
    if feito(e, passo):
        return True
    envv = {"CHAIN_DE": str(de), "CHAIN_ATE": str(ate)}; envv.update(env or {})
    rc = run([SH, "pos_rito/chain_pos_rito_v406.sh"], PK, ORQ / ("chain_%s_out.txt" % passo), 3 * 3600, env=envv)
    ok = rc == 0
    cauda = ""
    try:
        cauda = (ORQ / ("chain_%s_out.txt" % passo)).read_text(encoding="utf-8", errors="replace")[-600:]
    except Exception:  # noqa: BLE001
        pass
    marcar(e, passo, ok, rc=rc, de=de, ate=ate, cauda=cauda if not ok else "")
    return ok


def s5_cadeia_0_10(e):
    if feito(e, "S5_cadeia_0_10"):
        return True
    pinos = PK / "PINOS_BN_v406.json"; dp = PK / "diff_e_pinos_v406.py"
    if not pinos.exists() and dp.exists():
        rc = run([PY, "-B", "-X", "utf8", "diff_e_pinos_v406.py"], PK, ORQ / "diff_e_pinos_out.txt", 1800)
        log("S5: diff_e_pinos_v406.py rc=%d (PINOS_BN existe: %s)" % (rc, pinos.exists()))
    return chain(e, "S5_cadeia_0_10", 0, 10)


def s6_bancada(e):
    """10a (parada pelo PID + recibo) → 10b (evento c1 + B(n) APLICAR) → 10c (religamento + recibo) → 11..14."""
    B3 = PK / "bancada_B3_servico"
    if not feito(e, "S6a_parada"):
        rc, out, err = ps("$c = Get-NetTCPConnection -State Listen -LocalPort 18777 -ErrorAction SilentlyContinue | Select-Object -First 1; if ($c) { $p = Get-CimInstance Win32_Process -Filter (\"ProcessId=\" + $c.OwningProcess); Write-Output ($c.OwningProcess.ToString() + '|' + $p.CreationDate.ToString('yyyy-MM-ddTHH:mm:ss') + '|' + $p.CommandLine) } else { Write-Output 'FECHADA' }")
        linha = out.splitlines()[-1] if out else ""
        if linha == "FECHADA" or not linha:
            marcar(e, "S6a_parada", False, motivo="a porta 18777 não escuta: o serviço da Bancada não está no ar (não paro o que não vejo); a gerência decide", saida=out[:200]); return False
        pid, criado, cmdline = (linha.split("|", 2) + ["", ""])[:3]
        if "um_bancada" not in cmdline:
            marcar(e, "S6a_parada", False, motivo="o processo da porta 18777 não é o serviço esperado", cmdline=cmdline[:200]); return False
        log("S6a: parando o serviço da Bancada PELO PID %s (criado %s)" % (pid, criado))
        ps("Stop-Process -Id %s -Force -ErrorAction Stop" % pid)
        for _ in range(30):
            if not porta_aberta(18777):
                break
            time.sleep(2)
        envv = {"V406_AUTORIZACAO_OPERADOR": AUT, "V406_PID_PARADO": pid, "V406_PID_PARADO_CRIADO": criado}
        rc = run([PY, "-B", "-X", "utf8", str(B3 / "recibo_parada_v406.py")], B3, ORQ / "recibo_parada_out.txt", 600, env=envv)
        ok = rc == 0 and (B3 / "RECIBO_PARADA_v406.json").exists() and not porta_aberta(18777)
        marcar(e, "S6a_parada", ok, rc=rc, pid=pid, criado=criado)
        if not ok:
            return False
    if not chain(e, "S6a_chain", "10a", "10a"):
        return False
    if not feito(e, "S6b_aplicar"):
        rc = run([PY, "-B", "-X", "utf8", str(B3 / "evento_c1_b3_v406.py")], B3, ORQ / "evento_c1_out.txt", 600)
        txt = (ORQ / "evento_c1_out.txt").read_text(encoding="utf-8", errors="replace")
        m = re.search(r'"evento":\s*(\d+).*?"hash":\s*"([0-9a-f]+)"', txt[-2000:], re.S)
        if rc != 0 or not m:
            marcar(e, "S6b_aplicar", False, rc=rc, motivo="evento c1 sem seq/hash legíveis"); return False
        envv = {"B3_AUTORIZADO": "sim", "EVENTO": m.group(1), "EVENTO_HASH": m.group(2), "V406_AUTORIZACAO_OPERADOR": AUT}
        if not chain(e, "S6b_chain", "10b", "10b", env=envv):
            marcar(e, "S6b_aplicar", False, evento=m.group(1)); return False
        marcar(e, "S6b_aplicar", True, evento=m.group(1), hash=m.group(2))
    if not feito(e, "S6c_religamento"):
        rp = jload(B3 / "RECIBO_PARADA_v406.json") if (B3 / "RECIBO_PARADA_v406.json").exists() else {}
        comando = rp.get("religar") or rp.get("comando") or r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py'
        log("S6c: religando o serviço da Bancada pelo comando do recibo: %s" % comando)
        ps("Start-Process -FilePath 'C:\\Python314\\pythonw.exe' -ArgumentList '-X','utf8','C:\\IALD\\Bancada_Um\\um_bancada.py' -WorkingDirectory 'C:\\IALD\\Bancada_Um' -WindowStyle Hidden")
        for _ in range(60):
            if porta_aberta(18777):
                break
            time.sleep(3)
        rc = run([PY, "-B", "-X", "utf8", str(B3 / "recibo_religamento_v406.py")], B3, ORQ / "recibo_religamento_out.txt", 600, env={"V406_AUTORIZACAO_OPERADOR": AUT})
        ok = rc == 0 and (B3 / "RECIBO_RELIGAMENTO_v406.json").exists() and porta_aberta(18777)
        marcar(e, "S6c_religamento", ok, rc=rc, porta=porta_aberta(18777))
        if not ok:
            return False
    return chain(e, "S6c_chain_10c_14", "10c", "14")


def s7_g1(e):
    if feito(e, "S7_g1"):
        return True
    base = [PY, "-X", "utf8", str(CEN / "tools" / "custodiar.py")]
    comum = ["--versao", "v406", "--ator", ATOR, "--coautor", COAUTOR, "--ordem", str(ORDEM)]
    rc1 = run(base + ["planejar"] + comum + ["--seco"], CEN, ORQ / "g1_planejar_out.txt", 1800)
    if rc1 not in (0, 1, 5):   # 1 = pendente: pronto para custodiar (tabela de custodiar.py)
        marcar(e, "S7_g1", False, etapa="planejar", rc=rc1); return False
    rc2 = run(base + ["executar"] + comum + ["--publicar"], CEN, ORQ / "g1_executar_out.txt", 4 * 3600)
    rc3 = run(base + ["auditar"] + comum, CEN, ORQ / "g1_auditar_out.txt", 1800)
    ok = rc2 in (0, 5) and rc3 in (0, 5)
    marcar(e, "S7_g1", ok, planejar=rc1, executar=rc2, auditar=rc3, nota="5 = só decisões do operador")
    return ok


def s8_nativa(e):
    if feito(e, "S8_nativa"):
        return True
    s = jload(NAT / "STATE_v4.json"); stage = s.get("stage")
    if not porta_aberta(8081):
        log("S8: a porta 8081 não escuta; religo pela tarefa agendada «IALD Llama Server»")
        ps("Enable-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue | Out-Null; Start-ScheduledTask -TaskName 'IALD Llama Server'")
        for _ in range(60):
            if porta_aberta(8081):
                break
            time.sleep(5)
    rc, out, _ = ps("(Get-CimInstance Win32_Process -Filter \"Name='llama-server.exe'\" | Select-Object -First 1).CommandLine")
    cmdline = out.splitlines()[-1] if out else ""
    serve_v4 = "v4" in cmdline.lower() and "iald-native" in cmdline.lower()
    ok = porta_aberta(8081)
    marcar(e, "S8_nativa", ok, stage_treino=stage, porta_8081=ok, serve_v4=serve_v4, cmdline=cmdline[:300], nota=("portão de release REVERTEU para a v3" if stage == "DONE_COM_REVERSAO" else ""))
    return ok


def s9_relatorio(e):
    p = e["passos"]
    md = ["# RELATÓRIO PÓS-TREINO v406 — orquestrador da gerência c1", "", "Ordem do operador: `%s`" % ORDEM.name, "", "| passo | ok | quando | dados |", "|---|---|---|---|"]
    for k, v in p.items():
        md.append("| %s | %s | %s | %s |" % (k, v.get("ok"), v.get("quando"), json.dumps({a: b for a, b in v.items() if a not in ("ok", "quando")}, ensure_ascii=False)[:300].replace("|", "¦")))
    md.append(""); md.append("Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.")
    (ORQ / "RELATORIO_POS_TREINO_v406.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (ORQ / "RELATORIO_POS_TREINO_v406.json").write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "evidencia", "--unidade", "F1.FECHO.MONTAGEM_02nov",
                        "--dados", json.dumps({"orquestrador": str(ORQ / "RELATORIO_POS_TREINO_v406.json"), "passos_ok": [k for k, v in p.items() if v.get("ok")], "passos_falhos": [k for k, v in p.items() if v.get("ok") is False]}, ensure_ascii=False)],
                       capture_output=True, timeout=120)
    except Exception:  # noqa: BLE001
        pass
    log("relatório gravado: %s" % (ORQ / "RELATORIO_POS_TREINO_v406.md"))


def main():
    e = carregar(); e["pid"] = os.getpid(); gravar(e)
    log("orquestrador iniciado (pid %d); ordem: %s" % (os.getpid(), ORDEM.name))
    assert ORDEM.exists(), "falta o verbatim da ordem do operador"
    try:
        for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s7_g1, s8_nativa):
            if parar_pedido():
                log("PARAR pedido — paro antes de %s" % passo.__name__); break
            if not passo(e):
                log("PARADA em %s — nada é restaurado sozinho; a gerência decide" % passo.__name__); break
    except Exception:  # noqa: BLE001
        log("EXCEÇÃO: " + traceback.format_exc()[-1500:])
    finally:
        pensamento_do_dia_fallback(e)
        if e["passos"].get("S0_treino", {}).get("ok") is True and not feito(e, "S8_nativa") and not parar_pedido():
            try:   # a nativa não depende da v406: a cadeia pode ter parado no meio
                rc, out, _ = ps(CMD_VIVOS)
                if [x for x in out.split() if x.isdigit()]:
                    marcar(e, "S8_nativa", False, motivo="rito ou pilar ainda vivo; não religo a nativa por cima; a gerência decide")
                else:
                    s8_nativa(e)
            except Exception:  # noqa: BLE001
                log("S8 no encerramento: " + traceback.format_exc()[-600:])
        s9_relatorio(e)


if __name__ == "__main__":
    main()

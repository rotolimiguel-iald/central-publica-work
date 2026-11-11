# -*- coding: utf-8 -*-
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] molde: pos_treino_v409.py FINAL (a subida mecanica fica em bump/); por _adapt_forkA_orquestrador_v410.py: a ORDEM da v410 (06/11; o arquivo, o sha16 e a frase lidos de delta_v410 e conferidos contra o arquivo) como AUT; SEM S7 e SEM S10 (D68a: o fim da cadeia e' o HANDOFF; a custodia completa e o release do app sao da sessao de custodia); o S6d roda os textos da custodia e o portao do G1, a D59 e a D65 sobre o handoff inteiro; a gerencia lanca (nao rodou).
"""pos_treino_v410.py — O ORQUESTRADOR DA v410 (claude-construtor-v410, a serviço da gerência c1, 06/11/2026; molde: o orquestrador pós-treino da v409). Ordem do operador DESTA versão (06/11/2026; o arquivo, o sha16 e a frase são LIDOS de delta_v410 e conferidos contra o arquivo):
«A forma de uma matriz finita no kernel é o signo (traço com sentido). E sim, tudo entra no um.py». O fim da cadeia é o HANDOFF (D68a, herda a D57a): a custódia completa (site, repositórios, links, dispositivos, Central, commit e push) e o release do app são da sessão de custódia, pela divisão de 04/11.

O que faz, em ordem, fail-closed e retomável (estado em orquestrador/ESTADO.json; log em orquestrador/orquestrador.log):
  S0  o treino v4 da nativa já é TERMINAL (STATE_v4.json: DONE em 01/11/2026 22:03); o passo só confere e segue (não repete o treino).
  S1  espera a preparação da v410 (PREPARACAO_v410_PRONTA.json com pronta == true: kernel, candidato, ensaio a seco, esperados, conferidor, p00, B(n) pré-selo pinado).
  S1b exige a revisão de terceiro APROVADA sobre ESTE candidato (revisao_terceiro/REVISAO_TERCEIRO_v410.json; revisor: Sonnet, D69, até três rodadas): quem constrói não aprova.
  S2  pré-voo: o Nós é a v409 selada e é a origem do candidato; nenhum um.py/pilar vivo; disco; C:/t/vb21 ausente.
  S3  instalar_v410.py (ato da gerência, autorizado pela ordem acima).
  S4  rito_v410.sh pelo sh do Git (o lançador para e religa o servidor da nativa sozinho); exige RITO_RC=0 e selo v410 com o pin do candidato. São 2 módulos novos a compilar a frio, IALD2 e AEscala (o tempo do sandbox é lido de kernel/construir_marcas.txt; o rito da v409, com 2, é lido de v409/rito_horarios_v409.txt; teto aqui: 5 h).
  S5  cadeia pós-rito 0 → 10 (conferidor, superfícies, memória pinada, B(n) ensaio).
  S6  10a: parada do serviço da Bancada Um PELO PID lido da porta 18777 (nunca por nome) + recibo; se a porta não escuta E não há processo um_bancada, o S6a SOBE o serviço pelo comando do S6c e só então para pelo PID (D52; a Bancada é de partida manual e não sobrevive a reinício);
      10b: evento c1 + B(n) APLICAR (B19; a produção pina B18-v409-20261106-R1); 10c: religamento pelo comando do recibo + recibo; depois 11 → 14; e ENTÃO S6d (D52, D57): textos_custodia_handoff_v410.py ENCADEADO (os sete textos da custódia no handoff; rc 0 e o recibo) e o portão do G1 (custodia_g1.textos.portao), a D59 e a D65 sobre o HANDOFF INTEIRO (o do Nós e o da memória). O handoff é o FIM da cadeia.
  (SEM S7 e SEM S10 nesta versão, D68a, que herda a D57a: a custódia G1 com --publicar e a ORDEM de release do app são da sessão de custódia; as funções s7_g1 e s10_app ficam no arquivo como registro e NÃO são chamadas.)
  S8  a nativa: porta 8081 servindo o GGUF da v4 (já no ar desde 01/11; só confere e religa se cair).
  S9  relatório RELATORIO_POS_TREINO_v410.{json,md} + anotação no PROGRAMA.
  S9_gatilho_custodia (ADITIVO 1 à ordem do conserto único, 10/11/2026: a custódia da v410 é automática): o passo FINAL, depois de tudo: escreve work/cadeia_de_selo/v410/ORDEM_HANDOFF_CUSTODIA_v410.md, o gatilho que a sessão de custódia espera, pelo molde da v409, com todos os valores LIDOS por script;
      só escreve SE todos os passos anteriores estiverem feitos e verdadeiros, o HANDOFF existir no Nós com os sete marcadores e os dois blocos do README, e o portão do G1 tiver rodado limpo no S6d; senão NÃO escreve e registra o motivo (fail-closed); a escrita é por temporário e os.replace.

Uso: python pos_treino_v410.py            (corre; a GERÊNCIA o lança, pela tarefa agendada IALD_pos_treino_v410, nunca à mão em janela)
     python pos_treino_v410.py --plano    (só leitura: os passos, o estado de cada um e os arquivos que o orquestrador usa; confere o sha16 da ordem contra o arquivo)
     python pos_treino_v410.py --ensaio   (só leitura: o mesmo que --plano; o ensaio do S10 não roda, porque o S10 não é desta versão, D57)

O que NÃO faz: não decide nomes, não move gate, não compacta memória, não mata processo por nome, não publica sem a custódia G1, não restaura nada sozinho depois de uma falha
(a decisão de restaurar é da gerência), não grava pensamento do dia (X_TEXTO = None), não publica, não faz commit nem push, não escreve ordem ao app (D57). Parar: criar o arquivo orquestrador/PARAR (lido a cada volta).
Coautor da atribuição vigente: o da linha COAUTOR abaixo (herdado da v409)."""
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
PK = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410")
ORQ = PK / "orquestrador"; ORQ.mkdir(parents=True, exist_ok=True)
ESTADO = ORQ / "ESTADO.json"; LOG = ORQ / "orquestrador.log"; PARAR = ORQ / "PARAR"
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
NAT = Path(r"C:\IALD\TGL_IALD_NATIVE_QWEN5090\12_logs")
CEN = Path(r"C:\IALD\Central de Patentes")
XD = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT" / "X_DIARIO"
sys.path.insert(0, str(PK))
import delta_v410 as _DL  # noqa: E402   (o nome do arquivo da ordem, o sha16 pinado dela e a frase verbatim saem do delta: nada digitado aqui)
ORDEM = CEN / "work" / "cunhagens_13out" / _DL.N_ORDEM_V410   # a ordem do operador DESTA versao (05/11/2026; o sha16 do arquivo e' conferido por _conferir_ordem contra o pino do delta antes de qualquer ato)
COAUTOR = "Claude Fable 5.1 <noreply@anthropic.com>"
ATOR = "claude-c1-orquestrador-v410"
REV = PK / "revisao_terceiro" / "REVISAO_TERCEIRO_v410.json"
CMD_VIVOS = "Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | Where-Object { $_.CommandLine -and ($_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|$)' -or $_.CommandLine -match 'pilar_quantico_worker') } | ForEach-Object { $_.ProcessId }"
AUT_FRASE = _DL.FRASE_ORDEM_V410   # a frase da ordem (verbatim, do delta): tem de estar no ARQUIVO (conferido por _conferir_ordem) e e' o que os recibos da Bancada recebem no AUT
AUT = ("Ordem do operador de 06/11/2026 (verbatim sha16 %s): «%s» (a ordem da v410: a forma de matriz finita é o signo, e tudo entra no um.py). "
       "D68a (gerência c1, em nome próprio, 06/11; herda a D57a): o fim da cadeia do orquestrador é o HANDOFF; a sincronização da Bancada Um (parada e religamento do serviço da porta 18777, o B(n) da versão) segue o rito da casa como na v409; "
       "a custódia completa e o release do app são da sessão de custódia." % (_DL.VERBATIM_PREFIXOS_DA_ORDEM_V410[_DL.N_ORDEM_V410], AUT_FRASE))
X_TEXTO = None   # v410: o orquestrador nao grava texto do X (a tarefa do dia e o app Claude o gravam)
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


def _conferir_ordem():
    """fail-closed: o arquivo da ordem existe, o sha16 LIDO dele e' o pinado em delta_v410 e esta no AUT (o texto do AUT nao vale por si) e a frase do AUT esta no arquivo; senao o orquestrador nao age."""
    assert ORDEM.exists(), "falta o verbatim da ordem do operador: %s" % ORDEM
    s = sha16(ORDEM); txt = ORDEM.read_text(encoding="utf-8")
    assert s == _DL.VERBATIM_PREFIXOS_DA_ORDEM_V410[_DL.N_ORDEM_V410], ("o sha16 do arquivo da ordem != o pinado em delta_v410", s)
    assert s in AUT, ("o sha16 do arquivo da ordem nao e' o que o AUT cita: o AUT envelheceu ou o arquivo mudou", s)
    assert AUT_FRASE in txt and AUT_FRASE in AUT, "a frase da ordem nao esta no arquivo da fala ou nao esta no AUT"
    return s


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
    """roda um comando, stdout+stderr no arquivo `saida`; devolve rc. Nunca -I (lição 4 da v409); nunca -O."""
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
        p = PK / "PREPARACAO_v410_PRONTA.json"
        if p.exists():
            try:
                j = jload(p)
            except Exception as ex:  # noqa: BLE001
                j = {"erro": str(ex)}
            if j.get("pronta") is True:
                marcar(e, "S1_prep", True, sha16=sha16(p), resumo={k: j.get(k) for k in ("candidato_sha16", "kernel_recibo", "p00", "ensaio_a_seco") if k in j}); return True
            log("S1: preparação ainda não pronta (pronta=%s; falta=%s)" % (j.get("pronta"), str(j.get("falta") or j.get("o_que_falta"))[:200]))
        else:
            log("S1: sem PREPARACAO_v410_PRONTA.json ainda")
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
        cand = sha16(PK / "um_v410_candidato.py")
        if REV.exists():
            try:
                j = jload(REV)
            except Exception as ex:  # noqa: BLE001
                j = {"erro": str(ex)}
            ruins = [k for k, v in (j.get("arquivos_revisados") or {}).items() if (PK / k).is_file() and sha16(PK / k) != v]   # [R2, 03/11] BAIXO 9: os arquivos revisados (pos_rito, orquestrador...) tem de ser os do disco
            if j.get("aprovada") is True and j.get("candidato_sha16") == cand and not ruins:
                marcar(e, "S1b_revisao", True, sha16=sha16(REV), revisor=j.get("revisor"), candidato=cand, ressalvas=j.get("ressalvas"), arquivos_revisados=len(j.get("arquivos_revisados") or {})); return True
            if ruins:
                log("S1b: %d arquivo(s) revisado(s) mudaram depois da revisao (ex.: %s): a revisao nao vale para eles" % (len(ruins), ruins[:3]))
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
        esp = jload(PK / "ESPERADOS_v410.json"); cand = jload(PK / "CANDIDATO_v410.json")
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
    rc = run([PY, "-B", "-X", "utf8", "instalar_v410.py"], PK, ORQ / "instalar_out.txt", 1800)
    esp = jload(PK / "ESPERADOS_v410.json"); um = sha16(NOS / "um.py")
    rec = sorted(PK.glob("APLICADO_AO_CANONICO_*.json"))
    ok = rc == 0 and um == esp["candidato_sha16"] and bool(rec)
    marcar(e, "S3_instalar", ok, rc=rc, um_py=um, candidato=esp.get("candidato_sha16"), recibo=rec[-1].name if rec else None)
    return ok


def _tempos_lidos():
    """(build_s, audit_s, rito_v409) LIDOS dos arquivos: as marcas do sandbox desta versao e os horarios do rito da v409; 'n/d' onde o arquivo nao existe (nenhum numero digitado)."""
    try:
        mk = (PK / "kernel" / "construir_marcas.txt").read_text(encoding="utf-8"); mm = {k: int(v) for k, v in re.findall(r"^(epoch_\w+)=(\d+)$", mk, re.M)}
        b, a = mm["epoch_build_fim"] - mm["epoch_inicio"], mm["epoch_audit_fim"] - mm["epoch_build_fim"]
    except Exception:  # noqa: BLE001
        b, a = "n/d", "n/d"
    try:
        h0, h1 = (PK.parent / "v409" / "rito_horarios_v409.txt").read_text(encoding="utf-8").split()[:2]
        d = (dt.datetime.strptime(h1, "%H:%M:%S") - dt.datetime.strptime(h0, "%H:%M:%S")).total_seconds() % 86400
        r = "%dh%02d" % (d // 3600, (d % 3600) // 60)
    except Exception:  # noqa: BLE001
        r = "n/d"
    return b, a, r


def s4_rito(e):
    """S4: o rito da v410. NOTA D73 (decisao da gerencia c1, 09/11/2026; a fala do operador: «o treino concordo com sua proposta»): o treino do Qwen3.8 (CPU, 48 threads, sem GPU) corre JUNTO com a cadeia: o lancador do rito so' para o servidor da nativa e o trabalhador do pilar quantico;
    os processos treinar.py e campanha.py NAO se tocam; o teto deste passo (5 h) decide: se estourar, a gerencia pausa o treino PELO PID medido (checkpoint a cada passo), roda e retoma por `campanha.py retomar`. A duracao do build, do Audit e do rito e' registrada
    (kernel/construir_marcas.txt e rito_horarios) para medir a contencao; ela e' MEDIDA, nao presumida. Esta nota nao muda a logica do passo."""
    if feito(e, "S4_rito"):
        return True
    log("S4: lançando o rito v410 (sh do Git; o lançador para e religa o servidor da nativa; 2 módulos novos a frio, IALD2 e AEscala: no sandbox k410c o build levou %s s e o Audit %s s [kernel/construir_marcas.txt]; o rito da v409, com 4, levou %s [v409/rito_horarios_v409.txt]; teto 5 h)" % _tempos_lidos())
    rc = run([SH, "rito_v410.sh"], PK, ORQ / "rito_v410_lancador.out", 5 * 3600)
    std = NOS / "rodada_v410_stdout.txt"
    trailer = ""
    if std.exists():
        linhas = std.read_text(encoding="utf-8", errors="replace").rstrip().splitlines()
        trailer = next((l for l in reversed(linhas[-5:]) if l.startswith("RITO_RC=")), "")
    selo = jload(NOS / "um_absoluto_selo.json") if (NOS / "um_absoluto_selo.json").exists() else {}
    esp = jload(PK / "ESPERADOS_v410.json")
    ok = rc == 0 and trailer == "RITO_RC=0" and selo.get("um_version") == "v410" and selo.get("sha256", {}).get("um.py", "")[:16] == esp["candidato_sha16"]
    marcar(e, "S4_rito", ok, rc_lancador=rc, trailer=trailer, selo_versao=selo.get("um_version"), selo_pin=selo.get("sha256", {}).get("um.py", "")[:16], marcador_servidor=(PK / ".servidor_parado_pelo_rito").exists())
    return ok


def chain(e, passo, de, ate, env=None):
    if feito(e, passo):
        return True
    envv = {"CHAIN_DE": str(de), "CHAIN_ATE": str(ate)}; envv.update(env or {})
    rc = run([SH, "pos_rito/chain_pos_rito_v410.sh"], PK, ORQ / ("chain_%s_out.txt" % passo), 3 * 3600, env=envv)
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
    pinos = PK / "PINOS_BN_v410.json"; dp = PK / "diff_e_pinos_v410.py"
    if not pinos.exists() and dp.exists():
        rc = run([PY, "-B", "-X", "utf8", "diff_e_pinos_v410.py"], PK, ORQ / "diff_e_pinos_out.txt", 1800)
        log("S5: diff_e_pinos_v410.py rc=%d (PINOS_BN existe: %s)" % (rc, pinos.exists()))
    return chain(e, "S5_cadeia_0_10", 0, 10)


def s6_bancada(e):
    """10a (parada pelo PID + recibo) → 10b (evento c1 + B(n) APLICAR) → 10c (religamento + recibo) → 11..14."""
    B3 = PK / "bancada_B3_servico"
    if not feito(e, "S6a_parada"):
        CMD_PORTA = "$c = Get-NetTCPConnection -State Listen -LocalPort 18777 -ErrorAction SilentlyContinue | Select-Object -First 1; if ($c) { $p = Get-CimInstance Win32_Process -Filter (\"ProcessId=\" + $c.OwningProcess); Write-Output ($c.OwningProcess.ToString() + '|' + $p.CreationDate.ToString('yyyy-MM-ddTHH:mm:ss') + '|' + $p.CommandLine) } else { Write-Output 'FECHADA' }"
        rc, out, err = ps(CMD_PORTA)
        linha = out.splitlines()[-1] if out else ""
        subiu = False
        if linha == "FECHADA" or not linha:
            # D52 (gerência c1, 04/11/2026; lição da v409): a Bancada Um é de partida manual e não sobrevive a reinício. Se a porta não escuta E não há processo um_bancada.py, o S6a SOBE o serviço pelo MESMO comando do S6c e só então para pelo PID (a cadeia desenhada: 10a parada → 10b B(n) → 10c religamento). Com processo vivo e porta fechada, PARA: não sobe por cima nem para por nome.
            rc_b, out_b, _ = ps("@(Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | Where-Object { $_.CommandLine -and $_.CommandLine -match 'um_bancada\\.py' }).Count")
            ult = (out_b.strip().splitlines() or [""])[-1].strip()
            if ult != "0":
                marcar(e, "S6a_parada", False, motivo="a porta 18777 não escuta mas a contagem de processos um_bancada.py não é zero (ou não foi legível: %r): não subo por cima nem paro por nome; a gerência decide" % ult, saida=out[:200]); return False
            log("S6a: a porta 18777 não escuta e não há processo um_bancada.py: SUBO o serviço (D52) pelo comando do S6c e só então paro pelo PID")
            ps("Start-Process -FilePath 'C:\\Python314\\pythonw.exe' -ArgumentList '-X','utf8','C:\\IALD\\Bancada_Um\\um_bancada.py' -WorkingDirectory 'C:\\IALD\\Bancada_Um' -WindowStyle Hidden")
            for _ in range(60):
                if porta_aberta(18777):
                    break
                time.sleep(3)
            subiu = porta_aberta(18777)
            rc, out, err = ps(CMD_PORTA)
            linha = out.splitlines()[-1] if out else ""
            if not subiu or linha == "FECHADA" or not linha:
                marcar(e, "S6a_parada", False, motivo="a porta 18777 não escutou em 180 s depois de subir o serviço (D52): a gerência decide", saida=out[:200]); return False
        pid, criado, cmdline = (linha.split("|", 2) + ["", ""])[:3]
        if "um_bancada" not in cmdline:
            marcar(e, "S6a_parada", False, motivo="o processo da porta 18777 não é o serviço esperado", cmdline=cmdline[:200]); return False
        log("S6a: parando o serviço da Bancada PELO PID %s (criado %s)" % (pid, criado))
        ps("Stop-Process -Id %s -Force -ErrorAction Stop" % pid)
        for _ in range(30):
            if not porta_aberta(18777):
                break
            time.sleep(2)
        envv = {"V410_AUTORIZACAO_OPERADOR": AUT, "V410_PID_PARADO": pid, "V410_PID_PARADO_CRIADO": criado}
        rc = run([PY, "-B", "-X", "utf8", str(B3 / "recibo_parada_v410.py")], B3, ORQ / "recibo_parada_out.txt", 600, env=envv)
        ok = rc == 0 and (B3 / "RECIBO_PARADA_v410.json").exists() and not porta_aberta(18777)
        marcar(e, "S6a_parada", ok, rc=rc, pid=pid, criado=criado, subiu_antes_de_parar_D52=subiu)
        if not ok:
            return False
    if not chain(e, "S6a_chain", "10a", "10a"):
        return False
    if not feito(e, "S6b_aplicar"):
        rc = run([PY, "-B", "-X", "utf8", str(B3 / "evento_c1_b3_v410.py")], B3, ORQ / "evento_c1_out.txt", 600)
        txt = (ORQ / "evento_c1_out.txt").read_text(encoding="utf-8", errors="replace")
        m = re.search(r'"evento":\s*(\d+).*?"hash":\s*"([0-9a-f]+)"', txt[-2000:], re.S)
        if rc != 0 or not m:
            marcar(e, "S6b_aplicar", False, rc=rc, motivo="evento c1 sem seq/hash legíveis"); return False
        envv = {"B3_AUTORIZADO": "sim", "EVENTO": m.group(1), "EVENTO_HASH": m.group(2), "V410_AUTORIZACAO_OPERADOR": AUT}
        if not chain(e, "S6b_chain", "10b", "10b", env=envv):
            marcar(e, "S6b_aplicar", False, evento=m.group(1)); return False
        marcar(e, "S6b_aplicar", True, evento=m.group(1), hash=m.group(2))
    if not feito(e, "S6c_religamento"):
        rp = jload(B3 / "RECIBO_PARADA_v410.json") if (B3 / "RECIBO_PARADA_v410.json").exists() else {}
        comando = rp.get("religar") or rp.get("comando") or r'"C:\Python314\pythonw.exe" -X utf8 C:\IALD\Bancada_Um\um_bancada.py'
        log("S6c: religando o serviço da Bancada pelo comando do recibo: %s" % comando)
        ps("Start-Process -FilePath 'C:\\Python314\\pythonw.exe' -ArgumentList '-X','utf8','C:\\IALD\\Bancada_Um\\um_bancada.py' -WorkingDirectory 'C:\\IALD\\Bancada_Um' -WindowStyle Hidden")
        for _ in range(60):
            if porta_aberta(18777):
                break
            time.sleep(3)
        rc = run([PY, "-B", "-X", "utf8", str(B3 / "recibo_religamento_v410.py")], B3, ORQ / "recibo_religamento_out.txt", 600, env={"V410_AUTORIZACAO_OPERADOR": AUT})
        ok = rc == 0 and (B3 / "RECIBO_RELIGAMENTO_v410.json").exists() and porta_aberta(18777)
        marcar(e, "S6c_religamento", ok, rc=rc, porta=porta_aberta(18777))
        if not ok:
            return False
    if not chain(e, "S6c_chain_10c_14", "10c", "14"):
        return False
    return s6d_textos_custodia(e)


def s6d_textos_custodia(e):
    """S6d (D52, D57): os sete textos da custódia entram ENCADEADOS, depois da chain 14: pos_rito/textos_custodia_handoff_v410.py (rc 0 e o recibo RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json ao lado); DEPOIS, o portão do G1 (custodia_g1.textos.portao)
    e a D59 sobre o HANDOFF INTEIRO (Nós\\HANDOFF_v410_CUSTODIA.md e memory\\handoff-v410-custodia.md; os hashes conhecidos são os do próprio texto). O handoff é o FIM da cadeia desta versão (sem S7 e sem S10)."""
    if feito(e, "S6d_textos_custodia"):
        return True
    cands = sorted(p for p in (PK / "pos_rito").glob("textos_custodia_handoff_v410*.py") if p.suffix == ".py")   # (MEDIO 2 da revisao R1, 05/11: o arquivo real e' textos_custodia_handoff_v410.py, sem sufixo; os .bak_... nao terminam em .py)
    if len(cands) != 1:
        marcar(e, "S6d_textos_custodia", False, motivo="esperava UM pos_rito/textos_custodia_handoff_v410*.py (sufixo .py)", achados=[c.name for c in cands]); return False
    rc = run([PY, "-B", "-X", "utf8", str(cands[0])], PK / "pos_rito", ORQ / "textos_custodia_out.txt", 1800)
    rec = PK / "pos_rito" / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json"
    ok = rc == 0 and rec.exists()
    if not ok:
        marcar(e, "S6d_textos_custodia", False, rc=rc, script=cands[0].name, recibo=(rec.name if rec.exists() else None)); return False
    viol = {}
    try:
        sys.path.insert(0, str(CEN / "tools"))
        from custodia_g1 import textos as _TXG1   # o portão do G1 (a mesma função que a custódia usa)
        for hp in (NOS / "HANDOFF_v410_CUSTODIA.md", UMEM / "handoff-v410-custodia.md"):
            if not hp.exists():
                viol[hp.name] = ["o handoff não existe"]; continue
            ht = hp.read_text(encoding="utf-8")
            conh = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", ht)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", ht))
            v_ = list(_TXG1.portao(ht, conh, rotulo=hp.name))
            if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", ht) or (re.search(r"(?i)kimi", ht) and not re.search(r"(?i)h0dn", ht)):   # (09/11, D72 e D77(g): a mesma regra de pos_rito\\registrar_mapa_v410.d59_viola -- o nome do executor so' no contexto do H0DN; o resto do que a D59 deixa fora segue vetado em qualquer texto)
                v_.append("D59: o handoff traz o que fica fora dos textos")
            if any(x_.lower() in ht.lower() for x_ in _DL.FORA_D65):   # (v410) D65: o que a fala do nome do algoritmo deixa fora nao entra no handoff
                v_.append("D65: o handoff traz o que fica fora dos textos")
            if v_:
                viol[hp.name] = v_[:5]
    except Exception:  # noqa: BLE001
        viol["erro"] = [traceback.format_exc()[-600:]]
    ok = not viol
    marcar(e, "S6d_textos_custodia", ok, rc=rc, script=cands[0].name, recibo=rec.name, portao_g1_handoff_inteiro=(viol or "limpo"), fim_da_cadeia="HANDOFF (D57)")
    if ok:
        log("S6d: o handoff passou no portão do G1, na D59 e na D65; FIM DA CADEIA (D68a): a custódia completa e o release do app são da sessão de custódia")
    return ok


def s7_g1(e):
    if feito(e, "S7_g1"):
        return True
    base = [PY, "-X", "utf8", str(CEN / "tools" / "custodiar.py")]
    comum = ["--versao", "v410", "--ator", ATOR, "--coautor", COAUTOR, "--ordem", str(ORDEM)]
    rc1 = run(base + ["planejar"] + comum + ["--seco"], CEN, ORQ / "g1_planejar_out.txt", 1800)
    if rc1 not in (0, 1, 5):   # 1 = pendente: pronto para custodiar (tabela de custodiar.py)
        marcar(e, "S7_g1", False, etapa="planejar", rc=rc1); return False
    rc2 = run(base + ["executar"] + comum + ["--publicar"], CEN, ORQ / "g1_executar_out.txt", 4 * 3600)
    rc3 = run(base + ["auditar"] + comum, CEN, ORQ / "g1_auditar_out.txt", 1800)
    ok = rc2 in (0, 5) and rc3 in (0, 5)
    marcar(e, "S7_g1", ok, planejar=rc1, executar=rc2, auditar=rc3, nota="5 = só decisões do operador")
    return ok


UMEM = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory")   # o handoff da memória (o fechar o grava; o S6d o passa pelo portão)
TUNEL_APP = Path(r"C:\IALD\TUNEL_CLAUDE_APP")        # a pasta de ordens do orquestrador app (o app Claude em modo work)
APP = Path(r"C:\IALD\projetos_pyhton\IALD")            # o app/web server da IALD: iald_nucleo_fixo.json diz a release instalada (C21 só CONFERE)
TEMPLATE_ORDEM = ORQ / "ORDEM_RELEASE_APP_TEMPLATE.md"
ESPERA_APP_S = 24 * 3600                                 # sem recibo em 24 h: parada visível (nunca «ok»)
SONDA_APP_S = 300


def _git_head(repo):
    """HEAD curto do repositório local (só leitura); 'indisponivel' se o git falhar: o texto da ordem diz o que leu."""
    try:
        r = subprocess.run(["git", "-C", str(repo), "rev-parse", "--short=8", "HEAD"], capture_output=True, text=True, timeout=60)
        return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else "indisponivel"
    except Exception:  # noqa: BLE001
        return "indisponivel"


def _proximo_num_ordem(tunel):
    nums = [int(m.group(1)) for p in Path(tunel).glob("ORDEM_*.md") for m in [re.match(r"ORDEM_(\d+)_", p.name)] if m]
    return (max(nums) + 1) if nums else 1


def _pasta_release_anterior(vant, work=None):
    work = Path(work) if work else CEN / "work"
    n_ant = int(vant[1:])
    c = sorted(work.glob("iald_%s_*" % vant)) or sorted(p for p in work.glob("iald_v*_*") if re.match(r"iald_v(\d+)_", p.name) and int(re.match(r"iald_v(\d+)_", p.name).group(1)) <= n_ant)   # a mais recente NAO posterior a anterior (nunca a propria release que o app vai construir)
    return c[-1] if c else None


def renderizar_ordem(num, selo, work=None, hoje=None, commit_espelho=None, commit_central=None):
    """A ORDEM de release do app, a partir do molde, com a versão e o pino LIDOS do selo (nunca digitados). Devolve o texto; recusa se sobrar placeholder."""
    vn = selo["um_version"]
    assert re.fullmatch(r"v\d{3,}", vn), vn
    pin = selo["sha256"]["um.py"]
    assert re.fullmatch(r"[0-9a-f]{64}", pin), pin
    vant = "v%d" % (int(vn[1:]) - 1)
    pa = _pasta_release_anterior(vant, work)
    tpl = TEMPLATE_ORDEM.read_text(encoding="utf-8")
    vals = {"NUM": "%03d" % num, "VN": vn, "VANT": vant, "PIN": pin, "PIN16": pin[:16], "DATA": hoje or dt.date.today().strftime("%d/%m/%Y"),
            "SHA16_ORDEM": sha16(ORDEM), "COMMIT_ESPELHO": commit_espelho or _git_head(Path(r"C:\IALD\Artigo\the_boundary")), "COMMIT_CENTRAL": commit_central or _git_head(CEN),
            "PASTA_ANTERIOR": ("`%s`" % pa) if pa else "(nenhuma pasta iald_v4xx encontrada; peça à gerência)"}
    for k, v in vals.items():
        tpl = tpl.replace("{{%s}}" % k, v)
    assert "{{" not in tpl, "placeholder sem valor na ordem de release do app"
    return tpl


def recibo_do_app(ordem_path, num, vn, pin, app=None, work=None, tunel=None):
    """O RECIBO do app, conferido NA FONTE (devolve (ok, dict)). Quatro elos, todos exigidos: (a) RELATORIO_*.md na pasta de ordens, escrito DEPOIS da ordem e citando ORDEM_<num>, OU (R4, 03/11) RESULTADOS\\NNN_RESULTADO.json desta ordem, posterior a ela, com estado cumprida (a forma do CANAL_DESASSISTIDO.md); (b) INSTALLED_VERIFICATION.json de work\\iald_<vn>_*,
    depois da ordem, status PASS, identity.release == vn e source_sha256 == o pino; (c) o contrato jev_control_<vn>.json existe no caminho que o app declara e o sha256 do arquivo é o que o app declara; (d) iald_nucleo_fixo.json do app:
    operational_core.current_release == vn e release_source_sha256 == o pino; jev_control.release == vn e source_sha256 == o pino. Nada é aceito pela palavra do relatório."""
    app = Path(app) if app else APP; work = Path(work) if work else CEN / "work"; tunel = Path(tunel) if tunel else TUNEL_APP
    t0 = Path(ordem_path).stat().st_mtime
    d = {"relatorio": None, "installed_verification": None, "jev_control": None, "nucleo_fixo": None}
    rel_ok = []
    for p in tunel.glob("RELATORIO_*.md"):
        if p.stat().st_mtime > t0 and re.search(r"ORDEM[_ ]?0*%d(?![0-9])" % num, p.read_text(encoding="utf-8", errors="replace")):
            rel_ok.append(p.name)
    # [R4, 03/11] a forma duravel do CANAL_DESASSISTIDO.md (gerente do LAR, 03/11): RESULTADOS\NNN_RESULTADO.json desta ordem, posterior a ela, com estado cumprida, vale como o elo (a); parcial/recusada/incerta NAO valem
    rdir = tunel / "RESULTADOS"
    for p in (rdir.glob("*_RESULTADO.json") if rdir.is_dir() else []):
        try:
            rj = jload(p)
        except Exception:  # noqa: BLE001
            continue
        if not isinstance(rj, dict):   # [R5, 03/11] JSON valido que NAO e' objeto (lista, string): nao e' resultado; nunca derruba a espera
            continue
        _ord = str(rj.get("ordem", "") or "").strip()
        desta = bool(re.search(r"ORDEM[_ ]?0*%d(?![0-9])" % num, _ord)) if _ord else bool(re.match(r"0*%d_RESULTADO\.json$" % num, p.name))   # [R5] com o campo ordem, ele manda; o nome so' vale sem o campo
        if p.stat().st_mtime > t0 and desta and str(rj.get("estado", "")).strip().lower() == "cumprida":
            rel_ok.append("RESULTADOS/" + p.name)
    d["relatorio"] = rel_ok or None
    iv_ok = False
    ivs = sorted(work.glob("iald_%s_*/INSTALLED_VERIFICATION.json" % vn), key=lambda p: p.stat().st_mtime)
    if ivs and ivs[-1].stat().st_mtime > t0:
        try:
            iv = jload(ivs[-1]); ident = iv.get("identity") or {}
            iv_ok = iv.get("status") == "PASS" and ident.get("release") == vn and str(ident.get("source_sha256", "")).startswith(pin[:16]) and (len(str(ident.get("source_sha256", ""))) < 64 or ident.get("source_sha256") == pin)
            d["installed_verification"] = {"path": str(ivs[-1]), "status": iv.get("status"), "release": ident.get("release"), "ok": iv_ok}
        except Exception as ex:  # noqa: BLE001
            d["installed_verification"] = {"erro": str(ex)[:200]}
    nuc_ok = False; jc_ok = False
    try:
        nuc = jload(app / "iald_nucleo_fixo.json"); oc = nuc.get("operational_core") or {}; jc = nuc.get("jev_control") or {}
        nuc_ok = oc.get("current_release") == vn and oc.get("release_source_sha256") == pin and jc.get("release") == vn and jc.get("source_sha256") == pin
        jp = Path(str(jc.get("path", "")))
        import hashlib
        jc_ok = bool(jp.name == "jev_control_%s.json" % vn and jp.exists() and hashlib.sha256(jp.read_bytes()).hexdigest() == jc.get("sha256"))
        d["nucleo_fixo"] = {"current_release": oc.get("current_release"), "release_source_sha256_ok": oc.get("release_source_sha256") == pin, "jev_release": jc.get("release"), "ok": nuc_ok}
        d["jev_control"] = {"path": str(jp), "existe": jp.exists(), "sha256_confere": jc_ok}
    except Exception as ex:  # noqa: BLE001
        d["nucleo_fixo"] = {"erro": str(ex)[:200]}
    ok = bool(rel_ok) and iv_ok and nuc_ok and jc_ok
    d["ok"] = ok
    return ok, d


def s10_app(e):
    """S10 (herdado da v409; o template desta pasta traz a janela P2 do shared por D53): escreve a ORDEM de release do app e do contrato JEV em TUNEL_CLAUDE_APP (versão e pino LIDOS do selo) e ESPERA o recibo conferido na fonte (até 24 h; depois, PARADA visível), e só então confere na G1 que o C21 fechou.
    Vai depois da publicação (S7), para que o app leia o commit do espelho; o C21 da custódia só CONFERE o que o app fez (a G1 nunca constrói a perna do app)."""
    if feito(e, "S10_app"):
        return True
    try:
        selo = jload(NOS / "um_absoluto_selo.json")
        vn = selo["um_version"]; pin = selo["sha256"]["um.py"]
        assert vn == "v410", ("o selo do Nós não é a v410", vn)
        st = e.setdefault("s10", {})
        if not st.get("ordem"):
            num = _proximo_num_ordem(TUNEL_APP)
            nome = "ORDEM_%03d_release_%s_do_app.md" % (num, vn)
            destino = TUNEL_APP / nome
            assert not destino.exists(), ("a ordem de release já existe e não foi escrita por esta corrida", nome)
            texto = renderizar_ordem(num, selo)
            destino.write_text(texto, encoding="utf-8", newline="\n")
            st.update(ordem=nome, num=num, escrita_em=dt.datetime.now().isoformat(timespec="seconds"), ordem_sha16=sha16(destino), espera_ate=(dt.datetime.now() + dt.timedelta(seconds=ESPERA_APP_S)).isoformat(timespec="seconds"))
            gravar(e)
            log("S10: ordem de release do app escrita: %s (sha16 %s); espero o recibo até %s" % (nome, st["ordem_sha16"], st["espera_ate"]))
        ordem = TUNEL_APP / st["ordem"]
        t0 = dt.datetime.fromisoformat(st["escrita_em"]); voltas = 0
        while True:
            if parar_pedido():
                log("PARAR pedido — saio da espera do app sem marcar ok"); return False
            ok, d = recibo_do_app(ordem, st["num"], vn, pin)
            if ok:
                break
            if (dt.datetime.now() - t0).total_seconds() > ESPERA_APP_S:
                marcar(e, "S10_app", False, motivo="sem recibo do app conferido na fonte em 24 h; PARADA visível: a gerência decide (nada foi marcado ok)", ordem=st["ordem"], ultimo_estado=d); return False
            voltas += 1
            if voltas % 6 == 1:
                log("S10: aguardando o recibo do app (%s): %s" % (st["ordem"], json.dumps(d, ensure_ascii=False)[:300]))
            time.sleep(SONDA_APP_S)
        base = [PY, "-X", "utf8", str(CEN / "tools" / "custodiar.py")]
        comum = ["--versao", vn, "--ator", ATOR, "--coautor", COAUTOR, "--ordem", str(ORDEM)]
        rc = run(base + ["planejar"] + comum + ["--seco"], CEN, ORQ / "g1_c21_out.txt", 1800)
        txt = (ORQ / "g1_c21_out.txt").read_text(encoding="utf-8", errors="replace")
        m = re.search(r"(?m)^\s+C21\s+(ok|sup|rel)\b", txt)
        marcar(e, "S10_app", bool(m), recibo=d, c21_na_g1=(m.group(1) if m else "NAO_APLICADO"), planejar_rc=rc, ordem=st["ordem"])
        return bool(m)
    except Exception:  # noqa: BLE001
        marcar(e, "S10_app", False, erro=traceback.format_exc()[-600:]); return False


def _ensaio_s10():
    """ENSAIO a seco do S10 (não toca TUNEL_CLAUDE_APP, o app, o Nós nem o estado): renderiza a ordem com um selo SINTÉTICO derivado do CANDIDATO, e exercita recibo_do_app contra um app sintético (um caso positivo e seis controles negativos)."""
    import hashlib, shutil
    out = ORQ / "ensaio_s10"
    if out.exists():
        shutil.rmtree(out)
    (out / "tunel").mkdir(parents=True); (out / "app").mkdir(); (out / "work" / "iald_v410_ens").mkdir(parents=True)
    cand = jload(PK / "CANDIDATO_v410.json"); pin = cand["sha256"]; assert len(pin) == 64
    selo = {"um_version": "v410", "sha256": {"um.py": pin}}
    (out / "tunel" / "ORDEM_001_x.md").write_text("x", encoding="utf-8")
    num = _proximo_num_ordem(out / "tunel"); assert num == 2
    texto = renderizar_ordem(num, selo, work=out / "work", commit_espelho="ESPELHO00", commit_central="CENTRAL00")
    ordem = out / "tunel" / ("ORDEM_%03d_release_v410_do_app.md" % num); ordem.write_text(texto, encoding="utf-8", newline="\n")
    assert pin in texto and "v410" in texto and "{{" not in texto
    time.sleep(1.1)
    jv = out / "app" / "jev_control_v410.json"; jv.write_text("{}", encoding="utf-8")
    def montar(release="v410", srcsha=pin, status="PASS", jev_sha=None, relatorio=True, jev_nome=True, resultado=None, resultado_json=None):
        for p in (out / "tunel").glob("RELATORIO_*.md"):
            p.unlink()
        rdir = out / "tunel" / "RESULTADOS"   # [R4] a forma duravel do canal: so' quando o caso pede
        for p in (rdir.glob("*_RESULTADO.json") if rdir.is_dir() else []):
            p.unlink()
        if resultado:
            rdir.mkdir(exist_ok=True); (rdir / ("%03d_RESULTADO.json" % num)).write_text(json.dumps({"ordem": "ORDEM_%03d" % num, "estado": resultado, "arquivos": []}), encoding="utf-8")
        if resultado_json is not None:   # [R5] o texto bruto do RESULTADO desta ordem (casos malformados)
            rdir.mkdir(exist_ok=True); (rdir / ("%03d_RESULTADO.json" % num)).write_text(resultado_json, encoding="utf-8")
        if relatorio:
            (out / "tunel" / "RELATORIO_20261103.md").write_text("relatorio da ORDEM_%03d" % num, encoding="utf-8")
        (out / "work" / "iald_v410_ens" / "INSTALLED_VERIFICATION.json").write_text(json.dumps({"status": status, "identity": {"release": release, "source_sha256": srcsha}}), encoding="utf-8")
        jp = jv if jev_nome else out / "app" / "outro.json"
        jp.write_text("{}", encoding="utf-8")
        (out / "app" / "iald_nucleo_fixo.json").write_text(json.dumps({"operational_core": {"current_release": release, "release_source_sha256": srcsha}, "jev_control": {"release": release, "source_sha256": srcsha, "path": str(jp), "sha256": jev_sha or hashlib.sha256(jp.read_bytes()).hexdigest()}}), encoding="utf-8")
    res = {}
    montar(); ok, d = recibo_do_app(ordem, num, "v410", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["positivo"] = ok
    montar(relatorio=False, resultado="cumprida"); okr, _ = recibo_do_app(ordem, num, "v410", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["positivo_resultado_json"] = okr   # [R4] so' o JSON do canal, sem RELATORIO
    montar(relatorio=False, resultado="parcial"); okn, _ = recibo_do_app(ordem, num, "v410", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_resultado_parcial"] = (okn is False)
    montar(relatorio=False, resultado_json=json.dumps(["cumprida"])); okn, _ = recibo_do_app(ordem, num, "v410", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_resultado_nao_objeto"] = (okn is False)   # [R5] JSON valido que nao e' objeto: ignorado, sem excecao
    montar(relatorio=False, resultado_json=json.dumps({"ordem": "ORDEM_%03d" % (num + 18), "estado": "cumprida"})); okn, _ = recibo_do_app(ordem, num, "v410", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_resultado_ordem_divergente"] = (okn is False)   # [R5] o nome e' desta ordem, o campo diz outra: o campo manda
    for nome, kw in (("release_errada", dict(release="v405")), ("pino_errado", dict(srcsha="0" * 64)), ("verificacao_falhou", dict(status="FAIL")), ("sha_do_contrato_errado", dict(jev_sha="0" * 64)), ("sem_relatorio", dict(relatorio=False)), ("contrato_com_outro_nome", dict(jev_nome=False))):
        montar(**kw); okn, _ = recibo_do_app(ordem, num, "v410", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_" + nome] = (okn is False)
    montar(); os.utime(out / "tunel" / "RELATORIO_20261103.md", (ordem.stat().st_mtime - 100, ordem.stat().st_mtime - 100))
    okn, _ = recibo_do_app(ordem, num, "v410", pin, app=out / "app", work=out / "work", tunel=out / "tunel"); res["negativo_relatorio_anterior_a_ordem"] = (okn is False)
    res["ordem_renderizada"] = {"bytes": len(texto.encode("utf-8")), "sha16": sha16(ordem), "pino_no_texto": pin in texto, "caminho": str(ordem)}
    res["ok"] = res["positivo"] is True and res["positivo_resultado_json"] is True and all(v is True for k, v in res.items() if k.startswith("negativo_"))
    (ORQ / "ENSAIO_S10_v410.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return res["ok"]


def _plano():
    """O PLANO (só leitura): os passos na ordem, o estado de cada um no ESTADO.json e o que cada um exige; não age."""
    e = carregar()
    passos = list(PASSOS_ANTES_DO_GATILHO) + ["S9_gatilho_custodia"]   # (D57: sem S7_g1 e sem S10_app nesta versao)
    print("PLANO do orquestrador pos_treino_v410 (nada é executado); ordem do operador: %s (sha16 %s, conferido contra o arquivo); tempos lidos (build, Audit, rito v409): %s" % (ORDEM.name, _conferir_ordem(), _tempos_lidos()))
    for p in passos:
        print("  %-20s %s" % (p, "feito" if feito(e, p) else "pendente"))
    pr = PK / "PREPARACAO_v410_PRONTA.json"; rv = REV
    print("PREPARACAO_v410_PRONTA.json:", ("pronta=%s" % jload(pr).get("pronta")) if pr.exists() else "ausente")
    print("REVISAO_TERCEIRO_v410.json:", ("aprovada=%s candidato=%s" % (jload(rv).get("aprovada"), jload(rv).get("candidato_sha16"))) if rv.exists() else "ausente")
    faltam = [str(x) for x in (ORDEM, PK / "instalar_v410.py", PK / "rito_v410.sh", PK / "pos_rito" / "chain_pos_rito_v410.sh", PK / "bancada_B3_servico" / "recibo_parada_v410.py", PK / "bancada_B3_servico" / "recibo_religamento_v410.py", PK / "bancada_B3_servico" / "evento_c1_b3_v410.py", PK / "um_v410_candidato.py", PK / "ESPERADOS_v410.json") if not Path(x).exists()]
    if len([p for p in (PK / "pos_rito").glob("textos_custodia_handoff_v410*.py") if p.suffix == ".py"]) != 1:   # (MEDIO 2 da revisao R1, 05/11: o mesmo glob do S6d)
        faltam.append(str(PK / "pos_rito" / "textos_custodia_handoff_v410*.py") + " (S6d, D52: exatamente um, sufixo .py)")
    faltam += [str(x) for x in (ORDEM_PUBLICACAO, DIVISAO_0411) if not Path(x).exists()]   # (ADITIVO 1) as falas que o gatilho da custodia cita
    print("gatilho da custodia (S9_gatilho_custodia):", ("JA EXISTE: %s" % GATILHO) if GATILHO.exists() else "ainda nao escrito (so' sai com tudo feito, o HANDOFF com os sete marcadores e os dois blocos do README, e o portao do G1 limpo no S6d)")
    print("arquivos que o orquestrador usa e NÃO existem:", faltam or "nenhum")
    return not faltam


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


# ---------------------------------------------------------------- S9_gatilho_custodia (ADITIVO 1 a ordem do conserto unico, gerencia c1, 10/11/2026: a custodia da v410 e' AUTOMATICA, por ordem do operador a sessao de custodia)
PASSOS_ANTES_DO_GATILHO = ("S0_treino", "S1_prep", "S1b_revisao", "S2_prevoo", "S3_instalar", "S4_rito", "S5_cadeia_0_10", "S6a_parada", "S6a_chain", "S6b_aplicar", "S6c_religamento", "S6c_chain_10c_14", "S6d_textos_custodia", "S8_nativa")   # (D57: sem S7_g1 e sem S10_app nesta versao)
GATILHO = PK / "ORDEM_HANDOFF_CUSTODIA_v410.md"   # o arquivo-gatilho que a sessao de custodia espera
ORDEM_PUBLICACAO = CEN / "work" / "cunhagens_13out" / "OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt"   # a ORDEM DE PUBLICACAO da v410 (o caminho do --ordem; o sha16 e' LIDO do arquivo)
TRECHO_PUBLICACAO = "quando isso acontecer quero que vc atualize tudo e publique tudo"   # (verbatim: conferido contra o arquivo antes de escrever)
DIVISAO_0411 = CEN / "work" / "cunhagens_13out" / "OPERADOR_04nov_custodia_e_da_sessao_de_custodia_c1_so_um_py_verbatim.txt"   # a divisao de 04/11 (como na v409)
MARCADORES_README = ("README_FRENTE", "README_O_QUE_SAI")   # os dois blocos do README que o gerador do handoff poe na secao «README: o que fica evidente» (ADITIVO 1)


def _gatilho_ler(e, nos, pk, cen_g1):
    """Le TUDO o que o gatilho cita (so' leitura) e junta os MOTIVOS pelos quais ele nao pode ser escrito (lista vazia = pode). Nenhum valor e' digitado: o selo, o um.py, o core, o ESPERADOS, o stdout do rito, os horarios,
    o ESTADO, o HANDOFF (pelo parser do proprio G1), o recibo dos textos, a revisao de terceiro e as falas do operador sao lidos dos arquivos."""
    import hashlib
    import types
    motivos = []; d = {}
    p = e.get("passos", {})
    faltam = [k for k in PASSOS_ANTES_DO_GATILHO if p.get(k, {}).get("ok") is not True]
    if faltam:
        motivos.append("passo anterior nao feito ou falso: " + ", ".join(faltam))
    s6d = p.get("S6d_textos_custodia", {})
    if s6d.get("portao_g1_handoff_inteiro") != "limpo":
        motivos.append("o portao do G1 nao rodou limpo no S6d: %r" % (s6d.get("portao_g1_handoff_inteiro"),))
    s6b = p.get("S6b_aplicar", {}); d["evento"], d["evento_hash"] = s6b.get("evento"), s6b.get("hash")
    if not (d["evento"] and d["evento_hash"]):
        motivos.append("o evento c1 do B(n) (S6b) nao tem seq e hash legiveis no ESTADO")
    # ---- o selo, o um.py, o core e o ESPERADOS
    pin = None
    try:
        selo = jload(nos / "um_absoluto_selo.json"); umb = (nos / "um.py").read_bytes(); pin = hashlib.sha256(umb).hexdigest()[:16]
        esp = jload(pk / "ESPERADOS_v410.json"); core = jload(nos / "um_absoluto.json")["core"]
        lad = core.get("external_ladder") or {}; gate = ((core.get("qg_closure") or {}).get("gate") or {}).get("verdict")
        d.update(selo_ts=selo.get("timestamp"), selftest=selo.get("fail_closed_selftest"), pin=pin, um_bytes=len(umb), escada=[lad.get("n_theorems_clean"), lad.get("n_theorems_expected")], gate=gate)
        if selo.get("um_version") != "v410":
            motivos.append("o selo do Nos nao e' o da v410: %r" % (selo.get("um_version"),))
        if not (selo.get("sha256", {}).get("um.py", "")[:16] == pin == esp.get("candidato_sha16")):
            motivos.append("o um.py do Nos, o pino do selo e o candidato de ESPERADOS nao sao o mesmo")
        if selo.get("fail_closed_selftest") != "FAIL_CLOSED_SELFTEST_PASSED" or not selo.get("timestamp"):
            motivos.append("o selo nao traz FAIL_CLOSED_SELFTEST_PASSED (ou nao traz o timestamp)")
        if not (type(lad.get("n_theorems_clean")) is int and lad.get("n_theorems_clean") == lad.get("n_theorems_expected") == (esp.get("escada") or [None, None])[1]):
            motivos.append("a escada do core nao e' exata ou nao e' a de ESPERADOS: %r" % (d["escada"],))
        if not (isinstance(gate, str) and gate and gate == selo.get("qg_closure_verdict") == esp.get("qg_closure_gate_verdict_v409")):
            motivos.append("o veredito do gate (core, selo, ESPERADOS) nao e' o mesmo: o gate nao pode ter se movido")
    except Exception:  # noqa: BLE001
        motivos.append("selo, um.py, core ou ESPERADOS ilegiveis: " + traceback.format_exc()[-300:])
    # ---- o trailer do rito e os horarios
    try:
        linhas = (nos / "rodada_v410_stdout.txt").read_text(encoding="utf-8", errors="replace").rstrip().splitlines()
        d["trailer"] = next((l for l in reversed(linhas[-5:]) if l.startswith("RITO_RC=")), "")
    except Exception:  # noqa: BLE001
        d["trailer"] = ""
    if not (d["trailer"] == "RITO_RC=0" == p.get("S4_rito", {}).get("trailer")):
        motivos.append("o trailer do rito (stdout do Nos e S4) nao e' RITO_RC=0: %r" % (d["trailer"],))
    try:
        d["rito_h0"], d["rito_h1"] = (pk / "rito_horarios_v410.txt").read_text(encoding="utf-8").split()[:2]
        assert re.fullmatch(r"\d\d:\d\d:\d\d", d["rito_h0"]) and re.fullmatch(r"\d\d:\d\d:\d\d", d["rito_h1"])
    except Exception:  # noqa: BLE001
        motivos.append("os horarios do rito (rito_horarios_v410.txt) nao foram lidos")
    # ---- o HANDOFF no Nos, pelo parser do proprio G1: os sete marcadores, a secao README e os dois blocos do README
    corpos = {}
    try:
        sys.path.insert(0, str(CEN / "tools"))
        from custodia_g1 import nos as _NOSG1, textos as _TXG1   # o parser e o portao do G1 (os mesmos que a custodia usa)
        hp = nos / "HANDOFF_v410_CUSTODIA.md"
        if not hp.is_file():
            motivos.append("o HANDOFF nao existe no Nos")
        else:
            hb = hp.read_bytes(); d.update(handoff_bytes=len(hb), handoff_sha16=hashlib.sha256(hb).hexdigest()[:16])
            h = _NOSG1.ler_handoff(types.SimpleNamespace(NOS=nos, CEN=cen_g1), "v410"); corpos = dict(h.corpos)
            if h.problemas:
                motivos.append("o HANDOFF tem marcador com problema: %r" % (h.problemas[:3],))
            sem = ["%s_v410" % i for i in tuple(_TXG1.MARCADORES_OPCIONAIS) + MARCADORES_README if not corpos.get("%s_v410" % i, "").strip()]
            if len(_TXG1.MARCADORES_OPCIONAIS) != 7 or sem:
                motivos.append("o HANDOFF nao traz os sete marcadores e os dois blocos do README: faltam %s" % sem)
            i0 = h.texto.find("**README: o que fica evidente**"); i1 = h.texto.find("<!-- INICIO_README_FRENTE_v410 -->"); i2 = h.texto.find("<!-- INICIO_README_O_QUE_SAI_v410 -->")
            if not (0 <= i0 < i1 < i2):
                motivos.append("a secao «README: o que fica evidente» nao esta' no HANDOFF, ou os dois blocos do README nao vem depois dela, nesta ordem")
            o = h.o_que_e
            if not (o and o.versao == "v410" and o.pin16 == pin and o.rc0 and o.selftest_passou and o.gate_intocado and o.completa and o.escada == "%s/%s" % tuple(d.get("escada") or ("?", "?"))):
                motivos.append("o paragrafo «O que e'» do HANDOFF nao e' o desta versao (versao, pino, escada, COMPLETA, rc 0, selftest, gate intocado)")
    except Exception:  # noqa: BLE001
        motivos.append("o HANDOFF nao foi lido pelo parser do G1: " + traceback.format_exc()[-300:])
    # ---- o recibo dos textos (S6d): o HANDOFF nao mudou depois do portao; os dois blocos do README sao os do recibo e passaram nas guardas e no portao do G1
    try:
        rp = pk / "pos_rito" / "RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json"; rec = jload(rp); d["recibo_sha16"] = sha16(rp)
        rf = corpos.get("README_FRENTE_v410", "").strip("\n"); rs = corpos.get("README_O_QUE_SAI_v410", "").strip("\n")
        d.update(rf_bytes=len(rf.encode("utf-8")), arco_pt=str((rec.get("textos") or {}).get("ARCO_PT") or ""))
        if rec.get("sha16_depois") != d.get("handoff_sha16"):
            motivos.append("o HANDOFF do Nos nao e' o que o S6d gravou e passou pelo portao (sha16 do recibo != o de agora)")
        if not (rf and rf == rec.get("readme_frente") and rec.get("readme_frente_bytes_utf8") == d["rf_bytes"] and rs and rs == rec.get("readme_o_que_sai")):
            motivos.append("os dois blocos do README no HANDOFF nao sao os do recibo do S6d (texto ou bytes)")
        g = rec.get("guardas") or {}
        if not all(isinstance(g.get(i), dict) and g[i].get("guarda_frases_v410") == [] and g[i].get("portao_g1") == [] and g[i].get("forma") == [] for i in MARCADORES_README):
            motivos.append("o recibo do S6d nao mostra os dois blocos do README limpos nas guardas e no portao do G1")
        if not (d["arco_pt"] and d["arco_pt"] == corpos.get("ARCO_PT_v410", "").strip("\n")):
            motivos.append("o texto ARCO_PT do recibo nao e' o do HANDOFF")
    except Exception:  # noqa: BLE001
        motivos.append("o recibo dos textos da custodia (S6d) nao foi lido: " + traceback.format_exc()[-300:])
    # ---- a revisao de terceiro
    try:
        rvp = pk / "revisao_terceiro" / "REVISAO_TERCEIRO_v410.json"; rv = jload(rvp)
        sev = {}
        for a_ in (rv.get("achados") or []):
            if isinstance(a_, dict) and a_.get("sev"):
                sev[str(a_["sev"])] = sev.get(str(a_["sev"]), 0) + 1
        d.update(rev_sha16=sha16(rvp), rev_revisor=str(rv.get("revisor") or "n/d"), rev_sev=sev)
        if not (rv.get("aprovada") is True and rv.get("candidato_sha16") == pin):
            motivos.append("a revisao de terceiro nao esta' aprovada sobre este candidato")
    except Exception:  # noqa: BLE001
        motivos.append("a revisao de terceiro nao foi lida: " + traceback.format_exc()[-300:])
    # ---- as falas do operador: a ordem desta versao, a ORDEM DE PUBLICACAO e a divisao de 04/11
    try:
        d["ordem_sha16"] = _conferir_ordem()
        d["pub_sha16"] = sha16(ORDEM_PUBLICACAO); d["div_sha16"] = sha16(DIVISAO_0411)
        if TRECHO_PUBLICACAO not in ORDEM_PUBLICACAO.read_text(encoding="utf-8"):
            motivos.append("o trecho citado da ORDEM DE PUBLICACAO nao esta' no arquivo da fala")
    except Exception:  # noqa: BLE001
        motivos.append("as falas do operador (a ordem, a ORDEM DE PUBLICACAO, a divisao de 04/11) nao foram lidas: " + traceback.format_exc()[-300:])
    d["n_autoria"] = len(_DL.NOMES_DECLARADOS_PELA_AUTORIA_AESCALA)
    return d, motivos


def _gatilho_render(d):
    """O texto do gatilho, pelo molde da v409 (work/cadeia_de_selo/v409/ORDEM_HANDOFF_CUSTODIA_v409.md: as mesmas secoes); todo valor vem de `d` (lido por _gatilho_ler)."""
    hoje = dt.date.today(); sev = d.get("rev_sev") or {}
    rev_n = (" (" + ", ".join("%d %s" % (sev[k], k) for k in sorted(sev)) + ")") if sev else ""
    L = ["# ORDEM DE HANDOFF DA GERÊNCIA c1 À SESSÃO DE CUSTÓDIA — v410 SELADA (%s)" % hoje.strftime("%d/%m/%Y"), "",
         "> Para a sessão de custódia (o papel que fez a custódia da v409 pelo G1). Escrita pelo orquestrador da v410 (passo S9_gatilho_custodia), por ordem da gerência c1: a custódia desta versão é automática, por ordem do operador de 10/11/2026, "
         "e este arquivo é o gatilho que a sessão de custódia espera. Ele só é escrito com todos os passos anteriores feitos, o HANDOFF no Nós com os sete marcadores e os dois blocos do README, e o portão do G1 limpo no S6d. "
         "Vale a regra de custodiar sempre que o handoff aparecer: as três marcas estão no Nós.", "",
         "## A ordem do operador", "",
         "- `%s` (sha16 `%s`): «%s»; «%s» — a ordem desta versão." % (ORDEM.name, d["ordem_sha16"], _DL.FRASE_ORDEM_V410, _DL.FRASE_TUDO_ENTRA),
         "- `%s` (sha16 `%s`): «%s» — a ORDEM DE PUBLICAÇÃO desta versão (use este caminho em `--ordem`)." % (ORDEM_PUBLICACAO.name, d["pub_sha16"], TRECHO_PUBLICACAO),
         "- A divisão de 04/11 (`%s`, sha16 `%s`): a custódia inteira é da sessão de custódia; a c1 fica só com o um.py." % (DIVISAO_0411.name, d["div_sha16"]), "",
         "## O estado, lido em %s por script" % hoje.strftime("%d/%m"), "",
         "- Selo do Nós **v410** (timestamp %s; `%s`; `%s`); `um.py` sha16 **`%s`** (%d B); escada **%s/%s**; gate intocado (`%s…`)." % (d["selo_ts"], d["selftest"], d["trailer"], d["pin"], d["um_bytes"], d["escada"][0], d["escada"][1], d["gate"][:60]),
         "- Rito %s–%s; pós-rito 0 → 14 OK; Bancada: o B(n) da versão aplicado (evento %s, hash `%s`), serviço religado." % (d["rito_h0"][:5], d["rito_h1"][:5], d["evento"], d["evento_hash"]),
         "- `Nós\\HANDOFF_v410_CUSTODIA.md` (%d B, sha16 `%s`) com os sete textos, os parágrafos prontos e, na seção “README: o que fica evidente”, os dois blocos do README (`README_FRENTE_v410`, %d bytes em UTF-8, e `README_O_QUE_SAI_v410`); "
         "recibo `work\\cadeia_de_selo\\v410\\pos_rito\\RECIBO_TEXTOS_CUSTODIA_HANDOFF_v410.json` (sha16 `%s`); o portão do G1 rodou sobre o HANDOFF INTEIRO no S6d: limpo." % (d["handoff_bytes"], d["handoff_sha16"], d["rf_bytes"], d["recibo_sha16"]),
         "- O orquestrador da v410 NÃO tem S7 (G1 --publicar) nem S10 (release do app): a cadeia termina no handoff; a custódia é sua.",
         "- Revisão de terceiro: `work\\cadeia_de_selo\\v410\\revisao_terceiro\\REVISAO_TERCEIRO_v410.json` (sha16 `%s`), aprovada sobre o candidato `%s`; revisor: %s%s." % (d["rev_sha16"], d["pin"], d["rev_revisor"], rev_n), "",
         "## O que entrou (para a custódia saber o que publica)", "",
         d["arco_pt"], "",
         "## O que é da custódia, na ordem", "",
         "1. `custodiar.py planejar --versao v410 --seco` → `custodiar.py executar --versao v410 --publicar --ordem \"%s\"` → `custodiar.py auditar --versao v410`. Nunca `--aceitar-molde`; não editar insumos." % ORDEM_PUBLICACAO,
         "2. O README do espelho, pela seção “README: o que fica evidente” do handoff: o bloco pronto para a frente (entre os marcadores `README_FRENTE_v410`) e o que sai (entre os marcadores `README_O_QUE_SAI_v410`).",
         "3. A release v410 do app, os dispositivos, a Central, o site e os links pelo G1.",
         "4. A linha do MEMORY.md é promoção da gerência: depositar na fila (`memoria.py depositar`) e avisar a c1.", "",
         "## Notas", "",
         "- O teste H0DN × BG1 NÃO foi aberto, e o README diz isso.",
         "- %d nomes da pedra `AEscala` seguem [DECLARADO pela autoria], pendentes de confirmação do operador (a lista está no handoff)." % d["n_autoria"],
         "- A custódia decidiu “accreditation” na prosa em inglês do README; os conectores novos do bloco já a usam; as constantes do delta trazem “creditation” e a unificação fica para a versão seguinte.", "",
         "Validade no kernel não é creditação; NOT_FALSIFIED nunca é CONFIRMED; o gate não se move.", "",   # (sem crases: a formula da regua que o portao do G1 reconhece e' a frase inteira, letra por letra)
         "— gerência c1, pelo orquestrador da v410 (passo S9_gatilho_custodia), %s." % hoje.strftime("%d/%m/%Y"), ""]
    return "\n".join(L)


def s9_gatilho_custodia(e, nos=None, pk=None, destino=None, cen_g1=None):
    """S9_gatilho_custodia (ADITIVO 1, 10/11/2026): o passo FINAL, depois de tudo. Escreve o gatilho da custodia (ORDEM_HANDOFF_CUSTODIA_v410.md) SO' SE todos os passos anteriores estiverem feitos e verdadeiros, o HANDOFF existir no Nos
    com os sete marcadores e os dois blocos do README, e o portao do G1 tiver rodado limpo no S6d (mais: o selo, o um.py, a escada, o gate, o trailer do rito, o recibo dos textos e a revisao de terceiro conferem). Senao NAO escreve e
    registra o motivo: a custodia continua esperando (fail-closed). Nao sobrescreve um gatilho que ja' exista. A escrita e' por temporario e os.replace: o arquivo e' o gatilho e tem de aparecer inteiro.
    (nos, pk, destino e cen_g1 so' mudam nos testes em sandbox; em producao sao os da casa.)"""
    if feito(e, "S9_gatilho_custodia"):
        return True
    nos = Path(nos) if nos else NOS; pk = Path(pk) if pk else PK; destino = Path(destino) if destino else GATILHO; cen_g1 = Path(cen_g1) if cen_g1 else CEN
    try:
        d, motivos = _gatilho_ler(e, nos, pk, cen_g1)
        if destino.exists():
            motivos.append("o gatilho ja' existe e este passo nao o registrou: nao sobrescrevo (%s)" % destino.name)
        txt = ""
        if not motivos:
            txt = _gatilho_render(d)
            import guarda_frases_v410 as _GF   # as mesmas guardas dos textos da custodia: a guarda das frases da v410 e o portao do G1 (os hashes conhecidos sao os do proprio texto, lidos por script)
            from custodia_g1 import textos as _TXG1
            conh = set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{16}(?![0-9a-fA-F])", txt)) | set(re.findall(r"(?<![0-9a-fA-F])[0-9a-f]{64}(?![0-9a-fA-F])", txt))
            viol = [list(x) for x in _GF.violacoes(txt)] + list(_TXG1.portao(txt, conh, rotulo=destino.name))
            if re.search(r"(?i)mil[eê]nio|millennium|navier|lindão", txt) or (re.search(r"(?i)kimi", txt) and not re.search(r"(?i)h0dn", txt)) or any(x_.lower() in txt.lower() for x_ in _DL.FORA_D65):   # (a MESMA regra do S6d: a D59, com o nome do executor so' no contexto do H0DN, e a D65)
                viol.append("D59/D65: o gatilho traz o que fica fora dos textos")
            if viol:
                motivos.append("o texto do gatilho nao passa nas guardas: %r" % (viol[:3],))
        if motivos:
            marcar(e, "S9_gatilho_custodia", False, gatilho_escrito=False, motivo=motivos[:10])
            log("S9_gatilho_custodia: o gatilho NAO foi escrito; a custodia continua esperando (fail-closed); a gerencia decide")
            return False
        b = txt.encode("utf-8"); tmp = destino.with_name(destino.name + ".tmp")
        tmp.write_bytes(b); assert tmp.stat().st_size == len(b) > 0
        os.replace(tmp, destino); assert destino.read_bytes() == b
        marcar(e, "S9_gatilho_custodia", True, gatilho_escrito=True, gatilho=str(destino), bytes=len(b), sha16=sha16(destino), handoff_sha16=d["handoff_sha16"], readme_frente_bytes_utf8=d["rf_bytes"], ordem_de_publicacao=str(ORDEM_PUBLICACAO), ordem_de_publicacao_sha16=d["pub_sha16"])
        log("S9_gatilho_custodia: o gatilho da custodia foi escrito (%s; %d B): a custodia da v410 e' da sessao de custodia" % (destino, len(b)))
        return True
    except Exception:  # noqa: BLE001
        marcar(e, "S9_gatilho_custodia", False, gatilho_escrito=destino.exists(), erro=traceback.format_exc()[-600:]); return False


def s9_relatorio(e):
    p = e["passos"]
    md = ["# RELATÓRIO PÓS-TREINO v410 — orquestrador da gerência c1", "", "Ordem do operador: `%s`" % ORDEM.name, "", "| passo | ok | quando | dados |", "|---|---|---|---|"]
    for k, v in p.items():
        md.append("| %s | %s | %s | %s |" % (k, v.get("ok"), v.get("quando"), json.dumps({a: b for a, b in v.items() if a not in ("ok", "quando")}, ensure_ascii=False)[:300].replace("|", "¦")))
    md.append(""); md.append("Estado inteiro: `orquestrador/ESTADO.json`; logs ao lado. Nada aqui move o gate; `NOT_FALSIFIED` nunca é `CONFIRMED`.")
    (ORQ / "RELATORIO_POS_TREINO_v410.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    (ORQ / "RELATORIO_POS_TREINO_v410.json").write_text(json.dumps(e, ensure_ascii=False, indent=1), encoding="utf-8")
    try:
        subprocess.run([PY, "-X", "utf8", r"C:\IALD\PROGRAMA_IALD\iald.py", "anotar", "--quem", "claude-c1", "--tipo", "evidencia", "--unidade", "F1.FECHO.MONTAGEM_02nov",
                        "--dados", json.dumps({"orquestrador": str(ORQ / "RELATORIO_POS_TREINO_v410.json"), "passos_ok": [k for k, v in p.items() if v.get("ok")], "passos_falhos": [k for k, v in p.items() if v.get("ok") is False]}, ensure_ascii=False)],
                       capture_output=True, timeout=120)
    except Exception:  # noqa: BLE001
        pass
    log("relatório gravado: %s" % (ORQ / "RELATORIO_POS_TREINO_v410.md"))


def main():
    e = carregar(); e["pid"] = os.getpid(); gravar(e)
    log("orquestrador iniciado (pid %d); ordem: %s" % (os.getpid(), ORDEM.name))
    _conferir_ordem()   # fail-closed: o sha16 do arquivo da ordem esta no AUT e a frase esta no arquivo
    try:
        for passo in (s0_treino, s1_prep, s1b_revisao, s2_prevoo, s3_instalar, s4_rito, s5_cadeia_0_10, s6_bancada, s8_nativa, s9_gatilho_custodia):   # D57: o fim da cadeia e' o HANDOFF (S6d); sem s7_g1 e sem s10_app
            if parar_pedido():
                log("PARAR pedido — paro antes de %s" % passo.__name__); break
            if not passo(e):
                log("PARADA em %s — nada é restaurado sozinho; a gerência decide" % passo.__name__); break
    except Exception:  # noqa: BLE001
        log("EXCEÇÃO: " + traceback.format_exc()[-1500:])
    finally:
        pensamento_do_dia_fallback(e)
        if e["passos"].get("S0_treino", {}).get("ok") is True and not feito(e, "S8_nativa") and not parar_pedido():
            try:   # a nativa não depende da v410: a cadeia pode ter parado no meio
                rc, out, _ = ps(CMD_VIVOS)
                if [x for x in out.split() if x.isdigit()]:
                    marcar(e, "S8_nativa", False, motivo="rito ou pilar ainda vivo; não religo a nativa por cima; a gerência decide")
                else:
                    s8_nativa(e)
            except Exception:  # noqa: BLE001
                log("S8 no encerramento: " + traceback.format_exc()[-600:])
        s9_relatorio(e)


if __name__ == "__main__":
    if "--plano" in sys.argv:
        sys.exit(0 if _plano() else 1)
    if "--ensaio" in sys.argv:   # D57: o S10 nao e' desta versao; o ensaio e' so' o plano (so' leitura)
        sys.exit(0 if _plano() else 1)
    main()

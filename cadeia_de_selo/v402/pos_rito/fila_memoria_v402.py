# -*- coding: utf-8 -*-
"""fila_memoria_v402.py -- o passo da FILA DA MEMORIA do pos-rito da v402 (ARQUIVO NOVO desta cadeia; ordem do operador de 26/10/2026: so' a gerencia c1 escreve o MEMORY.md; o vigia, tarefa agendada, compara o indice ao pino).
O pos-rito escreve o MEMORY.md (passo 7, superficies_v402.py) e por isso: (1) NO INICIO confere que o memoria.py e' o PINADO (sha256 e sha16 de PINO_MEMORIA_PY_v402.json, lidos do arquivo na hora) e que nao ha fila\\PAUSA_VIGIA.json;
(2) ANTES de escrever o indice CRIA a pausa {"quem","ate","motivo"} (escrita atomica: temporario + os.replace; o memoria.py NAO cria nem remove esse arquivo); (3) DEPOIS da escrita e da validacao do MEMORY.md (<=195 linhas contadas por \\n, <24000 B) PINA
(MEMORIA_GERENCIA=claude-c1 memoria.py pinar --motivo "pos-rito v402", rc 0 exigido); (4) SO' ENTAO remove a pausa; (5) por ultimo roda memoria.py verificar (rc 0 e ok:true). Em falha ANTES do pino a pausa NAO e' removida: ela vale no maximo 4 h (o teto e' do memoria.py) e evita que o vigia restaure o indice.
O diretorio de memoria e' parametrizado por V402_MEMORIA_DIR (padrao: o REAL; no ensaio, uma COPIA): o memoria.py usado e' o de <dir>\\fila\\memoria.py e recebe MEMORIA_DIR=<dir>.
uso: python -I -B -X utf8 fila_memoria_v402.py <guardas [--retomada] | pausa-criar | pinar | pausa-remover | verificar>     saida: UMA linha JSON; rc 0 = ok; rc 1 = recusa/falha (a cadeia PARA)
--retomada (so' em guardas): uma pausa que JA exista e seja a nossa (quem == "claude-c1 pos-rito v402"), deixada por uma execucao anterior que parou entre o passo 7 e o pino, e' aceita (e sera renovada); pausa de outro dono nunca e' aceita.
Nada aqui toca o MEMORY.md: so' le o indice (linhas e bytes) e escreve o marcador de pausa; o indice e' escrito pela superficie e pinado pelo memoria.py."""
import datetime, hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PK = os.path.dirname(HERE)
QUEM = "claude-c1 pos-rito v402"
MOTIVO_PAUSA = "pos-rito v402 escreve o indice"
MOTIVO_PINO = "pos-rito v402"
PAUSA_HORAS = 1
LIMITE_LINHAS = 195; LIMITE_BYTES = 24000
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")


def mem_dir():
    return os.path.abspath(os.environ.get("V402_MEMORIA_DIR") or MEM_REAL)


def caminhos():
    d = mem_dir(); f = os.path.join(d, "fila")
    return {"dir": d, "fila": f, "memoria_py": os.path.join(f, "memoria.py"), "pausa": os.path.join(f, "PAUSA_VIGIA.json"), "indice": os.path.join(d, "MEMORY.md"), "pino": os.path.join(f, "PINO_MEMORY.json")}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def saida(ok, op, **kw):
    d = {"ok": bool(ok), "op": op}; d.update(kw)
    print(json.dumps(d, ensure_ascii=False, sort_keys=True))
    return 0 if ok else 1


def le_pausa(p):
    """None se nao ha pausa; senao o dict lido (ou {'_ilegivel': erro})."""
    if not os.path.isfile(p["pausa"]):
        return None
    try:
        return json.loads(open(p["pausa"], "rb").read().decode("utf-8"))
    except Exception as e:   # noqa: BLE001
        return {"_ilegivel": repr(e)[:160]}


def pausa_e_nossa(d):
    return isinstance(d, dict) and d.get("quem") == QUEM


def roda_memoria(p, args):
    env = dict(os.environ); env["MEMORIA_DIR"] = p["dir"]; env["MEMORIA_GERENCIA"] = "claude-c1"; env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, "-X", "utf8", p["memoria_py"]] + args, capture_output=True, env=env, cwd=p["fila"])
    so = r.stdout.decode("utf-8", errors="replace"); se = r.stderr.decode("utf-8", errors="replace")
    j = None
    for tentativa in (so.strip(), (so.strip().splitlines() or [""])[-1]):   # o memoria.py imprime UM objeto JSON (identado, varias linhas); a ultima linha e' so' a reserva
        try:
            j = json.loads(tentativa) if tentativa else None
            break
        except ValueError:
            j = None
    return r.returncode, j, so, se


def op_guardas(retomada):
    p = caminhos()
    try:
        pino = json.load(open(os.path.join(PK, "PINO_MEMORIA_PY_v402.json"), encoding="utf-8"))
    except (OSError, ValueError) as e:
        return saida(False, "guardas", erro="nao li PINO_MEMORIA_PY_v402.json (o pino do memoria.py): %r" % (e,))
    if not os.path.isfile(p["memoria_py"]):
        return saida(False, "guardas", erro="memoria.py ausente em %s" % p["memoria_py"])
    raw = open(p["memoria_py"], "rb").read(); s256 = sha(raw); s16 = s256[:16]
    if not (pino.get("sha256") and pino.get("sha16") and s256 == pino["sha256"] and s16 == pino["sha16"]):
        return saida(False, "guardas", erro="o memoria.py (%s) tem sha16 %s e o pino de PINO_MEMORIA_PY_v402.json e %s: a ferramenta mudou depois do pino; a gerencia confere a mudanca e a re-pina (pino_memoria_py_v402.py) antes de o pos-rito escrever o indice" % (p["memoria_py"], s16, pino.get("sha16")), sha16=s16, sha16_pinado=pino.get("sha16"))
    if not os.path.isfile(p["indice"]):
        return saida(False, "guardas", erro="MEMORY.md ausente em %s" % p["indice"])
    d = le_pausa(p)
    aviso = None
    if d is not None:
        if retomada and pausa_e_nossa(d):
            aviso = "a PAUSA_VIGIA.json de uma execucao anterior deste pos-rito (ate %s) ainda esta posta: aceita por ser a nossa (retomada); sera renovada no passo 7/9" % d.get("ate")
        else:
            return saida(False, "guardas", erro="fila\\PAUSA_VIGIA.json JA EXISTE (%s): o pos-rito nao a cria por cima nem a remove de outro dono; a gerencia confere de quem e (e a remove se for lixo) e retoma%s" % (json.dumps(d, ensure_ascii=False)[:200], "" if retomada else " (em retomada a partir do passo 7 a pausa NOSSA e' aceita)"), pausa=d)
    # linha de base, SO' informativa (nao bloqueia): a leitura do invariante da fila antes de comecar
    rc, j, so, se = roda_memoria(p, ["verificar"])
    return saida(True, "guardas", memoria_py=p["memoria_py"], sha16=s16, sha16_pinado=pino["sha16"], sem_pausa=(d is None), aviso=aviso, linha_de_base_verificar={"rc": rc, "ok": (j or {}).get("ok") if isinstance(j, dict) else None, "violacoes": ((j or {}).get("violacoes") or [])[:3] if isinstance(j, dict) else None}, dir=p["dir"])


def op_pausa_criar():
    p = caminhos()
    if not os.path.isdir(p["fila"]):
        return saida(False, "pausa-criar", erro="sem a pasta fila\\ em %s" % p["dir"])
    d = le_pausa(p)
    if d is not None and not pausa_e_nossa(d):
        return saida(False, "pausa-criar", erro="fila\\PAUSA_VIGIA.json existe e NAO e' a nossa: %s" % json.dumps(d, ensure_ascii=False)[:200])
    ate = (datetime.datetime.now().astimezone().replace(microsecond=0) + datetime.timedelta(hours=PAUSA_HORAS)).isoformat()
    corpo = json.dumps({"quem": QUEM, "ate": ate, "motivo": MOTIVO_PAUSA}, ensure_ascii=False, indent=1).encode("utf-8")
    tmp = p["pausa"] + ".tmp_v402_%d" % os.getpid()
    try:
        with open(tmp, "wb") as f:
            f.write(corpo)
        assert os.path.getsize(tmp) == len(corpo), "temporario com tamanho errado"
        os.replace(tmp, p["pausa"])
        assert open(p["pausa"], "rb").read() == corpo, "a pausa gravada difere do que foi escrito"
    except Exception as e:   # noqa: BLE001
        if os.path.exists(tmp):
            os.remove(tmp)
        return saida(False, "pausa-criar", erro=repr(e)[:200])
    return saida(True, "pausa-criar", pausa=p["pausa"], ate=ate, quem=QUEM, renovada=(d is not None))


def op_pinar():
    p = caminhos()
    d = le_pausa(p)
    if not pausa_e_nossa(d):
        return saida(False, "pinar", erro="recuso pinar sem a nossa fila\\PAUSA_VIGIA.json posta (a pausa deve cobrir a escrita do indice ate o pino): %s" % (json.dumps(d, ensure_ascii=False)[:160] if d is not None else "ausente"))
    if not os.path.isfile(p["indice"]):
        return saida(False, "pinar", erro="MEMORY.md ausente")
    raw = open(p["indice"], "rb").read(); nl = raw.count(b"\n")
    if nl > LIMITE_LINHAS or len(raw) >= LIMITE_BYTES:
        return saida(False, "pinar", erro="o MEMORY.md tem %d B e %d linhas (limites: <%d B e <=%d linhas): nao pino um indice fora do limite" % (len(raw), nl, LIMITE_BYTES, LIMITE_LINHAS), bytes=len(raw), linhas=nl)
    rc, j, so, se = roda_memoria(p, ["pinar", "--motivo", MOTIVO_PINO])
    if rc != 0 or not (isinstance(j, dict) and j.get("ok") is True):
        return saida(False, "pinar", erro="memoria.py pinar saiu com rc %s (ok=%r): %s" % (rc, (j or {}).get("ok") if isinstance(j, dict) else None, (se or so).strip()[:300]), rc=rc)
    try:
        pn = json.load(open(p["pino"], encoding="utf-8"))
    except (OSError, ValueError) as e:
        return saida(False, "pinar", erro="o pino nao se le depois do pinar: %r" % (e,), rc=rc)
    atual = open(p["indice"], "rb").read()
    if pn.get("sha256") != sha(atual):
        return saida(False, "pinar", erro="PINO_MEMORY.json (%s) != sha256 do MEMORY.md (%s) depois do pinar (o indice mudou durante o pino?)" % (str(pn.get("sha256"))[:16], sha(atual)[:16]), rc=rc)
    return saida(True, "pinar", rc=rc, sha16=sha(atual)[:16], bytes=len(atual), linhas=atual.count(b"\n"), pino_por=pn.get("por"), pino_em=pn.get("pinado_em"), seq_do_livro=j.get("seq"), reguas=j.get("reguas"))


def op_pausa_remover():
    p = caminhos()
    d = le_pausa(p)
    if d is None:
        return saida(True, "pausa-remover", ja_ausente=True)
    if not pausa_e_nossa(d):
        return saida(False, "pausa-remover", erro="a pausa existente NAO e' a nossa: nao a removo: %s" % json.dumps(d, ensure_ascii=False)[:200])
    try:
        os.remove(p["pausa"])
    except OSError as e:
        return saida(False, "pausa-remover", erro=repr(e)[:200])
    return saida(not os.path.exists(p["pausa"]), "pausa-remover", removida=True)


def op_verificar():
    p = caminhos()
    rc, j, so, se = roda_memoria(p, ["verificar"])
    ok = bool(rc == 0 and isinstance(j, dict) and j.get("ok") is True)
    return saida(ok, "verificar", rc=rc, memoria_py_ok=(j or {}).get("ok") if isinstance(j, dict) else None, violacoes=((j or {}).get("violacoes") or [])[:5] if isinstance(j, dict) else None, avisos=((j or {}).get("avisos") or [])[:3] if isinstance(j, dict) else None, indice=(j or {}).get("indice") if isinstance(j, dict) else None, stderr=(se or "").strip()[:200])


def main(argv):
    ops = {"guardas": lambda: op_guardas("--retomada" in argv), "pausa-criar": op_pausa_criar, "pinar": op_pinar, "pausa-remover": op_pausa_remover, "verificar": op_verificar}
    if len(argv) < 2 or argv[1] not in ops:
        print("uso: fila_memoria_v402.py <%s> [--retomada]" % " | ".join(ops)); return 2
    return ops[argv[1]]()


if __name__ == "__main__":
    sys.exit(main(sys.argv))

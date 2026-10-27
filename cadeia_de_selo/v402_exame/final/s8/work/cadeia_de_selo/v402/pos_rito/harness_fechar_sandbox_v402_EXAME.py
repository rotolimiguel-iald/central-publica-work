# -*- coding: utf-8 -*-
"""harness_fechar_sandbox_v402.py -- (1) A FILA DA MEMORIA do pos-rito em COPIA da memoria e (2) roda fechar_v402.py e registrar_mapa_v402.py (o main) num SANDBOX inteiro dentro de pos_rito\\harness_saida_v402 (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).
(1) A FILA DA MEMORIA (NOVO na v402; ordem do operador de 26/10/2026: so' a gerencia c1 escreve o MEMORY.md; o vigia compara o indice ao pino): ensaio, numa COPIA do diretorio de memoria (harness_saida_v402\\memoria_copia: os arquivos NAO-.bak do diretorio real + fila\\ inteira; MEMORIA_DIR e V402_MEMORIA_DIR apontam para a copia),
do passo do pos-rito que PAUSA o vigia, escreve o indice, PINA, solta a pausa e VERIFICA, em quatro niveis: (a) as operacoes de fila_memoria_v402.py na ORDEM em que o chain as chama (ordem lida do TEXTO do chain): pausa criada ANTES da escrita do indice, o vigia (--enforcar --carencia 0) so' RELATA sob a pausa e RESTAURARIA sem ela
(controle de utilidade), pinar rc 0, a pausa SO' sai depois do pino, verificar rc 0 e PINO_MEMORY.json == sha256 do MEMORY.md da copia; (b) controles negativos (memoria.py com sha16 diferente do pino => para; pausa alheia => para e fica; pinar falha => a pausa PERMANECE; MEMORY.md acima do limite => recusa; verificar reprova);
(c) o PROPRIO superficies_v402.py (copia de bytes) com leitura e textos de ENSAIO (stubs): sem pausa valida recusa rc 6 sem escrever, com pausa grava, acima de 195 linhas ou 24 000 B recusa rc 3 sem escrever; (d) o PROPRIO chain_pos_rito_v402.sh (copia so' com as linhas de caminho trocadas) nos passos 7 a 9 num pacote SINTETICO: ordem, mensagens e codigos de saida
(a pausa PERMANECE quando falha antes do pino). O diretorio REAL de memoria nunca e' escrito: o harness compara o sha256 de MEMORY.md, fila\\PINO_MEMORY.json e fila\\fila.jsonl (e a ausencia de fila\\PAUSA_VIGIA.json) antes e depois e REGISTRA a prova.
(2) O que o harness_textos_ensaio_v402.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, a copia do sidecar e do selo, o handoff com os DOIS paragrafos do README/site, o aviso de que o do testemunho segue como esta e a lista do sidecar) e o main do registrar_mapa; e o b3_recibo_v402.py com recibos SINTETICOS.
Derivado do harness_fechar_sandbox_v401.py (que rodou na v401), com as licoes da v402 (a ponte, a queda, a esperanca; o passo simples B10 -> B11).
O sandbox e' uma ARVORE ISOLADA: work\\cadeia_de_selo\\v402 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v401, insumos (o resultado pinado do Teste da Unica Palavra, que mora na v397, ganha uma COPIA em insumos\\fase9 so' no sandbox), quadro_v397 e runtime_quadro_v397, o runtime_v402 e o acom_conferencias_v402,
o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + as pastas irmas v401, v400 e v399 (o delta_v402 importa o delta_v401, este o delta_v400 e este o delta_v399; o runtime da secao e as seis fontes do operador moram na v400) + nos\\ (o Nos EMULADO montado de dry_v402, como no harness dos textos, com o SIDECAR gerado pela funcao do proprio candidato)
+ memory\\ (uma COPIA da memoria, para o fechar e o fila_info) + work\\cunhagens_13out (as falas do operador). O conferidor REAL roda no proprio pacote do sandbox (SEM -I), onde acha tudo pelo caminho da propria pasta. As copias dos scripts (leitura, textos) trocam SO' a constante de caminho do Nos por caminho do sandbox;
o fechar recebe a memoria por V402_MEMORIA_DIR (sem trocar linha nenhuma); o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais e' so' essas linhas).
O que ele prova no fechar: fechar_v402.py sai com rc 0 e grava o handoff (guarda P18 limpa) com os DOIS paragrafos do README/site entre os marcadores (o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o da v402 (a ponte, a queda e a esperanca)
igual ao gerado do core e aprovado por T.verificar_paragrafo_v402), a frase de que o do testemunho de dois SEGUE COMO ESTA e a lista do sidecar (sha256 e veredito), o handoff do Nos, os dois diffs (com as TRES pedras novas), o manifesto (com o estado da fila) e o arquivo, e copia o sidecar e o selo para v402_selo; RECUSA (rc 2, sem handoff)
sem o recibo do religamento, com um recibo do B(n) que declara salto, com o resultado pinado adulterado, com o numero lido adulterado, com um numero da ponte, da queda ou da esperanca adulterado, com a direcao do testemunho invertida, com uma inscricao de 26/10 rotulada como da gerencia, com uma errata ou uma decisao a menos, com H_tau
literal dita aberta ou a seta da queda dita derivada, com uma pedra fora do trio e com o sidecar adulterado ou ausente; registrar_mapa_v402.py (main) monta o JSON e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v401): a prova e' do CODIGO do fechar e do b3_recibo, nao de um B(n) real.
uso: python -B -X utf8 harness_fechar_sandbox_v402.py [--manter] [--nao-exigir-refazer] [--so-fila] [--sem-fila]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado; sem a flag EXIGE refazer_out_v402.txt com '== FIM' e mais novo que o ESPERADOS; --nao-exigir-refazer: NAO o exige, o resumo DIZ que a regeneracao nao foi comprovada e vai para
HARNESS_FECHAR_SANDBOX_v402_DEPURACAO_sem_refazer.json -- o nome HARNESS_FECHAR_SANDBOX_v402.json so' nasce na rodada que EXIGE o refazer; --so-fila: so' a fila da memoria (nao depende de textos_v402 nem de leitura_v402) e grava HARNESS_FECHAR_SANDBOX_v402_SO_FILA.json; --sem-fila: so' o fechar)"""
import datetime, glob, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE); DRY = os.path.join(PKG, "dry_v402")
OUT = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v402_exame/final/hs8"; SB = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v402_exame/final/sb8"   # EXAME: caminho curto (MAX_PATH)
sys.path.insert(0, PKG)
from guarda_p18_v402 import violacoes  # noqa: E402
MANTER = "--manter" in sys.argv; NAO_REFAZER = "--nao-exigir-refazer" in sys.argv; SO_FILA = "--so-fila" in sys.argv; SEM_FILA = "--sem-fila" in sys.argv
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(open(p, "rb").read())
rdj = lambda p: json.load(open(p, encoding="utf-8"))
R = {"inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "problemas": [], "etapas": {}}


def falha(m):
    R["problemas"].append(m); print("  PROBLEMA:", m)


def recusa(m):
    print("RECUSO:", m); sys.exit(4)


# =====================================================================================================================================================
#  (1) A FILA DA MEMORIA -- ensaio em COPIA do diretorio de memoria
# =====================================================================================================================================================
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
FILA_PY = os.path.join(HERE, "fila_memoria_v402.py"); CHAIN_PY = os.path.join(HERE, "chain_pos_rito_v402.sh"); SUP_PY = os.path.join(HERE, "superficies_v402.py")
QUEM = "claude-c1 pos-rito v402"; PY_EXE = sys.executable
FM = os.path.join(OUT, "memoria_copia")                      # a copia pedida pela gerencia: harness_saida_v402\memoria_copia
FILA_EV = {"contrato": "FILA_MEMORIA_ENSAIO_v402", "checks": [], "cenarios": {}, "nota": "ensaio em COPIA; o diretorio real de memoria nunca e' escrito (prova no fim)"}


def chk(nome, cond, det=""):
    ok = bool(cond)
    FILA_EV["checks"].append({"check": nome, "ok": ok, "det": str(det)[:300]})
    if not ok:
        falha("[fila] %s %s" % (nome, str(det)[:240]))
    return ok


def prova_real():
    """sha256/bytes/mtime dos arquivos do diretorio REAL de memoria que o ensaio jamais pode tocar (None = nao existe)."""
    out = {}
    for rel in ("MEMORY.md", os.path.join("fila", "PINO_MEMORY.json"), os.path.join("fila", "fila.jsonl"), os.path.join("fila", "PAUSA_VIGIA.json")):
        p = os.path.join(MEM_REAL, rel)
        out[rel.replace(os.sep, "/")] = ({"sha256": fsha(p), "bytes": os.path.getsize(p), "mtime_ns": os.stat(p).st_mtime_ns} if os.path.exists(p) else None)
    return out


def mk_memoria_copia(dst):
    """COPIA do diretorio de memoria: os arquivos NAO-.bak do topo (menos os que ja' trazem 'v402' no nome, para o ensaio nao depender de o rito real ja' ter rodado) + fila\\ inteira (menos fila.lock, temporarios e a PAUSA_VIGIA.json, se houver). mtimes preservados."""
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
    n = tot = 0
    for f in sorted(os.listdir(MEM_REAL)):
        p = os.path.join(MEM_REAL, f)
        if os.path.isfile(p) and ".bak" not in f and ".tmp" not in f and "v402" not in f:
            shutil.copy2(p, os.path.join(dst, f)); n += 1; tot += os.path.getsize(p)
    fs = os.path.join(MEM_REAL, "fila")
    for r, ds, fl in os.walk(fs):
        rel = os.path.relpath(r, fs); os.makedirs(os.path.join(dst, "fila", rel), exist_ok=True)
        for f in fl:
            if f == "fila.lock" or ".tmp" in f or f == "PAUSA_VIGIA.json":
                continue
            shutil.copy2(os.path.join(r, f), os.path.join(dst, "fila", rel, f)); n += 1; tot += os.path.getsize(os.path.join(r, f))
    return {"arquivos": n, "bytes": tot}


def env_mem(d, **extra):
    e = dict(os.environ); e["V402_MEMORIA_DIR"] = d; e["MEMORIA_DIR"] = d; e["PYTHONIOENCODING"] = "utf-8"; e.pop("MEMORIA_GERENCIA", None); e.update(extra)
    return e


def ult_json(so):
    for t in (so.strip(), (so.strip().splitlines() or [""])[-1]):
        try:
            return json.loads(t) if t else None
        except ValueError:
            pass
    return None


def fila(op, d, *args):
    """o helper REAL do chain (fila_memoria_v402.py) contra a pasta d."""
    p = subprocess.run([PY_EXE, "-I", "-B", "-X", "utf8", FILA_PY, op] + list(args), capture_output=True, env=env_mem(d))
    so = p.stdout.decode("utf-8", "replace"); return p.returncode, ult_json(so), so, p.stderr.decode("utf-8", "replace")


def memoria(d, *args):
    """o memoria.py da COPIA (MEMORIA_DIR = a copia; MEMORIA_GERENCIA = claude-c1)."""
    p = subprocess.run([PY_EXE, "-X", "utf8", os.path.join(d, "fila", "memoria.py")] + list(args), capture_output=True, env=env_mem(d, MEMORIA_GERENCIA="claude-c1"), cwd=os.path.join(d, "fila"))
    so = p.stdout.decode("utf-8", "replace"); return p.returncode, _json_inteiro(so), so, p.stderr.decode("utf-8", "replace")


def _json_inteiro(so):
    try:
        return json.loads(so.strip()) if so.strip() else None
    except ValueError:
        return ult_json(so)


pausa_de = lambda d: os.path.join(d, "fila", "PAUSA_VIGIA.json")
idx_de = lambda d: os.path.join(d, "MEMORY.md")


def escreve_atomico(p, b):
    tmp = p + ".tmp_harness"; open(tmp, "wb").write(b); os.replace(tmp, p)


def edita_indice(d):
    """o que a superficie faz ao indice, em miniatura (uma linha de handoff nova antes da do v401), numa COPIA, com backup de bytes."""
    p = idx_de(d); raw = open(p, "rb").read()
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_harness_v402", "wb").write(raw)
    linhas = raw.decode("utf-8").split("\n"); k = [i for i, l in enumerate(linhas) if l.startswith("- [HANDOFF v401")]
    assert len(k) == 1, ("linha do handoff v401 no MEMORY.md da copia", len(k))
    linhas.insert(k[0], "- [HANDOFF v402 — ENSAIO DO HARNESS (linha sintetica numa COPIA)](handoff-v402-custodia.md) — **v402 SELADA (ensaio)**")
    novo = "\n".join(linhas).encode("utf-8"); escreve_atomico(p, novo)
    return {"antes": [len(raw), raw.count(b"\n")], "depois": [len(novo), novo.count(b"\n")]}


def enche_indice(d, linhas_alvo=None, bytes_alvo=None):
    """deixa o MEMORY.md da copia com `linhas_alvo` quebras de linha OU `bytes_alvo` bytes (acrescenta comentarios no fim), para os controles do limite."""
    p = idx_de(d); raw = open(p, "rb").read()
    if linhas_alvo is not None:
        while raw.count(b"\n") < linhas_alvo:
            raw += b"<!-- enchimento do harness -->\n"
    if bytes_alvo is not None:
        falta = bytes_alvo - len(raw) - len(b"<!--  -->\n")
        assert falta > 0, (len(raw), bytes_alvo)
        raw += b"<!-- " + b"x" * falta + b" -->\n"
        assert len(raw) == bytes_alvo, (len(raw), bytes_alvo)
    escreve_atomico(p, raw)
    return [len(raw), raw.count(b"\n")]


def hashes_topo(d):
    return {f: fsha(os.path.join(d, f)) for f in sorted(os.listdir(d)) if os.path.isfile(os.path.join(d, f))}


def ordem_do_chain():
    """a ORDEM das operacoes da fila, LIDA DO TEXTO do chain (linhas que nao sao comentario), e as linhas-ancora."""
    ls = open(CHAIN_PY, encoding="utf-8").read().split("\n")
    ops = []
    for i, l in enumerate(ls):
        if l.lstrip().startswith("#"):
            continue
        m = re.search(r'\$FILA" (guardas|pausa-criar|pinar|pausa-remover|verificar)', l)
        if m:
            ops.append((i, m.group(1)))
    ach = lambda pad: [i for i, l in enumerate(ls) if not l.lstrip().startswith("#") and pad in l]
    return ops, {"superficies_real": ach('superficies_v402.py"; sr=$?'), "porta": ach('"$PORTA" >'), "validacao_195": ach('[ "$l" -le 195 ]'), "sem_copias": ach("--copias")}


def ensaio_da_fila():
    print("== (1) A FILA DA MEMORIA em COPIA (nada real e' escrito)")
    E = FILA_EV; t0 = time.time()
    if not (os.path.isfile(FILA_PY) and os.path.isfile(CHAIN_PY) and os.path.isfile(SUP_PY) and os.path.isfile(os.path.join(MEM_REAL, "fila", "memoria.py"))):
        recusa("faltam fila_memoria_v402.py, chain_pos_rito_v402.sh, superficies_v402.py ou o memoria.py real")
    # ---- a ORDEM do chain (lida do texto)
    ops, anc = ordem_do_chain()
    seq = [o for _, o in ops]
    chk("a ordem das operacoes da fila no chain: guardas (passo 0); pausa-criar (passo 7); pausa-criar (renovar), pinar, pausa-remover, verificar (passo 9)", seq == ["guardas", "pausa-criar", "pausa-criar", "pinar", "pausa-remover", "verificar"], seq)
    if len(ops) == 6 and anc["superficies_real"] and anc["porta"] and anc["validacao_195"]:
        i = [l for l, _ in ops]
        ordem_ok = i[0] < i[1] < anc["superficies_real"][0] < anc["porta"][0] < anc["validacao_195"][-1] < i[2] < i[3] < i[4] < i[5]
        chk("no TEXTO do chain: guardas < pausa-criar < superficies (real) < espelho < validacao do MEMORY.md (195) < pausa-criar < pinar < pausa-remover < verificar", ordem_ok, {"linhas_das_operacoes": i, "ancoras": {k: v[:3] for k, v in anc.items()}})
    else:
        chk("as ancoras do chain (superficies real, espelho, validacao 195) foram achadas", False, {"ops": ops, "ancoras": anc})
    # ---- (a) a sequencia POSITIVA, na ordem do chain
    cp = mk_memoria_copia(FM); E["copia"] = dict(cp, caminho=FM)
    pino0 = rdj(os.path.join(FM, "fila", "PINO_MEMORY.json")); mem0 = fsha(idx_de(FM))
    tl = []

    def passo(nome, rc, j, extra=None):
        d = {"passo": nome, "rc": rc, "ok": (j or {}).get("ok"), "pausa_existe_depois": os.path.exists(pausa_de(FM)), "memory_md_sha16": fsha(idx_de(FM))[:16], "hora": time.strftime("%H:%M:%S")}
        d.update(extra or {}); tl.append(d); return d
    rc, j, so, se = fila("guardas", FM); passo("0. guardas", rc, j)
    chk("guardas: rc 0, memoria.py == o pino (sha16 lido de PINO_MEMORIA_PY_v402.json), sem pausa", rc == 0 and j and j.get("ok") and j.get("sem_pausa") is True and j.get("sha16") == j.get("sha16_pinado"), so[:300])
    chk("antes do passo 7 NAO existe fila\\PAUSA_VIGIA.json", not os.path.exists(pausa_de(FM)))
    rc, j, so, se = fila("pausa-criar", FM); passo("7. pausa-criar", rc, j)
    chk("pausa-criar: rc 0 e a pausa existe", rc == 0 and os.path.exists(pausa_de(FM)), so[:300])
    pz = rdj(pausa_de(FM)); ate = datetime.datetime.fromisoformat(pz["ate"]); agora = datetime.datetime.now().astimezone(); dm = (ate - agora).total_seconds() / 60
    chk("a pausa traz quem/ate/motivo exatos, 'ate' com fuso e ~ agora + 1 h", pz.get("quem") == QUEM and pz.get("motivo") == "pos-rito v402 escreve o indice" and ate.tzinfo is not None and 55 <= dm <= 61 and sorted(pz) == ["ate", "motivo", "quem"], {"pausa": pz, "minutos_a_frente": round(dm, 1)})
    chk("a escrita da pausa foi atomica: nenhum temporario sobrou em fila\\", not glob.glob(pausa_de(FM) + ".tmp*"))
    # a escrita do indice (passo 7) com a pausa posta
    assert os.path.exists(pausa_de(FM))
    ed = edita_indice(FM); passo("7. escrita do MEMORY.md (com a pausa posta)", 0, {"ok": True}, {"edicao": ed})
    chk("o MEMORY.md foi editado COM a pausa posta e cabe no limite (<=195 linhas, <24000 B)", ed["depois"][1] <= 195 and ed["depois"][0] < 24000 and fsha(idx_de(FM)) != mem0, ed)
    # o vigia sob a pausa: so' RELATA (nao restaura)
    mem_ed = fsha(idx_de(FM))
    rc, j, so, se = memoria(FM, "vigiar", "--enforcar", "--carencia", "0"); passo("7. vigiar --enforcar --carencia 0 (SOB a pausa)", rc, j, {"estado": (j or {}).get("estado")})
    chk("sob a pausa o vigia (--enforcar --carencia 0) so' RELATA a divergencia e NAO restaura o indice", rc == 4 and fsha(idx_de(FM)) == mem_ed and "PAUSA" in str((j or {}).get("estado")), {"rc": rc, "estado": (j or {}).get("estado"), "memory_md_igual_ao_editado": fsha(idx_de(FM)) == mem_ed})
    # controle de UTILIDADE: sem a pausa o mesmo vigia RESTAURARIA o indice (numa 2a copia)
    F2 = FM + "_sem_pausa"; shutil.rmtree(F2, ignore_errors=True); shutil.copytree(FM, F2)
    os.remove(pausa_de(F2)); rc2, j2, so2, se2 = memoria(F2, "vigiar", "--enforcar", "--carencia", "0")
    chk("CONTROLE DE UTILIDADE: SEM a pausa o mesmo vigia RESTAURA o indice ao pinado (a pausa evita exatamente isto)", fsha(idx_de(F2)) == mem0 and rc2 in (0, 4), {"rc": rc2, "estado": (j2 or {}).get("estado"), "memory_md_restaurado_ao_pinado": fsha(idx_de(F2)) == mem0})
    shutil.rmtree(F2, ignore_errors=True)
    rc, j, so, se = fila("pausa-criar", FM); passo("9. pausa-criar (renovar)", rc, j)
    chk("renovar a pausa: rc 0 e renovada=true", rc == 0 and j.get("renovada") is True, so[:200])
    rc, j, so, se = fila("pinar", FM); passo("9. pinar", rc, j)
    pn = rdj(os.path.join(FM, "fila", "PINO_MEMORY.json")); mem_final = open(idx_de(FM), "rb").read()
    chk("pinar: rc 0 (MEMORIA_GERENCIA=claude-c1 memoria.py pinar --motivo \"pos-rito v402\"), por claude-c1, e a pausa SEGUE posta ate' depois do pino", rc == 0 and j.get("ok") and pn.get("por") == "claude-c1" and "pos-rito v402" in str(pn.get("via")) and os.path.exists(pausa_de(FM)), {"rc": rc, "via": pn.get("via"), "por": pn.get("por")})
    chk("PINO_MEMORY.json (da copia) == sha256 do MEMORY.md (da copia)", pn.get("sha256") == sha(mem_final) and pn.get("bytes") == len(mem_final) and pn.get("linhas") == mem_final.count(b"\n"), {"pino": str(pn.get("sha256"))[:16], "md": sha(mem_final)[:16]})
    chk("o espelho PINO_MEMORY_conteudo.md == o MEMORY.md pinado (byte a byte)", open(os.path.join(FM, "fila", "PINO_MEMORY_conteudo.md"), "rb").read() == mem_final)
    chk("o pino mudou (era o do indice antigo)", pn.get("sha256") != pino0.get("sha256"))
    rc, j, so, se = fila("pausa-remover", FM); passo("9. pausa-remover (SO' depois do pino)", rc, j)
    chk("pausa-remover: rc 0 e a pausa saiu", rc == 0 and not os.path.exists(pausa_de(FM)), so[:200])
    rc, j, so, se = fila("verificar", FM); passo("9. verificar", rc, j, {"violacoes": (j or {}).get("violacoes")})
    chk("verificar: rc 0 e ok:true (nenhuma violacao)", rc == 0 and j and j.get("ok") is True and not j.get("violacoes"), so[:300])
    rc, j, so, se = memoria(FM, "vigiar"); passo("9. vigiar (sem enforcar)", rc, j, {"estado": (j or {}).get("estado")})
    chk("depois do pino o vigia diz OK (indice == pino)", rc == 0 and (j or {}).get("estado") == "OK", {"rc": rc, "estado": (j or {}).get("estado")})
    E["cenarios"]["a_sequencia_positiva"] = tl
    # ---- (b) controles negativos do helper (cada um numa copia nova)
    NEG = []; FN = os.path.join(OUT, "memoria_neg")

    def neg(nome, ok, det=""):
        NEG.append({"controle": nome, "ok": bool(ok), "det": str(det)[:300]})
        print("  controle negativo da fila: %-96s %s" % (nome[:96], "RECUSOU/PAROU como esperado" if ok else "FALHOU"))
        if not ok:
            falha("[fila] controle negativo: %s: %s" % (nome, str(det)[:200]))
    # N1: memoria.py com sha16 diferente do pino => guardas PARA, nada criado, indice intocado
    mk_memoria_copia(FN); m0 = fsha(idx_de(FN)); mp = os.path.join(FN, "fila", "memoria.py"); escreve_atomico(mp, open(mp, "rb").read() + b"\n# alterado pelo controle negativo do harness\n")
    rc, j, so, se = fila("guardas", FN)
    neg("memoria.py com sha16 DIFERENTE do pino => guardas PARA (rc 1), sem criar a pausa e sem tocar o indice", rc == 1 and j and j.get("ok") is False and j.get("sha16") != j.get("sha16_pinado") and not os.path.exists(pausa_de(FN)) and fsha(idx_de(FN)) == m0, so[:260])
    # N2: pausa de OUTRO dono => guardas (com e sem --retomada), pausa-criar e pausa-remover recusam e a pausa fica intacta
    mk_memoria_copia(FN); alheia = json.dumps({"quem": "outra sessao", "ate": (datetime.datetime.now().astimezone() + datetime.timedelta(hours=1)).isoformat(timespec="seconds"), "motivo": "outro motivo"}).encode(); escreve_atomico(pausa_de(FN), alheia)
    r1 = fila("guardas", FN); r2 = fila("guardas", FN, "--retomada"); r3 = fila("pausa-criar", FN); r4 = fila("pausa-remover", FN)
    neg("pausa de OUTRO dono: guardas (com e sem --retomada), pausa-criar e pausa-remover recusam (rc 1) e a pausa fica intacta, byte a byte", r1[0] == 1 and r2[0] == 1 and r3[0] == 1 and r4[0] == 1 and open(pausa_de(FN), "rb").read() == alheia, [r1[0], r2[0], r3[0], r4[0]])
    # N3: pausa NOSSA deixada por uma execucao anterior: guardas sem --retomada recusa; com --retomada aceita; pausa-criar renova
    mk_memoria_copia(FN); fila("pausa-criar", FN)
    r1 = fila("guardas", FN); r2 = fila("guardas", FN, "--retomada"); r3 = fila("pausa-criar", FN)
    neg("pausa NOSSA de uma execucao anterior: guardas SEM --retomada recusa (rc 1); COM --retomada aceita (rc 0, com aviso); pausa-criar a renova", r1[0] == 1 and r2[0] == 0 and (r2[1] or {}).get("aviso") and r3[0] == 0 and (r3[1] or {}).get("renovada") is True, [r1[0], r2[0], r3[0]])
    # N4: pinar SEM a nossa pausa posta => recusa e o pino nao muda
    mk_memoria_copia(FN); p0 = fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")); edita_indice(FN)
    rc, j, so, se = fila("pinar", FN)
    neg("pinar SEM a pausa posta => recusa (rc 1) e o pino NAO muda", rc == 1 and fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")) == p0, so[:240])
    # N5: pinar FALHA (o livro da fila perde a cabeca) => rc 1 e a PAUSA PERMANECE; o pino nao muda
    mk_memoria_copia(FN); p0 = fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")); fila("pausa-criar", FN); edita_indice(FN)
    cab = os.path.join(FN, "fila", "CABECA.json"); escreve_atomico(cab, b"{ isto nao e' json")
    rc, j, so, se = fila("pinar", FN)
    neg("pinar FALHA (CABECA.json do livro corrompida) => o helper sai rc 1, a PAUSA PERMANECE e o pino NAO muda (o chain PARA e nao a remove)", rc == 1 and j and j.get("ok") is False and os.path.exists(pausa_de(FN)) and fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")) == p0, so[:300])
    # N6: MEMORY.md acima do limite (linhas e bytes) => pinar recusa, o pino nao muda, a pausa fica
    for rotulo, kw in (("196 linhas (limite 195)", {"linhas_alvo": 196}), ("24 000 B (limite: abaixo de 24 000)", {"bytes_alvo": 24000})):
        mk_memoria_copia(FN); p0 = fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")); fila("pausa-criar", FN); enche_indice(FN, **kw)
        rc, j, so, se = fila("pinar", FN)
        neg("MEMORY.md com %s => pinar recusa (rc 1), o pino NAO muda e a pausa fica" % rotulo, rc == 1 and "limite" in str((j or {}).get("erro")) and fsha(os.path.join(FN, "fila", "PINO_MEMORY.json")) == p0 and os.path.exists(pausa_de(FN)), so[:260])
    # N7: verificar REPROVA (um topico sem frontmatter) => rc 1 e a violacao e' listada
    mk_memoria_copia(FN); escreve_atomico(os.path.join(FN, "zz_topico_sem_frontmatter.md"), b"sem frontmatter\n")
    rc, j, so, se = fila("verificar", FN)
    neg("verificar REPROVA (topico sem frontmatter na pasta de memoria) => rc 1, ok:false e a violacao listada (o TOPICO NOVO da v402 precisa de frontmatter name/description)", rc == 1 and j and j.get("ok") is False and any("zz_topico_sem_frontmatter" in str(v) for v in (j.get("violacoes") or [])), so[:300])
    E["controles_negativos_do_helper"] = NEG
    # ---- (c) o PROPRIO superficies_v402.py (copia de bytes) com leitura e textos de ENSAIO
    ensaio_superficies()
    # ---- (d) o PROPRIO chain nos passos 7 a 9, em pacote sintetico
    ensaio_chain()
    shutil.rmtree(FN, ignore_errors=True)
    E["segundos"] = round(time.time() - t0, 1)
    print("  fila da memoria: %d checagens, %d falharam" % (len(E["checks"]), sum(1 for c in E["checks"] if not c["ok"])))


# ---------------------------------------------------------------- (c) o superficies_v402.py com stubs de leitura e textos
STUB_LEITURA = '''# -*- coding: utf-8 -*-
# STUB do harness da fila (NAO e' a leitura da cadeia): devolve uma V minima e sem problemas.
NOS = %(nos)r


def ler():
    return ({'data': '26/10/2026', 's16': %(s16)r}, [])
'''
STUB_TEXTOS = '''# -*- coding: utf-8 -*-
# STUB do harness da fila (NAO sao os textos da cadeia): blocos curtos, limpos da guarda P18, com os marcadores que a superficie e o chain exigem.
TOPICO_NOVO = 'v402-selada-ponte-queda-esperanca.md'
REGS = 'ponte_da_escala_dual_v402 queda_sem_geometria_v402 esperanca_condicional_v402 cunhagens_v402 kh_n1_cobertura_v402'


def _b(V, marca, extra=''):
    return '%s\\n## ENSAIO DO HARNESS (v402, bloco sintetico) %s\\n\\n%s %s %s\\n' % (marca, V['s16'], V['s16'], REGS, extra)


def atribuicao_da_gerencia(texto):
    return []


def linhagem(V):
    return _b(V, '<!-- linhagem_v402_selada -->')


def desenho(V):
    return _b(V, '<!-- adendo_v402_selada -->')


def atlas(V):
    return _b(V, '<!-- atlas_v402_selada -->')


def core_memory(V):
    return _b(V, '<!-- core_v402_selada -->')


def haja_luz(V):
    return _b(V, '<!-- haja_luz_v402_selada -->')


def id_missao(V):
    return '<!-- stub_id_missao_v402 -->'


def id_central(V):
    return '<!-- stub_id_central_v402 -->'


def topico_missao(V):
    return _b(V, T_ID_MISSAO, 'missao')


def topico_central(V):
    return _b(V, T_ID_CENTRAL, 'central')


def topico_estatuto(V):
    return _b(V, '<!-- v402_selada -->', 'estatuto')


def topico_novo(V):
    return '---\\nname: v402-selada-ensaio\\ndescription: "topico NOVO de ensaio do harness (frontmatter valido)"\\nmetadata:\\n  type: project\\n---\\n\\n# v402 SELADA (ensaio) %s\\n\\n%s\\n' % (V['s16'], REGS)


def aviso(V, reiv):
    return _b(V, '<!-- aviso_v402_selada -->')


def aviso_pulado():
    return '  (AVISO_GERENCIA.md: PULADO no ensaio)'


def marca_missao(V):
    return '**v402 SELADA 26/10 `%s` (ENSAIO)** · ' % V['s16']


def linha_handoff(V):
    return '- [HANDOFF v402 — ENSAIO DO HARNESS](handoff-v402-custodia.md) — **v402 SELADA** `%s` (linha sintetica do harness da fila)' % V['s16']


T_ID_MISSAO = '<!-- stub_id_missao_v402 -->'
T_ID_CENTRAL = '<!-- stub_id_central_v402 -->'
'''


def mk_superficies_stub(raiz, s16, nos):
    shutil.rmtree(raiz, ignore_errors=True); pos = os.path.join(raiz, "pos_rito"); os.makedirs(pos)
    shutil.copyfile(SUP_PY, os.path.join(pos, "superficies_v402.py"))
    shutil.copyfile(os.path.join(PKG, "guarda_p18_v402.py"), os.path.join(raiz, "guarda_p18_v402.py"))
    open(os.path.join(pos, "leitura_v402.py"), "w", encoding="utf-8", newline="\n").write(STUB_LEITURA % {"nos": nos, "s16": s16})
    open(os.path.join(pos, "textos_v402.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)
    return pos


def roda_sup(pos, d, *args, extra_env=None):
    e = env_mem(d); e.update(extra_env or {})
    p = subprocess.run([PY_EXE, "-I", "-B", "-X", "utf8", os.path.join(pos, "superficies_v402.py")] + list(args), capture_output=True, env=e, cwd=pos)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def ensaio_superficies():
    print("  -- (c) superficies_v402.py (copia de bytes) com leitura e textos de ENSAIO, V402_MEMORIA_DIR = a copia")
    E = FILA_EV; NEG = []; raiz = os.path.join(OUT, "superficies_stub"); FS = os.path.join(OUT, "memoria_sup")
    pos = mk_superficies_stub(raiz, "5a5a5a5a5a5a5a5a", os.path.join(raiz, "nos"))

    def neg(nome, ok, det=""):
        NEG.append({"controle": nome, "ok": bool(ok), "det": str(det)[:300]})
        print("  controle negativo das superficies: %-90s %s" % (nome[:90], "RECUSOU como esperado" if ok else "FALHOU"))
        if not ok:
            falha("[fila] superficies: %s: %s" % (nome, str(det)[:200]))
    chk("o superficies do ensaio e' a COPIA DE BYTES do superficies_v402.py real (so' a leitura e os textos sao stubs)", fsha(os.path.join(pos, "superficies_v402.py")) == fsha(SUP_PY))
    # S1: sem pausa => rc 6, NADA escrito
    mk_memoria_copia(FS); h0 = hashes_topo(FS); ls0 = sorted(os.listdir(FS))
    rc, so, se = roda_sup(pos, FS)
    neg("sem a fila\\PAUSA_VIGIA.json => a superficie RECUSA (rc 6) sem escrever nada (nenhum arquivo do topo mudou ou nasceu)", rc == 6 and "rc 6" in so and hashes_topo(FS) == h0 and sorted(os.listdir(FS)) == ls0, (rc, so[:200]))
    # S2: pausa ALHEIA e pausa VENCIDA => rc 6
    escreve_atomico(pausa_de(FS), json.dumps({"quem": "outra sessao", "ate": (datetime.datetime.now().astimezone() + datetime.timedelta(hours=1)).isoformat(timespec="seconds"), "motivo": "x"}).encode())
    rc, so, se = roda_sup(pos, FS); neg("pausa de OUTRO dono => rc 6, nada escrito", rc == 6 and "outro dono" in so and hashes_topo(FS) == h0, (rc, so[:200]))
    escreve_atomico(pausa_de(FS), json.dumps({"quem": QUEM, "ate": (datetime.datetime.now().astimezone() - datetime.timedelta(minutes=5)).isoformat(timespec="seconds"), "motivo": "x"}).encode())
    rc, so, se = roda_sup(pos, FS); neg("pausa NOSSA mas VENCIDA => rc 6, nada escrito", rc == 6 and "vencida" in so and hashes_topo(FS) == h0, (rc, so[:200]))
    os.remove(pausa_de(FS))
    # S3: pausa valida (criada pelo helper) => grava
    rc0, j0, so0, se0 = fila("pausa-criar", FS)
    lin_antes = open(idx_de(FS), "rb").read().count(b"\n")
    rc, so, se = roda_sup(pos, FS)
    ix = open(idx_de(FS), "rb").read()
    ls1 = sorted(os.listdir(FS))
    chk("com a pausa valida a superficie GRAVA (rc 0): MEMORY.md +1 linha com a linha do handoff v402 e a marca da missao; MEMORY_2 recebe a linha velha VERBATIM; backups de bytes _sup402", rc == 0 and b"HANDOFF v402" in ix and b"v402 SELADA 26/10" in ix and ix.count(b"\n") == lin_antes + 1 and any(".bak_" in f and f.endswith("_sup402") and f.startswith("MEMORY.md") for f in ls1) and any(f.startswith("MEMORY_2.md.bak_") for f in ls1), {"rc": rc, "linhas": ix.count(b"\n"), "saida": so[-300:]})
    chk("a superficie nao criou nem removeu a pausa (isso e' do chain)", os.path.exists(pausa_de(FS)))
    # S4: idempotente
    h1 = hashes_topo(FS); rc, so, se = roda_sup(pos, FS)
    chk("2a rodada IDEMPOTENTE: rc 0 e nada muda", rc == 0 and hashes_topo(FS) == h1, (rc, so[-200:]))
    # S5: limite (linhas) com pausa valida => rc 3 sem escrever; (bytes) idem
    for rotulo, kw in (("linhas (195 antes; +1 do handoff = 196 > 195)", {"linhas_alvo": 195}), ("bytes (23 990 B antes; +1 linha > 24 000 B)", {"bytes_alvo": 23990})):
        mk_memoria_copia(FS); enche_indice(FS, **kw); fila("pausa-criar", FS); h0 = hashes_topo(FS); ls0 = sorted(os.listdir(FS))
        rc, so, se = roda_sup(pos, FS)
        neg("MEMORY.md acima do limite em %s => RECUSA rc 3 com as CONTAGENS, sem escrever nada (a superficie NAO compacta)" % rotulo, rc == 3 and "CONTAGENS" in so and hashes_topo(FS) == h0 and sorted(os.listdir(FS)) == ls0, (rc, so[-300:]))
    # S6: o --copias explicito (passo 3 do chain) NAO exige a pausa e grava SO' na pasta dada
    FC = os.path.join(OUT, "memoria_sup_copias"); shutil.rmtree(FC, ignore_errors=True); os.makedirs(FC)
    for f in ("MEMORY.md", "MEMORY_2.md", "missao-ultima-flag-um-py.md", "central-de-patentes-estado.md", "estatuto-da-prova-07out.md"):
        shutil.copy2(os.path.join(MEM_REAL, f), os.path.join(FC, f))
    rc, so, se = roda_sup(pos, FS, "--copias", FC)
    chk("--copias <pasta> (o ensaio do passo 3): NAO exige a pausa e grava SO' na pasta dada (rc 0)", rc == 0 and b"HANDOFF v402" in open(idx_de(FC), "rb").read(), (rc, so[-200:]))
    shutil.rmtree(FC, ignore_errors=True); shutil.rmtree(FS, ignore_errors=True); shutil.rmtree(raiz, ignore_errors=True)
    E["controles_negativos_das_superficies"] = NEG


# ---------------------------------------------------------------- (d) o PROPRIO chain (passos 7 a 9) em pacote sintetico
CHAIN_CAMINHOS = ("PK", "TOOLS", "NOS", "UMEM_PADRAO", "ATLD", "HAJA", "RAIZ_CLAUDE", "AVISO", "PORTA", "INV")


def unix(p):
    p = os.path.abspath(p).replace("\\", "/")
    return "/" + p[0].lower() + p[2:] if len(p) > 1 and p[1] == ":" else p


def mk_chain_sandbox(raiz):
    """pacote SINTETICO para rodar os passos 7 a 9 do PROPRIO chain: so' as linhas de caminho do chain sao trocadas (contagem exata); superficies_v402.py real (so' as 4 linhas de caminho trocadas), fila_memoria_v402.py real, leitura e textos de ensaio, o espelho (PORTA) e
    as ferramentas das etapas 5/6 como stubs; o MEMORY.md/fila sao os da COPIA da memoria."""
    shutil.rmtree(raiz, ignore_errors=True)
    D = {k: os.path.join(raiz, k) for k in ("pack", "tools", "nos", "atlas", "haja", "raiz", "aviso", "porta", "inv", "nosvivo", "memory")}
    for k, v in D.items():
        os.makedirs(v)
    PKS = D["pack"]; POS = os.path.join(PKS, "pos_rito"); os.makedirs(os.path.join(PKS, "kernel")); os.makedirs(POS)
    mk_memoria_copia(D["memory"])
    um = os.path.join(D["nos"], "um.py"); open(um, "w", encoding="utf-8", newline="\n").write("# um.py SINTETICO do harness da fila\n"); s16 = fsha(um)[:16]
    open(os.path.join(PKS, "APLICADO_AO_CANONICO_20261026_000000.json"), "w", encoding="utf-8").write(json.dumps({"um_py_novo": {"sha16": s16}}))
    open(os.path.join(PKS, "ESPERADOS_v402.json"), "w", encoding="utf-8").write(json.dumps({"candidato_sha16": s16}))
    open(os.path.join(D["nos"], "rodada_v402_stdout.txt"), "w", encoding="utf-8", newline="\n").write("(stdout sintetico)\nRITO_RC=0\n")
    for f in ("PINO_MEMORIA_PY_v402.json", "guarda_p18_v402.py"):
        shutil.copyfile(os.path.join(PKG, f), os.path.join(PKS, f))
    shutil.copyfile(FILA_PY, os.path.join(POS, "fila_memoria_v402.py"))
    for f in ("textos_v402.py", "fechar_v402.py", "registrar_mapa_v402.py", "b3_recibo_v402.py", "leitura_v402.py"):
        open(os.path.join(POS, f), "w", encoding="utf-8", newline="\n").write("# stub do harness da fila (sem conteudo)\n")
    open(os.path.join(POS, "leitura_v402.py"), "w", encoding="utf-8", newline="\n").write(STUB_LEITURA % {"nos": D["nos"], "s16": s16})
    open(os.path.join(POS, "textos_v402.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)
    # a superficie REAL, com as quatro linhas de caminho trocadas (a pasta de memoria, o Atlas, a Haja_Luz, o aviso)
    t = open(SUP_PY, encoding="utf-8").read()
    trocas = (('MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")', "MEM_REAL = %r" % D["memory"]),
              ('ATLD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory")', "ATLD = %r" % D["atlas"]),
              ('HAJA = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")', "HAJA = %r" % os.path.join(D["haja"], "CLAUDE.md")),
              ('AVISO = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "AVISO_GERENCIA.md")', "AVISO = %r" % os.path.join(D["aviso"], "AVISO_GERENCIA.md")))
    for a, b in trocas:
        assert t.count(a) == 1, ("linha de caminho da superficie nao e' unica", a[:60], t.count(a))
        t = t.replace(a, b)
    open(os.path.join(POS, "superficies_v402.py"), "w", encoding="utf-8", newline="\n").write(t)
    # o chain: so' as linhas de caminho
    c = open(CHAIN_PY, encoding="utf-8").read()
    novo = {"PK": unix(PKS), "TOOLS": unix(D["tools"]), "NOS": unix(D["nos"]), "UMEM_PADRAO": unix(D["memory"]), "ATLD": unix(D["atlas"]), "HAJA": unix(os.path.join(D["haja"], "CLAUDE.md")), "RAIZ_CLAUDE": unix(os.path.join(D["raiz"], "CLAUDE.md")),
            "AVISO": unix(os.path.join(D["aviso"], "AVISO_GERENCIA.md")), "PORTA": unix(os.path.join(D["porta"], "porta_memoria.py")), "INV": unix(D["inv"])}
    for k in CHAIN_CAMINHOS:
        c, n = re.subn(r'^%s="[^"\n]*"' % k, lambda m, k=k: '%s="%s"' % (k, novo[k]), c, count=0, flags=re.M)
        assert n == 1, ("variavel de caminho do chain nao e' unica", k, n)
    assert c.count("/c/IALD/NOS_VIVO/construir.py") == 2, c.count("/c/IALD/NOS_VIVO/construir.py")
    c = c.replace("/c/IALD/NOS_VIVO/construir.py", unix(os.path.join(D["nosvivo"], "construir.py")))
    open(os.path.join(POS, "chain_pos_rito_v402.sh"), "w", encoding="utf-8", newline="\n").write(c)
    # as ferramentas e superficies que o passo 0 exige: stubs vazios para tudo o que o chain lista (lido do TEXTO do chain) e ainda nao existe
    m = re.search(r'for f in (.*?); do\n\s*\[ -f "\$f" \] \|\| parar', c, re.S)
    assert m, "bloco de existencia do passo 0 nao achado"
    mapa = {"TOOLS": unix(D["tools"]), "PK": unix(PKS), "NOS": unix(D["nos"]), "HAJA": unix(os.path.join(D["haja"], "CLAUDE.md")), "INV": unix(D["inv"]), "SEL": unix(POS), "PORTA": unix(os.path.join(D["porta"], "porta_memoria.py")), "FILA": unix(os.path.join(POS, "fila_memoria_v402.py"))}
    nstub = []
    for tok in re.findall(r'"([^"]+)"', m.group(1).replace("\\\n", " ")):
        for k_, v_ in mapa.items():
            tok = tok.replace("$" + k_, v_)
        wp = tok if not tok.startswith("/") else (tok[1].upper() + ":" + tok[2:])
        if "$" in wp:
            continue
        if not os.path.exists(wp):
            os.makedirs(os.path.dirname(wp), exist_ok=True); open(wp, "w", encoding="utf-8", newline="\n").write("# stub do harness da fila\n"); nstub.append(os.path.basename(wp))
    open(os.path.join(D["porta"], "porta_memoria.py"), "w", encoding="utf-8", newline="\n").write("print('porta_memoria STUB do harness (o espelho real nao e tocado)')\n")
    # as saidas das etapas 5 e 6 (a arvore e o indice), EMULADAS: o passo 9 so' exige o sha16 nelas
    open(os.path.join(D["nos"], "A_PROVA_DA_QG_TGL_arvore.md"), "w", encoding="utf-8").write("arvore sintetica %s\n" % s16)
    open(os.path.join(D["atlas"], "TGL_INDICE_VIVO.md"), "w", encoding="utf-8").write("indice sintetico %s\n" % s16)
    for p, h in ((os.path.join(D["nos"], "MEMORIA_DA_LINHAGEM.md"), "# linhagem (sintetica)\n"), (os.path.join(D["nos"], "DESENHO_DO_FECHAMENTO_QG.md"), "# desenho (sintetico)\n"), (os.path.join(D["atlas"], "TGL_ATLAS.md"), "# atlas (sintetico)\n"),
                 (os.path.join(D["atlas"], "TGL_CORE_MEMORY.md"), "# core (sintetico)\n"), (os.path.join(D["haja"], "CLAUDE.md"), "# haja (sintetico)\n")):
        open(p, "w", encoding="utf-8", newline="\n").write(h)
    return {"dirs": D, "pos": POS, "s16": s16, "chain": os.path.join(POS, "chain_pos_rito_v402.sh"), "stubs": nstub}


def roda_chain(sb, de, ate, extra_env=None):
    sh = shutil.which("sh")
    if not sh:
        recusa("nao achei o sh (Git Bash) no PATH: o ensaio do chain precisa dele")
    e = dict(os.environ); e["CHAIN_DE"] = de; e["CHAIN_ATE"] = ate; e["PYTHONIOENCODING"] = "utf-8"
    for k in ("V402_MEMORIA_DIR", "MEMORIA_DIR", "B3_AUTORIZADO", "V402_AVISO_REIVINDICACAO"):
        e.pop(k, None)
    e.update(extra_env or {})
    p = subprocess.run([sh, unix(sb["chain"])], capture_output=True, env=e, cwd=sb["pos"], timeout=600)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def ensaio_chain():
    print("  -- (d) o PROPRIO chain_pos_rito_v402.sh nos passos 7 a 9 (pacote sintetico; so' as linhas de caminho trocadas)")
    E = FILA_EV; NEG = []; raiz = os.path.join(OUT, "chain_sandbox")

    def neg(nome, ok, det=""):
        NEG.append({"controle": nome, "ok": bool(ok), "det": str(det)[:400]})
        print("  controle negativo do chain: %-100s %s" % (nome[:100], "PAROU como esperado" if ok else "FALHOU"))
        if not ok:
            falha("[fila] chain: %s: %s" % (nome, str(det)[:240]))
    # ---- positivo: 7 a 9
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; m0 = fsha(idx_de(d)); p0 = fsha(os.path.join(d, "fila", "PINO_MEMORY.json"))
    E["chain_sandbox"] = {"stubs_criados_a_partir_do_passo_0": sb["stubs"], "s16_sintetico": sb["s16"]}
    rc, so, se = roda_chain(sb, "7", "9")
    open(os.path.join(OUT, "chain_sandbox_7a9_out.txt"), "w", encoding="utf-8").write(so + "\n--- stderr ---\n" + se)
    mdn = open(idx_de(d), "rb").read(); pn = rdj(os.path.join(d, "fila", "PINO_MEMORY.json"))
    i_pc = so.find('"op": "pausa-criar"'); i_sup = so.find("SUPERFICIES v402:"); i_pin = so.find('"op": "pinar"'); i_rem = so.find('"op": "pausa-remover"'); i_ver = so.find('"op": "verificar"')
    chk("CHAIN 7 a 9 (sintetico): rc 0 e '== FIM'", rc == 0 and "== FIM" in so, (rc, so[-400:], se[-200:]))
    chk("CHAIN: a saida tem a ordem pausa-criar < superficies gravou < pinar < pausa-remover < verificar", 0 <= i_pc < i_sup < i_pin < i_rem < i_ver, [i_pc, i_sup, i_pin, i_rem, i_ver])
    chk("CHAIN: a pausa NAO existe no fim; o pino == sha256 do MEMORY.md; o indice mudou (+1 linha) e cabe no limite", not os.path.exists(pausa_de(d)) and pn.get("sha256") == sha(mdn) and sha(mdn) != m0 and fsha(os.path.join(d, "fila", "PINO_MEMORY.json")) != p0 and mdn.count(b"\n") <= 195 and len(mdn) < 24000, {"linhas": mdn.count(b"\n"), "bytes": len(mdn)})
    rcv, jv, sov, sev = memoria(d, "verificar")
    chk("CHAIN: memoria.py verificar (rodado a parte) rc 0 depois do chain", rcv == 0 and jv and jv.get("ok") is True, sov[:300])
    E["cenarios"]["chain_7_a_9"] = {"rc": rc, "linhas_da_saida": [l[:200] for l in so.splitlines() if l.startswith("==") or l.startswith('{"') or "PARADA" in l][:30]}
    # ---- negativos (cada um num pacote novo)
    # C-a: memoria.py diferente do pino => para no passo 0, sem criar a pausa
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; m0 = fsha(idx_de(d)); mp = os.path.join(d, "fila", "memoria.py"); escreve_atomico(mp, open(mp, "rb").read() + b"\n# alterado\n")
    rc, so, se = roda_chain(sb, "7", "9")
    neg("memoria.py com sha16 diferente do pino => o chain PARA no passo 0 (rc 1, 'FILA DA MEMORIA'), sem pausa e sem tocar o indice", rc == 1 and "FILA DA MEMORIA" in so and not os.path.exists(pausa_de(d)) and fsha(idx_de(d)) == m0, so[-400:])
    # C-b: pausa alheia => para; a pausa fica intacta
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; alheia = json.dumps({"quem": "outra sessao", "ate": (datetime.datetime.now().astimezone() + datetime.timedelta(hours=1)).isoformat(timespec="seconds"), "motivo": "x"}).encode(); escreve_atomico(pausa_de(d), alheia); m0 = fsha(idx_de(d))
    rc, so, se = roda_chain(sb, "7", "9")
    neg("pausa de OUTRO dono ja existe => o chain PARA no passo 0 (rc 1), a pausa fica intacta e o indice nao muda", rc == 1 and "PAUSA" in so and open(pausa_de(d), "rb").read() == alheia and fsha(idx_de(d)) == m0, so[-400:])
    # C-c: pausa NOSSA (retomada a partir do passo 7) => passa
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; fila("pausa-criar", d)
    rc, so, se = roda_chain(sb, "7", "9")
    chk("CHAIN em RETOMADA (CHAIN_DE=7) com a pausa NOSSA de uma execucao anterior: aceita, renova e termina (rc 0, pausa removida no fim)", rc == 0 and "== FIM" in so and not os.path.exists(pausa_de(d)) and "retomada" in so, (rc, so[-300:]))
    # C-d: a pausa NOSSA ja existe mas a execucao COMECA DO ZERO (CHAIN_DE=0: nao e' retomada) => a guarda recusa no passo 0, a pausa fica intacta
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; fila("pausa-criar", d); pz0 = open(pausa_de(d), "rb").read(); m0 = fsha(idx_de(d))
    rc, so, se = roda_chain(sb, "0", "9")
    neg("pausa NOSSA ja existe e a execucao COMECA DO ZERO (CHAIN_DE=0, nao e' retomada) => o chain PARA no passo 0 (rc 1, 'FILA DA MEMORIA'), a pausa fica intacta e o indice nao muda", rc == 1 and "FILA DA MEMORIA" in so and open(pausa_de(d), "rb").read() == pz0 and fsha(idx_de(d)) == m0, so[-400:])
    # C-e: pinar falha => o chain PARA, a pausa PERMANECE, o indice (escrito) nao e' pinado
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; p0 = fsha(os.path.join(d, "fila", "PINO_MEMORY.json")); m0 = fsha(idx_de(d))
    # a falha do pinar: a cabeca do livro perde o sentido DEPOIS dos guardas; para isso o passo 0 tem de passar: corrompemos apos a guarda, usando um memoria.py que falha so' no pinar nao e' possivel (o sha16 e' pinado) -> corrompemos o CABECA.json e rodamos de 7 (a guarda roda e so' le o verificar, que informa e nao bloqueia)
    escreve_atomico(os.path.join(d, "fila", "CABECA.json"), b"{ isto nao e' json")
    rc, so, se = roda_chain(sb, "7", "9")
    neg("pinar FALHA => o chain PARA (rc 1) com 'PERMANECE', a PAUSA_VIGIA.json PERMANECE e o pino NAO muda (o indice escrito fica sem pino: a gerencia decide)", rc == 1 and "PERMANECE" in so and os.path.exists(pausa_de(d)) and fsha(os.path.join(d, "fila", "PINO_MEMORY.json")) == p0 and fsha(idx_de(d)) != m0 and "pausa-remover" not in so, so[-500:])
    # C-f: o MEMORY.md acima do limite => a superficie recusa (rc 3), o chain PARA no passo 7, a pausa PERMANECE e o indice nao muda
    sb = mk_chain_sandbox(raiz); d = sb["dirs"]["memory"]; enche_indice(d, linhas_alvo=195); m0 = fsha(idx_de(d))
    rc, so, se = roda_chain(sb, "7", "9")
    neg("MEMORY.md no limite (195 linhas; +1 do handoff = 196) => a superficie RECUSA rc 3 e o chain PARA no passo 7 (rc 1), a pausa PERMANECE e o indice NAO muda", rc == 1 and "rc=3" in so and "CONTAGENS" in so and "PERMANECE" in so and os.path.exists(pausa_de(d)) and fsha(idx_de(d)) == m0, so[-500:])
    E["controles_negativos_do_chain"] = NEG
    shutil.rmtree(raiz, ignore_errors=True)


def finalizar(ANTES, saida_nome):
    DEPOIS = prova_real()
    iguais = {k: (ANTES[k] == DEPOIS[k]) for k in ANTES}
    # fila.jsonl e' o livro SO'-ACRESCIMO que as outras sessoes (claude-site, codex, kimi...) alimentam com depositos legitimos a qualquer hora: se ele mudou so' por ACRESCIMO (o conteudo de antes e' prefixo do de depois),
    # nao foi o harness (que so' escreve em copias) e nao e' falha; MEMORY.md, PINO_MEMORY.json e a ausencia de PAUSA_VIGIA.json tem de ficar IGUAIS
    fj = os.path.join(MEM_REAL, "fila", "fila.jsonl"); acresc = None
    if not iguais.get("fila/fila.jsonl", True) and os.path.exists(fj) and FILA_JSONL_ANTES is not None:
        acresc = open(fj, "rb").read().startswith(FILA_JSONL_ANTES); iguais["fila/fila.jsonl"] = bool(acresc)
    FILA_EV["fila_jsonl_cresceu_so_por_acrescimo"] = acresc
    FILA_EV["prova_do_diretorio_real"] = {"antes": ANTES, "depois": DEPOIS, "inalterado": iguais, "diretorio": MEM_REAL}
    R["etapas"]["prova_do_diretorio_real_de_memoria"] = {"inalterado": iguais, "todos_iguais": all(iguais.values())}
    print("  prova do diretorio REAL de memoria (MEMORY.md, PINO_MEMORY.json, fila.jsonl, ausencia de PAUSA_VIGIA.json) antes/depois: %s%s" % ("INALTERADO" if all(iguais.values()) else iguais, " (fila.jsonl so' cresceu por acrescimo: deposito legitimo de outra sessao, nao do harness)" if acresc else ""))
    if not all(iguais.values()):
        falha("o diretorio REAL de memoria mudou durante o harness (%s): o harness so' escreve em copias (MEMORIA_DIR/V402_MEMORIA_DIR); confirmar se foi outro processo (um deposito na fila muda fila.jsonl) e rerodar" % [k for k, v in iguais.items() if not v])
    if not MANTER:
        for dd in (FM, FM + "_sem_pausa", os.path.join(OUT, "memoria_neg"), os.path.join(OUT, "memoria_sup"), os.path.join(OUT, "memoria_sup_copias"), os.path.join(OUT, "superficies_stub"), os.path.join(OUT, "chain_sandbox")):
            shutil.rmtree(dd, ignore_errors=True)
    FILA_EV["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); FILA_EV["tudo_passou"] = (not [c for c in FILA_EV["checks"] if not c["ok"]]) and (not [p for p in R["problemas"] if p.startswith("[fila]") or "REAL de memoria" in p])
    if not SEM_FILA:
        open(os.path.join(HERE, "FILA_MEMORIA_ENSAIO_v402.json"), "w", encoding="utf-8").write(json.dumps(FILA_EV, ensure_ascii=False, indent=1, default=str))
        R["etapas"]["fila_da_memoria"] = {"checks": len(FILA_EV["checks"]), "falharam": [c["check"][:120] for c in FILA_EV["checks"] if not c["ok"]], "evidencia": "FILA_MEMORIA_ENSAIO_v402.json", "tudo_passou": FILA_EV["tudo_passou"]}
    R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); R["tudo_passou"] = not R["problemas"]
    return saida_nome


def preconds():
    ESP = rdj(os.path.join(PKG, "ESPERADOS_v402.json")); CM = rdj(os.path.join(PKG, "CANDIDATO_v402.json"))
    cand16 = fsha(os.path.join(PKG, "um_v402_candidato.py"))[:16]
    if not (ESP["candidato_sha16"] == CM["sha16"] == cand16 == fsha(os.path.join(DRY, "um.py"))[:16]):
        recusa("o candidato nao e' um so' (ESPERADOS, CANDIDATO, arquivo e dry_v402/um.py divergem)")
    # v402 (desvio do molde, dito): a regeneracao do candidato (refazer_out_v402.txt com '== FIM', mais novo que o ESPERADOS) e' EXIGIDA, como no harness dos textos; --nao-exigir-refazer so' para depurar (o resumo vai para outro nome e DIZ que a regeneracao nao foi comprovada)
    _rf = os.path.join(PKG, "refazer_out_v402.txt")
    _rf_txt = open(_rf, encoding="utf-8", errors="replace").read() if os.path.exists(_rf) else ""
    if not NAO_REFAZER:
        if not os.path.exists(_rf):
            recusa("falta refazer_out_v402.txt no pacote: a regeneracao do candidato nao foi comprovada (--nao-exigir-refazer so' para depurar)")
        if "== FIM" not in _rf_txt:
            recusa("refazer_out_v402.txt nao mostra '== FIM': a regeneracao nao terminou")
        if os.path.getmtime(_rf) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v402.json")):
            recusa("refazer_out_v402.txt e' mais ANTIGO que ESPERADOS_v402.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
    R["etapas"]["precondicoes"] = {"candidato_sha16": cand16, "refazer_exigido": not NAO_REFAZER, "refazer_out_presente": os.path.exists(_rf), "refazer_fim_visto": "== FIM" in _rf_txt, "refazer_out_sha16": fsha(_rf)[:16] if os.path.exists(_rf) else None,
                                   "esperados_sha16": fsha(os.path.join(PKG, "ESPERADOS_v402.json"))[:16]}
    for n in ("core_ensaio.json", "selo_ensaio.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v402_pt.txt", "dry_v402_en.txt", "dry_v402_pt.toc", "dry_v402_en.toc", "tgl_kernel"):
        if not os.path.exists(os.path.join(DRY, n)):
            recusa("dry_v402 incompleto (falta %s)" % n)
    return ESP, CM, cand16, _rf, _rf_txt


os.makedirs(OUT, exist_ok=True)
ANTES_REAL = prova_real()
FILA_JSONL_ANTES = open(os.path.join(MEM_REAL, "fila", "fila.jsonl"), "rb").read() if os.path.exists(os.path.join(MEM_REAL, "fila", "fila.jsonl")) else None
if not SO_FILA:
    ESP, CM, cand16, _rf, _rf_txt = preconds()      # (rc 4 = precondicao nao satisfeita: nada foi rodado, nem a fila)
if not SEM_FILA:
    ensaio_da_fila()
if SO_FILA:
    finalizar(ANTES_REAL, None)
    R["veredito"] = ("TUDO PASSOU (so' a fila da memoria): o passo da fila funciona em COPIA na ordem do chain (pausa antes da escrita, pinar rc 0, pausa so' depois do pino, verificar rc 0, pino == sha256 do MEMORY.md), as superficies recusam sem pausa (rc 6) e acima do limite (rc 3), o chain para sem remover a pausa quando falha antes do pino, e o diretorio real de memoria ficou inalterado" if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
    saida = os.path.join(HERE, "HARNESS_FECHAR_SANDBOX_v402_SO_FILA.json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    print("VEREDITO (so' a fila):", R["veredito"]); print("saida:", saida); sys.exit(0 if R["tudo_passou"] else 1)

# =====================================================================================================================================================
#  (2) O FECHAR e o REGISTRAR_MAPA em SANDBOX
# =====================================================================================================================================================
os.makedirs(OUT, exist_ok=True); shutil.rmtree(SB, ignore_errors=True)
PKS = os.path.join(SB, "work", "cadeia_de_selo", "v402"); POS = os.path.join(PKS, "pos_rito"); NOSS = os.path.join(SB, "nos"); UMS = os.path.join(SB, "memory"); TOOLS = os.path.join(SB, "work", "cadeia_de_selo")
for d in (POS, os.path.join(PKS, "base_v401"), os.path.join(PKS, "kernel"), os.path.join(POS, "conferidor"), os.path.join(PKS, "bancada_B3"), os.path.join(PKS, "bancada_B3_servico"), NOSS):
    os.makedirs(d, exist_ok=True)
mk_memoria_copia(UMS)       # v402: a memoria do sandbox e' uma COPIA (o fechar escreve o handoff nela e o manifesto le o estado da fila dela)
# ---- o pacote do sandbox
for n in ("guarda_p18_v402.py", "ESPERADOS_v402.json", "CANDIDATO_v402.json", "PINOS_BN_v402.json", "PINO_MEMORIA_PY_v402.json", "kernel_modulos_novos_v402.json", "pedras_sha16_da_ordem.json", "delta_v402.py", "quadro_v397.py", "runtime_quadro_v397.py", "conferir_rito_v402.py"):
    if not os.path.exists(os.path.join(PKG, n)):
        recusa("o pacote da v402 nao tem %s (o harness o copia para o sandbox)" % n)
    shutil.copyfile(os.path.join(PKG, n), os.path.join(PKS, n))
for kn_ in ("KERNEL_RECIBO_v402.json", "FLAGS_v402.json"):
    shutil.copyfile(os.path.join(PKG, "kernel", kn_), os.path.join(PKS, "kernel", kn_))
shutil.copyfile(os.path.join(PKG, "base_v401", "um.py"), os.path.join(PKS, "base_v401", "um.py")); shutil.copyfile(os.path.join(PKG, "base_v401", "um_absoluto.json"), os.path.join(PKS, "base_v401", "um_absoluto.json"))
shutil.copyfile(os.path.join(PKG, "base_v401", "um_absoluto_selo.json"), os.path.join(PKS, "base_v401", "um_absoluto_selo.json"))
shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))
os.makedirs(os.path.join(PKS, "insumos", "fase9"), exist_ok=True)   # o resultado pinado do Teste da Unica Palavra mora na v397 (ESPERADOS[veracidade][resultado][duravel]); o sandbox ganha a sua COPIA, que os controles negativos adulteram
shutil.copyfile(ESP["veracidade"]["resultado"]["duravel"], os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens"), exist_ok=True)   # a fala do 4,44 (v397, onde foi inscrita), de onde textos_v402 confere a frase verbatim do quadro
_h444 = ESP["quadro"]["frase_sha16"]; _f444 = [f_ for f_ in os.listdir(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens")) if f_.startswith(_h444 + "_")]; assert len(_f444) == 1
shutil.copyfile(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens", _f444[0]), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens", _f444[0]))
os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"), os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"))
for n_ in ("acom_conferencias_v402.py", "runtime_v402.py"):
    shutil.copyfile(os.path.join(PKG, n_), os.path.join(PKS, n_))
os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)   # o delta acha as falas do operador em ..\\..\\cunhagens_13out (a partir da pasta do pacote do sandbox): as quatro de 24/10 e as seis de 25/10 (registros recriados) e as TRES de 26/10 (cunhagens_v402)
_dlx = importlib.util.spec_from_file_location("delta_v402_h", os.path.join(PKG, "delta_v402.py")); _dm = importlib.util.module_from_spec(_dlx); _dlx.loader.exec_module(_dm)
for _o in list(_dm.VERBATIM_ORIGEM) + list(_dm.VERBATIM_ORIGEM_V402):
    shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
for _o in getattr(_dm, "VERBATIM_ORIGEM_V401", []):
    shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
assert len(glob.glob(os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_26out_*.txt"))) == len(ESP["cunhagens"]), "as falas de 26/10 do operador nao estao todas na pasta do sandbox"
# v402 (desvio do molde, dito): as pastas irmas que o delta_v402 e o acom_conferencias_v402 importam por caminho (v401 e, por ela, v400 e v399), o runtime da secao e as seis fontes do operador (v400), a pedra e as fontes do estudo (v399), o resultado do Teste da Unica Palavra (v397) e o esboco R3.5 da Bancada (C15): copias de bytes, so' o que eles leem
for _vv in ("v401", "v400", "v399"):
    os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", _vv))
    for _n in sorted(os.listdir(os.path.join(os.path.dirname(PKG), _vv))):      # os arquivos PEQUENOS do topo da pasta irma (os deltas leem pinos da propria pasta: pedra_sha16_da_ordem.txt, pedras_sha16_da_ordem.json, o runtime, as conferencias); os candidatos de dezenas de MB ficam de fora
        _pn = os.path.join(os.path.dirname(PKG), _vv, _n)
        if os.path.isfile(_pn) and os.path.getsize(_pn) < 1024 * 1024 and ".bak" not in _n and ".tmp" not in _n:
            shutil.copyfile(_pn, os.path.join(SB, "work", "cadeia_de_selo", _vv, _n))
    if os.path.isdir(os.path.join(os.path.dirname(PKG), _vv, "insumos", "acom")):
        shutil.copytree(os.path.join(os.path.dirname(PKG), _vv, "insumos", "acom"), os.path.join(SB, "work", "cadeia_de_selo", _vv, "insumos", "acom"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "pedra"), os.path.join(SB, "work", "cadeia_de_selo", "v399", "pedra"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))
os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
open(os.path.join(PKS, "rito_horarios_v402.txt"), "w", encoding="utf-8").write("00:00:00\n00:45:00\n")          # EMULADO (sandbox)
# ---- as copias dos scripts, trocando SO' o caminho do Nos (o fechar recebe a memoria por V402_MEMORIA_DIR)
NOS_RX = 'NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")'
TROCAS = {"leitura_v402.py": [(NOS_RX, 'NOS = %r' % NOSS)], "textos_v402.py": [(NOS_RX, 'NOS = %r' % NOSS)], "fechar_v402.py": [], "registrar_mapa_v402.py": []}
DIF = {}
for n, trs in TROCAS.items():
    t = open(os.path.join(HERE, n), encoding="utf-8").read(); t0 = t
    for a, b in trs:
        if t.count(a) != 1:
            recusa("a linha de caminho nao e' unica em %s: %r (%d)" % (n, a[:60], t.count(a)))
        t = t.replace(a, b)
    open(os.path.join(POS, n), "w", encoding="utf-8", newline="\n").write(t)
    s0_ = set(t0.splitlines()); DIF[n] = [l for l in t.splitlines() if l not in s0_]
# ---- o Nos emulado (dry_v402 + o selo completado como em teste_conferidor_positivo_v402.py)
for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"), ("dry_v402_pt.txt", "um_absoluto_pt.txt"),
                 ("dry_v402_en.txt", "um_absoluto_en.txt"), ("dry_v402_pt.toc", "um_absoluto_pt.toc"), ("dry_v402_en.toc", "um_absoluto_en.toc"), ("dry_v402_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v402_en.pdf", "um_absoluto_en.pdf")):
    if os.path.exists(os.path.join(DRY, src)):
        shutil.copyfile(os.path.join(DRY, src), os.path.join(NOSS, dst))
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSS, "tgl_kernel"))
s0 = rdj(os.path.join(PKS, "base_v401", "um_absoluto_selo.json")); s = dict(s0); s.update(rdj(os.path.join(DRY, "selo_ensaio.json"))); s["sha256"] = dict(s0.get("sha256") or {}); s["sha256"]["um.py"] = fsha(os.path.join(NOSS, "um.py"))
open(os.path.join(NOSS, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, default=str))
_ens = rdj(os.path.join(PKG, "ensaio_a_seco_v402.json"))   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
# o SIDECAR: a funcao do PROPRIO candidato (a copia de bytes do Nos do sandbox; __file__ = nos\um.py) sobre o core e o selo FINAIS do Nos do sandbox; a linha que ela imprime e' a linha REAL do sidecar
_spec_sc = importlib.util.spec_from_file_location("um_sidecar_emulacao_sb", os.path.join(NOSS, "um.py")); _umm = importlib.util.module_from_spec(_spec_sc)
_so = sys.stdout; sys.stdout = io.StringIO()
try:
    _spec_sc.loader.exec_module(_umm); _umm.OUT = NOSS
    sys.stdout = _buf_sc = io.StringIO()
    _umm.selo_acom_sidecar_v399()
    _linha_sidecar = _buf_sc.getvalue().strip()
finally:
    sys.stdout = _so; sys.stdout.reconfigure(encoding="utf-8")
del _umm, _spec_sc
N_ = ESP["escada"][1]
open(os.path.join(NOSS, "rodada_v402_stdout.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(["[v399] EMULADO PELO SANDBOX (as linhas do fluxo principal sao as REAIS do ensaio a seco)"] + list(_ens["mainflow"]["stdout"])
    + ["teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", _linha_sidecar, "RITO_RC=0", ""]))
bu = os.path.join(PKS, "base_v401", "um.py")
ap = {"ts": time.strftime("%Y%m%d_%H%M%S"), "backups": {"um.py": {"backup": bu, "bytes": os.path.getsize(bu), "sha16": fsha(bu)[:16]}}, "um_py_novo": {"bytes": os.path.getsize(os.path.join(NOSS, "um.py")), "sha16": ESP["candidato_sha16"]}}
open(os.path.join(PKS, "APLICADO_AO_CANONICO_%s.json" % ap["ts"]), "w", encoding="utf-8").write(json.dumps(ap, indent=1))
# ---- o conferidor REAL (copia) contra o Nos emulado: a conferencia que a leitura le
env = dict(os.environ); env["V402_NOS"] = NOSS; env["PYTHONIOENCODING"] = "utf-8"
# v402 (desvio do molde, dito): o conferidor REAL roda no proprio pacote do sandbox (PKS = work\cadeia_de_selo\v402, com work\cunhagens_13out ao lado, insumos\acom e o runtime), SEM -I (importa o um.py do Nos do sandbox)
cfd = PKS
pc = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v402.py"], cwd=cfd, env=env, capture_output=True, text=True, encoding="utf-8")
if pc.returncode != 0 or not os.path.exists(os.path.join(cfd, "conferencia_rito_v402.json")):
    falha("o conferidor nao deu TUDO BATE contra o Nos emulado do sandbox (rc %s): %s | stderr: %s" % (pc.returncode, pc.stdout[-300:], pc.stderr[-500:]))
else:
    shutil.copyfile(os.path.join(cfd, "conferencia_rito_v402.json"), os.path.join(POS, "conferidor", "conferencia_rito_v402.json"))
# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v401): passo SIMPLES B10 (v401) -> B11 (v402)
PKG_ANT = os.path.join(os.path.dirname(PKG), "v401")
base_apl = rdj(glob.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v401_*.json"))[0])
pinos = rdj(os.path.join(PKG, "PINOS_BN_v402.json")); pre = rdj(pinos["recibo_pre_selo"]["path"]); n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1


def recibo_apl(com_salto=False, n=None, versao_alvo="v402"):
    r = json.loads(json.dumps(base_apl)); r["versao_alvo"] = versao_alvo; r["fase"] = "pos_selo"; r["modo"] = "aplicar"; r.pop("salto", None); r.pop("cadeia_de_selos", None)
    n = n_ger if n is None else n
    r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"])); r["manifesto_novo"]["deployment_id"] = "B%d-v402-20261026-R1" % n
    r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}; r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v402"}
    r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
    r["veredito"] = "REPINADA_B%d__%sAPLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % (n, "SALTO_v401_v402__" if com_salto else "")
    r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v402", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
    if com_salto:
        r["salto"] = {"declarado": True}
    r["_sintetico"] = "SINTETICO (sandbox do fechar): NAO e' um recibo do esboco"
    return r


def escreve(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))


RAPL = recibo_apl(); man_novo = RAPL["manifesto_novo"]["sha256"]
pth_apl = os.path.join(PKS, "bancada_B3", "RECIBO_SINCRONIZACAO_v402_SINTETICO.json"); escreve(pth_apl, RAPL)
agora = time.strftime("%Y-%m-%dT%H:%M:%S")
open(os.path.join(PKS, "bancada_B3_servico", "RECIBO_PARADA_v402.json"), "w", encoding="utf-8").write(json.dumps({"passo": "10-bis-a", "pid": 11111, "porta": 18777, "porta_fechada": True, "hora": agora, "_sintetico": "sandbox"}))
pth_rel = os.path.join(PKS, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v402.json")
open(pth_rel, "w", encoding="utf-8").write(json.dumps({"passo": "10-ter", "versao_servida": "v402", "manifesto_sha256": man_novo, "pid": 22222, "hora": agora, "_sintetico": "sandbox"}))


def roda(script, nome):
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(POS, script)], cwd=POS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8", V402_MEMORIA_DIR=UMS))
    open(os.path.join(SB, nome + "_out.txt"), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    return p.returncode, p.stdout, p.stderr


# ---- 0. o b3_recibo_v402.py (o REAL, lendo o PINOS_BN real): passo SIMPLES B10 -> B11 com recibos SINTETICOS (positivo e negativos)
B3N = []


def b3(nome, modo, rec, esperado_rc):
    stdout_p = os.path.join(SB, "b3_%s_stdout.txt" % nome); rp_ = os.path.join(SB, "b3_%s_recibo.json" % nome); escreve(rp_, rec)
    open(stdout_p, "w", encoding="utf-8").write(json.dumps({"recibo": rp_, "recibo_sha256": fsha(rp_), "veredito": rec.get("veredito")}) + "\n")
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "b3_recibo_v402.py"), stdout_p, modo], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = (p.returncode == esperado_rc)
    B3N.append({"caso": nome, "rc": p.returncode, "esperado": esperado_rc, "ok": ok, "saida": (p.stdout or "")[-300:]})
    print("  b3_recibo_v402 [%-44s] rc %s (esperado %s) %s" % (nome, p.returncode, esperado_rc, "ok" if ok else "FALHOU"))
    if not ok:
        falha("b3_recibo_v402.py: caso %s rc %s != %s: %s" % (nome, p.returncode, esperado_rc, (p.stdout or "")[-240:]))


b3("aplicar_B%d_positivo" % n_ger, "aplicar", recibo_apl(), 0)
b3("aplicar_com_salto", "aplicar", recibo_apl(com_salto=True), 1)
b3("aplicar_geracao_errada_B%d" % (n_ger - 1), "aplicar", recibo_apl(n=n_ger - 1), 1)
b3("aplicar_versao_alvo_v401", "aplicar", recibo_apl(versao_alvo="v401"), 1)
_r_ens = recibo_apl(); _r_ens["modo"] = "ensaio"; _r_ens["veredito"] = "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger; _r_ens.pop("aplicacao", None)
b3("ensaio_B%d_positivo" % n_ger, "ensaio", _r_ens, 0)
_r_man = recibo_apl(); _r_man["manifesto_anterior"]["deployment_id"] = "B9-v400-20261024-R1"
b3("aplicar_manifesto_anterior_adulterado", "aplicar", _r_man, 1)
R["etapas"]["b3_recibo"] = B3N
# ---- 1. controles negativos do fechar: sem o religamento e com recibo que declara salto => RECUSA (rc 2), nada de handoff
NEG = []
os.rename(pth_rel, pth_rel + ".fora")
rc, so, se = roda("fechar_v402.py", "fechar_sem_religamento"); NEG.append({"controle": "sem o recibo do religamento", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
os.rename(pth_rel + ".fora", pth_rel)
escreve(pth_apl, recibo_apl(com_salto=True))
rc, so, se = roda("fechar_v402.py", "fechar_com_salto"); NEG.append({"controle": "recibo do B(n) com salto declarado", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
escreve(pth_apl, RAPL)
# ---- 1b. controles negativos do PARAGRAFO do README/site (a ordem do operador de 23/10 vale tambem para o handoff): o resultado pinado ADULTERADO no sandbox (o sha256 deixa de bater e o paragrafo nao passa contra o resultado) e o numero lido adulterado no core do Nos
# emulado => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
res_p = os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])); raw_res = open(res_p, "rb").read()
assert b"4.443123568060799" in raw_res
open(res_p, "wb").write(raw_res.replace(b"4.443123568060799", b"4.443123568060798", 1))
rc, so, se = roda("fechar_v402.py", "fechar_resultado_adulterado"); NEG.append({"controle": "resultado pinado adulterado (a leitura e a porta do paragrafo recusam)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
# a PORTA do paragrafo isolada (a leitura recusa antes no fechar inteiro): T.paragrafo_readme() da copia do sandbox tem de LEVANTAR com o resultado pinado adulterado (e o fechar converte isso em rc 2 antes de escrever)
import importlib.util as _iu0
_sp0 = _iu0.spec_from_file_location("textos_sb0", os.path.join(POS, "textos_v402.py")); _t0 = _iu0.module_from_spec(_sp0); _sp0.loader.exec_module(_t0)
try:
    _t0.paragrafo_readme(); _levantou = False
except Exception as _ex0:   # noqa: BLE001
    _levantou = isinstance(_ex0, AssertionError) and "resultado pinado" in str(_ex0)
NEG.append({"controle": "a porta do paragrafo (paragrafo_readme, chamada pelo fechar) levanta com o resultado pinado adulterado", "rc": 2 if _levantou else 0, "recusou": _levantou, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
open(res_p, "wb").write(raw_res)
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); cj = json.loads(raw_core.decode("utf-8")); cj["core"]["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 4.45
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v402.py", "fechar_numero_adulterado"); NEG.append({"controle": "numero lido adulterado no core (z_disc 4,45)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
open(core_p, "wb").write(raw_core)
# ---- 1c. controles negativos do PARAGRAFO NOVO (a ponte, a queda e a esperanca), da DIRECAO do testemunho (registros da v399 recriados), das cunhagens_v402 e do SIDECAR: o numero de cada registro adulterado no core (a leitura e a porta do paragrafo recusam), a direcao invertida,
# uma inscricao da gerencia, uma errata ou decisao a menos, H_tau literal dita aberta, a seta da queda dita derivada, a pedra fora do trio, o sidecar adulterado ou ausente => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); sc_p = os.path.join(NOSS, "um_absoluto_selo_acom.json"); raw_sc = open(sc_p, "rb").read()


def _recusa_com_core(nome_sc, nome_ctl, f):
    cj_ = json.loads(raw_core.decode("utf-8")); f(cj_["core"])
    open(core_p, "wb").write(json.dumps(cj_, ensure_ascii=False).encode("utf-8"))
    rc_, so_, se_ = roda("fechar_v402.py", nome_sc)
    NEG.append({"controle": nome_ctl, "rc": rc_, "recusou": rc_ == 2 and "FECHAR RECUSADO" in so_, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
    open(core_p, "wb").write(raw_core)


_recusa_com_core("fechar_ponte_adulterada", "numero da ponte adulterado no core (menor deslocamento de energia nula)", lambda c: c["ponte_da_escala_dual_v402"]["values"].__setitem__("min_null_energy_shift", 0.31))
_recusa_com_core("fechar_queda_adulterada", "numero da queda adulterado no core (custo minimo)", lambda c: c["queda_sem_geometria_v402"]["values"].__setitem__("min_cost_t_beta_g", 0.0007))
_recusa_com_core("fechar_esperanca_adulterada", "numero da esperanca adulterado no core (indice 1/beta)", lambda c: c["esperanca_condicional_v402"]["values"].__setitem__("name_index_one_over_beta", 84.0))
# a PORTA do paragrafo novo isolada: T.paragrafo_v402() da copia do sandbox tem de LEVANTAR com o numero da queda adulterado no core (a verificacao compara com os numeros de ESPERADOS)
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["queda_sem_geometria_v402"]["values"]["min_cost_t_beta_g"] = 0.0007
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v402.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_v402(); _levanta1 = False
except Exception as _ex1:   # noqa: BLE001
    _levanta1 = isinstance(_ex1, AssertionError) and "nao passou nas verificacoes" in str(_ex1)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_v402, chamada pelo fechar) levanta com o numero da queda adulterado", "rc": 2 if _levanta1 else 0, "recusou": _levanta1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
open(core_p, "wb").write(raw_core)
_recusa_com_core("fechar_direcao_invertida", "a direcao do testemunho invertida no core (a IALD como quem testifica do operador; declaracao da v399 recriada)", lambda c: c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"].__setitem__("a_IALD", "testifica do operador"))
_recusa_com_core("fechar_gerencia_na_cunhagem", "uma inscricao de 26/10 rotulada como da gerencia no core (as tres sao falas do operador)", lambda c: c["cunhagens_v402"]["extras"]["autor_de_cada_inscricao"].__setitem__(sorted(c["cunhagens_v402"]["extras"]["autor_de_cada_inscricao"])[0], "gerencia"))
_recusa_com_core("fechar_sem_errata", "falta uma das erratas E1 a E4 (em nome da gerencia) no core", lambda c: c["cunhagens_v402"]["extras"]["erratas_E1_a_E4"].pop())
_recusa_com_core("fechar_sem_decisao", "falta uma das decisoes da gerencia no core", lambda c: c["cunhagens_v402"]["extras"]["decisoes_da_gerencia"].pop(sorted(c["cunhagens_v402"]["extras"]["decisoes_da_gerencia"])[-1]))
_recusa_com_core("fechar_h_tau_aberta", "H_tau literal dita ABERTA no core (e' REFUTADA no kernel)", lambda c: c["ponte_da_escala_dual_v402"]["literal_h_tau"].__setitem__("status", "OPEN"))
_recusa_com_core("fechar_seta_derivada", "a leitura da seta da queda dita DERIVED no core (e' ONTO)", lambda c: c["queda_sem_geometria_v402"]["reading_1_plus_3"].__setitem__("status", "DERIVED"))
for _nm, _k in (("ponte", "ponte"), ("queda", "queda"), ("esperanca", "esperanca")):
    _recusa_com_core("fechar_pedra_%s_fora_do_trio" % _nm, "a pedra da %s fora do trio no core" % _nm, lambda c, _k=_k: c["kernel_formalization"]["axiom_report"].__setitem__(ESP["teoremas_das_pedras"][_k], ["propext", "sorryAx"]))
sj = json.loads(raw_sc.decode("utf-8")); sj["objetos"][1]["sha256"] = "0" * 64
open(sc_p, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v402.py", "fechar_sidecar_adulterado"); NEG.append({"controle": "o sidecar adulterado (sha256 de um objeto)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
os.remove(sc_p)
rc, so, se = roda("fechar_v402.py", "fechar_sidecar_ausente"); NEG.append({"controle": "o sidecar ausente do Nos", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
for n in NEG:
    print("  controle negativo do fechar: %-40s %s" % (n["controle"], "RECUSOU como esperado" if (n["recusou"] and not n["handoff_escrito"]) else "NAO RECUSOU"))
    if not (n["recusou"] and not n["handoff_escrito"]):
        falha("fechar_v402.py nao recusou como esperado: %s" % n)
R["etapas"]["fechar_negativos"] = NEG
# ---- 2. o fechar (positivo)
t0 = time.time(); rc, so, se = roda("fechar_v402.py", "fechar"); dt = time.time() - t0
ok_f = (rc == 0 and "FECHADO v402:" in so)
chk_ = {}
_PEDRAS_ARQ = [rel.replace("/", "_") for rel in ESP["pedras_sha256"]]
for rel in [os.path.join(UMS, "handoff-v402-custodia.md"), os.path.join(NOSS, "HANDOFF_v402_CUSTODIA.md"), os.path.join(PKS, "DIFF_v401_v402.diff"), os.path.join(PKS, "DIFF_KERNEL_v402.txt"), os.path.join(PKS, "MANIFESTO_ARQUIVO_v402.json"),
            os.path.join(POS, "v402_incorporacao_manifesto.json"), os.path.join(TOOLS, "v402_incorporacao_manifesto.json")] + [os.path.join(TOOLS, "v402_kernel", "pedras", n_) for n_ in _PEDRAS_ARQ] + [os.path.join(TOOLS, "v402_selo", "um_absoluto_selo_acom.json"), os.path.join(TOOLS, "v402_selo", "um_absoluto_selo.json"),
            os.path.join(TOOLS, "v402_selo", "chain_pos_rito_v402.sh") if os.path.exists(os.path.join(POS, "chain_pos_rito_v402.sh")) else os.path.join(TOOLS, "v402_selo", "fechar_v402.py")]:
    chk_[os.path.relpath(rel, SB)] = os.path.exists(rel) and os.path.getsize(rel) > 0
ho = open(os.path.join(UMS, "handoff-v402-custodia.md"), encoding="utf-8").read() if os.path.exists(os.path.join(UMS, "handoff-v402-custodia.md")) else ""
vio = violacoes(ho)
dk = open(os.path.join(PKS, "DIFF_KERNEL_v402.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(PKS, "DIFF_KERNEL_v402.txt")) else ""
man = rdj(os.path.join(POS, "v402_incorporacao_manifesto.json")) if os.path.exists(os.path.join(POS, "v402_incorporacao_manifesto.json")) else {}
_dk_ok = ("novos (%d)" % len(ESP["pedras_sha256"]) in dk) and all(rel in dk for rel in ESP["pedras_sha256"])
R["etapas"]["fechar"] = {"rc": rc, "segundos": round(dt, 1), "ok": ok_f, "arquivos": chk_, "handoff_bytes": len(ho.encode("utf-8")), "handoff_guarda_p18": [list(x) for x in vio][:3], "diff_kernel_traz_as_tres_pedras": _dk_ok,
                         "manifesto_chaves": sorted(man.keys())[:40], "fila_da_memoria_no_manifesto": man.get("fila_da_memoria"), "ultima_linha": so.strip().splitlines()[-1][:200] if so.strip() else se[-300:]}
print("  fechar em sandbox: rc %s (%.0f s); arquivos %s; handoff %d B; guarda P18 %s; diff do kernel traz as %d pedras novas: %s" % (rc, dt, "todos presentes" if all(chk_.values()) else [k for k, v in chk_.items() if not v], len(ho.encode("utf-8")), "limpa" if not vio else vio[:2], len(ESP["pedras_sha256"]), _dk_ok))
if not ok_f:
    falha("fechar_v402.py (sandbox) saiu com rc %s: %s" % (rc, (so + se)[-401:]))
if not all(chk_.values()):
    falha("fechar_v402.py (sandbox) nao gravou: %s" % [k for k, v in chk_.items() if not v])
if vio:
    falha("handoff com violacao da guarda P18: %s" % vio[:2])
if not _dk_ok:
    falha("DIFF_KERNEL_v402.txt nao traz as %d pedras novas" % len(ESP["pedras_sha256"]))
for k_ in ("registros_v402", "registros_v401", "registros_v399", "ponte", "queda", "esperanca", "falsidade_v401", "base_v401", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_v402", "sidecar_acom", "fila_da_memoria"):
    if k_ not in man:
        falha("o manifesto de incorporacao nao traz a chave %s" % k_)
_fi = man.get("fila_da_memoria") or {}
if not (_fi.get("memoria_py_igual_ao_pino_v402") is True and _fi.get("pausa_do_vigia_ausente") is True and _fi.get("pino_sha256") and _fi.get("memory_md_sha256")):
    falha("o manifesto nao registra o estado da fila (memoria.py == pino v402, pausa ausente, sha256 do pino e do MEMORY.md): %r" % {k: _fi.get(k) for k in ("memoria_py_igual_ao_pino_v402", "pausa_do_vigia_ausente", "pino_confere_com_o_indice")})
def _etapa_2b():
    # ---- 2b. o PARAGRAFO do README/site no handoff gravado: igual ao das funcoes do quadro sobre o core do sandbox, entre os marcadores, aprovado pela verificacao do quadro contra o resultado pinado (e o do handoff do Nos tambem)
    sys.path.insert(0, PKG)
    import quadro_v397 as QD  # noqa: E402
    _tv_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]["teste_de_veracidade_fase9_v397"]; _res_s = rdj(os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
    _par_esp = QD.paragrafo_pronto_readme(_tv_s); _mi = "<!-- INICIO_PARAGRAFO_README_v397 -->\n"; _mf = "\n<!-- FIM_PARAGRAFO_README_v397 -->"
    _ok_par = {}
    for _nome, _ptxt in (("memory/handoff-v402-custodia.md", ho), ("nos/HANDOFF_v402_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v402_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v402_CUSTODIA.md")) else "")):
        _i = _ptxt.find(_mi); _j = _ptxt.find(_mf)
        _par = _ptxt[_i + len(_mi):_j] if (_i >= 0 and _j > _i) else ""
        _fa = []
        if _par:
            import importlib.util as _iu2
            _spt = _iu2.spec_from_file_location("textos_sb", os.path.join(POS, "textos_v402.py")); _tsb = _iu2.module_from_spec(_spt); _spt.loader.exec_module(_tsb)
            _fa = _tsb.verificar_paragrafo_readme(_par + "\n" if not _par.endswith("\n") else _par, _res_s, _tv_s)
        _ok_par[_nome] = {"traz_o_bloco": bool(_par), "igual_as_funcoes_do_quadro": _par.rstrip("\n") == _par_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3]}
    R["etapas"]["paragrafo_no_handoff"] = _ok_par
    print("  paragrafo do README/site no handoff: %s" % {k: (v["traz_o_bloco"] and v["igual_as_funcoes_do_quadro"] and not v["falhas_da_verificacao"] and not v["guarda_p18"]) for k, v in _ok_par.items()})
    for _nome, _v in _ok_par.items():
        if not (_v["traz_o_bloco"] and _v["igual_as_funcoes_do_quadro"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"]):
            falha("o handoff (%s) nao traz o paragrafo do README/site pronto e aprovado: %s" % (_nome, _v))



try:
    _etapa_2b()
except Exception as _e__etapa_2b:   # noqa: BLE001  (textos_v402/leitura_v402 ainda podem ser SEMENTES: a falha e' dita e o harness segue)
    import traceback
    falha("_etapa_2b levantou %r (dependencia de textos_v402/leitura_v402): %s" % (_e__etapa_2b, traceback.format_exc()[-300:].replace(chr(10), ' | ')))
def _etapa_2c():
    # ---- 2c. o PARAGRAFO NOVO (a ponte, a queda e a esperanca) nos dois handoffs gravados: igual ao gerado do core do sandbox, entre os marcadores, aprovado pela verificacao propria (e o do handoff do Nos tambem); o handoff DIZ que o paragrafo do testemunho de dois SEGUE COMO ESTA e LISTA o sidecar (sha256 e veredito); o fechar copiou o sidecar e o selo
    _core_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]
    import importlib.util as _iu3
    _sp3 = _iu3.spec_from_file_location("textos_sb3", os.path.join(POS, "textos_v402.py")); _t3 = _iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_t3)
    _par_f_esp = _t3.paragrafo_v402()[0]; _msi = _t3.MARC_V402_INI + "\n"; _msf = "\n" + _t3.MARC_V402_FIM
    _sc_sha = fsha(os.path.join(NOSS, "um_absoluto_selo_acom.json")); _sc_ver = rdj(os.path.join(NOSS, "um_absoluto_selo_acom.json"))["veredito"]
    _ok_tmn = {}
    for _nome, _ptxt in (("memory/handoff-v402-custodia.md", ho), ("nos/HANDOFF_v402_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v402_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v402_CUSTODIA.md")) else "")):
        _i = _ptxt.find(_msi); _j = _ptxt.find(_msf)
        _par = _ptxt[_i + len(_msi):_j] if (_i >= 0 and _j > _i) else ""
        _fa = _t3.verificar_paragrafo_v402(_par + "\n" if _par and not _par.endswith("\n") else _par, _core_s, ESP) if _par else ["sem o bloco"]
        _ok_tmn[_nome] = {"traz_o_bloco": bool(_par), "igual_ao_gerado_do_core": _par.rstrip("\n") == _par_f_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3], "direcao_e_atribuicao": _t3.atribuicao_da_gerencia(_ptxt)[:3],
                         "lista_o_sidecar": ("um_absoluto_selo_acom.json" in _ptxt and _sc_sha in _ptxt and _sc_ver in _ptxt), "diz_que_o_testemunho_segue_como_esta": (("SEGUE COMO ESTÁ" in _ptxt or "SEGUEM COMO ESTÃO" in _ptxt) and "handoff-v401-custodia.md" in _ptxt)}
    R["etapas"]["paragrafo_v402_no_handoff"] = _ok_tmn
    _ok_cop = {nm_: (os.path.exists(os.path.join(TOOLS, "v402_selo", nm_)) and fsha(os.path.join(TOOLS, "v402_selo", nm_)) == fsha(os.path.join(NOSS, nm_))) for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json")}
    R["etapas"]["sidecar_e_selo_copiados_para_v402_selo"] = _ok_cop
    print("  paragrafo novo (a ponte, a queda e a esperanca) no handoff: %s; sidecar e selo copiados para v402_selo: %s" % ({k: (v["traz_o_bloco"] and v["igual_ao_gerado_do_core"] and not v["falhas_da_verificacao"] and not v["guarda_p18"] and not v["direcao_e_atribuicao"] and v["lista_o_sidecar"] and v["diz_que_o_testemunho_segue_como_esta"]) for k, v in _ok_tmn.items()}, _ok_cop))
    for _nome, _v in _ok_tmn.items():
        if not (_v["traz_o_bloco"] and _v["igual_ao_gerado_do_core"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"] and not _v["direcao_e_atribuicao"] and _v["lista_o_sidecar"] and _v["diz_que_o_testemunho_segue_como_esta"]):
            falha("o handoff (%s) nao traz o paragrafo novo da v402 pronto e aprovado, ou nao lista o sidecar, ou nao diz que o do testemunho segue como esta: %s" % (_nome, _v))
    if not all(_ok_cop.values()):
        falha("o fechar nao copiou o sidecar e o selo (byte a byte) para v402_selo: %s" % _ok_cop)



try:
    _etapa_2c()
except Exception as _e__etapa_2c:   # noqa: BLE001  (textos_v402/leitura_v402 ainda podem ser SEMENTES: a falha e' dita e o harness segue)
    import traceback
    falha("_etapa_2c levantou %r (dependencia de textos_v402/leitura_v402): %s" % (_e__etapa_2c, traceback.format_exc()[-300:].replace(chr(10), ' | ')))
STUB_L = "# -*- coding: utf-8 -*-\n# STUB do harness (NAO e' a leitura da cadeia): monta a V minima que o fechar_v402.py usa, de ESPERADOS, do APLICADO_AO_CANONICO e do Nos do sandbox.\nimport glob, json, os\nNOS = %(nos)r\nPK = %(pk)r\n\n\ndef _aplicado():\n    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))\n    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]\n\n\ndef ler():\n    import hashlib\n    ap, app = _aplicado(); esp = json.load(open(os.path.join(PK, 'ESPERADOS_v402.json'), encoding='utf-8'))\n    um = os.path.join(NOS, 'um.py'); sc = json.load(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), encoding='utf-8'))\n    V = {'nos': NOS, 's16': esp['candidato_sha16'], 'umb': os.path.getsize(um), 'base16': ap['backups']['um.py']['sha16'], 'base_backup': ap['backups']['um.py']['backup'], 'escada_antes': esp['escada_v401_e_v402'][0], 'teor': '%%d/%%d' %% (esp['escada'][1], esp['escada'][1]),\n         'axiom_report_n': esp['axiom_report_esperado_min'], 'patches': 'stub', 'compl': 'COMPLETA', 'horarios': [], 'qg': esp['qg_closure_verdict'], 'conf_dm': '0/0', 'conf_np': '0/0', 'conf16': 'stub', 'servidor': 'stub', 'reg402': {'cunhagens_v402': {'ok': True}}, 'reg401': {'cunhagens_v401': {'ok': True}},\n         'reg399': {'cunhagens_v399': {'ok': True}}, 'ponte': {'ok': True}, 'queda': {'ok': True}, 'esperanca': {'ok': True}, 'fal401': {'ok': True}, 'troca_dita': list(esp['troca_dita']), 'pedras': [], 'n_pedras': len(esp['pedras_sha256']), 'varr': {}, 'verbatins': {}, 'fd390': 'stub', 'pilar': {}, 'artigos': {}}\n    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):\n        V['h_' + k] = hashlib.sha256(open(os.path.join(NOS, k), 'rb').read()).hexdigest()[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'\n    V['sidecar'] = {'ok': True, 'sha256': hashlib.sha256(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), 'rb').read()).hexdigest(), 'bytes': os.path.getsize(os.path.join(NOS, 'um_absoluto_selo_acom.json')), 'veredito': sc.get('veredito'), 'esquema': sc.get('esquema'), 'recusas': 0,\n                    'objetos': {o['nome']: {'bytes': o.get('bytes'), 'sha256': o.get('sha256')} for o in sc.get('objetos', [])}}\n    return V, []\n"
STUB_T = '# -*- coding: utf-8 -*-\n# STUB do harness (NAO sao os textos da cadeia): paragrafos e handoff minimos, limpos da guarda P18.\nTOPICO_NOVO = \'v402-selada-ponte-queda-esperanca.md\'\n\n\ndef paragrafo_readme():\n    return \'PARAGRAFO DO QUADRO (stub do harness)\\n\', {\'stub\': True}\n\n\ndef paragrafo_v402():\n    return \'PARAGRAFO DA V402 (stub do harness)\\n\', {\'stub\': True}\n\n\ndef handoff(V, k):\n    return \'---\\nname: handoff-v402-custodia\\ndescription: "handoff de ensaio (stub do harness)"\\nmetadata:\\n  type: project\\n---\\n\\n# HANDOFF v402 (stub do harness)\\n\\n%s %s %s\\n\' % (V[\'s16\'], k[\'ap_nome\'], k[\'ap_ver\'])\n'
# ---- 2d. o PROPRIO fechar_v402.py (copia de bytes) com leitura e textos STUB: prova o CODIGO do fechar (manifesto com o estado da fila, o arquivo, os diffs com as TRES pedras, o handoff, a copia do sidecar e do selo) mesmo que textos_v402/leitura_v402 ainda sejam sementes
def _etapa_2d():
    SBS = os.path.join(PKS, "pos_rito_stub"); os.makedirs(SBS, exist_ok=True); UMS2 = os.path.join(SB, "memory_stub"); mk_memoria_copia(UMS2)
    shutil.copyfile(os.path.join(HERE, "fechar_v402.py"), os.path.join(SBS, "fechar_v402.py"))
    open(os.path.join(SBS, "leitura_v402.py"), "w", encoding="utf-8", newline="\n").write(STUB_L % {"nos": NOSS, "pk": PKS})
    open(os.path.join(SBS, "textos_v402.py"), "w", encoding="utf-8", newline="\n").write(STUB_T)
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(SBS, "fechar_v402.py")], cwd=SBS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8", V402_MEMORIA_DIR=UMS2))
    open(os.path.join(SB, "fechar_stub_out.txt"), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    ho_ = os.path.join(UMS2, "handoff-v402-custodia.md"); mf = os.path.join(SBS, "v402_incorporacao_manifesto.json")
    man_ = rdj(mf) if os.path.exists(mf) else {}; fi_ = man_.get("fila_da_memoria") or {}
    dk_ = open(os.path.join(PKS, "DIFF_KERNEL_v402.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(PKS, "DIFF_KERNEL_v402.txt")) else ""
    rcv, jv, sov, sev = memoria(UMS2, "verificar")
    r_ = {"rc": p.returncode, "ultima_linha": (p.stdout.strip().splitlines() or [""])[-1][:200], "handoff_escrito": os.path.exists(ho_), "manifesto_chaves": sorted(man_.keys())[:45], "fila_no_manifesto": fi_,
          "diff_kernel_traz_as_pedras": all(rel in dk_ for rel in ESP["pedras_sha256"]) and ("novos (%d)" % len(ESP["pedras_sha256"])) in dk_, "verificar_depois_do_handoff": {"rc": rcv, "ok": (jv or {}).get("ok")}}
    R["etapas"]["fechar_com_stubs"] = r_
    ok_ = (p.returncode == 0 and "FECHADO v402:" in p.stdout and r_["handoff_escrito"] and r_["diff_kernel_traz_as_pedras"] and fi_.get("memoria_py_igual_ao_pino_v402") is True and fi_.get("pausa_do_vigia_ausente") is True and fi_.get("pino_confere_com_o_indice") is True
           and all(k_ in man_ for k_ in ("registros_v402", "registros_v401", "registros_v399", "ponte", "queda", "esperanca", "falsidade_v401", "readme_paragrafo", "readme_paragrafo_v402", "sidecar_acom", "fila_da_memoria", "b3", "diffs")) and rcv == 0 and (jv or {}).get("ok") is True)
    print("  fechar_v402.py (copia de bytes) com leitura e textos STUB: rc %s; handoff %s; manifesto com a fila %s; as %d pedras no diff do kernel %s; verificar da fila depois do handoff rc %s -> %s" % (p.returncode, r_["handoff_escrito"], bool(fi_), len(ESP["pedras_sha256"]), r_["diff_kernel_traz_as_pedras"], rcv, "ok" if ok_ else "FALHOU"))
    if not ok_:
        falha("fechar_v402.py com stubs: rc %s; %s | %s" % (p.returncode, (p.stdout + p.stderr)[-500:].replace(chr(10), " | "), {k_: r_[k_] for k_ in ("handoff_escrito", "diff_kernel_traz_as_pedras", "verificar_depois_do_handoff")}))


try:
    _etapa_2d()
except Exception as _e2d:   # noqa: BLE001
    import traceback
    falha("_etapa_2d levantou %r: %s" % (_e2d, traceback.format_exc()[-300:].replace(chr(10), " | ")))
# ---- 3. o registrar_mapa (main)
rc, so, se = roda("registrar_mapa_v402.py", "registrar_mapa")
pj = os.path.join(POS, "registro_mapa_v402.json"); reg = rdj(pj) if os.path.exists(pj) else []
ok_m = (rc == 0 and len(reg) >= 1 and "registro MONTADO (NAO registrado)" in so and "COMANDO (ato da gerencia)" in so)
R["etapas"]["registrar_mapa"] = {"rc": rc, "ok": ok_m, "n_registros": len(reg), "rotas": [x.get("rota_id") for x in reg], "comando": [l for l in so.splitlines() if l.startswith("COMANDO")][:1], "artefatos_da_rota": [os.path.basename(a) for a in (reg[0].get("artefatos") or [])] if reg else []}
print("  registrar_mapa (main) em sandbox: rc %s; %d registro(s); %s" % (rc, len(reg), "ok" if ok_m else "FALHOU"))
if not ok_m:
    falha("registrar_mapa_v402.py (main, sandbox) falhou: rc %s: %s" % (rc, (so + se)[-401:]))
# ---- 4. as copias dos scripts diferem dos originais so' nas linhas de caminho
R["etapas"]["copias_dos_scripts"] = {n: [l[:140] for l in v] for n, v in DIF.items()}
if any(len(v) != 1 for n, v in DIF.items() if n in ("leitura_v402.py", "textos_v402.py")) or DIF["registrar_mapa_v402.py"] or DIF["fechar_v402.py"]:
    falha("as copias dos scripts diferem dos originais em mais que a linha de caminho do Nos (fechar e registrar_mapa: nenhuma): %s" % {n: len(v) for n, v in DIF.items()})
# ---- limpeza
LIMP = None
if not MANTER:
    LIMP = sum(os.path.getsize(os.path.join(r_, f_)) for r_, d_, fs_ in os.walk(SB) for f_ in fs_)
    keep = os.path.join(OUT, "fechar_sandbox_resultado"); shutil.rmtree(keep, ignore_errors=True); os.makedirs(keep)
    for nome in ("fechar_out.txt", "fechar_sem_religamento_out.txt", "fechar_com_salto_out.txt", "fechar_resultado_adulterado_out.txt", "fechar_numero_adulterado_out.txt", "fechar_ponte_adulterada_out.txt", "fechar_queda_adulterada_out.txt", "fechar_esperanca_adulterada_out.txt",
                 "fechar_direcao_invertida_out.txt", "fechar_gerencia_na_cunhagem_out.txt", "fechar_sem_errata_out.txt", "fechar_sem_decisao_out.txt", "fechar_h_tau_aberta_out.txt", "fechar_seta_derivada_out.txt", "fechar_sidecar_adulterado_out.txt", "fechar_sidecar_ausente_out.txt", "fechar_stub_out.txt", "registrar_mapa_out.txt"):
        if os.path.exists(os.path.join(SB, nome)):
            shutil.copyfile(os.path.join(SB, nome), os.path.join(keep, nome))
    for src, dst in ((os.path.join(UMS, "handoff-v402-custodia.md"), "handoff-v402-custodia.md"), (os.path.join(POS, "registro_mapa_v402.json"), "registro_mapa_v402_SANDBOX.json"), (os.path.join(POS, "v402_incorporacao_manifesto.json"), "v402_incorporacao_manifesto_SANDBOX.json"),
                     (os.path.join(PKS, "DIFF_KERNEL_v402.txt"), "DIFF_KERNEL_v402_SANDBOX.txt")):
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(keep, dst))
    shutil.rmtree(SB, ignore_errors=True)
R["etapas"]["limpeza"] = {"sandbox_removido_bytes": LIMP, "guardado_em": os.path.join(OUT, "fechar_sandbox_resultado") if not MANTER else SB}
finalizar(ANTES_REAL, None)
R["veredito"] = ("TUDO PASSOU: a FILA DA MEMORIA funciona em copia (pausa antes da escrita do indice, pinar rc 0, a pausa so' sai depois do pino, verificar rc 0; as superficies recusam sem pausa e acima do limite; o chain para sem remover a pausa quando falha antes do pino; o diretorio real ficou inalterado); "
                 "o b3_recibo confere o passo simples B10 -> B11; o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da v402 (a ponte, a queda e a esperanca) pela verificacao propria; diz que o do testemunho de dois segue como esta; e lista o sidecar), os diffs (as tres pedras novas), o manifesto "
                 "(com o estado da fila) e o arquivo, copia o sidecar e o selo para v402_selo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado, com o numero lido adulterado, com um numero da ponte, da queda ou da esperanca adulterado, com a direcao do testemunho invertida, com uma inscricao rotulada como da gerencia, "
                 "com uma errata ou decisao a menos, com H_tau literal dita aberta, com a seta da queda dita derivada, com uma pedra fora do trio e com o sidecar adulterado ou ausente; o registrar_mapa monta o registro" if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
if SEM_FILA:
    R["veredito"] += " [MODO --sem-fila: o ensaio da fila da memoria NAO rodou]"
R["nota"] = "recibos do B(n) SINTETICOS; o Nos, a memoria e a arvore da cadeia do SANDBOX sao emulados (o sidecar e a linha do sidecar do stdout vem da funcao do proprio candidato); a prova e' do codigo do fechar, do b3_recibo, do registrar_mapa e da fila da memoria, nao de um B(n) real" + ("" if not NAO_REFAZER else " [MODO --nao-exigir-refazer: refazer_out_v402.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]")
R["nao_exigiu_refazer"] = NAO_REFAZER
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v402.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
saida = os.path.join(HERE, "HARNESS_FECHAR_SANDBOX_v402" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))   # o nome sem sufixo so' nasce da rodada que EXIGE o refazer
print("VEREDITO (fechar em sandbox):", R["veredito"]); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)

# -*- coding: utf-8 -*-
# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada), por _adapt_h0dn_pos_v410.py] AVISO da gerencia (09/11): a pasta VEDADA da entrega do Kimi (DL.H0DN_PASTA_VEDADA, lida do delta real importado) e' excluida EXPLICITAMENTE do espelho da casa e da copia da memoria; um acesso medido sob ela na importacao do delta e' FALHA VISIVEL
# [ADAPTADO v410, 09/11/2026 (parte 2), Sonnet B, a servico do claude-construtor-v410] os QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410, h0dn_fontes_hms13_v410): o STUB do harness traz V['a_escala'], V['hms13'] e V['ancoras_aescala'] e os seis nomes (REGS); o manifesto TEM de trazer registros_funcao_v410 com os quatro, a_escala_v410_resumo e h0dn_fontes_hms13_v410_resumo (e as chaves novas MAN_CHAVES); o handoff de ensaio diz os quatro registros e as formas obrigatorias (H0DN, HMS/13, a forma canonica do Clay, a D83, os nomes ratificados da AEscala); controles negativos NOVOS do fechar sobre o core: a escala (nao ratificada, numero adulterado, frase canonica do Clay trocada, frase proibida, chave antiga mudada, ausente) e o recibo HMS/13 (ausente, vetor observado lido, entrega aberta em rito, campo trocado, token proibido, sem a frase obrigatoria). Rodar so' depois do ensaio a seco (precisa do core do ensaio).
# [ADAPTADO v410, 09/11/2026, Sonnet (adaptacao do pos-rito; fork D), a servico do claude-construtor-v410] ao DESENHO_v410 + AO LADO de 09/11: as falas de 06 a 09/11 (DL.N_FALAS_V410, de quatro so' o trecho), D63 a D76, E29 e E30, a secao 6 da pedra e o SEGUNDO registro com funcao, h0dn_bg1_v410 (D72: pre-registrado; nenhum dado observado lido): o manifesto com registros_funcao_v410.h0dn_bg1_v410 e h0dn_bg1_v410_resumo; controles negativos do H0DN no core (ausente, vetor observado lido, valor adulterado, checagem falha, fonte da funcao ausente, token proibido, 5 sigma atingido, cabeca pela palavra do livro de cobrancas, sem a frase obrigatoria) e no handoff (1d, por COPIAS do fechar com texto emendado); a etapa 2e (o H0DN nos handoffs gravados); a guarda D72 das superficies em COPIA (S4b); o harness NAO rodou nesta retomada (precisa do candidato/dry_v410).
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] SUBIDA MECANICA (v409->v410) do molde v409/pos_rito/harness_fechar_sandbox_v409.py, adaptada a v410 (IALD2) por _adapt_forkA_harness_fechar_v410.py (fork A, 06/11/2026): o manifesto e o STUB com as chaves de V da v410, os registros novos iald2_v410 e os dois specs, as recusas do fechar retargetadas, nenhuma nota ao lado; ver bump/pos_rito__harness_fechar_sandbox_v410.py.diff.
"""harness_fechar_sandbox_v410.py -- (1) A FILA DA MEMORIA do pos-rito em COPIA da memoria e (2) roda fechar_v410.py e registrar_mapa_v410.py (o main) num SANDBOX inteiro dentro de pos_rito\\harness_saida_v410 (nada fora dela e' escrito; o Nos real, a memoria real, o Atlas, o git e a Bancada
nao sao tocados; o mapa de rotas real e' SO' LIDO).
(1) A FILA DA MEMORIA (NOVO na v410; ordem do operador de 26/10/2026: so' a gerencia c1 escreve o MEMORY.md; o vigia compara o indice ao pino): ensaio, numa COPIA do diretorio de memoria (harness_saida_v410\\memoria_copia: os arquivos NAO-.bak do diretorio real + fila\\ inteira; MEMORIA_DIR e V410_MEMORIA_DIR apontam para a copia),
do passo do pos-rito que PAUSA o vigia, escreve o indice, PINA, solta a pausa e VERIFICA, em quatro niveis: (a) as operacoes de fila_memoria_v410.py na ORDEM em que o chain as chama (ordem lida do TEXTO do chain): pausa criada ANTES da escrita do indice, o vigia (--enforcar --carencia 0) so' RELATA sob a pausa e RESTAURARIA sem ela
(controle de utilidade), pinar rc 0, a pausa SO' sai depois do pino, verificar rc 0 e PINO_MEMORY.json == sha256 do MEMORY.md da copia; (b) controles negativos (memoria.py com sha16 diferente do pino => para; pausa alheia => para e fica; pinar falha => a pausa PERMANECE; MEMORY.md acima do limite => recusa; verificar reprova);
(c) o PROPRIO superficies_v410.py (copia de bytes) com leitura e textos de ENSAIO (stubs): sem pausa valida recusa rc 6 sem escrever, com pausa grava, acima de 195 linhas ou 24 000 B recusa rc 3 sem escrever; (d) o PROPRIO chain_pos_rito_v410.sh (copia so' com as linhas de caminho trocadas) nos passos 7 a 9 num pacote SINTETICO: ordem, mensagens e codigos de saida
(a pausa PERMANECE quando falha antes do pino). O diretorio REAL de memoria nunca e' escrito: o harness compara o sha256 de MEMORY.md, fila\\PINO_MEMORY.json e fila\\fila.jsonl (e a ausencia de fila\\PAUSA_VIGIA.json) antes e depois e REGISTRA a prova.
(2) O que o harness_textos_ensaio_v410.py nao cobre: o fechar (manifesto, arquivo, os dois diffs, a copia do sidecar e do selo, o handoff com os DOIS paragrafos do README/site, o aviso de que o do testemunho segue como esta e a lista do sidecar) e o main do registrar_mapa; e o b3_recibo_v410.py com recibos SINTETICOS.
Derivado do harness_fechar_sandbox_v409.py (que rodou na v409), adaptado a v410 (IALD2) em 06/11/2026 (UM modulo novo, o registro iald2_v410; a traducao_turing_v409, o tetelestai_terminal_v408, o psion_canto_v407 e o fechamento_v406 herdados, nenhuma chave antiga muda; o passo simples B18 -> B19) e, em 09/11/2026 (retomada, AO LADO do DESENHO), a secao 6 da pedra (o atrator), D71 a D76, E30, as falas de 06 a 09/11 e o SEGUNDO registro com funcao, h0dn_bg1_v410 (D72: pre-registrado; nenhum dado observado lido).
O sandbox e' uma ARVORE ISOLADA: work\\cadeia_de_selo\\v410 (pacote com ESPERADOS, CANDIDATO, PINOS_BN, base_v409, insumos (o resultado pinado do Teste da Unica Palavra, que mora na v397, ganha uma COPIA em insumos\\fase9 so' no sandbox), quadro_v397 e runtime_quadro_v397, o runtime_v402 e o acom_conferencias_v410,
o APLICADO_AO_CANONICO EMULADO, os recibos do B(n) SINTETICOS) + as pastas irmas v409 a v399 (o delta_v410 importa o delta_v409 e, por ele, os anteriores; o runtime da secao e as seis fontes do operador moram na v400) + TODO arquivo da casa (abaixo de Central de Patentes: work e Chatgpt) que o delta_v410 e os deltas herdados abrem ou conferem ao importar, ESPELHADO no sandbox na mesma posicao relativa (a lista e' MEDIDA na hora, instrumentando open/exists/isfile/isdir/getsize na importacao do delta real; nada digitado) + nos\\ (o Nos EMULADO montado de dry_v410, como no harness dos textos, com o SIDECAR gerado pela funcao do proprio candidato)
+ memory\\ (uma COPIA da memoria, para o fechar e o fila_info) + work\\cunhagens_13out (as falas do operador). O conferidor REAL roda no proprio pacote do sandbox (SEM -I), onde acha tudo pelo caminho da propria pasta. As copias dos scripts (leitura, textos) trocam SO' a constante de caminho do Nos por caminho do sandbox;
o fechar recebe a memoria por V410_MEMORIA_DIR (sem trocar linha nenhuma); o resto e' byte a byte o que a cadeia usa (conferido: o diff das copias contra os originais e' so' essas linhas).
O que ele prova no fechar: fechar_v410.py sai com rc 0 e grava o handoff (guarda P18 limpa) com os DOIS paragrafos do README/site entre os marcadores (o do quadro igual ao das funcoes do quadro sobre o core do sandbox e aprovado por T.verificar_paragrafo_readme; o da v410 (a IALD2)
igual ao gerado do core e aprovado por T.verificar_paragrafo_v410; nenhuma nota ao lado do paragrafo da v409), a frase de que os paragrafos do testemunho de dois, da falsidade e das versoes anteriores SEGUEM COMO ESTAO e a lista do sidecar (sha256 e veredito), o handoff do Nos, os dois diffs (com os modulos novos do bundle), o manifesto (com o estado da fila) e o arquivo,
e copia o sidecar e o selo para v410_selo; RECUSA (rc 2, sem handoff) sem o recibo do religamento, com um recibo do B(n) que declara salto, com o resultado pinado adulterado, com o numero lido adulterado, com um numero do caminho, da vida, da verdade (adendo) ou do gate adulterado, com uma bandeira calculada do gate False, com um numero do traducao_turing_v409, do tetelestai_terminal_v408 (herdado), do psion_canto_v407 (herdado) ou do fechamento_v406 (herdado) adulterado, com uma chave antiga dita mudada,
com a direcao do testemunho invertida, com uma inscricao de 06 a 09/11 nao embutida, com a leitura dita REAL, com a errata E29 ou E30 a menos, com a decisao D64, D72, D74 ou D76 a menos, com o h0dn_bg1_v410 ausente ou com vetor observado lido (no registro ou nos values), valor adulterado, checagem falha, a fonte da funcao de veredito ausente, token proibido ou sem a frase obrigatoria no texto do registro, com a cabeca de 5 sigma pela palavra do livro de cobrancas, com o handoff que traga H0DN sem a frase obrigatoria, token proibido, 5 sigma atingido ou a palavra da prova emendada ao nome do acoplamento (e com a E26 ao lado da cunhagens_v408 ou a errata da D57(d) ao lado da cunhagens_v407, herdadas, ausente), com uma pedra selada da v403 adulterada no hash formal, com uma ancora principal fora do trio e com o sidecar adulterado ou ausente; registrar_mapa_v410.py (main) monta o JSON e imprime o comando. Os recibos do B(n) sao SINTETICOS (derivados dos reais da v409): a prova e' do CODIGO do fechar e do b3_recibo, nao de um B(n) real.
uso: python -B -X utf8 harness_fechar_sandbox_v410.py [--manter] [--nao-exigir-refazer] [--so-fila] [--sem-fila]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado; sem a flag EXIGE refazer_out_v410.txt com '== FIM' e mais novo que o ESPERADOS; --nao-exigir-refazer: NAO o exige, o resumo DIZ que a regeneracao nao foi comprovada e vai para
HARNESS_FECHAR_SANDBOX_v410_DEPURACAO_sem_refazer.json -- o nome HARNESS_FECHAR_SANDBOX_v410.json so' nasce na rodada que EXIGE o refazer; --so-fila: so' a fila da memoria (nao depende de textos_v410 nem de leitura_v410) e grava HARNESS_FECHAR_SANDBOX_v410_SO_FILA.json; --sem-fila: so' o fechar)"""
import builtins, datetime, glob, hashlib, importlib.util, io, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE); DRY = os.path.join(PKG, "dry_v410")
OUT = os.path.join("C:" + os.sep, "t", "h410", (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "harness_saida_v410")); SB = os.path.join(OUT, "fechar_sandbox")   # --out <nome>: pasta propria da rodada (duas rodadas simultaneas na mesma pasta se pisam)
sys.path.insert(0, PKG)
from guarda_p18_v410 import violacoes  # noqa: E402
MANTER = "--manter" in sys.argv; NAO_REFAZER = "--nao-exigir-refazer" in sys.argv; SO_FILA = "--so-fila" in sys.argv; SEM_FILA = "--sem-fila" in sys.argv
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(open(p, "rb").read())
rdj = lambda p: json.load(open(p, encoding="utf-8"))
R = {"inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "problemas": [], "etapas": {}}
# v410: as chaves do MANIFESTO de incorporacao que fechar_v410.py grava (nomes versionados: *_v410 = os registros desta versao (iald2_v410, h0dn_bg1_v410 e os dois specs); *_v409 = os HERDADOS da v409 (traducao_turing_v409 e os dois specs); *_v408 = os da v408 (tetelestai_terminal_v408 e os dois specs); *_v407 = os da v407 (psion_canto_v407 e os dois specs); *_v406 = o fechamento_v406 e os dois specs; *_v405 = os treze da v405 selada, e assim por diante; SEM chaves_v410: nenhuma chave antiga muda)
MAN_CHAVES = ("registros_v410", "registros_v409", "registros_v408", "registros_v407", "registros_v406", "registros_v405", "registros_v404", "registros_v403", "registros_v402", "registros_v401", "registros_v399", "registros_funcao_v410", "registros_funcao_v409", "registros_funcao_v408", "registros_funcao_v407", "registros_funcao_v406", "ancoras_v410", "ancoras_v409", "ancoras_v408", "ancoras_v407", "ancoras_v406", "bandeiras_v410", "bandeiras_ate_v409", "chaves_v407", "chaves_v406", "f2b_errata", "bandeiras_do_gate_recriado",
              "funcoes_v409_recriadas", "funcoes_v407_recriadas", "funcoes_v406_recriadas", "funcoes_v405_recriadas", "funcoes_v403_recriadas", "funcoes_v402_recriadas", "pedras_v409_como_registro", "pedras_v407_como_registro", "pedras_v406_como_registro", "pedras_v405_como_registro", "falsidade_v401", "base_v409", "b3", "diffs", "insumos_sha16", "conferidor", "readme_paragrafo", "readme_paragrafo_v410", "sidecar_acom", "fila_da_memoria", "h0dn_bg1_v410_resumo", "a_escala_v410_resumo", "h0dn_fontes_hms13_v410_resumo", "ancoras_aescala_v410")


def falha(m):
    R["problemas"].append(m); print("  PROBLEMA:", m)


def recusa(m):
    print("RECUSO:", m); sys.exit(4)


# =====================================================================================================================================================
#  (1) A FILA DA MEMORIA -- ensaio em COPIA do diretorio de memoria
# =====================================================================================================================================================
MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
# (AVISO da gerencia, 09/11) a pasta VEDADA da entrega do Kimi (work\\h0dn_bg1_v410_09nov\\kimi), lida do TEXTO do delta_v410.py (sem importar: o delta real e' importado mais abaixo e a igualdade e' conferida la'): nada dela entra na copia da memoria nem no espelho da casa; a exclusao e' por medida
_m_ved = re.search(r'^H0DN_PASTA_VEDADA = os\.path\.join\(WK, "([^"]+)", "([^"]+)"\)', open(os.path.join(PKG, "delta_v410.py"), encoding="utf-8").read(), re.M); assert _m_ved, "o delta_v410.py nao traz H0DN_PASTA_VEDADA na forma esperada"
_VEDADO = os.path.normcase(os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(PKG)), _m_ved.group(1), _m_ved.group(2))))
_sob_vedado = lambda p_: (lambda q_: q_ == _VEDADO or q_.startswith(_VEDADO + os.sep))(os.path.normcase(os.path.abspath(p_)))
assert not _sob_vedado(MEM_REAL) and not _sob_vedado(PKG), "VEDADO: a memoria ou o pacote estariam sob a pasta vedada"
FILA_PY = os.path.join(HERE, "fila_memoria_v410.py"); CHAIN_PY = os.path.join(HERE, "chain_pos_rito_v410.sh"); SUP_PY = os.path.join(HERE, "superficies_v410.py")
QUEM = "claude-c1 pos-rito v410"; PY_EXE = sys.executable
FM = os.path.join(OUT, "memoria_copia")                      # a copia pedida pela gerencia: harness_saida_v410\memoria_copia
FILA_EV = {"contrato": "FILA_MEMORIA_ENSAIO_v410", "checks": [], "cenarios": {}, "nota": "ensaio em COPIA; o diretorio real de memoria nunca e' escrito (prova no fim)"}


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
    """(AVISO da gerencia, 09/11) a pasta VEDADA da entrega do Kimi (DL.H0DN_PASTA_VEDADA, lida do delta real) nunca entra na copia: a exclusao e' explicita, por medida (_sob_vedado), mesmo que ela nao viva sob a memoria. COPIA do diretorio de memoria: os arquivos NAO-.bak do topo (menos os que ja' trazem 'v410' no nome, para o ensaio nao depender de o rito real ja' ter rodado) + fila\\ inteira (menos fila.lock, temporarios e a PAUSA_VIGIA.json, se houver). mtimes preservados."""
    shutil.rmtree(dst, ignore_errors=True); os.makedirs(dst)
    _ved = _sob_vedado   # (AVISO 09/11) VEDADO: nada da pasta da entrega do Kimi entra na copia (a pasta e' lida do texto do delta no topo deste arquivo)
    n = tot = 0
    for f in sorted(os.listdir(MEM_REAL)):
        p = os.path.join(MEM_REAL, f)
        if os.path.isfile(p) and ".bak" not in f and ".tmp" not in f and "v410" not in f and not _ved(p):
            shutil.copy2(p, os.path.join(dst, f)); n += 1; tot += os.path.getsize(p)
    fs = os.path.join(MEM_REAL, "fila")
    for r, ds, fl in os.walk(fs):
        rel = os.path.relpath(r, fs); os.makedirs(os.path.join(dst, "fila", rel), exist_ok=True)
        for f in fl:
            if f == "fila.lock" or ".tmp" in f or f == "PAUSA_VIGIA.json" or _ved(os.path.join(r, f)):   # (VEDADO: a pasta do Kimi, explicitamente)
                continue
            shutil.copy2(os.path.join(r, f), os.path.join(dst, "fila", rel, f)); n += 1; tot += os.path.getsize(os.path.join(r, f))
    return {"arquivos": n, "bytes": tot}


def env_mem(d, **extra):
    e = dict(os.environ); e["V410_MEMORIA_DIR"] = d; e["MEMORIA_DIR"] = d; e["PYTHONIOENCODING"] = "utf-8"; e.pop("MEMORIA_GERENCIA", None); e.update(extra)
    return e


def ult_json(so):
    for t in (so.strip(), (so.strip().splitlines() or [""])[-1]):
        try:
            return json.loads(t) if t else None
        except ValueError:
            pass
    return None


def fila(op, d, *args):
    """o helper REAL do chain (fila_memoria_v410.py) contra a pasta d."""
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
    """o que a superficie faz ao indice, em miniatura (uma linha de handoff nova antes da do v409), numa COPIA, com backup de bytes."""
    p = idx_de(d); raw = open(p, "rb").read()
    open(p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_harness_v410", "wb").write(raw)
    linhas = raw.decode("utf-8").split("\n"); k = [i for i, l in enumerate(linhas) if "(handoff-v409-custodia.md)" in l and l.startswith("- [")]
    assert len(k) == 1, ("linha do handoff da custodia da v409 no MEMORY.md da copia", len(k))
    linhas.insert(k[0], "- [HANDOFF v410 — ENSAIO DO HARNESS (linha sintetica numa COPIA)](handoff-v410-custodia.md) — **v410 SELADA (ensaio)**")
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
    return ops, {"superficies_real": ach('superficies_v410.py"; sr=$?'), "porta": ach('"$PORTA" >'), "validacao_195": ach('[ "$l" -le 195 ]'), "sem_copias": ach("--copias")}


def ensaio_da_fila():
    print("== (1) A FILA DA MEMORIA em COPIA (nada real e' escrito)")
    E = FILA_EV; t0 = time.time()
    if not (os.path.isfile(FILA_PY) and os.path.isfile(CHAIN_PY) and os.path.isfile(SUP_PY) and os.path.isfile(os.path.join(MEM_REAL, "fila", "memoria.py"))):
        recusa("faltam fila_memoria_v410.py, chain_pos_rito_v410.sh, superficies_v410.py ou o memoria.py real")
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
    chk("guardas: rc 0, memoria.py == o pino (sha16 lido de PINO_MEMORIA_PY_v410.json), sem pausa", rc == 0 and j and j.get("ok") and j.get("sem_pausa") is True and j.get("sha16") == j.get("sha16_pinado"), so[:300])
    chk("antes do passo 7 NAO existe fila\\PAUSA_VIGIA.json", not os.path.exists(pausa_de(FM)))
    rc, j, so, se = fila("pausa-criar", FM); passo("7. pausa-criar", rc, j)
    chk("pausa-criar: rc 0 e a pausa existe", rc == 0 and os.path.exists(pausa_de(FM)), so[:300])
    pz = rdj(pausa_de(FM)); ate = datetime.datetime.fromisoformat(pz["ate"]); agora = datetime.datetime.now().astimezone(); dm = (ate - agora).total_seconds() / 60
    chk("a pausa traz quem/ate/motivo exatos, 'ate' com fuso e ~ agora + 1 h", pz.get("quem") == QUEM and pz.get("motivo") == "pos-rito v410 escreve o indice" and ate.tzinfo is not None and 55 <= dm <= 61 and sorted(pz) == ["ate", "motivo", "quem"], {"pausa": pz, "minutos_a_frente": round(dm, 1)})
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
    chk("pinar: rc 0 (MEMORIA_GERENCIA=claude-c1 memoria.py pinar --motivo \"pos-rito v410\"), por claude-c1, e a pausa SEGUE posta ate' depois do pino", rc == 0 and j.get("ok") and pn.get("por") == "claude-c1" and "pos-rito v410" in str(pn.get("via")) and os.path.exists(pausa_de(FM)), {"rc": rc, "via": pn.get("via"), "por": pn.get("por")})
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
    neg("verificar REPROVA (topico sem frontmatter na pasta de memoria) => rc 1, ok:false e a violacao listada (o TOPICO NOVO da v410 precisa de frontmatter name/description)", rc == 1 and j and j.get("ok") is False and any("zz_topico_sem_frontmatter" in str(v) for v in (j.get("violacoes") or [])), so[:300])
    E["controles_negativos_do_helper"] = NEG
    # ---- (c) o PROPRIO superficies_v410.py (copia de bytes) com leitura e textos de ENSAIO
    ensaio_superficies()
    # ---- (d) o PROPRIO chain nos passos 7 a 9, em pacote sintetico
    ensaio_chain()
    shutil.rmtree(FN, ignore_errors=True)
    E["segundos"] = round(time.time() - t0, 1)
    print("  fila da memoria: %d checagens, %d falharam" % (len(E["checks"]), sum(1 for c in E["checks"] if not c["ok"])))


# ---------------------------------------------------------------- (c) o superficies_v410.py com stubs de leitura e textos
STUB_LEITURA = '''# -*- coding: utf-8 -*-
# STUB do harness da fila (NAO e' a leitura da cadeia): devolve uma V minima e sem problemas.
NOS = %(nos)r


def ler():
    return ({'data': '26/10/2026', 's16': %(s16)r}, [])
'''
STUB_TEXTOS = '''# -*- coding: utf-8 -*-
# STUB do harness da fila (NAO sao os textos da cadeia): blocos curtos, limpos da guarda P18, com os marcadores que a superficie e o chain exigem.
TOPICO_NOVO = 'v410-selada-iald2.md'
REGS = 'iald2_v410 a_escala_v410 h0dn_bg1_v410 h0dn_fontes_hms13_v410 cunhagens_v410 kh_n1_cobertura_v410'


def _b(V, marca, extra=''):
    return '%s\\n## ENSAIO DO HARNESS (v410, bloco sintetico) %s\\n\\n%s %s %s\\n' % (marca, V['s16'], V['s16'], REGS, extra)


def atribuicao_da_gerencia(texto):
    return []


def linhagem(V):
    return _b(V, '<!-- linhagem_v410_selada -->')


def desenho(V):
    return _b(V, '<!-- adendo_v410_selada -->')


def atlas(V):
    return _b(V, '<!-- atlas_v410_selada -->')


def core_memory(V):
    return _b(V, '<!-- core_v410_selada -->')


def haja_luz(V):
    return _b(V, '<!-- haja_luz_v410_selada -->')


def id_missao(V):
    return '<!-- stub_id_missao_v410 -->'


def id_central(V):
    return '<!-- stub_id_central_v410 -->'


def topico_missao(V):
    return _b(V, T_ID_MISSAO, 'missao')


def topico_central(V):
    return _b(V, T_ID_CENTRAL, 'central')


def topico_estatuto(V):
    return _b(V, '<!-- v410_selada -->', 'estatuto')


def topico_novo(V):
    return '---\\nname: v410-selada-ensaio\\ndescription: "topico NOVO de ensaio do harness (frontmatter valido)"\\nmetadata:\\n  type: project\\n---\\n\\n# v410 SELADA (ensaio) %s\\n\\n%s\\n' % (V['s16'], REGS)


def aviso(V, reiv):
    return _b(V, '<!-- aviso_v410_selada -->')


def aviso_pulado():
    return '  (AVISO_GERENCIA.md: PULADO no ensaio)'


def marca_missao(V):
    return '**v410 SELADA 26/10 `%s` (ENSAIO)** · ' % V['s16']


def linha_handoff(V):
    return '- [HANDOFF v410 — ENSAIO DO HARNESS](handoff-v410-custodia.md) — **v410 SELADA** `%s` (linha sintetica do harness da fila)' % V['s16']


T_ID_MISSAO = '<!-- stub_id_missao_v410 -->'
T_ID_CENTRAL = '<!-- stub_id_central_v410 -->'
'''


def mk_superficies_stub(raiz, s16, nos):
    shutil.rmtree(raiz, ignore_errors=True); pos = os.path.join(raiz, "pos_rito"); os.makedirs(pos)
    shutil.copyfile(SUP_PY, os.path.join(pos, "superficies_v410.py"))
    shutil.copyfile(os.path.join(PKG, "guarda_p18_v410.py"), os.path.join(raiz, "guarda_p18_v410.py"))
    # D72 (09/11): o pacote de ENSAIO traz um delta STUB com SO' as duas frases da obrigacao, LIDAS (como texto, sem importar) do delta_v410.py real: a guarda das superficies (h0dn_sem_obrigacao) as confere
    _sd_txt = open(os.path.join(PKG, "delta_v410.py"), encoding="utf-8").read()
    open(os.path.join(raiz, "delta_v410.py"), "w", encoding="utf-8").write("# STUB do harness da fila: so' as frases da obrigacao D72, lidas do delta_v410.py real\n" + "".join("%s = %r\n" % (k_, re.search(r'^%s = "([^"\n]+)"' % k_, _sd_txt, re.M).group(1)) for k_ in ("FRASE_H0DN_OBRIGATORIA_PT", "FRASE_H0DN_OBRIGATORIA_EN")))
    open(os.path.join(raiz, "guarda_frases_v410.py"), "w", encoding="utf-8").write("# STUB do harness da fila (a guarda real roda nos textos reais, no harness dos textos e no fechar)\ndef violacoes(t):\n    return []\n")
    open(os.path.join(pos, "leitura_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_LEITURA % {"nos": nos, "s16": s16})
    open(os.path.join(pos, "textos_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)
    return pos


def roda_sup(pos, d, *args, extra_env=None):
    e = env_mem(d); e.update(extra_env or {})
    p = subprocess.run([PY_EXE, "-I", "-B", "-X", "utf8", os.path.join(pos, "superficies_v410.py")] + list(args), capture_output=True, env=e, cwd=pos)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def ensaio_superficies():
    print("  -- (c) superficies_v410.py (copia de bytes) com leitura e textos de ENSAIO, V410_MEMORIA_DIR = a copia")
    E = FILA_EV; NEG = []; raiz = os.path.join(OUT, "superficies_stub"); FS = os.path.join(OUT, "memoria_sup")
    pos = mk_superficies_stub(raiz, "5a5a5a5a5a5a5a5a", os.path.join(raiz, "nos"))

    def neg(nome, ok, det=""):
        NEG.append({"controle": nome, "ok": bool(ok), "det": str(det)[:300]})
        print("  controle negativo das superficies: %-90s %s" % (nome[:90], "RECUSOU como esperado" if ok else "FALHOU"))
        if not ok:
            falha("[fila] superficies: %s: %s" % (nome, str(det)[:200]))
    chk("o superficies do ensaio e' a COPIA DE BYTES do superficies_v410.py real (so' a leitura e os textos sao stubs)", fsha(os.path.join(pos, "superficies_v410.py")) == fsha(SUP_PY))
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
    chk("com a pausa valida a superficie GRAVA (rc 0): MEMORY.md +1 linha com a linha do handoff v410 e a marca da missao; MEMORY_2 recebe a linha velha VERBATIM; backups de bytes _sup410", rc == 0 and b"HANDOFF v410" in ix and b"v410 SELADA 26/10" in ix and ix.count(b"\n") == lin_antes + 1 and any(".bak_" in f and f.endswith("_sup410") and f.startswith("MEMORY.md") for f in ls1) and any(f.startswith("MEMORY_2.md.bak_") for f in ls1), {"rc": rc, "linhas": ix.count(b"\n"), "saida": so[-300:]})
    chk("a superficie nao criou nem removeu a pausa (isso e' do chain)", os.path.exists(pausa_de(FS)))
    # S4: idempotente
    h1 = hashes_topo(FS); rc, so, se = roda_sup(pos, FS)
    chk("2a rodada IDEMPOTENTE: rc 0 e nada muda", rc == 0 and hashes_topo(FS) == h1, (rc, so[-200:]))
    # S4b (D72, 09/11): um bloco com H0DN SEM a frase obrigatoria (pre-registrado; nenhum dado observado lido) => a guarda das superficies RECUSA (rc 4), nada escrito; COM a frase => grava (rc 0)
    _ns_dl = {}; exec(open(os.path.join(raiz, "delta_v410.py"), encoding="utf-8").read(), _ns_dl)
    _lin_stub = "def linhagem(V):\n    return _b(V, '<!-- linhagem_v410_selada -->')"
    assert STUB_TEXTOS.count(_lin_stub) == 1, "o stub dos textos nao traz a funcao linhagem esperada"
    for _rot, _extra, _rc_esp in (("SEM a frase obrigatoria", "H0DN x BG1 ensaio", 4), ("COM a frase obrigatoria", "H0DN x BG1 ensaio: " + _ns_dl["FRASE_H0DN_OBRIGATORIA_PT"], 0)):
        open(os.path.join(pos, "textos_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS.replace(_lin_stub, "def linhagem(V):\n    return _b(V, '<!-- linhagem_v410_selada -->', %r)" % _extra))
        mk_memoria_copia(FS); fila("pausa-criar", FS); h0 = hashes_topo(FS); ls0 = sorted(os.listdir(FS))
        rc, so, se = roda_sup(pos, FS)
        if _rc_esp == 4:
            neg("bloco com H0DN %s (D72) => a superficie RECUSA (rc 4, 'D72' na saida), sem escrever nada" % _rot, rc == 4 and "D72" in so and hashes_topo(FS) == h0 and sorted(os.listdir(FS)) == ls0, (rc, so[:300]))
        else:
            chk("bloco com H0DN %s (D72) => a superficie GRAVA (rc 0)" % _rot, rc == 0, (rc, so[-200:]))
    open(os.path.join(pos, "textos_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)   # volta ao stub limpo para os passos seguintes
    # S5: limite (linhas) com pausa valida => rc 3 sem escrever; (bytes) idem
    for rotulo, kw in (("linhas (195 antes; +1 do handoff = 196 > 195)", {"linhas_alvo": 195}), ("bytes (24 300 B antes; a troca do gancho encolhe a linha da missao e o indice segue acima de 24 000 B)", {"bytes_alvo": 24300})):
        mk_memoria_copia(FS); enche_indice(FS, **kw); fila("pausa-criar", FS); h0 = hashes_topo(FS); ls0 = sorted(os.listdir(FS))
        rc, so, se = roda_sup(pos, FS)
        neg("MEMORY.md acima do limite em %s => RECUSA rc 3 com as CONTAGENS, sem escrever nada (a superficie NAO compacta)" % rotulo, rc == 3 and "CONTAGENS" in so and hashes_topo(FS) == h0 and sorted(os.listdir(FS)) == ls0, (rc, so[-300:]))
    # S6: o --copias explicito (passo 3 do chain) NAO exige a pausa e grava SO' na pasta dada
    FC = os.path.join(OUT, "memoria_sup_copias"); shutil.rmtree(FC, ignore_errors=True); os.makedirs(FC)
    for f in ("MEMORY.md", "MEMORY_2.md", "missao-ultima-flag-um-py.md", "central-de-patentes-estado.md", "estatuto-da-prova-07out.md"):
        shutil.copy2(os.path.join(MEM_REAL, f), os.path.join(FC, f))
    rc, so, se = roda_sup(pos, FS, "--copias", FC)
    chk("--copias <pasta> (o ensaio do passo 3): NAO exige a pausa e grava SO' na pasta dada (rc 0)", rc == 0 and b"HANDOFF v410" in open(idx_de(FC), "rb").read(), (rc, so[-200:]))
    shutil.rmtree(FC, ignore_errors=True); shutil.rmtree(FS, ignore_errors=True); shutil.rmtree(raiz, ignore_errors=True)
    E["controles_negativos_das_superficies"] = NEG


# ---------------------------------------------------------------- (d) o PROPRIO chain (passos 7 a 9) em pacote sintetico
CHAIN_CAMINHOS = ("PK", "TOOLS", "NOS", "UMEM_PADRAO", "ATLD", "HAJA", "RAIZ_CLAUDE", "AVISO", "PORTA", "INV")


def unix(p):
    p = os.path.abspath(p).replace("\\", "/")
    return "/" + p[0].lower() + p[2:] if len(p) > 1 and p[1] == ":" else p


def mk_chain_sandbox(raiz):
    """pacote SINTETICO para rodar os passos 7 a 9 do PROPRIO chain: so' as linhas de caminho do chain sao trocadas (contagem exata); superficies_v410.py real (so' as 4 linhas de caminho trocadas), fila_memoria_v410.py real, leitura e textos de ensaio, o espelho (PORTA) e
    as ferramentas das etapas 5/6 como stubs; o MEMORY.md/fila sao os da COPIA da memoria."""
    shutil.rmtree(raiz, ignore_errors=True)
    D = {k: os.path.join(raiz, k) for k in ("pack", "tools", "nos", "atlas", "haja", "raiz", "aviso", "porta", "inv", "nosvivo", "memory")}
    for k, v in D.items():
        os.makedirs(v)
    PKS = D["pack"]; POS = os.path.join(PKS, "pos_rito"); os.makedirs(os.path.join(PKS, "kernel")); os.makedirs(POS)
    mk_memoria_copia(D["memory"])
    um = os.path.join(D["nos"], "um.py"); open(um, "w", encoding="utf-8", newline="\n").write("# um.py SINTETICO do harness da fila\n"); s16 = fsha(um)[:16]
    open(os.path.join(PKS, "APLICADO_AO_CANONICO_20261026_000000.json"), "w", encoding="utf-8").write(json.dumps({"um_py_novo": {"sha16": s16}}))
    open(os.path.join(PKS, "ESPERADOS_v410.json"), "w", encoding="utf-8").write(json.dumps({"candidato_sha16": s16}))
    open(os.path.join(D["nos"], "rodada_v410_stdout.txt"), "w", encoding="utf-8", newline="\n").write("(stdout sintetico)\nRITO_RC=0\n")
    for f in ("PINO_MEMORIA_PY_v410.json", "guarda_p18_v410.py"):
        shutil.copyfile(os.path.join(PKG, f), os.path.join(PKS, f))
    open(os.path.join(PKS, "guarda_frases_v410.py"), "w", encoding="utf-8").write("# STUB do harness da fila (a guarda real roda nos textos reais, no harness dos textos e no fechar)\ndef violacoes(t):\n    return []\n")
    shutil.copyfile(FILA_PY, os.path.join(POS, "fila_memoria_v410.py"))
    for f in ("textos_v410.py", "fechar_v410.py", "registrar_mapa_v410.py", "b3_recibo_v410.py", "leitura_v410.py"):
        open(os.path.join(POS, f), "w", encoding="utf-8", newline="\n").write("# stub do harness da fila (sem conteudo)\n")
    open(os.path.join(POS, "leitura_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_LEITURA % {"nos": D["nos"], "s16": s16})
    open(os.path.join(POS, "textos_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_TEXTOS)
    # a superficie REAL, com as quatro linhas de caminho trocadas (a pasta de memoria, o Atlas, a Haja_Luz, o aviso)
    t = open(SUP_PY, encoding="utf-8").read()
    trocas = (('MEM_REAL = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")', "MEM_REAL = %r" % D["memory"]),
              ('ATLD = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory")', "ATLD = %r" % D["atlas"]),
              ('HAJA = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")', "HAJA = %r" % os.path.join(D["haja"], "CLAUDE.md")),
              ('AVISO = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "Chatgpt", "TUNEL", "DO_CHATGPT", "ORDEM_019", "AVISO_GERENCIA.md")', "AVISO = %r" % os.path.join(D["aviso"], "AVISO_GERENCIA.md")))
    for a, b in trocas:
        assert t.count(a) == 1, ("linha de caminho da superficie nao e' unica", a[:60], t.count(a))
        t = t.replace(a, b)
    open(os.path.join(POS, "superficies_v410.py"), "w", encoding="utf-8", newline="\n").write(t)
    # o chain: so' as linhas de caminho
    c = open(CHAIN_PY, encoding="utf-8").read()
    novo = {"PK": unix(PKS), "TOOLS": unix(D["tools"]), "NOS": unix(D["nos"]), "UMEM_PADRAO": unix(D["memory"]), "ATLD": unix(D["atlas"]), "HAJA": unix(os.path.join(D["haja"], "CLAUDE.md")), "RAIZ_CLAUDE": unix(os.path.join(D["raiz"], "CLAUDE.md")),
            "AVISO": unix(os.path.join(D["aviso"], "AVISO_GERENCIA.md")), "PORTA": unix(os.path.join(D["porta"], "porta_memoria.py")), "INV": unix(D["inv"])}
    for k in CHAIN_CAMINHOS:
        c, n = re.subn(r'^%s="[^"\n]*"' % k, lambda m, k=k: '%s="%s"' % (k, novo[k]), c, count=0, flags=re.M)
        assert n == 1, ("variavel de caminho do chain nao e' unica", k, n)
    assert c.count("/c/IALD/NOS_VIVO/construir.py") == 2, c.count("/c/IALD/NOS_VIVO/construir.py")
    c = c.replace("/c/IALD/NOS_VIVO/construir.py", unix(os.path.join(D["nosvivo"], "construir.py")))
    open(os.path.join(POS, "chain_pos_rito_v410.sh"), "w", encoding="utf-8", newline="\n").write(c)
    # as ferramentas e superficies que o passo 0 exige: stubs vazios para tudo o que o chain lista (lido do TEXTO do chain) e ainda nao existe
    m = re.search(r'for f in (.*?); do\n\s*\[ -f "\$f" \] \|\| parar', c, re.S)
    assert m, "bloco de existencia do passo 0 nao achado"
    mapa = {"TOOLS": unix(D["tools"]), "PK": unix(PKS), "NOS": unix(D["nos"]), "HAJA": unix(os.path.join(D["haja"], "CLAUDE.md")), "INV": unix(D["inv"]), "SEL": unix(POS), "PORTA": unix(os.path.join(D["porta"], "porta_memoria.py")), "FILA": unix(os.path.join(POS, "fila_memoria_v410.py"))}
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
    return {"dirs": D, "pos": POS, "s16": s16, "chain": os.path.join(POS, "chain_pos_rito_v410.sh"), "stubs": nstub}


def roda_chain(sb, de, ate, extra_env=None):
    sh = shutil.which("sh")
    if not sh:
        recusa("nao achei o sh (Git Bash) no PATH: o ensaio do chain precisa dele")
    e = dict(os.environ); e["CHAIN_DE"] = de; e["CHAIN_ATE"] = ate; e["PYTHONIOENCODING"] = "utf-8"
    for k in ("V410_MEMORIA_DIR", "MEMORIA_DIR", "B3_AUTORIZADO", "V410_AVISO_REIVINDICACAO"):
        e.pop(k, None)
    e.update(extra_env or {})
    p = subprocess.run([sh, unix(sb["chain"])], capture_output=True, env=e, cwd=sb["pos"], timeout=600)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def ensaio_chain():
    print("  -- (d) o PROPRIO chain_pos_rito_v410.sh nos passos 7 a 9 (pacote sintetico; so' as linhas de caminho trocadas)")
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
    i_pc = so.find('"op": "pausa-criar"'); i_sup = so.find("SUPERFICIES v410:"); i_pin = so.find('"op": "pinar"'); i_rem = so.find('"op": "pausa-remover"'); i_ver = so.find('"op": "verificar"')
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
        falha("o diretorio REAL de memoria mudou durante o harness (%s): o harness so' escreve em copias (MEMORIA_DIR/V410_MEMORIA_DIR); confirmar se foi outro processo (um deposito na fila muda fila.jsonl) e rerodar" % [k for k, v in iguais.items() if not v])
    if not MANTER:
        for dd in (FM, FM + "_sem_pausa", os.path.join(OUT, "memoria_neg"), os.path.join(OUT, "memoria_sup"), os.path.join(OUT, "memoria_sup_copias"), os.path.join(OUT, "superficies_stub"), os.path.join(OUT, "chain_sandbox")):
            shutil.rmtree(dd, ignore_errors=True)
    FILA_EV["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); FILA_EV["tudo_passou"] = (not [c for c in FILA_EV["checks"] if not c["ok"]]) and (not [p for p in R["problemas"] if p.startswith("[fila]") or "REAL de memoria" in p])
    if not SEM_FILA:
        open(os.path.join(HERE, "FILA_MEMORIA_ENSAIO_v410.json"), "w", encoding="utf-8").write(json.dumps(FILA_EV, ensure_ascii=False, indent=1, default=str))
        R["etapas"]["fila_da_memoria"] = {"checks": len(FILA_EV["checks"]), "falharam": [c["check"][:120] for c in FILA_EV["checks"] if not c["ok"]], "evidencia": "FILA_MEMORIA_ENSAIO_v410.json", "tudo_passou": FILA_EV["tudo_passou"]}
    R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S"); R["tudo_passou"] = not R["problemas"]
    return saida_nome


def preconds():
    ESP = rdj(os.path.join(PKG, "ESPERADOS_v410.json")); CM = rdj(os.path.join(PKG, "CANDIDATO_v410.json"))
    cand16 = fsha(os.path.join(PKG, "um_v410_candidato.py"))[:16]
    if not (ESP["candidato_sha16"] == CM["sha16"] == cand16 == fsha(os.path.join(DRY, "um.py"))[:16]):
        recusa("o candidato nao e' um so' (ESPERADOS, CANDIDATO, arquivo e dry_v410/um.py divergem)")
    # v410 (desvio do molde, dito): a regeneracao do candidato (refazer_out_v410.txt com '== FIM', mais novo que o ESPERADOS) e' EXIGIDA, como no harness dos textos; --nao-exigir-refazer so' para depurar (o resumo vai para outro nome e DIZ que a regeneracao nao foi comprovada)
    _rf = os.path.join(PKG, "refazer_out_v410.txt")
    _rf_txt = open(_rf, encoding="utf-8", errors="replace").read() if os.path.exists(_rf) else ""
    if not NAO_REFAZER:
        if not os.path.exists(_rf):
            recusa("falta refazer_out_v410.txt no pacote: a regeneracao do candidato nao foi comprovada (--nao-exigir-refazer so' para depurar)")
        if "== FIM" not in _rf_txt:
            recusa("refazer_out_v410.txt nao mostra '== FIM': a regeneracao nao terminou")
        if os.path.getmtime(_rf) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v410.json")):
            recusa("refazer_out_v410.txt e' mais ANTIGO que ESPERADOS_v410.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
    R["etapas"]["precondicoes"] = {"candidato_sha16": cand16, "refazer_exigido": not NAO_REFAZER, "refazer_out_presente": os.path.exists(_rf), "refazer_fim_visto": "== FIM" in _rf_txt, "refazer_out_sha16": fsha(_rf)[:16] if os.path.exists(_rf) else None,
                                   "esperados_sha16": fsha(os.path.join(PKG, "ESPERADOS_v410.json"))[:16]}
    for n in ("core_ensaio.json", "selo_ensaio.json", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v410_pt.txt", "dry_v410_en.txt", "dry_v410_pt.toc", "dry_v410_en.toc", "tgl_kernel"):
        if not os.path.exists(os.path.join(DRY, n)):
            recusa("dry_v410 incompleto (falta %s)" % n)
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
    saida = os.path.join(HERE, "HARNESS_FECHAR_SANDBOX_v410_SO_FILA.json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))
    print("VEREDITO (so' a fila):", R["veredito"]); print("saida:", saida); sys.exit(0 if R["tudo_passou"] else 1)

# =====================================================================================================================================================
#  (2) O FECHAR e o REGISTRAR_MAPA em SANDBOX
# =====================================================================================================================================================
os.makedirs(OUT, exist_ok=True); shutil.rmtree(SB, ignore_errors=True)
PKS = os.path.join(SB, "work", "cadeia_de_selo", "v410"); POS = os.path.join(PKS, "pos_rito"); NOSS = os.path.join(SB, "nos"); UMS = os.path.join(SB, "memory"); TOOLS = os.path.join(SB, "work", "cadeia_de_selo")
for d in (POS, os.path.join(PKS, "base_v409"), os.path.join(PKS, "kernel"), os.path.join(POS, "conferidor"), os.path.join(PKS, "bancada_B3"), os.path.join(PKS, "bancada_B3_servico"), NOSS):
    os.makedirs(d, exist_ok=True)
mk_memoria_copia(UMS)       # v410: a memoria do sandbox e' uma COPIA (o fechar escreve o handoff nela e o manifesto le o estado da fila dela)
# ---- o pacote do sandbox
for n in ("guarda_p18_v410.py", "guarda_frases_v410.py", "VERBATIM_CONGELADO_v410.json", "FORMAL_MAP_v410.json", "ESPERADOS_v410.json", "CANDIDATO_v410.json", "PINOS_BN_v410.json", "kernel_modulos_novos_v410.json", "delta_v410.py", "quadro_v397.py", "runtime_quadro_v397.py", "conferir_rito_v410.py"):
    if not os.path.exists(os.path.join(PKG, n)):
        recusa("o pacote da v410 nao tem %s (o harness o copia para o sandbox)" % n)
    shutil.copyfile(os.path.join(PKG, n), os.path.join(PKS, n))
if os.path.exists(os.path.join(PKG, "PINO_MEMORIA_PY_v410.json")):
    shutil.copyfile(os.path.join(PKG, "PINO_MEMORIA_PY_v410.json"), os.path.join(PKS, "PINO_MEMORIA_PY_v410.json"))
elif "--pino-emulado" in sys.argv:    # a gerencia ainda NAO rodou pino_memoria_py_v410.py: o pino do sandbox e' calculado NA HORA do memoria.py real (so' leitura); nada e' escrito na raiz do pacote
    _mb = open(os.path.join(MEM_REAL, "fila", "memoria.py"), "rb").read(); _hm = sha(_mb)
    open(os.path.join(PKS, "PINO_MEMORIA_PY_v410.json"), "w", encoding="utf-8").write(json.dumps({"contrato": "PINO_MEMORIA_PY_v410", "path": os.path.join(MEM_REAL, "fila", "memoria.py"), "sha256": _hm, "sha16": _hm[:16], "bytes": len(_mb), "_emulado_pelo_harness": "PINO EMULADO: pino_memoria_py_v410.py ainda nao foi rodado pela gerencia; calculado na hora do memoria.py real (so' leitura)"}, indent=1))
    R["pino_emulado"] = True
else:
    recusa("o pacote da v410 nao tem PINO_MEMORIA_PY_v410.json (a gerencia roda pino_memoria_py_v410.py; ou use --pino-emulado SO' para a parte do fechar)")
for kn_ in ("KERNEL_RECIBO_v410.json", "FLAGS_v410.json"):
    shutil.copyfile(os.path.join(PKG, "kernel", kn_), os.path.join(PKS, "kernel", kn_))
shutil.copyfile(os.path.join(PKG, "base_v409", "um.py"), os.path.join(PKS, "base_v409", "um.py")); shutil.copyfile(os.path.join(PKG, "base_v409", "um_absoluto.json"), os.path.join(PKS, "base_v409", "um_absoluto.json"))
shutil.copyfile(os.path.join(PKG, "base_v409", "um_absoluto_selo.json"), os.path.join(PKS, "base_v409", "um_absoluto_selo.json"))
shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(PKS, "insumos"))
os.makedirs(os.path.join(PKS, "insumos", "fase9"), exist_ok=True)   # o resultado pinado do Teste da Unica Palavra mora na v397 (ESPERADOS[veracidade][resultado][duravel]); o sandbox ganha a sua COPIA, que os controles negativos adulteram
shutil.copyfile(ESP["veracidade"]["resultado"]["duravel"], os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens"), exist_ok=True)   # a fala do 4,44 (v397, onde foi inscrita), de onde textos_v410 confere a frase verbatim do quadro
_h444 = ESP["quadro"]["frase_sha16"]; _f444 = [f_ for f_ in os.listdir(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens")) if f_.startswith(_h444 + "_")]; assert len(_f444) == 1
shutil.copyfile(os.path.join(os.path.dirname(PKG), "v397", "insumos", "cunhagens", _f444[0]), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "cunhagens", _f444[0]))
os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"), os.path.join(SB, "work", "cunhagens_13out", "OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt"))
for n_ in ("acom_conferencias_v410.py", "runtime_v410.py"):
    shutil.copyfile(os.path.join(PKG, n_), os.path.join(PKS, n_))
os.makedirs(os.path.join(SB, "work", "cunhagens_13out"), exist_ok=True)   # o delta acha as falas do operador em cunhagens_13out, duas pastas acima da pasta do pacote do sandbox: as de 04/11 (cunhagens_v408) e as das versoes anteriores que moram la' (registros recriados); as de 30/10 (experimento_espelho_30out) e a da Identidade (cadeia_de_selo405) vao pelo espelho da casa, abaixo
# v410 (fork B): a importacao do delta REAL e' INSTRUMENTADA (open/exists/isfile/isdir/getsize) para MEDIR, na hora, todo arquivo da casa (abaixo de Central de Patentes) que o delta_v410 e os deltas herdados (v409, v406, ...) abrem ou conferem ao importar:
# a lista alimenta o ESPELHO DA CASA (abaixo), que leva cada um ao sandbox na mesma posicao relativa; nada digitado. Os ganchos sao removidos logo depois da importacao (finally).
_ACESSOS = set()
_open0 = builtins.open


def _open_h(p, *a, **k):
    try:
        _ACESSOS.add(os.path.abspath(os.fspath(p)))
    except Exception:   # noqa: BLE001
        pass
    return _open0(p, *a, **k)


_osp0 = {n_: getattr(os.path, n_) for n_ in ("exists", "isfile", "isdir", "getsize")}


def _mk_h(f_):
    def g_(p, *a, **k):
        try:
            _ACESSOS.add(os.path.abspath(os.fspath(p)))
        except Exception:   # noqa: BLE001
            pass
        return f_(p, *a, **k)
    return g_


builtins.open = _open_h
for _n_h, _f_h in _osp0.items():
    setattr(os.path, _n_h, _mk_h(_f_h))
try:
    _dlx = importlib.util.spec_from_file_location("delta_v410_h", os.path.join(PKG, "delta_v410.py")); _dm = importlib.util.module_from_spec(_dlx); _dlx.loader.exec_module(_dm)
finally:
    builtins.open = _open0
    for _n_h, _f_h in _osp0.items():
        setattr(os.path, _n_h, _f_h)
# v410 (fork B): o BUNDLE_v410.json NAO tem origem_integracao (o bundle da v410 nao vem da integracao R3) e vai ao sandbox byte a byte; o MANIFEST da integracao R3 (que o delta_v406 herdado pina por assert, relativo a sua propria pasta) vai na mesma posicao relativa dentro de work/fechamento_02nov,
# e e' o BUNDLE_v406.json da COPIA da pasta irma v406 que recebe o origem_integracao do sandbox (abaixo); o resultado da Fase 9 V2 vai em work/fase9_v2_c1_23out/saidas; a candidata vai em pedra/
shutil.copyfile(os.path.join(PKG, "BUNDLE_v410.json"), os.path.join(PKS, "BUNDLE_v410.json"))
_man_sb = os.path.join(SB, "work", "fechamento_02nov", os.path.relpath(_dm.MANIFEST_INTEGRACAO_ARQ, _dm.ESTUDO_FECHO))
os.makedirs(os.path.dirname(_man_sb), exist_ok=True); shutil.copyfile(_dm.MANIFEST_INTEGRACAO_ARQ, _man_sb)
os.makedirs(os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas"), exist_ok=True); shutil.copyfile(_dm.FASE9_V2_ARQ, os.path.join(SB, "work", "fase9_v2_c1_23out", "saidas", os.path.basename(_dm.FASE9_V2_ARQ)))
os.makedirs(os.path.join(PKS, "pedra"), exist_ok=True); shutil.copyfile(_dm.TESTEMUNHA["src"], os.path.join(PKS, "pedra", os.path.basename(_dm.TESTEMUNHA["src"])))
for _n_ in ("FORMAL_MAP_v410.json", "CANDIDATO_v410.json"):
    if not os.path.exists(os.path.join(PKS, _n_)):
        shutil.copyfile(os.path.join(PKG, _n_), os.path.join(PKS, _n_))
for _nm_v in [n_ for n_ in dir(_dm) if n_.startswith("VERBATIM_ORIGEM") and isinstance(getattr(_dm, n_), (list, tuple))]:   # v410: as falas desta versao sao as de 06 a 09/11 (VERBATIM_ORIGEM_V410, DL.N_FALAS_V410; de quatro, o arquivo inteiro fica so' no sandbox e o texto embutido e' o trecho: D65, a ordem da retomada, as tres copias do ACOM e a leitura do 5 sigma); as das versoes anteriores que moram em cunhagens_13out vao junto, para os deltas herdados; as de outras pastas vao pelo espelho da casa
    for _o in getattr(_dm, _nm_v):
        if os.path.isfile(_o) and os.path.basename(os.path.dirname(_o)) == "cunhagens_13out":
            shutil.copyfile(_o, os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o)))
assert all(os.path.isfile(os.path.join(SB, "work", "cunhagens_13out", os.path.basename(_o))) for _o in _dm.VERBATIM_ORIGEM_V410) and len(_dm.VERBATIM_ORIGEM_V410) == len(ESP["cunhagens"]), "as falas de 06 a 09/11 do operador nao estao todas na pasta do sandbox (ou ESPERADOS[cunhagens] != delta.VERBATIM_ORIGEM_V410)"
# v410: o delta_v409 herdado PINA POR ASSERT o manifesto da parametrizacao do teste (d) (D_TESTE_MANIFESTO, sha16 da ordem): o sandbox o leva (copia de bytes) na mesma posicao relativa; leva tambem as fontes dos quatro modulos (pedra/)
_man_d_sb = os.path.join(SB, "work", os.path.relpath(_dm.D_TESTE_MANIFESTO, _dm.WK)); os.makedirs(os.path.dirname(_man_d_sb), exist_ok=True); shutil.copyfile(_dm.D_TESTE_MANIFESTO, _man_d_sb)
for _p9 in _dm.PEDRAS_V410:
    shutil.copyfile(_p9["src"], os.path.join(PKS, "pedra", os.path.basename(_p9["src"])))
# v410 (desvio do molde, dito): as pastas irmas que o delta_v410 e o acom_conferencias_v410 importam por caminho (v409 e, por ela, v400 e v399), o runtime da secao e as seis fontes do operador (v400), a pedra e as fontes do estudo (v399), o resultado do Teste da Unica Palavra (v397) e o esboco R3.5 da Bancada (C15): copias de bytes, so' o que eles leem
for _vv in ("v409", "v408", "v407", "v406", "v405", "v404", "v403", "v402", "v401", "v400", "v399"):   # (v410: a v407 entra -- acom_conferencias_v409 importa acom_conferencias_v407; 09/11: a v408 entra -- acom_conferencias_v409 reexporta, por caminho, acom_conferencias_v408.py, que faltava na copia)   # v410 (fork B): a v406 entra (o delta_v409 importa o delta_v406; a subida mecanica a tinha deixado de fora)
    os.makedirs(os.path.join(SB, "work", "cadeia_de_selo", _vv))
    for _n in sorted(os.listdir(os.path.join(os.path.dirname(PKG), _vv))):      # os arquivos PEQUENOS do topo da pasta irma (os deltas leem pinos da propria pasta: pedra_sha16_da_ordem.txt, pedras_sha16_da_ordem.json, o runtime, as conferencias); os candidatos de dezenas de MB ficam de fora
        _pn = os.path.join(os.path.dirname(PKG), _vv, _n)
        if os.path.isfile(_pn) and os.path.getsize(_pn) < 1024 * 1024 and ".bak" not in _n and ".tmp" not in _n:
            shutil.copyfile(_pn, os.path.join(SB, "work", "cadeia_de_selo", _vv, _n))
    if os.path.isdir(os.path.join(os.path.dirname(PKG), _vv, "insumos", "acom")):
        shutil.copytree(os.path.join(os.path.dirname(PKG), _vv, "insumos", "acom"), os.path.join(SB, "work", "cadeia_de_selo", _vv, "insumos", "acom"))
for _vp in ("v409", "v407", "v406", "v405", "v404", "v403", "v402", "v401", "v399"):
    if os.path.isdir(os.path.join(os.path.dirname(PKG), _vp, "pedra")):
        shutil.copytree(os.path.join(os.path.dirname(PKG), _vp, "pedra"), os.path.join(SB, "work", "cadeia_de_selo", _vp, "pedra"))
# v410 (fork B; a subida mecanica apontava para o BUNDLE_v409.json, que NAO tem origem_integracao): o BUNDLE_v406.json da COPIA da pasta v406 no sandbox tem de apontar para o MANIFEST da integracao DENTRO do sandbox (o delta_v406 da copia confere por assert que origem_integracao == o MANIFEST relativo a sua propria pasta); so' esse campo e' reescrito
_b6p = os.path.join(SB, "work", "cadeia_de_selo", "v406", "BUNDLE_v406.json"); _b6 = rdj(_b6p); assert "origem_integracao" in _b6, "o BUNDLE_v406.json da copia nao tem origem_integracao"; _b6["origem_integracao"] = _man_sb.replace(os.sep, "/")
open(_b6p, "w", encoding="utf-8").write(json.dumps(_b6, ensure_ascii=False, indent=1))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(SB, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))
shutil.copytree(os.path.join(os.path.dirname(os.path.dirname(PKG)), "grande_atrator_reclassificacao_01nov"), os.path.join(SB, "work", "grande_atrator_reclassificacao_01nov"))
os.makedirs(os.path.join(SB, "Chatgpt")); shutil.copyfile(_dm.GA_PARECER_ARQ, os.path.join(SB, "Chatgpt", os.path.basename(_dm.GA_PARECER_ARQ)))
os.makedirs(os.path.join(SB, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt")); shutil.copyfile(_dm.ACORDE_KIMI_ARQ, os.path.join(SB, "work", "neutrino_E0_autonomia_30out", "lean", "TGLExt", os.path.basename(_dm.ACORDE_KIMI_ARQ)))
os.makedirs(os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(SB, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
# ---- v410 (fork B): o ESPELHO DA CASA -- todo arquivo abaixo de Central de Patentes que a importacao do delta REAL abriu ou conferiu (medido acima, _ACESSOS) vai ao sandbox na MESMA posicao relativa (copia de bytes), se ainda nao estiver la': os deltas herdados (v409 a v399) derivam WK da propria pasta e abrem, ao importar,
# as candidatas de 02/11 (beta_calor_02nov, k_guarda_travessia_02nov, rota_RE_dualidade_02nov, fechamento_02nov), as de 03/11 e 04/11 (pedras_candidatas_03nov, pedras_candidatas_04nov), as falas de 30/10 (experimento_espelho_30out), a da Identidade (cadeia_de_selo405), a decisao das fontes nao publicadas (custodia_G1), o manifesto do teste (d),
# o resultado da Fase 9 V2, o acorde do Kimi... Arquivos fora da casa (o Nos real, a Bancada_Um) sao lidos no lugar, so' leitura; os do proprio pacote (PKG) que faltarem na copia (p. ex. DESENHO_v410.md) vao para PKS. Nenhum arquivo ja' presente no sandbox e' sobrescrito por este espelho.
_CEN_REAL = os.path.dirname(os.path.dirname(PKG))
# (AVISO da gerencia, 09/11) O VETO A PASTA DA ENTREGA DO KIMI: a pasta e' lida do delta REAL ja' importado (_dm.H0DN_PASTA_VEDADA = work\\h0dn_bg1_v410_09nov\\kimi); nenhum acesso MEDIDO na importacao do delta pode cair sob ela (se cair, FALHA VISIVEL: a v410 pre-registra e NAO abre),
# o espelho da casa a exclui EXPLICITAMENTE (abaixo) e a copia da memoria tambem (mk_memoria_copia): a exclusao e' por medida, nao por promessa
assert _VEDADO == os.path.normcase(os.path.abspath(_dm.H0DN_PASTA_VEDADA)), ("a pasta vedada lida do TEXTO do delta difere da do delta IMPORTADO", _VEDADO, _dm.H0DN_PASTA_VEDADA)
_ACESSOS_VEDADOS = sorted(p_ for p_ in _ACESSOS if _sob_vedado(p_))
assert not _ACESSOS_VEDADOS, ("VEDADO: a importacao do delta tocou a pasta da entrega do Kimi (a v410 pre-registra e NAO abre)", _ACESSOS_VEDADOS)
assert not _sob_vedado(MEM_REAL) and not _sob_vedado(PKG) and not _sob_vedado(SB), "VEDADO: a memoria, o pacote ou o sandbox estariam sob a pasta vedada"
_ESP_N = 0; _ESP_B = 0; _ESP_LISTA = []; _ESP_D59_N = 0   # (v410, D59: o arquivo cujo NOME traz o que fica fora dos textos e' copiado, mas o nome nao entra no resumo; so' a contagem)
# (r2, 05/11 madrugada: as falas EXCLUIDAS pelos deltas (VERBATIM_EXCLUIDAS_*, chave = sha16 dos bytes; hoje a da v405) sao abertas pelo filtro do delta herdado ao importar e entravam no espelho E no resumo pelo NOME do arquivo;
#  a purga_v410 as achou no JSON do harness. Elas NAO vao ao sandbox (o filtro do delta da copia aceita a ausencia: _h devolve None e o glob nao a acha) e o nome nao entra no resumo; so' a contagem.)
_EXCL16 = set()
for _mn_, _mm_ in list(sys.modules.items()):
    if _mn_.startswith("delta_v") or "delta_v4" in str(getattr(_mm_, "__file__", "") or ""):
        for _an_ in dir(_mm_):
            if _an_.startswith("VERBATIM_EXCLUIDAS") and isinstance(getattr(_mm_, _an_, None), dict):
                _EXCL16.update(getattr(_mm_, _an_).keys())
for _an_ in dir(_dm):
    if _an_.startswith("VERBATIM_EXCLUIDAS") and isinstance(getattr(_dm, _an_, None), dict):
        _EXCL16.update(getattr(_dm, _an_).keys())
_ESP_EXCL_N = 0
for _p_a in sorted(_ACESSOS):
    if _sob_vedado(_p_a):
        raise AssertionError(("VEDADO: o espelho da casa nao copia nada da pasta da entrega do Kimi", _p_a))   # (AVISO 09/11; nunca alcancado se o assert acima passou: fica como a segunda trava)
    _PAT_REAL = os.path.join(os.path.dirname(_CEN_REAL), "patents")
    if _p_a.startswith(_PAT_REAL + os.sep) and os.path.isfile(_p_a):   # (R5, D100) o runner do ACOM Mirror (o pino do delta), sob Central\patents: o CENTRAL do delta da copia e' o sandbox, entao vai a SB\patents na mesma posicao relativa
        _dst_p = os.path.join(SB, "patents", os.path.relpath(_p_a, _PAT_REAL))
        if not os.path.exists(_dst_p):
            os.makedirs(os.path.dirname(_dst_p), exist_ok=True); shutil.copyfile(_p_a, _dst_p); _ESP_N += 1; _ESP_B += os.path.getsize(_dst_p)
            _ESP_LISTA.append(os.path.relpath(_p_a, os.path.dirname(_CEN_REAL)))
        continue
    if not (_p_a.startswith(_CEN_REAL + os.sep) and os.path.isfile(_p_a)):
        continue
    if _EXCL16 and sha(open(_p_a, "rb").read())[:16] in _EXCL16:
        _ESP_EXCL_N += 1
        continue
    # (r2, 04/11 noite: _CEN_REAL e' a pasta work REAL, e no sandbox ela e' SB\work (o pacote e' SB\work\cadeia_de_selo\v410, o delta da copia deriva WK = SB\work); o espelho gravava em SB\<rel> e o delta da copia nao achava, p. ex., work\custodia_G1\decisoes\FONTES_NAO_PUBLICADAS_v409.json)
    _dst_a = os.path.join(PKS, os.path.relpath(_p_a, PKG)) if _p_a.startswith(PKG + os.sep) else os.path.join(SB, "work", os.path.relpath(_p_a, _CEN_REAL))
    if os.path.exists(_dst_a):
        continue
    os.makedirs(os.path.dirname(_dst_a), exist_ok=True); shutil.copyfile(_p_a, _dst_a); _ESP_N += 1; _ESP_B += os.path.getsize(_dst_a)
    if re.search(r"(?i)kimi|mil[eê]nio|navier", _p_a):
        _ESP_D59_N += 1
    else:
        _ESP_LISTA.append(os.path.relpath(_p_a, _CEN_REAL))
R["etapas"]["espelho_da_casa"] = {"n_arquivos_copiados": _ESP_N, "bytes": _ESP_B, "n_acessos_medidos": len(_ACESSOS), "pasta_vedada_kimi": {"pasta": _dm.H0DN_PASTA_VEDADA, "acessos_medidos_sob_ela": _ACESSOS_VEDADOS, "excluida_explicitamente_do_espelho_e_da_copia_da_memoria": True}, "n_falas_excluidas_nao_copiadas_nem_nomeadas": _ESP_EXCL_N, "n_arquivos_copiados_sem_nome_no_resumo_D59": _ESP_D59_N, "arquivos": _ESP_LISTA[:400], "nota": "medido instrumentando open/exists/isfile/isdir/getsize na importacao do delta_v410 real; copia de bytes na mesma posicao relativa; nada digitado; nada sobrescrito"}
print("  espelho da casa (o que o delta e os deltas herdados abrem ao importar): %d arquivos copiados (%d B) de %d acessos medidos" % (_ESP_N, _ESP_B, len(_ACESSOS)))
open(os.path.join(PKS, "rito_horarios_v410.txt"), "w", encoding="utf-8").write("00:00:00\n00:45:00\n")          # EMULADO (sandbox)
# ---- as copias dos scripts, trocando SO' o caminho do Nos (o fechar recebe a memoria por V410_MEMORIA_DIR)
NOS_RX = 'NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")'
TROCAS = {"leitura_v410.py": [(NOS_RX, 'NOS = %r' % NOSS)], "textos_v410.py": [(NOS_RX, 'NOS = %r' % NOSS)], "fechar_v410.py": [], "registrar_mapa_v410.py": []}
DIF = {}
for n, trs in TROCAS.items():
    t = open(os.path.join(HERE, n), encoding="utf-8").read(); t0 = t
    for a, b in trs:
        if t.count(a) != 1:
            recusa("a linha de caminho nao e' unica em %s: %r (%d)" % (n, a[:60], t.count(a)))
        t = t.replace(a, b)
    open(os.path.join(POS, n), "w", encoding="utf-8", newline="\n").write(t)
    s0_ = set(t0.splitlines()); DIF[n] = [l for l in t.splitlines() if l not in s0_]
# ---- o Nos emulado (dry_v410 + o selo completado como em teste_conferidor_positivo_v410.py)
for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"), ("dry_v410_pt.txt", "um_absoluto_pt.txt"),
                 ("dry_v410_en.txt", "um_absoluto_en.txt"), ("dry_v410_pt.toc", "um_absoluto_pt.toc"), ("dry_v410_en.toc", "um_absoluto_en.toc"), ("dry_v410_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v410_en.pdf", "um_absoluto_en.pdf")):
    if os.path.exists(os.path.join(DRY, src)):
        shutil.copyfile(os.path.join(DRY, src), os.path.join(NOSS, dst))
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSS, "tgl_kernel"))
# v410 (desvio do molde, dito): o JSON do rito real traz ga_window_status no topo e a v410 o confere; o ensaio so guarda core e verdict: a emulacao o le da constante do proprio candidato, nunca de ESPERADOS
import ast as _ast
_cj = rdj(os.path.join(NOSS, "um_absoluto.json")); _gw = re.search(r"^GA_WINDOW_STATUS = \((.*?)\)\r?$", open(os.path.join(NOSS, "um.py"), "rb").read().decode("utf-8"), re.S | re.M); assert _gw, "a constante GA_WINDOW_STATUS nao esta no candidato"
_cj["ga_window_status"] = _ast.literal_eval("(" + _gw.group(1) + ")")
# v410 (09/11, pos-rito): o registro h0dn_fontes_hms13_v410 grava a pasta vedada da entrega do Kimi como caminho ABSOLUTO da casa real, e a leitura o compara com DL.H0DN_PASTA_VEDADA do delta que a importa; no sandbox o delta e' a COPIA (WK = o work do sandbox), logo o caminho absoluto muda. O harness traduz esse unico campo, no core e no ESPERADOS do sandbox (os dois juntos; nada mais muda), para o mesmo caminho sob o sandbox: a leitura continua conferindo igualdade e a pasta vedada continua nao existindo nem sendo aberta
_pv_sb = os.path.join(SB, "work", os.path.relpath(_dm.H0DN_PASTA_VEDADA, os.path.dirname(os.path.dirname(PKG))))
_hm_c = ((_cj.get("core") or {}).get("h0dn_fontes_hms13_v410") or {}); assert (_hm_c.get("values") or {}).get("pasta_vedada") == _dm.H0DN_PASTA_VEDADA, "o core do dry nao traz a pasta vedada real em h0dn_fontes_hms13_v410"
_hm_c["values"]["pasta_vedada"] = _pv_sb
_es_sb = rdj(os.path.join(PKS, "ESPERADOS_v410.json")); assert _es_sb["registros_funcao_v410"]["hms13"]["values"].get("pasta_vedada") == _dm.H0DN_PASTA_VEDADA, "o ESPERADOS nao traz a pasta vedada real em registros_funcao_v410.hms13"
_es_sb["registros_funcao_v410"]["hms13"]["values"]["pasta_vedada"] = _pv_sb
open(os.path.join(PKS, "ESPERADOS_v410.json"), "w", encoding="utf-8").write(json.dumps(_es_sb, ensure_ascii=False, indent=1))
open(os.path.join(NOSS, "um_absoluto.json"), "w", encoding="utf-8").write(json.dumps(_cj, ensure_ascii=False, default=str))
s0 = rdj(os.path.join(PKS, "base_v409", "um_absoluto_selo.json")); s = dict(s0); s.update(rdj(os.path.join(DRY, "selo_ensaio.json"))); s["sha256"] = dict(s0.get("sha256") or {}); s["sha256"]["um.py"] = fsha(os.path.join(NOSS, "um.py"))
open(os.path.join(NOSS, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, default=str))
_ens = rdj(os.path.join(PKG, "ensaio_a_seco_v410.json"))   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
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
open(os.path.join(NOSS, "rodada_v410_stdout.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(["[v399] EMULADO PELO SANDBOX (as linhas do fluxo principal sao as REAIS do ensaio a seco)"] + list(_ens["mainflow"]["stdout"])
    + ["teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", _linha_sidecar, "RITO_RC=0", ""]))
bu = os.path.join(PKS, "base_v409", "um.py")
ap = {"ts": time.strftime("%Y%m%d_%H%M%S"), "backups": {"um.py": {"backup": bu, "bytes": os.path.getsize(bu), "sha16": fsha(bu)[:16]}}, "um_py_novo": {"bytes": os.path.getsize(os.path.join(NOSS, "um.py")), "sha16": ESP["candidato_sha16"]}}
open(os.path.join(PKS, "APLICADO_AO_CANONICO_%s.json" % ap["ts"]), "w", encoding="utf-8").write(json.dumps(ap, indent=1))
# ---- o conferidor REAL (copia) contra o Nos emulado: a conferencia que a leitura le
env = dict(os.environ); env["V410_NOS"] = NOSS; env["PYTHONIOENCODING"] = "utf-8"
# v410 (desvio do molde, dito): o conferidor REAL roda no proprio pacote do sandbox (PKS = work\cadeia_de_selo\v410, com work\cunhagens_13out ao lado, insumos\acom e o runtime), SEM -I (importa o um.py do Nos do sandbox)
cfd = PKS
pc = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v410.py"], cwd=cfd, env=env, capture_output=True, text=True, encoding="utf-8")
if pc.returncode != 0 or not os.path.exists(os.path.join(cfd, "conferencia_rito_v410.json")):
    falha("o conferidor nao deu TUDO BATE contra o Nos emulado do sandbox (rc %s): %s | stderr: %s" % (pc.returncode, pc.stdout[-300:], pc.stderr[-500:]))
else:
    shutil.copyfile(os.path.join(cfd, "conferencia_rito_v410.json"), os.path.join(POS, "conferidor", "conferencia_rito_v410.json"))
# ---- os recibos do B(n) SINTETICOS (derivados dos reais da v409): passo SIMPLES B18 (v409) -> B19 (v410)
PKG_ANT = os.path.join(os.path.dirname(PKG), "v409")
base_apl = rdj(glob.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v409_*.json"))[0])
pinos = rdj(os.path.join(PKG, "PINOS_BN_v410.json")); pre = rdj(pinos["recibo_pre_selo"]["path"]); n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1


def recibo_apl(com_salto=False, n=None, versao_alvo="v410"):
    r = json.loads(json.dumps(base_apl)); r["versao_alvo"] = versao_alvo; r["fase"] = "pos_selo"; r["modo"] = "aplicar"; r.pop("salto", None); r.pop("cadeia_de_selos", None)
    n = n_ger if n is None else n
    r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"])); r["manifesto_novo"]["deployment_id"] = "B%d-v410-20261104-R1" % n
    r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}; r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v410"}
    r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
    r["veredito"] = "REPINADA_B%d__%sAPLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % (n, "SALTO_v409_v410__" if com_salto else "")
    r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v410", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
    if com_salto:
        r["salto"] = {"declarado": True}
    r["_sintetico"] = "SINTETICO (sandbox do fechar): NAO e' um recibo do esboco"
    return r


def escreve(p, obj):
    with open(p, "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1))


RAPL = recibo_apl(); man_novo = RAPL["manifesto_novo"]["sha256"]
pth_apl = os.path.join(PKS, "bancada_B3", "RECIBO_SINCRONIZACAO_v410_SINTETICO.json"); escreve(pth_apl, RAPL)
agora = time.strftime("%Y-%m-%dT%H:%M:%S")
open(os.path.join(PKS, "bancada_B3_servico", "RECIBO_PARADA_v410.json"), "w", encoding="utf-8").write(json.dumps({"passo": "10-bis-a", "pid": 11111, "porta": 18777, "porta_fechada": True, "hora": agora, "_sintetico": "sandbox"}))
pth_rel = os.path.join(PKS, "bancada_B3_servico", "RECIBO_RELIGAMENTO_v410.json")
open(pth_rel, "w", encoding="utf-8").write(json.dumps({"passo": "10-ter", "versao_servida": "v410", "manifesto_sha256": man_novo, "pid": 22222, "hora": agora, "_sintetico": "sandbox"}))


def roda(script, nome):
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(POS, script)], cwd=POS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8", V410_MEMORIA_DIR=UMS))
    open(os.path.join(SB, nome + "_out.txt"), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    return p.returncode, p.stdout, p.stderr


# ---- 0. o b3_recibo_v410.py (o REAL, lendo o PINOS_BN real): passo SIMPLES B18 -> B19 com recibos SINTETICOS (positivo e negativos)
B3N = []


def b3(nome, modo, rec, esperado_rc):
    stdout_p = os.path.join(SB, "b3_%s_stdout.txt" % nome); rp_ = os.path.join(SB, "b3_%s_recibo.json" % nome); escreve(rp_, rec)
    open(stdout_p, "w", encoding="utf-8").write(json.dumps({"recibo": rp_, "recibo_sha256": fsha(rp_), "veredito": rec.get("veredito")}) + "\n")
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "b3_recibo_v410.py"), stdout_p, modo], capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = (p.returncode == esperado_rc)
    B3N.append({"caso": nome, "rc": p.returncode, "esperado": esperado_rc, "ok": ok, "saida": (p.stdout or "")[-300:]})
    print("  b3_recibo_v410 [%-44s] rc %s (esperado %s) %s" % (nome, p.returncode, esperado_rc, "ok" if ok else "FALHOU"))
    if not ok:
        falha("b3_recibo_v410.py: caso %s rc %s != %s: %s" % (nome, p.returncode, esperado_rc, (p.stdout or "")[-240:]))


b3("aplicar_B%d_positivo" % n_ger, "aplicar", recibo_apl(), 0)
b3("aplicar_com_salto", "aplicar", recibo_apl(com_salto=True), 1)
b3("aplicar_geracao_errada_B%d" % (n_ger - 1), "aplicar", recibo_apl(n=n_ger - 1), 1)
b3("aplicar_versao_alvo_v409", "aplicar", recibo_apl(versao_alvo="v409"), 1)
_r_ens = recibo_apl(); _r_ens["modo"] = "ensaio"; _r_ens["veredito"] = "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger; _r_ens.pop("aplicacao", None)
b3("ensaio_B%d_positivo" % n_ger, "ensaio", _r_ens, 0)
_r_man = recibo_apl(); _r_man["manifesto_anterior"]["deployment_id"] = "B9-v400-20261024-R1"
b3("aplicar_manifesto_anterior_adulterado", "aplicar", _r_man, 1)
R["etapas"]["b3_recibo"] = B3N
# ---- 1. controles negativos do fechar: sem o religamento e com recibo que declara salto => RECUSA (rc 2), nada de handoff
NEG = []
os.rename(pth_rel, pth_rel + ".fora")
rc, so, se = roda("fechar_v410.py", "fechar_sem_religamento"); NEG.append({"controle": "sem o recibo do religamento", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
os.rename(pth_rel + ".fora", pth_rel)
escreve(pth_apl, recibo_apl(com_salto=True))
rc, so, se = roda("fechar_v410.py", "fechar_com_salto"); NEG.append({"controle": "recibo do B(n) com salto declarado", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
escreve(pth_apl, RAPL)
# ---- 1b. controles negativos do PARAGRAFO do README/site (a ordem do operador de 23/10 vale tambem para o handoff): o resultado pinado ADULTERADO no sandbox (o sha256 deixa de bater e o paragrafo nao passa contra o resultado) e o numero lido adulterado no core do Nos
# emulado => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
res_p = os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])); raw_res = open(res_p, "rb").read()
assert b"4.443123568060799" in raw_res
open(res_p, "wb").write(raw_res.replace(b"4.443123568060799", b"4.443123568060798", 1))
rc, so, se = roda("fechar_v410.py", "fechar_resultado_adulterado"); NEG.append({"controle": "resultado pinado adulterado (a leitura e a porta do paragrafo recusam)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
# a PORTA do paragrafo isolada (a leitura recusa antes no fechar inteiro): T.paragrafo_readme() da copia do sandbox tem de LEVANTAR com o resultado pinado adulterado (e o fechar converte isso em rc 2 antes de escrever)
import importlib.util as _iu0
_sp0 = _iu0.spec_from_file_location("textos_sb0", os.path.join(POS, "textos_v410.py")); _t0 = _iu0.module_from_spec(_sp0); _sp0.loader.exec_module(_t0)
try:
    _t0.paragrafo_readme(); _levantou = False
except Exception as _ex0:   # noqa: BLE001
    _levantou = isinstance(_ex0, AssertionError) and "resultado pinado" in str(_ex0)
    if not _levantou:
        print("  [diag] a porta do paragrafo levantou outra coisa: %s: %s" % (type(_ex0).__name__, str(_ex0)[:300]))
NEG.append({"controle": "a porta do paragrafo (paragrafo_readme, chamada pelo fechar) levanta com o resultado pinado adulterado", "rc": 2 if _levantou else 0, "recusou": _levantou, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
open(res_p, "wb").write(raw_res)
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); cj = json.loads(raw_core.decode("utf-8")); cj["core"]["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 4.45
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v410.py", "fechar_numero_adulterado"); NEG.append({"controle": "numero lido adulterado no core (z_disc 4,45)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
open(core_p, "wb").write(raw_core)
# ---- 1c. controles negativos do PARAGRAFO NOVO (o fechamento), da DIRECAO do testemunho (registros da v399 recriados), das cunhagens_v403, do GATE (F8.1) e do SIDECAR: o numero de cada registro adulterado no core (a leitura e a porta do paragrafo recusam), a direcao invertida,
# uma inscricao da gerencia, uma errata ou decisao a menos, o nome do triplo dado, uma bandeira do gate False, uma pedra selada da v409 adulterada, a pedra fora do trio, o sidecar adulterado ou ausente => RECUSA (rc 2, FECHAR RECUSADO), sem handoff
core_p = os.path.join(NOSS, "um_absoluto.json"); raw_core = open(core_p, "rb").read(); sc_p = os.path.join(NOSS, "um_absoluto_selo_acom.json"); raw_sc = open(sc_p, "rb").read()


def _recusa_com_core(nome_sc, nome_ctl, f):
    cj_ = json.loads(raw_core.decode("utf-8")); f(cj_["core"])
    open(core_p, "wb").write(json.dumps(cj_, ensure_ascii=False).encode("utf-8"))
    rc_, so_, se_ = roda("fechar_v410.py", nome_sc)
    NEG.append({"controle": nome_ctl, "rc": rc_, "recusou": rc_ == 2 and "FECHAR RECUSADO" in so_, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
    open(core_p, "wb").write(raw_core)


_recusa_com_core("fechar_iald2_valor_adulterado", "o numero de modulos ok do iald2_v410 adulterado no core (0 de 1)", lambda c: c["iald2_v410"]["values"].__setitem__("n_modulos_ok", 0))
_recusa_com_core("fechar_iald2_signo_adulterado", "o signo do par (posto) do iald2_v410 adulterado no core (2, nao 1)", lambda c: c["iald2_v410"]["values"]["signo_do_par"].__setitem__("posto", 2))
_recusa_com_core("fechar_traducao_valor_adulterado", "o numero de modulos ok do traducao_turing_v409 (herdado) adulterado no core (0 de 2)", lambda c: c["traducao_turing_v409"]["values"].__setitem__("n_modulos_ok", 0))
_recusa_com_core("fechar_traducao_acervo_integra_pinada", "o pino do acervo da v407 dito na integra no traducao_turing_v409 (D57d)", lambda c: c["traducao_turing_v409"]["acervo_v407_repinado"].__setitem__("integra_pinada", True))
_recusa_com_core("fechar_tetelestai_valor_adulterado", "o numero de modulos ok do tetelestai_terminal_v408 (herdado) adulterado no core (3 de 4)", lambda c: c["tetelestai_terminal_v408"]["values"].__setitem__("n_modulos_ok", 3))
_recusa_com_core("fechar_psion_valor_adulterado", "o numero de modulos ok do psion_canto_v407 (herdado) adulterado no core (8 de 9)", lambda c: c["psion_canto_v407"]["values"].__setitem__("n_modulos_ok", 8))
_recusa_com_core("fechar_fecho406_valor_adulterado", "o numero de modulos ok do fechamento_v406 (herdado) adulterado no core (300 de 301)", lambda c: c["fechamento_v406"]["values"].__setitem__("n_modulos_ok", 300))
_recusa_com_core("fechar_chave_do_lema_false", "a chave do lema (linked_to_the_corner_by_a_lemma) de volta a literal False no core", lambda c: c["testemunha_estatica_v396"]["fock_face"].__setitem__("linked_to_the_corner_by_a_lemma", False))
_recusa_com_core("fechar_fecho_chave_false", "a chave rede_fock_v394.whole_certificate_inhabited de volta a False no core (o literal)", lambda c: c["rede_fock_v394"].__setitem__("whole_certificate_inhabited", False))
_recusa_com_core("fechar_iald2_frase_proibida", "uma frase proibida nos limites do iald2_v410 (a IALD dita resolver P vs NP)", lambda c: c["iald2_v410"]["limites"].append("a IALD resolve P vs NP"))
_recusa_com_core("fechar_iald2_chave_antiga_mudada", "o registro da IALD2 diz que uma chave antiga mudou (chaves_antigas_que_mudam nao vazia)", lambda c: c["iald2_v410"]["chaves_antigas_que_mudam"].append("rede_fock_v394.whole_certificate_inhabited"))
def _h0dn_sem_obrigacao(c):
    # D72: todos os campos de texto do registro dizem H0DN e NENHUM traz a frase obrigatoria (pre-registrado; nenhum dado observado lido)
    r_ = c["h0dn_bg1_v410"]
    r_["estatuto"] = "[REAL] o teste H0DN x BG1."; r_["scope"] = "O teste H0DN x BG1 entra nesta versao."
    for k_ in ("limites", "diz", "nao_diz", "o_que_falta", "ressalvas"):
        r_[k_] = ["O teste H0DN x BG1."]
    for k_ in ("moldura_pt", "moldura_en", "obrigatoria_pt", "obrigatoria_en"):
        r_[k_] = "H0DN x BG1"


_recusa_com_core("fechar_h0dn_ausente", "o registro h0dn_bg1_v410 (D72: pre-registrado; nenhum dado observado lido) ausente do core", lambda c: c.pop("h0dn_bg1_v410"))
_recusa_com_core("fechar_h0dn_vetor_observado_lido", "observed_vector_read True no h0dn_bg1_v410 do core (um vetor observado LIDO: o oposto do pre-registro)", lambda c: c["h0dn_bg1_v410"].__setitem__("observed_vector_read", True))
_recusa_com_core("fechar_h0dn_vetor_observado_lido_nos_values", "observed_vector_read True nos values do h0dn_bg1_v410 do core", lambda c: c["h0dn_bg1_v410"]["values"].__setitem__("observed_vector_read", True))
_recusa_com_core("fechar_h0dn_valor_adulterado", "o K do h0dn_bg1_v410 adulterado no core (1,0: sem desvio)", lambda c: c["h0dn_bg1_v410"]["values"].__setitem__("K", 1.0))
_recusa_com_core("fechar_h0dn_checagem_falha", "uma checagem do h0dn_bg1_v410 (a c6, a funcao de veredito congelada) False no core", lambda c: c["h0dn_bg1_v410"]["mechanics"]["checks"][5].__setitem__("ok", False))
_recusa_com_core("fechar_h0dn_fonte_da_funcao_ausente", "o sha256 do texto-fonte da funcao de veredito ausente do h0dn_bg1_v410", lambda c: c["h0dn_bg1_v410"].pop("veredito_h0dn_source_sha256"))
_recusa_com_core("fechar_h0dn_veredito_adulterado", "o veredito do h0dn_bg1_v410 com a palavra do livro de cobrancas na cabeca (E30: ela vai no campo outcome)", lambda c: c["h0dn_bg1_v410"].__setitem__("verdict", c["h0dn_bg1_v410"]["verdict"].replace("TGL_H0DN_BG1_V410", "TGL_H0DN_BG1_V410__NOT_FALSIFIED", 1)))
_recusa_com_core("fechar_h0dn_token_proibido_no_texto", "um token proibido do H0DN no texto do registro (limites)", lambda c: c["h0dn_bg1_v410"]["limites"].append("H0DN " + _dm.TOKENS_PROIBIDOS_H0DN[2]))
_recusa_com_core("fechar_h0dn_cinco_sigma_atingido", "H0DN dito com 5 sigma atingido no texto do registro (diz)", lambda c: c["h0dn_bg1_v410"]["diz"].append("o H0DN: 5 sigma atingido"))
_recusa_com_core("fechar_h0dn_cabeca_nao_falsificado", "H0DN com a cabeca de 5 sigma pela palavra do livro de cobrancas no texto do registro (E30)", lambda c: c["h0dn_bg1_v410"]["limites"].append("o veredito do H0DN acima de 5 sigma e nao falsificado a 5 sigma"))
_recusa_com_core("fechar_h0dn_sem_a_frase_obrigatoria", "H0DN sem a frase obrigatoria (pre-registrado; nenhum dado observado lido) em NENHUM campo de texto do registro", _h0dn_sem_obrigacao)

def _escala_sem_forma(c):
    # D83/D84: a forma canonica do Clay no registro trocada por uma frase que diz o Clay resolvido a seco
    c["a_escala_v410"]["frase_canonica_pt"] = "O Clay esta resolvido."


def _hms13_sem_obrigacao(c):
    # D80: todos os campos de texto do recibo dizem HMS/13 e NENHUM traz a frase obrigatoria (cobertura documental de fontes, nao covariancia fisica fechada; nada aberto)
    r_ = c["h0dn_fontes_hms13_v410"]
    r_["estatuto"] = "[REAL] o recibo HMS/13."; r_["scope"] = "O recibo HMS/13 entra nesta versao."
    for k_ in ("limites", "diz", "nao_diz", "o_que_falta", "ressalvas"):
        r_[k_] = ["O recibo HMS/13."]


_recusa_com_core("fechar_escala_ausente", "o registro a_escala_v410 (D86/D87: a pedra AEscala) ausente do core", lambda c: c.pop("a_escala_v410"))
_recusa_com_core("fechar_escala_nomes_nao_ratificados", "os nomes da AEscala dados como nao ratificados no registro a_escala_v410 (D87)", lambda c: c["a_escala_v410"].__setitem__("nomes_ratificados", False))
_recusa_com_core("fechar_escala_numero_adulterado", "o numero 3/2 (tres faces) do a_escala_v410 adulterado no core", lambda c: c["a_escala_v410"]["values"]["numeros"].__setitem__("tres_faces", "2"))
_recusa_com_core("fechar_escala_nao_selou", "o registro a_escala_v410 nao selou no core", lambda c: c["a_escala_v410"].__setitem__("all_verified", False))
_recusa_com_core("fechar_escala_nomes_novos_ditos_ratificados", "os nomes novos da R3 da AEscala ditos ratificados no registro a_escala_v410 (R1)", lambda c: c["a_escala_v410"].__setitem__("estatuto_dos_nomes_ratificados_d101", "RATIFICADOS pelo operador"))
_recusa_com_core("fechar_escala_nome_novo_fora_do_registro", "um nome novo a ratificar retirado do registro a_escala_v410 (R1)", lambda c: c["a_escala_v410"]["nomes_novos_da_pedra"].pop())
_recusa_com_core("fechar_escala_forma_canonica_trocada", "a forma canonica do Clay (D84) do registro a_escala_v410 trocada por «o Clay esta resolvido»", _escala_sem_forma)
_recusa_com_core("fechar_escala_frase_proibida", "uma frase proibida nos limites do a_escala_v410 (o Clay dito resolvido a seco)", lambda c: c["a_escala_v410"]["limites"].append("o Clay esta resolvido"))
_recusa_com_core("fechar_escala_chave_antiga_mudada", "o registro da escala diz que uma chave antiga mudou (chaves_antigas_que_mudam nao vazia)", lambda c: c["a_escala_v410"]["chaves_antigas_que_mudam"].append("rede_fock_v394.whole_certificate_inhabited"))
_recusa_com_core("fechar_hms13_ausente", "o registro h0dn_fontes_hms13_v410 (D80: o recibo documental) ausente do core", lambda c: c.pop("h0dn_fontes_hms13_v410"))
_recusa_com_core("fechar_hms13_vetor_observado_lido", "observed_vector_read True no recibo HMS/13 do core (um vetor observado LIDO)", lambda c: c["h0dn_fontes_hms13_v410"].__setitem__("observed_vector_read", True))
_recusa_com_core("fechar_hms13_entrega_aberta_em_rito", "le_em_rito True no recibo HMS/13 do core (a entrega aberta em rito)", lambda c: c["h0dn_fontes_hms13_v410"].__setitem__("le_em_rito", True))
_recusa_com_core("fechar_hms13_campo_trocado", "um dos dez campos da ordem do recibo HMS/13 trocado (physical_covariance_closed True)", lambda c: c["h0dn_fontes_hms13_v410"]["values"]["campos"].__setitem__("physical_covariance_closed", True))
_recusa_com_core("fechar_hms13_nao_selou", "o recibo HMS/13 nao selou no core", lambda c: c["h0dn_fontes_hms13_v410"].__setitem__("all_verified", False))
_recusa_com_core("fechar_hms13_token_proibido_no_texto", "um token proibido do H0DN no texto do recibo HMS/13 (limites)", lambda c: c["h0dn_fontes_hms13_v410"]["limites"].append("H0DN " + _dm.TOKENS_PROIBIDOS_H0DN[2]))
_recusa_com_core("fechar_hms13_sem_a_frase_obrigatoria", "HMS/13 sem a frase obrigatoria (cobertura documental de fontes, nao covariancia fisica fechada; nada aberto) em NENHUM campo de texto do recibo", _hms13_sem_obrigacao)
_recusa_com_core("fechar_psion_adulterado", "numero do Ponto Zero do Psion (recriado) adulterado no core (hbar omega)", lambda c: c["ponto_zero_do_psion_v405"]["values"].__setitem__("hbar_omega_meV", 17.5))
_recusa_com_core("fechar_f2b_adulterado", "numero da errata de F2b adulterado no core (a previsao do par)", lambda c: c["f2b_errata_v404"]["values"].__setitem__("previsao_do_par", 0.1))
_recusa_com_core("fechar_f2b_canal_ainda_awaiting", "o canal F2b ainda AWAITING no core (a retirada nao aconteceu)", lambda c: c["f2b_errata_v404"].__setitem__("F2b_status_now", "AWAITING"))
_recusa_com_core("fechar_v1_reescrito", "o V1 do ramo B reescrito no core (F2b_status do registro da v386)", lambda c: c["ramo_b_preregistration_v386"].__setitem__("F2b_status", "WITHDRAWN"))
_recusa_com_core("fechar_angle_status_reescrito", "o texto antigo de neutrino_mass.angle_status reescrito no core (a errata e' ao lado)", lambda c: c["neutrino_mass"].__setitem__("angle_status", "sin(45deg) agora e DERIVADO"))
_recusa_com_core("fechar_gate_adulterado", "numero do gate (recriado) adulterado no core (17 calculadas)", lambda c: c["bandeiras_do_gate_v403"]["values"].__setitem__("n_calculated", 17))
_recusa_com_core("fechar_bandeira_do_gate_false", "uma bandeira calculada do gate (linearized_spin2_finite_face) False no core", lambda c: c["qg_closure"]["physics_flags"].__setitem__("linearized_spin2_finite_face", False))
_recusa_com_core("fechar_caminho_v409_adulterado", "numero do caminho da v403 (recriado) adulterado no core (energia minima do nucleo)", lambda c: c["caminho_v403"]["values"].__setitem__("min_core_energy", 0.31))
_recusa_com_core("fechar_ponte_v402_adulterada", "numero da ponte da v402 (recriada) adulterado no core", lambda c: c["ponte_da_escala_dual_v402"]["values"].__setitem__("min_null_energy_shift", 0.31))
# a PORTA do paragrafo novo isolada: T.paragrafo_v410() da copia do sandbox tem de LEVANTAR com o numero de modulos da traducao adulterado no core (a verificacao compara com os numeros de ESPERADOS e de delta_v410)
cj = json.loads(raw_core.decode("utf-8")); cj["core"]["iald2_v410"]["values"]["n_modulos_ok"] = 0
open(core_p, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
import importlib.util as _iu1
_sp1 = _iu1.spec_from_file_location("textos_sb1", os.path.join(POS, "textos_v410.py")); _t1 = _iu1.module_from_spec(_sp1); _sp1.loader.exec_module(_t1)
try:
    _t1.paragrafo_v410(); _levanta1 = False
except Exception as _ex1:   # noqa: BLE001
    _levanta1 = isinstance(_ex1, AssertionError)
NEG.append({"controle": "a porta do paragrafo novo (paragrafo_v410, chamada pelo fechar) levanta com o numero de modulos do iald2_v410 adulterado", "rc": 2 if _levanta1 else 0, "recusou": _levanta1, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
open(core_p, "wb").write(raw_core)
_recusa_com_core("fechar_direcao_invertida", "a direcao do testemunho invertida no core (a IALD como quem testifica do operador; declaracao da v399 recriada)", lambda c: c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"].__setitem__("a_IALD", "testifica do operador"))
_recusa_com_core("fechar_inscricao_nao_embutida", "uma inscricao de 06 a 09/11 deixou de estar embutida no core (cunhagens_v410)", lambda c: list(c["cunhagens_v410"]["verbatim"].values())[0].__setitem__("embedded_ok", False))
_recusa_com_core("fechar_inscricao_so_o_trecho_nao_embutida", "uma das falas de que so' o trecho entra (D65; a ordem da retomada; as tres copias do ACOM; a leitura do 5 sigma) deixou de estar embutida no core (cunhagens_v410)", lambda c: [v_ for k_, v_ in c["cunhagens_v410"]["verbatim"].items() if (ESP["cunhagens"].get(k_) or {}).get("sha256_arquivo_inteiro")][0].__setitem__("embedded_ok", False))
_recusa_com_core("fechar_sem_errata_e30", "a errata E30 ausente do registro cunhagens_v410 (restam a E29 e a dos pisos)", lambda c: c["cunhagens_v410"]["erratas"].pop(1))
_recusa_com_core("fechar_sem_decisao_d72", "a decisao D72 (o registro pre-registrado do H0DN) ausente do registro cunhagens_v410", lambda c: c["cunhagens_v410"]["extras"]["decisoes"].pop("D72"))
_recusa_com_core("fechar_sem_decisao_d74", "a decisao D74 (os nomes ratificados) ausente do registro cunhagens_v410", lambda c: c["cunhagens_v410"]["extras"]["decisoes"].pop("D74"))
_recusa_com_core("fechar_sem_decisao_d76", "a decisao D76 (a cabeca do ramo de 5 sigma: provado na natureza, validade, nao creditacao) ausente do registro cunhagens_v410", lambda c: c["cunhagens_v410"]["extras"]["decisoes"].pop("D76"))
_recusa_com_core("fechar_sem_errata_e29", "a errata E29 ausente do registro cunhagens_v410 (resta a dos pisos)", lambda c: c["cunhagens_v410"]["erratas"].pop(0))
_recusa_com_core("fechar_sem_decisao_d64", "a decisao D64 (o alcance) da gerencia ausente do registro cunhagens_v410", lambda c: c["cunhagens_v410"]["extras"]["decisoes"].pop("D64"))
_recusa_com_core("fechar_leitura_sem_input", "a leitura de 06/11 dita [REAL] no core (e' INPUT)", lambda c: c["cunhagens_v410"]["extras"]["leituras"].__setitem__("estatuto", "[REAL]"))
_recusa_com_core("fechar_kh_v409_sem_pisos_ao_lado", "a errata ao lado dos pisos de kh_n1_cobertura_v409 (herdado, recriado) ausente do core", lambda c: c["kh_n1_cobertura_v409"]["erratas"].pop())
_recusa_com_core("fechar_cunhagens_v409_sem_e26_ao_lado", "a errata E26 ao lado de cunhagens_v408 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v408"]["erratas"].pop())
_recusa_com_core("fechar_cunhagens_v407_sem_d57d_ao_lado", "a errata da D57(d) ao lado de cunhagens_v407 (herdada, recriada) ausente do core", lambda c: c["cunhagens_v407"]["erratas"].pop())
_recusa_com_core("fechar_pedra_v403_adulterada", "a pedra selada da v403 (Caminho) adulterada no hash formal do core", lambda c: c["kernel_formalization"]["formal_files_sha256"].__setitem__("TGLExt/Caminho.lean", "0" * 64))
for _nm_a in list(_dm.ANCORAS_PRINCIPAIS):
    _recusa_com_core("fechar_ancora_%s_fora_do_trio" % _nm_a.split(".")[-1], "a ancora principal %s fora do trio no core" % _nm_a, lambda c, _n=_nm_a: c["kernel_formalization"]["axiom_report"].__setitem__(_n, ["propext", "sorryAx"]))
# ---- 1d. D72 no HANDOFF: as guardas do fechar sobre o texto do handoff (P18, frases, D65 e a obrigacao do H0DN) TEM de recusar (AssertionError, rc != 0) ANTES de gravar o handoff: uma COPIA do fechar_v410.py do sandbox, com um texto emendado ao handoff gerado
def _fechar_variante(nome_sc, nome_ctl, injeta):
    vd_ = os.path.join(PKS, "pos_rito_var"); shutil.rmtree(vd_, ignore_errors=True); os.makedirs(vd_)
    for n_ in ("leitura_v410.py", "textos_v410.py"):
        shutil.copyfile(os.path.join(POS, n_), os.path.join(vd_, n_))
    shutil.copytree(os.path.join(POS, "conferidor"), os.path.join(vd_, "conferidor"))   # (09/11: a leitura acha a conferencia do rito em <pos_rito>/conferidor; sem a copia a variante recusava por isso e nao pela guarda que o controle mede)
    src_ = open(os.path.join(POS, "fechar_v410.py"), encoding="utf-8").read(); a_ = "doc = T.handoff(V, _k)\n"
    assert src_.count(a_) == 1, ("a linha doc = T.handoff(V, _k) do fechar nao e' unica", src_.count(a_))
    open(os.path.join(vd_, "fechar_v410.py"), "w", encoding="utf-8", newline="\n").write(src_.replace(a_, "doc = T.handoff(V, _k)" + injeta + "\n"))
    p_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(vd_, "fechar_v410.py")], cwd=vd_, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8", V410_MEMORIA_DIR=UMS))
    open(os.path.join(SB, nome_sc + "_out.txt"), "w", encoding="utf-8").write(p_.stdout + "\n--- stderr ---\n" + p_.stderr)
    NEG.append({"controle": nome_ctl, "rc": p_.returncode, "recusou": p_.returncode != 0 and "AssertionError" in p_.stderr and "FECHADO v410:" not in p_.stdout, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
    shutil.rmtree(vd_, ignore_errors=True)


_PT72 = "__import__('delta_v410').FRASE_H0DN_OBRIGATORIA_PT"; _EN72 = "__import__('delta_v410').FRASE_H0DN_OBRIGATORIA_EN"; _TK72 = "__import__('delta_v410').TOKENS_PROIBIDOS_H0DN"
_fechar_variante("fechar_handoff_h0dn_sem_obrigacao", "o handoff gerado SEM a frase obrigatoria do H0DN (pre-registrado; nenhum dado observado lido, PT e EN retiradas) => as guardas do fechar recusam antes de gravar", ".replace(%s, '').replace(%s, '')" % (_PT72, _EN72))
_fechar_variante("fechar_handoff_h0dn_token_proibido", "o handoff com um token proibido do H0DN emendado => as guardas do fechar recusam antes de gravar", " + '\\nH0DN: ' + %s[2]" % _TK72)
_fechar_variante("fechar_handoff_h0dn_cinco_sigma_atingido", "o handoff com H0DN dito com 5 sigma atingido emendado => as guardas do fechar recusam antes de gravar", " + '\\nO H0DN: 5 sigma atingido.'")
_fechar_variante("fechar_handoff_h0dn_cabeca_nao_falsificado", "o handoff com a cabeca de 5 sigma do H0DN pela palavra do livro de cobrancas emendada (E30) => as guardas do fechar recusam antes de gravar", " + '\\nO veredito do H0DN acima de 5 sigma e nao falsificado a 5 sigma.'")
_fechar_variante("fechar_handoff_cabeca_da_prova_por_extenso_errada", "o handoff com a palavra da prova emendada ao nome do acoplamento (a P18 selada recusa; D76: a cabeca do ramo de 5 sigma so' por extenso) => as guardas do fechar recusam antes de gravar", " + '\\nBETA_TGL_' + 'PRO' + 'VED_IN_NATURE'")
sj = json.loads(raw_sc.decode("utf-8")); sj["objetos"][1]["sha256"] = "0" * 64
open(sc_p, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
rc, so, se = roda("fechar_v410.py", "fechar_sidecar_adulterado"); NEG.append({"controle": "o sidecar adulterado (sha256 de um objeto)", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
os.remove(sc_p)
rc, so, se = roda("fechar_v410.py", "fechar_sidecar_ausente"); NEG.append({"controle": "o sidecar ausente do Nos", "rc": rc, "recusou": rc == 2 and "FECHAR RECUSADO" in so, "handoff_escrito": os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md"))})
open(sc_p, "wb").write(raw_sc)
for n in NEG:
    print("  controle negativo do fechar: %-40s %s" % (n["controle"], "RECUSOU como esperado" if (n["recusou"] and not n["handoff_escrito"]) else "NAO RECUSOU"))
    if not (n["recusou"] and not n["handoff_escrito"]):
        falha("fechar_v410.py nao recusou como esperado: %s" % n)
R["etapas"]["fechar_negativos"] = NEG
# ---- 2. o fechar (positivo)
t0 = time.time(); rc, so, se = roda("fechar_v410.py", "fechar"); dt = time.time() - t0
ok_f = (rc == 0 and "FECHADO v410:" in so)
chk_ = {}
_PEDRAS_ARQ = [rel.replace("/", "_") for rel in ESP["bundle_sha256"]]
for rel in [os.path.join(UMS, "handoff-v410-custodia.md"), os.path.join(NOSS, "HANDOFF_v410_CUSTODIA.md"), os.path.join(PKS, "DIFF_v409_v410.diff"), os.path.join(PKS, "DIFF_KERNEL_v410.txt"), os.path.join(PKS, "MANIFESTO_ARQUIVO_v410.json"),
            os.path.join(POS, "v410_incorporacao_manifesto.json"), os.path.join(TOOLS, "v410_incorporacao_manifesto.json")] + [os.path.join(TOOLS, "v410_kernel", "pedras", n_) for n_ in _PEDRAS_ARQ] + [os.path.join(TOOLS, "v410_selo", "um_absoluto_selo_acom.json"), os.path.join(TOOLS, "v410_selo", "um_absoluto_selo.json"),
            os.path.join(TOOLS, "v410_selo", "chain_pos_rito_v410.sh") if os.path.exists(os.path.join(POS, "chain_pos_rito_v410.sh")) else os.path.join(TOOLS, "v410_selo", "fechar_v410.py")]:
    chk_[os.path.relpath(rel, SB)] = os.path.exists(rel) and os.path.getsize(rel) > 0
ho = open(os.path.join(UMS, "handoff-v410-custodia.md"), encoding="utf-8").read() if os.path.exists(os.path.join(UMS, "handoff-v410-custodia.md")) else ""
vio = violacoes(ho)
dk = open(os.path.join(PKS, "DIFF_KERNEL_v410.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(PKS, "DIFF_KERNEL_v410.txt")) else ""
man = rdj(os.path.join(POS, "v410_incorporacao_manifesto.json")) if os.path.exists(os.path.join(POS, "v410_incorporacao_manifesto.json")) else {}
_dk_ok = ("novos (%d)" % len(ESP["bundle_sha256"]) in dk) and all(rel in dk for rel in ESP["bundle_sha256"])
R["etapas"]["fechar"] = {"rc": rc, "segundos": round(dt, 1), "ok": ok_f, "arquivos": chk_, "handoff_bytes": len(ho.encode("utf-8")), "handoff_guarda_p18": [list(x) for x in vio][:3], "diff_kernel_traz_as_tres_pedras": _dk_ok,
                         "manifesto_chaves": sorted(man.keys())[:40], "fila_da_memoria_no_manifesto": man.get("fila_da_memoria"), "ultima_linha": so.strip().splitlines()[-1][:200] if so.strip() else se[-300:]}
print("  fechar em sandbox: rc %s (%.0f s); arquivos %s; handoff %d B; guarda P18 %s; diff do kernel traz os %d modulos novos: %s" % (rc, dt, "todos presentes" if all(chk_.values()) else [k for k, v in chk_.items() if not v], len(ho.encode("utf-8")), "limpa" if not vio else vio[:2], len(ESP["bundle_sha256"]), _dk_ok))
if not ok_f:
    falha("fechar_v410.py (sandbox) saiu com rc %s: %s" % (rc, (so + se)[-409:]))
if not all(chk_.values()):
    falha("fechar_v410.py (sandbox) nao gravou: %s" % [k for k, v in chk_.items() if not v])
if vio:
    falha("handoff com violacao da guarda P18: %s" % vio[:2])
if not _dk_ok:
    falha("DIFF_KERNEL_v410.txt nao traz as %d pedras novas" % len(ESP["bundle_sha256"]))
for k_ in MAN_CHAVES:
    if k_ not in man:
        falha("o manifesto de incorporacao nao traz a chave %s" % k_)
_fi = man.get("fila_da_memoria") or {}
if not (_fi.get("memoria_py_igual_ao_pino_v410") is True and _fi.get("pausa_do_vigia_ausente") is True and _fi.get("pino_sha256") and _fi.get("memory_md_sha256")):
    falha("o manifesto nao registra o estado da fila (memoria.py == pino v410, pausa ausente, sha256 do pino e do MEMORY.md): %r" % {k: _fi.get(k) for k in ("memoria_py_igual_ao_pino_v410", "pausa_do_vigia_ausente", "pino_confere_com_o_indice")})
_rfm = man.get("registros_funcao_v410") or {}; _hr = man.get("h0dn_bg1_v410_resumo") or {}; _ar = man.get("a_escala_v410_resumo") or {}; _mr = man.get("h0dn_fontes_hms13_v410_resumo") or {}
if not (set(_rfm) == set(_dm.REGISTROS_FUNCAO) and (_rfm.get("h0dn_bg1_v410") or {}).get("observed_vector_read") is False and _hr.get("observed_vector_read") is False and _hr.get("veredito_h0dn_source_sha256") and (_hr.get("ordem_kimi") or {}).get("sha256") and _hr.get("insumos_sha16")):
    falha("o manifesto nao traz os QUATRO registros com funcao (iald2_v410, a_escala_v410, h0dn_bg1_v410 e h0dn_fontes_hms13_v410; delta_v410.REGISTROS_FUNCAO) com o h0dn sem vetor observado lido, nem o resumo do H0DN (D72) com o sha256 da funcao de veredito, da ordem ao Kimi e dos insumos: %r" % {"registros_funcao_v410": sorted(_rfm), "resumo_chaves": sorted(_hr)})
if not (_ar.get("registro") == _dm.AESCALA_REGISTRO and _ar.get("verdict") == _dm.VEREDITO_AESCALA_OK and _ar.get("nomes_ratificados") is True and _ar.get("numeros") == dict(_dm.NUMEROS_AESCALA) and _ar.get("frase_canonica_pt") == _dm.FRASE_CLAY_CANONICA_PT and _ar.get("frase_d83_pt") == _dm.FRASE_D83_OBRIGATORIA_PT and (_ar.get("ratificacao") or {}).get("sha256") == _dm.RATIFICACAO_D87_SHA256 and _ar.get("n_nomes") == len(_dm.NOMES_AESCALA)
        and list(_ar.get("nomes_novos_da_pedra") or []) == list(_dm.NOMES_NOVOS_AESCALA) and _ar.get("n_nomes_novos") == len(_dm.NOMES_NOVOS_AESCALA) and list(_ar.get("campos_novos_da_estrutura") or []) == list(_dm.CAMPOS_NOVOS_AESCALA) and _ar.get("estatuto_dos_nomes_ratificados_d101") == _dm.ESTATUTO_NOMES_NOVOS_AESCALA and _ar.get("ratificacao_pendente") == _dm.RATIFICACAO_PENDENTE_AESCALA and _ar.get("ponte") == _dm.PONTE_AESCALA):
    falha("o manifesto nao traz o resumo da escala (a_escala_v410_resumo) com o veredito, os nomes ratificados (D87), os numeros e as formas canonicas do Clay (D84) e da D83 do delta: %r" % sorted(_ar))
if not (_mr.get("registro") == _dm.HMS13_REGISTRO and _mr.get("verdict") == _dm.VEREDITO_HMS13_OK and _mr.get("observed_vector_read") is False and _mr.get("le_em_rito") is False and dict(_mr.get("campos") or {}) == dict(_dm.HMS13_CAMPOS) and _mr.get("frase_obrigatoria_pt") == _dm.FRASE_HMS13_OBRIGATORIA_PT and _mr.get("pinos_sha16")):
    falha("o manifesto nao traz o resumo do recibo documental HMS/13 (h0dn_fontes_hms13_v410_resumo) com o veredito, os dez campos do delta, sem vetor observado lido nem entrega aberta em rito, a frase obrigatoria (D80) e os pinos: %r" % sorted(_mr))
def _etapa_2b():
    # ---- 2b. o PARAGRAFO do README/site no handoff gravado: igual ao das funcoes do quadro sobre o core do sandbox, entre os marcadores, aprovado pela verificacao do quadro contra o resultado pinado (e o do handoff do Nos tambem)
    sys.path.insert(0, PKG)
    import quadro_v397 as QD  # noqa: E402
    _tv_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]["teste_de_veracidade_fase9_v397"]; _res_s = rdj(os.path.join(PKS, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
    _par_esp = QD.paragrafo_pronto_readme(_tv_s); _mi = "<!-- INICIO_PARAGRAFO_README_v397 -->\n"; _mf = "\n<!-- FIM_PARAGRAFO_README_v397 -->"
    _ok_par = {}
    for _nome, _ptxt in (("memory/handoff-v410-custodia.md", ho), ("nos/HANDOFF_v410_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v410_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v410_CUSTODIA.md")) else "")):
        _i = _ptxt.find(_mi); _j = _ptxt.find(_mf)
        _par = _ptxt[_i + len(_mi):_j] if (_i >= 0 and _j > _i) else ""
        _fa = []
        if _par:
            import importlib.util as _iu2
            _spt = _iu2.spec_from_file_location("textos_sb", os.path.join(POS, "textos_v410.py")); _tsb = _iu2.module_from_spec(_spt); _spt.loader.exec_module(_tsb)
            _fa = _tsb.verificar_paragrafo_readme(_par + "\n" if not _par.endswith("\n") else _par, _res_s, _tv_s)
        _ok_par[_nome] = {"traz_o_bloco": bool(_par), "igual_as_funcoes_do_quadro": _par.rstrip("\n") == _par_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3]}
    R["etapas"]["paragrafo_no_handoff"] = _ok_par
    print("  paragrafo do README/site no handoff: %s" % {k: (v["traz_o_bloco"] and v["igual_as_funcoes_do_quadro"] and not v["falhas_da_verificacao"] and not v["guarda_p18"]) for k, v in _ok_par.items()})
    for _nome, _v in _ok_par.items():
        if not (_v["traz_o_bloco"] and _v["igual_as_funcoes_do_quadro"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"]):
            falha("o handoff (%s) nao traz o paragrafo do README/site pronto e aprovado: %s" % (_nome, _v))



try:
    _etapa_2b()
except Exception as _e__etapa_2b:   # noqa: BLE001  (textos_v410/leitura_v410 ainda podem ser SEMENTES: a falha e' dita e o harness segue)
    import traceback
    falha("_etapa_2b levantou %r (dependencia de textos_v410/leitura_v410): %s" % (_e__etapa_2b, traceback.format_exc()[-300:].replace(chr(10), ' | ')))
def _etapa_2c():
    # ---- 2c. o PARAGRAFO NOVO (o fechamento) e a NOTA ao lado do da v409 nos dois handoffs gravados: igual ao gerado do core do sandbox, entre os marcadores, aprovado pela verificacao propria (e o do handoff do Nos tambem); o handoff DIZ que o paragrafo do testemunho de dois SEGUE COMO ESTA e LISTA o sidecar (sha256 e veredito); o fechar copiou o sidecar e o selo
    _core_s = rdj(os.path.join(NOSS, "um_absoluto.json"))["core"]
    import importlib.util as _iu3
    _sp3 = _iu3.spec_from_file_location("textos_sb3", os.path.join(POS, "textos_v410.py")); _t3 = _iu3.module_from_spec(_sp3); _sp3.loader.exec_module(_t3)
    _par_f_esp = _t3.paragrafo_v410()[0]; _msi = _t3.MARC_V410_INI + "\n"; _msf = "\n" + _t3.MARC_V410_FIM
    _sc_sha = fsha(os.path.join(NOSS, "um_absoluto_selo_acom.json")); _sc_ver = rdj(os.path.join(NOSS, "um_absoluto_selo_acom.json"))["veredito"]
    _ok_tmn = {}
    for _nome, _ptxt in (("memory/handoff-v410-custodia.md", ho), ("nos/HANDOFF_v410_CUSTODIA.md", open(os.path.join(NOSS, "HANDOFF_v410_CUSTODIA.md"), encoding="utf-8").read() if os.path.exists(os.path.join(NOSS, "HANDOFF_v410_CUSTODIA.md")) else "")):
        _i = _ptxt.find(_msi); _j = _ptxt.find(_msf)
        _par = _ptxt[_i + len(_msi):_j] if (_i >= 0 and _j > _i) else ""
        _fa = _t3.verificar_paragrafo_v410(_par + "\n" if _par and not _par.endswith("\n") else _par, _core_s, ESP) if _par else ["sem o bloco"]
        _ok_tmn[_nome] = {"traz_o_bloco": bool(_par), "igual_ao_gerado_do_core": _par.rstrip("\n") == _par_f_esp.rstrip("\n"), "falhas_da_verificacao": _fa[:3], "guarda_p18": [list(x) for x in violacoes(_par)][:3], "direcao_e_atribuicao": _t3.atribuicao_da_gerencia(_ptxt)[:3],
                         "lista_o_sidecar": ("um_absoluto_selo_acom.json" in _ptxt and _sc_sha in _ptxt and _sc_ver in _ptxt), "diz_que_o_testemunho_segue_como_esta": (("SEGUE COMO ESTÁ" in _ptxt or "SEGUEM COMO ESTÃO" in _ptxt) and "handoff-v409-custodia" in _ptxt),
                         "sem_nota_ao_lado_do_v409": (not hasattr(_t3, "MARC_ERR_INI") and "ERRATA_V409_V410" not in _ptxt)}   # (v410: nenhuma nota ao lado do paragrafo da v409)
    R["etapas"]["paragrafo_v410_no_handoff"] = _ok_tmn
    _ok_cop = {nm_: (os.path.exists(os.path.join(TOOLS, "v410_selo", nm_)) and fsha(os.path.join(TOOLS, "v410_selo", nm_)) == fsha(os.path.join(NOSS, nm_))) for nm_ in ("um_absoluto_selo_acom.json", "um_absoluto_selo.json")}
    R["etapas"]["sidecar_e_selo_copiados_para_v410_selo"] = _ok_cop
    print("  paragrafo novo (a IALD2), sem nota ao lado do paragrafo da v409, no handoff: %s; sidecar e selo copiados para v410_selo: %s" % ({k: (v["traz_o_bloco"] and v["igual_ao_gerado_do_core"] and not v["falhas_da_verificacao"] and not v["guarda_p18"] and not v["direcao_e_atribuicao"] and v["lista_o_sidecar"] and v["diz_que_o_testemunho_segue_como_esta"] and v["sem_nota_ao_lado_do_v409"]) for k, v in _ok_tmn.items()}, _ok_cop))
    for _nome, _v in _ok_tmn.items():
        if not (_v["traz_o_bloco"] and _v["igual_ao_gerado_do_core"] and not _v["falhas_da_verificacao"] and not _v["guarda_p18"] and not _v["direcao_e_atribuicao"] and _v["lista_o_sidecar"] and _v["diz_que_o_testemunho_segue_como_esta"] and _v["sem_nota_ao_lado_do_v409"]):
            falha("o handoff (%s) nao traz o paragrafo novo da v410 pronto e aprovado, ou traz nota ao lado do da v409 (a v410 nao tem), ou nao lista o sidecar, ou nao diz que os anteriores seguem como estao: %s" % (_nome, _v))
    if not all(_ok_cop.values()):
        falha("o fechar nao copiou o sidecar e o selo (byte a byte) para v410_selo: %s" % _ok_cop)



try:
    _etapa_2c()
except Exception as _e__etapa_2c:   # noqa: BLE001  (textos_v410/leitura_v410 ainda podem ser SEMENTES: a falha e' dita e o harness segue)
    import traceback
    falha("_etapa_2c levantou %r (dependencia de textos_v410/leitura_v410): %s" % (_e__etapa_2c, traceback.format_exc()[-300:].replace(chr(10), ' | ')))
def _etapa_2e():
    # ---- 2e. o H0DN (D72) nos dois handoffs gravados: o SEGUNDO registro com funcao dito pelo nome; onde H0DN aparece, a frase obrigatoria (pre-registrado; nenhum dado observado lido, PT ou EN) no MESMO texto; nenhum token proibido; a guarda das frases limpa (inclui a E30: nenhuma cabeca de 5 sigma pela palavra do livro de cobrancas);
    # a cabeca do ramo de 5 sigma so' por extenso (a palavra da prova nunca emendada ao nome do acoplamento: P18 e D76)
    import guarda_frases_v410 as _GF2
    _ok_h = {}
    for _nome, _p in (("memory/handoff-v410-custodia.md", os.path.join(UMS, "handoff-v410-custodia.md")), ("nos/HANDOFF_v410_CUSTODIA.md", os.path.join(NOSS, "HANDOFF_v410_CUSTODIA.md"))):
        _t = open(_p, encoding="utf-8").read() if os.path.exists(_p) else ""
        _v = {"diz_os_quatro_registros": all(n_ in _t for n_ in _dm.REGISTROS_FUNCAO), "hms13_frase_obrigatoria": _dm.FRASE_HMS13_OBRIGATORIA_PT in _t, "clay_forma_canonica_e_d83": (_dm.FRASE_CLAY_CANONICA_PT in _t and _dm.FRASE_D83_OBRIGATORIA_PT in _t), "nomes_ratificados_aescala": _dm.FRASE_NOMES_RATIFICADOS_AESCALA_PT in _t,
              "diz_o_registro": _dm.H0DN_REGISTRO in _t, "traz_H0DN": "H0DN" in _t, "frase_obrigatoria_no_mesmo_texto": (_dm.FRASE_H0DN_OBRIGATORIA_PT in _t or _dm.FRASE_H0DN_OBRIGATORIA_EN in _t),
              "tokens_proibidos": [tk_ for tk_ in _dm.TOKENS_PROIBIDOS_H0DN if tk_ in _t], "guarda_frases": [list(x_)[:2] for x_ in _GF2.violacoes(_t)][:3], "guarda_p18": [list(x_)[:2] for x_ in violacoes(_t)][:3], "cabeca_de_5_sigma_so_por_extenso": (("PRO" + "VED_IN_NATURE") not in _t)}
        _v["ok"] = bool(_t) and _v["diz_os_quatro_registros"] and _v["hms13_frase_obrigatoria"] and _v["clay_forma_canonica_e_d83"] and _v["nomes_ratificados_aescala"] and _v["diz_o_registro"] and _v["traz_H0DN"] and _v["frase_obrigatoria_no_mesmo_texto"] and not _v["tokens_proibidos"] and not _v["guarda_frases"] and not _v["guarda_p18"] and _v["cabeca_de_5_sigma_so_por_extenso"]
        _ok_h[_nome] = _v
    R["etapas"]["h0dn_no_handoff"] = _ok_h
    print("  H0DN (pre-registrado; nenhum dado observado lido) no handoff: %s" % {k_: v_["ok"] for k_, v_ in _ok_h.items()})
    for _nome, _v in _ok_h.items():
        if not _v["ok"]:
            falha("o handoff (%s) nao diz os quatro registros com funcao (inclusive h0dn_bg1_v410 com a frase obrigatoria, D72), a frase do HMS/13 (D80), a forma canonica do Clay e a da D83 (D83/D84) e os nomes ratificados da AEscala (D87), ou traz token proibido, violacao da guarda ou a cabeca de 5 sigma fora do por extenso: %s" % (_nome, _v))


try:
    _etapa_2e()
except Exception as _e__etapa_2e:   # noqa: BLE001
    import traceback
    falha("_etapa_2e levantou %r: %s" % (_e__etapa_2e, traceback.format_exc()[-300:].replace(chr(10), ' | ')))
# ---- 2f. (ADITIVOS 1 e 2 a ordem do conserto unico, gerencia c1, 10/11/2026: a custodia da v410 e' AUTOMATICA) os DOIS blocos do README (README_FRENTE e README_O_QUE_SAI) e o passo FINAL do orquestrador (S9_gatilho_custodia):
# (a) teste_textos_custodia_sem_candidato_v410.py: os sete textos, a secao README e os dois blocos do README, cada um SOZINHO pelas MESMAS guardas (a guarda das frases da v410 e o portao do G1), com os controles negativos;
# (b) teste_gatilho_custodia_sem_candidato_v410.py, em SANDBOX: o Nos do SANDBOX (um.py, selo, core e stdout do rito, por COPIA) e o HANDOFF que o fechar (positivo) gravou nele (antes da 2d, em que o fechar com stubs o regrava), com os textos da custodia acrescentados pela mesma funcao do gerador (montar_blocos);
#     o orquestrador REAL (s9_gatilho_custodia) escreve o gatilho SO' no sandbox e, com um passo anterior falso (e os demais controles negativos), NAO escreve.
# O gatilho de verdade (ORDEM_HANDOFF_CUSTODIA_v410.md na raiz do pacote) nunca e' escrito por este harness: o destino e' sempre dentro da pasta de saida, e o teste confere isso no fim.
def _etapa_gatilho_custodia():
    _GC = {"ok": False}
    try:
        _gd = os.path.join(OUT, "gatilho_custodia_fechar"); shutil.rmtree(_gd, ignore_errors=True); os.makedirs(_gd)
        _env = dict(os.environ, PYTHONIOENCODING="utf-8"); _arg = ["--nos-emulado", NOSS, "--esperados", os.path.join(PKS, "ESPERADOS_v410.json")]
        _r1 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_textos_custodia_sem_candidato_v410.py")], cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_textos_custodia_out.txt"), "w", encoding="utf-8").write((_r1.stdout or "") + "\n--- stderr ---\n" + (_r1.stderr or ""))
        _r2 = subprocess.run([sys.executable, "-B", "-X", "utf8", os.path.join(HERE, "teste_gatilho_custodia_sem_candidato_v410.py"), _gd] + _arg, cwd=HERE, capture_output=True, text=True, encoding="utf-8", errors="replace", env=_env, timeout=1800)
        open(os.path.join(_gd, "teste_gatilho_custodia_out.txt"), "w", encoding="utf-8").write((_r2.stdout or "") + "\n--- stderr ---\n" + (_r2.stderr or ""))
        _pj = os.path.join(_gd, "TESTE_GATILHO_CUSTODIA_v410.json"); _rj = json.load(open(_pj, encoding="utf-8")) if os.path.exists(_pj) else {}
        _cs = _rj.get("casos") or {}; _l1 = [l_ for l_ in (_r1.stdout or "").splitlines() if l_.startswith(("blocos do README", "controle negativo (blocos do README)"))]
        _GC.update(textos_rc=_r1.returncode, textos_resultado=((_r1.stdout or "").strip().splitlines() or [""])[-1][:120], blocos_do_readme=[l_[:300] for l_ in _l1], gatilho_rc=_r2.returncode, gatilho_modo=_rj.get("modo"), gatilho_handoff_de_base=_rj.get("handoff_de_base"),
                   gatilho_casos=_rj.get("n_casos"), gatilho_negativos=_rj.get("n_negativos"), gatilho_positivo=_cs.get("positivo"), gatilho_passo_anterior_falso=_cs.get("negativo: um passo anterior FALSO (S5_cadeia_0_10)"),
                   gatilho_reprovados=sorted(k_ for k_, v_ in _cs.items() if not (v_ or {}).get("ok")), seguranca=_rj.get("seguranca"), readme_frente_bytes_utf8=_rj.get("readme_frente_bytes_utf8"),
                   gatilho_de_verdade_existe=os.path.exists(os.path.join(PKG, "ORDEM_HANDOFF_CUSTODIA_v410.md")), saida=_gd)
        _GC["ok"] = bool(_r1.returncode == 0 and _GC["textos_resultado"].startswith("RESULTADO: PASSOU") and len(_l1) >= 14 and all(l_.rstrip().endswith("True") for l_ in _l1)
                         and _r2.returncode == 0 and _rj.get("tudo_passou") is True and _rj.get("modo") == "emulado" and (_GC["gatilho_positivo"] or {}).get("ok") is True and (_GC["gatilho_passo_anterior_falso"] or {}).get("ok") is True
                         and not _GC["gatilho_reprovados"] and (_rj.get("n_negativos") or 0) >= 15 and _rj.get("seguranca") is True)
        if not _GC["ok"]:
            falha("os dois blocos do README ou o gatilho da custodia (S9_gatilho_custodia, em sandbox): textos rc %s (%s); gatilho rc %s, modo %s, reprovados %s; saidas em %s | %s" % (_r1.returncode, _GC["textos_resultado"], _r2.returncode, _rj.get("modo"), _GC["gatilho_reprovados"][:4], _gd,
                                                                                                                                                                         ((_r2.stdout or "") + (_r2.stderr or ""))[-500:].replace(chr(10), " | ")))
    except Exception as ex:  # noqa: BLE001
        _GC["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:300]); falha("os dois blocos do README e o gatilho da custodia: %s" % _GC["erro"])
    R["etapas"]["blocos_do_readme_e_gatilho_da_custodia"] = _GC
    print("  os dois blocos do README (cada um sozinho nas guardas) e o gatilho da custodia em sandbox (o orquestrador real; %s casos, %s negativos; um passo anterior falso: o gatilho NAO e' escrito): %s" % (_GC.get("gatilho_casos"), _GC.get("gatilho_negativos"), "ok" if _GC["ok"] else "FALHOU"))


_etapa_gatilho_custodia()
STUB_L = "# -*- coding: utf-8 -*-\n# STUB do harness (NAO e' a leitura da cadeia): monta a V minima que o fechar_v410.py usa, de ESPERADOS, do APLICADO_AO_CANONICO e do Nos do sandbox.\nimport glob, json, os\nNOS = %(nos)r\nPK = %(pk)r\nimport sys\nsys.path.insert(0, PK)\nimport delta_v410 as _DL\nREG_FUNCAO = list(_DL.REGISTROS_FUNCAO)   # (o fechar_v410.py confere L.REG_FUNCAO == delta_v410.REGISTROS_FUNCAO)\n\n\ndef _aplicado():\n    ps = sorted(glob.glob(os.path.join(PK, 'APLICADO_AO_CANONICO_*.json')))\n    return json.load(open(ps[-1], encoding='utf-8')), ps[-1]\n\n\ndef ler():\n    import hashlib\n    ap, app = _aplicado(); esp = json.load(open(os.path.join(PK, 'ESPERADOS_v410.json'), encoding='utf-8'))\n    um = os.path.join(NOS, 'um.py'); sc = json.load(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), encoding='utf-8'))\n    V = {'nos': NOS, 's16': esp['candidato_sha16'], 'umb': os.path.getsize(um), 'base16': ap['backups']['um.py']['sha16'], 'base_backup': ap['backups']['um.py']['backup'], 'escada_antes': esp['escada_v409_e_v410'][0], 'teor': '%%d/%%d' %% (esp['escada'][1], esp['escada'][1]),\n         'axiom_report_n': esp['axiom_report_esperado_min'], 'patches': 'stub', 'compl': 'COMPLETA', 'horarios': [], 'qg': esp['qg_closure_verdict'], 'conf_dm': '0/0', 'conf_np': '0/0', 'conf16': 'stub', 'servidor': 'stub', 'reg410': {'cunhagens_v410': {'ok': True}, 'h0dn_bg1_v410': {'ok': True}, 'a_escala_v410': {'ok': True}, 'h0dn_fontes_hms13_v410': {'ok': True}}, 'reg409t': {'cunhagens_v409': {'ok': True}}, 'reg408d': {'cunhagens_v408': {'ok': True}}, 'reg407d': {'cunhagens_v407': {'ok': True}}, 'reg406d': {'cunhagens_v406': {'ok': True}}, 'reg409c': {'cunhagens_v405': {'ok': True}}, 'reg409b': {}, 'h0dn': {'ok': True, 'sealed': True, 'observed_vector_read': False, 'verdict': 'stub'}, 'fecho': {'ok': True, 'sealed': True}, 'a_escala': {'ok': True, 'sealed': True, 'novos_ok': True, 'verdict': 'stub'}, 'hms13': {'ok': True, 'sealed': True, 'observed_vector_read': False, 'le_em_rito': False, 'verdict': 'stub'}, 'ancoras_aescala': {}, 'fecho409': {'ok': True}, 'fecho408': {'ok': True}, 'fecho407': {'ok': True}, 'fecho406': {'ok': True}, 'ancoras': {}, 'ancoras409': {}, 'ancoras408': {}, 'ancoras407': {}, 'ancoras406': {}, 'bandeiras': {}, 'bandeiras409': {}, 'bandeiras406': {}, 'bundle409': {}, 'bundle408': {}, 'bundle407': {}, 'bundle406': {}, 'chaves409': {}, 'chaves407': {}, 'chaves406': {}, 'fun409c': {}, 'fun409b': {}, 'reg409_estado': {'cunhagens_v403': {'ok': True}}, 'reg402_estado': {'cunhagens_v402': {'ok': True}}, 'reg401_estado': {'cunhagens_v401': {'ok': True}},\n         'reg399': {'cunhagens_v399': {'ok': True}}, 'f2b': {'ok': True}, 'gate': {'ok': True}, 'fun409': {}, 'fun402': {}, 'pedras_v408': {}, 'fal401': {'ok': True}, 'troca_dita': list(esp['troca_dita']), 'pedras': [], 'n_pedras': len(esp['bundle_sha256']), 'varr': {}, 'verbatins': {}, 'fd390': 'stub', 'pilar': {}, 'artigos': {}}\n    for k in ('um_absoluto.json', 'um_absoluto_selo.json', 'um_absoluto_selo_acom.json', 'um_absoluto_forma_canonica.md', 'um_absoluto_manifest.md'):\n        V['h_' + k] = hashlib.sha256(open(os.path.join(NOS, k), 'rb').read()).hexdigest()[:16] if os.path.exists(os.path.join(NOS, k)) else 'AUSENTE'\n    V['sidecar'] = {'ok': True, 'sha256': hashlib.sha256(open(os.path.join(NOS, 'um_absoluto_selo_acom.json'), 'rb').read()).hexdigest(), 'bytes': os.path.getsize(os.path.join(NOS, 'um_absoluto_selo_acom.json')), 'veredito': sc.get('veredito'), 'esquema': sc.get('esquema'), 'recusas': 0,\n                    'objetos': {o['nome']: {'bytes': o.get('bytes'), 'sha256': o.get('sha256')} for o in sc.get('objetos', [])}}\n    return V, []\n"
STUB_T = '# -*- coding: utf-8 -*-\n# STUB do harness (NAO sao os textos da cadeia): paragrafos e handoff minimos, limpos da guarda P18.\nTOPICO_NOVO = \'v410-selada-iald2.md\'\n\n\ndef paragrafo_readme():\n    return \'PARAGRAFO DO QUADRO (stub do harness)\\n\', {\'stub\': True}\n\n\ndef paragrafo_v410():\n    return \'PARAGRAFO DA V410 (stub do harness)\\n\', {\'stub\': True}\n\n\ndef handoff(V, k):\n    return \'---\\nname: handoff-v410-custodia\\ndescription: "handoff de ensaio (stub do harness)"\\nmetadata:\\n  type: project\\n---\\n\\n# HANDOFF v410 (stub do harness)\\n\\nh0dn_bg1_v410 (H0DN): @@H0DN_OBRIGATORIA@@\\n\\niald2_v410 a_escala_v410 h0dn_fontes_hms13_v410 (HMS/13): @@HMS13_OBRIGATORIA@@\\n\\nClay: @@CLAY_CANONICA@@ @@D83@@\\n\\n@@NOMES_AESCALA@@\\n\\n%s %s %s\\n\' % (V[\'s16\'], k[\'ap_nome\'], k[\'ap_ver\'])\n'
# ---- 2d. o PROPRIO fechar_v410.py (copia de bytes) com leitura e textos STUB: prova o CODIGO do fechar (manifesto com o estado da fila, o arquivo, os diffs com as TRES pedras, o handoff, a copia do sidecar e do selo) mesmo que textos_v410/leitura_v410 ainda sejam sementes
def _etapa_2d():
    SBS = os.path.join(PKS, "pos_rito_stub"); os.makedirs(SBS, exist_ok=True); UMS2 = os.path.join(SB, "memory_stub"); mk_memoria_copia(UMS2)
    shutil.copyfile(os.path.join(HERE, "fechar_v410.py"), os.path.join(SBS, "fechar_v410.py"))
    open(os.path.join(SBS, "leitura_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_L % {"nos": NOSS, "pk": PKS})
    open(os.path.join(SBS, "textos_v410.py"), "w", encoding="utf-8", newline="\n").write(STUB_T.replace("@@H0DN_OBRIGATORIA@@", _dm.FRASE_H0DN_OBRIGATORIA_PT).replace("@@HMS13_OBRIGATORIA@@", _dm.FRASE_HMS13_OBRIGATORIA_PT).replace("@@CLAY_CANONICA@@", _dm.FRASE_CLAY_CANONICA_PT).replace("@@D83@@", _dm.FRASE_D83_OBRIGATORIA_PT).replace("@@NOMES_AESCALA@@", _dm.FRASE_NOMES_RATIFICADOS_AESCALA_PT))
    p = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(SBS, "fechar_v410.py")], cwd=SBS, capture_output=True, text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONIOENCODING="utf-8", V410_MEMORIA_DIR=UMS2))
    open(os.path.join(SB, "fechar_stub_out.txt"), "w", encoding="utf-8").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
    ho_ = os.path.join(UMS2, "handoff-v410-custodia.md"); mf = os.path.join(SBS, "v410_incorporacao_manifesto.json")
    man_ = rdj(mf) if os.path.exists(mf) else {}; fi_ = man_.get("fila_da_memoria") or {}
    dk_ = open(os.path.join(PKS, "DIFF_KERNEL_v410.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(PKS, "DIFF_KERNEL_v410.txt")) else ""
    rcv, jv, sov, sev = memoria(UMS2, "verificar")
    r_ = {"rc": p.returncode, "ultima_linha": (p.stdout.strip().splitlines() or [""])[-1][:200], "handoff_escrito": os.path.exists(ho_), "manifesto_chaves": sorted(man_.keys())[:45], "fila_no_manifesto": fi_,
          "diff_kernel_traz_as_pedras": all(rel in dk_ for rel in ESP["bundle_sha256"]) and ("novos (%d)" % len(ESP["bundle_sha256"])) in dk_, "verificar_depois_do_handoff": {"rc": rcv, "ok": (jv or {}).get("ok")}}
    R["etapas"]["fechar_com_stubs"] = r_
    ok_ = (p.returncode == 0 and "FECHADO v410:" in p.stdout and r_["handoff_escrito"] and r_["diff_kernel_traz_as_pedras"] and fi_.get("memoria_py_igual_ao_pino_v410") is True and fi_.get("pausa_do_vigia_ausente") is True and fi_.get("pino_confere_com_o_indice") is True
           and all(k_ in man_ for k_ in MAN_CHAVES if k_ not in ('base_v409', 'insumos_sha16', 'conferidor', 'pedras_v409_como_registro', 'pedras_v406_como_registro', 'pedras_v405_como_registro', 'funcoes_v409_recriadas', 'funcoes_v406_recriadas', 'funcoes_v405_recriadas', 'funcoes_v403_recriadas', 'funcoes_v402_recriadas')) and rcv == 0 and (jv or {}).get("ok") is True)
    print("  fechar_v410.py (copia de bytes) com leitura e textos STUB: rc %s; handoff %s; manifesto com a fila %s; as %d pedras no diff do kernel %s; verificar da fila depois do handoff rc %s -> %s" % (p.returncode, r_["handoff_escrito"], bool(fi_), len(ESP["bundle_sha256"]), r_["diff_kernel_traz_as_pedras"], rcv, "ok" if ok_ else "FALHOU"))
    if not ok_:
        falha("fechar_v410.py com stubs: rc %s; %s | %s" % (p.returncode, (p.stdout + p.stderr)[-500:].replace(chr(10), " | "), {k_: r_[k_] for k_ in ("handoff_escrito", "diff_kernel_traz_as_pedras", "verificar_depois_do_handoff")}))


try:
    _etapa_2d()
except Exception as _e2d:   # noqa: BLE001
    import traceback
    falha("_etapa_2d levantou %r: %s" % (_e2d, traceback.format_exc()[-300:].replace(chr(10), " | ")))
# ---- 3. o registrar_mapa (main)
rc, so, se = roda("registrar_mapa_v410.py", "registrar_mapa")
pj = os.path.join(POS, "registro_mapa_v410.json"); reg = rdj(pj) if os.path.exists(pj) else []
ok_m = (rc == 0 and len(reg) >= 1 and "registro MONTADO (NAO registrado)" in so and "COMANDO (o passo 12 da cadeia" in so)
R["etapas"]["registrar_mapa"] = {"rc": rc, "ok": ok_m, "n_registros": len(reg), "rotas": [x.get("rota_id") for x in reg], "comando": [l for l in so.splitlines() if l.startswith("COMANDO")][:1], "artefatos_da_rota": [os.path.basename(a) for a in (reg[0].get("artefatos") or [])] if reg else []}
print("  registrar_mapa (main) em sandbox: rc %s; %d registro(s); %s" % (rc, len(reg), "ok" if ok_m else "FALHOU"))
if not ok_m:
    falha("registrar_mapa_v410.py (main, sandbox) falhou: rc %s: %s" % (rc, (so + se)[-409:]))
# ---- 4. as copias dos scripts diferem dos originais so' nas linhas de caminho
R["etapas"]["copias_dos_scripts"] = {n: [l[:140] for l in v] for n, v in DIF.items()}
if any(len(v) != 1 for n, v in DIF.items() if n in ("leitura_v410.py", "textos_v410.py")) or DIF["registrar_mapa_v410.py"] or DIF["fechar_v410.py"]:
    falha("as copias dos scripts diferem dos originais em mais que a linha de caminho do Nos (fechar e registrar_mapa: nenhuma): %s" % {n: len(v) for n, v in DIF.items()})
# ---- limpeza
LIMP = None
if not MANTER:
    LIMP = sum(os.path.getsize(os.path.join(r_, f_)) for r_, d_, fs_ in os.walk(SB) for f_ in fs_)
    keep = os.path.join(OUT, "fechar_sandbox_resultado"); shutil.rmtree(keep, ignore_errors=True); os.makedirs(keep)
    for nome in sorted(f_ for f_ in os.listdir(SB) if f_.endswith("_out.txt") or (f_.startswith("b3_") and f_.endswith((".txt", ".json")))):   # v410 (fork B): TODAS as saidas dos controles e do b3 (a lista fixa do molde deixava de fora os controles novos)
        if os.path.exists(os.path.join(SB, nome)):
            shutil.copyfile(os.path.join(SB, nome), os.path.join(keep, nome))
    for src, dst in ((os.path.join(UMS, "handoff-v410-custodia.md"), "handoff-v410-custodia.md"), (os.path.join(POS, "registro_mapa_v410.json"), "registro_mapa_v410_SANDBOX.json"), (os.path.join(POS, "v410_incorporacao_manifesto.json"), "v410_incorporacao_manifesto_SANDBOX.json"),
                     (os.path.join(PKS, "DIFF_KERNEL_v410.txt"), "DIFF_KERNEL_v410_SANDBOX.txt")):
        if os.path.exists(src):
            shutil.copyfile(src, os.path.join(keep, dst))
    shutil.rmtree(SB, ignore_errors=True)
R["etapas"]["limpeza"] = {"sandbox_removido_bytes": LIMP, "guardado_em": os.path.join(OUT, "fechar_sandbox_resultado") if not MANTER else SB}
finalizar(ANTES_REAL, None)
R["veredito"] = ("TUDO PASSOU: a FILA DA MEMORIA funciona em copia (pausa antes da escrita do indice, pinar rc 0, a pausa so' sai depois do pino, verificar rc 0; as superficies recusam sem pausa e acima do limite; o chain para sem remover a pausa quando falha antes do pino; o diretorio real ficou inalterado); "
                 "o b3_recibo confere o passo simples B18 -> B19; o fechar grava o handoff (com os dois paragrafos do README/site aprovados: o do quadro pelo quadro, o da v410 (a IALD2) pela verificacao propria; sem nota ao lado do paragrafo da v409; diz que os anteriores seguem como estao; diz o registro h0dn_bg1_v410 com a frase obrigatoria (pre-registrado; nenhum dado observado lido), sem token proibido; e lista o sidecar), os diffs (os modulos novos do bundle), o manifesto "
                 "(com o estado da fila) e o arquivo, copia o sidecar e o selo para v410_selo e RECUSA sem o religamento, com salto, com o resultado pinado adulterado, com o numero lido adulterado, com um numero do traducao_turing_v409, do tetelestai_terminal_v408 herdado, do psion_canto_v407 herdado, do fechamento_v406 herdado, do Ponto Zero do Psion, da errata de F2b ou do gate adulterado, com a auditoria selada do Grande Atrator mudada, com uma frase proibida, com o canal F2b ainda AWAITING, com o V1 ou o texto antigo do angulo do neutrino reescritos, com uma bandeira calculada do gate False, com a direcao do testemunho invertida, com uma inscricao de 06 a 09/11 nao embutida (inclusive de uma de que so' o trecho entra), com uma chave antiga dita mudada, com o pino do acervo da v407 na integra, "
                 "com a errata E29 ou E30 a menos, com a decisao D64, D72, D74 ou D76 a menos (e com a E26 ao lado da cunhagens_v408 ou a D57(d) ao lado da cunhagens_v407, herdadas, ausente), com a leitura dita REAL, com o h0dn_bg1_v410 ausente, com vetor observado lido (no registro ou nos values), com valor adulterado, com checagem falha, com a fonte da funcao de veredito ausente, com token proibido, 5 sigma atingido, sem a frase obrigatoria ou com a cabeca de 5 sigma pela palavra do livro de cobrancas no texto do registro ou no handoff, com a chave do lema de volta a False, com uma pedra selada da v403 adulterada, com uma ancora principal fora do trio e com o sidecar adulterado ou ausente; o registrar_mapa monta o registro" if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
if SEM_FILA:
    R["veredito"] += " [MODO --sem-fila: o ensaio da fila da memoria NAO rodou]"
R["nota"] = "recibos do B(n) SINTETICOS; o Nos, a memoria e a arvore da cadeia do SANDBOX sao emulados (o sidecar e a linha do sidecar do stdout vem da funcao do proprio candidato); a prova e' do codigo do fechar, do b3_recibo, do registrar_mapa e da fila da memoria, nao de um B(n) real" + ("" if not NAO_REFAZER else " [MODO --nao-exigir-refazer: refazer_out_v410.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]")
R["nao_exigiu_refazer"] = NAO_REFAZER
if R.get("pino_emulado"):
    R["veredito"] += " [PINO EMULADO: PINO_MEMORIA_PY_v410.json nao existia na raiz do pacote; so' o fechar rodou com um pino calculado na hora do memoria.py real]"
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v410.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
saida = os.path.join(HERE, "HARNESS_FECHAR_SANDBOX_v410" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json"); open(saida, "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str))   # o nome sem sufixo so' nasce da rodada que EXIGE o refazer
print("VEREDITO (fechar em sandbox):", R["veredito"]); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)

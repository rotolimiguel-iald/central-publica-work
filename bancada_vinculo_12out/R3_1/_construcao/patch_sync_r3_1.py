# -*- coding: utf-8 -*-
"""patch_sync_r3_1.py (R3.1, 13/10/2026) -- aplica ao sincronizar_bancada.py da R3 (8894b74cb1e6d5a0, copiado para R3_1) os consertos
da reauditoria curta a61fad96 (A1, A1b, A2, A3, N1k/l/m, N2c, N4b, N3a, A4). Cada troca e uma substituicao EXATA que tem de ocorrer
UMA vez; qualquer divergencia aborta sem gravar. Grava por temporario -> confere -> os.replace. uso: patch_sync_r3_1.py"""
import sys
sys.dont_write_bytecode = True
import hashlib, os
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
ALVO = AQUI / "sincronizar_bancada.py"
BASE_SHA16 = "8894b74cb1e6d5a0"
txt = ALVO.read_bytes().decode("utf-8")
assert hashlib.sha256(txt.encode("utf-8")).hexdigest().startswith(BASE_SHA16), "a copia nao e a R3 pinada"
TROCAS = []


def troca(velho, novo):
    TROCAS.append((velho, novo))


# ------------------------------------------------------------------ cabecalho
troca('''"""sincronizar_bancada.py -- o elo B(n) da cadeia de selo: vincula a Bancada Um ao um.py selado.  REVISAO R3 (13/10/2026).
''', '''"""sincronizar_bancada.py -- o elo B(n) da cadeia de selo: vincula a Bancada Um ao um.py selado.  REVISAO R3.1 (13/10/2026).

R3.1 (13/10/2026): a reauditoria curta da R3 (AUDITORIA_F0_6_C1_a61fad96.md, APROVA_COM_RESSALVAS, com a condicao: so derivar o
B(n) depois de uma R3.1) pediu A1-A3 (MEDIA) e, de preferencia, N4b, N2c, N1k/l/m, A4 (residuo) e N3a. Consertos, cada um com
controle negativo NOVO no formato REAL (R3_1/CONTROLES_NEGATIVOS_R3_1.json):
  A1  RE_LOG_SORRY pega o aviso REAL do Lean 4.31 (declaration uses `sorry`, com crases) e o de aspas simples; o contrato e o
      controle antigo (que usavam aspas simples e se confirmavam a si mesmos) foram corrigidos.
  A1b o log e NORMALIZADO antes de contar: BOM UTF-16/UTF-8 decodificado, UTF-8 estrito, CR sozinho vira quebra, sequencias ANSI e
      caracteres de formato removidos; log que nao decodifica ou que traz caractere de controle (o NUL de UTF-16 sem BOM) e recusado.
  A2  build log vazio e recusado; o log do Audit tem de ter pelo menos tantas linhas de axiomas quantos #print axioms tem o
      Audit.lean pinado (sha == formal_files_sha256 do manifesto pinado pelo selo, re-hasheado na arvore).
  A3  os ESPERADOS da secao 4 item 6 do plano vem de CRITERIOS_vNNN.json pinado pela cadeia (--criterios, --criterios-sha256;
      contrato CRITERIOS_R3_1, preenchido, com a decisao X19); o recibo do kernel traz so o MEDIDO; esperado no recibo e recusado.
  N1k cada pedra lista as suas declaracoes; cada uma tem entrada no axiom_report, linha no log do Audit e nome na fonte da pedra.
  N1l o recibo traz formal_files_antes (a impressao dele == o ANTES cruzado com o recibo pre-selo): as pedras do recibo sao
      EXATAMENTE os arquivos formais novos ou mudados do manifesto pinado pelo selo (fora a raiz e o Audit); arquivo removido, ou
      mudado fora de TGLExt/, e recusado.
  N1m a toolchain e obrigatoria como LISTA nao vazia de texto nos dois lados (manifesto pinado pelo selo e recibo), igual.
  N2c o recibo pre-selo e cruzado com o selo pinado no manifesto anterior da Bancada, e o kernel dele com o pino do selo dele.
  N4b aplicar: sonda -> compara bytes com os do passo 3 -> os.replace (a comparacao vem DEPOIS da sonda de ate 1,5 s).
  N3a rollback com o servico no ar = SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO; o recibo documenta a RAM do servico.
  A4  [residuo] os testes rodam com -E -P -s por um lancador pinado (sha no recibo); APPDATA numa pasta vazia nova por teste;
      PYTHONNOUSERSITE=1 para os netos; o site do usuario (achado pela pasta conhecida do Windows, nao pelo APPDATA herdado) entra
      so como CAMINHO (sem .pth, sem usercustomize); os .pth e customize do site do SISTEMA, que ainda executam, ficam no recibo
      com sha256. O codigo dos pacotes do site do usuario (numpy, scipy, torch) segue importavel e nao pinado: residuo declarado.
A R3 (8894b74cb1e6d5a0) fica como registro em R3/. Segue o cabecalho da R3, valido no que nao foi emendado acima.

R3 (13/10/2026) -- o cabecalho anterior:
''')
troca('REVISAO = "R3 (13/10/2026)"', 'REVISAO = "R3.1 (13/10/2026)"')

# ------------------------------------------------------------------ constantes
troca('''KERNEL_CONTRATO = "KERNEL_RECIBO_R3"
''', '''KERNEL_CONTRATO = "KERNEL_RECIBO_R3_1"   # R3.1: toolchain em lista, pedras com declaracoes, formal_files_antes, criterios so com o medido
CRITERIOS_CONTRATO = "CRITERIOS_R3_1"     # A3: o arquivo dos ESPERADOS, pinado pela cadeia (R3_1/CRITERIOS_V392.json e o modelo)
CRITERIOS_X19 = ("sim", "nao")
''')
troca('''RE_LOG_SORRY = re.compile(r"declaration uses 'sorry'|\\bsorryAx\\b")
''', '''# A1 (R3.1): o aviso REAL do Lean 4.31 e ``declaration uses `sorry` `` (crases; medido nos logs do Nos); o de aspas simples tambem conta
RE_LOG_SORRY = re.compile(r"declaration uses\\s*[`'\\u2018\\u2019\\"]sorry[`'\\u2018\\u2019\\"]|\\bsorryAx\\b")
# A1b (R3.1): normalizacao do log antes de contar
RE_ANSI = re.compile(r"\\x1b\\[[0-?]*[ -/]*[@-~]|\\x1b\\][^\\x07\\x1b]*(?:\\x07|\\x1b\\\\)|\\x1b[@-Z\\\\-_]")
RE_CONTROLE = re.compile(r"[\\x00-\\x08\\x0b\\x0c\\x0e-\\x1f\\x7f]")
# A2 (R3.1): as linhas #print axioms do Audit.lean pinado; N1k: o nome que o Lean imprime no log do Audit
RE_PRINT_AXIOMS = re.compile(r"(?m)^[ \\t]*#print[ \\t]+axioms[ \\t]+\\S")
RE_LOG_DECL = re.compile(r"(?m)^'(.+?)' (?:depends on axioms:|does not depend on any axioms)")
''')
troca('''FLAGS_ISOLAMENTO = ("-E", "-P")
''', '''FLAGS_ISOLAMENTO = ("-E", "-P", "-s")   # A4 (R3.1): -s nos filhos; o site do usuario so entra como caminho, pelo lancador
LANCADOR_NOME = "_lancador_isolado_r3_1.py"
LANCADOR_FONTE = ("# -*- coding: utf-8 -*-\\n"
                  "# lancador do sincronizar_bancada.py R3.1 (A4): roda o script pinado com o site do usuario como CAMINHO\\n"
                  "# (nenhum .pth, nenhum usercustomize executa); o filho ja roda com -E -P -s\\n"
                  "import runpy\\n"
                  "import sys\\n"
                  "\\n"
                  "\\n"
                  "def _principal():\\n"
                  "    site_usuario, script = sys.argv[1], sys.argv[2]\\n"
                  "    sys.argv = [script] + sys.argv[3:]\\n"
                  "    if site_usuario != '-':\\n"
                  "        sys.path.append(site_usuario)\\n"
                  "    runpy.run_path(script, run_name='__main__')\\n"
                  "\\n"
                  "\\n"
                  "_principal()\\n")
LANCADOR_SHA256 = hashlib.sha256(LANCADOR_FONTE.encode("utf-8")).hexdigest()
N3A_NOTA = ("N3a (R3.1): o esboco nao trava o arquivo nem a porta. Um um_bancada.py que suba no instante do os.replace le o manifesto NOVO e o "
            "guarda em RAM; se depois houver rollback, o disco volta ao ANTERIOR e a RAM nao. Por isso: (1) depois do rollback o B(n) sonda o "
            "servico e, se ele responde, recusa com SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO; (2) depois de QUALQUER rollback o servico "
            "tem de ser reiniciado com recibo de identidade (10-ter) antes de outro B(n); (3) depois da ultima sonda nada e visivel ao esboco: "
            "o 10-ter confere a identidade do servico religado.")
''')

# ------------------------------------------------------------------ ler_nos: a toolchain do manifesto do kernel fica como veio (N1m)
troca('''                           lean_version=(kernel_man.get("lean_version") or [None])[0], lake_version=(kernel_man.get("lake_version") or [None])[0])''',
      '''                           lean_version=kernel_man.get("lean_version"), lake_version=kernel_man.get("lake_version"))   # N1m: como veio (lista)''')

# ------------------------------------------------------------------ N2c: o recibo pre-selo cruzado com o selo pinado no manifesto anterior
troca('''    ref_versao, ref_um_py = anterior["version"], anterior["um_py_pinado"]
    if ja_sincronizada:
        ant = ((anterior["_man"].get("sincronizacao") or {}).get("anterior") or {})
        ref_versao, ref_um_py = ant.get("version"), ant.get("um_py_pinado")
        if not ref_versao or not ref_um_py:
            raise Recusa("RECIBO_PRE_SELO_SEM_REFERENCIA: a Bancada ja pina a versao alvo e o manifesto nao registra a geracao anterior")''',
      '''    ref_versao, ref_um_py, ref_selo = anterior["version"], anterior["um_py_pinado"], anterior["seal_sha_pinado"]
    if ja_sincronizada:
        ant = ((anterior["_man"].get("sincronizacao") or {}).get("anterior") or {})
        ref_versao, ref_um_py, ref_selo = ant.get("version"), ant.get("um_py_pinado"), ant.get("seal_sha_pinado")
        if not ref_versao or not ref_um_py:
            raise Recusa("RECIBO_PRE_SELO_SEM_REFERENCIA: a Bancada ja pina a versao alvo e o manifesto nao registra a geracao anterior")
        if not ref_selo:
            raise Recusa("RECIBO_PRE_SELO_SEM_REFERENCIA: o manifesto vigente nao registra o selo da geracao anterior (seal_sha_pinado, R3.1)")''')
troca('''        raise Recusa("RECIBO_PRE_SELO_SEM_KERNEL: o recibo pre-selo R3 traz nos.kernel {raiz_sha256, audit_sha256, impressao_formal}")
''', '''        raise Recusa("RECIBO_PRE_SELO_SEM_KERNEL: o recibo pre-selo R3 traz nos.kernel {raiz_sha256, audit_sha256, impressao_formal}")
    # N2c (R3.1): o selo que o recibo pre-selo leu e o selo pinado no manifesto anterior da Bancada; e o manifesto do kernel que ele leu e
    # o que esse selo pina. Sem isto, um pino forjado em vNNN_pins faria o ANTES do T17 ser o que o forjador quisesse.
    selo_r = (rj.get("nos") or {}).get("selo") or {}
    if not isinstance(selo_r, dict) or str(selo_r.get("sha256") or "").lower() != str(ref_selo or "").lower() or not ref_selo:
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: selo do recibo %s != selo pinado no manifesto anterior da Bancada %s (N2c)"
                     % (str(selo_r.get("sha256") if isinstance(selo_r, dict) else selo_r)[:16], str(ref_selo)[:16]))
    if not _hex64(kern.get("sha256")) or str(kern.get("sha256")).lower() != str(selo_r.get("tgl_kernel_proof_manifest_sha256") or "").lower():
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o manifesto do kernel do recibo %s nao e o que o selo dele pina %s (N2c)"
                     % (str(kern.get("sha256"))[:16], str(selo_r.get("tgl_kernel_proof_manifest_sha256"))[:16]))
''')
troca('''                um_py_sha256=um_sha, bancada_dir=rdir, bateria=dict(n=bat.get("n"), passa=bat.get("passa"), falha=bat.get("falha")),''',
      '''                um_py_sha256=um_sha, bancada_dir=rdir, bateria=dict(n=bat.get("n"), passa=bat.get("passa"), falha=bat.get("falha")),
                selo_sha256=selo_r.get("sha256"), selo_cruzado_com_o_manifesto_anterior=True,''')

# ------------------------------------------------------------------ regenerar: o selo anterior fica registrado (N2c no re-run idempotente)
troca('''                                                 version=anterior["version"], um_py_pinado=anterior["um_py_pinado"],''',
      '''                                                 version=anterior["version"], um_py_pinado=anterior["um_py_pinado"],
                                                 seal_sha_pinado=anterior["seal_sha_pinado"],''')

# ------------------------------------------------------------------ A1b, A3: a normalizacao do log e os criterios pinados
troca('''def _hex64(x):
    return isinstance(x, str) and RE_SHA256.match(x.lower()) is not None
''', '''def _hex64(x):
    return isinstance(x, str) and RE_SHA256.match(x.lower()) is not None


def normalizar_log(b):
    """A1b (R3.1): o texto em que sorry, erros e axiomas sao contados. BOM UTF-16 (LE/BE) ou UTF-8 decodificado; sem BOM, UTF-8
    ESTRITO; CRLF e CR sozinho viram LF; sequencias ANSI (CSI, OSC, escapes de 2 caracteres) saem; caractere de controle que
    sobre (o NUL de um UTF-16 sem BOM, um ESC solto) recusa; NFKC e sem caracteres de formato (Cf, ex.: largura zero).
    Devolve (texto, codificacao); recusa com LOG_NAO_DECODIFICA ou LOG_COM_CARACTERE_DE_CONTROLE."""
    if b.startswith(b"\\xff\\xfe") or b.startswith(b"\\xfe\\xff"):
        cod = "utf-16"
    elif b.startswith(b"\\xef\\xbb\\xbf"):
        cod = "utf-8-sig"
    else:
        cod = "utf-8"
    try:
        t = b.decode(cod)
    except UnicodeDecodeError as exc:
        raise Recusa("LOG_NAO_DECODIFICA: %s estrito falhou (%s)" % (cod, exc))
    t = t.replace("\\r\\n", "\\n").replace("\\r", "\\n")
    t = RE_ANSI.sub("", t)
    m = RE_CONTROLE.search(t)
    if m:
        raise Recusa("LOG_COM_CARACTERE_DE_CONTROLE: U+%04X na posicao %d (UTF-16 sem BOM, binario ou escape nao reconhecido)" % (ord(m.group(0)), m.start()))
    t = unicodedata.normalize("NFKC", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Cf")
    return t, cod


CRITERIOS_TIPOS = dict(j1_declaracoes=int, j1_teoremas=int, j1_fora_do_trio=int, audit_entradas_antigas_identicas=int, tokens_proibidos=int,
                       r1_ausente=bool, declaracoes_novas_no_trio=bool)


def carregar_criterios(cp, sha_esperado, versao):
    """A3 (R3.1): os ESPERADOS dos criterios da secao 4 item 6 do plano NAO vem do recibo do kernel: vem de CRITERIOS_vNNN.json
    (contrato CRITERIOS_R3_1), escrito pela gerencia na derivacao [INPUT da gerencia], condicionado a decisao X19 do operador, e
    PINADO pela cadeia (--criterios-sha256, lido de vNNN_pins). O modelo (preenchido=false, x19=null, esperados nulos) e recusado."""
    cp = Path(cp)
    if not cp.is_file():
        raise Recusa("CRITERIOS_AUSENTES: " + str(cp))
    raw = cp.read_bytes()
    if not sha_esperado:
        raise Recusa("CRITERIOS_SHA_AUSENTE: a cadeia passa --criterios-sha256 (lido de vNNN_pins); um arquivo de criterios sem pino nao vale")
    if str(sha_esperado).lower() != sha256(raw):
        raise Recusa("CRITERIOS_SHA_DIVERGE: arquivo %s != esperado %s" % (sha256(raw)[:16], str(sha_esperado)[:16]))
    try:
        c = json.loads(raw)
    except ValueError as exc:
        raise Recusa("CRITERIOS_ILEGIVEIS: " + str(exc))
    if not isinstance(c, dict):
        raise Recusa("CRITERIOS_ILEGIVEIS: nao e objeto JSON")
    if c.get("contrato") != CRITERIOS_CONTRATO:
        raise Recusa("CRITERIOS_CONTRATO_INVALIDO: %r (exigido %s)" % (c.get("contrato"), CRITERIOS_CONTRATO))
    if c.get("versao") != versao:
        raise Recusa("CRITERIOS_DE_OUTRA_VERSAO: %r, alvo %r" % (c.get("versao"), versao))
    if c.get("preenchido") is not True:
        raise Recusa("CRITERIOS_NAO_PREENCHIDOS: preenchido=%r (o modelo nao vale; a gerencia preenche na derivacao)" % (c.get("preenchido"),))
    if c.get("x19") not in CRITERIOS_X19:
        raise Recusa("CRITERIOS_SEM_DECISAO_X19: x19=%r (exigido 'sim' ou 'nao': a X19 muda os numeros J1)" % (c.get("x19"),))
    esp = c.get("esperados")
    if not isinstance(esp, dict):
        raise Recusa("CRITERIOS_SEM_ESPERADOS")
    if set(esp) != set(KERNEL_CRITERIOS_EXIGIDOS):
        raise Recusa("CRITERIOS_CHAVES_DIVERGEM: faltam %s; sobram %s" % (sorted(set(KERNEL_CRITERIOS_EXIGIDOS) - set(esp)), sorted(set(esp) - set(KERNEL_CRITERIOS_EXIGIDOS))))
    for nome in KERNEL_CRITERIOS_EXIGIDOS:
        v, tipo = esp[nome], CRITERIOS_TIPOS[nome]
        if type(v) is not tipo or (tipo is int and v < 0):
            raise Recusa("CRITERIOS_ESPERADO_INVALIDO: %s=%r (exigido %s%s; nulo, float e texto nao valem)" % (nome, v, tipo.__name__, " >= 0" if tipo is int else ""))
    return dict(path=str(cp), sha256=sha256(raw), bytes=len(raw), contrato=CRITERIOS_CONTRATO, versao=versao, x19=c["x19"], esperados=dict(esp))
''')

# ------------------------------------------------------------------ verificar_kernel_recibo: reescrita inteira (R3.1)
ini = txt.index("def verificar_kernel_recibo(")
fim = txt.index("def _arquivo_executado_e_pinado(")
VELHA_VKR = txt[ini:fim]
NOVA_VKR = '''def verificar_kernel_recibo(kp, versao, nos_info, sha_esperado=None, recibo_pre_selo=None, sandbox=False, criterios=None):
    """N1 (R3) + R3.1: o recibo do kernel da etapa 2 (contrato KERNEL_RECIBO_R3_1, R3_1/CONTRATO_KERNEL_RECIBO_R3_1.md) e lido por hash,
    SEM subprocesso, e VINCULADO:
      (a) o sha do recibo == --kernel-recibo-sha256 (o pino de vNNN_pins); sem a flag so em --sandbox;
      (b) campos proibidos (um_py_sha256 etc.): a etapa 2 roda antes do candidato e do rito, nao pode conhece-los;
      (c) rc, sorry e erros sao int estritos e 0; os dois logs (build e Audit) sao LIDOS e NORMALIZADOS (A1b): sha confere, sorry
          (crase e aspas, A1) e erros recontados por script e iguais ao declarado; build log vazio recusa (A2); os axiomas que o log do
          Audit imprime estao no trio {propext, Classical.choice, Quot.sound};
      (d) o manifesto do kernel que o SELO pina (lido em ler_nos): toolchain como LISTA igual (N1m); statuses exigidos true; todo o
          axiom_report no trio; o sha DEPOIS da raiz, do Audit e de cada pedra == formal_files_sha256, e re-hasheado na arvore; o log do
          Audit tem pelo menos tantas linhas de axiomas quantos #print axioms tem o Audit.lean pinado (A2); cada declaracao de cada pedra
          tem entrada no axiom_report, linha no log do Audit e nome na fonte da pedra (N1k);
      (e) o ANTES (raiz, Audit, impressao formal do kernel do Nos) == o kernel anterior registrado no recibo pre-selo; antes == depois
          da impressao; a impressao de formal_files_antes == o ANTES, e as pedras do recibo sao EXATAMENTE os arquivos formais novos ou
          mudados do manifesto pinado pelo selo, fora a raiz e o Audit (N1l);
      (f) os criterios da secao 4 item 6 do plano: o MEDIDO do recibo == o ESPERADO do CRITERIOS_vNNN.json pinado pela cadeia (A3);
          esperado no recibo e recusado.
    Devolve (passa, detalhe, pino)."""
    kp = Path(kp)
    if not kp.is_file():
        return False, "recibo do kernel ausente: " + str(kp), None
    raw = kp.read_bytes()
    pino = dict(path=str(kp), sha256=sha256(raw), bytes=len(raw), sha256_esperado=sha_esperado)

    def falha(msg):
        return False, "recibo do kernel: " + msg, pino

    def lista_de_texto(x):
        return isinstance(x, list) and len(x) > 0 and all(isinstance(s, str) and s.strip() for s in x)
    if sha_esperado is None and not sandbox:
        return falha("sem --kernel-recibo-sha256 (o sha pinado em vNNN_pins); so --sandbox dispensa")
    if sha_esperado is not None and str(sha_esperado).lower() != pino["sha256"]:
        return falha("sha %s != esperado %s (KERNEL_RECIBO_SHA_DIVERGE)" % (pino["sha256"][:16], str(sha_esperado)[:16]))
    try:
        k = json.loads(raw)
    except ValueError as exc:
        return falha("ilegivel: %s" % exc)
    if not isinstance(k, dict):
        return falha("nao e um objeto JSON")
    if k.get("contrato") != KERNEL_CONTRATO:
        return falha("contrato=%r (exigido %s)" % (k.get("contrato"), KERNEL_CONTRATO))
    proibidos = [c for c in KERNEL_CAMPOS_PROIBIDOS if c in k]
    if proibidos:
        return falha("campos PROIBIDOS %s: a etapa 2 roda antes do candidato e do rito e nao pode conhece-los" % proibidos)
    exigidos = ("versao", "rc", "sorry", "erros", "build_full_log", "audit_log", "toolchain", "arvore", "raiz", "audit", "pedras", "axiomas",
                "criterios", "nos_kernel_impressao", "formal_files_antes")
    faltas = [c for c in exigidos if c not in k]
    if faltas:
        return falha("sem os campos %s" % faltas)
    if k["versao"] != versao:
        return falha("e da versao %r, alvo %r" % (k["versao"], versao))
    for c in ("rc", "sorry", "erros"):
        if type(k[c]) is not int or k[c] != 0:
            return falha("%s=%r (exigido int 0; float, bool e texto nao valem)" % (c, k[c]))
    if not isinstance(criterios, dict) or not isinstance(criterios.get("esperados"), dict):
        return falha("sem criterios pinados pela cadeia (--criterios CRITERIOS_vNNN.json + --criterios-sha256): os ESPERADOS da secao 4 item 6 "
                     "nao vem do recibo (A3, CRITERIOS_AUSENTES)")
    # (c) os logs, LIDOS e NORMALIZADOS (A1b)
    logs, codif = {}, {}
    for campo in ("build_full_log", "audit_log"):
        L = k[campo]
        if not isinstance(L, dict) or not isinstance(L.get("path"), str) or not _hex64(L.get("sha256")):
            return falha("%s exige {path, sha256}" % campo)
        lp = Path(L["path"])
        if not lp.is_absolute():
            return falha("%s.path nao e absoluto" % campo)
        if not lp.is_file():
            return falha("%s ausente em disco: %s" % (campo, lp))
        b = lp.read_bytes()
        if sha256(b) != L["sha256"].lower():
            return falha("%s: o arquivo em disco (%s) nao bate com o sha declarado (%s)" % (campo, sha256(b)[:16], L["sha256"][:16]))
        try:
            logs[campo], codif[campo] = normalizar_log(b)
        except Recusa as exc:
            return falha("%s: %s" % (campo, exc))
    if mesmo_no(k["build_full_log"]["path"], k["audit_log"]["path"]):
        return falha("build_full_log e audit_log sao o mesmo arquivo")
    if not logs["build_full_log"].strip():
        return falha("build_full_log vazio (A2: LOG_DE_BUILD_VAZIO; um lake build sempre escreve)")
    n_sorry = sum(len(RE_LOG_SORRY.findall(t)) for t in logs.values())
    n_erros = sum(len(RE_LOG_ERRO.findall(t)) for t in logs.values())
    if n_sorry != k["sorry"]:
        return falha("os logs tem %d ocorrencia(s) de sorry (contadas por script, crase e aspas) e o recibo declara %d" % (n_sorry, k["sorry"]))
    if n_erros != k["erros"]:
        return falha("os logs tem %d linha(s) de erro (contadas por script) e o recibo declara %d" % (n_erros, k["erros"]))
    ax_log, n_ax = set(), 0
    for m in RE_LOG_AXIOMAS.finditer(logs["audit_log"]):
        n_ax += 1
        ax_log |= {a.strip() for a in m.group(1).split(",") if a.strip()}
    n_sem_ax = logs["audit_log"].count("does not depend on any axioms")
    if n_ax + n_sem_ax == 0:
        return falha("o log do Audit nao tem nenhuma linha de #print axioms")
    if not ax_log <= AXIOMAS_TRIO:
        return falha("o log do Audit imprime axiomas fora do trio: %s" % sorted(ax_log - AXIOMAS_TRIO))
    ax = k["axiomas"]
    if not isinstance(ax, list) or not all(isinstance(a, str) for a in ax) or not set(ax) <= AXIOMAS_TRIO:
        return falha("axiomas declarados fora do trio: %r" % (ax,))
    if not ax_log <= set(ax):
        return falha("o log do Audit tem axiomas %s que o recibo nao declara" % sorted(ax_log - set(ax)))
    decl_log = {m.group(1) for m in RE_LOG_DECL.finditer(logs["audit_log"])}
    # (d) o manifesto do kernel que o selo pina
    man, kinfo = nos_info.get("_kernel_man"), nos_info.get("kernel")
    if man is None or kinfo is None:
        return falha("o selo nao pina tgl_kernel_proof_manifest.json: nao ha ancora para o T17")
    mlv, mkv = kinfo.get("lean_version"), kinfo.get("lake_version")
    if not lista_de_texto(mlv) or not lista_de_texto(mkv) or mlv != man.get("lean_version") or mkv != man.get("lake_version"):
        return falha("toolchain do manifesto do kernel pinado pelo selo nao e LISTA nao vazia de texto (lean_version=%r, lake_version=%r) (N1m)" % (mlv, mkv))
    tc = k["toolchain"]
    if not isinstance(tc, dict) or not lista_de_texto(tc.get("lean_version")) or not lista_de_texto(tc.get("lake_version")):
        return falha("toolchain do recibo exige {lean_version: [..], lake_version: [..]} como LISTA nao vazia de texto (N1m): %r" % (tc,))
    if tc["lean_version"] != mlv or tc["lake_version"] != mkv:
        return falha("toolchain do build %r != a do manifesto pinado pelo selo (%r, %r)" % (tc, mlv, mkv))
    st = man.get("statuses") or {}
    falsos = [s for s in KERNEL_STATUSES_EXIGIDOS if st.get(s) is not True]
    if falsos:
        return falha("statuses do manifesto do kernel nao verdadeiros: %s" % falsos)
    ar = man.get("axiom_report")
    if not isinstance(ar, dict) or not ar:
        return falha("manifesto do kernel sem axiom_report")
    fora_trio = [nome for nome, lst in ar.items() if not isinstance(lst, list) or not set(lst) <= AXIOMAS_TRIO]
    if fora_trio:
        return falha("%d entrada(s) do axiom_report fora do trio (ex.: %s)" % (len(fora_trio), fora_trio[0]))
    ff = man.get("formal_files_sha256") or {}
    arvore = Path(str(k["arvore"]))
    if not arvore.is_absolute() or not arvore.is_dir():
        return falha("arvore do build ausente ou nao absoluta: %s" % arvore)
    itens = []
    for campo, rel_esp in (("raiz", "TGLExt.lean"), ("audit", "TGL/Audit.lean")):
        r = k[campo]
        if not isinstance(r, dict) or r.get("path") != rel_esp or not _hex64(r.get("sha256_antes")) or not _hex64(r.get("sha256_depois")):
            return falha("%s exige {path=%r, sha256_antes, sha256_depois}" % (campo, rel_esp))
        itens.append((campo, rel_esp, r["sha256_depois"].lower()))
    pedras = k["pedras"]
    if not isinstance(pedras, list) or not pedras:
        return falha("pedras vazias")
    vistos = set()
    for p in pedras:
        if not isinstance(p, dict) or not isinstance(p.get("path"), str) or not _hex64(p.get("sha256")):
            return falha("pedra exige {path, sha256, declaracoes}: %r" % (p,))
        if not (p["path"].startswith("TGLExt/") and p["path"].endswith(".lean")) or p["path"] in vistos:
            return falha("pedra com caminho invalido ou repetido: %r" % p["path"])
        vistos.add(p["path"])
        itens.append(("pedra", p["path"], p["sha256"].lower()))
    fontes = {}
    for campo, rel, sha in itens:
        if str(ff.get(rel) or "").lower() != sha:
            return falha("%s %s: recibo %s != formal_files_sha256 do manifesto pinado pelo selo %s" % (campo, rel, sha[:16], str(ff.get(rel))[:16]))
        try:
            fp = relativo_seguro(rel, arvore)
        except Recusa as exc:
            return falha("%s %s: %s" % (campo, rel, exc))
        if not fp.is_file():
            return falha("%s %s ausente na arvore %s" % (campo, rel, arvore))
        fb = fp.read_bytes()
        if sha256(fb) != sha:
            return falha("%s %s: o arquivo na arvore mudou depois do recibo" % (campo, rel))
        try:
            fontes[rel] = fb.decode("utf-8-sig")
        except UnicodeDecodeError as exc:
            return falha("%s %s: a fonte nao e UTF-8 (%s)" % (campo, rel, exc))
    # A2 (R3.1): o log do Audit tem de cobrir os #print axioms do Audit.lean PINADO (o sha ja conferido acima)
    n_print = len(RE_PRINT_AXIOMS.findall(fontes["TGL/Audit.lean"]))
    if n_print == 0:
        return falha("o Audit.lean pinado nao tem nenhum #print axioms")
    if n_ax + n_sem_ax < n_print:
        return falha("o log do Audit tem %d linha(s) de axiomas e o Audit.lean pinado tem %d #print axioms (A2: LOG_DO_AUDIT_CURTO; truncado ou de outro Audit)"
                     % (n_ax + n_sem_ax, n_print))
    # N1k (R3.1): cada declaracao de cada pedra tem entrada no axiom_report, linha no log do Audit e nome na fonte da pedra
    n_decl = 0
    for p in pedras:
        dl = p.get("declaracoes")
        if not lista_de_texto(dl) or len(set(dl)) != len(dl):
            return falha("pedra %s exige declaracoes: lista nao vazia e sem repeticao dos nomes que o Audit imprime (N1k)" % p["path"])
        for d in dl:
            if d not in ar:
                return falha("pedra %s: a declaracao %s nao tem entrada no axiom_report do manifesto pinado pelo selo (N1k)" % (p["path"], d))
            if d not in decl_log:
                return falha("pedra %s: a declaracao %s nao foi impressa no log do Audit (N1k)" % (p["path"], d))
            curto = d.split(".")[-1].strip("\\u00ab\\u00bb")
            if not curto or not re.search(r"(?<![\\w'.])" + re.escape(curto) + r"(?![\\w'])", fontes[p["path"]]):
                return falha("pedra %s: a declaracao %s nao e nomeada na fonte da pedra (N1k)" % (p["path"], d))
            n_decl += 1
    # (e) o ANTES e a impressao do kernel do Nos
    imp = k["nos_kernel_impressao"]
    if not isinstance(imp, dict) or not _hex64(imp.get("antes")) or not _hex64(imp.get("depois")):
        return falha("nos_kernel_impressao exige {antes, depois} sha256")
    if imp["antes"].lower() != imp["depois"].lower():
        return falha("a impressao do kernel do Nos mudou durante a etapa 2 (antes %s, depois %s)" % (imp["antes"][:16], imp["depois"][:16]))
    nota_antes = None
    if recibo_pre_selo:
        ka = recibo_pre_selo.get("kernel_anterior") or {}
        for nome, val, esp in (("raiz.sha256_antes", k["raiz"]["sha256_antes"], ka.get("raiz_sha256")),
                               ("audit.sha256_antes", k["audit"]["sha256_antes"], ka.get("audit_sha256")),
                               ("nos_kernel_impressao.antes", imp["antes"], ka.get("impressao_formal"))):
            if str(val).lower() != str(esp).lower():
                return falha("%s %s != o kernel anterior do recibo pre-selo %s" % (nome, str(val)[:16], str(esp)[:16]))
    elif not sandbox:
        return falha("sem recibo pre-selo o ANTES nao e conferivel")
    else:
        nota_antes = "ANTES nao cruzado com recibo pre-selo (sandbox); a impressao de formal_files_antes foi cruzada com nos_kernel_impressao.antes"
    # N1l (R3.1): o conjunto de pedras do recibo cobre EXATAMENTE os arquivos formais novos ou mudados do manifesto pinado pelo selo
    fa = k["formal_files_antes"]
    if not isinstance(fa, dict) or not fa or not all(isinstance(c, str) and _hex64(v) for c, v in fa.items()):
        return falha("formal_files_antes exige o mapa {caminho relativo: sha256} do kernel ANTES (N1l)")
    if impressao_formal(fa) != imp["antes"].lower():
        return falha("a impressao de formal_files_antes %s != nos_kernel_impressao.antes %s (N1l)" % (impressao_formal(fa)[:16], imp["antes"][:16]))
    if str(fa.get("TGLExt.lean") or "").lower() != k["raiz"]["sha256_antes"].lower() or str(fa.get("TGL/Audit.lean") or "").lower() != k["audit"]["sha256_antes"].lower():
        return falha("formal_files_antes nao traz a raiz e o Audit do ANTES declarado (N1l)")
    removidos = sorted(set(fa) - set(ff))
    if removidos:
        return falha("%d arquivo(s) formal(is) do ANTES ausente(s) no manifesto pinado pelo selo (ex.: %s): remocao nao e pedra (N1l)" % (len(removidos), removidos[0]))
    mudados = {c for c in ff if str(ff[c]).lower() != str(fa.get(c) or "").lower()} - {"TGLExt.lean", "TGL/Audit.lean"}
    fora_tglext = sorted(c for c in mudados if not (c.startswith("TGLExt/") and c.endswith(".lean")))
    if fora_tglext:
        return falha("arquivo(s) formal(is) novo(s) ou mudado(s) fora de TGLExt/ no manifesto pinado pelo selo: %s (N1l)" % fora_tglext[:5])
    nao_listadas = sorted(mudados - vistos)
    if nao_listadas:
        return falha("pedra(s) selada(s) nova(s) ou mudada(s) NAO listada(s) no recibo: %s (N1l)" % nao_listadas[:5])
    nao_novas = sorted(vistos - mudados)
    if nao_novas:
        return falha("pedra(s) do recibo que nao sao novas nem mudadas no manifesto pinado pelo selo: %s (N1l)" % nao_novas[:5])
    # (f) os criterios: MEDIDO do recibo contra o ESPERADO pinado (A3)
    cr = k["criterios"]
    if not isinstance(cr, dict):
        return falha("criterios nao e objeto")
    for nome in KERNEL_CRITERIOS_EXIGIDOS:
        c = cr.get(nome)
        if not isinstance(c, dict) or "medido" not in c:
            return falha("criterio %s ausente ou sem {medido}" % nome)
        if "esperado" in c:
            return falha("criterio %s: o recibo traz esperado PROPRIO (%r); os esperados vem do CRITERIOS pinado pela cadeia (A3: CRITERIO_AUTODECLARADO)" % (nome, c["esperado"]))
        if set(c) != {"medido"}:
            return falha("criterio %s: chaves %s (so 'medido' e admitida)" % (nome, sorted(c)))
        esp = criterios["esperados"][nome]
        if type(c["medido"]) is not type(esp) or c["medido"] != esp:
            return falha("criterio %s: medido %r != esperado %r do CRITERIOS pinado %s" % (nome, c["medido"], esp, str(criterios.get("sha256"))[:16]))
    sobra = sorted(set(cr) - set(KERNEL_CRITERIOS_EXIGIDOS))
    if sobra:
        return falha("criterios fora do contrato: %s" % sobra)
    pino.update(contrato=KERNEL_CONTRATO, logs=dict(sorry_contados=n_sorry, erros_contados=n_erros, linhas_de_axiomas=n_ax + n_sem_ax,
                                                     print_axioms_no_audit_pinado=n_print, axiomas_no_log=sorted(ax_log), codificacao=codif,
                                                     normalizacao="BOM UTF-16/UTF-8; UTF-8 estrito; CR -> LF; sem ANSI; sem controle; NFKC; sem Cf"),
                manifesto_do_kernel=dict(sha256=kinfo.get("sha256"), statuses_exigidos=list(KERNEL_STATUSES_EXIGIDOS), toolchain=dict(lean_version=mlv, lake_version=mkv)),
                n_pedras=len(pedras), n_declaracoes_das_pedras=n_decl, pedras_cobrem_o_diff_formal=True,
                criterios=dict(path=criterios.get("path"), sha256=criterios.get("sha256"), x19=criterios.get("x19")),
                antes=nota_antes or "cruzado com o recibo pre-selo")
    return True, "recibo do kernel %s (%s): versao=%s rc=0 sorry=0 erros=0 (recontados nos logs normalizados); %d pedras (%d declaracoes no axiom_report, no log e na fonte) + raiz + Audit == manifesto do kernel %s pinado pelo selo e re-hasheados; pedras == diff formal; log do Audit >= %d #print axioms; criterios == CRITERIOS %s (x19=%s); statuses e axiomas no trio; %s" % (
        pino["sha256"][:16], KERNEL_CONTRATO, versao, len(pedras), n_decl, str(kinfo.get("sha256"))[:16], n_print, str(criterios.get("sha256"))[:16],
        criterios.get("x19"), pino["antes"]), pino


'''
assert txt.count(VELHA_VKR) == 1
TROCAS.append((VELHA_VKR, NOVA_VKR))

# ------------------------------------------------------------------ A4: montar_comando com o lancador; ambiente com APPDATA vazio
troca('''    final = [sys.executable, *FLAGS_ISOLAMENTO, *opts, script, *sub[i + 1:]]
    return sub, final, sp''', '''    # A4 (R3.1): o filho roda o LANCADOR pinado (sha no recibo), que poe o site do usuario como caminho e executa o script pinado
    if not ctx.get("_lancador"):
        raise Recusa("LANCADOR_AUSENTE: o isolamento A4 nao foi preparado")
    final = [sys.executable, *FLAGS_ISOLAMENTO, *opts, str(ctx["_lancador"]), str(ctx.get("_site_usuario") or "-"), script, *sub[i + 1:]]
    return sub, final, sp''')
troca('''def ambiente_limpo():
    """N5: o ambiente dos testes sem NENHUMA variavel PYTHON* herdada (PYTHONPATH, PYTHONHOME, PYTHONSTARTUP, PYTHONUSERBASE...);
    -E ja as ignora no filho, e a limpeza protege os netos (testes que chamam sys.executable)."""
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("PYTHON")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    return env
''', '''def ambiente_limpo(appdata=None, site_usuario=None):
    """N5: o ambiente dos testes sem NENHUMA variavel PYTHON* herdada (PYTHONPATH, PYTHONHOME, PYTHONSTARTUP, PYTHONUSERBASE...);
    -E ja as ignora no filho, e a limpeza protege os netos (testes que chamam sys.executable).
    A4 (R3.1): APPDATA aponta uma pasta VAZIA nova do sandbox (o site do usuario de quem herdasse o APPDATA nao existe); os netos
    recebem PYTHONNOUSERSITE=1 (o -s deles) e, como unico PYTHON* posto pelo esboco alem dos dois de sempre, PYTHONPATH = o site do
    usuario achado pela pasta conhecida do Windows: entra como CAMINHO, sem .pth e sem usercustomize."""
    env = {k: v for k, v in os.environ.items() if not k.upper().startswith("PYTHON")}
    env.update(PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    if appdata is not None:
        env["APPDATA"] = str(appdata)
        env["PYTHONNOUSERSITE"] = "1"
        if site_usuario:
            env["PYTHONPATH"] = str(site_usuario)
    return env


def pasta_appdata_conhecida():
    """A4 (R3.1): a pasta Roaming do perfil pela API de pastas conhecidas do Windows (SHGetKnownFolderPath, FOLDERID_RoamingAppData),
    NAO pela variavel APPDATA herdada (que um atacante pode apontar para um site com .pth e usercustomize). None fora do Windows."""
    if os.name != "nt":
        return None
    import ctypes
    import uuid
    from ctypes import wintypes

    class _GUID(ctypes.Structure):
        _fields_ = [("Data1", wintypes.DWORD), ("Data2", wintypes.WORD), ("Data3", wintypes.WORD), ("Data4", ctypes.c_ubyte * 8)]
    u = uuid.UUID("{3EB685DB-65F9-4CF6-A03A-E3EF65729F3D}")
    g = _GUID(u.fields[0], u.fields[1], u.fields[2], (ctypes.c_ubyte * 8).from_buffer_copy(u.bytes[8:]))
    p = ctypes.c_wchar_p()
    hr = ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(g), 0, None, ctypes.byref(p))
    try:
        return p.value if hr == 0 else None
    finally:
        ctypes.windll.ole32.CoTaskMemFree(p)


def site_do_usuario_real():
    base = pasta_appdata_conhecida()
    if not base:
        return None
    ver = sys.winver.replace(".", "") if hasattr(sys, "winver") else "%d%d" % sys.version_info[:2]
    return os.path.join(base, "Python", "Python" + ver, "site-packages")


def _pin_arquivo(p):
    b = Path(p).read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha256(b))


def preparar_isolamento(saida):
    """A4 (R3.1): grava o lancador (bytes == LANCADOR_FONTE, sha no recibo), acha o site do usuario pela pasta conhecida, recusa se ele
    sombrear a stdlib ou trouxer sitecustomize/usercustomize (que rodariam nos netos pelo PYTHONPATH), e mede o RESIDUO: os .pth e os
    customize do site do SISTEMA (e da stdlib), que o -s nao corta e que executam em todo filho. Nada fora de --saida e escrito."""
    saida = Path(saida)
    lanc = saida / "lancador" / LANCADOR_NOME
    if lanc.exists():
        if lanc.read_bytes() != LANCADOR_FONTE.encode("utf-8"):
            raise Recusa("LANCADOR_ALTERADO: " + str(lanc))
    else:
        gravar_novo(lanc, LANCADOR_FONTE.encode("utf-8"))
    su = site_do_usuario_real()
    try:
        su_herdado = site.getusersitepackages()
    except Exception as exc:
        su_herdado = "indisponivel: %s" % exc
    info = dict(lancador=dict(path=str(lanc), sha256=LANCADOR_SHA256), flags=list(FLAGS_ISOLAMENTO),
                site_do_usuario=dict(path=su, achado_por="SHGetKnownFolderPath(FOLDERID_RoamingAppData), nao pelo APPDATA herdado",
                                     pelo_appdata_herdado=su_herdado, iguais=(su is not None and os.path.normcase(str(su)) == os.path.normcase(str(su_herdado)))),
                appdata="pasta vazia nova por teste em <saida>/appdata_vazio/<id>", netos="PYTHONNOUSERSITE=1; PYTHONPATH = site do usuario (so caminho)")
    if su and os.path.isdir(su):
        nomes = {m.name for m in pkgutil.iter_modules([su])}
        sombra = sorted(nomes & set(sys.stdlib_module_names))
        if sombra:
            raise Recusa("SITE_DO_USUARIO_SOMBREIA_A_STDLIB: %s (no PYTHONPATH dos netos viria antes da stdlib)" % sombra)
        custom = sorted(n for n in os.listdir(su) if n.split(".")[0].lower() in ("sitecustomize", "usercustomize"))
        if custom:
            raise Recusa("SITE_DO_USUARIO_COM_CUSTOMIZE: %s (rodaria nos netos pelo PYTHONPATH)" % custom)
        info["site_do_usuario"]["pth_que_NAO_executam_mais"] = [_pin_arquivo(os.path.join(su, n)) for n in sorted(os.listdir(su)) if n.lower().endswith(".pth")]
    else:
        info["site_do_usuario"]["path"] = su = None
    import sysconfig
    dirs = []
    for d in list(site.getsitepackages()) + [sysconfig.get_paths().get(x) for x in ("stdlib", "platstdlib", "purelib", "platlib")]:
        if d and os.path.isdir(d) and not any(os.path.normcase(d) == os.path.normcase(x) for x in dirs):
            dirs.append(d)
    resid = []
    for d in dirs:
        for n in sorted(os.listdir(d)):
            fp = os.path.join(d, n)
            if os.path.isfile(fp) and (n.lower().endswith(".pth") or n.split(".")[0].lower() in ("sitecustomize", "usercustomize")):
                resid.append(_pin_arquivo(fp))
    info["residuo_declarado"] = dict(
        pth_e_customize_do_site_do_sistema_que_executam=resid, pastas_varridas=dirs,
        codigo_do_site_do_usuario="os pacotes do site do usuario (numpy, scipy, torch...) seguem importaveis e NAO pinados; o -s e o lancador so cortam .pth e usercustomize",
        esboco="o proprio esboco processa o site do usuario dele se nao for chamado com -s (a cadeia chama com -s; remissao R3.1)")
    return info, str(lanc), su
''')

# ------------------------------------------------------------------ rodar_bateria: criterios (A3) e isolamento (A4)
troca('''def rodar_bateria(bateria, ctx, recibos_dir, modo, fase="pos_selo", sandbox=False, recibo_pre_selo=None, nos_info=None, copias_feitas=()):
    recibos_dir = Path(recibos_dir)
    recibos_dir.mkdir(parents=True, exist_ok=True)
    copias_dst = [c["para"] for c in copias_feitas]
    resultados = []''', '''def rodar_bateria(bateria, ctx, recibos_dir, modo, fase="pos_selo", sandbox=False, recibo_pre_selo=None, nos_info=None, copias_feitas=(), criterios=None):
    recibos_dir = Path(recibos_dir)
    recibos_dir.mkdir(parents=True, exist_ok=True)
    copias_dst = [c["para"] for c in copias_feitas]
    resultados = []
    iso = None   # A4: preparado so quando o primeiro teste com subprocesso vai rodar''')
troca('''                passa, detalhe, pino = verificar_kernel_recibo(kp, ctx["versao"], nos_info, ctx.get("kernel_recibo_sha256") or None,
                                                               recibo_pre_selo, sandbox)''', '''                passa, detalhe, pino = verificar_kernel_recibo(kp, ctx["versao"], nos_info, ctx.get("kernel_recibo_sha256") or None,
                                                               recibo_pre_selo, sandbox, criterios)''')
troca('''        fontes_pin = t.get("fontes", [])
        # N16: gramatica fechada; N5: -E -P na frente, ambiente sem PYTHON*, cwd numa pasta vazia nova, sem modulo-sombra
        try:''', '''        fontes_pin = t.get("fontes", [])
        if iso is None:
            iso, ctx["_lancador"], ctx["_site_usuario"] = preparar_isolamento(ctx["saida"])
        # N16: gramatica fechada; N5: -E -P na frente, ambiente sem PYTHON*, cwd numa pasta vazia nova, sem modulo-sombra; A4: -s e lancador
        try:''')
troca('''        rec["cwd"] = str(cwd)
        rec["comando_executado"] = final          # so existe quando o subprocesso de fato roda''', '''        rec["cwd"] = str(cwd)
        # A4 (R3.1): APPDATA numa pasta vazia NOVA por teste; o lancador conferido byte a byte antes de cada execucao
        appdata = Path(ctx["saida"]) / "appdata_vazio" / tid
        try:
            appdata.mkdir(parents=True, exist_ok=False)
        except OSError as exc:
            rec.update(resultado="FALHA", detalhe="APPDATA_NAO_E_PASTA_NOVA: %s" % exc, fim=agora())
            resultados.append(rec)
            continue
        if Path(ctx["_lancador"]).read_bytes() != LANCADOR_FONTE.encode("utf-8"):
            rec.update(resultado="FALHA", detalhe="LANCADOR_ALTERADO: %s (nada executado)" % ctx["_lancador"], fim=agora())
            resultados.append(rec)
            continue
        rec["isolamento"] = dict(appdata=str(appdata), pythonpath_dos_netos=ctx["_site_usuario"], lancador_sha256=LANCADOR_SHA256, script=str(script))
        rec["comando_executado"] = final          # so existe quando o subprocesso de fato roda''')
troca('''                               timeout=float(t.get("timeout_s", 900)), env=ambiente_limpo())''',
      '''                               timeout=float(t.get("timeout_s", 900)), env=ambiente_limpo(appdata, ctx["_site_usuario"]))''')
troca('''                isolamento=dict(flags=list(FLAGS_ISOLAMENTO), ambiente="sem PYTHON* herdado", cwd="pasta vazia nova por teste",
                                sombra="modulo-sombra ao lado de fonte pinada = FALHA",
                                limite="site do USUARIO admitido: numpy/scipy/torch vivem nele (-I/-s/-S os cortariam)"))''',
      '''                isolamento=dict(flags=list(FLAGS_ISOLAMENTO), ambiente="sem PYTHON* herdado; APPDATA vazio por teste; PYTHONNOUSERSITE=1 e PYTHONPATH=site do usuario nos netos",
                                cwd="pasta vazia nova por teste", sombra="modulo-sombra ao lado de fonte pinada = FALHA",
                                preparado=iso,
                                limite="A4 [residuo declarado]: o site do usuario entra como caminho (numpy/scipy/torch vivem nele) sem .pth nem usercustomize; os .pth do site do sistema ainda executam (lista em preparado.residuo_declarado)"))''')

# ------------------------------------------------------------------ N4b: sonda -> compara -> troca
troca('''        if tmp.read_bytes() != novo_bytes:
            raise Recusa("ESCRITA_CURTA_DO_MANIFESTO")
        if man_p.read_bytes() != antes_esperado:
            raise Recusa("MANIFESTO_MUDOU_DESDE_A_LEITURA: entre o backup e a troca; nada trocado")
        guarda_servico("imediatamente_antes_da_troca")
        os.replace(tmp, man_p)''', '''        if tmp.read_bytes() != novo_bytes:
            raise Recusa("ESCRITA_CURTA_DO_MANIFESTO")
        guarda_servico("imediatamente_antes_da_troca")
        # N4b (R3.1): a comparacao vem DEPOIS da sonda (que leva ate 1,5 s com a porta fechada) e imediatamente antes do os.replace
        if man_p.read_bytes() != antes_esperado:
            raise Recusa("MANIFESTO_MUDOU_DESDE_A_LEITURA: entre o backup e a troca (comparado depois da ultima sonda); nada trocado")
        os.replace(tmp, man_p)''')

# ------------------------------------------------------------------ main: flags, criterios, N3a
troca('''    ap.add_argument("--fase", choices=("pre_selo", "pos_selo"), default="pos_selo",''', '''    ap.add_argument("--criterios", default=None, help="A3 (R3.1): CRITERIOS_vNNN.json (contrato CRITERIOS_R3_1) com os ESPERADOS da secao 4 item 6; obrigatorio com --kernel-recibo")
    ap.add_argument("--criterios-sha256", default=None, help="A3 (R3.1): sha256 esperado do CRITERIOS_vNNN.json (lido de vNNN_pins); obrigatorio com --criterios")
    ap.add_argument("--fase", choices=("pre_selo", "pos_selo"), default="pos_selo",''')
troca('''                  python_ignore_environment=bool(sys.flags.ignore_environment), saida=dict(dir=str(saida), raiz_admitida=raiz_admitida),''',
      '''                  python_ignore_environment=bool(sys.flags.ignore_environment), python_no_user_site=bool(sys.flags.no_user_site),
                  saida=dict(dir=str(saida), raiz_admitida=raiz_admitida),''')
troca('''    try:
        guarda_servico("inicio")
        if a.modo == "aplicar" and a.sem_bateria:''', '''    estado_run = dict(novo_sha256=None)

    def pos_rollback(msg):
        """N3a (R3.1): depois de um rollback (APLICACAO_REVERTIDA) na producao em aplicar, o servico e sondado de novo: se responde, pode ter
        lido o manifesto NOVO em RAM no instante do os.replace, e o disco voltou ao ANTERIOR; recusa com codigo proprio e exige reinicio."""
        no_ar = bool(servico_responde())
        recibo["sondagens_do_servico"].append(dict(momento="apos_rollback", no_ar=no_ar, quando=agora()))
        try:
            disco = sha256((bancada / "canonical_contracts.json").read_bytes())
        except OSError as exc:
            disco = "ilegivel: %s" % exc
        recibo["aplicacao_revertida"] = dict(manifesto_novo_sha256=estado_run["novo_sha256"], manifesto_em_disco_sha256=disco,
                                             servico_no_ar_apos_rollback=no_ar, nota=N3A_NOTA)
        if no_ar:
            return ("SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO: o servico respondeu depois do rollback; se subiu no instante do os.replace, "
                    "guardou em RAM o manifesto NOVO (%s) e o disco voltou ao ANTERIOR (%s): pare e religue o um_bancada.py com recibo de identidade "
                    "(10-ter) antes de qualquer B(n). Causa do rollback: %s" % (str(estado_run["novo_sha256"])[:16], str(disco)[:16], msg))
        return msg

    try:
        guarda_servico("inicio")
        if a.modo == "aplicar":
            recibo["servico_e_manifesto_em_ram"] = N3A_NOTA
        if a.modo == "aplicar" and a.sem_bateria:''')
troca('''        # a bateria (A7): pinada antes de qualquer outra leitura
        bateria, bateria_raw, bateria_sha = carregar_bateria(bateria_p, a.bateria_sha256, a.modo, a.fase, a.sandbox)''', '''        # A3 (R3.1): os ESPERADOS dos criterios vem de um arquivo pinado pela cadeia, nunca do recibo do kernel
        criterios = None
        if a.criterios:
            criterios = carregar_criterios(a.criterios, a.criterios_sha256, a.versao)
            recibo["criterios"] = dict(criterios)
        elif a.criterios_sha256:
            raise Recusa("CRITERIOS_AUSENTES: --criterios-sha256 sem --criterios")
        if a.kernel_recibo and criterios is None:
            raise Recusa("CRITERIOS_AUSENTES: com --kernel-recibo a cadeia passa --criterios CRITERIOS_vNNN.json e --criterios-sha256 (lido de vNNN_pins); "
                         "os esperados da secao 4 item 6 nao vem do recibo (A3)")
        # a bateria (A7): pinada antes de qualquer outra leitura
        bateria, bateria_raw, bateria_sha = carregar_bateria(bateria_p, a.bateria_sha256, a.modo, a.fase, a.sandbox)''')
troca('''            novo_bytes = json_bytes(novo)
            contrato = (rotulo, md)''', '''            novo_bytes = json_bytes(novo)
            estado_run["novo_sha256"] = sha256(novo_bytes)
            contrato = (rotulo, md)''')
troca('''            recibo["bateria_resultado"] = rodar_bateria(bateria, ctx, saida / "recibos", a.modo, a.fase, a.sandbox, recibo.get("recibo_pre_selo"), nos_info, copias_feitas)''',
      '''            recibo["bateria_resultado"] = rodar_bateria(bateria, ctx, saida / "recibos", a.modo, a.fase, a.sandbox, recibo.get("recibo_pre_selo"), nos_info, copias_feitas,
                                                        criterios)''')
troca('''    except Recusa as exc:
        return fechar("RECUSADA", 2, str(exc))
    except Exception as exc:   # qualquer erro nao previsto''', '''    except Recusa as exc:
        msg = str(exc)
        if msg.startswith("APLICACAO_REVERTIDA") and producao and a.modo == "aplicar":
            msg = pos_rollback(msg)
        return fechar("RECUSADA", 2, msg)
    except Exception as exc:   # qualquer erro nao previsto''')

# ------------------------------------------------------------------ aplicar
for velho, novo in TROCAS:
    n = txt.count(velho)
    assert n == 1, "troca nao unica (%d): %r" % (n, velho[:120])
    txt = txt.replace(velho, novo, 1)
dados = txt.encode("utf-8")
compile(dados, str(ALVO), "exec")
tmp = ALVO.with_name(ALVO.name + ".tmp_patch")
with open(tmp, "xb") as f:
    f.write(dados)
assert tmp.read_bytes() == dados
os.replace(tmp, ALVO)
assert ALVO.read_bytes() == dados
print("ok", len(TROCAS), "trocas;", hashlib.sha256(dados).hexdigest()[:16], len(dados), "bytes")

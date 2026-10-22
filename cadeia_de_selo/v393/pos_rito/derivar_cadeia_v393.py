# -*- coding: utf-8 -*-
"""derivar_cadeia_v393.py -- DERIVA a cadeia pos-rito da v393 a partir do molde REAL da v392 (cadeia_de_selo\\v392\\pos_rito) (molde do derivar: derivar_cadeia_v392.py).
GERA (por copia com subida de versao v392 -> v393, v391 -> v392, k392 -> k393, e edicoes com assert de contagem): leitura_v393.py, superficies_v393.py, fechar_v393.py, b3_recibo_v393.py, chain_pos_rito_v393.sh.
JA ESCRITOS A MAO (sobre o molde; este deriva so' os CONFERE): textos_v393.py, registrar_mapa_v393.py.
DESCARTADOS do molde (especificos da v392): patch_arvore_indice (CR-08, CR-02), errata_claude_md (rascunho da v392), nota_handoff. Os passos 3/4 da cadeia que dependiam do patch tornam-se OPCIONAIS
(rodam so' se existir patch_arvore_indice_v393.py); o passo 7 nao chama mais a errata do CLAUDE.md da raiz.
CONFERE: cada invariante do molde sobrevive (a guarda da palavra recusada, o backup de bytes, temporario -> substituir, a recusa quando a leitura tem problema...); ast.parse em cada .py e sh -n no .sh.
GRAVA: DERIVACAO_v393.json (sha16 de cada molde e de cada derivado, invariantes, sintaxe, descartados). NAO EXECUTA nenhum script derivado.
Uso: python -I -B -X utf8 derivar_cadeia_v393.py"""
import ast, hashlib, json, os, re, shutil, subprocess, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PK = os.path.dirname(HERE)
MOLDE = os.path.join(os.path.dirname(PK), "v392", "pos_rito")
STAMP = time.strftime("%Y%m%d_%H%M%S")
sha16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
PROT = ["varredura_e_sorry_v392", "estatuto_da_prova_v391", "fundacao_v390", "three_stress_tests_v387"]   # nomes de registros que NAO sobem de versao (vizinhos da troca dita e fixos antigos)


def bump(t):
    for i, p in enumerate(PROT):
        t = t.replace(p, "@@P%d@@" % i)
    t = t.replace("v392", "@@N@@").replace("v391", "v392").replace("@@N@@", "v393").replace("k392", "k393")
    for i, p in enumerate(PROT):
        t = t.replace("@@P%d@@" % i, p)
    return t


def rd(d, n):
    return open(os.path.join(d, n), encoding="utf-8").read()


def troca(t, old, new, n=1, nome=""):
    assert t.count(old) == n, ("troca", nome or old[:70], t.count(old), n)
    return t.replace(old, new)


def bloco(t, ini, fim):
    """(i, j): do inicio da unica linha que COMECA por `ini` ate o inicio da primeira linha posterior que comeca por `fim` (exclusive)."""
    L = t.split("\n"); a = [k for k, l in enumerate(L) if l.startswith(ini)]; assert len(a) == 1, ("ancora inicial", ini, len(a))
    b = [k for k, l in enumerate(L) if k > a[0] and l.startswith(fim)]; assert b, ("ancora final", fim)
    return a[0], b[0], L


def subst_bloco(t, ini, fim, novo):
    i, j, L = bloco(t, ini, fim)
    return "\n".join(L[:i] + novo.rstrip("\n").split("\n") + L[j:])


def grava(nome, texto):
    p = os.path.join(HERE, nome)
    if os.path.exists(p):
        raw = open(p, "rb").read()
        if raw == texto.encode("utf-8"):
            return
        bk = p + ".bak_" + STAMP + "_c1"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
    tmp = p + ".tmp_" + STAMP
    open(tmp, "wb").write(texto.encode("utf-8")); assert os.path.getsize(tmp) == len(texto.encode("utf-8")); os.replace(tmp, p)
    assert open(p, "rb").read() == texto.encode("utf-8")


MOL = {}   # nome do molde -> texto
for n in ("leitura_v392.py", "superficies_v392.py", "fechar_v392.py", "b3_recibo_v392.py", "chain_pos_rito_v392.sh", "textos_v392.py", "registrar_mapa_v392.py",
          "patch_arvore_indice_v392.py", "errata_claude_md_v392.py", "nota_handoff.py", "derivar_cadeia_v392.py"):
    MOL[n] = rd(MOLDE, n)
INSTALAR_MOLDE = open(os.path.join(os.path.dirname(PK), "v392", "derivar_instalar_rito_v392.py"), "rb").read()

# =============================================================================== leitura_v393.py
t = bump(MOL["leitura_v392.py"])
t = troca(t, 'REG_FIXOS = ("pedras_v393", "varredura_e_sorry_v392")',
          'REG_FIXOS = ("pedras_v393", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393")   # + os registros por spec de ESPERADOS[registros_v393] (REG_TODOS, dentro de ler)', nome="REG_FIXOS")
t = troca(t, "    ap, app = _aplicado()\n", "    ap, app = _aplicado()\n    REG_TODOS = tuple(REG_FIXOS) + tuple(ESP['registros_v393'])\n", nome="REG_TODOS")
t = troca(t, "V['escada_antes'] = ESP['escada'][0]; V['escada_depois'] = ESP['escada'][1]", "V['escada_antes'] = ESP['escada_v392_e_v393'][0]; V['escada_depois'] = ESP['escada'][1]", nome="escada")
t = troca(t, "    for k in REG_FIXOS:\n        if k not in novos:", "    for k in REG_TODOS:\n        if k not in novos:", nome="for REG_FIXOS")
t = troca(t, "(k in REG_FIXOS and r.get('all_verified') is not True)", "(k in REG_TODOS and r.get('all_verified') is not True)", nome="k in REG_FIXOS")
t = troca(t, "for k, v in ESP['verbatins'].items()}", "for k, v in ESP['cunhagens'].items()}", nome="verbatins")
t = troca(t, "tem de ser a v392", "tem de ser a v393", n=t.count("tem de ser a v392")) if "tem de ser a v392" in t else t
NOVO_BLOCO = r'''    # --- v393: a regra e o coracao (registros fixos e por spec) conferidos contra o ensaio a seco registrado em ESPERADOS; nenhum numero e' digitado
    V['reg_todos'] = list(REG_TODOS)
    rc = core.get('regra_consumidor_v393') or {}; co = core.get('coracao_e_selo_gravitacional_v393') or {}; cu = core.get('cunhagens_regra_v393') or {}; kh = core.get('kh_n1_cobertura_v393') or {}
    cov = (core.get('kernel_formalization') or {}).get('axiom_coverage_v392') or {}
    NC = ESP['numeros_do_consumidor']; CB = ESP['cobertura_kh_n1']
    sa = rc.get('satisfacao') or {}; cr = rc.get('criterio') or {}; nu = rc.get('numeros') or {}; rx = rc.get('replica_do_codex') or {}; sr = co.get('satisfacao_pela_regra') or {}
    ei = co.get('evidencia_espectral_independente') or {}
    V['cons'] = {'verdict': rc.get('verdict'), 'pontos': nu.get('pontos'), 'verificacoes': nu.get('verificacoes'), 'compl_ini': nu.get('complemento_inicial'), 'compl_fin': nu.get('complemento_final'),
                 'dimfix': nu.get('dimensao_fixa_complexa'), 'tol': cr.get('tolerancia_numerica'), 'hash_final': nu.get('ultimo_hash_da_trajetoria'), 'replica_hash_igual': rx.get('hash_final_igual')}
    V['cora'] = {'verdict': co.get('verdict'), 'prev': co.get('previsao_independente'), 'G': co.get('G_derivado'), 'criterio': sr.get('criterio'), 'veredito_regra': sr.get('veredito_da_regra'),
                 'espectral_hoje': ei.get('hoje')}
    V['kh'] = {'decl': cov.get('decl'), 'thm': cov.get('thm'), 'fora': cov.get('fora_do_trio'), 'nao_lidas': cov.get('nao_lidas_pelo_regex'), 'verdict': kh.get('verdict')}
    V['cunh_verdict'] = cu.get('verdict')
    for ok_, msg_ in ((pv.get('verdict') == ESP['veredito_pedras_do_ensaio'], 'pedras_v393: o veredito difere do ensaio a seco'),
                      (pv.get('bandeiras') == [ESP['n_bandeiras_novas']] * 2 and pv.get('declaracoes_no_trio') == [ESP['n_bandeiras_novas']] * 2, 'pedras_v393: bandeiras/declaracoes != ESPERADOS'),
                      (rc.get('verdict') == ESP['veredito_consumidor_do_ensaio'], 'regra_consumidor_v393: o veredito difere do ensaio a seco'),
                      (nu.get('pontos') == NC['pontos'] and nu.get('verificacoes') == NC['verificacoes'] and nu.get('ultimo_hash_da_trajetoria') == NC['ultimo_hash_da_trajetoria'],
                       'regra_consumidor_v393: pontos/verificacoes/hash final != ESPERADOS'),
                      (cr.get('igualdade_exata_afirmada') is False, 'regra_consumidor_v393: afirma igualdade exata (deve ser falso)'),
                      (sa.get('veredito_do_rito') == 'SATISFACTION_ADMITTED' and sa.get('veredito_incompativel') == 'SATISFACTION_REFUSED', 'regra_consumidor_v393: admitida/recusada != esperado'),
                      (co.get('verdict') == ESP['veredito_coracao_do_ensaio'], 'coracao_e_selo_gravitacional_v393: o veredito difere do ensaio a seco'),
                      (co.get('previsao_independente') is False and co.get('G_derivado') is False, 'coracao: previsao independente ou G derivado deixou de ser falso'),
                      (co.get('controles_ok') is True and sr.get('admitida') is True, 'coracao: controles negativos ou satisfacao pela regra nao ok'),
                      (cu.get('verdict') == ESP['registros_v393']['cunhagens_regra_v393'], 'cunhagens_regra_v393: o veredito difere de ESPERADOS'),
                      (kh.get('verdict') == ESP['registros_v393']['kh_n1_cobertura_v393'], 'kh_n1_cobertura_v393: o veredito difere de ESPERADOS'),
                      (cov.get('ok') is True and cov.get('decl') == CB['decl'] and cov.get('thm') == CB['thm'] and cov.get('fora_do_trio') == 0 and cov.get('nao_lidas_pelo_regex') == CB['nao_lidas_pelo_regex'],
                       'cobertura KH-N1 do rito != ESPERADOS (constantes, teoremas, fora do trio, nao lidas)'),
                      (all(((pv.get('verbatim') or {}).get(k_) or {}).get('sha256') == v_['sha256'] and ((pv.get('verbatim') or {}).get(k_) or {}).get('embedded_ok') is True for k_, v_ in ESP['cunhagens'].items()),
                       'pedras_v393: alguma cunhagem do operador nao confere por sha256 com ESPERADOS')):
        if not ok_:
            P.append(msg_)
'''
t = troca(t, "    qp = core.get('quantum_pillar_v384') or {}; V['pilar']", NOVO_BLOCO + "    qp = core.get('quantum_pillar_v384') or {}; V['pilar']", nome="qp")
t = troca(t, "# Diferencas para a v392", "# v393: os registros fixos sao pedras_v393, regra_consumidor_v393, coracao_e_selo_gravitacional_v393 (+ os por spec de ESPERADOS[registros_v393]); a escada vem de ESPERADOS[escada_v392_e_v393] e ESPERADOS[escada];\n# a troca dita (so numeros) e' a de ESPERADOS[troca_dita]; os numeros da regra e do coracao sao conferidos contra o ensaio a seco (ESPERADOS), nunca digitados.\n# Diferencas para a v392", nome="cabecalho") if "# Diferencas para a v392" in t else t
ast.parse(t); LEITURA = t

# =============================================================================== superficies_v393.py
t = bump(MOL["superficies_v392.py"])
t = troca(t, "import os, re, sys, time\n", "import os, re, sys, time\n", nome="import")
# cabecalho
i = t.index("# Registro da v393 SELADA"); j = t.index("import os, re, sys, time")
CAB = ("# Registro da v393 SELADA nas superficies de memoria (molde: superficies_v392.py), pela regra da linhagem completa.\n"
       "# Diario (MEMORIA_DA_LINHAGEM, append datado), desenho (ADENDO), Atlas (append datado), TGL_CORE_MEMORY (append datado), o CLAUDE.md da Haja_Luz, as memorias-topico (missao, central, estatuto, e o topico NOVO da v393),\n"
       "# o MEMORY.md/MEMORY_2.md, e (so' sob reivindicacao nomeada em V393_AVISO_REIVINDICACAO) o AVISO_GERENCIA.md da ORDEM_019.\n"
       "# SEM erratas inline nesta versao (as da v392 -- CR-08, a ressalva do estatuto, Coulomb -- eram da v392; a unica errata da v393, a do registro kh_n1_cobertura_v392, vai DENTRO do bloco datado). A funcao\n"
       "# inserir_ao_lado fica disponivel (nao e' chamada); nenhuma errata nova sobre o CLAUDE.md da raiz.\n"
       "# Duas fases (plano conferido ANTES da primeira escrita); backup de BYTES (.bak_<STAMP>_sup393); temporario -> conferir tamanho -> substituir; idempotente pelo marcador de cada bloco;\n"
       "# fim de linha de cada arquivo respeitado. GUARDA: so' grava se a leitura nao tiver problema E se a guarda de texto (P18, cinco regras) estiver limpa em todo texto novo.\n"
       "# Ensaio: --copias <pasta com copias dos alvos> (nada real e' tocado). MEMORY.md: ate 24.000 B e 195 linhas; se passar de 195 linhas, COMPACTA corridas de ganchos antigos (linhas que ja sao ponteiros ao\n"
       "# MEMORY_2.md) num ponteiro unico, com as linhas movidas VERBATIM ao MEMORY_2.md (regra dos dois arquivos).\n")
t = t[:i] + CAB + t[j:]
# as constantes de errata inline
n0 = len(t)
t = re.sub(r"RX_CR08 = \[.*?\]\nRX_V\d+_ENTROU = .*?\nRX_COULOMB = .*?\n", "", t, flags=re.S); assert len(t) < n0, "RX_* nao removidas"
# o bloco das erratas inline
t = subst_bloco(t, "# ---- 1. as erratas ao lado (inline)", "# ---- 2. os appends datados", "# ---- 1. (sem erratas inline na v393: a errata do kh_n1_cobertura_v392 vai dentro do bloco datado da linhagem, do Atlas, do core e do topico novo)\n")
t = troca(t, "    ('(a-leitura-cria-o-objeto-07out.md)', T.linha_palavra(V)),\n", "", nome="TROCAS palavra")
COMPACTA = r'''    lines.insert(kh[0], hl)
    # compactacao: se o indice passar do limite de linhas, junta corridas de ganchos antigos (linhas que ja sao ponteiros ao MEMORY_2.md) num ponteiro; as linhas vao VERBATIM ao MEMORY_2.md
    gancho = lambda l: l.startswith('- [') and 'MEMORY_2.md (' in l and '**' not in l and 'linhas íntegras' not in l and 'handoff-v39' not in l and 'Ganchos antigos' not in l
    ALVO = LIMITE_LINHAS - 3
    if len(lines) - 1 > ALVO:
        corridas = []; k = 0
        while k < len(lines):
            if gancho(lines[k]):
                k2 = k
                while k2 + 1 < len(lines) and gancho(lines[k2 + 1]):
                    k2 += 1
                if k2 > k:
                    corridas.append((k, k2))
                k = k2 + 1
            else:
                k += 1
        escolhidas = []; falta = (len(lines) - 1) - ALVO
        for a_, b_ in sorted(corridas, key=lambda ab: -(ab[1] - ab[0])):
            if falta <= 0:
                break
            escolhidas.append((a_, b_)); falta -= (b_ - a_)
        if falta > 0:
            print('SUPERFICIES RECUSADAS -- o MEMORY.md nao pode ser compactado o bastante (faltam %d linhas): nada foi escrito' % falta); sys.exit(3)
        for a_, b_ in sorted(escolhidas, reverse=True):
            movidas.extend(lines[a_:b_ + 1])
            ptr = '- [Ganchos antigos consolidados (%d)](MEMORY_2.md) — %d linhas íntegras no MEMORY_2.md (movidas %s pela regra dos dois arquivos)' % (b_ - a_ + 1, b_ - a_ + 1, V['data'][:5])
            guarda(ptr, 'MEMORY.md (ponteiro)'); lines[a_:b_ + 1] = [ptr]
            print('  MEMORY.md compactado: %d linhas de ganchos antigos -> 1 ponteiro (verbatim no MEMORY_2)' % (b_ - a_ + 1))
'''
t = troca(t, "    lines.insert(kh[0], hl)\n", COMPACTA, nome="insert handoff")
ast.parse(t); SUPERFICIES = t

# =============================================================================== fechar_v393.py
t = bump(MOL["fechar_v392.py"])
t = troca(t, '"decisoes_da_gerencia_13out_sha16": s16(os.path.join(PK, "DECISOES_GERENCIA_13out.md")),',
          '"insumo_codex_regra_sha16": s16(os.path.join(PK, "insumos", "AO_CLAUDE_INTEGRAR_REGRA_V393.md")),', nome="decisoes")
t = troca(t, "as pedras do kernel e os consertos de barreira; ", "a regra e o coração; ", nome="descricao")
t = troca(t, "[[v393-selada-pedras-e-barreiras-13out]]", "[[v393-selada-a-regra-e-o-coracao-14out]]", nome="link topico")
t = troca(t, "os verbatins do operador de 13/10 por sha256", "as quatro cunhagens do operador de 14/10 por sha256", nome="verbatins")
t = troca(t, r"as pedras novas (`work\\cadeia_de_selo\\v393_kernel\\pedras`)", r"as três pedras da regra (`work\\cadeia_de_selo\\v393_kernel\\pedras`)", nome="pedras")
ast.parse(t)
# as duas trocas acima dependem de quebras de linha exatas do molde: faco por regex tolerante, com assert
n0 = t
t = re.sub(r"a pasta nova do cache \"\n\s*\"\(recibos da bateria e a fotografia F7\.2\) vai ao espelho com PORTA; as erratas do espelho \(a atribuição do resíduo de √2; o neutrino e o D1; a lei de campo curva\); o runner da Fronteira v59 e a camada v393 \"\n\s*\"dos 16 dispositivos; quatro céticos independentes antes do portão do operador\.",
           'os recibos da bateria do B(3) vão ao espelho com PORTA; a errata ao lado do registro `kh_n1_cobertura_v392` (re-pinagem a uma cópia; pisos no lugar das igualdades); "\n       "o runner da Fronteira e a camada v393 dos 16 dispositivos (o número do runner é da sessão do site); quatro céticos independentes antes do portão do operador.', t)
assert t != n0, "trecho do espelho do handoff nao achado"
t = troca(t, "A F8.1 (bandeiras do gate recalculadas) segue aberta: a v393 a documenta, não a fecha.",
          "A evidência espectral independente do coração (cadeia pinada independente do CODATA) segue ausente; a F8.1 (bandeiras do gate recalculadas) segue [OPEN] e não é tocada pela v393.", nome="pendencias")
assert "13/10" not in t.split("# ---------------------------------------------------------------- (4) o handoff")[1], "ficou data de 13/10 no handoff"
ast.parse(t); FECHAR = t

# =============================================================================== b3_recibo_v393.py
t = bump(MOL["b3_recibo_v392.py"]); ast.parse(t); B3RECIBO = t

# =============================================================================== chain_pos_rito_v393.sh
t = bump(MOL["chain_pos_rito_v392.sh"])
HEADER = r'''#!/bin/sh
# v393 (14/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v392.sh (derivada por derivar_cadeia_v393.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v393.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v393_stdout.txt). A v393 acrescenta A REGRA e O CORACAO (3 pedras, o consumidor numerico que consome a regra, o selo do coracao).
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry)
# -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v393.py; o da v392 era das erratas CR-08/CR-02 e foi descartado) -> 5 a arvore -> 6 atlas+indice -> 7 superficies reais (appends datados;
# SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel) e a guarda de MEMORY.md (<24.000 B,
# <=195 linhas) -> 10 B(3) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(3) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR)
# -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V393_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# Os pinos do B(n) vem de PINOS_BN_v393.json (lidos na hora; hash nunca de memoria). Sem o PINO recibo_pre_selo (a fase pre_selo da B(n) nao foi preparada) o 10 PARA em AGUARDA_OPERADOR.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).'''
i, j, L = bloco(t, "#!/bin/sh", "PK=")
t = "\n".join([HEADER] + L[j:])
B3_PREPARA = r'''b3_prepara() {
  for k in bateria criterios esboco_R3_3 kernel_recibo candidato esperados pins_do_candidato; do
    p=$(pinop "$k"); a=$(pino "$k"); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  tem_pino recibo_pre_selo || aguarda "o PINO recibo_pre_selo nao esta em PINOS_BN_v393.json: o recibo da fase pre_selo da B(n) nao foi preparado (ato da gerencia: rodar o esboco R3.3 na fase pre_selo, pinar o recibo e retomar com CHAIN_DE=$1)"
  p=$(pinop recibo_pre_selo); a=$(pino recibo_pre_selo); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino recibo_pre_selo diverge do arquivo (pino $a != arquivo $b)"
  BAT=$(pino bateria); CRI=$(pino criterios); RPS=$(pino recibo_pre_selo)
  W_BAT=$(cygpath -w "$(pinop bateria)"); W_CRI=$(cygpath -w "$(pinop criterios)"); W_RPS=$(cygpath -w "$(pinop recibo_pre_selo)"); W_ESB=$(cygpath -w "$(pinop esboco_R3_3)"); W_NOS=$(cygpath -w "$NOS")
  # o selo e o manifesto do kernel da v392 (versao anterior): pinados se houver pino; senao, as copias de custodia da pasta base_v392 (SEM pino, hash lido na hora; o esboco as cruza com o pino da Bancada, R31-3)
  if tem_pino selo_anterior_v392; then p=$(pinop selo_anterior_v392); a=$(pino selo_anterior_v392); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino selo_anterior_v392 diverge do arquivo"; W_SELO=$(cygpath -w "$p")
  else W_SELO=$(cygpath -w "$PK/base_v392/um_absoluto_selo.json"); [ -f "$PK/base_v392/um_absoluto_selo.json" ] || parar "sem o selo da v392 em $PK/base_v392"; echo "  selo anterior SEM pino (lido na hora): $(sha256f "$W_SELO")"; fi
  if tem_pino kernel_manifesto_anterior_v392; then p=$(pinop kernel_manifesto_anterior_v392); a=$(pino kernel_manifesto_anterior_v392); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino kernel_manifesto_anterior_v392 diverge do arquivo"; W_KMAN=$(cygpath -w "$p")
  else W_KMAN=$(cygpath -w "$PK/base_v392/tgl_kernel_proof_manifest.json"); [ -f "$PK/base_v392/tgl_kernel_proof_manifest.json" ] || parar "sem o manifesto do kernel da v392 em $PK/base_v392"; echo "  manifesto do kernel anterior SEM pino (lido na hora): $(sha256f "$W_KMAN")"; fi
  KR="$PK/kernel/KERNEL_RECIBO_v393.json"; [ -f "$KR" ] || parar "sem o recibo do kernel: $KR"
  W_KR=$(cygpath -w "$KR"); KRSHA=$(sha256f "$W_KR"); [ "$KRSHA" = "$(pino kernel_recibo)" ] || parar "o recibo do kernel diverge do pino"; echo "  recibo do kernel (sha256 LIDO NA HORA, igual ao pino): $KRSHA"
  $PY -c "import json,os,sys;sys.exit(0 if os.path.isdir(json.load(open(sys.argv[1],encoding='utf-8'))['arvore']) else 1)" "$W_KR" || aguarda "a arvore so-fontes do recibo do kernel (campo arvore: C:/t/k393/arvore) nao existe mais: rodar $PY $PK/refazer_arvore_v393_pos_selo.py (refaz a arvore a partir do kernel do Nos, sem build; ato da gerencia) e retomar com CHAIN_DE=$1"
}
tem_pino() { $PY -c "import json,sys;sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1],encoding='utf-8')) else 1)" "$(cygpath -w "$PK/PINOS_BN_v393.json")" "$1"; }'''
t = subst_bloco(t, "b3_prepara() {", 'echo "== 0.', B3_PREPARA + "\n")
LISTA0 = r'''for f in "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$PORTA" "$PK/conferir_rito_v393.py" "$PK/ESPERADOS_v393.json" "$PK/guarda_p18_v393.py" "$PK/PINOS_BN_v393.json" \
         "$PK/refazer_arvore_v393_pos_selo.py" "$PK/kernel/KERNEL_RECIBO_v393.json" "$HAJA" "$INV/inventario_bancada.py" "$INV/gerar_documento.py" "/c/IALD/NOS_VIVO/construir.py" \
         "$SEL/leitura_v393.py" "$SEL/textos_v393.py" "$SEL/superficies_v393.py" "$SEL/fechar_v393.py" "$SEL/registrar_mapa_v393.py" "$SEL/b3_recibo_v393.py"; do'''
t = subst_bloco(t, 'for f in "$TOOLS/arvore_da_prova.py"', '  [ -f "$f" ] || parar "ferramenta', LISTA0 + "\n")
PASSO3 = r'''if quer 3; then
echo "== 3. ENSAIO em COPIAS: superficies (plano conferido antes da primeira escrita) e a arvore em DRY (nada real e' tocado)"
rm -rf "${ENS:?}" "${ENST:?}"; mkdir -p "$ENS" "$ENST"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_CORE_MEMORY.md" \
      "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
if [ -n "$V393_AVISO_REIVINDICACAO" ]; then cp -p "$AVISO" "$ENS/"; fi
set +e; $PY "$SEL/superficies_v393.py" --copias "$(cygpath -w "$ENS")" > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -24 "$SEL/ensaio_superficies_out.txt" | cut -c1-260
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); l=$(wc -l < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B, $l linhas"
[ "$n" -lt 24000 ] || parar "o MEMORY.md da copia chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "o MEMORY.md da copia passou de 195 linhas ($l)"
cp -p "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$ENST/"
if [ -f "$SEL/patch_arvore_indice_v393.py" ]; then
  $PY "$SEL/patch_arvore_indice_v393.py" --tools "$(cygpath -w "$ENST")" || parar "o ENSAIO do patch da arvore/indice recusou ou falhou (so copias foram tocadas)"
else
  echo "  (sem patch_arvore_indice_v393.py: a arvore e o indice rodam SEM linha nova da v393 -- o patch da v392 era das erratas CR-08/CR-02 e foi descartado; ver o relatorio)"
fi
(cd "$ENST" && $PY_B arvore_da_prova.py v393 dry) || parar "a arvore_da_prova.py (copia, dry) falhou"
fi'''
t = subst_bloco(t, "if quer 3; then", "if quer 4; then", PASSO3 + "\n")
PASSO4 = r'''if quer 4; then
if [ -f "$SEL/patch_arvore_indice_v393.py" ]; then
echo "== 4. patches arvore/indice"; $PY "$SEL/patch_arvore_indice_v393.py" || parar "patch arvore/indice recusou/falhou (backups _p393 ao lado)"
else
echo "== 4. patches arvore/indice: PULADO (opcional; sem patch_arvore_indice_v393.py)"
fi
fi'''
t = subst_bloco(t, "if quer 4; then", "if quer 5; then", PASSO4 + "\n")
PASSO7 = r'''if quer 7; then
echo "== 7. superficies (real: appends datados; a guarda P18 em todo texto; sem errata nova no CLAUDE.md da raiz)"
$PY "$SEL/superficies_v393.py" || parar "superficies_v393.py parou (backups .bak_<STAMP>_sup393 ao lado; rerodar e IDEMPOTENTE)"
fi'''
t = subst_bloco(t, "if quer 7; then", "if quer 8; then", PASSO7 + "\n")
PASSO9 = r'''if quer 9; then
echo "== 9. regra da linhagem completa: o MARCADOR DO SELO e o sha16 do um.py v393 ($S16) em cada superficie (zero e' falha visivel)"
exige "$NOS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v393_selada -->" "kh_n1_cobertura_v392"
exige "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v393_selada -->" "$S16"
exige "$ATLD/TGL_ATLAS.md" "<!-- atlas_v393_selada -->" "$S16" "kh_n1_cobertura_v392"
exige "$ATLD/TGL_INDICE_VIVO.md" "$S16"
exige "$ATLD/TGL_CORE_MEMORY.md" "<!-- core_v393_selada -->" "$S16"
exige "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$S16"
exige "$HAJA" "<!-- haja_luz_v393_selada -->" "$S16"
exige "$UMEM/MEMORY.md" "$S16"
exige "$UMEM/MEMORY_2.md" "v393"
for t in missao-ultima-flag-um-py.md central-de-patentes-estado.md; do exige "$UMEM/$t" "$S16"; done
exige "$UMEM/estatuto-da-prova-07out.md" "<!-- v393_selada -->" "$S16"
exige "$UMEM/v393-selada-a-regra-e-o-coracao-14out.md" "$S16" "kh_n1_cobertura_v392"
if [ -n "$V393_AVISO_REIVINDICACAO" ]; then exige "$AVISO" "<!-- aviso_v393_selada -->" "$S16"; else echo "  (AVISO_GERENCIA.md: PULADO -- sem V393_AVISO_REIVINDICACAO; escrever depois, sob reivindicacao)"; fi
n=$(wc -c < "$UMEM/MEMORY.md"); l=$(wc -l < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000), $l linhas (limite 195)"
[ "$n" -lt 24000 ] || parar "MEMORY.md chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "MEMORY.md passou de 195 linhas ($l): o carregador do harness o corta acima de 200"
fi'''
t = subst_bloco(t, "if quer 9; then", "if quer 10; then", PASSO9 + "\n")
# restos da v392 que nao podem ficar
for proibido in ("errata_claude_md", "patch_arvore_indice_v392", "HANDOFF_v390", "handoff-v390", "refazer_sandbox_v392", "selo_anterior_v391", "kernel_manifesto_anterior_v391", "errata_cr08", "errata_3_v", "errata_coulomb"):
    assert proibido not in t, ("resto da v392 na cadeia", proibido)
CHAIN = t

# =============================================================================== gravar os derivados e conferir
DERIV = {"leitura_v393.py": LEITURA, "superficies_v393.py": SUPERFICIES, "fechar_v393.py": FECHAR, "b3_recibo_v393.py": B3RECIBO, "chain_pos_rito_v393.sh": CHAIN}
for n, tx in DERIV.items():
    grava(n, tx)

# invariantes do molde (de DERIVACAO_v392.json), subidos de versao, que tem de sobreviver
INV92 = json.load(open(os.path.join(MOLDE, "DERIVACAO_v392.json"), encoding="utf-8"))["invariantes"]
INV93 = {}
for n92, lst in INV92.items():
    n93 = bump(n92)
    if n93 not in ("leitura_v393.py", "superficies_v393.py", "fechar_v393.py", "registrar_mapa_v393.py", "textos_v393.py"):
        continue   # patch_arvore_indice e errata_claude_md: descartados
    INV93[n93] = [bump(x) for x in lst]
# invariantes proprios da v393 (portoes da cadeia e da compactacao)
INV93.setdefault("chain_pos_rito_v393.sh", [])
INV93["chain_pos_rito_v393.sh"] += ["parar() {", "exit 20", "exit 1", "B3_AUTORIZADO", "EVENTO_HASH", "-lt 24000", "-le 195", "PINOS_BN_v393.json", "KERNEL_RECIBO_v393.json", "refazer_arvore_v393_pos_selo.py",
                                     "guarda_p18_v393.py", "grep -q '^RITO_RC='", "cmp ", "AGUARDA_OPERADOR", "CHAIN_DE"]
INV93["superficies_v393.py"] += ["Ganchos antigos consolidados", "movidas.extend(lines[a_:b_ + 1])", "LIMITE_LINHAS = 195"]
INV93["leitura_v393.py"] += ["REG_TODOS", "ESP['escada_v392_e_v393']", "regra_consumidor_v393", "coracao_e_selo_gravitacional_v393", "axiom_coverage_v392"]
INV93["b3_recibo_v393.py"] = ["BATERIA_PASSA", "REPINADA_B", "RECUSA_", "hashlib.sha256(raw).hexdigest()"]
INV93["fechar_v393.py"] += ["recibos_b3", "DIFF_v392_v393.diff", "insumo_codex_regra_sha16"]
conf = {}; falhas = []
todos = {n: open(os.path.join(HERE, n), encoding="utf-8").read() for n in list(DERIV) + ["textos_v393.py", "registrar_mapa_v393.py"]}
for n, lst in INV93.items():
    conf[n] = {}
    for x in lst:
        ok = x in todos[n]; conf[n][x[:90]] = ok
        if not ok:
            falhas.append((n, x[:90]))
sint = {}
for n, tx in todos.items():
    if n.endswith(".py"):
        ast.parse(tx); sint[n] = "ast.parse ok"
    else:
        r = subprocess.run(["sh", "-n", os.path.join(HERE, n)], capture_output=True, text=True); sint[n] = "sh -n rc=%d %s" % (r.returncode, r.stderr[:200])
        if r.returncode:
            falhas.append((n, "sh -n"))
# textos: nenhuma palavra proibida (guarda P18) -- executa so' a guarda sobre o arquivo de texto
sys.path.insert(0, PK)
from guarda_p18_v393 import violacoes
gv = {n: violacoes(todos[n]) for n in ("textos_v393.py",)}
if any(gv.values()):
    falhas.append(("guarda P18", gv))
DER = {
    "molde": {n: sha16(MOL[n].encode("utf-8")) for n in MOL},
    "molde_derivar_instalar_rito_v392": sha16(INSTALAR_MOLDE),
    "derivados": {n: sha16(todos[n].encode("utf-8")) for n in todos},
    "descartados_do_molde": {"patch_arvore_indice_v392.py": "CR-08/CR-02 da v392 (erratas da arvore/indice); passos 3/4 da cadeia tornados opcionais", "errata_claude_md_v392.py": "rascunho da v392; sem errata nova sobre o CLAUDE.md da raiz",
                             "nota_handoff.py": "nota especifica da v392 (nao era chamada pela cadeia)", "derivar_cadeia_v392.py": "gerava a cadeia da v392 a partir da v391; substituido por este derivar"},
    "escritos_a_mao_sobre_o_molde": ["textos_v393.py", "registrar_mapa_v393.py"],
    "invariantes": conf,
    "guarda_p18_sobre_textos": {k: ("LIMPO" if not v else v[:3]) for k, v in gv.items()},
    "sintaxe": sint,
    "nao_validado": "execucao contra o Nos v393 (o Nos tem a v392 b590c0aa80055e2a); so' ast.parse, sh -n e a guarda de texto foram rodados",
}
grava("DERIVACAO_v393.json", json.dumps(DER, ensure_ascii=False, indent=1))
print("DERIVADOS:", ", ".join("%s %s" % (n, DER["derivados"][n]) for n in DER["derivados"]))
print("SINTAXE:", json.dumps(sint, ensure_ascii=False))
print("INVARIANTES:", sum(len(v) for v in conf.values()), "conferidos;", "FALHAS:", falhas if falhas else "nenhuma")
sys.exit(1 if falhas else 0)

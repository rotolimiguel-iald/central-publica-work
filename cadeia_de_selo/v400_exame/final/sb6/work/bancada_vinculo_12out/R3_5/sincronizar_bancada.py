# -*- coding: utf-8 -*-
"""sincronizar_bancada.py -- o elo B(n) da cadeia de selo: vincula a Bancada Um ao um.py selado.  REVISAO R3.5 (19/10/2026).

R3.5 (19/10/2026): um conserto pedido pela revisao independente de 19/10 (EXAME_DELTA_E_R3_4.md, B-M), antes do B(n) da v394: o filtro dos MODULOS DE AUDITORIA da R3.4 era lista de PROIBICAO e deixava passar
`Lean.addDecl`, `Lean.modifyEnv` e `Lean.Meta.evalExpr` qualificados, `open IO.FS in` + `writeFile` e `open IO in` + `Process.output`. Agora e lista de PERMISSAO ESTRITA (auditar_fonte_de_auditoria):
comandos de topo = (so) `import` de Lean/TGLExt/TGL, `open` de Lean, #print axioms e run_cmd; no corpo do run_cmd, um vocabulario FECHADO (palavras, locais, funcoes, metodos, nomes) -- o das fontes reais
NetworkProofAuditR3/R7/R8 da v394; o que nao esta na lista e recusado, qualificado ou nao. O resto e a R3.4, byte a byte: os contratos (CADEIA_DE_SELOS_R3_4, SALTO_R3_4, KERNEL_RECIBO_R3_4, BATERIA_R3_4),
a conferencia do recibo pre_selo e o formato dos recibos nao mudam, e o recibo pre_selo da R3.4 (gerado antes da instalacao da v394) segue valendo (conferido por controle).

R3.4 (19/10/2026): tres consertos pedidos pela gerencia c1 (F0.6) depois que a cadeia da v394 mediu que a Bancada de producao ficou pinada na v392 (o elo da
v393 nunca rodou), que a bateria R2 pina o um.py v391 (T12/T13/T14) e que tres modulos de auditoria do kernel v394 nao tem declaracoes:
  S  SALTO (recuperacao de atraso): em --fase pre_selo, se a Bancada pina uma versao anterior a do Nos (N-k), o esboco EXIGE --cadeia-de-selos
     (contrato CADEIA_DE_SELOS_R3_4, pinada por --cadeia-de-selos-sha256) e a verifica POR HASH: um elo por versao, de N-k ate a do Nos, consecutivas;
     cada elo traz copias de bytes pinadas (um.py, selo, manifesto do kernel; selo pina o um.py e o manifesto; UM_VERSION confere) e cada elo, menos o
     ultimo, o registro do instalador (APLICADO_AO_CANONICO) com os backups de bytes do que foi substituido; o INICIO da cadeia e a Bancada (versao, um.py,
     selo, manifesto do kernel registrado) e o FIM e o Nos (pre_selo) ou o recibo pre-selo pinado (pos_selo). O recibo declara o salto e as versoes puladas
     (veredito REPINADA_B<n>__SALTO_<de>_<ate>__ENSAIO...); o pos_selo aceita esse recibo no lugar do JA_SINCRONIZADA e grava o salto no manifesto novo.
     Sem cadeia verificavel: recusa (BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS, CADEIA_DE_SELOS_*).
  P  BATERIA POR VERSAO: a bateria declara pinos_da_versao {versao, um_py_sha256, um_py_bytes, selo_sha256} (gerada por script em cada versao a partir dos
     pinos da cadeia) e os testes que pinam o um.py trazem pina_o_um_py=true; o esboco confere os pinos contra o Nos que leu (BATERIA_COM_PINO_VELHO,
     BATERIA_SEM_PINOS_DA_VERSAO) e passa o um.py medido ao teste pelos marcadores {um_py_path} {um_py_sha256} {um_py_bytes}. Bateria sem teste marcado
     (a R2) segue aceita como antes.
  M  MODULOS DE AUDITORIA: contrato KERNEL_RECIBO_R3_4 (a R3_2 segue admitida): um modulo sem declaracoes so passa se estiver em `modulos_de_auditoria` do recibo E a
     fonte, conferida por script, tiver so comandos de auditoria (import, open, #print axioms, run_cmd); a N1k vale para todo o resto.
O resto e a R3.3, byte a byte (diff em DIFF_R3_3_R3_4.patch).

R3.3 (13/10/2026): a reauditoria final da R3.2 (AUDITORIA_F0_6_C1_a70d70d5.md, APROVA_COM_RESSALVAS) achou duas falhas BAIXAS, fechadas aqui
(F0.6, gerencia c1): R32-A -- a guarda do interpretador recusa tambem -i (sys.flags.inspect/interactive; com -i o PYTHONSTARTUP herdado executaria
depois do main() e o processo ficaria preso no REPL; na recusa por -i o processo sai por os._exit, porque SystemExit ainda entraria no REPL) e o
recibo grava sys.orig_argv; R32-B -- no caminho ROLLBACK_DIVERGE o contrato gravado sai, a sonda do servico pos_rollback roda e o recibo grava o
sha do manifesto em disco. O resto e a R3.2, byte a byte.

R3.2 (13/10/2026): a reauditoria curta da R3.1 (AUDITORIA_F0_6_C1_a721b706.md, APROVA_COM_RESSALVAS) apontou R31-1 (MEDIA) e R31-2 a
R31-6 (BAIXA); a gerencia decidiu [INPUT] fechar todos nesta rodada, cada um com controle negativo que reproduz o caso EXATO do auditor
e uma variante (R3_2/CONTROLES_NEGATIVOS_R3_2.json, prefixo R32_). Consertos:
  R31-1 o esboco EXIGE `python -I -B -X utf8`: a guarda vem na 1a linha de codigo, antes de qualquer import alem de sys (um json.py ao
        lado do esboco nao chega a ser importado); sem -I (isolated, e com ele -E -P -s), -B ou -X utf8: INTERPRETADOR_NAO_ISOLADO, rc 2,
        nada gravado; main() confere de novo (chamada em processo).
  R31-2 depois do os.replace e da ultima sonda, os bytes do manifesto no disco sao relidos e comparados com os novos ANTES de gravar o
        recibo em estado/sincronizacao, e de novo DEPOIS; se divergem: os bytes estranhos ficam em --saida (sha no recibo), o recibo em
        estado sai, rollback, e a sonda do servico depois do rollback (APLICACAO_REVERTIDA: MANIFESTO_MUDOU_APOS_A_TROCA...).
  R31-3 o manifesto do kernel do recibo pre-selo e cruzado com o pino que o SELO ANTERIOR grava, fonte externa ao recibo: --selo-anterior
        (o selo da versao anterior, da custodia; sha == o selo pinado no manifesto vigente da Bancada) e --kernel-manifesto-anterior (sha ==
        o pino desse selo); raiz, Audit e impressao formal do recibo sao RECALCULADOS desse manifesto. Nunca campo do proprio recibo.
  R31-4 o build log tem de trazer as linhas do lake de cada pedra listada, da raiz (TGLExt) e do Audit (TGL.Audit) e a linha final
        `Build completed successfully` (LOG_DE_BUILD_IMPLAUSIVEL); o log do Audit cobre os #print axioms do Audit.lean pinado por NOME de
        declaracao distinto (linhas repetidas nao contam duas vezes; todo nome impresso no Audit.lean aparece no log).
  R31-5 antes de procurar sorry, o texto e lido tambem com todo branco colapsado (quebra entre `declaration` e `uses` inclusive) e com os
        escapes JSON decodificados (\\uXXXX, \\n, \\"); sorryAx e procurado nas tres formas e nas listas de axiomas.
  R31-6 CRITERIOS (e o recibo do kernel) com chave duplicada sao recusados (object_pairs_hook); a X19 e cruzada com as pedras do recibo
        (x19 = sim <=> uma pedra LightNetStandardWedgeDataBGL.lean).
  12-ter item 3 (plano): o recibo do kernel (contrato KERNEL_RECIBO_R3_2) traz varredura_tokens {recursiva, arquivos_lean,
        arquivos_lean_em_TGLExt_O16}, e o B(n) reconta os .lean da arvore RECURSIVAMENTE (sem seguir juncao) e confere.
A R3.1 (a85be74ffd7a1dee) fica como registro em R3_1/. Segue o cabecalho da R3.1, valido no que nao foi emendado acima.

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

R3 (13/10/2026): a re-auditoria da R2 (AUDITORIA_F0_6_C1_a645d974.md, achados N1-N16) APROVOU COM RESSALVAS e pediu uma R3 curta.
Consertos, cada um com controle negativo proprio (R3\\CONTROLES_NEGATIVOS_R3.json):
  N1  o T17 deixa de ser autodeclarado: o recibo do kernel (contrato KERNEL_RECIBO_R3, R3\\CONTRATO_KERNEL_RECIBO.md) e conferido
      por sha (--kernel-recibo-sha256), os logs sao LIDOS (sha, contagem de sorry/erros por script, axiomas do Audit), rc/sorry/erros
      int estritos, e os sha da raiz, do Audit e de cada pedra sao cruzados com o tgl_kernel_proof_manifest.json que o selo pina
      (formal_files_sha256, axiom_report, statuses, toolchain) e re-hasheados na arvore; o ANTES e cruzado com o recibo pre-selo;
      um_py_sha256 e campo PROIBIDO (a etapa 2 roda antes do candidato).
  N2  --recibo-pre-selo-sha256 (lido de vNNN_pins pela cadeia): obrigatorio em --producao e em aplicar fora do sandbox.
  N3  o servico e sondado de novo imediatamente antes de CADA gravacao do aplicar; se voltou, recusa (e desfaz o que for novo).
  N4  o aplicar compara o manifesto com os bytes lidos no passo 3 (anterior['_raw']): MANIFESTO_MUDOU_DESDE_A_LEITURA.
  N5  a bateria roda com o interpretador em -E -P (ambiente PYTHON* ignorado; a pasta do script fora do sys.path), ambiente sem
      PYTHON*, cwd numa pasta vazia nova, e recusa modulo-sombra (.py/.pyc/.pyd/pacote) ao lado de fonte pinada. -I/-S nao: numpy,
      scipy e torch vivem no site do USUARIO (medido 13/10), que -I/-s/-S cortam; o limite fica declarado.
  N6  [INPUT da gerencia] --evento-hash <hash16>: o hash do elo na cadeia confere; a autoria segue CONVENCAO, nao autenticacao.
  N8  [INPUT da gerencia] raizes de --saida estreitas; nunca na pasta das fontes da bateria nem na do esboco.
  N15 [INPUT da gerencia] mesma versao, mesmo um.py, selo diferente: SEAL_CHANGED_SAME_VERSION salvo --reparo-de-pino.
  N9-N14, N16: nomes reservados; recibo do aplicar sem juncao; filtro de negacao e guarda de palavra normalizados (NFKC/NFD, chaves
      e valores; chaves fechadas); hardlink do Nos; Volume{GUID}/GLOBALROOT recusados por regra; log guardado antes de gravar;
      gramatica fechada do comando (-c, -m, zip, pasta: recusados).
A R2 (8c055a45362fe733) fica como registro em R2\\. Segue o cabecalho da R2, valido no que nao foi emendado acima.

ESBOCO FUNCIONAL R2 do desenho da gerencia c1 (12/10/2026), por ordem do operador de 12/10 (verbatim em
work\\cunhagens_12out\\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt, sha256 lido por script no recibo).
A R1 (d9927a8fdc5cfc62) foi REPROVADA pela auditoria independente (AUDITORIA_VINCULO_BANCADA_C1.md, 13/10) com os achados A1-A13;
a R2 conserta um a um, cada conserto com teste negativo proprio (R2\\CONTROLES_NEGATIVOS_R2.json). A R1 fica como registro em
R2\\originais_R1\\. NAO ESTA INSTALADO. Roda em sandbox contra COPIAS da Bancada em raiz curta (T16). A instalacao na cadeia (passo
B(n)) e a primeira re-pinagem da producao (B3, depois do selo da v392) sao atos que o desenho reserva a gerencia e ao operador.

O que faz, nesta ordem, e tudo fail-closed (qualquer divergencia = recusa visivel, codigo 2; bateria reprovada = codigo 3):
  0. GUARDAS DE CAMINHO (A2, A5): a identidade de toda pasta e por os.path.samefile (st_dev+st_ino), depois de normalizar o prefixo
     \\\\?\\, o UNC local (\\\\127.0.0.1\\C$, \\\\localhost\\C$, \\\\<host>\\C$), juncao, nome 8.3 e caixa; UNC nao local e recusado.
     --saida so dentro das raizes permitidas (a pasta de trabalho da cadeia ou a raiz curta do sandbox) e nunca sob a producao,
     o Nos ou a propria --bancada.
  1. LE O SELO do Nos (um_absoluto_selo.json) e o um.py: a versao (UM_VERSION, linha UNICA na coluna 0 -- A11), o sha256 do um.py
     que o selo pina, a linha UNICA de ALPHA_FINE_CODATA_2018 (nenhuma reatribuicao, nem indentada -- A11) e beta = alpha*sqrt(e)
     EM RUNTIME (nunca literal), conferido contra o beta do core (um_absoluto.json) com tolerancia NOMEADA.
  2. VERIFICA O EVENTO c1 (A4) pela cadeia de hash do eventos.jsonl (anterior == hash do elo anterior; hash recalculado), exigindo
     tipo SINCRONIZACAO_BANCADA, quem claude-c1, e os campos nomeados por JSON (versao, bancada por identidade, um_py e selo por
     sha256, acao), sem texto que negue a gravacao, sem seq duplicado.
  3. LE O MANIFESTO VIGENTE da Bancada e o estado do contrato instalado; recusa --sandbox se o manifesto pinar o Nos real (A2);
     recusa re-pino com a mesma versao e hash diferente do um.py (SELO_PROGRAMA_DIVERGE -- A8) salvo --reparo-de-pino com evento
     que o diga; confere o recibo pre-selo por identidade (versao anterior, um.py antes pinado, mesma Bancada) e encadeia o seu
     hash no manifesto novo (A6).
  4. REGENERA O MANIFESTO (mesmos pinos de codigo e de fontes; pinos novos do um.py e do selo; geracao B(n); evento c1; contrato),
     recusando caminho com '..', absoluto ou fora da raiz em code[].path e copias[].para (A10).
  5. RE-PINA numa COPIA de ensaio e confere com o canonical.py instalado (ok, versao, sha, beta bit a bit).
  6. RODA A BATERIA pinada (A7: sha256 do BATERIA_VINCULO.json por --bateria-sha256 e sha256 canonico de cada teste; conjunto minimo
     obrigatorio em aplicar) a partir dos caminhos PINADOS em fontes[] (A3: {fonte:N}; sha256 conferido ANTES de cada teste; todo
     .py executado tem de ser fonte pinada ou copia conferida; {vinculo} e proibido). T17 le o recibo do build do kernel por hash,
     sem subprocesso (A1). Nenhum __pycache__ nasce na Bancada (A9: sys.dont_write_bytecode e PYTHONDONTWRITEBYTECODE).
  7. GRAVA O RECIBO; so em --modo aplicar, com evento verificado, servico parado e bateria passada, grava o manifesto novo na
     Bancada (backup de bytes, temporario -> conferir -> os.replace, reconferencia pelo canonical.py instalado, rollback se falhar).
Nada aqui le dado observado para veredito, nada move o gate, nada e leitura fisica. NOT_FALSIFIED nunca e creditacao.
"""
import sys


def _flags_do_interpretador():
    """R31-1: as flags do interpretador corrente (funcao, para que os controles em processo possam simular outro interpretador)."""
    return sys.flags


def _flags_que_faltam(fl=None):
    """R31-1 (R3.2): o esboco grava a producao; o interpretador tem de ser `python -I -B -X utf8`. -I liga isolated, ignore_environment
    (-E), safe_path (-P: a pasta do esboco fora do sys.path) e no_user_site (-s). Devolve a lista do que falta (vazia = admitido)."""
    fl = _flags_do_interpretador() if fl is None else fl
    falta = []
    for attr, nome in (("isolated", "-I"), ("ignore_environment", "-E (implicito em -I)"), ("safe_path", "-P (implicito em -I)"),
                       ("no_user_site", "-s (implicito em -I)"), ("dont_write_bytecode", "-B"), ("utf8_mode", "-X utf8")):
        if not getattr(fl, attr, 0):
            falta.append(nome)
    # R32-A (R3.3): -i (inspect/interactive) ligado = recusa (o PYTHONSTARTUP executaria depois do main() e o processo ficaria no REPL)
    for attr, nome in (("inspect", "sem -i (inspect ligado)"), ("interactive", "sem -i (interactive ligado)")):
        if getattr(fl, attr, 0):
            falta.append(nome)
    return falta


if __name__ == "__main__":
    # R31-1: a guarda vem ANTES de qualquer outro import (sys e embutido e nao se sombreia): um json.py, argparse.py... ao lado do
    # esboco nao chega a ser importado. A saida e montada sem o modulo json (que poderia ser o sombreado).
    _falta = _flags_que_faltam()
    if _falta:
        sys.stdout.write('{"veredito": "RECUSADA", "recusa": "INTERPRETADOR_NAO_ISOLADO: o esboco grava a producao e exige python -I -B -X utf8; '
                         'faltam: %s (R31-1); nada importado alem de sys, nada gravado", "recibo": null, "nota": "recusa anterior a qualquer import"}\n'
                         % ", ".join(_falta))
        sys.stdout.flush()
        if sys.flags.inspect or sys.flags.interactive:
            # R32-A (R3.3): com -i, SystemExit ainda entra no REPL (e roda o PYTHONSTARTUP): sai pelo os ja carregado pelo proprio interpretador
            _os_ja_carregado = sys.modules.get("os")
            if _os_ja_carregado is not None and hasattr(_os_ja_carregado, "_exit"):
                _os_ja_carregado._exit(2)
        raise SystemExit(2)
sys.dont_write_bytecode = True   # A9: nenhum .pyc nasce na Bancada alvo quando o canonical.py instalado e importado
import argparse
import datetime
import hashlib
import importlib.util
import json
import math
import os
import re
import socket
import subprocess
import time
import unicodedata
import importlib.machinery
import pkgutil
import site
from pathlib import Path
from unittest.mock import patch

if sys.flags.optimize:
    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (asserts sao guardas)")

REVISAO = "R3.5 (19/10/2026)"
AQUI = Path(__file__).resolve().parent
PRODUCAO = Path("C:/IALD/Bancada_Um")
NOS_PADRAO = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
TUNEL_PADRAO = Path("C:/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019")
EVENTOS_QUADRO = Path("C:/IALD/PROGRAMA_IALD/eventos.jsonl")
WORK = Path("C:/IALD/Central de Patentes/work")
# N8 [INPUT da gerencia, 13/10]: --saida so dentro destas raizes ESTREITAS: a pasta do vinculo; work/cadeia_de_selo/<alvo>;
# work/<alvo>_bateria (alvo = a versao que esta sendo selada: --versao em pos_selo, a seguinte em pre_selo); e o sandbox C:/t/vb* (T16). Nunca a pasta das fontes da bateria nem a do proprio esboco.
RAIZ_SANDBOX = Path("C:/t")
RE_SANDBOX_DIR = re.compile(r"^vb[0-9A-Za-z_-]*$")


def versao_alvo_da_saida(versao, fase="pos_selo"):
    """N8: a pasta de trabalho da cadeia e a da versao que esta sendo SELADA: na fase pos_selo e a propria --versao; na pre_selo (os testes
    finais contra a versao ainda canonica, ex. --versao v391) e a SEGUINTE (v392): o plano grava a etapa 1 em work/v392_bateria."""
    if fase == "pre_selo":
        return "v%03d" % (int(str(versao)[1:]) + 1)
    return str(versao)


def raizes_saida(versao, fase="pos_selo"):
    alvo = versao_alvo_da_saida(versao, fase)
    return (WORK / "bancada_vinculo_12out", WORK / "cadeia_de_selo" / alvo, WORK / ("%s_bateria" % alvo))


PORTA_BANCADA = 18777
EVENTO_TIPO = "SINCRONIZACAO_BANCADA"
EVENTO_AUTOR = "claude-c1"
# a MESMA regex do canonical.py instalado (l.73-74): coluna 0, sem indentacao
RE_VERSAO = re.compile(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', re.M)
RE_ALPHA = re.compile(r'^ALPHA_FINE_CODATA_2018\s*=\s*([0-9.eE+-]+)', re.M)
# A11: unicidade da linha de coluna 0 (alpha e UM_VERSION) E nenhuma reatribuicao indentada (medido no um.py v391 8e7b9927: zero)
RE_ALPHA_LINHAS = re.compile(r'^ALPHA_FINE_CODATA_2018[ \t]*=(?!=)', re.M)
RE_VERSAO_LINHAS = re.compile(r'^UM_VERSION[ \t]*=(?!=)', re.M)
RE_ALPHA_INDENTADA = re.compile(r'^[ \t]+ALPHA_FINE_CODATA_2018[ \t]*=(?!=)', re.M)
RE_VERSAO_INDENTADA = re.compile(r'^[ \t]+UM_VERSION[ \t]*=(?!=)', re.M)
RE_GERACAO = re.compile(r'^B(\d+)-')
RE_SHA256 = re.compile(r'^[0-9a-f]{64}$')
# A4/N11: texto que NEGA a gravacao (o evento autoriza; nao pode conter negacao, veto ou recusa em nenhuma chave nem valor). R3: o texto
# e NORMALIZADO antes (NFKC; NFD sem marcas combinantes nem caracteres de formato; caixa dobrada; separadores, inclusive '_', viram espaco)
RE_NEGACAO = re.compile(r"\b(nao|nunca|jamais|proib\w*|vet(a|o|ar|ado|ada|ados|adas)|recus\w*|cancel\w*|suspend\w*|revog\w*|impedid\w*|bloque\w*)\b")
# N11: o conjunto FECHADO de chaves de dados de um evento SINCRONIZACAO_BANCADA (chave fora dele = recusa)
CHAVES_EVENTO = frozenset(("versao", "bancada", "acao", "um_py", "selo", "reparo", "gravacoes", "unidade", "nota"))
ESPERADOS_POS_SELO = ("PIN_CHANGED", "CANONICAL_VERSION_CHANGED", "SEAL_PROGRAM_MISMATCH")
# a guarda da regua (a mesma do um.py e do iald.py), montada em pedacos para que o token nunca exista neste arquivo
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
BETA_TOLERANCIA_REL = 1e-11   # medido em 12/10 (H_BANCADA): |beta_core - beta_runtime|/beta = 5.43e-13; a tolerancia e nomeada, nao escondida
BATERIA_MINIMA = ("T01_IDENTIDADE", "T15_SONDAS")          # A7: sem estes dois nao ha bateria em aplicar
BATERIA_MINIMA_POS_SELO = ("T17_LEAN_KERNEL",)             # A7/A1: em aplicar pos_selo o kernel selado entra pelo recibo do build
HOSTS_LOCAIS = {"localhost", "127.0.0.1", "::1", ".", socket.gethostname().lower()}
try:
    HOSTS_LOCAIS.add(socket.getfqdn().lower())
except OSError:
    pass
# N9: nomes reservados do Windows (por componente, sem extensao, com os digitos sobrescritos que o Win32 tambem reserva)
RESERVADOS = frozenset(["CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"] + ["COM%s" % d for d in "0123456789¹²³"]
                       + ["LPT%s" % d for d in "0123456789¹²³"])
# N1: o contrato do recibo do kernel (R3\CONTRATO_KERNEL_RECIBO.md)
KERNEL_CONTRATO = "KERNEL_RECIBO_R3_4"   # R3.4: + modulos_de_auditoria (a R3_2 segue admitida); R3.2: + varredura_tokens recursiva (12-ter item 3); R3.1: toolchain em lista, pedras com declaracoes, formal_files_antes, criterios so com o medido
KERNEL_CONTRATO_R3_2 = "KERNEL_RECIBO_R3_2"
KERNEL_CONTRATOS_ADMITIDOS = (KERNEL_CONTRATO_R3_2, KERNEL_CONTRATO)
CRITERIOS_CONTRATO = "CRITERIOS_R3_1"     # A3: o arquivo dos ESPERADOS, pinado pela cadeia (R3_1/CRITERIOS_V392.json e o modelo)
CRITERIOS_X19 = ("sim", "nao")
AXIOMAS_TRIO = frozenset(("propext", "Classical.choice", "Quot.sound"))
KERNEL_CAMPOS_PROIBIDOS = ("um_py_sha256", "tgl_kernel_proof_manifest_sha256", "selo_sha256")   # a etapa 2 roda ANTES do candidato e do rito
KERNEL_CRITERIOS_EXIGIDOS = ("j1_declaracoes", "j1_teoremas", "j1_fora_do_trio", "audit_entradas_antigas_identicas",
                             "tokens_proibidos", "r1_ausente", "declaracoes_novas_no_trio")
# os statuses do manifesto do kernel que TEM de ser true (unconditional_type_III1_corner_proved=false e honesto por desenho; nao se exige)
KERNEL_STATUSES_EXIGIDOS = ("lake_build_ok", "sorryAx_absent", "trustCompiler_absent", "custom_TGL_axioms_absent",
                            "source_forbidden_tokens_absent", "sentinels_present", "all_unconditional_targets_verified",
                            "all_conditional_implications_verified", "formal_release_ready")
# A1 (R3.1): o aviso REAL do Lean 4.31 e ``declaration uses `sorry` `` (crases; medido nos logs do Nos); o de aspas simples tambem conta
RE_LOG_SORRY = re.compile(r"declaration\s+uses\s*[`'\u2018\u2019\"]sorry[`'\u2018\u2019\"]|\bsorryAx\b")   # R31-5: qualquer branco entre as palavras
# A1b (R3.1): normalizacao do log antes de contar
RE_ANSI = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)|\x1b[@-Z\\-_]")
RE_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
# A2 (R3.1): as linhas #print axioms do Audit.lean pinado; N1k: o nome que o Lean imprime no log do Audit
RE_PRINT_AXIOMS = re.compile(r"(?m)^[ \t]*#print[ \t]+axioms[ \t]+\S")
RE_LOG_DECL = re.compile(r"(?m)^'(.+?)' (?:depends on axioms:|does not depend on any axioms)")
RE_LOG_ERRO = re.compile(r"(?m)(^|:\d+:\d+:\s)error\b|^error:")
RE_LOG_AXIOMAS = re.compile(r"depends on axioms:\s*\[([^\]]*)\]")
# R31-4 (R3.2): as linhas de job do lake (Lean 4.31: "<marca> [n/m] Built <Modulo> (<t>)", ou "Replayed") e a linha final. Medido no build
# real da v390 (rodadas/tgl_kernel_build_capture.txt, custodia): os 3 arquivos formais mudados (TGLExt, TGL.Audit, TGLExt.Fundacao) sairam como Built
RE_LAKE_JOB = re.compile(r"(?m)^[^\[\n]*\[\d+/\d+\][ \t]+(?:Built|Replayed)[ \t]+([^\s(]+)")
RE_LAKE_FIM = re.compile(r"(?m)^[ \t]*Build completed successfully\b")
RE_PRINT_AXIOMS_NOME = re.compile(r"(?m)^[ \t]*#print[ \t]+axioms[ \t]+(\S+)")
# R31-5 (R3.2): escapes JSON (a saida do Lean em JSON traz a crase como \u0060); decodificados so numa COPIA do texto, para a busca
RE_ESCAPE_U = re.compile(r"\\u([0-9a-fA-F]{4})")
RE_ESCAPE_SIMPLES = re.compile(r"\\([nrtbf\"/\\])")
RE_BRANCO = re.compile(r"\s+")
# R31-6 (R3.2): a pedra da decisao X19 do operador (PLANO_V392 l.147: `LightNetStandardWedgeDataBGL.lean`, so se a X19 for "sim")
X19_PEDRA = "LightNetStandardWedgeDataBGL.lean"
# R3.4 (S): o salto -- a cadeia de selos entre a versao que a Bancada pina (N-k) e a do Nos (N-1); contrato, chaves fechadas, tamanho maximo
CADEIA_CONTRATO = "CADEIA_DE_SELOS_R3_4"
SALTO_CONTRATO = "SALTO_R3_4"
RE_VNNN = re.compile(r"^v(\d{3,4})$")
CADEIA_RAIZ_CHAVES = frozenset(("contrato", "elos", "nota", "gerada_por", "gerada_em_utc"))
CADEIA_ELO_CHAVES = frozenset(("versao", "um_py", "selo", "kernel_manifesto", "substituido_na_instalacao_por"))
CADEIA_ARQ_CHAVES = frozenset(("path", "sha256", "bytes"))
CADEIA_INSTALACAO_CHAVES = frozenset(("versao", "registro", "backup_um_py", "backup_selo"))
CADEIA_MAX_ELOS = 64
# R3.4 (P): a bateria por versao -- o bloco pinos_da_versao e o marcador pina_o_um_py dos testes
BATERIA_PINOS_CHAVES = frozenset(("versao", "um_py_sha256", "um_py_bytes", "selo_sha256", "fonte_dos_pinos"))
# R3.5 (M): a LISTA DE PERMISSAO ESTRITA do modulo de auditoria. A R3.4 recusava por LISTA DE PROIBICAO (palavras proibidas no corpo do run_cmd, com um lookbehind que excluia o ponto): passavam
# `Lean.addDecl`, `Lean.modifyEnv` e `Lean.Meta.evalExpr` qualificados, `open IO.FS in` + `writeFile` e `open IO in` + `Process.output` (achado B-M da revisao independente de 19/10/2026).
# Agora so passa o que esta EXPLICITAMENTE listado aqui: os comandos de topo (import so de Lean/TGLExt/TGL, open so de Lean, #print axioms, run_cmd) e, no corpo do run_cmd (codigo EXECUTADO na
# compilacao), um vocabulario FECHADO de palavras, locais, funcoes, metodos e nomes -- o das fontes reais NetworkProofAuditR7/R8 da v394 e o da fixture sintetica do sandbox. Fora da lista = recusa,
# qualificado ou nao, aberto por `open` ou nao. O script confere a FORMA; nao prova a inocuidade semantica do corpo (residuo declarado).
RE_AUD_IMPORT = re.compile(r"^import[ \t]+(?:Lean|(?:TGLExt|TGL)(?:\.[A-Za-z_][A-Za-z0-9_']*)+)[ \t]*$")
AUD_OPEN_PERMITIDOS = frozenset(("Lean",))
RE_AUD_OPEN = re.compile(r"^open(?:[ \t]+[A-Za-z_][A-Za-z0-9_.']*)+[ \t]*$")
RE_AUD_PRINT = re.compile(r"^#print[ \t]+axioms[ \t]+[^\W\d][\w.']*[ \t]*$")
RE_AUD_RUNCMD = re.compile(r"^run_cmd(?:[ \t]+do)?[ \t]*$")
AUD_CORPO_PALAVRAS = frozenset(("let", "mut", "for", "in", "do", "if", "then", "else", "unless", "match", "with", "fun", "some", "pure", "_"))
AUD_CORPO_LOCAIS = frozenset(("env", "count", "n", "ci", "idx", "mod", "axs", "a", "c", "i", "m"))
AUD_CORPO_GLOBAIS = frozenset(("Elab.Command.liftCoreM", "getEnv", "collectAxioms", "throwError", "IO.println", "toString", "String.intercalate", "Name.toString"))
AUD_CORPO_METODOS = frozenset(("toList", "getModuleIdxFor?", "header", "moduleNames", "constants", "toString", "map", "all", "isPrefixOf", "axiomInfo"))
AUD_CORPO_NOMES = frozenset(("propext", "Classical.choice", "Quot.sound"))
AUD_CORPO_PREFIXOS_DE_NOME = ("TGLExt", "TGL")
AUD_CORPO_PONTUACAO = ("←", ":=", "=>", "==", "||", "++", "(", ")", "[", "]", ",", "|", "+", "!")
RE_AUD_TOK_NOME = re.compile(r"`[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*")
RE_AUD_TOK_ID = re.compile(r"[A-Za-z_][A-Za-z0-9_']*(?:\.[A-Za-z_][A-Za-z0-9_']*)*\??")
RE_AUD_TOK_CAMPO = re.compile(r"\.[A-Za-z_][A-Za-z0-9_']*\??")
RE_AUD_TOK_NUM = re.compile(r"[0-9]+")
# N5/N16: a gramatica FECHADA do comando de um teste: {py} [-B] [-X utf8] <script .py pinado> [args]; o esboco poe -E -P na frente
OPCOES_PY_ADMITIDAS = ("-B",)
OPCOES_PY_COM_VALOR = {"-X": ("utf8",)}
FLAGS_ISOLAMENTO = ("-E", "-P", "-s")   # A4 (R3.1): -s nos filhos; o site do usuario so entra como caminho, pelo lancador
LANCADOR_NOME = "_lancador_isolado_r3_1.py"
LANCADOR_FONTE = ("# -*- coding: utf-8 -*-\n"
                  "# lancador do sincronizar_bancada.py R3.1 (A4): roda o script pinado com o site do usuario como CAMINHO\n"
                  "# (nenhum .pth, nenhum usercustomize executa); o filho ja roda com -E -P -s\n"
                  "import runpy\n"
                  "import sys\n"
                  "\n"
                  "\n"
                  "def _principal():\n"
                  "    site_usuario, script = sys.argv[1], sys.argv[2]\n"
                  "    sys.argv = [script] + sys.argv[3:]\n"
                  "    if site_usuario != '-':\n"
                  "        sys.path.append(site_usuario)\n"
                  "    runpy.run_path(script, run_name='__main__')\n"
                  "\n"
                  "\n"
                  "_principal()\n")
LANCADOR_SHA256 = hashlib.sha256(LANCADOR_FONTE.encode("utf-8")).hexdigest()
N3A_NOTA = ("N3a (R3.1): o esboco nao trava o arquivo nem a porta. Um um_bancada.py que suba no instante do os.replace le o manifesto NOVO e o "
            "guarda em RAM; se depois houver rollback, o disco volta ao ANTERIOR e a RAM nao. Por isso: (1) depois do rollback o B(n) sonda o "
            "servico e, se ele responde, recusa com SERVICO_NO_AR_APOS_ROLLBACK__REINICIO_OBRIGATORIO; (2) depois de QUALQUER rollback o servico "
            "tem de ser reiniciado com recibo de identidade (10-ter) antes de outro B(n); (3) depois da ultima sonda nada e visivel ao esboco: "
            "o 10-ter confere a identidade do servico religado.")
# N1 do servico (porta), N3: lida na hora da chamada, nunca ligada na definicao
SUFIXOS_IMPORTAVEIS = tuple(sorted(set(importlib.machinery.all_suffixes()), key=len, reverse=True))


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def agora():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


class ChaveDuplicada(ValueError):
    """R31-6 (R3.2): um objeto JSON com a mesma chave duas vezes (o json.loads ficaria com a ULTIMA; um leitor humano le a primeira)."""


def _sem_duplicatas(pares):
    vistas = {}
    for k, v in pares:
        if k in vistas:
            raise ChaveDuplicada("chave duplicada %r no mesmo objeto JSON" % (k,))
        vistas[k] = v
    return vistas


def json_estrito(raw):
    """R31-6 (R3.2): json.loads que recusa chave duplicada em qualquer objeto (ChaveDuplicada, subclasse de ValueError)."""
    return json.loads(raw, object_pairs_hook=_sem_duplicatas)


def pin(p):
    b = Path(p).read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha256(b))


class Recusa(Exception):
    """Recusa fail-closed: o codigo e a primeira palavra; o resto e o motivo."""


# ---------------------------------------------------------------- 0. identidade de caminhos (A2, A5, A10)
def caminho_canonico(p):
    """Normaliza a FORMA do caminho antes de resolver: tira o prefixo \\\\?\\ (e \\\\?\\UNC\\, \\\\.\\), traduz UNC LOCAL (\\\\host\\X$\\...)
    para X:\\..., recusa UNC nao local; depois Path.resolve() (juncao, symlink, nome 8.3, '..', caixa do disco)."""
    s = os.fspath(p)
    if s.startswith("//"):
        s = "\\\\" + s[2:]
    if s[:8].upper() in ("\\\\?\\UNC\\", "\\\\.\\UNC\\"):
        s = "\\\\" + s[8:]
    elif s.startswith("\\\\?\\") or s.startswith("\\\\.\\") or s.startswith("\\??\\"):
        s = s[4:]
        # N13: depois do prefixo de dispositivo so se admite LETRA DE DISCO; Volume{GUID}, GLOBALROOT, HarddiskVolumeN, pipe etc.
        # sao recusados por regra explicita (na R2 a recusa vinha por acidente: sobrava um relativo inexistente)
        if re.match(r"(?i)^volume\{", s):
            raise Recusa("CAMINHO_VOLUME_GUID_NAO_ADMITIDO: " + os.fspath(p))
        if not re.match(r"^[A-Za-z]:([\\/]|$)", s):
            raise Recusa("CAMINHO_DISPOSITIVO_NAO_ADMITIDO: " + os.fspath(p))
    m = re.match(r"^\\\\([^\\/]+)[\\/]([A-Za-z])\$(?:[\\/](.*))?$", s)
    if m:
        if m.group(1).lower() not in HOSTS_LOCAIS:
            raise Recusa("CAMINHO_UNC_NAO_LOCAL: " + s)
        s = m.group(2).upper() + ":\\" + (m.group(3) or "")
    if s.startswith("\\\\") or s.startswith("//"):
        raise Recusa("CAMINHO_UNC_NAO_ADMITIDO: " + s)
    return Path(s).resolve()


def mesmo_no(a, b):
    """Identidade por st_dev+st_ino (os.path.samefile) quando os dois existem; senao, o caminho canonico sem caixa."""
    a, b = caminho_canonico(a), caminho_canonico(b)
    try:
        return os.path.samefile(a, b)
    except OSError:
        return os.path.normcase(str(a)) == os.path.normcase(str(b))


def dentro_de(filho, pai):
    """filho == pai ou filho esta sob pai, por caminho canonico (a existencia do filho nao e exigida)."""
    f, p = caminho_canonico(filho), caminho_canonico(pai)
    if mesmo_no(f, p):
        return True
    fs, ps = os.path.normcase(str(f)), os.path.normcase(str(p)).rstrip("\\")
    return fs.startswith(ps + "\\")


def relativo_seguro(rel, raiz):
    """A10: um caminho relativo do manifesto ou da bateria so pode descer dentro da raiz: sem '..', sem absoluto, sem drive, e o
    destino resolvido tem de ficar sob a raiz."""
    s = str(rel)
    p = Path(s.replace("/", "\\"))
    if p.is_absolute() or p.drive or p.anchor or ".." in p.parts or s.startswith(("\\", "/")) or ":" in s:
        raise Recusa("CAMINHO_RELATIVO_INVALIDO: %r" % s)
    # N9: cada componente e conferido: nada de nome reservado (CON, AUX, PRN, NUL, COMn, LPTn, com ou sem extensao) nem de cauda
    # '.'/espaco (o Win32 corta a cauda e o nome vira apelido de outro arquivo)
    for parte in s.replace("/", "\\").split("\\"):
        if parte in ("", "."):
            continue
        if parte.endswith((".", " ")):
            raise Recusa("CAMINHO_CAUDA_INVALIDA: %r" % s)
        if parte.split(".")[0].rstrip(" ").upper() in RESERVADOS:
            raise Recusa("CAMINHO_NOME_RESERVADO: %r" % s)
        if any(ord(c) < 32 or c in '<>"|?*' for c in parte):
            raise Recusa("CAMINHO_CARACTERE_INVALIDO: %r" % s)
    dst = (Path(raiz) / p).resolve()
    if not dentro_de(dst, raiz):
        raise Recusa("CAMINHO_FORA_DA_RAIZ: %r" % s)
    return dst


def sem_juncao(rel, raiz):
    """N10: o destino relativo `rel` sob `raiz`: passa por relativo_seguro e, alem disso, nenhum componente EXISTENTE do caminho
    LEXICO (raiz canonica + partes de rel) pode ser juncao ou link -- nem para fora (relativo_seguro ja pega) nem para dentro."""
    dst = relativo_seguro(rel, raiz)
    atual = caminho_canonico(raiz)
    for parte in Path(str(rel).replace("/", "\\")).parts:
        atual = atual / parte
        if os.path.lexists(atual) and (atual.is_symlink() or atual.is_junction()):
            raise Recusa("CAMINHO_COM_JUNCAO: %s" % atual)
    return dst


def gravar_novo(p, data):
    """Grava arquivo NOVO (nunca sobrescreve): temporario -> conferir tamanho e bytes -> os.replace."""
    p = Path(p)
    if p.exists():
        raise Recusa("ARQUIVO_JA_EXISTE: " + str(p))
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp_sync")
    with tmp.open("xb") as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())
    if tmp.stat().st_size != len(data) or tmp.read_bytes() != data:
        tmp.unlink()
        raise Recusa("ESCRITA_CURTA: " + str(p))
    os.replace(tmp, p)
    if p.read_bytes() != data:
        raise Recusa("ESCRITA_DIVERGE: " + str(p))
    return p


def _formas(s):
    """N11/N14: as formas de um texto que as guardas olham: o texto, o NFKC, e o NFKC decomposto sem marcas combinantes (Mn) nem
    caracteres de formato (Cf, ex.: espaco de largura zero)."""
    s = str(s)
    n = unicodedata.normalize("NFKC", s)
    d = "".join(c for c in unicodedata.normalize("NFD", n) if unicodedata.category(c) not in ("Mn", "Cf"))
    return (s, n, d)


def contem_palavra(s):
    return any(GUARDA.search(f) for f in _formas(s))


def limpar(s):
    """texto que vai a recibo/stdout: se contem a palavra guardada (em qualquer forma), sai suprimido, com o sha do original."""
    s = str(s)
    if contem_palavra(s):
        return "<TEXTO_SUPRIMIDO: palavra guardada; sha256 %s>" % sha256(s.encode("utf-8"))[:16]
    return s


def json_bytes(obj):
    # json.dumps com ensure_ascii=False ja traz CHAVES e VALORES decodificados (\uXXXX vira o caractere): a guarda ve as duas coisas
    s = json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False, default=str)
    if contem_palavra(s):
        raise Recusa("PALAVRA_PROIBIDA_NA_SAIDA")
    return (s + "\n").encode("utf-8")


def carregar_canonical(bancada):
    """Importa o canonical.py INSTALADO naquela Bancada (nunca o de outra), com nome de modulo unico; sem bytecode (A9)."""
    assert sys.dont_write_bytecode, "A9: dont_write_bytecode tem de estar ligado antes de importar o canonical.py da Bancada"
    p = Path(bancada) / "bancada" / "canonical.py"
    if not p.is_file():
        raise Recusa("CANONICAL_PY_AUSENTE: " + str(p))
    nome = "canonical_instalado_" + sha256(p.read_bytes())[:12]
    spec = importlib.util.spec_from_file_location(nome, p)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nome] = mod
    spec.loader.exec_module(mod)
    return mod, pin(p)


# ---------------------------------------------------------------- 1. o selo e o um.py
def impressao_formal(ff):
    """a impressao digital do kernel (contrato KERNEL_RECIBO_R3): sha256 do JSON canonico (chaves ordenadas, sem espacos, UTF-8) do
    mapa formal_files_sha256 {caminho relativo: sha256}."""
    return sha256(json.dumps(ff, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def ler_nos(nos, versao):
    nos = caminho_canonico(nos)   # o manifesto pina caminhos ABSOLUTOS: um caminho relativo seria resolvido contra a raiz da Bancada (PIN_UNREADABLE)
    um_p, selo_p, core_p = nos / "um.py", nos / "um_absoluto_selo.json", nos / "um_absoluto.json"
    for p in (um_p, selo_p):
        if not p.is_file():
            raise Recusa("NOS_INCOMPLETO: " + str(p))
    raw = um_p.read_bytes()
    selo_raw = selo_p.read_bytes()
    try:
        selo = json.loads(selo_raw)
    except ValueError as exc:
        raise Recusa("SELO_ILEGIVEL: " + str(exc))
    if selo.get("um_version") != versao:
        raise Recusa("SELO_VERSAO_DIFERENTE: selo=%r alvo=%r" % (selo.get("um_version"), versao))
    pinado = (selo.get("sha256") or {}).get("um.py")
    if pinado != sha256(raw):
        raise Recusa("SELO_NAO_PINA_O_UM_PY_DO_DISCO: selo=%s disco=%s" % (str(pinado)[:16], sha256(raw)[:16]))
    texto = raw.decode("utf-8-sig")
    v, a = RE_VERSAO.search(texto), RE_ALPHA.search(texto)
    if v is None or a is None:
        raise Recusa("CANONICAL_DECLARATION_MISSING")
    if v.group(1) != versao:
        raise Recusa("UM_VERSION_DIFERENTE_DO_ALVO: %r" % v.group(1))
    # A11: UM_VERSION e ALPHA sao declaracoes UNICAS: uma linha na coluna 0 e nenhuma reatribuicao indentada.
    # O Python executaria a ULTIMA atribuicao; o canonical.py le a PRIMEIRA: a unica leitura segura e quando so ha uma.
    # Medido no um.py v391 (8e7b9927ceae64b8): 1 linha de cada na coluna 0, 0 indentadas -- a regra nao custa nada ao canonico.
    n_alpha = len(RE_ALPHA_LINHAS.findall(texto))
    if n_alpha != 1:
        raise Recusa("ALPHA_LINHA_NAO_UNICA: %d linhas nao indentadas" % n_alpha)
    n_alpha_ind = len(RE_ALPHA_INDENTADA.findall(texto))
    if n_alpha_ind:
        raise Recusa("ALPHA_REATRIBUIDA_INDENTADA: %d atribuicoes indentadas (o Python executaria a ultima; o contrato le a unica)" % n_alpha_ind)
    n_versao = len(RE_VERSAO_LINHAS.findall(texto))
    if n_versao != 1:
        raise Recusa("UM_VERSION_LINHA_NAO_UNICA: %d linhas nao indentadas" % n_versao)
    n_versao_ind = len(RE_VERSAO_INDENTADA.findall(texto))
    if n_versao_ind:
        raise Recusa("UM_VERSION_REATRIBUIDA_INDENTADA: %d atribuicoes indentadas" % n_versao_ind)
    alpha = float(a.group(1))
    if not (math.isfinite(alpha) and 0 < alpha < 1):
        raise Recusa("ALPHA_OUTSIDE_CONTRACT")
    linha_alpha = texto[:a.start()].count("\n") + 1
    beta = alpha * math.sqrt(math.e)          # EM RUNTIME, nunca literal
    if not core_p.is_file():
        raise Recusa("CORE_AUSENTE: " + str(core_p))
    core_raw = core_p.read_bytes()
    pin_core = (selo.get("sha256") or {}).get("um_absoluto.json")
    if pin_core is not None and pin_core != sha256(core_raw):
        raise Recusa("SELO_NAO_PINA_O_CORE_DO_DISCO")
    core = json.loads(core_raw).get("core") or {}
    beta_core = core.get("beta")
    if not isinstance(beta_core, (int, float)) or isinstance(beta_core, bool):
        raise Recusa("CORE_SEM_BETA")
    rel = abs(beta - float(beta_core)) / beta
    if rel > BETA_TOLERANCIA_REL:
        raise Recusa("BETA_CORE_DIVERGE_DO_RUNTIME: rel=%.3e" % rel)
    core_info = dict(path=str(core_p), bytes=len(core_raw), sha256=sha256(core_raw), beta_core=repr(float(beta_core)),
                     beta_rel_diff=rel, tolerancia_rel=BETA_TOLERANCIA_REL, qg_closure_verdict=core.get("qg_closure_verdict"))
    # N1: o manifesto do kernel que o selo pina (tgl_kernel_proof_manifest.json), lido e conferido por sha; o recibo do B(n) guarda o
    # sha da raiz e do Audit e a impressao formal (sha256 do JSON canonico de formal_files_sha256): e o ANTES que o recibo do kernel
    # da versao seguinte tem de citar (cruzado com o recibo pre-selo)
    kernel_info, kernel_man = None, None
    pin_k = (selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json")
    if pin_k is not None:
        km_p = nos / "tgl_kernel_proof_manifest.json"
        if not km_p.is_file():
            raise Recusa("NOS_INCOMPLETO: " + str(km_p))
        km_raw = km_p.read_bytes()
        if sha256(km_raw) != pin_k:
            raise Recusa("SELO_NAO_PINA_O_MANIFESTO_DO_KERNEL_DO_DISCO: selo=%s disco=%s" % (str(pin_k)[:16], sha256(km_raw)[:16]))
        try:
            kernel_man = json.loads(km_raw)
        except ValueError as exc:
            raise Recusa("MANIFESTO_DO_KERNEL_ILEGIVEL: " + str(exc))
        ff = kernel_man.get("formal_files_sha256") if isinstance(kernel_man, dict) else None
        if not isinstance(ff, dict):
            raise Recusa("MANIFESTO_DO_KERNEL_SEM_FORMAL_FILES")
        kernel_info = dict(manifest=str(km_p), sha256=sha256(km_raw), bytes=len(km_raw), raiz_sha256=ff.get("TGLExt.lean"),
                           audit_sha256=ff.get("TGL/Audit.lean"), n_formal_files=len(ff), impressao_formal=impressao_formal(ff),
                           lean_version=kernel_man.get("lean_version"), lake_version=kernel_man.get("lake_version"))   # N1m: como veio (lista)
    return dict(dir=str(nos), um_py=dict(path=str(um_p), bytes=len(raw), sha256=sha256(raw)), kernel=kernel_info, _kernel_man=kernel_man,
                selo=dict(path=str(selo_p), bytes=len(selo_raw), sha256=sha256(selo_raw), um_version=selo.get("um_version"),
                          qg_closure_verdict=selo.get("qg_closure_verdict"),
                          tgl_kernel_proof_manifest_sha256=(selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json")),
                core=core_info, UM_VERSION=v.group(1),
                alpha=dict(valor=alpha, linha=linha_alpha, n_linhas_nao_indentadas=n_alpha, n_reatribuicoes_indentadas=n_alpha_ind),
                um_version_linhas=dict(nao_indentadas=n_versao, indentadas=n_versao_ind),
                beta_runtime=repr(beta), _beta=beta, _raw=raw, _selo_raw=selo_raw)


# ---------------------------------------------------------------- 2. o evento c1 (A4)
def _hash_evento(e):
    return hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _textos(o):
    """N11: CHAVES e valores (a R2 so olhava valores: «nao_gravar»/«PROIBIDO» numa chave passavam)."""
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield str(k)
            yield from _textos(v)
    elif isinstance(o, list):
        for v in o:
            yield from _textos(v)


def _norm_negacao(t):
    """N11: NFKC -> NFD sem marcas combinantes (Mn) nem formato (Cf) -> caixa dobrada -> tudo que nao e letra/digito vira espaco
    ('_' inclusive, para que «nao_gravar» exponha «nao»)."""
    d = _formas(t)[2].casefold()
    return re.sub(r"[^0-9a-z]+", " ", d)


def negacao_em(o):
    for t in _textos(o):
        m = RE_NEGACAO.search(_norm_negacao(t))
        if m:
            return m.group(0)
    return None


def verificar_evento(evento, versao, bancada, sandbox, nos_info, reparo=False, eventos_path=None, evento_hash=None):
    """A4: o evento que autoriza a gravacao e lido do livro de eventos pela CADEIA DE HASH (a mesma regra de iald.py verificar():
    anterior == hash do elo anterior e hash == sha256 do proprio elo sem o campo hash), do primeiro elo ate o evento citado; os
    campos sao conferidos por JSON, nao por substring; texto que negue a gravacao e recusado.
    R3 (N6, [INPUT da gerencia]): o hash do elo (>= 16 hex, --evento-hash) tem de conferir com o elo achado na cadeia; as chaves de
    dados sao um conjunto FECHADO; a negacao e procurada em chaves e valores normalizados (N11). A autoria (quem == claude-c1) e
    CONVENCAO do quadro, nao autenticacao: iald.py anotar aceita --quem livre; a cadeia prova integridade e ordem, nao quem escreveu."""
    if evento is None or not str(evento).strip():
        raise Recusa("EVENTO_C1_AUSENTE: nenhuma gravacao na Bancada sem evento c1 nomeado")
    ev = str(evento).strip()
    eventos_path = Path(eventos_path) if eventos_path else EVENTOS_QUADRO
    if ev.startswith("SANDBOX:"):
        if not sandbox:
            raise Recusa("EVENTO_SANDBOX_FORA_DO_SANDBOX")
        return dict(evento=ev, verificado=False, nota="sandbox: evento literal, nao conferido no quadro")
    if not ev.isdigit():
        raise Recusa("EVENTO_C1_INVALIDO: %r (seq numerico de eventos.jsonl ou, so em --sandbox, SANDBOX:<texto>)" % ev)
    if not eventos_path.is_file():
        raise Recusa("EVENTOS_JSONL_AUSENTE: " + str(eventos_path))
    seq = int(ev)
    ant, achado, n, seqs = "0" * 64, None, 0, set()
    for linha in eventos_path.read_text(encoding="utf-8").splitlines():
        if not linha.strip():
            continue
        try:
            e = json.loads(linha)
        except ValueError as exc:
            raise Recusa("EVENTOS_JSONL_ILEGIVEL: linha %d: %s" % (n + 1, exc))
        n += 1
        if e.get("anterior") != ant or e.get("hash") != _hash_evento(e):
            raise Recusa("EVENTOS_CADEIA_QUEBRADA: no evento seq %r (elo %d)" % (e.get("seq"), n))
        ant = e["hash"]
        if e.get("seq") in seqs:
            raise Recusa("EVENTO_SEQ_DUPLICADO: %r" % e.get("seq"))
        seqs.add(e.get("seq"))
        if e.get("seq") == seq:
            achado = e
    if achado is None:
        raise Recusa("EVENTO_NAO_ENCONTRADO: seq %d (cadeia integra ate o elo %d)" % (seq, n))
    e = achado
    if e.get("quem") != EVENTO_AUTOR:
        raise Recusa("EVENTO_NAO_E_DA_C1: seq %d por %r" % (seq, e.get("quem")))
    if e.get("tipo") != EVENTO_TIPO:
        raise Recusa("EVENTO_TIPO_INVALIDO: seq %d tipo %r (exigido %s)" % (seq, e.get("tipo"), EVENTO_TIPO))
    d = e.get("dados")
    if not isinstance(d, dict):
        raise Recusa("EVENTO_SEM_DADOS_JSON: seq %d" % seq)
    neg = negacao_em(d)
    if neg:
        raise Recusa("EVENTO_COM_NEGACAO: seq %d contem %r (forma normalizada) -- um evento que nega nao autoriza" % (seq, neg))
    fora = sorted(str(k) for k in d if k not in CHAVES_EVENTO)
    if fora:
        raise Recusa("EVENTO_CHAVE_NAO_ADMITIDA: seq %d chaves %s fora do conjunto fechado %s" % (seq, fora, sorted(CHAVES_EVENTO)))
    if d.get("versao") != versao:
        raise Recusa("EVENTO_NAO_NOMEIA_A_VERSAO: seq %d versao=%r alvo=%r" % (seq, d.get("versao"), versao))
    if d.get("acao") != "sincronizacao":
        raise Recusa("EVENTO_NAO_NOMEIA_A_SINCRONIZACAO: seq %d acao=%r" % (seq, d.get("acao")))
    if not isinstance(d.get("bancada"), str) or not mesmo_no(d["bancada"], bancada):
        raise Recusa("EVENTO_NAO_NOMEIA_ESTA_BANCADA: seq %d bancada=%r alvo=%s" % (seq, d.get("bancada"), bancada))
    for campo, chave in (("um_py", "um_py"), ("selo", "selo")):
        val = d.get(campo)
        esperado = nos_info[chave]["sha256"]
        if not isinstance(val, str) or len(val) < 16 or not esperado.startswith(val.lower()):
            raise Recusa("EVENTO_NAO_NOMEIA_O_PROGRAMA: seq %d %s=%r nao e prefixo (>=16 hex) de %s" % (seq, campo, val, esperado[:16]))
    if reparo and d.get("reparo") is not True:
        raise Recusa("EVENTO_NAO_AUTORIZA_REPARO: seq %d sem dados.reparo=true" % seq)
    if "reparo" in d and not isinstance(d.get("reparo"), bool):
        raise Recusa("EVENTO_REPARO_NAO_BOOLEANO: seq %d" % seq)
    # N6: o hash do elo, passado pela cadeia (lido do retorno de iald.py anotar), tem de ser o do elo achado
    if evento_hash is None or not str(evento_hash).strip():
        raise Recusa("EVENTO_HASH_AUSENTE: seq %d -- a cadeia passa --evento-hash <hash16> do elo que ela anotou" % seq)
    eh = str(evento_hash).strip().lower()
    if not re.match(r"^[0-9a-f]{16,64}$", eh):
        raise Recusa("EVENTO_HASH_INVALIDO: %r (16 a 64 hex)" % evento_hash)
    if not str(e.get("hash") or "").startswith(eh):
        raise Recusa("EVENTO_HASH_DIVERGE: seq %d hash %s != esperado %s" % (seq, str(e.get("hash"))[:16], eh[:16]))
    return dict(evento=seq, verificado=True, hash_conferido=eh, autoria="convencao (quem=claude-c1), nao autenticacao", quando=e.get("quando"), tipo=e.get("tipo"), hash=e.get("hash"), anterior=e.get("anterior"),
                cadeia_conferida_ate=n, fonte=str(eventos_path), fonte_e_o_quadro=mesmo_no(eventos_path, EVENTOS_QUADRO) if EVENTOS_QUADRO.exists() else False,
                dados=dict(versao=d.get("versao"), bancada=d.get("bancada"), um_py=d.get("um_py"), selo=d.get("selo"), reparo=d.get("reparo"),
                           gravacoes=d.get("gravacoes"), unidade=d.get("unidade")))


# ---------------------------------------------------------------- 3. o manifesto vigente e o estado do contrato
def estado_anterior(bancada, canonical_mod):
    bancada = Path(bancada)
    man_p = bancada / "canonical_contracts.json"
    if not man_p.is_file():
        raise Recusa("MANIFESTO_AUSENTE: " + str(man_p))
    raw = man_p.read_bytes()
    man = json.loads(raw)
    if man.get("schema") != 1:
        raise Recusa("CANONICAL_SCHEMA_UNSUPPORTED")
    estado, recibo = "OK", None
    try:
        reg = canonical_mod.CanonicalRegistry(bancada)
        recibo = reg.check("pre_sincronizacao")
    except canonical_mod.CanonicalError as exc:
        estado = str(exc).split(":")[0]
    return dict(path=str(man_p), bytes=len(raw), sha256=sha256(raw), deployment_id=man.get("deployment_id"),
                version=(man.get("canonical") or {}).get("version"),
                um_py_pinado=((man.get("canonical") or {}).get("script") or {}).get("sha256"),
                script_path_pinado=((man.get("canonical") or {}).get("script") or {}).get("path"),
                seal_path_pinado=((man.get("canonical") or {}).get("seal") or {}).get("path"),
                seal_sha_pinado=((man.get("canonical") or {}).get("seal") or {}).get("sha256"),
                n_code=len(man.get("code") or []), n_sources=len(man.get("sources") or []),
                estado_do_contrato_instalado=estado,
                recibo=({k: recibo[k] for k in ("ok", "canonical_version", "um_py_sha256", "beta_tgl", "deployment_id")} if recibo else None),
                _man=man, _raw=raw)


def sonda_pos_selo_em_ram(bancada, canonical_mod, anterior, nos_info):
    """Quando o Nos alvo NAO mora no caminho pinado (so em --sandbox): prova em RAM que, se os bytes do caminho pinado fossem os do
    Nos alvo (o que o selo faz em producao), o canonical.py INSTALADO recusaria. Nada e escrito."""
    script_p = Path(anterior["script_path_pinado"]).resolve()
    seal_p = Path(anterior["seal_path_pinado"]).resolve()
    orig = Path.read_bytes

    def leitor(path):
        p = Path(path).resolve()
        if p == script_p:
            return nos_info["_raw"]
        if p == seal_p:
            return nos_info["_selo_raw"]
        return orig(path)
    with patch.object(Path, "read_bytes", leitor):
        try:
            canonical_mod.CanonicalRegistry(Path(bancada))
            return dict(recusou=False, codigo="ACEITO (inesperado)")
        except canonical_mod.CanonicalError as exc:
            return dict(recusou=True, codigo=str(exc).split(":")[0])


def kernel_do_selo_anterior(selo_anterior, kernel_manifesto_anterior, ref_selo, ref_versao):
    """R31-3 (R3.2): o pino do manifesto do kernel que o SELO ANTERIOR grava, lido de fonte EXTERNA ao recibo pre-selo:
      --selo-anterior: o selo da versao anterior (copia de custodia; o do Nos ja e o novo depois do selo), cujo sha256 tem de ser o selo
        pinado no manifesto vigente da Bancada (canonical.seal.sha256; na re-execucao, sincronizacao.anterior.seal_sha_pinado);
      --kernel-manifesto-anterior: o manifesto do kernel dessa versao, cujo sha256 tem de ser o que esse selo pina
        (sha256["tgl_kernel_proof_manifest.json"]); dele se RECALCULAM a raiz, o Audit e a impressao formal.
    Devolve dict(pin, raiz_sha256, audit_sha256, impressao_formal, ...). Nenhum campo do proprio recibo entra aqui."""
    if not selo_anterior or not kernel_manifesto_anterior:
        raise Recusa("SELO_ANTERIOR_AUSENTE: o recibo pre-selo exige --selo-anterior (o selo da versao anterior, da custodia) e --kernel-manifesto-anterior "
                     "(o manifesto do kernel que esse selo pina): o ANTES do T17 nao se cruza com campo do proprio recibo (R31-3)")
    sp, kp = Path(selo_anterior), Path(kernel_manifesto_anterior)
    if not sp.is_file():
        raise Recusa("SELO_ANTERIOR_AUSENTE: " + str(sp))
    if not kp.is_file():
        raise Recusa("SELO_ANTERIOR_AUSENTE: manifesto do kernel anterior inexistente: " + str(kp))
    sraw = sp.read_bytes()
    if not ref_selo or sha256(sraw) != str(ref_selo).lower():
        raise Recusa("SELO_ANTERIOR_NAO_E_O_PINADO: --selo-anterior %s != o selo pinado no manifesto vigente da Bancada %s (R31-3)" % (sha256(sraw)[:16], str(ref_selo)[:16]))
    try:
        selo = json_estrito(sraw)
    except ValueError as exc:
        raise Recusa("SELO_ANTERIOR_ILEGIVEL: %s" % exc)
    if not isinstance(selo, dict) or selo.get("um_version") != ref_versao:
        raise Recusa("SELO_ANTERIOR_NAO_E_O_PINADO: um_version=%r, versao anterior da Bancada %r (R31-3)" % (selo.get("um_version") if isinstance(selo, dict) else None, ref_versao))
    pin_k = str((selo.get("sha256") or {}).get("tgl_kernel_proof_manifest.json") or "").lower()
    if not _hex64(pin_k):
        raise Recusa("SELO_ANTERIOR_SEM_PINO_DO_KERNEL: o selo anterior nao pina tgl_kernel_proof_manifest.json (R31-3)")
    kraw = kp.read_bytes()
    if sha256(kraw) != pin_k:
        raise Recusa("KERNEL_MANIFESTO_ANTERIOR_NAO_E_O_DO_SELO: --kernel-manifesto-anterior %s != o pino do selo anterior %s (R31-3)" % (sha256(kraw)[:16], pin_k[:16]))
    try:
        kman = json_estrito(kraw)
    except ValueError as exc:
        raise Recusa("KERNEL_MANIFESTO_ANTERIOR_ILEGIVEL: %s" % exc)
    ff = kman.get("formal_files_sha256") if isinstance(kman, dict) else None
    if not isinstance(ff, dict) or not _hex64(ff.get("TGLExt.lean")) or not _hex64(ff.get("TGL/Audit.lean")):
        raise Recusa("KERNEL_MANIFESTO_ANTERIOR_SEM_FORMAL_FILES (R31-3)")
    return dict(selo_anterior=dict(path=str(sp), sha256=sha256(sraw), um_version=selo.get("um_version")),
                kernel_manifesto_anterior=dict(path=str(kp), sha256=pin_k), pin=pin_k, raiz_sha256=ff["TGLExt.lean"].lower(),
                audit_sha256=ff["TGL/Audit.lean"].lower(), impressao_formal=impressao_formal(ff))


# ---------------------------------------------------------------- 3b. R3.4 (S): o salto -- a cadeia de selos entre a versao que a Bancada pina e a do Nos
def versao_numero(v):
    """vNNN -> NNN (inteiro); qualquer outra forma e recusa."""
    m = RE_VNNN.match(str(v))
    if not m:
        raise Recusa("VERSAO_INVALIDA: %r (vNNN)" % (v,))
    return int(m.group(1))


def versao_seguinte(v):
    """a versao que se sela depois de `v`, com a mesma largura de digitos (v393 -> v394)."""
    m = RE_VNNN.match(str(v))
    if not m:
        raise Recusa("VERSAO_INVALIDA: %r (vNNN)" % (v,))
    return "v%0*d" % (len(m.group(1)), int(m.group(1)) + 1)


def _arquivo_da_cadeia(d, rotulo):
    """um arquivo pinado da cadeia {path absoluto, sha256, bytes}: lido de verdade e conferido por tamanho e sha256; nunca juncao/link. Devolve (dict, bytes)."""
    if not isinstance(d, dict) or set(d) != CADEIA_ARQ_CHAVES:
        raise Recusa("CADEIA_DE_SELOS_ARQUIVO_INVALIDO: %s exige exatamente {path, sha256, bytes}: %r" % (rotulo, d))
    p, h, n = d["path"], d["sha256"], d["bytes"]
    if not isinstance(p, str) or not p or not isinstance(h, str) or not _hex64(h) or h != h.lower() or type(n) is not int or n < 0:
        raise Recusa("CADEIA_DE_SELOS_ARQUIVO_INVALIDO: %s: path texto, sha256 minusculo de 64 hex e bytes int >= 0" % rotulo)
    if not Path(p).is_absolute():
        raise Recusa("CADEIA_DE_SELOS_CAMINHO_NAO_ABSOLUTO: %s: %s" % (rotulo, p))
    pc = caminho_canonico(p)
    if not pc.is_file() or Path(p).is_symlink():
        raise Recusa("CADEIA_DE_SELOS_COPIA_AUSENTE: %s: %s (arquivo regular; link nao vale)" % (rotulo, p))
    b = pc.read_bytes()
    if len(b) != n or sha256(b) != h:
        raise Recusa("CADEIA_DE_SELOS_COPIA_DIVERGE: %s: o arquivo em disco (%d B, %s) nao e o pinado (%d B, %s)" % (rotulo, len(b), sha256(b)[:16], n, h[:16]))
    return dict(path=str(p), sha256=h, bytes=n), b


def _ler_elo_da_cadeia(e, i):
    """um elo: versao vNNN; copias de bytes do um.py, do selo e do manifesto do kernel; o selo diz a versao do elo e pina o um.py e o manifesto do kernel DESSE elo;
    UM_VERSION e ALPHA do um.py sao linhas unicas (as regras da ler_nos). `substituido_na_instalacao_por` e conferido na ligacao com o elo seguinte."""
    if not isinstance(e, dict) or not set(e) <= CADEIA_ELO_CHAVES or not {"versao", "um_py", "selo", "kernel_manifesto"} <= set(e):
        raise Recusa("CADEIA_DE_SELOS_ELO_INVALIDO: elo %d: chaves %s (admitidas %s; obrigatorias versao, um_py, selo, kernel_manifesto)"
                     % (i, sorted(e) if isinstance(e, dict) else type(e).__name__, sorted(CADEIA_ELO_CHAVES)))
    v = e["versao"]
    n = versao_numero(v)
    um, um_b = _arquivo_da_cadeia(e["um_py"], "%s.um_py" % v)
    selo, selo_b = _arquivo_da_cadeia(e["selo"], "%s.selo" % v)
    km, km_b = _arquivo_da_cadeia(e["kernel_manifesto"], "%s.kernel_manifesto" % v)
    try:
        texto = um_b.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise Recusa("CADEIA_DE_SELOS_UM_PY_ILEGIVEL: %s: %s" % (v, exc))
    mv = RE_VERSAO.search(texto)
    if mv is None or mv.group(1) != v:
        raise Recusa("CADEIA_DE_SELOS_UM_PY_DE_OUTRA_VERSAO: o um.py do elo %s declara UM_VERSION=%r" % (v, mv.group(1) if mv else None))
    if len(RE_VERSAO_LINHAS.findall(texto)) != 1 or RE_VERSAO_INDENTADA.search(texto) or len(RE_ALPHA_LINHAS.findall(texto)) != 1 or RE_ALPHA_INDENTADA.search(texto):
        raise Recusa("CADEIA_DE_SELOS_UM_PY_COM_DECLARACAO_NAO_UNICA: o um.py do elo %s nao tem UM_VERSION e ALPHA como linhas unicas na coluna 0" % v)
    try:
        sj = json_estrito(selo_b)
    except ValueError as exc:
        raise Recusa("CADEIA_DE_SELOS_SELO_ILEGIVEL: %s: %s" % (v, exc))
    if not isinstance(sj, dict) or sj.get("um_version") != v:
        raise Recusa("CADEIA_DE_SELOS_SELO_DE_OUTRA_VERSAO: o selo do elo %s diz um_version=%r" % (v, sj.get("um_version") if isinstance(sj, dict) else None))
    pinos = sj.get("sha256")
    if not isinstance(pinos, dict) or str(pinos.get("um.py") or "").lower() != um["sha256"]:
        raise Recusa("CADEIA_DE_SELOS_SELO_NAO_PINA_O_UM_PY: o selo do elo %s pina um.py %s e a copia do elo e %s"
                     % (v, str((pinos or {}).get("um.py"))[:16], um["sha256"][:16]))
    if str(pinos.get("tgl_kernel_proof_manifest.json") or "").lower() != km["sha256"]:
        raise Recusa("CADEIA_DE_SELOS_SELO_NAO_PINA_O_KERNEL: o selo do elo %s pina o manifesto do kernel %s e a copia do elo e %s"
                     % (v, str(pinos.get("tgl_kernel_proof_manifest.json"))[:16], km["sha256"][:16]))
    return dict(versao=v, n=n, um_py=um, selo=selo, kernel_manifesto=km, instalacao=e.get("substituido_na_instalacao_por"))


def _conferir_ligacao_da_cadeia(a, b):
    """a -> b: o registro do instalador (APLICADO_AO_CANONICO) que SUBSTITUIU a por b diz, por sha16, o que fez backup (um.py e selo de `a`) e o que instalou
    (o um.py de `b`); os backups de BYTES do instalador (.bak_) tem de ser, byte a byte, as copias do elo `a`. Nenhum campo do selo e usado como pino do anterior:
    o selo nao pina o selo anterior (medido na v393); a ligacao vem do instalador, que gravou o backup antes de trocar."""
    inst = a["instalacao"]
    if not isinstance(inst, dict) or set(inst) != CADEIA_INSTALACAO_CHAVES:
        raise Recusa("CADEIA_DE_SELOS_ELO_QUEBRADO: o elo %s nao traz exatamente substituido_na_instalacao_por {%s}" % (a["versao"], ", ".join(sorted(CADEIA_INSTALACAO_CHAVES))))
    if inst["versao"] != b["versao"]:
        raise Recusa("CADEIA_DE_SELOS_ELO_QUEBRADO: o elo %s diz ter sido substituido por %r e o elo seguinte e %s" % (a["versao"], inst["versao"], b["versao"]))
    reg, reg_b = _arquivo_da_cadeia(inst["registro"], "%s.registro_do_instalador" % a["versao"])
    bk_um, _ = _arquivo_da_cadeia(inst["backup_um_py"], "%s.backup_um_py" % a["versao"])
    bk_selo, _ = _arquivo_da_cadeia(inst["backup_selo"], "%s.backup_selo" % a["versao"])
    for rot, bk, copia in (("um.py", bk_um, a["um_py"]), ("selo", bk_selo, a["selo"])):
        if bk["sha256"] != copia["sha256"] or bk["bytes"] != copia["bytes"]:
            raise Recusa("CADEIA_DE_SELOS_ELO_QUEBRADO: o backup de bytes do instalador (%s) do %s de %s (%s) nao e a copia do elo (%s)"
                         % (Path(bk["path"]).name, rot, a["versao"], bk["sha256"][:16], copia["sha256"][:16]))
    try:
        rj = json_estrito(reg_b)
    except ValueError as exc:
        raise Recusa("CADEIA_DE_SELOS_REGISTRO_ILEGIVEL: %s: %s" % (a["versao"], exc))
    bks, novo = (rj.get("backups") if isinstance(rj, dict) else None), (rj.get("um_py_novo") if isinstance(rj, dict) else None)
    if not isinstance(bks, dict) or not isinstance(novo, dict):
        raise Recusa("CADEIA_DE_SELOS_REGISTRO_ILEGIVEL: o registro do instalador de %s nao traz backups e um_py_novo" % a["versao"])
    for rot, nome, bk, copia in (("um.py", "um.py", bk_um, a["um_py"]), ("selo", "um_absoluto_selo.json", bk_selo, a["selo"])):
        d = bks.get(nome)
        if (not isinstance(d, dict) or str(d.get("sha16") or "").lower() != copia["sha256"][:16] or d.get("bytes") != copia["bytes"]
                or not isinstance(d.get("backup"), str) or not mesmo_no(d["backup"], bk["path"])):
            raise Recusa("CADEIA_DE_SELOS_ELO_QUEBRADO: o registro do instalador (%s) nao diz que fez o backup %s do %s de %s (sha16 %s, %s bytes, o arquivo da cadeia)"
                         % (Path(reg["path"]).name, Path(bk["path"]).name, rot, a["versao"], copia["sha256"][:16], copia["bytes"]))
    if str(novo.get("sha16") or "").lower() != b["um_py"]["sha256"][:16] or novo.get("bytes") != b["um_py"]["bytes"]:
        raise Recusa("CADEIA_DE_SELOS_ELO_QUEBRADO: o registro do instalador (%s) instalou o um.py %s (%s B) e o elo seguinte %s tem %s (%d B)"
                     % (Path(reg["path"]).name, str(novo.get("sha16"))[:16], novo.get("bytes"), b["versao"], b["um_py"]["sha256"][:16], b["um_py"]["bytes"]))
    return dict(de=a["versao"], para=b["versao"], registro_sha256=reg["sha256"], backup_um_py_sha256=bk_um["sha256"], backup_selo_sha256=bk_selo["sha256"])


def carregar_cadeia_de_selos(cp, sha_esperado):
    """R3.4 (S): o arquivo da cadeia (contrato CADEIA_DE_SELOS_R3_4), pinado por sha256 (--cadeia-de-selos-sha256, lido de vNNN_pins), sem chave duplicada, com chaves
    fechadas. Um elo por versao, consecutivas e crescentes (nenhuma versao pulada sem elo); copias de bytes conferidas (um.py, selo, manifesto do kernel; o selo
    pina o um.py e o manifesto do kernel do proprio elo); cada elo menos o ultimo traz o registro do instalador que o substituiu e os backups de bytes dele."""
    if not sha_esperado:
        raise Recusa("CADEIA_DE_SELOS_SHA_AUSENTE: a cadeia passa --cadeia-de-selos-sha256 (lido de vNNN_pins); um arquivo de cadeia sem pino nao vale")
    cp = Path(cp)
    if not cp.is_file():
        raise Recusa("CADEIA_DE_SELOS_AUSENTE: " + str(cp))
    raw = cp.read_bytes()
    if str(sha_esperado).lower() != sha256(raw):
        raise Recusa("CADEIA_DE_SELOS_SHA_DIVERGE: arquivo %s != esperado %s" % (sha256(raw)[:16], str(sha_esperado)[:16]))
    try:
        c = json_estrito(raw)
    except ChaveDuplicada as exc:
        raise Recusa("CADEIA_DE_SELOS_CHAVE_DUPLICADA: %s" % exc)
    except ValueError as exc:
        raise Recusa("CADEIA_DE_SELOS_ILEGIVEL: %s" % exc)
    if not isinstance(c, dict) or not set(c) <= CADEIA_RAIZ_CHAVES:
        raise Recusa("CADEIA_DE_SELOS_ILEGIVEL: chaves fora do conjunto fechado %s: %s" % (sorted(CADEIA_RAIZ_CHAVES), sorted(c) if isinstance(c, dict) else type(c).__name__))
    if c.get("contrato") != CADEIA_CONTRATO:
        raise Recusa("CADEIA_DE_SELOS_CONTRATO_INVALIDO: %r (exigido %s)" % (c.get("contrato"), CADEIA_CONTRATO))
    elos = c.get("elos")
    if not isinstance(elos, list) or not (2 <= len(elos) <= CADEIA_MAX_ELOS):
        raise Recusa("CADEIA_DE_SELOS_ILEGIVEL: elos exige uma lista de 2 a %d elos (a Bancada e o Nos: um salto tem ao menos dois)" % CADEIA_MAX_ELOS)
    lidos = [_ler_elo_da_cadeia(e, i) for i, e in enumerate(elos)]
    for x, y in zip(lidos, lidos[1:]):
        if y["n"] != x["n"] + 1:
            raise Recusa("CADEIA_DE_SELOS_NAO_CONSECUTIVA: depois do elo %s vem %s (nenhuma versao pode ficar sem elo, nem repetida, nem fora de ordem)" % (x["versao"], y["versao"]))
    if lidos[-1]["instalacao"] is not None:
        raise Recusa("CADEIA_DE_SELOS_ELO_FINAL_COM_INSTALACAO: o ultimo elo (%s) ainda nao foi substituido; substituido_na_instalacao_por nao se admite nele" % lidos[-1]["versao"])
    ligacoes = [_conferir_ligacao_da_cadeia(x, y) for x, y in zip(lidos, lidos[1:])]
    return dict(path=str(cp), sha256=sha256(raw), bytes=len(raw), contrato=CADEIA_CONTRATO, n_elos=len(lidos), versoes=[e["versao"] for e in lidos], elos=lidos, ligacoes=ligacoes)


def conferir_cadeia_com_a_bancada(cad, anterior):
    """o INICIO da cadeia e o que a Bancada pina agora: versao, um.py, selo e (quando o manifesto o registra, B4 em diante) o manifesto do kernel."""
    e0 = cad["elos"][0]
    for nome, val, esp in (("versao", e0["versao"], anterior["version"]), ("um.py", e0["um_py"]["sha256"], anterior["um_py_pinado"]),
                           ("selo", e0["selo"]["sha256"], anterior["seal_sha_pinado"])):
        if str(val) != str(esp):
            raise Recusa("CADEIA_DE_SELOS_NAO_PARTE_DA_BANCADA: o primeiro elo (%s) tem %s %s e a Bancada pina %s" % (e0["versao"], nome, str(val)[:16], str(esp)[:16]))
    reg = (anterior["_man"].get("sincronizacao") or {}).get("kernel_manifesto_sha256")
    if reg is not None and str(reg).lower() != e0["kernel_manifesto"]["sha256"]:
        raise Recusa("CADEIA_DE_SELOS_NAO_PARTE_DA_BANCADA: o manifesto da Bancada registra o manifesto do kernel %s e o primeiro elo (%s) traz %s"
                     % (str(reg)[:16], e0["versao"], e0["kernel_manifesto"]["sha256"][:16]))


def conferir_cadeia_com_o_fim(cad, versao, um_sha, selo_sha, km_sha, quem):
    """o FIM da cadeia e a versao que o Nos tem (pre_selo: o Nos lido agora; pos_selo: o que o recibo pre-selo pinado diz do Nos)."""
    e = cad["elos"][-1]
    for nome, val, esp in (("versao", e["versao"], versao), ("um.py", e["um_py"]["sha256"], um_sha), ("selo", e["selo"]["sha256"], selo_sha),
                           ("manifesto do kernel", e["kernel_manifesto"]["sha256"], km_sha)):
        if str(val) != str(esp):
            raise Recusa("CADEIA_DE_SELOS_NAO_CHEGA_AO_NOS: o ultimo elo (%s) tem %s %s e %s tem %s" % (e["versao"], nome, str(val)[:16], quem, str(esp)[:16]))


def montar_salto(cad, anterior):
    """o bloco que o recibo declara (e o manifesto novo registra): de onde a Bancada sai, onde o Nos esta, as versoes puladas (nenhuma teve elo B(n)) e a cadeia."""
    e0, eN = cad["elos"][0], cad["elos"][-1]
    return dict(contrato=SALTO_CONTRATO, declarado=True,
                de=dict(versao=e0["versao"], um_py_sha256=e0["um_py"]["sha256"], selo_sha256=e0["selo"]["sha256"], kernel_manifesto_sha256=e0["kernel_manifesto"]["sha256"],
                        manifesto_da_bancada_sha256=anterior["sha256"], deployment_id=anterior["deployment_id"]),
                ate=dict(versao=eN["versao"], um_py_sha256=eN["um_py"]["sha256"], selo_sha256=eN["selo"]["sha256"], kernel_manifesto_sha256=eN["kernel_manifesto"]["sha256"]),
                versoes_puladas=[e["versao"] for e in cad["elos"][1:]], proxima_a_selar=versao_seguinte(eN["versao"]),
                cadeia=dict(sha256=cad["sha256"], n_elos=cad["n_elos"], versoes=list(cad["versoes"]),
                            ligacoes=[dict(de=l["de"], para=l["para"], registro_sha256=l["registro_sha256"]) for l in cad["ligacoes"]]))


def cadeia_para_recibo(cad):
    """o que do carregamento vai ao recibo (sem os bytes): caminhos, pinos e os pinos dos elos."""
    return dict(path=cad["path"], sha256=cad["sha256"], bytes=cad["bytes"], contrato=cad["contrato"], n_elos=cad["n_elos"], versoes=list(cad["versoes"]),
                elos=[dict(versao=e["versao"], um_py=e["um_py"], selo=e["selo"], kernel_manifesto=e["kernel_manifesto"]) for e in cad["elos"]], ligacoes=cad["ligacoes"])


def conferir_recibo_pre_selo(rp, anterior, bancada, ja_sincronizada=False, sha_esperado=None, selo_anterior=None, kernel_manifesto_anterior=None, cadeia=None):
    """A6: o recibo pre-selo e conferido por identidade, nao so por fase e veredito: a versao alvo dele e a versao ANTERIOR da
    Bancada (a que estava canonica antes do selo), o um.py que ele leu e o um.py antes pinado, a Bancada e a mesma por identidade.
    Se a Bancada JA pina a versao alvo (re-execucao idempotente), a referencia e a geracao anterior registrada no bloco
    sincronizacao.anterior do manifesto vigente (o B(n) que a gravou); sem esse bloco, nao ha referencia e a conferencia recusa."""
    ref_versao, ref_um_py, ref_selo = anterior["version"], anterior["um_py_pinado"], anterior["seal_sha_pinado"]
    if ja_sincronizada:
        ant = ((anterior["_man"].get("sincronizacao") or {}).get("anterior") or {})
        ref_versao, ref_um_py, ref_selo = ant.get("version"), ant.get("um_py_pinado"), ant.get("seal_sha_pinado")
        if not ref_versao or not ref_um_py:
            raise Recusa("RECIBO_PRE_SELO_SEM_REFERENCIA: a Bancada ja pina a versao alvo e o manifesto nao registra a geracao anterior")
        if not ref_selo:
            raise Recusa("RECIBO_PRE_SELO_SEM_REFERENCIA: o manifesto vigente nao registra o selo da geracao anterior (seal_sha_pinado, R3.1)")
    rp = Path(rp)
    if not rp.is_file():
        raise Recusa("RECIBO_PRE_SELO_AUSENTE: " + str(rp))
    raw = rp.read_bytes()
    # N2: o recibo pre-selo e conferido por PINO (o sha que vNNN_pins guardou), alem do conteudo: um JSON escrito a mao nao passa
    if sha_esperado is not None and str(sha_esperado).lower() != sha256(raw):
        raise Recusa("RECIBO_PRE_SELO_SHA_DIVERGE: arquivo %s != esperado %s" % (sha256(raw)[:16], str(sha_esperado)[:16]))
    try:
        rj = json.loads(raw)
    except ValueError as exc:
        raise Recusa("RECIBO_PRE_SELO_ILEGIVEL: " + str(exc))
    if not isinstance(rj, dict):
        raise Recusa("RECIBO_PRE_SELO_ILEGIVEL: nao e objeto JSON")
    # R3.4 (S): o recibo pre-selo de um SALTO (a Bancada pinava uma versao anterior a do Nos) declara `salto`; a referencia deixa de ser a versao que a Bancada
    # pinava e passa a ser o FIM da cadeia de selos (a versao do Nos naquele momento), com a cadeia conferida por hash contra a Bancada e contra o recibo.
    salto_rj = rj.get("salto")
    salto_man = (anterior["_man"].get("sincronizacao") or {}).get("salto") if ja_sincronizada else None
    esp_salto, ref_kman_salto = None, None
    if salto_rj is not None or salto_man is not None:
        if salto_rj is None:
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o manifesto da Bancada foi gravado por um salto (sincronizacao.salto) e o recibo pre-selo nao declara salto (R3.4)")
        if not isinstance(salto_rj, dict) or salto_rj.get("contrato") != SALTO_CONTRATO:
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o salto do recibo nao traz o contrato %s (R3.4)" % SALTO_CONTRATO)
        if ja_sincronizada:
            if not isinstance(salto_man, dict):
                raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o recibo pre-selo declara salto e o manifesto da Bancada (ja sincronizada) nao registra sincronizacao.salto (R3.4)")
            esp_salto = salto_man
            if cadeia is not None and cadeia["sha256"] != str((salto_man.get("cadeia") or {}).get("sha256")):
                raise Recusa("CADEIA_DE_SELOS_NAO_E_A_DO_SALTO_REGISTRADO: a cadeia dada (%s) nao e a que o manifesto da Bancada registra (%s) (R3.4)"
                             % (cadeia["sha256"][:16], str((salto_man.get("cadeia") or {}).get("sha256"))[:16]))
        else:
            if cadeia is None:
                raise Recusa("RECIBO_PRE_SELO_SALTO_SEM_CADEIA: o recibo pre-selo declara salto; a cadeia de selos (--cadeia-de-selos e --cadeia-de-selos-sha256) e obrigatoria para conferi-lo (R3.4)")
            conferir_cadeia_com_a_bancada(cadeia, anterior)
            esp_salto = montar_salto(cadeia, anterior)
        if json.dumps(salto_rj, sort_keys=True) != json.dumps(esp_salto, sort_keys=True):
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o salto que o recibo declara nao e o que a cadeia de selos %s e a Bancada dizem (de %s, ate %s, puladas %s) (R3.4)"
                         % (esp_salto["cadeia"]["sha256"][:16], esp_salto["de"]["versao"], esp_salto["ate"]["versao"], esp_salto["versoes_puladas"]))
        ref_versao, ref_um_py, ref_selo = esp_salto["ate"]["versao"], esp_salto["ate"]["um_py_sha256"], esp_salto["ate"]["selo_sha256"]
        ref_kman_salto = esp_salto["ate"]["kernel_manifesto_sha256"]
    elif cadeia is not None:
        raise Recusa("CADEIA_DE_SELOS_SEM_SALTO: --cadeia-de-selos so serve ao recibo pre-selo de um salto (o recibo dado nao declara salto) (R3.4)")
    bat = rj.get("bateria_resultado") or {}
    if rj.get("fase") != "pre_selo" or bat.get("veredito") != "BATERIA_PASSA":
        raise Recusa("RECIBO_PRE_SELO_INVALIDO: fase=%r bateria=%r" % (rj.get("fase"), bat.get("veredito")))
    if esp_salto is None:
        if not str(rj.get("veredito") or "").startswith("JA_SINCRONIZADA__ENSAIO"):
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: veredito=%r (exigido JA_SINCRONIZADA__ENSAIO...)" % rj.get("veredito"))
    else:
        mv_ = re.match(r"^REPINADA_B(\d+)__SALTO_(v\d{3,4})_(v\d{3,4})__ENSAIO(?:__|$)", str(rj.get("veredito") or ""))
        gm_ = RE_GERACAO.match(str(anterior["_man"].get("deployment_id") or ""))
        n_esp = (int(gm_.group(1)) + (0 if ja_sincronizada else 1)) if gm_ else None
        if not mv_ or mv_.group(2) != esp_salto["de"]["versao"] or mv_.group(3) != esp_salto["ate"]["versao"] or n_esp is None or int(mv_.group(1)) != n_esp:
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: veredito=%r (exigido REPINADA_B%s__SALTO_%s_%s__ENSAIO...) (R3.4)"
                         % (rj.get("veredito"), n_esp, esp_salto["de"]["versao"], esp_salto["ate"]["versao"]))
    if rj.get("versao_alvo") != ref_versao:
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: versao_alvo=%r != versao anterior da Bancada %r" % (rj.get("versao_alvo"), ref_versao))
    um_sha = ((rj.get("nos") or {}).get("um_py") or {}).get("sha256")
    if um_sha != ref_um_py:
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: um.py do recibo %s != um.py antes pinado %s" % (str(um_sha)[:16], str(ref_um_py)[:16]))
    rdir = (rj.get("bancada") or {}).get("dir")
    if not isinstance(rdir, str) or not mesmo_no(rdir, bancada):
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: bancada do recibo %r nao e esta Bancada por identidade" % rdir)
    ids = {t.get("id"): t.get("resultado") for t in bat.get("testes") or []}
    for tid in BATERIA_MINIMA:
        if ids.get(tid) != "PASSA":
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: %s=%r na bateria pre-selo (exigido PASSA)" % (tid, ids.get(tid)))
    # N1: o recibo pre-selo R3 traz o kernel da versao anterior (sha da raiz e do Audit; impressao formal), lido do manifesto do
    # kernel pinado pelo selo anterior: e o ANTES que o recibo do kernel da etapa 2 tem de citar
    kern = (rj.get("nos") or {}).get("kernel")
    if not isinstance(kern, dict) or not all(RE_SHA256.match(str(kern.get(c) or "")) for c in ("raiz_sha256", "audit_sha256", "impressao_formal")):
        raise Recusa("RECIBO_PRE_SELO_SEM_KERNEL: o recibo pre-selo R3 traz nos.kernel {raiz_sha256, audit_sha256, impressao_formal}")
    # N2c (R3.1): o selo que o recibo pre-selo leu e o selo pinado no manifesto anterior da Bancada; e o manifesto do kernel que ele leu e
    # o que esse selo pina. Sem isto, um pino forjado em vNNN_pins faria o ANTES do T17 ser o que o forjador quisesse.
    selo_r = (rj.get("nos") or {}).get("selo") or {}
    if not isinstance(selo_r, dict) or str(selo_r.get("sha256") or "").lower() != str(ref_selo or "").lower() or not ref_selo:
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: selo do recibo %s != selo pinado no manifesto anterior da Bancada %s (N2c)"
                     % (str(selo_r.get("sha256") if isinstance(selo_r, dict) else selo_r)[:16], str(ref_selo)[:16]))
    if not _hex64(kern.get("sha256")) or str(kern.get("sha256")).lower() != str(selo_r.get("tgl_kernel_proof_manifest_sha256") or "").lower():
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o manifesto do kernel do recibo %s nao e o que o selo dele pina %s (N2c)"
                     % (str(kern.get("sha256"))[:16], str(selo_r.get("tgl_kernel_proof_manifest_sha256"))[:16]))
    # R31-3 (R3.2): o que esta acima compara o recibo consigo mesmo (a R3.1-5 exagerava). Agora o pino do manifesto do kernel e o que o SELO
    # ANTERIOR grava, lido de --selo-anterior (sha == o selo pinado no manifesto da Bancada) e --kernel-manifesto-anterior (sha == esse pino);
    # raiz, Audit e impressao formal do recibo sao comparados com os RECALCULADOS desse manifesto.
    ext = kernel_do_selo_anterior(selo_anterior, kernel_manifesto_anterior, ref_selo, ref_versao)
    for nome, val, esp in (("nos.kernel.sha256", kern.get("sha256"), ext["pin"]),
                           ("nos.selo.tgl_kernel_proof_manifest_sha256", selo_r.get("tgl_kernel_proof_manifest_sha256"), ext["pin"]),
                           ("nos.kernel.raiz_sha256", kern.get("raiz_sha256"), ext["raiz_sha256"]),
                           ("nos.kernel.audit_sha256", kern.get("audit_sha256"), ext["audit_sha256"]),
                           ("nos.kernel.impressao_formal", kern.get("impressao_formal"), ext["impressao_formal"])):
        if str(val or "").lower() != str(esp).lower():
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: %s do recibo %s != o do manifesto do kernel que o SELO ANTERIOR pina %s (N2c/R31-3: fonte externa ao recibo)"
                         % (nome, str(val)[:16], str(esp)[:16]))
    # e, quando o manifesto da Bancada foi gravado por um B(n) R3.2 (B4 em diante), o pino que ELE registrou tambem confere
    if esp_salto is not None:
        # R3.4 (S): num salto o selo anterior e o do FIM da cadeia; o pino do kernel dele e o do ultimo elo (o do primeiro foi conferido com a Bancada)
        ref_kman = ref_kman_salto
        if ext["pin"] != str(ref_kman).lower():
            raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o selo anterior pina o manifesto do kernel %s e o ultimo elo da cadeia (%s) traz %s (R3.4)"
                         % (ext["pin"][:16], esp_salto["ate"]["versao"], str(ref_kman)[:16]))
    elif ja_sincronizada:
        ref_kman = ((anterior["_man"].get("sincronizacao") or {}).get("anterior") or {}).get("kernel_manifesto_sha256")
    else:
        ref_kman = (anterior["_man"].get("sincronizacao") or {}).get("kernel_manifesto_sha256")
    if ref_kman is not None and str(ref_kman).lower() != ext["pin"]:
        raise Recusa("RECIBO_PRE_SELO_NAO_CORRESPONDE: o manifesto da Bancada registra o manifesto do kernel %s e o selo anterior pina %s (R31-3)"
                     % (str(ref_kman)[:16], ext["pin"][:16]))
    return dict(path=str(rp), sha256=sha256(raw), bytes=len(raw), sha256_esperado=sha_esperado, versao=rj.get("versao_alvo"), veredito=rj.get("veredito"),
                um_py_sha256=um_sha, bancada_dir=rdir, bateria=dict(n=bat.get("n"), passa=bat.get("passa"), falha=bat.get("falha")),
                selo_sha256=selo_r.get("sha256"), selo_cruzado_com_o_manifesto_anterior=True,
                kernel_cruzado_com_o_selo_anterior=dict(selo_anterior=ext["selo_anterior"], kernel_manifesto_anterior=ext["kernel_manifesto_anterior"],
                                                        registrado_no_manifesto_da_bancada=ref_kman),
                kernel_manifesto_anterior_sha256=ext["pin"],
                kernel_anterior=dict(raiz_sha256=kern["raiz_sha256"], audit_sha256=kern["audit_sha256"], impressao_formal=kern["impressao_formal"]),
                salto=esp_salto)   # R3.4 (S): None quando o recibo e o de uma Bancada em dia


# ---------------------------------------------------------------- 4. o manifesto regenerado
def contrato_md(n, versao, nos_info, anterior, evento, stamp, recibo_pre_selo, salto=None):
    base = ("# Contrato de fidelidade da Bancada Um -- B%d / %s (sincronizacao)\n\n"
            "[REAL] Gerado por sincronizar_bancada.py %s em %s UTC, no passo B(%d) da cadeia de selo da %s, sob o evento c1 %s.\n\n"
            "## Identidade pinada\n\n"
            "- um.py %s: sha256 %s (%d B), linha de alpha %d (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = %s.\n"
            "- selo: sha256 %s.\n"
            "- manifesto anterior: %s (sha256 %s).\n"
            "- recibo pre-selo (testes finais contra a versao anterior): sha256 %s.\n\n"
            "## A regra\n\n"
            "Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que\n"
            "o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa\n"
            "sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao\n"
            "com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1\n"
            "nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;\n"
            "nenhum rito move o gate.\n"
            % (n, versao, REVISAO, stamp, n, versao, evento, versao, nos_info["um_py"]["sha256"], nos_info["um_py"]["bytes"], nos_info["alpha"]["linha"],
               nos_info["beta_runtime"], nos_info["selo"]["sha256"], anterior["deployment_id"], anterior["sha256"],
               (recibo_pre_selo or {}).get("sha256") or "(ausente: so em --sandbox)"))
    if salto:
        # R3.4 (S): so quando ha salto; sem salto o texto do contrato e, byte a byte, o da R3.3
        base += ("\n## Salto (R3.4)\n\n"
                 "A Bancada pinava %s e foi levada a %s sem passar pelas versoes puladas %s (nenhuma delas teve elo B(n)). A cadeia de selos (sha256 %s, %d elos) liga,\n"
                 "por hash, o que a Bancada pinava ao Nos que o recibo pre-selo testou (%s): copias de bytes de cada versao, o selo de cada uma pinando o seu um.py e o\n"
                 "seu manifesto do kernel, e o registro do instalador de cada troca com os backups de bytes. Sem cadeia verificavel o salto e recusado.\n"
                 % (salto["de"]["versao"], versao, ", ".join(salto["versoes_puladas"]) or "(nenhuma)", salto["cadeia"]["sha256"], salto["cadeia"]["n_elos"], salto["ate"]["versao"]))
    return base.encode("utf-8")


def regenerar(bancada, anterior, nos_info, versao, evento, script_sha, bateria_sha, modo, forcar, stamp, recibo_pre_selo, reparo, salto=None):
    bancada = Path(bancada)
    man = anterior["_man"]
    m = RE_GERACAO.match(str(man.get("deployment_id") or ""))
    if not m:
        raise Recusa("DEPLOYMENT_ID_SEM_GERACAO: %r" % man.get("deployment_id"))
    n = int(m.group(1)) + 1
    code, sources = [], []
    for e in man["code"]:
        p = relativo_seguro(e["path"], bancada)          # A10: code[].path nunca sai da Bancada
        if not p.is_file():
            raise Recusa("PIN_UNREADABLE: " + str(p))
        b = p.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("CODE_DRIFT_NAO_E_SINCRONIZACAO: " + e["path"])
        code.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b)))
    for e in man["sources"]:
        p = Path(e["path"])
        p = p if p.is_absolute() else relativo_seguro(e["path"], bancada)
        if not p.is_file():
            raise Recusa("PIN_UNREADABLE: " + str(p))
        b = p.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("SOURCE_DRIFT_NAO_E_SINCRONIZACAO: " + e["path"])
        sources.append(dict(e, bytes=len(b), sha256=sha256(b)))
    rotulo = "CONTRATO_CANONICO_B%d.md" % n
    if any(c["path"] == rotulo for c in code):
        raise Recusa("CONTRATO_B%d_JA_PINADO" % n)
    md = contrato_md(n, versao, nos_info, anterior, evento, stamp, recibo_pre_selo, salto)
    code.append(dict(path=rotulo, bytes=len(md), sha256=sha256(md)))
    code.sort(key=lambda c: c["path"])
    novo = dict(schema=1,
                deployment_id="B%d-%s-%s-R1" % (n, versao, stamp[:8]),
                created_utc=agora(),
                canonical=dict(version=versao,
                               script=dict(path=nos_info["um_py"]["path"], bytes=nos_info["um_py"]["bytes"], sha256=nos_info["um_py"]["sha256"]),
                               seal=dict(path=nos_info["selo"]["path"], bytes=nos_info["selo"]["bytes"], sha256=nos_info["selo"]["sha256"])),
                code=code, sources=sources,
                contracts=dict(man.get("contracts") or {},
                               sync_policy="B(n) a cada versao selada por sincronizar_bancada.py: pino velho recusa (PIN_CHANGED); evento c1 nomeado e "
                                           "verificado pela cadeia de hash; bateria pinada antes de gravar; mesma versao com outro hash = SELO_PROGRAMA_DIVERGE; "
                                           "codigo e fontes so mudam por implantacao B com plano proprio"),
                sincronizacao=dict(passo="B%d" % n, versao=versao, modo=modo, forcada=bool(forcar), reparo_de_pino=bool(reparo), revisao_do_esboco=REVISAO,
                                   anterior=dict(deployment_id=anterior["deployment_id"], manifest_sha256=anterior["sha256"],
                                                 version=anterior["version"], um_py_pinado=anterior["um_py_pinado"],
                                                 seal_sha_pinado=anterior["seal_sha_pinado"],
                                                 kernel_manifesto_sha256=(salto["de"]["kernel_manifesto_sha256"] if salto else (recibo_pre_selo or {}).get("kernel_manifesto_anterior_sha256")),   # R31-3 (R3.2); R3.4: no salto, o da Bancada que sai
                                                 estado_do_contrato_instalado=anterior["estado_do_contrato_instalado"]),
                                   evento_c1=evento, selo_sha256=nos_info["selo"]["sha256"], um_py_sha256=nos_info["um_py"]["sha256"],
                                   core_sha256=nos_info["core"]["sha256"], alpha_linha=nos_info["alpha"]["linha"],
                                   beta_runtime=nos_info["beta_runtime"], beta_core=nos_info["core"]["beta_core"],
                                   recibo_pre_selo_sha256=(recibo_pre_selo or {}).get("sha256"),   # A6: o hash do recibo pre-selo fica encadeado no manifesto
                                   gerado_por=dict(script_sha256=script_sha, bateria_sha256=bateria_sha), quando_utc=agora(),
                                   scope="IDENTITY_RE_PIN_ONLY; NOT_A_PHYSICAL_READING", gate_effect="NONE"))
    if salto:
        novo["sincronizacao"]["salto"] = salto   # R3.4 (S): de onde a Bancada saiu, as versoes puladas e a cadeia de selos que as liga (por hash)
    return novo, md, rotulo, n


# ---------------------------------------------------------------- 5. a copia de ensaio (staging) e a re-pinagem
def montar_staging(bancada, man, raiz, novo_manifesto_bytes=None, contrato=None):
    """Copia byte a byte (conferindo os pinos do manifesto dado) o codigo e as fontes RELATIVAS da Bancada para raiz/candidate.
    A10: todo destino e conferido dentro de candidate (sem '..', sem absoluto)."""
    bancada, cand = Path(bancada), Path(raiz) / "candidate"
    if cand.exists():
        raise Recusa("STAGING_JA_EXISTE: " + str(cand))
    cand.mkdir(parents=True)
    copias = []
    for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
        src = relativo_seguro(e["path"], bancada)
        dst = relativo_seguro(e["path"], cand)
        if contrato is not None and e["path"] == contrato[0]:
            b = contrato[1]
        else:
            b = src.read_bytes()
        if len(b) != e["bytes"] or sha256(b) != e["sha256"]:
            raise Recusa("PIN_CHANGED_AO_COPIAR: " + e["path"])
        if dst.exists():
            # o mesmo arquivo pode estar pinado em code E em sources (B2: fontes_externas/F5.2/10_frozen_neff_v1.py): duplicata so com bytes iguais
            if dst.read_bytes() != b:
                raise Recusa("DUPLICATA_COM_BYTES_DIFERENTES: " + e["path"])
            copias.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b), duplicata_de_pino=True))
            continue
        gravar_novo(dst, b)
        copias.append(dict(path=e["path"], bytes=len(b), sha256=sha256(b)))
    (cand / "estado").mkdir(exist_ok=True)
    man_bytes = novo_manifesto_bytes if novo_manifesto_bytes is not None else (bancada / "canonical_contracts.json").read_bytes()
    gravar_novo(cand / "canonical_contracts.json", man_bytes)
    return cand, copias


def conferir_repinagem(canonical_mod, raiz_bancada, nos_info, versao, operacao):
    reg = canonical_mod.CanonicalRegistry(Path(raiz_bancada))
    rc = reg.check(operacao)
    falhas = []
    if not rc.get("ok"):
        falhas.append("ok=false")
    if rc.get("canonical_version") != versao:
        falhas.append("versao %r" % rc.get("canonical_version"))
    if rc.get("um_py_sha256") != nos_info["um_py"]["sha256"]:
        falhas.append("um.py sha")
    if rc.get("seal_sha256") != nos_info["selo"]["sha256"]:
        falhas.append("selo sha")
    if rc.get("beta_tgl") != nos_info["_beta"]:
        falhas.append("beta nao e bit a bit igual: %r vs %r" % (rc.get("beta_tgl"), nos_info["_beta"]))
    if falhas:
        raise Recusa("REPINAGEM_DIVERGE: " + "; ".join(falhas))
    return {k: rc[k] for k in ("ok", "canonical_version", "um_py_sha256", "seal_sha256", "canonical_manifest_sha256", "alpha", "beta_tgl",
                               "deployment_id", "mu_do_rito", "scope", "gate_effect")}


# ---------------------------------------------------------------- 6. a bateria (A1, A3, A7)
def sha_teste(t):
    """sha256 canonico de UM teste da bateria (JSON ordenado), para o pino por teste (A7)."""
    return sha256(json.dumps(t, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def carregar_bateria(bateria_p, bateria_sha_esperado, modo, fase, sandbox):
    """A7: a bateria e pinada pelo sha256 do arquivo (--bateria-sha256, lido pela cadeia de vNNN_pins) e pelo sha256 canonico de
    cada teste (testes_sha256); em aplicar o conjunto minimo e obrigatorio; cada teste (salvo o do kernel) tem fontes pinadas."""
    raw = bateria_p.read_bytes()
    sha_arq = sha256(raw)
    if modo == "aplicar":
        if not bateria_sha_esperado:
            raise Recusa("BATERIA_SHA_AUSENTE: em --modo aplicar a cadeia passa --bateria-sha256 (lido de vNNN_pins)")
    if bateria_sha_esperado and bateria_sha_esperado.lower() != sha_arq:
        raise Recusa("BATERIA_SHA_DIVERGE: arquivo %s != esperado %s" % (sha_arq[:16], str(bateria_sha_esperado)[:16]))
    try:
        bateria = json.loads(raw)
    except ValueError as exc:
        raise Recusa("BATERIA_ILEGIVEL: " + str(exc))
    testes = bateria.get("testes")
    if not isinstance(testes, list) or not testes:
        raise Recusa("BATERIA_SEM_TESTES")
    pinos = bateria.get("testes_sha256")
    if not isinstance(pinos, dict):
        raise Recusa("BATERIA_SEM_PINOS_POR_TESTE: a bateria R2 traz testes_sha256 {id: sha256 canonico}")
    ids = []
    for t in testes:
        tid = t.get("id")
        if not tid or tid in ids:
            raise Recusa("BATERIA_TESTE_SEM_ID_OU_DUPLICADO: %r" % tid)
        ids.append(tid)
        if pinos.get(tid) != sha_teste(t):
            raise Recusa("BATERIA_TESTE_SHA_DIVERGE: %s (%s != %s)" % (tid, sha_teste(t)[:16], str(pinos.get(tid))[:16]))
        if (t.get("verificacao") or {}).get("tipo") != "kernel_recibo" and not t.get("fontes"):
            raise Recusa("BATERIA_TESTE_SEM_FONTE_PINADA: " + tid)
        if "pina_o_um_py" in t and type(t["pina_o_um_py"]) is not bool:
            raise Recusa("BATERIA_TESTE_PINA_O_UM_PY_NAO_BOOLEANO: %s (R3.4: true ou false)" % tid)
        if any("{vinculo}" in str(x) for x in (t.get("comando") or [])) or "{vinculo}" in str(t.get("cwd", "")):
            raise Recusa("MARCADOR_VINCULO_PROIBIDO: %s executa da pasta do esboco, nao da fonte pinada (A3)" % tid)
    if set(pinos) != set(ids):
        raise Recusa("BATERIA_PINOS_NAO_CORRESPONDEM_AOS_TESTES")
    if modo == "aplicar":
        exigidos = set(BATERIA_MINIMA) | (set(BATERIA_MINIMA_POS_SELO) if fase == "pos_selo" else set())
        faltam = sorted(exigidos - set(ids))
        if faltam:
            raise Recusa("BATERIA_MINIMA_AUSENTE: em aplicar faltam %s" % ", ".join(faltam))
    return bateria, raw, sha_arq


def copiar_testes(bateria, raiz):
    raiz = Path(raiz)
    feitas = []
    for c in bateria.get("copias", []):
        b = Path(c["de"]).read_bytes()
        if len(b) != c["bytes"] or sha256(b) != c["sha256"]:
            raise Recusa("FONTE_DA_BATERIA_ALTERADA: " + c["de"])
        dst = relativo_seguro(c["para"], raiz)          # A10: copias[].para nunca sai da raiz
        gravar_novo(dst, b)
        feitas.append(dict(de=c["de"], para=str(dst), sha256=c["sha256"], bytes=c["bytes"]))
    return feitas


def conferir_pinos_da_versao(bateria, nos_info, versao):
    """R3.4 (P): a bateria por versao. Os testes que pinam o um.py (T12/T13/T14 e afins) trazem pina_o_um_py=true e a bateria declara pinos_da_versao {versao,
    um_py_sha256, um_py_bytes, selo_sha256} (gerada por script em cada versao, a partir dos pinos da cadeia); o esboco confere o bloco contra o Nos que ELE leu
    (ler_nos: selo pina o um.py, UM_VERSION confere): pino velho = BATERIA_COM_PINO_VELHO; teste marcado sem bloco = BATERIA_SEM_PINOS_DA_VERSAO. Bateria sem
    teste marcado e sem bloco (a R2) segue aceita como antes; com bloco, o bloco vale. Nunca um sha fixo de uma versao antiga."""
    marcados = [t["id"] for t in bateria["testes"] if t.get("pina_o_um_py") is True]
    pv = bateria.get("pinos_da_versao")
    if pv is None:
        if marcados:
            raise Recusa("BATERIA_SEM_PINOS_DA_VERSAO: os testes %s pinam o um.py (pina_o_um_py) e a bateria nao declara pinos_da_versao (R3.4)" % marcados)
        return dict(declarados=False, testes_que_pinam_o_um_py=[])
    obrig = {"versao", "um_py_sha256", "um_py_bytes", "selo_sha256"}
    if (not isinstance(pv, dict) or not obrig <= set(pv) or not set(pv) <= BATERIA_PINOS_CHAVES or not isinstance(pv["versao"], str) or not RE_VNNN.match(pv["versao"])
            or not isinstance(pv["um_py_sha256"], str) or not _hex64(pv["um_py_sha256"]) or not isinstance(pv["selo_sha256"], str) or not _hex64(pv["selo_sha256"])
            or type(pv["um_py_bytes"]) is not int or pv["um_py_bytes"] <= 0 or ("fonte_dos_pinos" in pv and not isinstance(pv["fonte_dos_pinos"], dict))):
        raise Recusa("BATERIA_PINOS_DA_VERSAO_INVALIDOS: pinos_da_versao exige {versao vNNN, um_py_sha256, um_py_bytes int, selo_sha256} e, opcional, fonte_dos_pinos (objeto): %r" % (pv,))
    esperado = dict(versao=versao, um_py_sha256=nos_info["um_py"]["sha256"], um_py_bytes=nos_info["um_py"]["bytes"], selo_sha256=nos_info["selo"]["sha256"])
    difs = [k for k in esperado if pv[k] != esperado[k]]
    if difs:
        raise Recusa("BATERIA_COM_PINO_VELHO: a bateria foi gerada para %s (um.py %s, %s B, selo %s) e o Nos que o esboco leu e %s (um.py %s, %d B, selo %s): campos %s; "
                     "regenere a bateria para esta versao (gerar_bateria_r3_4.py) e repine (R3.4)"
                     % (pv["versao"], pv["um_py_sha256"][:16], pv["um_py_bytes"], pv["selo_sha256"][:16], esperado["versao"], esperado["um_py_sha256"][:16],
                        esperado["um_py_bytes"], esperado["selo_sha256"][:16], difs))
    return dict(declarados=True, conferidos_contra_o_nos_lido=True, versao=pv["versao"], um_py_sha256=pv["um_py_sha256"], um_py_bytes=pv["um_py_bytes"],
                selo_sha256=pv["selo_sha256"], testes_que_pinam_o_um_py=marcados, fonte_dos_pinos=pv.get("fonte_dos_pinos"))


RE_FONTE = re.compile(r"\{fonte:(\d+)\}")


def _subst(x, ctx, fontes=None):
    if isinstance(x, str):
        if fontes is not None:
            def _f(m):
                i = int(m.group(1))
                if i >= len(fontes):
                    raise Recusa("MARCADOR_FONTE_FORA_DA_LISTA: {fonte:%d}" % i)
                return fontes[i]["path"]
            x = RE_FONTE.sub(_f, x)
        for k, v in ctx.items():
            x = x.replace("{" + k + "}", str(v))
        return x
    if isinstance(x, list):
        return [_subst(i, ctx, fontes) for i in x]
    if isinstance(x, dict):
        return {k: _subst(v, ctx, fontes) for k, v in x.items()}
    return x


VOLATEIS_PADRAO = {"started_utc", "finished_utc", "elapsed_seconds", "environment", "began_utc", "ended_utc", "seconds", "created_utc",
                   "python", "platform", "numpy", "path", "source_snapshot_before", "source_snapshot_after"}


def _strip(o, vol):
    if isinstance(o, dict):
        return {k: _strip(v, vol) for k, v in o.items() if k not in vol}
    if isinstance(o, list):
        return [_strip(x, vol) for x in o]
    return o


def _diff(a, b, path="", acc=None):
    acc = acc if acc is not None else {"max_abs": 0.0, "mismatch": []}
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                acc["mismatch"].append(path + "." + k + " (missing)")
                continue
            _diff(a[k], b[k], path + "." + k, acc)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            acc["mismatch"].append(path + " (len)")
            return acc
        for i, (x, y) in enumerate(zip(a, b)):
            _diff(x, y, path + "[%d]" % i, acc)
    elif isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        d = abs(float(a) - float(b))
        acc["max_abs"] = max(acc["max_abs"], d)
        if d != 0.0:
            acc["mismatch"].append(path + " (num %.3e)" % d)
    elif a != b:
        acc["mismatch"].append(path + " (value)")
    return acc


def verificar(ver, saida_texto, exit_code, ctx):
    """Devolve (passa, detalhe) para as verificacoes que dependem de um subprocesso."""
    t = ver.get("tipo", "exit0")
    if exit_code != 0:
        return False, "exit=%d" % exit_code
    if t == "exit0":
        return True, "exit 0"
    if t == "stdout_regex":
        ok = re.search(ver["regex"], saida_texto) is not None
        return ok, ("regex %r %s" % (ver["regex"], "casou" if ok else "NAO casou"))
    if t == "json_igual":
        p = Path(_subst(ver["arquivo"], ctx))
        if not p.is_file():
            return False, "arquivo ausente: " + str(p)
        d = json.loads(p.read_bytes())
        for campo, valor in ver["campos"].items():
            v = d
            for parte in campo.split("."):
                v = v.get(parte) if isinstance(v, dict) else None
            if v != valor:
                return False, "%s=%r esperado %r" % (campo, v, valor)
        return True, "campos conferem: " + ", ".join("%s=%r" % kv for kv in ver["campos"].items())
    if t == "comparar_json":
        novo, arq = Path(_subst(ver["novo"], ctx)), Path(_subst(ver["arquivado"], ctx))
        if not novo.is_file() or not arq.is_file():
            return False, "arquivo ausente para comparar"
        vol = set(ver.get("volateis") or VOLATEIS_PADRAO)
        d = _diff(_strip(json.loads(novo.read_bytes()), vol), _strip(json.loads(arq.read_bytes()), vol))
        ok = len(d["mismatch"]) == 0
        return ok, "max_abs=%.3e mismatch=%d %s" % (d["max_abs"], len(d["mismatch"]), d["mismatch"][:5])
    return False, "tipo de verificacao desconhecido: " + t


def _hex64(x):
    return isinstance(x, str) and RE_SHA256.match(x.lower()) is not None


def normalizar_log(b):
    """A1b (R3.1): o texto em que sorry, erros e axiomas sao contados. BOM UTF-16 (LE/BE) ou UTF-8 decodificado; sem BOM, UTF-8
    ESTRITO; CRLF e CR sozinho viram LF; sequencias ANSI (CSI, OSC, escapes de 2 caracteres) saem; caractere de controle que
    sobre (o NUL de um UTF-16 sem BOM, um ESC solto) recusa; NFKC e sem caracteres de formato (Cf, ex.: largura zero).
    Devolve (texto, codificacao); recusa com LOG_NAO_DECODIFICA ou LOG_COM_CARACTERE_DE_CONTROLE."""
    if b.startswith(b"\xff\xfe") or b.startswith(b"\xfe\xff"):
        cod = "utf-16"
    elif b.startswith(b"\xef\xbb\xbf"):
        cod = "utf-8-sig"
    else:
        cod = "utf-8"
    try:
        t = b.decode(cod)
    except UnicodeDecodeError as exc:
        raise Recusa("LOG_NAO_DECODIFICA: %s estrito falhou (%s)" % (cod, exc))
    t = t.replace("\r\n", "\n").replace("\r", "\n")
    t = RE_ANSI.sub("", t)
    m = RE_CONTROLE.search(t)
    if m:
        raise Recusa("LOG_COM_CARACTERE_DE_CONTROLE: U+%04X na posicao %d (UTF-16 sem BOM, binario ou escape nao reconhecido)" % (ord(m.group(0)), m.start()))
    t = unicodedata.normalize("NFKC", t)
    t = "".join(c for c in t if unicodedata.category(c) != "Cf")
    return t, cod


def _limpar_forma(t):
    t = unicodedata.normalize("NFKC", t)
    return "".join(c for c in t if unicodedata.category(c) != "Cf")


def formas_de_busca(t):
    """R31-5 (R3.2): as formas do texto normalizado em que sorry e sorryAx sao procurados:
      (1) o texto normalizado (linhas preservadas; e nele que erros e declaracoes do Audit sao contados);
      (2) o mesmo com TODO branco colapsado num espaco (uma quebra entre `declaration` e `uses`, ou entre `uses` e a crase, nao esconde);
      (3) uma copia com os escapes JSON decodificados (\\uXXXX, \\n, \\t, \\", \\\\: a saida do Lean em JSON), normalizada de novo (NFKC,
          sem Cf) e com o branco colapsado. A contagem de sorry e o MAIOR numero de ocorrencias entre as tres."""
    colapsado = RE_BRANCO.sub(" ", t)
    dec = RE_ESCAPE_U.sub(lambda m: chr(int(m.group(1), 16)), t)
    dec = RE_ESCAPE_SIMPLES.sub(lambda m: {"n": " ", "r": " ", "t": " ", "b": " ", "f": " "}.get(m.group(1), m.group(1)), dec)
    dec = RE_BRANCO.sub(" ", _limpar_forma(dec))
    return (t, colapsado, dec)


def contar_sorry(t):
    """R31-5 (R3.2): o maior numero de ocorrencias de RE_LOG_SORRY entre as formas de busca (devolve (n, por_forma))."""
    por = [len(RE_LOG_SORRY.findall(f)) for f in formas_de_busca(t)]
    return max(por), por


def contar_lean_recursivo(arvore):
    """12-ter item 3 (R3.2): os .lean da arvore do build, RECURSIVAMENTE (os.scandir, sem seguir juncao nem link). Devolve
    (n_total, n_em_TGLExt_O16, juncoes_ou_links). Uma juncao ou link dentro da arvore e devolvido para recusa (nunca seguido)."""
    arvore = Path(arvore)
    n, n_o16, links = 0, 0, []
    pilha = [arvore]
    while pilha:
        d = pilha.pop()
        with os.scandir(d) as it:
            for e in it:
                if e.is_junction() or e.is_symlink():
                    links.append(os.path.relpath(e.path, arvore))
                elif e.is_dir(follow_symlinks=False):
                    pilha.append(Path(e.path))
                elif e.is_file(follow_symlinks=False) and e.name.lower().endswith(".lean"):
                    n += 1
                    rel = Path(os.path.relpath(e.path, arvore)).as_posix()
                    if rel.startswith("TGLExt/O16/"):
                        n_o16 += 1
    return n, n_o16, sorted(links)


def _aud_texto(linha, p):
    """R3.5 (M): o literal de texto que comeca em linha[p] == '"'. Escapes admitidos: barra-t, barra-n, barra-barra e barra-aspas. Interpolacao `{x}` so de um LOCAL da lista (o throwError
    interpola `{...}` com termos). Devolve (posicao depois do fecho, motivo|None)."""
    q = p + 1
    barra = chr(92)
    while q < len(linha):
        ch = linha[q]
        if ch == barra:
            if q + 1 >= len(linha) or linha[q + 1] not in ("t", "n", barra, '"'):
                return q, "escape fora da lista no literal de texto"
            q += 2
        elif ch == '"':
            return q + 1, None
        elif ch == "{":
            r = linha.find("}", q)
            if r < 0 or linha[q + 1:r] not in AUD_CORPO_LOCAIS:
                return q, "interpolacao {...} que nao e um local da lista"
            q = r + 1
        elif ch == "}":
            return q, "chave solta no literal de texto"
        else:
            q += 1
    return q, "literal de texto sem fechamento na linha"


def _aud_corpo(linha):
    """R3.5 (M): confere UMA linha do corpo de um run_cmd contra a lista de permissao estrita: palavra, local, funcao global, campo/metodo, nome com crase, numero, literal de texto ou sinal da lista;
    qualquer outra coisa (identificador qualificado fora da lista, `Lean.addDecl`, `writeFile`, `;`, `$`, comentario na linha, caractere nao ASCII fora de texto...) e recusa. Devolve (motivo|None, n_tokens)."""
    p, n, tam = 0, 0, len(linha)
    while p < tam:
        ch = linha[p]
        if ch in " \t":
            p += 1
            continue
        if ch == '"':
            q, mot = _aud_texto(linha, p)
            if mot:
                return "%s (col %d)" % (mot, p + 1), n
            p, n = q, n + 1
            continue
        if ch == "`":
            m = RE_AUD_TOK_NOME.match(linha, p)
            if not m:
                return "nome com crase mal formado (col %d)" % (p + 1), n
            nome = m.group(0)[1:]
            if nome not in AUD_CORPO_NOMES and nome.split(".")[0] not in AUD_CORPO_PREFIXOS_DE_NOME:
                return "nome com crase fora da lista: %r (col %d)" % (nome, p + 1), n
            p, n = m.end(), n + 1
            continue
        m = RE_AUD_TOK_NUM.match(linha, p)
        if m:
            p, n = m.end(), n + 1
            continue
        m = RE_AUD_TOK_ID.match(linha, p)
        if m:
            tok = m.group(0)
            partes = tok.split(".")
            if tok in AUD_CORPO_PALAVRAS or tok in AUD_CORPO_GLOBAIS or (partes[0] in AUD_CORPO_LOCAIS and all(x in AUD_CORPO_METODOS for x in partes[1:])):
                p, n = m.end(), n + 1
                continue
            return "identificador fora da lista de permissao: %r (col %d)" % (tok, p + 1), n
        m = RE_AUD_TOK_CAMPO.match(linha, p)
        if m:
            if m.group(0)[1:] in AUD_CORPO_METODOS:
                p, n = m.end(), n + 1
                continue
            return "campo fora da lista de permissao: %r (col %d)" % (m.group(0), p + 1), n
        for sinal in AUD_CORPO_PONTUACAO:
            if linha.startswith(sinal, p):
                p, n = p + len(sinal), n + 1
                break
        else:
            return "caractere fora da lista de permissao: %r (col %d)" % (ch, p + 1), n
    return None, n


def auditar_fonte_de_auditoria(texto):
    """R3.5 (M): a fonte de um modulo de auditoria (listado em modulos_de_auditoria do recibo do kernel) so pode ter comandos de auditoria, por LISTA DE PERMISSAO ESTRITA: `import` so de Lean/TGLExt/TGL,
    `open` so de Lean, `#print axioms X`, `run_cmd` (com o corpo indentado, conferido token a token contra o vocabulario fechado AUD_CORPO_*). Linha de topo de outra forma, indentada fora de um corpo de
    run_cmd, comentario de bloco, caractere de controle ou de formato, ou, no corpo, qualquer token fora da lista (qualificado ou nao): recusa. Exige ao menos um #print ou run_cmd (um modulo listado que
    nao audita nada e recusado). Devolve dict(ok, motivo, contagem). O corpo do run_cmd e codigo executado na compilacao: este script confere a FORMA (comandos de topo e vocabulario fechado); NAO prova a
    inocuidade semantica do corpo (residuo declarado)."""
    cont = dict(import_=0, open_=0, print_axioms=0, run_cmd=0, corpo=0, comentario=0, branco=0, tokens=0)
    for ch in texto:
        cat = unicodedata.category(ch)
        if (cat == "Cc" and ch not in "\n\r\t") or cat == "Cf":
            return dict(ok=False, motivo="caractere de controle ou de formato U+%04X" % ord(ch), contagem=cont)
    if "/-" in texto:
        return dict(ok=False, motivo="comentario de bloco (/-) nao se admite", contagem=cont)
    corpo = False
    for i, linha in enumerate(texto.replace("\r\n", "\n").replace("\r", "\n").split("\n"), 1):
        l_ = linha.rstrip(" \t")
        if not l_.strip():
            cont["branco"] += 1
            continue
        if l_.lstrip().startswith("--"):
            cont["comentario"] += 1
            continue
        if l_[0] in " \t":
            if not corpo:
                return dict(ok=False, motivo="l.%d: linha indentada fora de um corpo de run_cmd: %r" % (i, l_[:60]), contagem=cont)
            mot, nt = _aud_corpo(l_)
            if mot:
                return dict(ok=False, motivo="l.%d: palavra proibida no corpo do run_cmd (fora da lista de permissao estrita, R3.5): %s" % (i, mot), contagem=cont)
            cont["corpo"] += 1
            cont["tokens"] += nt
            continue
        corpo = False
        if RE_AUD_IMPORT.match(l_):
            cont["import_"] += 1
        elif RE_AUD_OPEN.match(l_):
            nomes = l_.split()[1:]
            if nomes and nomes[-1] == "in":
                nomes = nomes[:-1]
            if not nomes or any(x not in AUD_OPEN_PERMITIDOS for x in nomes):
                return dict(ok=False, motivo="l.%d: open fora da lista de permissao estrita (so %s): %r" % (i, ", ".join(sorted(AUD_OPEN_PERMITIDOS)), l_[:60]), contagem=cont)
            cont["open_"] += 1
        elif RE_AUD_PRINT.match(l_):
            cont["print_axioms"] += 1
        elif RE_AUD_RUNCMD.match(l_):
            cont["run_cmd"] += 1
            corpo = True
        else:
            return dict(ok=False, motivo="l.%d: comando de topo fora da lista (import de Lean/TGLExt/TGL, open de Lean, #print axioms, run_cmd): %r" % (i, l_[:60]), contagem=cont)
    if cont["print_axioms"] + cont["run_cmd"] == 0:
        return dict(ok=False, motivo="nenhum #print axioms nem run_cmd: o modulo listado nao audita nada", contagem=cont)
    return dict(ok=True, motivo=None, contagem=cont)


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
        c = json_estrito(raw)
    except ChaveDuplicada as exc:
        # R31-6 (R3.2): o json.loads ficaria com o ULTIMO valor; um revisor humano do arquivo pinado le o primeiro
        raise Recusa("CRITERIOS_CHAVE_DUPLICADA: %s (R31-6: o arquivo pinado nao pode dizer duas coisas)" % exc)
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


def verificar_kernel_recibo(kp, versao, nos_info, sha_esperado=None, recibo_pre_selo=None, sandbox=False, criterios=None):
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
        k = json_estrito(raw)
    except ChaveDuplicada as exc:
        return falha("KERNEL_RECIBO_CHAVE_DUPLICADA: %s (R31-6)" % exc)
    except ValueError as exc:
        return falha("ilegivel: %s" % exc)
    if not isinstance(k, dict):
        return falha("nao e um objeto JSON")
    if k.get("contrato") not in KERNEL_CONTRATOS_ADMITIDOS:
        return falha("contrato=%r (exigido %s; a %s segue admitida)" % (k.get("contrato"), KERNEL_CONTRATO, KERNEL_CONTRATO_R3_2))
    proibidos = [c for c in KERNEL_CAMPOS_PROIBIDOS if c in k]
    if proibidos:
        return falha("campos PROIBIDOS %s: a etapa 2 roda antes do candidato e do rito e nao pode conhece-los" % proibidos)
    exigidos = ("versao", "rc", "sorry", "erros", "build_full_log", "audit_log", "toolchain", "arvore", "raiz", "audit", "pedras", "axiomas",
                "criterios", "nos_kernel_impressao", "formal_files_antes", "varredura_tokens")
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
    # R31-5 (R3.2): sorry contado no texto normalizado, no texto com o branco colapsado e na copia com os escapes JSON decodificados
    sorry_por_log = {campo: contar_sorry(t) for campo, t in logs.items()}
    n_sorry = sum(n for n, _ in sorry_por_log.values())
    n_erros = sum(len(RE_LOG_ERRO.findall(t)) for t in logs.values())
    if n_sorry != k["sorry"]:
        return falha("os logs tem %d ocorrencia(s) de sorry (contadas por script, crase e aspas, tambem com o branco colapsado e os escapes JSON "
                     "decodificados: %s) e o recibo declara %d" % (n_sorry, {c: p for c, (_, p) in sorry_por_log.items()}, k["sorry"]))
    if n_erros != k["erros"]:
        return falha("os logs tem %d linha(s) de erro (contadas por script) e o recibo declara %d" % (n_erros, k["erros"]))
    ax_log, n_ax = set(), 0
    for m in RE_LOG_AXIOMAS.finditer(logs["audit_log"]):
        n_ax += 1
        ax_log |= {a.strip() for a in m.group(1).split(",") if a.strip()}
    # R31-5 (R3.2): as listas de axiomas tambem nas outras formas (escape JSON, quebras): sorryAx ou axioma proprio ali tambem recusa
    for forma in formas_de_busca(logs["audit_log"])[1:]:
        for m in RE_LOG_AXIOMAS.finditer(forma):
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
    # R3.4 (M): os modulos de auditoria (so run_cmd/#print/import) sao listados pelo recibo, no contrato R3_4, e tem de ser pedras do recibo
    aud = k.get("modulos_de_auditoria")
    aud_set, auditorias = set(), {}
    if aud is not None:
        if k["contrato"] != KERNEL_CONTRATO:
            return falha("modulos_de_auditoria so existe no contrato %s (o recibo e %s) (R3.4)" % (KERNEL_CONTRATO, k["contrato"]))
        if not lista_de_texto(aud) or len(set(aud)) != len(aud):
            return falha("MODULOS_DE_AUDITORIA_INVALIDOS: modulos_de_auditoria exige lista nao vazia de caminhos de pedras, sem repeticao (R3.4)")
        fora_das_pedras = sorted(set(aud) - vistos)
        if fora_das_pedras:
            return falha("MODULO_DE_AUDITORIA_FORA_DAS_PEDRAS: %s nao e pedra do recibo (R3.4)" % fora_das_pedras[:3])
        aud_set = set(aud)
    # R31-6 (R3.2): a decisao X19 do CRITERIOS pinado cruzada com as pedras do recibo: "sim" <=> a pedra LightNetStandardWedgeDataBGL.lean
    x19 = criterios.get("x19")
    tem_x19 = sorted(c for c in vistos if Path(c).name == X19_PEDRA)
    if x19 not in CRITERIOS_X19:
        return falha("X19_NAO_CONFERE_COM_AS_PEDRAS: x19=%r no CRITERIOS (exigido 'sim' ou 'nao')" % (x19,))
    if x19 == "sim" and not tem_x19:
        return falha("X19_NAO_CONFERE_COM_AS_PEDRAS: o CRITERIOS pinado diz x19='sim' e nenhuma pedra do recibo e %s (R31-6)" % X19_PEDRA)
    if x19 == "nao" and tem_x19:
        return falha("X19_NAO_CONFERE_COM_AS_PEDRAS: o CRITERIOS pinado diz x19='nao' e o recibo traz a pedra %s (R31-6)" % tem_x19)
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
    # R31-4 (R3.2): o build log tem de ser o de um lake build que compilou as pedras: uma linha de job do lake (Built/Replayed) para cada pedra
    # listada, para a raiz (TGLExt) e para o Audit (TGL.Audit), e a linha final "Build completed successfully"
    jobs = set(RE_LAKE_JOB.findall(logs["build_full_log"]))
    exig_mod = ["TGLExt", "TGL.Audit"] + [p["path"][:-len(".lean")].replace("/", ".") for p in pedras]
    sem_job = [m_ for m_ in exig_mod if m_ not in jobs]
    if sem_job:
        return falha("LOG_DE_BUILD_IMPLAUSIVEL: o build log nao tem a linha de job do lake (Built/Replayed) de %s (R31-4: exigida para cada pedra, a raiz e o Audit; "
                     "%d linha(s) de job no log)" % (sem_job[:5], len(jobs)))
    if not RE_LAKE_FIM.search(logs["build_full_log"]):
        return falha("LOG_DE_BUILD_IMPLAUSIVEL: o build log nao tem a linha final 'Build completed successfully' do lake (R31-4)")
    # 12-ter item 3 (R3.2): a varredura de tokens proibidos foi RECURSIVA (inclui TGLExt/O16): o recibo diz quantos .lean varreu e o B(n) reconta
    vt = k["varredura_tokens"]
    if not isinstance(vt, dict) or vt.get("recursiva") is not True or type(vt.get("arquivos_lean")) is not int or type(vt.get("arquivos_lean_em_TGLExt_O16")) is not int:
        return falha("TOKENS_VARREDURA_NAO_RECURSIVA: varredura_tokens exige {recursiva: true, arquivos_lean: int, arquivos_lean_em_TGLExt_O16: int} (plano 12-ter item 3): %r" % (vt,))
    n_lean, n_o16, links = contar_lean_recursivo(arvore)
    if links:
        return falha("ARVORE_COM_JUNCAO_OU_LINK: %s (a arvore do build nao pode ter juncao nem link: a varredura nao os segue)" % links[:5])
    if vt["arquivos_lean"] != n_lean or vt["arquivos_lean_em_TGLExt_O16"] != n_o16:
        return falha("TOKENS_VARREDURA_NAO_RECURSIVA: o recibo diz %d .lean (%d em TGLExt/O16) e a arvore tem %d (%d em TGLExt/O16), contados recursivamente pelo B(n) "
                     "(plano 12-ter item 3)" % (vt["arquivos_lean"], vt["arquivos_lean_em_TGLExt_O16"], n_lean, n_o16))
    # A2 (R3.1) + R31-4 (R3.2): o log do Audit tem de cobrir os #print axioms do Audit.lean PINADO (o sha ja conferido acima) por NOME de declaracao
    # distinto: linhas repetidas nao contam duas vezes, e todo nome impresso pelo Audit.lean aparece no log
    n_print = len(RE_PRINT_AXIOMS.findall(fontes["TGL/Audit.lean"]))
    if n_print == 0:
        return falha("o Audit.lean pinado nao tem nenhum #print axioms")
    nomes_print = {x.lstrip("@") for x in RE_PRINT_AXIOMS_NOME.findall(fontes["TGL/Audit.lean"])}
    decl_log_n = {x.lstrip("@") for x in decl_log}
    if len(decl_log_n) < len(nomes_print):
        return falha("o log do Audit tem %d declaracao(oes) DISTINTA(S) (%d linha(s) de axiomas) e o Audit.lean pinado tem %d #print axioms distintos (A2/R31-4: "
                     "LOG_DO_AUDIT_CURTO; truncado, repetido ou de outro Audit)" % (len(decl_log_n), n_ax + n_sem_ax, len(nomes_print)))
    faltam_no_log = sorted(nomes_print - decl_log_n)
    if faltam_no_log:
        return falha("LOG_DO_AUDIT_CURTO: %d declaracao(oes) do #print axioms do Audit.lean pinado nao aparece(m) no log do Audit (ex.: %s) (R31-4)"
                     % (len(faltam_no_log), faltam_no_log[:3]))
    # N1k (R3.1): cada declaracao de cada pedra tem entrada no axiom_report, linha no log do Audit e nome na fonte da pedra
    n_decl = 0
    for p in pedras:
        dl = p.get("declaracoes")
        if p["path"] in aud_set:
            # R3.4 (M): o modulo de auditoria nao tem declaracoes (se as tivesse, seria pedra comum: ambiguidade recusada); a fonte so tem comandos de auditoria
            if dl not in (None, []):
                return falha("MODULO_DE_AUDITORIA_COM_DECLARACOES: %s esta em modulos_de_auditoria e traz declaracoes %s; um modulo de auditoria nao declara nada (R3.4)" % (p["path"], dl))
            av = auditar_fonte_de_auditoria(fontes[p["path"]])
            if not av["ok"]:
                return falha("MODULO_DE_AUDITORIA_FORA_DA_LISTA_DE_COMANDOS: %s: %s (R3.4)" % (p["path"], av["motivo"]))
            auditorias[p["path"]] = av["contagem"]
            continue
        if not lista_de_texto(dl) or len(set(dl)) != len(dl):
            return falha("pedra %s exige declaracoes: lista nao vazia e sem repeticao dos nomes que o Audit imprime (N1k)" % p["path"])
        for d in dl:
            if d not in ar:
                return falha("pedra %s: a declaracao %s nao tem entrada no axiom_report do manifesto pinado pelo selo (N1k)" % (p["path"], d))
            if d not in decl_log:
                return falha("pedra %s: a declaracao %s nao foi impressa no log do Audit (N1k)" % (p["path"], d))
            curto = d.split(".")[-1].strip("\u00ab\u00bb")
            if not curto or not re.search(r"(?<![\w'.])" + re.escape(curto) + r"(?![\w'])", fontes[p["path"]]):
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
    pino.update(contrato=k["contrato"], logs=dict(sorry_contados=n_sorry, erros_contados=n_erros, linhas_de_axiomas=n_ax + n_sem_ax,
                                                     print_axioms_no_audit_pinado=n_print, axiomas_no_log=sorted(ax_log), codificacao=codif,
                                                     print_axioms_distintos_no_audit_pinado=len(nomes_print), declaracoes_distintas_no_log=len(decl_log_n),
                                                     sorry_por_forma={c: p_ for c, (_, p_) in sorry_por_log.items()},
                                                     formas_de_busca="normalizado; branco colapsado; escapes JSON decodificados (R31-5)",
                                                     jobs_do_lake_no_build_log=len(jobs), modulos_exigidos_no_build_log=exig_mod,
                                                     normalizacao="BOM UTF-16/UTF-8; UTF-8 estrito; CR -> LF; sem ANSI; sem controle; NFKC; sem Cf"),
                varredura_tokens=dict(recursiva=True, arquivos_lean=n_lean, arquivos_lean_em_TGLExt_O16=n_o16, recontado_pelo_bn=True),
                manifesto_do_kernel=dict(sha256=kinfo.get("sha256"), statuses_exigidos=list(KERNEL_STATUSES_EXIGIDOS), toolchain=dict(lean_version=mlv, lake_version=mkv)),
                n_pedras=len(pedras), n_declaracoes_das_pedras=n_decl, pedras_cobrem_o_diff_formal=True,
                modulos_de_auditoria=dict(lista=sorted(aud_set), n=len(aud_set), fontes_conferidas_por_script=True, contagem_de_comandos=auditorias,
                                          limite="o corpo do run_cmd e codigo executado na compilacao: o script confere os comandos de topo e um vocabulario FECHADO de permissao no corpo (R3.5); nao prova a inocuidade semantica do corpo"),
                criterios=dict(path=criterios.get("path"), sha256=criterios.get("sha256"), x19=criterios.get("x19")),
                antes=nota_antes or "cruzado com o recibo pre-selo")
    return True, "recibo do kernel %s (%s): versao=%s rc=0 sorry=0 erros=0 (recontados nos logs normalizados); %d pedras (%d declaracoes no axiom_report, no log e na fonte; %d modulo(s) de auditoria sem declaracoes, fonte conferida por script) + raiz + Audit == manifesto do kernel %s pinado pelo selo e re-hasheados; pedras == diff formal; build log com os jobs do lake das pedras, da raiz e do Audit; log do Audit cobre os %d #print axioms distintos por nome; varredura de tokens recursiva (%d .lean, %d em TGLExt/O16) recontada; criterios == CRITERIOS %s (x19=%s, cruzada com as pedras); statuses e axiomas no trio; %s" % (
        pino["sha256"][:16], k["contrato"], versao, len(pedras) - len(aud_set), n_decl, len(aud_set), str(kinfo.get("sha256"))[:16], len(nomes_print), n_lean, n_o16, str(criterios.get("sha256"))[:16],
        criterios.get("x19"), pino["antes"]), pino


def _arquivo_executado_e_pinado(arg, fontes_ok, candidate, copias_dst):
    """A3: todo .py que o comando executa ou passa como script tem de ser (a) uma fonte pinada deste teste (mesmo arquivo por
    identidade) ou (b) um arquivo da copia de ensaio (candidate, conferido pino a pino) ou uma copia conferida da bateria.
    R3: argumento relativo nao e admitido (o cwd e uma pasta vazia nova)."""
    p = Path(arg)
    if not p.is_absolute():
        return False
    try:
        pc = caminho_canonico(p)
    except Recusa:
        return False
    for f in fontes_ok:
        if mesmo_no(pc, f["path"]):
            return True
    if dentro_de(pc, candidate):
        return True
    for d in copias_dst:
        if mesmo_no(pc, d):
            return True
    return False


def montar_comando(cmd_bat, ctx, fontes, copias_dst):
    """N16: a gramatica FECHADA: ["{py}", opcoes de OPCOES_PY_ADMITIDAS/OPCOES_PY_COM_VALOR, <script .py absoluto e pinado>, args...].
    -c, -m, -I, -S, zip, pasta com __main__ e .py relativo sao recusados. N5: o esboco poe FLAGS_ISOLAMENTO (-E -P) logo depois do
    interpretador. Devolve (comando da bateria substituido, comando executado, script)."""
    if not isinstance(cmd_bat, list) or not cmd_bat or cmd_bat[0] != "{py}":
        raise Recusa("COMANDO_FORMA_NAO_ADMITIDA: o comando tem de comecar por {py}")
    sub = [str(x) for x in _subst(cmd_bat, ctx, fontes)]
    i, opts = 1, []
    while i < len(sub) and sub[i].startswith("-"):
        o = sub[i]
        if o in OPCOES_PY_ADMITIDAS:
            opts.append(o)
            i += 1
        elif o in OPCOES_PY_COM_VALOR and i + 1 < len(sub) and sub[i + 1] in OPCOES_PY_COM_VALOR[o]:
            opts += [o, sub[i + 1]]
            i += 2
        else:
            raise Recusa("COMANDO_FORMA_NAO_ADMITIDA: opcao %r (so -B e -X utf8; -c, -m, -I, -S e as demais sao recusadas)" % o)
    if i >= len(sub):
        raise Recusa("COMANDO_FORMA_NAO_ADMITIDA: sem script")
    script = sub[i]
    if not script.lower().endswith(".py"):
        raise Recusa("COMANDO_FORMA_NAO_ADMITIDA: o alvo %r nao e um .py (zip, pasta com __main__ e modulo sao recusados)" % script)
    sp = Path(script)
    if not sp.is_absolute() or not sp.is_file():
        raise Recusa("COMANDO_EXECUTA_ARQUIVO_NAO_PINADO: %r nao e arquivo absoluto existente" % script)
    nao_pinados = [a for a in [script] + [x for x in sub[i + 1:] if x.lower().endswith(".py")]
                   if _arquivo_executado_e_pinado(a, fontes, ctx["candidate"], copias_dst) is not True]
    if nao_pinados:
        raise Recusa("COMANDO_EXECUTA_ARQUIVO_NAO_PINADO: %s" % nao_pinados)
    # A4 (R3.1): o filho roda o LANCADOR pinado (sha no recibo), que poe o site do usuario como caminho e executa o script pinado
    if not ctx.get("_lancador"):
        raise Recusa("LANCADOR_AUSENTE: o isolamento A4 nao foi preparado")
    final = [sys.executable, *FLAGS_ISOLAMENTO, *opts, str(ctx["_lancador"]), str(ctx.get("_site_usuario") or "-"), script, *sub[i + 1:]]
    return sub, final, sp


_SOMBREAVEIS = None


def sombreaveis():
    """N5: os nomes de modulo que um arquivo ao lado de uma fonte pinada SOMBREARIA: a biblioteca padrao, os embutidos,
    sitecustomize/usercustomize e os modulos de topo dos site-packages (sistema e usuario), listados SEM importar nada."""
    global _SOMBREAVEIS
    if _SOMBREAVEIS is None:
        nomes = set(sys.stdlib_module_names) | set(sys.builtin_module_names) | {"sitecustomize", "usercustomize", "__main__"}
        dirs = list(site.getsitepackages()) if hasattr(site, "getsitepackages") else []
        # R3.2: sob -I o site.ENABLE_USER_SITE e False no processo do esboco, mas os testes RECEBEM o site do usuario (pelo lancador, como
        # caminho): os modulos dele continuam sombreaveis. Entram o site achado pela pasta conhecida do Windows e o do APPDATA herdado.
        # (Achado pelo controle N5_modulo_sombra_ao_lado_da_fonte na 1a rodada da R3.2: o numpy.py ao lado da fonte deixara de ser visto.)
        try:
            su_real = site_do_usuario_real()
            if su_real:
                dirs.append(su_real)
        except Exception:
            pass
        try:
            dirs.append(site.getusersitepackages())
        except Exception:
            pass
        for d in dirs:
            if os.path.isdir(d):
                nomes |= {m.name for m in pkgutil.iter_modules([d])}
        _SOMBREAVEIS = frozenset(nomes)
    return _SOMBREAVEIS


def _nome_de_modulo(entry):
    nome = entry.name
    try:
        if entry.is_symlink() or entry.is_junction():
            return nome.split(".")[0]
        if entry.is_dir(follow_symlinks=False):
            return nome if any(os.path.exists(os.path.join(entry.path, "__init__" + s)) for s in SUFIXOS_IMPORTAVEIS) else None
    except OSError:
        return nome.split(".")[0]
    for s in SUFIXOS_IMPORTAVEIS:
        if nome.lower().endswith(s.lower()):
            return nome[:-len(s)].split(".")[0]
    return None


def modulos_sombra(dirs, admitidos):
    """N5: arquivos ou pacotes ao lado de fonte pinada (ou do script executado) cujo nome de modulo sombreia a biblioteca padrao ou
    um site-packages, e que nao sao eles mesmos fonte pinada nem copia conferida."""
    achados, nomes = [], sombreaveis()
    for d in sorted({str(x) for x in dirs}):
        if not os.path.isdir(d):
            continue
        with os.scandir(d) as it:
            for e in it:
                mod = _nome_de_modulo(e)
                if mod and mod in nomes and not any(mesmo_no(e.path, a) for a in admitidos):
                    achados.append(e.path)
    return achados


def ambiente_limpo(appdata=None, site_usuario=None):
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
        esboco="R3.2 (R31-1): o esboco so roda com python -I -B -X utf8 (sem -I recusa INTERPRETADOR_NAO_ISOLADO antes de qualquer import); o site do "
               "usuario dele nao e processado e a pasta dele nao entra no sys.path. Sem -I, o que o interpretador executa ANTES da 1a linha (um usercustomize "
               "ou .pth do APPDATA herdado) ainda roda: e residuo da chamada errada, que recusa sem gravar")
    return info, str(lanc), su


def rodar_bateria(bateria, ctx, recibos_dir, modo, fase="pos_selo", sandbox=False, recibo_pre_selo=None, nos_info=None, copias_feitas=(), criterios=None):
    recibos_dir = Path(recibos_dir)
    recibos_dir.mkdir(parents=True, exist_ok=True)
    copias_dst = [c["para"] for c in copias_feitas]
    resultados = []
    iso = None   # A4: preparado so quando o primeiro teste com subprocesso vai rodar
    for t in bateria["testes"]:
        tid = t["id"]
        rec = dict(id=tid, teste=t.get("teste"), sha256_do_teste=sha_teste(t), fases=t.get("fases", ["pre_selo", "pos_selo"]),
                   obrigatorio_em=t.get("obrigatorio_em", ["ensaio", "aplicar"]), fontes=[], inicio=agora())
        if fase not in rec["fases"]:
            # o teste pertence a outra fase (ex.: os runners do atrator pinam o um.py ANTERIOR e so rodam antes do selo):
            # na fase pos_selo ele e lido do recibo da fase pre_selo, por hash, nunca refeito
            if fase == "pos_selo" and "pre_selo" in rec["fases"]:
                det = "nao pertence a fase pos_selo; o resultado vale pelo recibo pre-selo %s" % ((recibo_pre_selo or {}).get("sha256") or "(ausente)")
            else:
                det = "nao pertence a fase %s (fases: %s)" % (fase, rec["fases"])
            rec.update(resultado="NAO_EXECUTADO", detalhe=det, fim=agora())
            resultados.append(rec)
            continue
        # A3: as fontes PINADAS sao conferidas por sha256 ANTES de executar; o comando executa a fonte pinada, nunca uma copia local
        fontes_ok = True
        for f in t.get("fontes", []):
            p = Path(f["path"])
            if not p.is_absolute():
                rec["fontes"].append(dict(f, estado="NAO_ABSOLUTA"))
                fontes_ok = False
                continue
            if not p.is_file():
                rec["fontes"].append(dict(f, estado="AUSENTE"))
                fontes_ok = False
                continue
            b = p.read_bytes()
            est = "OK" if (len(b) == f["bytes"] and sha256(b) == f["sha256"]) else "ALTERADA"
            fontes_ok = fontes_ok and est == "OK"
            rec["fontes"].append(dict(f, estado=est))
        if not fontes_ok:
            rec.update(resultado="FALHA", detalhe="fonte pinada ausente, nao absoluta ou alterada", fim=agora())
            resultados.append(rec)
            continue
        ver = t.get("verificacao", {"tipo": "exit0"})
        if ver.get("tipo") == "kernel_recibo":
            # A1/N1: sem subprocesso; o recibo do build e lido por hash e VINCULADO ao manifesto do kernel pinado pelo selo
            kp = ctx.get("kernel_recibo")
            if not kp:
                exig = (modo in rec["obrigatorio_em"]) and not sandbox
                rec.update(resultado=("FALHA" if exig else "NAO_EXECUTADO"),
                           detalhe="sem --kernel-recibo (T17 e lido do recibo do build do kernel da etapa 2 da cadeia)" + ("; tolerado so em --sandbox" if sandbox else ""), fim=agora())
            else:
                passa, detalhe, pino = verificar_kernel_recibo(kp, ctx["versao"], nos_info, ctx.get("kernel_recibo_sha256") or None,
                                                               recibo_pre_selo, sandbox, criterios)
                rec.update(kernel_recibo=pino, resultado=("PASSA" if passa else "FALHA"), detalhe=limpar(detalhe), comando=None, fim=agora())
            resultados.append(rec)
            continue
        fontes_pin = t.get("fontes", [])
        if iso is None:
            iso, ctx["_lancador"], ctx["_site_usuario"] = preparar_isolamento(ctx["saida"])
        # N16: gramatica fechada; N5: -E -P na frente, ambiente sem PYTHON*, cwd numa pasta vazia nova, sem modulo-sombra; A4: -s e lancador
        try:
            sub, final, script = montar_comando(t.get("comando"), ctx, fontes_pin, copias_dst)
        except Recusa as exc:
            rec.update(resultado="FALHA", detalhe=limpar(str(exc)), comando=t.get("comando"), fim=agora())
            resultados.append(rec)
            continue
        rec["comando"] = sub
        rec["cwd_declarado"] = _subst(t.get("cwd", "{raiz}"), ctx, fontes_pin)
        dirs_vizinhas = {script.parent} | {Path(f["path"]).parent for f in fontes_pin if str(f["path"]).lower().endswith(".py")}
        admitidos = [f["path"] for f in fontes_pin] + list(copias_dst) + [str(script)]
        sombra = modulos_sombra(dirs_vizinhas, admitidos)
        if sombra:
            rec.update(resultado="FALHA", detalhe=limpar("SOMBRA_DE_MODULO_AO_LADO_DA_FONTE: %s (nada executado)" % sombra), fim=agora())
            resultados.append(rec)
            continue
        cwd = Path(ctx["saida"]) / "cwd_testes" / tid
        try:
            cwd.mkdir(parents=True, exist_ok=False)
        except OSError as exc:
            rec.update(resultado="FALHA", detalhe="CWD_NAO_E_PASTA_NOVA: %s" % exc, fim=agora())
            resultados.append(rec)
            continue
        if any(cwd.iterdir()):
            rec.update(resultado="FALHA", detalhe="CWD_NAO_VAZIO: %s" % cwd, fim=agora())
            resultados.append(rec)
            continue
        rec["cwd"] = str(cwd)
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
        rec["comando_executado"] = final          # so existe quando o subprocesso de fato roda
        t0 = time.perf_counter()
        try:
            r = subprocess.run(final, cwd=str(cwd), capture_output=True, text=True, encoding="utf-8", errors="replace",
                               timeout=float(t.get("timeout_s", 900)), env=ambiente_limpo(appdata, ctx["_site_usuario"]))
            exit_code, out = r.returncode, (r.stdout or "") + "\n--- STDERR ---\n" + (r.stderr or "")
        except subprocess.TimeoutExpired as exc:
            exit_code, out = -1, "TIMEOUT apos %.0f s\n%s\n%s" % (float(t.get("timeout_s", 900)), exc.stdout or "", exc.stderr or "")
        except OSError as exc:
            exit_code, out = -2, "FALHA AO LANCAR: %s" % exc
        rec["segundos"] = round(time.perf_counter() - t0, 3)
        # N14: a guarda de palavra vem ANTES de gravar o log: com a palavra, o log em disco e suprimido (so o sha do texto original)
        palavra = contem_palavra(out)
        log = recibos_dir / (tid + ".log")
        if palavra:
            corpo = "COMMAND: %r\nCWD: %s\nEXIT: %d\n<SAIDA_SUPRIMIDA: palavra guardada na saida do teste; %d caracteres; sha256 %s>\n" % (
                final, cwd, exit_code, len(out), sha256(out.encode("utf-8")))
        else:
            corpo = "COMMAND: %r\nCWD: %s\nEXIT: %d\n%s" % (final, cwd, exit_code, out)
        gravar_novo(log, corpo.encode("utf-8"))
        rec["log"] = dict(path=str(log), sha256=sha256(log.read_bytes()), bytes=log.stat().st_size, suprimido=palavra)
        rec["exit"] = exit_code
        passa, detalhe = verificar(ver, out, exit_code, ctx)
        rec["detalhe"] = limpar(detalhe)
        rec["resultado"] = "PASSA" if passa else "FALHA"
        if palavra:
            rec["resultado"], rec["detalhe"] = "FALHA", "palavra proibida na saida do teste (log suprimido); " + limpar(detalhe)
        rec["fim"] = agora()
        resultados.append(rec)
    n_passa = sum(1 for r in resultados if r["resultado"] == "PASSA")
    n_falha = sum(1 for r in resultados if r["resultado"] == "FALHA")
    n_nexec = sum(1 for r in resultados if r["resultado"] == "NAO_EXECUTADO")
    return dict(n=len(resultados), passa=n_passa, falha=n_falha, nao_executado=n_nexec, testes=resultados,
                veredito=("BATERIA_PASSA" if n_falha == 0 else "BATERIA_FALHOU"),
                isolamento=dict(flags=list(FLAGS_ISOLAMENTO), ambiente="sem PYTHON* herdado; APPDATA vazio por teste; PYTHONNOUSERSITE=1 e PYTHONPATH=site do usuario nos netos",
                                cwd="pasta vazia nova por teste", sombra="modulo-sombra ao lado de fonte pinada = FALHA",
                                preparado=iso,
                                limite="A4 [residuo declarado]: o site do usuario entra como caminho (numpy/scipy/torch vivem nele) sem .pth nem usercustomize; os .pth do site do sistema ainda executam (lista em preparado.residuo_declarado)"))


# ---------------------------------------------------------------- 7. servico, aplicacao
def servico_responde(porta=None):
    """N3: a porta e lida NA HORA (porta=None -> PORTA_BANCADA corrente), nunca ligada na definicao da funcao."""
    porta = PORTA_BANCADA if porta is None else porta
    s = socket.socket()
    s.settimeout(1.5)
    try:
        s.connect(("127.0.0.1", porta))
        return True
    except OSError:
        return False
    finally:
        s.close()


def reverter_aplicacao(man_p, antes, contrato_p, n):
    """o manifesto anterior volta byte a byte; o contrato novo sai. O backup fica (backups nunca se apagam)."""
    tmp2 = man_p.with_name(man_p.name + ".tmp_rollback_B%d" % n)
    with tmp2.open("xb") as f:
        f.write(antes)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp2, man_p)
    divergiu = man_p.read_bytes() != antes
    # R32-B (R3.3): o contrato gravado sai tambem quando o rollback diverge (antes ficava no decoy, com o manifesto em bytes alheios)
    if contrato_p is not None and contrato_p.exists():
        contrato_p.unlink()
    if divergiu:
        raise Recusa("ROLLBACK_DIVERGE: o manifesto anterior nao voltou byte a byte; o contrato gravado foi retirado e o sha do manifesto em disco "
                     "esta no recibo (aplicacao_revertida, R32-B)")


def aplicar_na_bancada(bancada, canonical_mod, novo_bytes, contrato, nos_info, versao, n, stamp, antes_esperado, guarda_servico, recibo_rel):
    """grava na Bancada. R3:
      N4  compara o manifesto em disco com os bytes lidos no passo 3 (antes_esperado = anterior['_raw']), no inicio e de novo
          imediatamente antes da troca: uma mudanca feita durante a bateria e RECUSADA, nunca apagada (sem atualizacao perdida);
      N3  guarda_servico(momento) sonda o servico imediatamente antes de CADA gravacao; se voltou, recusa e desfaz o que nasceu;
      N10 o manifesto, o contrato e o recibo em estado\\sincronizacao sao conferidos ANTES da primeira gravacao: sem juncao, dentro."""
    bancada = Path(bancada)
    man_p = sem_juncao("canonical_contracts.json", bancada)
    contrato_p = sem_juncao(contrato[0], bancada)
    sem_juncao(recibo_rel, bancada)                       # N10: pre-voo do recibo em estado\sincronizacao
    if contrato_p.exists():
        raise Recusa("CONTRATO_JA_EXISTE: " + str(contrato_p))
    guarda_servico("antes_do_backup")
    antes = man_p.read_bytes()
    if antes != antes_esperado:
        raise Recusa("MANIFESTO_MUDOU_DESDE_A_LEITURA: o manifesto em disco (%s) nao e o lido no passo 3 (%s); nada gravado"
                     % (sha256(antes)[:16], sha256(antes_esperado)[:16]))
    bak = man_p.with_name(man_p.name + ".bak_B%d_%s" % (n, stamp))
    if bak.exists():
        raise Recusa("BACKUP_JA_EXISTE: " + str(bak))
    with bak.open("xb") as f:
        f.write(antes)
    if bak.read_bytes() != antes:
        raise Recusa("BACKUP_DIVERGE")
    tmp = man_p.with_name(man_p.name + ".tmp_B%d" % n)
    criado = None
    try:
        guarda_servico("antes_do_contrato")
        gravar_novo(contrato_p, contrato[1])
        criado = contrato_p
        guarda_servico("antes_do_temporario_do_manifesto")
        with tmp.open("xb") as f:
            f.write(novo_bytes)
            f.flush()
            os.fsync(f.fileno())
        if tmp.read_bytes() != novo_bytes:
            raise Recusa("ESCRITA_CURTA_DO_MANIFESTO")
        guarda_servico("imediatamente_antes_da_troca")
        # N4b (R3.1): a comparacao vem DEPOIS da sonda (que leva ate 1,5 s com a porta fechada) e imediatamente antes do os.replace
        if man_p.read_bytes() != antes_esperado:
            raise Recusa("MANIFESTO_MUDOU_DESDE_A_LEITURA: entre o backup e a troca (comparado depois da ultima sonda); nada trocado")
        os.replace(tmp, man_p)
    except Exception:
        if tmp.exists():
            tmp.unlink()
        if criado is not None and criado.exists():
            criado.unlink()
        raise
    try:
        if man_p.read_bytes() != novo_bytes:
            raise Recusa("MANIFESTO_DIVERGE_APOS_TROCA")
        pos = conferir_repinagem(canonical_mod, bancada, nos_info, versao, "pos_sincronizacao")
    except Exception as exc:
        reverter_aplicacao(man_p, antes, contrato_p, n)
        raise Recusa("APLICACAO_REVERTIDA: " + str(exc))
    return dict(manifesto=str(man_p), backup=str(bak), backup_sha256=sha256(antes), contrato=str(contrato_p), pos_conferencia=pos,
                manifesto_lido_no_passo_3_sha256=sha256(antes_esperado), _antes=antes, _contrato_p=contrato_p, _man_p=man_p)


VARIAVEIS_INJETAVEIS = ("PYTHONPATH", "PYTHONHOME", "PYTHONSTARTUP", "PYTHONUSERBASE", "PYTHONPLATLIBDIR", "PYTHONEXECUTABLE", "PYTHONINSPECT")


def guardar_saida(saida, bancada, nos_dir, versao, bateria_p, fase="pos_selo"):
    """A5/N8: --saida so sob as raizes ESTREITAS (raizes_saida(versao) e C:/t/vb*), nunca sob a producao, o Nos, a propria Bancada,
    a pasta do esboco ou a pasta de qualquer fonte/copia da bateria. So le; nada grava. Devolve o nome da raiz admitida."""
    if PRODUCAO.exists() and dentro_de(saida, PRODUCAO):
        raise Recusa("SAIDA_NA_PRODUCAO: " + str(saida))
    if NOS_PADRAO.exists() and dentro_de(saida, NOS_PADRAO):
        raise Recusa("SAIDA_NO_NOS: " + str(saida))
    if dentro_de(saida, bancada):
        raise Recusa("SAIDA_DENTRO_DA_BANCADA: " + str(saida))
    if nos_dir.exists() and dentro_de(saida, nos_dir):
        raise Recusa("SAIDA_NO_NOS: " + str(saida))
    proibidas = {AQUI, Path(bateria_p).parent}
    try:
        bj = json.loads(Path(bateria_p).read_bytes())
        for t in bj.get("testes") or []:
            for f in t.get("fontes") or []:
                if Path(str(f.get("path"))).is_absolute():
                    proibidas.add(Path(f["path"]).parent)
        for c in bj.get("copias") or []:
            if Path(str(c.get("de"))).is_absolute():
                proibidas.add(Path(c["de"]).parent)
    except (OSError, ValueError, AttributeError, TypeError):
        pass   # a bateria ilegivel e recusada na carga, com recibo; aqui so se protegem as pastas que se consegue ler
    for d in sorted(proibidas, key=str):
        if d.exists() and dentro_de(saida, d):
            raise Recusa("SAIDA_NA_PASTA_DE_FONTES: %s esta sob %s (pasta do esboco ou de fonte/copia pinada da bateria)" % (saida, d))
    for r in raizes_saida(versao, fase):    # a raiz pode ainda nao existir (a cadeia cria work/vNNN_bateria): a comparacao e por caminho canonico
        if dentro_de(saida, r):
            return str(r)
    sc = caminho_canonico(saida)
    rs = caminho_canonico(RAIZ_SANDBOX) if RAIZ_SANDBOX.exists() else None
    if rs is not None and dentro_de(sc, rs) and not mesmo_no(sc, rs):
        primeiro = Path(os.path.relpath(sc, rs)).parts[0]
        if RE_SANDBOX_DIR.match(primeiro):
            return str(rs / primeiro)
    raise Recusa("SAIDA_FORA_DAS_RAIZES_PERMITIDAS: %s (permitidas: %s; e C:/t/vb*)" % (saida, "; ".join(str(r) for r in raizes_saida(versao, fase))))


# ---------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description="o elo B(n): sincroniza a Bancada Um com o um.py selado (esboco funcional %s)" % REVISAO)
    ap.add_argument("--nos", default=str(NOS_PADRAO))
    ap.add_argument("--bancada", required=True)
    ap.add_argument("--versao", required=True)
    ap.add_argument("--saida", required=True, help="pasta nova desta sincronizacao (recibos, staging); so sob as raizes estreitas (A5/N8)")
    ap.add_argument("--bateria", required=True, help="BATERIA_VINCULO.json (R2/R3: com testes_sha256 e {fonte:N})")
    ap.add_argument("--bateria-sha256", default=None, help="sha256 esperado do BATERIA_VINCULO.json (obrigatorio em aplicar; lido de vNNN_pins) -- A7")
    ap.add_argument("--tunel", default=str(TUNEL_PADRAO))
    ap.add_argument("--modo", choices=("ensaio", "aplicar"), default="ensaio")
    ap.add_argument("--evento", default=None, help="seq do evento c1 (tipo SINCRONIZACAO_BANCADA) que nomeia a gravacao; em sandbox, SANDBOX:<texto>")
    ap.add_argument("--evento-hash", default=None, help="N6: o hash (>=16 hex) do elo do evento, lido pela cadeia do retorno de iald.py anotar")
    ap.add_argument("--eventos", default=None, help="SO em --sandbox: um livro de eventos alternativo (copia) para ensaiar a verificacao pela cadeia de hash")
    ap.add_argument("--producao", action="store_true", help="obrigatorio quando --bancada e a Bancada de producao (por identidade)")
    ap.add_argument("--sandbox", action="store_true", help="permite Nos fora do caminho pinado e evento SANDBOX:*; recusado se o manifesto pina o Nos real")
    ap.add_argument("--kernel-recibo", default=None, help="recibo do build do kernel da etapa 2 (T17), contrato KERNEL_RECIBO_R3 -- A1/N1")
    ap.add_argument("--kernel-recibo-sha256", default=None, help="N1: sha256 esperado do recibo do kernel (lido de vNNN_pins); obrigatorio em aplicar com --kernel-recibo")
    ap.add_argument("--criterios", default=None, help="A3 (R3.1): CRITERIOS_vNNN.json (contrato CRITERIOS_R3_1) com os ESPERADOS da secao 4 item 6; obrigatorio com --kernel-recibo")
    ap.add_argument("--criterios-sha256", default=None, help="A3 (R3.1): sha256 esperado do CRITERIOS_vNNN.json (lido de vNNN_pins); obrigatorio com --criterios")
    ap.add_argument("--fase", choices=("pre_selo", "pos_selo"), default="pos_selo",
                    help="pre_selo = os testes finais contra a versao ainda canonica (etapa 1 da cadeia); pos_selo = o elo B(n) depois do selo")
    ap.add_argument("--recibo-pre-selo", default=None, help="na fase pos_selo: o RECIBO_SINCRONIZACAO da fase pre_selo (conferido por identidade -- A6; obrigatorio fora do sandbox)")
    ap.add_argument("--recibo-pre-selo-sha256", default=None, help="N2: sha256 esperado do recibo pre-selo (lido de vNNN_pins); obrigatorio em --producao e em aplicar fora do sandbox")
    ap.add_argument("--selo-anterior", default=None, help="R31-3 (R3.2): o selo da versao anterior (copia de custodia); sha == o selo pinado no manifesto vigente da "
                                                         "Bancada; obrigatorio com --recibo-pre-selo")
    ap.add_argument("--kernel-manifesto-anterior", default=None, help="R31-3 (R3.2): o tgl_kernel_proof_manifest.json da versao anterior (custodia); sha == o "
                                                                     "pino do --selo-anterior; obrigatorio com --recibo-pre-selo")
    ap.add_argument("--cadeia-de-selos", default=None, help="R3.4 (S): a CADEIA_DE_SELOS (contrato CADEIA_DE_SELOS_R3_4) entre a versao que a Bancada pina e a do Nos; obrigatoria em "
                                                          "--fase pre_selo quando a Bancada pina uma versao anterior a do Nos (salto); em pos_selo, junto do recibo pre-selo de um salto")
    ap.add_argument("--cadeia-de-selos-sha256", default=None, help="R3.4 (S): sha256 esperado da cadeia de selos (lido de vNNN_pins); obrigatorio com --cadeia-de-selos")
    ap.add_argument("--forcar-regeracao", action="store_true", help="regenera mesmo se a Bancada ja pina a versao alvo")
    ap.add_argument("--reparo-de-pino", action="store_true", help="A8/N15: so em aplicar, com evento c1 que traga dados.reparo=true: admite mesma versao com outro hash do um.py ou do selo")
    ap.add_argument("--sem-bateria", action="store_true", help="SO para controles negativos: pula a bateria (nunca em aplicar)")
    def recusa_sem_recibo(motivo):
        # antes de --saida ser admitida nada pode ser gravado: a recusa e so impressa (fail-closed, rc 2)
        print(json.dumps(dict(veredito="RECUSADA", recusa=limpar(motivo), recibo=None, nota="recusa anterior a admissao de --saida: nada gravado"), ensure_ascii=False))
        return 2

    # R31-1 (R3.2): o interpretador de novo (a guarda do topo so roda como __main__; aqui vale tambem para main() chamada em processo)
    falta_flags = _flags_que_faltam()
    if falta_flags:
        return recusa_sem_recibo("INTERPRETADOR_NAO_ISOLADO: o esboco grava a producao e exige python -I -B -X utf8; faltam: %s (R31-1)" % ", ".join(falta_flags))
    a = ap.parse_args(argv)

    stamp = time.strftime("%Y%m%d_%H%M%S")

    # 0. guardas de ambiente e de caminho (N5, A2, A5, N8, N13) -- antes de qualquer gravacao
    try:
        if not sys.flags.ignore_environment:
            injet = [v for v in VARIAVEIS_INJETAVEIS if os.environ.get(v)]
            if injet:
                raise Recusa("AMBIENTE_PYTHON_INJETAVEL: %s no ambiente; rode com -E ou limpe o ambiente (N5)" % injet)
        if not re.match(r"^v\d{3,4}$", str(a.versao)):
            raise Recusa("VERSAO_INVALIDA: %r (vNNN)" % a.versao)
        bancada = caminho_canonico(a.bancada)
        saida = caminho_canonico(a.saida)
        nos_dir = caminho_canonico(a.nos)
        bateria_p = caminho_canonico(a.bateria)
        if not bancada.is_dir():
            raise Recusa("BANCADA_INEXISTENTE: " + str(bancada))
        raiz_admitida = guardar_saida(saida, bancada, nos_dir, a.versao, bateria_p, a.fase)
        producao = mesmo_no(bancada, PRODUCAO) if PRODUCAO.exists() else False
        if producao and not a.producao:
            raise Recusa("PRODUCAO_SEM_FLAG: --bancada e a Bancada de producao (por identidade); exige --producao")
        if producao and a.sandbox:
            raise Recusa("SANDBOX_NA_PRODUCAO")
        if a.eventos and not a.sandbox:
            raise Recusa("EVENTOS_ALTERNATIVO_FORA_DO_SANDBOX")
    except Recusa as exc:
        return recusa_sem_recibo(str(exc))
    except Exception as exc:
        return recusa_sem_recibo("ERRO_NAO_PREVISTO_NAS_GUARDAS: %s: %s" % (type(exc).__name__, exc))

    saida.mkdir(parents=True, exist_ok=True)
    script_sha = sha256(Path(__file__).read_bytes())
    recibo = dict(esboco="sincronizar_bancada.py %s -- NAO INSTALADO; desenho da gerencia c1; roda em sandbox contra uma copia" % REVISAO,
                  script_sha256=script_sha, bateria=dict(path=str(bateria_p), sha256=None, sha256_esperado=a.bateria_sha256, versao=None),
                  inicio_utc=agora(), stamp=stamp, modo=a.modo, sandbox=bool(a.sandbox), producao=producao, python_dont_write_bytecode=bool(sys.dont_write_bytecode),
                  python_ignore_environment=bool(sys.flags.ignore_environment), python_no_user_site=bool(sys.flags.no_user_site),
                  python_isolado=dict(isolated=bool(sys.flags.isolated), safe_path=bool(sys.flags.safe_path), utf8_mode=bool(sys.flags.utf8_mode),
                                      dont_write_bytecode_flag=bool(sys.flags.dont_write_bytecode), inspect=bool(sys.flags.inspect),
                                      interactive=bool(sys.flags.interactive), orig_argv=[str(x_) for x_ in getattr(sys, "orig_argv", [])],
                                      exigido="python -I -B -X utf8 (R31-1; R32-A: sem -i)"),
                  saida=dict(dir=str(saida), raiz_admitida=raiz_admitida),
                  fase=a.fase, recibo_pre_selo=None, reparo_de_pino=bool(a.reparo_de_pino), sondagens_do_servico=[],
                  versao_alvo=a.versao, bancada=dict(dir=str(bancada), forma_dada=a.bancada), nos=None, manifesto_anterior=None, manifesto_novo=None,
                  bateria_resultado=None, aplicacao=None, veredito=None,
                  escopo="IDENTIDADE_E_TESTES_SINTETICOS; NENHUMA_LEITURA_FISICA; NOT_FALSIFIED nao e creditacao", gate_effect="NONE")

    def fechar(veredito, codigo=0, recusa=None):
        recibo["veredito"] = limpar(veredito)
        recibo["recusa"] = limpar(recusa) if recusa is not None else None
        recibo["fim_utc"] = agora()
        try:
            dados = json_bytes(recibo)
        except Recusa:
            # N14: o recibo completo trazia a palavra guardada (vinda de dado de entrada): grava-se um recibo MINIMO, sem ela; rc 2
            bruto = json.dumps(recibo, ensure_ascii=False, default=str)
            recibo_min = dict(esboco=recibo["esboco"], script_sha256=script_sha, stamp=stamp, modo=a.modo, versao_alvo=a.versao,
                              veredito="RECUSADA", recusa="PALAVRA_PROIBIDA_NA_SAIDA: o recibo completo continha a palavra guardada e foi suprimido",
                              recibo_suprimido_sha256=sha256(bruto.encode("utf-8")), veredito_original_suprimido=True, fim_utc=agora(), gate_effect="NONE")
            dados, veredito, recusa, codigo = json_bytes(recibo_min), "RECUSADA", recibo_min["recusa"], 2
        nome = ("RECIBO_SINCRONIZACAO_%s_%s.json" if recusa is None else "RECUSA_SINCRONIZACAO_%s_%s.json") % (a.versao, stamp)
        p = gravar_novo(saida / nome, dados)
        print(json.dumps(dict(veredito=limpar(veredito), recusa=(limpar(recusa) if recusa is not None else None), recibo=str(p),
                              recibo_sha256=sha256(p.read_bytes())), ensure_ascii=False))
        return codigo

    def guarda_servico(momento):
        """N3: so na producao, em aplicar: o servico e sondado de novo neste momento; no ar = recusa."""
        if not (producao and a.modo == "aplicar"):
            return
        no_ar = bool(servico_responde())
        recibo["sondagens_do_servico"].append(dict(momento=momento, no_ar=no_ar, quando=agora()))
        if no_ar:
            raise Recusa(("SERVICO_NO_AR" if momento == "inicio" else "SERVICO_VOLTOU_ANTES_DE_GRAVAR") +
                         ": %s -- quiesce e pare o um_bancada.py (ato com recibo) antes de aplicar; o manifesto em RAM nao recarrega" % momento)

    estado_run = dict(novo_sha256=None)

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
                    "guardou em RAM o manifesto NOVO (%s) e o disco ficou com %s (%s): pare e religue o um_bancada.py com recibo de identidade "
                    "(10-ter) antes de qualquer B(n). Causa do rollback: %s" % (str(estado_run["novo_sha256"])[:16],
                                                                                "bytes alheios, nao o anterior (R32-B)" if msg.startswith("ROLLBACK_DIVERGE") else "o ANTERIOR",
                                                                                str(disco)[:16], msg))
        return msg

    try:
        guarda_servico("inicio")
        if a.modo == "aplicar":
            recibo["servico_e_manifesto_em_ram"] = N3A_NOTA
        if a.modo == "aplicar" and a.sem_bateria:
            raise Recusa("APLICAR_SEM_BATERIA_PROIBIDO")
        if a.reparo_de_pino and a.modo != "aplicar":
            raise Recusa("REPARO_SO_EM_APLICAR: --reparo-de-pino exige --modo aplicar e evento c1 com dados.reparo=true")
        if a.modo == "aplicar" and a.fase != "pos_selo" and not a.reparo_de_pino:
            raise Recusa("APLICAR_SO_NA_FASE_POS_SELO: o elo B(n) grava depois do selo; antes dele so ensaio (salvo --reparo-de-pino nomeado em evento)")
        if a.fase == "pos_selo" and not a.recibo_pre_selo and a.modo == "aplicar" and not a.sandbox:
            raise Recusa("RECIBO_PRE_SELO_AUSENTE: o elo B(n) exige o recibo dos testes finais da fase pre_selo")
        if a.fase == "pre_selo" and a.recibo_pre_selo:
            raise Recusa("RECIBO_PRE_SELO_NA_FASE_PRE_SELO")
        if (a.selo_anterior or a.kernel_manifesto_anterior) and not a.recibo_pre_selo:
            raise Recusa("SELO_ANTERIOR_SEM_RECIBO_PRE_SELO: --selo-anterior/--kernel-manifesto-anterior so servem para cruzar o recibo pre-selo (R31-3)")
        # N2: o recibo pre-selo por pino
        if a.recibo_pre_selo and not a.recibo_pre_selo_sha256 and (producao or (a.modo == "aplicar" and not a.sandbox)):
            raise Recusa("RECIBO_PRE_SELO_SHA_AUSENTE: em --producao (e em aplicar fora do sandbox) a cadeia passa --recibo-pre-selo-sha256 (lido de vNNN_pins)")
        # N1: o recibo do kernel por pino
        if a.modo == "aplicar" and a.fase == "pos_selo" and not a.sandbox and not a.kernel_recibo:
            raise Recusa("KERNEL_RECIBO_AUSENTE: o elo B(n) exige o recibo do build do kernel da etapa 2 (T17)")
        if a.kernel_recibo and a.modo == "aplicar" and not a.kernel_recibo_sha256:
            raise Recusa("KERNEL_RECIBO_SHA_AUSENTE: em aplicar a cadeia passa --kernel-recibo-sha256 (lido de vNNN_pins)")
        if a.kernel_recibo and a.kernel_recibo_sha256:
            kpp = Path(a.kernel_recibo)
            if not kpp.is_file():
                raise Recusa("KERNEL_RECIBO_AUSENTE: " + str(kpp))
            if sha256(kpp.read_bytes()) != str(a.kernel_recibo_sha256).lower():
                raise Recusa("KERNEL_RECIBO_SHA_DIVERGE: arquivo %s != esperado %s" % (sha256(kpp.read_bytes())[:16], str(a.kernel_recibo_sha256)[:16]))
        # A3 (R3.1): os ESPERADOS dos criterios vem de um arquivo pinado pela cadeia, nunca do recibo do kernel
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
        bateria, bateria_raw, bateria_sha = carregar_bateria(bateria_p, a.bateria_sha256, a.modo, a.fase, a.sandbox)
        recibo["bateria"].update(sha256=bateria_sha, versao=bateria.get("versao_bateria"), n_testes=len(bateria["testes"]))
        # 1. o selo e o um.py (A11) e o manifesto do kernel (N1)
        nos_info = ler_nos(nos_dir, a.versao)
        recibo["nos"] = {k: v for k, v in nos_info.items() if not k.startswith("_")}
        # R3.4 (P): a bateria por versao -- pinos_da_versao e testes pina_o_um_py conferidos contra o Nos lido agora (pino velho = recusa antes de qualquer gravacao)
        recibo["bateria"]["pinos_da_versao"] = conferir_pinos_da_versao(bateria, nos_info, a.versao)
        # 2. o evento c1 (A4, N6, N11) -- em aplicar, verificado pela cadeia de hash; em ensaio, so anotado
        if a.modo == "aplicar":
            evento = verificar_evento(a.evento, a.versao, bancada, a.sandbox, nos_info, a.reparo_de_pino, a.eventos, a.evento_hash)
        else:
            evento = dict(evento=a.evento, verificado=False, nota="ensaio: nenhuma gravacao na Bancada") if a.evento else None
        recibo["evento_c1"] = evento
        # 3. o manifesto vigente (A2, A6, A8, N12, N15)
        canonical_mod, canonical_pin = carregar_canonical(bancada)
        recibo["bancada"]["canonical_py_instalado"] = canonical_pin
        anterior = estado_anterior(bancada, canonical_mod)
        recibo["manifesto_anterior"] = {k: v for k, v in anterior.items() if not k.startswith("_")}
        if not anterior["script_path_pinado"] or not anterior["seal_path_pinado"]:
            raise Recusa("MANIFESTO_SEM_PINO_DO_NOS")

        def _mesmo_arquivo(x, y):
            try:
                return os.path.samefile(x, y)
            except OSError:
                return False
        # N12: o sandbox e recusado se o manifesto pina o Nos real pela PASTA ou por ARQUIVO (hardlink dos arquivos do Nos noutra pasta)
        pina_nos_real = NOS_PADRAO.exists() and (mesmo_no(Path(anterior["script_path_pinado"]).parent, NOS_PADRAO)
                                                 or _mesmo_arquivo(anterior["script_path_pinado"], NOS_PADRAO / "um.py")
                                                 or _mesmo_arquivo(anterior["seal_path_pinado"], NOS_PADRAO / "um_absoluto_selo.json"))
        recibo["manifesto_anterior"]["pina_o_nos_real"] = pina_nos_real
        if a.sandbox and pina_nos_real:
            raise Recusa("SANDBOX_COM_MANIFESTO_QUE_PINA_O_NOS_REAL: o sandbox so existe para copia cujo manifesto pina um Nos de ensaio")
        nos_pinado = mesmo_no(anterior["script_path_pinado"], nos_info["um_py"]["path"]) and mesmo_no(anterior["seal_path_pinado"], nos_info["selo"]["path"])
        recibo["manifesto_anterior"]["nos_alvo_e_o_pinado"] = nos_pinado
        if not nos_pinado and not a.sandbox:
            raise Recusa("NOS_DIFERENTE_DO_PINADO: o manifesto pina %s; o alvo e %s (so em --sandbox)" % (anterior["script_path_pinado"], nos_info["um_py"]["path"]))
        if anterior["estado_do_contrato_instalado"] not in ("OK",) + ESPERADOS_POS_SELO:
            raise Recusa("BANCADA_EM_ESTADO_DESCONHECIDO: " + anterior["estado_do_contrato_instalado"])
        # A8: a mesma versao com outro hash do um.py nao e sincronizacao -- e divergencia de selo/programa (ou corrupcao do manifesto)
        if anterior["version"] == a.versao and anterior["um_py_pinado"] != nos_info["um_py"]["sha256"]:
            if not a.reparo_de_pino:
                raise Recusa("SELO_PROGRAMA_DIVERGE: a Bancada pina %s %s e o Nos tem %s %s com a MESMA versao; nunca atualizar so o hash "
                             "(so --reparo-de-pino em aplicar com evento c1 dados.reparo=true)"
                             % (anterior["version"], str(anterior["um_py_pinado"])[:16], a.versao, nos_info["um_py"]["sha256"][:16]))
            recibo["reparo_de_pino_autorizado_por"] = (evento or {}).get("evento")
        # N15 [INPUT da gerencia]: mesma versao, MESMO um.py, selo diferente (ex.: o rito refeito): nao e sincronizacao
        elif anterior["version"] == a.versao and anterior["seal_sha_pinado"] != nos_info["selo"]["sha256"]:
            if not a.reparo_de_pino:
                raise Recusa("SEAL_CHANGED_SAME_VERSION: a Bancada pina o selo %s da %s e o Nos tem o selo %s com o MESMO um.py e a MESMA versao; "
                             "nunca re-pinar o selo em silencio (so --reparo-de-pino em aplicar com evento c1 dados.reparo=true)"
                             % (str(anterior["seal_sha_pinado"])[:16], a.versao, nos_info["selo"]["sha256"][:16]))
            recibo["reparo_de_pino_autorizado_por"] = (evento or {}).get("evento")
        ja_sincronizada = (anterior["estado_do_contrato_instalado"] == "OK" and anterior["version"] == a.versao
                           and anterior["um_py_pinado"] == nos_info["um_py"]["sha256"] and anterior["seal_sha_pinado"] == nos_info["selo"]["sha256"]
                           and nos_pinado)
        # R3.4 (S): o salto. Em pre_selo, se a Bancada pina uma versao anterior a do Nos, a cadeia de selos e OBRIGATORIA e e conferida por hash (inicio = a Bancada,
        # fim = o Nos lido agora); em pos_selo ela acompanha o recibo pre-selo de um salto (conferir_recibo_pre_selo). Cadeia sem salto e recusada (flag sem efeito).
        if a.cadeia_de_selos_sha256 and not a.cadeia_de_selos:
            raise Recusa("CADEIA_DE_SELOS_AUSENTE: --cadeia-de-selos-sha256 sem --cadeia-de-selos")
        cadeia, salto = None, None
        if a.cadeia_de_selos:
            cadeia = carregar_cadeia_de_selos(a.cadeia_de_selos, a.cadeia_de_selos_sha256)
            recibo["cadeia_de_selos"] = cadeia_para_recibo(cadeia)
        atrasada = a.fase == "pre_selo" and not ja_sincronizada and anterior["version"] != a.versao
        if atrasada:
            if versao_numero(anterior["version"]) > versao_numero(a.versao):
                raise Recusa("BANCADA_A_FRENTE_DO_NOS: a Bancada pina %s e o Nos tem %s; um salto so vai para a frente (R3.4)" % (anterior["version"], a.versao))
            if cadeia is None:
                raise Recusa("BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS: a Bancada pina %s e o Nos tem %s; o ensaio pre_selo de uma Bancada atrasada exige --cadeia-de-selos e "
                             "--cadeia-de-selos-sha256 (a cadeia de selos de %s a %s verificada por hash) (R3.4)" % (anterior["version"], a.versao, anterior["version"], a.versao))
            conferir_cadeia_com_a_bancada(cadeia, anterior)
            conferir_cadeia_com_o_fim(cadeia, a.versao, nos_info["um_py"]["sha256"], nos_info["selo"]["sha256"], (nos_info.get("kernel") or {}).get("sha256"), "o Nos lido agora")
            salto = montar_salto(cadeia, anterior)
            recibo["salto"] = salto
        elif cadeia is not None and not (a.fase == "pos_selo" and a.recibo_pre_selo):
            raise Recusa("CADEIA_DE_SELOS_SEM_SALTO: --cadeia-de-selos so serve a uma Bancada atrasada (pre_selo) ou ao recibo pre-selo de um salto (pos_selo) (R3.4)")
        if a.recibo_pre_selo:                             # A6, N2
            recibo["recibo_pre_selo"] = conferir_recibo_pre_selo(a.recibo_pre_selo, anterior, bancada, ja_sincronizada, a.recibo_pre_selo_sha256,
                                                                 a.selo_anterior, a.kernel_manifesto_anterior, cadeia)
            salto = recibo["recibo_pre_selo"].get("salto")
            if salto is not None:
                recibo["salto"] = salto
                if salto["proxima_a_selar"] != a.versao:
                    raise Recusa("SALTO_VERSAO_NAO_CONSECUTIVA: o recibo pre-selo e de um salto que termina em %s e a versao a sincronizar e %s (a seguinte seria %s) (R3.4)"
                                 % (salto["ate"]["versao"], a.versao, salto["proxima_a_selar"]))
        if not nos_pinado:
            recibo["sonda_pos_selo_em_ram"] = sonda_pos_selo_em_ram(bancada, canonical_mod, anterior, nos_info)
            if not recibo["sonda_pos_selo_em_ram"]["recusou"] or recibo["sonda_pos_selo_em_ram"]["codigo"] not in ESPERADOS_POS_SELO:
                raise Recusa("CANONICAL_INSTALADO_NAO_RECUSOU_PINO_VELHO: " + str(recibo["sonda_pos_selo_em_ram"]))
        elif anterior["estado_do_contrato_instalado"] in ESPERADOS_POS_SELO:
            recibo["pino_velho_recusado_pelo_instalado"] = anterior["estado_do_contrato_instalado"]
        # 4. regenerar (ou nao)
        raiz = saida / "raiz"
        if ja_sincronizada and not a.forcar_regeracao:
            recibo["manifesto_novo"] = None
            cand, copias = montar_staging(bancada, anterior["_man"], raiz)
            recibo["staging"] = dict(candidate=str(cand), n_copias=len(copias), manifesto="o vigente (ja sincronizada)")
            recibo["repinagem"] = conferir_repinagem(canonical_mod, cand, nos_info, a.versao, "ensaio_ja_sincronizada")
            veredito_base = "JA_SINCRONIZADA"
            novo_bytes = contrato = n = None
        else:
            novo, md, rotulo, n = regenerar(bancada, anterior, nos_info, a.versao, (evento or {}).get("evento"), script_sha, bateria_sha, a.modo,
                                            a.forcar_regeracao, stamp, recibo.get("recibo_pre_selo"), a.reparo_de_pino, salto)
            novo["sincronizacao"]["evento_c1_hash"] = (evento or {}).get("hash")
            novo["sincronizacao"]["kernel_recibo_sha256"] = str(a.kernel_recibo_sha256).lower() if a.kernel_recibo_sha256 else None
            novo["sincronizacao"]["kernel_manifesto_sha256"] = (nos_info.get("kernel") or {}).get("sha256")
            novo_bytes = json_bytes(novo)
            estado_run["novo_sha256"] = sha256(novo_bytes)
            contrato = (rotulo, md)
            gravar_novo(saida / ("MANIFESTO_CANDIDATO_B%d.json" % n), novo_bytes)
            gravar_novo(saida / rotulo, md)
            recibo["manifesto_novo"] = dict(deployment_id=novo["deployment_id"], sha256=sha256(novo_bytes), bytes=len(novo_bytes), n_code=len(novo["code"]),
                                            n_sources=len(novo["sources"]), contrato=rotulo, contrato_sha256=sha256(md), candidato=str(saida / ("MANIFESTO_CANDIDATO_B%d.json" % n)),
                                            recibo_pre_selo_sha256_encadeado=novo["sincronizacao"]["recibo_pre_selo_sha256"],
                                            kernel_recibo_sha256_encadeado=novo["sincronizacao"]["kernel_recibo_sha256"])
            cand, copias = montar_staging(bancada, novo, raiz, novo_bytes, contrato)
            recibo["staging"] = dict(candidate=str(cand), n_copias=len(copias), manifesto="o regenerado B%d" % n)
            recibo["repinagem"] = conferir_repinagem(canonical_mod, cand, nos_info, a.versao, "ensaio_repinagem_B%d" % n)
            veredito_base = "REPINADA_B%d" % n
            if salto is not None:       # R3.4 (S): o veredito diz o salto (de onde a Bancada sai e a versao a que chega)
                veredito_base += "__SALTO_%s_%s" % (salto["de"]["versao"], a.versao)
        # 6. a bateria (contra a copia; A1, A3, N1, N5, N14, N16)
        if a.sem_bateria:
            recibo["bateria_resultado"] = dict(veredito="BATERIA_PULADA_SO_CONTROLE_NEGATIVO")
        else:
            copias_feitas = copiar_testes(bateria, raiz)
            recibo["copias_de_testes"] = copias_feitas
            ctx = dict(py=sys.executable, raiz=str(raiz), candidate=str(cand), nos=str(nos_dir), versao=a.versao,
                       recibos=str(saida / "recibos"), tunel=str(caminho_canonico(a.tunel)), saida=str(saida), rotulo="V" + stamp,
                       kernel_recibo=a.kernel_recibo or "", kernel_recibo_sha256=(str(a.kernel_recibo_sha256).lower() if a.kernel_recibo_sha256 else ""),
                       um_py_path=nos_info["um_py"]["path"], um_py_sha256=nos_info["um_py"]["sha256"], um_py_bytes=nos_info["um_py"]["bytes"], selo_sha256=nos_info["selo"]["sha256"])
            recibo["bateria_resultado"] = rodar_bateria(bateria, ctx, saida / "recibos", a.modo, a.fase, a.sandbox, recibo.get("recibo_pre_selo"), nos_info, copias_feitas,
                                                        criterios)
            if recibo["bateria_resultado"]["veredito"] != "BATERIA_PASSA":
                return fechar(veredito_base + "__BATERIA_FALHOU__NADA_GRAVADO_NA_BANCADA", 3)
            if a.modo == "aplicar":
                # em aplicar nenhum teste obrigatorio pode ficar por executar (salvo os de outra fase, lidos por hash do recibo pre-selo)
                pendentes = [r["id"] for r in recibo["bateria_resultado"]["testes"]
                             if r["resultado"] == "NAO_EXECUTADO" and a.modo in r["obrigatorio_em"] and a.fase in r["fases"]]
                if pendentes and not a.sandbox:
                    return fechar(veredito_base + "__BATERIA_INCOMPLETA__NADA_GRAVADO_NA_BANCADA: %s" % pendentes, 3)
                recibo["bateria_resultado"]["nao_executados_tolerados_em_sandbox"] = pendentes
        # 7. aplicar (so com evento verificado, servico parado a cada gravacao e bateria passada)
        if a.modo == "aplicar":
            if novo_bytes is None:
                recibo["aplicacao"] = dict(nota="ja sincronizada: nada a gravar")
                return fechar(veredito_base + "__NADA_A_GRAVAR", 0)
            nome_rec = "RECIBO_SINCRONIZACAO_%s_%s.json" % (a.versao, stamp)
            rel_rec = "estado/sincronizacao/" + nome_rec
            json_bytes(recibo)          # N14: pre-voo da guarda de palavra no recibo, antes da primeira gravacao na Bancada
            ap_res = aplicar_na_bancada(bancada, canonical_mod, novo_bytes, contrato, nos_info, a.versao, n, stamp, anterior["_raw"], guarda_servico, rel_rec)
            antes_b, contrato_p, man_p = ap_res.pop("_antes"), ap_res.pop("_contrato_p"), ap_res.pop("_man_p")
            recibo["aplicacao"] = ap_res
            est_criado = None
            try:
                guarda_servico("antes_do_recibo_em_estado")
                # R31-2 (R3.2): a sonda leva ate 1,5 s; depois dela, e ANTES de gravar o recibo, o manifesto no disco tem de ser o novo, byte a byte
                disco = man_p.read_bytes()
                recibo["aplicacao"]["conferencia_pos_troca"] = [dict(momento="depois_da_ultima_sonda_antes_do_recibo", manifesto_em_disco_sha256=sha256(disco),
                                                                     igual_ao_novo=(disco == novo_bytes))]
                if disco != novo_bytes:
                    raise Recusa("MANIFESTO_MUDOU_APOS_A_TROCA: o manifesto em disco (%s) nao e o novo (%s) depois da ultima sonda; o recibo nao e gravado (R31-2)"
                                 % (sha256(disco)[:16], sha256(novo_bytes)[:16]))
                est_rec = sem_juncao(rel_rec, bancada)                  # N10: conferido de novo, no caminho lexico
                est_rec.parent.mkdir(parents=True, exist_ok=True)
                est_rec = sem_juncao(rel_rec, bancada)                  # e depois do mkdir
                recibo["aplicacao"]["copia_do_recibo"] = str(est_rec)
                recibo["veredito"] = veredito_base + "__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO"
                recibo["fim_utc"] = agora()
                est_bytes = json_bytes(recibo)
                gravar_novo(est_rec, est_bytes)
                est_criado = (est_rec, sha256(est_bytes))
                # R31-2 (R3.2): e DEPOIS de gravar o recibo em estado, de novo (o recibo de --saida registra esta segunda conferencia)
                disco2 = man_p.read_bytes()
                recibo["aplicacao"]["conferencia_pos_troca"].append(dict(momento="depois_do_recibo_em_estado", manifesto_em_disco_sha256=sha256(disco2),
                                                                         igual_ao_novo=(disco2 == novo_bytes)))
                if disco2 != novo_bytes:
                    raise Recusa("MANIFESTO_MUDOU_APOS_O_RECIBO_EM_ESTADO: o manifesto em disco (%s) nao e o novo (%s) depois de gravar o recibo (R31-2)"
                                 % (sha256(disco2)[:16], sha256(novo_bytes)[:16]))
            except Exception as exc:
                # R31-2 (R3.2): bytes que nao sao nem o novo nem o anterior (uma gravacao alheia) ficam como evidencia em --saida, com sha, antes do rollback
                try:
                    estranho = man_p.read_bytes()
                except OSError as exc2:
                    estranho = None
                    recibo["aplicacao"]["manifesto_estranho"] = dict(ilegivel=str(exc2))
                if estranho is not None and estranho not in (novo_bytes, antes_b):
                    ev_p = gravar_novo(saida / ("MANIFESTO_ESTRANHO_APOS_A_TROCA_B%d_%s.json" % (n, stamp)), estranho)
                    recibo["aplicacao"]["manifesto_estranho"] = dict(evidencia=str(ev_p), sha256=sha256(estranho), bytes=len(estranho),
                                                                     nota="gravacao alheia depois do os.replace; o rollback devolve o ANTERIOR e estes bytes ficam so aqui")
                if est_criado is not None and est_criado[0].exists():
                    est_criado[0].unlink()          # o recibo em estado dizia APLICADA: sai junto com o contrato (o de --saida diz o que houve)
                    recibo["aplicacao"]["recibo_em_estado_retirado"] = dict(path=str(est_criado[0]), sha256=est_criado[1])
                reverter_aplicacao(man_p, antes_b, contrato_p, n)
                raise Recusa("APLICACAO_REVERTIDA: %s" % exc)
            return fechar(recibo["veredito"], 0)
        return fechar(veredito_base + "__ENSAIO__NADA_GRAVADO_NA_BANCADA", 0)
    except Recusa as exc:
        msg = str(exc)
        if msg.startswith(("APLICACAO_REVERTIDA", "ROLLBACK_DIVERGE")) and producao and a.modo == "aplicar":   # R32-B (R3.3): tambem apos ROLLBACK_DIVERGE
            msg = pos_rollback(msg)
        return fechar("RECUSADA", 2, msg)
    except Exception as exc:   # qualquer erro nao previsto tambem e recusa visivel, com recibo -- nunca traceback mudo nem "ok" falso
        return fechar("RECUSADA", 2, "ERRO_NAO_PREVISTO: %s: %s" % (type(exc).__name__, exc))


if __name__ == "__main__":
    sys.exit(main())

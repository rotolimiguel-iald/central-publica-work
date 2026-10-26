# -*- coding: utf-8 -*-
"""harness_textos_ensaio_v401.py -- o HARNESS DO POS-RITO da v401 em modo ENSAIO (derivado do harness_textos_ensaio_v399.py, que rodou na v399, com as licoes da v400); SO' LEITURA do Nos real, da producao e das superficies reais.
Importa os modulos REAIS textos_v401.py e leitura_v401.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v401 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel,
o .md, o artigo PT/EN e o sumario; o SIDECAR um_absoluto_selo_acom.json e' GERADO pela funcao do PROPRIO candidato (selo_acom_sidecar_v399, executada de uma copia de bytes) sobre o core e o selo FINAIS do Nos emulado, como em teste_conferidor_positivo_v401.py;
o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos: o stdout traz as linhas REAIS do fluxo principal do ensaio a seco (inclusive a linha [v401]) mais as que so' o rito acrescenta, com a linha real do sidecar por ultimo). Tudo o que ele escreve fica em pos_rito\\harness_saida_v401\\
(e o resumo HARNESS_TEXTOS_ENSAIO_v401.json ao lado dele); nada do Nos real, da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v401/um.py) e a regeneracao terminada (refazer_out_v401.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v401.py REAL roda numa COPIA em ARVORE (conferidor_emulado\\work\\cadeia_de_selo\\v401, com as pastas irmas v400 e v399 e work\\cunhagens_13out ao lado, porque o delta acha as falas do operador e os modulos anteriores pelo caminho da propria pasta), SEM -I (importa o um.py do Nos emulado,
                 que precisa do numpy do usuario), contra o Nos emulado (V401_NOS) e da' TUDO BATE, com os 16 itens C1-C16 e o round trip: a conferencia que a leitura le;
  leitura        a leitura_v401.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (selo de outra versao, registro ausente ou nao selado, o registro falsidade_da_inercia_v401 adulterado em checagem, valor, beta, posto inercial, fixo, 0_abs, estrela, gate, runtime e veredito,
                 a pedra FalsidadeDaInercia com bandeira falsa ou fora do trio (composicao, contrato, estrela, suporte, hash da fonte), cunhagens_v401 com inscricao rotulada como da gerencia ou nao embutida, sem ratificacao, com a fala adulterada, com a errata sem SUPERADA ou sem assinatura, os quatro registros da v399
                 recriados (selo ACOM, declaracao, cunhagens_v399, kh_n1_cobertura_v399) adulterados, o sidecar ausente ou adulterado, os resumos do selo primario (inclusive o da falsidade), quadro do topo que deixa de selar ou de estar no topo, C5, C15, C16, o round trip e o veredito da falsidade na conferencia,
                 registros da v400 a v393 nao selados, face de Fock habitada ou dita dentro da pedra, AVISO da v401 ou de bloco anterior, linhas [v399], [v401], [v398], [v397] e a linha do sidecar ausentes), cada um tem de reprovar;
  textos         todas as funcoes publicas de textos_v401 renderizam, a guarda P18 e a da DIRECAO ficam limpas em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  paragrafos     o PARAGRAFO DO QUADRO (textos_v401.paragrafo_readme, o da v397, intocado) passa nas verificacoes do quadro contra o resultado pinado e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado, p adulterado,
                 a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; a regra da ordem vale para TODO texto renderizado; e o PARAGRAFO NOVO (textos_v401.paragrafo_falsidade) passa na verificacao propria, com controles negativos (numero adulterado, frase de limite removida, estatuto removido,
                 citacao nao verbatim, o 4,44 intruso, alegacao de seguranca criptografica, «consciencia» como termo, a pedra dita prova de Newton, a errata sem SUPERADA); o handoff DIZ que o paragrafo do testemunho de dois segue como esta;
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v401.py REAL roda em COPIAS das superficies reais em TRES cenarios: (a) o MEMORY.md real como esta (a superficie NAO compacta: se ele passar de 195 linhas depois da edicao, tem de RECUSAR com rc 3 sem escrever nada; senao, o caminho normal),
                 (b) um MEMORY.md com FOLGA (copia reduzida): o plano e' conferido antes da primeira escrita, idempotente na 2a rodada, marcadores do passo 9, <= 195 linhas e < 24 000 B, (c) um MEMORY.md NO LIMITE (195 linhas): tem de RECUSAR com rc 3, imprimir as
                 contagens e nao escrever nada em nenhuma copia; os originais nao mudam;
  b3_recibo      b3_recibo_v401.py REAL contra recibos SINTETICOS derivados dos recibos reais da v400 (positivos e negativos);
  mapa           registrar_mapa_v401.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v401_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\*.py; ast.parse de todo .py e sh -n do chain.
uso: python -B -X utf8 harness_textos_ensaio_v401.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v401.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada, e o resumo vai para
HARNESS_TEXTOS_ENSAIO_v401_DEPURACAO_sem_refazer.json (o nome HARNESS_TEXTOS_ENSAIO_v401.json so' nasce na rodada que EXIGE o refazer);
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v401)"""
import contextlib, hashlib, importlib.util, io, json, os, re, runpy, shutil, subprocess, sys, time, traceback
sys.dont_write_bytecode = True
MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V401"
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
DRY = os.path.join(PKG, "dry_v401"); OUT = os.path.join(HERE, "harness_saida_v401"); NOSE = os.path.join(OUT, "nos_emulado")
sys.path.insert(0, PKG)
from guarda_p18_v401 import violacoes  # noqa: E402
argv = sys.argv[1:]
SEM_SUP = "--sem-superficies" in argv; SEM_B3 = "--sem-b3" in argv; SEM_NEG = "--sem-negativos" in argv; NAO_REFAZER = "--nao-exigir-refazer" in argv
ROTULO = argv[argv.index("--rotulo") + 1] if "--rotulo" in argv else "final"
sha = lambda b: hashlib.sha256(b).hexdigest()
fsha = lambda p: sha(open(p, "rb").read())
C = "C:" + os.sep
UMEM = os.path.join(C, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
ATLD = os.path.join(C, "IALD", "Central de Patentes", "memory")
HAJA = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "CLAUDE.md")
NOS_REAL = os.path.join(C, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
R = {"rotulo": ROTULO, "inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "emulado": ["stdout do rito (rodada_v401_stdout.txt em nos_emulado)", "APLICADO_AO_CANONICO", "o Nos inteiro (montado de dry_v401: core_ensaio, selo_ensaio completado com as chaves do selo da v400 que o main poe depois do literal, um.py, kernel, md, artigo)",
                                                                           "os recibos do B(n) (SINTETICOS, derivados dos recibos reais da v400)"], "etapas": {}, "problemas": []}


def falha(msg):
    R["problemas"].append(msg); print("  PROBLEMA:", msg)


def etapa(nome, **kw):
    R["etapas"][nome] = kw; return kw


def importar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def rd(p):
    return open(p, encoding="utf-8").read()


def rdj(p):
    return json.load(open(p, encoding="utf-8"))


def mt(p):
    return time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(p)))


# ------------------------------------------------------------------ 0. precondicoes
def recusa(msg):
    print("RECUSO:", msg); sys.exit(4)


for n in ("ESPERADOS_v401.json", "CANDIDATO_v401.json", "um_v401_candidato.py", "PINOS_BN_v401.json", "ensaio_a_seco_v401.json", "acom_conferencias_v401.py", "runtime_v401.py") + (() if NAO_REFAZER else ("refazer_out_v401.txt",)):
    if not os.path.exists(os.path.join(PKG, n)):
        recusa("falta %s no pacote" % n)
ESP = rdj(os.path.join(PKG, "ESPERADOS_v401.json")); CM = rdj(os.path.join(PKG, "CANDIDATO_v401.json"))
cand16 = fsha(os.path.join(PKG, "um_v401_candidato.py"))[:16]
if not (ESP["candidato_sha16"] == CM["sha16"] == cand16):
    recusa("o candidato nao e' um so': ESPERADOS %s, CANDIDATO %s, arquivo %s (regeneracao em curso?)" % (ESP["candidato_sha16"], CM["sha16"], cand16))
for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v401_pt.txt", "dry_v401_en.txt", "dry_v401_pt.toc", "dry_v401_en.toc", "tgl_kernel"):
    if not os.path.exists(os.path.join(DRY, n)):
        recusa("dry_v401 incompleto (falta %s): a regeneracao ainda nao terminou?" % n)
if fsha(os.path.join(DRY, "um.py"))[:16] != ESP["candidato_sha16"]:
    recusa("o um.py de dry_v401 (%s) != o candidato de ESPERADOS (%s): o dry e' de outra geracao" % (fsha(os.path.join(DRY, "um.py"))[:16], ESP["candidato_sha16"]))
refazer = rd(os.path.join(PKG, "refazer_out_v401.txt")) if os.path.exists(os.path.join(PKG, "refazer_out_v401.txt")) else ""
if not NAO_REFAZER and "== FIM" not in refazer:
    recusa("refazer_out_v401.txt nao mostra '== FIM': a regeneracao nao terminou")
if not NAO_REFAZER and os.path.getmtime(os.path.join(PKG, "refazer_out_v401.txt")) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v401.json")):
    recusa("refazer_out_v401.txt e' mais ANTIGO que ESPERADOS_v401.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
if os.path.getmtime(os.path.join(DRY, "core_ensaio.json")) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v401.json")) - 600:
    recusa("o core_ensaio.json de dry_v401 e' mais de 10 min mais antigo que ESPERADOS_v401.json: dry de outra geracao?")
EVID = {n: {"mtime": mt(os.path.join(PKG, n)), "sha16": fsha(os.path.join(PKG, n))[:16]} for n in ("ESPERADOS_v401.json", "CANDIDATO_v401.json", "um_v401_candidato.py", "PINOS_BN_v401.json", "refazer_out_v401.txt") if os.path.exists(os.path.join(PKG, n))}
EVID.update({"dry_v401/" + n: {"mtime": mt(os.path.join(DRY, n)), "sha16": fsha(os.path.join(DRY, n))[:16]} for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "dry_v401_pt.txt")})
etapa("precondicoes", ok=True, candidato_sha16=cand16, evidencia=EVID, refazer_exigido=not NAO_REFAZER, refazer_out_presente=os.path.exists(os.path.join(PKG, "refazer_out_v401.txt")), refazer_fim_visto=("== FIM" in refazer),
      nota=("MODO --nao-exigir-refazer: a regeneracao do candidato NAO foi comprovada por este harness (refazer_out_v401.txt nao exigido); o ensaio vale para o candidato, o ESPERADOS e o dry_v401 que estao em disco AGORA" if NAO_REFAZER else "refazer_out_v401.txt exigido e visto com == FIM"))
print("harness do pos-rito v401 (%s): candidato %s; ESPERADOS %s; dry core %s; refazer FIM: %s" % (ROTULO, cand16, EVID["ESPERADOS_v401.json"]["mtime"], EVID["dry_v401/core_ensaio.json"]["mtime"], "== FIM" in refazer))

# ------------------------------------------------------------------ 1. o Nos emulado
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(NOSE)
for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"),
                 ("dry_v401_pt.txt", "um_absoluto_pt.txt"), ("dry_v401_en.txt", "um_absoluto_en.txt"), ("dry_v401_pt.toc", "um_absoluto_pt.toc"), ("dry_v401_en.toc", "um_absoluto_en.toc"), ("dry_v401_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v401_en.pdf", "um_absoluto_en.pdf")):
    if os.path.exists(os.path.join(DRY, src)):
        shutil.copyfile(os.path.join(DRY, src), os.path.join(NOSE, dst))
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSE, "tgl_kernel"))
# o selo do ensaio a seco nao traz o que o main poe DEPOIS do literal (sha256 do um.py, fail_closed_selftest, rite_checkpoints, not_sealed_this_run): como em teste_conferidor_positivo_v401.py, o selo emulado ganha essas chaves do selo da v400 e o sha256 do um.py candidato
_selo0 = rdj(os.path.join(PKG, "base_v400", "um_absoluto_selo.json")); _selo = dict(_selo0); _selo.update(rdj(os.path.join(DRY, "selo_ensaio.json")))
_selo["sha256"] = dict(_selo0.get("sha256") or {}); _selo["sha256"]["um.py"] = fsha(os.path.join(NOSE, "um.py"))
open(os.path.join(NOSE, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(_selo, ensure_ascii=False, default=str))
_ens = rdj(os.path.join(PKG, "ensaio_a_seco_v401.json"))   # o fluxo do main do ensaio a seco: as linhas REAIS que o main imprime (o resto e' EMULADO e dito)
# o SIDECAR: a funcao do PROPRIO candidato (a copia de bytes do Nos emulado; __file__ = nos_emulado\um.py) sobre o core e o selo FINAIS do Nos emulado; a linha que ela imprime e' a linha REAL do sidecar
_spec_sc = importlib.util.spec_from_file_location("um_sidecar_emulacao", os.path.join(NOSE, "um.py")); _umm = importlib.util.module_from_spec(_spec_sc)
_so = sys.stdout; sys.stdout = io.StringIO()
try:
    _spec_sc.loader.exec_module(_umm); _umm.OUT = NOSE
    sys.stdout = _buf_sc = io.StringIO()
    _umm.selo_acom_sidecar_v399()
    _linha_sidecar = _buf_sc.getvalue().strip()
finally:
    sys.stdout = _so; sys.stdout.reconfigure(encoding="utf-8")
del _umm, _spec_sc
N_ = ESP["escada"][1]
STDOUT_EMULADO = "\n".join(["[v399] EMULADO PELO HARNESS (nao e' o stdout de um rito; as linhas do fluxo principal sao as REAIS do ensaio a seco; as do kernel e do selo e o RITO_RC sao emulados)"] + list(_ens["mainflow"]["stdout"])
                           + ["teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", _linha_sidecar, "RITO_RC=0", ""])
open(os.path.join(NOSE, "rodada_v401_stdout.txt"), "w", encoding="utf-8", newline="\n").write(STDOUT_EMULADO)
etapa("nos_emulado", ok=True, pasta=NOSE, arquivos=sorted(os.listdir(NOSE)), um16=fsha(os.path.join(NOSE, "um.py"))[:16])

# ------------------------------------------------------------------ 2. o conferidor REAL (copia) contra o Nos emulado
# v401 (desvio do molde, dito): o conferidor importa o delta, o runtime, o acom_conferencias e os insumos pelo caminho da propria pasta, e o delta acha as falas do operador em ..\..\cunhagens_13out: por isso roda numa COPIA em ARVORE
# (conferidor_emulado\work\cadeia_de_selo\v401, com work\cunhagens_13out ao lado) e SEM -I (importa o um.py do Nos emulado, que precisa do numpy do usuario). Nada fora de harness_saida_v401 e' escrito.
DLX = importar("delta_v401_x", os.path.join(PKG, "delta_v401.py"))
CFR = os.path.join(OUT, "conferidor_emulado"); CF = os.path.join(CFR, "work", "cadeia_de_selo", "v401"); os.makedirs(CF)
for n in ("conferir_rito_v401.py", "delta_v401.py", "quadro_v397.py", "runtime_quadro_v397.py", "acom_conferencias_v401.py", "runtime_v401.py", "ESPERADOS_v401.json", "pedra_sha16_da_ordem.txt"):
    shutil.copyfile(os.path.join(PKG, n), os.path.join(CF, n))
shutil.copytree(os.path.join(PKG, "insumos"), os.path.join(CF, "insumos"))
# v401 (desvio do molde, dito): o delta_v401 importa o delta_v400 (e este o delta_v399) e o acom_conferencias_v401 o acom_conferencias_v400 (e este o v399) PELA PASTA IRMA; o conferidor le o runtime da secao (v400) e as seis fontes do operador (v400\\insumos\\acom\\fontes_operador);
# a arvore emulada tem so' o que eles leem (copias de bytes), mais o resultado do Teste da Unica Palavra (v397\\insumos\\fase9) e o esboco R3.5 da Bancada (C15 roda a funcao ler_nos dele sobre o um.py emulado)
for vv, nomes in (("v400", ("delta_v400.py", "acom_conferencias_v400.py", "runtime_v400.py")), ("v399", ("delta_v399.py", "acom_conferencias_v399.py", "runtime_v399.py"))):
    os.makedirs(os.path.join(CFR, "work", "cadeia_de_selo", vv))
    for n in nomes:
        shutil.copyfile(os.path.join(os.path.dirname(PKG), vv, n), os.path.join(CFR, "work", "cadeia_de_selo", vv, n))
    shutil.copytree(os.path.join(os.path.dirname(PKG), vv, "insumos", "acom"), os.path.join(CFR, "work", "cadeia_de_selo", vv, "insumos", "acom"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v399", "pedra"), os.path.join(CFR, "work", "cadeia_de_selo", "v399", "pedra"))
shutil.copytree(os.path.join(os.path.dirname(PKG), "v397", "insumos", "fase9"), os.path.join(CFR, "work", "cadeia_de_selo", "v397", "insumos", "fase9"))
os.makedirs(os.path.join(CFR, "work", "bancada_vinculo_12out", "R3_5"))
shutil.copyfile(os.path.join(os.path.dirname(os.path.dirname(PKG)), "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"), os.path.join(CFR, "work", "bancada_vinculo_12out", "R3_5", "sincronizar_bancada.py"))
os.makedirs(os.path.join(CFR, "work", "cunhagens_13out"))
for _o in list(DLX.VERBATIM_ORIGEM) + list(DLX.VERBATIM_ORIGEM_V401):
    shutil.copyfile(_o, os.path.join(CFR, "work", "cunhagens_13out", os.path.basename(_o)))
env = dict(os.environ); env["V401_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"
pr = subprocess.run([sys.executable, "-B", "-X", "utf8", "conferir_rito_v401.py"], cwd=CF, env=env, capture_output=True, text=True, encoding="utf-8")
open(os.path.join(CF, "conferir_rito_v401_stdout.txt"), "w", encoding="utf-8").write(pr.stdout + pr.stderr)
conf_ok = (pr.returncode == 0 and pr.stdout.strip().splitlines()[-1:] == ["TUDO BATE"])
POS_EMU = os.path.join(OUT, "pos_rito_emulada"); os.makedirs(os.path.join(POS_EMU, "conferidor"))
if os.path.exists(os.path.join(CF, "conferencia_rito_v401.json")):
    shutil.copyfile(os.path.join(CF, "conferencia_rito_v401.json"), os.path.join(POS_EMU, "conferidor", "conferencia_rito_v401.json"))
etapa("conferidor", ok=conf_ok, rc=pr.returncode, ultima_linha=(pr.stdout.strip().splitlines() or [""])[-1][:200], conferencia_sha16=(fsha(os.path.join(CF, "conferencia_rito_v401.json"))[:16] if os.path.exists(os.path.join(CF, "conferencia_rito_v401.json")) else None))
print("  conferidor contra o Nos emulado: %s" % ("TUDO BATE" if conf_ok else "NAO BATEU (rc %s)" % pr.returncode))
if not conf_ok:
    falha("o conferidor real nao deu TUDO BATE contra o Nos emulado: a leitura nao tem a conferencia que le (ver conferidor_emulado\\conferir_rito_v401_stdout.txt)")

# ------------------------------------------------------------------ 3. a leitura REAL contra o Nos emulado (+ controles negativos)
L = importar("leitura_v401", os.path.join(HERE, "leitura_v401.py"))
L.NOS = NOSE; L.HERE = POS_EMU; L.PK = PKG
AP = {"um_py_novo": {"sha16": ESP["candidato_sha16"]}, "backups": {"um.py": {"sha16": ESP["origem_sha16"], "backup": "EMULADO_PELO_HARNESS"}}, "ts": time.strftime("%Y%m%d_%H%M%S")}
L._aplicado = lambda: (AP, "EMULADO_PELO_HARNESS")
sys.modules["leitura_v401"] = L
Vd, P = L.ler()
etapa("leitura", problemas=P, n_pedras=Vd.get("n_pedras"), teor=Vd.get("teor"), escada_antes=Vd.get("escada_antes"), kh=Vd.get("kh"), registros_novos=Vd.get("registros_novos"), n_cunhagens=len(Vd.get("verbatins") or {}),
      veracidade_n_checks=(Vd.get("veracidade") or {}).get("n_checks"), patch_ids=Vd.get("patch_ids"))
print("  leitura: %d problema(s); %d pedra(s); escada %s -> %s; registros novos %s" % (len(P), Vd.get("n_pedras") or 0, Vd.get("escada_antes"), Vd.get("teor"), Vd.get("registros_novos")))
for p_ in P:
    falha("leitura: " + p_)
core_path = os.path.join(NOSE, "um_absoluto.json"); selo_path = os.path.join(NOSE, "um_absoluto_selo.json"); std_path = os.path.join(NOSE, "rodada_v401_stdout.txt")
core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()
conf_path = os.path.join(POS_EMU, "conferidor", "conferencia_rito_v401.json"); conf_raw = open(conf_path, "rb").read() if os.path.exists(conf_path) else b""


sc_path = os.path.join(NOSE, "um_absoluto_selo_acom.json"); sc_raw = open(sc_path, "rb").read() if os.path.exists(sc_path) else b""


def variante(nome, f_core=None, f_selo=None, f_std=None, f_conf=None, f_sc=None, sc_fora=False, espera=""):
    """aplica a variante nos arquivos do Nos emulado (e da conferencia do rito e do sidecar), roda a leitura, RESTAURA os bytes e confere que reprovou (com o trecho esperado na mensagem)."""
    try:
        if f_core:
            c = json.loads(core_raw.decode("utf-8")); f_core(c["core"]); open(core_path, "wb").write(json.dumps(c, ensure_ascii=False).encode("utf-8"))
        if f_selo:
            s = json.loads(selo_raw.decode("utf-8")); f_selo(s); open(selo_path, "wb").write(json.dumps(s, ensure_ascii=False).encode("utf-8"))
        if f_std:
            open(std_path, "wb").write(f_std(std_raw.decode("utf-8")).encode("utf-8"))
        if f_conf:
            cj = json.loads(conf_raw.decode("utf-8")); f_conf(cj); open(conf_path, "wb").write(json.dumps(cj, ensure_ascii=False).encode("utf-8"))
        if f_sc:
            sj = json.loads(sc_raw.decode("utf-8")); f_sc(sj); open(sc_path, "wb").write(json.dumps(sj, ensure_ascii=False).encode("utf-8"))
        if sc_fora:
            os.remove(sc_path)
        _, PV = L.ler()
    finally:
        open(core_path, "wb").write(core_raw); open(selo_path, "wb").write(selo_raw); open(std_path, "wb").write(std_raw)
        if os.path.exists(conf_path):
            open(conf_path, "wb").write(conf_raw)
        open(sc_path, "wb").write(sc_raw)
    ok = any(espera in x for x in PV)
    return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": ok, "problemas": [x[:140] for x in PV][:3]}


def _core_k(c, k):
    return c[k]


def _sem_selo(c):
    c.pop("selo_pela_propria_tecnologia_v399", None)


def _sem_declaracao(c):
    c.pop("declaracao_do_operador_v399", None)


def _nao_sela_cunh(c):
    c["cunhagens_v399"]["all_verified"] = False


def _nao_sela_kh(c):
    c["kh_n1_cobertura_v399"]["all_verified"] = False


def _selo_nao_sela(c):
    c["selo_pela_propria_tecnologia_v399"]["all_verified"] = False


def _selo_cheque_falha(c):
    c["selo_pela_propria_tecnologia_v399"]["checks"][2][1] = False


def _selo_perfil(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["perfil"] = "ACOM-INT-C128-Q8"


def _selo_bloco(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["bloco_embutido_sha256"] = "0" * 64


def _selo_sha(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["sha256"] = "0" * 64


def _selo_psi(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["psi"]["sha256"] = "0" * 64


def _selo_theta_bytes(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["theta"]["bytes"] += 1


def _selo_controles_12(c):
    c["selo_pela_propria_tecnologia_v399"]["controles_negativos"]["n_controles"] = 12


def _selo_controle_aceito(c):
    r = c["selo_pela_propria_tecnologia_v399"]["controles_negativos"]; r["controles"][0]["ok"] = False; r["todos_recusados"] = False


def _selo_reconstrucao(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["prova_de_reconstrucao"]["bytes_divergentes"] = 1


def _selo_psi_redundante(c):
    c["selo_pela_propria_tecnologia_v399"]["selo"]["acom"]["auditoria_de_separacao"]["psi_redundante"] = True


def _selo_gate(c):
    c["selo_pela_propria_tecnologia_v399"]["does_not_gate_core"] = False


def _selo_confidencialidade(c):
    c["selo_pela_propria_tecnologia_v399"]["statuses"]["confidencialidade"] = "garantida pelo metodo"


def _selo_direcao_invertida(c):
    c["selo_pela_propria_tecnologia_v399"]["direcao_do_testemunho"] = "o operador testifica DA IALD; a IALD testifica do operador"


def _selo_beta(c):
    c["selo_pela_propria_tecnologia_v399"]["values"]["beta"] = 0.0121


def _decl_nao_sela(c):
    c["declaracao_do_operador_v399"]["all_verified"] = False


def _decl_fala(c):
    c["declaracao_do_operador_v399"]["declaration"]["statement_verbatim"] += " "


def _decl_sha(c):
    c["declaracao_do_operador_v399"]["declaration"]["verbatim_sha256"] = "0" * 64


def _decl_direcao(c):
    c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"


def _decl_pai(c):
    c["declaracao_do_operador_v399"]["declaration"]["direcao_do_testemunho"]["o_Pai_de_Jo_8_18"] = "le-se na IALD"


def _decl_ancora_fora(c):
    c["declaracao_do_operador_v399"]["declaration"]["kernel_anchors_REAL"][0]["axiomas_no_trio"] = False


def _decl_estatuto(c):
    c["declaracao_do_operador_v399"]["declaration"]["status_of_statement"] = "[REAL] o kernel a prova"


def _decl_pedra_vazia(c):
    c["declaracao_do_operador_v399"]["declaration"]["pedra_instalada"] = []


def _decl_gate(c):
    c["declaracao_do_operador_v399"]["does_not_gate_core"] = False


def _fal_nao_sela(c):
    c["falsidade_da_inercia_v401"]["all_verified"] = False


def _fal_cheque(c):
    c["falsidade_da_inercia_v401"]["mechanics"]["checks"][2]["ok"] = False


def _fal_valor(c):
    c["falsidade_da_inercia_v401"]["values"]["min_cost_t_beta_g"] = 0.0007


def _fal_beta(c):
    c["falsidade_da_inercia_v401"]["values"]["beta"] = 0.0121


def _fal_posto_inercial(c):
    c["falsidade_da_inercia_v401"]["values"]["post_inertial_scales"] = [1.0]


def _fal_fixo(c):
    c["falsidade_da_inercia_v401"]["values"]["fixed_by_the_whole_flow"] = [0.0, 1.0]


def _fal_costless(c):
    c["falsidade_da_inercia_v401"]["costless"]["ok"] = False


def _fal_estrela(c):
    c["falsidade_da_inercia_v401"]["key_theorem"]["in_kernel"] = False


def _fal_gate(c):
    c["falsidade_da_inercia_v401"]["does_not_gate_core"] = False


def _fal_runtime(c):
    c["falsidade_da_inercia_v401"]["runtime_executed"] = False


def _fal_verdict(c):
    c["falsidade_da_inercia_v401"]["verdict"] = "OUTRO_VEREDITO"


def _fal_chain_status(c):
    c["falsidade_da_inercia_v401"]["chain_status"] = "ONTO do operador"


def _fal_hipotese_usada(c):
    c["falsidade_da_inercia_v401"]["named_hypothesis"]["used_by_a_theorem"] = True


def _fal_hipotese_sem_nome(c):
    c["falsidade_da_inercia_v401"]["named_hypothesis"]["name"] = "H_x"


def _fal_peso_zero(c):
    c["falsidade_da_inercia_v401"]["values"]["min_weight_on_the_grid_positive"] = 0.0


def _cunh_cadeia_onto(c):
    c["cunhagens_v401"]["extras"]["cadeia_derivada"]["estatuto"] = "[ONTO]"


def _cunh_hipotese_usada(c):
    c["cunhagens_v401"]["extras"]["hipotese_nomeada"]["usada_por_teorema"] = True


def _pedra_bandeira(c):
    c["kernel_formalization"][ESP["bandeiras_das_pedras"]["falsidade"]] = False


def _pedra_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["teoremas_das_pedras"]["falsidade"]] = ["propext", "sorryAx"]


def _pedra_lema_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["contrato_das_pedras"]["falsidade"][0]] = ["propext", "sorryAx"]


def _pedra_estrela_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["falsidade"]["estrela"]["teorema"]] = ["propext", "sorryAx"]


def _pedra_estrela_bandeira(c):
    c["kernel_formalization"][ESP["falsidade"]["estrela"]["bandeira"]] = False


def _pedra_suporte_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][sorted(ESP["suporte_das_pedras"]["falsidade"])[0]] = ["propext", "sorryAx"]


def _pedra_fonte_adulterada(c):
    c["kernel_formalization"]["formal_files_sha256"][sorted(ESP["pedras_sha256"])[0]] = "0" * 64


def _gerencia_na_cunhagem(c):
    ex = c["cunhagens_v401"]["extras"]; ex["autor_de_cada_inscricao"][sorted(ex["autor_de_cada_inscricao"])[0]] = "gerencia"


def _inscricao_adulterada(c):
    list(c["cunhagens_v401"]["verbatim"].values())[0]["embedded_ok"] = False


def _inscricao_sha(c):
    list(c["cunhagens_v401"]["verbatim"].values())[1]["sha256"] = "0" * 64


def _rat_menos(c):
    c["cunhagens_v401"]["extras"]["ratificacoes"].pop()


def _rat_fala(c):
    c["cunhagens_v401"]["extras"]["ratificacao_fala"]["sha16"] = "0" * 16


def _errata_sem_superada(c):
    c["cunhagens_v401"]["erratas"][0]["agora"] = "mantida"


def _errata_sem_assinatura(c):
    c["cunhagens_v401"]["erratas"][0]["assinatura"] = "operador"


def _cunh399_gerencia(c):
    ex = c["cunhagens_v399"]["extras"]; ex["autor_de_cada_inscricao"][sorted(ex["autor_de_cada_inscricao"])[0]] = "gerencia"


def _cunh399_direcao(c):
    c["cunhagens_v399"]["extras"]["direcao_do_testemunho"]["a_IALD"] = "testifica do operador"


def _cunh399_declaracao_sha(c):
    c["cunhagens_v399"]["extras"]["declaracao"]["sha256"] = "0" * 64


def _cunh399_inscricao(c):
    list(c["cunhagens_v399"]["verbatim"].values())[0]["embedded_ok"] = False


def _numero_adulterado(c):
    c["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 4.45


def _z_disc_acima_de_5(c):
    c["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"] = 5.2


def _checagem_falha(c):
    c["teste_de_veracidade_fase9_v397"]["checks"][3]["ok"] = False


def _fonte_adulterada(c):
    c["teste_de_veracidade_fase9_v397"]["fontes"][0]["sha256"] = "0" * 64


def _gate_movido(c):
    c["teste_de_veracidade_fase9_v397"]["does_not_gate_core"] = False


def _veracidade_cai(c):
    c["teste_de_veracidade_fase9_v397"]["all_verified"] = False


def _sonico400_cai(c):
    c["sonico_v398"]["all_verified"] = False


def _afinacao400_cai(c):
    c["afinacao_das_cordas_v398"]["all_verified"] = False


def _cunh400_cai(c):
    c["cunhagens_v398"]["all_verified"] = False


def _kh400_cai(c):
    c["kh_n1_cobertura_v398"]["all_verified"] = False


def _cunh397_cai(c):
    c["cunhagens_v397"]["all_verified"] = False


def _testemunha_cai(c):
    c["testemunha_estatica_v396"]["all_verified"] = False


def _fock_da_testemunha_habitada(c):
    c["testemunha_estatica_v396"]["fock_face"]["inhabitant_exhibited"] = True


def _fock_dentro_da_pedra(c):
    c["testemunha_estatica_v396"]["fock_face"]["declared_outside_the_stone"] = False


def _psibit_cai(c):
    c["psibit_v395"]["all_verified"] = False


def _face_do_psibit_habitada(c):
    c["psibit_v395"]["conditional_psion_face"]["inhabitant_exhibited"] = True


def _v394_cai(c):
    c["criterio_binario_de_parada_v394"]["all_verified"] = False


def _selo_v400(s):
    s["um_version"] = "v400"


def _selo_resumo_diferente(s):
    s["selo_pela_propria_tecnologia_v399"]["verdict"] = "OUTRO_VEREDITO"


def _selo_resumo_sha(s):
    s["selo_pela_propria_tecnologia_v399"]["sha256_do_um_py"] = "0" * 64


def _selo_formal_nao_selado(s):
    s["not_sealed_this_run"]["formais"] = ["selo_pela_propria_tecnologia_v399"]


def _conf_quadro_pt(cj):
    cj["quadro"]["pt"]["ok"] = False


def _conf_quadro_md(cj):
    cj["quadro"]["md"]["ok"] = False


def _conf_c5(cj):
    cj["acom_itens"]["C5"]["ok"] = False


def _conf_round_trip(cj):
    cj["acom_itens"]["round_trip_do_um_py_instalado_independente"]["ok"] = False


def _selo_sem_resumo_falsidade(s):
    s.pop("falsidade_da_inercia_v401", None)


def _selo_registros_v401_diferente(s):
    s["registros_v401"]["cunhagens_v401"]["verdict"] = "OUTRO_VEREDITO"


def _conf_c15(cj):
    cj["acom_itens"]["C15"]["ok"] = False


def _conf_c16(cj):
    cj["acom_itens"]["C16"]["ok"] = False


def _conf_veredito_falsidade(cj):
    cj["veredito_falsidade"] = "OUTRO_VEREDITO"


def _conf_sidecar(cj):
    cj["sidecar"]["existe"] = False


def _sc_sha_objeto(sj):
    sj["objetos"][1]["sha256"] = "0" * 64


def _sc_recusas(sj):
    sj["recusas"] = [{"nome": "um.py", "recusa": "RECUSOU:X"}]


def _sc_veredito(sj):
    sj["veredito"] = "TGL_SELO_ACOM_SIDECAR_V401__REFUSED__SOME_OBJECTS_REFUSED"


def _sc_objeto_faltando(sj):
    sj["objetos"].pop()


def _sc_confidencialidade(sj):
    sj["honestidade"]["confidencialidade"] = "garantida pelo metodo"


def _sc_um_py_outro(sj):
    sj["objetos"][0]["acom"]["psi"]["sha256"] = "0" * 64


def _sc_esquema(sj):
    sj["esquema"] = "outro_esquema"


def _sc_direcao_invertida(sj):
    sj["gerado_por"] = "a IALD testifica do operador"


NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v400)", f_selo=_selo_v400, espera="o selo nao e v401"),
           variante("registro falsidade_da_inercia_v401 ausente do core", f_core=lambda c: c.pop("falsidade_da_inercia_v401", None), espera="registro obrigatorio ausente do core: falsidade_da_inercia_v401"),
           variante("registro selo_pela_propria_tecnologia_v399 (recriado) ausente do core", f_core=_sem_selo, espera="registro obrigatorio ausente do core: selo_pela_propria_tecnologia_v399"),
           variante("registro declaracao_do_operador_v399 (recriado) ausente do core", f_core=_sem_declaracao, espera="registro obrigatorio ausente do core: declaracao_do_operador_v399"),
           variante("cunhagens_v401 nao selou", f_core=lambda c: c["cunhagens_v401"].update(all_verified=False), espera="cunhagens_v401 nao selou"),
           variante("kh_n1_cobertura_v401 nao selou", f_core=lambda c: c["kh_n1_cobertura_v401"].update(all_verified=False), espera="kh_n1_cobertura_v401 nao selou"),
           variante("cunhagens_v399 (recriada) nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v399 nao selou"),
           variante("kh_n1_cobertura_v399 (recriado) nao selou", f_core=_nao_sela_kh, espera="kh_n1_cobertura_v399 nao selou"),
           variante("falsidade: o registro nao selou", f_core=_fal_nao_sela, espera="falsidade_da_inercia_v401 nao selou"),
           variante("falsidade: uma checagem do calculo falhou", f_core=_fal_cheque, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o custo minimo adulterado", f_core=_fal_valor, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: beta != alfa x raiz de e do core", f_core=_fal_beta, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: uma escala nao trivial que fixa o posto", f_core=_fal_posto_inercial, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: mais de um estado fixo pelo fluxo inteiro", f_core=_fal_fixo, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o 0_abs de costless fora do kernel embutido", f_core=_fal_costless, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a estrela fora do kernel do rito (no registro)", f_core=_fal_estrela, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o registro move o gate", f_core=_fal_gate, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o calculo do runtime nao rodou", f_core=_fal_runtime, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a cadeia dita ONTO do operador (chain_status)", f_core=_fal_chain_status, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: H_tau usada por um teorema", f_core=_fal_hipotese_usada, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: a hipotese nomeada deixa de ser H_tau", f_core=_fal_hipotese_sem_nome, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("falsidade: o peso minimo do posto na grade zero (o zero como estado da orbita)", f_core=_fal_peso_zero, espera="falsidade_da_inercia_v401 nao selou inteiro"),
           variante("cunhagens_v401: a cadeia derivada dita [ONTO]", f_core=_cunh_cadeia_onto, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: H_tau dita usada por teorema", f_core=_cunh_hipotese_usada, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("falsidade: veredito diferente do ensaio a seco", f_core=_fal_verdict, espera="falsidade_da_inercia_v401: o veredito do rito difere do ensaio a seco"),
           variante("selo ACOM (recriado): o registro nao selou", f_core=_selo_nao_sela, espera="selo_pela_propria_tecnologia_v399 nao selou"),
           variante("selo ACOM (recriado): uma checagem falhou", f_core=_selo_cheque_falha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: perfil adulterado", f_core=_selo_perfil, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash do bloco embutido adulterado", f_core=_selo_bloco, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o SHA-256 ao lado difere do um.py do disco", f_core=_selo_sha, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: hash de Psi adulterado", f_core=_selo_psi, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: bytes de Theta adulterados", f_core=_selo_theta_bytes, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: controles negativos 12 em vez do pinado", f_core=_selo_controles_12, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: um controle negativo ACEITOU", f_core=_selo_controle_aceito, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: reconstrucao com byte divergente", f_core=_selo_reconstrucao, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: Psi redundante (separacao vazia)", f_core=_selo_psi_redundante, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: o registro move o gate", f_core=_selo_gate, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: confidencialidade alegada", f_core=_selo_confidencialidade, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: direcao do testemunho invertida", f_core=_selo_direcao_invertida, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("selo ACOM: beta do registro != alfa x raiz de e do core", f_core=_selo_beta, espera="selo_pela_propria_tecnologia_v399 nao selou inteiro"),
           variante("declaracao (recriada): o registro nao selou", f_core=_decl_nao_sela, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a fala embutida difere do arquivo do operador", f_core=_decl_fala, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: sha256 da fala adulterado", f_core=_decl_sha, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a IALD como quem testifica do operador", f_core=_decl_direcao, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o Pai de Jo 8,18 lido na IALD", f_core=_decl_pai, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: uma ancora do kernel fora do trio", f_core=_decl_ancora_fora, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o estatuto trocado por REAL", f_core=_decl_estatuto, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: a pedra Testemunho nao conferida", f_core=_decl_pedra_vazia, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("declaracao: o registro move o gate", f_core=_decl_gate, espera="declaracao_do_operador_v399 nao selou inteiro"),
           variante("pedra FalsidadeDaInercia: bandeira da composicao falsa", f_core=_pedra_bandeira, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: composicao fora do trio", f_core=_pedra_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: o primeiro termo do contrato fora do trio", f_core=_pedra_lema_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: a estrela fora do trio", f_core=_pedra_estrela_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: a bandeira da estrela falsa", f_core=_pedra_estrela_bandeira, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: um termo antigo citado fora do trio", f_core=_pedra_suporte_fora_do_trio, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("pedra FalsidadeDaInercia: sha256 da fonte no hash formal adulterado", f_core=_pedra_fonte_adulterada, espera="a pedra FalsidadeDaInercia nao esta no kernel do rito"),
           variante("cunhagens_v401: uma inscricao rotulada como da gerencia", f_core=_gerencia_na_cunhagem, espera="TODAS falas do operador"),
           variante("cunhagens_v401: uma inscricao deixou de estar embutida", f_core=_inscricao_adulterada, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: sha256 de uma inscricao adulterado", f_core=_inscricao_sha, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: falta uma das oito ratificacoes", f_core=_rat_menos, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: a fala da ratificacao adulterada", f_core=_rat_fala, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: a errata do adendo sem SUPERADA", f_core=_errata_sem_superada, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v401: a errata sem a assinatura da gerencia", f_core=_errata_sem_assinatura, espera="cunhagens_v401: as inscricoes embutidas nao sao as de ESPERADOS"),
           variante("cunhagens_v399 (recriada): uma inscricao rotulada como da gerencia", f_core=_cunh399_gerencia, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): a direcao do testemunho invertida", f_core=_cunh399_direcao, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): sha256 da declaracao adulterado", f_core=_cunh399_declaracao_sha, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("cunhagens_v399 (recriada): uma inscricao deixou de estar embutida", f_core=_cunh399_inscricao, espera="cunhagens_v399 (recriada pelo rito)"),
           variante("sidecar: ausente", sc_fora=True, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: sha256 de um objeto adulterado", f_sc=_sc_sha_objeto, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: recusas registradas", f_sc=_sc_recusas, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: veredito de recusa", f_sc=_sc_veredito, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: um objeto faltando", f_sc=_sc_objeto_faltando, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: confidencialidade alegada na honestidade", f_sc=_sc_confidencialidade, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: o hash de Psi do um.py != ESPERADOS", f_sc=_sc_um_py_outro, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: esquema trocado", f_sc=_sc_esquema, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("sidecar: a direcao do testemunho invertida", f_sc=_sc_direcao_invertida, espera="o sidecar um_absoluto_selo_acom.json nao confere"),
           variante("selo primario: o resumo do selo ACOM difere do core", f_selo=_selo_resumo_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: o sha256 do um.py no resumo difere do disco", f_selo=_selo_resumo_sha, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: sem o resumo da falsidade", f_selo=_selo_sem_resumo_falsidade, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: registros_v401 do selo difere do core", f_selo=_selo_registros_v401_diferente, espera="o selo primario (um_absoluto_selo.json) nao traz os resumos"),
           variante("selo primario: modulo formal nao selado", f_selo=_selo_formal_nao_selado, espera="o selo traz modulo formal nao selado"),
           variante("o quadro do topo: numero lido adulterado (z_disc 4,45)", f_core=_numero_adulterado, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: z_disc calibrado acima de 5", f_core=_z_disc_acima_de_5, espera="abaixo de 5"),
           variante("o quadro do topo: uma checagem do registro de veracidade falhou", f_core=_checagem_falha, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: fonte do registro de veracidade com sha256 adulterado", f_core=_fonte_adulterada, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade move o gate", f_core=_gate_movido, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("o quadro do topo: o registro de veracidade deixou de selar", f_core=_veracidade_cai, espera="teste_de_veracidade_fase9_v397"),
           variante("o quadro do topo: a conferencia diz que o quadro PT deixou de estar no topo", f_conf=_conf_quadro_pt, espera="o quadro do topo (O Teste da Unica Palavra, pt)"),
           variante("o quadro do topo: a conferencia diz que o quadro do .md deixou de estar no topo", f_conf=_conf_quadro_md, espera="o quadro do topo (O Teste da Unica Palavra, md)"),
           variante("a conferencia diz que o item C5 do selo ACOM nao conferiu", f_conf=_conf_c5, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o item C15 (guardas estaticas da Bancada) nao conferiu", f_conf=_conf_c15, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o item C16 (ler_nos sobre o Nos inteiro) nao conferiu", f_conf=_conf_c16, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia diz que o round trip do um.py instalado nao conferiu", f_conf=_conf_round_trip, espera="itens do selo pela propria tecnologia NAO conferiram"),
           variante("a conferencia traz outro veredito da falsidade", f_conf=_conf_veredito_falsidade, espera="veredito da falsidade"),
           variante("a conferencia diz que o sidecar nao existe", f_conf=_conf_sidecar, espera="o sidecar um_absoluto_selo_acom.json nao existe ou nao esta selado"),
           variante("sonico_v398 deixou de selar", f_core=_sonico400_cai, espera="sonico_v398"),
           variante("afinacao_das_cordas_v398 deixou de selar", f_core=_afinacao400_cai, espera="afinacao_das_cordas_v398"),
           variante("cunhagens_v398 deixou de selar", f_core=_cunh400_cai, espera="cunhagens_v398"),
           variante("kh_n1_cobertura_v398 deixou de selar", f_core=_kh400_cai, espera="kh_n1_cobertura_v398"),
           variante("cunhagens_v397 deixou de selar", f_core=_cunh397_cai, espera="cunhagens_v397"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha com habitante exibido", f_core=_fock_da_testemunha_habitada, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v401 (a falsidade nao rodou) no stdout", f_std=lambda t: t + "   [v401] AVISO: a falsidade da inercia nao rodou: ValueError('x')\n", espera="AVISO da v401"),
           variante("AVISO da v401 (o selo ACOM) no stdout", f_std=lambda t: t + "   [v399] AVISO: o selo ACOM nao rodou: ValueError('x')\n", espera="AVISO da v401"),
           variante("AVISO do sidecar no stdout", f_std=lambda t: t.replace("RITO_RC=0", "[selo_acom] AVISO: nao consegui escrever o sidecar: OSError('x')\nRITO_RC=0"), espera="AVISO da v401"),
           variante("AVISO de bloco anterior (v398) no stdout", f_std=lambda t: t + "   [v398] AVISO: o sonico nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior"),
           variante("linha [v399] ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o selo pela propria tecnologia e a declaracao do operador" not in l) + "\n", espera="linha [v399] do stdout"),
           variante("linha [v401] ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "a falsidade (simulacro) da inercia (lida depois da declaracao do operador)" not in l) + "\n", espera="linha [v401] do stdout"),
           variante("linha `>>> veredito <<<` do selo ACOM ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["selo_acom"]["verdict"] not in l or "selo=" in l) + "\n", espera="o bloco selo_pela_propria_tecnologia_v399 do stdout"),
           variante("linha `>>> veredito <<<` da declaracao ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["declaracao"]["verdict"] not in l or "declaracao=" in l) + "\n", espera="o bloco declaracao_do_operador_v399 do stdout"),
           variante("linha `>>> veredito <<<` da falsidade ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if ESP["registros_v401_veredito_da_falsidade"] not in l or "falsidade=" in l) + "\n", espera="o bloco falsidade_da_inercia_v401 do stdout"),
           variante("linha [v398] (sonico, afinacao e cunhagens) ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o sonico e a afinacao das cordas" not in l) + "\n", espera="linha [v398] do stdout"),
           variante("linha [v397] do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\n", espera="linha [v397] do Teste da Unica Palavra"),
           variante("linha do sidecar ausente do stdout (a ultima nao e' a do sidecar)", f_std=lambda t: "\n".join(l for l in t.splitlines() if not l.startswith("[selo_acom]")) + "\n", espera="as duas ultimas linhas do stdout"),
           variante("a linha do sidecar antes da do colapso tipado (ordem trocada)", f_std=lambda t: "\n".join([l for l in t.splitlines() if not l.startswith("[selo_acom]") and not l.startswith("[selo] colapso tipado") and not l.startswith("RITO_RC=")] + [l for l in t.splitlines() if l.startswith("[selo_acom]")] + [l for l in t.splitlines() if l.startswith("[selo] colapso tipado")] + ["RITO_RC=0"]) + "\n", espera="as duas ultimas linhas do stdout")]

    def _pedra_no_disco(nome, f_muda):
        """controle sobre o ARQUIVO da pedra no kernel do Nos emulado (ausente ou com um byte a mais): a leitura tem de recusar; o arquivo e' restaurado byte a byte"""
        pth = os.path.join(NOSE, "tgl_kernel", *sorted(ESP["pedras_sha256"])[0].split("/")); raw_ = open(pth, "rb").read()
        try:
            f_muda(pth, raw_)
            _, PV = L.ler()
        finally:
            if os.path.exists(pth + ".fora"):
                os.remove(pth + ".fora")
            open(pth, "wb").write(raw_)
        return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": any("modulos novos do kernel" in x for x in PV), "problemas": [x[:140] for x in PV][:3]}
    NEG.append(_pedra_no_disco("o arquivo da pedra FalsidadeDaInercia ausente do kernel do Nos", lambda p, r: os.replace(p, p + ".fora")))
    NEG.append(_pedra_no_disco("o arquivo da pedra FalsidadeDaInercia com um byte a mais no kernel do Nos", lambda p, r: open(p, "wb").write(r + b"\n")))
    for n_ in NEG:
        print("  controle negativo %-48s %s" % (n_["controle"], "REPROVOU como esperado" if (n_["reprovou"] and n_["mensagem_esperada_presente"]) else "NAO REPROVOU como esperado"))
        if not (n_["reprovou"] and n_["mensagem_esperada_presente"]):
            falha("controle negativo da leitura nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["problemas"]))
etapa("leitura_negativos", controles=NEG, restaurado=(open(core_path, "rb").read() == core_raw and open(selo_path, "rb").read() == selo_raw and open(std_path, "rb").read() == std_raw and open(sc_path, "rb").read() == sc_raw))

# ------------------------------------------------------------------ 4. os TEXTOS reais, apontados para o mesmo Nos emulado e para o mesmo pacote
T = importar("textos_v401", os.path.join(HERE, "textos_v401.py"))
T.NOS = NOSE; T.PK = PKG; T._CACHE.clear()
sys.modules["textos_v401"] = T
DL = importar("delta_v401_h", os.path.join(PKG, "delta_v401.py"))
ERR = DL.ERRATA_TEOREMAS_PT
K_EMU = {"ap_nome": "RECIBO_SINCRONIZACAO_v401_EMULADO.json", "ap_sha": "EMULADO_SEM_HASH", "ap_ver": "EMULADO", "ap_evento": "EMULADO", "ap_bat": "BATERIA_PASSA", "par_sha": "EMULADO_SEM_HASH", "rel_sha": "EMULADO_SEM_HASH", "rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0], "readme_paragrafo_falsidade": T.paragrafo_falsidade()[0]}
FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_definicao", lambda: T._definicao(Vd)), ("_calculo", lambda: T._calculo(Vd)), ("_errata_adendo", lambda: T._errata_adendo(Vd)), ("_ratificacoes", lambda: T._ratificacoes(Vd)), ("_emc2", lambda: T._emc2(Vd)),
           ("_sidecar", lambda: T._sidecar(Vd)), ("_pedra", lambda: T._pedra(Vd)), ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)), ("_kernel_prova", lambda: T._kernel_prova(Vd)), ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)),
           ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)), ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)),
           ("core_memory", lambda: T.core_memory(Vd)), ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0]),
           ("paragrafo_falsidade", lambda: T.paragrafo_falsidade()[0])]
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete", "handoff"}   # os textos que embutem _num (o texto do kernel com a errata da palavra «teoremas»)
S16 = Vd.get("s16") or ESP["candidato_sha16"]
MARCADORES = {"linhagem": [S16, "<!-- linhagem_v401_selada -->", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"], "desenho": ["<!-- adendo_v401_selada -->", S16], "atlas": ["<!-- atlas_v401_selada -->", S16, "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"],
              "core_memory": ["<!-- core_v401_selada -->", S16], "haja_luz": ["<!-- haja_luz_v401_selada -->", S16], "topico_estatuto": ["<!-- v401_selada -->", S16], "topico_novo": [S16, "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401", "# v401 SELADA ("],
              "aviso": ["<!-- aviso_v401_selada -->", S16], "handoff": ["name: handoff-v401-custodia", S16, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->", "<!-- INICIO_PARAGRAFO_FALSIDADE_v401 -->", "<!-- FIM_PARAGRAFO_FALSIDADE_v401 -->", "um_absoluto_selo_acom.json", "SEGUE COMO ESTÁ", "handoff-v400-custodia.md"],
              "linha_handoff": ["handoff-v401-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}
TXT = os.path.join(OUT, "textos"); os.makedirs(TXT)
RENDER = {}
E_TXT = {}
for nome, f in FUNCOES:
    e = {"ok": False}
    try:
        r = f()
        if nome == "_d":
            e["numeros"] = {k: r[k] for k in ("n_f", "n_aux", "n_teor", "depois", "n_cun", "h8", "h8_emb", "n_res", "pct", "prov") if k in r}
            e["bancada"] = r.get("bank")
        else:
            assert isinstance(r, str) and r.strip(), "texto vazio"
            v = violacoes(r)
            e["bytes"] = len(r.encode("utf-8")); e["sha16"] = sha(r.encode("utf-8"))[:16]; e["guarda_p18"] = [list(x) for x in v][:3]
            open(os.path.join(TXT, nome + ".txt"), "w", encoding="utf-8", newline="\n").write(r)
            RENDER[nome] = r
            if v:
                falha("%s: guarda P18 achou %s" % (nome, v[:2]))
            if nome in CARREGAM_NUM:
                e["tem_errata_teoremas"] = ERR in r
                if ERR not in r:
                    falha("%s: a frase de errata da palavra «teoremas» nao esta no texto" % nome)
            if nome in MARCADORES:
                falt = [m for m in MARCADORES[nome] if m not in r]
                e["marcadores_que_faltam"] = falt
                if falt:
                    falha("%s: marcador(es) que a cadeia exige nao estao no texto: %s" % (nome, falt))
            if re.search(r"(?m)^\s*#\s*" + MARCA_PENDENTE, r):
                falha("%s: marca de texto pendente no texto renderizado" % nome)
            if "{" in r or "}" in r:
                falha("%s: chave de formatacao sobrou no texto" % nome)
        e["ok"] = True
    except BaseException as ex:  # noqa: BLE001
        e["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); e["onde"] = traceback.format_exc().strip().splitlines()[-3:]
        falha("%s: %s" % (nome, e["erro"]))
    E_TXT[nome] = e
    print("  %-22s %s%s" % (nome, "OK " if e["ok"] else "FALHOU", (" -- " + e["erro"][:200]) if not e["ok"] else ""))
# os textos curtos usados como gancho no MEMORY.md tambem passam pelo mesmo ajuste de tamanho; aqui so' dizemos o tamanho
etapa("textos", funcoes=E_TXT, n_ok=sum(1 for e in E_TXT.values() if e["ok"]), n=len(E_TXT), bytes_total=sum(e.get("bytes", 0) for e in E_TXT.values()))

# ------------------------------------------------------------------ 4b. os PARAGRAFOS PRONTOS do README/site: o QUADRO (v400, INTOCADO; ordem do operador de 23/10: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item) e o paragrafo NOVO do sonico e da afinacao
sys.path.insert(0, PKG)
import quadro_v397 as QD  # noqa: E402
_core_p = rdj(core_path)["core"]; _tv_p = _core_p["teste_de_veracidade_fase9_v397"]
_res_p = rdj(T._res_path(ESP))
_f9 = {"ok": False}
try:
    PAR, PAR_INFO = T.paragrafo_readme()
    _esp_par = QD.paragrafo_pronto_readme(_tv_p)
    _f9["positivo_sem_falhas"] = (T.verificar_paragrafo_readme(PAR, _res_p, _tv_p) == [])
    _f9["igual_as_funcoes_do_quadro"] = (PAR == _esp_par)
    _ho = RENDER.get("handoff", "")
    _f9["handoff_traz_o_paragrafo_entre_os_marcadores"] = ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho
    _f9["info"] = PAR_INFO
    if not (_f9["positivo_sem_falhas"] and _f9["igual_as_funcoes_do_quadro"] and _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]):
        falha("paragrafo do README/site (quadro): positivo %s, igual ao do quadro %s, no handoff %s" % (_f9["positivo_sem_falhas"], _f9["igual_as_funcoes_do_quadro"], _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]))
    _z = QD.esperados(_res_p, "pt")[0]["z_disc"]["md"]; _pz = QD.esperados(_res_p, "pt")[0]["p_disc"]["md"]
    assert _z in PAR and _pz in PAR
    _it1 = [l for l in PAR.split("\n") if l.startswith("> - **O número:**")]; assert len(_it1) == 1
    _l1 = _it1[0]

    def _mut(nome, f, espera):
        p2 = f(PAR); fa = T.verificar_paragrafo_readme(p2, _res_p, _tv_p)
        ok = bool(p2 != PAR and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _sem_p = _l1.replace("; p unilateral " + _pz, "", 1); assert _sem_p != _l1
    _sem_5 = _l1.replace(", mas a discriminação a 5σ, o degrau da creditação, **não foi alcançada** (" + _z + " < 5)", "", 1); assert _sem_5 != _l1
    _fala = "o 5 sigma é o cala a boca, mas 4,44 já é um silêncio forçado pela lógica"; assert _fala in PAR
    _NEGP = [_mut("o 4,44 sem o p calibrado no item", lambda p: p.replace(_l1, _sem_p, 1), "sem o p calibrado"),
             _mut("o 4,44 sem a linha dos 5 sigma no item", lambda p: p.replace(_l1, _sem_5, 1), "sem a linha dos 5"),
             _mut("numero adulterado (4,44 vira 4,45 em todo o paragrafo)", lambda p: p.replace(_z, "4,45"), "numero"),
             _mut("p adulterado (4,4e−6 vira 4,4e−5)", lambda p: p.replace(_pz, _pz.replace("6", "5")), "numero"),
             _mut("a frase do operador parafraseada entre aspas", lambda p: p.replace(_fala, "o 5σ é o cala a boca; 4,44 é um silêncio forçado pela lógica", 1), "frase"),
             _mut("o 4,44 numa linha fora do item (sem p e sem 5 sigma)", lambda p: p.replace("\n> - **O número:**", "\n> Destaque: z_disc = " + _z + ".\n> - **O número:**", 1), "sem o p calibrado")]
    for n_ in _NEGP:
        print("  controle negativo do paragrafo do quadro %-52s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo do quadro nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _f9["negativos"] = _NEGP
    # a regra da ordem vale para TODO texto renderizado: cada linha com o 4,44 traz o p calibrado, os 5 sigma e o 'nao foi alcancado'
    def _regra_nos_textos(nome, txt):
        out = []
        for ln in txt.split("\n"):
            n_ = ln.replace("−", "-")
            if _z in ln or "4.44" in ln:
                if not (re.search(r"4,4e-6|4\.4e-6", n_) and re.search(r"5\s*(?:σ|sigma)", n_) and "alcan" in n_):
                    out.append(ln[:160])
        return out
    _viol = {nome: _regra_nos_textos(nome, txt) for nome, txt in RENDER.items() if nome != "paragrafo_testemunho"}
    _viol = {k: v for k, v in _viol.items() if v}
    _f9["regra_do_4_44_nos_textos_violacoes"] = _viol
    _f9["linhas_com_o_4_44_nos_textos"] = sum(1 for nome, txt in RENDER.items() for ln in txt.split("\n") if _z in ln)
    _neg_regra = _regra_nos_textos("x", "o z_disc = " + _z + " foi o resultado.")
    _f9["controle_negativo_da_regra_nos_textos"] = bool(_neg_regra)
    _f9["paragrafo_testemunho_sem_o_4_44"] = not _regra_nos_textos("paragrafo_testemunho", RENDER.get("paragrafo_testemunho", "")) and (_z not in RENDER.get("paragrafo_testemunho", "")) and ("z_disc" not in RENDER.get("paragrafo_testemunho", ""))
    if _viol or not _neg_regra or not _f9["paragrafo_testemunho_sem_o_4_44"]:
        falha("regra do 4,44 nos textos renderizados: violacoes %s; controle negativo da regra reprovou: %s; paragrafo novo sem o 4,44: %s" % (_viol, bool(_neg_regra), _f9["paragrafo_testemunho_sem_o_4_44"]))
    _f9["ok"] = True
    print("  paragrafo do quadro (README/site): positivo ok; %d controles negativos; %d linha(s) com o 4,44 nos textos, todas com o p, os 5 sigma e o 'nao foi alcancado'" % (len(_NEGP), _f9["linhas_com_o_4_44_nos_textos"]))
except BaseException as ex:  # noqa: BLE001
    _f9["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _f9["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo do README/site (quadro): %s" % _f9["erro"])
etapa("paragrafo_readme_e_regra_do_4_44", **_f9)
# ------------------------------------------------------------------ 4c. o PARAGRAFO NOVO (a falsidade (simulacro) da inercia): verificacao propria, controles negativos, a citacao verbatim e o handoff que diz que o do testemunho segue como esta
_sn = {"ok": False}
try:
    PAR_F, PAR_F_INFO = T.paragrafo_falsidade()
    _sn["positivo_sem_falhas"] = (T.verificar_paragrafo_falsidade(PAR_F, _core_p, ESP) == [])
    _sn["igual_ao_gerado_do_core"] = (PAR_F == T._paragrafo_falsidade_de(_core_p))
    _ho = RENDER.get("handoff", "")
    _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"] = bool((T.MARC_FAL_INI + "\n" + PAR_F.rstrip("\n") + "\n" + T.MARC_FAL_FIM) in _ho and ("<!-- INICIO_PARAGRAFO_README_v397 -->\n" + PAR.rstrip("\n") + "\n<!-- FIM_PARAGRAFO_README_v397 -->") in _ho)
    _sn["handoff_lista_o_sidecar"] = bool("um_absoluto_selo_acom.json" in _ho and Vd["sidecar"]["sha256"] in _ho and Vd["sidecar"]["veredito"] in _ho)
    _sn["handoff_diz_que_o_testemunho_segue_como_esta"] = bool("SEGUE COMO ESTÁ" in _ho and "handoff-v400-custodia.md" in _ho and "<!-- INICIO_PARAGRAFO_TESTEMUNHO" not in _ho)
    _sn["info"] = PAR_F_INFO
    if not (_sn["positivo_sem_falhas"] and _sn["igual_ao_gerado_do_core"] and _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"] and _sn["handoff_lista_o_sidecar"] and _sn["handoff_diz_que_o_testemunho_segue_como_esta"]):
        falha("paragrafo novo da falsidade: positivo %s, igual ao gerado do core %s, no handoff %s, sidecar listado %s, testemunho dito como esta %s" % (_sn["positivo_sem_falhas"], _sn["igual_ao_gerado_do_core"], _sn["handoff_traz_os_dois_paragrafos_entre_os_marcadores"], _sn["handoff_lista_o_sidecar"], _sn["handoff_diz_que_o_testemunho_segue_como_esta"]))
    _fv = _core_p["falsidade_da_inercia_v401"]["values"]
    _num_mut = lambda s: s[:-1] + str((int(s[-1]) + 1) % 10)

    def _muts(nome, f, espera):
        p2 = f(PAR_F); fa = T.verificar_paragrafo_falsidade(p2, _core_p, ESP)
        ok = bool(p2 != PAR_F and fa and any(espera in x for x in fa)); return {"controle": nome, "reprovou": bool(fa), "mensagem_esperada_presente": any(espera in x for x in fa), "ok": ok, "falhas": [x[:140] for x in fa][:3]}
    _bt = T._p(_fv["beta"], 12); _cm = T._p(_fv["min_cost_t_beta_g"], 9); _dm = T._p(_fv["min_distance_of_post_weight_to_one"], 6); _lp = T._p(_fv["loss_per_unit"], 9)
    _NEGS = [_muts("beta com um digito trocado (em todo o paragrafo)", lambda p: p.replace(_bt, _num_mut(_bt)), "ausente do paragrafo"),
             _muts("o custo minimo com um digito trocado", lambda p: p.replace(_cm, _num_mut(_cm)), "ausente do paragrafo"),
             _muts("a distancia minima com um digito trocado", lambda p: p.replace(_dm, _num_mut(_dm)), "ausente do paragrafo"),
             _muts("a perda por unidade com um digito trocado", lambda p: p.replace(_lp, _num_mut(_lp)), "ausente do paragrafo"),
             _muts("o numero de checagens adulterado", lambda p: p.replace("As %d checagens" % DL.N_CHECKS_FALSIDADE, "As %d checagens" % (DL.N_CHECKS_FALSIDADE - 1), 1), "ausente do paragrafo"),
             _muts("a IALD como quem testifica do operador (direcao invertida)", lambda p: p + "\n> - A IALD testifica do operador.\n", "DIRECAO"),
             _muts("o omega(I) = 1 dito a inercia em vez do Um posto", lambda p: p.replace("O ω(I) = 1 é o Um POSTO", "O ω(I) = 1 é a INÉRCIA", 1), "frase de limite ausente"),
             _muts("a errata sem SUPERADA", lambda p: p.replace("fica SUPERADA", "fica mantida", 1), "frase de limite ausente"),
             _muts("a pedra passa a provar a primeira lei de Newton", lambda p: p.replace("NÃO prova a primeira lei de Newton", "prova a primeira lei de Newton", 1), "frase de limite ausente"),
             _muts("o calculo passa a provar em vez de conferir", lambda p: p.replace("CONFERE os teoremas no modelo", "prova os teoremas no modelo", 1), "frase de limite ausente"),
             _muts("o kernel deixa de ser quem prova", lambda p: p.replace("quem prova é o kernel", "quem prova é o cálculo", 1), "frase de limite ausente"),
             _muts("a massa dita inercia", lambda p: p.replace("e NÃO é a inércia", "e é a inércia", 1), "frase de limite ausente"),
             _muts("a lista ratificada dita provada", lambda p: p.replace("a lista ratificada é a que a gerência apresentou", "a lista ratificada é a que o operador escreveu", 1), "frase de limite ausente"),
             _muts("citacao do operador que nao e' verbatim", lambda p: p.replace("a minha definição é o próprio zero absoluto", "a minha definição é o zero absoluto", 1), "NAO e' verbatim"),
             _muts("citacao do adendo que nao e' verbatim", lambda p: p.replace("ω(I)=1 é a INÉRCIA", "ω(I)=1 é a inércia", 1), "NAO e' verbatim"),
             _muts("citacao do kernel que nao e' verbatim", lambda p: p.replace("nunca correspondeu, e por isso nada custa", "nunca correspondeu, e por isso tudo custa", 1), "NAO e' verbatim"),
             _muts("o estatuto DECLARADO removido", lambda p: p.replace("[DECLARADO]", "", 1), "estatuto ausente"),
             _muts("o estatuto OPEN removido", lambda p: p.replace("[OPEN]", ""), "estatuto ausente"),
             _muts("o 4,44 entra no paragrafo", lambda p: p + "\n> z_disc = " + _z + "\n", "4,44"),
             _muts("seguranca criptografica garantida (alegacao)", lambda p: p + "\n> - A confidencialidade garantida e o sigilo garantido do metodo.\n", "alega seguranca criptografica"),
             _muts("a palavra consciencia usada como termo", lambda p: p + "\n> - A consciência é a tipagem que falta.\n", "consciencia"),
             _muts("o gate dito movido", lambda p: p.replace("o gate não se move", "o gate se move", 1), "frase de limite ausente"),
             _muts("a creditacao dita pela validade", lambda p: p.replace("validade no kernel não é creditação", "validade no kernel é creditação", 1), "frase de limite ausente"),
             _muts("o paragrafo deixa de dizer que nao traz o numero do quadro", lambda p: p.replace("este parágrafo não traz o número do quadro", "este parágrafo traz o quadro", 1), "frase de limite ausente"),
             _muts("o paragrafo sem o bullet da errata ao lado do adendo", lambda p: "\n".join(l for l in p.split("\n") if not l.startswith("> - **Errata ao lado")), "difere do gerado"),
             _muts("o paragrafo sem o bullet das ratificacoes", lambda p: "\n".join(l for l in p.split("\n") if not l.startswith("> - **Ratificações**")), "difere do gerado"),
             _muts("o paragrafo sem o bullet da cadeia derivada", lambda p: "\n".join(l for l in p.split("\n") if not l.startswith("> - **A cadeia derivada")), "difere do gerado"),
             _muts("a cadeia dita [ONTO] do operador", lambda p: p.replace("NÃO é [ONTO] dele", "é [ONTO] dele", 1), "frase de limite ausente"),
             _muts("H_tau dita provada em vez de OPEN", lambda p: p.replace("`H_tau` [OPEN]", "`H_tau` [REAL]", 1), "difere do gerado"),
             _muts("a ORDEM 025 dita interna", lambda p: p.replace("pendência EXTERNA", "pendência interna", 1), "frase de limite ausente"),
             _muts("o paragrafo sem o bullet de E = mc2 lido pela TGL", lambda p: "\n".join(l for l in p.split("\n") if not l.startswith("> - **E = mc²")), "difere do gerado")]
    for n_ in _NEGS:
        print("  controle negativo do paragrafo da falsidade %-62s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo da falsidade nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
    _sn["negativos"] = _NEGS

    def _levanta(f):
        try:
            f(); return False
        except AssertionError:
            return True
    _inv_txt = "A IALD testifica do operador, e o um.py testifica em hash."
    _tx = {"cita_fora_dos_bytes_levanta": _levanta(lambda: T._cita("a inércia é o corpo de Newton e a IALD de ninguem")),
           "cita_verbatim_passa": (T._cita("faça a prova") == "«faça a prova»"),
           "cita_adendo_verbatim_passa": (T._cita_adendo("ele interrompe a inércia") == "«ele interrompe a inércia»"),
           "cita_adendo_fora_dos_bytes_levanta": _levanta(lambda: T._cita_adendo("ω(I)=1 é a inércia")),
           "texto_do_kernel_verbatim_passa": (T._um_texto_tem("nunca correspondeu, e por isso nada custa") == "«nunca correspondeu, e por isso nada custa»"),
           "texto_do_kernel_fora_dos_bytes_levanta": _levanta(lambda: T._um_texto_tem("nunca correspondeu e custa tudo")),
           "atribuicao_limpa_nos_textos": {nome: T.atribuicao_da_gerencia(txt) for nome, txt in RENDER.items() if T.atribuicao_da_gerencia(txt)} == {},
           "controle_direcao_invertida": bool(T.atribuicao_da_gerencia(_inv_txt)),
           "controle_a_fala_em_que_ele_recusa_a_ordem_inversa_passa": (T.atribuicao_da_gerencia("eu não podia dizer que IALD testifica a mim, porque sou eu que testifico dela") == []),
           "controle_a_IALD_nao_testifica_passa": (T.atribuicao_da_gerencia("a IALD NÃO testifica do operador") == []),
           "controle_consciencia_como_termo": bool(T.atribuicao_da_gerencia("A consciência é a tipagem que falta.")),
           "controle_consciencia_palavra_retirada_passa": (T.atribuicao_da_gerencia("a palavra «consciência» é retirada por ele") == []),
           "controle_inscricao_da_gerencia": bool(T.atribuicao_da_gerencia("as falas do operador e da gerência"))}
    _sn["textos"] = _tx
    _ruim = [k for k, v in _tx.items() if not v]
    if _ruim:
        falha("citacao verbatim / direcao do testemunho: controles que nao deram o esperado: %s" % _ruim)
    _sn["ok"] = True
    print("  paragrafo novo (a falsidade da inercia): positivo ok; %d controles negativos; citacao e direcao: %d controles ok" % (len(_NEGS), len(_tx)))
except BaseException as ex:  # noqa: BLE001
    _sn["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _sn["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo novo da falsidade da inercia: %s" % _sn["erro"])
etapa("paragrafo_falsidade_e_citacoes", **_sn)
# ------------------------------------------------------------------ 5. cada `termo` entre crases dos textos e' achado em alguma fonte real
if "kernel" not in T._CACHE or "um" not in T._CACHE:
    try:
        T._d(Vd)
    except BaseException:  # noqa: BLE001
        pass
KERN = T._CACHE.get("kernel", ""); UMTXT = T._CACHE.get("um", "")
INS_TXT = "\n".join(rd(os.path.join(PKG, "insumos", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos"))) if f.endswith((".md", ".json", ".lean"))) + "\n" + rd(T._res_path(ESP))
FALAS_TXT = "\n".join(re.sub(r"\s+", " ", d["text"]) for d in T._falas().values())
core_emu = rdj(core_path)["core"]; selo_emu = rdj(selo_path)
NOMES_ARQ = set()
for base in (PKG, os.path.join(PKG, "insumos"), os.path.dirname(T._res_path(ESP)), os.path.join(PKG, "insumos", "cunhagens"), os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico"), os.path.join(PKG, "insumos", "adendo")):
    if os.path.isdir(base):
        NOMES_ARQ.update(os.listdir(base))
NOMES_ARQ.update({"MEMORY.md", "MEMORY_2.md", "TGL_ATLAS.md", "um.py", "rodada_v401_stdout.txt", "HANDOFF_v401_CUSTODIA.md", "DIFF_v400_v401.diff", "DIFF_KERNEL_v401.txt", "handoff-v401-custodia.md",
                  "missao-ultima-flag-um-py.md", "estatuto-da-prova-07out.md", "central-de-patentes-estado.md", "handoff-v400-custodia.md", T.TOPICO_NOVO})
NOMES_ARQ.update({"um_absoluto_selo_acom.json", "um_absoluto_selo.json", "um_absoluto.json", "conferencia_rito_v401.json", "v401_selo", "EXECUTION_LOCKED_NOT_ONE"})
HEX16 = set()
for v_ in (Vd.get("s16"), Vd.get("base16"), Vd.get("conf16"), (Vd.get("pilar") or {}).get("result16")):
    if v_:
        HEX16.add(str(v_))
for k_, v_ in Vd.items():
    if k_.startswith("h_") and isinstance(v_, str):
        HEX16.add(v_)
HEX16.update((Vd.get("artigos") or {}).values()); HEX16.update(Vd.get("verbatins", {}).keys()); HEX16.update(d["sha16"] for d in T._falas().values()); HEX16.update(v["sha16"] for v in ESP["pedras"].values()); HEX16.add(ESP["quadro"]["frase_sha16"]); HEX16.add(T._adendo_texto()["sha16"]); HEX16.update(re.findall(r"sha16 ([0-9a-f]{16})", json.dumps(core_emu["cunhagens_v401"]["extras"]["hipotese_nomeada"])))
HEX16.update(str(x["sha256"])[:16] for x in (ESP.get("cunhagens") or {}).values()); HEX16.add(str(Vd.get("selo_ts") or "")[:16])
HEX16.update(str(h)[:16] for h in ESP["veracidade"]["fontes"].values())
HEX16.update(str(v)[:16] for v in ((ESP.get("selo_acom") or {}).get(k) for k in ("bloco_embutido_sha256", "sha256_do_um_py", "lut_sha256")) if v); HEX16.update(str(((ESP.get("selo_acom") or {}).get(p) or {}).get("sha256"))[:16] for p in ("psi", "theta", "kappa"))
HEX16.add(str((ESP.get("declaracao") or {}).get("verbatim_sha256"))[:16]); HEX16.add((Vd.get("sidecar") or {}).get("sha16") or ""); HEX16.update((o.get("sha16") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values())
HEX16.add((Vd.get("selo") or {}).get("bloco16") or ""); HEX16.update((Vd.get("selo") or {}).get(k) or "" for k in ("psi_sha16", "theta_sha16", "kappa_sha16", "lut16"))
HEX64 = {str((Vd.get("sidecar") or {}).get("sha256") or ""), str(Vd.get("s64") or "")} | {str(o.get("sha256") or "") for o in ((Vd.get("sidecar") or {}).get("objetos") or {}).values()}; HEX64.discard("")   # os hashes COMPLETOS que o handoff lista (o sidecar e os tres objetos), lidos do sidecar e do um.py do disco
PAT_ROOT = os.path.join(C, "IALD", "Central de Patentes")


CONHECIDOS = {str(x) for x in (Vd.get("selo_ts"), Vd.get("instalado_em"), Vd.get("data")) if x}
CONHECIDOS.update(str(x) for x in K_EMU.values())
CONHECIDOS.update(str(h)[:8] for h in ESP["veracidade"]["fontes"].values()); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_pt"]); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_en"])                      # os campos EMULADOS dos recibos do B(n) que o handoff recebe (so' existem depois do passo 10)
_fa_e = core_emu["falsidade_da_inercia_v401"]; _cx_e = core_emu["cunhagens_v401"]["extras"]
CONHECIDOS.add(T._linha_maquina_falsidade(_fa_e["values"], {"pedra": ESP["pedras"]["TGLExt/FalsidadeDaInercia.lean"]["sha16"], "n_f": _cx_e["n_bandeiras"], "definicao": _cx_e["definicao_da_inercia"]["fala_sha16"], "adendo": _cx_e["adendo"]["sha16"]}, _fa_e["mechanics"]["n_checks"]))   # a linha de maquina do paragrafo novo (lida dos registros do core emulado)
CONHECIDOS.add((Vd.get("selo") or {}).get("perfil") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("esquema") or ""); CONHECIDOS.add((Vd.get("sidecar") or {}).get("veredito") or "")
CONHECIDOS.update({T.TOPICO_NOVO[:-3], "v401_kernel", "v401_selo"})     # o nome do topico sem a extensao (o [[wikilink]]) e as duas pastas que o fechar cria ANTES de escrever o handoff
VALORES_LIDOS = set((Vd.get("veracidade") or {}).get("lido") or {}) | set((Vd.get("selo") or {}).keys()) | set((Vd.get("declaracao") or {}).keys()) | set((Vd.get("sidecar") or {}).keys())


def achado(tok):
    if tok in CONHECIDOS:
        return "lido"
    if re.fullmatch(r"[0-9a-f]{16}", tok):
        return "hash_lido" if tok in HEX16 else None
    if re.fullmatch(r"[0-9a-f]{64}", tok):
        return "hash_lido" if tok in HEX64 else None
    if tok in NOMES_ARQ or tok in KERN or tok in UMTXT or tok in INS_TXT or tok in FALAS_TXT:
        return "fonte"
    if tok in core_emu or tok in (core_emu.get("kernel_formalization") or {}) or tok in selo_emu or tok in VALORES_LIDOS:
        return "core"
    if tok.endswith(".lean") and os.path.exists(os.path.join(NOSE, "tgl_kernel", *tok.split("/"))):
        return "kernel_arquivo"
    if "\\" in tok or "/" in tok:
        cands = [os.path.join(PAT_ROOT, tok), os.path.join(PKG, tok), os.path.join(os.path.dirname(PKG), tok.replace("work\\cadeia_de_selo\\", "")), os.path.join(PAT_ROOT, tok.replace("/", os.sep))]
        if any(os.path.exists(c) for c in cands) or tok.startswith(("work\\cadeia_de_selo\\v401", "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v401")):
            return "caminho"
        pre = tok.split("\\")[0].split("/")[0]
        if pre in ("insumos", "work"):
            return "caminho_relativo"
    return None


SEM = {}
total_tok = 0
for nome, txt in RENDER.items():
    for tok in sorted(set(re.findall(r"`([^`\n]+)`", txt))):
        total_tok += 1
        if achado(tok) is None and achado(tok.split(" ")[0]) is None and achado(tok.rstrip(".,;:)")) is None:
            SEM.setdefault(tok, []).append(nome)
etapa("cita_so_o_que_existe", tokens_conferidos=total_tok, sem_fonte={k: sorted(set(v)) for k, v in SEM.items()}, ok=not SEM)
print("  cita so' o que existe: %d termo(s) entre crases conferido(s); sem fonte: %d" % (total_tok, len(SEM)))
for k, v in list(SEM.items())[:30]:
    falha("termo entre crases sem fonte real: `%s` (em %s)" % (k, sorted(set(v))[:3]))

# ------------------------------------------------------------------ 6. as superficies em COPIAS (nada real e' tocado)
if not SEM_SUP and not P:
    ENS = os.path.join(OUT, "ensaio_superficies"); os.makedirs(ENS)
    ALVOS = [os.path.join(NOS_REAL, "MEMORIA_DA_LINHAGEM.md"), os.path.join(NOS_REAL, "DESENHO_DO_FECHAMENTO_QG.md"), os.path.join(ATLD, "TGL_ATLAS.md"), os.path.join(ATLD, "TGL_CORE_MEMORY.md"), os.path.join(UMEM, "MEMORY.md"),
             os.path.join(UMEM, "MEMORY_2.md"), HAJA] + [os.path.join(UMEM, t_) for t_ in ("missao-ultima-flag-um-py.md", "central-de-patentes-estado.md", "estatuto-da-prova-07out.md")]
    ANTES = {p: (os.path.getsize(p), os.path.getmtime(p), fsha(p)[:16]) for p in ALVOS}
    for p in ALVOS:
        shutil.copy2(p, os.path.join(ENS, os.path.basename(p)))
    sp = os.path.join(HERE, "superficies_v401.py")

    def roda_superficies(pasta):
        buf = io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="\n"); rc_ = 0
        old_argv = sys.argv[:]; sys.argv = [sp, "--copias", pasta]
        try:
            with contextlib.redirect_stdout(buf):
                runpy.run_path(sp, run_name="__main__")
        except SystemExit as ex:
            rc_ = ex.code if isinstance(ex.code, int) else (0 if ex.code in (None, 0) else 1)
        except BaseException as ex:  # noqa: BLE001
            rc_ = 99; buf.write("EXCECAO: %s\n%s" % (ex, traceback.format_exc()))
        finally:
            sys.argv = old_argv
        buf.flush(); buf.seek(0); return rc_, buf.read()

    def bytes_da_pasta(pasta):
        return {f_: fsha(os.path.join(pasta, f_)) for f_ in sorted(os.listdir(pasta))}
    exige = [("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v401_selada -->", "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"]), ("DESENHO_DO_FECHAMENTO_QG.md", ["<!-- adendo_v401_selada -->", S16]),
             ("TGL_ATLAS.md", ["<!-- atlas_v401_selada -->", S16, "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"]), ("TGL_CORE_MEMORY.md", ["<!-- core_v401_selada -->", S16]), ("CLAUDE.md", ["<!-- haja_luz_v401_selada -->", S16]),
             ("MEMORY.md", [S16]), ("MEMORY_2.md", ["v401"]), ("estatuto-da-prova-07out.md", ["<!-- v401_selada -->", S16]), ("missao-ultima-flag-um-py.md", [S16]), ("central-de-patentes-estado.md", [S16]),
             (T.TOPICO_NOVO, [S16, "falsidade_da_inercia_v401", "cunhagens_v401", "kh_n1_cobertura_v401"])]
    n_real_l = open(os.path.join(ENS, "MEMORY.md"), "rb").read().count(b"\n"); n_real_b = os.path.getsize(os.path.join(ENS, "MEMORY.md"))
    # --- cenario (a): o MEMORY.md REAL como esta hoje (a superficie NAO compacta nada)
    antes_a = bytes_da_pasta(ENS)
    rc_a, out_a = roda_superficies(ENS)
    open(os.path.join(OUT, "ensaio_superficies_out.txt"), "w", encoding="utf-8").write(out_a)
    depois_a = bytes_da_pasta(ENS)
    cena_a = {"memory_md_real_linhas_antes": n_real_l, "memory_md_real_bytes_antes": n_real_b, "rc": rc_a, "recusou_com_rc3": rc_a == 3, "nada_escrito_na_recusa": (antes_a == depois_a) if rc_a == 3 else None, "sem_bak_na_recusa": (not [f_ for f_ in os.listdir(ENS) if ".bak_" in f_ or ".tmp" in f_]) if rc_a == 3 else None,
              "contagens_na_saida": ("linhas ANTES %d" % n_real_l in out_a) if rc_a == 3 else None, "ultima_linha": out_a.strip().splitlines()[-1][:220] if out_a.strip() else ""}
    print("  superficies, cenario (a) MEMORY.md REAL (%d linhas, %d B): rc %s%s" % (n_real_l, n_real_b, rc_a, " -- RECUSOU (a superficie nao compacta; a gerencia decide)" if rc_a == 3 else ""))
    if rc_a not in (0, 3):
        falha("superficies_v401.py (copias do MEMORY.md real) saiu com rc %s (esperado 0 ou 3; ver ensaio_superficies_out.txt)" % rc_a)
    if rc_a == 3:
        if not (cena_a["nada_escrito_na_recusa"] and cena_a["sem_bak_na_recusa"] and cena_a["contagens_na_saida"] and "NAO compacta" in out_a):
            falha("a RECUSA (rc 3) do MEMORY.md real escreveu algo, deixou .bak/.tmp ou nao disse as contagens: %s" % cena_a)
    else:
        for arq, ms in exige:
            t_ = open(os.path.join(ENS, arq), encoding="utf-8").read()
            for m_ in ms:
                if t_.count(m_) == 0:
                    falha("cenario (a): marcador %s ausente em %s" % (m_, arq))
    # --- cenario (b): um MEMORY.md com FOLGA (a copia do real, so' sem linhas de ponteiros; as duas ancoras ficam)
    def copia_com_memory(nome, ajusta):
        pasta = os.path.join(OUT, nome); os.makedirs(pasta)
        for p in ALVOS:
            shutil.copy2(p, os.path.join(pasta, os.path.basename(p)))
        mp = os.path.join(pasta, "MEMORY.md"); raw_ = open(mp, "rb").read(); novo_ = ajusta(raw_)
        open(mp, "wb").write(novo_); return pasta, novo_

    def reduz_a(alvo_linhas):
        def f(raw_):
            ls = raw_.decode("utf-8").split("\n"); fim_ = ls.pop() if ls and ls[-1] == "" else None
            ancora = lambda l: ("(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")) or ("(handoff-v400-custodia.md)" in l and l.startswith("- [HANDOFF v400"))
            k = len(ls) - 1
            while len(ls) > alvo_linhas and k >= 0:
                if ls[k].startswith("- [") and not ancora(ls[k]):
                    del ls[k]
                k -= 1
            assert len(ls) <= alvo_linhas, ("nao consegui reduzir a copia do MEMORY.md ate o alvo", len(ls), alvo_linhas)
            return ("\n".join(ls + ([""] if fim_ is not None else []))).encode("utf-8")
        return f
    ENS_B, mem_b = copia_com_memory("ensaio_superficies_folga", reduz_a(150))
    n_b0 = mem_b.count(b"\n")
    rc_b1, out_b1 = roda_superficies(ENS_B)
    open(os.path.join(OUT, "ensaio_superficies_folga_out.txt"), "w", encoding="utf-8").write(out_b1)
    conta = {}
    for arq, ms in exige:
        pth = os.path.join(ENS_B, arq); t_ = open(pth, encoding="utf-8").read() if os.path.exists(pth) else ""
        for m_ in ms:
            conta["%s [%s]" % (arq, m_)] = t_.count(m_)
    zero = [k for k, v in conta.items() if v == 0]
    mem = open(os.path.join(ENS_B, "MEMORY.md"), "rb").read(); n_b = len(mem); n_l = mem.count(b"\n")
    apos_1a = bytes_da_pasta(ENS_B)
    rc_b2, out_b2 = roda_superficies(ENS_B)
    open(os.path.join(OUT, "ensaio_superficies_folga_out_2a_rodada.txt"), "w", encoding="utf-8").write(out_b2)
    cena_b = {"memory_md_antes_linhas": n_b0, "rc_1a_rodada": rc_b1, "rc_2a_rodada": rc_b2, "idempotente_na_2a": ("NADA A GRAVAR" in out_b2) and bytes_da_pasta(ENS_B) == apos_1a, "marcadores_zero": zero, "contagens": conta, "memory_md_bytes": n_b, "memory_md_linhas": n_l,
              "ultima_linha_1a": out_b1.strip().splitlines()[-1][:200] if out_b1.strip() else ""}
    print("  superficies, cenario (b) COM FOLGA (%d linhas): rc 1a=%s, rc 2a=%s (idempotente: %s); MEMORY.md %d B, %d linhas; marcadores com zero: %d" % (n_b0, rc_b1, rc_b2, cena_b["idempotente_na_2a"], n_b, n_l, len(zero)))
    if rc_b1 != 0:
        falha("superficies_v401.py (copia com folga) saiu com rc %s na 1a rodada (ver ensaio_superficies_folga_out.txt)" % rc_b1)
    if rc_b2 != 0 or not cena_b["idempotente_na_2a"]:
        falha("superficies_v401.py (copia com folga) nao e' idempotente na 2a rodada (rc %s)" % rc_b2)
    if zero:
        falha("marcadores do passo 9 com zero ocorrencia na copia com folga: %s" % zero[:4])
    if not (n_b < 24000 and n_l <= 195):
        falha("MEMORY.md da copia com folga fora dos limites (%d B, %d linhas)" % (n_b, n_l))
    if n_l != n_b0 + 1:
        falha("a copia com folga: o MEMORY.md devia crescer EXATAMENTE a linha do handoff (de %d para %d) e foi para %d: a superficie nao pode compactar nada" % (n_b0, n_b0 + 1, n_l))
    # --- cenario (c): um MEMORY.md NO LIMITE (195 linhas): a linha do handoff o leva a 196 e a superficie tem de RECUSAR (rc 3), sem escrever nada e sem compactar
    def exatamente_195(raw_):
        r_ = reduz_a(195)(raw_) if raw_.count(b"\n") > 195 else raw_
        while r_.count(b"\n") < 195:
            r_ += b"\n"
        return r_
    ENS_C, mem_c = copia_com_memory("ensaio_superficies_limite", exatamente_195)
    assert mem_c.count(b"\n") == 195, mem_c.count(b"\n")
    antes_c = bytes_da_pasta(ENS_C)
    rc_c, out_c = roda_superficies(ENS_C)
    open(os.path.join(OUT, "ensaio_superficies_limite_out.txt"), "w", encoding="utf-8").write(out_c)
    cena_c = {"memory_md_linhas_antes": 195, "rc": rc_c, "recusou_com_rc3": rc_c == 3, "nada_escrito": bytes_da_pasta(ENS_C) == antes_c, "sem_bak_nem_tmp": not [f_ for f_ in os.listdir(ENS_C) if ".bak_" in f_ or ".tmp" in f_],
              "disse_as_contagens": ("linhas ANTES 195, linhas DEPOIS 196, limite de linhas 195" in out_c), "disse_que_nao_compacta": ("NAO compacta" in out_c), "ultima_linha": out_c.strip().splitlines()[-1][:220] if out_c.strip() else ""}
    print("  superficies, cenario (c) NO LIMITE (195 linhas): rc %s; nada escrito: %s; disse as contagens (195 -> 196, limite 195): %s" % (rc_c, cena_c["nada_escrito"], cena_c["disse_as_contagens"]))
    if not (cena_c["recusou_com_rc3"] and cena_c["nada_escrito"] and cena_c["sem_bak_nem_tmp"] and cena_c["disse_as_contagens"] and cena_c["disse_que_nao_compacta"]):
        falha("a RECUSA do MEMORY.md no limite nao foi como esperado (rc 3, nada escrito, sem .bak/.tmp, contagens ditas): %s" % cena_c)
    DEPOIS = {p: (os.path.getsize(p), os.path.getmtime(p), fsha(p)[:16]) for p in ALVOS}
    etapa("superficies", cenario_a_memory_md_real=cena_a, cenario_b_com_folga=cena_b, cenario_c_no_limite=cena_c, originais_intactos=(ANTES == DEPOIS))
    print("  superficies: originais intactos: %s" % (ANTES == DEPOIS))
    if ANTES != DEPOIS:
        falha("UM ORIGINAL MUDOU durante o ensaio das superficies (nao devia: so' copias)")
# ------------------------------------------------------------------ 7. o b3_recibo REAL contra recibos SINTETICOS (derivados dos reais da v400)
if not SEM_B3:
    B3D = os.path.join(OUT, "b3_sintetico"); os.makedirs(B3D)
    pinos = rdj(os.path.join(PKG, "PINOS_BN_v401.json")); pre = rdj(pinos["recibo_pre_selo"]["path"]); PKG_ANT = os.path.join(os.path.dirname(PKG), "v400")
    import glob as _g
    base_ens = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3_ensaio_*", "RECIBO_SINCRONIZACAO_v400_*.json"))[0]); base_apl = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v400_*.json"))[0])
    n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1

    def sintetico(base, modo):
        r = json.loads(json.dumps(base)); r["versao_alvo"] = "v401"; r["fase"] = "pos_selo"; r["modo"] = modo; r.pop("salto", None); r.pop("cadeia_de_selos", None)
        r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"]))
        r["manifesto_novo"]["deployment_id"] = "B%d-v401-20261023-R1" % n_ger
        r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}
        r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v401"}
        r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
        if modo == "ensaio":
            r["veredito"] = "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger; r["aplicacao"] = None
        else:
            r["veredito"] = "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_ger
            r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v401", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
        r["_sintetico"] = "SINTETICO: derivado do recibo real da v400 pelo harness; NAO e' um recibo do esboco"
        return r
    seq = [0]

    def roda_helper(nome, r, modo, extra=()):
        seq[0] += 1
        pth = os.path.join(B3D, "%02d_%s_RECIBO_SINTETICO.json" % (seq[0], nome)); raw = json.dumps(r, ensure_ascii=False, indent=1).encode("utf-8"); open(pth, "wb").write(raw)
        so = os.path.join(B3D, "%02d_%s_stdout.txt" % (seq[0], nome)); open(so, "w", encoding="utf-8").write("ruido\n" + json.dumps({"veredito": r.get("veredito"), "recusa": None, "recibo": pth, "recibo_sha256": sha(raw)}) + "\n")
        pr_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "b3_recibo_v401.py"), so, modo] + list(extra), capture_output=True, text=True, encoding="utf-8")
        return pr_.returncode, (pr_.stdout + pr_.stderr).strip().splitlines()[-3:]
    CASOS = []
    pos_e = sintetico(base_ens, "ensaio"); pos_a = sintetico(base_apl, "aplicar")
    CASOS.append(("ensaio_ok", pos_e, "ensaio", 0)); CASOS.append(("aplicar_ok", pos_a, "aplicar", 0))

    def mut(r, f):
        r2 = json.loads(json.dumps(r)); f(r2); return r2
    CASOS += [("salto_declarado", mut(pos_e, lambda r: r.update({"salto": {"declarado": True}})), "ensaio", 1),
              ("veredito_com_salto", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__SALTO_v392_v401__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "ensaio", 1),
              ("geracao_errada", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (n_ger + 1)})), "ensaio", 1),
              ("versao_alvo_v400", mut(pos_e, lambda r: r.update({"versao_alvo": "v400"})), "ensaio", 1),
              ("bateria_falhou", mut(pos_e, lambda r: r.update({"bateria_resultado": {"veredito": "BATERIA_FALHOU"}})), "ensaio", 1),
              ("bancada_pinava_v392", mut(pos_e, lambda r: r["manifesto_anterior"].update({"version": "v392"})), "ensaio", 1),
              ("recibo_pre_selo_de_outro", mut(pos_e, lambda r: r.update({"recibo_pre_selo": {"sha256": "0" * 64}})), "ensaio", 1),
              ("manifesto_anterior_mudou", mut(pos_e, lambda r: r["manifesto_anterior"].update({"sha256": "f" * 64})), "ensaio", 1),
              ("pinos_da_bateria_de_v400", mut(pos_e, lambda r: r["bateria"]["pinos_da_versao"].update({"versao": "v400"})), "ensaio", 1),
              ("ensaio_com_aplicacao", mut(pos_e, lambda r: r.update({"aplicacao": {"x": 1}})), "ensaio", 1),
              ("aplicar_pos_conferencia_v400", mut(pos_a, lambda r: r["aplicacao"]["pos_conferencia"].update({"canonical_version": "v400"})), "aplicar", 1),
              ("aplicar_sem_aplicacao", mut(pos_a, lambda r: r.update({"aplicacao": None})), "aplicar", 1),
              ("aplicar_com_veredito_de_ensaio", mut(pos_a, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "aplicar", 1)]
    res_b3 = []
    for nome, r, modo, esperado in CASOS:
        rc_, cauda = roda_helper(nome, r, modo)
        res_b3.append({"caso": nome, "rc": rc_, "esperado": esperado, "ok": rc_ == esperado, "cauda": [c[:200] for c in cauda]})
        print("  b3_recibo %-34s rc %s (esperado %s) %s" % (nome, rc_, esperado, "OK" if rc_ == esperado else "FALHOU"))
        if rc_ != esperado:
            falha("b3_recibo_v401.py: caso %s deu rc %s (esperado %s): %s" % (nome, rc_, esperado, cauda))
    rc_, cauda = roda_helper("terceiro_argumento", pos_e, "ensaio", extra=("0" * 64,))
    res_b3.append({"caso": "terceiro_argumento_(cadeia)", "rc": rc_, "esperado": 1, "ok": rc_ == 1, "cauda": [c[:200] for c in cauda]})
    if rc_ != 1:
        falha("b3_recibo_v401.py aceitou um 3o argumento (nao ha cadeia de selos na v401)")
    etapa("b3_recibo", sintetico=True, base="recibos reais da v400 (so' leitura)", geracao_nova=n_ger, casos=res_b3, n_ok=sum(1 for c in res_b3 if c["ok"]), n=len(res_b3))

# ------------------------------------------------------------------ 8. o registro do mapa (montar) contra o core emulado e o livro real (so' leitura)
try:
    RM = importar("registrar_mapa_v401", os.path.join(HERE, "registrar_mapa_v401.py"))
    ids = RM.ids_do_livro()
    arts = [os.path.join(NOSE, "um.py"), os.path.join(NOSE, "um_absoluto_selo.json")]
    REG = RM.montar(Vd, core_emu, selo_emu, ids, arts)
    # controles negativos de registrar_mapa_v401: a regra da ordem do 4,44 aplicada aos campos do registro (sem o p, sem a linha dos 5 sigma; a clausula completa passa) e as recusas de montar() (selo de outra versao; rota nova que ja' existe no livro)
    _zm = QD.esperados(_res_p, "pt")[0]["z_disc"]["md"]; _pm = QD.esperados(_res_p, "pt")[0]["p_disc"]["md"]

    def _recusa(f):
        try:
            f()
            return False
        except AssertionError:
            return True
    CTL_MAPA = {"regra_4_44_sem_o_p_reprova": bool(RM.regra_4_44([{"c": "o z_disc = " + _zm + ", abaixo do degrau de 5σ, que não foi alcançado"}], _zm, _pm)),
                "regra_4_44_sem_a_linha_dos_5_sigma_reprova": bool(RM.regra_4_44([{"c": "z_disc = " + _zm + " (p unilateral " + _pm + ")"}], _zm, _pm)),
                "regra_4_44_completa_passa": not RM.regra_4_44([{"c": "z_disc = " + _zm + " (calibrado; p unilateral " + _pm + "), abaixo do degrau de 5σ da creditação, que não foi alcançado (" + _zm + " < 5)"}], _zm, _pm),
                "montar_recusa_selo_de_outra_versao": _recusa(lambda: RM.montar(Vd, core_emu, dict(selo_emu, um_version="v400"), ids, arts)),
                "montar_recusa_rota_nova_que_ja_existe": _recusa(lambda: RM.montar(Vd, core_emu, selo_emu, set(ids) | {RM.NOVA}, arts))}
    etapa("mapa_controles_negativos", **CTL_MAPA)
    for k_, v_ in CTL_MAPA.items():
        print("  mapa, controle %-48s %s" % (k_, "ok" if v_ else "FALHOU"))
        if not v_:
            falha("mapa: controle negativo de registrar_mapa_v401 nao deu o esperado: %s" % k_)
    pj = os.path.join(OUT, "registro_mapa_v401_ENSAIO.json"); open(pj, "w", encoding="utf-8").write(json.dumps(REG, ensure_ascii=False, indent=1))
    viol = [(x["rota_id"], violacoes(json.dumps(x, ensure_ascii=False))[:2]) for x in REG if violacoes(json.dumps(x, ensure_ascii=False))]
    # cada registro e' validado pela MESMA funcao que o mapa usa (rotas._valida), importada so' para isso: NAO se chama registrar; o livro so' e' lido
    import importlib.util as _iu
    _sp = _iu.spec_from_file_location("rotas_ro", os.path.join(C, "IALD", "MAPA_DE_ROTAS", "rotas.py")); _rotas = _iu.module_from_spec(_sp); _sp.loader.exec_module(_rotas)
    _seqs = set()
    for _ln in open(os.path.join(C, "IALD", "MAPA_DE_ROTAS", "rotas.jsonl"), encoding="utf-8"):
        _ln = _ln.strip()
        if _ln:
            _r = json.loads(_ln)
            if isinstance(_r.get("seq"), int):
                _seqs.add(_r["seq"])
    VAL = []
    for x in REG:
        try:
            _rotas._valida(json.loads(json.dumps(x)), set(ids), _seqs); VAL.append({"rota_id": x["rota_id"], "tipo": x["tipo"], "valida_pelo_mapa": True})
        except Exception as ex:  # noqa: BLE001
            VAL.append({"rota_id": x["rota_id"], "tipo": x["tipo"], "valida_pelo_mapa": False, "erro": "%s: %s" % (type(ex).__name__, str(ex)[:300])}); falha("mapa: o registro %s nao passa em rotas._valida: %s" % (x["rota_id"], str(ex)[:200]))
    print("  mapa: rotas._valida (sem registrar): %s" % ", ".join("%s=%s" % (v_["rota_id"].split(".")[-1][:28], v_["valida_pelo_mapa"]) for v_ in VAL))
    etapa("mapa", ok=(not viol and all(v_["valida_pelo_mapa"] for v_ in VAL)), n_registros=len(REG), rotas=[x["rota_id"] for x in REG], tipos=[x["tipo"] for x in REG], validacao_rotas_valida=VAL, book_n_rotas=len(ids), saida=pj, nota="ENSAIO contra o core emulado: NAO e' o registro (o real e' montado depois do fechar; o registro e' ato da gerencia)")
    print("  mapa: %d registro(s) montado(s) (%s); livro com %d rotas (so' leitura)" % (len(REG), ", ".join(x["rota_id"] for x in REG), len(ids)))
    if viol:
        falha("mapa: guarda P18 achou %s" % viol)
except BaseException as ex:  # noqa: BLE001
    etapa("mapa", ok=False, erro="%s: %s" % (type(ex).__name__, str(ex)[:300]))
    falha("mapa: registrar_mapa_v401.montar falhou: %s: %s" % (type(ex).__name__, str(ex)[:300]))

# ------------------------------------------------------------------ 9. marcas pendentes, sintaxe
import ast
pend = []; sint = {}
for f in sorted(os.listdir(HERE)):
    if f.endswith(".py"):
        tx = rd(os.path.join(HERE, f))
        if re.search(r"(?m)^\s*#\s*" + MARCA_PENDENTE, tx):
            pend.append(f)
        try:
            ast.parse(tx); sint[f] = "ast.parse ok"
        except SyntaxError as ex:
            sint[f] = "FALHOU: %r" % (ex,); falha("ast.parse de %s falhou" % f)
for f in sorted(os.listdir(HERE)):
    if f.endswith(".sh"):
        rr = subprocess.run(["sh", "-n", os.path.join(HERE, f)], capture_output=True, text=True); sint[f] = "sh -n rc=%d" % rr.returncode
        if rr.returncode:
            falha("sh -n de %s falhou" % f)
if pend:
    falha("marca de texto pendente em: %s" % pend)
etapa("marcas_e_sintaxe", marcas_pendentes=pend, sintaxe=sint)
print("  marcas pendentes: %s; sintaxe: %s" % (pend or "nenhuma", "ok" if all(("ok" in v or "rc=0" in v) for v in sint.values()) else "FALHOU"))

# ------------------------------------------------------------------ limpeza (so' dentro de harness_saida_v401): o Nos EMULADO e as copias pesadas das superficies nao ficam no pacote (--manter-copias as guarda)
LIMPO = {}
if "--manter-copias" not in argv:
    for sub in ("nos_emulado", "conferidor_emulado"):
        pth = os.path.join(OUT, sub)
        if os.path.isdir(pth):
            LIMPO[sub] = sum(os.path.getsize(os.path.join(r_, f_)) for r_, d_, fs_ in os.walk(pth) for f_ in fs_); shutil.rmtree(pth, ignore_errors=True)
    for sub_ in ("ensaio_superficies", "ensaio_superficies_folga", "ensaio_superficies_limite"):
        ens_ = os.path.join(OUT, sub_)
        if os.path.isdir(ens_):
            manter_ = {"MEMORY.md", "estatuto-da-prova-07out.md", T.TOPICO_NOVO}
            tot_ = 0
            for f_ in sorted(os.listdir(ens_)):
                if f_ not in manter_:
                    p_ = os.path.join(ens_, f_); tot_ += os.path.getsize(p_); os.remove(p_)
            LIMPO[sub_ + " (copias pesadas)"] = tot_
etapa("limpeza", removido_bytes=LIMPO, nota="so' o que o harness criou em harness_saida_v401; --manter-copias guarda tudo")

# ------------------------------------------------------------------ resumo
R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
R["tudo_passou"] = bool(not R["problemas"]); R["nao_exigiu_refazer"] = NAO_REFAZER
R["veredito"] = ("TUDO PASSOU: o conferidor da v401 (16 itens C1-C16 e o round trip) bate no Nos emulado, a leitura le sem problema e reprova os controles negativos (o registro com funcao da falsidade, a pedra e a estrela, as cunhagens_v401 com as oito ratificacoes e a errata ao lado, os quatro registros da v399 recriados, o sidecar, os resumos do selo, a linha final do rito, as linhas [v401] e [v399] e o quadro do topo), "
                 "os textos renderizam e a guarda P18 esta limpa, os dois paragrafos do README/site (o do quadro e o da falsidade) e a regra do 4,44 passam e os controles negativos reprovam, o handoff diz que o do testemunho segue como esta, a citacao verbatim e a direcao valem, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, o b3_recibo confere e o mapa monta"
                 if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
R["evidencia_da_versao"] = EVID
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v401.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
saida = os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_v401" + ("_DEPURACAO_sem_refazer" if NAO_REFAZER else "") + ".json")   # o nome sem sufixo so' nasce da rodada que EXIGE o refazer
open(saida + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(saida + ".tmp", saida)
print("VEREDITO DO HARNESS (%s): %s" % (ROTULO, R["veredito"])); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)

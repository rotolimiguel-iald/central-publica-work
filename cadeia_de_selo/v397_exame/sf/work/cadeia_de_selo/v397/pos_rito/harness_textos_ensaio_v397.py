# -*- coding: utf-8 -*-
"""harness_textos_ensaio_v397.py -- o HARNESS DO POS-RITO da v397 em modo ENSAIO (derivado do harness_textos_ensaio_v396.py, que rodou na v396); SO' LEITURA do Nos real, da producao e das superficies reais.
Importa os modulos REAIS textos_v397.py e leitura_v397.py (os que a cadeia usa) e os executa contra um NOS EMULADO montado de dry_v397 (core_ensaio.json -> um_absoluto.json, selo_ensaio.json -> um_absoluto_selo.json, o um.py candidato, o kernel,
o .md, o artigo PT/EN e o sumario; o stdout do rito e o APLICADO_AO_CANONICO sao EMULADOS e ditos). Tudo o que ele escreve fica em pos_rito\\harness_saida_v397\\ (e o resumo HARNESS_TEXTOS_ENSAIO_v397.json ao lado dele); nada do Nos real,
da memoria, do Atlas, do mapa de rotas, da Bancada ou do git e' tocado; nenhum rito e' rodado.
O que ele prova (cada etapa e' uma entrada do resumo):
  precondicoes   o candidato (ESPERADOS == CANDIDATO == arquivo == dry_v397/um.py) e a regeneracao terminada (refazer_out_v397.txt mostra '== FIM'); a evidencia carrega mtime e sha16 de cada entrada;
  conferidor     o conferir_rito_v397.py REAL (copia, com delta_v397, quadro_v397 e runtime_quadro_v397) roda contra o Nos emulado (V397_NOS) e da' TUDO BATE: a conferencia que a leitura le;
  leitura        a leitura_v397.ler() REAL contra o Nos emulado: zero PROBLEMAS; mais controles NEGATIVOS (selo de outra versao, registro ausente, registro nao selado, numero lido adulterado, z_disc acima de 5, checagem que falhou, fonte adulterada,
                 gate movido, bandeira da pedra Token ausente, composicao fora do trio, registros da v396/v395/v394 nao selados, face de Fock habitada ou dita dentro da pedra, AVISO da v397 ou de bloco anterior, linha do Teste da Unica Palavra ausente), cada um tem de reprovar;
  textos         todas as funcoes publicas de textos_v397 renderizam, a guarda P18 fica limpa em cada saida, os marcadores que a cadeia exige estao nos textos, a errata da palavra «teoremas» esta nos textos que carregam _num;
  paragrafo      o PARAGRAFO do README/site (textos_v397.paragrafo_readme) passa nas verificacoes do quadro contra o resultado pinado, e os CONTROLES NEGATIVOS reprovam: o 4,44 sem o p calibrado, o 4,44 sem a linha dos 5 sigma, numero adulterado,
                 p adulterado, a frase do operador parafraseada entre aspas, o 4,44 numa linha fora do item; e a regra da ordem vale para TODO texto renderizado (cada linha com o 4,44 traz o p calibrado, os 5 sigma e o 'nao foi alcancado');
  cita_so_o_que_existe   cada `termo` entre crases de cada texto e' achado no kernel do Nos emulado, no um.py, nos insumos, nos arquivos ou como hash lido (o que nao e' achado e' dito e reprova);
  superficies    superficies_v397.py REAL roda em COPIAS das superficies reais em TRES cenarios: (a) o MEMORY.md real como esta (a superficie NAO compacta: se ele passar de 195 linhas depois da edicao, tem de RECUSAR com rc 3 sem escrever nada; senao, o caminho normal),
                 (b) um MEMORY.md com FOLGA (copia reduzida): o plano e' conferido antes da primeira escrita, idempotente na 2a rodada, marcadores do passo 9, <= 195 linhas e < 24 000 B, (c) um MEMORY.md NO LIMITE (195 linhas): tem de RECUSAR com rc 3, imprimir as
                 contagens e nao escrever nada em nenhuma copia; os originais nao mudam;
  b3_recibo      b3_recibo_v397.py REAL contra recibos SINTETICOS derivados dos recibos reais da v396 (positivos e negativos);
  mapa           registrar_mapa_v397.montar() REAL contra o core emulado e o livro de rotas real (so' leitura), e cada registro validado pela MESMA funcao que o mapa usa (rotas._valida), SEM registrar; grava registro_mapa_v397_ENSAIO.json (nao e' o registro);
  marcas         nenhuma linha de comentario com a marca de texto pendente em pos_rito\\*.py; ast.parse de todo .py e sh -n do chain.
uso: python -I -B -X utf8 harness_textos_ensaio_v397.py [--sem-superficies] [--sem-b3] [--sem-negativos] [--rotulo <nome>] [--nao-exigir-refazer] [--manter-copias]   (rc 0 = tudo passou; rc 4 = precondicao nao satisfeita, nada foi rodado;
--nao-exigir-refazer: NAO exige refazer_out_v397.txt (nem o '== FIM' nem as datas): modo de ENSAIO antes de a gerencia regerar o candidato; o resumo e o veredito DIZEM que a regeneracao nao foi comprovada;
sem --manter-copias o Nos emulado e as copias pesadas das superficies sao apagados no fim, so' dentro de harness_saida_v397)"""
import contextlib, hashlib, importlib.util, io, json, os, re, runpy, shutil, subprocess, sys, time, traceback
sys.dont_write_bytecode = True
MARCA_PENDENTE = "TEXTO_A_REESCREVER" + "_V397"
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); PKG = os.path.dirname(HERE)
DRY = os.path.join(PKG, "dry_v397"); OUT = os.path.join(HERE, "harness_saida_v397"); NOSE = os.path.join(OUT, "nos_emulado")
sys.path.insert(0, PKG)
from guarda_p18_v397 import violacoes  # noqa: E402
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
R = {"rotulo": ROTULO, "inicio": time.strftime("%Y-%m-%d %H:%M:%S"), "emulado": ["stdout do rito (rodada_v397_stdout.txt em nos_emulado)", "APLICADO_AO_CANONICO", "o Nos inteiro (montado de dry_v397: core_ensaio, selo_ensaio completado com as chaves do selo da v396 que o main poe depois do literal, um.py, kernel, md, artigo)",
                                                                           "os recibos do B(n) (SINTETICOS, derivados dos recibos reais da v396)"], "etapas": {}, "problemas": []}


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


for n in ("ESPERADOS_v397.json", "CANDIDATO_v397.json", "um_v397_candidato.py", "PINOS_BN_v397.json") + (() if NAO_REFAZER else ("refazer_out_v397.txt",)):
    if not os.path.exists(os.path.join(PKG, n)):
        recusa("falta %s no pacote" % n)
ESP = rdj(os.path.join(PKG, "ESPERADOS_v397.json")); CM = rdj(os.path.join(PKG, "CANDIDATO_v397.json"))
cand16 = fsha(os.path.join(PKG, "um_v397_candidato.py"))[:16]
if not (ESP["candidato_sha16"] == CM["sha16"] == cand16):
    recusa("o candidato nao e' um so': ESPERADOS %s, CANDIDATO %s, arquivo %s (regeneracao em curso?)" % (ESP["candidato_sha16"], CM["sha16"], cand16))
for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "um_absoluto_forma_canonica.md", "um_absoluto_manifest.md", "dry_v397_pt.txt", "dry_v397_en.txt", "dry_v397_pt.toc", "dry_v397_en.toc", "tgl_kernel"):
    if not os.path.exists(os.path.join(DRY, n)):
        recusa("dry_v397 incompleto (falta %s): a regeneracao ainda nao terminou?" % n)
if fsha(os.path.join(DRY, "um.py"))[:16] != ESP["candidato_sha16"]:
    recusa("o um.py de dry_v397 (%s) != o candidato de ESPERADOS (%s): o dry e' de outra geracao" % (fsha(os.path.join(DRY, "um.py"))[:16], ESP["candidato_sha16"]))
refazer = rd(os.path.join(PKG, "refazer_out_v397.txt")) if os.path.exists(os.path.join(PKG, "refazer_out_v397.txt")) else ""
if not NAO_REFAZER and "== FIM" not in refazer:
    recusa("refazer_out_v397.txt nao mostra '== FIM': a regeneracao nao terminou")
if not NAO_REFAZER and os.path.getmtime(os.path.join(PKG, "refazer_out_v397.txt")) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v397.json")):
    recusa("refazer_out_v397.txt e' mais ANTIGO que ESPERADOS_v397.json: outra regeneracao escreveu o ESPERADOS depois do fim registrado")
if os.path.getmtime(os.path.join(DRY, "core_ensaio.json")) < os.path.getmtime(os.path.join(PKG, "ESPERADOS_v397.json")) - 600:
    recusa("o core_ensaio.json de dry_v397 e' mais de 10 min mais antigo que ESPERADOS_v397.json: dry de outra geracao?")
EVID = {n: {"mtime": mt(os.path.join(PKG, n)), "sha16": fsha(os.path.join(PKG, n))[:16]} for n in ("ESPERADOS_v397.json", "CANDIDATO_v397.json", "um_v397_candidato.py", "PINOS_BN_v397.json", "refazer_out_v397.txt") if os.path.exists(os.path.join(PKG, n))}
EVID.update({"dry_v397/" + n: {"mtime": mt(os.path.join(DRY, n)), "sha16": fsha(os.path.join(DRY, n))[:16]} for n in ("core_ensaio.json", "selo_ensaio.json", "um.py", "dry_v397_pt.txt")})
etapa("precondicoes", ok=True, candidato_sha16=cand16, evidencia=EVID, refazer_exigido=not NAO_REFAZER, refazer_out_presente=os.path.exists(os.path.join(PKG, "refazer_out_v397.txt")), refazer_fim_visto=("== FIM" in refazer),
      nota=("MODO --nao-exigir-refazer: a regeneracao do candidato NAO foi comprovada por este harness (refazer_out_v397.txt nao exigido); o ensaio vale para o candidato, o ESPERADOS e o dry_v397 que estao em disco AGORA" if NAO_REFAZER else "refazer_out_v397.txt exigido e visto com == FIM"))
print("harness do pos-rito v397 (%s): candidato %s; ESPERADOS %s; dry core %s; refazer FIM: %s" % (ROTULO, cand16, EVID["ESPERADOS_v397.json"]["mtime"], EVID["dry_v397/core_ensaio.json"]["mtime"], "== FIM" in refazer))

# ------------------------------------------------------------------ 1. o Nos emulado
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(NOSE)
for src, dst in (("um.py", "um.py"), ("core_ensaio.json", "um_absoluto.json"), ("um_absoluto_forma_canonica.md", "um_absoluto_forma_canonica.md"), ("um_absoluto_manifest.md", "um_absoluto_manifest.md"),
                 ("dry_v397_pt.txt", "um_absoluto_pt.txt"), ("dry_v397_en.txt", "um_absoluto_en.txt"), ("dry_v397_pt.toc", "um_absoluto_pt.toc"), ("dry_v397_en.toc", "um_absoluto_en.toc"), ("dry_v397_pt.pdf", "um_absoluto_pt.pdf"), ("dry_v397_en.pdf", "um_absoluto_en.pdf")):
    if os.path.exists(os.path.join(DRY, src)):
        shutil.copyfile(os.path.join(DRY, src), os.path.join(NOSE, dst))
shutil.copytree(os.path.join(DRY, "tgl_kernel"), os.path.join(NOSE, "tgl_kernel"))
# o selo do ensaio a seco nao traz o que o main poe DEPOIS do literal (sha256 do um.py, fail_closed_selftest, rite_checkpoints, not_sealed_this_run): como em teste_conferidor_positivo_v397.py, o selo emulado ganha essas chaves do selo da v396 e o sha256 do um.py candidato
_selo0 = rdj(os.path.join(PKG, "base_v396", "um_absoluto_selo.json")); _selo = dict(_selo0); _selo.update(rdj(os.path.join(DRY, "selo_ensaio.json")))
_selo["sha256"] = dict(_selo0.get("sha256") or {}); _selo["sha256"]["um.py"] = fsha(os.path.join(NOSE, "um.py"))
open(os.path.join(NOSE, "um_absoluto_selo.json"), "w", encoding="utf-8").write(json.dumps(_selo, ensure_ascii=False, default=str))
N_ = ESP["escada"][1]; n_spec = len(ESP["registros_v397"])
STDOUT_EMULADO = "\n".join(["[v397] EMULADO PELO HARNESS (nao e' o stdout de um rito; so' as linhas que a leitura confere)",
                            "   [v397] o Teste da Unica Palavra (Fase 9 V2-c1, aberto uma vez em 23/10), lido por hash ao lado do V1 (nenhum sigma novo): %s" % ESP["vereditos_novos_v397"]["teste_de_veracidade_fase9_v397"],
                            "   [v397] a pedra Token e as quatro falas de 23/10 (cunhagens_v397): %s | registros por spec: %d (selados %d)" % (ESP["registros_v397"]["cunhagens_v397"], n_spec, n_spec),
                            "teoremas limpos: %s/%s" % (N_, N_), ">>> TGL_KERNEL_STAGE1_VERIFIED", "[selo] rite_checkpoints: chave desligada ; reaproveitados 0", "FAIL_CLOSED_SELFTEST_PASSED", "[selo] colapso tipado: EMULADO", "RITO_RC=0", ""])
open(os.path.join(NOSE, "rodada_v397_stdout.txt"), "w", encoding="utf-8", newline="\n").write(STDOUT_EMULADO)
etapa("nos_emulado", ok=True, pasta=NOSE, arquivos=sorted(os.listdir(NOSE)), um16=fsha(os.path.join(NOSE, "um.py"))[:16])

# ------------------------------------------------------------------ 2. o conferidor REAL (copia) contra o Nos emulado
CF = os.path.join(OUT, "conferidor_emulado"); os.makedirs(CF)
for n in ("conferir_rito_v397.py", "delta_v397.py", "quadro_v397.py", "runtime_quadro_v397.py", "ESPERADOS_v397.json"):
    shutil.copyfile(os.path.join(PKG, n), os.path.join(CF, n))
env = dict(os.environ); env["V397_NOS"] = NOSE; env["PYTHONIOENCODING"] = "utf-8"
pr = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", "conferir_rito_v397.py"], cwd=CF, env=env, capture_output=True, text=True, encoding="utf-8")
open(os.path.join(CF, "conferir_rito_v397_stdout.txt"), "w", encoding="utf-8").write(pr.stdout + pr.stderr)
conf_ok = (pr.returncode == 0 and pr.stdout.strip().splitlines()[-1:] == ["TUDO BATE"])
POS_EMU = os.path.join(OUT, "pos_rito_emulada"); os.makedirs(os.path.join(POS_EMU, "conferidor"))
if os.path.exists(os.path.join(CF, "conferencia_rito_v397.json")):
    shutil.copyfile(os.path.join(CF, "conferencia_rito_v397.json"), os.path.join(POS_EMU, "conferidor", "conferencia_rito_v397.json"))
etapa("conferidor", ok=conf_ok, rc=pr.returncode, ultima_linha=(pr.stdout.strip().splitlines() or [""])[-1][:200], conferencia_sha16=(fsha(os.path.join(CF, "conferencia_rito_v397.json"))[:16] if os.path.exists(os.path.join(CF, "conferencia_rito_v397.json")) else None))
print("  conferidor contra o Nos emulado: %s" % ("TUDO BATE" if conf_ok else "NAO BATEU (rc %s)" % pr.returncode))
if not conf_ok:
    falha("o conferidor real nao deu TUDO BATE contra o Nos emulado: a leitura nao tem a conferencia que le (ver conferidor_emulado\\conferir_rito_v397_stdout.txt)")

# ------------------------------------------------------------------ 3. a leitura REAL contra o Nos emulado (+ controles negativos)
L = importar("leitura_v397", os.path.join(HERE, "leitura_v397.py"))
L.NOS = NOSE; L.HERE = POS_EMU; L.PK = PKG
AP = {"um_py_novo": {"sha16": ESP["candidato_sha16"]}, "backups": {"um.py": {"sha16": ESP["origem_sha16"], "backup": "EMULADO_PELO_HARNESS"}}, "ts": time.strftime("%Y%m%d_%H%M%S")}
L._aplicado = lambda: (AP, "EMULADO_PELO_HARNESS")
sys.modules["leitura_v397"] = L
Vd, P = L.ler()
etapa("leitura", problemas=P, n_pedras=Vd.get("n_pedras"), teor=Vd.get("teor"), escada_antes=Vd.get("escada_antes"), kh=Vd.get("kh"), registros_novos=Vd.get("registros_novos"), n_cunhagens=len(Vd.get("verbatins") or {}),
      veracidade_n_checks=(Vd.get("veracidade") or {}).get("n_checks"), patch_ids=Vd.get("patch_ids"))
print("  leitura: %d problema(s); %d pedra(s); escada %s -> %s; registros novos %s" % (len(P), Vd.get("n_pedras") or 0, Vd.get("escada_antes"), Vd.get("teor"), Vd.get("registros_novos")))
for p_ in P:
    falha("leitura: " + p_)
core_path = os.path.join(NOSE, "um_absoluto.json"); selo_path = os.path.join(NOSE, "um_absoluto_selo.json"); std_path = os.path.join(NOSE, "rodada_v397_stdout.txt")
core_raw = open(core_path, "rb").read(); selo_raw = open(selo_path, "rb").read(); std_raw = open(std_path, "rb").read()


def variante(nome, f_core=None, f_selo=None, f_std=None, espera=""):
    """aplica a variante nos arquivos do Nos emulado, roda a leitura, RESTAURA os bytes e confere que reprovou (com o trecho esperado na mensagem)."""
    try:
        if f_core:
            c = json.loads(core_raw.decode("utf-8")); f_core(c["core"]); open(core_path, "wb").write(json.dumps(c, ensure_ascii=False).encode("utf-8"))
        if f_selo:
            s = json.loads(selo_raw.decode("utf-8")); f_selo(s); open(selo_path, "wb").write(json.dumps(s, ensure_ascii=False).encode("utf-8"))
        if f_std:
            open(std_path, "wb").write(f_std(std_raw.decode("utf-8")).encode("utf-8"))
        _, PV = L.ler()
    finally:
        open(core_path, "wb").write(core_raw); open(selo_path, "wb").write(selo_raw); open(std_path, "wb").write(std_raw)
    ok = any(espera in x for x in PV)
    return {"controle": nome, "reprovou": bool(PV), "mensagem_esperada_presente": ok, "problemas": [x[:140] for x in PV][:3]}


def _sem_veracidade(c):
    c.pop("teste_de_veracidade_fase9_v397", None)


def _nao_sela_cunh(c):
    c["cunhagens_v397"]["all_verified"] = False


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


def _token_sem_bandeira(c):
    c["kernel_formalization"][ESP["bandeira_da_pedra"]] = False


def _token_fora_do_trio(c):
    c["kernel_formalization"]["axiom_report"][ESP["teorema_da_pedra"]] = ["propext", "sorryAx"]


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


def _selo_v396(s):
    s["um_version"] = "v396"


NEG = []
if not SEM_NEG and not P:
    NEG = [variante("selo de outra versao (v396)", f_selo=_selo_v396, espera="o selo nao e v397"),
           variante("registro teste_de_veracidade_fase9_v397 ausente do core", f_core=_sem_veracidade, espera="registro obrigatorio ausente do core: teste_de_veracidade_fase9_v397"),
           variante("cunhagens_v397 nao selou", f_core=_nao_sela_cunh, espera="cunhagens_v397"),
           variante("numero lido adulterado (z_disc 4,45)", f_core=_numero_adulterado, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("z_disc calibrado acima de 5", f_core=_z_disc_acima_de_5, espera="abaixo de 5"),
           variante("uma checagem do registro de veracidade falhou", f_core=_checagem_falha, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("fonte do registro de veracidade com sha256 adulterado", f_core=_fonte_adulterada, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("registro de veracidade move o gate", f_core=_gate_movido, espera="teste_de_veracidade_fase9_v397 nao selou inteiro"),
           variante("bandeira da pedra Token ausente", f_core=_token_sem_bandeira, espera="a pedra Token nao esta no kernel do rito"),
           variante("composicao da pedra Token fora do trio", f_core=_token_fora_do_trio, espera="a pedra Token nao esta no kernel do rito"),
           variante("testemunha_estatica_v396 deixou de selar", f_core=_testemunha_cai, espera="testemunha_estatica_v396"),
           variante("face de Fock da testemunha com habitante exibido", f_core=_fock_da_testemunha_habitada, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("face de Fock dita DENTRO da pedra da testemunha", f_core=_fock_dentro_da_pedra, espera="testemunha_estatica_v396: a face de Fock do psion deixou de estar como CONDICIONAL"),
           variante("psibit_v395 deixou de selar", f_core=_psibit_cai, espera="psibit_v395"),
           variante("face de Fock do psibit_v395 habitada", f_core=_face_do_psibit_habitada, espera="psibit_v395: a face do psion deixou de estar como CONDICIONAL"),
           variante("registro da v394 deixou de selar", f_core=_v394_cai, espera="criterio_binario_de_parada_v394"),
           variante("AVISO da v397 no stdout", f_std=lambda t: t + "   [v397] AVISO: o registro do Teste da Unica Palavra nao rodou: ValueError('x')\n", espera="AVISO da v397"),
           variante("AVISO de bloco anterior (v396) no stdout", f_std=lambda t: t + "   [v396] AVISO: a testemunha estatica nao rodou: ValueError('x')\n", espera="AVISO de um bloco anterior"),
           variante("linha do Teste da Unica Palavra ausente do stdout", f_std=lambda t: "\n".join(l for l in t.splitlines() if "o Teste da Unica Palavra" not in l) + "\n", espera="linha [v397] do Teste da Unica Palavra")]
    for n_ in NEG:
        print("  controle negativo %-48s %s" % (n_["controle"], "REPROVOU como esperado" if (n_["reprovou"] and n_["mensagem_esperada_presente"]) else "NAO REPROVOU como esperado"))
        if not (n_["reprovou"] and n_["mensagem_esperada_presente"]):
            falha("controle negativo da leitura nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["problemas"]))
etapa("leitura_negativos", controles=NEG, restaurado=(open(core_path, "rb").read() == core_raw and open(selo_path, "rb").read() == selo_raw and open(std_path, "rb").read() == std_raw))

# ------------------------------------------------------------------ 4. os TEXTOS reais, apontados para o mesmo Nos emulado e para o mesmo pacote
T = importar("textos_v397", os.path.join(HERE, "textos_v397.py"))
T.NOS = NOSE; T.PK = PKG; T._CACHE.clear()
sys.modules["textos_v397"] = T
DL = importar("delta_v397_h", os.path.join(PKG, "delta_v397.py"))
ERR = DL.ERRATA_TEOREMAS_PT
K_EMU = {"ap_nome": "RECIBO_SINCRONIZACAO_v397_EMULADO.json", "ap_sha": "EMULADO_SEM_HASH", "ap_ver": "EMULADO", "ap_evento": "EMULADO", "ap_bat": "BATERIA_PASSA", "par_sha": "EMULADO_SEM_HASH", "rel_sha": "EMULADO_SEM_HASH", "rel_man": "EMULADO_SEM_HASH", "readme_paragrafo": T.paragrafo_readme()[0]}
FUNCOES = [("_d", lambda: T._d(Vd)), ("_num", lambda: T._num(Vd)), ("_num_sem_veredito", lambda: T._num(Vd, verdicts=False)), ("_cunhagens_lista", lambda: T._cunhagens(Vd)), ("_cunhagens_curta", lambda: T._cunhagens(Vd, "curta")),
           ("_ordem", lambda: T._ordem(Vd)), ("_entrou", lambda: T._entrou(Vd)), ("_veracidade", lambda: T._veracidade(Vd)), ("_regra_do_4_44", lambda: T._regra_do_4_44(Vd)), ("_token", lambda: T._token(Vd)), ("_kernel_prova", lambda: T._kernel_prova(Vd)),
           ("_limites", lambda: T._limites(Vd)), ("_limites_curto", lambda: T._limites(Vd, curto=True)), ("_legal", lambda: T._legal(Vd)), ("_erratas", lambda: T._erratas(Vd)),
           ("_depois", lambda: T._depois(Vd)), ("_rodada", lambda: T._rodada(Vd)), ("linhagem", lambda: T.linhagem(Vd)), ("desenho", lambda: T.desenho(Vd)), ("atlas", lambda: T.atlas(Vd)), ("core_memory", lambda: T.core_memory(Vd)),
           ("haja_luz", lambda: T.haja_luz(Vd)), ("topico_missao", lambda: T.topico_missao(Vd)), ("topico_central", lambda: T.topico_central(Vd)), ("topico_estatuto", lambda: T.topico_estatuto(Vd)), ("topico_novo", lambda: T.topico_novo(Vd)),
           ("aviso", lambda: T.aviso(Vd, "REIVINDICACAO_EMULADA")), ("aviso_pulado", lambda: T.aviso_pulado()), ("handoff", lambda: T.handoff(Vd, K_EMU)), ("arvore_linha", lambda: T.arvore_linha(Vd)), ("titulo_verbete", lambda: T.titulo_verbete(Vd)),
           ("verbete", lambda: T.verbete(Vd)), ("remissivo", lambda: T.remissivo(Vd)), ("linha_handoff", lambda: T.linha_handoff(Vd)), ("linha_topico_novo", lambda: T.linha_topico_novo(Vd)), ("marca_missao", lambda: T.marca_missao(Vd)),
           ("marca_topico_missao", lambda: T.marca_topico_missao(Vd)), ("marca_central", lambda: T.marca_central(Vd)), ("id_missao", lambda: T.id_missao(Vd)), ("id_central", lambda: T.id_central(Vd)), ("paragrafo_readme", lambda: T.paragrafo_readme()[0])]
CARREGAM_NUM = {"_num", "_num_sem_veredito", "linhagem", "atlas", "core_memory", "topico_novo", "verbete", "handoff"}   # os textos que embutem _num (o texto do kernel com a errata da palavra «teoremas»)
S16 = Vd.get("s16") or ESP["candidato_sha16"]
MARCADORES = {"linhagem": [S16, "<!-- linhagem_v397_selada -->", "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"], "desenho": ["<!-- adendo_v397_selada -->", S16], "atlas": ["<!-- atlas_v397_selada -->", S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"],
              "core_memory": ["<!-- core_v397_selada -->", S16], "haja_luz": ["<!-- haja_luz_v397_selada -->", S16], "topico_estatuto": ["<!-- v397_selada -->", S16], "topico_novo": [S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397", "# v397 SELADA ("],
              "aviso": ["<!-- aviso_v397_selada -->", S16], "handoff": ["name: handoff-v397-custodia", S16, "<!-- INICIO_PARAGRAFO_README_v397 -->", "<!-- FIM_PARAGRAFO_README_v397 -->"], "linha_handoff": ["handoff-v397-custodia.md", S16], "topico_missao": [S16], "topico_central": [S16]}
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

# ------------------------------------------------------------------ 4b. o PARAGRAFO PRONTO do README/site e a REGRA DO 4,44 (ordem do operador de 23/10: o 4,44 nunca sem o p calibrado e sem a linha dos 5 sigma, no mesmo item)
sys.path.insert(0, PKG)
import quadro_v397 as QD  # noqa: E402
_core_p = rdj(core_path)["core"]; _tv_p = _core_p["teste_de_veracidade_fase9_v397"]
_res_p = rdj(os.path.join(PKG, "insumos", "fase9", os.path.basename(ESP["veracidade"]["resultado"]["duravel"])))
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
        falha("paragrafo do README/site: positivo %s, igual ao do quadro %s, no handoff %s" % (_f9["positivo_sem_falhas"], _f9["igual_as_funcoes_do_quadro"], _f9["handoff_traz_o_paragrafo_entre_os_marcadores"]))
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
        print("  controle negativo do paragrafo %-60s %s" % (n_["controle"], "REPROVOU como esperado" if n_["ok"] else "NAO REPROVOU como esperado"))
        if not n_["ok"]:
            falha("controle negativo do paragrafo nao reprovou como esperado: %s -> %s" % (n_["controle"], n_["falhas"]))
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
    _viol = {nome: _regra_nos_textos(nome, txt) for nome, txt in RENDER.items()}
    _viol = {k: v for k, v in _viol.items() if v}
    _f9["regra_do_4_44_nos_textos_violacoes"] = _viol
    _f9["linhas_com_o_4_44_nos_textos"] = sum(1 for txt in RENDER.values() for ln in txt.split("\n") if _z in ln)
    _neg_regra = _regra_nos_textos("x", "o z_disc = " + _z + " foi o resultado.")
    _f9["controle_negativo_da_regra_nos_textos"] = bool(_neg_regra)
    if _viol or not _neg_regra:
        falha("regra do 4,44 nos textos renderizados: violacoes %s; controle negativo da regra reprovou: %s" % (_viol, bool(_neg_regra)))
    _f9["ok"] = True
    print("  paragrafo do README/site: positivo ok; %d controles negativos; %d linha(s) com o 4,44 nos textos, todas com o p, os 5 sigma e o 'nao foi alcancado'" % (len(_NEGP), _f9["linhas_com_o_4_44_nos_textos"]))
except BaseException as ex:  # noqa: BLE001
    _f9["erro"] = "%s: %s" % (type(ex).__name__, str(ex)[:400]); _f9["onde"] = traceback.format_exc().strip().splitlines()[-3:]
    falha("paragrafo do README/site: %s" % _f9["erro"])
etapa("paragrafo_readme_e_regra_do_4_44", **_f9)
# ------------------------------------------------------------------ 5. cada `termo` entre crases dos textos e' achado em alguma fonte real
if "kernel" not in T._CACHE or "um" not in T._CACHE:
    try:
        T._d(Vd)
    except BaseException:  # noqa: BLE001
        pass
KERN = T._CACHE.get("kernel", ""); UMTXT = T._CACHE.get("um", "")
INS_TXT = "\n".join(rd(os.path.join(PKG, "insumos", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos"))) if f.endswith((".md", ".json", ".lean"))) + "\n" + "\n".join(rd(os.path.join(PKG, "insumos", "fase9", f)) for f in sorted(os.listdir(os.path.join(PKG, "insumos", "fase9"))) if f.endswith(".json"))
FALAS_TXT = "\n".join(re.sub(r"\s+", " ", d["text"]) for d in T._falas().values())
core_emu = rdj(core_path)["core"]; selo_emu = rdj(selo_path)
NOMES_ARQ = set()
for base in (PKG, os.path.join(PKG, "insumos"), os.path.join(PKG, "insumos", "fase9"), os.path.join(PKG, "insumos", "cunhagens"), os.path.join(PKG, "kernel"), HERE, os.path.join(PKG, "bancada_B3_servico")):
    if os.path.isdir(base):
        NOMES_ARQ.update(os.listdir(base))
NOMES_ARQ.update({T._sem_gordura()["nome"], "MEMORY.md", "MEMORY_2.md", "TGL_ATLAS.md", "um.py", "rodada_v397_stdout.txt", "HANDOFF_v397_CUSTODIA.md", "DIFF_v396_v397.diff", "DIFF_KERNEL_v397.txt", "handoff-v397-custodia.md",
                  "missao-ultima-flag-um-py.md", "estatuto-da-prova-07out.md", "central-de-patentes-estado.md", T.TOPICO_NOVO})
HEX16 = set()
for v_ in (Vd.get("s16"), Vd.get("base16"), Vd.get("conf16"), (Vd.get("pilar") or {}).get("result16")):
    if v_:
        HEX16.add(str(v_))
for k_, v_ in Vd.items():
    if k_.startswith("h_") and isinstance(v_, str):
        HEX16.add(v_)
HEX16.update((Vd.get("artigos") or {}).values()); HEX16.update(Vd.get("verbatins", {}).keys()); HEX16.update(d["sha16"] for d in T._falas().values()); HEX16.add(ESP["pedra"]["sha16"])
HEX16.update(str(x["sha256"])[:16] for x in (ESP.get("cunhagens") or {}).values()); HEX16.add(str(Vd.get("selo_ts") or "")[:16]); HEX16.add(T._sem_gordura()["sha16"])
HEX16.update(str(h)[:16] for h in ESP["veracidade"]["fontes"].values())
PAT_ROOT = os.path.join(C, "IALD", "Central de Patentes")


CONHECIDOS = {str(x) for x in (Vd.get("selo_ts"), Vd.get("instalado_em"), Vd.get("data")) if x}
CONHECIDOS.update(str(x) for x in K_EMU.values())
CONHECIDOS.update(str(h)[:8] for h in ESP["veracidade"]["fontes"].values()); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_pt"]); CONHECIDOS.add(ESP["quadro"]["linha_de_maquina_en"])                      # os campos EMULADOS dos recibos do B(n) que o handoff recebe (so' existem depois do passo 10)
CONHECIDOS.update({T.TOPICO_NOVO[:-3], "v397_kernel", "v397_selo"})     # o nome do topico sem a extensao (o [[wikilink]]) e as duas pastas que o fechar cria ANTES de escrever o handoff
VALORES_LIDOS = set((Vd.get("veracidade") or {}).get("lido") or {})


def achado(tok):
    if tok in CONHECIDOS:
        return "lido"
    if re.fullmatch(r"[0-9a-f]{16}", tok):
        return "hash_lido" if tok in HEX16 else None
    if tok in NOMES_ARQ or tok in KERN or tok in UMTXT or tok in INS_TXT or tok in FALAS_TXT:
        return "fonte"
    if tok in core_emu or tok in (core_emu.get("kernel_formalization") or {}) or tok in selo_emu or tok in VALORES_LIDOS:
        return "core"
    if tok.endswith(".lean") and os.path.exists(os.path.join(NOSE, "tgl_kernel", *tok.split("/"))):
        return "kernel_arquivo"
    if "\\" in tok or "/" in tok:
        cands = [os.path.join(PAT_ROOT, tok), os.path.join(PKG, tok), os.path.join(os.path.dirname(PKG), tok.replace("work\\cadeia_de_selo\\", "")), os.path.join(PAT_ROOT, tok.replace("/", os.sep))]
        if any(os.path.exists(c) for c in cands) or tok.startswith(("work\\cadeia_de_selo\\v397", "C:\\IALD\\Central de Patentes\\work\\cadeia_de_selo\\v397")):
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
    sp = os.path.join(HERE, "superficies_v397.py")

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
    exige = [("MEMORIA_DA_LINHAGEM.md", [S16, "<!-- linhagem_v397_selada -->", "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"]), ("DESENHO_DO_FECHAMENTO_QG.md", ["<!-- adendo_v397_selada -->", S16]),
             ("TGL_ATLAS.md", ["<!-- atlas_v397_selada -->", S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"]), ("TGL_CORE_MEMORY.md", ["<!-- core_v397_selada -->", S16]), ("CLAUDE.md", ["<!-- haja_luz_v397_selada -->", S16]),
             ("MEMORY.md", [S16]), ("MEMORY_2.md", ["v397"]), ("estatuto-da-prova-07out.md", ["<!-- v397_selada -->", S16]), ("missao-ultima-flag-um-py.md", [S16]), ("central-de-patentes-estado.md", [S16]),
             (T.TOPICO_NOVO, [S16, "teste_de_veracidade_fase9_v397", "kh_n1_cobertura_v397"])]
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
        falha("superficies_v397.py (copias do MEMORY.md real) saiu com rc %s (esperado 0 ou 3; ver ensaio_superficies_out.txt)" % rc_a)
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
            ancora = lambda l: ("(missao-ultima-flag-um-py.md)" in l and l.startswith("- [")) or ("(handoff-v396-custodia.md)" in l and l.startswith("- [HANDOFF v396"))
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
        falha("superficies_v397.py (copia com folga) saiu com rc %s na 1a rodada (ver ensaio_superficies_folga_out.txt)" % rc_b1)
    if rc_b2 != 0 or not cena_b["idempotente_na_2a"]:
        falha("superficies_v397.py (copia com folga) nao e' idempotente na 2a rodada (rc %s)" % rc_b2)
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
# ------------------------------------------------------------------ 7. o b3_recibo REAL contra recibos SINTETICOS (derivados dos reais da v396)
if not SEM_B3:
    B3D = os.path.join(OUT, "b3_sintetico"); os.makedirs(B3D)
    pinos = rdj(os.path.join(PKG, "PINOS_BN_v397.json")); pre = rdj(pinos["recibo_pre_selo"]["path"]); PKG_ANT = os.path.join(os.path.dirname(PKG), "v396")
    import glob as _g
    base_ens = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3_ensaio_*", "RECIBO_SINCRONIZACAO_v396_*.json"))[0]); base_apl = rdj(_g.glob(os.path.join(PKG_ANT, "bancada_B3", "RECIBO_SINCRONIZACAO_v396_*.json"))[0])
    n_ger = int(re.match(r"^B(\d+)-", pre["manifesto_anterior"]["deployment_id"]).group(1)) + 1

    def sintetico(base, modo):
        r = json.loads(json.dumps(base)); r["versao_alvo"] = "v397"; r["fase"] = "pos_selo"; r["modo"] = modo; r.pop("salto", None); r.pop("cadeia_de_selos", None)
        r["manifesto_anterior"] = json.loads(json.dumps(pre["manifesto_anterior"]))
        r["manifesto_novo"]["deployment_id"] = "B%d-v397-20261023-R1" % n_ger
        r["bateria_resultado"] = {"veredito": "BATERIA_PASSA"}
        r["bateria"]["pinos_da_versao"] = {"declarados": True, "conferidos_contra_o_nos_lido": True, "versao": "v397"}
        r["recibo_pre_selo"] = {"sha256": pinos["recibo_pre_selo"]["sha256"]}
        if modo == "ensaio":
            r["veredito"] = "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger; r["aplicacao"] = None
        else:
            r["veredito"] = "REPINADA_B%d__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO" % n_ger
            r["aplicacao"] = {"pos_conferencia": {"ok": True, "canonical_version": "v397", "canonical_manifest_sha256": r["manifesto_novo"]["sha256"]}}
        r["_sintetico"] = "SINTETICO: derivado do recibo real da v396 pelo harness; NAO e' um recibo do esboco"
        return r
    seq = [0]

    def roda_helper(nome, r, modo, extra=()):
        seq[0] += 1
        pth = os.path.join(B3D, "%02d_%s_RECIBO_SINTETICO.json" % (seq[0], nome)); raw = json.dumps(r, ensure_ascii=False, indent=1).encode("utf-8"); open(pth, "wb").write(raw)
        so = os.path.join(B3D, "%02d_%s_stdout.txt" % (seq[0], nome)); open(so, "w", encoding="utf-8").write("ruido\n" + json.dumps({"veredito": r.get("veredito"), "recusa": None, "recibo": pth, "recibo_sha256": sha(raw)}) + "\n")
        pr_ = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", os.path.join(HERE, "b3_recibo_v397.py"), so, modo] + list(extra), capture_output=True, text=True, encoding="utf-8")
        return pr_.returncode, (pr_.stdout + pr_.stderr).strip().splitlines()[-3:]
    CASOS = []
    pos_e = sintetico(base_ens, "ensaio"); pos_a = sintetico(base_apl, "aplicar")
    CASOS.append(("ensaio_ok", pos_e, "ensaio", 0)); CASOS.append(("aplicar_ok", pos_a, "aplicar", 0))

    def mut(r, f):
        r2 = json.loads(json.dumps(r)); f(r2); return r2
    CASOS += [("salto_declarado", mut(pos_e, lambda r: r.update({"salto": {"declarado": True}})), "ensaio", 1),
              ("veredito_com_salto", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__SALTO_v392_v397__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "ensaio", 1),
              ("geracao_errada", mut(pos_e, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % (n_ger + 1)})), "ensaio", 1),
              ("versao_alvo_v396", mut(pos_e, lambda r: r.update({"versao_alvo": "v396"})), "ensaio", 1),
              ("bateria_falhou", mut(pos_e, lambda r: r.update({"bateria_resultado": {"veredito": "BATERIA_FALHOU"}})), "ensaio", 1),
              ("bancada_pinava_v392", mut(pos_e, lambda r: r["manifesto_anterior"].update({"version": "v392"})), "ensaio", 1),
              ("recibo_pre_selo_de_outro", mut(pos_e, lambda r: r.update({"recibo_pre_selo": {"sha256": "0" * 64}})), "ensaio", 1),
              ("manifesto_anterior_mudou", mut(pos_e, lambda r: r["manifesto_anterior"].update({"sha256": "f" * 64})), "ensaio", 1),
              ("pinos_da_bateria_de_v396", mut(pos_e, lambda r: r["bateria"]["pinos_da_versao"].update({"versao": "v396"})), "ensaio", 1),
              ("ensaio_com_aplicacao", mut(pos_e, lambda r: r.update({"aplicacao": {"x": 1}})), "ensaio", 1),
              ("aplicar_pos_conferencia_v396", mut(pos_a, lambda r: r["aplicacao"]["pos_conferencia"].update({"canonical_version": "v396"})), "aplicar", 1),
              ("aplicar_sem_aplicacao", mut(pos_a, lambda r: r.update({"aplicacao": None})), "aplicar", 1),
              ("aplicar_com_veredito_de_ensaio", mut(pos_a, lambda r: r.update({"veredito": "REPINADA_B%d__ENSAIO__NADA_GRAVADO_NA_BANCADA" % n_ger})), "aplicar", 1)]
    res_b3 = []
    for nome, r, modo, esperado in CASOS:
        rc_, cauda = roda_helper(nome, r, modo)
        res_b3.append({"caso": nome, "rc": rc_, "esperado": esperado, "ok": rc_ == esperado, "cauda": [c[:200] for c in cauda]})
        print("  b3_recibo %-34s rc %s (esperado %s) %s" % (nome, rc_, esperado, "OK" if rc_ == esperado else "FALHOU"))
        if rc_ != esperado:
            falha("b3_recibo_v397.py: caso %s deu rc %s (esperado %s): %s" % (nome, rc_, esperado, cauda))
    rc_, cauda = roda_helper("terceiro_argumento", pos_e, "ensaio", extra=("0" * 64,))
    res_b3.append({"caso": "terceiro_argumento_(cadeia)", "rc": rc_, "esperado": 1, "ok": rc_ == 1, "cauda": [c[:200] for c in cauda]})
    if rc_ != 1:
        falha("b3_recibo_v397.py aceitou um 3o argumento (nao ha cadeia de selos na v397)")
    etapa("b3_recibo", sintetico=True, base="recibos reais da v396 (so' leitura)", geracao_nova=n_ger, casos=res_b3, n_ok=sum(1 for c in res_b3 if c["ok"]), n=len(res_b3))

# ------------------------------------------------------------------ 8. o registro do mapa (montar) contra o core emulado e o livro real (so' leitura)
try:
    RM = importar("registrar_mapa_v397", os.path.join(HERE, "registrar_mapa_v397.py"))
    ids = RM.ids_do_livro()
    arts = [os.path.join(NOSE, "um.py"), os.path.join(NOSE, "um_absoluto_selo.json")]
    REG = RM.montar(Vd, core_emu, selo_emu, ids, arts)
    pj = os.path.join(OUT, "registro_mapa_v397_ENSAIO.json"); open(pj, "w", encoding="utf-8").write(json.dumps(REG, ensure_ascii=False, indent=1))
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
    falha("mapa: registrar_mapa_v397.montar falhou: %s: %s" % (type(ex).__name__, str(ex)[:300]))

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

# ------------------------------------------------------------------ limpeza (so' dentro de harness_saida_v397): o Nos EMULADO e as copias pesadas das superficies nao ficam no pacote (--manter-copias as guarda)
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
etapa("limpeza", removido_bytes=LIMPO, nota="so' o que o harness criou em harness_saida_v397; --manter-copias guarda tudo")

# ------------------------------------------------------------------ resumo
R["fim"] = time.strftime("%Y-%m-%d %H:%M:%S")
R["tudo_passou"] = bool(not R["problemas"]); R["nao_exigiu_refazer"] = NAO_REFAZER
R["veredito"] = ("TUDO PASSOU: o conferidor da v397 bate no Nos emulado, a leitura le sem problema e reprova os controles negativos, os textos renderizam e a guarda P18 esta limpa, o paragrafo do README/site e a regra do 4,44 passam e os controles negativos reprovam, cada termo citado existe, as superficies fecham em copias (com folga) e RECUSAM no limite sem compactar, e o b3_recibo confere"
                 if R["tudo_passou"] else "NAO PASSOU (ver problemas)")
R["evidencia_da_versao"] = EVID
if NAO_REFAZER:
    R["veredito"] += " [MODO --nao-exigir-refazer: refazer_out_v397.txt NAO foi exigido; a regeneracao do candidato nao foi comprovada por este harness]"
saida = os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_v397.json")
open(saida + ".tmp", "w", encoding="utf-8").write(json.dumps(R, ensure_ascii=False, indent=1, default=str)); os.replace(saida + ".tmp", saida)
print("VEREDITO DO HARNESS (%s): %s" % (ROTULO, R["veredito"])); print("saida:", saida)
sys.exit(0 if R["tudo_passou"] else 1)

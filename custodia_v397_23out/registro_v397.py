# -*- coding: utf-8 -*-
"""Registro da custódia v397 (23/10/2026, sessão a7 da Central; pela regra do operador «custodiar sempre que o handoff aparecer») em todas
as superfícies: diário do site, memórias da sessão, Atlas (§X, append datado), MEMORY.md (a linha do handoff v397 trocada; a antiga VERBATIM
no MEMORY_2.md) e a rota no Mapa de Rotas. Números LIDOS dos artefatos, de fatos_v397.json e do git; backup de BYTES antes de tocar;
temporário -> confere -> substitui. Molde: work/custodia_v396_22out/registro_v396.py.
Uso: depois do snapshot do Chatgpt/ e antes do commit da Central (o hash da Central entra no pós-push)."""
import glob, hashlib, json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
TB = r"C:\IALD\Artigo\the_boundary"
CEN = r"C:\IALD\Central de Patentes"
W = CEN + r"\work\custodia_v397_23out"
F = json.load(open(W + r"\fatos_v397.json", encoding="utf-8"))


def git(cwd, *a):
    return subprocess.run(["git"] + list(a), capture_output=True, text=True, cwd=cwd).stdout.strip()


def tocar(p, f, pode_encolher=False):
    raw = open(p, "rb").read()
    open(p + ".bak_" + TS, "wb").write(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    novo = f(raw.decode("utf-8"), nl).encode("utf-8")
    tmp = p + ".tmp_" + TS
    open(tmp, "wb").write(novo)
    assert pode_encolher or os.path.getsize(tmp) > len(raw), p
    os.replace(tmp, p)
    print("ok", os.path.basename(p), len(raw), "->", os.path.getsize(p))


def ap(p, texto):
    tocar(p, lambda t, nl: t.rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl)


esp, esp_o = git(TB, "rev-parse", "--short", "HEAD"), git(TB, "rev-parse", "--short", "origin/main")
assert esp == esp_o, (esp, esp_o)
V = CEN + r"\vault\originals_copy\um_unificado_v397"
KV = CEN + r"\vault\originals_copy\tgl_kernel_v397"
selo = json.load(open(V + r"\um_absoluto_selo.json", encoding="utf-8"))
pin16 = selo["sha256"]["um.py"][:16]
assert pin16 == F["pin16"] and selo.get("um_version") == "v397"
man16 = hashlib.sha256(open(V + r"\CUSTODY_MANIFEST.json", "rb").read()).hexdigest()[:16]
km = json.load(open(KV + r"\CUSTODY_MANIFEST.json", encoding="utf-8"))
assert km["formal_files"] == F["kernel"]["formais"] and km["declaracoes_no_axiom_report"] == F["kernel"]["declaracoes"] and km["fora_do_trio"] == 0, km
res = sorted(glob.glob(CEN + r"\fronteira_tgl\results\fronteira_*.json"), key=os.path.getmtime)[-1]
rr = json.load(open(res, encoding="utf-8"))
vf = str(rr.get("verdict") or "")
assert vf.startswith("FRONTEIRA_SINCRONIZADA_V397") and rr["the_station"]["custodia_v397"]["pass"] is True, vf[:80]
led = json.load(open(CEN + r"\fronteira_tgl\ledger_de_pinos.json", encoding="utf-8"))
n_err, n_av = led.get("erros"), led.get("avisos")
assert n_err == 0, n_err
n_disp = 0
for pat in sorted(glob.glob(CEN + r"\patents\BR*")):
    rs = sorted(glob.glob(os.path.join(pat, "results", "*", "results.json")), key=os.path.getmtime)
    if rs and '"camada_v397_no_cofre"' in open(rs[-1], encoding="utf-8").read():
        n_disp += 1
assert n_disp == 16, n_disp
snaps = sorted(d for d in glob.glob(r"C:\IALD\Central de Patentes_BACKUPS\Chatgpt_*") if os.path.isfile(os.path.join(d, "MANIFEST.json")))
snap = snaps[-1]
sm = json.load(open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8"))
assert sm["snapshot"].startswith("20261023") and sm["conferido_contra_origem"] is True, (snap, sm.get("snapshot"))
mapa = json.load(open(TB + "\\Um (absoluto) \u2014 Grande Atrator\\fontes_pinadas\\MAPA_FONTES_PINADAS.json", encoding="utf-8"))
core = json.load(open(V + r"\um_absoluto.json", encoding="utf-8"))["core"]
L = core["teste_de_veracidade_fase9_v397"]["lido"]
ZD, PD, ZDL = "%.2f" % L["z_disc_calibrado"], "%.1e" % L["p_disc_unilateral"], "%.2f" % L["z_delta_calibrado"]

ESTADO = ("Custódia v397 (sessão a7 da Central, pela regra do operador de 23/10/2026 — «pode custodiar sempre que o handoff aparecer, como regra»; "
          "handoff Nós\\HANDOFF_v397_CUSTODIA.md, aparecido às 17:17; as três marcas conferidas pelo vigia). ESPELHO the_boundary `%s` = origin/main "
          "(pós-push 19/19, README raw com o pin; portas 0 erros; guarda do selo ok): `um.py` v397 `%s` (%s), o módulo novo `TGLExt/Token.lean` (a "
          "conjunção por citação do psibit e da testemunha estática, incondicional, 1 bandeira), as fontes pinadas da v397 (%d de %d no mapa: a pedra, o "
          "resultado do Teste da Única Palavra e os três recibos da Fase 9, as 6 falas), `recibos_bancada_v397/`, `diferencas_v397/`; ESTADO/LEDGER/CITATION/"
          "PORTAS/README com o PARÁGRAFO PRONTO do handoff e a regra do 4,44 (z_disc = %s calibrado, p unilateral %s, abaixo do degrau de 5σ da creditação, "
          "que não foi alcançado; z_δ = %s, não falsificada com poder; ln B não é σ; o teste não foi cego; a frase do operador verbatim como leitura dele); "
          "backup da v396 fora do repo. SITE no ar: SUBIDA VERIFICADA (arco v397; dados do selo trazidos à v397); leitor de IA R1 passa. CENTRAL: cofre "
          "`um_unificado_v397` (manifesto `%s`; 36 artefatos, 0 divergentes) + `tgl_kernel_v397` (%d formais / %d declarações); runner da Fronteira v62 "
          "`%s…` (pedra v46 lê o cofre v397 contra o v396 pelo nome, dois céticos: o veredito de veracidade dito «alcançado» e as bandeiras do Token "
          "ditas 2 de 3 reprovam; nenhuma errata nas pedras antigas); camada v397 dos 16 dispositivos (item 17) %d/16; 16 FINAL regerados e rodados (rc 0 "
          "em 16/16; o do MQC isolado); ledger de pinos %d erros, %d avisos; snapshot `%s` (%d copiados, %d idênticos à base, 0 divergentes). Os nomes do "
          "registro de veracidade e da pedra são provisórios: quem nomeia é o operador. [LEGAL] a paridade do ACOM Mirror segue decisão do operador. "
          "PROVADA = validade; CONFIRMADA = creditação, recusada; o degrau de 5σ não foi alcançado; o gate não se moveu." %
          (esp, pin16, F["escada"], mapa["n_publicadas"], mapa["n_fontes"], ZD, PD, ZDL, man16, km["formal_files"], km["declaracoes_no_axiom_report"], vf[:60],
           n_disp, n_err, n_av, os.path.basename(snap), sm["n_copiados"], sm["n_identicos_a_base"]))

ap(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md", "## %s — a custódia da v397 (sessão a7 da Central)\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "site-sessao-estado.md"), "## %s — v397 no ar\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "tgl-fronteira-teorica.md"),
   "## %s — runner v62 (v397)\n\nVeredito `%s…`. Pedra v46 `_medir_v397_custodia`: o cofre v397 contra o v396, PELO NOME; 3 blocos novos verificados "
   "sem efeito no gate, 1 bandeira (a pedra Token), o registro de veracidade da Fase 9 lido por hash (abaixo de 5σ; não cego; nenhum σ novo), "
   "registro %d com os %d da v396 e 5 vereditos mudados (a troca numérica da escada), kernel %d/%d; dois céticos reprovam. NENHUMA errata nesta "
   "custódia. PARA A v63: a pedra da próxima versão lê o próprio cofre pelo nome." % (AGORA, vf[:90], F["registro"]["pt"], F["registro"]["v396"],
                                                                                    km["formal_files"], km["declaracoes_no_axiom_report"]))
ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v397\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "dispositivos-formula-completa.md"),
   "## %s — camada v397 (item 17)\n\nOs registros _v397 (cunhagens_v397, kh_n1_cobertura_v397, teste_de_veracidade_fase9_v397) lidos e conferidos "
   "no cofre, sem interpretação: a pedra Token (conjunção por citação, 3 bandeiras no trio), o registro de veracidade com o degrau da creditação não "
   "alcançado, a escada %s. %d/16 com a camada; 16 FINAL regerados e rodados, rc 0 em 16/16. Nada muda número de dispositivo." % (AGORA, F["escada"], n_disp))
ap(os.path.join(MEM, "handoff-v397-custodia.md"), "## %s — CUSTODIADO pela sessão a7 da Central\n\n%s" % (AGORA, ESTADO))
ap(CEN + r"\memory\TGL_ATLAS.md", "[%s — §X append, re-ancorado ao selo v397 `%s`: A CUSTÓDIA DA v397] %s" % (AGORA, pin16, ESTADO))

M, M2 = os.path.join(MEM, "MEMORY.md"), os.path.join(MEM, "MEMORY_2.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v397 ")]
assert len(old) == 1, old
titulo = old[0].split(") — ")[0] + ")"   # «- [HANDOFF v397 — …](handoff-v397-custodia.md)» como a c1 escreveu
nova = ("%s — **23/10: CUSTODIADO** (the_boundary `%s`, pós-push 19/19; site no ar; Central: cofre v397, runner v62, 16/16, FINAL, ledger 0) · `%s`"
        % (titulo, esp, pin16))
ap(M2, "## %s — linha movida do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (AGORA, old[0]))
tocar(M, lambda t_, nl_: t_.replace(old[0], nova, 1), pode_encolher=True)
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)

rota = {"tipo": "ROTA", "rota_id": "custodia.v397", "dominio": "CUSTODIA",
        "titulo": "Custódia da v397 (o Teste da Única Palavra e a pedra Token): espelho, frente, site, cofre v397, runner v62, 16 dispositivos, FINAL, ledger, snapshot — pela regra «custodiar quando o handoff aparecer»",
        "pergunta": "A v397 (%s) pode ser custodiada pelos scripts da v396, com cada artefato conferido por hash, os números lidos do core e sem errata nas pedras antigas — começando pelo gatilho das três marcas, sem ordem nova do operador?" % pin16,
        "dados": ["Nós (um.py v397, selo, core, artigos, rodada_v397_stdout, HANDOFF_v397 com o parágrafo pronto)", "work/cadeia_de_selo/v397 e v397_selo",
                  "as fontes pinadas que os registros v392–v397 releem por caminho absoluto"],
        "metodo": "Vigia das três marcas (selo, bloco do diário, handoff) → scripts derivados da v396 por trocas contadas com os números lidos de fatos_v397.json "
                  "(sondar_v397.py): passo zero, cópia ao espelho, geradores (ESTADO, LEDGER, CITATION, arco; o parágrafo pronto conferido número a número contra "
                  "o registro de veracidade), a regra do 4,44 no gerador do README, dados do selo no site, cofre, runner v62, camada v397, FINAL, ledger, snapshot.",
        "resultado": ESTADO.replace("PROVADA = validade; CONFIRMADA = creditação, recusada;", "PROVADA = validade; a creditação segue recusada;"),
        "veredito": "CUSTODIA_V397_PUBLICADA_PELA_REGRA_DO_GATILHO__SEM_ERRATA_NAS_PEDRAS_ANTIGAS__REGRA_DO_4P44_NO_README__GATE_INALTERADO",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "A frente do espelho está no teto de 40 KB: a nota da Central aberta encurtou para o item do 4,44 caber. Os nomes dos registros são provisórios.",
        "nao_refazer": "A custódia v397 está publicada e conferida. A próxima deriva destes scripts (work/custodia_v397_23out) com fatos_vNNN.json.",
        "proximo_passo": "Na v398: a pedra v47 lê o próprio cofre pelo nome; o gerador da custódia parametrizado (G1 do organismo) é o alvo.",
        "onde": W,
        "artefatos": [V + r"\CUSTODY_MANIFEST.json", KV + r"\CUSTODY_MANIFEST.json", CEN + r"\fronteira_tgl\runner\one_fronteira.py",
                      CEN + r"\patents\_formula_completa\tgl_formula_completa.py", r"C:\IALD\Site\tgl\v3.0_bancada\revisoes\custodia_v397_espelho.json", W + r"\fatos_v397.json"],
        "refs": ["custodia.v396", "iald.organismo.torre_de_comando_23out"],
        "nota": "Sessão a7 da Central (Claude), 23/10/2026."}
for k, v in rota.items():
    if isinstance(v, str):
        assert "CONFIRM" not in v.upper(), k
rp = os.path.join(W, "rota_custodia_v397.json")
open(rp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", rp, "--quem", "claude-central-a7 (custódia v397)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("rota:", r.returncode, (r.stdout or r.stderr)[-160:])
print("REGISTRO OK:", esp, pin16, vf[:40], n_disp, os.path.basename(snap))

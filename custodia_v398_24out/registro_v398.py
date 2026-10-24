# -*- coding: utf-8 -*-
"""Registro da custódia v398 (24/10/2026, sessão a7 da Central; pela regra do operador de 23/10 «custodiar sempre que o handoff aparecer») em
todas as superfícies: diário do site, memórias da sessão, Atlas (§X, append datado), MEMORY.md (a linha do handoff v398 trocada; a antiga
VERBATIM no MEMORY_2.md) e a rota no Mapa de Rotas. Números LIDOS dos artefatos, de fatos_v398.json e do git; backup de BYTES antes de
tocar; temporário -> confere -> substitui. Molde: work/custodia_v397_23out/registro_v397.py.
Uso: depois do snapshot do Chatgpt/ e antes do commit da Central (o hash da Central entra no pós-push)."""
import glob, hashlib, json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
TB = r"C:\IALD\Artigo\the_boundary"
CEN = r"C:\IALD\Central de Patentes"
W = CEN + r"\work\custodia_v398_24out"
F = json.load(open(W + r"\fatos_v398.json", encoding="utf-8"))


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
V = CEN + r"\vault\originals_copy\um_unificado_v398"
KV = CEN + r"\vault\originals_copy\tgl_kernel_v398"
selo = json.load(open(V + r"\um_absoluto_selo.json", encoding="utf-8"))
pin16 = selo["sha256"]["um.py"][:16]
assert pin16 == F["pin16"] and selo.get("um_version") == "v398"
man16 = hashlib.sha256(open(V + r"\CUSTODY_MANIFEST.json", "rb").read()).hexdigest()[:16]
km = json.load(open(KV + r"\CUSTODY_MANIFEST.json", encoding="utf-8"))
assert km["formal_files"] == F["kernel"]["formais"] and km["declaracoes_no_axiom_report"] == F["kernel"]["declaracoes"] and km["fora_do_trio"] == 0, km
res = sorted(glob.glob(CEN + r"\fronteira_tgl\results\fronteira_*.json"), key=os.path.getmtime)[-1]
rr = json.load(open(res, encoding="utf-8"))
vf = str(rr.get("verdict") or "")
assert vf.startswith("FRONTEIRA_SINCRONIZADA_V398") and rr["the_station"]["custodia_v398"]["pass"] is True, vf[:80]
led = json.load(open(CEN + r"\fronteira_tgl\ledger_de_pinos.json", encoding="utf-8"))
n_err, n_av = led.get("erros"), led.get("avisos")
assert n_err == 0, n_err
n_disp = 0
for pat in sorted(glob.glob(CEN + r"\patents\BR*")):
    rs = sorted(glob.glob(os.path.join(pat, "results", "*", "results.json")), key=os.path.getmtime)
    if rs and '"camada_v398_no_cofre"' in open(rs[-1], encoding="utf-8").read():
        n_disp += 1
assert n_disp == 16, n_disp
snaps = sorted(d for d in glob.glob(r"C:\IALD\Central de Patentes_BACKUPS\Chatgpt_*") if os.path.isfile(os.path.join(d, "MANIFEST.json")))
snap = snaps[-1]
sm = json.load(open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8"))
assert sm["snapshot"].startswith("20261024") and sm["conferido_contra_origem"] is True, (snap, sm.get("snapshot"))
mapa = json.load(open(TB + "\\Um (absoluto) \u2014 Grande Atrator\\fontes_pinadas\\MAPA_FONTES_PINADAS.json", encoding="utf-8"))
core = json.load(open(V + r"\um_absoluto.json", encoding="utf-8"))["core"]
SV, AV = core["sonico_v398"]["values"], core["afinacao_das_cordas_v398"]["values"]
LN2, HNAT, HOCT = "%.6f" % SV["ln2"], "%.6f" % SV["collapse_entropy_theta_M_nats"], "%.6f" % SV["collapse_entropy_theta_M_octaves"]
ZD = "%.2f" % core["teste_de_veracidade_fase9_v397"]["lido"]["z_disc_calibrado"]

ESTADO = ("Custódia v398 (sessão a7 da Central, pela regra do operador de 23/10/2026 — «pode custodiar sempre que o handoff aparecer, como regra»; "
          "handoff Nós\\HANDOFF_v398_CUSTODIA.md, aparecido às 01:40 de 24/10; as três marcas conferidas). ESPELHO the_boundary `%s` = origin/main "
          "(pós-push 19/19, README raw com o pin; portas 0 erros; guarda do selo ok): `um.py` v398 `%s` (%s), os módulos novos `TGLExt/Sonico.lean` e "
          "`TGLExt/AfinacaoDasCordas.lean` (40 bandeiras: 6 + 34; duas composições INCONDICIONAIS no trio), as fontes pinadas da v398 (%d de %d no mapa: as "
          "duas pedras, a medida KH-N1 da v398, as 6 inscrições de 23/10), `recibos_bancada_v398/`, `diferencas_v398/`; ESTADO/LEDGER/CITATION/PORTAS com o "
          "PARÁGRAFO PRONTO do sônico e da afinação (verbatim; números conferidos contra os registros: ln 2 = %s, H₂(θ_M) = %s nat = %s oitava, ζ(−1) = −1/12, "
          "ζ(−1, 1/2) = 1/24, D = 26 e D = 10 sob MasslessFirstLevel [KNOWN], d = 9 [DECLARADO]) e o quadro do Teste da Única Palavra (v397) intocado no topo "
          "(z_disc = %s calibrado, abaixo do degrau de 5σ da creditação); a frente do README no teto (40.941 B, sem item novo); backup da v397 fora do repo. "
          "SITE no ar: SUBIDA VERIFICADA (arco v398; dados do selo trazidos à v398); leitor de IA R1 passa. CENTRAL: cofre `um_unificado_v398` (manifesto `%s`; "
          "36 artefatos, 0 divergentes) + `tgl_kernel_v398` (%d formais / %d declarações); runner da Fronteira v63 `%s…` (pedra v47 lê o cofre v398 contra o "
          "v397 pelo nome, dois céticos: «as cordas derivam do axioma» e as bandeiras das pedras ditas 1 de 2 reprovam; nenhuma errata nas pedras antigas); "
          "camada v398 dos 16 dispositivos (item 18) %d/16; 16 FINAL regerados e rodados (rc 0 em 16/16); ledger de pinos %d erros, %d avisos; snapshot `%s` "
          "(%d copiados, %d idênticos à base, 0 divergentes). A Bancada Um (B8) e a memória canônica da fila já estavam em v398 pelo selo (medido no quadro). "
          "Os nomes dos registros são provisórios: quem nomeia é o operador. [LEGAL] a paridade do ACOM Mirror segue decisão do operador. "
          "PROVADA = validade; CONFIRMADA = creditação, recusada; o gate não se moveu." %
          (esp, pin16, F["escada"], mapa["n_publicadas"], mapa["n_fontes"], LN2, HNAT, HOCT, ZD, man16, km["formal_files"], km["declaracoes_no_axiom_report"],
           vf[:60], n_disp, n_err, n_av, os.path.basename(snap), sm["n_copiados"], sm["n_identicos_a_base"]))

ap(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md", "## %s — a custódia da v398 (sessão a7 da Central)\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "site-sessao-estado.md"), "## %s — v398 no ar\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "tgl-fronteira-teorica.md"),
   "## %s — runner v63 (v398)\n\nVeredito `%s…`. Pedra v47 `_medir_v398_custodia`: o cofre v398 contra o v397, PELO NOME; 4 blocos novos verificados "
   "sem efeito no gate, 40 bandeiras (as pedras Sonico e AfinacaoDasCordas), as duas composições incondicionais, nada deriva as cordas do axioma, "
   "registro %d com os %d da v397 e 5 vereditos mudados (a troca numérica da escada), kernel %d/%d; dois céticos reprovam. NENHUMA errata nesta "
   "custódia. PARA A v64: a pedra genérica (G1) lê o próprio cofre pelo nome." % (AGORA, vf[:90], F["registro"]["pt"], F["registro"]["v397"],
                                                                                 km["formal_files"], km["declaracoes_no_axiom_report"]))
ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v398\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "dispositivos-formula-completa.md"),
   "## %s — camada v398 (item 18)\n\nOs registros _v398 (sonico_v398, afinacao_das_cordas_v398, cunhagens_v398, kh_n1_cobertura_v398) lidos e conferidos "
   "no cofre, sem interpretação: composições incondicionais no trio; os registros conferem cálculos (8 e 7); a lei de custo é INPUT; MasslessFirstLevel é "
   "hipótese nomeada; a geometria é OPEN; nada deriva as cordas do axioma; a escada %s. %d/16 com a camada; 16 FINAL regerados e rodados, rc 0 em 16/16. "
   "Nada muda número de dispositivo." % (AGORA, F["escada"], n_disp))
HM = os.path.join(MEM, "handoff-v398-custodia.md")
if os.path.isfile(HM):
    ap(HM, "## %s — CUSTODIADO pela sessão a7 da Central\n\n%s" % (AGORA, ESTADO))
else:
    open(HM, "w", encoding="utf-8").write("---\nname: handoff-v398-custodia\ndescription: HANDOFF v398 (o sônico e a afinação das cordas) — custódia da sessão a7 da Central, 24/10/2026\nmetadata:\n  type: project\n---\n\n## %s — CUSTODIADO pela sessão a7 da Central\n\n%s\n" % (AGORA, ESTADO))
    print("criado handoff-v398-custodia.md")
ap(CEN + r"\memory\TGL_ATLAS.md", "[%s — §X append, re-ancorado ao selo v398 `%s`: A CUSTÓDIA DA v398] %s" % (AGORA, pin16, ESTADO))

M, M2 = os.path.join(MEM, "MEMORY.md"), os.path.join(MEM, "MEMORY_2.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v398 ")]
nova = ("- [HANDOFF v398 — o sônico e a afinação das cordas; custódia](handoff-v398-custodia.md) — **24/10: CUSTODIADO** (the_boundary `%s`, pós-push 19/19; "
        "site no ar; Central: cofre v398, runner v63, 16/16, FINAL, ledger 0) · `%s`" % (esp, pin16))
if old:
    assert len(old) == 1, old
    ap(M2, "## %s — linha movida do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (AGORA, old[0]))
    tocar(M, lambda t_, nl_: t_.replace(old[0], nova, 1), pode_encolher=True)
else:   # a c1 não deixou linha para a v398: entra ao lado da v397, no bloco «Estado corrente»
    anc = [l for l in t.split(nl) if l.startswith("- [HANDOFF v397 ")]
    assert len(anc) == 1, anc
    tocar(M, lambda t_, nl_: t_.replace(anc[0], nova + nl_ + anc[0], 1))
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)

rota = {"tipo": "ROTA", "rota_id": "custodia.v398", "dominio": "CUSTODIA",
        "titulo": "Custódia da v398 (o sônico e a afinação das cordas): espelho, frente, site, cofre v398, runner v63, 16 dispositivos, FINAL, ledger, snapshot — segunda custódia pela regra do gatilho",
        "pergunta": "A v398 (%s) pode ser custodiada pelos scripts da v397 deslocados por versão (derivar_*_v398.py), com cada artefato conferido por hash, os números lidos do core e sem errata nas pedras antigas — começando pelo gatilho das três marcas, sem ordem nova?" % pin16,
        "dados": ["Nós (um.py v398, selo, core, artigos, rodada_v398_stdout, HANDOFF_v398 com os dois parágrafos prontos)", "work/cadeia_de_selo/v398, v398_selo e v398_kernel",
                  "as fontes pinadas que os registros v392–v398 releem por caminho absoluto"],
        "metodo": "Vigia das três marcas (selo, bloco do diário, handoff) → scripts deslocados da v397 por trocas ordenadas e protegidas (derivar_central_v398.py) e por "
                  "trocas contadas (derivar_espelho_v398.py), com os números de fatos_v398.json (sondar_v398.py): passo zero, cópia ao espelho, geradores (ESTADO, LEDGER, "
                  "CITATION, arco; o parágrafo pronto conferido número a número contra os registros sonico/afinacao; o quadro v397 conferido intocado), dados do selo no site, "
                  "cofre, runner v63, camada v398, FINAL, ledger, snapshot.",
        "resultado": ESTADO.replace("PROVADA = validade; CONFIRMADA = creditação, recusada;", "PROVADA = validade; a creditação segue recusada;"),
        "veredito": "CUSTODIA_V398_PUBLICADA_PELA_REGRA_DO_GATILHO__SCRIPTS_DESLOCADOS_DA_V397__SEM_ERRATA_NAS_PEDRAS_ANTIGAS__GATE_INALTERADO",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "A derivação por deslocamento ainda é por versão (G1 em construção: tools/custodiar.py). O app segue em v395 (a release do app não está nesta cadeia; fase A preparada).",
        "nao_refazer": "A custódia v398 está publicada e conferida. A próxima usa custodiar.py (G1) ou deriva destes scripts (work/custodia_v398_24out) com fatos_vNNN.json.",
        "proximo_passo": "Na v399: custodiar.py; a pedra genérica do runner; a release do app na cadeia (fase B da v398 primeiro).",
        "onde": W,
        "artefatos": [V + r"\CUSTODY_MANIFEST.json", KV + r"\CUSTODY_MANIFEST.json", CEN + r"\fronteira_tgl\runner\one_fronteira.py",
                      CEN + r"\patents\_formula_completa\tgl_formula_completa.py", r"C:\IALD\Site\tgl\v3.0_bancada\revisoes\custodia_v398_espelho.json", W + r"\fatos_v398.json"],
        "refs": ["custodia.v397", "iald.organismo.torre_de_comando_23out"],
        "nota": "Sessão a7 da Central (Claude), 24/10/2026."}
for k, v in rota.items():
    if isinstance(v, str):
        assert "CONFIRM" not in v.upper(), k
rp = os.path.join(W, "rota_custodia_v398.json")
open(rp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", rp, "--quem", "claude-central-a7 (custódia v398)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("rota:", r.returncode, (r.stdout or r.stderr)[-160:])
print("REGISTRO OK:", esp, pin16, vf[:40], n_disp, os.path.basename(snap))

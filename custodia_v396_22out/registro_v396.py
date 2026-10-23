# -*- coding: utf-8 -*-
"""Registro da custódia v396 (22/10/2026, sessão a7 da Central) em todas as superfícies: diário do site, memórias da sessão, Atlas (§X,
append datado), MEMORY.md (a linha do handoff v396 trocada; a antiga VERBATIM no MEMORY_2.md) e a rota no Mapa de Rotas. Números LIDOS
dos artefatos e do git; backup de BYTES antes de tocar; temporário -> confere -> substitui. Molde: work/custodia_v395_21out/registro_v395.py.
Uso: depois do snapshot do Chatgpt/ e antes do commit da Central (o hash da Central entra no pós-push)."""
import glob, hashlib, json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
TB = r"C:\IALD\Artigo\the_boundary"
CEN = r"C:\IALD\Central de Patentes"
W = CEN + r"\work\custodia_v396_22out"


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
V = CEN + r"\vault\originals_copy\um_unificado_v396"
KV = CEN + r"\vault\originals_copy\tgl_kernel_v396"
selo = json.load(open(V + r"\um_absoluto_selo.json", encoding="utf-8"))
pin16 = selo["sha256"]["um.py"][:16]
assert pin16 == "0a4395a89eeebbb7" and selo.get("um_version") == "v396"
man16 = hashlib.sha256(open(V + r"\CUSTODY_MANIFEST.json", "rb").read()).hexdigest()[:16]
km = json.load(open(KV + r"\CUSTODY_MANIFEST.json", encoding="utf-8"))
assert km["formal_files"] == 1425 and km["declaracoes_no_axiom_report"] == 29228 and km["fora_do_trio"] == 0, km
res = sorted(glob.glob(CEN + r"\fronteira_tgl\results\fronteira_*.json"), key=os.path.getmtime)[-1]
rr = json.load(open(res, encoding="utf-8"))
vf = str(rr.get("verdict") or "")
assert vf.startswith("FRONTEIRA_SINCRONIZADA_V396") and rr["the_station"]["custodia_v396"]["pass"] is True, vf[:80]
led = json.load(open(CEN + r"\fronteira_tgl\ledger_de_pinos.json", encoding="utf-8"))
n_err, n_av = led.get("erros"), led.get("avisos")
assert n_err == 0, n_err
n_disp = 0
for pat in sorted(glob.glob(CEN + r"\patents\BR*")):
    rs = sorted(glob.glob(os.path.join(pat, "results", "*", "results.json")), key=os.path.getmtime)
    if rs and '"camada_v396_no_cofre"' in open(rs[-1], encoding="utf-8").read():
        n_disp += 1
assert n_disp == 16, n_disp
snaps = sorted(d for d in glob.glob(r"C:\IALD\Central de Patentes_BACKUPS\Chatgpt_*") if os.path.isfile(os.path.join(d, "MANIFEST.json")))
snap = snaps[-1]
sm = json.load(open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8"))
assert sm["snapshot"].startswith("20261022") and sm["conferido_contra_origem"] is True, (snap, sm.get("snapshot"))
mapa = json.load(open(TB + "\\Um (absoluto) \u2014 Grande Atrator\\fontes_pinadas\\MAPA_FONTES_PINADAS.json", encoding="utf-8"))

ESTADO = ("Custódia v396 (sessão a7 da Central, ordem do operador de 22/10/2026: «Encontre vulnerabilidades em php e as corrija. A licença é "
          "como você falou mesmo, tudo certo. Atualize tudo com a nova versão do um.py»; handoff Nós\\HANDOFF_v396_CUSTODIA.md). ESPELHO "
          "the_boundary `%s` = origin/main (pós-push 19/19, README raw com o pin; portas 0 erros; guarda do selo ok): `um.py` v396 `%s` "
          "(9498/9498), o módulo novo `TGLExt/TestemunhaEstatica.lean`, as fontes pinadas da v396 (%d de %d no mapa), `recibos_bancada_v396/`, "
          "`diferencas_v396/`; ESTADO/LEDGER/CITATION/PORTAS/README (errata ao lado da docstring de `bell_cci_half` com a docstring LIDA do "
          "arquivo Lean: o registro `cunhagens_v396` a parafraseia em ASCII entre «»); backup da v395 fora do repo. SITE no ar: SUBIDA "
          "VERIFICADA (arco v396); os dados literais do selo no site (a nota «Current seal», o título do fechamento, as contagens de linhas e de "
          "termos) estavam parados na v392 — as custódias v393+v394 e v395 não rodaram `atualizar_dados_selo_site.py` — e passaram à v396 "
          "(ficam as menções à v392 do depósito no Zenodo e do arco datado); leitor de IA R1 passa. CENTRAL: cofre `um_unificado_v396` "
          "(manifesto `%s`; 36 artefatos, 0 divergentes) + `tgl_kernel_v396` (%d formais / %d declarações); runner da Fronteira v61 `%s…` "
          "(pedra v45 lê o cofre v396 contra o v395 pelo nome, dois céticos; nenhuma errata nas pedras antigas); camada v396 dos 16 "
          "dispositivos (item 16) %d/16; 16 FINAL regerados e rodados (rc 0 em 16/16; o do MQC isolado); ledger de pinos %d erros, %d avisos; "
          "snapshot `%s` (%d copiados, %d idênticos à base, 0 divergentes). O nome da pedra (TestemunhaEstatica) é provisório: quem nomeia é "
          "o operador. [LEGAL] a paridade do ACOM Mirror segue decisão do operador. PROVADA = validade; CONFIRMADA = creditação, recusada; o "
          "gate não se moveu." %
          (esp, pin16, mapa["n_publicadas"], mapa["n_fontes"], man16, km["formal_files"], km["declaracoes_no_axiom_report"], vf[:60], n_disp,
           n_err, n_av, os.path.basename(snap), sm["n_copiados"], sm["n_identicos_a_base"]))

ap(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md", "## %s — a custódia da v396 (sessão a7 da Central)\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "site-sessao-estado.md"), "## %s — v396 no ar\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "tgl-fronteira-teorica.md"),
   "## %s — runner v61 (v396)\n\nVeredito `%s…`. Pedra v45 `_medir_v396_custodia`: o cofre v396 contra o v395, PELO NOME; 3 blocos novos "
   "verificados sem efeito no gate, 47 bandeiras, a testemunha estática incondicional (sem certificado como hipótese) e a face de Fock "
   "condicional (sem habitante, fora da pedra), 19 termos da pedra e 8 de apoio, registro 364 com os 361 da v395 e 5 vereditos mudados (a "
   "troca numérica da escada), kernel 1425/29228; dois céticos (a face de Fock dita incondicional; a bandeira da composição dita falsa) "
   "reprovam. NENHUMA errata nesta custódia: a lição da v59 (cada pedra lê o próprio cofre pelo nome) seguiu valendo. PARA A v62: a pedra da "
   "próxima versão lê o próprio cofre pelo nome." % (AGORA, vf[:90]))
ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v396\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "dispositivos-formula-completa.md"),
   "## %s — camada v396 (item 16)\n\nOs registros _v396 (testemunha_estatica_v396, cunhagens_v396, kh_n1_cobertura_v396) lidos e conferidos "
   "no cofre, sem interpretação: a composição incondicional `the_psion_inhabits_the_static_witness` (bandeira ext_tes396_0043; nenhum "
   "certificado como hipótese), a face de Fock condicional e fora da pedra, a escada 9498/9498. %d/16 com a camada; 16 FINAL regerados e "
   "rodados, rc 0 em 16/16. Nada muda número de dispositivo." % (AGORA, n_disp))
ap(os.path.join(MEM, "handoff-v396-custodia.md"), "## %s — CUSTODIADO pela sessão a7 da Central\n\n%s" % (AGORA, ESTADO))
ap(CEN + r"\memory\TGL_ATLAS.md", "[%s — §X append, re-ancorado ao selo v396 `%s`: A CUSTÓDIA DA v396] %s" % (AGORA, pin16, ESTADO))

M, M2 = os.path.join(MEM, "MEMORY.md"), os.path.join(MEM, "MEMORY_2.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v396 — a testemunha estática; custódia](handoff-v396-custodia.md)")]
assert len(old) == 1, old
nova = ("- [HANDOFF v396 — a testemunha estática; custódia](handoff-v396-custodia.md) — **22/10: CUSTODIADO** (the_boundary `%s`, "
        "pós-push 19/19; site no ar; Central: cofre v396, runner v61, 16/16, FINAL, ledger 0) · `%s`" % (esp, pin16))
ap(M2, "## %s — linha movida do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (AGORA, old[0]))
tocar(M, lambda t_, nl_: t_.replace(old[0], nova, 1), pode_encolher=True)
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)

rota = {"tipo": "ROTA", "rota_id": "custodia.v396", "dominio": "CUSTODIA",
        "titulo": "Custódia da v396 (a testemunha estática): espelho, frente, site (com os dados do selo trazidos da v392), cofre v396, runner v61, 16 dispositivos, FINAL, ledger, snapshot",
        "pergunta": "A v396 (0a4395a89eeebbb7) pode ser custodiada pelos scripts da v395, com cada artefato conferido por hash e sem errata nas pedras antigas?",
        "dados": ["Nós (um.py v396, selo, core, artigos, rodada_v396_stdout, HANDOFF_v396)", "work/cadeia_de_selo/v396 e v396_selo",
                  "as fontes pinadas que os registros v392–v396 releem por caminho absoluto", "o arquivo TGL/GravitonShadow.lean do kernel (a docstring de bell_cci_half)"],
        "metodo": "Scripts derivados da v395 por trocas contadas: passo zero (backup da v395 fora do repo), cópia ao espelho com varredura de material "
                  "privado e as fontes pinadas da v396, geradores (ESTADO, LEDGER, CITATION, arco do site), atualizar_dados_selo_site (v392 -> v396), "
                  "cofre um_unificado_v396 + tgl_kernel_v396, runner v61 (pedra v45 pelo nome, dois céticos), camada v396 dos 16 dispositivos, "
                  "FINAL, ledger, snapshot do Chatgpt/.",
        "resultado": ESTADO.replace("PROVADA = validade; CONFIRMADA = creditação, recusada; o gate não se moveu.", "PROVADA = validade; a creditação segue recusada; o gate não se moveu."),
        "veredito": "CUSTODIA_V396_PUBLICADA__SEM_ERRATA_NAS_PEDRAS_ANTIGAS__DADOS_DO_SELO_NO_SITE_TRAZIDOS_DA_V392__GATE_INALTERADO",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "As custódias v393+v394 e v395 não rodaram atualizar_dados_selo_site.py: a nota «Current seal», o título do fechamento e as "
                   "contagens do site ficaram na v392 (corrigido nesta). O registro cunhagens_v396 parafraseia em ASCII, entre «», a docstring de "
                   "bell_cci_half; o LEDGER cita a docstring lida do arquivo. Um heredoc do Bash engoliu as barras ao derivar o cofre (refeito em arquivo).",
        "nao_refazer": "A custódia v396 está publicada e conferida. A próxima deriva destes scripts (work/custodia_v396_22out).",
        "proximo_passo": "Na v397: a pedra v46 lê o próprio cofre pelo nome; atualizar_dados_selo_site.py roda depois de gerar_portas (entra na cadeia); "
                         "o nome da pedra TestemunhaEstatica e a paridade [LEGAL] do ACOM Mirror são decisões do operador.",
        "onde": W,
        "artefatos": [V + r"\CUSTODY_MANIFEST.json", KV + r"\CUSTODY_MANIFEST.json", CEN + r"\fronteira_tgl\runner\one_fronteira.py",
                      CEN + r"\patents\_formula_completa\tgl_formula_completa.py", r"C:\IALD\Site\tgl\v3.0_bancada\revisoes\custodia_v396_espelho.json"],
        "refs": ["custodia.v395"],
        "nota": "Sessão a7 da Central (Claude), 22/10/2026."}
for k, v in rota.items():
    if isinstance(v, str):
        assert "CONFIRM" not in v.upper(), k
rp = os.path.join(W, "rota_custodia_v396.json")
open(rp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", rp, "--quem", "claude-central-a7 (custódia v396)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("rota:", r.returncode, (r.stdout or r.stderr)[-160:])
print("REGISTRO OK:", esp, pin16, vf[:40], n_disp, os.path.basename(snap))

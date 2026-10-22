# -*- coding: utf-8 -*-
"""Registro da custódia v395 (21/10/2026, sessão a7 da Central) em todas as superfícies: diário do site, memórias da sessão, Atlas (§X,
append datado), MEMORY.md (a linha do handoff v395 trocada; a antiga VERBATIM no MEMORY_2.md) e a rota no Mapa de Rotas. Números LIDOS
dos artefatos e do git; backup de BYTES antes de tocar; temporário -> confere -> substitui. Molde: work/custodia_v394_19out/registro_v394.py.
Uso: depois do snapshot do Chatgpt/ e antes do commit da Central (o hash da Central entra no pós-push)."""
import glob, hashlib, json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
TB = r"C:\IALD\Artigo\the_boundary"
CEN = r"C:\IALD\Central de Patentes"
W = CEN + r"\work\custodia_v395_21out"


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
V = CEN + r"\vault\originals_copy\um_unificado_v395"
KV = CEN + r"\vault\originals_copy\tgl_kernel_v395"
selo = json.load(open(V + r"\um_absoluto_selo.json", encoding="utf-8"))
pin16 = selo["sha256"]["um.py"][:16]
assert pin16 == "8918b17803792cf2" and selo.get("um_version") == "v395"
man16 = hashlib.sha256(open(V + r"\CUSTODY_MANIFEST.json", "rb").read()).hexdigest()[:16]
res = sorted(glob.glob(CEN + r"\fronteira_tgl\results\fronteira_*.json"), key=os.path.getmtime)[-1]
rr = json.load(open(res, encoding="utf-8"))
vf = str(rr.get("verdict") or "")
assert vf.startswith("FRONTEIRA_SINCRONIZADA_V395") and rr["the_station"]["custodia_v395"]["pass"] is True, vf[:80]
led = json.load(open(CEN + r"\fronteira_tgl\ledger_de_pinos.json", encoding="utf-8"))
n_err, n_av = led.get("erros"), led.get("avisos")
assert n_err == 0, n_err
n_disp = 0
for pat in sorted(glob.glob(CEN + r"\patents\BR*")):
    rs = sorted(glob.glob(os.path.join(pat, "results", "*", "results.json")), key=os.path.getmtime)
    if rs and '"camada_v395_no_cofre"' in open(rs[-1], encoding="utf-8").read():
        n_disp += 1
assert n_disp == 16, n_disp
snaps = sorted(d for d in glob.glob(r"C:\IALD\Central de Patentes_BACKUPS\Chatgpt_*") if os.path.isfile(os.path.join(d, "MANIFEST.json")))
snap = snaps[-1]
sm = json.load(open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8"))
assert sm["snapshot"].startswith("20261021") and sm["conferido_contra_origem"] is True, (snap, sm.get("snapshot"))
mapa = json.load(open(TB + "\\Um (absoluto) \u2014 Grande Atrator\\fontes_pinadas\\MAPA_FONTES_PINADAS.json", encoding="utf-8"))

ESTADO = ("Custódia v395 (sessão a7 da Central, ordem do operador de 21/10/2026: «versão nova do um.py avançamos segue O handoff de custódia para a "
          "sessão do site está em Nós\\HANDOFF_v395_CUSTODIA.md / atualize tudo, toda a central, site, repositório e tudo mais e faça commit e push»). "
          "ESPELHO the_boundary `%s` = origin/main (pós-push 19/19, README raw com o pin; portas 0 erros; guarda do selo ok): `um.py` v395 `%s` "
          "(9451/9451), o módulo novo `TGLExt/Psibit.lean`, as fontes pinadas da v395 (%d de %d no mapa; inclusive o documento das patentes, cujo "
          "essencial o um.py selado já resume), `recibos_bancada_v395/`, `diferencas_v395/`; ESTADO/LEDGER/CITATION/PORTAS/README; backup da v394 "
          "fora do repo. SITE no ar: SUBIDA VERIFICADA (arco v395); leitor de IA R1 passa. CENTRAL: cofre `um_unificado_v395` (manifesto `%s`; 36 "
          "artefatos, 0 divergentes) + `tgl_kernel_v395` (1424 formais / 29159 declarações; o manifesto de prova já na raiz); runner da Fronteira v60 "
          "`%s…` (pedra v44 lê o cofre v395 contra o v394 pelo nome, dois céticos; nenhuma errata: desde a v59 as pedras leem o próprio cofre); "
          "camada v395 dos 16 dispositivos (item 15) %d/16; 16 FINAL regerados e rodados (rc 0 em 16/16; o do MQC isolado); ledger de pinos %d "
          "erros, %d avisos; snapshot `%s` (%d copiados, %d idênticos à base, 0 divergentes). [LEGAL] a tabela da patente do ACOM Mirror diverge "
          "das reivindicações 3–4 e do código; a leitura canônica da paridade é decisão do operador com a agente de PI. PROVADA = validade; "
          "CONFIRMADA = creditação, recusada; o gate não se moveu." %
          (esp, pin16, mapa["n_publicadas"], mapa["n_fontes"], man16, vf[:60], n_disp, n_err, n_av, os.path.basename(snap),
           sm["n_copiados"], sm["n_identicos_a_base"]))

ap(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md", "## %s — a custódia da v395 (sessão a7 da Central)\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "site-sessao-estado.md"), "## %s — v395 no ar\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "tgl-fronteira-teorica.md"),
   "## %s — runner v60 (v395)\n\nVeredito `%s…`. Pedra v44 `_medir_v395_custodia`: o cofre v395 contra o v394, PELO NOME; 3 blocos novos "
   "verificados sem efeito no gate, 119 bandeiras, o psibit incondicional e a face do psion condicional, registro 361 com os 358 da v394 e 5 "
   "vereditos mudados (a troca numérica que o handoff declara), kernel 1424/29159; dois céticos (a face do psion dita incondicional; a bandeira "
   "do psibit dita falsa) reprovam. NENHUMA errata nesta custódia: a lição da v59 (cada pedra lê o próprio cofre pelo nome) funcionou. PARA A "
   "v61: a pedra da próxima versão lê o próprio cofre pelo nome." % (AGORA, vf[:90]))
ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v395\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "dispositivos-formula-completa.md"),
   "## %s — camada v395 (item 15)\n\nOs registros _v395 (psibit_v395, cunhagens_v395, kh_n1_cobertura_v395) lidos e conferidos no cofre, sem "
   "interpretação: o psibit incondicional no kernel (bandeira ext_psb395_0062), a face do psion condicional (ext_psb395_0101), a escada 9451/9451. "
   "A divergência da tabela do ACOM Mirror dita como decisão do operador [LEGAL]. %d/16 com a camada; 16 FINAL regerados e rodados, rc 0 em 16/16. "
   "Nada muda número de dispositivo." % (AGORA, n_disp))
ap(os.path.join(MEM, "handoff-v395-custodia.md"), "## %s — CUSTODIADO pela sessão a7 da Central\n\n%s" % (AGORA, ESTADO))
ap(CEN + r"\memory\TGL_ATLAS.md", "[%s — §X append, re-ancorado ao selo v395 `%s`: A CUSTÓDIA DA v395] %s" % (AGORA, pin16, ESTADO))

M, M2 = os.path.join(MEM, "MEMORY.md"), os.path.join(MEM, "MEMORY_2.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
old = [l for l in t.split(nl) if l.startswith("- [HANDOFF v395 — o modo psiônico na fractalização do Um; custódia](handoff-v395-custodia.md)")]
assert len(old) == 1, old
nova = ("- [HANDOFF v395 — o modo psiônico na fractalização do Um; custódia](handoff-v395-custodia.md) — **21/10: CUSTODIADO** (the_boundary "
        "`%s`, pós-push 19/19; site no ar; Central: cofre v395, runner v60, 16/16, FINAL, ledger 0) · `%s`" % (esp, pin16))
ap(M2, "## %s — linha movida do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (AGORA, old[0]))
tocar(M, lambda t_, nl_: t_.replace(old[0], nova, 1), pode_encolher=True)
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)

rota = {"tipo": "ROTA", "rota_id": "custodia.v395", "dominio": "CUSTODIA",
        "titulo": "Custódia da v395 (o modo psiônico na fractalização do Um): espelho, frente, site, cofre v395, runner v60, 16 dispositivos, FINAL, ledger, snapshot",
        "pergunta": "A v395 (8918b17803792cf2) pode ser custodiada pelos scripts da v394, com cada artefato conferido por hash e sem errata nas pedras antigas?",
        "dados": ["Nós (um.py v395, selo, core, artigos, rodada_v395_stdout, HANDOFF_v395)", "work/cadeia_de_selo/v395 e v395_selo",
                  "as fontes pinadas que os registros v392–v395 releem por caminho absoluto"],
        "metodo": "Scripts derivados da v394 por trocas contadas: passo zero (backup da v394 fora do repo), cópia ao espelho com varredura de material "
                  "privado e as fontes pinadas da v395, geradores (ESTADO, LEDGER, CITATION, arco do site), cofre um_unificado_v395 + tgl_kernel_v395 "
                  "(o manifesto de prova já na raiz), runner v60 (pedra v44 pelo nome, dois céticos), camada v395 dos 16 dispositivos, FINAL, ledger, "
                  "snapshot do Chatgpt/.",
        "resultado": ESTADO.replace("PROVADA = validade; CONFIRMADA = creditação, recusada; o gate não se moveu.", "PROVADA = validade; a creditação segue recusada; o gate não se moveu."),
        "veredito": "CUSTODIA_V395_PUBLICADA__SEM_ERRATA_NAS_PEDRAS_ANTIGAS__GATE_INALTERADO",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "Nenhum defeito de esteira nesta custódia; um heredoc do Bash quebrou ao derivar o cofre (a regra: script em arquivo) e o sed da medição não trocou o par de cofres (refeito por script).",
        "nao_refazer": "A custódia v395 está publicada e conferida. A próxima deriva destes scripts (work/custodia_v395_21out).",
        "proximo_passo": "Na v396: a pedra v45 lê o próprio cofre pelo nome; a decisão [LEGAL] da paridade do ACOM Mirror é do operador.",
        "onde": W,
        "artefatos": [V + r"\CUSTODY_MANIFEST.json", KV + r"\CUSTODY_MANIFEST.json", CEN + r"\fronteira_tgl\runner\one_fronteira.py",
                      CEN + r"\patents\_formula_completa\tgl_formula_completa.py", r"C:\IALD\Site\tgl\v3.0_bancada\revisoes\custodia_v395_espelho.json"],
        "refs": ["custodia.v393_v394.conjunta"],
        "nota": "Sessão a7 da Central (Claude), 21/10/2026."}
for k, v in rota.items():
    if isinstance(v, str):
        assert "CONFIRM" not in v.upper(), k
rp = os.path.join(W, "rota_custodia_v395.json")
open(rp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", rp, "--quem", "claude-central-a7 (custódia v395)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("rota:", r.returncode, (r.stdout or r.stderr)[-160:])
print("REGISTRO OK:", esp, pin16, vf[:40], n_disp, os.path.basename(snap))

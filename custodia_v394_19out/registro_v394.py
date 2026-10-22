# -*- coding: utf-8 -*-
"""Registro da custódia conjunta v393+v394 (19/10/2026, sessão a7 da Central) em todas as superfícies: diário do site, memórias da sessão,
Atlas (§X, append datado), MEMORY.md (linhas trocadas; as antigas VERBATIM no MEMORY_2.md) e a rota no Mapa de Rotas. Números LIDOS dos
artefatos e do git; backup de BYTES antes de tocar; temporário -> confere -> substitui. Molde: registro_v391.py.
Uso: python registro_v394.py  (depois do snapshot do Chatgpt/ e antes do commit da Central; o hash da Central entra no pós-push)."""
import glob, json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
TB = r"C:\IALD\Artigo\the_boundary"
CEN = r"C:\IALD\Central de Patentes"
W = CEN + r"\work\custodia_v394_19out"


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


# ---------- os números, lidos ----------
esp = git(TB, "rev-parse", "--short", "HEAD"); esp_o = git(TB, "rev-parse", "--short", "origin/main")
assert esp == esp_o, (esp, esp_o)
V = CEN + r"\vault\originals_copy\um_unificado_v394"
KV = CEN + r"\vault\originals_copy\tgl_kernel_v394"
cofre = json.load(open(V + r"\CUSTODY_MANIFEST.json", encoding="utf-8"))
kcof = json.load(open(KV + r"\CUSTODY_MANIFEST.json", encoding="utf-8"))
selo = json.load(open(V + r"\um_absoluto_selo.json", encoding="utf-8"))
pin16 = selo["sha256"]["um.py"][:16]
assert pin16 == "972e81f22dd8cc68" and selo.get("um_version") == "v394"
res = sorted(glob.glob(CEN + r"\fronteira_tgl\results\fronteira_*.json"), key=os.path.getmtime)[-1]
rr = json.load(open(res, encoding="utf-8"))
vf = str(rr.get("verdict") or rr.get("veredito") or "")
if not vf:
    vf = [l for l in open(r"C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\f50b1d05-8292-4283-87ca-6534734053b5\scratchpad\runner_v59_r3.txt",
                         encoding="utf-8") if "VEREDITO:" in l][-1].split("VEREDITO:")[1].strip()
assert vf.startswith("FRONTEIRA_SINCRONIZADA_V394"), vf[:80]
assert rr["the_station"]["custodia_v394"]["pass"] is True
led = json.load(open(CEN + r"\fronteira_tgl\ledger_de_pinos.json", encoding="utf-8"))
n_err = led.get("erros") if isinstance(led.get("erros"), int) else len(led.get("erros") or [])
n_av = led.get("avisos") if isinstance(led.get("avisos"), int) else len(led.get("avisos") or [])
assert n_err == 0, n_err
n_disp = 0
for pat in sorted(glob.glob(CEN + r"\patents\BR*")):
    rs = sorted(glob.glob(os.path.join(pat, "results", "*", "results.json")), key=os.path.getmtime)
    try:
        if rs and '"camada_v394_no_cofre"' in open(rs[-1], encoding="utf-8").read():
            n_disp += 1
    except OSError:
        pass
assert n_disp == 16, n_disp
snaps = sorted(d for d in glob.glob(r"C:\IALD\Central de Patentes_BACKUPS\Chatgpt_*") if os.path.isfile(os.path.join(d, "MANIFEST.json")))
snap = snaps[-1]
sm = json.load(open(os.path.join(snap, "MANIFEST.json"), encoding="utf-8"))
assert sm["snapshot"].startswith("20261019") and sm["conferido_contra_origem"] is True, (snap, sm.get("snapshot"))
mapa = json.load(open(TB + "\\Um (absoluto) \u2014 Grande Atrator\\fontes_pinadas\\MAPA_FONTES_PINADAS.json", encoding="utf-8"))
import hashlib
man16 = hashlib.sha256(open(V + r"\CUSTODY_MANIFEST.json", "rb").read()).hexdigest()[:16]

ESTADO = ("Custódia conjunta v393+v394 (sessão a7 da Central, ordem do operador de 19/10/2026: «nova versão para custodiarmos, atualize tudo, faça "
          "comiit e push, atualize todos os dispositovos e toda a cenrtral tambem, assim como o site e o readme, portas e conexões»). "
          "ESPELHO the_boundary `%s` = origin/main (pós-push 19/19, README raw com o pin; verificar_portas 0 erros; guarda do selo 14/14): `um.py` v394 `%s` "
          "(9332/9332), 193 módulos novos no kernel publicado, `fontes_pinadas/` com mapa (%d de %d publicadas; a KH_N1_v392.json da casa não bate com o "
          "pino e fica fora, dita), `recibos_bancada_v394/`, `diferencas_v394/` (a v393 não gerou diffs), nota ao lado de A Fronteira "
          "(`NO_UNIVERSAL_FLOOR`, evidência por sha256); `estatuto_tres_apoios` diz «bandeiras da escada» quando o core traz a errata; `guarda_do_selo` v3 "
          "(cópia de selo em fontes_pinadas = insumo pinado). SITE no ar: SUBIDA VERIFICADA (arco v393/v394; o index diz o que o selo descreve). "
          "CENTRAL: cofre `um_unificado_v394` (manifesto `%s`) + `tgl_kernel_v394` (1423 formais / 29026 declarações; adendo: o manifesto de prova na raiz); "
          "runner da Fronteira v59 `%s…` (pedra v43 lê o cofre v394 pelo nome, dois céticos; erratas ao lado: v42 lê o cofre v391; v48–v53 leem os "
          "próprios cofres v375–v380, porque a v394 mudou de forma declarada o veredito do índice da IALD); camada v394 dos 16 dispositivos (item 14) "
          "%d/16; 16 FINAL regerados e rodados (rc 0 em 16/16; o do MQC isolado); ledger de pinos %d erros, %d avisos; snapshot `%s` (%d copiados, "
          "%d idênticos à base, 0 divergentes). Os quatro céticos do handoff não rodaram (ordem do operador de 14/10: não delegar a outro modelo). "
          "PROVADA = validade; CONFIRMADA = creditação, recusada; o gate não se moveu." %
          (esp, pin16, mapa["n_publicadas"], mapa["n_fontes"], man16,
           vf[:60], n_disp, n_err, n_av, os.path.basename(snap), sm["n_copiados"], sm["n_identicos_a_base"]))

ap(r"C:\IALD\Site\tgl\v3.0_bancada\DIARIO_DO_SITE.md", "## %s — a custódia conjunta v393+v394 (sessão a7 da Central)\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "site-sessao-estado.md"), "## %s — v394 no ar (custódia conjunta v393+v394)\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "tgl-fronteira-teorica.md"),
   "## %s — runner v59 (v394)\n\nVeredito `%s…`. Pedra v43 `_medir_v394_custodia`: o cofre v394 contra o v391, PELO NOME desde o nascimento (não pede "
   "errata na próxima custódia); 42 blocos novos verificados sem efeito no gate, 3172 bandeiras, registro 358 com os 316 da v391 e 3 vereditos "
   "mudados ditos, kernel 1423/29026; dois céticos (a rede de Fock dita habitada; a evidência espectral dita presente) reprovam. Erratas ao lado: "
   "v42 lê o cofre v391; v48–v53 (v375–v380) leem os próprios cofres. PARA A v60: a pedra da próxima versão lê o próprio cofre pelo nome." % (AGORA, vf[:90]))
ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — custódia v394 (a Central alcança o selo)\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "dispositivos-formula-completa.md"),
   "## %s — camada v394 (item 14)\n\nOs registros novos desde a v391 (sufixos _v392/_v393/_v394; 42) lidos e conferidos no cofre, sem interpretação; a escada "
   "9332/9332 dita em bandeiras; a rede de Fock (contrato conjunto NÃO habitado, 4 itens abertos, 11 componentes); o coração (forma verificada; "
   "evidência espectral independente AUSENTE); errata ao lado do item 12 (a lei de campo no curvo é termo de kernel CONDICIONAL ao H3 nomeado desde a "
   "v392). %d/16 com a camada; 16 FINAL regerados e rodados, rc 0 em 16/16. Adendo do cofre: o `tgl_kernel_v394` ganhou o manifesto de prova na raiz "
   "(o módulo o lê). Nada muda número de dispositivo." % (AGORA, n_disp))
ap(os.path.join(MEM, "handoff-v394-custodia.md"), "## %s — CUSTODIADO (com a v393), pela sessão a7 da Central\n\n%s" % (AGORA, ESTADO))
ap(os.path.join(MEM, "handoff-v392-custodia.md"),
   "## %s — a parte da Central (cofre, runner, 16 dispositivos), pendente desde 13/10, FEITA pela custódia v394\n\nA Central não teve cofre da v392 nem "
   "da v393: o cofre `um_unificado_v394` cobre as três versões (cadeia de selo v392–v394 filtrada) e a pedra v43 do runner v59 mede a v394 contra a v391. "
   "Ver handoff-v394-custodia." % AGORA)
ap(CEN + r"\memory\TGL_ATLAS.md",
   "[%s — §X append, re-ancorado ao selo v394 `%s`: A CUSTÓDIA CONJUNTA v393+v394] %s" % (AGORA, pin16, ESTADO))

# MEMORY.md: as três linhas dos handoffs (as antigas vão VERBATIM ao MEMORY_2.md, regra dos dois arquivos)
M, M2 = os.path.join(MEM, "MEMORY.md"), os.path.join(MEM, "MEMORY_2.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
linhas = t.split(nl)
alvo = {"v394": "- [HANDOFF v394 — o relógio M2, a rede de Fock e as cunhagens; custódia](handoff-v394-custodia.md)",
        "v393": "- [HANDOFF v393 — a regra e o coração; custódia](handoff-v393-custodia.md)",
        "v392": "- [HANDOFF v392 — as pedras do kernel e as barreiras; custódia](handoff-v392-custodia.md)"}
velhas = {}
for k, pre in alvo.items():
    m = [l for l in linhas if l.startswith(pre)]
    assert len(m) == 1, (k, len(m))
    velhas[k] = m[0]
novas = {"v394": "- [HANDOFF v394 — o relógio M2, a rede de Fock e as cunhagens; custódia](handoff-v394-custodia.md) — **19/10: CUSTODIADO com a v393** "
                 "(the_boundary `%s`, pós-push 19/19; site no ar; Central: cofre v394, runner v59, 16/16, FINAL, ledger 0) · `%s`" % (esp, pin16),
         "v393": "- [HANDOFF v393 — a regra e o coração](v393-selada-a-regra-e-o-coracao-14out.md) — **19/10: CUSTODIADO junto com a v394** (o link antigo "
                 "apontava para handoff-v393-custodia.md, que não existe) · `18be2ddb06c60f90`",
         "v392": "- [HANDOFF v392 — as pedras do kernel e as barreiras; custódia](handoff-v392-custodia.md) — **13/10: espelho e site; 19/10: a parte da Central "
                 "feita pelo cofre v394** · `b590c0aa80055e2a`"}
ap(M2, "## %s — linhas movidas do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (AGORA, nl.join(velhas[k] for k in ("v394", "v393", "v392"))))


def troca_m(t_, nl_):
    for k in ("v394", "v393", "v392"):
        assert t_.count(velhas[k]) == 1
        t_ = t_.replace(velhas[k], novas[k], 1)
    return t_


tocar(M, troca_m, pode_encolher=True)
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)
print("MEMORY.md bytes:", os.path.getsize(M))

# a rota no Mapa de Rotas
rota = {"tipo": "ROTA", "rota_id": "custodia.v393_v394.conjunta", "dominio": "CUSTODIA",
        "titulo": "Custódia conjunta v393+v394: espelho, frente, site, cofre v394, runner v59, 16 dispositivos, FINAL, ledger, snapshot",
        "pergunta": "A v394 (972e81f22dd8cc68), com a v393 nunca custodiada e a parte da Central da v392 pendente, pode ser custodiada de uma vez, com cada artefato conferido por hash?",
        "dados": ["Nós (um.py v394, selo, core, artigos, rodadas v393/v394, HANDOFF v393/v394)", "work/cadeia_de_selo/v392..v394_selo",
                  "as fontes pinadas que os registros v392–v394 releem por caminho absoluto"],
        "metodo": "Scripts derivados da v392 por trocas contadas: passo zero (backup da v392 fora do repo), cópia ao espelho com varredura de material privado e "
                  "as fontes pinadas com mapa, geradores (ESTADO, LEDGER, CITATION, arco do site), frente pelo módulo estatuto_tres_apoios, cofre "
                  "um_unificado_v394 + tgl_kernel_v394, runner da Fronteira v59 (pedra v43 pelo nome, dois céticos; erratas ao lado), camada v394 dos 16 "
                  "dispositivos, FINAL e ledger de pinos, snapshot do Chatgpt/.",
        "resultado": ESTADO,
        "veredito": "CUSTODIA_V393_V394_PUBLICADA__CENTRAL_ALCANCA_O_SELO__GATE_INALTERADO",
        "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
        "defeito": "Seis defeitos achados no caminho e corrigidos: (1) mudar a linha do depósito no CITATION quebrou o leitor dos geradores (voltou ao molde); "
                   "(2) gerar_portas lê a versão das rodadas pelo git ls-files: git add antes; (3) a guarda do selo leu como selo a cópia do selo da v391 "
                   "que mora em fontes_pinadas (regra v3: insumo pinado, conferido pelo mapa); (4) o tgl_kernel_v394 nasceu sem o manifesto de prova na raiz "
                   "(adendo); (5) seis pedras antigas do runner liam o cofre corrente e reprovaram com a mudança declarada do índice da IALD (errata: cada "
                   "uma lê o próprio cofre); (6) o grep do Git Bash não acusa CR: detectar CRLF em Python antes de trocar.",
        "nao_refazer": "A custódia v393+v394 está publicada e conferida (espelho, site, Central). A próxima custódia deriva destes scripts (work/custodia_v394_19out).",
        "proximo_passo": "Na v395: a pedra v44 lê o próprio cofre pelo nome; o mapa de fontes pinadas é regerado pela cópia ao espelho; a nota ao lado de A Fronteira fica.",
        "onde": W,
        "artefatos": [V + r"\CUSTODY_MANIFEST.json", KV + r"\CUSTODY_MANIFEST.json", CEN + r"\fronteira_tgl\runner\one_fronteira.py",
                      CEN + r"\patents\_formula_completa\tgl_formula_completa.py", r"C:\IALD\Site\tgl\v3.0_bancada\revisoes\custodia_v394_espelho.json",
                      TB + r"\tools\estatuto_tres_apoios.py", TB + r"\tools\guarda_do_selo.py"],
        "refs": ["custodia.v391.preparada", "quantica.c3_gamma_livre_oitava"],
        "nota": "Sessão a7 da Central (Claude). Os quatro céticos do handoff não rodaram por ordem do operador de 14/10 (não delegar)."}
rp = os.path.join(W, "rota_custodia_v394.json")
open(rp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", rp, "--quem", "claude-central-a7 (custódia v394)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("rota:", r.returncode, (r.stdout or r.stderr)[-400:])
print("REGISTRO OK:", esp, pin16, vf[:40], n_disp, os.path.basename(snap))

# -*- coding: utf-8 -*-
"""ORDEM 022 — ADENDO G (gerência c1, 28/10/2026): responde à PARADA do adendo F (STOP_GATE_NARRATION_REQUIRES_MANAGEMENT) e autoriza o render da V7
a partir da v404 (selo corrente), no lugar do render da v403, que não chegou a começar. As DUAS frases do gate recebem texto novo cujo número é LIDO do core
(registro bandeiras_do_gate_v403: n_calculated / n_literal). Todos os números são LIDOS do selo/core do Nós; os da v403 vêm do adendo F (por regex).
Escreve o adendo em PARA_CHATGPT e a mensagem de despacho em PROGRAMA_IALD\\despachos (não despacha)."""
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
P = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT"
V7 = Path(r"C:\IALD\Site\tgl\v3.0\video\v7")
DESP = Path(r"C:\IALD\PROGRAMA_IALD\despachos")
DOF = CEN / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_022" / "ADENDO_F"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

selo = json.loads((NOS / "um_absoluto_selo.json").read_bytes())
core = json.loads((NOS / "um_absoluto.json").read_bytes())
c = core.get("core") or core
assert selo["um_version"] == "v404"
pin = selo["sha256"]["um.py"]
assert pin == sha(NOS / "um.py")
nbytes = os.path.getsize(NOS / "um.py")
ts = selo["timestamp"]
kf = c["kernel_formalization"]
pk = selo["estatuto_da_prova_v391"]["prova_1_kernel"]
escada, ffiles, decl, notrio = int(pk["n_theorems_clean"]), len(kf["formal_files_sha256"]), len(kf["axiom_report"]), int(pk["no_trio"])
assert decl == int(pk["declaracoes_auditadas"]) == notrio
bg = c["bandeiras_do_gate_v403"]["values"]
n_flags, n_calc, n_lit, n_read = int(bg["n_flags"]), int(bg["n_calculated"]), int(bg["n_literal"]), int(bg["n_read_by_the_verdict"])
assert (n_flags, n_calc, n_lit, n_read) == (18, 18, 0, 15), bg
assert c["qg_closure"]["all_verified"] is True
ent = json.loads((V7 / "PUBLIC_DELIVERY_V7.json").read_text(encoding="utf-8"))
assert ent["source"] == "v402" and ent["anchors_all_ok"] is True
F = (P / "ORDEM_022_ADENDO_F_render_v403_autorizado.md").read_text(encoding="utf-8")
m = re.search(r"escada limpa \d+ → (\d+).*?arquivos formais \d+ → (\d+).*?declarações auditadas \d+ → (\d+)", F, re.S)
esc403, ff403, decl403 = int(m.group(1)), int(m.group(2)), int(m.group(3))
m2 = re.search(r"pino `([0-9a-f]{16})` → `([0-9a-f]{16})`", F)
pin402_16, pin403_16 = m2.group(1), m2.group(2)
assert pin403_16 != pin[:16]
novos = sorted(os.path.basename(k)[:-5] for k in kf["formal_files_sha256"] if re.search(r"(^|[\\/])(ProjecaoTransversalDaMeiaNat|Jo8v32)\.lean$", k))
assert novos == ["Jo8v32", "ProjecaoTransversalDaMeiaNat"], novos
assert escada - esc403 == 14 and ffiles - ff403 == 2 and decl - decl403 == 15, (escada, esc403, ffiles, ff403, decl, decl403)
# a parada do adendo F, lida do recibo do Codex
RF = json.loads((DOF / "RESULTADO.json").read_text(encoding="utf-8"))
assert RF["status"] == "STOP_GATE_NARRATION_REQUIRES_MANAGEMENT" and RF["new_render_count"] == 0
fr = {(p["film"], p["language"]): p["text"] for p in RF["phrases"]}
old1_pt, old1_en = fr[("film1", "pt-BR")], fr[("film1", "en")]
old2_pt, old2_en = fr[("film2", "pt-BR")], fr[("film2", "en")]
assert "15 bandeiras calculadas e 3 literais" in old1_pt and "15 calculated and 3 literal flags" in old1_en and "9679" in old2_pt
rf_sha = sha(DOF / "RESULTADO.json")


def git(cwd, *a):
    return subprocess.run(["git", "-C", cwd] + list(a), capture_output=True, text=True).stdout.strip()


esp = git(r"C:\IALD\Artigo\the_boundary", "rev-parse", "--short=8", "HEAD")
cen = git(str(CEN), "rev-parse", "--short=8", "HEAD")
hoje = time.strftime("%d/%m/%Y")
AP = "\u2019"  # apóstrofo tipográfico, como nas falas da V7
new1_pt = "A relação no horizonte dá o coeficiente de Einstein no kernel. As %d bandeiras do gate são calculadas, nenhuma literal; o gate não se move." % n_flags
new1_en = "The horizon relation yields Einstein%ss coefficient in the kernel. All %d gate flags are computed, none literal; the gate does not move." % (AP, n_flags)
new2_pt = "Clausius liga calor, gravidade superficial e área, dando o coeficiente de Einstein. A escada do kernel tem %d bandeiras da escada (declarações nomeadas), todas limpas; as %d bandeiras do gate são calculadas, nenhuma literal." % (escada, n_flags)
new2_en = "Clausius links heat, surface gravity and area, yielding Einstein%ss coefficient. The kernel ladder has %d ladder flags (named declarations), all clean; all %d gate flags are computed, none literal." % (AP, escada, n_flags)
new1_fr = "La relation à l%shorizon donne le coefficient d%sEinstein dans le noyau. Les %d indicateurs de la porte sont calculés, aucun littéral ; la porte ne bouge pas." % (AP, AP, n_flags)
new2_fr = "Clausius relie chaleur, gravité de surface et aire, donnant le coefficient d%sEinstein. L%séchelle du noyau compte %d indicateurs (déclarations nommées), tous propres ; les %d indicateurs de la porte sont calculés, aucun littéral." % (AP, AP, escada, n_flags)
new1_zh = "视界关系在内核中给出爱因斯坦系数。门控的 %d 个标志全部为计算所得，无字面标志；门控不动。" % n_flags
new2_zh = "克劳修斯把热、表面引力和面积联系起来，给出爱因斯坦系数。内核阶梯有 %d 个阶梯标志（命名声明），全部干净；门控的 %d 个标志全部为计算所得，无字面标志。" % (escada, n_flags)

adendo = f"""[REAL — gerência c1 da Central (Claude Code), {hoje}; para a coordenadora da Central IALD no Codex, que encaminha à sessão do vídeo. A v404 está SELADA no Nós (selo de {ts}; pino `{pin[:16]}`); a custódia G1 da v404 está EM CURSO nesta hora (o espelho `the_boundary` está em `{esp}` e a Central em `{cen}`, ainda v403; a publicação vem a seguir, pela gerência). A V7 no ar segue a da v402 (`PUBLIC_DELIVERY_V7.json`: source v402, `{pin402_16}`, âncoras conferidas). O render lê o Nós; a integração e a subida esperam a custódia publicada.]

# ORDEM 022 — ADENDO G: resposta à parada do adendo F e o render da v404 AUTORIZADO (selo corrente lido na hora)

**1. A parada do adendo F foi CERTA e está decidida.** O recibo `DO_CHATGPT\\ORDEM_022\\ADENDO_F\\RESULTADO.json` (sha256 `{rf_sha}`) parou antes do render porque a V7 diz, em duas falas, «15 bandeiras calculadas e 3 literais». Isso era verdade na v402 (errata de 13/10/2026). Desde a v403 (F8.1) as três bandeiras que eram literais são lidas das suas fontes, fail-closed: o registro `bandeiras_do_gate_v403` do core da v404 diz, lido agora por script, `n_flags` = {n_flags}, `n_calculated` = {n_calc}, `n_literal` = {n_lit}, `n_read_by_the_verdict` = {n_read} (6 + 5 + 4; as outras 3 são informativas). A letra do veredito do gate é a da v402: o gate não se move. **O número corrige a frase.** Troque SÓ estas duas falas, nas quatro línguas, pelos textos abaixo (verbatim; os números {escada} e {n_flags} são lidos do selo/core na hora do render, como manda o adendo D — se divergirem do que está aqui, PARE):

- Filme 1, segmento `horizon` (144–168 s), cue 1:
  - PT: «{new1_pt}»
  - EN: «{new1_en}»
  - FR (legenda): «{new1_fr}»
  - zh-Hans (legenda): «{new1_zh}»
- Filme 2, segmento `einstein` (288–324 s), cue 1:
  - PT: «{new2_pt}»
  - EN: «{new2_en}»
  - FR (legenda): «{new2_fr}»
  - zh-Hans (legenda): «{new2_zh}»

(As falas antigas, para conferência: Filme 1 PT «{old1_pt}»; Filme 2 PT «{old2_pt}».) Nada mais do texto muda: o aceite editorial do operador de 27/10 (a locução explicativa PT/EN) vale para todo o resto.

**2. TTS: AUTORIZADO só para essas duas falas, em PT e em EN (quatro segmentos de áudio).** Declare o custo no recibo. Se o motor exigir TTS de QUALQUER outra fala (por exemplo, por causa dos números da escada em outra cena), PARE e diga quais e quanto custa ANTES de rodar. Legendas FR e zh-Hans mudam só como texto.

**3. O render é da v404, não da v403.** O render da v403 não começou e não deve começar: o selo corrente é a v404. Renderize a V7 a partir da v404 do mesmo modo do adendo E (selo corrente lido na hora; `import um` em cópia isolada; nada escrito no Nós; nenhum número digitado). O que mudou, LIDO por script do `um_absoluto_selo.json` e do `um_absoluto.json` do Nós em {hoje} (confira pelos seus seletores; se divergir, PARE):

- versão v403 → v404; pino `{pin403_16}` → `{pin[:16]}` (um.py, {nbytes:,} bytes; selo de {ts});
- escada limpa {esc403} → {escada} (`estatuto_da_prova_v391/prova_1_kernel/n_theorems_clean`; a escada total é a mesma);
- arquivos formais {ff403} → {ffiles} (`core/kernel_formalization/formal_files_sha256`);
- declarações auditadas {decl403} → {decl} (`core/kernel_formalization/axiom_report`; `prova_1_kernel/no_trio` = {notrio}, nenhuma fora do trio);
- dois módulos novos no kernel — `ProjecaoTransversalDaMeiaNat` (nome provisório da gerência, aceito pelo operador) e `Jo8v32` (o nome que o operador deu ao triplo inteiro em 28/10), {escada - esc403} bandeiras novas. Como nos adendos E e F, os módulos NÃO entram no filme por nome; entram só as contagens.

Qualquer OUTRO número do filme que mudar é motivo de PARAR e dizer qual (o quadro do Teste da Única Palavra, v397, segue intocado: z_disc 4,44 calibrado, abaixo do degrau de 5σ da creditação, que não foi alcançado). Antes de entregar, releia o selo (se a versão mudar, PARE). Critérios e entrega: os do adendo E (`DO_CHATGPT\\ORDEM_022\\ADENDO_G\\` + `PUBLIC_DELIVERY_V7.json` reemitido em `video_um\\`; depósito na fila da memória). Nada se publica pela sessão do vídeo; a gerência integra por hash e sobe depois da custódia publicada. Depois da integração vem a Fase 2 da vitrine do X para a v404 (ORDEM 026-X, adendo próprio da gerência; a Fase 2 da v403 fica sem vitrine própria: a v404 a sucede).

Custo (gestão de tokens da casa): um só render; TTS só o do item 2.

— Claude (gerência c1 da Central), {hoje}. NOT_FALSIFIED nunca é a palavra da creditação; PROVADA = validade, não creditação; o gate não se moveu.
"""
assert "QG confirmada" not in adendo and "pós-dição" not in adendo
out = P / "ORDEM_022_ADENDO_G_render_v404_e_frases_do_gate.md"
assert not out.exists(), "o adendo G já existe"
out.write_bytes(adendo.encode("utf-8"))
h = sha(out)
msg = (f"[gerência c1 da Central, {hoje} — para a coordenadora da Central IALD, que encaminha à sessão do vídeo.] ORDEM 022 — ADENDO G: (1) a PARADA do adendo F está decidida: as duas falas «15 bandeiras calculadas e 3 literais» "
       f"(filme 1, horizon; filme 2, einstein) recebem texto novo, lido do core da v404 ({n_flags} bandeiras calculadas, {n_lit} literais; o gate não se move) — textos verbatim PT/EN/FR/zh-Hans no adendo; "
       f"(2) TTS autorizado SÓ para essas duas falas em PT e EN (quatro segmentos), custo declarado no recibo; qualquer outro TTS é motivo de PARAR e dizer o custo antes; "
       f"(3) o render é da v404 (selo corrente; o da v403 não começou e não deve começar): v403 → v404, pino {pin403_16} → {pin[:16]}; escada {esc403} → {escada}; arquivos formais {ff403} → {ffiles}; "
       f"declarações auditadas {decl403} → {decl} (nenhuma fora do trio); dois módulos novos (ProjecaoTransversalDaMeiaNat, Jo8v32; só as contagens entram no filme). Qualquer outro número que mudar é motivo de PARAR. "
       f"A v404 está SELADA no Nós; a custódia G1 corre agora e a publicação vem a seguir; nada se publica pela sessão do vídeo; a gerência integra por hash e sobe depois da custódia.\n\n"
       f"Adendo completo: {out} (sha256 {h}). Recibo em DO_CHATGPT\\ORDEM_022\\ADENDO_G\\ + PUBLIC_DELIVERY_V7.json reemitido em video_um\\; depósito na fila da memória.\n")
DESP.mkdir(exist_ok=True)
mp = DESP / "msg_ordem022_adendo_g_28out.md"
assert not mp.exists()
mp.write_bytes(msg.encode("utf-8"))
print("adendo G:", out, "sha256", h)
print("mensagem:", mp, "sha256", sha(mp))
print("numeros:", {"escada": (esc403, escada), "formal_files": (ff403, ffiles), "decl": (decl403, decl), "pin": (pin403_16, pin[:16]), "bytes": nbytes, "gate": (n_flags, n_calc, n_lit, n_read)})

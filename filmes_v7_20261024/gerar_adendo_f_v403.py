# -*- coding: utf-8 -*-
"""ORDEM 022 — ADENDO F (gerência c1, 28/10/2026): o render da V7 a partir da v403, autorizado pela regra da casa (a cada versão nova, um
adendo «selo corrente lido na hora»). Todos os números são LIDOS do selo/core do Nós e da entrega V7 no ar; os da v402 vêm do adendo E (lidos
por regex) e da PUBLIC_DELIVERY_V7.json. Escreve o adendo em PARA_CHATGPT e a mensagem de despacho em PROGRAMA_IALD\\despachos (não despacha)."""
import hashlib, json, os, re, time
from pathlib import Path
CEN = Path(r"C:\IALD\Central de Patentes"); NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
P = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT"; V7 = Path(r"C:\IALD\Site\tgl\v3.0\video\v7"); DESP = Path(r"C:\IALD\PROGRAMA_IALD\despachos")
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
selo = json.loads((NOS / "um_absoluto_selo.json").read_bytes()); core = json.loads((NOS / "um_absoluto.json").read_bytes()); c = core.get("core") or core
assert selo["um_version"] == "v403"
pin = selo["sha256"]["um.py"]; assert pin == sha(NOS / "um.py")
nbytes = os.path.getsize(NOS / "um.py"); ts = selo["timestamp"]
kf = c["kernel_formalization"]; pk = selo["estatuto_da_prova_v391"]["prova_1_kernel"]
escada, ffiles, decl, notrio = int(pk["n_theorems_clean"]), len(kf["formal_files_sha256"]), len(kf["axiom_report"]), int(pk["no_trio"])
assert decl == int(pk["declaracoes_auditadas"]) == notrio
ent = json.loads((V7 / "PUBLIC_DELIVERY_V7.json").read_text(encoding="utf-8"))
assert ent["source"] == "v402" and ent["anchors_all_ok"] is True
pin402 = ent["source_sha256"]
E = (P / "ORDEM_022_ADENDO_E_render_v402_autorizado.md").read_text(encoding="utf-8")
m = re.search(r"escada limpa \d+ → (\d+).*?arquivos formais \d+ → (\d+).*?declarações auditadas \d+ → (\d+)", E, re.S)
esc402, ff402, decl402 = int(m.group(1)), int(m.group(2)), int(m.group(3))
assert pin402[:16] in E
novos = sorted(os.path.basename(k)[:-5] for k in kf["formal_files_sha256"] if re.search(r"(^|[\\/])(Caminho|Vida|VerdadeAdendo)\.lean$", k))
assert novos == ["Caminho", "VerdadeAdendo", "Vida"], novos
assert escada - esc402 == 5 and ffiles - ff402 == 3 and decl - decl402 == 5, (escada, esc402, ffiles, ff402, decl, decl402)
# estado publicado da v403 (lido dos repositórios locais)
import subprocess
def git(cwd, *a): return subprocess.run(["git", "-C", cwd] + list(a), capture_output=True, text=True).stdout.strip()
esp = git(r"C:\IALD\Artigo\the_boundary", "rev-parse", "--short=8", "HEAD"); cen = git(str(CEN), "rev-parse", "--short=8", "HEAD")
hoje = time.strftime("%d/%m/%Y")
adendo = f"""[REAL — gerência c1 da Central (Claude Code), {hoje}; para a coordenadora da Central IALD no Codex, que encaminha à sessão do vídeo. A v403 está SELADA no Nós e PUBLICADA (the_boundary `{esp}`, Central `{cen}`, site no ar com «v403 · {pin[:16]}»); a V7 no ar é a da v402 (`PUBLIC_DELIVERY_V7.json`: source v402, `{pin402[:16]}`, âncoras conferidas).]

# ORDEM 022 — ADENDO F: o render da v403 está AUTORIZADO (selo corrente lido na hora); nenhuma correção nova

Pela regra da casa (a cada versão nova, um adendo «selo corrente lido na hora»): renderize a V7 a partir da v403 do mesmo modo do adendo E (selo corrente lido na hora; `import um` em cópia isolada; nada escrito no Nós; nenhum número digitado). As falas e as legendas NÃO mudam de texto além dos números lidos do selo: o aceite editorial do operador de 27/10 (a locução explicativa PT/EN) vale; não há frase nova para aprovar.

O que mudou, LIDO por script do `um_absoluto_selo.json` e do `um_absoluto.json` do Nós em {hoje} (confira pelos seus seletores; se divergir, PARE):

- versão v402 → v403; pino `{pin402[:16]}` → `{pin[:16]}` (um.py, {nbytes:,} bytes; selo de {ts});
- escada limpa {esc402} → {escada} (`estatuto_da_prova_v391/prova_1_kernel/n_theorems_clean`; a escada total é a mesma);
- arquivos formais {ff402} → {ffiles} (`core/kernel_formalization/formal_files_sha256`);
- declarações auditadas {decl402} → {decl} (`core/kernel_formalization/axiom_report`; `prova_1_kernel/no_trio` = {notrio}, nenhuma fora do trio);
- três módulos novos no kernel — `Caminho`, `Vida` e `VerdadeAdendo`, os nomes que o operador deu em 27/10 às pedras da v402 ({escada - esc402} bandeiras novas). Como no adendo E, os módulos NÃO entram no filme por nome; entram só as contagens.
- as três bandeiras do gate que eram literais passam a calculadas (F8.1); a letra do veredito do gate é a da v402 (o gate não se move). Se a V7 tiver alguma frase sobre as bandeiras do gate, PARE e diga qual: nada disso entra sem a gerência.

Qualquer OUTRO número do filme que mudar é motivo de PARAR e dizer qual (o quadro do Teste da Única Palavra, v397, segue intocado: z_disc 4,44 calibrado, abaixo do degrau de 5σ da creditação, que não foi alcançado). Antes de entregar, releia o selo (se a versão mudar, PARE). Critérios e entrega: os do adendo E (`DO_CHATGPT\\ORDEM_022\\ADENDO_F\\` + `PUBLIC_DELIVERY_V7.json` reemitido em `video_um\\`; depósito na fila da memória). Nada se publica pela sessão do vídeo; a gerência integra por hash e sobe. Depois da integração vem a Fase 2 da vitrine do X para a v403 (ORDEM 026-X, adendo próprio da gerência): o gerador da vitrine recusa enquanto a V7 no ar não for do selo corrente.

Custo (gestão de tokens da casa): um só render; sem TTS novo se o texto das falas não mudar além dos números. Se o motor exigir TTS novo por causa dos números, diga quanto custa ANTES de rodar.

— Claude (gerência c1 da Central), {hoje}. NOT_FALSIFIED nunca é a palavra da creditação; PROVADA = validade, não creditação; o gate não se moveu.
"""
out = P / "ORDEM_022_ADENDO_F_render_v403_autorizado.md"
assert not out.exists(), "o adendo F já existe"
out.write_bytes(adendo.encode("utf-8"))
h = sha(out)
msg = (f"[gerência c1 da Central, {hoje} — para a coordenadora da Central IALD, que encaminha à sessão do vídeo.] ORDEM 022 — ADENDO F: o render da V7 a partir da v403 está AUTORIZADO "
       f"(selo corrente lido na hora, como no adendo E), sem correção nova de texto. O que mudou, lido do selo/core por script: v402 → v403, pino {pin402[:16]} → {pin[:16]}; "
       f"escada {esc402} → {escada}; arquivos formais {ff402} → {ffiles}; declarações auditadas {decl402} → {decl} (nenhuma fora do trio); três módulos novos (Caminho, Vida, VerdadeAdendo; "
       f"não entram no filme por nome, só as contagens). Qualquer outro número que mudar é motivo de PARAR. A v403 está PUBLICADA (the_boundary {esp}; Central {cen}; site no ar). "
       f"Nada se publica pela sessão do vídeo; a gerência integra por hash e sobe. Se o render exigir TTS novo, diga o custo antes de rodar.\n\n"
       f"Adendo completo: {out} (sha256 {h}). Recibo em DO_CHATGPT\\ORDEM_022\\ADENDO_F\\ + PUBLIC_DELIVERY_V7.json reemitido em video_um\\; depósito na fila da memória.\n")
DESP.mkdir(exist_ok=True)
mp = DESP / "msg_ordem022_adendo_f_28out.md"
assert not mp.exists()
mp.write_bytes(msg.encode("utf-8"))
print("adendo F:", out, "sha256", h); print("mensagem:", mp, "sha256", sha(mp))
print("numeros:", {"escada": (esc402, escada), "formal_files": (ff402, ffiles), "decl": (decl402, decl), "pin": (pin402[:16], pin[:16]), "bytes": nbytes})

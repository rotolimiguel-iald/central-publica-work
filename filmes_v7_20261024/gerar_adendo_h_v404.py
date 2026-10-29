# -*- coding: utf-8 -*-
"""ORDEM 022 — ADENDO H (gerência c1, 28/10/2026): responde à parada do adendo G (STOP_ADDITIONAL_TTS_REQUIRES_AUTHORIZATION): autoriza as DUAS
sínteses adicionais (film1/return/cue0, PT e EN; só o número da escada muda, 9679 -> 9698) e o render da v404 com as SEIS unidades novas.
Os textos das duas unidades e os números vêm LIDOS do RESULTADO.json do adendo G (nada digitado). Escreve o adendo em PARA_CHATGPT e a
mensagem de despacho em PROGRAMA_IALD\\despachos (não despacha)."""
import hashlib
import json
import time
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
P = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT"
DESP = Path(r"C:\IALD\PROGRAMA_IALD\despachos")
DOG = CEN / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_022" / "ADENDO_G"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()

R = json.loads((DOG / "RESULTADO.json").read_text(encoding="utf-8"))
assert R["status"] == "STOP_ADDITIONAL_TTS_REQUIRES_AUTHORIZATION" and R["render_started"] is False and R["tts_started"] is False
assert R["order"]["path"].endswith("ORDEM_022_ADENDO_G_render_v404_e_frases_do_gate.md")
assert sha(P / "ORDEM_022_ADENDO_G_render_v404_e_frases_do_gate.md") == R["order"]["sha256"]
r_sha = sha(DOG / "RESULTADO.json")
uc = R["unit_counts"]
assert (uc["new_authorized"], uc["new_outside_authorization"]) == (4, 2), uc
add = R["additional_new_units"]
assert len(add) == 2 and {u["language"] for u in add} == {"en", "pt-BR"}
for u in add:
    assert len(u["occurrences"]) == 1 and u["occurrences"][0] == {"film": "film1", "segment": "return", "cue_index": 0}, u["occurrences"]
    assert hashlib.sha256(u["text"].encode("utf-8")).hexdigest() == u["text_sha256"]
pt = [u for u in add if u["language"] == "pt-BR"][0]
en = [u for u in add if u["language"] == "en"][0]
# o número da escada falado tem de ser o do selo corrente, lido agora
selo = json.loads((NOS / "um_absoluto_selo.json").read_bytes())
assert selo["um_version"] == "v404"
escada = int(selo["estatuto_da_prova_v391"]["prova_1_kernel"]["n_theorems_clean"])
assert str(escada) in pt["text"] and str(escada) in en["text"], (escada, pt["text"], en["text"])
cost = R["cost"]
assert cost["actual_new_tts_requests"] == 0
custo_est = cost["estimated_direct_tts_charge_all_new_units"]
hoje = time.strftime("%d/%m/%Y")
adendo = f"""[REAL — gerência c1 da Central (Claude Code), {hoje}; para a coordenadora da Central IALD no Codex, que encaminha à sessão do vídeo. Responde ao recibo do adendo G `DO_CHATGPT\\ORDEM_022\\ADENDO_G\\RESULTADO.json` (sha256 `{r_sha}`), estado `{R["status"]}`.]

# ORDEM 022 — ADENDO H: as duas sínteses adicionais estão AUTORIZADAS; o render da v404 segue

**1. A parada foi certa e está decidida.** O inventário da sessão do vídeo achou, além das quatro unidades autorizadas pelo adendo G, duas unidades sem áudio no cache: `film1/return/cue0`, em PT e em EN, onde só o número da escada muda ({escada}, lido do selo corrente, como manda o adendo D). **Autorizo as duas**, verbatim como o recibo as traz (as hashes dos textos são as do recibo):

- PT ({pt["characters"]} caracteres; sha256 do texto `{pt["text_sha256"][:16]}`): «{pt["text"]}»
- EN ({en["characters"]} caracteres; sha256 do texto `{en["text_sha256"][:16]}`): «{en["text"]}»

**2. Escopo total de TTS desta rodada: SEIS unidades novas** (as quatro do adendo G mais estas duas), nas vozes e no formato do plano v402 ({R["voices"]["pt-BR"]}, {R["voices"]["en"]}; {R["format"]}). Custo direto estimado pelo recibo: US$ {custo_est} no transporte já instalado [DERIVED, estimativa da sessão do vídeo, não cotação do provedor]; declare no recibo final o que de fato foi gasto. Qualquer SÉTIMA unidade é motivo de PARAR e dizer qual.

**3. O render da v404 segue** nos termos do adendo G (selo corrente lido na hora; `import um` em cópia isolada; nada escrito no Nós; nenhum número digitado; a comparação integral dos demais números é feita ANTES do render e qualquer outro número que mudar é motivo de PARAR). Entrega: `DO_CHATGPT\\ORDEM_022\\ADENDO_H\\` (ou o mesmo recibo do G, atualizado) + `PUBLIC_DELIVERY_V7.json` reemitido em `video_um\\`; depósito na fila da memória. Nada se publica pela sessão do vídeo; a gerência integra por hash e sobe depois da custódia publicada (o espelho `the_boundary` já está em v404; o site já diz «v404 · {selo["sha256"]["um.py"][:16]}»).

— Claude (gerência c1 da Central), {hoje}. NOT_FALSIFIED nunca é a palavra da creditação; PROVADA = validade, não creditação; o gate não se moveu.
"""
assert "QG confirmada" not in adendo and "pós-dição" not in adendo
out = P / "ORDEM_022_ADENDO_H_duas_sinteses_adicionais_autorizadas.md"
assert not out.exists(), "o adendo H já existe"
out.write_bytes(adendo.encode("utf-8"))
h = sha(out)
msg = (f"[gerência c1 da Central, {hoje} — para a coordenadora da Central IALD, que encaminha à sessão do vídeo.] ORDEM 022 — ADENDO H: a parada do adendo G (duas sínteses adicionais, film1/return/cue0 PT e EN, só o número da escada {escada}) está DECIDIDA: "
       f"as duas unidades estão AUTORIZADAS verbatim como o recibo as traz (hashes dos textos {pt['text_sha256'][:16]} e {en['text_sha256'][:16]}); escopo total SEIS unidades novas de TTS; custo direto estimado US$ {custo_est} (DERIVED, a declarar no recibo final); "
       f"qualquer sétima unidade é motivo de PARAR. O render da v404 segue nos termos do adendo G; comparação integral dos demais números antes do render; qualquer outro número que mudar é motivo de PARAR. "
       f"Nada se publica pela sessão do vídeo; a gerência integra por hash e sobe depois da custódia (o espelho e o site já estão em v404).\n\n"
       f"Adendo completo: {out} (sha256 {h}). Recibo em DO_CHATGPT\\ORDEM_022\\ADENDO_H\\ (ou o do G atualizado) + PUBLIC_DELIVERY_V7.json reemitido em video_um\\; depósito na fila da memória.\n")
DESP.mkdir(exist_ok=True)
mp = DESP / "msg_ordem022_adendo_h_28out.md"
assert not mp.exists()
mp.write_bytes(msg.encode("utf-8"))
print("adendo H:", out, "sha256", h)
print("mensagem:", mp, "sha256", sha(mp))
print("unidades adicionais:", [(u["language"], u["characters"], u["text_sha256"][:16]) for u in add], "escada", escada, "custo_est", custo_est)

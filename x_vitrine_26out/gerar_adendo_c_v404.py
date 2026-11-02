# -*- coding: utf-8 -*-
"""ORDEM 026-X — ADENDO C (gerência c1, 29/10/2026): a Fase 2 da vitrine no X para a v404 (a da v403 não existiu: a V7 da v403 nunca foi
renderizada; o adendo G da ORDEM 022 trocou o render da v403 pelo da v404). Tudo lido: o MANIFEST.json novo da vitrine, o anterior em
_anteriores\\<carimbo>\\ (para dizer o que mudou), o ponteiro V7 no AR (tem de ser v404; senão recusa), o registro da subida verificada
(carimbo e lotes), o recibo do adendo H. Escreve o adendo em PARA_CHATGPT e a mensagem de despacho em PROGRAMA_IALD\\despachos (não despacha).
Régua do X: nenhum nome de arquivo do programa solto fora de URL nos textos que o Codex publica (os textos vêm do gerador, já conferidos)."""
import hashlib
import json
import os
import re
import time
import urllib.request
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
P = CEN / "Chatgpt" / "TUNEL" / "PARA_CHATGPT"
X = P / "X_VITRINE"
DESP = Path(r"C:\IALD\PROGRAMA_IALD\despachos")
BANC = Path(r"C:\IALD\Site\tgl\v3.0_bancada")
H = CEN / "Chatgpt" / "TUNEL" / "DO_CHATGPT" / "ORDEM_022" / "ADENDO_H" / "RESULTADO.json"
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
lerj = lambda p: json.loads(Path(p).read_text(encoding="utf-8"))

m = lerj(X / "MANIFEST.json")
assert m["selo"]["versao"] == "v404" and m["selo"]["pin_um_py"].startswith("3820476c83267f61"), m["selo"]
man_sha = sha(X / "MANIFEST.json")
# cada arquivo do manifesto confere no disco
for nome, e in m["arquivos"].items():
    assert sha(X / nome) == e["sha256"] and (X / nome).stat().st_size == e["bytes"], nome
for k, v in m["videos"].items():
    assert Path(v["caminho"]).is_file() and sha(v["caminho"]) == v["sha256"], k
ant_dirs = sorted(d for d in (X / "_anteriores").iterdir() if d.is_dir() and (d / "MANIFEST.json").is_file())
ant = lerj(ant_dirs[-1] / "MANIFEST.json")
assert ant["selo"]["versao"] == "v402", ("o manifesto anterior não é o da Fase 2 da v402", ant["selo"])
mudou = {n: (m["arquivos"][n]["sha256"] != ant["arquivos"].get(n, {}).get("sha256")) for n in m["arquivos"]}
assert mudou["CUSTODIA_v404.txt"] and "CUSTODIA_v404.txt" not in ant["arquivos"]
# o AR: o ponteiro V7 do site tem de ser v404 (fail-closed)
with urllib.request.urlopen("https://teoriadagravitacaoluminodinamica.com/video/v7/PUBLIC_DELIVERY_V7.json", timeout=60) as r:
    ar = json.loads(r.read().decode("utf-8"))
assert ar.get("version") == "v404" and ar.get("source_sha256", "").startswith("3820476c83267f61"), ("o ar não tem a V7 da v404", ar.get("version"))
# a subida verificada mais recente que levou video/v7 (o manifesto completo dos lotes)
subs = sorted(d for d in (BANC / "subidas").iterdir() if d.is_dir() and not d.name.endswith("_dryrun") and (d / "RELATORIO.md").is_file())
ult = None
for d in reversed(subs):
    rel = (d / "RELATORIO.md").read_text(encoding="utf-8", errors="replace")
    if "SUBIDA VERIFICADA" in rel and (d / "MANIFESTO_SUBIDA.json").is_file():
        ms = lerj(d / "MANIFESTO_SUBIDA.json")
        if any(a["caminho"] == "video/v7/render/filme1_1080p_pt-BR.mp4" and a["sha256"] == m["videos"]["filme1"]["sha256"] for a in ms["arquivos"]):
            ult = d
            break
assert ult is not None, "nenhuma subida verificada com o filme 1 da v404"
lotes = sorted(d for d in (BANC / "revisoes").iterdir() if d.name.startswith("lotes_") and d.stat().st_mtime > time.time() - 6 * 3600)
n_lotes = len(list(lotes[-1].glob("lote_*.json"))) if lotes else 0
carimbo = ult.name[:15]
hora_ar = "%s/%s/%s às %s:%s" % (carimbo[6:8], carimbo[4:6], carimbo[0:4], carimbo[9:11], carimbo[11:13])
h = lerj(H)
assert h["status"] == "BUILT_FOR_MANAGEMENT_INTEGRATION_PUBLICATION" and h["source"] == "v404"
a = h["audio"]
s16 = lambda n: m["arquivos"][n]["sha256"][:16]
v16 = lambda k: m["videos"][k]["sha256"][:16]
hoje = time.strftime("%d/%m/%Y")
bio_txt = "A bio NÃO mudou: não toque nela." if not mudou["bio.txt"] else "A bio mudou: `bio.txt` (`%s`), verbatim." % s16("bio.txt")
fix_txt = ("O fixado mudou: `fixado.txt` (`%s`). Publique-o e fixe-o. O fixado anterior continua publicado e só deixa de ser o fixado." % s16("fixado.txt")
           if mudou["fixado.txt"] else "O fixado NÃO mudou: não publique outro.")
capa_txt = ("A capa mudou: `capa_1500x500.jpg` (`%s`), a imagem nova do filme 1." % s16("capa_1500x500.jpg")) if mudou["capa_1500x500.jpg"] else "A capa NÃO mudou."
art_txt = ("O artigo mudou (`artigo.txt`, `%s`; capa `artigo_capa_1500x600.jpg`, `%s`): aponta para a v404 e a ressalva do gate passou a dizer o que o core "
           "diz desde a v403 (as 18 bandeiras calculadas, 0 literais; o veredito lê 15; as quatro experimentais de um só booleano, aberto). Se o X permitir "
           "editar o artigo da Fase 1 no MESMO id, atualize-o com o texto verbatim (como na Fase 2 da v402). Se não permitir, NÃO publique outro artigo: relate."
           % (s16("artigo.txt"), s16("artigo_capa_1500x600.jpg"))) if mudou["artigo.txt"] else "O artigo NÃO mudou."
adendo = f"""# ORDEM 026-X — ADENDO C · Fase 2 da vitrine no X para a v404 ({hoje})

Da gerência c1 (Claude, Central), sob a ORDEM 026-X (a vitrine da TGL no X; numeração em `ORDEM_026_NUMERACAO_duas_ordens_026.md`), o seu ADENDO A (sem o nome do programa solto nos textos) e o ADENDO B (a Fase 2 da v402, executada e aceita em 28/10). A Fase 2 da v403 NÃO existiu: a V7 da v403 não foi renderizada (o adendo G da ORDEM 022 trocou aquele render pelo da v404), e a vitrine só se publica com os filmes do selo corrente.

**O que mudou:** a v404 está custodiada e publicada (espelho `the_boundary` e site). Os dois filmes V7 renderizados da v404 (ORDEM 022, adendos G e H: as frases do gate lidas do core, {a["new_units"]} sínteses novas e {a["reused_units"]} reutilizadas, revisão independente) estão NO AR no site desde {hora_ar}, com subida verificada ({n_lotes} lotes atômicos mais o manifesto completo). A autorização do operador para integrar e publicar os dois filmes é a do recibo `DO_CHATGPT\\ORDEM_022\\ADENDO_E\\AUTORIZACAO_OPERADOR_INTEGRAR_PUBLICAR_20261027.json`, e a ordem da casa é a sua: a cada custódia, fixado e post da versão.

**O manifesto novo:** `X_VITRINE\\MANIFEST.json`, sha256 `{man_sha}`, versão do selo v404, pin `{m["selo"]["pin_um_py"]}`, gerado em {m["gerado_em"]}. O manifesto da Fase 2 da v402 está em `X_VITRINE\\_anteriores\\{ant_dirs[-1].name}\\`. Confira por script o sha256 de cada arquivo contra o manifesto antes de usar. Se algum divergir, PARE.

## O que publicar (modo seguro, um item por vez, recibo de cada um)

1. **O post da versão:** `CUSTODIA_v404.txt` (sha256 `{m["arquivos"]["CUSTODIA_v404.txt"]["sha256"]}`), verbatim. Depois de publicar, acrescente-o aos Destaques.
2. **Os dois filmes da v404,** como posts novos. Cada um leva o texto verbatim do `filme1_post.txt` (`{s16("filme1_post.txt")}`) e do `filme2_post.txt` (`{s16("filme2_post.txt")}`), com o vídeo de narração pt-BR do manifesto e a legenda pt-BR (`filme1_pt-BR.srt` `{s16("filme1_pt-BR.srt")}` e `filme2_pt-BR.srt` `{s16("filme2_pt-BR.srt")}`); se a interface oferecer um segundo espaço de legenda, a EN (`{s16("filme1_en.srt")}`, `{s16("filme2_en.srt")}`). Os vídeos (caminho e sha256 no manifesto, campo `videos`):
   - filme 1: `{m["videos"]["filme1"]["caminho"]}` (`{v16("filme1")}`, {m["videos"]["filme1"]["duracao_s"]} s)
   - filme 2: `{m["videos"]["filme2"]["caminho"]}` (`{v16("filme2")}`, {m["videos"]["filme2"]["duracao_s"]} s)
   Acrescente os dois aos Destaques. Os posts dos filmes da v401 e da v402 continuam publicados, sem edição.
3. **O fixado:** {fix_txt}
4. **A capa:** {capa_txt}
5. **A bio:** {bio_txt} O nome «L», a foto e o @ não se tocam.
6. **O artigo:** {art_txt}

## Paradas

- Login, verificação de conta, captcha ou qualquer pedido de pagamento: PARE e relate. Você nunca paga nem loga pelo operador.
- Mensagem de erro, texto truncado, ou o X transformando algum nome em link: PARE no item e relate. Não reescreva o texto.
- Nada de repetir a Fase 1 nem a Fase 2 da v402: o que já foi publicado não se publica de novo.

## A devolução

`DO_CHATGPT\\ORDEM_026\\VITRINE\\RESULTADO_FASE2_v404.json` com:
- a URL e o id de cada post;
- o sha256 de cada arquivo usado;
- capturas do perfil final e do fixado (texto de acessibilidade: as URLs vêm como nós «link» separados; a gerência confere texto e URLs à parte);
- o que não foi feito e por quê.

Depósito na fila da memória. A gerência confere e dá o aceite. NOT_FALSIFIED nunca é a palavra da creditação; PROVADA = validade; o gate não se moveu.

— Claude (gerência c1 da Central), {hoje}.
"""
assert "QG confirmada" not in adendo and "pós-dição" not in adendo
out = P / "ORDEM_026_ADENDO_C_fase2_v404.md"
assert not out.exists(), "o adendo C já existe"
out.write_bytes(adendo.encode("utf-8"))
hh = sha(out)
msg = (f"[gerência c1 da Central, {hoje} — para a coordenadora da Central IALD, que encaminha a quem executa a vitrine do X.] ORDEM 026-X — ADENDO C: a Fase 2 da vitrine para a v404 "
       f"(a da v403 não existiu: a V7 da v403 não foi renderizada). Os dois filmes V7 da v404 estão no ar no site desde {hora_ar} (subida verificada, {n_lotes} lotes + manifesto completo). "
       f"Manifesto novo X_VITRINE\\MANIFEST.json sha256 {man_sha} (v404, pin {m['selo']['pin_um_py'][:16]}). Publicar em modo seguro, um item por vez, recibo de cada um: "
       f"o post da versão CUSTODIA_v404.txt ({m['arquivos']['CUSTODIA_v404.txt']['sha256'][:16]}); os dois filmes (posts verbatim + vídeo pt-BR + legenda pt-BR; EN se houver segundo espaço); "
       f"fixado {'novo (publicar e fixar)' if mudou['fixado.txt'] else 'sem mudança'}; capa {'nova' if mudou['capa_1500x500.jpg'] else 'sem mudança'}; bio {'mudou' if mudou['bio.txt'] else 'NÃO mudou (não tocar)'}; "
       f"artigo {'atualizado no MESMO id (a ressalva do gate agora lê bandeiras_do_gate_v403); se não der para editar, relatar, nunca criar outro' if mudou['artigo.txt'] else 'sem mudança'}. "
       f"Paradas: login/pagamento/captcha, erro, texto truncado, nome virando link. Nada se repete da Fase 1 nem da Fase 2 da v402.\n\n"
       f"Adendo completo: {out} (sha256 {hh}). Devolução: DO_CHATGPT\\ORDEM_026\\VITRINE\\RESULTADO_FASE2_v404.json + depósito na fila da memória.\n")
DESP.mkdir(exist_ok=True)
mp = DESP / "msg_ordem026_adendo_c_29out.md"
assert not mp.exists()
mp.write_bytes(msg.encode("utf-8"))
print("adendo C:", out, "sha256", hh)
print("mensagem:", mp, "sha256", sha(mp))
print("mudou:", {k: v for k, v in mudou.items()}, "| ar:", ar.get("version"), "| subida:", ult.name, "| lotes:", n_lotes)

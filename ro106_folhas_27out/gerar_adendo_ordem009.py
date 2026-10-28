# -*- coding: utf-8 -*-
"""ORDEM 009 — ADENDO 001 AO MANIFESTO DE INSUMOS (P3/B4): as folhas substitutivas e as cartas da Regra 26.4 dos RO/106 do MQC (050579) e do
Aprendizado (050576), ACEITAS pela revisão independente (R2 do MQC; R3 do Aprendizado). Hash e páginas lidos dos arquivos por script.
Não escreve sobre adendo existente (open 'x')."""
import hashlib, json, time
from pathlib import Path
K = Path(r"C:\IALD\Central de Patentes\work\ro106_folhas_27out")
R = K / "REVISAO"
OUT = Path(r"C:\TUNEL_PCT\PARA_CODEX\ORDEM_009_INSUMOS_ADENDO_001.json")
try:
    from pypdf import PdfReader
    pag = lambda p: len(PdfReader(str(p)).pages)
except Exception:  # noqa: BLE001
    pag = lambda p: None
def item(p, destino, papel, nota):
    b = p.read_bytes()
    return {"destino": destino, "caminho": str(p), "bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(), "paginas": pag(p), "papel": papel, "nota": nota}
def rev(p):
    return {"caminho": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
d = {
 "ordem": "ORDEM 009 — ADENDO 001 AO MANIFESTO DE INSUMOS (P3/B4: resposta aos RO/106 de 09/10/2026 do MQC e do Aprendizado)",
 "gerado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
 "gerador": "Claude (Central, gerência a7) — preparação sonnet-ro106-preparador; revisão independente sonnet-ro106-revisor",
 "nota": ("Libera para ANEXAR, em resposta ao RO/106 de cada PCT, as folhas de substituição dos desenhos e a carta da Regra 26.4 aqui listadas — "
          "SÓ depois da frase B4 do operador digitada na conversa, uma por PCT: «PODE ENVIAR AS FOLHAS SUBSTITUTIVAS DOS DESENHOS DO 050579» / "
          "«... DO 050576». Conferir o sha256 antes de anexar; divergência = PARE. Prazo FATAL 09/12/2026 (Regra 26.5); o RO marca as folhas "
          "(Seção 325: canto superior direito e margem inferior, deixados livres). Numeração n/N com o novo total (Seção 207; o conjunto de "
          "desenhos é substituído inteiro: 050576 5→6 folhas, 050579 3→8). A carta tem o bloco de assinatura, local e data em branco: a "
          "assinatura é a do envio pelo ePCT autorizada pela frase [LEGAL]. Não libera pagamento: se a tela pedir taxa por folha, PARE e relate. "
          "No 050576 vai a variante PRINCIPAL (conservadora: «PHO», como visível no depositado); a variante «PHOT» só por adendo novo da Central, "
          "se o operador e o agente de PI a escolherem. Escolhas [LEGAL] em aberto, listadas na REVISÃO: PHO/PHOT, sentido das setas da Fig. 1 "
          "(o do depositado), forma dos glifos 𝒜/ℰ (MQC Fig. 8), substituição integral, altura-x das minúsculas sem haste."),
 "arquivos": [
  item(K / "FOLHAS_SUBSTITUTIVAS_050579.pdf", "ePCT PCT/BR2026/050579 (MQC) — resposta ao RO/106 de 09/10/2026", "ANEXAR",
       "folhas de substituição dos desenhos (Regra 26), 8 folhas; REVISÃO R2 ACEITA"),
  item(K / "CARTA_REGRA_26_4_050579.pdf", "ePCT PCT/BR2026/050579 (MQC) — resposta ao RO/106 de 09/10/2026", "ANEXAR",
       "carta da Regra 26.4"),
  item(K / "FOLHAS_SUBSTITUTIVAS_050576.pdf", "ePCT PCT/BR2026/050576 (Aprendizado Contínuo) — resposta ao RO/106 de 09/10/2026", "ANEXAR",
       "folhas de substituição dos desenhos (Regra 26), 6 folhas, variante PRINCIPAL; REVISÃO R3 ACEITA"),
  item(K / "CARTA_REGRA_26_4_050576.pdf", "ePCT PCT/BR2026/050576 (Aprendizado Contínuo) — resposta ao RO/106 de 09/10/2026", "ANEXAR",
       "carta da Regra 26.4 da variante PRINCIPAL"),
 ],
 "revisao": [rev(R / "REVISAO_RO106_050579_R2.md"), rev(R / "REVISAO_RO106_050579_R2.json"),
             rev(R / "REVISAO_RO106_050576_R3.md"), rev(R / "REVISAO_RO106_050576_R3.json")],
 "nao_liberado": [item(K / "FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf", "—", "NAO_ANEXAR", "variante PHOT: só por adendo novo"),
                  item(K / "CARTA_REGRA_26_4_050576_PHOT.pdf", "—", "NAO_ANEXAR", "carta da variante PHOT: só por adendo novo")],
}
with OUT.open("x", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print(OUT, hashlib.sha256(OUT.read_bytes()).hexdigest()[:16])
for a in d["arquivos"]:
    print(a["sha256"][:16], a["paginas"], Path(a["caminho"]).name)

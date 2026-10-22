# -*- coding: utf-8 -*-
"""Filtro das NOTAS OPERACIONAIS do operador (critério do operador, 22/10/2026: «não precisa se tornar público as notas de aviso pra
mim, a exemplo do protocolo do MS e as leituras das patentes»). Usado no retrato do cockpit e nos repositórios públicos. Nada é
apagado em silêncio: cada trecho omitido vira a linha «[nota operacional do operador — omitida no retrato público]». O original fica
intocado na Central do operador.
v2 (22/10, mesma sessão): «ENTREGA/REVISÃO/ORDEM» só contam no contexto do protocolo (PCT, INPI, RO/, IB/) — as ENTREGAS da bancada do
ChatGPT são ciência (pedras, teoremas) e ficam; «Sentinela», «GRU», «Pix» só como palavra inteira («biosentinelas», «grupo», «pixel» ficam)."""
import re

MARCA = "> [nota operacional do operador — omitida no retrato público]"
TERMOS = re.compile(
    r"(?i)(prazo fatal|alvo precaucional|\bRO/10[0-9]\b|\bIB/3[0-9]{2}\b|mandado de seguran|\bMS\b.{0,12}(28/10|ACOM|ajuiz)|\bGRU\b|\bpix\b|"
    r"\beOwner\b|exig[eê]ncia do INPI|despacho da RPI|\bsentinela\b|monitor de patentes|c[oó]digo 2(48|60)\b|Regra 20\.5|Rule 20\.5|"
    r"emenda restritiva|segunda gera[cç][aã]o do ACOM|marcos_fixos|ENTRADA_CODEX|TUNEL_PCT|REVIS[AÃ]O[_ ]0\d\d.{0,200}PCT|"
    r"ENTREGA[_ ]0\d\d.{0,120}(PCT|INPI|RO/|IB/)|ePCT.{0,30}(prazo|janela|transmiss|pagamento|taxa))")
SECOES_FORA = re.compile(r"^#{2,4}\s*J\.3\b")      # «J.3 — Prazos, procedimento e achados vivos» sai inteira


def filtrar_markdown(t: str) -> tuple[str, int]:
    """Tira a seção J.3 inteira e todo bloco (separado por linha em branco) que traga termo operacional."""
    linhas = t.split("\n")
    out, n, pulando, nivel = [], 0, False, 0
    for ln in linhas:
        m = re.match(r"^(#{1,6})\s", ln)
        if m:
            if pulando and len(m.group(1)) <= nivel:
                pulando = False
            if SECOES_FORA.match(ln):
                pulando, nivel = True, len(m.group(1))
                out.append(ln.split("—")[0].rstrip() + " — (seção operacional do operador: omitida no retrato público)")
                n += 1
                continue
        if not pulando:
            out.append(ln)
    t = "\n".join(out)
    blocos = re.split(r"(\n\s*\n)", t)
    res = []
    for b in blocos:
        if b.strip() and TERMOS.search(b):
            res.append(MARCA); n += 1
        else:
            res.append(b)
    return "".join(res), n

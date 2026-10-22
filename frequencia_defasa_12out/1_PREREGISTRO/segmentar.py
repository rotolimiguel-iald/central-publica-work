# -*- coding: utf-8 -*-
# Segmentacao dos quatro textos do operador em FRASES (somente leitura dos textos).
# Regra fixa: (1) linhas nao vazias; (2) dentro da linha, corte apos [.!?] seguido de espaco e de
# maiuscula/aspas/asterisco/parentese, desde que o caractere antes do ponto NAO seja digito
# (evita cortar enumeracoes "1. O Posto"). Linhas so de marcacao ("---") viram segmento de marcacao.
# Uso: importado por gerar_preregistro.py; rodado sozinho, imprime os segmentos.
import hashlib, json, re, sys, unicodedata

BASE = "C:\\IALD\\Central de Patentes\\work\\"
TEXTOS = {
    "V1": BASE + "cunhagens_12out\\OPERADOR_10out_posto_rank_texto_verbatim.txt",
    "V2": BASE + "cunhagens_12out\\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "V3": BASE + "cunhagens_10out\\OPERADOR_10out_posto_rank_verbatim.txt",
    "V4": BASE + "cunhagens_10out\\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
}
SHA16_ORDEM = {"V1": "8d252f24e2806ff3", "V2": "2c8b7b712aa9ad7f", "V3": "5b9afcc691a0e1e4", "V4": "b365591ceb346cdf"}
V2_FRONTEIRA_TEMPO = "O que mais me fascina"   # a parte do TEMPO (F1.TEMPO) comeca nesta linha

_CORTE = re.compile(r'(?<=[^\d][.!?])\s+(?=[A-Z\u00C0-\u00DD"\u201C*(])')
_MARCACAO = re.compile(r'^\s*(-{3,}|\*{3,}|_{3,})\s*$')


def ler(chave):
    b = open(TEXTOS[chave], "rb").read()
    h = hashlib.sha256(b).hexdigest()
    if h[:16] != SHA16_ORDEM[chave]:
        raise SystemExit("FALHA VISIVEL: %s sha16 %s difere da ordem %s" % (chave, h[:16], SHA16_ORDEM[chave]))
    if b.startswith(b"\xef\xbb\xbf"):
        raise SystemExit("FALHA VISIVEL: %s tem BOM" % chave)
    return b, h, b.decode("utf-8")


def normalizar(s):
    """Para comparar V1 e V2: tira marcacao markdown e espacos, NFC."""
    s = unicodedata.normalize("NFC", s)
    s = re.sub(r"^\s*(#+\s*|\*\s+|\*\s{2,})", "", s)
    s = s.replace("**", "").replace("*", "")
    s = re.sub(r"\s+", " ", s).strip()
    return s


def segmentos(chave):
    b, h, t = ler(chave)
    linhas = t.split("\n")
    out = []
    fronteira = None
    if chave == "V2":
        for i, ln in enumerate(linhas, 1):
            if ln.startswith(V2_FRONTEIRA_TEMPO):
                fronteira = i
                break
        if fronteira is None:
            raise SystemExit("FALHA VISIVEL: fronteira do tempo nao achada em V2")
    for i, ln in enumerate(linhas, 1):
        if not ln.strip():
            continue
        escopo = "TRILHA_POSTO"
        if chave == "V2" and i >= fronteira:
            escopo = "FORA_DO_ESCOPO_F1_TEMPO"
        if _MARCACAO.match(ln):
            out.append(dict(id="%s.L%02d.M" % (chave, i), texto=ln, linha=i, frase=0, tipo="MARCACAO", escopo=escopo))
            continue
        partes = [p for p in _CORTE.split(ln.strip()) if p.strip()]
        for k, p in enumerate(partes, 1):
            out.append(dict(id="%s.L%02d.S%d" % (chave, i, k), texto=p, linha=i, frase=k, tipo="FRASE", escopo=escopo))
    return out, h, len(b), fronteira


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    todos = {}
    for c in ("V1", "V2", "V3", "V4"):
        segs, h, n, fr = segmentos(c)
        todos[c] = segs
        print("=====", c, n, h, "fronteira_tempo=%s" % fr)
        for s in segs:
            print("%-14s %-24s %s" % (s["id"], s["escopo"][:24], s["texto"][:150]))
    # V2 x V1 (so trilha)
    v1n = {normalizar(s["texto"]): s["id"] for s in todos["V1"]}
    print("===== V2 identico a V1 (normalizado)?")
    for s in todos["V2"]:
        if s["escopo"] != "TRILHA_POSTO":
            continue
        print("%-14s -> %s" % (s["id"], v1n.get(normalizar(s["texto"]), "(sem par em V1)")))

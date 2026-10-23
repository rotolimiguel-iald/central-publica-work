# -*- coding: utf-8 -*-
"""f9v2_text.py -- leitura de FONTES PUBLICAS como dado nao confiavel: bytes -> texto normalizado, sem executar nada.
HTML: remove script/style/tags, desfaz entidades, normaliza espacos e sinais (U+00B1, U+2212). PDF: pypdf, pagina a pagina.
Usado pelo runner (extracao dos centros) e pelas ferramentas de pinagem. Rodar sempre com python -I."""
import html
import io
import re
import unicodedata


def norm_text(s):
    s = html.unescape(s)
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("±", "+/-").replace("−", "-").replace("–", "-").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def html_to_text(raw):
    t = raw.decode("utf-8", "replace")
    t = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    return norm_text(t)


def pdf_pages_text(raw):
    from pypdf import PdfReader
    rd = PdfReader(io.BytesIO(raw))
    return [norm_text(p.extract_text() or "") for p in rd.pages]

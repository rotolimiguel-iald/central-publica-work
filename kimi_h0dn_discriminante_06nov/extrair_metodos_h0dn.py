from pathlib import Path
import re
from bs4 import BeautifulSoup

SOURCE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\cross_rung\H0DN_paper_v1.html")
OUT = Path(r"C:\IALD\Central de Patentes\work\kimi_h0dn_discriminante_06nov\H0DN_METODOS_AGREGACAO.md")
PATTERN = re.compile(
    r"inverse[- ]variance|weighted|weighting|aggregat|multiple surveys|"
    r"multiple light|same SN|duplicate|light.curve|covariance|calibrator",
    re.IGNORECASE,
)

soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
lines = [
    "# Trechos metodológicos do artigo H0DN v1",
    "",
    "Extração local de parágrafos, sem leitura ou ajuste de centros observados.",
    "",
]
count = 0
for element in soup.find_all(["p", "li", "figcaption"]):
    text = " ".join(element.get_text(" ", strip=True).split())
    if len(text) < 20 or not PATTERN.search(text):
        continue
    # Avoid nested duplicate list/paragraph text.
    if element.name == "li" and element.find_parent("li") is not None:
        continue
    heading = element.find_previous(["h1", "h2", "h3", "h4", "h5"])
    section = " ".join(heading.get_text(" ", strip=True).split()) if heading else "(sem seção)"
    count += 1
    lines.extend([f"## {count}. {section}", "", text, ""])
    if count >= 180:
        break
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"matches={count} output={OUT}")

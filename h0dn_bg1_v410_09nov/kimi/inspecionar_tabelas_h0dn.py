from pathlib import Path
from bs4 import BeautifulSoup

SOURCE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\cross_rung\H0DN_paper_v1.html")
OUT = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\TABELAS_H0DN.txt")

soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
lines = []
for table in soup.find_all("table"):
    caption = table.find("figcaption")
    text = " ".join((caption or table).get_text(" ", strip=True).split())
    rows = table.find_all("tr")
    if any(key in text for key in ["baseline", "Baseline", "parameter", "Distance", "H0", "Table 2", "Table 3", "Table 4"]):
        lines.append(f"ID={table.get('id')} rows={len(rows)} TEXT={text[:1200]}\n")
OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"tables_selected={len(lines)} output={OUT}")

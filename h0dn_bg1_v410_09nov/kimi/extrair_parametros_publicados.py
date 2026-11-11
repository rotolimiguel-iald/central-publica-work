from pathlib import Path
from bs4 import BeautifulSoup
import json

SOURCE = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\cross_rung\H0DN_paper_v1.html")
OUT = Path(r"C:\IALD\Central de Patentes\work\h0dn_bg1_v410_09nov\kimi\PARAMETROS_PUBLICADOS_TABELAS.json")
soup = BeautifulSoup(SOURCE.read_text(encoding="utf-8"), "html.parser")
result = {}
for table_id in ["A6.T11.2", "A6.T12.2"]:
    table = soup.find("table", id=table_id)
    rows = []
    for tr in table.find_all("tr"):
        cells = [" ".join(td.get_text(" ", strip=True).split()) for td in tr.find_all(["td", "th"])]
        if cells:
            rows.append(cells)
    result[table_id] = rows
OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
for table_id, rows in result.items():
    print(table_id, "rows", len(rows))
    for row in rows[-20:]:
        print(row)

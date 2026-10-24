# -*- coding: utf-8 -*-
import re
p = r"C:\IALD\Central de Patentes\x"
print(p, len(p))
print(re.findall(r"\*\*(v\d{3}) SELADA", "## **v398 SELADA**"))
print("linha\nliteral", '\d+', "\u00e9")

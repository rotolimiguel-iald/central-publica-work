# -*- coding: utf-8 -*-
"""A vigia do handoff da v410 (ordem do operador de 10/11/2026: «assim que cair vc já faça tudo de forma desassistida»; verbatim em
work\\cunhagens_13out\\OPERADOR_10nov_v410_atualize_e_publique_tudo_desassistido_verbatim.txt). So leitura. A cada 5 min confere:
  1. o selo do No's diz um_version = v410 e fail_closed_selftest = FAIL_CLOSED_SELFTEST_PASSED;
  2. existe No's\\HANDOFF_v410_CUSTODIA.md;
  3. existe work\\cadeia_de_selo\\v410\\ORDEM_HANDOFF_CUSTODIA_v410.md (a c1 o grava POR ULTIMO: e o gatilho);
  4. nenhum dos dois arquivos mudou nos ultimos 3 min (a c1 terminou de escrever).
Sai (e a sessao de custodia acorda) quando os quatro valem. Grava o batimento em VIGIA_ULTIMO_BATIMENTO.txt. Falha de leitura (selo sendo escrito) = tenta de novo."""
import json
import time
from pathlib import Path

NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
ORD = Path(r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\ORDEM_HANDOFF_CUSTODIA_v410.md")
HO = NOS / "HANDOFF_v410_CUSTODIA.md"
BAT = Path(__file__).with_name("VIGIA_ULTIMO_BATIMENTO.txt")
V = "v410"


def estado():
    try:
        s = json.loads((NOS / "um_absoluto_selo.json").read_text(encoding="utf-8"))
        selo_ok = s.get("um_version") == V and s.get("fail_closed_selftest") == "FAIL_CLOSED_SELFTEST_PASSED"
        selo_txt = "%s/%s" % (s.get("um_version"), s.get("fail_closed_selftest"))
    except Exception as e:  # noqa: BLE001  (o selo pode estar sendo escrito)
        selo_ok, selo_txt = False, "ilegivel (%s)" % type(e).__name__
    agora = time.time()
    arquivos = all(p.is_file() for p in (HO, ORD))
    parados = arquivos and all(agora - p.stat().st_mtime > 180 for p in (HO, ORD))
    return selo_ok and arquivos and parados, "selo %s | handoff %s | ordem %s | parados %s" % (selo_txt, HO.is_file(), ORD.is_file(), parados)


while True:
    ok, txt = estado()
    BAT.write_text(time.strftime("%Y-%m-%d %H:%M:%S") + " " + txt + "\n", encoding="utf-8")
    if ok:
        print("HANDOFF v410 CAIU:", txt)
        break
    time.sleep(300)

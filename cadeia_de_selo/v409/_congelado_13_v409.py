# -*- coding: utf-8 -*-
"""_congelado_13_v409.py -- (claude-construtor-v409, 05/11/2026) a lista CONGELADA das falas ganha a 13a: a ORDEM do operador «eu quero que entre tudo na versão 409 não deixar nada para a v410»
(DESENHO, AO LADO de ~18h; sha256 LIDO do arquivo; o prefixo do DESENHO conferido). Backup de bytes; temporario -> conferir -> substituir."""
import datetime, hashlib, json, os
H = os.path.dirname(os.path.abspath(__file__)); CONG = os.path.join(H, "VERBATIM_CONGELADO_v409.json")
NOVA = os.path.join(os.path.dirname(os.path.dirname(H)), "cunhagens_13out", "OPERADOR_05nov_tudo_na_v409_nada_para_a_v410_verbatim.txt")
raw = open(CONG, "rb").read(); c = json.loads(raw.decode("utf-8"))
assert c["n"] == 12 == len(c["arquivos"]) and NOVA not in c["arquivos"], c["n"]
b = open(NOVA, "rb").read(); h = hashlib.sha256(b).hexdigest(); assert h.startswith("fb3dc69e3c9b5516"), h[:16]
c["arquivos"].append(NOVA); c["registro"].append({"arquivo": NOVA, "sha256": h, "bytes": len(b), "autor": "operador"}); c["n"] = len(c["arquivos"])
c.setdefault("acrescimos", []).append({"quando": datetime.datetime.now().isoformat(timespec="seconds"), "por": "claude-construtor-v409", "o_que": "a 13a fala: a ORDEM do operador que traz tudo para a v409 (DESENHO, AO LADO de ~18h), inteira", "sha16": h[:16]})
c["nota"] = ("as treze falas de 05/11/2026 que esta versao embute (as dez do DESENHO_v409 §3 e as tres dos AO LADO do fim dele); de tres, so' o trecho e' embutido e citado (duas pela D59; uma porque o resto e' aviso operacional); "
             "lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); bk = CONG + ".bak_" + ts + "_tudo"; open(bk, "wb").write(raw); assert open(bk, "rb").read() == raw
nb = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8"); open(CONG + ".tmp", "wb").write(nb); assert os.path.getsize(CONG + ".tmp") == len(nb); os.replace(CONG + ".tmp", CONG)
print("VERBATIM_CONGELADO_v409.json:", c["n"], "falas; a 13a", h[:16])

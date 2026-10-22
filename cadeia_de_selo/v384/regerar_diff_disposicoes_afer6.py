# -*- coding: utf-8 -*-
"""8a afericao (7N10/8N10): a evidencia da errata da gravacao inline da 6a (diff_disposicoes_afer6_edicao_inline.txt, sha256 1426f55d...) foi gravada
TRANSCODIFICADA (cp1252, CRLF misturado), nao como os bytes do diff. Aqui o diff e' REGERADO por script salvo, a partir dos BYTES dos dois estados (o backup
.bak_20261004_064923 e o estado gravado, que e' o .bak_antes_afer7, identico ao .bak_20261004_073834), com o diff do Git, saida gravada em wb. O arquivo
antigo FICA como registro (nao e' apagado nem sobrescrito)."""
import hashlib, json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(HERE, "disposicoes_afericoes_v384.json.bak_20261004_064923")
B = os.path.join(HERE, "disposicoes_afericoes_v384.json.bak_antes_afer7")
h = lambda b: hashlib.sha256(b).hexdigest()
ba, bb = open(A, "rb").read(), open(B, "rb").read()
assert b"\r" not in ba and b"\r" not in bb, "os dois estados sao UTF-8 com LF"
assert bb == open(os.path.join(HERE, "disposicoes_afericoes_v384.json.bak_20261004_073834"), "rb").read()
r = subprocess.run(["diff", os.path.basename(A), os.path.basename(B)], cwd=HERE, capture_output=True)
assert r.returncode == 1 and r.stdout, (r.returncode, r.stderr)   # 1 = ha diferenca
OUT = os.path.join(HERE, "diff_disposicoes_afer6_edicao_inline_BYTES.txt")
assert not os.path.exists(OUT) or open(OUT, "rb").read() == r.stdout, "ja existe com outro conteudo"
open(OUT + ".tmp", "wb").write(r.stdout); assert open(OUT + ".tmp", "rb").read() == r.stdout; os.replace(OUT + ".tmp", OUT)
VELHO = os.path.join(HERE, "diff_disposicoes_afer6_edicao_inline.txt")
rec = {"regerado": os.path.basename(OUT), "sha256": h(r.stdout), "bytes": len(r.stdout), "comando": "diff %s %s" % (os.path.basename(A), os.path.basename(B)),
       "de": {"arquivo": os.path.basename(A), "sha256": h(ba)}, "para": {"arquivo": os.path.basename(B), "sha256": h(bb)},
       "antigo_transcodificado_fica_como_registro": {"arquivo": os.path.basename(VELHO), "sha256": h(open(VELHO, "rb").read())},
       "o_antigo_decodificado_em_cp1252_e_normalizado_para_LF_confere_com_o_regerado":
           open(VELHO, "rb").read().decode("cp1252").replace("\r\n", "\n").encode("utf-8") == r.stdout}
json.dump(rec, open(OUT + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rec, ensure_ascii=False, indent=1))

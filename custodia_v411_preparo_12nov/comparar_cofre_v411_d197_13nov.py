# -*- coding: utf-8 -*-
"""D197: compara, hash a hash, o cofre da v411 regerado pela C3 com o movido para C:\\t (13/11/2026, claude-site-custodia).
Só pode diferir o SEMANTICA_CUSTODIA.json e, no CUSTODY_MANIFEST.json do um_unificado, só o campo que pina o sha256 dele
(semantica_custodia.sha256). Qualquer outra diferença: PARA (código 1). Só leitura."""
import hashlib, json, sys
from pathlib import Path

OC = Path(r"C:\IALD\Central de Patentes\vault\originals_copy")
DEST = Path(r"C:\t\custodia_v411_cofre_antes_d197")
rec = json.loads((DEST / "RECIBO_MOVER_COFRE_v411_D197.json").read_text(encoding="utf-8"))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


dif = []
for n, arqs in rec["arquivos"].items():
    novos = {str(p.relative_to(OC / n)).replace("\\", "/") for p in (OC / n).rglob("*") if p.is_file()}
    if novos != set(arqs):
        dif.append("%s: conjunto de arquivos difere (+%s -%s)" % (n, sorted(novos - set(arqs))[:5], sorted(set(arqs) - novos)[:5]))
    for k, e in arqs.items():
        p = OC / n / k
        if not p.is_file() or sha(p) == e["sha256"]:
            continue
        if n == "um_unificado_v411" and k == "SEMANTICA_CUSTODIA.json":
            print("  difere (permitido): %s/%s" % (n, k))
            continue
        if n == "um_unificado_v411" and k == "CUSTODY_MANIFEST.json":
            a = json.loads((DEST / n / k).read_text(encoding="utf-8"))
            b = json.loads(p.read_text(encoding="utf-8"))
            ra, rb = dict(a), dict(b)
            sa, sb = dict(ra.pop("semantica_custodia", {})), dict(rb.pop("semantica_custodia", {}))
            ha, hb = sa.pop("sha256", None), sb.pop("sha256", None)
            if ra == rb and sa == sb and hb == sha(OC / n / "SEMANTICA_CUSTODIA.json"):
                print("  difere (permitido): %s/%s, só semantica_custodia.sha256 (%s -> %s, o do SEMANTICA novo)" % (n, k, str(ha)[:16], str(hb)[:16]))
                continue
            dif.append("%s/%s: difere além do pino da semântica: %s" % (n, k, sorted(x for x in set(ra) | set(rb) if ra.get(x) != rb.get(x))[:8]))
            continue
        dif.append("%s/%s difere" % (n, k))
S = json.loads((OC / "um_unificado_v411" / "SEMANTICA_CUSTODIA.json").read_text(encoding="utf-8"))
S0 = json.loads((DEST / "um_unificado_v411" / "SEMANTICA_CUSTODIA.json").read_text(encoding="utf-8"))
so_regra = ({k: x for k, x in S.items() if k != "blocos"} == {k: x for k, x in S0.items() if k != "blocos"}
            and {k: x for k, x in S["blocos"].items() if k != "cunhagens_v411"} == {k: x for k, x in S0["blocos"].items() if k != "cunhagens_v411"}
            and S["blocos"]["cunhagens_v411"]["campos"] == [{"caminho": "kernel.bandeiras", "par_igual_zero": True}, {"caminho": "kernel.declaracoes_no_trio", "par_igual_zero": True}])
print("  no SEMANTICA, só a regra do cunhagens_v411 mudou (par_igual -> par_igual_zero):", so_regra)
if not so_regra:
    dif.append("SEMANTICA_CUSTODIA.json: difere além da regra do cunhagens_v411")
print("RESULTADO:", "IGUAL, exceto o permitido" if not dif else "DIFERE - PARAR: " + "; ".join(dif))
sys.exit(1 if dif else 0)

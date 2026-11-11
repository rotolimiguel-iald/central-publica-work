# -*- coding: utf-8 -*-
"""_r6c_17_p00_fala_de_trecho_fora_do_recibo_v410.py -- ADAPTACAO MECANICA MINIMA, fora da ESPEC e FORA do candidato (dita no relatorio; sha antes e depois em _r6c_RESULTADO_v410.json):
a checagem do p00 «[v410, AEscala, D87] a pedra TGLExt.AEscala ...» compara as falas do recibo dos nomes (por sha256) com as do contrato do candidato, tirando as que estao FORA do recibo (DL.FALAS_FORA_DO_RECIBO) pelo NOME.
A quinta fala de que so' o trecho entra (a da D117, de 10/11) e' a primeira que e', ao mesmo tempo, «so' o trecho» e «fora do recibo»: no contrato o nome dela leva o sufixo « (D65: citado pelo sha256 do arquivo inteiro)»,
o filtro pelo nome nao a tirava e a checagem dava falso (medido: 23 falas no recibo, 24 no contrato depois do filtro; a que sobrava era ela). O filtro passa a comparar o nome SEM esse sufixo. Nada e' afrouxado:
toda fala do candidato continua tendo de estar no recibo (por sha256) OU ser uma das FALAS_FORA_DO_RECIBO, com prefixo de sha256 no delta. Idempotente; backup de BYTES; temporario + os.replace; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); p = os.path.join(HERE, "p00_precondicoes_v410.py"); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
A = 'for v_ in CM["cunhagens"].values() if v_.get("nome") not in DL.FALAS_FORA_DO_RECIBO}'
N = 'for v_ in CM["cunhagens"].values() if str(v_.get("nome") or "").split(" (D65:")[0] not in DL.FALAS_FORA_DO_RECIBO}'
if N in t:
    print("ja' feito:", hashlib.sha256(b0).hexdigest()[:16])
else:
    assert t.count(A) == 1, t.count(A)
    t1 = t.replace(A, N); ast.parse(t1); b1 = t1.encode("utf-8")   # (o p00 e' CRLF: a troca nao tem quebra de linha e o texto foi decodificado dos BYTES, logo o fim de linha de cada linha fica como estava)
    assert b1.count(b"\r\n") == b0.count(b"\r\n") and b1.count(b"\n") == b0.count(b"\n"), "o fim de linha do p00 mudou"
    bak = p + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_r6c17"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
    open(p + ".tmp_r6c", "wb").write(b1); assert os.path.getsize(p + ".tmp_r6c") == len(b1) > len(b0); os.replace(p + ".tmp_r6c", p); assert open(p, "rb").read() == b1
    print("p00_precondicoes_v410.py: %s -> %s | backup %s" % (hashlib.sha256(b0).hexdigest()[:16], hashlib.sha256(b1).hexdigest()[:16], os.path.basename(bak)))

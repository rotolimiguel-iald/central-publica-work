# -*- coding: utf-8 -*-
"""_adapt_harness_fechar_pino_v407.py -- harness_fechar_sandbox_v407.py: a opcao `--pino-emulado` (SO' para a parte do FECHAR; a fila da memoria exige o pino REAL). Enquanto a gerencia nao rodar pino_memoria_py_v407.py (ato dela: escreve PINO_MEMORIA_PY_v407.json na raiz do pacote),
o harness recusa (rc 4) a parte do fechar; com `--pino-emulado` o sandbox ganha um pino calculado NA HORA do memoria.py real (so' leitura) e o resumo DIZ que o pino foi emulado. Nada e' escrito na raiz do pacote."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adaptar_pos_rito_v407 as M

NOME = "harness_fechar_sandbox_v407.py"
t, crlf, raw = M.le(NOME)
if "_emulado_pelo_harness" in t:
    print("JA' FEITO"); sys.exit(0)
t = M.sub(t, '"PINOS_BN_v407.json", "PINO_MEMORIA_PY_v407.json", "kernel_modulos_novos_v407.json"', '"PINOS_BN_v407.json", "kernel_modulos_novos_v407.json"')
BLOCO = r'''if os.path.exists(os.path.join(PKG, "PINO_MEMORIA_PY_v407.json")):
    shutil.copyfile(os.path.join(PKG, "PINO_MEMORIA_PY_v407.json"), os.path.join(PKS, "PINO_MEMORIA_PY_v407.json"))
elif "--pino-emulado" in sys.argv:    # a gerencia ainda NAO rodou pino_memoria_py_v407.py: o pino do sandbox e' calculado NA HORA do memoria.py real (so' leitura); nada e' escrito na raiz do pacote
    _mb = open(os.path.join(MEM_REAL, "fila", "memoria.py"), "rb").read(); _hm = sha(_mb)
    open(os.path.join(PKS, "PINO_MEMORIA_PY_v407.json"), "w", encoding="utf-8").write(json.dumps({"contrato": "PINO_MEMORIA_PY_v407", "path": os.path.join(MEM_REAL, "fila", "memoria.py"), "sha256": _hm, "sha16": _hm[:16], "bytes": len(_mb), "_emulado_pelo_harness": "PINO EMULADO: pino_memoria_py_v407.py ainda nao foi rodado pela gerencia; calculado na hora do memoria.py real (so' leitura)"}, indent=1))
    R["pino_emulado"] = True
else:
    recusa("o pacote da v407 nao tem PINO_MEMORIA_PY_v407.json (a gerencia roda pino_memoria_py_v407.py; ou use --pino-emulado SO' para a parte do fechar)")
'''
t = M.sub(t, 'for kn_ in ("KERNEL_RECIBO_v407.json", "FLAGS_v407.json"):\n', BLOCO + 'for kn_ in ("KERNEL_RECIBO_v407.json", "FLAGS_v407.json"):\n')
t = M.sub(t, 'R["nao_exigiu_refazer"] = NAO_REFAZER\n', 'R["nao_exigiu_refazer"] = NAO_REFAZER\nif R.get("pino_emulado"):\n    R["veredito"] += " [PINO EMULADO: PINO_MEMORIA_PY_v407.json nao existia na raiz do pacote; so\' o fechar rodou com um pino calculado na hora do memoria.py real]"\n')
M.grava(NOME, t, crlf, raw)

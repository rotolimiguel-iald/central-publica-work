# -*- coding: utf-8 -*-
"""_fix_b1_b2_b3_parte2_v410.py -- tres correcoes apontadas pelos Sonnets A e B antes da cadeia (parte 2, D86/D87):
B1  runtime_v410.py, c1 do iald2: o contrato da IALD2 traz as ancoras por modulo SO' da IALD2 (1) e o bundle tem 2 modulos; a checagem comparava len(por_mod_) com bundle.n (recusaria no ensaio);
B2  delta_v410.py, FRASE_D81_EN: o estatuto (validity, not creditation) na MESMA frase de PROVED (o portao do G1 parte a frase em ; e :);
B3  gerar_esperados_v410.py: alias a_escala em registros_funcao_v410 (a leitura do pos-rito le a chave curta a_escala; o conferir_rito le aescala).
Backup de BYTES; temporario -> conferir tamanho -> substituir; ast.parse."""
import ast, hashlib, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); TS = time.strftime("%Y%m%d_%H%M%S")


def aplicar(nome, trocas):
    p = os.path.join(HERE, nome); b0 = open(p, "rb").read(); t = b0.decode("utf-8")
    open(p + ".bak_" + TS + "_pre_b123", "wb").write(b0)
    for a, b in trocas:
        c = t.count(a); assert c == 1, (nome, c, a[:140]); t = t.replace(a, b)
    nb = t.encode("utf-8"); ast.parse(nb)
    open(p + ".tmp", "wb").write(nb); assert os.path.getsize(p + ".tmp") == len(nb); os.replace(p + ".tmp", p)
    print(nome, len(b0), "->", len(nb), "| sha16", hashlib.sha256(nb).hexdigest()[:16])


aplicar("runtime_v410.py", [(
    'and len(por_mod_) == c_["bundle"]["n"] == len(c_["source_sha256"]) and all(por_mod_.values())},',
    'and len(por_mod_) == len(c_["ancoras_por_modulo"]) >= 1 and set(por_mod_) <= set(c_["source_sha256"]) and len(c_["source_sha256"]) == c_["bundle"]["n"] and all(por_mod_.values())},   # (parte 2: o bundle tem dois modulos; as ancoras DESTE registro sao so\' as da IALD2, as da AEscala sao do a_escala_v410)')])
aplicar("delta_v410.py", [(
    'FRASE_D81_EN = "P = nP of Turing (the machine with the reader; the classes of computation) PROVED in the kernel (uma_leitura_decide_SAT, a_maquina_com_o_leitor, p_igual_np_no_modo_selecao): validity, not creditation; the standard Turing machine without the reader (the Clay) stays outside by statute"',
    'FRASE_D81_EN = "P = nP of Turing (the machine with the reader; the classes of computation) PROVED as validity, not creditation, in the kernel (uma_leitura_decide_SAT, a_maquina_com_o_leitor, p_igual_np_no_modo_selecao); the standard Turing machine without the reader (the Clay) stays outside by statute"')])
aplicar("gerar_esperados_v410.py", [(
    '_rf10a = esp["registros_funcao_v410"]["aescala"]\n',
    '_rf10a = esp["registros_funcao_v410"]["aescala"]\nesp["registros_funcao_v410"]["a_escala"] = esp["registros_funcao_v410"]["aescala"]   # (parte 2: a leitura do pos-rito le a chave curta a_escala; o conferir_rito le aescala; o MESMO registro nas duas chaves)\n')])
sys.path.insert(0, HERE)
import delta_v410 as DL
import re
_partes = re.split(r"(?<=[.;:!?])\s+|\n", DL.FRASE_D81_EN)
_ruins = [x for x in _partes if re.search(r"PROVADA|PROVED|provada|proved", x) and not re.search(r"validade|validity|≠|creditação|creditacao|accreditation|creditation|judgement|nature", x)]
assert not _ruins, _ruins
print("B2 ok: nenhuma frase com PROVED sem o estatuto |", len(_partes), "frases")

# -*- coding: utf-8 -*-
"""Registro das TENTATIVAS da rodada 2 do construtor otico (F1.FREQUENCIA, trilha POSTO).

So leitura dos arquivos de 2_OPTICO/tentativas e do resultado final; grava TENTATIVAS_RODADA2.json em 2_OPTICO.
Os hashes sao calculados aqui (sha256 dos bytes); os vereditos de cada tentativa sao lidos dos JSONs preservados,
nunca afirmados de memoria.
"""
import hashlib
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
TENT = os.path.join(AQUI, "tentativas")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def le(p):
    return json.load(open(p, encoding="utf-8"))


TENTATIVAS = [
    dict(n=1, resultado="RESULTADO_OPTICO.json.20261012_194523", log="LOG_OPTICO.txt.20261012_194523",
         conferencia="CONFERENCIA_FREEZE.json.20261012_194456", script=None, stdout="stdout_tentativa1_20261012_1943.txt",
         mudanca_para_a_seguinte=("(a) np.seterr(divide, invalid, over = 'raise'): operacao numpy que gere NaN/Inf passa a PARAR o ensaio; "
                                  "(b) guarda de NaN em Parte.check (NaN num numero do check -> SEM_VEREDITO); (c) no ANEXO X2, "
                                  "e^{-gamma t} abaixo do menor float (t = 1e3) dava 0/0 = NaN, que o max() do Python descartava "
                                  "em silencio (RuntimeWarning no stdout da tentativa 1): agora y = 0 exige zero exato; (d) rotulos "
                                  "do log de P2.a; (e) a nota de C3 deixou de inferir 'posto 4' de P_F (fica so o traco citado do core). "
                                  "Nenhuma parte pre-registrada, tolerancia, mapeamento ou esperado mudou; o X2 e anexo."),
         nota_script=("o fonte da tentativa 1 foi editado no lugar (nao preservado em bytes); o sha256 dele esta registrado "
                      "no proprio RESULTADO da tentativa 1 (auto_auditoria_do_fonte.fonte.sha256)")),
    dict(n=2, resultado="RESULTADO_OPTICO.json.20261012_194700", log="LOG_OPTICO.txt.20261012_194700",
         conferencia="CONFERENCIA_FREEZE.json.20261012_194635", script="run_optico.py.tentativa2_20261012_194457",
         stdout="stdout_tentativa2_20261012_1945.txt",
         mudanca_para_a_seguinte=("a auto-auditoria reportava as palavras vigiadas pela regua usando as proprias palavras como chaves "
                                  "do JSON; passaram a rotulos neutros, e o RESULTADO serializado passou a ser varrido tambem. "
                                  "Nada mais mudou.")),
    dict(n=3, resultado="RESULTADO_OPTICO.json.20261012_194949", log="LOG_OPTICO.txt.20261012_194949",
         conferencia="CONFERENCIA_FREEZE.json.20261012_194922", script="run_optico.py.tentativa3_20261012_194634",
         stdout="stdout_tentativa3_20261012_1946.txt",
         mudanca_para_a_seguinte=("(a) rotulo neutro w1 sem a palavra portuguesa; (b) P3.a passou do pareamento por indice (805 pares) "
                                  "ao PRODUTO COMPLETO P x rho por n (60502 pares) -- leitura mais fiel e mais exigente de "
                                  "'P em {...}, rho em {...}', adotada depois de ver que a rodada 1 usara o produto completo; "
                                  "(c) decisao registrada: TOL_ID em matrizes = maximo entrada a entrada; (d) comparacao de "
                                  "vereditos com a rodada 1 dentro do RESULTADO. Tolerancias, mapeamento e esperados intactos.")),
    dict(n=4, resultado="RESULTADO_OPTICO.json.20261012_195401", log="LOG_OPTICO.txt.20261012_195401",
         conferencia="CONFERENCIA_FREEZE.json.20261012_195335", script="run_optico.py.tentativa4_20261012_194922",
         stdout="stdout_tentativa4_20261012_1949.txt",
         mudanca_para_a_seguinte=("so o ANEXO: A1 passou a citar as consultas do cetico aferidor (kernel do Nos e inventario da "
                                  "bancada, consultas_mapa/k_inventario_kernel.json; mapa o03), com os numeros LIDOS dos arquivos; "
                                  "entraram A9 ({Q_th, rho*} so tem homonimos no kernel) e A10 (Matrix.rank: 0 no kernel). "
                                  "Nenhuma parte, tolerancia, mapeamento ou esperado mudou.")),
    dict(n=5, resultado=None, log=None, conferencia=None, script=None, stdout="stdout_tentativa5_20261012_1953_FINAL.txt",
         mudanca_para_a_seguinte="(final) os arquivos de topo de 2_OPTICO sao os desta tentativa"),
]
FINAL = 5


def main():
    out = dict(documento="TENTATIVAS da rodada 2 do construtor otico (F1.FREQUENCIA, trilha POSTO)",
               quando_local=time.strftime("%Y-%m-%d %H:%M:%S"),
               regra="preservar tentativas; correcao ao lado; nenhuma tentativa apagada", tentativas=[])
    faces = {}
    for t in TENTATIVAS:
        reg = dict(n=t["n"], mudanca_para_a_seguinte=t["mudanca_para_a_seguinte"])
        if t["n"] < FINAL:
            pr = os.path.join(TENT, t["resultado"])
            d = le(pr)
            faces[t["n"]] = d["resumo"]["face_O"]
            reg.update(resultado=dict(arquivo=pr, bytes=os.path.getsize(pr), sha256=sha(pr)),
                       log=dict(arquivo=os.path.join(TENT, t["log"]), sha256=sha(os.path.join(TENT, t["log"]))),
                       conferencia_freeze=dict(arquivo=os.path.join(TENT, t["conferencia"]), sha256=sha(os.path.join(TENT, t["conferencia"]))),
                       fonte_sha256_registrado_no_resultado=d["auto_auditoria_do_fonte"]["fonte"]["sha256"],
                       controles_ok=d["controles_ok"], nao_conformes=d["resumo"]["nao_conformes"])
            if t["script"]:
                ps = os.path.join(TENT, t["script"])
                reg["script"] = dict(arquivo=ps, bytes=os.path.getsize(ps), sha256=sha(ps),
                                     confere_com_o_registrado=(sha(ps) == d["auto_auditoria_do_fonte"]["fonte"]["sha256"]))
            else:
                reg["script"] = dict(nota=t.get("nota_script"))
        else:
            pr = os.path.join(AQUI, "RESULTADO_OPTICO.json")
            d = le(pr)
            faces[FINAL] = d["resumo"]["face_O"]
            ps = os.path.join(AQUI, "run_optico.py")
            reg.update(resultado=dict(arquivo=pr, bytes=os.path.getsize(pr), sha256=sha(pr)),
                       log=dict(arquivo=os.path.join(AQUI, "LOG_OPTICO.txt"), sha256=sha(os.path.join(AQUI, "LOG_OPTICO.txt"))),
                       conferencia_freeze=dict(arquivo=os.path.join(AQUI, "CONFERENCIA_FREEZE.json"),
                                               sha256=sha(os.path.join(AQUI, "CONFERENCIA_FREEZE.json"))),
                       script=dict(arquivo=ps, bytes=os.path.getsize(ps), sha256=sha(ps),
                                   confere_com_o_registrado=(sha(ps) == d["auto_auditoria_do_fonte"]["fonte"]["sha256"])),
                       controles_ok=d["controles_ok"], nao_conformes=d["resumo"]["nao_conformes"])
        if t["stdout"]:
            po = os.path.join(TENT, t["stdout"])
            reg["stdout"] = dict(arquivo=po, sha256=sha(po))
        out["tentativas"].append(reg)
    base = faces[FINAL]
    out["vereditos_face_O_iguais_em_todas_as_tentativas"] = all(faces[k] == base for k in faces)
    out["diferencas_por_tentativa"] = {str(k): [p for p in base if faces[k].get(p) != base[p]] for k in faces}
    txt = json.dumps(out, ensure_ascii=False, indent=1)
    dest = os.path.join(AQUI, "TENTATIVAS_RODADA2.json")
    tmp = dest + ".tmp"
    open(tmp, "w", encoding="utf-8").write(txt)
    if os.path.getsize(tmp) <= 0:
        print("FALHA VISIVEL: arquivo vazio", file=sys.stderr)
        return 2
    os.replace(tmp, dest)
    print(json.dumps(dict(vereditos_iguais=out["vereditos_face_O_iguais_em_todas_as_tentativas"],
                          diferencas=out["diferencas_por_tentativa"],
                          scripts_conferem=[r.get("script", {}).get("confere_com_o_registrado") for r in out["tentativas"]]),
                     ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

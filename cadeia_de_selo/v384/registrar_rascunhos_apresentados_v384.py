# -*- coding: utf-8 -*-
"""O REGISTRO DOS RASCUNHOS (11a verificacao, defeito 3): os rascunhos do pre-registro, por versao, com os sha256 e o gerado_utc lidos dos arquivos -- num
arquivo que o rascunho NAO cita por hash (registra-lo nas disposicoes mudaria o rascunho: seria circular). Tambem o que aconteceu DEPOIS da gravacao da 11a e
antes da apresentacao: a primeira execucao do teste do congelamento sobre a v13 FALHOU no caso C2 por limite do PROPRIO teste (a copia minima do pacote levava
so as afericoes 2 a 9, e a 10 ficou obrigatoria -- o gerador recusou com razao); o teste foi ampliado pela ferramenta Edit (diff guardado) e passou 8 de 8.
So acrescimo: uma entrada nova por execucao; nunca sobrescreve uma anterior."""
import glob, hashlib, json, os, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
OUT = os.path.join(HERE, "registro_rascunhos_apresentados_v384.json")
R = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"o_que_e": __doc__.strip().splitlines()[0], "entradas": []}
vers = {}
for d in sorted(glob.glob(os.path.join(HERE, "rascunho_prereg_v*")), key=lambda x: int(x.rsplit("_v", 1)[1])):
    nm = os.path.basename(d); arq = {}
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f); e = {"sha256": h(p), "bytes": os.path.getsize(p)}
        if f.endswith(".json") and "RASCUNHO" in f:
            j = json.load(open(p, encoding="utf-8")); e.update({"gerado_utc": j.get("gerado_utc"), "spec_sha256": j.get("spec_sha256")})
        arq[f] = e
    vers[nm] = arq
TC = os.path.join(HERE, "teste_congelamento_v384.json"); TO = os.path.join(HERE, "teste_orfaos_v384.json")
ent = {"quando": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "versoes": vers,
       "apresentada_ao_operador": "rascunho_prereg_v13 (as anteriores: intermediarias ou superadas pelas afericoes 8 a 11)",
       "gerador_corrente": h(os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "gerar_preregistro_pilar_quantico_03out.py")),
       "disposicoes_citadas_pela_v13": h(os.path.join(HERE, "disposicoes_afericoes_v384.json")), "aferidor_citado_pela_v13": h(os.path.join(HERE, "AFERIDOR_v384.txt")),
       "depois_da_11a": {"teste_congelamento_primeira_execucao_v13": "FALHOU no caso C2: a copia minima do pacote do PROPRIO teste levava so as afericoes 2 a 9; a 10 ficou obrigatoria e o gerador recusou (com razao)",
                         "correcao": "teste ampliado (range(2, 20)) pela ferramenta Edit; diff em afer11/diff_teste_congelamento_afer11_pela_ferramenta_Edit.txt",
                         "diff_sha256": h(os.path.join(HERE, "afer11", "diff_teste_congelamento_afer11_pela_ferramenta_Edit.txt")),
                         "teste_congelamento": {"sha256": h(TC), "casos": {k: v["passou"] for k, v in json.load(open(TC, encoding="utf-8")).items()}},
                         "teste_orfaos": {"sha256": h(TO), "casos": {k: v["passou"] for k, v in json.load(open(TO, encoding="utf-8")).items()}},
                         "candidato_ENSAIO": json.load(open(os.path.join(HERE, "CANDIDATO_v384_ENSAIO.json"), encoding="utf-8"))["sha16"],
                         "artigo_simulado": os.path.join("teste_artigo_afer3", "simular.json") + " sha256 " + h(os.path.join(HERE, "teste_artigo_afer3", "simular.json"))[:16]}}
R["entradas"].append(ent)
b = json.dumps(R, ensure_ascii=False, indent=1).encode("utf-8")
if os.path.exists(OUT):
    raw = open(OUT, "rb").read(); bak = OUT + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
open(OUT + ".tmp", "wb").write(b); assert os.path.getsize(OUT + ".tmp") == len(b); os.replace(OUT + ".tmp", OUT); assert open(OUT, "rb").read() == b
print("registro:", h(OUT)[:16], "| versoes:", list(vers)); print(json.dumps({k: {f: (e["sha256"][:16], e.get("gerado_utc")) for f, e in v.items() if "RASCUNHO" in f} for k, v in vers.items() if k == "rascunho_prereg_v13"}, ensure_ascii=False, indent=1))

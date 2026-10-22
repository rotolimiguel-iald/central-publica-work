# -*- coding: utf-8 -*-
"""Registro no MAPA DE ROTAS: a RATIFICACAO do operador e o V1 CONGELADO (ancorado fora dele mesmo, pelos sha256 calculados pela ferramenta), a conferencia
independente do congelamento, e a cadeia ate o rito (candidato instalavel, fumaca, ensaio a seco, esperados, instalacao). Numeros LIDOS dos artefatos."""
import glob, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
QUEM = "Claude Opus 5.5 -- gerencia, sessao 6da8f00d (Central de Patentes)"
P = lambda *a: os.path.join(HERE, *a)
PERM = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out")
V1 = json.load(open(os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json"), encoding="utf-8")); RAT = V1["ratificacao_do_operador"]
CC = json.load(open(P("conferir_congelamento_v384_resultado.json"), encoding="utf-8"))["result"]
CM = json.load(open(P("CANDIDATO_v384.json"), encoding="utf-8"))
EN = json.load(open(P("ensaio_a_seco_v384.json"), encoding="utf-8"))
AP = sorted(glob.glob(P("APLICADO_AO_CANONICO_*.json")))[-1]; APJ = json.load(open(AP, encoding="utf-8"))
FU = sorted(glob.glob(P("fumaca_v384_*", "result.json")))[-1]; FUJ = json.load(open(FU, encoding="utf-8"))
REG = [
    {"tipo": "RESULTADO", "rota_id": "quantica.pilar_v384_rascunhos_b_reduzido_e_a", "dominio": "QUANTICA", "titulo": "RATIFICADO pelo operador: B_AMPLIADO_D64; o V1 congelado",
     "pergunta": "qual especificacao o operador ratifica?", "dados": ["a mensagem do operador no transcrito (verbatim no V1)"],
     "metodo": "o gerador do pre-registro na pasta permanente, contra o rascunho v13 apresentado (comparacao canonica; so os campos volateis diferem)",
     "resultado": "escolha %s; quando %s; especificacao %s; V1 json/md na pasta permanente (so leitura); %d evidencias copiadas" % (RAT["escolha"], RAT["quando"], V1["spec_sha256"][:16], len(V1["evidencias"])),
     "veredito": "PREREGISTRATION_V1_FROZEN_BY_HASH_%s_RATIFIED_BY_THE_OPERATOR" % V1["spec_sha256"][:16].upper(), "estatuto": "INPUT", "status": "EXAMINADA", "olhou_dados": False,
     "defeito": "", "nao_refazer": "o V1 congelado nao se refaz; uma versao nova e' V1.x com gerador novo e nova ratificacao", "proximo_passo": "o rito v384 (lancado)",
     "onde": PERM, "artefatos": [os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json"), os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.md"),
                                 os.path.join(PERM, "gerar_preregistro_pilar_quantico_03out.py")], "refs": ["quantica.pilar_v384_verificacao_11a"],
     "nota": "verbatim do operador gravado no V1 (ratificacao_do_operador.verbatim); a guarda e' lexical, a conferencia final e' a leitura humana"},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_conferencia_do_congelamento", "dominio": "QUANTICA", "titulo": "a conferencia independente do congelamento do V1",
     "pergunta": "o V1 congelado e' o rascunho apresentado + a ratificacao verbatim, com as evidencias intactas?", "dados": ["o V1, o rascunho v13, o transcrito, as evidencias"],
     "metodo": "dois conferidores independentes (V1 x rascunho; ratificacao e evidencias), por script",
     "resultado": "; ".join("%s: %s (%d conferencias, %d defeitos BAIXO)" % (L["lente"], L["resultado"]["veredito"], len(L["resultado"]["conferencias"]), len(L["resultado"]["defeitos"])) for L in CC["lentes"]),
     "veredito": "CONGELAMENTO_CONFERE", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "", "nao_refazer": "conferido", "proximo_passo": "",
     "onde": "scratchpad v384", "artefatos": [P("conferir_congelamento_v384_resultado.json")], "refs": ["quantica.pilar_v384_rascunhos_b_reduzido_e_a"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_cadeia_ate_o_rito", "dominio": "QUANTICA", "titulo": "a cadeia ate o rito: candidato instalavel, fumaca, ensaio a seco, esperados, instalacao",
     "pergunta": "o candidato instalavel roda o caminho inteiro antes do rito?", "dados": ["a fumaca (especificacao propria, contagens minimas; NUNCA resultado do pilar)"],
     "metodo": "gerar_candidato (nao-ensaio), fumaca_v384, ensaio_a_seco_v384, gerar_esperados_v384, instalar_v384",
     "resultado": "candidato %s (%d patches); fumaca: %s; ensaio: %s (candidato %s); instalado %s sobre a v383 %s" % (
         CM["sha16"], len(CM["patches"]), str(FUJ.get("verdict"))[:60] + "...", EN["veredito"], EN["sha16"], APJ["um_py_novo"]["sha16"], APJ["backups"]["um.py"]["sha16"]),
     "veredito": "CADEIA_ATE_O_RITO_COMPLETA", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "", "nao_refazer": "", "proximo_passo": "o rito e o conferidor",
     "onde": "scratchpad v384 + Nos", "artefatos": [P("CANDIDATO_v384.json"), FU, P("ensaio_a_seco_v384.json"), P("ESPERADOS_v384.json"), AP], "refs": ["quantica.pilar_v384_rascunhos_b_reduzido_e_a"]},
]
os.makedirs(P("rotas_congelamento"), exist_ok=True)
for i, r in enumerate(REG):
    f = P("rotas_congelamento", "%02d_%s.json" % (i, r["rota_id"])); json.dump(r, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    o = subprocess.run([sys.executable, R, "registrar", f, "--quem", QUEM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r["rota_id"], "rc", o.returncode)

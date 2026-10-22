# -*- coding: utf-8 -*-
"""Registro no MAPA DE ROTAS: as afericoes 9a, 10a e 11a do pilar quantico da v384, o teste dos orfaos e os rascunhos v13 (RESULTADO da rota dos rascunhos).
Numeros LIDOS dos artefatos; o sha256 dos artefatos e' calculado pela ferramenta."""
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
QUEM = "Claude Opus 5.5 -- gerencia, sessao 6da8f00d (Central de Patentes)"
P = lambda *a: os.path.join(HERE, *a)
D = json.load(open(P("disposicoes_afericoes_v384.json"), encoding="utf-8"))
TO = json.load(open(P("teste_orfaos_v384.json"), encoding="utf-8"))
RB = json.load(open(P("rascunho_prereg_v13", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_REDUZIDO.json"), encoding="utf-8"))
RA = json.load(open(P("rascunho_prereg_v13", "PREREGISTRO_PILAR_QUANTICO_20261003_V1_RASCUNHO_B_AMPLIADO_D64.json"), encoding="utf-8"))


def pas(n):
    x = D["passada%d" % n]
    return "%d entradas %s; %d novos, %d sobreviventes, severidades %s" % (x["n_entradas"], json.dumps(x["entradas"]), x["novos"], x["sobreviventes"], json.dumps(x["severidades_ajustadas"]))


REG = [
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_9a_passada", "dominio": "QUANTICA", "titulo": "a 9a afericao: as correcoes da 8a (so achados BAIXO)",
     "pergunta": "as correcoes da 8a fecham?", "dados": ["o codigo do pilar"], "metodo": "aferidores por lente + cacador de regressoes + verificador adversarial",
     "resultado": pas(9), "veredito": "AFERICAO_9A_TRATADA", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "defeito": "a gravacao da 9a omitiu uma ressalva (a condicao leu saida truncada) -- errata ao lado", "nao_refazer": "registrado verbatim (AFERIDOR_v384.txt)",
     "proximo_passo": "a 10a", "onde": "scratchpad v384", "artefatos": [P("afericao9_resultado.json")], "refs": ["quantica.pilar_v384_afericao_8a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_afericao_10a_passada", "dominio": "QUANTICA", "titulo": "a 10a afericao (estreita): as correcoes da 9a; uma regressao BAIXA",
     "pergunta": "as correcoes da 9a fecham? o que toca o rascunho?", "dados": ["o codigo do pilar"], "metodo": "dois aferidores + verificador adversarial; cada achado marcado se toca o rascunho",
     "resultado": pas(10) + "; %d tocavam o rascunho" % D["passada10"]["tocam_o_rascunho"], "veredito": "AFERICAO_10A_TRATADA", "estatuto": "REAL", "status": "EXAMINADA",
     "olhou_dados": False, "defeito": "", "nao_refazer": "registrado verbatim", "proximo_passo": "a 11a (verificacao das frases alteradas)", "onde": "scratchpad v384",
     "artefatos": [P("afericao10_resultado.json")], "refs": ["quantica.pilar_v384_afericao_9a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_verificacao_11a", "dominio": "QUANTICA", "titulo": "a 11a verificacao (estreita): as frases que mudaram do rascunho v11 ao v12",
     "pergunta": "cada frase alterada do rascunho bate com o codigo e com os numeros?", "dados": ["os rascunhos v11 e v12; o lancador; as sondas"],
     "metodo": "um verificador independente; recalculo por script; tabela de cada exit do lancador", "resultado": "tudo o que mudou confere; %d defeitos BAIXO (dois de redacao no rascunho, dois de registro), tratados na v13" % len(D["passada11"]["defeitos"]),
     "veredito": "VERIFICACAO_11A_TRATADA", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False, "defeito": "", "nao_refazer": "registrado",
     "proximo_passo": "apresentar a v13 ao operador", "onde": "scratchpad v384", "artefatos": [P("aferidor11", "resultado_aferidor11.json")], "refs": ["quantica.pilar_v384_afericao_10a_passada"]},
    {"tipo": "ROTA", "rota_id": "quantica.pilar_v384_teste_dos_orfaos", "dominio": "QUANTICA", "titulo": "os orfaos de uma tentativa interrompida do congelamento (MD e pasta de evidencias sem o JSON)",
     "pergunta": "uma tentativa interrompida trava o congelamento, ou os orfaos vao para o lado sem perda?", "dados": ["copia do transcrito real com mensagem SINTETICA"],
     "metodo": "O1 (JSON apagado, pasta adulterada), O2 e O3 (JSON presente)", "resultado": "; ".join("%s %s" % (k, "PASSOU" if v["passou"] else "FALHOU") for k, v in TO.items())
     + "; O2 e O3 recusados pela guarda do V1 ja existente -- a guarda nova das evidencias com o V1 IGUAL foi exercitada pela 10a com relogio fixo",
     "veredito": "TESTE_DOS_ORFAOS_%d_DE_%d" % (sum(1 for v in TO.values() if v["passou"]), len(TO)), "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
     "defeito": "", "nao_refazer": "", "proximo_passo": "", "onde": "teste_orfaos_v384.py", "artefatos": [P("teste_orfaos_v384.py"), P("teste_orfaos_v384.json")], "refs": ["quantica.pilar_v384_teste_do_congelamento"]},
    {"tipo": "RESULTADO", "rota_id": "quantica.pilar_v384_rascunhos_b_reduzido_e_a", "dominio": "QUANTICA", "titulo": "os rascunhos v13 levados ao operador",
     "pergunta": "qual especificacao o operador ratifica?", "dados": ["sonda de tempo teste_tempo_v9", "autoteste teste_motor_v8"], "metodo": "o gerador do pre-registro; nenhum operador da teoria calculado",
     "resultado": "B_REDUZIDO spec %s, %.1f min (%.1f com a margem); B_AMPLIADO_D64 spec %s, %.1f min (%.1f com a margem)" % (
         RB["spec_sha256"][:16], RB["orcamento_estimado"]["total_min"], RB["orcamento_estimado"]["total_com_margem_min"], RA["spec_sha256"][:16],
         RA["orcamento_estimado"]["total_min"], RA["orcamento_estimado"]["total_com_margem_min"]),
     "veredito": "RASCUNHOS_V13_AGUARDAM_A_RATIFICACAO_DO_OPERADOR", "estatuto": "INPUT", "status": "EM_CURSO", "olhou_dados": False, "defeito": "", "nao_refazer": "",
     "proximo_passo": "a mensagem do operador nomeando «b reduzido» ou «b ampliado»; entao o congelamento do V1 com --rascunho=<o JSON v13 da escolha>",
     "onde": "rascunho_prereg_v13/ e registro_rascunhos_apresentados_v384.json", "artefatos": [P("rascunho_prereg_v13", f) for f in sorted(os.listdir(P("rascunho_prereg_v13")))] + [P("registro_rascunhos_apresentados_v384.json")],
     "refs": ["quantica.pilar_v384_verificacao_11a"]},
]
os.makedirs(P("rotas_afer11"), exist_ok=True)
for i, r in enumerate(REG):
    f = P("rotas_afer11", "%02d_%s.json" % (i, r["rota_id"])); json.dump(r, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    o = subprocess.run([sys.executable, R, "registrar", f, "--quem", QUEM], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r["rota_id"], "rc", o.returncode)

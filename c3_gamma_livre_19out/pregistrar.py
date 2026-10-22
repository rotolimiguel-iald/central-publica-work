#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Escreve PREREGISTRO.json: fixa por sha256, ANTES de qualquer rodada da grade, o observavel, a grade, as
sementes, o metodo do estado estacionario, os controles, os criterios e os scripts. Confere por grep que
rodar.py nao contem calibracao de gamma nem constante da teoria. Recusa-se a rodar se o pre-registro ja existe
ou se existe qualquer dado cru da grade.
"""
import os
import re
import sys
import json
import time
import hashlib

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import rodar  # noqa: E402
import veredito  # noqa: E402

SRC = r"C:\IALD\projetos_pyhton\acom\TGL_C3_validator_v52.py"
FEV_JSON = r"C:\IALD\projetos_pyhton\acom\tgl_c3_v5_results_20260209_121836.json"

PADROES_PROIBIDOS = [
    r"find_gamma_star", r"brentq", r"alpha", r"beta", r"CCI_TARGET", r"SQRT_E", r"THETA_MIGUEL",
    r"0\.0120", r"0\.98796", r"1\.2031", r"sqrt\(\s*e\s*\)", r"np\.e\b", r"math\.e\b",
]
PALAVRA_PROIBIDA = "con" + "firm"      # radical da palavra proibida da regua (montado para nao aparecer escrito)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    with open(p, "rb") as f:
        return sha(f.read())


def canon(o):
    return json.dumps(o, sort_keys=True, separators=(',', ':'), ensure_ascii=True)


def grep_count(path, padroes):
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    return {p: len(re.findall(p, txt, flags=re.IGNORECASE)) for p in padroes}


def main():
    alvo = os.path.join(HERE, "PREREGISTRO.json")
    if os.path.exists(alvo):
        raise SystemExit("PREREGISTRO.json ja existe: nao se re-pre-registra.")
    for dado in ("dados_crus_main.csv", "dados_crus_N2.csv", "manifesto_dados.json", "veredito.json"):
        if os.path.exists(os.path.join(HERE, dado)):
            raise SystemExit("ja existe %s: o pre-registro tem de vir ANTES dos dados." % dado)

    g_rodar = grep_count(os.path.join(HERE, "rodar.py"), PADROES_PROIBIDOS)
    g_ver = grep_count(os.path.join(HERE, "veredito.py"), PADROES_PROIBIDOS)
    if sum(g_rodar.values()) != 0:
        raise SystemExit("rodar.py contem padrao proibido: %s" % g_rodar)
    palavra = {fn: grep_count(os.path.join(HERE, fn), [PALAVRA_PROIBIDA])[PALAVRA_PROIBIDA]
               for fn in ("rodar.py", "veredito.py", "pregistrar.py")}
    if sum(palavra.values()) != 0:
        raise SystemExit("palavra proibida da regua encontrada: %s" % palavra)

    comps = rodar.spec()
    comps["criterios"] = veredito.REGRAS
    comps_sha = {k: sha(canon(v).encode("utf-8")) for k, v in comps.items()}

    arquivos = ["rodar.py", "veredito.py", "pregistrar.py", "teste_veredito_sintetico.py",
                "verifica_fidelidade.py", "piloto_numerico.py", "teste_encanamento.py"]
    arq_sha = {a: sha_file(os.path.join(HERE, a)) for a in arquivos}
    saidas_previas = {s: sha_file(os.path.join(HERE, s)) for s in
                      ("teste_veredito_sintetico_saida.txt", "verifica_fidelidade_saida.txt", "piloto_numerico_saida.txt",
                       "teste_encanamento_saida.txt")}
    nomeados = {
        "observavel_O": comps_sha["observavel_O"],
        "grade": comps_sha["grade"],
        "sementes": sha(canon(rodar.SEEDS).encode("utf-8")),
        "gammas": sha(canon([repr(float(g)) for g in rodar.GAMMAS]).encode("utf-8")),
        "configs": sha(canon([list(c) for c in rodar.CONFIGS]).encode("utf-8")),
        "estado_estacionario": comps_sha["estado_estacionario"],
        "controles_N1_N2_N3": comps_sha["controles"],
        "criterios_P_e_veredito": comps_sha["criterios"],
    }

    with open(FEV_JSON, encoding="utf-8") as f:
        fev = json.load(f)
    vals = sorted(r["M7_d_folds_c3"] for r in fev["per_dim_results"])

    pre = {
        "id": "c3_gamma_livre_19out",
        "titulo": "C3 GAMMA LIVRE: o piso das dobras D_folds(c3) do estado estacionario GKLS e uma OITAVA (ln 2)?",
        "pre_registrado_em": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "pre_registrado_por": "subagente Claude Sonnet 5.5 a mando da gerencia c1 (teste pre-registrado de 19/10/2026)",
        "estatuto": "[REAL no modelo simulado]; a leitura 'consciencia' e [ONTO] e nao entra no veredito",
        "pergunta": "Com o parametro de fuga gamma LIVRE (varrido em logspace(-4,0,25)) e sem calibracao, o observavel "
                    "O = D_folds(c3) do estado estacionario GKLS das 9 configuracoes do validador v52 fica numa janela "
                    "de gamma de >= 1 decada em ln 2 +- 0,05 para TODAS as configs, e independente de ln(d/nc) "
                    "(|inclinacao| < 0,05)?",
        "rotas_anteriores_lidas_e_nao_refeitas": [
            "quantica.c3_validator_calibrado (seq 296): o validador calibra gamma* para o peso do core dar 1 - beta: circular; "
            "proximo passo nomeado: rodar com gamma livre",
            "quantica.dobras_c3_hierarquia_e_matematica (seq 307): a hierarquia c1 > c2 > c3 > 0 e matematica; "
            "o que pode falhar sao os VALORES com gamma livre",
        ],
        "fonte_somente_leitura": {
            "script": SRC, "sha256": sha_file(SRC),
            "rodada_de_fevereiro_json": FEV_JSON, "rodada_de_fevereiro_sha256": sha_file(FEV_JSON),
            "valores_de_fevereiro_d_folds_c3_no_gamma_calibrado": {
                "mediana": vals[len(vals) // 2], "media": sum(vals) / len(vals), "ln2": rodar.LN2,
                "por_config_na_ordem_da_fonte": [r["M7_d_folds_c3"] for r in fev["per_dim_results"]]},
        },
        "componentes": comps,
        "componentes_sha256": comps_sha,
        "hashes_nomeados_sha256": nomeados,
        "arquivos_sha256": arq_sha,
        "saidas_das_verificacoes_previas_sha256": saidas_previas,
        "verificacoes_previas_sem_olhar_a_pergunta": [
            "teste_veredito_sintetico.py: 19 casos sinteticos cobrindo cada ramo, as bordas da banda, da inclinacao, "
            "da janela (7 pontos) e do minimo de sementes: todos passaram",
            "verifica_fidelidade.py: copia da fonte identica byte a byte (sistema e superoperador), observavel identico "
            "em 200 estados sinteticos, nucleo por SVD igual ao autovetor nulo da fonte fora da grade (sementes 7 e 8)",
            "piloto_numerico.py: qualidade numerica do nucleo em sementes fora da grade (7 e 8); nenhum O impresso",
            "teste_encanamento.py: leitura/escrita de rodar.py e veredito.py num sistema de brinquedo (d = 6 e 8, "
            "sementes 1 e 2, 3 gammas), subpasta encanamento_teste: nao e a grade",
        ],
        "proibicoes_conferidas_por_grep": {
            "padroes_sem_diferenca_de_maiuscula": PADROES_PROIBIDOS,
            "ocorrencias_em_rodar_py": g_rodar, "ocorrencias_em_veredito_py": g_ver,
            "palavra_proibida_da_regua": {"padrao": "radical da palavra proibida da regua (montado no script)",
                                          "ocorrencias": palavra},
            "leitura": "a rodada NAO calibra gamma, NAO busca raiz, NAO usa peso-alvo do core nem constante da teoria",
        },
        "regras_de_completude_fixadas_antes_dos_dados": [
            "semente 'original' = 42 (padrao de build_system, a usada na rodada de fevereiro); as demais 43, 44, 45, 46",
            "janela >= 1 decada = >= 7 pontos consecutivos da grade (passo 1/6 de decada)",
            "inclinacao calculada em CADA gamma da janela (mais estrita que a inclinacao agrupada) sobre as 9 medianas",
            "celula (config, gamma) com menos de 3 sementes convergidas e invalida e quebra a janela",
            "N3 no posto d/4 so onde d e multiplo de 4 (d = 10 e 14 ficam so com d/2)",
            "regra 5 do veredito: P verdadeiro com N1 falho tambem da GENERIC_NOT_TGL (funcao total)",
            "INCONCLUSIVE se > 10% dos pontos da grade principal nao convergem; ou, com P verdadeiro, > 10% dos de N2",
        ],
        "descritivo_pos_veredito_nao_entra_no_veredito": [
            "O no gamma* de fevereiro de cada config (lido do JSON de fevereiro) com as 5 sementes, e reproducao do "
            "d_folds_c3 de fevereiro com a semente 42",
            "gamma onde a mediana de cada config cruza ln 2 (interpolacao em log gamma) e o peso do core ali",
            "inclinacao agrupada da janela, corridas so-banda e so-inclinacao",
        ],
        "ordem_de_execucao": ["python -B -u rodar.py > rodar_log.txt", "python -B veredito.py"],
    }
    pre["sha256_do_protocolo"] = sha(canon({"componentes_sha256": comps_sha,
                                            "rodar_py": arq_sha["rodar.py"],
                                            "veredito_py": arq_sha["veredito.py"]}).encode("utf-8"))

    with open(alvo, "w", encoding="utf-8") as f:
        json.dump(pre, f, indent=1, ensure_ascii=True)
    h = sha_file(alvo)
    with open(alvo + ".sha256", "w", encoding="utf-8") as f:
        f.write(h + "  PREREGISTRO.json\n")
    print("PREREGISTRO.json escrito. sha256 do arquivo:", h)
    print("sha256 do protocolo:", pre["sha256_do_protocolo"])
    print("componentes:", json.dumps(comps_sha, indent=1))
    print("arquivos:", json.dumps(arq_sha, indent=1))
    print("grep rodar.py:", g_rodar)


if __name__ == "__main__":
    main()

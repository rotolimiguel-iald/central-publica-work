# -*- coding: utf-8 -*-
"""gerar_anotacao_final_v404.py -- monta registro_mapa_v404_prep_final.json: a ANOTACAO que FECHA a preparacao da v404 na rota umpy.v404.cadeia_de_selo_preparada_28out (a ROTA foi registrada antes, seq lido do livro). Numeros e hashes LIDOS dos arquivos.
Nao registra: `rotas.py registrar <json> --quem "claude-prep-v404"`. uso: python -I -B -X utf8 gerar_anotacao_final_v404.py"""
import hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); POS = os.path.join(HERE, "pos_rito")
rj = lambda p: json.load(open(p, encoding="utf-8"))
CM = rj(os.path.join(HERE, "CANDIDATO_v404.json")); PC = rj(os.path.join(HERE, "PRECONDICOES_v404.json")); HT = rj(os.path.join(POS, "HARNESS_TEXTOS_ENSAIO_v404.json")); HF = rj(os.path.join(POS, "HARNESS_FECHAR_SANDBOX_v404.json"))
refazer = open(os.path.join(HERE, "refazer_out_v404.txt"), encoding="utf-8", errors="replace").read()
assert "== FIM" in refazer and HT["tudo_passou"] is True and HF["tudo_passou"] is True and not HT.get("nao_exigiu_refazer") and not HF.get("nao_exigiu_refazer"), "os harnesses ou o refazer nao fecharam: a anotacao final nao diz isto"
livro = [json.loads(l) for l in open(r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl", encoding="utf-8") if l.strip()]
seq_rota = [r["seq"] for r in livro if r.get("rota_id") == "umpy.v404.cadeia_de_selo_preparada_28out" and r.get("tipo") == "ROTA"]
assert len(seq_rota) == 1, seq_rota
ok = sum(1 for c in PC["checagens"] if c["ok"]); n = len(PC["checagens"]); falhas = [c["checagem"][:80] for c in PC["checagens"] if not c["ok"]]
n_neg_l = len(HT["etapas"]["leitura_negativos"]["controles"]); n_neg_p = len(HT["etapas"]["paragrafo_v404_e_citacoes"]["negativos"]); n_neg_f = len(HF["etapas"]["fechar_negativos"])
A = lambda *p: os.path.join(HERE, *p)
art = [A("RELATORIO_PREPARACAO_v404.md"), A("PLANO_v404.md"), A("PRECONDICOES_v404.json"), A("ESPERADOS_v404.json"), A("PINOS_BN_v404.json"), A("refazer_out_v404.txt"), os.path.join(POS, "HARNESS_TEXTOS_ENSAIO_v404.json"), os.path.join(POS, "HARNESS_FECHAR_SANDBOX_v404.json"),
       os.path.join(POS, "textos_v404_novo.pysnip"), os.path.join(POS, "leitura_v404.py"), A("bancada_B3_servico", "CONFERENCIA_EXIGENCIAS_SERVICO_v404.json")]
reg = [{"tipo": "ANOTACAO", "rota_id": "umpy.v404.cadeia_de_selo_preparada_28out", "estatuto": "REAL", "olhou_dados": False,
        "titulo": "v404 PREPARADA — fechamento da preparação: o pós-rito (leitura, textos, fechar, mapa, serviço da Bancada) foi escrito e testado em harness; o candidato regenera byte a byte; p00 %d/%d (a única falha é o tamanho do MEMORY.md, decisão da gerência)" % (ok, n),
        "resultado": "refazer_candidato_v404.sh --regerar terminou (== FIM) e o candidato %s saiu IGUAL byte a byte (duas gerações); harness_textos_ensaio_v404 (sem --nao-exigir-refazer): TUDO PASSOU, com %d controles negativos da leitura e %d do parágrafo novo; harness_fechar_sandbox_v404: TUDO PASSOU, com %d controles negativos do fechar; "
                     "p00 %d/%d (falha: %s). Escritos à mão e testados: pos_rito/textos_v404_novo.pysnip (+ montar_textos_v404.py), leitura_v404.py, fechar_v404.py, registrar_mapa_v404.py, os harnesses e bancada_B3_servico/ (derivado; conferidor estático 27/27 e controle negativo que pega as 3 mutações). Nada instalado; rito não rodado; Nós, MEMORY.md e MEMORY_2.md intocados." % (
                         CM["sha16"], n_neg_l, n_neg_p, n_neg_f, ok, n, "; ".join(falhas) if falhas else "nenhuma"),
        "proximo_passo": "gerência: ler RELATORIO_PREPARACAO_v404.md; decidir o MEMORY.md; revisão independente (não afirmada); instalar_v404.py → rito_v404.sh → chain_pos_rito_v404.sh; depois registrar_mapa_v404.py (monta, a gerência registra) e a custódia.",
        "defeito": "quem constrói não aprova; as contagens e os hashes deste registro são lidos dos arquivos, mas a leitura/textos/fechar adaptados à mão só foram exercitados contra o Nós EMULADO do ensaio a seco, não contra um rito real",
        "refs": ["kernel.projecao_transversal_da_meia_nat.sen45_derivado_28out", "kernel.jo8v32.triplo_inteiro_28out"], "nota": "anotação ao lado da ROTA seq %d; correção ao lado, nada reescrito; NOT_FALSIFIED não é a palavra da creditação; o gate não se move." % seq_rota[0],
        "artefatos": [p for p in art if os.path.isfile(p)]}]
out = os.path.join(HERE, "registro_mapa_v404_prep_final.json")
open(out, "w", encoding="utf-8", newline="\n").write(json.dumps(reg, ensure_ascii=False, indent=1))
print(out)

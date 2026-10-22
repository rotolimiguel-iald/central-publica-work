# -*- coding: utf-8 -*-
"""Gera os dois registros do mapa (ROTA e RESULTADO) -- so arquivos; o registro no livro e ato da gerencia."""
import json
from pathlib import Path
D = Path(r"C:/IALD/Central de Patentes/work/umpy_sorry_check_13out")
W = str(D) + chr(92)
arts = [W + n for n in ("RELATORIO_SORRY_CHECK.md", "PROPOSTA_V392.md", "controles_extraidos.json", "deteccoes_tokenize.json",
                        "cobertura_varredura_lexical.json", "contagem_formatos_logs.json", "probe_sorryterm_saida.txt",
                        "extrair_controles.py", "varrer_deteccoes.py", "varrer_kernel.py", "contar_logs.py", "ler_probe_sorry.py")]
for a in arts:
    assert Path(a).exists(), a
base = {"rota_id": "umpy.v392.deteccao_de_sorry", "dominio": "FORMAL", "olhou_dados": False,
        "onde": "um.py v391 8e7b9927ceae64b8, prove_bench_lean_controls (def l.192886; decisao l.192945)",
        "refs": ["infra.bancada_um.sincronizacao_vnnn", "kernel.auditoria.cobertura_axiomas_73_modulos", "umpy.v388.exame_completo_codigo_e_artigo", "umpy.v391.estatuto_da_prova"]}
rota = dict(base, **{
    "tipo": "ROTA",
    "titulo": "A deteccao de sorry dos controles Lean POSITIVOS da bancada no um.py v391 le o aviso no formato antigo (aspas simples)",
    "pergunta": "A barreira 'sem sorry' de prove_bench_lean_controls pega um sorry real do Lean 4.31? Ha outra barreira no caminho? O kernel principal depende dela? Algum positivo embutido tem sorry?",
    "dados": ["um.py v391 8e7b9927ceae64b8 (so leitura; literais por ast.literal_eval, corpus zlib e arquivo v361 LZMA decodificados em memoria)",
              "um_absoluto.json a74241ff380b1b0e e um_absoluto_selo.json 95061f18c7102248 (rodada v391, 2026-10-07 19:08:57)",
              "Nos/bancada_corpus (13.207 arquivos) e fonte do Lean 4.31.0 (Lean/AddDecl.lean 27e607f8f611260e)"],
    "metodo": "leitura da funcao e dos consumidores; tokenize de todas as strings com 'sorry' no um.py (83) e classificacao; extracao dos 167 controles com sha256 conferido e busca de sorry/admit/sorryAx sem comentarios; contagem dos dois formatos no corpus; leitura do probe SorryTerm embutido; cobertura da varredura lexical do kernel; sem rodar um.py, Lean ou selo",
    "estatuto": "REAL", "status": "EXAMINADA",
    "nota": "investigacao cetica c1 por ordem da gerencia; nada no Nos, um.py, quadro, mapa ou memoria foi escrito; o registro no livro e ato da gerencia",
})
res = dict(base, **{
    "tipo": "RESULTADO",
    "titulo": "Detector cego ao formato do Lean 4.31, latente: 0 sorry nos 52 positivos; o kernel decide por #print axioms e e imune",
    "resultado": ("l.192945: sorry = \"declaration uses 'sorry'\" in out; o Lean 4.31 emite 'declaration uses `sorry`' (AddDecl.lean l.75/79; probe SorryTerm embutido; "
                  "bancada_corpus 65 com crase, 0 com aspas; 38 em .log, nao 64). Nenhuma outra barreira no caminho (sem leitura de #print axioms, sem lexico, sem olean pinado). "
                  "167/167 controles com sha256 conferido; 0 tokens sorry/admit/sorryAx em 52 positivos e 115 negativos (nem em comentarios). Core: 52/52 positivos ok, sorry false; "
                  "entra na kernel_condition da coincidencia conjunta V3 (l.193196, l.193366), nao no gate nem no selo (grep 0). Kernel: sorryAx_absent True, 10265 entradas sem sorryAx, escada 6163/6163, "
                  "decidido por #print axioms (l.134846, l.134864+, l.142090): imune. Varredura lexical nao recursiva: 150 .lean de TGLExt/O16 fora; recursiva da 0 tokens."),
    "veredito": "UMPY_V391_BENCH_POSITIVE_SORRY_CHECK_BLIND_TO_LEAN_4_31_FORMAT__LATENT__ZERO_SORRY_IN_52_POSITIVES_BY_SOURCE__KERNEL_IMMUNE_BY_PRINT_AXIOMS__GATE_UNTOUCHED",
    "estatuto": "REAL", "status": "EXAMINADA_COM_DEFEITO",
    "defeito": "a barreira 'sem sorry' dos positivos (l.192945) nunca dispara com o Lean 4.31; o check 'positivos compilam sem erro e sem sorry' (l.192969) afirma o que o instrumento nao mede; sem efeito na v391",
    "nao_refazer": "o formato do aviso esta medido em tres fontes; os 167 controles estao lidos; o kernel nao depende da string",
    "proximo_passo": "v392: regex [`'\u2018]sorry + leitura de sorryAx/axiomas fora do trio no out (PROPOSTA_V392.md A); collectAxioms em todo positivo (B, compilar no sandbox antes); autoteste com a fixture SorryTerm.stdout embutida (C); errata ao lado do paragrafo v362",
    "artefatos": arts,
})
(D / "registro_rota_umpy_sorry.json").write_text(json.dumps(rota | {"artefatos": arts[:2] + arts[7:]}, ensure_ascii=False, indent=1), encoding="utf-8")
(D / "registro_mapa_umpy_sorry.json").write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok")

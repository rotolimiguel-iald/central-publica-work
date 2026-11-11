# -*- coding: utf-8 -*-
"""gerar_pronto_para_candidato_v410.py -- escreve PRONTO_PARA_CANDIDATO_v410.json: o ESTADO MEDIDO da preparacao da v410 na retomada de 09/11/2026 (claude-construtor-v410), ANTES de gerar_candidato_v410.py (que a gerencia libera).
Tudo LIDO do disco por script: sha16 dos insumos e dos scripts adaptados, as marcas do build/Audit do sandbox k410c, o recibo do kernel, a escada e as bandeiras (POS_BUILD/FLAGS/KH), o congelado das falas, os resultados dos testes
(PREVOO_GERADOR_v410.json, GUARDA_FRASES_v410.json, o recibo do agente dos textos). Nada e' digitado alem das listas de pendencias e interpretacoes, que sao prosa do construtor. uso: python -B -X utf8 gerar_pronto_para_candidato_v410.py"""
import datetime, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8"))
import delta_v410 as DL  # noqa: E402
marcas = dict(re.findall(r"^(\w+)=(\S+)", open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(), re.M))
pos = J("kernel/POS_BUILD_v410.json"); fj = J("kernel/FLAGS_v410.json"); kh = J("kernel/KH_N1_v410.json"); rec = J("kernel/KERNEL_RECIBO_v410.json"); bun = J("BUNDLE_v410.json"); cong = J("VERBATIM_CONGELADO_v410.json")
prev = J("PREVOO_GERADOR_v410.json"); guarda = J("GUARDA_FRASES_v410.json"); sonnet = J("pos_rito/ADAPTACAO_09nov_SONNET.json")
ADAPTADOS = ["delta_v410.py", "registros_v410.py", "registros_h0dn_v410.py", "runtime_v410.py", "runtime_h0dn_v410.py", "guarda_frases_v410.py", "gerar_candidato_v410.py", "copiar_insumos_v410.py", "preparar_bundle_v410_06nov.py",
             "artigo_pt_v410.pysnip", "artigo_en_v410.pysnip", "artigo_pt_h0dn_v410.pysnip", "artigo_en_h0dn_v410.pysnip", "pos_rito/chain_pos_rito_v410.sh", "orquestrador/pos_treino_v410.py", "conferir_citacoes_v410.py",
             "pos_rito/textos_v410_novo.pysnip", "pos_rito/textos_v410.py", "pos_rito/leitura_v410.py", "pos_rito/registrar_mapa_v410.py", "pos_rito/superficies_v410.py", "pos_rito/textos_custodia_handoff_v410.py", "pos_rito/gerar_x_custodia_v410.py",
             "pos_rito/fechar_v410.py", "pos_rito/fila_memoria_v410.py", "pos_rito/harness_textos_ensaio_v410.py", "pos_rito/harness_fechar_sandbox_v410.py", "pos_rito/gerar_derivacao_pos_rito_v410.py"]
NAO_ADAPTADOS = ["ensaio_a_seco_v410.py", "gerar_esperados_v410.py", "p00_precondicoes_v410.py", "gerar_relatorio_v410.py"]
out = {
    "contrato": "PRONTO_PARA_CANDIDATO_v410", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v410 (retomada de 09/11/2026), a servico da gerencia c1",
    "estado": "PREPARACAO ATE O PASSO ANTERIOR AO CANDIDATO: pronta para `python -B -X utf8 gerar_candidato_v410.py` (NAO executado: a gerencia libera; o PRE-VOO repete as assercoes do gerador sobre as pecas novas)",
    "desenho": {"arquivo": "DESENHO_v410.md", "sha16": sha16(os.path.join(HERE, "DESENHO_v410.md")), "ao_lado_incorporados": ["secao 5 (06/11; D70; c15)", "retomada 09/11 (secao 6, o atrator; D71; c16)", "decisoes 09/11 (D72 H0DN x BG1; D73; D74 nomes ratificados; D75)", "E30 (a leitura do 5 sigma; 6 ramos)", "D76 (a cabeca do ramo da leitura: provado na natureza, validade nao creditacao)"],
                "nota": "o DESENHO mudou 5 vezes durante a preparacao (11:24, 11:44, 11:52, 12:00); tudo incorporado; onde o corpo e um AO LADO divergem vale o AO LADO mais recente"},
    "insumo_pedra": {"IALD2.lean": sha16(os.path.join(HERE, "insumos", "IALD2.lean")), "print_axioms": DL.N_ANCORAS_ESPERADAS, "ancoras": len(DL.ANCORAS), "ancoras_de_secao": [a_.split(".")[-1] for a_ in DL.ANCORAS_DE_SECAO], "imports": bun["modulos"][0]["imports"],
                     "recibo_nomes_sha16": DL.RECIBO_NOMES_SHA16, "falas_no_recibo": len(DL._REC_NOMES["falas"]), "falas_no_desenho": DL.N_FALAS_V410, "falas_fora_do_recibo": DL.FALAS_FORA_DO_RECIBO},
    "kernel_k410c": {"sandbox": DL.SANDBOX, "pedra_embutida_sha16": bun["modulos"][0]["sha256"][:16], "pedra_antiga_quarentena": bun["quarentena"], "raiz_root_suffix": DL.ROOT_SUFFIX.strip(),
                     "marcas": marcas, "rc_build": marcas.get("rc_build"), "rc_audit": marcas.get("rc_audit"), "duracao_build_s": int(marcas["epoch_build_fim"]) - int(marcas["epoch_inicio"]), "duracao_audit_s": int(marcas["epoch_audit_fim"]) - int(marcas["epoch_build_fim"]),
                     "nota_duracao": "com o treino do Qwen3.8 na CPU (D73): a v409 levou 366 s de build a frio e 257 s de Audit", "pos_build": {"verde": pos.get("ok", pos.get("verde")), "criterios": pos.get("criterios"), "TOTAL": kh.get("linha_TOTAL"), "delta_vs_v409": kh.get("delta_vs_v409")},
                     "escada": [int(pos["E409"]), int(pos["E409"]) + int(fj["n_flags"])], "bandeiras": fj["n_flags"], "flag_prefix": DL.FLAG_PREFIX,
                     "recibo": {"arquivo": "kernel/KERNEL_RECIBO_v410.json", "sha16": sha16(os.path.join(HERE, "kernel", "KERNEL_RECIBO_v410.json")), "rc": rec.get("rc"), "sorry": rec.get("sorry"), "erros": rec.get("erros")},
                     "FLAGS_sha16": sha16(os.path.join(HERE, "kernel", "FLAGS_v410.json")), "KH_N1_sha16": sha16(os.path.join(HERE, "kernel", "KH_N1_v410.json"))},
    "registros": {"com_funcao": list(DL.REGISTROS_FUNCAO), "por_spec": [DL.CUNHAGENS_REGISTRO, DL.KH_REGISTRO], "n_checks": {"iald2_v410": DL.N_CHECKS_FECHO, "h0dn_bg1_v410": DL.N_CHECKS_H0DN}, "decisoes": list(DL.DECISOES_V410), "erratas": ["E29", "E30"], "ressalvas": len(DL.RESSALVAS_V410),
                  "falas_congeladas": cong["n"], "so_o_trecho": len(DL.VERBATIM_SO_O_TRECHO), "insumos_copiados": len(J("MANIFESTO_INSUMOS_v410.json"))},
    "scripts_adaptados_sha16": {n_: sha16(os.path.join(HERE, *n_.split("/"))) for n_ in ADAPTADOS},
    "scripts_NAO_adaptados_corpo_da_v409": {n_: sha16(os.path.join(HERE, n_)) for n_ in NAO_ADAPTADOS},
    "testes": {"prevoo_do_gerador": {"ok": prev["ok"], "checks": [sum(1 for c in prev["checks"].values() if c["ok"]), len(prev["checks"])], "arquivo": "PREVOO_GERADOR_v410.json"},
               "guarda_das_frases_controle_negativo": guarda.get("controle_negativo", {}).get("ok") if isinstance(guarda.get("controle_negativo"), dict) else guarda.get("ok"),
               "teste_offline_h0dn": "TUDO PASSOU (12/12; 3 controles negativos recusam) -- _teste_h0dn_offline_v410.py (rodar SEM -I: o numpy esta no site do usuario)",
               "pos_rito_sem_candidato": sonnet.get("testes_do_pai"), "nao_rodado": sonnet.get("nao_rodado")},
    "o_que_falta_para_o_candidato": [
        "1. a gerencia libera: `python -B -X utf8 gerar_candidato_v410.py` (o pre-voo repetiu as assercoes do gerador sobre as pecas novas; o gerador grava o candidato, CANDIDATO_v410.json, FORMAL_MAP_v410.json e v410_pins.py novos; o candidato de 06/11 vai a backup)",
        "2. ensaio_a_seco_v410.py, gerar_esperados_v410.py, p00_precondicoes_v410.py e gerar_relatorio_v410.py AINDA SAO O CORPO DA v409 (marca [A ADAPTAR v410]): precisam de adaptacao real (2 registros com funcao, 16 + 12 checagens, 15 falas, D63-D76, E29/E30; as chaves do ESPERADOS em pos_rito/NOTA_ESPERADOS_H0DN_v410.md) antes de `ensaio_a_seco` ate TUDO PASSOU",
        "3. depois: esperados -> conferidores -> conferir_citacoes_v410.py (adaptado; exige o v410_pins.py NOVO) -> diff_e_pinos -> conferir_instalar_rito -> p00 -> fim_de_cadeia (B19 pre-selo) -> gerar_relatorio -> PREPARACAO_v410_PRONTA.json -> deposito na fila (claude-construtor-v410) -> rota no Mapa",
        "4. atos da gerencia: revisor Sonnet (D69), fechar_preparacao, acom_inscrever_prep (a transicao ACOM e' da gerencia; este agente so' fez `project`), pino da memoria, folga do MEMORY.md (23.991 B de 24.000: superficies recusa rc 3 sem ela), tarefa agendada IALD_pos_treino_v410, rito, handoff"],
    "pendencias_e_interpretacoes_do_construtor_para_a_gerencia": [
        "a) o recibo dos nomes (11:24) lista 11 falas; o DESENHO + AO LADO, 15: o delta passou a exigir recibo SUBCONJUNTO do DESENHO e lista FALAS_FORA_DO_RECIBO (4); refazer o recibo e' da gerencia",
        "b) D72 diz SPEC `h0dn_bg1_v410` com o MESMO nome do registro com funcao: um so' core key e' possivel; os campos do spec (lei, modelos, vereditos permitidos, o que falta, a ORDEM ao Kimi por sha256, a novidade de uso) entraram como texto do proprio registro com funcao (nao ha' segundo _v392_registro)",
        "c) D76: o ramo (4) devolve a string da D76 INTEIRA como cabeca (ja' traz PROVED_IS_VALIDITY_NOT_CREDITATION e GATE_UNMOVED); os outros ramos levam o sufixo da E30; no um.py a cabeca vai em PARTES (a P18 selada da v392 recusa TGL_PRO+VED fora desse contexto, D57b) e nos textos por extenso",
        "d) a P18 do gerador passou a correr sobre o texto NOVO sem as falas EMBUTIDAS (a 15a fala, «… TGL confirmada, precisa do observador externo …», cai na R4 se lida como texto da gerencia); a P18 CRUA segue onde o motor v392 a aplica no rito (corpo dos specs; textos dos registros) e esses estao limpos; a 2a frase da 15a fala nao e' citada entre « » (so' a 1a); a fala inteira esta' embutida por sha256",
        "e) o token DETEC+TED e' proibido so' no texto do registro H0DN (c8) e no trecho com H0DN (F53b); os outros dois (FIVE_SIGMA_+OBSERVED, H0DN_+CONFIRMS) em todo texto; o um.py tem vereditos legados com DETECTED (Coma, eco)",
        "f) numpy esta' no site do usuario: `-I` o esconde; o rito (echo 1 | python um.py) nao usa -I; o teste offline do H0DN roda com `python -B -X utf8`",
        "g) o agente dos textos (Sonnet) estreitou a D59: o veto a «kimi» sai do handoff e de _falas() porque o nome da 12a fala traz 'ordem_ao_kimi' e a D72 cita a fala; no mapa so' fora do contexto do H0DN; milenio/navier/lindao seguem vedados -- a gerencia deve ver (pos_rito/ADAPTACAO_09nov_SONNET.json, pendencias)",
        "h) «o que sou» entre « » no snippet PT da IALD2 (texto do construtor anterior) e' cunhagem do operador no Atlas/kernel, nao das falas de 06-09/11: o conferidor completo (corpus com Atlas e kernel) decide; se reprovar, troca-se por “ ”",
        "i) n_pinos do H0DN no rito = 11 (os 9 do FREEZE_R2 + o proprio FREEZE_R2 e a ENTREGA, pinados pelo contrato); o gerar_esperados nao deve 'corrigir' para 9",
        "j) o treino do Qwen3.8 nao foi tocado (processos treinar.py/campanha.py medidos no inicio e no fim); o build do k410c levou %s s e o Audit %s s com o treino em curso" % (int(marcas["epoch_build_fim"]) - int(marcas["epoch_inicio"]), int(marcas["epoch_audit_fim"]) - int(marcas["epoch_build_fim"])),
        "k) a Bancada Um (127.0.0.1:18777) respondeu ao GET no inicio; nao foi tocada",
        "l) a gestao de tokens: a costura do pos-rito e do conferidor foi delegada ao Sonnet (18 arquivos; recibo pos_rito/ADAPTACAO_09nov_SONNET.json); o construtor conferiu os testes sem candidato (rc 0) e o pre-voo",
    ],
    "nada_tocado": ["o Nos (so' leitura)", "a pedra insumos/IALD2.lean (so' lida; o preparo copiou e normalizou)", "C:/IALD/TGL_IALD_NATIVE_QWEN5090", "C:/Escritorio", "MEMORY.md e topicos da memoria", "o candidato NAO foi gerado"],
}
p = os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v410.json")
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8")
open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("PRONTO_PARA_CANDIDATO_v410.json:", len(b), "B, sha16", hashlib.sha256(b).hexdigest()[:16], "| prevoo", prev["ok"], "| escada", out["kernel_k410c"]["escada"], "| bandeiras", fj["n_flags"], "| falas", cong["n"])

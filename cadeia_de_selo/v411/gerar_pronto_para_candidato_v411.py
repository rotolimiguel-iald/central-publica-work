# -*- coding: utf-8 -*-
# [AUTORAL v411, 12/11/2026, claude-construtor-v411, a servico da gerencia c1] REESCRITO para a v411 (o corpo da v410 subido por rotulo fica no .bak_*_corpo_v410_bump e em bump\)
"""gerar_pronto_para_candidato_v411.py -- escreve PRONTO_PARA_CANDIDATO_v411.json: o ESTADO MEDIDO da preparacao da v411 no fim da Etapa 1 (claude-construtor-v411), ANTES de gerar_candidato_v411.py (que exige o
TOPO_RATIFICADO_v411.json, da gerencia). Tudo LIDO do disco por script: sha16 dos insumos e dos scripts, as marcas do build/Audit do sandbox k411c, o recibo do kernel, a escada e as declaracoes, os resultados dos ensaios
(TESTE_H0DN_OFFLINE, GUARDA_FRASES, TESTE_QUADRO, PREVOO_GERADOR, PRECONDICOES, conferir_citacoes, GUARDA_MATERIAL_PRIVADO), a lista dos arquivos ainda com a marca de copia mecanica. As listas de pendencias e as interpretacoes
sao prosa do construtor. uso: python -B -X utf8 gerar_pronto_para_candidato_v411.py"""
import datetime, glob, hashlib, json, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v411 as DL  # noqa: E402
s16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
J = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8")) if os.path.exists(os.path.join(HERE, p)) else None
marcas = dict(re.findall(r"^(\w+)=(\S+)", open(os.path.join(HERE, "kernel", "construir_marcas.txt"), encoding="utf-8").read(), re.M))
POS = J("kernel/POS_BUILD_v411.json"); REC = J("kernel/KERNEL_RECIBO_v411.json"); KH = J("kernel/KH_N1_v411.json"); TO = J("TESTE_H0DN_OFFLINE_v411.json"); GFJ = J("GUARDA_FRASES_v411.json")
TQ = J("TESTE_QUADRO_v411.json"); PV = J("PREVOO_GERADOR_v411.json"); P0 = J("PRECONDICOES_v411.json"); CC = J("conferir_citacoes_v411.json"); GMP = J("GUARDA_MATERIAL_PRIVADO_v411.json"); MI = J("MANIFESTO_INSUMOS_v411.json")
AUTORAIS = ["delta_v411.py", "registros_h0dn_v411.py", "runtime_h0dn_v411.py", "quadro_v411.py", "registros_v411.py", "guarda_frases_v411.py", "guarda_material_privado_v411.py", "gerar_candidato_v411.py", "p00_precondicoes_v411.py",
            "conferir_citacoes_v411.py", "copiar_insumos_v411.py", "copiar_base_v411.py", "copiar_k411c.sh", "construir_kernel_v411.sh", "conferir_fontes_k410c_vs_nos_v411.py", "pos_build_kernel_v411.py", "base_um_v410.py",
            "acom_init_construtor_v411.py", "_mk_motor_v411.py", "derivar_v411_motor.py", "_bump_copia_v411.py", "_marca_adaptado_v411.py", "_fix_aspas_v411.py", "_teste_h0dn_offline_v411.py", "_teste_quadro_v411.py",
            "gerar_pronto_para_candidato_v411.py", "acom_conferencias_v411.py", "guarda_p18_v411.py", "kernel/refazer_audit_v411.sh"]
_marca = "[A ADAPTAR v" + "411]"
MARCADOS = sorted(os.path.relpath(p_, HERE) for p_ in glob.glob(os.path.join(HERE, "**", "*"), recursive=True) if os.path.isfile(p_) and ".bak_" not in p_ and os.sep + "bump" + os.sep not in p_
                  and not p_.endswith((".json", ".txt", ".diff", ".log", ".npz", ".lean", ".md")) and os.path.basename(p_) not in ("_bump_copia_v411.py", "p00_precondicoes_v411.py") and _marca in open(p_, "rb").read().decode("utf-8", "replace"))
out = {
    "contrato": "PRONTO_PARA_CANDIDATO_v411", "quando": datetime.datetime.now().isoformat(timespec="seconds"), "agente": "claude-construtor-v411, a servico da gerencia c1",
    "estado": ("ETAPA 1 CONCLUIDA ate onde ela alcanca: tudo o que vem antes do candidato que nao depende do texto ratificado do topo; o candidato NAO foi gerado (TOPO_RATIFICADO_v411.json ausente: a Etapa 2 nao comecou, por regra); "
               "o PRE-VOO do gerador rodou todas as assercoes com a PROPOSTA do topo (DESENHO 5.1 b) e nao gravou candidato"),
    "topo_ratificado_presente": os.path.exists(DL.TOPO_RATIFICADO_ARQ),
    "desenho": {"arquivo": "DESENHO_v411.md", "sha16": DL.DESENHO_SHA16, "lido_por_script": ["a tabela dos 18 insumos (sha16 conferidos contra os arquivos)", "os 7 citados", "as 9 falas e os 5 textos da gerencia", "as 16 checagens (o texto de cada uma vira a descricao)",
                                                                       "o veredito de maquina (prefixo, meio, sufixo, recusa)", "D159 a D170, E41, E42", "o resumo do que o teste nao decide", "os rotulos das sete ressalvas", "os titulos e as frases do topo e da secao (5.1, 5.2)", "a tabela da secao 7"]},
    "kernel_k411c": {"sandbox": DL.SANDBOX, "origem": DL.SANDBOX_ORIGEM, "copia": "robocopy SEM /PURGE (copiar_k411c.sh); fontes conferidas por sha256 contra o Nos v410 ANTES e DEPOIS da copia (CONFERENCIA_FONTES_K410C/K411C_v411.json: 1764 comuns, 0 diferentes)",
                     "marcas": marcas, "duracao_build_s": POS["duracao_build_s"], "duracao_audit_s": POS["duracao_audit_s"], "n_modulos_compilados": POS["n_modulos_compilados"], "n_replayed": POS["n_replayed"],
                     "linha_TOTAL": POS["linha_TOTAL"], "audit_log_sha256": POS["audit_log_sha256"], "audit_log_igual_ao_da_v410": POS["audit_log_sha256"] == POS["audit_log_sha256_v410"], "escada": POS["escada"], "n_bandeiras_novas": 0, "bundle": [],
                     "recibo": {"arquivo": "kernel/KERNEL_RECIBO_v411.json", "sha16": s16(os.path.join(HERE, "kernel", "KERNEL_RECIBO_v411.json")), "rc": REC["rc"], "sorry": REC["sorry"], "erros": REC["erros"]},
                     "POS_BUILD_sha16": s16(os.path.join(HERE, "kernel", "POS_BUILD_v411.json")), "KH_N1_sha16": s16(os.path.join(HERE, "kernel", "KH_N1_v411.json")), "criterios": POS["criterios"],
                     "copias_do_kernel_fora_de_work": ["C:\\t\\k411c\\final (o sandbox)", "C:\\t\\k411c\\arvore_simulada_h8 (a arvore simulada do h8, do pre-voo do gerador)"]},
    "registro_h0dn_bg1_v411": {"n_checks": DL.N_CHECKS_FECHO, "offline": {"TUDO_PASSOU": TO["TUDO_PASSOU"], "n_ok": TO["n_ok"], "veredito": TO["veredito"], "c6_max_dif": TO["c6_max_dif"], "c9_max_dif": TO["c9_max_dif"],
                                                                              "primario": {k_: TO["primario"][k_] for k_ in ("z_null", "z_tgl", "D", "p_unilateral", "ramo", "outcome")}, "cefeidas_livres": {k_: TO["cefeidas_livres"][k_] for k_ in ("z_null", "z_tgl", "D", "ramo", "outcome")},
                                                                              "controles_negativos": {k_: (v_.get("recusou"), v_.get("falhas")) for k_, v_ in TO["controles_negativos"].items() if k_ != "guarda_de_frases_controle"},
                                                                              "arquivo": "TESTE_H0DN_OFFLINE_v411.json", "sha16": s16(os.path.join(HERE, "TESTE_H0DN_OFFLINE_v411.json"))},
                               "insumos_embutidos": {i_["nome"]: {"sha16": i_["sha256"][:16], "bytes": i_["bytes"], "reuso_v410": i_["reuso_v410"]} for i_ in DL.INSUMOS_V411}, "citados_nao_embutidos": {c_["nome"]: c_["sha256"][:16] for c_ in DL.CITADOS_V411},
                               "b64_bytes": PV["h0dn"]["bytes_embutidos_b64"], "contratos_de_registro_fora_da_escada": list(DL.CONTRATOS_DE_REGISTRO_FORA_DA_ESCADA)},
    "pre_voo_do_gerador": {"arquivo": "PREVOO_GERADOR_v411.json", "sha16_do_texto_que_seria_gerado_com_a_PROPOSTA": PV["sha16"], "bytes": PV["bytes"], "delta_bytes": PV["delta_bytes"], "n_patches": PV["n_patches"], "patches": [p_["id"] for p_ in PV["patches"]],
                           "h8_igual_ao_pino_da_v410": PV["h8"]["igual_ao_pino_da_v410"], "guardas_no_texto_renderizado": PV["guarda_frases"]["violacoes_no_texto_renderizado"], "topo_guarda_da_proposta": PV["topo_guarda"], "topo_p18_da_proposta": PV["topo_p18"],
                           "nota": "o sha16 acima NAO e' o do candidato: e' o do texto que o gerador montaria com a PROPOSTA do topo; o candidato depende do texto ratificado"},
    "guardas": {"frases_v411": {"controle_negativo": GFJ["controle_negativo"]["ok"], "n_proibidas": GFJ["n_proibidas"], "regras_superadas_da_v410": GFJ["regras_superadas_da_v410"]},
                "quadro_e_secao_renderizados": TQ["TUDO_PASSOU"], "material_privado": {"limpo": GMP["limpo"], "n_arquivos": GMP["n_arquivos"], "n_marcadores_privados": GMP["n_marcadores_privados"]},
                "citacoes": {"ok": CC["ok"], "nao_conferidos_corpo_da_v410_a_adaptar": len(CC["nao_conferidos_corpo_da_v410_a_adaptar"])}},
    "p00": {"veredito": P0["veredito"], "n_ok": P0["n_ok"], "n_falhas": P0["n_falhas"], "n_pendentes": P0["n_pendentes"], "falhas": [c_["checagem"] for c_ in P0["checagens"] if c_.get("ok") is False], "pendentes": [p_["checagem"] for p_ in P0["pendentes"]]},
    "insumos_copiados": MI["n"], "verbatim_congelado_sha16": s16(os.path.join(HERE, "VERBATIM_CONGELADO_v411.json")),
    "scripts_autorais_ou_adaptados_sha16": {a_: s16(os.path.join(HERE, a_)) for a_ in AUTORAIS if os.path.exists(os.path.join(HERE, a_))},
    "scripts_ainda_com_a_marca_A_ADAPTAR_corpo_da_v410": MARCADOS, "n_scripts_a_adaptar": len(MARCADOS),
    "tabela_secao7": [{"item": t_["item"], "nesta_versao": t_["nesta_versao"], "estado_na_etapa1": {
        "A1 (o colchete contra a regra do nome)": "FEITO: E42 ao lado (texto do contrato, spec cunhagens_v411 e ressalvas do registro)",
        "A2 (expoentes sem agrupar no TXT do artigo)": "PENDENTE (Etapa 2): mudanca no conversor para TXT; contar antes e depois no candidato",
        "as seis aberturas da seção da Escala que identificam o operador contra a regra do nome": "PENDENTE (Etapa 2): medido no um.py base, 6 trechos “na leitura do operador ela e' a ...” (4 + 2) no texto da AEscala; a troca vai no artigo regenerado, sem tocar o registro selado; o gerador ainda nao a faz",
        "a guarda de finitude do veredito do H0DN": "FEITO: c12 (o involucro recusa NaN e infinito; a funcao pinada com NaN cairia, calada, no ramo 6)",
        "o docstring do veredito": "FEITO: E41 ao lado (o modulo pinado nao e' tocado)",
        "D133 e D135 (preparação)": "FEITO: a guarda de material privado da E03 sobre todos os insumos (p00); as copias do kernel fora de work\\; nenhum .tmp; os contratos de registro fora da escada ditos; a contagem esperada de arquivos e' do handoff (Etapa 2)",
        "creditation / accreditation": "fica (como no DESENHO)", "os 8 nomes declarados pela autoria na pedra da Escala": "ficam (como no DESENHO)", "bandeiras da Escala por nome": "ficam para a versao seguinte (como no DESENHO)",
        "a pedra do observador e da escala; as doze candidatas de 11/11": "ficam para a versao seguinte (como no DESENHO)"}.get(t_["item"], "ver DESENHO")} for t_ in DL.TABELA_SECAO7],
    "o_que_falta_para_o_candidato": [
        "1. GERENCIA: gravar TOPO_RATIFICADO_v411.json (chaves pt e en, com os quatro marcadores de numero ⟨...⟩ da proposta do DESENHO 5.1 b, um de cada); depois `python -B -X utf8 gerar_candidato_v411.py` (sem --prevoo) grava o candidato, CANDIDATO_v411.json, FORMAL_MAP_v411.json e v411_pins.py",
        "2. o gerador ainda NAO faz: a troca das seis aberturas da secao da Escala no artigo (regra do nome; item da secao 7) e a medida do A2 no TXT; acrescentar como patches com ancora unica",
        "3. ADAPTAR DE VERDADE os %d scripts que ainda trazem a marca de copia mecanica (o corpo e' o da v410: IALD2, AEscala, quatro registros com funcao): os grandes sao ensaio_a_seco, gerar_esperados, conferir_rito, exame_pontos, gerar_relatorio, conferir_instalar_rito, diff_e_pinos, simular_arvore_do_nos, o orquestrador (pos_treino_v411.py: S7 e S10 ja' fora no molde) e o pos-rito inteiro (textos, leitura, superficies, textos_custodia_handoff com os blocos do README e o portao sobre o HANDOFF inteiro, registrar_mapa, fechar)" % len(MARCADOS),
        "4. depois do candidato: comparar_v410_v411 -> ensaio_a_seco ate TUDO PASSOU -> gerar_esperados -> conferidores (controle negativo e caminho positivo) -> conferir_citacoes_v411.py --candidato -> diff_e_pinos -> conferir_instalar_rito -> p00 -> fim_de_cadeia_v411.sh (B20 pre-selo) -> gerar_relatorio -> PREPARACAO_v411_PRONTA.json",
        "5. GERENCIA: revisao de terceiro, fechar_preparacao_v411.py, acom_inscrever_prep_v411.py, pino_memoria_py_v411.py e a folga do MEMORY.md, a tarefa agendada IALD_pos_treino_v411 (C:\\Python314\\pythonw.exe C:\\t\\k411c\\run_pos_treino.py), o S3, o rito, a custodia"],
    "interpretacoes_e_desvios_do_construtor": [
        "a) o veredito de maquina segue o molde do DESENHO: no meio, a faixa de |Z contra K| entra EXATAMENTE como o literal a escreve (CONSISTENT_WITHIN_1SIGMA), sem prefixo; os ramos, o BELOW_5SIGMA e o OUTCOME sao montados do recalculo (outro ramo que o do resultado embutido = RECUSA)",
        "b) a guarda de frases da v411 herda a da v410 MENOS duas regras superadas pela abertura (D169): a F54 (onde H0DN aparece, “pre-registrado; nenhum dado observado lido”) sai e da lugar a F67; da F56 sai so' “o teste aberto / a abertura feita” (a covariancia fisica dita fechada segue reprovada). A gerencia confirma ou corrige",
        "c) a cabeca do teste (exata, DESENHO 5.1 a) traz TGL_PRO+VED, que a P18 selada da v392 (R1) recusa fora do contexto da validade: no texto renderizado (quadro, .md, selo) ela aparece INTEIRA e a P18 e' aplicada com a cabeca retirada; os conferidores do pos-rito e do handoff que passarem a P18 crua sobre o artigo, o handoff ou o selo terao de dizer a mesma excecao (so' a cabeca pre-registrada exata)",
        "d) o que o teste nao decide: os textos usam o RESUMO da gerencia no DESENHO (secao 4); o verbatim da secao 6 do pre-registro NAO e' reemitido (o primeiro item traz a palavra da creditacao, que a P18 recusa); o registro grava o sha256 da secao 6 e o numero de itens",
        "e) o titulo EN do quadro e a frase EN ao lado do estatuto da prova sao traducao do construtor (o DESENHO da' so' o PT); as horas dos atos saem em UTC, como nos recibos",
        "f) os dois insumos de reuso (estimador congelado e BG1) apontam o blob da v410 (_V410_H0DN_INSUMOS), conferido pelo MESMO sha256; os outros 16 vao em base64 (668368 B de b64)",
        "g) o recalculo no ensaio offline e' IDENTICO bit a bit ao resultado da abertura (max dif 0,0 em t, Z, D, suporte, estresses, coerencia e decomposicao); o DESENHO pede 1e-9",
        "h) a mecanica tem a assinatura v411_h0dn_mechanics(beta_, core_, c_, ...) com argumentos opcionais (texto, insumos, caminhos tocados, a funcao e o contrato da v410) para os controles negativos; no rito ela le os globais",
        "i) o vigia de arquivos da v410 (_v410_h0dn_vigia_arquivos) mede os caminhos tocados; a c1 recusa caminho sob a pasta do Kimi (o veto, medido); os 7 caminhos tocados no ensaio sao do import de submodulos do scipy",
        "j) o p00 da v411 foi REESCRITO (o da v410 e' de conteudo IALD2/AEscala); o veredito dele hoje e' FALHOU so' pela marca de copia mecanica nos %d scripts ainda nao adaptados, mais 4 pendentes (o topo, o candidato e o que segue, o pino do memoria.py, a folga do MEMORY.md)" % len(MARCADOS),
        "k) a marca historica de cabecalho das copias (# [ADAPTADO v410, ...]) foi PRESERVADA no bump (subir o rotulo dela diria que a v411 a escreveu); outras linhas historicas sem colchete subiram (ex.: no acom_conferencias, corrigido a mao)"],
    "pendencias_da_gerencia": ["TOPO_RATIFICADO_v411.json (a palavra do operador sobre 5.1 b)", "a revisao de terceiro", "acom_inscrever_prep_v411.py e fechar_preparacao_v411.py (os bumps estao com a marca)", "pino_memoria_py e a folga do MEMORY.md", "a tarefa agendada", "o S3, o rito, a custodia"],
    "nada_tocado": ["o Nos (so' leitura; base_v410 e' copia de bytes)", "o pacote work\\h0dn_bg1_v411_emenda_11nov (so' lido; o executor NAO rodou)", "work\\h0dn_bg1_v410_09nov\\kimi (nada lido)", "C:\\IALD\\TGL_IALD_NATIVE_QWEN5090 (o treino nao foi tocado nem medido)",
                    "a Bancada Um (so' GET)", "C:\\Escritorio", "MEMORY.md e topicos", "o candidato NAO foi gerado"],
    "acom": {"referencia": os.path.join(HERE, "SESSION_REFERENCE_prep_v411.json"), "sha16": s16(os.path.join(HERE, "SESSION_REFERENCE_prep_v411.json")), "nota": "init da fonte DESENHO_v411.md e project; a transicao e' da gerencia (acom_inscrever_prep_v411.py)"},
}
p = os.path.join(HERE, "PRONTO_PARA_CANDIDATO_v411.json")
if os.path.exists(p):
    open(p + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(open(p, "rb").read())
b = json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"); open(p + ".tmp", "wb").write(b); assert os.path.getsize(p + ".tmp") == len(b); os.replace(p + ".tmp", p)
print("PRONTO_PARA_CANDIDATO_v411.json", hashlib.sha256(b).hexdigest()[:16], len(b), "B | a adaptar:", len(MARCADOS), "| p00:", P0["veredito"])

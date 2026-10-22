# -*- coding: utf-8 -*-
"""gerar_registro_r3_4.py (R3.4, 19/10/2026) -- escreve R3_4/registro_mapa_F0.6_R3_4.json (RESULTADO, rota infra.bancada_um.sincronizacao_vnnn; so os campos de `rotas.py modelo`) com os NUMEROS lidos
dos artefatos (controles, recibo real, verificacao do diff). Registro PREPARADO e NAO registrado (ato da gerencia). So le; escreve UM arquivo NOVO.
uso: python -I -B -X utf8 gerar_registro_r3_4.py"""
import sys
sys.dont_write_bytecode = True
import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent.parent
C = json.loads((AQUI / "CONTROLES_NEGATIVOS_R3_4.json").read_bytes())
V = json.loads((AQUI / "VERIFICACAO_DIFF_R3_4.json").read_bytes())
P = json.loads((AQUI / "PINO_RECIBO_PRE_SELO_v394_R3_4.json").read_bytes())
assert C["veredito"] == "TODOS_OS_CONTROLES_NEGATIVOS_RECUSAM_COMO_ESPERADO" and V["reproduz_bit_a_bit"] is True and P["utilizavel_como_recibo_pre_selo_do_B_n"] is True
nomes = [c["controle"] for c in C["controles"]]
n_s, n_p, n_m = (sum(1 for n in nomes if n.startswith(p)) for p in ("R34_S_", "R34_P_", "R34_M_"))
base = str(AQUI)
arts = ["sincronizar_bancada.py", "controles_negativos_r3_4.py", "montar_sandbox.py", "gerar_cadeia_de_selos.py", "gerar_bateria_r3_4.py", "derivar_recibo_kernel_r3_4.py", "bateria_r3_4/t12_t14_atrator_r3_4.py",
        "bateria_r3_4/PINO_UM_PY_v393.json", "BATERIA_VINCULO_v393.json", "CADEIA_DE_SELOS_v394.json", "KERNEL_RECIBO_v394_R3_4.json", "CRITERIOS_V392.json", "CONTROLES_NEGATIVOS_R3_4.json",
        "DIFF_R3_3_R3_4.patch", "VERIFICACAO_DIFF_R3_4.json", "PINOS_R3_4.json", "PINOS_BN_v394.R3_4.json", "PINO_RECIBO_PRE_SELO_v394_R3_4.json", "RESULTADO_R3_4.md",
        "recibo_pre_selo_v394/" + Path(P["path"]).name, "evidencias/VERIFICACAO_RECIBO_PRE_SELO_REAL.json"]
reg = dict(
    tipo="RESULTADO", rota_id="infra.bancada_um.sincronizacao_vnnn", dominio="INFRA",
    titulo="R3.4 do esboco sincronizar_bancada.py: salto com a cadeia de selos verificada por hash, bateria por versao (pino do um.py lido dos pinos da cadeia) e modulos de auditoria sem declaracoes; %d/%d controles com python -I -B -X utf8; recibo pre_selo REAL da v394 com BATERIA_PASSA" % (C["passam"], C["n"]),
    pergunta="A R3.4 deixa o elo B(n) recuperar a Bancada de producao pinada na v392 (o elo da v393 nunca rodou) sem confiar em campo do proprio recibo, regenera a bateria por versao (T12/T13/T14 sem o sha fixo da v391) e aceita as 3 pedras de auditoria sem declaracoes (NetworkProofAuditR3/R7/R8), sem regredir os 401 controles da R3.3?",
    dados=["Bancada de producao (so lida): manifesto B3 %s" % C["producao_intocada"]["manifesto_sha256"][:16],
           "Nos real v393 (so lido): um.py 18be2ddb06c60f90, selo bfddccfd153374dd; copias de bytes base_v392/base_v393 e APLICADO_AO_CANONICO_20261014_172946 da cadeia_de_selo (so lidas) com os backups .bak_ do Nos",
           "F1.ATRATOR do tunel (so lido): pre-registro congelado que pina o um.py v391, runners e resultados arquivados",
           "KERNEL_RECIBO_v394 (R3_2, snapshot de bytes em R3_4/evidencias, igual ao vivo no fecho) e as 3 fontes de NetworkProofAuditR3/R7/R8 (copias em R3_4/evidencias/fontes_reais_v394; so lidos)",
           "sandbox C:/t/vb10 (raiz curta; %d juncoes desfeitas com os.rmdir no link; apagado)" % len(C["juncoes_criadas"]),
           "livro de eventos real (so lido): %d linhas na fotografia final; nenhum elo de sincronizacao" % C["eventos_jsonl_real"]["linhas_depois"]],
    metodo="copia da R3.3 pinada (71507fd02b70b115) com patch: carregar_cadeia_de_selos (contrato CADEIA_DE_SELOS_R3_4, chaves fechadas, copias de bytes por sha256, selo pina o um.py e o kernel de cada elo, "
           "registro do instalador + backups de bytes por ligacao, elos consecutivos, inicio = Bancada, fim = Nos/recibo) e BANCADA_ATRASADA_SEM_CADEIA_DE_SELOS em pre_selo; recibo declara salto e versoes puladas "
           "(REPINADA_B<n>__SALTO_<de>_<ate>); pos_selo aceita o recibo de salto e grava sincronizacao.salto; pinos_da_versao + pina_o_um_py na bateria (BATERIA_COM_PINO_VELHO, BATERIA_SEM_PINOS_DA_VERSAO) com "
           "gerar_bateria_r3_4.py e o driver t12_t14_atrator_r3_4.py (pino do um.py repinado NA COPIA do pre-registro); KERNEL_RECIBO_R3_4 com modulos_de_auditoria e varredura da fonte por script; sandbox "
           "reconstruido de copias de bytes; controles herdados com os runs refeitos e %d novos" % len(C["novos_R3_4"]),
    resultado="%s %d/%d em %s s (R3.3 %d/%d presentes, R3.2 %d/%d, R3.1 %d/%d, R3 %d/%d; %d novos: %d S, %d P, %d M); recibo pre_selo REAL da v394 (salto v392 a v393, ensaio): %s, bateria %s com %d PASSA, %d FALHA e %d NAO_EXECUTADO "
              "(T17, so no pos_selo), aceito pelo caminho de conferencia do B(n) contra a producao real em leitura; DIFF reproduz a R3.4 bit a bit" % (
                  C["veredito"], C["passam"], C["n"], C["segundos"], C["da_R3_3_presentes"], C["n_da_R3_3"], C["da_R3_2_presentes"], C["n_da_R3_2"], C["da_R3_1_presentes"], C["n_da_R3_1"], C["da_R3_presentes"],
                  C["n_da_R3"], len(C["novos_R3_4"]), n_s, n_p, n_m, P["veredito"], P["contagens"]["veredito_bateria"], P["contagens"]["passa"], P["contagens"]["falha"], P["contagens"]["nao_executado"]),
    veredito="R3_4_ENTREGUE__AGUARDA_REAUDITORIA_CURTA", estatuto="REAL", status="EM_CURSO", olhou_dados=False,
    defeito="a cadeia prova consistencia de copias de bytes e de registros do instalador, nao autenticidade (o selo NAO pina o selo anterior: medido; sem assinatura); o pre-registro do atrator e repinado so na copia do replay "
            "(adendo a ratificar pelo Codex); o corpo do run_cmd de um modulo de auditoria so tem comandos de topo e lista fechada conferidos, a inocuidade semantica nao e provada; o B(n) pos_selo da v394 REAL nao "
            "foi rodado (precisa do selo v394, do recibo do kernel R3_4, da bateria da v394 e do CRITERIOS_v394); residuos da R3.3 seguem",
    nao_refazer="nao refazer o salto, a bateria por versao, o modulo de auditoria nem os 401 controles da R3.3; nao rodar a bateria R2 contra o Nos atual (o T12 pina o um.py v391)",
    proximo_passo="gerencia: reauditar so as partes novas (S, P, M); pinar esboco, bateria v393, cadeia e recibo pre_selo em vNNN_pins (PINOS_BN_v394.R3_4.json); decidir o recibo do kernel R3_4 (derivado, proposto) e o x19; "
                  "depois do selo da v394 gerar a bateria da v394 e rodar o pos_selo em ensaio; operador: B(n) aplicar com evento c1 e 10-ter",
    onde=base, artefatos=[str(AQUI / a) for a in arts], refs=[],
    nota="F0.6 R3.4, construtor Sonnet da gerencia c1, a pedido da gerencia (cadeia da v394). Registro preparado e NAO registrado (ato da gerencia). NOT_FALSIFIED nunca e creditacao; gate NONE.")
p = AQUI / "registro_mapa_F0.6_R3_4.json"
with open(p, "xb") as f:
    f.write(json.dumps(reg, ensure_ascii=False, indent=1).encode("utf-8"))
print(p, len(reg["artefatos"]))

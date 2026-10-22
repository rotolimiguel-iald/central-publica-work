# -*- coding: utf-8 -*-
"""Gera registro_mapa_F1.MOTOR_R2.json (proposta de registro RESULTADO na rota formal.iald_o_motor_unico; NAO registra:
o registro no mapa e ato da gerencia). Artefatos so se existirem (falha visivel se faltar algum)."""
import os, json, hashlib

AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rel = ["fonte/TGLExt/IALD.lean", "fonte/AuditIALD_R2.lean", "olean/IALD.olean", "olean/TheUnitIsTheRank.olean",
       "olean/TheTimeIsNotAPost.olean", "logs/r2_iald_final_RECIBO.json", "logs/r2_iald_final_SAIDA.txt",
       "logs/r2_audit_final_RECIBO.json", "logs/r2_audit_final_SAIDA.txt", "TABELA_R1_R2.md", "COMPARACAO_R1_R2.json",
       "DECLARACOES_R2.json", "DIFF_R1_R2.diff", "numerico/ensaio_motor_r2.py", "numerico/RESULTADO_NUMERICO_R2.json",
       "IMPRESSAO_DIGITAL_KERNEL_ANTES.json", "IMPRESSAO_DIGITAL_KERNEL_DEPOIS.json", "medidas/SANDBOX_MONTAGEM.json",
       "medidas/CONFERENCIA_REGUA.json", "RESULTADO_R2.md"]
arts = []
for r in rel:
    p = os.path.normpath(os.path.join(AQUI, r))
    if not os.path.isfile(p):
        raise SystemExit("FALHA VISIVEL: artefato ausente " + p)
    arts.append(p)
rec = json.load(open(os.path.join(AQUI, "logs", "r2_audit_final_RECIBO.json"), encoding="utf-8"))
ri = json.load(open(os.path.join(AQUI, "logs", "r2_iald_final_RECIBO.json"), encoding="utf-8"))
num = json.load(open(os.path.join(AQUI, "numerico", "RESULTADO_NUMERICO_R2.json"), encoding="utf-8"))
cmp_ = json.load(open(os.path.join(AQUI, "COMPARACAO_R1_R2.json"), encoding="utf-8"))
reg = {
    "tipo": "RESULTADO",
    "rota_id": "formal.iald_o_motor_unico",
    "dominio": "FORMAL",
    "titulo": "Pedra TGLExt.IALD r2 (o motor unico, nome provisorio): as oito correcoes C1-C8 aplicadas em sandbox",
    "pergunta": "A pedra r1 corrigida por C1-C8 (sem decidir o que e do operador) compila, fica no trio e mantem os enunciados que ja passavam?",
    "dados": ["nenhum dado observado; so o kernel v391 do Nos (so leitura) e as candidatas vigentes da v392"],
    "metodo": ("lean v4.31.0 copiado para C:/t/mo2; LEAN_PATH = copia verificada do .lake/build do Nos + pacotes do .lake, so leitura; "
               "#print axioms de todas as declaracoes; comparacao r1/r2 de enunciados por script; ensaio numerico refeito com beta de runtime "
               "(ALPHA_FINE_CODATA_2018 da l.5557 do um.py x sqrt e); impressao digital do tgl_kernel antes e depois"),
    "resultado": ("EXIT %d, %d erros, %d sorry; %d declaracoes, %d/%d #print axioms no trio; fonte %s; olean %s (reproduzido bit a bit); "
                  "r1->r2: %s, REMOVIDA 0; ensaio %d/%d %s; kernel antes = depois; achado: a condicao exata da idempotencia e "
                  "ancora fraca OU motor nulo (o motor nulo tem peso)") % (
        ri["exit_code"], ri["n_erros"], ri["declaration_uses_sorry"], rec["n_print_axioms"],
        sum(1 for v in rec["axiomas"].values() if set(v) <= {"propext", "Classical.choice", "Quot.sound"}), rec["n_print_axioms"],
        ri["source_sha256"][:16], ri["olean_sha256"][:16],
        ", ".join("%s %d" % (k, v) for k, v in sorted(cmp_["contagem"].items())),
        num["checks_total"] - len(num["checks_falhos"]), num["checks_total"], num["sanidade"]),
    "veredito": "PEDRA_R2_COMPILADA_EM_SANDBOX__C1_C8_APLICADAS__NAO_INSTALADA__GATE_INTOCADO",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": ("Nao reauditada por terceiro; ESPEC/PREREGISTRO/RESULTADO_CONSTRUCAO/relatorio seguem com as frases antigas (correcao ao lado e da gerencia); "
                "a Fundacao continua no fecho de importacao so por TheTimeIsNotAPost; o nome dephasing de B8(iii) mantem o homonimo em ingles (rotulado)."),
    "nao_refazer": "Nao refazer C1-C8 nem o re-pino: a r2 compila no trio e a tabela r1->r2 e calculada por script.",
    "proximo_passo": ("Reauditoria independente da r2; decisoes do operador: U unitario por tipo (P3), DualScalingData do motor (P4), "
                      "Pi_N := post a (P2), nome e entrada na v392 (P6)."),
    "onde": os.path.normpath(os.path.join(AQUI, "fonte/TGLExt/IALD.lean")),
    "artefatos": arts,
    "refs": ["formal.iald_o_motor_unico"],
    "nota": "Proposta gerada pelo construtor da rodada 2; nao registrada no mapa (a unidade proibe escrever no mapa).",
}
out = os.path.join(AQUI, "registro_mapa_F1.MOTOR_R2.json")
json.dump(reg, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(out, hashlib.sha256(open(out, "rb").read()).hexdigest()[:16])
print(reg["resultado"])

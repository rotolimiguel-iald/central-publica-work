# -*- coding: utf-8 -*-
"""Gera registro_rota_F1.IDENTIDADE.json (ROTA) e registro_mapa_F1.IDENTIDADE.json (RESULTADO), so com os campos de
`rotas.py modelo`, e poe o sha256 do FREEZE na tabela do RESULTADO.md. Nao registra no mapa (isso e da gerencia)."""
import json, os, hashlib

B = "C:/IALD/Central de Patentes/work/identidade_cordeiro_13out/"
BS = chr(92)


def win(p):
    return p.replace("/", BS)


# 1) sha do FREEZE na tabela do RESULTADO.md (troca exata, uma vez)
fz = hashlib.sha256(open(B + "2_PREREGISTRO/FREEZE.json", "rb").read()).hexdigest()
rp = B + "4_RESULTADO/RESULTADO.md"
s = open(rp, encoding="utf-8").read()
old = "(congelado 13/10/2026 08:10:04 −03:00; a pedra NÃO existia) | ver o arquivo |"
if old in s:
    s = s.replace(old, "(congelado 13/10/2026 08:10:04 −03:00; a pedra NÃO existia) | `" + fz + "` |", 1)
    open(rp, "w", encoding="utf-8", newline="\n").write(s)

arts = ["2_PREREGISTRO/PREREGISTRO.json", "2_PREREGISTRO/FREEZE.json", "3_PEDRA/pedra/TheIdentityHasAName.lean",
        "3_PEDRA/pedra/TheIdentityHasAName.olean", "3_PEDRA/logs/final_RECIBO.json", "3_PEDRA/logs/auditoria_SAIDA.txt",
        "3_PEDRA/logs/ENSAIO_NUMERICO.json", "3_PEDRA/logs/IMPRESSAO_ANTES.json", "3_PEDRA/logs/IMPRESSAO_DEPOIS.json",
        "4_RESULTADO/RESULTADO.md", "1_LEVANTAMENTO/LEVANTAMENTO.md"]
for a in arts:
    assert os.path.exists(B + a), a
arts = [win(B + a) for a in arts]

comum = {
    "rota_id": "formal.a_identidade_tem_nome",
    "dominio": "FORMAL",
    "titulo": "F1.IDENTIDADE: a pedra da identidade (tudo defasa, o traço permanece; ω projeção quadrática da inscrição com α lido por dentro; eu sou o que sou; o alicerce; o Nome posto; na Torre H_φ)",
    "pergunta": "A ordem do operador de 13/10 (verbatim sha256 2ebc1dd3d73cf940…) cabe no kernel como validade da estrutura, com o Nome como dado POSTO e não como teorema, e com instância na Torre?",
    "dados": ["verbatim do operador de 13/10/2026 (sha256 2ebc1dd3d73cf94094551de520d5d9765dde5633594f2c4ca61cc2fb1df1002e)",
              "kernel do Nós (tgl_kernel, só leitura; .olean do TGLExt copiados e conferidos byte a byte)",
              "um.py v391 (8e7b9927ceae64b8) l.5557 lida nos bytes, sem executar (só o ensaio numérico)"],
    "metodo": "Levantamento (mapa, inventário, kernel, candidatas v392) -> pré-registro I1-I6 e C1-C5 congelado por hash (FREEZE 13/10 08:10 -03:00) antes da pedra -> pedra em sandbox (toolchain v4.31.0 copiado, LEAN_PATH só-leitura, -o só no sandbox) -> #print axioms + collectAxioms do namespace -> ensaio numérico de I1-I2 -> impressão digital do tgl_kernel antes/depois.",
    "olhou_dados": False,
    "onde": win(B + "3_PEDRA/pedra/TheIdentityHasAName.lean") + " (namespace TGLExt.TheIdentityHasAName; NÃO instalada)",
    "artefatos": arts,
    "refs": ["formal.posto_e_defasagem_da_unidade", "formal.iald_o_motor_unico", "umpy.v390.selo_fundacao_agape",
             "kernel.lema3.superposicao_e_a_passagem_07out", "kernel.v386_tipagem_do_verbo",
             "kernel.leitura_cria_o_objeto_07out", "formal.f1_2.dual_scaling_reuse_011"],
}
rota = dict(tipo="ROTA", **comum)
rota.update({
    "resultado": "ver o registro RESULTADO desta rota",
    "veredito": "",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "defeito": "pendências do operador: nome da pedra, termo do cordeiro imolado, escolha da Torre, Nome no core; auditoria independente não feita",
    "nao_refazer": "levantamento, pré-registro congelado e compilação em sandbox medidos; não recompilar sem mudança de bytes da pedra",
    "proximo_passo": "auditoria independente (quem constrói não aprova); decisões do operador; instalação na v392 se ordenada",
    "nota": "Construtor da gerência c1, 13/10/2026. O Nome é dado [POSTO pelo operador]; nenhum teorema fala de história ou de pessoa; [ONTO] a identificação do cordeiro imolado; números do artigo Conscious Singularity [DECLARADO], fora da pedra."})
res = dict(tipo="RESULTADO", **comum)
res.update({
    "resultado": "EXIT 0, 0 erros, 0 avisos, 0 sorry; 119 constantes do namespace no trio {propext, Classical.choice, Quot.sound} por collectAxioms, 0 fora; olean 06e2a9990f3714b2; fonte 1b68316aecf6cdc6; impressão digital do tgl_kernel antes = depois (d6e073568d17e26b, 11049 arquivos). I1.a-b PASSA (traço 1 sob dephase para todo t e no limite); I1.c-d PASSA como negativo (posto 2 para t > 0 e no limite); I2.a-e PASSA (1 = q² + α²; Tr = 1, idempotente, posto 1; ⟨e₂, ω e₂⟩ = α²; a forma não fixa α; √(leitura interior) = α); I3.a-d PASSA; I4 CITADA/ONTO/OPEN (re-exportação de Fundacao.agape sob o nome provisório alicerce_fundante); I5 PASSA (NamedIdentity, ofName, rename por rfl, the_structure_does_not_fix_the_name) com o nome Jesus Cristo como dado POSTO; I6.a PASSA na Torre H_φ (TowerHilbert, omegaState, modularFlow, σ_x Ω); I6.b FALHA como pré-registrada (a defasagem da torre é unitária); C1-C5 PASSA; ensaio numérico com α da l.5557: critérios ok.",
    "veredito": "PEDRA_IDENTIDADE_SANDBOX__I1_I2_I3_I5_I6A_PASSAM__I1_NEGATIVO_DO_POSTO_PASSA__I4_CITADA_ONTO_OPEN__I6B_FALHA_PRE_REGISTRADA__119_CONSTANTES_NO_TRIO__NOME_POSTO_PARAMETRICO__NAO_INSTALADA__GATE_INTOCADO",
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "defeito": "I6.b não construído (falta defasagem dissipativa em B(H_φ)); o negativo do posto vale na base de D [INPUT da gerência]; auditoria independente pendente; fatos das candidatas v392 re-provados por cópia citada (não importados)",
    "nao_refazer": "não recompilar a pedra sem mudança de bytes; não reabrir o levantamento (LEVANTAMENTO_DADOS.json)",
    "proximo_passo": "auditoria cética independente; operador: nome da pedra, termo do cordeiro imolado, Torre, Nome no core do um.py; v392 se ordenado",
    "nota": "Desvios ao lado do pré-registro: I2.c sem hipóteses e I2.e só com 0 ≤ α (mais fortes); C2 com conjunção extra diagExpect ω = ω; C3 refina a régua (em [−1, 0) a forma vale e falha a recuperação). Nada move o gate; validade no kernel não é creditação."})
for nome, d in [("registro_rota_F1.IDENTIDADE.json", rota), ("registro_mapa_F1.IDENTIDADE.json", res)]:
    json.dump(d, open(B + "4_RESULTADO/" + nome, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", fz[:16])

# -*- coding: utf-8 -*-
"""Monta os dois registros do mapa de rotas da F1.TEMPO (ROTA e RESULTADO), versao R2, e os valida A SECO
com rotas._valida (so le arquivos e calcula sha256). NAO registra: `rotas.py registrar` e ato da gerencia
(a ROTA primeiro, depois o RESULTADO). Grava tambem as consultas feitas ao mapa (so leitura)."""
import importlib.util, json, os, re, subprocess, sys
ROTAS_PY = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # 4_RELATORIO
R2S = os.path.join(BASE, "R2", "saidas")
RID = "formal.tempo_santo_fluxo_e_dissipacao"
U = r"C:\IALD\Central de Patentes\work\tempo_santo_12out"
REFS = ["formal.singularidade_le_atrator", "quantica.pilar_v384_rodada_completa", "umpy.v390.selo_fundacao_agape",
        "kernel.v386_tipagem_do_verbo", "kernel.leitura_cria_o_objeto_07out", "formal.f1_2.dual_scaling_reuse_011",
        "programa.auditoria.f1_2_ponte_v351_07out", "quantica.inventario_gkls_um_py_kernel",
        "infra.bancada_um.sincronizacao_vnnn"]

ROTA = {
 "tipo": "ROTA",
 "rota_id": RID,
 "dominio": "FORMAL",
 "titulo": "F1.TEMPO: o tempo que não se deixa nomear (texto do operador de 12/10: Kadosh, Pauli, fluxo modular, Liouville, dissipação, atrator, «puro amor») testado na face finita do kernel (pedra candidata em sandbox) e num modelo ótico sintético; pré-registro congelado (R1), ADENDO aditivo congelado antes do reensaio (R2), duas auditorias independentes por rodada",
 "pergunta": "O que, na segunda parte do texto de 12/10 sobre o tempo «santo», tem forma matemática na face finita e passa no kernel e no modelo ótico: (T1) não há operador de tempo em dimensão finita; (T2) Pauli em dimensão infinita (só citação); (T3) o tempo como fluxo modular KMS; (T4) Liouville × dissipação; (T5) o conjunto fixo da defasagem pura; (T6) a seta pela pureza; (T7) o inverso não positivo; (T8) a coerência obedece à Ágape; (T9) o tempo não é posto (nenhum instante finito é idempotente; posto pleno; o posto só no limite); (T10) o relógio lê módulo período e o agora não se move; (T11) em ½·1 o relógio modular para? E o que é só leitura [ONTO] ou literatura [KNOWN]?",
 "dados": [
  "nenhum dado observado",
  "modelo ótico sintético da F1.ATRATOR: S = Smat(θ_M), C = D∘Ad(S)∘D, T = R + λ(I − R), λ = 1 − 2β; β lido nos bytes do um.py v391 (l.5557, igual à l.95) e calculado em runtime; semente 20261012"
 ],
 "metodo": "R1 (12/10): levantamento → pré-registro congelado por hash ANTES de qualquer ensaio (FREEZE 6b29d4c9b09e5553, 16:09:07Z: 23 frases mapeadas, 30 excertos, 11 afirmações, 22 controles, 15 sondas; regra por subitem PASSA/FALHA/NÃO_CONSTRUÍDA/INVÁLIDO, CITADA, LEITURA, ABERTA; sem veredito global) → face ótica (float64 + decimal 200) → face kernel (pedra TGLExt.TheTimeHasNoRank em sandbox, Lean 4.31.0, LEAN_PATH só de leitura, impressão digital do tgl_kernel igual) → duas auditorias → relatório R1. Replicação sem ADENDO (2_OPTICO/rodada_2 com código novo; 3_KERNEL/rodada_2) auditada em 13/10 (reprodução e estatuto). R2: ADENDO aditivo congelado (FREEZE_R2 0737f608505afdb5, 23:07:58Z) com erratas ao lado ao pré-registro (E3), regra uniforme de tolerância τ(k) = k·(w·|δ| + m·eps) + c·eps (Higham) + caminho exato a 200 dígitos (mpmath × decimal), lista E5 de correção da pedra e controles AUD-1/2/5/6/7/8 e C-UNIF-a..d → reensaio ótico R2 (T9.o′(c), O-f′; V4 reproduz a R1 bit a bit) → pedra corrigida TGLExt.TheTimeIsNotAPost (E5 item a item; T3.b(iii) habitada + face finita) → relatório R2. Auditoria independente da R2 (U1) ainda por fazer.",
 "estatuto": "INPUT (protocolo da gerência c1); alvo REAL na face finita; DERIVED β (lido e calculado); KNOWN por citação (Pauli, Liouville, tempo térmico, Takesaki, Landauer, Higham); ONTO as leituras do operador; OPEN o ciclo limite e a identificação dos três comportamentos com os dois regimes da casa",
 "status": "EM_CURSO",
 "olhou_dados": False,
 "onde": U + r" (0_LEVANTAMENTO, 1_PREREGISTRO, 2_OPTICO, 3_KERNEL, 4_RELATORIO, 5_R2); pedra candidata R2 5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean (não instalada; nome provisório)",
 "artefatos": [
  r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
  U + r"\1_PREREGISTRO\FREEZE.json",
  U + r"\1_PREREGISTRO\PREREGISTRO.json",
  U + r"\1_PREREGISTRO\PREREGISTRO.md",
  U + r"\0_LEVANTAMENTO\LEVANTAMENTO.md",
  U + r"\5_R2\0_ADENDO\FREEZE_R2.json",
  U + r"\5_R2\0_ADENDO\ADENDO_R2.md",
  U + r"\5_R2\0_ADENDO\ADENDO_R2.json",
  U + r"\5_R2\0_ADENDO\scripts\tolerancia_uniforme_r2.py"
 ],
 "refs": REFS,
 "nota": "Unidade F1.TEMPO (trilha TEMPO) da gerência c1, workflow posto-e-tempo (wf_ce423138-e42); trilha irmã F1.FREQUENCIA (o rank; texto de 11/10). Consultas antes, com o mapa só lido (R2\\saidas\\rotas): 0 rotas para «tempo santo», «F1.TEMPO», «TheTimeIsNotAPost» (livro com 1.043 registros, cabeça a817c19e72d1f159). O registro desta rota é ato da gerência; nenhum executor escreveu no mapa. A cunhagem é do operador."
}

RESULTADO = {
 "tipo": "RESULTADO",
 "rota_id": RID,
 "titulo": "F1.TEMPO, duas colunas: R1 (FREEZE 6b29d4c9) — PASSA em T1, T3 a T8, T10, T11, T2 CITADA, T9 FALHA só pelo critério numérico ótico (1e-13 abaixo do piso do float64); R2 (ADENDO, FREEZE_R2 0737f608) — T9.o′(c) e O-f′ PASSA sob tolerância uniforme e caminho exato a 200 dígitos, pedra corrigida TheTimeIsNotAPost compilada limpa (152 no trio, 0 sorry) com T3.b(iii) habitada; ciclo limite ABERTA; falta a auditoria independente da R2 (U1) e o nome do operador antes de entrar no um.py",
 "resultado": "Por afirmação, pela regra congelada (R1 | R2): T1 PASSA | PASSA; T2 CITADA (T2.b PASSA, opcional) | CITADA; T3 PASSA com ressalva (T3.b(iii) sem habitante) | PASSA sem ressalva (probe_identity_flow_not_kms_inhabited com theSpecificAQFTWitness; identity_flow_not_kms_finite: ω(E01E10) = 2/3 ≠ 1/3); T4 PASSA | PASSA (O-f′: float rel 5,913e-16 ≤ τ_B(10) = 1,032e-14; exato ≤ 1,76e-199; C-UNIF-a FALHA desde k = 3 como registrado; T4.b(iii) condicional, sem FockCertificate); T5 PASSA (T5.c CITADA) | idem; T6 PASSA | PASSA; T7 PASSA | PASSA; T8 PASSA + LEITURA | idem (a Ágape é a lei e^{-s}; AUD-1 em termo); T9 FALHA (T9.o(c): 6,518119377574294e-13 > 1e-13 em k = 10^4, acima desde k = 1529; piso k|δ|/2 com δ = 1,1796e-16; kernel T9.a-e PASSA) | T9′ PASSA (float 6,518e-13 ≤ τ_T(10^4) = 2,8107e-12, razão máx. 0,417; exato mpmath 200 ≤ 1,34e-198; decimal 200 ≤ 1,48e-197; C-UNIF-b/c/d como registrado; T9.t LEITURA da gerência, corrigida); T10 PASSA + LEITURA | idem (título com «registra»); T11 PASSA, face finita | idem (reafirmação; ½·1 tem posto 2 e pureza ½); S46.3 ciclo limite ABERTA. Replicação sem ADENDO (2_OPTICO/rodada_2, 3_KERNEL/rodada_2): 621 números iguais à R1, 0 diferenças; pedra a68539d8cf14260d recompilada por auditor com .olean 9d9a1e122b01b1e8 idêntico (141 no trio). Pedra R2 4d8a82591badd010: EXIT 0, 152 #print axioms (151 no trio; post_not_isUnit sem axioma), 0 sorry, 0 aviso, .olean b52382ec16542a84, toolchain apagado; 18 aspas, todas substrings dos verbatins; SEM auditoria independente. β em runtime 0,012031300400803142 (lido nos bytes, Δ = 0); impressão digital do tgl_kernel igual (meta b1b47447, src 911cb40b) em todas as etapas.",
 "veredito": "SEM_VEREDITO_GLOBAL__R1_T1_PASSA__T2_CITADA__T3_PASSA_RESSALVA__T4_PASSA__T5_PASSA__T6_PASSA__T7_PASSA__T8_PASSA_LEITURA__T9_FALHA_CRITERIO_NUMERICO_OTICO__T10_PASSA_LEITURA__T11_PASSA_FACE_FINITA__R2_SOB_ADENDO_T3_PASSA_SEM_RESSALVA__T4_PASSA__T9_PASSA_TAU_UNIFORME_E_EXATO_200__PEDRA_R2_COMPILADA_SEM_AUDITORIA_INDEPENDENTE__CICLO_LIMITE_ABERTA__NAO_ENTRA_NO_UM_PY_ANTES_DA_U1_E_DO_NOME__GATE_INTOCADO",
 "estatuto": "REAL (face finita: kernel em sandbox e modelo sintético); DERIVED β; INPUT da gerência a regra uniforme (justificada por Higham, KNOWN); KNOWN por citação; ONTO as leituras; validade matemática na face testada, não creditação",
 "status": "EXAMINADA_COM_DEFEITO",
 "olhou_dados": False,
 "defeito": "(1) A pedra R2 (TheTimeIsNotAPost.lean 4d8a82591badd010) e o reensaio R2 (RESULTADO_REENSAIO_R2.json 44e745447fae0991) têm só a autoconferência dos construtores; a auditoria independente de 13/10 recompilou e refez a REPLICAÇÃO sem ADENDO (3_KERNEL/rodada_2, 2_OPTICO/rodada_2), não a R2 (regra U1 do ADENDO). (2) Nomes residuais na pedra R2 que carregam leitura além do termo: the_two_regimes_of_time (a docstring declara a identificação [OPEN]) e the_face_lands / face_has_a_limit / face_distinguishes_instants / face_clock_has_no_period («face» é a palavra do regime da casa; aqui nomeia o decaimento real); a replicação os havia neutralizado, o E5 não os listou. (3) O nome da pedra é provisório; o final é do operador. (4) β segue rotulado «[REAL — medido aqui]» no RESULTADO_OPTICO.json e no run_optico.py da replicação 2_OPTICO/rodada_2 (errata ao lado proposta); as erratas E1 (fractal_dephasing_principle, âncoras definicionais) e E2 (dois sentidos de «defasar») no um.py são atos da cadeia de selo ainda não feitos. (5) T4.b(iii) segue condicional (FockCertificate sem habitante exibido). (6) Toolchain Lean de 3,0 GB deixado no scratchpad pelo auditor de estatuto da R1 (TEMPO_AUD_ESTATUTO/sandbox), fora da casa, não apagado.",
 "nao_refazer": "Não refazer os ensaios óticos nem as compilações da R1 e da replicação: o ótico reproduziu bit a bit em três execuções e dois códigos; a pedra da replicação deu .olean idêntico em auditor independente. Não ler a FALHA R1 de T9 como contraexemplo: é piso da representação float64 (k|δ|/2), a identidade é exata e o kernel a prova; não ler o PASSA R2 de T9 sozinho: as duas colunas ficam. Não ler a face ótica como evidência nem como rito: é consistência numérica. Não ler T2 como teste. Não ler a Ágape na coerência como conteúdo próprio do dephasing (vale para toda lei e^{-s}; o próprio é o registro que não escala). Não atribuir ao operador «o tempo é o Verbo, não o Nome», «o tempo não tem posto» nem «o relógio mede a sombra»: 0 ocorrências nos verbatins. Não pedir limite ao ângulo. Não contar «152 teoremas». Não reensaiar T9 numa representação que passe sem ADENDO R3.",
 "proximo_passo": "(a) U1: dois auditores independentes com sandbox próprio recompilam TheTimeIsNotAPost.lean 4d8a82591badd010 (.olean b52382ec16542a84 bit a bit; trio; 0 sorry; fingerprint igual; toolchain apagado; caveat de caminho longo), refazem reensaio_r2.py d1297cb94b363398 (medidas idênticas; C-UNIF como registrado) e conferem E5 item a item e as 16/18 aspas. (b) Gerência: decidir N1/N2 (renomear the_two_regimes_of_time e face_* em tentativa preservada antes da U1, ou docstring). (c) Operador: o nome da pedra; qual «defasar» é o tempo; repousar × ser lembrada; o chão firme; a reunião puro amor/ágape/sacrifício-amor; «santo»; o ciclo limite. (d) Erratas ao lado E1, E2 (um.py, cadeia de selo) e E6 (replicação ótica, β [DERIVED]). (e) Na v392 entram só os subitens PASSA reauditados, com CITADA e LEITURA marcadas, o quadro de duas colunas (T9: R1 FALHA | R2 PASSA), junto com o teorema do atrator; inserção pela cadeia de selo. (f) Registrar esta rota (ROTA primeiro) e atualizar o quadro.",
 "onde": U + r"\4_RELATORIO\RELATORIO_FINAL.md (R2: tabela na §2; achados na §5; erratas na §6; divergências na §7; resíduo na §8; o que falta na §9); relatório R1 preservado em 4_RELATORIO\R1_preservado\RELATORIO_FINAL_R1.md",
 "artefatos": [
  U + r"\4_RELATORIO\RELATORIO_FINAL.md",
  U + r"\4_RELATORIO\R1_preservado\RELATORIO_FINAL_R1.md",
  U + r"\2_OPTICO\RESULTADO_OPTICO.json",
  U + r"\2_OPTICO\diagnostico\DIAGNOSTICO_T9c.json",
  U + r"\3_KERNEL\RESULTADO_KERNEL.json",
  U + r"\3_KERNEL\sandbox\TheTimeHasNoRank.lean",
  U + r"\2_OPTICO\rodada_2\RESULTADO_OPTICO.json",
  U + r"\2_OPTICO\rodada_2\COMPARACAO_R1_R2.json",
  U + r"\3_KERNEL\rodada_2\RESULTADO_KERNEL.json",
  U + r"\3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.lean",
  U + r"\3_KERNEL\rodada_2\sandbox\TheTimeHasNoRank.olean",
  U + r"\5_R2\0_ADENDO\ADENDO_R2.md",
  U + r"\5_R2\0_ADENDO\FREEZE_R2.json",
  U + r"\5_R2\2_REENSAIO\RESULTADO_REENSAIO_R2.json",
  U + r"\5_R2\2_REENSAIO\RECIBO_REENSAIO_R2.json",
  U + r"\5_R2\2_REENSAIO\reensaio_r2.py",
  U + r"\5_R2\2_REENSAIO\CONTINUACAO_13out\RECHECK_INDEPENDENTE_13out.json",
  U + r"\5_R2\1_PEDRA\RESULTADO_PEDRA_R2.json",
  U + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.lean",
  U + r"\5_R2\1_PEDRA\sandbox\TheTimeIsNotAPost.olean",
  U + r"\5_R2\1_PEDRA\saidas\TABELA_DECLARACOES_R2.md",
  U + r"\5_R2\1_PEDRA\saidas\CONFERENCIA_ASPAS_PEDRA_R2.json",
  U + r"\5_R2\1_PEDRA\saidas\LIMPEZA_RECIBO.json",
  U + r"\4_RELATORIO\AUDITORIAS_R2\MANIFESTO_COPIA_AUDITORIAS_R2.json",
  U + r"\4_RELATORIO\AUDITORIAS_R2\TEMPO_AUD_REPRO\AUDITORIA_REPRO_TEMPO.md",
  U + r"\4_RELATORIO\AUDITORIAS_R2\TEMPO_AUD_REPRO\AUD_COMPILE_PEDRA.json",
  U + r"\4_RELATORIO\AUDITORIAS_R2\TEMPO_AUD_ESTATUTO\MEDIDAS_AUD.json",
  U + r"\4_RELATORIO\R2\saidas\HASHES_RELATORIO_R2.json",
  U + r"\4_RELATORIO\R2\saidas\BETA_RUNTIME_RELATORIO_R2.json"
 ],
 "refs": REFS,
 "nota": "Duas auditorias independentes em 13/10 auditaram a REPLICAÇÃO sem ADENDO (reprodução: 621 números iguais, .olean idêntico, 8 sondas no trio, pode aceitar como está; estatuto: a unidade não pode fechar enquanto a R2 não estiver parada por hash e reauditada). Não se contradizem: objetos diferentes; vale o «não» para a unidade. Pela regra V2 do ADENDO, a R2 de registro é 5_R2; as pastas rodada_2 são tentativas preservadas. O relatório R2 preserva o R1 byte a byte. Um PASSA é validade matemática na face testada, não creditação; o gate não se move; β na natureza a 5σ não é tocado."
}


def carregar_rotas():
    spec = importlib.util.spec_from_file_location("rotas_somente_leitura", ROTAS_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gravar(nome, obj):
    out = os.path.join(BASE, nome)
    b = json.dumps(obj, ensure_ascii=False, indent=1).encode("utf-8")
    with open(out + ".tmp", "wb") as f:
        f.write(b)
    if open(out + ".tmp", "rb").read() != b:
        raise SystemExit("FALHA VISIVEL: temporario nao confere: " + out)
    os.replace(out + ".tmp", out)
    return out


def consultas():
    os.makedirs(os.path.join(R2S, "rotas"), exist_ok=True)
    res = {}
    for termo in ("tempo santo", "F1.TEMPO", "TheTimeIsNotAPost", "TheTimeHasNoRank", "Pauli", "ciclo limite"):
        r = subprocess.run([sys.executable, "-X", "utf8", ROTAS_PY, "consultar", termo], capture_output=True)
        try:
            d = json.loads(r.stdout.decode("utf-8"))
        except Exception:
            d = {"erro": r.stdout.decode("utf-8", "replace")[:300]}
        res[termo] = {"n": d.get("n"), "n_registros": d.get("n_registros"), "cabeca": d.get("cabeca"),
                      "rotas": [x.get("rota_id") for x in d.get("rotas", [])][:10]}
    with open(os.path.join(R2S, "rotas", "CONSULTAS_R2.json"), "wb") as f:
        f.write(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
    return res


def main():
    rotas = carregar_rotas()
    regs = rotas._le()
    ids = {r["rota_id"] for r in regs if r["tipo"] == "ROTA"}
    seqs = {r["seq"] for r in regs}
    val = {"livro_n_registros": len(regs), "rota_id_ja_existe": RID in ids, "refs_existentes": {r: (r in ids) for r in REFS}}
    v1 = rotas._valida(ROTA, ids, seqs)
    v2 = rotas._valida(RESULTADO, ids | {RID}, seqs)
    proibidas = re.compile("CONF" + "IRM|n[aã]o prov" + "ou|p[oó]s-di[cç]+[aã]o", re.I)
    for nome, obj, v in (("ROTA", ROTA, v1), ("RESULTADO", RESULTADO, v2)):
        txt = json.dumps(obj, ensure_ascii=False)
        val[nome] = {"valida_a_seco": True, "palavras_proibidas": proibidas.findall(txt),
                     "maior_campo_de_texto": max(len(str(obj[k])) for k in obj if isinstance(obj[k], str)),
                     "artefatos": [(a["caminho"], a["sha256"][:16], a["bytes"]) for a in v.get("artefatos", [])]}
    f1 = gravar("registro_rota_F1.TEMPO.json", ROTA)
    f2 = gravar("registro_mapa_F1.TEMPO.json", RESULTADO)
    val["arquivos"] = [f1, f2]
    val["consultas"] = consultas()
    val["nota"] = ("Validacao a seco com rotas._valida (le arquivos e calcula sha256; nao escreve). Registrar e ato da "
                   "gerencia: primeiro registro_rota_F1.TEMPO.json, depois registro_mapa_F1.TEMPO.json. Os registros R1 "
                   "estao preservados em R1_preservado.")
    out = os.path.join(R2S, "VALIDACAO_REGISTROS_R2.json")
    with open(out + ".tmp", "wb") as f:
        f.write(json.dumps(val, ensure_ascii=False, indent=1).encode("utf-8"))
    os.replace(out + ".tmp", out)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(val, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()

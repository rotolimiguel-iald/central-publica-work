# -*- coding: utf-8 -*-
"""gerar_registro_mapa.py -- DELTA 19/10: escreve registro_mapa_delta_19out.json (SO' os campos de `rotas.py modelo`; tipo ROTA) LENDO os artefatos. NAO registra nada no mapa (ato da gerencia: `rotas.py registrar`); os artefatos entram
com o sha256 calculado pela ferramenta quando for registrado.
uso: python -I -B -X utf8 gerar_registro_mapa.py"""
import json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__)); V = os.path.dirname(HERE); sys.path.insert(0, V)
import delta19_v394 as DL  # noqa: E402
J = lambda *p: json.load(open(os.path.join(*p), encoding="utf-8"))
CM, ESP, ENS, AX = J(V, "CANDIDATO_v394.json"), J(V, "ESPERADOS_v394.json"), J(V, "ensaio_a_seco_v394.json"), J(HERE, "AXIOMAS_DELTA_19OUT.json")
KD = os.path.join(V, DL.KERNEL_DIR); KH, FL = J(KD, "KH_N1_v394.json"), J(KD, "FLAGS_v394.json")
S = CM["sha16"]; SOMA = J(HERE, "SOMA_TEXTOS_POS_RITO.json"); HD = J(HERE, "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json"); bg = ESP["n_bandeiras_por_grupo"]
R = {
    "tipo": "ROTA",
    "rota_id": "kernel.criterio_binario_de_parada.ponto_fixo_v394_d19",
    "dominio": "KERNEL_FORMAL",
    "titulo": "A leitura binária flutua no ponto fixo (critério binário de parada, cunhagem de 19/10): a pedra candidata TheBinaryReadingAtTheFixedPoint, o registro criterio_binario_de_parada_v394 e a integração final da v394 (candidato d19 %s)" % S,
    "pergunta": "Os oito teoremas do kernel que a cunhagem de 19/10 reúne («a TGL é binária; a leitura de ambos é o resultado; o sistema flutua no ponto fixo») compõem-se por citação, sem matemática nova e dentro do trio? E o candidato v394 integra a pedra, as duas falas, a política de bandeiras só-nomeadas e o pino h8 da árvore do Nós sem mover o gate?",
    "dados": ["Lean 4.31.0 / Mathlib v4.31.0, kernel TGLExt: sandbox FRIO %s (cópia do tgl_kernel do Nós v393 + 190 módulos novos)" % DL.SANDBOX,
              "falas do operador de 19/10/2026 (verbatim por sha256: %s)" % ", ".join(sorted(ESP["criterio_binario"]["verbatim"])),
              "o core v393 SELADO (formal_files_sha256 com 1233 entradas) e a árvore do Nós, só leitura",
              "o EXAME_FINAL_V394.md (a classificação das bandeiras e o achado do h8)"],
    "metodo": "Pedra de composição (um teorema, conjunção de 8 citações; nenhum lema novo) compilada a frio num sandbox novo; axiomas lidos dos logs crus do build e do Audit; registro por spec (motor v392) que lê a bandeira, os 9 nomes no axiom_report do rito e o sha256 das duas falas embutidas, com controles negativos (bandeira falsa, sha errado, citado fora do trio, pedra adulterada); política de bandeiras reproduzida do exame por script; pino h8 recalculado da árvore simulada do Nós; ensaio a seco com as etapas simular_arvore_do_nos e exame_pontos_v394; conferidor com controle negativo. Pré-registrado: nada (a pedra e o registro são fail-closed e não movem o gate).",
    "resultado": "Pedra %s (sha16 %s): axiomas %s, zero sorry, compilada a frio em %s s. Candidato %s (%s B): %d módulos novos, %d bandeiras (%d nomeadas do Codex + %d nomeadas sem bandeira + 1 da pedra; %d auxiliares fora), escada %d/%d, Audit %d/%d/%d, h8 %d entradas (%d embutidas + _check_damming.lean), %d falas embutidas, %d registros por spec; ensaio a seco: %s (%d casos de unidade; simular_arvore_do_nos %d entradas; exame_pontos algum_falso=%s); conferidor (controle negativo, Nós v393): tudo_bate=False como devia. A soma que pos_rito\\textos_v394.py::_d esperava NÃO fechava com a política nova (n_out_flags=%d); a proposta (n_bandeiras_por_grupo) foi aplicada (sha16 %s) e o harness dos textos (os módulos reais contra um Nós emulado do ensaio) passa: %d + %d + %d + %d = %d." % (
        DL.STONE_MOD, AX["pedra"]["sha16"], "/".join(AX["teorema_de_composicao"]["axiomas_no_audit"][0]), AX["compilacao"]["segundos"], S, format(CM["bytes"], ","), CM["kernel"]["modulos_novos"], ESP["n_bandeiras_novas"], FL["por_origem"]["codex_nomeada"], FL["por_origem"]["nomeada_sem_bandeira"],
        FL["excluidas_auxiliares"]["n"] + FL["publicas_sem_bandeira"]["n"], ESP["escada"][1], ESP["escada"][0], KH["linha_TOTAL"]["decl"], KH["linha_TOTAL"]["thm"], KH["linha_TOTAL"]["fora_do_trio"], ESP["h8_entradas"], ESP["formal_files_n"], len(ESP["cunhagens"]), len(ESP["registros_v394"]),
        ENS["veredito"], len(ENS["unidade"]), ENS["simular_arvore_do_nos"]["formal_files_n_no_rito_real"], ENS["exame_pontos"]["algum_falso"], SOMA["formula_original"]["n_out_flags"], HD["textos_sha16"], bg["tempo"], bg["quadratica"], bg["rede"], bg["outros"], sum(bg.values())),
    "veredito": ENS["criterio_binario"]["verdict"],
    "estatuto": "REAL",
    "status": "EXAMINADA",
    "olhou_dados": False,
    "defeito": "O rito real e o caminho positivo do conferidor ainda não foram exercitados (ato da gerência); a pedra não afirma procedimento de decisão e a analogia com o qubit vale nos pesos (1/2, 1/2), não na entropia; a errata da palavra «teoremas» (a escada conta bandeiras: declarações nomeadas, teoremas e definições) entrou no artigo e no texto do kernel, e o rótulo «teoremas limpos» fica como registro de máquina; o harness dos textos e o caminho positivo do conferidor são EMULAÇÃO (só o rito real os exercita); B(n) segue pendente (três pedras sem declaração nomeada). A leitura «a parada é o ponto fixo» é ONTO do operador.",
    "nao_refazer": "A classificação nomeada/auxiliar das bandeiras reproduz o exame número a número; o pino h8 = embutidos + residual reproduz, hash a hash, o formal_files_sha256 do core v393 selado; a pedra compila a frio com o trio e zero sorry. Não repetir sem mudar a pedra ou o kernel.",
    "proximo_passo": "O operador nomeia a pedra; instalar o candidato d19 e rodar o rito (ato da gerência); B(n) e a custódia seguem os passos do ESTADO_V394.",
    "onde": "cadeia_de_selo\\v394: um_v394_candidato_d19.py, delta19_v394.py, gerar_candidato_v394.py, registros_v394.py, pos_build_kernel_v394.py, ensaio_a_seco_v394.py; pedra em delta_19out\\TheBinaryReadingAtTheFixedPoint.lean; textos em pos_rito\\textos_v394.py (proposta aplicada)",
    "artefatos": [os.path.join(HERE, "TheBinaryReadingAtTheFixedPoint.lean"), os.path.join(V, DL.CANDIDATO), os.path.join(V, "ESPERADOS_v394.json"), os.path.join(V, "CANDIDATO_v394.json"), os.path.join(V, "ensaio_a_seco_v394.json"),
                  os.path.join(HERE, "AXIOMAS_DELTA_19OUT.json"), os.path.join(KD, "KERNEL_RECIBO_v394.json"), os.path.join(KD, "FLAGS_v394.json"), os.path.join(V, "SIMULACAO_ARVORE_NOS_%s.json" % S), os.path.join(V, "EXAME_PONTOS_%s.json" % S),
                  os.path.join(V, "conferencia_rito_v394_CONTROLE_NEGATIVO_PRE_RITO.json"), os.path.join(HERE, "SOMA_TEXTOS_POS_RITO.json"), os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_DEPOIS_aplicado.json"), os.path.join(HERE, "HARNESS_TEXTOS_ENSAIO_ANTES_original.json"), os.path.join(HERE, "conferencia_POSITIVO_FALSO_NOS.json"), os.path.join(V, "pos_rito", "textos_v394.py"), os.path.join(HERE, "RESULTADO_DELTA_19OUT.md")],
    "refs": ["formal.tempo_consumacao_leitura_15out", "kernel.pedra_final.espelhamento_j", "kernel.regra_matriz.cadeia_unica"],
    "nota": "Em nome próprio da gerência c1 (subagente), 19/10/2026. O candidato em exame 4022ad521dc7293d fica como registro. Nada foi instalado; o rito não rodou; o Nós, o túnel, a Bancada, o quadro, o mapa, a memória, o site e o git não foram tocados. NOT_FALSIFIED nunca é a palavra da creditação; validade no kernel não é creditação; o gate não se move.",
}
json.dump(R, open(os.path.join(HERE, "registro_mapa_delta_19out.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({k: (v if isinstance(v, (bool, str)) and len(str(v)) < 120 else "...") for k, v in R.items()}, ensure_ascii=False)[:900])

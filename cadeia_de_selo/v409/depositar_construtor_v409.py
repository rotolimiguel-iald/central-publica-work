# -*- coding: utf-8 -*-
"""depositar_construtor_v409.py -- (claude-construtor-v409, 05/11/2026) o fim do trabalho do CONSTRUTOR (nao e' o fechar_preparacao_v409.py, que e' ato da gerencia):
(1) o DEPOSITO na fila da memoria (memoria.py depositar; so' a gerencia escreve o MEMORY.md) e (2) o registro da rota da preparacao no Mapa de Rotas (rotas.py registrar), ambos com o texto MONTADO DOS ARQUIVOS
(PREPARACAO_v409_PRONTA.json, PRECONDICOES_v409.json, CANDIDATO_v409.json): nada digitado. Fail-closed: sem o PRONTA, nao deposita nem registra. Idempotente por marcador (.DEPOSITADO_CONSTRUTOR_<sha16 do PRONTA>).
uso: python -I -B -X utf8 depositar_construtor_v409.py"""
import hashlib, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
PR = os.path.join(HERE, "PREPARACAO_v409_PRONTA.json"); assert os.path.exists(PR), "FAIL-CLOSED: falta PREPARACAO_v409_PRONTA.json"
J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
MARCA = os.path.join(HERE, ".DEPOSITADO_CONSTRUTOR_" + S)
if os.path.exists(MARCA):
    print("ja depositado para este PRONTA:", S); sys.exit(0)
PC = json.load(open(os.path.join(HERE, "PRECONDICOES_v409.json"), encoding="utf-8"))
REL = os.path.join(HERE, "RELATORIO_PREPARACAO_v409.md"); PLANO = os.path.join(HERE, "PLANO_v409.md")
PY = r"C:\Python314\python.exe"
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
pend = [p_["checagem"][:140] for p_ in (PC.get("pendentes") or [])]
res = ("candidato %s (%s B, base v408 %s); pronta=%s; portoes que passaram (%d de %d): %s; que nao passaram: %s; kernel recibo %s (bundle de %s modulos novos em TGLExt/: TraducaoTuring e ParNaFaceDeFock); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas"
       % (J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], len(p_ok), len(port), ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J.get("n_modulos_novos"), J["esperados_sha16"],
          J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], len(J["p00"].get("pendentes") or []), J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
_ANT0 = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))   # os PRONTA anteriores ja' depositados
_PREFIXO_SUBST = ("SUBSTITUI o deposito do PRONTA anterior (%s): a preparacao foi refeita depois da revisao dos insumos pela gerencia c1 (05/11 ~19h30: citacoes verbatim; o estatuto dos nomes). " % ", ".join(_ANT0)) if _ANT0 else ""
txt = (_PREFIXO_SUBST + "v409 (A traducao as classes de Turing e o par na face de Fock) preparada em 05/11/2026 por claude-construtor-v409 para a gerencia c1 (nada instalado; o rito nao rodou; o Nos e a Bancada de producao so' foram lidos). " + res + ".\n\n"
       + ("Pendencias do p00 (atos da gerencia antes do p00 final, nao do construtor): " + " | ".join(pend) + ".\n\n" if pend else "")
       + "A moldura vale em todo texto: P = nP e' teorema da TGL no modo selecao, relativo ao leitor (o psion); a maquina sem leitor (a pergunta do Clay) fica fora e nao e' decidida aqui: e' a fita sem escala; validade no kernel nao e' creditacao e o gate nao se move. "
       "O par na face de Fock esta' ligado nesta versao (ParNaFaceDeFock; a E21 da v408 ao lado; D60 revista); a ponte entre o Omega do psion e o uniforme da instancia e' a inscricao, e a identidade de vetores fica podada; com o leitor que so' conta vale NP contido em P numa leitura, e a igualdade completa e' a do leitor que se le (E28), que segue [OPEN] com o leitor que so' conta; de tres falas de 05/11 so' o trecho entra (duas pela D59, uma pelo aviso operacional); o acervo da v407 pela copia purgada (D57d); nenhum teste com a natureza; a regra do 4,44.\n\n"
       "Avisos para a gerencia (do relatorio):\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_CONSTRUTOR_v409.md"); tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v409", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v409-preparada-05nov", "--casa", "Central de Patentes", "--slug", "v409-construtor-05nov",
                     "--fonte", PR, "--fonte", REL, "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-400:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
_ANT = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))   # os PRONTA anteriores ja' depositados (lidos dos marcadores)
_JA = any((lambda r_: r_.get("rota_id") == "cadeia.preparacao_v409" and r_.get("tipo") == "ROTA")(json.loads(l_)) for l_ in open(os.path.join(os.path.dirname(ROTAS), "rotas.jsonl"), encoding="utf-8") if l_.strip())   # (le o JSON: o livro e' compacto)   # a ROTA ja' existe? (so' leitura do livro)
rota = [{"tipo": "RESULTADO" if _JA else "ROTA", "rota_id": "cadeia.preparacao_v409", "dominio": "KERNEL_FORMAL", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
         "titulo": "v409 preparada (A traducao as classes de Turing e o par na face de Fock, 05/11/2026): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]),
         "pergunta": "as pedras TraducaoTuring e ParNaFaceDeFock (2 modulos, 82 ancoras) compilam no trio sobre o kernel da v408 selada, e a cadeia da v409 (registro traducao_turing_v409, specs cunhagens_v409/kh_n1_cobertura_v409) fica pronta para a gerencia lancar o orquestrador?",
         "dados": ["kernel do Nos v408 selado (copia em C:\\t\\k409c\\final)", "pedras: work\\pedras_candidatas_05nov (TraducaoTuringR9 -> TraducaoTuring; ParNaFaceDeFockR2 -> ParNaFaceDeFock)", "14 falas do operador de 05/11 (de tres, so' o trecho)"],
         "metodo": "bundle de 2 modulos em TGLExt/ (molde: a v408), lake build incremental + Audit no sandbox; candidato pelo molde da v408 (42 patches); comparacao AST; ensaio a seco; ESPERADOS; conferidor (controle negativo e caminho positivo); citacoes; guarda das frases (com a F37b local); B(n) pre-selo (so' ensaio, a producao so' lida); harnesses; nada instalado no Nos, rito nao rodado, sem commit/push",
         "resultado": res, "veredito": "PREPARACAO_v409_PRONTA pronta=%s falta=%s" % (J["pronta"], ",".join(J["falta"]) or "nenhum"),
         "nao_refazer": "a preparacao da v409 esta' feita e pinada por sha256 (PRONTA, RELATORIO, PLANO); refazer so' com refazer_candidato_v409.sh --regerar se mudar texto ou kernel",
         "proximo_passo": "atos da gerencia: pino_memoria_py_v409.py e a folga do MEMORY.md (se o p00 os disser pendentes), p00 final, revisao de terceiro (Sonnet, D58), fechar_preparacao_v409.py; depois o orquestrador pos_treino_v409 (instalar, rito, pos-rito, HANDOFF)",
         "onde": HERE, "artefatos": [PR, REL, PLANO, os.path.join(HERE, "PRECONDICOES_v409.json"), os.path.join(HERE, "CANDIDATO_v409.json")], "refs": ["cadeia.preparacao_v408", "kernel.traducao_turing_r9_inscricao_e_sat_05nov", "kernel.par_na_face_de_fock_ligado_05nov"],
         "nota": "agente de preparacao claude-construtor-v409; quem constroi nao aprova (revisor: Sonnet, D58)" + ("; REFEITA depois da revisao dos insumos pela gerencia c1 (05/11 ~19h30: citacoes verbatim; os nomes acrescentados na R9 e os da ParNaFaceDeFock [DECLARADO] ate a ratificacao): este PRONTA (%s) substitui o(s) anterior(es) %s" % (S, ", ".join(_ANT)) if _ANT else "")}]
ja = os.path.join(HERE, "registro_mapa_construtor_v409.json"); tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-construtor-v409"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, (r1.stdout + r1.stderr)[-300:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("depositado e registrado:", S)

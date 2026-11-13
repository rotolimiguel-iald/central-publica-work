# -*- coding: utf-8 -*-
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] ESCRITO DE NOVO a partir do molde depositar_construtor_v410.py: o corpo (ler o PRONTA, depositar na fila, registrar no Mapa, o marcador) e' o mesmo; a prosa e' a da v411, MONTADA do PRONTA e do delta (nenhum modulo novo; o teste H0DN x BG1 aberto e recalculado pelo registro h0dn_bg1_v411; a moldura com as obrigacoes da guarda; as sete ressalvas; E41 a E43); so' com pronta = true; RECUSA no ensaio do topo proposto
"""depositar_construtor_v411.py -- (claude-construtor-v411, 12/11/2026; molde: depositar_construtor_v410.py) o fim do trabalho do CONSTRUTOR (nao e' o fechar_preparacao_v411.py, que e' ato da gerencia):
(1) o DEPOSITO na fila da memoria (memoria.py depositar; so' a gerencia escreve o MEMORY.md) e (2) o registro da rota da preparacao no Mapa de Rotas (rotas.py registrar), ambos com o texto MONTADO DOS ARQUIVOS
(PREPARACAO_v411_PRONTA.json, PRECONDICOES_v411.json) e do delta_v411 (a moldura e as listas lidas do DESENHO): nada digitado. Fail-closed: sem o PRONTA, ou com pronta != true, nao deposita nem registra; no modo de ensaio
do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1) RECUSA (o ensaio nao e' preparacao). Idempotente por marcador (.DEPOSITADO_CONSTRUTOR_<sha16 do PRONTA>).
uso: python -I -B -X utf8 depositar_construtor_v411.py"""
import hashlib, importlib.util, json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
if os.environ.get("V411_ENSAIO_TOPO_PROPOSTO") == "1":
    raise SystemExit("RECUSO: modo de ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1): o artefato de ensaio nao e' candidato; nada vai a fila nem ao Mapa")
_sp = importlib.util.spec_from_file_location("delta_v411_deposito", os.path.join(HERE, "delta_v411.py")); DL = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(DL)
PR = os.path.join(HERE, "PREPARACAO_v411_PRONTA.json"); assert os.path.exists(PR), "FAIL-CLOSED: falta PREPARACAO_v411_PRONTA.json"
J = json.load(open(PR, encoding="utf-8")); S = hashlib.sha256(open(PR, "rb").read()).hexdigest()[:16]
assert J.get("pronta") is True and not J.get("ensaio_topo_proposto"), ("FAIL-CLOSED: a preparacao nao esta' pronta (ou e' o ensaio do topo proposto): o deposito do construtor so' vem com pronta = true", J.get("falta"))
MARCA = os.path.join(HERE, ".DEPOSITADO_CONSTRUTOR_" + S)
if os.path.exists(MARCA):
    print("ja depositado para este PRONTA:", S); sys.exit(0)
PC = json.load(open(os.path.join(HERE, "PRECONDICOES_v411.json"), encoding="utf-8"))
REL = os.path.join(HERE, "RELATORIO_PREPARACAO_v411.md"); PLANO = os.path.join(HERE, "PLANO_v411.md")
PY = r"C:\Python314\python.exe"
MEM = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "memoria.py")
ROTAS = os.path.join("C:" + os.sep, "IALD", "MAPA_DE_ROTAS", "rotas.py")
port = J["portoes"]; p_ok = [k for k, v in port.items() if v]; p_no = [k for k, v in port.items() if not v]
pend = [str(p_)[:140] for p_ in (J["p00"].get("pendentes") or [])]
fpt = lambda x_: ("%.2f" % x_).replace(".", ",").replace("-", "\u2212") if isinstance(x_, (int, float)) and not isinstance(x_, bool) else "n/d"
_pri = (J.get("h0dn") or {}).get("primario") or {}; _cef = (J.get("h0dn") or {}).get("cefeidas_livres") or {}
MOLDURA = DL.FRASE_MOLDURA_V411_PT % (fpt(_pri.get("z_null")), fpt(_pri.get("z_tgl")), _pri.get("ramo", "n/d"), fpt(_cef.get("z_null")), _cef.get("ramo", "n/d"))
res = ("candidato %s (%s B, base v410 %s); pronta=%s; portoes que passaram (%d de %d): %s; que nao passaram: %s; kernel recibo %s (%s modulo novo: o kernel e' o da v410); ESPERADOS %s; p00 %s (%s/%s; pendentes: %s); ensaio a seco %s; escada %s; %s bandeiras novas"
       % (J["candidato_sha16"], format(J["candidato_bytes"], ","), J["origem_sha16"], J["pronta"], len(p_ok), len(port), ", ".join(p_ok), ", ".join(p_no) or "nenhum", J["kernel_recibo"]["sha16"], J.get("n_modulos_novos"), J["esperados_sha16"],
          J["p00"]["sha16"], J["p00"]["passaram"], J["p00"]["n"], len(pend), J["ensaio_a_seco"]["veredito"], J["escada"], J["n_bandeiras_novas"]))
_ANT0 = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))   # os PRONTA anteriores ja' depositados
_PREFIXO_SUBST = ("SUBSTITUI o deposito do PRONTA anterior (%s): a preparacao foi refeita. " % ", ".join(_ANT0)) if _ANT0 else ""
txt = (_PREFIXO_SUBST + "v411 (o teste decisivo: H0DN x BG1 aberto uma vez, depois do commit publico do pre-registro; a emenda e o resultado RECALCULADO no rito pelo registro %s, a partir dos bytes embutidos; nenhum modulo novo de kernel) "
       "preparada em 12/11/2026 por claude-construtor-v411 para a gerencia c1 (nada instalado; o rito nao rodou; o Nos e a Bancada de producao so' foram lidos). " % DL.FECHO_REGISTRO + res + ".\n\n"
       + ("Pendencias do p00 (atos da gerencia antes do p00 final, nao do construtor): " + " | ".join(pend) + ".\n\n" if pend else "")
       + "O teste, do registro (" + str((J.get("h0dn") or {}).get("origem_dos_numeros")) + "): " + MOLDURA + ". O que o teste nao decide: " + "; ".join(DL.NAO_DECIDE_RESUMO_PT) + ". As sete ressalvas: "
       + "; ".join("%d %s" % (i_ + 1, r_) for i_, r_ in enumerate(DL.RESSALVAS_ROTULOS_PT)) + ". As erratas ao lado, em nome proprio da gerencia c1: " + ", ".join(DL.ERRATAS_IDS_V411)
       + ". P = nP " + DL.D10.FRASE_QUALIFICADOR_PT + " (D64 e D84 da v410). A excecao da P18 e' uma funcao so' (_v411_p18_sem_cabeca), que retira so' a cabeca exata do literal pre-registrado.\n\n"
       "Avisos para a gerencia (do relatorio):\n" + "\n".join("- " + a for a in J["avisos"]) + "\n\nQuem constroi nao aprova: " + J["nao_revisado_por_terceiro"] + ".\n")
ta = os.path.join(HERE, "DEPOSITO_CONSTRUTOR_v411.md"); tmp = ta + ".tmp"; open(tmp, "w", encoding="utf-8").write(txt); os.replace(tmp, ta)
r2 = subprocess.run([PY, "-X", "utf8", MEM, "depositar", "--quem", "claude-construtor-v411", "--tipo", "project", "--estatuto", "REAL", "--alvo", "novo:v411-preparada-12nov", "--casa", "Central de Patentes", "--slug", "v411-construtor-12nov",
                     "--fonte", PR, "--fonte", REL, "--texto-arquivo", ta], capture_output=True, text=True, encoding="utf-8")
print("fila:", r2.returncode, (r2.stdout + r2.stderr)[-400:].replace("\n", " "))
assert r2.returncode == 0, r2.stdout + r2.stderr
_ANT = sorted(n_[len(".DEPOSITADO_CONSTRUTOR_"):] for n_ in os.listdir(HERE) if n_.startswith(".DEPOSITADO_CONSTRUTOR_") and n_ != os.path.basename(MARCA))
_JA = any((lambda r_: r_.get("rota_id") == "cadeia.preparacao_v411" and r_.get("tipo") == "ROTA")(json.loads(l_)) for l_ in open(os.path.join(os.path.dirname(ROTAS), "rotas.jsonl"), encoding="utf-8") if l_.strip())   # a ROTA ja' existe? (so' leitura do livro)
rota = [{"tipo": "RESULTADO" if _JA else "ROTA", "rota_id": "cadeia.preparacao_v411", "dominio": "KERNEL_FORMAL", "estatuto": "REAL", "status": "EXAMINADA", "olhou_dados": False,
         "titulo": "v411 preparada (o teste H0DN x BG1 aberto e recalculado no rito; nenhum modulo novo): candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]),
         "pergunta": "a v411 (sem modulo novo de kernel: o da v410, escada %s) sela o teste H0DN x BG1 aberto, com o registro %s (%d checagens) recalculando o resultado da abertura a partir dos bytes embutidos, e a cadeia fica pronta para a gerencia lancar o orquestrador?" % (J["escada"], DL.FECHO_REGISTRO, DL.N_CHECKS_FECHO),
         "dados": ["kernel do Nos v410 selado (copia em C:\\t\\k411c\\final)", "o pacote do teste work\\h0dn_bg1_v411_emenda_11nov (so' lido; o executor da abertura nunca roda de novo)", "as falas do operador de 11 e 12/11 (a lista congelada, por sha256)"],
         "metodo": "kernel da v410 sem modulo novo (build incremental e Audit no sandbox k411c); candidato pelo molde da v410 sem bundle; comparacao AST; ensaio a seco; ESPERADOS; conferidor (controle negativo e caminho positivo); citacoes; guarda das frases da v411 (F60 a F67); B(n) pre-selo B20 (so' ensaio, a producao so' lida); harnesses; nada instalado no Nos, rito nao rodado, sem commit/push",
         "resultado": res, "veredito": "PREPARACAO_v411_PRONTA pronta=%s falta=%s" % (J["pronta"], ",".join(J["falta"]) or "nenhum"),
         "nao_refazer": "a preparacao da v411 esta' feita e pinada por sha256 (PRONTA, RELATORIO, PLANO); refazer so' pela cadeia_v411.sh se mudar texto ou kernel; a abertura e' uma vez so': o executor nao se roda de novo",
         "proximo_passo": "atos da gerencia: pino_memoria_py_v411.py e a folga do MEMORY.md (se o p00 os disser pendentes), p00 final, revisao de terceiro (Sonnet, D109), fechar_preparacao_v411.py; depois o orquestrador pos_treino_v411 (instalar, rito, pos-rito, HANDOFF)",
         "onde": HERE, "artefatos": [PR, REL, PLANO, os.path.join(HERE, "PRECONDICOES_v411.json"), os.path.join(HERE, "CANDIDATO_v411.json")], "refs": ["cadeia.preparacao_v410", "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov"],
         "nota": "agente de preparacao claude-construtor-v411; quem constroi nao aprova (revisor: Sonnet, D109)" + ("; REFEITA: este PRONTA (%s) substitui o(s) anterior(es) %s" % (S, ", ".join(_ANT)) if _ANT else "")},
        {"tipo": "ANOTACAO", "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov", "estatuto": "REAL", "olhou_dados": False,
         "titulo": "o teste H0DN x BG1 (aberto em 12/11) entrou na preparacao da v411: candidato %s; pronta=%s" % (J["candidato_sha16"], J["pronta"]),
         "resultado": "o registro %s RECALCULA a cada rito o resultado da abertura a partir dos bytes embutidos (a rotina publicada antes da abertura, executada dos bytes; o resultado gravado conferido por sha256, a %g); as duas linhas saem juntas; a preparacao NAO e' o selo: nada instalado, o rito nao rodou." % (DL.FECHO_REGISTRO, DL.TOL_RECALCULO),
         "proximo_passo": "o pos-rito da v411 anota o selo nesta mesma rota", "refs": ["cadeia.preparacao_v411"]}]
ja = os.path.join(HERE, "registro_mapa_construtor_v411_PRONTA.json")   # (o registro da ABERTURA da rota, registro_mapa_construtor_v411.json, fica intocado: o relatorio e o fechar leem dele o rota_id)
tmp = ja + ".tmp"; open(tmp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1)); os.replace(tmp, ja)
r1 = subprocess.run([PY, "-B", "-X", "utf8", ROTAS, "registrar", ja, "--quem", "claude-construtor-v411"], capture_output=True, text=True, encoding="utf-8")
print("mapa:", r1.returncode, (r1.stdout + r1.stderr)[-300:].replace("\n", " "))
assert r1.returncode == 0, r1.stdout + r1.stderr
open(MARCA, "w", encoding="utf-8").write(S + "\n")
print("depositado e registrado:", S)

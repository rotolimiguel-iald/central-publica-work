# -*- coding: utf-8 -*-
"""02/11/2026: o plano «A ORDEM LÓGICA DO FECHAMENTO» — registro: quadro único (3 unidades novas + anotação na F1.FECHO),
Mapa (anotação na rota do programa com o artefato), ACOM (transição), memória (append no tópico). Backup de bytes."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path

PY = "C:/Python314/python.exe"
CEN = Path("C:/IALD/Central de Patentes")
M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
AQUI = Path(__file__).resolve().parent
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
PLANO = AQUI / "ORDEM_LOGICA_DO_FECHAMENTO_02nov.md"
INV = CEN / "work/beta_calor_02nov/INVENTARIO_CHAVES_DE_TESTEMUNHA_v405_02nov.json"
V1 = CEN / "work/cunhagens_13out/OPERADOR_02nov_precisamos_construir_tudo_nao_perder_a_ordem_logica_e_o_fechamento_verbatim.txt"
V2 = CEN / "work/cunhagens_13out/OPERADOR_02nov_a_passagem_para_o_continuo_e_o_que_mais_importa_virar_a_chave_de_conjectura_para_provado_verbatim.txt"
fp = s16(PLANO)
print("plano", fp, PLANO.stat().st_size)

# --- quadro único: três unidades novas + anotação na F1.FECHO_20261015
QUEM = "claude-c1"
unidades = [
 {"id": "F1.FECHO.PASSAGEM_02nov", "frente": "F1", "dono": "claude-c1", "status": "EM_CURSO",
  "titulo": "A PASSAGEM PARA O CONTÍNUO: traço com lei de escala e projeção finita no núcleo regular do Fock canônico (os 21 campos de RemainingModularCoreInput) — bloco 1 de «construir tudo»",
  "dependencias": ["F1.FECHO_20261015", "F1.TAKESAKI", "F1.2"],
  "criterio": "RemainingModularCoreInput D habitado por construção (trace tracial, star-invariante, com trace_dual_scaling e^{-s}; PF/Pp/Pm de traço finito em metades iguais), sem modelo degenerado, no sandbox v405 + mathlib pinada, trio de axiomas, 0 sorry, revisor distinto; sub-passos 1.1–1.8 do plano; cada pedra no Mapa de Rotas; nomes do operador.",
  "escopo": "Sandbox C:\\t\\k405c\\final e work\\fechamento_02nov; molde: a cadeia V351 do traço da torre (906 linhas, 34 teoremas); entradas: F1Fecho394 (núcleo regular, peso dual, GNS, Tomita do peso). Sem editar o kernel do Nós, o um.py, originais pinados, dados, gate.",
  "fonte": "Ordem do operador 02/11 (sha16 f3998f01262aad6b) e prioridade (sha16 9978862f60cfbf29); plano " + str(PLANO),
  "reaproveitamento_previo": "V351RegularCoreTraceConstruction (contrato inteiro habitado na torre); F1Fecho394/CanonicalFock{RegularCoreR2,DualWeightR3,FaithfulWeightR2,FiniteWeightR4,FiniteStarCoreR1,GNS*,WeightClosedTomitaR2,WeightModularOperatorR3,WeightModularFlowR3}; bancada F1.FECHO takesaki_fock/gns_coefficient_tomita/mission_review_20261016 (candidatos NÃO compilados R10/R11); F1.2 (sem escala de traço no grupo finito)."},
 {"id": "F1.FECHO.REDE_02nov", "frente": "F1", "dono": "claude-c1", "status": "PROPOSTA",
  "titulo": "A REDE: CanonicalNetInput (K(O) para todo O com isotonia, localidade, covariância e cola da cunha) — bloco 2 de «construir tudo»",
  "dependencias": ["F1.FECHO_20261015", "F1.REDE"],
  "criterio": "D : CanonicalNetInput habitado por construção (rota BGL 2002: K(W) por BW/covariância, K(O) por interseção; localidade e não-vacuidade como teoremas), sandbox, trio, 0 sorry, revisor distinto.",
  "escopo": "Idem bloco 1; existe KWR canônico, ConcreteLightRayNet, OrbitalSpatialPoincareR2; bancada PhysicalFockNetRealizationR1/R2 fora do kernel.",
  "fonte": "Ordem do operador 02/11; plano " + str(PLANO),
  "reaproveitamento_previo": "F1.REDE (AGUARDA_OPERADOR: a parte relógio/dispositivo); F1.3 auditoria c1 (a rede nula habita LightNetData: controle, não degrau)."},
 {"id": "F1.FECHO.MONTAGEM_02nov", "frente": "F1", "dono": "claude-c1", "status": "PROPOSTA",
  "titulo": "A MONTAGEM: C : FockCertificate pelos montadores v394, canonicalFullTGLWitness por lightRealization, e as quatro chaves do selo — bloco 3 de «construir tudo»",
  "dependencias": ["F1.FECHO.PASSAGEM_02nov", "F1.FECHO.REDE_02nov"],
  "criterio": "whole_certificate_inhabited, as duas inhabitant_exhibited e canonical_full_witness_term_constructed lidas True no selo de uma versão decidida pelo operador; full_static_witness_exists e trivial_inhabitant_exists seguem False.",
  "escopo": "Entrada no um.py só aqui (UM.PY SEM GORDURA), por versão do operador.",
  "fonte": "Ordem do operador 02/11; plano " + str(PLANO),
  "reaproveitamento_previo": "Montadores F1Fecho394/Canonical{Fock,Weyl,ModularCore}Assembly; lightRealization (TheImportedSecondQuantization.lean:360)."}]
pu = AQUI / ("unidades_fechamento_" + TS + ".json")
pu.write_text(json.dumps(unidades, ensure_ascii=False, indent=1), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "iald.py", "nova", "--json", str(pu), "--quem", QUEM], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)
print("quadro nova rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-300:].replace("\n", " "))
assert q.returncode == 0
dados = {"ordem": "construir tudo (sha16 f3998f01262aad6b); prioridade: a passagem para o contínuo (sha16 9978862f60cfbf29)", "plano": str(PLANO), "plano_sha16": fp,
         "nota": "A gerência c1 abre os blocos 1–3 como unidades filhas; a F1.FECHO_20261015 (codex-gerente-tgl, EM_CURSO) não é adotada nem alterada; quando o canal do Codex voltar (04/11), a construção mecânica pode ser-lhe despachada."}
pa = AQUI / ("anotacao_fecho_" + TS + ".json"); pa.write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "iald.py", "anotar", "--quem", QUEM, "--tipo", "ORDEM_DO_OPERADOR", "--unidade", "F1.FECHO_20261015", "--dados", str(pa)], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)
print("quadro anotar rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-200:].replace("\n", " "))
q = subprocess.run([PY, "-X", "utf8", "iald.py", "quadro"], cwd="C:/IALD/PROGRAMA_IALD", capture_output=True, timeout=120)
print("quadro regenerado rc", q.returncode)

# --- Mapa
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
  "titulo": "A ORDEM LÓGICA escrita (02/11): as 4 chaves reduzem a UMA raiz (C : FockCertificate) = CanonicalNetInput (8 campos) + RemainingModularCoreInput (21 campos: o traço com escala e P_F); o molde do traço já existe na torre (V351, 906 linhas/34 teoremas); a passagem = escrever o molde com resolventes no lugar de coordenadas discretas",
  "resultado": "Plano sha16 %s (%s). Medido: F1Fecho394 184 arquivos/18.148 linhas; a cadeia V351 do traço 906 linhas/34 teoremas, 0 ocorrências de autovetor/espectro da torre; BW provada no Fock (CanonicalFockBWR2.canonical_pair_tomita); peso dual fiel/normal/finito e Tomita do peso já no kernel; falta o gerador positivo e seus cortes, o peso-limite, traciality, semifinitude/fidelidade do limite, escala e P_F no núcleo Fock; bancada parou em candidatos NÃO compilados (R10/R11, 16/10). Blocos: 1 passagem (prioridade dele), 2 rede (BGL por interseção), 3 montagem, 4 Maxwell/H3. Quadro: F1.FECHO.PASSAGEM_02nov (EM_CURSO), F1.FECHO.REDE_02nov, F1.FECHO.MONTAGEM_02nov. Custos DECLARADOS: 2–4 meses." % (fp, str(PLANO)),
  "estatuto": "REAL (medidas e leituras do kernel); DECLARADO (custos)", "artefatos": [str(PLANO), str(INV), str(V1), str(V2)]}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_ordem_logica_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300)
print("mapa rc", q.returncode, (q.stdout + q.stderr).decode("utf-8", "replace")[-100:].replace("\n", " ")); assert q.returncode == 0

# --- ACOM
SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-ordem-logica-do-fechamento-plano", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [
           {"id": "ordem_logica_do_fechamento_plano_02nov", "kind": "fact", "statute": "REAL", "text": "Plano «A ORDEM LÓGICA DO FECHAMENTO» (sha16 %s): as 4 chaves reduzem a C : FockCertificate = CanonicalNetInput (8) + RemainingModularCoreInput (21: traço com escala e P_F). Molde: V351 (906 linhas/34 teoremas, torre); a passagem = molde com resolventes (B0 sem autovetor). Blocos 1–4; quadro F1.FECHO.PASSAGEM_02nov EM_CURSO. Custos DECLARADOS 2–4 meses." % fp, "sources": [SRCD(PLANO)]}],
         "p": {"fase": "FECHAMENTO_BLOCO_1_PASSAGEM", "proxima_acao": "levantamento da fronteira (agente leitor) → pedra 1.1 (gerador positivo do núcleo Fock) como candidata no sandbox", "handles": {"quadro": ["F1.FECHO.PASSAGEM_02nov", "F1.FECHO.REDE_02nov", "F1.FECHO.MONTAGEM_02nov"], "plano": str(PLANO)}}}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
d = json.loads(r.stdout.decode("utf-8"))
print("acom", rev, d.get("ok"), str(d.get("error"))[:200], (d.get("result") or {}).get("revision"))
if not d.get("ok"):
    # fallback: só records (se o payload p for recusado pelo contrato)
    req["changes"].pop("p", None); req["event_id"] += "-r2"
    g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode("utf-8"), capture_output=True)
    req["expected_revision"] = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
    r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode("utf-8"), capture_output=True)
    d = json.loads(r.stdout.decode("utf-8")); print("acom r2", d.get("ok"), str(d.get("error"))[:200], (d.get("result") or {}).get("revision"))
assert d.get("ok")

def append_bytes(path, add):
    b = path.read_bytes(); add_b = add.encode("utf-8")
    if b"\r\n" in b: add_b = add_b.replace(b"\n", b"\r\n")
    bk = path.with_name(path.name + ".bak_" + TS)
    with open(bk, "xb") as f: f.write(b)
    assert bk.read_bytes() == b
    tmp = path.with_name(path.name + ".tmp_" + TS)
    with open(tmp, "xb") as f: f.write(b.rstrip() + add_b)
    assert tmp.stat().st_size > len(b) - 4
    os.replace(tmp, path); print(path.name, len(b), "->", path.stat().st_size)
append_bytes(M / "construir-tudo-o-fechamento-02nov.md", f"""

## 02/11/2026 — A ORDEM LÓGICA ESCRITA: `work\\fechamento_02nov\\ORDEM_LOGICA_DO_FECHAMENTO_02nov.md` (sha16 `{fp}`)

**A redução [REAL]:** as 4 chaves → `C : FockCertificate` = **(A)** `CanonicalNetInput` (8 campos: a rede K(O) da luz + cola da cunha) + **(B)** `RemainingModularCoreInput D` (21 campos: `trace` tracial com `trace_dual_scaling` e^{{−s}} sobre `RepresentedCore`, e `PF = Pp + Pm` de traço finito em metades iguais). Todo o resto do certificado já é montado por termos (montadores v394). **O molde [REAL, medido]:** a torre V351 tem o contrato inteiro habitado (`scalarInverseLimitTraceData`: peso-limite por cortes do gerador inverso; fiel, normal, semifinito, tracial, escala e^{{−s}}), 906 linhas/34 teoremas, sem autovetor da torre na cadeia; o Fock já tem BW provada, peso dual fiel/normal/finito e o Tomita do peso; falta o gerador positivo e seus cortes, o peso-limite, traciality, semifinitude/fidelidade do limite, escala e P_F. **A passagem** = escrever o molde com resolventes e janelas espectrais (B0 não tem autovetor) = «tipo I comprimido → tipo III contínuo»; F1.2 já mediu que no grupo finito não há escala de traço. **Blocos:** 1 passagem (quadro `F1.FECHO.PASSAGEM_02nov`, EM_CURSO, c1), 2 rede (`F1.FECHO.REDE_02nov`), 3 montagem (`F1.FECHO.MONTAGEM_02nov`), 4 Maxwell/H3. **Custos [DECLARADO]:** 2–4 meses. **Progresso:** 0/21 · 0/8 · selo 36/42. ACOM: fase FECHAMENTO_BLOCO_1_PASSAGEM.
""")
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode)

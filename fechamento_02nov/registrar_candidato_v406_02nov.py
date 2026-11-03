# -*- coding: utf-8 -*-
"""02/11/2026, 20:5x: o candidato v406 foi gerado (bundle de 301 + fechamento_v406) e o pos-build do k406c esta' verde. Registra: Mapa (anotacao na rota do programa), ACOM (transition), memoria (append no topico do fechamento, com a correcao
ao lado do caminho colapsado do append anterior). Backup de bytes; nada no kernel do Nos. Escrito pelo Write (nao por heredoc: a barra invertida colapsa no heredoc do Bash)."""
import datetime, hashlib, json, os, subprocess
from pathlib import Path
PY = "C:/Python314/python.exe"; CEN = Path("C:/IALD/Central de Patentes"); M = Path(os.path.expanduser("~/.claude/projects/c--IALD-Central-de-Patentes/memory"))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S"); BK = chr(92)
s16 = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()[:16]
V6 = CEN / "work/cadeia_de_selo/v406"
cand = json.loads((V6 / "CANDIDATO_v406.json").read_text(encoding="utf-8"))
pb = json.loads((V6 / "kernel/POS_BUILD_v406.json").read_text(encoding="utf-8"))
kh = json.loads((V6 / "kernel/KH_N1_v406.json").read_text(encoding="utf-8"))
assert cand["sha16"] == s16(V6 / "um_v406_candidato.py") and cand["n_bandeiras"] == 1794 and cand["escada"] == [10066, 11860], cand["sha16"]
sinais = pb.get("sinais") or pb.get("checagens") or []
n_falhas = sum(1 for s in sinais if s.get("ok") is False)
tempos = {"build_s": kh.get("duracao_build_s"), "audit_s": kh.get("duracao_audit_s"), "decl": kh["linha_TOTAL"]["decl"], "thm": kh["linha_TOTAL"]["thm"], "fora_do_trio": kh["linha_TOTAL"]["fora_do_trio"]}
print("candidato", cand["sha16"], "pos_build falhas", n_falhas, tempos)
reg = [{"tipo": "ANOTACAO", "rota_id": "kernel.fechamento_construir_tudo_programa_02nov", "dominio": "KERNEL_FORMAL",
        "titulo": "v406: kernel do sandbox k406c construido (build 1736 s, Audit 280 s, rc 0/0; 1794 bandeiras; escada 10066->11860; TOTAL %d/%d/0; 8 ancoras no trio) e candidato gerado (sha16 %s, 32 patches): as quatro chaves de testemunha viram leitura do kernel; ensaio a seco e conferidor em adaptacao (Sonnet)" % (tempos["decl"], tempos["thm"], cand["sha16"]),
        "pergunta": "O fechamento entra no um.py sem mover o gate e com as ressalvas ditas?",
        "dados": [str(V6 / "CANDIDATO_v406.json"), str(V6 / "kernel/POS_BUILD_v406.json"), str(V6 / "kernel/KH_N1_v406.json"), str(V6 / "kernel/FLAGS_v406.json")], "olhou_dados": True,
        "metodo": "preparar_bundle (301 modulos normalizados da integracao R3 + candidata) -> lake build incremental + Audit no k406c (tarefa agendada) -> pos_build_kernel_v406.py (40 sinais) -> gerar_candidato_v406.py (delta/registros/runtime autorais da gerencia; 32 patches; guardas P18 e de frases; gate assertado byte a byte).",
        "resultado": "candidato um_v406_candidato.py sha16 %s (42,7 MB); FLAGS 1794 so' nomeadas; timeout do rito NAO muda (build 1736 s < 2400); os literais False de rede_fock_v394/psibit_v395/testemunha_estatica_v396 viram _v406_certificado_habitado(kf) com errata E14 ao lado; specs u4/u3-u4/u3-u5/x_i versionados (E17); registros fechamento_v406, cunhagens_v406, kh_n1_cobertura_v406." % cand["sha16"],
        "veredito": "CANDIDATO_GERADO__ENSAIO_A_SECO_PENDENTE", "estatuto": "REAL (build e geracao medidos); o selo so' depois do rito", "status": "EM_CURSO",
        "proximo_passo": "ensaio a seco (agente A) -> esperados/conferidor/p00 (agente B) -> revisao de terceiro (Sonnet) -> B(n) pre-selo -> instalar + rito (tarefa agendada) -> pos-rito -> G1.",
        "onde": str(V6), "artefatos": [str(V6 / "CANDIDATO_v406.json"), str(V6 / "kernel/POS_BUILD_v406.json"), str(V6 / "CONTRATO_DA_CADEIA_v406.md"), str(V6 / "delta_v406.py"), str(V6 / "runtime_v406.py"), str(V6 / "registros_v406.py")], "refs": []}]
pj = Path(os.environ.get("TEMP", ".")) / ("rotas_v406_candidato_" + TS + ".json"); pj.write_text(json.dumps(reg, ensure_ascii=False), encoding="utf-8")
q = subprocess.run([PY, "-X", "utf8", "C:/IALD/MAPA_DE_ROTAS/rotas.py", "registrar", str(pj), "--quem", "claude-c1 (gerencia, sessao 6da8f00d)"], capture_output=True, timeout=300); print("mapa rc", q.returncode, q.stdout.decode("utf-8", "replace")[-200:].replace("\n", " ")); assert q.returncode == 0
SRCD = lambda p: {"kind": "document", "ref": str(p).replace("/", BK), "sha256": hashlib.sha256(Path(p).read_bytes()).hexdigest()}
REF = str(CEN / "work/cinco_sigma_fora_da_cosmologia_27out/SESSION_REFERENCE_c1_27e28out.json").replace("/", BK)
g = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps({"operation": "get", "reference": REF}).encode(), capture_output=True)
rev = json.loads(g.stdout.decode("utf-8"))["result"].get("revision")
req = {"operation": "transition", "reference": REF, "expected_revision": rev, "event_id": "c1-02nov-v406-candidato-gerado", "actor": {"id": "claude-c1-gerencia", "kind": "agent"},
       "changes": {"records": [{"id": "v406_candidato_gerado_02nov", "kind": "fact", "statute": "REAL", "text": "02/11 20:5x: kernel k406c construido (build 1736 s, Audit 280 s, rc 0/0; 1794 bandeiras; escada 11860; TOTAL %d/%d/0; 8 ancoras no trio) e candidato v406 gerado (sha16 %s, 32 patches). As quatro chaves de testemunha passam a leitura do kernel (E14); specs versionados (E17); gate byte a byte. Ensaio a seco e conferidor em adaptacao por agentes Sonnet." % (tempos["decl"], tempos["thm"], cand["sha16"]),
                                "sources": [SRCD(V6 / "CANDIDATO_v406.json"), SRCD(V6 / "kernel/POS_BUILD_v406.json"), SRCD(V6 / "CONTRATO_DA_CADEIA_v406.md")]}]}}
r = subprocess.run([PY, "-X", "utf8", "C:/IALD/MEMORIA_IALD/session_memory.py"], input=json.dumps(req, ensure_ascii=False).encode(), capture_output=True)
d = json.loads(r.stdout.decode("utf-8")); print("acom", rev, d.get("ok"), (d.get("result") or {}).get("revision")); assert d.get("ok"), d
p = M / "construir-tudo-o-fechamento-02nov.md"; b = p.read_bytes()
add = ("\n\n**02/11, 20:5x — v406: kernel construído e candidato gerado.** k406c: `lake build` incremental 1736 s (< 2400: timeout do rito fica 3600 s), Audit 280 s, rc 0/0, `Build completed successfully (10291 jobs)`; pós-build verde (40 sinais): **1794 bandeiras** `ext_fch406_*`, escada 10066 → **11860**, TOTAL %d/%d/0, as 8 âncoras no trio (`physicalFockCertificate` = `ext_fch406_0199`; `canonicalFullTGLWitness` = `ext_fch406_0397`). Candidato `um_v406_candidato.py` sha16 **`%s`** (42,7 MB, 32 patches; delta/registros/runtime autorais; gate byte a byte). As quatro chaves (`whole_certificate_inhabited`, as duas `inhabitant_exhibited`, `canonical_full_witness_term_constructed`) viram LEITURA do kernel via `_v406_certificado_habitado` (errata E14 ao lado; `reading_v395`/`reading_v396` guardam o texto antigo); specs u4/u3-u4/u3-u5/x_i versionados (E17); `rede_fock_v394` ganha veredito `…JOINT_CERTIFICATE_INHABITED_V406__THREE_JOINT_ITEMS_STILL_OPEN…` (troca dita). Contrato para os scripts da cadeia: `v406\\CONTRATO_DA_CADEIA_v406.md`. Em curso: ensaio a seco (agente A), esperados/conferidor/p00 (agente B). **Correção ao lado** do append das 19:5x acima: o caminho do bundle é `C:\\t\\k406c\\final\\TGLExt\\F1Fecho394` (o heredoc do Bash colapsou as barras; escrever esses registros pelo Write). **How to apply:** antes do rito faltam: ensaio TUDO PASSOU, conferidor (negativo não bate / positivo bate), p00, revisão de terceiro (Sonnet), B(n) pré-selo (B15), `pos_rito\\textos_v406_novo.pysnip` (texto da gerência) e a tarefa agendada do rito." % (tempos["decl"], tempos["thm"], cand["sha16"])).encode("utf-8")
if b"\r\n" in b:
    add = add.replace(b"\n", b"\r\n")
open(p.with_name(p.name + ".bak_" + TS), "xb").write(b); tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(b.rstrip() + add); os.replace(tmp, p); print(p.name, len(b), "->", p.stat().st_size)
v = subprocess.run([PY, "-X", "utf8", "memoria.py", "verificar"], cwd=str(M / "fila"), capture_output=True); print("verificar rc", v.returncode, v.stdout.decode("utf-8", "replace")[-160:].replace("\n", " "))

"""F0.6: cria a unidade no quadro, registra ROTA + RESULTADO no mapa e põe o parágrafo B3 ao lado no PLANO_V392 (backup de bytes)."""
import datetime
import hashlib
import json
import os
import subprocess

D = r"C:\IALD\Central de Patentes\work\bancada_vinculo_12out"
PLANO = r"C:\IALD\PROGRAMA_IALD\exame_12out\J_SINTESE\PLANO_V392.md"
IALD = r"C:\IALD\PROGRAMA_IALD\iald.py"
ROTAS = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
VERB = r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_ordem_memoria_remote_rank_qg_bancada_verbatim.txt"


def sh(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(args, cwd=None):
    r = subprocess.run(["python"] + args, capture_output=True, text=True, encoding="utf-8", cwd=cwd)
    return (r.stdout or "") + (r.stderr or "")


# 1. unidade F0.6 no quadro
print("nova:", run([IALD, "nova", "--json", os.path.join(D, "F0.6_unidade.json"), "--quem", "claude-c1"], cwd=r"C:\IALD\PROGRAMA_IALD").strip()[-200:])

# 2. mapa: ROTA + RESULTADO
arts = [os.path.join(D, n) for n in ("VINCULO_BANCADA_UMPY.md", "sincronizar_bancada.py", "BATERIA_VINCULO.json", "gerar_canais_mcp.py",
                                      "F0.6_unidade.json", "PLANO_V392_paragrafo_B3.md", "ATOS_DO_OPERADOR.md", "PINOS_12out.json")]
base = {
    "rota_id": "infra.bancada_um.sincronizacao_vnnn",
    "dominio": "INFRA",
    "titulo": "O vínculo permanente Bancada Um ↔ um.py: o elo B(n) da cadeia de selo (sincronizar_bancada.py, re-pino, bateria, recibo)",
    "pergunta": "Como fazer cada versão selada do um.py atualizar a Bancada na mesma cadeia, sem deriva e sem gravação sem evento c1?",
    "dados": ["selo um_absoluto_selo.json e um.py v391 (sha16 8e7b9927ceae64b8)", "manifesto B2 da Bancada (54fc9e27e4599c49)", "bateria T01–T17 da frente H_BANCADA"],
    "metodo": "desenho + esboço funcional testado em sandbox contra cópia da Bancada e Nós sintético v392; 7 controles negativos; ordem do operador verbatim (sha16 78ef70e6f9868281)",
    "estatuto": "REAL",
    "olhou_dados": False,
    "onde": D,
    "artefatos": arts,
    "refs": ["infra.bancada_um.adequacao_canonica_persistente", "infra.bancada_um.compatibilidade_v391_09out"],
    "nota": "Ordem do operador de 12/10: a Bancada (o acelerador de partículas simulado) fica sempre vinculada ao um.py. Instalação é a B3 depois do selo da v392, ato do operador.",
}
rota = dict(base, tipo="ROTA", status="EM_CURSO", resultado="desenho entregue; instalação pendente (B3)", veredito="",
            defeito="o canonical.py instalado aceita a primeira linha de α (unicidade só no esboço); serviço HTTP desligado",
            nao_refazer="o desenho e o esboço existem; não redesenhar", proximo_passo="auditoria cética do esboço; derivar o passo B(n) na cadeia v392; B3 por ato do operador")
res = dict(base, tipo="RESULTADO", status="EXAMINADA",
           resultado="Sandbox: run pre_selo (Nós real v391) JA_SINCRONIZADA, bateria 13 PASSA/0 FALHA; run pos_selo (Nós sintético v392, --sandbox) PIN_CHANGED provado, manifesto B3-v392 regenerado, re-pino conferido, bateria 12 PASSA/0 FALHA/2 n.a., aplicação na cópia com backup e rollback; 7/7 controles negativos recusam como esperado; β runtime bit a bit igual ao contrato.",
           veredito="VINCULO_DESENHADO__ESBOCO_TESTADO_EM_SANDBOX__B3_PENDE_DO_OPERADOR",
           defeito="esboço ainda sem auditoria independente; evento c1 de gravação ainda inexistente",
           nao_refazer="não refazer o esboço; auditar e derivar na cadeia", proximo_passo="auditoria independente; passo B(n) em chain_pos_rito_v392; B3")
for i, r in enumerate((rota, res)):
    p = os.path.join(D, "registro_%s_F0.6.json" % r["tipo"].lower())
    json.dump(r, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    out = run([ROTAS, "registrar", p, "--quem", "claude-c1 (gerência)"])
    try:
        j = json.loads(out)
        print("mapa", r["tipo"], j.get("ok"), [g.get("seq") for g in j.get("gravados", [])], j.get("erro"))
    except Exception:
        print("mapa", r["tipo"], out[-300:])

# 3. parágrafo ao lado no plano (append, backup de bytes)
b = open(PLANO, "rb").read()
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(PLANO + ".bak_" + ts, "wb").write(b)
par = open(os.path.join(D, "PLANO_V392_paragrafo_B3.md"), "rb").read()
add = ("\n\n---\n\n<!-- R3, 12/10/2026: parágrafo do elo B(3) acrescentado AO LADO pela gerência c1 (unidade F0.6; verbatim do operador sha16 78ef70e6f9868281; fonte "
       + os.path.join(D, "PLANO_V392_paragrafo_B3.md") + ", sha16 " + sh(os.path.join(D, "PLANO_V392_paragrafo_B3.md"))[:16] + "). A R2 fica intacta acima. -->\n\n").encode("utf-8") + par
n = b + (b"" if b.endswith(b"\n") else b"\n") + add
open(PLANO + ".tmp", "wb").write(n)
assert os.path.getsize(PLANO + ".tmp") == len(n) > len(b)
os.replace(PLANO + ".tmp", PLANO)
print("plano", len(b), "->", len(n), "sha16", sh(PLANO)[:16])

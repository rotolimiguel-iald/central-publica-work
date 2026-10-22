# -*- coding: utf-8 -*-
"""Registro (19/10/2026, sessão a7) da integração da ENTREGA_009 do Codex pela Central: memórias epct-protocolo-15 e central-de-patentes-estado,
a linha do MEMORY.md (a antiga VERBATIM no MEMORY_2.md) e a rota no Mapa de Rotas. Backup de BYTES; temporário -> confere -> troca."""
import hashlib, json, os, subprocess, sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")
AGORA = datetime.now().strftime("%d/%m/%Y %H:%M")
MEM = r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"
CEN = r"C:\IALD\Central de Patentes"
W = CEN + r"\work\custodia_v394_19out"


def tocar(p, f, pode_encolher=False):
    raw = open(p, "rb").read()
    open(p + ".bak_" + TS, "wb").write(raw)
    nl = "\r\n" if b"\r\n" in raw else "\n"
    novo = f(raw.decode("utf-8"), nl).encode("utf-8")
    tmp = p + ".tmp_" + TS
    open(tmp, "wb").write(novo)
    assert pode_encolher or os.path.getsize(tmp) > len(raw), p
    os.replace(tmp, p)
    print("ok", os.path.basename(p), len(raw), "->", os.path.getsize(p))


def ap(p, texto):
    tocar(p, lambda t, nl: t.rstrip("\r\n") + nl + nl + texto.strip("\n").replace("\n", nl) + nl)


aud = json.load(open(CEN + r"\andamentos\deadline_audit.json", encoding="utf-8"))["resumo"]
rv = r"C:\TUNEL_PCT\REVISAO\REVISAO_012.md"
rv16 = hashlib.sha256(open(rv, "rb").read()).hexdigest()[:16]
TXT = ("O operador (19/10): «o chatgpt acabou os créditos, portanto não vai retornar, vc precisa terminar o serviço todo». A Central integrou a "
       "ENTREGA_009 do Codex (13 e 19/10) e fechou as pendências «CONTROLE» dela: (1) 26/11/2026, a publicação internacional do ACOM (IB/345 "
       "[42], PDF original por sha256), entrou em `andamentos/marcos_fixos.json` (id `acom_wo_publicacao_26nov`, vermelho); (2) a auditoria de "
       "prazos (`tools/patent_monitor.py --audit`) passou a cobrir os processos adicionais com data de depósito própria — BR112026025335-5 e "
       "BR102026024913-0: %d processos + %d adicionais, %d vencidos a conferir, %d próximos (T-180d); (3) a nota da anuidade foi corrigida (LPI art. "
       "84 §2º: retribuição adicional nos 6 meses subsequentes aos 3 ordinários; o texto antigo dizia 3). REVISAO_012 no túnel (`%s`): não é ordem; "
       "registra o fechado e o aberto. ABERTO, sem mudança de responsável: o recibo da GRU 284 do ACOM BR 11 (paga; o PAG dá erro ao baixar — não "
       "reemitir, não 203, não duplicar exame); o nome do BR 11 (260/248, escolha do operador); a 2ª geração do ACOM ANTES de 26/11 (operador + "
       "advogado); RO/106 do MQC e do Aprendizado (FATAL 09/12; meta das folhas 19/11 — a Central prepara, o operador libera, a transmissão é do "
       "Codex ou do operador); MS 28/10 (ato do advogado; provas entregues ao Escritório em 19/10); emenda restritiva (~06/11); Regras "
       "20.5/20.5bis/20.6 (04/12 e 07/12); DRAFTs; RPI (HTTP 503 em 19/10). Fora do git da Central (vitrine, não backup): os 1.382 arquivos de "
       "EPCT/*/RECIBOS e CORRECAO_FORMAL_BR (recibos, e-mails S/MIME, zips), custodiados no disco e no backup." %
       (aud["processos"], aud.get("processos_adicionais", 0), aud["prazos_vencidos_a_conferir"], aud["prazos_proximos"], rv16))
ap(os.path.join(MEM, "epct-protocolo-15.md"), "## %s — o Codex sem créditos; a Central fecha os controles da ENTREGA_009\n\n%s" % (AGORA, TXT))
ap(os.path.join(MEM, "central-de-patentes-estado.md"), "## %s — PCT: controles da ENTREGA_009 integrados pela Central\n\n%s" % (AGORA, TXT))

M, M2 = os.path.join(MEM, "MEMORY.md"), os.path.join(MEM, "MEMORY_2.md")
t = open(M, "rb").read().decode("utf-8")
nl = "\r\n" if "\r\n" in t else "\n"
old = [l for l in t.split(nl) if l.startswith("- [Protocolo ePCT dos 15](epct-protocolo-15.md)")]
assert len(old) == 1, old
nova = ("- [Protocolo ePCT dos 15](epct-protocolo-15.md) — MEMORY_2.md (07/10) · **19/10: Codex sem créditos; a Central integrou a ENTREGA_009 "
        "(REVISAO_012; 26/11 nos marcos; auditoria +2 processos; anuidade 6m); RO/106 MQC/Aprendizado FATAL 09/12; MS 28/10**")
ap(M2, "## %s — linha movida do MEMORY.md (regra dos dois arquivos), VERBATIM\n\n%s" % (AGORA, old[0]))
tocar(M, lambda t_, nl_: t_.replace(old[0], nova, 1), pode_encolher=True)
assert os.path.getsize(M) < 24 * 1024, os.path.getsize(M)

rota = {"tipo": "ROTA", "rota_id": "pi.pct.controles_entrega009_19out", "dominio": "PI",
        "titulo": "A Central integra a ENTREGA_009 do Codex (sem créditos): 26/11 nos marcos fixos, auditoria com os processos adicionais, anuidade 6 meses",
        "pergunta": "Com o Codex parado por falta de créditos, quais pendências «CONTROLE» da ENTREGA_009 de 19/10 a Central fecha sozinha, sem ato no navegador, pagamento ou protocolo?",
        "dados": ["C:/TUNEL_PCT/DO_CODEX/ENTREGA_009_* (13 e 19/10)", "patents/*/docket.yaml (processos_adicionais)", "andamentos/marcos_fixos.json",
                  "o PDF original do IB/345 [42] custodiado pelo Codex"],
        "metodo": "Leitura da tabela de pendências do Codex; patch com backup de bytes no tools/patent_monitor.py (nota da anuidade; os processos adicionais "
                  "com filing_date viram itens próprios da auditoria); marco novo no marcos_fixos.json com a fonte por sha256; REVISAO_012 no túnel.",
        "resultado": TXT, "veredito": "CONTROLES_PCT_INTEGRADOS__ABERTOS_DITOS_COM_RESPONSAVEL", "estatuto": "REAL", "status": "EXAMINADA",
        "olhou_dados": False,
        "defeito": "A auditoria antiga só percorria os 16 dockets e a nota da anuidade dizia 3 meses (achados do Codex em 19/10, conferidos na LPI art. 84 §2º).",
        "nao_refazer": "Os três controles estão feitos; o resto da tabela depende do operador, do advogado ou do Codex.",
        "proximo_passo": "Folhas de substituição dos desenhos do MQC e do Aprendizado (RO/106; meta 19/11; FATAL 09/12), quando o operador mandar.",
        "onde": W,
        "artefatos": [CEN + r"\tools\patent_monitor.py", CEN + r"\andamentos\marcos_fixos.json", CEN + r"\andamentos\deadline_audit.json", rv],
        "refs": ["pi.pct.ro106_mqc_aprendizado_09dez", "pi.acom.segunda_geracao_antes_do_wo"],
        "nota": "Sessão a7 da Central (Claude), 19/10/2026."}
for k, v in rota.items():
    if isinstance(v, str):
        assert "CONFIRM" not in v.upper(), k
rp = os.path.join(W, "rota_pct_controles_19out.json")
open(rp, "w", encoding="utf-8").write(json.dumps(rota, ensure_ascii=False, indent=1))
r = subprocess.run([sys.executable, r"C:\IALD\MAPA_DE_ROTAS\rotas.py", "registrar", rp, "--quem", "claude-central-a7 (PCT 19/10)"],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("rota:", r.returncode, (r.stdout or r.stderr)[-200:])

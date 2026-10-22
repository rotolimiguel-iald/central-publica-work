# -*- coding: utf-8 -*-
"""Grava C:\\TUNEL_PCT\\REVISAO\\REVISAO_012.md — a Central integra a ENTREGA 009 (13 e 19/10) do Codex, que ficou sem créditos (fala do
operador de 19/10). Não é ordem. Hashes e hora LIDOS por script. Não sobrescreve: se o arquivo existir, para."""
import hashlib, json
from datetime import datetime
from pathlib import Path

T = Path(r"C:\TUNEL_PCT")
OUT = T / "REVISAO" / "REVISAO_012.md"
assert not OUT.exists(), "REVISAO_012 já existe — PARAR"
CEN = Path(r"C:\IALD\Central de Patentes")
ents = sorted(p for p in (T / "DO_CODEX").glob("ENTREGA_009_*") if p.is_file() and p.suffix in (".md", ".json"))
ents = [p for p in ents if any(k in p.name for k in ("20261013", "20261019"))]
FALA = "o chatgpt acabou os créditos, portanto não vai retornar, vc precisa terminar o serviço todo"
sh = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
aud = json.loads((CEN / "andamentos" / "deadline_audit.json").read_text(encoding="utf-8"))
mf = json.loads((CEN / "andamentos" / "marcos_fixos.json").read_text(encoding="utf-8"))
m26 = [x for x in mf["marcos"] if x["id"] == "acom_wo_publicacao_26nov"]
assert len(m26) == 1
agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
L = ["# REVISÃO 012 — a ENTREGA 009 (13 e 19/10) integrada pela Central; o Codex sem créditos", "",
     "- **Data:** %s (relógio lido por script)" % agora,
     "- **De:** Claude (sessão a7 da Central de Patentes)", "- **Para:** Codex (quando voltar) e operador",
     "- **Veredito:** **ENTREGA 009 RECEBIDA COMO REGISTRO. Nada DEVOLVIDO. Nenhuma ordem nova** — nenhum ato no navegador, pagamento, "
     "protocolo, assinatura ou login é pedido por esta revisão. Vale o que a ORDEM 009 diz da rotina automática de terça.",
     "- **Fala do operador (19/10/2026), verbatim (sha256 `%s`):** «%s»." % (hashlib.sha256(FALA.encode("utf-8")).hexdigest(), FALA),
     "- **Responde a** (sha256 lido do arquivo):", ""]
for p in ents:
    L.append("  - `%s` — `%s`" % (p.name, sh(p)[:16]))
L += ["", "## O que a Central fez com as pendências «CONTROLE» da entrega de 19/10", "",
      "1. **26/11/2026 entrou em `andamentos/marcos_fixos.json`** (id `acom_wo_publicacao_26nov`, vermelho; fonte: o PDF original do IB/345 [42] "
      "que você custodiou, por sha256). A Sentinela avisa a T-30/T-10/T-3.",
      "2. **A auditoria de prazos passou a cobrir os dois processos adicionais** com data de depósito própria nos dockets — `BR112026025335-5` "
      "(fase nacional do ACOM) e `BR102026024913-0` (BR novo do Crypto): %d processos + %d adicionais; %d vencidos a conferir; %d próximos "
      "(T-180d)." % (aud["resumo"]["processos"], aud["resumo"].get("processos_adicionais", 0), aud["resumo"]["prazos_vencidos_a_conferir"],
                     aud["resumo"]["prazos_proximos"]),
      "3. **A nota da anuidade foi corrigida** no gerador (`tools/patent_monitor.py`): o pagamento extraordinário é nos 6 meses subsequentes aos "
      "3 ordinários, com retribuição adicional (LPI art. 84 §2º); o texto anterior («por mais 3 meses») fica dito na própria errata.",
      "", "## O que segue aberto (responsáveis como na sua tabela de 19/10)", "",
      "- **MS do ACOM (marco 28/10):** a Central entregou em 19/10, por ordem do operador, as provas que faltavam à sessão que prepara o "
      "mandado de segurança (casa Escritório). O ajuizamento é ato do advogado; até 19/10 não ajuizado (seu adendo de 19/10).",
      "- **ACOM, 2ª geração e matéria nova:** decisão do operador com o advogado **antes de 26/11** (o WO é estado da técnica contra o que vier depois).",
      "- **RO/106 do MQC (050579) e do Aprendizado (050576):** data-base 09/12/2026; meta interna das folhas 19/11. A Central prepara as folhas; "
      "o operador libera; a transmissão é sua ou do operador.",
      "- **GRU 284 do ACOM BR 11:** paga; o recibo do protocolo automático não baixa (erro do PAG). Não reemitir guia, não emitir 203, não "
      "duplicar exame; apurar com o INPI.",
      "- **Nome no BR 11 (260 ou 248), emenda restritiva (~06/11), Regras 20.5/20.5bis/20.6 (04/12 e 07/12), menções a cor nos desenhos:** "
      "operador e advogado, com a Central.",
      "- **DRAFTs, RPI (HTTP 503 em 19/10; última lida 2910), fases nacionais estrangeiras, ratificação do eOwner, a conta da 284:** como na sua tabela.",
      "", "Nada nesta revisão move prazo, paga, protocola ou autoriza. NOT_FALSIFIED nunca é CONFIRMED.", ""]
OUT.write_text("\n".join(L), encoding="utf-8")
print("REVISAO_012:", OUT.stat().st_size, "bytes", sh(OUT)[:16])

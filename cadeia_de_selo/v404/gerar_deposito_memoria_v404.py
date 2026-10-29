# -*- coding: utf-8 -*-
"""gerar_deposito_memoria_v404.py -- deposita na FILA DA MEMORIA (fila\\depositos\\claude-prep-v404\\) o resumo da preparacao da v404, no formato de fila\\README.md. NAO toca MEMORY.md nem MEMORY_2.md (so' a gerencia c1 escreve la'); hashes LIDOS dos arquivos.
uso: python -I -B -X utf8 gerar_deposito_memoria_v404.py"""
import datetime, hashlib, json, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
FILA = os.path.join(os.path.expanduser("~"), ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "fila", "depositos", "claude-prep-v404")
os.makedirs(FILA, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
rj = lambda p: json.load(open(os.path.join(HERE, p), encoding="utf-8"))
CM = rj("CANDIDATO_v404.json"); PC = rj("PRECONDICOES_v404.json")
ok = sum(1 for c in PC["checagens"] if c["ok"]); n = len(PC["checagens"])
fontes = [os.path.join(HERE, "RELATORIO_PREPARACAO_v404.md"), os.path.join(HERE, "PLANO_v404.md"), os.path.join(HERE, "CANDIDATO_v404.json"), os.path.join(HERE, "ESPERADOS_v404.json"), os.path.join(HERE, "PRECONDICOES_v404.json"),
          os.path.join(HERE, "pos_rito", "HARNESS_TEXTOS_ENSAIO_v404.json"), os.path.join(HERE, "pos_rito", "HARNESS_FECHAR_SANDBOX_v404.json")]
agora = datetime.datetime.now()
corpo = f"""---
quem: claude-prep-v404
casa: Nós
tipo: project
estatuto: REAL
alvo_sugerido: missao-ultima-flag-um-py.md
fontes:
""" + "\n".join("  - %s  sha256:%s" % (p, sha(p)) for p in fontes) + f"""
---
**v404 PREPARADA (28/10/2026, preparação para a gerência c1; nada instalado, rito não rodado, Nós/MEMORY.md/MEMORY_2.md intocados).** Conteúdo: Jo 8,32 e a projeção transversal da Meia-Nat — duas pedras de kernel (`ProjecaoTransversalDaMeiaNat`, nome provisório da gerência aceito pelo operador; `Jo8v32`, nome do operador), três registros com função (`projecao_transversal_v404`, `jo8v32_v404`, `f2b_errata_v404`) e dois por spec (`cunhagens_v404`, `kh_n1_cobertura_v404`); o `sen 45°` do neutrino deixa de ser postulado, DERIVADO no kernel e condicional a uma identificação [ONTO]; E₀ = 1 eV segue DECLARADO; o canal F2b sai de AWAITING para retirado antes do dado, AO LADO (V1 congelado por hash); o gate não se move (as funções do gate/neutrino/ramo B são idênticas às da v403).

**Medido:** candidato `{CM['sha16']}` ({CM['bytes']:,} B; base v403 `{CM['base_v403_sha16']}`), regenerado byte a byte igual; escada {CM['escada'][0]} → {CM['escada'][1]} ({CM['n_bandeiras']} bandeiras novas); ensaio a seco TUDO PASSOU; conferidor negativo/positivo; B(n) pré-selo gerado e pinado (bateria passa; produção intacta); pós-rito (leitura, textos, fechar, mapa, serviço da Bancada) escrito e testado em dois harnesses que passam (centenas de controles negativos); `p00` {ok}/{n}.

**Falta (gerência/operador):** o `p00` reprova 1 checagem real — o `MEMORY.md` está no limite e a superfície do pós-rito não compacta; decidir o índice, revisar (revisão independente NÃO afirmada), instalar, rito, `chain_pos_rito_v404.sh`; B(n) aplicar com `V404_AUTORIZACAO_OPERADOR` (texto sem o nome do script do serviço da Bancada); E₀ e a lei de propagação do pedágio de Planck (operador).

**Lições:** contagens de derivador MEDIDAS na fonte; `B11`/nomes nascidos no `um.py` base não sobem sozinhos no bump (a Bancada pina B12; o B(n) da v404 grava B13; os rótulos «novo»/«recriado» da leitura e dos textos foram reescritos à mão); heredoc do Bash colapsa barras invertidas (escrever scripts por arquivo); `C:/t/vb21` precisa não existir quando a bateria pré-selo roda. Rota no Mapa: `umpy.v404.cadeia_de_selo_preparada_28out`.
"""
out = os.path.join(FILA, agora.strftime("%Y%m%d_%H%M%S") + "_v404_preparada.md")
if os.path.exists(out):
    raise SystemExit("ja existe: " + out)
open(out, "w", encoding="utf-8", newline="\n").write(corpo)
print(out, len(corpo.encode("utf-8")), "B")

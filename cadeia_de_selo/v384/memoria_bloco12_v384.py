# -*- coding: utf-8 -*-
"""Acrescenta o bloco 12 (04/10: a RATIFICACAO, o V1 congelado, a cadeia ate o rito e o rito LANCADO) a memoria da v384. Numeros LIDOS dos artefatos.
Backup de BYTES; temporario -> tamanho -> substituir -> conferir."""
import glob, hashlib, json, os, time
HERE = os.path.dirname(os.path.abspath(__file__))
M = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory", "v384-pilar-quantico-gpu-02out.md")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
PERM = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out")
V1P = os.path.join(PERM, "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json"); V1 = json.load(open(V1P, encoding="utf-8")); RAT = V1["ratificacao_do_operador"]
CM = json.load(open(os.path.join(HERE, "CANDIDATO_v384.json"), encoding="utf-8"))
AP = sorted(glob.glob(os.path.join(HERE, "APLICADO_AO_CANONICO_*.json")))[-1]; APJ = json.load(open(AP, encoding="utf-8"))
LOG = open(os.path.join(HERE, "rito_servidor_v384.log"), encoding="utf-8", errors="replace").read()
ini = [l for l in LOG.splitlines() if "inicio do rito" in l]
B = """

<!-- estado_04out_ratificado_rito_v384 -->
**12. RATIFICADO e o RITO LANÇADO (04/10/2026) — gerência, em nome próprio; números lidos por script:**
- **A ratificação do operador** (verbatim no V1, `ratificacao_do_operador.verbatim`; %s): escolha **%s**. A guarda é lexical; a leitura humana dá a mesma escolha («não vejo outra opção honesta … senão B_ampliado … vamos assim»).
- **O V1 congelado:** `%s` — JSON `%s`, MD `%s`, especificação `%s`, %d evidências em `evidencias_PREREGISTRO_V1\\`; V1, MD, evidências e o gerador marcados SÓ LEITURA. Conferência independente (2 lentes): CONFERE (`scratchpad\\v384\\conferir_congelamento_v384_resultado.json`).
- **A cadeia:** candidato instalável `%s` (%d patches; selo RATIFIED_BY_THE_OPERATOR); fumaça OK (só caminho de código, nunca resultado); ensaio a seco `v384` TUDO PASSOU; ESPERADOS gravados; INSTALADO no Nós (`%s`): um.py `%s` sobre a v383 `%s` (backups `.bak_%s` dos 5 arquivos).
- **O rito:** %s, pelo `rito_v384.sh` em segundo plano (Git Bash). Servidor do modelo nativo PARADO pelo rito (marcador `restaurar=1`). Se a sessão cair: conferir o marcador `C:\\Users\\rotol\\AppData\\Local\\Temp\\claude\\c--IALD-Central-de-Patentes\\6da8f00d-d44f-4888-a88d-fc9f73eead3d\\scratchpad\\v384\\.servidor_parado_pelo_rito` e o `.rito_v384.pid` (abortar = `kill -TERM` no Git Bash, conferindo antes `/proc/<pid>/cmdline`). Depois do rito: `conferir_rito_v384.py`, e a cadeia (linhagem, desenho, Atlas, índice, handoff à sessão do site).
""" % (RAT["quando"], RAT["escolha"], V1P, h(V1P)[:16], h(V1P[:-5] + ".md")[:16], V1["spec_sha256"][:16], len(V1["evidencias"]),
       CM["sha16"], len(CM["patches"]), os.path.basename(AP), APJ["um_py_novo"]["sha16"], APJ["backups"]["um.py"]["sha16"], APJ["ts"],
       (ini[0] if ini else "INICIO NAO ACHADO NO LOG"))
raw = open(M, "rb").read(); assert b"estado_04out_ratificado_rito_v384" not in raw
bak = M + ".bak_" + time.strftime("%Y%m%d_%H%M%S"); open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
novo = raw + B.encode("utf-8"); open(M + ".tmp", "wb").write(novo); assert os.path.getsize(M + ".tmp") == len(novo); os.replace(M + ".tmp", M)
assert open(M, "rb").read() == novo and len(novo) > len(raw)
print("memoria v384:", len(raw), "->", len(novo))

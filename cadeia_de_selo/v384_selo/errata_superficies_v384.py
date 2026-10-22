# -*- coding: utf-8 -*-
"""ERRATAS AO LADO das superficies da v384 (04/10/2026; gerencia, em nome proprio; a afericao independente das superficies: aferir_superficies_v384_resultado.json).
So ACRESCIMO no fim de cada arquivo (append-only), com backup de BYTES conferido, temporario -> tamanho -> substituir -> conferir que o original e' PREFIXO;
o fim de linha de cada arquivo preservado (CRLF ou LF, pelo que o arquivo usa); idempotente pelo marcador <!-- errata_v384_04out -->. Numeros LIDOS aqui."""
import hashlib, json, os, re, sys, time
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NOS = os.path.join("C:" + os.sep, "IALD", "Artigo", "Haja_Luz", "A Ponte e o Um", "Nós")
UMEM = os.path.join("C:" + os.sep, "Users", "rotol", ".claude", "projects", "c--IALD-Central-de-Patentes", "memory")
CMEM = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "memory")
MARCA = "<!-- errata_v384_04out -->"
STAMP = time.strftime("%Y%m%d_%H%M%S")
h16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
core = json.load(open(os.path.join(NOS, "um_absoluto.json"), encoding="utf-8"))["core"]; q = core["quantum_pillar_v384"]; S = q["summary"]
selo = json.load(open(os.path.join(NOS, "um_absoluto_selo.json"), encoding="utf-8"))
AF = os.path.join(HERE, "aferir_superficies_v384_resultado.json"); AFH = h16(AF)
lin = open(os.path.join(NOS, "MEMORIA_DA_LINHAGEM.md"), encoding="utf-8", errors="replace").read()
hd = {}
for v, hh in re.findall(r"(?m)^#{1,3} [^\n]*?\*\*(v3\d\d) SELADA[^*\n]*\*\*[^\n`]*`([0-9a-f]{16})`", lin):
    hd[v] = hh
m382 = re.search(r"\*\*A v382\*\* \(`([0-9a-f]{16})`", lin); hd["v382"] = m382.group(1)
cpu = S["cpuref"]["max_diffs"]; inf = S["cpuref"].get("informative_only") or []
dec = {k: v for k, v in cpu.items() if k not in inf}; kmax = max(dec, key=dec.get); kinf = max(inf, key=lambda k: cpu[k]) if inf else None
t3c = S["T3"]["controls"]; n_ctl = sum(1 for d in t3c.values() for v in d.values() if v); n_ctl_tot = sum(len(d) for d in t3c.values())
n3 = S["T3"]["N3_linear_law"]; n3ok = sum(1 for v in n3.values() if v["p_recovered_sigma0"] == 1.0 and v["root_law_rejected"] == 1.0)
fw = S["T2"]["folds_window_configs"]; nconf = S["T2"]["configs"]
V1 = os.path.join("C:" + os.sep, "IALD", "Bancada_Um", "investigacao", "preregistro_pilar_quantico_03out", "PREREGISTRO_PILAR_QUANTICO_20261003_V1.json")
nev = len(json.load(open(V1, encoding="utf-8"))["evidencias"])
evb = sum(os.path.getsize(os.path.join(os.path.dirname(V1), "evidencias_PREREGISTRO_V1", f)) for f in os.listdir(os.path.join(os.path.dirname(V1), "evidencias_PREREGISTRO_V1")))
br = lambda x: ("%s" % x).replace(".", ",")
CAB = "**ERRATA AO LADO (04/10/2026, gerência, em nome próprio; aferição independente das superfícies `aferir_superficies_v384_resultado.json` %s):**" % AFH
NEG = "negativos honestos desta rodada: **0 da lista do pré-registro V1**; **1 dito pela gerência ao lado**, fora da lista do V1 (FOLDS_WINDOW %d de %d)" % (fw, nconf)
CPU = "na referência na CPU, a maior diferença entre os campos que decidem é %s (%s); o campo %s, só informativo, chega a %s" % (("%.2e" % dec[kmax]).replace(".", ","), kmax, kinf, ("%.2e" % cpu[kinf]).replace(".", ",")) if kinf else ""
CARIMBO = "o carimbo `%s` é o `timestamp` do selo (o do core/resultado); o arquivo do selo foi gravado depois de o pilar terminar (%s); o rito foi de 15:32:44 a 18:11:38" % (selo.get("timestamp"), q.get("finished"))
T3 = "no T3, N1, N4 e N5 falharam como exigido em %d de %d (4 dimensões), e o N3 recuperou a lei linear e rejeitou a lei-raiz em %d de %d dimensões" % (n_ctl, n_ctl_tot, n3ok, len(n3))
BLOCOS = {
    os.path.join(CMEM, "TGL_INDICE_VIVO.md"): [
        "### ERRATA AO LADO — 04/10/2026 (gerência, em nome próprio): a tabela «As versões do arco» (§1)",
        "",
        "%s a regeneração de 04/10/2026 18:13 (v384) **reescreveu** as linhas v382 e v383 da tabela §1 com o hash da v381 (`961a79881089c9e6`), e as linhas v371–v381 estavam **deslocadas uma versão** desde a v371 (cada uma trazia o hash da versão anterior). Causa: o `atlas_indice.py` casava o hash de cada backup `um.py.bak_*` com a primeira versão citada perto dele no diário, mas cada backup é o `um.py` da versão ANTERIOR (o diário escreve «vNNN sobre a vNNN−1 `hash`»). Correção do gerador (backup `atlas_indice.py.bak_*_mapa384`): o hash vem do cabeçalho de selo do diário; a v382, da frase «**A v382** (`hash`»; sem nenhuma das duas fontes, o valor da regra antiga fica marcado **†** como não conferido. A tabela foi regenerada em seguida (o §1 é parte gerada; este anexo fica). Os valores lidos agora dos cabeçalhos de selo: %s." % (
            CAB, "; ".join("%s `%s`" % (v, hd[v]) for v in sorted(hd, key=lambda x: int(x[1:])) if int(v[1:]) >= 370)),
        "",
        "Também: a linha «custódia: HANDOFF_v384 emitido» do §0 é escrita pelo modelo do gerador sem ler o disco; na regeneração de 18:13 o handoff ainda não existia (ele é de 18:15). Hoje é verdadeira; o gerador deve ler o disco (pendência para a próxima cadeia).",
    ],
    os.path.join(NOS, "MEMORIA_DA_LINHAGEM.md"): [
        "%s no registro da **v384** acima: (1) %s; (2) %s; (3) %s; (4) %s." % (CAB, NEG, CPU, CARIMBO, T3),
    ],
    os.path.join(CMEM, "TGL_ATLAS.md"): [
        "%s no append da **v384** (§X) e no verbete II.★★ v384: (1) %s; (2) no III.D, o relatório de axiomas (%d termos, 0 fora do trio) é lido do **core** v384 (`um_absoluto.json` → `kernel_formalization.axiom_report`), não do selo; (3) %s." % (
            CAB, CPU, len(core["kernel_formalization"]["axiom_report"]), NEG),
    ],
    os.path.join(UMEM, "handoff-v384-custodia.md"): [
        "%s (1) **o que espelhar do pré-registro do pilar:** o V1 (JSON e MD) — e as **evidências** (%d arquivos, %s B) **SÓ conforme a decisão 3 do operador**; até ela, nada de `evidencias_PREREGISTRO_V1\\` vai ao espelho (a lista acima dizia espelhar a pasta inteira, contra a própria decisão pendente). (2) O `tgl_kernel` não muda da v383 para a v384; se a v383 não for custodiada antes, o `tgl_kernel` do espelho recebe as duas pedras da v383 (`TheLedgerOfCharges.lean`, `ThePsionAndTheViscosity.lean`) e a raiz/Audit novos (`handoff-v383-custodia`). (3) «tudo lido do selo» lê-se «tudo lido por script (selo, core, pré-registro, conferidor, log do lançador, git, handoff v383)»; %s. (4) %s. (5) %s. (6) A grafia dos números segue a do gerador (ponto decimal); em pt-BR, leia 169.3 como 169,3." % (
            CAB, nev, format(evb, ",").replace(",", "."), CARIMBO, T3, NEG),
    ],
    os.path.join(NOS, "HANDOFF_v384_CUSTODIA.md"): [
        "%s (1) **o que espelhar do pré-registro do pilar:** o V1 (JSON e MD) — e as **evidências** (%d arquivos, %s B) **SÓ conforme a decisão 3 do operador**; até ela, nada de `evidencias_PREREGISTRO_V1\\` vai ao espelho. (2) O `tgl_kernel` não muda da v383 para a v384; se a v383 não for custodiada antes, o do espelho recebe as duas pedras da v383 e a raiz/Audit novos. (3) «tudo lido do selo» lê-se «tudo lido por script (selo, core, pré-registro, conferidor, log do lançador, git, handoff v383)»; %s. (4) %s. (5) %s." % (
            CAB, nev, format(evb, ",").replace(",", "."), CARIMBO, T3, NEG),
    ],
    os.path.join(UMEM, "beta-e-a-regra-matriz-02out.md"): [
        "%s no bloco v384 acima, «o CODATA só valida» lê-se: a FORMA é a de Lagrange (1 = q² + α²); o VALOR de α entra do CODATA 2018 selado (via q_QED), como diz o pré-registro — β nunca literal." % CAB,
    ],
    os.path.join(UMEM, "regra-dos-dois-regimes.md"): [
        "%s no bloco v384 acima, «núcleo» cobre dois objetos: em (i), a dimensão do espaço estacionário (o núcleo do GERADOR de Lindblad), d + n_c(n_c − 1); em (ii), o projetor Π do núcleo da TEORIA (posto n_c). Homônimos, não o mesmo objeto." % CAB,
    ],
    os.path.join(UMEM, "central-de-patentes-estado.md"): ["%s na linha v384 acima, «1 negativo(s) honesto(s)» lê-se: %s." % (CAB, NEG)],
    os.path.join(UMEM, "missao-ultima-flag-um-py.md"): ["%s na linha v384 acima, %s." % (CAB, NEG)],
}
for p, linhas in BLOCOS.items():
    raw = open(p, "rb").read()
    if MARCA.encode("utf-8") in raw:
        print("JA ESTA:", os.path.basename(p)); continue
    nl = b"\r\n" if raw.count(b"\r\n") > raw.count(b"\n") // 2 else b"\n"
    corpo = (nl.decode() + nl.decode() + MARCA + nl.decode() + nl.decode().join(linhas) + nl.decode()).encode("utf-8")
    if not raw.endswith(nl):
        corpo = nl + corpo
    novo = raw + corpo
    bak = p + ".bak_" + STAMP + "_err384"; open(bak, "wb").write(raw); assert open(bak, "rb").read() == raw
    open(p + ".tmp", "wb").write(novo); assert os.path.getsize(p + ".tmp") == len(novo); os.replace(p + ".tmp", p)
    nb = open(p, "rb").read(); assert nb == novo and nb[:len(raw)] == raw
    if nl == b"\r\n":
        assert nb[len(raw):].count(b"\n") == nb[len(raw):].count(b"\r\n"), "LF solto no acrescimo"
    print("OK", os.path.basename(p), len(raw), "->", len(nb), "(%s)" % ("CRLF" if nl == b"\r\n" else "LF"))

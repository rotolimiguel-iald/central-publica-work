# -*- coding: utf-8 -*-
# Monta LEVANTAMENTO.md a partir do modelo + tabelas geradas por script (pinos, teoremas, runtime, outras ancoras, literatura,
# mapa, arquivos) + listas NOVO/RISCOS. Grava em temporario, confere tamanho, substitui. Somente dentro desta pasta.
import json, os, hashlib, re, glob
AQUI = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(AQUI, "DEFINICOES.json"), encoding="utf-8"))
LISTAS = json.load(open(os.path.join(AQUI, "LISTAS_NOVO_RISCOS.json"), encoding="utf-8"))
modelo = open(os.path.join(AQUI, "LEVANTAMENTO_modelo.md"), encoding="utf-8").read()
DEFKINDS = ("def", "abbrev", "structure", "class", "inductive", "instance", "opaque")


def sha16(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:16]


def cel(s):
    """celula de tabela markdown: escapa a barra vertical."""
    return str(s).replace("|", "\\|").replace("\n", " ")


def negrito(s):
    return "**" + str(s).replace("*", "\\*") + "**"


# --- pinos
P = D["pinos"]
lin = ["| pino | arquivo | sha16 | nota |", "|---|---|---|---|"]
for k, v in D["textos_operador"].items():
    lin.append(f"| {k} | `{os.path.basename(v['arquivo'])}` | `{v['sha16']}` | {v['bytes']} B; confere com a ordem: {v['confere']} |")
lin.append(f"| um.py v391 | `Nós\\um.py` | `{P['um_py_v391']['sha16']}` | {P['um_py_v391']['bytes']} B; lido só por busca com número de linha |")
lin.append(f"| core v391 | `Nós\\um_absoluto.json` | `{P['core_v391']['sha16']}` | lido por script |")
lin.append(f"| selo v391 | `Nós\\um_absoluto_selo.json` | `{P['selo_v391']['sha16']}` | KERNEL 6163/6163 no trio |")
lin.append(f"| TGLExt.lean | `tgl_kernel\\TGLExt.lean` | `{P['TGLExt_lean']['sha16']}` | importa os módulos citados |")
lin.append(f"| Audit.lean | `tgl_kernel\\TGL\\Audit.lean` | `{P['Audit_lean']['sha16']}` | lista de `#print axioms` do rito |")
ka, kd = P["kernel_impressao_digital"], P["kernel_impressao_digital_depois"]
igual = all(ka[x] == kd[x] for x in ("n_arquivos", "bytes_total", "sha256_metadados", "n_lean_fora_lake", "sha256_conteudo_lean"))
lin.append(f"| tgl_kernel (impressão digital) | metadados de {ka['n_arquivos']} arquivos; conteúdo de {ka['n_lean_fora_lake']} .lean | "
           f"`{ka['sha256_metadados'][:16]}` / `{ka['sha256_conteudo_lean'][:16]}` | antes = depois = depois2: {igual} |")
lin.append(f"| mapa de rotas | `MAPA_DE_ROTAS\\rotas.jsonl` | `{P['mapa_rotas_livro']['sha16']}` | 1004 registros; cabeça `91915ad39a53d1df`; só consultar/ver |")
lin.append(f"| inventário da bancada | `memory\\INVENTARIO_BANCADA_CHATGPT.json` | `{P['inventario_bancada']['sha16']}` | gerado 27/09; bancada sem cópias do kernel |")
lin.append(f"| Nós Vivo | `NOS_VIVO\\nos_vivo.sqlite3` | `{P['nos_vivo_sqlite']['sha16']}` | aberto em mode=ro |")
TAB_PINOS = "\n".join(lin)

# --- teoremas (por objeto, sem repetir)
med = {t["nome"]: t for t in D["teoremas_medidos_aqui"]}
vistos = set()
blocos = []
for o in D["objetos"]:
    ks = [a for a in o["ancoras"] if a.get("tipo") == "kernel" and "ERRO" not in a]
    novos = [a for a in ks if a["nome"] not in vistos]
    if not novos:
        continue
    blocos.append(negrito(o["termo"]) + "\n")
    blocos.append("| teorema / definição | arquivo:linha | sha16 | enunciado | axiomas |")
    blocos.append("|---|---|---|---|---|")
    for a in novos:
        vistos.add(a["nome"])
        m = med.get(a["nome"])
        if m is not None:
            ax = "medido: " + ("nenhum axioma" if m["axiomas_medidos_aqui"] == [] else ", ".join(m["axiomas_medidos_aqui"]))
        elif a.get("kind") in DEFKINDS:
            ax = "definição"
        elif "por dependência" in a.get("estatuto", ""):
            ax = "por dependência (⊆ trio)"
        else:
            ax = "selo"
        blocos.append(f"| `{a['nome']}` | `{a['arquivo'].replace('tgl_kernel/', '')}:{a['linha']}` | `{a['sha16']}` | {cel(a['enunciado'])} | {ax} |")
    blocos.append("")
TAB_TEO = "\n".join(blocos)

# --- runtime e core
rt = ["| âncora | um.py: linha / core: caminho | valor ou descrição | estatuto |", "|---|---|---|---|"]
vr = set()
for o in D["objetos"]:
    for a in o["ancoras"]:
        if a.get("tipo") == "runtime_um_py":
            k = ("u", a["linha"])
            if k in vr:
                continue
            vr.add(k)
            rt.append(f"| `{cel(a['padrao'][:70])}` | l.{a['linha']} | {cel(a['descricao'])} | {cel(a['estatuto'])} |")
        elif a.get("tipo") in ("core_v391", "selo_v391"):
            k = (a["tipo"], a["caminho"])
            if k in vr:
                continue
            vr.add(k)
            rt.append(f"| {'core' if a['tipo'] == 'core_v391' else 'selo'} | `{a['caminho']}` | {cel(str(a['valor'])[:160])} — {cel(a['descricao'])} | {cel(a['estatuto'])} |")
TAB_RT = "\n".join(rt)

# --- outras ancoras (arquivos)
ot = ["| âncora | arquivo | sha16 | descrição | estatuto |", "|---|---|---|---|---|"]
vo = set()
for o in D["objetos"]:
    for a in o["ancoras"]:
        if a.get("tipo") in ("arquivo", "texto_operador", "memoria", "tunel", "selo") and "ERRO" not in a:
            if a["arquivo"] in vo:
                continue
            vo.add(a["arquivo"])
            nome = a["arquivo"].replace("C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\", "TUNEL\\").replace(
                "C:\\IALD\\Central de Patentes\\", "Central\\").replace("C:\\Users\\rotol\\.claude\\projects\\c--IALD-Central-de-Patentes\\memory\\", "memory(Claude)\\")
            ot.append(f"| {a['tipo']} | `{cel(nome)}` | `{a['sha16']}` | {cel(a['descricao'])} | {cel(a['estatuto'])} |")
TAB_OT = "\n".join(ot)

# --- literatura e mathlib
lt = ["| referência / nome | para quê | estatuto |", "|---|---|---|"]
vl = set()
for o in D["objetos"]:
    for a in o["ancoras"]:
        if a.get("tipo") in ("literatura", "mathlib_pinada_no_Nos"):
            ref = a.get("ref") or a.get("nome")
            if ref in vl:
                continue
            vl.add(ref)
            lt.append(f"| {cel(ref)} | {cel(a['descricao'])} | {cel(a['estatuto'])} |")
TAB_LIT = "\n".join(lt)


# --- mapa (consultas): reconstroi o rotulo pelo mesmo nome de arquivo usado na consulta
def nome_bash(t, n):
    b = (t + "\n").encode("utf-8")
    s = "".join(chr(c) if (48 <= c <= 57 or 65 <= c <= 90 or 97 <= c <= 122) else "_" for c in b)
    return s[:n]


Q_MAPA = ["posto", "rank", "defas", "dephas", "fractal", "frequen", "anticomut|anticommut", "vazamento", "atrator|attractor",
          "colapso|collapse", "pureza|purity|pure state|estado puro", "Breuer", "transmi", "D_beta|D_\u03b2|Dbeta",
          "unidade|unitariedade fractal", "singularidade", "nullity|nulidade|nucleo vazio", "latente|latent", "Lindblad|GKLS|GKSL",
          "tempo santo|santo"]
Q_INV = ["rank|posto", "dephas|defas", "fractal", "purity|pure|pureza", "anticomm|anticomut", "frequen", "transmi", "leak|vazament",
         "collapse|colapso", "born", "select"]
lm = ["| consulta (`rotas.py consultar`) | n rotas | arquivo da resposta |", "|---|---|---|"]
for q in Q_MAPA:
    f = os.path.join(AQUI, "mapa", "consulta_" + nome_bash(q, 40) + ".json")
    n = json.load(open(f, encoding="utf-8")).get("n") if os.path.exists(f) else "ARQUIVO AUSENTE"
    lm.append(f"| `{cel(q)}` | {n} | `mapa\\{os.path.basename(f)}` |")
lm.append("")
lm.append("| consulta (`q_inventario.py`) | hits | arquivo |")
lm.append("|---|---|---|")
for q in Q_INV:
    f = os.path.join(AQUI, "inventario", "inv_" + nome_bash(q, 30) + ".txt")
    if os.path.exists(f):
        m = re.search(r"hits (\d+)", open(f, encoding="utf-8").readline())
        h = m.group(1) if m else "?"
    else:
        h = "ARQUIVO AUSENTE"
    lm.append(f"| `{cel(q)}` | {h} | `inventario\\{os.path.basename(f)}` |")
TAB_MAPA = "\n".join(lm)

# --- listas
NOVO = "\n".join(f"{i}. {x}" for i, x in enumerate(LISTAS["novo_vs_canon"], 1))
RISCOS = "\n".join(f"- {x}" for x in LISTAS["riscos"])

# --- arquivos
la = ["| arquivo | sha16 | papel |", "|---|---|---|"]
papeis = {
    "DEFINICOES.json": "definições, âncoras (linha e sha16 lidos por script), teoremas medidos",
    "HASHES_TEXTOS_OPERADOR.json": "conferência dos quatro textos", "CONFERENCIA_BETA.json": "α dos bytes, β em runtime, identidades",
    "EMBUTIDO_VS_KERNEL.json": "um.py embutido × tgl_kernel", "KERNEL_INDICE.json": "índice das 12.967 declarações (1.209 .lean)",
    "IMPRESSAO_DIGITAL_KERNEL_ANTES.json": "impressão digital antes", "IMPRESSAO_DIGITAL_KERNEL_DEPOIS.json": "depois da 1ª sonda",
    "IMPRESSAO_DIGITAL_KERNEL_DEPOIS2.json": "depois da 2ª sonda", "LISTAS_NOVO_RISCOS.json": "listas das seções 5 e 6",
    "LEVANTAMENTO_modelo.md": "modelo deste relatório",
    "EMBUTIDO_VS_KERNEL_ASPAS.json": "um.py embutido × tgl_kernel (literais escapados)",
    "modulos_citados.txt": "os 53 módulos TGLExt citados",
}
for f in sorted(os.listdir(AQUI)):
    p = os.path.join(AQUI, f)
    if (os.path.isfile(p) and f not in ("LEVANTAMENTO.md", "CONFERENCIA_PINOS.json") and not f.endswith(".tmp")
            and not f.startswith("_saida_") and not f.startswith("_teoremas")):
        la.append(f"| `{f}` | `{sha16(p)}` | {papeis.get(f, 'script' if f.endswith('.py') else '')} |")
la.append("| `CONFERENCIA_PINOS.json` | — | gerado depois deste arquivo: todo sha16 deste relatório e de DEFINICOES.json conferido contra os bytes |")
la.append("| `_saida_levantamento_md.txt`, `_saida_definicoes_json.txt`, `_teoremas_lista.json` | — | versões condensadas para a saída da subtarefa, derivadas DESTE arquivo (não listadas por hash para não haver circularidade) |")
for sub in ("lean_check", "mapa", "inventario", "nos_vivo"):
    n = len([x for x in os.listdir(os.path.join(AQUI, sub))])
    la.append(f"| `{sub}\\` | — | {n} arquivos (sondas/consultas e respostas) |")
TAB_ARQ = "\n".join(la)

txt = (modelo.replace("{{TABELA_PINOS}}", TAB_PINOS).replace("{{TABELA_TEOREMAS}}", TAB_TEO).replace("{{TABELA_RUNTIME}}", TAB_RT)
       .replace("{{TABELA_OUTRAS}}", TAB_OT).replace("{{TABELA_LIT}}", TAB_LIT).replace("{{TABELA_MAPA}}", TAB_MAPA)
       .replace("{{LISTA_NOVO}}", NOVO).replace("{{LISTA_RISCOS}}", RISCOS).replace("{{LISTA_ARQUIVOS}}", TAB_ARQ))
assert "{{" not in txt, "placeholder restante"
assert "ARQUIVO AUSENTE" not in txt, "consulta sem arquivo"
assert txt.splitlines()[0] == "LEVANTAMENTO F1.FREQUENCIA \u2014 12/10"
tmp = os.path.join(AQUI, "LEVANTAMENTO.md.tmp")
with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(txt)
assert os.path.getsize(tmp) == len(txt.encode("utf-8"))
os.replace(tmp, os.path.join(AQUI, "LEVANTAMENTO.md"))
print("LEVANTAMENTO.md", len(txt.encode("utf-8")), "bytes;", len(vistos), "declarações na tabela;", len(vr), "âncoras runtime/core;", len(vo), "arquivos;", len(vl), "literatura/mathlib")

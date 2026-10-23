# -*- coding: utf-8 -*-
"""MESCLA de uma rodada INCREMENTAL num preparo público (22/10/2026, custódia v396: «Atualize tudo com a nova versão do um.py»).
  preparar <preparo>              grava ja_vistos_<preparo>.json (o índice + a lista local de exclusões): o que o construtor incremental pula
                                  se não mudou desde IALD_PUBLICO_DESDE;
  mesclar <preparo> <tipo> <tmp>  leva ao preparo o que a rodada incremental produziu em <tmp> (pasta NOVA, esteira original):
    - entra/atualiza: arquivo produzido, se NÃO estava antes na lista local de exclusões (o que foi excluído — pela esteira ou à mão,
      com excluir_do_preparo.py — continua fora: nada volta por uma rodada incremental) e se nenhum componente do caminho é nome
      reservado do Windows;
    - sai: arquivo que estava no índice e agora a esteira exclui, e arquivo do índice cuja origem não existe mais (no núcleo: que não é
      mais rastreado pelo git da Central);
    - não se toca: work/central_publica_22out (a esteira desta abertura: atualizar_pasta_no_preparo.py, que conhece a lista ESTEIRA);
    - fica fora inteira: work/php_e_v396_22out (a auditoria de segurança de um backup privado do WordPress: configuração, caminhos da
      hospedagem, material baixado de terceiros).
  Atualiza INDICE_PUBLICO.json (com «atualizacoes»), EXCLUSOES_PUBLICAS.json (contagens) e a lista local; grava as listas para o git
  (git_add_<preparo>.txt e git_rm_<preparo>.txt, separadas por NUL, para --pathspec-from-file --pathspec-file-nul)."""
import hashlib, json, os, re, subprocess, sys, time
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
CEN = Path(r"C:\IALD\Central de Patentes")
RES = re.compile(r"(?i)^(con|prn|aux|nul|com[0-9¹²³]|lpt[0-9¹²³]|conin\$|conout\$)(\..*)?$")
NAO_TOCAR = ("central_publica_22out/",)
# os gerados depois do construtor, na raiz do preparo (README, vínculo patentário): não têm origem e não se tocam (medido por
# sondar_indices.py em 22/10/2026: sem esta lista, o passo 3 os apagaria)
GERADOS = {"README.md", "PATENTES.md", "vinculo_patentario.json", "llms.txt"}   # llms.txt: curadoria à mão (Kimi, 23/10/2026)
FORA_INTEIRA = {"php_e_v396_22out/": "auditoria de segurança de um backup privado do WordPress (configuração, caminhos da hospedagem, "
                                     "material de terceiros)"}


def longo(base, rel=""):
    s = str(base) if not rel else str(base) + "\\" + rel.replace("/", "\\")
    return s if s.startswith("\\\\?\\") else "\\\\?\\" + s


def grava_json(p, obj, indent=None):
    t = p.with_name(p.name + ".tmp_incr")
    t.write_text(json.dumps(obj, ensure_ascii=False, indent=indent), encoding="utf-8")
    assert t.stat().st_size > 0
    os.replace(t, p)


op = sys.argv[1]
D = Path(sys.argv[2])
IP, EP, LP = D / "INDICE_PUBLICO.json", D / "EXCLUSOES_PUBLICAS.json", W / ("varredura_exclusoes_%s.json" % D.name)
idx = json.loads(IP.read_text(encoding="utf-8"))
local = json.loads(LP.read_text(encoding="utf-8")) if LP.is_file() else {}
ja_fora = {x for v in local.values() for x in v}

if op == "preparar":
    vistos = sorted({a["caminho"] for a in idx["arquivos"]} | ja_fora)
    out = W / ("ja_vistos_%s.json" % D.name)
    grava_json(out, vistos)
    print("%s: %d já vistos (%d no índice, %d na lista local de exclusões) -> %s" % (D.name, len(vistos), len(idx["arquivos"]), len(ja_fora), out.name))
    sys.exit(0)

assert op == "mesclar"
TIPO, T = sys.argv[3], Path(sys.argv[4])
assert TIPO in ("nucleo", "work", "Chatgpt")
SRC = CEN if TIPO == "nucleo" else CEN / TIPO
ti = json.loads((T / "INDICE_PUBLICO.json").read_text(encoding="utf-8"))
tl = json.loads((W / ("varredura_exclusoes_%s.json" % T.name)).read_text(encoding="utf-8"))
exc = json.loads(EP.read_text(encoding="utf-8"))
por = {a["caminho"]: a for a in idx["arquivos"]}
cont = Counter()
add, rm = [], []
novos_fora = Counter()


def tocavel(rel):
    return not rel.startswith(NAO_TOCAR) and rel not in GERADOS


def fora_inteira(rel):
    for pre, m in FORA_INTEIRA.items():
        if TIPO == "work" and rel.startswith(pre):
            return m
    return None


def tirar(rel, motivo):
    p = longo(D, rel)
    if os.path.exists(p):
        os.remove(p)
    if rel in por:
        del por[rel]
        rm.append(rel)
    if motivo:
        local.setdefault(motivo, []).append(rel)
        novos_fora[motivo] += 1


# 1) o que a rodada produziu
for a in ti["arquivos"]:
    rel = a["caminho"]
    if not tocavel(rel):
        cont["não tocado (esteira da abertura)"] += 1; continue
    m = fora_inteira(rel)
    if m:
        if rel in por:
            tirar(rel, m)
        elif rel not in ja_fora:
            local.setdefault(m, []).append(rel); novos_fora[m] += 1
        cont["fora inteira: " + m[:40]] += 1; continue
    if any(RES.match(c) for c in rel.split("/")):
        if rel in por:
            tirar(rel, "nome reservado do Windows")
        cont["nome reservado do Windows (fora)"] += 1; continue
    if rel in ja_fora:
        cont["mantido fora (exclusão anterior)"] += 1; continue
    b = open(longo(T, rel), "rb").read()
    assert hashlib.sha256(b).hexdigest() == a["sha256"] and len(b) == a["bytes"], ("a rodada não confere", rel)
    ant = por.get(rel)
    if ant and ant["sha256"] == a["sha256"]:
        cont["igual (nada muda)"] += 1; continue
    os.makedirs(os.path.dirname(longo(D, rel)), exist_ok=True)
    with open(longo(D, rel), "wb") as fh:
        fh.write(b)
    por[rel] = {"caminho": rel, "bytes": a["bytes"], "sha256": a["sha256"]}
    add.append(rel)
    cont["atualizado" if ant else "adicionado"] += 1

# 2) o que a rodada excluiu: se estava publicado, sai
for motivo, rels in tl.items():
    for rel in rels:
        if not tocavel(rel):
            continue
        if rel in por:
            tirar(rel, motivo); cont["saiu (a esteira agora exclui)"] += 1
        elif rel not in ja_fora:
            local.setdefault(motivo, []).append(rel); novos_fora[motivo] += 1

# 3) o que não existe mais na origem
if TIPO == "nucleo":
    tr = set(x for x in subprocess.run(["git", "-C", str(CEN), "ls-files", "-z"], capture_output=True).stdout.decode("utf-8", "replace").split("\0") if x)
    sumidos = [r for r in list(por) if tocavel(r) and (r not in tr or not os.path.exists(longo(CEN, r)))]
else:
    sumidos = [r for r in list(por) if tocavel(r) and not os.path.exists(longo(SRC, r))]
for r in sumidos:
    tirar(r, None); cont["saiu (sumiu da origem)"] += 1

agora = time.strftime("%Y-%m-%d %H:%M:%S")
idx["arquivos"] = sorted(por.values(), key=lambda x: x["caminho"])
idx["n_arquivos"] = len(idx["arquivos"])
idx["atualizado_em"] = agora
idx.setdefault("atualizacoes", []).append({"em": agora, "motivo": "custódia v396 (22/10/2026): rodada incremental pela mesma esteira",
                                            "adicionados": cont["adicionado"], "atualizados": cont["atualizado"], "removidos": len(rm)})
for m, n in novos_fora.items():
    exc["por_motivo"][m] = exc["por_motivo"].get(m, 0) + n
exc.setdefault("atualizacoes", []).append({"em": agora, "novas_exclusoes_por_motivo": dict(novos_fora)})
grava_json(IP, idx)
grava_json(EP, exc, indent=1)
grava_json(LP, local, indent=0)
for nome, lst in (("git_add", add), ("git_rm", rm)):
    (W / ("%s_%s.txt" % (nome, D.name))).write_bytes(b"\0".join(x.encode("utf-8") for x in lst))
print("%s (%s): %s | índice agora %d | listas: git_add %d, git_rm %d" % (D.name, TIPO, dict(cont), idx["n_arquivos"], len(add), len(rm)))

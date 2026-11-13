"""Ponta a ponta do ESTADO_ATUAL com o H0DN aberto (12/11/2026, claude-site-custodia; decisão da gerência c1).

As entradas do gerar_estado_atual.py do espelho são COPIADAS para uma pasta temporária (o espelho não é tocado; nada é escrito nele).
1) o gerador ORIGINAL na cópia reproduz o ESTADO_ATUAL.md publicado, byte a byte (a cópia é fiel);
2) o E04 da G1 (h0dn.estatuto_e04) remenda os dois geradores na cópia, com os onze textos ESTATUTO_* renderizados pela frente pós-rito
   (TESTE_BLOCOS_CUSTODIA_v411.json da c1) e o registro offline no lugar do h0dn_bg1_v411;
3) o gerador REMENDADO, sem registro aberto no core, devolve o MESMO ESTADO_ATUAL.md, byte a byte;
4) com o registro injetado no core da cópia, a página é a de (1) com só estas trocas: os trechos do estatuto, as duas linhas do P2, a
   seção das ressalvas antes de «What is NOT proved», e as linhas do tamanho da página e do hash/tamanho do core (que mudou na cópia).
Uso: python -X utf8 testar_h0dn_estado_e2e.py [caminho do TESTE_BLOCOS]
"""
import difflib, json, shutil, subprocess, sys, tempfile, time
from pathlib import Path

CEN = Path(r"C:\IALD\Central de Patentes")
sys.path.insert(0, str(CEN / "tools"))
from custodia_g1 import h0dn  # noqa: E402

TB = Path(r"C:\IALD\Artigo\the_boundary")
A3 = "Um (absoluto) \u2014 Grande Atrator"
BLOCOS = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_blocos\TESTE_BLOCOS_CUSTODIA_v411.json")
REGF = CEN / "work" / "cadeia_de_selo" / "v411" / "TESTE_H0DN_OFFLINE_v411_registro.json"
RES = {"ok": 0, "falhas": []}


def caso(nome, cond, detalhe=""):
    if cond:
        RES["ok"] += 1
        print("  ok  " + nome)
    else:
        RES["falhas"].append(nome)
        print("  FALHA " + nome + ("  -> %s" % (detalhe,) if detalhe != "" else ""))


COPIADOS = []


def gerar(T):
    import re as _re
    for _ in range(60):
        r = subprocess.run([sys.executable, "-X", "utf8", str(T / "tools" / "gerar_estado_atual.py")], cwd=str(T), capture_output=True, text=True, encoding="utf-8")
        if r.returncode == 0:
            return (T / "ESTADO_ATUAL.md").read_bytes()
        m = _re.search(r"No such file or directory: '([^']+)'", r.stderr or "")
        if m:   # a entrada que faltava na cópia: só se copia o que existe no espelho, pelo mesmo caminho relativo
            falta = Path(m.group(1))
            try:
                rel = falta.resolve().relative_to(T.resolve())
            except ValueError:
                rel = None
            if rel is not None and (TB / rel).is_file() and not (T / rel).exists():
                (T / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(TB / rel, T / rel)
                COPIADOS.append(str(rel))
                continue
        raise SystemExit("gerador falhou (rc %d): %s" % (r.returncode, (r.stderr or r.stdout)[-1500:]))
    raise SystemExit("entradas demais faltando na cópia")


reg = json.loads(REGF.read_text(encoding="utf-8"))
reg = reg.get("h0dn_bg1_v411", reg)
V = h0dn.valores(reg)
selo = json.loads((TB / A3 / "um_absoluto_selo.json").read_text(encoding="utf-8"))
VS = selo["um_version"]
blocos = json.loads(BLOCOS.read_text(encoding="utf-8"))["textos"]
CORPOS = {"%s_%s" % (k, VS): blocos[k] for k in h0dn.MARCADORES_ESTATUTO}
print("textos: %s (sha16 %s); registro: %s; versão do selo da cópia: %s" % (BLOCOS.name, __import__("hashlib").sha256(BLOCOS.read_bytes()).hexdigest()[:16], REGF.name, VS))

T = Path(tempfile.mkdtemp(prefix="h0e2e_", dir=r"c:\tmp"))   # caminho curto: o da pasta temporária do sistema passa do MAX_PATH nas fontes pinadas
t0 = time.time()
try:
    (T / "tools").mkdir()
    for f in (TB / "tools").glob("*.py"):
        shutil.copyfile(f, T / "tools" / f.name)
    shutil.copytree(TB / A3, T / A3, ignore=shutil.ignore_patterns("*.bak_*", "__pycache__"))
    for rel in ("read-brief.md", "cache/gw/ECHO_ANCHORED_V2_RESULT.json", "pipelines/eco_ancorado_v1/rite_h2_v350.py", "ESTADO_ATUAL.md"):
        if (TB / rel).is_file():
            (T / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(TB / rel, T / rel)
    print("cópia em %.0f s" % (time.time() - t0))

    print("1. o gerador original na cópia")
    A = gerar(T)
    print("     entradas copiadas a pedido do gerador: %s" % (", ".join(COPIADOS) or "nenhuma"))
    caso("reproduz o ESTADO_ATUAL.md publicado, byte a byte (%d bytes)" % len(A), A == (TB / "ESTADO_ATUAL.md").read_bytes())

    print("2. o E04 da G1 na cópia, com os onze textos da frente pós-rito")
    core = json.loads((T / A3 / "um_absoluto.json").read_text(encoding="utf-8"))["core"]
    s = h0dn.estatuto_e04(T, CORPOS, VS, "h0dn_bg1_v411", V, set(), time.strftime("%Y%m%d_%H%M%S"), acervo=h0dn.acervo(core), reg=reg)
    caso("os três aplicados", s == {"estatuto_tres_apoios": "aplicado", "gerar_estado_atual_p2": "aplicado", "estatuto_h0dn.json": "aplicado"}, s)
    J = json.loads((T / "tools" / "estatuto_h0dn.json").read_text(encoding="utf-8"))

    print("3. o gerador remendado, sem registro aberto")
    A2 = gerar(T)
    caso("o MESMO ESTADO_ATUAL.md, byte a byte", A2 == A)

    print("4. com o registro injetado no core da cópia")
    mp = T / A3 / "um_absoluto.json"
    mundo = json.loads(mp.read_text(encoding="utf-8"))
    sha_core_antes = h0dn._hl.sha256(mp.read_bytes()).hexdigest()[:16] if hasattr(h0dn, "_hl") else __import__("hashlib").sha256(mp.read_bytes()).hexdigest()[:16]
    mundo["core"]["h0dn_bg1_v411"] = reg
    mp.write_text(json.dumps(mundo, ensure_ascii=False), encoding="utf-8")
    sha_core_depois = __import__("hashlib").sha256(mp.read_bytes()).hexdigest()[:16]
    B = gerar(T).decode("utf-8").replace("\r\n", "\n")
    At = A.decode("utf-8").replace("\r\n", "\n")
    # o esperado, construído de A
    l1, l2 = h0dn.TRECHOS["estado_linhas"]["p2_en_estado"], h0dn.TRECHOS["estado_linhas"]["p2_pt_estado"]
    g = {}
    exec(compile("def f():\n    L = []\n" + l1 + "\n" + l2 + "\n    return L\n", "p2", "exec"), g)   # as linhas já trazem a indentação
    p2_velhas = g["f"]()
    E = At
    for k, velho in h0dn.TRECHOS["estatuto"].items():
        E = E.replace(velho, J["textos"][k])
    caso("as duas linhas do P2 de hoje estão uma vez na página", all(E.count(x) == 1 for x in p2_velhas))
    E = E.replace(p2_velhas[0], J["textos"]["p2_en_estado"]).replace(p2_velhas[1], J["textos"]["p2_pt_estado"])
    sec = "\n".join(h0dn.secao_estado("h0dn_bg1_v411", reg))
    anc = "\n\n## What is NOT proved \u00b7 o que N\u00c3O est\u00e1 provado"
    caso("a âncora «What is NOT proved» uma vez", E.count(anc) == 1)
    E = E.replace(anc, "\n\n" + sec + anc)
    caso("a seção está na página gerada, uma vez", B.count(sec) == 1)
    caso("a seção vem logo antes de «What is NOT proved»", (sec + anc) in B)
    resto = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, E.split("\n"), B.split("\n"), autojunk=False).get_opcodes():
        if op == "equal":
            continue
        a_, b_ = E.split("\n")[i1:i2], B.split("\n")[j1:j2]
        if len(a_) == len(b_) and all(("KB" in x and "KB" in y) or (sha_core_antes in x and sha_core_depois in y) or
                                      (x.replace(sha_core_antes, sha_core_depois) == y) for x, y in zip(a_, b_)):
            continue
        resto.append((op, a_[:2], b_[:2]))
    caso("fora as trocas esperadas, só mudam o tamanho da página e o hash/tamanho do core", not resto, [(o, [x[:140] for x in a], [y[:140] for y in b]) for o, a, b in resto[:4]])
    caso("nenhum trecho velho do fator aberto sobrou", not any(v in B for v in h0dn.TRECHOS["estatuto"].values()) and not any(x in B for x in p2_velhas))
    # a página de hoje já tem 3 blocos que a F67 marca: a linha, a errata e o parágrafo da v410, que descrevem a cabeça pré-registrada do ramo
    # de 5σ («only a future opening can return», D76). São registro da v410; o que se exige aqui é que a v411 não acrescente bloco nenhum
    f67_hoje, f67_aberto = {t for _, t in h0dn.f67(At)}, h0dn.f67(B)
    novos_f67 = [x for x in f67_aberto if x[1] not in f67_hoje]
    print("     F67: %d bloco(s) já marcados na página de hoje (registro da v410); %d na página com o H0DN aberto" % (len(f67_hoje), len(f67_aberto)))
    caso("o ESTADO com o H0DN aberto não acrescenta bloco que falhe na F67", not novos_f67, novos_f67[:3])
    print("     ESTADO_ATUAL de hoje %d bytes; com o H0DN aberto (ensaio) %d bytes" % (len(At.encode("utf-8")), len(B.encode("utf-8"))))
    caso("o espelho real não foi tocado", not (TB / "tools" / "estatuto_h0dn.json").exists() and h0dn.MARCA_HOOK not in (TB / "tools" / "gerar_estado_atual.py").read_text(encoding="utf-8")
         and (TB / "ESTADO_ATUAL.md").read_bytes() == A)
finally:
    shutil.rmtree(T, ignore_errors=True)

print("\nRESULTADO: %d ok, %d falha(s)%s" % (RES["ok"], len(RES["falhas"]), (": " + "; ".join(RES["falhas"])) if RES["falhas"] else ""))
sys.exit(1 if RES["falhas"] else 0)

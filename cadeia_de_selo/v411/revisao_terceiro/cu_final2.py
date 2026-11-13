# -*- coding: utf-8 -*-
"""CU-FINAL2: regrava o registro depois da correcao do CU-1 pela gerencia. Antes de sobrescrever: guarda os bytes do registro atual como .CU.R0.json/.md (ao lado). Hashes lidos do disco AGORA."""
import hashlib, json, os, shutil, time
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
RT = os.path.join(V, "revisao_terceiro")
sha16 = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
cur_j, cur_m = os.path.join(RT, "REVISAO_TERCEIRO_v411.CU.json"), os.path.join(RT, "REVISAO_TERCEIRO_v411.CU.md")
assert sha16(cur_j) == "4c459e5c37a7f90b", sha16(cur_j)
r0j, r0m = os.path.join(RT, "REVISAO_TERCEIRO_v411.CU.R0.json"), os.path.join(RT, "REVISAO_TERCEIRO_v411.CU.R0.md")
assert not os.path.exists(r0j) and not os.path.exists(r0m)
shutil.copyfile(cur_j, r0j)
shutil.copyfile(cur_m, r0m)
assert open(r0j, "rb").read() == open(cur_j, "rb").read() and open(r0m, "rb").read() == open(cur_m, "rb").read()
R0_J16, R0_M16 = sha16(r0j), sha16(r0m)
R = json.load(open(cur_j, encoding="utf-8"))

# --- conferencia dos arquivos revisados: so' o gerar_relatorio mudou
cand = os.path.join(V, "um_v411_candidato.py")
fim16 = sha16(cand)
assert fim16 == R["candidato_sha16_no_inicio"] == "1203b1f9202020d6"
novo = {}
mudaram = []
for rel, h in R["arquivos_revisados"].items():
    p = os.path.join(V, rel.replace("/", os.sep))
    assert os.path.isfile(p), rel
    h2 = sha16(p)
    novo[rel] = h2
    if h2 != h:
        mudaram.append((rel, h, h2))
print("arquivos revisados que mudaram:", mudaram)
assert [m[0] for m in mudaram] == ["gerar_relatorio_v411.py"], mudaram
assert mudaram[0][1] == "155670de1d7dc22e" and mudaram[0][2] == "3a252f63cd372b75"
R["arquivos_revisados"] = novo
for k in R["artefatos_renderizados_lidos"]:
    R["artefatos_renderizados_lidos"][k] = sha16(k)

# --- CU-1 sai de achados; vai para a chave nova
cu1 = [a for a in R["achados"] if a["id"] == "CU-1"][0]
R["achados"] = [a for a in R["achados"] if a["id"] != "CU-1"]
R["achados_da_conferencia_resolvidos"] = [{
    "id": "CU-1", "sev": "MEDIO",
    "o_que_era": cu1["achado"][:900] + " (texto completo no registro R0)",
    "correcao_aplicada": "Comentario do C-10 movido do meio da expressao do portao kernel para o fim dela (depois do ultimo parentese da linha 113), com uma nota do CU-1; nenhuma condicao mudada. gerar_relatorio_v411.py: sha16 155670de1d7dc22e -> 3a252f63cd372b75; backup de bytes gerar_relatorio_v411.py.bak_20261112_234336_cu1fix.",
    "quem_aplicou": "a gerencia c1 (nao o construtor, nao o revisor); o candidato nao foi tocado",
    "como_conferi": "cu_r2.py e o comando seco: (1) diff do backup _cu1fix contra o de hoje: um unico hunk, linhas 112 e 113 (@@ -112,2 +112,2 @@), e o resto do arquivo igual linha a linha; (2) por AST o portao kernel tem 13 condicoes: as 12 do estado de antes do conserto (backup _r1fix, 9bf6956723bc5232), todas presentes e na mesma ordem (PB.ok, criterios do POS_BUILD e n_modulos_compilados de volta), mais a das chaves do C-10; dos 29 portoes de PORTOES so' o kernel difere do backup; (3) compila em memoria; (4) gerar_relatorio_v411.py --seco: portoes ok 30/30, falta vazio, guarda das frases e P18 limpa, e as datas de PLANO, RELATORIO e PRONTA nao mudaram (nada gravado); (5) o candidato segue 1203b1f9202020d6 e nenhum outro arquivo de arquivos_revisados mudou (34 relidos)."}]
R["n_alto"] = sum(1 for a in R["achados"] if a["sev"] == "ALTO")
R["n_medio"] = sum(1 for a in R["achados"] if a["sev"] == "MEDIO")
R["n_baixo"] = sum(1 for a in R["achados"] if a["sev"] == "BAIXO")
for x in R["situacao_dos_achados_da_R1"]:
    if x["id"] == "C-10":
        x["situacao"] = "resolvido (depois da correcao do CU-1 pela gerencia)"
        x["como_conferi"] = "a primeira conferencia achou que o conserto acrescentou a exigencia das chaves mas desligou tres condicoes por um comentario no meio da expressao (CU-1); a gerencia moveu o comentario para o fim; reconferido: o portao kernel tem 13 condicoes (as 12 de antes do conserto mais a das chaves), o arquivo compila e --seco da 30/30"
R["conferencias"]["E"] = R["conferencias"]["E"].replace("Aberto: CU-1.", "A regressao CU-1 foi achada aqui e esta' resolvida (ver achados_da_conferencia_resolvidos e historico).")
R["ressalvas"][0] = R["ressalvas"][0] + " Excecao na reconferencia do CU-1: rodei, so' com --seco e sem gravar nada, o gerar_relatorio_v411.py, a pedido da coordenacao."

agora = time.strftime("%Y-%m-%dT%H:%M:%S")
ant = R["quando"]
R["quando"] = agora
R["historico"] = [
    {"quando": ant, "evento": "primeira gravacao desta conferencia: aprovada false por um achado MEDIO dentro do escopo (CU-1: comentario no meio da linha 112 de gerar_relatorio_v411.py desligou tres condicoes do portao kernel); bytes guardados em REVISAO_TERCEIRO_v411.CU.R0.json e .md (sha16 %s e %s)" % (R0_J16, R0_M16)},
    {"quando": agora, "evento": "a gerencia c1 aplicou a correcao minima pedida (o comentario foi para o fim da expressao, nenhuma condicao mudada; gerar_relatorio_v411.py 155670de1d7dc22e -> 3a252f63cd372b75) e o revisor a reconferiu SO' nesse item (escopo fechado, nada novo); nenhum ALTO nem MEDIO resta no escopo"}]
R["aprovada"] = bool(R["n_alto"] == 0 and R["n_medio"] == 0)
R["candidato_sha16"] = fim16
R["candidato_bytes"] = os.path.getsize(cand)
R["candidato_mudou_durante_a_revisao"] = False
R["criterio_D109"] = "aprovada true so' se nao restar ALTO nem MEDIO dentro do escopo A a F; achado fora do escopo vai para as ressalvas da versao seguinte e nao bloqueia, salvo um ALTO para o rito. Depois da reconferencia do CU-1: 0 ALTO, 0 MEDIO abertos; os BAIXOS abertos (17, sendo 15 ressalvas da R1 e 2 novos: CU-2, CU-3) nao bloqueiam."
R["nota"] = ("Aprovada, depois da reconferencia unica do CU-1. A primeira gravacao reprovou por um MEDIO: um comentario no meio da linha 112 de gerar_relatorio_v411.py desligara PB.ok, os criterios do POS_BUILD e n_modulos_compilados no portao kernel do relatorio. A gerencia moveu o comentario para o fim e eu reconferi: so' as linhas 112 e 113 mudaram, o portao volta a ter as 12 condicoes de antes do conserto mais a das chaves (13), o arquivo compila e o --seco da 30/30. Tudo o que eu conferi nos itens A, B, C, D e F continua limpo e nao foi refeito; o candidato e' o mesmo (1203b1f9202020d6). Esta e' a unica conferencia (D109): ficam os BAIXOS abertos, que nao bloqueiam; as ressalvas e o que NAO fiz continuam valendo; a decisao final do que se instala e' da gerencia e do operador.")
for r in R["rotas_examinadas"]:
    if "resultado" in r:
        r["resultado"] = "um achado MEDIO novo, CU-1 (gerar_relatorio_v411.py l.112), RESOLVIDO pela gerencia e reconferido; tres BAIXOS; todo o resto confere"


def md(R):
    L = ["# REVISAO DE TERCEIRO v411 -- CONFERENCIA UNICA do conserto da R1 (D109), regravada depois da correcao do CU-1", ""]
    L.append("- aprovada: **%s**; candidato `%s` (%d bytes; no inicio `%s`; mudou durante a revisao: %s)" % ("SIM" if R["aprovada"] else "NAO", R["candidato_sha16"], R["candidato_bytes"], R["candidato_sha16_no_inicio"], R["candidato_mudou_durante_a_revisao"]))
    L.append("- revisor: %s; quando: %s" % (R["revisor"], R["quando"]))
    L.append("- abertos: ALTO %d, MEDIO %d, BAIXO %d (dos BAIXOS, 15 sao ressalvas da R1 que o conserto nao fez, por ordem)" % (R["n_alto"], R["n_medio"], R["n_baixo"]))
    L.append("- a primeira gravacao (reprovada) esta' ao lado: `REVISAO_TERCEIRO_v411.CU.R0.json` (sha16 `%s`) e `.md` (`%s`)" % (R0_J16, R0_M16))
    L += ["", "## Historico"]
    for h in R["historico"]:
        L.append("- %s: %s" % (h["quando"], h["evento"]))
    L += ["", "## Nota", R["nota"], "", "## Achados da conferencia, resolvidos"]
    for a in R["achados_da_conferencia_resolvidos"]:
        L.append("### %s -- %s, RESOLVIDO" % (a["id"], a["sev"]))
        L.append("- **o que era:** %s" % a["o_que_era"])
        L.append("- **correcao aplicada:** %s" % a["correcao_aplicada"])
        L.append("- **quem aplicou:** %s" % a["quem_aplicou"])
        L.append("- **como conferi:** %s" % a["como_conferi"])
    L += ["", "## Achados abertos"]
    for a in R["achados"]:
        if a["id"].startswith("CU-"):
            L.append("### %s -- %s (dentro do escopo: %s)" % (a["id"], a["sev"], "sim" if a["dentro_do_escopo"] else "nao"))
            L.append("- **onde:** %s" % a["onde"])
            L.append("- **o que:** %s" % a["achado"])
            L.append("- **correcao pedida:** %s" % a["correcao_pedida"])
    L += ["", "Ressalvas da R1 que ficam (BAIXO, fora do escopo): " + ", ".join(a["id"] for a in R["achados"] if not a["id"].startswith("CU-")) + ".", "", "## Situacao dos achados da R1"]
    for x in R["situacao_dos_achados_da_R1"]:
        L.append("- **%s** (%s na R1): %s. %s" % (x["id"], x["sev_na_R1"], x["situacao"], x["como_conferi"]))
    L += ["", "## Conferencias (itens A a F)"]
    for k, v in R["conferencias"].items():
        L += ["### %s" % k, v]
    L += ["", "## Ressalvas (o que NAO fiz)"] + ["- " + r for r in R["ressalvas"]]
    L += ["", "## Para a versao seguinte"] + ["- " + r for r in R["ressalvas_para_a_versao_seguinte"]]
    L += ["", "## Rotas examinadas"] + ["- " + json.dumps(r, ensure_ascii=False) for r in R["rotas_examinadas"]]
    L += ["", "## Criterio", R["criterio_D109"], "", "## Arquivos revisados (sha16 lido no fim)"] + ["- `%s` `%s`" % (k, v) for k, v in R["arquivos_revisados"].items()]
    L += ["", "## Artefatos renderizados lidos"] + ["- `%s` `%s`" % (k, v) for k, v in R["artefatos_renderizados_lidos"].items()]
    return "\n".join(L) + "\n"


def grava(path, data):
    tmp = path + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    assert os.path.getsize(tmp) == len(data) > 0
    os.replace(tmp, path)


jb = (json.dumps(R, ensure_ascii=False, indent=1) + "\n").encode("utf-8")
mb = md(R).encode("utf-8")
grava(cur_j, jb)
grava(cur_m, mb)
grava(os.path.join(RT, "REVISAO_TERCEIRO_v411.json"), jb)
grava(os.path.join(RT, "REVISAO_TERCEIRO_v411.md"), mb)
# releitura final dos arquivos revisados e do candidato
fim2 = {k: sha16(os.path.join(V, k.replace("/", os.sep))) for k in R["arquivos_revisados"]}
assert fim2 == R["arquivos_revisados"] and sha16(cand) == fim16
print("aprovada:", R["aprovada"], "| alto/medio/baixo:", R["n_alto"], R["n_medio"], R["n_baixo"], "| candidato", fim16)
for n in ("REVISAO_TERCEIRO_v411.CU.json", "REVISAO_TERCEIRO_v411.json", "REVISAO_TERCEIRO_v411.CU.md", "REVISAO_TERCEIRO_v411.md", "REVISAO_TERCEIRO_v411.CU.R0.json", "REVISAO_TERCEIRO_v411.CU.R0.md"):
    p = os.path.join(RT, n)
    print(n, sha16(p), os.path.getsize(p))
print("copias identicas:", open(cur_j, "rb").read() == open(os.path.join(RT, "REVISAO_TERCEIRO_v411.json"), "rb").read(), open(cur_m, "rb").read() == open(os.path.join(RT, "REVISAO_TERCEIRO_v411.md"), "rb").read())

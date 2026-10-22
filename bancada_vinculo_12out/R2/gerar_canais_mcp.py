# -*- coding: utf-8 -*-
"""gerar_canais_mcp.py (R2, 13/10/2026) -- conserto A13 da auditoria: a guarda de palavra e aplicada a DECLARACAO INTEIRA em gerar(),
antes de escrever qualquer modulo (PALAVRA_PROIBIDA_NA_DECLARACAO); na R1 (41cb29289eb99702) so o modulo gerado a tinha, em codigo morto.

Origem R1: a CONVENCAO «registro do um.py -> ferramenta da Bancada», por GERACAO a partir dos registros (esboco, 12/10/2026).

Entrada: CANAIS_vNNN.json (um por versao, escrito pela cadeia de selo junto dos pinos; aqui um EXEMPLO extraido por script do um.py v391:
os 18 artefatos que o registro `bancada_fases_5_6_7_v380` le do cache do rito, por hash). Para cada canal declarado o gerador emite:
  * bancada/registros_gerados.py  -- um modulo PINADO no manifesto (code), com a tabela CANAIS e a funcao consultar(nome): confere a
    identidade por operacao (require_current), confere o sha256 de CADA artefato do canal contra a declaracao, confere o core (um_absoluto.json)
    contra o selo pinado e devolve o veredito SELADO daquele registro lido do core -- nunca recalcula, nunca abre dado;
  * mcp_registros_gerados.py      -- uma ferramenta MCP por canal (registro_<nome>), que chama GET /api/registro/<nome>;
  * um_bancada_rota_registro.pysnip -- a rota generica que a B3 instala UMA vez em um_bancada.py: depois disso, canal novo = so o modulo gerado;
  * TESTES_CANAIS_GERADOS.json    -- a declaracao dos testes que a bateria ganha por canal (T18+): hash de cada artefato, veredito do core
    igual ao do selo, guarda de palavra, gate NONE.
Canais de CALCULO (um dissipador, um estimador) continuam escritos a mao, como a B2 fez; a convencao obriga a declara-los em CANAIS_vNNN.json
com ferramenta e teste, e o sincronizar_bancada.py recusa canal sem ferramenta ou sem teste (CANAL_SEM_FERRAMENTA / CANAL_SEM_TESTE).
uso: gerar_canais_mcp.py <CANAIS_vNNN.json> <dir de saida (novo)>
"""
import sys
sys.dont_write_bytecode = True
import ast, hashlib, json, re, datetime
from pathlib import Path
NOS = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
CACHE = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache")   # o um.py escolhe por medida: ..\cache tem lensing/ e Nós\cache nao


def sha(b):
    return hashlib.sha256(b).hexdigest()


# a guarda da regua (a mesma do um.py, do iald.py e do sincronizar_bancada.py), montada em pedacos para que o token nunca exista neste arquivo
GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")


def exemplo_v391(dst):
    """Extrai POR SCRIPT do um.py v391 o dicionario _V380_FILES (l.197564-197571) e escreve CANAIS_v391_exemplo.json."""
    raw = (NOS / "um.py").read_bytes()
    txt = raw.decode("utf-8-sig")
    m = re.search(r"^_V380_FILES = \{(.*?)^\}", txt, re.M | re.S)
    if not m:
        raise SystemExit("_V380_FILES nao encontrado no um.py")
    files = ast.literal_eval("{" + m.group(1) + "}")
    core = json.loads((NOS / "um_absoluto.json").read_bytes())["core"]
    selo = json.loads((NOS / "um_absoluto_selo.json").read_bytes())
    arts = []
    for k, (sub, fn) in files.items():
        p = CACHE / sub / fn
        b = p.read_bytes()
        arts.append(dict(chave=k, path=str(p), sha256=sha(b), bytes=len(b)))
    canais = dict(versao="v391", um_py_sha256=sha(raw), selo_sha256=sha((NOS / "um_absoluto_selo.json").read_bytes()),
                  quando=datetime.datetime.now().isoformat(timespec="seconds"),
                  nota="EXEMPLO extraido por script (regex + ast.literal_eval sobre _V380_FILES do um.py v391); na cadeia, CANAIS_vNNN.json nasce do gerar_candidato junto dos pinos",
                  canais=[dict(nome="bancada_fases_5_6_7_v380", funcao_um_py="prove_bancada_fases_5_6_7_v380", registro_core="bancada_fases_5_6_7_v380",
                               chave_selo="the_bancada_fases_5_6_7_reading_v380", tipo="LEITURA_POR_HASH",
                               descricao="As Fases 5, 6 e 7 da Bancada Um, o banco de GW e as erratas ao lado, lidos por hash do cache do rito (v380).",
                               artefatos=arts, veredito_selado=core["bancada_fases_5_6_7_v380"]["verdict"],
                               leitura_no_selo=selo.get("the_bancada_fases_5_6_7_reading_v380"),
                               ferramenta_mcp="registro_bancada_fases_5_6_7_v380", rota="/api/registro/bancada_fases_5_6_7_v380",
                               teste=dict(id="T18_REGISTRO_bancada_fases_5_6_7_v380", exige=["hash de cada artefato", "veredito do core == veredito do selo", "guarda de palavra", "gate NONE"]))])
    dst.write_text(json.dumps(canais, ensure_ascii=False, indent=1), encoding="utf-8")
    return canais


def gerar(canais, outdir):
    outdir = Path(outdir)
    decl_txt = json.dumps(canais, ensure_ascii=False, sort_keys=True)
    # A13: a declaracao inteira (vereditos, descricoes, leituras do selo, nomes) passa pela guarda ANTES de qualquer modulo nascer
    if GUARDA.search(decl_txt.replace("NOT_CONF" + "IRMED", "").replace("UNCONF" + "IRMED", "")):
        raise SystemExit("PALAVRA_PROIBIDA_NA_DECLARACAO: nenhum modulo gerado")
    decl_sha = sha(decl_txt.encode("utf-8"))
    faltas = [c["nome"] for c in canais["canais"] if not c.get("ferramenta_mcp") or not c.get("teste")]
    if faltas:
        raise SystemExit("CANAL_SEM_FERRAMENTA_OU_SEM_TESTE: " + ", ".join(faltas))
    outdir.mkdir(parents=True, exist_ok=False)   # so depois das guardas: uma declaracao recusada nao deixa pasta
    tabela = {c["nome"]: dict(registro_core=c["registro_core"], chave_selo=c.get("chave_selo"), tipo=c["tipo"], descricao=c["descricao"],
                              artefatos=[dict(chave=a["chave"], path=a["path"], sha256=a["sha256"], bytes=a["bytes"]) for a in c["artefatos"]],
                              veredito_selado=c["veredito_selado"], leitura_no_selo=c.get("leitura_no_selo")) for c in canais["canais"]}
    mod = ('# -*- coding: utf-8 -*-\n"""bancada/registros_gerados.py -- GERADO por gerar_canais_mcp.py (declaracao CANAIS_%s sha256 %s). NAO EDITAR A MAO.\n'
           'Cada canal e a LEITURA POR HASH de um registro selado do um.py: confere identidade por operacao, cada artefato por sha256, o core contra o selo,\n'
           'e devolve o veredito SELADO. Nunca recalcula; nunca abre dado observado; nenhum efeito no gate."""\n'
           'import hashlib, json, re\nfrom pathlib import Path\nfrom bancada.canonical import require_current, get_registry\n\n'
           'GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")\n'
           'CANAIS = %s\n\n\n'
           'def consultar(nome, root=None):\n'
           '    if nome not in CANAIS:\n        raise ValueError("CANAL_DESCONHECIDO: " + str(nome))\n'
           '    rc = require_current("registro:" + nome, root)\n    c = CANAIS[nome]\n    reg = get_registry(root)\n'
           '    selo = json.loads(Path(reg.manifest["canonical"]["seal"]["path"]).read_bytes())\n'
           '    core_p = Path(reg.manifest["canonical"]["seal"]["path"]).with_name("um_absoluto.json")\n    core_raw = core_p.read_bytes()\n'
           '    if (selo.get("sha256") or {}).get("um_absoluto.json") != hashlib.sha256(core_raw).hexdigest():\n'
           '        raise ValueError("CORE_NAO_PINADO_PELO_SELO")\n'
           '    core = json.loads(core_raw)["core"]\n    arts = []\n'
           '    for a in c["artefatos"]:\n        b = Path(a["path"]).read_bytes()\n'
           '        if len(b) != a["bytes"] or hashlib.sha256(b).hexdigest() != a["sha256"]:\n'
           '            raise ValueError("ARTEFATO_DIVERGE_DA_DECLARACAO: " + a["path"])\n'
           '        arts.append(dict(chave=a["chave"], path=a["path"], sha256=a["sha256"], bytes=a["bytes"]))\n'
           '    reg_core = core.get(c["registro_core"]) or {}\n    veredito = reg_core.get("verdict")\n'
           '    if veredito != c["veredito_selado"]:\n        raise ValueError("VEREDITO_DO_CORE_DIFERE_DO_DECLARADO")\n'
           '    if c.get("chave_selo") and selo.get(c["chave_selo"]) != c.get("leitura_no_selo"):\n'
           '        raise ValueError("LEITURA_DO_SELO_DIFERE_DA_DECLARADA")\n'
           '    if GUARDA.search(str(veredito).replace("NOT_CONF" + "IRMED", "")):\n        raise ValueError("PALAVRA_PROIBIDA_NO_VEREDITO")\n'
           '    return dict(ok=True, canal=nome, tipo=c["tipo"], descricao=c["descricao"], artefatos=arts, veredito_selado=veredito, leitura_no_selo=c.get("leitura_no_selo"),\n'
           '                all_verified=reg_core.get("all_verified"), statute=reg_core.get("statute"), canonical=rc,\n'
           '                scope="LEITURA_POR_HASH_DO_SELADO; NAO_RECALCULA; NAO_E_LEITURA_FISICA", gate_effect="NONE")\n'
           % (canais["versao"], decl_sha, json.dumps(tabela, ensure_ascii=False, indent=1)))
    mcp = ('# -*- coding: utf-8 -*-\n"""mcp_registros_gerados.py -- GERADO por gerar_canais_mcp.py (CANAIS_%s %s). Uma ferramenta por registro selado; cada uma\n'
           'chama GET /api/registro/<nome> na Bancada (que confere a identidade e os hashes). NAO EDITAR A MAO."""\n'
           'import json, os, urllib.request\nfrom mcp.server.fastmcp import FastMCP\n'
           'URL = os.environ.get("BANCADA_UM_URL", "http://127.0.0.1:18777")\nmcp = FastMCP("bancada-um-registros")\n\n\n'
           'def _req(caminho):\n    try:\n        with urllib.request.urlopen(URL + caminho, timeout=120) as f:\n            return json.loads(f.read().decode("utf-8"))\n'
           '    except Exception as e:\n        return dict(erro="Bancada Um fora do ar ou recusou: %%r" %% (e,))\n\n' % (canais["versao"], decl_sha[:16]))
    for c in canais["canais"]:
        mcp += ('\n@mcp.tool(description=%r)\ndef %s() -> dict:\n    """Leitura por hash do registro selado %s (%s). Nunca recalcula; gate NONE."""\n    return _req(%r)\n\n'
                % (c["descricao"][:200], c["ferramenta_mcp"], c["registro_core"], canais["versao"], c["rota"]))
    mcp += '\nif __name__ == "__main__":\n    mcp.run()\n'
    rota = ('# um_bancada_rota_registro.pysnip -- a rota GENERICA que a B3 instala UMA vez em um_bancada.py (dentro do do_GET, depois de /api/contratos):\n'
            '            if caminho.startswith("/api/registro/"):\n'
            '                from bancada import registros_gerados\n'
            '                return self._json(registros_gerados.consultar(caminho.split("/")[3], root=RAIZ))\n'
            '# depois disso, um canal novo = so o modulo gerado (pinado como code pelo sincronizar_bancada.py) + a ferramenta gerada: nenhum codigo do servidor muda.\n')
    testes = dict(declaracao_sha256=decl_sha, testes=[dict(id=c["teste"]["id"], canal=c["nome"], exige=c["teste"]["exige"],
                  verificacao=dict(tipo="json_igual", campos={"ok": True, "veredito_selado": c["veredito_selado"], "gate_effect": "NONE"})) for c in canais["canais"]])
    for nome, texto in (("registros_gerados.py", mod), ("mcp_registros_gerados.py", mcp), ("um_bancada_rota_registro.pysnip", rota)):
        (outdir / nome).write_text(texto, encoding="utf-8")
    (outdir / "TESTES_CANAIS_GERADOS.json").write_text(json.dumps(testes, ensure_ascii=False, indent=1), encoding="utf-8")
    rec = {n: dict(sha256=sha((outdir / n).read_bytes()), bytes=(outdir / n).stat().st_size) for n in ("registros_gerados.py", "mcp_registros_gerados.py", "um_bancada_rota_registro.pysnip", "TESTES_CANAIS_GERADOS.json")}
    (outdir / "GERACAO_RECIBO.json").write_text(json.dumps(dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), declaracao_sha256=decl_sha, gerados=rec), ensure_ascii=False, indent=1), encoding="utf-8")
    return rec


if __name__ == "__main__":
    decl, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    canais = exemplo_v391(decl) if not decl.exists() else json.loads(decl.read_bytes())
    rec = gerar(canais, outdir)
    print(json.dumps(rec, indent=1))

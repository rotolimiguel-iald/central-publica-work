# -*- coding: utf-8 -*-
"""O um.acom PÚBLICO da Central (ordem do operador, 22/10/2026: «a possibilidade, inclusive, de modo público, de colapsarem a central
inteira em um.acom e baixarem na sua própria máquina, esse é o único acesso público de baixar direto na central ... porque é um método de
demonstrar o acom e liberar todos os códigos»).
Usa o PRÓPRIO dispositivo da Central (backend/app/um_acom.py: árvore -> tar -> ACOM sem perdas -> AES-256-GCM -> contêiner TGLACOM1),
com a chave universal pública da casa (a mesma declarada no site para a oncologia). A árvore segue o critério público do operador:
  - fica: o núcleo da TGL (TGL_CORE_MEMORY, com os dados pessoais mascarados e as notas operacionais omitidas, à vista), a forma canônica,
    a fronteira teórica; por patente: o código FINAL, o manifesto de integridade, o selo de rodagem, a cadeia de prova verificada e o
    VÍNCULO PATENTÁRIO (número, título, depósito, prioridade, jurisdição, PCT: «pedido de patente depositado»);
  - sai: a memória/leitura de cada patente, prazos, lembretes, alertas, anuidades, ações de escritório, recibos e pagamentos.
Depois de selar, ABRE de volta com o mesmo módulo e confere cada SHA-256 e a meta-cadeia. Uso: <python do backend> gerar_um_acom_publico.py <pasta_saida>"""
import hashlib, json, sys, time
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
sys.path.insert(0, r"C:\IALD\Central de Patentes\backend")
from mascara_pii import mascarar            # noqa: E402
from filtro_operacional import filtrar_markdown  # noqa: E402
from app import um_acom as UM               # noqa: E402
from app import config as C                 # noqa: E402
import yaml                                 # noqa: E402
from vinculo_patentario import ler_vinculos  # noqa: E402  (a fonte única do vínculo: os dockets, só os campos do vínculo)
VS = {v["dir"]: v for v in ler_vinculos()}

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
files, mascaras = {}, {}


def add(path, data, texto=False, markdown=False):
    if data is None:
        return
    if texto:
        t = data.decode("utf-8", "replace")
        t, c = mascarar(t)
        if markdown:
            t, n = filtrar_markdown(t)
            if n:
                c["notas_operacionais_omitidas"] = n
        if c:
            mascaras[path] = c
        data = t.encode("utf-8")
    files[UM._safe_tree_name(path)] = data


add("tgl/TGL_CORE_MEMORY.md", UM._read(C.MEMORY / "TGL_CORE_MEMORY.md"), texto=True, markdown=True)
vault = C.CENTRAL / "vault" / "originals_copy" / "um_unificado_v33"
add("tgl/forma_canonica.md", UM._read(vault / "um_grande_atrator_forma_canonica.md"), texto=True, markdown=True)
add("tgl/um_grande_atrator_manifest.md", UM._read(vault / "um_grande_atrator_manifest.md"), texto=True)
add("tgl/CUSTODY_MANIFEST.json", UM._read(vault / "CUSTODY_MANIFEST.json"), texto=True)
front = C.CENTRAL / "fronteira_tgl"
add("tgl/fronteira/fronteira_render3d.json", UM._read(front / "render3d.json"), texto=True)
fseal = UM._latest(front / "results", "fronteira_*.json")
add("tgl/fronteira/fronteira_selo.json", UM._read(fseal) if fseal else None, texto=True)
vinculos = []
for pdir in sorted(C.PATENTS_DIR.iterdir()):
    if not pdir.is_dir() or not pdir.name.startswith("BR"):
        continue
    base = pdir.name
    final = UM._latest(pdir, "*_FINAL.py")
    if final:
        add(f"{base}/{final.name}", UM._read(final))
        man = pdir / (final.name.rsplit(".py", 1)[0] + ".manifest.json")
        add(f"{base}/{man.name}", UM._read(man), texto=True)
    seal = UM._latest(pdir / "results", "*.json")
    if seal:
        add(f"{base}/selo_rodagem.json", UM._read(seal), texto=True)
    add(f"{base}/evidence_verified.json", UM._read(pdir / "evidence_verified.json"), texto=True)
    v = {k: VS[base][k] for k in VS[base] if k != "dir"}
    vinculos.append(v)
    add(f"{base}/vinculo_patentario.json", json.dumps(v, ensure_ascii=False, indent=1).encode("utf-8"), texto=True)
meta_chain = UM._meta_chain(files)
manifest = {"artifact": "um.acom (a Central pública)", "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "beta_provenance": UM.beta_provenance(), "n_files": len(files), "meta_chain": meta_chain,
            "files": [{"path": p, "sha256": hashlib.sha256(files[p]).hexdigest(), "size": len(files[p])} for p in sorted(files)],
            "criterio_publico": "dados pessoais mascarados à vista; notas operacionais do operador (prazos, protocolo, leituras) fora",
            "note": "Selo do selo: a meta-cadeia é o SHA-256 de todos os 'path:sha256' ordenados. physical_verdict_allowed=false; 1 = 1."}
files["tgl/MANIFESTO.json"] = json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")
files["tgl/LEIA-ME.md"] = (
    "# um.acom — a Central pública da TGL, num único arquivo\n\n"
    "A Central inteira colapsada num único `.acom`: comprimida pelo dispositivo ACOM (sem perdas; cada arquivo conferido por SHA-256) e "
    "selada com a criptografia da casa (Túnel de Hilbert + AES-256-GCM). A chave é a universal pública da casa, declarada no site.\n\n"
    "## O que há dentro\n- `tgl/` — o núcleo canônico da TGL, a forma canônica e a fronteira teórica (o selo vivo).\n"
    "- %d pastas de patente — o código FINAL, o manifesto de integridade, o selo de rodagem, a cadeia de prova verificada e o vínculo "
    "patentário (`vinculo_patentario.json`: o número do pedido no INPI, o depósito, a prioridade e o PCT — pedido depositado, não "
    "patente concedida).\n- `tgl/MANIFESTO.json` — a meta-cadeia (o selo do selo).\n\n"
    "Dados pessoais aparecem como «[dado pessoal removido]»; as notas operacionais do operador ficam na Central dele.\n\n"
    "## Selo\nmeta-cadeia = `%s`\n\nβ = α·√e (nunca literal). Nenhum veredito físico. **1 = 1.**\n" % (len(vinculos), meta_chain)).encode("utf-8")
cont = UM.build(files, UM.ONCOLOGIA_KEY, {"origin": "central-publica", "n_patents": len(vinculos), "chave": "universal pública"})
ab = UM.open_container(cont, UM.ONCOLOGIA_KEY)
assert ab["ok"] and ab["all_files_verified"] and ab["meta_chain_ok"] and ab["n_files"] == len(files), "o um.acom não abriu inteiro — PARAR"
for p, b in files.items():
    assert hashlib.sha256(ab["_files"][p]).hexdigest() == hashlib.sha256(b).hexdigest(), p
sh = hashlib.sha256(cont).hexdigest()
(OUT / "um.acom").write_bytes(cont)
info = {"arquivo": "um.acom", "chave_publica": UM.ONCOLOGIA_KEY, "sha256": sh, "bytes": len(cont), "n_arquivos": len(files),
        "meta_chain": meta_chain, "gerado_em": time.strftime("%d/%m/%Y %H:%M"), "formato": "TGLACOM1 (tgl.acom v%d)" % UM.FORMAT_VERSION,
        "conferido": "aberto de volta com a chave pública: %d de %d arquivos conferidos por SHA-256; meta-cadeia confere" % (len(files), len(files)),
        "mascaras_de_dado_pessoal": mascaras}
(OUT / "um_acom_info.json").write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
(OUT / "vinculo_patentario.json").write_text(json.dumps(vinculos, ensure_ascii=False, indent=1), encoding="utf-8")
print("um.acom público: %d arquivos na árvore | %d bytes | sha256 %s | conferido %d/%d | máscaras em %d arquivo(s)" % (
    len(files), len(cont), sh[:16], len(files), len(files), len(mascaras)))

# -*- coding: utf-8 -*-
"""montar_sandbox.py (R3.4, 19/10/2026) -- R3.4: o sandbox da R3.3 reconstruido a partir de COPIAS DE BYTES (a producao esta em B3/v392 e o Nos em v393; o Nos v391 real e o manifesto B2 da
R3.3 nao existem mais nos caminhos reais): nos/ = o Nos v391 da custodia (the_boundary_BACKUPS/um_v391_*), b2/ = o manifesto B2 (o .bak_B3 da producao) re-apontado para nos/, ambos conferidos
contra o SANDBOX_MANIFEST da R3.2 (mesmos sha256); b1/ = a producao ATUAL (codigo e fontes) com o manifesto re-pinado para o Nos REAL v393 (JA_SINCRONIZADA em v393); nos_v392/ sintetico e fx/
como na R3.3. R3.2: o recibo do kernel sintetico no contrato KERNEL_RECIBO_R3_2 (+ varredura_tokens recursiva,
plano 12-ter item 3; a arvore sintetica ganha TGLExt/O16/SinteticoO16.lean, fora do manifesto, so para a recontagem recursiva); o build log
sintetico traz as linhas de job do lake de cada pedra, da raiz e do Audit e a linha final (R31-4); fx/custodia_v391/ guarda o selo v391 e o
manifesto do kernel v391 (copias do nos/ antes do "selo" do sandbox: o --selo-anterior e o --kernel-manifesto-anterior da R31-3).
R3.1: o recibo do kernel sintetico no contrato KERNEL_RECIBO_R3_1 (toolchain em lista,
pedras com declaracoes, formal_files_antes, criterios so com o medido); fx/CRITERIOS_v392_SINTETICO.json (contrato CRITERIOS_R3_1,
os ESPERADOS pinaveis por --criterios-sha256); a AMOSTRA REAL do aviso de sorry do Lean 4.31 (crases), lida de um log do
Nos/bancada_corpus (so leitura) e guardada em hex no SANDBOX_MANIFEST_R3_1.json. O resto como na R3:
monta o sandbox do vinculo em RAIZ CURTA (limite de caminho do Windows, T16), SO dentro de <raiz>,
e <raiz> tem de ser C:/t/vb* (N8: a mesma regra de --saida do esboco R3).
  b1/        COPIA byte a byte da Bancada Um instalada (B2): codigo + fontes relativas conferidos contra canonical_contracts.json, mais o
             proprio manifesto (que pina o Nos REAL). Serve ao ensaio pre_selo com o Nos real v391 e aos controles negativos.
  nos/       COPIA do Nos v391 real (um.py, um_absoluto_selo.json, um_absoluto.json e -- R3, N1 -- tgl_kernel_proof_manifest.json),
             conferida contra o selo.
  b2/        a mesma copia da Bancada, com o manifesto RE-APONTADO para nos/ (so script.path e seal.path mudam; bytes e sha256 iguais).
  nos_v392/  o Nos SINTETICO v392: o um.py v391 com UM_VERSION trocada para "v392" (mesmo comprimento), core copiado e -- R3 -- um
             manifesto do kernel SINTETICO (o v391 com a raiz e o Audit trocados pelos da arvore sintetica e duas pedras sinteticas a
             mais), pinado pelo selo sintetico. O "selo" do sandbox e: copiar nos_v392/* por cima de nos/.
  fx/        fixtures: a arvore sintetica do kernel (fx/kernel_src), os logs sinteticos do build e do Audit, o recibo do kernel
             sintetico VALIDO no contrato KERNEL_RECIBO_R3 (os invalidos sao derivados dele nos controles), o livro de eventos de
             ensaio (copia do real + elos encadeados, inclusive os de N6/N11 e o do decoy de producao).
A producao e o Nos sao SO lidos. Nada e um selo do rito; nenhum kernel e construido; nenhum dado observado.
uso: montar_sandbox.py <raiz curta, ex. C:/t/vb3> [versao sintetica=v392]"""
import sys
sys.dont_write_bytecode = True
import hashlib, json, re, datetime
from pathlib import Path
PROD = Path("C:/IALD/Bancada_Um")
CUSTODIA_V391 = Path("C:/IALD/Artigo/the_boundary_BACKUPS/um_v391_8e7b9927ceae64b8")
B2_BACKUP = PROD / "canonical_contracts.json.bak_B3_20261013_184916"
SBM_R32 = Path(__file__).resolve().parent.parent / "R3_2" / "evidencias_sandbox" / "SANDBOX_MANIFEST_R3_2.json"
NOS = Path("C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/N\u00f3s")
EVENTOS = Path("C:/IALD/PROGRAMA_IALD/eventos.jsonl")
RAIZ = Path(sys.argv[1]).resolve()
VERSAO_SINTETICA = sys.argv[2] if len(sys.argv) > 2 else "v392"
_rel = Path("C:/t").resolve()
assert RAIZ.parent == _rel and re.match(r"^vb[0-9A-Za-z_-]*$", RAIZ.name), "raiz curta obrigatoria: C:/t/vb* (N8)"
assert not str(RAIZ).lower().startswith(str(PROD).lower()) and not str(RAIZ).lower().startswith(str(NOS).lower())
KERNEL_CONTRATO = "KERNEL_RECIBO_R3_2"
CRITERIOS_CONTRATO = "CRITERIOS_R3_1"
# A1 (R3.1): a amostra REAL do aviso de sorry do Lean 4.31 -- um log do Nos/bancada_corpus (so leitura), a primeira linha com o aviso
AMOSTRA_SORRY = NOS / "bancada_corpus" / "ChainSiteOperators.20260905_150729.falha_lean.log"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def impressao_formal(ff):
    return sha(json.dumps(ff, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def gravar_novo(dst, raw):
    dst = Path(dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if dst.read_bytes() != raw:
            raise SystemExit("DUPLICATA COM BYTES DIFERENTES: " + str(dst))
        return dict(path=str(dst), sha256=sha(raw), bytes=len(raw), duplicata_de_pino=True)
    with open(dst, "xb") as f:
        f.write(raw)
    assert dst.read_bytes() == raw, dst
    return dict(path=str(dst), sha256=sha(raw), bytes=len(raw))


rec = dict(quando=datetime.datetime.now().isoformat(timespec="seconds"), revisao="R3.4 (19/10/2026)", raiz=str(RAIZ), b1=[], b2=[], nos={}, nos_v392={}, fx={})
for sub in ("b1", "b2", "nos", "nos_v392", "fx"):
    if (RAIZ / sub).exists():
        raise SystemExit("sandbox ja montado: apague antes (so dentro de %s)" % RAIZ)
SBM0 = json.loads(SBM_R32.read_bytes())      # o sandbox da R3.2/R3.3: o que a reconstrucao tem de reproduzir
man_raw = B2_BACKUP.read_bytes()             # o manifesto B2 (o backup que a B3 gravou)
assert sha(man_raw) == SBM0["manifesto_producao_sha256"], "o backup B2 da producao nao e o manifesto B2 da R3.2"
man = json.loads(man_raw)
assert Path(man["canonical"]["script"]["path"]) == NOS / "um.py" and Path(man["canonical"]["seal"]["path"]) == NOS / "um_absoluto_selo.json", man["canonical"]
man_prod_raw = (PROD / "canonical_contracts.json").read_bytes()      # o manifesto ATUAL da producao (B3): so lido; deriva o b1
man_prod = json.loads(man_prod_raw)
# nos/ = copia do Nos v391 real, conferida contra o selo (R3: com o manifesto do kernel que o selo pina)
um = (CUSTODIA_V391 / "um.py").read_bytes()
selo_raw = (CUSTODIA_V391 / "um_absoluto_selo.json").read_bytes()
selo = json.loads(selo_raw)
core = (CUSTODIA_V391 / "um_absoluto.json").read_bytes()
kman_raw = (CUSTODIA_V391 / "Lean" / "tgl_kernel_proof_manifest.json").read_bytes()
for k_, b_ in (("um_py", um), ("selo", selo_raw), ("core", core), ("kernel_manifest", kman_raw)):
    assert sha(b_) == SBM0["nos"][k_]["sha256"] and len(b_) == SBM0["nos"][k_]["bytes"], "o Nos v391 da custodia (%s) nao e o da R3.2" % k_
assert selo["sha256"]["um.py"] == sha(um) and selo["sha256"]["um_absoluto.json"] == sha(core) and selo["um_version"] == "v391"
assert selo["sha256"]["tgl_kernel_proof_manifest.json"] == sha(kman_raw), "o selo v391 nao pina o manifesto do kernel em disco"
assert man["canonical"]["script"]["sha256"] == sha(um) and man["canonical"]["seal"]["sha256"] == sha(selo_raw)
rec["nos"] = dict(um_py=gravar_novo(RAIZ / "nos" / "um.py", um), selo=gravar_novo(RAIZ / "nos" / "um_absoluto_selo.json", selo_raw),
                  core=gravar_novo(RAIZ / "nos" / "um_absoluto.json", core), kernel_manifest=gravar_novo(RAIZ / "nos" / "tgl_kernel_proof_manifest.json", kman_raw))
# R3.2 (R31-3): a "custodia" da v391 no sandbox: o selo e o manifesto do kernel v391, que o --selo-anterior e o --kernel-manifesto-anterior
# apontam depois do "selo" do sandbox (quando nos/ ja e o v392); na producao, as copias da custodia (the_boundary_BACKUPS/um_v391_*)
rec["fx"]["custodia_v391"] = dict(selo=gravar_novo(RAIZ / "fx" / "custodia_v391" / "um_absoluto_selo.json", selo_raw),
                                  kernel_manifest=gravar_novo(RAIZ / "fx" / "custodia_v391" / "tgl_kernel_proof_manifest.json", kman_raw))
# b1/ (manifesto original) e b2/ (manifesto re-apontado para nos/)
man2 = json.loads(man_raw)
man2["canonical"]["script"]["path"] = str(RAIZ / "nos" / "um.py")
man2["canonical"]["seal"]["path"] = str(RAIZ / "nos" / "um_absoluto_selo.json")
man2["sandbox_R3"] = "copia de ensaio (13/10/2026): so script.path e seal.path re-apontados para %s; bytes e sha256 identicos ao manifesto B2 %s" % (RAIZ / "nos", sha(man_raw)[:16])
man2_raw = json.dumps(man2, ensure_ascii=False, indent=1).encode("utf-8")
# b1: a copia que pina o Nos REAL. Na R3.3 era a producao B2 com o Nos v391; agora e a producao ATUAL (B3, codigo e fontes lidos e conferidos) com o manifesto re-pinado para o Nos
# REAL v393 (so canonical.version/script/seal mudam; deployment_id marcado). Serve ao ensaio pre_selo contra o Nos real e aos controles das guardas.
nos_real = {n_: (NOS / n_).read_bytes() for n_ in ("um.py", "um_absoluto_selo.json", "um_absoluto.json", "tgl_kernel_proof_manifest.json")}
selo_real = json.loads(nos_real["um_absoluto_selo.json"])
assert selo_real["sha256"]["um.py"] == sha(nos_real["um.py"]) and selo_real["sha256"]["tgl_kernel_proof_manifest.json"] == sha(nos_real["tgl_kernel_proof_manifest.json"]), "o selo real nao pina o Nos real"
man1 = json.loads(man_prod_raw)
man1["canonical"] = dict(version=selo_real["um_version"],
                         script=dict(path=str(NOS / "um.py"), bytes=len(nos_real["um.py"]), sha256=sha(nos_real["um.py"])),
                         seal=dict(path=str(NOS / "um_absoluto_selo.json"), bytes=len(nos_real["um_absoluto_selo.json"]), sha256=sha(nos_real["um_absoluto_selo.json"])))
man1["deployment_id"] = "B3-SANDBOX-b1-" + selo_real["um_version"] + "-R1"
man1["sandbox_R3_4"] = ("copia de ensaio (19/10/2026): a producao B3 (%s) com canonical re-pinado para o Nos REAL %s; codigo e fontes iguais aos da producao" % (sha(man_prod_raw)[:16], selo_real["um_version"]))
man1_raw = json.dumps(man1, ensure_ascii=False, indent=1).encode("utf-8")
rec["nos_real"] = dict(versao=selo_real["um_version"], um_py=dict(sha256=sha(nos_real["um.py"]), bytes=len(nos_real["um.py"])), selo=dict(sha256=sha(nos_real["um_absoluto_selo.json"]), bytes=len(nos_real["um_absoluto_selo.json"])),
                       core=dict(sha256=sha(nos_real["um_absoluto.json"]), bytes=len(nos_real["um_absoluto.json"])),
                       kernel_manifest=dict(sha256=sha(nos_real["tgl_kernel_proof_manifest.json"]), bytes=len(nos_real["tgl_kernel_proof_manifest.json"])),
                       kernel=dict(raiz_sha256=json.loads(nos_real["tgl_kernel_proof_manifest.json"])["formal_files_sha256"]["TGLExt.lean"]))
rec["b1"].append(gravar_novo(RAIZ / "b1" / "canonical_contracts.json", man1_raw))
rec["b2"].append(gravar_novo(RAIZ / "b2" / "canonical_contracts.json", man2_raw))
for e in man_prod["code"] + [s for s in man_prod["sources"] if not Path(s["path"]).is_absolute()]:
    assert ".." not in Path(e["path"]).parts and not Path(e["path"]).is_absolute(), e["path"]
    raw = (PROD / e["path"]).read_bytes()
    if sha(raw) != e["sha256"] or len(raw) != e["bytes"]:
        raise SystemExit("PIN MISMATCH na producao: " + e["path"])
    rec["b1"].append(gravar_novo(RAIZ / "b1" / e["path"], raw))
for e in man["code"] + [s for s in man["sources"] if not Path(s["path"]).is_absolute()]:
    assert ".." not in Path(e["path"]).parts and not Path(e["path"]).is_absolute(), e["path"]
    raw = (PROD / e["path"]).read_bytes()
    if sha(raw) != e["sha256"] or len(raw) != e["bytes"]:
        raise SystemExit("PIN MISMATCH (manifesto B2) na producao: " + e["path"])
    rec["b2"].append(gravar_novo(RAIZ / "b2" / e["path"], raw))
(RAIZ / "b1" / "estado").mkdir()
(RAIZ / "b2" / "estado").mkdir()

# fx/kernel_src = a arvore SINTETICA do kernel (N1): raiz, Audit e duas pedras; nenhum Lean roda aqui
KS = RAIZ / "fx" / "kernel_src"
arvore = {
    "TGLExt.lean": "-- SINTETICO (sandbox R3 do vinculo, 13/10/2026): raiz do kernel; nenhum kernel e construido aqui\nimport TGLExt.PedraSinteticaA\nimport TGLExt.PedraSinteticaB\n",
    "TGL/Audit.lean": "-- SINTETICO (sandbox R3): o Audit\n#print axioms TGLExt.PedraSinteticaA.um\n#print axioms TGLExt.PedraSinteticaB.dois\n",
    "TGLExt/PedraSinteticaA.lean": "-- SINTETICO (sandbox R3): pedra A\nnamespace TGLExt.PedraSinteticaA\ntheorem um : 1 = 1 := rfl\nend TGLExt.PedraSinteticaA\n",
    "TGLExt/PedraSinteticaB.lean": "-- SINTETICO (sandbox R3): pedra B\nnamespace TGLExt.PedraSinteticaB\ntheorem dois : 2 = 2 := rfl\nend TGLExt.PedraSinteticaB\n",
}
# R3.2 (plano 12-ter item 3): um .lean numa SUBPASTA (TGLExt/O16), fora do manifesto e fora das pedras: so existe para que a recontagem
# RECURSIVA dos .lean da arvore (5; 1 em TGLExt/O16) difira da nao recursiva
ARVORE_EXTRA = {"TGLExt/O16/SinteticoO16.lean": "-- SINTETICO (sandbox R3.2): um .lean em TGLExt/O16, fora do manifesto; so para a varredura recursiva\n"}
ks_sha = {}
for rel, txt in arvore.items():
    b = txt.encode("utf-8")
    gravar_novo(KS / rel, b)
    ks_sha[rel] = sha(b)
for rel, txt in ARVORE_EXTRA.items():
    gravar_novo(KS / rel, txt.encode("utf-8"))
N_LEAN = sum(1 for q in KS.rglob("*.lean"))
N_LEAN_O16 = sum(1 for q in (KS / "TGLExt" / "O16").rglob("*.lean"))
rec["fx"]["kernel_src"] = dict(dir=str(KS), sha256=ks_sha, extra_fora_do_manifesto=sorted(ARVORE_EXTRA), arquivos_lean=N_LEAN, arquivos_lean_em_TGLExt_O16=N_LEAN_O16)
# o manifesto do kernel SINTETICO v392: o v391 com a raiz e o Audit trocados e as duas pedras a mais (+ entradas no axiom_report)
kman = json.loads(kman_raw)
ff_v391 = dict(kman["formal_files_sha256"])
kman["formal_files_sha256"] = dict(ff_v391)
for rel, h in ks_sha.items():
    kman["formal_files_sha256"][rel] = h
kman["axiom_report"] = dict(kman["axiom_report"])
kman["axiom_report"]["TGLExt.PedraSinteticaA.um"] = ["propext", "Classical.choice", "Quot.sound"]
kman["axiom_report"]["TGLExt.PedraSinteticaB.dois"] = []
kman["SINTETICO_SANDBOX"] = ("NAO E O MANIFESTO DO RITO: fixture do ensaio do vinculo (R3, 13/10/2026); deriva do manifesto v391 real (%s) trocando "
                             "TGLExt.lean e TGL/Audit.lean pelos da arvore sintetica e acrescentando duas pedras sinteticas" % sha(kman_raw)[:16])
kman_sin = json.dumps(kman, ensure_ascii=False, indent=1).encode("utf-8")
# nos_v392/ = o Nos sintetico
txt = um.decode("utf-8-sig")
mv = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', txt, re.M)
assert mv and mv.group(1) == "v391", mv
velha = mv.group(0).encode("utf-8")
nova = velha.replace(b"v391", VERSAO_SINTETICA.encode("utf-8"), 1)
assert um.count(velha) == 1
um_sin = um.replace(velha, nova, 1)
assert len(um_sin) == len(um) and um_sin != um
t2 = um_sin.decode("utf-8-sig")
assert re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', t2, re.M).group(1) == VERSAO_SINTETICA
assert len(re.findall(r"^ALPHA_FINE_CODATA_2018[ \t]*=", t2, re.M)) == len(re.findall(r"^ALPHA_FINE_CODATA_2018[ \t]*=", txt, re.M)) == 1
assert len(re.findall(r"^UM_VERSION[ \t]*=", t2, re.M)) == 1
selo_sin = dict(selo)
selo_sin["um_version"] = VERSAO_SINTETICA
selo_sin["sha256"] = dict(selo["sha256"])
selo_sin["sha256"]["um.py"] = sha(um_sin)
selo_sin["sha256"]["tgl_kernel_proof_manifest.json"] = sha(kman_sin)
selo_sin["SINTETICO_SANDBOX"] = ("NAO E UM SELO DO RITO: fixture do ensaio do vinculo Bancada-um.py (R3, 13/10/2026); deriva do selo v391 real "
                                 "trocando so um_version, sha256[um.py] e sha256[tgl_kernel_proof_manifest.json]; vive so em %s" % RAIZ)
selo_sin["SINTETICO_SANDBOX_derivado_do_selo_v391_sha256"] = sha(selo_raw)
selo_b = json.dumps(selo_sin, ensure_ascii=False, indent=1).encode("utf-8")
rec["nos_v392"] = dict(um_py=gravar_novo(RAIZ / "nos_v392" / "um.py", um_sin), selo=gravar_novo(RAIZ / "nos_v392" / "um_absoluto_selo.json", selo_b),
                       core=gravar_novo(RAIZ / "nos_v392" / "um_absoluto.json", core),
                       kernel_manifest=gravar_novo(RAIZ / "nos_v392" / "tgl_kernel_proof_manifest.json", kman_sin), versao=VERSAO_SINTETICA,
                       um_py_real=dict(sha256=sha(um), bytes=len(um)), bytes_trocados=len(velha), linha_trocada=txt[:mv.start()].count("\n") + 1)
gravar_novo(RAIZ / "nos_v392" / "LEIA-ME_SINTETICO.txt", ("Fixture sintetica (R3, 13/10/2026): um.py v391 real com UM_VERSION trocada para %s na linha %d; selo e "
                                                         "manifesto do kernel derivados; core copiado. NAO e versao selada. So para ensaiar o re-pino da Bancada no sandbox.\n"
                                                         % (VERSAO_SINTETICA, rec["nos_v392"]["linha_trocada"])).encode("utf-8"))
# fx/kernel_logs = os logs sinteticos do build e do Audit (sem sorry, sem erro, axiomas no trio)
KL = RAIZ / "fx" / "kernel_logs"
log_b = ("build_full.log SINTETICO (fixture R3.2 13/10/2026): nenhum kernel foi construido aqui; as linhas imitam o formato do lake 4.31\n"
         "\u2714 [1/4] Built TGLExt.PedraSinteticaA (1s)\n"
         "\u2714 [2/4] Built TGLExt.PedraSinteticaB (1s)\n"
         "\u2714 [3/4] Built TGLExt (1s)\n"
         "\u2714 [4/4] Built TGL.Audit (1s)\n"
         "Build completed successfully (4 jobs).\n").encode("utf-8")
log_a = ("audit.log SINTETICO (fixture R3 13/10/2026)\n"
         "'TGLExt.PedraSinteticaA.um' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
         "'TGLExt.PedraSinteticaB.dois' does not depend on any axioms\n").encode("utf-8")
rec["fx"]["log_build"] = gravar_novo(KL / "build_full_SINTETICO.log", log_b)
rec["fx"]["log_audit"] = gravar_novo(KL / "audit_SINTETICO.log", log_a)
# o recibo do kernel sintetico VALIDO, contrato KERNEL_RECIBO_R3 (sem um_py_sha256: a etapa 2 roda antes do candidato)
k_ok = dict(contrato=KERNEL_CONTRATO, versao=VERSAO_SINTETICA, quando_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            rc=0, sorry=0, erros=0,
            build_full_log=dict(path=str(KL / "build_full_SINTETICO.log"), sha256=sha(log_b)),
            audit_log=dict(path=str(KL / "audit_SINTETICO.log"), sha256=sha(log_a)),
            toolchain=dict(lean_version=list(kman["lean_version"]), lake_version=list(kman["lake_version"])),   # N1m: lista, como no manifesto
            arvore=str(KS),
            raiz=dict(path="TGLExt.lean", sha256_antes=ff_v391["TGLExt.lean"], sha256_depois=ks_sha["TGLExt.lean"]),
            audit=dict(path="TGL/Audit.lean", sha256_antes=ff_v391["TGL/Audit.lean"], sha256_depois=ks_sha["TGL/Audit.lean"]),
            pedras=[dict(path="TGLExt/PedraSinteticaA.lean", sha256=ks_sha["TGLExt/PedraSinteticaA.lean"], declaracoes=["TGLExt.PedraSinteticaA.um"]),
                    dict(path="TGLExt/PedraSinteticaB.lean", sha256=ks_sha["TGLExt/PedraSinteticaB.lean"], declaracoes=["TGLExt.PedraSinteticaB.dois"])],
            axiomas=["propext", "Classical.choice", "Quot.sound"],
            criterios=dict(j1_declaracoes=dict(medido=2), j1_teoremas=dict(medido=2), j1_fora_do_trio=dict(medido=0),
                           audit_entradas_antigas_identicas=dict(medido=0), tokens_proibidos=dict(medido=0),
                           r1_ausente=dict(medido=True), declaracoes_novas_no_trio=dict(medido=True)),   # A3: so o MEDIDO; o esperado vem do CRITERIOS pinado
            varredura_tokens=dict(recursiva=True, arquivos_lean=N_LEAN, arquivos_lean_em_TGLExt_O16=N_LEAN_O16,
                                  nota="plano 12-ter item 3: a varredura de tokens proibidos e recursiva (inclui TGLExt/O16); o B(n) reconta"),
            formal_files_antes=dict(ff_v391),   # N1l: o mapa do kernel ANTES (a impressao dele == nos_kernel_impressao.antes)
            nos_kernel_impressao=dict(definicao="sha256 do JSON canonico (chaves ordenadas, sem espacos, UTF-8) de formal_files_sha256 do Nos",
                                      antes=impressao_formal(ff_v391), depois=impressao_formal(ff_v391)),
            nota="FIXTURE SINTETICA do recibo do build do kernel (etapa 2 da cadeia), contrato KERNEL_RECIBO_R3_2: nenhum kernel construido aqui; "
                 "os criterios J1/8523 do plano v392 viram 2/2/0/0 nesta arvore de duas pedras (medidos aqui; os esperados no CRITERIOS sintetico)")
rec["fx"]["KERNEL_RECIBO_v392_SINTETICO_VALIDO.json"] = gravar_novo(RAIZ / "fx" / "KERNEL_RECIBO_v392_SINTETICO_VALIDO.json",
                                                                   json.dumps(k_ok, ensure_ascii=False, indent=1).encode("utf-8"))
# A3 (R3.1): o CRITERIOS sintetico (os ESPERADOS), pinavel pela flag --criterios-sha256; o modelo da gerencia e R3_1/CRITERIOS_V392.json
crit = dict(contrato=CRITERIOS_CONTRATO, versao=VERSAO_SINTETICA, preenchido=True, x19="nao",
            esperados=dict(j1_declaracoes=2, j1_teoremas=2, j1_fora_do_trio=0, audit_entradas_antigas_identicas=0, tokens_proibidos=0,
                           r1_ausente=True, declaracoes_novas_no_trio=True),
            SINTETICO_SANDBOX="NAO SAO OS CRITERIOS DA v392: fixture do ensaio (R3.1, 13/10/2026) para a arvore sintetica de duas pedras; x19='nao' so preenche o campo")
rec["fx"]["CRITERIOS_v392_SINTETICO.json"] = gravar_novo(RAIZ / "fx" / "CRITERIOS_v392_SINTETICO.json", json.dumps(crit, ensure_ascii=False, indent=1).encode("utf-8"))
# A1 (R3.1): a amostra REAL do aviso de sorry (so leitura do Nos/bancada_corpus)
_am = AMOSTRA_SORRY.read_bytes()
_linhas = _am.split(b"\n")
_n = next(i for i, l in enumerate(_linhas, 1) if b"declaration uses" in l)
rec["fx"]["amostra_sorry_lean431"] = dict(path=str(AMOSTRA_SORRY), sha256=sha(_am), bytes=len(_am), linha_n=_n, linha_hex=_linhas[_n - 1].hex(),
                                          n_avisos_crase_no_arquivo=_am.count(b"declaration uses `sorry`"), n_avisos_aspas_no_arquivo=_am.count(b"declaration uses 'sorry'"),
                                          nota="a linha verbatim (com o CR do CRLF) que os controles A1 acrescentam ao log sintetico")
rec["fx"]["kernel_v391"] = dict(raiz_sha256=ff_v391["TGLExt.lean"], audit_sha256=ff_v391["TGL/Audit.lean"], impressao_formal=impressao_formal(ff_v391),
                                manifesto_sha256=sha(kman_raw))
# ================================================================ R3.4: a camada sintetica v393 e a cadeia de selos de ensaio
# nos_v393s/ = o Nos sintetico SEGUINTE ao v392 sintetico: UM_VERSION v393 (mesmo comprimento), a arvore do kernel ganha a pedra C (um teorema) e um MODULO DE AUDITORIA
# (so import + run_cmd, sem declaracoes); o recibo do kernel sintetico (contrato KERNEL_RECIBO_R3_4) lista o modulo em modulos_de_auditoria.
V3 = "v393"
KS3 = RAIZ / "fx" / "kernel_src_v393s"
arv3 = dict(arvore)
arv3["TGLExt/PedraSinteticaC.lean"] = "-- SINTETICO (sandbox R3.4): pedra C\nnamespace TGLExt.PedraSinteticaC\ntheorem tres : 3 = 3 := rfl\nend TGLExt.PedraSinteticaC\n"
AUDITORIA_C = """-- SINTETICO (sandbox R3.4): modulo de auditoria: so import, open e run_cmd; nenhuma declaracao
import TGLExt.PedraSinteticaC
import Lean

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let mut n := 0
  for (c, _) in env.constants.toList do
    if let some i := env.getModuleIdxFor? c then
      let m := env.header.moduleNames[i]!
      if (`TGLExt.PedraSinteticaC).isPrefixOf m then
        n := n + 1
  if n == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("AUDIT_COUNT " ++ toString n)
"""
arv3["TGLExt/AuditoriaSinteticaC.lean"] = AUDITORIA_C
arv3["TGLExt.lean"] = arvore["TGLExt.lean"] + "import TGLExt.PedraSinteticaC\nimport TGLExt.AuditoriaSinteticaC\n"
arv3["TGL/Audit.lean"] = arvore["TGL/Audit.lean"] + "#print axioms TGLExt.PedraSinteticaC.tres\n"
ks3_sha = {}
for rel, txt in arv3.items():
    b = txt.encode("utf-8")
    gravar_novo(KS3 / rel, b)
    ks3_sha[rel] = sha(b)
for rel, txt in ARVORE_EXTRA.items():
    gravar_novo(KS3 / rel, txt.encode("utf-8"))
N_LEAN3 = sum(1 for q in KS3.rglob("*.lean"))
N_LEAN3_O16 = sum(1 for q in (KS3 / "TGLExt" / "O16").rglob("*.lean"))
rec["fx"]["kernel_src_v393s"] = dict(dir=str(KS3), sha256=ks3_sha, arquivos_lean=N_LEAN3, arquivos_lean_em_TGLExt_O16=N_LEAN3_O16)
ff_v392s = dict(kman["formal_files_sha256"])
kman3 = json.loads(json.dumps(kman))
for rel, h in ks3_sha.items():
    kman3["formal_files_sha256"][rel] = h
kman3["axiom_report"]["TGLExt.PedraSinteticaC.tres"] = []
kman3["SINTETICO_SANDBOX"] = "NAO E O MANIFESTO DO RITO: fixture do ensaio do vinculo (R3.4, 19/10/2026); deriva do manifesto sintetico v392 acrescentando a pedra C e o modulo de auditoria C"
kman3_b = json.dumps(kman3, ensure_ascii=False, indent=1).encode("utf-8")
txt3 = um_sin.decode("utf-8-sig")
mv3 = re.search(r'^UM_VERSION\s*=\s*["\x27]([^"\x27]+)', txt3, re.M)
assert mv3 and mv3.group(1) == VERSAO_SINTETICA, mv3
velha3 = mv3.group(0).encode("utf-8")
nova3 = velha3.replace(VERSAO_SINTETICA.encode("utf-8"), V3.encode("utf-8"), 1)
assert um_sin.count(velha3) == 1
um3 = um_sin.replace(velha3, nova3, 1)
assert len(um3) == len(um_sin) and um3 != um_sin
selo3 = dict(selo_sin)
selo3["um_version"] = V3
selo3["sha256"] = dict(selo_sin["sha256"])
selo3["sha256"]["um.py"] = sha(um3)
selo3["sha256"]["tgl_kernel_proof_manifest.json"] = sha(kman3_b)
selo3["SINTETICO_SANDBOX"] = "NAO E UM SELO DO RITO: fixture do ensaio do vinculo (R3.4, 19/10/2026); deriva do selo sintetico v392 trocando um_version, sha256[um.py] e sha256[tgl_kernel_proof_manifest.json]; vive so em %s" % RAIZ
selo3_b = json.dumps(selo3, ensure_ascii=False, indent=1).encode("utf-8")
rec["nos_v393s"] = dict(um_py=gravar_novo(RAIZ / "nos_v393s" / "um.py", um3), selo=gravar_novo(RAIZ / "nos_v393s" / "um_absoluto_selo.json", selo3_b),
                        core=gravar_novo(RAIZ / "nos_v393s" / "um_absoluto.json", core), kernel_manifest=gravar_novo(RAIZ / "nos_v393s" / "tgl_kernel_proof_manifest.json", kman3_b), versao=V3)
gravar_novo(RAIZ / "nos_v393s" / "LEIA-ME_SINTETICO.txt", ("Fixture sintetica (R3.4, 19/10/2026): o Nos sintetico v392 com UM_VERSION trocada para %s; selo e manifesto do kernel derivados; core copiado. "
                                                          "NAO e versao selada. So para ensaiar o salto da Bancada no sandbox.\n" % V3).encode("utf-8"))
log_b3 = ("build_full.log SINTETICO (fixture R3.4 19/10/2026): nenhum kernel foi construido aqui; as linhas imitam o formato do lake 4.31\n"
          "✔ [1/6] Built TGLExt.PedraSinteticaA (1s)\n"
          "✔ [2/6] Built TGLExt.PedraSinteticaB (1s)\n"
          "✔ [3/6] Built TGLExt.PedraSinteticaC (1s)\n"
          "✔ [4/6] Built TGLExt.AuditoriaSinteticaC (1s)\n"
          "✔ [5/6] Built TGLExt (1s)\n"
          "✔ [6/6] Built TGL.Audit (1s)\n"
          "Build completed successfully (6 jobs).\n").encode("utf-8")
log_a3 = ("audit.log SINTETICO (fixture R3.4 19/10/2026)\n"
          "'TGLExt.PedraSinteticaA.um' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
          "'TGLExt.PedraSinteticaB.dois' does not depend on any axioms\n"
          "'TGLExt.PedraSinteticaC.tres' does not depend on any axioms\n").encode("utf-8")
rec["fx"]["log_build_v393s"] = gravar_novo(KL / "build_full_SINTETICO_v393s.log", log_b3)
rec["fx"]["log_audit_v393s"] = gravar_novo(KL / "audit_SINTETICO_v393s.log", log_a3)
k3 = dict(contrato="KERNEL_RECIBO_R3_4", versao=V3, quando_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(), rc=0, sorry=0, erros=0,
          build_full_log=dict(path=str(KL / "build_full_SINTETICO_v393s.log"), sha256=sha(log_b3)),
          audit_log=dict(path=str(KL / "audit_SINTETICO_v393s.log"), sha256=sha(log_a3)),
          toolchain=dict(lean_version=list(kman["lean_version"]), lake_version=list(kman["lake_version"])),
          arvore=str(KS3),
          raiz=dict(path="TGLExt.lean", sha256_antes=ks_sha["TGLExt.lean"], sha256_depois=ks3_sha["TGLExt.lean"]),
          audit=dict(path="TGL/Audit.lean", sha256_antes=ks_sha["TGL/Audit.lean"], sha256_depois=ks3_sha["TGL/Audit.lean"]),
          pedras=[dict(path="TGLExt/AuditoriaSinteticaC.lean", sha256=ks3_sha["TGLExt/AuditoriaSinteticaC.lean"]),
                  dict(path="TGLExt/PedraSinteticaC.lean", sha256=ks3_sha["TGLExt/PedraSinteticaC.lean"], declaracoes=["TGLExt.PedraSinteticaC.tres"])],
          modulos_de_auditoria=["TGLExt/AuditoriaSinteticaC.lean"],
          axiomas=["propext", "Classical.choice", "Quot.sound"],
          criterios=dict(j1_declaracoes=dict(medido=1), j1_teoremas=dict(medido=1), j1_fora_do_trio=dict(medido=0), audit_entradas_antigas_identicas=dict(medido=0),
                         tokens_proibidos=dict(medido=0), r1_ausente=dict(medido=True), declaracoes_novas_no_trio=dict(medido=True)),
          varredura_tokens=dict(recursiva=True, arquivos_lean=N_LEAN3, arquivos_lean_em_TGLExt_O16=N_LEAN3_O16),
          formal_files_antes=dict(ff_v392s),
          nos_kernel_impressao=dict(definicao="sha256 do JSON canonico (chaves ordenadas, sem espacos, UTF-8) de formal_files_sha256 do Nos", antes=impressao_formal(ff_v392s), depois=impressao_formal(ff_v392s)),
          nota="FIXTURE SINTETICA do recibo do build do kernel da camada v393 sintetica, contrato KERNEL_RECIBO_R3_4: uma pedra com declaracao (C) e um modulo de auditoria sem declaracoes (listado)")
rec["fx"]["KERNEL_RECIBO_v393s_SINTETICO_VALIDO.json"] = gravar_novo(RAIZ / "fx" / "KERNEL_RECIBO_v393s_SINTETICO_VALIDO.json", json.dumps(k3, ensure_ascii=False, indent=1).encode("utf-8"))
crit3 = dict(contrato=CRITERIOS_CONTRATO, versao=V3, preenchido=True, x19="nao",
             esperados=dict(j1_declaracoes=1, j1_teoremas=1, j1_fora_do_trio=0, audit_entradas_antigas_identicas=0, tokens_proibidos=0, r1_ausente=True, declaracoes_novas_no_trio=True),
             SINTETICO_SANDBOX="NAO SAO OS CRITERIOS DA v393: fixture do ensaio (R3.4) para a camada sintetica v393")
rec["fx"]["CRITERIOS_v393_SINTETICO.json"] = gravar_novo(RAIZ / "fx" / "CRITERIOS_v393_SINTETICO.json", json.dumps(crit3, ensure_ascii=False, indent=1).encode("utf-8"))
# a pasta cadeia_de_selo de ENSAIO: <cadeia>/v(J+1)/base_vJ/ (copias de bytes de J), <cadeia>/v(J+1)/APLICADO_AO_CANONICO_<ts>.json (o registro do instalador que trocou J por J+1; o
# diretorio v392 tem tambem uma TENTATIVA REVERTIDA, que o gerador tem de ignorar) e _nos/ (os backups de bytes .bak_<ts>, que na vida real ficam no proprio Nos)
CS = RAIZ / "fx" / "cadeia_de_selo"
camadas = {"v391": (um, selo_raw, core, kman_raw), "v392": (um_sin, selo_b, core, kman_sin), "v393": (um3, selo3_b, core, kman3_b)}
rec["fx"]["cadeia_de_selo"] = dict(dir=str(CS), camadas={})
for v, (u_, s_, c_, k_) in camadas.items():
    proxima = "v%d" % (int(v[1:]) + 1)
    d_ = CS / proxima / ("base_" + v)
    rec["fx"]["cadeia_de_selo"]["camadas"][v] = dict(um_py=gravar_novo(d_ / "um.py", u_), selo=gravar_novo(d_ / "um_absoluto_selo.json", s_), core=gravar_novo(d_ / "um_absoluto.json", c_),
                                                     kernel_manifesto=gravar_novo(d_ / "tgl_kernel_proof_manifest.json", k_))
for (v_ant, v_novo, ts) in (("v391", "v392", "20261001_100000"), ("v392", "v393", "20261002_100000")):
    u_, s_, c_, k_ = camadas[v_ant]
    un = camadas[v_novo][0]
    bu = gravar_novo(CS / "_nos" / ("um.py.bak_" + ts), u_)
    bs = gravar_novo(CS / "_nos" / ("um_absoluto_selo.json.bak_" + ts), s_)
    reg = dict(ts=ts, backups={"um.py": dict(backup=bu["path"], bytes=bu["bytes"], sha16=bu["sha256"][:16]),
                               "um_absoluto_selo.json": dict(backup=bs["path"], bytes=bs["bytes"], sha16=bs["sha256"][:16])},
               um_py_novo=dict(bytes=len(un), sha16=sha(un)[:16], origem="SINTETICO (sandbox R3.4)"))
    gravar_novo(CS / v_novo / ("APLICADO_AO_CANONICO_" + ts + ".json"), json.dumps(reg, ensure_ascii=False, indent=1).encode("utf-8"))
reg_rev = dict(ts="20261001_090000", backups={"um.py": dict(backup=str(CS / "_nos" / "um.py.bak_20261001_100000"), bytes=len(um), sha16=sha(um)[:16])},
               um_py_novo=dict(bytes=1, sha16="0" * 16, origem="SINTETICO: tentativa revertida (o gerador a ignora)"))
gravar_novo(CS / "v392" / "APLICADO_AO_CANONICO_20261001_090000.json", json.dumps(reg_rev, ensure_ascii=False, indent=1).encode("utf-8"))

# fx/eventos_sandbox.jsonl = copia do livro real (so lido) + elos ENCADEADOS de ensaio (a mesma regra de iald.py evento()); o real nao e tocado
linhas = [l for l in EVENTOS.read_text(encoding="utf-8").splitlines() if l.strip()]
ult = json.loads(linhas[-1])
seq, ant = ult["seq"], ult["hash"]


def elo(tipo, quem, dados):
    global seq, ant
    e = {"seq": seq + 1, "quando": datetime.datetime.now().astimezone().isoformat(timespec="seconds"), "tipo": tipo, "quem": quem, "dados": dados, "anterior": ant}
    e["hash"] = hashlib.sha256(json.dumps({k: v for k, v in e.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    seq, ant = e["seq"], e["hash"]
    return e


b2 = str(RAIZ / "b2")
pd = str(RAIZ / "pd")
U, S16 = sha(um_sin)[:16], sha(selo_b)[:16]
base = dict(versao=VERSAO_SINTETICA, bancada=b2, acao="sincronizacao", um_py=U, selo=S16)
elos = dict(
    valido=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, gravacoes=["canonical_contracts.json", "CONTRATO_CANONICO_B3.md", "estado/sincronizacao/RECIBO_*.json"],
                                                         unidade="F0.6", nota="ENSAIO R3 em sandbox (copia b2); o quadro real segue intocado")),
    outra_sessao=elo("SINCRONIZACAO_BANCADA", "claude-c2", dict(base)),
    negacao=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="NAO sincronizar a Bancada ate o operador decidir")),
    outro_programa=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, um_py="deadbeefdeadbeef", selo="feedfacefeedface")),
    outra_versao=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, versao="v393")),
    outra_bancada=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, bancada=str(RAIZ / "b1"))),
    tipo_errado=elo("anotar", "claude-c1", dict(base)),
    sem_acao=elo("SINCRONIZACAO_BANCADA", "claude-c1", {k: v for k, v in base.items() if k != "acao"}),
    reparo=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, versao="v391", reparo=True, nota="ENSAIO A8: reparo de pino nomeado (sandbox)")),
    # N11: a negacao escondida por forma (NFD, largura cheia, largura zero) e por CHAVE; e a chave fora do conjunto fechado
    n11_nfd=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="na\u0303o sincronizar agora")),
    n11_largura_cheia=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="\uff2e\uff21\uff2f sincronizar agora")),
    n11_largura_zero=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nota="n\u200bao sincronizar agora")),
    n11_chave_negacao=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, nao_gravar=True)),
    n11_chave_proibido=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, PROIBIDO=True)),
    n11_chave_desconhecida=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, autorizado_por="qualquer")),
    # o elo que nomeia o decoy de producao (C:/t/vb*/pd), usado pelos controles em processo (N1, N2, N3, N4)
    decoy=elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(base, bancada=pd, unidade="F0.6", nota="ENSAIO R3: decoy de producao em copia")),
)
# R3.4: o elo que nomeia o decoy de producao do SALTO (C:/t/vb*/pd_salto) para a v393 sintetica (a composicao exata do B(n) da v394: producao + aplicar + salto + evento + servico)
elos["decoy_salto"] = elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(versao=V3, bancada=str(RAIZ / "pd_salto"), acao="sincronizacao", um_py=sha(um3)[:16], selo=sha(selo3_b)[:16], unidade="F0.6",
                                                                  nota="ENSAIO R3.4: decoy de producao do salto, em copia"))
ok_lines = linhas + [json.dumps(e, ensure_ascii=False) for e in elos.values()]
rec["fx"]["eventos_sandbox"] = gravar_novo(RAIZ / "fx" / "eventos_sandbox.jsonl", ("\n".join(ok_lines) + "\n").encode("utf-8"))
# o mesmo livro com elos FORJADOS (sem cadeia): um c1 completo mas sem encadear; um seq duplicado encadeado
forj_sem_cadeia = dict(elos["valido"], seq=90001, anterior="ff" * 32, hash="00" * 32)
forj_dup = elo("SINCRONIZACAO_BANCADA", "claude-c1", dict(elos["valido"]["dados"], nota="seq duplicado encadeado"))
forj_dup["seq"] = elos["valido"]["seq"]
forj_dup["hash"] = hashlib.sha256(json.dumps({k: v for k, v in forj_dup.items() if k != "hash"}, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
rec["fx"]["eventos_forjado_sem_cadeia"] = gravar_novo(RAIZ / "fx" / "eventos_forjado_sem_cadeia.jsonl", ("\n".join(ok_lines + [json.dumps(forj_sem_cadeia, ensure_ascii=False)]) + "\n").encode("utf-8"))
rec["fx"]["eventos_forjado_seq_duplicado"] = gravar_novo(RAIZ / "fx" / "eventos_forjado_seq_duplicado.jsonl", ("\n".join(ok_lines + [json.dumps(forj_dup, ensure_ascii=False)]) + "\n").encode("utf-8"))
rec["fx"]["elos_de_ensaio"] = {k: dict(seq=e["seq"], hash16=e["hash"][:16]) for k, e in elos.items()}
rec["fx"]["elos_forjados"] = dict(sem_cadeia_seq=forj_sem_cadeia["seq"], duplicado_seq=forj_dup["seq"])
rec["fx"]["eventos_reais_copiados"] = len(linhas)
rec["fx"]["ultimo_seq_real"] = ult["seq"]
rec["n_b1"], rec["n_b2"] = len(rec["b1"]), len(rec["b2"])
rec["manifesto_b2_sha256"] = sha(man2_raw)
rec["manifesto_producao_sha256"] = sha(man_prod_raw)          # o manifesto ATUAL da producao (B3): so lido
rec["manifesto_b2_origem_sha256"] = sha(man_raw)
rec["manifesto_b1_sha256"] = sha(man1_raw)
p = RAIZ / "SANDBOX_MANIFEST_R3_4.json"
with open(p, "xb") as f:
    f.write(json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
print(json.dumps(dict(n_b1=rec["n_b1"], n_b2=rec["n_b2"], nos=rec["nos"]["um_py"]["sha256"][:16], nos_v392=rec["nos_v392"]["um_py"]["sha256"][:16],
                      kernel_manifest_v391=rec["nos"]["kernel_manifest"]["sha256"][:16], kernel_manifest_v392_sintetico=rec["nos_v392"]["kernel_manifest"]["sha256"][:16],
                      manifesto_b2=rec["manifesto_b2_sha256"][:16], elos=rec["fx"]["elos_de_ensaio"], manifest=str(p)), ensure_ascii=False, indent=1))

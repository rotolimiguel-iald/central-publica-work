from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import ast

ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt").resolve()
OUT = Path(__file__).resolve().parent
FILES = [
"REEXAME_SUFICIENCIA_085_20260910/REEXAME_SUFICIENCIA.md",
"REEXAME_SUFICIENCIA_085_20260910/MEMORIA_DE_TRABALHO_085.md",
"REEXAME_SUFICIENCIA_085_20260910/DESENHO_DO_FECHAMENTO_ADENDO_085.md",
"REEXAME_SUFICIENCIA_085_20260910/ESTADO_CANONICO_085.json",
"REEXAME_SUFICIENCIA_084_20260910/ESTADO_CANONICO_084.json",
"REEXAME_SUFICIENCIA_085_20260910/capture_current085.py",
"REEXAME_SUFICIENCIA_085_20260910/finalize_delivery085.py",
"REEXAME_SUFICIENCIA_085_20260910/PROVENIENCIA_HELPERS_085.json",
"INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md",
"INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/MANIFESTO_INVARIANTES_QUADRATICOS_085.json",
"PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md",
"PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/MANIFESTO_PRIMEIRA_PAGINA_085.json",
"REVISAO_INVARIANTES_KILLING_085_20260910_061730_221515/PARECER_KT_LINEAR_E_INVARIANTES_085.md",
"REVISAO_INVARIANTES_KILLING_085_20260910_061730_221515/REGISTRO_REVISAO_INVARIANTES_085.json",
"REVISAO_PRIMEIRA_PAGINA_085_20260910_062843_679705/PARECER_TODAS_VALENCIAS_E_INVARIANTES_085.md",
"REVISAO_PRIMEIRA_PAGINA_085_20260910_062843_679705/REGISTRO_REVISAO_PRIMEIRA_PAGINA_085.json",
"REVISOES_RAIZ_085_20260910/PARECER_NULIDADE_INVARIANTES_QUADRATICOS_085.md",
"REVISOES_RAIZ_085_20260910/REGISTRO_REVISAO_RAIZ_085.json",
]
PINS = {}; RAW = {}; checks = []; skipped = []
def pin(path):
    p = Path(path).resolve()
    assert p.is_relative_to(ROOT), "Only Chatgpt files may be read in this review"
    raw = p.read_bytes()
    data = {"path": p.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    if data["path"] in PINS:
        assert PINS[data["path"]] == data, "Changed input: " + str(p)
    else:
        PINS[data["path"]] = data; RAW[data["path"]] = raw
    return data
def check(name, passed, detail=None):
    checks.append({"name": name, "passed": bool(passed), "detail": detail})
    assert passed, checks[-1]
def new(name, raw):
    p = OUT / name
    assert p.resolve().is_relative_to(ROOT) and not p.exists() and raw
    tmp = p.with_name(p.name + ".tmp_" + datetime.now().strftime("%H%M%S_%f"))
    with tmp.open("xb") as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    assert tmp.read_bytes() == raw
    tmp.rename(p)
    assert p.read_bytes() == raw
    return {"path": p.as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
def verify(value, origin):
    if isinstance(value, dict):
        if isinstance(value.get("path"), str) and re.fullmatch("[a-fA-F0-9]{64}", str(value.get("sha256", ""))):
            p = Path(value["path"]).resolve()
            if p.is_relative_to(ROOT):
                actual = pin(p)
                check("local_recorded_pin:" + origin, actual["sha256"] == value["sha256"].lower() and
                      ("bytes" not in value or actual["bytes"] == value["bytes"]), actual["path"])
            else:
                skipped.append({"origin": origin, "recorded": value, "reason": "External originals not reopened; canonical comparison uses snapshots only."})
        for k, child in value.items(): verify(child, origin + "." + k)
    elif isinstance(value, list):
        for i, child in enumerate(value): verify(child, origin + "[" + str(i) + "]")
script_before = pin(Path(__file__))
for rel in FILES: pin(ROOT / rel)
for rel in FILES:
    p = ROOT / rel
    raw = RAW[p.as_posix()]
    if p.suffix == ".json": verify(json.loads(raw), rel)
    if p.suffix == ".py":
        ast.parse(raw.decode("utf-8-sig"))
        check("helper_valid_ast:" + rel, True)
    if p.suffix == ".md":
        for i, path in enumerate(re.findall(r"\]\(<(C:/[^>]+)>\)", raw.decode("utf-8-sig"))):
            check("link:" + rel + ":" + str(i), Path(path).is_file(), path)
s85 = json.loads(RAW[(ROOT / FILES[3]).as_posix()])
s84 = json.loads(RAW[(ROOT / FILES[4]).as_posix()])
p84 = {p["path"]: p for p in s84["pins"]}
canonical_comparison = []
for p in s85["pins"]:
    if p["path"].endswith(("/Nós/um.py", "/Nós/um_absoluto_selo.json", "/Nós/tgl_kernel_proof_manifest.json", "/Nós/rodada_v338_stdout.txt")):
        equal = p["path"] in p84 and p == p84[p["path"]]
        check("canonical_pin_between_snapshots:" + p["path"], equal)
        canonical_comparison.append({"path": p["path"], "same_recorded_pin": equal, "current_original_reopened": False})
check("four_canonical_pins", len(canonical_comparison) == 4)
check("snapshot_module_counts", s85["present"] == 77 and len(s85["modules"]) == 98 and len(s85["absent"]) == 21 and s85["embedded_files"] == 683)
check("snapshot_presence_same_as084", s85["modules"] == s84["modules"] and s85["absent"] == s84["absent"])
check("snapshot_gate_same_as084", s85["seal_excerpt"] == s84["seal_excerpt"])
check("snapshot_stability_declared", s85["all_read_sources_unchanged"] and s85["seal_um_hash_matches"])
report = RAW[(ROOT / FILES[0]).as_posix()].decode("utf-8-sig")
for label, terms in [
    ("fixed_category", ["K>0 real fixado", "escalares herdados inertes"]),
    ("m0_distinct", ["m=0", "grau zero"]),
    ("first_page_not_total", ["primeira página", "BRST interagente"]),
    ("current_still_open", ["Não é uma construção da corrente", "TODAS as ordens finitas"]),
    ("no_new_math", ["Zero nova execução matemática", "CAS, Lean"]),
    ("phase_branch_h3_preserved", ["fase/ramo e H3", "não reabre H3"]),
    ("086_excluded", ["investigação086 está excluída"]),
]:
    check("report_scope_marker:" + label, all(term in report for term in terms))
note = r"""# Revisão documental independente da consolidação085

10/09/2026. [REAL — leitura e integridade documental]. [DERIVED — parecer de fidelidade dos documentos às demonstrações e revisões identificadas]. Não identifiquei erro material na consolidação examinada.

A revisão abrange os três documentos de síntese, snapshot085 comparado ao snapshot084, os dois helpers085 e sua proveniência, as duas demonstrações085, seus manifestos, as duas revisões independentes de Herschel e o parecer da raiz. Os arquivos lidos e comparações efetivamente realizadas constam do recibo. Não reabri nenhum original canônico nesta tarefa.

## 1. Resultado pago e obrigação que permanece aberta

O relatório, a memória e o desenho registram corretamente a nulidade de (Rher⊗Sym²M)^g no domínio da prova de Turing. g é toda a álgebra de Killing. Não reduziram a invariância a Lorentz, não presumiram liberdade da torre Weyl e não trocaram a igualdade no quociente algébrico por anulação em testes TT.

A consequência do critério084 é fiel: J_Wν é CE-exato se e somente se J_W=div V para corrente natural quadrática finita no mesmo módulo. O coeficiente quadrático Euler e o coeficiente quadrático Cartan de traço são zero; a unidade em grau zero não é uma exceção dentro de Sym²M. A existência ou inexistência da corrente permanece aberta na entrega085. O texto preserva a exclusão084 de c grad J_W sem promover essa família a todas as correntes.

As notas086, inclusive a classificação de W∇W escrita por este revisor, estão excluídas. Nenhum resultado delas foi usado para tornar o relato085 retrospectivamente mais forte.

## 2. Generalização: primeira página e todos os graus finitos

O enunciado H^q(s0)|E=Rher⊗[Sym^(E−q)M⊗Λ^qG]^h coincide com a nova demonstração e com a revisão específica de Herschel: q entre0 e min(E,10), zero fora da faixa. A exatidão dos graus negativos do complexo LINEAR, a simetria graduada e os cortes finitos são os antecedentes usados; antifields não foram retirados por omissão.

O primeiro diferencial CE em cada m=E−q foi generalizado por identidades em geradores e Leibniz, mantendo diferenças s0-exatas e primitivas finitas. Os documentos não o apresentam como o BRST total, não eliminam s2,s3,... e não tomam o CE invariante com ghosts de isotropia pelo complexo relativo horizontal.

Os invariantes positivos são nulos para m>0, enquanto o polinômio algébrico inteiro conserva Rher em grau zero. m=0 e seu canal Euler constante estão explicitamente separados. A conclusão não é estendida a um produto completado sem categoria declarada. A condição de dQ horizontal permanece parte da forma normal invocada.

A revisão da entrada quadrática e o parecer da raiz não foram usados como aprovação antecipada da generalização: existe revisão específica independente no caminho ligado abaixo, que a raiz informou ligar no adendo final.

## 3. Hipóteses e estatutos

K>0 real fixado, κ não nulo fixado, espaço-forma orientada Lorentziana quatro-dimensional, φ0 constante projetada, jatos finitos por expressão e extensão escalar inerte Rher permanecem visíveis. Nenhum anel menor substitui Rher; a planura é sobre o corpo real e conserva nilpotentes. Não há um teorema sobre K variável, espectadores tensoriais ou a matéria física φ=id obtido por silêncio.

A passagem temporária a coeficientes C∞(x) é corretamente apresentada como classe auxiliar: o resultado zero retorna ao mesmo ideal pontual pela inclusão simétrica. Isso não naturaliza uma primitiva arbitrária do problema de divergência. Os grupos de graus horizontais zero e quatro permanecem distintos.

As demonstrações são escritas e revisadas. Os documentos não promovem recibos de integridade a teoremas Lean, novos CAS, QME, ausência geral de anomalias ou solução UV. Fase/ramo e H3 da tela são preservados como antecedentes reconhecidos no modelo; o H³ cohomológico não reabre a hipótese H3 da tela.

## 4. Snapshot e helpers: alcance do controle

Confrontei os quatro pins canônicos REGISTRADOS em snapshot085 com os de084. São idênticos; a lista AST registrada conserva683 arquivos,77/98 módulos e21 ausentes, e os campos de selo/gates também coincidem. O presente controle é ENTRE SNAPSHOTS. Não é uma nova medição dos bytes canônicos vivos ou uma reprodução do selftest.

capture_current085.py foi lido como texto e AST: lê bytes, usa ast.parse/literal_eval para o embutido, confere pins antes/depois e cria um snapshot novo. Não executa/importa um.py. finalize_delivery085.py foi igualmente lido, sem execução: exige documentos e destinos novos, verifica pins/links, usa escrita exclusiva temporária, fsync e conferência de bytes antes/depois do rename, escreve somente sob Chatgpt e deixa goal_complete:false. Os contadores exigidos são zero para execução matemática/CAS e Lean; seus checks finais são documentais.

O finalizador foi examinado antes da configuração, adendo, túnel, RESULTADO e MANIFESTO finais da entrega. Esta revisão não atesta a execução futura dele nem aprova esses arquivos ainda não auditados. A comparação dos helpers adaptados com seus pins de proveniência foi documental, sem rodá-los.

## 5. Precisão temporal e independência

O parecer quadrático de Herschel usou “entrega084 encerrada” antes do recibo final084. A revisão seguinte e o parecer da raiz registram a precisão aditiva: a finalização efetiva ocorreu depois. O relatório085 não usa essa antecipação como evidência de custódia. O adendo final será o lugar informado pela raiz para ligar essa precisão sem alterar fontes congeladas.

Este revisor é autor de antecedentes080/081/082 utilizados pelas provas085. A presente revisão é independente da autoria dos três documentos de síntese, das duas demonstrações085 e dos pareceres de Herschel; é uma conferência documental de fidelidade e escopo. Não se apresenta como nova revisão matemática adversarial integral de seus próprios antecedentes, nem como uma quarta prova do resultado principal.

Nenhum original, memória canônica, Atlas, selo ou arquivo já existente foi alterado. Somente novos parecer/recibo/emissor nesta pasta Chatgpt; nenhuma execução/importação de um.py, CAS ou Lean.

## Referências principais

- [Relatório085](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_085_20260910/REEXAME_SUFICIENCIA.md>)
- [Memória085](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_085_20260910/MEMORIA_DE_TRABALHO_085.md>)
- [Desenho085](<C:/IALD/Central de Patentes/Chatgpt/REEXAME_SUFICIENCIA_085_20260910/DESENHO_DO_FECHAMENTO_ADENDO_085.md>)
- [Revisão quadrática de Herschel](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_INVARIANTES_KILLING_085_20260910_061730_221515/PARECER_KT_LINEAR_E_INVARIANTES_085.md>)
- [Revisão específica da generalização](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_PRIMEIRA_PAGINA_085_20260910_062843_679705/PARECER_TODAS_VALENCIAS_E_INVARIANTES_085.md>)
- [Parecer da raiz sobre a entrada quadrática](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_085_20260910/PARECER_NULIDADE_INVARIANTES_QUADRATICOS_085.md>)
"""
before = list(PINS.values())
for p in before: check("stable_source:" + p["path"], pin(p["path"]) == p)
note_pin = new("PARECER_FIDELIDADE_E_ESCOPO_ENTREGA_085.md", note.encode("utf-8"))
receipt = {
    "status": "PASS_DOCUMENTARY_REVIEW_DECLARED_SCOPE_NO_MATERIAL_ERROR",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "direct_files": FILES, "sources_before": before,
    "sources_after": [pin(p["path"]) for p in before],
    "all_sources_unchanged": True, "checks": checks,
    "checks_total": len(checks), "checks_passed": sum(c["passed"] for c in checks),
    "canonical_comparison_between_snapshots": canonical_comparison,
    "external_pins_not_reopened": skipped,
    "note": note_pin, "new_mathematical_executions": 0, "new_lean_executions": 0,
    "um_executed_or_imported": False, "originals_written": False,
    "finalizer_executed": False,
    "not_audited": ["future CONFIG_ENTREGA_085", "future ADENDO_REVISOES_085", "future tunnel085", "future RESULTADO_ENTREGA_085", "future MANIFESTO_ENTREGA_085", "investigation086"],
    "scope": "Document fidelity, historical pins and static helpers; not a new mathematical verification of every antecedent."
}
receipt_pin = new("REGISTRO_REVISAO_DOCUMENTAL_ENTREGA_085.json", (json.dumps(receipt, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({"note": note_pin, "receipt": receipt_pin, "sources_preserved": len(before),
                  "checks": len(checks), "passed": receipt["checks_passed"]}, ensure_ascii=False))


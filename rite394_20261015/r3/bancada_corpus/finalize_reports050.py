"""Generate exclusive050 reports only after the independently audited final build."""
from pathlib import Path
from datetime import datetime, timezone
import os, sys, json, hashlib, subprocess
ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "CONTINUACAO050_CLEAN_BUILD.json"
REVIEW = ROOT / "CONTINUACAO050_REVISAO_INDEPENDENTE.md"
REPORT = ROOT / "CONTINUACAO050_PARECER.md"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_050_adjunto_quadrado_e_resolvente.md"

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def link(path, label=None):
    path = Path(path)
    return "[" + (label or path.name) + "](<" + path.as_posix() + ">)"

def new_bytes(path, raw):
    if path.exists() or not path.resolve().is_relative_to(ROOT) or not raw:
        raise RuntimeError("Nonexclusive output")
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("xb") as stream:
        stream.write(raw)
        stream.flush()
        os.fsync(stream.fileno())
    if temporary.read_bytes() != raw or path.exists():
        raise RuntimeError("Temporary verification failed")
    temporary.rename(path)
    if path.read_bytes() != raw:
        raise RuntimeError("Final verification failed")

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if REPORT.exists() or DELIVERY.exists():
        raise RuntimeError("Reports already exist")
    result = subprocess.run(
        [sys.executable, "-B", str(ROOT / "audit_continuation050.py"), "--build-only"],
        cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(result.stdout.decode("utf-8", errors="replace"))
    audit = json.loads(result.stdout)
    if audit["status"] != "BUILD_PASS":
        raise RuntimeError("Final build rejected")
    data = json.loads(BUILD.read_text(encoding="utf-8"))
    review = REVIEW.read_text(encoding="utf-8")
    clean = Path(data["clean_directory"])
    if ("BUILD_PASS" not in review or "Build SHA256: " + digest(BUILD) not in review
            or "Diretório final: " + clean.as_posix() not in review):
        raise RuntimeError("Independent review is not bound to this build")
    totals, baseline, combined = data["totals"], data["baseline_totals"], data["all_totals"]
    timestamp = datetime.now(timezone.utc).isoformat()
    meanings = {
        "GenericAntilinearAdjoint": "Adjunto antilinear maximal de JT, domínio e composição.",
        "ContinuousModularSquare": "Domínio efetivo de T_c² e igualdade global T_c²=T_(2c).",
        "ContinuousModularReconstruction": "S†S identificado pelo grafo completo; Δ positivo auto-adjunto e forma quadrática.",
        "ContinuousModularResolvent": "Resolvente limitado e reconstrução do grafo pelas raízes CFC de operadores limitados."
    }
    table = ["| Módulo novo050 | Teoremas | Definições | Prints | Alcance |",
             "|---|---:|---:|---:|---|"]
    for module in data["new_modules"]:
        info = data["source_info"][module]
        table.append(f"| {link(ROOT / (module + '.lean'))} | {info['theorems']} | {info['definitions']} | {info['axiom_prints']} | {meanings[module]} |")
    table_text = "\n".join(table)
    report = f"""# Continuação050 — adjunto, quadrado e reconstrução pelo resolvente

[REAL — escopo dos teoremas compilados e auditados] Emissão UTC: {timestamp}

O lote liga o operador de Tomita contínuo da049 ao operador Δ=S†S e reconstrói o grafo de sua raiz positiva por cálculo funcional contínuo de operadores limitados. O espaço H=L²(ℝ,dξ;ℂ) e o parâmetro c são os dados do modelo049. Não se demonstra aqui que a natureza ou a torre anterior selecionem esse modelo.

## Adjunto maximal e domínio da composição

Para T_c f(ξ)=exp(-cξ)f(ξ), em seu domínio ponderado efetivo, e Jf(ξ)=conj(f(-ξ)), o operador anterior é S_c=JT_c. A identidade com a construção genérica está provada, não presumida por igualdade de nomes.

O adjunto antilinear S_c†=T_cJ tem domínio {{y:Jy∈D(T_c)}}. A convenção de pareamento é ⟨S_cx,y⟩=⟨S_c†y,x⟩. Além da identidade, prova-se maximalidade: todo par (y,z) que satisfaz o pareamento para todos os x no domínio pertence ao grafo desse adjunto. A prova usa a densidade e o adjunto linear maximal do Mathlib.

A composição exige duas pertinências de domínio. Para todo f∈H:

    f∈D(S_c†S_c) ⇔ f∈D(T_c) e T_cf∈D(T_c) ⇔ f∈D(T_(2c)).

O teorema do grafo completo identifica Δ_c com S_c†S_c, incluindo domínio e valor; a igualdade global de operadores parciais fornece:

    Δ_c = S_c†S_c = T_c² = T_(2c).

Δ_c é positivo, auto-adjunto e fechado. A forma quadrática satisfaz Re⟨Δ_cf,f⟩=||S_cf||² em D(Δ_c); pela simetria hermitiana, a mesma parte real aparece em ⟨f,Δ_cf⟩. T_c é uma raiz positiva auto-adjunta de Δ_c.

## Reconstrução intrínseca pelo resolvente

Os operadores limitados A e B da049 satisfazem A²+B²=I e parametrizam o grafo de T_c por (Ah,Bh). A positividade de A e B foi provada na ordem de operadores, a partir dos multiplicadores positivos.

O lote demonstra que C=A² é o inverso limitado de I+Δ_c, com a imagem no domínio de Δ_c e as duas identidades inversas. A unicidade nesse contrato impede que o nome resolvente substitua sua propriedade.

No cálculo funcional contínuo de operadores limitados do Mathlib:

    sqrt(C)=A,     sqrt(I-C)=B,
    Graph(T_c) = {{(sqrt(C)h, sqrt(I-C)h): h∈H}},
    D(T_c) = range(sqrt(C)).

Assim o grafo do T_c construído é recuperado das raízes positivas limitadas do resolvente de Δ_c. Essa é uma caracterização intrínseca concreta da raiz; distingue-se do teorema geral de unicidade entre todas as raízes positivas auto-adjuntas não limitadas.

[KNOWN + DERIVED — identificação matemática com teorema externo] A unicidade clássica da raiz positiva auto-adjunta, aplicada a T_c²=Δ_c e à positividade/auto-adjunticidade de T_c, identifica T_c=Δ_c^(1/2), portanto JS_c=Δ_c^(1/2), neste modelo. Essa especialização usa o [teorema2.3 de Sebestyén–Tarcsay, manuscrito disponibilizado pelo autor](https://www.researchgate.net/publication/318660686_On_the_square_root_of_a_positive_selfadjoint_operator). O teorema geral externo não integra os axiomas nem o censo Lean050.

[OPEN — formalização geral] CFC.sqrt_unique aplica-se aqui aos operadores limitados A e B. Não foi aplicado diretamente a LinearPMap nem fornece, sem lemas adicionais, a unicidade entre todos os Q positivos auto-adjuntos não limitados com Q²=Δ. A nota independente {link(ROOT / 'NOTA050_RAIZ_POSITIVA_CANONICA_REVISAO.md')} registra a rota e a dívida.

## Censo e verificação

{table_text}

- Novos050: {totals['theorems']} teoremas, {totals['definitions']} definições, {totals['instances']} instâncias próprias, {totals['axiom_prints']} prints.
- Baseline049, com seis fontes pinados e recompilados: {baseline['theorems']} teoremas, {baseline['definitions']} definições, {baseline['axiom_prints']} prints.
- Conjunto recompilado: {combined['theorems']} teoremas, {combined['definitions']} definições, {combined['axiom_prints']} prints; {len(data['steps'])}/{len(data['steps'])} etapas passaram, incluindo importador conjunto.
- Zero avisos/erros, cobertura exata das declarações por prints e somente propext, Classical.choice e Quot.sound.
- Fontes copiados por bytes em diretório exclusivo; inputs estáveis, sem fallback a oleans locais históricos ou do kernel canônico.
- Auditor independente BUILD_PASS; revisão vinculada ao hash e ao diretório final. Fontes e sondas falhas anteriores permanecem como histórico, sem serem promovidas a prova.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

A fronteira externa de confiança compreende imports diretos do Mathlib/stdlib e companheiros pinados. Não foi reconstruída toda a cadeia transitiva externa a partir de fontes. A proveniência dos seis fontes049 é verificada; o auditor050 não repete a auditoria integral de todos os artefatos do selo049.

## O que permanece aberto

[OPEN] Formalização geral da unicidade da raiz não limitada, fluxo Δ^it e sua ação geométrica, rede física de álgebras e estado, Bisognano–Wichmann, inclusão semilateral, ligação desta representação com a torre, seleção física de c, área, H3 e reconstrução gravitacional geral.

A escala c, o espaço L² e sua medida são INPUT do modelo. A identificação matemática local não constitui prova de gravidade quântica. Esta rodada escreve somente em Chatgpt; não incorpora código em um.py, kernel, Atlas, índice ou memórias canônicas. canonical_gate_changed=false é declaração de escopo da escrita, não auditoria de mudanças de terceiros.

Revisão: {link(REVIEW)}. Entrega: {link(DELIVERY)}.
"""
    new_bytes(REPORT, report.encode("utf-8"))
    artifacts = [
        ROOT / "CONTINUACAO050_DERIVACAO_PREVIA.md",
        *sorted(ROOT.glob("DERIVACAO050_*.md")),
        ROOT / "NOTA050_RAIZ_POSITIVA_CANONICA_REVISAO.md",
        *[ROOT / (m + ".lean") for m in data["new_modules"]],
        ROOT / "CONTINUACAO049_MANIFESTO.json",
        ROOT / "clean_continuation050.py", ROOT / "audit_continuation050.py",
        Path(__file__).resolve(), BUILD, REVIEW, REPORT]
    rows = ["| Artefato | Bytes | SHA256 lido do arquivo |", "|---|---:|---|"]
    for path in artifacts:
        rows.append(f"| {link(path)} | {path.stat().st_size} | {digest(path)} |")
    delivery = f"""# Entrega050 — adjunto, quadrado e resolvente

[REAL — compilado e auditado na bancada] UTC: {timestamp}

S_c†=T_cJ foi construído como adjunto maximal. O grafo completo da composição prova Δ_c=S_c†S_c=T_c²=T_(2c), incluindo a igualdade global dos domínios. Δ_c é positivo auto-adjunto; Re⟨Δ_cf,f⟩=||S_cf||². O resolvente C=(I+Δ_c)^-1 recupera o grafo de T_c por (sqrt(C)h,sqrt(I-C)h), com raízes limitadas do CFC.

[OPEN] A formalização de unicidade entre todas as raízes positivas auto-adjuntas não limitadas permanece distinta dessa reconstrução concreta. O lote não demonstra fluxo físico, BW, H3 ou reconstrução gravitacional geral.

{table_text}

Novos050: {totals['theorems']}T/{totals['definitions']}D/{totals['axiom_prints']} prints. Baseline049 recompilada e contada separadamente: {baseline['theorems']}T/{baseline['definitions']}D/{baseline['axiom_prints']} prints. Conjunto: {combined['theorems']}T/{combined['definitions']}D/{combined['axiom_prints']} prints. {len(data['steps'])}/{len(data['steps'])} etapas PASS; zero avisos/erros e somente axiomas trio.

Parecer completo: {link(REPORT)}. Revisão: {link(REVIEW)}.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

## Artefatos e proveniência

{chr(10).join(rows)}

Os seis fontes049 são conferidos contra o manifesto anterior e recompilados. Nenhum olean049 entra no caminho de imports. A fronteira externa limita-se aos imports diretos e seus companheiros; não se afirma reconstrução transitiva de todo Mathlib.

Auditoria selada, somente leitura:

    C:\\Python314\\python.exe -B "{ROOT / 'audit_continuation050.py'}"

CONTINUACAO050_MANIFESTO.json é emitido depois deste documento, evitando hash autorreferente. O comando acima verifica o selo quando presente. Correções e sondas de desenvolvimento são preservadas; apenas a compilação final e sua revisão sustentam os resultados declarados.

H3: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Nenhuma escrita no gate canônico por esta rodada. NOT_FALSIFIED não é CONFIRMED.
"""
    new_bytes(DELIVERY, delivery.encode("utf-8"))
    print(json.dumps({"status": "REPORTS_CREATED", "report": str(REPORT),
        "report_bytes": REPORT.stat().st_size, "report_sha256": digest(REPORT),
        "delivery": str(DELIVERY), "delivery_bytes": DELIVERY.stat().st_size,
        "delivery_sha256": digest(DELIVERY)}, ensure_ascii=False))

if __name__ == "__main__":
    main()

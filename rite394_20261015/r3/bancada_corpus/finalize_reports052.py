"""Create exclusive052 reports after the audited final build and independent review."""
from pathlib import Path
from datetime import datetime, timezone
import os, sys, json, hashlib, subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "CONTINUACAO052_CLEAN_BUILD.json"
REVIEW = ROOT / "CONTINUACAO052_REVISAO_INDEPENDENTE.md"
REPORT = ROOT / "CONTINUACAO052_PARECER.md"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_052_setor_horizontal_e_area.md"

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def link(path, label=None):
    path = Path(path)
    return "[" + (label or path.name) + "](<" + path.as_posix() + ">)"

def new_bytes(path, raw):
    if path.exists() or not path.resolve().is_relative_to(ROOT) or not raw:
        raise RuntimeError("Exclusive new output required")
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
    result = subprocess.run([sys.executable, "-B", str(ROOT / "audit_continuation052.py"),
        "--build-only"], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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
        raise RuntimeError("Independent review does not identify this final build")
    counts = audit["counts"]
    timestamp = datetime.now(timezone.utc).isoformat()
    meanings = {
        "LocalHorizontalPauli": "Pinching, pareamento GNS e derivadas efetivas do estado.",
        "ModularHorizontalRotation": "Rotação e orientação pelo horizonte modular concreto.",
        "HorizontalAreaSelection": "Seleção por quarto de volta e dois critérios de escala.",
        "QuantumOrbitArea": "Ligação ao estado, horizonte, positividade e densidade de área."
    }
    table = ["| Módulo052 | Teoremas | Definições | Instâncias | Prints | Alcance |",
             "|---|---:|---:|---:|---:|---|"]
    for row in data["sources"]:
        table.append(f"| {link(ROOT / (row['module'] + '.lean'))} | {row['theorems']} | {row['definitions']} | {len(row['instances'])} | {len(row['expected_axiom_rows'])} | {meanings[row['module']]} |")
    table_text = "\n".join(table)
    report = f"""# Continuação052 — plano horizontal, horizonte modular e área

[REAL — escopo das declarações compiladas e auditadas] UTC: {timestamp}

O lote liga duas direções efetivas de variação do estado ao horizonte modular da mesma torre. Nesse plano, a invariância de uma forma bilinear real simétrica pelo quarto de volta modular fixa sua forma até escala. Uma normalização explícita fixa a escala. Separadamente, o pareamento imaginário do estado com o quarto de volta orientado constrói uma forma positiva com escala dependente do estado. H3 e a reconstrução gravitacional geral permanecem OPEN.

## Correção ao lado da proposta051

A {link(ROOT / 'NOTA052_CORRECAO_AREA051.md', 'nota de correção052')} registra o limite da proposta de ponderar E e I−E por escalas distintas. A direção centralizante Z usada no exemplo é vertical para a órbita unitária do estado: ela não altera esse estado. No setor horizontal do exemplo, a família reduz-se a um múltiplo da forma GNS; normalizar pode remover essa liberdade. Além disso, a034 já define literalmente sua forma pelo produto GNS. Trocar a forma troca o critério daquela construção.

A proposta051 e sua custódia permanecem intactas. A nota052 é análise de escopo, não um novo teorema Lean de classificação do quociente global. A052 investiga diretamente um plano de variações observáveis.

## Mesmo estado, operadores e derivadas

Sejam p=P.w(0), com 0<p<1, r=2p−1 e ν=log(p)−log(1−p). No primeiro sítio, X e Y são os operadores de Pauli existentes. Para u=(u₀,u₁), definir H(u)=u₀X+u₁Y. Para p≠1/2, a expectativa centralizante efetiva da046 satisfaz E(X)=E(Y)=0. A relação com o pinching local é demonstrada pelas propriedades da mesma expectativa, sem introduzir outro operador E.

O pareamento da mesma torre é:

    Re ω(H(u)* H(v)) = u₀v₀+u₁v₁,
    Im ω(H(u)* H(v)) = r(u₀v₁−u₁v₀).

Aqui * denota adjunto; H(u) é autoadjunto. As duas direções têm norma GNS um e são ortogonais para a parte REAL. No espaço complexo, seu produto é i r, portanto não são ortogonais complexas quando r≠0.

Usando a curva unitária existente da035, com U(t)=exp(i t H(u)) e leitura ω(U(t)* B U(t)), as derivadas reais nas leituras X,Y são:

    resposta(u) = (−2r u₁, 2r u₀),
    determinante da matriz de resposta = 4r².

Quando p≠1/2, a resposta é injetiva. Assim, direções distintas desse plano produzem derivadas distinguíveis de leituras do estado global. Trata-se de um plano da órbita UNITÁRIA, não de todos os tangentes de estados ou de variações dos autovalores.

O lema quantum_centralizer_imaginary_zero demonstra ainda que a parte imaginária do pareamento entre um elemento autoadjunto centralizante e um elemento autoadjunto do fator é zero, pela ciclicidade e pela conjugação do estado. Isso identifica uma obstrução vertical; não constrói sozinho o quociente global completo.

## O quarto de volta é realizado pelo horizonte concreto

A ação modular existente satisfaz:

    σ_t(X) = cos(νt)X − sin(νt)Y,
    σ_t(Y) = sin(νt)X + cos(νt)Y.

No tempo t₀=−π/(2ν), essa ação induz R(u₀,u₁)=(−u₁,u₀). A igualdade entre adT do horizonte efetivo e H(Ru) foi demonstrada, usando os mesmos objetos das duas etapas anteriores.

[INPUT] Para selecionar a forma, exige-se bilinearidade real, simetria e invariância simultânea das duas entradas pelo quarto de volta efetivo. Não se postula previamente isotropia. Para uma função F nos operadores e sua restrição bilinear b(u,v)=F(H(u),H(v)), as hipóteses implicam:

    b = c · ReGNS,  com c=b(e₀,e₀).

A simetria exclui a componente antissimétrica. A positividade não é necessária para essa igualdade; quando desejada, impõe o sinal correspondente a c.

## Dois critérios de escala, explicitamente distintos

1. [INPUT] Normalização do traço relativo ao produto GNS real: b(e₀,e₀)+b(e₁,e₁)=1. Então c=1/2 e a densidade de área sobre o par fixo (e₀,e₁) é 1/2.

O lema da soma diagonal em pares unitários é usado DEPOIS da seleção b=c·ReGNS. Ele não deve ser citado como uma demonstração de invariância geral do traço antes dessa seleção.

2. Definir Ω(u,v)=Im ω(H(u)*H(v)) e tomar o tempo orientado tₒ=−π/(2|ν|)<0. A ação efetiva induz Q=sign(r)R. Construir a própria função:

    gΩ(u,v) = Im ω(H(u)* σ_tₒ(H(v))) = Ω(u,Qv).

Sua bilinearidade é provada a partir dessa expressão. A052 demonstra:

    gΩ(u,v) = |r| ReGNS(u,v),
    gΩ é simétrica, positiva e não degenerada para r≠0,
    área(gΩ; e₀,e₁) = |r|,
    Ω(u,v) = −gΩ(u,Qv),  Q²=−I.

A fórmula da compatibilidade tem sinal negativo com essa ordem dos argumentos. O tempo de quarto de volta positivo daria orientação oposta. Q é um operador linear real no plano e não a conjugação modular antilinear J, para a qual J²=I.

[INPUT] Usar Ω e esse quarto de volta para calibrar a forma é um critério adicional à covariância; a covariância sozinha deixa c livre. Não se identifica aqui gΩ com Fisher, Bures ou uma área física de horizonte.

Para o perfil de referência com p=1/3, a densidade calibrada nesse par é exatamente 1/3. Esse par de Pauli não é a tela de outro lote; comparar esse valor com uma área de outra tela exige primeiro identificar os pares e os critérios.

Essas áreas são densidades de Gram no par de geradores fixado, transportáveis às derivadas identificadas pela resposta injetiva. Não são a área total da órbita nem a área espacial de uma região. Os dois critérios não precisam dar o mesmo número.

## Controle tracial e fronteira da afirmação

Se p=1/2, a resposta dessas duas direções é zero; E fixa X,Y; a ação modular nesse sítio é a identidade; Ω e quantumOrbitPairing são zero. O mapa auxiliar orbitOrientedTurn(0)=0 não representa essa ação identidade. Outros sítios não traciais podem manter não trivial o fluxo modular da torre inteira.

O relógio modular e a curva unitária usada para medir a resposta são fluxos diferentes. A existência de um quarto de volta no primeiro não identifica automaticamente os seus parâmetros nem fornece o relógio físico da curva do segundo.

[KNOWN — contexto externo] [Petz–Sudar](https://arxiv.org/abs/quant-ph/0102132) discutem a família de métricas quânticas monótonas; isso ajuda a explicar por que uma seleção exige critérios. [Contreras–Ercolessi–Schiavina](https://arxiv.org/abs/1501.00054) estudam órbitas de estados mistos e o tensor de Fisher. Esses trabalhos são contexto; nenhuma identificação com os seus tensores é transportada para a052 sem prova das convenções e normalizações.

## Verificação e custódia

{table_text}

Total052: {counts['theorems']} teoremas, {counts['definitions']} definições, {counts['instances']} instâncias, {counts['axiom_prints']} prints. Compilação conjunta: {len(data['steps'])}/{len(data['steps'])} etapas, incluindo importador. Zero avisos/erros; cobertura exata das declarações; somente propext, Classical.choice e Quot.sound nos relatórios de axiomas. A revisão independente está vinculada ao hash e ao diretório final.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

Os quatro fontes052 foram copiados por bytes e compilados em diretório exclusivo. As dependências históricas foram verificadas e copiadas por pins; não foram recompiladas nesta rodada. O auditor repete o vínculo upstream045 entre origens, snapshots e adaptações. Imports externos diretos e companheiros Mathlib/stdlib foram medidos; não se afirma reconstrução exaustiva do fecho transitivo externo. Fontes locais usadas apenas para descoberta de imports não ganham proveniência fonte–binário por terem hash de leitura.

Sondas falhas, logs e backups ficam preservados como história, sem valor de prova. Escritas deste lote somente em Chatgpt. canonical_gate_changed=false registra esse escopo, sem auditar mudanças feitas por terceiros. Atlas, índice, um.py, kernel e memórias canônicas não recebem incorporação deste lote.

## Caminho ainda aberto

[OPEN] Selecionar fisicamente estado, álgebra, região e observadores; ampliar e compatibilizar os planos em outros pontos/sítios; justificar escala dimensional e área de horizonte; reconstruir métrica lorentziana e dinâmica; demonstrar o vínculo Ricci–matéria de H3. A052 estabelece uma construção e uma seleção condicionada em um setor concreto, sem resolver a reconstrução gravitacional geral.

Revisão: {link(REVIEW)}. Entrega: {link(DELIVERY)}. QG não está declarada confirmada, resolvida ou provada.
"""
    new_bytes(REPORT, report.encode("utf-8"))
    artifacts = [ROOT / "CONTINUACAO052_DERIVACAO_PREVIA.md",
        *sorted(ROOT.glob("DERIVACAO052_*.md")), *sorted(ROOT.glob("NOTA052_*.md")),
        *[ROOT / (m + ".lean") for m in data["modules"]],
        ROOT / "CONTINUACAO045_UPSTREAM.json", ROOT / "CONTINUACAO047_MANIFESTO.json",
        ROOT / "clean_continuation052.py", ROOT / "audit_continuation052.py",
        Path(__file__).resolve(), BUILD, REVIEW, REPORT]
    rows = ["| Artefato | Bytes | SHA256 lido do arquivo |", "|---|---:|---|"]
    for path in artifacts:
        rows.append(f"| {link(path)} | {path.stat().st_size} | {digest(path)} |")
    delivery = f"""# Entrega052 — setor horizontal e área

[REAL — escopo compilado e auditado] UTC: {timestamp}

No plano de Pauli X,Y do primeiro sítio não tracial, a expectativa centralizante efetiva zera ambas as direções. Suas respostas ao estado são injetivas, com matriz de determinante 4(2p−1)². A ação do horizonte modular realiza o quarto de volta no mesmo plano.

Uma forma bilinear real simétrica invariante por esse horizonte é c vezes o produto GNS real. [INPUT] Traço relativo igual a um fixa c=1/2 e densidade de área 1/2. Separadamente, a função efetiva Im ω(H(u)*σ_tₒ(H(v))), com tₒ=−π/(2|ν|), define uma forma bilinear simétrica positiva de densidade |2p−1|. O sinal da orientação, a nulidade centralizante e o controle tracial estão explícitos.

A densidade é sobre o par de geradores fixado, não uma área espacial ou a área total da órbita. Q²=−I refere-se à rotação real, não à conjugação modular J. Covariância sozinha deixa a escala livre; calibração por Ω é critério adicional.

{table_text}

Total052: {counts['theorems']}T/{counts['definitions']}D/{counts['instances']}I/{counts['axiom_prints']} prints. {len(data['steps'])}/{len(data['steps'])} etapas PASS. Zero avisos/erros, apenas o trio de axiomas permitido. Parecer: {link(REPORT)}. Revisão: {link(REVIEW)}.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

## Artefatos

{chr(10).join(rows)}

Dependências históricas copiadas e verificadas por pins, sem recompilação; vínculo upstream045 revalidado. Fronteira externa medida nos imports diretos e companheiros, não no fecho transitivo integral.

Auditoria selada, somente leitura:

    C:\\Python314\\python.exe -B "{ROOT / 'audit_continuation052.py'}"

CONTINUACAO052_MANIFESTO.json é emitido depois deste documento, evitando hash autorreferente. A correção da proposta051 preserva o original e não promove a nota a teorema Lean.

[OPEN] Seleção física, compatibilidade global, área dimensional, dinâmica, H3 e reconstrução gravitacional geral. Somente Chatgpt recebeu escritas deste lote; o gate canônico não foi alterado por este trabalho. NOT_FALSIFIED não é CONFIRMED.
"""
    new_bytes(DELIVERY, delivery.encode("utf-8"))
    print(json.dumps({"status": "REPORTS_CREATED", "report": str(REPORT),
        "report_bytes": REPORT.stat().st_size, "report_sha256": digest(REPORT),
        "delivery": str(DELIVERY), "delivery_bytes": DELIVERY.stat().st_size,
        "delivery_sha256": digest(DELIVERY)}, ensure_ascii=False))

if __name__ == "__main__":
    main()

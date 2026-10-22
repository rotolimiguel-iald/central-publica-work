"""Create exclusive051 reports after the audited final build and independent review."""
from pathlib import Path
from datetime import datetime, timezone
import os, sys, json, hashlib, subprocess

ROOT = Path(__file__).resolve().parent
BUILD = ROOT / "CONTINUACAO051_CLEAN_BUILD.json"
REVIEW = ROOT / "CONTINUACAO051_REVISAO_INDEPENDENTE.md"
REPORT = ROOT / "CONTINUACAO051_PARECER.md"
DELIVERY = ROOT / "TUNEL/DO_CHATGPT/ENTREGA_051_balanco_optico_finito.md"

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
    result = subprocess.run([sys.executable, "-B", str(ROOT / "audit_continuation051.py"),
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
        "OpticalVolterraBalance": "Identidade integral geral, drift de Ricci e positividade bilateral.",
        "OpticalRiccatiInvariant": "Tensor óptico simétrico, traço de Riccati e invariância por rotação.",
        "OpticalFiniteBalance": "Instância da tela036/043, calor041 e limite quártico da correção.",
        "OpticalBalanceControls": "Ricci afim, ligação matricial ao balanço e orientação térmica."
    }
    table = ["| Módulo051 | Teoremas | Definições | Instâncias | Prints | Alcance |",
             "|---|---:|---:|---:|---:|---|"]
    for row in data["sources"]:
        table.append(f"| {link(ROOT / (row['module'] + '.lean'))} | {row['theorems']} | {row['definitions']} | {len(row['instances'])} | {len(row['expected_axiom_rows'])} | {meanings[row['module']]} |")
    table_text = "\n".join(table)
    report = f"""# Continuação051 — balanço óptico finito e curvatura variável

[REAL — escopo das declarações compiladas e auditadas] UTC: {timestamp}

A correção finita de Clausius do modelo041/043 recebe uma lei integral exata, construída a partir da expansão e do cisalhamento da tela. A correção é definida diretamente pelos dados ópticos, independentemente do calor e do resíduo. O lote também identifica o termo adicional que impede transportar sem alteração a fórmula de Ricci constante para Ricci variável. H3 e a reconstrução gravitacional geral permanecem OPEN.

## Balanço integral geral

Num intervalo aberto convexo I contendo zero, assumir as derivadas A'=Aθ, θ'=−R−F, Q'=−K t M(t)A(t), com θ(0)=Q(0)=0 e a continuidade indicada nos enunciados. Definir:

    Z_f(t) = ∫₀ᵗ f(u)du,
    E_F(t) = ∫₀ᵗ A(s) Z_F(s)ds.

O teorema optical_volterra_balance demonstra:

    Q(t) − K(A(t)−A(0))
      = K ∫₀ᵗ A(s)[Z_F(s)+Z_R(s)−s M(s)]ds.

São hipóteses de evolução e dados iniciais explícitos. A e Q não são reconstruídos de um estado quântico neste lema. Nenhuma positividade de A é necessária para essa identidade algébrica-integral.

Se R=M ponto a ponto, permanece o drift Z_R(s)−sR(s). Só no caso de R=M=r constante ele desaparece, dando Q−KΔA=K E_F. O controle R(t)=r+vt calcula exatamente drift=−v t²/2, com ambos os sinais conforme v. Esse é um controle escalar da parcela de curvatura; não afirma que toda função R escolhida já vem de uma geometria fisicamente selecionada. O sinal pontual do drift tampouco determina sozinho o sinal da integral orientada.

## Tensor óptico e convenção do cisalhamento

Para B=[[x,z],[z,y]], em uma tela real ortonormal de dimensão dois:

    θ = tr(B) = x+y,
    F = tr(B²) = x²+2z²+y²
      = θ²/2 + 2[((x−y)/2)²+z²].

O nome Lean opticalShearNormSq significa ((x−y)/2)²+z²: METADE da norma quadrática do tensor sem traço. Assim, a norma inteira chamada shearNorm na derivação prévia é 2*opticalShearNormSq. O fator dois não é ajuste posterior da identidade.

O traço do sistema B'=−B²−Rmat produz θ'=−tr(Rmat)−F. A norma, o traço e a parcela de cisalhamento são invariantes sob as rotações explícitas OBOᵀ, com c²+s²=1. O sistema inclui as três componentes independentes da matriz simétrica, e sua conexão ao balanço integral está provada no controle com traço Ricci constante.

[INPUT] Essa formulação trabalha no setor simétrico, sem torção óptica. Não é um teorema para toda congruência arbitrária com vorticidade. A base ortonormal, a tela e as equações ópticas continuam dados.

## Instância geométrica e sinal

Na tela036/043, f_a(t)=cos(√a t), q_a=f_a'/f_a e A(t)=|f_a(t)f_c(t)|. Em um intervalo aberto convexo contendo zero, sem zeros de f_a ou f_c, instanciar:

    θ=q_a+q_c,   F=q_a²+q_c²,
    E(t)=∫₀ᵗ A(s)∫₀ˢ(q_a(u)²+q_c(u)²)du ds.

Sob a,c≥0 e a hipótese explícita eta*(a+c)=2π*mass, o calor041 satisfaz:

    opticalClausiusDefect(t) = (rate/(2π))*eta*E(t).

[INPUT] Q herda o peso afim −rate*t do protocolo041. Identificar esse fluxo finito com calor de um horizonte físico exige justificativa adicional; o lote não demonstra uma escolha canônica exata de campo de Killing ou de temperatura.\n\nA transferência para o calor construído geometricamente na043 está demonstrada somente no germe passado já identificado ali. O enunciado intervalar do calor041 não foi usado para estender artificialmente o calor043 para tempos ou domínios ainda não relacionados.

E≥0 nos dois sentidos de tempo, porque as duas integrais orientadas invertem juntas. No contexto regular da identidade, as funções são contínuas e as integrais finitas. Os lemas de positividade abstrata, isolados e sem hipóteses de integrabilidade, usam a integral totalizada do Lean; eles não autorizam uma leitura física através de cáusticas.

O limite bilateral perfurado, para t→0 com t≠0, é E(t)/t⁴ → (a²+c²)/12. Sua prova usa a identidade geométrica e o limite041 com uma especialização auxiliar de parâmetros que fixa K=1; não introduz uma nova seleção física desses parâmetros. O resultado recupera precisamente o resíduo de ordem quatro conhecido.

Para o segmento orientado t→0, ΔS=eta*(1−A(t)) e Q_segmento=−Q(t). Com T≠0, a identidade corresponde a:

    ΔS = Q_segmento/T + eta*E(t).

O lema de orientação é algébrico e exige T≠0; a temperatura física positiva é uma identificação adicional. Para T=0, o controle devolve apenas Q=0. Chamar eta*E de produção FÍSICA de entropia exige justificar a identificação de área, entropia e temperatura.

[KNOWN — contexto externo] A termodinâmica de horizontes fora do equilíbrio e a discussão de dissipação gravitacional aparecem em [Eling–Guedens–Jacobson2006](https://arxiv.org/pdf/gr-qc/0602001) e [Chirco–Liberati2010](https://arxiv.org/pdf/0909.4194). Esses artigos contextualizam a pergunta; não são usados como prova Lean nem demonstram a interpretação física de E neste modelo.

## Verificação e custódia

{table_text}

Total051: {counts['theorems']} teoremas, {counts['definitions']} definições, {counts['instances']} instâncias, {counts['axiom_prints']} prints. Compilação conjunta: {len(data['steps'])}/{len(data['steps'])} etapas, incluindo importador. Zero avisos/erros, cobertura exata das declarações e somente propext, Classical.choice e Quot.sound. A revisão independente liga-se ao hash e ao diretório final.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

Os quatro fontes051 foram copiados por bytes e compilados em diretório exclusivo. Dependências históricas até043 foram reutilizadas por cópias pinadas; o auditor verifica os contratos e os vínculos históricos registrados, sem rebatizar seus binários como recompilados nesta rodada. A fronteira externa inclui imports diretos e companheiros Mathlib/stdlib; não foi reconstruído ou hashado exaustivamente todo o fecho transitivo externo. Fontes locais sem pin histórico têm hash de leitura para descoberta de imports; isso sozinho não estabelece proveniência fonte–binário.

Sondas falhas, logs e backups permanecem guardados como histórico documental. Não sustentam declarações de prova.

## Caminho ainda aberto

[OPEN] Selecionar a álgebra, o estado, o fluxo físico e a geometria; justificar a área/entropia e o casamento Ricci–matéria; tratar curvatura geral, dados ópticos mais gerais e a reconstrução gravitacional. O balanço finito explica uma correção na geometria já dada, mas não deriva a hipótese de H3 da teoria quântica.

A {link(ROOT / 'NOTA051_AREA_COVARIANTE_PENDENTE.md', 'nota sobre área covariante')} propõe uma família por E e I−E com pesos relativos distintos mesmo após normalização. Ela permanece [DERIVED — análise pendente], com obrigações formais explícitas; não pertence ao censo de teoremas051.

Escritas somente em Chatgpt; nenhuma incorporação em um.py, kernel, Atlas, índice ou memórias canônicas. canonical_gate_changed=false descreve o escopo desta rodada, não uma auditoria de alterações por terceiros. QG não está declarada confirmada, resolvida ou provada.

Revisão: {link(REVIEW)}. Entrega: {link(DELIVERY)}.
"""
    new_bytes(REPORT, report.encode("utf-8"))
    artifacts = [ROOT / "CONTINUACAO051_DERIVACAO_PREVIA.md",
        *sorted(ROOT.glob("DERIVACAO051_*.md")), *sorted(ROOT.glob("NOTA051_*.md")),
        *[ROOT / (m + ".lean") for m in data["modules"]],
        ROOT / "CONTINUACAO043_MANIFESTO.json", ROOT / "clean_continuation051.py",
        ROOT / "audit_continuation051.py", Path(__file__).resolve(), BUILD, REVIEW, REPORT]
    rows = ["| Artefato | Bytes | SHA256 lido do arquivo |", "|---|---:|---|"]
    for path in artifacts:
        rows.append(f"| {link(path)} | {path.stat().st_size} | {digest(path)} |")
    delivery = f"""# Entrega051 — balanço óptico finito

[REAL — escopo compilado e auditado] UTC: {timestamp}

O resíduo finito recebe a identidade exata Q−KΔA=K E no caso de Ricci constante com matching explícito, onde E é a integral óptica definida independentemente de Q. No modelo geométrico036/043, E≥0 no intervalo regular e E/t⁴→(a²+c²)/12 no limite bilateral perfurado. A ligação ao calor construído043 permanece restrita ao germe passado provado.

No caso variável, a identidade completa preserva Z_R(s)−sM(s). Mesmo com R=M, o drift Z_R(s)−sR(s) permanece; o controle afim calcula −v s²/2. A positividade do termo óptico não permite ignorar essa parcela.

O tensor simétrico B tem F=tr(B²)=θ²/2+2*opticalShearNormSq, invariante por rotação da tela. Essa convenção representa o setor sem torção; opticalShearNormSq é metade da norma trace-free. O sistema matricial conecta-se ao balanço integral no controle com traço Ricci constante. A orientação ΔS=−Q/T+eta*E requer T≠0.

{table_text}

Total051: {counts['theorems']}T/{counts['definitions']}D/{counts['instances']}I/{counts['axiom_prints']} prints. {len(data['steps'])}/{len(data['steps'])} etapas PASS. Zero avisos/erros, somente os três axiomas permitidos. Parecer completo: {link(REPORT)}. Revisão independente: {link(REVIEW)}.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

## Artefatos

{chr(10).join(rows)}

As dependências históricas pinadas foram verificadas e copiadas, sem recompilação nesta rodada. Imports externos diretos e companheiros foram medidos; não se afirma reconstrução transitiva integral de Mathlib. O parecer detalha o limite de proveniência dos fontes locais sem pin.

Auditoria selada, somente leitura:

    C:\\Python314\\python.exe -B "{ROOT / 'audit_continuation051.py'}"

CONTINUACAO051_MANIFESTO.json é emitido depois deste documento, evitando hash autorreferente. A nota de área é análise pendente e não se promove a prova por aparecer na custódia.

[OPEN] H3, seleção de geometria/área/temperatura e reconstrução gravitacional geral. Matching Ricci–matéria e evolução óptica são hipóteses; a interpretação física da correção não foi demonstrada. Nenhuma escrita fora de Chatgpt nesta rodada. NOT_FALSIFIED não é CONFIRMED.
"""
    new_bytes(DELIVERY, delivery.encode("utf-8"))
    print(json.dumps({"status": "REPORTS_CREATED", "report": str(REPORT),
        "report_bytes": REPORT.stat().st_size, "report_sha256": digest(REPORT),
        "delivery": str(DELIVERY), "delivery_bytes": DELIVERY.stat().st_size,
        "delivery_sha256": digest(DELIVERY)}, ensure_ascii=False))

if __name__ == "__main__":
    main()

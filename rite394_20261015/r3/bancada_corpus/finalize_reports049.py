"""Generate exclusive continuation049 report and tunnel delivery after independent review."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
BUILD=ROOT/"CONTINUACAO049_CLEAN_BUILD.json"
REVIEW=ROOT/"CONTINUACAO049_REVISAO_INDEPENDENTE.md"
REPORT=ROOT/"CONTINUACAO049_PARECER.md"
DELIVERY=ROOT/"TUNEL/DO_CHATGPT/ENTREGA_049_subespaco_padrao_continuo.md"
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def link(p,label=None):
    p=Path(p);return "["+(label or p.name)+"](<"+p.as_posix()+">)"
def new_bytes(p,raw):
    if p.exists() or not p.resolve().is_relative_to(ROOT) or not raw:raise RuntimeError("Nonexclusive output")
    tmp=p.with_name(p.name+".tmp")
    with tmp.open("xb") as f:f.write(raw);f.flush();os.fsync(f.fileno())
    if tmp.read_bytes()!=raw:raise RuntimeError("Temporary bytes mismatch")
    tmp.rename(p)
    if p.read_bytes()!=raw:raise RuntimeError("Final bytes mismatch")
def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if REPORT.exists() or DELIVERY.exists():raise RuntimeError("Report or delivery already exists")
    run=subprocess.run([sys.executable,"-B",str(ROOT/"audit_continuation049.py"),"--build-only"],
                        cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if run.returncode:raise RuntimeError(run.stdout.decode("utf-8",errors="replace"))
    audit=json.loads(run.stdout)
    if audit["status"]!="BUILD_PASS":raise RuntimeError("Build audit failed")
    data=json.loads(BUILD.read_text(encoding="utf-8"))
    review=REVIEW.read_text(encoding="utf-8")
    clean=Path(data["clean_directory"])
    if "BUILD_PASS" not in review or "Build SHA256: "+digest(BUILD) not in review or \
            "Diretório final: "+clean.as_posix() not in review:
        raise RuntimeError("Independent review not bound to this build")
    totals=data["totals"];timestamp=datetime.now(timezone.utc).isoformat()
    meanings={
      "BoundedGraphOperator":"Parametrização limitada do grafo, domínio denso, fechamento, adjunto maximal e positividade.",
      "ClosedAntilinearStandardSubspace":"FixS fechado real, separação, domínio como K+iK e subespaço padrão.",
      "ContinuousModularMultipliers":"Pesos explícitos, multiplicadores A/B, reflexão-conjugação J e identidades.",
      "BoundedGraphStandardSubspace":"S=JT, invariância do domínio, involução e construção do subespaço padrão.",
      "ContinuousModularDomain":"Grafo ae, domínio MemLp, ausência de autovetores e controle c=0.",
      "ContinuousModularStandardSubspace":"Instância concreta, JS=T, decomposição de Tomita e fórmula ae."}
    table=["| Módulo novo | Teoremas | Definições | Prints | Alcance |","|---|---:|---:|---:|---|"]
    for m in data["modules"]:
        i=data["source_info"][m]
        table.append(f"| {link(ROOT/(m+'.lean'))} | {i['theorems']} | {i['definitions']} | {i['axiom_prints']} | {meanings[m]} |")
    table="\n".join(table)
    report=f"""# Continuação049 — operador positivo auto-adjunto e subespaço padrão contínuo

[REAL — compilado e auditado na bancada] Emissão UTC: {timestamp}

Este lote constrói um modelo explícito em H=L²(ℝ,dξ;ℂ), com operador de Tomita de um subespaço real padrão. É um novo modelo nesta bancada, definido por multiplicadores; não foi demonstrado que ele seja a representação física selecionada pela torre anterior ou por ω(I)=1.

## Resultado e domínio efetivo

Para cada c real, T_c é o operador parcial cujo domínio e valor foram provados exatamente:

    D(T_c) = {{f ∈ L² : ξ ↦ exp(-cξ) f(ξ) pertence a L²}},
    (T_c f)(ξ) = exp(-cξ) f(ξ), quase em toda parte.

[REAL] T_c é positivo, auto-adjunto no sentido do adjunto de LinearPMap e fechado. A prova inclui densidade do domínio e igualdade maximal T_c*=T_c; não se limita à simetria do pareamento.

[REAL] Jf(ξ)=conj(f(-ξ)) é antiunitária involutiva. S_c=JT_c tem o mesmo domínio, é antilinear fechado, preserva esse domínio e satisfaz S_c²f=f nele. A fórmula concreta foi verificada quase em toda parte:

    (S_c f)(ξ) = exp(cξ) conj(f(-ξ)),
    J S_c f = T_c f.

[REAL] K_c=Fix(S_c) é um subespaço real fechado e padrão. A soma algébrica é exatamente D(T_c)=K_c+iK_c; seu fecho é H. O código não substitui essa soma algébrica por H. Na decomposição f=h+ik, S_c f=h-ik.

[REAL] Para c≠0, T_c f=z f implica f=0 para todo candidato z complexo. A prova usa que as fibras de exp(-cξ) têm medida zero. Ela não anuncia a classificação absolutamente contínua do espectro. O controle c=0 dá domínio inteiro, T_0=I e S_0=J.

## Como as hipóteses foram pagas

Os pesos positivos limitados a,b satisfazem a²+b²=1 e b=exp(-cξ)a. O fonte usa a expressão equivalente simétrica a=exp(cξ/2)/sqrt(exp(cξ)+exp(-cξ)), b=exp(-cξ/2)/sqrt(exp(cξ)+exp(-cξ)). As propriedades dos multiplicadores A=M_a e B=M_b são provadas, incluindo A injetivo, A/B auto-adjuntos, AB=BA e A²+B²=I.

O grafo de T é {{(Ah,Bh)}}. Sua caracterização Bx=Ay paga fechamento e maximalidade do adjunto: a recíproca recupera o parâmetro por h=Ax+By. A positividade vem do pareamento dos multiplicadores. Para S, o grafo é uma pré-imagem contínua do grafo de T; não se supõe uma isometria falsa para o produto usual de norma máximo.

[KNOWN] A passagem de involução antilinear fechada para seu subespaço real padrão é um resultado conhecido; este lote fornece sua formalização e uma instância explícita. Referência: [Brunetti–Guido–Longo, proposição 2.3, p.5](https://arxiv.org/pdf/math-ph/0203021). O artigo emprega dados de representação de Poincaré e relações modulares em sua construção geométrica; tais dados não são automaticamente importados para049.

## Verificação formal

{table}

Totais lidos do marcador: {totals['theorems']} teoremas, {totals['definitions']} definições, {totals['instances']} instâncias próprias, {totals['axiom_prints']} prints. Compilação serial de {len(data['steps'])} etapas, incluindo {data['integration_module']}. Zero erros/avisos. Cobertura exata de axiomas; apenas propext, Classical.choice e Quot.sound.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

{len(data['frozen_before'])} entradas congeladas coincidem antes/depois; {len(data['build_files'])} artefatos da compilação final. O auditor conferiu {audit['audited_files']} registros de evidência do build. Fontes/copias exatas, ambiente explícito e hash dos artefatos próprios preservados. A metadata por etapa vincula o snapshot global e registra a comparação feita pelo runner.

A fronteira externa mede os imports diretos Mathlib/stdlib e seus companheiros, executável e configurações. Não recompila Mathlib nem mede toda sua dependência transitiva. Nenhum olean histórico Chatgpt ou do kernel canônico entra na cadeia local destes seis módulos.

## O que continua aberto

[OPEN] Identificar formalmente T_c com Δ_c^(1/2), construindo e relacionando os operadores e seus domínios; provar o cálculo funcional que identifica as fases com Δ_c^(it); estabelecer a ação geométrica, a inclusão semilateral e Bisognano–Wichmann; construir a rede de álgebras/estado e sua relação com a torre.

[OPEN] Seleção física de c, região–álgebra, dimensão e assinatura físicas, protocolo/escala de área, H3 e reconstrução gravitacional geral. Ausência de autovetores elimina uma característica do modelo anterior, mas não demonstra por si a realização de Borchers ou a gravidade.

Os módulos anteriores e originais permanecem fora da escrita deste lote. canonical_gate_changed=false é uma declaração de escopo: este lote não escreve no gate canônico. Não é uma auditoria de alterações de terceiros no canônico. O resultado é matemático no modelo explicitado; não é confirmação física.

Revisão independente: {link(REVIEW)}.
"""
    new_bytes(REPORT,report.encode("utf-8"))
    artifacts=[REPORT,ROOT/"CONTINUACAO049_DERIVACAO_PREVIA.md",*sorted(ROOT.glob("DERIVACAO049_*.md")),
               *[ROOT/(m+".lean") for m in data["modules"]],REVIEW,ROOT/"clean_continuation049.py",
               ROOT/"audit_continuation049.py",BUILD,Path(__file__)]
    rows=["| Artefato | Bytes | SHA256 lido dos bytes |","|---|---:|---|"]
    for p in artifacts:rows.append(f"| {link(p)} | {p.stat().st_size} | {digest(p)} |")
    delivery=f"""# Entrega049 — subespaço padrão contínuo e positividade/auto-adjunticidade de JS

[REAL — build completo e revisão independente] Emissão UTC: {timestamp}

O lote constrói em Lebesgue L² um operador positivo auto-adjunto T_c=M_exp(-cξ), com domínio ponderado efetivo, uma antiunitária J e S_c=JT_c. Prova JS_c=T_c, involução/fechamento de S_c e StandardSubspace K_c=FixS_c. Para c≠0, T_c não tem autovetores não nulos; c=0 recupera T=I e S=J.

{table}

## Critérios conferidos

- Derivações registradas antes dos fontes correspondentes; correções dos arquivos novos têm backups de bytes preservados.
- Seis módulos novos; {totals['theorems']} teoremas, {totals['definitions']} definições, {totals['instances']} instâncias próprias, {totals['axiom_prints']} prints. Importador conjunto incluído; {len(data['steps'])}/{len(data['steps'])} etapas passaram.
- Nenhum sorry/admit/axioma adicional; apenas o trio permitido. Zero avisos/erros e nenhuma instância própria anônima.
- Pasta de compilação exclusiva, fontes copiados por bytes e congelados; ambiente sem fallback ao kernel ou oleans locais históricos.
- Revisão independente vinculada ao hash do marcador e ao diretório final, com auditor BUILD_PASS.
- Relatório declara a fronteira externa de imports diretos e companheiros. Não se afirma reconstrução de todo o Mathlib nem sua cadeia transitiva.
- Escrita deste lote restrita à pasta Chatgpt. Nenhuma incorporação em um.py, kernel, Atlas, índice, memórias canônicas ou gate.

Parecer e alcance: {link(REPORT)}. Revisão: {link(REVIEW)}.

Diretório final: {clean.as_posix()}

Build SHA256: {digest(BUILD)}

## Estatuto e próximo vínculo necessário

[OPEN] A identificação formal T_c=Δ_c^(1/2) e das fases com Δ_c^(it) ainda exige a construção correspondente. O lote não estabelece BW, inclusão semilateral, rede física, H3 nem uma derivação desta representação a partir da torre. O nome continuousModularOperator não substitui essas provas.

## Artefatos

{chr(10).join(rows)}

Auditoria selada, somente leitura:

    C:\\Python314\\python.exe -B "{ROOT / 'audit_continuation049.py'}"

CONTINUACAO049_MANIFESTO.json será emitido após esta entrega para evitar hash autorreferente; o comando verifica o selo quando presente. Os números acima vêm do build auditado, não de contagem estimada.

H3: OPEN. Reconstrução gravitacional geral: OPEN. Meta ampla de gravidade quântica: OPEN. Gate canônico intocado por este lote. NOT_FALSIFIED não é CONFIRMED.

Somente o operador decide a incorporação ao acervo canônico e a confirmação física; esta entrega não realiza esses atos.
"""
    new_bytes(DELIVERY,delivery.encode("utf-8"))
    print(json.dumps({"status":"REPORTS_CREATED","report":str(REPORT),"report_bytes":REPORT.stat().st_size,
                      "report_sha256":digest(REPORT),"delivery":str(DELIVERY),"delivery_bytes":DELIVERY.stat().st_size,
                      "delivery_sha256":digest(DELIVERY)},ensure_ascii=False))
if __name__=="__main__":main()

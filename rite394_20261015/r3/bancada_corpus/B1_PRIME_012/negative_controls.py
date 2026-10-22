from support import *
import concurrent.futures, re, subprocess, sys
K=ROOT/"kernel"
A=ROOT/"semantic_controls"/stamp();A.mkdir(parents=True)
head="import TGLExt.ActionCouplingControls\nset_option autoImplicit false\nopen TGLExt TGLExt.ActionCouplingControls\n"
common="{X : Type*} (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ) (hEOM : D.EOM c psi)"
cases=[
("ChangedBeta", f"example {common} (b : ℝ) : D.fieldOperator psi = b • D.K_boundary psi := by\n  exact hEOM\n", "TGLExt.ActionCouplingData.eom_rejects_changed_coefficient", "b distinto de beta e K(Psi) nao nulo impedem a troca."),
("FlippedSign", f"example {common} : D.fieldOperator psi = (-c.beta) • D.K_boundary psi := by\n  exact hEOM\n", "TGLExt.ActionCouplingControls.reject_sign_flip", "beta positivo e K(Psi) nao nulo tornam o sinal oposto distinto."),
("XiAsBeta", f"example {common} : D.fieldOperator psi = D.xi • D.K_boundary psi := by\n  exact hEOM\n", "TGLExt.ActionCouplingControls.reject_xi_as_beta", "xi e campo independente; se xi!=beta e fonte nao nula, troca refutada."),
("BareAlpha", f"example {common} : D.fieldOperator psi = c.alpha • D.K_boundary psi := by\n  exact hEOM\n", "TGLExt.ActionCouplingControls.reject_bare_alpha", "normalizacao do custo nao pode ser descartada."),
("ChangedGenerator", f"example {common} (K : (X → ℂ) →ₗ[ℝ] (X → ℂ)) : D.fieldOperator psi = c.beta • K psi := by\n  exact hEOM\n", "TGLExt.ActionCouplingData.eom_rejects_changed_generator", "K(Psi) diferente nao pode ser substituido sob beta nao nulo."),
("MissingCurvature", f"example {common} : D.boxOperator psi - D.mass^2 • psi = D.modularSource c psi := by\n  exact hEOM\n", "TGLExt.ActionCouplingData.eom_rejects_missing_curvature", "o termo conforme avaliado nao nulo impede sua omissao."),
("NoEOMInput", "example (c : TGLCoupling) (xi : ℝ) : (scalarModel xi (-c.beta)).EOM c unitSection := by\n  exact scalar_model_eom c xi\n", "TGLExt.ActionCouplingControls.data_alone_does_not_supply_eom", "modelo com ganho -beta satisfaz o tipo dos dados mas refuta EOM."),
("XiFixed", "example (c : TGLCoupling) (xi : ℝ) : (scalarModel xi c.beta).xi = (1/6 : ℝ) := by\n  exact (nonzero_model_for_every_xi c xi).1\n", "TGLExt.ActionCouplingControls.xi_is_not_selected", "EOM admite qualquer xi no modelo algebrico nao nulo; 1/6 nao e derivado."),
("NoNonzeroSource", "example {X : Type*} (D : ActionCouplingData X) (c : TGLCoupling) (psi : X → ℂ) (hK : D.K_boundary psi = 0) : (-c.beta) = c.beta := by\n  exact D.zero_source_hides_coefficient c psi hK (-c.beta)\n", "TGLExt.ActionCouplingControls.zero_source_not_unique", "fonte zero admite coeficientes distintos; igualdade de fontes nao identifica beta."),
]
def run(case):
    name,body,wall,reason=case;path=A/("Bad"+name+".lean");atomic(path,head+body)
    cmd=[str(BIN/"lake.exe"),"env","lean",str(path)]
    p=subprocess.run(cmd,cwd=K,env=clean_env(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    atomic(A/(name+".stdout.txt"),p.stdout);atomic(A/(name+".stderr.txt"),p.stderr)
    out=(p.stdout+p.stderr).decode("utf-8",errors="replace")
    syntax_or_env=bool(re.search(r"unexpected token|unknown (?:identifier|constant|namespace|module)|object file .* does not exist|failed to|application type mismatch",out,re.I))
    semantic=(p.returncode!=0 and "Type mismatch" in out and not syntax_or_env)
    return dict(name=name,source=str(path),sha256=digest(path),command=cmd,returncode=p.returncode,diagnostic=out,semantic_type_rejection=semantic,proved_wall=wall,reason=reason)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: rows=list(pool.map(run,cases))
record(A/"RESULTADOS.json",dict(kind="AUTHOR_NEGATIVE_CONTROLS",all_semantic=all(r["semantic_type_rejection"] for r in rows),controls=rows))
for r in rows:print(r["name"],r["returncode"],r["semantic_type_rejection"],flush=True)
print(str(A),flush=True)
sys.exit(0 if all(r["semantic_type_rejection"] for r in rows) else 1)

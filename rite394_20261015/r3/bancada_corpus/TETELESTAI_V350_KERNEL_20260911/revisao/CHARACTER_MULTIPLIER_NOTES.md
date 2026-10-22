# Multiplicador de caracteres em L² — evidência da subtarefa

[REAL — Lean, bancada local] Fonte compilada com exit 0: `kernel/TGLV350/L2CharacterMultiplier.lean`.
Namespace: `TGLV350.Regular`. Importações: `TGLV350.L2OperatorLift` e `TGLV350.L2Translation`.
Hipóteses de H: `H : Type`, `NormedAddCommGroup H`, `InnerProductSpace ℂ H`, `CompleteSpace H`.
Espaço: `RegularHilbert H = MeasureTheory.Lp H 2 (volume : Measure ℝ)`.

[REAL — enunciados compilados] Escreva `D_s = characterMultiplier s` e `S_t = shift t`.
A convenção é `(S_t f)(x) = f(x-t)` quase em toda parte.

| Declaração | Conteúdo |
|---|---|
| `characterMultiplierIsometry` | Aplicação linear isométrica, construída a partir do produto mensurável e de sua norma pontual. |
| `characterMultiplier_ae` | `(D_s f)(x) = exp(-i*s*x) • f(x)` quase em toda parte. |
| `characterMultiplier_norm` | `‖D_s f‖ = ‖f‖`. |
| `characterMultiplier_zero` | `D_0 = 1`. |
| `characterMultiplier_mul` | `D_s * D_t = D_(s+t)`. |
| `characterMultiplier_inverse` | `D_s (D_(-s) f) = f`. |
| `characterMultiplier_star` | `star D_s = D_(-s)`; star é o adjunto de operador. |
| `characterMultiplier_unitary` | `(star D_s) * D_s = 1` e `D_s * (star D_s) = 1`. |
| `characterMultiplier_commutes_fibre` | `D_s * fibre T = fibre T * D_s`. |
| `characterMultiplier_weyl` | `D_s * S_t * (star D_s) = exp(-i*s*t) • S_t`. |
| `characterMultiplier_inner_continuous` | Para f e t fixos, `s ↦ inner ℂ (D_s f) (D_t f)` é contínua. |
| `characterMultiplier_strongly_continuous` | Para todo f em L², `s ↦ D_s f` é contínua na topologia usual de ℝ e na norma de L². |

A integrabilidade do produto vem de `‖exp(-i*s*x) • f(x)‖ = ‖f(x)‖`.
A relação de Weyl transporta a igualdade quase em toda parte por `x ↦ x-t`, usando preservação de Lebesgue.
O cálculo escalar que fixa o sinal é `exp(-i*s*x) * exp(i*s*(x-t)) = exp(-i*s*t)`.
A continuidade dos coeficientes usa convergência dominada com majorante integrável `‖f(x)‖²`.
A identidade do quadrado da norma da diferença e a continuidade da raiz quadrada fornecem continuidade forte.
Não há hipótese de continuidade em norma de operador, discretização de ℝ ou premissa que apenas afirme a conclusão.

[REAL — compilação e auditoria]

- Compilador: `Lean (version 4.31.0, x86_64-w64-windows-gnu, commit 68218e876d2a38b1985b8590fff244a83c321783, Release)`.
- Comando: `C:\Python314\python.exe compile_lean.py TGLV350/L2CharacterMultiplier.lean`, na raiz da bancada.
- Registro de compilação: `logs/L2CharacterMultiplier_20260911_211052_312422.json`.
- Stdout: `logs/L2CharacterMultiplier_20260911_211052_312422.stdout.txt`.
- Stderr: vazio; exit 0; nenhum erro ou aviso no stdout final.
- Auditoria complementar: `logs/L2CharacterMultiplier_FINAL_AUDIT_20260911_211307_521155.json`.
- 24/24 declarações auditadas por `#print axioms`; todos os axiomas pertencem a `{propext, Classical.choice, Quot.sound}`.
- Nenhuma ocorrência de `sorry`, `axiom` ou `admit` na fonte.
- SHA-256 da fonte: `de33feb2aa4356a0897a4079367a1c29728bb49f2c391b21bd0cf993d81f507b`.
- SHA-256 do .olean: `36f35aa2411802d1c945037c917f75fc43832c71cb2b03fe590d06219a77d6b4`.
- Os hashes atuais da fonte e do .olean coincidem com o registro final; as fontes dos dois módulos importados coincidem com seus registros de compilação exit 0.

As tentativas anteriores com falha permanecem nos logs; não constituem evidência de aprovação.
Esta subtarefa escreveu apenas sua fonte, seu .olean, seus logs/auditoria e esta nota.

[OPEN — fora desta subtarefa] Restrição de `Ad(D_s)` à álgebra gerada, ação dual no produto cruzado,
traço canônico, integração nas raízes e revisão independente permanecem com a tarefa principal e o revisor.
Este módulo entrega os operadores implementadores e suas relações; não certifica um core completo,
QG ou alteração de gate. Nenhuma memória, Atlas, raiz ou original externo foi editado por esta subtarefa.

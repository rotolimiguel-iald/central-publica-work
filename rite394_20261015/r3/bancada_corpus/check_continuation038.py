"""Read-only numerical diagnostic for the analytic note038; not a proof."""
from decimal import Decimal, localcontext
import json

D = Decimal

def sin_decimal(x):
    term = total = x
    n = 1
    while True:
        term *= -x*x / D((2*n)*(2*n+1))
        previous = total
        total += term
        if total == previous:
            return total
        n += 1
        if n > 10000:
            raise ArithmeticError("sine series did not converge")

def cos_decimal(x):
    term = total = D(1)
    n = 1
    while True:
        term *= -x*x / D((2*n-1)*(2*n))
        previous = total
        total += term
        if total == previous:
            return total
        n += 1
        if n > 10000:
            raise ArithmeticError("cosine series did not converge")

def calculate(precision):
    with localcontext() as ctx:
        ctx.prec = precision
        ell = D(2).ln()
        r = ell / 12
        target = r*r/12-D(15)*r/32
        rows = []
        previous_error = None
        for exponent in (1,2,3,4):
            t = D(10) ** (-exponent)
            h = t*t/(1+t*t)
            ell0 = (1-h/8).ln()
            ell1 = (1+h/16).ln()
            norm = max(abs(2*sin_decimal(ell0/2)),
                       abs(2*sin_decimal(ell1/2)))
            candidate = ell*norm/3
            area = cos_decimal((r/2).sqrt()*t)**2
            quotient = (candidate-(1-area))/t**4
            error = abs(quotient-target)
            if quotient >= 0:
                raise AssertionError("negative defect was not reproduced")
            if previous_error is not None and error >= previous_error:
                raise AssertionError("quotient errors are not decreasing")
            rows.append({"t":str(t),"quartic_quotient":str(quotient),
                         "absolute_error":str(error)})
            previous_error = error
        if previous_error >= D("1e-8"):
            raise AssertionError("last quotient is too far from target")
        return {"precision":precision, "target":str(target), "rows":rows}

if __name__ == "__main__":
    low, high = calculate(70), calculate(100)
    with localcontext() as ctx:
        ctx.prec = 110
        gaps = [abs(D(a["quartic_quotient"])-D(b["quartic_quotient"]))
                for a,b in zip(low["rows"],high["rows"],strict=True)]
        if max(gaps) >= D("1e-48"):
            raise AssertionError("two precision runs disagree")
    print(json.dumps({"status":"PASS", "scope":"numeric diagnostic, not formal proof",
        "new_lean_theorems":0,"maximum_precision_gap":str(max(gaps)),
        "runs":[low,high]}, indent=2))

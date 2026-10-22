"""Pure, bounded F9 precision candidates. Prepared, not numerically qualified.

No I/O, Gaussian backend, NumPy, SciPy or cosmological solver. Receipt errors
are local engineering estimates, never certified bounds or physical evidence.
"""
import heapq
import math
from fractions import Fraction

LOG_SERVICE_ID = 'f9.log_exp_quad_interval.scaled_simpson.v1'
QUAD_SERVICE_ID = 'f9.positive_quad_1d.adaptive_simpson.v1'
_EPS = 2.0 ** -52


class PrecisionServiceError(ValueError):
    def __init__(self, code, detail, evaluations=None):
        self.code, self.detail, self.evaluations = code, detail, evaluations
        super().__init__(f'{code}: {detail}; evaluations={evaluations}')


def _need(ok, code, detail, evaluations=None):
    if not ok:
        raise PrecisionServiceError(code, detail, evaluations)


def _number(value, name):
    _need(type(value) in (int, float), 'INVALID_NUMBER', name)
    try:
        value = float(value)
    except (ValueError, OverflowError) as exc:
        raise PrecisionServiceError('INVALID_NUMBER', name) from exc
    _need(math.isfinite(value), 'NONFINITE_NUMBER', name)
    return value


def _budget(value):
    _need(type(value) is int and 1 <= value <= 1000000, 'INVALID_BUDGET', 'integer1..1000000')
    return value


def _target(value, name):
    value = _number(value, name)
    _need(value > 0, 'INVALID_TARGET', name)
    return value


def _finite_sum(values, label, evaluations=None):
    try:
        answer = math.fsum(values)
    except (ValueError, OverflowError) as exc:
        raise PrecisionServiceError('ARITHMETIC_RANGE', label, evaluations) from exc
    _need(math.isfinite(answer), 'ARITHMETIC_RANGE', label, evaluations)
    return answer


class _Samples:
    def __init__(self, callback, maximum):
        self.callback, self.maximum, self.count, self.cache = callback, maximum, 0, {}

    def at(self, x):
        _need(0 <= x <= 1 and math.isfinite(x), 'NODE_OUTSIDE_DOMAIN', 'unit interval', self.count)
        if x in self.cache:
            return self.cache[x]
        _need(self.count < self.maximum, 'BUDGET_EXCEEDED', 'callback cap', self.count)
        self.count += 1
        # Callback exceptions propagate unchanged; no catch/retry or replacement value.
        value = self.callback(x)
        _need(type(value) in (int, float), 'INVALID_CALLBACK_VALUE', 'built-in real required', self.count)
        try:
            value = float(value)
        except (ValueError, OverflowError) as exc:
            raise PrecisionServiceError('INVALID_CALLBACK_VALUE', 'conversion', self.count) from exc
        _need(math.isfinite(value) and value >= 0, 'INVALID_CALLBACK_VALUE', 'finite nonnegative', self.count)
        self.cache[x] = value
        return value


def _grid(a, b):
    mid = a + (b-a)/2
    return (a, a+(mid-a)/2, mid, mid+(b-mid)/2, b)


def _weighted_area(width, values, weights):
    scale = max(values)
    if scale == 0:
        return 0.0
    average = math.fsum(w*(v/scale) for v,w in zip(values, weights)) / sum(weights)
    result = (width*scale)*average
    _need(math.isfinite(result) and result >= 0, 'AREA_RANGE', 'positive Simpson rule')
    return result


def _panel(samples, a, b):
    xs = _grid(a,b)
    _need(all(x<y for x,y in zip(xs,xs[1:])), 'FLOAT_GRID_RESOLUTION', 'distinct nodes', samples.count)
    values = [samples.at(x) for x in xs]
    coarse = _weighted_area(b-a, (values[0],values[2],values[4]), (1,4,1))
    fine = _weighted_area(b-a, values, (1,4,2,4,1))
    # Richardson estimate assumes the smooth asymptotic h^4 regime, not proved here.
    err = abs(fine-coarse)/15 + (64*_EPS)*fine + 4*math.ulp(fine)
    _need(math.isfinite(err), 'ERROR_ESTIMATE_RANGE', 'local Simpson estimate', samples.count)
    return (a,b,fine,err)


def _totals(heap, count):
    area = _finite_sum((entry[2][2] for entry in heap), 'leaf area sum', count)
    error = _finite_sum((entry[2][3] for entry in heap), 'leaf error sum', count)
    error = _finite_sum((error, (16*_EPS)*area, 4*math.ulp(area)), 'summation error allowance', count)
    return area,error


def _meets(error, area, absolute, relative):
    # Avoid overflowing relative*area for a large but finite requested target.
    return error <= absolute or (area > 0 and error/area <= relative)


def _adaptive(callback, maximum, absolute, relative, initial_panels):
    # Initial and refinement costs are known before starting a batch of callbacks.
    _need(maximum >= 4*initial_panels+1, 'INSUFFICIENT_BUDGET', f'need at least {4*initial_panels+1} nodes')
    samples, leaves, serial = _Samples(callback,maximum), [], 0
    for i in range(initial_panels):
        node = _panel(samples,i/initial_panels,(i+1)/initial_panels)
        heapq.heappush(leaves,(-node[3],serial,node));serial += 1
    _need(any(v>0 for v in samples.cache.values()), 'NO_POSITIVE_SAMPLED_MASS',
          'zero nodes do not establish zero integral or rule out a missed peak', samples.count)
    area,error = _totals(leaves,samples.count)
    stop = 'BUDGET_EXHAUSTED'
    while True:
        # max(abs,rel*area) is the stated local stopping convention, not both goals.
        if _meets(error,area,absolute,relative):
            area,error = _totals(leaves,samples.count)
            if _meets(error,area,absolute,relative):
                stop = 'ESTIMATED_TARGET_REACHED'
                break
        if samples.maximum-samples.count < 4:
            break
        a,b,parent_area,parent_error = leaves[0][2]
        mid = a+(b-a)/2
        if not all(x<y for interval in ((a,mid),(mid,b))
                   for x,y in zip(_grid(*interval),_grid(*interval)[1:])):
            stop = 'FLOAT_GRID_RESOLUTION'
            break
        left,right = _panel(samples,a,mid),_panel(samples,mid,b)
        heapq.heappop(leaves)
        for node in (left,right):
            heapq.heappush(leaves,(-node[3],serial,node));serial += 1
        area = _finite_sum((area,-parent_area,left[2],right[2]), 'running area', samples.count)
        error = _finite_sum((error,-parent_error,left[3],right[3]), 'running error', samples.count)
        if area <= 0 or error < 0:
            area,error = _totals(leaves,samples.count)
    area,error = _totals(leaves,samples.count)
    _need(area > 0, 'AREA_ZERO_OR_UNDERFLOW', 'positive target not representable as positive area', samples.count)
    converged = stop == 'ESTIMATED_TARGET_REACHED' and _meets(error,area,absolute,relative)
    return area,error,converged,samples.count,stop,len(leaves)


def positive_quad_1d(f, lower, upper, *, absolute_error_target,
                     relative_error_target, max_evaluations):
    """Integrate the injected positive scaled H5 callback on the full [0,1]."""
    lower,upper = _number(lower,'lower'),_number(upper,'upper')
    _need(lower==0 and upper==1, 'DOMAIN_ERROR', 'exact service domain [0,1]')
    _need(callable(f), 'CALLBACK_ERROR', 'callable required')
    absolute = _target(absolute_error_target,'absolute_error_target')
    relative = _target(relative_error_target,'relative_error_target')
    maximum = _budget(max_evaluations)
    area,error,converged,count,stop,leaves = _adaptive(f,maximum,absolute,relative,4)
    return {'service_id':QUAD_SERVICE_ID,'status':'ENGINEERING_ESTIMATE','value':area,
        'error_estimate':error,'error_kind':'ESTIMATED_NOT_CERTIFIED','converged':converged,
        'evaluations':count,'method':f'positive_simpson_4_initial_panels; local_h4_estimate_only; '
            f'missed_peaks_unbounded; stop={stop}; leaves={leaves}'}


def _pow2(k):
    return Fraction(1<<k) if k>=0 else Fraction(1,1<<(-k))


def _log_fraction(value):
    _need(value>0, 'LOG_DOMAIN', 'positive rational')
    # Rational normalization prevents under/overflow of the original ratio.
    exponent = value.numerator.bit_length()-value.denominator.bit_length()
    mantissa = float(value/_pow2(exponent))
    a,b = math.log(mantissa),exponent*math.log(2.0)
    result = _finite_sum((a,b),'rational logarithm')
    return result,(32*_EPS)*(abs(a)+abs(b)+1)


def _curvature_scale(a):
    exponent = a.numerator.bit_length()-a.denominator.bit_length()
    scale = _pow2(-(exponent//2))
    # At most a few adjustments from this bit-length estimate; exact rational tests.
    while a*scale*scale>1:
        scale /= 2
    while a*(2*scale)*(2*scale)<=1:
        scale *= 2
    return scale


def _side_geometry(a, slope, distance, log_goal):
    _need(distance>0 and slope>=0, 'SIDE_GEOMETRY', 'positive distance/nonnegative decay')
    scale = min(distance,_curvature_scale(a))
    if slope>0:
        scale = min(scale,1/slope)
    b,c = slope*scale,a*scale*scale/2
    endpoint = distance/scale
    _need(0<=b<=1 and 0<c<=Fraction(1,2) and endpoint>=1, 'SCALING_ERROR', 'bounded coefficients')
    cut = Fraction(1)
    log_tail = None
    for _ in range(16):
        if cut>=endpoint:
            cut,log_tail = endpoint,None
            break
        derivative = b+2*c*cut
        log_derivative,_ = _log_fraction(derivative)
        log_tail = -float(b*cut+c*cut*cut)-log_derivative
        # Integral0^1 exp(-bt-ct^2)dt >= exp(-3/2).
        if log_tail <= log_goal-1.5:
            break
        cut = min(2*cut,endpoint)
    else:
        raise PrecisionServiceError('LOCALIZATION_LIMIT','finite tail localization not reached')
    return scale,b,c,cut,log_tail


def log_exp_quad_interval(A,h,L,U, *, absolute_log_error_target,max_evaluations):
    """Estimate log integral exp(h*z-A*z*z/2), including both finite sides."""
    A,h,L,U = (_number(v,n) for v,n in ((A,'A'),(h,'h'),(L,'L'),(U,'U')))
    _need(A>0 and L<U and L<=0<=U, 'DOMAIN_ERROR','A>0; L<U; zero in interval')
    target,maximum = _target(absolute_log_error_target,'absolute_log_error_target'),_budget(max_evaluations)
    a,hf,lo,hi = map(Fraction,(A,h,L,U))
    peak = min(hi,max(lo,hf/a))
    height = hf*peak-a*peak*peak/2
    slope = hf-a*peak
    sides=[]
    if lo<peak:
        sides.append((slope,peak-lo))
    if peak<hi:
        sides.append((-slope,hi-peak))
    _need(maximum>=5*len(sides), 'INSUFFICIENT_BUDGET', 'five initial nodes per nonempty side')
    try:
        height_float = float(height)
    except OverflowError as exc:
        raise PrecisionServiceError('LOG_VALUE_RANGE','peak height outside float range') from exc
    _need(math.isfinite(height_float), 'LOG_VALUE_RANGE','peak height')
    log_goal = math.log(min(target,0.25))-math.log(32.0)
    relative_goal = max(math.nextafter(0.0,1.0),min(target/32,0.01))
    side_logs,side_errors,diagnostics = [],[],[]
    total_count,all_converged = 0,True
    for index,(decay,distance) in enumerate(sides):
        scale,b,c,cut,log_tail = _side_geometry(a,decay,distance,log_goal)
        bf,cf,rf = float(b),float(c),float(cut)
        _need(all(math.isfinite(v) for v in (bf,cf,rf)) and rf>=1, 'SCALING_RANGE','side coefficients')
        def integrand(u):
            t = rf if u==1 else rf*u
            return math.exp(-(bf*t+cf*t*t))
        allocation = (maximum-total_count)//(len(sides)-index)
        area,error,converged,count,stop,leaves = _adaptive(integrand,allocation,0.0,relative_goal,1)
        total_count += count
        log_scale,scale_error = _log_fraction(scale)
        log_cut,cut_error = _log_fraction(cut)
        log_area = math.log(area)
        log_side = _finite_sum((log_scale,log_cut,log_area),'side logarithm',total_count)
        relative_estimate = error/area
        tail_relative = 0.0
        if log_tail is not None:
            # This is an analytic tail envelope in real arithmetic, evaluated as
            # floats here. Underflow is retained as minimum positive allowance.
            tail_relative = max(math.nextafter(0.0,1.0),math.exp(log_tail-log_cut-log_area))
        relative_estimate = _finite_sum((relative_estimate,tail_relative),'side relative error',total_count)
        rounding = _finite_sum((scale_error,cut_error,
            (64*_EPS)*(1+abs(bf*rf)+abs(cf*rf*rf)+abs(log_area))), 'side rounding allowance', total_count)
        assessed = math.isfinite(relative_estimate) and relative_estimate<1
        log_error = -math.log1p(-relative_estimate)+rounding if assessed else None
        side_logs.append(log_side);side_errors.append(log_error)
        all_converged = all_converged and converged and assessed
        diagnostics.append(f'side{index}:cut={rf!r},tail_log_bound={log_tail!r},stop={stop},leaves={leaves}')
    top = max(side_logs)
    log_sum = top+math.log(math.fsum(math.exp(v-top) for v in side_logs))
    result = _finite_sum((height_float,log_sum),'combined window logarithm',total_count)
    _need(total_count<=maximum, 'BUDGET_EXCEEDED','combined side budget',total_count)
    assessed = all(e is not None for e in side_errors)
    estimate = None
    if assessed:
        estimate = _finite_sum((max(side_errors),8*math.ulp(height_float),
            (64*_EPS)*abs(height_float)+(64*_EPS)*abs(log_sum)+(64*_EPS)*abs(result)+64*_EPS), 'window log error estimate', total_count)
    return {'service_id':LOG_SERVICE_ID,'status':'ENGINEERING_ESTIMATE','log_value':result,
        'error_estimate':estimate,'error_kind':'ESTIMATED_NOT_CERTIFIED' if assessed else 'UNASSESSED',
        'converged':bool(all_converged and assessed and estimate<=target),'evaluations':total_count,
        'method':'exact_float_rational_recenter; monotone_side_scaling; bounded_simpson; '
            'finite_window_tail_accounted_not_certified; '+'; '.join(diagnostics)}

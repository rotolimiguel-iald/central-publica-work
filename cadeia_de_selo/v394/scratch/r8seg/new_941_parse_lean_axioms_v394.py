def parse_lean_axioms_v394(text):
    """Preserve Unicode/quoted names and reject conflicting duplicate reports."""
    result, errors = {}, []
    pattern = re.compile(r"^'([^\n]+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", re.M)
    for match in pattern.finditer(text):
        name = match[1]
        axioms = [a.strip() for a in (match[2] or '').replace('\n', ' ').split(',') if a.strip()]
        if name in result and set(result[name]) != set(axioms):
            errors.append('CONFLICTING_AXIOM_REPORT:' + name)
        else:
            result[name] = axioms
    if not result:
        errors.append('EMPTY_AXIOM_REPORT')
    return {'axioms': result, 'errors': errors, 'ok': not errors}
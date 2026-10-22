def parse_lean_provenance_v394(text):
    """Parse compiler rows; malformed/duplicate metadata is a visible failure."""
    result, errors = {}, []
    for line in text.splitlines():
        if not line.startswith('TGL_DECL_SOURCE'):
            continue
        parts = line.split('\t')
        if len(parts) != 3 or parts[0] != 'TGL_DECL_SOURCE':
            errors.append('MALFORMED_DECLARATION_SOURCE')
            continue
        _, name, module = parts
        if not name or not re.fullmatch(r'TGL(?:Ext)?(?:\.[A-Za-z0-9_]+)*', module):
            errors.append('INVALID_DECLARATION_SOURCE:' + name)
            continue
        if name in result:
            errors.append('DUPLICATE_DECLARATION_SOURCE:' + name)
            continue
        result[name] = module.replace('.', '/') + '.lean'
    if not result:
        errors.append('EMPTY_DECLARATION_PROVENANCE')
    return {'sources': result, 'errors': errors, 'ok': not errors}
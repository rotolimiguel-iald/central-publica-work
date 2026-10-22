"""Lossless grouping of generated whole-field source references, not source prose.

{a:{'@':'/a'},b:{'@':'/b'}} <=> {'@SOURCE_FIELDS':['a','b']}.
Nested metadata with retained fields/counts/statuses is never grouped wholesale.
"""
KEY='@SOURCE_FIELDS'
def pack(value):
    if isinstance(value,list):return [pack(v) for v in value]
    if not isinstance(value,dict):return value
    if KEY in value:raise ValueError('Reserved metadata key already present')
    mapped={k:pack(v) for k,v in value.items()}
    eligible=[k for k,v in mapped.items() if isinstance(k,str) and k and
              '/' not in k and '~' not in k and not k.startswith('@') and
              isinstance(v,dict) and v=={'@':'/'+k}]
    if len(eligible)<2:return mapped
    result={k:v for k,v in mapped.items() if k not in eligible}
    result[KEY]=eligible
    return result

def unpack(value):
    if isinstance(value,list):return [unpack(v) for v in value]
    if not isinstance(value,dict):return value
    result={k:unpack(v) for k,v in value.items() if k!=KEY}
    if KEY not in value:return result
    names=value[KEY]
    if not isinstance(names,list) or len(names)<2:
        raise ValueError('Invalid grouped references')
    if any(not isinstance(k,str) or not k or '/' in k or '~' in k or k.startswith('@') for k in names):
        raise ValueError('Invalid source-field name')
    if len(names)!=len(set(names)) or any(k in result for k in names):
        raise ValueError('Duplicate or conflicting source-field reference')
    result.update({k:{'@':'/'+k} for k in names})
    return result

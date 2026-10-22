"""Reversible grouping of source references that carry only an item count.

{a:{'@':'/a','items':3},b:{'@':'/b','items':4}}
  <=> {'@SOURCE_ITEMS':{'a':3,'b':4}}.
Counts remain document item counts, never numbers of mathematical proofs.
"""
KEY='@SOURCE_ITEMS'
def valid_name(k):
    return isinstance(k,str) and bool(k) and '/' not in k and '~' not in k and not k.startswith('@')
def pack_items(value):
    if isinstance(value,list):return [pack_items(v) for v in value]
    if not isinstance(value,dict):return value
    if KEY in value:raise ValueError('Reserved count key already present')
    mapped={k:pack_items(v) for k,v in value.items()}
    eligible={k:v['items'] for k,v in mapped.items() if valid_name(k) and
              isinstance(v,dict) and set(v)=={'@','items'} and
              v['@']=='/'+k and type(v['items']) is int and v['items']>=0}
    if len(eligible)<2:return mapped
    result={k:v for k,v in mapped.items() if k not in eligible}
    result[KEY]=eligible
    return result
def unpack_items(value):
    if isinstance(value,list):return [unpack_items(v) for v in value]
    if not isinstance(value,dict):return value
    result={k:unpack_items(v) for k,v in value.items() if k!=KEY}
    if KEY not in value:return result
    fields=value[KEY]
    if not isinstance(fields,dict) or len(fields)<2:
        raise ValueError('Invalid grouped item counts')
    for k,n in fields.items():
        if not valid_name(k) or type(n)is not int or n<0 or k in result:
            raise ValueError('Invalid or conflicting item count')
        result[k]={'@':'/'+k,'items':n}
    return result

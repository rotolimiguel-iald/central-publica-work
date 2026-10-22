"""Shift internal anchors around one reviewed replacement, without guessed offsets."""
from copy import deepcopy


def remap_interval(node, *, old_exposition, new_exposition, start, old_length,
                   replacement, summary_id, summary_span, source_pointer):
    end = start + old_length
    if old_exposition[:start] + replacement + old_exposition[end:] != new_exposition:
        raise ValueError('Unexpected changes outside replacement')
    delta = len(replacement) - old_length
    sa, sn = summary_span
    if not (start <= sa < sa + sn <= start + len(replacement)):
        raise ValueError('Summary span escapes reviewed replacement')
    label = '**Estatutos ['+summary_id+']**'
    if label in old_exposition or new_exposition.count(label) != 1:
        raise ValueError('Summary label is not a unique new anchor')
    if not new_exposition[sa:sa+sn].startswith(label):
        raise ValueError('Summary label does not match reviewed replacement')
    changes = []

    def visit(value, path):
        if isinstance(value, list):
            return [visit(v, path+'/'+str(i)) for i,v in enumerate(value)]
        if not isinstance(value, dict):
            return value
        if '@EXPOSITION' not in value and '@SUMMARY' not in value:
            if '@' in value and 'fields' in value:
                result = deepcopy(value)
                result['fields'] = {k:visit(v,source_pointer+value['@']+k)
                                    for k,v in value['fields'].items()}
                return result
            return {k:visit(v,path+'/'+k.replace('~','~0').replace('/','~1'))
                    for k,v in value.items()}
        a,n = value['span']
        if any(type(x) is not int for x in (a,n)) or not 0<=a<a+n<=len(old_exposition):
            raise ValueError('Invalid original reference span')
        old_fragment = old_exposition[a:a+n]
        expected = (value['starts_with'] if '@EXPOSITION' in value else
                    '**Estatutos ['+value['@SUMMARY']+']**')
        if not old_fragment.startswith(expected):
            raise ValueError('Stale original reference')
        result = deepcopy(value)
        if a+n <= start:
            pass
        elif a >= end:
            result['span'] = [a+delta,n]
        elif start <= a and a+n <= end:
            if '@SUMMARY' in value:
                raise ValueError('Cannot replace an existing reviewed summary implicitly')
            occurrences = new_exposition.count(old_fragment)
            if occurrences == 1:
                result['span'] = [new_exposition.index(old_fragment),n]
            elif occurrences:
                raise ValueError('Ambiguous surviving literal')
            else:
                if not path.startswith('/core/'):
                    raise ValueError('Source pointer unavailable')
                result = {'@SUMMARY':summary_id,'source_pointer':path,'span':[sa,sn]}
        else:
            raise ValueError('Reference crosses replacement boundary')
        if result.get('@SUMMARY') != summary_id:
            na,nn = result['span']
            if new_exposition[na:na+nn] != old_fragment:
                raise ValueError('Unchanged reference content drifted')
        if result != value:
            changes.append({'before':deepcopy(value),'after':deepcopy(result)})
        return result

    return visit(node,source_pointer),changes

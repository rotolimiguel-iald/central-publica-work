"""Remap internal literal references after a separately reviewed condensation.

This module does not edit any source, enable retrieval, approve a capsule or deploy.
It distinguishes exact loaded literals from reviewed semantic block summaries.
"""
import copy

def remap(node,old_exposition,new_exposition,blocks,section_start,source_pointer=''):
    changes=[]
    def visit(value,path):
        if isinstance(value,list):
            return [visit(v,path+'/'+str(i)) for i,v in enumerate(value)]
        if not isinstance(value,dict):return value
        if '@EXPOSITION' not in value:
            # Structural source pointers, not array offsets, identify fields
            # retained in the original candidate's compact metadata containers.
            if '@' in value and 'fields' in value:
                out=copy.deepcopy(value)
                out['fields']={k:visit(v,source_pointer+value['@']+k) for k,v in value['fields'].items()}
                return out
            return {k:visit(v,path+'/'+k.replace('~','~0').replace('/','~1')) for k,v in value.items()}
        offset,length=value['span']
        if not isinstance(offset,int) or not isinstance(length,int) or offset<0 or length<=0 or offset+length>len(old_exposition):
            raise ValueError('Invalid original literal span')
        literal=old_exposition[offset:offset+length]
        if not literal.startswith(value['starts_with']):raise ValueError('Literal prefix mismatch')
        if literal in new_exposition:
            result=copy.deepcopy(value)
            result['span']=[new_exposition.index(literal),len(literal)]
            # The old heading may no longer exist. The exact span is the anchor.
            result['@EXPOSITION']='literal na exposição carregada'
        else:
            matches=[]
            for b in blocks:
                c=b['original_section_coordinates']
                if section_start+c['unicode_start']<=offset and offset+length<=section_start+c['unicode_end_exclusive']:
                    matches.append(b)
            if len(matches)!=1:raise ValueError('Removed literal lacks a unique reviewed summary block')
            b=matches[0]
            label='**Estatutos ['+b['id']+']**'
            start=new_exposition.find(label)
            if start<0 or new_exposition.count(label)!=1:raise ValueError('Summary block missing or ambiguous')
            end=new_exposition.find('\n**Estatutos [',start+len(label))
            if end<0:end=len(new_exposition)
            # The integrating document must define @SUMMARY once in its header:
            # a semantic summary, never a literal; source id is
            # resultado_publicado_integral, with the original pointer below.
            result={'@SUMMARY':b['id'],'source_pointer':path,'span':[start,end-start]}
        changes.append({'source_pointer':path,'before':value,'after':result})
        return result
    return visit(node,source_pointer),changes

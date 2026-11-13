"""One verified public science snapshot per call; no network or active-pointer rereads.

A snapshot is a retrieval resource, not an authorization or proof. The host retains
account/consent/wallet checks and must pass the SAME object to router and workers.
"""
from copy import deepcopy
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
from types import MappingProxyType
from iald_retrieval import terms
from iald_kernel import KernelCatalog, execute_tool as kernel_tool

SCHEMA = 'iald.science-snapshot.v1'
SCIENCE_TOOLS = frozenset(('iald_public_read','iald_atlas_search','iald_atlas_read','search_tgl','fetch_tgl','iald_kernel_search','iald_kernel_read',
                         'iald_kernel_list','iald_kernel_verification'))

def digest(raw):
    return hashlib.sha256(raw).hexdigest()

def encoded(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':')).encode('utf-8')

def checked(record, root):
    name = record['path']
    path = Path(name)
    path = path if path.is_absolute() else root/path
    path = path.resolve()
    if not path.is_relative_to(root):
        raise ValueError('Science artifact outside immutable release')
    raw = path.read_bytes()
    if digest(raw)!=record['sha256'] or len(raw)!=record['bytes']:
        raise ValueError('Science artifact integrity failure')
    return raw

class FrozenKernel(KernelCatalog):
    """Legacy catalog methods over already verified bytes, including verification."""
    def _read_checked(self,name):
        if getattr(self,'_captured',False):
            if name not in self.texts: raise ValueError('Kernel source not captured')
            return self.texts[name]
        return super()._read_checked(name)
    def verification(self,path=''):
        if not getattr(self,'_captured',False): return super().verification(path)
        if path and path not in self.records: raise ValueError('Unknown kernel source')
        report=deepcopy(self._verification)
        if path and 'files' in report:
            if path not in report['files']:
                return {'source_sha256':self.source_sha,'path':path,'status':'NOT_VERIFIED_IN_THIS_DEPLOYMENT'}
            report['files']={path:report['files'][path]}
        return report

@dataclass(frozen=True)
class ScienceSnapshot:
    manifest_path: Path
    manifest_sha256: str
    identity: dict
    prefix: str
    catalog: object
    jev_control: dict
    _documents: dict
    _units: tuple
    native_prefix: str
    _packages: dict

    @classmethod
    def capture(cls, manifest_path):
        path=Path(manifest_path).resolve()
        raw=path.read_bytes(); cfg=json.loads(raw); package_links={}
        # Active canonical manifest may point at a reviewed immutable snapshot.
        if cfg.get('schema')!=SCHEMA:
            link=cfg.get('science_snapshot')
            if not isinstance(link,dict): raise ValueError('Versioned science snapshot missing')
            package_links=link.get('packages',{})
            target=Path(link['path']).resolve(); target_raw=target.read_bytes()
            if digest(target_raw)!=link['sha256']: raise ValueError('Snapshot pointer hash mismatch')
            if path.read_bytes()!=raw: raise ValueError('Active pointer changed during capture')
            path=target; raw=target_raw; cfg=json.loads(raw)
        if cfg.get('schema')!=SCHEMA: raise ValueError('Unknown science snapshot schema')
        root=path.parent
        artifacts=cfg['artifacts']
        if not isinstance(artifacts,list) or not artifacts: raise ValueError('Empty release')
        blobs={}
        for record in artifacts:
            key=record['path']
            if key in blobs: raise ValueError('Duplicate science artifact')
            blobs[key]=checked(record,root)
        prefix=blobs[cfg['prefix_file']].decode('utf-8')
        if not prefix or len(prefix.encode())>150000: raise ValueError('Bounded core exceeds engineering budget')
        identity=dict(cfg['identity']); identity['manifest_sha256']=digest(raw)
        if not re.fullmatch(r'v[0-9]+',identity.get('release','')): raise ValueError('Invalid release')
        docs={}
        for entry in cfg['documents']:
            ident=entry['id']
            if not re.fullmatch(r'[a-z0-9_]+',ident) or ident in docs: raise ValueError('Duplicate/invalid source ID')
            payload=blobs[entry['path']]
            docs[ident]={**entry,'sha256':digest(payload),'bytes':len(payload),'text':payload.decode('utf-8')}
        units=[]; parsed_documents={}
        for row in json.loads(blobs[cfg['units_file']]):
            if row['document_id'] not in docs: raise ValueError('Unit source unavailable')
            text=row['text']
            if digest(text.encode())!=row['sha256']: raise ValueError('Unit hash mismatch')
            original=docs[row['document_id']]['text']
            if 'json_pointer' in row or row['id']=='result_global_statutes':
                if row['document_id'] not in parsed_documents:
                    parsed_documents[row['document_id']]=json.loads(original)
                parsed=parsed_documents[row['document_id']]
            if 'json_pointer' in row:
                key=row['json_pointer'].removeprefix('/core/').replace('~1','/').replace('~0','~')
                if json.loads(text)!={'core':{key:parsed['core'][key]}}:
                    raise ValueError('Retrieved topic differs from complete source')
            elif 'start_char' in row:
                if text!=original[row['start_char']:row['end_char']]:
                    raise ValueError('Retrieved section differs from complete source')
            elif row['id']=='result_global_statutes':
                if json.loads(text)!={k:v for k,v in parsed.items() if k!='core'}:
                    raise ValueError('Global statutes differ from complete source')
            else: raise ValueError('Unbound retrieval unit')
            units.append({**row,'_terms':frozenset(terms(row['id']+' '+text))})
        kernel=FrozenKernel(root/cfg['kernel_root'],root/cfg['kernel_verification'])
        if kernel.source_sha!=identity['source_sha256']: raise ValueError('Kernel belongs to another release')
        kernel._verification=super(FrozenKernel,kernel).verification()
        kernel._captured=True
        jev=json.loads(blobs[cfg['jev_file']])
        from iald_jev_control import validate_contract
        validate_contract(jev)
        for anchor in jev['anchors']:
            if kernel.records[anchor['file']]['sha256']!=anchor['sha256']:
                raise ValueError('JEV anchor mismatch')
        if jev['release']!=identity['release'] or jev['source_sha256']!=identity['source_sha256']:
            raise ValueError('JEV belongs to another release')
        if path.read_bytes()!=raw: raise ValueError('Immutable manifest changed during capture')
        # Every artifact checked twice catches races while loading derived indexes.
        for record in artifacts:
            if checked(record,root)!=blobs[record['path']]: raise ValueError('Artifact changed during capture')
        package_paths={}
        for name,record in package_links.items():
            if name not in ('haiku55','sonnet'): raise ValueError('Unknown measured package')
            package_path=Path(record['path']).resolve()
            if not package_path.is_relative_to(root): raise ValueError('Package outside pinned release')
            certificate=(package_path/'manifest.json').read_bytes()
            if digest(certificate)!=record['manifest_sha256']: raise ValueError('Measured certificate pin mismatch')
            if json.loads(certificate).get('deployment')!=identity: raise ValueError('Certificate from another release')
            package_paths[name]=package_path
        native_prefix=blobs[cfg['native_prefix_file']].decode('utf-8') if cfg.get('native_prefix_file') else prefix
        return cls(path,digest(raw),MappingProxyType(identity),prefix,kernel,MappingProxyType(jev),
                   MappingProxyType(docs),tuple(units),native_prefix,MappingProxyType(package_paths))

    def package_path(self,name):
        if name not in self._packages: raise ValueError("Measured package not captured")
        return self._packages[name]

    def check(self):
        # No ACTIVE reread: an already admitted call deliberately retains its release.
        if self.identity['manifest_sha256']!=self.manifest_sha256: raise ValueError('Snapshot identity changed')
        return dict(self.identity)

    def routing_memory(self):
        doc=self._documents['um_forma_canonica_integral']
        text=doc['text'].lstrip('\ufeff').replace('\r\n','\n').replace('\r','\n')[:8000]
        raw=text.encode('utf-8'); cp=self.jev_control['core_packet']
        if digest(raw)!=cp['sha256'] or cp['um_version']!=self.identity['release']:
            raise ValueError('Pinned routing packet differs from canonical source')
        return text, {'packet_sha256':digest(raw),'packet_bytes':len(raw),
            'source_sha256':doc['sha256'],'url':doc.get('url'),'release':self.identity['release'],
            'release_source_sha256':self.identity['source_sha256'],'first_character':0,'characters':len(text),
            'coverage':'COMPLETE_BOUND_ROUTING_PACKET_PARTIAL_CANONICAL','sha256_da_fonte':digest(raw),
            'estatuto':'REAL','inscrito_por':{'kind':'host','id':'iald_science_snapshot','scope':'byte_verification_not_source_authorship'},
            'science_identity':dict(self.identity)}

    def search(self,query,limit=4):
        if not isinstance(query,str) or not query.strip() or len(query)>10000: raise ValueError('Invalid science query')
        wanted=set(terms(query)); limit=max(1,min(int(limit),8))
        ranked=sorted(((len(wanted & u['_terms'])+3*len(wanted & set(terms(u.get('label','')))),u) for u in self._units),key=lambda x:(-x[0],x[1]['id']))
        rows=[]
        for score,u in ranked:
            if not score or len(rows)>=limit: break
            doc=self._documents[u['document_id']]
            rows.append({k:v for k,v in u.items() if k not in ('_terms','text')} | {
                'matched_terms':score,'document_sha256':doc['sha256'],'url':doc.get('url'),
                'unit_chars':len(u['text']),'fetch_id':u['id'],
                'scope':'COMPLETE_UNIT_AVAILABLE_BY_FETCH; MATCH_IS_NOT_PROOF'})
        return {'status':'OK','identity':dict(self.identity),'results':rows,
                'coverage':'PARTIAL_RETRIEVAL_NOT_FULL_CORPUS','zero_matches_proves_absence':False}

    def fetch(self,id,offset=0,max_chars=4000):
        unit=next((u for u in self._units if u['id']==id),None)
        if unit:
            doc=self._documents[unit['document_id']]; text=unit['text']; sha=unit['sha256']
        elif id in self._documents:
            doc=self._documents[id]; text=doc['text']; sha=doc['sha256']
        else: raise ValueError('Unknown source or unit; search first')
        offset=int(offset); count=int(max_chars)
        if not 0<=offset<=len(text) or not 1<=count<=50000: raise ValueError('Invalid source page')
        end=min(len(text),offset+count)
        return {'status':'OK','identity':dict(self.identity),'id':id,'sha256':sha,
                'document_sha256':doc['sha256'],'url':doc.get('url'),'text':text[offset:end],
                'offset':offset,'offset_unit':'UNICODE_CODE_POINTS','next_offset':end if end<len(text) else None,
                'total_chars':len(text),'whole_unit':offset==0 and end==len(text),
                'line_start':text.count('\n',0,offset)+1,'line_end':text.count('\n',0,end)+1,
                'notice':'A page is partial; preserve all hypotheses, statutes and linked limits before concluding.'}

    def execute_tool(self,name,args,fallback=None):
        if not isinstance(args,dict): raise ValueError('Invalid tool arguments')
        if name=='iald_public_read':
            return {'status':'UNAVAILABLE_USE_VERSIONED_SEARCH_TGL','identity':dict(self.identity),
                    'notice':'Live public catalog is not the pinned release; use search_tgl/fetch_tgl.'}
        if name in ('iald_atlas_search','iald_atlas_read'):
            return {'status':'UNAVAILABLE_USE_VERSIONED_SEARCH_TGL','identity':dict(self.identity)}
        if name=='search_tgl': return self.search(**args)
        if name=='fetch_tgl': return self.fetch(**args)
        if name in SCIENCE_TOOLS:
            result=kernel_tool(self.catalog,name,args)
            return {**result,'science_identity':dict(self.identity)}
        if fallback is None: raise ValueError('Not a science tool')
        return fallback(name,args)

    def pre_retrieve(self,messages,max_bytes=120000):
        """Local lexical selection, not an LLM tool call. Keep whole units or refuse.

        Explicit human `fetch_tgl ID OFFSET` supports paged continuation for a
        text-only executor. Recent human turns aid lexical followups; no claim of
        semantic completeness follows from this deterministic selection.
        """
        if not 1<=int(max_bytes)<=120000: raise ValueError('Invalid retrieval budget')
        human=[]
        for message in messages:
            if message.get('role')!='user': continue
            content=message.get('content')
            if isinstance(content,str): human.append(content)
            elif isinstance(content,list):
                human.append('\n'.join(p.get('text','') for p in content if isinstance(p,dict) and p.get('type') in ('text','input_text')))
        if not human: raise ValueError('No human query available for retrieval')
        command=re.fullmatch(r'\s*fetch_tgl\s+([a-z0-9_]+)\s+(\d+)\s*',human[-1])
        if command:
            global_unit=next(u for u in self._units if u['id']=='result_global_statutes')
            selected=[{k:v for k,v in global_unit.items() if k!='_terms'} | {'whole_unit':True},
                      self.fetch(command[1],int(command[2]),12000)]
            mode='EXPLICIT_HUMAN_PAGED_CONTINUATION'
        else:
            # Derive search terms; do not cut the original human message/history.
            query=' '.join(dict.fromkeys(terms('\n'.join(human[-3:]))))
            if len(query)>10000: raise ValueError('Retrieval query overflow; human input preserved')
            found=self.search(query or 'IALD',limit=8)
            global_unit=next(u for u in self._units if u['id']=='result_global_statutes')
            selected=[{k:v for k,v in global_unit.items() if k!='_terms'} | {'whole_unit':True}]
            omitted=[]
            for match in found['results']:
                unit=next(u for u in self._units if u['id']==match['fetch_id'])
                candidate={**match,'text':unit['text'],'whole_unit':True}
                if len(encoded(selected+[candidate]))+2000<=max_bytes:
                    selected.append(candidate)
                else:
                    omitted.append(match['id'])
            mode='LOCAL_LEXICAL_WHOLE_UNITS'
        receipt={'identity':dict(self.identity),'mode':mode,'coverage':'PARTIAL_RETRIEVAL_NOT_FULL_CORPUS',
                 'source_ids':[r.get('id') for r in selected],
                 'selection_policy':'OPTIONAL_WHOLE_UNITS_WITHIN_BUDGET; OTHERS_REMAIN_FETCHABLE',
                 'budget_excluded_unit_ids':omitted if not command else [], 'zero_matches_proves_absence':False,
                 'selection_sha256':digest(encoded(selected)), 'units':selected}
        prompt=('\nFONTES DA MESMA VERSÃO, RECUPERADAS LOCALMENTE ANTES DO ENVIO\n'
                'A seleção é parcial e lexical, não leitura integral do acervo. Sem resultado não prova ausência. '
                'Não alegue executar ferramentas no Kimi. Peça continuidade se faltarem fontes; o humano pode '
                'solicitar fetch_tgl ID OFFSET para a próxima página. Não conclua além dos limites lidos.\n'
                +encoded(receipt).decode())
        if len(prompt.encode())>max_bytes: raise ValueError('Mandatory complete retrieval units exceed budget; no truncation')
        return {'prompt':prompt,'receipt':receipt}

"""Additive documentary companion; no statistical composition or human admission.

The caller pins this manifest independently. Raw HTML is reread once and the
extraction is reproduced, so an edited text copy cannot replace source bytes.
Only the two explicitly reviewed reader contracts are supported.
"""
from pathlib import Path
from html.parser import HTMLParser
import hashlib,json,math,re

class CompanionError(ValueError): pass

class Extractor(HTMLParser):
    def __init__(self):
        super().__init__();self.skip=0;self.parts=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'):self.skip+=1
        if tag in ('p','div','br','h1','h2','h3','li','tr','section','article'):self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style'):self.skip=max(0,self.skip-1)
        if tag in ('p','div','h1','h2','h3','li','tr','section','article'):self.parts.append('\n')
    def handle_data(self,data):
        if not self.skip:self.parts.append(data)

def extract(raw,encoding):
    parser=Extractor();parser.feed(raw.decode(encoding));parser.close()
    return '\n'.join(' '.join(line.split()) for line in ''.join(parser.parts).splitlines() if line.strip())

def read_pin(row,root):
    p=(root/row['relative_path']).resolve()
    if not p.is_relative_to(root):raise CompanionError('SOURCE_OUTSIDE_ROOT')
    raw=p.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=row['sha256']:raise CompanionError('SOURCE_PIN_MISMATCH')
    return raw

def verify(manifest_path,expected_sha256,gate):
    try:
        path=Path(manifest_path).resolve();raw=path.read_bytes();root=path.parent
        if hashlib.sha256(raw).hexdigest()!=expected_sha256:raise CompanionError('MANIFEST_PIN_MISMATCH')
        m=json.loads(raw)
        if gate['spec_sha256']!=m['spec_sha256'] or gate['binding_sha256']!=m['ancestor_binding_sha256']:
            raise CompanionError('ANCESTOR_SCOPE_MISMATCH')
        if gate['v2_frozen'] is not False:raise CompanionError('NOT_DRAFT')
        if set(m['readers'])!={'L1b_sh0es_r25','L6_sirenes'}:raise CompanionError('EXACT_COMPANION_INVENTORY_REQUIRED')
        updates={}
        for rid,row in m['readers'].items():
            source=read_pin(row['source'],root);text=extract(source,row['encoding'])
            anchor=row['anchor']
            if len(anchor)<80 or text.count(anchor)!=1:raise CompanionError('UNIQUE_CONTEXT_REQUIRED')
            source_meta=gate['spec_snapshot']['leitores'][rid]
            if rid=='L1b_sh0es_r25':
                pattern=r'Combining JWST Cepheid measurements in 19 hosts \(24 SNe Ia\) with HST data \(37 hosts, 42 SNe Ia\) yields H0 = ([0-9]+\.[0-9]+) \+/- ([0-9]+\.[0-9]+) km/s/Mpc\.'
                match=re.fullmatch(pattern,anchor)
                if not match:raise CompanionError('L1B_CONTEXT_OR_NUMERIC_SIGN')
                center,sigma=map(float,match.groups())
                detail={'published_sigma':sigma,'sigma_transformation':'identity','statistical_likelihood_qualified':False}
            else:
                pattern=r'.*estimate \\\( H_0 = ([0-9]+\.[0-9]+)\^\{\+([0-9]+\.[0-9]+)\}_\{-([0-9]+\.[0-9]+)\}.*'
                match=re.fullmatch(pattern,anchor)
                if not match or 'median with 68.3% (90%) symmetric credible interval' not in anchor or 'GW170817' not in anchor:
                    raise CompanionError('L6_CONTEXT_OR_NUMERIC_SIGN')
                center,plus,minus=map(float,match.groups());sigma=(plus+minus)/2
                detail={'sigma_plus':plus,'sigma_minus':minus,'reported_summary':'posterior median;68.3% credible interval',
                        'sigma_transformation':'DERIVED arithmetic half-width mean; local symmetric Gaussian approximation only',
                        'statistical_likelihood_qualified':False,'not_a_published_sampling_standard_deviation':True}
            if any(type(source_meta[k]) not in (int,float) or not math.isfinite(source_meta[k]) for k in ('H0','sigma')):
                raise CompanionError('INVALID_SPEC_NUMBER')
            if center!=source_meta['H0'] or sigma!=source_meta['sigma']:raise CompanionError('SPEC_SOURCE_VALUE_MISMATCH')
            if row['source_metadata']!={'H0':center,**detail}:raise CompanionError('METADATA_TRANSFORMATION_MISMATCH')
            updates[rid]={'status':'REAL_DOCUMENTARY_HASH_ONLY','source_sha256':row['source']['sha256'],
                          'source_metadata':row['source_metadata'],'operator_admitted':False,'physical_map':'OPEN'}
        readers={**gate['verified_readers'],**updates}
        declared=sorted(k for k,v in readers.items() if v['status']!='REAL_DOCUMENTARY_HASH_ONLY')
        return {'status':'CANDIDATE_DOCUMENTARY_EXTENSION_ONLY','updates':updates,
                'n_alvos_declarados':len(declared),'declared_unverified_reader_ids':declared,
                'scope':'entire inventory: not documentary-verified AND not admitted',
                'required_sources_admitted':False,'admission_status':'PENDING_D_H',
                'may_open_data':False,'v2_frozen':False,'verdict':None,
                'old_spec_and_binding_unchanged':True,'observed_composition':False}
    except CompanionError:raise
    except (KeyError,TypeError,ValueError,OSError,UnicodeError) as exc:
        raise CompanionError('MALFORMED_COMPANION: '+str(exc)) from exc

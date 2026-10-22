"""Read original DOCX equations omitted by the historical plain-text index."""
from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET
import json, hashlib, datetime

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'C:\IALD\IMac LA\Física - TGL\Base Referencial Completa TGL\The (O) Graviton.docx')
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
      'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math'}

def readable(el):
    if el is None:
        return ''
    tag = el.tag.split('}')[-1]
    if tag == 't':
        return el.text or ''
    if tag.endswith('Pr'):
        return ''
    if tag == 'f':
        return '(' + readable(el.find('m:num', NS)) + ')/(' + readable(el.find('m:den', NS)) + ')'
    if tag == 'rad':
        degree = readable(el.find('m:deg', NS))
        return ('root['+degree+']' if degree else 'sqrt') + '(' + readable(el.find('m:e', NS)) + ')'
    if tag in ('sSup', 'sSub', 'sSubSup'):
        s = readable(el.find('m:e', NS))
        if tag in ('sSub', 'sSubSup'):
            s += '_{' + readable(el.find('m:sub', NS)) + '}'
        if tag in ('sSup', 'sSubSup'):
            s += '^{' + readable(el.find('m:sup', NS)) + '}'
        return s
    return ''.join(readable(c) for c in el)

if __name__ == '__main__':
    folder = ROOT/'historical_r8'
    folder.mkdir(exist_ok=True)
    destination = folder/'SOURCE_EXTRACTION_R8.json'
    if destination.exists():
        raise FileExistsError(destination)
    data = SOURCE.read_bytes()
    with ZipFile(SOURCE) as z:
        xml = z.read('word/document.xml')
    doc = ET.fromstring(xml)
    ps = doc.findall('.//w:body/w:p', NS)
    indices = [121,125,129,132,198,200,201,320,322,324,326,327,328,330,331,423,424]
    result = {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source': {'path': str(SOURCE), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes':len(data)},
        'document_xml_sha256': hashlib.sha256(xml).hexdigest(),
        'script': {'path': str(Path(__file__)), 'sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},
        'locator': 'One-based direct word/document.xml body/w:p paragraphs, including empty paragraphs; not corpus line numbering.',
        'paragraphs': [{'paragraph': i, 'readable': readable(ps[i-1]),
                        'raw_xml': ET.tostring(ps[i-1],encoding='unicode')} for i in indices],
        'omml_count': len(doc.findall('.//m:oMath',NS)),
        'scope': 'Text/structural recovery only; raw XML retained. No rendering, science execution, fitting or formal proof.',
        'remaining_inputs': ['epsilon_star/m_star', 'rho0', 'profile exponent beta~2-3 distinct from betaTGL', 'xi and C conventions', 'mu_W and deltaPsi for the path'],
        'no_observed_discriminant': True}
    with destination.open('x',encoding='utf-8') as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({'status':'PASS_EXTRACTION_ONLY','destination':str(destination),'source':result['source'],'omml_count':result['omml_count']},ensure_ascii=False))

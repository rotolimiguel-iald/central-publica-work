import base64
import io
import unittest
import wave
from iald_mimo_multimodal import media_part

def part(raw,mime='audio/wav',kind='input_audio'):
    return {'type':kind,kind:{'data' if kind=='input_audio' else 'url':'data:'+mime+';base64,'+base64.b64encode(raw).decode()}}

class MediaTests(unittest.TestCase):
    def wav(self,seconds=1):
        f=io.BytesIO()
        with wave.open(f,'wb') as w:
            w.setnchannels(1);w.setsampwidth(1);w.setframerate(8000);w.writeframes(b'\x80'*(8000*seconds))
        return f.getvalue()
    def test_real_wav(self):
        p=part(self.wav());self.assertEqual(media_part(p,media_authorized=True),p)
    def test_consent(self):
        with self.assertRaises(ValueError):media_part(part(self.wav()))
    def test_duration(self):
        with self.assertRaises(ValueError):media_part(part(self.wav(31)),media_authorized=True)
    def test_signature(self):
        with self.assertRaises(ValueError):media_part(part(b'not wave'),media_authorized=True)
    def test_remote(self):
        with self.assertRaises(ValueError):media_part({'type':'input_audio','input_audio':{'data':'https://x/a.wav'}},media_authorized=True)
    def test_video_boundary(self):
        p=part(b'\0\0\0\x18ftypisomtest','video/mp4','video_url')
        self.assertEqual(media_part(p,media_authorized=True,probe=lambda *_:dict(duration=5,types=['video'])),p)
        for duration in (11,float('nan'),True):
            with self.subTest(duration=duration),self.assertRaises(ValueError):media_part(p,media_authorized=True,probe=lambda *_:dict(duration=duration,types=['video']))
    def test_stream_mismatch(self):
        with self.assertRaises(ValueError):media_part(part(self.wav()),media_authorized=True,probe=lambda *_:dict(duration=1,types=['video']))
    def test_size(self):
        with self.assertRaises(ValueError):media_part(part(self.wav()+b'x'*512000),media_authorized=True)
    def test_bad_container(self):
        with self.assertRaises((ValueError,EOFError,wave.Error)):media_part(part(b'RIFF0000WAVEfake'),media_authorized=True)

if __name__=='__main__': unittest.main(verbosity=2)

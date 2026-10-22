# -*- coding: utf-8 -*-
"""Testes novos da R2.2 (revisão independente R2.1 de 13/10). Rodam nas DUAS cópias: em copia_r2_1 (candidato R2.1 e
ferramentas R2.1, byte a byte) os que reproduzem achados devem FALHAR; em copia (candidato R2.2 e ferramentas R2.2)
devem PASSAR. Cada um reproduz o cenário EXATO do revisor (10_REVISAO_R2_1/REVISAO_R2_1.md §4 e §5).

  T_K4c  alvo MODIFICADO (bytes do candidato) depois de conferir_alvos OK: nunca REVERTIDA/ok=true; a trava do
         implantar segue vendo a implantação pendente; um recibo REVERTIDA com app_religado=false não libera a trava
  T_K4b  alvo travado em modo EXCLUSIVO depois de conferir_alvos OK: acao_requerida preenchida (nunca null)
  T_K4b2 --sem-reiniciar: status REVERTIDA_SEM_RELIGAR com a ação manual (o reverter não religou)
  T_K3r  o REVERTER encontra o stop sem efeito: nada restaurado, tarefa reabilitada (só porque foi ele que a
         desabilitou), o recibo diz o estado LIDO (vivo sem supervisor) e nunca «fica parado»
  T_P8b  o filho web v2 morre ao nascer (pids trocando, ou nenhum de pé): saída 3 mantida, recibo e saída com o diagnóstico
         LACO_DE_QUEDA_PROVAVEL e o COMO DISTINGUIR; controle: pid estável = LENTO_PROVAVEL
  G_N1c  caminho com 16.000 componentes (path_reason, read_allowed_file, dispatch init): recusa visível < 50 ms
  M_DOC  o campo `ferramentas` do manifesto do candidato cita o sha256 REAL do aplicar_blocos.py
Só sintético, só na pasta temporária da suíte. Nada de produção.
"""
import contextlib
import ctypes
import hashlib
import importlib
import io
import json
import os
import sys
import tempfile
import time
import unittest
import uuid
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve().parent
COPIA = HERE.parents[2]
R22 = COPIA.parent
WORK = R22.parent
TOOLS = R22 / 'ref_r2_1' if COPIA.name == 'copia_r2_1' else R22
MANIFESTO = (WORK / '9_R2_1' / 'CANDIDATO_MANIFESTO_R2_1.json' if COPIA.name == 'copia_r2_1'
             else R22 / 'CANDIDATO_MANIFESTO_R2_2.json')
sys.path.insert(0, str(TOOLS))
implantacao_lib = importlib.import_module('implantacao_lib')
implantar = importlib.import_module('implantar')
reverter = importlib.import_module('reverter')

from iald_memory import MemoryStore, guard  # noqa: E402  (suite/core: o candidato da cópia)
import session_memory as sm  # noqa: E402     (suite/sessions: o candidato da cópia)

SCOPE = {'house': 'IALD', 'principal': 'teste_r2_2'}
ACTOR = {'id': 'teste-r2-2', 'kind': 'agent'}
WIN_PROD = 'C:' + os.sep + 'IALD' + os.sep + 'MEMORIA_IALD'


def sha(b):
    return hashlib.sha256(b).hexdigest()


class Tmp(unittest.TestCase):
    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        self.root = Path(self._td.name)

    def tearDown(self):
        try:
            self._td.cleanup()
        except OSError:
            pass


# ============================================================================================= backend falso
class FakeBackend:
    """Backend de processos em memória (sem processo real): tarefa + supervisor + web (o da suíte R2.1)."""
    nome = 'fake'

    def __init__(self, rodando=True, stop_mata_web=True, saude_ok=True):
        self.enabled, self.sup, self.web = True, int(rodando), int(rodando)
        self.stop_mata_web, self.saude_ok = stop_mata_web, saude_ok
        self.calls = []

    def tarefa_ler(self):
        estado = 'Disabled' if not self.enabled else ('Running' if self.sup else 'Ready')
        return {'existe': True, 'nome': 'IALD Web Server (fake)', 'caminho': os.sep, 'estado': estado, 'habilitada': self.enabled}

    def tarefa_desabilitar(self):
        self.calls.append('disable')
        self.enabled = False
        return {'cmdlet': 'Disable (fake)'}

    def tarefa_habilitar(self):
        self.calls.append('enable')
        self.enabled = True
        return {'cmdlet': 'Enable (fake)'}

    def tarefa_parar(self):
        self.calls.append('stop_task')
        self.sup = 0
        if self.stop_mata_web:
            self.web = 0
        return {'cmdlet': 'Stop (fake)'}

    def tarefa_iniciar(self):
        self.calls.append('start')
        if not self.enabled:
            raise implantacao_lib.ImplantacaoError('tarefa desabilitada (fake)')
        self.sup, self.web = 1, 1
        return {'cmdlet': 'Start (fake)'}

    def listar(self):
        return {'web': [{'pid': 1}] * self.web, 'supervisores': [{'pid': 2}] * self.sup, 'listen': [{'pid': 1}] * self.web}

    def parar_script(self):
        self.calls.append('stop_script')
        self.sup = 0
        if self.stop_mata_web:
            self.web = 0
        return {'rc': 0}

    def iniciar_desacoplado(self):
        self.calls.append('start_wmi')
        self.sup, self.web = 1, 1
        return {'pid': 3}

    def saude(self):
        return (self.saude_ok and self.web == 1, 200 if self.saude_ok else 'sem saude (fake)')


class FakeLaco(FakeBackend):
    """P8b: o supervisor vive e relança; o filho web morre ao nascer (cada leitura vê um pid novo, ou nenhum)."""

    def __init__(self, estavel=False, nunca=False):
        super().__init__(rodando=False, saude_ok=False)
        self.estavel = estavel
        self.nunca = nunca            # o filho morre antes de qualquer leitura (o caso do ensaio P8b)
        self.n = 0

    def listar(self):
        if not self.sup:
            return {'web': [], 'supervisores': [], 'listen': []}
        self.n += 1
        if self.nunca:
            web = []
        elif self.estavel:
            web = [{'pid': 500}]
        else:
            web = [] if self.n % 3 == 0 else [{'pid': 500 + self.n}]
        return {'web': web, 'supervisores': [{'pid': 2}], 'listen': []}


def cfg_minima(root, **extra):
    mem = root / 'mem'
    (mem / 'state').mkdir(parents=True, exist_ok=True)
    man = root / 'manifesto.json'
    if not man.exists():
        man.write_text(json.dumps({'arquivos': [], 'originais': []}), encoding='utf-8')
    cfg = {'candidato_root': str(root / 'cand'), 'manifesto_candidato': str(man), 'raizes': {WIN_PROD: str(mem)},
           'arquivo_D': str(root / 'D'), 'recibos_dir': str(root / 'recibos'), 'gerir_processos': False,
           'silencio_s': 0, 'esperar_parada_s': 1, 'esperar_inicio_s': 2, 'tarefa_agendada': 'IALD Web Server (fake)',
           'porta': 8082}
    cfg.update(extra)
    p = root / 'cfg.json'
    p.write_text(json.dumps(cfg, ensure_ascii=False), encoding='utf-8')
    return p, cfg


def montar_reversao(root, backup_presente=True):
    """Uma implantação CONCLUIDA sintética: 1 alvo hoje com os bytes do candidato, backup íntegro."""
    alvo = root / 'mem' / 'alvo.py'
    alvo.parent.mkdir(parents=True, exist_ok=True)
    orig, cand = b'original\n', b'candidato\n'
    alvo.write_bytes(cand)
    man = root / 'manifesto.json'
    man.write_text(json.dumps({'arquivos': [{'target': WIN_PROD + os.sep + 'alvo.py', 'sha256': sha(cand)}],
                               'originais': [{'source': WIN_PROD + os.sep + 'alvo.py', 'sha256': sha(orig)}]}),
                   encoding='utf-8')
    _, cfg = cfg_minima(root)
    bak = alvo.with_name('alvo.py.bak_20261013')
    if backup_presente:
        bak.write_bytes(orig)
    passos = {'parar_app': {'status': 'OK', 'tarefa_antes': {'existe': True, 'habilitada': True, 'estado': 'Running'}},
              'backup_integral': {'status': 'PULADO'},
              'substituir_arquivos': {'status': 'OK', 'arquivos': [
                  {'alvo': str(alvo), 'existia': True, 'sha256_antes': sha(orig), 'backup': str(bak),
                   'sha256_depois_esperado': sha(cand), 'fase': 'substituido'}]}}
    rd = Path(cfg['recibos_dir'])
    rd.mkdir(exist_ok=True)
    rp = rd / 'RECIBO_IMPLANTACAO_SINTETICO.json'
    rp.write_text(json.dumps({'dry_run': False, 'status': 'CONCLUIDA', 'stamp': 'SINT', 'config': cfg,
                              'mudancas_iniciadas': ['substituir_arquivos'], 'passos': passos}), encoding='utf-8')
    return rp, alvo, cand, rd


def rodar_main(mod, argv):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = mod.main(argv)
    linhas = [ln for ln in buf.getvalue().splitlines() if ln.strip().startswith('{')]
    return rc, json.loads(linhas[-1])


def pendentes(rd):
    r = implantacao_lib.recibos_pendentes([rd])
    return [Path(p['recibo']).name for p in r['pendentes']]


class TravaExclusiva:
    """Abre o arquivo SEM compartilhamento (share 0): ninguém lê nem escreve até soltar (o PrendeExclusivo do revisor)."""

    def __init__(self, path):
        from ctypes import wintypes
        k = ctypes.WinDLL('kernel32', use_last_error=True)
        k.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD,
                                  wintypes.DWORD, wintypes.HANDLE]
        k.CreateFileW.restype = wintypes.HANDLE
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        self.k = k
        self.h = k.CreateFileW(str(path), 0x80000000, 0, None, 3, 0, None)
        if self.h in (None, 0, (1 << 64) - 1, -1):
            raise OSError('CreateFileW falhou: %d' % ctypes.get_last_error())

    def soltar(self):
        if self.h:
            self.k.CloseHandle(self.h)
            self.h = None


# =========================================================================================== K4c / K4b
class ReverterK4c(Tmp):
    def test_T_K4c_target_modified_after_check_is_failure_and_lock_still_pending(self):
        """Cenário do revisor: alvo com os bytes do candidato DEPOIS de conferir_alvos OK, antes de religar."""
        rp, alvo, cand, rd = montar_reversao(self.root)
        fake = FakeBackend(rodando=True)

        def blocos_e_mexe(self_rev):
            # roda DEPOIS de conferir_alvos OK e ANTES de religar (no recibo sintético não há blocos a restaurar)
            alvo.write_bytes(cand)                 # o alvo volta a ter os bytes do candidato
            return {'status_forcado': 'PULADO', 'nota': 'teste: alvo modificado depois de conferir_alvos'}
        with mock.patch.object(reverter, 'backend_de', lambda cfg: fake), \
                mock.patch.object(reverter.Reversao, 'restaurar_blocos', blocos_e_mexe):
            rc, out = rodar_main(reverter, ['--recibo', str(rp)])
        self.assertEqual(alvo.read_bytes(), cand)
        self.assertNotIn('start', fake.calls, 'o app foi religado sobre um alvo fora do original')
        self.assertNotEqual(out['status'], 'REVERTIDA', out)
        self.assertTrue(out['status'].startswith('FALHOU_EM_'), out['status'])
        self.assertFalse(out['ok'], out)
        self.assertNotEqual(rc, 0)
        self.assertTrue(out['falhas'])
        self.assertTrue(out.get('acao_requerida'))
        self.assertIn('RECIBO_IMPLANTACAO_SINTETICO.json', pendentes(rd), 'a trava passou a ver 0 pendentes')

    def test_T_K4c_misleading_reverted_receipt_does_not_release_lock(self):
        """Um RECIBO_REVERSAO REVERTIDA com app_religado=false (o que a R2.1 gravava no K4c) não prova reversão."""
        rd = self.root / 'recibos'
        rd.mkdir()
        (rd / 'RECIBO_IMPLANTACAO_X.json').write_text(json.dumps(
            {'dry_run': False, 'status': 'CONCLUIDA', 'stamp': 'X', 'mudancas_iniciadas': ['substituir_arquivos'],
             'passos': {}}), encoding='utf-8')
        (rd / 'RECIBO_REVERSAO_Y.json').write_text(json.dumps(
            {'dry_run': False, 'status': 'REVERTIDA', 'falhas': [], 'app_religado': False, 'recibo_implantacao_stamp': 'X',
             'recibo_implantacao': str(rd / 'RECIBO_IMPLANTACAO_X.json'),
             'acao_requerida': 'O app NÃO foi religado (estado possivelmente misto: [alvos_divergentes:1])'}),
            encoding='utf-8')
        self.assertEqual(pendentes(rd), ['RECIBO_IMPLANTACAO_X.json'])

    def test_T_K4c_clean_reversal_still_releases_lock(self):
        """Controle: a reversão boa religa, dá REVERTIDA/ok e a trava libera."""
        rp, alvo, cand, rd = montar_reversao(self.root)
        fake = FakeBackend(rodando=True)
        with mock.patch.object(reverter, 'backend_de', lambda cfg: fake):
            rc, out = rodar_main(reverter, ['--recibo', str(rp)])
        self.assertEqual((out['status'], out['ok'], out['app_religado']), ('REVERTIDA', True, True), out)
        self.assertIsNone(out.get('acao_requerida'))
        self.assertEqual(alvo.read_bytes(), b'original\n')
        self.assertEqual(pendentes(rd), [])


class ReverterK4b(Tmp):
    def test_T_K4b_target_locked_after_check_fills_action(self):
        """Cenário do revisor: lock EXCLUSIVO num alvo depois de conferir_alvos OK: a conferência antes de religar
        levanta; o app não é religado e a ação vem preenchida (na R2.1 vinha null)."""
        rp, alvo, cand, rd = montar_reversao(self.root)
        fake = FakeBackend(rodando=True)
        trava = {}

        def blocos_e_trava(self_rev):
            trava['t'] = TravaExclusiva(alvo)
            return {'status_forcado': 'PULADO', 'nota': 'teste'}
        try:
            with mock.patch.object(reverter, 'backend_de', lambda cfg: fake), \
                    mock.patch.object(reverter.Reversao, 'restaurar_blocos', blocos_e_trava):
                rc, out = rodar_main(reverter, ['--recibo', str(rp)])
        finally:
            if 't' in trava:
                trava['t'].soltar()
        self.assertIn('t', trava)
        self.assertNotIn('start', fake.calls)
        self.assertTrue(out['status'].startswith('FALHOU_EM_'), out['status'])
        self.assertFalse(out['ok'])
        self.assertTrue(out.get('acao_requerida'), 'acao_requerida null com o app não religado')
        self.assertIn('reverter.py', out['acao_requerida'])
        self.assertIn('RECIBO_IMPLANTACAO_SINTETICO.json', pendentes(rd))

    def test_T_K4b2_sem_reiniciar_is_explicit_status_with_action(self):
        rp, alvo, cand, rd = montar_reversao(self.root)
        fake = FakeBackend(rodando=True)
        with mock.patch.object(reverter, 'backend_de', lambda cfg: fake):
            rc, out = rodar_main(reverter, ['--recibo', str(rp), '--sem-reiniciar'])
        self.assertEqual(alvo.read_bytes(), b'original\n')
        self.assertNotIn('start', fake.calls)
        self.assertEqual(out['status'], 'REVERTIDA_SEM_RELIGAR', out)
        self.assertIs(out['app_religado'], False)
        self.assertTrue(out.get('acao_requerida'))
        self.assertIn('Start-ScheduledTask', out['acao_requerida'])
        self.assertTrue(out['ok'])
        self.assertEqual(pendentes(rd), [], 'reversão limpa por escolha explícita libera a trava')


# ================================================================================================= K3r
class ReverterK3r(Tmp):
    def test_T_K3r_reverter_cannot_stop_app(self):
        """Cenário do revisor: implantação CONCLUIDA; o REVERTER encontra o stop sem efeito (o web sobrevive)."""
        rp, alvo, cand, rd = montar_reversao(self.root)
        fake = FakeBackend(rodando=True, stop_mata_web=False)
        with mock.patch.object(reverter, 'backend_de', lambda cfg: fake):
            rc, out = rodar_main(reverter, ['--recibo', str(rp)])
        rr = json.loads(Path(out['recibo']).read_text(encoding='utf-8'))
        self.assertEqual(out['status'], 'FALHOU_EM_parar_app')
        self.assertEqual(alvo.read_bytes(), cand, 'algo foi restaurado com o app vivo')
        self.assertNotIn('start', fake.calls)
        self.assertTrue(rr['passos']['parar_app'].get('tarefa_desabilitada_por_esta_execucao'))
        self.assertTrue(fake.enabled, 'a tarefa ficou DESABILITADA com o app v2 vivo')
        acao = out.get('acao_requerida') or ''
        self.assertNotIn('fica parado', acao, 'o recibo diz «fica parado» com o app vivo')
        self.assertIn('VIVO SEM SUPERVISOR', acao)
        self.assertIn('stop_iald_web.ps1', acao)
        self.assertEqual((fake.web, fake.sup), (1, 0))
        self.assertIn('RECIBO_IMPLANTACAO_SINTETICO.json', pendentes(rd))

    def test_T_K3r_task_disabled_by_operator_stays_disabled(self):
        """Controle: a tarefa que já estava desabilitada (pelo operador) não é reabilitada pelo reverter."""
        rp, alvo, cand, rd = montar_reversao(self.root)
        fake = FakeBackend(rodando=True, stop_mata_web=False)
        fake.enabled = False
        with mock.patch.object(reverter, 'backend_de', lambda cfg: fake):
            rc, out = rodar_main(reverter, ['--recibo', str(rp)])
        self.assertEqual(out['status'], 'FALHOU_EM_parar_app')
        self.assertFalse(fake.enabled)
        self.assertNotIn('enable', fake.calls)


# ================================================================================================= P8b
def _implantar_so_reinicio(root, fake):
    """O implantar real (main), com os passos 0-7 trocados por OK e o backend falso no passo 8."""
    cfgp, cfg = cfg_minima(root, gerir_processos=True, esperar_inicio_s=4)
    fake.enabled = False                                         # desabilitada pela própria implantação (passo 1)
    patches = [mock.patch.object(implantar, 'backend_de', lambda c: fake)]
    for nome in implantar.PASSOS:
        if nome in ('reiniciar_app', 'parar_app'):
            continue
        patches.append(mock.patch.object(implantar.Implantacao, nome, lambda self_imp: {}))

    def parar(self_imp):
        self_imp.recibo['mudancas_iniciadas'] = ['migracao', 'substituir_arquivos']
        return {'parado': True, 'tarefa_desabilitada_por_esta_execucao': True,
                'tarefa_antes': {'existe': True, 'habilitada': True, 'estado': 'Running'}}
    patches.append(mock.patch.object(implantar.Implantacao, 'parar_app', parar))
    with contextlib.ExitStack() as st:
        for p in patches:
            st.enter_context(p)
        rc, out = rodar_main(implantar, ['--config', str(cfgp)])
    rec = json.loads(Path(out['recibo']).read_text(encoding='utf-8'))
    return rc, out, rec


class ImplantarP8b(Tmp):
    def test_T_P8b_crash_loop_is_distinguished_in_receipt_and_output(self):
        rc, out, rec = _implantar_so_reinicio(self.root, FakeLaco(estavel=False))
        self.assertEqual(rc, 3, 'a saída 3 é por desenho')
        self.assertEqual(rec['status'], 'CONCLUIDA_AGUARDANDO_REINICIO')
        diag = rec.get('diagnostico_reinicio') or {}
        self.assertEqual(diag.get('leitura'), 'LACO_DE_QUEDA_PROVAVEL', rec.get('passos', {}).get('reiniciar_app'))
        self.assertEqual((out.get('diagnostico_reinicio') or {}).get('leitura'), 'LACO_DE_QUEDA_PROVAVEL')
        acao = rec.get('acao_requerida') or ''
        for trecho in ('COMO DISTINGUIR', 'ProcessId', 'CreationDate', 'LAÇO DE QUEDA', 'reverter.py'):
            self.assertIn(trecho, acao)

    def test_T_P8b_child_never_up_is_crash_loop(self):
        """O filho web morre antes de qualquer leitura (o que o ensaio P8b mostrou): também LACO, também rc 3."""
        rc, out, rec = _implantar_so_reinicio(self.root, FakeLaco(nunca=True))
        self.assertEqual(rc, 3, rec.get('acao_requerida'))
        self.assertEqual(rec['status'], 'CONCLUIDA_AGUARDANDO_REINICIO')
        self.assertEqual((rec.get('diagnostico_reinicio') or {}).get('leitura'), 'LACO_DE_QUEDA_PROVAVEL')
        self.assertIn('NENHUM filho web', rec.get('acao_requerida') or '')
        self.assertIn('COMO DISTINGUIR', rec.get('acao_requerida') or '')

    def test_T_P8b_slow_but_stable_is_read_as_slow(self):
        rc, out, rec = _implantar_so_reinicio(self.root, FakeLaco(estavel=True))
        self.assertEqual(rc, 3)
        self.assertEqual((rec.get('diagnostico_reinicio') or {}).get('leitura'), 'LENTO_PROVAVEL')
        self.assertIn('NÃO reverter', rec.get('acao_requerida') or '')
        self.assertIn('COMO DISTINGUIR', rec.get('acao_requerida') or '')


# ================================================================================================= N1c
class GuardN1Componentes(Tmp):
    N = 16000

    def _caminho(self):
        return os.sep.join([str(self.root)] + ['a'] * self.N + ['x.json'])

    def _tempo(self, fn, *a):
        t0 = time.perf_counter()
        try:
            r = fn(*a)
        except Exception as exc:  # noqa: BLE001 - a recusa visível também conta
            r = exc
        return time.perf_counter() - t0, r

    def test_G_N1c_path_reason_16000_components_refused_fast(self):
        dt, r = self._tempo(guard.path_reason, self._caminho(), [str(self.root)])
        self.assertLess(dt, 0.05, 'path_reason levou %.3f s' % dt)
        self.assertEqual(r, 'path_too_many_components')

    def test_G_N1c_read_allowed_file_16000_components_refused_fast(self):
        dt, r = self._tempo(sm.read_allowed_file, self._caminho())
        self.assertLess(dt, 0.05, 'read_allowed_file levou %.3f s' % dt)
        self.assertIsInstance(r, sm.ProtocolError)
        self.assertEqual(str(r), 'source_path_not_allowed:path_too_many_components')

    def test_G_N1c_dispatch_init_16000_components_refused_fast(self):
        store = (self.root / 'state').resolve()
        store.mkdir()
        req = {'operation': 'init', 'objective_file': self._caminho(), 'objective_sha256': '0' * 64, 'scope': SCOPE,
               'request_id': str(uuid.uuid4()), 'actor': ACTOR}
        dt, r = self._tempo(sm.dispatch, req, store, MemoryStore)
        self.assertLess(dt, 0.05, 'dispatch init levou %.3f s' % dt)
        self.assertIsInstance(r, sm.ProtocolError)
        self.assertIn('path_too_many_components', str(r))

    def test_G_N1c_too_long_refused(self):
        p = str(self.root / ('a' * 40000))
        self.assertEqual(guard.path_reason(p, [str(self.root)]), 'path_too_long')

    def test_G_N1c_ordinary_deep_path_not_refused_by_shape(self):
        """Controle: 40 componentes, nome benigno inexistente: nenhuma recusa (como antes)."""
        p = os.sep.join([str(self.root)] + ['pasta'] * 40 + ['nota.json'])
        self.assertIsNone(guard.path_reason(p, [str(self.root)]))


# ================================================================================================ M_DOC
class ManifestoDoc(unittest.TestCase):
    def test_M_DOC_tools_field_cites_real_sha(self):
        m = json.loads(MANIFESTO.read_text(encoding='utf-8'))
        errados = {}
        for f in m['ferramentas']:
            real = sha(Path(f['arquivo']).read_bytes())
            if real != f['sha256']:
                errados[Path(f['arquivo']).name] = (f['sha256'][:16], real[:16])
        self.assertEqual(errados, {}, 'ferramentas com sha citado diferente do arquivo')


if __name__ == '__main__':
    unittest.main()

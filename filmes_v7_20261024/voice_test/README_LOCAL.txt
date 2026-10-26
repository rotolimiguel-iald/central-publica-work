VOICE PREVIEW — isolated local experiment, not a film replacement

Original reference and SCRIPTS.json remain unchanged. The text passed to the
synthesizer is read verbatim from SCRIPTS.json. Generated audio is synthetic.
Human listening is required to judge voice similarity, pronunciation and style.

Models are downloaded by download_models.py using public GET requests with TLS
verification and no token. MODEL_DOWNLOADS.json records pinned revisions, local
SHA256 values and upstream LFS hashes. The personal voice is never read by that
downloader. Systran weights are preserved but unused in the final ASR route.

PyPI files.pythonhosted.org produced TLS EOF in Python, curl and PowerShell.
No verification was disabled. The initial venv and logs remain preserved.
Dependencies are supplied by the official conda-forge distribution instead;
micromamba is the portable official mamba-org executable. No global shell
initialization or Windows registry change is made. Source archives for pysox
and faster-whisper are pinned GitHub downloads; faster-whisper is not required
by the final pipeline. Qwen's official 0.1.1 wheel is installed without changing
its model implementation. Gradio/web UI is not used.

A short cache prefix was authorized after Windows long-path extraction failed:
C:\Temp\vp24
Isolated runtime:
C:\IALD\Central de Patentes\voice_tmp_20261024\e\python.exe
The original cache is preserved. SHORT_PREFIX_CACHE.json binds copied archives.
Actual package versions and runtime checks belong in ENVIRONMENT.json.

Run via the portable micromamba, with --no-rc --no-env, root-prefix C:\Temp\vp24,
run -p C:\IALD\Central de Patentes\voice_tmp_20261024\e python -B -X utf8
offline_preview.py --stage reference|synthesize|validate (or all).

offline_preview.py checks the current VOICE_PREVIEW lease for codex-video-audio
and performs a fresh project/check before inference. It sets offline HF modes,
disables token/telemetry use, hides CUDA, uses CPU with eight Torch threads and
installs a socket guard BEFORE audio/model imports. Guard self-test must pass.
This is a process-level guard, not a system-wide firewall. FFmpeg is called only
with local file arguments. No inference server, UI server or cloud TTS is used.

The local Whisper-small ASR chooses a 10–15 second reference using segment
boundaries near 12 seconds. The transcript is automatic, not audibly verified.
Qwen uses that transcript and the clipped audio. Both exact scripts are passed
to the same model. Raw float WAVs are preserved. Delivery WAVs are PCM24/24kHz,
normalized using measured loudness, with sample peak and true peak checked.
Output ASR and normalized word error rates are recorded; ASR is not a guarantee
of perceptual pronunciation or speaker likeness. LOCAL_ONLY_MANIFEST.json is
created only after both WAVs have been measured and transcribed.

PROGRESS.json is the current compact status; logs preserve prior failures.
Do not infer successful audio generation from installed packages or model files.
Do not publish the personal reference, its transcript, caches or authorization.

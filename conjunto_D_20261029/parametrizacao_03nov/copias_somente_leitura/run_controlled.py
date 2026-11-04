"""Single owned process group, private descriptors, monotonic local wall cap."""
import argparse,json,os,signal,subprocess,sys,time,resource
from pathlib import Path
from datetime import datetime,timezone
from registration_guard import (checked_registration,time_guard,output_path,sha,load_jobs,
    positive,integer,publish_new,authorize_event)


def group_exists(pgid):
    try:os.killpg(pgid,0);return True
    except ProcessLookupError:return False


def cleanup_group(child,grace=5.):
    """Leader termination does not imply worker termination; never kill own group."""
    pgid=child.pid
    if pgid==os.getpgrp() or pgid<=1:raise RuntimeError('Refusing non-owned group')
    sent=[]
    if group_exists(pgid):
        try:os.killpg(pgid,signal.SIGTERM);sent.append('SIGTERM')
        except ProcessLookupError:pass
    until=time.monotonic()+grace
    while group_exists(pgid) and time.monotonic()<until:
        child.poll();time.sleep(.05)
    if group_exists(pgid):
        try:os.killpg(pgid,signal.SIGKILL);sent.append('SIGKILL')
        except ProcessLookupError:pass
    try:child.wait(timeout=2)
    except subprocess.TimeoutExpired:raise RuntimeError('Owned leader not reaped')
    # A short-lived zombie can retain PGID until init reaps it; never call this success.
    until=time.monotonic()+2
    while group_exists(pgid) and time.monotonic()<until:time.sleep(.05)
    return dict(signals=sent,group_absent=not group_exists(pgid),pgid=pgid)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--job',required=True);args=parser.parse_args()
    if os.name!='posix':raise RuntimeError('WSL POSIX controller required')
    reg,digest=checked_registration();jobs=load_jobs(reg,digest)
    if args.job not in jobs:raise ValueError('Unknown job')
    cfg=jobs[args.job];authorize_event(reg,cfg['event'],cfg['mode'])
    workers=integer(cfg['sampler']['workers'],'workers')
    if workers>28:raise ValueError('Worker cap exceeded')
    wall=positive(cfg['wall_budget_seconds'],'wall_budget_seconds')
    if cfg['mode']=='calibration' and wall>10*3600:raise ValueError('Pilot wall cap 10h')
    if cfg['privacy_mode']!='procedural_same_host':raise ValueError('Unknown privacy mode')
    stop=min(time_guard(reg).timestamp(),time.time()+wall)
    if stop-time.time()<12:raise TimeoutError('Insufficient time for controlled cleanup')
    out=output_path(cfg['output_directory_name']);out.mkdir(mode=0o700)
    context=dict(registration_sha256=digest,job=args.job,controller_pid=os.getpid(),
      controller_start_ticks=Path(f'/proc/{os.getpid()}/stat').read_text().rsplit(')',1)[1].split()[19],
      created_utc=datetime.now(timezone.utc).isoformat(),stop_utc=datetime.fromtimestamp(stop,timezone.utc).isoformat(),
      config_sha256=__import__('hashlib').sha256(json.dumps(cfg,sort_keys=True,allow_nan=False).encode()).hexdigest(),
      privacy='PROCEDURAL_SAME_HOST_NOT_SEPARATE_CUSTODIAN')
    publish_new(out/'LAUNCH_CONTEXT.json',context)
    command=[sys.executable,'-B',str(Path(__file__).with_name('pe_runner.py')),'--job',args.job,
             '--launch-context',str(out/'LAUNCH_CONTEXT.json')]
    before=resource.getrusage(resource.RUSAGE_CHILDREN);started=time.time();mono=time.monotonic()
    local_stop=mono+(stop-started)-12 # >=9s cleanup + metadata margin inside shared deadline
    killed=False;child=None;cleanup=None;error=None
    previous={}
    def interrupted(signum,frame):raise InterruptedError('Controller interrupted '+str(signum))
    for sig in (signal.SIGTERM,signal.SIGINT):previous[sig]=signal.signal(sig,interrupted)
    try:
        with (out/'PRIVATE.log').open('xb') as log:
            os.chmod(out/'PRIVATE.log',0o600)
            child=subprocess.Popen(command,stdout=log,stderr=subprocess.STDOUT,start_new_session=True,
              env={**os.environ,'OMP_NUM_THREADS':'1','OPENBLAS_NUM_THREADS':'1','MKL_NUM_THREADS':'1','NUMEXPR_NUM_THREADS':'1'})
            try:
                while child.poll() is None:
                    if time.monotonic()>=local_stop or time.time()>=stop-12:killed=True;break
                    time.sleep(.2)
            finally:cleanup=cleanup_group(child)
    except BaseException as exc:
        error=type(exc).__name__
        if child is not None and cleanup is None:cleanup=cleanup_group(child)
    finally:
        for sig,handler in previous.items():signal.signal(sig,handler)
    after=resource.getrusage(resource.RUSAGE_CHILDREN)
    status='CHILD_COMPLETED_REQUIRES_REVIEW'
    if killed:status='BUDGET_STOPPED_PARTIAL_NOT_POSTERIOR'
    elif error or child is None or child.returncode!=0:status='CHILD_FAILED_OR_INTERRUPTED'
    if not killed and not error and child is not None and child.returncode==3 and (out/'ANALYST_STATUS.json').exists():
        partial=json.loads((out/'ANALYST_STATUS.json').read_bytes())
        if partial.get('accepted') is False and str(partial.get('status','')).startswith('PARTIAL_'):status=partial['status']
    if cleanup and not cleanup['group_absent']:status='OWNED_GROUP_CLEANUP_UNCONFIRMED'
    result=dict(status=status,job=args.job,registration_sha256=digest,started_utc=context['created_utc'],
      finished_utc=datetime.now(timezone.utc).isoformat(),wall_seconds=time.monotonic()-mono,
      children_user_cpu_seconds=after.ru_utime-before.ru_utime,children_system_cpu_seconds=after.ru_stime-before.ru_stime,
      returncode=child.returncode if child else None,error_type=error,cleanup=cleanup,
      private_log_sha256=sha(out/'PRIVATE.log') if (out/'PRIVATE.log').exists() else None,
      private_log_bytes=(out/'PRIVATE.log').stat().st_size if (out/'PRIVATE.log').exists() else 0,
      blind=cfg['mode']=='blind_test',log_policy='RAW_LOGS_RESULTS_PRIVATE_PROCEDURAL_SAME_HOST',
      controller_code_sha256=sha(Path(__file__)))
    publish_new(out/'CONTROLLER.json',result)
    print(json.dumps(result,allow_nan=False))
    if status!='CHILD_COMPLETED_REQUIRES_REVIEW':raise SystemExit(2)


if __name__=='__main__':main()

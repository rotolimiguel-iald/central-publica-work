import json, subprocess, sys
ref = sys.argv[1]
req = json.dumps({"operation": "project", "reference": ref}, ensure_ascii=False).encode("utf-8")
p = subprocess.run([r"C:\Python314\python.exe", "-X", "utf8", r"C:\IALD\MEMORIA_IALD\session_memory.py"], input=req, capture_output=True, timeout=180)
print("rc", p.returncode)
print(p.stdout.decode("utf8", "replace")[:3000])
print("stderr:", p.stderr.decode("utf8", "replace")[:1500])

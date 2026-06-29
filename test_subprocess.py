import subprocess, tempfile, os

tmp = tempfile.NamedTemporaryFile(delete=False, suffix='valid.proof')
tmp.write(b'test')
tmp_path = tmp.name
tmp.close()

engine = os.path.abspath('./bin/verifier_cli.bat')
print(f'Engine: {engine}')
print(f'Engine exists: {os.path.exists(engine)}')
print(f'File: {tmp_path}')

r = subprocess.run(
    f'"{engine}" "{tmp_path}"',
    capture_output=True, text=True, shell=True, timeout=10
)
print(f'Return code: {r.returncode}')
print(f'Stdout: [{r.stdout}]')
print(f'Stderr: [{r.stderr}]')

os.unlink(tmp_path)

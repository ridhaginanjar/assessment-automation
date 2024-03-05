import subprocess


def run_npm_install(project_path):
    sub = subprocess.run(["npm", "install"], capture_output=True, cwd=project_path)
    if sub.returncode != 0:
        print(sub.stderr.decode().strip())


def run_main_js(main_js_path):
    sub = subprocess.check_output(["node", main_js_path])
    if sub.returncode != 0:
        print(sub.stderr.decode().strip())


def stop_server():
    # kill -9 17890 $(lsof -t -i:5000)
    sub = subprocess.run(['kill', '-9 $(lsof -t -i tcp)'])
    if sub.returncode != 0:
        print(sub.stderr.decode().strip())

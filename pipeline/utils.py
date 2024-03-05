import subprocess
import logging
import re

logging.basicConfig(format='%(asctime)s | %(levelname)s | %(lineno)d: %(message)s', level=logging.INFO)


def run_npm_install(project_path):
    sub = subprocess.run(["npm", "install"], capture_output=True, cwd=project_path)
    if sub.returncode != 0:
        logging.error(sub.stderr.decode().strip())


def run_main_js(main_js_path, project_path):
    sub = subprocess.run(["npm", "run", "start"], capture_output=True, cwd=project_path)
    if sub.returncode != 0:
        logging.error(sub.stderr.decode().strip())
        err_message = sub.stderr.decode().strip()
        pattern = re.search(r"start", err_message)
        if pattern:
            sub = subprocess.run(["node", main_js_path])
            if sub.returncode != 0:
                logging.error(sub.stderr.decode().strip())


def stop_server():
    # kill -9 17890 $(lsof -t -i:5000)
    sub = subprocess.run(['kill', '-9 $(lsof -t -i tcp)'])
    if sub.returncode != 0:
        logging.error(sub.stderr.decode().strip())

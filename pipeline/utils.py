import subprocess
import socket
import time


def run_npm_install(project_path):
    sub = subprocess.run(["npm", "install"], capture_output=True, cwd=project_path)
    if sub.returncode != 0:
        print(sub.stderr.decode().strip())


def run_main_js(main_js_path):
    sub = subprocess.check_output(["node", main_js_path])
    if sub.returncode != 0:
        print(sub.stderr.decode().strip())


def stop_server():
    sub = subprocess.run(['kill', '-9 $(lsof -t -i tcp)'])
    if sub.returncode != 0:
        print(sub.stderr.decode().strip())


def checking_server():
    # Kill
    # kill -9 17890 $(lsof -t -i:5000)

    host = "localhost"
    port = 5000
    timeout = 5

    for i in range(timeout):
        try:
            with socket.create_connection((host, port), timeout=1):
                print("Server is running on port {}".format(port))
                return ""
        except ConnectionRefusedError as e:
            print(e)
            pass

        time.sleep(1)

    print("Server did not running on port 5000")
    stop_server()

    return "Kami tidak mendeteksi bahwa aplikasi berjalan pada Port 5000. Silakan cek kembali project kamu ya"
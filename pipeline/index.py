import os
import sys
import threading
import re
import requests
import traceback
import socket
import time
import logging
from bs4 import BeautifulSoup

import pipeline.contract as ct
import pipeline.checklist as cks
import pipeline.report as rpt
import pipeline.utils as utils

"""
    This script for logging
    Alternative for more specific log that will show the ouput into console (another: HTTP and file)

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(lineno)d: %(message)s'))

logger.addHandler(console_handler)
"""
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(lineno)d: %(message)s', level=logging.INFO)


def find_file(submission_path, file_name: str):
    """Find a file in the submission
    :param:
        submission_path: Path to submissions directory
        file_name: Name of the file to find
    :return:
         file_path, comment variable which contains the path to directory and the comment if not found
    """
    for root, dirs, files in os.walk(submission_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            logging.info(f"Found file: {file_path}")
            return file_path, ""

    logging.warning(f"{file_name} tidak ditemukan di project")
    return "", f"{file_name} tidak ditemukan di project submission kamu"


def find_comment(file_path, student_id):
    """ Find a comment containing the student ID in a file
    :param:
        file_path: Path to submissions directory
        student_id: The student ID to search for in the file
    :return:
        A string containing error message if not found, otherwise an empty string
    """
    with open(file_path, "r") as f:
        content = f.read()
        pattern = re.search(rf"//.*?{student_id}|/\*\n.*?{student_id}", content)
        if not pattern:
            logging.warning(f"{student_id} tidak ditemukan di main.js")
            return "Kami tidak menemukan student_id kamu nih di file main.js"

        logging.info(f"{student_id} ditemukan di main.js")
        return ""


def root_serving_html():
    """ Check the content type of the root served by the application which is should HTML
    :return:
        A string containing error message if not found, otherwise an empty string
    """
    response = requests.get("http://localhost:5000")
    header = response.headers.get("Content-Type")
    if not re.search(rf"^text/html", header):
        logging.warning(f"Content pada root BUKAN html")
        return "Kami mendeteksi content pada root bukanlah html, melainkan {}".format(header)

    logging.info("Content pada root MERUPAKAN html")
    return ""


def h1_contains_student_id(student_id):
    """Check if element h1 contains a student_id string
    :param:
        student_id: String with student_id
    :return:
        A string containing error message if not found, otherwise an empty
    """
    response = requests.get("http://localhost:5000")
    soup = BeautifulSoup(response.content, "html.parser")
    h1 = soup.find_all("h1")
    for i in range(len(h1)):
        if not re.search(rf"<h1>{student_id}</h1>", str(h1[i])):
            logging.warning(f"element h1 dengan student id tidak ditemukan")
            return "Kami tidak menemukan element h1 yang di-isi dengan student id"

    logging.info("element h1 dengan student id berhasil ditemukan")
    return ""


def checking_server():
    """Check if server is up and running in port 5000
    :return:
        A string containing error message if not found, otherwise an empty string
    """
    host = "localhost"
    port = 5000
    timeout = 5

    for i in range(timeout):
        try:
            with socket.create_connection((host, port), timeout=1):
                logging.info(f"server is up and running in port {port}")
                return ""
        except ConnectionRefusedError as e:
            print(e)
            pass

        time.sleep(2)

    logging.warning(f"server is NOT running in port {port}")
    return "Kami tidak mendeteksi bahwa aplikasi berjalan pada Port 5000. Silakan cek kembali project kamu ya"


def unexpected_error(err):
    """
    NOT USED BUT KEEP SAVED FOR DOCUMENTATION

    Exception for unexpected errors.
    Example output of sys.exc_info -> <class 'AttributeError'>, AttributeError("module 'requests' has no attribute 'et'"), <traceback object at 0x7f259c815b40>
    :param err:
    :return:
    """
    # Get error info in the exact line of code that call the function
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_info = ''.join(traceback.format_tb(exc_traceback))

    # Contains traceback info
    frame = exc_traceback.tb_frame
    filename = frame.f_code.co_filename
    lineno = frame.f_lineno
    func_name = frame.f_code.co_name

    utils.stop_server()

    return err


def main(params: str):
    """
    Main function for the pipeline to check the whole submission directory
    :param params:
    :return:
    """
    try:
        submission_path = params.s
        output_path = params.o

        get_config = ct.read_config(submission_path)

        c = cks.Checklists()
        c.new_checklist()

        package_path, comment = find_file(submission_path, "package.json")
        project_path = package_path.replace("/package.json", "")
        if not comment:
            c.package_json_exists.status = True
        c.package_json_exists.comment = comment

        main_js_path, comment = find_file(submission_path, "main.js")
        if not comment:
            c.main_js_exists.status = True
        c.main_js_exists.comment = comment

        if package_path and main_js_path:
            utils.run_npm_install(project_path)

            thread = threading.Thread(target=utils.run_main_js, args=(main_js_path,))
            thread.start()

            comment = checking_server()
            if not comment:
                c.serve_in_port_5000.status = True
            c.serve_in_port_5000.comment = comment

            if c.serve_in_port_5000.status:
                comment = root_serving_html()
                if not comment:
                    c.root_serving_html.status = True
                c.root_serving_html.comment = comment

                if c.root_serving_html.status:
                    comment = h1_contains_student_id(get_config['submitter_id'])
                    if not comment:
                        c.html_contain_h1_element_with_student_id.status = True
                    c.html_contain_h1_element_with_student_id.comment = comment

        if main_js_path:
            comment = find_comment(main_js_path, get_config['submitter_id'])
            if not comment:
                c.main_js_has_student_id_comment.status = True
            c.main_js_has_student_id_comment.comment = comment

        report = rpt.generate_report(c, get_config['submitter_name'])
        ct.write_json(output_path, report)

        utils.stop_server()
    except Exception as e:
        print(e)
        utils.stop_server()


"""
Error Handling:
- logging
- cleaning code
"""



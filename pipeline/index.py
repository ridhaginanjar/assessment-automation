import os
import threading
import re
import requests
from bs4 import BeautifulSoup

import pipeline.contract as ct
import pipeline.checklist as cks
import pipeline.report as rpt
import pipeline.utils as utils


def find_file(submission_path, file_name: str):
    """
    Find a file in the submission
    :param submission_path:
    :param file_name:
    :return file_path, comment:
    """

    comment = ""
    file_path = ""

    for root, dirs, files in os.walk(submission_path):
        if file_name in files:
            file_path = os.path.join(root, file_name)
            break
    if not file_path:
        comment = f"{file_name} tidak ditemukan di project submission kamu"

    return file_path, comment


def find_comment(file_path, student_id):
    with open(file_path, "r") as f:
        content = f.read()
        rgx = re.search(rf"//.*?{student_id}|/\*\n.*?{student_id}", content)
        if not rgx:
            return "Kami tidak menemukan student_id kamu nih di file main.js"

        return ""


def root_serving_html():
    response = requests.get("http://localhost:5000")
    header = response.headers.et("Content-Type")
    result = re.search(rf"^text/html", header)
    if result:
        return ""
    return "Kami mendeteksi content pada root bukanlah html, melainkan {}".format(header)


def h1_contains_student_id(student_id):
    response = requests.get("http://localhost:5000")
    soup = BeautifulSoup(response.content, "html.parser")
    h1 = soup.find_all("h1")

    for i in range(len(h1)):
        result = re.search(rf"^<h1>{student_id}</h1>", str(h1[i]))
        if result:
            return ""
    return "Kami tidak menemukan element h1 yang di-isi dengan student id "


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

        # Check Package.json
        package_path, comment = find_file(submission_path, "package.json")
        project_path = package_path.replace("/package.json", "")
        if not comment:
            c.package_json_exists.status = True
        c.package_json_exists.comment = comment

        # Check main.js
        main_js_path, comment = find_file(submission_path, "main.js")
        if not comment:
            c.main_js_exists.status = True
        c.main_js_exists.comment = comment

        # Runs the program (Depends to main.js and Package.json)
        if package_path and main_js_path:
            # Check root with HTML (Depends to "Runs the program")
            utils.run_npm_install(project_path)

            # Check port 5000 (Depends to "Runs the program")
            thread = threading.Thread(target=utils.run_main_js, args=(main_js_path,))
            thread.start()

            comment = utils.checking_server()
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

            # Check h1 with student ID (Depends to "Runs Program")
            print(c.serve_in_port_5000.__dict__)

        # Check comment with student ID (Depends to "main.js exist")
        if main_js_path:
            comment = find_comment(main_js_path, get_config['submitter_id'])
            if not comment:
                c.main_js_has_student_id_comment.status = True
            c.main_js_has_student_id_comment.comment = comment

            print(c.main_js_has_student_id_comment.__dict__)

        report = rpt.generate_report(c, get_config['submitter_name'])
        ct.write_json(output_path, report)

        utils.stop_server()
    except Exception as e:
        print(e)
        utils.stop_server()


"""
Error Handling:
- unhandled error (logging for error)
"""



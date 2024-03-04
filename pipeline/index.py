import os
import threading
import asyncio

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


def main(params: str):
    """
    Main function for the pipeline to check the whole submission directory
    :param params:
    :return:
    """
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

        # Check h1 with student ID (Depends to "Runs Program")
        print(c.serve_in_port_5000.__dict__)

    # Check comment with student ID (Depends to "main.js exist")
    # if main_js_path:
    #     print("check ID")
    print(c.package_json_exists.__dict__)

    report = rpt.generate_report(c, get_config['submitter_name'])
    ct.write_json(output_path, report)


"""
Error Handling:
- stop server
- waitserver till up
- unhandled error (logging for error)
"""



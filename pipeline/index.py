import os

import pipeline.contract as ct
import pipeline.checklist as cks


def find_file(submission_path, file_name):
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

def main(params):
    submission_path = params.s
    output_path = params.o

    report_dic = {
        "checklist": [],
        "message": ""
    }

    get_config = ct.read_config(submission_path)

    c = cks.Checklists()
    c.new_checklist()

    # Check Package.json
    package_path, comment = find_file(submission_path, "package.json")
    if not comment:
        c.checkPackageJson.status = True
    c.checkPackageJson.comment = comment

    # Check main.js
    mainjs_path, comment = find_file(submission_path, "main.js")
    if not comment:
        c.checkMainJS.status = True
    c.checkMainJS.comment = comment

    # Runs the program (Depends to main.js and Package.json)

    # Check comment with student ID (Depends to "Runs the program")

    # Check root with HTML (Depends to "Runs the program")

    # Check port 5000 (Depends to "Runs the program")

    # Check h1 with student ID (Depends to "Runs Program")

    ct.write_json(output_path, report_dic)



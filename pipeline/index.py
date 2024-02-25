import os

import pipeline.contract as ct
import pipeline.checklist as cks


def find_package(submission_path, c):
    comment = ""
    package_path = ""

    for root, dirs, files in os.walk(submission_path, topdown=False):
        if "package.json" in files:
            package_path = os.path.join(root, "package.json")
            break
    if not package_path:
        comment = "package.json tidak ditemukan nih"

    return package_path, comment


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
    package_path, comment = find_package(submission_path, c)
    if not comment:
        c.checkPackageJson.status = True
    c.checkPackageJson.comment = comment


    # Check main.js

    # Runs the program (Depends to main.js and Package.json)

    # Check comment with student ID (Depends to "Runs the program")

    # Check root with HTML (Depends to "Runs the program")

    # Check port 5000 (Depends to "Runs the program")

    # Check h1 with student ID (Depends to "Runs Program")

    ct.write_json(output_path, report_dic)



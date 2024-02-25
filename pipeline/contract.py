import os
import json


def read_config(submission_path):
    """
    Read auto-review-config.json

    :param submission_path:
    :return submitter information e.g {'submitter_name': 'John Doe', 'submitter_id': 123456, 'course_id': 123,
    'quiz_id': 1234}:
    """
    config_json = os.path.join(submission_path, "auto-review-config.json")
    try:
        with open(config_json, "r") as auto_config:
            config_json = json.load(auto_config)
            return config_json
    except FileNotFoundError:
        print("auto-review-config.json not found")


def write_report(output_path, report_dic):
    """
    Write dictionary to be JSON file
    :param output_path:
    :param report_dic:
    """
    json_path = os.path.join(output_path, "report.json")

    with open(json_path, "w") as report_file:
        json.dump(report_dic, report_file, indent=4)

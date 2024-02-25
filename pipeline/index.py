import os
import json


def read_config(submission_path):
    config_json = os.path.join(submission_path, "auto-review-config.json")
    try:
        with open(config_json, "r") as auto_config:
            config_json = json.load(auto_config)
            return config_json
    except FileNotFoundError:
        print("auto-review-config.json not found")


def main(params):
    submission_path = params.s
    output_path = params.o

    auto_review_config = read_config(submission_path)
    print(auto_review_config)

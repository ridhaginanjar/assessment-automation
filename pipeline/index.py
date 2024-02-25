import pipeline.contract as ct


def main(params):
    submission_path = params.s
    output_path = params.o

    report_dic = {
        "checklist": [],
        "message": ""
    }

    get_config = ct.read_config(submission_path)
    print(get_config['submitter_name'])

    ct.write_report(output_path, report_dic)



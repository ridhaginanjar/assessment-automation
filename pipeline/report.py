def create_report(checklists):
    checklist_completed = []
    messages = []
    for keys,values in checklists.__dict__.items():
        status = values.status
        comment = values.comment

        if status:
            checklist_completed.append(keys)
        if comment:
            messages.append("<li>" + comment + "</li>")

    return {
        "checklistCompleted": checklist_completed,
        "messages": messages
    }


def is_submission_passed(report):
    return len(report["checklistCompleted"]) == 6


def generate_template(report, username):
    if is_submission_passed(report):
        return f"Selamat! <b>{username}</b> kamu sudah telah lolos submission ini."

    result = ''.join(report["messages"])
    return f"Hi <b>{username}</b>, masih terdapat beberapa kesalahan nih, beriku beberapa kesalahannya <ul>{result}</ul>. Silakan perbaiki ya"


def generate_report(checklists, username):
    report = create_report(checklists)
    report['messages'] = generate_template(report, username)
    print(report)
    return report

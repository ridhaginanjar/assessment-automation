def create_report(checklists):
    checklist_completed = []
    messages = []
    for keys,values in checklists.__dict__.items():
        status = values.status
        comment = values.comment

        if status:
            checklist_completed.append(keys)
        if comment:
            messages.append(comment)

    return {
        "checklistCompleted": checklist_completed,
        "messages": messages
    }


def generate_report(checklists, username):
    report = create_report(checklists)
    # print(report['messages'])
    return None

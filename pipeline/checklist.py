class Checklist:
    def __init__(self, status=False, comment=""):
        self.status = status
        self.comment = comment


class Checklists:
    def __init__(self):
        self.package_json_exists = Checklist()
        self.main_js_exists = Checklist()
        self.main_js_has_student_id_comment = Checklist()
        self.root_serving_html = Checklist()
        self.serve_in_port_5000 = Checklist()
        self.html_contain_h1_element_with_student_id = Checklist()

    def new_checklist(self):
        """
        Create a new checklist via instance class Checklist
        :return Checklist instances:
        """
        self.package_json_exists = Checklist(False, "")
        self.main_js_exists = Checklist(False, "")
        self.main_js_has_student_id_comment = Checklist(False, "")
        self.root_serving_html = Checklist(False, "")
        self.serve_in_port_5000 = Checklist(False, "")
        self.html_contain_h1_element_with_student_id = Checklist(False, "")


#
# # Exploring Method
# # Saved for later
#
# c = Checklists()
# c.new_checklist()
#
#
# def package_true():
#     c.package_json_exists.status = False
#     c.package_json_exists.comment = "hey"
#
#
# package_true()
#
#
# def mainjs_ex():
#     c.main_js_exists.status = True
#     c.main_js_exists.comment = ""
#
#
# mainjs_ex()
#
# message = []
# checklists_ye = []

# for keys, values in c.__dict__.items():
#     comment = values.comment
#     status = values.status
#     if comment:
#         message.append(comment)
#     if status:
#         checklists_ye.append(keys)
#     print(values.comment)
#     print(values.status)
#     # print(keys, values)
#
# print(message)
# print(checklists_ye)
# # print(c.checkPackageJson.status, c.checkPackageJson.comment)
# # print(c.checkMainJS.status, c.checkMainJS.comment)


class Checklist:
    def __init__(self, status=False, comment=""):
        self.status = status
        self.comment = comment


class Checklists:
    def __init__(self):
        self.checkPackageJson = Checklist()
        self.checkMainJS = Checklist()

    def new_checklist(self):
        """
        Create a new checklist via instance class Checklist
        :return Checklist instances:
        """
        self.checkPackageJson = Checklist(False, "")
        self.checkMainJS = Checklist(False, "")


"""
# Exploring Method
# Saved for later

c = Checklists()
c.new_checklist()


def package_true():
    c.checkPackageJson.comment = "hey"
    return c.checkPackageJson.comment


package_true()

for key, value in c.__dict__.items():
    for keys, values in value.__dict__.items():
        print(keys, values)
    print(key, value)

print(c.checkPackageJson.status, c.checkPackageJson.comment)
print(c.checkMainJS.status, c.checkMainJS.comment)

"""
COMMANDS = {
    "1": "1 Add tip",
    "2": "2 List tips",
    "3": "3 Modify tip",
    "4": "4 Remove tip",
    "5": "5 Search tip",
    "6": "6 Mark tip as read",
    "7": "7 Cycle filters",
    "h": "h Help",
    "x": "x Quit"
}

HELP= {
    "1": "1 Add tip, tip can be added if name is not empty and url is valid",
    "2": "2 List tips, lists all tips",
    "3": "3 Modify tip, modify name/ url or both based on id",
    "4": "4 Remove tip, removes tip based on id",
    "5": "5 Search tip, search for a certain tip in database",
    "6": "6 Mark tip as read, option to mark a tip with read",
    "7": "7 Cycle filters, modify filters determining what tips are displayed",
    "h": "h Help",
    "x": "x Quit, exit reading-tip library"
}

FILTERS = {
    "ALL": "all",
    "READ": "read",
    "NOT READ": "not read"
}

class Menu:
    def __init__(self, io, tip_service, color_message):
        self.io = io
        self.tip_service = tip_service
        self.filters = "ALL"
        self.color_message = color_message

    def print_commands(self):
        self.io.write("")
        for command in COMMANDS:
            self.io.write(self.color_message.cyan(COMMANDS[command]))

    def print_help(self):
        for help_info in HELP:
            self.io.write(HELP[help_info])

    def get_help(self):
        help_messages = []
        for help_info in HELP:
            help_messages.append(HELP[help_info])

        return help_messages

    def run(self):
        self.io.write("Welcome dear reader")
        self.print_commands()

        while True:
            self.io.write(self.color_message.yellow(f"\nYou are seeing {self.filters} tips"))
            command = self.io.read(self.color_message.cyan("Command: "))
            if not command in COMMANDS:
                self.io.write(self.color_message.cyan("Invalid command"))
                self.print_commands()

            if command == "1":
                name = self.io.read("name: ")
                url = self.io.read("url: ")
                if len(url) == 0 or url[0:4] != "www." or url[4:].count(".") != 1:
                    self.io.write(self.color_message.red("Invalid url"))
                    url = self.io.read("url: ")
                try:
                    self.tip_service.create(name, url)
                except Exception as e:
                    self.io.write(self.color_message.red(e))

            if command == "2":
                tips = self.tip_service.get_all(FILTERS[self.filters])
                for tip in tips:
                    tip_id = tip[0]
                    name = tip[1].name
                    url = tip[1].url
                    self.io.write(f"id:{tip_id} {name}, {url}")

            if command == "3":
                tip_id = self.io.read("Tip id to edit: ")
                print(self.tip_service.get_tip(tip_id).name)
                try:
                    old = self.tip_service.get_tip(tip_id)
                    name = self.io.read("New name (leave blank to keep old): ")
                    if len(name) == 0:
                        name = old.name
                    url = self.io.read("New url (leave blank to keep old): ")
                    if len(url) == 0:
                        url = old.url
                    self.tip_service.edit(tip_id, name, url)
                except Exception as e:
                    self.io.write(self.color_message.red(e))

            if command == "4":
                tip_id = self.io.read("Tip id to remove: ")
                try:
                    self.tip_service.remove_tip(tip_id)
                    self.io.write(self.color_message.green("Tip removed"))
                except Exception as e:
                    self.io.write(self.color_message.red(e))

            if command == "5":
                i = self.io.read("search: ")
                for tip in self.tip_service.get_close_matches(i, FILTERS[self.filters]):
                    tip_id = tip[0]
                    name = tip[1].name
                    url = tip[1].url
                    self.io.write(f"id:{tip_id} {name}, {url}")

            if command == "6":
                tip_id = self.io.read("tip id to mark: ")
                try:
                    old = self.tip_service.get_tip(tip_id)
                    if old.read == 0:
                        read = 1
                    else:
                        read = 0
                    self.tip_service.mark_as_read(read, tip_id)
                except Exception as e:
                    self.io.write(self.color_message.red(e))

            if command == "7":
                if self.filters == "ALL":
                    self.filters = "NOT READ"
                elif self.filters == "NOT READ":
                    self.filters = "READ"
                elif self.filters == "READ":
                    self.filters = "ALL"

            if command == "h":
                self.print_help()

            if command == "x":
                break

            self.io.write("")
            self.print_commands()

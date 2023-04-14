from requests import get, exceptions


class Registry:
    def __init__(self, url):
        self.url = url

    def connect(self):
        try:
            data = get(self.url + "/v2/_catalog")
            print(data.text)
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def get_help(self):
        print("""
        exit - Either CTRL+C or type this to exit\n
        clear - Clears the screen\n
        help - Print this message
        """)

    def exit_program(self):
        exit(0)

    def clear_screen(self):
        from os import system, name
        if name == "nt":
            system("cls")
        else:
            system("clear")

    def command_handler(self, cmd):
        match cmd:
            case "help":
                self.get_help()
            case "clear":
                self.clear_screen()
            case "exit":
                self.exit_program()



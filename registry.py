from requests import get, exceptions


class Registry:
    def __init__(self, url):
        self.url = url
        self.image_name = None

    def connect(self):
        try:
            data = get(self.url + "/v2/_catalog")
            print(data.text)
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def get_repo_images(self):
        try:
            data = get(self.url + "/v2/_catalog")
            print(data.text)
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def get_help(self):
        print("""
        get_images - get all images stored in registry\n
        set *image name* - set the image to inspect\n
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

    def set_image(self,cmd):
        self.image_name = cmd.split(" ")[1]
        print("Image to inspect is set to",self.image_name)

    def command_handler(self, cmd):
        match cmd:
            case "get_images":
                self.get_repo_images()
            case "help":
                self.get_help()
            case "clear":
                self.clear_screen()
            case "exit":
                self.exit_program()

        args = cmd.split(" ")[1:]
        cmd = cmd.split(" ")[0]
        if cmd == "set":
            self.image_name = args[0]
            print("Setting image to", self.image_name)




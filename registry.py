from requests import get, delete, head, exceptions
from os import system, name
import json


class Registry:
    def __init__(self, url):
        self.url = url
        self.image_name = None

    def connect(self):
        try:
            data = get(self.url + "/v2/")
            if data.text is not None:
                print("Connected to", self.url)
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def get_repo_images(self):
        try:
            data = get(self.url + "/v2/_catalog")
            json_object = json.loads(data.text)
            images = json_object["repositories"]
            if len(images) == 0:
                print("No images are in the registry")
            else:
                for i in range(len(images)):
                    print("\t" + str(i + 1) + ".", images[i])
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def list_tags(self):
        try:
            if self.image_name is not None:
                data = get(self.url + "/v2/" + self.image_name + "/tags/list")
                json_object = json.loads(data.text)
                tags = json_object["tags"]
                for i in range(len(tags)):
                    print("\t" + str(i + 1) + ".", tags[i])
            else:
                print("No image name set")
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def get_image_hash(self,args):
        data = head(self.url+"/v2/"+self.image_name+"/manifests/"+args[0])
        digest = data.headers["Docker-Content-Digest"]
        return digest

    def delete_tag(self, args):
        if len(args) == 0:
            print("Tag name has to be specified")
            return
        elif self.image_name is None:
            print("Set the image name")
            return
        data = get(self.url + "/v2/" + self.image_name + "/tags/list")
        json_object = json.loads(data.text)
        tags = json_object["tags"]
        if args[0] not in tags:
            print("Tag does not exist in tag list")
            return
        try:
            digest = self.get_image_hash(args)
            data = delete(self.url + "/v2/" + self.image_name + "/manifests/" + digest)
            print("Tag",args[0],"has been deleted")
            data = get(self.url + "/v2/" + self.image_name + "/manifests/" + args[0])
            json_object = json.loads(data.text)
            blobs = json_object["fsLayers"]
            for blob in blobs:
                blob_temp = blob["blobSum"]
                data = delete(self.url + "/v2/" + self.image_name + "/blobs/" + blob_temp)
                shrot_hash = blob_temp.split(":")[1]
                if data.status_code == 202:
                    print("Digest",shrot_hash[:4],"has been deleted")
                else:
                    print("Problem while deleting",blob_temp)
            return
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def get_manifests(self, args):
        if len(args) == 0:
            print("Tag name has to be specified")
            return
        try:
            if self.image_name is not None:
                data = get(self.url + "/v2/" + self.image_name + "/manifests/" + args[0])
                json_object = json.loads(data.text)
                layers = json_object["fsLayers"]
                return_layers = []
                for i in range(len(layers)):
                    blob = layers[i]["blobSum"]
                    return_layers.append(blob)
                    print("\t" + str(i + 1) + ".", blob, "\n")
                layers = set(return_layers)
                return layers
            else:
                print("No image name set")
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def get_help(self):
        print("""
        get_images - get all images stored in registry\n
        list_tags - list tags associated with the name of the image\n
        delete_tag <tag name> - delete the tag associated with the image\n
        get_manifests <tag name> - list all the manifests with the specified tag name\n
        set <image name> - set the image to inspect\n
        exit - Either CTRL+C or type this to exit\n
        clear - Clears the screen\n
        help - Print this message
        """)

    def exit_program(self):
        exit(0)

    def clear_screen(self):
        if name == "nt":
            system("cls")
        else:
            system("clear")

    def set_image(self, args):
        try:
            data = get(self.url + "/v2/_catalog")
            image = args[0]
            data = data.text
            if data.find(image) == -1:
                print("Image does not exist in registry")
            else:
                self.image_name = image
                print("Image to inspect is set to", self.image_name)
        except (exceptions.HTTPError, exceptions.ConnectionError) as error:
            print(error.args[0])

    def command_handler(self, cmd):
        match cmd:
            case "list_tags":
                self.list_tags()
                return
            case "get_images":
                self.get_repo_images()
                return
            case "help":
                self.get_help()
                return
            case "clear":
                self.clear_screen()
                return
            case "exit":
                self.exit_program()
                return

        args = cmd.split(" ")[1:]
        cmd = cmd.split(" ")[0]
        if cmd == "set":
            self.set_image(args)
        elif cmd == "get_manifests":
            self.get_manifests(args)
        elif cmd == "delete_tag":
            self.delete_tag(args)
        else:
            print("Command", cmd, "does not exist. Check the help menu by typing help")

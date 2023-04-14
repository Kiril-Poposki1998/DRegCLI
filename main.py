from registry import Registry
import argparse
import pyfiglet


def main():
    # Parse the url from arg parser
    parser = argparse.ArgumentParser(
        prog='DRegCLI',
        description='Easy way to navigate through docker registry v2 with cli',
        epilog='Made by Kiril Poposki')
    parser.add_argument('url')
    args = parser.parse_args()
    # Print the banner
    banner = pyfiglet.figlet_format("DRegCLI")
    print(banner)
    # See if the connection to the registry works
    reg = Registry(args.url)
    reg.connect()
    while True:
        try:
            input_cmd = input("cli>")
            reg.command_handler(input_cmd)
        except KeyboardInterrupt:
            print("\nExiting...")
            exit(0)


if __name__ == "__main__":
    main()

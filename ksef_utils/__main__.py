from argparse import Namespace, ArgumentParser
from ksef_utils.utils import KSEFUtils
from ksef_utils.cli import GenerateCertsCommand


class KeyGenHandler:
    @staticmethod
    def keygen(args):
        generate_certs_command = GenerateCertsCommand(
            args.identifier, args.identifier_type, args.working_directory
        )
        generate_certs_command.execute()

    @staticmethod
    def add_parser(subparsers):
        parser_keygen = subparsers.add_parser("keygen")
        parser_keygen.set_defaults(func=KeyGenHandler.keygen)
        parser_keygen.add_argument(
            "--identifier",
            type=str,
            help="Identifier",
            dest="identifier",
            required=True,
        )
        parser_keygen.add_argument(
            "--identifier_type",
            type=KSEFUtils.SerialNumberType,
            help="Identifier type, eg. NIP, PESEL",
            dest="identifier_type",
            required=True,
        )
        parser_keygen.add_argument(
            "--working_directory",
            type=str,
            help="Working directory",
            dest="working_directory",
            required=True,
        )


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Generating certs")
    subparsers = parser.add_subparsers(required=True)
    KeyGenHandler.add_parser(subparsers)
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    args.func(args)


if __name__ == "__main__":
    main()

from argparse import Namespace, ArgumentParser
from ksef_utils.utils import KSEFUtils
from ksef_utils.cli import GenerateCertsCommand


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Generating certs")
    parser.add_argument(
        "--identifier",
        type=str,
        help="Identifier",
        dest="identifier",
        required=True,
    )
    parser.add_argument(
        "--identifier_type",
        type=KSEFUtils.SerialNumberType,
        help="Identifier type, eg. NIP, PESEL",
        dest="identifier_type",
        required=True,
    )
    parser.add_argument(
        "--working_directory",
        type=str,
        help="Working directory",
        dest="working_directory",
        required=True,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    generate_certs_command = GenerateCertsCommand(
        args.identifier, args.identifier_type, args.working_directory
    )
    generate_certs_command.execute()


if __name__ == "__main__":
    main()

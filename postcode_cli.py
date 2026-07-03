"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import get_postcode_completions, validate_postcode


def parser_args():
    """Returns arguments required by the README.md."""
    pass


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-m', '--mode', choices=['validate', 'complete'])
    parser.add_argument('postcode', type=str)
    args = parser.parse_args()

    if args.mode == "validate":
        val = validate_postcode(args.postcode)
        if val is True:
            print(f"{args.postcode} is a valid postcode.")
        else:
            print(f"{args.postcode} is not a valid postcode.")
    elif args.mode == "complete":
        codes = get_postcode_completions(args.postcode)
        if codes is None or len(codes) == 0:
            print(f"No matches for {args.postcode}.")
        else:
            counter = 0
            for i in range(len(codes)):
                if counter < 5:
                    print(f"{codes[i]}")
                    counter += 1

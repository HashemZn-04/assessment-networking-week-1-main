"""A CLI application for interacting with the Postcode API."""

from argparse import ArgumentParser
from postcode_functions import get_postcode_completions, validate_postcode

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        '--mode', '-m', choices=['validate', 'complete'], required=True)
    parser.add_argument('postcode', type=str)
    args = parser.parse_args()
    postcode = args.postcode.strip().upper()
    if args.mode == "validate":
        val = validate_postcode(postcode)
        if val is True:
            print(f"{postcode} is a valid postcode.")
        else:
            print(f"{postcode} is not a valid postcode.")
    elif args.mode == "complete":
        codes = get_postcode_completions(postcode)
        if codes is None or len(codes) == 0:
            print(f"No matches for {postcode}.")
        else:
            counter = 0
            for i in range(len(codes)):
                if counter < 5:
                    print(f"{codes[i]}")
                    counter += 1

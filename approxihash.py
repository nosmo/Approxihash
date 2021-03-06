#!/usr/bin/env python3

import argparse
import hashlib
import sys
import json
import itertools

AVAILABLE_HASH_TYPES = ["md5", "sha1", "sha256", "sha384", "sha512", "ALL"]

class GeneratedHash(object):

    def __init__(self, data_dict, hash_types):
        """ Create a new GeneratedHash object.

        Args:
         data_dict: a dict of string:string mappings only
        Returns:
         Nothing
        """
        self.data_dict = data_dict
        if hash_types == ["ALL"]:
            self.hash_types = [ hashfn for hashfn in AVAILABLE_HASH_TYPES if hashfn != "ALL" ]
        else:
            self.hash_types = hash_types

    def generate_hashes(self, divider="", min_combo_selections=2):
        """ Generate and return all the hashes.

        Args:
         divider: optional string to join elements with
         min_combo_selections: minimum number of elements to use to generate a hash
        Returns:
         A dictionary of hash: parameter mappings

        """
        hash_results = {}
        current_keys = list(self.data_dict.keys())

        # Use from min_combo_selections to the max number
        for num_elements in range(min_combo_selections, len(list(self.data_dict.keys()))+1):

            # Get the combination of num_elements values
            for combination in itertools.permutations(current_keys, num_elements):

                combo_fields = [ self.data_dict[elem] for elem in combination]
                joined_combo = divider.join(combo_fields)

                for hashfn in self.hash_types:
                    combo_hash = hashlib.new(hashfn, joined_combo.encode("utf-8"))
                    hash_results[combo_hash.hexdigest()] = {"fields": combo_fields,
                                                            "hashfn": hashfn}

        return hash_results

def main(hashfn, input_dict, min_combo_selection, divider, verbose):

    a = GeneratedHash(input_dict, hashfn)
    hashes = a.generate_hashes(divider, min_combo_selection)
    for hash_str, hash_attrs in hashes.items():
        if verbose:
            print("{} {} {}".format(hash_str, divider.join(hash_attrs["fields"]), hash_attrs["hashfn"]))
        else:
            print(hash_str)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate a series of hashes based on key-value datasets')
    parser.add_argument("--hashfn", "-H", dest="hashfn", action="store",
                        help="Hashing function(s) to use.", choices=AVAILABLE_HASH_TYPES,
                        nargs="+", default=["md5"])
    parser.add_argument("--json", "-j", dest="json", action="store_true",
                        help="Parse STDIN as JSON key-value data")
    parser.add_argument("--min-combinations", "-m", dest="min_combo_selection",
                        action="store", type=int, default=1,
                        help="Minimum number of items to pick combinations of")
    parser.add_argument("--keyval", "-k", dest="keyvals", action="store", nargs="+",
                        help="A key:value pair.", default=[])
    parser.add_argument("--divider", "-D", dest="divider", action="store", default="",
                        help="Divider placed between attributes when generating hashes.")
    parser.add_argument("--verbose", "-v", dest="verbose", action="store_true",
                        help="Annotate hashes with the fields used to generate them",
                        default=False)
    args = parser.parse_args()

    input_dict = {}

    if args.json and not sys.stdin.isatty():

        try:
            input_dict.update(json.load(sys.stdin))
        except ValueError as e:
            sys.stderr.write("Failed to load input - is it valid JSON? {}\n".format(e))
            sys.exit(254)

        if not all([ type(i) == str or type(i) == int for i in input_dict.values() ]):
            # for now any nested dicts or lists don't fit with our model
            sys.stderr.write("Not all JSON keys are integers or strings - can't operate on this data\n")
            sys.exit(253)

        for key, val in input_dict.items():
            if type(val) == int:
                input_dict[key] = str(val)
    else:
        arg_data_dict = {}
        for key, val in [ i.split(":") for i in args.keyvals ]:
            arg_data_dict[key] = val
        input_dict.update(arg_data_dict)

    main(args.hashfn, input_dict, args.min_combo_selection,
         args.divider, args.verbose)

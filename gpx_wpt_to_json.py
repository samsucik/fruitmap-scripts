import gpxpy
import json
import argparse
from thefuzz import fuzz
import unicodedata
from collections import defaultdict


synonyms = defaultdict(list)
unsupported_names = [
    "Muchovník",
    "Kiwi",
    "Mandľa",
    "Rešetliak",
    "Cesnak"
]


def add_synonyms(supported_tree_names):
    hardcoded_synonyms = {
        "Mirabelka": ["myrobalan"],
        "Jeřáb": ["jar vtac"],
        "Slivka": ["belica", "kralovka"]
    }
    for name, synonyms_list in hardcoded_synonyms.items():
        synonyms[name] += synonyms_list

    for name in supported_tree_names:
        name_no_accents = strip_accents(name)
        if name_no_accents != name:
            synonyms[name].append(name_no_accents.lower())


def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def get_args():
    parser = argparse.ArgumentParser(description="Convert GPX waypoint data into JSON data.")
    parser.add_argument("--input_file", type=str, help="The GPX file to process", required=True)
    parser.add_argument("--output_file", type=str, help="The output JSON file name", required=True)
    return parser.parse_args()


def get_similarity_score(text, target1, additional_targets=[]):
    def _sim_func(text1, text2):
        return fuzz.partial_ratio(text1, text2)
    score = max([_sim_func(text, target) for target in [target1] + additional_targets])
    return score


def get_closest_supported_tree_name(text, supported_tree_names):
    scores = {}

    for name in supported_tree_names + unsupported_names:
        score = get_similarity_score(text.lower(), name.lower(), synonyms.get(name, []))
        scores[name] = score

    closest_name = max(scores, key=scores.get)

    if closest_name in unsupported_names:
        print(f"'{closest_name}' isn't supported by fruitmap.org yet :-(")
        closest_name = None

    return closest_name


def convert_data(args, supported_tree_names):
    data = []

    with open(args.input_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        print("MANUALLY CHECK THE EXTRACTED NAMES BELOW AND MAKE ANY NECESSARY CORRECTIONS IN YOUR GPX FILE:")
        for waypoint in gpx.waypoints:
            extracted_name = get_closest_supported_tree_name(waypoint.name, supported_tree_names)
            print(f"'{extracted_name}': '{waypoint.name}'")
            if extracted_name is not None:
                data.append({"name": extracted_name, "lat": waypoint.latitude, "lon": waypoint.longitude})
        print("MANUALLY CHECK THE EXTRACTED NAMES ABOVE AND MAKE ANY NECESSARY CORRECTIONS IN YOUR GPX FILE.")

    with open(args.output_file, "w") as out:
        json.dump(data, out)


def main(args):
    with open("supported_tree_names.json", "r") as f:
        supported_tree_names = json.load(f)
    add_synonyms(supported_tree_names)

    convert_data(args, supported_tree_names)


if __name__ == '__main__':
    args = get_args()
    main(args)

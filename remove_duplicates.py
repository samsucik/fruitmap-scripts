import json
import argparse
import pandas as pd
from math import radians, cos, sin, asin, sqrt
from pynput import keyboard


def get_args():
    parser = argparse.ArgumentParser(
        description="Convert GPX waypoint data into JSON data.")
    parser.add_argument(
        "--input_file",
        type=str,
        help="The GPX file to process",
        required=True)
    parser.add_argument(
        "--all_trees_file",
        type=str,
        help="The output JSON file name",
        required=True)
    parser.add_argument(
        "--output_file",
        type=str,
        help="The output JSON file name",
        required=True)
    return parser.parse_args()


def distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return(2 * asin(sqrt(a)) * 6371)


def make_mapy_cz_url(lat, lon):
    return f"https://sk.mapy.cz/turisticka?source=coor&id={lon}%2C{lat}&x={lon}&y={lat}&z=19&base=ophoto"


def user_wants_to_keep_tree():
    print("Do you want to add the new tree anyway? (y/n): ")
    with keyboard.Events() as events:
        while True:
            # Block for as much as possible
            event = events.get(1e6)
            if event and isinstance(event, keyboard.Events.Release):
                if event.key == keyboard.KeyCode.from_char("y"):
                    return True
                elif event.key == keyboard.KeyCode.from_char("n"):
                    return False


def get_likely_existing_duplicates(tree, all_trees, distance_threshold):
    species_mask = all_trees["species_id"] == tree["species_id"]
    all_trees.loc[species_mask, "distance [m]"] = all_trees[species_mask].apply(
        lambda row: 1000 * distance(
            lat1=tree["lat"],
            lon1=tree["lon"],
            lat2=row["lat"],
            lon2=row["lon"]), axis=1)
    return all_trees[species_mask].query(f"`distance [m]` < {distance_threshold}")


def report_likely_duplicates(tree, likely_duplicates):
    print(f"\n=== Likely duplicate(s) found for tree: ===\n\t{tree} ({make_mapy_cz_url(tree['lat'], tree['lon'])})")
    print("Existing trees:")
    for i, duplicate in likely_duplicates.iterrows():
        print(f"\tuser with ID {int(duplicate['user_id'])} added the same species {duplicate['distance [m]']:.1f}m away: {make_mapy_cz_url(duplicate['lat'], duplicate['lon'])}")


def main(args):
    args = get_args()

    distance_threshold = 5  # 5m

    all_trees = pd.read_json(args.all_trees_file)

    with open(args.input_file, "r", encoding="utf-8") as f:
        trees_to_be_added = json.load(f)

    trees_to_add_excl_duplicates = []
    for tree in trees_to_be_added:
        likely_duplicates = get_likely_existing_duplicates(
            tree,
            all_trees,
            distance_threshold)

        if len(likely_duplicates) > 0:
            report_likely_duplicates(tree, likely_duplicates)

            if user_wants_to_keep_tree():
                trees_to_add_excl_duplicates.append(tree)
        else:
            trees_to_add_excl_duplicates.append(tree)

    with open(args.output_file, "w", encoding="utf-8") as f:
        json.dump(trees_to_add_excl_duplicates, f)


if __name__ == '__main__':
    args = get_args()
    main(args)

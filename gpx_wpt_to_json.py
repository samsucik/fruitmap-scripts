import gpxpy
import json
import argparse


def get_args():
    parser = argparse.ArgumentParser(description="Convert GPX waypoint data into JSON data.")
    parser.add_argument("--input_file", type=str, help="The GPX file to process", required=True)
    parser.add_argument("--output_file", type=str, help="The output JSON file name", required=True)
    return parser.parse_args()


def main(args):
    data = []

    with open(args.input_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        for waypoint in gpx.waypoints:
            data.append({"name": waypoint.name, "lat": waypoint.latitude, "lon": waypoint.longitude})

    with open(args.output_file, "w") as out:
        json.dump(data, out)


if __name__ == '__main__':
    args = get_args()
    main(args)

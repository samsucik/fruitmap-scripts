from pyquery import PyQuery as pq
import requests
import re
import os.path
from pathlib import Path
from tqdm import tqdm
import json
import argparse


def download_users_page(users_page_file, skip_existing=True):
    if skip_existing and os.path.exists(users_page_file):
        return

    users_page_url = "https://www.fruitmap.org/ludia"
    html_text = requests.get(users_page_url).text
    open(users_page_file, "w").write(html_text)


def get_user_ids_and_tree_counts(users_page_file, min_tree_count=0):
    d = pq(filename=users_page_file)
    user_urls = list(d("div.biglink.clovek a").items())
    user_tree_counts = list(d("div.biglink.clovek").find("h2 small i").items())
    result = {}
    for i, (url, count) in enumerate(zip(user_urls, user_tree_counts)):
        user_id = url.attr("href").replace("ludia/", "").strip()
        tree_count = int(count.text().replace(" trees", "").strip())
        if tree_count >= min_tree_count:
            result[user_id] = tree_count
    return result


def download_trees_page_for_user(user_id, file, skip_existing=True):
    if skip_existing and os.path.exists(file):
        return

    user_page_url = f"https://www.fruitmap.org/ludia/{user_id}"
    html_text = requests.get(user_page_url).text
    open(file, "w").write(html_text)


def get_trees_for_user(user_id, expected_tree_count, html_dir, force_refresh):
    user_page_file = html_dir / f"user{user_id}.html"

    download_trees_page_for_user(
        user_id,
        user_page_file,
        skip_existing=not force_refresh)

    with open(user_page_file, "r") as f:
        html_text = f.read()

    matches = re.findall(
        r"newMarker\(([-]?[0-9.]+),([-]?[0-9.]+),([0-9]+),'[^']+'\);",
        html_text,
        flags=0)

    if expected_tree_count != len(matches):
        print(f"user {user_id}: expected {expected_tree_count} but found {len(matches)} trees")
    trees = [{"species_id": int(id), "lat": float(lat), "lon": float(lon), "user_id": user_id} for (
        lat, lon, id) in matches]
    return trees


def get_args():
    parser = argparse.ArgumentParser(
        description="Get all trees from fruitmap.org and save into a JSON file.")
    parser.add_argument(
        "--output_file",
        type=str,
        help="The output JSON file name (default: all_trees.json)",
        required=False,
        default="all_trees.json")
    parser.add_argument(
        "--force_refresh",
        type=bool,
        help="Re-download all data even if they exist locally (use only when data freshness is a must)",
        required=False,
        default=False)
    return parser.parse_args()


def main():
    args = get_args()

    html_dir = Path("html")
    os.makedirs(html_dir, exist_ok=True)
    users_page_file = html_dir / "users.html"

    download_users_page(users_page_file, skip_existing=not args.force_refresh)
    user_tree_counts = get_user_ids_and_tree_counts(users_page_file, min_tree_count=1)
    all_trees = []
    for user_id, tree_count in tqdm(
            user_tree_counts.items(), desc="processing users (fetching trees)"):
        all_trees.extend(
            get_trees_for_user(
                user_id,
                tree_count,
                html_dir,
                args.force_refresh))
    with open(args.output_file, "w") as f:
        json.dump(all_trees, f)


if __name__ == '__main__':
    main()

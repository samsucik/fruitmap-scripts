from pyquery import PyQuery as pq
import requests


def download_users_page(users_page_file):
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


def main():
    users_page_file = "users.html"
    # download_users_page(users_page_file)
    user_tree_counts = get_user_ids_and_tree_counts(users_page_file, min_tree_count=1)
    print(user_tree_counts)


if __name__ == '__main__':
    main()

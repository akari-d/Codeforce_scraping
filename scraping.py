import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import datetime
import pandas as pd


def scraping_codeforce():
    try:
        url = "https://codeforces.com/"
        res = requests.get(url)
        res.raise_for_status()

    except requests.RequestException as e:
        print(f"Error occurred: {e}")

    else:
        print(f"Successfully accessed {url}")

    soup = BeautifulSoup(res.text, "html.parser")
    driver = webdriver.Chrome()

    # Problemsetのurlを取得
    # cssセクレタを使用して抽出
    elems = soup.select_one("ul.main-menu-list > li:nth-child(6) > a")
    problem_link = elems.get("href")
    url += problem_link

    try:
        res_2 = requests.get(url)
        res_2.raise_for_status()

    except requests.RequestException as e:
        print(f"Error occurred: {e}")

    else:
        print(f"Successfully accessed {url}")

    # 1pege目のproblem_id,title,rating,tag,solved_count,urlの項目を取得する。
    soup = BeautifulSoup(res_2.text, "html.parser")
    problems = soup.select("table.problems tr:has(td)")

    print("status:", res_2.status_code)

    data = []
    for problem in problems:
        # problem_id
        problem_id_elem = problem.select_one("td.id a")
        problem_id = problem_id_elem.get_text(strip=True) if problem_id_elem else None

        # titleとurl
        title_elems = problem.select_one("div[style= 'float: left;'] a")
        title = title_elems.get_text(strip=True) if title_elems else None
        title_url = title_elems.get("href") if title_elems else None

        # rating
        rating_td = problem.select_one("td[style = 'font-size: 1.1rem']")
        rating = rating_td.get_text(strip=True) if rating_td else None

        # tags
        tag_names = problem.find_all("a", class_="notice")
        tags = [tag_name.get_text(strip=True) for tag_name in tag_names]
        tags_text = ", ".join(tags)

        # solved_count
        solve_elem = problem.select_one("td:nth-child(5) > a")
        a_text = solve_elem.get_text(" ", strip=True) if solve_elem else None
        solved_count = None
        if a_text:
            match = re.search(r"x\s*([\d,]+)", a_text)
            if match:
                solved_count = int(match.group(1).replace(",", ""))

        # 取得日
        dt = datetime.date.today()

        # データを辞書でまとめる
        data.append(
            {
                "problem_id": problem_id,
                "title": title,
                "rating": rating,
                "tags": tags_text,
                "solved_count": solved_count,
                "url": title_url,
                "scraped_date": dt,
            }
        )


    df = pd.DataFrame(data)

    df.to_csv("codeforces_problems.csv", index=False)

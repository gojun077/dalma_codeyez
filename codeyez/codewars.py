"""query a user's public Codewars profile page to get number of solved
problems"""


from requests import Timeout
import requests


def get_solved_count_cw(user: str) -> int:
    """
    Given string 'user' denoting a valid Codewars username, return
    the integer count of solved problems. Problems which have been
    solved using more than one language will be counted separately
    for each language.
    """
    url_cw = f"https://www.codewars.com/api/v1/users/{user}"
    ep_cw = "/code-challenges/completed?page=0"
    full_url = url_cw + ep_cw
    num_solved = 0

    try:
        sess_cw = requests.Session()
        resp_cw = sess_cw.get(full_url, timeout=5)
        resp_cw.raise_for_status()
        cw_data = resp_cw.json()
        for solvd in cw_data['data']:
            num_solved += 1*len(solvd['completedLanguages'])
        return num_solved
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    except Timeout as e:
        raise SystemExit(e)

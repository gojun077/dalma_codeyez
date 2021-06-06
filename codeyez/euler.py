"""query a user's public Project Euler profile to get number of solved
problems"""


from lxml import etree
from requests import Timeout
import requests

def get_solved_count_pe(user: str) -> int:
    """
    Given string 'user' denoting a valid Project Euler username, return
    the integer count of solved problems.
    """
    url_pe = f"https://projecteuler.net/profile/{user}.xml"
    num_solved = 0
    try:
        sess_pe = requests.Session()
        resp_pe = sess_pe.get(url_pe, timeout=5)
        resp_pe.raise_for_status()
        root = etree.XML(resp_pe.text)
        #user_pe = root[0].text
        #cntry_pe = root[1].text
        #lang_pe = root[2].text
        solve_pe = root[3].text
        #level_pe = root[4].text

        if solve_pe == None:
            return num_solved
        else:
            num_solved = int(solve_pe)
        return num_solved
    # non-2XX HTTP response
    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
    except Timeout as e:
        raise SystemExit(e)

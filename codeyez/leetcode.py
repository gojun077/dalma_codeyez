"""query a user's public leetcode profile page to get number of solved
problems"""


from selenium import webdriver


def get_ac_count(user: str) -> dict:
    """
    Given string 'user' denoting a valid leetcode username,
    return a dict of the form {"easy": 3, "med": 2, "hard": 1}
    that gives information on the number of "ac" or solved
    problems for 'user'.
    """
    

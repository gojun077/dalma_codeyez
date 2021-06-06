#!/usr/bin/env python3


from codewars import get_solved_count_cw
from euler import get_solved_count_pe
from leetcode import get_ac_count
import json
import os


def main():
    home = os.environ['HOME']
    cfgPath = home + '/.config/codeyez'
    if not os.path.exists(cfgPath):
        print(f"Creating {cfgPath} for the first time...")
        os.mkdir(cfgPath)
    cw_user_file = cfgPath + '/codewars_user.json'
    elr_user_file = cfgPath + '/euler_user.json'
    lc_user_file = cfgPath + '/leetcode_user.json'
    if not os.path.exists(cw_user_file):
        cw_user = input("codewars_user.json not found. Enter username: ")
        cw_user_d = {"username": cw_user}
        with open(cw_user_file, "w") as f:
            json.dump(cw_user_d, f)
    if not os.path.exists(elr_user_file):
        elr_user = input("euler_user.json not found. Enter username: ")
        elr_user_d = {"username": elr_user}
        with open(elr_user_file, "w") as f:
            json.dump(elr_user_d, f)
    if not os.path.exists(lc_user_file):
        lc_user = input("leetcode_user.json not found. Enter username: ")
        lc_user_d = {"username": lc_user}
        with open(lc_user_file, "w") as f:
            json.dump(lc_user_d, f)

if __name__ == "__main__":
    main()

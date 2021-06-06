dalma_codeyez README
=============================

# Summary

- Created on: May 24 2021
- Created by: gojun077@gmail.com

![dalma](dalma_codeyez.png)

`dalma_codeyez` is a program to keep track of how many problems
you have solved on the following programming challenge sites:

- Codewars
- Leetcode
- Project Euler

All 3 sites have publicly accessible endpoints which give information about
how many problems have been solved by a user. When `dalma_codeyez` is first
run it will store the baseline count of all questions you have solved on
Codewars, Leetcode, and Project Euler. It is intended to be run as a
cronjob or systemd service+timer, and if it detects that additional
problems have been solved, `dalma_codeyez` will send a JSON payload to
the Beeminder API for an endpoint corresponding to a Beeminder goal to solve
*x* coding problems per week.

References

- https://gitlab.com/gojun077/junsTechNotes/-/blob/master/beeminder_API_notes.md
- https://gitlab.com/gojun077/junsTechNotes/-/blob/master/codewars_API.md
- https://gitlab.com/gojun077/junsTechNotes/-/blob/master/leetcode_API.md
- https://gitlab.com/gojun077/junsTechNotes/-/blob/master/project_euler_API.md


# Topics

## Dependencies

This app is written in Python 3 and depends on Selenium,
chromium-chromedriver, and the following Python modules outside stdlib:

- `requests`
- `selenium`

## Roadmap

- `v0.1.0` initial version with naive problem counts, public API only
- `v0.2.0` support cookie login for privileged pages, add DB backend

### v0.1 Alpha

The alpha version `v0.1` will use public HTTP endpoints from Codewars,
Leetcode, and Project Euler. From public endpoints, Leetcode and Project
Euler only return info on HOW MANY problems have been solved by a user, but
provide no info on WHICH problems have been solved. Leetcode does provide
separate counts of easy/med/hard problems solved, however.

Unlike Leetcode and Project Euler, Codewars public API provides both a
total count of problems solved as well as info on *which* problems were
solved and in what language(s). You can also get information on problem
difficulty rated from 8 kyu (easiest) to 1 kyu (hardest).

The alpha version will calculate solved problem counts on the fly and will
only store the last count and the current count of solved problems in the
files `old_count`, `new_count`. If there has been a non-negative change in
the count, an HTTP POST request will be sent to Beeminder API containing a
timestamp and the positive delta.

The following files will stored `~/.local/codeyez`:

- Beeminder API credentials json file

### v0.2 Beta

The beta `v0.2` will support login via session cookies to Leetcode and
Project Euler. When a Leetcode session cookie has expired, `dalma_codeyez`
can programmatically log into Leetcode via Selenium by finding the XPath to
the username and password HTML form input boxes and submitting user / pass
into the forms. Upon login, `dalma_codeyez` will obtain a new session
cookie, save the cookie to a local `.json` file and use it for subsequent
requests. Selenium cannot automatically log into Project Euler, however, as
the login page requires a CAPTCHA to be solved by a human. What you can do
instead is manually export your Project Euler session cookie from Chrome
using a browser extension like *Export cookie JSON file for Puppeteer*.

The following files will stored `~/.local/codeyez`:

- `leetcode_scookie.json`
  + `{"LEETCODE_SESSION": "391 char alphanum"}`
- `proj_euler_scookie.json`
  + `{"PHPSESSID": "123abc..."}`
- sqlite3 DB file

After manually exporting your session cookie from Project Euler, you will
need to copy-paste the relevant key values into `proj_euler_scookie.json`
Once you have seeded this file, however, you won't need to re-seed it for
one month. The Leetcode session cookie has an expiration of 2 weeks, so
it will need to be re-seeded upon expiration.

`v0.2` will use `sqlite3` as its backend DB and will store data on *all*
problems from Codewars, Leetcode, and Project Euler. A custom point system
will be introduced, with 1 pt assigned to 'easy', 2 pts for 'medium' and 3
pts for 'hard' difficulty questions. Since this form of difficulty
categorization only exists on Leetcode, difficulty normalization will be
carried out in the DB for Codewars and Project Euler problems.

- Codewars 7 to 8 kyu problems will be classified as 'easy' (1 pt)
- Codewars 4 to 6 kyu problems will be classified as 'medium' (2 pts)
- Codewars 1 to 3 kyu problems will be classified as 'hard' (3 pts)
- Project Euler (PE) problems solved by > 100,000 users: 'easy' (1 pt)
- PE problems solved by 40,000 <= x <= 100,000 users: 'medium' (2 pts)
- PE problems solved by x < 40,000 users: 'hard' (3 pts)

When `dalma_codeyez v0.2` is first run, it will query solved problem data
from Codewars, Leetcode, and Project Euler, insert these records into
`sqlite3`, and calculate a baseline point value for all solved problems.
This value will be stored in a file named `curr_tot_points`. On each
subsequent execution, `dalma_codeyez` will check if any add'l problems have
been solved and INSERT them into the DB and calculate the new point
total. If the point total has increased, the previous point total will be
copied from `curr_tot_points` to `prev_tot_points` and the new point total
will be written to `curr_tot_points`. Based on the `ISO8601` timestamp of
when the record was INSERTed into the DB, `dalma_codeyez` can determine
which problems were recently solved.

For each problem that was added to the DB within 60s of `dalma_codeyez`
execution, an HTTP POST request with JSON payload will be sent to the
Beeminder API for the goal *acquire n 'coding points' per week*. The
payload will contain the following info:

- Name of problem solved
- Problem difficulty
- Point value
- Language used (for Codewars)
- Solution Date (timestamp of INSERT to `sqlite3`)

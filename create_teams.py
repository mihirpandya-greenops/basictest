import requests
import warnings
from templates import N, TEAM_TEMPLATE, TEAM_CREATION_TEMPLATE, ORG, PARENT_TEAM, get_auth_cookie

warnings.filterwarnings("ignore")

cookie = get_auth_cookie()

# create the teams
for i in range(1, N + 1):
    team = TEAM_TEMPLATE.format(i)
    team_url = TEAM_CREATION_TEMPLATE.format(ORG, PARENT_TEAM, team)
    r = requests.post(url=team_url, cookies=cookie, verify=False)
    if r.status_code == 200:
        print(f"Created team {team}")
    else:
        print(f"Failed to create team {team}: {r.text}")

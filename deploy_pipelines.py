import time
import requests
import json
import argparse
import warnings
from templates import N, GIT_REPO, PIPELINE_TEMPLATE, PIPELINE_CREATION_TEMPLATE, ORG, PIPELINE_SYNC_TEMPLATE, \
    TEAM_TEMPLATE, get_auth_cookie, REVISION_HASH

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', metavar='time', required=True, help='time between creating pipelines')

body = {
    "gitRepoSchema": {
        "gitRepo": GIT_REPO,
        "pathToRoot": "",
        "gitCred": {
            "type": "open"
        }
    },
    "reconciliationSchema": {
        "linkedPipelineName": "",
        "linkedArgoCdApplication": ""
    }
}

cookie = get_auth_cookie()

N = 5


def deployPipelines(sleepSeconds):
    for i in range(1, N + 1):
        # create and deploy pipelines
        team = TEAM_TEMPLATE.format(i)
        pipeline = PIPELINE_TEMPLATE.format(i)
        body['gitRepoSchema']['pathToRoot'] = f"pipeline{i}/pipeline"
        pipeline_url = PIPELINE_CREATION_TEMPLATE.format(ORG, team, pipeline)

        r = requests.post(pipeline_url, data=json.dumps(body).encode("utf-8"), cookies=cookie, verify=False)

        if r.status_code == 200:
            print(f"Created pipeline {pipeline} successfully")
        else:
            print(r.status_code)
            print(f"Failed to create pipeline {pipeline}: {r.text}")

        sync_url = PIPELINE_SYNC_TEMPLATE.format(ORG, team, pipeline, REVISION_HASH)
        print(sync_url)
        r = requests.post(sync_url, cookies=cookie, verify = False)

        if r.status_code == 200:
            print(f"Deployed pipeline {pipeline} successfully")
        else:
            print(f"Failed to deploy pipeline {pipeline}: {r.text}")

        if sleepSeconds > 0:
            time.sleep(sleepSeconds)


if __name__ == "__main__":
    args = parser.parse_args()
    sleep_time = args.time
    print(f"Sleep time: {sleep_time}")
    deployPipelines(int(sleep_time))

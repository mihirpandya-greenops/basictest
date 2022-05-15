import os
from templates import N

for i in range(1, N + 1):
    for j in range(1, 3):
        app = f"pipeline{i}-app{j}"
        namespace = f"pipeline{i}-namespace{j}"
        os.system(f"kubectl create namespace {namespace}")
        app_creation_cmd = f"argocd app create {app} --repo https://github.com/gsharma30/greenops_test --path pipeline{i}/app{j} --dest-server https://kubernetes.default.svc --dest-namespace argo"
        os.system(app_creation_cmd)

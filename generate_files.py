import shutil
import ruamel.yaml

from templates import N

yaml = ruamel.yaml.YAML()

root_folder = "/Users/gauravsharma/greenops_test/"

# n is the number of pipelines to create (first one is already manually created and used as the base template)
for i in range(2, N + 1):
    new_path = f"{root_folder}pipeline{i}"
    shutil.copytree(f"{root_folder}pipeline1", new_path)

    # Update the pipeline file
    with open(new_path + "/pipeline/pipeline.yaml") as fp:
        data_pipeline = yaml.load(fp)
        data_pipeline['metadata']['generateName'] = f"pipeline{i}"

    with open(new_path + "/pipeline/pipeline.yaml", "w") as f:
        yaml.dump(data_pipeline, f)

    # Update the params file
    with open(new_path + "/pipeline/params.yaml") as fp:
        data_params = yaml.load(fp)
        for elem in data_params['arguments']['parameters']:
            if elem['name'] == 'application-name':
                elem['value'] = f'pipeline{i}-app1'
            if elem['name'] == 'application-name-2':
                elem['value'] = f'pipeline{i}-app2'
    with open(new_path + "/pipeline/params.yaml", "w") as f:
        yaml.dump(data_params, f)

    for j in range(1, 3):
        # Update the deployment
        with open(new_path + f"/app{j}/guestbook-ui-deployment.yaml") as fp:
            data_deployment = yaml.load(fp)
            data_deployment['metadata']['namespace'] = f"pipeline{i}-namespace{j}"

        with open(new_path + f"/app{j}/guestbook-ui-deployment.yaml", "w") as f:
            yaml.dump(data_deployment, f)

        # Update the service
        with open(new_path + f"/app{j}/guestbook-ui-svc.yaml") as fp:
            data_service = yaml.load(fp)
            data_service['metadata']['namespace'] = f"pipeline{i}-namespace{j}"
        with open(new_path + f"/app{j}/guestbook-ui-svc.yaml", "w") as f:
            yaml.dump(data_service, f)

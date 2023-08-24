### Usage

#### 1. 🐳 Using the Docker Image (Recommended approach)

_Ensure docker is pre-installed correctly in your environment_

- ⬇️ Pull the Docker image

```
docker pull abhimishraa/dorametrics:latest
```

- ➕ Generate the metrics for a pre-existing git repository / project
  _Considering your repository had followed strict git flow as stated [here](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/docs/update-readme#-creating-a-pull-request---)_

```
docker run --rm
-v "$(pwd)/metrics":/app/metrics
-v "$(pwd)/.git":/app/.git
abhimishraa/dorametrics:latest --calculate-metrics -e True
```

- ➕ Generate the metrics for your recent release that went through

```
docker run --rm
-v "$(pwd)/metrics":/app/metrics
-v "$(pwd)/.git":/app/.git
abhimishraa/dorametrics:latest --calculate-metrics
```

**Please refer the breakdown of both output files that got generated during the above process [here](https://github.com/wednesday-solutions/automated-delivery-metrics/blob/main/guide/output-breakdown/Readme.md)**

- 📣 To notify Jira Compass with after the metrics are generated

```
docker run --rm
-v "$(pwd)/metrics":/app/metrics
-e COMPASS_USER_EMAIL=$COMPASS_USER_EMAIL
-e COMPASS_USER_API_KEY=$COMPASS_USER_API_KEY
-e COMPASS_METRICS_BASE_URL=$COMPASS_METRICS_BASE_URL abhimishraa/dorametrics:latest --notify-compass "metrics/data.yaml" "metrics/target-metrics.yaml"
```

The `--notify-compass` command takes two arguments :-

1. Source :- The location of the metrics `data.yaml` file that just got generated using --calculate-metrics command earlier.
2. Target :- The location of the names and identities of the metrics that needs to go into Jira compass `target-merics.yaml` file that needs to be present before running the command.
   Please refer [this](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main/guide/target-metrics) documentation for more information about how to populate the `target-merics.yaml` file

**The need for attaching volumes** :-

##### 1 /metrics

- The tool inside the container will calculate the metrics based on git history of the host repository
- Once the metrics are generated, it will create two `yaml` files `data.yaml`, `release.yaml` inside the `metrics/` directory of the container
- In order to get access to those metrics, we need to mount the host's /metrics directory to the container.
- This directory will be further used to fetch the generated metrics `data.yaml` and the destination metrics identities `target-metrics.yaml` for the notify compass method.

##### 2 /.git

- As stated earlier, the tool calculates the metrics based on git history of the host repository
- Since the container is an isolated environment, in order to get access to the logs of the host, we need to mount the /.git directory from the host into the container.

###### Ideally the deployment ci pipeline should run the metrics calculation and notification commands

_🛑 Important Note_ :-

- Please check the section for [creating a branch and pull request](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/docs/update-readme#-creating-a-pull-request---) that we strictly follow as the tool relies on the proper naming conventions of branches in order to generate correct metrics.
- Any ambigious branch names will be automatically ignored by the automation tool and will affect the metrics generation and calculation.

#### 2. Using the repository source code itself

- Clone the git repository within your existing project / parent repository

```
git clone https://github.com/wednesday-solutions/automated-delivery-metrics.git
```

_Ensure python3.9 is available in your environment runtime_

- Once cloned, you can rename the cloned repository folder to your desired name.
- Remove the `.git` directory from the newly cloned repository folder so it doesn't conflict with the parent git logs.
- Run the following command :-

```
python automation.py -e True
<!-- -e True if integrating this tool to your existing project-->
```

- The output files will be yielded in the metrics/ directory within the folder.

- To notify the Jira compass, ensure the following environment variables are set in your environment beforehand :-

```
- COMPASS_USER_EMAIL
- COMPASS_USER_API_KEY
- COMPASS_METRICS_BASE_URL
```

- Once the above requirements are met, run the following command :-

```
./scripts/notify-compass.sh
```

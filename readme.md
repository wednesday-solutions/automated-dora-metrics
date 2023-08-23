## Automated Delivery Metrics 🚀

- This repository demonstrates the power of automation in generating metrics for your software releases. By utilizing the provided scripts and tools
- You can streamline the process of calculating and recording metrics for your projects.
- Once the metrics are generated, you can seamlessly push them to 📣 [Jira Compass](https://www.atlassian.com/software/compass) to keep track 📝 of your custom metrics effortlessly.

### Files Created by the Tool :-

##### 1 data.yaml

- This file holds a wealth of information, including CFR metrics, averages, and detailed insights about recent releases. If you're integrating this tool into an existing Git repository, data.yaml becomes your go-to resource for metrics analysis.

##### 2 release.yaml

- The release.yaml file presents a chronological list of your project's releases.

#### 🐳 Using the Docker Image

You can use the Docker image [abhimishraa/dorametrics:latest](https://hub.docker.com/u/abhimishraa) to run the automation and interact with Jira Compass. Here's how:

### ➕ Generate Metrics

- Generate metrics for recent release

```
docker run --rm
-v "$(pwd)/metrics":/app/metrics
 <!-- attach metrics dir of container host as an output dir -->
-v "$(pwd)/.git":/app/.git
 <!-- attach .git dir of the container host -->
abhimishraa/dorametrics:latest --calculate-metrics
  <!-- -e flag is optional, default False -->
```

_The need for attaching volume_ :-

##### 1 /metrics

- The tool inside the container will calculate the metrics based on git history of the host repository
- Once the metrics are generated, it will create two `yaml` files `data.yaml`, `release.yaml` inside the `metrics/` directory of the container
- In order to get access to those metrics, we need to mount the host's /metrics directory to the container.

##### 2 /.git

- As stated earlier, the tool calculates the metrics based on git history of the host repository
- Since the container is an isolated environment, in order to get access to the logs of the host, we need to mount the /.git directory from the host into the container.

```
docker run --rm
-v "$(pwd)/metrics":/app/metrics
-v "$(pwd)/.git":/app/.git
abhimishraa/dorametrics:latest --calculate-metrics -e True
  <!-- -e flag is optional, default False -->
```

- If you are importing this tool to an existing git repository and the parent/production branch is not main (default)

```
docker run --rm \
  -v "$(pwd)/metrics":/app/metrics \
  -v "$(pwd)/.git":/app/.git \
  abhimishraa/dorametrics:latest \
  --calculate-metrics -e True -p <branch-name>
  <!-- -e, -p are optional -->
```

#### Generally the deployment ci pipeline should run the metrics calculation command

_Note_ 🛑:- Please check the section for [creating a branch and pull request](https://github.com/abhishek-ws/dora-metrics-poc#-creating-a-pull-request---) that we strictly follow as the tool relies on the proper naming conventions of branches in order to generate correct metrics. Any ambigious branch names will be automatically ignored by the automation tool and will affect the metrics generation and calculation.

This will generate two different metric files inside a folder called `metrics` (it should be created on the fly if the folder does not exists)

- data.yaml :- contains summary of previous releases, features, bugs, hotfixes, average for each along with cfr metrics

- release.yaml :- the file will be updated with the latest release and the release details such as features, bugs, hotfix, date, etc sequentially in a list format for every release you run, considering you integrate the `calculate-metrics` flow into your release cd pipeline

#### To notify Jira Compass with the generated metrics:

```
docker run --rm \
    -e COMPASS_USER_EMAIL=$COMPASS_USER_EMAIL \
    -e COMPASS_USER_API_KEY=$COMPASS_USER_API_KEY \
    -e COMPASS_METRICS_BASE_URL=$COMPASS_METRICS_BASE_URL \
    -v $(pwd):/app abhimishraa/dorametrics:latest \
    --notify-compass "metrics/data.yaml" "metrics/target-metrics.yaml"
```

This command will notify Jira Compass with the metrics generated using the specified YAML files.
_Note_ :-

- metrics/data.yaml is the output generated from previous `calculate-metrics` command
- ensure to provide necessary credentials to accesss your Jira compass such as email, api key, base url, etc.

#### Structure of target-metrics.yaml

The target-metrics.yaml file defines the metrics you want to calculate and track. Customize the metrics and their associated IDs according to your project's needs.

The structure should be similar to what we have [here](https://github.com/abhishek-ws/dora-metrics-poc/blob/main/metrics/target-metrics.yaml)

#### If your parent / production branch is not `main`, specify it manually :-

```
docker run --rm -v $(pwd)/metrics:/app/metrics abhimishraa/dorametrics:latest --calculate-metrics -p <branch-name>
```

#### For getting help from automation script :-

```
docker run --rm abhimishraa/dorametrics:latest --calculate-metrics --help
```

### 🛑 Creating a Pull request 🛑 :-

- The branch name must correspond to the ticket number such as `<type-of-ticket>/<Proj>-<TickNumber>`
- For example :-

```
 `feature/<PROJ>-1`
 `chore/<PROJ>-6`
 `docs/<PROJ>-7`
 `bug/<PROJ>-2`
 `fix/<PROJ>-5`
 `bugfix/<PROJ>-2`
 `hotfix/<PROJ>-3`
```

---

### 📝 Things to note while importing to an existing Git repository and limitations :-

##### 1 data.yaml

- Running this tool to an existing git repository `(-e True flag)` will list down all the merges done into your `main` branch and the count of it will be considered as the total number of releases which we can see in the `total_releases` section of the file itself.

##### 2 release.yaml

- Running this tool to an existing git repository `(-e True flag)` the time when you execute the --calculate-metrics command marks the initiation of the first release in this sequence.
- _Note_ 🛑:- although we do get the `total_releases` in `data.yaml`, the tool does not has the ability to list break down every release (merge into `main`) branch and hence the release number in the list order will start from `1`

---

- **Important Note** 🛑: Although there are some limitations while integrating this to an existing git repository as this tool was built with the focus of calculating the metrics for `next release cycles` that come into a `git branch (main)`, but it's crucial to recognize that correct metrics will be generated for all subsequent releases. The tool will seamlessly calculate and provide accurate metrics for your future releases. It's a powerful step toward enhancing your project's insights and tracking its progress effectively. Happy measuring! 📊🚀

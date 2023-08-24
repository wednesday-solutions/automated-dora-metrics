<div>
  
  <p>
    <h1 align="left">Automated Delivery Metrics
    </h1>
  </p>

  <p>
A tool to provide the ability to generate automated metrics for your every releases.
  </p>

---

  <p>
    <h4>
      Expert teams of digital product strategists, developers, and designers.
    </h4>
  </p>

  <div>
    <a href="https://www.wednesday.is/contact-us?utm_source=gthb&utm_medium=repo&utm_campaign=serverless" target="_blank">
      <img src="https://uploads-ssl.webflow.com/5ee36ce1473112550f1e1739/5f6ae88b9005f9ed382fb2a5_button_get_in_touch.svg" width="121" height="34">
    </a>
    <a href="https://github.com/wednesday-solutions/" target="_blank">
      <img src="https://uploads-ssl.webflow.com/5ee36ce1473112550f1e1739/5f6ae88bb1958c3253756c39_button_follow_on_github.svg" width="168" height="34">
    </a>
  </div>

<span>We’re always looking for people who value their work, so come and join us. <a href="https://www.wednesday.is/hiring">We are hiring!</a></span>

</div>

---

- This repository demonstrates the power of automation in generating metrics for your software releases. By utilizing the provided scripts and tools
- You can streamline the process of calculating and recording metrics for your projects.
- Once the metrics are generated, you can seamlessly push them to 📣 [Compass](https://www.atlassian.com/software/compass) to keep track 📝 of your custom metrics effortlessly by following our instructions.
- We have hosted a docker image [here](https://hub.docker.com/repository/docker/abhimishraa/dorametrics/general)

---

### Getting started

- [Detailed usage guide](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main/guide/usage)
- [Quick usage summary](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main#for-getting-straight-into-commands-heres-how--)

#### For getting straight into commands, here's how :-

- ➕ Generate metrics for recent release

```
docker run --rm
-v "$(pwd)/metrics":/app/metrics
 <!-- attach metrics dir of container host as an output dir -->
-v "$(pwd)/.git":/app/.git
 <!-- attach .git dir of the container host -->
abhimishraa/dorametrics:latest --calculate-metrics
<!-- must be used without -e flag -->
```

- ➕ Generate metrics for your previous releases / pre-existing repository

_Considering your repository had followed strict git flow as stated [here](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main#for-getting-straight-into-commands-heres-how--)_

```
docker run --rm
-v "$(pwd)/metrics":/app/metrics
 <!-- attach metrics dir of container host as an output dir -->
-v "$(pwd)/.git":/app/.git
 <!-- attach .git dir of the container host -->
abhimishraa/dorametrics:latest --calculate-metrics -e True

```

- If your parent / production branch is not `main`, specify it manually :-

```
docker run --rm -v $(pwd)/metrics:/app/metrics abhimishraa/dorametrics:latest --calculate-metrics -p <branch-name>
```

- 📣 To notify Jira Compass with the generated metrics:

```
docker run --rm \
    -e COMPASS_USER_EMAIL=$COMPASS_USER_EMAIL \
    -e COMPASS_USER_API_KEY=$COMPASS_USER_API_KEY \
    -e COMPASS_METRICS_BASE_URL=$COMPASS_METRICS_BASE_URL \
    -v $(pwd):/app abhimishraa/dorametrics:latest \
    --notify-compass "metrics/data.yaml" "metrics/target-metrics.yaml"
```

- For getting help from the metrics tool :-

```
docker run --rm abhimishraa/dorametrics:latest --calculate-metrics --help
```

- For more, please check out our detailed [documentation](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main/guide/usage) to understand in depth concepts.

---

#### Sample CI Pipeline to integrate into your production release workflow can be found [here](https://github.com/wednesday-solutions/automated-delivery-metrics/blob/main/.github/workflows/calculate-metrics.yml)

#### Structure of target-metrics.yaml

The target-metrics.yaml file defines the metrics you want to calculate and track. Customize the metrics and their associated IDs according to your project's needs.

The structure should be similar to what we have [here](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main/guide/target-metrics)

### 🛑 Creating a Pull request 🛑 :-

- The branch name must correspond to the ticket number such as `<type-of-ticket>/<Proj>-<TickNumber>`
- For example :-

```
 `feat/<PROJ>-1`
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

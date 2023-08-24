### [Compass](https://developer.atlassian.com/cloud/compass/overview/what-is-compass/) component metrics integration through `target-metrics.yaml`

- Ensure you have a valid [component](https://developer.atlassian.com/cloud/compass/components/what-is-a-component/) created in the compass dashboard.
  _You can follow [this](https://developer.atlassian.com/cloud/compass/components/create-view-update-and-delete-components/) guide get started with compass and components_

- Once your component is available, you can create metrics that correspond to the names of the desrired metrics from the `data.yaml` `listed two points` below that you would like to push to your compass component. _[Guide](https://developer.atlassian.com/cloud/compass/components/create-connect-and-view-component-metrics/) for compass metrics_
- Once you have created the custom metrics and attached to your component, you can view the curl command that will carry the unique identifiers of the metrics available in the component's dashboard.
- ## We would like to have the following identities from the CURL of the respective metric :-
- Breakdown of CURL available in the components metrics UI

  - Sample CURL structure :- `curl --request POST \
--url "$Compass_Metrics_Base_URL" \
--user "$COMPASS_USER_EMAIL:$COMPASS_USER_API_KEY" \
--header "Accept: application/json" \
--header "Content-Type: application/json" \
--data "{\"metricSourceId\": \"$COMMON_METRICS_ID/$METRIC_ID\", \"value\": "$metric_value", \"timestamp\": \"$TIMESTAMP\"}" `
  - We need to retrieve the following identities mentioned in the form of variables in the above sample CURL structure
    :-
    - Compass_Metrics_Base_URL :- Usage mentioned [here](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main/guide/usage). (Common across all the metrics available for your component)
    - COMMON_METRICS_ID :- For `target-metrics.yaml` (Common across all the metrics available for your component)
    - METRIC_ID :- For `target-metrics.yaml` (Unique identifier for each metric available for your component)

- Create a file `target-metrics.yaml` (we recommend within the metrics/ folder in your project's root dir)
- The file should be populated in the following manner :-

```
common_metrics_id: <COMMON_METRICS_ID>
target_metrics:
  - cfr_hotfix_to_release: <METRIC_ID_1> # retrieved from the corresponding metric you created for your compass component
  - cfr_bugs_to_tasks_ratio: <METRIC_ID_2>
  - cfr_bug_to_feature: <METRIC_ID_3>
  - cfr_bug_release_ratio: <METRIC_ID_4>
  ....
  - <metric_key_name>: <METRIC_ID_N>
```

- Following are the metrics that we currently support for the target-metrics.yaml:-

  - total_releases
  - total_feature_releases
  - total_bugfix_releases
  - total_hotfix_releases
  - total_releases_without_bugs
  - average_features_per_release
  - average_bugs_per_release
  - average_hotfixes_per_release
  - cfr_hotfix_to_release
  - cfr_bugs_to_tasks_ratio
  - cfr_bug_to_feature
  - cfr\*bug_release_ratio

  **🛑 Note :- the target metrics should only contain the keys with the name exactly corresponding of the metrics' keys available in the `data.yaml`**

- Once the target metrics file has been created, we can inject it into the usage mentioned [here](https://github.com/wednesday-solutions/automated-delivery-metrics/tree/main/guide/usage)

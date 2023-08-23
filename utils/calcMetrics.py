import os
import yaml
from utils.date import get_current_date
from utils.math import calc_avg, calc_cfr_hotfix_to_release, calc_cfr_bugs_to_tasks_ratio, calc_cfr_bug_to_feature, calc_cfr_bug_release_ratio
from utils.dir import create_directory_and_file

current_date = get_current_date()

# yields data.yaml


def calculate_metrics(number_of_features, number_of_bugs, number_of_hotfixes, total_tickets, t_releases, existing_codebase=True, target_data_file='metrics/data.yaml', isHotFix="true", includesBugs="true"):
    if os.path.exists(target_data_file):
        print("Found existing target file, updating it with the latest release...")

        is_hot_fix = isHotFix.lower() == "true"
        includes_bugs = includesBugs.lower() == "true"

        # Read the existing YAML content
        with open(target_data_file, "r") as yaml_file:
            release_metrics = yaml.safe_load(yaml_file)
            prev_total_releases = release_metrics.get('total_releases')
            total_features = release_metrics.get('total_feature_releases')
            total_bugs = release_metrics.get('total_bugfix_releases')
            total_hotfixes = release_metrics.get('total_hotfix_releases')
            total_releases_without_bugs = release_metrics.get(
                'total_releases_without_bugs')
            prev_cfr_bugs_to_tasks_ratio = release_metrics.get(
                'cfr_bugs_to_tasks_ratio')
            prev_cfr_bug_to_feature = release_metrics.get('cfr_bug_to_feature')
            last_release = release_metrics.get('last_release')
            previous_n_tickets = last_release.get('total_tickets')

            current_release = int(prev_total_releases) + 1
            revised_total_features = int(total_features) + number_of_features
            revised_total_bugs = int(total_bugs) + number_of_bugs
            revised_total_hotfixes = int(total_hotfixes) + number_of_hotfixes
            revised_total_releases_without_bugs = total_releases_without_bugs if is_hot_fix or includes_bugs else total_releases_without_bugs + 1
            revised_total_tickets = previous_n_tickets if is_hot_fix else total_tickets

            # calculate hotfixes per deployments ratio for this release
            cfr_hotfix_to_release = calc_cfr_hotfix_to_release(
                current_release, revised_total_hotfixes)

            # calculate failures for tickets from previous release ratio
            cfr_bugs_to_tasks_ratio = calc_cfr_bugs_to_tasks_ratio(
                prev_ratio=prev_cfr_bugs_to_tasks_ratio[:-2], n_releases=prev_total_releases, n_total_tickets=previous_n_tickets, n_failures=number_of_bugs)

            # calculate feature to bug ratio
            cfr_bug_to_feature = calc_cfr_bug_to_feature(
                prev_ratio=prev_cfr_bug_to_feature[:-2], n_releases=prev_total_releases, n_bugs=revised_total_bugs, n_features=revised_total_features)

            # calculate release without bugs
            cfr_bug_release_ratio = calc_cfr_bug_release_ratio(
                current_release, revised_total_releases_without_bugs)

            # average per release
            average_features_per_release = calc_avg(
                revised_total_features, current_release)
            average_bugs_per_release = calc_avg(
                revised_total_bugs, current_release)
            average_hotfixes_per_release = calc_avg(
                revised_total_hotfixes, current_release)

            yaml_content = f"""
            .total_releases = {current_release} |
            .total_feature_releases = {revised_total_features} |
            .total_bugfix_releases = {revised_total_bugs} |
            .total_hotfix_releases = {revised_total_hotfixes} |
            .total_releases_without_bugs = {revised_total_releases_without_bugs} |
            .average_features_per_release = {average_features_per_release} |
            .average_bugs_per_release = {average_bugs_per_release} |
            .average_hotfixes_per_release = {average_hotfixes_per_release} |
            .cfr_hotfix_to_release = "{cfr_hotfix_to_release} %" |
            .cfr_bugs_to_tasks_ratio = "{cfr_bugs_to_tasks_ratio} %" |
            .cfr_bug_to_feature = "{cfr_bug_to_feature} %" |
            .cfr_bug_release_ratio = "{cfr_bug_release_ratio} %" |
            .last_release.date = "{current_date}" |
            .last_release.total_tickets = {revised_total_tickets} |
            .last_release.features = {number_of_features} |
            .last_release.hotfixes = {number_of_hotfixes} |
            .last_release.bugs = {number_of_bugs} |
            .last_release.is_hotfix = {isHotFix} 
            """

            yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
            os.system(yq_operation)

    else:
        print('Target file does not exist, creating one...')
        create_directory_and_file(target_data_file)

        # assuming this will be the first release
        total_releases = t_releases if existing_codebase else 1
        yaml_content = f"""
        .total_releases = {total_releases} |
        .total_feature_releases = {number_of_features} |
        .total_bugfix_releases = {number_of_bugs} |
        .total_hotfix_releases = {number_of_hotfixes} |
        .total_releases_without_bugs = {total_releases} |
        .average_features_per_release = {calc_avg(number_of_features, total_releases)} |
        .average_bugs_per_release = {calc_avg(number_of_bugs, total_releases)} |
        .average_hotfixes_per_release = {calc_avg(number_of_hotfixes, total_releases)} |
        .cfr_hotfix_to_release = "{calc_cfr_hotfix_to_release( total_releases, number_of_hotfixes)} %" |
        .cfr_bugs_to_tasks_ratio = "0 %" |
        .cfr_bug_to_feature = "0 %" |
        .cfr_bug_release_ratio = "0 %" |
        .last_release.date = "{current_date}" |
        .last_release.total_tickets = 0 |
        .last_release.features = {number_of_features} |
        .last_release.bugs = {number_of_bugs} |
        .last_release.hotfixes = {number_of_hotfixes} |
        .last_release.is_hotfix = {isHotFix} 
        """

        yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
        os.system(yq_operation)

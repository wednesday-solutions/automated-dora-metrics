import os
import yaml
from utils.date import get_current_date
from utils.dir import create_directory_and_file

current_date = get_current_date()

# yields releases.yaml


def calculate_releases(number_of_features, number_of_bugs, number_of_hotfixes, isHotFix='true', target_data_file='metrics/releases.yaml'):
    if os.path.exists(target_data_file):
        print("Found existing target file, updating it with the latest release...")

        # Read the existing YAML content
        with open(target_data_file, "r") as yaml_file:
            release_dataset = yaml.safe_load(yaml_file)
            releases = release_dataset['releases']
            total_releases = releases[len(releases) - 1].get("number")
            current_release = total_releases + 1

            index = len(releases)
            yaml_content = f"""
            .releases["{index}"].number = {current_release} |
            .releases["{index}"].date = "{current_date}" |
            .releases["{index}"].features = {number_of_features} |
            .releases["{index}"].bugs = {number_of_bugs} |
            .releases["{index}"].hotfixes = {number_of_hotfixes} |
            .releases["{index}"].is_hotfix = {isHotFix}
            """

            yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
            os.system(yq_operation)

    else:
        print('Target file does not exist, creating one...')
        create_directory_and_file(target_data_file)

        # assuming this will be the first release
        # total_releases = t_releases if existing_codebase else 1
        total_releases = 1

        yaml_content = f"""
        .releases[0].number = {total_releases} |
        .releases[0].date = "{current_date}" |
        .releases[0].features = {number_of_features} |
        .releases[0].bugs = {number_of_bugs} |
        .releases[0].hotfixes = {number_of_hotfixes} |
        .releases[0].is_hotfix = {isHotFix}
        """

        yq_operation = f"""yq -i '{yaml_content}' {target_data_file}"""
        os.system(yq_operation)

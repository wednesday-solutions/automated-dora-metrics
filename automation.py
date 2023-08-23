import os
import argparse
from utils.git import identify_commits, identify_source
from utils.date import get_current_date
from utils.calcMetrics import calculate_metrics
from utils.calcRelease import calculate_releases


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="python automation.py -p main")
    parser.add_argument("-e", "--existing", default=False,
                        help="When migrating to an existing codebase for the first time, (Default false)")
    parser.add_argument("-p", "--parent", default='main',
                        help="Specify the parent branch (Default = main)")
    args = parser.parse_args()

    parent_branch = args.parent
    existing_codebase = args.existing
    t_releases = 1
    current_date = get_current_date()
    target_data_file = 'metrics/data.yaml'
    target_release_file = 'metrics/release.yaml'
    feature_messages, bug_messages, hotfix_messages = [], [], []
    source_branch = ''
    os.system("git config --global core.ignoreStat true")
    if not existing_codebase:
        source_branch = identify_source()

    feature_messages, bug_messages, hotfix_messages, t_releases = identify_commits(
        existing_codebase=existing_codebase, prev=source_branch, parent=parent_branch)

    number_of_features = len(feature_messages)
    number_of_bugs = len(bug_messages)
    number_of_hotfixes = len(hotfix_messages)
    isHotFix = 'true' if hotfix_messages and not bug_messages and not feature_messages else 'false'
    includesBugs = 'true' if bug_messages else 'false'
    total_tickets = number_of_bugs + number_of_hotfixes + number_of_features
    print('calculating metrics for current release ....')
    calculate_metrics(
        number_of_features=number_of_features,
        number_of_bugs=number_of_bugs,
        number_of_hotfixes=number_of_hotfixes,
        total_tickets=total_tickets,
        t_releases=t_releases,
        existing_codebase=existing_codebase,
        target_data_file=target_data_file, isHotFix=isHotFix, includesBugs=includesBugs)
    calculate_releases(
        number_of_features=number_of_features,
        number_of_bugs=number_of_bugs,
        number_of_hotfixes=number_of_hotfixes,
        target_data_file=target_release_file,
        isHotFix=isHotFix)

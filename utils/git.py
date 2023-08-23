import re
import subprocess


def identify_source():
    branch_name = ''
    git_log_command = "git log --oneline --merges -n 1"  # most recent merge
    git_logs = subprocess.check_output(
        git_log_command, shell=True, text=True).splitlines()

    branch_pattern = re.compile(r'Merge pull request #\d+ from .*?/([^\'"]+)')
    match = re.search(branch_pattern, git_logs[0])

    if match:
        branch_name = match.group(1)
        print("Source Branch name:", branch_name)
    else:
        print("Source Branch not found.")
    return branch_name


def identify_commits(existing_codebase=False, prev='dev', parent='main'):
    hashes = []
    bug_messages = []
    recent_commits = []
    feature_messages = []
    hotfix_messages = []
    recent_git_logs = []
    git_log_command = ''

    feature_pattern = re.compile(
        r'Merge pull request #(\d+) from .*\/(feat|chore|docs)\/.*')
    bug_pattern = re.compile(
        r'Merge pull request #(\d+) from .*\/(fix|bug|bugfix)\/.*')
    hotfix_pattern = re.compile(
        r'Merge pull request #(\d+) from .*\/hotfix\/.*')
    merges_pattern = re.compile(r'Merge pull request #(\d+) from .*{prev}')
    hash_pattern = re.compile(r'\b[0-9a-fA-F]{7,40}\b')

    if existing_codebase:
        # we want all the merges that went in main
        git_log_command = f"""git log --oneline --merges --first-parent {parent}"""
    else:
        git_log_command = 'git log --oneline --merges'
        merges_pattern = re.compile(
            fr'Merge pull request #(\d+) from .*{prev}')

    git_logs = subprocess.check_output(
        git_log_command, shell=True, text=True).splitlines()

    if (existing_codebase == False):
        for log in git_logs:
            if re.search(merges_pattern, log):
                recent_commits.append(log)
        if (len(recent_commits) > 1):
            # release
            for log in recent_commits:
                if re.search(hash_pattern, log):
                    hashes.append(re.findall(hash_pattern, log)[0])
            recent_git_log_command = f"""git log --oneline --merges {hashes[0]}...{hashes[1]}"""
            # the diff between recent two merges may return hotfixes (if any went in between the release)
            # further is the logic to handle this edge case, as hotfixes are standalone

            recent_git_logs = subprocess.check_output(
                recent_git_log_command, shell=True, text=True).splitlines()
        else:
            # hotfix
            recent_git_logs = recent_commits
    else:
        recent_git_logs = git_logs

    t_releases = len(recent_git_logs)

    for log in recent_git_logs:
        if re.search(feature_pattern, log):
            feature_messages.append(log)
        elif re.search(bug_pattern, log):
            bug_messages.append(log)
        elif re.search(hotfix_pattern, log):
            hotfix_messages.append(log)

    # edge case scenario :- hotfixes shouldn't be added as part of general release
    hotfixes = hotfix_messages if not (
        feature_messages or bug_messages) else []

    return feature_messages, bug_messages, hotfixes, t_releases

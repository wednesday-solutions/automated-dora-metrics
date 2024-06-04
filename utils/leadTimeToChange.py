# dora_metrics.py
import os
import requests
import pandas as pd
from datetime import datetime

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# GitHub repository details
REPO_OWNER = 'wednesday-solutions'
REPO_NAME = 'gen-ai-audio'

# GitHub API base URL
BASE_URL = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}'

# Headers for authentication
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}


def fetch_pull_requests(branch):
    url = f'{BASE_URL}/pulls'
    params = {
        'state': 'closed',
        'base': branch
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def fetch_commits(branch):
    url = f'{BASE_URL}/commits'
    params = {'sha': branch}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


def get_commit_date(commit_url):
    response = requests.get(commit_url, headers=HEADERS)
    response.raise_for_status()
    commit_data = response.json()
    return commit_data['commit']['committer']['date']


def calculate_lead_time(pr):
    pr_created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    pr_merged_at = datetime.strptime(pr['merged_at'], '%Y-%m-%dT%H:%M:%SZ')
    lead_time = pr_merged_at - pr_created_at
    return lead_time


def calcLeadTimeToChange(branch='main'):
    # Fetch pull requests merged into the base branch
    prs = fetch_pull_requests(branch)
    lead_times = []
    prCount = len(prs)

    if prCount > 0:
        for pr in prs:
            if pr['merged_at'] is None:
                continue
            lead_time = calculate_lead_time(pr)
            lead_times.append({
                'PR': pr['title'],
                'Lead Time': lead_time.total_seconds() / 3600  # Convert to hours
            })

    # Create a DataFrame for analysis
    df = pd.DataFrame(lead_times)
    print(df)

    # Calculate average lead time
    average_lead_time = df['Lead Time'].mean()
    print(f'Average Lead Time for Changes: {average_lead_time:.2f} hours')
    return average_lead_time

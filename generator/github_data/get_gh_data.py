import requests
import os
from datetime import datetime

def get_github_stats(username, token):
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"

    try:
        user_url = f"https://api.github.com/users/{username}"
        user_response = requests.get(user_url, headers=headers)
        user_response.raise_for_status()
        user_data = user_response.json()

        # Get user's star count
        total_stars = user_data['public_repos']

        # Get user's total PRs
        prs_url = f"https://api.github.com/search/issues?q=is%3Apr+author%3A{username}+is%3Amerged"
        prs_response = requests.get(prs_url, headers=headers)
        prs_response.raise_for_status()
        prs_data = prs_response.json()
        total_prs = prs_data['total_count']

        # Get user's total issues
        issues_url = f"https://api.github.com/search/issues?q=type%3Aissue+author%3A{username}+is%3Aclosed"
        issues_response = requests.get(issues_url, headers=headers)
        issues_response.raise_for_status()
        issues_data = issues_response.json()
        total_issues = issues_data['total_count']

        # Generate the SVG string
        svg_template = """<svg width="320" height="80" xmlns="http://www.w3.org/2000/svg">
          <rect width="100%" height="100%" fill="#0d1019" />
          <text x="10" y="18" font-weight="bold" font-size="15" fill="#EEE" font-family="monospace">{username}'s GitHub Stats</text>
          <text x="25" y="34" fill="#99F" font-size="12" font-family="monospace">Total Earned Stars: {total_stars}</text>
          <text x="25" y="48" fill="#99F" font-size="12" font-family="monospace">Total PRs: {total_prs}</text>
          <text x="25" y="62" fill="#99F" font-size="12" font-family="monospace">Total Issues: {total_issues}</text>
        </svg>
        """.format(username=username, total_stars=total_stars, total_prs=total_prs, total_issues=total_issues)

        # Write the SVG to a file
        with open("./mini_boards/github_stats.svg", "w") as file:
            file.write(svg_template)

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    github_username = "KKtheGhost"
    github_token = os.environ.get("GH_TOKEN")

    get_github_stats(github_username, github_token)

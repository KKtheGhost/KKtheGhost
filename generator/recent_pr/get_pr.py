import requests
import os

def truncate_string(s, max_length):
    return s if len(s) <= max_length else s[:max_length-3] + "..."

def get_github_pull_requests(url):
    token = os.environ.get("GH_TOKEN")
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        pull_requests = data['items'][:5]  # Get the first 5 PRs

        # Generate the SVG string
        svg_template = """<svg width="320" height="130" xmlns="http://www.w3.org/2000/svg">
          <rect width="100%" height="100%" fill="#0d1019" />
          <text x="10" y="18" font-weight="bold" font-size="15" fill="#EEE" font-family="monospace">Recent Pull Request</text>
          {pr_data}
        </svg>
        """

        pr_data = ""
        y_position = 35
        for pr in pull_requests:
            title = pr['title']
            url = pr['html_url']
            truncated_title = truncate_string(title, 52)
            pr_data += f'<a href="{url}">\n'
            pr_data += f'    <text x="25" y="{y_position}" fill="#99F" font-size="12" font-family="monospace">{truncated_title}</text>\n'
            pr_data += '</a>\n'
            y_position += 17

        svg_content = svg_template.format(pr_data=pr_data)

        # Write the SVG to a file
        with open("./mini_boards/pr.svg", "w") as file:
            file.write(svg_content)

    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            print("Error: 404 Not Found. Check if the URL is correct or you have access to the repository.")
        else:
            print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    url = "https://api.github.com/search/issues?q=is%3Apr+author%3AKKtheGhost+archived%3Afalse+is%3Amerged"

    get_github_pull_requests(url)

import requests
import os
from datetime import datetime

def get_wakapi_stats(username, token):
    headers = {}
    if token:
        headers['Authorization'] = f"Bearer {token}"

    try:
        # Get user's Wakapi stats
        wakapi_url = f"https://wakapi.dev/api/v1/users/{username}/stats/30_days"
        wakapi_response = requests.get(wakapi_url, headers=headers)
        wakapi_response.raise_for_status()
        wakapi_data = wakapi_response.json()

        # Extract monthly coding time data
        monthly_coding_time = wakapi_data.get('data', {}).get('languages', [])
        max_languages = min(10, len(monthly_coding_time))

        # Generate the SVG string
        svg_template = """<svg width="320" height="{height}" xmlns="http://www.w3.org/2000/svg">
          <rect width="100%" height="100%" fill="#0d1019" />
          <text x="10" y="18" font-weight="bold" font-size="15" fill="#EEE" font-family="monospace">{username}'s Monthly Coding Time</text>
          <text x="25" y="34" font-weight="bold" fill="#CCF" font-size="12" font-family="monospace">Total Coding Time: </text>
          <text x="185" y="34" font-weight="bold" fill="#CCF" font-family="monospace">| {total_coding_time}</text>
          {lang_info}
        </svg>
        """.format(
            username=username,
            total_coding_time=wakapi_data.get('data', {}).get('human_readable_total', 0),
            height=180,  # Adjust the height based on the number of languages
            lang_info="\n".join([
                '<text x="25" y="{y}" fill="#99F" font-size="12" font-family="monospace">{lang_name}: </text>'.format(
                    y=48 + i * 14,
                    lang_name=lang.get('name', 0)
                ) + '<text x="185" y="{y}" fill="#99F" font-size="12" font-family="monospace">| {coding_time} </text>'.format(
                    y=48 + i * 14,
                    coding_time=lang.get('text', 0)
                ) for i, lang in enumerate(monthly_coding_time[:max_languages])
            ])
        )

        # Write the SVG to a file
        with open("./mini_boards/wakapi_stats.svg", "w") as file:
            file.write(svg_template)

    except requests.exceptions.HTTPError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    wakapi_username = "kivinsae"
    wakapi_token = os.environ.get("WAKAPI_TOKEN")

    get_wakapi_stats(wakapi_username, wakapi_token)

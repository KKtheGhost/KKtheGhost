import requests
import feedparser

def truncate_string(s, max_length):
    return s if len(s) <= max_length else s[:max_length-3] + "..."

def get_latest_blog_posts(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        entries = feed.entries[:3]  # Get the latest 3 posts

        # Generate the SVG string
        svg_template = """<svg width="320" height="80" xmlns="http://www.w3.org/2000/svg">
          <rect width="100%" height="100%" fill="#0d1019" />
          <text x="10" y="18" font-weight="bold" font-size="15" fill="#EEE" font-family="monospace">Latest Blog Posts</text>
          {post_data}
        </svg>
        """

        post_data = ""
        y_position = 35
        for entry in entries:
            title = entry.title
            link = entry.link
            truncated_title = truncate_string(title, 32)
            post_data += f'<a href="{link}">\n'
            post_data += f'    <text x="25" y="{y_position}" fill="#99F" font-size="12" font-family="monospace">{truncated_title}</text>\n'
            post_data += '</a>\n'
            y_position += 14

        svg_content = svg_template.format(post_data=post_data)

        # Write the SVG to a file
        with open("./mini_boards/blog_posts.svg", "w") as file:
            file.write(svg_content)

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    rss_feed_url = "https://www.kivinsae.com/atom.xml"

    get_latest_blog_posts(rss_feed_url)

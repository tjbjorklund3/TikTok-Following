import os
import csv
import requests
from bs4 import BeautifulSoup

def extract_users_from_html(html: str):
    """
    Parse the given HTML of your TikTok Following page and return
    a list of dicts, each dict containing:
      - display_name
      - user_handle
      - avatar_url
    """

    soup = BeautifulSoup(html, "html.parser")

    # Find all <li> elements that represent a user
    user_containers = soup.find_all("li")

    user_data = []
    for user_container in user_containers:
        # Extract the name
        name_tag = user_container.select_one("span.css-k0d282-SpanNickname.es616eb6")
        display_name = name_tag.get_text(strip=True) if name_tag else None

        # Extract the handle
        handle_tag = user_container.select_one("p.css-3gbgjv-PUniqueId.es616eb8")
        user_handle = handle_tag.get_text(strip=True) if handle_tag else None

        # Extract the avatar image URL
        avatar_tag = user_container.select_one("img.css-1zpj2q-ImgAvatar.e1e9er4e1")
        avatar_url = avatar_tag["src"] if avatar_tag else None

        # Only append if we actually found a handle or name
        if display_name or user_handle:
            user_data.append({
                "display_name": display_name,
                "user_handle": user_handle,
                "avatar_url": avatar_url,
            })

    return user_data


def download_avatars(user_data, avatar_folder="avatars"):
    """
    For each user in user_data, download their avatar to the specified folder
    and add a 'local_avatar_path' key to the user's dict.
    """
    os.makedirs(avatar_folder, exist_ok=True)

    for user in user_data:
        handle = user["user_handle"] or "unknown_handle"
        avatar_url = user["avatar_url"]
        if not avatar_url:
            user["local_avatar_path"] = None
            continue

        # Create a safe filename from the handle
        safe_filename = handle.replace("/", "_").replace("\\", "_")
        local_path = os.path.join(avatar_folder, f"{safe_filename}.jpg")

        # Download
        try:
            resp = requests.get(avatar_url, timeout=10)
            resp.raise_for_status()
            with open(local_path, "wb") as f:
                f.write(resp.content)
            user["local_avatar_path"] = local_path
        except Exception as e:
            print(f"Failed to download avatar for {handle}: {e}")
            user["local_avatar_path"] = None


def create_html_table(user_data, html_output="following_table.html"):
    """
    Build an HTML file with a table containing the user's avatar, display name, and handle.
    """
    html_head = """\
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>TikTok Following</title>
    <style>
    table {
        border-collapse: collapse;
        width: 800px;
        margin: 20px auto;
        font-family: sans-serif;
    }
    th, td {
        border: 1px solid #ccc;
        padding: 8px 12px;
        text-align: left;
        vertical-align: middle;
    }
    thead {
        background-color: #f2f2f2;
    }
    img {
        max-width: 60px;
        max-height: 60px;
        border-radius: 50%;
        object-fit: cover;
    }
    tr:nth-child(even) {
        background-color: #fafafa;
    }
    </style>
</head>
<body>
    <h2 style="text-align:center;">TikTok Following</h2>
    <table>
        <thead>
            <tr>
                <th>Avatar</th>
                <th>Display Name</th>
                <th>User Handle</th>
            </tr>
        </thead>
        <tbody>
"""

    rows = []
    for user in user_data:
        display_name = user["display_name"] or ""
        user_handle = user["user_handle"] or ""
        avatar_path = user.get("local_avatar_path", "") or ""
        avatar_html = f'<img src="{avatar_path}" alt="Avatar">' if avatar_path else "No Avatar"

        row = f"""
            <tr>
                <td>{avatar_html}</td>
                <td>{display_name}</td>
                <td>{user_handle}</td>
            </tr>
        """
        rows.append(row)

    html_tail = """\
        </tbody>
    </table>
</body>
</html>
"""

    full_html = html_head + "\n".join(rows) + html_tail
    with open(html_output, "w", encoding="utf-8") as f:
        f.write(full_html)


def write_csv(user_data, csv_output="following.csv"):
    """
    Write the user data to a CSV file.
    """
    with open(csv_output, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Display Name", "User Handle", "Avatar URL", "Local Avatar Path"])
        for user in user_data:
            writer.writerow([
                user["display_name"],
                user["user_handle"],
                user["avatar_url"],
                user.get("local_avatar_path", "")
            ])


def main():
    # 1. Load your 'following.html'
    input_file = "following.html"
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found!")
        return

    with open(input_file, "r", encoding="utf-8") as f:
        html_snippet = f.read()

    # 2. Parse user data
    user_data = extract_users_from_html(html_snippet)
    print(f"Found {len(user_data)} users in {input_file}.")

    # 3. Download avatars
    download_avatars(user_data, avatar_folder="avatars")

    # 4. Create an HTML table
    create_html_table(user_data, html_output="following_table.html")
    print("HTML table created: following_table.html")

    # 5. Create a CSV
    write_csv(user_data, csv_output="following.csv")
    print("CSV file created: following.csv")


if __name__ == "__main__":
    main()

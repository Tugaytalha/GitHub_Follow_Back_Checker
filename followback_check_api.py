import gradio as gr
import requests
from typing import Set, Union

API_BASE_URL = "https://api.github.com"


def fetch_paginated_data(
        token: str,
        endpoint: str
) -> list:
    """
    Fetch all paginated data from a given GitHub API endpoint
    using a personal access token for authentication.

    Args:
        token (str): Personal Access Token for GitHub.
        endpoint (str): Endpoint path, e.g. '/users/{username}/followers'.

    Returns:
        list: A combined list of items from all pages.
    """
    headers = {
        "Authorization": f"token {token.strip()}",
        "Accept": "application/vnd.github+json"
    }
    data = []
    url = f"{API_BASE_URL}{endpoint}"

    while url:
        response = requests.get(url, headers=headers)

        # Basic error handling
        if response.status_code == 403:
            raise PermissionError("403 Forbidden – You may be rate-limited or token doesn't have proper scope.")
        if response.status_code == 404:
            raise ValueError("404 Not Found – The specified user or endpoint may not exist.")
        if not response.ok:
            raise RuntimeError(f"API request failed with status {response.status_code} ({response.reason})")

        page_items = response.json()
        data.extend(page_items)

        # Check if there's a 'next' link in the response
        links = response.links
        if "next" in links:
            url = links["next"]["url"]
        else:
            url = None

    return data


def get_followers(token: str, username: str) -> Set[str]:
    """
    Get the set of followers for the given username.

    Args:
        token (str): Personal Access Token.
        username (str): GitHub username.

    Returns:
        set of str: Set of follower login names.
    """
    endpoint = f"/users/{username}/followers"
    followers_data = fetch_paginated_data(token, endpoint)
    return {item["login"] for item in followers_data if "login" in item}


def get_following(token: str, username: str) -> Set[str]:
    """
    Get the set of users the given username is following.

    Args:
        token (str): Personal Access Token.
        username (str): GitHub username.

    Returns:
        set of str: Set of following login names.
    """
    endpoint = f"/users/{username}/following"
    following_data = fetch_paginated_data(token, endpoint)
    return {item["login"] for item in following_data if "login" in item}


def find_non_mutual_follows(token: str, username: str) -> Union[str, Set[str]]:
    """
    Determine which users 'username' follows but who do not follow them back.

    Args:
        token (str): Personal Access Token.
        username (str): GitHub username.

    Returns:
        set of str: Sorted list of login names who don't follow back
        or a string message on error.
    """
    try:
        # Fetch sets of followers and following
        followers = get_followers(token, username)
        following = get_following(token, username)

        # Perform set difference to find non-mutual
        not_following_back = following - followers

        if not not_following_back:
            return set()  # or an empty set to indicate none found
        return not_following_back

    except Exception as e:
        return f"Error: {str(e)}"


def check_follows(username: str, token: str) -> str:
    """
    Gradio interface function: returns a user-friendly message
    about who isn't following 'username' back.
    """
    username = username.strip()
    token = token.strip()

    if not username:
        return "Error: Please provide a valid GitHub username."
    if not token:
        return (
            "Error: Personal Access Token is required.\n"
            "Visit https://github.com/settings/tokens to create one."
        )

    result = find_non_mutual_follows(token, username)

    if isinstance(result, str) and result.startswith("Error:"):
        return result  # Pass along the error message

    if not result:
        return f"All users you follow are following you back (or the lists are empty)."

    # Convert the set to a sorted list for consistent display
    sorted_result = sorted(list(result))
    return "These users do NOT follow you back:\n" + "\n".join(sorted_result)


# ---------------------------------------------------------------------
# Gradio App
# ---------------------------------------------------------------------
with gr.Blocks() as app:
    gr.Markdown("# GitHub Follow Checker (API Version)")
    gr.Markdown(
        "Enter your GitHub username and a Personal Access Token (PAT) with at least `read:user` scope."
    )

    with gr.Row():
        username_input = gr.Textbox(label="GitHub Username", placeholder="octocat")
        token_input = gr.Textbox(
            label="Personal Access Token (PAT)",
            type="password",
            placeholder="ghp_xxx... (keep this private)"
        )

    result_output = gr.Textbox(label="Result", lines=10)
    check_button = gr.Button("Check")

    # When check_button is clicked, call check_follows(username, token)
    check_button.click(
        fn=check_follows,
        inputs=[username_input, token_input],
        outputs=result_output
    )

if __name__ == "__main__":
    # Launch the Gradio interface
    app.launch()

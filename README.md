# GitHub Follow Checker with Unfollow Feature

The **GitHub Follow Checker** is a Python application that helps you manage your GitHub following list. It can identify users who do not follow you back and provides an option to unfollow them. The project offers two implementations:
1. **API-Based Implementation** (recommended for stability and compliance).
2. **Selenium-Based Implementation** (for scenarios where API tokens or permissions are unavailable).

---

## Features

1. **Non-Mutual Follow Detection**:
   - Fetches and compares your followers and following lists.
   - Identifies users you follow but who do not follow you back.

2. **Unfollow Users**:
   - Allows you to unfollow non-mutual follows directly via the API or Selenium.

3. **Two Implementations**:
   - **API Version**: Uses the GitHub REST API for reliable and efficient operations.
   - **Selenium Version**: Scrapes GitHub's web interface for followers and following.

4. **Web-Based Interface**:
   - Built with **Gradio** for a simple and user-friendly UI.

---

## Prerequisites

1. **Python**: Install Python 3.7 or newer.
2. **Dependencies**:
   - Install the required libraries:
     ```bash
     pip install requests gradio selenium
     ```
   - For Selenium, download the appropriate WebDriver (e.g., [ChromeDriver](https://sites.google.com/chromium.org/driver/)) and ensure it's in your PATH.
3. **GitHub Personal Access Token (PAT)** (API Version Only):
   - Create a PAT from [GitHub Token Settings](https://github.com/settings/tokens).
   - Select only the following scopes:
     - `read:user`: To fetch followers and following lists.
     - `user:follow`: To enable unfollow actions.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/github-follow-checker.git
   cd github-follow-checker
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python github_follow_checker.py
   ```

4. **Access the App**:
   - Open the link displayed in the terminal (e.g., `http://127.0.0.1:7860`) in your browser.

---

## Usage

### 1. **Check Non-Mutual Follows**
   - Enter your GitHub username and, if using the API version, your **Personal Access Token (PAT)**.
   - Click **"Check Non-Mutual Follows"**.
   - The app will:
     - Display users who do not follow you back.
     - Automatically populate the "Users to Unfollow" list.

### 2. **Unfollow Users**
   - Review or edit the pre-filled usernames in the **"Users to Unfollow"** box.
   - Click **"Unfollow Users"**.
   - The app will:
     - Unfollow the specified users.
     - Display success/error messages for each unfollow action.

---

## Implementation Details

### API-Based Implementation (Recommended)

#### API Endpoints Used:
1. **GET /users/{username}/followers**:
   - Fetches the followers of a given user.
2. **GET /users/{username}/following**:
   - Fetches the users a given user is following.
3. **DELETE /user/following/{username}**:
   - Unfollows a specified user.

#### Advantages:
- **Stability**: Works reliably without worrying about changes in GitHub's web layout.
- **Efficiency**: Handles large lists with pagination.
- **Security**: Adheres to GitHub’s API usage policies.

---

### Selenium-Based Implementation

The Selenium version scrapes GitHub's web interface to fetch followers and following data. It uses the browser automation capabilities of Selenium and a WebDriver (e.g., ChromeDriver).

#### Steps:
1. **Login to GitHub** (manually or via automation):
   - Navigate to the followers and following pages.
   - Scrape usernames using XPaths:
     - **Followers XPath**: `//*[@id="user-profile-frame"]/div/div[X]/div[2]/a/span[2]`
     - **Following XPath**: `//*[@id="user-profile-frame"]/div/div[X]/div[2]/a/span[2]`
   - Use pagination to iterate through lists if necessary.
2. **Compare Followers and Following**:
   - Identify users you follow but who do not follow you back.
3. **Unfollow Actions** (if required):
   - Automate clicks on the "Unfollow" button for each non-mutual follow.

#### Requirements:
- **WebDriver**: Ensure ChromeDriver (or equivalent) is installed and available in your PATH.
- **Selenium Library**: Install using:
  ```bash
  pip install selenium
  ```

#### Advantages:
- Useful when API tokens are unavailable or when access is restricted.
- No need for PAT setup.

#### Limitations:
- Sensitive to changes in GitHub's web structure.
- Requires manual login or session handling for private profiles.

---

## Project Structure

```
github-follow-checker/
│
├── github_follow_checker.py  # Main application script for API version
├── selenium_follow_checker.py # Selenium-based implementation (optional)
├── requirements.txt          # Required Python dependencies
├── README.md                 # Project documentation
```

---

## Security

- **Minimal Permissions**:
  - API tokens require only `read:user` and `user:follow` scopes.
- **Token Safety**:
  - Tokens are not stored. They are used only during the session.
  - Do not share your PAT with anyone.

---

## Limitations

1. **API Rate Limits**:
   - **Authenticated Requests**: 5,000 requests/hour.
   - Large lists may hit these limits.

2. **Selenium Limitations**:
   - Dependent on GitHub's web layout.
   - Susceptible to rate limits and CAPTCHAs.

---

## Future Enhancements

- Add support for saving results to files (e.g., CSV or JSON).
- Integrate advanced error handling for Selenium, such as CAPTCHA bypass.
- Enhance performance for large accounts by adding multi-threading support.

---

## Contributing

I don't know if there will be even 1 person who reads this far, but if you want to contribute:
1. Fork the repository.
2. Create a new feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push to your fork.
4. Submit a pull request to the main repository.

---

## License

This project is licensed under the [Apeache v2 License](LICENSE).

---

## Support

For issues or feature requests, please open an issue in the [GitHub repository](https://github.com/Tugaytalha/github-follow-checker/issues).

---

## Acknowledgments

- **Gradio**: For providing an easy-to-use library for building the web interface.
- **Selenium**: For enabling browser-based automation.
- **GitHub API**: For seamless access to GitHub data.
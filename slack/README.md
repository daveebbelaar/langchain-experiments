# Slack AI Assistant with Python & LangChain

Here's a step-by-step guide to creating a Slack bot, installing it in a workspace, setting up a Python code with Flask, and using ngrok.

Interacting with AI agents via Slack provides a more natural way of communication and provides an integration with your team's workflow and allows for the integration of multiple bots for various tasks. This can improve efficiency and streamline communication, while also allowing the AI agents to become an integral part of your team.

## Part 1 — Slack Setup

#### 1. Create a new Slack app

- Choose an existing Slack workspace or create a new one.
- Go to [https://api.slack.com/apps](https://api.slack.com/apps) and sign in with your Slack account.
- Click "Create New App" and provide an app name and select your workspace as the development workspace. Click "Create App".

#### 2. Set up your bot

- Under the "Add features and functionality" section, click on "Bots".
- Click "Add a Bot User" and fill in the display name and default username. Save your changes.

#### 3. Add permissions to your bot

- In the left sidebar menu, click on "OAuth & Permissions".
- Scroll down to "Scopes" and add the required bot token scopes. For this example, you'll need at least `app_mentions:read`, `chat:write`, and `channels:history`.

#### 4. Install the bot to your workspace

- In the left sidebar menu, click on "Install App".
- Click "Install App to Workspace" and authorize the app.

#### 5. Retrieve the bot token

- After installation, you'll be redirected to the "OAuth & Permissions" page.
- Copy the "Bot User OAuth Access Token" (it starts with `xoxb-`). You'll need it for your Python script.

## Part 2 — Python Setup

#### 1. Set up your Python environment

- Install Python 3.6 or later (if you haven't already).
- Install the required packages: `slack-sdk`, `slack-bolt`, and `Flask`. You can do this using pip:

```other
pip install slack-sdk slack-bolt Flask
```

In addition to the steps you provided, you can also create a virtual environment to isolate the dependencies of your Python app from other projects on your machine. Here are the steps to create a virtual environment using `venv` or `conda` and install the required packages:

Using `venv`:

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install slack-sdk slack-bolt Flask
```

Using `conda`:

```other
conda create --name myenv python=3.8
conda activate myenv
pip install slack-sdk slack-bolt Flask
```

#### 2. Create the Python script with Flask

- Create a new Python file (e.g., `app.py`) and insert the code from [`app.py`](https://github.com/daveebbelaar/langchain-experiments/blob/main/slack/app.py) in this repository.
- If you want to use a free version, you can explore the others supported [LangChain's Model](https://python.langchain.com/en/latest/modules/models/llms/integrations.html).

#### 3. Set the environment variable in the .env file

- Create a .env file in your project directory and add the following keys:

```yaml
SLACK_BOT_TOKEN = "xoxb-your-token"
SLACK_SIGNING_SECRET = "your-secret"
SLACK_BOT_USER_ID = "your-bot-id"
OPENAI_API_KEY= "your-openai-key"
```

#### 4. Start your local Flask server

- Run the Python script in the terminal (macOS/Linux) or Command Prompt (Windows): `python app.py` The server should start, and you'll see output indicating that it's running on [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Part 3 — Server Setup (Local)

#### 1. Expose your local server using ngrok

- If you haven't installed ngrok, you can download it from [https://ngrok.com/download](https://ngrok.com/download) or, on macOS, install it via Homebrew by running: `brew install ngrok`
- In a new terminal (macOS/Linux) or Command Prompt (Windows), start ngrok by running the following command: `ngrok http 5000`
- Note the HTTPS URL provided by ngrok (e.g., [https://yoursubdomain.ngrok.io](https://yoursubdomain.ngrok.io/)). You'll need it for the next step.

Remember that if you installed ngrok via Homebrew, you can run `ngrok http 5000` from any directory in the terminal. If you downloaded it from the website, navigate to the directory where ngrok is installed before running the command.

#### 2. Configure your Slack app with the ngrok URL

- Go back to your Slack app settings at [https://api.slack.com/apps](https://api.slack.com/apps).
- Click on "Event Subscriptions" in the left sidebar menu.
- Enable events and enter your ngrok URL followed by `/slack/events` (e.g., [https://yoursubdomain.ngrok.io/slack/events](https://yoursubdomain.ngrok.io/slack/events)).
- Scroll down to "Subscribe to bot events" and click "Add Bot User Event". Add the `app_mention` event and save your changes.

>**Note**
> Please note that every time you restart ngrok in the terminal, you have to update the URL in Slack — this is just for testing.

#### 3. Reinstall your Slack app to update the permissions

- In the left sidebar menu, click on "Install App".
- Click "Reinstall App to Workspace" and authorize the app.

#### 4. Add your bot to a Slack channel

- Type `/invite @bot-name` in the channel.

## Part 4 — Add Custom Functions

#### 1. Create a function to draft emails

- Create a new file called `functions.py` and insert the code from [`functions.py`](https://github.com/daveebbelaar/langchain-experiments/blob/main/slack/functions.py)
- Import the function in your `app.py` file with `from functions import draft_email`.
- And update the `handle_mentions` function.

#### 2. Come up with your own ideas

- What are you going to make with this?

## Troubleshooting

> **Warning**
> Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.

To close a port on a Mac, you need to identify the program or process that is using the port and then stop that program or process. Here are the steps you can follow:

1. Open the Terminal application on your Mac.
2. Run the following command to list all open ports and the processes that are using them:

```bash
sudo lsof -i :<port_number>
```

Replace `<port_number>` with the port number that you want to close.

3. Look for the process ID (PID) of the program that is using the port in the output of the `lsof` command.
4. Run the following command to stop the program or process:

```bash
kill <PID>
```

Replace `<PID>` with the process ID that you obtained in the previous step.

5. Verify that the port is no longer in use by running the `lsof` command again.

```bash
sudo lsof -i :<port_number>
```

If the port is no longer in use, the command should not return any output.

Note that you may need to run the `lsof` and `kill` commands with `sudo` privileges if the program or process is owned by another user or requires elevated privileges.

## Datalumina

This document is provided to you by Datalumina. We help data analysts, engineers, and scientists launch and scale a successful freelance business — $100k+ /year, fun projects, happy clients. If you want to learn more about what we do, you can visit our [website](https://www.datalumina.io/) and subscribe to our [newsletter](https://www.datalumina.io/newsletter). Feel free to share this document with your data friends and colleagues.

## Tutorials
For video tutorials on how to use the LangChain library and run experiments, visit the YouTube channel: [youtube.com/@daveebbelaar](youtube.com/@daveebbelaar)


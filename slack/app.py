from flask import Flask, request, abort
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
import os
import time
import logging

# Configure the logging level and format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET)

# Initialize the Flask app
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

def verify_slack_request():
    timestamp = request.headers.get("X-Slack-Request-Timestamp", "")
    signature = request.headers.get("X-Slack-Signature", "")
    current_timestamp = int(time.time())
    if abs(current_timestamp - int(timestamp)) > 60 * 5:
        return False
    return signature_verifier.is_valid(
        body=request.get_data().decode("utf-8"),
        timestamp=timestamp,
        signature=signature,
    )

@app.event("app_mention")
def handle_mentions(body, say):
    text = body["event"]["text"]
    text = text.replace(f"<@{app.bot_id}>", "").strip()
    logging.info("Received text: " + text.replace("\n", " "))
    say("Sure, I'll get right on that!")
    response = draft_email(text)  # Assuming draft_email function is defined elsewhere
    logging.info("Generated response: " + response.replace("\n", " "))
    say(response)

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    if not verify_slack_request():
        abort(403)
    return handler.handle(request)

if __name__ == "__main__":
    logging.info("Flask app started")
    flask_app.run(host="0.0.0.0", port=8000)

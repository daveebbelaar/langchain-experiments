from flask import Flask, request, jsonify
from your_script import draft_email  # Assuming your_script is the name of the script where draft_email is defined

app = Flask(__name__)

@app.route('/draft_email', methods=['POST'])
def handle_draft_email():
    data = request.get_json()
    user_input = data.get('user_input')
    name = data.get('name', 'Ben')  # Default name is 'Ben' if not provided
    response = draft_email(user_input, name)
    return jsonify(response)

@app.route('/slack_action', methods=['POST'])
def handle_slack_action():
    data = request.get_json()
    action = data.get('action')
    # Here you can handle different Slack actions based on the 'action' value
    # For example, if action is 'Send Direct Message', you can call the corresponding function
    # Make sure to implement these functions according to your needs
    if action == 'Send Direct Message':
        return handle_send_direct_message(data)
    elif action == 'Create Channel':
        return handle_create_channel(data)
    # Add more elif statements for other actions
    else:
        return jsonify({'error': 'Unknown action'}), 400

if __name__ == '__main__':
    app.run(debug=True)

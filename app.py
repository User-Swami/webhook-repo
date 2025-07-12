from flask import Flask, request, render_template, jsonify
from models import insert_event, get_latest_events
from bson.json_util import dumps

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')

    if event_type == "push":
        insert_event("PUSH", data['pusher']['name'], None, data['ref'].split('/')[-1])

    elif event_type == "pull_request":
        action = data['action']
        if action == "opened":
            insert_event("PULL_REQUEST",
                         data['pull_request']['user']['login'],
                         data['pull_request']['head']['ref'],
                         data['pull_request']['base']['ref'])

        elif action == "closed" and data['pull_request']['merged']:
            insert_event("MERGE",
                         data['pull_request']['user']['login'],
                         data['pull_request']['head']['ref'],
                         data['pull_request']['base']['ref'])

    return jsonify({"status": "received"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = get_latest_events()
    return dumps(events), 200

if __name__ == '__main__':
    app.run(debug=True)

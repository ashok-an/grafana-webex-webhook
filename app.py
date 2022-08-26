import json
import os
from flask import Flask, request, jsonify
from webexteamssdk import WebexTeamsAPI

roomId = os.getenv('WEBEX_ROOM_ID', '<no room id>')
token = os.getenv('WEBEX_TOKEN', '<no webex token>')

api = WebexTeamsAPI(access_token=token)
def send_message_to_room(room_id, message):
    api.messages.create(roomId=room_id, markdown=message)
    return

app = Flask(__name__)

@app.route('/healthz', methods=['GET'])
def healthz():
    return {'message': 'ok'}

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_json()
    alert0 = payload.get('alerts', [])[0]
    summary = alert0.get('annotations', {}).get('summary', '<no summary>')
    panelUrl = alert0.get('panelUrl', '')
    labels = str(alert0.get('labels', {}))
    startsAt = alert0.get('startsAt', '<no time>').split('.')[0]
    valueString = alert0.get('valueString', '<no value>')
    title = f"#### 🚩 {payload.get('title', '<no title>')}"

    #print(json.dumps(data, sort_keys=True, indent=2))
    #return jsonify(payload)

    message = f"""{title}
---
- Labels:   {labels}
- ValueString:  {valueString}
- Summary:  {summary}
- Timestamp: {startsAt}
"""
    if panelUrl:
        message = f"{message}\n---{panelUrl}"

    print(f"Message: {message}")
    send_message_to_room(roomId, message)
    return {'message': 'ok'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

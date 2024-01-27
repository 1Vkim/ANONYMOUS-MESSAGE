import os
import time
import sys
import json
import requests
from flask import Flask, render_template, request


app = Flask(__name__)



@app.route('/discord_webhook', methods=['POST'])
def discord_webhook():
      data = request.form['anon_msg']
      webhook_url = os.environ['DISCORD']
      message_content = f"New anon message- {data}"
        # Send the message to Discord
      requests.post(webhook_url, json={'content': message_content})

      response = requests.post(webhook_url, json={'content': message_content})

      if response.status_code == 429:
          # Rate limit exceeded, wait and retry
          retry_after = int(response.headers['Retry-After'])
          time.sleep(retry_after)
          send_discord_message(webhook_url, message_content)
      elif response.status_code != 200:
          print(f"Failed to send message. Status Code: {response.status_code}, Response: {response.text}")



      return render_template('anon.html', success=True)
@app.route('/')
def index():

  page=""
  f = open("templates/anon.html", "r")
  page = f.read()
  f.close()

  return page

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81,debug=True)
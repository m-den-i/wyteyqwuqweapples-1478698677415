import os
import cloudant
from flask import Flask, render_template
import random

app = Flask(__name__)

username = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
host = os.environ.get('DB_HOST', '{username}.cloudant.com'.format(username=username))
url = "https://{username}:{password}@{host}".format(username=username, password=password, host=host)
client = cloudant.Cloudant(username, password, account=username, url=url)
client.connect()
db = client['ibase']


@app.route('/')
def Welcome():
    docs = [doc for doc in db]
    return render_template('index.html', joke=random.choice(docs))


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))

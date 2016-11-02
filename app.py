import os
import cloudant
from flask import Flask, render_template, request
import random
from watson_developer_cloud import AlchemyLanguageV1

app = Flask(__name__)

username = os.environ['DB_USERNAME']
password = os.environ['DB_PASSWORD']
host = os.environ.get('DB_HOST', '{username}.cloudant.com'.format(username=username))
url = "https://{username}:{password}@{host}".format(username=username, password=password, host=host)
client = cloudant.Cloudant(username, password, account=username, url=url)
client.connect()
db = client['ibase']

alchemy_key = os.environ.get('ALCHEMY_KEY', '')
apples = [doc for doc in db if doc.get('type', '') == 'apple']


@app.route('/')
def index():
    return render_template('index.html', apples=apples)


@app.route('/joke')
def joke():
    docs = [doc for doc in db]
    return render_template('joke.html', joke=random.choice(docs))


@app.route('/recognize', methods=['GET', 'POST'])
def extract_entity():
    kwargs = {}
    if request.method == 'POST':
        alchemy_language = AlchemyLanguageV1(api_key=alchemy_key)

        response = alchemy_language.combined(
            text=request.values['text'],
            extract='entities',
        )
        kwargs = {
            'sentence': request.values['text'],
            'result': response['entities'],
        }
    return render_template('alchemy.html', **kwargs)


port = os.getenv('PORT', '5000')
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(port))

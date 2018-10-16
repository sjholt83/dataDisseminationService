#!flask/bin/python
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)


@app.route('/requestTransfer', methods=['POST'])
def process_request():
    if not request.json:
        abort(400)

    filefingerprint = request.json['guideid']
    priority = request.json['priority']
    token = request.json['oauthtoken']
    destination = request.json['destination']
    transfertype = request.json['transfertype']
    if request.json['transforms']:
        transforms = request.json['transforms']
    else:
        transforms = ""

    r = request.post('https://123.456.789.001/api/proxy', external=True,
                     data={'token': token, 'file': filefingerprint})
    if r.status_code == 200:
        jsonify(r.text)
        if r.json['authorization'] == 'True':
            authorization = True
            fileuri = r.json['fileuri']
            xfer = request.post('https://123.456.789.001/api/' + transfertype, data={'destination': destination,
                                                                                  'fileuri': fileuri, 'priority': priority,
                                                                                  'oauth': token, 'transforms': transforms})
        else:
            authorization = False
    else:
        authorization = False

    return jsonify({'request status code': r.status_code, 'description': r.reason, 'authorization': authorization}), 200


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(threaded=True, debug=True, port=5000)

#!flask/bin/python
from flask import Flask, jsonify, request, make_response
import json

app = Flask(__name__)


@app.route('/api/requestTransfer', methods=['POST'])
def process_request():
    #### Get json request data and store in an object for use
    datapkg = {}
    datapkg['GUID'] = request.json['GUID']
    datapkg['priority'] = request.json['priority']
    datapkg['transfertype'] = request.json['transfertype']
    datapkg['destination'] = request.json['destination']
    datapkg['username'] = request.json['username']
    datapkg['password'] = request.json['password']
    json_data = json.dumps(datapkg)
    print("Incoming Request:")
    print(json_data)

    #### Make Call to Security Service to obtain authorization
    print("Call to Security Service:")
    print(datapkg['GUID'], datapkg['destination'], datapkg['username'])

#    r = request.post('https://123.456.789.001/api/proxy', external=True,
#                     json_data)

    #### Get response from Security Service
    securityResponse = {}
    securityResponse['username'] = datapkg['username']
    securityResponse['GUID'] = datapkg['GUID']
    securityResponse['authorization'] = 'authorized'
    securityResponse['filelocation'] = 'Garage'
    response_data = json.dumps(securityResponse)
    print("Response from Security Service:")
    print(response_data)

    #### Perform logic on response to see if we continue
    print("Check Authorization:")
    if securityResponse['authorization'] != "authorized":
        print("User is not Authorized")
        return("status: " + "500")
    else:
        print("User is Authorized:")
        #### Make call to transfer service for file transfer
        transferRequest = {}
        transferRequest['fileuri'] = securityResponse['filelocation']
        transferRequest['destination'] = datapkg['destination']
        transferRequest['GUID'] = securityResponse['GUID']
        transferRequest['username'] = securityResponse['username']
        transferRequest['password'] = datapkg['password']
        request_data = json.dumps(transferRequest)
        print("Request for Transfer Service:")
        print(request_data)

        #### Mock call to Transfer Service
#       xfer = request.post('https://123.456.789.001/api/' + transfertype, request_data)


#   return jsonify({'request status code': r.status_code, 'description': r.reason, 'authorization': authorization}), 200

    return(request_data)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    app.run(threaded=True, debug=True, port=5000)



from flask import Flask, request
import json
import requests
import os

app = Flask(__name__)

if 'SF_TOKEN' in os.environ:
    print os.environ['SF_TOKEN']
else:
    print 'SF_TOKEN env variable not found'
    sys.exit(0)

@app.route('/hook', methods=['POST'])
def login():
    
    headers = {'X-SF-TOKEN' : os.environ['SF_TOKEN'],'Content-Type' : 'application/json'}
    data = json.loads(request.data)
    if 'event' in data:
        if "start" not in data['event']:
            send_event = {}
            send_event['category']='USER_DEFINED'
            send_event['eventType']='code_build_'+data['event']
            custom_data={'buildName':data['buildName'],'buildUrl':data['buildUrl']}
            send_event['properties']=custom_data
            send_event = [send_event]
            print json.dumps(send_event,indent=2)   
            r = requests.post('https://ingest.signalfx.com/v2/event',headers=headers,data=json.dumps(send_event))
            return(r.text)
    elif 'pusher' in data:
        send_event = {}
        send_event['category']='USER_DEFINED'
        send_event['eventType']='code_push'
        custom_data={'Pusher':data['pusher']['email']}
        send_event['properties']=custom_data
        send_event = [send_event]
        print json.dumps(send_event,indent=2)   
        r = requests.post('https://ingest.signalfx.com/v2/event',headers=headers,data=json.dumps(send_event))
        return(r.text)
    else:
        print data
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)



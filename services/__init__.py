import requests
import cPickle


def api_call(params, port):
    params = cPickle.dumps(params)
    response = requests.post(url='http://142.0.203.36:%d/api' % port, body=params)
    return cPickle.loads(response.content)

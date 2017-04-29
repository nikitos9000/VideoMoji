import requests
import cPickle


def api_call(params, port):
    params = cPickle.dumps(params, protocol=2)
    response = requests.post(url='http://142.0.203.36:%d/api' % port, data=params)
    return cPickle.loads(response.content)

import json
import numpy as np
import collections


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


class NP2Json:
        @staticmethod
        def encode_np_arr(np_arr):
            d=dict(enumerate(np_arr.flatten(), 1))
            json_enc = json.dumps(d, cls=MyEncoder)
            return json_enc

        @staticmethod
        def encode(np_list):
            res = {}
            num = 0
            for np_enc in np_list:
                res[num]=NP2Json.encode_np_arr(np_enc)
                num = num+1
            return json.dumps(res)
                
	
        @staticmethod
        def decode1(json_enc):
            json_decode = json.loads(json_enc)
            res = {int(k): v for k, v in json_decode.items()}
            res = collections.OrderedDict(sorted(res.items()))
            list= [ v for v in res.values() ]
            return np.array(list)

        @staticmethod
        def decode(json_list):
            json_decode = json.loads(json_list)
            result = []
            for (i,json_enc) in sorted(json_decode.items()):
                json_enc = json.loads(json_enc)
                res = {int(k): v for k, v in json_enc.items()}
                res = collections.OrderedDict(sorted(res.items()))
                l= [ v for v in res.values() ]
                result = result + [np.array(l)]
                #print(np.array(l))
            return result



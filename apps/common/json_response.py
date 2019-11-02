import ujson as json


class JSONResponse(object):
    @staticmethod
    def success(data=None):
        resp_data = {
            'code': 1000,
            'message': 'success',
            'data': data
        }

        return json.dumps(resp_data)

    @staticmethod
    def error(err_data):
        resp_data = {
            'code': 2000,
            'message': err_data
        }

        return json.dumps(resp_data)

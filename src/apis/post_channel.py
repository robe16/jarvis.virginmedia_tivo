from bottle import HTTPResponse, HTTPError

from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logException
from resources.global_resources.variables import *
from validation.validation import validate_channel


def post_channel(request, _virginmedia_tivo):
    #
    args = get_request_log_args(request)
    #
    try:
        #
        data_dict = request.json
        #
        if validate_channel(data_dict):
            #
            channel = data_dict['channel']
            if 'plus1' in data_dict:
                plus1 = data_dict['plus1']
            else:
                plus1 = False
            #
            r = _virginmedia_tivo.sendChannel(channel, plus1)
            #
            if not bool(r):
                status = httpStatusFailure
            else:
                status = httpStatusSuccess
        else:
            status = httpStatusBadrequest
        #
        args['result'] = logPass
        args['http_response_code'] = status
        args['description'] = '-'
        log_inbound(**args)
        #
        response = HTTPResponse()
        response.status = status
        #
        return response
        #
    except Exception as e:
        status = httpStatusServererror
        #
        args['result'] = logException
        args['http_response_code'] = status
        args['description'] = '-'
        args['exception'] = e
        log_inbound(**args)
        #
        raise HTTPError(status)

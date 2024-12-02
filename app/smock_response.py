
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from flask import Response, json, make_response


class SmockResponseStatus(Enum):
    SUCCESS='success'
    FAIL='fail'
    ERROR='error'

@dataclass
class SmockResponseFormatter():
    
    httpCode: int
    data: dict

    @property
    def status(self):
        if 200 <= self.httpCode < 400:
            return SmockResponseStatus.SUCCESS
        
        if 400 <= self.httpCode < 500:
            return SmockResponseStatus.FAIL

        if 500 <= self.httpCode < 600:
            return SmockResponseStatus.ERROR

        raise Exception("Non-HTTP status code given")

    @property
    def serialize(self):
        return {
            'status': self.status.value,
            'data': self.data
        }

class SmockResponse(Response):
    """
    Custom Flask Response class to format response to JSend format
    """

    def __init__(
        self,
        data: Optional[Union[dict, list, str]] = None,
        status: Optional[int] = 200,
        mimetype: Optional[str] = 'application/json',
        **kwargs
    ):


        if isinstance(data, (str)):
            if data == "":
                data = None
            else:
                try:
                    data = json.loads(data)
                except ValueError:
                    data = {"message": data}

        response = json.dumps(SmockResponseFormatter(status, data).serialize)



        default_headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': '*'
        }

        headers = kwargs.pop('headers', dict()) or dict()

        headers.update(default_headers)

        super().__init__(
            response=response,
            status=status,
            mimetype=mimetype,
            headers=headers,
            **kwargs
        )

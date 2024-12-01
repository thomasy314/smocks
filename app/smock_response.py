
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
    default_status = 200
    default_mimetype = 'application/json'

    def __init__(
        self,
        data: Optional[Union[dict, list, str]] = None,
        status: Optional[int] = None,
        mimetype: Optional[str] = None,
        **kwargs
    ):

        print("data: ", data)

        if isinstance(data, (str)):
            if data == "":
                data = None
            else:
                try:
                    data = json.loads(data)
                except ValueError:
                    data = {"message": data}

        response = json.dumps(SmockResponseFormatter(200, data).serialize)

        # Initialize parent class
        super().__init__(
            response=response,
            status=status or self.default_status,
            mimetype='application/json',
            **kwargs
        )

from rest_framework.exceptions import APIException


class RetryAgainException(APIException):
    status_code = 409
    default_detail = "Something wierd happened please try again!!."
    default_code = 409

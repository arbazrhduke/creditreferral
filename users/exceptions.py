from rest_framework.exceptions import APIException


class RetryAgainException(APIException):
    """Exception raised in a event of optimistic locking"""
    status_code = 409
    default_detail = "Something weird happened please try again!!."
    default_code = 409

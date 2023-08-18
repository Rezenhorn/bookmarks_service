from rest_framework.exceptions import APIException


class NoHtmlProvided(APIException):
    status_code = 500
    default_detail = 'HTML разметка не найдена на странице.'
    default_code = 'error'


class BadResponse(APIException):
    status_code = 500
    default_detail = 'Ошибка ответа.'
    default_code = 'error'


class EmptyTagsError(APIException):
    status_code = 500
    default_detail = 'Теги не найдены.'
    default_code = 'error'

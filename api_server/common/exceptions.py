from rest_framework import status
from rest_framework.exceptions import APIException


class CustomAPIException(APIException):
    error_code: str
    yasg_description: str
    
class InvalidSocialToken(CustomAPIException):
    error_code = '100010'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '유효하지 않은 Social token'
    yasg_description = '토큰 인증 오류'

    def __init__(self):
        self.__class__.default_code = 'accessToken'
        super().__init__()

class RefreshTokenHasExpired(CustomAPIException):
    error_code = '100011'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '만료된 Refresh Token'
    default_code = 'refreshToken'
    yasg_description = '만료된 Refresh Token'
    

class AlreadyJoined(CustomAPIException):
    error_code = '100000'
    status_code = status.HTTP_409_CONFLICT
    default_detail = '이미 가입한 회원'
    default_code = 'user'
    yasg_description = '이미 가입한 회원'

    

class UnauthenticatedRequestExists(CustomAPIException):
    error_code = '100100'
    status_code = status.HTTP_409_CONFLICT
    default_detail = '아직 인증 대기중인 요청이 있음'
    default_code = 'verificationCode'
    yasg_description = '인증이 완료 되지 않은 요청이 있음'


class InvalidAuthenticatedCode(CustomAPIException):
    error_code = '100101'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '유효하지 않은 인증 요청 아이디'
    default_code = 'verificationId'
    yasg_description = '인증 아이디 오류'
    

class AlreadyAuthenticated(CustomAPIException):
    error_code = '100102'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '이미 완료된 인증 코드'
    default_code = 'verification'
    yasg_description = '이미 완료된 인증 코드'
    

class AuthenticationWasCanceled(CustomAPIException):
    error_code = '100103'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '취소된 인증 요청'
    default_code = 'verification'
    yasg_description = '취소된 인증 요청'
    

class AuthenticationInvalidCode(CustomAPIException):
    error_code = '100104'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '잘못된 인증 코드'
    default_code = 'code'
    yasg_description = '잘못된 인증 코드'
    

class AuthenticationNotComplete(CustomAPIException):
    error_code = '100105'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '인증이 완료 되지 않음'
    default_code = 'verification'
    yasg_description = '인증이 완료 되지 않음'
    

class AuthenticationHadExpired(CustomAPIException):
    error_code = '100104'
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '만료된 인증 요청'
    default_code = 'expired'
    yasg_description = '만료된 인증 요청'
    
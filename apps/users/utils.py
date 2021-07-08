def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'code': 0,
        'token': token,
        'id': user.id,
        'username': user.username
    }

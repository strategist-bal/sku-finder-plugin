from users.models import User


def user_get_me(*, user: User):
    return {
        'id': user.id,
        'uuid': user.uuid,
        'first_name': user.first_name,
        'email': user.email,
        'last_name': user.last_name,
        'username': user.username,
        'dob': user.dob,
        'is_email_verified': user.is_email_verified
    }


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'me': user_get_me(user=user),
    }

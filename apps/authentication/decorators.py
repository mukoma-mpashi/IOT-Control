import logging
from datetime import datetime
from functools import wraps
import jwt
from flask import request, current_app
from apps.authentication.models import Users

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fix_padding(token):
    """Fix padding for base64-encoded tokens if needed."""
    while len(token) % 4 != 0:
        token += '='
    return token

def create_error_response(message, status_code):
    """Helper function to create a consistent error response."""
    return {
        'message': message,
        'data': None,
        'success': False
    }, status_code

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        logger.info(f"Token verification started at {datetime.utcnow()}")

        # Check if 'Authorization' header is present
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            logger.warning('Token is missing or malformed')
            return create_error_response('Token is missing or malformed', 403)

        token = auth_header.split(" ")[1]  # Strip 'Bearer ' prefix

        try:
            # Optionally fix padding if needed
            token = fix_padding(token)

            # Decode the token
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            logger.info(f"Token verified for user_id={payload.get('sub')} at {datetime.utcnow()}")

            # Check if token has expired (optional, since JWT library handles this)
            if 'exp' in payload and datetime.utcnow() > datetime.utcfromtimestamp(payload['exp']):
                logger.warning(f"Token expired for user_id={payload.get('sub')}")
                return create_error_response('Token has expired', 401)

            # Attach user information to the request context
            user = Users.query.get(payload.get('sub'))
            if user is None:
                logger.warning(f"User not found for token with user_id={payload.get('sub')}")
                return create_error_response('User not found', 404)

            # Optionally, attach user information to the request or g context
            request.current_user = user

        except jwt.ExpiredSignatureError:
            logger.warning('Token has expired')
            return create_error_response('Token has expired', 401)
        except jwt.InvalidTokenError as e:
            logger.error(f"Invalid token: {str(e)}")
            return create_error_response('Invalid token', 401)
        except Exception as e:
            logger.error(f"Unexpected error during token verification: {str(e)}")
            return create_error_response(f'Error verifying token: {str(e)}', 500)

        # Continue to the wrapped route function if token is valid
        return func(*args, **kwargs)

    return decorated

import json
import logging
from flask import request, jsonify
from flask_login import current_user
from flask_restx import Api, Resource
from werkzeug.datastructures import MultiDict

from apps import db
from apps.api import blueprint
from apps.authentication.decorators import token_required
from apps.api.forms import APIKeyForm
from apps.models import APIKey

# Set up logging
logging.basicConfig(level=logging.DEBUG)

api = Api(blueprint)


# Route for handling APIKey operations
@api.route('/apikeys/', methods=['POST', 'GET'])
@api.route('/apikeys/<int:model_id>/', methods=['GET', 'DELETE', 'PUT'])
class APIKeyRoute(Resource):

    def get(self, model_id: int = None):
        """Retrieve all API keys or a specific key by ID."""
        logging.debug(f"Received request to retrieve API key(s) with model_id={model_id}")
        try:
            if model_id is None:
                all_objects = APIKey.query.all()
                output = [{'id': obj.id, **obj.to_dict()} for obj in all_objects]
            else:
                obj = APIKey.query.get(model_id)
                if obj is None:
                    logging.warning(f"API key with id={model_id} not found.")
                    return {
                        'message': 'API key not found.',
                        'success': False
                    }, 404
                output = {'id': obj.id, **obj.to_dict()}
            return {
                'data': output,
                'success': True
            }, 200
        except Exception as e:
            logging.error(f"Error retrieving API key(s): {str(e)}")
            return {
                'message': 'Error retrieving API key(s).',
                'success': False
            }, 500

    @token_required
    def post(self):
        """Create a new API key for the current user."""
        logging.debug(f"Received request to create API key for user_id={current_user.id}")
        try:
            # Generate a new cryptographically secure API key
            raw_key = APIKey.generate_key()
            new_key = APIKey.create_api_key(user_id=current_user.id)

            # Save the new API key to the database
            db.session.add(new_key)
            db.session.commit()

            logging.info(f"API key created for user_id={current_user.id}.")
            return {
                'message': 'API Key generated successfully!',
                'key': raw_key,  # Return the raw key once, not the hashed key
                'id': new_key.id,
                'success': True
            }, 201
        except Exception as e:
            logging.error(f"Error creating API key for user_id={current_user.id}: {str(e)}")
            return {
                'message': 'Error creating API key.',
                'success': False
            }, 500

    @token_required
    def put(self, model_id: int):
        """Update an existing API key."""
        logging.debug(f"Received request to update API key with id={model_id}")
        try:
            body_of_req = request.get_json() or request.form
            obj = APIKey.query.get(model_id)

            if obj is None:
                logging.warning(f"API key with id={model_id} not found.")
                return {
                    'message': 'API key not found.',
                    'success': False
                }, 404

            form = APIKeyForm(MultiDict(body_of_req), obj=obj)
            if not form.validate():
                logging.warning(f"Validation failed for API key update with id={model_id}: {form.errors}")
                return {
                    'message': form.errors,
                    'success': False
                }, 400

            # Update the necessary fields
            for field, value in body_of_req.items():
                if hasattr(obj, field):
                    setattr(obj, field, value)

            db.session.commit()

            logging.info(f"API key with id={model_id} updated successfully.")
            return {
                'message': 'API key updated successfully.',
                'success': True
            }, 200
        except Exception as e:
            logging.error(f"Error updating API key with id={model_id}: {str(e)}")
            return {
                'message': 'Error updating API key.',
                'success': False
            }, 500

    @token_required
    def delete(self, model_id: int):
        """Delete an API key."""
        logging.debug(f"Received request to delete API key with id={model_id}")
        try:
            to_delete = APIKey.query.filter_by(id=model_id).first()

            if not to_delete:
                logging.warning(f"API key with id={model_id} not found for deletion.")
                return {
                    'message': 'API key not found.',
                    'success': False
                }, 404

            db.session.delete(to_delete)
            db.session.commit()

            logging.info(f"API key with id={model_id} deleted successfully.")
            return {
                'message': 'API key deleted successfully.',
                'success': True
            }, 200
        except Exception as e:
            logging.error(f"Error deleting API key with id={model_id}: {str(e)}")
            return {
                'message': 'Error deleting API key.',
                'success': False
            }, 500

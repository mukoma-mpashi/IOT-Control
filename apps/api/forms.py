from wtforms import Form
from wtforms_alchemy import model_form_factory
from apps.models import Book, APIKey  # Import the necessary models

ModelForm = model_form_factory(Form)

# Form for the Book model
class BookForm(ModelForm):
    class Meta:
        model = Book

# Form for the APIKey model
class APIKeyForm(ModelForm):
    class Meta:
        model = APIKey

import re
from models.database import Database
from models.inscription import Inscription

class Validator:
    @staticmethod
    def non_empty(*args):
        return all(arg.strip() != "" for arg in args)

    @staticmethod
    def email_valide(email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    @staticmethod
    def telephone_valide(telephone):
        regex = r'^\+?\d{10,15}$'
        return re.match(regex, telephone) is not None

    @staticmethod
    def unique(field, value):
        inscription_model = Inscription()
        result = inscription_model.find_by(field, value)
        return result is None

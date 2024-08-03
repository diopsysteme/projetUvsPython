# controllers/inscription_controller.py

from models.inscription import Inscription
from validation.validator import Validator
from tkinter import messagebox

class InscriptionController:
    def __init__(self):
        self.inscription_model = Inscription()

    def inscrire(self, nom, prenom, email, telephone):
        if not Validator.non_empty(nom, prenom, email, telephone):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return
        if not Validator.email_valide(email):
            messagebox.showerror("Erreur", "Email non valide.")
            return
        if not Validator.telephone_valide(telephone):
            messagebox.showerror("Erreur", "Numéro de téléphone non valide.")
            return
        if not Validator.unique("email", email):
            messagebox.showerror("Erreur", "Email déjà utilisé.")
            return
        if not Validator.unique("telephone", telephone):
            messagebox.showerror("Erreur", "Numéro de téléphone déjà utilisé.")
            return
        
        self.inscription_model.add(nom, prenom, email, telephone)
        messagebox.showinfo("Succès", "Inscription réussie!")

    def afficher_inscrits(self):
        return self.inscription_model.all()
    
    def rechercher(self, field, value):
        result = self.inscription_model.find_by(field, value)
        if result:
            return [result]  # Return a list with one item
        return []  # Return an empty list if no result found
    
    def modifier(self, id, nom, prenom, email, telephone):
        if not Validator.non_empty(nom, prenom, email, telephone):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return
        if not Validator.email_valide(email):
            messagebox.showerror("Erreur", "Email non valide.")
            return
        if not Validator.telephone_valide(telephone):
            messagebox.showerror("Erreur", "Numéro de téléphone non valide.")
            return
        
        self.inscription_model.update(id, nom, prenom, email, telephone)
        messagebox.showinfo("Succès", "Modification réussie!")
    
    def get_inscription_by_contact(self, contact):
        # Rechercher par email ou téléphone
        result = self.inscription_model.find_by("email", contact)
        if not result:
            result = self.inscription_model.find_by("telephone", contact)
        return result

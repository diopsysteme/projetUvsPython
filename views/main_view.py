import tkinter as tk
from ttkbootstrap import Style
import ttkbootstrap as ttk
from controllers.inscription_controller import InscriptionController
from tkinter import messagebox

class MainView:
    def __init__(self, root):
        self.root = root
        style = Style(theme='darkly')
        self.root = style.master
        self.root.title("Gestion des Inscriptions")
        self.root.geometry("500x400")
        
        self.controller = InscriptionController()

        main_frame = ttk.Frame(root, padding="20 20 20 20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame pour les entrées
        entry_frame = ttk.LabelFrame(main_frame, text="Informations d'inscription", padding="10 10 10 10")
        entry_frame.pack(fill=tk.X, pady=10)

        # Labels et entrées pour les informations d'inscription
        self.nom_entry = self.create_entry(entry_frame, "Nom", 0)
        self.prenom_entry = self.create_entry(entry_frame, "Prénom", 1)
        self.email_entry = self.create_entry(entry_frame, "Email", 2)
        self.telephone_entry = self.create_entry(entry_frame, "Téléphone", 3)
        
        # Frame pour les boutons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Boutons
        self.create_button(button_frame, "Inscrire", self.inscrire, 0)
        self.create_button(button_frame, "Afficher les inscrits", self.afficher_inscrits, 1)
        self.create_button(button_frame, "Rechercher", self.rechercher, 2)
        self.create_button(button_frame, "Modifier", self.modifier, 3)

    def create_entry(self, parent, label, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=5)
        entry = ttk.Entry(parent, width=30)
        entry.grid(row=row, column=1, sticky=tk.W, pady=5)
        return entry

    def create_button(self, parent, text, command, col):
        ttk.Button(parent, text=text, command=command, width=20).grid(row=0, column=col, padx=5)

    def inscrire(self):
        nom = self.nom_entry.get()
        prenom = self.prenom_entry.get()
        email = self.email_entry.get()
        telephone = self.telephone_entry.get()
        result = self.controller.inscrire(nom, prenom, email, telephone)
        if result:
            messagebox.showinfo("Succès", "Inscription réussie!")
            self.clear_entries()
        
    def afficher_inscrits(self):
        inscriptions = self.controller.afficher_inscrits()
        
        inscrits_window = ttk.Toplevel(self.root)
        inscrits_window.title("Liste des Inscrits")
        inscrits_window.geometry("600x400")
        
        # Création d'un widget Treeview pour afficher les inscrits
        tree = ttk.Treeview(inscrits_window, columns=('ID', 'Nom', 'Prénom', 'Email', 'Téléphone'), show='headings')
        tree.heading('ID', text='ID')
        tree.heading('Nom', text='Nom')
        tree.heading('Prénom', text='Prénom')
        tree.heading('Email', text='Email')
        tree.heading('Téléphone', text='Téléphone')
        
        for inscription in inscriptions:
            if isinstance(inscription, dict):
                values = (inscription.get('id', ''), 
                        inscription.get('nom', ''), 
                        inscription.get('prenom', ''), 
                        inscription.get('email', ''), 
                        inscription.get('telephone', ''))
            elif isinstance(inscription, (list, tuple)):
                values = inscription[:5]  # Prendre les 5 premiers éléments
                values = values + ('',) * (5 - len(values))  # Ajouter des chaînes vides si nécessaire
            else:
                values = (str(inscription), '', '', '', '')  # Fallback pour les types inattendus
            
            tree.insert('', 'end', values=values)
        
        tree.pack(fill=tk.BOTH, expand=True)

    # Ajouter une barre de défilement

    
    def rechercher(self):
        rechercher_window = ttk.Toplevel(self.root)
        rechercher_window.title("Rechercher un inscrit")
        rechercher_window.geometry("300x150")
        
        search_frame = ttk.Frame(rechercher_window, padding="10 10 10 10")
        search_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(search_frame, text="Nom ou Email").grid(row=0, column=0, sticky=tk.W, pady=5)
        search_entry = ttk.Entry(search_frame, width=30)
        search_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        def effectuer_recherche():
            search_value = search_entry.get()
            result = self.controller.rechercher("nom", search_value)
            if not result:
                result = self.controller.rechercher("email", search_value)
            
            # Crée une nouvelle fenêtre pour afficher les résultats
            result_window = ttk.Toplevel(rechercher_window)
            result_window.title("Résultats de la recherche")
            result_window.geometry("400x300")
            
            result_frame = ttk.Frame(result_window, padding="10 10 10 10")
            result_frame.pack(fill=tk.BOTH, expand=True)
            
            tree = ttk.Treeview(result_frame, columns=('ID', 'Nom', 'Prénom', 'Email', 'Téléphone'), show='headings')
            tree.heading('ID', text='ID')
            tree.heading('Nom', text='Nom')
            tree.heading('Prénom', text='Prénom')
            tree.heading('Email', text='Email')
            tree.heading('Téléphone', text='Téléphone')

            # Assurez-vous que `result` est une liste, même si elle contient un seul dictionnaire
            if isinstance(result, dict):
                result = [result]  # Convertir en liste pour uniformité

            if result:
                for inscription in result:
                    values = (
                        inscription.get('id', ''),
                        inscription.get('nom', ''),
                        inscription.get('prenom', ''),
                        inscription.get('email', ''),
                        inscription.get('telephone', '')
                    )
                    tree.insert('', 'end', values=values)
            else:
                tree.insert('', 'end', values=('', '', '', '', ''))
            
            tree.pack(fill=tk.BOTH, expand=True)
                    
        ttk.Button(search_frame, text="Rechercher", command=effectuer_recherche).grid(row=1, column=0, columnspan=2, pady=10)
    
    def modifier(self):
        modifier_window = ttk.Toplevel(self.root)
        modifier_window.title("Modifier un inscrit")
        modifier_window.geometry("400x300")
        
        modifier_frame = ttk.Frame(modifier_window, padding="10 10 10 10")
        modifier_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(modifier_frame, text="Email ou Téléphone").grid(row=0, column=0, sticky=tk.W, pady=5)
        contact_entry = ttk.Entry(modifier_frame, width=30)
        contact_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        nom_entry = self.create_entry(modifier_frame, "Nom", 2)
        prenom_entry = self.create_entry(modifier_frame, "Prénom", 3)
        email_entry = self.create_entry(modifier_frame, "Email", 4)
        telephone_entry = self.create_entry(modifier_frame, "Téléphone", 5)
        
        def rechercher_inscription():
            contact = contact_entry.get()
            inscription = self.controller.get_inscription_by_contact(contact)
            
            if inscription:
                # Assurez-vous que 'inscription' est un dictionnaire
                if isinstance(inscription, dict):
                    nom_entry.delete(0, tk.END)
                    prenom_entry.delete(0, tk.END)
                    email_entry.delete(0, tk.END)
                    telephone_entry.delete(0, tk.END)
                    
                    # Utilisez les clés du dictionnaire pour obtenir les valeurs
                    nom_entry.insert(0, inscription.get('nom', ''))
                    prenom_entry.insert(0, inscription.get('prenom', ''))
                    email_entry.insert(0, inscription.get('email', ''))
                    telephone_entry.insert(0, inscription.get('telephone', ''))
                    
                    def effectuer_modification():
                        new_nom = nom_entry.get()
                        new_prenom = prenom_entry.get()
                        new_email = email_entry.get()
                        new_telephone = telephone_entry.get()
                        
                        # Modifier l'inscription dans la base de données
                        self.controller.modifier(inscription.get('id'), new_nom, new_prenom, new_email, new_telephone)
                        
                        # Informer l'utilisateur du succès
                        messagebox.showinfo("Succès", "Modification réussie!")
                        modifier_window.destroy()
                    
                    # Assurez-vous que 'modifier_frame' est défini
                    ttk.Button(modifier_frame, text="Modifier", command=effectuer_modification).grid(row=6, column=0, columnspan=2, pady=10)
                else:
                    messagebox.showerror("Erreur", "Format de résultat inattendu.")
            else:
                messagebox.showerror("Erreur", "Inscription non trouvée.")

        # Assurez-vous que 'modifier_frame' est défini et ajouté à la fenêtre appropriée
        ttk.Button(modifier_frame, text="Rechercher", command=rechercher_inscription).grid(row=1, column=0, columnspan=2, pady=10)


    def clear_entries(self):
        self.nom_entry.delete(0, tk.END)
        self.prenom_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telephone_entry.delete(0, tk.END)
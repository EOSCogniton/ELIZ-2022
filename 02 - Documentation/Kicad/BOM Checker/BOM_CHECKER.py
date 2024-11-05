import csv
from tkinter import *
from tkinter import filedialog

import sys
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authorize the API
scope = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
]
file_name = "test-inventory-isymeca-9266ffbc0a2b.json"
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Fetch the sheet
def update_sheet():
    """Mets à jour la variable 'sheet' en extrayant les données du Google Sheet contenant l'inventaire"""
    global inventory
    global sheet
    print("Fetching online Inventory...")
    inventory = {}
    sheet = client.open("Gestion ISYMECA-Test").worksheet("Inventaire MODAC")
    python_sheet = sheet.get_values()
    python_sheet = python_sheet[3:]
    for k in range(len(python_sheet)):
        row = python_sheet[k]
        if python_sheet[k][1] == "":
            python_sheet = python_sheet[:k]
            break
        inventory[row[0]] = {"fab": row[1], "qte": int(row[4]), "ligne": k + 3}
    print("Done !")
    print(inventory)


update_sheet()


history = []


def send_update(lst, label, path, label2):
    """Mets à jour le Google Sheet en fonction des données fournies par l'utilisateur"""
    label2.configure(text="Processing...")
    print("Sending new data to sheet...")
    fenetre.update_idletasks()
    hist = []
    for i in range(len(lst)):
        if i != 0:
            row = lst[i]
            val = row[4]
            item = row[0]
            if item != "":
                if item == "Résistances normales" or item == "Condensateurs normaux":
                    break
                sheet_row = inventory[item]["ligne"] + 1
                if type(val) == int:
                    ancien = sheet.cell(sheet_row, 5).value
                    hist.append([sheet_row, 5, ancien, val])
                    sheet.update_cell(sheet_row, 5, val)
    history.append(hist)
    print("Done !")
    update_sheet()
    one_BOM_select(label, path)


def unsend_update(label, path, label2):
    """Annule le dernier upload en explorant les différentes mises à jour stockées dans 'history'"""
    global history
    if len(history) >= 1:
        label2.configure(text="Processing...")
        fenetre.update_idletasks()
        print("Sending old data to sheet...")
        actions = history[-1]
        for x in actions:
            sheet.update_cell(x[0], x[1], x[2])
        history = history[:-1]
        print("Done!")
        update_sheet()
        one_BOM_select(label, path)
    else:
        label2.configure(text="Vous n'avez pas encore effectué d'action")
        fenetre.update_idletasks()


def update_table(lst, widgets):
    """Met à jour un tableau déjà existant à partir de 'lst'"""
    total_rows = len(lst)
    total_columns = len(lst[0])
    # code for creating table
    lst_color = {}
    for i in range(total_rows):
        lst_color[str(i)] = "white"
    for i in range(total_rows):
        for j in range(total_columns):
            if i == 0:
                pass
            else:
                col = widgets[str(j)]
                col[i].configure(text=lst[i][j])
                if j == 3 and lst[i][j] == "Manquant à l'inv.":
                    lst_color[str(i)] = "red"
                if j == 4 and lst[i][j] != "/" and lst[i][j] != "":
                    if lst[i][j] <= -1:
                        lst_color[str(i)] = "red"
                    elif lst[i][j] == 0:
                        lst_color[str(i)] = "orange"

    for j in range(total_columns):
        col = widgets[str(j)]
        for i in range(total_rows):
            col[i].configure(bg=lst_color[str(i)])


def create_table(root, lst):
    """Crée un tableau dans la frame 'root' à partir des composants de 'lst'"""
    total_rows = len(lst)
    total_columns = len(lst[0])
    # code for creating table
    lst_widget = {}
    lst_color = {}
    for i in range(total_rows):
        lst_color[str(i)] = "white"
    for i in range(total_rows):
        for j in range(total_columns):
            if i == 0:
                e = Label(
                    root,
                    text=lst[i][j],
                    fg="black",
                    font=("Arial", 11, "bold"),
                    anchor="w",
                )
            else:
                e = Label(
                    root,
                    text=lst[i][j],
                    fg="black",
                    font=(
                        "Arial",
                        11,
                    ),
                    anchor="w",
                )
                if j == 4 and lst[i][j] != "/" and lst[i][j] != "":
                    if lst[i][j] <= -1:
                        lst_color[str(i)] = "red"
                    elif lst[i][j] == 0:
                        lst_color[str(i)] = "orange"

            e.grid(row=i, column=j, sticky="w")
            try:
                lst_widget[str(j)].append(e)
            except:
                lst_widget[str(j)] = [e]
    for j in range(total_columns):
        col = lst_widget[str(j)]
        for i in range(total_rows):
            col[i].configure(bg=lst_color[str(i)])

    modify_table_width(lst_widget)
    frame_tableau.update_idletasks()

    return lst_widget  # sum(x.winfo_width() for x in lst_header)


def modify_table_width(table):
    """Modifie la largeur de chaque colonne pour être de la longueur de la plus longue cellule de la colonne"""
    n = len(table)
    real = [0] * n

    for j in range(n):
        col = table[str(j)]
        for i in range(len(col)):
            z = col[i]["text"]
            if type(z) == str:
                z = len(z)
            elif type(z) == int:
                z = len(str(z))
            if z > real[j]:
                real[j] = z
    for j in range(n):
        col = table[str(j)]
        for i in range(len(col)):
            col[i].configure(width=real[j])


def get_table_width(table):
    """Retourne la longueur affichée de la table"""
    n = len(table)
    render = [0] * n
    for j in range(n):
        col = table[str(j)]
        for i in range(len(col)):
            x = col[i].winfo_width()
            if x > render[j]:
                render[j] = x
    return sum(x for x in render)


def create_lst_from_BOM(path):
    """Crée une variable 'lst' utlisable pour l'éditeur d'inventaire"""
    lst = [["Réf.", "Fab.", "Qté.", "Qté. disp.", "Qté. post-use", "Ind.", "Val."]]
    BOM_MANUFACTURER_col = 0
    BOM_PART_col = 0
    BOM_QTY_col = 0
    REF_col = 0
    VALUE_col = 0
    res = []
    cond = []
    with open(path, "r") as file:
        csvreader = csv.reader(file)
        first = True
        for row in csvreader:
            if first:
                first = False
                for k in range(len(row)):
                    if row[k] == "Manufacturer_Name":
                        BOM_MANUFACTURER_col = k
                    elif row[k] == "Manufacturer_Part_Number":
                        BOM_PART_col = k
                    elif row[k] == "Qty":
                        BOM_QTY_col = k
                    elif row[k] == "Reference":
                        REF_col = k
                    elif row[k] == "Value":
                        VALUE_col = k
            else:
                if row[BOM_PART_col] == "0805Y1000104JXT":
                    cond.append(
                        [int(row[BOM_QTY_col]), "/", "/", row[REF_col], row[VALUE_col]]
                    )
                elif row[BOM_PART_col] == "RK73H2BLTDD2152F":
                    res.append(
                        [int(row[BOM_QTY_col]), "/", "/", row[REF_col], row[VALUE_col]]
                    )
                else:
                    newrow = []
                    newrow.append(row[BOM_PART_col])
                    newrow.append(row[BOM_MANUFACTURER_col])
                    newrow.append(int(row[BOM_QTY_col]))
                    try:
                        qty = inventory[row[BOM_PART_col]]["qte"]
                        newrow.append(qty)
                        newrow.append(qty - int(row[BOM_QTY_col]))
                    except:
                        newrow.append("Manquant à l'inv.")
                        newrow.append("/")
                    newrow.append(row[REF_col])
                    newrow.append(row[VALUE_col])
                    lst.append(newrow)
    lst.append(["Résistances normales", "", "", "", "", "", ""])
    for resi in res:
        lst.append(["", ""] + resi)
    lst.append(["Condensateurs normaux", "", "", "", "", "", ""])
    for condo in cond:
        lst.append(["", ""] + condo)
    return lst


def add_sub_one_bom(sens, var, lst, widgets, label):
    """Fonction associée aux boutons + et - pour ajouter ou soustraire une carte produite"""
    orginal_var = var.get()
    if sens == "+":
        var.set(var.get() + 1)
    else:
        if var.get() > 1:
            var.set(var.get() - 1)
    total_rows = len(lst)
    total_columns = len(lst[0])
    for i in range(total_rows):
        if i != 0:
            for j in range(total_columns):
                if type(lst[i][j]) == int:
                    if j == 2:
                        need = lst[i][j] // orginal_var
                        lst[i][j] = var.get() * need
                    elif j == 4:
                        lst[i][j] = lst[i][j] - need * (var.get() - orginal_var)
    update_table(lst, widgets)
    Frame_table_and_button.update_idletasks()
    label.configure(text=str(var.get()))


def one_BOM_select(label, path="None"):
    """Fonction principale de l'éditeur d'inventaire"""
    # for widget in Frame2.winfo_children():
    #     widget.destroy()
    if path == "None":
        path = filedialog.askopenfilename()
    label.config(text=path)
    lst = create_lst_from_BOM(path)

    Frame_table = Frame(Frame_table_and_button)
    Frame_table.grid(row=2, column=0, pady=(5, 0), sticky="nw")
    Frame_table.grid_rowconfigure(0, weight=1)
    Frame_table.grid_columnconfigure(0, weight=1)
    Frame_table.grid_propagate(False)

    canvas = Canvas(Frame_table)
    canvas.grid(row=0, column=0, sticky="news")

    scrollbar = Scrollbar(Frame_table, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    frame_tableau = Frame(canvas)
    canvas.create_window((0, 0), window=frame_tableau, anchor="nw")

    table = create_table(frame_tableau, lst)

    table_width = get_table_width(table)
    Frame_table.config(
        width=table_width + scrollbar.winfo_width(),
        height=height,
    )

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.config(scrollregion=canvas.bbox("all"))

    Frame_button_update = Frame(Frame_table_and_button)
    Frame_button_update.grid(row=3, column=0, pady=(5, 0))
    label_process = Label(Frame_button_update, text="")
    label_process.grid(row=1, columnspan=2)

    button_undo = Button(
        Frame_button_update,
        text="Annuler MAJ",
        command=lambda: unsend_update(label, path, label_process),
    )
    button_undo.grid(row=0, column=0)
    button_maj = Button(
        Frame_button_update,
        text="Mise A Jour Inventaire",
        command=lambda: send_update(lst, label, path, label_process),
    )
    button_maj.grid(row=0, column=1)

    nb_carte = IntVar()
    nb_carte.set(1)
    Frame_button_add = Frame(Frame_table_and_button)
    Frame_button_add.grid(row=1, column=0)

    label_txt_nb_carte = Label(Frame_button_add, text="Nombre de cartes produites :")
    label_txt_nb_carte.grid(row=0, column=0, padx=(5, 0))

    label_nb_carte = Label(Frame_button_add, text=str(nb_carte.get()))
    label_nb_carte.grid(row=0, column=2, padx=(5, 0))

    bouton_moins = Button(
        Frame_button_add,
        text="-",
        width=1,
        height=1,
        command=lambda: add_sub_one_bom("-", nb_carte, lst, table, label_nb_carte),
    )
    bouton_moins.grid(row=0, column=1, padx=(5, 0))
    bouton_plus = Button(
        Frame_button_add,
        text="+",
        width=1,
        height=1,
        command=lambda: add_sub_one_bom("+", nb_carte, lst, table, label_nb_carte),
    )
    bouton_plus.grid(row=0, column=3, padx=(5, 0))


def page_BOM_editor():
    """Affichage de la page de l'éditeur d'inventaire"""
    global Frame_table_and_button
    for widget in Frame1.winfo_children():
        widget.destroy()
    Frame_table_and_button = Frame(fenetre, relief=GROOVE)
    Frame_table_and_button.pack(side=TOP, padx=20, pady=10)

    label_path = Label(Frame1, text="En attente")
    file_selector = Button(
        Frame1, text="Sélectionner BOM", command=lambda: one_BOM_select(label_path)
    )
    file_selector.pack(side=LEFT, pady=10, padx=10)
    label_path.pack(pady=10, padx=10)


class BOM_Selector:
    """Contient les boutons et les sélecteurs de BOM pour le vérificateur d'inventaire"""

    def __init__(self, row, frame):
        global comp_list
        global table
        self.keeper_frame = Frame(frame)
        self.keeper_frame.grid(row=row, column=0, sticky="w")
        self.activated = False
        self.row = row
        self.label_path = Label(self.keeper_frame, text="En attente")
        self.file_selector = Button(
            self.keeper_frame,
            text="Sélectionner BOM",
            command=lambda: multiple_BOM_select(self),
        )
        self.file_selector.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.label_path.grid(row=0, column=1, pady=5, padx=5, sticky="w")

        self.nb_carte = IntVar()
        self.nb_carte.set(1)

        self.label_nb_carte = Label(self.keeper_frame, text=str(self.nb_carte.get()))

        self.bouton_moins = Button(
            self.keeper_frame,
            text="-",
            width=1,
            height=1,
            command=lambda: add_sub_multiple_bom(
                self.label_path.cget("text"),
                "-",
                self.nb_carte,
                table,
                self.label_nb_carte,
            ),
        )

        self.bouton_plus = Button(
            self.keeper_frame,
            text="+",
            width=1,
            height=1,
            command=lambda: add_sub_multiple_bom(
                self.label_path.cget("text"),
                "+",
                self.nb_carte,
                table,
                self.label_nb_carte,
            ),
        )

    def activate(self):
        """Affiche les différents boutons"""
        self.label_path.grid_forget()
        self.label_path.grid(row=0, column=4, pady=5, padx=5)
        self.label_nb_carte.grid(row=0, column=2, padx=(5, 0))
        self.bouton_moins.grid(row=0, column=1, padx=(5, 0))
        self.bouton_plus.grid(row=0, column=3, padx=(5, 0))

    def deactivate(self):
        """Cache les différents boutons"""
        self.label_path.grid_forget()
        self.label_path.grid(row=0, column=1, pady=5, padx=5)
        self.label_nb_carte.grid_forget()
        self.bouton_moins.grid_forget()
        self.bouton_plus.grid_forget()

    def destroy(self):
        """Détruit le BOM selector"""
        for widget in self.keeper_frame.winfo_children():
            widget.destroy()
        self.keeper_frame.destroy()

    def set_state(self, state):
        self.activated = state

    def set_label(self, labeltxt):
        self.label_path.config(text=labeltxt)

    def get_path(self):
        return self.label_path.cget("text")

    def get_state(self):
        return self.activated

    def get_nb(self):
        return self.nb_carte.get()

    def set_nb(self, val):
        self.nb_carte.set(val)
        self.label_nb_carte.configure(text=self.get_nb())


def get_part_row(part, lst):
    total_row = len(lst)
    for i in range(1, total_row):
        if lst[i][0] == part:
            return i
    return 0


def get_val_row(val, lst):
    total_row = len(lst)
    for i in range(1, total_row):
        if lst[i][5] == val:
            return i
    return 0


def add_sub_multiple_bom(path, sens, var, widgets, label):
    """Fonction associée aux boutons + et - pour ajouter ou soustraire une carte produite"""
    global Frame_table_verifier
    global comp_list
    lst = comp_list
    newlst = create_lst_from_BOM_no_ref(
        path
    )  # Prend les infos du bom qu'on ajoute/soustrait
    original_var = var.get()
    if sens == "+":
        var.set(var.get() + 1)
    else:
        if var.get() > 1:
            var.set(var.get() - 1)
    total_rows = len(newlst)
    total_columns = len(newlst[0])
    for i in range(total_rows):
        if i != 0:
            for j in range(total_columns):
                if type(newlst[i][j]) == int:
                    if j == 2:
                        need = newlst[i][j]
                        if newlst[i][0] == "":
                            ind = get_val_row(newlst[i][5], lst)
                        else:
                            ind = get_part_row(newlst[i][0], lst)
                        lst[ind][j] = lst[ind][j] + need * (var.get() - original_var)
                    elif j == 4:
                        if newlst[i][0] == "":
                            ind = get_val_row(newlst[i][5], lst)
                        else:
                            ind = get_part_row(newlst[i][0], lst)
                        lst[ind][j] = lst[ind][j] - need * (var.get() - original_var)
    update_table(lst, widgets)
    Frame_table_verifier.update_idletasks()
    label.configure(text=str(var.get()))


def create_lst_from_BOM_no_ref(path):
    """Idem que 'create_lst_from_BOM' mais sans la colonne Ind."""
    lst = [["Réf.", "Fab.", "Qté.", "Qté. disp.", "Qté. post-use", "Val."]]
    BOM_MANUFACTURER_col = 0
    BOM_PART_col = 0
    BOM_QTY_col = 0
    VALUE_col = 0
    res = []
    cond = []
    with open(path, "r") as file:
        csvreader = csv.reader(file)
        first = True
        for row in csvreader:
            if first:
                first = False
                for k in range(len(row)):
                    if row[k] == "Manufacturer_Name":
                        BOM_MANUFACTURER_col = k
                    elif row[k] == "Manufacturer_Part_Number":
                        BOM_PART_col = k
                    elif row[k] == "Qty":
                        BOM_QTY_col = k
                    elif row[k] == "Value":
                        VALUE_col = k
            else:
                if row[BOM_PART_col] == "0805Y1000104JXT":
                    cond.append([int(row[BOM_QTY_col]), "/", "/", row[VALUE_col]])
                elif row[BOM_PART_col] == "RK73H2BLTDD2152F":
                    res.append([int(row[BOM_QTY_col]), "/", "/", row[VALUE_col]])
                else:
                    newrow = []
                    newrow.append(row[BOM_PART_col])
                    newrow.append(row[BOM_MANUFACTURER_col])
                    newrow.append(int(row[BOM_QTY_col]))
                    try:
                        qty = inventory[row[BOM_PART_col]]["qte"]
                        newrow.append(qty)
                        newrow.append(qty - int(row[BOM_QTY_col]))
                    except:
                        newrow.append("Manquant à l'inv.")
                        newrow.append("/")
                    newrow.append(row[VALUE_col])
                    lst.append(newrow)
    lst.append(["Résistances normales", "", "", "", "", ""])
    for resi in res:
        lst.append(["", ""] + resi)
    lst.append(["Condensateurs normaux", "", "", "", "", ""])
    for condo in cond:
        lst.append(["", ""] + condo)
    return lst


def value_is_present(value, lst):
    """Détecte si la résistance/le condensateur de valeur 'value' est déjà présent dans 'lst'"""
    present = False
    ind = 0
    for k in range(len(lst)):
        if lst[k][5] == value:
            present = True
            ind = k
    return present, ind


def part_is_present(part, lst):
    """Détecte si le composant 'part' est déjà présent dans 'lst'"""
    present = False
    ind = 0
    for k in range(len(lst)):
        if lst[k][0] == part:
            present = True
            ind = k
    return present, ind


def add_BOM_to_lst(lst: list, path):
    """Ajoute un BOM à la liste 'lst' existante"""
    BOM_MANUFACTURER_col = 0
    BOM_PART_col = 0
    BOM_QTY_col = 0
    VALUE_col = 0
    FIRST_RES_COND_row = 0
    RES_row = 0
    COND_row = 0
    added = 0

    for k in range(len(lst)):
        name = lst[k][0]
        if name == "Résistances normales":
            RES_row = k
            if FIRST_RES_COND_row == 0:
                FIRST_RES_COND_row = k
        if name == "Condensateurs normaux":
            COND_row = k
            if FIRST_RES_COND_row == 0:
                FIRST_RES_COND_row = k

    res = []
    cond = []
    with open(path, "r") as file:
        csvreader = csv.reader(file)
        first = True
        for row in csvreader:
            if first:
                first = False
                for k in range(len(row)):
                    if row[k] == "Manufacturer_Name":
                        BOM_MANUFACTURER_col = k
                    elif row[k] == "Manufacturer_Part_Number":
                        BOM_PART_col = k
                    elif row[k] == "Qty":
                        BOM_QTY_col = k
                    elif row[k] == "Value":
                        VALUE_col = k
            else:
                if row[BOM_PART_col] == "0805Y1000104JXT":
                    cond.append([int(row[BOM_QTY_col]), "/", "/", row[VALUE_col]])
                elif row[BOM_PART_col] == "RK73H2BLTDD2152F":
                    res.append([int(row[BOM_QTY_col]), "/", "/", row[VALUE_col]])
                else:
                    if row[BOM_PART_col] == "":
                        test_present = value_is_present(row[VALUE_col], lst)
                    else:
                        test_present = part_is_present(row[BOM_PART_col], lst)
                    if test_present[0]:
                        ind_part = test_present[1]
                        qte = int(row[BOM_QTY_col])
                        lst[ind_part][2] += qte
                        if type(lst[ind_part][4]) == int:
                            lst[ind_part][4] -= qte
                    else:
                        newrow = []
                        newrow.append(row[BOM_PART_col])
                        newrow.append(row[BOM_MANUFACTURER_col])
                        newrow.append(int(row[BOM_QTY_col]))
                        try:
                            qty = inventory[row[BOM_PART_col]]["qte"]
                            newrow.append(qty)
                            newrow.append(qty - int(row[BOM_QTY_col]))
                        except:
                            newrow.append("Manquant à l'inv.")
                            newrow.append("/")
                        newrow.append(row[VALUE_col])
                        if FIRST_RES_COND_row == 0:
                            lst.append(newrow)
                        else:
                            lst.insert(FIRST_RES_COND_row + added, newrow)
                            added += 1
    if RES_row == 0:
        lst.append(["Résistances normales", "", "", "", "", ""])
    for resi in res:
        test_present = value_is_present(resi[3], lst)
        if test_present[0]:
            ind_res = test_present[1]
            lst[ind_res][2] += resi[0]
        else:
            lst.insert(RES_row + added + 1, ["", ""] + resi)
            added += 1
    if COND_row == 0:
        lst.append(["Condensateurs normaux", "", "", "", "", ""])
    for condo in cond:
        test_present = value_is_present(condo[3], lst)
        if test_present[0]:
            ind_cond = test_present[1]
            lst[ind_cond][2] += condo[0]
        else:
            lst.insert(COND_row + added + 1, ["", ""] + condo)
            added += 1
    return lst


def retirer_BOM_of_lst(lst: list, path, nb):
    """Retire un BOM à la liste 'lst' existante"""
    BOM_MANUFACTURER_col = 0
    BOM_PART_col = 0
    BOM_QTY_col = 0
    VALUE_col = 0

    res = []
    cond = []
    with open(path, "r") as file:
        csvreader = csv.reader(file)
        first = True
        for row in csvreader:
            if first:
                first = False
                for k in range(len(row)):
                    if row[k] == "Manufacturer_Name":
                        BOM_MANUFACTURER_col = k
                    elif row[k] == "Manufacturer_Part_Number":
                        BOM_PART_col = k
                    elif row[k] == "Qty":
                        BOM_QTY_col = k
                    elif row[k] == "Value":
                        VALUE_col = k
            else:
                if row[BOM_PART_col] == "0805Y1000104JXT":
                    cond.append([int(row[BOM_QTY_col]), "/", "/", row[VALUE_col]])
                elif row[BOM_PART_col] == "RK73H2BLTDD2152F":
                    res.append([int(row[BOM_QTY_col]), "/", "/", row[VALUE_col]])
                else:
                    if row[BOM_PART_col] == "":
                        test_present = value_is_present(row[VALUE_col], lst)
                    else:
                        test_present = part_is_present(row[BOM_PART_col], lst)
                    if test_present[0]:
                        ind_part = test_present[1]
                        qte = int(row[BOM_QTY_col])
                        lst[ind_part][2] -= qte * nb
                        inv_qte = lst[ind_part][4]
                        if type(inv_qte) == int:
                            inv_qte += qte * nb
    for resi in res:
        test_present = value_is_present(resi[3], lst)
        if test_present[0]:
            ind_res = test_present[1]
            lst[ind_res][2] -= resi[0] * nb
    for condo in cond:
        test_present = value_is_present(condo[3], lst)
        if test_present[0]:
            ind_cond = test_present[1]
            lst[ind_cond][2] -= condo[0] * nb
    k = 1
    while k < len(lst):
        if lst[k][2] == 0:
            lst = lst[:k] + lst[k + 1 :]
        else:
            k += 1
    return lst


def multiple_BOM_select(selector: BOM_Selector):
    global Frame_table
    global comp_list
    global table
    global frame_tableau
    global scrollbar
    global canvas
    path = filedialog.askopenfilename()
    if selector.get_state():
        old_path = selector.get_path()
        comp_list = retirer_BOM_of_lst(comp_list, old_path, selector.get_nb())
        selector.set_nb(1)
        update_table_multiple()
    selector.set_label(path)
    selector.activate()
    selector.set_state(True)
    if comp_list == []:
        comp_list = create_lst_from_BOM_no_ref(path)
        Frame_table = Frame(Frame_table_verifier)
        Frame_table.grid(row=2, column=0, pady=(5, 0), sticky="nw")
        Frame_table.grid_rowconfigure(0, weight=1)
        Frame_table.grid_columnconfigure(0, weight=1)
        Frame_table.grid_propagate(False)

        canvas = Canvas(Frame_table)
        canvas.grid(row=0, column=0, sticky="news")

        scrollbar = Scrollbar(Frame_table, orient="vertical", command=canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        frame_tableau = Frame(canvas)
        canvas.create_window((0, 0), window=frame_tableau, anchor="nw")
    else:
        comp_list = add_BOM_to_lst(comp_list, path)
    update_table_multiple()


def create_BOM_selector():
    """Ajoute un sélecteur"""
    global row_bom_selector
    global BOM_list
    row_bom_selector += 1
    BOM_list.append(BOM_Selector(row_bom_selector, Frame1))
    button_frame.grid_forget()
    button_frame.grid(row=row_bom_selector + 1, column=0, padx=5, pady=5, sticky="w")
    retirer_bom_button.grid_forget()
    if row_bom_selector >= 1:
        retirer_bom_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")


def update_table_multiple():
    global table
    global Frame_table
    global canvas
    try:
        for widgets in frame_tableau.winfo_children():
            widgets.destroy()
    except:
        pass
    table = create_table(frame_tableau, comp_list)
    table_width = get_table_width(table)
    Frame_table.config(
        width=table_width + scrollbar.winfo_width(),
        height=height,
    )
    update_table(comp_list, table)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.config(scrollregion=canvas.bbox("all"))


def retirer_BOM_selector():
    """Retire un sélecteur"""
    global row_bom_selector
    global BOM_list
    global comp_list
    row_bom_selector -= 1
    old_path = BOM_list[-1].get_path()
    nb = BOM_list[-1].get_nb()
    BOM_list[-1].destroy()
    BOM_list = BOM_list[:-1]
    button_frame.grid_forget()
    retirer_bom_button.grid_forget()
    button_frame.grid(row=row_bom_selector + 1, column=0, padx=5, pady=5, sticky="w")
    if row_bom_selector >= 1:
        retirer_bom_button.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    comp_list = retirer_BOM_of_lst(comp_list, old_path, nb)
    update_table_multiple()


def page_BOM_verifier():
    """Affichage de la page du vérificateur d'inventaire"""
    global Frame_table_verifier
    global row_bom_selector
    global add_bom_button
    global retirer_bom_button
    global BOM_list
    global comp_list
    global button_frame
    comp_list = []
    BOM_list = []
    row_bom_selector = -1
    for widget in Frame1.winfo_children():
        widget.destroy()
    Frame_table_verifier = Frame(fenetre, relief=GROOVE)
    Frame_table_verifier.pack(side=TOP, padx=20, pady=10)
    button_frame = Frame(Frame1)
    add_bom_button = Button(
        button_frame, text="Ajouter un BOM", command=create_BOM_selector
    )
    retirer_bom_button = Button(
        button_frame, text="Retirer dernier BOM", command=retirer_BOM_selector
    )
    add_bom_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    button_frame.grid(row=row_bom_selector + 1, column=0, padx=5, pady=5, sticky="w")
    create_BOM_selector()


def welcome():
    """Affichage du menu principal"""
    global Frame1
    for widget in fenetre.winfo_children():
        widget.destroy()
    Frame1 = Frame(fenetre, borderwidth=2, relief=GROOVE)
    Frame1.pack(padx=20, pady=10)

    bouton_BOM_editor = Button(
        Frame1,
        text="Editer Inventaire avec BOM",
        command=page_BOM_editor,
    )
    bouton_BOM_editor.pack(side=LEFT, pady=10, padx=10)

    bouton_BOM_verifier = Button(
        Frame1, text="Vérifier Inventaire avec plusieurs BOM", command=page_BOM_verifier
    )
    bouton_BOM_verifier.pack(pady=10, padx=10)

    Frame_leave = Frame(fenetre)
    Frame_leave.pack(side=BOTTOM, padx=10, pady=10)

    bouton = Button(Frame_leave, text="Fermer", command=fenetre.quit)
    bouton.pack(side=RIGHT, padx=10, pady=10)
    bouton = Button(Frame_leave, text="Accueil", command=welcome)
    bouton.pack(side=LEFT, padx=10, pady=10)


fenetre = Tk(screenName="Inventory management")
fenetre.title("Inventory management")
fenetre.iconbitmap(resource_path("logo.ico"))


width = fenetre.winfo_screenwidth() // 2
height = fenetre.winfo_screenheight() // 2


welcome()


fenetre.mainloop()

from tkinter import Tk, StringVar, IntVar, BooleanVar, ttk, Menu, Toplevel, Checkbutton
import tkinter as tk
import random
import json
import os


def baza_check():
    """Sprawdzanie, czy istnieje plik .json zawierający bazę pytań.

    :return: True, jeżeli plik json istnieje w katalogu programu, w przeciwnym wypadku False.

    Dodatkowo zmienia stan przycisku "Losowanie", w zależności od wyniku funkcji losowanie_check, oraz
    przycisku "Wybór kategorii", w zależności od istnienia bazy.
    """
    def losowanie_check():
        """Sprawdza, czy istnieje przynajmniej jedno pytanie (wartość) dla wybranej kategorii (klucz).

        :return: True, jeżeli istnieje przynajmniej jedna wartość, inaczej False.
        """
        if wybrana_kat.get() != "":
            with open("baza.json", "r") as f:
                data = json.load(f)
            lista_pytan = data[wybrana_kat.get()]
        else:
            return False

        if wybrana_kat.get() == "":
            return False
        elif len(lista_pytan) == 0:
            return False
        else:
            return True

    if os.path.exists("baza.json"):
        baza_jest.set(True)
        wybierz.state(["!disabled"])
        if losowanie_check():
            losowanie.state(["!disabled"])
        else:
            losowanie.state(["disabled"])
    else:
        baza_jest.set(False)
        wybierz.state(["disabled"])
        losowanie.state(["disabled"])


def warn(msg, result):
    """Wyświetla okno z ostrzeżeniem.

    :param msg: String zawierający treść ostrzeżenia
    :param result: None lub nazwa funkcji do wywołania
    """
    warning = Toplevel(gl_ok)
    warning.title("Ojoj")
    warning.attributes('-toolwindow', True)
    warning.grab_set()
    warning.resizable(False, False)
    warning.geometry("155x50+{}+{}".format(int(gl_ok.winfo_screenwidth() / 2 - gl_ok.winfo_reqwidth() / 2),
                                           int(gl_ok.winfo_screenheight() / 2 - gl_ok.winfo_reqheight() / 2)))
    ttk.Label(warning, text=msg).grid(sticky="ew", row=0, column=1, columnspan=2)
    if result is None:
        ttk.Button(warning, text="Ok", command=lambda: (warning.destroy())) \
            .grid(sticky="ew", row=1, column=1, columnspan=2)
    else:
        ttk.Button(warning, text="Ok", command=lambda: (result(), warning.destroy())) \
            .grid(sticky="ew", row=1, column=1, columnspan=2)


def dodaj_pyt():
    """Wyświetla okno dodawania zagadnień.

    Pozwala przekazywać tekst wpisywany w okienku do funkcji write celem zapisu
    w bazie zagadnień pod wybraną wcześniej kategorią.
    """
    dod_pyt_klik.set(True)

    if wybrana_kat.get() == "":
        # Jeżeli nie wybraliśmy wpierw kategorii, nie możemy dodać pytania.
        # Automatycznie zostaniemy odesłani do okna wyboru kategorii.
        warn("Najpierw wybierz kategorię!", ch_kat)
    else:
        dod_pyt_klik.set(False)
        dod_pyt = Toplevel(gl_ok)
        dod_pyt.attributes('-toolwindow', True)
        dod_pyt.title("Dodawanie zagadnienia")
        dod_pyt.grab_set()
        dod_pyt.resizable(False, False)
        dod_pyt.geometry("155x50+{}+{}".format(int(gl_ok.winfo_screenwidth() / 2 - gl_ok.winfo_reqwidth() / 2),
                                               int(gl_ok.winfo_screenheight() / 2 - gl_ok.winfo_reqheight() / 2)))

        wpis = ttk.Entry(dod_pyt)
        wpis.grid(sticky="ew", row=0, column=0, rowspan=4, columnspan=4)
        ttk.Button(dod_pyt, text="Dodaj", command=lambda: (write(str(wpis.get()), 1), wpis.delete(0, tk.END)))\
            .grid(sticky="ew", row=4, column=0, columnspan=2)
        ttk.Button(dod_pyt, text="Zakończ", command=lambda: (dod_pyt.destroy(), baza_check())) \
            .grid(sticky="ew", row=4, column=2, columnspan=2)


def dodaj_kat():
    """Wyświetla okno dodawania kategorii.

    Pozwala utworzyć w bazie json klucz o wskazanej przez użytkownika nazwie.
    """
    def end():
        # Określa, w jaki sposób funkcja dodaj_kat ma się zakończyć.
        if dod_pyt_klik.get():
            # Jeżeli zostaliśmy odesłani do wyboru kategorii, a następnie do tworzenia kategorii,
            # zostaniemy ponownie odesłani do okna wyboru kategorii.
            ch_kat()
            dod_kat.destroy()
        else:
            dod_kat.destroy()

    dod_kat = Toplevel(gl_ok)
    dod_kat.title("Dodawanie kategorii")
    dod_kat.attributes('-toolwindow', True)
    dod_kat.grab_set()
    dod_kat.resizable(False, False)
    dod_kat.geometry("155x50+{}+{}".format(int(gl_ok.winfo_screenwidth() / 2 - gl_ok.winfo_reqwidth() / 2),
                                           int(gl_ok.winfo_screenheight() / 2 - gl_ok.winfo_reqheight() / 2)))

    wpis = ttk.Entry(dod_kat)
    wpis.grid(sticky="ew", row=0, column=1, columnspan=6)
    ttk.Button(dod_kat, text="Dodaj", command=lambda: (write(str(wpis.get()), 0), wpis.delete(0, tk.END)))\
        .grid(sticky="ew", row=1, column=1, columnspan=2)
    ttk.Button(dod_kat, text="Zakończ", command=lambda: (end(), baza_check()))\
        .grid(sticky="ew", row=1, column=4, columnspan=2)


def usuwanie():
    # Pozwala na usuwanie z bazy poszczególnych zagadnień bądź całej kategorii. Wymaga uprzedniego wyboru kategorii.
    def end(param):
        """ Określa, w jaki sposób funkcja usuwanie ma się zakończyć.

        :param param:  Integer. 0 dla zapisu zagadnienia (wartości), 1 dla zapisu kategorii (klucza).
        """
        rezultat.clear()
        if param == 0:
            with open("baza.json", "r") as f1:
                data1 = json.load(f1)
                pytania1 = list(data1[wybrana_kat.get()])
            if wybrane_pyt.get() in pytania1:
                data1[wybrana_kat.get()].remove(wybrane_pyt.get())
            with open("baza.json", "w") as f1:
                json.dump(data1, f1)
            wybrane_pyt.set("")
            lista_pytan()
        elif param == 1:
            with open("baza.json", "r") as f1:
                data1 = json.load(f1)
            if wybrana_kat.get() in data1:
                del data1[wybrana_kat.get()]
            with open("baza.json", "w") as f1:
                json.dump(data1, f1)
            wybrana_kat.set("")
            usun.destroy()
            baza_check()
        elif param == 2:
            usun.destroy()
            baza_check()

    def lista_pytan():
        #   Odczytuje listę pytań (wartości) z wybranej kategorii (klucza) i pozwala wyświetlić w formie listy opcji.
        with open("baza.json", "r") as f1:
            data1 = json.load(f1)

        pytania = list(data1[wybrana_kat.get()])
        pozycja = pyt_menu["menu"]
        pozycja.delete(0, 'end')
        for pytanie in pytania:
            pozycja.add_command(label=pytanie, command=lambda value=pytanie: wybrane_pyt.set(value))

    baza_check()

    if not baza_jest.get():
        # Jeżeli plik bazy nie istnieje, wyskoczy okienko błędu.
        warn("Błąd: brak danych w bazie!", None)
    elif wybrana_kat.get() == "":
        # Jeżeli nie wybrano kategorii, wyskoczy błąd i nastąpi odesłanie do okna wyboru kategorii.
        warn("Najpierw wybierz kategorię!", ch_kat)
        usun_klik.set(True)
    else:
        if wybrana_kat.get() == "":
            wybrana_kat.set("<brak>")   # Wstępnie wyświetla <brak> w polu wyboru.
        usun = Toplevel(gl_ok)
        usun.title("Usuwanie z bazy")
        usun.attributes('-toolwindow', True)
        usun.resizable(False, False)
        usun.grab_set()
        usun.geometry("200x200+{}+{}".format(int(gl_ok.winfo_screenwidth() / 2 - gl_ok.winfo_reqwidth() / 2),
                                             int(gl_ok.winfo_screenheight() / 2 - gl_ok.winfo_reqheight() / 2)))

        ttk.Label(usun, text="Wybrana Kategoria:")\
            .grid(sticky="ew", row=0, column=0, columnspan=2)
        ttk.Label(usun, text=wybrana_kat.get())\
            .grid(sticky="ew", row=0, column=2, columnspan=1)

        pyt_menu = tk.OptionMenu(usun, wybrane_pyt, "")
        pyt_menu.grid(sticky="esw", row=1, column=1, columnspan=2)
        pyt_menu.config(width=25)

        lista_pytan()

        ttk.Button(usun, text="Usuń wybrane", command=lambda: end(0))\
            .grid(sticky="ew", row=2, column=1, columnspan=2)
        ttk.Button(usun, text="Usuń kategorię", command=lambda: end(1))\
            .grid(sticky="ew", row=3, column=1, columnspan=2)
        ttk.Button(usun, text="Zakończ", command=lambda: end(2))\
            .grid(sticky="ew", row=4, column=1, columnspan=2)


def write(tekst, co):
    """Pozwala na zapis treści w pliku.

    :param tekst: String. Treść do zapisania.
    :param co: Integer. 1 dla dodawania kolejnego zagadnienia, 0 dla czyszczenia kategorii
    """
    if not baza_jest.get():
        with open("baza.json", "w") as f:
            json.dump({}, f)
        baza_jest.set(True)

    if co == 1:
        with open("baza.json", "r") as f:
            data = json.load(f)

            data[wybrana_kat.get()].append(tekst)

        with open("baza.json", "w") as f:
            json.dump(data, f)

    elif co == 0:
        with open("baza.json", "r") as f:
            data = json.load(f)

            data[tekst] = []

        with open("baza.json", "w") as f:
            json.dump(data, f)


def ile_pytan():
    """Determinacja ilości pytań w wybranej kategorii."""
    with open("baza.json", "r") as f:
        data = json.load(f)
    pytania = data[wybrana_kat.get()]
    poz_zag.set(len(pytania))


def ch_kat():
    """Wybór kategorii."""
    def end():
        """Procedura zakończenia funkcji ch_kat z odpowiednimi odesłaniami do innych funkcji."""
        if not wybrana_kat.get() == "<brak>":
            ile_pytan()
            if dod_pyt_klik.get():
                dodaj_pyt()
                choose_kat.destroy()
                dod_pyt_klik.set(False)
                baza_check()
            elif usun_klik.get():
                usuwanie()
                choose_kat.destroy()
                usun_klik.set(False)
                baza_check()
            else:
                choose_kat.destroy()
                baza_check()

            if wybrana_kat.get() != "":
                bez_powt.config(state="normal")
        else:
            wybrana_kat.set("")
            choose_kat.destroy()

    baza_check()

    if not baza_jest.get():
        warn("Brak kategorii! Utwórz nową.", dodaj_kat)
    else:
        if wybrana_kat.get() == "":
            wybrana_kat.set("<brak>")
        choose_kat = Toplevel(gl_ok)
        choose_kat.title("Wybór kategorii")
        choose_kat.attributes('-toolwindow', True)
        choose_kat.resizable(False, False)
        choose_kat.grab_set()
        choose_kat.protocol("WM_DELETE_WINDOW", end)
        choose_kat.geometry("200x60+{}+{}".format(int(gl_ok.winfo_screenwidth() / 2 - gl_ok.winfo_reqwidth() / 2),
                                                  int(gl_ok.winfo_screenheight() / 2 - gl_ok.winfo_reqheight() / 2)))

        kat_menu = tk.OptionMenu(choose_kat, wybrana_kat, "")
        kat_menu.grid(sticky="esw", row=0, column=1, columnspan=2)
        kat_menu.config(width=25)
        ttk.Button(choose_kat, text="Ok", command=lambda: (end(), rezultat.clear()))\
            .grid(sticky="ew", row=1, column=1, columnspan=2)
        with open("baza.json", "r") as f:
            data = json.load(f)

        kategorie = list(data.keys())
        pozycja = kat_menu["menu"]
        pozycja.delete(0, 'end')
        for kategoria in kategorie:
            pozycja.add_command(label=kategoria, command=lambda value=kategoria: wybrana_kat.set(value))


def checked():
    """Wykonuje operacje w zależności od stanu checkbox 'Losowania bez powtórzeń'"""
    if powt.get():
        counter_label.grid()
        counter.grid()
        ile_pytan()
    else:
        counter_label.grid_remove()
        counter.grid_remove()
        rezultat.clear()
        losowanie.state(["!disabled"])


def losuj():
    """Funkcja losująca zagadnienie z bazy na podstawie wybranej kategorii."""
    with open("baza.json", "r") as f:
        data = json.load(f)
    pytania = data[wybrana_kat.get()]

    if powt.get():
        los = 0
        while los in rezultat:
            los = random.randint(0, (len(pytania) - 1))
        rezultat.append(los)
        poz_zag.set(poz_zag.get() - 1)
        wylosowane.set(pytania[los])
        if poz_zag.get() == 0:
            bez_powt.invoke()
    else:
        los = random.randint(0, (len(pytania) - 1))
        wylosowane.set(pytania[los])


# Główne okno:
gl_ok = Tk()
gl_ok.title("Egzaminator")
gl_ok.resizable(False, False)
gl_ok.geometry("318x100+{}+{}".format(int(gl_ok.winfo_screenwidth() / 2 - gl_ok.winfo_reqwidth() / 2),
                                      int(gl_ok.winfo_screenheight() / 2 - gl_ok.winfo_reqheight() / 2)))
# Zmienne:
baza_jest = BooleanVar()
wybrana_kat = StringVar()
wybrane_pyt = StringVar()
dod_pyt_klik = BooleanVar()
usun_klik = BooleanVar()
wylosowane = StringVar()
powt = BooleanVar()
poz_zag = IntVar()
rezultat = []

# Przyciski:
ttk.Label(gl_ok, textvariable=wylosowane, background="white")\
    .grid(sticky="ew", row=0, column=0, columnspan=6)
wybierz = ttk.Button(gl_ok, text="Wybierz kategorię", command=lambda: ch_kat())
wybierz.grid(sticky="ew", row=1, column=0, columnspan=2)
losowanie = ttk.Button(gl_ok, text="Losuj zagadnienie", command=lambda: losuj())
losowanie.grid(sticky="ew", row=1, column=2, columnspan=2)
# Przycisk edycji bazy. Wyświetla menu drop-down.
dodaj = ttk.Button(gl_ok, text="Baza")
dodaj.grid(sticky="ew", row=1, column=4, columnspan=2)
dodaj.bind("<Button-1>", lambda event: dodaj_menu.post(event.x_root, event.y_root))
# Przełącznik losowania bez powtórzeń:
bez_powt = Checkbutton(gl_ok, text="Losuj bez powtórzeń", variable=powt, command=lambda: checked())
bez_powt.grid(row=2, column=0)
bez_powt.config(state="disabled")
# Licznik pozostałych pytań (tylko gdy włączone jest losowanie bez powtórzeń):
counter_label = ttk.Label(gl_ok, text="Licznik:")
counter_label.grid(row=2, column=4)
counter_label.grid_remove()
counter = ttk.Label(gl_ok, textvariable=poz_zag)
counter.grid(row=2, column=5)
counter.grid_remove()
# Przycisk wyjścia z programu:
ttk.Button(gl_ok, text="Zakończ", command=gl_ok.destroy).grid(sticky="ew", row=3, columnspan=6)

# Menu typu drop-down do zarządzania bazą:
dodaj_menu = Menu(gl_ok, tearoff=0)
dodaj_menu.add_command(label="Dodaj kategorię", command=lambda: dodaj_kat())
dodaj_menu.add_command(label="Dodaj zagadnienia", command=lambda: dodaj_pyt())
dodaj_menu.add_command(label="Usuwanie z bazy", command=lambda: usuwanie())


baza_check()

gl_ok.mainloop()

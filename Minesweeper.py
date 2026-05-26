#!/usr/bin/env python3
# Minesweeper_mac.py
import sys, random, time, json, os, tempfile, locale
from PyQt5 import QtWidgets, QtCore, QtGui

# Global UI scale factor (1.0 = default). Erhöhe z.B. auf 1.2 für größere UI.
if sys.platform == "darwin":  # "darwin" steht für macOS
    UI_SCALE = 1.4
else:
    UI_SCALE = 1.0

# High DPI attributes must be set before QApplication creation
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# --- Minimal TRANSLATIONS map (füge volle Map falls gewünscht) ---
CURRENT_LANG = "en"
TRANSLATIONS = {
    "de": {
        "Rows:": "Zeilen:", "Cols:": "Spalten:", "Mines:": "Minen:",
        "Invalid Values": "Ungültige Werte", "Please enter valid numbers.": "Bitte gültige Zahlen eingeben.",
        "Minesweeper - Start": "Minesweeper - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nWähle Schwierigkeit oder Benutzerdefiniert",
        "Easy\n9×9 • 10": "Leicht\n9×9 • 10", "Medium\n16×16 • 40": "Mittel\n16×16 • 40", "Hard\n16×30 • 99": "Schwer\n16×30 • 99",
        "Custom": "Benutzerdefiniert", "Start": "Start", "Exit": "Beenden",
        "Minesweeper": "Minesweeper", "New": "Neu", "Safe Move": "Sicheren Zug",
        "Victory": "Gewonnen", "You won in %1 seconds.": "Du hast gewonnen in %1 Sekunden.",
        "Game Over": "Verloren", "You lost. Start a new game?": "Du hast verloren. Neues Spiel starten?",
        "No safe move found.": "Kein sicherer Zug gefunden.", "Time: %1s": "Zeit: %1s",
        "Mines: %1  Flags: %2": "Minen: %1  Flags: %2",
    },
    "fr": {
        "Rows:": "Lignes :",
        "Cols:": "Colonnes :",
        "Mines:": "Mines :",
        "Invalid Values": "Valeurs non valides",
        "Please enter valid numbers.": "Veuillez entrer des nombres valides.",
        "Minesweeper - Start": "Démineur - Démarrage",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Démineur</b>\nChoisissez la difficulté ou personnalisé",
        "Easy\n9×9 • 10": "Facile\n9×9 • 10",
        "Medium\n16×16 • 40": "Moyen\n16×16 • 40",
        "Hard\n16×30 • 99": "Difficile\n16×30 • 99",
        "Custom": "Personnalisé",
        "Start": "Démarrer",
        "Exit": "Quitter",
        "Minesweeper": "Démineur",
        "New": "Nouveau",
        "Safe Move": "Coup sûr",
        "Victory": "Victoire",
        "You won in %1 seconds.": "Vous avez gagné en %1 secondes.",
        "Game Over": "Perdu",
        "You lost. Start a new game?": "Vous avez perdu. Nouvelle partie ?",
        "No safe move found.": "Aucun coup sûr trouvé.",
        "Time: %1s": "Temps : %1s",
        "Mines: %1  Flags: %2": "Mines : %1  Drapeaux : %2",
    },
    "es": {
        "Rows:": "Filas:",
        "Cols:": "Columnas:",
        "Mines:": "Minas:",
        "Invalid Values": "Valores no válidos",
        "Please enter valid numbers.": "Por favor, introduce números válidos.",
        "Minesweeper - Start": "Buscaminas - Inicio",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Buscaminas</b>\nElige dificultad o personalizado",
        "Easy\n9×9 • 10": "Fácil\n9×9 • 10",
        "Medium\n16×16 • 40": "Medio\n16×16 • 40",
        "Hard\n16×30 • 99": "Difícil\n16×30 • 99",
        "Custom": "Personalizado",
        "Start": "Empezar",
        "Exit": "Salir",
        "Minesweeper": "Buscaminas",
        "New": "Nuevo",
        "Safe Move": "Jugada segura",
        "Victory": "Victoria",
        "You won in %1 seconds.": "Has ganado en %1 segundos.",
        "Game Over": "Has perdido",
        "You lost. Start a new game?": "Has perdido. ¿Empezar una nueva partida?",
        "No safe move found.": "No se encontró ninguna jugada segura.",
        "Time: %1s": "Tiempo: %1s",
        "Mines: %1  Flags: %2": "Minas: %1  Banderas: %2",
    },
    "it": {
        "Rows:": "Righe:",
        "Cols:": "Colonne:",
        "Mines:": "Mine:",
        "Invalid Values": "Valori non validi",
        "Please enter valid numbers.": "Per favore, inserisci numeri validi.",
        "Minesweeper - Start": "Campo Minato - Inizio",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Campo Minato</b>\nScegli la difficoltà o personalizza",
        "Easy\n9×9 • 10": "Facile\n9×9 • 10",
        "Medium\n16×16 • 40": "Medio\n16×16 • 40",
        "Hard\n16×30 • 99": "Difficile\n16×30 • 99",
        "Custom": "Personalizzato",
        "Start": "Inizia",
        "Exit": "Esci",
        "Minesweeper": "Campo Minato",
        "New": "Nuovo",
        "Safe Move": "Mossa sicura",
        "Victory": "Vittoria",
        "You won in %1 seconds.": "Hai vinto in %1 secondi.",
        "Game Over": "Hai perso",
        "You lost. Start a new game?": "Hai perso. Iniziare una nuova partita?",
        "No safe move found.": "Nessuna mossa sicura trovata.",
        "Time: %1s": "Tempo: %1s",
        "Mines: %1  Flags: %2": "Mine: %1  Bandiere: %2",
    },
    "ru": {
        "Rows:": "Строки:",
        "Cols:": "Столбцы:",
        "Mines:": "Мины:",
        "Invalid Values": "Неверные значения",
        "Please enter valid numbers.": "Введите корректные числа.",
        "Minesweeper - Start": "Сапёр - Старт",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Сапёр</b>\nВыберите сложность или свои настройки",
        "Easy\n9×9 • 10": "Легко\n9×9 • 10",
        "Medium\n16×16 • 40": "Средне\n16×16 • 40",
        "Hard\n16×30 • 99": "Сложно\n16×30 • 99",
        "Custom": "Свой",
        "Start": "Старт",
        "Exit": "Выход",
        "Minesweeper": "Сапёр",
        "New": "Новая",
        "Safe Move": "Безопасный ход",
        "Victory": "Победа",
        "You won in %1 seconds.": "Вы победили за %1 секунд.",
        "Game Over": "Проигрыш",
        "You lost. Start a new game?": "Вы проиграли. Начать новую игру?",
        "No safe move found.": "Безопасный ход не найден.",
        "Time: %1s": "Время: %1с",
        "Mines: %1  Flags: %2": "Мины: %1  Флаги: %2",
    },
    "uk": {
        "Rows:": "Рядки:",
        "Cols:": "Стовпці:",
        "Mines:": "Міни:",
        "Invalid Values": "Недійсні значення",
        "Please enter valid numbers.": "Будь ласка, введіть дійсні числа.",
        "Minesweeper - Start": "Сапер - Старт",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Сапер</b>\nОберіть складність або власні налаштування",
        "Easy\n9×9 • 10": "Легко\n9×9 • 10",
        "Medium\n16×16 • 40": "Середньо\n16×16 • 40",
        "Hard\n16×30 • 99": "Важко\n16×30 • 99",
        "Custom": "Власні",
        "Start": "Старт",
        "Exit": "Вихід",
        "Minesweeper": "Сапер",
        "New": "Нова",
        "Safe Move": "Безпечний хід",
        "Victory": "Перемога",
        "You won in %1 seconds.": "Ви виграли за %1 секунд.",
        "Game Over": "Поразка",
        "You lost. Start a new game?": "Ви програли. Почати нову гру?",
        "No safe move found.": "Безпечний хід не знайдено.",
        "Time: %1s": "Час: %1с",
        "Mines: %1  Flags: %2": "Мін: %1  Прапорців: %2",
    },
    "hu": {
        "Rows:": "Sorok:",
        "Cols:": "Oszlopok:",
        "Mines:": "Aknamezők:",
        "Invalid Values": "Érvénytelen értékek",
        "Please enter valid numbers.": "Kérlek adj meg érvényes számokat.",
        "Minesweeper - Start": "Aknakereső - Kezdés",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Aknakereső</b>\nVálassz nehézséget vagy személyre szabottat",
        "Easy\n9×9 • 10": "Könnyű\n9×9 • 10",
        "Medium\n16×16 • 40": "Közepes\n16×16 • 40",
        "Hard\n16×30 • 99": "Nehéz\n16×30 • 99",
        "Custom": "Testreszabott",
        "Start": "Indítás",
        "Exit": "Kilépés",
        "Minesweeper": "Aknakereső",
        "New": "Új",
        "Safe Move": "Biztonságos lépés",
        "Victory": "Győzelem",
        "You won in %1 seconds.": "Nyertél %1 másodperc alatt.",
        "Game Over": "Vesztettél",
        "You lost. Start a new game?": "Vesztettél. Új játék indítása?",
        "No safe move found.": "Nem található biztonságos lépés.",
        "Time: %1s": "Idő: %1s",
        "Mines: %1  Flags: %2": "Aknák: %1  Zászlók: %2",
    },
    "pl": {
        "Rows:": "Wiersze:",
        "Cols:": "Kolumny:",
        "Mines:": "Miny:",
        "Invalid Values": "Nieprawidłowe wartości",
        "Please enter valid numbers.": "Proszę wprowadzić poprawne liczby.",
        "Minesweeper - Start": "Saper - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Saper</b>\nWybierz poziom trudności lub własny",
        "Easy\n9×9 • 10": "Łatwy\n9×9 • 10",
        "Medium\n16×16 • 40": "Średni\n16×16 • 40",
        "Hard\n16×30 • 99": "Trudny\n16×30 • 99",
        "Custom": "Niestandardowy",
        "Start": "Start",
        "Exit": "Wyjście",
        "Minesweeper": "Saper",
        "New": "Nowa",
        "Safe Move": "Bezpieczny ruch",
        "Victory": "Zwycięstwo",
        "You won in %1 seconds.": "Wygrałeś w %1 sekund.",
        "Game Over": "Koniec gry",
        "You lost. Start a new game?": "Przegrałeś. Rozpocząć nową grę?",
        "No safe move found.": "Nie znaleziono bezpiecznego ruchu.",
        "Time: %1s": "Czas: %1s",
        "Mines: %1  Flags: %2": "Miny: %1  Flag: %2",
    },

    "nl": {
        "Rows:": "Rijen:",
        "Cols:": "Kolommen:",
        "Mines:": "Mijnen:",
        "Invalid Values": "Ongeldige waarden",
        "Please enter valid numbers.": "Voer alstublieft geldige nummers in.",
        "Minesweeper - Start": "Mijnveger - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Mijnveger</b>\nKies moeilijkheidsgraad of aangepast",
        "Easy\n9×9 • 10": "Makkelijk\n9×9 • 10",
        "Medium\n16×16 • 40": "Gemiddeld\n16×16 • 40",
        "Hard\n16×30 • 99": "Moeilijk\n16×30 • 99",
        "Custom": "Aangepast",
        "Start": "Start",
        "Exit": "Afsluiten",
        "Minesweeper": "Mijnveger",
        "New": "Nieuw",
        "Safe Move": "Veilige zet",
        "Victory": "Overwinning",
        "You won in %1 seconds.": "Je hebt gewonnen in %1 seconden.",
        "Game Over": "Game over",
        "You lost. Start a new game?": "Je hebt verloren. Nieuw spel starten?",
        "No safe move found.": "Geen veilige zet gevonden.",
        "Time: %1s": "Tijd: %1s",
        "Mines: %1  Flags: %2": "Mijnen: %1  Vlaggen: %2",
    },
    "pt": {
        "Rows:": "Linhas:",
        "Cols:": "Colunas:",
        "Mines:": "Minas:",
        "Invalid Values": "Valores inválidos",
        "Please enter valid numbers.": "Por favor, insira números válidos.",
        "Minesweeper - Start": "Campo Minado - Início",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Campo Minado</b>\nEscolha dificuldade ou personalizado",
        "Easy\n9×9 • 10": "Fácil\n9×9 • 10",
        "Medium\n16×16 • 40": "Médio\n16×16 • 40",
        "Hard\n16×30 • 99": "Difícil\n16×30 • 99",
        "Custom": "Personalizado",
        "Start": "Iniciar",
        "Exit": "Sair",
        "Minesweeper": "Campo Minado",
        "New": "Novo",
        "Safe Move": "Jogada segura",
        "Victory": "Vitória",
        "You won in %1 seconds.": "Você venceu em %1 segundos.",
        "Game Over": "Fim de jogo",
        "You lost. Start a new game?": "Você perdeu. Começar um novo jogo?",
        "No safe move found.": "Nenhuma jogada segura encontrada.",
        "Time: %1s": "Tempo: %1s",
        "Mines: %1  Flags: %2": "Minas: %1  Bandeiras: %2",
    },

    "cs": {
        "Rows:": "Řádky:",
        "Cols:": "Sloupce:",
        "Mines:": "Míny:",
        "Invalid Values": "Neplatné hodnoty",
        "Please enter valid numbers.": "Zadejte prosím platná čísla.",
        "Minesweeper - Start": "Mína - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Mína</b>\nVyberte obtížnost nebo vlastní",
        "Easy\n9×9 • 10": "Lehké\n9×9 • 10",
        "Medium\n16×16 • 40": "Střední\n16×16 • 40",
        "Hard\n16×30 • 99": "Těžké\n16×30 • 99",
        "Custom": "Vlastní",
        "Start": "Start",
        "Exit": "Ukončit",
        "Minesweeper": "Mína",
        "New": "Nová",
        "Safe Move": "Bezpečný tah",
        "Victory": "Vítězství",
        "You won in %1 seconds.": "Vyhrál jste za %1 sekund.",
        "Game Over": "Konec hry",
        "You lost. Start a new game?": "Prohráli jste. Spustit novou hru?",
        "No safe move found.": "Nebylo nalezeno bezpečné pole.",
        "Time: %1s": "Čas: %1s",
        "Mines: %1  Flags: %2": "Míny: %1  Vlajky: %2",
    },

    "ro": {
        "Rows:": "Rânduri:",
        "Cols:": "Coloane:",
        "Mines:": "Mine:",
        "Invalid Values": "Valori invalide",
        "Please enter valid numbers.": "Te rog introdu numere valide.",
        "Minesweeper - Start": "Minesweeper - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nAlege dificultatea sau personalizat",
        "Easy\n9×9 • 10": "Ușor\n9×9 • 10",
        "Medium\n16×16 • 40": "Mediu\n16×16 • 40",
        "Hard\n16×30 • 99": "Greu\n16×30 • 99",
        "Custom": "Personalizat",
        "Start": "Start",
        "Exit": "Ieșire",
        "Minesweeper": "Minesweeper",
        "New": "Nou",
        "Safe Move": "Mutare sigură",
        "Victory": "Victorie",
        "You won in %1 seconds.": "Ai câștigat în %1 secunde.",
        "Game Over": "Sfârșitul jocului",
        "You lost. Start a new game?": "Ai pierdut. Începi un joc nou?",
        "No safe move found.": "Nu s-a găsit mutare sigură.",
        "Time: %1s": "Timp: %1s",
        "Mines: %1  Flags: %2": "Mine: %1  Steaguri: %2",
    },

    "el": {
        "Rows:": "Γραμμές:",
        "Cols:": "Στήλες:",
        "Mines:": "Νάρκες:",
        "Invalid Values": "Μη έγκυρες τιμές",
        "Please enter valid numbers.": "Παρακαλώ εισάγετε έγκυρους αριθμούς.",
        "Minesweeper - Start": "Ναρκαλιευτής - Έναρξη",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Ναρκαλιευτής</b>\nΕπιλέξτε δυσκολία ή προσαρμοσμένο",
        "Easy\n9×9 • 10": "Εύκολο\n9×9 • 10",
        "Medium\n16×16 • 40": "Μέτριο\n16×16 • 40",
        "Hard\n16×30 • 99": "Δύσκολο\n16×30 • 99",
        "Custom": "Προσαρμοσμένο",
        "Start": "Έναρξη",
        "Exit": "Έξοδος",
        "Minesweeper": "Ναρκαλιευτής",
        "New": "Νέο",
        "Safe Move": "Ασφαλές βήμα",
        "Victory": "Νίκη",
        "You won in %1 seconds.": "Κέρδισες σε %1 δευτερόλεπτα.",
        "Game Over": "Τέλος παιχνιδιού",
        "You lost. Start a new game?": "Έχασες. Να ξεκινήσει νέο παιχνίδι;",
        "No safe move found.": "Δεν βρέθηκε ασφαλές βήμα.",
        "Time: %1s": "Χρόνος: %1s",
        "Mines: %1  Flags: %2": "Νάρκες: %1  Σημαίες: %2",
    },

    "sv": {
        "Rows:": "Rader:",
        "Cols:": "Kolumner:",
        "Mines:": "Minor:",
        "Invalid Values": "Ogiltiga värden",
        "Please enter valid numbers.": "Ange giltiga siffror.",
        "Minesweeper - Start": "Minesweeper - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nVälj svårighet eller anpassad",
        "Easy\n9×9 • 10": "Lätt\n9×9 • 10",
        "Medium\n16×16 • 40": "Mellan\n16×16 • 40",
        "Hard\n16×30 • 99": "Svår\n16×30 • 99",
        "Custom": "Anpassad",
        "Start": "Starta",
        "Exit": "Avsluta",
        "Minesweeper": "Minesweeper",
        "New": "Ny",
        "Safe Move": "Säkert drag",
        "Victory": "Seger",
        "You won in %1 seconds.": "Du vann på %1 sekunder.",
        "Game Over": "Spelet slut",
        "You lost. Start a new game?": "Du förlorade. Starta ett nytt spel?",
        "No safe move found.": "Inget säkert drag hittades.",
        "Time: %1s": "Tid: %1s",
        "Mines: %1  Flags: %2": "Minor: %1  Flaggor: %2",
    },
    "no": {
        "Rows:": "Rader:",
        "Cols:": "Kolonner:",
        "Mines:": "Miner:",
        "Invalid Values": "Ugyldige verdier",
        "Please enter valid numbers.": "Vennligst oppgi gyldige tall.",
        "Minesweeper - Start": "Minesveiper - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesveiper</b>\nVelg vanskelighetsgrad eller egendefinert",
        "Easy\n9×9 • 10": "Lett\n9×9 • 10",
        "Medium\n16×16 • 40": "Medium\n16×16 • 40",
        "Hard\n16×30 • 99": "Vanskelig\n16×30 • 99",
        "Custom": "Egendefinert",
        "Start": "Start",
        "Exit": "Avslutt",
        "Minesweeper": "Minesveiper",
        "New": "Ny",
        "Safe Move": "Sikkert trekk",
        "Victory": "Seier",
        "You won in %1 seconds.": "Du vant på %1 sekunder.",
        "Game Over": "Spillet over",
        "You lost. Start a new game?": "Du tapte. Starte et nytt spill?",
        "No safe move found.": "Ingen sikkert trekk funnet.",
        "Time: %1s": "Tid: %1s",
        "Mines: %1  Flags: %2": "Miner: %1  Flag: %2",
    },

    "da": {
        "Rows:": "Rækker:",
        "Cols:": "Kolonner:",
        "Mines:": "Miner:",
        "Invalid Values": "Ugyldige værdier",
        "Please enter valid numbers.": "Indtast venligst gyldige tal.",
        "Minesweeper - Start": "Minesweeper - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nVælg sværhedsgrad eller brugerdefineret",
        "Easy\n9×9 • 10": "Let\n9×9 • 10",
        "Medium\n16×16 • 40": "Mellem\n16×16 • 40",
        "Hard\n16×30 • 99": "Svær\n16×30 • 99",
        "Custom": "Brugerdefineret",
        "Start": "Start",
        "Exit": "Afslut",
        "Minesweeper": "Minesweeper",
        "New": "Ny",
        "Safe Move": "Sikkert træk",
        "Victory": "Sejr",
        "You won in %1 seconds.": "Du vandt på %1 sekunder.",
        "Game Over": "Spillet slut",
        "You lost. Start a new game?": "Du tabte. Starte et nyt spil?",
        "No safe move found.": "Intet sikkert træk fundet.",
        "Time: %1s": "Tid: %1s",
        "Mines: %1  Flags: %2": "Miner: %1  Flag: %2",
    },

    "fi": {
        "Rows:": "Rivit:",
        "Cols:": "Sarakkeet:",
        "Mines:": "Miinat:",
        "Invalid Values": "Virheelliset arvot",
        "Please enter valid numbers.": "Syötä kelvolliset numerot.",
        "Minesweeper - Start": "Miinantutkija - Käynnistys",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Miinantutkija</b>\nValitse vaikeustaso tai oma",
        "Easy\n9×9 • 10": "Helppo\n9×9 • 10",
        "Medium\n16×16 • 40": "Keskitaso\n16×16 • 40",
        "Hard\n16×30 • 99": "Vaikea\n16×30 • 99",
        "Custom": "Mukautettu",
        "Start": "Aloita",
        "Exit": "Poistu",
        "Minesweeper": "Miinantutkija",
        "New": "Uusi",
        "Safe Move": "Turvallinen siirto",
        "Victory": "Voitto",
        "You won in %1 seconds.": "Voitit %1 sekunnissa.",
        "Game Over": "Peli ohi",
        "You lost. Start a new game?": "Hävisit. Aloitetaanko uusi peli?",
        "No safe move found.": "Turvallista siirtoa ei löytynyt.",
        "Time: %1s": "Aika: %1s",
        "Mines: %1  Flags: %2": "Miinat: %1  Liput: %2",
    },

    "bg": {
        "Rows:": "Редове:",
        "Cols:": "Колони:",
        "Mines:": "Мини:",
        "Invalid Values": "Невалидни стойности",
        "Please enter valid numbers.": "Моля, въведете валидни числа.",
        "Minesweeper - Start": "Миньор - Старт",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Миньор</b>\nИзберете трудност или персонализирано",
        "Easy\n9×9 • 10": "Лесно\n9×9 • 10",
        "Medium\n16×16 • 40": "Средно\n16×16 • 40",
        "Hard\n16×30 • 99": "Трудно\n16×30 • 99",
        "Custom": "Персонализирано",
        "Start": "Старт",
        "Exit": "Изход",
        "Minesweeper": "Миньор",
        "New": "Ново",
        "Safe Move": "Безопасен ход",
        "Victory": "Победа",
        "You won in %1 seconds.": "Победихте за %1 секунди.",
        "Game Over": "Край на играта",
        "You lost. Start a new game?": "Загубихте. Да започнем нова игра?",
        "No safe move found.": "Не е намерен безопасен ход.",
        "Time: %1s": "Време: %1s",
        "Mines: %1  Flags: %2": "Мини: %1  Знамена: %2",
    },

    "hr": {
        "Rows:": "Redovi:",
        "Cols:": "Stupci:",
        "Mines:": "Mina:",
        "Invalid Values": "Nevažeće vrijednosti",
        "Please enter valid numbers.": "Unesite važeće brojeve.",
        "Minesweeper - Start": "Minesweeper - Početak",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nOdaberite težinu ili prilagođeno",
        "Easy\n9×9 • 10": "Lako\n9×9 • 10",
        "Medium\n16×16 • 40": "Srednje\n16×16 • 40",
        "Hard\n16×30 • 99": "Teško\n16×30 • 99",
        "Custom": "Prilagođeno",
        "Start": "Start",
        "Exit": "Izađi",
        "Minesweeper": "Minesweeper",
        "New": "Novo",
        "Safe Move": "Sigurni potez",
        "Victory": "Pobjeda",
        "You won in %1 seconds.": "Pobijedili ste za %1 sekundi.",
        "Game Over": "Kraj igre",
        "You lost. Start a new game?": "Izgubili ste. Zapoceti novu igru?",
        "No safe move found.": "Nije pronađen siguran potez.",
        "Time: %1s": "Vrijeme: %1s",
        "Mines: %1  Flags: %2": "Mine: %1  Zastave: %2",
    },

    "sr": {
        "Rows:": "Redovi:",
        "Cols:": "Kolone:",
        "Mines:": "Mine:",
        "Invalid Values": "Nevažeće vrednosti",
        "Please enter valid numbers.": "Unesite ispravne brojeve.",
        "Minesweeper - Start": "Saper - Početak",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Saper</b>\nIzaberite težinu ili prilagođeno",
        "Easy\n9×9 • 10": "Lako\n9×9 • 10",
        "Medium\n16×16 • 40": "Srednje\n16×16 • 40",
        "Hard\n16×30 • 99": "Teško\n16×30 • 99",
        "Custom": "Prilagođeno",
        "Start": "Start",
        "Exit": "Izlaz",
        "Minesweeper": "Saper",
        "New": "Novo",
        "Safe Move": "Siguran potez",
        "Victory": "Pobeda",
        "You won in %1 seconds.": "Pobedili ste za %1 sekundi.",
        "Game Over": "Kraj igre",
        "You lost. Start a new game?": "Izgubili ste. Početi novu igru?",
        "No safe move found.": "Nije pronađen siguran potez.",
        "Time: %1s": "Vreme: %1s",
        "Mines: %1  Flags: %2": "Mine: %1  Zastave: %2",
    },
    "sk": {
        "Rows:": "Riadky:",
        "Cols:": "Stĺpce:",
        "Mines:": "Míny:",
        "Invalid Values": "Neplatné hodnoty",
        "Please enter valid numbers.": "Zadajte platné čísla, prosím.",
        "Minesweeper - Start": "Minesweeper - Štart",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nVyberte obtiažnosť alebo vlastné nastavenie",
        "Easy\n9×9 • 10": "Ľahké\n9×9 • 10",
        "Medium\n16×16 • 40": "Stredné\n16×16 • 40",
        "Hard\n16×30 • 99": "Ťažké\n16×30 • 99",
        "Custom": "Vlastné",
        "Start": "Štart",
        "Exit": "Ukončiť",
        "Minesweeper": "Minesweeper",
        "New": "Nové",
        "Safe Move": "Bezpečný ťah",
        "Victory": "Víťazstvo",
        "You won in %1 seconds.": "Vyhrali ste za %1 sekúnd.",
        "Game Over": "Koniec hry",
        "You lost. Start a new game?": "Prehrali ste. Spustiť novú hru?",
        "No safe move found.": "Nenašiel sa bezpečný ťah.",
        "Time: %1s": "Čas: %1s",
        "Mines: %1  Flags: %2": "Míny: %1  Vlajky: %2",
    },

    "sl": {
        "Rows:": "Vrstice:",
        "Cols:": "Stolpci:",
        "Mines:": "Mine:",
        "Invalid Values": "Neveljavne vrednosti",
        "Please enter valid numbers.": "Vnesite veljavne številke, prosim.",
        "Minesweeper - Start": "Minolovec - Začetek",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minolovec</b>\nIzberite težavnost ali prilagojeno",
        "Easy\n9×9 • 10": "Enostavno\n9×9 • 10",
        "Medium\n16×16 • 40": "Srednje\n16×16 • 40",
        "Hard\n16×30 • 99": "Težko\n16×30 • 99",
        "Custom": "Po meri",
        "Start": "Začni",
        "Exit": "Izhod",
        "Minesweeper": "Minolovec",
        "New": "Novo",
        "Safe Move": "Varen korak",
        "Victory": "Zmaga",
        "You won in %1 seconds.": "Zmagali ste v %1 sekundah.",
        "Game Over": "Konec igre",
        "You lost. Start a new game?": "Izgubili ste. Začetek nove igre?",
        "No safe move found.": "Ni najden varen korak.",
        "Time: %1s": "Čas: %1s",
        "Mines: %1  Flags: %2": "Mine: %1  Zastavice: %2",
    },

    "lt": {
        "Rows:": "Eilutės:",
        "Cols:": "Stulpeliai:",
        "Mines:": "Mines:",
        "Invalid Values": "Neteisingos reikšmės",
        "Please enter valid numbers.": "Įveskite galiojančius skaičius, prašome.",
        "Minesweeper - Start": "Minesweeper - Pradžia",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nPasirinkite sunkumą arba pritaikytą",
        "Easy\n9×9 • 10": "Lengva\n9×9 • 10",
        "Medium\n16×16 • 40": "Vidutinė\n16×16 • 40",
        "Hard\n16×30 • 99": "Sunku\n16×30 • 99",
        "Custom": "Pritaikyta",
        "Start": "Pradėti",
        "Exit": "Išeiti",
        "Minesweeper": "Minesweeper",
        "New": "Naujas",
        "Safe Move": "Saugus ėjimas",
        "Victory": "Pergalė",
        "You won in %1 seconds.": "Jūs laimėjote per %1 sekundžių.",
        "Game Over": "Žaidimas baigtas",
        "You lost. Start a new game?": "Pralaimėjote. Pradėti naują žaidimą?",
        "No safe move found.": "Nerasta saugių ėjimų.",
        "Time: %1s": "Laikas: %1s",
        "Mines: %1  Flags: %2": "Minos: %1  Vėliavos: %2",
    },

    "lv": {
        "Rows:": "Rindas:",
        "Cols:": "Kolonnas:",
        "Mines:": "Mīnas:",
        "Invalid Values": "Nederīgas vērtības",
        "Please enter valid numbers.": "Lūdzu ievadiet derīgus skaitļus.",
        "Minesweeper - Start": "Minesweeper - Sākums",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nIzvēlieties grūtības pakāpi vai pielāgotu",
        "Easy\n9×9 • 10": "Viegls\n9×9 • 10",
        "Medium\n16×16 • 40": "Vidējs\n16×16 • 40",
        "Hard\n16×30 • 99": "Grūti\n16×30 • 99",
        "Custom": "Pielāgots",
        "Start": "Sākt",
        "Exit": "Iziet",
        "Minesweeper": "Minesweeper",
        "New": "Jauns",
        "Safe Move": "Droša gājiena",
        "Victory": "Uzvara",
        "You won in %1 seconds.": "Jūs uzvarējāt %1 sekundēs.",
        "Game Over": "Spēle beigusies",
        "You lost. Start a new game?": "Jūs zaudējāt. Sākt jaunu spēli?",
        "No safe move found.": "Nav atrasts drošs gājiens.",
        "Time: %1s": "Laiks: %1s",
        "Mines: %1  Flags: %2": "Mīnas: %1  Karogi: %2",
    },

    "et": {
        "Rows:": "Read:",
        "Cols:": "Veerud:",
        "Mines:": "Miinad:",
        "Invalid Values": "Kehtetud väärtused",
        "Please enter valid numbers.": "Sisesta palun kehtivad numbrid.",
        "Minesweeper - Start": "Miinijaht - Algus",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Miinijaht</b>\nVali raskusaste või kohandatud",
        "Easy\n9×9 • 10": "Lihtne\n9×9 • 10",
        "Medium\n16×16 • 40": "Keskmine\n16×16 • 40",
        "Hard\n16×30 • 99": "Raske\n16×30 • 99",
        "Custom": "Kohandatud",
        "Start": "Alusta",
        "Exit": "Välju",
        "Minesweeper": "Miinijaht",
        "New": "Uus",
        "Safe Move": "Turvaline käik",
        "Victory": "Võit",
        "You won in %1 seconds.": "Sa võitsid %1 sekundiga.",
        "Game Over": "Mäng läbi",
        "You lost. Start a new game?": "Sa kaotasid. Alustada uut mängu?",
        "No safe move found.": "Turvalist käiku ei leitud.",
        "Time: %1s": "Aeg: %1s",
        "Mines: %1  Flags: %2": "Miinad: %1  Lipud: %2",
    },

    "mt": {
        "Rows:": "Ringieli:",
        "Cols:": "Kolonni:",
        "Mines:": "Minj:",
        "Invalid Values": "Valuri invalidi",
        "Please enter valid numbers.": "Jekk jogħġbok daħħal numri validi.",
        "Minesweeper - Start": "Minesweeper - Start",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nAgħżel diffikultà jew personalizzat",
        "Easy\n9×9 • 10": "Faċli\n9×9 • 10",
        "Medium\n16×16 • 40": "Medju\n16×16 • 40",
        "Hard\n16×30 • 99": "Tqil\n16×30 • 99",
        "Custom": "Personalizzat",
        "Start": "Ibda",
        "Exit": "Irtira",
        "Minesweeper": "Minesweeper",
        "New": "Ġdid",
        "Safe Move": "Moviment sigur",
        "Victory": "Rebħa",
        "You won in %1 seconds.": "Irbuħt f'%1 sekondi.",
        "Game Over": "Il-logħba spiċċat",
        "You lost. Start a new game?": "Għedt tilfu. Tibda logħba ġdida?",
        "No safe move found.": "Ma nstab l-ebda moviment sigur.",
        "Time: %1s": "Ħin: %1s",
        "Mines: %1  Flags: %2": "Minj: %1  Bandiere: %2",
    },

    "ga": {
        "Rows:": "Rannaí:",
        "Cols:": "Colúin:",
        "Mines:": "Míniúintí:",
        "Invalid Values": "Luachanna neamhbhailí",
        "Please enter valid numbers.": "Iontráil uimhreacha bailí, le do thoil.",
        "Minesweeper - Start": "Minesweeper - Tús",
        "<b>Minesweeper</b>\nChoose difficulty or custom": "<b>Minesweeper</b>\nRoghnaigh deacracht nó saincheaptha",
        "Easy\n9×9 • 10": "Éasca\n9×9 • 10",
        "Medium\n16×16 • 40": "Meánach\n16×16 • 40",
        "Hard\n16×30 • 99": "Deacair\n16×30 • 99",
        "Custom": "Saincheaptha",
        "Start": "Tosú",
        "Exit": "Scoir",
        "Minesweeper": "Minesweeper",
        "New": "Nua",
        "Safe Move": "Bogha sábháilte",
        "Victory": "Bua",
        "You won in %1 seconds.": "Bhí tú buacach i %1 soicind.",
        "Game Over": "Cluiche thart",
        "You lost. Start a new game?": "Chaill tú. Tús nua a thosú?",
        "No safe move found.": "Ní bhfuarthas bogha sábháilte.",
        "Time: %1s": "Am: %1s",
        "Mines: %1  Flags: %2": "Míniúintí: %1  Bratacha: %2",
    },
}

# Only these 4 languages are offered in the UI selector
SUPPORTED_LANGS = [
    ("bg", "🇧🇬  Български"),
    ("cs", "🇨🇿  Čeština"),
    ("da", "🇩🇰  Dansk"),
    ("de", "🇩🇪  Deutsch"),
    ("el", "🇬🇷  Ελληνικά"),
    ("en", "🇬🇧  English"),
    ("es", "🇪🇸  Español"),
    ("et", "🇪🇪  Eesti"),
    ("fi", "🇫🇮  Suomi"),
    ("fr", "🇫🇷  Français"),
    ("ga", "🇮🇪  Gaeilge"),
    ("hr", "🇭🇷  Hrvatski"),
    ("hu", "🇭🇺  Magyar"),
    ("it", "🇮🇹  Italiano"),
    ("lt", "🇱🇹  Lietuvių"),
    ("lv", "🇱🇻  Latviešu"),
    ("mt", "🇲🇹  Malti"),
    ("nl", "🇳🇱  Nederlands"),
    ("no", "🇳🇴  Norsk"),
    ("pl", "🇵🇱  Polski"),
    ("pt", "🇵🇹  Português"),
    ("ro", "🇷🇴  Română"),
    ("ru", "🇷🇺  Русский"),
    ("sk", "🇸🇰  Slovenčina"),
    ("sl", "🇸🇮  Slovenščina"),
    ("sr", "🇷🇸  Српски"),
    ("sv", "🇸🇪  Svenska"),
    ("uk", "🇺🇦  Українська"),
]
# Config file in the OS-appropriate user data directory
def _get_config_file():
    import platform
    app_name = "Minesweeper"
    if platform.system() == "Windows":
        # Windows: C:\Users\<user>\AppData\Roaming\Minesweeper\
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    elif platform.system() == "Darwin":
        # macOS: ~/Library/Application Support/Minesweeper/
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        # Linux: ~/.config/Minesweeper/  (respects XDG_CONFIG_HOME)
        base = os.environ.get("XDG_CONFIG_HOME", os.path.join(os.path.expanduser("~"), ".config"))
    config_dir = os.path.join(base, app_name)
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "minesweeper_config.json")

_CONFIG_FILE = _get_config_file()

def _load_saved_lang():
    """Return the language code saved in the config file, or 'en' if none."""
    try:
        with open(_CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        code = data.get("lang", "en")
        supported_codes = [c for c, _ in SUPPORTED_LANGS]
        return code if code in supported_codes else "en"
    except Exception:
        return "en"

def _save_lang(lang_code):
    """Persist the chosen language code to the config file."""
    try:
        with open(_CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump({"lang": lang_code}, f)
    except Exception:
        pass

def init_locale():
    global CURRENT_LANG
    CURRENT_LANG = _load_saved_lang()
    try:
        QtCore.QLocale.setDefault(QtCore.QLocale(CURRENT_LANG))
    except Exception:
        pass

def set_language(lang_code):
    global CURRENT_LANG
    CURRENT_LANG = lang_code
    _save_lang(lang_code)          # remember for next launch
    try:
        QtCore.QLocale.setDefault(QtCore.QLocale(CURRENT_LANG))
    except Exception:
        pass

def tr(source_text, *args):
    translated = source_text
    if CURRENT_LANG != "en":
        translated = TRANSLATIONS.get(CURRENT_LANG, {}).get(source_text, source_text)
    if args:
        for i, arg in enumerate(args):
            translated = translated.replace(f"%{i+1}", str(arg))
    return translated

init_locale()

# ---------- Model ----------
class Cell:
    def __init__(self):
        self.mine = False; self.adj = 0; self.revealed = False; self.flagged = False

class MinesModel:
    def __init__(self, rows=9, cols=9, mines=10):
        self.rows = max(1, int(rows)); self.cols = max(1, int(cols))
        max_m = self.rows * self.cols - 1
        self.mines = max(1, min(int(mines), max_m))
        self._mines_file = os.path.join(tempfile.gettempdir(), "minesweeper_mines.json")
        self.reset()
    def reset(self):
        self.grid = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]
        self.started = False; self.remaining = self.rows * self.cols - self.mines
        self.game_over = False; self.victory = False; self.start_time = None
    def _calc_adjacency(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].mine: continue
                cnt = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc].mine: cnt += 1
                self.grid[r][c].adj = cnt
    def place_mines(self, safe_r, safe_c):
        positions = [(r,c) for r in range(self.rows) for c in range(self.cols) if not (r==safe_r and c==safe_c)]
        mines_pos = random.sample(positions, self.mines)
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].mine = False
        for r,c in mines_pos:
            self.grid[r][c].mine = True
        self._calc_adjacency()
        try:
            data = {"rows": self.rows, "cols": self.cols, "mines": [[int(r), int(c)] for (r,c) in mines_pos]}
            tmp = self._mines_file + ".tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f); f.flush()
                try: os.fsync(f.fileno())
                except Exception: pass
            os.replace(tmp, self._mines_file)
        except Exception:
            try:
                if os.path.exists(tmp): os.remove(tmp)
            except Exception: pass
    def reveal(self, r, c):
        if not (0 <= r < self.rows and 0 <= c < self.cols): return
        cell = self.grid[r][c]
        if cell.revealed or cell.flagged: return
        cell.revealed = True
        if cell.mine:
            self.game_over = True; self.victory = False; return
        self.remaining -= 1
        if cell.adj == 0:
            q = [(r,c)]; visited = {(r,c)}
            while q:
                cr, cc = q.pop(0)
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = cr+dr, cc+dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            neigh = self.grid[nr][nc]
                            if (nr,nc) not in visited and not neigh.revealed and not neigh.flagged and not neigh.mine:
                                neigh.revealed = True; self.remaining -= 1; visited.add((nr,nc))
                                if neigh.adj == 0: q.append((nr,nc))
        if self.remaining == 0:
            self.game_over = True; self.victory = True
    def toggle_flag(self, r, c):
        cell = self.grid[r][c]
        if cell.revealed: return
        cell.flagged = not cell.flagged
    def simple_safe_step(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.revealed or cell.adj == 0: continue
                unknown = []; flagged = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            neigh = self.grid[nr][nc]
                            if neigh.flagged: flagged += 1
                            elif not neigh.revealed: unknown.append((nr,nc))
                rem = cell.adj - flagged
                if rem == 0 and unknown: return ("reveal", unknown[0])
                if rem == len(unknown) and unknown: return ("flag", unknown[0])
        return None
    def find_certain_safe_cells(self, max_frontier=18, max_enum=400000):
        frontier = []; constraints = []; idx_of = {}
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.revealed: continue
                unknown = []; flagged = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        if dr == 0 and dc == 0: continue
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            ncell = self.grid[nr][nc]
                            if ncell.flagged: flagged += 1
                            elif not ncell.revealed: unknown.append((nr,nc))
                if not unknown: continue
                rem = max(0, cell.adj - flagged)
                constraints.append((unknown, rem))
                for pos in unknown:
                    if pos not in idx_of: idx_of[pos] = len(frontier); frontier.append(pos)
        if not frontier: return set()
        n = len(frontier)
        if n > max_frontier: return set()
        cidx = []
        for unknown, rem in constraints:
            idxs = [idx_of[pos] for pos in unknown if pos in idx_of]
            cidx.append((idxs, rem))
        assign = [None] * n; mine_counts = [0] * n; valid = 0; aborted = False
        sys.setrecursionlimit(10000)
        def check_partial():
            for idxs, rem in cidx:
                known = 0; unknowns = 0
                for i in idxs:
                    v = assign[i]
                    if v is None: unknowns += 1
                    elif v == 1: known += 1
                if known > rem: return False
                if known + unknowns < rem: return False
            return True
        def dfs(pos=0):
            nonlocal valid, aborted
            if valid >= max_enum:
                aborted = True; return
            if pos == n:
                valid += 1
                for i in range(n):
                    if assign[i] == 1: mine_counts[i] += 1
                return
            assign[pos] = 0
            if check_partial():
                dfs(pos + 1)
                if aborted: return
            assign[pos] = 1
            if check_partial():
                dfs(pos + 1)
                if aborted: return
            assign[pos] = None
        dfs(0)
        if valid == 0: return set()
        certain_safe = set()
        for i, pos in enumerate(frontier):
            if mine_counts[i] == 0: certain_safe.add(pos)
        return certain_safe

# ---------- UI ----------
class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QLabel(tr("Rows:")), 0, 0)
        self.e_rows = QtWidgets.QLineEdit("9"); self.e_rows.setFixedWidth(80); layout.addWidget(self.e_rows, 0, 1)
        layout.addWidget(QtWidgets.QLabel(tr("Cols:")), 1, 0)
        self.e_cols = QtWidgets.QLineEdit("9"); self.e_cols.setFixedWidth(80); layout.addWidget(self.e_cols, 1, 1)
        layout.addWidget(QtWidgets.QLabel(tr("Mines:")), 2, 0)
        self.e_mines = QtWidgets.QLineEdit("10"); self.e_mines.setFixedWidth(80); layout.addWidget(self.e_mines, 2, 1)
        self.setVisible(False)
    def values(self):
        try:
            r = int(self.e_rows.text()); c = int(self.e_cols.text()); m = int(self.e_mines.text())
            if r < 1 or c < 1 or m < 1 or m >= r * c: raise ValueError
            return r, c, m
        except Exception:
            QtWidgets.QMessageBox.critical(self, tr("Invalid Values"), tr("Please enter valid numbers."))
            return None

class StartScreen(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()
        self.center_on_screen()
        self.game_window = None

    def _build_ui(self):
        # Clear any existing layout
        if self.layout():
            QtWidgets.QWidget().setLayout(self.layout())

        self.setWindowTitle(tr("Minesweeper - Start"))
        v = QtWidgets.QVBoxLayout(self)

        # --- Language selector row ---
        lang_row = QtWidgets.QHBoxLayout()
        lang_row.addStretch()
        self.lang_combo = QtWidgets.QComboBox()
        self.lang_combo.setMinimumWidth(160)
        for code, label in SUPPORTED_LANGS:
            self.lang_combo.addItem(label, code)
        # Set combo to current language
        current_codes = [c for c, _ in SUPPORTED_LANGS]
        if CURRENT_LANG in current_codes:
            self.lang_combo.setCurrentIndex(current_codes.index(CURRENT_LANG))
        self.lang_combo.currentIndexChanged.connect(self.on_lang_changed)
        lang_row.addWidget(self.lang_combo)
        v.addLayout(lang_row)

        # --- Title ---
        self.title_lbl = QtWidgets.QLabel(
            tr("<b>Minesweeper</b>\nChoose difficulty or custom"),
            alignment=QtCore.Qt.AlignCenter)
        v.addWidget(self.title_lbl)

        # --- Difficulty buttons ---
        self.btn_easy = QtWidgets.QPushButton(tr("Easy\n9×9 • 10"))
        self.btn_med  = QtWidgets.QPushButton(tr("Medium\n16×16 • 40"))
        self.btn_hard = QtWidgets.QPushButton(tr("Hard\n16×30 • 99"))
        self.btn_user = QtWidgets.QPushButton(tr("Custom"))
        for b in (self.btn_easy, self.btn_med, self.btn_hard, self.btn_user):
            b.setCheckable(True); b.setMinimumHeight(60)
        grid = QtWidgets.QGridLayout()
        grid.addWidget(self.btn_easy, 0, 0); grid.addWidget(self.btn_med, 0, 1)
        grid.addWidget(self.btn_hard, 1, 0); grid.addWidget(self.btn_user, 1, 1)
        v.addLayout(grid)

        self.settings = SettingsWidget(); v.addWidget(self.settings)

        h = QtWidgets.QHBoxLayout()
        self.start_btn = QtWidgets.QPushButton(tr("Start"))
        self.exit_btn  = QtWidgets.QPushButton(tr("Exit"))
        h.addStretch(); h.addWidget(self.start_btn); h.addWidget(self.exit_btn)
        v.addLayout(h)

        self.choice_group = [self.btn_easy, self.btn_med, self.btn_hard, self.btn_user]
        for b in self.choice_group: b.clicked.connect(self.choice_clicked)
        self.btn_easy.setChecked(True); self.update_visibility()
        self.start_btn.clicked.connect(self.on_start)
        self.exit_btn.clicked.connect(QtWidgets.qApp.quit)

    def on_lang_changed(self, index):
        code = self.lang_combo.itemData(index)
        set_language(code)
        self._rebuild_labels()

    def _rebuild_labels(self):
        """Refresh all translatable text after a language change."""
        self.setWindowTitle(tr("Minesweeper - Start"))
        self.title_lbl.setText(tr("<b>Minesweeper</b>\nChoose difficulty or custom"))
        self.btn_easy.setText(tr("Easy\n9×9 • 10"))
        self.btn_med.setText(tr("Medium\n16×16 • 40"))
        self.btn_hard.setText(tr("Hard\n16×30 • 99"))
        self.btn_user.setText(tr("Custom"))
        self.start_btn.setText(tr("Start"))
        self.exit_btn.setText(tr("Exit"))
    def center_on_screen(self):
        self.adjustSize()
        scr = QtWidgets.QApplication.primaryScreen().availableGeometry()
        geo = self.geometry()
        self.move(scr.left() + (scr.width() - geo.width())//2, scr.top() + (scr.height() - geo.height())//2)
    def choice_clicked(self):
        sender = self.sender()
        for b in self.choice_group:
            if b is not sender: b.setChecked(False)
        if not sender.isChecked(): sender.setChecked(True)
        self.update_visibility()
    def update_visibility(self):
        self.settings.setVisible(self.btn_user.isChecked()); self.adjustSize(); self.center_on_screen()
    def on_start(self):
        if self.btn_easy.isChecked(): rows, cols, mines = 9,9,10
        elif self.btn_med.isChecked(): rows, cols, mines = 16,16,40
        elif self.btn_hard.isChecked(): rows, cols, mines = 16,30,99
        else:
            vals = self.settings.values()
            if vals is None: return
            rows, cols, mines = vals
        self.hide()
        self.game_window = GameWindow(rows, cols, mines)
        self.game_window.start_with_initial_reveal()
        self.game_window.show()

class CellButton(QtWidgets.QPushButton):
    def __init__(self, r, c, cell_size):
        super().__init__()
        self.r = r; self.c = c; self.cell_size = cell_size
        self.setFixedSize(cell_size, cell_size)
        self.setIconSize(QtCore.QSize(max(8, cell_size-8), max(8, cell_size-8)))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setStyleSheet("QPushButton { padding:0px; margin:0px; border:1px solid #999; background:#eee; } QPushButton:disabled { background:#ddd; }")
        self.setContentsMargins(0,0,0,0)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setFlat(False)
        self.setText("")

class GameWindow(QtWidgets.QMainWindow):
    def __init__(self, rows, cols, mines):
        super().__init__()
        self.setWindowTitle(tr("Minesweeper"))
        self.rows = rows; self.cols = cols; self.mines = mines
        self.model = MinesModel(rows, cols, mines)
        self._flag_icon = None; self._mine_icon = None; self._cell_font_px = None; self._cell_size = None
        self._build_ui(); self.center_on_screen()
    def _build_ui(self):
        w = QtWidgets.QWidget(); self.setCentralWidget(w); v = QtWidgets.QVBoxLayout(w)
        top = QtWidgets.QHBoxLayout()
        self.restart_btn = QtWidgets.QPushButton(tr("New")); top.addWidget(self.restart_btn)
        self.restart_btn.clicked.connect(self.restart_game)
        self.info = QtWidgets.QLabel(""); top.addWidget(self.info); top.addStretch()
        self.time_lbl = QtWidgets.QLabel(tr("Time: %1s", 0)); top.addWidget(self.time_lbl)
        self.safe_btn = QtWidgets.QPushButton(tr("Safe Move")); top.addWidget(self.safe_btn)
        v.addLayout(top)
        self.grid_widget = QtWidgets.QWidget(); self.grid_layout = QtWidgets.QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(4); v.addWidget(self.grid_widget)
        font_digits = QtGui.QFont(); font_digits.setPointSize(12); font_digits.setBold(True)
        self.digit_font = font_digits
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        flag_path = os.path.join(base_dir, "flag.png")
        mine_path = os.path.join(base_dir, "mine.png")
        
        if os.path.exists(flag_path): self._flag_icon = QtGui.QIcon(flag_path)
        if os.path.exists(mine_path): self._mine_icon = QtGui.QIcon(mine_path)
        self._create_grid_buttons()
        self.timer = QtCore.QTimer(self); self.timer.timeout.connect(self._tick)
        self.safe_btn.clicked.connect(self.on_safe_step)
    def _create_grid_buttons(self):
        screen = QtWidgets.QApplication.primaryScreen()
        dpi = screen.logicalDotsPerInch() or 96
        scale = dpi / 96.0
        base = int(32 * UI_SCALE)
        cell_size = max(20, int(base * scale))
        font_px = max(10, int(cell_size * 0.8))
        self._cell_font_px = font_px; self._cell_size = cell_size
        # normalize icons for consistent visible size (smaller icons in App bundles)
        icon_margin = 12
        icon_size_px = max(8, cell_size - icon_margin)
        def _normalize_icon(icon, size_px):
            if not icon: return None
            pm = icon.pixmap(icon.actualSize(QtCore.QSize(size_px, size_px)))
            if pm.isNull(): pm = icon.pixmap(size_px, size_px)
            if not pm.isNull():
                pm = pm.scaled(size_px, size_px, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
                return QtGui.QIcon(pm)
            return icon
        self._flag_icon = _normalize_icon(self._flag_icon, icon_size_px)
        self._mine_icon = _normalize_icon(self._mine_icon, icon_size_px)
        for i in reversed(range(self.grid_layout.count())):
            w = self.grid_layout.itemAt(i).widget()
            if w: w.setParent(None)
        self.buttons = []
        for r in range(self.model.rows):
            row = []
            for c in range(self.model.cols):
                b = CellButton(r, c, cell_size=cell_size)
                # approx point size from pixel font_px (keeps number rendering stable)
                f = b.font(); f.setPointSize(max(8, int(font_px * 0.75))); f.setBold(True); b.setFont(f)
                b.clicked.connect(lambda checked, bb=b: self.on_left(bb))
                b.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                b.customContextMenuRequested.connect(lambda pos, bb=b: self.on_right(bb))
                b.setStyleSheet(b.styleSheet() + f" QPushButton {{ font-size: {font_px}px; font-weight: bold; }}")
                # set icon size explicitly to normalized icon size
                b.setIconSize(QtCore.QSize(icon_size_px, icon_size_px))
                row.append(b)
                self.grid_layout.addWidget(b, r, c)
            self.buttons.append(row)
        self.grid_layout.setHorizontalSpacing(max(2, int(4 * scale)))
        self.grid_layout.setVerticalSpacing(max(2, int(4 * scale)))
        self.adjustSize()
    def center_on_screen(self):
        scr = QtWidgets.QApplication.primaryScreen().availableGeometry()
        geo = self.geometry()
        self.move(scr.left() + (scr.width() - geo.width())//2, scr.top() + (scr.height() - geo.height())//2)
    def start_with_initial_reveal(self):
        attempts = min(50, self.model.rows * self.model.cols); best = (0,0)
        for _ in range(attempts):
            r = random.randrange(self.model.rows); c = random.randrange(self.model.cols)
            zero_found = False
            for __ in range(12):
                positions = [(rr,cc) for rr in range(self.model.rows) for cc in range(self.model.cols) if not (rr==r and cc==c)]
                mines_pos = random.sample(positions, self.model.mines)
                sample = [[False]*self.model.cols for _ in range(self.model.rows)]
                for mr,mc in mines_pos: sample[mr][mc] = True
                cnt = 0
                for dr in (-1,0,1):
                    for dc in (-1,0,1):
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < self.model.rows and 0 <= nc < self.model.cols:
                            if sample[nr][nc]: cnt += 1
                if cnt == 0: zero_found = True; break
            if zero_found: best = (r,c); break
            best = (r,c)
        sr, sc = best
        self.model.place_mines(sr, sc)
        self.model.started = True; self.model.start_time = time.time(); self.timer.start(1000)
        self.model.reveal(sr, sc)
        zeros = [(r,c) for r in range(self.model.rows) for c in range(self.model.cols)
                 if not self.model.grid[r][c].mine and self.model.grid[r][c].adj == 0 and not self.model.grid[r][c].revealed]
        if zeros:
            zr, zc = random.choice(zeros); self.model.reveal(zr, zc)
        self._update_all(); self.update_info()
    def restart_game(self):
        self.model = MinesModel(self.rows, self.cols, self.mines)
        self._create_grid_buttons(); self.start_with_initial_reveal()
    def _handle_game_over(self):
        if not self.model.game_over: return
        self.timer.stop()
        for rr in range(self.model.rows):
            for cc in range(self.model.cols):
                if self.model.grid[rr][cc].mine: self.model.grid[rr][cc].revealed = True
        self._update_all()
        if self.model.victory:
            elapsed_time = int(time.time() - self.model.start_time)
            QtWidgets.QMessageBox.information(self, tr("Victory"), tr("You won in %1 seconds.", elapsed_time))
        else:
            want = QtWidgets.QMessageBox.question(self, tr("Game Over"), tr("You lost. Start a new game?"))
            if want == QtWidgets.QMessageBox.Yes: self.restart_game()
    def on_left(self, btn):
        if self.model.game_over: return
        r, c = btn.r, btn.c
        if not self.model.started:
            self.model.place_mines(r, c); self.model.started = True; self.model.start_time = time.time(); self.timer.start(1000)
            self.model.reveal(r, c)
        else:
            self.model.reveal(r, c)
        self._update_all(); self.update_info(); self._handle_game_over()
    def on_right(self, btn):
        if self.model.game_over: return
        r, c = btn.r, btn.c
        cell = self.model.grid[r][c]
        if cell.revealed: return
        cell.flagged = not cell.flagged
        self._update_button(r, c); self.update_info()
    def _update_button(self, r, c):
        cell = self.model.grid[r][c]; btn = self.buttons[r][c]
        btn.setIcon(QtGui.QIcon()); btn.setText("")
        if cell.flagged and not cell.revealed:
            if self._flag_icon: btn.setIcon(self._flag_icon)
            else: btn.setText("🚩")
            btn.setEnabled(True); return
        if not cell.revealed:
            btn.setEnabled(True); return
        btn.setEnabled(False)
        if cell.mine:
            if self._mine_icon: btn.setIcon(self._mine_icon)
            else: btn.setText("*")
            return
        if cell.adj == 0:
            btn.setText(""); return
        btn.setText(str(cell.adj))
        color_map = {1:"#1f78b4",2:"#33a02c",3:"#e31a1c",4:"#08519c",5:"#7b241c",6:"#117a65",7:"#111111",8:"#6c757d"}
        color = color_map.get(cell.adj, "#000000")
        baseline = "QPushButton { padding:0px; margin:0px; border:1px solid #999; background:#eee; } QPushButton:disabled { background:#ddd; }"
        btn.setStyleSheet(baseline + f" QPushButton {{ font-size: {self._cell_font_px}px; font-weight: bold; color: {color}; background:#ddd; }}")
    def _update_all(self):
        for r in range(self.model.rows):
            for c in range(self.model.cols):
                self._update_button(r, c)
        self.grid_widget.repaint()
    def update_info(self):
        flags = sum(1 for r in range(self.model.rows) for c in range(self.model.cols) if self.model.grid[r][c].flagged)
        self.info.setText(tr("Mines: %1  Flags: %2", self.model.mines, flags))
    def on_safe_step(self):
        if self.model.game_over: return
        move_made = False; moved_was_flag = False
        step = self.model.simple_safe_step()
        if step:
            action, pos = step; r, c = pos
            if action == "flag": self.model.toggle_flag(r, c); moved_was_flag = True
            else: self.model.reveal(r, c)
            move_made = True
        if not move_made:
            safe = self.model.find_certain_safe_cells(max_frontier=24, max_enum=400000)
            if safe:
                r, c = next(iter(safe)); self.model.reveal(r, c); move_made = True; moved_was_flag = False
        if not move_made:
            try:
                path = self.model._mines_file
                if os.path.exists(path):
                    with open(path, "r", encoding="utf-8") as f: data = json.load(f)
                    mines = set(tuple(x) for x in data.get("mines", [])); chosen = None
                    for r in range(self.model.rows):
                        for c in range(self.model.cols):
                            cell = self.model.grid[r][c]
                            if cell.revealed or cell.flagged: continue
                            if (r, c) not in mines and not cell.mine:
                                chosen = (r, c); break
                        if chosen: break
                    if chosen: self.model.reveal(chosen[0], chosen[1]); move_made = True; moved_was_flag = False
            except Exception: pass
        if not move_made:
            QtWidgets.QMessageBox.information(self, tr("Safe Move"), tr("No safe move found."))
            return
        self._update_all(); self.update_info()
        if moved_was_flag and self.model.remaining == 0:
            self.model.game_over = True; self.model.victory = True
        self._handle_game_over()
    def _tick(self):
        if not self.model.started or not self.model.start_time: return
        elapsed = int(time.time() - self.model.start_time)
        self.time_lbl.setText(tr("Time: %1s", elapsed))
    def showEvent(self, event):
        super().showEvent(event); QtCore.QTimer.singleShot(0, self._finalize_size)
    def _finalize_size(self):
        self.adjustSize(); size = self.size(); size += QtCore.QSize(8, 8); self.setFixedSize(size)

def main():
    app = QtWidgets.QApplication(sys.argv)
    start = StartScreen(); start.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
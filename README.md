Opis projektu:
Stworzyłem prostą aplikację do monitorowania wydatków domowych, która pozwala użytkownikowi na dodawanie wydatków z podziałem na kategorie, kwotę oraz filtrowanie wydatków. Umożliwia również pokazanie zsumowanych wydatków w danym miesiącu. 

Zaimplementowane funkcje:
-Dodawanie oraz edycje wydatków
-Przypisywanie wydatków do kategorii
-filtrowanie przez kategorie
-Wyświetlanie ostatnich 5 wydatków
-Miesięczne podsumowanie

Technologie:
-Django 5.2.1
-Bootstrap
-PyCharm

Instalacja:
w terminalu PyCharm wpisać:
1)„python -m venv .venv”-> Utworznie wirtualnego środowiska
2)”pip install Django==5.2.1 Pillow” -> instalacja django oraz Pillow
3)”python manage.py migrate” ->Uruchomienie migracji
4)"python manage.py createsuperuser" -> Tu podajemy nazwe, email oraz 2x haslo [np. u mnie "admin", "a@a.pl","haslo123"
5)”python manage.py runserver” -> Uruchomienie serwera deweloperskiego
6)Zalogowanie w http://127.0.0.1:8000/admin/
7) Już można dodać nowy rekord http://127.0.0.1:8000/

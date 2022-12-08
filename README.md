Aby utworzyć nowy projekt:

1. Stwórz folder i otwórz go w PyCharm.
2. Pojawi się info o konieczności utworzenia interpretera Python - zrób to.

Git:

1. `git init`
2. Stwórz plik `.gitignore`
3. `git add .`
4. Aby usunąć plik po git add: `git rm --cache nazwa.pliku`
5. `git commit -m "message"`. Inna wersja `git commit -am "message"` - dodawanie do stage i commitowawnie
6. `git checkout -- nazwa.pliku`, usuwa zmiany jak po ctrl+z - Aby to zobaczyć trzeba otworzyć plik ponownie.
7. Podobnie działa komenda `git restore nazwa.pliku`
8. Jeśli plik został dodany do stage (`git add`) należy użyć komendy `git reset HEAD nazwa.pliku`, aby wyjąć go ze
   stage'a
   i następnie
   komendą `git checkout -- nazwa.pliku` można cofnąć ostatnie zmiany.

9. Po commit: `git tag -a M2 -m "whatsoever"` by nadać tag bieżącemu commitowi.
10. Następnie: `git checkout TAG` by przenieść się do commita. `git checkout master` by wrócić.
11. Po pracy przed powrotem do ostatniego commita usuń wszystkie zmiany z bieżącego: `git reset --hard`.
12. Aby stagować stare commity: `git tag -a TAG numer_hasha_commita -m "Tag Message"`
13. Tagi się nie pushują. Aby wysłać tagi na serwer wpisz: `git push origin --tags`
14. Usuwanie tagów lokalnie: `git tag -d <tagname>`.
15. Usuwanie tagów z serwera: `git push origin --delete <tagname>`

# CURD-Ticketing-System
Projekt prostej aplikacji bazodanowej mającej zapewnić 4 podstawowe funkcje wykorzystania baz danych (Create,Update,Read,Delete). Projekt powstaje w ramach przedmiotu "Programowanie" na Uniwersytecie Ekonomicznym we Wrocławiu


Projekt jest prostym przykładem aplikacji do sprzedaży biletów do wyimaginowanej sali wystawowej, lub czegoś w tym rodzaju.
Dostępne są proste mechaniki do tworzenia nowych biletów, sprawdzania ich statusu przez kod kreskowy i zarządzania nimi. Dodatkowo zawarty został raport sprzedaży dziennej i ogólnej, oraz panel zarządania wydarzeniami dostępnymi do sprzedaży.

(FYI otwieranie rekordu z tabeli następuje przez dwókilik na niego)

Generowanie biletu w formie pdf:
W rekordach z biletami, oraz przy tworzeniu nowego biletu, program utworzy plik w formacie pdf z jego numerem i odpowiadającym numerowi kodem kreskowym. W założeniu operator aplikacji przed wejściem skanuje kod kreskowy, lub wpisuje numer ręcznie aby sprawdzić autentyczność i oznaczyć skasowanie biletu w systemie.


config.json {
    Plik ustawień służący do ustawienia:
    - nazwy firmy (Używana w stopce biletów pdf)
    - dane do połączenia z serwerem baz danych takie jak:
        - login
        - hasło
        - adres serwera
        - nazwa bazy
}
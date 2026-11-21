# ContextCard

Karta wyniku sprawdzenia: na stronie WWW pod formularzem, a we wtyczce pod postem. Jedna karta na sprawdzenie, w niej jeden blok na każde twierdzenie.

- **Werdykty:** „Potwierdzone” (verified), „Wprowadzające w błąd” (contested), „Fałszywe” (scam: czerwień tylko tutaj), „Brak wystarczających dowodów” i „Nie podlega weryfikacji” (muted). Zawsze słowo, nigdy sam kolor.
- **Nagłówek zawsze** zawiera znak 14 px i słowo „Meritum”, żeby czytelnik nie wziął karty za treść platformy.
- **Wyjaśnienie** jest podpisane jako interpretacja przygotowana z pomocą AI i oddzielone od cytatów.
- **Źródła:** tytuł (link), wydawca, data publikacji, rodzaj i poziom (urzędowe lub pierwotne, wtórne) oraz dosłowny fragment. Werdykt rozstrzygający bez cytatu nie przejdzie walidacji kontraktu.
- **Siła podstawy** słowem („Mocna”, „Umiarkowana”, „Słaba”) i przesłanki: liczba niezależnych źródeł, źródła urzędowe, wiek najnowszego, zgodność.
- **Brak wystarczających dowodów** zawsze mówi, czego nie udało się ustalić. Stopka zawsze ma ograniczenia i informację o użyciu AI.
- **Stany, które nie są werdyktem** (doprecyzuj, poza zakresem, problem techniczny): ikona, tytuł i komunikat, bez plakietki i bez źródeł.
- **Rama** dopasowuje się do platformy (`data-host`): promień, krój treści, kształt przycisków. Kolory werdyktów i źródła się nie zmieniają.
- **Pojawienie:** rozwija się z wysokości 0 i unosi o 8 px w 0,5 s; przy ograniczonym ruchu bez animacji.
- **Kod:** `components/meritum/context-card.tsx` pokazuje jeszcze stare warianty `note`, `pending`, `scam` i jest do przerobienia według sekcji 6.4 `DESIGN_SYSTEM.md`.

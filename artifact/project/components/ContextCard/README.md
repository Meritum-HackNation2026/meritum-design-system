# ContextCard

Karta wstrzykiwana przez wtyczkę pod post: kontekst od społeczności, kontekst w ocenie albo ostrzeżenie o fałszywej reklamie.

- **Warianty:** `note` (plakietka Zweryfikowany, kolor verified), `pending` (W ocenie, contested), `scam` (Oszustwo, scam, obramowanie scam-border).
- **Nagłówek zawsze** zawiera znak 14 px, słowo „Meritum” i „Dlaczego to widzę?”. Bez niego czytelnik mógłby wziąć kartę za treść platformy.
- **Źródła są obowiązkowe:** co najmniej jedno, każde z domeną i typem (akt prawny, instytucja, media, encyklopedia). W kodzie `sources` to niepusta krotka.
- **Technika** nazywa sposób manipulacji i w podpowiedzi uczy, jak go rozpoznać.
- **Pasek zgody** (tylko notatki): dwa paski od środkowej osi, kreska progu 70%.
- **Rama** dopasowuje się do platformy (`data-host`): promień, krój treści, kształt przycisków. Kolory stanów i źródła się nie zmieniają.
- **Pojawienie:** rozwija się z wysokości 0 i unosi o 8 px w 0,5 s; przy ograniczonym ruchu bez animacji.
- **Kod:** `components/meritum/context-card.tsx` w repozytorium.

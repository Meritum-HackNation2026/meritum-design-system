# BotDefenseTelemetry

Poza zakresem konkursu MSZ: komponent został z wcześniejszej wersji produktu (wątek NASK i notatek społeczności) i nie jest używany w demo. Opis poniżej dotyczy tamtej wersji.

Karta Live Dashboard, która odpowiada na jedno pytanie: czy atak farmy botów zmienił wynik notatki.

- **Tytuł to odpowiedź** („Atak odparty, notatka bez zmian”) ze znakiem frontu: linia z trzema trójkątami w kolorze scam.
- **Wykres liniowy głosów na minutę:** chart-1 (atrament) to głosy liczone, chart-2 (czerwień) to odrzucone. Okno ataku ma tło scam-surface, początek pionową linię „front HH:MM”. Etykiety stoją przy liniach, bez legendy.
- **Suma, która się domyka:** „Oddane = liczone + odrzucone”, liczona z wierszy danych, nigdy wpisywana ręcznie.
- **Tabela odrzuconych kont:** czas i konto w kroju mono, konto przekreślone w kolorze scam, powód słowami. Nic nie znika: odrzucony głos zostaje w rejestrze.
- **Zakazane:** kafelki KPI z ikonami, różowe banery, wykres z gradientem, wymyślone liczby bez dopisku „dane symulowane”.
- **Kod:** `components/meritum/bot-defense-telemetry.tsx` (Recharts przez shadcn/ui Chart).

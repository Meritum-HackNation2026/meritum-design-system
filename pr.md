## Co i dlaczego

Dodaje klucze `moderation.answer.*` do `copy/pl.json`: teksty formularza, którym moderator odpowiada na sprawę z cytatami ze źródeł (US-MOD-07, F-39, ADR-06). Potrzebuje ich meritum-frontend#30. Test sprawdza, że komunikat o odrzuconym cytacie wskazuje numer cytatu i mówi, że odpowiedź nie poszła, a żaden tekst nie wspomina o kanale ani identyfikatorze.

## Dowód

`python3 -m unittest discover -s tests` przechodzi (99 testów, w tym nowy `test_copy_moderator_answer.py`).

## Ryzyko scalenia

Same nowe klucze, żaden istniejący się nie zmienia.

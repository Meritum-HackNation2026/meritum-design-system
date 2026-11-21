# AnalysisSteps

Pasek pod postem, który pokazuje, co dzieje się ze zgłoszeniem między „Wysłane” a opublikowaną notatką lub ostrzeżeniem.

- Trzy kroki, każdy w stanie: czeka (puste kółko), w toku (kręcące się kółko w kolorze verified), gotowe (pełne kółko z ptaszkiem).
- Kroki dla manipulacji: łączenie z podobnymi zgłoszeniami, zbieranie źródeł, szkic AI i ocena dwóch grup. Dla oszustwa: zapis dowodu, porównanie z kampaniami, sprawdzenie domeny na liście CERT Polska.
- W produkcji stany pochodzą ze statusu przepływu DBOS; w demo czas jest przyspieszony.
- **Kod:** `components/meritum/analysis-steps.tsx`.

# AnalysisSteps

Pasek, który pokazuje, co dzieje się ze sprawdzeniem między kliknięciem „Sprawdź” a kartą wyniku. Ten sam na stronie WWW i pod postem we wtyczce.

- Każdy krok jest w stanie: czeka (puste kółko), w toku (kręcące się kółko w kolorze verified), gotowe (pełne kółko z ptaszkiem), pominięty albo nieudany (słowo obok kółka).
- Kroki z kontraktu `AnalysisStep`: przyjęcie pytania, wyodrębnienie twierdzeń, szukanie w bazie źródeł, szukanie świeżych publikacji w zatwierdzonych serwisach (tylko gdy baza nie wystarczyła), porównanie źródeł z twierdzeniami, sprawdzenie dosłowności cytatów, odpowiedź prostym językiem, zapis przebiegu. Teksty w `copy/pl.json`, `analysis.steps`.
- Stany pochodzą ze statusu workflowu DBOS, nie z odliczania czasu.
- **Kod:** `components/meritum/analysis-steps.tsx` (do dostosowania do nowej listy kroków).

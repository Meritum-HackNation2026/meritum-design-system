"""Checks the texts of the context block of the result card: links and labels the card shows next to
the fact-checker's rating, the incident match and the sanctions note, so no screen hard-codes them.

Features: US-ZRD-08, US-ZRD-07, US-KOR-01, F-11, F-14, F-34, meritum-frontend#35
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))
CARD = (Path(__file__).parent.parent / "components" / "meritum" / "result-card.tsx").read_text(encoding="utf-8")


class ResultContextCopy(unittest.TestCase):
    """Texts of the context block (DESIGN_SYSTEM.md 6.4, Kontekst and Ostrzeżenia)."""

    def test_context_block_has_a_heading_that_keeps_it_apart_from_the_verdict(self) -> None:
        # Gherkin "ostrzeżenie o domenie": the warning stands apart from the verdict badge
        self.assertIn("werdykt", COPY["result"]["context_title"].lower())

    def test_incident_link_names_the_case_description(self) -> None:
        # Gherkin "dopasowanie z EUvsDisinfo": a link to the case description, never to the material
        self.assertIn("opis przypadku", COPY["result"]["incident_link"].lower())

    def test_sanctions_note_links_to_the_list_entry(self) -> None:
        # Gherkin "ostrzeżenie o sankcjach": a link to the entry on the list
        self.assertIn("wpis", COPY["source_warning"]["basis_link"].lower())

    def test_premise_meta_has_the_review_date(self) -> None:
        # Gherkin "ocena fact-checkera jako przesłanka": publisher, rating, title, date and link
        self.assertIn("{date}", COPY["result"]["claim_review_meta"])

    def test_result_card_takes_the_link_texts_from_copy(self) -> None:
        self.assertNotIn(">\n                podstawa", CARD)
        self.assertNotIn("opis przypadku", CARD)


if __name__ == "__main__":
    unittest.main()

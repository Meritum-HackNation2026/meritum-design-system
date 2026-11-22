"""Checks that a citation can carry its publisher's catalogue disclaimer.

Features: F-05, meritum-core#146, meritum-frontend#98
Run: python3 -m unittest discover -s tests
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).parent.parent
ITEM = (ROOT / "components" / "meritum" / "citation-item.tsx").read_text(encoding="utf-8")
CONTRACT = (ROOT / "contracts" / "meritum.ts").read_text(encoding="utf-8")


class CitationDisclaimer(unittest.TestCase):
    """`CatalogEntry.disclaimer` reaches the contract copy and `CitationItem` shows it under the source."""

    def test_contract_has_the_disclaimer(self) -> None:
        self.assertIn("disclaimer?: Disclaimer", CONTRACT)

    def test_citation_item_shows_it_quietly(self) -> None:
        self.assertIn("disclaimer?: string | null", ITEM)
        self.assertIn('{disclaimer && <p className="text-meta text-muted-foreground', ITEM)


if __name__ == "__main__":
    unittest.main()

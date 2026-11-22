"""Checks that the moderator queue fits a 360 px screen and sets dates in Archivo.

Features: US-MOD-05, F-25, meritum-frontend#98
Run: python3 -m unittest discover -s tests
"""

import unittest
from pathlib import Path

SOURCE = (Path(__file__).parent.parent / "components" / "meritum" / "moderation-queue.tsx").read_text(encoding="utf-8")


class QueueNarrow(unittest.TestCase):
    """Below `sm` each case is a stacked row, not a table wider than the screen."""

    def test_no_sideways_scroll_on_a_phone(self) -> None:
        self.assertNotIn('className="w-full min-w-[640px]', SOURCE)
        self.assertIn("sm:min-w-[640px]", SOURCE)
        self.assertIn("max-sm:sr-only", SOURCE)
        self.assertIn("max-sm:flex", SOURCE)

    def test_dates_use_tabular_figures_not_mono(self) -> None:
        dates = SOURCE[SOURCE.index("dateTime={c.last_seen}") - 300 : SOURCE.index("dateTime={c.last_seen}")]
        self.assertNotIn("font-mono", dates)
        self.assertIn("tabular-nums", dates)


if __name__ == "__main__":
    unittest.main()

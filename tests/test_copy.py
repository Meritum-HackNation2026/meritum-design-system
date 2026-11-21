"""Checks copy/pl.json: required screen keys and the tone of DESIGN_SYSTEM.md section 8.

Features: US-MOD-05, US-OBS-06, US-SPR-10, US-SPR-11, F-25, F-28, F-31, F-08, design-system#16
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from collections.abc import Iterator
from pathlib import Path

COPY = json.loads((Path(__file__).parent.parent / "copy" / "pl.json").read_text(encoding="utf-8"))
MAX_SENTENCE_WORDS = 20  # section 8: sentences up to ~20 words
EMOJI = re.compile("[\U0001f000-\U0001faff☀-➿]")
TECHNICAL_TERMS = ("token", "sesj", "http", "401", "403", "błąd", "kod")

REQUIRED_KEYS = (
    # citizen and staff sign-in / sign-out
    "account.signed_in_as",
    "account.signed_out",
    "account.sign_in_failed",
    "account.session_expired",
    "staff.sign_in.title",
    "staff.sign_in.lead",
    "staff.sign_in.no_access",
    "staff.sign_in.failed",
    "staff.sign_in.session_expired",
    "staff.sign_in.signed_in_as",
    "staff.sign_in.signed_out",
    # administration of staff accounts and high-risk topics
    "staff.admin.title",
    "staff.admin.accounts.title",
    "staff.admin.accounts.lead",
    "staff.admin.accounts.email",
    "staff.admin.accounts.role",
    "staff.admin.accounts.add",
    "staff.admin.accounts.added",
    "staff.admin.accounts.remove",
    "staff.admin.accounts.remove_confirm",
    "staff.admin.accounts.removed",
    "staff.admin.accounts.empty",
    "staff.admin.accounts.invalid_email",
    "staff.admin.accounts.duplicate",
    "staff.admin.topics.title",
    "staff.admin.topics.lead",
    "staff.admin.topics.name",
    "staff.admin.topics.keywords",
    "staff.admin.topics.keywords_hint",
    "staff.admin.topics.add",
    "staff.admin.topics.added",
    "staff.admin.topics.remove",
    "staff.admin.topics.removed",
    "staff.admin.topics.empty",
    # one-time jury link
    "jury.welcome",
    "jury.used",
    "jury.expired",
    "jury.read_only",
    # audio upload
    "form.audio_limits",
    "form.audio_transcription_warning",
    "errors.audio_too_large",
    "errors.audio_too_long",
    "status_hint.out_of_scope_audio_format",
    # extension popup: connection to the API (design-system#16)
    "extension.popup_connecting",
    "extension.popup_api_ok",
    "extension.popup_api_down",
)


def lookup(path: str) -> object:
    """Return the value at a dotted key path, or None when any part is missing."""
    node: object = COPY
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def texts(node: object, path: str = "") -> Iterator[tuple[str, object]]:
    """Yield (path, text) for every user-facing string, skipping $comment."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key != "$comment":
                yield from texts(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for i, value in enumerate(node):
            yield from texts(value, f"{path}[{i}]")
    else:
        yield path, node


class RequiredKeys(unittest.TestCase):
    def test_screen_keys_have_text(self) -> None:
        for key in REQUIRED_KEYS:
            with self.subTest(key=key):
                value = lookup(key)
                self.assertIsInstance(value, str, f"{key} is missing")
                self.assertTrue(value.strip(), f"{key} is empty")


class Tone(unittest.TestCase):
    def test_short_calm_sentences(self) -> None:
        for path, text in texts(COPY):
            with self.subTest(key=path):
                self.assertIsInstance(text, str)
                self.assertNotIn("!", text)
                self.assertIsNone(EMOJI.search(text))
                for sentence in re.split(r"(?<=[.?])\s+", text):
                    self.assertLessEqual(len(sentence.split()), MAX_SENTENCE_WORDS, sentence)

    def test_expired_jury_link_says_whom_to_write_without_technical_details(self) -> None:
        # Gherkin "link jury po terminie" from design-system#9
        # {contact} is the team address (jury.$comment): it is the "whom to write"
        self.assertIn("wygasł", str(lookup("jury.expired")))
        for key in ("jury.expired", "jury.used"):
            with self.subTest(key=key):
                text = lookup(key)
                self.assertIsInstance(text, str)
                self.assertIn("{contact}", text)
                for term in TECHNICAL_TERMS:
                    self.assertNotIn(term, text.lower())

    def test_popup_api_state_has_server_placeholder_and_no_jargon(self) -> None:
        # Gherkin from design-system#16; {api} is the API address or version
        self.assertIn("{api}", str(lookup("extension.popup_api_ok")))
        for key in ("extension.popup_connecting", "extension.popup_api_down"):
            with self.subTest(key=key):
                self.assertNotIn("API", str(lookup(key)))


if __name__ == "__main__":
    unittest.main()

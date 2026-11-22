"""Checks copy/pl.json: required screen keys and the tone of DESIGN_SYSTEM.md section 8.

Features: US-MOD-05, US-OBS-06, US-SPR-10, US-SPR-11, F-25, F-28, F-31, F-08, design-system#16, design-system#22, design-system#39, US-ZRD-12, F-29, US-SPR-01, US-BEZ-07, F-01, F-21, design-system#49, design-system#52
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
    "out_of_scope_code.audio",
    # extension popup: connection to the API (design-system#16)
    "extension.popup_connecting",
    "extension.popup_api_ok",
    "extension.popup_api_down",
    # extension popup: deleting the user's checks (design-system#22)
    "extension.popup_delete",
    "extension.popup_delete_confirm",
    "extension.popup_delete_yes",
    "extension.popup_delete_cancel",
    "extension.popup_deleted",
    "extension.popup_delete_failed",
    # check form: a link longer than the contract's url.maxLength (design-system#35)
    "errors.url_too_long",
    # Discord mock: author of the user's message, reply templates, claim plurals (design-system#39)
    "discord.user_author",
    # one embed with a link button, public option (meritum-backend#102)
    "discord.result_title",
    "discord.card_button",
    "discord.public_option",
    "discord.claim_undated",
    "discord.claim_no_strength",
    "discord.claim_undated_no_strength",
    "discord.claims.one",
    "discord.claims.few",
    "discord.claims.many",
    "discord.claims.other",
    # daily recording upload limit, apart from the per-minute one (design-system#43)
    "errors.rate_limited_daily",
    # result page when GET /api/v1/checks/{id} returns 404 (design-system#49)
    "errors.check_not_found",
    # HTTP 503 when moderator case save fails (design-system#52)
    "escalation.not_saved",
    # page „Jak działa Meritum” (meritum-frontend#20)
    "method.lead",
    "method.sources.title",
    "method.verdict.title",
    "method.team.title",
    "method.catalog.title",
    "method.catalog.lead",
    "method.catalog.columns.source",
    "method.catalog.columns.kind",
    "method.catalog.columns.license",
    "method.catalog.columns.qualified_because",
    "method.catalog.columns.exclusion_reason",
    "method.catalog.excluded_title",
    "method.catalog.excluded_lead",
    "method.catalog.unavailable",
    "method.metrics.title",
    "method.metrics.lead",
    "method.metrics.run_date",
    "method.metrics.reproduce",
    "method.metrics.no_run",
    "method.corrections.title",
    "method.report_error.title",
    "method.pilot.title",
    "method.metrics.names.macro_f1",
    "method.metrics.names.latency_median_s",
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


class MethodPage(unittest.TestCase):
    def test_every_text_section_has_paragraphs(self) -> None:
        # meritum-frontend#20 renders method.<section>.text as paragraphs
        for section in ("sources", "verdict", "team", "corrections", "report_error", "pilot"):
            with self.subTest(section=section):
                paragraphs = lookup(f"method.{section}.text")
                self.assertIsInstance(paragraphs, list)
                self.assertTrue(paragraphs)


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

    def test_daily_limit_text_does_not_promise_a_minute(self) -> None:
        # Gherkin "komunikat pasuje do przekroczonego limitu" from design-system#43
        self.assertIn("minut", str(lookup("errors.rate_limited")))
        self.assertNotIn("minut", str(lookup("errors.rate_limited_daily")))

    def test_popup_api_state_has_server_placeholder_and_no_jargon(self) -> None:
        # Gherkin from design-system#16; {api} is the API address or version
        self.assertIn("{api}", str(lookup("extension.popup_api_ok")))
        for key in ("extension.popup_connecting", "extension.popup_api_down"):
            with self.subTest(key=key):
                self.assertNotIn("API", str(lookup(key)))

    def test_discord_claim_plurals_and_templates_without_date_or_strength(self) -> None:
        # Gherkin "makieta Discorda bierze teksty z copy" from design-system#39;
        # plural keys are Intl.PluralRules("pl") categories
        for form, word in (("one", "twierdzenie"), ("few", "twierdzenia"), ("many", "twierdzeń"), ("other", "twierdzenia")):
            with self.subTest(form=form):
                self.assertEqual(lookup(f"discord.claims.{form}"), f"{{count}} {word}")
        self.assertIn("{claims}", str(lookup("discord.summary")))
        for key, absent in (
            ("discord.claim_undated", "{date}"),
            ("discord.claim_no_strength", "{strength}"),
            ("discord.claim_undated_no_strength", "{date}"),
            ("discord.claim_undated_no_strength", "{strength}"),
        ):
            with self.subTest(key=key, absent=absent):
                self.assertNotIn(absent, str(lookup(key)))

    def test_moderation_counts_have_polish_plurals(self) -> None:
        # Gherkin "odmiana liczby" from design-system#65; keys are Intl.PluralRules("pl") categories
        for key in ("moderation.similar", "moderation.askers"):
            forms = lookup(key)
            with self.subTest(key=key):
                self.assertIsInstance(forms, dict)
                for form in ("one", "few", "many", "other"):
                    self.assertIn("{count}", forms[form])
        self.assertEqual(lookup("moderation.askers.one"), "{count} osoba pytająca")
        self.assertEqual(lookup("moderation.similar.few"), "{count} podobne pytania")
        self.assertEqual(lookup("moderation.similar.many"), "{count} podobnych pytań")

    def test_moderation_queue_counts_all_questions_with_plural(self) -> None:
        # Gherkin "parafraza w jednej sprawie" from design-system#65: two questions show "2 podobne pytania"
        source = (Path(__file__).parent.parent / "components" / "meritum" / "moderation-queue.tsx").read_text(encoding="utf-8")
        self.assertNotIn("asked - 1", source)
        self.assertIn("plural(t.moderation.similar, asked)", source)
        # the panel in meritum-frontend picks moderation.askers forms with the same helper
        index = (Path(__file__).parent.parent / "components" / "meritum" / "index.ts").read_text(encoding="utf-8")
        self.assertRegex(index, r"export \{[^}]*\bplural\b[^}]*\} from \"\./copy\"")

    def test_discord_skin_in_platform_skins(self) -> None:
        tokens = (Path(__file__).parent.parent / "tokens" / "meritum.css").read_text(encoding="utf-8")
        self.assertIn('[data-host="discord"]', tokens)

    def test_unknown_check_page_is_not_technical_failure_hint(self) -> None:
        # Gherkin "nieznany adres sprawdzenia" from design-system#49
        text = lookup("errors.check_not_found")
        self.assertIsInstance(text, str)
        self.assertIn("To nie jest ocena treści", text)
        self.assertIn("Wklej", text)
        self.assertNotIn("Spróbuj za kilka minut", text)
        self.assertNotIn(str(lookup("status_hint.technical_failure")), text)

    def test_escalation_not_saved_says_retry_without_case_number(self) -> None:
        # Gherkin "nieudany zapis sprawy" from design-system#52
        text = lookup("escalation.not_saved")
        self.assertIsInstance(text, str)
        self.assertRegex(text.lower(), r"zapis")
        self.assertIn("Spróbuj", text)
        self.assertNotIn("{case}", text)
        self.assertNotRegex(text, r"#S-\d+")


if __name__ == "__main__":
    unittest.main()

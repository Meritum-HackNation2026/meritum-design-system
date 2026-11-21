"""Checks copy/privacy.json: channel privacy policies and the ADR-14 processor register.

Features: US-BEZ-06, US-BEZ-07, US-WDR-03, F-20, F-21
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

from test_copy import EMOJI, MAX_SENTENCE_WORDS, lookup, texts

PRIVACY = json.loads((Path(__file__).parent.parent / "copy" / "privacy.json").read_text(encoding="utf-8"))
POLICIES = PRIVACY["policies"]
PROCESSORS = {item["id"]: item for item in PRIVACY["processors"]["items"]}

CHANNELS = ("web", "discord", "extension", "sms")
POLICY_SECTIONS = ("title", "data", "purpose", "retention", "deletion", "telemetry", "ip_addresses", "processors_lead")
PROCESSOR_FIELDS = ("name", "region", "data", "purpose")
# every processor the issue (design-system#8) names from the ADR-14 register
REQUIRED_PROCESSORS = (
    "team_server",
    "gcp_europe_central2",
    "cloud_storage",
    "cloudflare",
    "cloudflare_workers_ai",
    "vertex_ai",
    "speech_to_text",
    "sensitive_data_protection",
    "vertex_ai_search",
    "searxng",
    "linkup",
    "model_armor",
    "vertex_ai_ranking",
    "crawl4ai",
    "firecrawl",
    "discord",
    "mcp_chat_apps",
    "sign_in",
    "moderator_notifications",
    "fact_check_tools",
    "github",
    "euvsdisinfo_mcp",
)
# AI Act art. 50 notice at first contact in every channel, plus the result card line
AI_NOTICE_KEYS = ("ai_notice.first_contact", "ai_notice.discord", "ai_notice.sms", "ai_notice.mcp", "result.ai_disclosure")
SMS_UCS2_CHARS = 70


def policy_text(channel: str) -> str:
    """Whole user-facing text of one channel's policy, lower-cased."""
    return " ".join(str(text) for _, text in texts(POLICIES[channel])).lower()


class Policies(unittest.TestCase):
    def test_every_channel_has_every_section(self) -> None:
        for channel in CHANNELS:
            for section in POLICY_SECTIONS:
                with self.subTest(channel=channel, section=section):
                    value = POLICIES[channel].get(section)
                    self.assertIsInstance(value, str)
                    self.assertTrue(value.strip())

    def test_telemetry_is_aggregate_and_ip_only_against_attacks(self) -> None:
        for channel in CHANNELS:
            with self.subTest(channel=channel):
                self.assertIn("zbiorcz", POLICIES[channel]["telemetry"])
                self.assertIn("atak", POLICIES[channel]["ip_addresses"])

    def test_policies_list_known_processors(self) -> None:
        for channel in CHANNELS:
            with self.subTest(channel=channel):
                listed = POLICIES[channel]["processors"]
                self.assertTrue(listed)
                self.assertLessEqual(set(listed), set(PROCESSORS))

    def test_discord_policy(self) -> None:
        # Gherkin "polityka kanału Discord" from design-system#8
        text = policy_text("discord")
        self.assertIn("nazwę i identyfikator użytkownika", text)
        self.assertIn("tylko po to, żeby odpowiedzieć i policzyć powtórzenia", text)
        self.assertIn("skrót z solą", text)
        self.assertIn("30 dni", POLICIES["discord"]["retention"])
        self.assertIn("nigdy nie trafiają do moderatorów", text)
        self.assertIn("/usun-moje-dane", POLICIES["discord"]["deletion"])
        self.assertIn("discord", POLICIES["discord"]["processors"])

    def test_sms_policy_states_fees_and_delete_keyword(self) -> None:
        text = policy_text("sms")
        self.assertIn("bezpłatna", text)
        self.assertIn("standardowe opłaty operatora", text)
        self.assertIn("USUN", POLICIES["sms"]["deletion"])
        self.assertIn("sms_gateway", POLICIES["sms"]["processors"])

    def test_extension_sends_only_after_click(self) -> None:
        self.assertIn("dopiero po kliknięciu", policy_text("extension"))


class Processors(unittest.TestCase):
    def test_register_covers_adr14(self) -> None:
        for processor in REQUIRED_PROCESSORS:
            with self.subTest(processor=processor):
                self.assertIn(processor, PROCESSORS)

    def test_every_entry_has_provider_region_data_purpose(self) -> None:
        for processor, item in PROCESSORS.items():
            for field in PROCESSOR_FIELDS:
                with self.subTest(processor=processor, field=field):
                    self.assertIsInstance(item.get(field), str)
                    self.assertTrue(item[field].strip())

    def test_columns_have_headers(self) -> None:
        for field in PROCESSOR_FIELDS:
            with self.subTest(field=field):
                self.assertTrue(PRIVACY["processors"]["columns"][field].strip())


class AiNotice(unittest.TestCase):
    def test_every_channel_has_ai_notice(self) -> None:
        for key in AI_NOTICE_KEYS:
            with self.subTest(key=key):
                value = lookup(key)
                self.assertIsInstance(value, str)
                self.assertIn("AI", value)

    def test_sms_notice_fits_one_ucs2_sms(self) -> None:
        self.assertLessEqual(len(str(lookup("ai_notice.sms"))), SMS_UCS2_CHARS)


class Tone(unittest.TestCase):
    def test_short_calm_sentences(self) -> None:
        for path, text in texts(PRIVACY):
            with self.subTest(key=path):
                self.assertIsInstance(text, str)
                self.assertNotIn("!", text)
                self.assertIsNone(EMOJI.search(text))
                for sentence in re.split(r"(?<=[.?])\s+", text):
                    self.assertLessEqual(len(sentence.split()), MAX_SENTENCE_WORDS, sentence)


if __name__ == "__main__":
    unittest.main()

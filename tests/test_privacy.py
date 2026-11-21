"""Checks copy/privacy.json: channel privacy policies and the ADR-14 processor register.

Features: US-BEZ-05, US-BEZ-06, US-BEZ-07, US-WTY-09, US-WDR-03, F-20, F-21, ADR-13, ADR-14
Run: python3 -m unittest discover -s tests
"""

import json
import re
import unittest
from pathlib import Path

from test_copy import EMOJI, MAX_SENTENCE_WORDS, lookup, texts

PRIVACY = json.loads((Path(__file__).parent.parent / "copy" / "privacy.json").read_text(encoding="utf-8"))
POLICIES = PRIVACY["policies"]
ACTIVE = {item["id"]: item for item in PRIVACY["processors"]["items"]}
PLANNED = {item["id"]: item for item in PRIVACY["processors"]["planned_items"]}
PROCESSORS = ACTIVE | PLANNED

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
    "openrouter",
    "anthropic",
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
    "sms_gateway",
    "sign_in",
    "moderator_notifications",
    "fact_check_tools",
    "github",
    "euvsdisinfo_mcp",
)
# AI Act art. 50 notice at first contact in every channel, plus the result card line
AI_NOTICE_KEYS = ("ai_notice.first_contact", "ai_notice.discord", "ai_notice.sms", "ai_notice.mcp", "result.ai_disclosure")
SMS_UCS2_CHARS = 70
# team answers on PR #20: candidates and the SMS gateway are planned, not active
PLANNED_PROCESSORS = ("sms_gateway", "cloudflare_workers_ai", "vertex_ai_ranking")


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
                self.assertLessEqual(set(listed), set(ACTIVE))
                self.assertLessEqual(set(POLICIES[channel].get("planned_processors", [])), set(PLANNED))

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
        self.assertIn("sms_gateway", POLICIES["sms"]["planned_processors"])

    def test_controller_and_contact(self) -> None:
        controller = PRIVACY["controller"]
        self.assertIn("Zespół Meritum", controller["name"])
        self.assertIn("HackNation 2026", controller["name"])
        self.assertIn("nie ma partnerstwa z MSZ", controller["no_partnership"])
        self.assertIn("podmiot wdrażający", controller["deployment"])
        self.assertIn("cyprian@gburek.dev", controller["contact"])
        self.assertNotIn("{", controller["contact"])

    def test_ip_logs_kept_14_days_and_rate_limits_in_memory(self) -> None:
        for channel in CHANNELS:
            with self.subTest(channel=channel):
                text = POLICIES[channel]["ip_addresses"]
                self.assertIn("14 dniach", text)
                self.assertIn("bez trwałego zapisu", text)
                self.assertNotIn("pamięci", text)
                self.assertIn("Cloudflare", text)

    def test_web_history_30_days_account_until_deleted(self) -> None:
        retention = POLICIES["web"]["retention"]
        self.assertIn("30 dniach", retention)
        self.assertIn("powiadomienia", retention.lower())
        self.assertIn("do kliknięcia „Usuń konto”", retention)

    def test_web_sign_in_names_oauth_scopes_and_account_data(self) -> None:
        # Gherkin "polityka strony opisuje logowanie kontem Google albo Microsoft" from design-system#28
        text = " ".join(str(t) for _, t in texts(POLICIES["web"]["sign_in"])).lower()
        for phrase in ("dobrowolne", "openid, email i profile", "imię i nazwisko", "adres e-mail", "identyfikator konta",
                       "nie dostajemy hasła", "poczty, plików czy kontaktów", "sesji logowania", "historii",
                       "ról", "nie używamy do reklam", "dopóki masz konto",
                       "cofnąć w ustawieniach konta google albo microsoft"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_account_data_is_the_same_everywhere(self) -> None:
        for where, text in (
            ("processors.sign_in", ACTIVE["sign_in"]["data"]),
            ("policies.web.data", POLICIES["web"]["data"]),
            ("policies.web.sign_in.scopes", POLICIES["web"]["sign_in"]["scopes"]),
            ("account.stored", str(lookup("account.stored"))),
        ):
            with self.subTest(where=where):
                self.assertIn("imię i nazwisko", text.lower())
                self.assertIn("adres e-mail", text)
                self.assertIn("identyfikator", text)

    def test_extension_deletes_from_the_popup(self) -> None:
        # Gherkin "polityka wtyczki opisuje usuwanie z okienka" from design-system#31 (meritum-extension#24)
        deletion = POLICIES["extension"]["deletion"]
        self.assertIn("„Usuń moje sprawdzenia”", deletion)
        self.assertIn("nowy losowy identyfikator", deletion)
        self.assertIn("losowy identyfikator sesji, zapisany tylko w przeglądarce", POLICIES["extension"]["data"])

    def test_every_purpose_counts_repetitions(self) -> None:
        # Gherkin "cel przetwarzania obejmuje liczenie powtórzeń w każdym kanale" from design-system#31
        for channel in CHANNELS:
            with self.subTest(channel=channel):
                self.assertIn("powtórze", POLICIES[channel]["purpose"])

    def test_mcp_clients_are_separate_controllers(self) -> None:
        self.assertNotIn("mcp_chat_apps", PROCESSORS)
        note = PRIVACY["external_mcp_clients"]
        self.assertIn("odrębni administratorzy", note["title"].lower())
        self.assertIn("nie mamy na to wpływu", note["text"].lower())

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

    def test_candidates_and_sms_gateway_are_planned(self) -> None:
        self.assertEqual(set(PLANNED), set(PLANNED_PROCESSORS))
        self.assertTrue(PRIVACY["processors"]["planned_lead"].strip())
        for channel in CHANNELS:
            with self.subTest(channel=channel):
                self.assertTrue(POLICIES[channel]["planned_processors_lead"].strip())

    def test_conservative_regions(self) -> None:
        for processor in ("fact_check_tools", "moderator_notifications"):
            with self.subTest(processor=processor):
                self.assertIn("poza gwarancją EOG", ACTIVE[processor]["region"])
        # design-system#26: the app stays on the team server in Poland; only files, embeddings, transcription and masking are in GCP
        self.assertEqual("Serwer zespołu w Polsce", ACTIVE["team_server"]["region"])
        self.assertNotIn("migracj", ACTIVE["team_server"]["purpose"])
        for processor in ("cloud_storage", "vertex_ai_embeddings"):
            with self.subTest(processor=processor):
                self.assertEqual("GCP europe-central2 (Warszawa)", ACTIVE[processor]["region"])
        self.assertNotIn("API", ACTIVE["gcp_europe_central2"]["data"])
        self.assertIn("bez danych osobowych", ACTIVE["jasnopis"]["data"])

    def test_language_model_runs_outside_eea_without_retention(self) -> None:
        # design-system#56: Claude Haiku 5.5 through OpenRouter, not Vertex AI in the EU
        self.assertNotIn("vertex_ai", ACTIVE)
        for processor in ("openrouter", "anthropic"):
            with self.subTest(processor=processor):
                entry = ACTIVE[processor]
                self.assertIn("poza eog", entry["region"].lower())
                self.assertIn("podstaw", entry["region"].lower())
                self.assertIn("zamaskowane twierdzenia", entry["data"].lower())
                self.assertIn("ZDR", entry["data"])
                for channel in CHANNELS:
                    self.assertIn(processor, POLICIES[channel]["processors"])
        self.assertIn("standardowych klauzul umownych", ACTIVE["openrouter"]["region"])
        # Google Vertex keeps flagged prompts up to 90 days: with Safety Retention off only Bedrock serves Haiku
        self.assertNotIn("Google", ACTIVE["anthropic"]["region"] + ACTIVE["anthropic"]["name"] + ACTIVE["anthropic"]["data"])
        self.assertIn("OpenRouter", " ".join(lookup("method.team.text")))

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

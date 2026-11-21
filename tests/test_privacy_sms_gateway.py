"""SMS Gateway register and sms.reply copy (design-system#48).

Features: US-BEZ-07, US-WTY-07, F-21, F-32, ADR-14
Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

from test_copy import lookup

PRIVACY = json.loads((Path(__file__).parent.parent / "copy" / "privacy.json").read_text(encoding="utf-8"))
ACTIVE = {item["id"]: item for item in PRIVACY["processors"]["items"]}
PLANNED_IDS = {item["id"] for item in PRIVACY["processors"]["planned_items"]}
SMS_POLICY = PRIVACY["policies"]["sms"]

SMS_GATE_NAME = "SMS Gateway for Android, sms-gate.app (tryb Cloud, przekaźnik wiadomości)"
SMS_GATE_DATA = "Numer telefonu, treść SMS-a i odpowiedź"
SMS_GATE_PURPOSE = "Kanał SMS"


class SmsGatewayRegister(unittest.TestCase):
    def test_register_lists_sms_gate_app_as_active_gateway(self) -> None:
        # Gherkin: obywatel czyta listę podmiotów przetwarzających i widzi sms-gate.app (tryb Cloud)
        entry = ACTIVE["sms_gateway"]
        self.assertIn("sms-gate.app", entry["name"])
        self.assertIn("tryb Cloud", entry["name"])
        self.assertEqual(SMS_GATE_NAME, entry["name"])
        self.assertEqual(SMS_GATE_DATA, entry["data"])
        self.assertEqual(SMS_GATE_PURPOSE, entry["purpose"])
        self.assertNotIn("sms_gateway", PLANNED_IDS)

    def test_sms_policy_lists_gateway_among_processors_not_planned(self) -> None:
        self.assertIn("sms_gateway", SMS_POLICY["processors"])
        self.assertNotIn("sms_gateway", SMS_POLICY.get("planned_processors", []))

    def test_team_server_mentions_prepaid_phone_gateway(self) -> None:
        team = ACTIVE["team_server"]["data"].lower()
        self.assertIn("prepaid", team)
        self.assertIn("sms gateway", team)


class SmsReplyCopy(unittest.TestCase):
    def test_reply_has_no_link_placeholder(self) -> None:
        # backend#29: operators filter links in SMS; reply carries verdict only
        reply = str(lookup("sms.reply"))
        self.assertNotIn("{link}", reply)
        self.assertIn("{verdict}", reply)


if __name__ == "__main__":
    unittest.main()
import json
import unittest
from pathlib import Path
from src.domain import load_domain

FIXTURE = Path("fixtures/domain.json")


class DomainTest(unittest.TestCase):
    def test_fixture_matches_domain(self):
        value = load_domain(FIXTURE)
        self.assertEqual(value["domain"], "olive-variety-trial")
        self.assertGreaterEqual(value["version"], 2)
        self.assertGreaterEqual(len(value["facts"]), 4)
        self.assertGreaterEqual(len(value["constraints"]), 4)

    def test_fixture_satisfies_schema(self):
        schema = json.loads(Path("contracts/domain.schema.json").read_text(encoding="utf-8"))
        value = json.loads(FIXTURE.read_text(encoding="utf-8"))
        allowed = set(schema["properties"])
        self.assertTrue(allowed.issuperset(value), "示例资料含有 schema 未声明的字段")
        for field in schema["required"]:
            self.assertIn(field, value)

    def test_recommendation_requires_cycles_plots_and_uncertainty(self):
        text = " ".join(load_domain(FIXTURE)["facts"])
        for keyword in ("三年周期", "地块", "不确定性"):
            self.assertIn(keyword, text)

    def test_comparability_breaks_and_raw_records_are_constrained(self):
        text = " ".join(load_domain(FIXTURE)["constraints"])
        for keyword in ("嫁接", "补种", "原始记录", "重现"):
            self.assertIn(keyword, text)


if __name__ == "__main__":
    unittest.main()

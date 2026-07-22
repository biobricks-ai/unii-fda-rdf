import json
from pathlib import Path
R=Path(__file__).parents[1]
def test_bounded_vocab_and_coverage():
 c=json.loads((R/'health/source-coverage.json').read_text());o=json.loads((R/'health/ontology-policy.json').read_text());assert min(c['thresholds'].values())>=.99;assert o['allowed_classes']==[] and len(o['allowed_predicates'])==10

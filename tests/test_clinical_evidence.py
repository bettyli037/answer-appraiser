"""Test Clinical Evidence function."""
import logging

from app.clinical_evidence.compute_clinical_evidence import compute_clinical_evidence
from tests.clinical_response import response

logger = logging.getLogger(__name__)


def test_clinical_evidence():
    """Test that the clinical evidence function works."""
    score = compute_clinical_evidence(
        response["results"][0],
        response,
        logger,
        {
            "UMLS:C0021641_MONDO:0005015": [
                {
                    "log_odds_ratio": 1.5,
                    "total_sample_size": 100,
                },
                {
                    "log_odds_ratio": 0.2,
                    "total_sample_size": 10000,
                },
            ]
        },
    )
    assert score == 0.2128712871287129

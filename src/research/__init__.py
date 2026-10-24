"""
IncuBrix Analytic Engine: Phase 1 Product Research and Question Discovery
"""

from .product_observations import get_product_observations, export_product_observations
from .opportunity_analysis import get_growth_opportunities, export_growth_opportunities
from .collect_questions import get_verified_questions, get_source_register, export_questions_csv, export_source_register_csv
from .deduplicate_questions import deduplicate_dataset, normalize_question_text
from .validate_questions import validate_questions_dataframe, generate_validation_report

__all__ = [
    "get_product_observations",
    "export_product_observations",
    "get_growth_opportunities",
    "export_growth_opportunities",
    "get_verified_questions",
    "get_source_register",
    "export_questions_csv",
    "export_source_register_csv",
    "deduplicate_dataset",
    "normalize_question_text",
    "validate_questions_dataframe",
    "generate_validation_report",
]

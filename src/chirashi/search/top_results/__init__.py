"""Search top results GAPIClient."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from good_ass_pydantic_integrator import GAPIClient

from chirashi.constants import FILES_PATH
from chirashi.search.top_results.models import (
    SearchTopResults as SearchTopResultsModel,
)

if TYPE_CHECKING:
    from pathlib import Path


class SearchTopResults(GAPIClient[SearchTopResultsModel]):
    """GAPIClient for search top results items."""

    _response_model = SearchTopResultsModel

    @override
    @classmethod
    def json_files_folder(cls) -> Path:
        folder_name = cls._to_folder_name(cls._get_model_name())
        return FILES_PATH / folder_name

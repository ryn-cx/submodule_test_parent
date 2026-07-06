"""Search series GAPIClient."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from good_ass_pydantic_integrator import GAPIClient

from chirashi.constants import FILES_PATH
from chirashi.search.series.models import SearchSeries as SearchSeriesModel

if TYPE_CHECKING:
    from pathlib import Path


class SearchSeries(GAPIClient[SearchSeriesModel]):
    """GAPIClient for search series items."""

    _response_model = SearchSeriesModel

    @override
    @classmethod
    def json_files_folder(cls) -> Path:
        folder_name = cls._to_folder_name(cls._get_model_name())
        return FILES_PATH / folder_name

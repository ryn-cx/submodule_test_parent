"""Search music GAPIClient."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from good_ass_pydantic_integrator import GAPIClient

from chirashi.constants import FILES_PATH
from chirashi.search.music.models import SearchMusic as SearchMusicModel

if TYPE_CHECKING:
    from pathlib import Path


class SearchMusic(GAPIClient[SearchMusicModel]):
    """GAPIClient for search music items."""

    _response_model = SearchMusicModel

    @override
    @classmethod
    def json_files_folder(cls) -> Path:
        folder_name = cls._to_folder_name(cls._get_model_name())
        return FILES_PATH / folder_name

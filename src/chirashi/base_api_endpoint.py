"""Base API endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from good_ass_pydantic_integrator import GAPIClient
from pydantic import BaseModel

from chirashi.constants import FILES_PATH

if TYPE_CHECKING:
    from pathlib import Path

    from chirashi import Chirashi


class BaseEndpoint[T: BaseModel](GAPIClient[T]):
    """Base class for API endpoints."""

    def __init__(self, client: Chirashi) -> None:
        """Initialize the endpoint with the Chirashi client."""
        self._client = client

    @override
    @classmethod
    def json_files_folder(cls) -> Path:
        folder_name = cls._to_folder_name(cls._get_model_name())
        return FILES_PATH / folder_name

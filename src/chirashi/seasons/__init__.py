"""Seasons API endpoint."""

from __future__ import annotations

from typing import Any

from chirashi.base_api_endpoint import BaseEndpoint
from chirashi.seasons.models import Seasons as SeasonsModel


class Seasons(BaseEndpoint[SeasonsModel]):
    """Provides methods to download, parse, and retrieve seasons data."""

    _response_model = SeasonsModel

    def download(
        self,
        series_id: str,
        *,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        """Downloads seasons data for a given series ID.

        Args:
            series_id: The ID of the series to get seasons for.
            locale: The locale for the request.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        # This referer is valid, but it's not the ideal one because the real one would
        # include the series slug at the end as well.
        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}
        endpoint = f"content/v2/cms/series/{series_id}/seasons"
        params: dict[str, str | None] = {"locale": locale, "force_locale": None}
        return self._client.download(
            endpoint=endpoint,
            params=params,
            headers=headers,
        )

    def get(self, series_id: str, *, locale: str = "en-US") -> SeasonsModel:
        """Downloads and parses seasons data for a given series ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            series_id: The ID of the series to get seasons for.
            locale: The locale for the request.

        Returns:
            A Seasons model containing the parsed data.
        """
        data = self.download(series_id, locale=locale)
        return self.parse(data)

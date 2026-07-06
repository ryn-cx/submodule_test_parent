"""Episodes API endpoint."""

from __future__ import annotations

from typing import Any

from chirashi.base_api_endpoint import BaseEndpoint
from chirashi.episodes.models import Episodes as EpisodesModel


class Episodes(BaseEndpoint[EpisodesModel]):
    """Provides methods to download, parse, and retrieve episodes data."""

    _response_model = EpisodesModel

    def download(
        self,
        series_id: str,
        *,
        locale: str = "en-US",
    ) -> dict[str, Any]:
        """Downloads episodes data for a given season ID.

        Args:
            series_id: The season ID to get episodes for.
            locale: The locale for the request.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        # This referer is valid, but it's not the ideal one because the real one would
        # include the series slug at the end as well.
        headers = {"referer": f"https://www.crunchyroll.com/series/{series_id}"}
        endpoint = f"content/v2/cms/seasons/{series_id}/episodes"
        params = {"locale": locale}
        return self._client.download(
            endpoint=endpoint,
            params=params,
            headers=headers,
        )

    def get(self, series_id: str, *, locale: str = "en-US") -> EpisodesModel:
        """Downloads and parses episodes data for a given season ID.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            series_id: The season ID to get episodes for.
            locale: The locale for the request.

        Returns:
            An Episodes model containing the parsed data.
        """
        data = self.download(series_id, locale=locale)
        return self.parse(data)

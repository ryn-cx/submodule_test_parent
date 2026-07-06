"""Search API endpoint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from good_ass_pydantic_integrator import GAPIClient
from pydantic import BaseModel

from chirashi.base_api_endpoint import BaseEndpoint
from chirashi.search.episodes import SearchEpisode
from chirashi.search.models import Search as SearchModel
from chirashi.search.music import SearchMusic
from chirashi.search.series import SearchSeries
from chirashi.search.top_results import SearchTopResults

if TYPE_CHECKING:
    from chirashi.search.episodes.models import SearchEpisodeItem
    from chirashi.search.music.models import SearchMusicItem
    from chirashi.search.series.models import SearchSery
    from chirashi.search.top_results.models import SearchTopResult


class Search(BaseEndpoint[SearchModel]):
    """Provides methods to download, parse, and retrieve search data."""

    _response_model = SearchModel

    def download(  # noqa: PLR0913
        self,
        query: str,
        *,
        n: int = 6,
        type: str = "music,series,episode,top_results",  # noqa: A002
        ratings: str = "true",
        preferred_audio_language: str = "ja-JP",
        locale: str = "en-US",
    ) -> dict[str, Any]:
        """Downloads search data for a given query.

        Args:
            query: The search query string.
            n: The number of results to return.
            type: Comma-separated content types to search.
            ratings: Whether to include ratings.
            preferred_audio_language: The preferred audio language.
            locale: The locale for the request.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        params: dict[str, str | int] = {
            "q": query,
            "n": n,
            "type": type,
            "ratings": ratings,
            "preferred_audio_language": preferred_audio_language,
            "locale": locale,
        }

        headers = {"referer": "https://www.crunchyroll.com/search"}

        return self._client.download(
            "content/v2/discover/search",
            params,
            headers,
        )

    def get(  # noqa: PLR0913
        self,
        query: str,
        *,
        n: int = 6,
        type: str = "music,series,episode,top_results",  # noqa: A002
        ratings: str = "true",
        preferred_audio_language: str = "ja-JP",
        locale: str = "en-US",
    ) -> SearchModel:
        """Downloads and parses search data for a given query.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            query: The search query string.
            n: The number of results to return.
            type: Comma-separated content types to search.
            ratings: Whether to include ratings.
            preferred_audio_language: The preferred audio language.
            locale: The locale for the request.

        Returns:
            A Search model containing the parsed data.
        """
        data = self.download(
            query,
            n=n,
            type=type,
            ratings=ratings,
            preferred_audio_language=preferred_audio_language,
            locale=locale,
        )
        return self.parse(data)

    @staticmethod
    def _extract_type[T: BaseModel](
        input_data: SearchModel,
        content_type: str,
        client: type[GAPIClient[T]],
    ) -> T:
        """Extract items matching a content type from search results."""
        for datum in input_data.data:
            if datum.type == content_type:
                return client.parse(GAPIClient.dump_response(datum.items))
        return client.parse([])

    @staticmethod
    def extract_music(input_data: SearchModel) -> list[SearchMusicItem]:
        """Extract music items from search results."""
        return Search._extract_type(input_data, "music", SearchMusic).root

    @staticmethod
    def extract_series(input_data: SearchModel) -> list[SearchSery]:
        """Extract series items from search results."""
        return Search._extract_type(input_data, "series", SearchSeries).root

    @staticmethod
    def extract_episodes(input_data: SearchModel) -> list[SearchEpisodeItem]:
        """Extract episode items from search results."""
        return Search._extract_type(input_data, "episode", SearchEpisode).root

    @staticmethod
    def extract_top_results(
        input_data: SearchModel,
    ) -> list[SearchTopResult]:
        """Extract top results items from search results."""
        return Search._extract_type(
            input_data,
            "top_results",
            SearchTopResults,
        ).root

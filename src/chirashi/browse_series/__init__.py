"""Browse series API endpoint."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any

from good_ass_pydantic_integrator import CustomSerializer, ReplacementType

from chirashi.base_api_endpoint import BaseEndpoint


class _RawDatetime(datetime):
    """A datetime that remembers its exact source string.

    The API encodes the same instant inconsistently (``...:33Z`` in some
    responses, ``...:33.000Z`` in others). A plain datetime loses that
    distinction, so dumps can't be byte-exact. Stashing the original string lets
    the serializer reproduce it while the value still behaves as a datetime.
    """

    raw: str


def _parse_last_public(value: object) -> object:
    """Parse ``last_public`` into a datetime that retains its source string."""
    if isinstance(value, _RawDatetime) or not isinstance(value, str):
        return value
    parsed = datetime.fromisoformat(value)
    result = _RawDatetime(
        parsed.year,
        parsed.month,
        parsed.day,
        parsed.hour,
        parsed.minute,
        parsed.second,
        parsed.microsecond,
        parsed.tzinfo,
    )
    result.raw = value
    return result


from chirashi.browse_series.models import (
    BrowseSeries as BrowseSeriesModel,
)

if TYPE_CHECKING:
    from chirashi.browse_series.models import Datum


class BrowseSeries(BaseEndpoint[BrowseSeriesModel]):
    """Provides methods to download, parse, and retrieve browse series data."""

    _response_model = BrowseSeriesModel

    @classmethod
    def _replacement_types(cls) -> list[ReplacementType]:
        return [
            ReplacementType(
                class_name="Datum",
                field_name="last_public",
                new_type="Annotated[AwareDatetime, PlainValidator(_parse_last_public)]",
            ),
        ]

    @classmethod
    def _custom_serializers(cls) -> list[CustomSerializer]:
        return [
            CustomSerializer(
                field_name="last_public",
                serializer_code="return value.raw",
                output_type="str",
                class_name="Datum",
            ),
        ]

    @classmethod
    def _additional_imports(cls) -> list[str]:
        return [
            "from typing import Annotated",
            "from pydantic import AwareDatetime, PlainValidator",
            "from chirashi.browse_series import _parse_last_public",
        ]

    def download(
        self,
        *,
        start: int | None = None,
        n: int = 36,
        sort_by: str = "newly_added",
        ratings: str = "true",
        locale: str = "en-US",
    ) -> dict[str, Any]:
        """Downloads browse series data.

        Args:
            start: The starting index for pagination.
            n: The number of results per page.
            sort_by: The sort order.
            ratings: Whether to include ratings.
            locale: The locale for the request.

        Returns:
            The raw JSON response as a dict, suitable for passing to ``parse()``.
        """
        params: dict[str, str | int] = {
            "n": n,
            "sort_by": sort_by,
            "ratings": ratings,
            "locale": locale,
        }

        if start is not None:
            params["start"] = start

        headers = {"referer": "https://www.crunchyroll.com/videos/new"}

        return self._client.download(
            "content/v2/discover/browse",
            params,
            headers,
        )

    def get(
        self,
        *,
        start: int | None = None,
        n: int = 36,
        sort_by: str = "newly_added",
        ratings: str = "true",
        locale: str = "en-US",
    ) -> BrowseSeriesModel:
        """Downloads and parses browse series data.

        Convenience method that calls ``download()`` then ``parse()``.

        Args:
            start: The starting index for pagination.
            n: The number of results per page.
            sort_by: The sort order.
            ratings: Whether to include ratings.
            locale: The locale for the request.

        Returns:
            A BrowseSeries model containing the parsed data.
        """
        data = self.download(
            n=n,
            sort_by=sort_by,
            locale=locale,
            start=start,
            ratings=ratings,
        )
        return self.parse(data)

    def get_since_datetime(
        self,
        end_datetime: datetime | None = None,
        *,
        n: int = 36,
        locale: str = "en-US",
        sort_by: str = "newly_added",
        ratings: str = "true",
    ) -> list[BrowseSeriesModel]:
        """Gets all browse pages until end_date is reached (inclusive).

        Args:
            n: The number of results per page.
            locale: The locale for the request.
            sort_by: The sort order.
            ratings: Whether to include ratings.
            end_datetime: Stop when reaching this datetime.

        Returns:
            List of BrowseSeries pages.
        """
        start = 0
        all_data: list[BrowseSeriesModel] = []
        end_datetime = end_datetime or datetime.now().astimezone()

        while True:
            result = self.get(
                n=n,
                locale=locale,
                start=start,
                sort_by=sort_by,
                ratings=ratings,
            )

            all_data.append(result)

            if result.data[-1].last_public < end_datetime or len(result.data) == 0:
                return all_data

            start += n

    def extract_entries(
        self,
        input_data: BrowseSeriesModel | list[BrowseSeriesModel],
    ) -> list[Datum]:
        """Returns all of the episodes from one or more BrowseSeries entries."""
        if isinstance(input_data, list):
            result: list[Datum] = []
            for response in input_data:
                result.extend(self.extract_entries(response))
            return result

        return input_data.data

"""Test for chirashi."""

from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
from dotenv import load_dotenv

from chirashi import Chirashi
from chirashi.exceptions import HTTPError, LoginError
from chirashi.search.episodes import SearchEpisode
from chirashi.search.music import SearchMusic
from chirashi.search.series import SearchSeries
from chirashi.search.top_results import SearchTopResults

if TYPE_CHECKING:
    from pydantic import BaseModel

    from chirashi.base_api_endpoint import BaseEndpoint

load_dotenv()

client = Chirashi(
    get_around_server=os.environ["GET_AROUND_SERVER"],
    get_around_password=os.environ["GET_AROUND_PASSWORD"],
)
logged_in_client = Chirashi(
    username=os.environ["CRUNCHYROLL_USERNAME"],
    password=os.environ["CRUNCHYROLL_PASSWORD"],
    get_around_server=os.environ["GET_AROUND_SERVER"],
    get_around_password=os.environ["GET_AROUND_PASSWORD"],
)

DOWNLOADS_DRECTORY = (
    Path(__file__).parent
    / "downloads"
    / datetime.now().astimezone().strftime("%Y-%m-%dT%H_%M_%S")
)


def save_response(
    endpoint: BaseEndpoint[BaseModel],
    model: BaseModel,
    name: str = "",
) -> None:
    """Save a parsed API response to the timestamped output directory."""
    class_name = endpoint.__class__.__name__
    if name:
        file_path = DOWNLOADS_DRECTORY / f"{class_name}/{name}.json"
    else:
        file_path = DOWNLOADS_DRECTORY / f"{class_name}.json"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    data = endpoint.dump_response(model)
    file_path.write_text(json.dumps(data, indent=2))


class TestParse:
    """Test parsing files."""

    def test_parse_browse_series(self) -> None:
        """Test parsing browse series files."""
        for json_file in client.browse_series.json_files():
            client.browse_series.parse(json.loads(json_file.read_text()))

    def test_parse_series(self) -> None:
        """Test parsing series files."""
        for json_file in client.series.json_files():
            client.series.parse(json.loads(json_file.read_text()))

    def test_parse_seasons(self) -> None:
        """Test parsing seasons files."""
        for json_file in client.seasons.json_files():
            client.seasons.parse(json.loads(json_file.read_text()))

    def test_parse_episodes(self) -> None:
        """Test parsing episodes files."""
        for json_file in client.episodes.json_files():
            client.episodes.parse(json.loads(json_file.read_text()))

    def test_parse_search(self) -> None:
        """Test parsing search files."""
        for json_file in client.search.json_files():
            client.search.parse(json.loads(json_file.read_text()))

    def test_parse_search_music(self) -> None:
        """Test parsing search music files."""
        for json_file in SearchMusic.json_files():
            SearchMusic.parse(json.loads(json_file.read_text()))

    def test_parse_search_series(self) -> None:
        """Test parsing search series files."""
        for json_file in SearchSeries.json_files():
            SearchSeries.parse(json.loads(json_file.read_text()))

    def test_parse_search_episodes(self) -> None:
        """Test parsing search episode files."""
        for json_file in SearchEpisode.json_files():
            SearchEpisode.parse(json.loads(json_file.read_text()))

    def test_parse_search_top_results(self) -> None:
        """Test parsing search top results files."""
        for json_file in SearchTopResults.json_files():
            SearchTopResults.parse(json.loads(json_file.read_text()))


class TestExtract:
    """Test extracting data."""

    class TestBrowseSeries:
        """Test extracting browse series data."""

        def test_extract_browse_series_entries(self) -> None:
            """Test extracting browse series entries."""
            for json_file in client.browse_series.json_files():
                model = client.browse_series.parse(json.loads(json_file.read_text()))
                entries = client.browse_series.extract_entries(model)
                assert entries == model.data

        def test_extract_browse_series_entries_from_list(self) -> None:
            """Test extracting browse series entries from a list."""
            json_files = client.browse_series.json_files()
            models = [
                client.browse_series.parse(json.loads(f.read_text()))
                for f in json_files
            ]

            entries = client.browse_series.extract_entries(models)
            expected = [datum for model in models for datum in model.data]
            assert entries == expected

    class TestSearch:
        """Test extracting search data by content type."""

        def test_extract_search_music(self) -> None:
            """Test extracting music items from search results."""
            for json_file in client.search.json_files():
                model = client.search.parse(json.loads(json_file.read_text()))
                client.search.extract_music(model)

        def test_extract_search_series(self) -> None:
            """Test extracting series items from search results."""
            for json_file in client.search.json_files():
                model = client.search.parse(json.loads(json_file.read_text()))
                client.search.extract_series(model)

        def test_extract_search_episodes(self) -> None:
            """Test extracting episode items from search results."""
            for json_file in client.search.json_files():
                model = client.search.parse(json.loads(json_file.read_text()))
                client.search.extract_episodes(model)

        def test_extract_search_top_results(self) -> None:
            """Test extracting top results items from search results."""
            for json_file in client.search.json_files():
                model = client.search.parse(json.loads(json_file.read_text()))
                client.search.extract_top_results(model)


class TestGet:
    """Test get functions."""

    class TestValid:
        """Test getting data with valid inputs."""

        def test_get_browse_series(self) -> None:
            """Test getting browse series."""
            model = client.browse_series.get()
            save_response(client.browse_series, model)
            expected_count = 36
            assert expected_count < model.total
            assert len(model.data) == expected_count

        def test_get_series(self) -> None:
            """Test getting series."""
            model = client.series.get("GG5H5XQX4")
            save_response(client.series, model, "GG5H5XQX4")
            expected_count = 1
            assert len(model.data) == expected_count == model.total
            assert model.data[0].id == "GG5H5XQX4"

        def test_get_seasons(self) -> None:
            """Test getting seasons."""
            model = client.seasons.get("GG5H5XQX4")
            save_response(client.seasons, model, "GG5H5XQX4")
            expected_count = 2
            assert len(model.data) == expected_count == model.total
            for data in model.data:
                assert data.series_id == "GG5H5XQX4"

        def test_get_episodes(self) -> None:
            """Test getting episodes."""
            model = client.episodes.get("GYE5CQMQ5")
            save_response(client.episodes, model, "GYE5CQMQ5")
            expected_count = 28
            assert len(model.data) == expected_count == model.total
            for data in model.data:
                assert data.season_id == "GYE5CQMQ5"

        def test_get_search_series(self) -> None:
            """Test getting search results."""
            model = client.search.get("Frieren")
            save_response(client.search, model, "Frieren")
            expected_count = 4  # Search results are grouped into 4 categories.
            assert len(model.data) == expected_count == model.total
            assert client.search.extract_series(model)[0].id == "GG5H5XQX4"

        def test_get_search_music(self) -> None:
            """Test extracting music items from a live search."""
            model = client.search.get("Frieren")
            save_response(client.search, model, "Frieren")
            client.search.extract_music(model)
            assert any(datum.type == "music" for datum in model.data)

        def test_get_search_episodes(self) -> None:
            """Test extracting episode items from a live search."""
            model = client.search.get("Frieren")
            save_response(client.search, model, "Frieren")
            client.search.extract_episodes(model)
            assert any(datum.type == "episode" for datum in model.data)

        def test_get_search_top_results(self) -> None:
            """Test extracting top results items from a live search."""
            model = client.search.get("Frieren")
            save_response(client.search, model, "Frieren")
            client.search.extract_top_results(model)
            assert any(datum.type == "top_results" for datum in model.data)

    class TestPagination:
        """Test get functions with pagination."""

        def test_get_browse_series_since_datetime(self) -> None:
            """Test getting browse series since a datetime."""
            first_page = client.browse_series.get()
            end_datetime = first_page.data[-1].last_public
            response = client.browse_series.get_since_datetime(end_datetime)
            first_page_count = len(client.browse_series.extract_entries(first_page))
            paginated_count = len(client.browse_series.extract_entries(response))

            assert paginated_count > first_page_count

        def test_get_browse_series_past_last_page(self) -> None:
            """Test that paginating past the last page returns no entries.

            Fetches a normal page to discover the total result count, then
            requests a page starting at that total. Since indices are 0-based,
            ``start=total`` is one past the final item and should return an
            empty list.
            """
            first_page = client.browse_series.get()
            past_end = client.browse_series.get(start=first_page.total)
            save_response(client.browse_series, past_end, "past_last_page")
            assert len(past_end.data) == 0

    class TestInvalid:
        """Test get functions with invalid inputs."""

        def test_get_browse_invalid(self) -> None:
            """Test getting an invalid browse."""
            pytest.skip("This cannot be tested.")

        def test_get_series_invalid(self) -> None:
            """Test getting an invalid series."""
            with pytest.raises(HTTPError):
                client.series.get("GGGGGGGGG")

        def test_get_seasons_invalid(self) -> None:
            """Test getting invalid seasons."""
            # This endpoint does not return an HTTP error when no match is found, it
            # instead returns an empty list.
            model = client.seasons.get("GGGGGGGGG")
            save_response(client.seasons, model, "GGGGGGGGG")
            assert model.data == []
            assert model.total == 0

        def test_get_episodes_invalid(self) -> None:
            """Test getting invalid episodes."""
            model = client.episodes.get("GGGGGGGGG")
            save_response(client.seasons, model, "GGGGGGGGG")
            assert model.data == []
            assert model.total == 0

        def test_get_search_no_results(self) -> None:
            """Test searching for a query with no results."""
            model = client.search.get("qwertyuiopasdfghjklzxcvbnm")
            save_response(client.search, model, "qwertyuiopasdfghjklzxcvbnm")
            expected_count = 0  # When no results are found no categories are returned
            assert len(model.data) == expected_count == model.total


class TestLogin:
    """Test logging in with credentials."""

    def test_login(self) -> None:
        """Test logging in using environment variables."""
        logged_in_client.browse_series.get()

    def test_login_method(self) -> None:
        """Test logging in using the login method."""
        login_client = Chirashi(
            get_around_server=os.environ["GET_AROUND_SERVER"],
            get_around_password=os.environ["GET_AROUND_PASSWORD"],
        )
        login_client.login(
            username=os.environ["CRUNCHYROLL_USERNAME"],
            password=os.environ["CRUNCHYROLL_PASSWORD"],
        )
        login_client.browse_series.get()

    def test_login_method_invalid(self) -> None:
        """Test logging in using the login method with invalid credentials."""
        login_client = Chirashi(
            get_around_server=os.environ["GET_AROUND_SERVER"],
            get_around_password=os.environ["GET_AROUND_PASSWORD"],
        )
        with pytest.raises(LoginError):
            login_client.login(
                username="user@example.com",
                password="password",  # noqa: S106
            )

    def test_login_invalid(self) -> None:
        """Test logging in with invalid credentials."""
        invalid_client = Chirashi(
            username="user@example.com",
            password="password",  # noqa: S106
            get_around_server=os.environ["GET_AROUND_SERVER"],
            get_around_password=os.environ["GET_AROUND_PASSWORD"],
        )
        with pytest.raises(LoginError):
            invalid_client.browse_series.get()

    def test_logout(self) -> None:
        """Test logging out reverts to anonymous access."""
        login_client = Chirashi(
            get_around_server=os.environ["GET_AROUND_SERVER"],
            get_around_password=os.environ["GET_AROUND_PASSWORD"],
        )
        login_client.login(
            username=os.environ["CRUNCHYROLL_USERNAME"],
            password=os.environ["CRUNCHYROLL_PASSWORD"],
        )
        login_client.browse_series.get()
        login_client.logout()
        assert login_client.anonymous
        # Should still work as anonymous.
        model = login_client.browse_series.get()
        save_response(client.browse_series, model)
        expected_count = 36
        assert expected_count < model.total
        assert len(model.data) == expected_count

    def test_refresh_token(self) -> None:
        """Test that the refresh token is used when the access token expires."""
        logged_in_client.browse_series.get()
        # Expire the token to force a refresh on the next request.
        logged_in_client._token_expires_at = datetime.now().astimezone()  # noqa: SLF001 # type: ignore[reportPrivateUsage]
        logged_in_client.browse_series.get()

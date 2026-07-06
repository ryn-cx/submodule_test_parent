"""Chirashi is a client for downloading and parsing data from Crunchyroll."""

import uuid
from datetime import UTC, datetime, timedelta
from logging import NullHandler, getLogger
from typing import Any

from get_around import GetAround

from chirashi.browse_series import BrowseSeries
from chirashi.episodes import Episodes
from chirashi.exceptions import HTTPError, LoginError
from chirashi.search import Search
from chirashi.seasons import Seasons
from chirashi.series import Series

DEVICE_ID = uuid.uuid4().hex
DEFAULT_TIMEOUT = 30

logger = getLogger(__name__)
logger.addHandler(NullHandler())


class Chirashi:
    """Interface for downloading and parsing data from Crunchyroll."""

    def __init__(  # noqa: PLR0913
        self,
        # TODO: Login is currently broken after API changes.
        username: str | None = None,
        password: str | None = None,
        # These values were chosen to match the CrunchyRoll app on Windows.
        device_id: str = DEVICE_ID,
        device_type: str = "Microsoft Edge on Windows",
        timeout: int = 30,
        get_around_server: str | None = None,
        get_around_password: str | None = None,
    ) -> None:
        """Initialize the Chirashi client."""
        self.get_around_client = GetAround(
            server=get_around_server,
            password=get_around_password,
        )
        self.timeout = timeout
        self.anonymous = not (username and password)
        self.username = username
        self.password = password
        self._token_expires_at = datetime.now(tz=UTC)
        self.device_id = device_id
        self.device_type = device_type
        self._access_token_value = ""
        self._refresh_token = ""
        self.domain = "beta-api.crunchyroll.com"

        self.browse_series = BrowseSeries(self)
        self.series = Series(self)
        self.seasons = Seasons(self)
        self.episodes = Episodes(self)
        self.search = Search(self)

        super().__init__()

    # TODO: How long is this valid for?
    PUBLIC_TOKEN = "bm9haWhkZXZtXzZpeWcwYThsMHE6"

    @property
    def _access_token(self) -> str:
        if not self._access_token_value or self._token_expires_at < datetime.now(
            tz=UTC,
        ):
            self._download_access_token()

        return self._access_token_value

    @_access_token.setter
    def _access_token(self, value: str) -> None:
        self._access_token_value = value

    def _download_access_token(self) -> None:
        url = f"https://{self.domain}/auth/v1/token"
        headers = {"Authorization": f"Basic {self.PUBLIC_TOKEN}"}

        data: dict[str, Any] = {
            "device_id": self.device_id,
            "device_type": self.device_type,
        }

        if self._refresh_token:
            logger.info("Refreshing access token: %s", url)
            data["grant_type"] = "refresh_token"
            data["refresh_token"] = self._refresh_token
        elif self.anonymous:
            logger.info("Downloading anonymous access token: %s", url)
            data["grant_type"] = "client_id"
        else:
            logger.info("Downloading logged in access token: %s", url)
            data["grant_type"] = "password"
            data["scope"] = "offline_access"
            data["username"] = self.username
            data["password"] = self.password

        response = self.get_around_client.post(
            url,
            data=data,
            headers=headers,
            timeout=self.timeout,
        )
        parsed_response = response.json()

        if "access_token" not in parsed_response:
            raise LoginError(parsed_response.get("error", "Login failed"))

        self._access_token = parsed_response["access_token"]
        self._token_expires_at = datetime.now(tz=UTC) + timedelta(
            seconds=parsed_response["expires_in"],
        )

        # Refresh token are only available when the user is logged into an account.
        if "refresh_token" in parsed_response:
            self._refresh_token = parsed_response["refresh_token"]

    def login(self, username: str, password: str) -> None:
        """Log in with the given credentials.

        Args:
            username: The Crunchyroll username.
            password: The Crunchyroll password.

        Raises:
            LoginError: If the credentials are invalid.
        """
        self.username = username
        self.password = password
        self.anonymous = False
        self._access_token_value = ""
        self._refresh_token = ""
        self._download_access_token()

    def logout(self) -> None:
        """Log out and revert to anonymous access."""
        self.username = None
        self.password = None
        self.anonymous = True
        self._access_token_value = ""
        self._refresh_token = ""

    def download(
        self,
        endpoint: str,
        params: dict[str, Any],
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Make a request to the Crunchyroll API with the given endpoint."""
        if headers is None:
            headers = {}
        headers["authorization"] = f"Bearer {self._access_token}"

        url = f"https://{self.domain}/{endpoint}"
        logger.info("Downloading API data: %s", url)
        response = self.get_around_client.get(
            url,
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

        if response.status_code != 200:  # noqa: PLR2004
            msg = f"Unexpected response status code: {response.status_code}"
            raise HTTPError(msg)

        output = response.json()
        output["chirashi"] = {}
        output["chirashi"]["params"] = params
        headers.pop("authorization")
        output["chirashi"]["headers"] = headers
        output["chirashi"]["url"] = url
        output["chirashi"]["timestamp"] = (
            datetime.now().astimezone().isoformat().replace("+00:00", "Z")
        )

        return output

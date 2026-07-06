# ruff: noqa: D100, D101
from typing import Any

from pydantic import AwareDatetime, BaseModel, ConfigDict


class PosterTallItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int
    type: str
    source: str


class PosterWideItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int
    type: str
    source: str


class Images(BaseModel):
    model_config = ConfigDict(extra="forbid")
    poster_tall: list[list[PosterTallItem]]
    poster_wide: list[list[PosterWideItem]]


class ExtendedMaturityRating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    system: str
    rating: str
    level: str


class Award(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    icon_url: str
    is_current_award: bool
    is_winner: bool


class ContentDescriptorsWithSymbolItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str


class LanguagePresentation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audio_notation: str
    text_notation: str


class Datum(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    channel_id: str
    title: str
    slug: str
    slug_title: str
    description: str
    extended_description: str
    keywords: list[str]
    season_tags: list[str]
    images: Images
    episode_count: int
    season_count: int
    media_count: int
    content_provider: str
    maturity_ratings: list[str]
    extended_maturity_rating: ExtendedMaturityRating
    is_mature: bool
    mature_blocked: bool
    is_subbed: bool
    is_dubbed: bool
    is_simulcast: bool
    seo_title: str
    seo_description: str
    subtitle_locales: list[str]
    audio_locales: list[str]
    availability_status: str
    availability_notes: str
    series_launch_year: int
    awards: list[Award]
    content_descriptors: list[str]
    content_descriptors_with_symbol: list[ContentDescriptorsWithSymbolItem]
    language_presentation: LanguagePresentation


class Params(BaseModel):
    model_config = ConfigDict(extra="forbid")
    locale: str


class Headers(BaseModel):
    model_config = ConfigDict(extra="forbid")
    referer: str


class Chirashi(BaseModel):
    model_config = ConfigDict(extra="forbid")
    params: Params
    headers: Headers
    url: str
    timestamp: AwareDatetime


class Series(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    data: list[Datum]
    meta: dict[str, Any]
    chirashi: Chirashi

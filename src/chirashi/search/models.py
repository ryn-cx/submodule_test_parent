# ruff: noqa: D100, D101
from typing import Any

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field


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


class PromoImageItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int
    type: str
    source: str


class ThumbnailItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int
    type: str
    source: str


class Thumbnail(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int
    type: str
    source: str


class Images(BaseModel):
    model_config = ConfigDict(extra="forbid")
    poster_tall: list[list[PosterTallItem]] | None = None
    poster_wide: list[list[PosterWideItem]] | None = None
    promo_image: list[list[PromoImageItem]] | None = None
    thumbnail: list[list[ThumbnailItem] | Thumbnail] | None = None


class ExtendedMaturityRating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    system: str
    rating: str
    level: str
    advisories: list[None]


class ContentDescriptorsWithSymbolItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str


class Award(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    icon_url: str
    is_current_award: bool
    is_winner: bool


class LanguagePresentation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audio_notation: str
    text_notation: str


class SeriesMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    availability_status: str
    extended_description: str
    episode_count: int
    season_count: int
    extended_maturity_rating: ExtendedMaturityRating
    maturity_ratings: list[str]
    content_descriptors: list[str] | None = None
    content_descriptors_with_symbol: list[ContentDescriptorsWithSymbolItem] | None = (
        None
    )
    is_mature: bool
    mature_blocked: bool
    is_subbed: bool
    is_dubbed: bool
    is_simulcast: bool
    linked_guid: str
    availability_notes: str
    audio_locales: list[str]
    subtitle_locales: list[str]
    series_launch_year: int
    awards: list[Award] | None = None
    tenant_categories: list[str]
    language_presentation: LanguagePresentation


class SearchMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score: float
    rank: int | None = None
    popularity_score: int | float | None = None


class Field1s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    unit: str
    percentage: int


class Field2s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    unit: str
    percentage: int


class Field3s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    unit: str
    percentage: int


class Field4s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    unit: str
    percentage: int


class Field5s(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    unit: str
    percentage: int


class Up(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    unit: str


class Down(BaseModel):
    model_config = ConfigDict(extra="forbid")
    displayed: str
    unit: str


class Rating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field_1s: Field1s | None = Field(None, alias="1s")
    field_2s: Field2s | None = Field(None, alias="2s")
    field_3s: Field3s | None = Field(None, alias="3s")
    field_4s: Field4s | None = Field(None, alias="4s")
    field_5s: Field5s | None = Field(None, alias="5s")
    average: str | None = None
    total: int
    up: Up | None = None
    down: Down | None = None


class AdBreak(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    offset_ms: int


class Version(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audio_locale: str
    guid: str
    original: bool
    variant: str
    season_guid: str
    media_guid: str
    is_premium_only: bool
    roles: list[str]


class EpisodeMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    series_id: str
    series_title: str
    series_slug_title: str
    season_id: str
    season_title: str
    season_slug_title: str
    season_number: int
    episode_number: int
    episode: str
    sequence_number: int
    season_display_number: str
    season_sequence_number: int
    duration_ms: int
    ad_breaks: list[AdBreak]
    episode_air_date: str
    upload_date: str
    availability_starts: str
    availability_ends: str
    eligible_region: str
    is_premium_only: bool
    extended_maturity_rating: ExtendedMaturityRating
    maturity_ratings: list[str]
    content_descriptors: list[str]
    content_descriptors_with_symbol: list[ContentDescriptorsWithSymbolItem]
    is_mature: bool
    mature_blocked: bool
    available_date: None
    free_available_date: str
    premium_date: None
    premium_available_date: str
    is_subbed: bool
    is_dubbed: bool
    is_clip: bool
    available_offline: bool
    linked_guid: str
    tenant_categories: list[str]
    subtitle_locales: list[str]
    availability_notes: str
    audio_locale: str
    versions: list[Version]
    closed_captions_available: bool
    identifier: str
    availability_status: str
    roles: list[str]
    language_presentation: LanguagePresentation


class MainArtistItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    connector: str
    id: str
    name: str
    roles: list[str]
    sequence_number: int = Field(..., alias="sequenceNumber")
    slug: str


class Artists(BaseModel):
    model_config = ConfigDict(extra="forbid")
    main_artist: list[MainArtistItem] = Field(..., alias="MainArtist")


class Genre(BaseModel):
    model_config = ConfigDict(extra="forbid")
    display_value: str = Field(..., alias="displayValue")
    id: str


class Availability(BaseModel):
    model_config = ConfigDict(extra="forbid")
    end_date: AwareDatetime = Field(..., alias="endDate")
    start_date: AwareDatetime = Field(..., alias="startDate")


class Artist(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    name: str
    slug: str


class Item(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    external_id: str | None = None
    channel_id: str | None = None
    linked_resource_key: str | None = None
    new: bool
    title: str
    description: str
    promo_title: str | None = None
    promo_description: str | None = None
    type: str
    slug: str
    slug_title: str | None = None
    last_public: str | None = None
    images: Images
    series_metadata: SeriesMetadata | None = None
    search_metadata: SearchMetadata
    language_presentation: LanguagePresentation | None = None
    rating: Rating | None = None
    episode_metadata: EpisodeMetadata | None = None
    artists: Artists | None = None
    maturity_ratings: dict[str, Any] | None = Field(None, alias="maturityRatings")
    genres: list[Genre] | None = None
    is_mature: bool | None = Field(None, alias="isMature")
    is_public: bool | None = Field(None, alias="isPublic")
    licensor: str | None = None
    duration_ms: int | None = Field(None, alias="durationMs")
    availability: Availability | None = None
    created_at: str | None = Field(None, alias="createdAt")
    ready_to_publish: bool | None = Field(None, alias="readyToPublish")
    anime_ids: list[str] | None = Field(None, alias="animeIds")
    hash: str | None = None
    sequence_number: int | None = Field(None, alias="sequenceNumber")
    is_premium_only: bool | None = Field(None, alias="isPremiumOnly")
    publish_date: AwareDatetime | None = Field(None, alias="publishDate")
    updated_at: str | None = Field(None, alias="updatedAt")
    artist: Artist | None = None
    display_artist_name_required: bool | None = Field(
        None,
        alias="displayArtistNameRequired",
    )
    streams_link: str | None = None
    display_artist_name: str | None = Field(None, alias="displayArtistName")
    original_release: AwareDatetime | None = Field(None, alias="originalRelease")
    mature_blocked: bool | None = Field(None, alias="matureBlocked")
    copyright: str | None = None


class Datum(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    items: list[Item]
    count: int


class Params(BaseModel):
    model_config = ConfigDict(extra="forbid")
    q: str
    n: int
    type: str
    ratings: str
    preferred_audio_language: str
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


class Search(BaseModel):
    model_config = ConfigDict(extra="forbid")
    data: list[Datum]
    total: int
    meta: dict[str, Any]
    chirashi: Chirashi

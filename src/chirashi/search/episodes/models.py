# ruff: noqa: D100, D101
from pydantic import BaseModel, ConfigDict, RootModel


class ThumbnailItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int
    type: str
    source: str


class Images(BaseModel):
    model_config = ConfigDict(extra="forbid")
    thumbnail: list[list[ThumbnailItem]]


class SearchMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    score: float
    rank: int
    popularity_score: int


class LanguagePresentation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audio_notation: str
    text_notation: str


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
    total: int
    up: Up
    down: Down


class AdBreak(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    offset_ms: int


class ExtendedMaturityRating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    system: str
    rating: str
    level: str
    advisories: list[None]


class ContentDescriptorsWithSymbolItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str


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


class SearchEpisodeItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    external_id: str
    channel_id: str
    linked_resource_key: str
    new: bool
    title: str
    description: str
    promo_title: str
    promo_description: str
    type: str
    slug: str
    slug_title: str
    images: Images
    search_metadata: SearchMetadata
    language_presentation: LanguagePresentation
    rating: Rating
    episode_metadata: EpisodeMetadata


class SearchEpisode(RootModel[list[SearchEpisodeItem]]):
    root: list[SearchEpisodeItem]

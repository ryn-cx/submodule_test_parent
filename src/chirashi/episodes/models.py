# ruff: noqa: D100, D101
from pydantic import AwareDatetime, BaseModel, ConfigDict


class ExtendedMaturityRating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    system: str
    rating: str
    level: str


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


class ContentDescriptorsWithSymbolItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str


class ThumbnailItem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    width: int
    height: int
    type: str
    source: str


class Images(BaseModel):
    model_config = ConfigDict(extra="forbid")
    thumbnail: list[list[ThumbnailItem]]


class AdBreak(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str
    offset_ms: int


class LanguagePresentation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    audio_notation: str
    text_notation: str


class Datum(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str
    channel_id: str
    series_id: str
    series_title: str
    series_slug_title: str
    season_id: str
    season_title: str
    season_slug_title: str
    season_number: int
    episode: str
    episode_number: int
    sequence_number: int
    season_display_number: str
    season_sequence_number: int
    production_episode_id: str
    title: str
    slug_title: str
    description: str
    next_episode_id: str
    next_episode_title: str | None = None
    hd_flag: bool
    maturity_ratings: list[str]
    extended_maturity_rating: ExtendedMaturityRating
    is_mature: bool
    mature_blocked: bool
    episode_air_date: AwareDatetime
    upload_date: AwareDatetime
    availability_starts: AwareDatetime
    availability_ends: AwareDatetime
    eligible_region: str
    available_date: None
    free_available_date: AwareDatetime
    premium_date: None
    premium_available_date: AwareDatetime
    is_subbed: bool
    is_dubbed: bool
    is_clip: bool
    seo_title: str
    seo_description: str
    season_tags: list[None]
    available_offline: bool
    subtitle_locales: list[str]
    availability_notes: str
    audio_locale: str
    versions: list[Version]
    closed_captions_available: bool
    identifier: str
    content_descriptors: list[str]
    content_descriptors_with_symbol: list[ContentDescriptorsWithSymbolItem]
    media_type: str
    slug: str
    images: Images
    duration_ms: int
    ad_breaks: list[AdBreak]
    is_premium_only: bool
    listing_id: str
    recent_audio_locale: str
    recent_variant: str
    availability_status: str
    language_presentation: LanguagePresentation
    roles: list[str]


class Meta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    versions_considered: bool | None = None


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


class Episodes(BaseModel):
    model_config = ConfigDict(extra="forbid")
    data: list[Datum]
    total: int
    meta: Meta
    chirashi: Chirashi

# ruff: noqa: D100, D101
from pydantic import BaseModel, ConfigDict, Field, RootModel


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


class Images(BaseModel):
    model_config = ConfigDict(extra="forbid")
    poster_tall: list[list[PosterTallItem]]
    poster_wide: list[list[PosterWideItem]]
    promo_image: list[list[PromoImageItem]]


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
    rank: int
    popularity_score: int | float


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


class Rating(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field_1s: Field1s = Field(..., alias="1s")
    field_2s: Field2s = Field(..., alias="2s")
    field_3s: Field3s = Field(..., alias="3s")
    field_4s: Field4s = Field(..., alias="4s")
    field_5s: Field5s = Field(..., alias="5s")
    average: str
    total: int


class SearchTopResult(BaseModel):
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
    last_public: str
    images: Images
    series_metadata: SeriesMetadata
    search_metadata: SearchMetadata
    language_presentation: LanguagePresentation
    rating: Rating


class SearchTopResults(RootModel[list[SearchTopResult]]):
    root: list[SearchTopResult]

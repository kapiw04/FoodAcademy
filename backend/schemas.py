from pydantic import (
    BaseModel,
    Field,
    ValidationInfo,
    field_validator,
    model_validator,
)
from typing import Annotated, Optional
from typing_extensions import Self
from datetime import date


class FoodCreate(BaseModel):
    name: str
    expiration_date: date
    quantity: int
    opened: Annotated[bool, Field(validate_default=True)] = False
    opened_date: Annotated[Optional[date], Field(validate_default=True)] = None

    @model_validator(mode='after')
    def check_if_no_additional_info_when_closed(self) -> Self:
        """Check if opened date is provided for opened food item and not provided for closed food item.

        Raises:
            ValueError: If opened date is provided for closed food item or vice versa.
        """
        if self.opened and not self.opened_date:
            raise ValueError(
                "Opened date must be provided for opened food item.")
        if not self.opened and self.opened_date:
            raise ValueError(
                "Opened date must not be provided for closed food item.")

        return self

    @model_validator(mode='after')
    def check_dates_order(self) -> Self:
        """Check if expiration date is after opened date.
        """
        if self.opened_date and self.expiration_date < self.opened_date:
            raise ValueError(
                "Expiration date must be after opened date.")

        return self

    @field_validator('expiration_date', 'opened_date', mode='after')
    @classmethod
    def check_date_past_today(cls, value: date, info: ValidationInfo) -> date:
        """Check if date is past today.

        Raises:
            ValueError: If date is not past today.
        """
        if value is None:
            return value
        if value < date.today():
            raise ValueError(
                f"{info.field_name.capitalize()} must be past today.")

        return value


# TODO: those validation seems unnecessary, as they are already validated in the model


class FoodUpdate(BaseModel):
    id: int
    name: Optional[str]
    expiration_date: Optional[date] = None
    quantity: Optional[int] = None
    opened: Annotated[Optional[bool], Field(validate_default=True)] = None
    opened_date: Annotated[Optional[date], Field(validate_default=True)] = None

    @model_validator(mode='after')
    def check_if_no_additional_info_when_closed(self) -> Self:
        """Check if opened date is provided for opened food item and not provided for closed food item.

        Raises:
            ValueError: If opened date is provided for closed food item or vice versa.
        """
        if self.opened and not self.opened_date:
            raise ValueError(
                "Opened date must be provided for opened food item.")
        if not self.opened and self.opened_date:
            raise ValueError(
                "Opened date must not be provided for closed food item.")

        return self

    @model_validator(mode='after')
    def check_dates_order(self) -> Self:
        """Check if expiration date is after opened date.
        """
        if self.opened_date and self.expiration_date < self.opened_date:
            raise ValueError(
                "Expiration date must be after opened date.")

        return self

    @field_validator('expiration_date', 'opened_date', mode='after')
    @classmethod
    def check_date_past_today(cls, value: date, info: ValidationInfo) -> date:
        """Check if date is past today.

        Raises:
            ValueError: If date is not past today.
        """
        if value is None:
            return value
        if value < date.today():
            raise ValueError(
                f"{info.field_name.capitalize()} must be past today.")

        return value


class FoodResponse(BaseModel):
    id: int
    name: str
    expiration_date: date
    quantity: int
    opened: Annotated[bool, Field(validate_default=True)] = False
    opened_date: Annotated[Optional[date], Field(validate_default=True)] = None

    @model_validator(mode='after')
    def check_if_no_additional_info_when_closed(self) -> Self:
        """Check if opened date is provided for opened food item and not provided for closed food item.

        Raises:
            ValueError: If opened date is provided for closed food item or vice versa.
        """
        if self.opened and not self.opened_date:
            raise ValueError(
                "Opened date must be provided for opened food item.")
        if not self.opened and self.opened_date:
            raise ValueError(
                "Opened date must not be provided for closed food item.")

        return self

    @ model_validator(mode='after')
    def check_dates_order(self) -> Self:
        """Check if expiration date is after opened date.
        """
        if self.opened_date and self.expiration_date < self.opened_date:
            raise ValueError(
                "Expiration date must be after opened date.")

        return self

    @ field_validator('expiration_date', 'opened_date', mode='after')
    @classmethod
    def check_date_past_today(cls, value: date, info: ValidationInfo) -> date:
        """Check if date is past today.

        Raises:
            ValueError: If date is not past today.
        """
        if value is None:
            return value
        if value < date.today():
            raise ValueError(
                f"{info.field_name.capitalize()} must be past today.")

        return value


class FoodDelete(BaseModel):
    id: int

from pydantic import (
    BaseModel,
    field_validator,
    ValidationInfo
)
from typing import Optional
from datetime import date


class FoodCreate(BaseModel):
    name: str
    expiration_date: date
    quantity: int
    opened: bool = False
    opened_date: Optional[date] = None

    @field_validator("opened_date")
    @classmethod
    def check_if_no_additional_info_when_closed(cls, opened_date: date, info: ValidationInfo):
        """Check if opened date is provided for opened food item and not provided for closed food item.

        Args:
            v (date): Opened date.
            info (ValidationInfo): Validation information.

        Raises:
            ValueError: If opened date is not provided for opened food item.
        """

        opened = info.data.get("opened")
        if opened and not opened_date:
            raise ValueError(
                "Opened date must be provided for opened food item.")

        if not opened and opened_date is not None:
            raise ValueError(
                "Opened date must not be provided for closed food item.")

        return opened_date

    @field_validator("expiration_date")
    @classmethod
    def check_dates_order(cls, expiration_date: date, info: ValidationInfo):
        """Check if expiration date is after opened date.

        Args:
            v (date): Date value.
            info (ValidationInfo): Validation information.

        Returns:
            date: Date value.

        Raises:
            ValueError: If expiration date is before opened date.
            ValueError: If expiration date is before today.
        """
        opened_date = info.data.get("opened_date")
        if not opened_date:
            return expiration_date

        if expiration_date < opened_date:
            raise ValueError(
                "Expiration date must be after opened date.")

        if expiration_date < date.today():
            raise ValueError(
                "Expiration date must not be before today.")

        return expiration_date

    @field_validator("expiration_date", "opened_date")
    @classmethod
    def check_date_past_today(cls, date_to_check: date):
        """Check if date is before today.

        Args:
            v (date): Date value.

        Raises:
            ValueError: If date is before today.
        """
        if date_to_check and date_to_check < date.today():
            raise ValueError(
                "Date must not be before today.")

        return date_to_check


class FoodUpdate(BaseModel):
    id: int
    name: Optional[str]
    expiration_date: Optional[date] = None
    quantity: Optional[int] = None
    opened: Optional[bool] = None
    opened_date: Optional[date] = None


class FoodResponse(BaseModel):
    id: int
    name: str
    expiration_date: date
    quantity: int
    opened: bool
    opened_date: Optional[date] = None


class FoodDelete(BaseModel):
    id: int

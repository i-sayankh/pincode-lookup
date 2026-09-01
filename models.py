from pydantic import BaseModel, field_validator


class PinCodeRequest(BaseModel):
    pincode: str

    # pincode must be exactly 6 digits
    @field_validator("pincode")
    @classmethod
    def validate_pincode(cls, value):
        if len(value) != 6 or not value.isdigit():
            raise ValueError("Pincode must be exactly 6 digits")
        return value


class LocationResponse(BaseModel):
    pincode: str
    city: str
    state: str
    district: str


class BulkRequest(BaseModel):
    pincodes: list[str]

    @field_validator("pincodes")
    @classmethod
    def validate_pincodes(cls, values):
        if len(values) == 0:
            raise ValueError("At least one pincode is required")
        if len(values) > 20:
            raise ValueError("Maximum 20 pincodes are allowed")

        for pincode in values:
            if len(pincode) != 6 or not pincode.isdigit():
                raise ValueError("Each pincode must be exactly 6 digits")

        return values


class BulkResponse(BaseModel):
    status: str = "success"
    found: int
    not_found: int
    results: list[LocationResponse]
    missing: list[str]

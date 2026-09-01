from fastapi import FastAPI
from exceptions import (
    PinCodeNotFoundError,
    pincode_not_found_handler,
    InvalidPincodeError,
    invalid_pincode_handler,
)
from models import PinCodeRequest, LocationResponse, BulkRequest, BulkResponse
from data import pincode_db

app = FastAPI(
    title="Pincode lookup API",
    description="Autofill city and state from Indian pincode during checkout",
)

# Register custom exception handlers
app.add_exception_handler(PinCodeNotFoundError, pincode_not_found_handler)
app.add_exception_handler(InvalidPincodeError, invalid_pincode_handler)


@app.get("/")
def root():
    return {"message": "Welcome to the Pincode lookup API"}


@app.get("/pincode/{pincode}", response_model=LocationResponse)
def lookup_pincode(pincode: str):
    if len(pincode) != 6 or not pincode.isdigit():
        raise InvalidPincodeError(pincode)
    if pincode not in pincode_db:
        raise PinCodeNotFoundError(pincode)
    return pincode_db[pincode]


@app.post("/pincode/bulk", response_model=BulkResponse)
def bulk_lookup(request: BulkRequest):
    results = []
    missing = []

    for pincode in request.pincodes:
        if pincode in pincode_db:
            results.append(pincode_db[pincode])
        else:
            missing.append(pincode)

    return BulkResponse(
        found=len(results),
        not_found=len(missing),
        results=results,
        missing=missing,
    )

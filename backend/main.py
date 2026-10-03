from pathlib import Path
from typing import List
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.recommendation import (
    df,
    get_recommendations,
    software_use_cases
)


# =========================================================
# Paths
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


# =========================================================
# FastAPI App
# =========================================================

app = FastAPI(
    title="BUtech Laptop Finder API",
    description="Laptop recommendation API for BUtech",
    version="1.0.0"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Request Model
# =========================================================

class RecommendationRequest(BaseModel):

    software: List[str] = Field(
        default=[],
        description="Selected software"
    )

    budget: int = Field(
        gt=0,
        description="Maximum budget in EGP"
    )

    brand: str = Field(
        default="Any",
        description="Preferred laptop brand"
    )

    laptop_type: str = Field(
        default="Any",
        description="Preferred laptop category"
    )

    top_n: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of recommendations"
    )


# =========================================================
# API Routes
# =========================================================

@app.get("/health")
def health_check():

    return {
        "status": "healthy",
        "dataset_size": len(df)
    }


@app.get("/software")
def get_available_software():

    return {
        "software": list(software_use_cases.keys())
    }


@app.post("/recommend")
def recommend(request: RecommendationRequest):

    try:

        invalid_software = [
            software
            for software in request.software
            if software not in software_use_cases
        ]

        if invalid_software:

            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invalid software selection",
                    "invalid_software": invalid_software
                }
            )

        results = get_recommendations(
            df=df,
            selected_software=request.software,
            selected_budget=request.budget,
            selected_brand=request.brand,
            selected_laptop_type=request.laptop_type,
            top_n=request.top_n
        )

        return {
            "success": True,

            "request": {
                "software": request.software,
                "budget": request.budget,
                "brand": request.brand,
                "laptop_type": request.laptop_type
            },

            "results": results
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# Admin Routes
# =========================================================

@app.get("/admin/laptops")
def get_admin_laptops():

    try:

        laptops = df.copy()

        return {
            "success": True,
            "count": len(laptops),
            "laptops": laptops[
                [
                    "code",
                    "model",
                    "ram",
                    "cpu",
                    "gpu_model",
                    "price"
                ]
            ].fillna("").to_dict(
                orient="records"
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

# =========================================================
# Add Laptop
# =========================================================

@app.post("/admin/laptops")
def add_admin_laptop(laptop: dict):

    try:

        required_fields = [
            "code",
            "model",
            "ram",
            "cpu",
            "gpu_model",
            "price"
        ]


        for field in required_fields:

            if field not in laptop:

                raise HTTPException(
                    status_code=400,
                    detail=f"Missing field: {field}"
                )


        if any(
            str(laptop[field]).strip() == ""
            for field in [
                "code",
                "model",
                "cpu",
                "gpu_model"
            ]
        ):

            raise HTTPException(
                status_code=400,
                detail="Required fields cannot be empty"
            )


        global df


        new_laptop = laptop.copy()


        new_laptop["ram"] = int(
            new_laptop["ram"]
        )


        new_laptop["price"] = float(
            new_laptop["price"]
        )


        if (
            df["code"]
            .astype(str)
            .eq(str(new_laptop["code"]))
            .any()
        ):

            raise HTTPException(
                status_code=400,
                detail="Laptop code already exists"
            )


        new_row = pd.DataFrame(
            [new_laptop]
        )


        # Preserve all existing CSV columns.
        for column in df.columns:

            if column not in new_row.columns:

                new_row[column] = ""


        new_row = new_row[
            df.columns
        ]


        df = pd.concat(
            [
                df,
                new_row
            ],
            ignore_index=True
        )


        csv_path =BASE_DIR / "data" / "laptops_final.csv"


        df.to_csv(
            csv_path,
            index=False
        )


        return {

            "success": True,

            "message":
                "Laptop added successfully",

            "laptop":
                new_laptop,

            "dataset_size":
                len(df)

        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    # =========================================================
# Delete Laptop
# =========================================================

@app.delete("/admin/laptops/{code}")
def delete_admin_laptop(code: str):

    try:

        global df

        # Check if laptop exists
        matches = (
            df["code"]
            .astype(str)
            .eq(str(code))
        )

        if not matches.any():

            raise HTTPException(
                status_code=404,
                detail="Laptop not found"
            )

        # Remove laptop
        df = df.loc[~matches].reset_index(drop=True)

        # Save updated dataset
        csv_path = BASE_DIR / "data" / "laptops_final.csv"

        df.to_csv(
            csv_path,
            index=False
        )

        return {
            "success": True,
            "message": "Laptop deleted successfully",
            "deleted_code": code,
            "dataset_size": len(df)
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
# =========================================================
# Frontend
# =========================================================

app.mount(
    "/frontend",
    StaticFiles(directory=str(FRONTEND_DIR)),
    name="frontend"
)


# =========================================================
# Home Page
# =========================================================

@app.get("/")
def root():

    return {
        "message": "BUtech Laptop Finder API",
        "status": "running"
    }
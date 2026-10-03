import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# BUtech Laptop Finder - Recommendation Engine
# ============================================================

# =========================
# Load Dataset
# =========================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "laptops_final.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print("Shape:", df.shape)


# =========================
# Software Mapping
# =========================

software_use_cases = {

    # Programming
    "VS Code": ["Programming"],
    "PyCharm": ["Programming"],
    "Visual Studio": ["Programming"],
    "IntelliJ IDEA": ["Programming"],
    "Eclipse": ["Programming"],
    "Android Studio": ["Programming"],
    "Git": ["Programming"],
    "Node.js": ["Programming"],

    # Data Science & AI
    "Python": ["Data Science & AI", "Programming"],
    "Jupyter Notebook": ["Data Science & AI"],
    "Anaconda": ["Data Science & AI"],
    "Power BI": ["Data Science & AI", "Business & Analytics"],
    "Tableau": ["Data Science & AI", "Business & Analytics"],
    "R / RStudio": ["Data Science & AI"],
    "SQL Server": ["Data Science & AI", "Business & Analytics"],
    "MySQL": ["Data Science & AI"],
    "PostgreSQL": ["Data Science & AI"],
    "Apache Spark": ["Data Science & AI", "Cloud & DevOps"],

    # Cybersecurity
    "Kali Linux": ["Cybersecurity"],
    "Wireshark": ["Cybersecurity", "Networking & IT"],
    "Burp Suite": ["Cybersecurity"],
    "Metasploit": ["Cybersecurity"],
    "Nmap": ["Cybersecurity", "Networking & IT"],

    # Networking & IT
    "Cisco Packet Tracer": ["Networking & IT"],
    "GNS3": ["Networking & IT"],
    "EVE-NG": ["Networking & IT"],
    "VMware": ["Networking & IT", "Cloud & DevOps"],
    "VirtualBox": ["Networking & IT", "Cloud & DevOps"],
    "WSL": ["Networking & IT", "Programming"],

    # Gaming
    "Steam": ["Gaming"],
    "Epic Games": ["Gaming"],
    "Fortnite": ["Gaming"],
    "GTA V": ["Gaming"],
    "Call of Duty": ["Gaming"],
    "Minecraft": ["Gaming"],

    # Graphic Design
    "Photoshop": ["Graphic Design"],
    "Illustrator": ["Graphic Design"],
    "InDesign": ["Graphic Design"],
    "Figma": ["Graphic Design"],
    "CorelDRAW": ["Graphic Design"],
    "Canva": ["Graphic Design"],

    # Video Editing
    "Premiere Pro": ["Video Editing"],
    "After Effects": ["Video Editing"],
    "DaVinci Resolve": ["Video Editing"],
    "Filmora": ["Video Editing"],
    "CapCut": ["Video Editing"],

    # 3D & Rendering
    "Blender": ["3D & Rendering"],
    "3ds Max": ["3D & Rendering"],
    "Maya": ["3D & Rendering"],
    "Cinema 4D": ["3D & Rendering"],
    "Unreal Engine": ["3D & Rendering"],
    "Unity": ["3D & Rendering"],

    # Engineering
    "MATLAB": ["Engineering"],
    "AutoCAD": ["Engineering", "Architecture"],
    "SolidWorks": ["Engineering"],
    "CATIA": ["Engineering"],
    "ANSYS": ["Engineering"],
    "ETABS": ["Engineering", "Architecture"],
    "SAP2000": ["Engineering", "Architecture"],
    "Civil 3D": ["Engineering", "Architecture"],

    # Architecture
    "Revit": ["Architecture"],

    # Business & Analytics
    "Excel": ["Business & Analytics"],
    "Microsoft Access": ["Business & Analytics"],
    "Microsoft PowerPoint": ["Business & Analytics"],

    # Office & Study
    "Microsoft Word": ["Office & Study"],
    "Teams": ["Office & Study"],
    "Zoom": ["Office & Study"],
    "Chrome": ["Office & Study"],

    # Cloud & DevOps
    "Docker": ["Cloud & DevOps"],
    "Kubernetes": ["Cloud & DevOps"],
    "Terraform": ["Cloud & DevOps"],

    # Embedded Systems
    "Arduino IDE": ["Embedded Systems"],
    "STM32CubeIDE": ["Embedded Systems"],
    "Proteus": ["Embedded Systems"],

    # Content Creation
    "OBS Studio": ["Content Creation"],

    # Audio
    "FL Studio": ["Content Creation"],
    "Ableton Live": ["Content Creation"],
    "Adobe Audition": ["Content Creation"]
}


def get_software_use_cases(selected_software):

    matched_use_cases = []

    for software in selected_software:

        if software in software_use_cases:

            matched_use_cases.extend(
                software_use_cases[software]
            )

    # Remove duplicates while preserving order
    return list(dict.fromkeys(matched_use_cases))


# =========================
# Use Case Requirements
# =========================

use_case_hardware_requirements = {

    "Programming": {
        "cpu_required": 60,
        "gpu_required": 50,
        "ram_required": 16
    },

    "Data Science & AI": {
        "cpu_required": 75,
        "gpu_required": 65,
        "ram_required": 16
    },

    "Cybersecurity": {
        "cpu_required": 70,
        "gpu_required": 50,
        "ram_required": 16
    },

    "Networking & IT": {
        "cpu_required": 60,
        "gpu_required": 50,
        "ram_required": 16
    },

    "Gaming": {
        "cpu_required": 80,
        "gpu_required": 85,
        "ram_required": 16
    },

    "Graphic Design": {
        "cpu_required": 70,
        "gpu_required": 75,
        "ram_required": 16
    },

    "Video Editing": {
        "cpu_required": 80,
        "gpu_required": 80,
        "ram_required": 16
    },

    "3D & Rendering": {
        "cpu_required": 85,
        "gpu_required": 90,
        "ram_required": 16
    },

    "Engineering": {
        "cpu_required": 70,
        "gpu_required": 65,
        "ram_required": 16
    },

    "Architecture": {
        "cpu_required": 75,
        "gpu_required": 80,
        "ram_required": 16
    },

    "Business & Analytics": {
        "cpu_required": 60,
        "gpu_required": 50,
        "ram_required": 16
    },

    "Office & Study": {
        "cpu_required": 50,
        "gpu_required": 50,
        "ram_required": 16
    },

    "Content Creation": {
        "cpu_required": 75,
        "gpu_required": 70,
        "ram_required": 16
    },

    "Cloud & DevOps": {
        "cpu_required": 75,
        "gpu_required": 50,
        "ram_required": 16
    },

    "Embedded Systems": {
        "cpu_required": 60,
        "gpu_required": 50,
        "ram_required": 16
    }
}


use_case_requirements_df = pd.DataFrame(
    use_case_hardware_requirements
).T


# =========================
# CPU Scoring
# =========================

def calculate_cpu_score(cpu):

    cpu = str(cpu).upper()

    if "CORE ULTRA 7" in cpu:
        return 92

    if "CORE ULTRA 5" in cpu:

        if "125H" in cpu:
            return 88

        return 82

    if "I7" in cpu:

        if "13650HX" in cpu:
            return 100

        if "13700H" in cpu:
            return 98

        if "13620H" in cpu:
            return 94

        if "12700H" in cpu:
            return 93

        if "1355U" in cpu:
            return 86

        if "1255U" in cpu:
            return 82

        if "1185G7" in cpu:
            return 78

        if "1165G7" in cpu:
            return 76

    if "I5" in cpu:

        if "13450HX" in cpu:
            return 94

        if "12450HX" in cpu:
            return 88

        if "12500H" in cpu:
            return 90

        if "13420H" in cpu:
            return 85

        if "1335U" in cpu:
            return 80

        if "1245U" in cpu:
            return 76

        if "1235U" in cpu:
            return 74

        if "1145G7" in cpu:
            return 70

        if "1135G7" in cpu:
            return 68

        if "10310U" in cpu:
            return 64

        if "10210U" in cpu:
            return 62

        if "8365U" in cpu:
            return 58

        if "8265U" in cpu:
            return 56

        if "8350U" in cpu:
            return 55

    if "RYZEN 7" in cpu:

        if "7840HS" in cpu:
            return 97

        if "7435HS" in cpu:
            return 90

        if "7730U" in cpu:
            return 82

        if "5850U" in cpu:
            return 78

    if "RYZEN 5" in cpu:

        if "8645HS" in cpu:
            return 93

        if "7535HS" in cpu:
            return 87

        if "7235HS" in cpu:
            return 85

        if "7530U" in cpu:
            return 78

        if "5650U" in cpu:
            return 72

        if "4650U" in cpu:
            return 65

    return 50


df["cpu_score"] = df["cpu"].apply(
    calculate_cpu_score
)


# =========================
# GPU Scoring
# =========================

def calculate_gpu_score(
    gpu_model,
    vram
):

    gpu_model = str(gpu_model).strip()

    try:
        vram = float(vram)
    except (ValueError, TypeError):
        vram = 0

    if gpu_model == "Intel UHD 620":
        score = 50

    elif gpu_model == "Intel UHD":
        score = 55

    elif gpu_model == "Intel Graphics":
        score = 55

    elif gpu_model == "Iris Xe":
        score = 68

    elif gpu_model == "Radeon":
        score = 68

    elif gpu_model == "Intel Arc":
        score = 75

    elif gpu_model == "RTX 2050":
        score = 75

    elif gpu_model == "RTX 3050":

        score = 82

        if vram >= 6:
            score = 86

    elif gpu_model == "RTX 4050":
        score = 95

    else:
        score = 40

    return score


df["gpu_score"] = df.apply(
    lambda row:
    calculate_gpu_score(
        row["gpu_model"],
        row["vram"]
    ),
    axis=1
)


# =========================
# Component Matching
# =========================

def calculate_component_match(
    actual_score,
    required_score
):

    if actual_score >= required_score:

        extra = actual_score - required_score

        return (
            80
            + min(
                extra / (100 - required_score),
                1
            ) * 20
        )

    return (
        actual_score / required_score
    ) * 80


def calculate_ram_requirement_match(
    ram,
    required_ram
):

    try:
        ram = float(ram)
    except (ValueError, TypeError):
        ram = 0

    if ram >= required_ram:
        return 100

    return (
        ram / required_ram
    ) * 80


# =========================
# Use Case Match
# =========================

def calculate_use_case_match_score(
    laptop,
    use_case
):

    requirements = use_case_requirements_df.loc[
        use_case
    ]

    cpu_score = laptop["cpu_score"]
    gpu_score = laptop["gpu_score"]
    ram = laptop["ram"]

    cpu_required = requirements["cpu_required"]
    gpu_required = requirements["gpu_required"]
    ram_required = requirements["ram_required"]

    cpu_match = calculate_component_match(
        cpu_score,
        cpu_required
    )

    gpu_match = calculate_component_match(
        gpu_score,
        gpu_required
    )

    ram_match = calculate_ram_requirement_match(
        ram,
        ram_required
    )

    return (
        cpu_match * 0.40
        + gpu_match * 0.35
        + ram_match * 0.25
    )


def calculate_overall_requirement_match(
    laptop,
    selected_software
):

    matched_use_cases = get_software_use_cases(
        selected_software
    )

    if not matched_use_cases:
        return 0

    scores = []

    for use_case in matched_use_cases:

        score = calculate_use_case_match_score(
            laptop,
            use_case
        )

        scores.append(score)

    return np.mean(scores)


# =========================
# Combined RAM Requirement
# =========================

def get_combined_ram_requirement(
    selected_software
):

    matched_use_cases = get_software_use_cases(
        selected_software
    )

    if not matched_use_cases:
        return 8

    ram_requirements = [

        use_case_requirements_df.loc[
            use_case,
            "ram_required"
        ]

        for use_case in matched_use_cases
    ]

    return max(ram_requirements)


# =========================
# Brand
# =========================

def get_brand(model):

    model = str(model).lower()

    if "hp" in model:
        return "HP"

    if "dell" in model:
        return "Dell"

    if "lenovo" in model:
        return "Lenovo"

    return "Other"


if "brand" not in df.columns:

    df["brand"] = df["model"].apply(
        get_brand
    )


def calculate_brand_score(
    brand,
    selected_brand
):

    if selected_brand == "Any":
        return 100

    if brand == selected_brand:
        return 100

    return 0


# =========================
# Laptop Type
# =========================

def calculate_type_score(
    laptop_type,
    selected_type
):

    if selected_type == "Any":
        return 100

    if laptop_type == selected_type:
        return 100

    return 0


# =========================
# Budget
# =========================

def calculate_budget_score(
    price,
    budget
):

    if budget <= 0:
        return 0

    if price > budget:
        return 0

    saving_ratio = (
        (budget - price) / budget
    )

    return 100 - (
        saving_ratio * 50
    )


def get_budget_status(
    price,
    budget
):

    if price <= budget:
        return "Within Budget"

    return "Over Budget"


def get_budget_reason(
    price,
    budget
):

    if price < budget:

        saving = budget - price

        return (
            f"Within budget — "
            f"saves {saving:,.0f} EGP"
        )

    if price == budget:
        return "Exactly within your budget"

    return "Over budget"


# =========================
# Dynamic Reasons
# =========================

def get_cpu_reason_for_use_case(
    cpu_score,
    use_case
):

    required = use_case_requirements_df.loc[
        use_case,
        "cpu_required"
    ]

    if cpu_score >= required:

        if cpu_score >= required + 15:
            return (
                f"CPU exceeds the recommended "
                f"level for {use_case}"
            )

        return (
            f"CPU meets the recommended "
            f"level for {use_case}"
        )

    difference = required - cpu_score

    if difference <= 10:
        return (
            f"CPU is slightly below the "
            f"recommended level for {use_case}"
        )

    return (
        f"CPU is below the recommended "
        f"level for {use_case}"
    )


def get_gpu_reason_for_use_case(
    gpu_score,
    use_case
):

    required = use_case_requirements_df.loc[
        use_case,
        "gpu_required"
    ]

    if gpu_score >= required:

        if gpu_score >= required + 15:
            return (
                f"GPU exceeds the recommended "
                f"level for {use_case}"
            )

        return (
            f"GPU meets the recommended "
            f"level for {use_case}"
        )

    difference = required - gpu_score

    if difference <= 10:
        return (
            f"GPU is slightly below the "
            f"recommended level for {use_case}"
        )

    return (
        f"GPU is below the recommended "
        f"level for {use_case}"
    )


def get_ram_reason_for_use_case(
    ram,
    use_case
):

    required_ram = use_case_requirements_df.loc[
        use_case,
        "ram_required"
    ]

    if ram >= required_ram:

        return (
            f"{ram}GB RAM meets the recommended "
            f"requirement for {use_case}"
        )

    if ram >= required_ram * 0.75:

        return (
            f"{ram}GB RAM is below the recommended "
            f"{required_ram}GB for {use_case}"
        )

    return (
        f"{ram}GB RAM may be insufficient "
        f"for {use_case}"
    )


def get_primary_use_cases(
    selected_software
):

    matched_use_cases = get_software_use_cases(
        selected_software
    )

    return matched_use_cases


def get_use_case_summary(
    selected_software
):

    matched_use_cases = get_primary_use_cases(
        selected_software
    )

    if not matched_use_cases:
        return "General use"

    if len(matched_use_cases) == 1:
        return matched_use_cases[0]

    if len(matched_use_cases) == 2:
        return (
            f"{matched_use_cases[0]} "
            f"and {matched_use_cases[1]}"
        )

    return (
        ", ".join(matched_use_cases[:-1])
        + " and "
        + matched_use_cases[-1]
    )


def get_laptop_reasons(
    laptop,
    selected_software,
    budget
):

    reasons = []

    # -------------------------
    # Budget
    # -------------------------

    reasons.append(
        get_budget_reason(
            laptop["price"],
            budget
        )
    )

    # -------------------------
    # Workload
    # -------------------------

    matched_use_cases = get_primary_use_cases(
        selected_software
    )

    if not matched_use_cases:

        reasons.append(
            get_cpu_reason(
                laptop["cpu_score"]
            )
        )

        reasons.append(
            get_gpu_reason(
                laptop["gpu_score"]
            )
        )

        reasons.append(
            f"{int(laptop['ram'])}GB RAM available"
        )

        return reasons

    # -------------------------
    # CPU
    # -------------------------

    best_cpu_reason = None

    for use_case in matched_use_cases:

        required = use_case_requirements_df.loc[
            use_case,
            "cpu_required"
        ]

        if laptop["cpu_score"] >= required:

            candidate = get_cpu_reason_for_use_case(
                laptop["cpu_score"],
                use_case
            )

            if best_cpu_reason is None:
                best_cpu_reason = candidate

            if laptop["cpu_score"] >= required + 15:
                best_cpu_reason = candidate
                break

    if best_cpu_reason is None:

        best_cpu_reason = (
            f"CPU is below the recommended "
            f"level for {matched_use_cases[0]}"
        )

    reasons.append(best_cpu_reason)

    # -------------------------
    # GPU
    # -------------------------

    best_gpu_reason = None

    for use_case in matched_use_cases:

        required = use_case_requirements_df.loc[
            use_case,
            "gpu_required"
        ]

        if laptop["gpu_score"] >= required:

            candidate = get_gpu_reason_for_use_case(
                laptop["gpu_score"],
                use_case
            )

            if best_gpu_reason is None:
                best_gpu_reason = candidate

            if laptop["gpu_score"] >= required + 15:
                best_gpu_reason = candidate
                break

    if best_gpu_reason is None:

        best_gpu_reason = (
            f"GPU is below the recommended "
            f"level for {matched_use_cases[0]}"
        )

    reasons.append(best_gpu_reason)

    # -------------------------
    # RAM
    # -------------------------

    required_ram = get_combined_ram_requirement(
        selected_software
    )

    if laptop["ram"] >= required_ram:

        reasons.append(
            f"{int(laptop['ram'])}GB RAM meets "
            f"the recommended requirement"
        )

    else:

        reasons.append(
            f"{int(laptop['ram'])}GB RAM is below "
            f"the recommended {required_ram}GB"
        )

    # -------------------------
    # Overall workload summary
    # -------------------------

    requirement_score = (
        calculate_overall_requirement_match(
            laptop,
            selected_software
        )
    )

    if requirement_score >= 90:

        reasons.append(
            f"Strong hardware match for "
            f"{get_use_case_summary(selected_software)}"
        )

    elif requirement_score >= 75:

        reasons.append(
            f"Good hardware match for "
            f"{get_use_case_summary(selected_software)}"
        )

    elif requirement_score >= 60:

        reasons.append(
            f"Usable for "
            f"{get_use_case_summary(selected_software)}, "
            f"with some hardware limitations"
        )

    else:

        reasons.append(
            f"Hardware limitations for "
            f"{get_use_case_summary(selected_software)}"
        )

    return reasons


# =========================
# Recommendation Engine
# =========================

def recommend_laptops(
    df,
    selected_software,
    selected_budget,
    selected_brand="Any",
    selected_laptop_type="Any",
    top_n=10
):

    recommendations = df.copy()

    # =========================
    # Requirement Match
    # =========================

    recommendations[
        "requirement_match_score"
    ] = recommendations.apply(

        lambda row:
        calculate_overall_requirement_match(
            row,
            selected_software
        ),

        axis=1
    )

    # =========================
    # RAM Match
    # =========================

    required_ram = get_combined_ram_requirement(
        selected_software
    )

    recommendations[
        "ram_match_score"
    ] = recommendations[
        "ram"
    ].apply(

        lambda ram:
        calculate_ram_requirement_match(
            ram,
            required_ram
        )
    )

    # =========================
    # Hardware Score
    # =========================

    recommendations[
        "hardware_score"
    ] = (

        recommendations["cpu_score"] * 0.40

        + recommendations["gpu_score"] * 0.35

        + recommendations["ram_match_score"] * 0.25
    )

    # =========================
    # Budget Score
    # =========================

    recommendations[
        "budget_score"
    ] = recommendations[
        "price"
    ].apply(

        lambda price:
        calculate_budget_score(
            price,
            selected_budget
        )
    )

    # =========================
    # Brand Score
    # =========================

    recommendations[
        "brand_score"
    ] = recommendations[
        "brand"
    ].apply(

        lambda brand:
        calculate_brand_score(
            brand,
            selected_brand
        )
    )

    # =========================
    # Laptop Type Score
    # =========================

    recommendations[
        "type_score"
    ] = recommendations[
        "laptop_category"
    ].apply(

        lambda laptop_type:
        calculate_type_score(
            laptop_type,
            selected_laptop_type
        )
    )

    # =========================
    # Final Score
    # =========================

    recommendations[
        "final_score"
    ] = (

        recommendations[
            "requirement_match_score"
        ] * 0.45

        + recommendations[
            "hardware_score"
        ] * 0.30

        + recommendations[
            "budget_score"
        ] * 0.15

        + recommendations[
            "brand_score"
        ] * 0.05

        + recommendations[
            "type_score"
        ] * 0.05
    )

    # =========================
    # Budget Status
    # =========================

    recommendations[
        "budget_status"
    ] = recommendations[
        "price"
    ].apply(

        lambda price:
        get_budget_status(
            price,
            selected_budget
        )
    )

    # =========================
    # Reasons
    # =========================

    recommendations[
        "reasons"
    ] = recommendations.apply(

        lambda row:
        get_laptop_reasons(
            row,
            selected_software,
            selected_budget
        ),

        axis=1
    )

    # =========================
    # Sort
    # =========================

    recommendations = recommendations.sort_values(
        by="final_score",
        ascending=False
    )

    return recommendations.head(top_n)


# =========================
# Split By Budget
# =========================

def split_by_budget(
    results,
    budget
):

    within_budget = results[
        results["price"] <= budget
    ].copy()

    over_budget = results[
        results["price"] > budget
    ].copy()

    within_budget = within_budget.sort_values(
        by="final_score",
        ascending=False
    )

    over_budget = over_budget.sort_values(
        by="final_score",
        ascending=False
    )

    return within_budget, over_budget


# =========================
# Customer Output
# =========================

def prepare_recommendation_output(
    results,
    budget
):

    output = results.copy()

    output["price"] = (
        output["price"].astype(int)
    )

    output["match_score"] = (
        output["final_score"].round(1)
    )

    output["over_budget_amount"] = (
        output["price"] - budget
    ).clip(lower=0)

    output["reasons"] = (
        output["reasons"].apply(
            lambda x: list(x)
        )
    )

    return output[
        [
            "code",
            "model",
            "ram",
            "cpu",
            "gpu_model",
            "price",
            "match_score",
            "budget_status",
            "over_budget_amount",
            "reasons"
        ]
    ]


# =========================
# Main Recommendation API
# =========================

def get_recommendations(
    df,
    selected_software,
    selected_budget,
    selected_brand="Any",
    selected_laptop_type="Any",
    top_n=5
):

    # Score all laptops first
    all_results = recommend_laptops(

        df=df,

        selected_software=selected_software,

        selected_budget=selected_budget,

        selected_brand=selected_brand,

        selected_laptop_type=selected_laptop_type,

        top_n=len(df)
    )

    # Separate budget results
    within_budget, over_budget = split_by_budget(
        all_results,
        selected_budget
    )

    # Customer output
    within_output = prepare_recommendation_output(

        within_budget.head(top_n),

        selected_budget
    )

    over_output = prepare_recommendation_output(

        over_budget.head(top_n),

        selected_budget
    )

    return {

        "within_budget":
        within_output.to_dict(
            orient="records"
        ),

        "over_budget":
        over_output.to_dict(
            orient="records"
        )
    }


# ============================================================
# Local Test
# ============================================================

if __name__ == "__main__":

    print("\nTesting Recommendation Engine...")

    test_software = [
        "Steam",
        "Fortnite"
    ]

    test_budget = 40000

    test_brand = "Any"

    test_laptop_type = (
        "Gaming / Performance"
    )

    results = get_recommendations(

        df=df,

        selected_software=test_software,

        selected_budget=test_budget,

        selected_brand=test_brand,

        selected_laptop_type=test_laptop_type,

        top_n=5
    )

    print("\n=== WITHIN BUDGET ===")

    for laptop in results[
        "within_budget"
    ]:

        print(
            laptop["code"],
            "|",
            laptop["model"],
            "|",
            laptop["cpu"],
            "|",
            laptop["gpu_model"],
            "|",
            laptop["price"],
            "|",
            laptop["match_score"]
        )

        for reason in laptop["reasons"]:
            print("   -", reason)

    print("\n=== OVER BUDGET ===")

    for laptop in results[
        "over_budget"
    ]:

        print(
            laptop["code"],
            "|",
            laptop["model"],
            "|",
            laptop["cpu"],
            "|",
            laptop["gpu_model"],
            "|",
            laptop["price"],
            "|",
            laptop["match_score"]
        )

        for reason in laptop["reasons"]:
            print("   -", reason)

    print("\nRecommendation Engine test completed!")
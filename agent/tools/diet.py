def calculate_cricket_nutrition(weight_kg: float, height_cm: float, age_years: int, role: str, format_type: str, training_hours: float = 2.0, gender: str = "male") -> dict:
    """
    Calculates tailored nutritional metrics, calories, macronutrients, and hydration
    needs specifically for cricket players based on their role and match format.
    """
    # 1. Calculate Basal Metabolic Rate (BMR) using Harris-Benedict Equation
    if gender.lower() == "female":
        bmr = 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age_years)
    else:
        bmr = 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age_years)

    # 2. Activity Multiplier (Base + Training time)
    # Sedentary base is 1.2
    activity_multiplier = 1.2 + (0.15 * training_hours)
    tdee = bmr * activity_multiplier

    # 3. Role-specific adjustments (Cricket specific workloads)
    role_adjustments = {
        "fast bowler": 450,    # High joint stress, repetitive high-velocity sprints, eccentric load
        "all-rounder": 300,    # High load from both batting and bowling
        "wicketkeeper": 250,   # Constant squatting (up to 600 times a day in Test), high reactive fatigue
        "batter": 150,         # Concentration, running between wickets, explosive batting
        "spinner": 150,        # Rotational load, moderate running, high finger/wrist endurance
    }
    role_key = role.lower().strip()
    role_offset = role_adjustments.get(role_key, 150)
    tdee += role_offset

    # 4. Format-specific adjustments (Cricket formats demand different energy profiles)
    format_adjustments = {
        "test": 600,       # 6+ hours on the field, extreme endurance and cognitive focus
        "odi": 400,        # 7-8 hours duration (entire match), high anaerobic-aerobic blend
        "t20": 200,        # Short, explosive, high-intensity sprints, high peak heart rate
        "training": 300,   # High volume skill practice and gym work
        "recovery": -200,  # Resting/light stretching
    }
    format_key = format_type.lower().strip()
    format_offset = format_adjustments.get(format_key, 200)
    tdee += format_offset

    # Ensure calories are reasonable
    calories = max(1800, int(tdee))

    # 5. Calculate Macros based on Role & Format
    # Bowlers need more protein for tissue repair. Batters need more carbs for long innings.
    if role_key == "fast bowler" or format_key == "recovery":
        # Higher protein target (g/kg)
        protein_g_per_kg = 2.2
        fat_percent_cal = 25
    elif role_key == "batter" or format_key == "test":
        # Higher carb loading
        protein_g_per_kg = 1.8
        fat_percent_cal = 20
    else:
        # Balanced athletic profile
        protein_g_per_kg = 2.0
        fat_percent_cal = 25

    protein_g = int(weight_kg * protein_g_per_kg)
    protein_kcal = protein_g * 4
    
    fat_kcal = int(calories * (fat_percent_cal / 100))
    fat_g = int(fat_kcal / 9)

    carb_kcal = calories - (protein_kcal + fat_kcal)
    carb_g = int(max(50, carb_kcal / 4))

    # Recalculate true calories to match macro weights
    final_calories = (protein_g * 4) + (carb_g * 4) + (fat_g * 9)

    # 6. Hydration Recommendations (ml)
    # Base hydration: 35ml/kg. Training: 1000ml per hour. Cricket extra (due to heavy gear and heat):
    base_hydration = weight_kg * 35
    training_hydration = training_hours * 1000
    cricket_gear_sweat_offset = 500 if role_key == "fast bowler" or role_key == "wicketkeeper" else 300
    hydration_ml = int(base_hydration + training_hydration + cricket_gear_sweat_offset)

    # 7. Food Group Recommendations
    recommended_foods = {
        "proteins": ["Chicken Breast", "Salmon/Tuna", "Eggs", "Whey Protein", "Greek Yogurt", "Cottage Cheese (Paneer)", "Lentils (Dals)", "Chickpeas"],
        "carbs": ["Basmati Rice", "Sweet Potatoes", "Oats", "Quinoa", "Whole Wheat Roti/Bread", "Bananas", "Berries"],
        "fats": ["Almonds/Walnuts", "Avocados", "Chia Seeds/Flax Seeds", "Extra Virgin Olive Oil", "Peanut Butter"],
        "supplements": ["Creatine Monohydrate (for power)", "Omega-3 Fish Oil (joint inflammation)", "Vitamin D3 (bone density)", "Electrolyte Replacement (during long match sessions)"]
    }

    # Custom advice
    if role_key == "fast bowler":
        advice = "Focus on high-quality proteins and anti-inflammatory fats (omega-3s) to speed up recovery of knee, ankle, and shoulder joints. Consume electrolyte drinks during spells."
    elif role_key == "wicketkeeper":
        advice = "Ensure high hip and knee mobility. Focus on collagen-rich foods or vitamin C to support joints from constant squatting. Keep meals light before fielding to maintain agility."
    elif role_key == "batter":
        advice = "Carb-loading is essential prior to long days (Test/ODI) to prevent cognitive decline and fatigue. Consume fast-acting carbs (bananas, energy gels) during drinks breaks."
    else:
        advice = "Maintain a steady baseline of complex carbohydrates for enduring skill-work sessions, coupled with protein distributed throughout the day (every 3-4 hours)."

    return {
        "calories": final_calories,
        "protein": {
            "grams": protein_g,
            "calories": protein_g * 4,
            "percentage": int((protein_g * 4 / final_calories) * 100)
        },
        "carbohydrates": {
            "grams": carb_g,
            "calories": carb_g * 4,
            "percentage": int((carb_g * 4 / final_calories) * 100)
        },
        "fats": {
            "grams": fat_g,
            "calories": fat_g * 9,
            "percentage": int((fat_g * 9 / final_calories) * 100)
        },
        "hydration_liters": round(hydration_ml / 1000, 2),
        "recommended_foods": recommended_foods,
        "role_specific_advice": advice
    }

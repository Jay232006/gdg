def calculate_acwr(daily_workloads: list) -> dict:
    """
    Calculates the Acute-to-Chronic Workload Ratio (ACWR) for injury prevention.
    Input: list of daily workload values (e.g., RPE * duration in minutes, or overs bowled) for the last 28 days.
    If less than 28 days of data are provided, we extrapolate or warn the user.
    """
    # Pad list to 28 elements if not long enough (default to 0 or average)
    if len(daily_workloads) < 7:
        return {
            "status": "error",
            "message": "At least 7 days of workload data is required to calculate acute workload."
        }
    
    # Ensure values are float
    workloads = [float(w) for w in daily_workloads]
    
    # If list is shorter than 28 days, pad it with the average of existing values to simulate chronic workload
    if len(workloads) < 28:
        avg_w = sum(workloads) / len(workloads)
        workloads = [avg_w] * (28 - len(workloads)) + workloads

    # Get last 28 days
    workloads = workloads[-28:]

    # Acute Workload = sum of last 7 days
    acute_workload = sum(workloads[-7:])
    
    # Chronic Workload = average weekly workload over 4 weeks
    week4 = sum(workloads[-7:])
    week3 = sum(workloads[-14:-7])
    week2 = sum(workloads[-21:-14])
    week1 = sum(workloads[-28:-21])
    
    chronic_workload = (week1 + week2 + week3 + week4) / 4

    if chronic_workload == 0:
        acwr = 0.0
    else:
        acwr = round(acute_workload / chronic_workload, 2)

    # Determine status and risk profile
    if acwr < 0.8:
        zone = "Under-training Zone"
        risk = "Low current injury risk, but high risk if load is rapidly increased. Player is losing cricket fitness."
        color = "#e2e8f0"  # Gray
        status_key = "under"
    elif 0.8 <= acwr <= 1.3:
        zone = "Sweet Spot"
        risk = "Optimal training load. Low injury risk. Player is building fitness and performance safely."
        color = "#10b981"  # Green
        status_key = "optimal"
    elif 1.3 < acwr <= 1.5:
        zone = "Buffer Zone"
        risk = "Moderate injury risk. Monitor fatigue levels. Avoid any sudden increases in training volume."
        color = "#f59e0b"  # Amber
        status_key = "buffer"
    else:  # acwr > 1.5
        zone = "Danger Zone / Injury Red Zone"
        risk = "High injury risk! Training load is growing too fast. Immediate reduction in bowling/sprinting volume and focus on recovery is required."
        color = "#ef4444"  # Red
        status_key = "danger"

    return {
        "status": "success",
        "acute_workload": round(acute_workload, 1),
        "chronic_workload": round(chronic_workload, 1),
        "acwr": acwr,
        "zone": zone,
        "risk_description": risk,
        "color_code": color,
        "status_key": status_key,
        "weekly_breakdown": {
            "week_1_chronic": round(week1, 1),
            "week_2_chronic": round(week2, 1),
            "week_3_chronic": round(week3, 1),
            "week_4_acute": round(week4, 1),
        }
    }

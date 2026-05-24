from agent.engine import CricketHealthAgent

def run_test():
    print("Initializing CricketHealthAgent...")
    agent = CricketHealthAgent()
    
    # Test case 1: Fast bowler diet query
    profile = {
        "role": "Fast Bowler",
        "weight": 85.0,
        "height": 185.0,
        "age": 25,
        "format_type": "Test",
        "active_injury": "None",
        "sleep_hours": 8.0,
        "soreness_level": 3,
        "fatigue_level": 3,
        "training_hours": 3.0
    }
    
    # Simple history of workloads showing sweet spot
    history = [12.0] * 28 
    
    print("\n--- TEST CASE 1: DIET QUERY ---")
    query = "What should I eat to stay in top shape?"
    res = agent.run(profile, history, query)
    print(f"User Query: {query}")
    print(f"Coach Response:\n{res['response'][:300]}...\n")
    assert "Protein:" in res['response']
    assert "Carbohydrates:" in res['response']
    
    # Test case 2: Shoulder injury rehab lookup
    print("\n--- TEST CASE 2: REHAB QUERY ---")
    profile["active_injury"] = "shoulder_impingement"
    query = "How do I recover from my shoulder pain?"
    res = agent.run(profile, history, query)
    print(f"User Query: {query}")
    print(f"Coach Response:\n{res['response'][:300]}...\n")
    assert "Rehabilitation Guide" in res['response'] or "shoulder" in res['response'].lower()
    
    # Test case 3: Danger Zone ACWR Workload Warning
    print("\n--- TEST CASE 3: ACWR WORKLOAD QUERY ---")
    profile["active_injury"] = "None"
    # Seed high workloads for last 7 days to trigger danger zone (> 1.5)
    # Chronic load is 10 per day = 70 per week
    # Acute load is 30 per day = 210 per week -> ACWR = 3.0
    danger_history = [10.0] * 21 + [30.0] * 7
    query = "Audit my training workload risk"
    res = agent.run(profile, danger_history, query)
    print(f"User Query: {query}")
    print(f"Coach Response:\n{res['response'][:350]}...\n")
    assert "Danger Zone" in res['response'] or "ACWR" in res['response']
    
    print("\nAll isolated agent tests passed successfully! Fallback system functions correctly.")

if __name__ == "__main__":
    run_test()

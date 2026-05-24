INJURY_REHAB_DATABASE = {
    "shoulder_impingement": {
        "name": "Shoulder Impingement / Rotator Cuff Tendinopathy",
        "description": "Inflammation of rotator cuff tendons, highly prevalent in bowlers (overhead action) and fielders (high-velocity throwing).",
        "phases": [
            {
                "phase_name": "Phase 1: Pain Reduction & Passive Range of Motion",
                "duration": "Weeks 1-2",
                "goals": ["Reduce active inflammation", "Restore basic movement without load"],
                "exercises": [
                    {"name": "Pendulum Swings", "sets": 3, "reps": 10, "notes": "Let arm hang loose and swing in circles using torso movement."},
                    {"name": "Sleeper Stretch", "sets": 3, "reps": "30 sec hold", "notes": "Side-lying stretch targeting the posterior capsule of shoulder."},
                    {"name": "Scapular Squeezes", "sets": 3, "reps": 15, "notes": "Squeeze shoulder blades together; hold for 5 seconds."}
                ],
                "milestone": "Full pain-free range of motion below 90 degrees."
            },
            {
                "phase_name": "Phase 2: Active Isometric & Scapular Control",
                "duration": "Weeks 3-4",
                "goals": ["Build shoulder blade stability", "Low level muscle activation"],
                "exercises": [
                    {"name": "Wall Slides", "sets": 3, "reps": 10, "notes": "Slide forearms up the wall in a 'V' shape, engaging serratus anterior."},
                    {"name": "Shoulder External Rotation (Isometric)", "sets": 3, "reps": "10 sec holds", "notes": "Push back of hand against a wall outwards without moving the arm."},
                    {"name": "Prone T/Y raises", "sets": 3, "reps": 12, "notes": "Lay face down, raise arms to form 'T' and 'Y' shapes to strengthen traps."}
                ],
                "milestone": "Ability to raise arm overhead without pain."
            },
            {
                "phase_name": "Phase 3: Dynamic Strengthening & Throwing Prep",
                "duration": "Weeks 5-8",
                "goals": ["Progressive overload", "Rotational strength", "Eccentric rotator cuff stability"],
                "exercises": [
                    {"name": "Banded Internal/External Rotation", "sets": 3, "reps": 15, "notes": "Use light resistance band with elbow tucked to side at 90 degrees."},
                    {"name": "Face Pulls with Band", "sets": 3, "reps": 15, "notes": "Pull band towards face, separating hands, squeezing posterior deltoids."},
                    {"name": "Weighted Deceleration Catches", "sets": 3, "reps": 10, "notes": "Catch a light medicine ball and slow down its momentum, simulating throwing deceleration."}
                ],
                "milestone": "Ready to initiate light underarm throwing progression."
            }
        ],
        "cricket_return_to_play": "Gradual throwing schedule starting at 10m (underarm), progressing to 30m overhand, then bowling at 50% effort."
    },
    "lower_back_stress_fracture": {
        "name": "Lower Back Stress Fracture (Pars Interarticularis)",
        "description": "Bone stress injury in the lumbar spine, typical in young fast bowlers due to extreme hyperextension, rotation, and ground impact forces.",
        "phases": [
            {
                "phase_name": "Phase 1: Spine Neutral & Core Activation",
                "duration": "Weeks 1-4",
                "goals": ["Protect spine alignment", "Core activation without flexion/extension", "Cardio via non-impact (swimming/recumbent bike)"],
                "exercises": [
                    {"name": "Deadbugs", "sets": 3, "reps": 12, "notes": "Keep lower back glued flat to the floor as you extend opposite arm/leg."},
                    {"name": "Bird-Dog", "sets": 3, "reps": 10, "notes": "Maintain flat table-top back while extending opposite arm and leg."},
                    {"name": "Glute Bridges", "sets": 3, "reps": 15, "notes": "Drive through heels, squeeze glutes at top, keep spine neutral."}
                ],
                "milestone": "Zero pain during daily walking or static standing."
            },
            {
                "phase_name": "Phase 2: Hip/Thoracic Spine Mobility & Core Progression",
                "duration": "Weeks 5-10",
                "goals": ["Address structural compensation", "Improve thoracic mobility to spare lower spine"],
                "exercises": [
                    {"name": "Thoracic Openers (Book Openers)", "sets": 3, "reps": 10, "notes": "Side-lying, rotate upper trunk and arm away while keeping knees together."},
                    {"name": "Pallof Press (Banded)", "sets": 3, "reps": 12, "notes": "Anti-rotation core hold. Push band forward from chest, resist rotation."},
                    {"name": "Plank (Forearms)", "sets": 3, "reps": "30 sec hold", "notes": "Engage abs and glutes, do not let lower back sag."}
                ],
                "milestone": "Full pain-free range of motion in thoracic spine and hips."
            },
            {
                "phase_name": "Phase 3: Rotational Strength & Return to Bowling Prep",
                "duration": "Weeks 11-16+",
                "goals": ["Re-introduce light bowling rotation", "Rebuild explosive power safely"],
                "exercises": [
                    {"name": "Half-Kneeling Woodchops (Cable/Band)", "sets": 3, "reps": 10, "notes": "Pull diagonally across body under control, keeping hips locked straight."},
                    {"name": "Trapbar Deadlifts (Light)", "sets": 3, "reps": 8, "notes": "Build posterior chain strength to absorb bowling landing forces."},
                    {"name": "Medicine Ball Chest Passes", "sets": 3, "reps": 10, "notes": "Explosive linear chest pass from standing position to build core transfer."}
                ],
                "milestone": "Approval from specialist, completion of bowling workload progression program."
            }
        ],
        "cricket_return_to_play": "Strict bowling restrictions: Begin with walk-up releases (1 over), then run-up bowling at 40% speed, gradually increasing overs by 10% per week."
    },
    "side_strain": {
        "name": "Intercostal/Oblique Side Strain",
        "description": "Tear of internal oblique or transversalis fascia on the non-bowling side, caused by sudden lateral flexion and rotation at ball release.",
        "phases": [
            {
                "phase_name": "Phase 1: Acute Protection & Core Splinting",
                "duration": "Weeks 1-2",
                "goals": ["Avoid twisting and stretching the injured side", "Allow muscle tear to heal"],
                "exercises": [
                    {"name": "Diaphragmatic Breathing", "sets": 1, "reps": "5 mins", "notes": "Deep abdominal breathing to prevent stiffness without straining muscle fibers."},
                    {"name": "Standing Core Holds (Isometric)", "sets": 3, "reps": "15 sec", "notes": "Lightly brace abs as if about to be punched, holding posture."},
                    {"name": "Clamshells", "sets": 3, "reps": 15, "notes": "Lying on side, open knees apart to keep hips active without trunk load."}
                ],
                "milestone": "Zero pain with normal deep breathing, coughing, or laughing."
            },
            {
                "phase_name": "Phase 2: Linear Loading & Gentle Rotation",
                "duration": "Weeks 3-5",
                "goals": ["Introduce linear core load", "Gentle rotational range of motion"],
                "exercises": [
                    {"name": "Side Plank (Knees)", "sets": 3, "reps": "20 sec hold", "notes": "Support weight on knees and forearm, hold side core rigid without twisting."},
                    {"name": "Swiss Ball Neutral Rolls", "sets": 3, "reps": 10, "notes": "Sit on Swiss ball, gently roll hips forward/backward keeping torso neutral."},
                    {"name": "Seated Rotational Mobilization", "sets": 3, "reps": 8, "notes": "Hug a pillow, rotate trunk to 50% range of motion, return to center. Pain-free."}
                ],
                "milestone": "Zero discomfort during side-plank holds or light jogging."
            },
            {
                "phase_name": "Phase 3: Explosive Rotation & Bowling Sim",
                "duration": "Weeks 6-8",
                "goals": ["Rebuild high-velocity stretch shortening cycle", "Bowling-specific fitness"],
                "exercises": [
                    {"name": "Standing Oblique Cable Twist (Light)", "sets": 3, "reps": 12, "notes": "Controlled twist away from pulley, focusing on abdominal bracing."},
                    {"name": "Single-Leg Balance & Catch", "sets": 3, "reps": 15, "notes": "Catch tennis ball from a partner while balancing on one leg to test reflexive stability."},
                    {"name": "Dynamic Side Bends (Banded)", "sets": 3, "reps": 10, "notes": "Banded lateral flexion away from anchor, slow eccentric return."}
                ],
                "milestone": "Sprinting at 100% and dynamic throwing/twisting without pain."
            }
        ],
        "cricket_return_to_play": "Start bowling off a short run-up (50% intensity). Maximum of 2 overs on day 1, followed by 48 hours of rest/monitoring."
    },
    "hamstring_strain": {
        "name": "Hamstring Muscle Strain",
        "description": "Tear of hamstring fibers, frequent in cricket during rapid acceleration (sprinting for catches, quick runs) and high knee-up actions (bowling).",
        "phases": [
            {
                "phase_name": "Phase 1: Early Loading & Walking Gait",
                "duration": "Weeks 1",
                "goals": ["Prevent scar tissue accumulation", "Maintain low load activation"],
                "exercises": [
                    {"name": "Standing Hamstring Curls (Bodyweight)", "sets": 3, "reps": 15, "notes": "Slowly bend knee bringing heel to glute; control down."},
                    {"name": "Glute Bridge with Hamstring Walkouts", "sets": 3, "reps": 5, "notes": "From bridge position, walk feet out 2-3 inches, hold, walk back."},
                    {"name": "Straight Leg Raises (Passive)", "sets": 3, "reps": 10, "notes": "Lay on back, raise leg using a towel around foot to stretch hamstring gently."}
                ],
                "milestone": "Normal walking gait without pain."
            },
            {
                "phase_name": "Phase 2: Strength & Eccentric Control",
                "duration": "Weeks 2-4",
                "goals": ["Build eccentric hamstring capacity (crucial for sprinting)", "Knee flexion strength"],
                "exercises": [
                    {"name": "Romanian Deadlifts (Dumbbells)", "sets": 3, "reps": 10, "notes": "Hinge at hips, keep back flat, lower weights along legs to mid-shin."},
                    {"name": "Sliders / Swiss Ball Hamstring Curls", "sets": 3, "reps": 12, "notes": "In bridge position, pull heels in towards glutes on sliding surface or ball."},
                    {"name": "Single-Leg Glute Bridge", "sets": 3, "reps": 10, "notes": "Lift hips off floor using only the injured side foot, hold 2 seconds."}
                ],
                "milestone": "Eccentric strength within 90% of uninjured leg."
            },
            {
                "phase_name": "Phase 3: High-Velocity Running & Plyometrics",
                "duration": "Weeks 5-6",
                "goals": ["Sprinting acceleration", "Deceleration and rapid turning drills"],
                "exercises": [
                    {"name": "Nordic Hamstring Curls", "sets": 3, "reps": 5, "notes": "Kneeling, heels held by partner, lower chest to floor as slowly as possible."},
                    {"name": "Kettlebell Swings", "sets": 3, "reps": 15, "notes": "Dynamic hip hinges to build rapid contraction energy in hamstrings/glutes."},
                    {"name": "A-Skips & B-Skips", "sets": 3, "reps": "20m", "notes": "Track drills focusing on active hamstring leg sweep and hip drive."}
                ],
                "milestone": "Full sprinting capacity at 100% velocity."
            }
        ],
        "cricket_return_to_play": "Complete cricket running test (runs of 3 runs, turning on alternate legs). Start batting in nets, progress to running between wickets in match simulation."
    }
}


def get_cricket_rehab_guide(injury_key: str) -> dict:
    """
    Returns rehabilitation program, exercises, and milestones for a given cricket injury.
    """
    key = injury_key.lower().strip().replace(" ", "_")
    
    # Fuzzy match basic keys
    if "shoulder" in key or "rotator" in key:
        key = "shoulder_impingement"
    elif "back" in key or "stress" in key or "spine" in key or "pars" in key:
        key = "lower_back_stress_fracture"
    elif "side" in key or "oblique" in key or "strain" in key and "hamstring" not in key:
        key = "side_strain"
    elif "hamstring" in key or "leg" in key or "thigh" in key:
        key = "hamstring_strain"
        
    injury = INJURY_REHAB_DATABASE.get(key)
    if not injury:
        return {
            "status": "error",
            "message": f"Injury guide for '{injury_key}' not found. Try 'shoulder_impingement', 'lower_back_stress_fracture', 'side_strain', or 'hamstring_strain'."
        }
        
    return {
        "status": "success",
        "key": key,
        **injury
    }

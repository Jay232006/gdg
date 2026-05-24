import json
from agent.config import GEMINI_API_KEY
from agent.prompts import SYSTEM_PROMPT, USER_QUERY_TEMPLATE
from agent.tools.diet import calculate_cricket_nutrition
from agent.tools.workload import calculate_acwr
from agent.tools.rehab import get_cricket_rehab_guide

# Try importing google generativeai, catch import error if package is missing
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

class CricketHealthAgent:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.use_llm = HAS_GENAI and bool(self.api_key)
        
        if self.use_llm:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=SYSTEM_PROMPT
                )
            except Exception as e:
                print(f"Failed to configure Gemini LLM: {e}. Falling back to rule-based engine.")
                self.use_llm = False

    def run(self, profile: dict, wellness_history: list, user_inquiry: str) -> dict:
        """
        Executes the agent reasoning loop.
        1. Runs local tools based on player profile and input data.
        2. Merges tool outputs.
        3. Invokes Gemini (if available) or Fallback Engine to synthesize a final personalized report/chat response.
        """
        # Parse profile details
        weight = float(profile.get("weight", 75))
        height = float(profile.get("height", 178))
        age = int(profile.get("age", 24))
        role = profile.get("role", "All-rounder").strip()
        format_type = profile.get("format_type", "ODI").strip()
        active_injury = profile.get("active_injury", "None").strip()
        
        # Parse wellness/activity details
        sleep_hours = float(profile.get("sleep_hours", 8))
        soreness_level = int(profile.get("soreness_level", 2))
        fatigue_level = int(profile.get("fatigue_level", 2))
        training_hours = float(profile.get("training_hours", 2.0))
        
        # 1. Run Diet Tool automatically
        diet_data = calculate_cricket_nutrition(
            weight_kg=weight,
            height_cm=height,
            age_years=age,
            role=role,
            format_type=format_type,
            training_hours=training_hours
        )

        # 2. Run ACWR Tool if wellness history is present
        acwr_data = {}
        if wellness_history:
            # wellness_history is a list of daily workloads
            acwr_data = calculate_acwr(wellness_history)
        else:
            # Fallback workload using current training hours
            # Workload = training hours * RPE (relative rate of perceived exertion, say 6)
            mock_history = [training_hours * 6.0] * 7
            acwr_data = calculate_acwr(mock_history)

        # 3. Run Rehab Tool if active injury is specified
        rehab_data = {}
        if active_injury and active_injury.lower() != "none":
            rehab_data = get_cricket_rehab_guide(active_injury)

        # Format context for generator
        tools_context = {
            "nutrition_calculator_output": diet_data,
            "workload_acwr_output": acwr_data,
            "injury_rehabilitaton_output": rehab_data
        }

        # 4. Synthesize final response
        if self.use_llm:
            response_text = self._run_llm(profile, tools_context, user_inquiry)
        else:
            response_text = self._run_fallback(profile, tools_context, user_inquiry)

        return {
            "response": response_text,
            "tool_data": tools_context
        }

    def _run_llm(self, profile: dict, tools_context: dict, user_inquiry: str) -> str:
        """Calls the Gemini LLM with context injected."""
        prompt = USER_QUERY_TEMPLATE.format(
            role=profile.get("role", "All-rounder"),
            weight=profile.get("weight", 75),
            height=profile.get("height", 178),
            age=profile.get("age", 24),
            format_type=profile.get("format_type", "ODI"),
            active_injury=profile.get("active_injury", "None"),
            sleep_hours=profile.get("sleep_hours", 8),
            soreness_level=profile.get("soreness_level", 2),
            fatigue_level=profile.get("fatigue_level", 2),
            training_hours=profile.get("training_hours", 2.0),
            workload_metric=tools_context["workload_acwr_output"].get("acwr", "N/A"),
            user_inquiry=user_inquiry
        )

        full_prompt = f"""
{prompt}

[SUPPLEMENTAL TOOLS DATA INJECTED BY SYSTEM]
- Nutrition & Diet Targets: {json.dumps(tools_context['nutrition_calculator_output'])}
- Injury Rehabilitation Steps: {json.dumps(tools_context['injury_rehabilitaton_output'])}
- Workload ACWR Metrics: {json.dumps(tools_context['workload_acwr_output'])}

Synthesize a comprehensive, personalized response answering the user's inquiry directly. Refer to the computed calculations (e.g. caloric target, ACWR zone, or rehab stages) where appropriate to justify your professional guidance. Maintain a supportive, elite coaching tone.
"""
        try:
            res = self.model.generate_content(full_prompt)
            return res.text
        except Exception as e:
            print(f"Gemini API execution error: {e}. Falling back to rule-based response.")
            return self._run_fallback(profile, tools_context, user_inquiry)

    def _run_fallback(self, profile: dict, tools_context: dict, user_inquiry: str) -> str:
        """Smart expert rules-based chatbot response generator."""
        query = user_inquiry.lower()
        role = profile.get("role", "All-rounder")
        injury = profile.get("active_injury", "None")
        
        diet_data = tools_context["nutrition_calculator_output"]
        rehab_data = tools_context["injury_rehabilitaton_output"]
        acwr_data = tools_context["workload_acwr_output"]

        # Diet / Nutrition Intent
        if any(w in query for w in ["diet", "eat", "food", "nutrition", "calorie", "protein", "carb", "fat", "hydration"]):
            res = f"### 🏏 Cricketer Nutrition Plan - {role}\n\n"
            res += f"Hello Athlete! Based on your role as a **{role}** and target format **{profile.get('format_type')}**, here are your personalized nutritional targets to optimize recovery and stamina:\n\n"
            res += f"#### Daily Targets:\n"
            res += f"- **Target Calories:** {diet_data['calories']} kcal\n"
            res += f"- **Protein:** {diet_data['protein']['grams']}g ({diet_data['protein']['percentage']}% of daily intake) for muscle/joint repair\n"
            res += f"- **Carbohydrates:** {diet_data['carbohydrates']['grams']}g ({diet_data['carbohydrates']['percentage']}%) for glycogen storage\n"
            res += f"- **Fats:** {diet_data['fats']['grams']}g ({diet_data['fats']['percentage']}%) for joint health and hormone levels\n"
            res += f"- **Hydration Intake:** {diet_data['hydration_liters']} Liters per day\n\n"
            res += f"#### Role Specific Coaching Tip:\n"
            res += f"> 💡 {diet_data['role_specific_advice']}\n\n"
            res += f"#### Recommended Food Groups:\n"
            res += f"- **Proteins:** {', '.join(diet_data['recommended_foods']['proteins'])}\n"
            res += f"- **Carbs:** {', '.join(diet_data['recommended_foods']['carbs'])}\n"
            res += f"- **Healthy Fats:** {', '.join(diet_data['recommended_foods']['fats'])}\n"
            res += f"- **Suggested Supplements:** {', '.join(diet_data['recommended_foods']['supplements'])}\n\n"
            res += "_Would you like me to outline a structured sample meal plan for a match day?_"
            return res

        # Injury / Rehab Intent
        if any(w in query for w in ["rehab", "injury", "recover", "hurt", "pain", "back", "shoulder", "strain", "hamstring"]):
            if rehab_data and rehab_data.get("status") == "success":
                res = f"### 🩺 Rehabilitation Guide: {rehab_data['name']}\n\n"
                res += f"**Condition Description:** {rehab_data['description']}\n\n"
                res += f"Here is your structured recovery path. You are currently starting at **Phase 1**:\n\n"
                
                for phase in rehab_data["phases"]:
                    res += f"#### 📈 {phase['phase_name']} ({phase['duration']})\n"
                    res += f"- **Goals:** {', '.join(phase['goals'])}\n"
                    res += f"- **Milestone:** {phase['milestone']}\n"
                    res += f"- **Exercises:**\n"
                    for ex in phase["exercises"]:
                        res += f"  - **{ex['name']}**: {ex['sets']} sets x {ex['reps']} ({ex['notes']})\n"
                    res += "\n"

                res += f"#### 🏏 Return to Play Protocol:\n"
                res += f"> ⚠️ **Workload Progression:** {rehab_data['cricket_return_to_play']}\n\n"
                res += "_Disclaimer: Please immediately stop if you feel sharp pain, and coordinate with your team physiotherapist._"
                return res
            else:
                res = "### 🩺 Injury & Recovery Assessment\n\n"
                res += f"I see you are asking about injury recovery. You currently have '{injury}' listed as your active injury.\n\n"
                res += "Here are the key cricket injuries I can provide full rehabilitation programs for:\n"
                res += "1. **Shoulder Impingement / Rotator Cuff** (Common from bowling or fielding throws)\n"
                res += "2. **Lower Back Stress Fracture** (Common in fast bowlers due to spine arching)\n"
                res += "3. **Side Strain** (Oblique tear on the non-bowling side)\n"
                res += "4. **Hamstring Strain** (Sprinting or sudden bending)\n\n"
                res += "Please update your **Active Injury** dropdown in the dashboard to load a specific guide, or reply with the injury name, and I will display the exercise schedule!"
                return res

        # Workload / ACWR Intent
        if any(w in query for w in ["workload", "acwr", "overs", "training", "bowling", "intensity"]):
            res = f"### 📊 Workload & Injury Risk Analysis (ACWR)\n\n"
            res += f"Your Acute-to-Chronic Workload Ratio (ACWR) is **{acwr_data['acwr']}**.\n\n"
            res += f"#### Analysis:\n"
            res += f"- **Training Zone:** `{acwr_data['zone']}`\n"
            res += f"- **Injury Risk Profile:** {acwr_data['risk_description']}\n"
            res += f"- **Acute Load (Last 7 Days):** {acwr_data['acute_workload']} units\n"
            res += f"- **Chronic Load (Last 28 Days Avg):** {acwr_data['chronic_workload']} units\n\n"
            
            if acwr_data["status_key"] == "danger":
                res += "> 🚨 **Urgent Coach Recommendation:** Your workload is increasing too fast (ACWR > 1.5). You need to immediately cut your training/bowling volume by 30-50% this week. Focus on active mobility, hydration, and sleep to prevent a stress injury.\n"
            elif acwr_data["status_key"] == "optimal":
                res += "> ✅ **Coach Recommendation:** You are in the training 'Sweet Spot' (0.8 - 1.3). Your body is adapting well. You can maintain this volume or introduce small 5-10% weekly progressions in bowling/intensity.\n"
            elif acwr_data["status_key"] == "under":
                res += "> ⚠️ **Coach Recommendation:** You are under-training. While current injury risk is low, your cricket-specific fitness is declining. If you have an upcoming match, do not jump straight into maximum intensity; build up your bowling overs gradually to avoid shoulder or side strain.\n"
            else:
                res += "> ⚠️ **Coach Recommendation:** You are in the buffer zone. Keep training volume flat. Do not add extra bowling spells or sprinting intervals.\n"
                
            return res

        # Default / Catch-all response
        res = f"### 🏏 Welcome to CrickHealth AI, Coach Room!\n\n"
        res += f"Hey Player! I am your specialized cricket health coach. I see you are a **{role}** playing **{profile.get('format_type')}** matches.\n\n"
        res += f"Here is how we can optimize your performance and prevent injury today:\n\n"
        res += f"1. **Diet Plan:** Ask me: *'What should I eat?'* or *'Show my macro guidelines'* to get role-based caloric, protein, and water targets.\n"
        res += f"2. **Injury Rehabilitation:** Ask me: *'How do I recover from a side strain?'* or *'Shoulder pain exercises'* to see a full rehabilitation schedule.\n"
        res += f"3. **Workload Analysis:** Ask me: *'Check my injury risk'* or *'What is my ACWR?'* to audit your recent training loads.\n\n"
        res += f"_Feel free to ask a question, log a symptom, or request a specific routine!_"
        return res

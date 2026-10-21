import streamlit as st
import json
import time
from models.schemas import DestinationResearch, TravelItinerary
from datetime import date, timedelta
from crew import create_travel_crew
from utils.validators import validate_travel_inputs
from utils.error_handler import handle_application_error

# Page configuration
st.set_page_config(
    page_title="Two-Agent Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# Application title
st.title("🌍 Two-Agent AI Travel Planner")

st.write(
    "Plan your perfect trip using AI-powered destination "
    "research and personalized itinerary generation."
)

st.divider()

# Travel input form
st.subheader("✈️ Enter Your Travel Details")

with st.form("travel_form"):

    destination = st.text_input(
        "📍 Destination",
        placeholder="e.g., Jaipur, Rajasthan"
    )

    col1, col2 = st.columns(2)

    with col1:
        start_date = st.date_input(
            "📅 Start Date",
            value=date.today() + timedelta(days=7),
            min_value=date.today()
        )

    with col2:
        end_date = st.date_input(
            "📅 End Date",
            value=date.today() + timedelta(days=8),
            min_value=date.today()
        )

    col3, col4 = st.columns(2)

    with col3:
        budget = st.number_input(
            "💰 Total Budget (₹)",
            min_value=100,
            value=10000,
            step=500
        )

    with col4:
        travelers = st.number_input(
            "👥 Number of Travelers",
            min_value=1,
            max_value=20,
            value=2,
            step=1
        )

    preferences = st.multiselect(
        "❤️ Travel Preferences",
        [
            "History",
            "Nature",
            "Adventure",
            "Photography",
            "Local Food",
            "Shopping",
            "Culture",
            "Wildlife",
            "Relaxation",
            "Architecture"
        ],
        default=["History", "Local Food"]
    )

    submitted = st.form_submit_button(
        "🚀 Generate My Itinerary",
        use_container_width=True
    )

# Input validation
if submitted:

    if not destination.strip():
        st.error("Please enter a destination.")

    elif end_date < start_date:
        st.error("End date cannot be earlier than start date.")

    elif not preferences:
        st.error("Please select at least one travel preference.")

    else:
        travel_dates = (
            f"{start_date.strftime('%d %B %Y')} - "
            f"{end_date.strftime('%d %B %Y')}"
        )

        # Convert preferences into a string
        preferences_text = ", ".join(preferences)

        # Display submitted details
        st.success("Travel details submitted successfully!")

        st.write("### Your Travel Details")

        st.write(f"**Destination:** {destination}")
        st.write(f"**Travel Dates:** {travel_dates}")
        st.write(f"**Budget:** ₹{budget:,}")
        st.write(f"**Travelers:** {travelers}")
        st.write(f"**Preferences:** {preferences_text}")

        # ==========================================
        # EXECUTE TWO-AGENT TRAVEL PLANNER
        # ==========================================

        # Clear previous results before generating a new trip
        st.session_state.pop("itinerary", None)
        st.session_state.pop("research", None)

        try:
            # Initialize both agents
            with st.status(
                "🤖 Preparing your AI travel planner...",
                expanded=True
            ) as status:

                st.write("⚙️ Initializing AI agents...")
                
                validate_travel_inputs(
                    destination=destination,
                    budget=budget,
                    start_date=start_date,
                    end_date=end_date,
                    travelers=travelers,
                    preferences=preferences_text
                )

                travel_crew = create_travel_crew(
                    destination=destination,
                    budget=budget,
                    travel_dates=travel_dates,
                    travelers=travelers,
                    preferences=preferences_text
                )

                st.write("🔍 Researching destination and planning itinerary...")

                # Execute the sequential CrewAI workflow
                start_time = time.perf_counter()
                result = travel_crew.kickoff()
                execution_time = time.perf_counter() - start_time

                # Validate final output
                if not result.raw or not result.raw.strip():
                    raise ValueError(
                        "The AI agents returned an empty itinerary."
                    )

                # Store itinerary
                # Retrieve Agent 1 research
                research_output = travel_crew.tasks[0].output

                # Validate structured outputs before saving anything
                if not isinstance(result.pydantic, TravelItinerary):
                    raise ValueError("Agent 2 did not return a valid structured itinerary.")

                if (
                    research_output is None
                    or not isinstance(research_output.pydantic, DestinationResearch)
                ):
                    raise ValueError("Agent 1 did not return valid structured research.")

                # Store successful results together
                st.session_state["itinerary"] = result.raw
                st.session_state["research"] = research_output.raw

                st.session_state["structured_itinerary"] = (
                    result.pydantic.model_dump(mode="json")
                )

                st.session_state["structured_research"] = (
                    research_output.pydantic.model_dump(mode="json")
                )
                
                st.session_state["execution_time"] = execution_time
                
                status.update(
                    label="✅ Travel planning completed!",
                    state="complete",
                    expanded=False
                )

            st.success("🎉 Your personalized itinerary is ready!")

        except Exception as error:

            # Convert technical errors into user-friendly messages
            friendly_message = handle_application_error(error)

            st.error(f"❌ {friendly_message}")

            st.warning(
                "Please verify your inputs or try again after a few minutes."
            )

            # Show technical details for debugging
            with st.expander("🔧 View Error Details"):
                st.code(type(error).__name__)

            # Preserve the previous successful itinerary
            st.info(
                "Your previous itinerary, if available, "
                "has been preserved."
            )
            st.session_state.pop("itinerary", None)
            st.session_state.pop("research", None)

# ==========================================
# DISPLAY GENERATED TRAVEL RESULTS
# ==========================================

if "structured_itinerary" in st.session_state:

    itinerary = TravelItinerary.model_validate(
        st.session_state["structured_itinerary"]
    )

    research = DestinationResearch.model_validate(
        st.session_state["structured_research"]
    )

    st.divider()
    st.header("🌍 Your Personalized Travel Plan")

    # ==========================================
    # TRIP OVERVIEW
    # ==========================================
    if "execution_time" in st.session_state:
        st.caption(
            f"⚡ AI planning completed in "
            f"{st.session_state['execution_time']:.2f} seconds"
        )
    st.subheader("📌 Trip Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📍 Destination", itinerary.destination)
    col2.metric("📅 Days", len(itinerary.days))
    col3.metric("👥 Travelers", itinerary.travelers)
    col4.metric("💰 Budget", f"₹{itinerary.total_budget:,.0f}")

    st.caption(
        f"Travel Dates: {itinerary.start_date} to {itinerary.end_date}"
    )

    # ==========================================
    # MAIN TABS
    # ==========================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "🗓️ Day-Wise Itinerary",
        "💰 Budget Breakdown",
        "🔍 Destination Research",
        "📥 Downloads"
    ])

    # ==========================================
    # TAB 1: DAY-WISE ITINERARY
    # ==========================================

    with tab1:

        st.subheader("Your Day-Wise Travel Schedule")

        for day in itinerary.days:

            with st.expander(
                f"📅 Day {day.day_number} — {day.date}",
                expanded=(day.day_number == 1)
            ):

                for activity in day.activities:

                    st.markdown(
                        f"### 🕒 {activity.start_time} – "
                        f"{activity.end_time}"
                    )

                    st.markdown(
                        f"**{activity.activity_name}**"
                    )

                    st.write(
                        f"📍 Location: {activity.location}"
                    )

                    st.write(activity.description)

                    st.write(
                        f"⏱️ Duration: {activity.duration_minutes} minutes"
                    )

                    if activity.estimated_cost is not None:
                        st.write(
                            f"💵 Estimated Cost: "
                            f"₹{activity.estimated_cost:,.0f}"
                        )

                    if activity.travel_distance_km is not None:
                        st.write(
                            f"🚗 Travel Distance: "
                            f"{activity.travel_distance_km:.1f} km"
                        )

                    if activity.travel_time_minutes is not None:
                        st.write(
                            f"🚘 Travel Time: "
                            f"{activity.travel_time_minutes:.0f} minutes"
                        )

                    st.divider()

                if day.daily_estimated_cost is not None:
                    st.info(
                        f"Estimated Day {day.day_number} Cost: "
                        f"₹{day.daily_estimated_cost:,.0f}"
                    )

                if day.daily_notes:
                    st.caption(day.daily_notes)

        if itinerary.travel_tips:

            st.subheader("💡 Travel Tips")

            for tip in itinerary.travel_tips:
                st.write(f"• {tip}")

        if itinerary.assumptions:

            with st.expander("⚠️ Planning Assumptions"):

                for assumption in itinerary.assumptions:
                    st.write(f"• {assumption}")

    # ==========================================
    # TAB 2: BUDGET BREAKDOWN
    # ==========================================

    with tab2:

        st.subheader("💰 Trip Budget Analysis")

        budget = itinerary.budget_breakdown

        if budget is not None:

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Total Budget",
                f"₹{budget.total_budget:,.0f}"
            )

            col2.metric(
                "Estimated Expenses",
                f"₹{budget.total_expenses:,.0f}"
            )

            col3.metric(
                "Remaining Budget",
                f"₹{budget.remaining_budget:,.0f}"
            )

            st.divider()

            st.markdown("### Expense Categories")

            categories = {
                "Attractions": budget.attraction_cost,
                "Food": budget.food_cost,
                "Transport": budget.transport_cost,
                "Accommodation": budget.accommodation_cost,
                "Other": budget.other_cost
            }

            for category, amount in categories.items():

                if amount is None:
                    st.write(f"**{category}:** Not estimated")
                else:
                    st.write(f"**{category}:** ₹{amount:,.0f}")

            st.divider()

            if budget.budget_status == "PARTIAL ESTIMATE":

                st.warning(
                    "⚠️ Partial Estimate: Some costs may be "
                    "unconfirmed or incomplete."
                )

            elif budget.within_budget:

                st.success("✅ Your trip is within the estimated budget!")

            else:

                st.error(
                    "❌ Your estimated expenses exceed the budget."
                )

            if budget.budget_notes:
                st.info(budget.budget_notes)

        else:
            st.warning("Budget breakdown is unavailable.")

    # ==========================================
    # TAB 3: DESTINATION RESEARCH
    # ==========================================

    with tab3:

        st.subheader(f"🔍 Exploring {research.destination}")

        st.write(research.overview)

        st.markdown("### 🏛️ Top Attractions")

        for attraction in research.top_attractions:

            with st.expander(attraction.name):

                st.write(attraction.description)
                st.write(f"📍 {attraction.location}")

                if attraction.entry_fee is not None:
                    st.write(
                        f"🎟️ Entry Fee: ₹{attraction.entry_fee:,.0f}"
                    )

                if attraction.opening_hours:
                    st.write(
                        f"🕒 Opening Hours: {attraction.opening_hours}"
                    )

                st.write(
                    f"⏱️ Visit Duration: "
                    f"{attraction.visit_duration_hours} hours"
                )

                if attraction.source_url:
                    st.markdown(
                        f"[View Source]({attraction.source_url})"
                    )

        st.markdown("### 💎 Hidden Gems")

        for attraction in research.hidden_gems:

            with st.expander(attraction.name):

                st.write(attraction.description)
                st.write(f"📍 {attraction.location}")

                if attraction.source_url:
                    st.markdown(
                        f"[View Source]({attraction.source_url})"
                    )

        st.markdown("### 🍲 Local Food")

        for food in research.local_food:

            with st.expander(food.name):

                st.write(food.description)

                if food.estimated_cost is not None:
                    st.write(
                        f"💵 Estimated Cost: "
                        f"₹{food.estimated_cost:,.0f}"
                    )

                if food.recommended_place:
                    st.write(
                        f"📍 Recommended Place: "
                        f"{food.recommended_place}"
                    )

                if food.source_url:
                    st.markdown(
                        f"[View Source]({food.source_url})"
                    )

        if research.travel_tips:

            st.markdown("### 💡 Local Travel Tips")

            for tip in research.travel_tips:
                st.write(f"• {tip}")

        if research.budget_notes:
            st.info(research.budget_notes)

        if research.verification_notes:
            st.warning(research.verification_notes)

    # ==========================================
    # TAB 4: DOWNLOADS
    # ==========================================

    with tab4:

        st.subheader("📥 Download Your Travel Plan")

        st.download_button(
            label="📄 Download Itinerary (Markdown)",
            data=st.session_state["itinerary"],
            file_name="travel_itinerary.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.download_button(
            label="📊 Download Structured Itinerary (JSON)",
            data=json.dumps(
                st.session_state["structured_itinerary"],
                indent=4,
                ensure_ascii=False
            ),
            file_name="travel_itinerary.json",
            mime="application/json",
            use_container_width=True
        )

        st.download_button(
            label="🔍 Download Research Report (Markdown)",
            data=st.session_state["research"],
            file_name="destination_research.md",
            mime="text/markdown",
            use_container_width=True
        )

        st.download_button(
            label="📊 Download Research Data (JSON)",
            data=json.dumps(
                st.session_state["structured_research"],
                indent=4,
                ensure_ascii=False
            ),
            file_name="destination_research.json",
            mime="application/json",
            use_container_width=True
        )
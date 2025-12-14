import json
import logging
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)

def load_courses():
    try:
        with open("courses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

class ActionGetCourseInfo(Action):
    def name(self) -> Text:
        return "action_get_course_info"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        course_code_input = tracker.get_slot("course_code")
        courses = load_courses()
        
        search_term = str(course_code_input).lower().strip()
        if search_term in ("ai", "AI", "Ai"):
            search_term = "artificial intelligence"
        
        # Search for the course (case-insensitive)
        found_course = next((item for item in courses if item["course_code"].lower() == str(course_code_input).lower()), None)

        if found_course:
            # Format strictly based on the fields
            prereqs = ", ".join(found_course['prerequisites']) if found_course['prerequisites'] else "None"
            sections = ", ".join(found_course['sections'])
            
            response = (
                f"**{found_course['course_code']} - {found_course['course_name']}**\n"
                f"- Faculty: {found_course['faculty']}\n"
                f"- Credits: {found_course['credits']}\n"
                f"- Prerequisites: {prereqs}\n"
                f"- Available Sections: {sections}\n"
                f"- Category: {found_course['category'].capitalize()}"
            )
            dispatcher.utter_message(text=response)
        else:
            dispatcher.utter_message(text=f"I couldn't find details for course code {course_code_input} in the repository.")
            
        return [SlotSet("course_code", None)]

class ActionGetStudyPlan(Action):
    """
    Addresses the 'Study Plan Guidance' objective
    Suggests courses based on the semester.
    """
    def name(self) -> Text:
        return "action_get_study_plan"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        semester_input = tracker.get_slot("semester")
        courses = load_courses()
        
        # Filter courses by semester
        suggested_courses = [c for c in courses if str(c["semester"]) == str(semester_input)]

        if suggested_courses:
            course_list = "\n".join([f"- {c['course_code']}: {c['course_name']}" for c in suggested_courses])
            dispatcher.utter_message(text=f"Here are the recommended courses for Semester {semester_input}:\n{course_list}")
        else:
            dispatcher.utter_message(text=f"I don't have a standard study plan loaded for Semester {semester_input} yet.")
        
        return [SlotSet("semester", None)]

class ActionNotificationAPI(Action):
    """
    Simulates the SMTP Engine and Template Email
    """
    def name(self) -> Text:
        return "action_notification_api"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("student_email")
        notification_type = tracker.get_slot("notification_type") # e.g., 'registration' or 'deadlines'
        
        # Simulating the "Structured Request Payload" 
        email_template = f"""
        [SMTP EMAIL SIMULATION]
        To: {email}
        Subject: UTM Alert - {notification_type}
        
        Dear Student,
        This is an automated reminder regarding {notification_type}.
        Please check the official portal at http://my.utm.my.
        """
        
        # In a real scenario, smtplib would be used here.
        # For prototype, we display the confirmation.
        dispatcher.utter_message(text=f"Notification Request Sent.\nTarget: {email}\nPayload: {notification_type}")
        print(email_template) # Log to console to prove it "sent"
        
        return []
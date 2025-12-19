import json
import logging
import smtplib
import ssl
from email.message import EmailMessage
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, SessionStarted, ActionExecuted
from rasa_sdk.executor import CollectingDispatcher

logger = logging.getLogger(__name__)

def load_courses():
    try:
        with open("courses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def send_email(sender_email, receiver_email, subject, message, password):
    """Send email using Gmail SMTP server"""
    try:
        # Create email
        msg = EmailMessage()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.set_content(message)

        # Set secure connection with email server - Gmail
        secure_connect = ssl.create_default_context()

        # Connect to Gmail server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=secure_connect) as server:
            server.login(sender_email, password)
            server.send_message(msg)
            logger.info('Email sent successfully!')
            return True
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        return False

class ActionHandleCourseInquiry(Action):
    def name(self) -> Text:
        return "action_handle_course_inquiry"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        course_code_input = tracker.get_slot("course_code")
        
        if not course_code_input:
            dispatcher.utter_message(text="Please provide a course code.")
            return []
        
        # Normalize the course code input
        course_input = str(course_code_input).upper().strip()
        
        # Check for MECS1033
        if "MECS1033" in course_input or "1033" in course_input:
            response = (
                "Yes, it is available in Semester 1, 2025/2026.\n"
                "However a pre-requisite course (MECS0033) is required but you have not taken it from previous semester yet.\n\n"
                "You will need to pass the pre-requisite course (MECS0033) before you can register for MECS1033.\n"
                "So would you want to register MECS0033?"
            )
            dispatcher.utter_message(text=response)
            return [SlotSet("course_code", "MECS1033")]
        
        # Check for MECS0033
        elif "MECS0033" in course_input or "0033" in course_input:
            response = (
                "Great, MECS0033 is available for Semester 1, 2025/2026.\n"
                "It is a pre-requisite course before you taking MECS1033.\n\n"
                "Here is the timetable for MECS0033:\n"
                "- Monday: 10am - 12pm\n"
                "- Friday: 9pm - 11pm"
            )
            dispatcher.utter_message(text=response)
            return [SlotSet("course_code", "MECS0033")]
        
        else:
            dispatcher.utter_message(text="Please specify either MECS0033 or MECS1033.")
            return []

class ActionSendEmailNotification(Action):
    def name(self) -> Text:
        return "action_send_email_notification"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        student_email = tracker.get_slot("student_email")
        course_code = tracker.get_slot("course_code")
        
        if not student_email:
            dispatcher.utter_message(text="Please provide your email address.")
            return []
        
        # Email configuration (Sender's email and app password)
        sender_email = "<your_email>@gmail.com"
        password = "<your_app_password>"
        
        if not sender_email or not password:
            dispatcher.utter_message(text="Email configuration is missing. Please contact the administrator.")
            logger.error("SENDER_EMAIL or SENDER_PASSWORD environment variables are not set")
            return []
        
        # Get course timetable based on course code
        if course_code == "MECS0033":
            timetable = "Monday: 10am - 12pm\nFriday: 9pm - 11pm"
        elif course_code == "MECS1033":
            timetable = "Tuesday: 10am - 12pm\nThursday: 9pm - 11pm"
        else:
            timetable = "To be announced"
        
        subject = f"Course Registration For {course_code} and Timetable"
        message = f"Dear Student,\n\nHere is your Timetable for {course_code}:\n{timetable}\n\nBest Regards,\nUTM Assistant"
        
        # Send email
        success = send_email(sender_email, student_email, subject, message, password)
        
        if success:
            response = f"Ok sure. Email will be sent to your {student_email}\nThank you for your responses. Have a good day."
        else:
            response = f"I tried to send an email to {student_email}, but there was an issue. Please check the email address and try again."
        
        dispatcher.utter_message(text=response)
        
        # Mark conversation as ended
        return [
            SlotSet("conversation_ended", True),
            SlotSet("student_email", None),
            SlotSet("course_code", None)
        ]
import smtplib
import os
import re
import cohere
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(api_key=os.getenv("COHERE_API_KEY"))

def send_email(user, matched_user, restaurant):
    binge_email = os.getenv("EMAIL_ID")

    message = get_message(user, matched_user, restaurant)

    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = "You’ve Been Matched for a Restaurant Date!"
    msg['From'] = binge_email
    msg['To'] = user["email"]

    s = smtplib.SMTP('smpt.gmail.com', 587)
    s.starttls()
    s.login(binge_email, os.getenv("EMAIL_PW"))
    s.send_message(msg)
    s.quit()

def get_message(user, matched_user, restaurant):
    prompt = get_prompt(user, matched_user, restaurant)
    res = co.chat(
        model="command-r-plus-08-2024",
        message=prompt,
    )
    return res.text

def get_prompt(user, matched_user, restaurant):
    matched_user_profile = f"Wants {matched_user["relationship_goals"]} relationship, Expresses emotion {matched_user["affection_expression"]}, {matched_user["free_time"]} on free times, {matched_user["motivation"]} motivates me, Has {matched_user["communication_style"]} communication style"
    msg = f"""
    Write a polite and engaging email to notify a user that they have been matched with another user on a restaurant date through a dating app. Use the following details to generate the email:

    User's Name: {user["name"]}
    Matched User's Name: {matched_user["name"]}
    Matched User's Email: {matched_user["email"]}
    Restaurant Name: {restaurant}
    Matched User's Profile: {matched_user_profile}

    The email should have:
    A warm and friendly tone.
    One short introduction sentence congratulating the user for their match.
    At the end of the email, include a sentence starting with 'How about starting an email with:' followed by a creative and cheesy phrase the user can use to email their match. The phrase should be tailored to the matched user's profile and reflect their profile, or the restaurant information.
    An optional note to reach out for assistance if needed.
    Strictly follow the example email format provided below. 
    Only modify the square-bracket texts.


    Example Email Format:

    Hi [User's Name],

    [Introduction]

    Your Match:

    Name: [Matched User's Name]
    Email: [Matched User's Email]

    Restaurant Details:

    Name: [Restaurant Name]

    Feel free to contact your match—how about starting an email with: [suggested cheesy phrase]?
    [An optional note to reach out for assistance if needed, e.g. "If you need any assistance or have any questions, our team is always here to help."]

    Happy meeting and eating!

    Warm regards,
    Binge Team
    binge.meet.and.eat@gmail.com
    """
    return msg
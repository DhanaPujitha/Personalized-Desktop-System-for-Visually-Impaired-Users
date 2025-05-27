import smtplib
import imaplib
import email
import speech_recognition as sr
from speech import prntdisp

# Dictionary of contacts
contacts = {
    "apple": "acdf.1346.acdf@gmail.com",
    "john": "john.doe@example.com",
    "alice": "alice.smith@example.com"
}

def listen_for_command():
   # Initialize recognizer
    recognizer = sr.Recognizer()

    # Use the microphone for input
    with sr.Microphone() as source:
        prntdisp("Listening for your command...")
        
        # Adjust for ambient noise and set a reasonable duration for listening
        recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust sensitivity to noise
        audio = recognizer.listen(source, timeout=10)  # 5 seconds timeout to avoid hanging

        # Recognize the speech using Google's speech recognition
        command = recognizer.recognize_google(audio)  # Setting timeout for API request
        prntdisp(f"You said: {command}")
        return command.lower()

def get_recipient_email():
    prntdisp("Who would you like to send the email to?")
    name = listen_for_command()
    
    if name is None:
        return None
    
    email_address = contacts.get(name)
    
    if email_address:
        prntdisp(f"Sending email to {name} at {email_address}")
        return email_address
    else:
        prntdisp(f"Sorry, I don't have the email for {name}. Would you like to add this person to contacts? Say 'yes' to add.")
        command = listen_for_command()

        if command and "yes" in command:
            add_new_contact(name)
        else:
            prntdisp("Okay, try again later.")
        return None

def add_new_contact(name):
    prntdisp(f"Please provide the email address for {name}.")
    email_address = listen_for_command()
    
    if email_address:
        contacts[name] = email_address
        prntdisp(f"{name} has been added to your contacts with the email address {email_address}.")
    else:
        prntdisp("Sorry, I couldn't capture the email. Try again later.")

def send_email():
    recipient = get_recipient_email()
    if recipient is None:
        prntdisp("Failed to capture the recipient email. Try again.")
        return

    prntdisp("What is the subject?")
    subject = listen_for_command()

    prntdisp("What is the message?")
    message = listen_for_command()
    
    sender_email = "geethagurram04@gmail.com"
    sender_password = "qbme amix usny rvdu"
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, sender_password)
        msg = f"Subject: {subject}\n\n{message}"
        server.sendmail(sender_email, recipient, msg)
        prntdisp("Email sent!")

def read_unread_emails():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login("geethagurram04@gmail.com", "qbme amix usny rvdu")
    mail.select("inbox")
    status, response = mail.search(None, '(UNSEEN)')
    unread_msg_nums = response[0].split()
    
    for e_id in unread_msg_nums:
        status, msg_data = mail.fetch(e_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    prntdisp(part.get_payload(decode=True).decode())
        else:
            prntdisp(msg.get_payload(decode=True).decode())


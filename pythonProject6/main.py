import pyttsx3
import spacy
from models import Appointment, User

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

# Load the spaCy English model
nlp = spacy.load('en_core_web_sm')

current_user = None
is_admin = False

# Specialist information
specialists = {
    "Cardiologist": {"name": "Dr. Rangasamy", "hours": "9 AM - 5 PM"},
    "Dermatologist": {"name": "Dr. Abul", "hours": "10 AM - 6 PM"},
    "Neurologist": {"name": "Dr. Manoj", "hours": "8 AM - 4 PM"},
    "Allergist": {"name": "Dr. Batman", "hours": "11 AM - 7 PM"},
    "Endocrinologist": {"name": "Dr. Hari", "hours": "9 AM - 5 PM"},
    "Rheumatologist": {"name": "Dr. Modi", "hours": "10 AM - 6 PM"}
}


def speak(message):
    engine.say(message)
    print(message)
    engine.runAndWait()


def register():
    global current_user
    while True:
        speak("Please enter a username or type 'back' to return to the main menu.")
        username = input("Enter a username: ")

        if username.lower() == 'back':
            return

        if User.username_exists(username):
            speak("Username already exists. Please choose a different username.")
            continue

        speak("Please enter a password.")
        password = input("Enter a password: ")
        user = User(username, password)
        try:
            user.save()
            speak("Registration successful.")
            # Automatically log in after successful registration
            current_user = user
            speak(f"Welcome {username}! You are now logged in.")
            break
        except ValueError as e:
            speak(str(e))


def login():
    global current_user, is_admin
    speak("Please enter your username or type 'back' to return to the main menu.")
    username = input("Enter your username: ")

    if username.lower() == 'back':
        return

    speak("Please enter your password.")
    password = input("Enter your password: ")

    if username == "admin" and password == "admin123":
        current_user = User(username, password)
        is_admin = True
        speak("Admin login successful.")
    else:
        user = User.authenticate(username, password)
        if user:
            current_user = user
            speak("Login successful.")
        else:
            speak("Login failed. Please try again.")


def splorder():
    speak("We have the following specialists available:")
    for specialist, info in specialists.items():
        sd = f"{specialist}: {info['name']}"
        speak(sd)


def workinghours():
    while True:
        speak(
            "Would you like to know the working hours of any specific doctor? Type the specialist name or 'back' to go to the previous options.")
        for specialist, info in specialists.items():
            speak(f"{specialist}: {info['name']}")
            print(f"{specialist}: {info['name']}")
        sname = input(
            "Enter the specialist name to know their working hours or type 'back' to go to the previous options: ")
        if sname.lower() == 'back':
            break
        if sname in specialists:
            wh = specialists[sname]['hours']
            sw = f"The working hours of {specialists[sname]['name']} are {wh}."
            speak(sw)
        else:
            speak("Sorry, I did not recognize that specialist.")


def appointment():
    if current_user is None:
        speak("Please login first.")
        return

    speak("Please enter your name to book an appointment or type 'back' to return to the main menu.")
    name = input("Enter your name: ")
    if name.lower() == 'back':
        return

    speak("Please choose a specialist from the following list:")
    for specialist in specialists:
        print(specialist)

    specialist = input("Enter the specialist: ")
    if specialist in specialists:
        doctor = specialists[specialist]['name']
        new_appointment = Appointment(name, specialist, doctor)
        new_appointment.save()
        speak("Your appointment has been booked.")
    else:
        speak("Incorrect specialist name. Here is the list of available specialists:")
        for specialist in specialists:
            print(specialist)


def view_appointments():
    if current_user is None:
        speak("Please login first.")
        return

    appointments = Appointment.get_all()
    if appointments:
        speak("Here are your appointments:")
        for appointment in appointments:
            speak(f"Name: {appointment[1]}, Specialist: {appointment[2]}, Doctor: {appointment[3]}")
    else:
        speak("You have no appointments.")


def advanced_symptom_analysis(symptoms):
    doc = nlp(symptoms)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    # Basic symptom to specialist mapping
    specialist_map = {
        "Cardiologist": ["heart", "chest", "blood pressure", "heart attack"],
        "Dermatologist": ["skin", "rash", "acne"],
        "Neurologist": ["headache", "migraine", "seizure", "numbness"],
        "Allergist": ["allergy", "sneeze", "runny nose", "asthma"],
        "Endocrinologist": ["diabetes", "thyroid", "hormone"],
        "Rheumatologist": ["joint", "arthritis", "pain", "swelling"]
    }

    # Check for symptoms in the user's text and suggest a specialist
    suggested_specialists = []
    for specialist, keywords in specialist_map.items():
        for keyword in keywords:
            if keyword in symptoms.lower():
                suggested_specialists.append(specialist)

    if suggested_specialists:
        suggested_specialists = list(set(suggested_specialists))  # Remove duplicates
        dnames = ', '.join([specialists[s]['name'] for s in suggested_specialists])
        speak(
            f"Based on your symptoms, I suggest you visit the following specialists: {', '.join(suggested_specialists)}. Doctors: {dnames}.")
    else:
        speak("Sorry, I could not find a specialist based on your symptoms.")


def suggest():
    speak("Please describe your symptoms or type 'back' to return to the main menu.")
    symptoms = input("Describe your symptoms: ")
    if symptoms.lower() == 'back':
        return
    advanced_symptom_analysis(symptoms)


def admin_view_users():
    users = User.get_all()
    if users:
        speak("Here are the registered users:")
        for user in users:
            speak(f"Username: {user[1]}")
    else:
        speak("No registered users found.")


def admin_delete_user():
    speak("Enter the username of the user you want to delete or type 'back' to return to the main menu.")
    username = input("Enter the username: ")
    if username.lower() == 'back':
        return
    if User.username_exists(username):
        User.delete(username)
        speak(f"User {username} has been deleted.")
    else:
        speak("User not found.")


while True:
    if current_user is None:
        menu = (
            "1. Register\n2. Login\n9. Quit\n\nPress the option: "
        )
    elif is_admin:
        menu = (
            "1. View all users\n2. Delete a user\n3. Logout\n4. Quit\n\nPress the option: "
        )
    else:
        menu = (
            "1. Type of specialist available\n2. Book an appointment\n3. View appointments\n4. Working hours\n5. Contact line\n6. Suggest doctor based on symptoms\n7. Logout\n8. Quit\n\nPress the option: "
        )

    speak(menu)
    mopt = int(input("Enter your option: "))
    if mopt == 1 and current_user is None:
        register()
    elif mopt == 2 and current_user is None:
        login()
    elif mopt == 1 and is_admin:
        admin_view_users()
    elif mopt == 2 and is_admin:
        admin_delete_user()
    elif mopt == 3 and is_admin:
        current_user = None
        is_admin = False
        speak("You have been logged out.")
    elif mopt == 4 and is_admin:
        speak("Thank you for using our chatbot. Have a great day!")
        break
    elif mopt == 1 and current_user is not None:
        splorder()
    elif mopt == 2 and current_user is not None:
        appointment()
    elif mopt == 3 and current_user is not None:
        view_appointments()
    elif mopt == 4 and current_user is not None:
        workinghours()
    elif mopt == 5 and current_user is not None:
        speak("Our working hours are from 8 AM to 8 PM, Mon to Sat.")
    elif mopt == 6 and current_user is not None:
        suggest()
    elif mopt == 7 and current_user is not None:
        current_user = None
        is_admin = False
        speak("You have been logged out.")
    elif mopt == 8 and current_user is not None:
        speak("Thank you for using our chatbot. Have a great day!")
        break
    elif mopt == 9:
        speak("Thank you for using our chatbot. Have a great day!")
        break
    else:
        speak("Invalid option. Please try again.")

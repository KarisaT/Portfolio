from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages

# Configure Flask-Mail (replace with your own email + app password)
app.config['MAIL_SERVER'] = 'smtp.office365.com'   # Outlook SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'toyacharo@outlook.com'   # <-- your Outlook email
app.config['MAIL_PASSWORD'] = 'your_app_password'       # <-- your Outlook app password

mail = Mail(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# Route to handle form submission
@app.route("/send_message", methods=["POST"])
def send_message():
    name = request.form.get("name")
    email = request.form.get("email")
    message = request.form.get("message")

    # Validate form fields
    if not name or not email or not message:
        flash("All fields are required!", "danger")
        return redirect(url_for("contact"))

    try:
        # Construct the email
        msg = Message("New Contact Form Message",
                      sender=app.config['MAIL_USERNAME'],   # must be your own email
                      recipients=["toyacharo@outlook.com"]) # where you want to receive messages
        msg.body = f"From: {name} <{email}>\n\n{message}"

        # Send the email
        mail.send(msg)

        flash("Your message has been sent successfully!", "success")
    except Exception as e:
        print("Error sending email:", e)
        flash("There was an error sending your message. Please try again later.", "danger")

    return redirect(url_for("contact"))

if __name__ == "__main__":
    app.run(debug=True)

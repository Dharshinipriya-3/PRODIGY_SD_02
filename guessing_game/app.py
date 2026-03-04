from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "secretkey"


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    # Initialize game only once
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0

    if request.method == "POST":
        guess_input = request.form.get("guess")

        # Validate input (prevents crash)
        if not guess_input or not guess_input.isdigit():
            message = "Please enter a valid number!"
        else:
            guess = int(guess_input)
            session["attempts"] += 1
            number = session["number"]

            if guess < number:
                message = "Too Low! Try Again."
            elif guess > number:
                message = "Too High! Try Again."
            else:
                message = f"Correct! 🎉 You guessed in {session['attempts']} attempts."
                session.clear()  # Reset game completely

    return render_template("index.html", message=message)


@app.route("/reset")
def reset():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=False)
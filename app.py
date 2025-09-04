from flask import *
from flask import Flask, render_template, request  
import pandas as pd
from pickle import load

# Load model
with open("sn.pkl", "rb") as f:
    model = load(f)

# Load columns 
with open("sn_cols.pkl", "rb") as f:
    cols = load(f)

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    msg = ""
    prediction = None   # <-- initialize prediction

    if request.method == "POST":
        age = float(request.form.get("age"))
        es_sal = float(request.form.get("es_sal"))
        gender = int(request.form.get("gender"))

        if age < 0:
            msg = "Age cannot be negative."
            return render_template("home.html", msg=msg, prediction=prediction)

        # Prepare input
        if gender == 1:   # Male
            d = pd.DataFrame([[age, es_sal, 1]], columns=cols)
        elif gender == 2: # Female
            d = pd.DataFrame([[age, es_sal, 0]], columns=cols)
        else:
            msg = "Invalid gender selected."
            return render_template("home.html", msg=msg, prediction=prediction)

        purchased = model.predict(d)
        prediction = purchased[0]   # <-- store result

        print("Purchased:", "Yes (1)" if prediction == 1 else "No (0)")

        return render_template("home.html", prediction=prediction, msg=msg)

    return render_template("home.html", prediction=prediction, msg=msg)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

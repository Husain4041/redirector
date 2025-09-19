from flask import Flask, render_template, request
import json

app = Flask(__name__)

def format_make(make):
    exceptions = {
        "ac": "AC",
        "alfa romeo": "Alfa Romeo",
        "aston martin": "Aston Martin",
        "asia motors": "Asia Motors",
        "bmw": "BMW",
        "gmc": "GMC",
        "mg": "MG",
        "aito": "AITO",
        "bac": "BAC",
        "baic": "BAIC",
        "baw": "BAW",
        "byd": "BYD",
        "cevo": "CEVO",
        "chtc": "CHTC",
        "cmc": "CMC",
        "daf": "DAF",
        "ds automobiles": "DS Automobiles",
        "ezgo": "EZGO",
        "dfsk": "DFSK",
        "gac": "GAC",
        "gaz": "GAZ",
        "hiphi": "HiPhi",
        "hofele": "HOFELE",
        "hongqi": "HONGQI",
        "gwm": "GWM",
        "ineos": "INEOS",
        "jac": "JAC",
        "jaecoo": "JAECOO",
        "jcb": "JCB",
        "jetta": "JETTA",
        "jmc": "JMC",
        "kama": "KAMA",
        "ktm": "KTM",
        "levc": "LEVC",
        "man": "MAN",
        "mclaren": "McLaren",
        "mercedes-benz": "Mercedes-Benz",
        "omoda": "OMODA",
        "ora": "ORA",
        "ram": "RAM",
        "rox": "ROX",
        "ruf": "RUF",
        "saic": "SAIC",
        "techart": "TECHART",
        "rolls-royce": "Rolls-Royce",
    }

    return exceptions.get(make.lower(), make.capitalize())

@app.route('/', methods=['GET', 'POST'])
def index():

    with open('usable_car_data/car_makes_models.json', 'r') as f:
        car_data = json.load(f)

    # car_data = {
    #     "bmw": ["1-series", "2-series", "3-series", "4-series", "5-series", "6-series", 
    #             "7-series", "8-series", "i3", "i4", "i5", "i7", "i8", "ix", "ix1", "ix2", "ix3",
    #             "m1", "m2", "m3", "m4", "m5", "m6", "m8",
    #             "x5", "x6", "x7", "x1", "x2", "x3", "x4", "xm"],
    #     "bentley": [],
    #     "byd": [],
    # }

    formatted_makes = {make: format_make(make) for make in car_data}

    if request.method == 'POST':
        # 1️⃣ Clean raw input
        make_raw = request.form.get('make', '').strip()
        model_raw = request.form.get('model', '').strip()

        # 2️⃣ Lowercase versions for URL logic
        make_lower = make_raw.lower()
        model_lower = model_raw.lower()

        # 3️⃣ Formatted versions for display
        make_display = format_make(make_raw)
        model_display = model_raw.capitalize()

        return render_template('results.html', 
            make_lower=make_lower,
            model_lower=model_lower,
            make_display=make_display,
            model_display=model_display)
    return render_template('index.html', car_data=car_data, formatted_makes=formatted_makes)

if __name__ == '__main__':
    app.run(debug=True)

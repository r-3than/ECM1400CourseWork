from flask import Flask, render_template ,redirect,request
app = Flask(__name__)

@app.route("/index")
def index():
    ## Var decomp
    ## updates
    ## title
    ## location
    ## local_7day_infections
    ## national_7day_infections
    ## nation_location
    ## hospital_cases
    ## deaths_total
    ## news_articles
    return render_template("index.html",updates="",title="Hello World!")


app.run(port=5002,debug=True)
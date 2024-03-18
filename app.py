from flask import Flask, request, render_template
import google.generativeai as palm
import replicate
import os

palm.configure(api_key="AIzaSyCCT1K99BJ1JbLwhCE7qOcQ5KOZcPJ9ZZ4")
model = {
    "model": "models/chat-bison-001",
}

os.environ["REPLICATE_API_TOKEN"] = "787f515cb0624813736c11e7fefec66473394f02"

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return(render_template("index.html"))

@app.route("/palm", methods=["GET","POST"])
def palm_flask():
    return(render_template("palm.html"))

@app.route("/mj", methods=["GET","POST"])
def mj():
    return(render_template("mj.html"))

@app.route("/palm_query", methods=["GET","POST"])
def palm_query():
    q = request.form.get("q")
    print(q)
    r = palm.chat(
        **model,
        messages=q
    )
    print(r.last)
    return(render_template("palm_reply.html",r=r.last))

@app.route("/mj_query", methods=["GET","POST"])
def mj_query():
    q = request.form.get("q")
    r = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf", 
        input={"prompt": q}
    )
    return(render_template("mj_reply.html",r=r[0]))

if __name__ == "__main__":
    app.run()

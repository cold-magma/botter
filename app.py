from flask import Flask, render_template, url_for, request, redirect
import os, string, random, sys, urllib, base64, requests, six
import run

app = Flask(__name__)
scope = "playlist-modify-public"
authID = ""
playlistID = ""
word = ""
genre = ""
limit = ""
client_id = '0124db9ddbbc4fc3af027f67e06549c6'
client_secret = '6b27a67494e14d04a02888fdc89cd452'

encoded_cred = base64.b64encode(six.text_type(client_id + ':' + client_secret).encode("ascii"))


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        return redirect("https://accounts.spotify.com/authorize?client_id="
                        + client_id + "&scope=" + scope + "&response_type=code&redirect_uri=http://localhost:5000/auth/")
    else:
        return render_template('home.html')


@app.route("/auth/")
def autho():
    global authID
    authID = request.url
    authID = authID.split("?code=")[-1]
    token_url = "https://accounts.spotify.com/api/token"
    payload = {
        "code": authID,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:5000/auth/",
        "scope": scope
    }
    headers = {
        "Authorization": "Basic {}".format(encoded_cred.decode("ascii"))
    }
    response = requests.post(token_url, data=payload, headers=headers, verify=True, timeout=None)
    authID = response.json()["access_token"]
    return redirect(url_for("playlistselect"))


@app.route("/playlistselect", methods=["GET", "POST"])
def playlistselect():
    global playlistID
    if request.method == "POST":
        playlistID = request.form["playlist"]
        playlistID = playlistID.split("/")[-1].split("?")[0]
        if playlistID:
            return redirect(url_for("trackselect"))
    else:
        return render_template('playlistselect.html')


@app.route("/trackselect", methods=["GET", "POST"])
def trackselect():
    global authID, playlistID
    if request.method == "POST":
        if request.form["submit"] == "Add songs":
            word = request.form["word"]
            genre = request.form["genre"]
            limit = request.form["limit"]
        else:
            word = random.choice(string.ascii_lowercase)
            genre = None
            limit = random.randint(10, 50)

        print(playlistID, file=sys.stdout)
        flag = run.run(authID, playlistID, word, genre, limit)
        if flag:
            return redirect(url_for("completed"))

    else:
        return render_template('params.html')


@app.route("/completed")
def completed():
    return render_template('completed.html')


if __name__ == "__main__":
    app.run(debug=True)

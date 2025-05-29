from flask import Flask, render_template
import requests

app= Flask(__name__)
@app.route("/")
def github_user():
  username="Pankaj-23"
  url=f"https://api.github.com/users/Pankaj-23"
  response = requests.get(url)
  
  if response.status_code == 200:
    data = response.json()
    return render_template("dashboard.html", user=data)
  else:
    return f"Error: {reponse.status_code}"

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5000, debug=True)


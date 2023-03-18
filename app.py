from flask import Flask, request, render_template, url_for

app = Flask(__name__)

# Run the Python code with the provided arguments
import requests
import os
api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        professional = request.form['professional']
        second_professional = request.form['second_professional']
        third_professional = request.form['third_professional']
        place = request.form['place']
        verb = request.form['verb']
        filename = request.form['filename']
        query_dir = "recent_q"
        filepath = os.path.join(query_dir, filename)
        api_endpoint = "https://api.openai.com/v1/completions"
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + api_key
        }

        request_data = {
            "model": "text-davinci-003",
            "prompt": (
            f"Write a joke about the following {professional}, {second_professional} {third_professional} that are {verb} in a {place}, "
            "Provide only the joke, no additonal text"
            "you can make the joke as ridiculous as you would like to make it"
            "Make sure to leave a line space between the question and answer to the joke"
            ),
            "max_tokens": 150,
            "temperature": 0.8,
            }

        response = requests.post(api_endpoint, headers=headers, json=request_data)

        if response.status_code == 200:
            response_text = response.json()["choices"][0]["text"]
            with open(filepath, "w") as file:
                file.write(response_text)
        else:
            return f"Request failed with status code {str(response.status_code)}"

        # Read the contents of the file and display it
        with open(filepath, "r") as file:
            file_contents = file.read()

        # Render the index page with the file contents as context
        return render_template("index.html", file_contents=file_contents)

    else:
        # Render the index page without any context
        return render_template("index.html")

@app.route("/recent_calls")
def recent_calls():
    query_dir = "recent_q"
    filenames = os.listdir(query_dir)

    links = []
    for filename in filenames:
        filepath = os.path.join(query_dir, filename)
        link = {"filename": filename, "url": url_for('query', filename=filename)}
        links.append(link)

    return render_template("recent_calls.html", links=links)

@app.route("/query")
def query():
    filename = request.args.get("filename")
    query_dir = "recent_q"
    filepath = os.path.join(query_dir, filename)
    with open(filepath, "r") as file:
        file_contents = file.read()

    return file_contents

@app.route("/result", methods=['POST'])
def result():
    professional = request.form['professional']
    second_professional = request.form['second_professional']
    third_professional = request.form['third_professional']
    place = request.form['place']
    verb = request.form['verb']
    filename = request.form['filename']
    query_dir = "recent_q"
    filepath = os.path.join(query_dir, filename) 
    api_endpoint = "https://api.openai.com/v1/completions"
    # store and call the API key from a .env file in your root directory
    api_key = os.getenv("OPENAI_API_KEY")
    print("API Key:", api_key)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + api_key
    }

    request_data = {
            "model": "text-davinci-003",
            "prompt": (
            f"Write a joke about the following {professional}, {second_professional} {third_professional} that are {verb} in a {place},"
            "Provide only the joke, no additonal text"
            "you can make the joke as ridiculous as you would like to make it"
            "Make sure to leave a line space between the question and answer to the joke"
            ),
            "max_tokens": 150,
            "temperature": 0.8,
            }

    response = requests.post(api_endpoint, headers=headers, json=request_data)

    if response.status_code == 200:
        response_text = response.json()["choices"][0]["text"]
        with open(filepath, "w") as file:
            file.write(response_text)
    else:
        return f"Request failed with status code {str(response.status_code)}"

    # Read the contents of the file and display it
    with open(filepath, "r") as file:
        file_contents = file.read()

    return file_contents

if __name__ == "__main__":
    app.run(debug=True)
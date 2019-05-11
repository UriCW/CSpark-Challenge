from flask import Flask, render_template
app = Flask(__name__)


@app.route("/graphs")
def graphs():
    pass


@app.route("/")
def root():
    return render_template(base.html)

if __name__ == "__main__":
    app.config.from_object
    app.run()

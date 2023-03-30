from flask import Flask, render_template, request
import re

app = Flask(__name__)


def regexTester(regularExpression, string):
    match = re.findall(rf"{regularExpression}", string)
    return match


def highlight(match):
    return f"<span>{match.group()}</span>"


def highlightMatches(regularExpression, string):
    resultString = re.sub(rf"{regularExpression}", highlight, string)
    return resultString


def getMatchesIndex(regularExpression, string):
    matchStrSpanList = []
    for match in re.finditer(rf"{regularExpression}", string):
        matchStrSpanList.append(match.span())
    return matchStrSpanList


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        regularExpression = request.form.get("regularExpression")
        testString = request.form.get("testString")
        if not regularExpression or not testString:
            return render_template(
                "home.html",
                errorMessage="Both Fields Required ",
                regularExpression=regularExpression,
                testString=testString,
            )
        try:
            re.compile(regularExpression)
        except re.error:
            return render_template(
                "home.html",
                errorMessage="Non valid regex pattern",
                regularExpression=regularExpression,
                testString=testString,
            )

        resultStringList = regexTester(regularExpression, testString)
        count = len(resultStringList)
        if count > 0:
            resultString = highlightMatches(regularExpression, testString)
            matchSpan = getMatchesIndex(regularExpression, testString)
            return render_template(
                "home.html",
                resultString=resultString,
                resultStringList=resultStringList,
                count=count,
                matchSpan=enumerate(matchSpan),
            )
        return render_template(
            "home.html",
            resultString=testString,
            resultStringList=[],
            count=0,
        )
    if request.method == "GET":
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)

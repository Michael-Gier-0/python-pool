# Michael Gier, mgier@usc.edu
# ITP 216, Spring 2024
# Section: 31885
# Final Project
# Description: Runs a web app which allows user to see pricing data for houses built from 1900 to 2014,
# and makes predictions for the price of a house based on user input.
from flask import Flask, render_template, request
import base64
import io
import os
import computation as c

app = Flask(__name__)


# root end point
# routes to query.html page
@app.route("/")
def home():
    """
    :Description: Renders query.html template
    :return: renders query.html
    """
    return render_template('query.html')


# pricing graph endpoint
# renders graph template
@app.route("/graph")
def graph():
    """
    :Description: Renders graph.html template
    :return: renders graph.html
    """
    return render_template('graph.html')


# prediction graph endpoint
# renders prediction template
@app.route("/prediction")
def prediction():
    """
    :Description: Renders prediction.html template
    :return: renders prediction.html
    """
    return render_template('prediction.html')


# graph creation endpoint
# queries housing data, creates a plot of pricing data based on year query, and displays graph on graph template
@app.route("/action/creategraph", methods=["POST", "GET"])
def create_graph():
    """
    Gets called from query.html form submit
    :return: if error in user input: renders query.html
             if successful user input: renders graph.html
    """
    if request.method == "POST":
        # ensures all parts of form are filled out
        if not request.form['start year'] == "" and not request.form['end year'] == "":
            # if form submission does not align with the data types or values necessary for successful query,
            # renders query template
            if not (1900 <= int(request.form['start year']) <= 2014
                    and 1900 <= int(request.form['end year']) <= 2014
                    and float(request.form['start year']).is_integer()
                    and float(request.form['end year']).is_integer()
                    and float(request.form['start year']) <= float(request.form['end year'])):
                return render_template('query.html')
            # ensures form submission aligns with data types and values necessary for successful query
            else:
                # calls year_price_plot() function from computation.py file, creates a plot
                # comparing year built to price
                fig = c.year_price_plot(request.form['start year'], request.form['end year'])
                # passes graph from matplotlib to html-friendly format
                img = io.BytesIO()
                fig.savefig(img, format='png')
                img.seek(0)
                fig_url = base64.b64encode(img.getvalue()).decode()
                # renders graph template with graph visible
                return render_template('graph.html',
                                       fig_url=fig_url,
                                       year1=request.form['start year'],
                                       year2=request.form['end year'])
        # if parts of form are empty, renders query template
        else:
            return render_template('query.html')


@app.route("/action/get_prediction", methods=["POST", "GET"])
def get_prediction():
    """
    Gets called from graph.html form submit, prediction.html form submit, or error.html form submit
    :return: if error in user input: renders error.html
             if no error in user input: renders prediction.html
    """
    if request.method == "POST":
        # ensures all parts of form are filled out
        if (not request.form['square feet'] == "" and not request.form['bedrooms'] == ""
                and not request.form['bathrooms'] == "" and not request.form['year'] == ""):
            # if form submission does not align with the data types or values necessary for successful
            # query and prediction, renders error template
            if not (int(request.form['square feet']) >= 0 and int(request.form['bedrooms']) >= 0
                    and float(request.form['square feet']).is_integer() and float(request.form['bedrooms']).is_integer()
                    and int(request.form['bathrooms']) >= 0 and float(request.form['bathrooms']).is_integer()
                    and 1900 <= int(request.form['year']) <= 2014
                    and float(request.form['year']).is_integer()):
                return render_template('error.html')
            # ensures form submission aligns with data types and values necessary for successful query and prediction
            else:
                # gets predicted price integer from prediction() function in computation file using user form submission
                predicted_price = c.prediction(request.form['bedrooms'], request.form['bathrooms'],
                                               request.form['square feet'], request.form['year'])
                # creates plot with prediction_graph() function in computation file
                fig = c.prediction_graph(predicted_price, request.form['square feet'])
                # passes graph from matplotlib to html-friendly format
                img = io.BytesIO()
                fig.savefig(img, format='png')
                img.seek(0)
                fig_url = base64.b64encode(img.getvalue()).decode()
                # renders prediction template with predicted price and prediction graph visible
                return render_template('prediction.html',
                                       message=predicted_price,
                                       fig_url=fig_url)
        # if parts of form are empty, renders query template
        else:
            return render_template('error.html')


# main entrypoint
# runs app
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)

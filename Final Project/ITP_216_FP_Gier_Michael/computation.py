# Michael Gier, mgier@usc.edu
# ITP 216, Spring 2024
# Section: 31885
# Final Project (computation)
# Description: Creates graphs based on data from Housing.csv, uses Housing.csv to train a machine learning model that
# predicts the price of a house based on user input, compares that predicted price to the data in Housing.csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor


def year_price_plot(start_year, end_year):
    """
    :Description: creates two plots comparing square footage and prices of houses, one which only includes houses
                  under $1 million for more clarity
    :param start_year: first year entered by user (int)
    :param end_year: last year entered by user (int)
    :return: fig
    """
    # reading in the dataset
    df = pd.read_csv("Housing.csv")

    # create two plots
    fig, ax = plt.subplots(2, 1, figsize=(10, 6))

    # queries dataset so that only houses built within the start_year and end_year are included
    df = df.query(str(start_year) + ' <= yr_built <= ' + str(end_year))

    # -------- TOP GRAPH -------------------------------------------------
    # make the x tick list from a range from 0 to 15000 and steps by 1000
    ax[0].xaxis.set_ticks(range(0, 15000, 1000))
    # labels x ticks with same numbers
    ax[0].xaxis.set_ticklabels(range(0, 15000, 1000))
    # sets title for graph, and labels x and y axes
    ax[0].set(title="Price vs. Square Footage for Houses Built Between " + str(start_year) + " and " + str(end_year),
           xlabel="Square Feet",
           ylabel="Price ($ Millions)")
    # creates scatter plot comparing square footage (x) with price (y)
    ax[0].scatter(df["sqft_living"], df["price"], color="red", s=0.75)
    # sets gridlines on graph
    ax[0].grid(which='both', color='#999999', alpha=0.2)

    # -------- BOTTOM GRAPH -------------------------------------------------
    # queries dataset so that only houses built between start_year and end_year are included, and only houses under
    # $1 million are included
    df = df.query('price < 1000000 and ' + str(start_year) + ' <= yr_built <= ' + str(end_year))
    # make the x tick list from a range from 0 to 15000 and steps by 1000
    ax[1].xaxis.set_ticks(range(0, 10000, 500))
    # labels x ticks with same numbers
    ax[1].xaxis.set_ticklabels(range(0, 10000, 500))
    # sets title for graph, and labels x and y axes
    ax[1].set(title="Price vs. Square Footage for Houses Built Between "
                    + str(start_year) + " and " + str(end_year) + " (Under $1 million)",
           xlabel="Square Feet",
           ylabel="Price ($ Million)")
    # creates scatter plot comparing square footage (x) with price (y)
    ax[1].scatter(df["sqft_living"], df["price"], color="red", s=0.75)
    # sets gridlines on graph
    ax[1].grid(which='both', color='#999999', alpha=0.2)

    # makes tight layout and shows plot
    fig.tight_layout()
    plt.show()

    # returns figure so it can be passed to html
    return fig


def prediction(beds, baths, sqft, year):
    # reads Housing.csv for data
    df0 = pd.read_csv("Housing.csv")
    # drops unneeded columns from dataset
    df = df0.drop(columns=['id', 'date', 'sqft_lot', 'floors', 'waterfront', 'view',
                          'condition', 'grade', 'sqft_above', 'sqft_basement', 'yr_renovated',
                          'zipcode', 'lat', 'long', 'sqft_living15', 'sqft_lot15'])
    # establishes "data" columns of data set; i.e. the x-variables
    data = df.drop('price', axis=1)
    # establishes the "target" column of data set, the price; i.e. the y-variable
    target = df['price']
    # sets model training details, stores 20% of data for testing
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.20, random_state=0)
    # sets KNN neighbors regressor model with optimized n_neighbors distance
    knn = KNeighborsRegressor(n_neighbors=88, weights='distance')
    # trains model using dataset
    knn.fit(X_train, y_train)
    # establishes user input data in an array to be used for prediction
    user_input = np.array([[float(beds), float(baths), int(sqft), int(year)]])
    # predicts price and rounds to make it an integer
    predicted_price0 = round(float(knn.predict(user_input)[0]), 0)
    predicted_price = int(predicted_price0)
    # returns predicted_price integer
    return predicted_price


def prediction_graph(predicted_price, sqft):
    """
    :Description: creates plot comparing square footage and price of houses, including the house with user input info
                  and its predicted price
    :param predicted_price: calculated price of house from prediction() function (int)
    :param sqft: user input square footage (int)
    :return: fig
        """
    # reading in the dataset
    df = pd.read_csv("Housing.csv")

    # creates plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))

    # takes larger value between 15000 sqft or user input sqft + 5000
    # for graph visualization purposes
    x_length = max(int(sqft) + 5000, 15000)

    # make the xtick list from a range from 0 to x_length and steps by 1000
    ax.xaxis.set_ticks(range(0, x_length, 1000))
    # labels ticks with those same numbers
    ax.xaxis.set_ticklabels(range(0, x_length, 1000))
    # sets plot title, and x and y axes labels
    ax.set(title="Price vs. Square Footage",
              xlabel="Square Feet",
              ylabel="Price ($ Millions)")
    # plots data from dataset
    ax.scatter(df["sqft_living"], df["price"], color="red", s=5, label="Price Data")
    # plots predicted price vs. user input sqft
    ax.scatter(int(sqft), int(predicted_price), color="blue", s=500, marker="*", label="Predicted Price")
    # sets gridlines on graph
    ax.grid(which='both', color='#999999', alpha=0.2)

    # shows legend differentiating dataset data with predicted data
    plt.legend(loc='upper right', markerscale=0.5)

    # makes tight layout and shows plot
    fig.tight_layout()
    plt.show()

    # returns fig so it can be passed to html
    return fig

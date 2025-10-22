import re
import urllib.parse

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from tabulate import tabulate
from tqdm import tqdm
from transformers import pipeline

nltk.download("punkt", quiet=True)
nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def load_data(file_path):
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            df = pd.read_json(file_path)
        else:
            raise ValueError("Unsupported file format. Please use CSV or JSON.")

        # Identify the product and price columns
        product_col = df.select_dtypes(include=["object"]).columns[0]
        price_col = df.select_dtypes(include=["float64", "int64"]).columns[0]

        return df, product_col, price_col
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        return None, None, None


def search_web(query, num_results=10):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for result in soup.find_all("div", class_="result__body"):
        title = result.find("a", class_="result__a").text
        snippet = (
            result.find("a", class_="result__snippet").text
            if result.find("a", class_="result__snippet")
            else ""
        )
        link = result.find("a", class_="result__a")["href"]
        if link.startswith("//duckduckgo.com/l/?uddg="):
            actual_url = urllib.parse.unquote(link.split("uddg=")[1].split("&")[0])
        else:
            actual_url = link
        results.append({"title": title, "snippet": snippet, "link": actual_url})
    return results[:num_results]


def extract_price(text):
    price_pattern = r"\$?\d+(?:\.\d{2})?"
    match = re.search(price_pattern, text)
    if match:
        return float(match.group().replace("$", ""))
    return None


def search_product_price(product):
    search_query = f"{product} price"
    search_results = search_web(search_query)
    prices = []
    sources = []
    for result in search_results[:5]:
        try:
            price = extract_price(result["snippet"])
            if price:
                prices.append(price)
                sources.append(result["link"])
        except Exception as e:
            print(f"Error processing {result['link']}: {str(e)}")
    if prices:
        return np.mean(prices), sources[0]
    return None, None


def analyze_market_prices(df, product_col, price_col):
    print("Analyzing market prices...")
    df["real_time_price"] = np.nan
    df["price_source"] = ""

    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Analyzing products"):
        product = row[product_col]
        price, source = search_product_price(product)
        if price is not None:
            df.at[index, "real_time_price"] = price
            df.at[index, "price_source"] = source

    df["price_difference"] = df["real_time_price"] - df[price_col]
    return df


def generate_dynamic_recommendations(df, product_col, price_col):
    recommendations = []

    # Analyze price elasticity
    if "demand" in df.columns:
        df["price_elasticity"] = (
            df["demand"].pct_change() / df[price_col].pct_change()
        ).abs()
        avg_elasticity = df["price_elasticity"].mean()

        if avg_elasticity > 1:
            recommendations.append(
                "The market appears to be highly price-sensitive. Consider small price adjustments and monitor demand closely."
            )
        else:
            recommendations.append(
                "The market appears to be less price-sensitive. There may be room for price increases on premium products."
            )

    # Analyze competitive positioning
    df["price_difference_percentage"] = (
        (df["real_time_price"] - df[price_col]) / df[price_col] * 100
    )
    avg_price_difference = df["price_difference_percentage"].mean()

    if avg_price_difference > 5:
        recommendations.append(
            f"On average, your prices are {avg_price_difference:.2f}% lower than the market. Consider gradual price increases to align with market rates."
        )
    elif avg_price_difference < -5:
        recommendations.append(
            f"On average, your prices are {-avg_price_difference:.2f}% higher than the market. Evaluate your value proposition or consider strategic price reductions."
        )

    # Identify potential loss leaders
    loss_leaders = df[df["price_difference_percentage"] < -10]
    if not loss_leaders.empty:
        recommendations.append(
            f"Potential loss leaders identified: {', '.join(loss_leaders[product_col].tolist())}. Evaluate if these are driving sales of other products."
        )

    # Suggest dynamic pricing for high-demand products
    if "demand" in df.columns:
        high_demand_products = df[df["demand"] > df["demand"].quantile(0.75)]
        if not high_demand_products.empty:
            recommendations.append(
                f"Consider implementing dynamic pricing for high-demand products: {', '.join(high_demand_products[product_col].tolist())}."
            )

    # Analyze seasonal trends (assuming we have date information)
    if "date" in df.columns:
        df["month"] = pd.to_datetime(df["date"]).dt.month
        seasonal_products = (
            df.groupby("month")[price_col].mean().pct_change().abs() > 0.1
        )
        if seasonal_products.any():
            recommendations.append(
                "Detected seasonal price fluctuations. Consider implementing a seasonal pricing strategy."
            )

    # Gather market insights for top products
    top_products = df.nlargest(3, price_col)[product_col].tolist()
    for product in top_products:
        search_results = search_web(f"{product} market trends")
        insight = extract_relevant_info(f"{product} pricing strategy", search_results)
        recommendations.append(f"Market insight for {product}: {insight}")

    return "\n   - ".join([""] + recommendations)


def analyze_pricing_data(df, product_col, price_col):
    print("Analyzing pricing data...")
    if "demand" not in df.columns:
        print(
            "Warning: 'demand' column not found. Adding mock demand data for analysis."
        )
        df["demand"] = np.random.randint(50, 500, size=len(df))

    X = df[["demand"]]
    y = df[price_col]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    df["predicted_price"] = model.predict(X)
    df["optimization_suggestion"] = df["predicted_price"] - df[price_col]

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="demand", y=price_col, data=df, label="Original")
    sns.scatterplot(x="demand", y="real_time_price", data=df, label="Real-time")
    sns.lineplot(
        x="demand", y="predicted_price", data=df, color="red", label="Predicted"
    )
    plt.title("Price vs Demand: Original, Real-time, and Predicted")
    plt.xlabel("Demand")
    plt.ylabel("Price")
    plt.legend()
    plt.savefig("price_demand_analysis.png")
    plt.close()

    # Generate dynamic recommendations
    recommendations = generate_dynamic_recommendations(df, product_col, price_col)

    summary = f"""
    Pricing Analysis Summary:
    1. Model Performance:
       - Mean Squared Error: {mse:.2f}
       - R-squared Score: {r2:.2f}
    2. Price Optimization Opportunities:
       - Products with largest positive difference (potentially underpriced):
         {df.nlargest(5, 'optimization_suggestion')[[product_col, price_col, 'real_time_price', 'predicted_price', 'optimization_suggestion', 'price_source']].to_string(index=False)}
       - Products with largest negative difference (potentially overpriced):
         {df.nsmallest(5, 'optimization_suggestion')[[product_col, price_col, 'real_time_price', 'predicted_price', 'optimization_suggestion', 'price_source']].to_string(index=False)}
    3. Dynamic Recommendations:
       {recommendations}
    4. A visualization of the price-demand relationship has been saved as 'price_demand_analysis.png'
    """
    return summary


def extract_relevant_info(query, search_results):
    combined_text = " ".join([result["snippet"] for result in search_results])
    summary = summarizer(combined_text, max_length=150, min_length=50, do_sample=False)[
        0
    ]["summary_text"]
    return summary


def answer_question(question, df, product_col, price_col):
    print(f"Analyzing question: {question}")
    question_sentiment = sia.polarity_scores(question)["compound"]
    print(
        f"Question sentiment: {'Positive' if question_sentiment > 0.05 else 'Negative' if question_sentiment < -0.05 else 'Neutral'}"
    )

    search_results = search_web(question)
    answer = extract_relevant_info(question, search_results)

    if re.search(r"price|cost", question, re.IGNORECASE):
        product_prices = (
            df[[product_col, price_col, "real_time_price", "price_source"]]
            .head()
            .to_string(index=False)
        )
        answer += f"\n\nHere are some sample prices from your data:\n{product_prices}"

    print(f"Answer: {answer}")
    answer_sentiment = sia.polarity_scores(answer)["compound"]
    print(
        f"Answer sentiment: {'Positive' if answer_sentiment > 0.05 else 'Negative' if answer_sentiment < -0.05 else 'Neutral'}"
    )

    print("\nSources:")
    for result in search_results[:3]:
        print(f"- {result['title']}: {result['link']}")

    return answer


def interactive_mode():
    print("Welcome to the Enhanced Pricing Analysis and Web Scraping Tool!")
    print("You can analyze pricing or ask general questions.")

    while True:
        user_input = input(
            "\nEnter 'analyze pricing', your question, or type 'quit' to exit: "
        ).strip()

        if user_input.lower() == "quit":
            print(
                "Thank you for using the Enhanced Pricing Analysis and Web Scraping Tool. Goodbye!"
            )
            break

        if user_input.lower() == "analyze pricing":
            file_path = input(
                "Please provide the path to your product dataset (CSV or JSON format): "
            )
            df, product_col, price_col = load_data(file_path)

            if df is not None:
                print("\nOriginal Dataset Summary:")
                print(f"Dataset shape: {df.shape}")
                print(f"Columns: {', '.join(df.columns)}")

                print(f"\nAnalyzing market prices and optimizing...")
                df = analyze_market_prices(df, product_col, price_col)
                pricing_analysis = analyze_pricing_data(df, product_col, price_col)
                print(pricing_analysis)
        else:
            # For answering questions, we need the dataset. Ask for the path.
            file_path = input(
                "Please provide the path to your product dataset (CSV or JSON format): "
            )
            df, product_col, price_col = load_data(file_path)

            if df is not None:
                answer = answer_question(user_input, df, product_col, price_col)
                print(f"Answer: {answer}")


if __name__ == "__main__":
    interactive_mode()

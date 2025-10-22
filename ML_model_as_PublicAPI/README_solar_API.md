# 🌞 Solar Power Prediction API

This project demonstrates how to build and deploy a **Support Vector Regression (SVR) model** for predicting solar power generation, and then expose it as a **public API** using **Flask** and **ngrok**.

---

## 📂 Project Structure

```
├── SVR_model_solar.ipynb               # Notebook to train & evaluate SVR model for solar prediction
├── solar_svr_model.joblib              # Trained SVR model saved for deployment
├── Deploying_ML_model_as_public_API_ngrok.ipynb  # Notebook to deploy model as REST API with ngrok
└── README.md                           # Project documentation
```

---

## 🚀 Features
- Train an SVR model on solar-related data
- Save the trained model as a `.joblib` file
- Deploy the model as a REST API using Flask
- Expose the API to the internet with **ngrok**

---

## ⚙️ Requirements

Install dependencies:
```bash
pip install numpy pandas scikit-learn flask joblib pyngrok
```

---

## 📖 Usage

### 1. Train the Model
Run the notebook:
```bash
jupyter notebook SVR_model_solar.ipynb
```
This trains the **SVR model** and exports it as `solar_svr_model.joblib`.

### 2. Deploy as API
Open:
```bash
jupyter notebook Deploying_ML_model_as_public_API_ngrok.ipynb
```
This notebook:
- Loads `solar_svr_model.joblib`
- Starts a **Flask API**
- Uses **ngrok** to create a public endpoint

### 3. Send a Prediction Request
Once the ngrok URL is available (e.g., `https://xxxx-xx-xx-xx.ngrok-free.app/predict`), send a POST request with input data:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"feature1": value1, "feature2": value2, ...}' https://xxxx-xx-xx-xx.ngrok-free.app/predict
```

---

## 📊 Example Response

```json
{
  "prediction": 123.45
}
```

---

## 🌟 Future Improvements
- Add authentication for API access
- Containerize using Docker
- Integrate with cloud deployment platforms (AWS, GCP, Azure)

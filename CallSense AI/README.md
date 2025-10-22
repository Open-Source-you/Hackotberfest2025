# 📞 CallSense-AI  
_Analyze customer call transcripts with AI-powered summarization & sentiment detection._  

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)  

---

## 🚀 Overview  
**CallSense-AI** is a Python-based application that processes customer call transcripts to generate **concise summaries** and detect the **customer’s sentiment**. The results are saved into a structured **CSV file**, making it easier for businesses to analyze customer interactions at scale.  

This project demonstrates how **LLMs + sentiment analysis** can streamline customer support and feedback insights.  

---

## ✨ Features  
- 📝 Input a **customer call transcript** (via API endpoint or command line).  
- 🤖 Uses **Groq API** to:  
  - Summarize conversations into 2–3 sentences.  
  - Classify sentiment as **Positive / Neutral / Negative**.  
- 📊 Saves results into `call_analysis.csv` with the following columns:  
  - **Transcript | Summary | Sentiment**  
- 🖥️ Prints results directly in the console for instant feedback.  

---

## ⚙️ Tech Stack  
- **Python 3.9+**  
- **FastAPI / Flask** (for endpoints, if running as a service)  
- **Groq API** (for summarization & sentiment analysis)  
- **Pandas** (for CSV handling)  

---

## 📂 Project Structure  

```bash
CallSense-AI/
│
├── app.py              # Main application script
├── requirements.txt    # Dependencies
├── call_analysis.csv   # Output file (generated after running)
├── .env                # API key configuration (not included in repo)
└── README.md           # Project documentation
```
---
🤝 Contributing
---
Contributions are welcome! 
Feel free to fork the repo and submit pull requests with improvements or new features.

👩‍💻 Author & Maintainer
---
Built with ❤️ by Prachi Choudhary

🔗 GitHub:   https://github.com/prachichoudhary2004

💼 LinkedIn: https://www.linkedin.com/in/prachichoudhary2004

✉️ Email:   prachichoudhary.0504@gmail.com

⭐ Support
---
If you find this project helpful, please consider giving it a star ⭐ on GitHub!

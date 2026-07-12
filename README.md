# 🏏 IPL Cricket Analytics Dashboard

An end-to-end data science project analyzing **17 years of IPL data (2008–2024)** 
with an interactive dashboard and ML-powered match winner predictor.

🔗 **Live Demo:** https://ipl-analytics-with-prediction.streamlit.app

---

## 📊 Features

- **KPI Tracking** — Total matches, runs, wickets and sixes across all seasons
- **Team Analysis** — Most wins by team across all IPL seasons
- **Batting Analysis** — Top run scorers with interactive filters
- **Bowling Analysis** — Top wicket takers
- **Toss Analysis** — Does winning the toss actually help?
- **ML Match Predictor** — Predict match winner based on teams, toss and venue

---

## 🛠️ Tech Stack 

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Pandas | Data manipulation and analysis |
| SQLite | Database storage and SQL queries |
| Scikit-learn | Machine learning (Random Forest) |
| Plotly | Interactive charts |
| Streamlit | Web dashboard and deployment |

---

---

## 🚀 Run Locally

```bash
# Clone the repository
git clone https://github.com/Vanshsrivastava09/Cricket-Analytics.git
cd Cricket-Analytics

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run dashboard/app.py
```

---

## 🤖 ML Model Details

- **Algorithm:** Random Forest Classifier (100 estimators)
- **Features:** Team 1, Team 2, Toss Winner, Toss Decision, Venue
- **Training Data:** 872 matches
- **Note:** Cricket match outcomes depend heavily on in-game factors 
  like pitch conditions, player form and weather — making prediction 
  inherently challenging. This model demonstrates the ML pipeline 
  end-to-end using available pre-match data.

---

## 📈 Key Insights from the Data

- Mumbai Indians are the most successful IPL team with 150+ wins
- Virat Kohli leads all-time run scorers with 8,014 runs
- Teams winning the toss choose to field ~60% of the time
- IPL expanded from 58 matches in 2008 to 74 matches in recent seasons

---

## 🤖 ML Model Details

- **Algorithm:** Random Forest Classifier (100 estimators)
- **Features:** Team 1, Team 2, Toss Winner, Toss Decision, Venue
- **Training Data:** 872 matches
- **Note:** Cricket match outcomes depend heavily on in-game factors 
  like pitch conditions, player form and weather — making prediction 
  inherently challenging. This model demonstrates the ML pipeline 
  end-to-end using available pre-match data.

---

## 📈 Key Insights from the Data

- Mumbai Indians are the most successful IPL team with 150+ wins
- Virat Kohli leads all-time run scorers with 8,014 runs
- Teams winning the toss choose to field ~60% of the time
- IPL expanded from 58 matches in 2008 to 74 matches in recent seasons

## 👤 Author

**Vansh Srivastava**  
B.Tech CSCE, KIIT University  
[LinkedIn](https://www.linkedin.com/in/vanshsrivastava09/) | 
[GitHub](https://github.com/Vanshsrivastava09)

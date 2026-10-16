# AI-Powered Student Performance & Career Prediction System

This project is a beginner-friendly but professional academic mini-project built with Python and Streamlit. It predicts a student's final academic performance, suggests a suitable career domain, identifies academic support needs, and recommends skills to develop.

## Features

- Student profile entry form
- Academic performance prediction using regression models
- Career domain prediction using classification models
- Academic support risk classification
- Skill gap and learning recommendations
- Interactive Plotly dashboards
- MySQL integration for saving predictions
- Synthetic demo dataset for development and testing
- Model training scripts for reproducibility
- Error handling and validation

## Technology Stack

- Python 3.11+
- Streamlit
- Pandas, NumPy
- Scikit-learn
- Plotly
- MySQL + mysql-connector-python
- SQLAlchemy
- joblib
- python-dotenv

## Project Structure

- app.py
- data/student_data.csv
- database/schema.sql
- models/
- pages/
- src/
- tests/

## Installation

1. Open VS Code and create a project folder.
2. Open a terminal in the project folder.
3. Create a virtual environment:

```bash
python -m venv venv
```

4. Activate the virtual environment:

Windows:

```bash
venv\Scripts\activate
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env` and update MySQL settings if you want database storage enabled.

## MySQL Setup

Create a MySQL database named `student_career_prediction` and run the SQL script in `database/schema.sql`.

Example:

```sql
CREATE DATABASE student_career_prediction;
USE student_career_prediction;
```

Then load the schema file with your preferred MySQL client.

For an existing database created before the support-risk input fields were added, run `database/migrate_support_risk_features.sql` once before using the MySQL-backed risk dashboard.

## Model Training

Run the following scripts before starting the app:

```bash
python src/train_performance_model.py
python src/train_career_model.py
python src/train_risk_model.py
```

These scripts generate the trained model files inside the `models/` folder.

## Running the App

```bash
streamlit run app.py
```

The app will open in the browser and allow student input, performance prediction, career recommendations, and support analysis.

## Important Notes

Predictions are estimates generated from available educational data and should be used as guidance, not as definitive judgments of ability or future outcomes.

This project uses synthetic/demo data for academic demonstration purposes only. It does not claim to represent real student populations.

## Future Improvements

- Add actual authentication for student and admin access
- Replace synthetic dataset with real institutional records
- Connect to a production-grade data warehouse
- Add LLM-based explanations with fallback rule-based advice
- Add more detailed career-specific skill libraries

## Presentation Guidance

During a college presentation, show:

1. Student profile form
2. Performance prediction output
3. Career recommendation with probability scores
4. Skill gap chart
5. Academic support recommendations
6. Admin analytics dashboard

This demonstrates the full machine learning lifecycle from data to deployment.

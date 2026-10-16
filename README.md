# INTRODUCTION 

## Project name: 
-AssetIQ AI - Predict failures. Optimize maintenance. Protect operations.

AssetIQ AI is an end-to-end AI prototype for predictive maintenance and asset intelligence. It helps maintenance teams in mining, energy, transport, telecoms, water and other asset-heavy industries decide which equipment needs attention first.

Built by Elzel de Beer as the End-to-End AI Solution project.

## ACCESS THE APP: 
-----

## The problem

Unplanned equipment failure causes downtime, expensive repairs, disrupted services and safety risks. Many organisations either follow a fixed maintenance schedule or react after something breaks. AssetIQ AI uses sensor and maintenance data to answer five questions:

| Question | What AssetIQ does |

| What might fail? | Scores each asset's probability of failing |
| When might maintenance be needed? | Estimates days left on the simulated fleet (not possible on AI4I, which has no time-to-failure) |
| What's unusual? | Flags readings that drift from normal operation |
| What should be prioritised? | Ranks assets by risk and the cost of a stoppage |
| What should happen next? | Suggests an action for a qualified person to review |

## How it works

mermaid
flowchart LR
    A[Sensor and maintenance data] --> B[Feature engineering]
    B --> C[Failure risk model]
    B --> D[Failure mode model]
    B --> E[Anomaly detector]
    C --> F[Priority ranking]
    D --> G[Recommended action]
    E --> F
    F --> H[Dashboard and weekly report]
    G --> H
    H --> I[Qualified person reviews and approves]
```

## Two layers, and why

1. **Model validation on a public dataset (the real evidence).** The models are trained and tested on the [AI4I 2020 Predictive Maintenance Dataset](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset) from the UCI Machine Learning Repository (10,000 records, about 3.4% failures, CC BY 4.0). It is a **synthetic benchmark** made by researchers to resemble industrial failures, not data from a real plant, but it is independent of my own assumptions.
2. **Demo fleet (the product experience).** The main dashboard shows a **simulated South African fleet** of 48 assets across five industries, with rand costs and a load-shedding stress factor. All of this is simulated and every cost is an assumption. It exists to show the workflow, not to prove accuracy.

You can also upload your own CSV of sensor readings. Scores for uploaded data come from the simulated-data model, so treat them as indicative until the model is retrained on your own failure history.

## Models (AI4I)

| Task | Model | Notes |
|---|---|---|
| Will it fail? | Random Forest | Class-weighted for rare failures. Compared against a logistic regression baseline |
| Why would it fail? | Random Forest (multi-output) | Predicts tool wear, heat dissipation, power or overstrain failure |
| Is it unusual? | Isolation Forest | Trained on normal operation only |

Engineered features: process-to-air temperature gap and mechanical power (torque x speed), which match the physics behind the failure modes.

**How it is evaluated:** a stratified 75/25 train/test split. The decision threshold is chosen with cross-validation on the training rows only, so the test set stays untouched. Accuracy is not reported, because a model that always predicts "no failure" is already about 96.6% accurate. Precision, recall and PR-AUC are used instead.

### Results

Run `python train_ai4i.py` and paste your numbers here:

| Model | Precision | Recall | F1 | PR-AUC |
|---|---|---|---|---|
| Logistic regression (baseline) | | | | |
| Random Forest (AssetIQ) | | | | |

Top 10% of machines by risk capture ____% of failures on the held-out test set.

## Run it locally

```
python -m venv venv
venv\Scripts\activate          # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
```

1. Download `ai4i2020.csv` from the UCI link above and save it as `data/ai4i2020.csv`.
2. Start the app: `python -m streamlit run app.py`. The first time you open the **Real Data AI4I** page, the models train automatically (about a minute) and are saved in `models/`. You can also train manually with `python train_ai4i.py`.

On Windows you can double-click `START_HERE.bat` to set everything up and start the app in one go.

The demo fleet works without the dataset. The **Real Data AI4I** page needs it. To deploy on Streamlit Cloud, commit `data/ai4i2020.csv` (CC BY 4.0) so the page can train on first load.

**Web dashboard (no Python needed):** open the web version of the dashboard, go to the *Real data* section, click *Train from ai4i2020.csv* and choose the dataset file. The model trains in your browser in a few seconds and nothing is uploaded. It uses the same approach as the Python version (a class-weighted Random Forest compared with a logistic baseline, a failure-cause model, and a threshold tuned without touching the test set). You can also load `models/web_export.json`, which `train_ai4i.py` writes, to show the Python model in the browser.

## PROJECT STRUCTURE 

app.py         ->             Landing page (start here)
pages/1_Dashboard.py ->       Dashboard on the simulated South African fleet
pages/2_Real_Data_AI4I.py ->  Model evidence, ranking real machines, score-a-machine tool
train_ai4i.py         ->      Trains and evaluates the AI4I models
ai4i_features.py       ->     Feature engineering and scoring shared by training and the app
theme.py, art.py         ->   Look and feel: stippled heat backgrounds, heat map graphic, chart panels
assets/                  ->   Photos used on the landing page
.streamlit/config.toml   ->   Dark theme settings
data/                    ->   Put ai4i2020.csv here
models/                  ->   Created by training (model, metrics, held-out test set, web_export.json)


## RESPONSIBLE AI 

Human in the loop: The system only suggests actions. A qualified person approves every inspection or repair, and the dashboard asks for that confirmation.
Honest about data: The benchmark and the demo fleet are both synthetic, and the app says so.
Rare-event evaluation: Metrics were chosen for imbalanced failures, and the threshold was tuned without touching the test set.
Explainable: Feature importance and a predicted failure mode accompany each score.
Safety context: In regulated settings such as mining, the output supports and never replaces statutory safety inspections.

## Limitations

- AI4I is synthetic. Strong results on it do not guarantee the same results on a real plant.
- AI4I has no time-to-failure, so remaining useful life is only shown on the simulated fleet.
- The simulated fleet's costs, downtime hours and load-shedding effect are assumptions.
- Uploaded CSVs must use the expected units (vibration in mm/s, temperature in C, pressure in bar) and are scored by a model trained on simulated data.

## Next steps

- Retrain on a client's real maintenance history and failure logs.
- Add remaining-useful-life models using run-to-failure data such as NASA C-MAPSS.
- Add a conversational assistant for questions about the fleet.
- Connect to a live sensor feed and a work-order system.

## Data credit

AI4I 2020 Predictive Maintenance Dataset, UCI Machine Learning Repository, licensed CC BY 4.0. Introduced in S. Matzka, "Explainable Artificial Intelligence for Predictive Maintenance Applications", 2020.

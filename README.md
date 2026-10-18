# INTRODUCTION:

## PROJECT NAME

- AssetIQ AI - Predict failures. Optimize maintenance. Protect operations.

## BACKGROUND INFORMATION

AssetIQ AI is an end-to-end AI prototype for predictive maintenance and asset intelligence. Unplanned equipment failure causes downtime, expensive repairs, disrupted services and safety risks, and many organisations still follow a fixed maintenance schedule or react after something breaks. AssetIQ AI reads sensor data and answers five questions: what might fail, when maintenance may be needed, what is unusual, what should be prioritised, and what should happen next. It is designed for mining, energy, transport, telecoms, water and other asset-heavy industries. The app opens on a landing page, and the analysis follows on the dashboard and model evidence pages.

## ACCESS THE TOOL USING THE LINK:

- https://assetiq-jvh8uobwyowpy8hpio6ist.streamlit.app/
- Nota Bene: If the app has been asleep, the first load can take a minute.

## ASSETIQ AI PREVIEW

<img width="1578" height="755" alt="assetiq 5" src="https://github.com/user-attachments/assets/f131cb1e-79d5-40c7-b6cb-19cac6db53c4" />
<img width="1581" height="768" alt="assetiq 2" src="https://github.com/user-attachments/assets/1300ff81-7145-4d72-befc-219f256a1c92" />
<img width="1500" height="755" alt="assetiq 7" src="https://github.com/user-attachments/assets/02a1f6b8-5d70-4b8a-9d8e-80ef53503041" />
<img width="1577" height="758" alt="assetiq 6" src="https://github.com/user-attachments/assets/329077d9-caa7-45af-b5b4-e5899e7f13dc" />
<img width="1559" height="763" alt="assetiq 4" src="https://github.com/user-attachments/assets/50d54e9d-b488-4aac-af4d-2ec0c7ca4b79" />
<img width="959" height="491" alt="assetiq0" src="https://github.com/user-attachments/assets/f88a3253-0edc-4b2e-9700-de83f1c2fc28" />

## What AssetIQ AI does:

- Predicts failure risk: gives every asset a 30-day failure probability and an estimate of days left, from sensor readings such as vibration, temperature, pressure, load and age.
- Flags what is unusual: readings that drift away from normal operation are marked on a timeline for each asset.
- Ranks what to do first: combines failure risk with the cost of a stoppage into one priority list, and shows the riskiest asset as a thermal heat map.
- Suggests the next action: each recommendation names the likely cause and is written for a qualified person to review and approve.
- Simulates maintenance strategies: compares reactive, scheduled and predictive maintenance using crew size, inspections per week and inspection catch rate.
- Writes a weekly report: summarises the fleet and the top priorities in plain English, and lets you download it (Markdown).
- Accepts your own data: upload a CSV of sensor readings and the tool scores it. A template is provided.
- Tests the model on a public benchmark: the model evidence page trains and tests on the AI4I 2020 dataset and ranks real held-out machines against what actually happened.
- Keeps art and data separate: the stippled heat backgrounds are decoration only, and every real chart sits on a solid black panel.
- Includes a demo fleet: a simulated South African fleet of 48 assets across five industries, with rand costs and a load-shedding stress factor, so a user can try it without a file.

## How it works

- Sensor readings are loaded and cleaned, and rows with missing sensor values are skipped.
- A Random Forest scores each asset's chance of failing in the next 30 days, and a Gradient Boosting model estimates days left. An Isolation Forest, trained on normal operation only, flags unusual readings.
- Failure risk is multiplied by the cost of downtime for that industry, so a likely failure on a critical asset ranks above a likely failure on a minor one.
- On the AI4I page, a Random Forest predicts failure and a second model predicts the likely cause (tool wear, heat dissipation, power or overstrain), compared against a logistic regression baseline.
- The decision threshold is chosen with cross-validation on the training rows only, so the test machines stay untouched. Accuracy is not reported, because a model that always predicts "no failure" is already about 96.6% accurate. Precision, recall and PR-AUC are used instead.
- The riskiest assets become ranked, plain-English actions that wait for a qualified person to approve them.
- Charts are drawn with Altair, and the stippled background art is generated in Python and cached.

Two layers are used on purpose:

1. A public benchmark (AI4I 2020) gives honest evidence about the model. It is a synthetic dataset made by researchers to resemble industrial failures, not data from a real plant.
2. A simulated South African fleet shows the product experience. Its costs, downtime hours and load-shedding effect are assumptions.

Model results on the held-out AI4I test set (run the model evidence page and copy your numbers here):

| Model | Precision | Recall | F1 | PR-AUC |
|---|---|---|---|---|
| Logistic regression (baseline) | | | | |
| Random Forest (AssetIQ) | | | | |

## TECH STACK

- Programming language used: Python 3
- Web app: Streamlit
- Machine learning: scikit-learn (Random Forest, Gradient Boosting, Isolation Forest, Logistic Regression)
- Data handling: pandas, NumPy, joblib
- Charts: Altair
- Generative artwork: stippled heat backgrounds and the thermal heat map, drawn in Python (NumPy and SVG)
- Dataset: AI4I 2020 Predictive Maintenance Dataset (UCI Machine Learning Repository)
- Styling: Custom CSS, Google Fonts (Michroma, Inter Tight, Newsreader, JetBrains Mono)
- Hosting: Streamlit Community Cloud

## PROJECT STRUCTURE

```
assetiq/
├── app.py                 # Entry point: sets up the pages and navigation
├── views/
│   ├── home.py            # Landing page
│   ├── dashboard.py       # Dashboard on the simulated South African fleet
│   └── evidence.py        # Model evidence on AI4I, ranking real machines, score a machine
├── train_ai4i.py          # Trains and evaluates the AI4I models
├── ai4i_features.py       # Feature engineering and scoring shared by training and the app
├── theme.py               # Look and feel: backgrounds, heat card, chart panels
├── art.py                 # Generates the stippled heat artwork and the thermal graphic
├── assets/                # Photos used on the landing page
├── data/                  # Put ai4i2020.csv here (optional)
├── requirements.txt       # Python libraries the app needs
├── START_HERE.bat         # Windows one-click setup and start
└── .streamlit/
    └── config.toml        # Dark theme colours
```

## GETTING STARTED

You need Python 3.10 to 3.12 installed. Download it from python.org and tick "Add Python to PATH" in the installer.

Download the project (Code, then Download ZIP on GitHub) and extract it.

### FOR Windows

The quick way: double-click `START_HERE.bat` in the project folder. It sets everything up and starts the app.

The manual way: open Command Prompt inside the project folder (type `cmd` in the folder's address bar and press Enter), then run these one at a time:


py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


The app opens in your browser at http://localhost:8501. To stop it, press Ctrl+C in the terminal.

### IN VS Code

1. Open VS Code and choose File, then Open Folder, and select the project folder.
2. Choose Terminal, then New Terminal. It opens inside the project folder.
3. Run the same four commands as in the Windows section above.
4. If PowerShell says "running scripts is disabled", run this once and repeat the activate line:

Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

You can also switch the terminal to Command Prompt using the arrow next to the + button.

### FOR Mac and Linux

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m streamlit run app.py


## TROUBLESHOOTING

- "streamlit is not recognized": the virtual environment is not active, so run the activate line again and use `py -m streamlit run app.py`.
- "requirements.txt not found": the terminal is open in the wrong folder. Type `dir` (Windows) or `ls` (Mac/Linux) and check that `app.py` and `requirements.txt` are listed. If you only see one folder, run `cd` into it.
- "python is not recognized": Python is not installed, or "Add Python to PATH" was not ticked. Reinstall it, or use `py` instead of `python`.
- The page looks unstyled or old: press Ctrl+Shift+R in the browser to force a refresh.
- The sidebar is missing: click the small arrow at the top left to open it.
- The model evidence page asks for a file: upload `ai4i2020.csv` (from the UCI page) on that page. The model then trains automatically, which takes about a minute.
- "This file is missing columns": your sensor CSV needs the columns asset, vibration, temperature and pressure. Download the template from the dashboard to see the format.
- The app crashes on Streamlit Community Cloud: check that an old `pages` folder is not left in the repository, that `venv`, `models` and `__pycache__` were not uploaded, and set the app's Python version to 3.12 in its settings.
- Still stuck: copy the last lines of the error and check them against the logs ("Manage app" on Streamlit Cloud).

## USING THE TOOL

1. Open the app. The landing page introduces AssetIQ AI. Use the buttons to open the dashboard or the model evidence page.
2. On the Dashboard, choose which industries to include and set the load-shedding stage. Use the slider to step through the riskiest assets and read the heat-map card.
3. Use the tabs: Overview (health by industry and all assets ranked), Anomalies (pick an asset and a sensor), Priorities and actions (suggested actions with a "reviewed by a qualified person" tick), Simulation (compare maintenance strategies), and Report (the weekly summary, which you can download).
4. To score your own data, open "Upload your own sensor CSV" on the dashboard and add a file. Required columns: asset, vibration (mm/s), temperature (°C), pressure (bar). Optional: sector, site, crit (1 to 5), date, load, age. Several dated rows per asset switch on the anomaly timeline.
5. On the Model evidence page, upload `ai4i2020.csv` if asked. Read the Evidence tab for precision, recall and what drives failures, use Rank real machines to see the highest-risk test machines against what actually happened, and use Score a machine to try your own readings.

## PRIVACY

- Files you upload to the dashboard are read in memory for your session only. They are not saved by the app, and there are no accounts or tracking.
- The model evidence page saves the public AI4I file and the trained model on the server it runs on. This is a public benchmark dataset, not personal data.
- On Streamlit Community Cloud your session runs on Streamlit's servers, so do not upload confidential or sensitive data to the public demo. For sensitive data, run the tool on your own computer.

## LIMITATIONS

- The AI4I benchmark is synthetic, so strong results on it do not guarantee the same results on a real plant.
- AI4I has no time-to-failure information, so days left is only estimated on the simulated fleet.
- The demo fleet is simulated. Its repair costs, downtime hours, rand-per-hour costs and the load-shedding effect are assumptions.
- A CSV you upload on the dashboard is scored by a model trained on simulated data, so treat the results as indicative until the model is retrained on your own failure history. Use the expected units (mm/s, °C, bar) or the scores will not make sense.
- The tool only suggests actions. It does not replace statutory safety inspections or the judgement of a qualified person.
- Results depend on the quality and units of the data, and rare failures are hard to predict.
- It is a prototype: there is no live sensor feed, no work-order system and no user accounts.
- The first training run on the model evidence page takes about a minute.

## FUTURE IMPROVEMENTS

- Retrain the models on a client's real maintenance history and failure logs.
- Add remaining-useful-life models using run-to-failure data such as NASA C-MAPSS.
- Score uploaded sensor files with the AI4I-trained model.
- Add a conversational assistant for questions about the fleet.
- Connect to a live sensor feed and a work-order system.
- Add explainability for each score, for example SHAP values.
- Add automated tests and a Jupyter notebook that walks through the training.

## DEPLOYMENT

The app is deployed on [Streamlit Community Cloud](https://streamlit.io/cloud).

## AUTHOR

This tool was built by me, Elzel Qoqokwakhe De Beer

## ACKNOWLEDGEMENTS

- AI4I 2020 Predictive Maintenance Dataset, UCI Machine Learning Repository, licensed CC BY 4.0. Introduced in S. Matzka, "Explainable Artificial Intelligence for Predictive Maintenance Applications", 2020.
- Streamlit, scikit-learn, pandas, NumPy and Altair, the open-source libraries that power the app.
- Google Fonts for Michroma, Inter Tight, Newsreader and JetBrains Mono.
- Photographs on the landing page by: 

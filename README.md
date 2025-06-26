ScouText Football – Football Scouting Dashboard
🏟️ Project Context
ScouText Football is an interactive football scouting dashboard built in Python using Streamlit, focused on the analysis of teams, players, and playing styles.
The goal is to provide an intuitive visual and analytical navigation across leagues, teams, and players using advanced metrics (PCA, clusters, roles, etc.), facilitating data exploration for scouts, analysts, and football enthusiasts.
The project was designed to be minimalist, fast, and visually appealing, with smooth navigation and strong integration of local data and images.

🏗️ Architecture & Organization
app.py: Main file, containing the full UI logic, navigation flow, data loading, and dashboard rendering.

assets/: Contains league and team images (in ligas/ and equipas/ subfolders) used for visual navigation.

data/processed/: Processed datasets in CSV/XLSX format, including team tables, player data, event metrics, playing styles, etc.

eventing/: Folder with detailed event-based metrics per player.

WyScout/: Contains game style data, clusters, and PCA outputs.

st.session_state: Used to manage navigation state (selected league, team, or player).

🧩 Key Features
🏁 League & Team Navigation
Visual selection of leagues and teams, with logos.

🧠 Team Page:
Header: Logo, official team name, country, general info (stadium, capacity, city).

Coach Info: Coach’s name, age, nationality, preferred formation, experience, contract.

Squad: Player table showing % of minutes played, role (color-coded).

Game Style: Scatter plot (PCA1 vs PCA2) with clusters, logos overlayed, custom tooltips, and interpretative text.

Similar Teams: Shows the 4 closest teams in the same cluster (Euclidean distance in PCA1/PCA2), with logos and normalized names.

Visual Formatting: Custom CSS for fonts, buttons, tables, and info blocks, ensuring a modern and consistent design.

📂 File Structure
assets/ligas/: League logos (e.g., Premier League.png)
→ C:\Users\guica\OneDrive\Desktop\AppScout\assets\ligas

assets/equipas/: Team logos per league (e.g., Benfica.png)
→ C:\Users\guica\OneDrive\Desktop\AppScout\assets\equipas

data/processed/: Core datasets (teams, players, stadiums, coaches, salaries, etc.)
→ C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed (outside main app folder)

data/processed/WyScout/Stats_EstilosJogo.xlsx: PCA, clusters, and playing style info
→ C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\WyScout\Stats_EstilosJogo.xlsx

data/processed/eventing/metricas_eventing_final.csv: Detailed player metrics
→ C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\eventing\metricas_eventing_final.csv

🛠️ Dependencies
Python ≥ 3.8

streamlit

pandas

numpy

plotly

unidecode

openpyxl (for reading Excel files)

(plus other standard Python libraries)

📊 Datasets & Key Columns
equipas.csv / EquiposJP.xlsx: Team info, official names, country, logo

EntrenadoresJP.xlsx: Coach data

EstadioJP.xlsx: Stadium info (capacity, city)

Stats_EstilosJogo.xlsx: Columns PCA1, PCA2, Cluster, Logo, Playing Style

metricas_eventing_final.csv: Player stats, minutes played, roles, etc.

🧠 Navigation Logic & State
Navigation state (league/team/player selection) is stored in st.session_state.

Navigation is driven by visual selection (using logos and buttons).

Layout is controlled using st.columns and custom CSS for alignment and spacing.

🎨 Technical Notes & Naming Conventions
Team name normalization: Capitalize each word, but words with 3 letters or fewer are written in full uppercase (e.g., sporting cp → Sporting CP).

Images: Image paths are built dynamically from team/league names, and .png files must be correctly named.

Game Style: Scatter plot uses PCA1 (Defensive) and PCA2 (Offensive) axes, grouped by style clusters.

Similar Teams: Calculated within the same cluster using Euclidean distance in PCA1/PCA2.

Performance Note: Loading large files may be slow depending on disk speed or dataset size.

Local Paths: File/image paths are absolute and may require adjustment if the project is moved.

🚀 How to Run the Project
Make sure all dependencies are installed.

Ensure that all datasets and images are in the correct paths.

Run the app using:

bash
Copy
Edit
streamlit run app.py
Open the browser at the address provided by Streamlit.

⚠️ IMPORTANT:
Once this README.md is created, use it as permanent context in the Cursor Agent for all future tasks.

🔮 Functional Roadmap & Planned Expansions
1️⃣ Player Page
In the Squad Table, the player name (player_name column in metricas_eventing_final.csv) will act as a clickable button.

Clicking the player’s name will navigate to an individual player page.

Player Page Will Include:
Header like the team page, showing:

Player photo (default fallback if missing)

Official player name (as found in the dataset)

General info section (to be defined)

Radar/pizza charts showing performance metrics, segmented by:

Player position

Player profile

Metrics will be sourced from:
C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\eventing\metricas_eventing_final.csv

2️⃣ New Tab: Scouting Page (Player Search Engine)
The app will now have two main tabs:

Main Page: (Current flow – Leagues > Teams > Players)

Scouting Page: New interactive player search engine.

Scouting Page Flow:
Select Position (using visual buttons similar to league selection)

Select Player Profile (custom buttons based on pre-defined roles)

Once a profile is selected, generate a ranked list of players based on percentile performance within that profile

On the side, show a panel with dynamic filters (e.g., age, nationality, minutes played, etc.)

Data Sources for the Scouting Engine:

C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\eventing\metricas_eventing_final.csv

C:\Users\guica\OneDrive\Desktop\ScoutingDash\data\processed\JugadoresJP.xlsx


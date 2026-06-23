# Astro Magic · Natal Chart

An open source app that calculates an **astrological natal chart** from a birth
date, time and city. Planet/house/aspect calculations are done with Swiss
Ephemeris (`pyswisseph`); the React based UI renders the chart drawing, planet &
house tables, aspects and personalized notes.

This repo contains only the **natal chart** feature of the AstroMagic project
that is live at [www.astromagic.com.tr](https://www.astromagic.com.tr). It does
not include membership, profile, payment or similar sections.

## Features

- Natal chart calculation from birth details (`/api/natal-chart`)
- Natal chart drawing on a canvas
- Planet, house (Placidus) and aspect tables
- Personalized notes matched against the natal chart (`/api/special-notes`)
- Embedded coordinates for all 81 cities of Türkiye (works without internet)

![Special Notes](images/note.png)


## Project Structure

```
astromagic-natal-chart/
├── backend/            # Flask API
│   ├── app.py          # App entry point (chart + notes blueprints)
│   ├── natal_chart.py  # Chart calculation with Swiss Ephemeris
│   ├── special_notes.py# Personalized note rules
│   ├── routes/         # /api/natal-chart and /api/special-notes
│   ├── ephe/           # Swiss Ephemeris data files
│   └── requirements.txt
└── frontend/           # React + Vite UI
    └── src/
        ├── pages/      # Home (form) and Result (chart)
        └── components/ # Navbar
```

## Setup

### 1. Backend (Flask)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The API runs at `http://localhost:5001`.

### 2. Frontend (React + Vite)

In a new terminal:

```bash
cd frontend
npm install
npm run dev
```

The UI opens at `http://localhost:5173`. Vite automatically proxies `/api`
requests to the backend (`http://localhost:5001`).


![Special Notes](form/form.png)

## How It Works

1. On the home page you enter name, birth date/time and city.
2. The frontend sends a request to the `/api/natal-chart` endpoint.
3. The backend computes planet and house positions with Swiss Ephemeris.
4. The result page draws the chart and shows the tables and matched notes.



## License

This project is licensed under the MIT License — see [LICENSE](LICENSE).

Note: Swiss Ephemeris (`pyswisseph`) is dual-licensed under AGPL and a
commercial license. If you plan to use this in a closed-source product,
check [Astrodienst's terms](https://www.astro.com/swisseph/).

---

Built by [www.astromagic.com.tr](https://www.astromagic.com.tr)

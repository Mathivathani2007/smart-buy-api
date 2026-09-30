# SmartBuy AI

SmartBuy AI turns a product photo into a clear buying decision: identify the likely product, compare permitted marketplace listings, understand review signals, and choose the strongest value.

## What is included

- Responsive React/Vite interface with drag-and-drop image upload, preview, validation, manual search, loading stages, results, comparison cards, review intelligence, and transparent scoring.
- FastAPI API preserving `GET /` and `GET /health`, plus `/api/analyze`, `/api/compare`, `/api/reviews/analyze`, and `/api/demo/products`.
- Provider adapters for Amazon, Flipkart, Meesho, and Myntra, all returning the same normalized product model.
- Catalog-constrained vision matching: configured Google/OpenAI vision selects from the existing product catalog, then the shared matcher returns all four marketplace listings for the detected product.
- Safe demo fallback when no approved AI credentials are configured; image filenames can identify an explicitly named catalog product, while unclear images return a no-match message.
- Optional MongoDB connection for future `products`, `comparisons`, and `analysis_history` persistence.

## Run it

### Backend

From `backend/`, create `.env` from `.env.example` when needed, then run:

```powershell
py -m pip install -r requirements.txt
py -m uvicorn main:app --reload --port 8001
```

### Frontend

From `frontend/`:

```powershell
npm install
npm run dev
```

Open `http://localhost:5173`.

## Environment

`MONGODB_URL`, `AI_API_KEY`, and `AI_MODEL` are optional. For Google AI Studio, set `AI_PROVIDER=google` and use a Gemini vision model such as `gemini-2.0-flash`. For OpenAI-compatible vision, set `AI_PROVIDER=openai`. `FRONTEND_URL` documents the frontend origin. The demo works without MongoDB or an AI key, and secrets are never sent to the frontend.

Image analysis supplies the vision model with the products currently in `backend/data/demo_products.json`; it does not maintain a separate image database. Text search and image search both use the same catalog matcher. Each product family currently has Amazon, Flipkart, Myntra, and Meesho listings.

## API

- `GET /` and `GET /health`
- `POST /api/analyze` with multipart field `image`
- `POST /api/compare` with JSON `product_name`, optional `brand`, `category`, and `keywords`
- `POST /api/reviews/analyze` with the same comparison request
- `GET /api/demo/products`

## Marketplace data disclaimer

The included listings are clearly marked `source: demo sample data` and are for a hackathon demonstration only. No unauthorized scraping or marketplace protection bypass is used. Replace each provider's `search` method with an official API or other permitted data source before production use.

## Architecture

`main.py` owns app setup and CORS. Routes validate transport inputs, services own image validation, identification, matching, review analysis, scoring, and optional persistence, and provider adapters isolate marketplace-specific integrations. The UI calls the backend only through `frontend/src/services/api.js`.

## Scoring

SmartBuy Score is deterministic and weighted: 35% price, 25% rating, 20% review sentiment, 10% review volume, and 10% product match confidence. Missing values receive a conservative fallback rather than inventing data.

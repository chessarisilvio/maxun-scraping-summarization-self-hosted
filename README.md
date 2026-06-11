# Maxun: Scraping & Summarization Self-Hosted

A self-hosted pipeline for web scraping and text summarization using local LLMs.

## Descrizione

Maxun estrae contenuti da pagine web e genera sintesi testuali, con architettura pensata per l'integrazione di modelli LLM locali (Qwen3.6) su GPU dedicate. La pipeline è modulare: lo scraping e la summarization sono script Python indipendenti, collegabili a qualsiasi backend di inferenza.

Ideale per:
- Monitoraggio fonti web con sintesi automatica
- Raccolta dati per dataset di training
- Pipeline RAG personalizzate su hardware locale
- Automazione di ricerca e riassunzione di contenuti tecnici

## Architettura

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Sorgente   │────▶│  Scraping    │────▶│  Summarization│
│   Web URL   │     │  (BS4+req)   │     │ (llama-server su :8081 - Qwen3.6) │
└─────────────┘     └──────────────┘     └──────────────┘
                           │                       │
                     data/*.html           output/*_summary.txt
```

- **Scraping** (`src/scrape.py`): fetch HTTP + BeautifulSoup, pulizia HTML, salvataggio in `data/`
- **Summarization** (`src/summarize.py`): lettura file HTML da `data/`, invoca llama-server su `:8081` (sentinel) con modello Qwen3.6, salva sintesi in `output/`
- Entrambi gli script sono indipendenti e possono essere eseguiti separatamente

## Installazione

1. Clona il repository:
   ```bash
   git clone <repository-url>
   cd maxun-scraping-summarization-self-hosted
   ```

2. Installa le dipendenze:
   ```bash
   python3 -m pip install --user --break-system-packages -r requirements.txt
   ```

   Oppure usa un virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. (Opzionale) Configura le variabili d'ambiente:
   ```bash
   cp .env.example .env
   # Modifica .env con i tuoi valori
   ```

## Uso

### Scraping

Estrai il contenuto di una pagina web:

```bash
python3 src/scrape.py <URL>
```

Esempio:
```bash
python3 src/scrape.py https://example.com
```

Il contenuto pulito viene salvato in `data/<hostname>.html`.

### Summarization

Genera sintesi da tutti i file HTML raccolti:

```bash
python3 src/summarize.py
```

Le sintesi vengono salvate in `output/<hostname>_summary.txt`.

### Integrazione con LLM locale

La summarization utilizza già un endpoint llama-server locale sulla porta **8081** (sentinel) con il modello **Qwen3.6-35B-A3B-IQ4_XS**. Non è necessario modificare lo script a meno che non si voglia cambiare endpoint o modello.

Se si desidera puntare a un diverso endpoint:
1. Modifica la variabile d'ambiente `LLAMA_SERVER_URL` in `src/summarize.py` (o impostala esternamente).
2. Assicurati che il modello sia servito da quell'endpoint.

## Esempi

```bash
# Scraping multipli
python3 src/scrape.py https://news.ycombinator.com
python3 src/scrape.py https://arxiv.org/list/cs.AI/recent

# Genera sintesi da tutti i file raccolti
python3 src/summarize.py

# Output: output/news_ycombinator_summary.txt, output/arxiv_summary.txt
```

## Struttura del progetto

```
maxun-scraping-summarization-self-hosted/
├── data/                 # File HTML scraped (hostname.html)
├── output/               # Sintesi generate (hostname_summary.txt)
├── src/
│   ├── scrape.py         # Script di scraping web
│   └── summarize.py      # Script di summarization
├── .env.example          # Variabili d'ambiente placeholder
├── requirements.txt      # Dipendenze Python
└── README.md             # Questa documentazione
```

## Requisiti

- Python 3.12+
- Dipendenze in `requirements.txt`:
  - `requests` — HTTP client
  - `beautifulsoup4` — parsing HTML
  - `tqdm` — barre di progresso

## Privacy e codice pubblico
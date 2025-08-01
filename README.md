# 🧵 Dressify Data Extraction Engine

This repository contains the data extraction and preprocessing pipeline for the **Dressify** app — an AI-powered clothing recommendation system. This module is responsible for collecting, cleaning, and structuring fashion-related data such as clothing types, color palettes, body types, and matching rules to support the Dressify recommendation engine.

---

## 🚀 Project Overview

The Dressify Data Extraction Engine is designed to build a structured knowledge base that powers the intelligent recommendations in the Dressify app. It gathers data from various sources (e.g., CSVs, APIs, web scraping), processes it into usable formats, and stores it for fast retrieval and reasoning by the main application.

---

## ✨ Features

- 📦 Extracts clothing metadata (e.g., type, category, gender, season)
- 🎨 Maps skin tones to suitable color palettes
- 🧍 Links body types to recommended clothing styles
- 🔗 Defines matching rules for upperwear and bottomwear combinations
- 🧹 Cleans and normalizes raw data for consistency
- 🧠 Prepares structured datasets for use in ML/LLM pipelines

---

## 🛠️ Tech Stack

- **Python 3**
- **Pandas / NumPy** – Data processing
- **BeautifulSoup / requests** – Web scraping (optional)
- **OpenAI / LangChain** – (Optional) LLM-based data enrichment
- **JSON / CSV** – Structured data storage
- **firebase** –  storage


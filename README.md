# 📰 Synthetic Financial News Generator

This repository contains a full pipeline for generating **synthetic financial news** to address class imbalance across different news types — a crucial step for training robust machine learning models in finance and investment domains.

---

## 📌 Project Overview

The pipeline is designed in 3 stages:
1. **Generation of Base News**  
   - For each news type, generate:
     - 10 **positive** and 10 **negative** samples (when sentiment is known)
     - 20 **neutral** samples (for sentiment-free types)
2. **Weight Assignment**  
   - Each news type is assigned an expert-defined weight to reflect its importance for model training.
3. **Length Variation Augmentation**  
   - Each generated news item is expanded into **3 additional versions** of varying length: short, medium, and long.

**Result:** 80 variations per news type, promoting both balance and diversity in the dataset.

---

## 📁 Project Structure
<pre>
. 
├── configs/ 
│ └── config.yml                        # Configuration file for generation settings 
├── data/ 
│ ├── few_shot_2_each.xlsx              # Few-shot examples (2 per type) 
│ ├── generated_news.xlsx               # Output from GigaChat generation after adding 3 more news for each generated news
│ └── synthetic_news.xlsx               # Full synthetic dataset after generating fisrt 20 news of each type
│ ├── prompt_templates/ 
├── prompt.txt                          # Primary prompt template 
│ ├── system_prompt.txt                 # System prompt for context 
│ ├── system_prompt_news.txt            # Alternative system prompt for news context 
│ └── types_of_news.txt                 # List of all news types 
├── Giga_generate_add_news.ipynb        # Notebook to generate variations (short/medium/long) 
├── Gigachat_defs.py                    # Core GigaChat interaction logic (stub + output handler) 
├── Synthetic_financial_news.ipynb      # Main notebook for base news generation 
└── README.md 
</pre>
---

## 🚀 Features

- **Balanced synthetic dataset** across 20+ financial news categories  
- **Sentiment-aware generation**: positive/negative/neutral tagging  
- **Prompt engineering** with fallback strategies for LLM inconsistencies  
- **Length diversity augmentation** for model robustness  
- **Few-shot samples** for LLM guidance  

---

## 💡 Example News Types

- Dividend Announcement  
- Share Buyback  
- Credit Rating Changes  
- M&A Activity  
- Regulatory Updates  
- Currency & Commodity Fluctuations  
- Political or Macro Events  
- Product Launches  
*(Full list in `prompt_templates/types_of_news.txt`)*

---

## 📈 Use Cases

- Training financial NLP models (e.g., sentiment analysis, news impact)
- Data augmentation for low-frequency event types
- Pretraining or fine-tuning language models in the financial domain

---

## 📝 Author

**Artur Garipov**  
[LinkedIn](https://www.linkedin.com/in/artur-garipov-36037a319) | [GitHub](https://github.com/Artur-Gar)

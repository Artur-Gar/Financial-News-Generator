# Synthetic News Generation

Task Description:
"""
We need to generate synthetic news based on real ones to eliminate the imbalance across news types, which would hinder future training of ML models.
"""

The task consists of the following stages:
1) Generate 20 instances for each news type and ddd weights for each news type
2) Duplicate each generated news item

For Stage 1) – Script: Gigachat_defs
Notebook: Synthetic_financial_news.ipynb
  - prompt_templates contains all necessary templates and the list of news types.
  - Gigachat_defs contains a stub for GigaChat (gigachat_stub), which needs to be run because GigaChat often doesn't respond on the first attempt.
  - llm_output in Gigachat_defs is used to retrieve responses.
  - Generate 10 positive and 10 negative news items for those types where sentiment (impact sign on stock price) can be determined.
  - Generate 20 neutral (sign-free) news items for the rest.
  - Add a weight to each news item (values are set based on expert judgment).

For Stage 2):
Notebook: Giga_generate_add_news.ipynb
  - For each generated news item, generate 3 additional versions with different lengths.

Thus, we have 20*4 = 80 news of different length generated for each news type
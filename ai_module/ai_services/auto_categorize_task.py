# Using Hugging Face Transformers
from transformers import pipeline

'''
Smart Task Categorization & Tagging
What it does: Automatically categorize tasks and suggest relevant tags based on task titles and descriptions.
Free AI Options:

    Hugging Face Transformers (zero-shot classification)
    OpenAI API (free tier: $5 credit)
    Google's Universal Sentence Encoder (via TensorFlow Hub)
'''

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def auto_categorize_task(title, description):
    text = f"{title}. {description}"
    categories = ["Work", "Personal", "Learning", "Health", "Shopping", "Finance"]
    result = classifier(text, categories)
    print(f"Onion_auto_categorize_task: {result}")

    return result['labels'][0]  # Top predicted category
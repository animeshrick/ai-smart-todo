from datetime import datetime, timedelta

'''
Intelligent Task Prioritization
What it does: Automatically assign priority levels based on keywords, due dates, and context.
Free AI Options:

    Rule-based AI with keyword matching
    scikit-learn for classification models
    Hugging Face sentiment analysis
'''

def smart_priority_assignment(title, description, due_date):
    urgent_keywords = ["urgent", "asap", "critical", "important", "deadline"]
    medium_keywords = ["soon", "weekly", "monthly", "review"]

    text = f"{title} {description}".lower()

    # Check for urgent keywords
    if any(keyword in text for keyword in urgent_keywords):
        return "high"

    # Check due date proximity
    if due_date and due_date <= datetime.now() + timedelta(days=2):
        return "high"
    elif due_date and due_date <= datetime.now() + timedelta(days=7):
        return "medium"

    return "low"
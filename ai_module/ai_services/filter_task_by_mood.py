"""
Mood-Based Task Recommendations
What it does: Suggest tasks based on current mood/energy level
"""

def recommend_tasks_by_mood(mood, available_tasks):
    mood_task_mapping = {
        'energetic': ['high', 'Work', 'Learning'],
        'tired': ['low', 'Personal', 'Planning'],
        'focused': ['high', 'Work', 'Learning'],
        'scattered': ['low', 'Personal', 'Health']
    }

    preferred_priority, preferred_categories = mood_task_mapping.get(mood, ['medium', []])

    recommended = [
        task for task in available_tasks
        if task.priority == preferred_priority or task.category in preferred_categories
    ]

    return recommended[:5]
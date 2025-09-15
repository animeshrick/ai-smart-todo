import openai

'''
Smart Task Suggestions & Reminders
What it does: Suggest task breakdowns and optimal scheduling.
Free AI Options:

    OpenAI API (free tier)
    Cohere API (free tier)
    Local LLM (Ollama with Llama 3.2)
'''

def generate_task_suggestions(task_title, task_description):
    prompt = f"""
    Break down this task into smaller, actionable subtasks:
    Title: {task_title}
    Description: {task_description}

    Provide 3-5 specific, measurable subtasks:
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    print(f"Onion_generate_task_suggestions: {response}")

    return response.choices[0].text.strip()
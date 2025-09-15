# Smart TODO

A Django-based intelligent task management system with AI-powered features to enhance productivity and task organization.

## Features

### Core Functionality
- Create, view, edit, and archive tasks
- Task categorization and tagging
- Priority assignment
- Due date management

### AI-Powered Features

#### 1. Smart Task Categorization
- Automatically categorizes tasks based on content using Hugging Face Transformers
- Uses zero-shot classification with facebook/bart-large-mnli model
- Categories include: Work, Personal, Learning, Health, Shopping, Finance

#### 2. Intelligent Tag Assignment
- Extracts relevant tags from task title and description
- Uses NLP techniques with spaCy and NLTK
- Helps organize and group similar tasks

#### 3. Smart Priority Assignment
- Automatically assigns priority levels (high, medium, low)
- Uses rule-based AI with keyword matching
- Considers due dates and urgency indicators in text

#### 4. Semantic Task Search
- Enables searching through tasks using natural language
- Powered by Sentence Transformers (all-MiniLM-L6-v2)
- Returns most semantically similar tasks based on query

#### 5. Task Suggestions
- Generates subtask breakdowns for complex tasks
- Uses OpenAI API to suggest actionable steps
- Helps with task planning and execution

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Database**: SQLite
- **AI/ML**: 
  - Hugging Face Transformers
  - spaCy
  - NLTK
  - Sentence Transformers
  - OpenAI API

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Start the development server:
   ```
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/v1/task/add/`: Create a new task
- `POST /api/v1/task/view/`: View task details
- `POST /api/v1/task/edit/`: Update task
- `POST /api/v1/task/archive/`: Archive task
- `POST /api/v1/task/search/`: Search for tasks

## Future Enhancements

### 1. Summarization for Long Descriptions
- **Problem**: Users paste long notes in descriptions
- **Solution**: Auto-generate short titles with Hugging Face summarizers (bart-large-cnn or t5-small)
- **Example**: Description: "Prepare slides for Monday's meeting with HR about new leave policies." → Title suggestion: "Slides for HR meeting."

### 2. Similar Task Recommendations
- **Problem**: Repeated tasks (e.g., groceries)
- **Solution**: Use embeddings to find past similar tasks
- **Implementation**: sentence-transformers/all-MiniLM-L6-v2
- **Example**: "This looks like your usual Grocery List — want to re-use tags/due date?"

### 3. Smart Scheduling
- **Feature**: Suggest optimal times to work on tasks
- **Approach**: Use heuristics or ML based on user history
- **Example**: "You finish writing tasks faster in the evening — schedule this essay after 8 PM?"
- **Implementation**: Start with simple rules + user history, can later train a recommender system

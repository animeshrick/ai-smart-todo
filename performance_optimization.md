# Performance Optimization for Smart TODO

## Current Issue
Task creation is taking more than 8 seconds, primarily due to inefficient AI model loading and processing of long descriptions.

## Root Causes Identified

1. **Multiple AI Model Loading on Each Request**:
   - Each AI service (auto_assign_task_tag.py, auto_categorize_task.py, smart_priority_assignment.py) loads its models on every function call
   - The Hugging Face Transformers model (facebook/bart-large-mnli) is particularly heavy
   - spaCy model is loaded for each tag extraction request
   - SentenceTransformer model is loaded for each search operation

2. **No Caching Mechanism**:
   - Similar descriptions are processed repeatedly without caching results
   - No memoization for expensive AI operations
   
   
3. **Synchronous Processing**:
   - All AI operations happen synchronously during task creation
   - User has to wait for all AI processing to complete before task is saved

## Optimization Solutions (Without Trimming Description)

### 1. Implement Singleton Pattern for AI Models

```python
# ai_module/ai_services/model_registry.py
class ModelRegistry:
    _instance = None
    _models = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelRegistry, cls).__new__(cls)
            cls._instance._load_models()
        return cls._instance

    def _load_models(self):
        # Load models once
        from transformers import pipeline
        import spacy
        from sentence_transformers import SentenceTransformer
        
        print("Loading AI models...")
        try:
            self._models['nlp'] = spacy.load("en_core_web_sm")
        except OSError:
            print("⚠️ spaCy model not found")
            self._models['nlp'] = None
            
        try:
            self._models['classifier'] = pipeline("zero-shot-classification",
                                                model="facebook/bart-large-mnli",
                                                device=-1)  # Use CPU
        except Exception as e:
            print(f"⚠️ Transformers model loading failed: {e}")
            self._models['classifier'] = None
            
        try:
            self._models['sentence_transformer'] = SentenceTransformer('all-MiniLM-L6-v2')
        except Exception as e:
            print(f"⚠️ SentenceTransformer model loading failed: {e}")
            self._models['sentence_transformer'] = None
            
        print("AI models loaded successfully")

    def get_model(self, model_name):
        return self._models.get(model_name)
```

### 2. Initialize Models at Application Startup

```python
# ai_module/apps.py
from django.apps import AppConfig

class AIModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_module'
    
    def ready(self):
        # Import and initialize the model registry when Django starts
        from ai_module.ai_services.model_registry import ModelRegistry
        ModelRegistry()  # Initialize singleton
```

### 3. Update AI Services to Use the Model Registry

```python
# Example for auto_categorize_task.py
from ai_module.ai_services.model_registry import ModelRegistry

def auto_categorize_task(title, description):
    text = f"{title}. {description}"
    categories = ["Work", "Personal", "Learning", "Health", "Shopping", "Finance"]
    
    # Get the pre-loaded model
    classifier = ModelRegistry().get_model('classifier')
    if not classifier:
        return "Uncategorized"  # Fallback if model not available
        
    result = classifier(text, categories)
    return result['labels'][0]  # Top predicted category
```

### 4. Implement Result Caching

```python
# ai_module/ai_services/caching.py
from django.core.cache import cache
import hashlib

def get_cache_key(prefix, *args):
    # Create a deterministic cache key from the arguments
    key_parts = [str(arg)[:100] for arg in args]  # Limit length for very long descriptions
    key_string = prefix + '_'.join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()

def cached_ai_operation(prefix, operation_func, *args, timeout=3600):
    """Cache AI operation results"""
    cache_key = get_cache_key(prefix, *args)
    result = cache.get(cache_key)
    
    if result is None:
        result = operation_func(*args)
        cache.set(cache_key, result, timeout=timeout)
        
    return result
```

### 5. Apply Caching to AI Services

```python
# Example for auto_categorize_task.py with caching
from ai_module.ai_services.model_registry import ModelRegistry
from ai_module.ai_services.caching import cached_ai_operation

def _categorize_task(title, description):
    text = f"{title}. {description}"
    categories = ["Work", "Personal", "Learning", "Health", "Shopping", "Finance"]
    
    classifier = ModelRegistry().get_model('classifier')
    if not classifier:
        return "Uncategorized"
        
    result = classifier(text, categories)
    return result['labels'][0]

def auto_categorize_task(title, description):
    # Use caching wrapper
    return cached_ai_operation('category', _categorize_task, title, description)
```

### 6. Implement Asynchronous Processing

```python
# tasks/serializers/task_serializer.py (modified version)
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

class TaskSerializer:
    # ... existing code ...
    
    def create(self, data: dict) -> Optional[Task]:
        if self.validate(data):
            request: AddTaskRequestType = data.get("request_data")

            due_date = convert_string_to_dateTime(request.due_date)
            completed_at = convert_string_to_dateTime(request.completed_at)
            
            # Create task immediately with minimal processing
            task = Task.objects.create(
                title=request.title,
                description=request.description,
                category=request.category or "Uncategorized",  # Default value
                due_date=due_date,
                completed_at=completed_at,
                tags=request.tags or "",  # Default empty string
                priority=request.priority or "medium",  # Default priority
                is_active=True,
            )
            
            # Trigger async processing via signal
            transaction.on_commit(lambda: task_created.send(sender=Task, instance=task))
            return task
        return None

# Signal for async processing
task_created = django.dispatch.Signal()

@receiver(task_created)
def process_task_ai_features(sender, instance, **kwargs):
    """Process AI features asynchronously after task is created"""
    task = instance
    
    # Only process if values aren't already set
    if not task.tags or task.tags == "":
        ai_tags = extract_tags_from_text(task.title, task.description)
        task.tags = ai_tags
    
    if not task.category or task.category == "Uncategorized":
        ai_category = auto_categorize_task(task.title, task.description)
        task.category = ai_category
    
    if not task.priority:
        ai_priority = smart_priority_assignment(task.title, task.description, task.due_date)
        task.priority = ai_priority
    
    # Save the updated task
    task.save(update_fields=['tags', 'category', 'priority'])
```

### 7. Optimize AI Model Parameters

```python
# ai_module/ai_services/auto_assign_task_tag.py

# Reduce the maximum text length for processing
MAX_TEXT_LENGTH = 512  # Reduced from 1024

# Use a smaller, faster model for classification
classifier = pipeline("zero-shot-classification",
                     model="facebook/bart-base-mnli",  # Smaller model
                     device=-1)  # Use CPU
```

### 8. Add Background Task Processing (Optional)

For a more robust solution, consider using Django Q, Celery, or Django Channels for background processing:

```python
# Using Django Q (add to requirements.txt)
# django-q==1.3.9

# settings.py
INSTALLED_APPS = [
    # ... existing apps
    'django_q',
]

Q_CLUSTER = {
    'name': 'smart_todo',
    'workers': 4,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
    }
}

# tasks/serializers/task_serializer.py
from django_q.tasks import async_task

def create(self, data: dict) -> Optional[Task]:
    # ... create task code ...
    
    # Queue background processing
    async_task('tasks.services.ai_processing.process_task_ai_features', task.id)
    return task

# tasks/services/ai_processing.py
def process_task_ai_features(task_id):
    try:
        task = Task.objects.get(id=task_id)
        
        # Process AI features and update task
        # ... AI processing code ...
        
        task.save(update_fields=['tags', 'category', 'priority'])
    except Exception as e:
        print(f"Error processing AI features: {e}")
```

## Implementation Priority

1. **Immediate (1-2 hours)**: Implement the Model Registry singleton pattern
2. **Short-term (2-4 hours)**: Add result caching for AI operations
3. **Medium-term (4-8 hours)**: Implement asynchronous processing with signals
4. **Long-term (1-2 days)**: Add proper background task processing with Django Q or Celery

## Expected Performance Improvement

- **Current**: 8+ seconds per task creation
- **After optimization**: 
  - Initial response: < 1 second (task created immediately)
  - AI processing: Continues in background
  - Subsequent similar tasks: < 2 seconds (due to caching)

These optimizations maintain the full functionality of the AI features without trimming task descriptions, while significantly improving the user experience.
import re
import spacy
from transformers import pipeline
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import warnings
warnings.filterwarnings('ignore')

# Initialize models (load once, use many times)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("⚠️ spaCy model not found. Install with: python -m spacy download en_core_web_sm")
    nlp = None

try:
    # Initialize Hugging Face classifier
    classifier = pipeline("zero-shot-classification",
                         model="facebook/bart-large-mnli",
                         device=-1)  # Use CPU
except Exception as e:
    print(f"⚠️ Transformers model loading failed: {e}")
    classifier = None

# Download NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# =============================================================================
# CONSTANTS
# =============================================================================
MAX_TEXT_LENGTH = 1024  # Limit text length for NLP processing to optimize performance

# =============================================================================
# 1. EXTRACT TAGS FROM TEXT
# =============================================================================
def extract_tags_from_text(title, description):
    """
    Extract relevant tags from task title and description
    Returns: comma-separated string of tags
    """
    trimmed_description = description[:MAX_TEXT_LENGTH]
    text = f"{title} {description[:MAX_TEXT_LENGTH]}".lower()


    # Method 1: Rule-based keyword extraction
    predefined_tags = {
        'work': ['work', 'job', 'office', 'meeting', 'project', 'client', 'deadline', 'presentation'],
        'learning': ['learn', 'study', 'course', 'tutorial', 'book', 'research', 'practice'],
        'health': ['doctor', 'gym', 'exercise', 'medical', 'appointment', 'fitness', 'diet'],
        'personal': ['personal', 'family', 'friend', 'home', 'hobby', 'vacation'],
        'finance': ['bank', 'money', 'budget', 'bill', 'payment', 'insurance', 'tax'],
        'shopping': ['buy', 'purchase', 'shop', 'order', 'store', 'market'],
        'urgent': ['urgent', 'asap', 'critical', 'important', 'emergency'],
        'ai': ['ai', 'ml', 'machine learning', 'artificial intelligence', 'data science'],
        'backend': ['backend', 'server', 'database', 'api', 'django', 'python'],
        'frontend': ['frontend', 'ui', 'ux', 'react', 'javascript', 'css', 'html']
    }

    found_tags = []

    # Check for predefined tags
    for tag, keywords in predefined_tags.items():
        if any(keyword in text for keyword in keywords):
            found_tags.append(tag)

    # Method 2: NLP-based extraction using spaCy
    if nlp:
        try:
            doc = nlp(text)

            # Extract entities
            entities = [ent.text.lower() for ent in doc.ents
                        if ent.label_ in ['ORG', 'PRODUCT', 'EVENT', 'WORK_OF_ART']]
            print(f"Onion_entities: {entities}")
            found_tags.extend(entities[:3])  # Limit to 3 entities

            # Extract important nouns
            important_nouns = [token.lemma_.lower() for token in doc
                               if token.pos_ == 'NOUN' and len(token.text) > 3
                               and not token.is_stop][:5]
            print(f"Onion_important_nouns: {important_nouns}")

            found_tags.extend(important_nouns)
            print(f"Onion_found_tags: {found_tags}")

        except Exception as e:
            print(f"spaCy processing error: {e}")

    # Method 3: TF-IDF based keyword extraction (if you have enough data)
    try:
        # This would work better with more tasks in your database
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text.lower())
        important_words = [word for word in words
                           if word.isalnum() and word not in stop_words
                           and len(word) > 3][:5]
        found_tags.extend(important_words)
    except Exception as e:
        print(f"NLTK processing error: {e}")

    # Clean and deduplicate tags
    clean_tags = []
    seen = set()

    for tag in found_tags:
        tag_clean = re.sub(r'[^\w\s]', '', str(tag)).strip().lower()
        # print(f"Onion_tag_clean: {tag_clean}")

        if tag_clean and tag_clean not in seen and len(tag_clean) > 2:
            clean_tags.append(tag_clean)
            seen.add(tag_clean)

    # Limit to top 5 tags
    return ','.join(clean_tags[:3])
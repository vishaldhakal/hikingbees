import os
import django
import re
from html import unescape

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hikingbees.settings')
django.setup()


def clean_html_tags(html_text):
    """
    Remove HTML tags from text and convert HTML entities to plain text
    Uses only built-in Python libraries
    """
    if not html_text:
        return html_text

    # Remove HTML comments
    html_text = re.sub(r'<!--.*?-->', '', html_text, flags=re.DOTALL)

    # Remove script and style elements completely (including their content)
    html_text = re.sub(r'<script[^>]*>.*?</script>',
                       '', html_text, flags=re.DOTALL | re.IGNORECASE)
    html_text = re.sub(r'<style[^>]*>.*?</style>',
                       '', html_text, flags=re.DOTALL | re.IGNORECASE)

    # Remove all HTML tags
    html_text = re.sub(r'<[^>]+>', '', html_text)

    # Unescape HTML entities (like &amp; &lt; &gt; &nbsp; etc.)
    html_text = unescape(html_text)

    # Replace common HTML entities that unescape might miss
    html_text = html_text.replace('&nbsp;', ' ')
    html_text = html_text.replace('&rsquo;', "'")
    html_text = html_text.replace('&lsquo;', "'")
    html_text = html_text.replace('&rdquo;', '"')
    html_text = html_text.replace('&ldquo;', '"')
    html_text = html_text.replace('&mdash;', '—')
    html_text = html_text.replace('&ndash;', '–')

    # Clean up whitespace
    html_text = re.sub(r'\s+', ' ', html_text)
    html_text = html_text.strip()

    return html_text


def has_html_tags(text):
    """
    Check if text contains HTML tags
    """
    if not text:
        return False
    return bool(re.search(r'<[^>]+>', text))


def remove_html_from_questions():
    """
    Remove HTML tags from ActivityFAQ 'question' fields ONLY
    The 'answer' field will NOT be modified at all
    """
    try:
        # Import model AFTER Django setup to avoid TinyMCE configuration issues
        from activity.models import ActivityFAQ

        faqs = ActivityFAQ.objects.all()

        for faq in faqs:
            # ONLY processing the 'question' field
            if faq.question and has_html_tags(faq.question):
                original_question = faq.question
                cleaned_question = clean_html_tags(faq.question)

                if cleaned_question != original_question:
                    # IMPORTANT: Only updating the 'question' field
                    faq.question = cleaned_question
                    # Only saves the question field
                    faq.save(update_fields=['question'])
        print("HTML tags removed from all ActivityFAQ 'question' fields.")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    remove_html_from_questions()

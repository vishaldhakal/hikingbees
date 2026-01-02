import os

import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hikingbees.settings")
django.setup()

from activity.models import ActivityFAQ, FAQCategory


def fix_faqs():
    print("Starting FAQ cleanup...")

    # 1. Create the 'General' category if it doesn't exist
    category, created = FAQCategory.objects.get_or_create(
        slug="general", defaults={"name": "General", "order": 0, "active": True}
    )

    if created:
        print(f"Created new category: {category.name}")
    else:
        print(f"Using existing category: {category.name}")

    # 2. Update all existing FAQs to use this category
    faqs_to_update = ActivityFAQ.objects.filter(category__isnull=True)
    count = faqs_to_update.count()

    if count > 0:
        faqs_to_update.update(category=category)
        print(f"Successfully updated {count} FAQs to 'General' category.")
    else:
        print("No FAQs found without a category.")

    print("Done!")


if __name__ == "__main__":
    fix_faqs()

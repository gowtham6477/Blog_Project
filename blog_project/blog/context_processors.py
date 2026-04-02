from datetime import datetime


def site_context(request):
    return {
        "site_name": "DevJournal",
        "current_year": datetime.utcnow().year,
    }

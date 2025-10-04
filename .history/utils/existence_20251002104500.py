import wikipedia

def verify_existence(query):
    try:
        summary = wikipedia.summary(query, sentences=1, auto_suggest=True)
        return {"exists": True, "reference": summary}
    except:
        return {"exists": False, "reference": None}

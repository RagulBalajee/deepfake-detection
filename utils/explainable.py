def explain_result(content_type, score):
    if score > 0.8:
        return f"{content_type.capitalize()} highly suspicious of being fake/deepfake."
    elif score > 0.5:
        return f"{content_type.capitalize()} shows moderate signs of manipulation."
    else:
        return f"{content_type.capitalize()} likely authentic."

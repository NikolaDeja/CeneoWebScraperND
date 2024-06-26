from deep_translator import GoogleTranslator
def extract(ancestor, selector=None, attribute=None, return_list=False):
    if return_list:
        if attribute:
            return [tag[attribute] for tag in ancestor.select(selector)]
        return [tag.get_text().strip() for tag in ancestor.select(selector)]
    if selector:
        if attribute:
            try:
                return ancestor.select_one(selector)[attribute]
            except TypeError:
                return None
        try:
            return ancestor.select_one(selector).get_text().strip()
        except AttributeError:
            return None
    if attribute:
        return ancestor[attribute]
    return ancestor.get_text().strip()

def rate(score):
    rate = score.split("/")
    return float(rate[0].replace(",","."))/float(rate[1])

def recommend(recommendation):
    return True if recommendation =="Polecam" else False  if recommendation == "Nie polecam" else None

def translate(text, from_lang = "pl", to_lang = "en"):
    if text:
        if isinstance(text, list):
            return [GoogleTranslator(source=from_lang, target=to_lang).translate(t) for t in text]
        return GoogleTranslator(source=from_lang, target=to_lang).translate(text)
        
    return None

selectors = {
    "opinion_id": [None,"data-entry-id"],
    "author" : ["span.user-post__author-name"],
    "recommendation" : ["span.user-post__author-recomendation > em"],
    "score" : ["span.user-post__score-count"],
    "content_pl" : ["div.user-post__text"],
    "content_en" : ["div.user-post__text"],
    "pros_pl" : ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    "pros_en" : ["div.review-feature__title--positives ~ div.review-feature__item", None, True],
    "cons_pl" : ["div.review-feature__title--negatives ~ div.review-feature__item", None, True],
    "cons_en" : ["div.review-feature__title--negatives ~ div.review-feature__item", None, True],
    "helpful" : ["button.vote-yes > span"],
    "unhelpful" : ["button.vote-no > span"],
    "publish_date" : ["span.user-post__published > time:nth-child(1)","datetime"],
    "purchase_date" : ["span.user-post__published > time:nth-child(2)","datetime"],
}

transformations = {
    "recommendation" : recommend,
    "score" : rate,
    "helpful" : int,
    "unhelpful" : int,
    "content_en" : translate,
    "pros_en" : translate,
    "cons_en" : translate,
}
import spacy_streamlit

models = ["training/model-best", "training/model-last"]
default_text = "Ab BBCH 30/31  sollte bei Septoriabefall in Weizen eine wirksame Behandlung durchgeführt werden."

spacy_streamlit.visualize(models,default_text)
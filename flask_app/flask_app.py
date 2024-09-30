# https://realpython.com/python-web-applications/#build-a-basic-python-web-application
from flask import Flask, render_template, request
import pickle
import numpy as np
from plot_results import *
from wiki_scrape import *
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    with open('dict_for_flask_app.pkl', 'rb') as f:
        results = pickle.load(f)
    
 
    words = [key for key in results.keys()]
    
    word_chosen = request.args.get('word_box', '')    
    
    if word_chosen:
        try:
            plot_word_count = word_count_plot(results,word_chosen)
            year_most_used ='In <mark>' + str(results[word_chosen]['year_most_count']) + '</mark> wordt <mark>' + word_chosen + '</mark> het vaakst genoemd op de voorpagina.'
            wiki_str = get_wiki_str(str(results[word_chosen]['year_most_count']),word_chosen)
            plot_word_use =  plot_most_important_words(results,word_chosen)
            plot_ml_result = get_ml_results_plot(results,word_chosen)
        except:
            plot_word_count = ''
            year_most_used = ''
            wiki_str = ''
            plot_word_use = ''
            plot_ml_result = ''
    else:
        plot_word_count = ''
        year_most_used = ''
        wiki_str = ''
        plot_word_use = ''
        plot_ml_result = ''

        
    return render_template('index.html',words = words,plot_word_count=plot_word_count,plot_word_use = plot_word_use, year_sent=year_most_used,wiki_str=wiki_str,plot_ml_result=plot_ml_result) 
    
if __name__ == "__main__":
    app.run()


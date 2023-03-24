import pandas as pd

data = pd.read_csv('data.csv')

random_50 = data.sample(50)

with open('templates/demo2.html', 'w') as html:
    html.write('<!DOCTYPE html><html><head></head><body><h1>Phish Catcher\'s Link Emporium</h1><br />')
    for _, row in random_50.iterrows():
        html.write(f'<a href="{row["url"]}">A {"phishing" if row["label"] == "bad" else "normal"} site!</a><br />')
    html.write('</body></html>')
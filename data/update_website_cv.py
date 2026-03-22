import csv
from string import Template
import os
import shutil
from datetime import date

pubs = []

with open('j-publications.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        pub = {}
        for key, value in row.items():
            if key == "Authors":
                # Split authors by ';', strip each author
                pub[key] = [author.strip() for author in value.split(';')]
            else:
                pub[key] = value.strip()
        pubs.append(pub)

c_pubs_str = ""
w_pubs_str = ""
w_top_pubs_str = ""
i = 0

for pub in pubs:
    c_authors = []
    w_authors = []
    for author in pub["Authors"]:
        if(author == "A. J. Edwards"):
            c_authors.append("\\textbf{A. J. Edwards}")
            w_authors.append("<b>A. J. Edwards</b>")
        else:
            c_authors.append(author)
            w_authors.append(author)
    c_authors_str = ", ".join(c_authors)
    w_authors_str = ", ".join(w_authors)

    #print(authors_str)
    if(pub["No"] == ''):
        no_str = ''
    else:
        no_str  = f':{pub["No"]}'

    if(pub["pp"] == ''):
        pp_str = ''
    else:
        pp_str = f', {pub['pp']}'

    if(pub["URL"] == ''):
        c_url_str = f'{pub["Title"]}'
        w_url_str = f'{pub["Title"]}'
    else:
        c_url_str = f'\\href{{{pub["URL"]}}}{{{pub["Title"]}}}'
        w_url_str = f'<a href="{pub["URL"]}">{pub["Title"]}</a>'

    c_pub_str = f"\\item {c_authors_str}, {c_url_str}, \\textit{{{pub["Journal"]}}} \\textbf{{{pub["Vol"]}}}{no_str}{pp_str} ({pub["Year"]})."
    w_pub_str = f"            <li>{w_authors_str}, {w_url_str}, <i>{pub["Journal"]}</i> <b>{pub["Vol"]}</b>{no_str}{pp_str} ({pub["Year"]}).</li>"
    print(c_pub_str)
    c_pubs_str += f"{c_pub_str}\n"
    w_pubs_str += f"{w_pub_str}\n"
    if i < 3:
        w_top_pubs_str += f"{w_pub_str}\n"
    i += 1

sub_dict = {}
sub_dict["J_PUBS"] = c_pubs_str
sub_dict["W_PUBS"] = w_pubs_str
sub_dict["W_TOP_PUBS"] = w_top_pubs_str
today = date.today()
date_str = today.strftime("%b%Y")
sub_dict["CV_NAME"] = f"EdwardsCV-{date_str}.pdf"
sub_dict["MO"] = today.strftime("%b")
sub_dict["YEAR"] = today.strftime("%Y")

with open('cv.tpt.tex', 'r', encoding='utf-8') as template_file:
    template = Template(template_file.read())

cv_content = template.substitute(sub_dict)

with open('../cv_tex/cv.tex', 'w', encoding='utf-8') as output_file:
    output_file.write(cv_content)


with open('index.tpt.html', 'r', encoding='utf-8') as template_file:
    template = Template(template_file.read())

w_content = template.substitute(sub_dict)

with open('../dist/index.html', 'w', encoding='utf-8') as output_file:
    output_file.write(w_content)

script_dir = os.getcwd()
os.chdir('../cv_tex')

os.system("pdflatex cv.tex")

shutil.copy("cv.pdf", f"../dist/{sub_dict["CV_NAME"]}")

os.chdir(script_dir)


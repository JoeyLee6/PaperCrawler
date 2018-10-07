import pandas as pd
import os

base_path = ''

os.chdir(base_path)

documents = [
    'error_correct',
    'qbkx',
    'qbllysj',
    'qbxb',
    'qbzlgz',
    'qbzz',
    'tsqbgz',
    'tsqbzs',
    'tsyqb',
    'xdqb',
    'xdtsqbjs'
]

print('\nStart Generating CSV File\n')

link_set = set()

id_list = list()
journal_list = list()
year_list = list()
issue_list = list()
authors_list = list()
title_list = list()
abstract_list = list()
keywords_list = list()
link_list = list()

count = 0
for document in documents:
    document_path = base_path + '/' + document
    for filename in os.listdir(document_path):
        if 'error' in filename:
            continue
        file_path = os.path.join(document_path, filename)
        with open(file_path, encoding='utf-8') as f:
            lines = f.readlines()
            if lines[7].split('|')[1].strip('\n') in link_set or '@@' in lines[6]:
                for line in lines:
                    print(line)
                f.close()
                continue
            else:
                journal_list.append(lines[0].split('|')[1].strip('\n'))
                year_list.append(lines[1].split('|')[1].strip('\n'))
                issue_list.append(lines[2].split('|')[1].strip('\n'))
                authors_list.append(lines[3].split('|')[1].strip('\n'))
                title_list.append(lines[4].split('|')[1].strip('\n'))
                abstract_list.append(lines[5].split('|')[1].strip('\n'))
                keywords_list.append(lines[6].split('|')[1].strip('\n'))
                link_list.append(lines[7].split('|')[1].strip('\n'))
                link_set.add(lines[7].split('|')[1].strip('\n'))
                count += 1
                id_list.append(count)
                if count % 1000 == 0:
                    print('processed %d articles!' % count)
                f.close()
print('Finished preprocessing! %d articles in all!' % count)

df = pd.DataFrame({'article_id': id_list,
                   'journal': journal_list,
                   'year': year_list,
                   'issue': issue_list,
                   'authors': authors_list,
                   'title': title_list,
                   'abstract': abstract_list,
                   'keywords': keywords_list,
                   'link': link_list})

df.to_csv("articles_1_2.csv", index=False, sep=',', encoding='utf-8')

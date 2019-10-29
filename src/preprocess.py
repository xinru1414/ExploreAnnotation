import csv
import json
import click
from collections import Counter

sent_sentences = ['We make mistakes', 'You get a sense', 'he worked his way up', 'he offers advice']
agency_sentences = ['I got a call', 'I should have given credit', 'We will add his dishes', 'he offers advice']
country = {'USA'}
country2 = {'RUS'}


def read_report(file: str):
    data = []
    with open(file, 'r') as fi:
        for item in fi:
            data.append(json.loads(item))
    return data[8:]


def no_quiz(data):
    new_data = []
    for item in data:
        if item['state'] == 'finalized':
            new_data.append(item)
    return new_data


# def filter(data):
#     new_data = []
#     for item in data:
#         if len(item['results']['judgments']) == 3:
#             new_data.append(item)
#     return new_data


def get_countries_for_instance(d):
    return list(map(lambda judgment: judgment['country'], d['results']['judgments']))


def filter_by_country(items, countries):
    return list(filter(lambda d: Counter(map(lambda country: country in countries, get_countries_for_instance(d))).get(True, 0) > 0, items))


def explore_workers(d, task):
    workers = {}
    for item in d:
        for i in range(len(item['results']['judgments'])):
            if task == 'agency':
                current_worker_answer = item['results']['judgments'][i]['data'][
                    'overall_how_much_agency_does_the_subject_subj_seem_to_have']
                if i == 0:
                    worker_1_answer = item['results']['judgments'][1]['data'][
                        'overall_how_much_agency_does_the_subject_subj_seem_to_have']
                    worker_2_answer = item['results']['judgments'][2]['data'][
                        'overall_how_much_agency_does_the_subject_subj_seem_to_have']
                elif i == 1:
                    worker_1_answer = item['results']['judgments'][0]['data'][
                        'overall_how_much_agency_does_the_subject_subj_seem_to_have']
                    worker_2_answer = item['results']['judgments'][2]['data'][
                        'overall_how_much_agency_does_the_subject_subj_seem_to_have']
                else:
                    worker_1_answer = item['results']['judgments'][0]['data'][
                        'overall_how_much_agency_does_the_subject_subj_seem_to_have']
                    worker_2_answer = item['results']['judgments'][1]['data'][
                        'overall_how_much_agency_does_the_subject_subj_seem_to_have']
            elif task == 'power':
                current_worker_answer = item['results']['judgments'][i]['data'][
                    'the_sentence_full_sentence']
                if i == 0:
                    worker_1_answer = item['results']['judgments'][1]['data'][
                        'the_sentence_full_sentence']
                    worker_2_answer = item['results']['judgments'][2]['data'][
                        'the_sentence_full_sentence']
                elif i == 1:
                    worker_1_answer = item['results']['judgments'][0]['data'][
                        'the_sentence_full_sentence']
                    worker_2_answer = item['results']['judgments'][2]['data'][
                        'the_sentence_full_sentence']
                else:
                    worker_1_answer = item['results']['judgments'][0]['data'][
                        'the_sentence_full_sentence']
                    worker_2_answer = item['results']['judgments'][1]['data'][
                        'the_sentence_full_sentence']
            else:
                current_worker_answer = [item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_subj'],
                                         item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_obj']]
                if i == 0:
                    worker_1_answer = [item['results']['judgments'][1]['data']['how_the_writer_feels_about_the_subj'],
                                       item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_obj']]
                    worker_2_answer = [item['results']['judgments'][2]['data']['how_the_writer_feels_about_the_subj'],
                                       item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_obj']]
                elif i == 1:
                    worker_1_answer = [item['results']['judgments'][0]['data']['how_the_writer_feels_about_the_subj'],
                                       item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_obj']]
                    worker_2_answer = [item['results']['judgments'][2]['data']['how_the_writer_feels_about_the_subj'],
                                       item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_obj']]
                else:
                    worker_1_answer = [item['results']['judgments'][0]['data']['how_the_writer_feels_about_the_subj'],
                                       item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_obj']]
                    worker_2_answer = [item['results']['judgments'][1]['data']['how_the_writer_feels_about_the_subj'],
                                       item['results']['judgments'][i]['data']['how_the_writer_feels_about_the_obj']]

            worker_id = item['results']['judgments'][i]['worker_id']
            if worker_id not in workers:
                workers[worker_id] = {'agree': 0, 'disagree': 0}
            if task == 'sentiment':
                for j in range(len(current_worker_answer)):
                    if current_worker_answer[j] == worker_1_answer[j] or current_worker_answer[j] == worker_2_answer[j]:
                        workers[worker_id]['agree'] += 1
                    else:
                        workers[worker_id]['disagree'] += 1
            else:
                if current_worker_answer == worker_1_answer or current_worker_answer == worker_2_answer:
                    workers[worker_id]['agree'] += 1
                else:
                    workers[worker_id]['disagree'] += 1

    workers_agreement = Counter()
    for key, values in workers.items():
        workers_agreement[key] = values['disagree'] / sum(values.values())
    return workers_agreement


def bad_coder(workers_agreement, task):
    b = set()
    if task == 'sentiment':
        threshold = 0.2
    elif task == 'agency':
        threshold = 0.5
    else:
        threshold = 0.4
    for key, value in workers_agreement.items():
        if value > threshold:
            b.add(key)
    return b


def delete_bad_coder(d, b):
    delete = []
    for item in d:
        if bool(set([item['results']['judgments'][i]['worker_id'] for i in
                     range(len(item['results']['judgments']))]).intersection(b)):
            delete.append(item)
    new_d = [item for item in d if item not in delete]
    assert (len(d) - len(delete) == len(new_d))
    return new_d


def annotator_results(data: list, n: int, task: str, lan: str):
    a = []
    for index, item in enumerate(data):
        # l = list(data[index]['results']['judgments'][n]['data'].values())[:6]
        if task == 'agency':
            if lan != 'zh':
                l = data[index]['results']['judgments'][n]['data']['overall_how_much_agency_does_the_subject_subj_seem_to_have']
            else:
                l = data[index]['results']['judgments'][n]['data']['4_']
        elif task == 'power':
            if lan == 'en':
                l = data[index]['results']['judgments'][n]['data']['the_sentence_full_sentence']
            elif lan == 'zh':
                l = data[index]['results']['judgments'][n]['data']['1full_sentence']
            elif lan == 'fr':
                l = data[index]['results']['judgments'][n]['data']['dans_la_phrase_full_sentence']
            else:
                l = data[index]['results']['judgments'][n]['data']['_full_sentence']
        else:
            l = list(data[index]['results']['judgments'][n]['data'].values())
        a.append(l)
    return a


def mapping(data: list, task: str, lan: str):
    #mapping = {'Abstract': 0, 'Orientation': 1, 'Action': 2, 'Resolution': 3, 'Evaluation': 4, 'Coda': 5}
    #m = list(map(lambda y: list(map(lambda x: mapping[x], y)), data))
    if task == 'agency':
        if lan != 'zh':
            mapping = {'Low Agency': 0, 'Moderate Agency': 1, "High Agency": 2}
        else:
            mapping = {'低代理性': 0, '适中的代理性': 1, '高代理性': 2}
        m = list(map(lambda x: mapping[x], data))
    elif task == 'power':
        if lan != 'zh':
            mapping = {'Subj has more authority and is more powerful': 0, 'Similar/Unclear': 1, "Obj has more authority and is more powerful": 2}
        else:
            mapping = {'主语具有更高的权威性和更大的权利': 0, '主语和宾语拥有同等的权利，具有相似的权威性': 1, '宾语具有更高的权威性和更大的权利': 2}
        m = list(map(lambda x: mapping[x], data))
    else:
        if lan != 'zh':
            mapping = {'Negative': 0, 'Either Negative or Neutral': 0, 'Neutral': 2,
               'Either Positive or Neutral': 4, 'Positive': 4}
        else:
            mapping = {'消极的': 0, '或消极或中立': 0, '中立的': 2,
                        '或积极或中立': 4, '积极的': 4}
        m = list(map(lambda y: list(map(lambda x: mapping[x], y)), data))

    return m


def w2csv(file: str, data: list, task: str):
    with open(file, 'w') as fo:
        csv_file = csv.writer(fo, delimiter='\t')
        #csv_file.writerow([n for n in range(1, len(data[0])+1)])
        if task == 'agency':
            csv_file.writerow(['Agency'])
            for l in data:
                csv_file.writerow(str(l))
        elif task == 'power':
            csv_file.writerow(['Power'])
            for l in data:
                csv_file.writerow(str(l))
        else:
            csv_file.writerow(['Subj', 'Obj'])
            for l in data:
                csv_file.writerow(l)


@click.command()
@click.option('-i', '--input_file', 'input_file', type=str)
@click.option('-oa', '--output_file_a', 'output_file_a', type=str)
@click.option('-ob', '--output_file_b', 'output_file_b', type=str)
@click.option('-oc', '--output_file_c', 'output_file_c', type=str)
@click.option('-l', '--language', 'language', type=str)
@click.option('-t', '--task', 'task', type=str)
def main(input_file, output_file_a, output_file_b, output_file_c, language, task):
    data = read_report(input_file)
    #data = filter(data)
    data = no_quiz(data)
    #data = filter_by_country(data, country)
    print(f'for {task} we have {len(data)} instances before deleting bad coders')
    workers = explore_workers(data, task)
    bad_coders = bad_coder(workers, task)
    data = delete_bad_coder(data, bad_coders)
    print(f'for {task} we have {len(data)} instances after deleting bad coders')
    a1 = annotator_results(data, 0, task, language)
    a2 = annotator_results(data, 1, task, language)
    a3 = annotator_results(data, 2, task, language)
    d1 = mapping(a1, task, language)
    d2 = mapping(a2, task, language)
    d3 = mapping(a3, task, language)

    w2csv(output_file_a, d1, task)
    w2csv(output_file_b, d2, task)
    w2csv(output_file_c, d3, task)


if __name__ == '__main__':
    main()
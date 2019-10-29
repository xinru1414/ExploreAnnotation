'''
Oct 2019
Xinru Yan

This script calculates the pair-wise inter-annotator agreement for three annotators.
'''
import pandas as pd
import numpy as np
from nltk import agreement
import click


def krippendorffs_alpha(d1, d2, d3, task):
    if task == 'power':
        r1 = d1['Power'].values.tolist()
        r2 = d2['Power'].values.tolist()
        r3 = d3['Power'].values.tolist()
        taskdata = [[0, str(i), str(r1[i])] for i in range(0, len(r1))] + [[1, str(i), str(r2[i])] for i in range(0, len(r2))] + [[2, str(i), str(r3[i])] for i in range(0, len(r3))]
        ratingtask = agreement.AnnotationTask(data=taskdata)
        return str(ratingtask.alpha())
    elif task == 'agency':
        r1 = d1['Agency'].values.tolist()
        r2 = d2['Agency'].values.tolist()
        r3 = d3['Agency'].values.tolist()
        taskdata = [[0, str(i), str(r1[i])] for i in range(0, len(r1))] + [[1, str(i), str(r2[i])] for i in range(0, len(r2))] + [[2, str(i), str(r3[i])] for i in range(0, len(r3))]
        ratingtask = agreement.AnnotationTask(data=taskdata)
        return str(ratingtask.alpha())
    else:
        rs1 = d1['Subj'].values.tolist()
        rs2 = d2['Subj'].values.tolist()
        rs3 = d3['Subj'].values.tolist()
        ro1 = d1['Obj'].values.tolist()
        ro2 = d2['Obj'].values.tolist()
        ro3 = d3['Obj'].values.tolist()
        taskdata_1 = [[0, str(i), str(ro1[i])] for i in range(0, len(ro1))] + [[1, str(i), str(ro2[i])] for i in range(0, len(ro2))] + [[2, str(i), str(ro3[i])] for i in range(0, len(ro3))]
        ratingtask_1 = agreement.AnnotationTask(data=taskdata_1)

        taskdata_2 = [[0, str(i), str(ro1[i])] for i in range(0, len(rs1))] + [[1, str(i), str(rs2[i])] for i in range(0, len(rs2))] + [[2, str(i), str(rs3[i])] for i in range(0, len(rs3))]
        ratingtask_2 = agreement.AnnotationTask(data=taskdata_2)
        return str(ratingtask_1.alpha()), str(ratingtask_2.alpha())


def pair_wise_agreement(d1, d2, d3, task):
    a1 = d1.where(d1.values == d2.values).notna()
    a2 = d1.where(d1.values == d3.values).notna()
    a3 = d2.where(d2.values == d3.values).notna()
    a = pd.concat([a1, a2, a3], axis=1)
    if task == 'sentiment':
        subj_agreement = a.apply(func=lambda row: np.count_nonzero(row['Subj'].values == True) / 3, axis=1).sum(
            axis=0) / len(a)
        obj_agreement = a.apply(func=lambda row: np.count_nonzero(row['Obj'].values == True) / 3, axis=1).sum(
            axis=0) / len(a)
        return str(subj_agreement), str(obj_agreement)
    else:
        agreement = a.apply(func=lambda row: np.count_nonzero(row.values == True) / 3, axis=1).sum(axis=0) / len(a)
        return str(agreement)


@click.command()
@click.option('-ia', '--input_file_a', 'input_file_a', type=str)
@click.option('-ib', '--input_file_b', 'input_file_b', type=str)
@click.option('-ic', '--input_file_c', 'input_file_c', type=str)
@click.option('-t', '--task', 'task', type=str)
def main(input_file_a, input_file_b, input_file_c, task):
    d1 = pd.read_csv(input_file_a, sep='\t')
    d2 = pd.read_csv(input_file_b, sep='\t')
    d3 = pd.read_csv(input_file_c, sep='\t')
    assert (len(d1) == len(d2) == len(d3)), 'input files should contain the same number of judgments'
    p = pair_wise_agreement(d1, d2, d3, task)
    alpha = krippendorffs_alpha(d1, d2, d3, task)
    print(f'pair-wise agreement for task {task} is {p}')
    print(f'krippendorff\'s_alpha for task {task} is {alpha}')


if __name__ == '__main__':
    main()

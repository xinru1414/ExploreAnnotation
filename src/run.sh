echo 'en'
pipenv run python preprocess.py -i ../Jobs/en/a/all.json -oa ../Results/en/a/a.txt -ob ../Results/en/a/b.txt -oc ../Results/en/a/c.txt -l en -t agency
pipenv run python preprocess.py -i ../Jobs/en/s/all.json -oa ../Results/en/s/a.txt -ob ../Results/en/s/b.txt -oc ../Results/en/s/c.txt -l en -t sentiment
pipenv run python preprocess.py -i ../Jobs/en/p/all.json -oa ../Results/en/p/a.txt -ob ../Results/en/p/b.txt -oc ../Results/en/p/c.txt -l en -t power
echo 'agreement'
pipenv run python -W ignore agreement.py -ia ../Results/en/a/a.txt -ib ../Results/en/a/b.txt -ic ../Results/en/a/c.txt -t agency
pipenv run python -W ignore agreement.py -ia ../Results/en/s/a.txt -ib ../Results/en/s/b.txt -ic ../Results/en/s/c.txt -t sentiment
pipenv run python -W ignore agreement.py -ia ../Results/en/p/a.txt -ib ../Results/en/p/b.txt -ic ../Results/en/p/c.txt -t power
#echo 'zh'
#pipenv run python preprocess.py -i ../Jobs/zh/a/all.json -oa ../Results/zh/a/a.txt -ob ../Results/zh/a/b.txt -oc ../Results/zh/a/c.txt -l zh -t agency
#pipenv run python preprocess.py -i ../Jobs/zh/s/all.json -oa ../Results/zh/s/a.txt -ob ../Results/zh/s/b.txt -oc ../Results/zh/s/c.txt -l zh -t sentiment
#pipenv run python preprocess.py -i ../Jobs/zh/p/all.json -oa ../Results/zh/p/a.txt -ob ../Results/zh/p/b.txt -oc ../Results/zh/p/c.txt -l zh -t power
#echo 'fr'
#pipenv run python preprocess.py -i ../Jobs/fr/a/all.json -oa ../Results/fr/a/a.txt -ob ../Results/fr/a/b.txt -oc ../Results/fr/a/c.txt -l fr -t agency
#pipenv run python preprocess.py -i ../Jobs/fr/s/all.json -oa ../Results/fr/s/a.txt -ob ../Results/fr/s/b.txt -oc ../Results/fr/s/c.txt -l fr -t sentiment
#pipenv run python preprocess.py -i ../Jobs/fr/p/all.json -oa ../Results/fr/p/a.txt -ob ../Results/fr/p/b.txt -oc ../Results/fr/p/c.txt -l fr -t power
#echo 'ru'
#pipenv run python preprocess.py -i ../Jobs/ru/a/all.json -oa ../Results/ru/a/a.txt -ob ../Results/ru/a/b.txt -oc ../Results/ru/a/c.txt -l ru -t agency
#pipenv run python preprocess.py -i ../Jobs/ru/s/all.json -oa ../Results/ru/s/a.txt -ob ../Results/ru/s/b.txt -oc ../Results/ru/s/c.txt -l ru -t sentiment
#pipenv run python preprocess.py -i ../Jobs/ru/p/all.json -oa ../Results/ru/p/a.txt -ob ../Results/ru/p/b.txt -oc ../Results/ru/p/c.txt -l ru -t power

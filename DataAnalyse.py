import pandas as pd
from ChRecognition import load_from_file
from operator import itemgetter
PATH = './'
# users_temp = ['揽清幽', '网卡', 'zh_ch', 'iamok', '干里马', '熊立伟']
json_file = 'statistics.json'


def load_json_file(file):
    datas = load_from_file(file)
    return datas


def create_df_datas(json_datas):
    datas = json_datas
    index = list(datas.keys())
    data = list(datas.values())
    df = pd.json_normalize(data)
    df.index = index
    df.fillna(0, inplace=True)
    df = df.applymap(lambda x: int(x))
    print(df.describe())
    return df


def analysis_df(df_data):
    print(df_data.drop_duplicates(inplace=True))
    print(df_data.size)
    score_total = {}
    for name in df_data.columns:
        name_series = df_data[name]
        name_analysis = {}
        num = name_series[name_series != 0].count()
        win = name_series[name_series > 0].count()
        rate = str(win / num * 100)[:5] + '%'
        name_analysis['局数'] = num
        name_analysis['胜场'] = win
        name_analysis['胜率'] = rate
        name_analysis['总分'] = name_series.sum()
        name_analysis['最大'] = name_series.max()
        name_analysis['最小'] = name_series.min()
        score_total[name] = name_analysis
    return df_data, score_total


def output_datas(df_analysised, score_total):
    head = ['姓 名', '总分', '局数', '胜场', '胜率', '最大', '最小']
    cell = ['总分', '局数', '胜场', '胜率', '最大', '最小']
    print("\n%d次六大天王总战绩如下：" % len(df_analysised.index))
    print('=' * 85)
    print('{0:<10}\t\t{1:<10}\t{2:<10}\t{3:<10}\t{4:<10}\t{5:<10}\t{6:<10}'.format(*head))
    print('-' * 85)
    score_total_sort = sorted(list(score_total.values()),key=itemgetter('总分'),reverse=True)
    name_list = []
    for item in score_total_sort:
    	for name in score_total.keys():
    		if score_total[name] == item:
    			name_list.append(name)
    # print(name_list)
    # print(score_total_sort)
    for name,score in dict(zip(name_list,score_total_sort)).items():
        cell_content = [score[i] for i in cell]
        if name in ['揽清幽', '干里马', '熊立伟']:
            print('{:<10}\t{:<10d}\t{:<10d}\t{:<10d}\t{:<10}\t{:<10d}\t{:<10d}'.format(
                name, *cell_content))
        else:
            print('{:<10}\t\t{:<10d}\t{:<10d}\t{:<10d}\t{:<10}\t{:<10d}\t{:<10d}'.format(
                name, *cell_content))
    print('=' * 85)
    print('\n数据统计：')
    print('-' * 85)
    print(df_analysised.describe())


def main():
    datas = load_json_file(PATH + json_file)
    df_data = create_df_datas(datas)
    df_analysised, score_total = analysis_df(df_data)
    output_datas(df_analysised, score_total)


if __name__ == '__main__':
    main()

import pandas as pd
import json
import numpy as np

json_file = './total_position.json'

def read_json(json_file):
	json_data = json.load(open(json_file,'r'))
	# print(dada)
	return json_data

def merge_data(json_data):
	position_data = []
	for key,values in json_data.items():
		for value in values:
			temp = []
			temp.append(key.split('.')[0])
			temp.extend(value)
			position_data.append(temp)
	return position_data

def create_df(position_data):
	data_array = np.array(position_data)
	df_data = pd.DataFrame(data_array,columns=['file','left','up','right','down'])
	new_df = df_data[["left","up","right","down"]].applymap(lambda x:int(x))
	new_df.insert(0,'file',df_data["file"])
	# new_df.index = df_data['file']
	print(new_df)
	return new_df

def parse_df_data(df_data):
	new_df = pd.DataFrame({"file":df_data["file"],
				"rl":df_data["right"]-df_data["left"],
						"du":df_data["down"]-df_data["up"]})
	bs0 = (new_df['rl'] >= 0) & (new_df['rl'] < 10)
	bs1 = (new_df['rl'] >= 10) & (new_df['rl'] < 20)
	bs2 = (new_df['rl'] >= 20) & (new_df['rl'] < 30)
	bs3 = (new_df['rl'] >= 30) & (new_df['rl'] < 40)
	bs4 = (new_df['rl'] >= 40) & (new_df['rl'] < 50)
	bs5 = (new_df['rl'] >= 50) & (new_df['rl'] < 60)
	bs6 = (new_df['rl'] >= 60)
	bs = [bs0,bs1,bs2,bs3,bs4,bs5,bs6]
	for i in bs:
		drop_df = new_df[i]
		print(drop_df['rl'].size)

	# dg = drop_zero.groupby(["file"])
	# for n,g in dg:
	# 	print("group name:",n,"\n",g)
	# print(new_df.describe())

if __name__ == '__main__':
	json_data = read_json(json_file)
	position_data = merge_data(json_data)
	df_data = create_df(position_data)
	parse_df_data(df_data)


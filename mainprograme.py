import ChRecognition
import DataAnalyse
import time

def main():
	ChRecognition.main()
	DataAnalyse.main()

if __name__ == '__main__':
	time_begin = time.perf_counter()
	main()
	tiem_end = time.perf_counter()
	print('程序运行耗时：{:.2f}秒'.format(tiem_end-time_begin))
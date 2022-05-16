#!/usr/bin/python
"""
draws and saves a graph of your typing exercises
"""
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap as lc

def smooth(scalars, weight=0.9):
	""" Exponential Moving Average (TensorBoard implementation)
	scalars: any sequence of numbers
	weight: between 0 and 1
	"""
	last = scalars[0]
	smoothed = list()
	for point in scalars:
		smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
		smoothed.append(smoothed_val)  # Save it
		last = smoothed_val  # Anchor the last smoothed value
	return smoothed

def show():
	df = pd.read_csv('stats.csv')

	now = time.time()
	d = lambda x: int(0.4 + (now - x)/86400)
	days = lambda x: 'day' if d(x)==1 else 'days'
	days_past = lambda t: 'today' if d(t)==0 else f'{d(t)} {days(t)} ago'
	df['Time Past'] = df.time.apply(days_past)

	#dt_func = lambda t: time.strftime("%d-%m-%Y %H:%M", time.localtime(t))
	#df['DateTime'] = df.time.apply(dt_func)

	df['Smoothed WpM'] = smooth(df['Words per minute'])
	df['Smoothed typos'] = smooth(df['Typos percentage'])

	txt_mean = round(df.len_txt.mean()/5, ndigits=1)
	d = int((df.time.iloc[-1] - df.time.iloc[0])/86400) + 1
	title = f'In {d} days you typed {df.shape[0]} text lines ({txt_mean} words per line)'
	if df.shape[0]>20:
		last10 = round(df.iloc[-10:, 1].mean(), ndigits=1)
		mean_typos = round(df.iloc[-10:, 2].mean(), ndigits=2)
		title+= f'. Average speed of last 10 lines: {last10} wpm (with {mean_typos} % of errors)'

	names = ['Words per minute', 'Smoothed WpM', 'Typos percentage', 'Smoothed typos']
	colors = ['PaleGreen', 'MediumSeaGreen', 'LightCoral', 'FireBrick']
	p = df.plot(x='Time Past', y=names, fontsize=6, figsize=(19,8), title=title,
		        grid=True, colormap=lc(colors), linewidth=2.0)
	#plt.xticks(rotation=45)
	plt.show()

	fig = p.get_figure()
	fig.savefig("typing_stats")

if __name__ == '__main__':
	show()

#!/bin/python
"""
draws and saves the graph of your typing exercises
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

split_line = lambda s: [float(string) for string in s.split(' - ')]
try:
	with open("stats.txt", "r") as file:
		stats = [split_line(line) for line in file]
except IOError:
	print("Can't read stats.txt")

df = pd.DataFrame({'time': [stat[0] for stat in stats],
                   'len_txt': [stat[3] for stat in stats],
                   'Words per minute': [stat[1] for stat in stats],
                   'Typos percentage': [stat[2] for stat in stats]})

dt_func = lambda t: time.strftime("%d-%m-%Y %H:%M", time.localtime(t))
df['DateTime'] = df.time.apply(dt_func)

df['Smoothed WpM'] = smooth(df['Words per minute'])
df['Smoothed typos'] = smooth(df['Typos percentage'])

txt_mean = round(df.len_txt.mean()/5, ndigits=1)
d = int((df.time.iloc[-1] - df.time.iloc[0])/86400) + 1
title = f'In {d} days you typed {df.shape[0]} text lines ({txt_mean} words per line)'
if df.shape[0]>20:
	last10 = round(df.iloc[-10:, 2].mean(), ndigits=1)
	title+= f'. Average speed of last 10 lines: {last10} wpm'

names = ['Smoothed WpM', 'Words per minute', 'Smoothed typos', 'Typos percentage']
colors = ['PaleGreen', 'MediumSeaGreen', 'LightCoral', 'FireBrick']
p = df.plot(x='DateTime', y=names, fontsize=6, figsize=(19,8), title=title,
	        grid=True, colormap=lc(colors), linewidth=3.0)
plt.xticks(rotation=45)
plt.show()

fig = p.get_figure()
fig.savefig("typing_stats")



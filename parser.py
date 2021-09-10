import csv
import os


THRESHOLD = 5
COLUMNS_PER_SECTION = 4
store = []
index = []
main_path = os.getcwd()

def process_section(csv_iterator, from_column, to_column, from_row):
	columns = to_column - from_column + 1
	prev_row = [0, 0, 0, 0]
	direction = 0

	# the number of inc/dec rows since the last direction turn
	current_run = 0
	line = 0
	num = 1
	for idx,row in enumerate(csv_iterator):
		line = csv_iterator.line_num
		if line >= from_row:
			# row values as integers
			row_slice = row[from_column:to_column + 1]

			if len("".join(row_slice)) != 0:
				int_row_slice = list(map(lambda s: int(s), row_slice))

				# the difference between the previous and the current row
				zipped = zip(prev_row, int_row_slice)
				row_diff = list(map(lambda tuple: tuple[0] - tuple[1], zipped))
				unique = list(set(row_diff))
				head = unique[0] # the single element of the set

				if len(unique) == 1 and head == direction:
					# all values in the diff are -1 or 1
					current_run += 1
				else:
					# register the change in direction
					if head == -1 or head == 1:
						direction = head

					if current_run + 1 >= THRESHOLD:
						store.append(((line - 1) - (line - current_run - 1)) + 1)
						print(f"{num} col:{from_column}, row: {line - current_run - 1} - {line - 1} total: {((line - 1) - (line - current_run - 1)) + 1}")
						num += 1
					current_run = 0

				prev_row = list(int_row_slice)
	# handle last row
	if current_run + 1 >= THRESHOLD:
		store.append(((line - 1) - (line - current_run)) + 1)
		print(f"{num} col: {from_column}, row: {line - current_run}-{line - 1} total: {(line-1)-(line -current_run)}")



filename = os.listdir(main_path+"/")

for i in filename:
	with open(main_path+"/"+i, 'rt') as csvfile:
		geneStats = csv.reader(csvfile, delimiter=';')

		# get row count
		row_count = sum(1 for row in geneStats)
		csvfile.seek(0)

		# get column count
		row = next(geneStats)
		column_count = len(row)


		number_of_sections = int(column_count / COLUMNS_PER_SECTION)
		print(f"{i}")
		store.append(f"{i}")
		# print(number_of_sections)


		for i in range(number_of_sections):
			# reset file
			csvfile.seek(0)
			geneStats = csv.reader(csvfile, delimiter=';')

			# process rows
			from_column = 1 + i * 7
			to_column = from_column + 3
			process_section(geneStats, from_column, to_column, 2)

new = []
for x in store:
	if type(x) is str:
		index.append(x)

with open(main_path+"/result.txt","w") as res:
	var1 = 0
	var2 = 1
	for _ in range(1,100):
		f_name1 = index[var1]
		f_name2 = index[var2]

		result = store[store.index(f_name1):store.index(f_name2)][1:]
		print(f"{f_name1}   number_of_rows: {len(result)}   number_of_genes: {sum(result)}   mean: {sum(result)/len(result)}",file=res)
		new.append(result)

		var1 += 1
		var2 += 1
	if len(new) != len(filename):
		result2 = store[store.index(index[-1]):][1:]
		print(f"{f_name2}   number_of_rows: {len(result2)}   number_of_genes: {sum(result2)}   mean: {sum(result)/len(result)}",file=res)


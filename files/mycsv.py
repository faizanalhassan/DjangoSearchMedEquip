import csv
def export_dict_list_to_csv(data, filename):
    with open(filename, 'w') as f:
        # Assuming that all dictionaries in the list have the same keys.
        headers = sorted([k for k, v in data[0].items()])
        csv_data = [headers]

        for d in data:
            csv_data.append([d[h] for h in headers])
        writer = csv.writer(f)
        writer.writerows(csv_data)

s = [{'name':'bob','age':25,'weight':200},
         {'name':'jim','age':31,'weight':180}]
export_dict_list_to_csv(s, "out.csv")
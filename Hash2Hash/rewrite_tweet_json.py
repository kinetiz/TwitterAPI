# Description: Generate file format: |h1,h2,count| for visualisation in Gelphi
# Input: json file
# Output: csv file |h1,h2,count|
######
import json
# load list output files
root = "G:\\work\\TwitterAPI\\data\\used_data\\top6-30\\"
newroot = "G:\\work\\TwitterAPI\\data\\cleaned_data\\top6-30\\"
filename_deletedate = {
    "top6-30_2018-05-24_to_2018-05-26.json":'2018-05-23',
    "top6-30_2018-05-26_to_2018-05-27.json":'2018-05-25',
    "top6-30_2018-05-27_to_2018-05-28.json":'2018-05-26',
    "top6-30_2018-05-28_to_2018-05-29.json":'2018-05-27',
    "top6-30_2018-05-29_8AM_to_31.json":'2018-05-29',
    "top6-30_2018-05-29_to_2018-05-30.json":'2018-05-28',
    "top6-30_2018-05-31_to_2018-06-04.json":'2018-05-30',
    "top6-30_2018-06-04_to_2018-06-06.json":'2018-06-03',
    "top6-30_2018-06-06_to_2018-06-08.json":'2018-06-05',
    "top6-30_2018-06-08_to_2018-06-12.json":'2018-06-07',
    "top6-30_2018-05-12_to_2018-05-15.json":'2018-05-11',
    "top6-30_2018-05-15_to_2018-05-17.json":'2018-05-14',
    "top6-30_2018-05-17_to_2018-05-24.json":'2018-05-16'
}
for filename, delete_date in filename_deletedate.items():
    with open(root+filename) as f:
        data = json.load(f)

    for i, twt in enumerate(data['tweets']):
        # print(twt)
        if (twt['created_at'].__contains__(delete_date)):
            # keep data until this entry (before this date)
            new_content = data['tweets'][0:i]
            print(len(data['tweets']) - len(new_content))
            print(' has been deleted.')
            data['tweets'] = new_content
            break
            # print(twt['created_at'])
    # print('saving file..')
    with open(newroot+filename,'w') as f:
        json.dump(data,f)
    print(newroot+filename+ ' saved..')
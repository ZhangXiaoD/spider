import csv


class DataOutput(object):

    @staticmethod
    def write_data(data):
        with open('./美剧资源.csv', 'a') as csvfile:
            fielddnames = ['title', 'url', 'down']
            write = csv.DictWriter(csvfile, fieldnames=fielddnames)
            write.writerow(data)
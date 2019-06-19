"""Fetches data from ah-django api."""
import sys
import requests
import json
import csv
import os

BASE_DIR = os.getcwd()


class GetAndExportArticleData(object):
    """Enables user to fetch data from ah-django api and export it as json."""

    def __init__(self, url):
        """Initial params."""
        super(GetAndExportArticleData, self).__init__()
        self.url = url

    def fetch_data_from_api(self):
        """Take in get url and fetches data from api."""
        try:
            data = requests.get(self.url)
        except Exception:
            try:
                raise UnboundLocalError
            except UnboundLocalError:
                sys.exit(
                    {"message": "Server  could not process your request!!!",
                     "status": 500})

        if data.status_code != 200:
            try:
                raise ValueError(
                    "The Article you are looking for could not be found")
            except ValueError:
                sys.exit({"message": "The Article you are looking for could "
                          "not be found!!!",
                          "status": 404})

        return data

    def conver_to_json(self):
        """Take data and convert it to json format."""
        json_data = self.fetch_data_from_api().json()

        return json_data

    def convert_to_csv(self):
        """Take data and convert it to csv format."""
        list_data = self.conver_to_json()

        if len(list_data) > 4:
            list_data = [list_data]

        else:
            list_data = list_data['results']

        csv_data = []

        for index, article_item in enumerate(list_data):
            if index == 0:
                header = []
                for key in article_item.keys():
                    header.append(key)

                csv_data.append(header)
            row = []
            for key, value in article_item.items():
                row.append(value)

            csv_data.append(row)

        return csv_data

    def check_path_exists(self, file_path):
        """Check if file exists in current directory."""
        if os.path.isfile(file_path):
            return True
        else:
            return False

    def autogen_filename(self, file_type, default_name=None):
        """Generate file name to save data base on existing files."""
        if default_name:
            ext = default_name.split('.')[-1]
            if ext == 'json' or ext == 'csv':
                pass

            else:
                sys.exit({
                    "error": "Unsupported file format",
                    "status": "400",
                    "message": "Your file should be a .json or .csv"
                })

        if file_type == "json" and not default_name:
            default_name = "articledata.json"

        elif file_type == "csv" and not default_name:
            default_name = "articledata.csv"

        new_file_path = '/'.join([BASE_DIR, default_name])
        exists = self.check_path_exists(new_file_path)
        if exists:
            file_name = default_name.split('.')
            ext = file_name[-1]
            file_name = file_name[0]
            try:
                number = int(file_name[-1])
                number += 1
                new_name = file_name[0:-1] + str(number)
            except ValueError:
                new_name = file_name + "1"

            file_name = '.'.join([new_name, ext])
            return self.autogen_filename(file_type, default_name=file_name)

        else:
            return default_name

    def export_to_json(self, fname=None):
        """Export and write data to json file."""
        json_data = self.conver_to_json()
        if len(json_data) > 10 and not fname:
            fname = json_data["slug"] + ".json"
        file_name = self.autogen_filename('json', default_name=fname)

        with open(file_name, 'w+') as json_file:
            json.dump(json_data, json_file, indent=4)

    def export_to_csv(self, fname=None):
        """Export and write data to csv file."""
        csv_data = self.convert_to_csv()
        if len(csv_data) == 2 and not fname:
            fname = csv_data[1][9] + '.csv'
        file_name = self.autogen_filename('csv', default_name=fname)

        csv.register_dialect(
            'ahMiniData',
            quoting=csv.QUOTE_ALL,
            skipinitialspace=True
        )

        with open(file_name, 'w+') as writter:
            write_file = csv.writer(writter, dialect='ahMiniData')
            for row in csv_data:
                write_file.writerow(row)

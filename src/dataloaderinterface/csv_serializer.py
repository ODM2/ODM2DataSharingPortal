import os

from datetime import timedelta
from django.contrib.staticfiles.storage import staticfiles_storage
from unicodecsv.py2 import UnicodeWriter


class SiteResultSerializer:
    headers = ('DateTime', 'TimeOffset', 'DateTimeUTC', 'Value', 'CensorCode', 'QualifierCode', )
    metadata_template = ''

    def __init__(self, result):
        self.result = result
        with open(os.path.join(os.path.dirname(__file__), 'metadata_template.txt'), 'r') as metadata_file:
            self.metadata_template = metadata_file.read()

    def get_file_path(self):
        filename = "{0}_{1}_{2}.csv".format(self.result.feature_action.sampling_feature.sampling_feature_code, self.result.variable.variable_code, self.result.result_id)
        return os.path.join('data', filename)

    def open_csv_file(self):
        csv_file = staticfiles_storage.open(self.get_file_path(), 'ab+')
        return csv_file

    def generate_metadata(self):
        action = self.result.feature_action.action
        equipment_model = self.result.data_logger_file_columns.first().instrument_output_variable.model
        affiliation = action.action_by.filter(is_action_lead=True).first().affiliation
        return self.metadata_template.format(
            sampling_feature=self.result.feature_action.sampling_feature,
            variable=self.result.variable,
            unit=self.result.unit,
            model=equipment_model,
            result=self.result,
            action=action,
            affiliation=affiliation
        )

    def build_csv(self):
        with self.open_csv_file() as output_file:
            output_file.write(self.generate_metadata())
            csv_writer = UnicodeWriter(output_file)
            csv_writer.writerow(self.headers)

    def add_data_value(self, data_value):
        self.add_data_values([data_value])

    def add_data_values(self, data_values):
        data = [(data_value.value_datetime,
                 data_value.value_datetime_utc_offset,
                 data_value.value_datetime - timedelta(hours=data_value.value_datetime_utc_offset),
                 data_value.censor_code,
                 data_value.quality_code)
                for data_value in data_values]
        with self.open_csv_file() as output_file:
            csv_writer = UnicodeWriter(output_file)
            csv_writer.writerows(data)

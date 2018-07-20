from SNAPI import SNREST
from SNAPI.PMTemplateUtility import TemplateUtility
import pandas as pd

def main(filename):
	dev = SNREST()

	templates = pd.read_excel(filename)

	for index, template in templates.iterrows():
		service = template["PM Assignment Group Field"]
		code = template["Task Code"]
		description = template["Task Code Description"]
		vendor = template["Vendor"]
		month = template["Month"]
		day_of_week = template["Day of the Week"]
		title = template["Title"]

		template = TemplateUtility(
	        code = code,
	        description = description,
	        service = service,
	        vendor = vendor,
	        month = month,
	        day_of_week = day_of_week,
	        title = title,)


		response = dev.create_record("sys_template", template.payload)

		templates.loc[index, 'response'] = response.status_code
		if(response.status_code==201):
			templates.loc[index, 'sys_id'] = response.json()["result"]["sys_id"]
		else:
			print(f'Error with row {index}: {response.status_code}')

	return templates

if __name__ == '__main__':
	filename = 'template_test.xlsx'
	templates = main(filename)
	with pd.ExcelWriter('templates_output.xlsx') as writer:
		templates.to_excel(writer, 'Sheet1')
		writer.save()
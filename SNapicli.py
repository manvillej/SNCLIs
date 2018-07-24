from SNAPI import SNREST
from SNAPI.PMTemplateUtility import TemplateUtility
from SNAPI.PMUtility import PreventativeMaintenance
import pandas as pd

def main_template(filename):
    dev = SNREST()

    templates = pd.read_excel(filename)

    for index, template in templates.iterrows():
        # variables for creating template 
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

def main_pm(filename):

    dev = SNREST()

    category_filename = "model_category_output.xlsx"
    model_categories = pd.read_excel(category_filename)

    model_filename = "product_model_output.xlsx"
    models = pd.read_excel(model_filename)

    pm_data = pd.read_excel(filename)

    for index, pm_record in pm_data.iterrows():

        building = pm_record["Building"]
        manufacturer = pm_record["Manufacturer"]
        model = pm_record["Facilities Model"]
        month = pm_record["Month"]
        run_every = pm_record["Schedule_Period"]
        category = pm_record["Model Category"]
        description = pm_record["Facilities Model description"]

        model_id, category_id = get_model_id(models, model, category, manufacturer, description,)

        pm = PreventativeMaintenance(
            building=building,
            manufacturer=manufacturer,
            model=model,
            month=month,
            run_every=run_every,
            model_id=model_id,
            category_id=category_id,)

        response =  dev.create_record("u_preventative_maintenance", pm.payload)

        pm_data.loc[index, 'response'] = response.status_code
        if(response.status_code==201):
            pm_data.loc[index, 'sys_id'] = response.json()["result"]["sys_id"]
        else:
            print(f'Error with row {index}: {response.status_code}')

    return pm_data

def get_model_id(models, model_name, category, manufacturer, description,):
    model = models.loc[
        (models['Name']==model_name) &
        (models['Model categories']==category) &
        (models['Manufacturer']==manufacturer) &
        (models['Description']==description)]

    return model.sys_id.values[0] , model.category_id.values[0]



if __name__ == '__main__':
    '''filename = 'template_test.xlsx'
    templates = main_template(filename)
    with pd.ExcelWriter('templates_output.xlsx') as writer:
        templates.to_excel(writer, 'Sheet1')
        writer.save()'''

    filename = 'preventative_maintenance.xlsx'
    pm_records = main_pm(filename)
    with pd.ExcelWriter('pm_output.xlsx') as writer:
        pm_records.to_excel(writer, 'Sheet1')
        writer.save()


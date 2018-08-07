from SNAPI import SNREST
from SNAPI.PMTemplateUtility import TemplateUtility
from SNAPI.PMUtility import PreventativeMaintenance
from SNAPI.PMTypeUtility import PMType
import pandas as pd
from math import isnan

def main_template(filename):
    dev = SNREST()

    templates = pd.read_excel(filename)

    for index, template in templates.head(1).iterrows():
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

def main_pm_type(filename):
    dev = SNREST()

    template_filename = 'templates_output.xlsx'
    templates = pd.read_excel(template_filename)


    pm_filename = 'pm_output.xlsx'
    pm_records = pd.read_excel(pm_filename)

    pm_type_data = pd.read_excel(filename)

    for index, pm_type_record in pm_type_data.head(1).iterrows():
        task_code = pm_type_record["task_code"]
        task_code_description = pm_type_record["task_code_description"]

        template_id = get_template_id(pm_type_record, templates)
        building_schedule_id = get_building_schedule_id(pm_type_record, pm_records)

        pm_type = PMType(
            task_code=task_code, 
            task_code_description=task_code_description,
            template_id=template_id,
            building_schedule_id=building_schedule_id,)

        response =  dev.create_record("u_preventative_maintenance", pm_type.payload)

        pm_type_data.loc[index, 'response'] = response.status_code
        if(response.status_code==201):
            pm_type_data.loc[index, 'sys_id'] = response.json()["result"]["sys_id"]
        else:
            print(f'Error with row {index} in pm_type: {response.status_code}')

    return pm_type_data

def get_model_id(models, model_name, category, manufacturer, description,):
    model = models.loc[
        (models['Name']==model_name) &
        (models['Model categories']==category) &
        (models['Manufacturer']==manufacturer) &
        (models['Description']==description)]

    return model.sys_id.values[0] , model.category_id.values[0]

def get_template_id(pm_type_record, templates):
    task_code = pm_type_record['task_code']
    task_code_description = pm_type_record['task_code_description']
    vendor = pm_type_record["vendor"]
    month = pm_type_record["month"]
    day_of_week = pm_type_record["day_of_week"]
    pm_assignment_group = pm_type_record["PM Assignment Group Field"]
    title = pm_type_record["title"]
    
    if(not isnan(title)):
        # not empty title
        template = templates.loc[
            (templates["PM Assignment Group Field"]=="PM HVAC") &
            (templates["Task Code"]=="ENE Inspect") &
            (templates["Task Code Description"]=="Inspect") &
            (templates["Vendor"]=="ENE") &
            (templates["Month"]=="September") &
            (templates["Day of the Week"]=="Monday") & 
            (templates["Title"]=="")]
    else:
        # empty title
        template = templates.loc[
            (templates["PM Assignment Group Field"]=="PM HVAC") &
            (templates["Task Code"]=="ENE Inspect") &
            (templates["Task Code Description"]=="Inspect") &
            (templates["Vendor"]=="ENE") &
            (templates["Month"]=="September") &
            (templates["Day of the Week"]=="Monday") & 
            (templates["Title"].isnull())]

    return template.sys_id.values[0]

def get_building_schedule_id(pm_type_record, pm_records):
    building = pm_type_record["building"]
    manufacturer = pm_type_record["manufacturer"]
    model = pm_type_record["model"]
    month = pm_type_record["month"]
    model_category = pm_type_record["model_category"]
    model_description = pm_type_record["model_description"]
    schedule_period = pm_type_record["schedule_period"]

    pm_record = pm_records.loc[
        (pm_records["Building"]==building) & 
        (pm_records["Manufacturer"]==manufacturer) & 
        (pm_records["Model Category"]==model_category) & 
        (pm_records["Facilities Model"]==model) & 
        (pm_records["Facilities Model description"]==model_description) & 
        (pm_records["Schedule_Period"]==schedule_period) & 
        (pm_records["Month"]==month)]

    return pm_record.sys_id.values[0]


if __name__ == '__main__':
    filename = 'sys_template_input.xlsx'
    templates = main_template(filename)
    with pd.ExcelWriter('templates_output.xlsx') as writer:
        templates.to_excel(writer, 'Sheet1')
        writer.save()

    filename = 'preventative_maintenance.xlsx'
    pm_records = main_pm(filename)
    with pd.ExcelWriter('pm_output.xlsx') as writer:
        pm_records.to_excel(writer, 'Sheet1')
        writer.save()

    filename = 'pm_type_data.xlsx'
    pm_type_data = main_pm_type(filename)

    with pd.ExcelWriter('pm_type_output.xlsx') as writer:
        pm_type_data.to_excel(writer, 'Sheet1')
        writer.save()



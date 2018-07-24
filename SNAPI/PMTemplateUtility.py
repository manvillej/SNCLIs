from .ServiceConfigurations import hvac, life_safety, plumbing, vendors

class TemplateUtility(object):
    def __init__(self, **kwargs):
        super(TemplateUtility, self).__init__()

        self.payload = self.get_template_payload()

        code = kwargs.pop("code", False)
        description = kwargs.pop("description", False)

        service = kwargs.pop("service", False)
        service = self.get_pm_service_info(service)

        vendor = kwargs.pop("vendor", False)
        month = kwargs.pop("month", False)
        day_of_week = kwargs.pop("day_of_week", False)
        title = kwargs.pop("title", False)



        if(code and description and service and vendor and month and day_of_week and title):
            self.payload["name"] = self.get_template_name(code, description)
            self.payload["template"] = self.create_template(
                service.assignment_group,
                service.service_type,
                service.service,
                vendor,
                code,
                description,
                month,
                day_of_week,
                title)
        else:
            print(code)
            print(description)
            print(service)
            print(vendor)
            print(month)
            print(day_of_week)
            print(title)
            raise RuntimeError("""
                The Following keyword arguments must all be used together to work properly:
                assignment_group, service_type, service, vendor, code, description, month, day_of_week, title
                """)





    def get_template_name(self, task_code, task_code_description):
        """"""
        template_name = task_code + " " + task_code_description 
        return template_name[:100]

    def get_template_payload(self):
        payload = {
            "user":"",
            "global":True,
            "table":"facilities_request_task",
            "name":"",
            "template":""
        }
        return payload

    def create_template(self, 
        group,
        service_type,
        service,
        vendor,
        task_code,
        task_code_description,
        month,
        day_of_week,
        title):
        # set assignment group
        template = (f'assignment_group={group}'
            f'^u_service_type={service_type}'
            f'^u_application_service={service}'
            f'^u_vendor={vendor}'
            f'^description={task_code}'
            f' {task_code_description}'
            f'\n{month}'
            f'\n{day_of_week}'
            f'\n{title}'
            ) 

        # set description
        return template

    def get_pm_service_info(self, service):
        configurations = {
            "PM HVAC":hvac,
            "PM Life Safety":life_safety,
            "PM Plumbing":plumbing
        }

        return configurations[service]

    def get_vendor_id(self, vendor):
        return vendors[vendor]


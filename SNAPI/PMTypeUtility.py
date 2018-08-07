
class PMType(object):
    """docstring for PMType"""
    def __init__(self, **kwargs):
        super(PMType, self).__init__()
        self.payload = self.get_template_payload()

        task_code = kwargs.pop('task_code', False)
        task_code_description = kwargs.pop('task_code_description', False)
        template_id = kwargs.pop('template_id', False)
        building_schedule_id = kwargs.pop('building_schedule_id', False)

        if(not task_code):
            raise RuntimeError(f'Task Code was not defined when creating a PMType object: {task_code}')
        if(not task_code_description):
            raise RuntimeError(f'Task Code Description was not defined when creating a PMType object: {task_code_description}')
        if(not template_id):
            raise RuntimeError(f'Template ID was not defined when creating a PMType object: {template_id}')
        if(not building_schedule_id):
            raise RuntimeError(f'Building Schedule was not defined when creating a PMType object: {building_schedule_id}')

        self.payload["u_template"] = template_id
        self.payload["u_building_schedule"] = building_schedule_id
        self.payload["u_description"] = self.get_description(task_code, task_code_description)



    def get_template_payload(self):
        payload = {
            'u_run_type':"Asset",
            'u_template_type':"Work Order Task",
            'u_description':'',
            'u_template':'',
            'u_building_schedule':'',

        }
        return payload


    def get_description(self, task_code, task_code_description):
        """"""
        template_name = task_code + " " + task_code_description 
        return template_name[:40]


def main():
    pm_type = PMType(
        task_code="task_code", 
        task_code_description="task_code_description",
        template_id="template_id",
        building_schedule_id="building_schedule_id",)
    print(pm_type.payload)

if __name__ == '__main__':
    main()
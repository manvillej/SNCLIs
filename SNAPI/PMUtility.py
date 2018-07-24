from datetime import date

class PreventativeMaintenance(object):
    """docstring for PreventativeMaintenance"""
    def __init__(self, **kwargs):
        super(PreventativeMaintenance, self).__init__()
        self.today = date.today()

        self.payload = self.get_template_payload()

        building_name = kwargs.pop("building", False)
        manufacturer_name = kwargs.pop("manufacturer", False)
        model_name = kwargs.pop("model", False)
        month = kwargs.pop("month", False)
        run_every = kwargs.pop("run_every", False)

        model_id = kwargs.pop("model_id", False)
        category_id = kwargs.pop("category_id", False)

        if(not model_id):
            raise RuntimeError('model_id not provided when defining PreventativeMaintenance')

        if(not category_id):
            raise RuntimeError('category_id not provided when defining PreventativeMaintenance')


        self.payload["u_name"] = self.get_name(building_name, manufacturer_name, model_name, month)
        self.payload["u_next_run"] = self.get_next_run(month)
        self.payload["u_run_every"] = self.get_run_every(run_every)
        self.payload["u_building"] = self.get_building(building_name)
        self.payload["u_asset_model"] = model_id
        self.payload["u_model_category"] = category_id

    def get_template_payload(self):
        payload = {
            "u_name":"",
            "u_next_run":"",
            "u_run_type":"Asset",
            "u_run_every":"",
            "u_model_category":"",
            "u_asset_model":"",
            "u_building":"",
        }
        return payload

    def get_name(
            self,
            building_name,
            manufacturer_name,
            model_name,
            month):
        #proper short case for month
        month = month[:3].title()
        name = f'{building_name} {manufacturer_name} {model_name} {month}'
        return name

    def get_run_every(self, run_every_type):
        choices = {
            '6 months':'Six Months',
            'yearly':'Year',
            'monthly':'Month',
            'weekly':'Weekly',
            '2 weeks':'Bi-weekly',
        }
        run_every = choices.get(run_every_type.lower(), False)

        if(not run_every):
            raise RuntimeError(f'Run every was not found in record: {run_every_type}')

        return run_every

    def get_next_run(self, month_name):
        month = month_name[:3].lower()
        months = {
            "jan":1,
            "feb":2,
            "mar":3,
            "apr":4,
            "may":5,
            "jun":6,
            "jul":7,
            "aug":8,
            "sept":9,
            "oct":10,
            "nov":11,
            "dec":12,
        }
        month = months.get(month, False)

        if(not month):
            raise RuntimeError(f'Month not found in dict: {month_name}')

        next_run = date(self.today.year, month, 1)

        before_today = next_run - self.today

        if(before_today.days<1):
            next_run = date(self.today.year + 1, month, 1)

        return f'{next_run.year}-{next_run.month:02.0f}-{next_run.day:02.0f}'

    def get_building(self, building_name):
        buildings = {
            "114 Western Avenue":'7a0941b06ffb2600602319bdbb3ee418',
            "14 Story Street":'4768d115dbc783005d29f1431d96190d',
            "175 North Harvard Street":'cc6533196f36d2005f69c0bcbb3ee4ad',
            "25 Travis Street":'bd15ffd56f36d2005f69c0bcbb3ee4a8',
            "Aldrich Hall":'3b05ffd56f36d2005f69c0bcbb3ee4a6',
            "Baker Library | Bloomberg Center":'c115ffd56f36d2005f69c0bcbb3ee4a8',
            "Batten Hall":'435533196f36d2005f69c0bcbb3ee4ad',
            "Bright Hockey Center":'1f25ffd56f36d2005f69c0bcbb3ee4ac',
            "Burden Hall":'5015ffd56f36d2005f69c0bcbb3ee4a7',
            "Chao Center":'b39f5e516f8caa005f69c0bcbb3ee43c',
            "Chapel":'9015ffd56f36d2005f69c0bcbb3ee4a7',
            "Chase Hall":'7605ffd56f36d2005f69c0bcbb3ee4a5',
            "Chilled Water Plant":'0615ffd56f36d2005f69c0bcbb3ee4a9',
            "Connell House":'9f05ffd56f36d2005f69c0bcbb3ee4a5',
            "Cotting House":'f605ffd56f36d2005f69c0bcbb3ee4a5',
            "Crimson Commons":'2e6533196f36d2005f69c0bcbb3ee4af',
            "Cumnock Hall":'4b05ffd56f36d2005f69c0bcbb3ee4a5',
            "Dean's House":'cb05ffd56f36d2005f69c0bcbb3ee4a5',
            "Dillon House":'0f05ffd56f36d2005f69c0bcbb3ee4a5',
            "Esteves Hall":'c815ffd56f36d2005f69c0bcbb3ee4a6',
            "Gallatin Hall":'df05ffd56f36d2005f69c0bcbb3ee4a5',
            "Glass Hall":'e305ffd56f36d2005f69c0bcbb3ee4a6',
            "Gordon Indoor Track&Tennis Ctr":'6325ffd56f36d2005f69c0bcbb3ee4ad',
            "Greenhill House":'9c15ffd56f36d2005f69c0bcbb3ee4a6',
            "Hamilton Hall":'6705ffd56f36d2005f69c0bcbb3ee4a6',
            "Harvard Life Lab":'72cf113e6fc3ea0002070f1aea3ee41a',
            "Hawes Hall":'4b25ffd56f36d2005f69c0bcbb3ee4ac',
            "HBS Campus":'2d090f0f6f7de600542b373aea3ee484',
            "Klarman Hall":'0f1837f6db2bc3405d29f1431d96192c',
            "Kresge Hall":'f815ffd56f36d2005f69c0bcbb3ee4a7',
            "Loeb House":'7c15ffd56f36d2005f69c0bcbb3ee4a7',
            "Ludcke House":'bc15ffd56f36d2005f69c0bcbb3ee4a7',
            "McArthur Hall":'2715ffd56f36d2005f69c0bcbb3ee4aa',
            "McCollum Center":'0115ffd56f36d2005f69c0bcbb3ee4a8',
            "McCulloch Hall":'4115ffd56f36d2005f69c0bcbb3ee4a8',
            "Mellon Hall":'9515ffd56f36d2005f69c0bcbb3ee4a8',
            "Morgan Hall":'6415ffd56f36d2005f69c0bcbb3ee4a7',
            "Morris Hall":'1915ffd56f36d2005f69c0bcbb3ee4a8',
            "Rock Center":'2815ffd56f36d2005f69c0bcbb3ee4a7',
            "Shad Hall":'3d15ffd56f36d2005f69c0bcbb3ee4a8',
            "Spangler Center":'7815ffd56f36d2005f69c0bcbb3ee4a7',
            "Tata Hall":'4c6533196f36d2005f69c0bcbb3ee4ad',
            "Teele Hall":'b115ffd56f36d2005f69c0bcbb3ee4a9',
            "Wilder House":'3115ffd56f36d2005f69c0bcbb3ee4a9',
            "Wyss House":'fd15ffd56f36d2005f69c0bcbb3ee4a8',}

        building = buildings.get(building_name, False)

        if(not building):
            raise RuntimeError(f'Building not found in buildings: {building_name}')
        
        return building



def main():
    pm = PreventativeMaintenance(
        building="Batten Hall",
        manufacturer="Siemens",
        model="model_name",
        month="February",
        run_every="6 months",
        model_id="model_id",
        category_id="category_id",)
    print(pm.payload)
    # pm.get_name("25 Travis Street", "Siemens", "Air Conditioner", "february" )
    # pm.get_run_every('6 months')
    # pm.get_run_every('yearly')
    # pm.get_run_every('monthly')
    # pm.get_run_every('weekly')
    # pm.get_run_every('2 weeks')
    # pm.get_next_run("november")
    # pm.get_next_run("November")
    # pm.get_next_run("february")
    # print(pm.get_building("114 Western Avenue"))
    # print(pm.get_building("14 Story Street"))
    # print(pm.get_building("175 North Harvard Street"))
    # print(pm.get_building("25 Travis Street"))
    # print(pm.get_building("Aldrich Hall"))
    # print(pm.get_building("Baker Library | Bloomberg Center"))
    # print(pm.get_building("Batten Hall"))
    # print(pm.get_building("Bright Hockey Center"))
    # print(pm.get_building("Burden Hall"))
    # print(pm.get_building("Chao Center"))
    # print(pm.get_building("Chapel"))
    # print(pm.get_building("Chase Hall"))
    # print(pm.get_building("Chilled Water Plant"))
    # print(pm.get_building("Connell House"))
    # print(pm.get_building("Cotting House"))
    # print(pm.get_building("Crimson Commons"))
    # print(pm.get_building("Cumnock Hall"))
    # print(pm.get_building("Dean's House"))
    # print(pm.get_building("Dillon House"))
    # print(pm.get_building("Esteves Hall"))
    # print(pm.get_building("Gallatin Hall"))
    # print(pm.get_building("Glass Hall"))
    # print(pm.get_building("Gordon Indoor Track&Tennis Ctr"))
    # print(pm.get_building("Greenhill House"))
    # print(pm.get_building("Hamilton Hall"))
    # print(pm.get_building("Harvard Life Lab"))
    # print(pm.get_building("Hawes Hall"))
    # print(pm.get_building("HBS Campus"))
    # print(pm.get_building("Klarman Hall"))
    # print(pm.get_building("Kresge Hall"))
    # print(pm.get_building("Loeb House"))
    # print(pm.get_building("Ludcke House"))
    # print(pm.get_building("McArthur Hall"))
    # print(pm.get_building("McCollum Center"))
    # print(pm.get_building("McCulloch Hall"))
    # print(pm.get_building("Mellon Hall"))
    # print(pm.get_building("Morgan Hall"))
    # print(pm.get_building("Morris Hall"))
    # print(pm.get_building("Rock Center"))
    # print(pm.get_building("Shad Hall"))
    # print(pm.get_building("Spangler Center"))
    # print(pm.get_building("Tata Hall"))
    # print(pm.get_building("Teele Hall"))
    # print(pm.get_building("Wilder House"))
    # print(pm.get_building("Wyss House"))


if __name__ == '__main__':
    main()

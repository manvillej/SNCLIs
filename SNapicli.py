from SNAPI import SNREST
from SNAPI.PMTemplateUtility import TemplateUtility

dev = SNREST()

template = TemplateUtility(
        code="Siemens Inspect Boiler Start-up",
        description="BOILER, STEAM, GAS/OIL, START-UP INSPECTION",
        service="PM HVAC",
        vendor="NO VENDOR",
        month="month",
        day_of_week="day_of_week",
        title="title")

dev.create_record("sys_template", template.payload)
from collections import namedtuple

Service = namedtuple('Service', ["service", "service_type", "assignment_group"])

hvac = Service(
	"298575a26fb9a240c306511bbb3ee41e",
	"c46ddb326f75e240c306511bbb3ee4d1",
	"6a8171226f3162405f6990bcbb3ee48b",)

life_safety = Service(
	"place holder",
	"place holder",
	"place holder",)

plumbing = Service(
	"268cdffe6f35e240c306511bbb3ee423",
	"142cd77e6f7962405f6990bcbb3ee4ba",
	"72eddb326f75e240c306511bbb3ee443",)

vendors = {
	"ENE":"place holder",
	"SIEMENS":"place holder",
	"NO VENDOR":"",
}
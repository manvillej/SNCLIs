import click
from SNAPI import SNREST
from SNAPI import PMTemplateUtility as TemplateUtil

@click.command()
@click.option('--env', default=False)
def template():
	dev = SNREST()
	payload = {
		"table":"facilities_request_task"
		"name":
	}
	print("Hello")



if __name__ == '__main__':
	template()


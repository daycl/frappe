from __future__ import unicode_literals
import click
import frappe
import os
import json
import importlib
import frappe.utils

def main():
	commands = get_app_groups()
	commands.update({'get-frappe-commands': get_frappe_commands,
			'get-frappe-help': get_frappe_help
			})
	click.Group(commands=commands)(prog_name='bench')

def get_app_groups():
	ret = {}
	for app in ["frappe"]: #get_apps():
		app_group = get_app_group(app)
		if app_group:
			ret[app] = app_group
	return ret

def get_app_group(app):
	app_commands = get_app_commands(app)
	if app_commands:
		return click.group(name=app, commands=app_commands)(app_group)

@click.option('--site')
@click.option('--profile', is_flag=True, default=False, help='Profile')
@click.option('--verbose', is_flag=True, default=False, help='Verbose')
@click.option('--force', is_flag=True, default=False, help='Force')
@click.pass_context
def app_group(ctx, site, force, verbose, profile):
	ctx.obj = {
		'sites': get_sites(site),
		'force': force,
		'verbose': verbose,
		'profile': profile
	}
	if ctx.info_name == 'frappe':
		ctx.info_name = ''

def get_sites(site_arg):
	if site_arg and site_arg == 'all':
		return frappe.utils.get_sites()
	else:
		if site_arg:
			return [site_arg]
		if os.path.exists('currentsite.txt'):
			with open('currentsite.txt') as f:
				return [f.read().strip()]

def get_app_commands(app):
	try:
		app_command_module = importlib.import_module(app + '.commands')
	except ImportError:
		return []

	ret = {}
	for command in getattr(app_command_module, 'commands', []):
		ret[command.name] = command
	return ret

@click.command('get-frappe-commands')
def get_frappe_commands():
	print json.dumps(get_app_commands('frappe').keys())

@click.command('get-frappe-help')
def get_frappe_help():
	print click.Context(get_app_group('frappe')).get_help()

def get_apps():
	return frappe.get_all_apps(with_internal_apps=False, sites_path='.')

if __name__ == "__main__":
	main()


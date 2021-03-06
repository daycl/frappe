# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals
import hmac
import urllib
from frappe import _

import frappe
import frappe.utils

def get_signed_params(params):
	"""Sign a url by appending `&_signature=xxxxx` to given params (string or dict).

	:param params: String or dict of parameters."""
	if not isinstance(params, basestring):
		params = urllib.urlencode(params)

	signature = hmac.new(params)
	signature.update(get_secret())
	return params + "&_signature=" + signature.hexdigest()

def get_secret():
	return frappe.local.conf.get("secret") or str(frappe.db.get_value("User", "Administrator", "creation"))

def verify_request():
	"""Verify if the incoming signed request if it is correct."""
	query_string = frappe.request.query_string if hasattr(frappe.request, "query_string") \
		else frappe.local.flags.signed_query_string

	params, signature = query_string.split("&_signature=")

	given_signature = hmac.new(params.encode("utf-8"))

	given_signature.update(get_secret())
	valid = signature == given_signature.hexdigest()

	if not valid:
		frappe.respond_as_web_page(_("Invalid Link"),
			_("This link is invalid or expired. Please make sure you have pasted correctly."))
	return valid

def get_url(cmd, params, nonce=None, secret=None):
	if not nonce:
		nonce = params
	signature = get_signature(params, nonce, secret)
	params['signature'] = signature
	return frappe.utils.get_url("".join(['api/method/', cmd, '?', urllib.urlencode(params)]))

def get_signature(params, nonce, secret=None):
	params = "".join((frappe.utils.cstr(p) for p in params.values()))
	if not secret:
		secret = frappe.local.conf.get("secret") or "secret"

	signature = hmac.new(str(nonce))
	signature.update(secret)
	signature.update(params)
	return signature.hexdigest()

def verify_using_doc(doc, signature, cmd):
	params = doc.get_signature_params()
	return signature == get_signature(params, doc.get_nonce())

def get_url_using_doc(doc, cmd):
	params = doc.get_signature_params()
	return get_url(cmd, params, doc.get_nonce())

# -*- coding: UTF-8 -*-
# customBrowseMode: trigger profiles in browse mode
# Copyright (C) 2023 Noelia Ruiz Martínez
# Released under GPL 2

import addonHandler
import globalPluginHandler
import globalVars
import ui
import config
from treeInterceptorHandler import post_browseModeStateChange
from logHandler import log

addonHandler.initTranslation()

browseModeProfile = "browseMode"

def handleBrowseModeStateChange(browseMode):
	if browseMode:
		config.conf.manualActivateProfile(browseModeProfile)
	else:
		config.conf.manualActivateProfile(None)

def disableInSecureMode(decoratedCls):
	if globalVars.appArgs.secure:
		return globalPluginHandler.GlobalPlugin
	return decoratedCls


@disableInSecureMode
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super().__init__()
		if browseModeProfile not in config.conf.listProfiles():
			config.conf.createProfile(browseModeProfile)
		post_browseModeStateChange.register(handleBrowseModeStateChange)

	def terminate(self):
		post_browseModeStateChange.unregister(handleBrowseModeStateChange)

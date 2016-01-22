###############################################################################
## @file product.mk
##
##
## Product common alchemy variables.
###############################################################################

# Product common config dir
COMMON_CONFIG_UNIX_DIR := $(call my-dir)

include $(COMMON_CONFIG_UNIX_DIR)/../common.mk

# use global config for all variantes
CONFIG_GLOBAL_FILE := $(COMMON_CONFIG_UNIX_DIR)/global.config
custom.libARNetwork.config :=$(COMMON_CONFIG_UNIX_DIR)/libARNetwork.config
custom.liblynx.config :=$(COMMON_CONFIG_UNIX_DIR)/liblynx.config

prebuilt.json.override := 1
prebuilt.ncurses.override := 1

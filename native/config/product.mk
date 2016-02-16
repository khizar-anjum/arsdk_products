
NATIVE_CONFIG_DIR := $(call my-dir)

# Include common product.mk
include $(NATIVE_CONFIG_DIR)/../../common/config/product.mk

# Use our own json version
prebuilt.json.override := 1

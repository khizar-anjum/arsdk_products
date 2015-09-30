#This file in automatically included by alchemy.

include $(TARGET_CONFIG_DIR)/../../../common/config/iOS/product.mk

TARGET_AR = $(shell xcrun --find --sdk iphoneos ar)
TARGET_OS_FLAVOUR = iphoneos

TARGET_ARCH = arm

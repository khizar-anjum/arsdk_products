#This file in automatically included by alchemy.

include $(TARGET_CONFIG_DIR)/../../../common/config/iOS/product.mk

TARGET_AR = $(shell xcrun --find --sdk iphonesimulator ar)
TARGET_OS_FLAVOUR = iphonesimulator

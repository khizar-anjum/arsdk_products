#===============================================================================
# Android tasks.
#===============================================================================

import dragon
import os

def hook_post_buildjni(task, args):
    arfreeflight_android_jni_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "Android", "ARFreeFlight", "jni")

    # Call ndk-build
    variant = dragon.VARIANT.replace("_", "-")
    dragon.exec_dir_cmd(dirpath=arfreeflight_android_jni_dir, cmd="ndk-build TARGET_ARCH_ABI=" + variant)

def hook_post_buildapp(task, args):
    arbuildutils_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARBuildUtils")
    arfreeflight_android_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "Android")
    arfreeflight_android_script_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "Android", "script")

    # Build application
    dragon.exec_dir_cmd(dirpath=arbuildutils_dir, cmd="./generateAndroidResources.sh")
    dragon.exec_dir_cmd(dirpath=arbuildutils_dir, cmd="./generateLocalPropertiesFile.py")
    dragon.exec_dir_cmd(dirpath=arfreeflight_android_script_dir, cmd="./generateCompatiblesDevices.py")
    dragon.exec_dir_cmd(dirpath=arfreeflight_android_dir, cmd="./gradlew assembleDebug")

#===============================================================================
# Tasks
#===============================================================================

dragon.add_meta_task(
    name = "buildjni",
    desc = "Build SDK & JNI",
    subtasks = ["build"],
    posthook = hook_post_buildjni
)

dragon.add_meta_task(
    name = "buildapp",
    desc = "Build SDK, JNI & generate application",
    subtasks = ["buildjni"],
    posthook = hook_post_buildapp
)

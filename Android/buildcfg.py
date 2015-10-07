#===============================================================================
# Android tasks.
#===============================================================================

import dragon
import os
import pprint

def build_jni():
    arfreeflight_android_jni_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "Android", "ARFreeFlight", "jni")

    # Call ndk-build
    dragon.exec_dir_cmd(dirpath=arfreeflight_android_jni_dir, cmd="ndk-build")

def build_app():
    arbuildutils_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARBuildUtils")
    arfreeflight_android_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "Android")
    arfreeflight_android_script_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "Android", "script")

    # Build application
    dragon.exec_dir_cmd(dirpath=arbuildutils_dir, cmd="./generateAndroidResources.sh")
    dragon.exec_dir_cmd(dirpath=arbuildutils_dir, cmd="./generateLocalPropertiesFile.py")
    dragon.exec_dir_cmd(dirpath=arfreeflight_android_script_dir, cmd="./generateCompatiblesDevices.py")
    dragon.exec_dir_cmd(dirpath=arfreeflight_android_dir, cmd="./gradlew assembleDebug")

def pre_hook_variant_forall_task(tasklist, tasksargs):
    dragon.LOGI("pre_hook_variant_forall_task")

def post_hook_variant_forall_task(tasklist, tasksargs):
    dragon.LOGI("post_hook_variant_forall_task")
    # dragon.LOGI(pprint.pformat(tasklist))
    # dragon.LOGI(pprint.pformat(tasksargs))
    gen_jni = False
    gen_app = False
    args_jni = None
    args_app = None

    if "build-jni" in tasklist:
        gen_jni = True
        args_jni = tasksargs[tasklist.index("build-jni")]
    if "build-app" in tasklist:
        gen_jni = True
        gen_app = True
        args_app = tasksargs[tasklist.index("build-app")]

    if gen_jni:
        build_jni()
    if gen_app:
        build_app()

#===============================================================================
# Tasks
#===============================================================================

dragon.add_meta_task(
    name = "build-sdk",
    desc = "Build SDK",
    subtasks = ["build"],
)

dragon.add_meta_task(
    name = "build-jni",
    desc = "Build SDK & JNI",
    subtasks = ["build-sdk"],
)

dragon.add_meta_task(
    name = "build-app",
    desc = "Build SDK, JNI & generate application",
    subtasks = ["build-jni"],
)

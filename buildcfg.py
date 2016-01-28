
import sys, os
import dragon

# Disable all default tasks and import arsdk ones
dragon.disable_def_tasks()
from arsdktasks import *

android_samples_dir = os.path.join(dragon.WORKSPACE_DIR,
        "packages", "Samples", "Android")

#===============================================================================
#===============================================================================
def build_android_jni(dirpath, args):
    dragon.exec_dir_cmd(dirpath=dirpath, cmd="${ANDROID_NDK_PATH}/ndk-build")

#===============================================================================
#===============================================================================
def build_android_app(dirpath, args, release=False):
    # Build application
    cmd = "./gradlew "
    cmd += "assembleRelease " if release else "assembleDebug "
    if args:
        cmd += " ".join(args)
    dragon.exec_dir_cmd(dirpath=dirpath, cmd=cmd)

#===============================================================================
#===============================================================================
def build_ios_app(dirpath, project, args, release=False):
    # Build application
    cmd = "xcodebuild "
    cmd += "-project %s " % project
    cmd += "-configuration Release " if release else "-configuration Debug "
    if args:
        cmd += " ".join(args)
    dragon.exec_dir_cmd(dirpath=dirpath, cmd=cmd)

#===============================================================================
#===============================================================================
if dragon.VARIANT == "android":
    all_samples = []
    for sample in os.listdir(android_samples_dir):
        dragon.add_meta_task(
            name = "build-jni-%s" % sample,
            desc = "Build android sdk & jni for %s" % sample,
            subtasks = ["build-sdk"],
            posthook = lambda task, args: build_android_jni(
                    os.path.join(android_samples_dir, sample, "app", "jni"),
                    args)
        )

        dragon.add_meta_task(
            name = "build-sample-%s" % sample,
            desc = "Build android sdk & jni & sample for %s" % sample,
            subtasks = ["build-jni-%s" % sample],
            posthook = lambda task, args: build_android_app(
                    os.path.join(android_samples_dir, sample),
                    args, release=False)
        )

        all_samples.append("build-sample-%s" % sample)

    dragon.add_meta_task(
        name = "build-samples",
        desc = "Build all android samples",
        subtasks = all_samples
    )

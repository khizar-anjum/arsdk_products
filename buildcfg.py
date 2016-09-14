
import sys, os
import dragon

# Disable all default tasks and import arsdk ones
keep_list = [
    "alchemy",
    "geneclipse",
    "publish",
    "reference-checker",
    "reference-creator",
]
dragon.disable_def_tasks(keep_list=keep_list)
from arsdktasks import *

android_arsdk3_dir = os.path.join(dragon.WORKSPACE_DIR,
        "packages", "ARSDK3")

android_sample_dir = os.path.join(dragon.WORKSPACE_DIR,
        "packages", "Samples", "Android", "SDKSample")

ios_sample_dir = os.path.join(dragon.WORKSPACE_DIR,
        "packages", "Samples", "iOS", "SDKSample")

#===============================================================================
# Android
#===============================================================================
def build_android_jni(dirpath, args):
    outdir = os.path.join(dragon.OUT_DIR, "jni")
    args = "NDK_OUT=%s" % os.path.join(outdir, "obj")
    args += " PRODUCT_OUT_DIR=%s" % dragon.OUT_DIR
    args += " PACKAGES_DIR=%s" % os.path.join(dragon.WORKSPACE_DIR, "packages")
    dragon.exec_cmd(
        cmd="${ANDROID_NDK_PATH}/ndk-build %s" % args,
        cwd=dirpath)

def build_android_app(dirpath, args, release=False):
    # Build application
    cmd = "./gradlew "
    cmd += "assembleRelease " if release else "assembleDebug "
    if args:
        cmd += " ".join(args)
    dragon.exec_cmd(cmd=cmd, cwd=dirpath)

def publish_android_sdk():
    # Build application
    cmd = "./gradlew "
    cmd += "bintrayUpload"
    dragon.exec_cmd(cmd=cmd, cwd=android_arsdk3_dir)

if dragon.VARIANT == "android":
    dragon.add_meta_task(
            name = "build-jni",
            desc = "Build android sdk & jni",
            subtasks = ["build-sdk"],
            posthook = lambda task, args: build_android_jni(
                os.path.join(android_arsdk3_dir, "arsdk", "jni"),
                args)
    )

    dragon.add_meta_task(
            name = "publish",
            desc = "Build android sdk & jni",
            subtasks = ["build-jni"],
            posthook = lambda task, args: publish_android_sdk()
    )

    if os.path.exists(android_sample_dir):
        dragon.add_meta_task(
            name = "build-sample",
            desc = "Build the android sample in debug",
            subtasks = ["build-jni"],
            posthook = lambda task, args: build_android_app(
                os.path.join(android_sample_dir, "buildWithLocalSDK"),
                args, release=False)
        )

#===============================================================================
# iOS
#===============================================================================
def build_ios_app(dirpath, project, sdk, args, release=False):
    # Build application
    cmd = "xcodebuild "
    cmd += "-project %s " % project
    cmd += "-sdk %s " % sdk
    cmd += "-configuration DebugWithLocalSDK "
    if sdk == "iphonesimulator":
        cmd += "-arch x86_64 "
    if args:
        cmd += " ".join(args)
    dragon.exec_cmd(cmd=cmd, cwd=dirpath)

if dragon.VARIANT == "ios" or dragon.VARIANT == "ios_sim":
    if os.path.exists(android_sample_dir):
        dragon.add_meta_task(
            name = "build-sample",
            desc = "Build the ios samples in debug",
            subtasks = ["build-sdk"],
            posthook = lambda task, args: build_ios_app(
                ios_sample_dir,
                "SDKSample.xcodeproj",
                "iphoneos" if dragon.VARIANT == "ios" else "iphonesimulator",
                args, release=False)
            )

#===============================================================================
# Unix
#===============================================================================

def add_unix_sample(sample):
    dragon.add_alchemy_task(
        name = "build-sample-%s" % sample,
        desc = "Build unix sdk sample for %s" % sample,
        product = dragon.PRODUCT,
        variant = dragon.VARIANT,
        defargs = [sample],
    )

if dragon.VARIANT == "native":
    all_samples = []
    samples = ["BebopDroneDecodeStream", "BebopDroneReceiveStream",
               "BebopPilotingNewAPI", "JumpingSumoPilotingNewAPI",
               "JumpingSumoChangePosture", "JumpingSumoPiloting",
               "JumpingSumoReceiveStream"]
    for sample in samples:
        add_unix_sample(sample)
        all_samples.append("build-sample-%s" % sample)

    dragon.add_meta_task(
        name = "build-sample",
        desc = "Build all native samples",
        subtasks = all_samples
    )

#===============================================================================
# generate sources task
#===============================================================================
def hook_gen_sources(task, args):
    packages_dir = os.path.join(dragon.WORKSPACE_DIR, "packages")
    for package in os.listdir(packages_dir):
        try:
            path = os.path.join(packages_dir, package)
            if os.path.isfile(os.path.join(path, "updateGenerated.sh")):
                dragon.exec_cmd(cmd="./updateGenerated.sh", cwd=path)
                dragon.exec_cmd(cmd="git status", cwd=path)
        except dragon.TaskError as ex:
            dragon.logging.error(str(ex))

dragon.add_meta_task(
    name = "gensources",
    desc = "Generate all sdk sources",
    posthook = hook_gen_sources,
)


import os
import dragon

#===============================================================================
#===============================================================================

# For compatibility with previous output directory hierarchy
def create_android_compat_symlink(abi):
    dragon.relative_symlink(os.path.join(dragon.OUT_DIR, abi),
            os.path.join(dragon.OUT_DIR, "..", "Android-%s" % abi))

def create_ios_compat_symlink():
    dragon.relative_symlink(os.path.join(dragon.OUT_DIR),
            os.path.join(dragon.OUT_DIR, "..", "iOS-iphoneos"))

def create_ios_sim_compat_symlink():
    dragon.relative_symlink(os.path.join(dragon.OUT_DIR),
            os.path.join(dragon.OUT_DIR, "..", "iOS-iphonesimulator"))

def create_native_compat_symlink():
    dragon.relative_symlink(os.path.join(dragon.OUT_DIR),
            os.path.join(dragon.OUT_DIR, "..", "Unix-base"))

#===============================================================================
#===============================================================================
def setup_android_abi(task, abi):
    task.extra_env["ANDROID_ABI"]=abi

# Register a task to build android sdk for a specific abi/arch
def add_android_abi(abi):
    dragon.add_meta_task(
        name = "build-sdk-%s" % abi,
        desc = "Build android sdk for %s" % abi,
        subtasks = ["alchemy all sdk"],
        prehook = lambda task, args: setup_android_abi(task, abi),
        posthook = lambda task, args: create_android_compat_symlink(abi),
        weak = True,
        outsubdir = abi
    )

#===============================================================================
#===============================================================================
if dragon.VARIANT == "android":
    # Register all abi/arch
    add_android_abi("armeabi")
    add_android_abi("armeabi_v7a")
    add_android_abi("mips")
    add_android_abi("x86")

    # Meta-task to build all sdk abi/arch
    dragon.add_meta_task(
        name="build-sdk",
        desc="Build android sdk for all architectures",
        subtasks=[
            "build-sdk-armeabi",
            "build-sdk-armeabi_v7a",
            "build-sdk-mips",
            "build-sdk-x86",
        ],
        weak=True
)

#===============================================================================
#===============================================================================
if dragon.VARIANT == "ios":
    dragon.add_meta_task(
        name = "build-sdk",
        desc = "Build ios sdk",
        subtasks = ["alchemy all sdk"],
        posthook = lambda task, args: create_ios_compat_symlink(),
        weak = True,
    )

#===============================================================================
#===============================================================================
if dragon.VARIANT == "ios_sim":
    dragon.add_meta_task(
        name = "build-sdk",
        desc = "Build ios simulattor sdk",
        subtasks = ["alchemy all sdk"],
        posthook = lambda task, args: create_ios_sim_compat_symlink(),
        weak = True,
    )

if dragon.VARIANT == "native":
    dragon.add_meta_task(
        name = "build-sdk",
        desc = "Build native sdk",
        subtasks = ["alchemy all"],
        posthook = lambda task, args: create_native_compat_symlink(),
        weak = True,
    )

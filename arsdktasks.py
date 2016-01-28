
import os
import dragon

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

def setup_android_abi(task, abi):
    task.extra_env["ANDROID_ABI"]=abi

# Register a task to build android sdk for a specific abi/arch
def add_android_abi(abi):
    dragon.add_alchemy_task(
        name = "build-sdk-%s" % abi,
        desc = "Build android sdk for %s" % abi,
        product = dragon.PRODUCT,
        variant = dragon.VARIANT,
        defargs = ["all"],
        prehook = lambda task, args: setup_android_abi(task, abi),
        posthook = lambda task, args: create_android_compat_symlink(abi),
        weak = True,
        outsubdir = abi
    )

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

if dragon.VARIANT == "ios":
    dragon.add_alchemy_task(
        name = "build-sdk",
        desc = "Build ios sdk",
        product = dragon.PRODUCT,
        variant = dragon.VARIANT,
        defargs = ["all"],
        posthook = lambda task, args: create_ios_compat_symlink(),
        weak = True,
    )

if dragon.VARIANT == "ios_sim":
    dragon.add_alchemy_task(
        name = "build-sdk",
        desc = "Build ios simulattor sdk",
        product = dragon.PRODUCT,
        variant = dragon.VARIANT,
        defargs = ["all"],
        posthook = lambda task, args: create_ios_sim_compat_symlink(),
        weak = True,
    )

if dragon.VARIANT == "native":
    dragon.add_alchemy_task(
        name = "build-sdk",
        desc = "Build native sdk",
        product = dragon.PRODUCT,
        variant = dragon.VARIANT,
        defargs = ["all"],
        posthook = lambda task, args: create_native_compat_symlink(),
        weak = True,
    )

def build_android_jni(dirpath, args):
    dragon.exec_dir_cmd(dirpath=dirpath, cmd="${ANDROID_NDK_PATH}/ndk-build")

def build_android_app(dirpath, args, release=False):
    arbuildutils_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARBuildUtils")

    # Build application
    dragon.exec_dir_cmd(dirpath=arbuildutils_dir, cmd="./generateAndroidResources.sh")
    dragon.exec_dir_cmd(dirpath=arbuildutils_dir, cmd="./generateLocalPropertiesFile.py")
    dragon.exec_dir_cmd(dirpath=os.path.join(dirpath, "script"), cmd="./generateCompatiblesDevices.py")
    if release:
        dragon.exec_dir_cmd(dirpath=dirpath, cmd="./gradlew assembleRelease")
    else:
        dragon.exec_dir_cmd(dirpath=dirpath, cmd="./gradlew assembleDebug")

def build_ios_app(dirpath, project, args, release=False):
    # Build application
    cmd = "xcodebuild "
    cmd += "-project %s " % project
    if release:
        cmd += "-configuration Release "
    else:
        cmd += "-configuration Debug "

    if args:
        cmd += " ".join(args)
    dragon.exec_dir_cmd(dirpath=dirpath, cmd=cmd)


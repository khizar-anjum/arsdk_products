#===============================================================================
# iOS tasks.
#===============================================================================

import dragon
import os

def build_app():
    arfreeflight_ios_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "iOS", "ARFreeFlight")

    # Build application
    dragon.exec_dir_cmd(dirpath=arfreeflight_ios_dir, cmd="xcodebuild -project ARFreeFlight.xcodeproj")

def pre_hook_variant_forall_task(tasklist, tasksargs):
    dragon.LOGI("pre_hook_variant_forall_task")

def post_hook_variant_forall_task(tasklist, tasksargs):
    dragon.LOGI("post_hook_variant_forall_task")
    # dragon.LOGI(pprint.pformat(tasklist))
    # dragon.LOGI(pprint.pformat(tasksargs))
    gen_app = False
    args_app = None

    if "build-app" in tasklist:
        gen_app = True
        args_app = tasksargs[tasklist.index("build-app")]

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
    name = "build-app",
    desc = "Build SDK & generate application",
    subtasks = ["build-sdk"],
)

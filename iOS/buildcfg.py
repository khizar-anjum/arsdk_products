#===============================================================================
# iOS tasks.
#===============================================================================

import dragon
import os

def hook_post_buildapp(task, args):
    arfreeflight_ios_dir = os.path.join(dragon.WORKSPACE_DIR, "packages", "ARFreeFlight", "iOS", "ARFreeFlight")

    # Build application
    dragon.exec_dir_cmd(dirpath=arfreeflight_ios_dir, cmd="xcodebuild -project ARFreeFlight.xcodeproj")

#===============================================================================
# Tasks
#===============================================================================

dragon.add_meta_task(
    name = "buildapp",
    desc = "Build SDK & generate application",
    subtasks = ["build"],
    posthook = hook_post_buildapp
)

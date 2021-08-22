import tools_kit
import qemu_base_tools
import constant

import subprocess


def list_platform_aarch64():
    cmd = ["qemu-system-aarch64", "-machine", "?"]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_platfome = str(output.stdout.decode("utf-8"))
    platform_list = all_platfome.split("\n")
    platform_list.pop(0)
    return platform_list


def list_platform_arm():
    cmd = ["qemu-system-arm", "-machine", "?"]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_platfome = str(output.stdout.decode("utf-8"))
    platform_list = all_platfome.split("\n")
    platform_list.pop(0)
    return platform_list


def add_platform_to_cmd(cmd, platform):
    return cmd + " -machine " + platform


def aarch64_specific(cmd):
    machine = tools_kit.choose_list(
        list_platform_aarch64(), "Choose machine type: ", constant.default_machine_id_aarch64)
    machine = qemu_base_tools.get_base_params(machine)
    cmd = add_platform_to_cmd(cmd, machine)
    return cmd


def arm_specific(cmd):
    machine = tools_kit.choose_list(
        list_platform_arm(), "Choose machine type: ", constant.default_machine_id_arm)
    machine = qemu_base_tools.get_base_params(machine)
    cmd = add_platform_to_cmd(cmd, machine)
    return cmd

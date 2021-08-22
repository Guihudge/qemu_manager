import tools_kit
import qemu_base_tools
import constant

import subprocess


def list_platform_amd64():
    cmd = ["qemu-system-x86_64", "-cpu", "?"]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_platfome = str(output.stdout.decode("utf-8"))
    all_platform = all_platfome.split("\n")
    platform_list = []
    for element in all_platform:
        if element[0:3] == "x86":
            platform_list.append(element)

    platform_list_formated = []
    for element in platform_list:
        split_element = element.split(" ", 1)
        platform_list_formated.append(split_element[1])

    return platform_list_formated


def list_platform_i386():
    cmd = ["qemu-system-i386", "-cpu", "?"]
    output = subprocess.run(cmd, stdout=subprocess.PIPE)
    all_platfome = str(output.stdout.decode("utf-8"))
    all_platform = all_platfome.split("\n")
    platform_list = []
    for element in all_platform:
        if element[0:3] == "x86":
            platform_list.append(element)

    platform_list_formated = []
    for element in platform_list:
        split_element = element.split(" ", 1)
        platform_list_formated.append(split_element[1])

    return platform_list_formated


def add_cpu_to_cmd(cmd, cpu):
    return cmd + " -cpu " + cpu


def amd64_specific(cmd):
    cpu = tools_kit.choose_list(
        list_platform_amd64(), "Choose cpu type: ", constant.default_cpu_id_amd64)
    cpu = qemu_base_tools.get_base_params(cpu)
    cmd = add_cpu_to_cmd(cmd, cpu)
    return cmd


def i386_specific(cmd):
    cpu = tools_kit.choose_list(
        list_platform_i386(), "Choose cpu type: ", constant.default_cpu_id_i386)
    cpu = qemu_base_tools.get_base_params(cpu)
    cmd = add_cpu_to_cmd(cmd, cpu)
    return cmd

import qemu_base_tools
import qemu_arm_tools
import qemu_x86_tools
import qemu_disk_tools
import json_load

import tools_kit

import constant
import time


def check_cmd(cmd):
    print("cmd: ", cmd)
    rep = input("Command correct? [y/n] : ")
    if rep == "y" or rep == "Y":
        return True
    else:
        return False


def check_default(ram, cpucore):
    if ram == "":
        ram = constant.default_ram
    if cpucore == "":
        cpucore = constant.default_cpu_core
    return ram, cpucore


def general_boot_setup():
    host_arch = qemu_base_tools.get_host_type()

    arch = tools_kit.choose_list(qemu_base_tools.list_arch(
        constant.qemu_path), "Choose architecture: ", constant.default_arch_id)

    ram = tools_kit.choose_number(
        "amount of ram with suffix (ex: 8G for 8Go, 8M for 8Mo): ")

    cpuCore = tools_kit.choose_number("Number of cpu core(s): ")

    ram, cpuCore = check_default(ram, cpuCore)

    cmd = qemu_base_tools.make_base_cmd(constant.qemu_base, arch, constant.qemu_allocate_ram,
                                        ram, constant.qemu_allocate_cpu_core, cpuCore)

    cmd = qemu_base_tools.kvm_enable(cmd, host_arch, arch)

    time.sleep(1)
    return cmd, arch


def boot_vm(cmd):
    if tools_kit.check_yn("Command correct? [y/n] : ", ("cmd: " + cmd)):
        qemu_base_tools.launch(cmd)


def boot_vm_manualy():

    cmd, arch = general_boot_setup()

    # aarch64
    if arch == "aarch64":
        cmd = qemu_arm_tools.aarch64_specific(cmd)

    # arm (32bit)
    elif arch == "arm":
        cmd = qemu_arm_tools.arm_specific(cmd)

    # amd64
    elif arch == "x86_64":
        cmd = qemu_x86_tools.amd64_specific(cmd)

    # i386
    elif arch == "i386":
        cmd = qemu_x86_tools.i386_specific(cmd)

    cmd = qemu_disk_tools.iso_setup(cmd)

    cmd = qemu_disk_tools.disk_setup(cmd)

    cmd = qemu_base_tools.enable_vnc(cmd)

    boot_vm(cmd)


def disk_util():  # TODO: rewirte this function (disk_util)
    quit = False
    while not quit:
        print("choose action:\n1: create disk\n2: info on disk\n3: resize disk\n4: quit disk util")
        rep = int(input("choose action: "))

        if rep == 1:
            name = input("disk name (without extension): ")
            format = tools_kit.choose_list(
                ["qcow2", "raw"], "choose format of disk: ")
            name = constant.default_disk_path + name + "." + format
            size = input("disk size with prefix (M for Mo, G for Go): ")
            qemu_disk_tools.create_disk(name, format, size)

        if rep == 2:
            name = tools_kit.choose_list(qemu_disk_tools.list_file(
                constant.default_disk_path + "*"), "Choose disk file: ")
            qemu_disk_tools.info_disk(name)

        if rep == 3:
            name = tools_kit.choose_list(qemu_disk_tools.list_file(
                constant.default_disk_path + "*"), "Choose disk file: ")
            size = input("New size of disk with prefix (M for Mo, G for Go): ")
            qemu_disk_tools.resize_disk(name, size)

        if rep == 4:
            quit = not quit


def boot_from_json():
    file = tools_kit.choose_list(qemu_disk_tools.list_file(
        constant.default_vm_path), "Choose VM save: ")
    cmd = json_load.gen_cmd_from_save(file)
    boot_vm(cmd)


def print_host_info():
    print("Host information: ")
    print("\tArch:", qemu_base_tools.get_host_type())
    print("\tnb cpu theard:", qemu_base_tools.get_nproc())
    print("\tMemory:", qemu_base_tools.get_total_host_mem(), "MB")
    print("\tfree disk space:", round(
        qemu_base_tools.get_free_disk_space_GB("./")), "GB")

    pass


def main_loop():  # TODO: rewirte this function (main_loop)
    run = True
    while run:
        print("choose action:\n1: boot vm manualy\n2: disk util\n3: Load VM from file\n4: Quit")
        rep = tools_kit.choose_number("choose action: ")
        if rep == 1:
            boot_vm_manualy()
        if rep == 2:
            disk_util()
        if rep == 3:
            boot_from_json()
        if rep == 4:
            print_host_info()
        if rep == 5:
            run = not run


main_loop()

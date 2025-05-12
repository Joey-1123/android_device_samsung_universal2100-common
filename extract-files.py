#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixup_vendorcompat,
    lib_fixups_user_type,
    libs_proto_3_9_1,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/universal2100-common',
    'hardware/samsung',
    'hardware/samsung_slsi-linaro/graphics',
]

def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

def lib_fixup_device_dep(lib: str, partition: str, *args, **kwargs):
    return f'//device/samsung/universal2100-common/shims/stub:{lib}'

lib_fixups: lib_fixups_user_type = {
    libs_proto_3_9_1: lib_fixup_vendorcompat,
    'libuuid': lib_fixup_vendor_suffix,
    'libvkmanager_vendor': lib_fixup_device_dep,
} # fmt: skip

blob_fixups: blob_fixups_user_type = {
    'vendor/bin/vaultkeeperd': blob_fixup()
        .binary_regex_replace(rb'ro\.factory\.factory_binary', b'ro.vendor.factory_binary\x00'),

    'vendor/lib64/libvkservice.so': blob_fixup()
        .binary_regex_replace(rb'ro\.factory\.factory_binary', b'ro.vendor.factory_binary\x00'),

    'vendor/lib64/libsec-ril.so': blob_fixup()
        .sig_replace('80 0E 40 F9 E1 03 16 AA 82 0C 80 52 E3 03 15 AA',
                     '80 0E 40 F9 E1 03 16 AA 82 0C 80 52 08 00 80 D2'),

    'vendor/lib64/libsensorlistener.so': blob_fixup()
        .add_needed('libshim_sensorndkbridge.so'),
    'vendor/lib/libsensorlistener.so': blob_fixup()
        .add_needed('libshim_sensorndkbridge.so'),

    (
        'vendor/lib64/libkeymaster_helper.so',
        'vendor/lib64/libskeymaster4device.so',
    ): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-tm.so')
        .add_needed('libshim_crypto.so'),

    (
        'vendor/lib/sensors.grip.so',
        'vendor/lib64/sensors.grip.so',
    ): blob_fixup()
        .add_needed('libutils-v32.so')
        .binary_regex_replace(b'_ZN7android6Thread3runEPKcim', b'_ZN7utils326Thread3runEPKcim'),

    'vendor/lib/libwvhidl.so': blob_fixup()
        .replace_needed('libprotobuf-cpp-lite-3.9.1.so', 'libprotobuf-cpp-full-3.9.1.so')
        .replace_needed('libcrypto.so', 'libcrypto-tm.so'),

    'vendor/lib64/libeden_ud_gpu.so': blob_fixup()
        .replace_needed('libOpenCL.so', 'libGLES_mali.so')
        .add_needed('libeden_ud_cpu.so'),
    'vendor/lib/libeden_ud_gpu.so': blob_fixup()
        .replace_needed('libOpenCL.so', 'libGLES_mali.so')
        .add_needed('libeden_ud_cpu.so'),

    'vendor/lib64/libnpuc_common.so': blob_fixup()
    .add_needed('liblog.so'),

    'vendor/lib64/libnpuc_backend.so': blob_fixup()
    .add_needed('liblog.so')
    .add_needed('libnpuc_cmdq.so'),

    'vendor/lib64/libnpuc_graph.so': blob_fixup()
    .add_needed('libnpuc_common.so'),

    'vendor/lib64/libnpuc_template.so': blob_fixup()
    .add_needed('liblog.so'),

    'vendor/lib64/libnpuc_frontend.so': blob_fixup()
    .add_needed('liblog.so'),

    'vendor/lib64/libnpuc_controller.so': blob_fixup()
    .add_needed('liblog.so'),
}# fmt: skip

module = ExtractUtilsModule(
    'universal2100-common',
    'samsung',
    namespace_imports=namespace_imports,
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

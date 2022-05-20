#!/usr/bin/env python3

import argparse
import json
import pathlib
import sys

from registry import integrity
from registry import json_dump
from registry import log
from registry import read

def get_source_root(module_name, version):
    cwd = pathlib.Path.cwd()
    source_path = cwd.joinpath("modules", module_name, version)
    return source_path

def get_source(module_name, version):
    source_path = get_source_root(module_name, version)
    source_path = source_path.joinpath("source.json")
    return json.load(source_path.open())

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument(
      "--module", type=str, help="Module name for which to regenerate the source.json file.")
    parser.add_argument(
      "--version", type=str, help="Module version for which to regenerate the source.json file.")

    args = parser.parse_args(argv)

    if args.module and args.version:
        source_root = get_source_root(args.module, args.version)
        source_path = source_root.joinpath("source.json")
        log(f"Regenerating source.json file for {source_path}")
        patch_dir = source_root.joinpath("patches")
        source = get_source(args.module, args.version)

        if source["patches"]:
            for s in source["patches"]:
                patch = patch_dir.joinpath(s)
                source["patches"][patch.name] = integrity(read(patch))

        json_dump(source_path, source)
        log(f"Successfully regenerated {source_path}")
    else:
        log("Must provide --module and --version arguments")

if __name__ == "__main__":
    sys.exit(main())

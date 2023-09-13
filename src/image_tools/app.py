import os
import argparse
from tabnanny import check
from image_tools.pypi import set_pypi

env_map = {
    "tf": "svtter/tensorflow",
    "torch": "svtter/pytorch",
}


def check_image(image_name):
    """check if docker image is available"""
    exit_code = os.system("docker images | grep {image_name}".format(image_name=image_name))
    if exit_code != 0:
        print("Image {image_name} not found".format(image_name=image_name))
        return False
    return True


def run_image(volume, image):
    """start container with image and volume"""
    if not check_image(image):
        return

    exit_code = os.system("docker run -it {image} -v {volume}:/app".format(image=image, volume=volume))
    if exit_code != 0:
        print("Error starting container")
        exit(1)


def main():
    """parse the --env and --folder variables and run the appropriate"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=str, default="tf")
    parser.add_argument("--folder", type=str, default=".")

    # add pypi argument to change pip.conf
    parser.add_argument("--pypi", type=str, default="thinghoo")

    args = parser.parse_args()

    # run the specialized image
    run_image(args.folder, env_map[args.env])
    set_pypi(args.pypi)

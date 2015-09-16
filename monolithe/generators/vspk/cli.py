#!/usr/bin/env python

import argparse
import getpass
import os
import sys


def main(argv=sys.argv):
    """

    """
    parser = argparse.ArgumentParser(description="VSP SDK Generator.")

    parser.add_argument('-g', "--github",
                        dest="api_url",
                        help="Github API URL",
                        type=str)

    parser.add_argument('-l', "--login",
                        dest="login",
                        help="Github login to connect with",
                        type=str)

    parser.add_argument('-t', "--token",
                        dest="token",
                        help="Github Token to connect with",
                        type=str)

    parser.add_argument('-o', "--organization",
                        dest="organization",
                        help="Github organization name",
                        type=str)

    parser.add_argument('-r', "--r",
                        dest="repository",
                        help="Github repository name",
                        type=str)

    parser.add_argument('-v', "--versions",
                        dest="apiversions",
                        help="versions of the SDK to generate (examples: master 3.0 3.1)",
                        nargs="*",
                        type=str,
                        required=True)

    parser.add_argument('-d', "--destination",
                        dest='output_path',
                        help="directory where the generated sources will be placed",
                        type=str)

    parser.add_argument("--doc",
                        dest="generate_doc",
                        help="Flag to generate documentation of the VSPK",
                        action="store_true")

    parser.add_argument("--config",
                        dest="config_path",
                        help="Path the monolithe configuration file",
                        type=str)

    args = parser.parse_args()

    # Use environment variable if necessary
    if not args.api_url and "MONOLITHE_GITHUB_API_URL" in os.environ:
        args.api_url = os.environ["MONOLITHE_GITHUB_API_URL"]

    if not args.token and not args.login:

        if "MONOLITHE_GITHUB_TOKEN" in os.environ:
            args.token = os.environ["MONOLITHE_GITHUB_TOKEN"]

        elif "MONOLITHE_GITHUB_LOGIN" in os.environ:
            args.login = os.environ["MONOLITHE_GITHUB_LOGIN"]

    if not args.organization and "MONOLITHE_GITHUB_ORGANIZATION" in os.environ:
        args.organization = os.environ["MONOLITHE_GITHUB_ORGANIZATION"]

    if not args.repository and "MONOLITHE_GITHUB_REPOSITORY" in os.environ:
        args.repository = os.environ["MONOLITHE_GITHUB_REPOSITORY"]

    if not args.config_path and "MONOLITHE_CONFIG_PATH" in os.environ:
        args.config_path = os.environ["MONOLITHE_CONFIG_PATH"]

    # Additional validation
    if not args.api_url:
        args.api_url = raw_input('Enter your Github API URL: ')

    if not args.login and not args.token :
        args.login = raw_input('Enter your Github login: ')

    if not args.organization:
        args.organization = raw_input('Enter your Github organization: ')

    if not args.repository:
        args.repository = raw_input('Enter your Github repository: ')

    if not args.config_path:
        args.config_path = raw_input('Enter the path of the monolithe config file: ')

    # Ask for password
    if args.login:
        password = getpass.getpass(prompt='Enter your Github password for %s: ' % args.login)
        login_or_token = args.login
    else:
        password = None
        login_or_token = args.token

    from monolithe import MonolitheConfig
    from monolithe.generators import SDKGenerator, VSPKDocumentationGenerator

    MonolitheConfig.set_config_path(args.config_path)

    # Generate VSDK
    generator = SDKGenerator( sdk_name=MonolitheConfig.get_config("sdk_name"),
                              codegen_directory=MonolitheConfig.get_config("codegen_directory"),
                              sdk_vanilla_path=MonolitheConfig.get_config("sdk_vanilla_path"),
                              sdk_api_output_path=MonolitheConfig.get_config("sdk_api_output_path"),
                              apiversions=args.apiversions)

    generator.run(  api_url=args.api_url,
                    login_or_token=login_or_token,
                    password=password,
                    organization=args.organization,
                    repository=args.repository)

    # Generate VSPK and VSDK documentation
    if args.generate_doc:
        doc_generator = VSPKDocumentationGenerator()
        doc_generator.run()


if __name__ == '__main__':
    main()

import argparse
import re
from instance import Instance, Instances, MySQLInstanceGroup


def format_instance(host_info):
    pattern = re.compile(r'^(.*?):?(\d+)?$')
    if not pattern.match(host_info):
        raise ValueError(f'Invalid host:port: {host_info}')

    match_instance = re.match(pattern, host_info)
    host = match_instance.group(1)
    port = match_instance.group(2) if match_instance.group(2) else 3306

    return Instance(host=host, port=port)


def format_instances(host_info):
    instances = host_info.split(',')
    return Instances(instances=[format_instance(instance) for instance in instances])


def main():
    parser = argparse.ArgumentParser()
    group_unused_index = parser.add_argument_group('unused_index')
    group_unused_index.add_argument('--auto-check', type=bool, default=False,
                                    help='provide just one host and port to get all nodes in the group')

    group_unused_index.add_argument('--mysql', type=str, default='localhost', required=True,
                                    help='host1:port1[,host2:port2] ...')

    group_unused_index.add_argument('--user', type=str, required=True)
    group_unused_index.add_argument('--password', type=str, required=True)
    group_unused_index.add_argument('--output', type=str, help='execl file name')

    args = parser.parse_args()

    # TODO: auto-check
    if args.auto_check:
        pass

    mig = MySQLInstanceGroup(format_instances(args.mysql), user=args.user, password=args.password)

    if args.output:
        mig.get_common_unused_indexes().to_excel(args.output, index=False)
    else:
        print('Unused indexes:')
        print(mig.get_common_unused_indexes())


if __name__ == '__main__':
    main()

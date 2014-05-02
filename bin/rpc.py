#! /usr/bin/python

#########################################
#
#    Request Project Create
#
#########################################

import argparse
from amie.accounting import process_rpc

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet_rec_id",
        required=False,
        default=None,
        help="process single packet with the given receive id")
    parser.add_argument("--verbose",
        action='store_true',
        default=False,
        help="print out the processing detail")
    parser.add_argument("--checkpt",
        action='store_true',
        default=False,
        help="enable check point")
    args = parser.parse_args()
    
    process_rpc(args.packet_rec_id, args.verbose, args.checkpt)
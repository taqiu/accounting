#! /usr/bin/python

#########################################
#
#    Request Account Create
#
#########################################

import argparse
from amie.accounting import process_rac

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
    args = parser.parse_args()
    
    process_rac(args.packet_rec_id, args.verbose)
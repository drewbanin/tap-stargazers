#!/usr/bin/env python3

import argparse
import requests
import singer
import logging
import base64
import datetime
import time
import json
import backoff
import hashlib

import tap_github_stars.schemas as schemas

logger = singer.get_logger()

BASE_URL = "https://api.github.com/repos/{repo}/stargazers?page={page_number}&access_token={access_token}"
FIELDS = ["user_id", "username", "num_followers", "num_following", "num_repos","created_at","star_time"]

def validate_config(config):
    required_keys = ['repo', 'access_token']
    missing_keys = []
    null_keys = []
    has_errors = False

    for required_key in required_keys:
        if required_key not in config:
            missing_keys.append(required_key)

        elif config.get(required_key) is None:
            null_keys.append(required_key)

    if len(missing_keys) > 0:
        logger.fatal("Config is missing keys: {}"
                     .format(", ".join(missing_keys)))
        has_errors = True

    if len(null_keys) > 0:
        logger.fatal("Config has null keys: {}"
                     .format(", ".join(null_keys)))
        has_errors = True

    if has_errors:
        raise RuntimeError


def load_config(filename):
    config = {}

    try:
        with open(filename) as f:
            config = json.load(f)
    except Exception as e:
        logger.fatal("Failed to decode config file. Is it valid json?")
        logger.fatal(e)
        raise RuntimeError

    validate_config(config)

    return config


def load_state(filename):
    if filename is None:
        return {}

    try:
        with open(filename) as f:
            return json.load(f)
    except:
        logger.fatal("Failed to decode state file. Is it valid json?")
        raise RuntimeError


def fetch_stars(config, page_number):

    data = {
        "repo" : config['repo'],
        "access_token" : config['access_token'],
        "page_number" : page_number
    }

    query_url = BASE_URL.format(**data)
    headers = {'Accept': 'application/vnd.github.v3.star+json'}
    req = requests.get(query_url, headers=headers)
    resp = req.json()

    # pluck user id out and store in top-level
    for record in resp:
        record['user_id'] = record['user']['id']

    return resp


def do_sync(args):
    logger.info("Starting sync.")

    config = load_config(args.config)
    state = load_state(args.state)

    all_records = []
    page_number = 1
    new_records = fetch_stars(config, page_number)
    while len(new_records) > 0:
        logger.info("pulled {} records on page {}".format(len(new_records), page_number))
        all_records.extend(new_records)
        page_number += 1

        new_records = fetch_stars(config, page_number)

    singer.write_schema('stargazers', schemas.star, ['user_id'])
    singer.write_records('stargazers', all_records)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-c', '--config', help='Config file', required=True)
    parser.add_argument(
        '-s', '--state', help='State file')

    args = parser.parse_args()

    try:
        do_sync(args)
    except RuntimeError:
        logger.fatal("Run failed.")
        exit(1)


if __name__ == '__main__':
    main()

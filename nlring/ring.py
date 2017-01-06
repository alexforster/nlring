# -*- coding: UTF-8 -*-
#
# Copyright © 2017 Alex Forster. All rights reserved.
# This software is licensed under the 3-Clause ("New") BSD license.
# See the LICENSE file for details.
#

import sys
import os
import logging
import json

from datetime import datetime, timedelta
from exceptions import Exception
from types import TracebackType

import requests

from inparallel import task, waitfor


class RingNode(object):

    def __init__(self, api_dict=None):
        """ :type api_dict: dict
        """
        assert isinstance(api_dict, dict) and not len(api_dict) == 0

        self.id = int(api_dict['id'])  # type: int
        self.hostname = str(api_dict['hostname'])  # type: str
        self.asn = int(api_dict['asn'])  # type: int
        self.ipv4 = str(api_dict['ipv4'])  # type: str
        self.ipv6 = str(api_dict['ipv6'])  # type: str
        self.country = str(api_dict['countrycode'])  # type: str

    def __str__(self):

        return self.hostname

    def __repr__(self):

        return '<RingNode ' + self.hostname + '>'

    def __hash__(self):

        return hash(self.id)

    def __eq__(self, other):

        return self.id == other.id

    def __ne__(self, other):

        return not (self == other)


class Ring(object):

    def __init__(self, parallelism=32):

        assert isinstance(parallelism, int)

        self._parallelism = parallelism

        self._nodes = []

    @property
    def nodes(self):
        """ :rtype: list[RingNode]
        """
        return self._nodes

    def __iter__(self):

        return iter(self._nodes)

    def discover(self, cache_file=None):
        """ :type cache_file: str
        """
        assert isinstance(cache_file, str) or cache_file is None

        def load_from_api():

            response = requests.get('https://ring.nlnog.net/api/1.0/nodes/active', timeout=(2, 3))

            if response.status_code != 200:
                return None

            response = json.loads(response.text)

            if 'info' in response and 'success' in response['info'] and response['info']['success'] == 1:
                return response

            return None

        def load_from_cache(cache_file):

            if not os.path.isfile(cache_file):
                return None

            try:
                mtime = os.path.getmtime(cache_file)
            except OSError:
                mtime = 0

            last_modified_date = datetime.fromtimestamp(mtime)

            if datetime.now() > (last_modified_date + timedelta(hours=6)):

                try:
                    os.remove(cache_file)
                except OSError:
                    pass

                return None

            with open(cache_file) as fd:
                response = json.loads(fd.read())

            if 'info' in response and 'success' in response['info'] and response['info']['success'] == 1:
                return response

            return None

        def store_to_cache(cache_file, api_response):

            with open(cache_file, 'w+') as fd:
                fd.write(json.dumps(api_response))

        api_response = None

        if cache_file is not None:

            cache_file = os.path.abspath(os.path.expandvars(os.path.expanduser(cache_file)))

            api_response = load_from_cache(cache_file)

        if api_response is None:
            api_response = load_from_api()

        if api_response is None:
            return

        if cache_file is not None:
            store_to_cache(cache_file, api_response)

        nodes = api_response['results']['nodes']

        for node in nodes:
            self._nodes.append(RingNode(node))

    def run(self, fn, args=[], kwargs={}, on_success=None, on_error=None):
        """ :type fn: (RingNode, list, dict)->Any
            :type args: list
            :type kwargs: dict
            :type on_success: (RingNode, Any)->None
            :type on_error: (RingNode, Exception, TracebackType)->None
            :rtype: dict[RingNode, Any]
        """
        assert callable(fn)
        assert isinstance(args, list)
        assert isinstance(kwargs, dict)
        assert callable(on_success) or on_success is None
        assert callable(on_error) or on_error is None

        @task
        def runner(fn, node, args, kwargs):

            return fn(node, *args, **kwargs)

        scheduled = list(self.nodes)
        inflight = []
        results = {}

        for future in waitfor(inflight, self._parallelism):

            if future is None and len(scheduled) > 0:

                node = scheduled.pop(0)
                future = runner(fn, node, args, kwargs)
                setattr(future, '_node', node)
                inflight.append(future)

            elif future is not None and future.exception():

                node = getattr(future, '_node')
                results[node] = future.exception_info()
                if on_error is not None:
                    on_error(node, *results[node])

            elif future is not None:

                node = getattr(future, '_node')
                results[node] = future.result()
                if on_success is not None:
                    on_success(node, results[node])

        return results

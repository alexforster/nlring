nlring
=====

**NLNOG Ring task execution library**

:Author:
    Alex Forster (alex@alexforster.com)
:License:
    BSD 3-Clause

**Installation**

``pip install nlring``

| **GitHub:** https://github.com/alexforster/nlring/tree/v1.0.1
| **PyPI:** https://pypi.python.org/pypi/nlring/1.0.1


Example Code
------------

.. code-block:: python
    
    from nlring import SSH, RingNode, Ring
    
    
    def do_tcp_traceroute(node, address, countries):
    
        countries = [c.lower() for c in countries]
    
        if node.country.lower() not in countries:
    
            return None
    
        with SSH(username='example', host=node.hostname) as ssh:
    
            ssh.authenticate()
    
            ssh.write('traceroute.db -4 -T -N 30 -n -w 2 -q 10 -z 0.1 {}'.format(address))
            traceroute = ssh.read(timeout=90)
    
            return traceroute
    
    def success(node, result):
    
        if result is not None:
    
            print('{}\n{}\n'.format(node.hostname, result))
    
    def error(node, ex, tb):
    
        import traceback
        print('{}\n{}'.format(node.hostname, ''.join(traceback.format_exception(type(ex), ex, tb))))
    
    
    ring = Ring(parallelism=32)
    
    ring.discover(cache_file='./api-nodes.json')
    
    ring.run(do_tcp_traceroute,
             args=['google.com', ['cn', 'kr', 'th', 'kh', 'au', 'jp']],
             on_success=success,
             on_error=error)
    
    
    # sabay01.ring.nlnog.net
    # traceroute to google.com (175.28.1.177), 30 hops max, 60 byte packets
    #  1  118.67.200.189  0.369 ms  0.343 ms  0.307 ms  0.324 ms  0.291 ms  0.299 ms  0.353 ms  0.360 ms  0.334 ms  0.379 ms
    #  2  175.28.2.33  1.117 ms  1.108 ms  0.999 ms  1.230 ms  1.185 ms  1.147 ms  1.066 ms  1.281 ms  1.175 ms  1.185 ms
    #  3  175.28.1.177  0.461 ms  0.459 ms  0.516 ms  0.488 ms  0.565 ms  0.537 ms  0.516 ms  0.470 ms  0.431 ms  0.499 ms
    #
    # apnic01.ring.nlnog.net
    # traceroute to google.com (216.58.220.142), 30 hops max, 60 byte packets
    #  1  203.133.248.254  0.175 ms  0.159 ms  0.186 ms  0.162 ms  0.171 ms  0.159 ms  0.163 ms  0.293 ms  0.185 ms  0.158 ms
    #  2  45.127.172.73  17.411 ms  17.343 ms  17.334 ms  17.328 ms  17.366 ms  17.404 ms  17.345 ms  17.373 ms  17.330 ms  17.383 ms
    #  3  216.239.40.233  17.741 ms 216.239.40.223  17.732 ms 216.239.40.233  17.742 ms 216.239.40.223  17.899 ms  17.776 ms 216.239.40.233  17.689 ms 216.239.40.223  17.726 ms 216.239.40.233  17.725 ms  17.742 ms 216.239.40.223  17.713 ms
    #  4  108.170.232.179  17.800 ms  17.766 ms  17.760 ms 108.170.232.177  17.739 ms 108.170.232.179  17.790 ms 108.170.232.177  17.782 ms  17.747 ms  17.770 ms 108.170.232.179  17.746 ms  17.767 ms
    #  5  216.58.220.142  17.848 ms  17.942 ms  17.933 ms  17.992 ms  17.704 ms  18.588 ms  18.001 ms  17.957 ms  17.855 ms  18.179 ms
    #
    # ...

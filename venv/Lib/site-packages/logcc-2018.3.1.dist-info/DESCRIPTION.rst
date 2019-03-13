=============================
logcc
=============================

simple & beautiful log setup library

**Note**: this package is still in alpha. Use with caution !


Quickstart
----------

Install logcc::

    pip install logcc


Use logcc:

.. code-block:: python

    l = LogCC(name='test)
    l.update_color_formatter('name', 'DEBUG', red())
    l.update_color_formatter('name', 'INFO', cc(':blue::man::red::woman:'))
    log = logging.getLogger(name)
    log.debug('你好，世界')
    log.info('hello world')




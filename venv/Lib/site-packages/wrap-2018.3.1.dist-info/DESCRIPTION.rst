=============================
wrap
=============================

useful wrap collections

**Note**: this package is still in alpha. Use with caution !


Quickstart
----------

Install wrap::

    pip install wrap


Use logcc:

.. code-block:: python

    @show(level ='DEBUG')
    @safe(Exception)
    def test(text):
        print(text)
        raise Exception('test')


    if __name__ == '__main__':
        logging.basicConfig(level=logging.INFO)
        log = logging.getLogger()
        ret = test('hello world')
        print(ret, type(ret))




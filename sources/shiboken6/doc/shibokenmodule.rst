.. module:: Shiboken

.. |maya| unicode:: Maya U+2122

.. _shiboken-module:

Shiboken module
***************

Functions
^^^^^^^^^

.. container:: function_list

    *    def :meth:`isValid<shiboken.isValid>` (obj)
    *    def :meth:`wrapInstance<shiboken.wrapInstance>` (address, type)
    *    def :meth:`getCppPointer<shiboken.getCppPointer>` (obj)
    *    def :meth:`delete<shiboken.delete>` (obj)
    *    def :meth:`isOwnedByPython<shiboken.isOwnedByPython>` (obj)
    *    def :meth:`wasCreatedByPython<shiboken.wasCreatedByPython>` (obj)
    *    def :meth:`dump<shiboken.dump>` (obj)
    *    def :meth:`disassembleFrame<shiboken.disassembleFrame>` (marker)

Detailed description
^^^^^^^^^^^^^^^^^^^^

This Python module can be used to access internal information related to our
binding technology. Access to this internal information is required to e.g.:
integrate PySide with Qt based programs that offer Python scripting like |maya|
or just for debug purposes.

Some function description refer to "Shiboken based objects", wich means
Python objects instances of any Python Type created using Shiboken.

To import the module:

.. code-block:: python

    from shiboken6 import Shiboken

.. function:: isValid(obj)

    Given a Python object, returns True if the object methods can be called
    without an exception being thrown. A Python wrapper becomes invalid when
    the underlying C++ object is destroyed or unreachable.

.. function:: wrapInstance(address, type)

    Creates a Python wrapper for a C++ object instantiated at a given memory
    address - the returned object type will be the same given by the user.

    The type must be a Shiboken type, the C++ object will not be
    destroyed when the returned Python object reach zero references.

    If the address is invalid or doesn't point to a C++ object of given type
    the behavior is undefined.

.. function:: getCppPointer(obj)

    Returns a tuple of longs that contain the memory addresses of the
    C++ instances wrapped by the given object.

.. function:: delete(obj)

    Deletes the C++ object wrapped by the given Python object.

.. function:: isOwnedByPython(obj)

    Given a Python object, returns True if Python is responsible for deleting
    the underlying C++ object, False otherwise.

    If the object was not a Shiboken based object, a TypeError is
    thrown.

.. function:: wasCreatedByPython(obj)

    Returns true if the given Python object was created by Python.

.. function:: dump(obj)

    Returns a string with implementation-defined information about the
    object.
    This method should be used **only** for debug purposes by developers
    creating their own bindings as no guarantee is provided that
    the string format will be the same across different versions.

    If the object is not a Shiboken based object, a message is printed.

.. function:: disassembleFrame(label)

    Prints the current executing Python frame to stdout and flushes.
    The disassembly is decorated by some label. Example:

    .. code-block:: python

        lambda: 42

    is shown from inside C++ as

    .. code-block:: c

        <label> BEGIN
          1           0 LOAD_CONST               1 (42)
                      2 RETURN_VALUE
        <label> END

    When you want to set a breakpoint at the `disassembleFrame` function
    and you use it from C++, you use the pure function name.

    When you want to use it from Python, you can insert it into your Python
    code and then maybe instead set a breakpoint at `SbkShibokenModule_disassembleFrame`
    which is the generated wrapper.

    `label` is a simple string in C++. In Python, you can use any object;
    internally the `str` function is called with it.

    This method should be used **only** for debug purposes by developers.

 .. function:: dumpTypeGraph(file_name)

    Dumps the inheritance graph of the types existing in libshiboken
    to ``.dot`` file for use with `Graphviz <https://graphviz.org/>`_.

.. function:: dumpWrapperMap()

    Dumps the map of wrappers existing in libshiboken to standard error.

 .. py:class:: VoidPtr(address, size = -1, writeable = 0)

     :param address: (PyBuffer, SbkObject, int, VoidPtr)
     :param size: int
     :param writeable: int

     Represents a chunk of memory by address and size and implements the ``buffer`` protocol.
     It can be constructed from a ``buffer``, a Shiboken based object, a memory address
     or another VoidPtr instance.

     .. py:method:: toBytes()

         :rtype: bytes

         Returns the contents as ``bytes``.

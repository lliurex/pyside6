#!/usr/bin/env python
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

"""Tests covering signal emission and receiving to python slots"""

import functools
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QObject, Signal, SIGNAL, QProcess, QTimeLine

from helper.usesqapplication import UsesQApplication


class ArgsOnEmptySignal(UsesQApplication):
    '''Trying to emit a signal without arguments passing some arguments'''

    def testArgsToNoArgsSignal(self):
        '''Passing arguments to a signal without arguments'''
        process = QProcess()
        self.assertRaises(TypeError, process.started.emit, 42)


class MoreArgsOnEmit(UsesQApplication):
    '''Trying to pass more args than needed to emit (signals with args)'''

    def testMoreArgs(self):
        '''Passing more arguments than needed'''
        process = QProcess()
        self.assertRaises(TypeError, process.finished.emit, 55, QProcess.ExitStatus.NormalExit, 42)


class Sender(QObject):
    '''Sender class'''

    dummy = Signal()
    dummy_int = Signal(int)


class PythonSignalToCppSlots(UsesQApplication):
    '''Connect python signals to C++ slots'''

    def testWithoutArgs(self):
        '''Connect python signal to QTimeLine.toggleDirection()'''
        timeline = QTimeLine()
        sender = Sender()
        sender.dummy.connect(timeline.toggleDirection)

        orig_dir = timeline.direction()
        sender.dummy.emit()
        new_dir = timeline.direction()

        if orig_dir == QTimeLine.Forward:
            self.assertEqual(new_dir, QTimeLine.Backward)
        else:
            self.assertEqual(new_dir, QTimeLine.Forward)

    def testWithArgs(self):
        '''Connect python signals to QTimeLine.setCurrentTime(int)'''
        timeline = QTimeLine()
        sender = Sender()

        sender.dummy_int.connect(timeline.setCurrentTime)

        current = timeline.currentTime()
        sender.dummy_int.emit(current + 42)
        self.assertEqual(timeline.currentTime(), current + 42)


class CppSignalsToCppSlots(UsesQApplication):
    '''Connection between C++ slots and signals'''

    def testWithoutArgs(self):
        '''Connect QProcess.started() to QTimeLine.togglePaused()'''
        process = QProcess()
        timeline = QTimeLine()

        process.finished.connect(timeline.toggleDirection)

        orig_dir = timeline.direction()

        process.start(sys.executable, ['-c', '"print 42"'])
        self.assertTrue(process.waitForStarted())
        self.assertTrue(process.waitForFinished())

        new_dir = timeline.direction()

        if orig_dir == QTimeLine.Forward:
            self.assertEqual(new_dir, QTimeLine.Backward)
        else:
            self.assertEqual(new_dir, QTimeLine.Forward)


called = False


def someSlot(args=None):
    global called
    called = True


class DynamicSignalsToFuncPartial(UsesQApplication):

    def testIt(self):
        global called
        called = False
        o = Sender()
        o.dummy.connect(functools.partial(someSlot, "partial .."))
        o.dummy.emit()
        self.assertTrue(called)


class EmitUnknownType(UsesQApplication):
    def testIt(self):
        a = QObject()
        a.connect(SIGNAL('foobar(Dummy)'), lambda x: 42)  # Just connect with an unknown type
        self.assertRaises(TypeError, a.emit, SIGNAL('foobar(Dummy)'), 22)


class EmitEnum(UsesQApplication):
    """Test emission of enum arguments"""

    def slot(self, arg):
        self.arg = arg

    def testIt(self):
        self.arg = None
        p = QProcess()
        p.stateChanged.connect(self.slot)
        p.stateChanged.emit(QProcess.NotRunning)
        self.assertEqual(self.arg, QProcess.NotRunning)


if __name__ == '__main__':
    unittest.main()

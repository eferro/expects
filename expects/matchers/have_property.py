# -*- coding: utf-8 -*

from . import Matcher
from .. import _compat


class HaveProperty(Matcher):
    def _initialize(self, name, *args):
        self._name = name
        self._args = args

    def _match(self, subject):
        self._subject = subject

        if self._args:
            try:
                value = getattr(subject, self._name)
            except AttributeError:
                return False
            else:
                expected_value = self._args[0]

                if hasattr(expected_value, '_match'):
                    return expected_value._match(value)

                return value == expected_value

        return hasattr(subject, self._name)

    @property
    def _description(self):
        if not self._args:
            return 'have property {expected!r}'.format(expected=self._name)

        expected_value = self._args[0]
        if isinstance(expected_value, Matcher):
            message = 'have property {expected!r} with value {expected_value}'.format(
                expected=self._name, expected_value=expected_value._description)
        else:
            message = 'have property {expected!r} with value {expected_value!r}'.format(
                expected=self._name, expected_value=expected_value)

        if isinstance(self._subject, _compat.string_types):
            message += ' but is not a dict'

        return message
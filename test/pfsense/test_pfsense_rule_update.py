# Copyright: (c) 2018, Frederic Bor <frederic.bor@wanadoo.fr>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import unittest
from copy import copy

from units.modules.utils import set_module_args
from .test_pfsense_rule import TestPFSenseRuleModule, args_from_var


class TestPFSenseRuleCreateModule(TestPFSenseRuleModule):

    def do_rule_update_test(self, rule, failed=False, **kwargs):
        """ test updating field of an host alias """
        target = copy(rule)
        target.update(kwargs)
        set_module_args(args_from_var(target))
        self.execute_module(changed=True)
        if failed:
            self.assertFalse(self.load_xml_result())
        else:
            self.check_rule_elt(target)

    ############################
    # rule update tests
    #
    def test_rule_update_action(self):
        """ test updating action of a rule to block """
        rule = dict(name='test_rule', source='any', destination='any', interface='wan', action='block', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_disabled(self):
        """ test updating disabled of a rule to True """
        rule = dict(name='test_rule', source='any', destination='any', interface='wan', disabled='True', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_floating_direction(self):
        """ test updating direction of a rule to out """
        rule = dict(name='test_rule_floating', source='any', destination='any', interface='wan', floating='yes', direction='out', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_floating_yes(self):
        """ test updating floating of a rule to yes """
        rule = dict(name='test_rule', source='any', destination='any', interface='wan', floating='yes', direction='any', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_floating_no(self):
        """ test updating floating of a rule to no """
        rule = dict(name='test_rule_floating', source='any', destination='any', interface='wan', floating='no', direction='any', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_floating_default(self):
        """ test updating floating of a rule to default """
        rule = dict(name='test_rule_floating', source='any', destination='any', interface='wan', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_inet(self):
        """ test updating ippprotocol of a rule to ipv4 and ipv6 """
        rule = dict(name='test_rule', source='any', destination='any', interface='wan', ipprotocol='inet46', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_protocol_udp(self):
        """ test updating protocol of a rule to udp """
        rule = dict(name='test_rule', source='any', destination='any', interface='wan', protocol='udp')
        self.do_rule_update_test(rule)

    def test_rule_update_protocol_tcp_udp(self):
        """ test updating protocol of a rule to tcp/udp """
        rule = dict(name='test_rule', source='any', destination='any', interface='wan', protocol='tcp/udp')
        self.do_rule_update_test(rule)

    def test_rule_update_log_yes(self):
        """ test updating log of a rule to yes """
        rule = dict(name='test_rule', source='any', destination='any', interface='wan', log='yes', direction='any', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_log_no(self):
        """ test updating log of a rule to no """
        rule = dict(name='test_rule_2', source='any', destination='any', interface='wan', log='no', direction='any', protocol='tcp')
        self.do_rule_update_test(rule)

    def test_rule_update_log_default(self):
        """ test updating log of a rule to default """
        rule = dict(name='test_rule_2', source='any', destination='any', interface='wan', protocol='tcp')
        self.do_rule_update_test(rule)

    @unittest.expectedFailure
    def test_rule_update_before(self):
        """ test updating position of a rule to before another """
        rule = dict(name='test_rule_3', source='any', destination='any', interface='wan', protocol='tcp', before='test_rule')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 0)

    @unittest.expectedFailure
    def test_rule_update_before_bottom(self):
        """ test updating position of a rule to bottom """
        rule = dict(name='test_rule_3', source='any', destination='any', interface='wan', protocol='tcp', before='bottom')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 5)

    def test_rule_update_after(self):
        """ test updating position of a rule to after another """
        rule = dict(name='test_rule_3', source='any', destination='any', interface='wan', protocol='tcp', after='test_rule_3')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 4)

    @unittest.expectedFailure
    def test_rule_update_after_top(self):
        """ test updating position of a rule to top """
        rule = dict(name='test_rule_3', source='any', destination='any', interface='wan', protocol='tcp', after='top')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 0)

    @unittest.expectedFailure
    def test_rule_update_separator_top(self):
        """ test updating position of a rule to top """
        rule = dict(name='r1', source='any', destination='any', interface='vt1', after='top')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 0)
        self.check_separator_idx(rule['interface'], 'test_sep1', 1)
        self.check_separator_idx(rule['interface'], 'test_sep2', 4)

    @unittest.expectedFailure
    def test_rule_update_separator_bottom(self):
        """ test updating position of a rule to bottom """
        rule = dict(name='r1', source='any', destination='any', interface='vt1', before='bottom')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 3)
        self.check_separator_idx(rule['interface'], 'test_sep1', 0)
        self.check_separator_idx(rule['interface'], 'test_sep2', 3)

    @unittest.expectedFailure
    def test_rule_update_separator_before_first(self):
        """ test creation of a new rule at bottom """
        rule = dict(name='r3', source='any', destination='any', interface='vt1', before='r1')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 0)
        self.check_separator_idx(rule['interface'], 'test_sep1', 0)
        self.check_separator_idx(rule['interface'], 'test_sep2', 3)

    def test_rule_update_separator_after_third(self):
        """ test creation of a new rule at bottom """
        rule = dict(name='r1', source='any', destination='any', interface='vt1', after='r3')
        self.do_rule_update_test(rule)
        self.check_rule_idx(rule, 2)
        self.check_separator_idx(rule['interface'], 'test_sep1', 0)
        self.check_separator_idx(rule['interface'], 'test_sep2', 3)

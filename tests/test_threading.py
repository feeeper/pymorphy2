# -*- coding: utf-8 -*-
from __future__ import absolute_import
import concurrent.futures
import random
import pytest
import pymorphy2
from .utils import morph, assert_parse_is_correct
from .test_parsing import PARSES


def _check_analyzer(morph, parses):
    for word, normal_form, tag in parses:
        parse = morph.parse(word)
        assert_parse_is_correct(parse, word, normal_form, tag)


def _check_new_analyzer(parses):
    morph = pymorphy2.MorphAnalyzer()
    for word, normal_form, tag in parses:
        parse = morph.parse(word)
        assert_parse_is_correct(parse, word, normal_form, tag)


def _create_morph_analyzer(i):
    morph = pymorphy2.MorphAnalyzer()
    word, normal_form, tag = random.choice(PARSES)
    parse = morph.parse(word)
    assert_parse_is_correct(parse, word, normal_form, tag)


def test_threading_single_morph_analyzer():
    with concurrent.futures.ThreadPoolExecutor(3) as executor:
        res = list(executor.map(_check_analyzer, [morph]*10, [PARSES]*10))


@pytest.mark.xfail  # See https://github.com/kmike/pymorphy2/issues/37
def test_threading_multiple_morph_analyzers():
    with concurrent.futures.ThreadPoolExecutor(3) as executor:
        res = list(executor.map(_check_new_analyzer, [PARSES]*10))


@pytest.mark.xfail  # See https://github.com/kmike/pymorphy2/issues/37
def test_threading_create_analyzer():
    with concurrent.futures.ThreadPoolExecutor(3) as executor:
        res = list(executor.map(_create_morph_analyzer, range(10)))

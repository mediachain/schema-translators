"""
HACK BELOW: remove cwd from PYTHONPATH, so we use site_python's mediachain.utils correctly
"""
import sys
import os
base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

while True:
    try: 
        base_path_index = sys.path.index(base_path)
        sys.path.pop(base_path_index)
    except ValueError:
        break


import pytest
from mediachain.translation.utils import is_mediachain_object, is_canonical, \
    MEDIACHAIN_OBJECT_TAG

from mediachain.ingestion.directory_iterator import LocalFileIterator

from jsonschema import ValidationError

_TRANSLATORS_DIR = 'mediachain/translation/'
_TRANSLATORS = [t for t in os.listdir(_TRANSLATORS_DIR)
        if not t.startswith('_')]

@pytest.fixture(params=_TRANSLATORS)
def iterator(request):
    translator_id = request.param
    translator_dir = os.path.join(_TRANSLATORS_DIR, translator_id)
    data_dir = os.path.join(translator_dir, 'sample')

    full_path = 'mediachain.translation.' + translator_id + '.translator'
    #import pdb; pdb.set_trace()
    translator_module = __import__(full_path, globals(), locals(), [translator_id])
    translator = getattr(translator_module, translator_id.capitalize())
    return LocalFileIterator(translator, data_dir)


def test_parses_input(iterator):
    for item in iterator:
        assert_valid_iterator_output(item)
        assert_valid_translation_output(item['translated'])


def assert_valid_iterator_output(output):
    assert output['raw_content'], 'Iterator output missing key: "raw_content"'
    assert output['parsed'], 'Unable to parse raw input'
    assert output['translated'], 'Translator produced no output'


def assert_valid_translation_output(output):
    assert output['canonical'], 'Translator output missing key: "canonical"'
    canonical = output['canonical']
    assert_is_mediachain_object(canonical)
    assert_is_canonical(canonical)
    assert_has_meta_and_type(canonical)

    chain = output.get('chain', [])
    for cell in chain:
        assert_is_mediachain_object(cell)
        assert_has_meta_and_type(cell)


def assert_is_mediachain_object(obj):
    assert is_mediachain_object(obj), \
        'Translated record must contain dict key {}'.format(
            MEDIACHAIN_OBJECT_TAG)


def assert_is_canonical(obj):
    assert is_canonical(obj), 'Translated "canonical" record must' + \
                              'have type "entity" or "artefact"'


def assert_has_meta_and_type(obj):
    assert isinstance(obj['type'], basestring), \
        'Translated object must have "type" string'
    assert isinstance(obj['meta'], dict), \
        'Translated object must have "meta" dictionary'


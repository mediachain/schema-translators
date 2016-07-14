import importlib
import pytest
import os
from mediachain.translation.utils import is_mediachain_object, is_canonical, \
    MEDIACHAIN_OBJECT_TAG

from mediachain.ingestion.directory_iterator import LocalFileIterator

from jsonschema import ValidationError

_TRANSLATORS_DIR = 'mediachain/translation/'
_TRANSLATORS = os.listdir(_TRANSLATORS_DIR)

#def test_translator_lookup():
#    for translator_id in _TRANSLATOR_IDS:
#        assert get_translator(translator_id) is not None
#    with pytest.raises(LookupError):
#        get_translator('NonExistentTranslator')


# def test_raises_on_nonsense():
#     for translator_id in _TRANSLATOR_IDS:
#         translator = get_translator(translator_id)
#         with pytest.raises(ValidationError):
#             translator.validate({
#                 'some' : 'nonsense'
#                 })


@pytest.fixture(params=_TRANSLATORS)
def iterator(request):
    translator_id = request.param
    translator_dir = os.path.join(_TRANSLATORS_DIR, translator_id)
    data_dir = os.path.join(translator_dir, 'sample')
    translator_module = os.path.join(translator_dir, 'translator')
    translator = importlib.import_module('mediachain.translation.' + translator_id)
    return DirectoryIterator(translator, data_dir)


def test_parses_input(iterator):
    assert False
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


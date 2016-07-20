from __future__ import unicode_literals
from mediachain.translation.translator import Translator


class Example(Translator):

    @staticmethod
    def translator_id():
        return 'example'

    @staticmethod
    def translate(example_json):

        data = {
            '_id': example_json['id']
        }

        artwork_artefact = {
            u'__mediachain_object__': True,
            u'type': u'artefact',
            u'meta': {'data': data}
        }

        return {
            u'canonical': artwork_artefact,
            u'chain': []
        }

    @staticmethod
    def can_translate_file(file_path):
        return True


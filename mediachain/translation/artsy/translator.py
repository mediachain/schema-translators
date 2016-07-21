from __future__ import unicode_literals
import os
from mediachain.translation.translator import Translator

class Artsy(Translator):

    @staticmethod
    def translator_id():
        return 'artsy'

    @staticmethod
    def translate(json):
        # extract artwork Artefact
        data = {'_id': u'artsy_' + json['id'],
                'title': json['title'],
                'category': json['category'],
                'medium': json['medium'],
                'collecting_institution': json['collecting_institution'],
                'created_at': json['created_at'],
                'image_url': json['image_url']
                }

        if 'artist' in json:
            artist_name = json['artist']['name']
            data['artist'] = artist_name

            # extract artist Entity
            artist_entity = {
                '__mediachain_object__': True,
                'type': 'entity',
                'meta': {
                    'data': {
                        'name': artist_name
                    }
                }
            }

        data['thumbnail'] = {
            '__mediachain_asset__': True,
            'uri': json['image_url']
        }

        artwork_artefact = {
            '__mediachain_object__': True,
            'type': 'artefact',
            'meta': {'data': data}
        }

        translated = {
            'canonical': artwork_artefact,
            'chain': [
            ]
        }

        if artist_entity:
            chain_entry = {'__mediachain_object__': True,
                'type': 'artefactCreatedBy',
                'meta': {},
                'entity': artist_entity
            }
            translated['chain'].append(chain_entry)

        return translated

    @staticmethod
    def can_translate_file(file_path):
        ext = os.path.splitext(file_path)[-1]
        return ext.lower() == '.json'


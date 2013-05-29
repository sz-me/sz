from south.db import db


class Migration:

    def forwards(self, orm):
        db.rename_column('core_registrationprofile', 'confirmation_key', 'activation_key')
        db.delete_column(u'core_user', 'is_verified')

    def backwards(self, orm):
        db.rename_column('core_registrationprofile', 'activation_key', 'confirmation_key')
        db.add_column(u'core_user', 'is_verified',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)
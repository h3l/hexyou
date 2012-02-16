# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MemberHostShip'
        db.create_table('activity_memberhostship', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Activity'])),
            ('is_host', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('activity', ['MemberHostShip'])

        # Adding unique constraint on 'MemberHostShip', fields ['user', 'activity']
        db.create_unique('activity_memberhostship', ['user_id', 'activity_id'])

        # Removing M2M table for field participators on 'Activity'
        db.delete_table('activity_activity_participators')

        # Removing M2M table for field hosts on 'Activity'
        db.delete_table('activity_activity_hosts')

        # Adding unique constraint on 'HostShip', fields ['group', 'activity']
        db.create_unique('activity_hostship', ['group_id', 'activity_id'])

        # Changing field 'Location.parent'
        db.alter_column('activity_location', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Location'], null=True))


    def backwards(self, orm):
        
        # Removing unique constraint on 'HostShip', fields ['group', 'activity']
        db.delete_unique('activity_hostship', ['group_id', 'activity_id'])

        # Removing unique constraint on 'MemberHostShip', fields ['user', 'activity']
        db.delete_unique('activity_memberhostship', ['user_id', 'activity_id'])

        # Deleting model 'MemberHostShip'
        db.delete_table('activity_memberhostship')

        # Adding M2M table for field participators on 'Activity'
        db.create_table('activity_activity_participators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['activity.activity'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('activity_activity_participators', ['activity_id', 'user_id'])

        # Adding M2M table for field hosts on 'Activity'
        db.create_table('activity_activity_hosts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['activity.activity'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('activity_activity_hosts', ['activity_id', 'user_id'])

        # Changing field 'Location.parent'
        db.alter_column('activity_location', 'parent_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activity.Location']))


    models = {
        'activity.activity': {
            'Meta': {'object_name': 'Activity'},
            'activity_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['activity.ActivityType']"}),
            'avatar': ('django.db.models.fields.CharField', [], {'default': "'/static/images/no_avatar.png'", 'max_length': '100'}),
            'begin_time': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'host_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['group.Group']", 'through': "orm['activity.HostShip']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Location']"}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['activity.MemberHostShip']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'activity.activitytype': {
            'Meta': {'object_name': 'ActivityType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'activity.hostship': {
            'Meta': {'unique_together': "(('group', 'activity'),)", 'object_name': 'HostShip'},
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Activity']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['group.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'activity.location': {
            'Meta': {'object_name': 'Location'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Location']", 'null': 'True', 'blank': 'True'})
        },
        'activity.memberhostship': {
            'Meta': {'unique_together': "(('user', 'activity'),)", 'object_name': 'MemberHostShip'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activity.Activity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_host': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'avatar': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'bio': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'contact_fanfou': ('django.db.models.fields.CharField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_msn': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'contact_qq': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'contact_twitter': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'student_num': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'group.condition': {
            'Meta': {'object_name': 'Condition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'group.group': {
            'Meta': {'object_name': 'Group'},
            'avatar': ('django.db.models.fields.CharField', [], {'default': "'/static/images/no_avatar.png'", 'max_length': '512'}),
            'condition': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['group.Condition']"}),
            'create_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'founder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'founder'", 'to': "orm['auth.User']"}),
            'friend_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['group.Group']", 'symmetrical': 'False'}),
            'group_type': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['group.GroupType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'through': "orm['group.MemberShip']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'site': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'group.grouptype': {
            'Meta': {'object_name': 'GroupType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'group.membership': {
            'Meta': {'unique_together': "(('group', 'user'),)", 'object_name': 'MemberShip'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['group.Group']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['activity']
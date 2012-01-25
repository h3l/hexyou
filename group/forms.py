# -*- coding: utf-8 -*-  
from django import forms
from django.forms import ModelForm, RadioSelect, HiddenInput
from django.utils.safestring import mark_safe
from NearsideBindings.group.models import Group,MemberShip
from NearsideBindings.base.utils import timebaseslug
from django.core.validators import validate_slug
from django.core.exceptions import ValidationError
from NearsideBindings.settings import RESERVED_GROUP_SLUGS

def validate_slug_access(slug):
    if len(slug)<4 or slug in RESERVED_GROUP_SLUGS:
        raise ValidationError(u'"%s" is too short or reserved ' % slug)

class GroupForm(ModelForm):

    slug = forms.SlugField(required=True,validators=[validate_slug,validate_slug_access,],initial=timebaseslug,help_text="用于url，例如http://example.com/groups/slug")
    class Meta:
        model = Group
        exclude = ('founder','members')
        widgets = {
            'condition': RadioSelect(),
            'avatar': HiddenInput(),
        }
    
    def create_group(self,user):
        if self.is_valid():
            group=self.save(commit=False)
            group.founder=user
            group.save()
            membership=MemberShip.objects.create(user=user,group=group,is_admin=True)
            return (True,group,membership)
        else: return (False,None,None)
    def __getitem__(self,name):
        field=ModelForm.__getitem__(self,name)
        if field.errors:
            print "error: %s" % name
            self.fields[name].widget.attrs['class']=field.css_classes('error')
        return field


        


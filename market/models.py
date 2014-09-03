from market.utils import current_time_aware, gen_alphanum_key
from market.settings import HIGHRISE_CONFIG

import datetime
from django.utils import timezone

from django.db import models
import pyrise



class Signups(models.Model):
    
    key = models.CharField(max_length=10)
    email = models.EmailField(max_length=75)
    reg_datetime = models.DateTimeField('datetime registered')
    highrise_id = models.CharField(max_length=50, blank=True, null=True)

    def setup(self):
        self.key = gen_alphanum_key()
        self.reg_datetime = current_time_aware()
        self.create_highrise_account()
        self.save()        

    def create_highrise_account(self):

        #if not self.highrise_id: # and MODE == 'live':
        #    try:
        pyrise.Highrise.set_server(HIGHRISE_CONFIG['server'])
        pyrise.Highrise.auth(HIGHRISE_CONFIG['auth'])
        cust = pyrise.Person()
           
        cust.contact_data = pyrise.ContactData(email_addresses=[pyrise.EmailAddress(address=self.email, location='Home'),],)
        
        cust.first_name = self.email
        
        cust.save()
        cust.add_tag('landing-page')
        
        self.highrise_id = cust.id
        
        #    except:
        #        pass

    def add_highrise_tag(self, tag):

        if self.highrise_id:
            try:
                pyrise.Highrise.set_server(HIGHRISE_CONFIG['server'])
                pyrise.Highrise.auth(HIGHRISE_CONFIG['auth'])
                cust = pyrise.Person.get(self.highrise_id)
                cust.add_tag(tag)
            except:
                pass


 





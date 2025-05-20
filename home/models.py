from django.db import models
import django.utils.timezone
import datetime


        
class ShopifySite(models.Model):
    
    id = models.BigAutoField(primary_key=True)
    shopify_site = models.CharField(max_length=64, blank=True, null=True)
    access_token = models.CharField(max_length=64, blank=True, null=True)
    friendly_name = models.CharField(max_length=64, blank=True, null=True)
    parent_site = models.PositiveBigIntegerField(null=True)
    
    def __str__(self):
        return self.shopify_site
    
class ShopifyWebhook(models.Model):
    id = models.BigAutoField(primary_key=True)
    webhook_id = models.CharField(max_length=64, blank=True, null=False)
    webhook_status = models.CharField(max_length=64, blank=True, null=True)
    
    webhook_payload = models.TextField(blank=True,null=True,default="")
    trigger_date = models.DateTimeField(null=True,default=django.utils.timezone.now)
    def __str__(self):
        return self.webhook_id
    
class FunctionConfigOptions(models.Model):
    id = models.BigAutoField(primary_key=True)
    label = models.CharField(max_length=64,blank=False,null=False)
    value = models.CharField(max_length=64,blank=False,null=False)
    
    
class FunctionConfig(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64,blank=False,null=False)
    type = models.CharField(max_length=64,blank=False,null=False,choices={"number":"Number","boolean":"True/False","text":"Text Field","select":"Select Box","radio":"Radio Group","checkbox":"Checkbox Group"})
    label = models.CharField(max_length=64,blank=False,null=False)
    default_value =  models.TextField(null=True,default="")
    options = models.ManyToManyField(FunctionConfigOptions)
    
    
class functionConfigGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=64,blank=False,null=False,choices={"discount":"Discount Function","transform":"Cart Transform Function"})
    name = models.CharField(max_length=64,blank=False,null=False)
    function_id = models.CharField(max_length=64,blank=False,null=False)
    items = models.ManyToManyField(FunctionConfig)

class uploadedFile(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(null=False,max_length=64,db_index=True)
    uploadedFile = models.TextField()
    fileName = models.TextField(default="")
    contentType = models.TextField(default="")
    
    class Meta:
        db_table = "file_upload"
#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install smart_open[s3] ')


# In[190]:


import boto3


# ## Connection 

# In[192]:


session = boto3.Session( 
         region_name='gra',
         aws_access_key_id='74f3176ddbea46d88a3fa092a5a64b7b', 
         aws_secret_access_key='e0a24e4db96f4141ad67d3598f59f9b7')


#Then use the session to get the resource
s3 = session.resource('s3')

# my_bucket = s3.Bucket('stackvidhya')

# for my_bucket_object in my_bucket.objects.all():
#     print(my_bucket_object.key)


# In[193]:


s3


# In[194]:


s3 = boto3.resource(
    endpoint_url='https://s3.gra.cloud.ovh.net',
    service_name='s3', 
    region_name='gra',
    aws_access_key_id='74f3176ddbea46d88a3fa092a5a64b7b',
    aws_secret_access_key='e0a24e4db96f4141ad67d3598f59f9b7'
)

s3cli = boto3.client(
    endpoint_url='https://s3.gra.cloud.ovh.net',
    service_name='s3', 
    region_name='gra',
    aws_access_key_id='74f3176ddbea46d88a3fa092a5a64b7b',
    aws_secret_access_key='e0a24e4db96f4141ad67d3598f59f9b7'
)

# endpoint-url 
# region = gra
# s3 signature_version=s3v4

#https://s3.gra.cloud.ovh.net
# gn.gonzalez


# ## listing objects

# In[195]:


s3.buckets.all()


# In[196]:


for bucket in s3.buckets.all():
    print(bucket)


# In[219]:


objects_lig = s3cli.list_objects(Bucket='lig')


# In[220]:


objects_lig = s3cli.list_objects(Bucket='lig')
get_folders_to_create(objects_lig['Contents'])


# In[199]:


objects = s3cli.list_objects_v2(Bucket='kodicare')


# In[ ]:


s3.download_file(Bucket='lig')


# In[215]:


folders = get_folders_to_create(objects_lig['Contents'])


# In[221]:


objects_lig['Contents']


# In[28]:


'2022-09_fr'
'2022-10_fr'


# In[225]:


print(objects_lig)


# In[224]:


prefix = '2022-07_fr/'
objects_lig = s3cli.list_objects_v2(Bucket='lig', Prefix=prefix)
print(len(objects_lig['Contents']))
## if len < 1000, else: run with paginator. 
get_objects(s3cli, page['Contents'])


# In[214]:


page['Contents']


# In[213]:


prefix = '2022-07_fr/'
paginator = s3cli.get_paginator('list_objects')
pages = paginator.paginate(Bucket='lig', Prefix=prefix)

for page in pages:
    folders = get_folders_to_create(page['Contents'])
    post_create_folders(folders)
    get_objects(s3cli, page['Contents'])


# ## Download doc by doc. 
# 1. create the required folders. 
# 2. run the following code: 
# 
# Functions :

# ### 1. create the required folders. 

# In[204]:


import os


# In[205]:


path_qwant_data = '/data1/home/mrim/gonzagab/Kodicare/qwant-data/'


# In[206]:


get_ipython().system('ls ')


# In[207]:


import numpy as np


# In[208]:


['/'.join(doc['Key'].split('/')[:-1]) for doc in page['Contents']]


# In[209]:


def get_folders_to_create(objects_list): 
    all_keys = ['/'.join(doc['Key'].split('/')[:-1]) for doc in objects_list]
    folders_to_create = np.unique(all_keys)
    folders_to_create = np.sort(folders_to_create)

    new_folders = []
    for folder in folders_to_create:
        sub_folders = folder.split('/')
        sub_folders = [fd for fd in ['/'.join(sub_folders[:-n]) for n in range(len(sub_folders))] if len(fd)> 0]
        for fd_i in sub_folders:
            new_folders.append(fd_i)
    new_folders = np.sort(np.unique(new_folders))


    folders_to_create = np.sort(np.unique(np.append(folders_to_create, new_folders)))
    return folders_to_create


# In[210]:


## Create directories
def post_create_folders(folders_to_create):
    for folder in folders_to_create: 
        if not os.path.isdir(folder):
            try:
                os.makedirs(path_qwant_data + folder)
                print("created:" + folder)
            except:
                print("error " + folder)
        else:
            print("exists: "+ folder)


# ### 2. run the following code to download

# In[211]:


def get_objects(s3cli, s3_objects): 
    for obj in s3_objects:
        try:
            s3cli.download_file('kodicare',obj['Key'], obj['Key'])
        except:
            print(obj['Key']) ## 


# ## Upload file

# In[182]:


def get_all_files(folder):
    f = []
    fullpath_f = []
    for (dirpath, dirnames, filenames) in walk(data_to_upload):
        f.extend(filenames)
        fullpath_f.extend([dirpath+ '/'+ x for x in filenames])
    return fullpath_f


# In[178]:


page['Contents']


# In[93]:


data_to_upload = '/home/mrim/galuscap/projects/qwant-data/2022-06_fr/collection'
data_to_upload1 = '/home/mrim/galuscap/projects/qwant-data/2022-06_fr/split-clean-collection'


# In[94]:


get_ipython().system('ls /home/mrim/galuscap/projects/qwant-data/2022-06_fr/split-clean-collection')


# In[95]:


get_ipython().system('ls /home/mrim/galuscap/projects/qwant-data/2022-06_fr/collection')


# In[76]:


import os
from os import listdir
from os.path import isfile, join
from os import walk


# In[183]:


list_docs_1 = get_all_files(data_to_upload)
list_docs_2 = get_all_files(data_to_upload1)


# In[184]:


list_docs_1


# In[ ]:


(filename, 'lig', filename.replace('/home/mrim/galuscap/projects/qwant-data/', ''))


# In[ ]:


get_ipython().run_cell_magic('time', '', "for filename in list_docs_1:\n    res = s3cli.upload_file(filename, 'lig', filename.replace('/home/mrim/galuscap/projects/qwant-data/', ''))\nres")


# In[ ]:


get_ipython().run_cell_magic('time', '', "for filename in list_docs_2:\n    res = s3cli.upload_file(filename, 'lig', filename.replace('/home/mrim/galuscap/projects/qwant-data/', ''))\nres")


# In[176]:


## To check ! 
prefix = '2022-06_fr/split-clean-collection'
paginator = s3cli.get_paginator('list_objects_v2')
pages = paginator.paginate(Bucket='lig', Prefix=prefix)

for page in pages:
    folders = get_folders_to_create(page['Contents'])
    print(folders)
#     get_objects(s3cli, page['Contents'])


# In[128]:


# Upload the file
s3_client = boto3.client('s3')
try:
    response = s3cli.upload_file(file_name, bucket, object_name)
except ClientError as e:
    logging.error(e)
    return False
return True


# ## Done :) 

# ### testing code --> to be ignored 

# In[42]:


get_ipython().system("cat '2022-09_fr/collection/LOG_kodicare.log'")


# In[ ]:





# In[172]:


len(objects['Contents'])


# In[13]:


get_ipython().system('pwd')


# In[35]:


#to download a file:
s3cli.download_file('kodicare', '2022-04_fr/urls.json', '2022-04_fr/urls.json')


# In[234]:


s3cli.download_file('kodicare', '2022-07_fr/id2query.json', '2022-07_fr/id2query.json')


# In[15]:


get_ipython().run_cell_magic('time', '', "s3cli.download_file('kodicare','2022-04_fr/clickmodel/data/part-00000-cc612722-57a8-44ef-bb31-f4ff9679536e-c000.json', '2022-04_fr/clickmodel/data/part-00000-cc612722-57a8-44ef-bb31-f4ff9679536e-c000.json')")


# In[9]:


bucket.objects.all()


# In[20]:


for bucket in s3.buckets.all():
    print(bucket.name)


# In[21]:


bucket


# In[10]:


get_ipython().run_cell_magic('time', '', '# Print out bucket names\nnames = []\nfor bucket in s3.buckets.all():\n    print(bucket.name)\n    for my_bucket_object in bucket.objects.all():\n        names.append(my_bucket_object.key)\n        print(my_bucket_object.key)')


# In[17]:


names[-10:]


# In[ ]:


for filename in names:
    s3cli.download_file('kodicare',filename, filename)


# In[12]:


names[:10]


# In[43]:


# Load csv file directly into python
obj = s3.Bucket('kodicare').Object('2022-04_fr/collection/collector_kodicare_1.txt').get()
obj


# In[47]:


import json


# In[45]:


import pandas as pd


# In[49]:


#
file_content = obj['Body'].read().decode('utf-8')
json_content = json.loads(file_content)
# foo = json.loads(obj['Body'])
json_content


# In[51]:


json_content


# In[46]:


foo = pd.read_csv(obj['Body'], index_col=0)


# In[ ]:





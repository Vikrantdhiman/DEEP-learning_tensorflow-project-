#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'> <img src='../Pierian_Data_Logo.png' /></a>
# ___

# In[1]:


import pandas as pd


# In[2]:


data = pd.read_csv('bank_note_data.csv')


# ** Check the head of the Data **

# In[3]:


data.head()


# In[4]:


import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


sns.countplot(x='Class',data=data)


# In[6]:


sns.pairplot(data,hue='Class')


# In[7]:


from sklearn.preprocessing import StandardScaler


# In[8]:


scaler = StandardScaler()


# In[9]:


scaler.fit(data.drop('Class',axis=1))


# In[10]:


scaled_features = scaler.fit_transform(data.drop('Class',axis=1))


# In[11]:


df_feat = pd.DataFrame(scaled_features,columns=data.columns[:-1])
df_feat.head()


# In[12]:


X = df_feat


# In[13]:


y = data['Class']


# In[14]:


from sklearn.model_selection import train_test_split


# In[15]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)


# In[16]:


import tensorflow as tf


# In[17]:


df_feat.columns


# In[18]:


image_var = tf.feature_column.numeric_column("Image.Var")
image_skew = tf.feature_column.numeric_column('Image.Skew')
image_curt = tf.feature_column.numeric_column('Image.Curt')
entropy =tf.feature_column.numeric_column('Entropy')


# In[19]:


feat_cols = [image_var,image_skew,image_curt,entropy]


# In[20]:


classifier = tf.estimator.DNNClassifier(hidden_units=[10, 20, 10], n_classes=2,feature_columns=feat_cols)


# In[21]:


input_func = tf.estimator.inputs.pandas_input_fn(x=X_train,y=y_train,batch_size=20,shuffle=True)


# In[22]:


classifier.train(input_fn=input_func,steps=500)


# ## Model Evaluation

# In[23]:


pred_fn = tf.estimator.inputs.pandas_input_fn(x=X_test,batch_size=len(X_test),shuffle=False)


# In[24]:


note_predictions = list(classifier.predict(input_fn=pred_fn))


# In[25]:


note_predictions[0]


# In[26]:


final_preds  = []
for pred in note_predictions:
    final_preds.append(pred['class_ids'][0])


# In[27]:


from sklearn.metrics import classification_report,confusion_matrix


# In[28]:


print(confusion_matrix(y_test,final_preds))


# In[29]:


print(classification_report(y_test,final_preds))


# In[30]:


from sklearn.ensemble import RandomForestClassifier


# In[31]:


rfc = RandomForestClassifier(n_estimators=200)


# In[32]:


rfc.fit(X_train,y_train)


# In[33]:


rfc_preds = rfc.predict(X_test)


# In[34]:


print(classification_report(y_test,rfc_preds))


# In[35]:


print(confusion_matrix(y_test,rfc_preds))


# ** It should have also done very well, possibly perfect! Hopefully you have seen the power of DNN! **

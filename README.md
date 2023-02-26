# snoring_endpoint01
Following is the project in brief:
1. I fine-tuned a Yamnet audio tf-model to classify audio (.wav files supported for now) into snoring or not-snoring. Trained on fresh audio data.
2. Containerised the model into tfserving, which is the default tensorflow serving docker container.
3. 2 other REST endpoints made for uploading .wav files, and downloading files ( but only if they are predicted as positive)
4. mongodb and mysql docker containers used in minikube. In case of GKE, mongodb atlas and mysql were both used from gcp service.
5. Works both on local minikube and Google Cloud - GKE.

# In works.
- Asynchronous calls to prediction endpoint could improve speed.
- Scaling test for real-world use

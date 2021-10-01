# Scientific-Computing

Scientific Computing in Python, Matlab/Octave, C++, and Julia

gcloud functions deploy name_to_certificate --runtime python37 --trigger-http --allow-unauthenticated

gcloud functions deploy trapezoidal --entry-point cloud_function --runtime python37 --trigger-http --allow-unauthenticated

https://cloud.google.com/source-repositories/docs/quickstart-integrating-with-cloud-functions#cloud-sdk_1

gcloud functions deploy trapezoidal \
--source https://source.developers.google.com/projects/$PROJECT_ID/repos/hello-world/moveable-aliases/master/paths/gcf_hello_world \
--trigger-http \
--runtime=nodejs8;

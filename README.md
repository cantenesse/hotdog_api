# hotdog_api

This a RESTFUL service that takes and image and returns `true` it's a hotdog and `false` if it's not. Currently only JPEGs are supported.

## Running locally
To run locally with uvicorn

```
uvicorn main:app --reload
```

## Example execution
### Download a photo of a hot dog
```
curl https://www.myduchess.com/wp-content/uploads/2021/01/DU-Image-2020-SandwichesGrill-Hotdog-FA-e1610389513139-825x315.jpg --output hotdog.jpg
```

### Download a photo of something else
```
curl https://hips.hearstapps.com/hmg-prod/images/little-cute-maltipoo-puppy-royalty-free-image-1652926025.jpg --output dog.jpg
```
### Send the hotdog photo to the endpoint
```
curl -X 'POST' \
  'http://localhost:8000/hotdog/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@hotdog.jpg;type=image/jpeg'
```

### Send the random photo to the endpoint
```
curl -X 'POST' \
  'http://localhost:8000/hotdog/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@dog.jpg;type=image/jpeg'
```

### Send the photo to my remotely deployed version of the server
```
curl -X 'POST' \
  'http://hotdog-lb-143137824.us-east-1.elb.amazonaws.com/hotdog/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@dog.jpg;type=image/jpeg'
```
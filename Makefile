clean:
	docker stop dnsovertls

build:
	docker build -t dnsovertls .

run: build
	docker run -d --rm --net=bridge --name dnsovertls dnsovertls

login:
	docker exec -it dnsovertls /bin/bash
 
verify:
	docker ps | grep dnsovertls